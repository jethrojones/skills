---
name: glowforge
description: Design, prepare, and set up laser jobs on a Glowforge via app.glowforge.com — build Glowforge-ready SVGs (text outlined, one path per card, QR codes), engrave metal business cards, generate power/speed test patches, and drive the app through Chrome (upload, place, copy, rotate, set Manual settings). Use for any Glowforge, laser engraving, metal card, or "Print in the app" task. Always stops before the physical button.
---

# Glowforge

Everything here was learned the slow way on the Optimization Doc metal cards (2026-10-01). Follow it and skip the detours.

## Hard rules
- **Never press the physical button. Only press Print in the app if the user said so in that session.** Default: set everything up, stop at "Ready", report.
- A job runs **every** design on the canvas. Before printing, delete or Ignore anything already engraved, and confirm every design sits on a real card (nothing at the bed's 0,0 corner).
- The Glowforge **cannot cut metal**. It only engraves coated metal (anodized/painted). Blanks are 86 × 54 mm (3.386 × 2.126 in), 0.2 mm thick, blue and black.
- Lid open = the camera image is stale. Wait for the lid to close before aligning to cards.

## Part 1 — Make the file (do this in Python, not by hand)
Scripts live in `scripts/` (copy into the project folder; deps: `qrcode fonttools shapely opencv-python-headless` in a venv; fonts from the OpDoc design system `project/fonts/`).
- `make_cards_example.py` — full front/back card generator (86×54 mm, `viewBox 338.6×212.6`, units = 0.01 in).
- `make_test_patch.py` — six labeled swatches, one color per setting group.

Rules for Glowforge-friendly SVGs:
1. **Outline all text** (fontTools `SVGPathPen`); never rely on installed fonts.
2. **Merge each card's art into ONE `<path>`** (`fill-rule=evenodd`). Glowforge imports every `<path>` as a separate object; separate pieces make moving/duplicating a nightmare. One path = one click.
3. Black fill = engraved. Bright metal is what shows, so **QR codes are an engraved bright square with the dark modules knocked out** (normal polarity). Build with shapely: `box.difference(unary_union(modules))` so there are no row seams.
4. **Verify the QR decodes** from the rendered file in physical polarity: `cv2.QRCodeDetector().detectAndDecode(255 - gray)`. (zbarimg segfaults here — don't use it.)
5. Small text: stay ≥ ~11 units tall and prefer SemiBold/Bold. 7 pt Medium came out ragged at 225 LPI.
6. Different settings in one job → give each setting its own **fill color** (Glowforge groups by color).
7. Preview: `magick -density 300 -background white file.svg -flatten file.png`.

## Part 2 — Drive the app (Chrome extension)
Browser selection: two Chrome browsers are connected. Use `switch_browser`; the right one is named **"glowforge"**. Open `https://app.glowforge.com` (a design editor opens; the design title is "back").

Upload: `find` "input type=file (hidden)" → `file_upload` with the SVG path. **The ref changes every time — re-`find` before each upload.** Wait ~10 s for "Processing". New art lands at the bed's top-left (≈0,0).

Coordinates (screenshot frame ~1400×867, can shift to 1372×886 — re-check): ~66 px per inch on the bed; camera shows card edges imprecisely, align to the visible card edge, ±0.05 in is normal. Selection handles sit ~6–10 px outside the art.

Selecting / moving:
- `left_click_drag` on a selected object moves it (small 4–7 px drags work).
- **Marquee select works** when dragged from empty canvas (e.g. from lower-right to upper-left around the art). **Shift-click does not multi-select or deselect.** `cmd+a` selects everything.
- Copy/paste: `cmd+c`, `cmd+v` → copy appears ~0.1 in offset and selected; drag it into place.
- Rotate: drag the rotation handle (above top-center) to the side; it **snaps to exact 90°**. Move the object down onto the bed first — at the top edge the handle is off-screen.
- Delete: select, `Delete`. To clear: `cmd+a`, `Delete`.

Material and settings (blanks aren't in the catalog):
1. Top-left "Unknown Material" → **use uncertified material** → enter thickness `0.008` in (0.2 mm) → Submit.
2. Left panel thumbnail → "enter settings" → **MANUAL**.
3. Speed field: triple_click, type, `Return`. Power field: same. **Lines per inch** is a dropdown (225 → pick **340**). **Passes** is a dropdown (1/2/3).
4. **Leave by clicking another thumbnail or empty canvas. Do NOT click "< back" or the Engrave tab — it discards the manual settings.** Verify each thumbnail shows e.g. `1000/50/1x`.
5. Focus is Auto; it worked on these blanks. If the jig changes height, set Manual with the real height.

Print flow (only if authorized): Print → "Preparing" → Scanning/autofocus → **"Magic time — push the button"**. Stop there; the user presses the physical button. A "Proofgrade not found" amber warning is normal. A "Print done" side panel appears afterwards; Dismiss it.

## Part 3 — Settings log (update after every test)
Blue anodized alloy blanks, 225 LPI at 1000/50 = hazy, partial coating removal; **340 LPI is clearly sharper** (confirmed). The bright "deep" look needs more energy per area (raise power, lower speed, or 2 passes) without blooming the 0.2 mm blank.
- Test patch run 2026-10-01: swatches 1000/50, 1000/60, 1000/70, 1000/80, 800/70, 1000/60×2 at 340 LPI. **Winner: swatch 6 = 1000/60, 2 passes** (brightest, evenly cleared, cleanest label edges; 1–2 hazy, 3–5 bright but mottled).
- **Production: 1000 speed / 60 power / 2 passes / 340 LPI** for fronts and backs on blue blanks; black blanks started at the same settings.

## Typical session order
1. Read your project notes (if any) and the settings log above.
2. Generate/merge SVGs, verify QR, preview PNG.
3. `switch_browser` → open app → clear old art → upload → set material → place/copy/rotate → set Manual settings per color.
4. Screenshot-verify: all art on cards, all thumbnails show settings, no stray art. Report; stop before the button.
5. After the run: ask which test swatch won, update Part 3 and the vault note.

Created by Claude Sonnet 5.5 on 2026-10-01 14:23 PT
