---
description: Quick installation and setup check. Run this first after installing the plugin to verify everything works. Takes about 60 seconds. No content is created or modified. Also useful any time something feels broken.
---

# Skill: Check

> **Language**: Read `book.config.json → language`. Write all output in that language. Default: English.

Quick verification that the plugin is installed correctly and the project is ready to use.

Nothing is created or modified. This is read-only.

---

## What it checks

Run all checks silently, then present results in one block.

### 1. Plugin structure
Verify these files and directories exist:

| Path | Required |
|---|---|
| `.claude-plugin/plugin.json` | ✅ required |
| `book.config.json` | ✅ required |
| `outline.md` | ✅ required |
| `book-memory.md` | ✅ required |
| `demolition-history.md` | ✅ required |
| `skills/` directory | ✅ required |
| `presets/` directory | ✅ required |
| `personas/` directory | ✅ required |
| `chapters/` directory | ✅ required |
| `sessions/` directory | ✅ required |
| `characters/` directory | ⚪ optional |
| `memory/` directory | ⚪ optional (long-form only) |

### 2. Plugin manifest
Read `.claude-plugin/plugin.json`. Check:
- `name` is set and not the default
- `version` is present
- `author.name` is not empty or "Your Name"

### 3. Project configuration
Read `book.config.json`. Check:
- `title` is set and not "Your Book Title"
- `language` is set to a valid value
- `preset` is set (essay / fiction / manual / biography)
- `author_voice.tone` is not empty or default placeholder

### 4. Preset file
Based on `preset` value, verify the corresponding file exists:
- `presets/essay.md`
- `presets/fiction.md`
- `presets/manual.md`
- `presets/biography.md`

### 5. Onboarding status
Check `book.config.json` for:
- `author_profile` present → onboarding session 1 complete
- `book_profile` present → onboarding session 2 complete
- `author_voice.tone` not empty/default → onboarding session 3 complete

### 6. Skills count
Count `.md` files in `skills/` subdirectories. Expected: 23.

### 7. Quick smoke test
Generate one sentence in the author's voice (from `book.config.json → author_voice`) about the book's topic (from `book_profile → premise`). This proves the voice profile is readable and usable.

---

## Output format

```
GHOST WRITER — INSTALLATION CHECK
──────────────────────────────────────

Plugin structure
  ✅ All required files present
  ⚪ characters/ — not present (optional, create when needed)

Plugin manifest
  ✅ Name: ghost-writer
  ✅ Version: 1.0.0
  ⚠️  Author: still set to "Your Name" — update before publishing

Project configuration
  ✅ Title: [book title]
  ✅ Language: [language]
  ✅ Preset: [preset]
  ⚠️  author_voice.tone: still set to placeholder — run /ghost-writer:setup-voice

Onboarding status
  ✅ Session 1 — Author profile: complete
  ✅ Session 2 — Book profile: complete
  ⚠️  Session 3 — Voice profile: incomplete — run /ghost-writer:setup-voice

Skills
  ✅ 23 skills found

Voice smoke test
  ✅ "[one sentence generated in the author's voice about the book's topic]"

──────────────────────────────────────
STATUS: [READY / READY WITH WARNINGS / NOT READY]

[If READY]:
Everything looks good. Run `/ghost-writer:session-start` to begin.

[If READY WITH WARNINGS]:
The plugin works but some configuration is incomplete. Fix the warnings above when convenient — they won't block you from writing.
Next step: [most important action based on warnings]

[If NOT READY]:
Something is missing. Fix the errors above before writing.
Next step: [most critical fix]
```

---

## Status logic

**READY** — all required files present, `book.config.json` has real values, at least session 1 onboarding complete, smoke test passed.

**READY WITH WARNINGS** — plugin works but: author name still default, voice profile incomplete, or `plugin.json` not yet personalized for publishing.

**NOT READY** — required files missing, `book.config.json` still has placeholder values, or smoke test failed.
