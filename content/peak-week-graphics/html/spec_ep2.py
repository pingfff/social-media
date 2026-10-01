"""Episode 2 — Carbs 101: HTML graphic specs."""

D = "/Users/ping/Desktop/social-media/content/peak-week-graphics/episode 2/"

SPECS = [

# 01 — HOOK: 1 g carb drags ~3 g water
(D+"ep2-01-hook.png", """
<div class="eyebrow">Carbs 101</div>
<h1 class="h-xl mt-md">1 GRAM OF CARBS<br><span class="accent-blue">DRAGS 3 GRAMS</span><br>OF WATER WITH IT</h1>
<div class="mt-lg" style="display:flex;align-items:center;gap:36px">
  <div style="width:120px;height:120px;border-radius:50%;background:var(--amber);box-shadow:0 0 70px rgba(245,166,35,.5)"></div>
  <div style="font-family:Anton;font-size:90px;color:var(--dim)">&rarr;</div>
  <div style="display:flex;gap:26px">
    <div style="width:96px;height:96px;border-radius:50%;background:var(--blue);box-shadow:0 0 50px rgba(63,167,245,.5)"></div>
    <div style="width:96px;height:96px;border-radius:50%;background:var(--blue);box-shadow:0 0 50px rgba(63,167,245,.5)"></div>
    <div style="width:96px;height:96px;border-radius:50%;background:var(--blue);box-shadow:0 0 50px rgba(63,167,245,.5)"></div>
  </div>
</div>
<div class="body-lg mt-lg center">That&rsquo;s the entire secret of &ldquo;fullness&rdquo;</div>
<div class="spacer"></div>
""", "EP 2 &middot; CARBS 101"),

# 02 — EQUATION: FULL = carbs + water + sodium
(D+"ep2-02-equation.png", """
<div class="eyebrow">What makes a muscle</div>
<h1 class="h-md mt-sm">FULLNESS IS AN<br>EQUATION</h1>
<div class="eqrow mt-lg">
  <span class="chip accent-amber" style="--accent:var(--amber);border-color:rgba(245,166,35,.55)"><span class="dot" style="background:var(--amber)"></span>Carbs</span>
  <span class="eqplus">+</span>
  <span class="chip accent-blue" style="border-color:rgba(63,167,245,.55)"><span class="dot" style="background:var(--blue)"></span>Water</span>
</div>
<div class="eqrow mt-sm">
  <span class="eqplus">+</span>
  <span class="chip accent-coral" style="border-color:rgba(245,91,91,.55)"><span class="dot" style="background:var(--coral)"></span>Sodium</span>
</div>
<div class="eqeq mt-md">=</div>
<div class="pill solid-green mt-sm">Full</div>
<div class="body-lg mt-lg center">Muscle pushing against skin<br>like a water balloon</div>
<div class="spacer"></div>
""", "EP 2 &middot; CARBS 101"),

# 03 — CAPACITY fuel gauge
(D+"ep2-03-capacity.png", """
<div class="eyebrow">Storage capacity</div>
<h1 class="h-lg mt-sm">YOU HAVE MORE<br>ROOM THAN YOU<br><span class="accent-amber">THINK</span></h1>
<div class="card mt-lg" style="width:100%">
  <div class="tl-row"><div class="tl-day">MUSCLE</div><div class="tl-track"><div class="tl-fill" style="width:22%;background:var(--amber)">350&ndash;500 g</div></div></div>
  <div class="tl-row mt-sm"><div class="tl-day">LIVER</div><div class="tl-track"><div class="tl-fill" style="width:6%;background:var(--blue)">&nbsp;</div></div><div class="tl-note">60&ndash;120 g</div></div>
  <div class="tl-row mt-sm"><div class="tl-day">MAX</div><div class="tl-track"><div class="tl-fill" style="width:100%;background:var(--green)">~2,300 g &mdash; 100 kg of lean tissue</div></div></div>
</div>
<div class="body-lg mt-lg center">&asymp; 23 g glycogen per kg lean mass</div>
<div class="spacer"></div>
""", "EP 2 &middot; CARBS 101"),

# 04 — ASSIMILATION clock
(D+"ep2-04-assimilation.png", """
<div class="eyebrow">Why the Friday panic-feed fails</div>
<h1 class="h-xl mt-sm"><span class="accent-coral">24&ndash;48 H</span></h1>
<h1 class="h-md">TO STORE IT</h1>
<div class="card mt-lg" style="--accent:var(--coral)" >
  <div class="body-lg center">Carbs you eat &rarr; glycogen you can use<br><b style="color:#fff">is not instant</b></div>
</div>
<div class="body-lg mt-lg center">Nothing you eat in the venue parking lot<br>finishes the job today</div>
<div class="spacer"></div>
""", "EP 2 &middot; CARBS 101"),

# 05 — INSULIN SENSITIVITY arrow
(D+"ep2-05-insulin.png", """
<div class="eyebrow">The good news</div>
<h1 class="h-lg mt-sm">POST-PREP<br>CARBS GO<br><span class="accent-green">MUSCLE FIRST</span></h1>
<div class="card mt-lg" style="width:100%">
  <div class="flow-box" style="--accent:var(--amber)"><div class="fb-title">Carbs in</div></div>
  <div class="flow-arrow">&darr;</div>
  <div class="flow-box" style="--accent:var(--green)"><div class="fb-title accent-green">Glycogen refilled</div><div class="fb-sub">extreme insulin sensitivity after a long diet</div></div>
  <div class="flow-arrow">&darr;</div>
  <div class="flow-box" style="--accent:var(--dim)"><div class="fb-title" style="color:var(--dim)">Not fat storage</div><div class="fb-sub">de novo lipogenesis is inefficient when lean</div></div>
</div>
<div class="spacer"></div>
""", "EP 2 &middot; CARBS 101"),

# 06 — END CARD
(D+"ep2-06-endcard.png", """
<div class="spacer"></div>
<div class="eyebrow">Next episode</div>
<h1 class="h-xl mt-md">SODIUM<br><span class="accent-coral">101</span></h1>
<div class="body-lg mt-lg center">Carbs are the cargo.<br>Sodium is the truck.</div>
<div class="pill solid-green mt-lg">Follow so you don&rsquo;t miss it</div>
<div class="spacer"></div>
""", "EP 2 &middot; CARBS 101"),
]
