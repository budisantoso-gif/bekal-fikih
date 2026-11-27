#!/usr/bin/env python3
"""Poster QR A4 (300 dpi) -> qr/poster-qr-a4.png dan .pdf"""
import os, qrcode
from PIL import Image, ImageDraw, ImageFont
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL='https://budisantoso-gif.github.io/bekal-fikih/'
W,H=2480,3508
GREEN,GOLD,INK='#0F5C4A','#FAC775','#1F2A37'
F='/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf'
def font(sz,b=False): return ImageFont.truetype(F%('-Bold' if b else ''),sz)
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
d.rectangle([0,0,W,520],fill=GREEN)
def center(t,y,f,fill):
    w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=fill)
icon=Image.open(os.path.join(ROOT,'icons','icon-512.png')).resize((260,260))
im.paste(icon,((W-260)//2,70))
center('Bekal Fikih',360,font(110,True),'white')
center('Pindai untuk membuka aplikasi',640,font(80,True),INK)
q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_Q,box_size=1,border=4)
q.add_data(URL);q.make(fit=True)
n=len(q.get_matrix()); bs=1500//n
qi=q.make_image(fill_color='black',back_color='white').convert('RGB').resize((n*bs,n*bs),Image.NEAREST)
im.paste(qi,((W-qi.width)//2,820))
y=820+qi.height+60
center(URL.replace('https://',''),y,font(62,True),GREEN)
steps=['1. Buka tautan ini saat ada sinyal (cukup sekali).',
 '2. Setelah terbuka, aplikasi bisa dipakai tanpa sinyal.',
 '3. Agar mudah dibuka lagi: pilih "Tambahkan ke layar utama"',
 '    (Chrome: menu ⋮ · Safari: tombol Bagikan).']
y+=170
for s in steps:
    d.text((300,y),s,font=font(64),fill=INK); y+=100
d.rounded_rectangle([300,y+60,W-300,y+330],radius=36,fill='#FFF1CC',outline='#E8C766',width=4)
d.text((360,y+95),'Belum direview ustadz',font=font(66,True),fill='#4A3500')
d.text((360,y+190),'Rujukan utama tetap penjelasan ustadz dan kitabnya.',font=font(54),fill='#4A3500')
im.save(os.path.join(ROOT,'qr','poster-qr-a4.png'),dpi=(300,300))
im.save(os.path.join(ROOT,'qr','poster-qr-a4.pdf'),resolution=300)
