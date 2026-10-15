# SongForge — Multilingual Lyrics Lab

A static, browser-based **lyrics-only** generator for original lyrics in one or multiple languages, with genre and mood controls and optional parody mode. It does not generate music, audio, vocals, or beats.

## Installable PWA, responsive UI, and branding

SongForge includes an install control for supported browsers, a web app manifest, an offline service worker, a custom SVG logo and favicon, and responsive layouts for phones, tablets, and desktop screens. On iPhone/iPad, use Share → Add to Home Screen; browsers that do not expose an install prompt can show their own browser-menu installation option. PWA installation requires HTTPS (or localhost for development) and browser support.

## Python lyric engine (no AI)

Python owns the deterministic lyric templates and can generate a complete draft locally. The build step writes those templates to `content/lyric_engine.json`; the static browser app uses that JSON to compose interactive lyrics without running a Python server.

Generate lyrics locally from a terminal:

```bash
python lyric_engine.py --topic "neon city dreams" --mood Hopeful --genre Pop --rhyme-scheme AABB --verse-lines 6
python lyric_engine.py --topic "anime marathon" --parody --seed 7 --output song.txt
python lyric_engine.py --build-data --output content/lyric_engine.json
python -m unittest discover -s tests -v
python build.py
```

The browser studio includes a **Rhyme pattern** selector (Free verse, AABB, and ABAB), a **Lines per verse** setting (2, 4, 6, or 8), and a **Local rhyme finder**. The finder searches the Python-generated offline rhyme dictionary and offers clickable word suggestions without network access. The Python CLI supports the same rhyme patterns and configurable verse lengths.\n\nThis is template-based generation, not an AI model. Python is needed only for local CLI use and building/testing the static site; deployed browser interactions use the generated JSON and JavaScript.

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

The generated site is written to `dist/`. Deploy the contents of `dist/` to a static host. Browsers generally block local JSON fetches from `file://`, so preview through a static host rather than opening the HTML file directly. For GitHub Pages, enable Pages in **Repository Settings → Pages** and set the build/deployment source to **GitHub Actions**. The included workflow then builds and deploys the `dist/` folder on pushes to `main`.

## Generator expectations

The offline composer uses original templates and language resources, so it is a template-driven writing aid rather than a large language model. It never generates audio, music, vocals, or beats. English output varies with topic, mood, genre, and parody angle; other languages use curated phrase banks and may need more editing for naturalness. Language coverage and native-level fluency depend on the resources available. Users should review multilingual lyrics for naturalness.

## Features

- Genre, mood, theme, language, and song structure selection
- Single-language and mixed-language lyrics
- Optional original parody/comedy mode
- Editable lyrics with topic-, mood-, and genre-aware templates
- Live Lyric Coach checks section structure, line count, repeated lines, rough singability, possible English end-rhyme groups, and estimated syllable spread
- Coach feedback updates while editing and ignores intentional repeats inside chorus/hook sections
- Heuristic score is guidance only; it does not judge artistic quality or validate translations
- Automatic draft recovery in the same browser
- Keyboard shortcuts: `Ctrl/Cmd + S` to save and `Ctrl/Cmd + Enter` to generate
- Local library, favorites, search, autosave, and JSON backup/restore
- Copy a chorus or hook section by itself
- Clean lyric whitespace and section spacing without changing lyric wording
- TXT and Markdown export
- Favorites-only library filter and one-click song duplication
- Responsive interface with Unicode support

## Privacy

Songs and settings are stored in the current browser's local storage. They do not automatically sync between browsers or devices. Clear site data only if you are comfortable losing unsaved local content; export a backup first.

## License

Add a license before redistributing the project.
