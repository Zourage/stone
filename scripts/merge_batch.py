#!/usr/bin/env python3
"""Merge a proposed batch (roots.json + sentences.json) into the lexicon and corpus.

Usage: merge_batch.py BATCH_DIR [--apply]

Without --apply: dry run. Reports which roots would pass the validator (schema,
syllables, Korean collision, duplicates) and which sentences would parse, and
writes nothing. With --apply: adds the roots via validate.py --add, appends the
sentences with fresh ids, then runs validate.py. Review the dry run first.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEX = ROOT / "lexicon/lexicon.json"
COR = ROOT / "corpus/corpus.jsonl"


def run_validate(args=()):
    r = subprocess.run([sys.executable, str(ROOT / "scripts/validate.py"), *args], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    batch = Path(sys.argv[1])
    apply = "--apply" in sys.argv
    roots = json.load(open(batch / "roots.json", encoding="utf-8"))
    sents = json.load(open(batch / "sentences.json", encoding="utf-8"))
    # work on copies
    lex_bak, cor_bak = LEX.read_bytes(), COR.read_bytes()
    ok_flag = [False]
    try:
        tmp = Path(tempfile.mkdtemp()) / "roots.json"
        json.dump(roots, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
        code, out = run_validate(["--add", str(tmp)])
        print(out.strip())
        if code != 0:
            print("roots rejected; fix the batch"); return 1
        n0 = sum(1 for l in COR.read_text(encoding="utf-8").splitlines() if l.strip())
        with open(COR, "a", encoding="utf-8") as f:
            for k, s in enumerate(sents, 1):
                s = {"id": f"s{n0 + k:04d}", "en": s["en"], "st": s["st"], "features": s.get("features", []), "split": s.get("split", "train")}
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        code, out = run_validate()
        print(out.strip())
        if code != 0:
            print("sentences rejected; fix the batch"); return 1
        if not apply:
            print(f"DRY RUN OK: {len(roots)} roots, {len(sents)} sentences would be added (s{n0+1:04d}–s{n0+len(sents):04d}). Nothing written.")
            return 0
        ok_flag[0] = True
        print(f"APPLIED: {len(roots)} roots, {len(sents)} sentences (s{n0+1:04d}–s{n0+len(sents):04d}).")
        return 0
    finally:
        if not apply or ok_flag[0] is False:
            LEX.write_bytes(lex_bak); COR.write_bytes(cor_bak)


if __name__ == "__main__":
    sys.exit(main())
