---
name: integrate
description: Turn the author's answers from /rama:demolish or /rama:review into precise changes to the manuscript. Presents each change as current text versus proposed text, applies nothing without explicit approval, and checks every change for knock-on effects across the book. Usage /rama:integrate 5.
---

# RAMA: Integrate

*Adapted from ghost-writer's `integrate` (MIT, Simone Di Roma).*

Read `references/project-files.md` and `references/survey.md` first.

## Rules (non-negotiable)

- Never apply a change without the author's explicit approval.
- One integration at a time.
- Minimal changes: only what the answer requires.
- Check for knock-on effects after every change.
- The author's words take precedence over your formalization of them.
- Every new or rewritten sentence must pass the style guide. Reread the
  banned constructions before drafting any replacement text.

## Phase 0: Collect

Read the RAMA Log's `## Demolition Log` for this chapter, and its Decisions.
Collect the `resolved` items not yet `integrated`. Read the chapter in full,
the style guide, and the passages in other chapters that the resolutions
touch (a plant in an earlier chapter, say).

If an answer is ambiguous, ask before drafting.

## Phase 1: One at a time

1. Summarize the author's answer:
   > Your answer to [issue] was: [summary]. Right?
2. Say what the text needs and where (a new beat, a changed line, a plant
   in an earlier chapter, a cut).
3. Show the change:

   ```
   Chapter 5 · ¶14
   Current:  > …
   Proposed: > …
   What changed and why: one sentence.
   ```

4. Ask: **Apply / Apply with my change / Not this one.** If the author edits
   the text, restate the final version and confirm once more. Then apply.

## Phase 2: Knock-on effects

After each change, look for consequences: the same detail elsewhere, a
later reference, an Open Thread, a beat in a chapter not yet written. Propose
an adjustment for each. **Now / Later (log it as an Open Thread)**.

## Phase 3: Read through

When all items are done, reread the chapter as a whole. If an integrated
passage reads like a patch, offer to smooth the join without changing what
it says, and wait for approval before doing it.

## Phase 4: Record

- Demolition Log: set each applied item to `integrated <date>`.
- Continuity Ledger, Open Threads and Decisions: update for every changed fact.
- Beats file: if the chapter's events changed, update its beats and mark
  them `(Changed in integrate)`.
- Chapter Status: update the word count.

In a read-only claude.ai Project, write the full updated manuscript and RAMA
Log to outputs, and say which Project files to replace.

> [N] changes applied to Chapter 5; [D] deferred. Run `/rama:check 5` before moving on.
