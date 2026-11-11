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

Then run `export_epub.py` from the project root:

```bash
python3 export_epub.py .
```

---

## After export

Tell the author:
> EPUB exported to `manuscript/[title]-final.epub`. Ready to upload to Kindle Direct Publishing, Apple Books, or any e-reader.
>
> To test it: open the file in Calibre, Apple Books, or the Kindle Previewer.
