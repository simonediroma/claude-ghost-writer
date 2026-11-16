#!/usr/bin/env python3
"""
RAMA — Review PDF  (adapted from ghost-writer's review_pdf.py, MIT, Simone Di Roma)

Two commands:

  python3 review_pdf.py export <Title>.md [--chapters 5-7] [--out DIR]
      Builds DIR/review-[date].pdf (default DIR: review/ next to the
      manuscript). Every paragraph gets an ID in the margin (5.12 = chapter 5,
      paragraph 12), with wide margins and extra line spacing for annotating.
      Also writes DIR/review-map.json (ID -> chapter + paragraph text).
      Chapters are the manuscript's level-2 (##) headings, numbered in order.
      Paragraph numbers skip headings and scene-break lines. Text under a
      Part heading, before its first chapter, is numbered P1.1, P1.2, …

  python3 review_pdf.py import <annotated.pdf> --corrections "<Title> — Corrections.md" [--map review/review-map.json]
      Reads highlights, strike-outs, underlines, sticky notes and free-text
      comments from the annotated PDF and appends them to the corrections
      file, each with its paragraph ID, the highlighted text and the comment.

Requires: reportlab (export), pymupdf (import).
"""

import json
import re
import sys
from datetime import date
from pathlib import Path

OUT_DIR = Path('review')
MAP_PATH = OUT_DIR / 'review-map.json'
CORRECTIONS_PATH = Path('Corrections.md')
DIVIDER_RE = re.compile(r'^[\s*#~•·◆◇◐◑○●✦✧❧☙⁂—\-]+$')
CHAPTER_RE = re.compile(r'^##(?!#)\s+(.+?)\s*#*\s*$')
ID_RE = re.compile(r'^P?\d{1,3}\.\d{1,4}$')


# ─── Manuscript parsing ───────────────────────────────────────────────────────

def blocks_of(text):
    """Paragraph blocks of one chapter body. Headings become ('h', …); scene breaks are skipped."""
    blocks = []
    for raw in re.split(r'\n\s*\n', text):
        block = raw.strip()
        if not block or DIVIDER_RE.match(block):
            continue
        if block.startswith('#'):
            blocks.append(('h', block.lstrip('#').strip().rstrip('#').strip()))
            continue
        kind = 'quote' if block.startswith('>') else 'p'
        block = re.sub(r'^>\s?', '', block, flags=re.MULTILINE) if kind == 'quote' else block
        blocks.append((kind, ' '.join(line.strip() for line in block.splitlines())))
    return blocks


def split_manuscript(path):
    """[(n, heading, body_text)] in order. Chapters (## headings) are numbered 1, 2, 3…;
    text under a Part heading (# …) before its first chapter is its own unit, numbered P1, P2…"""
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    units, current, body, chapter_n, part_n = [], None, [], 0, 0

    def close():
        if current and (current[0].isdigit() or any(l.strip() for l in body)):
            units.append((current[0], current[1], '\n'.join(body)))

    for line in lines:
        m = CHAPTER_RE.match(line)
        if m:
            close()
            chapter_n += 1
            current, body = (str(chapter_n), m.group(1)), []
            continue
        if line.startswith('# '):
            close()
            part_n += 1
            current, body = (f'P{part_n}', line[2:].strip()), []
            continue
        if current:
            body.append(line)
    close()
    return units


def parse_range(spec, total):
    if not spec or spec == 'all':
        return set(range(1, total + 1))
    wanted = set()
    for part in spec.split(','):
        a, _, b = part.partition('-')
        wanted.update(range(int(a), int(b or a) + 1))
    return wanted


def collect(manuscript, spec=None):
    chapters = split_manuscript(manuscript)
    total = sum(1 for n, _, _ in chapters if n.isdigit())
    wanted = parse_range(spec, total)
    keep, next_part = [], None
    for n, title, text in chapters:
        if not n.isdigit():
            next_part = (n, title, text)  # include a Part opening only if its first chapter is wanted
            continue
        if int(n) in wanted:
            if next_part:
                keep.append(next_part)
            keep.append((n, title, text))
        next_part = None
    return [{'n': n, 'file': str(manuscript), 'title': title, 'blocks': blocks_of(text)}
            for n, title, text in keep]


def inline_markdown(text):
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<i>\1</i>', text)
    return text


def export(manuscript, spec=None):
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    book_title = Path(manuscript).stem
    head_meta = re.search(r'^Title:\s*(.+)$', Path(manuscript).read_text(encoding='utf-8')[:2000], flags=re.MULTILINE)
    if head_meta:
        book_title = head_meta.group(1).strip()

    chapters = collect(manuscript, spec)
    if not chapters:
        sys.exit('ERROR: no chapters (## headings) found in the manuscript.')

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
            mapping[ref] = {'chapter': ch['n'], 'heading': ch['title'], 'paragraph': n, 'text': text}
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
        CORRECTIONS_PATH.write_text(f'# {CORRECTIONS_PATH.stem}\n', encoding='utf-8')
    existing = CORRECTIONS_PATH.read_text(encoding='utf-8')
    start = len(re.findall(r'^\| N\d+ \|', existing, flags=re.MULTILINE)) + 1

    lines = [f'\n## Import {date.today().isoformat()} — {Path(pdf_path).name}\n',
             '| # | Where | Page | Type | Text | Note | Status |', '|---|---|---|---|---|---|---|']
    for i, it in enumerate(items, start=start):
        where = it['id']
        if where in mapping:
            where = f"{where} ({mapping[where]['heading']})"
        cell = lambda s: s.replace('|', '\\|').replace('\n', ' ')
        lines.append(f"| N{i} | {where} | {it['page']} | {it['kind']} | {cell(it['quote'])} | {cell(it['comment'])} | open |")
    CORRECTIONS_PATH.write_text(existing.rstrip('\n') + '\n' + '\n'.join(lines) + '\n', encoding='utf-8')
    print(f'{len(items)} annotations added to {CORRECTIONS_PATH}')


# ─── Main ─────────────────────────────────────────────────────────────────────

def option(args, name, default=None):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


if __name__ == '__main__':
    args = sys.argv[1:]
    if not args or args[0] not in ('export', 'import') or len(args) < 2:
        sys.exit(__doc__)
    command = args.pop(0)
    out = option(args, '--out')
    spec = option(args, '--chapters')
    corrections = option(args, '--corrections')
    map_path = option(args, '--map')
    if command == 'export':
        OUT_DIR = Path(out) if out else Path(args[0]).resolve().parent / 'review'
        MAP_PATH = OUT_DIR / 'review-map.json'
        export(args[0], spec)
    else:
        if corrections:
            CORRECTIONS_PATH = Path(corrections)
        if map_path:
            MAP_PATH = Path(map_path)
        import_annotations(args[0])
