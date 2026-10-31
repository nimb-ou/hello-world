# Firmware Interfaces and Driver Requirements (for the Software team)

Platforms:
- **AP**: MediaTek Genio 520 (Pebble) / Genio 720 (Square, Atlas). Linux (Yocto) or AOSP without GMS; the decision is shared with Software.
- **Hub**: Nordic nRF54L15 running Zephyr / nRF Connect SDK.

Pin-level detail is in `schematics/pinmap.md`. Requirements marked **[HW-critical]** are needed to hit the battery and thermal targets in `simulations/results.md`.

## 1. Partitioning

| Concern | Runs on | Why |
|---|---|---|
| Sensor sampling, step/PDR, heading fusion (BSX on BHI360), buttons, SOS, LED/haptics, battery alarms, GNSS duty-cycling control | **Hub (+ BHI360 fusion core)** | Must keep working while the AP is suspended (about 85 % of walking time) **[HW-critical]** |
| Map-matching, Map Vision geometry (left/right/look-up), story selection, routing, ASR/LLM/TTS, BT audio source, LTE/Wi-Fi, UI, OTA, LPA (eSIM) | **AP** | |
| Secure boot, key storage, attestation, theft-lock | AP TrustZone/OP-TEE + SE050E | |

## 2. Hub ↔ AP protocol (UART1, 1 Mbps, COBS + CRC16, protobuf/nanopb)

Messages:
- `SensorBatch` (up to 2 s at 25 Hz fused heading, steps, baro, mag quality flag).
- `KeyEvent` (press / double / long / SOS).
- `GnssFix` (if the hub owns the GNSS UART in low-power mode).
- `PowerReq` (AP_WAKE reasons).
- `HapticCmd`, `LedPattern`, `FgStatus`.

Wake rules:
- The hub asserts **AP_WAKE** only for:
  - a key event;
  - a geofence or "approaching POI" trigger, which is precomputed by the AP into a hub-resident list of the next 32 POIs;
  - a low-battery alarm;
  - a GNSS outage longer than N seconds.
- The AP uses **HUB_IRQ_N** to push the POI list, LED and haptic commands.

**SOS path [safety-critical]:**
1. A 3 s long-press on SOS is debounced in hub hardware/firmware.
2. Haptic confirmation.
3. The hub wakes the AP and starts a 10 s cancel window.
4. If the AP does not acknowledge within 5 s, the hub resets it via PWRKEY. On the Atlas, the hub can power the BG95-S5 through the AP watchdog-recovery path.

The SOS logic must have a unit-tested state machine and a watchdog.

## 3. Driver list and requirements

