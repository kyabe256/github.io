#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英単語語源大辞典 — ビルドスクリプト
src/*.txt (独自の軽量マークアップ) を読み込み、HTML を組み立てて WeasyPrint で PDF 化する。
"""
import os, re, sys, html, datetime, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "src")
DIST = os.path.join(BASE, "dist")

# ---------------------------------------------------------------- manifest
# (ファイル名, セクション種別)  種別: prose / entry
MANIFEST = [
    ("00_preface.txt",      "prose"),
    ("01_howto.txt",        "prose"),
    ("10_chap01.txt",       "prose"),
    ("11_chap02.txt",       "prose"),
    ("12_chap03.txt",       "prose"),
    ("13_chap04.txt",       "prose"),
    ("14_chap05.txt",       "prose"),
    ("15_chap06.txt",       "prose"),
    ("16_chap07.txt",       "prose"),
    ("17_chap08.txt",       "prose"),
    ("18_chap09.txt",       "prose"),
    ("19_chap10.txt",       "prose"),
    ("1a_chap11.txt",       "prose"),
    ("1b_chap12.txt",       "prose"),
    ("1c_chap13.txt",       "prose"),
    ("1d_chap14.txt",       "prose"),
    ("1e_chap15.txt",       "prose"),
    ("20_pie_roots.txt",    "entry"),
    ("29_latin_intro.txt",  "prose"),
    ("30_latin_stems.txt",  "entry"),
    ("31_greek_stems.txt",  "entry"),
    ("40_affixes.txt",      "entry"),
    ("50_dict_a.txt",       "entry"),
    ("51_dict_b.txt",       "entry"),
    ("52_dict_c.txt",       "entry"),
    ("53_dict_d.txt",       "entry"),
    ("54_dict_e.txt",       "entry"),
    ("55_dict_f.txt",       "entry"),
    ("56_dict_g.txt",       "entry"),
    ("57_dict_h.txt",       "entry"),
    ("58_dict_i.txt",       "entry"),
    ("59_dict_j.txt",       "entry"),
    ("60_dict_k.txt",       "entry"),
    ("61_dict_l.txt",       "entry"),
    ("62_dict_m.txt",       "entry"),
    ("63_dict_n.txt",       "entry"),
    ("64_dict_o.txt",       "entry"),
    ("65_dict_p.txt",       "entry"),
    ("66_dict_q.txt",       "entry"),
    ("67_dict_r.txt",       "entry"),
    ("68_dict_s.txt",       "entry"),
    ("69_dict_t.txt",       "entry"),
    ("70_dict_u.txt",       "entry"),
    ("71_dict_v.txt",       "entry"),
    ("72_dict_w.txt",       "entry"),
    ("73_dict_xyz.txt",     "entry"),
    ("74_field_a.txt",      "entry"),
    ("74_field_b.txt",      "entry"),
    ("74_field_c.txt",      "entry"),
    ("74_field_d.txt",      "entry"),
    ("76_loan_a.txt",       "entry"),
    ("76_loan_b.txt",       "entry"),
    ("80_topics.txt",       "prose"),
    ("85_myths.txt",        "prose"),
    ("88_study.txt",        "prose"),
    ("90_appendix.txt",     "prose"),
    ("95_biblio.txt",       "prose"),
]

# フィールドラベル
LABELS = {
    "lit":   "原義",
    "chain": "語源系統",
    "root":  "印欧語根",
    "desc":  None,          # ラベルなし本文
    "cog":   "同根語",
    "der":   "派生・関連語",
    "dbl":   "二重語",
    "eng":   "英語への流入",
    "form":  "語形",
    "first": "初出",
    "ex":    "用例",
    "conf":  "確実度",
    "note":  "ノート",
    "see":   "この語根から",
    "cf":    "参照",
}
ORDER = ["lit", "root", "chain", "first", "desc", "form", "cog", "der", "dbl",
         "eng", "ex", "conf", "note", "see", "cf"]

# 確実度ラベル → CSS クラス
CONF_CLASS = {
    "確実": "c-sure", "通説": "c-std", "一説": "c-one", "不確実": "c-vague",
    "誤り": "c-false", "俗説": "c-false",
}

_id_counter = [0]
def new_id(prefix="e"):
    _id_counter[0] += 1
    return "%s%d" % (prefix, _id_counter[0])

def sortkey(s):
    s = re.sub(r"^[*\-‐-―]+", "", s)
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return (s.lower(), s)

# 収集用
TOC = []        # (level, title, id)
INDEX_EN = []   # (display, id)
INDEX_ROOT = [] # (display, id)
INDEX_AFF = []  # (display, id)
INDEX_FIELD = []   # 分野別語彙
INDEX_EPONYM = []  # 人名・地名由来語
INDEXES = {"en": INDEX_EN, "root": INDEX_ROOT, "aff": INDEX_AFF,
           "field": INDEX_FIELD, "eponym": INDEX_EPONYM}

# 人名・地名に由来する見出し語。どのファイルにあっても人名・地名由来語索引に載せる。
# （:: index の指定とは独立に、見出し語そのもので判定する）
EPONYMS = set("""
academy algorithm atlas attic boycott bungalow canary cashmere copper czar dollar
dunce frank franchise gerrymander ghetto guy hooligan janitor jeans jockey jovial
juggernaut jumbo laconic lumber lunatic lyceum magpie marathon martial mausoleum
meander mesmerize nickel palace pamphlet pandemonium panic posh quixotic romance
sandwich scot-free shrapnel silhouette siren slave stoic suede tabby tantalize
tawdry turquoise tuxedo utopia vandal vaudeville volcano yankee zeppelin
""".split())

# 図版（figures.py があれば読み込む）
try:
    from figures import FIGURES
except Exception:
    FIGURES = {}
FIG_SEEN = []   # (番号, 名前, キャプション, id)

# ---------------------------------------------------------------- parser
class Parser:
    def __init__(self, kind):
        self.kind = kind
        self.out = []
        self.para = []
        self.list_mode = None
        self.in_entry = False
        self.entry_fields = []
        self.entry_head = None
        self.table = None
        self.index_target = None   # "en" / "root" / "aff" / None
        self.ebuf = []             # 整列待ちのエントリー

    # --- low level
    def flush_para(self):
        if self.para:
            self.out.append("<p>%s</p>" % " ".join(self.para).strip())
            self.para = []

    def flush_list(self):
        if self.list_mode:
            self.out.append("</%s>" % self.list_mode)
            self.list_mode = None

    def flush_table(self):
        if self.table is not None:
            rows = self.table
            sep = None
            for i, r in enumerate(rows):
                if r and all(re.fullmatch(r"-{2,}", c.strip()) for c in r):
                    sep = i
                    break
            head_rows = rows[:sep] if sep else (rows[:1] if len(rows) > 1 else [])
            body_rows = rows[sep + 1:] if sep is not None else rows[len(head_rows):]
            buf = ['<table class="tbl">']
            if head_rows:
                buf.append("<thead>")
                for r in head_rows:
                    buf.append("<tr>" + "".join("<th>%s</th>" % c for c in r) + "</tr>")
                buf.append("</thead>")
            buf.append("<tbody>")
            for r in body_rows:
                buf.append("<tr>" + "".join("<td>%s</td>" % c for c in r) + "</tr>")
            buf.append("</tbody></table>")
            self.out.append("\n".join(buf))
            self.table = None

    def flush_entry(self):
        if not self.in_entry:
            return
        buf = ['<div class="entry" id="%s">' % self.entry_head["id"]]
        # 重要度 ★ は見出し行に出す（フィールドとしては出力しない）
        head_html = self.entry_head["html"]
        lvls = [v for (k, v) in self.entry_fields if k == "lvl"]
        if lvls:
            n = lvls[0].count("★") or len(lvls[0].strip()) or 1
            n = max(1, min(3, n))
            head_html += ' <span class="stars">%s</span>' % ("★" * n)
        self.entry_fields = [(k, v) for (k, v) in self.entry_fields if k != "lvl"]
        buf.append('<p class="hw">%s</p>' % head_html)
        for key in ORDER:
            vals = [v for (k, v) in self.entry_fields if k == key]
            if not vals:
                continue
            label = LABELS.get(key)
            for v in vals:
                if label is None:
                    buf.append('<p class="ebody">%s</p>' % v)
                elif key == "chain":
                    buf.append('<p class="chain"><span class="lb">%s</span>%s</p>' % (label, v))
                elif key == "conf":
                    head = v.split("　")[0].split(" ")[0].strip("／/")
                    cls = CONF_CLASS.get(head, "c-std")
                    rest = v[len(head):].lstrip("　 ")
                    buf.append('<p class="fld"><span class="lb">%s</span>'
                               '<span class="conf %s">%s</span>%s</p>'
                               % (label, cls, head, ("　" + rest) if rest else ""))
                else:
                    buf.append('<p class="fld"><span class="lb">%s</span>%s</p>' % (label, v))
        # 未知キーも落とさない
        known = set(ORDER)
        for (k, v) in self.entry_fields:
            if k not in known:
                buf.append('<p class="fld"><span class="lb">%s</span>%s</p>' % (html.escape(k), v))
        buf.append("</div>")
        disp = re.sub(r"<[^>]+>", "", self.entry_head["raw"])
        self.ebuf.append((sortkey(disp), "\n".join(buf)))
        self.in_entry = False
        self.entry_fields = []

    def flush_entries(self):
        """バッファ中のエントリーを見出し語順に整列して出力する。"""
        if self.ebuf:
            self.ebuf.sort(key=lambda x: x[0])
            self.out.extend(h for _, h in self.ebuf)
            self.ebuf = []

    def flush_all(self):
        self.flush_para(); self.flush_list(); self.flush_table(); self.flush_entry()
        self.flush_entries()

    # --- main
    def feed(self, text):
        for raw in text.split("\n"):
            line = raw.rstrip()
            s = line.strip()

            if s.startswith("%%"):       # コメント
                continue

            if not s:
                self.flush_para(); self.flush_list(); self.flush_table()
                continue

            # 索引ターゲット指定 :: index en|root|aff|none
            if s.startswith(":: index"):
                self.flush_all()
                v = s.split()[-1]
                self.index_target = None if v == "none" else v
                continue

            # 見出し
            m = re.match(r"^(#{1,4})\s+(.*)$", s)
            if m:
                self.flush_all()
                lv = len(m.group(1))
                title = m.group(2).strip()
                hid = new_id("h")
                if lv <= 2:
                    TOC.append((lv, title, hid))
                cls = {1: "h1", 2: "h2", 3: "h3", 4: "h4"}[lv]
                self.out.append('<h%d id="%s" class="%s">%s</h%d>' % (lv, hid, cls, title, lv))
                continue

            # 図版　%fig 名前 ; キャプション
            if s.startswith("%fig "):
                self.flush_all()
                body = s[5:].strip()
                name, _, cap = body.partition(";")
                name = name.strip(); cap = cap.strip()
                svg = FIGURES.get(name)
                if svg is None:
                    sys.stderr.write("  [warn] 図版が見つかりません: %s\n" % name)
                    continue
                fid = new_id("f")
                num = len(FIG_SEEN) + 1
                FIG_SEEN.append((num, name, cap, fid))
                self.out.append(
                    '<figure id="%s">%s<figcaption>図 %d　%s</figcaption></figure>'
                    % (fid, svg, num, cap))
                continue

            # 語群見出し(アルファベット区切りなど)
            if s.startswith("=="):
                self.flush_all()
                self.out.append('<p class="alphamark">%s</p>' % s.lstrip("=").strip())
                continue

            # エントリー
            if s.startswith("@ "):
                self.flush_para(); self.flush_list(); self.flush_table(); self.flush_entry()
                body = s[2:].strip()
                parts = [p.strip() for p in body.split(" ; ")]
                hw = parts[0]
                eid = new_id("w")
                rest = parts[1:]
                h = '<span class="hwword">%s</span>' % hw
                if rest:
                    h += " " + " ".join(
                        ('<span class="hwmeta">%s</span>' % r) for r in rest)
                self.entry_head = {"id": eid, "html": h, "raw": hw}
                self.in_entry = True
                self.entry_fields = []
                disp = re.sub(r"<[^>]+>", "", hw)
                bucket = INDEXES.get(self.index_target)
                if bucket is not None:
                    bucket.append((disp, eid))
                if disp.strip().lower() in EPONYMS:
                    INDEX_EPONYM.append((disp, eid))
                continue

            # エントリーのフィールド
            m = re.match(r"^\+(\w+):\s*(.*)$", s)
            if m and self.in_entry:
                self.entry_fields.append((m.group(1), m.group(2).strip()))
                continue

            # 表
            if s.startswith("|"):
                self.flush_para(); self.flush_list()
                cells = [c.strip() for c in s.strip("|").split("|")]
                if self.table is None:
                    self.table = []
                self.table.append(cells)
                continue

            # 注記ボックス
            if s.startswith("> "):
                self.flush_para(); self.flush_list(); self.flush_table()
                self.out.append('<div class="note">%s</div>' % s[2:].strip())
                continue

            # 箇条書き
            m = re.match(r"^-\s+(.*)$", s)
            if m:
                self.flush_para(); self.flush_table()
                if self.list_mode != "ul":
                    self.flush_list(); self.out.append("<ul>"); self.list_mode = "ul"
                self.out.append("<li>%s</li>" % m.group(1))
                continue
            m = re.match(r"^\d+\.\s+(.*)$", s)
            if m:
                self.flush_para(); self.flush_table()
                if self.list_mode != "ol":
                    self.flush_list(); self.out.append("<ol>"); self.list_mode = "ol"
                self.out.append("<li>%s</li>" % m.group(1))
                continue

            # 通常段落
            self.flush_list(); self.flush_table()
            if self.in_entry:
                # エントリー中の素の行は desc 扱い
                self.entry_fields.append(("desc", s))
            else:
                self.para.append(s)

        self.flush_all()
        return "\n".join(self.out)

# ---------------------------------------------------------------- css
CSS = r"""
@page {
  size: A5;
  margin: 15mm 13mm 16mm 13mm;
  @bottom-center {
     content: counter(page);
     font-family: "Liberation Serif", serif; font-size: 8.5pt; color: #444;
     vertical-align: top; padding-top: 3mm;
  }
  @top-left {
     content: string(runhead);
     font-family: "Liberation Serif","DejaVu Serif","IPAGothic",serif;
     font-size: 7.5pt; color: #7a7f86; letter-spacing: .04em;
     vertical-align: bottom; padding-bottom: 2.5mm;
  }
}
/* 辞書パートだけ、右肩にそのページの見出し語範囲（柱）を出す */
@page dict {
  @top-right {
     content: string(hw, first) "　—　" string(hw, last);
     font-family: "Liberation Serif","DejaVu Serif","IPAGothic",serif;
     font-size: 8pt; color: #24507a; font-weight: bold; letter-spacing: .02em;
     vertical-align: bottom; padding-bottom: 2.5mm;
  }
}
@page cover { margin: 0; @bottom-center { content: none } @top-center { content: none } }
@page :first { @bottom-center { content: none } @top-center { content: none } }

