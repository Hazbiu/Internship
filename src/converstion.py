#!/usr/bin/env python3
"""
Robust USD → USDA converter
Works with usd-core / pxr inside a virtualenv
Safe for Isaac / Omniverse USD files with remote references
"""

import argparse
import os
import sys

def human_size(n: int) -> str:
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024
    return f"{n:.0f}PB"


def fail(msg, code=1):
    print(f"[ERROR] {msg}")
    sys.exit(code)


def main():
    parser = argparse.ArgumentParser(
        description="Convert USD file (.usd/.usdc/.usdz/.usda) → ASCII .usda"
    )
    parser.add_argument("input", help="Input USD file")
    parser.add_argument("-o", "--out", help="Output file (default: same name .usda)")
    parser.add_argument("--flatten", action="store_true",
                        help="Flatten stage (bakes references if resolvable)")
    parser.add_argument("--no-payloads", action="store_true",
                        help="Do NOT load payloads/references (recommended for Isaac/Omniverse)")
    args = parser.parse_args()

    in_file = args.input

    # ----------------------------
    # File checks
    # ----------------------------
    if not os.path.exists(in_file):
        fail(f"File not found: {in_file}")

    if not os.path.isfile(in_file):
        fail(f"Not a file: {in_file}")

    size = os.path.getsize(in_file)
    if size == 0:
        fail("File is empty (0 bytes)")

    print(f"[INFO] Input: {in_file} ({human_size(size)})")

    # ----------------------------
    # Output name
    # ----------------------------
    if args.out:
        out_file = args.out
    else:
        base, _ = os.path.splitext(in_file)
        out_file = base + ".usda"

    # ----------------------------
    # Import USD
    # ----------------------------
    try:
        from pxr import Usd, Sdf
    except Exception:
        fail("pxr not available. Activate your virtualenv with usd-core installed.")

    # ----------------------------
    # Validate layer
    # ----------------------------
    layer = Sdf.Layer.FindOrOpen(in_file)
    if layer is None:
        fail("USD cannot open this file as a layer (invalid/corrupt/not USD).")

    print(f"[INFO] Layer format: {layer.GetFileFormat().formatId}")

    # ----------------------------
    # Open stage safely
    # ----------------------------
    try:
        if args.no_payloads:
            stage = Usd.Stage.Open(in_file, load=Usd.Stage.LoadNone)
        else:
            stage = Usd.Stage.Open(in_file)
    except Exception as e:
        fail(f"Usd.Stage.Open failed: {e}")

    if stage is None:
        fail("Stage open returned None.")

    print("[INFO] Stage opened successfully")

    # ----------------------------
    # Export
    # ----------------------------
    try:
        if args.flatten:
            print("[INFO] Exporting FLATTENED stage...")
            ok = stage.Flatten().Export(out_file)
        else:
            print("[INFO] Exporting root layer...")
            ok = stage.GetRootLayer().Export(out_file)
    except Exception as e:
        fail(f"Export failed: {e}")

    if not ok:
        fail("Export returned False.")

    print(f"[SUCCESS] Converted → {out_file}")


if __name__ == "__main__":
    main()
