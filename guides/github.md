# Ghost Writer + GitHub — practical guide

How to use GitHub with the Ghost Writer plugin: why it pays off, how to connect it to Claude (Desktop and Code), and which GitHub features to use for the book's website.

---

## 1. Why use GitHub

A book written with Ghost Writer is a folder of text files (`chapters/`, `book.config.json`, `book-memory.md`, `outline.md`, `graph/`, `podcast/`…). Putting it on GitHub gives you:

| Benefit | What it means for the author |
|---|---|
| **History of every version** | Every `demolish` → `integrate` cycle changes the text. With git you can review or restore any earlier version of a chapter, even months later. |
| **Automatic backup** | The book doesn't live only on your computer. If the disk dies, `git clone` and carry on. |
| **Work from several devices** | Write in Claude Desktop at home, revise with Claude Code on the laptop, or from claude.ai/code in the browser: same folder, always up to date. |
| **Collaboration** | Co-authors, editors and beta readers can propose changes (pull requests) or leave notes (issues) without touching the main text. |
| **Free website** | `/ghost-writer:site` generates a site ready for **GitHub Pages**: free hosting, HTTPS included. |
| **Distribution** | PDF, EPUB and podcast MP3s can live in GitHub **Releases**, with a stable link for each version. |
| **Gallery** | `/ghost-writer:gallery` opens a pull request on claudeghostwriter.com to list the book in the site's gallery. Without a GitHub account it falls back to a form; with one it's fully automatic. |

**Private or public repository?** Drafts usually belong in a **private** repo. Note: GitHub Pages on a private repo requires a paid plan (GitHub Pro). Free alternative: a private repo for the book + a public repo just for the site (see §3.5).

---

## 2. Setup

### 2.1 Prerequisites (once)

