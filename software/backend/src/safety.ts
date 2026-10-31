/**
 * Safety service: "walk me home" timers and live-location share links.
 * Privacy: the server never sees plaintext location. The device encrypts location updates with a
 * per-share key (XChaCha20-Poly1305 on device; key travels only in the share URL #fragment, which
 * browsers never send to servers). The server stores opaque ciphertext blobs + timestamps.
 */
import { randomBytes, randomUUID } from "node:crypto";

export type TimerStatus = "active" | "checked_in" | "overdue" | "cancelled";
export interface WalkHomeTimer {
  id: string;
  user_id: string;
  created_at: number;
  due_at: number;
  status: TimerStatus;
  contacts: string[];
  share_token: string;
  escalated_at?: number;
  locations: { t: number; ciphertext: string }[];
}
export interface Notifier {
  notify(contacts: string[], message: string): Promise<void>;
}
export class MockNotifier implements Notifier {
  sent: { contacts: string[]; message: string }[] = [];
  async notify(contacts: string[], message: string) {
    this.sent.push({ contacts, message });
  }
}

export class SafetyService {
  private timers = new Map<string, WalkHomeTimer>();
  private byToken = new Map<string, string>();
  constructor(private notifier: Notifier, private clock: () => number = Date.now, private publicBase = "https://lore.travel/s") {}

  start(user_id: string, eta_minutes: number, contacts: string[]): { timer: WalkHomeTimer; share_url_base: string } {
    if (!(eta_minutes > 0 && eta_minutes <= 240)) throw new RangeError("eta_minutes must be 1..240");
    if (!contacts.length) throw new RangeError("at least one contact required");
    const now = this.clock();
    const timer: WalkHomeTimer = {
      id: randomUUID(), user_id, created_at: now, due_at: now + eta_minutes * 60_000, status: "active", contacts,
      share_token: randomBytes(16).toString("base64url"), locations: [],
    };
    this.timers.set(timer.id, timer);
    this.byToken.set(timer.share_token, timer.id);
    // The device appends `#k=<key>` client-side; the server never learns the key.
    return { timer, share_url_base: `${this.publicBase}/${timer.share_token}` };
  }

  get(id: string): WalkHomeTimer | undefined {
    const t = this.timers.get(id);
    if (t) this.evaluate(t);
    return t;
  }

  checkIn(id: string): WalkHomeTimer {
    const t = this.mustGet(id);
    if (t.status === "active" || t.status === "overdue") t.status = "checked_in";
    return t;
  }

  extend(id: string, minutes: number): WalkHomeTimer {
    const t = this.mustGet(id);
    if (t.status !== "active") throw new Error(`cannot extend a ${t.status} timer`);
    t.due_at += minutes * 60_000;
    return t;
  }

  cancel(id: string): WalkHomeTimer {
    const t = this.mustGet(id);
    t.status = "cancelled";
    return t;
  }

  /** Store an end-to-end encrypted location blob (base64url). Rejects anything that looks like plaintext JSON. */
  pushLocation(id: string, ciphertext: string): void {
    const t = this.mustGet(id);
    if (!/^[A-Za-z0-9_-]{32,4096}$/.test(ciphertext)) throw new RangeError("ciphertext must be base64url (E2E encrypted on device)");
    t.locations.push({ t: this.clock(), ciphertext });
    if (t.locations.length > 500) t.locations.shift();
  }

  /** What a contact's browser fetches via the share link (it decrypts locally with the #fragment key). */
  shareView(token: string) {
    const id = this.byToken.get(token);
    const t = id ? this.get(id) : undefined;
    if (!t || t.status === "cancelled") return undefined;
    return { status: t.status, due_at: t.due_at, latest: t.locations.at(-1) ?? null, count: t.locations.length };
  }

  /** Run periodically (and on read): escalate overdue timers exactly once. */
  async sweep(): Promise<number> {
    let n = 0;
    for (const t of this.timers.values()) {
      this.evaluate(t);
      if (t.status === "overdue" && !t.escalated_at) {
        t.escalated_at = this.clock();
        await this.notifier.notify(t.contacts, `LORE safety: a walk-home check-in is overdue. Live location: ${this.publicBase}/${t.share_token}`);
        n++;
      }
    }
    return n;
  }

  private evaluate(t: WalkHomeTimer): void {
    if (t.status === "active" && this.clock() > t.due_at) t.status = "overdue";
  }

  private mustGet(id: string): WalkHomeTimer {
    const t = this.timers.get(id);
    if (!t) throw new Error("not found");
    return t;
  }
}