| Device | Interface | Driver (Linux / Zephyr) | Requirements |
|---|---|---|---|
| Quectel EG25-G | USB2 (QMI/MBIM via `qmi_wwan`/`cdc_mbim`, `option` serial) + UART | ModemManager or a custom QMI service; AT over UART | **[HW-critical]** USB keeps the module awake (known Quectel behaviour). Use USB autosuspend + `AT+QSCLK=1` + DTR-controlled sleep. Wake on RI. Disable the module GNSS (`AT+QGPSEND`). Configure DRX/eDRX. Airplane mode cuts VBAT_LTE through LTE_PWR_EN |
| Infineon OC1230 eUICC | via modem USIM | **LPA** (SGP.22 LPAd, e.g. lpac-class open source or a partner SDK) | profile download over Wi-Fi or a bootstrap profile; SM-DP+ from the connectivity partner |
| Wi-Fi/BT combo | PCIe/SDIO + UART HCI | MediaTek vendor driver (mt76-class) + BlueZ (Linux) or Fluoride/Gabeldorsche (AOSP) | **A2DP Source** (SBC; AAC optional, licence needed), **LE Audio unicast client (BAP/CAP/VCP/MCP) + Auracast broadcast source**, HFP-AG for talk-back, GATT server for the phone app. Prefer LC3 when the sink supports it **[HW-critical]** |
| Quectel LC29HAA | UART (NMEA + PAIR binary) + 1PPS + WAKE/RST | gpsd or a custom parser; hub-side light parser | L1+L5 on; 1 Hz. **Duty-cycle 40 %** when PDR confidence is high **[HW-critical]**. Keep VBCKP alive for hot start (under 2 s). Inject time/position from LTE/Wi-Fi |
| BHI360 (+BMM350 aux) | SPI from hub | Bosch BHI360 SensorAPI + BSX fusion firmware image | virtual sensors: game rotation vector, geomagnetic RV, step counter/detector, PDR. Mag calibration-accuracy status forwarded to the AP EKF |
| BMP390 | I2C (hub) | Zephyr `bosch,bmp390` | 25 Hz while walking, used for "look up" / stairs |
| AMOLED | MIPI-DSI 1-lane (QSPI fallback) | DRM panel driver (MediaTek DSI) + DDIC init sequence from the panel vendor | 60 Hz UI / 15 Hz idle / AOD at 1 Hz, partial update; brightness from the ALS (optional, not in BOM); burn-in mitigation (pixel shift) |
| Touch | I2C2 | vendor input driver | gesture, wake-on-touch off by default |
| PAT9125 crown | I2C (hub) | custom Zephyr driver | motion IRQ; detent emulation with haptics |
| DRV2605L | I2C (hub) | Zephyr driver; ROM library + RTP | LRA auto-calibration at factory |
| TAS2563 | I2C1 + TDM | `tas2563` ALSA codec driver (upstream `tas2562` family) | speaker protection tuning file from TI PPC3; IV-sense as the AEC reference |
| PDM mics | PDM | ALSA DAI | 2-mic beamforming, wind NR, VAD for press-to-talk |
| BQ25620 | I2C0 | `bq256xx` power-supply driver (upstream) | JEITA, ship mode, input current limit, OTG off |
| MAX17262 | I2C0 | `max17042_battery` (upstream supports the max1726x family) | load the EZ model; report SoC/TTE to the UI |
| SE050E | I2C3 (secure) | NXP Plug&Trust middleware / OP-TEE TA | device identity certificate, attestation, LORE Pass entitlement keys, theft-lock |
| OV13B10 (Atlas) | CSI-2 4-lane | V4L2 sensor driver + MediaTek ISP tuning (needs ODM/ISP vendor tuning, ~6–8 weeks) | privacy LED is hard-wired to sensor power (cannot be disabled in software) |
| BG95-S5 (Atlas) | UART + PSM/WAKE | AT + Skylo NTN message API | SOS message flow only. Pointing/sky-view UX. Power off except during SOS or a weekly self-test |
| Genio NPU | – | NeuroPilot / LiteRT (TFLite) delegate; MediaTek GAI toolkit for LLMs ([model zoo](https://genio.mediatek.com/doc/iot-aihub/ai_hub/model_zoo/litert_gai/performance.html)) | INT4 weights, INT8/FP16 activations; budget below |

## 4. Power-management requirements [HW-critical]

1. Between stories the **AP must suspend** (suspend-to-RAM, target under 8 mW system with LTE in DRX). Pre-render the next story's audio, stream it to the combo chip, then suspend. Target AP awake ≤ 15 % while walking.
2. GNSS duty-cycling policy:
   - 40 % on in normal streets;
   - 100 % in the first 60 s after a turn or a map-matching ambiguity;
   - ≤ 20 % when stationary;
   - off when indoors (no fix for 60 s plus a barometer/Wi-Fi indoor hint).
3. Prefer LE Audio LC3 over A2DP SBC when available.
4. LTE: eDRX where the network supports it. Batch uploads. City-pack and model downloads only on Wi-Fi + charger.
5. Display: under 6 % on-time while walking; AOD off by default.
6. **Thermal governor:**
   - shell sensor (NTC on the mid-frame) target 41 °C;
   - NPU OPP step-down;
   - switch to cloud LLM when sustained load is over 60 s and LTE is good;
   - pocket detection (proximity/light or a mic heuristic) halves the power budget;
   - no on-device LLM while charging above 35 °C.
7. Battery: charge to 4.35 V by default ("travel longevity mode"), with 4.45 V "full" as a user option.

## 5. LLM / AI budget per SKU

| SKU | Resident models | Budget |
|---|---|---|
| Pebble | 1B INT4 (~0.65 GB) + ASR + TTS | ≤ 1.4 GB RAM; ~24 tok/s decode (E); bursts ≤ 15 s |
| Square | 3B INT4 (~1.75 GB) + ASR + TTS | ≤ 3 GB RAM; ~9 tok/s burst, ~4.5 tok/s thermally sustained (E) |
| Atlas | 3–4B INT4 + small VLM (~0.4 GB) | ≤ 4 GB RAM; camera → VLM ≤ 3 s per Glance |

## 6. Factory and test hooks required from firmware

- Factory test mode on pogo UART: AT-style command set for every peripheral.
- Sensor calibration upload: IMU 6-position; magnetometer hard/soft iron from the Helmholtz cage.
- RF test modes:
  - LTE: Quectel non-signalling `AT+QRFTEST`-class;
  - Wi-Fi/BT: DUT mode / MediaTek QA tool;
  - GNSS: C/N0 report.
- eSIM bootstrap provisioning.
- SE050 key injection via an HSM-signed blob.
- Ship mode entry.
- Logging of serial number, MAC/BD address, IMEI and EID to the MES.

## 7. OTA and security

- A/B partitions.
- Signed images (AVB on AOSP, or dm-verity on Yocto).
- Hub firmware updated by the AP over UART using MCUboot.
- Modem firmware via Quectel DFOTA.
- Rollback protection.
- Debug ports fused at PVT (SWD locked on the nRF54L15; JTAG disabled on the SoC).
