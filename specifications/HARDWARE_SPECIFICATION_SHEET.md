# Xiaomi Redmi Note 10 Pro / Pro Max (`sweet` / `sweetin`) Complete Hardware Specification Sheet

## 1. System-on-Chip (SoC) Overview

| Parameter | Specification |
|---|---|
| **SoC Model** | Qualcomm Snapdragon 732G (`SM7150-AC` / `SDMMAGPIE`) |
| **Silicon Fabrication** | Samsung 8nm LPP (Low Power Plus) FinFET process |
| **Die Architecture** | 64-bit Armv8.2-A big.LITTLE heterogeneous multi-processing |
| **CPU Cluster 0 (Performance)** | 2× Kryo 470 Gold @ 2.30 GHz (Custom Arm Cortex-A76 derivative) |
| **CPU Cluster 1 (Efficiency)** | 6× Kryo 470 Silver @ 1.80 GHz (Custom Arm Cortex-A55 derivative) |
| **L2 / L3 Cache Architecture** | 256 KB L2 per Gold core; 128 KB L2 per Silver core; 1 MB shared L3 system cache |
| **Graphics Processing Unit** | Qualcomm Adreno 618 @ 800 MHz (Vulkan 1.1, OpenGL ES 3.2, OpenCL 2.0) |
| **Digital Signal Processor** | Qualcomm Hexagon 692 DSP with Hexagon Vector eXtensions (HVX) |
| **Image Signal Processor** | Qualcomm Spectra 350 ISP (Dual 14-bit image signal processors) |
| **Neural Processing** | Qualcomm 4th Generation AI Engine (up to 3.6 TOPS aggregate) |
| **Security Subsystem** | Qualcomm Secure Processing Unit (SPU), ARM TrustZone, crypto acceleration engine |

---

## 2. Memory & Storage Subsystem

| Parameter | Specification |
|---|---|
| **RAM Type** | LPDDR4X Dual-Channel (16-bit × 2) @ 1866 MHz |
| **RAM Capacities** | 6 GB / 8 GB configurations |
| **Internal Flash Storage** | UFS 2.2 (Universal Flash Storage, Dual-Lane Gear 3) |
| **Storage Capacities** | 64 GB / 128 GB (`SK Hynix` / `Micron` / `Samsung` NAND) |
| **Sequential Read / Write** | ~950 MB/s Read, ~480 MB/s Write |
| **Expandable Storage** | Dedicated MicroSDXC slot (up to 1 TB support, SD 3.0 UHS-I mode) |

---

## 3. Display & Touch Controller

### Primary OEM Display Panel
- **Manufacturer & Model:** Samsung Display EA8076 (`dsi_k6_38_0c_0a_fhd_dsc_video_display`)
- **Panel Type:** Super AMOLED (Rigid OLED, Pentile Matrix)
- **Dimensions:** 6.67 inches (155.6 mm × 70.0 mm active area)
- **Aspect Ratio:** 20:9
- **Resolution:** 1080 × 2400 pixels (FHD+, 395 ppi)
- **Refresh Rates Supported:** 60 Hz and 120 Hz dynamic switching
- **Touch Sampling Rate:** 240 Hz
- **Peak Brightness:** 1200 nits (HBM), 450 nits typical
- **Color Gamut:** 100% DCI-P3 wide color gamut, HDR10 compliant
- **Brightness Controller:** 11-bit PWM (`0` to `2047` range) via MIPI DCS `0x51` / `0x53` registers
- **Sysfs Backlight Interface:** `/sys/class/backlight/panel0-backlight/`

### Replacement / Secondary Display Variant
- **Panel Type:** Aftermarket IPS LCD / TFT panel
- **Backlight Mechanism:** External WLED backlight driven via PM6150L WLED driver
- **Sysfs Backlight Interface:** `/sys/class/leds/lcd-backlight/`
- **Supported Mode:** 60 Hz lock (120 Hz causes frame tearing or blackout on aftermarket bridges)

### Touchscreen Digitizer
- **Controller ICs:** FocalTech FT5446 / Goodix GT9886 / Novatek NT36672C (detected dynamically via DTBO)
- **Interface:** I2C bus (`/dev/i2c-2`), multi-touch up to 10 points
- **Input Event Node:** `/dev/input/event2` (`fts_ts` or `goodix_ts`)

---

## 4. Audio Subsystem & Speakers

| Component | Hardware Details |
|---|---|
| **Audio Codec** | Qualcomm WCD9370 / WCD9375 SoundWire audio codec |
| **Speaker Amplifiers** | Dual AWINIC AW882xx Smart Power Amplifiers (Top ear-piece speaker + Bottom main speaker) |
| **Acoustic Configuration** | Dual stereo speakers with independent audio chambers |
| **Microphone Array** | Dual noise-cancelling microphones (Primary bottom mic + Secondary top ambient mic) |
| **Headphone Jack** | 3.5mm analog audio jack with integrated impedance detection |
| **Hi-Res Audio Certification** | 24-bit / 192 kHz lossless audio output via ALSA |

