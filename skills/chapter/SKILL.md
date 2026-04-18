---
description: Guided chapter macro. Runs the complete writing cycle for one chapter — concept dialogue, writing, demolition, and integration — in sequence. Supports resume: if interrupted, picks up from where it left off. Use this instead of running ask-before-writing, write, demolish, and integrate separately.
---

# Macro: Chapter

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This macro runs the full writing cycle for one chapter. If interrupted, it resumes from the last completed step.

---

## Setup — Session Check

First, read all files in `sessions/` that match pattern `chapter-*.md` and have `status: open`.

If open chapter sessions exist, present them:

```
OPEN CHAPTER SESSIONS

1. Chapter 3 — "The Minimum Path" — interrupted at: demolish (cycle 1 done, integration pending)
   Last worked on: [date]

2. Chapter 5 — "Epiphanies" — interrupted at: write (draft exists, not yet demolished)
   Last worked on: [date]

→ Resume one of these, or start a new chapter?
```

Options:
- **Resume [N]** — pick up from the saved step
- **New chapter** — start fresh (creates a new session)
- **Abandon [N]** — mark session as abandoned and start fresh on that chapter

If no open sessions exist, proceed directly to chapter selection.

---

## New Session — Chapter Selection

Read `book.config.json`, `book-memory.md`, `outline.md`, and the preset file.

Check onboarding: if `author_voice` or `preset` is missing:
> Your project isn't set up yet. Run `/ghost-writer:start` first.

Ask:
> Which chapter do you want to work on?
> [list chapters from outline with statuses]

Create a session file at `sessions/chapter-[NN]-[slug].md`:

```markdown
# Session: chapter — chapters/[NN]-[slug].md

> Created: [date]
> Last updated: [date]
> Status: open

## Macro
chapter

## Target
chapters/[NN]-[slug].md

## Current step
ask-before-writing

## Steps completed
- [ ] ask-before-writing
- [ ] write
- [ ] demolish
- [ ] integrate

## Notes
```

---

## Resuming a Session

Read the session file. Identify the current step. Skip all completed steps.

Tell the author:
> Resuming Chapter [N] — [title]. Last completed: [step]. Picking up at: [current step].

Then continue from that step.

After each step completes, update the session file:
- Check off the completed step
- Update `current step` to the next
- Update `last updated` date
- Add any relevant notes (e.g. "demolition cycle 1: 3 issues resolved, 1 deferred")

---

## Step 1 — Concept Dialogue

Tell the author:
> Before writing, let's make sure the concepts are clear. One question at a time.

Run `ask-before-writing`. When confirmed, update session: check off `ask-before-writing`, set current step to `write`.

---

## Step 2 — Write

Run `write` for the selected chapter. When draft is saved, update session: check off `write`, set current step to `demolish`.

Say:
> Draft saved. Read it, then tell me when you're ready to stress-test it. We can stop here — run `/ghost-writer:chapter` to resume at the demolition step.

---

## Step 3 — Demolish

Run `demolish`. When cycle complete and logs updated, update session: check off `demolish`, set current step to `integrate`.

Ask: > Run persona reads with `/ghost-writer:review` before integrating, or go straight to integration?

If review → note in session file, wait. If integrate → proceed.

---

## Step 4 — Integrate

Run `integrate`. When complete, update session:
- Check off `integrate`
- Set `status: complete`

---

## When the Cycle Is Complete

Mark session `status: complete` in the session file.

```
CHAPTER COMPLETE — [Chapter Title]
─────────────────────────────────
Version: [N]
Demolition cycles: [N]
Issues resolved: [N] | Deferred: [N] | Accepted: [N]
Session: closed ✅
─────────────────────────────────
```

Check consistency trigger — if 3+ chapters complete since last check, suggest `consistency-check`.

Say:
> Run `/ghost-writer:chapter` for the next chapter, or `/ghost-writer:session-start` to see your progress.
