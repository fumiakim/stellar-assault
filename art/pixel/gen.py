import json
from pal import PAL, SWAP_2P, mirror
import enemies as EN  # 定義を再利用（副作用でプレビューも出るが問題なし）
from ship import SHIP

def js_rows(rows):
    return '[' + ','.join("'%s'" % r for r in rows) + ']'
def js_pal(pal):
    items = []
    for k, v in pal.items():
        if v is None: continue
        items.append("'%s':'%s'" % (k, v))
    return '{' + ','.join(items) + '}'

out = []
out.append('/* --- ドット絵スプライト定義（art/pixel/ で設計） --- */')
out.append('const PAL_SHIP = %s;' % js_pal(PAL))
out.append('const ROWS_SHIP = %s;' % js_rows(SHIP))
out.append('const SP = {};')
out.append('SP.ship1 = spr(ROWS_SHIP, PAL_SHIP);')
out.append('SP.ship2 = recolor(ROWS_SHIP, PAL_SHIP, %s);' % js_pal(SWAP_2P))
for k in ['pop','zig','dive','sniper','mine','turret','carrier','heavy']:
    rows, pal = EN.E[k]
    out.append("SP.%s = spr(%s, %s);" % (k, js_rows(rows), js_pal(pal)))
out.append('// 被弾時に光らせる白抜き版')
out.append("for (const k in SP) SP[k + 'W'] = whiteOf(SP[k]);")
open('sprites.js','w').write('\n'.join(out) + '\n')
print('sprites.js', len('\n'.join(out)), 'chars')
