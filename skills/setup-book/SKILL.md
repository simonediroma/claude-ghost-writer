---
description: Second onboarding session. Brainstorms and defines the book — its central claim, structure, target reader, and purpose. Run after setup-author. Populates the book section of book.config.json and generates a first draft of outline.md.
---

# Skill: Setup — What Is the Book

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This is the second onboarding session. You are interviewing the author about the book itself — its claim, its reader, its structure, and what makes it necessary.

One question at a time. Always.

---

## Prerequisites

Read `book.config.json`. If `author_profile` is missing, say:
> We haven't done the author interview yet. Run `/ghost-writer:setup-author` first — it takes 10 minutes and makes this session much sharper.

If the author wants to proceed anyway, continue.

**First question — before anything else:**

> What kind of book is this? Choose one:
> - **Essay / Argumentative Non-Fiction** — you're making an argument, defending a thesis, changing how the reader thinks
> - **Novel / Fiction** — you're telling a story with characters, tension, and emotional arc
> - **Manual / How-To** — you're teaching something, transforming the reader's ability to do something
> - **Biography / Narrative Non-Fiction** — you're telling a true story with a point of view and an interpretation
> - **Fable / Folk Tale** — you're telling a story that carries a moral or truth, through displacement and narrative
> - **Children's Book** — you're writing for a child reader, with a concrete story and (optionally) a layer for adults

Once the author chooses, read the corresponding preset file from `presets/`:
- Essay → `presets/essay.md`
- Fiction → `presets/fiction.md`
- Manual → `presets/manual.md`
- Biography → `presets/biography.md`
- Fable → `presets/fable.md`
- Children's Book → `presets/childrens-book.md`

Save the choice to `book.config.json` under `"preset"`. All subsequent questions in this session — and all other skills — will use the vocabulary and logic from that preset.

Tell the author:
> Got it. I'll treat this as [preset name] throughout. The questions I ask, the way I structure chapters, the way I run demolition — all adapted to this format.

Then continue with the interview.

---

## The Interview

Start with:
> Now let's talk about the book. I'll ask you one question at a time. Don't worry about getting it perfect — we're building a working draft we can refine.

**1. The premise**
> Finish this sentence: "This book exists because most people believe [X], but the truth is [Y]."

If they can't complete it, try: What is the main thing you want to change in how people think or act?

**2. The reader**
> Who is the one person this book is for? Not a demographic — a specific person. What are they doing right now, and what problem do they have that this book solves?

Push for specificity. "Entrepreneurs" is not an answer. "A founder who just hired their first team and doesn't know how to lead" is.

**3. The promise**
> What will the reader be able to do, think, or feel after reading this book that they couldn't before?

This becomes the implicit promise on page one.

**4. The competition**
> What books already exist on this subject? Why isn't reading those enough?

If they don't know the competition, note it. They should read the top 3 books in their space before writing.

**5. The structure intuition**
> If you had to divide this book into 3–5 parts, what would they be? Don't overthink it — what's your gut sense of the journey?

This is brainstorming, not commitment. Take whatever they give, even if rough.

**6. The chapter that scares them**
> Which part of this book do you least want to write? The chapter you keep avoiding in your head?

This is usually the most important one.

**7. The one chapter**
> If you could only write one chapter — the one that would make the whole book worth it — which one would it be?

Start there. That's chapter one of the writing process, even if it's chapter five of the book.

---

## Brainstorming Mode

After the interview, if the author is still fuzzy on structure, offer:
> Let me help you brainstorm. Tell me everything you know about this subject — ideas, examples, arguments, stories. Don't organize it. Just talk. I'll find the patterns.

Listen without interrupting. Then identify:
- Recurring themes (likely chapter anchors)
- Specific stories (likely openings or illustrations)
- Strong opinions (likely central claims)
- Unresolved tensions (likely the interesting parts)

Present back: "I'm hearing three main threads: [X], [Y], [Z]. Do any of these feel like the spine of the book?"

---

## After the Interview

Generate a summary:

```
BOOK PROFILE (draft)

Premise: Most people believe [X]. This book argues [Y].
Reader: [specific person with specific problem]
Promise: After reading, the reader will [specific change]
Differentiation: Unlike [existing books], this book [key difference]
Gut structure: [3-5 part titles or themes]
The chapter to write first: [title]
The chapter they're avoiding: [title]
```

Ask: > Does this feel right? What's wrong or missing?

After confirmation:
1. Save to `book.config.json` under `"book_profile"`
2. Generate a first draft `outline.md` from the gut structure
3. Tell the author: > Book profile saved and outline drafted. When you're ready, run `/ghost-writer:setup-voice` to define how the book sounds.
