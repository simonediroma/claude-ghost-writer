---
description: Export the assembled manuscript as a DOCX file. Generates a clean Word document with proper styles — ready to send to an editor, literary agent, or traditional publisher. Run after manuscript-final has assembled the manuscript.
---

# Skill: Export DOCX

> **Language**: `book.config.json → language`. Author may write in any language; always reply in the configured one. Default: English.

Converts the assembled manuscript into a standard DOCX document. The format expected by most literary agents, editors, and traditional publishers.

---

## Prerequisites

Check that `manuscript/[title]-final.md` exists. If not:
> The manuscript hasn't been assembled yet. Run `/ghost-writer:finish` first, then export to DOCX.

---

## What it generates

- **Document styles**: Title, Heading 1 (chapters), Heading 2 (sections), Normal (body text), Block Quote
- **Standard manuscript formatting**: 12pt Times New Roman, double-spaced, 1-inch margins (industry standard for submissions)
- **Cover page**: title, author name, word count
- **Output**: `manuscript/[title]-final.docx`

---

## How to run

This skill generates a Python script and executes it using the computer tool.

Read from `book.config.json`:
- `title` — book title
- `author_profile.name` or `author_voice` — author name  
- `language` — for locale-aware formatting
- `version` — for cover page

Read the manuscript file at `manuscript/[title]-final.md`.

Then run `export_docx.py` from the project root:

```bash
python3 export_docx.py .
```

---

## After export

Tell the author:
> DOCX exported to `manuscript/[title]-final.docx`. Ready to send to editors, agents, or collaborators.
>
> The document uses standard manuscript formatting (12pt Times New Roman, double-spaced). If a publisher specifies different requirements, the formatting can be adjusted — just ask.
