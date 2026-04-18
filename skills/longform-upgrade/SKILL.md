---
description: Activates long-form mode for books with 10+ chapters. Restructures the project into parts, splits book-memory.md into per-part memory files, adds chapter summaries to existing files, and updates all skills to use lazy reading. Run automatically when the 10th chapter is completed, or manually at any time.
---

# Skill: Long-Form Upgrade

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This skill upgrades a standard project to long-form mode. It reorganizes how memory and context work — without changing the content of any chapter.

After this upgrade, skills read the global index + current part instead of everything. Only `consistency-check` and `manuscript-final` read the full manuscript.

---

## When to Run

**Automatic trigger**: `write` and `chapter` skills check the completed chapter count after each integration. When a 10th chapter is marked `complete`, they say:

> You now have 10 complete chapters. For books this long, I recommend activating long-form mode — it keeps context lean and makes consistency checks faster. Run `/ghost-writer:longform-upgrade`, or I can run it now. It takes about 5 minutes and doesn't change any content.

**Manual**: the author can run this at any time.

---

## Phase 0 — Assess Current Structure

Read `outline.md` and all files in `chapters/`.

Report:
```
LONG-FORM UPGRADE ASSESSMENT

Chapters complete: [N]
Chapters in progress: [N]
Chapters planned: [N]
book-memory.md size: [approximate — small / medium / large]

Suggested part structure based on outline:
  Part 1: Ch. 1–4 — [theme or arc description]
  Part 2: Ch. 5–9 — [theme or arc description]
  Part 3: Ch. 10+ — [theme or arc description]
```

Ask:
> Does this part structure make sense, or do you want to define it differently?

The author can accept, adjust boundaries, rename parts, or define a completely different grouping.

Do not proceed until the part structure is confirmed.

---

## Phase 1 — Update outline.md

Add part headers to `outline.md`:

```markdown
## Part 1 — [Title]
*Chapters 1–4 | Theme: [description]*

### Chapter 1 ...
### Chapter 2 ...

## Part 2 — [Title]
*Chapters 5–9 | Theme: [description]*

### Chapter 5 ...
```

---

## Phase 2 — Add Summaries to Chapter Files

For each completed chapter, add a `summary` field to its frontmatter:

```markdown
---
title: Chapter Title
version: 1.2
claim: The central claim.
status: complete
summary: [3-5 sentences: what happens in this chapter, what the reader learns, what changes, what is left open. Written for a reader who has read everything before it.]
---
```

Generate the summary from the chapter content. Present each summary to the author before writing it:
> Here's the summary for Chapter [N] — [title]:
> "[summary]"
> Does this capture it accurately?

Do not write summaries without confirmation.

---

## Phase 3 — Create Per-Part Memory Files

For each part, create `memory/part-[N].md` using the template.

Migrate relevant content from `book-memory.md` into the appropriate part file:
- Terms defined in chapters 1-4 → `memory/part-1.md`
- Terms defined in chapters 5-9 → `memory/part-2.md`
- etc.

Keep `book-memory.md` as a **global index** — lighter, with pointers to part files:

```markdown
# Book Memory — Global Index

> Long-form mode active. Detailed memory is in memory/part-N.md files.
> Read the relevant part file for chapter-level detail.

## Parts

| Part | Chapters | Memory file | Status |
|---|---|---|---|
| Part 1 — [title] | Ch. 1–4 | memory/part-1.md | complete |
| Part 2 — [title] | Ch. 5–9 | memory/part-2.md | in-progress |

## Global Defined Terms

Terms that appear across multiple parts and must be consistent everywhere.

| Term | Definition | Parts |
|---|---|---|
| [term] | [definition] | Part 1, Part 2 |

## Global Open Promises

Promises that span multiple parts.

| Promise | Made in | Resolved in |
|---|---|---|
| [promise] | Ch. N | — |

## Session Log
[preserved from original book-memory.md]
```

---

## Phase 4 — Update Reading Instructions

Add a note to `book.config.json`:

```json
"longform_mode": true,
"parts": [
  { "number": 1, "title": "[title]", "chapters": "1-4", "memory": "memory/part-1.md" },
  { "number": 2, "title": "[title]", "chapters": "5-9", "memory": "memory/part-2.md" }
]
```

---

## Phase 5 — Lazy Reading Protocol

After upgrade, all skills follow this reading protocol:

**Standard reads (per chapter work):**
1. `book.config.json` — always
2. `book-memory.md` — global index only
3. `memory/part-[current].md` — current part detail
4. `memory/part-[previous].md` — previous part handoff section only
5. Chapter summaries from adjacent chapters (not full text)
6. Full text of the specific chapter being worked on

**Full reads (consistency and closing):**
- `consistency-check` — reads all part memory files + all chapter summaries + spot-checks full text on flagged issues
- `manuscript-final` — reads everything

This protocol is documented in `book.config.json` and honored by all skills when `longform_mode: true`.

---

## After Upgrade

```
LONG-FORM UPGRADE COMPLETE

Parts defined: [N]
Chapter summaries added: [N]
Memory files created: [N]
Global index: book-memory.md (updated)

Skills now use lazy reading:
  → global index + current part + adjacent summaries
  → full read only for consistency-check and manuscript-final
```

Say:
> Long-form mode is active. Nothing changed in your chapters — only how context is managed. Continue writing with `/ghost-writer:chapter` as usual.
