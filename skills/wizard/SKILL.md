---
description: Project setup wizard for authors who don't know where to start. No configuration required. The author describes their idea in any form — a few sentences, a ramble, a vague feeling — and the wizard builds the entire project setup from the conversation. Determines genre, author voice, book premise, and target reader through dialogue. At the end, book.config.json and outline.md are ready and the author can start writing immediately.
---

# Skill: Project Wizard

> **Language**: Read `book.config.json → language` if it exists. Otherwise detect the language the author writes in and use that. Write all output in that language.

This wizard is for authors who have an idea but don't know how to start. No files to configure. No choices to make upfront. Just talk.

The wizard listens, asks a few questions, and builds everything automatically. At the end, the project is ready.

---

## Rules

- Never ask the author to make technical choices.
- Never mention presets, config files, or plugin structure.
- One question at a time. Always.
- If the author is vague, work with what they give — ask one clarifying question, not five.
- The goal is momentum, not perfection. A good-enough setup that gets the author writing is better than a perfect setup that takes an hour.

---

## Phase 0 — The Open Dump

Start with:

> Tell me about the book you want to write. Don't worry about being organized — just tell me what's in your head. It can be a vague feeling, a story you keep thinking about, something you want to say. Anything.

Then wait. Do not interrupt. Do not guide. Let the author say everything they have.

When they stop, read everything carefully before responding. Do not respond immediately — think first.

---

## Phase 1 — Reflect and Clarify

Reflect back what you heard in 3-4 sentences. Use their words, not yours.

Example:
> So you've been thinking about writing the story of how you built your company — the mistakes, the lessons, the things you wish someone had told you when you started. It's part memoir, part manual. You want it to be useful for other entrepreneurs, but also honest in a way that most business books aren't.

Then ask the one most important clarifying question — the thing you most need to know to move forward. Not a list. One question.

Example questions (choose the most relevant):
- "Who is the person you're writing this for — do you have someone specific in mind?"
- "Is this something that happened to you, or something you want to teach?"
- "Is there a story at the center of this, or is it more a collection of ideas?"
- "How long have you been thinking about this — and what's stopped you from starting before?"

---

## Phase 2 — Find the Shape

Based on the dump and the clarifying answer, internally identify the 2-3 most likely shapes for this book. Then present them simply — no jargon, no preset names.

Format:

