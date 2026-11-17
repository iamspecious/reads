"""
Tests for scripts/discover_books.py, with a pretend Bluesky feed: which
opening posts start a new book, which are left alone, and how the log
file comes out. No network.
"""

import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import discover_books as db  # noqa: E402

NOW = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
HANDLE = "booksbyspec.bsky.social"


def item(rkey, text, created="2026-11-18T09:15:00.000Z", reply=False, repost=False):
    record = {"text": text, "createdAt": created}
    if reply:
        record["reply"] = {"parent": {"uri": "at://x/app.bsky.feed.post/p"}}
    it = {"post": {"uri": f"at://did:plc:me/app.bsky.feed.post/{rkey}", "record": record}}
    if repost:
        it["reason"] = {"$type": "app.bsky.feed.defs#reasonRepost"}
    return it


class DiscoverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        (self.repo / "_logs").mkdir()
        (self.repo / "_config.yml").write_text("timezone: Europe/Berlin\nbluesky: booksbyspec.bsky.social\n")
        (self.repo / "_logs" / "a-court-of-silver-flames.md").write_text(
            '---\ntitle: A Court of Silver Flames\ncreator: Sarah J. Maas\ntype: book\nstatus: finished\n'
            'bluesky_thread: https://bsky.app/profile/booksbyspec.bsky.social/post/oldroot\n---\n')
        self.feed = []
        self._real = db.imp.xrpc
        db.imp.xrpc = lambda method, **p: {"feed": self.feed}

    def tearDown(self):
        db.imp.xrpc = self._real
        self.tmp.cleanup()

    def test_starts_a_new_book_with_tidy_author(self):
        self.feed = [item("newroot", "My thoughts as I go through A Court of Splintered Harmony by Sarah J Mass")]
        done = db.discover(self.repo, HANDLE, now=NOW)
        self.assertEqual(len(done), 1)
        text = (self.repo / "_logs" / "a-court-of-splintered-harmony.md").read_text()
        self.assertIn('title: "A Court of Splintered Harmony"', text)
        self.assertIn('creator: "Sarah J. Maas"', text)  # matched to the author already on the site
        self.assertIn("status: reading", text)
        self.assertIn("started: 2026-11-18", text)
        self.assertIn("bluesky_thread: https://bsky.app/profile/booksbyspec.bsky.social/post/newroot", text)

    def test_other_wordings_of_the_opener(self):
        # The real Splintered Harmony opener said "read through", not "go through".
        for i, line in enumerate([
            "My thoughts as I read through A Court of Splintered Harmony by Sarah J Maas",
            "My thoughts as I make my way through A Court of Splintered Harmony by Sarah J Maas",
        ]):
            m = db.OPENER_RE.match(line)
            self.assertTrue(m, line)
            self.assertEqual(m.group("title"), "A Court of Splintered Harmony")
            self.assertEqual(m.group("author"), "Sarah J Maas")
        self.assertIsNone(db.OPENER_RE.match("My thoughts as I finished A Court of Silver Flames by Sarah J Maas"))

    def test_ignores_everything_else(self):
        self.feed = [
            item("oldroot", "My thoughts as I go through A Court of Silver Flames by Sarah J Mass"),  # already linked
            item("chat", "Chapter 1: wow"),                                                          # not an opener
            item("rep", "My thoughts as I go through Fake by Someone", reply=True),                  # a reply
            item("rp", "My thoughts as I go through Theirs by Someone", repost=True),                # a repost
            item("old", "My thoughts as I go through Ancient by Someone", created="2026-10-01T00:00:00Z"),  # too old
        ]
        self.assertEqual(db.discover(self.repo, HANDLE, now=NOW), [])
        self.assertEqual(sorted(p.name for p in (self.repo / "_logs").iterdir()), ["a-court-of-silver-flames.md"])

    def test_new_author_kept_as_written_and_title_with_by(self):
        self.feed = [item("x1", "my thoughts as I go through Stand by Me by Stephen King.")]
        db.discover(self.repo, HANDLE, now=NOW)
        text = (self.repo / "_logs" / "stand-by-me.md").read_text()
        self.assertIn('title: "Stand by Me"', text)
        self.assertIn('creator: "Stephen King"', text)

    def test_links_an_existing_log_started_on_new(self):
        (self.repo / "_logs" / "piranesi.md").write_text(
            '---\ntitle: "Piranesi"\ncreator: "Susanna Clarke"\ntype: book\nstatus: reading\nstarted: 2026-11-18\n---\nnote\n')
        self.feed = [item("p1", "My thoughts as I go through Piranesi by Susanna Clarke")]
        db.discover(self.repo, HANDLE, now=NOW)
        text = (self.repo / "_logs" / "piranesi.md").read_text()
        self.assertIn("bluesky_thread: https://bsky.app/profile/booksbyspec.bsky.social/post/p1\n---\nnote\n", text)

    def test_dry_run_writes_nothing(self):
        self.feed = [item("newroot", "My thoughts as I go through A Court of Splintered Harmony by Sarah J Maas")]
        self.assertEqual(len(db.discover(self.repo, HANDLE, now=NOW, dry_run=True)), 1)
        self.assertFalse((self.repo / "_logs" / "a-court-of-splintered-harmony.md").exists())


if __name__ == "__main__":
    unittest.main()
