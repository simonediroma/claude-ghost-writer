#!/usr/bin/env python3
"""
Ghost Writer — Review PDF

Two commands:

  python3 review_pdf.py export [chapter files...]
      Builds manuscript/review-[date].pdf from chapters/: every paragraph gets
      an ID in the margin (e.g. 3.12 = chapter 3, paragraph 12), wide margins
      and extra line spacing for annotating on a tablet or on paper.
      Also writes manuscript/review-map.json (ID -> file + paragraph text).

  python3 review_pdf.py import <annotated.pdf>
      Reads highlights, strike-outs, underlines, sticky notes and free-text
      comments from the annotated PDF and appends them to corrections.md,
      each with its paragraph ID, the highlighted text and the comment.

Requires: reportlab (export), pymupdf (import).
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

PROJECT = Path('.')
CHAPTERS_DIR = PROJECT / 'chapters'
OUT_DIR = PROJECT / 'manuscript'
MAP_PATH = OUT_DIR / 'review-map.json'
CORRECTIONS_PATH = PROJECT / 'corrections.md'
ID_RE = re.compile(r'^\d{1,3}\.\d{1,4}$')


# ─── Chapter parsing ──────────────────────────────────────────────────────────

def chapter_number(path, index):
    m = re.match(r'(\d+)', path.stem)
    return int(m.group(1)) if m else index


def parse_chapter(path):
    """Return (title, [paragraph blocks]) — body text only, no frontmatter or logs."""
    text = path.read_text(encoding='utf-8')
    title = path.stem
    fm = re.match(r'^---\n(.*?)\n---\n', text, flags=re.DOTALL)
    if fm:
        t = re.search(r'^title:\s*(.+)$', fm.group(1), flags=re.MULTILINE)
        if t:
            title = t.group(1).strip().strip('"\'')
        text = text[fm.end():]
    # Stop at the Demolition Log (and any other trailing log section)
    text = re.split(r'^## (Demolition Log|Revision Log)', text, flags=re.MULTILINE)[0]

    blocks = []
    for raw in re.split(r'\n\s*\n', text):
        block = raw.strip()
        if not block or block == '---':
            continue
        if block.startswith('# '):
            title = block[2:].strip()
            continue
        if block.startswith('#'):
            blocks.append(('h', block.lstrip('#').strip()))
            continue
        kind = 'quote' if block.startswith('>') else 'p'
        block = re.sub(r'^>\s?', '', block, flags=re.MULTILINE) if kind == 'quote' else block
        blocks.append((kind, ' '.join(line.strip() for line in block.splitlines())))
    return title, blocks


def collect(files):
    if not files:
        files = sorted(p for p in CHAPTERS_DIR.glob('*.md') if not p.stem.startswith('example'))
    chapters = []
    for i, path in enumerate(files, start=1):
        path = Path(path)
        title, blocks = parse_chapter(path)
        chapters.append({'n': chapter_number(path, i), 'file': str(path), 'title': title, 'blocks': blocks})
    return chapters


# ─── Export ───────────────────────────────────────────────────────────────────

def inline_markdown(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<i>\1</i>', text)
    return text


def export(files):
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    config = {}
    if (PROJECT / 'book.config.json').exists():
        config = json.loads((PROJECT / 'book.config.json').read_text(encoding='utf-8'))
    book_title = config.get('title', 'Manuscript')

    chapters = collect(files)
    if not chapters:
        sys.exit('ERROR: no chapter files found in chapters/.')

    OUT_DIR.mkdir(exist_ok=True)
    out = OUT_DIR / f'review-{date.today().isoformat()}.pdf'

    body = ParagraphStyle('body', fontName='Times-Roman', fontSize=12, leading=21, alignment=TA_JUSTIFY)
    quote = ParagraphStyle('quote', parent=body, fontName='Times-Italic', leftIndent=0.8 * cm)
    head = ParagraphStyle('head', fontName='Helvetica-Bold', fontSize=12, leading=18, alignment=TA_LEFT)
    title_style = ParagraphStyle('title', fontName='Times-Bold', fontSize=20, leading=26, spaceAfter=18)
    pid = ParagraphStyle('pid', fontName='Helvetica-Bold', fontSize=8, leading=21, textColor=HexColor('#888888'))

    id_col, text_col = 1.4 * cm, 13.0 * cm
    story, mapping = [], {}

    for ch in chapters:
        story.append(Paragraph(f"{ch['n']} — {inline_markdown(ch['title'])}", title_style))
        n = 0
        for kind, text in ch['blocks']:
            if kind == 'h':
                story.append(Paragraph(inline_markdown(text), head))
                story.append(Spacer(1, 6))
                continue
            n += 1
            ref = f"{ch['n']}.{n}"
            mapping[ref] = {'file': ch['file'], 'paragraph': n, 'text': text}
            row = Table([[Paragraph(ref, pid), Paragraph(inline_markdown(text), quote if kind == 'quote' else body)]],
                        colWidths=[id_col, text_col])
            row.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(row)
        story.append(PageBreak())

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.setFillColor(HexColor('#999999'))
        canvas.drawString(2 * cm, 1.2 * cm, f'{book_title} — review copy {date.today().isoformat()}')
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(doc.page))
        canvas.restoreState()

    # Wide right margin left free for handwritten / stylus notes
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=1.8 * cm, rightMargin=A4[0] - 1.8 * cm - id_col - text_col,
                            topMargin=2 * cm, bottomMargin=2.2 * cm, title=f'{book_title} — review')
    doc.build(story, onFirstPage=footer, onLaterPages=footer)

    MAP_PATH.write_text(json.dumps({'pdf': str(out), 'created': date.today().isoformat(), 'paragraphs': mapping},
                                   ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'Review PDF: {out}')
    print(f'Paragraph map: {MAP_PATH} ({len(mapping)} paragraphs)')


# ─── Import ───────────────────────────────────────────────────────────────────

ANNOT_KINDS = {
    'Highlight': 'highlight', 'Underline': 'underline', 'StrikeOut': 'strike',
    'Squiggly': 'underline', 'Text': 'note', 'FreeText': 'note', 'Ink': 'drawing', 'Caret': 'insert',
}


def paragraph_ids(page):
    """Margin IDs on a page as [(y_top, id)], sorted top-down."""
    ids = []
    for x0, y0, x1, y1, word, *_ in page.get_text('words'):
        if x0 < 3.3 * 28.35 and ID_RE.match(word):
            ids.append((y0, word))
    return sorted(ids)


def import_annotations(pdf_path):
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    mapping = {}
    if MAP_PATH.exists():
        mapping = json.loads(MAP_PATH.read_text(encoding='utf-8')).get('paragraphs', {})

    doc = fitz.open(pdf_path)
    items, last_id = [], None
    for page in doc:
        ids = paragraph_ids(page)
        annots = sorted(page.annots() or [], key=lambda a: (a.rect.y0, a.rect.x0))
        for a in annots:
            kind = ANNOT_KINDS.get(a.type[1])
            if not kind:
                continue
            above = [ref for y, ref in ids if y <= a.rect.y0 + 2]
            ref = above[-1] if above else last_id
            quoted = ''
            if kind in ('highlight', 'underline', 'strike'):
                vs = a.vertices or []
                parts = []
                for i in range(0, len(vs) - 3, 4):
                    quad = fitz.Quad(vs[i:i + 4])
                    parts.append(page.get_textbox(quad.rect).strip())
                quoted = ' '.join(p for p in parts if p) or page.get_textbox(a.rect).strip()
            comment = (a.info.get('content') or '').strip()
            if kind == 'drawing' and not comment:
                comment = '(handwritten mark — check the page)'
            items.append({'id': ref or '?', 'page': page.number + 1, 'kind': kind,
                          'quote': re.sub(r'\s+', ' ', quoted), 'comment': comment})
        if ids:
            last_id = ids[-1][1]

    if not items:
        print('No annotations found.')
        return

    if not CORRECTIONS_PATH.exists():
        CORRECTIONS_PATH.write_text('# Corrections\n', encoding='utf-8')
    existing = CORRECTIONS_PATH.read_text(encoding='utf-8')
    start = len(re.findall(r'^\| N\d+ \|', existing, flags=re.MULTILINE)) + 1

    lines = [f'\n## Import {date.today().isoformat()} — {Path(pdf_path).name}\n',
             '| # | Where | Page | Type | Text | Note | Status |', '|---|---|---|---|---|---|---|']
    for i, it in enumerate(items, start=start):
        where = it['id']
        if where in mapping:
            where = f"{where} ({Path(mapping[where]['file']).name})"
        cell = lambda s: s.replace('|', '\\|').replace('\n', ' ')
        lines.append(f"| N{i} | {where} | {it['page']} | {it['kind']} | {cell(it['quote'])} | {cell(it['comment'])} | open |")
    CORRECTIONS_PATH.write_text(existing.rstrip('\n') + '\n' + '\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{len(items)} annotations added to {CORRECTIONS_PATH}')


# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] not in ('export', 'import'):
        sys.exit(__doc__)
    if sys.argv[1] == 'export':
        export(sys.argv[2:])
    else:
        if len(sys.argv) < 3:
            sys.exit('Usage: python3 review_pdf.py import <annotated.pdf>')
        import_annotations(sys.argv[2])
