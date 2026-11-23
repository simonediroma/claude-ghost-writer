---
description: Export the assembled manuscript as a readable PDF. Generates a clean, well-formatted PDF with cover page, table of contents, and chapter layout — ready to share with beta readers or distribute as a first draft. Run after manuscript-final has assembled the manuscript.
---

# Skill: Export PDF

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

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

Read from `book.config.json`:
- `title` — book title
- `author_voice` or `author_profile.name` — author name
- `language` — for font selection
- `version` — for cover page

Read the manuscript file at `manuscript/[title]-final.md`.

If `export_pdf.py` does not exist in the project root, write it now (see the full script below), then run:

```bash
pip install reportlab --quiet
python3 export_pdf.py .
```

---

## Script: export_pdf.py

If the file doesn't exist, write the following content to `export_pdf.py` in the project root, then run the commands above.

The script reads `book.config.json` and `manuscript/[title]-final.md`, generates a PDF with cover page, table of contents, and chapter layout using ReportLab, and saves it to `manuscript/[title]-final.pdf`.

Key functions to implement:
- `load_config(project_dir)` — reads `book.config.json`
- `find_manuscript(project_dir, config)` — locates the final markdown file
- `parse_manuscript(md_path)` — parses markdown into h1/h2/paragraph sections
- `make_styles()` — ReportLab styles (cover_title, chapter_title, body, blockquote)
- `BookDocument(BaseDocTemplate)` — custom page template with footer (title + page number)
- `build_cover(config, styles)` — cover page with title, author, date
- `build_toc(toc_entries, styles)` — table of contents
- `build_chapters(sections, styles)` — body content
- `export_pdf(project_dir)` — main entry point

Generate the full working script and write it to `export_pdf.py`. Use A4 format, Times New Roman for body, 11pt, justified alignment.

---

## After export

Tell the author:
> PDF exported to `manuscript/[title]-final.pdf`. Ready to share with beta readers.
>
> To convert to other formats for publication, Claude can also export to `.docx` (for editors) or `.epub` (for ebook distribution) — just ask.
