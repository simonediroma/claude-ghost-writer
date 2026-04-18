# Ghost Writer — Claude Code Plugin

Collaborative ghost writing assistant for books and long-form writing projects.

Based on the writing method developed in [quantum_fatalism](https://github.com/simonediroma/quantum_fatalism) — a philosophical essay written in explicit collaboration between a human author and Claude.

---

## Installation

```bash
/plugin install ghost-writer@claude-plugins-official
```

Or directly from GitHub:

```bash
/plugin install https://github.com/your-username/ghost-writer
```

Test locally before publishing:

```bash
claude --plugin-dir ./ghost-writer
```

---

## The one command to remember

```bash
/ghost-writer:resume
```

Run this whenever you open the project. It tells you what you last did, what's waiting, and exactly what to do next.

---

## Quick Start — Macro Commands

Four commands cover the entire book lifecycle. Use these if you don't want to manage the sequence manually.

| Command | What it runs |
|---|---|
| `/ghost-writer:check` | **Run this first** — verifies installation and setup in 60 seconds |
| `/ghost-writer:wizard` | **Start here if you don't know where to begin** — conversational setup from scratch |
| `/ghost-writer:start` | Full onboarding — author interview + book definition + voice fingerprint |
| `/ghost-writer:chapter` | Full chapter cycle — dialogue + write + demolish + integrate |
| `/ghost-writer:review [file]` | Full persona review — all 5 readers + integrate |
| `/ghost-writer:finish` | Book closing — introduction + conclusion + final audit + manuscript |

**Not sure which to use?** → `/ghost-writer:wizard`

The atomic commands (below) remain available for authors who want to control the sequence directly.

---

## Skills

### Onboarding — run once, in order

| Command | What it does |
|---|---|
| `/ghost-writer:session-start` | Opens any session — reads full project state, suggests what to do today |
| `/ghost-writer:setup-author` | Interview: who you are, your authority, your emotional stake |
| `/ghost-writer:setup-book` | Brainstorm: premise, reader, structure — selects the genre preset |
| `/ghost-writer:setup-voice` | Defines tone of voice via interview + writing sample analysis |

### Writing cycle — repeated per chapter

| Command | What it does |
|---|---|
| `/ghost-writer:ask-before-writing` | Structured dialogue before writing anything |
| `/ghost-writer:freeflow` | For blocked authors — dump everything, plugin organizes |
| `/ghost-writer:write [section]` | Generates the section after dialogue is confirmed |
| `/ghost-writer:demolish [file]` | Hostile critical analysis — one objection at a time |
| `/ghost-writer:demolish-persona [persona]` | Demolition from a specific reader's perspective |
| `/ghost-writer:integrate` | Incorporates responses into the text — one change at a time |

### Consistency — periodic

| Command | When |
|---|---|
| `/ghost-writer:consistency-check` | Every 3-4 completed chapters |
| `/ghost-writer:character-interview [name]` | Optional — before writing scenes with key characters |
| `/ghost-writer:character-check [name] [file]` | Optional — after writing scenes with profiled characters |

### Closing — run once, at the end

| Command | What it does |
|---|---|
| `/ghost-writer:write-opening` | Writes the introduction — last, after all chapters are complete |
| `/ghost-writer:write-closing` | Writes the conclusion — closes the arc |
| `/ghost-writer:manuscript-final` | Arc audit + assembles submission-ready manuscript |

### Utility

| Command | What it does |
|---|---|
| `/ghost-writer:status` | Project overview and suggested next step |

---

## Complete Workflow

```
ONBOARDING (once)
─────────────────────────────────────
session-start         → orient to the project
setup-author          → who are you, your authority, your stake
setup-book            → what is the book + genre preset + first outline draft
setup-voice           → tone of voice via interview + sample analysis

PER CHAPTER (repeated)
─────────────────────────────────────
session-start                   → briefing: where we left off
ask-before-writing              → concept dialogue, one question at a time
  └─ blocked? → freeflow        → dump everything, plugin organizes
write [section]                 → generates draft in author's voice
demolish [file]                 → hostile critique, logic and structure
demolish-persona editor         → structural diagnosis
demolish-persona target-reader  → does it work for the intended reader?
demolish-persona hostile-reader → does the argument hold under pressure?
integrate                       → incorporates all responses, one change at a time
  → chapter complete ✅

EVERY 3-4 CHAPTERS
─────────────────────────────────────
consistency-check     → term drift, contradicted claims, broken promises, tone arc

OPTIONAL (narrative books)
─────────────────────────────────────
character-interview [name]   → psychological profile before writing key scenes
character-check [name] [ch]  → behavioral consistency check after writing

CLOSING (once, at the end)
─────────────────────────────────────
write-opening         → introduction — written last
write-closing         → conclusion — resolves open promises
manuscript-final      → arc audit + optional process note + assembled manuscript
```

---

## Genre Presets

Selected during `setup-book`. Adapts vocabulary, questions, and demolition logic.

| Preset | Central concept | Demolition focus |
|---|---|---|
| `essay` | Thesis | Falsifiability, circularity, scope |
| `fiction` | Dramatic question | Motivation, consequence, earned change |
| `manual` | Transformation | Evidence, context dependency, prerequisites |
| `biography` | Interpretation | Evidence, selection bias, alternative readings |
| `fable` | The moral | Earned ending, displacement, narrative necessity |
| `childrens-book` | The heart | Age appropriateness, child logic, pacing, read-aloud quality |

---

## Reader Personas

Used with `/ghost-writer:demolish-persona`.

| Persona | What they find |
|---|---|
| `target-reader` | Accessibility, relevance, engagement |
| `hostile-reader` | Unsupported assertions, avoided objections |
| `domain-expert` | Technical gaps, overclaims |
| `editor` | Structure, pacing, prose problems |
| `out-of-target` | Unexplained jargon, invisible assumptions |

Custom personas: copy `personas/custom-template.md` and fill in.

---

## Core Principles

- **Claude formalizes, doesn't invent.** Concepts come from the author.
- **One question at a time.** Always.
- **No change without confirmation.** The author approves every modification.
- **Demolition strengthens.** Every weakness found now is one less for hostile readers.
- **Genre adapts everything.** Vocabulary, questions, structure — all shaped by the preset.
- **Memory is explicit.** Every term, promise, and demolition cycle is written down.
- **The introduction is written last.**

---

## Publishing to claude.com/plugins

1. Push to a public GitHub repo
2. Update `.claude-plugin/plugin.json` with your name and repo URL
3. Test locally: `claude --plugin-dir ./ghost-writer`
4. Submit at: `claude.ai/settings/plugins/submit`

---

## Credits

Original method: [Simone Di Roma — quantum_fatalism](https://github.com/simonediroma/quantum_fatalism)
License: MIT
