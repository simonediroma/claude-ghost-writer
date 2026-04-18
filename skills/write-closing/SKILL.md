---
description: Write the book's conclusion. Run after all chapters and the introduction are complete. The conclusion closes the arc opened by the introduction — it does not summarize, it lands. Reads the entire book and the introduction before writing.
---

# Skill: Write the Closing

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


The conclusion is not a summary. A summary insults the reader — they just read the book.

The conclusion is where the book lands. It closes what the introduction opened. It answers the question the book raised. It tells the reader what to do with what they now know, feel, or understand.

A conclusion that summarizes is a book that doesn't trust itself.

---

## Prerequisites

Check that `chapters/00-introduction.md` exists. If not:
> The conclusion should be written after the introduction — the two form an arc and must answer each other. Run `/ghost-writer:write-opening` first.

---

## Phase 0 — Read the Whole Book

Before asking any question, read:
1. `chapters/00-introduction.md` — what was promised at the opening
2. All chapters in order — the full arc of the book
3. `book-memory.md` — open promises, defined terms, chapter log
4. `demolition-history.md` — accepted limitations, deferred issues

Specifically identify:
- Every promise made in the introduction → has it been kept?
- Every open promise in `book-memory.md` → has it been resolved?
- The emotional or intellectual state the reader is in at the end of the last chapter → what do they need now?

---

## Phase 1 — The Interview

One question at a time.

**1. The landing**
> The reader has just finished the last chapter. What do you want them to feel in that moment — before they read the conclusion?

**2. The answer**
> What is the answer to the central question the book raised? Not a summary of the argument — the answer itself, stated as plainly as possible.

**3. The unresolved**
> Is there anything the book deliberately left open — a question it raised but didn't answer, a tension it named but didn't resolve? If yes: is that intentional, and how should the conclusion handle it?

**4. The call**
> What do you want the reader to do, think, or feel differently after closing this book? If there's an action — what is it? If there's a shift in perspective — what does the world look like from the other side?

**5. The last line**
> What is the last thing you want the reader to carry? Not a slogan — the specific thought, image, or question you want echoing after they close the book.

---

## Phase 2 — Check the Promises

Before writing, run a promise audit:

From `book-memory.md → Open Promises`, list every promise still marked unresolved.

For each:
> The book promised to address [X] in Chapter [N]. Did it? If not, the conclusion must either resolve it or explicitly acknowledge it as open.

Present the list to the author. For each unresolved promise, decide:
- **Resolve in conclusion** — address it here
- **Acknowledge as open** — name it as a deliberate unresolved question
- **Declare out of scope** — was implicitly resolved and doesn't need explicit treatment

---

## Phase 3 — Map the Conclusion

Propose a structure:

```
PROPOSED CONCLUSION STRUCTURE

The arrival: [where the reader is now — the emotional/intellectual position after the last chapter]
The answer: [the direct response to the book's central question]
The unresolved (if any): [what the book leaves open, and why — deliberately]
The implication: [what this means beyond the book — for the reader, for the field, for the world]
The call: [what the reader does with this — action, shift, question to carry]
The last image: [the closing move — concrete, specific, resonant]
```

Adapt for preset:
- **Fiction**: replace answer/implication with emotional resolution and thematic statement
- **Manual**: replace implication with the reader's next step — concrete and actionable
- **Biography**: replace call with the subject's significance — what this life illuminates

Ask: > Does this feel like the right ending? What's wrong or missing?

---

## Phase 4 — Write

Write the conclusion using:
- The exact voice from `book.config.json → author_voice`
- The specific images, terms, and examples established in the book — callbacks, not new material
- The answer to the central question — stated plainly, not hedged
- The last image confirmed in the interview

**Do not introduce new arguments, new examples, or new claims.** Everything in the conclusion must have been earned by what came before.

Save to `chapters/99-conclusion.md` with:
```markdown
---
title: Conclusion
version: 1.0
status: draft
written: last
---
```

Update `book-memory.md → Open Promises` — mark all resolved promises as resolved.

---

## After Writing

Tell the author:
> Conclusion drafted. Run `/ghost-writer:demolish-persona` with the `target-reader` persona — does the ending land for the reader this book was written for? Then check the arc: does the last line answer the first line of the introduction?
