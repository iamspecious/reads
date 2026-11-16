---
description: Log a Wild Rift play session from match-history screenshots and Spec's notes
argument-hint: (attach match history screenshot(s), then say or type your notes)
---

# Log a Wild Rift session

Spec has just played some Wild Rift and wants it on the site. They'll send one or more **screenshots** (usually the in-game Match History list, sometimes an end-of-match screen or the season stats screens) and **notes**, often spoken and transcribed. Turn that into one session entry on Tech by Spec.

Read `CLAUDE.md` first. Keep everything plain and quick: Spec is often between games.

## 1. Read the screenshots

Zoom in if needed: crop and enlarge the image to read small numbers and icons. Don't guess.

For **each match** pull out:

| Field | Required | Notes |
|---|---|---|
| `result` | yes | `win` (Victory) or `loss` (Defeat) |
| `champion` | yes | Spelled as Riot does: Yuumi, Lulu, Nami, Seraphine, Malphite, Cho'Gath, Lillia, Miss Fortune, Zyra, Milio |
| `kda` | yes | `[kills, deaths, assists]` |
| `mode` | if shown | e.g. `Ranked` |
| `duration` | if shown | `"18:10"` (quoted) |
| `gold` | if shown | the number under the coin icon |
| `score` | if shown | the match score (the column where MVP/SVP numbers sit) |
| `badge` | if earned | `MVP` or `SVP` |

**Order matters.** The game lists newest first; the entry lists matches **oldest first** (the order they were played).

If a screenshot isn't a Wild Rift match screen, or a number can't be read, say so and ask. Never invent a stat.

## 2. Show Spec what you read

Show a short table (result, champion, K/D/A, plus anything else you found) and ask: "Anything to fix?" Fix whatever they correct.

## 3. The notes

- Use Spec's own words. Don't summarise, reword, add opinions or add a conclusion.
- You may fix obvious dictation slips: champion names (Yummi → Yuumi), "GM 2" → "GM2", and missing full stops at the very end. Nothing more.
- A note about one specific match goes on that match as `note:`. Everything else goes in the body.
- No notes is fine: the body can be empty.

## 4. Write the entry

- **Log:** `league-of-legends-wild-rift`
- **Season:** the newest season in that log's `seasons:` list (highest number), unless the matches were clearly played in an earlier season; then ask.
- **Date and time:** when the session ended, in Europe/Berlin time with its offset (`+0100` in winter, `+0200` in summer). Use what Spec says, or the screenshot, or now.
- **File:** `_entries/YYYY-MM-DD-HHMMSS-league-of-legends-wild-rift.txt`, using that date and time.

Exact shape (no comments in the file, two-space indents exactly as shown; `tests/test_content.py` reads this shape):

```
---
date: 2026-11-16 23:40:00 +0100
log: league-of-legends-wild-rift
chapter: 23
matches:
  - result: win
    champion: Yuumi
    kda: [1, 2, 14]
    mode: Ranked
    duration: "17:02"
    gold: 9433
    score: 412
    badge: MVP
  - result: loss
    champion: Lulu
    kda: [0, 4, 9]
    note: "Spec's words about this match"
---
Spec's notes for the session, exactly as said.
```

- Leave out optional fields that weren't shown. Don't write empty ones.
- Quote `note:` values JSON-style (`"..."`) so colons or quotes in them can't break the file.
- If the notes contain two curly braces, or a curly brace followed by a percent sign, wrap the body in raw markers (see `_includes/entry-text.html`).

## 5. Season stats (only if those screenshots were sent)

If Spec sends the season **Detailed information** screens (Average / Best, S23 tab) or the **season history** cards, update that season in `_logs/league-of-legends-wild-rift.md`: `rank`, `matches`, `win_rate`, and `champion_stats` (same shape as the entries already there). For the **ALL** tab or the Profile champion tiles, update `profile:` instead. Show Spec what changed before posting.

## 6. Check and post

1. Run `python -m unittest discover -s tests`. Fix anything it flags.
2. Commit on your working branch with a message like `Log Wild Rift session: 4 matches (3W 1L)`, push, and open a pull request.
3. Give Spec a one-line summary and ask: "Post it?" Merge when they say yes.
4. A champion with no portrait yet gets one automatically: the *Fetch champion portraits* action runs after the merge.
5. After about two minutes, check the session shows on https://iamspecious.github.io/reads/logs/league-of-legends-wild-rift/ and tell Spec it's live.
