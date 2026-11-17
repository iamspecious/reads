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
| Books / Tech halves | `_data/sections.yml` |
| Bluesky import and sync | `scripts/import_bluesky.py`, `scripts/sync_bluesky.py` |

Entries are `.txt` (not Markdown) so text shows exactly as written. Text containing two curly braces or a curly brace followed by a percent sign is wrapped in raw markers (see `_includes/entry-text.html`).

## Finishing a book or game

Run **Sync Bluesky threads** first if the log has a `bluesky_thread`, because syncing stops once it's finished. Then in `_logs/<slug>.md`: `status: finished`, `finished: YYYY-MM-DD`, and `rating:` out of 5 if Spec gives one (decimals allowed, use their number exactly). Open a PR and ask before merging.

## Wild Rift sessions

Use the `/log-wild-rift-session` command (`.claude/commands/log-wild-rift-session.md`). It has the exact file format.
