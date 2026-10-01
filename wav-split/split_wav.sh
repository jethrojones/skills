#!/bin/bash
# Split a multi-channel WAV into per-channel mono WAVs (<name>_mic1.wav, ...).
# Usage: split_wav.sh <input.wav> [output_dir]   (default output: <input dir>/split)
# Created by Claude Fable 5 on 2026-07-04 09:03 PT
set -euo pipefail

IN="${1:?Usage: split_wav.sh <input.wav> [output_dir]}"
[ -f "$IN" ] || { echo "ERROR: file not found: $IN" >&2; exit 1; }

DIR="$(cd "$(dirname "$IN")" && pwd)"
BASE="$(basename "$IN")"
NAME="${BASE%.*}"
OUT="${2:-$DIR/split}"
mkdir -p "$OUT"

CH="$(ffprobe -v error -select_streams a:0 -show_entries stream=channels -of csv=p=0 "$IN")"
[ -n "$CH" ] && [ "$CH" -ge 1 ] || { echo "ERROR: could not read channel count" >&2; exit 1; }
echo "Input: $BASE — $CH channel(s)"

if [ "$CH" -eq 1 ]; then
  cp "$IN" "$OUT/${NAME}_mic1.wav"
  echo "Mono source; copied to ${NAME}_mic1.wav"
  exit 0
fi

FILTER="[0:a]channelsplit=channel_layout=${CH}c"
MAPS=()
for i in $(seq 1 "$CH"); do FILTER+="[c$i]"; done
for i in $(seq 1 "$CH"); do MAPS+=(-map "[c$i]" "$OUT/${NAME}_mic${i}.wav"); done

ffmpeg -hide_banner -loglevel error -y -i "$IN" -filter_complex "$FILTER" "${MAPS[@]}"

echo "Done:"
for i in $(seq 1 "$CH"); do ls -lh "$OUT/${NAME}_mic${i}.wav" | awk '{print "  " $NF " (" $5 ")"}'; done
