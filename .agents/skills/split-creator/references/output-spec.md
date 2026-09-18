# Program Output Specification

Every generated program is a single Markdown file at
`programs/<name>-<YYYY-MM-DD>.md` with exactly these sections:

## 1. Header

- Lifter (link to profile), goal, split name, days/week, session-length target
- One-paragraph summary of the design logic

## 2. Weekly schedule

Table: day → session (or rest), with rest-day rationale when non-obvious
(cite `knowledge/06`).

## 3. Session tables (one per training day)

| # | Exercise | Sets × Reps | RIR | Rest | Notes |
|---|----------|-------------|-----|------|-------|

- Exercises in execution order (compounds first; priority muscle first when
  specializing — cite `knowledge/05`)
- **No weights, percentages, or load suggestions anywhere** — loads are the
  lifter's choice; progression is defined in reps/sets/RIR terms only
- **Rest column is always "2 min"** (standardized rest); superset partners
  share one 2-min rest — mark supersets explicitly in the Exercise column
- Notes column: technique cues, stretch emphasis, substitution hints

## 4. Weekly volume audit

The `volume-audit.py` output table, **pasted verbatim** (muscle → weekly
sets → per session → landmark → verdict), with a link to the saved audit
JSON in `programs/audits/`. Any muscle deliberately at maintenance or
specialization volume, and every script warning, is justified in bullets
*below* the table — never by editing the table itself.

Followed by the `session-length.py` output table (pasted verbatim): session
→ hard sets → superset pairs → estimated length vs the Q6 budget. Every
over-budget warning must be resolved before shipping.

## 5. Block structure & progression

- Block length (overload weeks + deload week) and the chosen progression
  method (cite `knowledge/04`), written as concrete week-by-week rules, e.g.:
  "Weeks 1–4: add 1–2 reps per set weekly at the same RIR; when you hit the
  top of the rep range on all sets, add a set (cap: 5/exercise); Week 5:
  deload (halve sets, keep RIR-0-free)"
- Starting-effort calibration note for week 1 (e.g., begin at RIR 3–4 to
  leave progression room)

## 6. Deload plan

Type (volume / intensity / frequency-spread — cite `knowledge/06`), timing,
and what changes concretely.

## 7. Autoregulation & adjustment triggers

When to hold/dial back (performance down, soreness lingering, sleep crash —
cite `knowledge/06`), and the logbook rule (cite `knowledge/04`).

## 8. Design rationale & contradictions

- Which `07` decision-tree branch selected this split
- Volume allocation reasoning (cites)
- Every known contradiction (per `knowledge/08`) touched by this design:
  state the position taken and the lifter-context that justified it

## 9. Assumptions

Every intake default that was used, verbatim from the intake's defaults table.
