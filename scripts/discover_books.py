#!/usr/bin/env python3
"""
discover_books.py: start a new book's log by itself when Spec opens a new
Bluesky thread for it.

THE MARKER
 Spec opens each reading thread with the same kind of first post:
     My thoughts as I go through A Court of Splintered Harmony by Sarah J Maas
 Only that FIRST post needs the phrase. Everything after it is a reply in
 the thread ("Chapter 1: ...", a GIF, anything), and the normal sync picks
 those up because they're in the thread, whatever they say.

WHAT IT DOES
 1. Looks at Spec's recent posts on Bluesky (only new posts, not replies).
 2. For each one whose first line is "My thoughts as I go through <title>
    by <author>", made in the last 14 days, that no log is linked to yet:
      - if a book log with that title exists but has no thread yet (say,
        Spec started it on /new), it links that log to the thread;
      - otherwise it writes a new log: type book, status reading, started
        on the day of the post, linked to the post as its bluesky_thread.
 3. Then sync_bluesky.py runs as usual and pulls the whole thread in.

WHY ONLY THE LAST 14 DAYS
 So an old opening post can never bring back a book from long ago, for
 example after a log has been renamed or deleted on purpose.

WHY IT NEVER FINISHES THE PREVIOUS BOOK
 Finishing is Spec's call (with a date and a rating), so a new thread
 only ever starts something; it never closes anything.

AUTHOR SPELLING
 If the author is very close to one already on the site, the site's
 spelling is used. "Sarah J Mass" (as typed in the Silver Flames post)
 becomes "Sarah J. Maas", so her books stay together.
 Tripped me up: comparing names exactly would have made "Sarah J Mass" a
 different author from "Sarah J. Maas" because of one dot and one letter.

HOW IT RUNS
 Called by sync_bluesky.py at the start of every sync, on GitHub.
 By hand: python scripts/discover_books.py --dry-run
"""

import argparse
import difflib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import import_bluesky as imp

REPO = Path(__file__).resolve().parent.parent

# The opening phrase. Case doesn't matter. The title is everything up to the
# LAST " by ", so a title with "by" in it still works ("Stand by Me by ...").
# A full stop, colon or "..." at the end is ignored.
OPENER_RE = re.compile(
    r"^\s*my thoughts as i go through\s+(?P<title>.+)\s+by\s+(?P<author>.+?)\s*[.!:…]*\s*$",
    re.IGNORECASE,
)

# How far back to look for a new opening post.
LOOKBACK = timedelta(days=14)


def read_front_matter(path):
    """The simple "key: value" lines of a log's front matter, as a dict."""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    fm = parts[1] if len(parts) == 3 else ""
    out = {}
    for line in fm.splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            out[m.group(1)] = m.group(2).strip().strip('"')
    return out


def slugify(title):
    """A title as a file name: "A Court of Splintered Harmony" -> "a-court-of-splintered-harmony"."""
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]


def tidy_author(author, known):
    """Use the site's spelling of an author when it's clearly the same person.

    "Close" means at least 85% alike once dots, spaces and case are ignored.
    One typo in a name passes; two different authors don't.
    """
    def key(name):
        return re.sub(r"[^a-z]", "", name.lower())

    best, best_score = author, 0.0
    for k in known:
        score = difflib.SequenceMatcher(None, key(author), key(k)).ratio()
        if score > best_score:
            best, best_score = k, score
    return best if best_score >= 0.85 else author


def recent_openers(handle, now):
    """Spec's opening posts from the last 14 days: (title, author, post)."""
    feed = imp.xrpc("app.bsky.feed.getAuthorFeed", actor=handle, filter="posts_no_replies", limit=50)
    found = []
    for item in feed.get("feed", []):
        if item.get("reason"):
            continue  # a repost of someone else's post, not Spec's own
        post = item["post"]
        record = post.get("record", {})
        if record.get("reply"):
            continue
        created = datetime.fromisoformat(record.get("createdAt", "1970-01-01T00:00:00+00:00").replace("Z", "+00:00"))
        if now - created > LOOKBACK:
            continue
        first_line = (record.get("text") or "").strip().splitlines()[0] if record.get("text") else ""
        m = OPENER_RE.match(first_line)
        if m:
            found.append((m.group("title").strip(), m.group("author").strip(), post))
    return found


def write_log(path, title, creator, started, thread):
    """A new log file, in the same shape the /new page writes."""
    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"creator: {json.dumps(creator, ensure_ascii=False)}",
        "type: book",
        "status: reading",
        f"started: {started}",
        "finished:",
        "tags: []",
        f"bluesky_thread: {thread}",
        "---",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def link_thread(path, thread):
    """Add a bluesky_thread line to an existing log that doesn't have one."""
    text = path.read_text(encoding="utf-8")
    head, rest = text[4:].split("\n---\n", 1)
    head = re.sub(r"(?m)^bluesky_thread:.*\n?", "", head).rstrip("\n")
    path.write_text("---\n" + head + f"\nbluesky_thread: {thread}\n---\n" + rest, encoding="utf-8")


def discover(repo, handle, now=None, dry_run=False):
    """Find new opening posts and start (or link) their logs. Returns a list of what was done."""
    now = now or datetime.now(timezone.utc)
    logs_dir = repo / "_logs"
    logs = {p: read_front_matter(p) for p in sorted(logs_dir.glob("*.md"))}
    linked = {imp.RKEY_IN_URL_RE.search(f["bluesky_thread"]).group(1)
              for f in logs.values() if f.get("bluesky_thread") and imp.RKEY_IN_URL_RE.search(f["bluesky_thread"])}
    authors = sorted({f["creator"] for f in logs.values() if f.get("creator")})
    tz = imp.site_timezone(repo)

    done = []
    for title, author, post in recent_openers(handle, now):
        rkey = post["uri"].rsplit("/", 1)[-1]
        if rkey in linked or not re.fullmatch(r"[A-Za-z0-9]{1,64}", rkey):
            continue  # already has a log, or not a normal post ID
        thread = f"https://bsky.app/profile/{handle}/post/{rkey}"
        slug = slugify(title)
        if not slug:
            continue
        path = logs_dir / f"{slug}.md"
        if path.exists():
            existing = logs.get(path, {})
            if existing.get("bluesky_thread"):
                print(f"  Skipped '{title}': a log called {slug} already follows a different thread.")
                continue
            if not dry_run:
                link_thread(path, thread)
            done.append(f"Linked existing log '{existing.get('title', title)}' to its new thread")
            continue
        creator = tidy_author(author, authors)
        started = datetime.fromisoformat(post["record"]["createdAt"].replace("Z", "+00:00")).astimezone(tz).strftime("%Y-%m-%d")
        if not dry_run:
            write_log(path, title, creator, started, thread)
        done.append(f"Started '{title}' by {creator} (from {started})")
        linked.add(rkey)
    return done


def main(argv=None):
    parser = argparse.ArgumentParser(description="Start logs for new Bluesky reading threads.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--repo", default=str(REPO), help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    repo = Path(args.repo)
    handle = re.search(r"^bluesky:\s*(\S+)", (repo / "_config.yml").read_text(encoding="utf-8"), re.MULTILINE).group(1)
    done = discover(repo, handle, dry_run=args.dry_run)
    for line in done:
        print(line)
    if not done:
        print("No new reading threads.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
