# Collaborating on this book

This book is a Git repository. Collaboration works like any software project.

---

## Solo writing

Write directly on `main`. No branches needed.

---

## Co-authoring

Each author works on their own branch.

```bash
# Author A works on chapter 3
git checkout -b chapter-03-draft

# Write, demolish, integrate
# When done:
git add chapters/03-*.md book-memory.md demolition-history.md
git commit -m "Chapter 3: first complete cycle v1.1"
git push origin chapter-03-draft
```

Open a PR when the chapter is ready for the other author to review. Disagreements on integration choices → discuss in PR comments, resolve before merging.

---

## Editor involvement

The editor works on a review branch:

```bash
git checkout -b editorial-review-ch3
# Run /ghost-writer:review or /ghost-writer:demolish-persona
# Propose changes via integrate
git commit -m "Editorial: persona review Ch.3 — 4 issues flagged"
git push
```

Author reviews the PR, accepts or rejects changes, merges.

---

## What to commit

Always commit together:
- The chapter file (`chapters/NN-*.md`) — includes Demolition Log
- `book-memory.md` or the relevant `memory/part-N.md`
- `demolition-history.md`
- `outline.md` if status changed

Commit message convention:
```
[chapter N] action: description
```

Examples:
```
[ch3] draft: first version
[ch3] demolish: cycle 1 — 3 issues resolved, 1 deferred
[ch3] integrate: v1.1 — falsifiability issue resolved
[ch5] write-opening: introduction draft
[book] consistency-check: part 1 audit complete
```

---

## Conflict resolution

`book-memory.md` and `demolition-history.md` are the most likely to have merge conflicts — both authors may update them simultaneously.

Resolve conflicts manually: these files are plain text, conflicts are readable, and the right resolution is usually "keep both entries."

`sessions/` files are per-author — no conflicts expected if each author uses their own session names.
