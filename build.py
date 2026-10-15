#!/usr/bin/env python3
"""Build the static site; never starts a server."""
from pathlib import Path
import shutil
ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)
shutil.copy2(ROOT / "index.html", DIST / "index.html")
shutil.copytree(ROOT / "static", DIST / "static")
shutil.copytree(ROOT / "content", DIST / "content")
print("Built SongForge into", DIST)
