#!/usr/bin/env python3
"""
Ghost Writer — PDF Export Script
Converts manuscript/[title]-final.md to a clean, readable PDF.
"""

import json
import re
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate


# ─── Config ───────────────────────────────────────────────────────────────────

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
    # fallback: any md in manuscript/
    manuscripts = list((Path(project_dir) / "manuscript").glob("*.md"))
    if manuscripts:
        return manuscripts[0]
    return None


# ─── Markdown Parser ──────────────────────────────────────────────────────────

def parse_manuscript(md_path):
    """Parse markdown into structured sections."""
    text = md_path.read_text(encoding='utf-8')
    
    # Remove frontmatter
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)
    
    sections = []
    current_section = None
    current_paragraphs = []
    
    for line in text.split('\n'):
        if line.startswith('# ') and not line.startswith('## '):
            if current_section:
                current_section['paragraphs'] = current_paragraphs
                sections.append(current_section)
            current_section = {'type': 'h1', 'title': line[2:].strip(), 'paragraphs': []}
            current_paragraphs = []
        elif line.startswith('## '):
            if current_paragraphs and current_section:
                current_section['paragraphs'] = current_paragraphs
                sections.append(current_section)
            current_section = {'type': 'h2', 'title': line[3:].strip(), 'paragraphs': []}
            current_paragraphs = []
        elif line.startswith('### '):
            current_paragraphs.append(('h3', line[4:].strip()))
        elif line.startswith('> '):
            current_paragraphs.append(('blockquote', line[2:].strip()))
        elif line.strip() == '---':
            current_paragraphs.append(('hr', ''))
        elif line.strip():
            current_paragraphs.append(('p', line.strip()))
        
    if current_section:
        current_section['paragraphs'] = current_paragraphs
        sections.append(current_section)
    
    return sections


def extract_toc(sections):
    """Extract table of contents from sections."""
    toc = []
    for s in sections:
        if s['type'] in ('h1', 'h2'):
            toc.append(s['title'])
    return toc


# ─── Styles ───────────────────────────────────────────────────────────────────

DARK = HexColor('#1a1a2e')
MID = HexColor('#4a4a6a')
LIGHT = HexColor('#f8f8f4')
ACCENT = HexColor('#2d6a4f')

