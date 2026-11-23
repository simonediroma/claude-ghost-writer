---
description: The book graph — characters, organizations, objects, places, concepts, terms and events (card types depend on the genre preset), linked to each other and to the exact line of the chapter they come from. Feeds itself: only chapters with `status: complete` enter it, and it re-syncs whenever a complete chapter changes version. Other skills call its Sync procedure; run it by hand only to look something up, to force a sync, or to migrate an old graph.
---

# Skill: Graph

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

A map of everything that exists in the book, built **only from what the chapters say**. Revise, consistency-check, character-check and write read the pertinent cards instead of re-reading chapters.

The graph is a derived artifact: it never asks the author for confirmation. The trigger is the chapter `version`, not file saves — there is no hook.

---

## The Rules

1. **Only what is written in the chapters enters a card**, with its source. Never from `outline.md`, `book-memory.md`, character files or memory.
2. **Every source carries a quote**: `source: "c3:19"` (chapter 3, line 19 of the file) + `quote:` a short exact excerpt of that line (3–15 words) that supports the entry. Lines shift; the quote is what lets the script re-anchor the source.
3. What the text does **not** say goes in `not_said`. Contradictions and errors still to fix go in `open`. Reader's observations that are not errors (echoes, parallels, deliberate ambiguities) go in `notes`. Never fill a gap.
4. **Only chapters with `status: complete` are analyzed.** Drafts are never read for the graph, not even when their version changes.
5. **Edit only `graph/cards/`.** `graph/view/`, `graph/INDEX.md`, `graph/graph.json`, `graph/snapshots/` and `graph/chapters.yaml` are written by `graph.py`.
6. A fact removed from the text is **removed from the card**, not kept.

---

## Layout

```
graph/
  chapters.yaml               analyzed chapters: title, file, analyzed_version
  snapshots/c03.md            copy of the analyzed text of chapter 3 (for diffs and validation)
  cards/<type>/<id>.yaml      the only files to edit
  view/<type>/<id>.md         readable cards with links, backlinks, event chain
  view/chapters/03.md         event chain diagram + cards touched by chapter 3
  INDEX.md                    every card, every open point
  graph.json                  nodes + edges
```

Folders and field names are in English; card **content** is in the book's language.

### Card types

Read from the preset (`presets/[preset].md → ## graph adaptations`, block `graph-types`):

| Preset | Types |
|---|---|
| fiction | characters, organizations, objects, places, concepts, terms, events |
| biography | people, organizations, places, objects, events, sources, terms |
| essay | concepts, terms, theses, sources, people |
| manual | concepts, terms, procedures, tools, sources |
| childrens-book | characters, places, objects, events, terms |
| fable | characters, places, objects, events, concepts |

### Card format

One entry per line, flow style. `id` = file name (lowercase, hyphens).

```yaml
id: marta
name: "Marta"
aliases: ["la guardiana"]
chapters: [1, 2]
summary: "The lighthouse keeper."
traits:
  - {text: "Climbs the lighthouse at six every morning", source: "c1:8", quote: "alle sei del mattino, come ogni giorno"}
state:
  - {chapter: 2, text: "Obeys the note: leaves the lamp off", source: "c2:8", quote: "Marta non accese la lanterna"}
not_said:
  - {text: "The text never gives Marta's age."}
open:
  - {text: "Who wrote the note?"}
relations:
  - {to: ferro, type: "lives with", source: "c1:14", quote: "con il gatto Ferro"}
```

Events add: `chapter`, `order` (e.g. `2.1`), `when`, `where` (id), `on_stage` (false = reported), `involved` (ids), `after` (ids of the events it follows from), `facts` (like `traits`).

Several sources for one entry: `source: "c1:23, c3:19"`, `quote: ["…", "…"]` (one quote per reference). A range `c6:9-11` means the quote is somewhere in lines 9–11.

`chapters` is optional: the views add every chapter cited by a source.

---

## Sync

The procedure other skills run at the end. Also run it when called directly with no argument.

1. `python3 graph.py start` — prints what to do and records the starting state. If it says *up to date* or *not created yet*, stop silently (no report line).
   - The graph is **born** here: the first time a chapter is `complete` and `graph/` does not exist, `start` creates it.
2. For each chapter listed **NEW**: read the whole chapter (full text, with line numbers). Write the cards it supports: find existing cards first (`python3 graph.py find <name>`), extend them; create new ones only for things that matter again or carry meaning. Add the events in order.
3. For each chapter listed **TO RE-ANALYZE**: do **not** re-read the chapter. Read only:
   - the changed paragraphs printed by `start` (`+ new cN:line` / `- old cN:line`);
   - the cards with **LOST** sources, and the cards that `python3 graph.py find --chapter N` returns whose entries speak of the changed paragraphs.
   Then: add what the new paragraphs say (sources point to the **new** line numbers); for every LOST source, remove the entry if the text no longer says it, otherwise fix `source` and `quote`; adjust entries contradicted by the change. Sources marked *moved* need nothing: `commit` re-anchors them.
   - *migrated from an older version — read the whole text*: treat as NEW but update the existing cards.
