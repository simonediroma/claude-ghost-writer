---
description: Build the book's website — one pre-generated page ready for GitHub Pages, mobile first. Opening with cover and tagline, the book with a download button, featured characters or key ideas, the podcast episodes with RSS feed, and the explorable book graph (search, chapters, open points). Each optional section appears only when its source exists. Texts come from a short dialogue with the author and live in site.yaml.
---

# Skill: Site

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Turns what the project already has — the book, the graph, the podcast — into a website the author can publish for free on GitHub Pages. The page is generated into `docs/index.html`: all content is in the HTML, JavaScript only draws the graph.

If `build_site.py` does not exist in the project root, generate it before running any site command. The script reads `site.yaml`, `graph/cards/**/*.yaml`, podcast scripts and episodes, and writes a single self-contained `docs/index.html` with no external dependencies. Requires PyYAML; optional Pillow for cover resize, ffprobe for episode durations.

The author approves every text on the page. Nothing is published without them.

---

## Sections

| Section | Shown when | Source |
|---|---|---|
| Opening | always | `site.yaml` (kicker, title, subtitle, tagline) + `cover.jpg` / `cover.png` in the book root |
| The book | always | `site.yaml → book.paragraphs` + optional download (PDF / EPUB) |
| Characters / People / Key ideas | `featured` is not empty | `site.yaml → featured`; with `id`, the card links to the graph |
| Podcast | MP3s exist | `podcast/scripts/episode-NN.md` (title, description) + `podcast/episodes/*.mp3` + `podcast/feed.xml` |
| Graph | `graph/` exists | `graph/cards/**` (`/ghost-writer:graph`), optionally limited to the first N chapters |

The section title for featured entries follows the preset (fiction, fable, children's book → characters; biography → people; essay, manual → key ideas); `featured_title` overrides it.

---

## Step 1 — What exists

Read `book.config.json` and check, silently:
- `python3 -c "import yaml"` — if it fails, give the author `pip install pyyaml` and stop
- `graph/` → `python3 graph.py check` (if chapters wait for a sync, run the graph Sync first)
- `podcast/episodes/*.mp3`, `podcast/feed.xml`
- a cover (`cover.jpg`, `cover.png`), and files to offer for download (`manuscript/*.pdf`, `*.epub`)
- `site.yaml` — if it exists, this is an update: skip to the block the author wants to change

Then say in one line what the site will contain:
> The site will have: opening, the book, [characters], [podcast — N episodes], [graph — N cards]. Missing: [cover / download]. Shall we write the texts?

If there is no cover, say it once: the page works without it, but a square image (at least 720×720) makes the opening and the link previews much better.

---

## Step 2 — The texts (one block at a time)

Draft each block in the book's language and in the author's voice (`author_voice`), from `book_profile` / `premise`, `target_reader`, the outline and the **complete** chapters. Show the draft, wait for yes / change. Never spoil beyond what the author wants public.

1. **Opening**: `kicker` (genre and format, 3–7 words, e.g. "A serialized science-fiction novel"), `tagline` (one or two sentences: the hook), `subtitle`, `author`.
2. **The book**: `book.paragraphs`, 2–3 short paragraphs — the premise, the protagonist's situation, the tone. Back-cover copy, not a summary.
3. **Download** (optional): which file (`book.download.file`, a path from the book root), the button `label`, an optional `note` (format, chapters included).
4. **Featured** (optional, 3–5 entries): for fiction the main characters, for essays the key ideas. If the graph exists, propose cards from it (`python3 graph.py find <name>`) and use their `id`; write `role` (2–4 words) and `text` (2 sentences, no spoilers).
5. **Podcast** (if episodes exist): `podcast.title`, `podcast.text`.
6. **Graph** (if it exists):
   - Ask: *"The graph tells the whole book. Do you want to show it all, or only up to a chapter (for serial publication)?"* → `graph.up_to_chapter` (cards, facts and events beyond that chapter are left out; unsourced open points and notes are hidden).
   - `graph.start`: 6–8 cards to start from (default: the most connected).
   - `title`, `text`, `spoiler`, `open_notice` have defaults in the book's language: change them only if the author wants.

Write `site.yaml` (start from `python3 build_site.py --init` if it does not exist):

```yaml
title: "…"
subtitle: "…"
author: "…"
kicker: "…"
tagline: "…"
book:
  title: "The book"
  paragraphs: ["…", "…"]
  download: {file: "manuscript/my-book-final.pdf", label: "Download the book (PDF)", note: "A5, chapters 1–12"}
featured_title: "Characters"        # optional
featured:
  - {id: tom, role: "Repair technician", text: "…"}
  - {name: "Deep focus", role: "Idea", text: "…"}    # without the graph: name instead of id
podcast: {title: "The podcast", text: "One chapter per episode, read aloud."}
graph:
  up_to_chapter: null               # or N: show only chapters 1–N
  start: [tom, emma]
  search_placeholder: "Search: Tom, eWatch…"   # optional
colors: {accent: "#6ee7a0", background: "#0e1116"}   # optional
labels: {}                          # optional: override any interface label
output: docs
```

---

## Step 3 — Build

```bash
python3 build_site.py --check     # validates site.yaml, featured ids, files; writes nothing
python3 build_site.py             # writes docs/index.html, copies cover, download, episodes, feed.xml
```

It stops on graph errors (run `python3 graph.py build`), on template placeholders without a value; it warns about a missing cover, a missing download file, a featured `id` not in the graph, an empty `podcast.base_url`, a site over 900 MB.

If a browser is available, take a phone-width and a desktop screenshot of `docs/index.html` and show them to the author. Otherwise tell them to open `docs/index.html` in their browser.

---

## Step 4 — Publish on GitHub Pages

Explain once, then let the author do it (never push or change repository settings without being asked):

1. Commit `docs/` and push to GitHub.
2. Repository → **Settings → Pages → Build and deployment → Deploy from a branch** → branch `main`, folder `/docs` → Save.
3. After a minute the site is at `https://<user>.github.io/<repository>/`.
4. If there is a podcast: set `book.config.json → podcast.base_url` to `https://<user>.github.io/<repository>/episodes`, run `python3 export_podcast.py feed`, then `python3 build_site.py` again and push. The feed URL for podcast apps is `…/feed.xml`.

Limits: GitHub refuses files over 100 MB and Pages sites over 1 GB — at 96 kbps an episode is about 0.7 MB per minute.

---

## Keeping It Updated

The site is a derived file: it never asks for confirmation once `site.yaml` is approved.

- After a graph Sync, if `site.yaml` exists, `python3 build_site.py` is run (see `skills/graph/SKILL.md → Sync`).
- After new podcast episodes, the podcast skill runs it too.
- Texts: change `site.yaml` (through this skill), then rebuild.
- For serial publication, raise `graph.up_to_chapter` when a new chapter goes public.

Tell the author when `docs/` changed and needs a commit + push to go live.

---

## Requirements

Python 3.9+, PyYAML. Optional: Pillow (`pip install pillow`) for the 720 px cover, ffprobe (with ffmpeg) for exact episode durations. The page has no external dependencies: no fonts, scripts or trackers loaded from other sites.
