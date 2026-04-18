---
description: Runs a demolition of a chapter from the perspective of a specific reader persona. Use after the standard demolish cycle, or instead of it when you want a specific type of reader's reaction. Available personas: target-reader, hostile-reader, domain-expert, editor, out-of-target. The author can also create custom personas. Each persona finds different problems — run multiple for a full picture.
---

# Skill: Persona Demolition

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


Standard demolition attacks logical and structural weaknesses. Persona demolition asks: how does a specific type of reader actually experience this text?

The two are complementary. Run standard `demolish` for argument integrity. Run `demolish-persona` for reader experience.

---

## Setup

Read:
1. `book.config.json` — preset, voice profile, target reader definition
2. The chapter file specified by the author
3. The chapter's Demolition Log — note which standard demolition cycles have already run

Ask the author:
> Which persona do you want to run?
>
> **Default personas:**
> - `target-reader` — the reader this book was written for
> - `hostile-reader` — skeptical, looking for reasons to disbelieve
> - `domain-expert` — knows the field, notices what's missing or overclaimed
> - `editor` — structural and prose diagnosis, not argument evaluation
> - `out-of-target` — completely outside the assumed audience
>
> **Custom personas:** describe who you want, or name a file in `personas/`.
>
> You can run more than one — but run them sequentially, one at a time.

---

## Running a Default Persona

Load the corresponding file from `personas/`:
- `personas/target-reader.md`
- `personas/hostile-reader.md`
- `personas/domain-expert.md`
- `personas/editor.md`
- `personas/out-of-target.md`

For `target-reader`: read `book.config.json → book_profile → target_reader` and internalize that specific profile before proceeding.

For `domain-expert`: read `book.config.json → book_profile` to understand the subject domain.

Fully inhabit the persona. Read the chapter as that person — not as an analyst describing what that person would think, but as that person reacting in real time.

---

## Running a Custom Persona

If the author describes a custom persona, build it using this structure before proceeding:

```
Custom Persona: [name]

Who I am: [background, profession, age, knowledge level]
Why I picked up this book: [motivation]
What I know coming in: [relevant prior knowledge]
What I don't know: [relevant gaps]
What would make me put it down: [threshold]
My primary concern as a reader: [what I'm looking for]
```

Ask the author to confirm the persona before proceeding.

Offer to save it: > Do you want to save this persona to `personas/[name].md` for future use?

---

## The Persona Read

Read the chapter fully in character. Do not break character to offer meta-commentary. React as the persona reacts.

As you read, track:
- Moments of confusion or disengagement (for target-reader, out-of-target)
- Objections and skepticism (for hostile-reader)
- Technical gaps and overclaims (for domain-expert)
- Structural and prose problems (for editor)

---

## Feedback Format

Present feedback in the persona's voice — first person, specific, with exact locations in the text where possible.

```
PERSONA READ — [Persona Name] on [Chapter Title]

Opening reaction:
[One sentence: first impression as this persona]

What worked:
- [specific moment or passage] — [why it worked for this persona]

What didn't work:
1. [specific problem, with location] — [persona's reaction]
2. [specific problem, with location] — [persona's reaction]
3. [specific problem, with location] — [persona's reaction]

The moment I almost stopped reading:
[specific passage or moment, if any]

What I'll remember from this chapter:
[what the persona takes away — or "nothing specific"]

One thing I wanted that I didn't get:
[the persona's unmet expectation]
```

Then step out of character and say:
> That's the [persona name] read. Of these issues, which do you want to address?

---

## After the Persona Read

For issues the author wants to address:
- Route to `integrate` for text changes
- Route to `ask-before-writing` if the issue is conceptual (the problem is upstream of the text)

Update the Demolition Log in the chapter file — add a new entry:

```
### Persona Cycle — [Persona Name] — [date]

| Issue | Type | Status |
|---|---|---|
| [issue] | persona-[name] | resolved / deferred / accepted |
```

Update `demolition-history.md`:
- Add persona cycle to the chapter's Full Log section
- If a persona issue matches a pattern seen across chapters → add to Recurring Patterns

---

## Running Multiple Personas

If the author wants to run more than one persona on the same chapter, complete one full cycle — read, feedback, author response, log update — before starting the next.

Do not blend personas. Each persona sees different things. Mixing them produces generic feedback that could have come from anyone.

Suggested sequence for maximum coverage:
1. `editor` — structural problems first (no point polishing a broken structure)
2. `target-reader` — does it work for the intended audience?
3. `hostile-reader` — does the argument hold under pressure?
4. `domain-expert` — is it accurate and complete?
5. `out-of-target` — what is being assumed without knowing it?
