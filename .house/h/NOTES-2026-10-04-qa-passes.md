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
