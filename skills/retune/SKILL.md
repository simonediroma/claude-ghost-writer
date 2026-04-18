---
description: Use when the author reads a draft and says "this doesn't sound like me." Takes free-form input from the author — how they would say it, a voice note transcribed, a rough rewrite, anything — and uses it to retune the chapter to their actual voice. Not a structural critique. Not a demolition. A voice realignment.
---

# Skill: Retune

> **Language**: Read `book.config.json → language`. Write all output in that language. Default: English.

The author reads the draft and feels something is off. Not wrong — off. The words are right but the voice isn't theirs.

This skill fixes that. It takes whatever the author gives — a few sentences, a ramble, a voice note transcribed, a rough rewrite of one paragraph — and uses it as a fresh voice sample to realign the chapter.

No demolition. No structure critique. Just: make it sound like them.

---

## Rules

- Do not evaluate the author's raw input for quality. It is a voice sample, not a draft.
- Do not explain what you changed or why — just show the result.
- Never make structural changes. Retune keeps the content and order intact — only voice, rhythm, and word choice change.
- One pass at a time. Show the result, ask if it's closer.

---

## Phase 0 — Get the Chapter and the Sample

Ask:
> Which chapter feels off?

Read the chapter file.

Then ask:
> Show me how you'd say it. Don't try to write well — just talk. A few sentences, a voice note you transcribed, even just how you'd explain it to a friend. The rougher the better.

Wait. Do not suggest anything. Do not give examples. Let them produce something unguided.

If the author says they don't know how to start:
> Pick the part of the chapter that feels most wrong. Read it out loud. Now say the same thing in your own words — as if you're telling it to someone at dinner. Type that.

---

## Phase 1 — Analyze the Gap

Read both texts — the chapter draft and the author's raw input — side by side.

Internally identify the specific differences. Do not present this analysis to the author. Just use it.

Look for:

**Sentence length**: Is the draft longer and more complex than how they naturally speak? Or more clipped?

**Word choice**: Does the draft use more formal, literary, or abstract words than the sample? What specific words did the author use that the draft avoided?

**Rhythm**: Does the draft flow smoothly where the author's natural voice would land harder? Does the draft hedge where they're direct?

**Pronoun distance**: Does the draft describe things from outside ("one might notice") where the author speaks from inside ("I saw")?

**Energy**: Where does the author's sample have heat — opinion, impatience, humor, conviction — that the draft flattened into neutral prose?

**Specificity**: Does the author's sample use concrete details, names, numbers, sensory details that the draft replaced with abstractions?

---

## Phase 2 — Retune the Chapter

Rewrite the chapter preserving:
- All content — nothing added, nothing removed
- All structure — same order, same sections
- The meaning of every sentence

Change only:
- Word choice → toward the author's vocabulary from the sample
- Sentence length and rhythm → toward how they naturally speak
- Level of formality → toward their register
- Specificity → toward their concrete details where available
- Energy level → toward their natural heat or directness

If the author used a specific phrase or expression in the sample that fits, use it verbatim in the retune — even if it's rough. Their actual words are the goal, not polished versions of their words.

---

## Phase 3 — Present the Result

Show the retuned chapter without preamble. No explanation of what changed.

After the chapter, say only:
> Is this closer?

Three possible responses:

**Yes** → done. Update the chapter file. Update `book.config.json → author_voice` with any new patterns extracted from the sample — add specific phrases to `signature_phrases`, note any new vocabulary patterns.

**Closer but still off** → ask: > What's still wrong? Show me another passage — how you'd say that specific part.
Run another retune pass on the sections still off.

**No, it's worse** → ask: > What specifically got worse? Point me to a sentence.
Revert to the original for that section. Try a narrower retune.

---

## After a Successful Retune

Update `book.config.json → author_voice`:
- Add new `signature_phrases` found in the sample
- Update `rhythm` if the sample revealed something the original profile missed
- Add to `avoid` if specific patterns in the draft were consistently wrong

Tell the author:
> Voice profile updated with what I learned from your sample. Future chapters will use this.

This is the most important output of the retune — not the fixed chapter, but the improved voice profile that makes future chapters need less fixing.
