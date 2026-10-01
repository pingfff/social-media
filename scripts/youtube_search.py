"""Search YouTube for video ideas, ranked by performance.

Usage:
    python youtube_search.py "query" [--max 10] [--order relevance|viewCount|date]
    python youtube_search.py "query" --json

Requires YOUTUBE_API_KEY in .env at project root.
Costs 2 quota units per run (1 search.list + 1 videos.list).
"""

import argparse
import html
import json
import os
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://www.googleapis.com/youtube/v3"


def load_api_key():
    env_path = os.path.join(ROOT, ".env")
    if not os.path.exists(env_path):
        sys.exit("ERROR: .env not found at project root. Add YOUTUBE_API_KEY=... to it.")
    with open(env_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("YOUTUBE_API_KEY="):
                return line.split("=", 1)[1].strip()
    sys.exit("ERROR: YOUTUBE_API_KEY not found in .env")


def request(endpoint, params):
    params = dict(params, key=load_api_key())
    url = f"{API}/{endpoint}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
    with urllib.request.urlopen(req) as resp:
        data = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            import gzip
            data = gzip.decompress(data)
        return json.loads(data)


def iso8601_duration_to_seconds(d):
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    if not m:
        return 0
    h, mi, s = (int(x) if x else 0 for x in m.groups())
    return h * 3600 + mi * 60 + s


def search(query, max_results=10, order="relevance", duration=None, uploaded_after=None):
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": min(max_results, 50),
        "order": order,
    }
    if duration:
        params["videoDuration"] = duration
    if uploaded_after:
        params["publishedAfter"] = uploaded_after
    data = request("search", params)
    ids = [item["id"]["videoId"] for item in data.get("items", [])]
    if not ids:
        return []

    stats = {}
    details = request("videos", {"part": "statistics,contentDetails,snippet", "id": ",".join(ids)})
    for v in details.get("items", []):
        stats[v["id"]] = {
            "views": int(v["statistics"].get("viewCount", 0)),
            "likes": int(v["statistics"].get("likeCount", 0)),
            "comments": int(v["statistics"].get("commentCount", 0)),
            "duration": v["contentDetails"].get("duration", ""),
        }

    results = []
    for item in data["items"]:
        vid = item["id"]["videoId"]
        s = item["snippet"]
        st = stats.get(vid, {})
        views = st.get("views", 0)
        likes = st.get("likes", 0)
        results.append({
            "id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "title": html.unescape(s["title"]),
            "channel": s["channelTitle"],
            "published": s["publishedAt"][:10],
            "views": views,
            "likes": likes,
            "engagement_pct": round(likes / views * 100, 2) if views else 0,
            "duration": st.get("duration", ""),
        })
    return results


def main():
    p = argparse.ArgumentParser(description="Search YouTube for video ideas")
    p.add_argument("query", help="search query")
    p.add_argument("--max", type=int, default=10, help="max results (default 10)")
    p.add_argument("--order", default="relevance", choices=["relevance", "viewCount", "date", "rating"])
    p.add_argument("--duration", choices=["short", "medium", "long"], help="short <4min, medium 4-20min, long >20min")
    p.add_argument("--after", help="publishedAfter, e.g. 2025-01-01T00:00:00Z")
    p.add_argument("--json", action="store_true", help="output JSON")
    args = p.parse_args()

    results = search(args.query, args.max, args.order, args.duration, args.after)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    if not results:
        print("No results.")
        return

    results.sort(key=lambda r: r["views"], reverse=True)
    for i, r in enumerate(results, 1):
        print(f"{i:2}. {r['title']}")
        print(f"    {r['channel']} | {r['published']} | {r['duration']}")
        print(f"    {r['views']:,} views | {r['likes']:,} likes | {r['engagement_pct']}% engagement")
        print(f"    {r['url']}")


if __name__ == "__main__":
    main()
