#!/usr/bin/env python3
"""tg1dr -- TAXGNOMES 1 DRAFTS: take in sentences the local model drafted for the east direction.

usage: tg1dr.py ingest MODEL ANSWER.json [DATE]   writes drafts/DATE-MODEL-E.json (merging, never
                                                  dropping); prints what was kept and why not
ANSWER.json is the model's {"WORD": "sentence", ...}.  A sentence is kept only if it uses the word
(or its stem) and runs 25 words or fewer.  The model is not called here.
Unfolded from hello-taxgnomes.org; edit that, not this.
Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
Mentat (for Corwin; claude-opus-5-5)
"""
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv):
    if len(argv) < 3 or argv[0] != "ingest":
        sys.stderr.write(__doc__)
        return 2
    model, path = argv[1], argv[2]
    date = argv[3] if len(argv) > 3 else datetime.date.today().isoformat()
    if not re.match(r"^[A-Za-z0-9._:-]+$", model):
        sys.stderr.write("tg1dr: a model name is letters, digits and ._:- only\n")
        return 2
    ans = json.load(open(path, encoding="utf-8"))
    out_path = os.path.join(HERE, "drafts", "%s-%s-E.json" % (date, model.replace(":", "-")))
    have = json.load(open(out_path, encoding="utf-8")) if os.path.exists(out_path) else {}
    kept = 0
    for w, s in sorted(ans.items()):
        w = w.upper()
        s = " ".join(str(s).split())
        stem = w.lower()[:max(3, len(w) - 2)]
        if stem not in s.lower():
            print("dropped %s: the sentence does not use the word" % w)
            continue
        if len(s.split()) > 25:
            print("dropped %s: longer than 25 words" % w)
            continue
        if any(x["text"] == s for x in have.get(w, [])):
            continue
        have.setdefault(w, []).append({"text": s})
        kept += 1
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(have, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    print("tg1dr: kept %d sentence(s) in %s" % (kept, os.path.relpath(out_path, HERE)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
