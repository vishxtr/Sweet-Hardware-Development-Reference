# Xiaomi Redmi Note 10 Pro / Pro Max (`sweet`) Boot Image Specification

## 1. Boot Image Architecture (Header Version 2)

The Redmi Note 10 Pro uses the standard **Android Boot Image Header Version 2** specification.

```text
+---------------------------------+
| Boot Image Header (Page 0)      | 4,096 bytes
+---------------------------------+
| Kernel (Image.gz)               | ~18 - 20 MB (Padded to 4096-byte page boundary)
+---------------------------------+
| Ramdisk (rootfs / initramfs)    | ~1.5 - 5.5 MB (Padded to page boundary)
+---------------------------------+
| Second Stage Loader             | 0 bytes (Unused on Qualcomm platforms)
+---------------------------------+
| Recovery DTBO                   | 0 bytes (Separated into dedicated dtbo partition)
+---------------------------------+
| Device Tree Blob (DTB)          | Appended to kernel Image.gz or included in header v2
+---------------------------------+
```

---

## 2. Verified Header Geometry

| Field | Value | Description |
|---|---|---|
| **Magic** | `ANDROID!` | 8-byte ASCII identifier |
| **Header Version** | `2` | Android 10/11 Boot Image v2 format |
| **Page Size** | `4,096 bytes` (`0x1000`) | Hardware NAND flash page size |
| **Kernel Load Address** | `0x00008000` | Physical RAM offset for 64-bit kernel execution |
| **Ramdisk Load Address** | `0x01000000` | Physical RAM offset for compressed cpio archive |
| **Tags Address** | `0x00000100` | ATAGS / flattened device tree pointer |
| **OS Version (Raw)** | `536871338` | Encodes Android 11 / 12 security patch level |

---

## 3. Kernel Command-Line Reference

### Stock Android / LineageOS Cmdline:
```text
console=ttyMSM0,115200n8 earlycon=msm_geni_serial,0x880000 androidboot.hardware=qcom androidboot.console=ttyMSM0 service_locator.enable=1 lpm_levels.sleep_disabled=0 loop.max_part=7
```

### Certified SweetLinux (Ubuntu Touch / Lomiri) Cmdline:
```text
androidboot.selinux=permissive console=ttyMSM0,115200n8 androidboot.hardware=qcom androidboot.console=ttyMSM0 androidboot.memcg=1 lpm_levels.sleep_disabled=1 msm_rtb.filter=0x237 service_locator.enable=1 swiotlb=1 androidboot.usbcontroller=a600000.dwc3 earlycon=msm_geni_serial,0x880000 loop.max_part=7 androidboot.init_fatal_reboot_target=bootloader kpti=off fsck.mode=force fsck.repair=yes no_console_suspend pm_debug_messages=0 msm_drm.dsi_display0=dsi_k6_38_0c_0a_fhd_dsc_video_display:
```

### Crucial Cmdline Parameters Explained:
- `msm_drm.dsi_display0=dsi_k6_38_0c_0a_fhd_dsc_video_display:`: Forces Qualcomm MSM DRM driver to bind directly to the Samsung Super AMOLED panel interface at boot.
- **Removed:** `video=vfb:enable` (must remain absent to prevent virtual framebuffer collision with DRM/KMS).
- **Removed:** `console=tty0` (must remain absent to prevent fbcon from interrupting MIPI DCS power-on sequence).
- `androidboot.selinux=permissive`: Allows non-standard userspace daemons and containers to access device nodes.
- `androidboot.memcg=1`: Enables Linux cgroups memory controller required by systemd.
- `swiotlb=1`: Allocates Software I/O Translation Lookaside Buffer for DMA access.

---

## 4. How to Unpack and Repack the Boot Image

### Using `mkbootimg` / `unpack_bootimg` (Python):
```bash
# Unpack
python3 -m unpack_bootimg --boot_img boot.img --out out_boot/

# Repack
python3 -m mkbootimg \
    --header_version 2 \
    --os_version 11.0.0 \
    --os_patch_level 2026-10 \
    --kernel out_boot/kernel \
    --ramdisk out_boot/ramdisk \
    --cmdline "..." \
    --pagesize 4096 \
    --output new_boot.img
```
