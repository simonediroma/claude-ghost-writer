# Build Your Book Website

A step-by-step guide to turning the book you are writing with Ghost Writer into a website, free on GitHub Pages, with one command: `/ghost-writer:site`.

You get one page (`docs/index.html`). It is built for phones first and loads no external fonts, scripts or trackers. All the text is in the HTML; JavaScript only draws the graph.

---

## 1. What the site contains

The site uses what your project already has. Optional sections appear only when their source exists.

| Section | Appears when | Where it comes from |
|---|---|---|
| Opening (cover, title, tagline) | always | `site.yaml` + `cover.jpg` / `cover.png` |
| The book (+ download button) | always | `site.yaml → book` + a PDF / EPUB |
| Characters / People / Key ideas | you choose some | `site.yaml → featured` |
| Podcast (episodes + RSS) | MP3s exist | `/ghost-writer:podcast` |
| Explorable graph (search, chapters, open points) | `graph/` exists | `/ghost-writer:graph` |

The featured section's title depends on the preset: **characters** for fiction, fables and children's books, **people** for biographies, **key ideas** for essays and manuals.

---

## 2. Before you start

**Required**
- Python 3.9+ and PyYAML: `pip install pyyaml`
- A Ghost Writer project with `book.config.json` and at least some complete chapters
- A GitHub account (to publish)

**Recommended**
- **A cover.** Save a square image, at least 720×720, as `cover.jpg` or `cover.png` in the book root. The page works without one, but the opening and link previews (WhatsApp, social, email) look much better with it.
- **Pillow** (`pip install pillow`) to resize the cover to 720 px automatically.

**Optional, to fill more sections**

| You want | Run first |
|---|---|
| A download button | `/ghost-writer:manuscript-final`, then `/ghost-writer:export-pdf` or `/ghost-writer:export-epub` |
| The explorable graph | `/ghost-writer:graph` (complete chapters sync automatically) |
| Podcast episodes | `/ghost-writer:podcast` (requires `ffmpeg` and `pip install piper-tts numpy`); install `ffprobe` (it comes with ffmpeg) for exact durations |

You can publish the site early and add these later. Each rebuild picks up whatever is new.

---

## 3. Generate the site

Run:

```
/ghost-writer:site
```

### Step 1 — Inventory
The skill checks the project and tells you in one line what the site will contain and what is missing, for example:
> The site will have: opening, the book, characters, podcast — 12 episodes, graph — 84 cards. Missing: download. Shall we write the texts?

### Step 2 — The texts, one block at a time
Claude drafts each block in the book's language and in your voice. You approve or change each one before the next.

1. **Opening**: kicker (genre and format, 3–7 words), tagline (the hook), subtitle, author.
2. **The book**: 2–3 short paragraphs, written like back-cover copy, not a summary.
3. **Download** (optional): which file, the button label, a short note (format, chapters included).
4. **Featured** (optional, 3–5 entries): main characters or key ideas. If the graph exists, they link to their cards.
5. **Podcast** (if you have episodes): section title and a short text.
6. **Graph** (if it exists): show the whole book, or only up to chapter N (useful for serial publication), plus the 6–8 cards it starts from.

Nothing beyond what you want public is revealed. Everything is saved in `site.yaml`.

### Step 3 — Build

```bash
python3 build_site.py --check   # validates, writes nothing
python3 build_site.py           # writes docs/
```

If a browser is available, Claude shows you a phone and a desktop screenshot. Otherwise, open `docs/index.html` in your browser.

---

## 4. `site.yaml` at a glance

You can edit it by hand, or ask `/ghost-writer:site` to change one block.

