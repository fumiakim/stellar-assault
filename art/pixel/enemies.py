from pal import mirror, show
from PIL import Image

# 敵は共通の記号でパレットを組む: a=明 b=暗 c=輪郭 d=発光/コア e=金属
def P(a,b,c,d,e='#9fb4c9'):
    return {'.':None,'a':a,'b':b,'c':c,'d':d,'e':e}

E = {}

# --- pop 雑魚（10x10・下向きの矢） ---
E['pop'] = (mirror([
 '.....',
 '..caa',
 '.caaa',
 'caaad',
 'caabd',
 '.cabb',
 '..cab',
 '...cb',
 '....c',
 '.....',
]), P('#ff9a5c','#c2551f','#40200f','#ffe6a8'))

# --- zig 中型（12x12・横に張り出した翼） ---
E['zig'] = (mirror([
 '......',
 '..ccaa',
 '.caaaa',
 'caaaad',
 'caabbd',
 'caabbd',
 'c.cabb',
 'cc.cab',
 '..ccab',
 '...cab',
 '....cb',
 '.....c',
]), P('#8affd1','#2c9c76','#0d3328','#eafff6'))

# --- dive 突撃機（12x12・菱形） ---
E['dive'] = (mirror([
 '...cc.',
 '..caaa',
 '.caaaa',
 'caaaad',
 'caaddd',
 'caaaad',
 'caaaab',
 '.cabbb',
 '..cabb',
 '...cab',
 '....cb',
 '.....c',
]), P('#ffd45c','#b8842a','#3d2a08','#fff4c8'))

# --- sniper 狙撃機（12x12・鋭い） ---
E['sniper'] = (mirror([
 '.....c',
 '....ca',
 '...caa',
 '..caaa',
 '.caaad',
 'caaaad',
 'caaaab',
 'c.caab',
 'cc.cab',
 '...cab',
 '...ccb',
 '.....c',
]), P('#c98aff','#6a3aa8','#251038','#f0dcff'))

# --- turret 砲台（14x14・円形） ---
E['turret'] = (mirror([
 '....cc.',
 '..cceee',
 '.ceeeee',
 '.ceeaaa',
 'ceeaaaa',
 'ceaaadd',
 'ceaadd d'.replace(' ',''),
 'ceaaddd',
 'ceaaaad',
 'ceeaaaa',
 '.ceeaaa',
 '.cceeee',
 '..ccee e'.replace(' ',''),
 '....cc.',
]), P('#9fd8ff','#3f6f96','#10202e','#ffe066','#7f9bb5'))

# --- mine 機雷（10x10・トゲつき） ---
E['mine'] = (mirror([
 '..c.c',
 '..cac',
 '.ccac',
 'ccaaa',
 '.caad',
 '.caad',
 'ccaaa',
 '.ccac',
 '..cac',
 '..c.c',
]), P('#ffe066','#a87f18','#3a2c05','#ff6a3b'))

# --- carrier 母艦（22x16） ---
E['carrier'] = (mirror([
 '...ccccccc',
 '..ceeeeeee',
 '.ceeaaaaaa',
 'ceeaaaaaaa',
 'ceaaaddaaa',
 'ceaaaddaaa',
 'ceaaaaaaaa',
 'ceaabbbbaa',
 'ceaabbbbaa',
 'ceaaaaaaaa',
 'ceaadd ddaa'.replace(' ',''),
 'ceaaaaaaaa',
 '.ceeaaaaaa',
 '..cceeeeee',
 '...ccccccc',
 '.....ccccc',
]), P('#7fa8ff','#2b4f96','#0c1830','#ffd166','#5c78a8'))

# --- heavy 重爆（20x16） ---
E['heavy'] = (mirror([
 '.....ccc c'.replace(' ',''),
 '...cceeee',
 '..ceeaaaa',
 '.ceaaaaaa',
 'ceaaaaddd',
 'ceaaaaddd',
 'ceaaaaaaa',
 'ceaabbbba',
 'ceaabbbba',
 'ceaaaaaaa',
 '.ceaaddaa',
 '.ceaaddaa',
 '..cceaaaa',
 '...cceeaa',
 '.....ccee',
 '.......cc',
]), P('#ff8fa8','#a03c58','#340f1c','#fff0a8','#c26a7c'))

# 幅チェック＋プレビュー
order = ['pop','zig','dive','sniper','mine','turret','carrier','heavy']
imgs = []
for k in order:
    rows, pal = E[k]
    w = len(rows[0])
    for i,r in enumerate(rows): assert len(r)==w, (k,i,len(r),w)
    show(rows, pal, 'e-%s.png' % k, zoom=8)
    imgs.append((k, rows, pal))

pad = 12
Wt = sum(len(r[0])*8 for _,r,_ in imgs) + pad*(len(imgs)+1)
Ht = max(len(r)*8 for _,r,_ in imgs) + 60
sheet = Image.new('RGB',(Wt,Ht),(14,20,32))
x = pad
from PIL import ImageDraw, ImageFont
d = ImageDraw.Draw(sheet)
try: f = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 13)
except Exception: f = ImageFont.load_default()
for k, rows, pal in imgs:
    im = Image.open('e-%s.png' % k)
    sheet.paste(im, (x, 24))
    small = show(rows, pal, '/tmp/s.png', zoom=1)
    sheet.paste(small, (x, Ht-24))
    d.text((x, 6), '%s %dx%d' % (k, len(rows[0]), len(rows)), fill=(150,200,255), font=f)
    x += im.width + pad
sheet.save('enemies-sheet.png')
print('ok', [(k, len(E[k][0][0]), len(E[k][0])) for k in order])
