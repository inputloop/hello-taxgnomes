# DESIGN — 4 October 2026 — hello-taxgnomes, the Gnemonic Word Mines

DRAFT · unsigned · [ours — revisable] · a worked example for this turn's LENS; built under build-loop.

## 1. What the source asked for, in his words

(Spelling corrected as an accommodation; the verbatim message is in the session log.)

> As a worked example of a design component to have in this turn's LENS for mutual honing [...]
> we could implement a taxonomy driven plugin that uses a dictionary and worked taxonomy set
> implemented at build/compile time for some component targeting egad and working in and transiting
> egadjit (or just working in terms of the former, as may be the case), or another design framework
> if we can find that it is compatible, so that these mutual hooks are suggestions and not
> specifically "only" enforced ways to use what this composable design element/component and
> skill-shaped recipe forms provide to users: the ultimate behavior in the fully worked example
> (hello-taxgnomes: yes: G here, yes "Gnomes", as in "The Gnemonic Word Mines") we can offer a four
> direction slider over sophistication of language (N: simpler, toward grade-school normative or
> equivalent; S: denser, shorter sentences with more dense words, with longer sentences unpacking
> them to minimally give reference to the meaning in context), and tone/mood (E: more moody, greater
> intention/variety of intonation, wobblier; W: subtle toward direct/pedantic or dry); this can
> default to a GRAIN of backing sentences and this -1 (so 3) backing dictionary-shaped sources to
> incorporate, doing the building using forms of/based on the sample game and improving them -or
> dialing them back- per task as capacities actually allow, harnessing local agents such as our
> llama bridge where we can bring them to bear.

## 2. The design

**One literate file** (`hello-taxgnomes.org`) unfolds into the builder, the page, its egad hooks and
the checks, the same way kid-glove, drift and gw-survey do.

**Inputs, at build time only.** The word game's material (`mini-c4-game`): its four taxonomy tables
(272 words: GROWTH, OPTIMIZER, RECEIPT, TAG), their meanings and pooled sentences. Three
dictionary-shaped sources (GRAIN − 1):

1. WordNet 3.1 (glosses; `cntlist` sense frequencies),
2. GCIDE 0.53 (the 1913 Webster definitions; its `Syn.` lists),
3. SCOWL, as shipped in hunspell's `en_US.dic` (is a word common?).

Nothing is fetched at build time; the build reads caches already on disk, and a missing source is
named, never silently skipped.

**Four backing sentences per word (GRAIN).** One for each direction:

| direction | what it reads like | built from |
|---|---|---|
| N simpler | a grade-school sentence: short, common words | the gloss whose words are most often in SCOWL, plus the shortest example in the pool |
| S denser | one dense line, then a longer line unpacking it | GCIDE's definition (dense), then the WordNet gloss and where the word sits in its table |
| E moodier | more voice and intonation | a pooled sentence with voice (a question, a person speaking), else a drafted one (the local model), else a template |
| W drier | direct, pedantic, plain | `WORD (part of speech): gloss.` and GCIDE's synonyms |

The centre of the slider shows the plain gloss (the baseline, which can never be refused, as in
egadjit). Every sentence carries its sources (`wordnet-3.1:OFFSET`, `gcide-0.53`, `scowl`,
`pool:…`, `draft:MODEL`, `template:E2`), so a reader can see who wrote it: a dictionary, a person,
a template, or the model.

**The local model is optional.** Drafts for the E direction come from the llama bridge in the
background (`delegate_async`), are kept as JSON with the model's name and date, and are taken in by
the build when present. The build never calls the model; a build with no drafts gives a complete
page with templated E sentences, said as such.

**The page** is one HTML file, offline, with no network requests: the tables as a list of words; a
slider pad (pointer, arrow keys, and four labelled buttons as a path that needs no picture); the
reading in a live region so a screen reader hears each change; reduced motion honoured; colours from
egad's tokens when present, with fallbacks that meet AA.

**egad and egadjit hooks, as suggestions.**
- `egad/read-category.json`: an egadjit category `read` with treatments `baseline`, `north`,
  `south`, `east`, `west`. A viewer's preference (`prefer.read`) can choose where the knob starts;
  `resolve.py` can pick it for a forest of viewers. Without egad the page starts at the centre.
- `egad/greeting.org`: the smallest Org declaration of the component (property drawers egad's
  declarative layer reads).
- The page reads `--egad-*` custom properties if a host page defines them; otherwise its own.
Nothing in the page requires egad; nothing in egad has to change for the page to work.

**Two readers.** The builder (Python) writes `data/readings.json` and a flat `data/readings.txt`
(one sentence per line, with its word, direction and sources). A second reader in awk checks the
flat file against each direction's rule (below), independently of the builder. The page carries
inline tests for the slider, run headless.

## 3. What would show this design wrong

- A direction rule that cannot be checked mechanically (then it is a preference, and the page
  should say so beside that direction).
- North readings that are not simpler than south readings by the measures we chose (mean word
  length, share of SCOWL words).
- An E sentence that claims the model wrote it with no draft file behind it.
