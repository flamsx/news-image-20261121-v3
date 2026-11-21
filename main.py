#!/usr/bin/env python3
"""Entry point: copy the pre-rendered front page to /output/entry.png.

Standard library only. The image was rendered locally with Pillow and the
Lexend font (see draw_v3.py); the grading sandbox ships no Pillow, so this
program just copies the shipped bytes, which keeps both runs byte-identical.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUT = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    with open(OUT, "rb") as fh:
        data = fh.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry is not a PNG"
    assert len(data) <= 1048576, "entry is over 1 MiB"
    print("wrote %s (%d bytes, sha256 %s)"
          % (OUT, len(data), hashlib.sha256(data).hexdigest()))


if __name__ == "__main__":
    main()
