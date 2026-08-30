# -*- coding: utf-8 -*-
"""Generate a single continuous, brand-matched profile.svg for saudikramxx.

Palette + typeface sampled from https://sickteck.online/ (SIK TECH LLC).
Font is embedded as base64 woff2 so it renders identically everywhere with
no network request (external @font-face URLs are blocked in <img>-rendered SVG).
"""
import sys, io, os, math, textwrap

sp = sys.argv[1]
B64 = io.open(os.path.join(sp, 'assets', 'fonts', 'manrope-800.b64')).read().strip()
A = os.path.join(sp, 'assets')

BG, DEEP, CARD = '#0A0E16', '#0D1522', '#111A28'
BLUE, BLUE_D = '#4A9BFF', '#0B5FD9'
MUTED, LIGHT, DIM = '#AEBDCC', '#DCE6F2', '#5B6B7C'
GREEN = '#1ED9A3'
BORDER = '#1C2A3E'
W = 1200
PAD = 60


def esc(s):
    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return s.replace(u"’", '&#8217;').replace(u"—", '&#8212;').replace(u"·", '&#183;').replace("'", '&#8217;')


def txt(x, y, s, size, fill, weight=500, ls=None, anchor=None, cls='f'):
    a = ' text-anchor="%s"' % anchor if anchor else ''
    l = ' letter-spacing="%s"' % ls if ls is not None else ''
    return ('<text class="%s" x="%s" y="%.1f" fill="%s" font-size="%s" font-weight="%s"%s%s>%s</text>'
            % (cls, x, y, fill, size, weight, l, a, esc(s)))


def wrap(s, x, y, width_px, size, fill, weight=500, lh=1.55):
    cpl = max(10, int(width_px / (size * 0.505)))
    lines = textwrap.wrap(s, cpl)
    return ''.join(txt(x, y + i * size * lh, l, size, fill, weight) for i, l in enumerate(lines))


def eyebrow(y, s, col=BLUE, x=PAD):
    return txt(x, y, s, 13, col, 800, ls=2.6)


def headline(y, s, size=34, x=PAD):
    return txt(x, y, s, size, '#FFFFFF', 800, ls=-0.8)


def rule(y):
    return ('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-opacity=".55" stroke-width="1"/>'
            % (PAD, y, W - PAD, y, BORDER))


# ------------------------------------------------------------------ HERO
def hero():
    cx, cy, r, n = 1000, 196, 142, 300
    dots = []
    for i in range(n):
        yy = 1 - (i / (n - 1)) * 2
        rr = math.sqrt(max(0.0, 1 - yy * yy))
        th = math.pi * (3 - math.sqrt(5)) * i
        x, z = math.cos(th) * rr, math.sin(th) * rr
        depth = (z + 1) / 2
        op = round(0.14 + depth * 0.72, 3)
        col = BLUE if depth > 0.55 else ('#2E6FD0' if depth > 0.3 else '#1E3A5F')
        dur = round(2.4 + ((i * 7) % 11) * 0.42, 2)
        dots.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" fill-opacity="%s">'
                    '<animate attributeName="fill-opacity" values="%s;%s;%s" dur="%ss" '
                    'repeatCount="indefinite"/></circle>'
                    % (cx + x * r, cy + yy * r, round(0.7 + depth * 1.9, 2), col, op,
                       op, round(min(1, op * 1.9), 3), op, dur))
    b = '<rect width="%d" height="400" fill="url(#heroGlow)"/>' % W
    b += '<g>' + ''.join(dots) + '</g>'
    b += eyebrow(96, u'CUSTOM AI APPLICATIONS · AI AGENTS · RAG · AUTOMATION')
    b += txt(PAD - 2, 174, 'I Build AI Products', 60, '#FFFFFF', 800, ls=-1.6)
    b += txt(PAD - 2, 242, 'Around Your Business.', 60, BLUE, 800, ls=-1.6)
    b += txt(PAD, 288, u'Off-the-shelf AI is built for everyone, which means it’s built for no one.', 17, MUTED)
    b += txt(PAD, 314, u'I build the other kind — shaped around your process, your data, your tools.', 17, MUTED)
    b += '<g transform="translate(%d,336)">' % PAD
    b += '<rect width="212" height="36" rx="18" fill="url(#pill)"/>'
    b += txt(24, 23, 'sickteck.online', 13.5, '#FFFFFF', 700)
    b += txt(140, 23.5, u'→', 14, '#FFFFFF', 700)
    b += ('<g transform="translate(230,0)"><rect width="190" height="36" rx="18" fill="none" stroke="%s" '
          'stroke-opacity=".38"/><circle cx="25" cy="18" r="4.5" fill="%s">'
          '<animate attributeName="opacity" values="1;.25;1" dur="2.2s" repeatCount="indefinite"/></circle>'
          % (BLUE, GREEN))
    b += txt(39, 23, 'Available for projects', 13, LIGHT, 600) + '</g></g>'
    return 404, b


