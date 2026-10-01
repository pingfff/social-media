# Design System Reference

Companion to `content/peak-week-graphics/html/graphics.css`. Read this before
writing specs.

## Canvas & bands (1080x1920)

- `.page` handles padding (90x70px) and vertical flex — put content inside it.
- Top band (~y 120–400): `.eyebrow` (small caps label) + headline `h1`.
- Center band: the main visual (stat, timeline, flow…). Use `.spacer` to
  center vertically.
- Lower band: `.body-lg`/`.body-md` caption line.
- Bottom: `.footerline` + `.footertag` are added automatically by `render.py`
  from the spec's footer_tag.

## Typography scale

| Class | Size | Use |
|---|---|---|
| `giant` | 300px | one huge number (99%, 24–48 H) |
| `h-xl` | 150px | hook headlines |
| `h-lg` | 118px | standard headlines |
| `h-md` | 86px | section headlines |
| `h-sm` | 64px | card titles |
| `.body-lg` / `.body-md` | 44/38px | captions, subs |

Display face is Anton (uppercase only look); body is Barlow Condensed.
Accent a word: `<span class="accent-blue">word</span>` (amber/blue/coral/
green/red/violet).

## Components (snippets)

Hook:
```html
<div class="eyebrow">Carbs 101</div>
<h1 class="h-xl mt-md">1 GRAM OF CARBS<br><span class="accent-blue">DRAGS 3 GRAMS</span></h1>
<div class="body-lg mt-lg center">That's the entire secret of "fullness"</div>
<div class="spacer"></div>
```

Big stat:
```html
<div class="eyebrow">Storage capacity</div>
<h1 class="h-lg mt-sm">YOU HAVE MORE<br>ROOM THAN YOU<br><span class="accent-amber">THINK</span></h1>
<div class="card mt-lg" style="width:100%"> ... </div>
```

Equation (chips):
```html
<span class="chip" style="border-color:rgba(245,166,35,.55)"><span class="dot" style="background:var(--amber)"></span>Carbs</span>
<span class="eqplus">+</span> ... <div class="eqeq mt-md">=</div>
<div class="pill solid-green mt-sm">Full</div>
```

Vertical timeline (load strategies, protocols):
```html
<div class="tl-row"><div class="tl-day">MON</div>
  <div class="tl-track"><div class="tl-fill" style="width:22%;background:var(--amber)">350 g</div></div>
  <div class="tl-note">note</div></div>
```

Checklist (rules, do/don't):
```html
<div class="check-row struck" style="--accent:var(--red)">
  <div class="mark" style="background:var(--red);color:#fff">&times;</div>
  <div class="label">Cut sodium</div></div>
```
(Green `&check;` for do-rules; struck + red `&times;` for don't-rules.)

Flow (mechanisms, cause→effect):
```html
<div class="flow-box" style="--accent:var(--coral)">
  <div class="fb-title accent-coral">Cortisol &uarr;</div>
  <div class="fb-sub">same receptor as aldosterone</div></div>
<div class="flow-arrow">&darr;</div>
```

Comparison panels (FLAT | FULL | SPILLED etc.):
```html
<div class="panels">
  <div class="panel" style="--accent:var(--flat)"><div class="p-name">Flat</div><div class="p-sub">small · soft</div></div>
  ...
</div>
```

End card:
```html
<div class="spacer"></div>
<div class="eyebrow">Next episode</div>
<h1 class="h-xl mt-md">SODIUM<br><span class="accent-coral">101</span></h1>
<div class="pill solid-green mt-lg">Follow so you don't miss it</div>
<div class="spacer"></div>
```

## Color semantics (fixed)

- `--amber` carbs · `--blue` water · `--coral` sodium · `--violet` potassium
- `--green` positive/full · `--red` danger/spill · `--flat` flat state
- Keep the same meaning across every collection so the feed looks coherent.

## Common failure modes

- Text too long → overflow skip. Shorten copy before shrinking type.
- **SVG label collisions.** Hand-placed SVG text is invisible to layout
  flow — the renderer only catches text-on-text overlap, not text on
  lines/bars/rects. Rules of thumb: never place a badge on the axis-label
  row (put it at the top of its marker line, clear of everything); keep
  ≥30px between any SVG text and any line/bar it isn't labeling; when two
  labels could ever share space (axis vs badge, line label vs marker),
  move one to an empty band. Example fix pattern: a SHOW DAY badge that
  overlapped "DAY 6" on the axis was moved to the top end of the dashed
  marker line where nothing else lives.
- Font not loading (offline): renderer falls back to Impact/Arial Narrow —
  acceptable, but re-render when back online.
- Don't nest `.card` inside `.card`; use one card + flow rows instead.

## Multi-lane timeline pattern (density-safe)

For protocol graphics tracking 2–3 variables (water/sodium/carbs) across
days: one lane per variable, equal-width day columns shared by every lane
and the label row, amount encoded as BAR HEIGHT inside a fixed-height track.
Never vary column widths (breaks cross-lane alignment), never put text
inside narrow cells, and use generous spacing (~120px lanes, ~60px gaps,
label + right-aligned summary on its own line above each lane). Reference
implementation: `spec_ep7.py` graphic 02.

- If a topic needs more than 3 lanes or ~7 rows, split it into two
  graphics rather than compressing.