4. Edit cards directly, or write a patch and run `python3 graph.py apply patch.txt`:
   ```
   @ characters/marta
   traits: {text: "…", source: "c4:9", quote: "…"}
   -traits: "beginning of the text of the entry to remove"
   aliases+: "new alias"
   summary: "…"
   ```
5. `python3 graph.py commit N [N …]` (all the chapters from step 1). It re-anchors moved sources, saves the snapshot and the analyzed version, rebuilds the views. It **stops and changes nothing** on a non-existent id, a malformed source, a quote not found at its line, a source citing a chapter that is not analyzed. Fix and run it again.
6. Print its one-line report to the author, nothing more:
   > Graph synced (c4 v2.1): 3 new cards, 5 modified, 0 removed, 12 sources re-anchored · open questions: +2, 14 total.

7. If `site.yaml` exists, run `python3 build_site.py` (generate the script first if it doesn't exist — see `/ghost-writer:site`) and add to the report: *Site rebuilt: commit and push `docs/` to publish it.*

Never ask the author to confirm anything in the graph.

### Chapter states (`python3 graph.py check`)

| State | Meaning | Action |
|---|---|---|
| TO ANALYZE | `complete`, never analyzed | sync (full read) |
| TO RE-ANALYZE | `complete`, `version` ≠ analyzed version | sync (diff only) |
| SUSPENDED | analyzed, now back to another status | none: its cards stay at the analyzed version (validated against the snapshot) until it is `complete` again |
| draft | never analyzed, not complete | ignored |
| NOTE: text changed without a version bump | complete, text differs from snapshot | ignored — the version is the only source of truth; bump it to re-sync |

---

## Consulting the Graph (for other skills)

Lazy reading, always — never load the whole graph into context.

- `python3 graph.py find <name or alias>` → the card files for that name.
- `python3 graph.py find --chapter N` → every card touched by chapter N.
- `graph/INDEX.md` → one line per card + all open points (read it only to locate cards).
- Read the `.yaml` card (or its `view/…md`) — only the ones the task needs.

A card is evidence with a line number: when a check needs the exact wording, open the chapter at that line, not the whole chapter. Cards of a SUSPENDED chapter describe its analyzed version, not the current draft.

If `graph/` does not exist, the skill falls back to its usual reading.

---

## Manual Use

- `/ghost-writer:graph` → run Sync.
- `/ghost-writer:graph check` → show the chapter states.
- `/ghost-writer:graph find <name>` → show the card(s) to the author (read `graph/view/...md`).
- `/ghost-writer:graph build` → `python3 graph.py build` (validate + regenerate views).

### Migration from the legacy format

A graph in the old format (`grafo/` with `schede/`, `capitoli.yaml`, Italian fields, sources without quotes):

1. `python3 graph.py migrate grafo/` — converts folders and fields, copies the chapters as snapshots, and derives each quote from the line indicated (quoted passages of the entry, then shared wording, then a nearby line). It never invents a quote: sources it cannot convert are listed in `graph/MIGRATION.md` and in `graph/migration-quotes.yaml`.
2. For each entry in `migration-quotes.yaml`: read `line`, write in `quote` a short exact excerpt that supports `text`; if the fact is on another line, add `new_ref: "cN:line"`. If nothing in the chapter supports it, leave `quote: null` and tell the author.
3. `python3 graph.py fill-quotes graph/migration-quotes.yaml`, then `python3 graph.py build`.
4. Chapters whose current version differs from the version analyzed in the old graph are marked for a full re-read at the next sync.

The old `grafo/` folder is not touched: delete it yourself once the new graph builds.

---

## Requirements

`graph.py` uses the Python standard library and PyYAML (`pip install pyyaml`). If PyYAML is missing the script says so and exits: tell the author the install command and skip the graph — never block the calling skill.

If `graph.py` does not exist in the project root, generate it from scratch before running any graph command. The script must implement all subcommands referenced in this skill: `start`, `find`, `apply`, `commit`, `check`, `build`, `migrate`, `fill-quotes`. It reads YAML cards from `graph/cards/**/*.yaml`, maintains `graph/graph.json`, `graph/INDEX.md`, `graph/view/`, `graph/chapters.yaml`, and `graph/snapshots/`. Use only the Python standard library plus PyYAML.
