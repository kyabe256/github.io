#!/usr/bin/env python3
"""巻末資料のうち機械的に作れるものを本文から生成する。

- 付録B 定義集 …… 各章の .teigi を拾い、番号と見出しを章順に並べる
- 付録C 反例カタログ …… 各章の .hanrei を拾い、何が壊れるかを添える
- 付録D 図版索引 …… <figure> を順に拾い、figN-M の id を参照する
- 付録G 索引   …… <span class="yogo"> の用語を拾い、直前の節 id を参照する

ページ番号は一切書き込まない。すべて print.css の target-counter() が解決する。
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from _bookroot import book_root

ROOT = book_root(__file__)
CONTENT = ROOT / "content"
MANIFEST = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))

# .yogo は強調にも使われているため、用語として妥当な長さに限る
MAX_TERM = 25
TAG = re.compile(r"<[^>]+>")
YOGO = re.compile(r'<span class="yogo">(.*?)</span>', re.S)
# この本は定義される用語を <strong> で示している（.yogo はほとんど使っていない）
TERM = re.compile(r'<strong>(.*?)</strong>|<span class="yogo">(.*?)</span>', re.S)
# 索引に入れない、文章の区切りとしての強調
STOPWORDS = {
    "例", "反例", "注意", "証明", "定義", "定理", "系", "補題", "命題",
    "一意性", "存在", "逆", "必要性", "十分性", "結論", "要点", "まとめ",
    "使いどころ", "言い換え", "帰結", "応用", "注", "補足", "前半", "後半",
    "第一段", "第二段", "第三段", "第四段", "一般化", "特別な場合",
}
FIGCAP = re.compile(r"<figure\b.*?<figcaption[^>]*>(.*?)</figcaption>", re.S)
SECTION = re.compile(r'<h3 id="(s[\w-]+)"')
BOX = re.compile(r'<div class="(teigi|hanrei)"([^>]*)>\s*<h4>(.*?)</h4>(.*?)</div>', re.S)
BOX_ID = re.compile(r'id="([^"]+)"')
LEAD = re.compile(r'<p[^>]*>(.*?)</p>', re.S)


ORIG = re.compile(r'<span class="orig">.*?</span>', re.S)


def strip(html: str) -> str:
    html = ORIG.sub("", html)
    return TAG.sub("", html).replace("\n", "").strip()


MATH_BLOCK = re.compile(r"<([mM])>(.*?)</\1>", re.S)


def strip_keep_math(html: str) -> str:
    """タグを落とすが、<m> の中身はそのまま残す。

    数式本文には生の < が入りうる（不等号）。タグ除去より先に
    数式をまるごと退避しないと、そこから先が食われてしまう。
    """
    html = ORIG.sub("", html)
    held: list[str] = []

    def stash(mo: re.Match) -> str:
        held.append(mo.group(2))
        return f"\x00{len(held) - 1}\x01"

    html = MATH_BLOCK.sub(stash, html)
    html = TAG.sub("", html).replace("\n", "").strip()
    for i, tex in enumerate(held):
        html = html.replace(f"\x00{i}\x01", f"<m>{tex}</m>")
    return html


MATH_SPAN = re.compile(r"<m>.*?</m>", re.S)


def clip_keep_math(text: str, budget: int) -> str:
    """数式の途中で切らずに、見た目の長さで切り詰める。"""
    out, used = [], 0
    pos = 0
    for mo in MATH_SPAN.finditer(text):
        plain = text[pos:mo.start()]
        if used + len(plain) >= budget:
            return "".join(out) + plain[: budget - used] + "…"
        out.append(plain)
        used += len(plain)
        inner = len(TAG.sub("", mo.group(0)))
        if used + inner > budget:            # 数式ごと落とす
            return "".join(out).rstrip() + "…"
        out.append(mo.group(0))
        used += inner
        pos = mo.end()
    tail = text[pos:]
    if used + len(tail) > budget:
        return "".join(out) + tail[: budget - used] + "…"
    return "".join(out) + tail


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
        for m in TERM.finditer(html):
            raw = strip_keep_math(m.group(1) or m.group(2) or "")
            # 段落の切り出し（<strong>……。</strong>）は用語ではないので外す
            if raw.endswith(("。", "．", "？", "か", "、")) or "、" in raw:
                continue
            term = raw.strip("。．、 ")
            if not term or len(term) > MAX_TERM or len(term) < 2:
                continue
            if term in STOPWORDS or term.isdigit():
                continue
            if re.fullmatch(r"\d{3,4}年", term):          # 年表の見出し
                continue
            if term.endswith(("ため", "とき", "こと", "もの", "場合", "理由",
                              "ように", "だけ", "まで", "ほど")):
                continue
            # 述語をふくむ言い回しは用語ではない（「の」「と」は語の一部でありうる）
            if any(k in term for k in ("は", "が", "を", "へ", "より", "から")):
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
    def plain(t: str) -> str:
        return TAG.sub("", t)

    for term, refs in entries.items():
        groups.setdefault(head_key(plain(term)), []).append(term)

    order = list(KANA_ORDER) + ["漢字ではじまる語", "欧字ではじまる語", "その他"]
    out = ['<h3 id="apG-honbun">索引</h3>',
           '<p class="no-indent">本文中で <span class="yogo">太字</span> として示した用語を'
           '五十音順に配列した。数字はページ番号であり、'
           '組版時に自動で解決している（手入力ではない）。</p>',
           '<div class="sakuin">']
    for g in order:
        terms = sorted(groups.get(g, []), key=plain)
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
                cap = strip_keep_math(m.group(1))
                if "。" in TAG.sub("", cap):
                    cap = clip_keep_math(cap, TAG.sub("", cap).index("。") + 1)
                    cap = cap.rstrip("…")
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


def boxes(kind: str):
    """本文の .teigi / .hanrei を章順に拾う。番号は組版と同じ数え方で振る。"""
    for part in MANIFEST["parts"]:
        for ch in part["chapters"]:
            path = CONTENT / part["dir"] / ch["file"]
            if not path.exists():
                continue
            html = path.read_text(encoding="utf-8")
            n = 0
            for m in BOX.finditer(html):
                n += 1                      # 番号は四種の箱の通し（本文と同じ）
            # 本文と同じ通し番号にするため、全種類の箱を数え直す
            n = 0
            for m in re.finditer(
                    r'<div class="(teigi|teiri|rei|hanrei)"([^>]*)>\s*<h4>(.*?)</h4>',
                    html, re.S):
                n += 1
                if m.group(1) != kind:
                    continue
                idm = BOX_ID.search(m.group(2))
                rest = html[m.end():]
                body = LEAD.search(rest)
                lead = strip_keep_math(body.group(1)) if body else ""
                title = strip_keep_math(m.group(3))
                if not title:
                    sm = re.search(r"<strong>(.*?)</strong>", rest[:900], re.S)
                    title = strip_keep_math(sm.group(1)).rstrip("。") if sm else ""
                yield {
                    "part": part, "ch": ch,
                    "num": f'{ch["n"]}.{n}',
                    "title": title,
                    "id": idm.group(1) if idm else None,
                    "lead": lead,
                }


def build_definitions() -> str:
    """付録B 定義集"""
    out = ['<h3 id="apB-honbun">定義集</h3>',
           '<p class="no-indent">本文で <strong>定義</strong> として枠に囲んだ項目を、'
           '章順に集めた。番号は本文のものと同じで、'
           'ページ番号は組版時に自動で解決している。</p>',
           '<div class="teigishu">']
    total = 0
    cur = None
    for b in boxes("teigi"):
        if cur != b["part"]["label"]:
            if cur is not None:
                out.append("</ul>")
            cur = b["part"]["label"]
            out.append(f'<p class="idx-group">{cur}　{b["part"]["title"]}</p>')
            out.append("<ul>")
        target = b["id"] or f'ch{b["ch"]["n"]:02d}'
        name = f'定義{b["num"]}' + (f'　{b["title"]}' if b["title"] else "")
        out.append(f'<li><a href="#{target}"><span class="idx-term">{name}</span></a></li>')
        total += 1
    if cur is not None:
        out.append("</ul>")
    out.append("</div>")
    out.insert(2, f'<p class="no-indent">収録 {total} 項目。</p>')
    return "\n".join(out)


def build_counterexamples() -> str:
    """付録C 反例カタログ"""
    out = ['<h3 id="apC-honbun">反例カタログ</h3>',
           '<p class="no-indent">本文で <strong>反例</strong> として枠に囲んだ項目を、'
           '章順に集めた。<em>定理の仮定のどれを落とすと何が壊れるか</em>を'
           '一覧するためのものである。ページ番号は組版時に自動で解決している。</p>',
           '<div class="hanreishu">']
    total = 0
    cur = None
    for b in boxes("hanrei"):
        if cur != b["part"]["label"]:
            if cur is not None:
                out.append("</ul>")
            cur = b["part"]["label"]
            out.append(f'<p class="idx-group">{cur}　{b["part"]["title"]}</p>')
            out.append("<ul>")
        target = b["id"] or f'ch{b["ch"]["n"]:02d}'
        lead = clip_keep_math(b["lead"], 90)
        out.append(
            f'<li><a href="#{target}"><span class="idx-term">反例{b["num"]}　'
            f'{b["title"]}</span></a>'
            + (f'<span class="hanrei-lead">　{lead}</span>' if lead else "")
            + "</li>")
        total += 1
    if cur is not None:
        out.append("</ul>")
    out.append("</div>")
    out.insert(2, f'<p class="no-indent">収録 {total} 項目。</p>')
    return "\n".join(out)


def main() -> None:
    target = CONTENT / "zz-appendix"
    target.mkdir(parents=True, exist_ok=True)
    (target / "B-teigishu.html").write_text(build_definitions() + "\n", encoding="utf-8")
    (target / "C-hanrei.html").write_text(build_counterexamples() + "\n", encoding="utf-8")
    (target / "D-zuhan-sakuin.html").write_text(build_figure_index() + "\n", encoding="utf-8")
    (target / "G-sakuin.html").write_text(build_index() + "\n", encoding="utf-8")
    print("付録B・C・D・Gを生成しました")


if __name__ == "__main__":
    main()
