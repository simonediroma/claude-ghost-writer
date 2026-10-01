# Changelog

## [Unreleased]

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
