# 生成した背景タイル

外部の画像生成（Replicate / `black-forest-labs/flux-schnell`）で「真上からの俯瞰」を作り、
後処理でドットグリッドに乗せ直したものです。生成そのままでは、ピクセルがグリッドに揃わず・
アンチエイリアスがかかり・色数が数千あるため、手描きのスプライトと並べると必ず浮きます。

## 後処理（make-bg.py）

1. **面積平均で 192×256 へ縮小** — この時点で 1ドット = 1ピクセルが保証される
2. **輝度と彩度を落とす** — 自機と弾が背景に埋もれないようにする（面ごとに調整）
3. **3枚を縦に積み、継ぎ目を狭くクロスディゾルブしてから暗く落とす**
   別々に生成した絵をただ混ぜると白っぽい帯が出るので、影を通過したように見せて隠す
4. **3枚まとめて24色に減色（ディザなし）** — 共通パレットになりタイル間で色が飛ばない

```bash
python3 make-all.py          # 全5面ぶんを作り直し、確認用モックも出力
python3 make-bg.py sky 0.46 0.20   # 個別（名前 暗さ 彩度ダウン）
```

面ごとの設定値は `make-all.py` の `STAGES` にあります。

| 面 | 名前 | 暗さ / 彩度ダウン |
|---|---|---|
| 1 | `sky` | 0.46 / 0.20 |
| 2 | `sea` | 0.62 / 0.40 |
| 3 | `canyon` | 0.58 / 0.45 |
| 4 | `city` | 0.60 / 0.38 |
| 5 | `fortress` | 0.58 / 0.38 |

## ゲーム側

`loadBGTiles(面番号, '名前', 3)` で登録します。3枚で 768 ドット分＝約3画面ぶんで一周します。
**読み込みに失敗した面は、これまでどおり手続き的な描画にフォールバック**するので、
PNG がなくてもゲームは動きます。画像の上には、動きのある近景
（鳥・波のきらめき・土煙・サーチライト・導管を流れる光）だけを手描きで重ねています。

## 生成に使ったプロンプト

`raw-*.png`（生成そのままの1024×1024）はサイズが大きいのでコミットしていません。
作り直す場合は以下で生成し、`raw-<名前>-0..2.png` として置いてください。
いずれも `num_outputs: 3, aspect_ratio: "1:1", output_format: "png", num_inference_steps: 4`。

- **sky** (seed 2201) — Top-down aerial view looking straight down through a broken layer of clouds, dark blue sea far below visible through the gaps between clouds, wispy cloud tops, twilight, 16-bit era pixel art game background, chunky visible pixels, limited palette of deep blues and pale grey clouds, flat even lighting, no characters, no aircraft, no text
- **sea** (seed 3312) — Top-down aerial view looking straight down at a dark tropical ocean, scattered small islands with sandy beaches and green vegetation, coral reefs in shallow turquoise water, white foam around the shores, deep navy open water, 16-bit era pixel art game background, chunky visible pixels, limited palette of deep blues and teals, flat even lighting, no boats, no characters, no text
- **canyon** (seed 5150) — Top-down aerial view looking straight down at a deep red rock canyon, a winding dry riverbed running vertically down the middle, layered rock strata on both cliff walls, scattered boulders and rubble on the canyon floor, thin glowing lava cracks, 16-bit era pixel art game background, chunky visible pixels, limited palette of dark browns and rust reds, flat even lighting, no characters, no vehicles, no text
- **city** (seed 4423) — Top-down aerial view looking straight down at a dense night city, illuminated skyscraper rooftops, glowing street grid, elevated highways with light trails, dark navy and cyan color scheme, tiny warm window lights, rooftop helipads, 16-bit era pixel art game background, chunky visible pixels, limited dark palette, flat even lighting, no characters, no text
- **fortress** (seed 5534) — Top-down aerial view looking straight down at the armored outer surface of a vast alien space fortress, interlocking metal plates, glowing energy conduits, ventilation grilles and machinery, hazard stripes, antenna arrays, dark steel blue with cyan and amber glow, 16-bit era pixel art game background, chunky visible pixels, limited dark palette, flat even lighting, no characters, no ships, no text