1. Create an account on [github.com](https://github.com).
2. Install **git** ([git-scm.com](https://git-scm.com)) and the **GitHub CLI** ([cli.github.com](https://cli.github.com)).
3. Log in from the terminal:

   ```bash
   gh auth login        # GitHub.com → HTTPS → log in with browser
   gh auth setup-git    # let git use gh's credentials
   ```

4. Turn the book folder into a repository:

   ```bash
   cd my-book
   git init
   git add .
   git commit -m "Start of the book"
   gh repo create my-book --private --source . --push
   ```

The plugin already ships a `.gitignore` that excludes Piper voices, audio samples and music kits (large, regenerable files).

### 2.2 Claude Code (terminal, IDE, desktop app)

Claude Code uses the `git` and `gh` installed on your computer directly: after §2.1 nothing else is needed.

**Install the plugin from GitHub:**

```bash
/plugin marketplace add simonediroma/claude-ghost-writer
/plugin install ghost-writer@simonediroma-ghost-writer
/ghost-writer:check
```

**Update the plugin** when a new version is out:

```bash
/plugin marketplace update simonediroma-ghost-writer
```

**Day-to-day use** — just ask in plain language:

- *"Commit chapter 3 with a message summarizing the integration"*
- *"Show me what changed in chapter 5 since yesterday"*
- *"Restore chapter 2 to the version before the demolition"*
- *"Push to GitHub"*

Recommended habit: one commit at the end of every `/ghost-writer:chapter` cycle and after every `integrate`.

**Optional — Claude inside GitHub.** `/install-github-app` installs the Claude GitHub App on the repo: you can then write `@claude` in an issue or pull request (e.g. *"@claude apply the corrections in this issue to chapter 4"*).

**Claude Code on the web (claude.ai/code).** Connect GitHub in the settings and pick the book's repo: Claude works on a cloud copy and pushes to a branch. Handy for working from a phone or a computer with nothing installed.

### 2.3 Claude Desktop (Chat and Cowork)

**Install the plugin:**
- in one click from the [Claude plugin directory](https://claude.ai/customize/plugins/id/4b831b3b-c718-4a20-b786-598ed6566696%40anthropic-plugin-directory) (it syncs to Claude Code and Cowork), or
- download the `.plugin` file from [claudeghostwriter.com](https://claudeghostwriter.com) and drag it into the app (or upload it from **Settings → Plugins**).

**Connect GitHub:**
1. **Settings → Connectors → GitHub → Connect** and authorize access.
2. In a chat or Project: **+** button → **Add from GitHub** → pick the repo and files (e.g. `outline.md`, `book-memory.md`, the chapters).

The connector gives Claude the book's **context** (read chapters, outline, memory) to discuss it, brainstorm or review. To **write** files and commit, use Cowork on the book's local folder, or the **Code** tab of the Desktop app (that's Claude Code, and works as in §2.2).

Typical mixed workflow: write and commit with Claude Code / Cowork → in Chat, with the GitHub connector, discuss the chapter you just pushed.

---

## 3. GitHub features for the website

`/ghost-writer:site` generates `docs/index.html`: a single page with no external dependencies — cover, presentation, download, characters/key ideas, podcast and book graph.

### 3.1 GitHub Pages — hosting (free)

Simplest method, no configuration:

1. Commit and push `docs/`.
2. Repo → **Settings → Pages → Build and deployment → Deploy from a branch** → branch `main`, folder `/docs` → **Save**.
3. After about a minute the site is live at `https://<user>.github.io/<repo>/`.

Limits: 1 GB per site, 100 MB per file, about 100 GB of bandwidth per month. An episode at 96 kbps is about 0.7 MB per minute.

### 3.2 Custom domain

1. **Settings → Pages → Custom domain** → `www.mybook.com` → Save (GitHub creates the `CNAME` file).
2. At your DNS provider: a `CNAME` record from `www` to `<user>.github.io`.
3. Tick **Enforce HTTPS** once it becomes available.

### 3.3 GitHub Actions — site always up to date

Instead of rebuilding and pushing `docs/` by hand, let GitHub regenerate it on every push. Create `.github/workflows/site.yml`:

```yaml
name: Book site
on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install pyyaml pillow
      - run: python3 build_site.py
      - uses: actions/upload-pages-artifact@v3
        with:
          path: docs

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

Then **Settings → Pages → Source: GitHub Actions**. From then on every push (new chapter, graph sync, new episode) updates the site on its own, and `docs/` no longer needs to be committed.

### 3.4 Releases — PDF, EPUB and podcast

Releases accept files up to 2 GB, don't count toward the 1 GB Pages limit, and give a stable link for each version of the book:

```bash
gh release create v1.0 manuscript/my-book.pdf manuscript/my-book.epub \
  --title "First edition" --notes "Chapters 1–12"
```

Direct file link: `https://github.com/<user>/<repo>/releases/download/v1.0/my-book.pdf`. Use it as `book.download` in `site.yaml`, or upload the MP3s to a release and use that address as `podcast.base_url` (see `/ghost-writer:podcast`). Worth it once the podcast passes a few hundred MB.

### 3.5 Private book, public site

If the book's repo is private and you don't have GitHub Pro:

1. Create a second, **public** repo, e.g. `my-book-site`.
2. Copy the contents of `docs/` there after each build (or ask Claude: *"copy docs/ to the site repo and push"*).
3. Enable Pages on the public repo (§3.1).

Drafts, demolitions and memory stay private: only what you approved in `site.yaml` goes online.

### 3.6 Issues and Discussions — reader feedback

- **Issues**: open one issue per chapter and ask beta readers to comment there. Then paste the text into `/ghost-writer:corrections import` to turn it into corrections.
- **Discussions** (Settings → Features): a public space for the site's readers. Add the link in `site.yaml` or the footer.

### 3.7 claudeghostwriter.com gallery

Once the site is live, `/ghost-writer:gallery` drafts the book entry and, with `gh` authenticated, opens the pull request on the official site's repo (fork + branch + PR). Without `gh` it generates a link to a pre-filled issue form. Nothing is sent without your OK.

---

## Quick summary

| Goal | Tool |
|---|---|
| Versions and backup of the book | private repo + commit after every `integrate` |
| Writing with Claude | Claude Code (CLI, IDE, Code tab) or Cowork |
| Discussing the book in chat | Claude Desktop + GitHub connector |
| Free website | `/ghost-writer:site` + GitHub Pages |
| Self-updating site | GitHub Actions |
| Heavy downloads and podcast | GitHub Releases |
| Reader feedback | Issues / Discussions |
| Public showcase | `/ghost-writer:gallery` |
