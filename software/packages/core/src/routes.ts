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
  /** Places with magnetic disturbance (trams, buses, steel) used by the simulation's compass model. */
  magneticZones?: { at: LatLng; radiusM: number }[];
  /** Distances (m) where the simulated user presses "tell me more". */
  tellMeMoreAtM?: number[];
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
  magneticZones: [{ at: { lat: 41.9003, lng: 12.4808 }, radiusM: 40 }],
  tellMeMoreAtM: [335, 1185],
};

/**
 * Mumbai test route (founder's first real walks): Gateway of India -> Regal Circle -> Kala Ghoda ->
 * Flora Fountain (Hutatma Chowk) -> Horniman Circle -> Chhatrapati Shivaji Maharaj Terminus.
 * Hand-traced along Chhatrapati Shivaji Marg, MG Road, Veer Nariman Road and D. N. Road (approx. 10-30 m).
 */
export const MUMBAI_DEMO_ROUTE: DemoRoute = {
  id: "mumbai-fort-heritage",
  name: "Gateway of India to CSMT (simulated walk)",
  path: [
    { lat: 18.9219, lng: 72.8344, label: "Gateway of India" },
    { lat: 18.9226, lng: 72.8338, label: "Apollo Bunder" },
    { lat: 18.9234, lng: 72.8331 },
    { lat: 18.9241, lng: 72.8323, label: "Regal Circle" },
    { lat: 18.9250, lng: 72.8320 },
    { lat: 18.9260, lng: 72.8321, label: "MG Road" },
    { lat: 18.9270, lng: 72.8321, label: "Chhatrapati Shivaji Maharaj Vastu Sangrahalaya" },
    { lat: 18.9283, lng: 72.8322, label: "Kala Ghoda" },
    { lat: 18.9295, lng: 72.8320 },
    { lat: 18.9308, lng: 72.8318, label: "MG Road (Fort)" },
    { lat: 18.9320, lng: 72.8318, label: "Flora Fountain / Hutatma Chowk" },
    { lat: 18.9323, lng: 72.8330, label: "Veer Nariman Road" },
    { lat: 18.9326, lng: 72.8341, label: "St. Thomas Cathedral" },
    { lat: 18.9330, lng: 72.8350, label: "Horniman Circle" },
    { lat: 18.9341, lng: 72.8352 },
    { lat: 18.9356, lng: 72.8354, label: "D. N. Road" },
    { lat: 18.9372, lng: 72.8355 },
    { lat: 18.9386, lng: 72.8356 },
    { lat: 18.9396, lng: 72.8352, label: "Chhatrapati Shivaji Maharaj Terminus" },
  ],
  crossings: [
    { at: { lat: 18.9241, lng: 72.8323 }, radiusM: 20, name: "Regal Circle" },
    { at: { lat: 18.9283, lng: 72.8322 }, radiusM: 12, name: "Kala Ghoda junction" },
    { at: { lat: 18.9320, lng: 72.8318 }, radiusM: 18, name: "Hutatma Chowk" },
    { at: { lat: 18.9386, lng: 72.8356 }, radiusM: 18, name: "CSMT junction" },
  ],
  talkingWindowsM: [
    [900, 950],
    [1700, 1750],
  ],
  stops: [
    { atM: 0, seconds: 40, label: "Look at the Gateway" },
    { atM: 800, seconds: 45, label: "Kala Ghoda" },
    { atM: 1450, seconds: 40, label: "Horniman Circle" },
  ],
  magneticZones: [{ at: { lat: 18.9390, lng: 72.8355 }, radiusM: 50 }],
  tellMeMoreAtM: [810, 1460],
};

export const DEMO_ROUTES: Record<string, DemoRoute> = { rome: ROME_DEMO_ROUTE, mumbai: MUMBAI_DEMO_ROUTE };
