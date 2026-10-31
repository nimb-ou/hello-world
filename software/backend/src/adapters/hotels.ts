/**
 * Hotel / booking affiliate adapter interface. Production: Booking.com Affiliate Partner,
 * Expedia Rapid, or a meta layer (e.g. Travelpayouts). Mock returns clearly-labelled SIMULATED data.
 */
export interface HotelOffer {
  id: string;
  name: string;
  lat: number;
  lng: number;
  price_per_night_eur: number;
  rating: number;
  deeplink: string;
  provider: string;
  simulated: boolean;
}
export interface HotelQuery {
  lat: number;
  lng: number;
  checkin?: string;
  nights?: number;
  guests?: number;
  max_price_eur?: number;
}
export interface HotelAffiliateAdapter {
  readonly name: string;
  search(q: HotelQuery): Promise<HotelOffer[]>;
}

export class MockHotelAdapter implements HotelAffiliateAdapter {
  readonly name = "mock";
  async search(q: HotelQuery): Promise<HotelOffer[]> {
    const offers: HotelOffer[] = [0, 1, 2, 3].map((i) => ({
      id: `mock-${i}`,
      name: `[SIMULATED] Hotel ${["Alfa", "Bravo", "Charlie", "Delta"][i]}`,
      lat: +(q.lat + (i - 1.5) * 0.002).toFixed(5),
      lng: +(q.lng + (i - 1.5) * 0.002).toFixed(5),
      price_per_night_eur: 110 + i * 45,
      rating: 4.6 - i * 0.2,
      deeplink: `https://example.com/mock-affiliate?hotel=${i}&aid=LORE&checkin=${q.checkin ?? ""}`,
      provider: "mock",
      simulated: true,
    }));
    return offers.filter((o) => q.max_price_eur === undefined || o.price_per_night_eur <= q.max_price_eur);
  }
}
