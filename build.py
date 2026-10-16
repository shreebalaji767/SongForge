#!/usr/bin/env python3
"""Build and validate the static SongForge site; never starts a server."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
import json
import re
import shutil
from lyric_engine import build_static_data

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
REQUIRED = [
    ROOT / "index.html",
    ROOT / "static" / "app.js",
    ROOT / "static" / "style.css",
    ROOT / "static" / "logo.svg",
    ROOT / "static" / "favicon.svg",
    ROOT / "static" / "icon.svg",
    ROOT / "content" / "catalog.json",
    ROOT / "manifest.webmanifest",
    ROOT / "sw.js",
]
for path in REQUIRED:
    if not path.is_file():
        raise SystemExit(f"Required static asset is missing: {path.relative_to(ROOT)}")


class AssetParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.assets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        for attr in ("src", "href"):
            value = attrs.get(attr)
            if value:
                self.assets.append(value)


html_path = ROOT / "index.html"
html = html_path.read_text(encoding="utf-8")
parser = AssetParser()
parser.feed(html)
parser.close()
for reference in parser.assets:
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc or reference.startswith(("#", "data:")):
        continue
    target = (ROOT / parsed.path).resolve()
    if not target.is_relative_to(ROOT) or not target.exists():
        raise SystemExit(f"Broken local HTML asset reference: {reference}")
js = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
missing_ids = sorted(set(re.findall(r"\$\(['\"]([^'\"]+)['\"]\)", js)) - parser.ids - {"lyricCoach"})
if missing_ids:
    raise SystemExit("JavaScript references missing HTML IDs: " + ", ".join(missing_ids))

manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
if not manifest.get("name") or not manifest.get("start_url") or not manifest.get("icons"):
    raise SystemExit("Web app manifest is missing required fields.")

with (ROOT / "content" / "catalog.json").open(encoding="utf-8") as catalog_file:
    catalog = json.load(catalog_file)
if not catalog.get("languages") or not catalog.get("genres") or not catalog.get("moods"):
    raise SystemExit("Catalog must contain languages, genres, and moods.")

# Generate the browser's free, offline lyric bank with Python at build time.
engine_path = ROOT / "content" / "lyric_engine.json"
build_static_data(engine_path)
engine = json.loads(engine_path.read_text(encoding="utf-8"))
for key in ("phrases", "parodyLines", "multilingualFandom", "arcs", "rhymeSchemes", "rhymeDictionary"):
    if not isinstance(engine.get(key), dict) or not engine[key]:
        raise SystemExit(f"Generated lyric engine is missing valid data: {key}")

if engine.get("version", 0) < 9:
    raise SystemExit("Generated lyric engine is outdated; expected version 9 or newer.")
if not engine.get("localizedPhrases", {}).get("zh") or not engine.get("localizedParody", {}).get("zh") or not engine.get("localizedRap", {}).get("zh"):
    raise SystemExit("Generated lyric engine is missing native Mandarin songwriting banks.")
required_zh_forms = {"Romance satire", "Anime / fandom obsession", "Everyday-life chaos", "Internet meme energy", "Genre exaggeration"}
if not required_zh_forms.issubset(engine.get("localizedSongForms", {}).get("zh", {})):
    raise SystemExit("One or more structured Mandarin parody forms are missing from generated data.")
if len(engine["localizedPhrases"]["zh"]) < 15 or len(engine["localizedRap"]["zh"]) < 16:
    raise SystemExit("Mandarin mood or rap bank is incomplete.")
for angle, lines in engine["localizedParody"]["zh"].items():
    if len(lines) < 20 or len(set(lines)) != len(lines):
        raise SystemExit(f"Mandarin parody bank must contain at least 20 unique lines: {angle}")
for angle, lines in engine["parodyLines"].items():
    if len(lines) < 32 or len(set(lines)) != len(lines):
        raise SystemExit(f"Parody bank must contain at least 32 unique lines: {angle}")

# Confirm the service worker only pre-caches assets that will be deployed.
service_worker = (ROOT / "sw.js").read_text(encoding="utf-8")
match = re.search(r"const SHELL=\[(.*?)\];", service_worker, re.S)
if not match:
    raise SystemExit("Service worker shell asset list was not found.")
for asset in re.findall(r"'([^']+)'", match.group(1)):
    local = asset.removeprefix("./")
    target = ROOT / ("index.html" if local in ("", ".") else local)
    if not target.exists():
        raise SystemExit(f"Service worker pre-cache asset is missing: {asset}")

if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)
shutil.copy2(ROOT / "index.html", DIST / "index.html")
shutil.copy2(ROOT / "manifest.webmanifest", DIST / "manifest.webmanifest")
shutil.copy2(ROOT / "sw.js", DIST / "sw.js")
shutil.copytree(ROOT / "static", DIST / "static")
shutil.copytree(ROOT / "content", DIST / "content")
(DIST / ".nojekyll").write_text("", encoding="utf-8")
# Check the actual deployment artifact, not only the source tree.
for relative in ("index.html", "static/app.js", "static/style.css", "content/catalog.json", "content/lyric_engine.json", "manifest.webmanifest", "sw.js", ".nojekyll"):
    if not (DIST / relative).is_file():
        raise SystemExit(f"Build output is incomplete: {relative}")
print(f"Validated {len(catalog['languages'])} languages, local HTML/JS references, service-worker assets, and generated lyric data; built: {DIST}")
