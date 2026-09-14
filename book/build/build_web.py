#!/usr/bin/env python3
"""『世界史大全』のWeb版を生成する。

PDF版と同じ断片（book/content/**.html）から、章ごとの静的HTMLを組み立てて
リポジトリ直下の worldhistory/ へ出力する。GitHub Pages でそのまま配信できる。

PDF版との違い:
- <ruby> を変換せず、本物のルビとして表示する
- フォントは Google Fonts のCDNを参照し、リポジトリを軽く保つ
- ページ番号の相互参照は使えないため、.xref / .sakuin / .zuhan の a::after は
  Web用CSSで無効化し、リンクそのものを生かす
"""
from __future__ import annotations

import html as htmlmod
import json
import re
import shutil
from pathlib import Path

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parent
CONTENT = BOOK / "content"
OUT = ROOT / "worldhistory"
MANIFEST = json.loads((BOOK / "manifest.json").read_text(encoding="utf-8"))

TITLE = MANIFEST["title"]
SUBTITLE = MANIFEST["subtitle"]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Noto+Sans+JP:wght@400;700&family=Noto+Serif+JP:wght@400;600&display=swap">')


def esc(s: str) -> str:
    return htmlmod.escape(s, quote=True)


def page(title: str, body: str, depth: int = 0, desc: str = "") -> str:
    up = "../" * depth
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc or SUBTITLE)}">
{FONTS}
<link rel="stylesheet" href="{up}web.css">
</head>
<body>
<header class="site">
  <a class="site-title" href="{up}index.html">{esc(TITLE)}</a>
  <nav class="site-nav">
    <a href="{up}index.html">目次</a>
    <a href="{up}sekaishi-taizen.pdf">PDF版</a>
  </nav>
</header>
<main>
{body}
</main>
<footer class="site">
  <p>{esc(TITLE)}　{esc(SUBTITLE)}</p>
  <p class="small">本文・図版とも本書のために作成したものです。引用した史料の訳は本書によります。</p>
