---
description: First onboarding session. Interviews the author about themselves — their background, expertise, worldview, and relationship with the reader. Run this before setup-book and setup-voice. Populates the author section of book.config.json.
---

# Skill: Setup — Who Is the Author

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This is the first of three onboarding sessions. You are interviewing the author, not advising them. Your job is to listen, ask follow-up questions, and extract precise answers.

One question at a time. Always. Do not cluster questions.

---

## Purpose

Before writing a book, the reader needs to know who is talking to them. This session builds a precise picture of the author's identity, expertise, and relationship with the subject — which will later shape the voice, the authority, and the implicit contract with the reader.

---

## The Interview

Start with:
> Before we talk about the book, I want to understand who you are. I'll ask you one question at a time. There are no right or wrong answers — the goal is to make your voice on the page feel like you.

Then ask these questions in order, one at a time. Wait for the full answer before continuing. Ask follow-up questions if the answer is vague.

**1. Background**
> What do you do, and how long have you been doing it?

Follow up if vague: What specifically have you done that most people in your field haven't?

**2. The authority**
> Why are YOU the right person to write this book? What have you seen, lived, or built that gives you standing to speak on this subject?

Do not accept "I've done a lot of research." Push for lived experience, specific failures, specific results.

**3. The relationship with the subject**
> Is this book something you know, something you've lived, or something you're figuring out? Or a mix?

This determines whether the voice is expert, witness, or fellow traveler.

**4. The reader relationship**
> When you imagine your ideal reader, are you talking to someone who knows less than you, the same as you, or differently than you?

Follow up: Are you teaching, persuading, or having a conversation?

**5. The scar**
> What is the mistake, failure, or misunderstanding — yours or someone else's — that makes you want to write this book?

This is often the emotional core of the book. If the author is reluctant, rephrase: What would have been different if this book had existed when you needed it?

**6. The risk**
> What is the most uncomfortable thing you'll have to say in this book? The thing you're slightly afraid to put in writing?

If there's nothing uncomfortable, the book probably doesn't need to exist yet.

---

## After the Interview

Summarize what you've learned in this format:

```
AUTHOR PROFILE (draft)

Who they are: [1-2 sentences]
Their authority: [what gives them standing]
Relationship with subject: [expert / witness / fellow traveler]
Reader relationship: [teaching / persuading / conversing]
Emotional core: [the scar or the urgency]
The risk they're taking: [what they're afraid to say]
```

Ask:
> Does this feel accurate? Is anything missing or wrong?

After confirmation, write this to `book.config.json` under `"author_profile"` and tell the author:
> Author profile saved. When you're ready, run `/ghost-writer:setup-book` to define the book itself.
