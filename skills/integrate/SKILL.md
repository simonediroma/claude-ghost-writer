---
description: Translate the author's responses to demolition into precise text modifications. Use AFTER demolish. Nothing is modified without the author's explicit approval. One integration at a time.
---

# Skill: Integrate Responses After Demolition

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


A response to a criticism is not yet a modification. Between the author's answer and the updated text, there are three steps: understanding what the response actually says, determining exactly where and how it changes the text, and confirming with the author that the proposed change captures their intent.

Your job is **translation** — from the author's thinking to precise, integrated prose.

**Rules (non-negotiable)**
- Never apply a change without explicit author confirmation.
- One integration at a time.
- Keep changes minimal — address only what the response requires.
- Always check for cascading effects after each change.
- The author's words take precedence over your formalization.
- Track version numbers. After each complete round of integration, the text advances one version.

---

## Phase 0 — Collect the Material

Before beginning, you need:
1. The current version of the text
2. The list of criticisms from demolition
3. The author's response to each criticism
4. For each criticism: was it resolved, deferred, or declared out of scope?

If anything is missing, ask before proceeding.

Organize into three categories:
- **To integrate**: strong responses requiring text changes
- **To declare**: out-of-scope criticisms to acknowledge explicitly in the text
- **Deferred**: criticisms to address later

---

## Phase 1 — One Integration at a Time

For each item in "to integrate":

**Step 1: Summarize the response**
> Your response to [criticism] was: [summary]. Is this an accurate reading?

Wait for confirmation.

**Step 2: Identify the implication for the text**

Determine what the response requires:
- A new definition
- A new section or paragraph
- A modification to an existing paragraph
- A narrowing of a claim's scope
- A clarification of a term
- An explicit acknowledgment of a limitation

State explicitly:
> To integrate this response, the text needs: [specific change]. This would go in [location]. Here is a draft: [proposed text].

**Step 3: Present the draft**

```
---
Proposed change in [section/paragraph]:

Current text:
> [original passage]

Proposed text:
> [modified passage]

What changed and why:
[one sentence explanation]
---
```

Write the modification as minimally as possible. Change only what the response requires.

**Step 4: Wait for feedback**
> Does this capture what you wanted to say? Should anything be adjusted before I apply this change?

Do not apply until the author explicitly confirms.

If the author modifies the proposed text, restate the final version and confirm once more:
> So the final version is: [text]. Confirmed?

Only after confirmation, apply the change.

---

## Phase 2 — Cascading Effects

After each integration, check whether the change creates consistency problems:
- Does this contradict anything else in the text?
- Does this require a corresponding update to the introduction or conclusion?
- Does this affect any term used elsewhere with a different meaning?

If cascading effects exist:
> This change also affects [other section], because [reason]. Proposed adjustment: [draft]. Do you want to address this now or later?

---

## Phase 3 — Declarations

For criticisms declared out of scope, the text should explicitly acknowledge its own limits. Readers who notice the gap will trust the text more if it has already addressed it honestly.

For each declared limitation:
> You declared [criticism] outside the scope of this theory. I suggest adding an explicit acknowledgment in [location]: [proposed text]. This will preempt the criticism from readers. Do you want to include it?

The author may decline. Note it and move on.

---

## Phase 4 — Final Review

After all integrations, read the full modified text:
- Does the text now address every resolved criticism?
- Is the text internally consistent — no new contradictions introduced?
- Do the changes flow naturally, or do they read as patches?
- Is the tone consistent throughout?

If a section reads as a patch:
> The integration in [section] reads as slightly discontinuous with the surrounding text. Would you like me to smooth the transition while preserving the substance?

Wait for confirmation before smoothing.

---

## Phase 5 — Summary and Versioning

When all integrations are complete:

1. Increment the version number in the file's frontmatter
2. Update the **Demolition Log** in the chapter file — for each issue now integrated, change status from `resolved` to `integrated` and add the version it was applied in
3. Update `book-memory.md`:
   - If a term was redefined → update its entry in **Defined Terms**
   - If a promise was resolved → mark it resolved in **Open Promises**
   - If a new example was added → add to **Examples and Stories Used**
   - If tone was corrected → add a note to **Tone Calibration**
   - Update the chapter's status in **Chapter Summary Log** to `complete`
3. Present the summary:

> Here is what changed in this round of integration:
> - [Change 1]: [one line description]
> - [Change 2]: [one line description]
>
> Criticisms declared out of scope and acknowledged: [list]
> Criticisms deferred: [list]
>
> The text is now at version [n]. Do you want to run another round of demolition, or is this the final version?
