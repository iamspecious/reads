# Books by Spec · Tech by Spec

Live logs of what Spec is reading and playing: short reactions, chapter by chapter, as they happen.

- **Books by Spec:** https://iamspecious.github.io/reads/
- **Tech by Spec** (games): https://iamspecious.github.io/reads/games/
- **Post something:** https://iamspecious.github.io/reads/new/

It's a plain Jekyll site built by GitHub Pages. No server, no paid services, no tracking, no cookies, and no keys or passwords stored anywhere.

## What's on the site

The site has two halves, switched with the **Books | Games** tabs at the top.

| | Books by Spec | Tech by Spec |
|---|---|---|
| Address | `/reads/` | `/reads/games/` |
| What's in it | books (and shows, for now) | games |
| Logo and colours | book logo, pink → violet → teal | Tech logo, deep purple → blue |
| Top box | Currently reading | Currently playing |
| RSS feed | `/reads/feed.xml` | `/reads/games/feed.xml` |

Each half has its own **Latest** page (newest entries first), **Logs** list (filter by status) and **Search**. A log goes in whichever half matches its `type:`. On the Games side, `status: reading` shows as "Playing".

- **Each log** has its own page, oldest entry first, so it reads like the journey.
- **Tap an entry's timestamp** to get a link to that one entry, to share it.
- **The look:** always dark, whatever the phone's setting. Each half wears its logo's colours: a gradient band behind the header, a soft glow at the top, a gradient border round the Currently box, and its own link and tag colour.

Names, logos, which types go where, and words like "reading/playing" are all in `_data/sections.yml`. Colours are in `assets/css/reads.css` (`.theme-books` and `.theme-games`). The heading font is Bebas Neue, stored in the repo (free licence in `assets/fonts/OFL.txt`).

## Games played in seasons (Wild Rift)

A game can be logged season by season instead of chapter by chapter. Add `progress: season` and a `seasons:` list to its log file (see `_logs/league-of-legends-wild-rift.md`):

```yaml
progress: season
seasons:
  - season: 23
    year: 2026
    year_name: Eminence      # the season year's name, optional
    rank: Grandmaster II
    mains: [Yuumi, Lulu, Nami]
    started: 2026-09-23
    ends: 2027-01-08         # or finished: once it's over
    matches: 343
    win_rate: 50
    note: Unplayed           # optional, shown with the dates
```

- **Currently playing** shows the newest season: number, year, rank, mains with portraits, dates and record.
- **The log page** has one block per season, newest first: the season's banner, then the notes for it.
- **On `/new`** the number box becomes **Season** for these games and starts on the current one. Notes are tagged `S23`.
- **New season or rank change:** edit the log file on GitHub. Put the new season at the top of the list and update `rank:` whenever it changes.
- **Champion portraits** come from Riot's official images (Data Dragon). The *Fetch champion portraits* action downloads any new main's portrait by itself when a log file changes. Spell names as Riot does (`Kai'Sa`, `Wukong`). A name with no portrait just shows as text.
- Rank and match history can't be fetched automatically: Riot has no public data service for Wild Rift, so they're typed in.

## Post from your phone

