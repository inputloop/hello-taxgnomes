#!/usr/bin/env python3
"""tg1bd -- TAXGNOMES 1 BUILD: the word game's tables and three dictionary sources, read at build
time, become four readings per word (north, south, east, west) plus the plain gloss.

usage: tg1bd.py            writes data/readings.json, data/readings.txt, data/words.txt,
                           data/drafts.txt and data/SOURCES; prints a summary line
Environment: TG_GAME (../mini-c4-game), TG_GCIDE (TG_GAME/sources/cache/gcide-0.53),
TG_SCOWL (/usr/share/hunspell/en_US.dic), TG_DRAFTS (drafts/), TG_OUT (data/).
The model is never called here: drafts already on disk are taken in, with their provenance.
Unfolded from hello-taxgnomes.org; edit that, not this.
Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
Mentat (for Corwin; claude-opus-5-5)
"""
import glob
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME = os.environ.get("TG_GAME", os.path.join(HERE, "..", "mini-c4-game"))
GCIDE = os.environ.get("TG_GCIDE", os.path.join(GAME, "sources", "cache", "gcide-0.53"))
SCOWL = os.environ.get("TG_SCOWL", "/usr/share/hunspell/en_US.dic")
DRAFTS = os.environ.get("TG_DRAFTS", os.path.join(HERE, "drafts"))
OUT = os.environ.get("TG_OUT", os.path.join(HERE, "data"))
TABLES = [("g", "GROWTH"), ("o", "OPTIMIZER"), ("r", "RECEIPT"), ("t", "TAG")]
VOICE = re.compile(r"[?!]|\b(I|me|my|you|your|we|us|let's)\b", re.I)
WORDS = re.compile(r"[A-Za-z']+")
E_TEMPLATES = [
    ("template:E1", "Listen: {w}. {G} -- and that is not nothing."),
    ("template:E2", "Oh, {w}! {G}, of all things."),
    ("template:E3", "{W}? Yes, {w}: {g}, and it hums quietly."),
    ("template:E4", "Say it slowly, {w}... {G}."),
]


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


DANGLING = {"a", "an", "the", "or", "and", "of", "to", "in", "as", "by", "with", "for", "etc"}


def clean(s):
    """Dictionary markup out: line breaks become slashes, tags go, glued quotes get a space."""
    s = s.replace("<br/", " / ")
    s = re.sub(r"<[^>]*>?", "", s)
    s = re.sub(r"([?!])([A-Za-z])", r"\1 \2", s)
    s = s.replace("[", "").replace("]", "")
    return " ".join(s.split())


def first_clause(s, limit=30):
    """The first clause, never cut mid-clause: past LIMIT words, cut at the last comma, and drop a
    dangling little word ("or a")."""
    s = clean(s).strip()
    s = re.split(r";\s|\.\s|\.$", s)[0].strip()
    w = s.split()
    if len(w) > limit:
        part = " ".join(w[:limit])
        k = part.rfind(",")
        s = part[:k] if k > len(part) // 3 else part
    w = s.rstrip(",:.").split()
    while w and w[-1].lower().strip(",.") in DANGLING:
        w.pop()
    return " ".join(w).rstrip(",:.")


def lower_first(s):
    return s[:1].lower() + s[1:] if s[:1].isupper() and s[1:2].islower() else s


def mean_len(s):
    t = WORDS.findall(s)
    return sum(len(x) for x in t) / len(t) if t else 99.0


def cap(s):
    return s[:1].upper() + s[1:] if s else s


def article(gloss):
    g = gloss.lower()
    if re.match(r"(a|an|the|one|any|some|something|someone)\b", g):
        return gloss
    return ("an " if g[:1] in "aeiou" else "a ") + gloss


def scowl_words():
    if not os.path.isfile(SCOWL):
        return None
    out = set()
    for i, line in enumerate(read(SCOWL).split("\n")):
        if i == 0 or not line:
            continue
        out.add(line.split("/")[0].lower())
    return out


