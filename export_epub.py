#!/usr/bin/env python3
"""
Ghost Writer — EPUB Export Script
Converts manuscript/[title]-final.md to a clean EPUB for e-readers.
Requires: ebooklib (pip install ebooklib)
"""

import json
import re
import sys
from pathlib import Path
from datetime import date


def load_config(project_dir):
    config_path = Path(project_dir) / "book.config.json"
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def find_manuscript(project_dir, config):
    title = config.get("title", "manuscript").lower()
    slug = re.sub(r'[^a-z0-9]+', '-', title).strip('-')
    candidates = [
        Path(project_dir) / "manuscript" / f"{slug}-final.md",
        Path(project_dir) / "manuscript" / "manuscript-final.md",
    ]
    for c in candidates:
        if c.exists():
            return c
    manuscripts = list((Path(project_dir) / "manuscript").glob("*.md"))
    if manuscripts:
        return manuscripts[0]
    return None


def parse_manuscript(md_path):
    """Parse markdown into structured sections."""
    text = md_path.read_text(encoding='utf-8')
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    sections = []
    current = None
    buf = []

    for line in text.split('\n'):
        if line.startswith('# ') and not line.startswith('## '):
            if current:
                current['lines'] = buf
                sections.append(current)
            current = {'type': 'h1', 'title': line[2:].strip()}
            buf = []
        elif line.startswith('## '):
            if current:
                current['lines'] = buf
                sections.append(current)
            current = {'type': 'h2', 'title': line[3:].strip()}
            buf = []
        else:
            buf.append(line)

    if current:
        current['lines'] = buf
        sections.append(current)

    return sections


def md_to_html(lines):
    """Convert markdown lines to simple HTML paragraphs."""
    html_parts = []
    para = []

    def flush_para():
        if para:
            text = ' '.join(para).strip()
            if text:
                text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
                text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
                text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)
                html_parts.append(f'<p>{text}</p>')
            para.clear()

    for line in lines:
        if line.startswith('### '):
            flush_para()
            html_parts.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('> '):
            flush_para()
            html_parts.append(f'<blockquote><p>{line[2:].strip()}</p></blockquote>')
        elif line.strip() == '---':
            flush_para()
            html_parts.append('<hr/>')
        elif line.strip():
            para.append(line.strip())
        else:
            flush_para()

    flush_para()
    return '\n'.join(html_parts)


def export_epub(project_dir='.'):
    try:
        from ebooklib import epub
    except ImportError:
        print("ERROR: ebooklib not installed. Run: pip install ebooklib")
        sys.exit(1)

    project_dir = Path(project_dir)
    config = load_config(project_dir)
    manuscript_path = find_manuscript(project_dir, config)

    if not manuscript_path:
        print("ERROR: No manuscript found in manuscript/ directory.")
        print("Run /ghost-writer:finish first to assemble the manuscript.")
        sys.exit(1)

    print(f"Reading: {manuscript_path}")

    title = config.get('title', 'Untitled')
    author_name = (
        config.get('author_profile', {}).get('name') or
        config.get('author', {}).get('name') or
        'Author'
    )
    language = config.get('language', 'en')
    premise = config.get('book_profile', {}).get('premise', '')

    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    output_path = project_dir / "manuscript" / f"{slug}-final.epub"

    book = epub.EpubBook()
    book.set_identifier(f'ghost-writer-{slug}')
    book.set_title(title)
    book.set_language(language)
    book.add_author(author_name)
    if premise:
        book.add_metadata('DC', 'description', premise)

    css = epub.EpubItem(
        uid='style',
        file_name='style/main.css',
        media_type='text/css',
        content='''
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em 2em; color: #1a1a1a; }
h1 { font-size: 2em; margin-top: 2em; margin-bottom: 0.5em; border-bottom: 1px solid #ccc; padding-bottom: 0.3em; }
h2 { font-size: 1.5em; margin-top: 1.5em; }
h3 { font-size: 1.1em; color: #555; margin-top: 1.2em; }
p { margin: 0.6em 0; text-align: justify; }
blockquote { margin: 1em 2em; font-style: italic; color: #555; border-left: 3px solid #ccc; padding-left: 1em; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5em auto; width: 40%; }
'''.strip()
    )
    book.add_item(css)

    sections = parse_manuscript(manuscript_path)
    spine = ['nav']
    toc = []
    chapters = []

    for i, section in enumerate(sections):
        body_html = md_to_html(section.get('lines', []))
        level = section['type']
        heading_tag = 'h1' if level == 'h1' else 'h2'
        content = f'''<?xml version='1.0' encoding='utf-8'?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="{language}">
<head>
  <title>{section["title"]}</title>
  <link rel="stylesheet" type="text/css" href="../style/main.css"/>
</head>
<body>
  <{heading_tag}>{section["title"]}</{heading_tag}>
  {body_html}
</body>
</html>'''

        ch = epub.EpubHtml(
            title=section['title'],
            file_name=f'chapter_{i+1:03d}.xhtml',
            lang=language,
            content=content
        )
        ch.add_item(css)
        book.add_item(ch)
        chapters.append(ch)
        spine.append(ch)
        toc.append(epub.Link(f'chapter_{i+1:03d}.xhtml', section['title'], f'ch{i+1}'))

    book.toc = toc
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(str(output_path), book)
    print(f"✅ EPUB exported: {output_path}")
    return output_path


if __name__ == '__main__':
    project_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    export_epub(project_dir)
