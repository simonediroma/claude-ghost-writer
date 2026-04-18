---
description: Final manuscript audit and preparation. Run after introduction, all chapters, and conclusion are complete and integrated. Performs a full arc check, verifies all promises are kept, checks opening-closing correspondence, and produces a clean manuscript ready for submission or publication. This is the last skill to run.
---

# Skill: Final Manuscript

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This is the last skill. Run it when every chapter, introduction, and conclusion is at final version.

It does two things: audits the complete manuscript as a whole, then assembles it into a clean, submission-ready file.

---

## Prerequisites

Check that these files exist and are at `status: complete`:
- `chapters/00-introduction.md`
- All chapter files
- `chapters/99-conclusion.md`

If any file is still `draft` or `in-review`, say:
> These files are not yet at final version: [list]. The manuscript audit should run on complete text. Do you want to proceed anyway?

---

## Phase 1 — The Arc Audit

Read the entire manuscript in order: introduction → chapters → conclusion.

Check these five things. Present findings one at a time.

**1. Opening–closing correspondence**

Read the first paragraph of the introduction and the last paragraph of the conclusion side by side.

Ask: does the ending answer the beginning? Does the book close what it opened?

Flag any gap:
> The introduction opens with [X]. The conclusion does not return to it. This may feel unresolved to the reader — or it may be intentional. Which is it?

**2. Promise audit**

Read `book-memory.md → Open Promises`. For every promise, verify it was resolved in the text.

If unresolved:
> The book promised [X] in Chapter [N]. I cannot find where it was resolved. The conclusion may need to address this explicitly, or the promise may need to be removed from where it was made.

**3. Term consistency**

Read `book-memory.md → Defined Terms`. Check that every defined term is used consistently across introduction, chapters, and conclusion.

Flag any drift found.

**4. Tone arc**

Read the opening paragraph of each chapter in sequence — introduction through conclusion.

Does the emotional temperature of the book follow a coherent arc? For essays and non-fiction: does it build toward resolution? For fiction: does it follow the dramatic arc? For manuals: does it move from problem to mastery?

Flag any chapter that breaks the arc without reason.

**5. The book's central claim**

State the book's central claim in one sentence, derived from reading the full manuscript.

Present it to the author:
> Based on the complete manuscript, the book's central claim is: [statement]. Is this what you intended?

If not, identify where the drift occurred.

---

## Phase 2 — Final Issues

Present all findings as a prioritized list. For each issue, the author decides: fix, acknowledge, or accept.

Do not proceed to manuscript assembly until all critical issues are resolved or consciously accepted.

---

## Phase 3 — Authorship Note (Optional)

Before assembling, ask once — and only once:

> Do you want to include a note on how this book was written?

If **no**: move directly to assembly. Never raise this again.

If **yes**: generate a draft based on the actual process recorded in the project logs — not a template, but a description of what actually happened.

Read:
- `book-memory.md → Session Log` — how many sessions, over what period
- `demolition-history.md → Summary` — total demolition cycles, issues raised and resolved
- `book.config.json → preset` — the type of book and method used

Draft a note in the author's voice (from `book.config.json → author_voice`). It should describe: what the collaboration looked like in practice, what the author contributed, what the plugin contributed, and how the iterative process worked. It should not oversell or undersell either party.

Present the draft:
> Here's a possible note on the writing process. This is entirely your choice — include it, modify it, or discard it. It's based on what actually happened in this project.

The author may edit freely. Do not push back on any modification, including removing Claude/AI from the attribution entirely. It is their book.

If included, save as `manuscript/process-note.md` and add it to the assembled manuscript after the conclusion, clearly marked as optional front or back matter.

---

## Phase 4 — Manuscript Assembly

When the audit is complete, assemble the full manuscript in order:

1. Title page
2. Table of contents (generated from chapter titles and `outline.md`)
3. Introduction (`chapters/00-introduction.md`)
4. Chapters in order (all files in `chapters/` except 00 and 99, sorted numerically)
5. Conclusion (`chapters/99-conclusion.md`)

Write the assembled manuscript to `manuscript/[book-title]-final.md`.

Format:
```markdown
# [Book Title]
### [Subtitle if any]

*[Author Name]*

---

## Table of Contents

1. Introduction
2. [Chapter 1 Title]
3. [Chapter 2 Title]
...
N. Conclusion

---

## Introduction

[content of 00-introduction.md, without frontmatter]

---

## Chapter 1 — [Title]

[content, without frontmatter]

---

[continue for all chapters]

---

## Conclusion

[content of 99-conclusion.md, without frontmatter]
```

---

## Phase 4 — Final Summary

After assembly, present:

```
MANUSCRIPT COMPLETE — [Book Title]
Version: [from book.config.json]
Date: [today]

Chapters: [N]
Total arc: introduction → [N chapters] → conclusion
Central claim: [one sentence]

Arc audit: [passed / N issues resolved / N issues accepted]
Promises: [all resolved / N acknowledged as open]
Term consistency: [consistent / N corrections applied]

File: manuscript/[book-title]-final.md

Issues accepted as limitations:
[list from demolition-history.md → Accepted Limitations]
```

Then say:
> The manuscript is assembled. One last thing before you send it anywhere: read it in one sitting, as a reader — not as the author. Every problem you notice in that read is real. Every part that surprises you with how good it is — that's also real.
>
> When you're ready to share with beta readers, run `/ghost-writer:export-pdf` to generate a clean, readable PDF.
