---
description: Export the assembled manuscript as an EPUB file. Generates a clean, well-structured EPUB compatible with all major e-readers (Kindle, Kobo, Apple Books, etc.). Run after manuscript-final has assembled the manuscript.
---

# Skill: Export EPUB

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Converts the assembled manuscript into a distributable EPUB. Standard format for e-readers and ebook platforms.

---

## Prerequisites

Check that `manuscript/[title]-final.md` exists. If not:
> The manuscript hasn't been assembled yet. Run `/ghost-writer:finish` first, then export to EPUB.

---

## What it generates

- **Metadata**: title, author, language, description (from `book_profile.premise`)
- **Cover page**: title and author
- **Table of contents**: chapter navigation
- **Chapter pages**: clean body text with proper EPUB structure
- **Output**: `manuscript/[title]-final.epub`

---

## How to run

This skill generates a Python script and executes it using the computer tool.

Read from `book.config.json`:
- `title` — book title
- `author_profile.name` or `author_voice` — author name  
- `language` — for EPUB metadata (`en`, `it`, `es`, `fr`, `de`, `pt`)
- `version` — for metadata

Read the manuscript file at `manuscript/[title]-final.md`.

If `export_epub.py` does not exist in the project root, generate it now (see Script section below), then run:

```bash
pip install ebooklib --quiet
python3 export_epub.py .
```

---

## Script: export_epub.py

If the file doesn't exist, generate a full Python script and write it to `export_epub.py`. The script must:

- Read `book.config.json` for `title`, `author_profile.name` (or `author_voice`), `language`, `version`
- Locate `manuscript/[title]-final.md`
- Parse the markdown: `# ` headings become chapters, `## ` become sections, paragraphs become body text, `> ` blockquotes are styled
- Build an EPUB using `ebooklib`: set metadata (title, author, language, UUID), create a cover page, table of contents, one HTML file per chapter
- Write the output to `manuscript/[title]-final.epub`

---

## After export

Tell the author:
> EPUB exported to `manuscript/[title]-final.epub`. Ready to upload to Kindle Direct Publishing, Apple Books, or any e-reader.
>
> To test it: open the file in Calibre, Apple Books, or the Kindle Previewer.
