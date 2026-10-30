/**
 * Heading fusion for Map Vision.
 *
 * Problem: the device must know which way the walker's BODY faces to say "on your left".
 * Sources and their failure modes:
 *  - Magnetometer/compass: absolute, available at rest, but biased by hard/soft iron and
 *    badly disturbed near cars, tram lines, steel shutters (very common in Rome).
 *  - GNSS course-over-ground: unbiased while walking > ~1 m/s, useless when slow/stopped,
 *    noisy in urban canyons.
 *  - Step direction (PDR): walking direction estimated from accelerometer during each step;
 *    moderately noisy but immune to magnetic disturbance.
 *  - Gyro yaw rate: excellent short-term relative rotation (drives the prediction step).
 *
 * `HeadingKalman` is a 2-state extended Kalman filter, state x = [heading, compassBias] (deg).
 * The bias state lets the filter learn a persistent compass offset whenever GNSS course or
 * step direction is trustworthy, and keep using the corrected compass when the user stops.
 *
 * `ComplementaryHeading` is a cheap fallback (used on the Pebble's low-power path).
 */
import { angleDiff, normalizeDeg } from "./geo.ts";

export interface CompassSample {
  t: number; // ms
  headingDeg: number;
  /** Magnetic field magnitude in microtesla, if available. Earth's field in Rome ~ 46 uT. */
  fieldUT?: number;
  /** Platform-reported accuracy (deg), e.g. iOS webkitCompassAccuracy. */
  accuracyDeg?: number;
}
export interface GpsCourseSample {
  t: number;
  courseDeg: number | null;
  speedMps: number;
  /** Horizontal accuracy in metres. */
  accuracyM?: number;
}
export interface StepSample {
  t: number;
  directionDeg: number;
  /** 0..1 quality from the step detector (peak regularity). */
  quality?: number;
}
export interface GyroSample {
  t: number;
  /** Yaw rate, deg/s, clockwise positive (already rotated into the horizontal plane). */
  yawRateDps: number;
}

export interface HeadingKalmanOptions {
  /** Process noise on heading (deg^2/s) without gyro. Walking people turn quickly. */
  qHeadingNoGyro?: number;
  /** Process noise on heading (deg^2/s) when gyro-propagated. */
  qHeadingGyro?: number;
  /** Bias random walk (deg^2/s). */
  qBias?: number;
  /** Expected Earth field magnitude (uT). */
  expectedFieldUT?: number;
  /** Fractional field deviation beyond which the compass is treated as disturbed. */
  fieldTolerance?: number;
  /** Mahalanobis gate (chi^2, 1 dof). 9 = 3 sigma. */
  gate?: number;
  compassSigmaDeg?: number;
  stepSigmaDeg?: number;
  minGpsSpeedMps?: number;
}

export interface HeadingEstimate {
  headingDeg: number;
  sigmaDeg: number;
  compassBiasDeg: number;
  /** "high" < 12 deg, "medium" < 30, "low" otherwise. Story engine avoids left/right claims on "low". */
  confidence: "high" | "medium" | "low";
  lastUpdate: number;
  rejected: { compass: number; gps: number; step: number };
}

export class HeadingKalman {
  // state
  private h = 0;
  private b = 0;
  // covariance [[p00, p01], [p01, p11]]
  private p00 = 180 ** 2;
  private p01 = 0;
  private p11 = 15 ** 2;
  private t: number | null = null;
  private lastGyro: GyroSample | null = null;
  private initialised = false;
  private rejected = { compass: 0, gps: 0, step: 0 };
  private readonly o: Required<HeadingKalmanOptions>;

  constructor(opts: HeadingKalmanOptions = {}) {
    this.o = {
      qHeadingNoGyro: 400,
      qHeadingGyro: 4,
      qBias: 0.05,
      expectedFieldUT: 46,
      fieldTolerance: 0.2,
      gate: 9,
      compassSigmaDeg: 10,
      stepSigmaDeg: 15,
      minGpsSpeedMps: 0.9,
      ...opts,
    };
  }

  /** Propagate state to time t (ms). Uses the most recent gyro rate if any. */
  predict(t: number): void {
    if (this.t === null) {
      this.t = t;
      return;
    }
    const dt = Math.max(0, (t - this.t) / 1000);
    if (dt === 0) return;
    const gyroFresh = this.lastGyro && t - this.lastGyro.t < 500;
    if (gyroFresh) this.h = normalizeDeg(this.h + this.lastGyro!.yawRateDps * dt);
    const q = gyroFresh ? this.o.qHeadingGyro : this.o.qHeadingNoGyro;
    this.p00 += q * dt;
    this.p11 += this.o.qBias * dt;
    this.t = t;
  }

  gyro(s: GyroSample): void {
    this.predict(s.t);
    this.lastGyro = s;
  }

