---
name: corrections
description: Collect and apply the corrections the author makes while rereading a RAMA book away from the computer. Prints a review PDF with paragraph IDs in the margin (5.12 = chapter 5, paragraph 12), imports highlights and comments from the annotated PDF, or parses free-form notes (phone notes, dictation, photos of marked-up pages). Everything goes into the Corrections file and is applied one at a time with the author's OK. Usage /rama:corrections print [5-7], /rama:corrections import [annotated.pdf], /rama:corrections.
---

# RAMA: Corrections

*Adapted from ghost-writer's `corrections` and `review_pdf.py` (MIT, Simone Di Roma).*

Read `references/project-files.md` and `references/survey.md` first.

The queue lives in `<Title> — Corrections.md` in the project folder.
`review_pdf.py` (in this skill's folder) does the PDF work.

## The rereading workflow (explain once, the first time)

> 1. `/rama:corrections print` gives you `review/review-<date>.pdf`, with a paragraph ID in the margin of every paragraph.
> 2. Read it anywhere and mark it up however is easiest:
>    - **PDF app** (Acrobat, Preview, Xodo, GoodNotes…): highlight or strike, and add a comment. Send me the annotated PDF.
>    - **Notes or dictation**: the ID plus the change, e.g. `5.12 grey not gray` · `6.3 the door was seaward in ch 4` · `7.2 cut this sentence`. Paste them here.
>    - **Paper**: mark it with a pen and send photos. The IDs tell me where each mark is.
> 3. Run `/rama:corrections` and we'll go through the queue.

## Print

```bash
python3 <this skill's folder>/review_pdf.py export "<Title>.md" [--chapters 5-7]
```

Needs `reportlab` (`pip install reportlab`). Writes the PDF and
`review/review-map.json`, a snapshot of every paragraph at print time used to
find passages even after later edits. Chapters are numbered in manuscript
order. Text that opens a Part (before its first chapter) is numbered `P2.1`,
`P2.2`, and so on.

> Review PDF ready: `review/review-<date>.pdf` ([N] paragraphs).

In claude.ai, run it on `/mnt/project/<Title>.md` with `--out /mnt/user-data/outputs`.

## Import

**Annotated PDF:**

```bash
python3 <this skill's folder>/review_pdf.py import <annotated.pdf> --corrections "<Title> — Corrections.md" --map review/review-map.json
```

Needs `pymupdf`. Ink marks have no text, so render the page and read it.

**Notes** (chat, a file, dictation): one row per note. Accept `5.12`,
`ch 5 para 12`, a page number (via the map), or just a quoted phrase.
Expect dictation errors: interpret the note, don't reject it.

**Photos:** read each mark and the ID beside it. If a mark is unreadable, log
it as `unreadable: ask`.

## Locate

For each row: search the quoted text in the chapter named by the ID. If it's
not found, take the paragraph text from `review-map.json` and fuzzy-match it
in the current manuscript. If it's still not found, mark it `location unclear`
and ask.

## Classify and summarize

| Type | Handling |
|---|---|
| `typo`, `punctuation` | can be applied as a batch |
| `rewrite`, `cut`, `insert` | one at a time, with the proposed text shown |
| `continuity` | one at a time; check every chapter that mentions the detail, then update the Continuity Ledger |
| `style` | a new or clarified style rule. Propose the line for the style guide, then find **every** violation, not just this one |
| `question` | discuss it; no automatic change |

```
CORRECTIONS: 23 open
  typo/punctuation 11 · rewrite/cut/insert 7 · continuity 2 · style 1 · questions 2
```

Survey: **Apply the 11 typo/punctuation fixes at once / Show them first / One at a time.**

## Apply

- Everything except an approved batch goes one at a time:
  `5.12 · original → proposed`, then **Apply / Change / Skip**.
- Never change voice or rhythm beyond what the note asks. Replacement text
  must pass the style guide.
- Set each row's status: `done`, `skipped`, `style rule added`, or `discussed`.

## Close

1. Move completed import blocks under `## Archive` (open rows stay on top).
2. RAMA Log: Ledger for continuity fixes, Decisions for anything that
   changes the book, and word counts.
3. In a read-only claude.ai Project, write the full updated manuscript,
   Corrections file and RAMA Log to outputs, and say which to replace.

> [N] corrections applied across chapters [list]; [M] skipped; [K] open. Run `/rama:corrections print` for a fresh PDF.
