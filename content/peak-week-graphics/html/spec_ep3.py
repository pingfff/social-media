"""Episode 3 — Sodium 101: visual-first rebuild (SVG charts & diagrams).
Old text-based version preserved in spec_ep3_text_backup.py."""

D = "/Users/ping/Desktop/social-media/content/peak-week-graphics/episode 3/"

SPECS = [

# 01 — HOOK: cut salt Thursday → rebound Saturday (type + rebound arrow)
(D+"ep3-01-hook.png", """
<div class="eyebrow">Sodium 101</div>
<h1 class="h-xl mt-md">CUT SALT<br>THURSDAY?<br><span class="accent-red">BIG MISTAKE</span></h1>
<div class="mt-lg" style="display:flex;justify-content:center">
<svg width="820" height="240" viewBox="0 0 820 240">
  <line x1="40" y1="120" x2="700" y2="120" stroke="#6b7484" stroke-width="6" stroke-linecap="round"/>
  <circle cx="150" cy="120" r="20" fill="#f55b5b"/>
  <text x="150" y="190" fill="#f55b5b" font-family="Anton" font-size="40" text-anchor="middle">THU</text>
  <text x="150" y="60" fill="#aab3c2" font-family="Barlow Condensed" font-size="36" text-anchor="middle">the cut</text>
  <circle cx="650" cy="120" r="26" fill="#f5a623"/>
  <circle cx="650" cy="120" r="40" fill="none" stroke="#f5a623" stroke-width="3" opacity=".5"/>
  <text x="650" y="190" fill="#f5a623" font-family="Anton" font-size="40" text-anchor="middle">SAT</text>
  <text x="650" y="58" fill="#f4f6fa" font-family="Anton" font-size="40" text-anchor="middle">SHOW DAY</text>
  <path d="M190 120 C 350 55, 500 55, 620 105" stroke="#f55b5b" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M620 105 l -26 -20 M620 105 l -30 8" stroke="#f55b5b" stroke-width="7" fill="none" stroke-linecap="round"/>
  <text x="360" y="28" fill="#f55b5b" font-family="Barlow Condensed" font-weight="700" font-size="36" text-anchor="middle">aldosterone rebounds</text>
</svg>
</div>
<div class="body-lg mt-md center">The Army ran this experiment. Here&rsquo;s what happened.</div>
<div class="spacer"></div>
""", "EP 3 &middot; SODIUM 101"),

# 02 — NO SALT = NO FILL: gut-wall membrane diagram, two panels
(D+"ep3-02-no-salt-no-fill.png", """
<div class="eyebrow">Why salt matters</div>
<h1 class="h-md mt-sm">SALT IS THE <span class="accent-coral">TRANSPORT</span> FOR CARBS</h1>
<div class="mt-lg" style="width:100%;display:flex;flex-direction:column;gap:50px">
  <div>
    <div style="font-family:Anton;font-size:52px;color:var(--green);margin-bottom:18px">WITH SALT &rarr; CARBS GET IN</div>
    <svg width="100%" viewBox="0 0 900 260">
      <rect x="20" y="20" width="360" height="220" rx="28" fill="rgba(255,255,255,.04)" stroke="rgba(255,255,255,.08)"/>
      <text x="200" y="255" fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="middle">gut</text>
      <circle cx="110" cy="90" r="26" fill="#f5a623"/><circle cx="185" cy="130" r="26" fill="#f5a623"/><circle cx="115" cy="175" r="26" fill="#f5a623"/>
      <circle cx="280" cy="85" r="18" fill="#f55b5b"/><circle cx="300" cy="150" r="18" fill="#f55b5b"/><circle cx="270" cy="195" r="18" fill="#f55b5b"/>
      <rect x="400" y="10" width="14" height="240" rx="7" fill="#3fd68c" opacity=".85"/>
      <rect x="388" y="70" width="38" height="52" rx="10" fill="#0b0d12" stroke="#3fd68c" stroke-width="3"/>
      <rect x="388" y="150" width="38" height="52" rx="10" fill="#0b0d12" stroke="#3fd68c" stroke-width="3"/>
      <path d="M240 90 C 330 70, 380 80, 500 85" stroke="#f5a623" stroke-width="6" fill="none" stroke-linecap="round"/>
      <path d="M240 175 C 330 190, 380 185, 500 180" stroke="#f5a623" stroke-width="6" fill="none" stroke-linecap="round"/>
      <rect x="520" y="20" width="360" height="220" rx="28" fill="rgba(63,214,140,.06)" stroke="rgba(63,214,140,.35)"/>
      <circle cx="620" cy="90" r="28" fill="#f5a623"/><circle cx="730" cy="130" r="28" fill="#f5a623"/><circle cx="640" cy="180" r="28" fill="#f5a623"/>
      <text x="700" y="255" fill="#3fd68c" font-family="Barlow Condensed" font-size="32" text-anchor="middle">muscle &mdash; full</text>
    </svg>
  </div>
  <div>
    <div style="font-family:Anton;font-size:52px;color:var(--red);margin-bottom:18px">NO SALT &rarr; CARBS PILE UP</div>
    <svg width="100%" viewBox="0 0 900 260">
      <rect x="20" y="20" width="360" height="220" rx="28" fill="rgba(255,255,255,.04)" stroke="rgba(255,255,255,.08)"/>
      <text x="200" y="255" fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="middle">gut &mdash; bloated</text>
      <circle cx="120" cy="95" r="26" fill="#f5a623"/><circle cx="185" cy="75" r="26" fill="#f5a623"/><circle cx="250" cy="95" r="26" fill="#f5a623"/>
      <circle cx="155" cy="150" r="26" fill="#f5a623"/><circle cx="220" cy="160" r="26" fill="#f5a623"/><circle cx="115" cy="195" r="26" fill="#f5a623"/>
      <circle cx="310" cy="200" r="16" fill="#3fa7f5" opacity=".8"/><circle cx="330" cy="150" r="16" fill="#3fa7f5" opacity=".8"/>
      <rect x="400" y="10" width="14" height="240" rx="7" fill="#e04848"/>
      <path d="M382 110 l 50 50 M432 110 l -50 50" stroke="#e04848" stroke-width="8" stroke-linecap="round"/>
      <rect x="520" y="20" width="360" height="220" rx="28" fill="rgba(255,255,255,.03)" stroke="rgba(255,255,255,.10)" stroke-dasharray="14 10"/>
      <text x="700" y="145" fill="#6b7484" font-family="Anton" font-size="46" text-anchor="middle">STAYS FLAT</text>
      <text x="700" y="255" fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="middle">muscle &mdash; empty</text>
    </svg>
  </div>
</div>
<div class="body-md mt-lg center">Water follows the carbs that never made it through</div>
<div class="spacer"></div>
""", "EP 3 &middot; SODIUM 101"),

# 03 — PUMPS: pressure gauge + icon chain
(D+"ep3-03-pumps.png", """
<div class="eyebrow">The pump connection</div>
<div class="mt-md" style="display:flex;justify-content:center">
<svg width="700" height="430" viewBox="0 0 700 430">
  <defs>
    <linearGradient id="gaugeArc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#3fa7f5"/><stop offset="100%" stop-color="#f55b5b"/>
    </linearGradient>
  </defs>
  <path d="M 120 380 A 230 230 0 0 1 580 380" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="34" stroke-linecap="round"/>
  <path d="M 120 380 A 230 230 0 0 1 580 380" fill="none" stroke="url(#gaugeArc)" stroke-width="34" stroke-linecap="round" stroke-dasharray="600 723" opacity=".9"/>
  <g stroke="#6b7484" stroke-width="4">
    <line x1="350" y1="128" x2="350" y2="150"/>
    <line x1="206" y1="196" x2="222" y2="212"/>
    <line x1="494" y1="196" x2="478" y2="212"/>
    <line x1="142" y1="330" x2="166" y2="338"/>
    <line x1="558" y1="330" x2="534" y2="338"/>
  </g>
  <path d="M 350 380 L 545 260" stroke="#f4f6fa" stroke-width="10" stroke-linecap="round"/>
  <circle cx="350" cy="380" r="22" fill="#f4f6fa"/>
  <text x="120" y="420" fill="#3fa7f5" font-family="Barlow Condensed" font-weight="700" font-size="34">low</text>
  <text x="505" y="420" fill="#f55b5b" font-family="Barlow Condensed" font-weight="700" font-size="34">pumped</text>
</svg>
</div>
<h1 class="h-sm mt-sm center">SALT &rarr; BLOOD PRESSURE &rarr; <span class="accent-coral">PUMP</span></h1>
<div class="body-md mt-md center">Acute sodium raises BP &mdash; that&rsquo;s why it belongs<br>before training and before the stage</div>
<div class="spacer"></div>
""", "EP 3 &middot; SODIUM 101"),

# 04 — ARMY STUDY: real line chart
(D+"ep3-04-army-study.png", """
<div class="eyebrow">6 days of sodium restriction</div>
<h1 class="h-sm mt-sm">THE ARMY STUDY</h1>
<div class="mt-lg" style="width:100%">
<svg width="100%" viewBox="0 0 900 620">
  <g stroke="rgba(255,255,255,.06)" stroke-width="2">
    <line x1="90" y1="120" x2="860" y2="120"/><line x1="90" y1="220" x2="860" y2="220"/>
    <line x1="90" y1="320" x2="860" y2="320"/><line x1="90" y1="420" x2="860" y2="420"/>
  </g>
  <text x="70" y="130" fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="end">3&times;</text>
  <text x="70" y="230" fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="end">2&times;</text>
  <text x="70" y="330" fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="end">1&times;</text>
  <line x1="90" y1="415" x2="820" y2="420" stroke="#7a828e" stroke-width="8" stroke-linecap="round"/>
  <text x="455" y="480" fill="#7a828e" font-family="Barlow Condensed" font-weight="700" font-size="36" text-anchor="middle">blood sodium: unchanged (139 &rarr; 138)</text>
  <path d="M90 420 L 350 420 L 490 250 L 640 150 L 800 105" stroke="#f55b5b" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity=".28"/>
  <path d="M90 420 L 350 420 L 490 250 L 640 150 L 800 105" stroke="#f55b5b" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
  <g fill="#f55b5b">
    <circle cx="90" cy="420" r="11"/><circle cx="350" cy="420" r="11"/>
    <circle cx="490" cy="250" r="11"/><circle cx="640" cy="150" r="11"/><circle cx="800" cy="105" r="13"/>
  </g>
  <text x="505" y="215" fill="#f55b5b" font-family="Anton" font-size="40" text-anchor="middle">2&times;</text>
  <text x="655" y="115" fill="#f55b5b" font-family="Anton" font-size="40" text-anchor="middle">3&times;</text>
  <text x="250" y="380" fill="#aab3c2" font-family="Barlow Condensed" font-weight="700" font-size="36" text-anchor="middle">aldosterone</text>
  <line x1="800" y1="66" x2="800" y2="530" stroke="#f5a623" stroke-width="4" stroke-dasharray="12 10"/>
  <rect x="700" y="0" width="200" height="56" rx="14" fill="#f5a623"/>
  <text x="800" y="39" fill="#3a2a00" font-family="Anton" font-size="36" text-anchor="middle">SHOW DAY</text>
  <g fill="#6b7484" font-family="Barlow Condensed" font-size="32" text-anchor="middle">
    <text x="90" y="590">DAY 1</text><text x="350" y="590">DAY 2</text><text x="490" y="590">DAY 3</text>
    <text x="640" y="590">DAY 4</text><text x="800" y="590">DAY 6</text>
  </g>
</svg>
</div>
<div class="body-lg mt-md center">Cut sodium &rarr; your body holds HARDER<br>onto sodium and water, right on stage day</div>
<div class="spacer"></div>
""", "EP 3 &middot; SODIUM 101"),

# 05 — THE RULE: rhythm strips (consistent vs jagged)
(D+"ep3-05-rule.png", """
<div class="eyebrow">The rule</div>
<h1 class="h-md mt-sm">SAME SALT<br><span class="accent-coral">EVERY MEAL</span></h1>
<div class="mt-lg" style="width:100%;display:flex;flex-direction:column;gap:56px">
  <div>
    <div style="font-family:Anton;font-size:46px;color:var(--green);margin-bottom:16px">&#10003; PREDICTABLE</div>
    <svg width="100%" viewBox="0 0 900 150">
      <g>
        <rect x="30"  y="60" width="70" height="60" rx="12" fill="#f55b5b"/>
        <rect x="165" y="60" width="70" height="60" rx="12" fill="#f55b5b"/>
        <rect x="300" y="60" width="70" height="60" rx="12" fill="#f55b5b"/>
        <rect x="435" y="60" width="70" height="60" rx="12" fill="#f55b5b"/>
        <rect x="570" y="60" width="70" height="60" rx="12" fill="#f55b5b"/>
        <rect x="705" y="60" width="70" height="60" rx="12" fill="#f55b5b"/>
      </g>
      <line x1="30" y1="130" x2="775" y2="130" stroke="rgba(255,255,255,.15)" stroke-width="3"/>
      <text x="65" y="40" fill="#6b7484" font-family="Barlow Condensed" font-size="30" text-anchor="middle">M</text>
      <text x="200" y="40" fill="#6b7484" font-family="Barlow Condensed" font-size="30" text-anchor="middle">T</text>
      <text x="335" y="40" fill="#6b7484" font-family="Barlow Condensed" font-size="30" text-anchor="middle">W</text>
      <text x="470" y="40" fill="#6b7484" font-family="Barlow Condensed" font-size="30" text-anchor="middle">T</text>
      <text x="605" y="40" fill="#6b7484" font-family="Barlow Condensed" font-size="30" text-anchor="middle">F</text>
      <text x="740" y="40" fill="#6b7484" font-family="Barlow Condensed" font-size="30" text-anchor="middle">S</text>
    </svg>
  </div>
  <div>
    <div style="font-family:Anton;font-size:46px;color:var(--red);margin-bottom:16px">&#10007; RANDOM &mdash; UNREADABLE BODY</div>
    <svg width="100%" viewBox="0 0 900 150">
      <g opacity=".85">
        <rect x="30"  y="95" width="70" height="25" rx="10" fill="#f55b5b"/>
        <rect x="165" y="30" width="70" height="90" rx="12" fill="#f55b5b"/>
        <rect x="300" y="115" width="70" height="5"  rx="4"  fill="#f55b5b"/>
        <rect x="435" y="55" width="70" height="65" rx="12" fill="#f55b5b"/>
        <rect x="570" y="100" width="70" height="20" rx="10" fill="#f55b5b"/>
        <rect x="705" y="35" width="70" height="85" rx="12" fill="#f55b5b"/>
      </g>
      <path d="M20 75 L 790 75" stroke="#e04848" stroke-width="8" stroke-linecap="round" opacity=".9"/>
      <line x1="30" y1="130" x2="775" y2="130" stroke="rgba(255,255,255,.15)" stroke-width="3"/>
    </svg>
  </div>
</div>
<div class="body-md mt-lg center">Your body only shows you Friday&rsquo;s change<br>if every day before it was identical</div>
<div class="spacer"></div>
""", "EP 3 &middot; SODIUM 101"),

# 06 — END CARD
(D+"ep3-06-endcard.png", """
<div class="spacer"></div>
<div class="eyebrow">Next episode</div>
<h1 class="h-xl mt-md">POTASSIUM<br><span class="accent-violet">THE ONE YOU<br>DON&rsquo;T LOAD</span></h1>
<div class="pill solid-green mt-lg">Follow so you don&rsquo;t miss it</div>
<div class="spacer"></div>
""", "EP 3 &middot; SODIUM 101"),
]
