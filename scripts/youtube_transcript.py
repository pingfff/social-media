"""Fetch YouTube video transcripts.

Usage:
    python youtube_transcript.py <url-or-video-id>            # print transcript
    python youtube_transcript.py <url-or-video-id> --save     # archive to knowledge/raw/transcripts/
    python youtube_transcript.py <url-or-video-id> --save --why "feeds cutting-101"

Requires youtube-transcript-api (pip install -r requirements.txt).
Transcript fetch does NOT use API quota; --save uses 1 unit for metadata.
--save archives to knowledge/raw/transcripts/ with metrics (views, likes,
duration) in the header — raw files are never read back; distill a clean
companion in knowledge/clean/transcripts/ instead.
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    sys.exit("ERROR: youtube-transcript-api not installed. Run: pip install -r requirements.txt")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def parse_video_id(arg):
    if re.fullmatch(r"[\w-]{11}", arg):
        return arg
    parsed = urllib.parse.urlparse(arg)
    if parsed.hostname in ("www.youtube.com", "youtube.com", "m.youtube.com"):
        if parsed.path == "/watch":
            return urllib.parse.parse_qs(parsed.query)["v"][0]
        m = re.search(r"/(shorts|embed|live)/([\w-]{11})", parsed.path)
        if m:
            return m.group(2)
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")[:11]
    sys.exit(f"ERROR: cannot parse video ID from: {arg}")


def get_metadata(video_id):
    """1 API quota unit. Returns dict: title, channel, views, likes, duration."""
    env_path = os.path.join(ROOT, ".env")
    key = None
    if os.path.exists(env_path):
        with open(env_path, encoding="utf-8") as f:
            for line in f:
                if line.startswith("YOUTUBE_API_KEY="):
                    key = line.split("=", 1)[1].strip()
    empty = {"title": None, "channel": None, "views": 0, "likes": 0, "duration": ""}
    if not key:
        return empty
    url = (
        "https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id="
        + video_id + "&key=" + key
    )
    try:
        req = urllib.request.Request(url, headers={"Accept-Encoding": "gzip"})
        import gzip
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
        items = json.loads(data).get("items", [])
        if items:
            s = items[0]["snippet"]
            st = items[0].get("statistics", {})
            return {
                "title": s["title"],
                "channel": s["channelTitle"],
                "views": int(st.get("viewCount", 0)),
                "likes": int(st.get("likeCount", 0)),
                "duration": items[0].get("contentDetails", {}).get("duration", ""),
            }
    except Exception:
        pass
    return empty


def sanitize(name):
    return re.sub(r'[<>:"/\\|?*]', "", name).strip().rstrip(".")


def main():
    p = argparse.ArgumentParser(description="Fetch a YouTube transcript")
    p.add_argument("video", help="URL or 11-char video ID")
    p.add_argument("--save", action="store_true", help="archive to knowledge/raw/transcripts/")
    p.add_argument("--why", default="", help="which series/episode this feeds (for the header)")
    p.add_argument("--lang", default="en", help="preferred language (default en)")
    p.add_argument("--json", action="store_true", help="output JSON with metadata + text")
    args = p.parse_args()

    video_id = parse_video_id(args.video)

    api = YouTubeTranscriptApi()
    fetched = api.fetch(video_id, languages=[args.lang])
    text = " ".join(s.text for s in fetched)
    text = re.sub(r"\s+", " ", text).strip()

    meta = get_metadata(video_id)
    title, channel = meta["title"], meta["channel"]

    if args.json:
        print(json.dumps({
            "id": video_id,
            "title": title,
            "channel": channel,
            "views": meta["views"],
            "likes": meta["likes"],
            "duration": meta["duration"],
            "snippets": len(fetched),
            "words": len(text.split()),
            "transcript": text,
        }, indent=2))
        return

    if not args.save:
        if title:
            print(f"# {title} — {channel}")
            print(f"# https://www.youtube.com/watch?v={video_id}")
            print(f"# {meta['views']:,} views | {meta['likes']:,} likes | {meta['duration']}")
            print(f"# {len(text.split())} words, {len(fetched)} snippets")
            print()
        print(text)
        return

    if not title:
        title = video_id
        channel = "unknown"
    folder = sanitize(f"{channel} - {title}")[:120]
    out_dir = os.path.join(ROOT, "knowledge", "raw", "transcripts", folder)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "transcript.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"source: https://www.youtube.com/watch?v={video_id}\n")
        f.write(f"fetched: {__import__('datetime').date.today().isoformat()}\n")
        f.write(f"why: {args.why or '<fill in which series/episode this feeds>'}\n")
        f.write(f"channel: {channel}\n")
        f.write(f"title: {title}\n")
        f.write(f"views: {meta['views']}\n")
        f.write(f"likes: {meta['likes']}\n")
        f.write(f"duration: {meta['duration']}\n\n")
        f.write(text + "\n")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
