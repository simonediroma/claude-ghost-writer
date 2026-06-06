---
description: Generate a section of the book from the outline. Use AFTER ask-before-writing is complete and the author has confirmed the summary. Requires book.config.json and outline.md to exist in the project directory.
---

# Skill: Write a Section

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.


Generate final text only after the structured dialogue (`ask-before-writing`) is complete and the author has confirmed the summary.

---

## Quick-Write Mode

If the author invokes this skill with `--quick`, or explicitly says they want to skip the dialogue and write directly, activate Quick-Write Mode:

1. Do not run or wait for `ask-before-writing`
2. Ask one single question instead:
   > In 2-3 sentences: what is this chapter about and what should the reader understand by the end of it?
3. After the author answers, proceed directly to writing — treat their description as the brief

Quick-Write is appropriate when the author already has a clear idea, wants a fast first draft to react to, or the chapter is straightforward enough that a full dialogue would add friction without value. Quick-Write drafts typically need more `integrate` work — flag this when presenting the draft.

---

## Before Writing

1. Read `book.config.json` — check preset and `longform_mode`
2. **If `longform_mode: true`**: read `book-memory.md` (global index only) + `memory/part-[current].md` + handoff section of the previous part file + summaries from adjacent chapter frontmatters. Read only `## Defined Terms`, `## Central Claims Made`, and `## Open Promises to the Reader` sections.
3. **If `longform_mode: false`**: read `book-memory.md` — but only the sections `## Defined Terms`, `## Central Claims Made`, and `## Open Promises to the Reader`. Skip `## Session Log`, `## Tone Calibration`, `## Recurring Metaphors`.
4. If this chapter features profiled characters, read their files in `characters/`
5. Read `outline.md` — identify the requested section and its central claim
6. **Style alignment**: if `voice-sample.md` exists and is populated, read it. If it does not exist or contains only the placeholder text, read one existing chapter from `chapters/` instead.
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
summary:
---

[text]
```

Update `outline.md` — change the section status to `draft`.

Update memory:
- If `longform_mode: true` → update `memory/part-[current].md` with new terms, promises, examples
- If `longform_mode: false` → update `book-memory.md` directly

**Silent voice update**: After saving the chapter file, silently extract and write to `voice-sample.md`:
1. The opening paragraph of the chapter
2. One paragraph from the middle that best shows the author's argumentative or narrative rhythm
3. The closing paragraph

Overwrite any previous content in `voice-sample.md`. Do not mention this step to the author.

**Silent summary update**: Immediately after the voice update, silently write a `summary` into the chapter file's frontmatter (the `summary:` field saved above). Write 3-5 sentences covering: what happens in this chapter, what the reader learns, what changes, and what remains open. Written for a reader who has already read everything before this chapter. Do not mention this step to the author. If `longform-upgrade` is later run, the summary is already present — present it for confirmation rather than regenerating it.

**Long-form trigger**: count complete chapters in `outline.md`. If this completion brings the total to exactly 10 and `longform_mode` is not yet active, say:
> You now have 10 complete chapters. For books this length, long-form mode keeps context lean and consistency checks fast. Run `/ghost-writer:longform-upgrade` when convenient — it takes about 5 minutes and doesn't change any content.

Then present to the author:
> Draft generated for [section]. Run `/ghost-writer:demolish` when ready.
