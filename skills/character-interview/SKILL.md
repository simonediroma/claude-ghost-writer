---
description: Optional. Deep interview to define a character's psychology, behavior, contradictions, and voice. Use for any character — real or fictional — whose consistency matters across chapters. Run once per character before writing scenes that feature them. Creates a character file in characters/ that all other skills will reference.
---

# Skill: Character Interview

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


This skill builds a precise psychological profile of a character through structured dialogue with the author. The goal is not a biography — it is a **behavioral map**: given any situation, how does this character think, react, and speak?

Works for both fictional characters and real people being portrayed in narrative non-fiction or biography.

One question at a time. Always. Do not cluster questions.

---

## Before Starting

Check if a `characters/` directory exists. If not, create it.
Check if a file `characters/[character-name].md` already exists. If yes, ask:
> A profile for [character] already exists. Do you want to update it or start from scratch?

Ask the author:
> Who are we building a profile for? Give me their name and their role in the book (protagonist, antagonist, secondary character, real person, etc.).

Then ask whether this is a **fictional character** or a **real person**. The interview has a different emphasis for each — but the core questions apply to both.

---

## Part 1: The Surface

**1. First impression**
> How does [character] enter a room? What do people notice first?

Push for specificity. Not "tall and confident" but what specifically — the way they move, what they do with their hands, whether they speak first or wait.

**2. The contradiction**
> What is the most surprising thing about [character] — the thing that contradicts the first impression?

Every compelling character has a gap between surface and interior. If there's no contradiction, the character isn't real yet.

**3. The voice**
> Give me three sentences this character would say — in their own words, in a casual moment. Not plot-relevant dialogue. Just them talking.

If the author struggles: What would this character say when they're annoyed? When they're trying to impress someone? When they're alone?

---

## Part 2: The Psychology

**4. The wound**
> What is the formative experience that shaped who [character] is today? The thing they carry without knowing it?

For real people: What is the event or period that most changed them?
If the author doesn't know yet: What do you suspect? What would make their behavior make sense?

**5. The belief**
> What does [character] believe about how the world works — the rule they live by, even if they've never said it out loud?

This is the worldview that drives their decisions. Push past the obvious: not "family comes first" but the deeper, often unconscious logic.

**6. The fear**
> What does [character] most want to avoid? Not in plot terms — psychologically. What would make them feel most exposed?

**7. The blind spot**
> What is [character] completely wrong about — something they're convinced of that the reader will see through?

This is what makes a character human. If they're right about everything, they're not a character, they're a mouthpiece.

---

## Part 3: Behavior Under Pressure

**8. Under stress**
> When [character] is under pressure, what do they do? Do they go quiet or loud? Control or release? Attack or withdraw?

Push for the specific behavior, not the label. Not "they get angry" but what that anger looks like.

**9. In conflict**
> How does [character] handle direct confrontation with someone they can't ignore? Give me the specific move they make.

**10. The tell**
> What does [character] do when they're lying, or hiding something, or pretending to feel something they don't?

Every character has a tell. If the author doesn't know, ask: What do YOU do in that situation? Often the character inherits something from the author.

**11. The want vs. the need**
> What does [character] think they want in this book? And what do they actually need — which may be different or even opposite?

This gap is often the engine of the story.

---

## Part 4: Real vs. Fictional (conditional)

### If fictional:
**12. The limit**
> What is one thing [character] would never do — a line they would not cross? And what would it take to make them cross it?

**13. The change**
> Does [character] change by the end of the book? If yes: what triggers the change, and what is the last version of them we see?

### If real:
**12. The public vs. private gap**
> How does [character] behave in public versus in private? What does the public version conceal?

**13. The authorial stance**
> How do you, as the author, feel about this person? Admiration, ambivalence, criticism — and how will that come through in the portrayal?

---

## After the Interview

Generate the character profile:

```markdown
---
name: [Character Name]
role: [protagonist / antagonist / secondary / real person]
type: [fictional / real]
version: 1.0
---

# [Character Name]

## Surface
[First impression + the contradiction]

## Voice
> "[Sample sentence 1]"
> "[Sample sentence 2]"
> "[Sample sentence 3]"

## Psychology
**The wound**: [formative experience]
**The belief**: [worldview they live by]
**The fear**: [what they most want to avoid]
**The blind spot**: [what they're wrong about]

## Under Pressure
**Under stress**: [specific behavior]
**In conflict**: [specific move]
**The tell**: [what they do when hiding something]
**Want vs. need**: [what they think they want / what they actually need]

## Arc (fictional) / Stance (real)
[Change arc OR authorial stance + public/private gap]

## Notes
[Anything the author flagged as uncertain or to revisit]
```

Ask: > Does this feel like [character]? What's missing or wrong?

After confirmation:
1. Save to `characters/[character-name].md`
2. Add an entry to `book-memory.md` under a new `## Characters` section if not present:

```
| [Name] | [role] | characters/[name].md |
```

Then tell the author:
> Profile saved. When you write scenes featuring [character], run `/ghost-writer:character-check [character-name]` to verify consistency before finalizing.
