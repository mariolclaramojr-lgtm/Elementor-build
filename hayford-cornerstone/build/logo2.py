"""Premium Hayford logo concepts. Text is converted to outlines so the SVGs need no fonts."""
import os
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

HERE = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(HERE, 'fonts')
_cache = {}
def font(name, **axes):
    k = (name, tuple(sorted(axes.items())))
    if k not in _cache:
        _cache[k] = instantiateVariableFont(TTFont(os.path.join(FD, name + '.ttf')), axes)
    return _cache[k]

def text(s, f, size, x, y, track=0.0, kern=True):
    """Return (svg path d, advance width). track in em."""
    gs = f.getGlyphSet(); cmap = f.getBestCmap(); upm = f['head'].unitsPerEm; sc = size / upm
    pen = SVGPathPen(gs); cx = 0
    for ch in s:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x + cx, y)))
        cx += gs[g].width * sc + track * size
    return pen.getCommands(), cx - track * size

def svg(w, h, body, title='Hayford Church'):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" width="{w:.0f}" height="{h:.0f}" '
            f'role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n')

# ---------------------------------------------------------------- marks (drawn in a 48 x 56 box)
def mark_monoline(c, sw=2.2):
    """A: fine-line arched window with a cross that grows from the threshold."""
    return (f'<g fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M6 55V24a18 18 0 0 1 36 0v31"/>'          # outer arch
            f'<path d="M2 55h44"/>'                              # threshold
            f'<path d="M24 14v41M16 25h16"/></g>')               # cross

def mark_crest(c, sw=1.6):
    """B: circular seal — thin ring, arched doorway, cross in negative space."""
    door = 'M15 44V27a9 9 0 0 1 18 0v17z'
    cross = 'M23 20.5h2v6h4.5v2H25V44h-2V28.5h-4.5v-2H23z'
    return (f'<circle cx="24" cy="28" r="23" fill="none" stroke="{c}" stroke-width="{sw}"/>'
            f'<circle cx="24" cy="28" r="19.6" fill="none" stroke="{c}" stroke-width="{sw*0.45}" opacity=".6"/>'
            f'<mask id="cm"><rect width="48" height="56" fill="#fff"/><path d="{cross}" fill="#000"/></mask>'
            f'<path d="{door}" fill="{c}" mask="url(#cm)"/>')

def mark_window(c, accent):
    """C: layered arches (light through a window) with an accent cross."""
    return (f'<path d="M4 55V24a20 20 0 0 1 40 0v31z" fill="{c}" opacity=".16"/>'
            f'<path d="M10 55V25a14 14 0 0 1 28 0v30z" fill="{c}" opacity=".38"/>'
            f'<path d="M16 55V27a8 8 0 0 1 16 0v28z" fill="{c}"/>'
            f'<path d="M24 30v16M19 35h10" stroke="{accent}" stroke-width="2.2" stroke-linecap="round"/>')

# ---------------------------------------------------------------- lockups
def concept_a(word, sub):
    fr = font('Fraunces', wght=560, opsz=72, SOFT=0, WONK=0)
    dm = font('DMSans', wght=600, opsz=14)
    p1, w1 = text('Hayford', fr, 40, 66, 33, track=-0.01)
    p2, w2 = text('CHURCH', dm, 9, 67.5, 56, track=0.62)
    W = 66 + max(w1, w2) + 2
    body = (f'<g transform="translate(0 1)">{mark_monoline(word)}</g>'
            f'<path d="{p1}" fill="{word}"/><path d="{p2}" fill="{sub}"/>')
    return svg(W, 58, body)

def concept_b(word, sub):
    fr = font('Fraunces', wght=500, opsz=48, SOFT=50, WONK=0)
    dm = font('DMSans', wght=500, opsz=14)
    p1, w1 = text('HAYFORD', fr, 28, 66, 33, track=0.14)
    p2, w2 = text('CHURCH', dm, 9, 66, 52, track=0.62)
    W = 66 + max(w1, w2) + 2
    rule = f'<path d="M{66 + w2 + 10:.1f} 48.5h{max(w1 - w2 - 10, 10):.1f}" stroke="{sub}" stroke-width="1"/>'
    body = f'{mark_crest(word)}<path d="{p1}" fill="{word}"/><path d="{p2}" fill="{sub}"/>{rule}'
    return svg(W, 58, body)

def concept_c(word, sub, accent):
    mr = font('Manrope', wght=300)
    fr = font('Fraunces', wght=500, opsz=36, SOFT=0, WONK=0)
    p1, w1 = text('HAYFORD', mr, 25, 64, 30, track=0.32)
    p2, w2 = text('Church', fr, 15, 65, 50, track=0.02)
    # italic accent: shear the serif word slightly
    W = 64 + max(w1, w2) + 2
    body = (f'{mark_window(word, accent)}<path d="{p1}" fill="{word}"/>'
            f'<g transform="translate(65 50) skewX(-10) translate(-65 -50)"><path d="{p2}" fill="{sub}"/></g>')
    return svg(W, 58, body)

if __name__ == '__main__':
    out = os.path.join(HERE, 'logo2')
    os.makedirs(out, exist_ok=True)
    INK, WHITE, ACC, ACCL, MUTED = '#0E1013', '#FFFFFF', '#3B55E6', '#AFBDFF', '#8A909A'
    files = {
        'A-light.svg': concept_a(INK, ACC), 'A-dark.svg': concept_a(WHITE, ACCL),
        'B-light.svg': concept_b(INK, ACC), 'B-dark.svg': concept_b(WHITE, ACCL),
        'C-light.svg': concept_c(INK, ACC, ACC), 'C-dark.svg': concept_c(WHITE, ACCL, ACCL),
    }
    for n, s in files.items():
        open(os.path.join(out, n), 'w').write(s)
    print('ok')
