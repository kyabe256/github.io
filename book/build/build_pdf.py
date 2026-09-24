#!/usr/bin/env python3
"""manifest.json と章ごとの HTML 断片から『世界史大全』のPDFを組版する。

  python book/build/build_pdf.py [-o 出力先.pdf] [--only p01,p02] [--no-stub]

未執筆の章は既定でスタブ（見出しだけ）として差し込むため、
執筆の途中でも常に通しでビルドでき、目次・しおり・ページ番号を確認できる。
"""
from __future__ import annotations

import argparse
import itertools
import json
import logging
import re
import sys
from datetime import date
from pathlib import Path

import mathbook
from _bookroot import book_root, slug_of

BOOK = book_root(__file__)
# 数学書のときだけ使う定理番号の対応表。manifest に "math": true があれば有効になる。
THM_REGISTRY: dict | None = None
CONTENT = BOOK / "content"
ASSETS = BOOK / "assets"
MANIFEST = BOOK / "manifest.json"


# ---------------------------------------------------------------- 断片の整形

RUBY_TAGS = re.compile(r"</?(?:ruby|rp)\b[^>]*>")


def flatten_ruby(html: str) -> str:
    """WeasyPrint は <ruby> を組めないため「漢字（かな）」に変換する。

    Web版では元の <ruby> のまま本物のルビとして表示される。
    """
    html = re.sub(r"<rt\b[^>]*>", "（", html)
    html = html.replace("</rt>", "）")
    return RUBY_TAGS.sub("", html)


def number_captions(html: str, ch_num: int) -> str:
    """図表キャプションに章番号を持たせ（図5-1 / 表5-2 の「5」の部分）、
    図版索引（付録D）が target-counter() で参照できる id を振る。"""
    html = re.sub(r"<figcaption(?![^>]*data-ch=)", f'<figcaption data-ch="{ch_num}"', html)
    html = re.sub(r"<caption(?![^>]*data-ch=)", f'<caption data-ch="{ch_num}"', html)

    counter = itertools.count(1)
    html = re.sub(r"<figure(?![^>]*\sid=)",
                  lambda _m: f'<figure id="fig{ch_num}-{next(counter)}"', html)
    return html


def load_chapter(part: dict, ch: dict, stub: bool) -> str | None:
    path = CONTENT / part["dir"] / ch["file"]
    heading = (
        f'<h2 id="ch{ch["n"]:02d}">'
        f'<span class="ch-num">第{ch["n"]}章　</span>{ch["title"]}</h2>'
    )

    if path.exists():
        body = path.read_text(encoding="utf-8").strip()
        # 断片は <h2> を持たない前提。持っていればそちらを優先する。
        if "<h2" not in body:
            body = heading + "\n" + body
        body = flatten_ruby(body)
        body = number_captions(body, ch["n"])
        # 数学書では定義・定理・例・反例に章内の通し番号を振る（第一パス）。
        # 番号を手で書かないための仕組み。THM_REGISTRY は assemble が用意する。
        if THM_REGISTRY is not None:
            body = mathbook.number_boxes(body, ch["n"], THM_REGISTRY)
        return f'<section class="chapter" id="chsec{ch["n"]:02d}">\n{body}\n</section>'

    if not stub:
        return None
    return (
        f'<section class="chapter" id="chsec{ch["n"]:02d}">\n{heading}\n'
        f'<p class="stub-note">（この章は執筆中です）</p>\n</section>'
    )


# ---------------------------------------------------------------- 前付け

def build_cover(m: dict) -> str:
    # 三層の呼び名は本ごとに違う。manifest の levels に無ければ従来の文面を使う。
    lv = m.get("levels", [
        "★　　高校「世界史探究」の本文",
        "★★　 大学の概説講義にあたる「ゼミナール」",
        "★★★ 大学院の議論にあたる「研究の最前線」",
    ])
    return f"""<section class="cover">
  <p class="cv-title">{m['title']}</p>
  <p class="cv-sub">{m['subtitle']}</p>
  <div class="cv-rule"></div>
  <p class="cv-levels">
    {'<br>'.join(lv)}
  </p>
  <p class="cv-foot">{m['edition']}</p>
</section>"""


