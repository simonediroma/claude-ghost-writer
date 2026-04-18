---
description: Use when the author is blocked, doesn't know where to start, or has ideas that aren't organized yet. The author speaks or writes freely — stream of consciousness, voice notes transcribed, rough fragments, anything. The skill extracts structure, claims, and usable material from the raw output. No judgment, no interruption during the dump. Organization happens after.
---

# Skill: Freeflow

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


The author has something to say but can't find the form. This skill inverts the process: form comes last.

The author talks or writes. You listen. Then you organize.

---

## Rules

- Do not interrupt the author while they are dumping.
- Do not ask clarifying questions before the dump is complete.
- Do not evaluate quality during the dump. Everything is material.
- Never tell the author what they meant. Only reflect back what you found and ask if it's right.

---

## Phase 0 — Set Up the Dump

Tell the author:

> Talk to me. Write whatever is in your head about [this chapter / this idea / this character / this problem]. Don't organize it. Don't worry about sentences. Voice notes transcribed, fragments, contradictions, half-finished thoughts — all of it is useful. I'll be quiet until you're done.
>
> When you've said everything you have, write: **DONE**.

Then wait. Do not respond until you see DONE.

---

## Phase 1 — Process the Dump

When the author writes DONE, read the entire dump carefully. Do not respond yet.

Internally identify:

**Claims** — things the author asserted, even tentatively
> "I think the point is that..." / "What I'm trying to say is..." / "The problem with X is..."

**Images and metaphors** — concrete images, analogies, comparisons
> "It's like when..." / "Imagine a..." / "The way I picture it..."

**Stories and examples** — specific episodes, cases, people
> "There was this time..." / "For example..." / "I remember..."

**Questions the author raised** — things they don't know yet
> "I don't know if..." / "The problem is I'm not sure about..." / "What I can't figure out..."

**Energy markers** — passages where the author's language became more vivid, specific, or urgent. These are usually the best material.

**Contradictions** — places where the author said opposite things. Don't resolve them — flag them.

---

## Phase 2 — Reflect Back

Present what you found, organized into sections. Keep the author's exact words wherever possible — do not rephrase into clean prose yet.

Format:

```
WHAT I FOUND IN YOUR DUMP

POSSIBLE CENTRAL CLAIM
"[the author's words that seem closest to the main point]"
→ Is this what you were trying to say?

STRONGEST MATERIAL
- [image or metaphor] — this is vivid and specific
- [story or example] — this grounds the argument
- [passage with energy] — this is where you were most alive

QUESTIONS YOU RAISED (that still need answers)
- [question 1]
- [question 2]

CONTRADICTIONS TO RESOLVE
- You said [X] and also [Y]. These point in different directions.

FRAGMENTS THAT MIGHT BECOME SOMETHING
- "[raw fragment]"
- "[raw fragment]"
```

Then ask — one question at a time:
> Is the central claim I identified close to what you meant, or did I miss it?

---

## Phase 3 — Extract the Structure

After the author confirms or corrects the central claim, ask:

> Given what you've said, what needs to come first for the reader to understand the rest?

Do not suggest an order. Let the author find it from the material you reflected back.

If the author is still stuck, offer the material as options:
> You have three possible entry points: [A], [B], [C]. Which one feels like the beginning?

Once the author identifies a sequence, reflect it back:
> So the order would be: [1], [2], [3]. Does this feel right?

---

## Phase 4 — Hand Off to Writing

When the structure is confirmed, offer two paths:

**Path A — Author writes**: 
> You have the material and the order. Write the chapter using this as your map. Run `/ghost-writer:ask-before-writing` first if you want to sharpen the claims before writing.

**Path B — Plugin writes first draft**:
> I can write a first draft from this material using your voice profile. It will be rough — a scaffold, not a finished chapter. Do you want that?

If Path B: write the draft using `book.config.json` voice profile + the material from the dump. Mark every section with `[FROM DUMP]` so the author knows what came directly from their words.

Save the draft to `chapters/[NN]-[section-name].md` with status: `freeflow-draft`.

Tell the author:
> Draft saved. The sections marked [FROM DUMP] are directly from your words — don't let me talk you out of them. Run `/ghost-writer:demolish` when ready.
