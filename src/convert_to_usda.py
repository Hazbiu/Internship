#!/usr/bin/env python3
import argparse
import os
import sys

def human_size(n: int) -> str:
    for unit in ["B","KB","MB","GB","TB"]:
        if n < 1024:
            return f"{n:.0f}{unit}"
        n /= 1024
    return f"{n:.0f}PB"

def main():
    p = argparse.ArgumentParser(
        description="Convert a USD-readable file to ASCII .usda using pxr (usd-core)."
    )
    p.add_argument("input", nargs="?", default=None,
                   help="Input file (e.g. scene.usdc). If omitted, tries to find a .usd/.usdc/.usda/.usdz in this directory.")
    p.add_argument("-o", "--out", default=None, help="Output .usda path (default: <input_basename>.usda)")
    p.add_argument("--flatten", action="store_true", help="Export flattened stage (bakes composition)")
    p.add_argument("--list", action="store_true", help="List USD-like files in this directory and exit")
    args = p.parse_args()

    here = os.path.abspath(os.path.dirname(__file__))

    # Gather candidates
    exts = (".usd", ".usdc", ".usda", ".usdz")
    candidates = [f for f in os.listdir(here) if f.lower().endswith(exts)]
    candidates.sort()

    if args.list:
        if not candidates:
            print("No .usd/.usdc/.usda/.usdz files found in:", here)
        else:
            print("USD-like files in:", here)
            for f in candidates:
                fp = os.path.join(here, f)
                try:
                    sz = os.path.getsize(fp)
                except OSError:
                    sz = -1
                print(f"  - {f}  ({human_size(sz) if sz >= 0 else 'size?'} )")
        return 0

    input_name = args.input
    if input_name is None:
        # Prefer scene.usdc if present, else first candidate
        if "scene.usdc" in candidates:
            input_name = "scene.usdc"
        elif candidates:
            input_name = candidates[0]
        else:
            print("ERROR: No input provided and no USD-like files found next to this script.", file=sys.stderr)
            print("Tip: run: python3 convert_to_usda.py --list", file=sys.stderr)
            return 2

    in_path = input_name if os.path.isabs(input_name) else os.path.join(here, input_name)

    # Basic file checks
    if not os.path.exists(in_path):
        print(f"ERROR: File not found: {in_path}", file=sys.stderr)
        print("Tip: run: python3 convert_to_usda.py --list", file=sys.stderr)
        return 2
    if not os.path.isfile(in_path):
        print(f"ERROR: Not a file: {in_path}", file=sys.stderr)
        return 2
    if not os.access(in_path, os.R_OK):
        print(f"ERROR: No read permission: {in_path}", file=sys.stderr)
        return 2

    try:
        size = os.path.getsize(in_path)
    except OSError as e:
        print(f"ERROR: Cannot stat file: {e}", file=sys.stderr)
        return 2

    print(f"Input : {in_path}")
    print(f"Size  : {human_size(size)}")
    if size == 0:
        print("ERROR: File is 0 bytes (empty).", file=sys.stderr)
        return 2

    out_path = args.out
    if out_path is None:
        base, _ = os.path.splitext(in_path)
        out_path = base + (".flattened.usda" if args.flatten else ".usda")
    else:
        out_path = out_path if os.path.isabs(out_path) else os.path.join(here, out_path)

    # Try to open via USD / SDF
    try:
        from pxr import Usd, Sdf
    except Exception as e:
        print("ERROR: Could not import pxr. Is your venv active and usd-core installed?", file=sys.stderr)
        print("Details:", e, file=sys.stderr)
        return 3

    # First: see if Sdf can open the layer at all (good diagnostic)
    layer = Sdf.Layer.FindOrOpen(in_path)
    if layer is None:
        print("ERROR: Sdf.Layer.FindOrOpen failed. USD cannot read this as a layer.", file=sys.stderr)
        print("Common causes:", file=sys.stderr)
        print("  - file is not a USD layer (wrong type/extension)", file=sys.stderr)
        print("  - file is corrupted or incomplete", file=sys.stderr)
        print("  - permissions / path issues", file=sys.stderr)
        return 4
    else:
        print(f"Layer : opened OK (format={layer.GetFileFormat().formatId})")

    # Then: open as a Stage (needed for flatten)
    try:
        stage = Usd.Stage.Open(in_path)
    except Exception as e:
        print("ERROR: Usd.Stage.Open failed.", file=sys.stderr)
        print("Details:", e, file=sys.stderr)
        return 5

    if stage is None:
        print("ERROR: Usd.Stage.Open returned None.", file=sys.stderr)
        return 5

    try:
        if args.flatten:
            ok = stage.Flatten().Export(out_path)
        else:
            ok = stage.GetRootLayer().Export(out_path)
    except Exception as e:
        print("ERROR: Export failed.", file=sys.stderr)
        print("Details:", e, file=sys.stderr)
        return 6

    if not ok:
        print("ERROR: Export returned False (no file written).", file=sys.stderr)
        return 6

    print(f"Output: {out_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
