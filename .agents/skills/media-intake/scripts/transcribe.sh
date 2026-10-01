#!/bin/bash
# Transcribe a media file to a raw transcript (no punctuation expected — matches
# the existing Program Design/ transcript style).
# Usage: transcribe.sh <input audio/video> <output txt> [model]
# Models: base (fast, default) | small (better) | medium (slow, best)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
export PATH="$ROOT/.config/bin:$PATH"
INPUT="$1"; OUTPUT="$2"; MODEL="${3:-base}"
[ -f "$INPUT" ] || { echo "input not found: $INPUT"; exit 1; }
TMP="$(mktemp -d)/audio.wav"
ffmpeg -y -loglevel error -i "$INPUT" -ar 16000 -ac 1 "$TMP"
python3 - "$TMP" "$OUTPUT" "$MODEL" <<'EOF'
import sys
from faster_whisper import WhisperModel
audio, out, model = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel(model, device="cpu", compute_type="int8")
segs, _ = m.transcribe(audio)
with open(out, "w") as f:
    f.write(" ".join(s.text.strip() for s in segs) + "\n")
print("wrote", out)
EOF
