#!/usr/bin/env python3
"""Education-targeted deep search (v2).
Usage: edu_search.py "big topic" [top_n]

Strategy:
  1. Decompose the topic into subtopics (built-in matrices or generic split)
  2. Per subtopic: open searches with educational intent phrases
  3. Plus one topic search per registry channel (channel-first)
  4. Enrich with statistics; down-rank vlog patterns; prefer substantive length
  5. Quality-weighted ranking: registry bonus, edu-keyword bonus, like:view
     ratio -- NOT raw views
Output: rank | videoId | [tags] | channel | views | likes | dur | score | title
Tags: R=registry channel, E=educational title, V=vlog-pattern (down-ranked)
"""
import sys, json, urllib.request, urllib.parse, os, re, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
KEY = open(os.path.join(ROOT, ".config/youtube-api-key")).read().strip()
CHANNELS = json.load(open(os.path.join(HERE, "..", "references", "channels.json")))

MATRICES = {
    "contest prep": [
        "contest prep diet deficit setup science",
        "rate of fat loss cutting evidence based",
        "refeeds diet breaks research bodybuilding",
        "metabolic adaptation contest prep evidence",
        "protein intake cutting deficit evidence based",
        "hunger management dieting adherence science",
        "cardio fat loss contest prep how much",
        "contest prep timeline how long guide",
    ],
}

EDU = ["science", "evidence based", "explained", "research", "guide", "how to"]
VLOG_RE = re.compile(r"full day of eating|what i eat|day in the life|fdoe|vlog|"
                     r"morning routine|tried .* diet|100 hours|eating challenge", re.I)
EDU_RE = re.compile(r"science|evidence|research|explained|guide|ultimate guide|"
                    r"myth|mistakes|everything you|complete|101|how to", re.I)

def get(url):
    with urllib.request.urlopen(url) as r: return json.load(r)

def search(q, n=15, channel=None):
    url = ("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video"
           f"&maxResults={n}&q={urllib.parse.quote(q)}&key={KEY}")
    if channel: url += f"&channelId={channel}"
    time.sleep(0.4)
    return [it["id"]["videoId"] for it in get(url).get("items", [])]

topic = sys.argv[1].lower()
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 15

queries = next((m for k, m in MATRICES.items() if k in topic), [f"{sys.argv[1]} {w}" for w in ("science", "evidence based", "explained guide")])
ids = []
for q in queries: ids += search(q)
for ch in CHANNELS.values(): ids += search(f"{sys.argv[1]}", channel=ch["id"], n=10)
ids = list(dict.fromkeys(ids))
if not ids: print("(no results)"); sys.exit(0)

rows = []
for i in range(0, len(ids), 50):
    v = get("https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails,snippet"
            f"&id={','.join(ids[i:i+50])}&key={KEY}")
    reg_ids = {c["id"] for c in CHANNELS.values()}
    for it in v["items"]:
        st = it.get("statistics", {})
        views = int(st.get("viewCount", 0)); likes = int(st.get("likeCount", 0))
        m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", it["contentDetails"]["duration"])
        h, mi, s = (int(x or 0) for x in m.groups()); mins = h*60+mi+s/60
        title = it["snippet"]["title"]; cid = it["snippet"]["channelId"]
        tags = []
        registry = cid in reg_ids
        edu = bool(EDU_RE.search(title)); vlog = bool(VLOG_RE.search(title))
        if registry: tags.append("R")
        if edu: tags.append("E")
        if vlog: tags.append("V")
        like_ratio = likes/max(views, 1)
        score = (views/1000) * (1 + like_ratio*20)
        if registry: score *= 4
        if edu: score *= 2
        if vlog: score *= 0.15
        if mins < 2: score = 0          # Shorts: hard drop
        elif mins < 6: score *= 0.3
        if mins >= 10: score *= 1.3
        rows.append({"id": it["id"], "ch": it["snippet"]["channelTitle"], "views": views,
                     "likes": likes, "dur": (f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"),
                     "title": title[:70], "tags": "".join(tags) or "-", "score": score})

rows.sort(key=lambda r: -r["score"])
for n, r in enumerate(rows[:TOP], 1):
    print(f'{n}. {r["id"]} | [{r["tags"]}] | {r["ch"]} | {r["views"]:,} views | '
          f'{r["likes"]:,} likes | {r["dur"]} | {r["title"]}')
