"""教科書本体の HTML を組み立てる。

軽量マークアップ (content/*.txt) を読み、盤面図・表・索引・相互参照を
展開して 1 枚の HTML にする。ページ番号は build.py が 2 パス目に流し込む。
"""

from __future__ import annotations

import html
import json
import os
import re

import shogi
from shogi import (BLACK, WHITE, FU, KY, KE, GI, KI, KA, HI, OU, TO, NY, NK, NG, UM, RY,
                   Position, ptype, pcolor, KANSUJI, ZENSUJI)

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")

BOARD_CH = {FU: "歩", KY: "香", KE: "桂", GI: "銀", KI: "金", KA: "角", HI: "飛", OU: "玉",
            TO: "と", NY: "杏", NK: "圭", NG: "全", UM: "馬", RY: "龍"}
HAND_NAME = {HI: "飛", KA: "角", KI: "金", GI: "銀", KE: "桂", KY: "香", FU: "歩"}


# ------------------------------------------------------------------ 盤面図

class Marker:
    """PDF から頁番号を逆算するための不可視マーカー。"""

    def __init__(self):
        self.n = 0
        self.ids = {}

    def emit(self, key: str) -> str:
        if key in self.ids:
            return ""
        self.n += 1
        self.ids[key] = self.n
        return '<span class="mk">%%m{0}%%</span>'.format(self.n)

    def idof(self, key):
        return self.ids.get(key)


def parse_sq(tok: str):
    """'76' -> (r, c)  (7筋6段)"""
    tok = tok.strip()
    f, r = int(tok[0]), int(tok[1])
    return (r - 1, 9 - f)


def hand_str(pos: Position, color: int) -> str:
    items = []
    for t in [HI, KA, KI, GI, KE, KY, FU]:
        n = pos.hands[color].get(t, 0)
        if n:
            items.append(HAND_NAME[t] + (KANSUJI[n - 1] if 2 <= n <= 9 else
                                         ("十" + (KANSUJI[n - 11] if n > 10 else "")) if n >= 10 else ""))
    return "　".join(items) if items else "なし"


def board_html(sfen: str, caption: str = "", hl=(), marker=None, key=None, cls="") -> str:
    pos = Position.from_sfen(sfen)
    hlset = set(parse_sq(x) for x in hl if x)
    rows = []
    head = "".join('<th class="f">%s</th>' % ZENSUJI[8 - c] for c in range(9))
    rows.append('<tr><th class="corner"></th>%s<th class="corner"></th></tr>' % head)
    for r in range(9):
        cells = []
        for c in range(9):
            p = pos.get(r, c)
            k = ' hl' if (r, c) in hlset else ''
            if p is None:
                cells.append('<td class="sq%s"></td>' % k)
            else:
                side = "b" if pcolor(p) == BLACK else "w"
                ch = BOARD_CH[ptype(p)]
                cells.append('<td class="sq%s"><span class="pc %s">%s</span></td>' % (k, side, ch))
        rows.append('<tr><th class="corner"></th>%s<th class="r">%s</th></tr>' % ("".join(cells), KANSUJI[r]))
    mk = marker.emit(key) if (marker and key) else ""
    cap = '<figcaption>%s%s</figcaption>' % (mk, caption) if caption else ""
    return ('<figure class="board %s">'
            '<div class="hand gote">後手持駒　%s</div>'
            '<table class="ban">%s</table>'
            '<div class="hand sente">先手持駒　%s</div>%s</figure>') % (
        cls, hand_str(pos, WHITE), "".join(rows), hand_str(pos, BLACK), cap)


def kanji_num(n: int) -> str:
    """1..999 を漢数字にする（奥付・扉用）。"""
    d = "〇一二三四五六七八九"
    if n < 10:
        return d[n]
    if n < 100:
        t, o = divmod(n, 10)
        return ("" if t == 1 else d[t]) + "十" + (d[o] if o else "")
    h, r = divmod(n, 100)
    return ("" if h == 1 else d[h]) + "百" + (kanji_num(r) if r else "")


# ------------------------------------------------------------------ 用語