html { font-size: 9.6pt; }
body {
  font-family: "Liberation Serif","DejaVu Serif","FreeSerif","IPAGothic",serif;
  line-height: 1.62; color: #16181c; text-align: justify;
  -weasy-hyphens: auto;
}
p { margin: 0 0 .42em 0; text-indent: 1em; }
p.noind, li p { text-indent: 0; }

h1 {
  string-set: runhead content();
  break-before: page;
  font-size: 17pt; line-height: 1.35; margin: 6mm 0 5mm 0;
  padding-bottom: 2.5mm; border-bottom: 1.1pt solid #1a1a1a;
  font-weight: bold; letter-spacing: .02em; text-align: left;
}
h2 { font-size: 12.4pt; margin: 5.5mm 0 2.2mm; padding-left: 2.4mm;
     border-left: 3pt solid #333; line-height: 1.35; break-after: avoid; text-align: left; }
h3 { font-size: 10.6pt; margin: 4mm 0 1.5mm; color: #1e1e1e; break-after: avoid; text-align: left; }
h3::before { content: "◆ "; color:#666; }
h4 { font-size: 9.8pt; margin: 3mm 0 1mm; break-after: avoid; text-align: left; }
h1 + p, h2 + p, h3 + p, h4 + p { text-indent: 0; }

ul, ol { margin: .3em 0 .6em 1.3em; padding: 0; }
li { margin: 0 0 .18em 0; text-align: justify; }

.note {
  border: .4pt solid #999; background: #f4f4f2; padding: 2.2mm 2.6mm;
  margin: 2.4mm 0; font-size: 8.9pt; line-height: 1.55; break-inside: avoid;
}
.note b:first-child { color:#000; }

table.tbl { border-collapse: collapse; width: 100%; margin: 2.2mm 0 3mm;
            font-size: 8.5pt; line-height: 1.42; }
table.tbl thead { display: table-header-group; }
table.tbl tr { break-inside: avoid; }
table.tbl th { background: #e8e8e6; border: .4pt solid #888; padding: 1.1mm 1.4mm;
               text-align: left; font-weight: bold; }
table.tbl td { border: .4pt solid #999; padding: 1.1mm 1.4mm; vertical-align: top; text-align: left; }

/* ---- 辞書エントリー ---- */
.entry { margin: 0 0 2.6mm 0; padding: 0 0 1.6mm 0; border-bottom: .3pt solid #dcdcdc;
         orphans: 2; widows: 2; }
p.hw { text-indent: 0; margin: 0 0 .5mm 0; line-height: 1.4; break-after: avoid; }
p.fld b, p.chain b, p.ebody b { color: #24507a; font-weight: bold; }
p.fld i, p.chain i { font-style: italic; }
.hwword { font-size: 11.4pt; font-weight: bold; letter-spacing: .01em;
          string-set: hw content(); }
.sec.entry { page: dict; }
.stars { font-size: 7.6pt; color: #c8952a; letter-spacing: .06em; vertical-align: .12em; }
.conf { font-size: 7.4pt; padding: 0 .35em; border-radius: 1pt; color: #fff; }
.c-sure  { background: #1E7A46; }
.c-std   { background: #24507a; }
.c-one   { background: #8a6d1f; }
.c-vague { background: #7a7f86; }
.c-false { background: #b3312c; }

/* ---- 図版 ---- */
figure { margin: 3.5mm 0 4mm; break-inside: avoid; text-align: center; }
figure svg { max-width: 100%; height: auto; }
figcaption { font-size: 7.8pt; color: #555; margin-top: 1.6mm; text-align: center;
             line-height: 1.5; }
.hwmeta { font-size: 8.6pt; color: #333; margin-left: .35em; }
.hwmeta::before { content: "〔"; color:#888; }
.hwmeta::after  { content: "〕"; color:#888; }
p.ebody { text-indent: 0; margin: 0 0 .34em 0; font-size: 9.2pt; line-height: 1.6; }
p.fld, p.chain { text-indent: 0; margin: 0 0 .3em 0; font-size: 8.7pt;
                 line-height: 1.55; padding-left: 6.6em; }
p.fld > .lb, p.chain > .lb {
  display: inline-block; width: 6.2em; margin-left: -6.6em; white-space: nowrap;
  font-size: 7.1pt; color: #fff; background: #555; text-align: center;
  border-radius: 1pt; padding: 0 .2em; letter-spacing: .02em;
}
p.chain { font-size: 8.9pt; }
p.chain > .lb { background: #24507a; }
.alphamark {
  text-indent: 0; break-before: page; font-size: 30pt; font-weight: bold;
  letter-spacing: .06em; margin: 2mm 0 4mm; padding-bottom: 1.5mm;
  border-bottom: 2pt solid #222; color: #222;
}

/* ---- 表紙 ---- */
.cover { page: cover; break-after: page; height: 210mm; position: relative; color:#fff;
         background: #16233a; }
.cover .inner { position: absolute; top: 38mm; left: 16mm; right: 16mm; }
.cover .jt { font-size: 30pt; font-weight: bold; line-height: 1.28; letter-spacing: .04em; }
.cover .et { font-size: 11.5pt; margin-top: 7mm; letter-spacing: .1em; color:#c8d4e6; line-height:1.5;}
.cover .rule { border-top: 1.4pt solid #8fa6c8; margin: 8mm 0 6mm; }
.cover .sub { font-size: 9.6pt; line-height: 1.9; color: #dde5f0; }
.cover .foot { position: absolute; bottom: 18mm; left: 16mm; right: 16mm;
               font-size: 8.6pt; color: #a9bad4; border-top:.5pt solid #56688a; padding-top:3mm;}

/* ---- 目次・索引 ---- */
.toc a, .idx a { text-decoration: none; color: #000; }
.toc ul { list-style: none; margin: 0; padding: 0; }
.toc li.l1 { margin: 2.2mm 0 .6mm; font-weight: bold; font-size: 9.8pt; }
.toc li.l2 { margin: 0 0 .3mm 1.4em; font-size: 8.8pt; }
.toc a::after { content: leader('.') target-counter(attr(href), page); color:#555; }
.idxwrap { columns: 3; column-gap: 4mm; column-rule: .3pt solid #ccc; font-size: 7.8pt;
           line-height: 1.45; }
.idxwrap p { text-indent: 0; margin: 0 0 .1em 0; break-inside: avoid; }
.idxwrap a::after { content: "  " target-counter(attr(href), page); color:#555; }
.idxhead { break-inside: avoid; font-weight: bold; font-size: 9pt; margin: 1.6mm 0 .6mm;
           border-bottom: .4pt solid #999; }
i, em { font-style: italic; }
b, strong { font-weight: bold; }
code, .mono { font-family: "DejaVu Sans Mono", monospace; font-size: .88em; }
.pie { font-style: italic; }
sup { font-size: .7em; vertical-align: super; }
a { color: #000; text-decoration: none; }
"""

# ---------------------------------------------------------------- build
STATS = ""

def build():
    global STATS
    body = []
    today = datetime.date.today()

    n_entries = 0
    for fn, kind in MANIFEST:
        fp = os.path.join(SRC, fn)
        if os.path.exists(fp):
            with open(fp, encoding="utf-8") as f:
                n_entries += sum(1 for ln in f if ln.startswith("@ "))
    prev = os.path.join(DIST, "english-etymology-dictionary.pdf")
    n_pages = None
    try:
        import pypdf
        n_pages = len(pypdf.PdfReader(prev).pages)
    except Exception:
        pass
    STATS = "全%s項目" % format(n_entries, ",")
    if n_pages:
        STATS += "／全%s ページ" % format(n_pages, ",")

    # 表紙
    body.append("""
<div class="cover"><div class="inner">
  <div class="jt">英単語語源大辞典</div>
  <div class="et">A COMPREHENSIVE ETYMOLOGICAL<br>DICTIONARY OF THE ENGLISH LANGUAGE<br>FOR JAPANESE READERS</div>
  <div class="rule"></div>
  <div class="sub">
    印欧祖語から現代英語まで<br>
    語根・接辞・音韻変化・意味変化の全体像
  </div>
  <div class="toc2">
    総説12章／印欧祖語語根辞典／ラテン語語幹辞典／ギリシア語語幹辞典<br>
    接辞辞典／A–Z 語源辞典本体／主題別語源誌／語源の俗説と真説／付録・索引
  </div>
</div>
<div class="foot">%s　%s 版</div></div>
""" % (STATS, today.strftime("%Y年%-m月")))

    # 目次プレースホルダ（後で差し込む）
    body.append("@@TOC@@")

    for fn, kind in MANIFEST:
        path = os.path.join(SRC, fn)
        if not os.path.exists(path):
            sys.stderr.write("  [skip] %s\n" % fn)
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        p = Parser(kind)
        body.append('<section class="sec %s">' % kind)
        body.append(p.feed(text))
        body.append("</section>")
        sys.stderr.write("  [ok]   %s (%d 文字)\n" % (fn, len(text)))

    # 索引
    body.append(build_index())

    doc = "\n".join(body)

    # 目次生成
    toc = ['<section><h1 id="toc-head" class="h1">目次</h1><div class="toc"><ul>']
    for lv, title, hid in TOC:
        if hid == "toc-head":
            continue
        plain = re.sub(r"<[^>]+>", "", title)
        toc.append('<li class="l%d"><a href="#%s">%s</a></li>' % (lv, hid, plain))
    toc.append("</ul></div></section>")
    doc = doc.replace("@@TOC@@", "\n".join(toc))

    page = """<!DOCTYPE html><html lang="ja"><head><meta charset="utf-8">
<title>英単語語源大辞典</title><style>%s</style></head><body>%s</body></html>""" % (CSS, doc)

    os.makedirs(DIST, exist_ok=True)
    hpath = os.path.join(DIST, "index.html")
    with open(hpath, "w", encoding="utf-8") as f:
        f.write(page)

    from weasyprint import HTML
    out = os.path.join(DIST, "english-etymology-dictionary.pdf")
    HTML(string=page, base_url=BASE).write_pdf(out)
    try:
        import pypdf
        n = len(pypdf.PdfReader(out).pages)
    except Exception:
        n = "?"
    sys.stderr.write("\n出力: %s (%s ページ, %.1f MB)\n" %
                     (out, n, os.path.getsize(out) / 1e6))

def group_index(items, title, prefix):
    if not items:
        return ""
    buf = ['<h2>%s</h2><div class="idxwrap">' % title]
    seen = set()
    uniq = []
    for disp, eid in items:
        k = (disp, eid)
        if k in seen:
            continue
        seen.add(k); uniq.append((disp, eid))
    uniq.sort(key=lambda x: sortkey(x[0]))
    cur = None
    for disp, eid in uniq:
        letter = sortkey(disp)[0][:1].upper() or "―"
        if letter != cur:
            cur = letter
            buf.append('<p class="idxhead">%s</p>' % letter)
        buf.append('<p><a href="#%s">%s</a></p>' % (eid, disp))
    buf.append("</div>")
    return "\n".join(buf)

def build_index():
    out = ['<section><h1 class="h1" id="idx-head">索引</h1>']
    TOC.append((1, "索引", "idx-head"))
    out.append(group_index(INDEX_EN,     "英語見出し語索引", "w"))
    out.append(group_index(INDEX_ROOT,   "印欧語根・語幹索引", "r"))
    out.append(group_index(INDEX_AFF,    "接辞索引", "a"))
    out.append(group_index(INDEX_FIELD,  "分野別語彙索引", "d"))
    out.append(group_index(INDEX_EPONYM, "人名・地名由来語索引", "p"))
    out.append("</section>")
    return "\n".join(out)

if __name__ == "__main__":
    build()
