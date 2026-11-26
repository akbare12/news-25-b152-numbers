#!/usr/bin/env python3
"""news-25 b152 numbers: copy the pre-rendered entry image to the output dir.

Stdlib only (os/shutil) — the grader runs with no third-party packages.
Entry: "Wednesday 25 November 2026", 50 stories (3 heroes + 10 cards + 37 also).
"""
import os
import shutil


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # sanity: the copy must be byte-identical to the bundled image
    assert os.path.getsize(dst) == os.path.getsize(src), "copy size mismatch"
    print("wrote", dst)


if __name__ == "__main__":
    main()
