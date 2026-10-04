#!/bin/sh
# unfold-check.sh -- two readers unfold a literate recipe: unfold.awk and Emacs's org-babel-tangle.
# They must write the same bytes, and the committed files must equal them.  No Emacs: that half
# says NOT CHECKED (never a silent pass).  --prove-red: a hand edit to an unfolded file is caught.
# usage: sh tests/unfold-check.sh RECIPE.org [EMACS] [--prove-red]
# The same file serves every recipe-style project (kid-glove, drift); keep the copies equal.
# Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
# Mentat (for Corwin; claude-opus-5-5)
set -u
here=$(cd "$(dirname "$0")/.." && pwd)
recipe=${1:?usage: unfold-check.sh RECIPE.org [EMACS] [--prove-red]}; EMACS=${2:-${EMACS:-emacs}}
red=0; for a; do [ "$a" = --prove-red ] && red=1; done
[ "$EMACS" = --prove-red ] && EMACS=emacs
w=$(mktemp -d) || exit 2; trap 'rm -rf "$w"' EXIT
files=$(awk '/^[ \t]*#\+(begin_src|BEGIN_SRC)[ \t]/ { n = split($0, x, /[ \t]+/); for (i = 1; i < n; i++) if (x[i] == ":tangle" && x[i+1] != "no") print x[i+1] }' "$here/$recipe" | sort -u)
check() { # TREE -> 0 when its unfolded files equal the recipe's (by both readers, where present)
  tree=$1; bad=0
  mkdir -p "$w/a" "$w/e"; cp "$tree/$recipe" "$w/a/"; cp "$tree/$recipe" "$w/e/"
  (cd "$w/a" && awk -f "$here/unfold.awk" "$recipe" >/dev/null)
  for f in $files; do cmp -s "$w/a/$f" "$tree/$f" || { echo "DIFFERS from the recipe: $f (hand-edited? run make unfold)"; bad=1; }; done
  if command -v "$EMACS" >/dev/null 2>&1 || [ -x "$EMACS" ]; then
    (cd "$w/e" && "$EMACS" -Q --batch --eval "(progn (require 'org) (require 'ob-tangle) (setq org-src-preserve-indentation t) (org-babel-tangle-file \"$recipe\"))" >/dev/null 2>&1)
    for f in $files; do cmp -s "$w/a/$f" "$w/e/$f" || { echo "READERS DISAGREE: $f (unfold.awk vs org-babel-tangle)"; bad=1; }; done
    [ $bad = 0 ] && echo "unfold: $(echo $files | wc -w) files equal the recipe; unfold.awk and Emacs agree"
  else
    [ $bad = 0 ] && echo "unfold: $(echo $files | wc -w) files equal the recipe (awk); the Emacs half NOT CHECKED (no $EMACS)"
  fi
  rm -rf "$w/a" "$w/e"; return $bad
}
if [ $red = 1 ]; then
  mkdir -p "$w/tree"; (cd "$here" && tar cf - --exclude=.git . ) | (cd "$w/tree" && tar xf -)
  f1=$(echo $files | cut -d' ' -f1); printf '\nhand edit\n' >> "$w/tree/$f1"
  if check "$w/tree" >/dev/null; then echo "unfold-check --prove-red: a hand edit was NOT caught"; exit 1; fi
  echo "unfold-check --prove-red: a hand edit was caught"; exit 0
fi
check "$here"
