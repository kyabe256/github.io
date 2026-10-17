"""問題集 第4章 地層・岩石と地質構造。CH に問題、verify() で数値と図の幾何を Python で検算する。問題はすべて書き下ろし。"""
import math
import re


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) <= 0.5 * 10 ** e * (1 + 1e-9), (x, shown, n)


# ---- 図（座標は計算で出す） ----
def _ln(x1, y1, x2, y2, c="#333", w=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def _ar(x1, y1, x2, y2, c="#333", w=1.2, hs=6):
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - hs * math.cos(a - 0.4), y2 - hs * math.sin(a - 0.4))
    p2 = (x2 - hs * math.cos(a + 0.4), y2 - hs * math.sin(a + 0.4))
    return (_ln(x1, y1, x2, y2, c, w) +
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>')


def _tx(x, y, s, size=11, anchor="start", c="#222", it=False):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _pts(ps):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in ps)


ROCK = {"gr": "礫岩", "ss": "砂岩", "ms": "泥岩", "tf": "凝灰岩", "ls": "石灰岩", "ig": "火成岩"}


def _defs(f):
    """岩石の模様（f は図ごとの接頭辞。id の重複を避ける）"""
    return ("<defs>"
            f'<pattern id="{f}gr" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#f3ead8"/>'
            '<circle cx="3" cy="3" r="2.2" fill="none" stroke="#555" stroke-width="0.8"/><circle cx="8" cy="8" r="1.6" fill="none" stroke="#555" stroke-width="0.8"/></pattern>'
            f'<pattern id="{f}ss" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#f6edc9"/>'
            '<circle cx="1.5" cy="1.5" r="0.75" fill="#666"/><circle cx="4.5" cy="4.5" r="0.75" fill="#666"/></pattern>'
            f'<pattern id="{f}ms" width="12" height="6" patternUnits="userSpaceOnUse"><rect width="12" height="6" fill="#dcdcdc"/>'
            '<line x1="1" y1="2" x2="6" y2="2" stroke="#666" stroke-width="0.8"/><line x1="7" y1="5" x2="11" y2="5" stroke="#666" stroke-width="0.8"/></pattern>'
            f'<pattern id="{f}tf" width="10" height="8" patternUnits="userSpaceOnUse"><rect width="10" height="8" fill="#f7e1ec"/>'
            '<path d="M2,2 L4,6 L6,2" fill="none" stroke="#a0457a" stroke-width="0.8"/></pattern>'
            f'<pattern id="{f}ls" width="16" height="8" patternUnits="userSpaceOnUse"><rect width="16" height="8" fill="#e4edf3"/>'
            '<path d="M0,0.5 H16 M0,4.5 H16 M5,0.5 V4.5 M13,4.5 V8" fill="none" stroke="#6a7f8f" stroke-width="0.8"/></pattern>'
            f'<pattern id="{f}ig" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#f2c9c9"/>'
            '<path d="M3,1 V5 M1,3 H5 M8,6 V10 M6,8 H10" fill="none" stroke="#a33" stroke-width="0.8"/></pattern>'
            "</defs>")


# 4-5 柱状図：上から順に（岩石, 厚さ [m], ラベル）
COLS = {"A": [("ss", 4, ""), ("tf", 1, "Y"), ("ms", 5, ""), ("tf", 1, "X"), ("ss", 3, "")],
        "B": [("gr", 3, ""), ("ss", 5, ""), ("tf", 1, "Y"), ("ms", 3, "")],
        "C": [("ms", 2, ""), ("tf", 1, "X"), ("ss", 4, ""), ("gr", 2, ""), ("ls", 4, "")]}


def _fig_cols():
    f, s, y0, w = "c4", 9, 26, 34
    p = [_defs(f)]
    for i, (name, lay) in enumerate(COLS.items()):
        x = 30 + i * 100
        y = y0
        p.append(_tx(x + w / 2, y0 - 8, f"地点 {name}", 11, "middle"))
        for kind, th, lab in lay:
            p.append(f'<rect x="{x}" y="{y:.1f}" width="{w}" height="{th * s:.1f}" fill="url(#{f}{kind})" stroke="#333" stroke-width="0.8"/>')
            if lab:
                p.append(_tx(x + w + 5, y + th * s / 2 + 4, lab, 11, c="#a0457a", it=True))
            y += th * s
        if name == "C":   # 礫岩と石灰岩の境界（不整合）を波線で
            yb = y0 + 9 * s
            wave = " ".join(f"{x + k * w / 8:.1f},{yb + (2 if k % 2 else -2):.1f}" for k in range(9))
            p.append(f'<polyline points="{wave}" fill="none" stroke="#c0392b" stroke-width="1.6"/>')
            p.append(_tx(x + w + 5, yb + 4, "Q", 11, c="#c0392b", it=True))
            p.append(_tx(x + w + 5, y0 + 11 * s + 4, "（フズリナ）", 9, c="#555"))
    # 縮尺と凡例
    p.append(_ln(8, y0, 8, y0 + 5 * s, "#333", 1.2))
    p += [_ln(5, y0, 11, y0, "#333", 1), _ln(5, y0 + 5 * s, 11, y0 + 5 * s, "#333", 1), _tx(4, y0 + 5 * s + 13, "5 m", 9)]
    lx, ly = 318, 30
    for k, kind in enumerate(["gr", "ss", "ms", "tf", "ls"]):
        p.append(f'<rect x="{lx}" y="{ly + 19 * k}" width="18" height="12" fill="url(#{f}{kind})" stroke="#333" stroke-width="0.6"/>')
        p.append(_tx(lx + 23, ly + 19 * k + 10, ROCK[kind], 10))
    return _svg(380, y0 + 14 * s + 18, p)


