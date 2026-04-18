---
description: Full review macro. Runs demolition from all five reader personas in sequence — editor, target-reader, hostile-reader, domain-expert, out-of-target — then integrates all responses. Supports resume: if interrupted mid-review, picks up from the last completed persona.
---

# Macro: Review

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


Five reader perspectives on one chapter. Supports resume — if interrupted, picks up from the last completed persona.

---

## Session Check

Read `sessions/review-[chapter-slug].md` if it exists.

If open session exists:
> You started a review of [chapter] but didn't finish. Last completed persona: [persona]. Resume, or start over?

If resuming → skip completed personas.
If new → create `sessions/review-[chapter-slug].md`:

```markdown
# Session: review — [chapter file]

> Created: [date]
> Last updated: [date]
> Status: open

## Target
[chapter file]

## Personas completed
- [ ] editor
- [ ] target-reader
- [ ] hostile-reader
- [ ] domain-expert
- [ ] out-of-target

## Current persona
editor

## Issues found
[accumulated as personas complete]
```

---

## Setup

Ask:
> Which chapter do you want to review? [list available files]

If never been through standard `demolish`:
> No standard demolition yet. Persona reads work best after basic argument stress-testing. Run `/ghost-writer:demolish` first, or proceed anyway?

---

## The Sequence

Run each persona in order. After each completes, update session file — check off persona, note issues found, update current persona.

**Persona 1 — Editor** → update session → say: "Editor done. Moving to target reader."
**Persona 2 — Target Reader** → update session → say: "Target reader done. Now the skeptic."
**Persona 3 — Hostile Reader** → update session → say: "Hostile reader done. Now the expert."
**Persona 4 — Domain Expert** → update session → say: "Expert done. Last read: the outsider."
**Persona 5 — Out of Target** → update session → mark all personas complete.

At any point the author can stop. On next run of `/ghost-writer:review`, session is detected and resumed.

---

## Consolidation and Integration

Present consolidated issue list. Run `integrate` on confirmed issues.

Mark session `status: complete`.

```
REVIEW COMPLETE — [Chapter Title]
─────────────────────────────────────
Personas: editor ✅ target ✅ hostile ✅ expert ✅ outsider ✅
Issues found: [N] | Resolved: [N] | Deferred: [N]
Session: closed ✅
```


This macro runs a complete multi-persona review of a chapter. Five different readers. One integration pass at the end.

It takes longer than a standard demolition. Use it on chapters that carry significant weight — the opening chapter, the chapter with the hardest argument, any chapter you're not sure about.

---

## Setup

Ask:
> Which chapter do you want to review? [list available chapter files]

Read the chapter file, its Demolition Log, and `demolition-history.md` to understand what has already been done.

If the chapter has never been through standard `demolish`, say:
> This chapter hasn't been through a standard demolition yet. The persona reads work best after the basic argument has been stress-tested. Do you want to run `/ghost-writer:demolish` first, or go straight to persona reads?

---

## The Sequence

Run the five personas in this order. Complete each fully — read, feedback, author responses — before moving to the next. Do not blend personas.

**Persona 1 — Editor**
Tell the author:
> First read: the editor. They're looking at structure and prose, not argument. They don't care if you're right — they care if the chapter works.

Run `demolish-persona` with `editor` persona. Collect all issues and author responses.

When complete:
> Editor done. Moving to your target reader.

---

**Persona 2 — Target Reader**
Tell the author:
> Second read: your target reader. [one-line description from book.config.json]. They want this book to work. They'll tell us where it didn't.

Run `demolish-persona` with `target-reader` persona.

When complete:
> Target reader done. Now the skeptic.

---

**Persona 3 — Hostile Reader**
Tell the author:
> Third read: the hostile reader. They're looking for reasons not to believe you. Every unsupported assertion, every avoided objection — they find it.

Run `demolish-persona` with `hostile-reader` persona.

When complete:
> Hostile reader done. Now the expert.

---

**Persona 4 — Domain Expert**
Tell the author:
> Fourth read: the domain expert. They know this field. They notice what's missing, overclaimed, or borrowed without attribution.

Run `demolish-persona` with `domain-expert` persona.

When complete:
> Expert done. Last read: the outsider.

---

**Persona 5 — Out of Target**
Tell the author:
> Fifth read: someone completely outside your assumed audience. They reveal what the chapter assumes without knowing it.

Run `demolish-persona` with `out-of-target` persona.

---

## Consolidation

After all five personas, present a consolidated issue list before integrating:

```
FULL REVIEW — [Chapter Title]
─────────────────────────────────────
Issues found across all 5 personas: [N total]

CRITICAL (multiple personas flagged this)
- [issue] — flagged by [editor, hostile-reader]

SIGNIFICANT
- [issue] — [persona]
- [issue] — [persona]

MINOR / EXPERT-ONLY
- [issue] — [persona] — note: general reader may not notice
```

Ask:
> Before we integrate: are there any issues here you want to discuss, or any you want to skip? Or shall we go through them all?

---

## Integration

Run the full `integrate` skill on all confirmed issues.

---

## When Complete

```
REVIEW COMPLETE — [Chapter Title]
─────────────────────────────────────
Version: [N]
Personas run: editor, target-reader, hostile-reader, domain-expert, out-of-target
Issues found: [N] | Resolved: [N] | Deferred: [N] | Accepted: [N]
─────────────────────────────────────
```

Then say:
> This chapter has been through the full review cycle. Run `/ghost-writer:chapter` for the next chapter, or `/ghost-writer:consistency-check` if you have 3+ chapters complete.
