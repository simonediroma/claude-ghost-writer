---
name: check
description: Make a RAMA chapter tip-top. Checks style-guide compliance (every rule and the revision checklist), outline and beats compliance, continuity against the rest of the book and the story bible, timeline, character facts, period accuracy, and copy-editing. Writes a ranked report, then goes through the fixes one at a time, applying each only with the author's OK. Usage /rama:check 5, /rama:check 5-7, or /rama:check all.
---

# RAMA: Check

The editorial pass that runs after `compose`. It finds everything that would
make a careful reader, editor or copy-editor stop. Then it fixes each problem
with the author's approval.

Before starting, read `references/project-files.md` and `references/survey.md`.

## Arguments

- `/rama:check 5`: one chapter, checked against everything before it.
- `/rama:check 5-7`: a range, checked as a unit and against what comes before it.
- `/rama:check all`: the whole manuscript as it stands.
- Optional `--only style,outline,continuity,timeline,characters,accuracy,copy`
  to run some passes only.

No argument: check the most recently composed chapter, and say which.

## Step 1: Read

Say right away: `Checking <scope>: <passes>. Reading…`

1. **Style guide**: in full. Build the working checklist from its Revision
   Checklist, plus every rule elsewhere in the guide that the checklist
   doesn't already cover (banned constructions, quotas, POV limits, orthography,
   dialogue punctuation, chapter-head form, section-break rules). Give each
   item an ID by section, e.g. `IX.3` or `XIX-Prose-5`, so findings can cite
   it.
2. **RAMA Log**: Decisions (these override the outline and bible), the
   Continuity Ledger, Open Threads and Check History.
3. **Outline**: entries for the chapters in scope, plus the Tracking tables.
4. **Beats**: entries for the chapters in scope.
5. **Story bible**: characters, places, timeline and rules the chapters touch.
6. **Manuscript**: the chapters in scope **in full**. For continuity on a
   single chapter or a range, search the earlier chapters for every name,
   object, place, date and number the chapters in scope use, and read those
   passages. Don't rely on memory or summaries. For `all`, read everything.

Check the latest `<Title> — Check Report.md` (if present) for findings the
author marked **intentional**. Don't raise those again.

## Step 2: The passes

Locate every finding as `ch.para`, following `project-files.md → Paragraph
IDs`. Quote the exact text: the shortest span that shows the problem.

**1. Style guide (`S`).** Every checklist item and rule, line by line. Count
what the guide quantifies (e.g. em dashes per 1,000 words of narration,
addresses to the reader per chapter) and report the count against the limit.
Flag banned words and constructions every time they occur, not just once.
Check the chapter heading against the guide's chapter-head form and the
scene-break mark against its rule.

**2. Outline and beats (`O`).** Every beat for the chapter is present and in
order. The *Ends on* image closes the chapter. Tracking rows are honored (the
moon phase, who holds the key, which evasions are kept). Flag beats that are
missing, out of order or contradicted, and outline promises the chapter should
have kept. A Decision in the RAMA Log overrides the outline. Don't flag text
that follows a Decision.

**3. Continuity (`K`).** Every concrete detail in scope that also appears
elsewhere (objects, places, layouts, distances, names and spellings, quoted
words recalled later, numbers, rules of the world) must match its first
mention and the Ledger. Name the first mention as canonical unless a Decision
says otherwise.

**4. Timeline (`T`).** Dates, seasons, weekdays, moon and tide where the book
tracks them, ages, durations ("three days later"), and the order of events.
Flag impossible sequences, characters in two places at once, and weather or
daylight that doesn't fit the date.

**5. Characters (`C`).** Facts (age, look, relationships, forms of address)
against the bible, `characters/` profiles and earlier chapters. Also voice and
behavior: does each character speak and act as established? Flag knowledge
a character shouldn't have yet, and anything the POV rules say the narrator
cannot know.

**6. Accuracy (`A`).** For historical or technical books: anachronistic
words, objects, idioms and psychology; terminology the guide says to get right;
real places and events. Mark items you can't verify as `verify`. Don't guess.
If the `fact-check` skill is available, offer to hand the `verify` items to it.

