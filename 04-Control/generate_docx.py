# -*- coding: utf-8 -*-
"""
Build Website Performance Specialist Technical Proposal & Framework (DOCX)
in the official executive format (Royal Blue / Coral brand, Navy #003366 theme,
Arial body, styled tables, callout boxes, branded header, metadata card, and page numbering).

Source : Website_Performance_Specialist_Proposal.md
Output : Website_Performance_Specialist_Technical_Proposal_and_Framework.docx
"""

import os
import re

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

NAVY = RGBColor(0x00, 0x33, 0x66)
ROYAL_BLUE = RGBColor(0x27, 0x40, 0x8B)
CORAL = RGBColor(0xDE, 0x5B, 0x3E)
DARK = RGBColor(0x22, 0x22, 0x22)
INK = RGBColor(0x11, 0x18, 0x27)
CODE_INK = RGBColor(0x0F, 0x17, 0x2A)
MUTED_SLATE = RGBColor(100, 116, 139)

XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"

BRAND_MAIN = "Website Performance"
BRAND_ACCENT = "Specialist"
BRAND_SUB = "Technical Proposal & Framework"
SUBTITLE = "Core Web Vitals Audit · Propertism.in Case Study · Zero-Regression Protocol"

META_CARD = [
    "**Role / Mandate:** Senior Website Performance Specialist · 6–8 Week Milestone Sprint",
    "**Engagement Scope:** Speed Audit, Core Web Vitals Optimization & Architecture Overhaul",
    "**Technical Authority:** Viji Munuswamy (Enterprise Systems & Performance Architect)",
    "**Reference Case Study:** Propertism.in (Enterprise Real Estate & Lead Generation Platform)",
    "**Core Methodology:** 3-Pillar Audit Framework · 4-Step Zero-Regression Safety Gate",
]


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'))

_INLINE_RE = re.compile(r'(\*\*.+?\*\*|`[^`]+?`|\*[^*\s][^*]*?\*)')

def add_inline(p, text, size=9.5, base_color=DARK, bold_color=NAVY):
    for part in re.split(_INLINE_RE, text):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**') and len(part) > 4:
            r = p.add_run(part[2:-2])
            r.bold = True
            r.font.name = 'Arial'
            r.font.size = Pt(size)
            r.font.color.rgb = bold_color
        elif part.startswith('`') and part.endswith('`') and len(part) > 2:
            r = p.add_run(part[1:-1])
            r.font.name = 'Consolas'
            r.font.size = Pt(size - 0.5)
            r.font.color.rgb = NAVY
        elif part.startswith('*') and part.endswith('*') and len(part) > 2:
            r = p.add_run(part[1:-1])
            r.italic = True
            r.font.name = 'Arial'
            r.font.size = Pt(size)
            r.font.color.rgb = base_color
        else:
            r = p.add_run(part)
            r.font.name = 'Arial'
            r.font.size = Pt(size)
            r.font.color.rgb = base_color

