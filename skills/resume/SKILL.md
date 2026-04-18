---
description: The one command to remember. Run this whenever you open the project and don't know where to start. Shows what you last did, what's waiting, and exactly what to do next — one clear recommendation. Nothing else.
---

# Skill: Resume

> **Language**: Read `book.config.json → language`. Write all output in that language. Default: English.

One command. One answer. Where were you, and what do you do now.

---

## What to read

Read quickly — this should feel instant:
1. `book.config.json` — title, preset
2. `outline.md` — chapter statuses at a glance
3. `sessions/` — any open macro sessions
4. The most recently modified file in `chapters/` — last thing touched
5. `demolition-history.md → Summary` counters only — not the full log

Do not read full chapter files. Do not read full memory files. This is a fast scan, not a deep read.

---

## Output

Keep it short. Three blocks, no more.

```
📚 [Book Title]
─────────────────────────────

LAST TIME
[One sentence: the last concrete thing that happened]
e.g. "You finished integrating Chapter 2 — it's now at v1.1."
e.g. "You were mid-demolition on Chapter 3, one issue left open."
e.g. "You ran the wizard and set up the project but haven't started writing yet."

WAITING
[One or two things that are pending — no more]
e.g. "Chapter 3 demolition has one deferred issue."
e.g. "Chapter 4 is drafted but hasn't been demolished yet."
e.g. "3 chapters complete — consistency check overdue."
[If nothing is waiting: "Nothing pending. Clean slate."]

NEXT
[One specific command to run — not a menu, one recommendation]
→ /ghost-writer:chapter
   "Pick up Chapter 3 demolition — the deferred issue on scope."
```

---

## The recommendation logic

Choose the single most useful next action:

- Open macro session exists → resume it: `/ghost-writer:[macro]`
- Chapter demolished, not integrated → `/ghost-writer:integrate`
- Chapter drafted, not demolished → `/ghost-writer:demolish`
- Chapter in ask-before-writing → `/ghost-writer:ask-before-writing`
- All chapters complete, no intro → `/ghost-writer:finish`
- 3+ chapters complete, no consistency check → `/ghost-writer:consistency-check`
- No chapters started, project configured → `/ghost-writer:chapter`
- Project not configured → `/ghost-writer:wizard`

One recommendation. Always. Never a list of options.

---

## Tone

Warm and direct. Like a colleague who knows the project and has been waiting for you.

Not a status report. Not a dashboard. A person saying: "Welcome back — here's where we are, here's what to do."

If the project is just starting:
> You're all set up. The best way to start is to pick the chapter you most want to write — not necessarily the first one.
> → `/ghost-writer:chapter`

If a lot has been done:
> Good progress. [X chapters] done, [Y] in progress.
> → [next action]

Never say "I noticed" or "According to the files." Just say what's true.
