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
- `knowledge/` — research library feeding scripts. See
  `knowledge/README.md` for folder layout, source-file header format
  (`source:` / `fetched:` / `why:`), and NOTES-section convention.
- `series/` — planned series (cutting-101, form-fix, hypertrophy-101,
  program-design-101, skits). Episode scripts go here once written.
- `scripts/` — internal tooling (Python, stdlib only, no dependencies).

## Writing rules

- Scripts must follow `brand/voice.md`: mechanism -> application structure,
  kilograms only, 60-75s educational = ~150-190 words, skits under ~60
  words, educational content stays clean (no profanity).
- Captions: all lowercase, one CAPS emphasis word, soft DM CTA.

## Tools

- `scripts/youtube_search.py` — YouTube Data API v3 search for video ideas:

  ```
  python scripts\youtube_search.py "query" --max 10
  python scripts\youtube_search.py "query" --order viewCount --json
  ```

  Returns titles, channels, views, likes, engagement %, URLs. Costs ~2
  quota units per run against a 10,000/day limit — batch queries
  deliberately, don't loop.

## Secrets

- `.env` holds `YOUTUBE_API_KEY` and is gitignored. NEVER commit it, never
  paste the key into scripts, docs, or commits. If the key appears in git
  history, it must be rotated (Google Cloud Console).

## Git

- Remote: `origin` -> https://github.com/pingfff/social-media.git
  (public). Default branch: `master`. Commit only when the user asks.
- Treat every file as publishable to a public repo.
