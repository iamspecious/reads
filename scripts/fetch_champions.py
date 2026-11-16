#!/usr/bin/env python3
"""
fetch_champions.py: download portraits of your mains into the site.

WHAT IT DOES
 1. Reads every log in _logs/ and collects the champion names listed under
    "mains:" in its seasons (for example: mains: [Yuumi, Lulu, Nami]).
 2. Asks Riot's official image service ("Data Dragon", the public home of
    League's champion pictures) for its newest list of champions.
 3. For each main that doesn't have a portrait yet, downloads the square
    portrait into assets/images/champions/<name>.png.

WHY RIOT'S PC LEAGUE IMAGES
 Wild Rift has no public data service of its own. Its champions are the
 same characters as PC League, which Riot publishes freely for fan sites.
 Riot's fan-content rules allow this kind of non-commercial use.

WHY DOWNLOAD AND NOT LINK
 Same as Bluesky images: a copy in the repo keeps working even if Riot
 moves its files, and visitors' browsers never contact Riot.

FILE NAMES
 Lower case, with spaces and punctuation removed, so "Kai'Sa" becomes
 kaisa.png. _includes/champion.html builds the same name to find it.
 Riot's own IDs are different for a few champions (Wukong is
 "MonkeyKing"), so we match on the champion's display name, not the ID.

HOW TO RUN IT
 It runs on GitHub (Actions -> "Fetch champion portraits"), by itself
 whenever a log file changes, or by pressing Run workflow.
 By hand: python scripts/fetch_champions.py
 It only uses Python's built-in tools, like the Bluesky importer.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "assets" / "images" / "champions"
DDRAGON = "https://ddragon.leagueoflegends.com"
USER_AGENT = "reads-champion-portraits/1.0 (+static site)"

# Finds "mains: [Yuumi, Lulu, Nami]" lines in a log's front matter.
MAINS_RE = re.compile(r"^\s*mains:\s*\[(.*?)\]\s*$", re.MULTILINE)


def slug(name):
    """The file name for a champion: lower case, letters and numbers only."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read(), resp.headers.get("Content-Type", "")


def wanted_mains(repo):
    """Every champion named under mains: in any log, without repeats."""
    names = []
    for path in sorted((repo / "_logs").glob("*.md")):
        for m in MAINS_RE.finditer(path.read_text(encoding="utf-8")):
            for raw in m.group(1).split(","):
                name = raw.strip().strip("\"'")
                if name and name not in names:
                    names.append(name)
    return names


def main():
    names = wanted_mains(REPO)
    missing = [n for n in names if not (OUT / f"{slug(n)}.png").exists()]
    print(f"Mains in the logs: {', '.join(names) or 'none'}")
    if not missing:
        print("Every main already has a portrait. Nothing to do.")
        return 0

    # The newest version of Riot's champion data comes first in this list.
    version = json.loads(get(f"{DDRAGON}/api/versions.json")[0])[0]
    champs = json.loads(get(f"{DDRAGON}/cdn/{version}/data/en_US/champion.json")[0])["data"]
    by_name = {slug(c["name"]): c["image"]["full"] for c in champs.values()}

    OUT.mkdir(parents=True, exist_ok=True)
    not_found = []
    for name in missing:
        image = by_name.get(slug(name))
        if not image:
            # Most likely a typo in the log, or a champion that only exists in Wild Rift.
            not_found.append(name)
            continue
        body, ctype = get(f"{DDRAGON}/cdn/{version}/img/champion/{image}")
        if not ctype.startswith("image/png"):
            raise SystemExit(f"Expected a PNG for {name}, got {ctype}. Nothing saved for it.")
        (OUT / f"{slug(name)}.png").write_bytes(body)
        print(f"  Saved {name} -> assets/images/champions/{slug(name)}.png")

    if not_found:
        print(f"No official portrait found for: {', '.join(not_found)}. Check the spelling in the log. "
              "Their names still show on the site, just without a picture.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
