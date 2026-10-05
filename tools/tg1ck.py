#!/usr/bin/env python3
"""tg1ck -- TAXGNOMES 1 CHECK: every word with a meaning has five readings, each with text and at
least one source; the complete count matches the build's own; no east reading shows a draft that
was retired (TG_DRAFTS, default drafts/).

usage: tg1ck.py DATA_DIR     exit 1 on a fault, with a line per fault
Unfolded from hello-taxgnomes.org; edit that, not this.
Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
Mentat (for Corwin; claude-opus-5-5)
"""
import glob
import json
import os
import sys

DRAFTS = os.environ.get("TG_DRAFTS", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "drafts"))
d = json.load(open(sys.argv[1] + "/readings.json", encoding="utf-8"))
bad = 0
for w, r in d["words"].items():
    if r.get("none"):
        continue
    R = r["readings"]
    if sorted(R) != ["E", "N", "S", "W", "baseline"]:
        print("FAIL %s: readings %s" % (w, sorted(R)))
        bad += 1
    for k, v in R.items():
        if not v["sources"] or not v["text"].strip():
            print("FAIL %s %s: empty text or no source" % (w, k))
            bad += 1
n = sum(1 for r in d["words"].values() if not r.get("none"))
if n != d["meta"]["counts"]["complete"]:
    print("FAIL complete count %d vs meta %d" % (n, d["meta"]["counts"]["complete"]))
    bad += 1
retired = set()
for f in glob.glob(os.path.join(DRAFTS, "*-E.json")):
    for w, items in json.load(open(f, encoding="utf-8")).items():
        retired.update((w.upper(), it["text"]) for it in items if it.get("retired"))
for w, r in d["words"].items():
    e = r.get("readings", {}).get("E")
    if e and (w.upper(), e["text"]) in retired:
        print("FAIL %s E: shows a draft that was retired" % w)
        bad += 1
sys.exit(1 if bad else 0)
