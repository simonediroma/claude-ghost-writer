---
name: compile
description: Compile a RAMA manuscript into .md, .docx and .epub. Checks the manuscript is clean and complete, makes sure chapter-head and scene-break glyphs exist in glyphs/ (and offers to draw them if not), then builds the Word file with the manuscript-docx skill and the ebook with the manuscript-epub skill. Usage /rama:compile, or /rama:compile docx|epub|md to build one format.
---

# RAMA: Compile

Produces the book files from `<Title>.md`. The formatting itself is done by two
companion skills, **manuscript-docx** and **manuscript-epub**. RAMA prepares the
input, settles the glyphs, runs both, and checks the results.

Before starting, read `references/project-files.md` and `references/survey.md`.

## Companion skills

| Output | Skill | In Claude Code / Cowork | In claude.ai |
|---|---|---|---|
| `.docx` | manuscript-docx | `Skill` tool: `anthropic-skills:manuscript-docx` (or plain `manuscript-docx`, whichever is installed) | invoke the **manuscript-docx** skill |
| `.epub` | manuscript-epub | `Skill` tool: `anthropic-skills:manuscript-epub` | invoke the **manuscript-epub** skill |

Load each skill's instructions and follow them for its part. They own trim,
styles, glyph placement, small caps, cover and validation. Don't reimplement
any of it here. If either skill is missing, say so and build only what you can
(`.md` always works).

## Arguments

`/rama:compile` builds all three. `/rama:compile docx`, `epub` or `md` builds
one. Options are passed through: `--trim 6x9`, `--no-glyphs` (draft for an
editor).

## Step 1: Pre-flight

Read the RAMA Log and the manuscript. Report, in one block:

- Chapters present versus the outline (`22 of 25`). If the book is incomplete,
  ask: **Compile what exists as a draft (Recommended) / Cancel.**
- Chapters never checked, or with open Critical findings in the Check Report.
  Ask: **Compile anyway / Run /rama:check first.**
- Format problems that would mis-set the book: a chapter heading without the
  colon split, a stray note, an HTML comment or word count, a scene-break mark
  that differs from the style guide's, text before the first heading other
  than `Title:` / `Author:` and front matter. Offer to fix each one in the
  manuscript (with approval), or work around it in the compile copy only.
- `Title:` and `Author:` lines are present. If they're missing, take them
  from the RAMA Log and confirm.
- Front matter the outline or style guide calls for (title page wording,
  epigraph, "To the Reader"). Make sure it's in the manuscript in the right
  form, and ask before adding anything.

## Step 2: Glyphs

Look in `glyphs/` in the project folder (and any glyph folder the RAMA Log
names) for:

- a **chapter head**: a file whose name contains `chapter` (e.g. `Chapter_head.png`)
- a **scene divider**: a file whose name contains `divider` (e.g. `divider.png`;
  per-break variants like `dividerPOL.png` are fine)

**Both present** → show their names and use them. **Either missing** → ask with
a survey:

> No [chapter-head / divider] glyph in `glyphs/`. What should compile do?
> - **Draw a set for this book (Recommended)**: I'll show you a contact sheet of motifs.
> - **I'll supply art**: I'll wait for you to add files to `glyphs/`.
> - **Compile with text markers**: `* * *` stays as text (fine for an editor's draft).

To draw a set, use manuscript-docx's glyph generator (its `scripts/make_glyph.py`
and `references/glyphs.md`):

1. Render the contact sheet of all motifs and show it.
2. Survey: offer three motifs **chosen for this book**, reading the style guide's
   tone and the story bible's images and objects. (A sea book might get
   `wave`, `key` or `asterism`; a book that wants to feel like an old volume,
   `triple`.) Do this once for the chapter head and once for the divider.
   The author can write in another motif or `rule`.
3. Draw the two chosen glyphs into `glyphs/` as `Chapter_head.png` and
   `divider.png`, show them, and confirm.
4. Record the glyph choice in the RAMA Log under Project.

In a read-only claude.ai Project, draw into `/mnt/user-data/outputs/glyphs/`
and tell the author to add the two PNGs to the Project for next time.

## Step 3: Build

Output folder: `build/` in the project folder (Code), or
`/mnt/user-data/outputs/` (claude.ai). File stem: the book title,
e.g. `The Shape of the Sea`.

1. **.md**: write `build/<Title>.md`: the manuscript exactly as compiled
   (front matter included, nothing RAMA-internal). This is the clean
   distributable Markdown.
2. **.docx**: run manuscript-docx on `build/<Title>.md`:
   - Settle **trim** with a survey (**US Letter for an editor / 6x9 / 7x10**),
     unless the RAMA Log already records one or the author passed `--trim`.
     Record the answer.
   - Pass `--glyph-dir glyphs` (or `--no-glyphs`).
   - Do the **dry run first** and read the report. Check the chapter count
     against Step 1, and that every divider and every Quoted Text call is
     right (epigraphs, letters, Scripture). Fix bad calls with `--quote` /
     `--no-quote`, as that skill describes, not by editing the .docx.
   - Note: every heading becomes a chapter section in the .docx, so Part
     headings set as their own section. Confirm with the author that this is
     wanted the first time. If not, record the alternative in the RAMA Log.
   - Convert, render a few pages and look at them, as that skill directs.
3. **.epub**: run manuscript-epub on the **.docx just built** (its preferred
   input, which keeps the small caps and glyphs). It will ask for a cover.
   If the author has none, build the interior-only draft it offers and say
   clearly that the file can't be uploaded to a store without one.

## Step 4: Report

```
Compiled The Shape of the Sea · 25 chapters · 89,240 words
  build/The Shape of the Sea.md
  build/The Shape of the Sea.docx   6x9 · glyphs: Chapter_head.png, divider.png · 25/25 recto
  build/The Shape of the Sea.epub   EPUBCheck: pass · cover: yes
```

Give any warnings from either skill in one line each. Add to the RAMA Log:
`<date> · compiled <formats> · <chapters> ch · <words> words`.
