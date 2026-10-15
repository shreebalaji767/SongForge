#!/usr/bin/env python3
"""Build and validate the static SongForge site; never starts a server."""
from pathlib import Path
import json
import shutil
from lyric_engine import build_static_data

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
REQUIRED = [
    ROOT / "index.html",
    ROOT / "static" / "app.js",
    ROOT / "static" / "style.css",
    ROOT / "content" / "catalog.json",
    ROOT / "manifest.webmanifest",
    ROOT / "sw.js",
]
for path in REQUIRED:
    if not path.is_file():
        raise SystemExit(f"Required static asset is missing: {path.relative_to(ROOT)}")

with (ROOT / "content" / "catalog.json").open(encoding="utf-8") as catalog_file:
    catalog = json.load(catalog_file)
if not catalog.get("languages") or not catalog.get("genres") or not catalog.get("moods"):
    raise SystemExit("Catalog must contain languages, genres, and moods.")

# Generate the browser's free, offline lyric bank with Python at build time.
build_static_data(ROOT / "content" / "lyric_engine.json")

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)
shutil.copy2(ROOT / "index.html", DIST / "index.html")
shutil.copy2(ROOT / "manifest.webmanifest", DIST / "manifest.webmanifest")
shutil.copy2(ROOT / "sw.js", DIST / "sw.js")
shutil.copytree(ROOT / "static", DIST / "static")
shutil.copytree(ROOT / "content", DIST / "content")
print(f"Validated catalog ({len(catalog['languages'])} languages), generated Python lyric bank, and built static site: {DIST}")
