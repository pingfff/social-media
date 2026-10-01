#!/usr/bin/env python3
"""Resolve educational channel names to YouTube channelIds (cached in channels.json).
Usage: resolve_channels.py "Channel Name" ["Another Name" ...]"""
import sys, json, urllib.request, urllib.parse, os

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "references", "channels.json")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
KEY = open(os.path.join(ROOT, ".config/youtube-api-key")).read().strip()

cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}

def get(url):
    with urllib.request.urlopen(url) as r: return json.load(r)

for name in sys.argv[1:]:
    if name in cache:
        print(f"{name} -> {cache[name]['id']} (cached)"); continue
    d = get("https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&maxResults=1"
            f"&q={urllib.parse.quote(name)}&key={KEY}")
    items = d.get("items", [])
    if not items:
        print(f"{name} -> NOT FOUND"); continue
    it = items[0]
    cid = it["snippet"]["channelId"]
    ch = get(f"https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id={cid}&key={KEY}")
    s = ch["items"][0]
    cache[name] = {"id": cid, "title": s["snippet"]["title"],
                   "subs": int(s["statistics"].get("subscriberCount", 0))}
    print(f"{name} -> {s['snippet']['title']} ({cache[name]['subs']:,} subs)")

os.makedirs(os.path.dirname(CACHE), exist_ok=True)
json.dump(cache, open(CACHE, "w"), indent=1)
