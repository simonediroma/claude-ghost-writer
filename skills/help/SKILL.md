---
description: Quick reference for all available Ghost Writer commands. Shows every skill grouped by workflow phase, with a one-line description and usage example. Run any time you forget what's available or what to do next.
---

# Skill: Help

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Displays all available Ghost Writer commands, grouped by workflow phase. Read-only — nothing is created or modified.

---

## Before Starting

Try to read `book.config.json`. If it exists:
- Use its `language` for output
- Read `book_profile.preset` to show preset-specific notes
- Note which onboarding phases are complete to highlight the logical next step

If `book.config.json` does not exist, output in English.

---

## Output

```
GHOST WRITER — COMMAND REFERENCE
─────────────────────────────────────────────────────────

SETUP (run once at the start of a project)

  /ghost-writer:check            Verify installation and project readiness
  /ghost-writer:wizard           Guided setup from scratch (conversational)
  /ghost-writer:start            Full onboarding: author → book → voice
  /ghost-writer:setup-author     Step 1: author background and authority
  /ghost-writer:setup-book       Step 2: premise, structure, genre preset
  /ghost-writer:setup-voice      Step 3: voice fingerprint from your writing

─────────────────────────────────────────────────────────

WRITING (run for each chapter)

  /ghost-writer:chapter          Full cycle: dialogue → draft → critique → integrate
  /ghost-writer:ask-before-writing   Structured concept dialogue before drafting
  /ghost-writer:freeflow         For blocked authors: dump everything, I organize
  /ghost-writer:write [section]  Generate a draft section in your voice
  /ghost-writer:demolish [file]  Hostile critique: find the holes
  /ghost-writer:demolish-persona [persona] [file]   Critique from a reader perspective
  /ghost-writer:integrate        Apply demolition feedback to the text

─────────────────────────────────────────────────────────

REVIEW & QUALITY

  /ghost-writer:review [file]    Full persona review (all 5 readers)
  /ghost-writer:consistency-check   Cross-chapter audit: drift, contradictions, broken promises
  /ghost-writer:proofread [file] Grammar, style, rhythm, and repetition check
  /ghost-writer:character-interview [name]   Build a character's psychological profile
  /ghost-writer:character-check [name] [file]   Verify character consistency in a scene

─────────────────────────────────────────────────────────

FINISHING (run once at the end)

  /ghost-writer:finish           Full closing: introduction → conclusion → audit → manuscript
  /ghost-writer:write-opening    Write the introduction (run after all chapters are done)
  /ghost-writer:write-closing    Write the conclusion
  /ghost-writer:manuscript-final Arc audit + assemble submission-ready manuscript

─────────────────────────────────────────────────────────

EXPORT

  /ghost-writer:export-pdf       Export manuscript as PDF (cover, TOC, clean layout)
  /ghost-writer:export-epub      Export manuscript as EPUB (for e-readers)
  /ghost-writer:export-docx      Export manuscript as DOCX (for editors and publishers)

─────────────────────────────────────────────────────────

STATUS & UTILITIES

  /ghost-writer:session-start    Opening briefing: where you left off, what's pending
  /ghost-writer:resume           One-line status + single next-action recommendation
  /ghost-writer:status           Full project overview with chapter statuses
  /ghost-writer:retune           Adjust voice profile mid-project
  /ghost-writer:longform-upgrade Activate long-form mode (recommended at 10+ chapters)
  /ghost-writer:help             Show this reference

─────────────────────────────────────────────────────────

READER PERSONAS (use with demolish-persona or review)

  target-reader     Your ideal reader — accessibility, relevance, engagement
  hostile-reader    Strongest critic — unsupported claims, avoided objections
  domain-expert     Specialist — technical gaps, overclaims
  editor            Structural reader — pacing, prose, arc
  out-of-target     Outsider — jargon, invisible assumptions

─────────────────────────────────────────────────────────
```

After the reference, check the project state and suggest the most useful next step:

If onboarding is incomplete:
> → Next step: `/ghost-writer:start` to set up author profile, book structure, and voice.

If chapters are in progress:
> → Next step: `/ghost-writer:resume` to see exactly where you left off.

If the project looks ready to export:
> → Next step: `/ghost-writer:finish` to close the book and prepare the manuscript.

If `book.config.json` doesn't exist:
> → No project found. Run `/ghost-writer:wizard` to start a new book from scratch.
