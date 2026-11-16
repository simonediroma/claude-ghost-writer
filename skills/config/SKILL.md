---
name: config
description: Configure a RAMA book project. Finds and checks the synopsis, outline, style guide and story bible (and the manuscript, if writing has started), asks the author survey questions about any gaps or contradictions, and writes the RAMA Log. If files are missing, interviews the author to build them, starting from a concept or adapting an older style guide. Run this first on every new book, and again whenever the project files change a lot. Usage /rama:config.
---

# RAMA: Config

Sets up a book project so the other RAMA skills (`beats`, `compose`, `check`,
`compile`) can work from it.

Before starting, read:
- `references/project-files.md`: which files make up a project, where to find them, and the RAMA Log format.
- `references/survey.md`: how to ask the author questions (three answers plus a write-in).

## Step 1: Inventory

Find the project folder (see `project-files.md → Where the project lives`) and
list every file in it. Sort each file into a role: synopsis (including a
`## Synopsis` section inside another file), outline, style guide, story bible,
manuscript, glyphs, characters, reference. If a RAMA Log already exists,
read it first; this run is an update, not a fresh setup.

Show the inventory in one short table and say right away which path you are
on:

- **All required files present** → Step 2 (Verify).
- **Some present** → Step 2 for what exists, then Step 3 for the rest.
- **Nothing (or only notes and a concept)** → Step 3 (Build).

If two files could fill one role (two style guides, say), ask in the first
survey which one is canonical. One may be an old guide to adapt; see Step 3.

## Step 2: Verify the files

Read every canonical file in full. Check each one against what the other
skills need from it:

**Synopsis**
- Exists, and is about 500–750 words. Shorter is fine if it covers the ending.
- States the ending. A synopsis that hides the ending can't guide beats.

**Outline**
- Every chapter is findable as a heading, in order. Count them, and check the
  count against any overview table in the outline.
- Each chapter has enough to beat from: what happens, whose scene, where it
  ends. Flag any chapter that is only a title.
- Parts (if any) are marked, and the chapter-head form is consistent.
- Word targets, if given, add up to the stated total.

**Style guide**
- Names the POV, tense and narrator.
- Gives the chapter-heading form and the scene-break mark. If it doesn't, ask.
- Lists banned constructions or a revision checklist. RAMA's `check` skill
  turns these into its checklist. If there is no checklist, offer to draft one
  from the guide's rules.

**Story bible** (if present)
- Characters have names, roles and the facts later chapters will rely on (age,
  relationships, appearance).
- The timeline is datable when the book is historical.
- List its own `Open questions`. Each one is a candidate survey question.

**Cross-file consistency**
- Names, dates, ages and places agree across the synopsis, outline and bible.
- The outline delivers the synopsis: the same ending and the same turns.
- The outline obeys the style guide (chapter-head form, frame rules, POV).
- Decisions the outline marks as open ("decide in drafting", "Decisions for
  the author", "To verify") are listed and ready to ask about.

**Manuscript** (if present)
- Chapters parse as level-2 headings in the format in `project-files.md`. If
  the format differs, show the difference and offer to convert it (with the
  author's approval) or record the actual format in the RAMA Log.
- Map each written chapter to its outline chapter and count its words.

Report what you found, grouped as **Blocking** (a later skill can't work
without a fix), **Contradictions** (two files disagree) and **Gaps** (something
is thin or open). Keep each item to one line, citing file and heading.

## Step 3: Survey

Turn every Blocking item, Contradiction and open decision into survey
questions (`survey.md`). Order them by how early in the book they matter. Ask
in batches of up to four, recording answers as you go.

Examples of good config questions (for a book like the sample):
- *The outline gives Chapter I as ~3,000 words, and the Part One table implies
  ~3,600 per chapter. Which target should compose aim for?*
- *The front matter lists an optional "To the Reader." Include it?*
- *The style guide sets `CHAPTER VII. In Which…` with a period. RAMA needs a
  colon in the manuscript heading to split it in the .docx. OK to use
  `## Chapter VII: In Which…` in the manuscript?*

Settle only what blocks writing. Things that matter only for one chapter can
wait until `beats` for that chapter. List them under **Open Threads** so
`beats` asks them at the right time.

## Step 3 (alternate): Build missing files

Build only the files that are missing, one at a time, in this order:
synopsis → outline → style guide → story bible. Each depends on the one before
it. Use survey rounds to draw the material out of the author. Write a draft,
show it, revise it on the author's notes, and save it only after they approve.

**Synopsis.** Start from whatever the author has: a concept, a paragraph, a
pitch. Survey for genre and comparables, protagonist and want, the central
turn, the ending, and the narrator's relation to events. Draft 500–750 words in
present tense, with the ending stated.

**Outline.** Survey for structure (Parts or not, chapter count, total length),
then go Part by Part. Each chapter gets a heading in the book's chapter-head
form, a one-line function, 4–8 bullet beats, and an *Ends on:* line. Add a
**Tracking** section only if the book has things to track (a calendar, a key
object, a secret).

**Style guide.** If the author has an **old style guide to adapt**, read it
first. Survey only the sections that must change for this book (period,
narrator, POV, register, banned constructions particular to the voice), and
keep the rest as written. Otherwise survey for POV and tense, register
(give three short sample passages in different registers and ask which is
closest), dialogue punctuation, chapter-head form, the section-break mark,
and banned constructions. Always end the guide with a **Revision Checklist**.
`check` runs it.

**Story bible.** Only if the book is part of a series or has a complicated
plot or backstory. Ask in the first survey whether one is wanted.
Characters (name, role, age, relationships, look, want/need), setting and
timeline, rules of the world, and open questions.

Name each new file per `project-files.md` and put it in the project folder.
In a read-only claude.ai Project, write it to `/mnt/user-data/outputs/` and
ask the author to add it to the Project.

## Step 4: Write the RAMA Log

Create or update `<Title> — RAMA Log.md` in the format in `project-files.md`:
the Project block, every Decision from this run, the Chapter Status table (one
row per outline chapter, filled in for chapters already written), a
Continuity Ledger seeded from the story bible's hard facts, and Open Threads.

If `glyphs/` is missing, note it under Project as
`Glyphs: none yet. compile will offer to draw them.` Don't create glyphs here.

## Step 5: Hand off

Finish with three lines at most:

> Project configured: [N] chapters, [M] written. Files: [list].
> [K] decisions logged; [J] open threads will come up in `beats`.
> Next: `/rama:beats [first unwritten chapter]`.
