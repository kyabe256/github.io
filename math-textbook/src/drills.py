"""各章の計算ドリルを生成する。答えは sympy / Fraction で計算するので必ず正しい。
出力: drills.json  {章番号: {"title":..., "items":[[問題latex, 答えlatex], ...]}}"""
import json, random, math, re
from fractions import Fraction as F
import sympy as sp
from sympy import latex, sqrt, Rational as R, pi, symbols, expand, factor, simplify

import os
random.seed(int(os.environ.get("SEED", "20261007")))
x, y, n, k, t = symbols('x y n k t')
D = {}

def L(e):
    # \sin{\left(x \right)} → \sin\left(x\right)（関数名の直後だけ整形）
    return FUNC_RE.sub(lambda m: m.group(1) + "\\left(" + m.group(2) + "\\right)", latex(e))

FUNC_RE = re.compile(r"(\\(?:sin|cos|tan|log)(?:\^\{\d+\})?)\{\\left\(([^{}]*?) \\right\)\}")

def add(ch, title, items):
    D[ch] = {"title": title, "items": items}

def nz(a, b):
    while True:
        v = random.randint(a, b)
        if v != 0:
            return v

def sgn(v):
    return f"({v})" if v < 0 else f"{v}"

def frac_tex(q):
    q = F(q)
    if q.denominator == 1:
        return str(q.numerator)
    s = "-" if q < 0 else ""
    return f"{s}\\frac{{{abs(q.numerator)}}}{{{q.denominator}}}"

def lin(a, b, var="x"):
    """a*var + b を latex で"""
    return L(sp.Symbol(var) * a + b)

# ---------- 1 正負の数 ----------
items = []
for i in range(30):
    kind = i % 5
    if kind == 0:
        a, b, c = nz(-15, 15), nz(-15, 15), nz(-15, 15)
        q = f"{a} + {sgn(b)} - {sgn(c)}"
        v = a + b - c
    elif kind == 1:
        a, b, c = nz(-9, 9), nz(-9, 9), nz(-5, 5)
        q = f"{sgn(a)} \\times {sgn(b)} \\times {sgn(c)}"
        v = a * b * c
    elif kind == 2:
        b = nz(-9, 9); a = b * nz(-9, 9); c = nz(-9, 9)
        q = f"{a} \\div {sgn(b)} + {sgn(c)}"
        v = a // b + c
    elif kind == 3:
        a, e, c = nz(-5, 5), random.choice([2, 3]), nz(-4, 4)
        q = f"({a})^{e} - {sgn(c)} \\times 3"
        v = a ** e - c * 3
    else:
        a, b = random.randint(2, 4), nz(-6, 6)
        q = f"-{a}^2 + {sgn(b)} \\times (-2)"
        v = -a * a + b * (-2)
    items.append([q, str(v)])
add(1, "正負の数", items)

# ---------- 2 文字式 ----------
items = []
for i in range(24):
    if i < 12:
        a, b, c, d, e, f = [nz(-6, 6) for _ in range(6)]
        expr_t = f"{a}({lin(b,0)} {'+' if c>0 else '-'} {abs(c)}y) - {sgn(d)}({lin(e,0)} {'+' if f>0 else '-'} {abs(f)}y)"
        v = expand(a * (b * x + c * y) - d * (e * x + f * y))
        items.append([expr_t, L(v)])
    else:
        a, b, c, d = nz(-5, 5), nz(-5, 5), nz(-5, 5), nz(-5, 5)
        p, q = random.choice([(2, 3), (3, 4), (2, 5), (4, 6), (3, 5)])
        e = (a * x + b) / p - (c * x + d) / q
        items.append([f"\\dfrac{{{L(a*x+b)}}}{{{p}}} - \\dfrac{{{L(c*x+d)}}}{{{q}}}", L(sp.together(sp.expand(e)))])
add(2, "文字式の計算", items)

# ---------- 3 一次方程式 ----------
items = []
for i in range(24):
    sol = nz(-9, 9)
    if i < 16:
        a, c = nz(-9, 9), nz(-9, 9)
        while a == c:
            c = nz(-9, 9)
        b = nz(-12, 12)
        d = a * sol + b - c * sol
        items.append([f"{L(a*x+b)} = {L(c*x+d)}", f"x={sol}"])
    else:
        p, q = random.choice([(2, 3), (3, 4), (2, 5), (4, 3), (6, 4)])
        a, b = nz(-4, 4), nz(-6, 6)
        # (x + a)/p = (x + b)/q + c  を作る
        lhs = F(sol + a, p); rhs0 = F(sol + b, q); c = lhs - rhs0
        if c.denominator != 1:
            c = F(round(float(c)))
            # 解を逆算
            s = sp.solve(sp.Eq((x + a) / p, (x + b) / q + int(c)), x)[0]
            ans = L(s)
        else:
            ans = str(sol)
        items.append([f"\\dfrac{{{L(x+a)}}}{{{p}}} = \\dfrac{{{L(x+b)}}}{{{q}}} {'+' if c>=0 else '-'} {abs(int(c))}", f"x={ans}"])
