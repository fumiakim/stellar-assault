#!/usr/bin/env python3
"""ship-1p.png を p1-a0.png から作り直すスクリプト。

Replicate（black-forest-labs/flux-schnell）で生成した p1-a0.png は
「純黒に近い背景の上に置かれた自機」なので、次の手順で透過スプライトにする。

  1. 明るい部分を機体とみなすマスクを作る
  2. 画像の外周からフラッドフィルして「外側の背景」だけを特定する
     （翼の内側にある濃紺のパネルは囲まれているため塗られず、不透明のまま残る）
  3. 外側は輝度に応じたアルファにしてアンチエイリアスを保つ。
     生成画像の背景は真っ黒ではなく輝度11程度あるので、BLACK でその分を切る
  4. 機体だけを切り出す。エンジンの炎はゲーム側で毎フレーム揺らして描くため含めない
  5. 孤立したノイズ片を消す

    python3 make-sprite.py
"""
from collections import deque
from PIL import Image, ImageDraw

SRC, DST = 'p1-a0.png', 'ship-1p.png'
TH        = 26              # 機体とみなす輝度
BLACK     = 15              # 背景の黒レベル（これ以下は完全透過）
RAMP      = 34              # アンチエイリアスの立ち上がり幅
HULL_BOX  = (163, 222, 862, 654)   # 機体だけを切り出す範囲（炎は除外）
OUT_WIDTH = 256

src = Image.open(SRC).convert('RGB')
W, H = src.size
px = src.load()

mask = Image.new('L', (W, H), 0)
mp = mask.load()
for y in range(H):
    for x in range(W):
        if max(px[x, y]) > TH:
            mp[x, y] = 255

fill = mask.copy()
for seed in [(0, 0), (W - 1, 0), (0, H - 1), (W - 1, H - 1),
             (W // 2, 0), (W // 2, H - 1), (0, H // 2), (W - 1, H // 2)]:
    if fill.getpixel(seed) == 0:
        ImageDraw.floodfill(fill, seed, 128)
fp = fill.load()

out = Image.new('RGBA', (W, H))
op = out.load()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if fp[x, y] == 128:                      # 外側の背景
            lum = max(r, g, b)
            a = 0 if lum <= BLACK else min(255, int((lum - BLACK) * 255 / RAMP))
        else:                                    # 機体の内側
            a = 255
        op[x, y] = (r, g, b, a)

hull = out.crop(HULL_BOX)
hull = hull.resize((OUT_WIDTH, round(OUT_WIDTH * hull.height / hull.width)), Image.LANCZOS)

# 最大の連結成分（＝機体）だけ残す
w, h = hull.size
p = hull.load()
seen = [[False] * h for _ in range(w)]
best, best_size = None, 0
for sy in range(h):
    for sx in range(w):
        if seen[sx][sy] or p[sx, sy][3] < 10:
            continue
        q = deque([(sx, sy)])
        seen[sx][sy] = True
        comp = []
        while q:
            x, y = q.popleft()
            comp.append((x, y))
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and not seen[nx][ny] and p[nx, ny][3] >= 10:
                    seen[nx][ny] = True
                    q.append((nx, ny))
        if len(comp) > best_size:
            best, best_size = comp, len(comp)

keep = set(best)
for y in range(h):
    for x in range(w):
        if p[x, y][3] > 0 and (x, y) not in keep:
            r, g, b, _ = p[x, y]
            p[x, y] = (r, g, b, 0)

hull.save(DST)
print('%s -> %s  %dx%d' % (SRC, DST, w, h))
