# 生成した背景タイル

外部の画像生成（Replicate / `black-forest-labs/flux-schnell`）で「真上からの俯瞰」を作り、
後処理でドットグリッドに乗せ直したものです。生成そのままでは、
ピクセルがグリッドに揃わず・アンチエイリアスがかかり・色数が数千あるため、
手描きのスプライトと並べると必ず浮きます。次の工程で本物のドット絵にしています。

1. **面積平均で 192×256 へ縮小** — この時点で 1ドット = 1ピクセルが保証される
2. **輝度と彩度を落とす** — 自機と弾が背景に埋もれないようにする
3. **3枚を縦に積んで継ぎ目をクロスブレンド** — 縦スクロールでループできるようにする
4. **3枚まとめて減色（24色・ディザなし）** — 共通パレットになり、タイル間で色が飛ばない

```bash
python3 make-bg.py canyon 0.42 0.55     # 暗さ 0.42 / 彩度ダウン 0.55
```

`raw-<名前>-0..2.png` を読んで `<名前>-0..2.png` を書き出します。
確認用に `<名前>-strip.png`（3枚を縦に繋いだ2倍表示）も出ます。

| ファイル | 内容 |
|---|---|
| `raw-canyon-0..2.png` | 生成そのまま（1024×1024） |
| `canyon-0..2.png` | ゲームが読む背景タイル（192×256・24色） |
| `make-bg.py` | 変換スクリプト |

ゲーム側は `loadBGTiles(面番号, '名前', 枚数)` で登録します。
**読み込みに失敗した面は、これまでどおり手続き的な描画にフォールバック**するので、
PNG がなくてもゲームは動きます。

生成に使ったプロンプト（3面・峡谷）:

> Top-down aerial view looking straight down at a deep red rock canyon,
> a winding dry riverbed running vertically down the middle, layered rock strata
> on both cliff walls, scattered boulders and rubble on the canyon floor,
> thin glowing lava cracks, 16-bit era pixel art game background,
> chunky visible pixels, limited palette of dark browns and rust reds,
> flat even lighting, no characters, no vehicles, no text