add(3, "一次方程式", items)

# ---------- 4 連立方程式 ----------
items = []
for i in range(16):
    sx, sy = nz(-6, 6), nz(-6, 6)
    while True:
        a, b, c, d = [nz(-5, 5) for _ in range(4)]
        if a * d - b * c != 0:
            break
    e1, e2 = a * sx + b * sy, c * sx + d * sy
    items.append([f"\\begin{{cases}}{L(a*x+b*y)}={e1}\\\\{L(c*x+d*y)}={e2}\\end{{cases}}", f"x={sx},\\ y={sy}"])
add(4, "連立方程式", items)

# ---------- 5 一次関数 ----------
items = []
for i in range(20):
    a, b = nz(-5, 5), random.randint(-8, 8)
    if i < 10:
        x1 = random.randint(-4, 2); x2 = x1 + random.randint(1, 4)
        items.append([f"2点 $({x1},{a*x1+b}),\\ ({x2},{a*x2+b})$ を通る直線", f"y={L(a*x+b)}"])
    else:
        a2, b2 = nz(-5, 5), random.randint(-8, 8)
        while a2 == a:
            a2 = nz(-5, 5)
        sx = F(b2 - b, a - a2); sy = a * sx + b
        items.append([f"$y={L(a*x+b)}$ と $y={L(a2*x+b2)}$ の交点", f"\\left({frac_tex(sx)},\\ {frac_tex(sy)}\\right)"])
add(5, "一次関数（直線の式・交点）", items)

# ---------- 6 平面図形・空間図形 ----------
items = []
for i in range(20):
    if i < 8:
        r = random.randint(2, 12); ang = random.choice([30, 45, 60, 72, 90, 120, 135, 150, 240, 270])
        arc = R(2 * r * ang, 360) * pi; area = R(r * r * ang, 360) * pi
        items.append([f"半径 {r}、中心角 ${ang}^\\circ$ のおうぎ形の弧の長さと面積", f"{L(arc)},\\ {L(area)}"])
    elif i < 14:
        r, h = random.randint(2, 9), random.randint(2, 12)
        kind = random.choice(["円柱", "円錐"])
        v = pi * r * r * h * (R(1, 3) if kind == "円錐" else 1)
        items.append([f"底面の半径 {r}、高さ {h} の{kind}の体積", L(v)])
    else:
        r = random.randint(1, 9)
        items.append([f"半径 {r} の球の体積と表面積", f"{L(R(4,3)*pi*r**3)},\\ {L(4*pi*r*r)}"])
add(6, "おうぎ形・立体の計量", items)

# ---------- 7 合同・多角形 ----------
items = []
for i in range(16):
    nn = random.randint(5, 20)
    if i % 2 == 0:
        items.append([f"正{nn}角形の1つの内角", f"{L(R(180*(nn-2), nn))}^\\circ"])
    else:
        items.append([f"内角の和が ${180*(nn-2)}^\\circ$ の多角形", f"{nn}角形"])
add(7, "多角形の角", items)

# ---------- 8 平方根 ----------
items = []
used = set()
for i in range(30):
    kind = i % 3
    if kind == 0:
        a, b = random.randint(1, 5), random.choice([2, 3, 5, 6, 7])
        c, d = random.randint(1, 5), b
        m1, m2 = a * a * b, c * c * d
        s = random.choice([1, -1])
        q = f"\\sqrt{{{m1}}} {'+' if s>0 else '-'} \\sqrt{{{m2}}}"
        v = sqrt(m1) + s * sqrt(m2)
    elif kind == 1:
        a, b = random.choice([(2, 3), (3, 5), (2, 7), (5, 2), (3, 2), (6, 3)])
        c = random.randint(1, 4)
        q = f"(\\sqrt{{{a}}} + {c}\\sqrt{{{b}}})^2"
        v = expand((sqrt(a) + c * sqrt(b)) ** 2)
    else:
        a = random.randint(1, 9); b = random.choice([2, 3, 5, 6, 7])
        q = f"\\dfrac{{{a}}}{{\\sqrt{{{b}}}}}"
        v = sp.radsimp(a / sqrt(b))
    items.append([q, L(v)])
add(8, "平方根の計算", items)

