#!/usr/bin/env python3
"""Convert nature-proposal-writer proposal markdown to properly formatted .docx.

Usage: python3 scripts/build_proposal_docx.py <input.md> [output.docx]

Formatting standard for academic proposals:
- Title: centered, Times New Roman + 宋体, 18pt bold
- Headings: Times New Roman + 宋体, 16/14/12pt bold, black
- Body: Times New Roman + 宋体, 12pt, 1.5 line spacing, NO first-line indent
- Margins: 1 inch all sides
- Tables: 10pt, Table Grid style
"""
import re
import sys
from pathlib import Path
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from math_to_omml import latex_to_omml

inpath = Path(sys.argv[1])
outpath = Path(sys.argv[2]) if len(sys.argv) > 2 else inpath.with_suffix('.docx')
if inpath.resolve() == outpath.resolve() or (outpath.exists() and inpath.samefile(outpath)):
    raise SystemExit('Output must not overwrite the source Markdown file')

doc = Document()

# Page setup
for section in doc.sections:
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Normal style
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
pf = style.paragraph_format
pf.line_spacing = 1.5
pf.space_before = Pt(0)
pf.space_after = Pt(0)
pf.first_line_indent = Cm(0)

# Heading styles
for level, size in [(1, 16), (2, 14), (3, 12)]:
    hs = doc.styles[f'Heading {level}']
    hs.font.name = 'Times New Roman'
    hs.font.size = Pt(size)
    hs.font.bold = True
    hs.font.color.rgb = RGBColor(0, 0, 0)
    hs.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    hs.paragraph_format.line_spacing = 1.5
    hs.paragraph_format.space_before = Pt(18 if level == 1 else 12 if level == 2 else 6)
    hs.paragraph_format.space_after = Pt(12 if level == 1 else 6 if level == 2 else 3)


INLINE = re.compile(
    r'!\[([^\]]*)\]\((<[^>]+>|(?:[^()]|\([^()]*\))+)\)'
    r'|\*\*(.+?)\*\*'
    r'|(?<![\\$])\$(?!\$)((?:\\.|[^$])+?)(?<!\\)\$'
    r'|\\\((.+?)\\\)'
)


def add_content(paragraph, text, *, bold=False, size=None, italic=False, color=None):
    def plain(value):
        if not value:
            return
        run = paragraph.add_run(value)
        if bold:
            run.bold = True
        if italic:
            run.italic = True
        if size:
            run.font.size = Pt(size)
        if color:
            run.font.color.rgb = color

    offset = 0
    for match in INLINE.finditer(text):
        plain(text[offset:match.start()])
        alt, image_path, strong, math_dollars, math_parentheses = match.groups()
        if image_path is not None:
            path = inpath.parent / image_path.strip('<>')
            if not path.is_file():
                raise SystemExit(f'Missing local image: {path}')
            image = paragraph.add_run().add_picture(str(path))
            image._inline.docPr.set('descr', alt)
            scale = min(1, Inches(6.2) / image.width, Inches(8.3) / image.height)
            image.width, image.height = int(image.width * scale), int(image.height * scale)
        elif strong is not None:
            add_content(paragraph, strong, bold=True, size=size, italic=italic, color=color)
        else:
            equation = latex_to_omml(math_dollars or math_parentheses)
            paragraph._p.append(equation[0])
        offset = match.end()
    plain(text[offset:])


def bp(text, **style):
    paragraph = doc.add_paragraph()
    add_content(paragraph, text, **style)
    return paragraph


def list_item(text):
    paragraph = doc.add_paragraph()
    paragraph.paragraph_format.left_indent = Cm(1)
    add_content(paragraph, text, size=11)


def split_cells(line):
    contents = line.strip().removeprefix('|')
    if contents.endswith('|') and not contents.endswith(r'\|'):
        contents = contents[:-1]
    return [cell.strip().replace(r'\|', '|') for cell in re.split(r'(?<!\\)\|', contents)]


