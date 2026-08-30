# -*- coding: utf-8 -*-
"""Generate the animated white/blue profile banner for saudikramxx.

Two variants (light/dark) swapped via <picture> so the banner blends into
GitHub's own canvas instead of sitting on it as a block.

All motion is SMIL, which survives GitHub's raw SVG delivery. No JS, no
external requests: Manrope is embedded as a base64 woff2 because external
@font-face URLs do not load in <img>-rendered SVG.

Regenerate:  python assets/generate.py .
"""
import sys, io, os

sp = sys.argv[1]
B64 = io.open(os.path.join(sp, 'assets', 'fonts', 'manrope-800.b64')).read().strip()
A = os.path.join(sp, 'assets')

W = 1200
PAD = 54
CYCLE = 14.0                      # seconds for a full rotation of the typed lines
TYPE, HOLD = 1.15, 1.95           # type-in, then hold

PHRASES = [
    u"AI agents wired into your own tools.",
    u"RAG that answers from your documents.",
    u"Workflows that run themselves.",
    u"Voice AI that works offline.",
]
CARDS = [
    (u"AI Agents",   u"wired into your tools"),
    (u"RAG",         u"answers from your docs"),
    (u"Automation",  u"processes that run themselves"),
    (u"Voice AI",    u"offline transcription + minutes"),
]
STATS = [
    (u"100%", u"line + branch coverage", u"hard CI gate, no exclusions"),
    (u"56",   u"architecture diagrams",  u"written before any code"),
    (u"0",    u"lock-in",                u"documented and handed over"),
]


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace(u"’", '&#8217;').replace(u"·", '&#183;'))


def kt(vals, times):
    """Emit values/keyTimes, de-duplicating non-increasing keyTimes."""
    v, t = [], []
    for val, tm in zip(vals, times):
        tm = min(1.0, max(0.0, tm))
        if t and tm <= t[-1]:
            tm = min(1.0, t[-1] + 1e-4)
        v.append(str(val)); t.append(tm)
    return ';'.join(v), ';'.join('%.5f' % x for x in t)


def typed_line(x, y, size, colour, caret):
    """Phrases that type in, hold, then clear - looping forever."""
    out = []
    slot = CYCLE / len(PHRASES)
    for i, p in enumerate(PHRASES):
        w = len(p) * size * 0.5            # approximate advance width for Manrope 600
        s0 = i * slot
        vals = [0, 0, w, w, 0, 0]
        times = [0.0, s0 / CYCLE, (s0 + TYPE) / CYCLE, (s0 + TYPE + HOLD) / CYCLE,
                 (s0 + TYPE + HOLD + 0.05) / CYCLE, 1.0]
        vv, tt = kt(vals, times)
        cid = 'clip%d' % i
        out.append('<clipPath id="%s"><rect x="%d" y="%d" height="%d" width="0">'
                   '<animate attributeName="width" values="%s" keyTimes="%s" dur="%ss" '
                   'repeatCount="indefinite" calcMode="spline" '
                   'keySplines="%s"/></rect></clipPath>'
                   % (cid, x, y - size, int(size * 1.6), vv, tt, CYCLE,
                      ' '.join(['.25 .1 .25 1'] * (len(vals) - 1))))
        out.append('<text class="f" x="%d" y="%d" fill="%s" font-size="%s" font-weight="600" '
                   'letter-spacing="-0.2" clip-path="url(#%s)">%s</text>'
                   % (x, y, colour, size, cid, esc(p)))
        # caret rides the end of the revealed text
        cvals = [x, x, x + w, x + w, x, x]
        cv, ct = kt(cvals, times)
        out.append('<rect y="%d" width="2.5" height="%d" rx="1.25" fill="%s" x="%d">'
                   '<animate attributeName="x" values="%s" keyTimes="%s" dur="%ss" '
                   'repeatCount="indefinite" calcMode="spline" keySplines="%s"/>'
                   '<animate attributeName="opacity" values="1;0;1" dur="1.05s" '
                   'repeatCount="indefinite"/></rect>'
                   % (y - size + 3, int(size * 1.15), caret, x, cv, ct, CYCLE,
                      ' '.join(['.25 .1 .25 1'] * (len(cvals) - 1))))
    return ''.join(out)


