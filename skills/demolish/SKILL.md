---
name: demolish
description: Hostile critical read of a drafted RAMA chapter. Finds its structural and dramatic weaknesses (unearned turns, thin motivation, slack scenes, plausibility gaps, cheats against the POV, promises the chapter breaks) and presents them one at a time for the author to answer. No fixes are offered during demolition; resolved responses go to /rama:integrate. Usage /rama:demolish 5, or /rama:demolish 5 --light for the three worst problems only.
---

# RAMA: Demolish

*Adapted from ghost-writer's `demolish` (MIT, Simone Di Roma), refocused for fiction.*

Read `references/project-files.md` and `references/survey.md` first.

`check` asks whether the chapter obeys the rules. `demolish` asks whether
it **works**. It reads as the toughest editor the book will meet.

## Rules (non-negotiable)

- One criticism at a time. Always.
- Do not soften the criticism.
- Do not offer solutions during demolition. Solutions come in integration.
- Do not move to the next criticism until the current one is resolved or deliberately deferred.
- Attack specific passages, choices and implications, never "the chapter in general."
- The goal is a stronger book, not a defeated author.

## Phase 0: Read

The chapter in full. Its beats and outline entry. The synopsis. The RAMA Log
(Decisions, Ledger, Open Threads, and the `## Demolition Log` section if
present). The chapters immediately before and after, if written.

If the RAMA Log's Demolition Log has entries for this chapter: don't raise
`resolved` or `integrated` issues again; raise `deferred` ones first; skip
`accepted` ones unless something new makes them critical. Say in one line
what earlier cycles left.

## Phase 1: Map the weaknesses (internally)

- **Causality**: does each turn follow from what came before, or does it
  happen because the outline needs it? Coincidences that do plot work.
- **Motivation**: does each character act from what they want, fear and
  know at this point? Would they really do this here?
- **Stakes and tension**: what is at risk in each scene? Scenes where nothing
  changes. Tension released too early.
- **POV and knowledge**: does the narrator claim what he couldn't know?
  Does hindsight cost him anything, or is it free?
- **Structure**: the opening (does it start in the right place?), scene
  order, proportion (what's dramatized versus summarized), and the ending
  (does it land on the image, or explain it?).
- **Promises**: setups made here that the book can't pay off, and payoffs
  the reader wasn't set up for.
- **Plausibility**: period, procedure and physical logic (tides, distances,
  how long things take).
- **Theme**: is the chapter saying something the book argues against
  elsewhere?

## Phase 2: Prioritize

Rank by damage to the reader's trust. Start with the worst. In `--light`
mode, keep only the three worst.

## Phase 3: One at a time

State the problem precisely, with location and quote. Say why it matters:
what it costs the reader. Then:

> How do you answer this?

## Phase 4: Weigh the answer

A **strong** answer changes the chapter (or a plan for a later one), narrows
what the chapter claims, gives a reason in the story that genuinely answers
the point, or accepts the limit knowingly. A **weak** answer restates the
intent ("what I meant was…"), changes the subject, or concedes without a
change.

If weak: restate the problem and ask again. If the author is stuck, go step
by step: rephrase it more simply; narrow it to the single passage; ask what
feels true; then offer a survey **Change the scene / Change the setup
earlier / Accept it as a known limit / write-in**, without filling in
the content.

If still stuck, defer it.

If strong:

> That works. It adds: [one line]. Next criticism, or integrate now?

## Phase 5: Log

When the author stops or the list is exhausted, add to the RAMA Log under
`## Demolition Log` (create the section after Check History):

```markdown
### Chapter 5 · cycle 1 · 2026-11-21
| Issue | Kind | Status | Resolution |
|---|---|---|---|
| Sharp's arrival at slack water is convenient | causality | resolved | Keziah sent for him in ch 4; plant a line there |
```

Status is one of `resolved` / `deferred` / `accepted`. A resolution that
changes the book also goes under Decisions.

> Logged. Run `/rama:integrate 5` to apply the resolved answers to the text.