# 4-6 ボーリング：A を原点、東を x、北を y [m]。地表の標高 [m]、凝灰岩上面までの深さ [m]
BOR = {"A": (0, 0, 120, 20), "B": (0, 100, 140, 40), "C": (100, 0, 110, 60)}
PD = (200, 0, 100)


def _fig_bor():
    ox, oy, s = 40, 150, 0.9
    X = lambda x: ox + s * x
    Y = lambda y: oy - s * y
    p = [f'<rect x="{X(-20):.1f}" y="{Y(140):.1f}" width="{s * 250:.1f}" height="{s * 160:.1f}" fill="#fbf8f3" stroke="#999" stroke-width="0.8"/>']
    for g in range(0, 221, 50):
        p.append(_ln(X(g), Y(-20), X(g), Y(140), "#e2e2e2", 0.8))
    for g in range(0, 131, 50):
        p.append(_ln(X(-20), Y(g), X(230), Y(g), "#e2e2e2", 0.8))
    for name, (x, y, h, d) in list(BOR.items()) + [("D", (PD[0], PD[1], PD[2], 0))]:
        p.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3.5" fill="#7a4a1f"/>')
        p.append(_tx(X(x) + 6, Y(y) - 6, name, 11))
    p += [_ar(X(205), Y(80), X(205), Y(125)), _tx(X(205), Y(128) - 3, "N", 10, "middle"),
          _ln(X(100), Y(-12), X(200), Y(-12), "#333", 1.2), _tx(X(150), Y(-12) + 12, "100 m", 9, "middle")]
    return _svg(270, 172, p)


# 4-7 断面図（px 座標）：不整合面 U、断層 F、岩脈 G
U_Y, DE_Y, TOP_Y, BOT_Y, W = 72, 48, 20, 170, 300
F_TOP, F_BOT = (170, U_Y), (230, BOT_Y)
SLOPE, OFF = 0.25, 28           # 地層境界の傾き、断層による右側のずれ（下がり）


def _lab(x):
    return 172 - SLOPE * x      # a/b 境界（左側）


def _lbc(x):
    return 130 - SLOPE * x      # b/c 境界（左側）


def _fig_sec():
    f = "s4"
    p = [_defs(f), "<defs>",
         f'<clipPath id="{f}L"><polygon points="{_pts([(0, U_Y), F_TOP, F_BOT, (0, BOT_Y)])}"/></clipPath>',
         f'<clipPath id="{f}R"><polygon points="{_pts([F_TOP, (W, U_Y), (W, BOT_Y), F_BOT])}"/></clipPath>', "</defs>"]
    for side, off in (("L", 0), ("R", OFF)):
        lab = lambda x: _lab(x) + off
        lbc = lambda x: _lbc(x) + off
        a = [(-10, lab(-10)), (W + 10, lab(W + 10)), (W + 10, 400), (-10, 400)]
        b = [(-10, lbc(-10)), (W + 10, lbc(W + 10)), (W + 10, lab(W + 10)), (-10, lab(-10))]
        c = [(-10, -50), (W + 10, -50), (W + 10, lbc(W + 10)), (-10, lbc(-10))]
        p.append(f'<g clip-path="url(#{f}{side})">'
                 f'<polygon points="{_pts(a)}" fill="url(#{f}ss)"/><polygon points="{_pts(b)}" fill="url(#{f}ms)"/>'
                 f'<polygon points="{_pts(c)}" fill="url(#{f}ls)"/>'
                 f'<polyline points="{_pts([(-10, lab(-10)), (W + 10, lab(W + 10))])}" fill="none" stroke="#333" stroke-width="0.9"/>'
                 f'<polyline points="{_pts([(-10, lbc(-10)), (W + 10, lbc(W + 10))])}" fill="none" stroke="#333" stroke-width="0.9"/></g>')
    p += [f'<rect x="0" y="{DE_Y}" width="{W}" height="{U_Y - DE_Y}" fill="url(#{f}gr)"/>',
          f'<rect x="0" y="{TOP_Y}" width="{W}" height="{DE_Y - TOP_Y}" fill="url(#{f}ss)"/>',
          f'<rect x="60" y="{DE_Y}" width="12" height="{BOT_Y - DE_Y}" fill="url(#{f}ig)" stroke="#a33" stroke-width="0.8"/>',
          _ln(0, DE_Y, W, DE_Y, "#333", 0.9), _ln(0, U_Y, W, U_Y, "#c0392b", 2),
          _ln(F_TOP[0], F_TOP[1], F_BOT[0], F_BOT[1], "#1d4e89", 2.2),
          f'<rect x="0" y="{TOP_Y}" width="{W}" height="{BOT_Y - TOP_Y}" fill="none" stroke="#333" stroke-width="1.2"/>']
    labs = [(25, 100, "c"), (95, 130, "b"), (160, 158, "a"), (250, 88, "c"), (275, 115, "b"), (285, 155, "a"),
            (150, 64, "d"), (150, 38, "e")]
    for x, y, s in labs:
        p.append(f'<rect x="{x - 7}" y="{y - 11}" width="14" height="14" rx="2" fill="#fff" opacity="0.85"/>')
        p.append(_tx(x, y, s, 12, "middle", it=True))
    p += [_tx(W + 6, U_Y + 4, "U", 12, c="#c0392b", it=True), _tx(205, 128, "F", 12, c="#1d4e89", it=True),
          _tx(66, BOT_Y + 14, "G", 12, "middle", "#a33", True)]
    lx, ly = W + 26, 30
    for k, kind in enumerate(["gr", "ss", "ms", "ls", "ig"]):
        p.append(f'<rect x="{lx}" y="{ly + 20 * k}" width="18" height="12" fill="url(#{f}{kind})" stroke="#333" stroke-width="0.6"/>')
        p.append(_tx(lx + 23, ly + 20 * k + 10, ROCK[kind], 10))
    return _svg(W + 80, BOT_Y + 22, p)


