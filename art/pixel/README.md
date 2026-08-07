# ドット絵の設計データ

`index.html` に埋め込まれているスプライトの元データです。ここで設計し、
`gen.py` が JavaScript の定義（`sprites.js`）を吐き出します。

| ファイル | 内容 |
|---|---|
| `pal.py`     | 共通パレットと、左半分から鏡像を作るヘルパ |
| `ship.py`    | 自機（16×16）。1P と 2P は色の差し替えのみ |
| `enemies.py` | 雑魚敵8種（pop / zig / dive / sniper / mine / turret / carrier / heavy） |
| `gen.py`     | 上記から `sprites.js` を生成 |
| `sprites.js` | 生成物。`index.html` にそのまま貼り込んである |

スプライトは文字列の配列で、1文字＝1ドット、`.` が透明です。
色を変えるならパレットだけ、形を変えるなら文字列を直せば済みます。

```bash
python3 gen.py        # sprites.js を作り直す
python3 ship.py       # 自機を ship1p.png / ship2p.png に拡大プレビュー
python3 enemies.py    # 敵一覧を enemies-sheet.png にプレビュー
```

生成し直したら `sprites.js` の中身を `index.html` の
「ドット絵スプライト定義」ブロックに貼り替えてください。

ボス5体・背景・爆発は文字列スプライトではなく、`index.html` 内で
整数座標の矩形（`rct` / `disc` / `oval`）を組み合わせて描いています。
