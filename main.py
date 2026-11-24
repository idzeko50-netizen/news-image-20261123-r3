#!/usr/bin/env python3
"""Entry point for news-image-20261123 round 3.

Copies entry/entry.png to MAKEFUN_OUTPUT_DIR (default /output) and
verifies the copy: PNG magic, 1024x1024 dimensions, size under 1 MiB,
and SHA-256 identical to the source. Standard library only, no network.
"""
import hashlib
import os
import shutil
import struct
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "entry", "entry.png")
MAX_BYTES = 1048576


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def png_dimensions(path):
    with open(path, "rb") as f:
        head = f.read(33)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file (bad magic bytes)")
    if head[12:16] != b"IHDR":
        raise ValueError("not a PNG file (no IHDR chunk)")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(SOURCE):
        print(f"missing source image: {SOURCE}", file=sys.stderr)
        return 1
    width, height = png_dimensions(SOURCE)
    if (width, height) != (1024, 1024):
        print(f"bad dimensions: {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        return 1
    size = os.path.getsize(SOURCE)
    if size > MAX_BYTES:
        print(f"image too large: {size} bytes > {MAX_BYTES}", file=sys.stderr)
        return 1
    before = sha256_of(SOURCE)
    shutil.copyfile(SOURCE, dest)
    os.chmod(dest, 0o644)
    after = sha256_of(dest)
    if after != before:
        print("SHA-256 mismatch after copy", file=sys.stderr)
        return 1
    if os.path.getsize(dest) != size:
        print("size mismatch after copy", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({width}x{height}, {size} bytes, sha256 {after})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
