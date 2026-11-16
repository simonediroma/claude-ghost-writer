---
name: beats
description: Create the story beats for one chapter of a RAMA book. Reads the outline entry, synopsis, story bible, style guide, the RAMA Log and every chapter already written, asks the author survey questions about anything unresolved, then writes a numbered beat list and saves it to the Beats file. Usage /rama:beats 5 (beats for the fifth chapter). Run before /rama:compose.
---

# RAMA: Beats

Turns the outline's entry for one chapter into a scene-by-scene beat list,
built on what the written chapters actually established, not just what the
outline planned.

Before starting, read `references/project-files.md` and `references/survey.md`.

## Arguments

`/rama:beats <n>`, where `<n>` is the chapter's ordinal number (see
`project-files.md → Chapter numbering`). With no number, use the first chapter
that has no beats in the RAMA Log's Chapter Status table, and say which one you
chose.

If no RAMA Log exists, say so and suggest `/rama:config` first. If the author
wants to go ahead anyway, work from the files you can find.

## Step 1: Read

Say right away: `Building beats for Chapter <n>: <chapter head>. Reading…`

Then read, in order:

1. **RAMA Log**: in full, especially the Decisions, Continuity Ledger and
   Open Threads.
2. **Outline**: the whole entry for chapter `n`, the entries for `n−1` and
   `n+1`, the Part overview this chapter sits in, and any Tracking tables that
   mention it (calendar, objects, evasions, custody).
3. **Synopsis**: in full.
4. **Story bible**: characters and places that appear in this chapter, the
   timeline around its dates, and its Open questions.
5. **Style guide**: POV, tense, register, structure and pacing rules,
   chapter-length and chapter-ending rules.
6. **Manuscript**: the **full text of chapter `n−1`**, and of `n−2` if the two
   are in one continuous sequence. For earlier chapters, read the opening and
   closing pages, and search for every character, object and place this
   chapter will use, reading each passage where it last appeared. If chapter
   `n` itself already exists, read it too and ask whether to re-beat it.
7. **Beats file**: earlier chapters' beats, so the structure doesn't repeat
   itself.

If earlier chapters are missing (beats for 5 with only 1–3 written), say so,
and work from the outline for the gap. Mark any beat that depends on the
unwritten chapter with `[DEPENDS ON CH 4]`.

## Step 2: Find what is unresolved

Before writing beats, list for yourself what the files don't settle for this
chapter:

- Outline beats the written chapters have since overtaken (a character who
  already knows something the outline has them learn here, or an object
  already moved).
- Open Threads due in this chapter or earlier and not yet paid off.
- Decisions the outline left open for this chapter ("decide in drafting").
- Choices with more than one good answer: whose scene opens the chapter,
  what's dramatized versus summarized, what's held back, how it ends.
- Facts the beats need that no file states (a date, a distance, a name).

## Step 3: Survey

Ask about the items from Step 2 that change the shape of the chapter, using
the survey method (three grounded options plus a write-in, up to four per
batch, at most three batches). Recommend when the written text or the style
guide points one way. Items that won't change the beats can wait for
`compose`. Note them for it.

If nothing is unresolved, say so in one line and skip the survey.

## Step 4: Write the beats

Write the beats as a numbered list, grouped by scene:

```markdown
## Chapter 5: In Which a Gentleman Comes Across the Bay

*Target ~3,600 words · Register: Dignity → Dread · POV: Harold, retrospective · Moon: two days before full*

**Function.** One or two sentences: what this chapter does for the book, and
what the reader knows at its end that they didn't at its start.

### Scene 1: The landing (≈900 words)
1. Sharp's skiff grounds below the station at the slack before the flood. Harold
   sees the boots first. *(Outline beat 1)*
2. …

### Scene 2: … (≈1,200 words)
…

**Ends on:** the concrete image the chapter closes with.

**Carry-forward**
- Continuity: facts this chapter will establish (for the Ledger).
- Threads opened: … / Threads paid off: …
- Held back: what the narrator withholds here, and where it pays off.

**For compose:** open questions deferred from the survey, plus [ASSUMED] items.
```

Rules for the beats:
- Each beat is one or two sentences: an action, a turn, a revelation or an
  image. Not prose, and not a summary of feelings.
- Tag beats that come straight from the outline `(Outline)`. Mark beats you
  added or changed `(New)` or `(Changed: <why>)`, so the author sees every
  departure from the outline.
- Respect the style guide's structural rules: no scene break before the first
  scene, the chapter-ending rule, how often the narrator addresses the reader,
  and its frame/tense rules.
- Scene word estimates should add up to the chapter target.
- Every survey answer must show up in a beat.

## Step 5: Review and save

Show the beats and ask a single survey question: **Approve / Approve with the
changes I'll describe / Rework a scene**. Revise until approved.

Then save:
- Add or replace the chapter's section in `<Title> — Beats.md` (create the
  file if needed, with `# <Title> — Beats` as its first line). Keep chapters in
  order.
- In the RAMA Log: set Chapter Status → Beats `✓ <date>`, add new Decisions,
  and update Open Threads.

Finish with:

> Beats for Chapter <n> saved ([S] scenes, ~[W] words planned). Next: `/rama:compose <n>`.
