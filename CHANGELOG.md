# Changelog

## [1.7.0] — 2026-11-23

### Added

- **`/ghost-writer:proofread`**, **`/ghost-writer:help`**, **`/ghost-writer:export-epub`**, **`/ghost-writer:export-docx`**.
- Typewriter icon for the marketplace listing.

### Changed

- **Marketplace compliance**: the Python scripts (`export_pdf.py`, `export_epub.py`, `export_docx.py`, `export_podcast.py`, `graph.py`, `build_site.py`, `review_pdf.py`), `tests/` and `site/page.html` are removed from the repository. The export, graph, podcast and site skills carry the script spec and Claude generates the script on first use.
- `plugin.json`: only allowed fields.
- `consistency-check` adds a character check for fiction presets; `longform-upgrade` has a configurable threshold; `check` expects 37 skills and checks graph and website.
- All examples in skills, `style-rules.md` and the README are now in English (corrections, podcast, revise, rules). Italian remains only where it is a feature: the per-language style defaults in `revise` and the migration from the legacy `grafo/` format.

### Fixed

- README: marketplace install command points to `simonediroma/claude-ghost-writer`.

## [1.6.0] — 2026-11-15

### Added

- **`/ghost-writer:site`** — the book's website: one pre-generated, mobile-first page for GitHub Pages (`docs/index.html`). Opening with cover, the book with a download button, featured characters / people / key ideas, podcast episodes with RSS feed, and the explorable book graph (search, type filters, chapter event chains, open points, every card in full). Optional sections appear only when their source exists; texts are drafted with the author and saved in `site.yaml`; interface labels follow the book's language (en, it; override with `labels`).
- **`build_site.py`** — `--init`, `--check`, build. Standard library + PyYAML (Pillow optional). `graph.up_to_chapter` hides everything beyond a chapter for serial publication.
- **`site/page.html`** — the page template, generalized to every preset's card types.
- Graph cards accept `notes` (reading observations that are not errors); the migration maps the legacy card-level `note` to it.

### Changed

- Graph sync and the podcast skill rebuild the site when `site.yaml` exists.
- `check` expects 33 skills and validates `site.yaml`.

## [1.5.0] — 2026-11-15

### Added

- **`/ghost-writer:graph`** — the book graph: cards for characters, organizations, objects, places, concepts, terms and events (fiction), or concepts, terms, theses, sources and people (essay), and the other presets' types, linked to each other and to the chapter line they come from. Only what the chapters say enters a card; `not_said` and `open` hold gaps and doubts.
- **`graph.py`** — `check`, `start`, `diff`, `commit`, `build`, `validate`, `find`, `apply`, `migrate`, `fill-quotes`. Standard library + PyYAML. Stops on non-existent ids, malformed sources, quotes not found at their line, sources citing chapters that are not analyzed; a failed commit is rolled back.
- **Self-feeding**: only `status: complete` chapters are analyzed; the trigger is the chapter `version` against the analyzed one. The graph is born with the first complete chapter. A chapter back in progress is *suspended*: its cards stay at the analyzed version until it is complete again.
- **Incremental update**: every source is `cN:line` + a short quote. A snapshot of the analyzed text gives the diff; moved sources are re-anchored automatically, only the changed paragraphs and the sources whose quote disappeared are handed to Claude.
- **Migration** from the earlier Italian format (`grafo/schede/`, `capitoli.yaml`): quotes derived from the cited lines, sources that cannot be converted listed in `graph/MIGRATION.md` and `graph/migration-quotes.yaml`, never invented.
- **`## graph adaptations`** in the fiction, biography, essay, manual, childrens-book and fable presets: card types per genre.

### Changed

- integrate, revise, corrections, retune, chapter, review end with a graph sync; session-start, resume, status run `graph.py check` as a safety net.
- revise, consistency-check, character-check and write read the pertinent cards instead of re-reading chapters when `graph/` exists; longform lazy reading covers the graph.
- integrate sets `status: complete` in the chapter frontmatter when the author declares the final version; revise and retune increment `version` when they change a chapter.
- `check` expects 32 skills and checks `graph.py`, PyYAML and the graph.

## [1.4.0] — 2026-11-01

### Added

- `grime-loop`: `--bassline` adds a 4-bar bass riff with its own level (stays audible with a low `--bed`), `--bass-sound piano|organ` picks a real Steinway or pipe-organ pedal bass (VCSL). `--bass-style dub` plays a sparse dub/steppers bass instead of the grime riff. `--bass-sound electric` uses a real electric bass (Karoryfer Growlybass, CC0) with light overdrive; `--bass-style punk` drives it in straight eighths.

## [1.3.0] — 2026-10-23

### Added

- **`/ghost-writer:podcast`** — turns the book into a narrated podcast, one episode per chapter. Narrator voice chosen from audio samples rendered from the book's own prose, tunable speed and pauses, optional per-character voices for dialogue. Each chapter is adapted into a script for the ear (lists, visual references, numbers and abbreviations) and approved by the author before rendering. Chapters are never modified.
- **`export_podcast.py`** — `voices`, `sample`, `build`, `feed`. Free and open source only: Piper TTS (offline) + ffmpeg. MP3 episodes with ID3 tags, optional intro/outro music, RSS `feed.xml`.
- **Intro jingle** — `export_podcast.py jingle` composes an original sting (numpy, no samples, no licenses) in 4 styles picked from the preset, plus `grime` (140 bpm, square bass, sci-fi whistle lead) and `grime-loop` (seamless 8-bar beat, real CC0 recordings from VCSL for drums, piano, cymbals and FX; only the whistle is synthesized and sits on top of the mix, with a digital bit-crushed delay; dorian, not horror); voice starts over the jingle's tail (`intro_overlap`). Optional AI route: prompt written for ACE-Step (Apache-2.0, local).
- **`podcast`** section in `book.config.json`.

