---
description: Collect and apply the corrections the author makes while re-reading the book away from the computer. Generates a review PDF with paragraph IDs in the margin (3.12 = chapter 3, paragraph 12), imports highlights and comments from the annotated PDF, or parses free-form notes (phone notes, voice dictation, photos of marked-up printed pages). Everything goes into corrections.md, then gets applied one by one with confirmation.
---

# Skill: Corrections

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Usage:
- `/ghost-writer:corrections print [chapters]` — create the review PDF to read on the couch
- `/ghost-writer:corrections import [annotated.pdf]` — import annotations from the PDF
- `/ghost-writer:corrections` — process notes pasted in chat, a notes file, or photos; or resume the open queue in `corrections.md`

---

## The Re-reading Workflow (explain once, the first time)

> 1. Run `/ghost-writer:corrections print` → you get `manuscript/review-[date].pdf`. Every paragraph has an ID in the margin.
> 2. Read it wherever you want — tablet, phone or printed. Annotate however is easiest for you:
>    - **Tablet/phone PDF app** (Adobe Acrobat, Xodo, Preview, Drawboard, Foxit…): highlight or strike the text and add a comment. Then send me the annotated PDF.
>    - **Notes app or voice dictation**: write the paragraph ID + what to change. E.g. `3.12 perchè → perché` · `5.4 qui gli occhi sono verdi, prima erano blu` · `7.2 togli questa frase`. Then paste the notes here.
>    - **Paper**: mark the printed page with a pen and take a photo. Send me the photos — the IDs in the margin tell me where each mark is.
> 3. Come back and run `/ghost-writer:corrections`. I put everything in `corrections.md` and we go through it.

---

## Print

Run:
```bash
python3 review_pdf.py export [chapter files]   # default: all chapters/
```
Requires `reportlab` (`pip install reportlab`). It also writes `manuscript/review-map.json`, the snapshot of every paragraph at print time — used to locate notes even if the text changes afterwards.

> Review PDF ready: `manuscript/review-[date].pdf` ([N] paragraphs, [P] pages).

---

## Import

### Annotated PDF
```bash
python3 review_pdf.py import [annotated.pdf]
```
Requires `pymupdf` (`pip install pymupdf`). Extracts highlights, underlines, strike-outs, sticky notes, free-text comments and ink marks, with paragraph ID, highlighted text and comment, and appends them to `corrections.md` with status `open`. Ink (handwritten) marks have no text: render that page and read it.

### Free-form notes (chat, file, dictation)
Parse each note into one row of `corrections.md`. Accept any format: `3.12`, `cap 3 par 12`, `p. 45` (use the page → ID mapping of the PDF if available), or just a quote ("dove dice 'la Panda rossa'"). Dictation errors are expected: interpret, don't reject.

### Photos of printed pages
Read the image. For every mark (circled word, strike-through, margin note, insertion caret), read the paragraph ID beside it and transcribe the mark as a row. If a mark is unreadable, add it with note `unreadable — ask` and ask the author when you reach it.

---

## Locate

For each row, find the exact passage in the **current** chapter file:
1. Search the quoted text in the chapter file named by the ID
2. If not found, use `review-map.json` → the paragraph text at print time, then fuzzy-match it in the current file (the text may have been edited since printing)
3. If still not found → `location unclear` — ask the author

---

## Classify

Give each row a type:

| Type | Example | Handling |
|---|---|---|
| `typo` | perchè → perché | batch-able |
| `punctuation` | ... → … | batch-able |
| `rewrite` | "riscrivi più asciutto" | one at a time — propose the new text |
| `cut` / `insert` | "togli", "aggiungi che…" | one at a time |
| `continuity` | "prima erano blu" | one at a time — check every chapter that mentions the detail, update `book-memory.md → Continuity Ledger` |
| `rule` | "sempre «» per i pensieri", "mai i : prima di una subordinata" | propose saving to `style-rules.md` (via the `rules` logic) — then find and fix all violations, not just this one |
| `question` | "è credibile?" | discuss — no automatic change |

Then show the summary:

```
CORRECTIONS — [N] open
  typo/punctuation: [n]  (can be applied in one go)
  rewrite/cut/insert: [n]
  continuity: [n]
  new rules: [n]
  questions: [n]
  unclear location: [n]
```

Ask:
> Apply the [n] typos and punctuation fixes in one go? (yes / show them first)

---

## Apply

- Typos/punctuation: apply after confirmation, then list them grouped by chapter.
- Everything else: **one at a time**. Show `ID — original → proposed`, wait for yes / change / skip.
- Never change voice or rhythm beyond what the note asks.
- After each item, set its status in `corrections.md`: `done`, `skipped`, `rule R[n]`, or `discussed`.
- In each modified chapter, increment `version` in the frontmatter.

---

## When Complete

1. Move completed import blocks under a `## Archive` heading at the bottom of `corrections.md` (keep open rows on top)
2. If any rule was added, offer: *"New rules saved. Run `/ghost-writer:revise --only rules` to check the whole book?"*
3. Tell the author:

> [N] corrections applied in [chapters]. [M] skipped, [K] open questions. When you want another round, run `/ghost-writer:corrections print` for a fresh PDF.
