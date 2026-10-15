import json
import tempfile
import unittest
from pathlib import Path

from lyric_engine import build_static_data, generate_lyrics


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

    def test_rhyme_scheme_inserts_requested_topic(self):
        lyrics = generate_lyrics("moonlit roads", rhyme_scheme="AABB", seed=5)
        self.assertIn("I turn moonlit roads into a spark tonight", lyrics)
        self.assertIn("We chase that spark until it shines bright", lyrics)

    def test_verse_line_count_is_configurable(self):
        lyrics = generate_lyrics("midnight trains", seed=4, verse_lines=6)
        verse_one = lyrics.split("[Verse 1]\\n", 1)[1].split("\\n\\n[Chorus]", 1)[0]
        verse_two = lyrics.split("[Verse 2]\\n", 1)[1].split("\\n\\n[Outro]", 1)[0]
        self.assertEqual(len(verse_one.splitlines()), 6)
        self.assertEqual(len(verse_two.splitlines()), 6)

    def test_build_writes_static_json_bank(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "lyric_engine.json"
            build_static_data(target)
            data = json.loads(target.read_text(encoding="utf-8"))
            self.assertIn("phrases", data)
            self.assertIn("parodyLines", data)
            self.assertIn("multilingualFandom", data)
            self.assertIn("rhymeSchemes", data)
            self.assertIn("AABB", data["rhymeSchemes"])
            self.assertIn("ABAB", data["rhymeSchemes"])
            self.assertIn("rhymeDictionary", data)
            self.assertGreaterEqual(len(data["rhymeDictionary"]), 20)


if __name__ == "__main__":
    unittest.main()
