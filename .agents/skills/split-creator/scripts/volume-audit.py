#!/usr/bin/env python3
"""Weekly volume audit for split-creator programs (SKILL.md Step 3, stage 3).

Checks per-muscle weekly hard-set totals against the volume landmarks
distilled in knowledge/02-programming-variables.md + muscle files 09-13.
Landmark data lives in references/volume-landmarks.json next to this
script — edit it only from cited knowledge-file content.

Usage:
  python3 .agents/skills/split-creator/scripts/volume-audit.py audit.json
  cat audit.json | python3 .agents/skills/split-creator/scripts/volume-audit.py -
  python3 .agents/skills/split-creator/scripts/volume-audit.py --landmarks other.json audit.json

Input JSON maps muscle -> list of hard sets per session, or -> a single
integer weekly total (warm-up sets never count [T4]):

  {
    "chest": [7, 3, 4],
    "back": [3, 10, 3],
    "biceps": 6,
    "side_delts": [3, 3, 3]
  }

Output: a markdown table for the program's weekly-volume-audit section plus
warnings (at/below retention, outside the band, over caution lines, single
sessions above the per-session plateau). Exit codes: 0 = audited, 2 = bad
input.
"""
import json
import os
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LANDMARKS = os.path.normpath(
    os.path.join(SKILL_DIR, os.pardir, "references", "volume-landmarks.json")
)

ALIASES = {
    "lats": "back",
    "quad": "quads",
    "hamstring": "hamstrings",
    "bicep": "biceps",
    "tricep": "triceps",
    "side delt": "side_delts",
    "side delts": "side_delts",
    "side_delt": "side_delts",
    "sidedelts": "side_delts",
    "rear delt": "rear_delts",
    "rear delts": "rear_delts",
    "rear_delt": "rear_delts",
    "front delt": "front_delts",
    "front delts": "front_delts",
    "front_delt": "front_delts",
    "trap": "traps",
    "abdominals": "abs",
}


def die(msg):
    sys.stderr.write("error: %s\n" % msg)
    sys.exit(2)


def read_input(path):
    if path == "-":
        try:
            return json.load(sys.stdin)
        except ValueError as exc:
            die("invalid JSON on stdin: %s" % exc)
    try:
        with open(path) as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        die("cannot read %s: %s" % (path, exc))


def normalize(muscle, value):
    """Return (weekly_total, sessions_list_or_None)."""
    if isinstance(value, bool):
        die("%s: expected integer or list of integers, got boolean" % muscle)
    if isinstance(value, int):
        if value < 0:
            die("%s: negative set count" % muscle)
        return value, None
    if isinstance(value, list) and all(
        isinstance(v, int) and not isinstance(v, bool) for v in value
    ):
        if any(v < 0 for v in value):
            die("%s: negative set count" % muscle)
        return sum(value), value
    die(
        "%s: expected integer (weekly total) or list of integers "
        "(sets per session)" % muscle
    )


def main():
    args = sys.argv[1:]
    landmarks_path = DEFAULT_LANDMARKS
    positional = []
    iterator = iter(args)
    for arg in iterator:
        if arg in ("-h", "--help"):
            print(__doc__)
            return
        if arg == "--landmarks":
            try:
                landmarks_path = next(iterator)
            except StopIteration:
                die("--landmarks requires a path")
        else:
            positional.append(arg)
    if len(positional) != 1:
        die("usage: volume-audit.py [--landmarks FILE] <audit.json | ->")

    data_in = read_input(positional[0])
    if not isinstance(data_in, dict):
        die("input must be a JSON object of muscle -> sets")

    try:
        with open(landmarks_path) as fh:
            lm = json.load(fh)
    except (OSError, ValueError) as exc:
        die("cannot read landmarks %s: %s" % (landmarks_path, exc))
    muscles = lm["muscles"]

    rows, warnings = [], []
    for raw_key in sorted(data_in):
        key = ALIASES.get(raw_key, raw_key)
        if key not in muscles:
            die(
                "unknown muscle %r; valid keys: %s"
                % (raw_key, ", ".join(sorted(muscles)))
            )
        entry = muscles[key]
        total, sessions = normalize(key, data_in[raw_key])
        lo, hi = entry["min"], entry["max"]
        retention = entry.get("retention", 3)
        generic = entry.get("generic", False)

        if total == 0:
            if entry.get("mode") == "mostly_indirect":
                verdict = "no direct volume — typically covered indirectly"
            else:
                verdict = "no direct volume"
        elif total <= retention:
            verdict = "at/below retention landmark (~%d) — maintenance only" % retention
            if entry.get("mode") != "mostly_indirect":
                warnings.append(
                    "%s: %d sets/wk is at or below the retention landmark (~%d) — "
                    "atrophy risk for a growth goal [T22 via knowledge/02]"
                    % (key, total, retention)
                )
        elif total < lo:
            verdict = "maintenance / minimal-growth zone (below %d–%d band)" % (lo, hi)
        elif total <= hi:
            verdict = "✅ growth band"
        else:
            verdict = "above %d–%d band — trial territory" % (lo, hi)
            warnings.append(
                "%s: %d sets/wk exceeds the %d–%d band — high-volume trial "
                "territory; justify it (contradiction #4: T6 allows 20–30 for "
                "small muscles, T22 says ROI is minuscule above 10–12)"
                % (key, total, lo, hi)
            )

        caution = entry.get("caution_over")
        if caution and total > caution:
            verdict += " 🚨 exceeds caution line (>%d)" % caution
            warnings.append(
                "%s: %d sets/wk exceeds the caution threshold >%d — %s [%s]"
                % (key, total, caution, entry.get("notes", ""), entry.get("source", ""))
            )

        if sessions:
            biggest = max(sessions)
            cap = lm["meta"]["session_caps"]["per_muscle_per_session_warn_over"]
            if biggest > cap:
                warnings.append(
                    "%s: %d sets in a single session exceeds the ~6–8 per-session "
                    "quality plateau [T4, T22] (~7 defensible when the muscle "
                    "spans regions, e.g. back/6 pull day) — redistribute or count "
                    "overlap honestly" % (key, biggest)
                )

        band = "%d–%d%s" % (lo, hi, " (generic)" if generic else "")
        sess = "/".join(str(s) for s in sessions) if sessions else "—"
        rows.append((key, total, sess, band, verdict, entry.get("notes", "")))

    print("## Weekly volume audit (generated by volume-audit.py)\n")
    print("| Muscle | Weekly sets | Per session | Landmark | Verdict |")
    print("|---|---|---|---|---|")
    for key, total, sess, band, verdict, _notes in rows:
        print("| %s | %s | %s | %s | %s |" % (key.replace("_", " "), total, sess, band, verdict))
    print()
    for key, total, sess, band, verdict, notes in rows:
        if notes:
            print("- **%s:** %s" % (key.replace("_", " "), notes))
    if warnings:
        print("\n**Warnings**\n")
        for warning in warnings:
            print("- %s" % warning)
    else:
        print("\nNo landmark warnings.")
    print(
        "\n*Counts are hard working sets only (warm-ups never count [T4]). "
        "Muscles marked (generic) have no muscle-specific landmark in the "
        "knowledge files — the 10–20 default from knowledge/02 was applied. "
        "Reconcile against the program's session tables before shipping.*"
    )


if __name__ == "__main__":
    main()
