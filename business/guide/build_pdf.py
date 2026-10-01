#!/usr/bin/env python3
"""Build the PingLifts Guide PDF: dark identity, image placeholders as labeled boxes."""
import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, Image as RLImage, KeepTogether, PageBreak, Flowable)
from PIL import Image as PILImage

INK, INK2, GREEN, CREAM, MUTED, BORDER = ('#141A13', '#1C241B', '#7FA96E', '#F4F0E6', '#9AA694', '#3A4636')
PAGE_W, PAGE_H = A4
M = 22*mm
AVAIL = PAGE_W - 2*M

S = {
 'part':   ParagraphStyle('part', fontName='Helvetica-Bold', fontSize=24, leading=29, textColor=HexColor(GREEN), spaceAfter=6),
 'partsub':ParagraphStyle('partsub', fontName='Helvetica', fontSize=11, leading=15, textColor=HexColor(MUTED), spaceAfter=14),
 'chap':   ParagraphStyle('chap', fontName='Helvetica-Bold', fontSize=15.5, leading=19, textColor=HexColor(CREAM), spaceBefore=16, spaceAfter=8),
 'h3':     ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=HexColor(GREEN), spaceBefore=10, spaceAfter=5),
 'body':   ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, leading=16, textColor=HexColor('#D8D4C8'), spaceAfter=8),
 'li':     ParagraphStyle('li', fontName='Helvetica', fontSize=10.5, leading=15, textColor=HexColor('#D8D4C8'), leftIndent=14, bulletIndent=4, spaceAfter=4),
 'nli':    ParagraphStyle('nli', fontName='Helvetica', fontSize=10.5, leading=15, textColor=HexColor('#D8D4C8'), leftIndent=18, spaceAfter=4),
 'quote':  ParagraphStyle('quote', fontName='Helvetica-Bold', fontSize=11, leading=16.5, textColor=HexColor(CREAM), leftIndent=10, rightIndent=10),
 'cellh':  ParagraphStyle('cellh', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=HexColor(GREEN)),
 'cell':   ParagraphStyle('cell', fontName='Helvetica', fontSize=10, leading=13, textColor=HexColor('#D8D4C8')),
 'boxlbl': ParagraphStyle('boxlbl', fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=HexColor(MUTED), alignment=TA_CENTER),
 'note':   ParagraphStyle('note', fontName='Helvetica-Oblique', fontSize=9, leading=13, textColor=HexColor(MUTED)),
}

def esc(t):
    t = t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'\*(.+?)\*', r'<i>\1</i>', t)
    return t

class PlaceholderBox(Flowable):
    """Labeled image slot for manual graphic insertion."""
    def __init__(self, label, width=AVAIL, height=62*mm):
        super().__init__()
        self.label, self.width, self.height = label, width, height
    def draw(self):
        c = self.canv
        c.saveState()
        c.setStrokeColor(HexColor(GREEN)); c.setFillColor(HexColor(INK2))
        c.setLineWidth(1.2); c.setDash(4, 3)
        c.roundRect(0, 0, self.width, self.height, 6*mm, stroke=1, fill=1)
        c.setDash()
        c.setFillColor(HexColor(GREEN))
        c.setFont('Helvetica-Bold', 9)
        c.drawCentredString(self.width/2, self.height/2 + 8, 'IMAGE')
        # wrap label
        words = self.label; maxw = self.width - 40
        lines, cur = [], ''
        for w in words.split():
            t = (cur + ' ' + w).strip()
            if c.stringWidth(t, 'Helvetica', 8.5) <= maxw: cur = t
            else: lines.append(cur); cur = w
        lines.append(cur)
        c.setFillColor(HexColor(MUTED)); c.setFont('Helvetica', 8.5)
        y = self.height/2 - 8
        for ln in lines[:3]:
            c.drawCentredString(self.width/2, y, ln); y -= 11
        c.restoreState()

def dark_page(canv, doc):
    canv.saveState()
    canv.setFillColor(HexColor(INK)); canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canv.setStrokeColor(HexColor(BORDER)); canv.setLineWidth(0.5)
    canv.line(M, 14*mm, PAGE_W - M, 14*mm)
    canv.setFillColor(HexColor(MUTED)); canv.setFont('Helvetica', 8)
    canv.drawCentredString(PAGE_W/2, 9*mm, str(canv.getPageNumber()))
    canv.restoreState()

