#!/usr/bin/env python3
"""
extract_boot.py - Android Boot Image Unpacker & Header Analyzer
Designed for Qualcomm SM7150 / Sweet hardware bringup.
"""
import os
import sys
import struct
import json

def unpack_boot_image(img_path, out_dir="boot_unpacked"):
    os.makedirs(out_dir, exist_ok=True)
    with open(img_path, "rb") as f:
        header = f.read(4096)
        magic = header[:8]
        if magic != b"ANDROID!":
            print(f"Error: Invalid magic '{magic}'. Not an Android boot image.")
            return False

        kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, second_size, second_addr, tags_addr, page_size, header_version = struct.unpack("<IIIIIIIII", header[8:44])
        os_version = struct.unpack("<I", header[44:48])[0]
        name = header[48:64].split(b"\0")[0].decode("utf-8", errors="ignore")
        cmdline = header[64:576].split(b"\0")[0].decode("utf-8", errors="ignore")
        extra_cmdline = header[576:1600].split(b"\0")[0].decode("utf-8", errors="ignore")
        if extra_cmdline:
            cmdline += " " + extra_cmdline

        meta = {
            "magic": "ANDROID!",
            "kernel_size": kernel_size,
            "kernel_addr": hex(kernel_addr),
            "ramdisk_size": ramdisk_size,
            "ramdisk_addr": hex(ramdisk_addr),
            "page_size": page_size,
            "header_version": header_version,
            "os_version": os_version,
            "name": name,
            "cmdline": cmdline
        }

        print(f"[+] Boot Header v{header_version} detected:")
        print(f"    Page Size:    {page_size}")
        print(f"    Kernel Size:  {kernel_size:,} bytes")
        print(f"    Ramdisk Size: {ramdisk_size:,} bytes")
        print(f"    Cmdline:      {cmdline}")

        with open(os.path.join(out_dir, "header_info.json"), "w") as jf:
            json.dump(meta, jf, indent=2)

        # Calculate offsets based on page boundary
        def page_align(val, psize):
            return ((val + psize - 1) // psize) * psize

        kernel_offset = page_size
        f.seek(kernel_offset)
        kernel_data = f.read(kernel_size)
        with open(os.path.join(out_dir, "kernel.gz"), "wb") as kf:
            kf.write(kernel_data)
        print(f"[✓] Extracted kernel to {out_dir}/kernel.gz")

        ramdisk_offset = kernel_offset + page_align(kernel_size, page_size)
        f.seek(ramdisk_offset)
        ramdisk_data = f.read(ramdisk_size)
        with open(os.path.join(out_dir, "ramdisk.cpio.gz"), "wb") as rf:
            rf.write(ramdisk_data)
        print(f"[✓] Extracted ramdisk to {out_dir}/ramdisk.cpio.gz")

    print("[SUCCESS] Unpack complete!")
    return True

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "/dev/block/bootdevice/by-name/boot"
    dest = sys.argv[2] if len(sys.argv) > 2 else "boot_unpacked"
    unpack_boot_image(src, dest)