```yaml
title: "The Last Repair"
subtitle: "A novel"
author: "Jane Doe"
kicker: "A serialized science-fiction novel"
tagline: "In a city where nothing breaks anymore, Tom still fixes things."
book:
  title: "The book"
  paragraphs: ["…", "…"]
  download: {file: "manuscript/the-last-repair.pdf", label: "Download the book (PDF)", note: "A5, chapters 1–12"}
featured_title: "Characters"           # optional, overrides the preset title
featured:
  - {id: tom, role: "Repair technician", text: "…"}       # id = graph card
  - {name: "Deep focus", role: "Idea", text: "…"}         # no graph: use name
podcast: {title: "The podcast", text: "One chapter per episode, read aloud."}
graph:
  up_to_chapter: null                  # or N: show only chapters 1–N
  start: [tom, emma]
colors: {accent: "#6ee7a0", background: "#0e1116"}   # optional
labels: {}                             # optional: override any interface label
output: docs
```

To start from an empty skeleton: `python3 build_site.py --init`.

---

## 5. Publish on GitHub Pages (free)

1. Commit the `docs/` folder and push the project to a GitHub repository.
2. On GitHub: **Settings → Pages → Build and deployment → Deploy from a branch** → branch `main`, folder `/docs` → **Save**.
3. After about a minute the site is live at `https://<user>.github.io/<repository>/`.

Claude never pushes or changes repository settings unless you ask.

**Custom domain** (optional): in **Settings → Pages → Custom domain**, enter your domain and follow GitHub's DNS instructions.

### With a podcast
1. In `book.config.json`, set `podcast.base_url` to `https://<user>.github.io/<repository>/episodes`.
2. `python3 export_podcast.py feed`
3. `python3 build_site.py`, then commit and push.
4. Submit `https://<user>.github.io/<repository>/feed.xml` to Spotify for Creators, Apple Podcasts and other directories.

**Limits:** GitHub refuses files over 100 MB and Pages sites over 1 GB. At 96 kbps an episode takes about 0.7 MB per minute.

---

## 6. Keep it updated

The site is a derived file. You never edit `docs/` by hand.

| What changed | What happens |
|---|---|
| A chapter becomes complete | The graph syncs and the site is rebuilt automatically |
| New podcast episodes | The podcast skill rebuilds the site |
| A text on the page | `/ghost-writer:site` → change the block → rebuild |
| A new chapter goes public (serial) | Raise `graph.up_to_chapter`, rebuild |

After every rebuild: **commit + push `docs/`** to put it live.

---

## 7. Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: yaml` | `pip install pyyaml` |
| Build stops on graph errors | `python3 graph.py build`, fix what it reports |
| "placeholder without a value" | Fill that field in `site.yaml` (or rerun `/ghost-writer:site`) |
| Featured `id` not in the graph | Use `python3 graph.py find <name>` to get the right id, or use `name` instead |
| Download button missing | Check the `book.download.file` path (relative to the book root) |
| Podcast episodes don't play in apps | `podcast.base_url` is empty or wrong: fix it, rerun `export_podcast.py feed` and the build |
| Site 404 on GitHub | Pages must point to branch `main`, folder `/docs`; wait a minute after saving |
| Warning: site over 900 MB | Lower the podcast bitrate or host episodes elsewhere (GitHub Releases, Internet Archive) |

---

## 8. Next: get listed

Once the site is live, add your book to the gallery on [claudeghostwriter.com](https://www.claudeghostwriter.com/books/):

```
/ghost-writer:gallery
```

Use your site's URL as the book's link.

---

## Quick checklist

- [ ] `pip install pyyaml` (and `pillow`)
- [ ] Square cover in the book root
- [ ] (optional) PDF/EPUB exported, graph synced, podcast rendered
- [ ] `/ghost-writer:site` → approve the texts
- [ ] `python3 build_site.py --check` → `python3 build_site.py`
- [ ] Check `docs/index.html` on phone and desktop
- [ ] Commit + push `docs/`, enable Pages (`main` / `/docs`)
- [ ] (podcast) set `base_url`, regenerate feed, rebuild, push
- [ ] `/ghost-writer:gallery`
