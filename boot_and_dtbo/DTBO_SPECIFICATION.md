# Xiaomi Redmi Note 10 Pro / Pro Max (`sweet`) DTBO Specification

## 1. Overview & Geometry

The Device Tree Blob Overlay (`dtbo`) partition on the Redmi Note 10 Pro (`/dev/block/sde45`) provides runtime board-specific hardware overlays applied on top of the base Qualcomm SDM730 / SM7150 device tree.

```text
+------------------------------------+
| DTBO Table Header (32 bytes)       | Magic: 0xd7b7ab1e (DT_TABLE_MAGIC)
+------------------------------------+
| Entry Descriptor #0 (32 bytes)     | dt_size: 268,280 bytes | Offset: 64
+------------------------------------+
| Flattened Device Tree Blob (DTB)   | Magic: 0xd00dfeed | Decompiled: sweet_dtbo.dts
+------------------------------------+
```

---

## 2. Table of Contents & Board Identifiers

| Parameter | Value | Description |
|---|---|---|
| **Magic** | `0xd7b7ab1e` | Android DTBO table magic |
| **Total Table Size** | `268,344 bytes` (262 KB) | Full DTBO partition payload |
| **Header Size** | `32 bytes` | Standard DTBO v0 header |
| **Entry Count** | `1` | Single unified board overlay |
| **Target Board Model** | `"SWEET"` | Redmi Note 10 Pro / Pro Max |
| **Compatible Strings** | `"qcom,sdmmagpie-qrd"`, `"qcom,sdmmagpie"`, `"qcom,qrd"` | Qualcomm SM7150 hardware family |
| **MSM ID** | `0x16d 0x00` (`365`) | Qualcomm Snapdragon 732G silicon ID |
| **Board ID** | `0x2e 0x00` (`46`) | Xiaomi Sweet hardware revision |

---

## 3. Key Hardware Nodes in `sweet_dtbo.dts`

The decompiled source code ([`sweet_dtbo.dts`](sweet_dtbo.dts)) spans **8,812 lines**. Key subsystem fragments include:

### 1. Display Controller & DSI Panel (`fragment@57` - `fragment@60`)
- **Node:** `dsi_k6_38_0c_0a_fhd_dsc_video_display`
- **Resolution:** 1080 × 2400 pixels
- **Timings:** H-active: 1080, H-front-porch: 48, H-back-porch: 24, H-sync: 12
- **DSI Lanes:** 4-lane MIPI DSI with DSC (Display Stream Compression)
- **Power Sequences:** 3-rail power supply (`vddio-supply`, `vdd-supply`, `vci-supply` via PM6150 / PM6150L LDOs)

### 2. Audio Subsystem (`fragment@0` - `fragment@10`)
- **SoundWire Bus Master:** Qualcomm SoundWire TX / RX / WSA masters
- **Audio Codec:** Qualcomm WCD937x codec linked via SoundWire
- **Smart PA:** Dual Awinic `aw882xx_smartpa@34` and `aw882xx_smartpa@35` on I2C bus

### 3. Touchscreen Controller (`fragment@45` - `fragment@48`)
- **FocalTech:** `focaltech@38` (FT5446) with interrupt pin `gpio31` and reset `gpio32`
- **Goodix:** `goodix@5d` (GT9886) fallback overlay

### 4. Charging & Battery (`fragment@75` - `fragment@80`)
- **Primary Charger:** `qcom,pm6150-charger`
- **Companion Charger:** `qcom,smb1395-charger` (enables 33W charge pump)
- **Battery Thermals:** `qcom,therm-node` mapped to `batt_therm` thermistor ADC channel

---

## 4. Decompilation & Compilation Commands

### Decompile DTB to DTS:
```bash
dtc -I dtb -O dts -o sweet_dtbo.dts sweet_dtbo.dtb
```

### Recompile DTS to DTB:
```bash
dtc -I dts -O dtb -o new_dtbo.dtb sweet_dtbo.dts
```

### Repack DTBO Image:
```bash
python3 /system/bin/mkdtboimg.py create new_dtbo.img --page_size=4096 new_dtbo.dtb
```
