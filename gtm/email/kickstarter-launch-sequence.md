# Kickstarter Launch Sequence

**Segments:** VIP ($1 reservers) · Engaged (opened or clicked in the last 30 days) · Rest of list · Backers (suppressed from "back us" emails once they pledge, via the Kickstarter backer export/BackerKit sync and by asking backers to click "I backed" to self-tag).
**Channels:** email + SMS (VIPs who opted in, US/UK/EU compliant) + IG Broadcast channel.
**Times are CEST.** Launch: Tue 25 May 2027, 15:00.

| # | When | Segment | Subject | Content / CTA |
|---|---|---|---|---|
| L-1 | Tue 18 May 10:00 | All | "One week. Here's everything you need to know." | Date, time (in each recipient's timezone via the ESP), tiers and prices, limits on early birds, "add to calendar" (.ics) |
| L-2 | Sun 23 May 18:00 | VIP | "48 hours, VIP. Your head start is 2 hours." | Exactly when the VIP link arrives (13:00 CEST on launch day); SMS opt-in |
| L-3 | Mon 24 May 18:00 | All non-VIP | "Tomorrow at 15:00 CEST" | Countdown GIF; "Super Early Birds are limited to 750 per model" |
| **L-4** | **Tue 25 May 13:00** | **VIP** | **"🔑 You're in early: LORE is live for VIPs"** | Direct link with a Kickstarter referral tag; tiers; "$1 credit + free clip will be applied in the pledge manager" |
| L-5 | Tue 25 May 15:00 | Engaged → Rest (waves of 5k, 10 min apart) | "LORE is live on Kickstarter" | Hero GIF, 3 bullets, prices, a single CTA button |
| L-6 | Tue 25 May 21:00 | Opened L-5, not backed | "Super Early Bird is going fast" | Real remaining-count (only if true at send time), a 2-line FAQ |
| L-7 | Wed 26 May 11:00 | Didn't open L-5 | "In case you missed it: LORE is live" | Resend with a new subject line |
| L-8 | Thu 27 May 18:00 | Backers | "Thank you! Can you help us reach [next stretch goal]?" | Referral link, share kit (pre-written posts), first stretch reveal |
| L-9 | Tue 1 Jun 10:00 | Non-backers | "Your questions, answered" | Top 6 objections (phone vs device, subscription, privacy, delivery risk, earphones, shipping/VAT) |
| L-10 | Mon 7 Jun 10:00 | Non-backers | "Halfway: what's new" | New add-on/bundle, creator reviews (real), city vote |
| L-11 | Mon 14 Jun 10:00 | All | "Field report: how accurate is LORE?" | Accuracy report (beta numbers + limits) |
| L-12 | Tue 22 Jun 15:00 | Non-backers | "48 hours left" | The last chance for KS pricing (retail later is $149/$299/$549) |
| L-13 | Thu 24 Jun 09:00 | Non-backers | "Last day: LORE closes at 15:00 CEST" | Short; countdown |
| L-14 | Thu 24 Jun 13:00 | Non-backers, opened L-13 | "2 hours left" | One line + button; SMS to VIP non-backers |
| L-15 | Thu 24 Jun 17:00 | Backers | "We did it. [N] founding walkers." | Final results, what happens next (pledge manager in ~7 days, monthly updates) |
| L-16 | Fri 25 Jun 10:00 | Non-backers | "Missed it? Late pledges are open" | BackerKit late-pledge store |

## Full copy: L-5 (launch email)

**Subject:** LORE is live on Kickstarter
**Preview:** From $99, and every street has a story.

> **It's live.**
> For the last [N] months we've been walking Rome with prototypes, checking facts and building LORE: a pocket-sized companion that tells you the stories of the city around you, through your own earphones.
>
> Today you can reserve yours:
> - **Pebble from $99** (retail $149)
> - **Square from $199** (retail $299): global data built in
> - **Atlas Founders Edition $399** (retail $549): numbered 001–500
>
> Super Early Bird prices are limited to the first 750 per model.
>
> [**Back LORE on Kickstarter →**]
>
> Grazie for being here from the start.
> Nimit
>
> *Shipping from Dec 2027 (Pebble/Square) and Apr 2028 (Atlas), estimated. Kickstarter is not a store: read our Risks & Challenges section before you back.*

## Full copy: L-12 (48 hours)
**Subject:** 48 hours left
> LORE closes on Kickstarter on Thursday at 15:00 CEST. After that, prices go to retail: $149, $299 and $549.
> [N] people from [N] countries have already backed it. If you've been waiting for a sign, this is the polite one. 🙂 [Back LORE →]

## Deliverability & compliance
Warm the domain from Feb 2027; send launch waves by engagement tier; plain-text versions; CAN-SPAM/GDPR footer with the company address; no purchased lists; SMS only with explicit opt-in (TCPA/PECR).
