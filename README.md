# social-media

Knowledge base for hypertrophy training and program-design content, distilled
from ~60 video transcripts (Nippard, Andy Baker, Westside Barbell, J3
University, John Meadows, Klemczewski, and others). Used as the factual source
of truth for social-media content, coaching programs, and program-design Q&A.

## Structure

| Path | Contents |
|---|---|
| `raw/` | Raw transcripts — batch 1 (`transcript1–23.txt`, general programming), batch 2 (bodypart folders: `arms/`, `back/`, `chest/`, `legs/`, `shoulders/`), batch 3 (`Peak Week/`, cited `[PW#]`/`[W#]`) |
| `knowledge/` | Distilled topic notes: `training/` (programming + muscle-specific, `01–13`), `bodybuilding/` (contest-prep/peak-week, five-section schema — see its README) |
| `knowledge/08-source-map.md` | Traceability index: each transcript's topic, what it feeds, and the catalogue of known contradictions between sources |
| `content/` | Instagram content built from the knowledge base: series plan, episode scripts, and the graphics system (`peak-week-graphics/html/` is the source of truth; rendered PNGs are git-ignored build artifacts) |
| `programs/` | Generated workout programs (`<name>-<date>.md`), audits, and lifter profiles |
| `business/` | Coaching business deliverables (PDF guides, flagship program) |
| `pingliftsfitness-site/` | Website assets |
| `.agents/skills/` | Repo skills: `split-creator` (program design), `reel-graphics` (vertical Instagram graphics), `media-intake` (find + transcribe new sources) |

## Conventions

- Claims in `knowledge/` cite their sources: `[T4]` → `raw/transcript4.txt`;
  `[back/7]` → `raw/back/7.txt`; `[PW3]` → `raw/Peak Week/transcript3.txt`.
- Quantitative claims live in the `Protocols & Numbers` tables of
  `knowledge/bodybuilding/`; downstream content (scripts, graphics) takes
  numbers from those tables, not prose.
- Where sources conflict, both positions are kept with citations — see
  "Known Contradictions" in the source map.
- Transcripts are immutable; corrections and distillations happen in `knowledge/`.

## Working with agents

Agent instructions live in [`AGENTS.md`](AGENTS.md). See it for citation rules,
how to add new transcripts, and repo gotchas.
