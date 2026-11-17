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
- **Champion portraits** come from Riot's official images (Data Dragon). The *Fetch portraits* action downloads any new main's portrait by itself when a log file changes. Spell names as Riot does (`Kai'Sa`, `Wukong`). A name with no portrait just shows as text.
- Rank and match history can't be fetched automatically: Riot has no public data service for Wild Rift, so they're typed in.

## Wild Rift sessions, stats and player card

**Logging a session (the easy way):** open a Claude Code session on this repo and type **`/log-wild-rift-session`**. Attach your Match History screenshot, then say or type how it went. Claude reads each match (win or loss, champion, K/D/A, and any other numbers it can see), shows you what it read, writes the session up in your own words, and asks "Post it?" before anything goes live. The instructions it follows are in `.claude/commands/log-wild-rift-session.md`. House rules for any Claude session are in `CLAUDE.md`.

Send the season *Detailed information* screens (Average / Best) or the Profile champion tiles too, and it updates the season or player-card stats.

**The Wild Rift log page** opens with four mini widgets (current season and rank, your logged record and recent form, most-played champion this season, mains), then four tabs:

- **Journal** (opens first): every note and session, newest first.
- **This season:** the current season's banner and dashboard.
- **Player:** your player card across every season.
- **History:** every past season.

Links like `.../league-of-legends-wild-rift/#player` open that tab directly. Links to a single entry still work.

**What's in those tabs:**

- **Player card:** your signature champions as portrait tiles (games, win rate, best score, Top 200 badges), a **rank journey** line through every played season, and an all-seasons Average | Best table.
- **Season dashboard** under each season's banner:
  - **from your sessions:** your record and win rate, a **form guide** (last 10 results as dots) and average K/D/A per champion, all updating by themselves;
  - **in-game stats:** the per-champion Average | Best table typed in from the game.
- **Session cards** in the timeline: one small card per match with a green or red edge, the champion's portrait, K/D/A and any MVP/SVP badge, plus your notes.

A session entry looks like this (Claude writes it for you):

```yaml
---
date: 2026-11-16 23:40:00 +0100
log: league-of-legends-wild-rift
chapter: 23
matches:
  - result: win          # win or loss
    champion: Yuumi
    kda: [1, 2, 14]
    badge: MVP           # optional; also mode, duration, gold, score, note
---
Your notes.
```

Any champion that appears gets its portrait downloaded automatically. Numbers can't be pulled from the game directly (Wild Rift has no public data feed), which is why they come from screenshots.

## Character cards (any game)

A game's log page can show a **character card**: a portrait, a name, details (race, job, world…) and a **spec sheet** of levels as bars. It's hidden until there's a name or a portrait, so an empty one never shows.

Add a `character:` section to the log's front matter. Every line is optional:

```yaml
character:
  name: Harrier "Harry" Du Bois
  portrait_page: https://discoelysium.fandom.com/wiki/Harrier_Du_Bois   # a wiki page, or…
  portrait_url:                                                       # …a direct picture link
  details:                     # shown in this order; blank values are skipped
    - {label: Race, value: Miqo'te}
    - {label: Job, value: White Mage}
  main: White Mage             # highlighted in the spec sheet
  sheet_max: 100               # the top level, so the bars know what "full" is
  sheet:
    - group: Healers
      rows:
        - {name: White Mage, level: 90}
        - {name: Scholar, level: 72}
```

- **The portrait** downloads by itself: the *Fetch portraits* action asks the wiki (Fandom or Wikipedia) for the page's main picture and saves a copy as `assets/images/characters/<log file name>.png`. A small "Image:" credit links back to the wiki. To swap it, delete that file and change the link.
- **Your own character** (like Final Fantasy): send Claude your character screen and it fills in the name, details and levels. A screenshot of your character can be the portrait too.
- **Final Fantasy Online** shows Liliah Proudfoot. Her home world, data centre and Free Company are left off on purpose, for privacy.

## Post from your phone

Open **/reads/new/** (add it to your home screen). It's one page:

1. **What are you reading or playing?** Tap the book or game. Ones marked `reading` are at the top.
2. Not there? Tap **Something else…** and pick another log, or **Start a new book, game or show**.
3. Write. The chapter is filled in with the last one you logged.
4. Tap **Post**. GitHub opens with the file filled in. Tap **Commit changes**. It's on the site a minute or two later.

You need to be signed in to GitHub in that browser or the GitHub app.

- **Starting something new:** fill in the title, author/studio and type (and the Bluesky thread link if you're posting it there), and tap *Save the new log on GitHub*. Commit, then come back to `/new`: the write screen is ready for the first entry. Two quick commits, only when you start something.
- **Finished?** First sync your last Bluesky posts in (**Sync from Bluesky**), because syncing stops once a book is finished. Then on the write screen, *Finished this one?* opens the log's file on GitHub. Change `status: reading` to `status: finished`, fill in `finished:` with the date, add `rating: 4` (out of 5; decimals like `2.53` are fine), and commit. Or just ask Claude to close it for you. The rating shows as stars on the book's page and in the Logs list.
- **Lost a post?** If the commit didn't go through (lost signal, tapped away), `/new` shows *Didn't commit it? Bring it back* for a day.
- **Sync from Bluesky** (bottom of `/new`): opens the sync on GitHub. Tap **Run workflow** twice and new Bluesky posts appear a minute or two later.

The page stores no keys or passwords. (A version that saved straight from the page with a stored key was built and then removed on purpose; see the top of `assets/js/new-entry.js`.)

## Bluesky sync

If a log has a `bluesky_thread:` line (a link to the **first post** of the thread) and is `status: reading`, new posts in that thread are copied to the site automatically.

- **Starting a new book (automatic):** open its thread with a first post that starts **"My thoughts as I go through *[title]* by *[author]*"**. The next sync spots it and starts the book's log by itself (status reading, started that day, linked to the thread), then pulls the thread in.
  - Only the first post needs that phrase. Replies like "Chapter 1: …" sync because they're in the thread.
  - If the author is close to one already on the site, the site's spelling is used ("Sarah J Mass" becomes Sarah J. Maas).
  - A new thread never finishes the previous book. You still do that yourself, with your rating.
  - Only opening posts from the last 14 days count, so old threads can't come back by accident.
- **Starting a book by hand instead:** paste the first post's link in the *Bluesky thread* box when you start the log on `/new`. If you start it on `/new` first and post the opener afterwards, the sync links the two instead of making a second log.

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

## Ratings, finished books and DNFs

- **Ratings** are out of 5, decimals allowed (`rating: 2.53`). They show as stars, partly filled for exact values, on the book's page and in the Logs list.
- **Did not finish:** set `status: dropped`. The site shows it as **Did not finish**, and the Logs list can filter for it.
- **Books from before the site** (the reading-list back catalogue) can have **no dates at all**. Only something you're currently reading needs a `started:` date. Your note about the book goes under the second `---` in its log file and shows at the top of its page.
- **The Logs list order:** dated logs come first, newest first, then undated ones A to Z.
- **Adding more from your reading list:** send Claude screenshots of the list. It adds each book with your rating and your note, word for word. Titles and author names get correct spellings, but your notes are never changed. If a note is cut off in the screenshot, it asks you for the rest instead of guessing.

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
rating:             # out of 5, once you've finished, e.g. 2.53
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
