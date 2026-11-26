# Ghost Writer — Claude Code Plugin

Collaborative ghost writing assistant for books and long-form writing projects.

**Official website: [claudeghostwriter.com](https://www.claudeghostwriter.com)**

Based on the writing method developed in [quantum_fatalism](https://github.com/simonediroma/quantum_fatalism) — a philosophical essay written in explicit collaboration between a human author and Claude.

---

## Installation

### From GitHub (available now)

Two commands:

```bash
# Step 1 — add the repo as marketplace
/plugin marketplace add simonediroma/claude-ghost-writer

# Step 2 — install the plugin
/plugin install ghost-writer@simonediroma-ghost-writer
```

### Manual install (.plugin file)

Download [ghost-writer-1.8.0.plugin](https://github.com/simonediroma/claude-ghost-writer/raw/main/dist/ghost-writer-1.8.0.plugin) and drag it into the Claude app (or upload it from **Settings → Plugins**).

### From the official marketplace (coming soon)

```bash
/plugin install ghost-writer@claude-plugins-official
```

### Test in locale

```bash
claude --plugin-dir ./ghost-writer
/ghost-writer:check
```

---

## The one command to remember

```bash
/ghost-writer:session-start
```

Run this whenever you open the project. It reads `project-state.md` (a compact digest updated at the end of every session) and briefs you in seconds — where you left off, what's pending, what to do today.

On the very first session, or if the digest is older than 7 days, it does a full read and regenerates the digest automatically.

---

## Quick Start — Macro Commands

Four commands cover the entire book lifecycle. Use these if you don't want to manage the sequence manually.

| Command | What it runs |
|---|---|
| `/ghost-writer:check` | **Run this first** — verifies installation and setup in 60 seconds |
| `/ghost-writer:wizard` | **Start here if you don't know where to begin** — conversational setup from scratch |
| `/ghost-writer:start` | Full onboarding — author interview + book definition + voice fingerprint |
| `/ghost-writer:chapter` | Full chapter cycle — dialogue + write + demolish + integrate |
| `/ghost-writer:review [file]` | Full persona review — all 5 readers + integrate |
| `/ghost-writer:finish` | Book closing — introduction + conclusion + final audit + manuscript |

**Not sure which to use?** → `/ghost-writer:wizard`

The atomic commands (below) remain available for authors who want to control the sequence directly.

---

## Skills

### Onboarding — run once, in order

| Command | What it does |
|---|---|
| `/ghost-writer:session-start` | Opens any session — reads full project state, suggests what to do today |
| `/ghost-writer:setup-author` | Interview: who you are, your authority, your emotional stake |
| `/ghost-writer:setup-book` | Brainstorm: premise, reader, structure — selects the genre preset |
| `/ghost-writer:setup-voice` | Defines tone of voice via interview + writing sample analysis |

### Writing cycle — repeated per chapter

| Command | What it does |
|---|---|
| `/ghost-writer:ask-before-writing` | Structured dialogue before writing anything |
| `/ghost-writer:freeflow` | For blocked authors — dump everything, plugin organizes |
| `/ghost-writer:write [section]` | Generates the section after dialogue is confirmed |
| `/ghost-writer:write [section] --quick` | Skips dialogue — asks one question, writes directly |
| `/ghost-writer:demolish [file]` | Hostile critical analysis — one objection at a time |
| `/ghost-writer:demolish [file] --light` | Fast stress-test — finds only the 3 most critical issues |
| `/ghost-writer:demolish-persona [persona]` | Demolition from a specific reader's perspective |
| `/ghost-writer:integrate` | Incorporates responses into the text — one change at a time |

### Consistency — periodic

| Command | When |
|---|---|
| `/ghost-writer:consistency-check` | Every 3-4 completed chapters |
| `/ghost-writer:revise [file]` | After integrate — grammar, punctuation vs style guide, timeline, character details, cross-chapter continuity |
| `/ghost-writer:revise --all` | Before `manuscript-final` — full editorial pass on the whole book |
| `/ghost-writer:rules [add "..."]` | Any time — store a writing rule (e.g. "never use a colon before a subordinate clause") in `style-rules.md` |
| `/ghost-writer:corrections print` | Before re-reading — review PDF with paragraph IDs in the margin |
| `/ghost-writer:corrections import [pdf]` | After re-reading — imports highlights/comments, notes or photos and applies them |

### Book graph — automatic

| Command | What it does |
|---|---|
| `/ghost-writer:graph` | Sync now (normally automatic) |
| `/ghost-writer:graph check` | Which chapters are waiting, suspended or aligned |
| `/ghost-writer:graph find [name]` | Show the card for a name |

See [Book Graph](#book-graph) below. Requires `pip install pyyaml`.

### Re-reading away from the computer

1. `/ghost-writer:corrections print` → `manuscript/review-[date].pdf`, every paragraph numbered (`3.12` = chapter 3, paragraph 12).
2. Read it on a tablet, phone or on paper and annotate the easiest way: highlights + comments in any PDF app, notes/dictation with the paragraph ID (`3.12 recieve → receive`), or photos of the marked-up printed pages.
3. `/ghost-writer:corrections import annotated.pdf` (or paste the notes / send the photos). Everything lands in `corrections.md`; typos are applied in one go, the rest one at a time. Notes like "always…" / "never…" become rules in `style-rules.md`.

Requires `pip install reportlab pymupdf`.
| `/ghost-writer:character-interview [name]` | Optional — before writing scenes with key characters |
| `/ghost-writer:character-check [name] [file]` | Optional — after writing scenes with profiled characters |

### Closing — run once, at the end

| Command | What it does |
|---|---|
| `/ghost-writer:write-opening` | Writes the introduction — last, after all chapters are complete |
| `/ghost-writer:write-closing` | Writes the conclusion — closes the arc |
| `/ghost-writer:manuscript-final` | Arc audit + assembles submission-ready manuscript |

### Podcast — optional, after the book is done

| Command | What it does |
|---|---|
| `/ghost-writer:podcast` | Turns the book into a narrated podcast: voice choice with samples, one script per chapter adapted for the ear (you approve each one), MP3 episodes + RSS feed |
| `/ghost-writer:podcast jingle` | Composes an original intro jingle offline (warm, upbeat, mysterious, playful, grime) or a seamless `grime-loop` beat made from real CC0 recordings |
| `/ghost-writer:podcast voice` | Pick or retune the narrator voice (speed, pauses) and optional character voices |

100% free and open source: [Piper](https://github.com/OHF-Voice/piper1-gpl) (offline TTS) + ffmpeg. Requires `pip install piper-tts numpy` and `ffmpeg`. Chapters are never modified — scripts live in `podcast/scripts/`.

### Utility

| Command | What it does |
|---|---|
| `/ghost-writer:status` | Project overview and suggested next step |

### Website — optional

| Command | What it does |
|---|---|
| `/ghost-writer:site` | Builds the book's website for GitHub Pages: opening, the book + download, characters or key ideas, podcast episodes, explorable graph |

See [Book Website](#book-website) below.

### Gallery — optional

| Command | What it does |
|---|---|
| `/ghost-writer:gallery` | Submits the book to the gallery on [claudeghostwriter.com](https://www.claudeghostwriter.com/books/): drafts the entry with you (title, genres, description, links, cover), validates it, then opens a pull request on the website repository with the GitHub CLI — or a pre-filled issue without it |

---

## Complete Workflow

```
ONBOARDING (once)
─────────────────────────────────────
session-start         → orient to the project (reads project-state.md digest)
setup-author          → who are you, your authority, your stake
setup-book            → what is the book + genre preset + first outline draft
setup-voice           → tone of voice via interview + sample analysis

PER CHAPTER (repeated)
─────────────────────────────────────
session-start                   → briefing: where we left off
ask-before-writing              → concept dialogue, one question at a time
  └─ blocked? → freeflow        → dump everything, plugin organizes
  └─ clear idea? → write --quick → skip dialogue, one question, write directly
write [section]                 → generates draft in author's voice
demolish [file]                 → hostile critique, logic and structure (7 vectors)
  └─ time-limited? → demolish --light  → 3 most critical issues only
demolish-persona editor         → structural diagnosis
demolish-persona target-reader  → does it work for the intended reader?
demolish-persona hostile-reader → does the argument hold under pressure?
integrate                       → incorporates all responses, one change at a time
revise [file]                   → grammar, punctuation, timeline, character details, continuity
  → chapter complete ✅
  → graph sync (automatic)       → new cards / re-anchored sources, one-line report

EVERY 3-4 CHAPTERS
─────────────────────────────────────
consistency-check     → term drift, contradicted claims, broken promises, tone arc
                         (streams findings as found; uses summaries first, full
                          text only on flagged chapters)

OPTIONAL (narrative books)
─────────────────────────────────────
character-interview [name]   → psychological profile before writing key scenes
character-check [name] [ch]  → behavioral consistency check after writing

CLOSING (once, at the end)
─────────────────────────────────────
write-opening         → introduction — written last
write-closing         → conclusion — resolves open promises
revise --all          → full editorial pass before assembly
manuscript-final      → arc audit + optional process note + assembled manuscript
```

---

## Genre Presets

Selected during `setup-book`. Adapts vocabulary, questions, and demolition logic.

| Preset | Central concept | Demolition focus | Graph cards |
|---|---|---|---|
| `essay` | Thesis | Falsifiability, circularity, scope | concepts, terms, theses, sources, people |
| `fiction` | Dramatic question | Motivation, consequence, earned change | characters, organizations, objects, places, concepts, terms, events |
| `manual` | Transformation | Evidence, context dependency, prerequisites | concepts, terms, procedures, tools, sources |
| `biography` | Interpretation | Evidence, selection bias, alternative readings | people, organizations, places, objects, events, sources, terms |
| `fable` | The moral | Earned ending, displacement, narrative necessity | characters, places, objects, events, concepts |
| `childrens-book` | The heart | Age appropriateness, child logic, pacing, read-aloud quality | characters, places, objects, events, terms |

---

## Reader Personas

Used with `/ghost-writer:demolish-persona` or run all five sequentially with `/ghost-writer:review`.

| Persona | What they find |
|---|---|
| `target-reader` | Accessibility, relevance, engagement |
| `hostile-reader` | Unsupported assertions, avoided objections |
| `domain-expert` | Technical gaps, overclaims |
| `editor` | Structure, pacing, prose problems |
| `out-of-target` | Unexplained jargon, invisible assumptions |

Each persona file opens with a `## Quick Summary` (role, focus, key questions, feedback style) that `demolish-persona` uses by default. The full behavioral profile is in the same file for deeper reads.

Custom personas: copy `personas/custom-template.md` and fill in.

---

## Book Graph

A map of everything that exists in the book — for fiction: characters, organizations, objects, places, concepts (rules, procedures, habits), terms (the glossary) and events, linked to each other and to the line of the chapter they come from. Card types depend on the preset (table above). Skill: `/ghost-writer:graph`; script: `graph.py`.

**It feeds itself — you never run it by hand.**

- Only chapters with `status: complete` enter the graph. Drafts are never analyzed, even when their version changes.
- The trigger is the chapter `version`: for each complete chapter, `graph.py check` compares the frontmatter version with the version analyzed in the graph. No hooks, no file watchers.
- The graph is born when the first chapter becomes `complete`.
- integrate, revise, corrections, retune, chapter and review end with a sync when they complete a chapter or change the version of a complete one. session-start, resume and status run `check` as a safety net (e.g. a chapter edited by hand and re-versioned).
- A chapter that goes back in progress is **suspended**: its cards stay at the analyzed version until it is `complete` again.
- No confirmation is asked: the graph is derived. Each sync ends with one line, e.g. *Graph synced (c4 v2.1): 3 new cards, 5 modified, 0 removed, 12 sources re-anchored · open questions: +2, 14 total.*

**A new version costs no re-read.** Every source is `c3:19` (chapter 3, line 19) plus a short exact quote. `graph.py` keeps a copy of the analyzed text, diffs it against the new one, finds each quote again and re-anchors the sources that moved. Claude reads only the changed paragraphs and the cards whose quote disappeared; facts the text no longer says are removed from the cards.

**Rules.** Nothing enters a card that the chapters don't say — not from the outline, not from book-memory. What the text doesn't say goes in `not_said`, doubts in `open`. Only `graph/cards/` is edited; views, index and JSON are regenerated. The script stops (and rolls back a commit) on non-existent ids, malformed sources, quotes not found at their line, or sources citing a chapter that is not analyzed.

**Who reads it.** revise, consistency-check, character-check and write read only the pertinent cards (`graph.py find <name>`, `graph.py find --chapter N`) instead of re-reading chapters. Never the whole graph.

```
graph/
  cards/<type>/<id>.yaml    the only files to edit
  view/…, INDEX.md          readable cards, backlinks, event chain per chapter (generated)
  graph.json                nodes + edges (generated)
  chapters.yaml             analyzed chapters and versions (generated)
  snapshots/cNN.md          analyzed text, for diffs (generated)
```

A card entry:

```yaml
traits:
  - {text: "Climbs the lighthouse at six every morning", source: "c1:8", quote: "alle sei del mattino, come ogni giorno"}
```

| Command | What it does |
|---|---|
| `python3 graph.py check` | Chapters to analyze, to re-analyze, suspended (read-only) |
| `python3 graph.py start` | Begins a sync: prints new chapters, changed paragraphs, moved and lost sources |
| `python3 graph.py commit N …` | Re-anchors sources, saves snapshot and version, rebuilds, prints the report |
| `python3 graph.py find <name>` / `--chapter N` | Pertinent cards (lazy reading) |
| `python3 graph.py apply patch.txt` | Adds/removes card entries without hand-editing YAML |
| `python3 graph.py build` / `validate` | Regenerate views / validate only |
| `python3 graph.py migrate grafo/` | Convert a graph in the earlier Italian format |

**Migrating an existing graph** (`grafo/` with `schede/`, `capitoli.yaml`, Italian fields, sources without quotes):

1. `python3 graph.py migrate grafo/` — converts folders and fields and derives each quote from the cited line. Sources it can't convert are listed in `graph/MIGRATION.md` and `graph/migration-quotes.yaml`; nothing is invented.
2. Fill `quote` (and `new_ref` if the fact is on another line) in `migration-quotes.yaml` — or ask Claude to — then `python3 graph.py fill-quotes graph/migration-quotes.yaml`.
3. `python3 graph.py build`. Delete `grafo/` once it builds.

Tests: `python3 tests/test_graph.py`.

---

## Book Website

`/ghost-writer:site` turns what the project already has into one page, ready to publish for free on GitHub Pages: `docs/index.html`, mobile first, no external fonts, scripts or trackers. All the content is in the HTML; JavaScript only draws the graph.

| Section | Appears when | Source |
|---|---|---|
| Opening | always | `site.yaml` + `cover.jpg` / `cover.png` |
| The book | always | `site.yaml → book` + optional download (PDF / EPUB) |
| Characters / People / Key ideas | `featured` is filled | `site.yaml → featured` (links to the graph card when `id` is set) |
| Podcast | MP3s exist | `podcast/scripts/` + `podcast/episodes/` + `podcast/feed.xml` (`/ghost-writer:podcast`) |
| Graph | `graph/` exists | the book graph: search, filters by type, event chain per chapter, open points, every card in full |

The skill drafts every text in the book's language and the author's voice, one block at a time, and saves it to `site.yaml`. For serial publication, `graph.up_to_chapter: N` shows only what happens up to chapter N. The site is rebuilt automatically after a graph sync and after new podcast episodes; publishing is a commit + push of `docs/`.

```bash
python3 build_site.py --init     # site.yaml skeleton from book.config.json
python3 build_site.py --check    # validate, write nothing
python3 build_site.py            # build docs/
```

Publish: repository **Settings → Pages → Deploy from a branch → `main` / `docs`**. With a podcast, set `podcast.base_url` to `https://<user>.github.io/<repository>/episodes` and run `python3 export_podcast.py feed` before the build. Requires `pip install pyyaml` (Pillow optional, for the 720 px cover).

---

## Core Principles

- **Claude formalizes, doesn't invent.** Concepts come from the author.
- **One question at a time.** Always.
- **No change without confirmation.** The author approves every modification to the text (the graph is derived and syncs on its own).
- **Demolition strengthens.** Every weakness found now is one less for hostile readers.
- **Genre adapts everything.** Vocabulary, questions, structure — all shaped by the preset.
- **Memory is explicit.** Every term, promise, and demolition cycle is written down.
- **The introduction is written last.**
- **The graph only knows what the chapters say.** Every card entry cites a line and quotes it.

---

## Project Files

Files the plugin reads and writes automatically. You don't need to edit these manually.

| File | Purpose | Updated by |
|---|---|---|
| `book.config.json` | Project metadata, voice profile, preset digest | setup-book, wizard, retune |
| `style-rules.md` | Punctuation conventions and the author's writing rules | write, integrate, revise, rules, corrections |
| `corrections.md` | Queue of corrections from re-reading sessions | corrections |
| `podcast/` | Episode plan, scripts, voices, MP3 episodes, `feed.xml` | podcast |
| `book-memory.md` | Defined terms, promises, claims, chapter log | write, integrate, consistency-check |
| `outline.md` | Chapter list with statuses | write, chapter, longform-upgrade |
| `voice-sample.md` | 3 paragraphs extracted from the last written chapter — style reference | write, integrate (silently) |
| `project-state.md` | Compact session digest — chapter counts, last step, open issues | session-start (silently, at end of session) |
| `demolition-history.md` | Book-level issue log, active + archived | demolish |
| `chapters/NN-slug.md` | Chapter text with frontmatter (title, version, claim, status, summary) | write, integrate |
| `sessions/` | Macro session state for resume support | chapter, review, finish |
| `memory/part-N.md` | Per-part memory (longform mode only) | longform-upgrade, write |
| `graph/cards/` | Book graph cards (the only graph files edited) | graph sync (from integrate, revise, corrections, retune, chapter, review, session-start, resume, status) |
| `graph/view/`, `graph/INDEX.md`, `graph/graph.json`, `graph/snapshots/` | Generated by `graph.py` — never edit | graph.py |
| `site.yaml` | Texts of the book website | site |
| `docs/` | The website (GitHub Pages) — generated by `build_site.py`, never edit | site, graph sync, podcast |

---

## Publishing to claude.com/plugins

1. Push to a public GitHub repo
2. Update `.claude-plugin/plugin.json` with your name and repo URL
3. Test locally: `claude --plugin-dir ./ghost-writer`
4. Submit at: `claude.ai/settings/plugins/submit`

---

## Credits

Original method: [Simone Di Roma — quantum_fatalism](https://github.com/simonediroma/quantum_fatalism)
License: MIT
