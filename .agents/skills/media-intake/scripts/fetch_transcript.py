#!/usr/bin/env python3
"""Fetch YouTube auto-generated captions directly (no audio download).
Usage: fetch_transcript.py <videoId or URL> <output.txt> [--keep-dupes]
Collapses YouTube's scrolling-duplicate caption artifacts; output is raw
lowercase-ish text matching the house raw/ transcript style."""
import sys, re

def clean(segments):
    out = []
    for s in segments:
        t = s.text.replace("\n", " ").strip()
        if not t or t == "[Music]":
            continue
        # collapse the repeated-phrase scroll artifact: drop a line if it is
        # a substring of (or contains) the previous line's tail
        if out:
            prev = out[-1].lower()
            cur = t.lower()
            if cur in prev or prev in cur:
                out[-1] = t if len(t) > len(out[-1]) else out[-1]
                continue
        out.append(t)
    text = " ".join(out)
    text = re.sub(r"\s+", " ", text).strip()
    return text + "\n"

def vid(arg):
    m = re.search(r"(?:v=|youtu\.be/|shorts/)([\w-]{11})", arg)
    return m.group(1) if m else arg

args = [a for a in sys.argv[1:] if not a.startswith("--")]
keep = "--keep-dupes" in sys.argv
video, output = vid(args[0]), args[1]

from youtube_transcript_api import YouTubeTranscriptApi
try:
    t = YouTubeTranscriptApi().fetch(video)
except Exception as e:
    print(f"FAILED: {str(e)[:160]}"); sys.exit(1)

text = " ".join(s.text for s in t) + "\n" if keep else clean(t)
open(output, "w").write(text)
print(f"wrote {output} ({len(t)} segments, {len(text)} chars)")
