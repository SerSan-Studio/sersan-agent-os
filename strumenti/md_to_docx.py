"""Convert a constrained Markdown document into a SERSAN-styled DOCX, using the marketing plan DOCX as the style template.
Usage: python -I -X utf8 md_to_docx.py <template.docx> <in.md> <out.docx> "<footer text>" [<lockup.png>]
With a lockup image (strumenti/brand/sersan-lockup.png, made by marchio.py) the brand goes on the cover, large,
and in the page header from page 2 on; headings take the brand navy of the mark.
Markdown subset: front matter lines '% Title', '% Subtitle', '% Status' at the top; '#'..'####' headings; paragraphs;
'- ' and '  - ' bullets; '1. ' numbered items; '> ' notes; ``` code blocks; pipe tables; **bold**, `code`, [text](url)."""
import sys, re, copy, docx
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Cm
from docx.text.paragraph import Paragraph
from docx.opc.constants import RELATIONSHIP_TYPE as RT

INK = RGBColor(0x0B, 0x14, 0x22)
BRAND_NAVY = RGBColor(0x13, 0x27, 0x41)   # upper half of the SerSan mark (public/favicon.svg)
BLUE = RGBColor(0x16, 0x68, 0xBA)
GREY = RGBColor(0x6B, 0x75, 0x86)
INLINE = re.compile(r'(\*\*.+?\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))')


def add_hyperlink(par, text, url):
    rid = par.part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement('w:hyperlink')
    h.set(qn('r:id'), rid)
    r = OxmlElement('w:r')
    rpr = OxmlElement('w:rPr')
    col = OxmlElement('w:color')
    col.set(qn('w:val'), '1668BA')
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rpr.append(col)
    rpr.append(u)
    r.append(rpr)
    t = OxmlElement('w:t')
    t.text = text
    t.set(qn('xml:space'), 'preserve')
    r.append(t)
    h.append(r)
    par._p.append(h)


def add_inline(par, text, size=None, color=None, bold=None, italic=None):
    for piece in INLINE.split(text):
        if not piece:
            continue
        if piece.startswith('**') and piece.endswith('**') and len(piece) > 4:
            run = par.add_run(piece[2:-2])
            run.bold = True
        elif piece.startswith('`') and piece.endswith('`') and len(piece) > 2:
            run = par.add_run(piece[1:-1])
            run.font.name = 'Consolas'
            run._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:cs'), 'Consolas')
        elif piece.startswith('[') and '](' in piece and piece.endswith(')'):
            label, url = piece[1:].split('](', 1)
            add_hyperlink(par, label, url[:-1])
            continue
        else:
            run = par.add_run(piece)
            if bold is not None:
                run.bold = bold
        if size:
            run.font.size = Pt(size)
        if color is not None:
            run.font.color.rgb = color
        if italic:
            run.italic = True


def clear_cell(tc):
    ps = tc.findall(qn('w:p'))
    p = Paragraph(ps[0], None)
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    for extra in ps[1:]:
        tc.remove(extra)
    return p


