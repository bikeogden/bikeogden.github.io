#!/usr/bin/env python3
"""Build the Ogden Bike Bus flyer as a print-ready Letter PDF."""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from owl import draw_owl

F = '/mnt/skills/examples/canvas-design/canvas-fonts'
pdfmetrics.registerFont(TTFont('Bric',     f'{F}/BricolageGrotesque-Bold.ttf'))
pdfmetrics.registerFont(TTFont('BricReg',  f'{F}/BricolageGrotesque-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Body',     f'{F}/WorkSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('BodyBold', f'{F}/WorkSans-Bold.ttf'))

INK      = (20/255, 33/255, 61/255)
INK_SOFT = (74/255, 85/255, 120/255)
PAPER    = (251/255, 250/255, 247/255)
LANE     = (0, 122/255, 61/255)
RULE     = (223/255, 220/255, 216/255)

W, H = letter
M    = 52                      # side margin
CX   = W/2
ASSETS = os.path.join(os.path.dirname(__file__), '..', 'bikeogden', 'assets')

STOPS = [
    ('8:00am', 'Kingsbury & Illinois', 'by the East Bank Club'),
    ('8:04am', 'Kingsbury & Erie',     ''),
    ('8:06am', 'Erie & Orleans',       ''),
    ('8:09am', 'Erie & Wells',         ''),
    ('8:13am', 'Erie & Dearborn',      'riders from the east join here'),
    ('8:16am', 'Dearborn & Chicago',   ''),
    ('8:20am', 'Ogden East Campus',    ''),
]


def wrap(c, text, font, size, maxw):
    c.setFont(font, size)
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if c.stringWidth(t, font, size) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines


def build(out_path):
    c = canvas.Canvas(out_path, pagesize=letter)
    c.setTitle('Ogden Bike Bus')

    c.setFillColorRGB(*PAPER); c.rect(0, 0, W, H, stroke=0, fill=1)
    c.setFillColorRGB(*LANE);  c.rect(0, H-13, W, 13, stroke=0, fill=1)

    y = H - 13 - 26

    # ---- owl ----
    owl = draw_owl(600)
    ow = 62; oh = ow * owl.height / owl.width
    c.drawImage(ImageReader(owl), CX - ow/2, y - oh, ow, oh, mask='auto')
    y -= oh + 16

    # ---- wordmark ----
    c.setFillColorRGB(*INK); c.setFont('Bric', 44)
    c.drawCentredString(CX, y - 34, 'Ogden Bike Bus')
    y -= 44

    c.setFillColorRGB(*INK_SOFT); c.setFont('Body', 11.5)
    c.drawCentredString(CX, y - 12,
        'The Ogden International School of Chicago  \u00b7  East and Jenner campuses')
    y -= 44

    # ---- call ----
    c.setFillColorRGB(*INK); c.setFont('Bric', 27)
    c.drawCentredString(CX, y - 22, 'Come ride to school with us!')
    y -= 40

    body = ('We ride every Friday school is open, in almost any weather. Bikes, '
            'scooters and trailers all welcome \u2014 and there\u2019s music. Adults '
            'ride at the front, the back and every turn.')
    c.setFillColorRGB(*INK_SOFT)
    for line in wrap(c, body, 'Body', 12.5, W - 2*M - 90):
        c.setFont('Body', 12.5)
        c.drawCentredString(CX, y, line); y -= 17.5
    y -= 20

    # ---- schedule ----
    c.setStrokeColorRGB(*RULE); c.setLineWidth(0.8)
    c.line(M, y, W-M, y); y -= 20

    c.setFillColorRGB(*INK); c.setFont('Bric', 15)
    c.drawCentredString(CX, y, 'Friday route'); y -= 21

    tx = M + 74
    for t, place, note in STOPS:
        c.setFillColorRGB(*INK); c.setFont('BodyBold', 12)
        c.drawString(tx, y, t)
        c.setFont('Body', 12)
        c.drawString(tx + 62, y, place)
        if note:
            w = c.stringWidth(place, 'Body', 12)
            c.setFillColorRGB(*INK_SOFT); c.setFont('Body', 10.5)
            c.drawString(tx + 62 + w + 7, y, '\u2014 ' + note)
        y -= 17.5

    y -= 4
    c.setFillColorRGB(*INK_SOFT); c.setFont('Body', 11)
    c.drawCentredString(CX, y,
        'Middle schoolers carry on to Jenner, leaving East Campus 8:30 and arriving 8:40.')
    y -= 16
    c.setStrokeColorRGB(*RULE); c.line(M, y, W-M, y)
    y -= 24

    # ---- QR codes ----
    qr = 138
    gap = 56
    total = qr*2 + gap
    x0 = CX - total/2
    codes = [
        (os.path.join(ASSETS, 'qr-whatsapp.png'), 'Parent riders group',
         ['Weather calls, route changes', 'and day-of updates on WhatsApp']),
        (os.path.join(ASSETS, 'qr-site.png'), 'Route, times & FAQs',
         ['Maps, rules, what to expect', 'bikeogden.github.io']),
    ]
    for i, (path, label, subs) in enumerate(codes):
        x = x0 + i*(qr+gap)
        c.drawImage(path, x, y - qr, qr, qr)
        ty = y - qr - 17
        c.setFillColorRGB(*INK); c.setFont('Bric', 13.5)
        c.drawCentredString(x + qr/2, ty, label)
        c.setFillColorRGB(*INK_SOFT); c.setFont('Body', 10)
        for s in subs:
            ty -= 13
            c.drawCentredString(x + qr/2, ty, s)

    # ---- footer ----
    fy = 52
    c.setStrokeColorRGB(*RULE); c.line(M, fy + 18, W-M, fy + 18)
    c.setFillColorRGB(*INK); c.setFont('BodyBold', 10.5)
    lead = 'Never done this before?'
    c.drawString(M, fy, lead)
    c.setFillColorRGB(*INK_SOFT); c.setFont('Body', 10.5)
    c.drawString(M + c.stringWidth(lead, 'BodyBold', 10.5) + 4, fy,
                 'Just turn up at any stop. No sign-up.')
    c.setFont('Body', 10.5)
    c.drawRightString(W-M, fy, 'bikeogden.github.io')

    c.showPage()
    c.save()
    return out_path


if __name__ == '__main__':
    p = build('flyer.pdf')
    print('wrote', p, os.path.getsize(p)//1024, 'KB')
