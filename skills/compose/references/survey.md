# The RAMA survey method

Whenever a RAMA skill needs something from the author, ask it as a **survey**:
each question gets **three concrete answers plus a write-in**. The author
should be able to answer most questions with one click, and the write-in
always lets them say something you didn't think of.

## How to ask

Use the structured question tool the platform gives you:

- **Claude Code / Cowork:** `AskUserQuestion`. Give exactly three options per
  question. The tool adds "Other" (the write-in) by itself, so don't add one.
  Use up to four questions per call.
- **claude.ai:** the `ask_user_input` tool, with three options per question.
  Say in the question text that the author can type their own answer instead.
- **No question tool:** write it in plain text, in the same shape, and wait:

  ```
  **Q1. How does Keziah learn the key has come back?**
  A. Harold tells her outright, against his own rule
  B. She sees it on his table and says nothing
  C. Sharp's letter reaches her first
  D. Write in: ___
  ```

  The author can answer `1B, 2A, 3: <their own words>`.

## What makes a good survey question

- **Ask only what the files don't answer.** Before asking, check the outline,
  synopsis, story bible, style guide, the RAMA Log's Decisions, and the
  written chapters. Asking something the author has already settled wastes
  their time and tells them you didn't read.
- **Three real, distinct options.** Each one should be something the author
  could plausibly choose, and each should lead the book somewhere different.
  Never pad with a strawman or a "none of the above."
- **Ground every option in the book.** Use the characters, places, objects
  and register from the project files, not generic craft advice.
- **Recommend when you have a reason.** Put your recommendation first and
  mark it `(Recommended)`, with the reason in its description. Don't
  recommend when the question is a matter of the author's taste or intent.
- **Concise.** A question is one sentence. An option label is a few words; the
  description says what follows from picking it.
- **Batch, then stop.** Ask up to four related questions at a time, then wait.
  Don't run more than three rounds before showing the author some output.
  If more questions remain, write your best assumption into the output and
  mark it `[ASSUMED]` so they can overrule it.
- **Never answer for the author.** If the author writes "you decide," choose,
  say what you chose in one line, and log it as a Decision marked
  `(RAMA's call)`.

## After the answers

Record every answer that changes the book under **Decisions** in the RAMA Log,
dated and tagged with the chapter: `2026-11-16 · ch 5 · <decision>`. Answers
that only shape the output at hand (a preference for this draft) don't need
logging.
