#!/usr/bin/env python3
"""Render the Winter Lock-In program (winter-program.html content) to PDF via ReportLab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
                                Table, TableStyle, KeepTogether, HRFlowable)

# palette (from the approved HTML)
INK    = colors.HexColor("#181b22")
MUTED  = colors.HexColor("#6b7280")
ACCENT = colors.HexColor("#f0a020")
GREEN  = colors.HexColor("#2f9e77")
RED    = colors.HexColor("#d9534f")
LINE   = colors.HexColor("#e5e7eb")
ROWALT = colors.HexColor("#f6f7f9")
DELOAD = colors.HexColor("#fdf6e9")
DELTXT = colors.HexColor("#8a6116")
NOTE_BG= colors.HexColor("#f2f7f4")
WARN_BG= colors.HexColor("#fdf3f2")
DARK   = colors.HexColor("#0d0f14")

W, H = A4
M = 14*mm
CW = W - 2*M   # content width

body    = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=13.5, textColor=INK, spaceAfter=6)
legend  = ParagraphStyle("legend", parent=body, fontSize=8, leading=10.5, textColor=MUTED)
h2      = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=INK,
                         spaceBefore=14, spaceAfter=6)
h3      = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=INK,
                         spaceBefore=10, spaceAfter=4)
cell    = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5, leading=11, textColor=INK)
cellb   = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
cellg   = ParagraphStyle("cellg", parent=cellb, textColor=GREEN)
cella   = ParagraphStyle("cella", parent=cellb, textColor=colors.HexColor("#b87a10"))
cellm   = ParagraphStyle("cellm", parent=cell, textColor=MUTED)
headc   = ParagraphStyle("headc", fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=colors.white)
note_p  = ParagraphStyle("note", parent=body, fontSize=8.5, leading=12, spaceAfter=0)

def P(t, s=cell): return Paragraph(t, s)

def styled_table(rows, widths, header=True, align_center_cols=None):
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="CENTER")
    st = [("VALIGN", (0,0), (-1,-1), "TOP"),
          ("TOPPADDING", (0,0), (-1,-1), 4), ("BOTTOMPADDING", (0,0), (-1,-1), 4),
          ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
          ("LINEBELOW", (0,0), (-1,-2), 0.5, LINE), ("BOX", (0,0), (-1,-1), 0.75, LINE)]
    if header:
        st += [("BACKGROUND", (0,0), (-1,0), DARK), ("TOPPADDING", (0,0), (-1,0), 5),
               ("BOTTOMPADDING", (0,0), (-1,0), 5)]
        for i in range(1, len(rows)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0,i), (-1,i), ROWALT))
    if align_center_cols:
        for c in align_center_cols:
            st.append(("ALIGN", (c,0), (c,-1), "CENTER"))
    t.setStyle(TableStyle(st))
    return t

def callout(text, bg, border):
    p = Paragraph(text, note_p)
    t = Table([[p]], colWidths=[CW])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),bg),
                           ("LINEBEFORE",(0,0),(0,-1),3,border),
                           ("TOPPADDING",(0,0),(-1,-1),7),("BOTTOMPADDING",(0,0),(-1,-1),7),
                           ("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10)]))
    return t

def section(num, title):
    return [Spacer(1, 10),
            HRFlowable(width="100%", thickness=1.6, color=INK, spaceAfter=6),
            Paragraph(f'<font color="#f0a020">{num}</font>&nbsp;&nbsp;{title}', h2)]

story = []

# ---- hero ----
hero_inner = [
    [Paragraph('<font color="#f0f2f8"><b>WINTER</b></font> <font color="#f0a020"><b>LOCK-IN</b></font>',
               ParagraphStyle("h1c", fontName="Helvetica-Bold", fontSize=30, leading=34))],
    [Paragraph("The complete 90-day program — every split, every session, every set already laid out. "
               "This is the exact framework from the carousel, filled in for you. Pick your track, "
               "follow the monthly plan, beat last week's numbers. That's the whole job.",
               ParagraphStyle("herop", fontName="Helvetica", fontSize=9.5, leading=14,
                              textColor=colors.HexColor("#9aa0ae")))],
    [Paragraph('<b>13 WEEKS · TRACK A: 4 DAYS (UPPER/LOWER) · TRACK B: 3 DAYS (FULL BODY)</b>',
               ParagraphStyle("tagp", fontName="Helvetica-Bold", fontSize=8, leading=11, textColor=GREEN))],
]
hero = Table(hero_inner, colWidths=[CW])
hero.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),DARK),
                          ("LEFTPADDING",(0,0),(-1,-1),18),("RIGHTPADDING",(0,0),(-1,-1),18),
                          ("TOPPADDING",(0,0),(0,0),20),("BOTTOMPADDING",(0,-1),(0,-1),20),
                          ("TOPPADDING",(0,1),(0,2),8)]))
story.append(hero)

# ---- 01 how it works ----
story += section("01", "How the 90 days work")
story.append(P("Three months, three jobs. Each month gets slightly harder — more sets, then closer to "
               "failure — while the exercises never change. You add reps every week; when you hit the top "
               "of a rep range on every set, add a little weight and start the climb again.", body))
rows = [[P("Phase",headc),P("Weeks",headc),P("Compound sets",headc),P("Isolation sets",headc),P("Effort (stop…)",headc)],
    [P("MONTH 1 — Build the base",cellg),P("1–4",cell),P("3 per exercise",cell),P("2 per exercise",cell),P("3–4 reps short of failure",cell)],
    [P("DELOAD",cella),P("5",cell),P("half the sets",cell),P("half the sets",cell),P("same weights, everything easy",cell)],
    [P("MONTH 2 — Add a set",cellg),P("6–9",cell),P("4 per exercise",cell),P("3 per exercise",cell),P("2–3 reps short of failure",cell)],
    [P("DELOAD",cella),P("10",cell),P("half the sets",cell),P("half the sets",cell),P("same weights, everything easy",cell)],
    [P("MONTH 3 — Top of the band",cella),P("11–13",cell),P("4 per exercise",cell),P("3 per exercise",cell),P("1–2 reps short of failure",cell)]]
t = styled_table(rows, [CW*.26, CW*.09, CW*.19, CW*.19, CW*.27])
t.setStyle(TableStyle([("BACKGROUND",(0,2),(-1,2),DELOAD),("BACKGROUND",(0,4),(-1,4),DELOAD)]))
story.append(t); story.append(Spacer(1,6))
story.append(callout("<b>The weekly rule:</b> beat last week's reps on every set. Bench 3×6–10 — week 1 you get "
                     "6, 6, 6. Week 2, 7, 7, 6. When you hit 10, 10, 10, add a little weight and start over at 6s. "
                     "Write every set down (notes app, notebook, whatever) — that's how you know it's working.",
                     NOTE_BG, GREEN))

# ---- 02 pick track ----
story += section("02", "Pick your track")
rows = [[P("",headc),P("Track A — Upper/Lower",headc),P("Track B — Full Body",headc)],
        [P("Days",cellb),P("4 per week — Mon / Tue / Thu / Fri",cell),P("3 per week — Mon / Wed / Fri",cell)],
        [P("Best for",cellb),P("You can train 4 days and want the fastest route",cell),P("3 days is what your schedule gives you",cell)],
        [P("Session length",cellb),P("~55–70 min",cell),P("~60–75 min",cell)]]
story.append(styled_table(rows, [CW*.16, CW*.42, CW*.42]))
story.append(P("Both tracks use the same monthly plan from section 01. Do one warm-up set of the first exercise "
               "per muscle before each session — light, never counted as work.", legend))

# ---- session table helper ----
def session(title, rows):
    data = [[P("#",headc),P("Exercise",headc),P("Sets × Reps",headc),P("Rest",headc),P("Notes / substitutions",headc)]]
    for i,(ex,sr,r,note) in enumerate(rows):
        data.append([P(str(i+1),cell),P(ex,cellb),P(sr,cell),P(r,cell),P(note,cellm)])
    tbl = styled_table(data, [CW*.05, CW*.28, CW*.13, CW*.09, CW*.45])
    return KeepTogether([Paragraph(title, h3), tbl, Spacer(1,4)])

# ---- 03 track A ----
story += section("03", "Track A — Upper/Lower (4 days)")
story.append(session("UPPER 1 — Monday (push-led)", [
    ("Barbell Bench Press","3 × 6–10","2 min","Machine chest press works fine"),
    ("Seated DB Shoulder Press","3 × 6–10","2 min","Alt: machine shoulder press"),
    ("Chest-Supported Row (machine or bench)","3 × 6–10","2 min","Alt: seated cable row, machine row"),
    ("Cable Lateral Raise","2 × 10–15","2 min","Side delts get nothing from pressing — don't skip"),
    ("Rope Pushdown","2 × 10–15","2 min","Alt: any triceps machine"),
    ("Hanging Leg Raise","2 × 10–15","2 min","Alt: ab wheel, cable crunch")]))
story.append(session("LOWER 1 — Tuesday (hamstring-led)", [
    ("Romanian Deadlift","3 × 6–10","2 min","The deadlift-style lift goes first while you're fresh — that's the point of this day"),
    ("Back Squat","3 × 6–10","2–4 min","Comes second on purpose. Alt: hack squat, leg press"),
    ("Leg Curl","2 × 10–15","2 min","Seated or lying"),
    ("Standing Calf Raise","2 × 10–15","2 min","Pause at the bottom stretch"),
    ("Ab Wheel","2 × 10–15","2 min","Alt: plank, cable crunch")]))
story.append(session("UPPER 2 — Thursday (back-led)", [
    ("Pull-Up","3 × 6–10","2 min","Alt: lat pulldown, single-arm pulldown"),
    ("Barbell Row","3 × 6–10","2 min","Alt: chest-supported row if lower back is beat"),
    ("Machine Shoulder Press","3 × 6–10","2 min","Want more chest? Swap for incline DB press"),
    ("DB Lateral Raise","2 × 10–15","2 min","Lighter than ego wants — control it"),
    ("Hammer Curl","2 × 10–15","2 min","Alt: incline DB curl"),
    ("Cable Crunch","2 × 10–15","2 min","Alt: hanging leg raise")]))
story.append(session("LOWER 2 — Friday (quad-led — no hinge today)", [
    ("Hack Squat","3 × 6–10","2–4 min","No barbell on your back today — your lower back gets a break. Alt: leg press"),
    ("Leg Extension","2 × 10–15","2 min","Squeeze at the top"),
    ("Seated Calf Raise","2 × 10–15","2 min",""),
    ("Cable Crunch","2 × 10–15","2 min","")]))

# ---- 04 track B ----
story += section("04", "Track B — Full Body (3 days)")
story.append(session("DAY 1 — Monday", [
    ("Back Squat","3 × 6–10","2–4 min","Alt: hack squat, leg press"),
    ("Barbell Bench Press","3 × 6–10","2 min","Alt: machine chest press"),
    ("Barbell Row","3 × 6–10","2 min","Alt: chest-supported row"),
    ("Cable Lateral Raise","2 × 10–15","2 min",""),
    ("Hammer Curl","2 × 10–15","2 min",""),
    ("Hanging Leg Raise","2 × 10–15","2 min","")]))
story.append(session("DAY 2 — Wednesday", [
    ("Romanian Deadlift","3 × 6–10","2 min","Alt: hip thrust, back extension"),
    ("Overhead Press","3 × 6–10","2 min","Alt: seated DB / machine shoulder press"),
    ("Lat Pulldown","3 × 6–10","2 min","Alt: pull-up, single-arm pulldown"),
    ("Rope Pushdown","2 × 10–15","2 min",""),
    ("Standing Calf Raise","2 × 10–15","2 min",""),
    ("Ab Wheel","2 × 10–15","2 min","")]))
story.append(session("DAY 3 — Friday (same slots, new lifts)", [
    ("Hack Squat <i>(instead of back squat)</i>","3 × 6–10","2–4 min","New lift for the squat slot"),
    ("Incline DB Press <i>(instead of flat bench)</i>","3 × 6–10","2 min","New lift for the press slot"),
    ("Seated Cable Row <i>(instead of barbell row)</i>","3 × 6–10","2 min","New lift for the pull slot"),
    ("DB Lateral Raise","2 × 10–15","2 min",""),
    ("Incline DB Curl","2 × 10–15","2 min",""),
    ("Cable Crunch","2 × 10–15","2 min","")]))

# ---- 05 rules ----
story += section("05", "The rules that make it work")
story.append(Paragraph("When to change exercises: you mostly don't", h3))
story.append(callout("<b>Don't swap exercises every month.</b> If your numbers are still climbing, change nothing. "
                     "Swap only when a lift has been stuck for 4–6 weeks — same reps, same weight, no progress. "
                     "Novelty feels productive; progression is productive.", WARN_BG, RED))
story.append(Spacer(1,6))
story.append(Paragraph("Deload weeks (5 and 10)", h3))
story.append(P("Half the sets, same weights, everything feels easy. You're letting your body catch up, not pushing "
               "for records — in week 6, go right back to the weights you were using in week 4.", body))
story.append(Paragraph("If a whole week goes bad", h3))
story.append(P("Missed sleep, work blew up, or two rough sessions in a row — just repeat the previous week instead "
               "of pushing forward. Never add extra exercises to \"make up\" for missed sessions.", body))
story.append(Paragraph("Want more of a specific muscle?", h3))
story.append(P("From month 2 onward, you may swap one exercise per session for a different one that hits the muscle "
               "you care about most (e.g., incline press in place of shoulder press on Upper 2 for more chest). "
               "One swap — not a rebuild. The volume table below shows where you have room.", body))

# ---- 06 volume audit ----
story += section("06", "Weekly volume audit (Track A, month 3)")
story.append(P("Working sets (not warm-ups) per muscle per week, counted directly plus the help they get from "
               "shared exercises. The growth sweet spot is 10–20 sets.", legend))
rows = [[P("Muscle",headc),P("Direct",headc),P("+ Indirect",headc),P("Total",headc),P("Verdict",headc)],
    [P("Quads",cellb),P("8",cell),P("+2",cell),P("10",cell),P("In the sweet spot",cellg)],
    [P("Hamstrings",cellb),P("7",cell),P("+2",cell),P("9",cell),P("In the sweet spot (lower end — on purpose)",cellg)],
    [P("Chest",cellb),P("4",cell),P("+4",cell),P("8",cell),P("Below the sweet spot — use the chest swap in section 5 if chest is a priority",cella)],
    [P("Back (lats/upper)",cellb),P("8",cell),P("+2",cell),P("10",cell),P("In the sweet spot",cellg)],
    [P("Side delts",cellb),P("6",cell),P("+6",cell),P("12",cell),P("In the sweet spot",cellg)],
    [P("Triceps",cellb),P("3",cell),P("+9",cell),P("12",cell),P("In the sweet spot",cellg)],
    [P("Biceps",cellb),P("3",cell),P("+4",cell),P("7",cell),P("Lower end — fine for most; arms-focused lifters add curls in month 2+",cella)],
    [P("Calves",cellb),P("6",cell),P("",cell),P("6",cell),P("Enough to keep them growing slowly; add a set in month 3 if calves matter to you",cella)]]
story.append(styled_table(rows, [CW*.17, CW*.08, CW*.10, CW*.08, CW*.57], align_center_cols=[1,2,3]))
story.append(Spacer(1,6))
story.append(callout("Track B lands similarly (~10–14 sets for the big muscles). Full body days spread volume "
                     "thinner per session but frequency is higher, which evens out over the week.", NOTE_BG, GREEN))

# ---- 07 calendar ----
story += section("07", "Your 13-week calendar")
cal = [[P("Wk",headc)]+[P(str(i),headc) for i in range(1,14)]]
phases = [("MONTH 1 — 3 sets · 3–4 short", [1,2,3,4], DELTXT, DELOAD),
          ("DELOAD", [5], DELTXT, DELOAD),
          ("MONTH 2 — 4 sets · 2–3 short", [6,7,8,9], INK, colors.white),
          ("DELOAD", [10], DELTXT, DELOAD),
          ("MONTH 3 — 4 sets · 1–2 short", [11,12,13], INK, colors.white)]
row = [P("Phase",cellb)]
labels = {w:(txt,bg) for txt,wks,_,bg in phases for w in wks for txt in [txt]}
row2 = [P("Phase",cellb)]
for w in range(1,14):
    txt = next(t for t,wks,_,_ in phases if w in wks)
    bg = next(b for t,wks,_,b in phases if w in wks)
    row2.append(P(txt if w in (1,5,6,10,11) else "", ParagraphStyle("cal", parent=cellb, fontSize=6.5, leading=8.5, alignment=TA_CENTER)))
cal.append(row2)
t = styled_table(cal, [CW*.08] + [CW*.92/13]*13, header=True, align_center_cols=list(range(14)))
deload_bg = []
for c in (5,10):
    deload_bg.append(("BACKGROUND",(c,1),(c,1),DELOAD))
t.setStyle(TableStyle(deload_bg))
story.append(KeepTogether([t]))
story.append(P("Same exercises all 13 weeks. Only the sets and effort change — and your rep numbers climb.", legend))

doc = BaseDocTemplate("winter-program.pdf", pagesize=A4,
                      leftMargin=M, rightMargin=M, topMargin=12*mm, bottomMargin=12*mm,
                      title="Winter Lock-In — The 90-Day Program",
                      author="Z.ai", subject="90-day hypertrophy program", creator="Z.ai")
frame = Frame(M, 12*mm, CW, H-24*mm, id="f")
doc.addPageTemplates([PageTemplate(id="page", frames=[frame])])
doc.build(story)
print("built winter-program.pdf")
