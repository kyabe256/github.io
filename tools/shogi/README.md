# 将棋原論 — 生成系

将棋の教科書 PDF（`shogi-genron.pdf`）を生成するための一式。原稿・図面・演習問題を
すべてプログラムから組み立て、将棋のルールに関わる部分は機械的に検証している。

## 構成

| ファイル | 役割 |
|---|---|
| `shogi.py` | 盤面表現、合法手生成、王手・詰み判定、詰将棋の完全探索、日本語の棋譜表記 |
| `kifu.py` | 定跡手順（USI 形式）の登録と合法性検証。局面図はここから生成する |
| `gen_tsume.py` | 詰将棋の自動生成。指定手数ちょうど・余詰なしの問題だけを採用する |
| `gen_hisshi.py` | 一手必至問題の自動生成。全ての受けに詰みがあることを確認する |
| `find_mate.py` | 囲いを崩した実戦形で詰みが成立する配置を探索する |
| `bookgen.py` | 軽量マークアップ（`content/*.txt`）から HTML を組み立てる |
| `book.css` | 組版（JIS B5、明朝本文、盤面図、目次、索引） |
| `render.js` | Chromium（Playwright）で HTML を PDF に印刷する |
| `build.py` | 頁番号を確定させるための複数パス・ビルド |

## 検証

```python
import shogi
p = shogi.Position.from_sfen("lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1")

def perft(pos, d):
    return 1 if d == 0 else sum(perft(pos.do(m), d - 1) for m in pos.legal_moves())

print([perft(p, d) for d in (1, 2, 3)])   # -> [30, 900, 25470]
```

深さ 4 は 719731。いずれも公表値と一致する。

## ビルド

必要なもの: Python 3.11、Node.js、`playwright`（Chromium）、`pypdf`、日本語フォント。

```
$ python3 gen_tsume.py '{"1":12,"3":32,"5":32,"7":20}' 2100   # 詰将棋を生成（時間がかかる）
$ python3 gen_hisshi.py 6 800                                  # 必至問題を生成
$ python3 build.py ../../shogi-genron.pdf                       # PDF を出力
```

`build.py` は次の手順で頁番号を確定する。

1. 見出し・図・用語の初出位置に不可視マーカーを埋め込んで PDF を出力する。
2. `pypdf` で PDF を読み、各マーカーが載った頁を取得する。
3. 目次・索引・相互参照に頁番号を流し込んで再出力し、頁割りが変わっていないことを確認する。

フォントの場所は環境変数 `SHOGI_SCRATCH` 配下の `fonts/` を見る（Noto Serif JP / Noto Sans JP）。

## マークアップ

`content/*.txt` で使える記法。

```
@part I | 部のタイトル | リード文
# 章タイトル      ## 節      ### 小見出し
@h1 番号なしの章   @apx A | 付録タイトル
@board <SFEN> | 図の説明 | hl=76,34        盤面図（網掛けの升を指定できる）
@mate  <SFEN> | 図の説明                   詰み形（ビルド時に詰みを検証する）
@mateline <SFEN> | 図の説明                実戦形の詰み（手順はソルバが生成）
@kifu <定跡名>                             kifu.py の手順と局面図を展開する
@hisshi <番号>                             必至問題
@problems <手数>   @answers                演習問題と解答
@toc  @index  @glossary                    目次・索引・用語辞典
@box 見出し ... @endbox                     定義・命題の囲み
@raw ... @endraw                           生の HTML
| 表 | ヘッダ |                            表
> 注記                                      補足の囲み
```
