#!/usr/bin/env python3
"""Render peak-week graphics from HTML specs via headless Chromium.
Usage: python3 render.py <spec.py module name>  — spec modules define SPECS: list of (filename, html).
Each HTML must be a full <body class="page"> inner; boilerplate is added here.
Also runs an in-browser overflow check before screenshotting.
"""
import sys, os, importlib, asyncio
from playwright.async_api import async_playwright

HTML_DIR = os.path.dirname(os.path.abspath(__file__))

def wrap(inner, tag):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="graphics.css"></head>
<body><div class="page">{inner}</div>
<div class="footerline"></div><div class="footertag">{tag}</div></body></html>"""

async def render_all(specs):
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        page = await browser.new_page(viewport={"width":1080,"height":1920}, device_scale_factor=1)
        for filename, inner, tag in specs:
            html_path = os.path.join(HTML_DIR, "_tmp.html")
            open(html_path,"w").write(wrap(inner, tag))
            await page.goto("file://"+html_path)
            await page.wait_for_timeout(600)  # fonts
            overflow = await page.evaluate("""() => {
                const bad = [];
                // phone safe area: Reels UI crops/overlays these borders
                const SAFE = {left: 105, right: 975, top: 135, bottom: 1785};
                document.querySelectorAll('.page *').forEach(el => {
                  const r = el.getBoundingClientRect();
                  if (r.right > 1082 || r.left < -2 || r.bottom > 1922)
                    bad.push('edge:'+el.className+':'+el.textContent.slice(0,30));
                });
                // every visible text element must sit inside the safe area
                document.querySelectorAll('.page, .page *').forEach(el => {
                  if (el.children.length > 0) return;
                  if (!el.textContent.trim()) return;
                  const r = el.getBoundingClientRect();
                  if (r.left < SAFE.left || r.right > SAFE.right ||
                      r.top < SAFE.top  || r.bottom > SAFE.bottom)
                    bad.push('unsafe:'+el.textContent.trim().slice(0,26)+
                      ` [${Math.round(r.left)},${Math.round(r.top)},${Math.round(r.right)},${Math.round(r.bottom)}]`);
                });
                // SVG text must never sit on top of other SVG text (labels, axis, badges)
                const texts = [...document.querySelectorAll('svg text')].map(el => ({
                  r: el.getBoundingClientRect(), s: el.textContent.slice(0,24)}));
                for (let i = 0; i < texts.length; i++)
                  for (let j = i+1; j < texts.length; j++) {
                    const a = texts[i].r, b = texts[j].r;
                    const ox = Math.min(a.right,b.right) - Math.max(a.left,b.left);
                    const oy = Math.min(a.bottom,b.bottom) - Math.max(a.top,b.top);
                    if (ox > 4 && oy > 4)
                      bad.push(`svg-overlap:'${texts[i].s}' x '${texts[j].s}'`);
                  }
                return bad;
            }""")
            if overflow:
                print(f"OVERFLOW in {filename}: {overflow[:4]}"); continue
            await page.screenshot(path=filename, clip={"x":0,"y":0,"width":1080,"height":1920})
            print("saved", filename)
        await browser.close()
        try: os.remove(os.path.join(HTML_DIR,"_tmp.html"))
        except FileNotFoundError: pass

def run(spec_module):
    mod = importlib.import_module(spec_module)
    asyncio.run(render_all(mod.SPECS))

if __name__ == "__main__":
    sys.path.insert(0, HTML_DIR)
    run(sys.argv[1])
