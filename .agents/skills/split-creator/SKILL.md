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
     one or two batches, then Q2/Q4/Q7/Q12, then Q8–Q11, then Q13–Q20.
     Never dump all 20 at once.
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
     name=<name> q1=<letter|ns|!text> q2=<text> ... q20=<text>
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

## Step 3 — Design pipeline

Consult the knowledge files **in this order**; each stage's output feeds the
next:

1. `knowledge/07-program-selection-decision-tree.md` — pick the split type and
   difficulty from profile sections A + D (training age, current-program audit,
   schedule). If the profile includes a current program, perform Step 0
   (volume audit) honestly: a new split that reduces per-muscle volume is an
   atrophy program.
   **Days-per-week → container mapping** (derived from the `knowledge/03`
   progression ladder; the 07 specialization branch may reshape the
   container — e.g. 3 uppers + 1 lower for an upper priority):
   - 2 days → full body
   - 3 days → full body (novice) or rotating Upper/Lower (intermediate+)
   - 4 days → Upper/Lower, synchronous (e.g. Mon/Tue/Thu/Fri)
   - 5–6 days → PPL family (synchronous/hybrid), or U/L + PPL hybrid
2. `knowledge/03-program-styles.md` — settle the split template and weekly
   layout (fixed weekdays vs rolling, rest-day placement).
3. `knowledge/02-programming-variables.md` + relevant muscle files
   (`knowledge/09-…13`) — per-muscle weekly volume, frequency, rep ranges,
   rest periods. Show the volume allocation against the landmarks, then
   mechanize the check: write the per-muscle hard-set counts per session to
   `programs/audits/<name>-<YYYY-MM-DD>.json` and run
   `python3 .agents/skills/split-creator/scripts/volume-audit.py <file>`;
   paste its generated table **verbatim** into the program's volume-audit
   section (do not hand-edit verdicts), and link the saved audit file.
   Resolve every warning the script prints below the table — deliberate
   maintenance/specialization choices stay, they just get flagged and
   justified in a bullet under the table, never by editing the table.
   Landmark data lives in `references/volume-landmarks.json`; update it only
   from cited knowledge-file content.
   **Rest standard:** every exercise in every generated program prescribes
   **2 minutes rest** (superset partners share one 2-min rest). Do not use
   per-exercise rest ranges. Also mechanize the time budget: add a
   `"target_min"` (intake Q6) and per-session set/superset counts to the
   same audit run via
   `python3 .agents/skills/split-creator/scripts/session-length.py <file>`
   (same directory, `<name>-<YYYY-MM-DD>-length.json`), paste its table
   verbatim, and resolve any over-budget warning by cutting sets, adding
   supersets, or moving work to another session.
4. `knowledge/05-exercise-selection.md` + muscle files — exercise selection
   honoring injuries (first filter), equipment, preferences, and
   stretch/lengthened-position bias. Max ~5 sets per exercise per session;
   spread volume across angles.
5. `knowledge/06-recovery-and-fatigue.md` — rest-day placement, session
   ordering, deload type and timing matched to the program's stressor.
6. `knowledge/04-progression-and-periodization.md` — block structure
   (overload weeks + deload) and the week-to-week progression method matched
   to training age.

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
logbook feedback loop (`knowledge/04`): adjust before rebuilding. Save a new
dated program file rather than overwriting, and update the profile if the
person's circumstances changed.
