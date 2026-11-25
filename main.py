#!/usr/bin/env python3
"""The 3AM Fridge Text — the one line a smart fridge texts its owner at 3am.

Writes a single line to /output/entry.txt. The gate requires UTF-8 text of
1 to 140 characters, not only white space, on one line. The text is a fixed
literal, so repeated runs are byte-identical (deterministic, no network,
no model calls, no randomness, no clock).

The joke: the fridge light has staged an intervention about the owner's
midnight snacking — and the fridge, traitorously, agrees with the light.
It is a fresh angle — nothing about milk, ice, a door left open, or
leftovers organising — in the voice of an appliance that has been awake
all night, has opinions, and has decided 3am is the moment to speak.
"""

import os
from pathlib import Path

LINE = "3am. The light just staged an intervention. It says the midnight snacking has to stop, and honestly, it has a point."

MAX_CHARS = 140


def validate(text: str) -> str:
    """Enforce the gate before anything is written: one line, 1-140 chars."""
    if not text or not text.strip():
        raise SystemExit("entry must not be empty or only white space")
    if text != text.strip():
        raise SystemExit("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise SystemExit(f"entry is {len(text)} characters, over the 140 cap")
    text.encode("utf-8")  # must be encodable UTF-8
    return text


def main() -> None:
    text = validate(LINE)
    out = Path(os.environ.get("OUTPUT_PATH", "/output/entry.txt"))
    out.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the file holds exactly the one line, nothing else.
    out.write_text(text, encoding="utf-8")
    # Verify what landed: re-read and check it byte for byte.
    written = out.read_text(encoding="utf-8")
    if written != text:
        raise SystemExit("verification failed: file does not match the entry")
    if len(written) != len(text) or len(written.encode("utf-8")) > MAX_CHARS:
        raise SystemExit("verification failed: written entry breaks the gate")
    print(f"Wrote {len(text)} characters to {out}")


if __name__ == "__main__":
    main()
