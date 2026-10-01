# Bodybuilding Prep Knowledge

Knowledge files for contest-prep and bodybuilding-specific content
(cutting, peak week, posing, show-day, offseason/Improvement season, etc.).

## Conventions

- Same citation rules as the parent `knowledge/` directory: every claim
  carries a transcript citation; never fabricate transcript content.
- New transcripts about bodybuilding prep go into a subfolder under
  `Program Design/` and get a row in `knowledge/08-source-map.md`.
  Peak-week material lives in `Program Design/Peak Week/` and is cited as
  `[PW#]` (transcripts) and `[W#]` (website link files).
- Files here are numbered in their own sequence starting at `01-`, independent
  of the parent directory's numbering.
- The parent `08-source-map.md` contradictions catalogue still applies —
  prep advice varies hugely by coach (deficit size, cardio, peak week), so
  present conflicting positions with citations and context, never averaged.

## Schema

All knowledge files here (01–06) follow a common in-file section order:

1. `## Principles` — conceptual guidance, no standalone numbers.
2. `## Protocols & Numbers` — timeline tables and quantitative protocols,
   each row carrying its citations.
3. `## Quotes` — verbatim source quotes with citations.
4. `## Contradictions & Context` — disagreements between sources plus the
   context that explains them.
5. `## Gaps` — what the transcripts do not cover.

Downstream consumers (scripts, graphics generators such as reel overlays)
must draw quantitative claims from the **Protocols & Numbers** tables, not
from prose elsewhere in the file — the tables are the canonical, cited home
for timings, dosages, and sequences.

## Files

All files follow the Schema above (Principles / Protocols & Numbers / Quotes /
Contradictions & Context / Gaps).

- `README.md` — this file.
- `01-peak-week-principles.md` — what peak week can/can't do, stage-leanness
  prerequisite, fatigue/cortisol model, natural vs enhanced, strategy
  selection, division differences, the MASS questionnaire study.
- `02-water-and-electrolytes.md` — fluid compartments, RAAS/Army-study data,
  water and sodium protocols by school (tables), potassium rules, show-day
  sodium use, health warnings.
- `03-carbohydrate-strategies.md` — the master strategy table (conventional,
  front, mid, back, back+clean-up, rapid back load, linear — with complete
  day-by-day amounts), J3U meal-tuning, protein & fat handling, food
  choices, spillover, supplements.
- `04-training-cardio-recovery.md` — training taper, cardio-to-steps, making
  weight, sleep, travel, monitoring/coaching logistics, posing practice.
- `05-show-day.md` — show-day principles and hour-by-hour timeline tables,
  pump-up, warmth, coach-eye heuristics, post-show rebound, mistakes checklist.
- `06-diuretics-and-health-risks.md` — diuretic consensus and pharmacology,
  case-study tables, electrolyte dangers, risk framing.
