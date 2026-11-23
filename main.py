#!/usr/bin/env python3
"""news-image-20261123 entrypoint.

Copies the repository's front-page image to /output/entry.png.
Standard library only, no network, deterministic: the bytes written are
exactly the bytes of entry.png in this repository.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