def build_guide() -> str:
    # 本ごとに差し替えられるよう、content/_guide.html があればそれを使う。
    # 無ければ従来の文面（世界史大全のもの）を出す。
    custom = CONTENT / "_guide.html"
    if custom.exists():
        return ('<section class="frontmatter" id="guide">\n'
                + custom.read_text(encoding="utf-8").strip() + "\n</section>")
    return """<section class="frontmatter" id="guide">
<h1>本書の使い方</h1>

<p class="no-indent">本書は、一冊のなかに三つの深さの記述を重ねている。読者は自分の目的に合わせて、
どの層まで降りるかを選ぶことができる。</p>

<div class="toi">
<h4>三つの層</h4>
<ul>
<li><strong>★ 本文</strong>　高校「世界史探究」に対応する。むずかしい言葉はできるだけ避け、
出来事の流れと因果が物語として頭に入るように書いた。まずここだけを通して読めば、
人類史の背骨が一本通る。</li>
<li><strong>★★ ゼミナール</strong>　大学の概説講義にあたる。本文で「こうなった」とだけ書いたことを、
概念・統計・地域間比較を使って「なぜそうなったのか」まで掘り下げる。</li>
<li><strong>★★★ 研究の最前線</strong>　大学院の演習にあたる。その論点について研究者が実際に何を争って
いるのか、どの史料をどう読むかで結論がどう変わるのかを示す。ここには「まだ答えが出ていない」
という記述が頻繁に登場する。それは本書の欠陥ではなく、歴史学という学問の現在地である。</li>
</ul>
</div>

<h3>各章の構成</h3>
<p>すべての章は同じ順序で組み立てられている。</p>
<ol>
<li><strong>この章の問い</strong>　その章を貫く問題提起。ここを頭に入れてから読むと、
事実の羅列が「問いへの答え」として並んで見えてくる。</li>
<li><strong>本文（★）と、途中に挟まる ★★ / ★★★ の囲み</strong></li>
<li><strong>史料を読む</strong>　同時代の人間が実際に書き残した文章を抜き出し、
そこから何が読み取れて、何は読み取れないのかを一緒に考える。</li>
<li><strong>図版</strong>　地図・系図・年表・グラフ。すべて本書のために描き起こした。</li>
<li><strong>章末問題</strong>　用語確認・記述・論述の三段階。解答例と採点の観点は付録Eにある。</li>
</ol>

<h3>凡例</h3>
<ul>
<li>年代は原則として西暦で示し、紀元前は「前」を冠する（例：前221年）。
世紀は算用数字で示す（例：15世紀）。</li>
<li>人物名のあとの丸括弧内は生没年、王・皇帝の場合は在位年を示し、
在位には「位」を冠する（例：アウグストゥス〈位前27〜後14〉）。</li>
<li>史料の日本語訳は、断りのないかぎり本書のために原典から訳出したものである。
訳文中の〔　〕は訳者による補足、…… は省略を示す。</li>
<li>研究者の名前は、その学説が特定の個人と強く結びついている場合にかぎって挙げた。</li>
<li>学界で決着していない論点については、断定を避け、対立する見解を併記した。</li>
</ul>
</section>"""


def build_toc(m: dict) -> str:
    rows = ['<section class="frontmatter toc" id="toc">', "<h1>目次</h1>", "<ul>"]
    for part in m["parts"]:
        period = (
            f'<span class="toc-period">{part["period"]}</span>' if part.get("period") else ""
        )
        rows.append(
            f'<li class="toc-part"><a href="#{part["id"]}">'
            f'{part["label"]}　{part["title"]}</a>{period}</li>'
        )
        for ch in part["chapters"]:
            rows.append(
                f'<li class="toc-chap"><a href="#ch{ch["n"]:02d}">'
                f'<span class="toc-n">第{ch["n"]}章</span>{ch["title"]}</a></li>'
            )
    rows.append('<li class="toc-part"><a href="#appendix">巻末資料</a></li>')
    for ap in m["appendix"]:
        rows.append(
            f'<li class="toc-chap"><a href="#{ap["id"]}">'
            f'<span class="toc-n">{ap["label"]}</span>{ap["title"]}</a></li>'
        )
    rows += ["</ul>", "</section>"]
    return "\n".join(rows)


def build_part_title(part: dict) -> str:
    period = f'<p class="part-period">{part["period"]}</p>' if part.get("period") else ""
    lead = f'<p class="part-lead">{part["lead"]}</p>' if part.get("lead") else ""
    return f"""<section class="part-title" id="{part['id']}">
  <p class="part-label">{part['label']}</p>
  <h1>{part['title']}</h1>
  {period}
  {lead}
</section>"""


def build_okuduke(m: dict) -> str:
    return f"""<section class="frontmatter" id="okuduke">
<div class="okuduke">
<p><strong>{m['title']}</strong>　{m['subtitle']}</p>
<p>{m['edition']}　{date.today().year}年発行</p>
<p>{m.get('colophon_note',
  '本文・図版・史料訳はすべて本書のために書き起こした。図版はコードで描画したSVGであり、'
  '外部の画像素材を使用していない。')}</p>
<p>組版：WeasyPrint（CSS Paged Media）／本文書体：Noto Serif JP、
見出し書体：Noto Sans JP（いずれも SIL Open Font License 1.1）</p>
<p>本書は Claude Code を用いて執筆・組版された。</p>
</div>
</section>"""


# ---------------------------------------------------------------- 組み立て

