# SongForge — Multilingual Lyrics Lab

A static, offline-capable songwriting studio for original lyrics in one or multiple languages, with genre and mood controls and optional parody mode.

## Principles

- Static HTML, CSS, JavaScript, and JSON output
- Python is used only at build time
- No database, backend, or Python server
- Browser `localStorage` for drafts, favorites, preferences, and library
- Export/import library backups as JSON
- No mandatory AI API or API keys

## Build

Requires Python 3.10+; no third-party packages are required.

```bash
python build.py
```

The generated site is written to `dist/`. Open `dist/index.html` locally or deploy the contents of `dist/` to a static host. For GitHub Pages, use the included workflow.

## Generator expectations

The offline composer uses original templates and language resources, so it is a template-driven writing aid rather than a large language model. Language coverage and native-level fluency depend on the resources available. Users should review multilingual lyrics for naturalness.

## Features

- Genre, mood, theme, language, and song structure selection
- Single-language and mixed-language lyrics
- Optional original parody/comedy mode
- Editable lyrics and section-level regeneration
- Local library, favorites, search, autosave, and JSON backup/restore
- TXT and Markdown export
- Responsive interface with Unicode support

## Privacy

Songs and settings are stored in the current browser's local storage. They do not automatically sync between browsers or devices. Clear site data only if you are comfortable losing unsaved local content; export a backup first.

## License

Add a license before redistributing the project.