# ------------------------------------------------------------------ SERVICES
def services():
    cards = [
        ("01", "AI AGENTS", "Custom AI agents & assistants",
         u"Agents that do the work instead of talking about it — wired into your internal tools "
         u"through MCP and tool-calling, with a human in the loop on anything irreversible."),
        ("02", "RETRIEVAL", "RAG & document intelligence",
         u"Answers grounded in your own documents, with citations. Contract, invoice and report "
         u"extraction, plus semantic search across an internal knowledge base."),
        ("03", "AUTOMATION", "AI workflow automation",
         u"AI dropped into a process you already run — triage, classification, summarisation, "
         u"reporting. Measured against the manual baseline it replaces, not against a demo."),
        ("04", "VOICE", "Voice & meeting AI",
         u"Speech-to-text and multilingual transcription that runs fully offline when the audio "
         u"cannot leave the building. Automatic minutes, action items and summaries."),
    ]
    cw, ch, gap = 528, 212, 24
    b = eyebrow(64, 'WHAT I BUILD') + headline(110, 'Four things, built properly.')
    for i, (num, tag, title, desc) in enumerate(cards):
        x = PAD + (i % 2) * (cw + gap)
        y = 148 + (i // 2) * (ch + gap)
        accent = GREEN if i % 2 == 0 else BLUE
        b += '<g transform="translate(%d,%d)">' % (x, y)
        b += '<rect width="%d" height="%d" rx="16" fill="%s" stroke="%s"/>' % (cw, ch, CARD, BORDER)
        b += '<rect x="0" y="26" width="3.5" height="%d" rx="1.75" fill="%s" fill-opacity=".85"/>' % (ch - 52, accent)
        b += txt(30, 44, u'%s · %s' % (num, tag), 11.5, accent, 800, ls=2.2)
        b += txt(30, 80, title, 21.5, '#FFFFFF', 800, ls=-0.4)
        b += wrap(desc, 30, 112, cw - 62, 14.5, MUTED) + '</g>'
    return 148 + 2 * ch + gap + 40, b


# ------------------------------------------------------------------ PROCESS
def process():
    steps = [("01", "Discovery", "your process, your data"), ("02", "Prototype", "something working, fast"),
             ("03", "Build", "production system"), ("04", "Ship", "deployed + documented"),
             ("05", "Iterate", "tuned on real usage")]
    sw, sg = 204, 26
    x0 = (W - (len(steps) * sw + (len(steps) - 1) * sg)) // 2
    b = eyebrow(64, 'HOW WE WORK') + headline(110, 'You see it working early.')
    b += ('<line x1="%d" y1="206" x2="%d" y2="206" stroke="%s" stroke-opacity=".4" stroke-width="1.5" '
          'stroke-dasharray="5 6"/>' % (x0 + sw // 2, x0 + len(steps) * sw + (len(steps) - 1) * sg - sw // 2, BLUE))
    for i, (n, t, d) in enumerate(steps):
        b += '<g transform="translate(%d,150)">' % (x0 + i * (sw + sg))
        b += '<rect width="%d" height="112" rx="14" fill="%s" stroke="%s"/>' % (sw, CARD, BORDER)
        b += ('<rect x="24" y="20" width="40" height="22" rx="11" fill="%s" fill-opacity=".14" stroke="%s" '
              'stroke-opacity=".45"/>' % (BLUE, BLUE))
        b += txt(44, 35.5, n, 11.5, BLUE, 800, anchor='middle')
        b += txt(24, 72, t, 18, '#FFFFFF', 800, ls=-0.3)
        b += txt(24, 93, d, 12.5, DIM, 500) + '</g>'
    b += txt(PAD, 300, u"No six-month discovery phase. Every step after the prototype is a decision "
                       u"you get to make with real output in front of you.", 15.5, MUTED)
    return 336, b


# ------------------------------------------------------------------ STACK
def stack():
    groups = [(u"AI & MODELS", GREEN, ["Claude", "OpenAI", "MCP", "LangChain", "Ollama", "Hugging Face", "Whisper", "pgvector"]),
              (u"BACKEND", BLUE, ["Python", "FastAPI", "Go", "PostgreSQL", "Redis", "Docker", "GitHub Actions", "Linux"]),
              (u"FRONTEND & QA", BLUE, ["TypeScript", "React", "Vite", "Tailwind", "Node.js", "Playwright", "Vitest", "pytest"])]
    b = eyebrow(64, 'STACK') + headline(110, 'What I build with.')
    y = 158
    for gname, gcol, items in groups:
        b += txt(PAD, y, gname, 11.5, gcol, 800, ls=2)
        cx, cy = PAD, y + 16
        for it in items:
            w = int(len(it) * 8.1) + 36
            if cx + w > W - PAD:
                cx, cy = PAD, cy + 44
            b += '<g transform="translate(%d,%d)">' % (cx, cy)
            b += '<rect width="%d" height="34" rx="17" fill="%s" stroke="%s"/>' % (w, CARD, BORDER)
            b += '<circle cx="18" cy="17" r="3.5" fill="%s"/>' % gcol
            b += txt(29, 22, it, 13.5, LIGHT, 600) + '</g>'
            cx += w + 10
        y = cy + 34 + 40
    return y - 4, b


# ------------------------------------------------------------------ PROOF
def proof():
    items = [(u"Tested like infrastructure", u"3,277 statements at 100% line + branch coverage behind a hard CI gate — no exclusions — with mypy in strict mode and ruff clean on every commit."),
             (u"Designed before it’s built", u"17 component specs and 56 architecture diagrams written before the first line of code."),
             (u"Safe by default", u"Secrets envelope-encrypted at rest, append-only audit trails, idempotent writes, kill switches, human approval on every irreversible action."),
             (u"Yours at the end", u"Documented, containerised and handed over — no black box, no lock-in to me.")]
    cw, ch, gap = 528, 168, 24
    b = eyebrow(64, 'WHY CLIENTS KEEP ME')
    b += headline(110, 'AI that survives production.')
    b += txt(PAD, 144, u"Anyone can demo a prompt. The hard part is the system around it.", 15.5, MUTED)
    for i, (t, d) in enumerate(items):
        x = PAD + (i % 2) * (cw + gap)
        y = 176 + (i // 2) * (ch + gap)
        b += '<g transform="translate(%d,%d)">' % (x, y)
        b += '<rect width="%d" height="%d" rx="16" fill="%s" stroke="%s"/>' % (cw, ch, CARD, BORDER)
        b += ('<circle cx="46" cy="44" r="15" fill="%s" fill-opacity=".13"/>'
              '<path d="M39 44 l5 5 l9 -10" fill="none" stroke="%s" stroke-width="2.4" '
              'stroke-linecap="round" stroke-linejoin="round"/>' % (GREEN, GREEN))
        b += txt(74, 50, t, 18, '#FFFFFF', 800, ls=-0.3)
        b += wrap(d, 30, 92, cw - 62, 14, MUTED) + '</g>'
    return 176 + 2 * ch + gap + 40, b


# ------------------------------------------------------------------ CTA
def cta():
    b = eyebrow(70, 'WORK WITH ME')
    b += headline(120, u"Let’s build something.", 38)
    b += txt(PAD, 162, u"Got a process that should be automated, a document pile nobody reads,", 16.5, MUTED)
    b += txt(PAD, 188, u"or an AI idea you cannot buy off the shelf? Tell me about it.", 16.5, MUTED)
    b += '<g transform="translate(%d,220)">' % PAD
    b += '<rect width="228" height="46" rx="23" fill="url(#pill)"/>'
    b += txt(30, 29, 'Start a project', 15, '#FFFFFF', 700)
    b += txt(180, 29.5, u'→', 15, '#FFFFFF', 700)
    b += ('<g transform="translate(248,0)"><rect width="300" height="46" rx="23" fill="none" stroke="%s" '
          'stroke-opacity=".4"/>' % BLUE)
    b += txt(30, 29, 'saudikram@proclaw.online', 15, LIGHT, 600) + '</g></g>'
    b += txt(PAD, 310, u"Most recent work is under NDA — happy to walk through architecture and code in a call.",
             13.5, DIM)
    return 348, b


# ------------------------------------------------------------------ COMPOSE
sections = [hero(), services(), process(), stack(), proof(), cta()]
total = sum(h for h, _ in sections)

defs = ('<defs><style>'
        "@font-face{font-family:'Manrope';font-style:normal;font-weight:200 800;"
        "src:url(data:font/woff2;base64," + B64 + ") format('woff2');}"
        ".f{font-family:'Manrope','Segoe UI',system-ui,Helvetica,Arial,sans-serif;}"
        '</style>'
        '<linearGradient id="bg" x1="0" y1="0" x2="0.6" y2="1">'
        '<stop offset="0%" stop-color="' + BG + '"/><stop offset="45%" stop-color="' + DEEP + '"/>'
        '<stop offset="100%" stop-color="' + BG + '"/></linearGradient>'
        '<radialGradient id="hg" cx="0.78" cy="0.4" r="0.6">'
        '<stop offset="0%" stop-color="' + BLUE_D + '" stop-opacity=".3"/>'
        '<stop offset="100%" stop-color="' + BLUE_D + '" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="pill" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="' + BLUE_D + '"/><stop offset="100%" stop-color="' + BLUE + '"/>'
        '</linearGradient>'
        '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
        '<path d="M40 0H0V40" fill="none" stroke="' + BLUE + '" stroke-opacity=".05" stroke-width="1"/>'
        '</pattern>'
        '<rect id="heroGlowRect"/></defs>')
defs = defs.replace('<rect id="heroGlowRect"/>', '')
defs = defs.replace('id="hg"', 'id="heroGlow"')

out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
       'role="img" aria-label="Saud Ikram - I build AI products around your business">' % (W, total, W, total),
       defs,
       '<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, total),
       '<rect width="%d" height="%d" fill="url(#grid)"/>' % (W, total)]
y = 0
for i, (h, b) in enumerate(sections):
    out.append('<g transform="translate(0,%d)">%s</g>' % (y, b))
    y += h
    if i < len(sections) - 1:
        out.append(rule(y))
out.append('</svg>')

svg = ''.join(out)
p = os.path.join(A, 'profile.svg')
io.open(p, 'w', encoding='utf-8', newline='\n').write(svg)
print('profile.svg: %d bytes, %dx%d, %d sections' % (len(svg), W, total, len(sections)))
