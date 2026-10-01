---
name: reel-graphics
description: Generates vertical 1080x1920 Instagram Reels graphics (hooks, stat cards, timelines, checklists, flows, comparison panels, end cards) using the repo's HTML/CSS design system rendered via headless Chromium. Use whenever the user asks for reel overlays, Instagram story/vertical graphics, on-screen visuals for videos, episode graphics, or wants to edit/re-render existing graphics in content/peak-week-graphics/ — even if they just say "make a visual/graphic for this episode/beat".
---

# Reel Graphics

Produces polished vertical (1080x1920) graphics for social videos by writing
small HTML specs and screenshotting them with headless Chromium. The design
system already exists — never rebuild it from scratch.

## The pipeline

Everything lives in `content/peak-week-graphics/html/`:

- `graphics.css` — the shared design system (fonts, colors, components).
- `render.py` — renderer + in-browser overflow checker.
- `spec_epN.py` — one module per episode/collection: `SPECS = [(png_path, inner_html, footer_tag)]`.

To generate or edit graphics:

1. Read `content/peak-week-graphics/html/graphics.css` and one existing spec
   (start with `spec_ep2.py`, the approved pilot) to learn the component classes.
2. Read `references/design-system.md` in this skill for color coding, layout
   bands, and the graphic archetypes with HTML snippets.
3. Add or edit specs in an existing `spec_*.py`, or create a new one (e.g.
   `spec_coaching.py` for a new content collection). Output paths point at the
   relevant collection folder, e.g. `content/peak-week-graphics/episode 2/`
   or a new `content/<collection>-graphics/` folder.
4. Render from the html directory:
   `cd content/peak-week-graphics/html && python3 render.py spec_ep2`
5. The renderer prints `OVERFLOW` and skips any graphic whose content escapes
   the canvas — reword or drop to a smaller heading class until everything
   saves cleanly. Never bypass this check.

If Playwright/Chromium is missing, install once:
`pip3 install playwright && python3 -m playwright install chromium`.

## Hard rules

- **1080x1920 only**, one idea per graphic, text SHORT (phone-sized reading).
- **Phone safe-area: no text within ~105px of the sides, ~135px of the top,
  or ~135px of the bottom canvas edge — and keep the bottom ~300px clear of
  anything important (the Reels UI overlays username/caption there).** The
  `.page` padding and footer position in `graphics.css` already enforce
  this, and `render.py` fails any text element that enters the unsafe
  border (`unsafe:` in the output). Design within the padded area; don't
  override `.page` padding or move the footer down.
- **Chart data must be drawn from the `## Protocols & Numbers` tables in the
  relevant `knowledge/bodybuilding/` file — never from prose, and never from
  a secondhand summary.** Those tables are the canonical, cited home for
  day-by-day amounts (e.g. standard back load = keto Mon–Wed, load begins
  Thu, peak carbs the day before the show; rapid back load = the entire load
  in the final 24 h). Do not conflate strategy variants in one timeline;
  label which variant a graphic shows. A chart with plausible-looking but
  wrong bars misleads viewers more than no chart.
- **Timelines must be complete.** If a graphic shows a peak-week protocol,
  every day of the stated range gets a row (Mon–Sat unless the strategy
  explicitly starts earlier, e.g. front load's Sunday deplete). Count the
  rows against the day labels before rendering; a missing Saturday was a
  real shipped bug.
- **Density budget: a graphic may carry at most ~3 data lanes / 6–7 rows.**
  Dense topics (multi-variable protocols) get split across graphics or
  restructured, never squeezed. Spacing rules when a chart holds multiple
  lanes: equal-width columns aligned across all lanes and the day-label row
  (encode AMOUNT as bar height inside a fixed grid — never as varying
  column widths, which break alignment); tall lanes (~120px) with large gaps
  between lanes (~60px); lane labels go on their own line above the lane,
  with the one-line summary right-aligned on the same line — no text inside
  narrow cells, no side note columns. If you remove all spacing and the
  graphic still reads as a wall, it is two graphics.
- **No information may ever overlay other information.** Labels, axis text,
  badges, and markers each need their own exclusive zone. The renderer checks
  HTML overflow AND pairwise overlap of SVG `<text>` elements — but it cannot
  catch SVG text sitting on shapes/lines/bars, so when hand-placing SVG:
  give every label clear margin from lines, bars, and other labels; place
  axis badges above or beside the chart area, never on the axis row; and when
  in doubt, move it further away. Overlapping text on a chart is a hard
  failure, not a style nit — a viewer misreading the axis is worse than no
  chart.
- Use the CSS classes; do not invent inline styles for things the system
  already provides (cards, chips, timelines, checklists, flows, panels).
- Color coding is fixed: amber=carbs, blue=water, coral=sodium, violet=potassium,
  green=positive, red=danger, grey=flat state.
- Layout bands: eyebrow/title at top, main content center, caption lower,
  footer tag bottom (`EP N · TOPIC` or collection equivalent).
- Every episode/content set gets a hook graphic first and an end-card last.
- No citations in graphics — they are viewer-facing.
- Health-risk topics get a `.disclaimer` line: "General information, not
  medical advice".

## After rendering

Verify output files are exactly 1080x1920 (e.g. with PIL) and report which
files changed. If the user supplied a reference image or brand asset, adapt
`graphics.css` variables/colors in one place rather than per-graphic overrides,
and note the change so the whole system stays consistent.
