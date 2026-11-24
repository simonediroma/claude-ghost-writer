---
description: Submit the book to the gallery on claudeghostwriter.com. Drafts the book entry with the author (title, genres, short description, links, cover), validates it against the site's rules, then opens a pull request on the website repository with the GitHub CLI — or, without it, a pre-filled "Add my book" issue. Nothing is sent without the author's explicit OK.
---

# Skill: Gallery

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English. The entry itself (fields, description, page text) is written in the **book's** language.

Shows the book in the public gallery at https://www.claudeghostwriter.com/books/. The website lives in the repository `simonediroma/claudeghostwriter.com`; each book is one folder:

```
content/books/<slug>/
  index.md     required
  cover.jpg    optional — .jpg, .png or .webp, 2:3 ratio, max 2 MB
```

The maintainer reviews every submission. The site updates a few minutes after the merge.

---

## Rules of the site (mirror of `scripts/validate_books.py`)

| Field | Required | Rule |
|---|---|---|
| `title` | yes | |
| `author` | yes | |
| `genres` | yes | YAML list, only: `essay`, `fiction`, `manual`, `biography`, `fable`, `childrens-book` |
| `description` | yes | max **300 characters**, shown on the card |
| `links` | yes | list of `{label, url}`; every `url` a full `https://` URL; no affiliate or tracking links |
| `language` | no | two-letter code (`en`, `it`, …) |
| `year` | no | |
| `date` | no | `YYYY-MM-DD`, newest first in the gallery |

- `slug` (folder name): lowercase-with-dashes, `^[a-z0-9]+(-[a-z0-9]+)*$`, from the title.
- The folder may contain only `index.md` and `cover.jpg` / `.jpeg` / `.png` / `.webp`.
- `index.md` starts with a `---` YAML front matter block; the text below it is shown on the book page (Markdown).

---

## Step 1 — What exists

Read silently:
- `book.config.json` → `title`, `subtitle`, `preset`, `language`, `author` section, `gallery` (a previous submission)
- `site.yaml` → `tagline`, `book.paragraphs` (reuse them: they are already approved)
- a cover: `cover.jpg`, `cover.png`, `cover.webp` in the book root
- public links: `site.yaml` / `podcast.base_url` (book website), `manuscript/` files, the git remote (`git remote get-url origin`) if the repo is public

If `gallery.pr_url` or `gallery.issue_url` exists, this is an **update**: say so, show the link, and ask what to change. Updates go to the same branch / pull request.

Say in one line what you found:
> For the gallery I have: title, author, genre [preset], [cover], [N links]. Missing: [links / cover]. Shall we write the entry?

**Links are required.** If the book is not online anywhere yet, stop: suggest `/ghost-writer:site` (free website on GitHub Pages) or a store page, and come back after.

---

## Step 2 — The entry (author approves each field)

Propose, wait for yes / change:

1. **Title, author, year, language** — from `book.config.json`. Author = the name the author wants public (ask if unsure).
2. **Genres** — map the preset: `essay`→essay, `fiction`→fiction, `manual`→manual, `biography`→biography, `fable`→fable, `childrens-book`→childrens-book. More than one only if the author asks.
3. **Short description** — 1–2 sentences, the hook, in the author's voice (`author_voice`). From the site tagline if present. **Count the characters**; max 300. No spoilers.
4. **Links** — label + URL each, e.g. `Read online`, `Buy on Amazon`, `Listen to the podcast`, `Read on GitHub`. Only `https://`; strip tracking parameters (`utm_*`, `ref`, `tag`, `fbclid`, `gclid`).
5. **About the book** (page text, optional) — 1–3 short paragraphs: the premise, then a line on how Ghost Writer was used. Reuse `site.yaml → book.paragraphs` when they exist.
6. **Cover** (optional) — without it the site draws a typographic cover. If the image is over 2 MB, or not 2:3, offer to fix it with Pillow (`pip install pillow`): crop to 2:3 centred, resize to max 1200 px high, save as JPEG quality 85. Never crop without showing the result first.

Then ask the three confirmations — all three are required by the site, the author must say yes to each:
- the book was written (fully or in part) with the Ghost Writer plugin;
- they are the author, or have the author's permission to list it;
- they have the rights to publish the cover image.

---

## Step 3 — Build and check locally

Write the entry to `gallery/<slug>/` in the book project:

