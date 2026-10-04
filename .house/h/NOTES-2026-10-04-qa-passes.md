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