def cover(canv, doc):
    canv.saveState()
    canv.setFillColor(HexColor(INK)); canv.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canv.setFillColor(HexColor(GREEN)); canv.setFont('Helvetica-Bold', 10)
    canv.drawString(M, PAGE_H - 40*mm, 'P I N G L I F T S   F I T N E S S')
    canv.setFillColor(HexColor(CREAM)); canv.setFont('Helvetica-Bold', 30)
    canv.drawString(M, PAGE_H - 62*mm, 'The Only Muscle Building')
    canv.drawString(M, PAGE_H - 74*mm, 'Cheat Sheet You Ever Need')
    canv.setStrokeColor(HexColor(GREEN)); canv.setLineWidth(2)
    canv.line(M, PAGE_H - 82*mm, M + 52*mm, PAGE_H - 82*mm)
    canv.setFillColor(HexColor(MUTED)); canv.setFont('Helvetica', 11.5)
    canv.drawString(M, PAGE_H - 92*mm, 'Training. Nutrition. Supplements. No guessing.')
    # gradient-blended opener: photo fades into the dark background at top and bottom
    src = PILImage.open('images/01-opener.jpg').convert('RGB')
    w = PAGE_W; h = PAGE_H * 0.58
    im_h = 900
    tmp = src.resize((int(w / h * im_h), im_h), PILImage.LANCZOS).convert('RGBA')
    fade_top, fade_bot = int(im_h * 0.45), int(im_h * 0.30)
    px_ = tmp.load()
    for y in range(im_h):
        if y < fade_top: a = int(255 * (y / fade_top) ** 1.3)
        elif y > im_h - fade_bot: a = int(255 * ((im_h - y) / fade_bot) ** 1.2)
        else: a = 255
        for x in range(tmp.size[0]):
            r, g, b, _ = px_[x, y]
            # blend toward ink as alpha falls so it melts into the background
            br = a / 255
            rr = int(r * br + 0x14 * (1 - br)); gg = int(g * br + 0x1A * (1 - br)); bb = int(b * br + 0x13 * (1 - br))
            px_[x, y] = (rr, gg, bb, 255)
    tmp.convert('RGB').save('/tmp/cover-blend.jpg', quality=90)
    canv.drawImage('/tmp/cover-blend.jpg', 0, 0, PAGE_W, h, mask='auto')
    canv.setFillColor(HexColor(MUTED)); canv.setFont('Helvetica', 9)
    canv.drawString(M, 18*mm, 'pingliftsfitness.com')
    canv.drawRightString(PAGE_W - M, 18*mm, '2026')
    canv.restoreState()

story = [Spacer(1, 1)]  # cover placeholder flow; we use PageTemplates instead
md = open('pinglifts-guide.md').read()
lines = md.split('\n')

flow = []
i = 0
in_tree = False
tree_buf = []
def flush_tree():
    global tree_buf
    if tree_buf:
        txt = '\n'.join(tree_buf).strip('`').strip()
        paras = [Paragraph(esc(l).replace('  ', '&nbsp;&nbsp;'), ParagraphStyle('tree', parent=S['body'], fontName='Courier', fontSize=8.8, leading=13, textColor=HexColor('#C9D3C2'), backColor=HexColor(INK2), borderPadding=8, leftIndent=6)) for l in txt.split('\n') if l.strip()]
        flow.extend(paras); flow.append(Spacer(1, 10))
        tree_buf = []