```markdown
---
title: "My Book"
author: "Author Name"
genres: [fiction]
language: en
year: 2026
date: 2026-11-24
description: "One or two sentences shown on the card."
links:
  - label: "Read online"
    url: "https://..."
---
Longer description shown on the book page (Markdown).
```

Quote string values (titles with `:` or `#` break YAML otherwise). `date` = today.

Check it with the rules above (a short inline Python check with PyYAML is enough: front matter parses, required fields, genres, description length, `https://` links, slug, allowed files, cover ≤ 2 MB). Fix and re-check until it passes. Show the final `index.md` to the author.

---

## Step 4 — Submit

Ask once, explicitly: *"Send it to the gallery now?"* Without a yes, stop here: the entry stays in `gallery/<slug>/`.

Check `gh auth status`.

### A. With the GitHub CLI (pull request)

Work in a temporary folder, never inside the book project:

```bash
WORK=$(mktemp -d)
gh repo fork simonediroma/claudeghostwriter.com --clone=false   # skip if the author owns the repo
gh repo clone <user>/claudeghostwriter.com "$WORK/site" -- --depth 1
cd "$WORK/site"
git remote add upstream https://github.com/simonediroma/claudeghostwriter.com 2>/dev/null
git fetch --depth 1 upstream main && git checkout -B book/<slug> upstream/main
mkdir -p content/books/<slug> && cp -r <book>/gallery/<slug>/. content/books/<slug>/
git add content/books/<slug>
git commit -m "Add book: <title>"
git push -u origin book/<slug>
gh pr create --repo simonediroma/claudeghostwriter.com --base main --head <user>:book/<slug> \
  --title "Add book: <title>" --body-file "$WORK/pr.md"
```

- `<user>` = `gh api user -q .login`. If it is `simonediroma` (the maintainer), skip the fork and push the branch to the main repository.
- If `content/books/<slug>/` already exists upstream and it is not this book, pick another slug (append the author's surname) and tell the author.
- `pr.md` follows the site's pull request template, with the checklist ticked as the author confirmed:

```markdown
## Add a book to the gallery

**Title:** <title>
**Author:** <author>
**How Ghost Writer was used** (optional, a few lines): <one or two lines>

### Checklist
- [x] One folder `content/books/<slug>/` with `index.md` (and optionally `cover.jpg` / `.png` / `.webp`, 2:3, max 2 MB)
- [x] The book was written (fully or in part) with the Ghost Writer plugin
- [x] I am the author, or I have the author's permission to list it
- [x] I have the rights to publish the cover image
- [x] Links point to the book (store page, website, repository) — no affiliate or tracking links
```

An update pushes a new commit to the same `book/<slug>` branch: the open pull request updates by itself.

### B. Without the GitHub CLI (issue form)

Build a pre-filled link to the **Add my book to the gallery** form (URL-encode every value):

```
https://github.com/simonediroma/claudeghostwriter.com/issues/new?template=add-book.yml
  &title=Book:%20<title>&author=<author>&genres=<genre>&language=<lang>&year=<year>
  &description=<description>&links=<Label | https://...  one per line>&about=<page text>
```

The `title` parameter sets the issue title, and dropdowns may not pre-fill: tell the author to fill **Title** and **Genre** by hand if they are empty.

Give the link to the author and tell them to: check the fields, drag the cover into *Cover image*, tick the three confirmations, and submit. Once the maintainer approves it, a pull request is created automatically. If the URL is longer than ~8000 characters, leave `about` out and tell the author to paste it from `gallery/<slug>/index.md`.

---

## After sending

Save to `book.config.json`:

```json
"gallery": {"slug": "<slug>", "pr_url": "<url or null>", "issue_url": "<url or null>", "submitted": "YYYY-MM-DD"}
```

Tell the author:
> Sent: [link]. The site checks it automatically (fields, links, cover, build); the maintainer reviews and merges, then the book appears at https://www.claudeghostwriter.com/books/<slug>/ within a few minutes. If a check fails, run `/ghost-writer:gallery` again to fix it.

Delete the temporary folder.

---

## Never

- Send anything without the author's yes to the three confirmations and to the final "send it".
- Push to `main` of the website repository, or force-push.
- Add affiliate or tracking links, or invent links that do not exist.
- Publish spoilers the author did not approve.