Open **/reads/new/** (add it to your home screen). It's one page:

1. **What are you reading or playing?** Tap the book or game. Ones marked `reading` are at the top.
2. Not there? Tap **Something else…** and pick another log, or **Start a new book, game or show**.
3. Write. The chapter is filled in with the last one you logged.
4. Tap **Post**. GitHub opens with the file filled in. Tap **Commit changes**. It's on the site a minute or two later.

You need to be signed in to GitHub in that browser or the GitHub app.

- **Starting something new:** fill in the title, author/studio and type (and the Bluesky thread link if you're posting it there), and tap *Save the new log on GitHub*. Commit, then come back to `/new`: the write screen is ready for the first entry. Two quick commits, only when you start something.
- **Finished?** On the write screen, *Finished this one?* opens the log's file on GitHub. Change `status: reading` to `status: finished`, fill in `finished:` with the date, and commit. Syncing from Bluesky stops for it.
- **Lost a post?** If the commit didn't go through (lost signal, tapped away), `/new` shows *Didn't commit it? Bring it back* for a day.
- **Sync from Bluesky** (bottom of `/new`): opens the sync on GitHub. Tap **Run workflow** twice and new Bluesky posts appear a minute or two later.

The page stores no keys or passwords. (A version that saved straight from the page with a stored key was built and then removed on purpose; see the top of `assets/js/new-entry.js`.)

## Bluesky sync

If a log has a `bluesky_thread:` line (a link to the **first post** of the thread) and is `status: reading`, new posts in that thread are copied to the site automatically.

- **When:** a timed job is set to run at :17 and :47 past every hour. **GitHub's timer is unreliable** and skips many runs, sometimes for hours, so for posts to appear straight away use **Sync from Bluesky** on `/new` (or Actions → *Sync Bluesky threads* → **Run workflow**). Nothing is ever missed: each sync picks up everything new since the last one.
- **What it takes:** every post *you* wrote in that thread, on **every branch**. It doesn't matter which of your own posts you hit reply on. Other people's replies are skipped. Posts are put in time order.
- **Pictures, GIFs and videos are copied onto the site**, not linked, so they keep working if Bluesky changes:
  - photos are saved as they are;
  - GIFs from Bluesky's GIF button (from Klipy, or Tenor) are saved as Klipy's small MP4 copy and play like a GIF: on their own, looping, silent;
  - uploaded videos and uploaded GIFs are saved up to 30 MB (GIF-style ones loop silently; real videos get play controls);
  - anything too big stays on Bluesky, and the entry's *Bluesky* link still gets you to it.
- **Older entries get their media back:** if an entry is missing a GIF or picture its post has, the next sync adds it. The text is never changed.
- **Safe to re-run:** posts already on the site are skipped (matched by the post's ID).
- **Posting in both places?** The same thing posted on Bluesky *and* on `/new` shows up twice. Pick one place per post.
- **Paused?** GitHub pauses timed jobs after 60 days with no activity in the repo. If the Actions tab says so, press the button there to turn it back on.

### Chapter tags

A post gets a chapter tag when it starts with or mentions one of these:

- `Ch 12`, `Ch. 12`, `ch12`, `Chapter 12`
- ranges: `Chapter 7 - 9`, `Chapters 12-14`, `Ch 7 to 9` → tagged `7-9`
- a bare number and a colon at the very start: `31: kiss of life…`, `34-37:`

Anything else, like "Just finished the second chapter" or a follow-up post with no number, is left untagged on purpose.

### Import a thread by hand

For a thread that isn't synced (say, a finished book):

1. On GitHub: **Actions → Import Bluesky thread → Run workflow**, branch `main`.
2. Paste the link to the **first post** of the thread, and type the **log slug** (the log's file name without `.md`, e.g. `a-court-of-silver-flames`).
3. Tick **Dry run** to just see the count first.
4. When it finishes, open the run: the summary shows how many posts were found and imported, and the first and last new post.

### Starting a log's Bluesky posts from fresh

To re-import a whole thread from scratch: delete that log's entries that have a `source_url:` line (keep any posted from `/new`), delete their files in `assets/images/entries/`, commit, then run **Sync from Bluesky**.

## Start a new log by hand

The easy way is *Start a new book, game or show* on `/new`. By hand: in `_logs/`, **Add file → Create new file**, name it e.g. `hades-ii.md` (the name becomes its web address), and paste:

```yaml
---
title: "Hades II"
creator: "Supergiant Games"
type: game          # book, game or show
status: reading     # reading, finished or dropped
started: 2026-11-20
finished:
tags: ["roguelike"]
bluesky_thread: https://bsky.app/profile/booksbyspec.bsky.social/post/3abc…   # optional
---
```

Anything under the second `---` shows as a note at the top of the log page.

## The files

**Entries** live in `_entries/`, one `.txt` file each. They're `.txt` so the text shows exactly as written (Markdown would turn `#hashtags` into headings).

```yaml
---
date: 2026-11-10 21:14:03 +0100
log: a-court-of-silver-flames
chapter: 12
source_url: https://bsky.app/profile/booksbyspec.bsky.social/post/3m…
images:                       # only if the post has pictures or GIF-button GIFs
  - src: "/assets/images/entries/3m…-1.jpg"
    alt: "description"
videos:                       # only if it has a video or a GIF saved as video
  - src: "/assets/images/entries/3m…-1.mp4"
    alt: "description"
    gif: true                 # true = loop silently like a GIF
---
The text, exactly as written.
```

`chapter` and `source_url` can be blank. If a post contains `{{` or `{%`, its text is wrapped in `{% raw %}…{% endraw %}` so it can't break the site build; the site removes the wrapper when showing it.

**Logs** live in `_logs/` (see above). **Media** lives in `assets/images/entries/`, named after the Bluesky post ID.

## Security, in short

- **Only you can change the site.** You're the only person with write access to the repo. Anyone else who taps Post just gets GitHub's "fork this repository" screen, and nothing changes unless you merge it.
- **No keys or passwords anywhere on the site.** Posting goes through GitHub's own screen, with your own login and two-factor sign-in. Keep two-factor on.
- **`/new` has a strict browser safety rule:** only this site's own scripts can run there, and the page can't send data anywhere by itself.
- **The importer only trusts known places:** Bluesky's servers, Klipy and Tenor for GIFs. Ordinary links in posts are never downloaded, and it refuses anything that isn't a real image or video.
- **Every change is in the git history** and can be undone.

## Checks

The **Check** action runs on every push, including every post from `/new` and every sync. It tests the importer against a pretend Bluesky, and validates every log and entry file: the log exists, the date has a time zone, media files are in the repo, template code is safely wrapped. A red X on the Actions tab names the file that needs fixing. Run it yourself with `python -m unittest discover -s tests`.

## If something looks wrong

- **Synced but nothing new appears:** open the sync run on the Actions tab and read its summary. It says how many of your posts it found in the thread and why any were skipped.
- **GIFs stop appearing:** Bluesky may have changed GIF service again. The trusted list is `GIF_HOSTS` in `scripts/import_bluesky.py`.
- **The site doesn't update after a commit:** check *pages build and deployment* on the Actions tab. If it's red, the Check action usually names the file causing it.

## Cost

Nothing. GitHub Actions and Pages are free for public repos, and Bluesky's public API needs no account or key.

## Turning the site on

Settings → Pages → *Deploy from a branch* → `main`, folder `/ (root)`.
