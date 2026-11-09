"""Genera il lockup SerSan (marchio a due toni + scritta SERSAN) per i documenti.
La scritta usa Sersan Display 340 (il font del logotipo del sito, derivato da Jost, licenza SIL OFL in brand/LICENSE-Jost.txt)
con la spaziatura del sito (0,3 em), convertita in tracciati: il PDF non ha bisogno del font installato.
Il marchio usa la geometria e i colori "chiari" di brand/favicon.svg (metà alta #132741, metà bassa #2280DC).
Uso, dalla cartella del progetto:  python -I -X utf8 strumenti/marchio.py
Scrive brand/sersan-lockup.svg e brand/sersan-lockup.png (sfondo trasparente)."""
import os, re
import fitz
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brand')
NAVY, BLUE = '#132741', '#2280DC'
TRACKING = 0.30          # em, come il data-hero-brand del sito
MARK_H = 200.0           # altezza del marchio (unità del viewBox originale)
CAP_RATIO = 0.42         # altezza delle maiuscole rispetto al marchio
GAP_RATIO = 0.60         # spazio marchio-scritta rispetto all'altezza delle maiuscole


def mark_paths():
    svg = open(os.path.join(HERE, 'favicon.svg'), encoding='utf-8').read()
    upper = re.search(r'class="upper" d="([^"]+)"', svg).group(1)
    lower = re.search(r'class="lower" d="([^"]+)"', svg).group(1)
    return upper, lower


def wordmark(text='SERSAN'):
    font = TTFont(os.path.join(HERE, 'sersan-display-340.woff2'))
    gs, cmap, hmtx = font.getGlyphSet(), font.getBestCmap(), font['hmtx']
    upm, cap = font['head'].unitsPerEm, font['OS/2'].sCapHeight
    parts, x, xmin, xmax = [], 0.0, None, None
    for i, ch in enumerate(text):
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs)
        gs[g].draw(pen)
        bp = BoundsPen(gs)
        gs[g].draw(bp)
        if bp.bounds:
            b0, b2 = x + bp.bounds[0], x + bp.bounds[2]
            xmin = b0 if xmin is None else min(xmin, b0)
            xmax = b2 if xmax is None else max(xmax, b2)
        parts.append((x, pen.getCommands()))
        x += hmtx[g][0] + (TRACKING * upm if i < len(text) - 1 else 0)
    return parts, xmin, xmax, cap


def build():
    upper, lower = mark_paths()
    parts, xmin, xmax, cap = wordmark()
    s = CAP_RATIO * MARK_H / cap                  # unità font -> unità del lockup
    mark_w = 162.38
    gap = GAP_RATIO * CAP_RATIO * MARK_H
    x0 = mark_w + gap - xmin * s                   # inizio della scritta, al bordo dell'inchiostro
    base = MARK_H / 2 + CAP_RATIO * MARK_H / 2     # maiuscole centrate sul marchio
    width = mark_w + gap + (xmax - xmin) * s
    pad = 4
    glyphs = '\n'.join(
        '<path transform="translate(%.3f %.3f) scale(%.5f %.5f)" d="%s"/>' % (x0 + gx * s, base, s, -s, d)
        for gx, d in parts if d)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.2f %.2f %.2f %.2f" width="%.2f" height="%.2f">\n'
           '<path fill="%s" d="%s"/>\n<path fill="%s" d="%s"/>\n<g fill="%s">\n%s\n</g>\n</svg>\n') % (
        -pad, -pad, width + 2 * pad, MARK_H + 2 * pad, width + 2 * pad, MARK_H + 2 * pad,
        NAVY, upper, BLUE, lower, NAVY, glyphs)
    svg_path = os.path.join(HERE, 'sersan-lockup.svg')
    open(svg_path, 'w', encoding='utf-8').write(svg)
    doc = fitz.open(stream=svg.encode('utf-8'), filetype='svg')
    page = doc[0]
    zoom = 2400 / page.rect.width                  # circa 2400 px di larghezza: nitido anche in stampa
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=True)
    png_path = os.path.join(HERE, 'sersan-lockup.png')
    pix.save(png_path)
    print('scritti', svg_path, 'e', png_path, '(%dx%d px)' % (pix.width, pix.height))


if __name__ == '__main__':
    build()
