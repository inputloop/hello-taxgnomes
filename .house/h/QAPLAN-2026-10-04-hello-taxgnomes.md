# QA PLAN — hello-taxgnomes

AS-OF 2026-10-04 · written before the build · checks run from the project root.

Each item names the check that settles it. `CHECK:` lines fail as issues; `WARN:` lines as warnings.

## Acceptance

1. The recipe unfolds the same by awk and by Emacs, and the committed files equal it.
   CHECK: sh tests/unfold-check.sh hello-taxgnomes.org "${EMACS:-emacs}"
2. The build is complete and honest: every word with a meaning has four readings; every reading
   cites at least one allowed source; words with no meaning are listed, not invented; a missing
   source is named.
   CHECK: sh tests/taxgnomes-tests.sh
3. The second reader (awk) agrees with the builder's own count and finds every direction's rule
   held: N's mean word length below S's for the table as a whole; N's share of SCOWL words at or
   above S's; W carries no exclamation or question; S has a dense line and an unpacking line; every
   `draft:` source has a draft file behind it.
   CHECK: sh tests/taxgnomes-tests.sh --reader
4. The checks can fail: planted faults (a reading with no source, a north sentence swapped for a
   south one, a draft citation with no draft file, a builder that drops a source) are each caught.
   (Amended in pass 3: the stray is in the builder, and a stray that does not run proves nothing.)
   CHECK: sh tests/taxgnomes-tests.sh --prove-red
5. The build never calls the model and needs no network: a build with the drafts folder hidden
   still completes, and says its E readings are templated.
   CHECK: sh tests/taxgnomes-tests.sh --cold

## The swing-dome (build-loop): a check per rung, or a line declining it

1. TOWER — the slider moves among the five readings by pointer, keys and buttons; the reading and
   its sources change together. Inline tests T-SLIDE, T-KEYS, T-SOURCES (headless, in the cloud
   sandbox: `comic_test.py`-style runner). WARN: (run elsewhere; recorded in the hand-back)
2. LADDER — keyboard reaches every control; the reading is in a live region; reduced motion turns
   transitions off; the four buttons are a path with no picture; colour pairs meet AA. Inline tests
   T-A11Y, T-MOTION, T-CONTRAST.
3. SIGNAGE — the page says, beside each reading, who wrote it (dictionary, pool, template, model),
   and says when E is templated because no drafts were present. Inline test T-SIGN.
4. ROOF — no network requests; nothing leaves; the page loads no outside script or font.
   CHECK: sh tests/taxgnomes-tests.sh --offline
5. PEERING — egadjit: `read-category.json` resolves with egad's own `jit/resolve.py` for a viewer
   who prefers north, and for one who refuses east. Runs where egad is checked out beside this
   project; elsewhere NOT CHECKED.
   WARN: sh tests/taxgnomes-tests.sh --egad
6. REMOTES — declined: no remote service or peer is involved in this example.
7. DOME — not-happy paths: a word with no meaning shows a plain "no meaning found" and its sources;
   a broken data file shows a message, not a blank page. Inline test T-EMPTY.

Manifest: none owed (no problem class has recurred here).

## Where checks run

The device shell (Avalon's VM) runs 1–5 and the egad check; the inline browser tests run in the
cloud sandbox (Playwright, headless). A check too slow for one call is split and says so.