### Changed

- `check` expects 31 skills.

## [1.2.0] — 2026-10-10

### Added

- **`/ghost-writer:revise`** — editorial revision pass: grammar and spelling, punctuation against the book's style guide, event timeline, per-character factual details, and continuity of details reused across chapters. Works on one chapter or the whole book (`--all`), with `--only` to select checks. Grammar/punctuation fixes can be applied in bulk; timeline/character/continuity issues are always resolved one at a time.
- **`style-rules.md`** — punctuation conventions + the author's writing rules (with right/wrong examples and scope). Read by `write`, `integrate` and checked by `revise`.
- **`/ghost-writer:rules`** — add, list, edit, remove and infer rules in natural language.
- **`/ghost-writer:corrections`** — re-reading workflow away from the computer: review PDF with paragraph IDs in the margin (`review_pdf.py export`), import of highlights/comments from the annotated PDF (`review_pdf.py import`), parsing of free-form notes, dictation and photos of marked-up pages. Queue in `corrections.md`; general notes become rules.
- **`## Timeline`** and **`## Continuity Ledger`** in `book-memory.md` — populated by `write`, `integrate` and `revise`.

### Changed

- `finish` runs `revise --all` before `manuscript-final`.
- `write` and `integrate` respect `style-rules.md`.
- `check` expects 30 skills.

## [1.1.0] — 2026-06-06

### Added

- **Quick-Write mode** (`--quick` flag on `/ghost-writer:write` and `/ghost-writer:chapter`): skips the structured `ask-before-writing` dialogue and asks a single 2-3 sentence description instead. For authors who already have a clear idea or want a fast first draft to react to.
- **Light Demolish mode** (`--light` flag on `/ghost-writer:demolish`): skips the full 7-category vulnerability mapping and identifies only the 3 most critical issues (central claim weakness, logical gap, predictable objection). Phases 3-5 run normally.
- **`project-state.md`**: compact project digest written silently at the end of every session. `session-start` reads this file on return visits instead of loading 7 source files — dramatically faster session opening.
- **`preset_digest` in `book.config.json`**: after `setup-book` or `wizard` determines the genre preset, a compact digest (identity, key vocabulary, demolish vectors, write structure) is extracted and stored in config. `ask-before-writing` and `chapter` use the digest instead of loading the full preset file.
- **Quick Summary sections in all 5 persona files**: each persona now opens with a `## Quick Summary` (role, focus areas, key questions, feedback style). `demolish-persona` reads only this section by default — reads the full profile only on first run or explicit request.
- **Chapter `summary` field in frontmatter**: `write` now silently generates a 3-5 sentence summary and writes it to the chapter frontmatter after each draft. This enables `consistency-check` to audit with summaries first and only read full chapter text on flagged issues — even without `longform-upgrade`.
- **Demolition archiving**: `demolish-persona` now archives resolved issue logs from complete chapters into a `## Archived Cycles` section of `demolition-history.md`. Active sections stay lean regardless of book length.

### Changed

- **`session-start`**: now shows the orienting line as soon as the book title and last action are known — does not wait for all file reads to complete. First meaningful output arrives immediately.
- **`consistency-check` (non-longform mode)**: now reads chapter `summary` fields first, drills into full text only for flagged chapters. Opening paragraphs only for tone drift checks. Mirrors the lazy-reading strategy of longform mode — no `longform-upgrade` required.
- **`consistency-check` output**: findings are now surfaced category by category as each check completes (CRITICAL first, then SIGNIFICANT, then MINOR), not held for a single final block.
- **`demolish` Phase 0**: reads `demolition-history.md` active sections only (skips `## Archived Cycles` and Full Log entries for complete chapters).
- **Language block condensed** in all 27 SKILL.md files: from ~50 tokens to ~18 tokens per skill invocation. Canonical wording preserved in `plugin.json → shared_instructions`.

### Fixed

- `session-start` would read the full preset file unnecessarily on return visits — now reads `preset_digest` from config if available.

## [1.0.0] — 2026-05-10

### Added

- **27 skills** covering the complete book writing lifecycle
- **6 genre presets**: essay, fiction, manual, biography, fable, children's book
- **5 reader personas** for demolition: target-reader, hostile-reader, domain-expert, editor, out-of-target
- **4 macro commands** for authors who prefer a guided workflow: `/ghost-writer:start`, `/ghost-writer:chapter`, `/ghost-writer:review`, `/ghost-writer:finish`
- **Session resume system** (`/ghost-writer:resume`) — always knows where you left off
- **Wizard** (`/ghost-writer:wizard`) — conversational setup for authors starting from scratch
- **Freeflow** (`/ghost-writer:freeflow`) — for blocked authors; dumps raw thoughts, plugin organizes
- **Long-form mode** (`/ghost-writer:longform-upgrade`) — switches to per-part memory strategy for 10+ chapter books
- **Character system** — interview and consistency check for narrative books
- **PDF export** (`/ghost-writer:export-pdf`) — generates submission-ready PDF via ReportLab
- **Multi-language support** — all output respects the `language` field in `book.config.json`
- **Demolition history** — book-level pattern tracking across all chapters
- **Consistency check** — periodic audit for term drift, contradicted claims, broken promises, and tone arc

### Method

Based on the writing method developed in [quantum_fatalism](https://github.com/simonediroma/quantum_fatalism), a philosophical essay written in explicit collaboration between a human author and Claude.

Core principles: Claude formalizes, doesn't invent. One question at a time. No change without confirmation. The introduction is written last.
