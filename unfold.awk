# unfold.awk -- unfold (tangle) an Org recipe: each src block with ":tangle PATH" is written to
# PATH, relative to the current directory.  Several blocks for one PATH are joined in order.
# Lines escaped with a leading comma (",*" ",#+") lose the comma, as Org's own tangle does.
# The second reader is Emacs: org-babel-tangle must write the same bytes (make check-unfold).
#
# usage: awk -f unfold.awk RECIPE.org      prints each path written
#
# Copyright 2026 Corwin Brust <corwin@bru.st> and Contributors; GPL-3.0-or-later.
# Mentat (for Corwin; claude-opus-5-5)
function dirof(p,   d) { d = p; if (sub(/\/[^\/]*$/, "", d)) return d; return "" }
/^[ \t]*#\+(begin_src|BEGIN_SRC)[ \t]/ {
  path = ""
  n = split($0, w, /[ \t]+/)
  for (i = 1; i < n; i++) if (w[i] == ":tangle") path = w[i + 1]
  if (path != "" && path != "no") {
    inblk = 1; out = path
    if (!(out in opened)) {
      opened[out] = 1; d = dirof(out)
      if (d != "") system("mkdir -p '" d "'")
      printf "" > out; print out
    }
    next
  }
}
inblk && /^[ \t]*#\+(end_src|END_SRC)[ \t]*$/ { inblk = 0; next }
inblk { line = $0; if (line ~ /^[ \t]*,(\*|#\+)/) sub(/,/, "", line); print line > out; next }
