#!/usr/bin/env python3
"""Generate the 9 lock-in-90 short-form slides (1080x1920).

Vertical layout keeps all content inside the iOS safe zone: headers start
below the camera bump (~300px) and footers sit above the home indicator.
The two screenshot slides (3-4) run their body content ~30% smaller so both
splits, day recommendations, and core work fit on one card each.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BG = (13, 15, 20)
FG = (240, 242, 248)
MUTED = (150, 156, 170)
ACCENT = (255, 176, 32)     # amber
ACCENT2 = (72, 199, 142)    # green
RED = (235, 87, 87)

FONT = "/System/Library/Fonts/Helvetica.ttc"

def F(size, bold=True):
    # single typeface everywhere: Helvetica Bold (the title font)
    return ImageFont.truetype(FONT, size, index=1)

def text_center(d, y, s, font, fill, tracking=0):
    if tracking:
        # letter-spaced text
        widths = [d.textlength(c, font=font) + tracking for c in s]
        total = sum(widths) - tracking
        x = (W - total) / 2
        for c, w in zip(s, widths):
            d.text((x, y), c, font=font, fill=fill)
            x += w
        return y + sum(1 for _ in ())  # unused
    bb = d.textbbox((0, 0), s, font=font)
    w = bb[2] - bb[0]
    d.text(((W - w) / 2 - bb[0], y), s, font=font, fill=fill)
    return y

def wrap(d, s, font, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def draw_wrapped(d, x, y, s, font, fill, maxw, align="left", lh=1.25):
    for line in wrap(d, s, font, maxw):
        if align == "center":
            bb = d.textbbox((0, 0), line, font=font)
            d.text((x - (bb[2]-bb[0])/2 - bb[0], y), line, font=font, fill=fill)
        else:
            d.text((x, y), line, font=font, fill=fill)
        y += int(font.size * lh)
    return y

def new_slide():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)

def top_bar(d, step_label):
    text_center(d, 190, step_label.upper(), F(34, True), ACCENT, tracking=10)
    d.line([(90, 260), (W-90, 260)], fill=(45, 50, 60), width=3)

def footer(d, page):
    text_center(d, H-150, f"{page} / 10", F(28), MUTED)

def card(d, y, h, x0=80, x1=W-80, fill=(24, 28, 36)):
    d.rounded_rectangle([x0, y, x1, y+h], radius=28, fill=fill)

def split_slide(step_label, title1, title2, days, note, page, fname):
    """Screenshot-style split slide; body content ~30% smaller than deck titles."""
    img, d = new_slide()
    top_bar(d, step_label)
    text_center(d, 310, title1, F(42, True), FG)
    text_center(d, 368, title2, F(42, True), ACCENT)
    y = 440
    for label, slots, col in days:
        lines = slots if isinstance(slots, list) else [slots]
        hh = 80 + 36 * len(lines)
        card(d, y, hh)
        text_center(d, y+24, label, F(31, True), col)
        yy = y + 78
        for ln in lines:
            text_center(d, yy, ln, F(26, True), FG)
            yy += 36
        y += hh + 40
    draw_wrapped(d, W/2, y+15, note, F(26, True), MUTED, 880, align="center")
    footer(d, page)
    img.save(fname)

# ---------------------------------------------------------------- slide 1
img, d = new_slide()
text_center(d, 420, "THE", F(70, True), MUTED, tracking=14)
text_center(d, 515, "90-DAY", F(150, True), FG)
text_center(d, 695, "LOCK-IN", F(150, True), ACCENT)
d.line([(120, 920), (W-120, 920)], fill=(45, 50, 60), width=3)
draw_wrapped(d, W/2, 980, "Build your own training program — not someone else's cookie-cutter one.",
             F(46, True), FG, 880, align="center")
card(d, 1180, 420)
text_center(d, 1240, "5 STEPS  ·  REAL NUMBERS", F(52, True), ACCENT2)
text_center(d, 1350, "Splits · Volume · Exercise selection", F(40), MUTED)
text_center(d, 1410, "Progression · When to change", F(40), MUTED)
text_center(d, 1510, "UNDER 90 SECONDS", F(44, True), FG, tracking=6)
footer(d, 1)
img.save("slide1-hook.png")

# ---------------------------------------------------------------- slide 2
img, d = new_slide()
top_bar(d, "Step 1 — Pick your split")
text_center(d, 310, "Your split is a schedule", F(58, True), FG)
text_center(d, 385, "decision, not a personality test", F(58, True), FG)
rows = [
    ("3 DAYS", "FULL BODY", ACCENT2),
    ("4 DAYS", "UPPER / LOWER  —  the sweet spot", ACCENT),
    ("5–6 DAYS", "PUSH / PULL / LEGS", ACCENT2),
]
y = 510
for label, val, col in rows:
    card(d, y, 230)
    text_center(d, y+42, label, F(60, True), col)
    text_center(d, y+124, val, F(44, True), FG)
    y += 275
draw_wrapped(d, W/2, y+30, "Pick the one you'll actually show up for — consistency beats optimization, every time.",
             F(40), MUTED, 860, align="center")
footer(d, 2)
img.save("slide2-split.png")

# ---------------------------------------------------------------- slide 3
# U/L template per knowledge/03-program-styles.md (J3U session design [T17]):
# Upper 1 push-biased (chest-braced rows), Lower 1 hamstring-focused, quads late;
# Upper 2 back-biased first; Lower 2 quad-focused, non-axial, no hinges.
split_slide(
    "Screenshot this",
    "UPPER / LOWER —", "the whole split",
    [
        ("MON · UPPER 1 — PUSH FIRST", ["HORIZONTAL PRESS", "VERTICAL PRESS", "HORIZONTAL PULL", "+ ISOLATIONS & CORE"], ACCENT2),
        ("TUE · LOWER 1 — HAMSTRING FOCUS", ["HINGE", "SQUAT", "+ ISOLATIONS & CORE"], ACCENT2),
        ("THU · UPPER 2 — BACK FIRST", ["VERTICAL PULL", "HORIZONTAL PULL", "VERTICAL PRESS", "+ ISOLATIONS & CORE"], ACCENT2),
        ("FRI · LOWER 2 — QUAD FOCUS · NO HINGE", ["SQUAT", "+ ISOLATIONS & CORE"], ACCENT2),
    ],
    "Every line is a slot — fill it with any lift you love.",
    3, "slide3-ul-split.png")

# ---------------------------------------------------------------- slide 4
# Full body 3x/week per knowledge/03-program-styles.md [T2, T17, T22]:
# the beginner/intermediate default; each day hits every pattern.
split_slide(
    "Screenshot this",
    "FULL BODY —", "the whole split",
    [
        ("MON · DAY 1", ["SQUAT", "HORIZONTAL PRESS", "HORIZONTAL PULL", "+ ISOLATIONS & CORE"], ACCENT2),
        ("WED · DAY 2", ["HINGE", "VERTICAL PRESS", "VERTICAL PULL", "+ ISOLATIONS & CORE"], ACCENT2),
        ("FRI · DAY 3", ["SQUAT — NEW LIFT", "HORIZONTAL PRESS — NEW LIFT", "HORIZONTAL PULL — NEW LIFT", "+ ISOLATIONS & CORE"], ACCENT2),
    ],
    "Every line is a slot — fill it with any lift you love.",
    4, "slide4-fb-split.png")

# ---------------------------------------------------------------- slide 5
# 3-month plan per knowledge/02-programming-variables.md: RPE/RIR escalates
# 6->7->8->9 across a block [T6]; add a set in month 2; deload every 5th week;
# compounds 6-10 / isolations 10-15 [T6, T8].
split_slide(
    "Screenshot this",
    "YOUR 90-DAY PLAN —", "month by month",
    [
        ("MONTH 1 — BUILD THE BASE", ["COMPOUNDS   3 SETS × 6–10 REPS", "ISOLATIONS   2 SETS × 10–15 REPS", "EFFORT   STOP 3–4 REPS SHORT"], ACCENT2),
        ("MONTH 2 — ADD A SET", ["COMPOUNDS   4 SETS × 6–10 REPS", "ISOLATIONS   3 SETS × 10–15 REPS", "EFFORT   STOP 2–3 REPS SHORT"], ACCENT2),
        ("MONTH 3 — TOP OF THE BAND", ["COMPOUNDS   4 SETS × 6–10 REPS", "ISOLATIONS   3 SETS × 10–15 REPS", "EFFORT   STOP 1–2 REPS SHORT"], ACCENT),
    ],
    "EVERY 5TH WEEK: DELOAD — HALF THE SETS, SAME WEIGHTS",
    5, "slide5-plan.png")

# ---------------------------------------------------------------- slide 10
# Concrete prescriptions per knowledge/02-programming-variables.md:
# compounds 6-10 / isolations 10-15 [T6, T8]; rest 2-3 min, heavy legs 4-5 [T3, T4];
# 1-3 reps from failure, log every set [T6]; ~6 hard sets per muscle per session cap [T4, T22].
img, d = new_slide()
top_bar(d, "Step 2 — Your exact numbers")
text_center(d, 300, "Sets, reps, rest —", F(54, True), FG)
text_center(d, 372, "here's what to do", F(54, True), ACCENT)
rows = [
    ("COMPOUNDS", "3 SETS × 6–10 REPS · REST 2–3 MIN · LEGS 4–5", ACCENT2),
    ("ISOLATIONS & CORE", "3 SETS × 10–15 REPS · REST 1–2 MIN", ACCENT2),
    ("EFFORT", "STOP 1–3 REPS FROM FAILURE · LOG EVERY SET", ACCENT2),
    ("SESSION CAP", "MAX ~6 HARD SETS PER MUSCLE · THEN STOP", ACCENT),
]
y = 460
for label, val, col in rows:
    card(d, y, 240)
    text_center(d, y+42, label, F(52, True), col)
    draw_wrapped(d, W/2, y+130, val, F(36, True), FG, 860, align="center", lh=1.25)
    y += 290
draw_wrapped(d, W/2, y+25, "Hit each muscle 2–3× a week and you land in the 10–20-set growth band.",
             F(38, True), MUTED, 880, align="center")
footer(d, 6)
img.save("slide6-numbers.png")

# ---------------------------------------------------------------- slide 10
img, d = new_slide()
top_bar(d, "Step 3 — Fill slots, not exercises")
text_center(d, 300, "Every session is built", F(48, True), FG)
text_center(d, 368, "from these movement slots", F(48, True), FG)
# slot -> 3-4 example exercises, compacted two-line cards
slots = [
    ("SQUAT", "back squat · hack squat · leg press · split squat", ACCENT2),
    ("HINGE", "deadlift · Romanian DL · hip thrust · back extension", ACCENT2),
    ("HORIZONTAL PRESS", "bench press · incline DB press · machine chest press", ACCENT2),
    ("VERTICAL PRESS", "overhead press · DB shoulder press · machine shoulder press", ACCENT2),
    ("HORIZONTAL PULL", "barbell row · chest-supported row · seated cable row", ACCENT2),
    ("VERTICAL PULL", "pull-up · single arm pulldown · lat pulldown", ACCENT2),
    ("CORE", "hanging leg raise · ab wheel · cable crunch · plank", ACCENT2),
    ("+ ISOLATIONS", "curls · triceps extensions · cable lateral raise · calf raises", ACCENT),
]
y = 445
for s, ex, col in slots:
    fill = (24, 28, 36) if s[0] != "+" else (30, 44, 38)
    card(d, y, 104, x0=90, x1=W-90, fill=fill)
    d.text((140, y+16), s, font=F(34, True), fill=col)
    d.text((140, y+62), ex, font=F(24, True), fill=MUTED)
    y += 124
draw_wrapped(d, W/2, y+18, "Pick any exercise you like for each slot.", F(36), MUTED, 860, align="center")
card(d, y+55, 140)
text_center(d, y+100, "COMPOUNDS  6–10 REPS   ·   ISOLATIONS  10–15", F(34), FG)
footer(d, 7)
img.save("slide7-slots.png")

# ---------------------------------------------------------------- slide 8
# Weekly double progression: add reps weekly, top out the range, add load and
# climb again [T6]; log every set ("beat the book").
img, d = new_slide()
top_bar(d, "Step 4 — The engine")
text_center(d, 300, "Every week:", F(58, True), FG)
text_center(d, 378, "beat last week", F(58, True), ACCENT)
card(d, 460, 220)
text_center(d, 505, "THE WEEKLY RULE", F(40, True), ACCENT2)
draw_wrapped(d, W/2, 575, "One more rep than last week, on every set.", F(44, True), FG, 860, align="center")
card(d, 720, 560)
text_center(d, 765, "EXAMPLE — BENCH 3 SETS × 6–10", F(38, True), ACCENT)
weeks = [
    ("WEEK 1", "6 · 6 · 6"),
    ("WEEK 2", "7 · 7 · 6"),
    ("WEEK 3", "8 · 8 · 7"),
    ("WEEK 4", "10 · 10 · 10   —   ADD LOAD, RESTART"),
]
y = 850
for label, reps in weeks:
    text_center(d, y, f"{label}   {reps}", F(40, True), FG if "ADD" not in reps else ACCENT2)
    y += 90
draw_wrapped(d, W/2, 1330, "Write down every set — that's how you know it's working.",
             F(42, True), MUTED, 880, align="center")
footer(d, 8)
img.save("slide8-engine.png")

# ---------------------------------------------------------------- slide 10
img, d = new_slide()
top_bar(d, "Step 5 — When to change exercises")
text_center(d, 330, "DON'T swap", F(80, True), FG)
text_center(d, 435, "every month.", F(80, True), RED)
d.line([(120, 590), (W-120, 590)], fill=(45, 50, 60), width=3)
text_center(d, 650, "If your numbers are climbing —", F(50, True), FG)
text_center(d, 720, "change nothing.", F(50, True), ACCENT2)
card(d, 850, 380)
text_center(d, 900, "SWAP ONLY WHEN", F(40, True), ACCENT)
text_center(d, 970, "a lift stalls for a full block", F(48, True), FG)
text_center(d, 1050, "(4–6 weeks)", F(40), MUTED)
card(d, 1310, 300, fill=(30, 26, 22))
draw_wrapped(d, W/2, 1370, "“Novelty feels productive. Progression is productive.”",
             F(48, True), ACCENT, 840, align="center", lh=1.35)
footer(d, 9)
img.save("slide9-swap.png")

# ---------------------------------------------------------------- slide 10
img, d = new_slide()
text_center(d, 460, "THE WHOLE FRAMEWORK.", F(64, True), FG)
text_center(d, 550, "NOW IT'S YOURS.", F(64, True), FG)
card(d, 760, 420, fill=(28, 46, 38))
text_center(d, 840, "COMMENT", F(48), FG, tracking=8)
text_center(d, 910, "“WINTER”", F(110, True), ACCENT2)
text_center(d, 1070, "and I'll send you the full 90-day program — free", F(40), MUTED)
draw_wrapped(d, W/2, 1260, "Every split, every session, every set — already laid out and volume-audited.",
             F(44, True), FG, 860, align="center", lh=1.35)
footer(d, 10)
img.save("slide10-cta.png")

print("done")
