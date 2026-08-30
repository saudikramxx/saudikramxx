# -*- coding: utf-8 -*-
"""Generate the simple white/blue header for the saudikramxx profile README.

Two variants so the banner blends into GitHub's own canvas instead of sitting
on it as a block: light uses #FFFFFF (GitHub light canvas), dark uses #0D1117
(GitHub dark canvas). Blue is SIK TECH's #0B5FD9 / #4A9BFF.

Manrope is embedded as base64 woff2 - external @font-face URLs do not load in
<img>-rendered SVG, but data URIs do.

Regenerate:  python assets/generate.py .
"""
import sys, io, os

sp = sys.argv[1]
B64 = io.open(os.path.join(sp, 'assets', 'fonts', 'manrope-800.b64')).read().strip()
A = os.path.join(sp, 'assets')

W, H = 1200, 190
NAVY, BLUE, BLUE_L = '#0A2540', '#0B5FD9', '#4A9BFF'


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
             .replace(u"’", '&#8217;').replace(u"·", '&#183;'))


def build(bg, name_col, tag_col, sub_col, rule_col):
    f = ("@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;"
         "src:url(data:font/woff2;base64," + B64 + ") format('woff2');}"
         ".f{font-family:'Manrope','Segoe UI',system-ui,Helvetica,Arial,sans-serif;}")
    p = []
    p.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
             'role="img" aria-label="Saud Ikram - I build custom AI applications around your business">'
             % (W, H, W, H))
    p.append('<defs><style>' + f + '</style></defs>')
    p.append('<rect width="%d" height="%d" fill="%s"/>' % (W, H, bg))
    # thin blue accent bar down the left of the text block
    p.append('<rect x="0" y="54" width="4" height="86" rx="2" fill="%s"/>' % tag_col)
    p.append('<text class="f" x="30" y="88" fill="%s" font-size="42" font-weight="800" '
             'letter-spacing="-1.2">Saud Ikram</text>' % name_col)
    p.append('<text class="f" x="32" y="126" fill="%s" font-size="20" font-weight="600" '
             'letter-spacing="-0.2">%s</text>'
             % (tag_col, esc(u"I build custom AI applications around your business.")))
    p.append('<line x1="32" y1="150" x2="%d" y2="150" stroke="%s" stroke-width="1"/>' % (W - 60, rule_col))
    p.append('<text class="f" x="32" y="172" fill="%s" font-size="13.5" font-weight="500" '
             'letter-spacing="0.4">%s</text>'
             % (sub_col, esc(u"AI agents · RAG & document intelligence · Workflow automation · Voice & meeting AI")))
    p.append('</svg>')
    return ''.join(p)


light = build(bg='#FFFFFF', name_col=NAVY, tag_col=BLUE, sub_col='#5B6B7C', rule_col='#DCE6F2')
dark = build(bg='#0D1117', name_col='#FFFFFF', tag_col=BLUE_L, sub_col='#8B949E', rule_col='#21262D')

io.open(os.path.join(A, 'header-light.svg'), 'w', encoding='utf-8', newline='\n').write(light)
io.open(os.path.join(A, 'header-dark.svg'), 'w', encoding='utf-8', newline='\n').write(dark)
print('header-light.svg %d bytes / header-dark.svg %d bytes (%dx%d)' % (len(light), len(dark), W, H))