def load_glossary():
    with open(os.path.join(CONTENT, "glossary.json"), encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------------ 本文パーサ

INLINE_RE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"(?<!\*)\*([^*\n]+?)\*(?!\*)"), r"<em>\1</em>"),
    (re.compile(r"`(.+?)`"), r"<code>\1</code>"),
]


class Book:
    def __init__(self, pagemap=None, tsume=None, hisshi=None):
        self.marker = Marker()
        self.pagemap = pagemap or {}
        self.out = []
        self.toc = []          # (level, number, title, key)
        self.index = {}        # term -> set of keys
        self.glossary = load_glossary()
        self.terms = sorted(self.glossary.keys(), key=len, reverse=True)
        self.tsume = tsume or []
        self.hisshi = hisshi or []
        self.fig_no = 0
        self.chapter = 0
        self.seen_terms = set()
        self.problem_no = 0
        self.problems = []     # (no, sfen, moves, pv, key)
        self.exercise = []

    # -- ページ番号 ---------------------------------------------------
    def page_of(self, key):
        mid = self.marker.idof(key)
        if mid is None:
            return None
        return self.pagemap.get(str(mid))

    def pn_span(self, key, cls="pn"):
        p = self.page_of(key)
        return '<span class="%s">%s</span>' % (cls, p if p else "&nbsp;")

    # -- インライン ---------------------------------------------------
    def inline(self, s: str, mark_terms=True) -> str:
        s = html.escape(s)
        s = s.replace("--", "—")
        for rx, rep in INLINE_RE:
            s = rx.sub(rep, s)
        # 相互参照 {{key|表示}}
        def xref(m):
            key = m.group(1)
            label = m.group(2) or ""
            return '%s<span class="xref">（%s頁）</span>' % (label, self.pn_span(key))
        s = re.sub(r"\{\{([A-Za-z0-9_.:-]+)\|([^}]*)\}\}", xref, s)
        if mark_terms:
            s = self.mark_terms(s)
        return s

    def mark_terms(self, s: str) -> str:
        for term in self.terms:
            if term in self.seen_terms:
                continue
            idx = s.find(term)
            if idx < 0:
                continue
            key = "ix:%s:%d" % (term, self.chapter)
            mk = self.marker.emit(key)
            self.index.setdefault(term, []).append(key)
            self.seen_terms.add(term)
            s = s[:idx] + mk + '<span class="ixt">' + term + "</span>" + s[idx + len(term):]
        return s

    # -- ブロック -----------------------------------------------------
    def add(self, h):
        self.out.append(h)

    def parse(self, text: str):
        lines = text.split("\n")
        i = 0
        para = []

        def flush():
            if para:
                self.add("<p>%s</p>" % self.inline("".join(para).strip()))
                para.clear()

        while i < len(lines):
            ln = lines[i]
            s = ln.strip()
            if not s:
                flush()
                i += 1
                continue
            if s.startswith("@"):
                flush()
                i = self.directive(s, lines, i)
                continue
            if s.startswith("#"):
                flush()
                lvl = len(s) - len(s.lstrip("#"))
                title = s.lstrip("#").strip()
                self.heading(lvl, title)
                i += 1
                continue
            if s.startswith("- "):
                flush()
                items = []
                while i < len(lines) and lines[i].strip().startswith("- "):
                    items.append("<li>%s</li>" % self.inline(lines[i].strip()[2:]))
                    i += 1
                self.add("<ul>%s</ul>" % "".join(items))
                continue
            if re.match(r"^\d+\.\s", s):
                flush()
                items = []
                while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                    items.append("<li>%s</li>" % self.inline(re.sub(r"^\d+\.\s", "", lines[i].strip())))
                    i += 1
                self.add("<ol>%s</ol>" % "".join(items))
                continue
            if s.startswith("|"):
                flush()
                rows = []
                while i < len(lines) and lines[i].strip().startswith("|"):
                    rows.append(lines[i].strip())
                    i += 1
                self.add(self.table(rows))
                continue
            if s.startswith(">"):
                flush()
                buf = []
                while i < len(lines) and lines[i].strip().startswith(">"):
                    buf.append(lines[i].strip()[1:].strip())
                    i += 1
                self.add('<div class="note"><p>%s</p></div>' % self.inline(" ".join(buf)))
                continue
            para.append(s)
            i += 1
        flush()

    def table(self, rows):
        cells = [[c.strip() for c in r.strip("|").split("|")] for r in rows]
        cells = [r for r in cells if not all(set(c) <= set("-: ") for c in r)]
        out = ["<table class=\"tbl\">"]
        for n, row in enumerate(cells):
            tag = "th" if n == 0 else "td"
            out.append("<tr>%s</tr>" % "".join("<%s>%s</%s>" % (tag, self.inline(c), tag) for c in row))
        out.append("</table>")
        return "".join(out)

    def heading(self, lvl, title):
        if lvl == 1:
            self.chapter += 1
            self.seen_terms = set()   # 索引は章ごとの初出を拾う
            key = "ch:%d" % self.chapter
            mk = self.marker.emit(key)
            self.toc.append((1, "第%d章" % self.chapter, title, key))
            self.add('<section class="chapter"><h1 id="%s"><span class="chno">第%s章</span>'
                     '<span class="chtitle">%s%s</span></h1>' % (key, self.chapter, mk, self.inline(title, False)))
        elif lvl == 2:
            key = "sec:%d:%d" % (self.chapter, len([t for t in self.toc if t[0] == 2]) + 1)
            mk = self.marker.emit(key)
            self.toc.append((2, "", title, key))
            self.add('<h2 id="%s">%s%s</h2>' % (key, mk, self.inline(title, False)))
        elif lvl == 3:
            self.add("<h3>%s</h3>" % self.inline(title, False))
        else:
            self.add("<h4>%s</h4>" % self.inline(title, False))

    # -- ディレクティブ ------------------------------------------------
    def directive(self, s, lines, i):
        m = re.match(r"^@(\w+)\s*(.*)$", s)
        name, rest = m.group(1), m.group(2)
        args = [a.strip() for a in rest.split("|")]
        if name == "part":
            key = "part:%s" % args[0]
            mk = self.marker.emit(key)
            self.toc.append((0, args[0], args[1], key))
            self.add('<section class="part" id="%s"><div class="partbox">'
                     '<div class="partno">第%s部</div><div class="parttitle">%s%s</div>'
                     '<div class="partlead">%s</div></div></section>'
                     % (key, args[0], mk, args[1], self.inline(args[2] if len(args) > 2 else "", False)))
            return i + 1
        if name == "board":
            self.fig_no += 1
            sfen = args[0]
            cap = args[1] if len(args) > 1 else ""
            hl = []
            cls = ""
            for a in args[2:]:
                if a.startswith("hl="):
                    hl = a[3:].split(",")
                elif a.startswith("cls="):
                    cls = a[4:]
            key = "fig:%d" % self.fig_no
            label = "第%d図" % self.fig_no
            self.add(board_html(sfen, "%s　%s" % (label, self.inline(cap, False)) if cap else label,
                                hl, self.marker, key, cls))
            return i + 1
        if name == "mate":
            # 詰み形であることをビルド時に検証する
            sfen = args[0]
            if len(sfen.split()) == 1:      # 盤面だけなら玉方の手番とみなす
                sfen += " w - 1"
            pos = Position.from_sfen(sfen)
            if pos.turn != WHITE:
                raise ValueError("@mate は後手番で書くこと: " + sfen)
            if not pos.in_check(WHITE) or pos.evasions():
                raise ValueError("@mate: 詰んでいない局面 " + sfen)
            self.fig_no += 1
            key = "fig:%d" % self.fig_no
            cap = args[1] if len(args) > 1 else ""
            hl = []
            for a in args[2:]:
                if a.startswith("hl="):
                    hl = a[3:].split(",")
            self.add(board_html(sfen, "第%d図　%s【詰み】" % (self.fig_no, self.inline(cap, False)),
                                hl, self.marker, key))
            return i + 1
        if name == "mateline":
            # 実戦形の詰み。手順はソルバに解かせ、図と手順の一致を保証する
            sfen, cap = args[0], (args[1] if len(args) > 1 else "")
            pos = Position.from_sfen(sfen)
            n = None
            for d in (1, 3, 5, 7, 9):
                n = shogi.mate_in(pos, d)
                if n:
                    break
            if not n:
                raise ValueError("@mateline: 詰みが見つからない " + sfen)
            pv = shogi.line_str(shogi.principal_variation(pos, n), sep="")
            self.fig_no += 1
            key = "fig:%d" % self.fig_no
            self.add(board_html(sfen, "第%d図　%s（先手番・%d手詰）" % (self.fig_no, self.inline(cap, False), n),
                                (), self.marker, key))
            self.add('<div class="kifuline">%s</div>' % pv)
            self.add('<div class="clearfix"></div>')
            return i + 1
        if name == "hisshi":
            n = int(args[0])
            p = self.hisshi[n]
            self.fig_no += 1
            key = "fig:%d" % self.fig_no
            self.add(board_html(p["sfen"], "第%d図　先手番。一手必至を掛けよ" % self.fig_no,
                                (), self.marker, key))
            defs = "".join("<li>%s　……　%s</li>" % (d, pv) for d, pv in p["defences"])
            self.add('<div class="note"><p><strong>正解　%s</strong>。'
                     'この一手で、後手がどう応じても詰みを逃れられない'
                     '（全%d通りの応手を完全探索で検証）。主な変化は次のとおり。</p>'
                     '<ul class="hs">%s</ul></div>' % (p["move"], p["n_def"], defs))
            self.add('<div class="clearfix"></div>')
            return i + 1
        if name == "box":
            title = args[0]
            buf = []
            i += 1
            while i < len(lines) and lines[i].strip() != "@endbox":
                buf.append(lines[i])
                i += 1
            saved, self.out = self.out, []
            self.parse("\n".join(buf))
            inner, self.out = "".join(self.out), saved
            self.add('<div class="tbox"><div class="tboxhead">%s</div>%s</div>'
                     % (self.inline(title, False), inner))
            return i + 1
        if name in ("h1", "apx"):
            if name == "apx":
                label, title = "付録%s" % args[0], args[1]
            else:
                label, title = "", args[0]
            key = "fm:%d" % (len(self.toc) + 1)
            mk = self.marker.emit(key)
            self.toc.append((1, label, title, key))
            lbl = ('<span class="chno">%s</span>' % label) if label else ""
            self.add('<section class="chapter %s"><h1 id="%s">%s<span class="chtitle">%s%s</span></h1>'
                     % ("" if label else "frontmatter", key, lbl, mk, title))
            return i + 1
        if name == "pagebreak":
            self.add('<div class="pagebreak"></div>')
            return i + 1
        if name == "problems":
            n = int(args[0])
            self.emit_problems(n)
            return i + 1
        if name == "answers":
            self.emit_answers()
            return i + 1
        if name == "glossary":
            self.emit_glossary()
            return i + 1
        if name == "index":
            self.add('<div class="idx-placeholder"></div>')
            return i + 1
        if name == "toc":
            self.add('<div class="toc-placeholder"></div>')
            return i + 1
        if name == "kifu":
            self.emit_kifu(args[0])
            return i + 1
        if name == "raw":
            buf = []
            i += 1
            while i < len(lines) and lines[i].strip() != "@endraw":
                buf.append(lines[i])
                i += 1
            self.add("\n".join(buf))
            return i + 1
        raise ValueError("unknown directive: " + s)

    # -- 詰将棋 -------------------------------------------------------
    def emit_problems(self, moves):
        probs = [p for p in self.tsume if p["moves"] == moves]
        self.add('<div class="probgrid">')
        for p in probs:
            self.problem_no += 1
            key = "prob:%d" % self.problem_no
            self.problems.append((self.problem_no, p, key))
            self.add(board_html(p["sfen"], "第%d問（%d手詰）" % (self.problem_no, moves),
                                (), self.marker, key, cls="small"))
        self.add("</div>")

    def emit_answers(self):
        self.add('<div class="answers">')
        for no, p, key in self.problems:
            self.add('<p class="ans"><span class="ansno">第%d問</span>'
                     '<span class="anspv">%s</span>'
                     '<span class="anssfen">%s</span></p>' % (no, p["pv"], html.escape(p["sfen"])))
        self.add("</div>")

    def emit_glossary(self):
        self.add('<dl class="glossary">')
        for term in sorted(self.glossary, key=lambda t: self.glossary[t][0]):
            yomi, desc = self.glossary[term][0], self.glossary[term][1]
            key = "gl:%s" % term
            mk = self.marker.emit(key)
            self.index.setdefault(term, []).append(key)
            self.add('<dt>%s%s<span class="yomi">（%s）</span></dt><dd>%s</dd>'
                     % (mk, term, yomi, self.inline(desc, False)))
        self.add("</dl>")

    def emit_kifu(self, name):
        import kifu
        line = kifu.LINES[name]
        seq, end = kifu.play(line["moves"])
        moves = kifu.notation(seq)
        self.add('<h3>%s</h3>' % line["title"])
        self.add("<p>%s</p>" % self.inline(line["note"]))
        marks = dict(line["marks"])
        chunks = []
        for i, mv in enumerate(moves, 1):
            chunks.append('<span class="mv"><span class="n">%d</span>%s</span>' % (i, mv))
        self.add('<div class="kifuline">%s</div>' % "".join(chunks))
        for ply, cap in line["marks"]:
            _, pos = kifu.play(line["moves"][:ply])
            self.fig_no += 1
            key = "fig:%d" % self.fig_no
            self.add(board_html(pos.to_sfen(), "第%d図　%s（%d手目まで）" % (self.fig_no, cap, ply),
                                (), self.marker, key, cls="wide"))

    # -- 目次・索引 ---------------------------------------------------
    def toc_html(self):
        out = ['<div class="toc">']
        for lvl, num, title, key in self.toc:
            if lvl == 0:
                out.append('<div class="toc-part">第%s部　%s<span class="dots"></span>%s</div>'
                           % (num, title, self.pn_span(key)))
            elif lvl == 1:
                out.append('<div class="toc-ch">%s%s<span class="dots"></span>%s</div>'
                           % (num + "　" if num else "", title, self.pn_span(key)))
            else:
                out.append('<div class="toc-sec">%s<span class="dots"></span>%s</div>'
                           % (title, self.pn_span(key)))
        out.append("</div>")
        return "".join(out)

    def index_html(self):
        def sortkey(t):
            g = self.glossary.get(t)
            return (g[0] if g else t)
        out = ['<div class="index">']
        for term in sorted(self.index, key=sortkey):
            pages = []
            for k in self.index[term]:
                p = self.page_of(k)
                if p and p not in pages:
                    pages.append(p)
            out.append('<div class="ixrow"><span class="ixterm">%s</span>'
                       '<span class="ixpages">%s</span></div>'
                       % (term, "、".join(str(p) for p in pages) if pages else "&nbsp;"))
        out.append("</div>")
        return "".join(out)


