#!/usr/bin/env python3
"""Draw N codepoints from the Yi Syllables block for the syllable inventory (D23).

Seeded random spread across U+A000-U+A48C: not contiguous, not in Yi's own
phonetic order, so our syllable structure has no correlation with Nuosu.
Writes spec/codepoints.json as an ordered list of "A0XX" hex strings.

Run once, when O1 fixes the count. Re-running with another seed or count is a
new decision and must be logged in decisions.md; the script refuses to
overwrite an existing file without --force.
"""
import argparse
import json
import random
import sys
from pathlib import Path

BLOCK = (0xA000, 0xA48C)
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "spec" / "codepoints.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, required=True, help="syllable inventory size (O1)")
    ap.add_argument("--seed", type=int, default=20260914)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if OUT.exists() and not a.force:
        print(f"{OUT} exists; changing it is a decision (see decisions.md). Use --force.", file=sys.stderr)
        return 2
    pool = list(range(BLOCK[0], BLOCK[1] + 1))
    cps = sorted(random.Random(a.seed).sample(pool, a.count))
    OUT.write_text(json.dumps({
        "block": "yi", "seed": a.seed, "count": a.count,
        "codepoints": [f"{c:04X}" for c in cps],
    }, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {a.count} codepoints, seed {a.seed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
