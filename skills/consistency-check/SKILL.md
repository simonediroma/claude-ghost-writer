---
description: Cross-chapter consistency audit. Reads all written chapters and book-memory.md to find term drift, tone inconsistencies, broken promises, contradicted claims, and repeated examples. Run every 3-4 chapters, or any time something feels off. Produces a prioritized list of inconsistencies for the author to resolve.
---

# Skill: Consistency Check

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


Read the entire book written so far and find every place where the text is inconsistent with itself.

This is not a demolition of individual arguments. It is a **structural audit** — looking across chapters for drift, contradiction, and broken continuity.

---

## Before Starting

Read in this order:
1. `book.config.json` — check preset and `longform_mode`
2. **If `longform_mode: true`**:
   - `book-memory.md` — global index
   - All files in `memory/` — per-part memory in full
   - `demolition-history.md`
   - All chapter **summaries** from frontmatter (not full text yet)
   - Drill into full chapter text only when a specific issue requires it
3. **If `longform_mode: false`**:
   - `book-memory.md` — full
   - `demolition-history.md`
   - All files in `chapters/` — full text

`demolition-history.md` is the most important input. Do not repeat work already documented — verify whether patterns have been resolved or are still active, and look for new ones not yet captured.

Do not begin the audit until you have read everything at the appropriate depth.

---

## What to Check

### 1. Term Drift
Compare every term listed in `book-memory.md → Defined Terms` against how it is actually used across all chapters.

Flag any case where:
- The term is used with a different meaning than its definition
- The term is redefined implicitly without acknowledgment
- A synonym is used inconsistently (sometimes "reader," sometimes "user," sometimes "audience")

### 2. Contradicted Claims
Compare every claim in `book-memory.md → Central Claims Made` against what subsequent chapters argue.

Flag any case where:
- A later chapter argues the opposite of an earlier claim
- A later chapter narrows or broadens a claim without acknowledging it
- The conclusion of one chapter contradicts the premise of another

### 3. Broken Promises
Check `book-memory.md → Open Promises`. For each unresolved promise, check whether it has in fact been addressed in the text (the memory file may be out of date).

Flag any promise that:
- Was made but never resolved
- Was resolved in a way inconsistent with how it was set up
- Is still pending but the book is more than halfway through

### 4. Repeated Examples
Check `book-memory.md → Examples and Stories Used`. Read the text for any example used more than once as if it were being introduced for the first time.

Flag repetitions and mark whether they're intentional callbacks or accidental duplicates.

### 5. Tone Drift
Read the opening paragraph of each chapter in sequence. Note the emotional temperature and register.

Flag any chapter where:
- The tone is noticeably more formal or informal than the surrounding chapters
- The voice shifts from first person to third, or from direct address to lecture
- The energy drops significantly (often a sign the author was less engaged with this section)

### 6. Arc Coherence
Read `book-memory.md → Chapter Summary Log`. Check whether the sequence of claims builds logically toward the book's central premise.

Flag any chapter that:
- Could be removed without affecting the argument
- Assumes knowledge the book hasn't yet provided
- Resolves tension prematurely (before it's been fully established)

---

## Output Format

Present findings as a prioritized list, most critical first:

```
CONSISTENCY AUDIT — [Book Title]
Chapters reviewed: [N]
Issues found: [N]

─────────────────────────────
CRITICAL (must fix before continuing)

1. TERM DRIFT — "[term]"
   Defined in Ch. 1 as: [definition]
   Used in Ch. 4 as: [different meaning]
   Impact: Readers who noticed the definition will feel misled.

2. CONTRADICTED CLAIM
   Ch. 2 argues: [claim]
   Ch. 5 argues: [opposite]
   Impact: The book cannot hold both positions without explanation.

─────────────────────────────
SIGNIFICANT (fix before final draft)

3. BROKEN PROMISE
   Ch. 1 promised to address: [X]
   Status: Unresolved. Book is [N]% complete.

─────────────────────────────
MINOR (note for revision pass)

4. TONE DRIFT — Ch. 3
   Noticeably more formal than surrounding chapters.
   Possible cause: [observation]

5. REPEATED EXAMPLE
   [Example] used in Ch. 2 and Ch. 6 as if introduced both times.
```

Then ask:
> Which of these do you want to address first? I can run a targeted `/ghost-writer:integrate` session on any of these, or you can fix them directly and I'll update `book-memory.md`.

---

## After Resolution

When the author resolves an issue:
1. Update `book-memory.md` to reflect the correction
2. If a term definition changed, flag all chapters that used the old definition
3. Mark the issue as resolved in the audit summary

After all critical issues are resolved:
> The book is now internally consistent on the issues found. Run another consistency check after [N] more chapters.
