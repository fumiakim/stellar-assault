#!/usr/bin/env python3
"""全ステージ分の背景タイルを作り、ゲーム画面のモックで見え方を確認する。"""
import subprocess, sys
sys.path.insert(0, '../pixel')
from PIL import Image, ImageDraw, ImageFont
from pal import PAL, SWAP_2P
from ship import SHIP

# 面ごとの 暗さ / 彩度ダウン（明るいほど数字が大きい）
STAGES = [
    ('sky',      0.46, 0.20),
    ('sea',      0.62, 0.40),
    ('canyon',   0.58, 0.45),
    ('city',     0.60, 0.38),
    ('fortress', 0.58, 0.38),
]
PW, PH = 192, 256

def sprite_img(rows, pal):
    w,h = len(rows[0]), len(rows)
    im = Image.new('RGBA',(w,h),(0,0,0,0)); p = im.load()
    for y,r in enumerate(rows):
        for x,ch in enumerate(r):
            c = pal.get(ch)
            if c: p[x,y] = tuple(int(c[i:i+2],16) for i in (1,3,5)) + (255,)
    return im

BALL = ['.####.','#%%%%#','#%00%#','#%00%#','#%%%%#','.####.']
def mock(bg):
    im = bg.copy(); d = ImageDraw.Draw(im)
    p2 = dict(PAL); p2.update(SWAP_2P)
    s1, s2 = sprite_img(SHIP, PAL), sprite_img(SHIP, p2)
    im.paste(s1,(70,200),s1); im.paste(s2,(106,200),s2)
    for i,x0 in enumerate([76,112]):
        col = (95,216,255) if i==0 else (255,177,95)
        for y in range(60,200,14):
            d.rectangle([x0,y,x0+1,y+9], fill=col); d.rectangle([x0,y+2,x0+1,y+5], fill=(255,255,255))
    for (bx,by,c) in [(40,90,(255,90,224)),(150,120,(255,207,74)),(60,150,(127,224,255)),
                      (128,70,(255,90,224)),(96,160,(255,207,74)),(30,180,(127,224,255))]:
        for yy,row in enumerate(BALL):
            for xx,ch in enumerate(row):
                if ch=='#': im.putpixel((bx+xx,by+yy),(8,12,20))
                elif ch=='%': im.putpixel((bx+xx,by+yy),c)
                elif ch=='0': im.putpixel((bx+xx,by+yy),(255,255,255))
    d.rectangle([0,0,PW-1,17], fill=(5,9,18)); d.rectangle([0,17,PW-1,17], fill=(44,90,140))
    return im

mocks = []
for name, dk, ds in STAGES:
    subprocess.run(['python3','make-bg.py',name,str(dk),str(ds)], check=True)
    mocks.append((name, mock(Image.open('%s-0.png' % name).convert('RGB'))))

Z = 2
sheet = Image.new('RGB',(len(mocks)*(PW*Z+12)+12, PH*Z+40),(12,14,20))
d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 14)
except Exception: f = ImageFont.load_default()
for i,(name,im) in enumerate(mocks):
    x = 12 + i*(PW*Z+12)
    sheet.paste(im.resize((PW*Z,PH*Z), Image.NEAREST),(x,28))
    d.text((x,8), '%s  (%.2f / %.2f)' % (name, STAGES[i][1], STAGES[i][2]), fill=(150,200,255), font=f)
sheet.save('all-mock.png'); print('all-mock.png', sheet.size)
