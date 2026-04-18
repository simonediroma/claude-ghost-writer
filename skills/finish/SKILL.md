---
description: Guided closing macro. Runs the complete book-closing sequence — introduction, conclusion, arc audit, manuscript assembly. Supports resume: if interrupted, picks up from the last completed step.
---

# Macro: Finish

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


Closes the book. Supports resume — if interrupted, picks up where it left off.

---

## Session Check

Read `sessions/finish.md` if it exists.

If open session exists:
> You started the closing sequence but didn't finish. Last completed: [step]. Resume, or start over?

If new → create `sessions/finish.md`:

```markdown
# Session: finish

> Created: [date]
> Last updated: [date]
> Status: open

## Steps completed
- [ ] write-opening
- [ ] write-closing
- [ ] manuscript-final

## Current step
write-opening

## Notes
```

---

## Setup

Check chapter statuses. If unfinished chapters exist, warn and ask to confirm.

Check what's already done — skip completed steps, resume from current.

---

## Step 1 — Introduction

Tell the author:
> The introduction is written last — it knows what the whole book delivers.

Run `write-opening`. On complete, update session: check off `write-opening`, set current to `write-closing`. Say:
> Introduction drafted. Read it, then run `/ghost-writer:finish` to continue with the conclusion.

---

## Step 2 — Conclusion

Run `write-closing` including promise audit. On complete, update session: check off `write-closing`, set current to `manuscript-final`. Say:
> Conclusion drafted. Read both together — does the last line answer the first? Run `/ghost-writer:finish` when ready for the final audit.

---

## Step 3 — Final Audit and Assembly

Run `manuscript-final`. On complete, mark session `status: complete`.

```
BOOK COMPLETE — [Book Title]
─────────────────────────────────────
Manuscript: manuscript/[title]-final.md
Session: closed ✅
─────────────────────────────────────
```

Say:
> The book is done. Read it in one sitting, as a reader — not as the author.


This macro closes the book. It runs in sequence: introduction, conclusion, final audit, manuscript assembly.

Run this when every chapter is written and integrated. Not before.

---

## Setup

Read `outline.md` and `book-memory.md`.

Check chapter statuses. If any chapter is still `draft` or `in-review`:
> These chapters aren't finished yet: [list]. The closing sequence works best on a complete book. Do you want to finish those chapters first, or proceed anyway?

Check what's already been done:
- If `chapters/00-introduction.md` exists → skip Step 1, say "Introduction already written."
- If `chapters/99-conclusion.md` exists → skip Step 2, say "Conclusion already written."
- If both exist → go directly to Step 3.

---

## Step 1 — Write the Introduction

Tell the author:
> The introduction is written last — it's the only part that knows what the whole book delivers. I'll read the entire manuscript before we start.

Run the full `write-opening` skill.

When the introduction draft is saved:
> Introduction drafted. Read it. When ready, we'll write the conclusion.

Wait for the author to confirm they've read it. Then proceed.

---

## Step 2 — Write the Conclusion

Tell the author:
> Now the conclusion. This closes the arc opened by the introduction — it doesn't summarize, it lands.

Run the full `write-closing` skill, including the promise audit.

When the conclusion draft is saved:
> Conclusion drafted. Read both the introduction and conclusion together — check that the last line answers the first. When ready, we'll do the final audit.

Wait for confirmation.

---

## Step 3 — Final Audit and Assembly

Tell the author:
> Final step: I'll read the complete manuscript and check the arc, then assemble everything into a single file.

Run the full `manuscript-final` skill, including:
- Arc audit (opening–closing correspondence, promise audit, term consistency, tone arc)
- Optional process note
- Manuscript assembly

---

## When Complete

```
BOOK COMPLETE — [Book Title]
─────────────────────────────────────
Chapters: [N] + introduction + conclusion
Final version: [from book.config.json]
Manuscript: manuscript/[title]-final.md

Arc audit: [passed / N issues resolved]
Open promises: [all resolved / N acknowledged]
─────────────────────────────────────
```

Then say:
> The manuscript is assembled at `manuscript/[title]-final.md`.
>
> One thing before you send it anywhere: read it in one sitting, as a reader — not as the author. Every problem you notice in that read is real. Every part that surprises you is also real.
>
> The book is done.
