# Knowledge Library

Everything needed to write accurate, current scripts.

## Layout: raw vs clean

```
knowledge/
  raw/          write-once archive. Agents NEVER read these files.
    transcripts/  news/  reddit/
  clean/        the ONLY reading surface for writing scripts.
    topics/       per-topic synthesis — READ THIS FIRST for a topic
    transcripts/  per-video distillations (claims + craft)
    news/  reddit/  research/
  SOURCES.md    which sites can be fetched directly
  WISHLIST.md   what to fetch next, per series
```

- `raw/` holds verbatim sources: full transcripts (auto-saved by
  `scripts/youtube_transcript.py --save`), full pasted articles, pasted
  Reddit threads. Reading raw/ is blocked by opencode permissions and
  forbidden by convention — the raw layer exists only as provenance.
- `clean/` holds distilled, standardized files (schema below). All
  script-writing pulls from clean/, never raw/.

## Pipeline (raw -> clean happens ONCE, at fetch time)

1. Fetch: transcript via script (or paste Reddit/blocked content into
   `raw/<type>/`, one file per source, with the header below).
2. Distill immediately, in the same task, from the in-session content
   (no need to re-read raw): write the clean companion file.
3. From then on, only the clean file is read or updated.

Raw header convention (auto-applied by the transcript script — includes
performance metrics so raw archives are self-contained):

```
source: <URL>
fetched: <date>
why: <which series/episode this feeds>
channel: <channel>
title: <title>
views: <number>
likes: <number>
duration: <ISO8601>
```

## Clean file schema

Markdown with YAML frontmatter; body sections fixed per type:

```markdown
---
type: transcript | news | reddit | research
source: <URL>                # omit for research (maintained summaries)
fetched: <YYYY-MM-DD>
channel: <channel>           # transcripts only
topics: [fat-loss, cutting]
series: [cutting-101]
raw: raw/transcripts/<folder>/transcript.txt   # pointer, never opened
---

# <Title>

## Key claims          (the evidence: claim + concrete numbers)
## Mechanisms          (physiology, analogies)       [when relevant]
## Craft notes          (see below — required for transcripts)
## Script angles       (episode ideas in the creator's voice)
```

### Craft notes (transcripts)

Studied creators are absorbed for HOW they hold an audience, not just
what they claim. Capture:

- **Hook (verbatim)**: the first 2-3 lines, quoted exactly, + one line
  on why it works (self-selection? stakes? curiosity?).
- **Retention devices**: open loops / teases ("the third one is the
  most neglected..."), signposts ("give me one minute to explain X"),
  "but" pivots, foreshadowing, placement of the curiosity gap.
- **Rhetorical devices**: concession patterns ("yes X works short-term,
  but..."), anaphora/repetition, second-person walkthroughs with
  concrete numbers, problem-agitation before the fix, normalizing
  failures (graph spikes = "blips").
- **Phrase bank**: 5-10 short verbatim lines worth adapting to the
  creator's voice (simplifiers, reframes, transitions).
- **Sponsor/CTA placement**: where the ad read sits and how the close
  works.

- `research/` files are maintained evidence summaries (no single
  source): use `maintained: true`, skip `source:` and `raw:`.
- Flag disagreements between sources inline (e.g. reverse-dieting
  takes) — dueling evidence is episode material.

### Topic synthesis files (`clean/topics/`)

One file per topic (e.g. `fat-loss.md`, `peak-week.md`), maintained by
the `@youtube-research` agent across runs. This is the entry point for
series creation — see the format in `.opencode/agents/youtube-research.md`
Phase 5: winning formats, hook patterns, saturated angles, library
pointers, series mapping.

## Reading path for series creation

When creating or extending a series:
1. `brand/voice.md` — canonical voice, always
2. `clean/topics/<topic>.md` — what works on the topic (if missing or
   thin, run `@youtube-research` first)
3. Per-video transcript files the topic file points to — claims +
   craft (hooks, phrasing)
4. `clean/research/` — the evidence base for mechanisms/numbers

## Division of labor

- I CAN fetch directly: Stronger By Science, BarBend, most article/news
  sites (see `SOURCES.md`), YouTube transcripts (via
  `scripts/youtube_transcript.py <url> --save --why ...`)
- I CANNOT fetch: Reddit (blocked), Instagram — paste into `raw/`.
