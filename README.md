# SongForge — Multilingual Lyrics Lab

A static, browser-based **lyrics-only** generator for original lyrics in one or multiple languages, with genre and mood controls and optional parody mode. It does not generate music, audio, vocals, or beats.

## Principles

- Static HTML, CSS, JavaScript, and JSON output
- Python is used only at build time
- No database, backend, or Python server
- Browser `localStorage` for drafts, favorites, preferences, and library
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
- TXT and Markdown export
- Favorites-only library filter and one-click song duplication
- Responsive interface with Unicode support

## Privacy

Songs and settings are stored in the current browser's local storage. They do not automatically sync between browsers or devices. Clear site data only if you are comfortable losing unsaved local content; export a backup first.

## License

Add a license before redistributing the project.
