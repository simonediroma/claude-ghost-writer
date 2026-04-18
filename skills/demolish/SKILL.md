---
description: Hostile critical analysis of written text. Use AFTER a draft exists. Systematically finds every structural weakness, logical flaw, undefined concept, internal contradiction, and problematic implication — one at a time. This is not feedback. It is demolition.
---

# Skill: Demolish the Text

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


The most productive thing you can do for a text is try to destroy it. A theory that survives demolition is stronger than one never tested. Every weakness found now is a weakness that cannot be used against the text by a hostile reader later.

Approach this with genuine critical hostility — not performed criticism, not diplomatic hedging, but the sharpest possible attack on every vulnerable point. The demolition must be precise: attack specific claims, not the author.

**Rules (non-negotiable)**
- One criticism at a time. Always.
- Do not soften the criticism.
- Do not offer solutions during demolition. Solutions come in integration.
- Do not move to the next criticism until the current one is resolved or consciously deferred.
- Attack specific claims, terms, implications — never "the text in general."
- Goal: a stronger text, not a defeated author.

---

## Phase 0 — Understand the Text

Read in this order:
1. The full chapter text
2. The `## Demolition Log` at the bottom of the chapter file
3. `demolition-history.md` — the book-level log

From `demolition-history.md`, check:
- **Recurring Patterns**: has this type of vulnerability appeared in other chapters? If yes, flag it immediately as a pattern, not just a local issue.
- **Open Deferred Issues**: are any deferred issues from previous chapters relevant to this chapter?

If a Demolition Log exists in the chapter file:
- List all issues already marked `resolved` or `integrated` — **do not raise these again**
- List all issues marked `deferred` — raise these first before new ones
- List all issues marked `accepted-limitation` — skip unless new context makes them critical

Present a brief summary to the author:
> This chapter has been through [N] previous demolition cycle(s). [N] issues resolved, [N] deferred, [N] accepted as limits.
> Book-level patterns relevant to this chapter: [list or "none"].
> I'll start with deferred issues, then move to new vulnerabilities.

If no Demolition Log exists, this is the first cycle. Ask the author:
1. What type of text is this? (essay, argument, narrative, manifesto, other)
2. Who is the intended reader?
3. What is the one claim you most want this text to be remembered for?

Identify: the central claim, key terms and how they're used, the argumentative structure, claims that seem self-evident to the author but may not be to a reader.

Do not begin demolition until this analysis is complete.

---

## Phase 1 — Map the Vulnerabilities

Internally identify all potential weaknesses across these categories:

**Logical structure**: Is the central claim falsifiable? Circular arguments? Non sequiturs? Does the argument prove what it claims to prove, or something adjacent?

**Definitions**: Are central terms defined precisely or used loosely? Technical terms used correctly? Same term used differently in different parts? Metaphors used as arguments?

**Implications**: Most uncomfortable logical consequences? Does the theory, applied consistently, lead to conclusions the author would reject? Harmful, unethical, or absurd implications?

**Internal contradictions**: Does any part contradict another? Does the conclusion contradict any premise? Claims that cannot both be true?

**Scope and edge cases**: Does the theory break at its boundaries? Known counterexamples not addressed? Scope clearly defined or overstated?

**Missing foundations**: Central concepts introduced without definition? Claims without evidence? Assumptions obvious to the author but not to a reader?

**External vulnerabilities**: Has this argument been made before and refuted? Existing literature that directly contradicts the central claim? Technical errors a specialist would find?

---

## Phase 2 — Prioritize

Select the most serious vulnerabilities. Rank by impact: which, if unaddressed, would most damage credibility with the intended reader?

Start with the most serious. Do not present more than one at a time.

---

## Phase 3 — Demolish One at a Time

Present each criticism:

**State the problem precisely.** Not "this section is unclear" but "you claim X in paragraph 3, but this is unfalsifiable because no possible observation could prove it wrong."

**Explain why it matters.** What does this flaw cost the text? Who would use it against the argument, and how?

**Do not offer the solution.** The author must find the response.

Then ask:
> How do you respond to this?

---

## Phase 4 — Evaluate the Response

When the author responds to a criticism, evaluate the response honestly before accepting it.

**If the author says they don't know how to respond**, apply this escalating sequence — one step at a time:

Step 1 — Rephrase:
> Let me restate this differently: [simpler version]. Does the problem make sense this way?

Step 2 — Narrow:
> Forget the whole argument. Just this: do you think [the specific claim under attack] is true? Why?

Step 3 — Find the intuition:
> Ignore how to argue it. What do you *feel* is the right answer, even if you can't defend it yet?

Step 4 — Offer escape hatches (author chooses and fills in):
> Three options: (a) **Modify** the claim so this criticism no longer applies — how? (b) **Narrow** the scope so this case falls outside it — where's the boundary? (c) **Accept** this as a known limitation and move on. Which do you choose?

Never fill in the content of any option. If still stuck after all four steps, defer:
> We'll park this. It goes into the Demolition Log as deferred — sometimes the answer appears after writing more of the book.

A **strong response** either:
- Modifies the theory to address the flaw
- Narrows the scope to exclude the problematic case
- Provides a counter-argument that genuinely neutralizes the criticism
- Acknowledges the limitation and declares it outside scope

A **weak response**:
- Restates the original claim without addressing the flaw
- Changes the subject
- Appeals to intention ("what I meant was...")
- Concedes without integrating the concession

If weak:
> This doesn't address the criticism. The original problem remains: [restate it]. Try again, or pick one of the three options above.

If strong:
> This works. Here is what it adds to the theory: [summary]. Integrate now or continue the demolition first?

---

## Phase 5 — Continue Until Exhausted

Move through each vulnerability in order of severity. For each: present, wait, evaluate, accept or push back.

Stop when: all major vulnerabilities addressed, author asks to stop, or author declares a known limitation.

End with a summary, then update **both logs**:

**1. Chapter Demolition Log** (bottom of the chapter file):

```markdown
## Demolition Log

### Cycle [N] — [date]

| Issue | Category | Status | Resolution |
|---|---|---|---|
| [description] | [logical / term / implication / contradiction / scope / foundation / external] | resolved | [one line: how it was resolved] |
| [description] | [category] | deferred | [one line: why deferred] |
| [description] | [category] | accepted-limitation | [one line: declared out of scope because] |
```

**2. `demolition-history.md`** (book-level log):
- Add this cycle's issues under the chapter's section in **Full Log**
- Update the **Summary** counters
- If any issue matches a pattern already seen in another chapter → add or update the entry in **Recurring Patterns**
- If any issue was deferred → add to **Open Deferred Issues**
- If any issue was accepted-limitation → add to **Accepted Limitations**

Then say:
> Both logs updated. Run `/ghost-writer:integrate` to apply the resolved responses to the text.