**7. Copy (`G`).** Spelling (in the book's chosen variant and orthography),
typos, repeated words, agreement, tense slips, pronoun reference, and
punctuation consistency (quotes, dashes, ellipses, serial comma, numbers).
Don't flag what the style guide deliberately mandates (period spellings,
dialect).

**8. Craft (`P`).** Things not covered by a rule that still weaken the
chapter: a scene that restates the previous one, an echoed word in close
range, a paragraph that explains what the scene already showed, a slack
opening, an ending that softens the closing image, and AI tells (not-X-but-Y,
reflexive triads, aphoristic closers, abstract emotional summary).

## Step 3: The report

Grade each finding:
- **Critical**: a reader will notice and lose trust (a continuity break, a POV
  violation, a beat that contradicts the plot, a banned construction the guide
  puts in bold).
- **Major**: noticeable on a careful read, or a clear rule violation.
- **Minor**: copy-editor level, or a matter of polish.

Write the report to `<Title> — Check Report.md` (it replaces the previous
one) and show it in chat:

```markdown
# Check Report: Chapters 5–7 · 2026-11-20
Passes: style, outline, continuity, timeline, characters, accuracy, copy, craft
Findings: 14 (Critical 2 · Major 5 · Minor 7)
Counts: em dashes ch5 3/3.6 · ch6 5/3.9 ✗ · addresses to reader ch5 1 · ch6 0 · ch7 1

| ID | Sev | Where | Text | Problem | Proposed fix | Status |
|---|---|---|---|---|---|---|
| K1 | Critical | 6.14 | "the shed's landward door" | Ch 4.9 (first mention) and the Ledger put the door to seaward | "the shed's seaward door" | open |
| S1 | Major | 5.22 | "rather than wait" | Banned: "rather than" (IX) | "and did not wait" | open |
```

Then a three-line summary: the worst problem, the main pattern (if the same
rule broke several times), and whether the chapters are clear to compile.

If a pass finds nothing, say `No <pass> findings.` in the report.

## Step 4: Fix, with the author's OK

Ask in a survey: **Go through fixes one at a time (Recommended) / Apply all
Minor copy and punctuation fixes at once, then the rest one at a time / Stop
here; I'll fix them myself.**

Then for each finding, in order of severity:

```
K1 · Critical · 6.14
Current:  …she went out by the shed's landward door and…
Proposed: …she went out by the shed's seaward door and…
Why: Ch 4.9 and the Ledger put the door to seaward.
```

Ask: **Apply / Apply with my change / Keep as is (intentional) / Skip for now.**

- Change only the quoted span and what it needs to read cleanly. Never
  rewrite around a fix, and never change voice.
- Every replacement text must itself pass the style guide.
- After each fix, check for knock-on effects (the same detail elsewhere, a
  later reference to it). Raise any you find as a new finding next in the
  queue.
- Update the finding's Status in the report: `fixed`, `intentional`, or
  `skipped`.
- **Intentional** items that set a precedent (a deliberate exception to a
  rule) go in the RAMA Log under Decisions, so later checks respect them.

The author can stop at any time. The report keeps the queue, and the next
`/rama:check` run offers to resume open findings first.

## Step 5: Close

1. Save the manuscript with the applied fixes. In a read-only claude.ai
   Project, write the full updated manuscript, report and RAMA Log to outputs,
   and say which Project files to replace.
2. RAMA Log:
   - Chapter Status → Last check `<date>` for each chapter.
   - Continuity Ledger → canonical values settled during fixing.
   - Check History → `<date> · check <scope> · <N> findings, <F> fixed, <I> intentional, <S> skipped.`
3. If one rule broke three or more times, suggest one clarifying line for the
   style guide (show it, and add it only on approval) and note the pattern for
   `compose`.

Finish with:

> Check complete for <scope>: [F] fixed, [I] kept, [S] open. [Clear to compile. | Open items remain; see the Check Report.]
