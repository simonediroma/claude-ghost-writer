---
description: Editorial revision pass. Checks grammar and spelling, punctuation and writing rules from style-rules.md, event timeline, per-character details (age, appearance, names, relationships), and continuity of details introduced in one chapter and reused in another (objects, places, dates, numbers, wording). Run on a single chapter after integrate, or on the whole book before manuscript-final. Proposes every fix — never applies without confirmation.
---

# Skill: Revise

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Usage:
- `/ghost-writer:revise [file]` — revise one chapter (and check it against everything written before it)
- `/ghost-writer:revise --all` — revise the whole book
- `/ghost-writer:revise [file|--all] --only grammar,rules,timeline,characters,continuity` — run only some checks

This is not demolition (arguments) and not character-check (psychology). It is the **copy-editor and continuity-editor pass**: the errors that make a reader stop and think "wait, that's wrong."

---

## Before Starting

Read `book.config.json` (`language`, `longform_mode`) and `style-rules.md`. Then immediately say:

> Starting revision — [chapter / whole book], checks: [list]. Reading...

Then read:

1. `book-memory.md` — sections `## Timeline`, `## Continuity Ledger`, `## Characters`, `## Defined Terms`
2. If `longform_mode: true` → also `memory/part-*.md` (same sections)
3. `characters/*.md` — only the **Facts** section (if present) and header data (name, age, role)
4. The chapter(s) to revise — **full text** (copy-editing cannot work from summaries)
5. For continuity checks on a single chapter: the summaries of earlier chapters; drill into full text of an earlier chapter only when a detail needs to be verified against its first mention

If `style-rules.md` is missing or its **Punctuation Conventions** still hold placeholders (`[e.g. …]`), ask **one** question:
> There are no punctuation conventions yet. Do you want me to (A) infer them from the chapters already written, or (B) use the standard conventions for [language]?

If A: run the `infer` logic of `/ghost-writer:rules`. If B: fill the table with the language defaults (see table below). Save after confirmation.

---

## The Five Checks

### 1. Grammar and spelling
Flag:
- Spelling errors and typos (double letters, missing letters, swapped words, repeated words "the the")
- Agreement errors (subject–verb, gender/number, noun–adjective)
- Tense errors and unmotivated tense shifts within a scene
- Wrong mood (e.g. Italian congiuntivo/condizionale, French subjonctif)
- Wrong prepositions, articles, pronouns with ambiguous reference
- Accents and apostrophes (e.g. Italian: `perché` not `perchè`, `po'` not `pò`, `qual è` not `qual'è`)

Do **not** flag deliberate choices: dialect, a character's voice, stylistic fragments, entries in `author_voice.signature_phrases`. If unsure, mark as `[possibly intentional]`.

### 2. Punctuation and writing rules
Check the text against `style-rules.md`:
- **Writing Rules** (`R1`, `R2`…): every violation, citing the rule ID. Use the ✅/❌ examples to interpret the rule; respect its scope (a rule on thoughts does not apply to dialogue).
- **Punctuation Conventions**: every deviation and every **inconsistency within the book** (even if both forms are correct, mixing them is an error):
- Dialogue marks (`«»` vs `""` vs `—`) and where punctuation goes relative to them
- Dashes (em dash `—` vs en dash `–` vs hyphen `-`; spaced or not)
- Ellipsis (`…` single character vs `...`; space before/after)
- Quotes inside quotes
- Serial (Oxford) comma
- Numbers (digits vs words), dates and time formats
- Capitalization after colon, of titles, of honorifics
- Spacing (double spaces, space before `?`/`!` per language)

### 3. Timeline
Build (or update) the event timeline from the text: every dated or datable event, every relative time marker ("three days later", "the following winter", "when she was twelve"), seasons, weekdays, ages, durations.

