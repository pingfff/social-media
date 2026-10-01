# Peak Week Graphics

Vertical 1080x1920 Reels overlays for the 17-episode Instagram series
(`../peak-week-scripts/`).

## Structure

- `episode 1/` ... `episode 17/` — final PNGs, numbered in script beat order
  (`epN-01-hook.png` ... `epN-NN-endcard.png`).
- `hero-square/` — older 1080x1080 hero graphics (superseded; kept for feed posts).
- `html/` — the rendering system:
  - `graphics.css` — shared design system (Anton/Barlow Condensed/Inter via
    Google Fonts, dark gradient + grain, color coding: amber=carbs,
    blue=water, coral=sodium, violet=potassium, green=positive, red=danger).
  - `spec_epN.py` — one module per episode: `SPECS = [(png_path, inner_html,
    footer_tag)]`.
  - `render.py` — renders specs via headless Chromium (Playwright) with an
    in-browser overflow check; skips any graphic whose content overflows.
- `vlib.py` — legacy matplotlib library (superseded by the HTML system).

## Re-rendering

    cd html
    python3 render.py spec_ep2      # any single episode

Requires `pip3 install playwright && python3 -m playwright install chromium`.

## Editing a graphic

Edit its HTML block in `html/spec_epN.py` and re-render. Classes available:
eyebrow, h-xl/h-lg/h-md/h-sm, giant, card, chip, pill, eqrow, tl-* (timeline),
check-row (checklist), flow-* (flows), panels/panel (comparisons), body-lg/md.
