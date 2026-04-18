---
description: Generate a section of the book from the outline. Use AFTER ask-before-writing is complete and the author has confirmed the summary. Requires book.config.json and outline.md to exist in the project directory.
---

# Skill: Write a Section

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


Generate final text only after the structured dialogue (`ask-before-writing`) is complete and the author has confirmed the summary.

---

## Before Writing

1. Read `book.config.json` — check preset and `longform_mode`
2. **If `longform_mode: true`**: read `book-memory.md` (global index only) + `memory/part-[current].md` + handoff section of the previous part file + summaries from adjacent chapter frontmatters
3. **If `longform_mode: false`**: read full `book-memory.md`
4. If this chapter features profiled characters, read their files in `characters/`
5. Read `outline.md` — identify the requested section and its central claim
6. Read at least one existing chapter in `chapters/` — align to established style
7. Confirm that `ask-before-writing` has been completed for this section

When writing, use terms **exactly** as defined in memory. Do not introduce new definitions for already-defined terms. Do not use examples already listed as if they're new.

If `author_voice.signature_phrases` contains entries, use them as anchors — these are phrases extracted from the author's actual speech and should appear naturally in the text where they fit.

If `ask-before-writing` has not been done, ask:
> We haven't done the structured dialogue for this section yet. Do you want to proceed anyway, or start with `/ghost-writer:ask-before-writing`?

---

## Writing Instructions

Respect strictly:
- **Voice**: use `author_voice.tone`, `register`, `pov` from `book.config.json`
- **Rhythm**: respect `author_voice.rhythm`
- **Prohibitions**: never use anything listed in `author_voice.avoid`
- **Consistency**: use terms and concepts exactly as defined in the dialogue

---

## Section Structure

1. **Opening** — image, analogy, or observation that hooks the reader
2. **Development** — main argument with the section's claim
3. **Implications** — what changes for the reader after this argument
4. **Transition** — connection to the next section (if applicable)

---

## Output

Save the text in `chapters/[NN]-[section-name].md` with this header:

```markdown
---
title: [Section Title]
version: 1.0
claim: [central claim of this section]
status: draft
---

[text]
```

Update `outline.md` — change the section status to `draft`.

Update memory:
- If `longform_mode: true` → update `memory/part-[current].md` with new terms, promises, examples
- If `longform_mode: false` → update `book-memory.md` directly

**Long-form trigger**: count complete chapters in `outline.md`. If this completion brings the total to exactly 10 and `longform_mode` is not yet active, say:
> You now have 10 complete chapters. For books this length, long-form mode keeps context lean and consistency checks fast. Run `/ghost-writer:longform-upgrade` when convenient — it takes about 5 minutes and doesn't change any content.

Then present to the author:
> Draft generated for [section]. Run `/ghost-writer:demolish` when ready.
