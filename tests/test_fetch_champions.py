"""
Tests for scripts/fetch_champions.py, with a pretend Riot server, so they
check our own rules (reading mains from logs, matching names, file names,
not downloading twice) without touching the network.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import fetch_champions as fc  # noqa: E402

CHAMPS = {"data": {
    "Yuumi": {"name": "Yuumi", "image": {"full": "Yuumi.png"}},
    "Lulu": {"name": "Lulu", "image": {"full": "Lulu.png"}},
    "MonkeyKing": {"name": "Wukong", "image": {"full": "MonkeyKing.png"}},
    "Kaisa": {"name": "Kai'Sa", "image": {"full": "Kaisa.png"}},
}}


class FetchTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "_logs").mkdir()
        (self.repo / "_logs" / "wr.md").write_text(
            "---\ntitle: WR\nseasons:\n  - season: 23\n    mains: [Yuumi, Lulu, Wukong, Kai'Sa, Notachamp]\n"
            "  - season: 22\n    mains: [Yuumi]\n---\n")
        self.calls = []

        def fake_get(url):
            self.calls.append(url)
            if url.endswith("versions.json"):
                return json.dumps(["99.1.1", "99.1.0"]).encode(), "application/json"
            if url.endswith("champion.json"):
                return json.dumps(CHAMPS).encode(), "application/json"
            return b"\x89PNGfake", "image/png"

        self._real = (fc.REPO, fc.OUT, fc.get)
        fc.REPO, fc.OUT, fc.get = self.repo, self.repo / "assets/images/champions", fake_get

    def tearDown(self):
        fc.REPO, fc.OUT, fc.get = self._real
        self.tmp.cleanup()

    def test_reads_mains_once_each(self):
        self.assertEqual(fc.wanted_mains(self.repo), ["Yuumi", "Lulu", "Wukong", "Kai'Sa", "Notachamp"])

    def test_reads_champions_from_stats_tiles_and_sessions(self):
        (self.repo / "_logs" / "wr.md").write_text(
            "---\nprofile:\n  signature:\n    - {champion: Lulu, games: 5}\nseasons:\n  - season: 23\n"
            "    champion_stats:\n      - champion: Milio\n        games: 2\n---\nchampion: NotInFrontMatter\n")
        (self.repo / "_entries").mkdir()
        (self.repo / "_entries" / "s.txt").write_text(
            "---\nmatches:\n  - result: win\n    champion: \"Cho'Gath\"\n    kda: [1, 2, 3]\n---\nhi\n")
        self.assertEqual(fc.wanted_mains(self.repo), ["Lulu", "Milio", "Cho'Gath"])

    def test_downloads_by_display_name_with_tidy_file_names(self):
        fc.main()
        for f in ["yuumi.png", "lulu.png", "wukong.png", "kaisa.png"]:
            self.assertTrue((fc.OUT / f).exists(), f)
        self.assertIn("https://ddragon.leagueoflegends.com/cdn/99.1.1/img/champion/MonkeyKing.png", self.calls)
        self.assertFalse((fc.OUT / "notachamp.png").exists())

    def test_never_downloads_twice(self):
        fc.main()
        self.calls.clear()
        (self.repo / "_logs" / "wr.md").write_text("---\nseasons:\n  - season: 23\n    mains: [Yuumi, Lulu]\n---\n")
        fc.main()
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
