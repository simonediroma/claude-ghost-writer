---
description: Write the book's introduction or opening chapter. Run AFTER all other chapters are complete — not before. The introduction is written last because it can only make promises the book has actually kept. Reads the entire book before writing a single word.
---

# Skill: Write the Opening

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


The introduction is written last. It is the only part of the book that knows what the whole book is.

An introduction written before the book makes promises that may not be kept. An introduction written after the book knows exactly what it delivers — and can promise only that.

---

## Prerequisites

Check `outline.md` and `book-memory.md`. If any chapter is still in `draft` or `in-review` status, say:
> The introduction should be written after all chapters are complete. These chapters are still in progress: [list]. Do you want to proceed anyway, knowing the introduction may need revision after those chapters are finished?

If the author confirms, continue.

---

## Phase 0 — Read the Whole Book

Before asking any question or writing any word, read:
1. All files in `chapters/` — every completed chapter
2. `book-memory.md` — every defined term, every promise made, every claim committed to
3. `demolition-history.md` — what the book struggled with, what limitations were accepted
4. `book.config.json` — the preset, the author's voice, the target reader

Do not begin the interview until you have read everything.

---

## Phase 1 — The Interview

One question at a time.

**1. The entry point**
> What is the first thing the reader needs to feel or understand to be ready for this book? Not the first argument — the emotional or intellectual door the introduction opens.

**2. The promise**
> Based on what the book actually delivers, complete this sentence: "By the end of this book, you will [specific transformation / understanding / feeling]."

Push for specificity. Not "understand X better" but the precise change.

**3. The reader's starting point**
> What does your reader believe or think or feel right now — before page one — that this book will change or challenge?

**4. The hook**
> What is the single most surprising, counterintuitive, or provocative thing in this book? The thing that, if you said it at a dinner party, would make the table go quiet?

This is often the best opening line. Not necessarily stated outright — but the energy that drives the opening.

**5. What the introduction must NOT do**
> Is there anything the introduction should avoid — a framing you've seen elsewhere that you don't want, a tone that would signal the wrong thing to your reader?

---

## Phase 2 — Map the Introduction

Based on the interview and your reading of the full book, propose a structure:

```
PROPOSED INTRODUCTION STRUCTURE

Opening move: [the hook or entry — what puts the reader in the right state]
The problem: [what makes this book necessary]
The argument: [the book's central claim, stated precisely but accessibly]
The promise: [what the reader will have by the end]
The road map: [brief orientation to the book's structure — optional, preset-dependent]
The invitation: [the closing move that hands the reader into chapter 1]
```

For **fiction preset**: replace argument/promise with dramatic question and emotional contract.
For **manual preset**: replace argument with the transformation, add "who this is for and who it isn't."
For **biography preset**: replace argument with interpretation, add the authorial stance.

Ask: > Does this structure feel right? What's missing or wrong?

---

## Phase 3 — Write

Write the introduction using:
- The author's voice from `book.config.json → author_voice`
- The exact terms and framing established in the book
- The specific hook and entry point confirmed in the interview
- No promises the book doesn't keep — check against `book-memory.md`

The introduction should feel like it was written by someone who has read the whole book — because it was.

Save to `chapters/00-introduction.md` with:
```markdown
---
title: Introduction
version: 1.0
status: draft
written: last
---
```

---

## After Writing

Tell the author:
> Introduction drafted. I'd suggest running `/ghost-writer:demolish-persona` with the `editor` persona on this — introductions are the most over-written part of any book. Then run `target-reader` to verify it opens the right door for your reader.
