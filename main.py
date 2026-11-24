#!/usr/bin/env python3
"""Copy the committed entry image to the grader output directory.

The image is pre-rendered and committed as entry.png next to this file.
This program does no rendering and writes nothing under the repo dir:
it only copies entry.png to the output directory and verifies the copy.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576  # 1 MiB
OUTPUT_NAME = "entry.png"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
    dst = os.path.join(out_dir, OUTPUT_NAME)

    if not os.path.isfile(src):
        print(f"error: source image not found: {src}", file=sys.stderr)
        return 1

    try:
        os.makedirs(out_dir, exist_ok=True)
        shutil.copyfile(src, dst)
    except OSError as exc:
        print(f"error: cannot copy entry image: {exc}", file=sys.stderr)
        return 1

    try:
        src_hash = sha256_file(src)
        dst_hash = sha256_file(dst)
    except OSError as exc:
        print(f"error: cannot verify copy: {exc}", file=sys.stderr)
        return 1

    if src_hash != dst_hash:
        print("error: copy is not byte-identical to source", file=sys.stderr)
        return 1

    size = os.path.getsize(dst)
    if size > MAX_BYTES:
        print(f"error: output too large: {size} bytes", file=sys.stderr)
        return 1

    print(f"ok: wrote {dst} ({size} bytes, sha256 {dst_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
