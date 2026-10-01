---
description: Manage the book's writing rules in style-rules.md — punctuation conventions and custom rules like "never use a colon to introduce a subordinate clause" or "always use double quotes for thoughts". Add, list, edit, remove. Rules are enforced by write, integrate and revise.
---

# Skill: Rules

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Usage:
- `/ghost-writer:rules` — list current rules
- `/ghost-writer:rules add "[rule in natural language]"` — add a rule
- `/ghost-writer:rules remove R[n]` / `edit R[n]`
- `/ghost-writer:rules infer` — fill the Punctuation Conventions from the chapters already written

All rules live in `style-rules.md`. If it doesn't exist, create it from the plugin template.

---

## Adding a Rule

1. Read the author's sentence. Decide whether it is a **punctuation convention** (one value for one element: dialogue marks, dashes, ellipsis…) or a **writing rule** (anything else).
2. Rewrite it as a precise, checkable rule and propose:
   - **Scope**: narration / dialogue / thoughts / all
   - **✅ Right** and **❌ Wrong** example — taken from the book if possible, otherwise invented in the author's voice
3. Ask: *"Is this the rule? (yes / change)"* — one question only.
4. On yes: save with the next ID (`R[n]`) and `Source: author, [date]`.
5. Search the chapters for existing violations and say how many:
   > Saved as R[n]. Found [N] existing violations in [chapters]. Run `/ghost-writer:revise --only rules` to fix them.

If the new rule conflicts with an existing one, show both and ask which wins before saving.

---

## Inferring Conventions

For each row of **Punctuation Conventions**, count the forms used in `chapters/` and propose the dominant one, with counts:
> Dialogue: «» 142 times, "" 9 times → «». Confirm?

Save after confirmation. If the book has no chapters yet, propose the defaults for `book.config.json → language` (see the table at the end of `skills/revise/SKILL.md`).

---

## Listing

Show the two tables compactly. For each writing rule, one line: `R[n] — [rule] ([scope])`.
