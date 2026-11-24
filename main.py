"""Entry point for the 23 November 2026 world-news image.

What it does, in order:
  1. Renders the front page (see tools/draw.py) to entry.png next to
     this file, so the picture always matches the current renderer.
  2. Copies that PNG to the grader's output directory
     (MAKEFUN_OUTPUT_DIR, or "output" when unset) as entry.png.
  3. Reads the copy back and checks it is byte-for-byte identical to
     the original, then prints a short confirmation line.

No network, no clock, no randomness: the same input always yields the
same bytes, so the grader's two runs agree.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from tools.draw import render  # noqa: E402


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    source = os.path.join(HERE, "entry.png")
    render(source)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)

    # Verify-after-copy: the delivered file must match the rendered one.
    if sha256_of(source) != sha256_of(target):
        print("ERROR: copied entry.png differs from rendered entry.png",
              file=sys.stderr)
        return 1

    size = os.path.getsize(target)
    if size > 1024 * 1024:
        print("ERROR: entry.png is %d bytes, over the 1 MiB cap"
              % size, file=sys.stderr)
        return 1

    print("wrote %s (%d bytes, sha256 %s)"
          % (target, size, sha256_of(target)))
    print("verified: copy matches rendered entry.png")
    return 0


if __name__ == "__main__":
    sys.exit(main())
