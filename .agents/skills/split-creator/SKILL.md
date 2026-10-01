---
name: split-creator
description: Designs detailed workout splits and training programs — full weekly schedules with exercises, sets/reps, RIR targets, rest periods, progression structures, and deloads — from an intake interview. Uses the knowledge base in knowledge/ as the source of truth. Use when the user asks to create, design, or redesign a workout program, split, or training plan.
---

# Workout Split Creator

Workflow: **intake → validate → design → output → iterate**. All training
recommendations must come from the `knowledge/` files, with citations in the
final program document.

## Step 1 — Intake

1. Check `programs/profiles/` for an existing profile of this person. If found,
   confirm it's still accurate (schedule, injuries, priorities change) and
   proceed to Step 2.
2. No profile (or stale)? **Run the interactive intake immediately — do not
   wait for the user to ask.** Interview them in-session with AskUserQuestion
   using the questionnaire in [assets/intake.md](assets/intake.md):
   - Ask the ★ hard-required questions first (Q1, Q3, Q5, Q6, Q15, Q16) in
     one or two batches, then Q2/Q4/Q7/Q12, then Q8–Q11, then Q13–Q22.
     Never dump all questions at once.
   - AskUserQuestion limits you to 4 questions per call with up to 4 options
     each — for questions with more options (Q1, Q5, Q6, Q15) fold the
     extras into the "Other" free-text choice, which the user can fill with
     the option letter or free text.
   - "Not sure" is always acceptable — answer `ns` on their behalf (the
     script records it as a defaulted value).
3. Then write the profile **through the intake script's batch mode** so
   validation and marking are identical to the terminal form:

   ```bash
   bash .agents/skills/split-creator/scripts/intake.sh --batch \
     name=<name> q1=<letter|ns|!text> q2=<text> ... q22=<text>
   ```

   Omit questions the user skipped entirely — the script applies their
   defaults and prints each one; carry those into the Assumptions section.
   If the script rejects an answer, re-ask that question and re-run. The
   script writes the self-contained profile to `programs/profiles/<name>.md`.
4. Alternative (offer only if the user prefers typing in a real terminal):
   they run `bash .agents/skills/split-creator/scripts/intake.sh`
   themselves — same validation, same markers.
5. Profiles mark deviations as `[ns: defaulted]` / `[free text]` — carry
   every marker into the program's Assumptions section. Reuse the saved
   profile for future designs and iterations.

## Step 2 — Validation

Hard-required before designing — ask if missing:

- Training age (structured training years)
- Days per week + max session length
- Primary goal
- Equipment access
- Injuries / pain constraints

Everything else may fall back to a recorded default. Every default used must
be listed in the program's "Assumptions" section.

## Step 3 — Design pipeline (standardized)

Ten stages (plus the level profile as stage 0), in order; each stage's
output feeds the next. Stages marked
*[rules]* are deterministic — apply the cited rules mechanically. Stages
marked *[judgment]* use the decision trees.

0. **Level profile** *[rules]* — classify the lifter (beginner /
   intermediate / advanced) from training age and apply
   [references/level-matrix.md](references/level-matrix.md) throughout all
   later stages: container, block length, progression speed, starting
   volume, exercise complexity, superset use, specialization permission.
   Level differentiates the whole program structure, not one parameter.
   Check the matrix's moderators (recovery budget, deficit, "progressing →
   change nothing") — they can override the level default.
1. **Recovery context** *[rules]* — read profile Q13 (sleep/stress) and
   Q14 (calories). Deficit: distribute leg volume as single movements
   across the week, keep 1 heavy top set on big lifts (`knowledge/training/06`
   § Prep/Deficit). Poor recovery budget or 35–40+ gray zone: default to
   the moderate branch of the `07` difficulty tree. Record any volume-band
   scaling this forces.
2. **Step 0 audit** *[judgment]* — `knowledge/training/07` § Step 0. If the profile
   includes a current program, audit its per-muscle weekly volume honestly:
   a new split that reduces volume is an atrophy program. No current
   program → start mid-band (middle of 10–20 for priorities, below for the
   rest) and let the logbook calibrate.
3. **Container** *[judgment]* — `knowledge/training/07` decision tree + the
   days-per-week → container mapping (from `knowledge/training/03`; the 07
   specialization branch may reshape the container — e.g. 3 uppers +
   1 lower for an upper priority). If the profile has a split-type
   preference (Q21), treat it as the app-style selection: validate it
   against the tree — honor it when the days/schedule/level allow
   (consistency beats optimality [T19–T22]) and surface the conflict when
   they don't, rather than silently overriding either way:
   - 2 days → full body
   - 3 days → full body (novice) or rotating Upper/Lower (intermediate+)
   - 4 days → Upper/Lower, synchronous (e.g. Mon/Tue/Thu/Fri)
   - 5–6 days → PPL family (synchronous/hybrid), or U/L + PPL hybrid