  /** Generic scalar update. H = [1, hb] where hb = 1 for compass (measures heading + bias). */
  private update(z: number, r: number, hb: 0 | 1, kind: keyof HeadingEstimate["rejected"]): boolean {
    const pred = this.h + hb * this.b;
    const y = angleDiff(pred, z); // wrapped innovation
    // S = H P H^T + R
    const s = this.p00 + 2 * hb * this.p01 + hb * hb * this.p11 + r;
    if (this.initialised && (y * y) / s > this.o.gate) {
      this.rejected[kind]++;
      return false;
    }
    // K = P H^T / S
    const k0 = (this.p00 + hb * this.p01) / s;
    const k1 = (this.p01 + hb * this.p11) / s;
    this.h = normalizeDeg(this.h + k0 * y);
    this.b = this.b + k1 * y;
    // P = (I - K H) P
    const h0 = 1;
    const h1 = hb;
    const n00 = (1 - k0 * h0) * this.p00 - k0 * h1 * this.p01;
    const n01 = (1 - k0 * h0) * this.p01 - k0 * h1 * this.p11;
    const n11 = -k1 * h0 * this.p01 + (1 - k1 * h1) * this.p11;
    this.p00 = Math.max(n00, 1e-6);
    this.p01 = n01;
    this.p11 = Math.max(n11, 1e-6);
    return true;
  }

  /** Returns false if the sample was rejected (disturbed field or outlier). */
  compass(s: CompassSample): boolean {
    this.predict(s.t);
    if (s.fieldUT !== undefined) {
      const dev = Math.abs(s.fieldUT - this.o.expectedFieldUT) / this.o.expectedFieldUT;
      if (dev > this.o.fieldTolerance) {
        this.rejected.compass++;
        return false;
      }
    }
    const sigma = Math.max(this.o.compassSigmaDeg, s.accuracyDeg ?? 0);
    if (!this.initialised) {
      this.h = normalizeDeg(s.headingDeg - this.b);
      this.p00 = sigma * sigma + this.p11;
      this.p01 = -this.p11; // h = z - b  =>  cov(h, b) = -var(b)
      this.initialised = true;
      return true;
    }
    return this.update(s.headingDeg, sigma * sigma, 1, "compass");
  }

  gps(s: GpsCourseSample): boolean {
    this.predict(s.t);
    if (s.courseDeg === null || !Number.isFinite(s.courseDeg) || s.speedMps < this.o.minGpsSpeedMps) return false;
    // Course noise ~ position noise / distance travelled per fix. Empirical: 25 deg at 1 m/s, floor 4 deg.
    const acc = s.accuracyM ?? 5;
    const sigma = Math.max(4, (5 * acc) / Math.max(s.speedMps, 0.1));
    if (!this.initialised) {
      this.h = normalizeDeg(s.courseDeg);
      this.p00 = sigma * sigma;
      this.initialised = true;
      return true;
    }
    return this.update(s.courseDeg, sigma * sigma, 0, "gps");
  }

  step(s: StepSample): boolean {
    this.predict(s.t);
    const q = Math.max(0.2, Math.min(1, s.quality ?? 0.7));
    const sigma = this.o.stepSigmaDeg / q;
    if (!this.initialised) {
      this.h = normalizeDeg(s.directionDeg);
      this.p00 = sigma * sigma;
      this.initialised = true;
      return true;
    }
    return this.update(s.directionDeg, sigma * sigma, 0, "step");
  }

  estimate(t?: number): HeadingEstimate {
    if (t !== undefined) this.predict(t);
    const sigma = Math.sqrt(this.p00);
    return {
      headingDeg: normalizeDeg(this.h),
      sigmaDeg: sigma,
      compassBiasDeg: this.b,
      confidence: !this.initialised ? "low" : sigma < 12 ? "high" : sigma < 30 ? "medium" : "low",
      lastUpdate: this.t ?? 0,
      rejected: { ...this.rejected },
    };
  }
}

/**
 * Complementary filter: integrate gyro, pull slowly towards the best absolute reference.
 * alpha = fraction of correction per update (0..1).
 */
export class ComplementaryHeading {
  private h: number | null = null;
  private t: number | null = null;
  constructor(private readonly alpha = 0.05) {}

  update(t: number, absoluteDeg: number | null, yawRateDps = 0): number {
    if (this.h === null) {
      this.h = normalizeDeg(absoluteDeg ?? 0);
      this.t = t;
      return this.h;
    }
    const dt = Math.max(0, (t - (this.t ?? t)) / 1000);
    this.h = normalizeDeg(this.h + yawRateDps * dt);
    if (absoluteDeg !== null) this.h = normalizeDeg(this.h + this.alpha * angleDiff(this.h, absoluteDeg));
    this.t = t;
    return this.h;
  }

  get value(): number | null {
    return this.h;
  }
}
