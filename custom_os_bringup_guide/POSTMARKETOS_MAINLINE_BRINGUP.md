# Mainline Linux & PostmarketOS Bringup Guide for Xiaomi Redmi Note 10 Pro (`sweet`)

## 1. Upstream Linux Mainline Kernel Status

The Qualcomm Snapdragon 732G (`SM7150-AC`) is closely related to the Snapdragon 730 (`SM7150`). In Linux kernel 6.6+ LTS and 6.10+, base SoC support exists in:
- `arch/arm64/boot/dts/qcom/sm7150.dtsi`
- Clock controllers: `drivers/clk/qcom/gcc-sm7150.c`, `drivers/clk/qcom/camcc-sm7150.c`, `drivers/clk/qcom/dispcc-sm7150.c`
- Pinctrl: `drivers/pinctrl/qcom/pinctrl-sm7150.c`
- Power domains: `drivers/soc/qcom/rpmhpd.c`

---

## 2. Hardware Bringup Matrix for Mainline Linux

| Subsystem | Mainline Driver | Status | Implementation Notes |
|---|---|---|---|
| **CPU (Kryo 470)** | `arm64`, `qcom-cpufreq-hw` | **Working** | Energy-Aware Scheduling (EAS), CPUFreq HW governor. |
| **GPU (Adreno 618)** | `freedreno`, `drm/msm` | **Working** | Fully accelerated via Mesa / Gallium `freedreno` and Vulkan `turnip`. |
| **Display (Samsung EA8076)**| `panel-samsung-ea8076` | **WIP / Staging** | Requires 4-lane MIPI DSI DCS driver with DSC 1.2 decompression support. |
| **Touchscreen (FocalTech)** | `focaltech_ft5446` | **Working** | Upstream standard `drivers/input/touchscreen/edt-ft5x06.c`. |
| **UFS Flash (Storage)** | `ufs-qcom` | **Working** | Standard Qualcomm UFS 2.2 host controller. |
| **Modem & Audio DSP** | `qcom_q6v5_pas` | **Working** | Hexagon ADSP/CDSP firmware loading via remoteproc. |
| **Audio (WCD937x)** | `snd-soc-wcd937x` | **Working** | Qualcomm SoundWire audio pipeline + ALSA UCM profile. |
| **Wi-Fi & Bluetooth** | `ath10k_snoc` / `hci_qca` | **Working** | WCN3990 firmware loaded via `ath10k/WCN3990/hw1.0/`. |
| **Sensors (IMU)** | `st_lsm6dso` | **Working** | IIO subsystem via SPI bus. |

---

## 3. PostmarketOS Device Package Blueprint

To create a native postmarketOS package (`device-xiaomi-sweet`):

```text
aports/device/testing/device-xiaomi-sweet/
├── APKBUILD
├── deviceinfo
└── modules-initfs
```

### `deviceinfo` Configuration:
```ini
deviceinfo_format_version="0"
deviceinfo_name="Xiaomi Redmi Note 10 Pro / Pro Max"
deviceinfo_manufacturer="Xiaomi"
deviceinfo_codename="xiaomi-sweet"
deviceinfo_year="2021"
deviceinfo_arch="aarch64"

# Boot image configuration
deviceinfo_flash_method="fastboot"
deviceinfo_generate_bootimg="true"
deviceinfo_bootimg_header_version="2"
deviceinfo_bootimg_pagesize="4096"
deviceinfo_kernel_cmdline="console=ttyMSM0,115200n8 earlycon=msm_geni_serial,0x880000 clk_ignore_unused pd_ignore_unused"
deviceinfo_dtb="sm7150-xiaomi-sweet"

# Display & UI
deviceinfo_screen_width="1080"
deviceinfo_screen_height="2400"
```