# 4-10 地質図：x 東、y 北 [m]。地形 z = 40 + 0.4|x-100| + 0.2y（南へ下る谷）、境界面 z = 220 - y（北へ傾く）
def ZT(x, y):
    return 40 + 0.4 * abs(x - 100) + 0.2 * y


def ZP(x, y):
    return 220 - y


def _trace_y(x):          # 境界線（地形と境界面の交線）の y
    return (220 - 40 - 0.4 * abs(x - 100)) / (0.2 + 1.0)


MP, MQ = (100, 190, 78), (160, 30)


def _fig_map():
    f, ox, oy, s = "m4", 34, 16, 1.2
    X = lambda x: ox + s * x
    Y = lambda y: oy + s * (200 - y)
    tr = [(X(x), Y(_trace_y(x))) for x in range(0, 201, 5)]
    north = tr + [(X(200), Y(200)), (X(0), Y(200))]
    south = tr + [(X(200), Y(0)), (X(0), Y(0))]
    p = [f'<defs><clipPath id="{f}c"><rect x="{X(0)}" y="{Y(200)}" width="{200 * s}" height="{200 * s}"/></clipPath></defs>',
         f'<polygon points="{_pts(north)}" fill="#e3e3e3"/>', f'<polygon points="{_pts(south)}" fill="#f6edc9"/>']
    for g in range(20, 200, 20):
        p += [_ln(X(g), Y(0), X(g), Y(200), "#fff", 0.8), _ln(X(0), Y(g), X(200), Y(g), "#fff", 0.8)]
    cl = [f'<g clip-path="url(#{f}c)">']
    for Z in range(50, 111, 10):
        def dx(y):
            return (Z - 40 - 0.2 * y) / 0.4
        ys = [y for y in range(0, 201)]
        left = [(X(100 - dx(y)), Y(y)) for y in ys if dx(y) >= 0]
        right = [(X(100 + dx(y)), Y(y)) for y in ys if dx(y) >= 0]
        cl.append(f'<polyline points="{_pts(left + right[::-1])}" fill="none" stroke="#7a4a1f" stroke-width="1"/>')
    cl.append("</g>")
    p += cl
    p.append(f'<polyline points="{_pts(tr)}" fill="none" stroke="#c0392b" stroke-width="2.2"/>')
    for Z in range(50, 111, 10):
        xb = 100 - (Z - 40) / 0.4
        if xb >= 0 and Z != 80:
            p.append(_tx(X(xb), Y(0) + 12, str(Z), 9, "middle", "#7a4a1f"))
        else:
            yl = (Z - 80) / 0.2
            p.append(_tx(X(0) - 3, Y(yl) + 3, str(Z), 9, "end", "#7a4a1f"))
    p += [f'<rect x="{X(0)}" y="{Y(200)}" width="{200 * s}" height="{200 * s}" fill="none" stroke="#333" stroke-width="1.2"/>',
          f'<circle cx="{X(MP[0]):.1f}" cy="{Y(MP[1]):.1f}" r="3.5" fill="#1d4e89"/>', _tx(X(MP[0]) + 6, Y(MP[1]) + 4, "P", 11, c="#1d4e89"),
          f'<circle cx="{X(MQ[0]):.1f}" cy="{Y(MQ[1]):.1f}" r="3.5" fill="#1d4e89"/>', _tx(X(MQ[0]) + 6, Y(MQ[1]) + 4, "Q", 11, c="#1d4e89"),
          _tx(X(40), Y(175), "泥岩", 11, "middle"), _tx(X(40), Y(60), "砂岩", 11, "middle"),
          _ar(X(200) + 18, Y(150), X(200) + 18, Y(190)), _tx(X(200) + 18, Y(194) - 2, "N", 10, "middle"),
          _ln(X(140), Y(0) + 22, X(200), Y(0) + 22, "#333", 1.2), _ln(X(140), Y(0) + 19, X(140), Y(0) + 25, "#333", 1),
          _ln(X(200), Y(0) + 19, X(200), Y(0) + 25, "#333", 1), _tx(X(170), Y(0) + 34, "50 m", 9, "middle")]
    return _svg(300, 300, p)


