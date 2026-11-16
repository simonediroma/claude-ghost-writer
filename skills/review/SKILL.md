---
name: review
description: Read a RAMA chapter as a specific kind of reader (editor, target reader, hostile reader, period or subject expert, someone outside the audience, or a custom persona) and report how that reader actually experiences it. Run one persona or all five in sequence. Usage /rama:review 5 editor, /rama:review 5 all, or /rama:review 5 [custom persona file].
---

# RAMA: Review

*Adapted from ghost-writer's `review` and `demolish-persona` (MIT, Simone Di Roma).*

Read `references/project-files.md` and `references/survey.md` first.

## Personas

Persona files are in this skill's `personas/` folder. Custom personas can
also live in the project's `personas/` folder. Read only the `## Quick Summary`
of a persona file unless the author asks for a deep read, or this is the
persona's first run on this book.

| Persona | For fiction, reads for |
|---|---|
| `editor` | structure, pacing, scene proportion, openings and endings, seams |
| `target-reader` | absorption: where they lean in, where they skim, what they'll remember. Uses the target reader recorded in the RAMA Log (ask once and record it if missing) |
| `hostile-reader` | plausibility, motivation, coincidence, POV cheats, sentiment the story hasn't earned |
| `domain-expert` | the book's subject or period expert (for a 19th-century coastal book: a maritime historian). Checks anachronism, procedure, terminology |
| `out-of-target` | a smart reader with none of the genre's habits. Is the book letting them in? |

The persona files were written for non-fiction. For fiction, translate
"argument" as **story logic** and "claim" as **what the chapter asks the
reader to believe**.

**Custom persona:** if the author describes one, build it with
`personas/custom-template.md`, confirm it, and offer to save it to the
project's `personas/` folder.

## Run

Read the chapter in full, its beats, the synopsis, the style guide's voice
section, and the RAMA Log.

With `all`, run them in this order: editor → target-reader → hostile-reader
→ domain-expert → out-of-target. Before each one, ask in a survey: **Next
persona / Skip this one / Stop here.** Store progress in the RAMA Log
(`Review in progress: ch 5, done: editor, target-reader`) so the next
`/rama:review 5 all` picks up where this one stopped.

Read fully in character. No meta-commentary while in character.

```
PERSONA READ: [persona] on Chapter 5

Opening reaction: [one sentence]
What worked:
- [passage, as ch.para] — [why, for this reader]
What didn't:
1. [passage] — [reaction]
2. …
Where I almost stopped: [passage or "nowhere"]
What I'll remember: [or "nothing specific"]
What I wanted and didn't get: [one line]
```

Step out of character:

> That's the [persona] read. Which of these do you want to address?

## After

Log the issues the author takes up under `## Demolition Log` in the RAMA Log
(kind: `persona:<name>`), with status `resolved`, `deferred` or `accepted`,
exactly as `demolish` does. Then:

> Run `/rama:integrate 5` to apply them.
