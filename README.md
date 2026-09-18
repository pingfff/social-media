# social-media

Knowledge base for hypertrophy training and program-design content, distilled
from ~40 video transcripts (Nippard, Andy Baker, Westside Barbell, J3
University, John Meadows, and others). Used as the factual source of truth for
social-media content and program-design Q&A.

## Structure

| Path | Contents |
|---|---|
| `Program Design/` | Raw transcripts — batch 1 (`transcript1–23.txt`, general programming), batch 2 (bodypart folders: `arms/`, `back/`, `chest/`, `legs/`, `shoulders/`) |
| `knowledge/` | Distilled topic notes, numbered `01`–`13` (principles, variables, splits, periodization, exercise selection, recovery, decision tree, muscle-specific files) |
| `knowledge/08-source-map.md` | Traceability index: each transcript's topic, what it feeds, and the catalogue of known contradictions between sources |
| `.agents/skills/split-creator/` | "Workout split creator" skill: intake questionnaire → design pipeline → program output spec |
| `programs/` | Generated programs (`<name>-<date>.md`) and lifter profiles (`profiles/`) |

## Conventions

- Claims in `knowledge/` cite their sources: `[T4]` → `Program Design/transcript4.txt`;
  `[back/7]` → `Program Design/back/7.txt`.
- Where sources conflict, both positions are kept with citations — see
  "Known Contradictions" in the source map.
- Transcripts are immutable; corrections and distillations happen in `knowledge/`.

## Working with agents

Agent instructions live in [`AGENTS.md`](AGENTS.md). See it for citation rules,
how to add new transcripts, and repo gotchas.