4. **Volume allocation** *[rules]* — per-muscle weekly sets against the
   landmarks (`knowledge/training/02` + muscle files `09–13`), **counting indirect
   volume**: pressing counts toward triceps (medial/lateral) and front
   delts; respect muscle caps (back >25 sets/wk = recovery risk;
   ~6 sets/muscle/session plateau). Scale the starting band per stage 1.
   Specialization reallocates sets — never conjures them.
5. **Frequency check** *[rules]* — every muscle's weekly sets land in ≥2
   sessions (3× for small/lagging muscles); ≤~6 hard sets/muscle/session;
   ≤~5 sets per exercise per session, then add an exercise at a new angle.
6. **Slot filling** *[judgment on selection, rules on parameters]* —
   `knowledge/training/05` + muscle files. Each session is built from slots:
   compounds first (priority muscle first when specializing), isolations
   later, stretch/lengthened-position bias, injuries as first filter,
   curated per-slot alternatives. Rep range by slot type (`knowledge/training/02`):
   compounds 6–10, isolations 10–15, adjusted for joint tolerance.
7. **Effort layer** *[rules]* — RIR targets by exercise type (`knowledge/training/07`
   § Effort Prescription): heavy free-weight compounds 1–3 RIR even on the
   last set; machines/cables last set to failure, earlier sets 1–2 RIR;
   isolations may go to failure. Novices get loose RIR; intermediates+
   explicit targets. Week 1 calibrates at RIR 3–4 to leave progression room.
8. **Weekly ordering** *[rules]* — `knowledge/training/06` § Rest Days & Scheduling:
   hardest sessions after rest days; deadlifts before the most rest days;
   lower-body days drain CNS ~24 h; never >3 consecutive training days;
   fixed vs rolling layout from `knowledge/training/03`.
9. **Engine** *[rules]* — `knowledge/training/04`: block structure (3–6 overload
   weeks + 1 deload; typical 4+1; novices skip deloads), progression
   method matched to training age (A reps / B sets / C RPE ramp), deload
   lever matched to the stressor (`knowledge/training/06`), logbook feedback loop.
   If the profile specifies a program length (Q22), validate it against
   the level matrix ("Interaction with split-duration selection"): e.g.
   12 wk at intermediate = 2 blocks of 4+1 + a week-1 calibration note;
   a length the matrix rejects (beginner + 4 wk with a deload) gets
   surfaced and corrected, not silently changed.
10. **Gates** *[rules]* — mechanized checks; resolve every warning before
    shipping:
    - Write the per-muscle hard-set counts per session to
      `programs/audits/<name>-<YYYY-MM-DD>.json` and run
      `python3 .agents/skills/split-creator/scripts/volume-audit.py <file>`;
      paste its table **verbatim** into the program's volume-audit section
      (do not hand-edit verdicts) and link the saved audit file. Deliberate
      maintenance/specialization choices stay — flag and justify them in a
      bullet under the table, never by editing it. Landmark data lives in
      `references/volume-landmarks.json`; update it only from cited
      knowledge-file content.
    - **Rest standard:** every exercise prescribes **2 minutes rest**
      (superset partners share one 2-min rest); no per-exercise ranges.
      Mechanize the time budget: add a `"target_min"` (intake Q6) and
      per-session set/superset counts, run
      `python3 .agents/skills/split-creator/scripts/session-length.py <file>`
      (writes `<name>-<YYYY-MM-DD>-length.json`), paste its table verbatim,
      and resolve over-budget warnings by cutting sets, adding supersets,
      or moving work to another session.

**Contradiction policy:** sources disagree by design (see
`knowledge/08-source-map.md` § Known Contradictions). Pick the position that
matches this lifter's context (training age, goal, recovery budget), state
which position was taken and why in the program's rationale. Never average
conflicting numbers or silently drop one side.

## Step 4 — Output

Write the program to `programs/<name>-<YYYY-MM-DD>.md` following
[references/output-spec.md](references/output-spec.md) exactly.

**Never prescribe weights, percentages, or loading suggestions** — the lifter
selects loads. All progression is expressed in reps, sets, and RIR terms.
Rest is always written as "2 min" (the standard) — supersets share it.

## Step 5 — Iteration

On follow-up ("stalling", "not recovering", "sessions too long"), apply the
logbook feedback loop (`knowledge/training/04`): adjust before rebuilding. Save a new
dated program file rather than overwriting, and update the profile if the
person's circumstances changed.
