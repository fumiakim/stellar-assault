#!/usr/bin/env python3
"""生成画像を、縦にループするドット絵の背景タイルに変換する。

  1. 面積平均で 192x256 に縮小（1ドット=1ピクセルを保証）
  2. 彩度と輝度を落とす（自機と弾が埋もれないように）
  3. 3枚を縦に積んで、タイル間と上下の折り返しの継ぎ目をクロスブレンド
  4. 3枚まとめて減色（＝共通パレット。タイルごとに色が変わるのを防ぐ）
  5. 1枚ずつ書き出す

    python3 make-bg.py canyon 0.42 0.55
"""
import sys
from PIL import Image

PW, PH = 192, 256
SEAM = 24            # 継ぎ目をブレンドする幅
COLORS = 24

def load(src, darken, desat):
    im = Image.open(src).convert('RGB').resize((PW, PH), Image.BOX)
    p = im.load()
    for y in range(PH):
        for x in range(PW):
            r,g,b = p[x,y]
            l = r*0.30 + g*0.59 + b*0.11
            p[x,y] = (min(255,int((r*(1-desat)+l*desat)*darken)),
                      min(255,int((g*(1-desat)+l*desat)*darken)),
                      min(255,int((b*(1-desat)+l*desat)*darken)))
    return im

def blend_seam(strip, y):
    """y を境にした継ぎ目を上下 SEAM/2 にわたって混ぜる（y は strip 内の位置）"""
    p = strip.load(); H = strip.height
    for i in range(SEAM):
        a = i/(SEAM-1)                      # 0→1
        ya = (y - SEAM//2 + i) % H
        yb = (y + SEAM//2 - i - 1) % H
        for x in range(PW):
            ca, cb = p[x,ya], p[x,yb]
            p[x,ya] = tuple(int(ca[c]*(1-a*0.5) + cb[c]*(a*0.5)) for c in range(3))
            p[x,yb] = tuple(int(cb[c]*(1-a*0.5) + ca[c]*(a*0.5)) for c in range(3))

def main():
    name   = sys.argv[1] if len(sys.argv) > 1 else 'canyon'
    darken = float(sys.argv[2]) if len(sys.argv) > 2 else 0.42
    desat  = float(sys.argv[3]) if len(sys.argv) > 3 else 0.55
    tiles = [load('raw-%s-%d.png' % (name, i), darken, desat) for i in range(3)]

    strip = Image.new('RGB', (PW, PH*len(tiles)))
    for i,t in enumerate(tiles): strip.paste(t, (0, i*PH))
    for i in range(len(tiles)): blend_seam(strip, i*PH)      # 0（＝折り返し）と各タイル境

    strip = strip.quantize(colors=COLORS, method=Image.MEDIANCUT, dither=Image.NONE).convert('RGB')
    for i in range(len(tiles)):
        out = strip.crop((0, i*PH, PW, (i+1)*PH))
        out.save('%s-%d.png' % (name, i), optimize=True)
    strip.resize((PW*2, strip.height*2), Image.NEAREST).save('%s-strip.png' % name)
    print('%s: %d tiles, %dx%d each, %d colors' % (name, len(tiles), PW, PH, len(strip.getcolors(65536))))

main()