def B(s):
    return f'<div class="bun">{s}</div>'


TAB_BOR = ('<table><tr><th>地点</th><th>位置</th><th>地表の標高</th><th>凝灰岩層の上面までの深さ</th></tr>'
           + "".join(f'<tr><td>{n}</td><td>{pos}</td><td>{h} m</td><td>{d} m</td></tr>'
                     for n, pos, (x, y, h, d) in (("A", "基準", BOR["A"]), ("B", "A の 100 m 北", BOR["B"]), ("C", "A の 100 m 東", BOR["C"])))
           + '</table>')
TANS = [20, 25, 27, 30]
TAB_TAN = ('<table><tr><th>$\\theta$</th>' + "".join(f"<td>${d}^\\circ$</td>" for d in TANS) + '</tr>'
           '<tr><th>$\\tan\\theta$</th>' + "".join(f"<td>{math.tan(math.radians(d)):.2f}</td>" for d in TANS) + '</tr></table>')

CH = {4: {
"goal": "風化から堆積までの流れと堆積岩・変成岩の種類を整理し、柱状図・断面図・地質図から地層の新旧、地質構造（走向・傾斜、断層、不整合）と地史を読み取れるようにする。",
"items": [
 {"lv": "A", "tag": "空欄補充",
  "q": "次の文の空欄に適する語を入れよ。" + B("地表の岩石は、気温の変化や水の凍結によって細かく割れる（ア）風化や、雨水や二酸化炭素のはたらきで成分がとけ出す（イ）風化を受ける。石灰岩地域では（イ）風化によって、鍾乳洞などの（ウ）地形ができる。河川は上流で谷底を深く削って（エ）谷をつくり、山地から平野に出る所では（オ）を、河口付近では（カ）をつくる。"),
  "a": "ア 物理的（機械的）　イ 化学的　ウ カルスト　エ V字　オ 扇状地　カ 三角州",
  "s": r"物理的風化は岩石を細かくするだけで成分は変わらない。寒冷地や昼夜の温度差の大きい乾燥地で進みやすい。化学的風化は高温多湿な地域で進みやすく、石灰岩は二酸化炭素を含む雨水にとけてカルスト地形をつくる。河川の流速が急に小さくなる所（山地の出口・河口）では、運ばれてきた粒子が堆積する。<br><b>ポイント</b>：「侵食→運搬→堆積」は流速で決まる。流速が小さくなる場所＝堆積の場所。"},
 {"lv": "A", "tag": "知識",
  "q": "次の (1)〜(6) の堆積岩の名称を答えよ。<br>(1) 直径 2 mm 以上の粒子が固まったもの<br>(2) 直径 $\\frac1{16}$〜2 mm の粒子が固まったもの<br>(3) 直径 $\\frac1{16}$ mm 以下の粒子が固まったもの<br>(4) 火山灰が堆積して固まったもの<br>(5) サンゴや有孔虫などの殻が集まってできた、うすい塩酸をかけると泡を出すもの<br>(6) 放散虫などの殻が集まってできた、非常にかたく、主成分が $\\mathrm{SiO_2}$ のもの",
  "a": "(1) 礫岩　(2) 砂岩　(3) 泥岩　(4) 凝灰岩　(5) 石灰岩　(6) チャート",
  "s": r"(1)〜(3) は砕屑岩で、粒子の大きさで分ける。(4) は火山砕屑岩。(5)(6) は生物の遺がいが集まってできた生物岩。石灰岩の主成分は炭酸カルシウム $\mathrm{CaCO_3}$ で、塩酸と反応して二酸化炭素を出す。チャートは鋼鉄のくぎでも傷がつかないほどかたい。<br><b>ポイント</b>：堆積岩の分類は「何が（砕屑物・火山砕屑物・生物の殻・水にとけていた物質）」集まったかで分ける。"},
 {"lv": "A", "tag": "空欄補充",
  "q": "次の文の空欄に適する語を入れよ。" + B("地層は、逆転していなければ下にあるものほど古い。これを（ア）の法則という。地層が連続して堆積している重なり方を（イ）という。これに対し、堆積が中断して侵食を受けたのち、再び堆積が始まった重なり方を（ウ）といい、その境界面の上には下の地層の岩石の破片を含む（エ）が見られることが多い。離れた地域の地層を比べるとき、火山灰層のように広い範囲に短い期間で堆積した、目印となる地層を（オ）という。"),
  "a": "ア 地層累重　イ 整合　ウ 不整合　エ 基底礫岩　オ 鍵層",
  "s": "不整合には、上下の地層が平行な平行不整合と、下の地層が傾いている（褶曲している）傾斜不整合がある。不整合面は、その場所がいったん陸上に出て侵食されたことを示す。<br><b>ポイント</b>：不整合＝「堆積→隆起→侵食→沈降→堆積」の記録。基底礫岩は不整合を見分ける目印。"},
 {"lv": "A", "tag": "知識",
  "q": "(1) マグマの熱によって周囲の岩石が変化する作用を何というか。また、この作用で泥岩や砂岩からできる、かたく緻密な岩石と、石灰岩からできる岩石の名称をそれぞれ答えよ。<br>(2) プレートの沈み込み帯などで、広い範囲にわたって高い温度や圧力を受けてできた変成岩のうち、うすくはがれやすい性質（片理）をもつものと、白と黒の縞模様をもつ粗粒のものの名称をそれぞれ答えよ。",
  "a": "(1) 接触変成作用。ホルンフェルス、結晶質石灰岩（大理石）　(2) 結晶片岩（片岩）、片麻岩",
  "s": "接触変成作用はマグマに接した数十 m〜数 km の範囲で起こり、主に熱によって鉱物が再結晶する。広域変成作用は数十〜数百 km にわたる帯状の地域（変成帯）で起こる。結晶片岩は、圧力の方向にそろって並んだ鉱物によって片理ができる。片麻岩はより高温でできる。<br><b>ポイント</b>：「接触変成岩＝熱、広域変成岩＝熱と圧力」。変成岩は、もとの岩石が固体のまま鉱物の組み合わせや組織が変わったもので、融けてはいない。"},
 {"lv": "B", "tag": "柱状図の読み取り",
  "q": "図は、近くにある3地点 A〜C の地層の柱状図である。X, Y はそれぞれ同じ時期に堆積した凝灰岩層である。地点 C の礫岩には石灰岩の礫が含まれ、最下部の石灰岩からはフズリナの化石が見つかった。地層の逆転はなく、同じ時期に堆積した地層の厚さは3地点で等しいものとする。" + _fig_cols() +
       "(1) 3地点の地層のうち、最も新しい地層と最も古い地層を、地点名と岩石名で答えよ。<br>(2) 地点 C の境界 Q を何というか。また、境界 Q ができるまでに地点 C で起こったことを、順に答えよ。<br>(3) 地点 C の礫岩 → 砂岩 → 泥岩 の重なりから、この間に地点 C の水深はどのように変化したと考えられるか。<br>(4) 凝灰岩層が鍵層として役立つ理由を答えよ。<br>(5) 地点 C の石灰岩ができた地質時代を答えよ。",
  "a": "(1) 最も新しい：地点 B の最上部の礫岩、最も古い：地点 C の石灰岩　(2) 不整合。石灰岩が海底で堆積 → 隆起して陸上で侵食 → 沈降 → 礫岩が堆積　(3) しだいに深くなった（海岸から遠くなった）。　(4) 火山灰は短い期間に広い範囲に降り積もるので、離れた地点でも同じ時期の地層とみなせるから。　(5) 古生代（後期）",
  "s": "(1) X, Y で3地点をつなぐと、新しい順に B の礫岩・砂岩 → Y → 泥岩 → X → 砂岩 → C の礫岩 → C の石灰岩 となる。Y の上の砂岩は、A では地表まで 4 m しかないが、B では 5 m あり、その上に礫岩が重なる。厚さが等しいので、B の礫岩は A の最上部より新しい。<br>(2) 礫岩に下の石灰岩の礫が含まれる（基底礫岩）ことから、石灰岩が陸上で侵食されたあと、その上に礫岩が堆積したとわかる。<br>(3) 粒子が上に向かって細かくなっている。細かい粒子ほど海岸から離れた深い所まで運ばれて堆積するので、水深が深くなった（または海岸線が遠ざかった）と考えられる。逆に B の泥岩 → 砂岩 → 礫岩 は浅くなったことを示す。<br>(4) 噴火は地質学的には一瞬のできごとで、火山灰は風で広く運ばれる。鉱物の組み合わせなどで個々の火山灰層を見分けられる。<br>(5) フズリナは古生代の石炭紀〜ペルム紀の示準化石。<br><b>ポイント</b>：柱状図の対比は「鍵層で横につなぐ → 新旧を並べる」。粒子の大きさの変化から水深（海岸からの距離）の変化を読む。"},
 {"lv": "B", "tag": "計算",
  "q": "ある地域で、同じ凝灰岩層の上面の深さをボーリングで調べた（表）。凝灰岩層は平面で、地層の逆転はないものとする。" + TAB_BOR + _fig_bor() +
       "(1) 地点 A, B, C の凝灰岩層の上面の標高をそれぞれ求めよ。<br>(2) 凝灰岩層の走向と、傾斜している向きを答えよ。<br>(3) 傾斜の角を $\\theta$ として $\\tan\\theta$ を求め、下の表から最も近い角を選べ。" + TAB_TAN +
       "(4) 地点 A の 200 m 東の地点 D（地表の標高 100 m）でボーリングを行うと、何 m の深さで凝灰岩層の上面に達するか。",
  "a": r"(1) A 100 m、B 100 m、C 50 m　(2) 走向は南北（N–S）、東へ傾斜　(3) $\tan\theta=0.50$、$27^\circ$　(4) 100 m",
  "s": r"(1) 標高＝地表の標高－深さ。A：$120-20=100\,\mathrm{m}$、B：$140-40=100\,\mathrm{m}$、C：$110-60=50\,\mathrm{m}$。<br>(2) A と B は同じ標高なので、AB を結ぶ南北の線が走向（地層面と水平面の交線の向き）。A の東の C で低くなっているので、東へ傾斜している。<br>(3) 走向に直角な東西方向に $100\,\mathrm{m}$ 進むと $50\,\mathrm{m}$ 下がるので $\tan\theta=\dfrac{50}{100}=0.50$。表の $\tan27^\circ=0.51$ が最も近い。<br>(4) D は A から東へ $200\,\mathrm{m}$ なので、上面の標高は $100-0.50\times200=0\,\mathrm{m}$。深さは $100-0=100\,\mathrm{m}$。<br><b>ポイント</b>：同じ標高の2点を結ぶと走向がわかる。傾斜の角は、走向に<b>直角な方向</b>の水平距離と高さの差から求める。"},
 {"lv": "B", "tag": "断面図の読み取り",
  "q": "図は、ある地域の地質断面図である。a〜e は堆積岩の地層、F は断層、U は地層の境界面、G は火成岩の岩脈である。d の礫岩には、c の石灰岩の礫が含まれていた。地層の逆転はないものとする。" + _fig_sec() +
       "(1) 断層 F の種類を答えよ。また、F を生じさせた力はどのような力か。<br>(2) 境界面 U を何というか。また、U は何を示しているか。<br>(3) a, b, c, d, e の堆積、F の活動、U の形成、G の貫入を、古いものから順に並べよ。<br>(4) G が e より古いと判断できる理由を答えよ。",
  "a": "(1) 正断層。左右に引っ張る力　(2) 不整合（面）。この地域がいったん陸上に出て侵食を受けたこと　(3) a → b → c → F → U → d → G → e　(4) G は d を貫いているが、e は貫いていないから。",
  "s": "(1) F は右へ傾いた断層面で、その上側（右側）の地層が、左側に比べて下にずれている。上盤が下がっているので正断層で、地殻が引き伸ばされる（引っ張りの）力がはたらいた。<br>(2) U は傾いた a〜c と F を切っており、その上に基底礫岩（d）がのっているので不整合面。a〜c が堆積したあと、傾き、断層が生じ、隆起して侵食され、再び沈降して d が堆積した。<br>(3) F は a〜c を切るので c の堆積より後。U は F を切るので F より後。G は d まで貫くので d より後で、e には達していないので e より前。<br>(4) 貫入した岩体は、貫いている地層より新しい（切っているものが新しい）。G は e に切られる形になっているので e より古い。<br><b>ポイント</b>：地史の決め手は「切る・切られる」と「上下（累重）」。断層は上盤の動きで正・逆を判断する。"},
 {"lv": "B", "tag": "考察",
  "q": "(1) ある砂岩層の中で、粒子が層の上部から下部に向かってしだいに細かくなっていた。この砂岩層は逆転していると考えられるか。理由とともに答えよ。<br>(2) (1) のような粒子の配列は、どのようにしてできるか。<br>(3) 地層の上下を判定するのに使える堆積構造を、(1) のもの以外に1つあげよ。<br>(4) 地層が波打つように曲がっている構造を何というか。また、山形に曲がった部分と谷形に曲がった部分をそれぞれ何というか。",
  "a": "(1) 逆転している。ふつうは下ほど粗く上ほど細かい（級化層理）のに、上下が逆になっているから。　(2) 水中で一度に運ばれた粒子のうち、大きく重い粒子ほど速く沈むため。　(3) 斜交葉理（クロスラミナ）、漣痕（リプルマーク）、生痕化石 など　(4) 褶曲。山形が背斜、谷形が向斜。",
  "s": "(1)(2) 混濁流（乱泥流）などで一度に運ばれた砂や泥は、大きい粒子から先に沈むので、1つの層の中で下が粗く上が細かくなる（級化層理）。観察された層は上が粗いので、上下が逆転している。<br>(3) 斜交葉理は、上の層に切られている側が上になる。生痕化石（巣穴の跡など）も上下の判定に使える。<br>(4) 褶曲は水平方向に圧縮する力で生じる。背斜の軸部では古い地層が、向斜の軸部では新しい地層が中心に現れる（逆転していない場合）。<br><b>ポイント</b>：級化層理は「下が粗く上が細かい」が正常。逆なら地層の逆転を疑う。"},
 {"lv": "C", "tag": "地質図の読み取り",
  "q": "図は、ある地域の地形図に、泥岩層と砂岩層の境界線（赤い線）を記入した地質図である。茶色の線は 10 m ごとの等高線で、数値は標高 [m] を表す。白い線は 20 m ごとの方眼である。境界面は平面で、地層の逆転や断層はないものとする。" + _fig_map() +
       "(1) 境界線と標高 80 m の等高線との2つの交点を結ぶ直線は、何を表しているか。また、その向きを答えよ。<br>(2) 境界面はどちらの向きに傾斜しているか。<br>(3) 境界面の傾斜の角を求めよ。<br>(4) 地点 P（標高 78 m）で鉛直にボーリングを行うと、何 m の深さで境界面に達するか。<br>(5) 泥岩層と砂岩層のうち、新しいのはどちらか。<br>(6) 境界線が谷の部分で北へ張り出している理由を、境界面の傾斜と関連づけて答えよ。",
  "a": r"(1) 境界面の標高 80 m の走向線。東西方向　(2) 北　(3) $45^\circ$　(4) 48 m　(5) 泥岩層　(6) 境界面は北へ傾いているので、標高の低い谷では、境界面が地表と交わる位置が北（傾斜の向き）へずれるから。",
  "s": r"(1) 境界線と等高線の交点では、境界面の標高がその等高線の値に等しい。80 m の等高線とは $y=140\,\mathrm{m}$ の2点（$x=70,\ 130\,\mathrm{m}$）で交わり、これを結ぶ直線は東西方向。境界面上の同じ標高の点を結んだ線（走向線）なので、走向は東西。<br>(2) 100 m の等高線とは $y=120\,\mathrm{m}$ の2点（$x=10,\ 190\,\mathrm{m}$）で交わる。北の走向線ほど標高が低いので、北へ傾斜している。<br>(3) 走向線の間隔（水平距離）は $140-120=20\,\mathrm{m}$、標高の差は $100-80=20\,\mathrm{m}$。$\tan\theta=\dfrac{20}{20}=1$ より $45^\circ$。<br>(4) 境界面の標高は北へ $1\,\mathrm{m}$ 進むごとに $1\,\mathrm{m}$ 下がる。P は $y=190\,\mathrm{m}$ なので、境界面の標高は $80-(190-140)=30\,\mathrm{m}$。深さは $78-30=48\,\mathrm{m}$。<br>(5) P の地下では、泥岩層の下に境界面があり、その下が砂岩層。逆転がないので、上にある泥岩層が新しい。<br>(6) 境界線は「地形面と境界面の交線」。谷は周りより低いので、北へ傾く境界面と交わるのは、より北の（境界面が低くなっている）所になる。<br><b>ポイント</b>：地質図では「境界線と等高線の交点」が境界面の標高を教えてくれる。同じ標高の交点を結んで走向線を引き、走向線の間隔から傾斜を求める。"},
 {"lv": "C", "tag": "計算・論述",
  "q": "ある地域では、下位の砂岩泥岩互層の上に、不整合面を隔てて礫岩層が重なっている。砂岩泥岩互層には2枚の凝灰岩層 T1, T2 がはさまれ、放射年代はそれぞれ 120万年前、90万年前で、T1 と T2 の間の地層の厚さは 45 m であった。T2 から不整合面までの砂岩泥岩互層の厚さは 30 m である。また、不整合面の 6.0 m 上の礫岩層中には、40万年前の凝灰岩層 T3 がはさまれていた。<br>(1) T1 と T2 の間の地層の平均の堆積速度は何 mm/年 か。<br>(2) (1) の速度で堆積が続いたとすると、不整合面のすぐ下の砂岩泥岩互層は何年前に堆積したものか。<br>(3) 礫岩層も同じ速度で堆積したとすると、礫岩層の堆積が始まったのは何年前か。<br>(4) (2)(3) から、不整合面をはさんで記録が欠けている期間は何年間か。また、この期間にこの地域で起こったことを、60字以内で述べよ。",
  "a": r"(1) $0.15\,\mathrm{mm/年}$　(2) 70万年前　(3) 44万年前　(4) 26万年間。解答例：砂岩泥岩互層が隆起して陸上に出て侵食を受け、その後に沈降して再び水中となり、礫岩層が堆積し始めた。（49字）",
  "s": r"(1) $45\,\mathrm{m}$ が $120-90=30\,\mathrm{万年}$ で堆積したので $\dfrac{45\times10^3\,\mathrm{mm}}{3.0\times10^5\,\mathrm{年}}=0.15\,\mathrm{mm/年}$。<br>(2) $30\,\mathrm{m}$ の堆積にかかる時間は $\dfrac{3.0\times10^4\,\mathrm{mm}}{0.15\,\mathrm{mm/年}}=2.0\times10^5\,\mathrm{年}$。$90-20=70\,\mathrm{万年前}$。<br>(3) $6.0\,\mathrm{m}$ の堆積に $\dfrac{6.0\times10^3}{0.15}=4.0\times10^4\,\mathrm{年}$ かかるので、$40+4=44\,\mathrm{万年前}$。<br>(4) $70-44=26\,\mathrm{万年間}$。この間に、堆積していた地層の一部が侵食で失われた可能性もあるので、(2) の 70万年前は「残っている地層のうち最も新しい部分」の年代である。<br><b>ポイント</b>：堆積速度＝厚さ÷時間。不整合面は「時間の空白」で、その長さは上下の地層の年代から見積もれる。"},
]}}