class Builder:
    def __init__(self, template, footer):
        self.doc = docx.Document(template)
        d = self.doc
        self.proto = copy.deepcopy(d.tables[0]._tbl)
        body = d.element.body
        for child in list(body):
            if child.tag != qn('w:sectPr'):
                body.remove(child)
        # the template links its footer from a section break that was just removed: link footer1 from the final sectPr
        sect = body.find(qn('w:sectPr'))
        if sect is not None and sect.find(qn('w:footerReference')) is None:
            for rid, rel in d.part.rels.items():
                if rel.reltype.endswith('/footer') and str(rel.target_part.partname).endswith('footer1.xml'):
                    ref = OxmlElement('w:footerReference')
                    ref.set(qn('w:type'), 'default')
                    ref.set(qn('r:id'), rid)
                    sect.insert(0, ref)
                    break
        for part in d.part.package.iter_parts():
            if '/word/footer' in str(part.partname) and hasattr(part, '_element'):
                for t in part._element.iter(qn('w:t')):
                    if t.text and 'Piano marketing 90 giorni · Documento interno' in t.text:
                        t.text = t.text.replace('Piano marketing 90 giorni · Documento interno', footer)
        self.first_h1 = True

    def brand(self, lockup):
        """Brand navy on headings, lockup in the header of every page but the cover."""
        for name in ('Heading 1', 'Heading 2', 'Heading 3'):
            self.doc.styles[name].font.color.rgb = BRAND_NAVY
        sec = self.doc.sections[-1]
        sec.different_first_page_header_footer = True
        # room between the header lockup and the body text
        sec.header_distance = Cm(1.0)
        sec.top_margin = Cm(2.3)
        hp = sec.header.paragraphs[0]
        for r in list(hp.runs):
            r._r.getparent().remove(r._r)
        hp.add_run().add_picture(lockup, height=Cm(0.5))
        # the cover keeps the page footer it always had
        fp = sec.first_page_footer.paragraphs[0]
        src = sec.footer.paragraphs
        if src and not fp.text:
            fp._p.getparent().replace(fp._p, copy.deepcopy(src[0]._p))

    def cover_lockup(self, lockup):
        p = self.doc.add_paragraph(style='Normal')
        p.add_run().add_picture(lockup, width=Cm(6.5))
        p.paragraph_format.space_after = Pt(28)
        return p

    def para(self, text, style='Normal', **kw):
        p = self.doc.add_paragraph(style=style)
        add_inline(p, text, **kw)
        return p

    def page_break(self):
        p = self.doc.add_paragraph()
        br = OxmlElement('w:br')
        br.set(qn('w:type'), 'page')
        p.add_run()._r.append(br)

    def heading(self, level, text):
        p = self.doc.add_paragraph(style='Heading %d' % min(level, 4))
        if level == 1:
            # "page break before" on the heading itself: a separate break paragraph can land alone
            # on a fresh page when the previous page is exactly full, leaving a blank page
            if not self.first_h1:
                p.paragraph_format.page_break_before = True
            self.first_h1 = False
        add_inline(p, text)
        return p

    def code(self, lines):
        for ln in lines:
            p = self.doc.add_paragraph(style='Normal')
            pPr = p._p.get_or_add_pPr()
            shd = OxmlElement('w:shd')
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')
            shd.set(qn('w:fill'), 'F2F4F7')
            pPr.append(shd)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.left_indent = Cm(0.4)
            r = p.add_run(ln if ln else ' ')
            r.font.name = 'Consolas'
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:cs'), 'Consolas')
            r.font.size = Pt(8.5)
        self.doc.add_paragraph()

    def table(self, header, rows):
        n = len(header)
        tbl = copy.deepcopy(self.proto)
        trs = tbl.findall(qn('w:tr'))
        hp, bp = trs[0], (trs[1] if len(trs) > 1 else trs[0])
        for tr in trs:
            tbl.remove(tr)

        def build_row(proto_tr, cells, is_header):
            tr = copy.deepcopy(proto_tr)
            tcs = tr.findall(qn('w:tc'))
            first = tcs[0]
            for tc in tcs:
                tr.remove(tc)
            for j in range(n):
                tc = copy.deepcopy(first)
                p = clear_cell(tc)
                add_inline(p, cells[j] if j < len(cells) else '', bold=True if is_header else None)
                tr.append(tc)
            # a row never splits across two pages; the header row repeats on every page of the table
            trPr = tr.find(qn('w:trPr'))
            if trPr is None:
                trPr = OxmlElement('w:trPr')
                tr.insert(0, trPr)
            if trPr.find(qn('w:cantSplit')) is None:
                trPr.append(OxmlElement('w:cantSplit'))
            if is_header and trPr.find(qn('w:tblHeader')) is None:
                trPr.append(OxmlElement('w:tblHeader'))
            return tr

        tbl.append(build_row(hp, header, True))
        for r in rows:
            tbl.append(build_row(bp, r, False))
        grid = tbl.find(qn('w:tblGrid'))
        total = sum(int(c.get(qn('w:w'))) for c in grid.findall(qn('w:gridCol')))
        for c in grid.findall(qn('w:gridCol')):
            grid.remove(c)
        lens = []
        for j in range(n):
            col = [header[j]] + [r[j] if j < len(r) else '' for r in rows]
            lens.append(max(6, min(60, max(len(x) for x in col))) ** 0.8)
        fr = [l / sum(lens) for l in lens]
        # a column is never narrower than its longest word (about 95 characters fit a full-width line)
        min_fr = []
        for j in range(n):
            col = [header[j]] + [r[j] if j < len(r) else '' for r in rows]
            words = [w for x in col for w in re.sub(r'[*`]', '', x).split()]
            longest = max([len(w) for w in words] or [4])
            min_fr.append(max(0.08, (longest + 2) / 95.0))
        # columns below their minimum are pinned to it; the others share the rest in proportion
        # (a plain max-then-normalize can shrink a pinned column below its longest word again)
        if sum(min_fr) >= 1:
            fr = [m / sum(min_fr) for m in min_fr]
        else:
            pinned = [False] * n
            while True:
                free = 1 - sum(m for m, p in zip(min_fr, pinned) if p)
                tot = sum(f for f, p in zip(fr, pinned) if not p)
                cand = [m if p else f / tot * free for f, m, p in zip(fr, min_fr, pinned)]
                low = [j for j in range(n) if not pinned[j] and cand[j] < min_fr[j]]
                if not low:
                    fr = cand
                    break
                for j in low:
                    pinned[j] = True
            fr = [f / sum(fr) for f in fr]  # only changes anything when every column ended up pinned
        widths = [int(total * f) for f in fr]
        for w in widths:
            gc = OxmlElement('w:gridCol')
            gc.set(qn('w:w'), str(w))
            grid.append(gc)
        for tr in tbl.findall(qn('w:tr')):
            for tc, w in zip(tr.findall(qn('w:tc')), widths):
                tcPr = tc.find(qn('w:tcPr'))
                if tcPr is None:
                    tcPr = OxmlElement('w:tcPr')
                    tc.insert(0, tcPr)
                tcW = tcPr.find(qn('w:tcW'))
                if tcW is None:
                    tcW = OxmlElement('w:tcW')
                    tcPr.insert(0, tcW)
                tcW.set(qn('w:w'), str(w))
                tcW.set(qn('w:type'), 'dxa')
        body = self.doc.element.body
        body.insert(len(body) - 1, tbl)
        self.doc.add_paragraph()


