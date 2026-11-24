#!/usr/bin/env python3
"""Copy the committed front-page image to the output directory.

The entry image is rendered once and committed as entry.png. This script
does no rendering at all: it only copies the committed file, checks the
copy byte-for-byte, and reports the result. It never writes inside the
repository, so it runs fine when the repo is mounted read-only.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576  # 1 MiB


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

    if not os.path.isfile(source):
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    size = os.path.getsize(source)
    if size > MAX_BYTES:
        print(
            f"error: entry.png is {size} bytes, over the 1 MiB limit",
            file=sys.stderr,
        )
        return 1

    source_hash = sha256_of(source)

    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)

    copy_hash = sha256_of(target)
    if copy_hash != source_hash:
        print(
            f"error: copy hash mismatch: {copy_hash} != {source_hash}",
            file=sys.stderr,
        )
        return 1

    print(f"wrote {target} ({size} bytes, sha256 {copy_hash})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
