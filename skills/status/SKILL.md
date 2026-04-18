---
description: Show the current state of the book project. Chapters completed, in draft, or not yet written. Suggests the next step. Use any time to get an overview of the project.
---

# Skill: Project Status

> **Language**: Read `book.config.json → language`. Write all output — questions, feedback, summaries, logs — in that language. The author may respond in any language; always reply in the configured language. Default: English.


Read `book.config.json` and `outline.md` and present a status report.

---

## Report Format

```
📚 [Book Title] — v[version]
─────────────────────────────────

✅ Complete:      X chapters
📝 Draft:         X chapters
⬜ To write:     X chapters

─────────────────────────────────
CHAPTERS

[✅/📝/⬜] Ch. 1 — [Title]     v[X.X]
[✅/📝/⬜] Ch. 2 — [Title]     v[X.X]
...

─────────────────────────────────
NEXT SUGGESTED STEP
[what to do now, based on status]
```

---

## Status Legend

- ✅ `complete` — written, demolition and integration done
- 🔄 `in-review` — written, demolition in progress
- 📝 `draft` — written, no revision yet
- ⬜ `to-write` — in outline only, no file yet

---

## Next Step Logic

- **Opening project for the day** → always suggest `/ghost-writer:session-start` first
- Outline is empty → suggest `/ghost-writer:setup-author` to start onboarding
- `book.config.json` incomplete → suggest `/ghost-writer:setup-book` or `/ghost-writer:setup-voice`
- Draft exists without demolition → suggest `/ghost-writer:demolish`
- Demolition done without integration → suggest `/ghost-writer:integrate`
- All chapters complete, no intro → suggest `/ghost-writer:write-opening`
- All chapters + intro complete, no conclusion → suggest `/ghost-writer:write-closing`
- All chapters + intro + conclusion complete → suggest `/ghost-writer:manuscript-final`
- Every 3-4 completed chapters → suggest `/ghost-writer:consistency-check`
- All integrated → suggest next chapter with `/ghost-writer:ask-before-writing` + `/ghost-writer:write`