def make_styles():
    base = getSampleStyleSheet()
    
    styles = {
        'cover_title': ParagraphStyle(
            'cover_title',
            fontName='Times-Bold',
            fontSize=36,
            textColor=DARK,
            alignment=TA_CENTER,
            spaceAfter=12,
            leading=44,
        ),
        'cover_subtitle': ParagraphStyle(
            'cover_subtitle',
            fontName='Times-Italic',
            fontSize=16,
            textColor=MID,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        'cover_author': ParagraphStyle(
            'cover_author',
            fontName='Helvetica',
            fontSize=13,
            textColor=MID,
            alignment=TA_CENTER,
            spaceAfter=6,
        ),
        'cover_meta': ParagraphStyle(
            'cover_meta',
            fontName='Helvetica',
            fontSize=9,
            textColor=HexColor('#999999'),
            alignment=TA_CENTER,
        ),
        'toc_title': ParagraphStyle(
            'toc_title',
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=DARK,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=20,
        ),
        'toc_entry': ParagraphStyle(
            'toc_entry',
            fontName='Helvetica',
            fontSize=11,
            textColor=MID,
            alignment=TA_LEFT,
            spaceAfter=8,
            leftIndent=0,
        ),
        'chapter_title': ParagraphStyle(
            'chapter_title',
            fontName='Times-Bold',
            fontSize=24,
            textColor=DARK,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=30,
            leading=30,
        ),
        'h2': ParagraphStyle(
            'h2',
            fontName='Times-Bold',
            fontSize=16,
            textColor=DARK,
            alignment=TA_LEFT,
            spaceBefore=24,
            spaceAfter=12,
        ),
        'h3': ParagraphStyle(
            'h3',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=MID,
            alignment=TA_LEFT,
            spaceBefore=16,
            spaceAfter=8,
        ),
        'body': ParagraphStyle(
            'body',
            fontName='Times-Roman',
            fontSize=11,
            textColor=HexColor('#2a2a2a'),
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=18,
            firstLineIndent=0,
        ),
        'blockquote': ParagraphStyle(
            'blockquote',
            fontName='Times-Italic',
            fontSize=11,
            textColor=MID,
            alignment=TA_LEFT,
            spaceAfter=10,
            leading=17,
            leftIndent=30,
            rightIndent=30,
        ),
    }
    return styles


# ─── Page Templates ───────────────────────────────────────────────────────────

class BookDocument(BaseDocTemplate):
    def __init__(self, filename, title, author, **kwargs):
        self.book_title = title
        self.book_author = author
        super().__init__(filename, **kwargs)
        
        margin = 2.5 * cm
        frame = Frame(
            margin, margin,
            A4[0] - 2 * margin,
            A4[1] - 2 * margin,
            id='normal'
        )
        template = PageTemplate(
            id='main',
            frames=[frame],
            onPage=self.add_footer
        )
        self.addPageTemplates([template])
    
    def add_footer(self, canvas, doc):
        if doc.page <= 2:  # No footer on cover and TOC
            return
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#999999'))
        # Left: book title
        canvas.drawString(2.5 * cm, 1.5 * cm, self.book_title)
        # Right: page number
        canvas.drawRightString(A4[0] - 2.5 * cm, 1.5 * cm, str(doc.page - 2))
        # Line
        canvas.setStrokeColor(HexColor('#dddddd'))
        canvas.line(2.5 * cm, 1.8 * cm, A4[0] - 2.5 * cm, 1.8 * cm)
        canvas.restoreState()


# ─── Content Builders ─────────────────────────────────────────────────────────

def build_cover(config, styles):
    story = []
    story.append(Spacer(1, 6 * cm))
    
    title = config.get('title', 'Untitled')
    story.append(Paragraph(title, styles['cover_title']))
    story.append(Spacer(1, 0.5 * cm))
    
    # Subtitle from book_profile if present
    premise = config.get('book_profile', {}).get('premise', '')
    if premise:
        story.append(Paragraph(premise, styles['cover_subtitle']))
        story.append(Spacer(1, 1 * cm))
    
    story.append(HRFlowable(
        width='40%', thickness=1,
        color=HexColor('#cccccc'),
        hAlign='CENTER', spaceAfter=20
    ))
    story.append(Spacer(1, 1 * cm))
    
    # Author
    author_name = (
        config.get('author_profile', {}).get('name') or
        config.get('author', {}).get('name') or
        'Author'
    )
    story.append(Paragraph(author_name, styles['cover_author']))
    story.append(Spacer(1, 4 * cm))
    
    # Meta
    version = config.get('version', '1.0')
    from datetime import date
    today = date.today().strftime('%B %Y')
    story.append(Paragraph(f"First draft — {today} — v{version}", styles['cover_meta']))
    
    story.append(PageBreak())
    return story


def build_toc(toc_entries, styles):
    story = []
    story.append(Spacer(1, 2 * cm))
    story.append(Paragraph("Contents", styles['toc_title']))
    story.append(HRFlowable(
        width='100%', thickness=0.5,
        color=HexColor('#eeeeee'),
        spaceAfter=16
    ))
    
    for i, entry in enumerate(toc_entries):
        # Clean entry title
        clean = re.sub(r'^(Chapter \d+|Introduction|Conclusion)\s*[—–-]\s*', '', entry)
        if not clean:
            clean = entry
        story.append(Paragraph(f"{clean}", styles['toc_entry']))
    
    story.append(PageBreak())
    return story


def inline_markdown(text):
    """Convert inline markdown to ReportLab XML."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'_(.+?)_', r'<i>\1</i>', text)
    # Escape ampersands not already escaped
    text = re.sub(r'&(?!amp;|lt;|gt;|quot;|#)', '&amp;', text)
    return text


def build_chapters(sections, styles):
    story = []
    
    for section in sections:
        if section['type'] == 'h1':
            story.append(Spacer(1, 1.5 * cm))
            story.append(Paragraph(
                inline_markdown(section['title']),
                styles['chapter_title']
            ))
            story.append(HRFlowable(
                width='60%', thickness=1,
                color=HexColor('#dddddd'),
                spaceAfter=20
            ))
            
        elif section['type'] == 'h2':
            story.append(PageBreak())
            story.append(Spacer(1, 1 * cm))
            story.append(Paragraph(
                inline_markdown(section['title']),
                styles['chapter_title']
            ))
            story.append(HRFlowable(
                width='60%', thickness=1,
                color=HexColor('#dddddd'),
                spaceAfter=20
            ))
        
        for para_type, para_text in section.get('paragraphs', []):
            if not para_text and para_type == 'p':
                continue
            text = inline_markdown(para_text)
            
            if para_type == 'p':
                story.append(Paragraph(text, styles['body']))
            elif para_type == 'h3':
                story.append(Paragraph(text, styles['h3']))
            elif para_type == 'blockquote':
                story.append(Paragraph(text, styles['blockquote']))
            elif para_type == 'hr':
                story.append(Spacer(1, 0.3 * cm))
                story.append(HRFlowable(
                    width='30%', thickness=0.5,
                    color=HexColor('#cccccc'),
                    hAlign='CENTER', spaceAfter=10
                ))
    
    return story


# ─── Main ─────────────────────────────────────────────────────────────────────

def export_pdf(project_dir='.'):
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
    
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    output_path = project_dir / "manuscript" / f"{slug}-final.pdf"
    
    styles = make_styles()
    sections = parse_manuscript(manuscript_path)
    toc = extract_toc(sections)
    
    doc = BookDocument(
        str(output_path),
        title=title,
        author=author_name,
        pagesize=A4,
        topMargin=2.5*cm,
        bottomMargin=2.5*cm,
        leftMargin=2.5*cm,
        rightMargin=2.5*cm,
    )
    
    story = []
    story += build_cover(config, styles)
    story += build_toc(toc, styles)
    story += build_chapters(sections, styles)
    
    doc.build(story)
    print(f"✅ PDF exported: {output_path}")
    return output_path


if __name__ == '__main__':
    project_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    export_pdf(project_dir)
