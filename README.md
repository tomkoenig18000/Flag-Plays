# Flag Plays

In-huddle play caller for flag football: 50 plays, filter fast, tap **CALL IT**, log how it went, and mark up the play with Apple Pencil. Installs to the iPad home screen and works fully offline.

## Install (iPad)
1. Open the site in Safari, tap Share, then **Add to Home Screen**.
2. Launch it once with signal so it can save every play image for offline use.
3. Open it from the home-screen icon. Updates arrive by themselves when you launch with signal (a "Reload" toast appears).

## Using it
- **Find a play**: tap a situation (Short / Intermediate / Long / Goal line / Trick), tags (★ Favourite, Run, Bunch), 🔥 Working (plays that worked when you ran them) or Not called yet. **#** jumps straight to a play number. *More* adds formation/concept filters and sort order.
- **Call it**: open a play and tap **▶ CALL IT**, then tap how it went (multi-select), gain, who it went to, down, and a note. Dictate with the 🎤 button or the iPad keyboard's mic key.
- **Draw**: **✏️ Draw** gives a pencil layer. *Temp* marks vanish when you leave the play; *Keep* marks are saved on that play. Palm rejection: once the Pencil is seen, finger touches don't draw (☝︎ turns finger drawing on).
- **Game log** lists this game's calls; tap one to edit. Start a new game from the game name in the top right.
- Swipe left/right on a play, or use ‹ ›, to move through the current filtered list.
- Everything is stored on the iPad. Use **Game name ▾ → Export backup** now and then.

## Developing
- `src/app.html` is the app (one file); `src/plays.json` holds play names, situations and tags; `src/VERSION` is the version shown in the menu and used for the service worker cache.
- `python3 build.py` regenerates `docs/` (served by GitHub Pages).
- `python3 tools/pdf_to_images.py Flag_Football_Plays.pdf` re-renders the play images from the playbook PDF (page N = play N).