Flag:
- Impossible sequences (an event referenced as past before it happens)
- Duration conflicts ("two weeks later" vs a date that implies two months)
- Season / weather / daylight conflicts (snow in "August", sunset at 5 pm in June)
- Weekday conflicts (a date stated as Monday that falls on another day, if the year is known)
- Age arithmetic (character is 30 in 2010 and 38 in 2015)
- Simultaneity conflicts (a character in two places at the same time)
- Historical anachronisms (objects, technology, expressions not yet existing at the story's date) — biography/fiction only

### 4. Character details
For every character who appears, collect the **factual** details stated in the text: full name and spelling, nicknames, age / birth date, physical traits (eyes, hair, height, scars, glasses), family and relationships, job, home, habits, possessions, how they address others (tu/lei, first name/surname).

Compare against `characters/[name].md → Facts` and against every previous mention. Flag any mismatch: eyes blue in Ch. 2 and green in Ch. 7; sister becomes cousin; name spelled `Katia` and `Katya`; switches from formal to informal address without a narrative reason.

(Psychology and behavior are out of scope — that's `/ghost-writer:character-check`.)

### 5. Cross-chapter continuity
For every **specific detail introduced in one chapter and mentioned again later**, verify it is identical. Typical items:
- Objects (the red car → later a blue car; a 3-room apartment → later 4 rooms)
- Places (street names, cities, the layout of a room, distances)
- Numbers (amounts, quantities, counts, prices, percentages, statistics)
- Quoted text that is quoted again later (a letter, a motto, a line of dialogue recalled)
- Names of minor entities (shops, pets, companies, ships, books)
- Facts and figures in non-fiction (a figure cited as 40% in Ch. 1 and 45% in Ch. 6; a source attributed to two different authors)
- Rules established in the world (magic system, company policy, a procedure in a manual)

Flag every mismatch, and note which version is the **first mention** (the default canonical one unless the author decides otherwise).

---

## Output Format

Surface findings **check by check as you complete each one** — do not wait for all five. For a single chapter with many grammar/punctuation hits, group them in one table instead of one block each.

```
REVISION — [Chapter title | Whole book]
Checks run: [list]
Issues found: [N]   (grammar [n] · punctuation [n] · timeline [n] · characters [n] · continuity [n])

─────────────────────────────
1. GRAMMAR AND SPELLING
| # | Ch. | Paragraph | Text | Fix | Note |
|---|---|---|---|---|---|
| G1 | 3 | §4 | "...perchè non..." | "...perché non..." | accent |

2. PUNCTUATION AND RULES
| # | Ch. | Paragraph | Text | Fix | Rule |
|---|---|---|---|---|---|
| P1 | 3 | §7 | "Vieni..." | "Vieni…" | ellipsis: single character |
| P2 | 3 | §9 | "Lo sapeva: perché…" | "Lo sapeva, perché…" | R1 |

─────────────────────────────
3. TIMELINE
T1 — [CRITICAL]
   Ch. 2: "[quote]" → [event] in spring 1998
   Ch. 5: "[quote]" → implies autumn 1998
   Conflict: [explanation]
   Fix options: (A) [...] (B) [...]

4. CHARACTER DETAILS
C1 — [Character] — eye colour
   Ch. 2 §3: "[quote]" → blue   (first mention)
   Ch. 7 §12: "[quote]" → green
   Fix: align Ch. 7 to "blue"?

5. CONTINUITY
K1 — [detail]
   Introduced Ch. 1 §5: "[quote]"
   Reused Ch. 4 §9: "[quote]"
   Mismatch: [what differs]
   Fix: align to first mention?
```

Severity for timeline / characters / continuity:
- **CRITICAL** — a careful reader will notice and lose trust (plot-relevant, impossible sequence)
- **SIGNIFICANT** — noticeable on re-read
- **MINOR** — only a copy-editor would catch it

If a check finds nothing: `No [check] issues found.` and move on.

---

## Applying Fixes

Ask:
> How do you want to proceed? (A) Apply all grammar and punctuation fixes in one go — I'll show the diff count per chapter. (B) Review them one by one. Timeline, character and continuity issues are always reviewed one at a time.

- Grammar/punctuation in bulk only with explicit (A). Skip anything marked `[possibly intentional]` unless the author confirms it.
- Timeline / character / continuity: **one issue at a time**. Ask which version is canonical, then show the exact replacement in every affected chapter before applying.
- Never change meaning, voice or rhythm while fixing a mechanical error.

---

## After Revision

1. Update `book-memory.md` (or `memory/part-[n].md` in longform mode):
   - `## Timeline` — add or correct every event found (canonical version only)
   - `## Continuity Ledger` — add every detail checked, with its canonical value and first-mention chapter
2. Update `characters/[name].md → Facts` with canonical physical and biographical data (create the section if missing)
3. If the conventions were inferred, save them to `style-rules.md`. If the author fixed the same kind of thing 3+ times and no rule covers it, propose a new rule (`/ghost-writer:rules add`)
4. In each revised chapter's frontmatter, set `revised: [date]`
5. Tell the author:

> Revision complete — [N] fixes applied, [M] left as intentional. Timeline and continuity ledger updated: future revisions will check new chapters against them automatically.

---

## Style Guide Defaults by Language

Used only when the author chooses (B) and `style-rules.md` has no conventions yet.

| Rule | it | en | es | fr | de | pt |
|---|---|---|---|---|---|---|
| dialogue | `«»` | `""` | `—` | `«»` with spaces | `„"` | `—` |
| nested quotes | `""` | `''` | `""` | `""` | `‚'` | `""` |
| dash | `—` spaced | `—` unspaced | `—` | `—` spaced | `–` spaced | `—` |
| ellipsis | `…` | `…` | `…` | `…` | `…` | `…` |
| serial comma | no | yes | no | no | no | no |
| space before `?!:;` | no | no | no | yes (thin) | no | no |
| numbers | words up to ten | words up to ten | words up to ten | words up to ten | words up to twelve | words up to ten |
