#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261125.

The entry is the front page this repository holds (entry.png): a
1024x1024 newspaper front page summing up Wednesday 25 November 2026,
drawn by compose.py with vector art only (no photographs, no network).
This program does no drawing and reaches no network: it copies that
one file to the grader's output directory, so both runs write
identical bytes. Python 3.13, standard library only.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil
from pathlib import Path

PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
_CHUNK = 1024 * 1024  # 1 MiB at a time; the image is about 140 KiB


def sha256_file(path: Path) -> str:
    """Streaming SHA-256 of a file, without loading it whole into memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(_CHUNK):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    with source.open("rb") as handle:
        magic = handle.read(8)
        handle.seek(-12, os.SEEK_END)
        tail = handle.read(12)
    if magic != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    if tail[4:8] != b"IEND":
        raise ValueError("entry.png is truncated: no IEND chunk")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    # Verify the copy landed whole: same size and same streaming hash
    # as the source, so a truncated or altered copy is caught even for
    # images far larger than memory.
    if dest.stat().st_size != source.stat().st_size:
        raise ValueError("copied entry.png has the wrong size")
    if sha256_file(dest) != sha256_file(source):
        raise ValueError("copied entry.png differs from the source")


if __name__ == "__main__":
    main()
