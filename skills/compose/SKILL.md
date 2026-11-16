---
name: compose
description: Ghost-write one chapter of a RAMA book from its approved beats, following the style guide to the letter. Asks any remaining questions as a survey first, drafts the full chapter, self-checks it against the style guide's checklist, and adds it to the manuscript file once the author approves it. Usage /rama:compose 5. Run after /rama:beats 5.
---

# RAMA: Compose

Writes the chapter. The beats say what happens, and the style guide says how
it reads. Your job is prose the author would sign.

Before starting, read `references/project-files.md` and `references/survey.md`.

## Arguments

`/rama:compose <n>`. With no number, use the first chapter that has beats and
no draft, and say which.

If chapter `n` has no beats in the Beats file, ask in a survey: **Run beats
first (Recommended) / Compose straight from the outline / Cancel.**

If chapter `n` is already in the manuscript, ask: **Write a fresh draft to
compare / Revise the existing text against the beats / Cancel.** Never
overwrite written text without that answer.

## Step 1: Read

Say right away: `Composing Chapter <n>: <chapter head>. Reading…`

1. **Style guide**: **in full, every time.** It is the governing document. Pay
   special attention to banned constructions, punctuation quotas, POV limits,
   register samples and the revision checklist.
2. **Beats**: this chapter's section, including *For compose* and [ASSUMED].
3. **RAMA Log**: Decisions, Continuity Ledger and Open Threads.
4. **Outline**: this chapter's entry and its Tracking rows.
5. **Story bible**: characters, places and facts the beats touch.
6. **Manuscript**: the **full text of the previous chapter** (for voice,
   rhythm and the exact handoff), plus the opening of the first chapter as a
   voice anchor. Look up the earlier passage behind every Continuity Ledger
   fact the beats rely on.

## Step 2: Last questions

Survey only what's still open: the beats' *For compose* list, [ASSUMED] items
the author hasn't confirmed, and anything the read turned up (a beat that now
conflicts with the Ledger, say). Use up to two batches. If nothing is open,
skip straight to drafting and say so in one line.

## Step 3: Draft

Write the whole chapter in one pass, in the manuscript format from
`project-files.md`:

- Heading: `## <Designation>: <Chapter head>` exactly as the RAMA Log
  specifies. If this chapter opens a Part, put the Part heading (and any frame
  passage the outline puts there) above it.
- One scene per beat group. Use the style guide's scene-break mark between
  scenes, with no break before the first scene.
- Hit the target length within ±10%.
- Follow every beat, in order. If the prose needs a beat changed, change it,
  and report the change in Step 5. Don't drop one silently.

Prose discipline:
- **The style guide wins** over your own habits, the outline's wording and
  genre convention. When it bans a construction, don't use it even once.
- Match the voice of the written chapters, not a generic version of the genre.
  Reread the register samples if the book has them.
- Concrete and specific: names, objects, weather, tools and period detail
  from the bible and outline. Never invent a fact that contradicts the Ledger.
  When you must invent one (a minor name, a distance), log it in Step 6.
- End on the image or line the beats give for *Ends on*.
- Avoid the stock AI tells: not-X-but-Y contrasts, triads by reflex, one-line
  zingers closing paragraphs, staged openers, stacked em dashes, abstract
  emotional summary after a concrete moment, and "something shifted"
  vagueness. If the style guide has its own list, it covers these too.

## Step 4: Self-check before showing

Go through the draft against the style guide's **Revision Checklist** (or, if
there is none, its stated rules) and against the beats. Fix what you find
before showing the draft. Count anything the guide quantifies (em dashes per
1,000 words, addresses to the reader per chapter). Don't show the author a
draft you know breaks a rule.

## Step 5: Present

Show the full chapter. Then a short note, no more than eight lines:

```
Chapter 5 · 3,640 words (target 3,600) · 4 scenes
Beats changed: 3.2 (Sharp names the boat, not Harold; the POV rule required it)
New facts: Sharp's skiff is the *Ruth*; the landing is the north cove
Checklist: passes. Em dashes 3 (quota 3)
Open: none
```

Then ask with a survey: **Accept and add to manuscript / Revise (I'll say
what) / Retune the voice (run /rama:retune).** Revise as many rounds as the
author wants. Show only the changed passages after the first round, unless
they ask for the whole chapter.

## Step 6: Save

Once accepted:

1. **Manuscript**: insert the chapter into `<Title>.md` in outline order (after
   chapter `n−1` and before `n+1`, if that exists), or replace the existing
   chapter if the author chose revision. Create the manuscript with
   `Title:` / `Author:` lines first if it doesn't exist.
2. **RAMA Log**:
   - Chapter Status → Draft `✓ <date>`, Words.
   - Continuity Ledger → every new concrete fact this chapter establishes.
   - Open Threads → mark payoffs and add threads opened.
   - Decisions → any choice made in this step that changes the book.
3. **Beats file**: if beats changed in drafting, update the chapter's beats to
   match what was written and mark the changes `(Changed in compose)`.

In a read-only claude.ai Project, write the full updated manuscript, RAMA Log
and Beats file to outputs, and say which three Project files to replace.

Finish with:

> Chapter <n> added to the manuscript ([W] words; book total [T] / [target]).
> Next: `/rama:check <n>`, or `/rama:beats <n+1>`.
