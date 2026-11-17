# CLAUDE.md — house rules for working on this repo

This is **Books by Spec** and **Tech by Spec**: Spec's live reading and gaming logs, a Jekyll site on GitHub Pages at https://iamspecious.github.io/reads/. The README explains how everything works for Spec; this file is for Claude.

## How Spec likes things done

- **Ask before anything goes live.** Work on a branch, open a pull request, and merge only when Spec says so ("post it", "go live", "merge").
- **Never write words on the site in Spec's voice.** Entry text is Spec's own, unchanged. No taglines, slogans or filler. Labels like "Latest" are fine.
- **Plain English for Spec.** Short sentences, everyday words, technical terms explained. Say what you checked and what you couldn't.
- **No keys, tokens or passwords** anywhere in the repo or on the site. This was decided deliberately (see the top of `assets/js/new-entry.js`).
- **No tracking, no outside scripts or fonts.** Media is downloaded into the repo, never hotlinked.

## Code rules

- Comment every script and template with **why** each part exists, in very plain English (like explaining to a kid).
- When something trips you up, add a "Tripped me up:" note in a comment where it happened.
- **Never put comments in generated files** (entries, the search index, images). Notes about them go in the script that makes them.
- **Liquid reads inside `{% comment %}` blocks.** Never write two curly braces, or a curly brace followed by a percent sign, inside a template comment: it breaks the build. `tests/test_content.py` checks for this.
- Run `python -m unittest discover -s tests` before pushing. The *Check* action runs it on every push.
- To check a build locally, the github-pages gem (Jekyll 3.10) is what GitHub uses.

## Where things live

| What | Where |
|---|---|
| Logs (one per book, game or show) | `_logs/<slug>.md` |
| Entries (one per post or session) | `_entries/YYYY-MM-DD-HHMMSS-<slug-or-post-id>.txt` |
| Pictures, GIFs, videos | `assets/images/entries/` |
| Champion portraits | `assets/images/champions/<name>.png` (fetched by a workflow) |
| Character portraits | `assets/images/characters/<log slug>.<ext>` (`scripts/fetch_portraits.py`, same workflow) |
| Books / Tech halves | `_data/sections.yml` |
| Bluesky import and sync | `scripts/import_bluesky.py`, `scripts/sync_bluesky.py` |
| New books from Bluesky openers | `scripts/discover_books.py` (runs at the start of every sync) |

Entries are `.txt` (not Markdown) so text shows exactly as written. Text containing two curly braces or a curly brace followed by a percent sign is wrapped in raw markers (see `_includes/entry-text.html`).

## Starting a book from Bluesky

Spec opens each reading thread with "My thoughts as I go through <title> by <author>" (or "read through"; any short phrase before "through" works). The sync starts that book's log by itself (see `scripts/discover_books.py`). If Spec asks why a new book didn't appear, check the first post really starts with that phrase and was made in the last 14 days, then read the *Sync Bluesky threads* run log.

## Finishing a book or game

Run **Sync Bluesky threads** first if the log has a `bluesky_thread`, because syncing stops once it's finished. Then in `_logs/<slug>.md`: `status: finished`, `finished: YYYY-MM-DD`, and `rating:` out of 5 if Spec gives one (decimals allowed, use their number exactly). Open a PR and ask before merging.

## Adding books from Spec's reading list

Spec keeps a reading list in a phone app (Read and Did Not Finish columns) and may send screenshots of it.

- One log per book: `type: book`, `status: finished` (Read) or `status: dropped` (Did Not Finish, shown on the site as "Did not finish").
- `started:` and `finished:` stay blank unless Spec gives dates. Only `status: reading` logs need a start date.
- `rating:` from the "3/5" at the start of a note (3.5/5 becomes `3.5`). No number means no rating line.
- The note goes **word for word** as the log body, rating and "DNF -" included, curly apostrophes included. Never reword or tidy it.
- **If a note is cut off** in the screenshot (ends in "…"), leave the note out and ask Spec for the full text. Never guess an ending.
- Fix only **titles and author names** (Hero's → Heroes, Pat Baker → Pat Barker, R.F Chang → R.F. Kuang), and say which you fixed.
- Genre hashtags become `tags:` ("#HistoricalFiction" → "Historical Fiction"). Leave out list-keeping tags: #Books, #Bought, #TBR, #DNF, #Currently.
- Check a log with that slug doesn't already exist before adding it.

## Character cards

A game log's `character:` section drives `_includes/character-card.html` (format in the README). Wiki pictures (Fandom, Wikipedia) are fine as portraits: use `portrait_page:` and the workflow downloads it. For Spec's own character, read their screenshots for name, details and levels, show them what you read, and only fill in what's visible. **Never put Spec's home world, data centre (server) or Free Company on the site**, even if a screenshot shows them: Spec asked for this, for privacy. A screenshot of their own character goes in directly as `assets/images/characters/<log slug>.jpg` (cropped to the character, about 600×800, with the photo's hidden details such as location removed).

## Wild Rift sessions

Use the `/log-wild-rift-session` command (`.claude/commands/log-wild-rift-session.md`). It has the exact file format.