> Based on what you've told me, I see this book taking one of a few shapes. Tell me which feels closest:
>
> **A — [Plain description]**
> [One sentence of what this version of the book would be and who it's for]
> Example: *"The Hard Thing About Hard Things" by Ben Horowitz*
>
> **B — [Plain description]**
> [One sentence of what this version would be]
> Example: *"Shoe Dog" by Phil Knight*
>
> **C — [Plain description]** *(only if genuinely distinct)*
> [One sentence]

Use real book examples the author might know. Never say "essay preset" or "biography preset" — say "a book that makes an argument" or "a book that tells your story".

Map shapes to presets internally:
- "A book that tells your story" → biography
- "A book that makes an argument or teaches something" → essay or manual
- "A story with characters" → fiction
- "A short story with a lesson" → fable
- "A story for children" → childrens-book

When the author chooses, confirm simply:
> Got it — [plain restatement of what the book is]. Let's build it that way.

---

## Phase 3 — The Three Essential Questions

Now ask three questions — one at a time — to fill in the minimum required information.

**Question 1 — The reader**
> Who is this book for? Don't think too hard — just tell me the first person who comes to mind when you imagine someone reading it.

Extract: target reader for `book.config.json`

**Question 2 — The voice**
> How do you want to sound in this book? Think about someone whose writing you love — or just describe the feeling. Formal or conversational? Serious or with some humor? Talking to a friend or talking to a crowd?

Extract: tone and register for `author_voice`

**Question 3 — The title (optional but useful)**
> Do you have a title in mind — even a working one? It doesn't have to be final.

Extract: title for `book.config.json`. If they don't have one, say "No problem — we can use a working title and change it later" and suggest one based on the premise.

---

## Phase 4 — Build the Project

Now build everything automatically from the conversation. Do not ask for more input.

### Extract the voice fingerprint from the dump

Before writing any configuration, re-read the author's dump from Phase 0 and their answers from Phases 1-3. This text is the most authentic sample of their voice that exists — analyze it directly.

Look for:

**Sentence rhythm**: How long are their sentences on average? Do they use short punchy bursts, or do they build long thoughts? Do they trail off, or land hard?

**Vocabulary**: Everyday words or technical ones? Formal or colloquial? Any recurring expressions, filler phrases, or signature words they use more than once?

**Pronouns**: Do they say "I" a lot? "We"? Do they talk directly to the reader ("you") or describe things from the outside?

**Energy markers**: Where did they speed up? Where did they slow down and add detail? What topic made them write the most?

**What they cut**: What's notably absent — humor, vulnerability, data, self-doubt? What do they seem to avoid?

**Emotional temperature**: Hot, cool, neutral? Do they editorialize or just describe?

**Specific phrases**: Pull 2-3 short phrases directly from their dump that sound unmistakably like them — not their best sentences, their most typical ones.

Build the voice fingerprint from this analysis — not from their answer to "how do you want to sound?" That question produces aspirations. The dump produces truth.

---

Create `book.config.json`:

```json
{
  "title": "[title from conversation or suggested working title]",
  "genre": "[mapped from shape choice]",
  "preset": "[mapped from shape choice]",
  "language": "[detected from conversation]",
  "target_reader": "[from Question 1]",
  "version": "0.1",
  "author_voice": {
    "tone": "[extracted from dump analysis — e.g. 'direct, slightly ironic, no patience for bullshit']",
    "register": "[extracted from dump — e.g. 'conversational, like talking to a colleague over coffee']",
    "pov": "[detected from dump — usually first person singular for memoir/essay]",
    "rhythm": "[extracted from dump — e.g. 'short declarative sentences, occasional long build-up, lands hard']",
    "vocabulary": "[extracted from dump — e.g. 'everyday words, sector-specific terms, no corporate jargon']",
    "signature_phrases": ["[phrase 1 from dump]", "[phrase 2 from dump]"],
    "avoid": "[extracted from dump — what's absent that should stay absent]",
    "voice_source": "wizard_dump"
  },
  "book_profile": {
    "premise": "[one sentence extracted from the dump]",
    "target_reader": "[from Question 1]",
    "promise": "to be defined"
  },
  "wizard_setup": true
}
```

**Note on `voice_source: "wizard_dump"`**: this flag tells `setup-voice` that a voice profile already exists and was built from real text. When the author runs `setup-voice` later, it will offer to refine the existing profile rather than build from scratch — using additional samples if available.

Create a first draft `outline.md` based on the shape chosen and what the author described. Keep it simple — 3-5 chapter placeholders with the author's language, not generic titles.

Example for a business memoir:
```markdown
# Outline — [Title]

## Chapter 1 — [The moment everything started / the origin]
## Chapter 2 — [The first big mistake]
## Chapter 3 — [What actually worked]
## Chapter 4 — [What I'd do differently]
## Chapter 5 — [What I want the reader to do with this]
```

---

## Phase 5 — The Handoff

Present the result simply — no technical details, no file names:

```
YOUR BOOK IS READY TO START

[Title]
[One sentence: what kind of book it is]
[One sentence: who it's for]

I've set up a first structure with [N] chapters to get you started.
You can change everything — titles, order, number of chapters — as you go.
```

Then say:

> You're ready to write. The best way to start is to pick the chapter you most want to write — not necessarily the first one — and begin there.
>
> Type `/ghost-writer:chapter` and tell me which chapter you want to tackle first.

---

## If the Author Is Still Vague After Phase 1

If after the dump and one clarifying question the idea is still too undefined to build anything, do not force a shape. Instead:

> It sounds like the idea isn't fully formed yet — and that's fine. Sometimes the best way to find the book is to start writing without knowing where it goes.
>
> Here's what I suggest: let's do a freeflow session. You talk, I listen, and we see what emerges. Type `/ghost-writer:freeflow` and tell me everything you know about this idea — even the parts that contradict each other.

This is the graceful exit — not a dead end, but a redirect to `freeflow` which can handle total ambiguity.
