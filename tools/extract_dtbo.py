#!/usr/bin/env python3
"""
extract_dtbo.py - Android DTBO Table Extractor & Compiler
Designed for Qualcomm SM7150 / Sweet hardware bringup.
"""
import os
import sys
import struct
import subprocess

def extract_dtbo(dtbo_path, out_dir="dtbo_unpacked"):
    os.makedirs(out_dir, exist_ok=True)
    with open(dtbo_path, "rb") as f:
        header = f.read(32)
        magic = header[:4]
        if magic != b"\xd7\xb7\xab\x1e":
            print(f"Error: Invalid DTBO table magic '{magic}'.")
            return False

        total_size, header_size, dt_entry_size, dt_entry_count, dt_entries_offset, page_size, version = struct.unpack(">IIIIIII", header[4:32])
        print(f"[+] DTBO Table Detected:")
        print(f"    Total Size:     {total_size:,} bytes")
        print(f"    Entries:        {dt_entry_count}")
        print(f"    Page Size:      {page_size}")

        f.seek(dt_entries_offset)
        entries_data = f.read(dt_entry_size * dt_entry_count)

        for i in range(dt_entry_count):
            e_data = entries_data[i * dt_entry_size : (i + 1) * dt_entry_size]
            dt_size, dt_offset, dt_id, dt_rev, custom = struct.unpack(">IIIII", e_data[:20])
            print(f"    [Entry #{i}] Size: {dt_size:,} bytes, Offset: {dt_offset}, ID: {hex(dt_id)}, Rev: {dt_rev}")

            f.seek(dt_offset)
            blob = f.read(dt_size)
            dtb_out = os.path.join(out_dir, f"overlay_{i}.dtb")
            dts_out = os.path.join(out_dir, f"overlay_{i}.dts")

            with open(dtb_out, "wb") as bf:
                bf.write(blob)

            # Decompile with dtc if available
            try:
                subprocess.run(["dtc", "-I", "dtb", "-O", "dts", "-o", dts_out, dtb_out], check=True)
                print(f"    [✓] Decompiled Entry #{i} to {dts_out}")
            except Exception as e:
                print(f"    [!] Could not decompile dtb with dtc: {e}")

    print("[SUCCESS] DTBO extraction complete!")
    return True

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "/dev/block/bootdevice/by-name/dtbo"
    dest = sys.argv[2] if len(sys.argv) > 2 else "dtbo_unpacked"
    extract_dtbo(src, dest)