def gcide_syns(wanted):
    if not os.path.isdir(GCIDE):
        return None
    syn, ent = {}, None
    for f in sorted(glob.glob(os.path.join(GCIDE, "CIDE.*"))):
        for line in read(f).split("\n"):
            m = re.search(r"<ent>([^<]+)</ent>", line)
            if m:
                ent = m.group(1).strip().upper()
            if "<syn>" in line and ent in wanted and ent not in syn:
                t = re.sub(r"<[^>]+>", "", line)
                t = t.split("Syn. --", 1)[-1]
                items = [x.strip(" .") for x in re.split(r"[,;]", t) if x.strip(" .")]
                items = [x for x in items if re.match(r"^[A-Za-z][A-Za-z -]{0,24}$", x)]
                if items:
                    syn[ent] = items[:4]
    return syn


def drafts():
    out = {}
    for f in sorted(glob.glob(os.path.join(DRAFTS, "*-E.json"))):
        m = re.match(r"(\d{4}-\d\d-\d\d)-(.+)-E\.json$", os.path.basename(f))
        if not m:
            continue
        model = m.group(2)
        for w, items in json.loads(read(f)).items():
            for it in items:
                out.setdefault(w.upper(), []).append(("draft:" + model, it["text"]))
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    present = {"wordnet-3.1+gcide-0.53 (game meanings)": os.path.isdir(os.path.join(GAME, "meanings")),
               "gcide-0.53 (synonyms)": os.path.isdir(GCIDE), "scowl (hunspell en_US)": os.path.isfile(SCOWL)}
    tables, words = [], {}
    for key, name in TABLES:
        heads = read(os.path.join(GAME, "taxonomy", "d", "m", key)).split()[1:]
        rows = []
        for line in read(os.path.join(GAME, "taxonomy", "m", key)).split("\n"):
            p = line.split()
            if len(p) != 5:
                continue
            rows.append([p[0], p[1:]])
            for i, w in enumerate(p[1:]):
                words[w] = {"table": name, "key": key, "row": p[0], "head": heads[i] if i < len(heads) else "",
                            "mates": [x for x in p[1:] if x != w]}
        tables.append({"key": key, "name": name, "heads": heads, "rows": rows})
    scowl = scowl_words()
    syns = gcide_syns(set(words)) or {}
    dr = drafts()
    counts = {"complete": 0, "none": 0, "E-draft": 0, "E-pool": 0, "E-template": 0}
    flat, wl, dl = [], [], []
    for w in sorted(words):
        rec = words[w]
        mpath = os.path.join(GAME, "meanings", w)
        wn = gc = None
        if os.path.isfile(mpath):
            for line in read(mpath).split("\n"):
                f = line.split("\t")
                if len(f) < 4 or not f[3].strip():
                    continue
                if f[1].startswith("wordnet") and not wn:
                    wn = (f[1], f[2], f[3].strip())
                elif f[1].startswith("gcide") and not gc:
                    gc = (f[1], f[2], f[3].strip())
        if not wn and not gc:
            rec["none"] = True
            counts["none"] += 1
            wl.append((w, "none"))
            continue
        pool = []
        ppath = os.path.join(GAME, "pool", w)
        if os.path.isfile(ppath):
            for line in read(ppath).split("\n"):
                f = line.split("\t")
                if len(f) < 3:
                    continue
                sent = clean(f[2])
                if "<" in f[2] and "<br/" not in f[2]:
                    continue
                if re.search(r"\b%s" % re.escape(w.lower()[:max(3, len(w) - 2)]), sent.lower()):
                    pool.append((f[1], sent))
        base = wn or gc
        pos = base[1] or "word"
        gloss = first_clause(base[2])
        lw = w.lower()
        R = {"baseline": {"text": "%s: %s." % (cap(lw), gloss), "sources": [base[0]]}}
        # north: the simpler of the two glosses, said plainly; then the shortest example
        simp = wn or gc
        sg = lower_first(first_clause(simp[2], 18))
        if pos == "verb":
            n1 = "To %s means to %s." % (lw, re.sub(r"^to ", "", sg))
        elif pos == "noun":
            n1 = "%s %s is %s." % ("An" if lw[:1] in "aeiou" else "A", lw, article(sg))
        else:
            n1 = "%s means %s." % (cap(lw), sg)
        nsrc = [simp[0], "scowl"] if scowl is not None else [simp[0]]
        short = sorted([p for p in pool if len(p[1].split()) <= 14 and not p[0].startswith("draft:")],
                       key=lambda p: (mean_len(p[1]), len(p[1])))
        if short:
            n1 += " For example: " + short[0][1].rstrip(".") + "."
            nsrc.append("pool:" + short[0][0])
        R["N"] = {"text": n1, "sources": nsrc}
        # south: one dense line, then the unpacking
        dense = gc if gc and len(first_clause(gc[2], 30).split()) >= 4 else (wn or gc)
        d1 = "%s: %s." % (w, first_clause(dense[2], 30))
        plain = first_clause((wn or gc)[2])
        where = "in the %s table it stands in row %s under %s, beside %s." % (rec["table"], rec["row"], rec["head"], ", ".join(rec["mates"]))
        un = "Unpacked: " + (where[:1].upper() + where[1:] if plain.lower() in d1.lower() else plain + "; " + where)
        R["S"] = {"text": d1 + " " + un, "sources": sorted({dense[0], (wn or gc)[0]}) + ["table:" + rec["key"]]}
        # east: a drafted sentence, else a pooled one with voice, else a template
        ed = [d for d in dr.get(w, []) if lw[:max(3, len(lw) - 2)] in d[1].lower() and len(d[1].split()) <= 25]
        voiced = [p for p in pool if VOICE.search(p[1]) and not p[0].startswith("draft:")]
        if ed:
            R["E"] = {"text": ed[0][1], "sources": [ed[0][0]]}
            counts["E-draft"] += 1
            dl.append((w, ed[0][0][len("draft:"):]))
        elif voiced:
            v = min(voiced, key=lambda p: len(p[1]))
            R["E"] = {"text": v[1], "sources": ["pool:" + v[0]]}
            counts["E-pool"] += 1
        else:
            k = int(hashlib.sha256(w.encode()).hexdigest(), 16) % len(E_TEMPLATES)
            name, t = E_TEMPLATES[k]
            R["E"] = {"text": t.format(w=lw, W=cap(lw), g=gloss, G=cap(gloss)), "sources": [name, base[0]]}
            counts["E-template"] += 1
        # west: plain, with the dictionary's synonyms
        wt = "%s (%s): %s." % (w, pos, gloss)
        wsrc = [base[0]]
        if w in syns:
            wt += " Synonyms: %s." % ", ".join(syns[w])
            wsrc.append("gcide-0.53")
        R["W"] = {"text": re.sub(r"[!?]", ".", wt), "sources": sorted(set(wsrc))}
        rec["pos"] = pos
        rec["readings"] = R
        counts["complete"] += 1
        wl.append((w, "meaning"))
        for d in ("baseline", "N", "S", "E", "W"):
            flat.append("%s\t%s\t%s\t%s" % (w, d, ",".join(R[d]["sources"]), R[d]["text"]))
    meta = {"title": "The Gnemonic Word Mines", "sources": present, "counts": counts,
            "grain": 4, "dictionary_sources": 3, "missing": [k for k, v in present.items() if not v]}
    with open(os.path.join(OUT, "readings.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": meta, "tables": tables, "words": words}, fh, ensure_ascii=False, indent=0, sort_keys=True)
    for name, lines in (("readings.txt", flat), ("words.txt", ["%s\t%s" % x for x in wl]), ("drafts.txt", ["%s\t%s" % x for x in dl])):
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + ("\n" if lines else ""))
    with open(os.path.join(OUT, "SOURCES"), "w", encoding="utf-8") as fh:
        for k, v in present.items():
            fh.write("%s\t%s\n" % ("present" if v else "MISSING", k))
    print("tg1bd: %d words; %d complete; %d with no meaning found; E: %d drafted, %d pooled, %d templated; missing sources: %s"
          % (len(words), counts["complete"], counts["none"], counts["E-draft"], counts["E-pool"], counts["E-template"],
             ", ".join(meta["missing"]) or "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