def add_custom_heading(doc, text, level):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.bold = True
    run.font.color.rgb = NAVY
    if level == 1:
        run.font.size = Pt(14)
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p._p.get_or_add_pPr().append(parse_xml(
            f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="2" w:color="003366"/></w:pBdr>'))
    elif level == 2:
        run.font.size = Pt(11.5)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p._p.get_or_add_pPr().append(parse_xml(
            f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="003366"/></w:pBdr>'))
    else:
        run.font.size = Pt(10)
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
    return p

def add_code_block(doc, code_lines):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=60, bottom=60, left=140, right=120)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        r'<w:left w:val="single" w:sz="18" w:space="0" w:color="003366"/>'
        r'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        r'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        r'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        r'</w:tcBorders>'))
    while code_lines and code_lines[-1].strip() == "":
        code_lines.pop()
    for idx, cl in enumerate(code_lines):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(cl if cl != "" else " ")
        run.font.name = 'Consolas'
        run.font.size = Pt(8.5)
        run.font.color.rgb = CODE_INK
        for t in run._r.findall(qn('w:t')):
            t.set(XML_SPACE, 'preserve')
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_callout_box(doc, text_lines):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Inches(7.0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=100, bottom=100, left=180, right=140)
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        r'<w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>'
        r'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
        r'</w:tcBorders>'))
    for idx, t_line in enumerate(text_lines):
        p = cell.paragraphs[0] if idx == 0 else cell.add_paragraph()
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.15
        add_inline(p, t_line, size=9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def add_styled_table(doc, header_cells, row_cells_list):
    cols = len(header_cells)
    tbl = doc.add_table(rows=len(row_cells_list) + 1, cols=cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = True
    
    # Header row formatting
    hdr = tbl.rows[0]
    hdr_trPr = hdr._tr.get_or_add_trPr()
    hdr_trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    hdr_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
    
    for c, text in enumerate(header_cells):
        cell = hdr.cells[c]
        set_cell_background(cell, "003366")
        set_cell_margins(cell, top=110, bottom=110, left=120, right=120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(text.replace('**', '').strip())
        r.bold = True
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for ridx, row_data in enumerate(row_cells_list):
        row = tbl.rows[ridx + 1]
        row_trPr = row._tr.get_or_add_trPr()
        row_trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        bg = "F9FAFC" if ridx % 2 == 1 else "FFFFFF"
        for c, text in enumerate(row_data):
            if c >= cols:
                continue
            cell = row.cells[c]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=70, bottom=70, left=100, right=100)
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                r'<w:left w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>'
                r'<w:top w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>'
                r'<w:right w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>'
                r'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D0D5DD"/>'
                r'</w:tcBorders>'))
            
            # Split cell text by <br>, <br/> or newline for elegant multi-line display
            raw_lines = re.split(r'<br\s*/?>|\n', text.strip())
            for lidx, line in enumerate(raw_lines):
                line = line.strip()
                p = cell.paragraphs[0] if lidx == 0 else cell.add_paragraph()
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.line_spacing = 1.12
                add_inline(p, line, size=9)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

_TABLE_SEP_RE = re.compile(r'^\|[\s:\-|]+\|$')

def build_docx(md_path, docx_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.55)
        section.bottom_margin = Inches(0.55)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    normal = doc.styles['Normal']
    normal.font.name = 'Arial'
    normal.font.size = Pt(9.5)
    normal.font.color.rgb = DARK
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(3)

    # ---- Branded header block ----
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_before = Pt(0)
    p_hdr.paragraph_format.space_after = Pt(2)
    r1 = p_hdr.add_run(BRAND_MAIN + "\u00a0")
    r1.bold = True
    r1.font.name = 'Arial'
    r1.font.size = Pt(20)
    r1.font.color.rgb = ROYAL_BLUE
    
    r2 = p_hdr.add_run(BRAND_ACCENT)
    r2.bold = True
    r2.font.name = 'Arial'
    r2.font.size = Pt(20)
    r2.font.color.rgb = CORAL

    p_sub1 = doc.add_paragraph()
    p_sub1.paragraph_format.space_before = Pt(0)
    p_sub1.paragraph_format.space_after = Pt(2)
    r3 = p_sub1.add_run(BRAND_SUB)
    r3.bold = True
    r3.font.name = 'Arial'
    r3.font.size = Pt(13.5)
    r3.font.color.rgb = NAVY

    p_sub2 = doc.add_paragraph()
    p_sub2.paragraph_format.space_before = Pt(0)
    p_sub2.paragraph_format.space_after = Pt(6)
    rs = p_sub2.add_run(SUBTITLE)
    rs.bold = True
    rs.font.name = 'Arial'
    rs.font.size = Pt(10.5)
    rs.font.color.rgb = NAVY
    p_sub2._p.get_or_add_pPr().append(parse_xml(
        f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="16" w:space="3" w:color="003366"/></w:pBdr>'))

    # ---- Metadata card ----
    if META_CARD:
        mtbl = doc.add_table(rows=1, cols=1)
        mtbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        mcell = mtbl.cell(0, 0)
        mcell.width = Inches(7.0)
        set_cell_background(mcell, "F4F7FA")
        set_cell_margins(mcell, top=120, bottom=120, left=200, right=150)
        mtcPr = mcell._tc.get_or_add_tcPr()
        mtcPr.append(parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            r'<w:left w:val="single" w:sz="24" w:space="0" w:color="003366"/>'
            r'<w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/>'
            r'</w:tcBorders>'))
        for idx, line in enumerate(META_CARD):
            p = mcell.paragraphs[0] if idx == 0 else mcell.add_paragraph()
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_inline(p, line, size=9.5)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # ---- Body ----
    lines = md_text.split('\n')
    i, n = 0, len(lines)
    in_table = False
    header, rows = [], []

    def flush_table():
        nonlocal in_table, header, rows
        if in_table:
            add_styled_table(doc, header, rows)
            in_table, header, rows = False, [], []

    while i < n:
        raw = lines[i]
        stripped = raw.strip()

        # skip HTML audit metadata comments
        if stripped.startswith('<!--'):
            while i < n and not lines[i].strip().endswith('-->'):
                i += 1
            i += 1
            continue

        # fenced code block
        if stripped.startswith('```'):
            code = []
            i += 1
            while i < n and not lines[i].lstrip().startswith('```'):
                code.append(lines[i].rstrip('\n').rstrip('\r'))
                i += 1
            i += 1
            flush_table()
            add_code_block(doc, code)
            continue

        # table rows
        if stripped.startswith('|') and stripped.endswith('|'):
            if _TABLE_SEP_RE.match(stripped):
                i += 1
                continue
            cells = [c.strip() for c in stripped.strip('|').split('|')]
            if not in_table:
                in_table, header, rows = True, cells, []
            else:
                rows.append(cells)
            i += 1
            continue
        flush_table()

        if not stripped or stripped == '---':
            i += 1
            continue

        # skip markdown H1 title line (since we render our branded header)
        if stripped.startswith('# ') and not stripped.startswith('## '):
            i += 1
            continue

        if stripped.startswith('> '):
            quote = []
            while i < n and lines[i].strip().startswith('> '):
                quote.append(lines[i].strip()[2:])
                i += 1
            add_callout_box(doc, quote)
            continue

        if stripped.startswith('#### '):
            add_custom_heading(doc, stripped[5:], 3)
        elif stripped.startswith('### '):
            add_custom_heading(doc, stripped[4:], 2)
        elif stripped.startswith('## '):
            add_custom_heading(doc, stripped[3:], 1)
        elif stripped.startswith('* ') or stripped.startswith('- ') or stripped.startswith('• '):
            leading_spaces = len(raw) - len(raw.lstrip())
            level = leading_spaces // 2
            content = re.sub(r'^[*\-•]\s+', '', stripped)
            
            p = doc.add_paragraph(style='List Bullet')
            if level > 0:
                p.paragraph_format.left_indent = Inches(0.25 + (0.25 * level))
                
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_inline(p, content)
        elif re.match(r'^\d+\.\s', stripped):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.25)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_inline(p, stripped)
        else:
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(4)
            p.paragraph_format.line_spacing = 1.15
            add_inline(p, stripped)
        i += 1

    flush_table()

    # ---- DOCX Footer with Page Numbers ----
    for section in doc.sections:
        footer = section.footer
        p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        run = p.add_run("")
        fldChar1 = parse_xml(r'<w:fldChar w:fldCharType="begin" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        instrText = parse_xml(r'<w:instrText xml:space="preserve" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">PAGE</w:instrText>')
        fldChar2 = parse_xml(r'<w:fldChar w:fldCharType="separate" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        fldChar3 = parse_xml(r'<w:fldChar w:fldCharType="end" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run._r.append(parse_xml(r'<w:t xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">1</w:t>'))
        run._r.append(fldChar3)
        
        run = p.add_run(" / ")
        run.font.size = Pt(9)
        run.font.color.rgb = MUTED_SLATE
        
        run = p.add_run("")
        fldChar1 = parse_xml(r'<w:fldChar w:fldCharType="begin" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        instrText = parse_xml(r'<w:instrText xml:space="preserve" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">NUMPAGES</w:instrText>')
        fldChar2 = parse_xml(r'<w:fldChar w:fldCharType="separate" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        fldChar3 = parse_xml(r'<w:fldChar w:fldCharType="end" xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        run._r.append(fldChar1)
        run._r.append(instrText)
        run._r.append(fldChar2)
        run._r.append(parse_xml(r'<w:t xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">1</w:t>'))
        run._r.append(fldChar3)

    doc.save(docx_path)
    print(f"[DOCX GENERATED] {docx_path} ({os.path.getsize(docx_path)} bytes)")
    return docx_path

if __name__ == '__main__':
    md_file = os.path.join(BASE_DIR, "Website_Performance_Specialist_Proposal.md")
    docx_file = os.path.join(BASE_DIR, "Website_Performance_Optimization_Proposal.docx")
    build_docx(md_file, docx_file)