---

## 5. Camera & Optical Sensors

| Camera Unit | Sensor Model | Resolution | Aperture & Lens | Features |
|---|---|---|---|---|
| **Primary Rear** | Samsung ISOCELL HM2 (`S5KHM2`) | 108 MP (12,000 × 9,000) | f/1.9, 1/1.52", 0.7µm | 9-in-1 Nonacell (12 MP 2.1µm), PDAF, 4K@30fps |
| **Ultra-Wide** | Sony IMX355 | 8 MP (3,264 × 2,448) | f/2.2, 1/4.0", 1.12µm | 118° Field of View (FOV) |
| **Telemacro** | OmniVision OV5675 | 5 MP (2,592 × 1,944) | f/2.4, 1/5.0", 1.12µm | 2× optical zoom macro, Autofocus (3cm - 10cm) |
| **Depth Sensor** | GalaxyCore GC02M1 | 2 MP (1,600 × 1,200) | f/2.4, 1/5.0", 1.75µm | Portrait depth calculation |
| **Front Selfie** | Sony IMX471 | 16 MP (4,608 × 3,456) | f/2.45, 1/3.06", 1.0µm | Fixed focus, HDR, 1080p@30/60fps |

---

## 6. Connectivity, Radio & Sensors

### Wireless Networking & Radio
- **WLAN / Bluetooth Chipset:** Qualcomm WCN3990 (integrated 2×2 MIMO Wi-Fi / BT)
- **Wi-Fi Standards:** 802.11 a/b/g/n/ac (2.4 GHz + 5.0 GHz dual-band, Wi-Fi Direct, Miracast)
- **Bluetooth:** Version 5.1 (A2DP, LE, aptX HD, aptX Adaptive, LDAC)
- **FM Radio:** Integrated FM receiver with RDS (requires wired 3.5mm headset as antenna)
- **NFC:** NXP SN100T NFC controller (Model variants with NFC: `sweet` Global / `M2101K6G`)
- **Infrared Transmitter:** Consumer IR Blaster (`/dev/spidev0.0` / `/sys/class/rc/rc0`)

### Cellular Modem & Bands
- **Modem:** Qualcomm Snapdragon X15 LTE (LTE-A Cat 15 DL 800 Mbps / Cat 13 UL 150 Mbps)
- **SIM Slots:** Dual Nano-SIM (4G Dual VoLTE standby) + Dedicated MicroSD tray
- **Supported Bands:**
  - FDD-LTE: B1 / B2 / B3 / B4 / B5 / B7 / B8 / B20 / B28
  - TDD-LTE: B38 / B40 / B41
  - 3G WCDMA: B1 / B2 / B4 / B5 / B8
  - 2G GSM: 850 / 900 / 1800 / 1900 MHz

### Hardware Sensors
- **Fingerprint:** Goodix / Fingerprint Cards (FPC) side-mounted capacitive sensor embedded in power key
- **Accelerometer & Gyroscope:** STMicroelectronics LSM6DSO / Bosch BMI260 (6-axis IMU via SPI)
- **Proximity Sensor:** Ultrasonic / Elliptic Labs virtual proximity sensor or physical optical sensor
- **Ambient Light Sensor:** Dual front and 360° rear light sensors (AMS TCS3701)
- **Compass / Magnetometer:** AKM AK09918 3-axis electronic compass
- **Vibration Motor:** Z-axis linear haptic motor (Qualcomm Haptics / AAC linear actuator)

---

## 7. Power, Charging & Battery Management

| Parameter | Specification |
|---|---|
| **Battery Model** | Xiaomi `BN53` |
| **Battery Chemistry** | Lithium-ion Polymer (Li-Po) |
| **Rated Capacity** | 4,920 mAh (minimum) / 5,020 mAh (typical) |
| **Nominal Voltage** | 3.87 V DC |
| **Charging Voltage Limit** | 4.45 V DC |
| **Primary Power Management IC** | Qualcomm PM6150 (System power, regulators, charging logic) |
| **Secondary Power Management IC** | Qualcomm PM6150L (Display bias, camera flash, WLED driver) |
| **Fast Charge Controller** | Qualcomm SMB1395 companion charge pump |
| **Wired Fast Charging** | 33W Turbo Charge (11V / 3A via proprietary protocol; 18W USB-PD / QC 4.0) |
| **Charge Times** | 0% to 59% in 30 minutes; 0% to 100% in ~74 minutes |
