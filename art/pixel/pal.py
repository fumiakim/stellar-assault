# 共通パレット（ドット絵）
PAL = {
 '.': None,
 '3': '#1a2432',   # 輪郭・影
 '2': '#5c7590',   # 機体（陰）
 '1': '#d8e6f2',   # 機体（明）
 '0': '#ffffff',   # ハイライト
 '4': '#2a6fd0',   # 翼（1P）
 '5': '#17427f',   # 翼（1P・陰）
 '6': '#4ff0ff',   # キャノピー
 '7': '#ffcf4a',   # 発光
}
SWAP_2P = {'4':'#e0741c', '5':'#8a3d08', '6':'#ffd24a'}

def mirror(left):
    """左半分（中心列を含む）を鏡像化して全幅にする"""
    return [l + l[::-1] for l in left]

def show(rows, pal, name, zoom=12, bg=(18,26,40)):
    from PIL import Image
    w, h = len(rows[0]), len(rows)
    im = Image.new('RGB', (w, h), bg)
    p = im.load()
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            c = pal.get(ch)
            if c:
                p[x, y] = tuple(int(c[i:i+2], 16) for i in (1, 3, 5))
    im = im.resize((w*zoom, h*zoom), Image.NEAREST)
    im.save(name)
    return im
