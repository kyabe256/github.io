# -*- coding: utf-8 -*-
"""
英単語語源大辞典 — 図版生成モジュール

すべての図を SVG 文字列として組み立て、FIGURES に名前で登録する。
本文と同じ色・書体に揃えること（墨 INK ／ 青 BLUE ／ 朱 RED ／ 灰 GRAY）。
座標系は viewBox の user unit。幅 460 が A5 の版面幅（約122mm）に対応する。
"""

INK   = "#16181c"
BLUE  = "#24507a"
RED   = "#b3312c"
GREEN = "#1E7A46"
GOLD  = "#8a6d1f"
GRAY  = "#7a7f86"
RULE  = "#b9c2cc"
FILL  = "#eef2f6"
FILL2 = "#f6f1e8"
PAPER = "#ffffff"

SERIF = "Liberation Serif, DejaVu Serif, IPAGothic, serif"
SANS  = "IPAGothic, Liberation Sans, DejaVu Sans, sans-serif"

# ------------------------------------------------------------------ helpers

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def svg(w, h, body, pad=2):
    return ('<svg viewBox="0 0 %d %d" width="100%%" xmlns="http://www.w3.org/2000/svg" '
            'font-family="%s" text-rendering="geometricPrecision">'
            '<rect x="0" y="0" width="%d" height="%d" fill="%s"/>%s</svg>'
            % (w, h, SANS, w, h, PAPER, body))


def t(x, y, s, size=10, fill=INK, anchor="middle", weight="normal",
      style="normal", family=None, ls=None):
    a = ' font-style="italic"' if style == "italic" else ""
    b = ' font-weight="bold"' if weight == "bold" else ""
    f = ' font-family="%s"' % (family or SANS)
    l = ' letter-spacing="%s"' % ls if ls else ""
    return ('<text x="%.1f" y="%.1f" font-size="%.1f" fill="%s" text-anchor="%s"%s%s%s%s>%s</text>'
            % (x, y, size, fill, anchor, a, b, f, l, esc(s)))


def box(x, y, w, h, fill=PAPER, stroke=INK, sw=1.0, r=2):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" '
            'fill="%s" stroke="%s" stroke-width="%.2f"/>' % (x, y, w, h, r, fill, stroke, sw))


