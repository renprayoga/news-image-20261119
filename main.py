#!/usr/bin/env python3
"""Hand the finished poster to the bounty harness.

The picture itself lives next to this file as ``entry.png`` (drawn by
``draw.py``). This little program only has one job: put an exact copy of
that picture into the folder the harness points at, so the judges see the
same bytes I verified on my own machine.

Where the copy goes:
  * the folder named by ``MAKEFUN_OUTPUT_DIR`` when that variable is set, or
  * a folder called ``output`` in the current working directory otherwise.

Only the Python standard library is used, and nothing here touches the
network or the clock, so the copy is byte-for-byte identical every time.
"""

from __future__ import annotations

import os
from pathlib import Path

PICTURE_NAME = "entry.png"
FALLBACK_FOLDER = "output"


def pick_destination() -> Path:
    """Work out where the poster should be delivered."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if chosen:
        return Path(chosen)
    return Path.cwd() / FALLBACK_FOLDER


def deliver(picture: Path, destination: Path) -> Path:
    """Copy the poster byte for byte and report where it landed."""
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / picture.name
    target.write_bytes(picture.read_bytes())
    return target


def run() -> int:
    here = Path(__file__).resolve().parent
    picture = here / PICTURE_NAME
    if not picture.is_file():
        print(f"poster missing: expected {picture} next to this program")
        return 1
    target = deliver(picture, pick_destination())
    print(f"poster delivered to {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
