# Changelog

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
