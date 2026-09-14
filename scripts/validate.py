#!/usr/bin/env python3
"""Validate lexicon + corpus. Run before every commit. Exit 1 on any failure.

Checks (D11, D15):
  - every lexicon form uses only codepoints in spec/codepoints.json
  - no duplicate forms, no duplicate glosses
  - every form follows the syllable inventory
  - every lexicon word appears in >=3 train corpus sentences
  - every feature tag appears in >=10 train sentences
  - every corpus `st` string uses only known words
  - held/train split ratio

--add: interactive path to add a lexicon entry through validation.

STUB - implement once spec/codepoints.json exists.
"""
import sys

def main():
    print("validate.py: stub - nothing to validate yet (codepoints not assigned).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