def table(headers, rows):
    t = doc.add_table(rows=1 + len(rows), cols=len(headers))
    t.style = 'Table Grid'
    for index, values in enumerate([headers, *rows]):
        if len(values) > len(headers):
            raise SystemExit(f'Table row {index + 1} has more cells than its header; escape literal pipes.')
        for cell, value in zip(t.rows[index].cells, values):
            add_content(cell.paragraphs[0], value, size=10, bold=(index == 0))
    doc.add_paragraph()


def is_table_separator(line):
    return all(re.fullmatch(r':?-{3,}:?', cell) for cell in split_cells(line))


# Parse markdown
with open(inpath, encoding='utf-8') as f:
    lines = f.readlines()

i = 0
in_code = False
code_buf = []
first_title = True

while i < len(lines):
    line = lines[i].rstrip('\n')

    if not line.strip():
        i += 1
        continue

    if line.strip().startswith('```'):
        if in_code:
            txt = '\n'.join(code_buf)
            p = doc.add_paragraph(style='Normal')
            p.paragraph_format.left_indent = Cm(1.0)
            run = p.add_run(txt)
            run.font.name = 'Consolas'
            run.font.size = Pt(9)
            code_buf = []
            in_code = False
        else:
            in_code = True
        i += 1
        continue

    if in_code:
        code_buf.append(line)
        i += 1
        continue

    stripped = line.strip()
    if stripped.startswith(('$$', r'\[')):
        closing = '$$' if stripped.startswith('$$') else r'\]'
        equation = stripped[2:]
        while not equation.rstrip().endswith(closing):
            i += 1
            if i == len(lines):
                raise SystemExit('Unclosed display equation')
            equation += '\n' + lines[i].rstrip()
        paragraph = doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph._p.append(latex_to_omml(equation.rstrip()[:-2].strip()))
        i += 1
        continue

    if first_title and line.startswith('# ') and not line.startswith('## '):
        title_text = line[2:].strip()
        p = doc.add_paragraph(style='Normal')
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_content(p, title_text, bold=True, size=18)
        first_title = False
        i += 1
        continue

    if line.startswith('# ') and not line.startswith('## '):
        add_content(doc.add_heading(level=1), line[2:].strip())
        i += 1
        continue

    if line.startswith('## ') and not line.startswith('### '):
        add_content(doc.add_heading(level=2), line[3:].strip())
        i += 1
        continue

    if line.startswith('### ') and not line.startswith('#### '):
        add_content(doc.add_heading(level=3), line[4:].strip())
        i += 1
        continue

    if line.startswith('#### '):
        p = doc.add_paragraph(style='Normal')
        add_content(p, line[5:].strip(), bold=True, size=12)
        i += 1
        continue

    if line.strip() == '---':
        doc.add_paragraph()
        i += 1
        continue

    if line.strip().startswith('|') and not is_table_separator(line):
        tbl_lines = [line]
        j = i + 1
        has_separator = j < len(lines) and is_table_separator(lines[j])
        if has_separator:
            j += 1
        while j < len(lines) and lines[j].strip().startswith('|'):
            tbl_lines.append(lines[j].rstrip('\n'))
            j += 1
        if len(tbl_lines) >= 2 or has_separator:
            headers = split_cells(tbl_lines[0])
            rows = [split_cells(row) for row in tbl_lines[1:]]
            table(headers, rows)
        i = j
        continue

    if line.strip().startswith('- '):
        list_item("• " + line.strip()[2:])
        i += 1
        continue

    if re.match(r'^\d+\.', line.strip()):
        list_item(line.strip())
        i += 1
        continue

    if line.startswith('>'):
        bp(line[1:].strip(), italic=True, size=10, color=RGBColor(80, 80, 80))
        i += 1
        continue

    bp(line.strip())
    i += 1

doc.save(outpath)
print(f"OK → {outpath}")
