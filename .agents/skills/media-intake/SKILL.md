---
name: media-intake
description: Finds, downloads, and transcribes fitness/bodybuilding source videos into raw transcripts for the knowledge base — YouTube search via API, audio download via yt-dlp, local transcription via faster-whisper. Use when the user wants to add a new video/source/transcript to the knowledge base, asks to find videos on a peak-week/prep/training topic, or hands over an audio/video file to transcribe into Program Design/.
---

# Media Intake

Turns source videos into cited knowledge-base transcripts — **with a human
curation gate before anything enters the repo.** The value of this knowledge
base is that every claim traces to a hand-picked source; do not bulk-ingest.

## Pipeline

### 1. Education-targeted search (default — works, tested)

    python3 .agents/skills/media-intake/scripts/edu_search.py "topic" 15

Four-layer targeting:
- **Subtopic matrix**: big topics are decomposed into specific subtopics
  (built-in for "contest prep"; generic split otherwise) so queries don't
  return the average of everything
- **Channel-first**: also searches within every registry channel
  (`references/channels.md` + `channels.json` — curated educational
  channels; add/verify with `scripts/resolve_channels.py`, and never trust
  a lookalike channel with tiny subs)
- **Vlog down-ranking**: titles matching full-day-of-eating / what-I-eat /
  day-in-the-life / challenge patterns are scored ×0.15; Shorts (<2 min)
  are dropped
- **Quality-weighted score**: like:view ratio instead of raw views, ×4 for
  registry channels, ×2 for educational titles (science/evidence/guide/
  myths/...), ×1.3 for ≥10 min

Output tags: `R` registry channel, `E` educational title, `V` vlog pattern.
API key lives at `.config/youtube-api-key` (git-ignored — never print or
commit it).

Cross-check the ranked list against `knowledge/08-source-map.md` and the
`*Source:*` lines of relevant knowledge files — mark candidates that
duplicate sources already in the KB.

Fallback for exploring a completely unknown area: `scripts/deep_search.py`
(pure popularity ranking) — use only to discover NEW channels worth vetting
into the registry, not as the primary funnel.

### 2. Fetch transcripts for the top 10–15 (primary path — no audio needed)

    python3 .agents/skills/media-intake/scripts/fetch_transcript.py VIDEO_ID_OR_URL OUT.txt

Pulls YouTube's auto-generated captions directly (via
`youtube-transcript-api`) and collapses the scrolling-duplicate artifacts.
This works even where media downloads are bot-blocked. Expect noise in
intro/music sections — the distiller reads loosely anyway; if a transcript
is garbled beyond use (rare), fall back to local transcription (step 4).
**Batch note:** YouTube rate-limits after ~14 rapid fetches — sleep ~20 s
between fetches when doing a full 10–15 video batch.

### 3. Summarize + recommend (LLM work, per candidate)

For each fetched transcript, read it (long ones: skim by section) and compare
against the relevant knowledge files. Produce a decision table for the user:

| # | Video | Channel | Stats | ~What it says (2–3 lines) | Recommendation |
|---|---|---|---|---|---|

Recommendation options: **ADD — fills gap** (topic/angle not in KB),
**ADD — new source on known topic** (strengthens or contradicts existing
claims → possible new contradiction entry), **SKIP — duplicate** (already
covered), **SKIP — low quality** (bro-science without substance, off-topic,
mostly vlog). Read the actual Protocols & Numbers tables when judging
coverage — do not assume from titles. Also note each video's notable
numbers/protocols/quotes inline so the user can judge without re-reading.

**The user makes the final add/skip decision.** Never file anything before
they confirm.

### 4. Fallback: transcribe audio locally (works, tested)

Only if captions are unavailable or unusable. First try audio download:

    yt-dlp -q -x --audio-format wav -o "NAME.%(ext)s" URL
    # client fallbacks if blocked: --extractor-args "youtube:player_client=tv"
    #                          or  --extractor-args "youtube:player_client=android_vr"

`yt-dlp` is at `~/Library/Python/3.9/bin/yt-dlp`; static `ffmpeg` is at
`.config/bin/ffmpeg` — export
`PATH="<repo>/.config/bin:$HOME/Library/Python/3.9/bin:$PATH"` first.
Known issue: some networks 403 every yt-dlp client. Fallbacks: (a) user's
`cookies.txt`; (b) user supplies the audio/video file directly. Surface
the blocker — don't retry forever.

Then transcribe locally:

    .agents/skills/media-intake/scripts/transcribe.sh INPUT.wav OUT.txt [base|small|medium]

`base` is fast and adequate for fitness talking-heads; `small` if the first
pass garbles key terms.

### 5. File it (only after user confirms the source is worth adding)

- Muscle-specific → `Program Design/<bodypart>/<next N>.txt`;
  peak week/prep → `Program Design/Peak Week/transcript<next N>.txt`;
  general → `Program Design/transcript<next N>.txt` (use `ls -v`, never renumber).
- Add a row to the right table in `knowledge/08-source-map.md` (topic,
  what it feeds) and note the citation tag the file will carry.
- Tell the user the file is staged and that `knowledge-distiller` (or a
  manual distill pass) is the next step.

## Rules

- Never enter a source into `Program Design/` without explicit user
  confirmation of that specific video.
- Do not edit existing transcripts; do not renumber files.
- Keep downloads and temp audio out of the repo tree (use /tmp).
- Website sources: save the URL into a `websiteN.txt` link file in the
  same folder, as done for Peak Week `[W#]`.
