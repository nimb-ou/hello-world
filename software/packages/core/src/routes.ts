/**
 * Demo walking route through central Rome used by the prototype's SIMULATION MODE and by
 * simulations/walk-sim.ts. Waypoints follow real streets (hand-traced; approximate to ~10 m).
 * Pantheon -> San Luigi dei Francesi -> Piazza Navona -> Pasquino -> Campo de' Fiori ->
 * Sant'Andrea della Valle -> Largo di Torre Argentina -> Piazza della Minerva -> Sant'Ignazio ->
 * Piazza di Pietra -> Via del Corso -> Trevi Fountain.
 *
 * `crossings` mark road crossings on busy streets (Corso Rinascimento, Corso Vittorio Emanuele II,
 * Largo Argentina, Via del Corso) where LORE must stay silent.
 */
import type { LatLng } from "./types.ts";

export interface DemoRoute {
  id: string;
  name: string;
  path: (LatLng & { label?: string })[];
  crossings: { at: LatLng; radiusM: number; name: string }[];
  /** Simulated companion conversation windows, in metres along the route. */
  talkingWindowsM: [number, number][];
  /** Simulated stops (metres along route, seconds standing). */
  stops: { atM: number; seconds: number; label: string }[];
}

export const ROME_DEMO_ROUTE: DemoRoute = {
  id: "rome-centro-classic",
  name: "Pantheon to Trevi (simulated walk)",
  path: [
    { lat: 41.89895, lng: 12.47685, label: "Piazza della Rotonda (Pantheon)" },
    { lat: 41.89935, lng: 12.47655 },
    { lat: 41.89945, lng: 12.4758, label: "Via Giustiniani" },
    { lat: 41.8995, lng: 12.4749, label: "San Luigi dei Francesi" },
    { lat: 41.8994, lng: 12.4741, label: "Corso del Rinascimento" },
    { lat: 41.8993, lng: 12.4735, label: "Piazza Navona (east side)" },
    { lat: 41.8988, lng: 12.4732, label: "Fountain of the Four Rivers" },
    { lat: 41.8981, lng: 12.4731 },
    { lat: 41.8978, lng: 12.4726, label: "Piazza di Pasquino" },
    { lat: 41.8972, lng: 12.4727, label: "Via di San Pantaleo" },
    { lat: 41.8967, lng: 12.4728, label: "Corso Vittorio Emanuele II" },
    { lat: 41.8962, lng: 12.4724 },
    { lat: 41.8957, lng: 12.4722, label: "Campo de' Fiori" },
    { lat: 41.8955, lng: 12.4730 },
    { lat: 41.8959, lng: 12.4737, label: "Sant'Andrea della Valle" },
    { lat: 41.8960, lng: 12.4750, label: "Corso Vittorio Emanuele II" },
    { lat: 41.8960, lng: 12.4762, label: "Largo di Torre Argentina" },
    { lat: 41.8964, lng: 12.4772 },
    { lat: 41.8972, lng: 12.4775, label: "Via dei Cestari" },
    { lat: 41.8979, lng: 12.4777, label: "Piazza della Minerva" },
    { lat: 41.8983, lng: 12.4783 },
    { lat: 41.8988, lng: 12.4793, label: "Piazza di Sant'Ignazio" },
    { lat: 41.8996, lng: 12.4796 },
    { lat: 41.8999, lng: 12.4801, label: "Piazza di Pietra" },
    { lat: 41.9003, lng: 12.4808, label: "Via del Corso" },
    { lat: 41.9006, lng: 12.4818, label: "Via delle Muratte" },
    { lat: 41.9008, lng: 12.4829, label: "Trevi Fountain" },
  ],
  crossings: [
    { at: { lat: 41.8994, lng: 12.4741 }, radiusM: 14, name: "Corso del Rinascimento" },
    { at: { lat: 41.8967, lng: 12.4728 }, radiusM: 14, name: "Corso Vittorio Emanuele II (west)" },
    { at: { lat: 41.8960, lng: 12.4762 }, radiusM: 18, name: "Largo di Torre Argentina" },
    { at: { lat: 41.9003, lng: 12.4808 }, radiusM: 14, name: "Via del Corso" },
  ],
  talkingWindowsM: [
    [700, 760],
    [1650, 1700],
  ],
  stops: [
    { atM: 330, seconds: 60, label: "Admire the Four Rivers" },
    { atM: 1180, seconds: 45, label: "Look at the temples of Largo Argentina" },
  ],
};
