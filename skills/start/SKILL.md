---
description: Guided onboarding macro. Runs the complete setup sequence — author interview, book definition with genre preset, and voice fingerprint. Supports resume: if interrupted mid-onboarding, picks up from the last completed session.
---

# Macro: Start

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This macro runs the full onboarding sequence. Supports resume — if you stopped mid-onboarding, it picks up where you left off.

---

## Session Check

Read `sessions/start.md` if it exists.

If it exists and `status: open`, say:
> You started the onboarding but didn't finish. Here's where you left off:
> [show completed steps and current step]
> Resume, or start over?

If resuming → skip completed sessions, start from current step.
If starting over → overwrite `sessions/start.md`.

If no session file exists → create `sessions/start.md`:

```markdown
# Session: start

> Created: [date]
> Last updated: [date]
> Status: open

## Steps completed
- [ ] setup-author
- [ ] setup-book
- [ ] setup-voice

## Current step
setup-author
```

---

## How it works

Check `book.config.json` to determine state:
- `author_profile` missing → Session 1
- `book_profile` missing → Session 2
- `author_voice` incomplete → Session 3
- All complete → say: > Already set up. Run `/ghost-writer:chapter` to start writing.

After each session completes, update `sessions/start.md` — check off the step, update current step and date.

When all three complete, mark `status: complete`.

---

## Session 1 — Who Are You

Tell the author:
> Let's set up your book. Three short sessions — first: who are you as an author?

Run `setup-author`. On complete, update session file. Say:
> Author profile saved. Continue now or run `/ghost-writer:start` to resume later.

---

## Session 2 — What Is the Book

Tell the author:
> Now let's define the book — what it argues, who it's for, and its structure.

Run `setup-book`. On complete, update session file. Say:
> Book profile saved. Continue now or run `/ghost-writer:start` to resume later.

---

## Session 3 — How Does It Sound

Tell the author:
> Last session: your voice. A few questions, then a writing sample if you have one.

Run `setup-voice`. On complete, mark session `status: complete`.

---

## When Complete

```
SETUP COMPLETE — [Book Title]
─────────────────────────────
Genre preset:     [preset]
Author:           [one line]
Book:             [premise]
Voice:            [sounds-like line]
Chapters planned: [N]
─────────────────────────────
```

Say:
> Run `/ghost-writer:chapter` to write your first chapter.