while i < len(lines):
    ln = lines[i].rstrip()
    if ln.strip().startswith('```'):
        in_tree = not in_tree; i += 1; continue
    if in_tree:
        tree_buf.append(ln); i += 1; continue
    flush_tree()
    s = ln.strip()
    if not s or s == '---':
        i += 1; continue
    m = re.match(r'^\*\*\[IMAGE: (.+?)\]\*\*$', s)
    if m:
        lbl = m.group(1).replace('✗', 'NO').replace('✓', 'YES')
        flow.append(Spacer(1, 8))
        gfx = next((p for key, p in [
            ('Three-panel myth', 'graphics/myth-pump-soreness-tension.png'),
            ('Rep-range', 'graphics/rep-range-equalizer.png'),
        ] if key in lbl and os.path.exists(p)), None)
        if gfx:
            im = PILImage.open(gfx)
            w = AVAIL; h = w * im.size[1] / im.size[0]
            flow.append(RLImage(gfx, width=w, height=h, hAlign='CENTER'))
        else:
            flow.append(PlaceholderBox(lbl))
        flow.append(Spacer(1, 10)); i += 1; continue
    if s.startswith('# '):
        if 'cheat sheet' in s.lower():
            i += 1; continue
        if flow: flow.append(PageBreak())
        flow.append(Spacer(1, 6))
        flow.append(Paragraph(esc(s[2:]), S['part'])); i += 1; continue
    if s.startswith('## '):
        txt = esc(s[3:])
        if txt.lower().startswith(('introduction', 'your next')) and flow:
            flow.append(PageBreak()); flow.append(Spacer(1, 6))
        flow.append(Paragraph(txt, S['chap'])); i += 1; continue
    if s.startswith('### '):
        flow.append(Paragraph(esc(s[4:]), S['h3'])); i += 1; continue
    if s.startswith('> '):
        flow.append(Spacer(1, 4))
        q = Paragraph(esc(s[2:]), S['quote'])
        qt = Table([[q]], colWidths=[AVAIL])
        qt.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), HexColor(INK2)),
                                ('LINEBEFORE', (0,0), (0,-1), 2, HexColor(GREEN)),
                                ('LEFTPADDING', (0,0), (-1,-1), 12), ('RIGHTPADDING', (0,0), (-1,-1), 12),
                                ('TOPPADDING', (0,0), (-1,-1), 9), ('BOTTOMPADDING', (0,0), (-1,-1), 9)]))
        flow.append(qt); flow.append(Spacer(1, 10)); i += 1; continue
    if s.startswith('- '):
        flow.append(Paragraph(esc(s[2:]), S['li'], bulletText='•')); i += 1; continue
    m = re.match(r'^(\d+)\.\s+(.*)$', s)
    if m:
        flow.append(Paragraph(esc(m.group(2)), S['nli'], bulletText=m.group(1) + '.')); i += 1; continue
    if s.startswith('|'):
        tbl_lines = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            row = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.match(r'^[-: ]+$', c) for c in row):
                tbl_lines.append(row)
            i += 1
        if tbl_lines:
            data = [[Paragraph(esc(c), S['cellh'] if r == 0 else S['cell']) for c in row] for r, row in enumerate(tbl_lines)]
            ncol = max(len(r) for r in data)
            widths = [AVAIL / ncol] * ncol
            t = Table(data, colWidths=widths, hAlign='CENTER')
            t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), HexColor(INK2)),
                                   ('LINEBELOW', (0,0), (-1,0), 0.8, HexColor(GREEN)),
                                   ('LINEBELOW', (0,-1), (-1,-1), 0.5, HexColor(BORDER)),
                                   ('ROWBACKGROUNDS', (0,1), (-1,-1), [HexColor('#161D15'), HexColor(INK2)]),
                                   ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                                   ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8)]))
            flow.append(Spacer(1, 6)); flow.append(t); flow.append(Spacer(1, 10))
        continue
    if s.startswith('*') and s.endswith('*') and not s.startswith('**'):
        flow.append(Paragraph(esc(s.strip('*')), S['note'])); i += 1; continue
    flow.append(Paragraph(esc(s), S['body'])); i += 1

flush_tree()

# closer photo before final disclaimer
cl = PILImage.open('images/28-closer.jpg'); cw, ch = AVAIL * 0.55, AVAIL * 0.55 * cl.size[1] / cl.size[0]
flow.append(Spacer(1, 12))
flow.append(RLImage('images/28-closer.jpg', width=cw, height=ch, hAlign='CENTER'))
flow.append(Spacer(1, 6))

doc = BaseDocTemplate('PingLifts-Guide-to-Building-Muscle.pdf', pagesize=A4,
                      leftMargin=M, rightMargin=M, topMargin=20*mm, bottomMargin=20*mm,
                      title='The Only Muscle Building Cheat Sheet You Ever Need', author='PingLifts Fitness')
frame_c = Frame(M, 20*mm, AVAIL, PAGE_H - 40*mm, id='c')
frame_b = Frame(M, 20*mm, AVAIL, PAGE_H - 40*mm, id='b')
doc.addPageTemplates([PageTemplate(id='cover', frames=[frame_c], onPage=cover),
                      PageTemplate(id='body', frames=[frame_b], onPage=dark_page)])
story = flow
from reportlab.platypus import NextPageTemplate
story = [NextPageTemplate('body'), PageBreak()] + flow
doc.build(story)
print('PDF built')
