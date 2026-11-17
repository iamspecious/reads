#!/usr/bin/env python3
"""
fetch_portraits.py: download each game's character portrait into the site.

WHAT IT DOES
 A game's log can have a "character:" section (see the README). If it
 gives either
     portrait_page: https://discoelysium.fandom.com/wiki/Harrier_Du_Bois
         (a wiki page about the character), or
     portrait_url:  https://.../picture.png
         (a direct link to a picture),
 and the site doesn't have that log's portrait yet, this downloads it to
     assets/images/characters/<log file name>.<png|jpg|webp|gif>
 _includes/character-card.html then shows it on the log page.

HOW A WIKI PAGE BECOMES A PICTURE
 Wikipedia and Fandom wikis run the same wiki software (MediaWiki). It has
 a public "api.php" that answers "what's the main picture on this page?"
 (prop=pageimages). We ask that, then download the picture it names.
 Fandom keeps api.php at /api.php; Wikipedia keeps it at /w/api.php.

WHY DOWNLOAD AND NOT LINK
 Same as everywhere else on the site: a copy in the repo keeps working if
 the wiki moves its files, and visitors' browsers never contact the wiki.
 Tripped me up (well, nearly): Fandom blocks pictures shown straight from
 its servers on other sites ("hotlinking"), so linking wouldn't even work.

RULES THAT KEEP IT SAFE
 - Only https links.
 - Only real pictures (png, jpeg, webp, gif) up to 8 MB are saved.
 - A portrait already in the repo is never downloaded again. To replace
   one, delete the file and the next run fetches it fresh.

HOW IT RUNS
 On GitHub, in the "Fetch portraits" action, whenever a log changes.
 By hand: python scripts/fetch_portraits.py
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "images" / "characters"
USER_AGENT = "reads-character-portraits/1.0 (+static site)"
EXT_FOR_TYPE = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/gif": ".gif"}
MAX_BYTES = 8 * 1024 * 1024

# The two lines we look for, inside a log's front matter. Indented, because
# they sit under "character:".
PAGE_RE = re.compile(r"^\s+portrait_page:\s*\"?(https://[^\s\"]+)\"?\s*$", re.MULTILINE)
URL_RE = re.compile(r"^\s+portrait_url:\s*\"?(https://[^\s\"]+)\"?\s*$", re.MULTILINE)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def picture_from_wiki_page(page):
    """Ask the wiki which picture is the main one on this page. Returns its link, or None."""
    parts = urllib.parse.urlparse(page)
    if parts.scheme != "https" or "/wiki/" not in parts.path:
        return None
    title = urllib.parse.unquote(parts.path.split("/wiki/", 1)[1])
    api_path = "/w/api.php" if parts.netloc.endswith("wikipedia.org") else "/api.php"
    query = urllib.parse.urlencode({
        "action": "query", "prop": "pageimages", "piprop": "original",
        "titles": title, "format": "json", "redirects": 1,
    })
    body, _ = get(f"https://{parts.netloc}{api_path}?{query}")
    pages = json.loads(body).get("query", {}).get("pages", {})
    for p in pages.values():
        src = (p.get("original") or {}).get("source")
        if src and src.startswith("https://"):
            return src
    return None


def wanted(repo):
    """(log file name, page or None, url or None) for every log asking for a portrait."""
    out = []
    for path in sorted((repo / "_logs").glob("*.md")):
        parts = path.read_text(encoding="utf-8").split("---", 2)
        fm = parts[1] if len(parts) == 3 else ""
        page = PAGE_RE.search(fm)
        url = URL_RE.search(fm)
        if page or url:
            out.append((path.stem, page.group(1) if page else None, url.group(1) if url else None))
    return out


def already_have(slug):
    return any((OUT / f"{slug}{ext}").exists() for ext in EXT_FOR_TYPE.values())


def main():
    todo = [w for w in wanted(REPO) if not already_have(w[0])]
    if not todo:
        print("Every character portrait asked for is already here. Nothing to do.")
        return 0
    OUT.mkdir(parents=True, exist_ok=True)
    for slug, page, url in todo:
        try:
            src = url or picture_from_wiki_page(page)
            if not src:
                print(f"  {slug}: the wiki page has no main picture. Try a direct portrait_url instead.")
                continue
            body, ctype = get(src)
            ext = EXT_FOR_TYPE.get(ctype.split(";")[0].strip().lower())
            if not ext:
                print(f"  {slug}: expected a picture but got '{ctype}'. Nothing saved.")
                continue
            if len(body) > MAX_BYTES:
                print(f"  {slug}: the picture is over 8 MB. Nothing saved.")
                continue
            (OUT / f"{slug}{ext}").write_bytes(body)
            print(f"  Saved {slug}{ext}")
        except Exception as err:  # noqa: BLE001 (one bad link shouldn't stop the others)
            print(f"  {slug}: couldn't fetch the portrait ({err}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
