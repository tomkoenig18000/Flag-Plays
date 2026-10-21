# Flag Plays

Single-file PWA for calling flag football plays from an iPad in the huddle. Same shape as the sibling `flag-ref` project.

## Layout
- `src/app.html` — the app (HTML + CSS + one script). `{{VERSION}}` and `{{PLAYS}}` are filled in by `build.py`.
- `src/plays.json` — 50 plays: `id`, `name`, `cat` (short/mid/long/goal/trick), `tags` (fav/run/bunch), optional `mark` (the G/K/J letters on the goal-line plays). Categories and tags come from Tom's own sheet; the in-app "Edit tags" overrides live in storage, not here.
- `build.py` → `docs/` (index.html, manifest, sw.js, icons). `docs/plays/NN.webp` are committed; regenerate with `tools/pdf_to_images.py`.

## Release
Bump `src/VERSION`, `python3 build.py`, commit, push `main` (Pages serves `docs/`).

## Rules that shape the code
- Big targets (≥ 48px) and few taps: cold hands, gloves, huddle time. Logging is CALL IT → tap result → Done.
- All user data is in IndexedDB (`main`, `ink`) with a localStorage mirror of `main`; nothing leaves the device. Backup is export/import JSON.
- Ink strokes are stored normalised to image width, so they survive any screen size. Temp layer is never persisted.
- Play names and notes are user text: always through `esc()`.
