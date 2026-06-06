---
description: Cross-chapter consistency audit. Reads all written chapters and book-memory.md to find term drift, tone inconsistencies, broken promises, contradicted claims, and repeated examples. Run every 3-4 chapters, or any time something feels off. Produces a prioritized list of inconsistencies for the author to resolve.
---

# Skill: Consistency Check

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.


Read the entire book written so far and find every place where the text is inconsistent with itself.

This is not a demolition of individual arguments. It is a **structural audit** — looking across chapters for drift, contradiction, and broken continuity.

---

## Before Starting

Read `book.config.json` first. Then immediately say:

> Starting consistency audit — [N chapters written, M complete]. Reading...

This lets the author know the skill is active before the heavier reads begin.

Then read the rest:

1. **Always**:
   - `book-memory.md` — full (active sections: Defined Terms, Central Claims, Open Promises, Examples, Recurring Metaphors, Chapter Summary Log)
   - `demolition-history.md` — **active sections only** (skip `## Archived Cycles`)

2. **If `longform_mode: true`**:
   - All files in `memory/` — per-part memory in full
   - All chapter `summary` fields from frontmatter — not full text
   - Drill into full chapter text only when a specific issue requires it

3. **If `longform_mode: false`**:
   - Read all chapter `summary` fields from frontmatter first
   - For **Tone Drift**: read only the opening paragraph of each chapter
   - For **Term Drift**, **Contradicted Claims**, **Broken Promises**, **Repeated Examples**, **Arc Coherence**: work from summaries; drill into full text only for chapters where the summary flags a potential issue or where the term/claim first appears
   - If a chapter has no `summary` field (written before auto-summary was active): read its full text
   - Full reads are the exception, not the rule

`demolition-history.md` is the most important input. Do not repeat work already documented — verify whether patterns have been resolved or are still active, and look for new ones not yet captured.

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

Present findings **category by category as you complete each check** — do not wait until all six checks are done before showing any output. Output CRITICAL findings immediately when found; do not hold them for a final summary block.

After completing all checks, present a clean consolidated header:

```
CONSISTENCY AUDIT — [Book Title]
Chapters reviewed: [N]
Issues found: [N]
```

Then the findings you already surfaced, organized:

```
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

If no issues found in a category, write one line: `No [category] issues found.` and move on immediately.

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
