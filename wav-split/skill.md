---
name: wav-split
description: Split a multi-channel podcast recorder WAV (Zoom PodTrak POD000xx.WAV files) into per-mic mono WAV files. Use when the user says "split this WAV", points at a POD000xx.WAV, or drops files in the "WAV Split DO NOT DELETE" folder.
---

# WAV Split — per-mic tracks from a recorder file

The user's podcast recorder produces one multi-channel `POD000xx.WAV`. Split it into one mono WAV per mic so each speaker gets a clean track for editing (Descript, etc.).

## How
Run the bundled script (ffmpeg must be installed; it is):

```bash
<skills-dir>/wav-split/split_wav.sh "/path/to/POD00005.WAV" [output_dir]
```

- Default output dir: a `split/` folder next to the source file (matches the existing recordings-folder convention).
- Output naming: `<basename>_mic1.wav`, `<basename>_mic2.wav`, … one mono 48 kHz file per channel, channel count auto-detected with ffprobe.
- A stereo source still yields two files (L→mic1, R→mic2) — that is intended for 2-mic sessions.

## Process
1. Verify the source file exists and `ffprobe` sees its channel count; report duration + channels.
2. Run the script. Don't re-split a file whose `_mic1.wav` already exists in the output dir unless asked — warn instead.
3. Report the output paths and sizes when done.

---
Created by Claude Fable 5 on 2026-07-04 09:03 PT
