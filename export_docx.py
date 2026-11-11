#!/usr/bin/env python3
"""
Ghost Writer — DOCX Export Script
Converts manuscript/[title]-final.md to a standard manuscript DOCX.
Requires: python-docx (pip install python-docx)
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


def apply_inline_markdown(paragraph, text):
    """Apply bold/italic from markdown to a docx paragraph."""
    from docx.oxml.ns import qn
    import docx

    parts = re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*|_[^_]+_)', text)
    for part in parts:
        if re.match(r'\*\*(.+)\*\*', part):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif re.match(r'\*(.+)\*', part) or re.match(r'_(.+)_', part):
            run = paragraph.add_run(part[1:-1])
            run.italic = True
        else:
            paragraph.add_run(part)


def export_docx(project_dir='.'):
    try:
        import docx
        from docx import Document
        from docx.shared import Pt, Inches, Cm
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.style import WD_STYLE_TYPE
    except ImportError:
        print("ERROR: python-docx not installed. Run: pip install python-docx")
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
    subtitle = config.get('subtitle', '')
    author_name = (
        config.get('author_profile', {}).get('name') or
        config.get('author', {}).get('name') or
        'Author'
    )
    today = date.today().strftime('%B %Y')

    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    output_path = project_dir / "manuscript" / f"{slug}-final.docx"

    doc = Document()

    # Page setup: standard manuscript (1-inch margins)
    section = doc.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    # Default body style: 12pt Times New Roman, double-spaced
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    from docx.shared import Pt as _Pt
    from docx.oxml.ns import qn
    import lxml.etree as etree
    normal_style.paragraph_format.line_spacing = Pt(24)  # double spacing

    # Cover page
    cover_title = doc.add_paragraph()
    cover_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover_title.add_run(title)
    run.bold = True
    run.font.size = Pt(24)
    run.font.name = 'Times New Roman'

    if subtitle:
        cover_sub = doc.add_paragraph()
        cover_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cover_sub.add_run(subtitle)
        run.italic = True
        run.font.size = Pt(14)
        run.font.name = 'Times New Roman'

    doc.add_paragraph()

    cover_author = doc.add_paragraph()
    cover_author.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover_author.add_run(author_name)
    run.font.size = Pt(13)
    run.font.name = 'Times New Roman'

    cover_date = doc.add_paragraph()
    cover_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cover_date.add_run(f'First draft — {today}')
    run.font.size = Pt(10)
    run.font.name = 'Times New Roman'
    run.font.color.rgb = docx.shared.RGBColor(0x99, 0x99, 0x99)

    doc.add_page_break()

    # Parse and add content
    text = manuscript_path.read_text(encoding='utf-8')
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    for line in text.split('\n'):
        if line.startswith('# ') and not line.startswith('## '):
            doc.add_page_break()
            p = doc.add_heading(line[2:].strip(), level=1)
            p.style.font.name = 'Times New Roman'
        elif line.startswith('## '):
            p = doc.add_heading(line[3:].strip(), level=2)
            p.style.font.name = 'Times New Roman'
        elif line.startswith('### '):
            p = doc.add_heading(line[4:].strip(), level=3)
            p.style.font.name = 'Times New Roman'
        elif line.startswith('> '):
            p = doc.add_paragraph(style='Quote' if 'Quote' in [s.name for s in doc.styles] else 'Normal')
            apply_inline_markdown(p, line[2:].strip())
            p.paragraph_format.left_indent = Cm(1.5)
            p.paragraph_format.right_indent = Cm(1.5)
        elif line.strip() == '---':
            p = doc.add_paragraph('* * *')
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif line.strip():
            p = doc.add_paragraph()
            apply_inline_markdown(p, line.strip())
            p.paragraph_format.line_spacing = Pt(24)

    doc.save(str(output_path))
    print(f"✅ DOCX exported: {output_path}")
    return output_path


if __name__ == '__main__':
    project_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    export_docx(project_dir)
