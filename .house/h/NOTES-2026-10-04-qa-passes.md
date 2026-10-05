# NOTES — 4 October 2026 — hello-taxgnomes, the QA passes

## Pass 1 (issues 5, warnings 1)
1. North picked GCIDE's definition whenever its words were shorter on average, so it read "An accent
   is A superior force of voice ... or a."  North should prefer the short WordNet gloss, lower-case
   it after the article, and never cut mid-clause.
2. Long definitions were cut at a word count, leaving dangling "or a."; cut at a clause or comma.
3. Pooled GCIDE sentences carry markup ("<br/") and glued quotes ("Dover?gate"); clean or skip.
4. South's dense line ended in ".." when the clause already ended in a period.
5. South's dense line could be one word ("Order."); fall back to WordNet when GCIDE's clause is short.
Warning: 192 of 261 east readings are templated; the local model's drafts are still running.

## Pass 2 (issues 2, warnings 1)
1. South repeated itself when its dense line was already the WordNet gloss ("ARRAY: an orderly
   arrangement. Unpacked: an orderly arrangement; ..."); the unpacking now says only where the word
   sits, when the gloss is already in the dense line.
2. GCIDE's editorial brackets ("[They] put a chain") showed in examples; taken out.
Warning: still 192 templated east readings (the model's drafts are pending).

## Pass 3 (issues 1, warnings 1): a check found wrong, and fixed
The whole plan ran: unfold (awk and Emacs agree), build honest, second reader agrees under awk,
mawk and gawk, cold build, offline, egad's resolver, the page's 9 inline tests (headless, in the
cloud).  One issue, in a check, not the work: prove-red's stray builder could not find the word game
from its scratch folder, crashed, and so was "caught" for the wrong reason.  The tests now point
every build at the game explicitly and refuse a stray that did not run.  (Build-loop rule 8: the
plan says the check was fixed, not the work.)
Warning: still 192 templated east readings.

## Cycle 2, pass 1 (issues 0, warnings 1) -- after the crash, 2026-10-04 evening
The crashed session's four background drafts never landed and their job ids were lost.  Re-sent
from a new session: four 48-word batches at once all hit Llama Bridge's 600 s per call (they
queued on one GPU); then 12-word batches one at a time: b00 landed (12 of 12 kept, about 9 min),
b01 hit 600 s.  Whole plan ran: build honest, second reader agrees, cold, offline, egad, prove-red.
Not run this pass: the page's 9 inline tests (only the data changed; owed at the next pass).
Warning: 180 east readings still templated.  Parked for an Avalon restart: RESTART-2026-10-04-east-drafts.md.

## Cycle 2, pass 2 (issues 0, warnings 1) -- after the Avalon restart, 2026-10-05 ~00:58Z
All 192 east readings drafted by gemma4:12b through the bridge (`gemma4:12b-8k`, the same weights with
an 8k context; why: PROBE-2026-10-04-ollama-speed.md).  Whole plan ran: unfold (awk on Avalon; the
Emacs half in the cloud sandbox, Emacs 29.3, on a staged copy, since Avalon's shell has no Emacs),
build honest (192 drafted, 0 templated), second reader agrees, cold, offline, egad, prove-red, and the
page's 9 inline tests (headless).
Warning: 14 drafts slipped past every check: 11 wrote the headword in capitals (b11b, b14a), LITHIUM
recited its gloss, MUTED carried a stray quotation mark, COMMAND was drafted as the verb.

## Cycle 2, pass 3 (issues 0, warnings 0) -- 2026-10-05 ~01:15Z
Fix, in the recipe: `tg1dr.py retire MODEL DATE WORD REASON` keeps a bad draft on record with its
reason; the builder passes over a retired draft; tg1ck refuses a build that shows one; prove-red
plants a retirement and a builder deaf to it (caught; the real builder is not).  Taking in an answer
now notes a headword written in capitals.  The 14 were retired and redrafted (r3/c1..c3, the r2 prompt
plus one line on case; the first wording overcorrected to all-lower-case and was not taken in).
Whole plan ran clean: unfold (awk and Emacs agree, 9 files; prove-red), build honest, second reader
agrees, cold, offline, egad, prove-red (six plants), and 9 of 9 inline tests.