# ---------- 9 展開と因数分解 ----------
items = []
for i in range(36):
    if i < 12:
        a, b, c, d = nz(-5, 5), nz(-7, 7), nz(-5, 5), nz(-7, 7)
        e = (a * x + b) * (c * x + d)
        items.append([f"({L(a*x+b)})({L(c*x+d)})", L(expand(e))])
    else:
        kind = i % 4
        if kind == 0:
            p, q = nz(-9, 9), nz(-9, 9); e = expand((x + p) * (x + q))
        elif kind == 1:
            p = random.randint(1, 9); m = random.randint(1, 4); e = expand((m * x) ** 2 - p * p)
        elif kind == 2:
            p = nz(-8, 8); c = random.randint(2, 4); e = expand(c * (x + p) ** 2)
        else:
            a, b, c, d = random.randint(1, 3), nz(-5, 5), random.randint(1, 3), nz(-5, 5)
            e = expand((a * x + b) * (c * x + d))
        items.append([L(e), L(factor(e))])
add(9, "展開と因数分解（前半が展開、後半が因数分解）", items)

# ---------- 10 二次方程式 ----------
items = []
for i in range(24):
    if i < 12:
        p, q = nz(-9, 9), nz(-9, 9); e = expand((x - p) * (x - q))
    else:
        a = random.randint(1, 3); b = random.randint(-7, 7); c = nz(-6, 6)
        while b * b - 4 * a * c < 0 or sp.sqrt(b * b - 4 * a * c).is_rational:
            b = random.randint(-7, 7); c = nz(-6, 6)
        e = a * x ** 2 + b * x + c
    sols = sorted(set(sp.solve(e, x)), key=lambda s: float(s))
    items.append([f"{L(e)}=0", "x=" + ",\\ ".join(L(s) for s in sols)])
add(10, "二次方程式", items)

# ---------- 11 y=ax^2 ----------
items = []
for i in range(16):
    a = nz(-4, 4)
    if i % 2 == 0:
        p = random.randint(-4, 2); q = p + random.randint(1, 4)
        items.append([f"$y={L(a*x**2)}$ で $x$ が ${p}$ から ${q}$ まで増加するときの変化の割合", str(a * (p + q))])
    else:
        p = random.randint(-3, 2); q = p + random.randint(2, 5)
        vals = [a * p * p, a * q * q] + ([0] if p <= 0 <= q else [])
        items.append([f"$y={L(a*x**2)}$ の $ {p} \\le x \\le {q}$ における $y$ の変域", f"{min(vals)} \\le y \\le {max(vals)}"])
add(11, "関数 y=ax²", items)

# ---------- 12 三平方 ----------
items = []
for i in range(20):
    a, b = random.randint(1, 12), random.randint(1, 12)
    if i % 2 == 0:
        items.append([f"直角をはさむ2辺が {a}, {b} の直角三角形の斜辺", L(sqrt(a * a + b * b))])
    else:
        c = max(a, b) + random.randint(1, 6)
        items.append([f"斜辺 {c}、他の1辺 {a} の直角三角形の残りの辺", L(sqrt(c * c - a * a))])
add(12, "三平方の定理", items)

# ---------- 13 確率 ----------
items = []
for s in range(2, 13):
    cnt = sum(1 for i in range(1, 7) for j in range(1, 7) if i + j == s)
    items.append([f"サイコロ2個の目の和が {s} になる確率", L(R(cnt, 36))])
for nn in range(2, 7):
    items.append([f"硬貨を {nn} 回投げて少なくとも1回表が出る確率", L(1 - R(1, 2 ** nn))])
for m in range(2, 7):
    cnt = sum(1 for i in range(1, 7) for j in range(1, 7) if (i * j) % m == 0)
    items.append([f"サイコロ2個の目の積が {m} の倍数になる確率", L(R(cnt, 36))])
add(13, "確率", items)

# ---------- 14 数と式・不等式 ----------
items = []
for i in range(20):
    if i < 10:
        a, b, c = nz(-6, 6), nz(-9, 9), nz(-9, 9)
        v = R(c - b, a)
        items.append([f"{L(a*x+b)} > {c}", f"x {'>' if a>0 else '<'} {L(v)}"])
    else:
        a, r = nz(-6, 6), random.randint(1, 7)
        op = random.choice(["<", "\\ge"])
        if op == "<":
            ans = f"{a-r} < x < {a+r}"
        else:
            ans = f"x \\le {a-r},\\ {a+r} \\le x"
        items.append([f"|{L(x-a)}| {op} {r}", ans])
add(14, "一次不等式・絶対値", items)

