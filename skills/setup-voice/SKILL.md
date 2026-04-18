---
description: Third onboarding session. Defines the author's tone of voice through guided interview AND analysis of writing samples they provide. Run after setup-author and setup-book. Populates author_voice in book.config.json. After this session, the plugin is ready to write.
---

# Skill: Setup — How the Book Sounds

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This is the third and final onboarding session. You are defining the author's voice — the specific way they sound on the page. This is done in two parts: a guided interview, then analysis of writing samples.

---

## Prerequisites

Read `book.config.json`. If `author_profile` or `book_profile` are missing, recommend running the previous sessions first. But if the author wants to proceed, continue.

---

## Part 1: The Voice Interview

Start with:
> Now let's figure out how your book sounds. I'll ask a few questions, then I'll ask you to share some writing you've done — anything: emails, posts, previous writing. The combination gives me a precise picture of your voice.

One question at a time.

**1. The reader they're talking to**
> When you write, do you imagine you're talking to one person or a crowd?

Follow up: What's the relationship — peer, student, friend, stranger?

**2. The dinner table test**
> Imagine explaining your book's main idea at a dinner table. Would you use the same words you'd use in the book, or would you translate them?

If yes: the book should sound like conversation. If no: ask why — and whether that gap is intentional or habitual.

**3. The thing they hate to read**
> What kind of writing do you find unreadable? Give me an example of a style or author that makes you cringe.

The opposite of this is part of their voice.

**4. The thing they love to read**
> Who do you wish you wrote like? Not to copy — to understand what you're drawn to.

**5. The rule they break**
> Is there a writing rule you consistently ignore? Something your English teacher would have marked wrong that you do on purpose?

This reveals intentional style choices.

**6. The speed**
> Do you think your natural writing pace is fast (short sentences, punchy) or slow (long sentences, layered)? Or does it vary by moment?

---

## Part 2: Writing Sample Analysis

After the interview, ask:
> Now I'd like to read something you've written — anything. A LinkedIn post, an email, a previous article, a chapter draft. Paste it here. The more authentic (not edited for publication), the better.

If they share a sample, analyze it for:

- **Sentence length**: average, variation, extremes
- **Vocabulary level**: simple/technical/mixed
- **Pronoun use**: I-heavy, we, you-focused?
- **Punctuation style**: dashes, colons, fragments?
- **Rhetorical moves**: questions, lists, analogies, stories?
- **Emotional temperature**: hot, cool, neutral?
- **What they cut**: what's notably absent (humor? vulnerability? data?)

Then produce a **Voice Fingerprint**:

```
VOICE FINGERPRINT

Sentence rhythm: [e.g. "Short punchy sentences with occasional long build-up. Average ~12 words."]
Vocabulary: [e.g. "Everyday words with precise technical terms when necessary. No jargon for its own sake."]
Pronouns: [e.g. "Strong 'you' — writes directly at the reader. Uses 'I' for personal stakes, avoids 'we'."]
Signature moves: [e.g. "Opens sections with a question. Uses em-dashes for asides. Lists of three."]
Emotional temperature: [e.g. "Warm but not effusive. Stakes are high but tone is calm."]
Avoid: [e.g. "No passive voice. No hedging ('it could be argued'). No academic citation style."]
Sounds like: [e.g. "If Malcolm Gladwell wrote with Paul Graham's directness."]
```

Ask: > Does this fingerprint feel like you? What's wrong or missing?

If they have no samples, build the fingerprint from the interview alone and flag it:
> This is based on the interview only — it will be less precise. Share a writing sample when you can and run `/ghost-writer:setup-voice` again to refine it.

---

## After the Session

1. Save the Voice Fingerprint to `book.config.json` under `"author_voice"`
2. Tell the author:

> Voice profile saved. You're ready to write.
>
> Here's your setup summary:
> - **Author**: [one line from author_profile]
> - **Book**: [premise in one sentence]
> - **Voice**: [sounds like line from fingerprint]
>
> Start your first chapter with `/ghost-writer:ask-before-writing`.
