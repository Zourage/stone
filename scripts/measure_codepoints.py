#!/usr/bin/env python3
"""Measure token cost of PUA codepoints (D10).

For each codepoint in U+E000-U+F8FF, send a test string to the count_tokens
endpoint and record tokens per glyph. Output spec/codepoints_cost.json sorted
by cost. Assign the cheapest codepoints to the most frequent syllables.

Requires ANTHROPIC_API_KEY in the environment. Batch many codepoints per
request and difference the counts to stay rate-limit friendly.

Also usable for the shelved Hangul experiment (D6): --block hangul measures
U+AC00-U+D7A3 instead, to cross with a Korean frequency list.

STUB - implement in the first Claude Code session.
"""
import sys

def main():
    print("measure_codepoints.py: stub.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
