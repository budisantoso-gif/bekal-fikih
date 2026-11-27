#!/usr/bin/env python3
"""Buat aset statis versi peserta: ikon, font lokal, QR.

Pakai:  python3 tools/make_assets.py [FONTSOURCE_NODE_MODULES] [URL]
- Ikon: bintang bersudut delapan (desain netral, bukan lambang lembaga mana pun).
- Font: salin woff2 dari paket npm @fontsource (lisensi SIL OFL 1.1):
    npm i @fontsource/amiri @fontsource/noto-naskh-arabic @fontsource/plus-jakarta-sans
- QR: tautan aplikasi.
"""
import math, os, shutil, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GREEN, GOLD = '#0F5C4A', '#FAC775'


def octagram(d, c, R, fill):
    for a in (math.pi / 4, 0):
        pts = [(c + R * math.cos(a + k * math.pi / 2), c + R * math.sin(a + k * math.pi / 2)) for k in range(4)]
        d.polygon(pts, fill=fill)


def icon(size, scale):
    S = size * 4
    im = Image.new('RGB', (S, S), GREEN)
    d = ImageDraw.Draw(im)
    c = S / 2
    R = S * scale
    octagram(d, c, R, GOLD)
    octagram(d, c, R * 0.55, GREEN)
    d.ellipse([c - R * 0.2, c - R * 0.2, c + R * 0.2, c + R * 0.2], fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)


def make_icons():
    out = os.path.join(ROOT, 'icons')
    os.makedirs(out, exist_ok=True)
    icon(192, 0.36).save(os.path.join(out, 'icon-192.png'), optimize=True)
    icon(512, 0.36).save(os.path.join(out, 'icon-512.png'), optimize=True)
    icon(512, 0.28).save(os.path.join(out, 'icon-maskable-512.png'), optimize=True)
    icon(180, 0.36).save(os.path.join(out, 'apple-touch-icon.png'), optimize=True)


FONTS = {
    'amiri-arabic-400.woff2': ('amiri', 'amiri-arabic-400-normal.woff2'),
    'amiri-arabic-700.woff2': ('amiri', 'amiri-arabic-700-normal.woff2'),
    'naskh-arabic-500.woff2': ('noto-naskh-arabic', 'noto-naskh-arabic-arabic-500-normal.woff2'),
    'naskh-arabic-600.woff2': ('noto-naskh-arabic', 'noto-naskh-arabic-arabic-600-normal.woff2'),
    'naskh-arabic-700.woff2': ('noto-naskh-arabic', 'noto-naskh-arabic-arabic-700-normal.woff2'),
}
for w in (400, 500, 700):
    FONTS['jakarta-latin-%d.woff2' % w] = ('plus-jakarta-sans', 'plus-jakarta-sans-latin-%d-normal.woff2' % w)
    FONTS['jakarta-latin-ext-%d.woff2' % w] = ('plus-jakarta-sans', 'plus-jakarta-sans-latin-ext-%d-normal.woff2' % w)


def copy_fonts(nm):
    out = os.path.join(ROOT, 'fonts')
    os.makedirs(out, exist_ok=True)
    for name, (pkg, f) in FONTS.items():
        shutil.copy(os.path.join(nm, '@fontsource', pkg, 'files', f), os.path.join(out, name))
    lic = os.path.join(nm, '@fontsource', 'amiri', 'LICENSE')
    # Teks lisensi OFL tiap keluarga font disertakan agar sesuai ketentuan lisensi.
    with open(os.path.join(out, 'LICENSES.txt'), 'w', encoding='utf-8') as fh:
        for pkg in ('amiri', 'noto-naskh-arabic', 'plus-jakarta-sans'):
            p = os.path.join(nm, '@fontsource', pkg, 'LICENSE')
            fh.write('=== %s ===\n' % pkg)
            fh.write(open(p, encoding='utf-8').read())
            fh.write('\n\n')


def make_qr(url):
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=16, border=4)
    q.add_data(url)
    q.make(fit=True)
    os.makedirs(os.path.join(ROOT, 'qr'), exist_ok=True)
    q.make_image(fill_color='black', back_color='white').save(os.path.join(ROOT, 'qr', 'qr-peserta.png'))


if __name__ == '__main__':
    make_icons()
    if len(sys.argv) > 1:
        copy_fonts(sys.argv[1])
    make_qr(sys.argv[2] if len(sys.argv) > 2 else 'https://budisantoso-gif.github.io/bekal-fikih/')
    print('ok')
