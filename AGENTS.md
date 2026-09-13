# Social Media Content Repo

Content operations for a fitness creator (natural bodybuilding, Classic
Physique). This repo produces scripts, research, and ideas for Instagram
Reels and YouTube — it is not a software project. Python scripts here are
internal tooling, not a product.

## Repo structure

- `brand/` — published content, organized by format
  (`Educational Workouts/`, `Peak Week 101/`, `Skits/`, `Talking Head/`).
  One folder per video: `transcript.txt`, `caption.txt`.
- `brand/voice.md` — CANONICAL voice profile. Read it before writing any
  script, caption, or skit. Persona facts, pacing budget (~150 words/min),
  hook patterns, skit formats, running gags, and CTA rules live there.
- `knowledge/` — research library feeding scripts, split into `raw/`
  (write-once archive: full transcripts + metrics, pasted
  articles/threads) and `clean/` (the ONLY reading surface: distilled
  files with YAML frontmatter + fixed sections; `clean/topics/` holds
  per-topic synthesis — read it first for a topic). NEVER read files
  under `knowledge/raw/` — also blocked by `opencode.json` read
  permission. Distill raw -> clean once, at fetch time, from
  in-session content. See `knowledge/README.md` for the pipeline,
  clean-file schema, and source-header format.
- `series/` — planned series (cutting-101, form-fix, hypertrophy-101,
  program-design-101, skits). Episode scripts go here once written.
- `scripts/` — internal tooling (Python). `youtube_search.py` is stdlib
  only; `youtube_transcript.py` needs `youtube-transcript-api`
  (`pip install -r requirements.txt`).

## Writing rules

- Scripts must follow `brand/voice.md`: mechanism -> application structure,
  kilograms only, 60-75s educational = ~150-190 words, skits under ~60
  words, educational content stays clean (no profanity).
- Captions: all lowercase, one CAPS emphasis word, soft DM CTA.

## Creating a series (e.g. "how to diet")

1. Read `brand/voice.md` — always first.
2. Read `knowledge/clean/topics/<topic>.md` (see `knowledge/README.md`
   reading path). If the topic file is missing or thin, run the
   `@youtube-research` agent to fill the library BEFORE planning.
3. Write `series/<name>/plan.md` — the episode map for user approval:
   series title + positioning, episode list (per episode: working
   title, one-line hook in the creator's voice, mechanism ->
   application beats, knowledge sources cited via clean-file paths).
4. WAIT for user approval of the plan.
5. On approval, write episode scripts into `series/<name>/` one at a
   time (or in requested batches), following voice rules and citing
   knowledge sources. One folder or file per episode, plus caption.

## Tools

- `@youtube-research` subagent (`.opencode/agents/youtube-research.md`) —
  the structured way to research YouTube: give it a topic, it runs
  batched queries (quota-capped, max 6 script runs per task), archives
  raw transcripts + metrics, distills clean transcript files (claims +
  craft), and maintains the `clean/topics/<topic>.md` synthesis. The
  library is the deliverable — it returns only a short confirmation.
  Prefer it over running the scripts ad hoc in the main session.
- `scripts/youtube_search.py` — YouTube Data API v3 search for video ideas:

  ```
  python scripts\youtube_search.py "query" --max 10
  python scripts\youtube_search.py "query" --order viewCount --json
  ```

  Returns titles, channels, views, likes, engagement %, URLs. Costs ~2
  quota units per run against a 10,000/day limit — batch queries
  deliberately, don't loop.
- `scripts/youtube_transcript.py` — fetch a video's transcript (manual
  or auto-generated captions), no quota cost:

  ```
  python scripts\youtube_transcript.py <url-or-id>            # print
  python scripts\youtube_transcript.py <url-or-id> --save --why "feeds cutting-101"
  ```

  `--save` archives to `knowledge/raw/transcripts/` with the standard
  header (costs 1 quota unit for metadata). Transcript fetching itself
  needs no API key. Distill a clean companion in
  `knowledge/clean/transcripts/` per the schema in
  `knowledge/README.md`.

## Secrets

- `.env` holds `YOUTUBE_API_KEY` and is gitignored. NEVER commit it, never
  paste the key into scripts, docs, or commits. If the key appears in git
  history, it must be rotated (Google Cloud Console).

## Git

- Remote: `origin` -> https://github.com/pingfff/social-media.git
  (public). Default branch: `master`. Commit only when the user asks.
- Treat every file as publishable to a public repo.
