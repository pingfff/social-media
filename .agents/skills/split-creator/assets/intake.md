# Intake Questionnaire

Lifter profile for split design. Answer by option letter or free text;
pressing Enter / "ns" accepts the default (defaults are always disclosed in
the generated program). ★ = hard-required.

The CLI validates option answers against the letters shown (an optional
note may follow the letter, e.g. `a mon/wed only`), records `ns` answers as
`[ns: defaulted]`, and accepts `!some text` as a free-text override when no
option fits (recorded as `[free text]`). Both markers must be disclosed in
the generated program's Assumptions section.

Two ways to fill this in:
- **In-chat (default):** ask the agent to design a split — it immediately
  interviews you with these questions via interactive prompts (★ questions
  first, then grouped batches), then writes the profile through the intake
  script's `--batch` mode so validation matches the terminal form exactly.
- **Terminal:** `bash .agents/skills/split-creator/scripts/intake.sh`
  runs the same questionnaire as an interactive CLI form.

Every question maps to a design decision: the annotation in *italics* names
the knowledge file(s) that consume the answer.

---

## A. Who

**Q1. ★ Training age?** *→ 07 ladder position; 04 progression method; deload need*
  a) none  b) <1 yr  c) 1–3 yrs  d) 3–10 yrs  e) 10+ yrs

**Q2. Age?** ____ *→ 06 recovery assumptions; 07 aggressiveness filter (35–40 gray zone, 50+)*

## B. Goal

**Q3. ★ Primary goal?** *→ 03 split structure; 04 progression style*
  a) hypertrophy  b) strength  c) recomp  d) general fitness

**Q4. Priority or lagging muscles?** ____ *→ 07 specialization branch; exercise order in 05; muscle-file volume bump*

## C. Schedule

**Q5. ★ Days per week available?** *→ 03 split choice*
  a) 2  b) 3  c) 4  d) 5  e) 6

**Q6. ★ Max session length?** *→ 07: ≤45 min → body-part days; >1.5 h → move up ladder*
  a) 45 min  b) 60 min  c) 75 min  d) 90+ min

**Q7. Schedule type + day constraints?** *→ 03 fixed vs rotating; 06 rest-day placement (leg/deadlift days after rest)*
  a) fixed weekdays (→ U/L or hybrid PPL)  b) flexible/rolling (→ rotating PPL)
  Preferred/impossible days: ____

## D. Current training

**Q8. Current split + months on it?** ____ *→ 07 Step 0 audit; 03 ladder position*

**Q9. Rough weekly hard sets per muscle?** ____ *→ 07 Step 0: new split must not reduce volume below current*

**Q10. Last 3 months: what progressed / stalled?** ____ *→ 07 Step 0 weak-point detection; ladder trigger*

**Q11. End-of-session state?** *→ 03 ladder trigger (sessions too long / back-half stalling)*
  a) fresh  b) drained  c) sessions routinely overrun 1–1.5 h

**Q12. Near-failure habits?** *→ 02 effort prescription; contradiction #11 resolution*
  a) regularly reach ~0–3 RIR  b) usually stop well short  c) never near failure

## E. Recovery & calories

**Q13. Recovery budget (sleep + stress combined)?** *→ 06 scheduling; 07 aggressive vs moderate design*
  a) good (7h+, low stress)  b) average  c) poor (short/poor sleep or high stress)

**Q14. Calorie situation?** *→ 06 deficit rules: distribute leg volume, keep 1 heavy top set*
  a) surplus  b) maintenance  c) deficit

## F. Equipment

**Q15. ★ Equipment access + notable machines?** *→ 05 exercise pool + substitutions; muscle-file picks*
  a) full commercial gym  b) basic gym (barbells/DBs/few machines)
  c) home setup  d) minimal (DBs/bands only)
  Machines worth noting (cables, hack squat, Smith…): ____

## G. Constraints & tastes

**Q16. ★ Injuries, painful movements, or mobility limits?** ____ *→ 05 first filter: swap or modify anything that hurts*
  (or "none")

**Q17. Exercise likes/dislikes/dealbreakers?** ____ *→ 05 selection pool; adherence (consistency rule, 07)*
  Disliked: ____  Favorites: ____ (or "no strong feelings")

## H. Preferences

**Q18. Frequency preference?** *→ 03: preference is a legitimate split selector (bro-split defense)*
  a) enjoy hitting muscles often  b) prefer rare & focused

**Q19. Deload preference?** *→ 06/T15 deload type selection*
  a) scheduled  b) by feel  c) spread-week (frequency deload)

**Q20. Anything else the program should respect?** ____ *→ adherence; the consistency rule beats optimization*

---

## Defaults (used when an answer is missing — always disclose in the program)

| Missing | Default |
|---|---|
| Q12 near-failure habits | ~2–3 RIR baseline; machines/cables may go to failure |
| Q13 recovery budget | Average — no aggressive high-frequency designs |
| Q14 calories | Maintenance |
| Q18 frequency preference | Split-type defaults from `knowledge/03` |
| Q19 deload preference | Scheduled deload every 4–6 weeks by program stressor (T15) |
| Q8–10 audit details | Ask once; if unknown, design conservatively and flag the assumption |