def line(x1, y1, x2, y2, stroke=INK, sw=1.0, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="%.2f"%s/>' % (x1, y1, x2, y2, stroke, sw, d))


def path(d, stroke=INK, sw=1.0, fill="none", dash=None):
    da = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<path d="%s" fill="%s" stroke="%s" stroke-width="%.2f"%s/>' % (d, fill, stroke, sw, da)


def arrow_defs():
    out = []
    for name, col in (("ah", INK), ("ahb", BLUE), ("ahr", RED), ("ahg", GRAY)):
        out.append('<marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" '
                   'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                   '<path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker>' % (name, col))
    return "<defs>" + "".join(out) + "</defs>"


def arrow(x1, y1, x2, y2, stroke=INK, sw=1.0, mid="ah", dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f" '
            'marker-end="url(#%s)"%s/>' % (x1, y1, x2, y2, stroke, sw, mid, d))


def labelbox(x, y, w, h, label, sub=None, fill=PAPER, stroke=INK,
             size=10, subsize=8, weight="normal", tcol=INK, family=None):
    o = [box(x, y, w, h, fill, stroke)]
    if sub:
        o.append(t(x + w / 2, y + h / 2 - 1, label, size, tcol, weight=weight, family=family))
        o.append(t(x + w / 2, y + h / 2 + subsize + 1.5, sub, subsize, GRAY, family=family))
    else:
        o.append(t(x + w / 2, y + h / 2 + size * 0.35, label, size, tcol,
                   weight=weight, family=family))
    return "".join(o)


FIGURES = {}


def reg(name):
    def deco(fn):
        FIGURES[name] = fn()
        return fn
    return deco


# ------------------------------------------------------------------ 1 系統樹

@reg("ie-tree")
def _ie_tree():
    W, H = 460, 340
    o = [arrow_defs()]
    cx = 230
    o.append(box(cx - 62, 8, 124, 26, FILL, BLUE, 1.2))
    o.append(t(cx, 21, "印欧祖語 PIE", 11, BLUE, weight="bold"))
    o.append(t(cx, 31, "前4500〜前2500頃", 7, GRAY))

    branches = [
        ("アナトリア", "ヒッタイト語ほか", "†"),
        ("トカラ", "トカラ語A・B", "†"),
        ("インド・イラン", "サンスクリット／ペルシア", ""),
        ("ギリシア", "古典ギリシア語", ""),
        ("アルメニア", "", ""),
        ("アルバニア", "", ""),
        ("イタリック", "ラテン語→ロマンス諸語", ""),
        ("ケルト", "アイルランド／ウェールズ", ""),
        ("ゲルマン", "英語・独語・北欧語", "★"),
        ("バルト・スラヴ", "ロシア語／リトアニア語", ""),
    ]
    y0 = 56
    dy = 27.5
    lx = 46          # 幹の x
    o.append(line(lx, 34, lx, y0 + dy * (len(branches) - 1), RULE, 1.2))
    o.append(line(cx, 34, cx, 44, RULE, 1.2))
    o.append(line(lx, 44, cx, 44, RULE, 1.2))
    o.append(line(lx, 44, lx, 56, RULE, 1.2))

    for i, (nm, sub, mk) in enumerate(branches):
        y = y0 + dy * i
        hot = (mk == "★")
        dead = (mk == "†")
        col = RED if hot else (GRAY if dead else INK)
        o.append(line(lx, y, lx + 22, y, RULE, 1.0))
        o.append(box(lx + 22, y - 10, 104, 20, FILL if hot else PAPER, col, 1.3 if hot else .9))
        o.append(t(lx + 74, y + 3.4, nm + ("語派" if len(nm) < 8 else ""), 9,
                   col, weight="bold" if hot else "normal"))
        if sub:
            o.append(t(lx + 134, y + 3.2, sub, 8, GRAY, anchor="start"))
        if dead:
            o.append(t(lx + 16, y + 3.2, "†", 8, GRAY, anchor="end"))
    o.append(t(lx + 22, y0 + dy * len(branches) + 6,
               "† 死語　★ 英語の属する語派", 7.5, GRAY, anchor="start"))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 2 グリムの法則

@reg("grimm")
def _grimm():
    W, H = 460, 210
    o = [arrow_defs()]
    o.append(t(230, 14, "グリムの法則 ― 三つの推移が玉突きで起こる", 10, INK, weight="bold"))

    rows = [
        ("第1段階", "無声閉鎖音", "p t k kʷ", "無声摩擦音", "f θ h hʷ", RED),
        ("第2段階", "有声閉鎖音", "b d g gʷ", "無声閉鎖音", "p t k kʷ", BLUE),
        ("第3段階", "有声帯気音", "bʰ dʰ gʰ gʷʰ", "有声閉鎖音", "b d g gʷ", GREEN),
    ]
    y = 34
    for (st, n1, s1, n2, s2, col) in rows:
        o.append(t(28, y + 16, st, 8.5, col, anchor="start", weight="bold"))
        o.append(box(74, y, 116, 32, PAPER, col, 1.0))
        o.append(t(132, y + 12, n1, 7.5, GRAY))
        o.append(t(132, y + 25, s1, 11, col, family=SERIF, weight="bold"))
        o.append(arrow(196, y + 16, 244, y + 16, col, 1.2,
                       "ahr" if col == RED else ("ahb" if col == BLUE else "ah")))
        o.append(box(250, y, 116, 32, FILL, col, 1.0))
        o.append(t(308, y + 12, n2, 7.5, GRAY))
        o.append(t(308, y + 25, s2, 11, col, family=SERIF, weight="bold"))
        y += 44

    # 玉突きを示す破線
    o.append(path("M 372 50 C 412 50 412 94 372 94", GRAY, .8, dash="3 2"))
    o.append(path("M 372 94 C 412 94 412 138 372 138", GRAY, .8, dash="3 2"))
    o.append(t(424, 74, "空いた", 7, GRAY))
    o.append(t(424, 84, "位置へ", 7, GRAY))

    o.append(t(230, 186, "L pater : E father ／ L decem : E ten ／ Skt bhrātā : E brother",
               8.5, INK, family=SERIF))
    o.append(t(230, 199, "ラテン語・ギリシア語はこの推移を受けていない ＝ 対応表として使える",
               7.5, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 3 ヴェルナー

@reg("verner")
def _verner():
    W, H = 460, 200
    o = [arrow_defs()]
    o.append(t(230, 14, "ヴェルナーの法則 ― アクセントの位置が運命を分ける", 10, INK, weight="bold"))
    o.append(box(160, 26, 140, 26, FILL, INK, 1.0))
    o.append(t(230, 43, "グリムの法則で生じた f θ h s", 8.5, INK))
    o.append(arrow(230, 52, 230, 66, INK, 1.0))
    o.append(t(230, 76, "直前の音節にPIEのアクセントがあるか？", 8.5, BLUE, weight="bold"))

    o.append(arrow(200, 82, 120, 100, GREEN, 1.1))
    o.append(arrow(260, 82, 340, 100, RED, 1.1))
    o.append(t(150, 94, "ある", 8, GREEN, weight="bold"))
    o.append(t(312, 94, "ない", 8, RED, weight="bold"))

    o.append(box(30, 104, 180, 60, PAPER, GREEN, 1.1))
    o.append(t(120, 120, "そのまま　f θ h s", 9.5, GREEN, weight="bold", family=SERIF))
    o.append(t(120, 137, "*bʰréh₂tēr（第1音節）", 8.5, INK, family=SERIF))
    o.append(t(120, 152, "→ brother　th のまま", 8.5, INK))

    o.append(box(250, 104, 180, 60, FILL2, RED, 1.1))
    o.append(t(340, 120, "有声化　b̄ ð ɣ z", 9.5, RED, weight="bold", family=SERIF))
    o.append(t(340, 137, "*ph₂tḗr（第2音節）", 8.5, INK, family=SERIF))
    o.append(t(340, 152, "→ father　d になる", 8.5, INK))

    o.append(t(230, 186, "father の d と brother の th の差は、数千年前のアクセント位置の化石である。",
               8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 4 大母音推移

@reg("gvs")
def _gvs():
    W, H = 460, 300
    o = [arrow_defs()]
    o.append(t(230, 14, "大母音推移 ― 長母音がいっせいに一段上がった", 10, INK, weight="bold"))
    # 台形（母音四辺形）
    o.append(path("M 110 40 L 350 40 L 300 210 L 160 210 Z", RULE, 1.2))
    o.append(t(96, 44, "高", 8, GRAY, anchor="end"))
    o.append(t(96, 210, "低", 8, GRAY, anchor="end"))
    o.append(t(110, 32, "前舌", 8, GRAY))
    o.append(t(350, 32, "後舌", 8, GRAY))

    pts = {  # name: (x, y)
        "iː": (118, 52), "eː": (128, 92), "ɛː": (140, 134), "aː": (168, 196),
        "uː": (342, 52), "oː": (330, 92), "ɔː": (316, 140),
    }
    for k, (x, y) in pts.items():
        o.append('<circle cx="%d" cy="%d" r="3" fill="%s"/>' % (x, y, BLUE))
        o.append(t(x + (12 if x < 230 else -12), y + 3, k, 9.5, BLUE,
                   anchor="start" if x < 230 else "end", family=SERIF))
    # 上昇の矢印
    ups = [("eː", "iː"), ("ɛː", "eː"), ("aː", "ɛː"), ("oː", "uː"), ("ɔː", "oː")]
    for a, b in ups:
        x1, y1 = pts[a]; x2, y2 = pts[b]
        o.append(arrow(x1, y1 - 4, x2, y2 + 5, RED, 1.1, "ahr"))
    # 二重母音化
    o.append(arrow(118, 48, 150, 30, GREEN, 1.2, "ah"))
    o.append(t(150, 26, "aɪ", 9.5, GREEN, family=SERIF))
    o.append(arrow(342, 48, 310, 30, GREEN, 1.2, "ah"))
    o.append(t(310, 26, "aʊ", 9.5, GREEN, family=SERIF))

    ex = [("tīme /tiːmə/", "time /taɪm/"), ("see /seː/", "/siː/"),
          ("name /naːmə/", "/neɪm/"), ("moon /moːn/", "/muːn/"),
          ("hous /huːs/", "house /haʊs/")]
    y = 234
    o.append(t(60, y, "中英語", 8, GRAY, anchor="start"))
    o.append(t(250, y, "現代英語", 8, GRAY, anchor="start"))
    for a, b in ex:
        y += 12
        o.append(t(60, y, a, 8.5, INK, anchor="start", family=SERIF))
        o.append(t(230, y, "→", 8, GRAY))
        o.append(t(250, y, b, 8.5, BLUE, anchor="start", family=SERIF))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 5 三層構造

@reg("strata")
def _strata():
    W, H = 460, 235
    o = [arrow_defs()]
    o.append(t(230, 14, "英語語彙の三層 ― 同じ意味を三つの高さで言える", 10, INK, weight="bold"))
    layers = [
        ("第三層　ラテン・ギリシア語（直接借用）", "15〜17世紀・学術・抽象・長い",
         "regal / interrogate / conflagration", "#dfe7f0", BLUE),
        ("第二層　ノルマン・フランス語", "1066年以後・行政／法／料理／芸術",
         "royal / question / flame", "#eae4f0", "#5a4a7a"),
        ("第一層　古英語（ゲルマン系本来語）", "5〜11世紀・日常・具体・短い・感情的",
         "kingly / ask / fire", "#e7efe6", GREEN),
    ]
    y = 34
    for (nm, sub, ex, bg, col) in layers:
        o.append(box(40, y, 380, 54, bg, col, 1.1))
        o.append(t(52, y + 16, nm, 9, col, anchor="start", weight="bold"))
        o.append(t(52, y + 30, sub, 7.5, GRAY, anchor="start"))
        o.append(t(52, y + 45, ex, 9, INK, anchor="start", family=SERIF, style="italic"))
        y += 62
    o.append(t(230, 224, "下ほど古く、日常的で、頻度が高い。上ほど新しく、抽象的で、格式が高い。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 6 語彙構成（円）

@reg("vocab-pie")
def _vocab_pie():
    import math
    W, H = 460, 230
    o = []
    o.append(t(230, 14, "英語の語彙構成 ― 見出し語ベースと使用頻度ベース", 10, INK, weight="bold"))

    def pie(cx, cy, r, data, title, sub):
        out = [t(cx, cy - r - 12, title, 9, INK, weight="bold"),
               t(cx, cy + r + 16, sub, 7.5, GRAY)]
        ang = -90.0
        for (lab, pct, col) in data:
            sweep = 360.0 * pct / 100.0
            a1 = math.radians(ang); a2 = math.radians(ang + sweep)
            x1 = cx + r * math.cos(a1); y1 = cy + r * math.sin(a1)
            x2 = cx + r * math.cos(a2); y2 = cy + r * math.sin(a2)
            large = 1 if sweep > 180 else 0
            out.append('<path d="M %.1f %.1f L %.1f %.1f A %d %d 0 %d 1 %.1f %.1f Z" '
                       'fill="%s" stroke="%s" stroke-width="0.8"/>'
                       % (cx, cy, x1, y1, r, r, large, x2, y2, col, PAPER))
            mid = math.radians(ang + sweep / 2)
            lx = cx + (r * 0.62) * math.cos(mid); ly = cy + (r * 0.62) * math.sin(mid)
            if pct >= 8:
                out.append(t(lx, ly + 3, "%d%%" % round(pct), 8, "#fff", weight="bold"))
            ang += sweep
        return "".join(out)

    left = [("ラテン語", 29, BLUE), ("フランス語", 29, "#6a5a8a"),
            ("ゲルマン系", 26, GREEN), ("ギリシア語", 6, GOLD),
            ("その他", 10, GRAY)]
    right = [("ゲルマン系", 83, GREEN), ("ラテン・仏語系", 14, BLUE), ("その他", 3, GRAY)]
    o.append(pie(126, 118, 58, left, "辞書の見出し語", "OED の見出し語ベース"))
    o.append(pie(334, 118, 58, right, "実際の使用頻度", "頻出1000語ベース"))

    # 凡例
    y = 204
    xs = 44
    for (lab, col) in [("ゲルマン系（本来語）", GREEN), ("フランス語系", "#6a5a8a"),
                       ("ラテン語系", BLUE), ("ギリシア語系", GOLD), ("その他", GRAY)]:
        o.append('<rect x="%d" y="%d" width="9" height="9" fill="%s"/>' % (xs, y - 7, col))
        o.append(t(xs + 13, y, lab, 7.5, INK, anchor="start"))
        xs += len(lab) * 6.6 + 26
    o.append(t(230, 224, "「借り物の語彙を、本来語の骨組みに載せた言語」＝英語", 7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 7 派生ツリー *bʰer-

def _derivtree(root, gloss, groups, W=460, note=None):
    """語根 → 経路 → 英語 の三段ツリー"""
    o = [arrow_defs()]
    o.append(box(W / 2 - 78, 8, 156, 30, FILL, BLUE, 1.3))
    o.append(t(W / 2, 22, root, 12, BLUE, weight="bold", family=SERIF))
    o.append(t(W / 2, 33, gloss, 8, GRAY))
    n = len(groups)
    colw = (W - 24) / n
    y_route = 66
    y_words = 96
    for i, (route, rsub, words, col) in enumerate(groups):
        cx = 12 + colw * i + colw / 2
        o.append(arrow(W / 2, 38, cx, y_route - 4, RULE, 1.0))
        o.append(box(cx - colw / 2 + 6, y_route - 2, colw - 12, 24, PAPER, col, 1.0))
        o.append(t(cx, y_route + 8, route, 8.5, col, weight="bold"))
        o.append(t(cx, y_route + 18, rsub, 7, GRAY))
        yy = y_words + 8
        for w in words:
            o.append(t(cx, yy, w, 8.4, INK, family=SERIF))
            yy += 12.5
    H = y_words + 8 + 12.5 * max(len(g[2]) for g in groups) + (22 if note else 8)
    if note:
        o.append(t(W / 2, H - 8, note, 7.5, GRAY))
    return svg(W, int(H), "".join(o))


@reg("bher-tree")
def _bher():
    return _derivtree(
        "*bʰer-", "「運ぶ・もたらす・産む」",
        [("ゲルマン祖語", "*beranan", ["bear", "birth", "born", "burden",
                                      "bier", "barrow", "bairn"], GREEN),
         ("ラテン語 ferre", "完了分詞 lātum", ["transfer", "refer", "offer",
                                            "suffer", "differ", "fertile",
                                            "circumference"], BLUE),
         ("ギリシア語 phérein", "", ["metaphor", "periphery", "euphoria",
                                   "phosphorus", "amphora",
                                   "paraphernalia"], GOLD)],
        note="一つの語根から、英語の三つの層すべてに語が届いている。")


@reg("steh2-tree")
def _steh2():
    return _derivtree(
        "*steh₂-", "「立つ」― 印欧語根で最も多産",
        [("本来語", "PGmc *standanan", ["stand", "stead", "steady", "stall",
                                       "still", "stem", "understand",
                                       "withstand"], GREEN),
         ("ラテン語 stāre", "sistere / status", ["state", "statue", "station",
                                               "stable", "constant", "obstacle",
                                               "resist", "cost", "arrest"], BLUE),
         ("ギリシア語 hístēmi", "stásis", ["static", "system", "ecstasy",
                                         "apostasy", "prostate", "stasis",
                                         "epistemology"], GOLD)],
        note="英語だけで200語を超える。stationery（文具）も「常設の店の」から。")


# ------------------------------------------------------------------ 8 母音弱化

@reg("cap-weak")
def _cap_weak():
    W, H = 460, 215
    o = [arrow_defs()]
    o.append(t(230, 14, "母音弱化 ― 同じ語根が四つの姿になる", 10, INK, weight="bold"))
    o.append(box(20, 30, 100, 34, FILL, BLUE, 1.2))
    o.append(t(70, 45, "capere", 11, BLUE, weight="bold", family=SERIF, style="italic"))
    o.append(t(70, 57, "「取る・つかむ」", 7.5, GRAY))

    forms = [
        ("cap-", "単独形", "capture, captive, capable", 78, INK),
        ("cip-", "複合・開音節", "anticipate, participate, principal", 112, BLUE),
        ("cept-", "完了分詞", "accept, except, concept, receipt", 146, RED),
        ("-ceive", "仏語経由", "receive, deceive, perceive, conceive", 180, GREEN),
    ]
    for (f, cond, ex, y, col) in forms:
        o.append(arrow(70, 64, 70, y - 8, RULE, 1.0) if f == "cap-" else "")
        o.append(box(20, y - 12, 68, 22, PAPER, col, 1.1))
        o.append(t(54, y + 2, f, 10, col, weight="bold", family=SERIF))
        o.append(t(100, y + 2, cond, 7.5, GRAY, anchor="start"))
        o.append(t(168, y + 2, ex, 8.6, INK, anchor="start", family=SERIF))
    o.append(line(70, 64, 70, 180, RULE, 1.0))
    for (_, _, _, y, _) in forms[1:]:
        o.append(line(70, y - 1, 20, y - 1, "none", 0))
    o.append(t(230, 206,
               "接頭辞が付いて音節が変わると a → i、完了分詞では a → e に弱まる。", 7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 9 ad- の同化

@reg("ad-assim")
def _ad_assim():
    W, H = 460, 200
    o = [arrow_defs()]
    o.append(t(230, 14, "接頭辞 ad- の同化 ― 見た目が9通りに化ける", 10, INK, weight="bold"))
    o.append(box(196, 26, 68, 26, FILL, BLUE, 1.3))
    o.append(t(230, 43, "ad-", 12, BLUE, weight="bold", family=SERIF))

    items = [("ac-", "accept"), ("af-", "affect"), ("ag-", "aggregate"),
             ("al-", "allocate"), ("an-", "announce"), ("ap-", "approve"),
             ("ar-", "arrive"), ("as-", "assist"), ("at-", "attend")]
    cols, rows = 5, 2
    bw, bh = 82, 30
    gapx, gapy = 6, 10
    x0 = (W - (cols * bw + (cols - 1) * gapx)) / 2
    y0 = 76
    for i, (pre, ex) in enumerate(items):
        r, c = divmod(i, cols)
        x = x0 + c * (bw + gapx); y = y0 + r * (bh + gapy)
        o.append(box(x, y, bw, bh, PAPER, GRAY, .9))
        o.append(t(x + bw / 2, y + 13, pre, 9.5, RED, weight="bold", family=SERIF))
        o.append(t(x + bw / 2, y + 25, ex, 8.2, INK, family=SERIF))
        o.append(arrow(230, 52, x + bw / 2, y - 3, RULE, .7))
    o.append(t(230, 168, "後ろの子音に引きずられて末尾の d が変わるだけで、意味はすべて同じ「〜へ」。",
               8, INK))
    o.append(t(230, 182, "長い語に出会ったら、まず語頭2〜3字を接頭辞として切り、同化を戻す。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 10 二重語

@reg("doublet")
def _doublet():
    W, H = 460, 225
    o = [arrow_defs()]
    o.append(t(230, 14, "二重語はこうして生まれる", 10, INK, weight="bold"))
    o.append(box(160, 26, 140, 30, FILL, BLUE, 1.3))
    o.append(t(230, 41, "L capitāle", 11, BLUE, weight="bold", family=SERIF, style="italic"))
    o.append(t(230, 52, "「（頭数で数える）財産」", 7.5, GRAY))

    routes = [
        (66, "北ノルマン方言", "catel", "cattle", "牛", GREEN),
        (230, "中央フランス語", "chatel", "chattel", "動産", "#6a5a8a"),
        (394, "ラテン語直輸入", "capitāle", "capital", "資本", BLUE),
    ]
    for (cx, route, mid, eng, ja, col) in routes:
        o.append(arrow(230, 56, cx, 78, RULE, 1.0))
        o.append(t(cx, 92, route, 8, col, weight="bold"))
        o.append(t(cx, 106, mid, 9, GRAY, family=SERIF, style="italic"))
        o.append(arrow(cx, 112, cx, 130, col, 1.0,
                       "ahb" if col == BLUE else "ah"))
        o.append(box(cx - 54, 134, 108, 34, PAPER, col, 1.2))
        o.append(t(cx, 150, eng, 11.5, col, weight="bold", family=SERIF))
        o.append(t(cx, 162, ja, 8, INK))
    o.append(t(230, 192, "同じ一語が、入ってきた経路と時期の違いで三つの別語になった。", 8.2, INK))
    o.append(t(230, 206, "経路が違えば、その時代までに起きた音変化の量も違う ―― これが二重語の正体。",
               7.8, GRAY))
    o.append(t(230, 219, "同型：guard／ward・hostel／hotel／hospital・frail／fragile", 7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 11 意味変化

@reg("semchange")
def _semchange():
    W, H = 460, 250
    o = [arrow_defs()]
    o.append(t(230, 14, "意味変化の五つの型", 10, INK, weight="bold"))
    types = [
        ("拡大", "適用範囲が広がる", "bird 雛鳥 → 鳥全般", GREEN),
        ("縮小", "適用範囲が狭まる", "meat 食物 → 肉", BLUE),
        ("良化", "価値が上がる", "nice 無知な → よい", GOLD),
        ("悪化", "価値が下がる", "silly 祝福された → 愚かな", RED),
        ("漂白", "内容語が機能語へ", "will 欲する → 未来の助動詞", GRAY),
    ]
    y = 32
    for (nm, desc, ex, col) in types:
        o.append(box(30, y, 60, 34, PAPER, col, 1.2))
        o.append(t(60, y + 21, nm, 11, col, weight="bold"))
        o.append(t(102, y + 14, desc, 8.2, GRAY, anchor="start"))
        o.append(t(102, y + 28, ex, 9, INK, anchor="start", family=SERIF))
        y += 42
    o.append(t(230, 240, "音の変化には法則があるが、意味の変化にあるのは「型」であって法則ではない。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 12 年表

@reg("timeline")
def _timeline():
    W, H = 460, 210
    o = [arrow_defs()]
    o.append(t(230, 14, "英語史 ― 五つの時代と、語彙が流れ込んだ瞬間", 10, INK, weight="bold"))
    x0, x1 = 34, 428
    y = 66
    periods = [
        ("古英語", 449, 1100, "#e7efe6", GREEN),
        ("中英語", 1100, 1500, "#eae4f0", "#6a5a8a"),
        ("初期近代", 1500, 1700, "#dfe7f0", BLUE),
        ("近代", 1700, 1900, "#f2ece0", GOLD),
        ("現代", 1900, 2025, "#f0e3e2", RED),
    ]
    lo, hi = 400, 2050

    def px(yr):
        return x0 + (x1 - x0) * (yr - lo) / (hi - lo)

    for (nm, a, b, bg, col) in periods:
        o.append('<rect x="%.1f" y="%d" width="%.1f" height="26" fill="%s" stroke="%s" '
                 'stroke-width="0.9"/>' % (px(a), y, px(b) - px(a), bg, col))
        o.append(t((px(a) + px(b)) / 2, y + 17, nm, 8.5, col, weight="bold"))
    o.append(line(x0, y + 26, x1, y + 26, INK, 1.0))
    for yr in (500, 1000, 1500, 2000):
        o.append(line(px(yr), y + 26, px(yr), y + 31, INK, .8))
        o.append(t(px(yr), y + 41, str(yr), 7.5, GRAY))

    events = [
        (597, "キリスト教化", "ラテン語（宗教）", -1),
        (793, "ヴァイキング", "古ノルド語（日常語）", 1),
        (1066, "ノルマン征服", "フランス語（支配層）", -1),
        (1476, "印刷術", "綴りの固定", 1),
        (1600, "ルネサンス", "ラテン・ギリシア語（学術）", -1),
        (1850, "帝国拡大", "世界の言語", 1),
    ]
    for (yr, nm, sub, side) in events:
        x = px(yr)
        ty = y - 8 if side < 0 else y + 52
        o.append(line(x, y if side < 0 else y + 26, x, ty + (6 if side < 0 else -6), RED, 1.0))
        o.append('<circle cx="%.1f" cy="%d" r="2.6" fill="%s"/>' % (x, y if side < 0 else y + 26, RED))
        o.append(t(x, ty, nm, 8, RED, weight="bold"))
        o.append(t(x, ty + (-10 if side < 0 else 11), sub, 7, GRAY))
    o.append(t(230, 196, "英語の語彙が三層になったのは、この六つの出来事の結果である。", 7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 13 曜日

@reg("weekdays")
def _weekdays():
    W, H = 460, 195
    o = [arrow_defs()]
    o.append(t(230, 14, "曜日名 ― ローマの神をゲルマンの神に置き換えた", 10, INK, weight="bold"))
    rows = [
        ("Sunday", "diēs Sōlis", "太陽", "太陽", GOLD),
        ("Monday", "diēs Lūnae", "月", "月", GRAY),
        ("Tuesday", "diēs Martis", "Mars", "Tīw 軍神", RED),
        ("Wednesday", "diēs Mercuriī", "Mercurius", "Wōden", BLUE),
        ("Thursday", "diēs Iovis", "Iuppiter", "Þunor 雷神", RED),
        ("Friday", "diēs Veneris", "Venus", "Frīg", "#6a5a8a"),
        ("Saturday", "diēs Saturnī", "Saturnus", "（置換されず）", GRAY),
    ]
    o.append(t(64, 32, "英語", 7.5, GRAY))
    o.append(t(180, 32, "ラテン語", 7.5, GRAY))
    o.append(t(288, 32, "ローマの神", 7.5, GRAY))
    o.append(t(396, 32, "ゲルマンの神", 7.5, GRAY))
    y = 46
    for (en, la, rm, gm, col) in rows:
        o.append(line(28, y + 8, 432, y + 8, RULE, .5))
        o.append(t(64, y + 4, en, 9, INK, family=SERIF, weight="bold"))
        o.append(t(180, y + 4, la, 8.5, GRAY, family=SERIF, style="italic"))
        o.append(t(288, y + 4, rm, 8.5, INK))
        o.append(arrow(322, y + 1, 350, y + 1, col, .9))
        o.append(t(396, y + 4, gm, 8.5, col, weight="bold"))
        y += 19
    o.append(t(230, 188, "Tīw は PIE *dyeus（天空神）＝ Zeus と同語源。皮肉にも Mars に当てられた。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 14 四体液

@reg("humors")
def _humors():
    W, H = 460, 190
    o = []
    o.append(t(230, 14, "四体液説 ― 医学は消えたが、性格語彙は残った", 10, INK, weight="bold"))
    data = [
        ("血液", "sanguis", "sanguine", "陽気・楽天的", RED),
        ("粘液", "phlegma", "phlegmatic", "冷静・鈍重", BLUE),
        ("黄胆汁", "cholē", "choleric", "短気・怒りっぽい", GOLD),
        ("黒胆汁", "melan cholē", "melancholy", "憂鬱・内向的", "#4a4a58"),
    ]
    bw = 100
    x0 = (W - (4 * bw + 3 * 8)) / 2
    for i, (ja, la, en, mean, col) in enumerate(data):
        x = x0 + i * (bw + 8)
        o.append(box(x, 34, bw, 96, PAPER, col, 1.2))
        o.append('<rect x="%.1f" y="34" width="%.1f" height="7" fill="%s"/>' % (x, bw, col))
        o.append(t(x + bw / 2, 58, ja, 10.5, col, weight="bold"))
        o.append(t(x + bw / 2, 72, la, 8, GRAY, family=SERIF, style="italic"))
        o.append(line(x + 14, 80, x + bw - 14, 80, RULE, .7))
        o.append(t(x + bw / 2, 96, en, 9.5, INK, family=SERIF, weight="bold"))
        o.append(t(x + bw / 2, 112, mean, 8, INK))
    o.append(t(230, 152, "四つの体液の配合が気質を決める、という古代医学の理論。", 8.2, INK))
    o.append(t(230, 168, "理論は否定されたが、四語すべてが性格を表す英語として生き残った。",
               8, GRAY))
    o.append(t(230, 182, "同じ地層に disaster（凶星）・influence（星の霊気）・lunatic（月）がある。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 15 語の層

@reg("word-layers")
def _word_layers():
    W, H = 460, 175
    o = [arrow_defs()]
    o.append(t(230, 14, "一語に三つの言語が積み重なる ― handkerchief", 10, INK, weight="bold"))
    parts = [
        ("hand", "古英語", "本来語・ゲルマン系", GREEN, 40, 92),
        ("kerch", "古フランス語 couvre-chef", "「頭を覆うもの」", "#6a5a8a", 140, 128),
        ("ief", "", "", "#6a5a8a", 0, 0),
    ]
    x = 60
    o.append(box(60, 34, 92, 34, "#e7efe6", GREEN, 1.2))
    o.append(t(106, 55, "hand", 13, GREEN, weight="bold", family=SERIF))
    o.append(box(152, 34, 210, 34, "#eae4f0", "#6a5a8a", 1.2))
    o.append(t(257, 55, "kerchief", 13, "#6a5a8a", weight="bold", family=SERIF))

    o.append(arrow(106, 68, 106, 88, GREEN, 1.0))
    o.append(t(106, 100, "古英語 hand", 8.5, GREEN, weight="bold"))
    o.append(t(106, 112, "本来語（ゲルマン系）", 7.5, GRAY))

    o.append(arrow(257, 68, 257, 88, "#6a5a8a", 1.0))
    o.append(t(257, 100, "古フランス語 couvrechief", 8.5, "#6a5a8a", weight="bold"))
    o.append(t(257, 112, "couvrir「覆う」+ chief「頭」", 7.5, GRAY))
    o.append(arrow(257, 118, 257, 132, RULE, .9))
    o.append(t(257, 144, "chief ＜ L caput「頭」＝ラテン語層", 8.2, BLUE, weight="bold"))
    o.append(t(230, 166, "本来は頭巾。手に持つようになって hand- が付いた。三層が一語に畳まれている。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 16 ケントゥム／サテム

@reg("centum-satem")
def _centum_satem():
    W, H = 460, 215
    o = [arrow_defs()]
    o.append(t(230, 14, "ケントゥムとサテム ― 「百」の語で分かれる二つの群", 10, INK, weight="bold"))
    o.append(box(170, 28, 120, 28, FILL, BLUE, 1.2))
    o.append(t(230, 40, "PIE *ḱm̥tóm", 10.5, BLUE, weight="bold", family=SERIF))
    o.append(t(230, 51, "「百」", 7.5, GRAY))
    o.append(arrow(200, 56, 130, 76, GREEN, 1.1))
    o.append(arrow(260, 56, 330, 76, RED, 1.1, "ahr"))

    o.append(box(30, 80, 190, 104, PAPER, GREEN, 1.2))
    o.append(t(125, 96, "ケントゥム語群", 10, GREEN, weight="bold"))
    o.append(t(125, 108, "*ḱ が k のまま", 8, GRAY))
    for i, s in enumerate(["L centum", "Gk he-katón", "E hund(red)",
                           "OIr cét", "Toch A känt"]):
        o.append(t(125, 124 + i * 12, s, 8.5, INK, family=SERIF))

    o.append(box(240, 80, 190, 104, FILL2, RED, 1.2))
    o.append(t(335, 96, "サテム語群", 10, RED, weight="bold"))
    o.append(t(335, 108, "*ḱ が s / š に摩擦音化", 8, GRAY))
    for i, s in enumerate(["Av satəm", "Skt śatám", "Lith šimtas",
                           "OCS sŭto", "Arm hariwr"]):
        o.append(t(335, 124 + i * 12, s, 8.5, INK, family=SERIF))
    o.append(t(230, 200, "かつては語族最初の分岐と考えられたが、トカラ語（最東端なのにケントゥム）の",
               7.8, GRAY))
    o.append(t(230, 211, "発見により、中央域で起きた後発の地域的革新とみなされるようになった。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 17 i-ウムラウト

@reg("i-mutation")
def _imut():
    W, H = 460, 205
    o = [arrow_defs()]
    o.append(t(230, 14, "i-ウムラウト ― 消えた i が、母音だけを残していった", 10, INK, weight="bold"))
    o.append(box(80, 28, 300, 30, FILL, BLUE, 1.1))
    o.append(t(230, 47, "後ろの音節に i / j があると、前の母音が前舌化する", 9, BLUE))
    steps = [
        ("*fōt-iz", "複数形。語尾に i がある", INK),
        ("*fœt-iz", "ō が前舌化して œ に", RED),
        ("fēt", "語尾の i が脱落。母音交替だけが残る", GREEN),
    ]
    y = 74
    for (form, desc, col) in steps:
        o.append(t(120, y, form, 12, col, family=SERIF, weight="bold"))
        o.append(t(170, y, desc, 8.2, GRAY, anchor="start"))
        if y < 110:
            o.append(arrow(120, y + 5, 120, y + 20, RULE, 1.0))
        y += 28
    o.append(line(28, 150, 432, 150, RULE, .8))
    o.append(t(230, 164, "この化石が、英語の不規則複数と語形の対をすべて説明する", 8.5, INK,
               weight="bold"))
    pairs = "foot/feet　tooth/teeth　goose/geese　man/men　mouse/mice　louse/lice"
    pairs2 = "long/length　full/fill　blood/bleed　old/elder　sit/set　fall/fell"
    o.append(t(230, 180, pairs, 8.4, BLUE, family=SERIF))
    o.append(t(230, 195, pairs2, 8.4, BLUE, family=SERIF))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 18 高地ドイツ語推移

@reg("hg-shift")
def _hg_shift():
    W, H = 460, 210
    o = []
    o.append(t(230, 14, "第二次子音推移 ― 英語とドイツ語の差はここで決まった", 10, INK,
               weight="bold"))
    rows = [
        ("p → pf / ff", "apple, ship, open", "Apfel, Schiff, offen"),
        ("t → z / ss", "ten, water, eat", "zehn, Wasser, essen"),
        ("k → ch", "make, book, I", "machen, Buch, ich"),
        ("d → t", "day, door, deep", "Tag, Tür, tief"),
        ("þ → d", "thing, three, thou", "Ding, drei, du"),
    ]
    o.append(t(78, 34, "変化", 7.5, GRAY))
    o.append(t(216, 34, "英語（推移なし）", 7.5, GRAY))
    o.append(t(360, 34, "ドイツ語（推移あり）", 7.5, GRAY))
    y = 48
    for (ch, en, de) in rows:
        o.append('<rect x="28" y="%d" width="404" height="26" fill="%s" stroke="%s" '
                 'stroke-width="0.6"/>' % (y, FILL if (y // 26) % 2 else PAPER, RULE))
        o.append(t(78, y + 17, ch, 9, RED, weight="bold", family=SERIF))
        o.append(t(216, y + 17, en, 8.6, INK, family=SERIF))
        o.append(t(360, y + 17, de, 8.6, BLUE, family=SERIF))
        y += 28
    o.append(t(230, 200, "ドイツ語だけがもう一段の推移を受けた。対応は機械的で、覚えれば読める。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 19 ラテン語幹交替

@reg("latin-stems")
def _latin_stems():
    W, H = 460, 235
    o = [arrow_defs()]
    o.append(t(230, 14, "ラテン語動詞の二つの幹 ― -tion 名詞から動詞に戻る道", 10, INK,
               weight="bold"))
    o.append(box(170, 28, 120, 26, FILL, BLUE, 1.2))
    o.append(t(230, 45, "ラテン語動詞", 9.5, BLUE, weight="bold"))
    o.append(arrow(200, 54, 140, 74, GREEN, 1.1))
    o.append(arrow(260, 54, 320, 74, RED, 1.1, "ahr"))
    o.append(t(112, 88, "現在幹", 9.5, GREEN, weight="bold"))
    o.append(t(348, 88, "完了分詞幹", 9.5, RED, weight="bold"))
    rows = [
        ("mittere", "admit, permit, submit", "missum", "mission, dismiss, promise"),
        ("cēdere", "precede, concede", "cessum", "process, access, success"),
        ("vidēre", "provide, evident, prudent", "vīsum", "vision, revise, supervise"),
        ("ferre", "transfer, refer, offer", "lātum", "relate, translate, oblate"),
        ("tenēre", "contain, retain, sustain", "tentum", "content, retention"),
    ]
    y = 106
    for (a, ax, b, bx) in rows:
        o.append(line(28, y - 8, 432, y - 8, RULE, .5))
        o.append(t(30, y, a, 8.8, GREEN, anchor="start", family=SERIF, style="italic"))
        o.append(t(30, y + 11, ax, 8.2, INK, anchor="start", family=SERIF))
        o.append(t(238, y, b, 8.8, RED, anchor="start", family=SERIF, style="italic"))
        o.append(t(238, y + 11, bx, 8.2, INK, anchor="start", family=SERIF))
        y += 25
    o.append(t(230, 226, "-tion / -sion / -ture の名詞は、ほぼ例外なく完了分詞幹から作られている。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 20 借用語の出身地

@reg("world-origins")
def _world_origins():
    W, H = 460, 250
    o = [arrow_defs()]
    o.append(t(230, 14, "英語に入った語の出身地", 10, INK, weight="bold"))
    cx, cy = 230, 126
    o.append('<circle cx="%d" cy="%d" r="34" fill="%s" stroke="%s" stroke-width="1.4"/>'
             % (cx, cy, FILL, BLUE))
    o.append(t(cx, cy - 2, "英語", 12, BLUE, weight="bold"))
    o.append(t(cx, cy + 12, "ENGLISH", 6.5, GRAY, ls="1"))

    import math
    langs = [
        ("ラテン語", "circle, item, focus", 250),
        ("フランス語", "court, beef, art", 290),
        ("古ノルド語", "they, sky, egg", 330),
        ("ギリシア語", "atom, logic", 10),
        ("アラビア語", "algebra, coffee", 50),
        ("インド諸語", "jungle, shampoo", 90),
        ("日本語・中国語", "tsunami, tea", 130),
        ("アメリカ先住民語", "tomato, canoe", 170),
        ("オランダ語", "deck, boss", 210),
    ]
    R = 96
    for (nm, ex, deg) in langs:
        a = math.radians(deg)
        x = cx + R * math.cos(a); y = cy + R * math.sin(a) * 0.82
        o.append(arrow(x - 22 * math.cos(a), y - 22 * math.sin(a) * 0.82,
                       cx + 38 * math.cos(a), cy + 38 * math.sin(a) * 0.82, RULE, .9))
        anchor = "middle"
        o.append(t(x, y - 3, nm, 8.4, INK, anchor=anchor, weight="bold"))
        o.append(t(x, y + 8, ex, 7.4, GRAY, anchor=anchor, family=SERIF))
    o.append(t(230, 238, "借用の博物館 ―― 語彙の約6割は外来。だが頻出100語はほぼすべて本来語。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 21 頻度と語源

@reg("freq-origin")
def _freq_origin():
    W, H = 460, 210
    o = []
    o.append(t(230, 14, "頻度順位が下がるほど、外来語の比率が上がる", 10, INK, weight="bold"))
    x0, y0, bw, gap = 60, 40, 58, 18
    bands = [("上位\n100語", 97, 3), ("上位\n1000語", 83, 17),
             ("上位\n5000語", 60, 40), ("上位\n1万語", 45, 55),
             ("辞書\n全体", 26, 74)]
    maxh = 120
    for i, (lab, ger, lat) in enumerate(bands):
        x = x0 + i * (bw + gap)
        hg = maxh * ger / 100.0
        hl = maxh * lat / 100.0
        o.append('<rect x="%.1f" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                 % (x, y0 + maxh - hg, bw, hg, "#8fbf9f"))
        o.append('<rect x="%.1f" y="%.1f" width="%d" height="%.1f" fill="%s"/>'
                 % (x, y0, bw, hl, "#93aac9"))
        o.append(box(x, y0, bw, maxh, "none", RULE, .8))
        o.append(t(x + bw / 2, y0 + maxh - hg + 13, "%d%%" % ger, 8.5, "#12482a",
                   weight="bold"))
        if hl > 16:
            o.append(t(x + bw / 2, y0 + 13, "%d%%" % lat, 8.5, "#183a5c", weight="bold"))
        for j, ln in enumerate(lab.split("\n")):
            o.append(t(x + bw / 2, y0 + maxh + 14 + j * 11, ln, 7.8, INK))
    o.append('<rect x="150" y="188" width="9" height="9" fill="#8fbf9f"/>')
    o.append(t(164, 196, "ゲルマン系（本来語）", 7.8, INK, anchor="start"))
    o.append('<rect x="272" y="188" width="9" height="9" fill="#93aac9"/>')
    o.append(t(286, 196, "ラテン・仏語系ほか", 7.8, INK, anchor="start"))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 22 調音位置

@reg("place-of-articulation")
def _place():
    W, H = 460, 215
    o = []
    o.append(t(230, 14, "調音位置 ― 音の変化はこの並びの上を移動する", 10, INK, weight="bold"))
    places = [("唇音", "p b f v m", 60), ("歯音", "t d θ ð s z n", 140),
              ("硬口蓋", "ʃ ʒ tʃ dʒ j", 226), ("軟口蓋", "k g ŋ", 312),
              ("声門", "h ʔ", 390)]
    # 口腔の断面（簡略）
    o.append(path("M 40 62 Q 230 34 420 62 L 420 92 Q 230 118 40 92 Z", RULE, 1.0, FILL))
    o.append(t(38, 58, "前", 7.5, GRAY, anchor="end"))
    o.append(t(424, 58, "後", 7.5, GRAY, anchor="start"))
    for (nm, syms, x) in places:
        o.append(line(x, 62, x, 132, RULE, .8, dash=None))
        o.append('<circle cx="%d" cy="77" r="3.2" fill="%s"/>' % (x, BLUE))
        o.append(t(x, 146, nm, 8.6, BLUE, weight="bold"))
        o.append(t(x, 160, syms, 8.6, INK, family=SERIF))
    o.append(line(28, 176, 432, 176, RULE, .8))
    o.append(t(230, 190, "グリムの法則は「閉鎖 → 摩擦」、大母音推移は「低 → 高」。",
               8.2, INK))
    o.append(t(230, 204, "音変化は、この調音の地図の上をすべるように起こる。", 7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 23 語根の費用対効果

@reg("root-roi")
def _root_roi():
    W, H = 460, 225
    o = []
    o.append(t(230, 14, "覚える価値の高い語根 ― 1語根あたりの英単語数", 10, INK, weight="bold"))
    data = [("*steh₂- 立つ", 200), ("*deh₃- 与える", 95), ("*bʰer- 運ぶ", 90),
            ("*kap- 取る", 85), ("*dʰeh₁- 置く", 80), ("*speḱ- 見る", 75),
            ("*ten- 張る", 70), ("*ǵenh₁- 生む", 68), ("*leg- 集める", 60),
            ("*wert- 回す", 55)]
    x0, y0 = 128, 34
    maxv = 200.0
    barw = 268
    for i, (nm, v) in enumerate(data):
        y = y0 + i * 18
        w = barw * v / maxv
        o.append(t(122, y + 10, nm, 8.4, INK, anchor="end", family=SERIF))
        o.append('<rect x="%d" y="%d" width="%.1f" height="12" fill="%s"/>'
                 % (x0, y + 1, w, BLUE if i < 3 else "#93aac9"))
        o.append(t(x0 + w + 6, y + 10, "%d語" % v, 7.8, GRAY, anchor="start"))
    o.append(t(230, 216, "上位10語根を押さえるだけで、800語近くの英単語が構造的に見えてくる。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 24 語彙カバー率

@reg("coverage")
def _coverage():
    W, H = 460, 238
    o = []
    o.append(t(230, 14, "何語覚えれば何割読めるか", 10, INK, weight="bold"))
    pts = [(0, 0), (1000, 72), (2000, 81), (3000, 85), (5000, 89),
           (8000, 93), (10000, 95), (15000, 97), (20000, 98)]
    x0, y0, w, h = 62, 36, 344, 132
    o.append(box(x0, y0, w, h, PAPER, RULE, .8))
    for pct in (25, 50, 75, 100):
        y = y0 + h - h * pct / 100.0
        o.append(line(x0, y, x0 + w, y, RULE, .5))
        o.append(t(x0 - 8, y + 3, "%d%%" % pct, 7.2, GRAY, anchor="end"))
    d = []
    for (v, p) in pts:
        x = x0 + w * (v / 20000.0)
        y = y0 + h - h * p / 100.0
        d.append("%s %.1f %.1f" % ("M" if not d else "L", x, y))
    o.append(path(" ".join(d), BLUE, 1.8))
    for (v, p) in pts:
        if v in (1000, 2000, 3000, 5000, 10000):
            x = x0 + w * (v / 20000.0)
            y = y0 + h - h * p / 100.0
            o.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (x, y, RED))
            o.append(t(x, y - 8, "%d%%" % p, 7.6, RED, weight="bold"))
            o.append(t(x, y0 + h + 12, "%s" % ("%dk" % (v // 1000)), 7.4, GRAY))
    o.append(t(230, y0 + h + 26, "覚えた語数（見出し語）", 7.8, GRAY))
    o.append(t(230, 212, "2000語で8割、3000語で85%。だが残り15%を埋めるには1万語以上が要る。",
               8.2, INK))
    o.append(t(230, 228, "TOEIC 600点の語彙目安は約3000語 ―― この曲線の「膝」にあたる。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


# ------------------------------------------------------------------ 25 語源の確からしさ

@reg("confidence")
def _confidence():
    W, H = 460, 200
    o = [arrow_defs()]
    o.append(t(230, 14, "語源説の確からしさ ― 四つの階層", 10, INK, weight="bold"))
    tiers = [
        ("確実", "年代の確かな用例がある", "father ＜ OE fæder", GREEN),
        ("通説", "標準的な辞典が一致して支持", "muscle ＜「小さなねずみ」", BLUE),
        ("一説", "有力だが異論がある", "book ＜「ブナ」", GOLD),
        ("不確実", "of unknown origin", "dog / big / bad / fun", GRAY),
    ]
    y = 34
    wmax = 340
    for i, (nm, crit, ex, col) in enumerate(tiers):
        w = wmax - i * 52
        x = (W - w) / 2
        o.append(box(x, y, w, 32, PAPER, col, 1.3))
        o.append('<rect x="%.1f" y="%.1f" width="6" height="32" fill="%s"/>' % (x, y, col))
        o.append(t(x + 40, y + 20, nm, 11, col, weight="bold"))
        o.append(t(x + 84, y + 13, crit, 7.8, GRAY, anchor="start"))
        o.append(t(x + 84, y + 26, ex, 8.4, INK, anchor="start", family=SERIF))
        y += 38
    o.append(t(230, 190, "本書は「〜とされる」「〜説がある」の留保を省略しない。曖昧さではなく誠実さである。",
               7.8, GRAY))
    return svg(W, H, "".join(o))


if __name__ == "__main__":
    import sys
    print("登録された図版: %d 点" % len(FIGURES))
    for k in sorted(FIGURES):
        print("  %-24s %6d bytes" % (k, len(FIGURES[k])))
