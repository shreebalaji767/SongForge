import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from lyric_engine import (
    avoid_duplicate_lines, build_static_data, end_rhyme_pairs, generate_lyrics, rhyme_key,
)


class LyricEngineTests(unittest.TestCase):
    def test_topic_is_used_in_generated_lyrics(self):
        lyrics = generate_lyrics("neon city dreams", seed=7)
        self.assertIn("neon city dreams", lyrics)
        self.assertIn("[Chorus]", lyrics)

    def test_seed_makes_generation_repeatable(self):
        self.assertEqual(
            generate_lyrics("new beginnings", mood="Hopeful", seed=42),
            generate_lyrics("new beginnings", mood="Hopeful", seed=42),
        )

    def test_parody_generates_lyrics_without_network(self):
        lyrics = generate_lyrics("anime marathon", parody=True, seed=3)
        self.assertIn("[Verse 1]", lyrics)
        self.assertIn("[Outro]", lyrics)

    def test_parody_verses_avoid_repeated_lines(self):
        lyrics = generate_lyrics("romance satire", parody=True, seed=17, verse_lines=8)
        verse_one = lyrics.split("[Verse 1]\n", 1)[1].split("\n\n[Chorus]", 1)[0].splitlines()
        verse_two = lyrics.split("[Verse 2]\n", 1)[1].split("\n\n[Outro]", 1)[0].splitlines()
        chorus = lyrics.split("[Chorus]\n", 1)[1].split("\n\n[Verse 2]", 1)[0].splitlines()
        self.assertEqual(len(verse_one), 8)
        self.assertEqual(len(verse_two), 8)
        self.assertEqual(len(set(verse_one + verse_two)), 16)
        self.assertTrue(set(verse_one + verse_two).isdisjoint(chorus))

    def test_rhyme_helpers_recognize_curated_end_rhymes(self):
        self.assertEqual(rhyme_key("night"), rhyme_key("bright"))
        self.assertEqual(rhyme_key("heart"), rhyme_key("start"))
        self.assertTrue(end_rhyme_pairs([
            "We walk into the night", "We turn the dark to light",
            "A road becomes a start", "A song comes from the heart",
        ]))

    def test_duplicate_repair_keeps_section_labels_and_removes_accidental_repeats(self):
        draft = "[Verse 1]\nA spark becomes a light\nA spark becomes a light\n\n[Chorus]\nA spark becomes a light\n\n[Outro]\nA spark becomes a light"
        repaired = avoid_duplicate_lines(draft, seed=4)
        self.assertEqual(repaired.count("[Verse 1]"), 1)
        self.assertEqual(repaired.count("[Chorus]"), 1)
        self.assertEqual(repaired.count("[Outro]"), 1)
        lines = [line.strip().casefold() for line in repaired.splitlines() if line.strip() and not line.startswith("[")]
        self.assertGreaterEqual(len(set(lines)), 2)

    def test_standard_generation_repairs_duplicate_lines(self):
        lyrics = generate_lyrics("city lights", mood="Hopeful", seed=19, verse_lines=8)
        body = [
            line.strip().casefold()
            for line in lyrics.splitlines()
            if line.strip() and not line.startswith("[")
        ]
        self.assertEqual(len(body), len(set(body)))

    def test_rhyme_scheme_inserts_requested_topic(self):
        lyrics = generate_lyrics("moonlit roads", rhyme_scheme="AABB", seed=5)
        self.assertIn("I turn moonlit roads into a spark tonight", lyrics)
        self.assertIn("We chase that spark until it shines bright", lyrics)

    def test_verse_line_count_is_configurable(self):
        lyrics = generate_lyrics("midnight trains", seed=4, verse_lines=6)
        verse_one = lyrics.split("[Verse 1]\n", 1)[1].split("\n\n[Chorus]", 1)[0]
        verse_two = lyrics.split("[Verse 2]\n", 1)[1].split("\n\n[Outro]", 1)[0]
        self.assertEqual(len(verse_one.splitlines()), 6)
        self.assertEqual(len(verse_two.splitlines()), 6)

    def test_build_writes_static_json_bank(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "lyric_engine.json"
            build_static_data(target)
            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertIn("phrases", data)
            self.assertIn("parodyLines", data)
            self.assertGreaterEqual(data["version"], 7)
            for angle, lines in data["parodyLines"].items():
                self.assertGreaterEqual(len(lines), 32, angle)
                self.assertEqual(len(lines), len(set(lines)), angle)
            self.assertIn("multilingualFandom", data)
            self.assertEqual(len(data["localizedPhrases"]["zh"]), 15)
            self.assertGreaterEqual(len(data["localizedRap"]["zh"]), 16)
            for angle, lines in data["localizedParody"]["zh"].items():
                self.assertGreaterEqual(len(lines), 20, angle)
                self.assertEqual(len(lines), len(set(lines)), angle)
            self.assertIn("rhymeSchemes", data)
            self.assertIn("AABB", data["rhymeSchemes"])
            self.assertIn("ABAB", data["rhymeSchemes"])
            self.assertIn("rhymeDictionary", data)
            self.assertGreaterEqual(len(data["rhymeDictionary"]), 20)



    def test_chinese_generation_uses_native_mandarin_banks(self):
        lyrics = generate_lyrics(
            "深夜外卖", mood="Playful", genre="Rap", parody=True,
            seed=21, verse_lines=8, language="zh",
            parody_angle="Romance satire",
        )
        self.assertIn("深夜外卖", generate_lyrics("深夜外卖", seed=21, language="zh"))
        self.assertIn("[Chorus]", lyrics)
        self.assertIn("，", lyrics)
        nonempty_lines = [line for line in lyrics.splitlines() if line.strip()]
        self.assertEqual(len(set(nonempty_lines)), len(nonempty_lines))
        verse_one = lyrics.split("[Verse 1]\n", 1)[1].split("\n\n[Chorus]", 1)[0]
        verse_two = lyrics.split("[Verse 2]\n", 1)[1].split("\n\n[Outro]", 1)[0]
        self.assertEqual(len(verse_one.splitlines()), 8)
        self.assertEqual(len(verse_two.splitlines()), 8)

    def test_chinese_cli_flag_writes_utf8_lyrics(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "chinese" / "song.txt"
            subprocess.run(
                [
                    sys.executable, str(root / "lyric_engine.py"),
                    "--topic", "夏夜", "--language", "zh", "--genre", "Rap",
                    "--seed", "8", "--output", str(target),
                ],
                cwd=root, check=True, capture_output=True, text=True,
            )
            lyric = target.read_text(encoding="utf-8")
            self.assertIn("夏夜", lyric)
            self.assertIn("，", lyric)

    def test_unknown_options_fall_back_and_line_count_is_clamped(self):
        lyrics = generate_lyrics(
            "quiet orbit", mood="Not a real mood", rhyme_scheme="unknown",
            seed=11, verse_lines=1,
        )
        verse_one = lyrics.split("[Verse 1]\n", 1)[1].split("\n\n[Chorus]", 1)[0]
        self.assertEqual(len(verse_one.splitlines()), 2)
        self.assertIn("quiet orbit", lyrics)

        long_lyrics = generate_lyrics("quiet orbit", seed=11, verse_lines=99)
        long_verse = long_lyrics.split("[Verse 1]\n", 1)[1].split("\n\n[Chorus]", 1)[0]
        self.assertEqual(len(long_verse.splitlines()), 8)

    def test_generated_engine_contains_every_browser_data_bank(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "content" / "lyric_engine.json"
            build_static_data(target)
            data = json.loads(target.read_text(encoding="utf-8"))
        for key in (
            "phrases", "parodyLines", "multilingualFandom", "arcs",
            "rhymeSchemes", "rhymeDictionary",
        ):
            self.assertIsInstance(data.get(key), dict)
            self.assertTrue(data[key], key)


    def test_cli_creates_missing_output_directories(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "nested" / "draft.txt"
            subprocess.run(
                [
                    sys.executable, str(root / "lyric_engine.py"),
                    "--topic", "quiet orbit", "--seed", "5",
                    "--output", str(target),
                ],
                cwd=root, check=True, capture_output=True, text=True,
            )
            self.assertTrue(target.is_file())
            self.assertIn("quiet orbit", target.read_text(encoding="utf-8"))

    def test_build_produces_complete_pages_artifact(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run(
            [sys.executable, str(root / "build.py")],
            cwd=root, check=False, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("local HTML/JS references", result.stdout)
        for relative in (
            "index.html", "static/app.js", "static/style.css",
            "content/catalog.json", "content/lyric_engine.json",
            "manifest.webmanifest", "sw.js", ".nojekyll",
        ):
            self.assertTrue((root / "dist" / relative).is_file(), relative)


if __name__ == "__main__":
    unittest.main()
