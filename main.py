# news-image-20261125 entrypoint: place the finished front page at
# /output/entry.png. compose.py already drew the page; this script only
# checks the bytes and writes them out, with no network and no drawing.

import os

NAME = "entry.png"
HEAD = b"\x89PNG\r\n\x1a\n"
TAIL = b"IEND"
LIMIT = 1048576


def _checked_bytes(path):
    with open(path, "rb") as handle:
        data = handle.read()
    if data[:8] != HEAD:
        raise SystemExit("entry.png: not a PNG file")
    if TAIL not in data[-16:]:
        raise SystemExit("entry.png: missing IEND trailer")
    if len(data) > LIMIT:
        raise SystemExit("entry.png: larger than 1 MiB")
    return data


def publish():
    here = os.path.dirname(os.path.abspath(__file__))
    data = _checked_bytes(os.path.join(here, NAME))
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, NAME)
    with open(dest, "wb") as handle:
        handle.write(data)
    with open(dest, "rb") as handle:
        if handle.read() != data:
            raise SystemExit("entry.png: copy mismatch after write")


publish()
