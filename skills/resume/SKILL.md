---
name: resume
description: Where am I? Reads the RAMA Log, beats, manuscript and latest check report, and gives a short briefing on where the book stands, plus the single next step to take. Run whenever you open a RAMA project and don't remember where you left off. Usage /rama:resume.
---

# RAMA: Resume

*Adapted from ghost-writer's `resume` / `session-start` (MIT, Simone Di Roma).*

Read `references/project-files.md` first.

## Read, lightly

1. RAMA Log: in full.
2. Beats file: headings only.
3. Manuscript: chapter headings and word counts only.
4. `<Title> — Check Report.md`: header and Status column only.
5. `<Title> — Corrections.md` (if present): count the open rows.
6. File modification times, to see what was touched last.

If no RAMA Log exists, the only recommendation is `/rama:config`.

## Brief

Keep it to ten lines at most:

```
THE SHAPE OF THE SEA · 9 of 25 chapters drafted · 31,400 / 89,000 words
Last touched: Chapter 9, composed 2026-11-18
Beats ready, not composed: 10
Check: chapters 1–8 checked; 9 not yet. 2 open findings (ch 7)
Open threads due soon: the Cranmers' net-shed key (pays off ch 11)
Decisions logged: 23

→ Next: /rama:check 9
```

## Choosing the one next step

Take the first rule that applies:

1. A Check Report has open Critical findings → `/rama:check <scope>` (resume fixing).
2. Open corrections in the queue → `/rama:corrections`.
3. A chapter composed and never checked → `/rama:check <n>`.
4. A chapter with beats and no draft → `/rama:compose <n>`.
5. The next outline chapter has no beats → `/rama:beats <n>`.
6. All chapters drafted and checked → `/rama:check all`, then `/rama:compile`.

Give one recommendation, then a single line naming one alternative if there
is an obvious one. Don't change any files.
