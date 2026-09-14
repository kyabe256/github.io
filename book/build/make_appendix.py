#!/usr/bin/env python3
"""巻末資料のうち機械的に作れるものを本文から生成する。

- 付録D 図版索引 …… <figure> を順に拾い、figN-M の id を参照する
- 付録G 索引   …… <span class="yogo"> の用語を拾い、直前の節 id を参照する

ページ番号は一切書き込まない。すべて print.css の target-counter() が解決する。
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
MANIFEST = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

# .yogo は強調にも使われているため、用語として妥当な長さに限る
MAX_TERM = 25
TAG = re.compile(r"<[^>]+>")
YOGO = re.compile(r'<span class="yogo">(.*?)</span>', re.S)
FIGCAP = re.compile(r"<figure\b.*?<figcaption[^>]*>(.*?)</figcaption>", re.S)
SECTION = re.compile(r'<h3 id="(s[\w-]+)"')


def strip(html: str) -> str:
    return TAG.sub("", html).replace("\n", "").strip()


def chapters():
    for part in MANIFEST["parts"]:
        for ch in part["chapters"]:
            path = CONTENT / part["dir"] / ch["file"]
            if path.exists():
                yield ch, path.read_text(encoding="utf-8")


def head_key(term: str) -> str:
    """索引の見出し分類。五十音・漢字・欧字で束ねる。"""
    for c in term:
        if c in "「『（・":
            continue
        n = unicodedata.normalize("NFKC", c)
        if "ぁ" <= n <= "ゖ" or "ァ" <= n <= "ヶ":
            kana = chr(ord(n) + 0x60) if "ぁ" <= n <= "ゖ" else n
            table = [("ア", "アイウエオヴ"), ("カ", "カキクケコガギグゲゴ"),
                     ("サ", "サシスセソザジズゼゾ"), ("タ", "タチツテトダヂヅデド"),
                     ("ナ", "ナニヌネノ"), ("ハ", "ハヒフヘホバビブベボパピプペポ"),
                     ("マ", "マミムメモ"), ("ヤ", "ヤユヨャュョ"),
                     ("ラ", "リルレロラ"), ("ワ", "ワヲンヰヱ")]
            for head, members in table:
                if kana in members:
                    return head
            return "ア"
        if "一" <= n <= "鿿":
            return "漢字ではじまる語"
        if n.isascii() and n.isalpha():
            return "欧字ではじまる語"
    return "その他"


KANA_ORDER = "アカサタナハマヤラワ"


def build_index() -> str:
    """付録G 索引"""
    entries: dict[str, list[tuple[int, str]]] = {}
    for ch, html in chapters():
        # 節見出しの位置を記録し、用語ごとに直前の節を参照先にする
        anchors = [(m.start(), m.group(1)) for m in SECTION.finditer(html)]
        for m in YOGO.finditer(html):
            term = strip(m.group(1))
            if not term or len(term) > MAX_TERM:
                continue
            target = f'ch{ch["n"]:02d}'
            for pos, sid in anchors:
                if pos < m.start():
                    target = sid
                else:
                    break
            entries.setdefault(term, [])
            if (ch["n"], target) not in entries[term]:
                entries[term].append((ch["n"], target))

    groups: dict[str, list[str]] = {}
    for term, refs in entries.items():
        groups.setdefault(head_key(term), []).append(term)

    order = list(KANA_ORDER) + ["漢字ではじまる語", "欧字ではじまる語", "その他"]
    out = ['<h3 id="apG-honbun">索引</h3>',
           '<p class="no-indent">本文中で <span class="yogo">太字</span> として示した用語を'
           '五十音順に配列した。数字はページ番号であり、'
           '組版時に自動で解決している（手入力ではない）。</p>',
           '<div class="sakuin">']
    for g in order:
        terms = sorted(groups.get(g, []))
        if not terms:
            continue
        out.append(f'<p class="idx-group">{g}</p>')
        out.append("<ul>")
        for term in terms:
            refs = entries[term][:6]
            links = "、".join(
                f'<a href="#{tgt}">{"" if i else ""}</a>' for i, (_n, tgt) in enumerate(refs))
            out.append(f'<li><span class="idx-term">{term}</span>{links}</li>')
        out.append("</ul>")
    out.append("</div>")
    return "\n".join(out)


def build_figure_index() -> str:
    """付録D 地図・図版索引"""
    out = ['<h3 id="apD-honbun">地図・図版索引</h3>',
           '<p class="no-indent">本書に収めた図版を章順に配列した。すべて本書のために'
           '作成したもので、外部の画像素材を用いていない。'
           'ページ番号は組版時に自動で解決している。</p>',
           '<div class="zuhan">']
    total = 0
    for part in MANIFEST["parts"]:
        rows = []
        for ch in part["chapters"]:
            path = CONTENT / part["dir"] / ch["file"]
            if not path.exists():
                continue
            for i, m in enumerate(FIGCAP.finditer(path.read_text(encoding="utf-8")), 1):
                cap = strip(m.group(1))
                cap = cap.split("。")[0] + "。" if "。" in cap else cap
                rows.append(
                    f'<li><a href="#fig{ch["n"]}-{i}">'
                    f'<span class="zu-num">図{ch["n"]}-{i}</span>　{cap}</a></li>')
                total += 1
        if rows:
            out.append(f'<p class="idx-group">{part["label"]}　{part["title"]}</p>')
            out.append("<ul>" + "".join(rows) + "</ul>")
    out.append("</div>")
    out.insert(2, f'<p class="no-indent">収録点数 {total} 点。</p>')
    return "\n".join(out)


def main() -> None:
    target = CONTENT / "zz-appendix"
    target.mkdir(parents=True, exist_ok=True)
    (target / "D-zuhan-sakuin.html").write_text(build_figure_index() + "\n", encoding="utf-8")
    (target / "G-sakuin.html").write_text(build_index() + "\n", encoding="utf-8")
    print("付録D・Gを生成しました")


if __name__ == "__main__":
    main()