</footer>
</body>
</html>
"""


def chapter_records() -> list[dict]:
    """本文の章を、部の情報と前後関係つきで並べる。"""
    recs = []
    for part in MANIFEST["parts"]:
        for ch in part["chapters"]:
            path = CONTENT / part["dir"] / ch["file"]
            if not path.exists():
                continue
            recs.append({
                "n": ch["n"], "title": ch["title"], "part": part,
                "path": path, "slug": f'ch{ch["n"]:02d}.html',
            })
    return recs


def appendix_records() -> list[dict]:
    recs = []
    for ap in MANIFEST["appendix"]:
        path = CONTENT / "zz-appendix" / ap["file"]
        if path.exists():
            recs.append({"label": ap["label"], "title": ap["title"],
                         "path": path, "slug": f'{ap["id"]}.html'})
    return recs


def webify_index(body: str) -> str:
    """索引をWeb向けに組み替える。

    PDF版の索引は「用語」＋「空のアンカー（::after がページ番号を出す）」という
    構造をとる。Webではページ番号が存在しないため、そのままでは押せないリンクに
    なってしまう。用語そのものを最初の参照へのリンクにし、二つめ以降は連番で示す。
    """
    def fix_item(m: re.Match) -> str:
        term = m.group(1)
        hrefs = re.findall(r'href="([^"]+)"', m.group(2))
        if not hrefs:
            return m.group(0)
        out = f'<a href="{hrefs[0]}">{term}</a>'
        for i, h in enumerate(hrefs[1:], 2):
            out += f'<a class="more" href="{h}">{i}</a>'
        return f"<li>{out}</li>"

    body = re.sub(r'<li><span class="idx-term">(.*?)</span>(.*?)</li>', fix_item, body)
    # 「数字はページ番号であり…」はPDF版だけの説明なので差し替える
    return body.replace(
        "数字はページ番号であり、組版時に自動で解決している（手入力ではない）。",
        "用語をたどると、それが登場する章へ移動する。"
        "同じ用語が複数の章に現れる場合は、二つめ以降を番号で示した。")


def rewrite_links(body: str, chapter_of: dict[str, str]) -> str:
    """断片内の href="#id" を、その id を持つページへのリンクに書き換える。"""
    def sub(m: re.Match) -> str:
        target = m.group(1)
        dest = chapter_of.get(target)
        if dest is None:
            return m.group(0)
        return f'href="{dest}#{target}"'
    return re.sub(r'href="#([^"]+)"', sub, body)


def build() -> None:
    OUT.mkdir(exist_ok=True)
    chapters = chapter_records()
    appendices = appendix_records()

    # id → 出力ファイル名の対応表（章をまたぐリンクの解決に使う）
    chapter_of: dict[str, str] = {}
    for rec in chapters:
        src = rec["path"].read_text(encoding="utf-8")
        chapter_of[f'ch{rec["n"]:02d}'] = rec["slug"]
        for i in range(1, src.count("<figure") + 1):
            chapter_of[f'fig{rec["n"]}-{i}'] = rec["slug"]
        for sid in re.findall(r'id="([^"]+)"', src):
            chapter_of[sid] = rec["slug"]
    for rec in appendices:
        for sid in re.findall(r'id="([^"]+)"', rec["path"].read_text(encoding="utf-8")):
            chapter_of[sid] = rec["slug"]

    # ---- 章 ----
    for i, rec in enumerate(chapters):
        src = rec["path"].read_text(encoding="utf-8").strip()
        # PDF版と同じく <figure> に id を振る（図版索引からのリンク先）
        counter = iter(range(1, 99))
        src = re.sub(r"<figure(?![^>]*\sid=)",
                     lambda _m: f'<figure id="fig{rec["n"]}-{next(counter)}"', src)
        src = re.sub(r"<figcaption(?![^>]*data-ch=)",
                     f'<figcaption data-ch="{rec["n"]}"', src)
        src = rewrite_links(src, chapter_of)

        prev_rec = chapters[i - 1] if i else None
        next_rec = chapters[i + 1] if i + 1 < len(chapters) else None
        nav = ['<nav class="chnav">']
        nav.append(f'<a class="prev" href="{prev_rec["slug"]}">← 第{prev_rec["n"]}章　'
                   f'{esc(prev_rec["title"])}</a>' if prev_rec else '<span></span>')
        nav.append(f'<a class="next" href="{next_rec["slug"]}">第{next_rec["n"]}章　'
                   f'{esc(next_rec["title"])} →</a>' if next_rec else '<span></span>')
        nav.append("</nav>")
        navhtml = "\n".join(nav)

        body = (f'<article class="chapter">\n'
                f'<p class="part-label">{esc(rec["part"]["label"])}　'
                f'{esc(rec["part"]["title"])}</p>\n'
                f'<h1><span class="ch-num">第{rec["n"]}章</span>'
                f'{esc(rec["title"])}</h1>\n{navhtml}\n{src}\n{navhtml}\n</article>')
        (OUT / rec["slug"]).write_text(
            page(f'第{rec["n"]}章 {rec["title"]}｜{TITLE}', body,
                 desc=f'{TITLE}　第{rec["n"]}章　{rec["title"]}'),
            encoding="utf-8")

    # ---- 巻末資料 ----
    for rec in appendices:
        src = rewrite_links(rec["path"].read_text(encoding="utf-8").strip(), chapter_of)
        src = webify_index(src)
        body = (f'<article class="chapter appendix">\n'
                f'<p class="part-label">巻末資料</p>\n'
                f'<h1><span class="ch-num">{esc(rec["label"])}</span>'
                f'{esc(rec["title"])}</h1>\n{src}\n</article>')
        (OUT / rec["slug"]).write_text(
            page(f'{rec["label"]} {rec["title"]}｜{TITLE}', body), encoding="utf-8")

    # ---- 目次 ----
    toc = ['<section class="hero">',
           f'<h1>{esc(TITLE)}</h1>',
           f'<p class="sub">{esc(SUBTITLE)}</p>',
           '<p class="lead">高校の「世界史探究」から大学の概説、そして学説の対立と史料批判まで、'
           '同じ主題を三つの水準で読めるように構成した通史です。'
           'すべての図版は本書のために作成し、史料の訳は本書によります。</p>',
           '<p class="dl"><a class="btn" href="sekaishi-taizen.pdf">PDF版をダウンロード</a>'
           f'<span class="meta">全{len(chapters)}章・巻末資料{len(appendices)}点</span></p>',
           '<div class="levels">',
           '<span class="lvtag t1">★ 高校</span>',
           '<span class="lvtag t2">★★ 大学</span>',
           '<span class="lvtag t3">★★★ 大学院</span>',
           '<span class="levels-note">同じ主題を三つの水準で扱います</span>',
           '</div>',
           '</section>']
    cur = None
    for rec in chapters:
        if rec["part"]["id"] != cur:
            if cur is not None:
                toc.append("</ol>")
            cur = rec["part"]["id"]
            toc.append(f'<h2 class="part">{esc(rec["part"]["label"])}　'
                       f'{esc(rec["part"]["title"])}'
                       f'<span class="period">{esc(rec["part"].get("period", ""))}</span></h2>')
            toc.append('<ol class="toc">')
        toc.append(f'<li><a href="{rec["slug"]}">'
                   f'<span class="n">第{rec["n"]}章</span>{esc(rec["title"])}</a></li>')
    toc.append("</ol>")
    toc.append('<h2 class="part">巻末資料</h2><ol class="toc">')
    for rec in appendices:
        toc.append(f'<li><a href="{rec["slug"]}">'
                   f'<span class="n">{esc(rec["label"])}</span>{esc(rec["title"])}</a></li>')
    toc.append("</ol>")
    (OUT / "index.html").write_text(page(f"{TITLE}｜{SUBTITLE}", "\n".join(toc)),
                                    encoding="utf-8")

    # ---- CSS と PDF ----
    shutil.copy(BOOK / "assets" / "css" / "web.css", OUT / "web.css")
    pdf = BOOK / "out" / "sekaishi-taizen.pdf"
    if pdf.exists():
        shutil.copy(pdf, OUT / "sekaishi-taizen.pdf")

    print(f"Web版を生成しました: {OUT}")
    print(f"  章 {len(chapters)} / 巻末 {len(appendices)} / PDF {'あり' if pdf.exists() else 'なし'}")


if __name__ == "__main__":
    build()
