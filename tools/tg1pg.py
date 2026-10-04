#!/usr/bin/env python3
"""tg1pg -- TAXGNOMES 1 PAGE: write build/hello-taxgnomes.html from page/template.html and
data/readings.json.  One file, offline; the readings are inlined.

usage: tg1pg.py [OUT.html]
Unfolded from hello-taxgnomes.org; edit that, not this.
Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
Mentat (for Corwin; claude-opus-5-5)
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv):
    out = argv[0] if argv else os.path.join(HERE, "build", "hello-taxgnomes.html")
    t = open(os.path.join(HERE, "page", "template.html"), encoding="utf-8").read()
    data = json.load(open(os.path.join(HERE, "data", "readings.json"), encoding="utf-8"))
    marker = "/*__READINGS__*/null"
    if t.count(marker) != 1:
        sys.stderr.write("tg1pg: the template must hold the readings marker exactly once\n")
        return 2
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(t.replace(marker, blob))
    print("tg1pg: %s (%d bytes)" % (os.path.relpath(out, HERE), os.path.getsize(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
