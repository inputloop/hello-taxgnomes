# RESTART · 2026-10-04 · hello-taxgnomes east drafts (parked for an Avalon restart)

Paste into a new Cowork task linked to avalon, with F:\claude\AS4CE\AS4CE0001 and
F:\claude\projects connected:

> Read and follow F:\claude\projects\hello-taxgnomes\.house\h\RESTART-2026-10-04-east-drafts.md

His words, when he parked it (spelling as he corrected it): "We have clearly demonstrated a clear
need to think in terms of restartability: while there are bigger triggers there are also smaller
ones." And: "it's worth it: this is why we use local tools. no problem to wait, big bummer to go
part way when we have already isolated the expensive part to my own compute, my own local agent."
So: finish all 192, however long it takes; never stop part way to save time.

## Where it stands (observed 2026-10-04 ~22:00Z)

- 12 of 192 east readings are drafted by gemma4:12b and built in (`drafts/2026-10-04-gemma4-12b-E.json`;
  build: 12 drafted, 69 pooled, 180 templated). All checks green; committed locally, not pushed.
- The 180 left are prompt files `drafts-2026-10-04/r2/b01.prompt` .. `b15.prompt` (12 words each).
  Every job, its id and how it ended: `drafts-2026-10-04/jobs.tsv`.
- build-loop: `SWING` here says cycle 2, pass 1 done (0 issues, 1 warning: the 180).
  Ask it: `sh <AS4CE0001>/skills/build-loop/scripts/sw1ng next` from this folder.
- Why it is slow (observed): Llama Bridge gives each generate call 600 s; jobs sent together queue
  on one GPU and the queued ones time out; 12 words took about 9 minutes (b00) or over 10 (b01).
  Ollama reports gemma4:12b has the "thinking" capability and was loaded with a 262,144-token
  context; the bridge sends no `think` option. GPU memory was never released before the restart.

## Two guesses, each with its test (run before the batches; each is one small call)

- H1, thinking is on by default and costs hidden tokens. Test: the same 3-word prompt with and
  without `"think": false`, timed by Ollama's own `eval_count` and `eval_duration`. Falsified if
  the two runs differ by less than a quarter in eval_count.
- H2, the 262,144 context spills past the GPU. Test: the same prompt with `"options":
  {"num_ctx": 8192}`. Falsified if its tokens/second is within a quarter of the default's.
- How to probe without a stuck call: in the built-in browser at http://127.0.0.1:11434/api/tags,
  start the fetch and store it (`window.P = fetch(...).then(r=>r.json())`), return at once, and
  read `await window.P` in a later call (the browser tool gives up at 45 s). Only on his own Ollama.
- If H1 or H2 holds: the bridge is Bryant's file, kept byte for byte, so write the finding as an
  offer-back note (AS4CE0001/advice/, an ENHANCE for llama_bridge: pass `think` and `num_ctx`), and
  keep using the bridge for the drafts; batch size can then grow to what fits well inside 600 s.

## The queue, one job at a time

For each of b01 .. b15, in order:
1. Say in chat what goes, to which model, and about how long (altorewired, grown 03).
2. `delegate_async` (model gemma4:12b, require_json, no_cache) with the prompt file's text.
3. Append its id to `jobs.tsv` at once.
4. Poll with a line to him between polls; while waiting, do other useful work.
5. Save the answer to `drafts-2026-10-04/answers/bNN.json` and run
   `python3 tools/tg1dr.py ingest gemma4:12b drafts-2026-10-04/answers/bNN.json 2026-10-04`
   (from the project root; path relative to it is `.house/h/drafts-2026-10-04/...`).
   Mark the job done, with how many were kept, in `jobs.tsv`.
6. A job that fails on the 600 s cap: split that batch in two (6 words) and send each; never skip it.

## When all 192 are in

`make build page`, then `make check` (both unfolders, all six checks, prove-red), then the
page's 9 inline tests (headless; owed since the data changed), then `sw1ng qa --issues N --warnings W`,
then `sw1ng complete` on a clean pass or the final swing. Commit locally (no push: he holds pushes).
Write the ChangeLog entry and a hand-back in AS4CE0001/Inbox. If a transcript of the session is at
hand, run `sh <AS4CE0001>/skills/altorewired/scripts/sl1gk TRANSCRIPT.jsonl` and say what it counts.