def assemble(m: dict, only: set[str] | None, stub: bool) -> tuple[str, dict]:
    parts_html: list[str] = []
    stats = {"written": 0, "stub": 0, "chars": 0}

    for part in m["parts"]:
        if only and part["id"] not in only:
            continue
        parts_html.append(build_part_title(part))
        for ch in part["chapters"]:
            frag = load_chapter(part, ch, stub)
            if frag is None:
                continue
            if (CONTENT / part["dir"] / ch["file"]).exists():
                stats["written"] += 1
                stats["chars"] += len(re.sub(r"<[^>]+>", "", frag))
            else:
                stats["stub"] += 1
            parts_html.append(frag)

    ap_html = ['<section class="part-title appendix" id="appendix">',
               '<p class="part-label">巻末</p><h1>巻末資料</h1>',
               '<p class="part-lead">年表・用語集・系図・解答例・読書案内・索引。'
               '本文を読み終えたあと、あるいは読みながら参照するための道具立てである。</p>',
               "</section>"]
    for ap in m["appendix"]:
        path = CONTENT / "zz-appendix" / ap["file"]
        head = f'<h1 id="{ap["id"]}">{ap["label"]}　{ap["title"]}</h1>'
        if path.exists():
            body = flatten_ruby(path.read_text(encoding="utf-8").strip())
            stats["written"] += 1
            stats["chars"] += len(re.sub(r"<[^>]+>", "", body))
            if "<h1" not in body:
                body = head + "\n" + body
        elif stub:
            body = head + '\n<p class="stub-note">（執筆中）</p>'
            stats["stub"] += 1
        else:
            continue
        ap_html.append(f'<section class="frontmatter appendix-body">\n{body}\n</section>')

    doc = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>{m['title']}</title>
<meta name="author" content="{m['publisher']}">
<meta name="description" content="{m['subtitle']}">
<meta name="dcterms.created" content="{date.today().isoformat()}">
<link rel="stylesheet" href="{(ASSETS / 'css' / 'common.css').as_uri()}">
<link rel="stylesheet" href="{(ASSETS / 'css' / 'print.css').as_uri()}">
</head>
<body>
{build_cover(m)}
{build_guide()}
{build_toc(m)}
{chr(10).join(parts_html)}
{chr(10).join(ap_html)}
{build_okuduke(m)}
</body>
</html>"""
    return doc, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--out", default=None, help="出力先。既定は out/<slug>.pdf")
    ap.add_argument("--only", help="部IDをカンマ区切りで指定（例 p00,p01）")
    ap.add_argument("--no-stub", action="store_true", help="未執筆の章を差し込まない")
    ap.add_argument("--keep-html", action="store_true", help="結合後のHTMLも残す")
    args = ap.parse_args()

    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    only = set(args.only.split(",")) if args.only else None

    # 数学書のときだけ、定理番号と数式の処理を有効にする。
    # 既存の二冊（manifest に "math" が無い）では一切走らない。
    global THM_REGISTRY
    is_math = bool(m.get("math"))
    if is_math:
        THM_REGISTRY = {}

    doc, stats = assemble(m, only, stub=not args.no_stub)

    if is_math:
        doc, missing = mathbook.resolve_refs(doc, THM_REGISTRY)   # 第二パス
        doc, mstats = mathbook.render_math(doc, BOOK)
        left = mathbook.leftovers(doc)
        stats["math"] = mstats
        stats["ref_missing"] = missing
        stats["leftovers"] = left

    out = Path(args.out) if args.out else BOOK / "out" / f"{slug_of(m)}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    html_path = out.with_suffix(".html")
    html_path.write_text(doc, encoding="utf-8")

    # フォント未収録文字（豆腐）を検出するためにログを捕まえる
    warnings: list[str] = []

    class Catch(logging.Handler):
        def emit(self, record):
            msg = record.getMessage()
            if "HarfBuzz" not in msg:
                warnings.append(msg)

    logger = logging.getLogger("weasyprint")
    logger.addHandler(Catch())
    logger.setLevel(logging.WARNING)

    from weasyprint import HTML  # 起動を速くするため遅延インポート

    HTML(filename=str(html_path)).write_pdf(str(out))

    if not args.keep_html:
        html_path.unlink()

    size_mb = out.stat().st_size / 1024 / 1024
    print(f"出力      : {out}  ({size_mb:.1f} MB)")
    print(f"執筆済み章: {stats['written']}　スタブ: {stats['stub']}")
    print(f"本文文字数: {stats['chars']:,} 字")

    if "math" in stats:
        ms, left = stats["math"], stats["leftovers"]
        print(f"数式      : {ms['total']} 種（新規レンダリング {ms['rendered']}）")
        print(f"定理番号  : {len(THM_REGISTRY)} 件に付与")
        problems = (ms["errors"] or ms.get("mjx_errors") or stats["ref_missing"]
                    or left["math"] or left["ref"]
                    or left["math_error"] or left["ref_error"])
        if problems:
            print("\n  ✗ 未解決:")
            for i, e in ms["errors"][:5]:
                print(f"    数式のエラー {i}: {e}")
            for tex in ms.get("mjx_errors", [])[:8]:
                print(f"    数式が黒箱になっている: {tex[:70]}")
            for t in stats["ref_missing"][:5]:
                print(f"    参照先が無い: {t}")
            if left["math"]:
                print(f"    置換されなかった <m>/<M>: {left['math']} 件")
            if left["ref"]:
                print(f"    置換されなかった <ref>: {left['ref']} 件")
        else:
            print("数式と参照: すべて解決")

    if warnings:
        print(f"\n警告 {len(warnings)} 件:")
        for w in dict.fromkeys(warnings):
            print("  -", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
