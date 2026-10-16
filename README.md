# SongForge — Multilingual Lyrics Lab

**Current release: v10.0** — structured Mandarin parody forms plus curated eight-line rap verses with deliberate end-sound families, varied cadence, and more topic-specific punchlines.

SongForge is a free, static, browser-based **lyrics-only** generator for original lyrics in one or multiple languages, with genre and mood controls and optional parody mode. It does not generate music, audio, vocals, or beats.

## What’s new in v10

- **Mandarin flow upgrade:** curated eight-line verses for all five parody categories use planned end-sound groupings, varied line lengths, and clearer punchline setups.
- **Full song arcs remain:** each category keeps its own hook, choir responses, bridge, final-chorus variation, and punchline outro.
- **Topic-aware intros:** the selected topic is incorporated into each structured Mandarin form; intentional hook repetition is preserved while accidental repeats are checked.
- **Offline-first, deterministic generation:** no AI model or paid generation service is used.
- **Validation:** Python unit tests, JavaScript syntax checks, and the static-site build run in the GitHub Actions workflow.

## Installable PWA, responsive UI, and branding

SongForge includes an install control for supported browsers, a web app manifest, an offline service worker, a custom SVG logo and favicon, and responsive layouts for phones, tablets, and desktop screens. On iPhone/iPad, use Share → Add to Home Screen; browsers that do not expose an install prompt can show their own browser-menu installation option. PWA installation requires HTTPS (or localhost for development) and browser support.

## Python lyric engine (no AI)

Python owns the deterministic lyric templates and can generate a complete draft locally. The build step writes those templates to `content/lyric_engine.json`; the static browser app uses that JSON to compose interactive lyrics without running a Python server.

Generate lyrics locally from a terminal:

```bash
python lyric_engine.py --topic "neon city dreams" --mood Hopeful --genre Pop --rhyme-scheme AABB --verse-lines 6
python lyric_engine.py --topic "anime marathon" --parody --seed 7 --output song.txt
python lyric_engine.py --topic "深夜外卖" --language zh --genre Rap --seed 7 --output chinese-song.txt
python lyric_engine.py --topic "恋爱脑" --language zh --parody --parody-angle "Romance satire" --verse-lines 8
python lyric_engine.py --build-data --output content/lyric_engine.json
python -m unittest discover -s tests -v
python build.py
```

The browser studio includes a **Rhyme pattern** selector (Free verse, AABB, and ABAB), a **Lines per verse** setting (2, 4, 6, or 8), and a **Local rhyme finder**. The finder searches the Python-generated offline rhyme dictionary and offers clickable word suggestions without network access. The Python CLI supports the same rhyme patterns and configurable verse lengths.

This is template-based generation, not an AI model. Python is needed for local CLI use and building/testing the static site; deployed browser interactions use the generated JSON and JavaScript.

## Free and offline-friendly

- No AI model, paid API, API key, subscription, or server required
- Installable as a Progressive Web App (PWA) on supported browsers
- The app shell is cached so it can reopen offline after the first successful visit
- Saved lyrics and drafts remain in this browser's local storage; use Backup to move them to another device
- Google Fonts are optional styling only; system font fallbacks are used if offline

## Principles

- Static HTML, CSS, JavaScript, and JSON output
- Python is used for the local CLI generator, build-time lyric-data generation, and tests
- No database, backend, or Python server
- Browser `localStorage` for drafts, favorites, preferences, and library
- Service worker caches the static app shell for offline reopening
- Export/import library backups as JSON
- No mandatory AI API or API keys
- Lyrics only: no audio, music, vocals, or beat generation

## Build

Requires Python 3.10+; no third-party packages are required.

```bash
python build.py
```

The generated site is written to `dist/`. Deploy the contents of `dist/` to a static host. Browsers generally block local JSON fetches from `file://`, so preview through a static host rather than opening the HTML file directly. For GitHub Pages, enable Pages in **Repository Settings → Pages** and set the build/deployment source to **GitHub Actions**. The included workflow builds and deploys the `dist/` folder on pushes to `main`.

## Generator expectations and lyric quality

The offline composer uses curated phrase banks and deterministic templates, so it is a template-driven writing aid rather than a large language model. Output quality depends on the language, topic, genre, mood, and parody angle; generated lyrics should be reviewed and edited before publishing.

Simplified Chinese (中文) has dedicated Mandarin phrase banks, rap resources, and localized comedy themes. All five Mandarin parody categories now have dedicated full-song structures. Romance satire combines conversational relationship jokes and a sincere emotional bridge; fandom satire riffs on late-night bingeing; everyday-life chaos turns procrastination into a comic arc; internet-meme satire uses chat and screen-time jokes; and genre exaggeration treats minor mishaps like cinematic events. Each form includes topic-aware setup, two category-specific verses, a choir-backed hook, a bridge, a final-hook variation, and an outro.

Other languages and categories use curated phrase banks and may need more editing for naturalness, rhyme, cultural fit, or idiomatic expression. Always review multilingual lyrics before publishing.

## Features

- **Engine v10:** dictionary-backed rhyme-family detection and stronger AABB/ABAB end-rhyme support
- Five structured Mandarin parody song forms with curated cadence-aware rap verses, spoken intros, rising pre-choruses, choir call-and-response, bridges, final-chorus variations, and comic outros
- Topic-aware Chinese lyric template and intentional chorus/hook repetition
- Duplicate-repair checks designed to avoid removing intentional hook repeats
- Lyric Coach rhyme scan checks curated dictionary families before falling back to suffix heuristics
- Genre, mood, theme, language, and song-structure selection
- Single-language and mixed-language lyrics
- Optional original parody/comedy mode, including Mandarin comedy categories
- Simplified Chinese songwriting with mood-aware phrases, Chinese rap resources, and localized humor
- Editable lyrics with topic-, mood-, and genre-aware templates
- Live Lyric Coach checks section structure, line count, repeated lines, rough singability, possible English end-rhyme groups, and estimated syllable spread
- Coach feedback updates while editing and ignores intentional repeats inside chorus/hook sections
- Heuristic score is guidance only; it does not judge artistic quality or validate translations
- Automatic draft recovery in the same browser
- Keyboard shortcuts: `Ctrl/Cmd + S` to save and `Ctrl/Cmd + Enter` to generate
- Local library, favorites, search, autosave, and JSON backup/restore
- Copy a chorus or hook section by itself
- Undo and redo recent lyric edits in the current editing session
- Clean lyric whitespace and section spacing without changing lyric wording
- TXT and Markdown export
- Favorites-only library filter and one-click song duplication
- Responsive interface with Unicode support

## Privacy

Songs and settings are stored in the current browser's local storage. They do not automatically sync between browsers or devices. Clear site data only if you are comfortable losing unsaved local content; export a backup first.

## License

Add a license before redistributing the project.