def parse_table(lines):
    rows = [[c.strip() for c in ln.strip().strip('|').split('|')] for ln in lines]
    header = rows[0]
    if len(rows) > 1 and set(''.join(rows[1])) <= set('-: '):
        return header, rows[2:]
    return header, rows[1:]


def main():
    tpl, src, out, footer = sys.argv[1:5]
    lockup = sys.argv[5] if len(sys.argv) > 5 else None
    lines = open(src, encoding='utf-8').read().split('\n')
    b = Builder(tpl, footer)
    meta = []
    while lines and lines[0].startswith('% '):
        meta.append(lines.pop(0)[2:])
    if lockup:
        b.brand(lockup)
        b.cover_lockup(lockup)
    else:
        b.para('', 'Normal')
    if len(meta) > 0:
        b.para(meta[0], 'Normal', size=28, color=BRAND_NAVY if lockup else INK)
    if len(meta) > 1:
        b.para(meta[1], 'Normal', size=13, color=BLUE)
    if len(meta) > 2:
        b.para(meta[2], 'Normal', size=9, color=GREY)
    heads, in_code = [], False
    for ln in lines:
        if ln.startswith('```'):
            in_code = not in_code
            continue
        m = None if in_code else re.match(r'^(#{1,2})\s+(.*)$', ln)
        if m:
            heads.append((len(m.group(1)), m.group(2).strip()))
    if heads:
        b.para('Indice', 'Heading 3')
        for lvl, t in heads:
            p = b.para(('    ' if lvl == 2 else '') + re.sub(r'[*`]', '', t), 'Normal',
                       size=9.5 if lvl == 2 else 10.5, color=INK if lvl == 1 else GREY)
            p.paragraph_format.space_after = Pt(0)
        b.page_break()
    i, para_buf = 0, []

    def flush():
        if para_buf:
            b.para(' '.join(s.strip() for s in para_buf))
            para_buf.clear()

    while i < len(lines):
        s = lines[i].rstrip()
        if not s.strip():
            flush(); i += 1; continue
        m = re.match(r'^(#{1,4})\s+(.*)$', s)
        if m:
            flush(); b.heading(len(m.group(1)), m.group(2).strip()); i += 1; continue
        if s.startswith('```'):
            flush(); j = i + 1; buf = []
            while j < len(lines) and not lines[j].startswith('```'):
                buf.append(lines[j]); j += 1
            b.code(buf); i = j + 1; continue
        if s.lstrip().startswith('|'):
            flush(); j = i; buf = []
            while j < len(lines) and lines[j].lstrip().startswith('|'):
                buf.append(lines[j]); j += 1
            h, rows = parse_table(buf); b.table(h, rows); i = j; continue
        if s.startswith('> '):
            flush(); b.para(s[2:], 'Normal', color=GREY, italic=True); i += 1; continue
        mb = re.match(r'^(\s*)[-*]\s+(.*)$', s)
        if mb:
            flush(); lvl = len(mb.group(1)) // 2
            b.para(mb.group(2), 'List Bullet 2' if lvl >= 1 else 'List Bullet'); i += 1; continue
        mn = re.match(r'^(\s*)(\d+)\.\s+(.*)$', s)
        if mn:
            flush(); lvl = len(mn.group(1)) // 2
            p = b.para(mn.group(2) + '. ' + mn.group(3), 'Normal')
            p.paragraph_format.left_indent = Cm(0.6 + 0.6 * lvl)
            p.paragraph_format.first_line_indent = Cm(-0.5)
            p.paragraph_format.space_after = Pt(2)
            i += 1; continue
        para_buf.append(s); i += 1
    flush()
    # titolo e oggetto del file: senza, restano quelli del modello di stile
    if meta:
        b.doc.core_properties.title = meta[0]
        b.doc.core_properties.subject = meta[1] if len(meta) > 1 else ''
    b.doc.save(out)
    print('saved', out)


if __name__ == '__main__':
    main()
