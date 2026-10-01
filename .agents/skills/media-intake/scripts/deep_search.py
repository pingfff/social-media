#!/usr/bin/env python3
"""Popularity-ranked deep search for source videos.
Usage: deep_search.py "query" [top_n]
Searches YouTube (relevance + date cross-check), enriches with statistics,
ranks by a popularity score, and prints the top N with stats.
Output line: rank | videoId | channel | views | likes | comments | duration | title
"""
import sys, json, urllib.request, urllib.parse, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
KEY = open(os.path.join(ROOT, ".config/youtube-api-key")).read().strip()
q = sys.argv[1]
TOP = int(sys.argv[2]) if len(sys.argv) > 2 else 15

def get(url):
    with urllib.request.urlopen(url) as r: return json.load(r)

def search(order, n=25):
    d = get("https://www.googleapis.com/youtube/v3/search?part=snippet&type=video"
           f"&maxResults={n}&order={order}&q={urllib.parse.quote(q)}&key={KEY}")
    return [it["id"]["videoId"] for it in d.get("items", [])]

ids = list(dict.fromkeys(search("relevance") + search("viewCount")))
if not ids: print("(no results)"); sys.exit(0)

rows = []
for i in range(0, len(ids), 50):
    v = get("https://www.googleapis.com/youtube/v3/videos?part=statistics,contentDetails,snippet"
            f"&id={','.join(ids[i:i+50])}&key={KEY}")
    for it in v["items"]:
        st = it.get("statistics", {})
        views = int(st.get("viewCount", 0))
        likes = int(st.get("likeCount", 0))
        comments = int(st.get("commentCount", 0))
        m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", it["contentDetails"]["duration"])
        h, mi, s = (int(x or 0) for x in m.groups())
        mins = h*60 + mi + s/60
        # popularity score: views dominate; likes/comments as engagement ratios
        score = views * (1 + min(likes/max(views,1), 0.05)*4 + min(comments/max(views,1), 0.01)*4)
        rows.append({"id": it["id"], "ch": it["snippet"]["channelTitle"], "title": it["snippet"]["title"],
                     "views": views, "likes": likes, "comments": comments, "mins": mins,
                     "dur": (f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"), "score": score})

rows.sort(key=lambda r: -r["score"])
# prefer substantive length for a knowledge base: deprioritize <4 min clips
rows.sort(key=lambda r: (0 if r["mins"] >= 4 else 1, -r["score"]))
for n, r in enumerate(rows[:TOP], 1):
    print(f'{n}. {r["id"]} | {r["ch"]} | {r["views"]:,} views | {r["likes"]:,} likes | '
          f'{r["comments"]:,} comments | {r["dur"]} | {r["title"][:75]}')
