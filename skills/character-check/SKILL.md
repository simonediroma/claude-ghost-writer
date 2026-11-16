---
name: character-check
description: Optional. Checks that a character in a RAMA chapter behaves, speaks and knows things consistently with their profile in characters/, the story bible and their earlier scenes. Flags voice drift, behavior that contradicts them, and knowledge slips, then fixes drift with the author's approval. Complements /rama:check. Usage /rama:character-check 5 [Name].
---

# RAMA: Character Check

*Adapted from ghost-writer's `character-check` (MIT, Simone Di Roma).*

Read `references/project-files.md` and `references/survey.md` first. Ask "intentional or drift?" as a survey: **Drift: fix it / Intentional: log as an arc moment / Not sure: show me the earlier scenes**. Any rewrite must pass the style guide and is applied only with the author's OK. Cite locations as `ch.para`.

Read the written chapter or scene and the character's profile. Find every place where the character on the page contradicts the character as defined.

This is not about whether the character is well-written in the abstract — it is about whether they are **consistent with their own established psychology**.

---

## Before Starting

1. Ask which character(s) to check and which chapter or scene to audit
2. Read `characters/[character-name].md` — the full profile
3. Read the specified chapter from the manuscript, plus the story bible entry for the character
4. The RAMA Log: Decisions and Continuity Ledger entries about the character
5. Earlier chapters: search the manuscript for the character and read their most recent scenes before this chapter

If no profile exists for the character:
> There's no profile for [character] yet. Run `/rama:character-interview [character-name]` first, or proceed without a profile (I'll flag what seems inconsistent based on the chapter alone).

---

## What to Check

### 1. Voice drift
Compare the character's dialogue and internal monologue against the **Voice** section of the profile (the three sample sentences).

Flag any line where:
- The vocabulary level shifts significantly (suddenly more educated, more crude, more formal)
- The rhythm is wrong (the character who speaks in short bursts suddenly has long elaborate sentences)
- The emotional temperature is off (warm character goes cold without cause)

### 2. Behavioral contradiction
Compare every action the character takes against **Under Pressure** and **In Conflict** from the profile.

Flag any moment where:
- The character does something the profile says they would not do — without a reason established in the text
- The character's stress response is the opposite of what's defined (withdraws when they should attack, speaks when they should go silent)
- The tell is absent in a scene where the character is clearly hiding something

### 3. Belief violation
Compare the character's decisions against **The Belief** in the profile — the worldview they live by.

Flag any decision that contradicts their core belief without the text acknowledging the contradiction. Contradictions can be intentional (character growth) or accidental (inconsistency). The check distinguishes between the two.

### 4. Blind spot awareness
Check whether the character shows awareness of their own **Blind spot** in moments where, by profile, they shouldn't.

A character who is wrong about something should not suddenly be right about it without a credible turning point.

### 5. Want vs. need coherence
Check whether the character's behavior in this chapter is consistent with their **Want vs. need** gap.

If the character is pursuing what they want, they should not simultaneously demonstrate awareness of what they need — unless the chapter is specifically the turning point.

### 6. Arc consistency (fictional) / Stance consistency (real)

**Fictional**: If the character has a defined change arc, check where this chapter sits in that arc. Is the character behaving at the right stage of their development?

**Real**: Check whether the portrayal is consistent with the authorial stance defined in the profile. If the author said they feel ambivalent about this person, is that ambivalence present in the prose — or has it collapsed into either admiration or criticism?

---

## Output Format

```
CHARACTER CHECK — [Character Name] in [Chapter Title]
Issues found: [N]

─────────────────────────────
SIGNIFICANT (changes how the reader perceives the character)

1. VOICE DRIFT — [ch.para]
   Line: "[the problematic line]"
   Profile says: [what the voice should sound like]
   Problem: [specific mismatch]

2. BEHAVIORAL CONTRADICTION — [scene description]
   Character does: [action]
   Profile says under pressure they: [expected behavior]
   Possible fix: [option A] or [option B]

─────────────────────────────
MINOR (noticeable on re-read, not on first pass)

3. BLIND SPOT SLIP — [scene description]
   Character seems aware of: [the thing they shouldn't know yet]
   This may be intentional — confirm with author.
```

For each issue, ask:
> Is this intentional — a moment of character development — or a drift you want to fix?

If intentional: note it in `characters/[name].md` under a new **Arc Moments** section.
If a drift: offer a targeted rewrite of the specific passage.

---

## After the Check

When all issues are resolved:
1. Update `characters/[name].md` — add any new behavioral data revealed in this chapter under **Notes**
2. If the character showed growth or change, log it under **Arc Moments**
3. Tell the author:

> [Character]'s behavior in [chapter] is now consistent with their profile. Profile updated with new data from this chapter.