def build(dark):
    bg      = '#0D1117' if dark else '#FFFFFF'
    name_c  = '#FFFFFF' if dark else '#0A2540'
    blue    = '#4A9BFF' if dark else '#0B5FD9'
    body    = '#8B949E' if dark else '#5B6B7C'
    line    = '#21262D' if dark else '#E3EAF2'
    card_bg = '#161B22' if dark else '#F6F9FC'
    green   = '#1ED9A3' if dark else '#0F9D74'

    p = []
    H = 700
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
             'role="img" aria-label="Saud Ikram - custom AI developer. AI agents wired into your '
             'tools, RAG over your documents, workflow automation, offline voice AI. '
             '100 percent line and branch coverage, 56 architecture diagrams, no lock-in. '
             'sickteck.online">' % (W, H, W, H))
    p.append("<defs><style>@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;"
             "src:url(data:font/woff2;base64," + B64 + ") format('woff2');}"
             ".f{font-family:'Manrope','Segoe UI',system-ui,Helvetica,Arial,sans-serif;}</style></defs>")
    p.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, bg))

    # ---------- hero ----------
    p.append('<rect x="0" y="46" width="4" height="112" rx="2" fill="%s"/>' % blue)
    p.append('<text class="f" x="%d" y="52" fill="%s" font-size="12.5" font-weight="800" '
             'letter-spacing="2.8">CUSTOM AI DEVELOPER</text>' % (PAD - 24, blue))
    p.append('<text class="f" x="%d" y="112" fill="%s" font-size="46" font-weight="800" '
             'letter-spacing="-1.4">Saud Ikram</text>' % (PAD - 26, name_c))
    p.append(typed_line(PAD - 24, 152, 23, blue, blue))

    # availability
    p.append('<g transform="translate(%d,182)">' % (PAD - 24))
    p.append('<circle cx="6" cy="6" r="5.5" fill="%s">'
             '<animate attributeName="opacity" values="1;.2;1" dur="2.1s" repeatCount="indefinite"/>'
             '</circle>'
             '<circle cx="6" cy="6" r="5.5" fill="none" stroke="%s" stroke-width="1.5" opacity="0">'
             '<animate attributeName="r" values="5.5;13" dur="2.1s" repeatCount="indefinite"/>'
             '<animate attributeName="opacity" values=".7;0" dur="2.1s" repeatCount="indefinite"/>'
             '</circle>' % (green, green))
    p.append('<text class="f" x="22" y="11" fill="%s" font-size="13.5" font-weight="600">'
             'Available for projects</text></g>' % body)

    p.append('<line x1="%d" y1="230" x2="%d" y2="230" stroke="%s" stroke-width="1"/>'
             % (PAD - 24, W - PAD, line))

    # ---------- four cards, staggered shimmer ----------
    cw, gap = 264, 18
    x0 = PAD - 24
    for i, (title, sub) in enumerate(CARDS):
        x = x0 + i * (cw + gap)
        p.append('<g transform="translate(%d,262)">' % x)
        p.append('<rect width="%d" height="104" rx="12" fill="%s" stroke="%s"/>' % (cw, card_bg, line))
        # accent bar breathes, staggered across the row
        p.append('<rect x="0" y="20" width="3" height="64" rx="1.5" fill="%s">'
                 '<animate attributeName="opacity" values=".25;1;.25" dur="3.4s" begin="%ss" '
                 'repeatCount="indefinite"/></rect>' % (blue, round(i * 0.55, 2)))
        p.append('<text class="f" x="24" y="46" fill="%s" font-size="19" font-weight="800" '
                 'letter-spacing="-0.3">%s</text>' % (name_c, esc(title)))
        p.append('<text class="f" x="24" y="72" fill="%s" font-size="13.5" font-weight="500">%s</text>'
                 % (body, esc(sub)))
        p.append('</g>')

    # ---------- stats, rings draw on loop ----------
    for i, (big, label, sub) in enumerate(STATS):
        x = x0 + i * 372
        p.append('<g transform="translate(%d,412)">' % x)
        r, cxy = 30, 34
        p.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="4"/>'
                 % (cxy, cxy, r, line))
        circ = 2 * 3.14159 * r
        p.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="4" '
                 'stroke-linecap="round" stroke-dasharray="%.2f" stroke-dashoffset="%.2f" '
                 'transform="rotate(-90 %d %d)">'
                 '<animate attributeName="stroke-dashoffset" values="%.2f;0;0;%.2f" '
                 'keyTimes="0;0.45;0.85;1" dur="4.2s" begin="%ss" repeatCount="indefinite"/></circle>'
                 % (cxy, cxy, r, blue, circ, circ, cxy, cxy, circ, circ, round(i * 0.4, 2)))
        p.append('<text class="f" x="%d" y="%d" fill="%s" font-size="17" font-weight="800" '
                 'text-anchor="middle">%s</text>' % (cxy, cxy + 6, name_c, esc(big)))
        p.append('<text class="f" x="80" y="30" fill="%s" font-size="14.5" font-weight="700">%s</text>'
                 % (name_c, esc(label)))
        p.append('<text class="f" x="80" y="50" fill="%s" font-size="12.5" font-weight="500">%s</text>'
                 % (body, esc(sub)))
        p.append('</g>')

    p.append('<line x1="%d" y1="514" x2="%d" y2="514" stroke="%s" stroke-width="1"/>'
             % (PAD - 24, W - PAD, line))

    # ---------- cta ----------
    p.append('<text class="f" x="%d" y="576" fill="%s" font-size="30" font-weight="800" '
             'letter-spacing="-0.9">%s</text>' % (PAD - 24, name_c, esc(u"Let’s build something.")))
    p.append('<text class="f" x="%d" y="606" fill="%s" font-size="15" font-weight="500">%s</text>'
             % (PAD - 24, body, esc(u"Tell me what should be automated.")))
    p.append('<g transform="translate(%d,626)">' % (PAD - 24))
    p.append('<rect width="214" height="44" rx="22" fill="%s"/>' % blue)
    p.append('<text class="f" x="28" y="28" fill="#FFFFFF" font-size="14.5" font-weight="700">'
             'sickteck.online</text>')
    p.append('<g><path d="M158 22 h16 M168 16 l6 6 l-6 6" fill="none" stroke="#FFFFFF" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
             '<animateTransform attributeName="transform" type="translate" '
             'values="0 0;7 0;0 0" dur="1.8s" repeatCount="indefinite" calcMode="spline" '
             'keyTimes="0;0.5;1" keySplines=".4 0 .2 1;.4 0 .2 1"/></g>')
    p.append('</g>')
    p.append('</svg>')
    return ''.join(p)


light, dark = build(False), build(True)
io.open(os.path.join(A, 'header-light.svg'), 'w', encoding='utf-8', newline='\n').write(light)
io.open(os.path.join(A, 'header-dark.svg'), 'w', encoding='utf-8', newline='\n').write(dark)
print('header-light.svg %d bytes / header-dark.svg %d bytes' % (len(light), len(dark)))