# ---------- 15 集合 ----------
items = []
for i in range(10):
    U = list(range(1, 13))
    A = sorted(random.sample(U, 5)); B = sorted(random.sample(U, 5))
    fmt = lambda S: "\\{" + ",".join(map(str, sorted(S))) + "\\}" if S else "\\varnothing"
    items.append([f"$U=\\{{1,\\dots,12\\}},\\ A={fmt(A)},\\ B={fmt(B)}$ のとき $A\\cap B,\\ A\\cup B,\\ \\overline{{A}}\\cap B$",
                  f"{fmt(set(A)&set(B))},\\ {fmt(set(A)|set(B))},\\ {fmt(set(B)-set(A))}"])
add(15, "集合の演算", items)

# ---------- 16 二次関数 ----------
items = []
for i in range(24):
    a = nz(-3, 3); p = nz(-5, 5); q = random.randint(-9, 9)
    e = expand(a * (x - p) ** 2 + q)
    if i < 14:
        items.append([f"y={L(e)}", f"y={L(a)}" + ("" if True else "") + f"(x{'-' if p>0 else '+'}{abs(p)})^2{'+' if q>=0 else '-'}{abs(q)},\\ 頂点({p},{q})"])
    else:
        lo = random.randint(-5, 3); hi = lo + random.randint(2, 5)
        f = sp.Lambda(x, e)
        cands = [lo, hi] + ([p] if lo <= p <= hi else [])
        vals = [(f(c), c) for c in cands]
        mx = max(vals, key=lambda t: t[0]); mn = min(vals, key=lambda t: t[0])
        items.append([f"$y={L(e)}\\ ({lo}\\le x\\le {hi})$ の最大値・最小値",
                      f"最大 {mx[0]}\\,(x={mx[1]}),\\ 最小 {mn[0]}\\,(x={mn[1]})"])
add(16, "二次関数（平方完成・最大最小）", items)
# 表記を整える（a=1, -1 のときの 1( を消す）
for it in D[16]["items"]:
    it[1] = it[1].replace("y=1(", "y=(").replace("y=-1(", "y=-(")

# ---------- 17 三角比 ----------
items = []
angs = [0, 30, 45, 60, 90, 120, 135, 150, 180]
for a in angs[1:-1]:
    th = sp.rad(a)
    tn = "なし" if a == 90 else L(sp.tan(th))
    items.append([f"\\sin {a}^\\circ,\\ \\cos {a}^\\circ,\\ \\tan {a}^\\circ", f"{L(sp.sin(th))},\\ {L(sp.cos(th))},\\ {tn}"])
for i in range(10):
    b, c = random.randint(2, 9), random.randint(2, 9); A = random.choice([60, 120, 90])
    a2 = b * b + c * c - 2 * b * c * sp.cos(sp.rad(A))
    items.append([f"$b={b},\\ c={c},\\ A={A}^\\circ$ のとき $a$ と面積 $S$", f"a={L(sp.radsimp(sp.sqrt(sp.nsimplify(a2))))},\\ S={L(sp.nsimplify(R(1,2)*b*c*sp.sin(sp.rad(A))))}"])
add(17, "三角比", items)

