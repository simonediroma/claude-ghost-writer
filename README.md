# RAMA

A ghost-writing workflow for Claude, built for novels written from a
**synopsis, outline, style guide and story bible**. RAMA reads those files,
asks you what they don't settle, and writes chapters that follow your style
guide to the letter. It then checks every chapter against the guide, the
outline and the rest of the book, and builds the finished book as `.md`,
`.docx` and `.epub`.

Every question RAMA asks is a **survey**: three concrete answers drawn from
your book, plus a write-in.

RAMA is a fork of [claude-ghost-writer](https://github.com/simonediroma/claude-ghost-writer)
by Simone Di Roma (MIT). Several of its editorial skills are adapted here.

## The workflow

| Command | What it does |
|---|---|
| `/rama:config` | Finds and checks the project files and asks about gaps and contradictions. Builds any missing file by interview, or adapts an old style guide. Writes the **RAMA Log**. |
| `/rama:beats 5` | Story beats for chapter 5, built on the outline **and** on what chapters 1–4 actually established. Surveys you first, then saves to the Beats file. |
| `/rama:compose 5` | Writes chapter 5 from its beats, to the style guide, self-checks it against the guide's revision checklist, and adds it to the manuscript once you approve. |
| `/rama:check 5` · `5-7` · `all` | Style guide, outline/beats, continuity, timeline, characters, period accuracy, copy and craft. Ranked report, then fixes one at a time with your OK. |
| `/rama:compile` | `.md` + `.docx` (via **manuscript-docx**) + `.epub` (via **manuscript-epub**). Uses the chapter-head and divider glyphs in `glyphs/`, and offers to draw them if they're missing. |

### Editorial extras (adapted from ghost-writer)

| Command | What it does |
|---|---|
| `/rama:resume` | Where you left off, and the one next step. |
| `/rama:demolish 5` | Hostile read for story logic, motivation, stakes and POV cheats, one criticism at a time. |
| `/rama:review 5 editor` / `all` | Persona reads: editor, target reader, hostile reader, period expert, out-of-target. |
| `/rama:integrate 5` | Turns your answers from demolish/review into approved text changes. |
| `/rama:retune 5` | "This isn't my voice." Realigns the voice to a rough sample from you. |
| `/rama:freeflow 7` | Brain-dump mode, which turns the dump into beats or decisions. |
| `/rama:character-interview Name` / `character-check 5 Name` | Deep character profiles and consistency checks. |
| `/rama:corrections` | Review PDF with paragraph IDs, then imports your annotations, notes or photos and applies them. |

## A RAMA project

```
The Shape of the Sea/
├── The Shape of the Sea — Outline.md        # with ## Synopsis, or a separate Synopsis file
├── The Shape of the Sea Style Guide.md
├── The Shape of the Sea — Story Bible.md    # if a series or complex
├── The Shape of the Sea.md                  # the manuscript: every chapter, one file
├── The Shape of the Sea — Beats.md          # written by beats
├── The Shape of the Sea — RAMA Log.md       # written by config; RAMA's memory
├── The Shape of the Sea — Check Report.md   # written by check
├── glyphs/Chapter_head.png, divider.png     # for compile
└── build/                                   # compile output
```

File names are matched by role, so `Outline.md` works too. The full contract
(manuscript heading format, paragraph IDs, RAMA Log sections) is in
[`shared/project-files.md`](shared/project-files.md). The survey rules are in
[`shared/survey.md`](shared/survey.md).

## Install

### Claude Code / Cowork (plugin, slash commands)

```bash
claude plugin marketplace add mweintr/RAMA
claude plugin install rama@mweintr-rama
```

Or, for a local checkout: `claude plugin marketplace add /path/to/RAMA`.

Open your book folder and run `/rama:config`.

### claude.ai (Projects)

Plugins aren't available in claude.ai chat, so RAMA ships each skill as an
uploadable zip in [`dist/claude-ai/`](dist/claude-ai/). Upload each one under
**Settings → Capabilities → Skills**. In claude.ai the skills are named
`rama-config`, `rama-beats` and so on. Ask for them by name ("run rama-beats
for chapter 5"), or with `/` where your client supports skill commands.

Put the book's files in a Project. Project files are read-only, so when RAMA
updates the manuscript, log or beats, it gives you the full new file to
download and tells you which Project file to replace.

### Companion skills

`/rama:compile` needs the **manuscript-docx** and **manuscript-epub** skills
installed. `check` can hand claims it can't verify to a **fact-check** skill,
if you have one.

## Developing

Edit skills in `skills/<name>/SKILL.md` and shared rules in `shared/`. Then run:

```bash
python3 scripts/build.py
```

This copies `shared/*.md` into every skill's `references/` folder and rebuilds
the claude.ai zips in `dist/claude-ai/`. Commit the results.

## License

MIT. See [LICENSE](LICENSE). Original work © Simone Di Roma; RAMA
modifications © Michael Weintraub.
