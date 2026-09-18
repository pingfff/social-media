# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

A text-only knowledge base about hypertrophy training and program design,
built from ~40 video transcripts (fitness YouTube channels: Jeff Nippard,
Andy Baker, Westside/conjugate, J3 University, Meadows, etc.). It serves as
the source of truth for producing social-media content and answering
program-design questions. There is no code, no build system, no tests.

## Layout

- `Program Design/` — raw transcripts, verbatim. Do not edit these.
  - `transcript1.txt` … `transcript23.txt` — batch 1: general program design.
  - `arms/`, `back/`, `chest/`, `legs/`, `shoulders/` — batch 2: muscle-specific
    transcripts, numbered per folder.
- `knowledge/` — distilled, numbered topic files (`01-…` through `13-…`).
  - `08-source-map.md` is the traceability index: transcript → topic mapping
    plus a list of known contradictions between sources. Keep it current.
- `.agents/skills/split-creator/` — the workout-split design skill
  (intake interview → decision-tree pipeline → program output). Programs are
  generated into `programs/`, lifter profiles into `programs/profiles/`.
  Run via `/skill:split-creator` or by asking for a split/program design.

## Citation conventions (critical)

- `[T4]` means `Program Design/transcript4.txt`.
- `[back/7]`, `[arms/2]` etc. mean `Program Design/<bodypart>/<n>.txt`.
- **Every claim in `knowledge/` must carry a transcript citation.** Never add
  uncited claims, and never fabricate transcript content — if a fact isn't in
  a transcript, it doesn't belong in the knowledge base.
- When verifying a claim, grep the cited transcript; transcripts are raw
  auto-generated text (no punctuation/capitalization), so search loosely
  (e.g. short lowercase phrases).

## Handling contradictions

Sources genuinely disagree (failure training, bro splits, volume norms,
eccentrics, deloads…). The current contradictions are catalogued in
`08-source-map.md` § "Known Contradictions". Rules:

- Do **not** silently resolve a contradiction or average the numbers.
- Present both positions with their citations and the context that explains
  the disagreement (e.g. natural vs assisted, novice vs advanced).
- If you find a *new* contradiction, add it to the catalogue.

## Adding new material

Also follow the skill's output spec
(`.agents/skills/split-creator/references/output-spec.md`) for any generated
program: sections, session tables, volume audit, no prescribed weights.

1. Drop the new transcript into the right place in `Program Design/`
   (a bodypart subfolder if muscle-specific, else the next `transcriptN.txt`).
2. Add a row to the appropriate table in `knowledge/08-source-map.md`
   (topic + which knowledge files it feeds).
3. Distill it into the existing numbered knowledge file(s), or create the
   next number in sequence — never renumber existing files.
4. Head each knowledge file's `*Source: …*` line must stay accurate.

## Gotchas

- The directory `Program Design` contains a space — always quote it in shell
  commands (`"Program Design/transcript1.txt"`).
- Filenames in `Program Design/` sort lexically (`transcript10` before
  `transcript2`); use version-sort (`ls -v`) when order matters.
- This is general fitness information for content creation, not medical
  advice; keep any generated content framed accordingly.