def verify():
    items = CH[4]["items"]
    # 4-5 柱状図：X・Y が各地点で1回ずつ、C の不整合（礫岩の下）の位置
    for n, lay in COLS.items():
        labs = [lab for _, _, lab in lay if lab]
        assert labs in (["Y", "X"], ["Y"], ["X"]), labs
    assert sum(t for _, t, _ in COLS["C"][:4]) == 9 and COLS["C"][3][0] == "gr" and COLS["C"][4][0] == "ls"
    # 厚さが等しいとき矛盾しない：Y の上の砂岩 A 4 m < B 5 m、X–Y 間の泥岩 A 5 m ≧ B 3 m・C 2 m（地表または柱状図の端で切れている）
    assert COLS["A"][0][1] < COLS["B"][1][1] and COLS["A"][2][1] >= COLS["B"][3][1] and COLS["A"][2][1] >= COLS["C"][0][1]
    assert COLS["A"][4][1] <= COLS["C"][2][1]
    # 4-6 三点問題
    el = {n: h - d for n, (x, y, h, d) in BOR.items()}
    assert el == {"A": 100, "B": 100, "C": 50}
    t = (el["A"] - el["C"]) / (BOR["C"][0] - BOR["A"][0])
    assert t == 0.5 and min(TANS, key=lambda d: abs(math.tan(math.radians(d)) - t)) == 27
    assert abs(round(math.tan(math.radians(27)), 2) - 0.51) < 1e-9
    zD = el["A"] - t * PD[0]
    assert zD == 0 and PD[2] - zD == 100
    # 4-7 断面図：右側（上盤）が下がっている → 正断層。断層面は右へ傾く。岩脈は d の上面まで。
    assert F_BOT[0] > F_TOP[0] and OFF > 0
    for x, y, s in [(25, 100, "c"), (95, 130, "b"), (160, 158, "a")]:      # 左側のラベルが正しい層にある
        xf = F_TOP[0] + (y - U_Y) * (F_BOT[0] - F_TOP[0]) / (BOT_Y - U_Y)
        assert x < xf and U_Y < y < BOT_Y
        assert {"c": y < _lbc(x), "b": _lbc(x) < y < _lab(x), "a": y > _lab(x)}[s]
    for x, y, s in [(250, 88, "c"), (275, 115, "b"), (285, 155, "a")]:
        xf = F_TOP[0] + (y - U_Y) * (F_BOT[0] - F_TOP[0]) / (BOT_Y - U_Y)
        assert x > xf
        assert {"c": y < _lbc(x) + OFF, "b": _lbc(x) + OFF < y < _lab(x) + OFF, "a": y > _lab(x) + OFF}[s]
    assert _lab(66) < BOT_Y      # 岩脈 G は a まで貫いている
    # 4-10 地質図：交点と走向線、傾斜、P の深さ
    for Z, yz, xs in ((80, 140, (70, 130)), (100, 120, (10, 190)), (90, 130, (40, 160))):
        for x in xs:
            assert abs(ZT(x, yz) - Z) < 1e-9 and abs(ZP(x, yz) - Z) < 1e-9 and abs(_trace_y(x) - yz) < 1e-9
    assert math.isclose(math.degrees(math.atan((100 - 80) / (140 - 120))), 45)
    assert ZT(MP[0], MP[1]) == MP[2] and ZP(*MP[:2]) == 30 and MP[2] - ZP(*MP[:2]) == 48
    assert ZT(MP[0], MP[1]) > ZP(MP[0], MP[1])                    # P の地表は境界面より上（泥岩）
    assert ZT(MQ[0], MQ[1]) < ZP(MQ[0], MQ[1])                    # Q は境界面より下（砂岩）
    assert _trace_y(100) == max(_trace_y(x) for x in range(0, 201))  # 谷で北へ張り出す
    # 4-11 堆積速度
    v = 45e3 / 30e4
    assert abs(v - 0.15) < 1e-12
    assert abs(30e3 / v - 2.0e5) < 1e-6 and abs(6.0e3 / v - 4.0e4) < 1e-6
    assert 90 - 20 == 70 and 40 + 4 == 44 and 70 - 44 == 26
    _form(items)


def _form(items):
    lv = [it["lv"] for it in items]
    assert lv == sorted(lv) and lv.count("A") == 4 and lv.count("B") in (4, 5) and lv.count("C") == 2, lv
    for it in items:
        for k in ("lv", "tag", "q", "a", "s"):
            assert it.get(k), k
        assert "<b>ポイント</b>" in it["s"]
        for k in ("q", "a", "s"):
            assert "$$" not in it[k] and it[k].count("$") % 2 == 0, (k, it["q"][:30])
        lims = [int(m) for m in re.findall(r"(\d+)字以内", it["q"])]
        ess = re.findall(r"解答例：(.*?)（(\d+)字）", it["a"])
        assert len(lims) == len(ess), (lims, ess)
        for (body, n), lim in zip(ess, lims):
            assert len(body) == int(n) <= lim, (len(body), n, lim, body)
