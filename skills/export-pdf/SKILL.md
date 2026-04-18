---
description: Export the assembled manuscript as a readable PDF. Generates a clean, well-formatted PDF with cover page, table of contents, and chapter layout — ready to share with beta readers or distribute as a first draft. Run after manuscript-final has assembled the manuscript.
---

# Skill: Export PDF

> **Language**: Read `book.config.json → language`. Write all output in that language. Default: English.

Converts the assembled manuscript into a shareable PDF. Clean typography, minimal design, ready to send.

---

## Prerequisites

Check that `manuscript/[title]-final.md` exists. If not:
> The manuscript hasn't been assembled yet. Run `/ghost-writer:finish` first, then export to PDF.

---

## What it generates

- **Cover page**: title, author name, version/date
- **Table of contents**: chapter titles with page numbers
- **Chapter pages**: clean body text, chapter headings, page numbers in footer
- **Output**: `manuscript/[title]-final.pdf`

---

## How to run

This skill generates a Python script and executes it using the computer tool.

Read from `book.config.json`:
- `title` — book title
- `author_voice` or `author_profile.name` — author name
- `language` — for font selection
- `version` — for cover page

Read the manuscript file at `manuscript/[title]-final.md`.

Then run the export script (see below).

---

## After export

Tell the author:
> PDF exported to `manuscript/[title]-final.pdf`. Ready to share with beta readers.
>
> To convert to other formats for publication, Claude can also export to `.docx` (for editors) or `.epub` (for ebook distribution) — just ask.
