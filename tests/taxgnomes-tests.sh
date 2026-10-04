#!/bin/sh
# taxgnomes-tests.sh -- hello-taxgnomes' checks.
# usage: sh tests/taxgnomes-tests.sh            the build is complete and honest
#        sh tests/taxgnomes-tests.sh --reader   the second reader agrees with the builder
#        sh tests/taxgnomes-tests.sh --prove-red    planted faults, each caught
#        sh tests/taxgnomes-tests.sh --cold     a build with no drafts completes and says so
#        sh tests/taxgnomes-tests.sh --offline  the page asks nothing of the network
#        sh tests/taxgnomes-tests.sh --egad     egadjit's resolver reads the category (needs ../egad)
# Builds into a scratch folder; the committed data/ is compared, never rewritten.
# Unfolded from hello-taxgnomes.org; edit that, not this.
# Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
# Mentat (for Corwin; claude-opus-5-5)
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
w=$(mktemp -d) || exit 2; trap 'rm -rf "$w"' EXIT
mode=${1:-}; fail=0
TG_GAME=${TG_GAME:-$(cd "$here/../mini-c4-game" 2>/dev/null && pwd)}; export TG_GAME
build() { # OUT [DRAFTS] [BUILDER]
  if [ -n "${2:-}" ]; then env TG_OUT="$1" TG_DRAFTS="$2" python3 "${3:-$here/tools/tg1bd.py}"
  else env TG_OUT="$1" python3 "${3:-$here/tools/tg1bd.py}"; fi
}
honest() { # DIR -> 0 when every word with a meaning has five readings, each with text and a source
  python3 "$here/tools/tg1ck.py" "$1"
}
plant() { # NAME AWKPROG -> the second reader must catch the fault planted in a copy of the build
  cp -R "$w/d" "$w/$1"; awk -F'\t' -v OFS='\t' "$2" "$w/d/readings.txt" > "$w/$1/readings.txt"
  cmp -s "$w/d/readings.txt" "$w/$1/readings.txt" && { echo "prove-red: $1 could not be planted"; r=1; return; }
  if sh "$here/tools/tg1rd" "$w/$1" > /dev/null; then echo "prove-red: $1 was NOT caught"; r=1; else echo "prove-red: $1 was caught"; fi
}
case $mode in
  ''|--reader)
    build "$w/d" > "$w/b.out" || { echo "FAIL the build"; exit 1; }
    for f in readings.json readings.txt words.txt drafts.txt SOURCES; do cmp -s "$w/d/$f" "$here/data/$f" || { echo "FAIL data/$f differs from a fresh build (run make build)"; fail=1; }; done
    grep -q 'missing sources: none' "$w/b.out" || { echo "FAIL a source is missing: $(cat "$w/b.out")"; fail=1; }
    honest "$w/d" || fail=1
    if [ "$mode" = --reader ]; then
      for a in awk mawk gawk; do command -v $a >/dev/null 2>&1 || continue
        TG1RD_AWK=$a sh "$here/tools/tg1rd" "$w/d" > "$w/r.$a" || { echo "FAIL the second reader ($a)"; grep FAULT "$w/r.$a" | head -3; fail=1; }
      done
      bc=$(sed -n 's/.*; \([0-9]*\) complete;.*/\1/p' "$w/b.out"); rc=$(sed -n 's/.*; \([0-9]*\) complete;.*/\1/p' "$w/r.awk")
      [ -n "$bc" ] && [ "$bc" = "$rc" ] || { echo "FAIL builder says $bc complete, reader $rc"; fail=1; }
      for a in mawk gawk; do [ -f "$w/r.$a" ] && { cmp -s "$w/r.awk" "$w/r.$a" || { echo "FAIL awk and $a read it differently"; fail=1; }; }; done
      [ $fail = 0 ] && echo "taxgnomes: the second reader agrees: $(cat "$w/r.awk")"
    else
      [ $fail = 0 ] && echo "taxgnomes: $(cat "$w/b.out")"
    fi ;;
  --cold)
    mkdir -p "$w/nodrafts"; build "$w/c" "$w/nodrafts" > "$w/c.out" || { echo "FAIL a build with no drafts"; exit 1; }
    grep -q ' 0 drafted,' "$w/c.out" || { echo "FAIL a build with no drafts still claims drafts: $(cat "$w/c.out")"; fail=1; }
    [ -s "$w/c/drafts.txt" ] && { echo "FAIL drafts.txt is not empty without drafts"; fail=1; }
    sh "$here/tools/tg1rd" "$w/c" > /dev/null || { echo "FAIL the second reader on the cold build"; fail=1; }
    [ $fail = 0 ] && echo "taxgnomes --cold: $(cat "$w/c.out")" ;;
  --offline)
    p="$here/build/hello-taxgnomes.html"; [ -f "$p" ] || { echo "FAIL no page built"; exit 1; }
    if grep -E -q '<(script|link|img|iframe)[^>]+(src|href)="?(https?:)?//' "$p" || grep -E -q '(fetch|XMLHttpRequest|WebSocket|@import)\(' "$p"; then echo "FAIL the page reaches for the network"; fail=1; fi
    [ $fail = 0 ] && echo "taxgnomes --offline: the page loads nothing from outside and asks nothing of the network" ;;
  --egad)
    rs="$here/../egad/jit/resolve.py"; [ -f "$rs" ] || { echo "taxgnomes --egad: NOT CHECKED (no ../egad)"; exit 0; }
    mkdir -p "$w/forest"; cp "$here/egad/read-category.json" "$w/forest/"
    printf '{"viewer":"nora","constraints":{"reduced_motion":false,"screen_reader":false},"prefer":{"read":["north","baseline"]}}\n' > "$w/nora.json"
    printf '{"viewer":"eli","constraints":{"reduced_motion":true,"screen_reader":false},"prefer":{"read":["east","west"]}}\n' > "$w/eli.json"
    python3 "$rs" "$w/forest" "$w/nora.json" | grep -q -- '-> north' || { echo "FAIL a viewer who prefers north did not get north"; fail=1; }
    python3 "$rs" "$w/forest" "$w/eli.json" | grep -q -- '-> west' || { echo "FAIL a reduced-motion viewer who prefers east was not moved to west"; fail=1; }
    [ $fail = 0 ] && echo "taxgnomes --egad: egadjit's resolver gives north to nora, and west (not east) to eli, who asked for reduced motion" ;;
  --prove-red)
    r=0
    build "$w/d" > /dev/null
    plant nosource 'NR == 1 { $3 = "" } { print }'
    plant draftless '!done && $2 == "E" { $3 = "draft:ghost-model"; done = 1 } { print }'
    plant westshouts '!done && $2 == "W" { $4 = $4 "!"; done = 1 } { print }'
    plant swapped '{ k[NR] = $1; d[NR] = $2; s[NR] = $3; t[NR] = $4; if ($2 == "N") n[$1] = $4; if ($2 == "S") so[$1] = $4 }
      END { for (i = 1; i <= NR; i++) { x = t[i]; if (d[i] == "N") x = so[k[i]]; else if (d[i] == "S") x = n[k[i]]; print k[i], d[i], s[i], x } }'
    sed 's/"sources": \[base\[0\]\]}}/"sources": []}}/' "$here/tools/tg1bd.py" > "$w/stray-builder.py"
    cmp -s "$here/tools/tg1bd.py" "$w/stray-builder.py" && { echo "prove-red: the stray builder could not be planted"; r=1; }
    build "$w/sb" "" "$w/stray-builder.py" > /dev/null 2>&1
    [ -f "$w/sb/readings.json" ] || { echo "prove-red: the stray builder did not run, so it proves nothing"; r=1; }
    if honest "$w/sb" > /dev/null; then echo "prove-red: a builder that drops a source was NOT caught"; r=1; else echo "prove-red: a builder that drops a source was caught"; fi
    [ $r = 0 ] && echo "PROVE-RED OK" || echo "PROVE-RED FAILED"; exit $r ;;
  *) echo "usage: taxgnomes-tests.sh [--reader|--prove-red|--cold|--offline|--egad]" >&2; exit 2 ;;
esac
exit $fail