# ------------------------------------------------------------------ 出力

def build_html(order, pagemap=None, tsume=None, hisshi=None, fontdir=""):
    book = Book(pagemap=pagemap, tsume=tsume, hisshi=hisshi)
    for fn in order:
        with open(os.path.join(CONTENT, fn), encoding="utf-8") as f:
            book.parse(f.read())
    body = "".join(book.out)
    body = body.replace('<div class="toc-placeholder"></div>', book.toc_html())
    body = body.replace('<div class="idx-placeholder"></div>', book.index_html())
    body = body.replace("@@STATS@@", "全六部%s章／詰将棋%s題（全題機械検証済）"
                        % (kanji_num(book.chapter), kanji_num(book.problem_no)))
    body = body.replace("@@FIGS@@", kanji_num(book.fig_no))
    body = body.replace("@@TERMS@@", kanji_num(len(book.glossary)))
    body = body.replace("@@LINES@@", kanji_num(len(__import__("kifu").LINES)))
    body = body.replace("@@PROBS@@", kanji_num(book.problem_no))
    # 章 section の閉じ忘れを補う
    body = body.replace('<section class="chapter">', '</section><section class="chapter">', 1000)
    body = body.replace('<section class="part">', '</section><section class="part">', 1000)
    if body.startswith("</section>"):
        body = body[len("</section>"):]
    body += "</section>"
    css = open(os.path.join(HERE, "book.css"), encoding="utf-8").read()
    css = css.replace("@FONTDIR@", fontdir)
    html_doc = ("<!DOCTYPE html><html lang=\"ja\"><head><meta charset=\"utf-8\">"
                "<title>将棋原論</title><style>%s</style></head><body>%s</body></html>"
                % (css, body))
    return html_doc, book
