# SongForge — Multilingual Lyrics Lab

**Current release: v8.0** — improved deterministic multilingual lyric generation, stronger rhyme-family support, and a structured Mandarin romance-satire song form with rap verses, choir call-and-response, an emotional bridge, and a comic outro.

SongForge is a free, static, browser-based **lyrics-only** generator for original lyrics in one or multiple languages, with genre and mood controls and optional parody mode. It does not generate music, audio, vocals, or beats.

## What’s new in v8

- **Structured Mandarin romance satire:** a complete song arc with spoken intro, rhythmic verses, rising pre-chorus, big chorus with choir responses, emotional bridge, final chorus variation, and comic outro.
- **Topic-aware Chinese lines:** the selected topic is woven into the lyrics rather than leaving the song entirely generic.
- **Intentional hook repetition:** chorus and call-and-response repeats are preserved while accidental duplicate lines are checked.
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

Simplified Chinese (中文) has dedicated Mandarin phrase banks, rap resources, and localized comedy themes. The **Romance satire** parody form is more structured than a generic template: it combines conversational Mandarin, escalating relationship jokes, rhythmic rap passages, a choir-backed hook, a sincere emotional bridge, and a final comic turn. The selected topic is inserted into relevant lines. This specialized form is a quality benchmark for further improvements; it does not mean every language or parody category currently has the same degree of structure.

Other languages and categories use curated phrase banks and may need more editing for naturalness, rhyme, cultural fit, or idiomatic expression. Always review multilingual lyrics before publishing.

## Features

- **Engine v8:** dictionary-backed rhyme-family detection and stronger AABB/ABAB end-rhyme support
- Structured Mandarin romance-satire song form with spoken intro, rhythmic verses, rising pre-chorus, choir call-and-response, emotional bridge, final chorus variation, and comic outro
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
