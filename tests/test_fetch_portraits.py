"""
Tests for scripts/fetch_portraits.py, with a pretend wiki, so they check our
own rules (which logs ask for a portrait, how a wiki page becomes a picture,
file names, refusing non-pictures, not downloading twice) without the network.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import fetch_portraits as fp  # noqa: E402


class PortraitTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        logs = self.repo / "_logs"
        logs.mkdir()
        (logs / "disco.md").write_text(
            "---\ntitle: Disco\ncharacter:\n  name: Harry\n"
            "  portrait_page: https://discoelysium.fandom.com/wiki/Harrier_Du_Bois\n---\n")
        (logs / "ff.md").write_text(
            "---\ntitle: FF\ncharacter:\n  name:\n  portrait_page:\n  portrait_url: \"https://img.example.com/me.jpg\"\n---\n")
        (logs / "empty.md").write_text("---\ntitle: Empty\ncharacter:\n  name:\n  portrait_page:\n  portrait_url:\n---\n")
        (logs / "unsafe.md").write_text("---\ntitle: U\ncharacter:\n  portrait_url: http://img.example.com/x.png\n---\n")
        self.calls = []

        def fake_get(url):
            self.calls.append(url)
            if "api.php" in url:
                pages = {"1": {"original": {"source": "https://static.wikia.example/harry.png"}}}
                return json.dumps({"query": {"pages": pages}}).encode(), "application/json"
            if url.endswith(".png"):
                return b"\x89PNGfake", "image/png"
            if url.endswith(".jpg"):
                return b"\xff\xd8fake", "image/jpeg; charset=binary"
            return b"<html>", "text/html"

        self._old = (fp.REPO, fp.OUT, fp.get)
        fp.REPO, fp.OUT, fp.get = self.repo, self.repo / "assets/images/characters", fake_get

    def tearDown(self):
        fp.REPO, fp.OUT, fp.get = self._old
        self.tmp.cleanup()

    def test_only_https_links_count(self):
        slugs = [w[0] for w in fp.wanted(self.repo)]
        self.assertEqual(slugs, ["disco", "ff"])  # empty and http-only are skipped

    def test_wiki_page_and_direct_link_are_saved_once(self):
        fp.main()
        out = self.repo / "assets/images/characters"
        self.assertEqual((out / "disco.png").read_bytes(), b"\x89PNGfake")
        self.assertEqual((out / "ff.jpg").read_bytes(), b"\xff\xd8fake")
        self.assertIn("https://discoelysium.fandom.com/api.php?", self.calls[0])
        self.assertIn("titles=Harrier_Du_Bois", self.calls[0])
        n = len(self.calls)
        fp.main()
        self.assertEqual(len(self.calls), n, "a portrait already saved is never fetched again")

    def test_wikipedia_uses_w_api(self):
        fp.picture_from_wiki_page("https://en.wikipedia.org/wiki/Cloud_Strife")
        self.assertTrue(self.calls[0].startswith("https://en.wikipedia.org/w/api.php?"))

    def test_non_picture_is_not_saved(self):
        (self.repo / "_logs" / "ff.md").write_text(
            "---\ntitle: FF\ncharacter:\n  portrait_url: https://img.example.com/page\n---\n")
        (self.repo / "_logs" / "disco.md").unlink()
        fp.main()
        self.assertFalse(any((self.repo / "assets/images/characters").glob("ff.*")))


if __name__ == "__main__":
    unittest.main()
