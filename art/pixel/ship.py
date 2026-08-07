from pal import PAL, SWAP_2P, mirror, show
# 左半分8列（col0=左端 / col7=中心左）→ 鏡像で16列
SHIP_L = [
 '.......1',   # 0  機首
 '.......1',   # 1
 '......21',   # 2
 '......11',   # 3
 '.....216',   # 4  キャノピー
 '.....216',   # 5
 '.....211',   # 6
 '...22211',   # 7  主翼つけ根
 '..244411',   # 8
 '.2444411',   # 9
 '.2445511',   # 10
 '..22.511',   # 11 主翼後縁
 '.....211',   # 12
 '.....231',   # 13
 '.....273',   # 14 ノズル
 '......7.',   # 15
]
SHIP = mirror(SHIP_L)
for i, r in enumerate(SHIP): assert len(r) == 16, (i, len(r))
show(SHIP, PAL, 'ship1p.png')
p2 = dict(PAL); p2.update(SWAP_2P)
show(SHIP, p2, 'ship2p.png')
# 並べて比較（実寸も）
from PIL import Image
a = Image.open('ship1p.png'); b = Image.open('ship2p.png')
sheet = Image.new('RGB', (a.width*2+60, a.height+40), (18,26,40))
sheet.paste(a,(10,10)); sheet.paste(b,(a.width+40,10))
s1 = show(SHIP, PAL, '/tmp/x.png', zoom=1); s2 = show(SHIP, p2, '/tmp/y.png', zoom=1)
sheet.paste(s1.resize((16,16), Image.NEAREST), (10, a.height+16))
sheet.paste(s2.resize((16,16), Image.NEAREST), (40, a.height+16))
sheet.save('ship-sheet.png')
print('\n'.join(SHIP))