# ---------- 18 データ ----------
items = []
for i in range(10):
    m = random.randint(3, 8)
    data = [random.randint(1, 10) for _ in range(m)]
    mean = R(sum(data), m); var = R(sum(d * d for d in data), m) - mean ** 2
    s = sorted(data); med = R(s[m // 2]) if m % 2 else R(s[m // 2 - 1] + s[m // 2], 2)
    items.append([f"データ ${','.join(map(str,data))}$ の平均値・中央値・分散", f"{L(mean)},\\ {L(med)},\\ {L(var)}"])
add(18, "平均・中央値・分散", items)

# ---------- 19 場合の数 ----------
items = []
for i in range(24):
    kind = i % 4
    nn = random.randint(4, 10); r = random.randint(2, min(5, nn))
    if kind == 0:
        items.append([f"{{}}_{{{nn}}}\\mathrm{{P}}_{{{r}}}", str(math.perm(nn, r))])
    elif kind == 1:
        items.append([f"{{}}_{{{nn}}}\\mathrm{{C}}_{{{r}}}", str(math.comb(nn, r))])
    elif kind == 2:
        items.append([f"{nn}人が円形に並ぶ方法", str(math.factorial(nn - 1))])
    else:
        nn2 = random.randint(3, 6); r2 = random.randint(1, nn2)
        items.append([f"サイコロを {nn2} 回投げて1の目がちょうど {r2} 回出る確率",
                      L(math.comb(nn2, r2) * R(1, 6) ** r2 * R(5, 6) ** (nn2 - r2))])
add(19, "場合の数と確率", items)

# ---------- 20 整数 ----------
items = []
for i in range(24):
    kind = i % 4
    if kind == 0:
        m = random.choice([12, 18, 24, 36, 48, 60, 72, 90, 96, 100, 120, 144, 180, 200, 210, 240, 360, 420])
        items.append([f"{m} の素因数分解と正の約数の個数", f"{L(sp.factorint(m, visual=True))}\\ (= {m}),\\ {sp.divisor_count(m)}個".replace("\\cdot", "\\cdot ")])
    elif kind == 1:
        g = random.randint(2, 15); a, b = g * random.randint(2, 20), g * random.randint(2, 20)
        items.append([f"{a} と {b} の最大公約数・最小公倍数", f"{math.gcd(a,b)},\\ {a*b//math.gcd(a,b)}"])
    elif kind == 2:
        m = random.randint(5, 100)
        items.append([f"{m} を2進法で表せ", f"{bin(m)[2:]}_{{(2)}}"])
    else:
        b = random.choice([3, 5]); m = random.randint(10, 120)
        digs = []
        v = m
        while v:
            digs.append(str(v % b)); v //= b
        s = "".join(reversed(digs))
        items.append([f"{s}_{{({b})}} を10進法で表せ", str(m)])
add(20, "整数の性質", items)
# factorint visual の表記を整形
for it in D[20]["items"]:
    if "素因数" in it[0]:
        m = int(it[0].split()[0])
        fac = sp.factorint(m)
        s = " \\cdot ".join(f"{p}^{{{e}}}" if e > 1 else f"{p}" for p, e in fac.items())
        it[1] = f"{s},\\ {sp.divisor_count(m)}個"

# ---------- 21 図形の性質 ----------
items = []
for i in range(12):
    if i % 2 == 0:
        ab, ac = random.randint(3, 12), random.randint(3, 12); bc = random.randint(abs(ab - ac) + 1, ab + ac - 1)
        items.append([f"$AB={ab},\\ AC={ac},\\ BC={bc}$ の $\\triangle ABC$ で、$\\angle A$ の二等分線と $BC$ の交点を $D$ とするときの $BD$", L(R(bc * ab, ab + ac))])
    else:
        pa, pb, pc = random.randint(2, 9), random.randint(2, 9), random.randint(2, 9)
        items.append([f"2つの弦 $AB,\\ CD$ が点 $P$ で交わり $PA={pa},\\ PB={pb},\\ PC={pc}$ のときの $PD$", L(R(pa * pb, pc))])
add(21, "図形の性質", items)

# ---------- 22 複素数・式と証明 ----------
I = sp.I
items = []
for i in range(24):
    kind = i % 3
    if kind == 0:
        a, b, c, d = nz(-5, 5), nz(-5, 5), nz(-5, 5), nz(-5, 5)
        items.append([f"({L(a+b*I)})({L(c+d*I)})", L(expand((a + b * I) * (c + d * I)))])
    elif kind == 1:
        a, b, c, d = nz(-5, 5), nz(-5, 5), nz(-4, 4), nz(-4, 4)
        items.append([f"\\dfrac{{{L(a+b*I)}}}{{{L(c+d*I)}}}", L(sp.simplify(sp.expand_complex((a + b * I) / (c + d * I))))])
    else:
        a, nn, r = random.randint(1, 3), random.randint(3, 7), None
        r = random.randint(1, nn - 1)
        items.append([f"$({L(x+a)})^{{{nn}}}$ の展開式における $x^{{{r}}}$ の係数", str(math.comb(nn, r) * a ** (nn - r))])
add(22, "複素数・二項定理", items)

# ---------- 23 図形と方程式 ----------
items = []
for i in range(20):
    kind = i % 3
    if kind == 0:
        a, b, r = nz(-6, 6), nz(-6, 6), random.randint(1, 8)
        e = expand((x - a) ** 2 + (y - b) ** 2 - r * r)
        items.append([f"{L(e)}=0 の中心と半径", f"({a},{b}),\\ {r}"])
    elif kind == 1:
        A, B, C = nz(-5, 5), nz(-5, 5), nz(-9, 9); px, py = nz(-5, 5), nz(-5, 5)
        dist = sp.radsimp(sp.Abs(A * px + B * py + C) / sp.sqrt(A * A + B * B))
        items.append([f"点 $({px},{py})$ と直線 ${L(A*x+B*y+C)}=0$ の距離", L(dist)])
    else:
        x1, y1, x2, y2 = [nz(-8, 8) for _ in range(4)]; m, nn = random.randint(1, 4), random.randint(1, 4)
        px = R(nn * x1 + m * x2, m + nn); py = R(nn * y1 + m * y2, m + nn)
        items.append([f"2点 $({x1},{y1}),\\ ({x2},{y2})$ を ${m}:{nn}$ に内分する点", f"\\left({L(px)},\\ {L(py)}\\right)"])
add(23, "図形と方程式", items)

# ---------- 24 三角関数 ----------
items = []
for num, den in [(7, 6), (5, 4), (4, 3), (3, 2), (5, 3), (7, 4), (11, 6), (2, 3), (5, 6), (-1, 3), (-3, 4), (13, 6)]:
    th = R(num, den) * pi
    tn = "なし" if sp.cos(th) == 0 else L(sp.tan(th))
    items.append([f"\\theta={L(th)}\\ のとき\\ \\sin\\theta,\\ \\cos\\theta,\\ \\tan\\theta", f"{L(sp.sin(th))},\\ {L(sp.cos(th))},\\ {tn}"])
for q, a in [("\\sin 75^\\circ", "\\frac{\\sqrt{6}+\\sqrt{2}}{4}"), ("\\cos 75^\\circ", "\\frac{\\sqrt{6}-\\sqrt{2}}{4}"),
             ("\\sin 15^\\circ", "\\frac{\\sqrt{6}-\\sqrt{2}}{4}"), ("\\tan 75^\\circ", "2+\\sqrt{3}"), ("\\cos 105^\\circ", "\\frac{\\sqrt{2}-\\sqrt{6}}{4}")]:
    items.append([q, a])
for a, b in [(1, 1), (1, sp.sqrt(3)), (sp.sqrt(3), 1), (3, 4), (-1, 1), (1, -sp.sqrt(3))]:
    rr = sp.sqrt(a * a + b * b)
    ta = {1: "", -1: "-"}.get(a, L(a)); tb = {1: "+", -1: "-"}.get(b, ("+" + L(b)) if not str(b).startswith("-") else L(b))
    items.append([f"{ta}\\sin\\theta {tb}\\cos\\theta\\ \\text{{の最大値・最小値}}", f"{L(rr)},\\ {L(-rr)}"])
add(24, "三角関数", items)

# ---------- 25 指数・対数 ----------
items = []
for i in range(24):
    kind = i % 4
    if kind == 0:
        b = random.choice([2, 3, 4, 8, 9, 27, 16, 25]); num, den = nz(-3, 3), random.choice([2, 3, 4])
        items.append([f"{b}^{{{L(R(num,den))}}}", L(sp.nsimplify(sp.Integer(b) ** R(num, den)))])
    elif kind == 1:
        b = random.choice([2, 3, 5]); e1 = random.randint(1, 6); m = b ** e1
        items.append([f"\\log_{{{b}}} {m}", str(e1)])
    elif kind == 2:
        b = random.choice([2, 3]); p, q = random.randint(2, 5), random.randint(1, 4)
        u = random.randint(2, 7)
        items.append([f"\\log_{{{b}}} {u*b**p} - \\log_{{{b}}} {u}", str(p)])
    else:
        b = random.choice([2, 3]); p = random.randint(2, 6)
        items.append([f"\\log_{{{b**2}}} {b**p}", L(R(p, 2))])
add(25, "指数・対数の計算", items)

# ---------- 26 微分(II) ----------
items = []
for i in range(24):
    cs = [random.randint(-6, 6) for _ in range(4)]
    f = cs[0] * x ** 3 + cs[1] * x ** 2 + cs[2] * x + cs[3]
    if f.is_number or sp.degree(f, x) < 2:
        f = f + x ** 3
    if i < 12:
        items.append([f"f(x)={L(f)}\\ \\text{{のとき}}\\ f'(x)", L(sp.diff(f, x))])
    elif i < 18:
        a = random.randint(-2, 2)
        fa, d = f.subs(x, a), sp.diff(f, x).subs(x, a)
        items.append([f"$y={L(f)}$ の $x={a}$ における接線", f"y={L(expand(d*(x-a)+fa))}"])
    else:
        p, q = sorted(random.sample(range(-4, 5), 2))
        g = expand(sp.integrate(3 * (x - p) * (x - q), x)) + random.randint(-5, 5)
        items.append([f"$f(x)={L(g)}$ の極大値・極小値", f"極大 {L(g.subs(x,p))}\\,(x={p}),\\ 極小 {L(g.subs(x,q))}\\,(x={q})"])
add(26, "微分（数II）", items)

# ---------- 27 積分(II) ----------
items = []
for i in range(24):
    cs = [random.randint(-6, 6) for _ in range(3)]
    f = cs[0] * x ** 2 + cs[1] * x + cs[2]
    if f == 0:
        f = x ** 2
    if i < 8:
        items.append([f"\\displaystyle\\int ({L(f)})\\,dx", L(sp.integrate(f, x)) + "+C"])
    elif i < 16:
        a = random.randint(-2, 1); b = a + random.randint(1, 3)
        items.append([f"\\displaystyle\\int_{{{a}}}^{{{b}}} ({L(f)})\\,dx", L(sp.integrate(f, (x, a, b)))])
    else:
        p, q = sorted(random.sample(range(-4, 5), 2)); m = random.choice([1, -1])
        g = expand(m * (x - p) * (x - q))
        items.append([f"$y={L(g)}$ と $x$ 軸で囲まれた部分の面積", L(R((q - p) ** 3, 6))])
add(27, "積分（数II）", items)

# ---------- 28 数列 ----------
items = []
for i in range(24):
    kind = i % 4
    if kind == 0:
        a, d, m = nz(-9, 9), nz(-5, 5), random.randint(10, 30)
        items.append([f"初項 {a}、公差 {d} の等差数列の第{m}項と初項から第{m}項までの和", f"{a+(m-1)*d},\\ {m*(2*a+(m-1)*d)//2}"])
    elif kind == 1:
        a, r, m = nz(-3, 3), random.choice([2, 3, -2, R(1, 2)]), random.randint(4, 8)
        s = sp.nsimplify(sum(a * r ** j for j in range(m)))
        items.append([f"初項 {a}、公比 ${L(r)}$ の等比数列の第{m}項と初項から第{m}項までの和", f"{L(a*r**(m-1))},\\ {L(s)}"])
    elif kind == 2:
        a, b = nz(-5, 5), random.randint(-5, 5); m = random.randint(5, 20)
        items.append([f"\\displaystyle\\sum_{{k=1}}^{{{m}}} ({L(a*k+b)})", str(sum(a * j + b for j in range(1, m + 1)))])
    else:
        a, b = nz(-3, 3), random.randint(-3, 3)
        e = a * k ** 2 + b * k
        items.append([f"\\displaystyle\\sum_{{k=1}}^{{n}} ({L(e)})", L(factor(sp.summation(e, (k, 1, n))))])
add(28, "数列", items)

# ---------- 29 統計的推測 ----------
items = []
for i in range(12):
    if i % 2 == 0:
        nn = random.choice([36, 72, 100, 144, 180, 360, 400, 600]); p = random.choice([R(1, 2), R(1, 6), R(1, 3), R(1, 4), R(1, 5)])
        items.append([f"二項分布 $B({nn},{L(p)})$ の期待値と標準偏差", f"{L(nn*p)},\\ {L(sp.sqrt(nn*p*(1-p)))}"])
    else:
        m, s, xx = random.randint(40, 70), random.choice([5, 10, 15, 20]), None
        xx = m + s * random.choice([-2, -1, 1, 2, R(1, 2), R(3, 2)])
        items.append([f"$X$ が $N({m},{s}^2)$ に従うとき $X={L(xx)}$ を標準化した値 $Z$", L((xx - m) / s)])
add(29, "統計的推測", items)

# ---------- 30 ベクトル ----------
items = []
for i in range(20):
    a1, a2, b1, b2 = [nz(-6, 6) for _ in range(4)]
    kind = i % 3
    if kind == 0:
        items.append([f"$\\vec a=({a1},{a2}),\\ \\vec b=({b1},{b2})$ のとき $\\vec a\\cdot\\vec b,\\ |\\vec a+\\vec b|$", f"{a1*b1+a2*b2},\\ {L(sp.sqrt((a1+b1)**2+(a2+b2)**2))}"])
    elif kind == 1:
        items.append([f"$\\vec a=({a1},{a2})$ と $\\vec b=(x,{b2})$ が垂直になる $x$", L(R(-a2 * b2, a1))])
    else:
        c1 = nz(-6, 6)
        items.append([f"$\\vec a=({a1},{a2},{c1}),\\ \\vec b=({b1},{b2},{c1+1})$ の内積", str(a1 * b1 + a2 * b2 + c1 * (c1 + 1))])
add(30, "ベクトル", items)

# ---------- 31 複素数平面 ----------
items = []
for z in [1 + I, 1 - I, sp.sqrt(3) + I, -1 + sp.sqrt(3) * I, 2 * I, -2, 1 + sp.sqrt(3) * I, -sp.sqrt(3) - I]:
    r = sp.Abs(z); th = sp.arg(z)
    th = th if th >= 0 else th + 2 * pi
    items.append([f"z={L(z)}\\ \\text{{を極形式で}}", f"{L(r)}\\left(\\cos {L(th)} + i\\sin {L(th)}\\right)"])
for z, m in [(1 + I, 4), (1 + I, 6), (sp.sqrt(3) + I, 6), (1 - I, 8), (-1 + sp.sqrt(3) * I, 3), (1 + sp.sqrt(3) * I, 5)]:
    items.append([f"({L(z)})^{{{m}}}", L(sp.expand(z ** m))])
add(31, "複素数平面", items)

# ---------- 32 極限 ----------
items = []
cands = [
    (3 * n ** 2 + n) / (n ** 2 - 4), (2 * n + 1) / (5 * n - 3), (n ** 2 + 1) / (n ** 3 + n), (4 * n ** 3 - n) / (2 * n ** 3 + 7),
    sp.sqrt(n ** 2 + 3 * n) - n, sp.sqrt(n ** 2 + 4 * n) - sp.sqrt(n ** 2 - n), (3 ** (n + 1) + 2 ** n) / (3 ** n - 2 ** n),
    (5 ** n - 3 ** n) / (5 ** n + 4 ** n), ((n + 1) / n) ** n, (1 + 2 / n) ** n,
]
for e in cands:
    items.append([f"\\displaystyle\\lim_{{n\\to\\infty}} {L(e)}", L(sp.limit(e, n, sp.oo))])
for e in [sp.sin(3 * x) / x, sp.sin(x) / (2 * x), (1 - sp.cos(x)) / x ** 2, sp.tan(x) / x, (sp.exp(x) - 1) / x, sp.log(1 + x) / x, (x ** 2 - 4) / (x - 2)]:
    pt = 2 if e == (x ** 2 - 4) / (x - 2) else 0
    items.append([f"\\displaystyle\\lim_{{x\\to {pt}}} {L(e)}", L(sp.limit(e, x, pt))])
for a, r in [(1, R(1, 2)), (3, R(1, 3)), (2, -R(1, 2)), (5, R(2, 5))]:
    items.append([f"初項 {a}、公比 ${L(r)}$ の無限等比級数の和", L(a / (1 - r))])
add(32, "極限", items)

# ---------- 33 微分(III) ----------
items = []
fs = [sp.sin(2 * x), sp.cos(x ** 2), sp.exp(3 * x), x * sp.exp(x), x ** 2 * sp.sin(x), sp.log(x ** 2 + 1), sp.log(sp.cos(x)),
      (x + 1) / (x - 1), x / (x ** 2 + 1), sp.sqrt(x ** 2 + 1), (2 * x - 1) ** 5, sp.exp(-x) * sp.cos(x), sp.tan(2 * x),
      x * sp.log(x), sp.sin(x) ** 3, 1 / sp.sqrt(x), sp.exp(x ** 2), sp.log(sp.Abs(x)), sp.sqrt(1 - x ** 2), x ** 3 * sp.exp(-x)]
for f in fs:
    d = sp.simplify(sp.diff(f, x))
    if d.is_rational_function(x):
        d = sp.factor(d)
    if f == sp.log(sp.Abs(x)):
        d = 1 / x
    items.append([f"y={L(f)}", f"y'={L(d)}"])
add(33, "微分法（数III）", items)

# ---------- 34 積分(III) ----------
items = []
ifs = [1 / x, sp.exp(2 * x), sp.sin(3 * x), sp.cos(x / 2), x * sp.exp(x), x * sp.sin(x), sp.log(x), x * sp.log(x), 2 * x / (x ** 2 + 1),
       sp.sin(x) ** 2, sp.cos(x) * sp.sin(x) ** 2, x * (x ** 2 + 1) ** 3, 1 / (x * (x + 1)), sp.exp(x) * sp.sin(x)]
for f in ifs:
    Fx = sp.integrate(f, x)
    Fx = sp.simplify(Fx) if f not in (sp.exp(x) * sp.sin(x),) else Fx
    # 教科書らしい形に直す（いずれも sympy の結果と定数差しかない）
    nice = {1 / x: "\\log|x|",
            x * (x ** 2 + 1) ** 3: "\\frac{(x^2+1)^4}{8}",
            1 / (x * (x + 1)): "\\log\\left|\\frac{x}{x+1}\\right|",
            2 * x / (x ** 2 + 1): "\\log(x^2+1)"}
    for g, s in nice.items():
        if f == g:
            assert sp.simplify(sp.diff(Fx, x) - f) == 0
    txt = nice.get(f, L(Fx))
    items.append([f"\\displaystyle\\int {L(f)}\\,dx", txt + "+C"])
dfs = [(sp.exp(x), 0, 1), (sp.sin(x), 0, pi), (sp.cos(x), 0, pi / 2), (1 / x, 1, sp.E), (x * sp.exp(x), 0, 1), (sp.log(x), 1, sp.E),
       (x * sp.cos(x), 0, pi / 2), (sp.sqrt(x), 0, 4)]
for f, a, b in dfs:
    items.append([f"\\displaystyle\\int_{{{L(a)}}}^{{{L(b)}}} {L(f)}\\,dx", L(sp.simplify(sp.integrate(f, (x, a, b))))])
add(34, "積分法（数III）", items)

json.dump(D, open(os.environ.get("OUT", "drills.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print({k: len(v["items"]) for k, v in D.items()}, sum(len(v["items"]) for v in D.values()))
