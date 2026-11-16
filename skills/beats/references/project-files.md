# RAMA project files

Every RAMA skill works from the same small set of files. This page says what
they are, how to find them, and how to write back to them. Read it before you
touch a project.

## Where the project lives

Look in this order and use the first place that has project files:

1. The folder the author named in the request.
2. The current working directory (Claude Code / Cowork).
3. `/mnt/project/` (a claude.ai Project), then `/mnt/user-data/uploads/`.

**Read-only projects.** Files in a claude.ai Project (`/mnt/project/`) cannot
be changed in place. When a skill needs to update one of them, write the full
updated file to `/mnt/user-data/outputs/` under **the same filename**. Then tell
the author which Project file to replace, one line per file. Never hand over a
partial file as a "patch": the author replaces the whole file.

## The files

`<Title>` is the book title exactly as the author writes it (e.g. *The Shape of
the Sea*). Filenames vary between books, so match on the role word and don't
require the exact punctuation. `The Shape of the Sea — Outline.md`,
`The Shape of the Sea - Outline.md` and `Outline.md` are all the outline. When
two files could fill the same role, ask which one is canonical, and record the
answer in the RAMA Log.

| Role | Typical name | Required | Notes |
|---|---|---|---|
| Synopsis | `<Title> — Synopsis.md` | yes | 500–750 words. Often **not a separate file**: look for a `## Synopsis` section in the outline or the story bible first. |
| Outline | `<Title> — Outline.md` | yes | Full chapter outline. Each chapter is a heading (`### Chapter V. In Which…`) with its beats, notes and tracking underneath. |
| Style guide | `<Title> Style Guide.md` | yes | Language, POV, voice, banned constructions, chapter-head form, section-break mark, revision checklist. **This document governs the prose.** |
| Story bible | `<Title> — Story Bible.md` | if series or complex | Characters, setting, timeline, mythology, open questions. |
| Manuscript | `<Title>.md` | once writing starts | **One file** holding every written chapter in order. RAMA's compose skill adds to it. |
| Beats | `<Title> — Beats.md` | created by beats | One section per chapter: `## Chapter 5 — <chapter head>`. |
| RAMA Log | `<Title> — RAMA Log.md` | created by config | Project state and RAMA's memory (see below). |
| Glyphs | `glyphs/` folder | for compile | `Chapter_head.png`, `divider.png` (optional per-break `divider<TAG>.png`). |
| Characters | `characters/<Name>.md` | optional | Deep profiles from `character-interview`. |
| Corrections | `<Title> — Corrections.md` | optional | Queue used by `corrections`. |

Other `.md` files in the folder (old style guides, research notes, sample
chapters, earlier drafts) are **reference material**. Read them when they are
relevant, but never treat them as canonical unless the RAMA Log says so.

## Chapter numbering

Authors call chapters by **ordinal number**: `5` means the fifth chapter in the
outline, counting continuously through Parts and whatever the numbering style
(`Chapter V`, `Chapter Five`, `5`). Prologue/epilogue: ask how to number them
the first time, then record the rule in the RAMA Log.

Accept `5`, `V`, `ch5`, `chapter 5`. A range is `5-7`. `all` means every chapter
in the manuscript.

## The manuscript format

The manuscript is a single Markdown file in the shape the compile step
(`manuscript-docx`) expects:

```markdown
Title: The Shape of the Sea
Author: Michael Weintraub

# Part One: The Letter and the Rescue

## Chapter I: In Which a Key Falls upon My Table

First paragraph…

* * *

Next scene…
```

- **Every chapter is a level-2 heading** with the form `## <Designation>: <Chapter head>`.
  The designation (`Chapter I`, `Chapter One`, `Chapter 1`) and the chapter-head
  style follow the style guide. The colon splits the designation from the
  chapter head in the .docx, so use a colon even when the style guide prints a
  period (`CHAPTER VII. In Which…`), and record that choice in the RAMA Log.
- Part headings, if the book has Parts, are level-1 (`# Part One: …`) and sit
  directly before the first chapter of the Part. Frame passages and other text
  that opens a Part go under the Part heading, before the chapter heading.
- A scene break is the mark the style guide names (default `* * *`) alone on a
  line. The first scene of a chapter takes no break.
- Epigraphs and quoted documents (letters, notices, Scripture) go in
  `> blockquote` so they set as Quoted Text.
- No word counts, notes, beats, logs or HTML comments in the manuscript. It
  must compile as-is at any moment.

When you find a chapter in the manuscript, match the heading text, and use the
chapter's position among the level-2 headings as its number.

### Paragraph IDs

Findings and corrections cite places as `ch.para`, e.g. `5.12`. The chapter
is the ordinal number. Paragraphs are the blank-line-separated blocks after
the chapter heading, counted from 1. Skip headings and scene-break lines, and
count each blockquote (an epigraph, a letter) as a paragraph. Text that opens a
Part, before its first chapter, is cited `P2.3` (Part 2, paragraph 3). The
`corrections` skill's review PDF numbers paragraphs exactly this way, so IDs
match between a check report and a printed review copy.

## The RAMA Log

`<Title> — RAMA Log.md` is RAMA's memory. Every skill reads it first and updates
it last. Keep it short and factual. Sections, in order:

```markdown
# <Title> — RAMA Log

## Project
- Title / Author / Series (book N of M, if any)
- Files: role → filename, one per line (canonical choices)
- Chapter heading form: `## Chapter I: In Which…` (roman / words / digits)
- Part headings: yes/no and form
- Scene break mark: `* * *`
- Target length: total words; per-chapter targets if the outline gives them
- Platform notes (e.g. claude.ai Project, read-only files)

## Decisions
Dated one-liners for every answer the author gave in a survey that changes
the book: `2026-11-16 · ch 5 · Sharp learns of the key from Keziah, not Harold.`
Decisions here override the outline and story bible until those files are
updated, and every skill must respect them.

## Chapter Status
| # | Chapter head | Beats | Draft | Words | Last check |
|---|---|---|---|---|---|

## Continuity Ledger
Concrete facts established in the written text that later chapters must keep:
`ch 3 · the shed door opens seaward, latch on the outside.` Add to it every
time a chapter is composed or a fix is applied.

## Open Threads
Promises, setups and questions the text has raised and not yet paid off,
with the chapter that raised them and the chapter the outline pays them off in.

## Check History
`2026-11-20 · check 5-7 · 14 findings, 12 fixed, 2 kept as intentional.`
```

## Writing back

- Change only what the skill is responsible for. Never rewrite the author's
  outline, style guide or bible as a side effect. When a survey answer
  contradicts one of them, log it under **Decisions** and offer to update the
  source file, one change at a time.
- Keep the author's filenames, headings and formatting conventions.
- After a write in a writable folder, say which files changed in one line.
