---
description: Grammar and style check for a chapter or section. Finds grammatical errors, style inconsistencies, repeated words, rhythm problems, and forbidden phrases from the author's voice profile. Run before integrating feedback or before final draft.
---

# Skill: Proofread

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Reads a chapter and identifies grammar errors, style violations, and prose problems. Reports findings by category, severity first. Does not rewrite — reports and waits for the author to decide what to fix.

---

## Usage

```
/ghost-writer:proofread [file]
/ghost-writer:proofread chapters/03-the-shift.md
```

If no file is given, ask:
> Which chapter should I proofread? (e.g. `chapters/03-the-shift.md`)

---

## Before Starting

Read:
1. `book.config.json` — especially `author_voice` (tone, register, rhythm, vocabulary, avoid, signature_phrases) and `style_rules` if present
2. The target chapter file

Then say:
> Proofreading [filename]. Reading...

---

## What to Check

### 1. Grammar Errors
Flag:
- Subject-verb agreement errors
- Tense inconsistency within paragraphs
- Dangling modifiers or misplaced clauses
- Sentence fragments (unless clearly intentional for style)
- Run-on sentences without clear structural purpose
- Punctuation errors (comma splices, missing closing quotes, misused semicolons)

### 2. Voice Violations
Compare the text against `author_voice` in `book.config.json`:
- **`avoid` list**: flag every instance of a phrase or pattern the author declared to avoid (passive voice, jargon, preachy tone, etc.)
- **`register`**: flag sections that drift significantly from the declared register (e.g. suddenly academic in a conversational text)
- **`pov`**: flag any unintended shift in point of view
- **`tone`**: flag paragraphs that break the declared tone

If `style_rules` exists in `book.config.json`, apply each rule as an additional check.

### 3. Rhythm Problems
Compare against `author_voice.rhythm`:
- If rhythm is "short sentences": flag consecutive long sentences (5+ clauses)
- If rhythm is "long periods": flag choppy runs of very short sentences
- If rhythm is "alternating": flag sections where variation disappears
- Flag paragraphs where all sentences are the same length (monotony)

### 4. Repetition
Scan for:
- The same word used 3+ times within 200 words (excluding articles, prepositions, necessary technical terms)
- The same sentence opening used 3+ times in sequence ("The...", "It...", "This...")
- The same transitional phrase used more than twice in the chapter ("Moreover", "In fact", "However")

### 5. Forbidden Phrases
If `author_voice.avoid` contains specific phrases, flag every occurrence.
If `style_rules` lists prohibited words or constructions, flag those too.

---

## Output Format

Present findings by severity. Output each category as it completes — do not wait for all checks.

```
PROOFREAD — [filename]
─────────────────────────────

GRAMMAR ERRORS (fix before sharing)

1. Line ~[N]: Subject-verb agreement
   "[quoted sentence]"
   → [brief explanation]

2. Line ~[N]: Tense shift
   "[quoted sentence]"
   → Switches from past to present mid-paragraph.

─────────────────────────────
VOICE VIOLATIONS

3. Line ~[N]: Passive voice (declared avoid)
   "[quoted sentence]"
   → Author declared no passive voice. Active alternative: [suggestion]

4. Para [N]: Register drift
   "[first phrase of paragraph]..."
   → Tone becomes academic here; surrounding text is conversational.

─────────────────────────────
RHYTHM

5. Para [N]: Rhythm monotony
   Five consecutive sentences of similar length (~12 words each).
   → Consider varying with one shorter or one significantly longer.

─────────────────────────────
REPETITION

6. Word "experience" — used 4 times in 180 words (paras 3-5)
7. Sentence opener "The" — used 5 times in a row (paras 6-7)

─────────────────────────────
ISSUES FOUND: [N]  |  Grammar: [N]  |  Voice: [N]  |  Rhythm: [N]  |  Repetition: [N]
```

If a category has no issues: `No [category] issues found.` and continue.

---

## After Report

Ask:
> Which of these do you want to fix first? I can suggest a rewrite for any specific issue, or you can fix them directly.

If the author asks for a rewrite suggestion, provide **one option only** — not a menu. Confirm before writing any change to the file. Never modify the chapter without explicit confirmation.

---

## Notes

- Line numbers are approximate (markdown files have no fixed line addresses). Use paragraph markers and quote the first few words of the problem sentence.
- Do not flag stylistic choices that match the declared voice (e.g. fragments as rhythm devices, intentional repetition for emphasis).
- If `author_voice` has no declared constraints, limit the voice check to obvious register breaks and POV shifts.
