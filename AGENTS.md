# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

A text-only knowledge base about hypertrophy training and program design,
built from ~40 video transcripts (fitness YouTube channels: Jeff Nippard,
Andy Baker, Westside/conjugate, J3 University, Meadows, etc.). It serves as
the source of truth for producing social-media content and answering
program-design questions. There is no code, no build system, no tests.

## Layout

- `raw/` — raw transcripts, verbatim. Do not edit these.
  - `transcript1.txt` … `transcript23.txt` — batch 1: general program design.
  - `arms/`, `back/`, `chest/`, `legs/`, `shoulders/` — batch 2: muscle-specific
    transcripts, numbered per folder.
  - `Peak Week/` — batch 3: peak-week / contest-prep-peak transcripts
    (`transcriptN.txt`, cited as `[PW#]`) plus `websiteN.txt` link files
    (cited as `[W#]`). Distilled into `knowledge/bodybuilding/01-06`.
- `knowledge/` — distilled, numbered topic files.
  - `training/` — `01-…` through `13-…`: programming and muscle-specific
    topics (principles, variables, program styles, progression, exercise
    selection, recovery, decision tree, then back/chest/legs/shoulders/arms).
  - `bodybuilding/` — bodybuilding-prep topics, own `01-…` numbering, all
    following the five-section schema (Principles / Protocols & Numbers /
    Quotes / Contradictions & Context / Gaps — see its README). Quantitative
    claims live in the Protocols & Numbers tables; downstream content
    (scripts, graphics) must take numbers from those tables, not prose.
  - `08-source-map.md` is the traceability index: transcript → topic mapping
    plus a list of known contradictions between sources. Keep it current.
- `content/` — social-media content built from the knowledge base.
  - `instagram-peak-week-series.md` — the 17-episode series plan.
  - `peak-week-scripts/` — one script per episode (hook, timestamped beats,
    captions with coaching CTA).
  - `peak-week-graphics/` — the graphics system: `html/` holds the design
    system + per-episode specs + `render.py` (the source of truth — re-render
    with `cd html && python3 render.py spec_epN`); `episode N/` folders hold
    rendered 1080x1920 PNGs, which are **git-ignored build artifacts**.
- `programs/` — generated workout programs (`programs/audits/`,
`programs/profiles/`) from the split-creator skill.
- `business/` — coaching business deliverables (PDF guides, flagship program
  manuscripts + build scripts).
- `pingliftsfitness-site/` — website assets.
- `.agents/skills/` — repo skills:
  - `split-creator/` — workout-split design (intake → decision tree →
    program into `programs/`).
  - `reel-graphics/` — vertical Instagram graphics via the HTML/Chromium
    pipeline in `content/peak-week-graphics/html/`.
  - `media-intake/` — find/download/transcribe new source videos into
    `raw/` (popularity-ranked deep search, caption fetch,
    local-whisper fallback, human curation gate).
- `.config/` — git-ignored local config (YouTube API key, static ffmpeg).

## Citation conventions (critical)

- `[T4]` means `raw/transcript4.txt`.
- `[back/7]`, `[arms/2]` etc. mean `raw/<bodypart>/<n>.txt`.
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

1. Drop the new transcript into the right place in `raw/`
   (a bodypart subfolder if muscle-specific, else the next `transcriptN.txt`).
2. Add a row to the appropriate table in `knowledge/08-source-map.md`
   (topic + which knowledge files it feeds).
3. Distill it into the existing numbered knowledge file(s), or create the
   next number in sequence — never renumber existing files.
4. Head each knowledge file's `*Source: …*` line must stay accurate.

## Gotchas

- Filenames in `raw/` sort lexically (`transcript10` before
  `transcript2`); use version-sort (`ls -v`) when order matters.
- This is general fitness information for content creation, not medical
  advice; keep any generated content framed accordingly.
