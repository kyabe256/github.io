"""第2章 2次関数（数学I）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に verify() がまとめて呼ぶ。"""
import math, random, re
from fractions import Fraction as Fr
from sympy import symbols, expand, Rational as R, sqrt, simplify, solve, real_roots, Poly, nsimplify

x, y, a, b, c, t, k = symbols("x y a b c t k", real=True)

# ------------------------------------------------------------ 図（SVG）
_FIGN = [0]


def _it(s):
    return re.sub(r"([a-z]+)", r'<tspan font-style="italic">\1</tspan>', s)


def _svg(xr, yr, W=200, H=150, curves=(), segs=(), pts=(), txt=(), xt=(), yt=(), O=True, xl="x", yl="y", Od=(-2, 11)):
    """xr, yr: 描画範囲。curves: (f, a, b[, 色, 線幅, 破線])。segs: ((x1,y1),(x2,y2)[, 色, 破線])。
    pts: (x, y, 'f'|'o')。txt: (x, y, 文字, dx, dy[, anchor])。xt/yt: (値, ラベル) 目盛り。"""
    x0, x1 = xr
    y0, y1 = yr
    Lp, Rp, Tp, Bp = 12, 12, 10, 12
    sx = (W - Lp - Rp) / (x1 - x0)
    sy = (H - Tp - Bp) / (y1 - y0)
    X = lambda u: Lp + (u - x0) * sx
    Y = lambda v: Tp + (y1 - v) * sy
    _FIGN[0] += 1
    cid = "c02clip%d" % _FIGN[0]
    o = ['<svg class="fig" width="%d" height="%d" viewBox="0 0 %d %d" font-family="Times New Roman,serif" font-size="11">' % (W, H, W, H),
         '<defs><clipPath id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath></defs>' % (cid, X(x0), Y(y1), X(x1) - X(x0), Y(y0) - Y(y1))]
    xa, ya = X(0), Y(0)
    if y0 <= 0 <= y1:
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#333" stroke-width="0.9"/>' % (3, ya, W - 4, ya))
        o.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#333"/>' % (W - 2, ya, W - 8, ya - 2.6, W - 8, ya + 2.6))
        o.append('<text x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (W - 6, ya + 12, _it(xl)))
    if x0 <= 0 <= x1:
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#333" stroke-width="0.9"/>' % (xa, H - 2, xa, 4))
        o.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#333"/>' % (xa, 2, xa - 2.6, 8, xa + 2.6, 8))
        o.append('<text x="%.1f" y="%.1f">%s</text>' % (xa + 5, 10, _it(yl)))
    if O and x0 <= 0 <= x1 and y0 <= 0 <= y1:
        o.append('<text x="%.1f" y="%.1f" text-anchor="end">O</text>' % (xa + Od[0], ya + Od[1]))
    for v, lab in xt:
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#333" stroke-width="0.8"/>' % (X(v), ya - 2.5, X(v), ya + 2.5))
        if lab:
            o.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10">%s</text>' % (X(v), ya + 12, _it(lab)))
    for v, lab in yt:
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#333" stroke-width="0.8"/>' % (xa - 2.5, Y(v), xa + 2.5, Y(v)))
        if lab:
            o.append('<text x="%.1f" y="%.1f" text-anchor="end" font-size="10">%s</text>' % (xa - 4, Y(v) + 3.5, _it(lab)))
    for s in segs:
        (p1, q1), (p2, q2) = s[0], s[1]
        col = s[2] if len(s) > 2 else "#777"
        dash = s[3] if len(s) > 3 else True
        o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="0.9"%s clip-path="url(#%s)"/>'
                 % (X(p1), Y(q1), X(p2), Y(q2), col, ' stroke-dasharray="3,2"' if dash else "", cid))
    for cv in curves:
        f, ta, tb = cv[0], cv[1], cv[2]
        col = cv[3] if len(cv) > 3 else "#16367a"
        lw = cv[4] if len(cv) > 4 else 1.5
        dash = cv[5] if len(cv) > 5 else False
        n = 160
        P = ["%.2f,%.2f" % (X(ta + (tb - ta) * i / n), Y(f(ta + (tb - ta) * i / n))) for i in range(n + 1)]
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f"%s clip-path="url(#%s)"/>'
                 % (" ".join(P), col, lw, ' stroke-dasharray="4,2"' if dash else "", cid))
    for p in pts:
        fill = "#fff" if (len(p) > 2 and p[2] == "o") else "#222"
        o.append('<circle cx="%.1f" cy="%.1f" r="2.1" fill="%s" stroke="#222" stroke-width="0.9"/>' % (X(p[0]), Y(p[1]), fill))
    for tx in txt:
        anc = tx[5] if len(tx) > 5 else "middle"
        o.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="10.5">%s</text>' % (X(tx[0]) + tx[3], Y(tx[1]) + tx[4], anc, _it(tx[2])))
    o.append("</svg>")
    return "".join(o)


def _cnt_roots(expr, var, lo=None, hi=None, lo_open=False, hi_open=False):
    """多項式 expr（有理係数）の相異なる実数解のうち、区間に入るものの個数（厳密）。"""
    rs = set(real_roots(Poly(expr, var)))
    n = 0
    for r in rs:
        if lo is not None and (r < lo or (lo_open and r == lo)):
            continue
        if hi is not None and (r > hi or (hi_open and r == hi)):
            continue
        n += 1
    return n


SEC = []

# ================================================================ 節1
SEC.append({"title": "2次関数のグラフと移動",
"base": r"""・$y=ax^2+bx+c=a\left(x+\dfrac{b}{2a}\right)^2-\dfrac{b^2-4ac}{4a}$ と平方完成すると，軸は直線 $x=-\dfrac{b}{2a}$，頂点は $\left(-\dfrac{b}{2a},\ -\dfrac{b^2-4ac}{4a}\right)$。$a>0$ なら下に凸，$a<0$ なら上に凸。<br>
・$x$ 軸方向に $p$，$y$ 軸方向に $q$ だけ平行移動：$x$ を $x-p$，$y$ を $y-q$ に置き換える（頂点の移動で考えてもよい）。<br>
・対称移動：$x$ 軸に関して $y\to-y$，$y$ 軸に関して $x\to-x$，原点に関して $x\to-x,\ y\to-y$，点 $(p,\,q)$ に関して $x\to2p-x,\ y\to2q-y$ と置き換える。""",
"items": [
 {"lv": 1, "title": "平方完成による軸と頂点",
  "q": r"次の2次関数のグラフの軸と頂点を求めよ。<br>(1) $y=2x^2-8x+5$　　(2) $y=-\dfrac12x^2-3x+1$",
  "hint": r"$x^2$ の係数で $x^2$ と $x$ の項をくくり，$(x-p)^2$ の形をつくる（平方完成）。$y=a(x-p)^2+q$ の軸は直線 $x=p$，頂点は点 $(p,\,q)$。",
  "sol": r"(1) $y=2(x^2-4x)+5=2\{(x-2)^2-4\}+5=2(x-2)^2-3$<br>よって　軸は直線 $\boldsymbol{x=2}$，頂点は点 $\boldsymbol{(2,\ -3)}$<br>"
         r"(2) $y=-\dfrac12(x^2+6x)+1=-\dfrac12\{(x+3)^2-9\}+1=-\dfrac12(x+3)^2+\dfrac{11}2$<br>よって　軸は直線 $\boldsymbol{x=-3}$，頂点は点 $\boldsymbol{\left(-3,\ \dfrac{11}2\right)}$",
  "note": r"頂点の $x$ 座標は $-\dfrac{b}{2a}$ でも求まる。(1) なら $-\dfrac{-8}{2\cdot2}=2$ で，$y$ 座標はこれを代入して $2\cdot4-16+5=-3$。平方完成の検算に使うとよい。",
  "ex": r"次の2次関数のグラフの軸と頂点を求めよ。<br>(1) $y=3x^2+12x+7$　　(2) $y=-2x^2+6x-1$",
  "exa": r"(1) 軸 $x=-2$，頂点 $(-2,\,-5)$　(2) 軸 $x=\dfrac32$，頂点 $\left(\dfrac32,\,\dfrac72\right)$"},
 {"lv": 1, "title": "平行移動した放物線の方程式",
  "q": r"放物線 $y=x^2-4x+1$ を，$x$ 軸方向に $3$，$y$ 軸方向に $-2$ だけ平行移動して得られる放物線の方程式を求めよ。",
  "hint": r"① 頂点がどこへ移るかを考える。② $x$ を $x-3$，$y$ を $y-(-2)=y+2$ に置き換える。のどちらでもよい。平行移動では $x^2$ の係数は変わらない。",
  "sol": r"$y=x^2-4x+1=(x-2)^2-3$ の頂点は $(2,\,-3)$。平行移動で頂点は $(2+3,\ -3-2)=(5,\,-5)$ に移り，$x^2$ の係数は $1$ のままだから<br>"
         r"$y=(x-5)^2-5$　すなわち　$\boldsymbol{y=x^2-10x+20}$",
  "note": r"置き換えによる方法：$y+2=(x-3)^2-4(x-3)+1=x^2-10x+22$ より $y=x^2-10x+20$。「点 $(x,\,y)$ が移動後の放物線上にある ⇔ 点 $(x-3,\,y+2)$ がもとの放物線上にある」から，$x\to x-3$，$y\to y+2$ と置き換える（符号に注意）。",
  "ex": r"放物線 $y=-2x^2+4x+3$ を，$x$ 軸方向に $-1$，$y$ 軸方向に $4$ だけ平行移動して得られる放物線の方程式を求めよ。",
  "exa": r"$y=-2x^2+9$"},
 {"lv": 2, "title": "対称移動（$x$ 軸・$y$ 軸・原点）",
  "q": r"放物線 $y=2x^2-4x+3$ を，次のものに関して対称移動して得られる放物線の方程式を求めよ。<br>(1) $x$ 軸　　(2) $y$ 軸　　(3) 原点",
  "hint": r"移動後の放物線上の点 $(x,\,y)$ に対し，それと対称な点がもとの放物線上にある。$x$ 軸なら $(x,\,-y)$，$y$ 軸なら $(-x,\,y)$，原点なら $(-x,\,-y)$ を代入する。",
  "sol": r"(1) $y$ を $-y$ に置き換えて　$-y=2x^2-4x+3$　よって　$\boldsymbol{y=-2x^2+4x-3}$<br>"
         r"(2) $x$ を $-x$ に置き換えて　$y=2(-x)^2-4(-x)+3$　よって　$\boldsymbol{y=2x^2+4x+3}$<br>"
         r"(3) $x$ を $-x$，$y$ を $-y$ に置き換えて　$-y=2x^2+4x+3$　よって　$\boldsymbol{y=-2x^2-4x-3}$",
  "note": r"頂点で確かめる：もとの頂点は $(1,\,1)$（$y=2(x-1)^2+1$）。(1) 頂点 $(1,\,-1)$・上に凸，(2) 頂点 $(-1,\,1)$・下に凸，(3) 頂点 $(-1,\,-1)$・上に凸。$x$ 軸・原点に関する対称移動では凸の向きが逆になり，$x^2$ の係数の符号が変わる。",
  "ex": r"放物線 $y=-x^2+6x-5$ を，(1) $x$ 軸　(2) $y$ 軸　(3) 原点 に関して対称移動して得られる放物線の方程式を求めよ。",
  "exa": r"(1) $y=x^2-6x+5$　(2) $y=-x^2-6x-5$　(3) $y=x^2+6x+5$"},
 {"lv": 2, "title": "グラフから係数の符号を読む",
  "q": _svg((-2.0, 3.6), (-2.6, 3.4), W=180, H=130,
             curves=[(lambda u: -(u - 1) ** 2 + 2.5, -2.0, 3.6)],
             xt=[(-1, "−1"), (1, "1")])
       + r"2次関数 $y=ax^2+bx+c$ のグラフが右の図のようになるとき，次の値の符号を答えよ。<br>(1) $a$　(2) $b$　(3) $c$<br>(4) $b^2-4ac$　(5) $a+b+c$　(6) $a-b+c$",
  "hint": r"$a$ は凸の向き，$b$ は軸 $x=-\dfrac{b}{2a}$ の位置と $a$ の符号，$c$ は $y$ 軸との交点，$b^2-4ac$ は $x$ 軸との共有点の個数，$a+b+c$ と $a-b+c$ は $x=1,\ -1$ のときの $y$ の値を見る。",
  "sol": r"(1) 上に凸だから　$\boldsymbol{a<0}$<br>"
         r"(2) 軸 $x=-\dfrac{b}{2a}$ が $x>0$ の部分にあるから $-\dfrac{b}{2a}>0$。$a<0$ より　$\boldsymbol{b>0}$<br>"
         r"(3) $y$ 軸との交点の $y$ 座標 $c$ が正だから　$\boldsymbol{c>0}$<br>"
         r"(4) $x$ 軸と異なる2点で交わるから　$\boldsymbol{b^2-4ac>0}$<br>"
         r"(5) $a+b+c$ は $x=1$ のときの $y$ の値で，図より正。$\boldsymbol{a+b+c>0}$<br>"
         r"(6) $a-b+c$ は $x=-1$ のときの $y$ の値で，図より負。$\boldsymbol{a-b+c<0}$",
  "note": r"(4) は「頂点の $y$ 座標 $-\dfrac{b^2-4ac}{4a}$ が正で $a<0$」からも分かる。$4a+2b+c$ なら $x=2$ のときの値，$4a-2b+c$ なら $x=-2$ のときの値を読めばよい。",
  "ex": r"2次関数 $y=ax^2+bx+c$ のグラフが下に凸で，頂点が第3象限にあり，$y$ 軸と $y>0$ の部分で交わる。$a,\ b,\ c,\ b^2-4ac$ の符号をそれぞれ答えよ。",
  "exa": r"$a>0,\ b>0,\ c>0,\ b^2-4ac>0$"},
 {"lv": 3, "title": "点に関する対称移動・移動を逆にたどる",
  "q": r"(1) 放物線 $y=x^2-2x+3$ を，点 $(2,\,1)$ に関して対称移動して得られる放物線の方程式を求めよ。<br>"
       r"(2) ある放物線を $x$ 軸方向に $2$，$y$ 軸方向に $-3$ だけ平行移動し，さらに原点に関して対称移動したところ，放物線 $y=-x^2+4x-1$ になった。もとの放物線の方程式を求めよ。",
  "hint": r"(1) 点 $(x,\,y)$ と点 $(2,\,1)$ に関して対称な点は，中点が $(2,\,1)$ となる点 $(4-x,\,2-y)$。(2) 移動を<b>逆の順に，逆向きに</b>たどる：原点に関する対称移動 → $x$ 軸方向に $-2$，$y$ 軸方向に $3$ の平行移動。",
  "sol": r"(1) 移動後の放物線上の点を $(x,\,y)$ とすると，点 $(4-x,\,2-y)$ がもとの放物線上にあるから<br>"
         r"$2-y=(4-x)^2-2(4-x)+3=x^2-6x+11$　よって　$\boldsymbol{y=-x^2+6x-9}$<br>"
         r"(2) $y=-x^2+4x-1$ を原点に関して対称移動すると　$-y=-x^2-4x-1$，すなわち $y=x^2+4x+1$<br>"
         r"これを $x$ 軸方向に $-2$，$y$ 軸方向に $3$ だけ平行移動すると<br>"
         r"$y-3=(x+2)^2+4(x+2)+1=x^2+8x+13$　よって　$\boldsymbol{y=x^2+8x+16}$",
  "note": r"(1) は頂点で確かめられる：$y=(x-1)^2+2$ の頂点 $(1,\,2)$ は点 $(2,\,1)$ に関して $(3,\,0)$ に移り，凸の向きが逆になるから $y=-(x-3)^2$。(2) も，答えの $y=(x+4)^2$ を問題文の順に移動すると $y=(x+2)^2-3$ → $y=-x^2+4x-1$ と戻ることを確かめておく。",
  "ex": r"(1) 放物線 $y=2x^2+4x$ を，点 $(-1,\,3)$ に関して対称移動して得られる放物線の方程式を求めよ。<br>"
        r"(2) ある放物線を $y$ 軸に関して対称移動し，さらに $x$ 軸方向に $-1$，$y$ 軸方向に $2$ だけ平行移動したところ，放物線 $y=x^2-4x+5$ になった。もとの放物線の方程式を求めよ。",
  "exa": r"(1) $y=-2x^2-4x+6$　(2) $y=x^2+6x+8$"},
]})


def _tr(f, p, q):          # x 方向 p, y 方向 q の平行移動（y=f(x) → y=f(x-p)+q）
    return expand(f.subs(x, x - p) + q)


def _pt(f, p, q):          # 点 (p,q) に関する対称移動
    return expand(2 * q - f.subs(x, 2 * p - x))


def _v1():
    assert expand(2 * (x - 2) ** 2 - 3) == 2 * x**2 - 8 * x + 5
    assert expand(-R(1, 2) * (x + 3) ** 2 + R(11, 2)) == -R(1, 2) * x**2 - 3 * x + 1
    assert expand(3 * (x + 2) ** 2 - 5) == 3 * x**2 + 12 * x + 7
    assert expand(-2 * (x - R(3, 2)) ** 2 + R(7, 2)) == -2 * x**2 + 6 * x - 1
    assert _tr(x**2 - 4 * x + 1, 3, -2) == x**2 - 10 * x + 20
    assert expand((x - 3) ** 2 - 4 * (x - 3) + 1) == x**2 - 10 * x + 22
    assert _tr(-2 * x**2 + 4 * x + 3, -1, 4) == -2 * x**2 + 9
    f = 2 * x**2 - 4 * x + 3
    assert expand(-f) == -2 * x**2 + 4 * x - 3 and expand(f.subs(x, -x)) == 2 * x**2 + 4 * x + 3
    assert expand(-f.subs(x, -x)) == -2 * x**2 - 4 * x - 3
    g = -x**2 + 6 * x - 5
    assert expand(-g) == x**2 - 6 * x + 5 and expand(g.subs(x, -x)) == -x**2 - 6 * x - 5 and expand(-g.subs(x, -x)) == x**2 + 6 * x + 5
    # 係数の符号：図の関数 y=-(x-1)^2+2.5 = -x^2+2x+1.5
    A, B, C = -1, 2, 1.5
    assert A < 0 and B > 0 and C > 0 and B * B - 4 * A * C > 0 and A + B + C > 0 and A - B + C < 0
    assert -(-1 - 1) ** 2 + 2.5 < 0 and -(0 - 1) ** 2 + 2.5 > 0       # x=-1 で負、根は -1 より右
    random.seed(2)
    for _ in range(2000):                     # 練習：a>0, 頂点 (p,q) が第3象限, c>0
        A = random.uniform(0.1, 5); p = -random.uniform(0.1, 5); q = -random.uniform(0.01, 5)
        C = A * p * p + q
        if C <= 0:
            continue
        B = -2 * A * p
        assert B > 0 and B * B - 4 * A * C > 0
    # 点対称・逆移動
    assert _pt(x**2 - 2 * x + 3, 2, 1) == -x**2 + 6 * x - 9
    assert expand((4 - x) ** 2 - 2 * (4 - x) + 3) == x**2 - 6 * x + 11
    orig = x**2 + 8 * x + 16
    h = _tr(orig, 2, -3)
    assert h == x**2 + 4 * x + 1 and expand(-h.subs(x, -x)) == -x**2 + 4 * x - 1
    assert expand((x + 2) ** 2 + 4 * (x + 2) + 1) == x**2 + 8 * x + 13
    assert _pt(2 * x**2 + 4 * x, -1, 3) == -2 * x**2 - 4 * x + 6
    o2 = x**2 + 6 * x + 8
    assert _tr(expand(o2.subs(x, -x)), -1, 2) == x**2 - 4 * x + 5


# ================================================================ 節2
SEC.append({"title": "2次関数の決定",
"base": r"""・頂点 $(p,\,q)$ や軸 $x=p$ が分かる　→　$y=a(x-p)^2+q$ とおく<br>
・$x$ 軸との交点 $(\alpha,\,0),\ (\beta,\,0)$ が分かる　→　$y=a(x-\alpha)(x-\beta)$ とおく<br>
・3点を通る　→　$y=ax^2+bx+c$ とおいて連立3元1次方程式を解く<br>
・$x$ 軸に接する　→　$y=a(x-p)^2$。直線に接する　→　連立して得られる2次方程式が重解をもつ（判別式 $=0$）""",
"items": [
 {"lv": 1, "title": "頂点・軸が分かっているときの決定",
  "q": r"次の条件を満たす放物線をグラフとする2次関数を求めよ。<br>(1) 頂点が点 $(1,\,-2)$ で，点 $(3,\,6)$ を通る。<br>(2) 軸が直線 $x=-1$ で，2点 $(0,\,1),\ (1,\,-5)$ を通る。",
  "hint": r"頂点や軸が与えられたら $y=a(x-p)^2+q$ の形でおく。(1) は未知数が $a$ だけ，(2) は $a,\ q$ の2つ。",
  "sol": r"(1) 頂点が $(1,\,-2)$ だから $y=a(x-1)^2-2$ とおける。点 $(3,\,6)$ を通るから $6=4a-2$，$a=2$。<br>よって　$\boldsymbol{y=2(x-1)^2-2}$（$y=2x^2-4x$）<br>"
         r"(2) 軸が $x=-1$ だから $y=a(x+1)^2+q$ とおける。2点を通るから $a+q=1,\ 4a+q=-5$。これを解いて $a=-2,\ q=3$。<br>よって　$\boldsymbol{y=-2(x+1)^2+3}$（$y=-2x^2-4x+1$）",
  "ex": r"次の条件を満たす2次関数を求めよ。<br>(1) グラフの頂点が点 $(-2,\,5)$ で，点 $(0,\,1)$ を通る。<br>(2) グラフの軸が直線 $x=2$ で，2点 $(1,\,0),\ (4,\,9)$ を通る。",
  "exa": r"(1) $y=-(x+2)^2+5$　(2) $y=3(x-2)^2-3$"},
 {"lv": 1, "title": "$x$ 軸との交点が分かっているときの決定",
  "q": r"グラフが $x$ 軸と2点 $(-1,\,0),\ (3,\,0)$ で交わり，点 $(1,\,-8)$ を通る2次関数を求めよ。",
  "hint": r"$x$ 軸との交点の $x$ 座標が $-1,\ 3$ だから $y=a(x+1)(x-3)$ とおける（因数分解形）。",
  "sol": r"$y=a(x+1)(x-3)$ とおく。点 $(1,\,-8)$ を通るから $-8=a\cdot2\cdot(-2)$，$a=2$。<br>よって　$\boldsymbol{y=2(x+1)(x-3)}$（$y=2x^2-4x-6$）",
  "note": r"一般形 $y=ax^2+bx+c$ とおいて3点の連立方程式を解いても同じ結果になるが，因数分解形のほうが計算が速い。",
  "ex": r"グラフが $x$ 軸と2点 $(-2,\,0),\ (4,\,0)$ で交わり，点 $(2,\,16)$ を通る2次関数を求めよ。",
  "exa": r"$y=-2(x+2)(x-4)$（$y=-2x^2+4x+16$）"},
 {"lv": 2, "title": "3点を通る放物線",
  "q": r"3点 $(-1,\,6),\ (1,\,0),\ (2,\,3)$ を通る放物線をグラフとする2次関数を求めよ。",
  "hint": r"$y=ax^2+bx+c$ とおき，3点の座標を代入して連立3元1次方程式をつくる。$x=\pm1$ の2式は辺々引くと $b$ だけが残る。",
  "sol": r"$y=ax^2+bx+c$ とおくと<br>$a-b+c=6$ ……①　$a+b+c=0$ ……②　$4a+2b+c=3$ ……③<br>"
         r"②$-$① より $2b=-6$，$b=-3$。② に代入して $a+c=3$，③ に代入して $4a+c=9$。<br>これらから $a=2,\ c=1$。よって　$\boldsymbol{y=2x^2-3x+1}$",
  "note": r"文字を1つずつ消去していくのが基本。どの2式を組み合わせると文字が消えやすいかを先に見る。",
  "ex": r"3点 $(0,\,-3),\ (1,\,0),\ (-2,\,-3)$ を通る放物線をグラフとする2次関数を求めよ。",
  "exa": r"$y=x^2+2x-3$"},
 {"lv": 3, "title": "$x$ 軸に接し2点を通る放物線",
  "q": r"グラフが $x$ 軸に接し，2点 $(0,\,4),\ (3,\,1)$ を通る2次関数を求めよ。",
  "hint": r"$x$ 軸に接する ⇔ 頂点が $x$ 軸上にある，だから $y=a(x-p)^2$ とおける。未知数 $a,\ p$ の連立方程式で，$a$ を消去すると $p$ の2次方程式になる。",
  "sol": r"$y=a(x-p)^2\ (a\neq0)$ とおく。2点を通るから<br>$ap^2=4$ ……①　$a(3-p)^2=1$ ……②<br>"
         r"① より $p\neq0$ で $a=\dfrac4{p^2}$。② に代入して $4(3-p)^2=p^2$<br>"
         r"$3p^2-24p+36=0$，$p^2-8p+12=0$，$(p-2)(p-6)=0$　よって $p=2,\ 6$<br>"
         r"$p=2$ のとき $a=1$，$p=6$ のとき $a=\dfrac19$。<br>よって　$\boldsymbol{y=(x-2)^2,\quad y=\dfrac19(x-6)^2}$",
  "note": r"答えが2つあることに注意。$4(3-p)^2=p^2$ を $2(3-p)=\pm p$ と開いてもよい。「直線 $y=k$ に接する」なら $y=a(x-p)^2+k$ とおけばよい。",
  "ex": r"グラフが $x$ 軸に接し，2点 $(1,\,2),\ (-1,\,8)$ を通る2次関数を求めよ。",
  "exa": r"$y=\dfrac12(x-3)^2,\quad y=\dfrac92\left(x-\dfrac13\right)^2$"},
 {"lv": 3, "title": "直線に接し，$x$ 軸から切り取る線分の長さが与えられた放物線",
  "q": r"放物線 $y=x^2+bx+c$ が直線 $y=2x-1$ に接し，かつ $x$ 軸から切り取る線分の長さが $4$ であるとき，定数 $b,\ c$ の値を求めよ。",
  "hint": r"$x$ 軸との交点の $x$ 座標は $x^2+bx+c=0$ の2解 $\dfrac{-b\pm\sqrt{b^2-4c}}2$ だから，切り取る長さは $\sqrt{b^2-4c}$。接する条件は，連立した2次方程式の判別式 $=0$。",
  "sol": r"$x^2+bx+c=0$ の2解は $\dfrac{-b\pm\sqrt{b^2-4c}}2$ で，その差が線分の長さだから<br>"
         r"$\sqrt{b^2-4c}=4$，すなわち $b^2-4c=16$ ……①<br>"
         r"また，$x^2+bx+c=2x-1$ すなわち $x^2+(b-2)x+c+1=0$ が重解をもつから<br>"
         r"$(b-2)^2-4(c+1)=0$，すなわち $b^2-4b-4c=0$ ……②<br>"
         r"①$-$② より $4b=16$，$b=4$。① より $c=0$。<br>よって　$\boldsymbol{b=4,\ c=0}$",
  "note": r"確かめ：$y=x^2+4x$ は $x$ 軸と $x=0,\ -4$ で交わり（長さ $4$），$x^2+4x-(2x-1)=(x+1)^2$ だから直線と点 $(-1,\,-3)$ で接する。",
  "ex": r"放物線 $y=x^2+bx+c$ が直線 $y=4x-3$ に接し，かつ $x$ 軸から切り取る線分の長さが $2$ であるとき，定数 $b,\ c$ の値を求めよ。",
  "exa": r"$b=1,\ c=-\dfrac34$"},
 {"lv": 5, "title": "3点での値による2次関数の評価（補間公式）",
  "q": r"2次関数 $f(x)=ax^2+bx+c$ が $|f(-1)|\leqq1,\ |f(0)|\leqq1,\ |f(1)|\leqq1$ を満たしている。<br>"
       r"(1) $-1\leqq x\leqq1$ のとき $|f(x)|\leqq\dfrac54$ であることを証明せよ。<br>(2) $|a|+|b|+|c|$ の最大値を求めよ。",
  "hint": r"条件は関数の値 $f(-1),\ f(0),\ f(1)$ で与えられている。そこで $p=f(-1),\ q=f(0),\ r=f(1)$ を新しい変数にとり，$a,\ b,\ c$ と $f(x)$ を $p,\ q,\ r$ で表す。$f(x)$ を $p,\ q,\ r$ の1次式と見ると，その係数の符号は $x$ の範囲で決まる。",
  "sol": r"$p=f(-1),\ q=f(0),\ r=f(1)$ とおくと $p=a-b+c,\ q=c,\ r=a+b+c$ だから<br>"
         r"$a=\dfrac{p+r}2-q,\quad b=\dfrac{r-p}2,\quad c=q$ ……①<br>"
         r"これを $f(x)=ax^2+bx+c$ に代入し，$p,\ q,\ r$ について整理すると<br>"
         r"$f(x)=\dfrac{x(x-1)}2\,p+(1-x^2)\,q+\dfrac{x(x+1)}2\,r$ ……②<br>"
         r"(1) $0\leqq x\leqq1$ のとき $\dfrac{x(x-1)}2\leqq0,\ 1-x^2\geqq0,\ \dfrac{x(x+1)}2\geqq0$。$|p|,\ |q|,\ |r|\leqq1$ だから，② より<br>"
         r"$|f(x)|\leqq\dfrac{x(1-x)}2+(1-x^2)+\dfrac{x(x+1)}2=-x^2+x+1=\dfrac54-\left(x-\dfrac12\right)^2\leqq\dfrac54$<br>"
         r"$-1\leqq x\leqq0$ のとき $\dfrac{x(x-1)}2\geqq0,\ 1-x^2\geqq0,\ \dfrac{x(x+1)}2\leqq0$ だから，同様に<br>"
         r"$|f(x)|\leqq\dfrac{x(x-1)}2+(1-x^2)-\dfrac{x(x+1)}2=-x^2-x+1=\dfrac54-\left(x+\dfrac12\right)^2\leqq\dfrac54$<br>"
         r"以上より，$-1\leqq x\leqq1$ のとき $\boldsymbol{|f(x)|\leqq\dfrac54}$ である。（終）<br>"
         r"(2) $|a|+|b|+|c|$ は，符号を選んだ $\pm a\pm b\pm c$（8通り）の最大値に等しい。① より<br>"
         r"$a+b+c=r,\quad a+b-c=r-2q,\quad a-b+c=p,\quad a-b-c=p-2q$<br>"
         r"で，残りの4通りはこれらの $-1$ 倍である。$|p|,\ |q|,\ |r|\leqq1$ より，これらの絶対値はすべて $3$ 以下だから $|a|+|b|+|c|\leqq3$。<br>"
         r"一方，$f(x)=2x^2-1$ は $f(-1)=1,\ f(0)=-1,\ f(1)=1$ で条件を満たし，$|a|+|b|+|c|=2+0+1=3$。<br>"
         r"よって，最大値は　$\boldsymbol{3}$",
  "note": r"(1) の等号は $p=-1,\ q=r=1$，すなわち $f(x)=-x^2+x+1$ の $x=\dfrac12$ で成り立つから，$\dfrac54$ はこれ以上小さくできない。② は「3点での値から2次関数を復元する式」（ラグランジュの補間公式）で，$x=-1,\ 0,\ 1$ を代入すると確かに $p,\ q,\ r$ になる。条件が関数の値で与えられた係数の評価では，まずこの書き換えを考える。",
  "ex": r"2次関数 $f(x)=ax^2+bx+c$ が $|f(0)|\leqq1,\ \left|f\left(\dfrac12\right)\right|\leqq1,\ |f(1)|\leqq1$ を満たすとき，$|a|+|b|+|c|$ の最大値を求めよ。",
  "exa": r"$17$（$f(x)=8x^2-8x+1$ のとき。$a=2f(0)-4f\left(\frac12\right)+2f(1)$，$b=-3f(0)+4f\left(\frac12\right)-f(1)$，$c=f(0)$ と表して評価する）"},
]})


def _v2():
    def ok(f, P):
        return all(f.subs(x, u) == v for u, v in P)
    f = 2 * (x - 1) ** 2 - 2; assert ok(f, [(3, 6), (1, -2)]) and expand(f) == 2 * x**2 - 4 * x
    f = -2 * (x + 1) ** 2 + 3; assert ok(f, [(0, 1), (1, -5)]) and expand(f) == -2 * x**2 - 4 * x + 1
    assert ok(-(x + 2) ** 2 + 5, [(0, 1), (-2, 5)]) and ok(3 * (x - 2) ** 2 - 3, [(1, 0), (4, 9)])
    assert ok(2 * (x + 1) * (x - 3), [(-1, 0), (3, 0), (1, -8)]) and expand(2 * (x + 1) * (x - 3)) == 2 * x**2 - 4 * x - 6
    assert ok(-2 * (x + 2) * (x - 4), [(-2, 0), (4, 0), (2, 16)]) and expand(-2 * (x + 2) * (x - 4)) == -2 * x**2 + 4 * x + 16
    assert solve([a - b + c - 6, a + b + c, 4 * a + 2 * b + c - 3], [a, b, c]) == {a: 2, b: -3, c: 1}
    assert solve([c + 3, a + b + c, 4 * a - 2 * b + c + 3], [a, b, c]) == {a: 1, b: 2, c: -3}
    p = symbols("p")
    assert set(solve(4 * (3 - p) ** 2 - p**2, p)) == {2, 6} and expand(4 * (3 - p) ** 2 - p**2) == 3 * p**2 - 24 * p + 36
    for f in [(x - 2) ** 2, R(1, 9) * (x - 6) ** 2]:
        assert ok(f, [(0, 4), (3, 1)])
    sols = solve([a * (1 - p) ** 2 - 2, a * (-1 - p) ** 2 - 8], [a, p], dict=True)
    assert {(s[a], s[p]) for s in sols} == {(R(1, 2), 3), (R(9, 2), R(1, 3))}
    # 接する・切り取る長さ
    assert solve([b**2 - 4 * c - 16, (b - 2) ** 2 - 4 * (c + 1)], [b, c], dict=True) == [{b: 4, c: 0}]
    assert expand((b - 2) ** 2 - 4 * (c + 1)) == b**2 - 4 * b - 4 * c
    assert solve([b**2 - 4 * c - 4, (b - 4) ** 2 - 4 * (c + 3)], [b, c], dict=True) == [{b: 1, c: R(-3, 4)}]
    assert expand(x**2 + x - R(3, 4) - (4 * x - 3)) == expand((x - R(3, 2)) ** 2)
    # 補間公式
    P, Q, Rr = symbols("P Q Rr")
    A = (P + Rr) / 2 - Q; B = (Rr - P) / 2; C = Q
    assert expand(A * x**2 + B * x + C - (x * (x - 1) / 2 * P + (1 - x**2) * Q + x * (x + 1) / 2 * Rr)) == 0
    assert expand(A - B + C - P) == 0 and expand(A + B + C - Rr) == 0
    random.seed(3)
    best = 0
    for _ in range(4000):
        pv, qv, rv = [random.choice([-1, 1, random.uniform(-1, 1)]) for _ in range(3)]
        Av, Bv, Cv = (pv + rv) / 2 - qv, (rv - pv) / 2, qv
        m = max(abs(Av * u * u + Bv * u + Cv) for u in [-1 + i / 200 for i in range(401)])
        assert m <= 1.25 + 1e-12
        best = max(best, abs(Av) + abs(Bv) + abs(Cv))
    assert abs(best - 3) < 1e-12
    assert abs(max(abs(-u * u + u + 1) for u in [i / 1000 for i in range(1001)]) - 1.25) < 1e-12
    # 練習：f(0), f(1/2), f(1) から |a|+|b|+|c| の最大は 17
    import itertools
    mx = max(abs(2 * f0 - 4 * fh + 2 * f1) + abs(-3 * f0 + 4 * fh - f1) + abs(f0)
             for f0, fh, f1 in itertools.product([-1, 1], repeat=3))
    assert mx == 17
    g = 8 * x**2 - 8 * x + 1
    assert [g.subs(x, u) for u in [0, R(1, 2), 1]] == [1, -1, 1]
    f0, fh, f1 = symbols("f0 fh f1")
    Ag, Bg, Cg = 2 * f0 - 4 * fh + 2 * f1, -3 * f0 + 4 * fh - f1, f0
    assert expand(Cg - f0) == 0 and expand(Ag / 4 + Bg / 2 + Cg - fh) == 0 and expand(Ag + Bg + Cg - f1) == 0


# ================================================================ 節3
SEC.append({"title": "2次関数の最大・最小",
"base": r"""・$f(x)=a(x-p)^2+q\ (a>0)$ の区間 $\alpha\leqq x\leqq\beta$ における最小値：軸 $x=p$ が区間内なら $f(p)=q$，区間の左外なら $f(\alpha)$，右外なら $f(\beta)$。<br>
・最大値：軸から遠いほうの端でとる。区間の中央 $\dfrac{\alpha+\beta}2$ と軸 $p$ の大小で場合を分ける（$a<0$ なら最大と最小の考え方が入れ替わる）。<br>
・置き換え $t=g(x)$ をしたら，$t$ のとり得る値の範囲を必ず求める。<br>
・2変数：条件式で1文字を消去する（残る文字の範囲に注意），または一方を固定して他方を動かす（予選決勝法）。""",
"items": [
 {"lv": 1, "title": "区間における最大・最小",
  "q": r"次の関数の最大値と最小値を求めよ。<br>(1) $y=x^2-4x+1\ \ (0\leqq x\leqq5)$　　(2) $y=-2x^2+8x-3\ \ (0\leqq x\leqq1)$",
  "hint": r"平方完成して頂点を求め，グラフをかいて，区間の両端と頂点の $y$ 座標を比べる。軸が区間内にあるかどうかが要点。",
  "sol": r"(1) $y=(x-2)^2-3$。軸 $x=2$ は区間内にある。$x=0$ で $y=1$，$x=5$ で $y=6$。<br>"
         r"よって　$\boldsymbol{x=5}$ で最大値 $\boldsymbol{6}$，$\boldsymbol{x=2}$ で最小値 $\boldsymbol{-3}$<br>"
         r"(2) $y=-2(x-2)^2+5$。軸 $x=2$ は区間の右外にあり，$0\leqq x\leqq1$ では $x$ が増えると $y$ も増える。$x=0$ で $y=-3$，$x=1$ で $y=3$。<br>"
         r"よって　$\boldsymbol{x=1}$ で最大値 $\boldsymbol{3}$，$\boldsymbol{x=0}$ で最小値 $\boldsymbol{-3}$",
  "note": r"(2) で頂点の $y$ 座標 $5$ を最大値としてしまう誤りが多い。頂点が区間に入っているかを必ず確かめる。",
  "ex": r"次の関数の最大値と最小値を求めよ。<br>(1) $y=2x^2+4x-1\ \ (-3\leqq x\leqq1)$　　(2) $y=-x^2+2x+2\ \ (2\leqq x\leqq4)$",
  "exa": r"(1) $x=-3,\ 1$ で最大値 $5$，$x=-1$ で最小値 $-3$　(2) $x=2$ で最大値 $2$，$x=4$ で最小値 $-6$"},
 {"lv": 2, "title": "最大値・最小値から係数を決める",
  "q": r"関数 $y=ax^2-4ax+b\ \ (1\leqq x\leqq4)$ の最大値が $6$，最小値が $-2$ であるとき，定数 $a,\ b$ の値を求めよ。ただし $a\neq0$ とする。",
  "hint": r"$y=a(x-2)^2-4a+b$ で軸は $x=2$（区間内）。$a>0$ と $a<0$ で凸の向きが変わり，最大・最小をとる場所が入れ替わる。区間の端では $x=4$ のほうが軸から遠い。",
  "sol": r"$y=a(x-2)^2-4a+b$。軸 $x=2$ は区間内にあり，端 $x=4$ は $x=1$ より軸から遠い。<br>"
         r"$x=2$ で $y=-4a+b$，$x=4$ で $y=b$，$x=1$ で $y=-3a+b$。<br>"
         r"[1] $a>0$ のとき　最大値は $b=6$，最小値は $-4a+b=-2$。よって $a=2,\ b=6$（$a>0$ を満たす）。<br>"
         r"[2] $a<0$ のとき　最大値は $-4a+b=6$，最小値は $b=-2$。よって $a=-2,\ b=-2$（$a<0$ を満たす）。<br>"
         r"以上より　$\boldsymbol{(a,\ b)=(2,\ 6),\ (-2,\ -2)}$",
  "note": r"求めた $a$ が場合分けの条件（$a>0$ など）を満たすかを必ず確かめる。",
  "ex": r"関数 $y=ax^2+2ax+b\ \ (-2\leqq x\leqq1)$ の最大値が $5$，最小値が $1$ であるとき，定数 $a,\ b$ の値を求めよ。ただし $a\neq0$ とする。",
  "exa": r"$(a,\ b)=(1,\ 2),\ (-1,\ 4)$"},
 {"lv": 2, "title": "置き換えによる最大・最小（4次関数）",
  "q": r"関数 $y=(x^2-2x)^2+4(x^2-2x)+1\ \ (-1\leqq x\leqq3)$ の最大値と最小値を求めよ。",
  "hint": r"$t=x^2-2x$ とおくと $y$ は $t$ の2次関数。まず，$-1\leqq x\leqq3$ のときの $t$ の範囲を求める。",
  "sol": r"$t=x^2-2x=(x-1)^2-1$ とおく。$-1\leqq x\leqq3$ のとき，$t$ は $x=1$ で最小値 $-1$，$x=-1,\ 3$ で最大値 $3$ をとるから $-1\leqq t\leqq3$。<br>"
         r"$y=t^2+4t+1=(t+2)^2-3$ は $-1\leqq t\leqq3$ で増加するから，$t=3$ のとき最大値 $9+12+1=22$，$t=-1$ のとき最小値 $1-4+1=-2$。<br>"
         r"$t=3$ となるのは $x=-1,\ 3$，$t=-1$ となるのは $x=1$ のとき。<br>"
         r"よって　$\boldsymbol{x=-1,\ 3}$ で最大値 $\boldsymbol{22}$，$\boldsymbol{x=1}$ で最小値 $\boldsymbol{-2}$",
  "note": r"$t$ の範囲を考えずに $(t+2)^2-3$ の頂点から「最小値 $-3$」とするのは誤り（$t=-2$ となる $x$ は存在しない）。最後に，最大・最小をとる $x$ の値に戻すこと。",
  "ex": r"関数 $y=(x^2+2x)^2-2(x^2+2x)-1$ の最小値と，そのときの $x$ の値を求めよ。",
  "exa": r"$x=-1\pm\sqrt2$ のとき最小値 $-2$"},
 {"lv": 2, "title": "条件つきの最大・最小（1次の条件式）",
  "q": r"$x\geqq0,\ y\geqq0,\ x+2y=3$ のとき，$x^2+y^2$ の最大値と最小値を求めよ。",
  "hint": r"条件式から $x=3-2y$ として $x$ を消去する。$x\geqq0$ から $y$ の範囲も制限されることに注意。",
  "sol": r"$x=3-2y$。$x\geqq0$ より $y\leqq\dfrac32$，これと $y\geqq0$ から $0\leqq y\leqq\dfrac32$。<br>"
         r"$x^2+y^2=(3-2y)^2+y^2=5y^2-12y+9=5\left(y-\dfrac65\right)^2+\dfrac95$<br>"
         r"$0\leqq y\leqq\dfrac32$ において，$y=\dfrac65$ で最小値 $\dfrac95$。最大値は軸から遠い端 $y=0$ でとり $9$（$y=\dfrac32$ では $\dfrac94$）。<br>"
         r"よって　$\boldsymbol{x=3,\ y=0}$ で最大値 $\boldsymbol{9}$，$\boldsymbol{x=\dfrac35,\ y=\dfrac65}$ で最小値 $\boldsymbol{\dfrac95}$",
  "note": r"図形的には，線分 $x+2y=3\ (x\geqq0,\ y\geqq0)$ 上の点と原点との距離の2乗。最小は原点から直線に下ろした垂線の足 $\left(\dfrac35,\,\dfrac65\right)$ のとき。",
  "ex": r"$x\geqq0,\ y\geqq0,\ 2x+y=4$ のとき，$2x^2+y^2$ の最大値と最小値を求めよ。",
  "exa": r"$x=0,\ y=4$ で最大値 $16$，$x=y=\dfrac43$ で最小値 $\dfrac{16}3$"},
 {"lv": 2, "title": "2変数関数の最小（平方完成を2回）",
  "q": r"$x,\ y$ が実数全体を動くとき，$x^2-2xy+2y^2-2x-4y+12$ の最小値と，そのときの $x,\ y$ の値を求めよ。",
  "hint": r"まず $y$ を定数とみて $x$ について平方完成し，残った $y$ の式をさらに平方完成する。（ ）$^2+$（ ）$^2+$ 定数 の形にする。",
  "sol": r"$x$ について整理して平方完成すると<br>"
         r"$x^2-2(y+1)x+2y^2-4y+12=\{x-(y+1)\}^2-(y+1)^2+2y^2-4y+12$<br>"
         r"$=(x-y-1)^2+y^2-6y+11=(x-y-1)^2+(y-3)^2+2$<br>"
         r"$(x-y-1)^2\geqq0,\ (y-3)^2\geqq0$ で，等号は $x-y-1=0,\ y-3=0$，すなわち $x=4,\ y=3$ のとき同時に成り立つ。<br>"
         r"よって　$\boldsymbol{x=4,\ y=3}$ のとき最小値 $\boldsymbol{2}$",
  "note": r"2つの平方が<b>同時に</b> $0$ になれることの確認が大切。$x,\ y$ に範囲の制限がつくと同時に $0$ にできないことがあり，そのときは予選決勝法（この節の後の例題）で考える。",
  "ex": r"$x,\ y$ が実数全体を動くとき，$x^2+2xy+3y^2+4x+8y+9$ の最小値と，そのときの $x,\ y$ の値を求めよ。",
  "exa": r"$x=-1,\ y=-1$ のとき最小値 $3$"},
 {"lv": 3, "title": "軸が動く場合の最大・最小",
  "q": r"$a$ を定数とする。関数 $f(x)=x^2-2ax+3\ \ (0\leqq x\leqq2)$ について，次のものを求めよ。<br>(1) 最小値 $m(a)$　　(2) 最大値 $M(a)$",
  "hint": r"$f(x)=(x-a)^2-a^2+3$ で，軸 $x=a$ が動く。最小値は「軸が区間の左外・区間内・右外」の3通り，最大値は「軸が区間の中央 $x=1$ より左か右か」の2通りに分ける。",
  "sol": r"$f(x)=(x-a)^2-a^2+3$，軸は $x=a$。$f(0)=3,\ f(2)=7-4a$。<br>"
         r"(1) [1] $a<0$ のとき　区間で増加するから $m(a)=f(0)=3$<br>"
         r"[2] $0\leqq a\leqq2$ のとき　$m(a)=f(a)=-a^2+3$<br>"
         r"[3] $a>2$ のとき　区間で減少するから $m(a)=f(2)=7-4a$<br>"
         r"(2) 区間の中央は $x=1$ で，軸から遠い端で最大となる。<br>"
         r"[1] $a<1$ のとき　$M(a)=f(2)=7-4a$　[2] $a=1$ のとき　$M(a)=f(0)=f(2)=3$　[3] $a>1$ のとき　$M(a)=f(0)=3$<br>"
         r"よって<br>(1) $a<0$ のとき $\boldsymbol{m(a)=3}$，$0\leqq a\leqq2$ のとき $\boldsymbol{m(a)=-a^2+3}$，$a>2$ のとき $\boldsymbol{m(a)=7-4a}$<br>"
         r"(2) $a<1$ のとき $\boldsymbol{M(a)=7-4a}$，$a\geqq1$ のとき $\boldsymbol{M(a)=3}$",
  "note": r"最小値と最大値で場合分けの境目が違う（最小値は $a=0,\ 2$，最大値は $a=1$）。$a=1$ では $x=0,\ 2$ の両方で最大となり，$7-4a$ と $3$ が一致するので，どちらの範囲に含めてもよい。",
  "ex": r"$a$ を定数とする。関数 $f(x)=x^2-4ax+1\ \ (0\leqq x\leqq1)$ の最小値 $m(a)$ と最大値 $M(a)$ を求めよ。",
  "exa": r"$m(a)$：$a<0$ のとき $1$，$0\leqq a\leqq\dfrac12$ のとき $1-4a^2$，$a>\dfrac12$ のとき $2-4a$。$M(a)$：$a<\dfrac14$ のとき $2-4a$，$a\geqq\dfrac14$ のとき $1$"},
 {"lv": 3, "title": "定義域が動く場合の最大・最小",
  "q": r"$a$ を定数とする。関数 $f(x)=x^2-4x+5\ \ (a\leqq x\leqq a+2)$ について，次のものを求めよ。<br>(1) 最小値 $m(a)$　　(2) 最大値 $M(a)$",
  "hint": r"今度はグラフ（軸 $x=2$）が固定で，幅 $2$ の区間が動く。区間を左から右へ動かしながら軸との位置関係で場合を分ける。最大値は区間の中央 $x=a+1$ と軸の大小で分ける。",
  "sol": r"$f(x)=(x-2)^2+1$，軸は $x=2$。$f(a)=a^2-4a+5,\ f(a+2)=a^2+1$。<br>"
         r"(1) [1] $a+2<2$ すなわち $a<0$ のとき　区間で減少するから $m(a)=f(a+2)=a^2+1$<br>"
         r"[2] $a\leqq2\leqq a+2$ すなわち $0\leqq a\leqq2$ のとき　$m(a)=f(2)=1$<br>"
         r"[3] $a>2$ のとき　区間で増加するから $m(a)=f(a)=a^2-4a+5$<br>"
         r"(2) 区間の中央は $x=a+1$。<br>"
         r"[1] $a+1<2$ すなわち $a<1$ のとき　左端が軸から遠いから $M(a)=f(a)=a^2-4a+5$<br>"
         r"[2] $a\geqq1$ のとき　右端が軸から遠い（$a=1$ では両端で等しい）から $M(a)=f(a+2)=a^2+1$<br>"
         r"よって<br>(1) $a<0$ のとき $\boldsymbol{m(a)=a^2+1}$，$0\leqq a\leqq2$ のとき $\boldsymbol{m(a)=1}$，$a>2$ のとき $\boldsymbol{m(a)=a^2-4a+5}$<br>"
         r"(2) $a<1$ のとき $\boldsymbol{M(a)=a^2-4a+5}$，$a\geqq1$ のとき $\boldsymbol{M(a)=a^2+1}$",
  "note": r"軸が動く場合も区間が動く場合も，「軸と区間の相対的な位置」で分けるという考え方は同じ。境目（$a=0,\ 1,\ 2$）で隣り合う式の値が一致することを確かめると検算になる。",
  "ex": r"$a$ を定数とする。関数 $f(x)=-x^2+2x+3\ \ (a\leqq x\leqq a+1)$ の最大値 $M(a)$ を求めよ。",
  "exa": r"$a<0$ のとき $M(a)=-a^2+4$，$0\leqq a\leqq1$ のとき $M(a)=4$，$a>1$ のとき $M(a)=-a^2+2a+3$"},
 {"lv": 3, "title": "条件つきの最大・最小（2次の条件式と変域）",
  "q": r"実数 $x,\ y$ が $x^2+2y^2=4$ を満たすとき，$x^2+4y$ の最大値と最小値を求めよ。また，そのときの $x,\ y$ の値を求めよ。",
  "hint": r"$x^2=4-2y^2$ を代入すると $y$ だけの2次関数になる。ただし $x$ は実数だから $x^2\geqq0$，これが $y$ の範囲を制限する。",
  "sol": r"$x^2=4-2y^2$ ……①。$x^2\geqq0$ より $4-2y^2\geqq0$，すなわち $-\sqrt2\leqq y\leqq\sqrt2$。<br>"
         r"$x^2+4y=4-2y^2+4y=-2(y-1)^2+6$<br>"
         r"$-\sqrt2\leqq y\leqq\sqrt2$ において，$y=1$ で最大値 $6$。最小値は軸から遠い端 $y=-\sqrt2$ でとり，$-2(-\sqrt2-1)^2+6=-4\sqrt2$。<br>"
         r"① より，$y=1$ のとき $x^2=2$ で $x=\pm\sqrt2$，$y=-\sqrt2$ のとき $x=0$。<br>"
         r"よって　$\boldsymbol{x=\pm\sqrt2,\ y=1}$ のとき最大値 $\boldsymbol{6}$，$\boldsymbol{x=0,\ y=-\sqrt2}$ のとき最小値 $\boldsymbol{-4\sqrt2}$",
  "note": r"$y$ の範囲を考え忘れると「最小値はない」と誤る。消去した文字（ここでは $x$）の実数条件が，残った文字の範囲になる。",
  "ex": r"実数 $x,\ y$ が $x^2+3y^2=9$ を満たすとき，$x^2+6y$ の最大値と最小値を求めよ。",
  "exa": r"$x=\pm\sqrt6,\ y=1$ のとき最大値 $12$，$x=0,\ y=-\sqrt3$ のとき最小値 $-6\sqrt3$"},
 {"lv": 4, "title": "最小値の最大値",
  "q": r"$a$ を定数とし，関数 $f(x)=x^2-2ax+a\ \ (0\leqq x\leqq1)$ の最小値を $m(a)$ とする。<br>(1) $m(a)$ を求めよ。<br>(2) $a$ がすべての実数値をとって変化するとき，$m(a)$ の最大値を求めよ。",
  "hint": r"(1) は軸 $x=a$ の位置で3通り。(2) は $b=m(a)$ のグラフ（3つの部分をつないだもの）をかいて，最も高いところを探す。",
  "sol": _svg((-0.7, 1.7), (-0.72, 0.42), W=170, H=125,
              curves=[(lambda u: u if u < 0 else (-u * u + u if u <= 1 else 1 - u), -0.7, 1.7)],
              segs=[((0.5, 0), (0.5, 0.25)), ((0, 0.25), (0.5, 0.25))], pts=[(0.5, 0.25)],
              xt=[(0.5, "1/2"), (1, "1")], yt=[(0.25, "1/4")], xl="a", yl="b", Od=(-3, -3))
         + r"$f(x)=(x-a)^2-a^2+a$，$f(0)=a,\ f(1)=1-a$。<br>"
         r"(1) $a<0$ のとき $\boldsymbol{m(a)=f(0)=a}$<br>$0\leqq a\leqq1$ のとき $\boldsymbol{m(a)=f(a)=-a^2+a}$<br>$a>1$ のとき $\boldsymbol{m(a)=f(1)=1-a}$<br>"
         r"(2) $b=m(a)$ のグラフは右の図のようになる。$a<0$ でも $a>1$ でも $m(a)<0$。<br>"
         r"$0\leqq a\leqq1$ では $m(a)=-\left(a-\dfrac12\right)^2+\dfrac14$ で，$a=\dfrac12$ のとき最大。<br>"
         r"よって　$m(a)$ は $\boldsymbol{a=\dfrac12}$ のとき最大値 $\boldsymbol{\dfrac14}$ をとる。",
  "note": r"「最小値の最大値」は，まず最小値を $a$ の関数として求め，次にその関数の最大値を考える2段階の問題。$m(a)$ のグラフが $a=0,\ 1$ でつながっていることを確かめると検算になる。",
  "ex": r"$a$ を定数とし，関数 $f(x)=x^2-2ax+2a+3\ \ (0\leqq x\leqq2)$ の最小値を $m(a)$ とする。$m(a)$ の最大値と，そのときの $a$ の値を求めよ。",
  "exa": r"$a=1$ のとき最大値 $4$"},
 {"lv": 4, "title": "最大値と最小値の差の最小",
  "q": r"$a$ を定数とし，関数 $f(x)=x^2-2ax\ \ (0\leqq x\leqq2)$ の最大値を $M$，最小値を $m$ とする。$g(a)=M-m$ を $a$ の式で表し，$g(a)$ の最小値を求めよ。",
  "hint": r"最小値は軸 $x=a$ が区間の左外・内・右外で，最大値は軸が区間の中央 $x=1$ の左右で分かれる。境目 $a=0,\ 1,\ 2$ をすべて使って4通りに分ける。",
  "sol": r"$f(x)=(x-a)^2-a^2$，$f(0)=0,\ f(2)=4-4a,\ f(a)=-a^2$。<br>"
         r"[1] $a<0$ のとき　$M=f(2)=4-4a,\ m=f(0)=0$ より $g(a)=4-4a$<br>"
         r"[2] $0\leqq a<1$ のとき　$M=f(2)=4-4a,\ m=-a^2$ より $g(a)=a^2-4a+4=(a-2)^2$<br>"
         r"[3] $1\leqq a\leqq2$ のとき　$M=f(0)=0,\ m=-a^2$ より $g(a)=a^2$<br>"
         r"[4] $a>2$ のとき　$M=f(0)=0,\ m=f(2)=4-4a$ より $g(a)=4a-4$<br>"
         r"$g(a)$ は $a\leqq1$ で減少し（[1] は減少，[2] の $(a-2)^2$ も $a<1$ で減少），$a\geqq1$ で増加する。<br>"
         r"よって　$g(a)$ は $\boldsymbol{a=1}$ のとき最小値 $\boldsymbol{1}$ をとる。",
  "note": r"$M-m$ は $f(x)$ に定数を加えても変わらないので，$f(x)=x^2-2ax+b$ でも答えは同じ。境目 $a=0,\ 1,\ 2$ で隣り合う式の値が一致する（$4,\ 1,\ 4$）ことで検算できる。",
  "ex": r"$a$ を定数とし，関数 $f(x)=x^2-2ax\ \ (0\leqq x\leqq1)$ の最大値と最小値の差を $g(a)$ とする。$g(a)$ の最小値を求めよ。",
  "exa": r"$a=\dfrac12$ のとき最小値 $\dfrac14$"},
 {"lv": 4, "title": "2変数関数の最小（予選決勝法）",
  "q": r"$x\geqq0,\ y\geqq0,\ x+y\leqq2$ を満たす実数 $x,\ y$ について，$F=x^2-2xy+2y^2-4y$ の最小値と，そのときの $x,\ y$ の値を求めよ。",
  "hint": r"2つの文字の範囲が絡み合っているので，まず $y$ を固定して $x$ だけを動かし（予選），得られた最小値を $y$ の関数とみてさらに $y$ を動かす（決勝）。$y$ を固定すると $x$ の範囲は $0\leqq x\leqq2-y$。",
  "sol": r"$y$ を $0\leqq y\leqq2$ の範囲で固定すると，$x$ は $0\leqq x\leqq2-y$ を動く。$F=(x-y)^2+y^2-4y$ は $x$ の2次関数で，軸は $x=y\ (\geqq0)$。<br>"
         r"[1] $y\leqq2-y$ すなわち $0\leqq y\leqq1$ のとき　軸が区間内にあり，最小値は $x=y$ のときの $y^2-4y$<br>"
         r"[2] $1<y\leqq2$ のとき　軸が区間の右外にあり，最小値は $x=2-y$ のときの $(2-2y)^2+y^2-4y=5y^2-12y+4$<br>"
         r"次に $y$ を動かす。$y^2-4y=(y-2)^2-4$ は $0\leqq y\leqq1$ で減少し，最小値は $y=1$ のときの $-3$。<br>"
         r"$5y^2-12y+4=5\left(y-\dfrac65\right)^2-\dfrac{16}5$ は，$1<y\leqq2$ において $y=\dfrac65$ で最小値 $-\dfrac{16}5$。<br>"
         r"$-\dfrac{16}5<-3$ だから，$F$ の最小値は $-\dfrac{16}5$ で，そのとき $y=\dfrac65,\ x=2-\dfrac65=\dfrac45$。<br>"
         r"よって　$\boldsymbol{x=\dfrac45,\ y=\dfrac65}$ のとき最小値 $\boldsymbol{-\dfrac{16}5}$",
  "note": r"範囲の制限がなければ $F=(x-y)^2+(y-2)^2-4$ で最小値 $-4\ (x=y=2)$ だが，点 $(2,\,2)$ は $x+y\leqq2$ を満たさない。「1文字を固定して動かす」予選決勝法は，2変数の範囲が絡むときの定石。",
  "ex": r"$x\geqq0,\ y\geqq0,\ x+y\leqq1$ を満たす実数 $x,\ y$ について，$x^2-2xy+3y^2-3y$ の最小値と，そのときの $x,\ y$ の値を求めよ。",
  "exa": r"$x=\dfrac5{12},\ y=\dfrac7{12}$ のとき最小値 $-\dfrac{25}{24}$"},
 {"lv": 5, "title": "絶対値の最大値の最小（3点での値の組合せ）",
  "q": r"実数 $a,\ b$ に対し，$-1\leqq x\leqq3$ における $|x^2+ax+b|$ の最大値を $M(a,\,b)$ とする。$a,\ b$ が実数全体を動くとき，$M(a,\,b)$ の最小値と，それを与える $a,\ b$ の値を求めよ。",
  "hint": r"$f(x)=x^2+ax+b$ の値を区間の両端と中央の3点 $x=-1,\ 1,\ 3$ でとり，$a,\ b$ が消える組合せ $f(-1)-2f(1)+f(3)$ をつくる。これが定数になることから $M$ の下からの評価が得られる。最後に等号が成り立つ $f$ を具体的に示す。",
  "sol": r"$f(x)=x^2+ax+b,\ M=M(a,\,b)$ とおく。$|f(-1)|,\ |f(1)|,\ |f(3)|$ はどれも $M$ 以下である。<br>"
         r"$f(-1)-2f(1)+f(3)=(1-a+b)-2(1+a+b)+(9+3a+b)=8$<br>だから<br>"
         r"$8=|f(-1)-2f(1)+f(3)|\leqq|f(-1)|+2|f(1)|+|f(3)|\leqq M+2M+M=4M$<br>"
         r"よって，すべての $a,\ b$ に対して $M\geqq2$ ……①<br>"
         r"逆に $a=-2,\ b=-1$ のとき $f(x)=(x-1)^2-2$。$-1\leqq x\leqq3$ では $0\leqq(x-1)^2\leqq4$ だから $-2\leqq f(x)\leqq2$ で，$x=1$ のとき $|f(x)|=2$。よって $M(-2,\,-1)=2$。<br>"
         r"さらに $M=2$ となるのは ① の不等号がすべて等号になるとき，すなわち $|f(-1)|=|f(1)|=|f(3)|=2$ で，かつ $f(-1),\ -2f(1),\ f(3)$ がすべて正のときに限る。"
         r"このとき $f(-1)=f(3)=2,\ f(1)=-2$ で，$f(-1)=f(3)$ より軸は $x=1$，よって $a=-2$，さらに $f(1)=-2$ より $b=-1$。<br>"
         r"以上より　$\boldsymbol{a=-2,\ b=-1}$ のとき最小値 $\boldsymbol{2}$",
  "note": r"放物線を区間の両端と中央で交互に $+2,\ -2,\ +2$ に触れさせるのが最良，という形（チェビシェフの多項式の考え方）。一般に長さ $L$ の区間では，$|x^2+ax+b|$ の最大値の最小は $\dfrac{L^2}8$ になる。「最大値の最小値」は，① どんな場合にも成り立つ下からの評価を示し，② それが実現できることを示す，の2段構えで答える。",
  "ex": r"実数 $a,\ b$ に対し，$0\leqq x\leqq4$ における $|x^2+ax+b|$ の最大値を $M(a,\,b)$ とする。$M(a,\,b)$ の最小値と，それを与える $a,\ b$ の値を求めよ。",
  "exa": r"$a=-4,\ b=2$ のとき最小値 $2$"},
]})


def _mx(f, lo, hi, n=4000, extra=()):
    vs = [f(lo + (hi - lo) * i / n) for i in range(n + 1)] + [f(e) for e in extra if lo <= e <= hi]
    return max(vs), min(vs)


def _v3():
    E = 1e-9
    def chk(f, lo, hi, M, m, extra=()):
        Mx, mn = _mx(f, lo, hi, extra=extra)
        assert abs(Mx - M) < 1e-7 and abs(mn - m) < 1e-7, (Mx, mn, M, m)
    chk(lambda u: u * u - 4 * u + 1, 0, 5, 6, -3)
    chk(lambda u: -2 * u * u + 8 * u - 3, 0, 1, 3, -3)
    chk(lambda u: 2 * u * u + 4 * u - 1, -3, 1, 5, -3)
    chk(lambda u: -u * u + 2 * u + 2, 2, 4, 2, -6)
    for A, B in [(2, 6), (-2, -2)]:
        chk(lambda u: A * u * u - 4 * A * u + B, 1, 4, 6, -2, extra=[2])
    for A, B in [(1, 2), (-1, 4)]:
        chk(lambda u: A * u * u + 2 * A * u + B, -2, 1, 5, 1, extra=[-1])
    sols = solve([b - 6, -4 * a + b + 2], [a, b]); assert sols == {a: 2, b: 6}
    chk(lambda u: (u * u - 2 * u) ** 2 + 4 * (u * u - 2 * u) + 1, -1, 3, 22, -2)
    g = (x**2 + 2 * x) ** 2 - 2 * (x**2 + 2 * x) - 1
    assert simplify(g.subs(x, -1 + sqrt(2)) + 2) == 0 and simplify(g.subs(x, -1 - sqrt(2)) + 2) == 0
    assert _mx(lambda u: (u * u + 2 * u) ** 2 - 2 * (u * u + 2 * u) - 1, -10, 10, n=20000)[1] >= -2 - E
    chk(lambda v: (3 - 2 * v) ** 2 + v * v, 0, 1.5, 9, 9 / 5, extra=[1.2])
    chk(lambda u: 2 * u * u + (4 - 2 * u) ** 2, 0, 2, 16, 16 / 3, extra=[4 / 3])
    assert expand((x - y - 1) ** 2 + (y - 3) ** 2 + 2) == x**2 - 2 * x * y + 2 * y**2 - 2 * x - 4 * y + 12
    assert expand(-(y + 1) ** 2 + 2 * y**2 - 4 * y + 12) == y**2 - 6 * y + 11
    assert expand((x + y + 2) ** 2 + 2 * (y + 1) ** 2 + 3) == x**2 + 2 * x * y + 3 * y**2 + 4 * x + 8 * y + 9
    # 軸が動く・区間が動く
    for i in range(-300, 501):
        A = i / 100
        f = lambda u: u * u - 2 * A * u + 3
        Mx, mn = _mx(f, 0, 2, n=400, extra=[A])
        m = 3 if A < 0 else (-A * A + 3 if A <= 2 else 7 - 4 * A)
        M = 7 - 4 * A if A < 1 else 3
        assert abs(mn - m) < E and abs(Mx - M) < E
        f = lambda u: u * u - 4 * A * u + 1
        Mx, mn = _mx(f, 0, 1, n=400, extra=[2 * A])
        m = 1 if A < 0 else (1 - 4 * A * A if A <= 0.5 else 2 - 4 * A)
        M = 2 - 4 * A if A < 0.25 else 1
        assert abs(mn - m) < E and abs(Mx - M) < E
        f = lambda u: u * u - 4 * u + 5
        Mx, mn = _mx(f, A, A + 2, n=400, extra=[2])
        m = A * A + 1 if A < 0 else (1 if A <= 2 else A * A - 4 * A + 5)
        M = A * A - 4 * A + 5 if A < 1 else A * A + 1
        assert abs(mn - m) < 1e-8 and abs(Mx - M) < 1e-8
        f = lambda u: -u * u + 2 * u + 3
        Mx = _mx(f, A, A + 1, n=400, extra=[1])[0]
        M = -A * A + 4 if A < 0 else (4 if A <= 1 else -A * A + 2 * A + 3)
        assert abs(Mx - M) < 1e-8
    # 2次の条件式（媒介変数で全点を調べる）
    th = [2 * math.pi * i / 40000 for i in range(40000)]
    v = [(2 * math.cos(s)) ** 2 + 4 * math.sqrt(2) * math.sin(s) for s in th]
    assert abs(max(v) - 6) < 1e-7 and abs(min(v) + 4 * math.sqrt(2)) < 1e-7
    v = [(3 * math.cos(s)) ** 2 + 6 * math.sqrt(3) * math.sin(s) for s in th]
    assert abs(max(v) - 12) < 1e-7 and abs(min(v) + 6 * math.sqrt(3)) < 1e-7
    assert simplify(-2 * (-sqrt(2) - 1) ** 2 + 6 + 4 * sqrt(2)) == 0
    # 最小値の最大値・差の最小
    ms, ms2, gs, gs2 = [], [], [], []
    for i in range(-300, 501):
        A = i / 200
        m = A if A < 0 else (-A * A + A if A <= 1 else 1 - A)
        assert abs(_mx(lambda u: u * u - 2 * A * u + A, 0, 1, n=400, extra=[A])[1] - m) < E
        ms.append(m)
        ms2.append(_mx(lambda u: u * u - 2 * A * u + 2 * A + 3, 0, 2, n=400, extra=[A])[1])
        Mx, mn = _mx(lambda u: u * u - 2 * A * u, 0, 2, n=400, extra=[A])
        gf = 4 - 4 * A if A < 0 else ((A - 2) ** 2 if A < 1 else (A * A if A <= 2 else 4 * A - 4))
        assert abs(Mx - mn - gf) < E
        gs.append(gf)
        Mx, mn = _mx(lambda u: u * u - 2 * A * u, 0, 1, n=400, extra=[A])
        gs2.append(Mx - mn)
    assert abs(max(ms) - 0.25) < E and abs(max(ms2) - 4) < E and abs(min(gs) - 1) < E and abs(min(gs2) - 0.25) < E
    assert abs(_mx(lambda u: u * u - 2 * u + 5, 0, 2, extra=[1])[1] - 4) < E      # 練習 a=1
    # 予選決勝法：格子で全探索し、答えの点で値が一致
    N = 600
    F1 = lambda u, v: u * u - 2 * u * v + 2 * v * v - 4 * v
    F2 = lambda u, v: u * u - 2 * u * v + 3 * v * v - 3 * v
    m1 = min(F1(2 * i / N, 2 * j / N) for i in range(N + 1) for j in range(N + 1 - i))
    m2 = min(F2(i / N, j / N) for i in range(N + 1) for j in range(N + 1 - i))
    assert F1(Fr(4, 5), Fr(6, 5)) == Fr(-16, 5) and m1 >= -3.2 - E and m1 < -3.2 + 1e-4
    assert F2(Fr(5, 12), Fr(7, 12)) == Fr(-25, 24) and m2 >= -25 / 24 - E and m2 < -25 / 24 + 1e-4
    # 絶対値の最大値の最小
    def Mab(A, B, lo, hi):
        return max(abs(u * u + A * u + B) for u in [lo + (hi - lo) * i / 400 for i in range(401)])
    assert abs(Mab(-2, -1, -1, 3) - 2) < E and abs(Mab(-4, 2, 0, 4) - 2) < E
    random.seed(5)
    for _ in range(3000):
        A, B = random.uniform(-8, 6), random.uniform(-8, 6)
        assert Mab(A, B, -1, 3) >= 2 - E and Mab(A, B, 0, 4) >= 2 - E
        dA, dB = random.uniform(-0.05, 0.05), random.uniform(-0.05, 0.05)
        assert Mab(-2 + dA, -1 + dB, -1, 3) > 2 and Mab(-4 + dA, 2 + dB, 0, 4) > 2
    ff = x**2 + a * x + b
    assert expand(ff.subs(x, -1) - 2 * ff.subs(x, 1) + ff.subs(x, 3)) == 8
    assert expand(ff.subs(x, 0) - 2 * ff.subs(x, 2) + ff.subs(x, 4)) == 8


# ================================================================ 節4
SEC.append({"title": "2次方程式と判別式",
"base": r"""・$ax^2+bx+c=0\ (a\neq0)$ の解は $x=\dfrac{-b\pm\sqrt{b^2-4ac}}{2a}$。$b=2b'$ のときは $x=\dfrac{-b'\pm\sqrt{b'^2-ac}}{a}$。<br>
・判別式 $D=b^2-4ac$：$D>0$ ⇔ 異なる2つの実数解，$D=0$ ⇔ 重解，$D<0$ ⇔ 実数解をもたない。放物線 $y=ax^2+bx+c$ と $x$ 軸の共有点の個数（2，1，0）に対応する。<br>
・共通解：共通解を $x=\alpha$ とおいて2式を連立し，$\alpha^2$ の項（または定数項）を消去する。<br>
・実数条件：「ある値 $k$ をとる実数 $x$ が存在する」⇔「$x$ の方程式が実数解をもつ」⇔「判別式 $\geqq0$」と読みかえる。""",
"items": [
 {"lv": 1, "title": "2次方程式の解法（因数分解・解の公式）",
  "q": r"次の2次方程式を解け。<br>(1) $3x^2-5x-2=0$　　(2) $x^2-4x+1=0$　　(3) $2x^2+3x-1=0$",
  "hint": r"まず因数分解できるかを見る。できなければ解の公式を使う。$x$ の係数が偶数なら $b=2b'$ の公式で計算が楽になる。",
  "sol": r"(1) $(3x+1)(x-2)=0$ より　$\boldsymbol{x=-\dfrac13,\ 2}$<br>"
         r"(2) $b'=-2$ として　$x=-(-2)\pm\sqrt{(-2)^2-1\cdot1}=\boldsymbol{2\pm\sqrt3}$<br>"
         r"(3) $x=\dfrac{-3\pm\sqrt{3^2-4\cdot2\cdot(-1)}}{2\cdot2}=\boldsymbol{\dfrac{-3\pm\sqrt{17}}4}$",
  "note": r"解の公式は平方完成から導かれる：$ax^2+bx+c=0$ を $a\left(x+\dfrac b{2a}\right)^2=\dfrac{b^2-4ac}{4a}$ と変形すればよい。",
  "ex": r"次の2次方程式を解け。<br>(1) $2x^2+5x-3=0$　　(2) $x^2+6x+4=0$　　(3) $3x^2-2x-2=0$",
  "exa": r"(1) $x=\dfrac12,\ -3$　(2) $x=-3\pm\sqrt5$　(3) $x=\dfrac{1\pm\sqrt7}3$"},
 {"lv": 1, "title": "判別式による実数解の個数と重解",
  "q": r"$k$ を定数とする。2次方程式 $x^2+2(k-1)x+k+5=0$ について<br>(1) 異なる2つの実数解をもつような $k$ の値の範囲を求めよ。<br>(2) 重解をもつような $k$ の値と，そのときの重解を求めよ。",
  "hint": r"$x$ の係数が $2(k-1)$ なので $\dfrac D4=b'^2-ac$ を使う。重解は $x=-\dfrac{b'}a$ で求まる。",
  "sol": r"$\dfrac D4=(k-1)^2-(k+5)=k^2-3k-4=(k+1)(k-4)$<br>"
         r"(1) $D>0$ より $(k+1)(k-4)>0$　よって　$\boldsymbol{k<-1,\ 4<k}$<br>"
         r"(2) $D=0$ より $k=-1,\ 4$。重解は $x=-(k-1)$ だから，$k=-1$ のとき $x=2$，$k=4$ のとき $x=-3$。<br>"
         r"よって　$\boldsymbol{k=-1}$ のとき重解 $\boldsymbol{x=2}$，$\boldsymbol{k=4}$ のとき重解 $\boldsymbol{x=-3}$",
  "note": r"放物線 $y=x^2+2(k-1)x+k+5$ と $x$ 軸の共有点の個数も同じ判別式で決まる。(1) は異なる2点で交わる，(2) は接する場合で，重解が接点の $x$ 座標になる。",
  "ex": r"$k$ を定数とする。2次方程式 $x^2+2kx+2k+3=0$ について<br>(1) 実数解をもたないような $k$ の値の範囲を求めよ。<br>(2) 重解をもつような $k$ の値と，そのときの重解を求めよ。",
  "exa": r"(1) $-1<k<3$　(2) $k=-1$ のとき $x=1$，$k=3$ のとき $x=-3$"},
 {"lv": 2, "title": "2つの2次方程式の少なくとも一方・一方だけが実数解をもつ条件",
  "q": r"$a$ を定数とする。2つの2次方程式 $x^2+2ax+2a+3=0$ ……①，$x^2-ax+a=0$ ……② について，次の条件を満たす $a$ の値の範囲を求めよ。<br>"
       r"(1) ①，② の少なくとも一方が実数解をもつ。<br>(2) ①，② の一方だけが実数解をもつ。",
  "hint": r"①，② の判別式 $D_1,\ D_2$ について，(1) は「$D_1\geqq0$ または $D_2\geqq0$」，(2) は「どちらか一方だけが成り立つ」。2つの範囲を数直線上に並べてかくと確実。",
  "sol": r"$\dfrac{D_1}4=a^2-(2a+3)=(a+1)(a-3)$，$D_2=a^2-4a=a(a-4)$<br>"
         r"$D_1\geqq0$ ⇔ $a\leqq-1,\ 3\leqq a$ ……③　　$D_2\geqq0$ ⇔ $a\leqq0,\ 4\leqq a$ ……④<br>"
         r"(1) ③ または ④ が成り立つ範囲だから　$\boldsymbol{a\leqq0,\ 3\leqq a}$<br>"
         r"(2) ③，④ の一方だけが成り立つ範囲だから　$\boldsymbol{-1<a\leqq0,\ 3\leqq a<4}$",
  "note": r"(1) は余事象「両方とも実数解をもたない」⇔ $D_1<0$ かつ $D_2<0$ ⇔ $0<a<3$ を求め，その残りとしてもよい。「または」「かつ」「一方だけ」の区別を数直線で確かめる。",
  "ex": r"$a$ を定数とする。2つの2次方程式 $x^2+2ax+4=0,\ x^2-2x+a=0$ について<br>(1) 少なくとも一方が実数解をもつ　(2) 一方だけが実数解をもつ<br>ような $a$ の値の範囲をそれぞれ求めよ。",
  "exa": r"(1) $a\leqq1,\ 2\leqq a$　(2) $-2<a\leqq1,\ 2\leqq a$"},
 {"lv": 3, "title": "共通解",
  "q": r"2つの2次方程式 $2x^2+kx+4=0,\ x^2+x+k=0$ が共通な実数解をもつように，定数 $k$ の値を定め，そのときの共通解を求めよ。",
  "hint": r"共通解を $x=\alpha$ とおいて2式を連立する。$\alpha^2$ の項を消去すると $(2-k)(\alpha-2)=0$ と因数分解できる。$k=2$ の場合を見落とさない。",
  "sol": r"共通解を $x=\alpha$ とすると　$2\alpha^2+k\alpha+4=0$ ……①　$\alpha^2+\alpha+k=0$ ……②<br>"
         r"②$\times2-$① より $(2-k)\alpha+2k-4=0$，すなわち $(2-k)(\alpha-2)=0$<br>"
         r"[1] $k=2$ のとき　①，② はともに $x^2+x+2=0$ と同値になるが，判別式は $1-8<0$ で実数解をもたないから不適。<br>"
         r"[2] $k\neq2$ のとき　$\alpha=2$。② に代入して $4+2+k=0$，$k=-6$。<br>"
         r"このとき ① は $2x^2-6x+4=2(x-1)(x-2)=0$，② は $x^2+x-6=(x-2)(x+3)=0$ となり，確かに共通解 $x=2$ をもつ。<br>"
         r"よって　$\boldsymbol{k=-6}$，共通解は $\boldsymbol{x=2}$",
  "note": r"② から $k=-\alpha^2-\alpha$ として ① に代入すると $\alpha$ の3次方程式になり扱いにくい。どの項を消去すれば因数分解できる形になるかを先に見通すとよい。",
  "ex": r"2つの2次方程式 $x^2+kx+3=0,\ x^2+3x+k=0$ が共通な実数解をもつように，定数 $k$ の値を定め，そのときの共通解を求めよ。",
  "exa": r"$k=-4$，共通解 $x=1$"},
 {"lv": 3, "title": "判別式による値域（実数解をもつ条件への読みかえ）",
  "q": r"$x$ が実数全体を動くとき，$y=\dfrac{2x+1}{x^2+2}$ のとり得る値の範囲を求めよ。",
  "hint": r"$y$ がある値 $k$ をとる ⇔ $\dfrac{2x+1}{x^2+2}=k$ を満たす実数 $x$ が存在する ⇔ 分母を払った $x$ の方程式が実数解をもつ。$x^2$ の係数が $k$ になるので，$k=0$ の場合を分ける。",
  "sol": r"$x^2+2>0$ だから，$y$ が値 $k$ をとるための条件は，$x$ の方程式 $k(x^2+2)=2x+1$，すなわち<br>"
         r"$kx^2-2x+2k-1=0$ ……①<br>が実数解をもつことである。<br>"
         r"[1] $k=0$ のとき　① は $-2x-1=0$ となり，実数解 $x=-\dfrac12$ をもつ。<br>"
         r"[2] $k\neq0$ のとき　① は2次方程式で，実数解をもつ条件は<br>"
         r"$\dfrac D4=1-k(2k-1)\geqq0$，$2k^2-k-1\leqq0$，$(2k+1)(k-1)\leqq0$　より　$-\dfrac12\leqq k\leqq1\ (k\neq0)$<br>"
         r"[1]，[2] より　$\boldsymbol{-\dfrac12\leqq y\leqq1}$",
  "note": r"最大値 $1$ は ① が重解 $x=1$ をもつとき（$x=1$ で $y=\dfrac33=1$），最小値 $-\dfrac12$ は $x=-2$ のとき。「値 $k$ をとる ⇔ 方程式が実数解をもつ」という読みかえは，分数式の値域や2変数の問題で広く使える。",
  "ex": r"$x$ が実数全体を動くとき，$y=\dfrac{x^2-x+1}{x^2+x+1}$ のとり得る値の範囲を求めよ。",
  "exa": r"$\dfrac13\leqq y\leqq3$"},
 {"lv": 4, "title": "実数条件による変数の範囲（3変数）",
  "q": r"実数 $x,\ y,\ z$ が $x+y+z=6,\ xy+yz+zx=9$ を満たすとき<br>(1) $z$ のとり得る値の範囲を求めよ。<br>(2) $x^2+y^2+4z$ のとり得る値の範囲を求めよ。",
  "hint": r"$z$ を固定すると $x+y$ と $xy$ が $z$ で表せる。$x,\ y$ は $t^2-(x+y)t+xy=0$ の2つの解だから，これが実数解をもつ（判別式 $\geqq0$）ことが $z$ の条件になる。",
  "sol": r"$x+y=6-z$，$xy=9-z(x+y)=9-z(6-z)=z^2-6z+9$。<br>"
         r"(1) $x,\ y$ は $t$ の2次方程式 $t^2-(6-z)t+z^2-6z+9=0$ の2つの解（重解の場合も含む）である。$x,\ y$ が実数であるための条件は，判別式について<br>"
         r"$(6-z)^2-4(z^2-6z+9)\geqq0$，$-3z^2+12z\geqq0$，$z(z-4)\leqq0$<br>"
         r"よって　$\boldsymbol{0\leqq z\leqq4}$　（$z=0$ のとき $x=y=3$，$z=4$ のとき $x=y=1$ で，端の値もとる）<br>"
         r"(2) $x^2+y^2=(x+y)^2-2xy=(6-z)^2-2(z^2-6z+9)=18-z^2$ だから<br>"
         r"$x^2+y^2+4z=-z^2+4z+18=-(z-2)^2+22$<br>"
         r"$0\leqq z\leqq4$ において，$z=2$ で最大値 $22$，$z=0,\ 4$ で最小値 $18$。<br>"
         r"よって　$\boldsymbol{18\leqq x^2+y^2+4z\leqq22}$",
  "note": r"「$x,\ y$ が実数」という条件を使わないと，$z$ が自由に動けるように見えてしまう。逆に，$0\leqq z\leqq4$ の各 $z$ に対して $t$ の方程式の実数解として $x,\ y$ が定まるので，範囲内のすべての値が実際にとれる。",
  "ex": r"実数 $x,\ y,\ z$ が $x+y+z=2,\ x^2+y^2+z^2=6$ を満たすとき，$z$ のとり得る値の範囲を求めよ。",
  "exa": r"$\dfrac{2-2\sqrt7}3\leqq z\leqq\dfrac{2+2\sqrt7}3$"},
 {"lv": 5, "title": "$f(f(x))=x$ の実数解の個数",
  "q": r"$a$ を実数の定数とし，$f(x)=x^2+2x+a$ とする。$x$ の方程式 $f(f(x))=x$ の異なる実数解の個数を，$a$ の値によって分類せよ。",
  "hint": r"$f(f(x))$ をそのまま展開すると4次式で見通しが悪い。$u=f(x)$ とおき，$f(u)-x=\{f(u)-f(x)\}+\{f(x)-x\}$ と分けると，$f(u)-f(x)=(u^2-x^2)+2(u-x)$ は $u-x$ でくくれる。",
  "sol": r"$u=f(x)$ とおくと<br>"
         r"$f(u)-x=\{f(u)-f(x)\}+\{f(x)-x\}=(u^2-x^2)+2(u-x)+(u-x)=(u-x)(u+x+3)$<br>"
         r"$u-x=x^2+x+a,\ u+x+3=x^2+3x+a+3$ だから，方程式は　$(x^2+x+a)(x^2+3x+a+3)=0$　と同値である。<br>"
         r"$P(x)=x^2+x+a,\ Q(x)=x^2+3x+a+3$ の判別式を $D_P,\ D_Q$ とすると　$D_P=1-4a,\quad D_Q=9-4(a+3)=-4a-3$<br>"
         r"また，$P(x)=0,\ Q(x)=0$ が共通解 $\beta$ をもつとすると，$Q(\beta)-P(\beta)=2\beta+3=0$ より $\beta=-\dfrac32$，$P\left(-\dfrac32\right)=a+\dfrac34=0$ より $a=-\dfrac34$ に限る。<br>"
         r"[1] $a<-\dfrac34$ のとき　$D_P>0,\ D_Q>0$ で共通解はないから　4個<br>"
         r"[2] $a=-\dfrac34$ のとき　$P(x)=\left(x+\dfrac32\right)\left(x-\dfrac12\right),\ Q(x)=\left(x+\dfrac32\right)^2$ だから，解は $x=-\dfrac32,\ \dfrac12$ の2個<br>"
         r"[3] $-\dfrac34<a<\dfrac14$ のとき　$D_P>0,\ D_Q<0$ だから　2個<br>"
         r"[4] $a=\dfrac14$ のとき　$D_P=0,\ D_Q<0$ だから，$x=-\dfrac12$ の1個<br>"
         r"[5] $a>\dfrac14$ のとき　$D_P<0,\ D_Q<0$ だから　0個<br>"
         r"よって　$\boldsymbol{a<-\dfrac34}$ のとき $\boldsymbol{4}$ 個，$\boldsymbol{-\dfrac34\leqq a<\dfrac14}$ のとき $\boldsymbol{2}$ 個，$\boldsymbol{a=\dfrac14}$ のとき $\boldsymbol{1}$ 個，$\boldsymbol{a>\dfrac14}$ のとき $\boldsymbol{0}$ 個",
  "note": r"$P(x)=0$ の解は $f(x)=x$ を満たす $x$（不動点），$Q(x)=0$ の解は $f(p)=q,\ f(q)=p\ (p\neq q)$ となる $p,\ q$（周期2の点）である。ここでは $D_Q=D_P-4$ なので，「$f(x)=x$ が実数解をもたなければ $f(f(x))=x$ も実数解をもたない」。これは一般の2次関数でも正しく，$f(x)-x$ が常に正（常に負）なら，$f(f(x))-x=\{f(f(x))-f(x)\}+\{f(x)-x\}$ も常に正（常に負）であることから示せる。",
  "ex": r"$a$ を実数の定数とし，$f(x)=x^2-4x+a$ とする。$x$ の方程式 $f(f(x))=x$ の異なる実数解の個数を，$a$ の値によって分類せよ。",
  "exa": r"$a<\dfrac{21}4$ のとき4個，$\dfrac{21}4\leqq a<\dfrac{25}4$ のとき2個，$a=\dfrac{25}4$ のとき1個，$a>\dfrac{25}4$ のとき0個"},
]})


def _v4():
    E = 1e-9
    S = lambda e: set(solve(e, x))
    assert S(3 * x**2 - 5 * x - 2) == {R(-1, 3), 2} and S(x**2 - 4 * x + 1) == {2 + sqrt(3), 2 - sqrt(3)}
    assert S(2 * x**2 + 3 * x - 1) == {(-3 + sqrt(17)) / 4, (-3 - sqrt(17)) / 4}
    assert S(2 * x**2 + 5 * x - 3) == {R(1, 2), -3} and S(x**2 + 6 * x + 4) == {-3 + sqrt(5), -3 - sqrt(5)}
    assert S(3 * x**2 - 2 * x - 2) == {(1 + sqrt(7)) / 3, (1 - sqrt(7)) / 3}
    assert expand((k - 1) ** 2 - (k + 5)) == expand((k + 1) * (k - 4)) and expand(k**2 - (2 * k + 3)) == expand((k + 1) * (k - 3))
    for kk, r in [(-1, 2), (4, -3)]:
        assert S(x**2 + 2 * (kk - 1) * x + kk + 5) == {r}
    for kk, r in [(-1, 1), (3, -3)]:
        assert S(x**2 + 2 * kk * x + 2 * kk + 3) == {r}
    for i in range(-80, 81):
        K = Fr(i, 10)
        n1 = _cnt_roots(x**2 + 2 * (K - 1) * x + K + 5, x); assert (n1 == 2) == (K < -1 or K > 4)
        n2 = _cnt_roots(x**2 + 2 * K * x + 2 * K + 3, x); assert (n2 == 0) == (-1 < K < 3)
        D1, D2 = (K + 1) * (K - 3), K * (K - 4)
        assert (D1 >= 0 or D2 >= 0) == (K <= 0 or K >= 3)
        assert ((D1 >= 0) != (D2 >= 0)) == (-1 < K <= 0 or 3 <= K < 4)
        E1, E2 = K * K - 4, 1 - K
        assert (E1 >= 0 or E2 >= 0) == (K <= 1 or K >= 2) and ((E1 >= 0) != (E2 >= 0)) == (-2 < K <= 1 or K >= 2)
    al = symbols("al")
    for e1, e2, ans in [(2 * al**2 + k * al + 4, al**2 + al + k, (-6, 2)), (al**2 + k * al + 3, al**2 + 3 * al + k, (-4, 1))]:
        sols = solve([e1, e2], [k, al], dict=True)
        real = [(s[k], s[al]) for s in sols if s[al].is_real]
        assert real == [ans], sols
    assert expand(2 * (al**2 + al + k) - (2 * al**2 + k * al + 4) - (2 - k) * (al - 2)) == 0
    # 値域
    vs = [(2 * u + 1) / (u * u + 2) for u in [i / 100 for i in range(-20000, 20001)]]
    assert abs(max(vs) - 1) < E and abs(min(vs) + 0.5) < E
    assert Fr(2 * 1 + 1, 1 + 2) == 1 and Fr(2 * (-2) + 1, 4 + 2) == Fr(-1, 2)
    vs = [(u * u - u + 1) / (u * u + u + 1) for u in [i / 100 for i in range(-20000, 20001)]]
    assert abs(max(vs) - 3) < E and abs(min(vs) - 1 / 3) < E
    assert expand((6 - k) ** 2 - 4 * (k**2 - 6 * k + 9)) == -3 * k**2 + 12 * k
    # 3変数
    for i in range(0, 401):
        Z = 4 * i / 400
        s_, p_ = 6 - Z, Z * Z - 6 * Z + 9
        d = s_ * s_ - 4 * p_
        assert d >= -1e-12
        X = (s_ + math.sqrt(max(d, 0))) / 2; Yv = s_ - X
        assert abs(X + Yv + Z - 6) < E and abs(X * Yv + Yv * Z + Z * X - 9) < 1e-9
        assert 18 - E <= X * X + Yv * Yv + 4 * Z <= 22 + E
    for Z in [-0.01, 4.01]:
        assert (6 - Z) ** 2 - 4 * (Z * Z - 6 * Z + 9) < 0
    z1, z2 = sorted(solve(3 * k**2 - 4 * k - 8, k), key=lambda v: float(v))
    assert simplify(z1 - (2 - 2 * sqrt(7)) / 3) == 0 and simplify(z2 - (2 + 2 * sqrt(7)) / 3) == 0
    assert expand((2 - k) ** 2 - 4 * (((2 - k) ** 2 - (6 - k**2)) / 2)) == expand(-(3 * k**2 - 4 * k - 8))
    # f(f(x))=x
    f = lambda e, A: e**2 + 2 * e + A
    assert expand(f(f(x, a), a) - x - (x**2 + x + a) * (x**2 + 3 * x + a + 3)) == 0
    g = lambda e, A: e**2 - 4 * e + A
    assert expand(g(g(x, a), a) - x - (x**2 - 5 * x + a) * (x**2 - 3 * x + a - 3)) == 0
    for i in range(-120, 41):
        A = Fr(i, 40)
        n = _cnt_roots(expand(f(f(x, R(A.numerator, A.denominator)), R(A.numerator, A.denominator)) - x), x)
        exp_ = 4 if A < Fr(-3, 4) else (2 if A < Fr(1, 4) else (1 if A == Fr(1, 4) else 0))
        assert n == exp_, (A, n)
    for i in range(120, 280, 2):
        A = Fr(i, 40)
        n = _cnt_roots(expand(g(g(x, R(A.numerator, A.denominator)), R(A.numerator, A.denominator)) - x), x)
        exp_ = 4 if A < Fr(21, 4) else (2 if A < Fr(25, 4) else (1 if A == Fr(25, 4) else 0))
        assert n == exp_, (A, n)


# ================================================================ 節5
SEC.append({"title": "2次不等式",
"base": r"""・$\alpha<\beta$ のとき　$(x-\alpha)(x-\beta)>0$ ⇔ $x<\alpha,\ \beta<x$，　$(x-\alpha)(x-\beta)<0$ ⇔ $\alpha<x<\beta$<br>
・$a>0,\ D<0$ のとき，$ax^2+bx+c>0$ の解はすべての実数，$ax^2+bx+c<0$ は解なし。$D=0$ のとき，$ax^2+bx+c>0$ の解は重解以外のすべての実数。<br>
・すべての実数 $x$ で $ax^2+bx+c>0$ ⇔「$a=b=0,\ c>0$」または「$a>0,\ D<0$」<br>
・区間内のすべての $x$ で $f(x)>0$ ⇔ その区間における $f(x)$ の最小値 $>0$（グラフで考える）""",
"items": [
 {"lv": 1, "title": "2次不等式の解法",
  "q": r"次の2次不等式を解け。<br>(1) $x^2-x-6>0$　　(2) $2x^2-3x-1\leqq0$　　(3) $x^2-6x+9>0$　　(4) $x^2+2x+3<0$",
  "hint": r"左辺 $=0$ の解を求め，下に凸の放物線が $x$ 軸より上か下かで読む。$D\leqq0$ のときは平方完成して考える。",
  "sol": r"(1) $(x+2)(x-3)>0$ より　$\boldsymbol{x<-2,\ 3<x}$<br>"
         r"(2) $2x^2-3x-1=0$ の解は $x=\dfrac{3\pm\sqrt{17}}4$ だから　$\boldsymbol{\dfrac{3-\sqrt{17}}4\leqq x\leqq\dfrac{3+\sqrt{17}}4}$<br>"
         r"(3) $(x-3)^2>0$ より　<b>$3$ 以外のすべての実数</b><br>"
         r"(4) $x^2+2x+3=(x+1)^2+2>0$ がすべての $x$ で成り立つから　<b>解なし</b>",
  "note": r"$x^2$ の係数が負のときは，両辺に $-1$ を掛けて正にしてから解く（不等号の向きが変わる）。",
  "ex": r"次の2次不等式を解け。<br>(1) $-x^2+2x+8\geqq0$　　(2) $3x^2+2x-2>0$　　(3) $4x^2-4x+1\leqq0$　　(4) $x^2-x+1>0$",
  "exa": r"(1) $-2\leqq x\leqq4$　(2) $x<\dfrac{-1-\sqrt7}3,\ \dfrac{-1+\sqrt7}3<x$　(3) $x=\dfrac12$　(4) すべての実数"},
 {"lv": 1, "title": "連立2次不等式",
  "q": r"連立不等式 $\begin{cases}x^2-4x-5<0\\2x^2-7x+3\geqq0\end{cases}$ を解け。",
  "hint": r"それぞれの不等式を解き，数直線上で共通部分をとる。端点を含むかどうかに注意。",
  "sol": r"$x^2-4x-5<0$ より $(x+1)(x-5)<0$，$-1<x<5$ ……①<br>"
         r"$2x^2-7x+3\geqq0$ より $(2x-1)(x-3)\geqq0$，$x\leqq\dfrac12,\ 3\leqq x$ ……②<br>"
         r"①，② の共通範囲を求めて　$\boldsymbol{-1<x\leqq\dfrac12,\ 3\leqq x<5}$",
  "ex": r"連立不等式 $x^2-2x-8\leqq0,\ x^2-x-2>0$ を解け。",
  "exa": r"$-2\leqq x<-1,\ 2<x\leqq4$"},
 {"lv": 2, "title": "文字係数を含む2次不等式",
  "q": r"$a$ を定数とする。不等式 $x^2-(a+2)x+2a<0$ を解け。",
  "hint": r"左辺は $(x-a)(x-2)$ と因数分解できる。2つの解 $a,\ 2$ の大小で場合を分ける。",
  "sol": r"不等式は $(x-a)(x-2)<0$ となる。<br>"
         r"[1] $a<2$ のとき　$\boldsymbol{a<x<2}$<br>"
         r"[2] $a=2$ のとき　$(x-2)^2<0$ となり　<b>解なし</b><br>"
         r"[3] $a>2$ のとき　$\boldsymbol{2<x<a}$",
  "note": r"$ax^2-(a+1)x+1<0$ のように $x^2$ の係数に文字を含むときは，さらに $a=0$（1次不等式になる）と $a<0$（両辺を $a$ で割ると不等号の向きが変わる）の場合も分ける。",
  "ex": r"$a$ を定数とする。不等式 $x^2-(a^2+a)x+a^3<0$ を解け。",
  "exa": r"$a<0,\ 1<a$ のとき $a<x<a^2$；$a=0,\ 1$ のとき解なし；$0<a<1$ のとき $a^2<x<a$"},
 {"lv": 2, "title": "すべての実数 $x$ で成り立つ条件",
  "q": r"すべての実数 $x$ に対して，不等式 $(a-1)x^2-2(a-1)x+3>0$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "hint": r"$x^2$ の係数 $a-1$ が $0$ になる場合（2次不等式でなくなる）を別に調べる。$a-1\neq0$ なら「下に凸 かつ $x$ 軸と共有点をもたない」。",
  "sol": r"[1] $a=1$ のとき　不等式は $3>0$ となり，すべての $x$ で成り立つ。<br>"
         r"[2] $a\neq1$ のとき　すべての $x$ で成り立つ条件は　$a-1>0$ かつ $\dfrac D4=(a-1)^2-3(a-1)<0$<br>"
         r"$\dfrac D4=(a-1)(a-4)<0$ より $1<a<4$ で，これは $a-1>0$ を満たす。<br>"
         r"[1]，[2] より　$\boldsymbol{1\leqq a<4}$",
  "note": r"$a=1$ の場合を落として $1<a<4$ とする誤りが多い。問題文に「2次不等式」とあれば $a\neq1$ が前提になり，答えは $1<a<4$ になる。",
  "ex": r"すべての実数 $x$ に対して，不等式 $(a+1)x^2+2(a+1)x+2>0$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$-1\leqq a<1$"},
 {"lv": 3, "title": "区間内のすべての $x$ で成り立つ条件",
  "q": r"$0\leqq x\leqq2$ を満たすすべての $x$ に対して，不等式 $x^2-2ax+a+2>0$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "hint": r"$f(x)=x^2-2ax+a+2$ とおき，「$0\leqq x\leqq2$ における $f(x)$ の最小値 $>0$」と言いかえる。最小値は軸 $x=a$ の位置で3通りに分かれる。",
  "sol": r"$f(x)=(x-a)^2-a^2+a+2$ とおく。求める条件は，$0\leqq x\leqq2$ における $f(x)$ の最小値が正であること。<br>"
         r"[1] $a<0$ のとき　最小値は $f(0)=a+2$。$a+2>0$ より $a>-2$。よって $-2<a<0$<br>"
         r"[2] $0\leqq a\leqq2$ のとき　最小値は $f(a)=-a^2+a+2$。$-a^2+a+2>0$ より $(a+1)(a-2)<0$，$-1<a<2$。よって $0\leqq a<2$<br>"
         r"[3] $a>2$ のとき　最小値は $f(2)=6-3a$。$6-3a>0$ より $a<2$ となり，$a>2$ を満たさないので不適。<br>"
         r"[1]～[3] を合わせて　$\boldsymbol{-2<a<2}$",
  "note": r"各場合で，得た範囲と場合分けの条件の共通部分をとり，最後に合併する。$f(x)=x^2+2-a(2x-1)$ と変形すると，グラフは $a$ によらず点 $\left(\dfrac12,\,\dfrac94\right)$ を通ることが分かり，見通しがよくなる。",
  "ex": r"$-1\leqq x\leqq1$ を満たすすべての $x$ に対して，不等式 $x^2+2ax+2a+3\geqq0$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$a\geqq-1$"},
 {"lv": 3, "title": "連立不等式の整数解の個数",
  "q": r"$a$ を定数とする。連立不等式 $x^2-x-6<0,\ x^2+(2-a)x-2a>0$ を満たす整数 $x$ がちょうど2個となるような $a$ の値の範囲を求めよ。",
  "hint": r"1つ目の解は $-2<x<3$ で，含まれる整数は $-1,\ 0,\ 1,\ 2$。2つ目は $(x+2)(x-a)>0$ で，$a$ と $-2$ の大小で場合を分ける。$-2<x<3$ のうち2つ目を満たす部分を数直線で調べる。",
  "sol": r"$x^2-x-6<0$ より $(x+2)(x-3)<0$，$-2<x<3$ ……①<br>"
         r"$x^2+(2-a)x-2a>0$ より $(x+2)(x-a)>0$ ……②<br>"
         r"[1] $a\leqq-2$ のとき　② の解は $x<a,\ -2<x$（$a=-2$ のときは $x\neq-2$）で，① の範囲はすべて ② を満たす。整数解は4個となり不適。<br>"
         r"[2] $a>-2$ のとき　② の解は $x<-2,\ a<x$。① との共通範囲は，$a<3$ なら $a<x<3$，$a\geqq3$ ならなし。<br>"
         r"$a<x<3$ に含まれる整数がちょうど2個，すなわち $1,\ 2$ だけとなる条件は　$0\leqq a<1$<br>"
         r"よって　$\boldsymbol{0\leqq a<1}$",
  "note": r"端の値の確認：$a=0$ のとき範囲は $0<x<3$ で整数は $1,\ 2$（適），$a=1$ のとき $1<x<3$ で整数は $2$ だけ（不適）。不等号に等号が入るかどうかまで丁寧に調べる。",
  "ex": r"$a$ を定数とする。連立不等式 $x^2-3x-10\leqq0,\ x^2-(a+3)x+3a<0$ を満たす整数 $x$ がちょうど2個となるような $a$ の値の範囲を求めよ。",
  "exa": r"$0\leqq a<1,\ 5<a$"},
 {"lv": 4, "title": "「すべて」と「ある」を含む2つの関数の大小",
  "q": r"$f(x)=x^2-2x+3,\ g(x)=-x^2+4x+a$（$a$ は定数）とする。次の条件が成り立つような $a$ の値の範囲をそれぞれ求めよ。<br>"
       r"(1) $0\leqq x\leqq3$ を満たすすべての $x$ に対して $f(x)\geqq g(x)$<br>"
       r"(2) $0\leqq x_1\leqq3,\ 0\leqq x_2\leqq3$ を満たすすべての $x_1,\ x_2$ に対して $f(x_1)\geqq g(x_2)$<br>"
       r"(3) $0\leqq x_1\leqq3$ を満たすどんな $x_1$ に対しても，$f(x_1)\geqq g(x_2)$ となる $x_2\ (0\leqq x_2\leqq3)$ が存在する",
  "hint": r"(1) は同じ $x$ どうしの比較だから $h(x)=f(x)-g(x)$ の最小値 $\geqq0$。(2) は $x_1,\ x_2$ が独立に動くから「$f$ の最小値 $\geqq$ $g$ の最大値」。(3) は「$f$ の最小値 $\geqq$ $g$ の最小値」。",
  "sol": r"$0\leqq x\leqq3$ において，$f(x)=(x-1)^2+2$ の最小値は $f(1)=2$。<br>"
         r"$g(x)=-(x-2)^2+a+4$ の最大値は $g(2)=a+4$，最小値は $g(0)=a$（$g(3)=a+3$）。<br>"
         r"(1) $h(x)=f(x)-g(x)=2x^2-6x+3-a=2\left(x-\dfrac32\right)^2-\dfrac32-a$。$0\leqq x\leqq3$ における最小値は $h\left(\dfrac32\right)=-\dfrac32-a$ で，これが $0$ 以上だから　$\boldsymbol{a\leqq-\dfrac32}$<br>"
         r"(2) （$f$ の最小値）$\geqq$（$g$ の最大値）だから $2\geqq a+4$。よって　$\boldsymbol{a\leqq-2}$<br>"
         r"(3) どの $x_1$ に対しても $f(x_1)\geqq$（$g$ の最小値）となればよいから，（$f$ の最小値）$\geqq$（$g$ の最小値），すなわち $2\geqq a$。よって　$\boldsymbol{a\leqq2}$",
  "note": r"(2) が成り立てば (1) も成り立つが，逆は成り立たない（(1) の範囲のほうが広い）。「すべて」「ある」の組合せごとに，どの最大値・最小値どうしを比べるかを整理しておく。",
  "ex": r"$f(x)=x^2-4x+5,\ g(x)=-x^2+2x+a$ とする。$0\leqq x\leqq3$ の範囲で考えるとき，次の条件を満たす $a$ の値の範囲を求めよ。<br>"
        r"(1) すべての $x$ に対して $f(x)\geqq g(x)$　(2) すべての $x_1,\ x_2$ に対して $f(x_1)\geqq g(x_2)$　(3) $f(x_1)\geqq g(x_2)$ となる $x_1,\ x_2$ が存在する",
  "exa": r"(1) $a\leqq\dfrac12$　(2) $a\leqq0$　(3) $a\leqq8$"},
 {"lv": 5, "title": "両端が動く2次不等式の整数解の個数（文字の分離）",
  "q": r"$a$ を定数とする。$x$ の不等式 $x^2-ax+a<0$ を満たす整数 $x$ がちょうど2個となるような $a$ の値の範囲を求めよ。",
  "hint": r"解の区間の両端が $a$ とともに動くので，直接数えるのは難しい。$a$ について整理すると $x^2<a(x-1)$ で，整数 $x$ を固定すれば $a$ の1次不等式になる。$x-1$ の符号で分けて $a$ を分離し，$h(x)=\dfrac{x^2}{x-1}$ の整数点での値を大きさの順に並べる。",
  "sol": r"不等式は $x^2<a(x-1)$ ……① と同値である。$x=1$ のとき ① は $1<0$ となり成り立たない。<br>"
         r"$h(x)=\dfrac{x^2}{x-1}=x+1+\dfrac1{x-1}$ とおくと，整数 $x\geqq2$ では $x-1>0$ だから ① ⇔ $a>h(x)$，整数 $x\leqq0$ では $x-1<0$ だから ① ⇔ $a<h(x)$。<br>"
         r"・$x\geqq2$ のとき　$h(x+1)-h(x)=1+\dfrac1x-\dfrac1{x-1}=1-\dfrac1{x(x-1)}>0$（$x(x-1)\geqq2$ より）。よって $h(2)<h(3)<h(4)<\cdots$ で，$h(2)=4,\ h(3)=\dfrac92,\ h(4)=\dfrac{16}3$。<br>"
         r"・$x\leqq0$ のとき　$h(x)-h(x-1)=1+\dfrac1{x-1}-\dfrac1{x-2}=1-\dfrac1{(x-1)(x-2)}>0$（$(x-1)(x-2)\geqq2$ より）。よって $h(0)>h(-1)>h(-2)>\cdots$ で，$h(0)=0,\ h(-1)=-\dfrac12,\ h(-2)=-\dfrac43$。<br>"
         r"$x\geqq2$ の整数が ① を満たすには $a>h(x)\geqq4$，$x\leqq0$ の整数が満たすには $a<h(x)\leqq0$ が必要だから，両側の整数が同時に解になることはない。<br>"
         r"[1] $a>4$ のとき　解となる整数は $h(x)<a$ を満たす $x\geqq2$ で，$h$ は増加するから小さい順に $2,\ 3,\ \cdots$ と含まれる。ちょうど2個（$x=2,\ 3$）となる条件は　$h(3)<a\leqq h(4)$，すなわち $\dfrac92<a\leqq\dfrac{16}3$<br>"
         r"[2] $a<0$ のとき　解となる整数は $h(x)>a$ を満たす $x\leqq0$ で，$0,\ -1,\ \cdots$ の順に含まれる。ちょうど2個（$x=0,\ -1$）となる条件は　$h(-2)\leqq a<h(-1)$，すなわち $-\dfrac43\leqq a<-\dfrac12$<br>"
         r"[3] $0\leqq a\leqq4$ のとき　解となる整数はない。<br>"
         r"よって　$\boldsymbol{-\dfrac43\leqq a<-\dfrac12,\quad\dfrac92<a\leqq\dfrac{16}3}$",
  "note": r"グラフでいえば，放物線 $y=x^2$ と点 $(1,\,0)$ を通る直線 $y=a(x-1)$ について，直線が放物線より上にある整数 $x$ を，傾き $a$ を変えながら数えている。解を $\dfrac{a\pm\sqrt{a^2-4a}}2$ と表して整数を数える方法は，両端が同時に動くため場合分けが非常に複雑になる。",
  "ex": r"$a$ を定数とする。$x$ の不等式 $x^2-ax+2a<0$ を満たす整数 $x$ がちょうど1個となるような $a$ の値の範囲を求めよ。",
  "exa": r"$-\dfrac13\leqq a<0,\quad8<a\leqq\dfrac{25}3$（$h(x)=\dfrac{x^2}{x-2}$ は $x\geqq3$ の整数では $h(4)=8$ が最小で，$h(3)=h(6)=9$ となる点に注意）"},
]})


def _v5():
    s17, s7 = math.sqrt(17), math.sqrt(7)
    pts = [i / 64 + 1 / 1000 for i in range(-640, 641)] + list(range(-10, 11))
    cases = [(lambda u: u * u - u - 6 > 0, lambda u: u < -2 or u > 3),
             (lambda u: 2 * u * u - 3 * u - 1 <= 0, lambda u: (3 - s17) / 4 <= u <= (3 + s17) / 4),
             (lambda u: u * u - 6 * u + 9 > 0, lambda u: u != 3),
             (lambda u: u * u + 2 * u + 3 < 0, lambda u: False),
             (lambda u: -u * u + 2 * u + 8 >= 0, lambda u: -2 <= u <= 4),
             (lambda u: 3 * u * u + 2 * u - 2 > 0, lambda u: u < (-1 - s7) / 3 or u > (-1 + s7) / 3),
             (lambda u: 4 * u * u - 4 * u + 1 <= 0, lambda u: u == 0.5),
             (lambda u: u * u - u + 1 > 0, lambda u: True),
             (lambda u: u * u - 4 * u - 5 < 0 and 2 * u * u - 7 * u + 3 >= 0, lambda u: -1 < u <= 0.5 or 3 <= u < 5),
             (lambda u: u * u - 2 * u - 8 <= 0 and u * u - u - 2 > 0, lambda u: -2 <= u < -1 or 2 < u <= 4)]
    for ineq, ans in cases:
        for u in pts + [0.5]:
            assert ineq(u) == ans(u), u
    assert set(solve(2 * x**2 - 3 * x - 1, x)) == {(3 + sqrt(17)) / 4, (3 - sqrt(17)) / 4}
    assert expand((x - a) * (x - a**2) - (x**2 - (a**2 + a) * x + a**3)) == 0
    G = [Fr(i, 8) for i in range(-40, 41)]
    for A in G:
        for X in G:
            ans = (A < X < 2) if A < 2 else (False if A == 2 else 2 < X < A)
            assert ((X - A) * (X - 2) < 0) == ans
            ans = (A < X < A * A) if (A < 0 or A > 1) else (False if A in (0, 1) else A * A < X < A)
            assert (X * X - (A * A + A) * X + A**3 < 0) == ans
    def allpos(p, q, r, strict=True):          # すべての実数 x で p x^2 + q x + r > 0（>=0）
        if p == 0:
            return q == 0 and (r > 0 if strict else r >= 0)
        return p > 0 and (q * q - 4 * p * r < 0 if strict else q * q - 4 * p * r <= 0)
    for A in G:
        assert allpos(A - 1, -2 * (A - 1), 3) == (1 <= A < 4)
        assert allpos(A + 1, 2 * (A + 1), 2) == (-1 <= A < 1)
    def minI(p, q, r, lo, hi):                  # p>0 の2次式の区間最小（厳密）
        v = Fr(-q, 2 * p)
        cand = [lo, hi] + ([v] if lo <= v <= hi else [])
        return min(p * u * u + q * u + r for u in cand)
    for A in G:
        assert (minI(1, -2 * A, A + 2, 0, 2) > 0) == (-2 < A < 2)
        assert (minI(1, 2 * A, 2 * A + 3, -1, 1) >= 0) == (A >= -1)
    # 整数解の個数（全列挙）
    for A in [Fr(i, 16) for i in range(-100, 161)]:
        n1 = sum(1 for X in range(-30, 31) if X * X - X - 6 < 0 and X * X + (2 - A) * X - 2 * A > 0)
        assert (n1 == 2) == (0 <= A < 1)
        n2 = sum(1 for X in range(-30, 31) if X * X - 3 * X - 10 <= 0 and X * X - (A + 3) * X + 3 * A < 0)
        assert (n2 == 2) == (0 <= A < 1 or A > 5)
    # すべて・ある
    for A in [Fr(i, 8) for i in range(-80, 81)]:
        xs = [Fr(i, 40) for i in range(0, 121)]
        fv = [X * X - 2 * X + 3 for X in xs]; gv = [-X * X + 4 * X + A for X in xs]
        assert (all(p >= q for p, q in zip(fv, gv))) == (A <= Fr(-3, 2))
        assert (min(fv) >= max(gv)) == (A <= -2) and (min(fv) >= min(gv)) == (A <= 2)
        fv = [X * X - 4 * X + 5 for X in xs]; gv = [-X * X + 2 * X + A for X in xs]
        assert (all(p >= q for p, q in zip(fv, gv))) == (A <= Fr(1, 2))
        assert (min(fv) >= max(gv)) == (A <= 0) and (max(fv) >= min(gv)) == (A <= 8)
    # 両端が動く不等式の整数解（全列挙）
    for i in range(-480, 721):                  # a = i/48（整数演算で厳密に）
        A = Fr(i, 48)
        n = sum(1 for X in range(-300, 301) if 48 * X * X - i * X + i < 0)
        assert (n == 2) == (Fr(-4, 3) <= A < Fr(-1, 2) or Fr(9, 2) < A <= Fr(16, 3)), (A, n)
        n = sum(1 for X in range(-300, 301) if 48 * X * X - i * X + 2 * i < 0)
        assert (n == 1) == (Fr(-1, 3) <= A < 0 or 8 < A <= Fr(25, 3)), (A, n)
    hh = lambda X: Fr(X * X, X - 1)
    assert all(hh(X + 1) > hh(X) for X in range(2, 300)) and all(hh(X) > hh(X - 1) for X in range(-300, 1))
    assert [hh(X) for X in (2, 3, 4, 0, -1, -2)] == [4, Fr(9, 2), Fr(16, 3), 0, Fr(-1, 2), Fr(-4, 3)]


# ================================================================ 節6
_A6 = 2 * math.sqrt(2) - 2
SEC.append({"title": "絶対値を含む関数とグラフ",
"base": r"""・$y=|f(x)|$ のグラフ：$y=f(x)$ のグラフの $x$ 軸より下の部分を，$x$ 軸に関して折り返す。<br>
・$y=f(|x|)$ のグラフ：$x\geqq0$ の部分をかき，それを $y$ 軸に関して折り返す（$y$ 軸に関して対称）。<br>
・絶対値は中身の符号で場合を分けてはずす：$A\geqq0$ なら $|A|=A$，$A<0$ なら $|A|=-A$。<br>
・$|A|=B$ ⇔「$B\geqq0$ かつ $A=\pm B$」，$|A|<B$ ⇔ $-B<A<B$，$|A|>B$ ⇔「$A<-B$ または $B<A$」""",
"items": [
 {"lv": 1, "title": "$y=|f(x)|$ のグラフ",
  "q": r"(1) 関数 $y=|x^2-2x-3|$ のグラフをかけ。<br>(2) 方程式 $|x^2-2x-3|=4$ を解け。",
  "hint": r"$y=x^2-2x-3=(x+1)(x-3)$ のグラフをかき，$x$ 軸より下にある $-1<x<3$ の部分を折り返す。(2) は $x^2-2x-3=\pm4$ を解く（グラフと直線 $y=4$ の共有点）。",
  "sol": _svg((-2.4, 4.4), (-4.6, 6.3), W=190, H=165,
              curves=[(lambda u: abs(u * u - 2 * u - 3), -2.4, 4.4),
                      (lambda u: u * u - 2 * u - 3, -1, 3, "#999", 0.9, True)],
              segs=[((-2.4, 4), (4.4, 4)), ((1, 0), (1, 4))],
              pts=[(1, 4), (1 - 2 * math.sqrt(2), 4), (1 + 2 * math.sqrt(2), 4)],
              xt=[(-1, "−1"), (3, "3"), (1, "1")], yt=[(3, ""), (4, "")],
              txt=[(3.4, 4, "y=4", 0, -4), (-0.05, 3, "3", -3, 4, "end")])
         + r"(1) $x^2-2x-3=(x-1)^2-4=(x+1)(x-3)$ だから<br>"
         r"$x\leqq-1,\ 3\leqq x$ のとき　$y=x^2-2x-3$<br>"
         r"$-1<x<3$ のとき　$y=-(x^2-2x-3)=-(x-1)^2+4$<br>"
         r"グラフは右の図の実線（破線の部分を $x$ 軸に関して折り返したもの。頂点 $(1,\,-4)$ は $(1,\,4)$ に移る）。<br>"
         r"(2) $x^2-2x-3=4$ より $x^2-2x-7=0$，$x=1\pm2\sqrt2$<br>"
         r"$x^2-2x-3=-4$ より $(x-1)^2=0$，$x=1$<br>"
         r"よって　$\boldsymbol{x=1,\ 1\pm2\sqrt2}$",
  "note": r"直線 $y=4$ は折り返した部分の頂点 $(1,\,4)$ で接するので，解は3個になる。$|f(x)|=k$ の解の個数は，$k$ と折り返した頂点の高さとの大小で変わる（文字定数の分離の節で扱う）。",
  "ex": r"関数 $y=|x^2-4x|$ のグラフをかき，方程式 $|x^2-4x|=3$ を解け。",
  "exa": r"グラフは $y=x^2-4x$ の $0<x<4$ の部分を $x$ 軸に関して折り返したもの（折り返した頂点は $(2,\,4)$）。$x=1,\ 3,\ 2\pm\sqrt7$"},
 {"lv": 2, "title": "$y=f(|x|)$ のグラフと最大・最小",
  "q": r"関数 $y=x^2-4|x|+3$ のグラフをかけ。また，$-1\leqq x\leqq3$ におけるこの関数の最大値と最小値を求めよ。",
  "hint": r"$x\geqq0$ と $x<0$ で絶対値をはずす。$|x|$ だけを含む式は $x$ を $-x$ にしても値が変わらないので，グラフは $y$ 軸に関して対称になる。",
  "sol": _svg((-4.0, 4.0), (-1.7, 4.4), W=200, H=165,
              curves=[(lambda u: u * u - 4 * abs(u) + 3, -4.0, 4.0)],
              segs=[((-2, 0), (-2, -1)), ((2, 0), (2, -1)), ((-0.05, -1), (2, -1))],
              xt=[(-3, "−3"), (-1, "−1"), (1, "1"), (3, "3"), (-2, ""), (2, "")],
              txt=[(-2, 0, "−2", 0, -4), (2, 0, "2", 0, -4), (0, 3, "3", 3, -2, "start"), (0, -1, "−1", -3, 4, "end")])
         + r"$x\geqq0$ のとき　$y=x^2-4x+3=(x-2)^2-1$<br>"
         r"$x<0$ のとき　$y=x^2+4x+3=(x+2)^2-1$<br>"
         r"グラフは右の図（$y$ 軸に関して対称）。<br>"
         r"$-1\leqq x\leqq0$ では $y=(x+2)^2-1$ は増加し，$x=-1$ で $0$，$x=0$ で $3$。<br>"
         r"$0\leqq x\leqq3$ では，$x=2$ で最小値 $-1$ をとり，$x=0$ で $3$，$x=3$ で $0$。<br>"
         r"よって　$\boldsymbol{x=0}$ で最大値 $\boldsymbol{3}$，$\boldsymbol{x=2}$ で最小値 $\boldsymbol{-1}$",
  "note": r"$y=f(|x|)$ 型は「$x\geqq0$ の部分をかいて $y$ 軸で折り返す」とすばやくかける。$x=0$ でグラフがとがり（頂点ではない），そこで最大となることに注意。",
  "ex": r"関数 $y=x^2-2|x-1|$ の $-2\leqq x\leqq2$ における最大値と最小値を求めよ。",
  "exa": r"$x=2$ で最大値 $2$，$x=-1$ で最小値 $-3$"},
 {"lv": 2, "title": "絶対値を含む方程式・不等式",
  "q": r"次の方程式・不等式を解け。<br>(1) $|x^2-4|=3x$　　(2) $|x^2-4|<3x$",
  "hint": r"絶対値の中身 $x^2-4$ の符号で，$x\leqq-2,\ 2\leqq x$ と $-2<x<2$ に分ける。左辺は $0$ 以上だから，右辺 $3x$ も $0$ 以上（(2) では正）でなければならないことを先に使うと場合が減る。",
  "sol": r"(1) 左辺 $\geqq0$ だから $3x\geqq0$，すなわち $x\geqq0$ が必要。<br>"
         r"[1] $x\geqq2$ のとき　$x^2-4=3x$，$(x+1)(x-4)=0$。$x\geqq2$ より $x=4$<br>"
         r"[2] $0\leqq x<2$ のとき　$-(x^2-4)=3x$，$(x+4)(x-1)=0$。$0\leqq x<2$ より $x=1$<br>"
         r"よって　$\boldsymbol{x=1,\ 4}$<br>"
         r"(2) 左辺 $\geqq0$ だから $3x>0$，すなわち $x>0$ が必要。<br>"
         r"[1] $x\geqq2$ のとき　$x^2-3x-4<0$，$(x+1)(x-4)<0$ より $-1<x<4$。$x\geqq2$ と合わせて $2\leqq x<4$<br>"
         r"[2] $0<x<2$ のとき　$4-x^2<3x$，$(x+4)(x-1)>0$ より $x<-4,\ 1<x$。$0<x<2$ と合わせて $1<x<2$<br>"
         r"[1]，[2] を合わせて　$\boldsymbol{1<x<4}$",
  "note": r"(2) は $|A|<B$ ⇔ $-B<A<B$ を使い，$-3x<x^2-4<3x$，すなわち「$x^2+3x-4>0$ かつ $x^2-3x-4<0$」を解いてもよい（$x<-4,\ 1<x$ と $-1<x<4$ の共通範囲で $1<x<4$）。グラフでは，$y=|x^2-4|$ が直線 $y=3x$ より下にある範囲である。",
  "ex": r"次の方程式・不等式を解け。<br>(1) $|x^2-2x-3|=x+1$　　(2) $|x^2-2x-3|>x+1$",
  "exa": r"(1) $x=-1,\ 2,\ 4$　(2) $x<-1,\ -1<x<2,\ 4<x$"},
 {"lv": 4, "title": "絶対値を含む関数の最大値（区間の端が動く）",
  "q": r"$a$ を正の定数とする。関数 $f(x)=x|x-2|$ の $0\leqq x\leqq a$ における最大値 $M(a)$ を求めよ。",
  "hint": r"まず $y=x|x-2|$ のグラフをかく（$x\geqq2$ と $x<2$ で分ける）。区間の右端 $a$ を動かすと，「山の頂上 $(1,\,1)$ を越えるか」「再び高さ $1$ に達する点を越えるか」で最大値の式が変わる。",
  "sol": _svg((-0.4, 3.0), (-0.45, 2.1), W=195, H=135,
              curves=[(lambda u: u * abs(u - 2), 0, 3.0)],
              segs=[((0, 1), (1 + math.sqrt(2), 1)), ((1, 0), (1, 1)), ((1 + math.sqrt(2), 0), (1 + math.sqrt(2), 1))],
              pts=[(1, 1), (1 + math.sqrt(2), 1)],
              xt=[(1, "1"), (2, "2"), (1 + math.sqrt(2), "1+√2")], yt=[(1, "1")])
         + r"$x\geqq2$ のとき $f(x)=x^2-2x=(x-1)^2-1$，$x<2$ のとき $f(x)=-x^2+2x=-(x-1)^2+1$。<br>"
         r"グラフは右の図。$x\geqq2$ の部分で $f(x)=1$ となるのは，$x^2-2x-1=0$ より $x=1+\sqrt2$。<br>"
         r"[1] $0<a<1$ のとき　区間で増加するから　$M(a)=f(a)=-a^2+2a$<br>"
         r"[2] $1\leqq a\leqq1+\sqrt2$ のとき　区間内で $f(x)\leqq1$ で，$x=1$ で最大となるから　$M(a)=1$<br>"
         r"[3] $a>1+\sqrt2$ のとき　$2\leqq x\leqq a$ で $f(x)$ は増加し $f(a)>1$ だから　$M(a)=f(a)=a^2-2a$<br>"
         r"よって　$0<a<1$ のとき $\boldsymbol{M(a)=-a^2+2a}$，$1\leqq a\leqq1+\sqrt2$ のとき $\boldsymbol{M(a)=1}$，$a>1+\sqrt2$ のとき $\boldsymbol{M(a)=a^2-2a}$",
  "note": r"境目の $a=1+\sqrt2$ は「山の高さ $1$ と右端での値が等しくなる」ところで，グラフと直線 $y=1$ の交点として求める。境目では隣り合う式の値が一致する（$a=1$ で $1$，$a=1+\sqrt2$ で $(1+\sqrt2)^2-2(1+\sqrt2)=1$）ことで検算できる。",
  "ex": r"$a$ を正の定数とする。関数 $f(x)=x|x-4|$ の $0\leqq x\leqq a$ における最大値 $M(a)$ を求めよ。",
  "exa": r"$0<a<2$ のとき $M(a)=-a^2+4a$，$2\leqq a\leqq2+2\sqrt2$ のとき $M(a)=4$，$a>2+2\sqrt2$ のとき $M(a)=a^2-4a$"},
 {"lv": 5, "title": "絶対値を含む関数の最大値の最小",
  "q": r"$a$ を実数の定数とし，$0\leqq x\leqq2$ における関数 $f(x)=|x^2-2ax|$ の最大値を $M(a)$ とする。<br>(1) $M(a)$ を求めよ。　　(2) $M(a)$ の最小値と，そのときの $a$ の値を求めよ。",
  "hint": r"$g(x)=x^2-2ax=(x-a)^2-a^2$ は $x=0,\ 2a$ で $0$ になり，$x=a$ で最小値 $-a^2$ をとる。$|g(x)|$ の最大値の候補は「折り返した頂点の高さ $a^2$」と「右端での値 $|g(2)|=|4-4a|$」。$a\leqq0$，$a\geqq2$，$0<a<2$ に分け，候補どうしの大小を比べる。",
  "sol": _svg((-0.25, 2.35), (-0.18, 0.95), W=170, H=120,
              curves=[(lambda u: abs(u * u - 2 * _A6 * u), 0, 2)],
              segs=[((0, _A6 ** 2), (2, _A6 ** 2)), ((_A6, 0), (_A6, _A6 ** 2)), ((2, 0), (2, _A6 ** 2))],
              pts=[(_A6, _A6 ** 2), (2, _A6 ** 2)],
              xt=[(_A6, "a"), (2 * _A6, "2a"), (2, "2")], yt=[(_A6 ** 2, "M")])
         + r"$g(x)=x^2-2ax=(x-a)^2-a^2$ とおくと $g(0)=0,\ g(2)=4-4a$。<br>"
         r"[1] $a\leqq0$ のとき　$0\leqq x\leqq2$ で $g(x)=x(x-2a)\geqq0$ で，$g$ は増加する。よって $M(a)=g(2)=4-4a$<br>"
         r"[2] $a\geqq2$ のとき　$0\leqq x\leqq2$ で $g(x)\leqq0$ で，$g$ は減少するから $|g(x)|$ は増加する。よって $M(a)=|g(2)|=4a-4$<br>"
         r"[3] $1\leqq a<2$ のとき　$2a\geqq2$ より $0\leqq x\leqq2$ で $g(x)\leqq0$ で，$|g(x)|=-(x-a)^2+a^2$ は $x=a$ で最大。よって $M(a)=a^2$<br>"
         r"[4] $0<a<1$ のとき　$0\leqq x\leqq2a$ では $g(x)\leqq0$ で $|g(x)|$ の最大は $|g(a)|=a^2$，$2a\leqq x\leqq2$ では $g(x)\geqq0$ で $g$ は増加し最大は $g(2)=4-4a$。<br>"
         r"$a^2-(4-4a)=a^2+4a-4$ は，$0<a<1$ において $a=2\sqrt2-2$ で $0$ となり，その前後で負から正に変わるから<br>"
         r"$0<a\leqq2\sqrt2-2$ のとき $M(a)=4-4a$，$2\sqrt2-2\leqq a<1$ のとき $M(a)=a^2$<br>"
         r"(1) 以上より　$a\leqq2\sqrt2-2$ のとき $\boldsymbol{M(a)=4-4a}$，$2\sqrt2-2\leqq a\leqq2$ のとき $\boldsymbol{M(a)=a^2}$，$a\geqq2$ のとき $\boldsymbol{M(a)=4a-4}$<br>"
         r"(2) $M(a)$ は $a\leqq2\sqrt2-2$ で減少し，$a\geqq2\sqrt2-2$ で増加する。よって最小値は<br>"
         r"$M(2\sqrt2-2)=4-4(2\sqrt2-2)=12-8\sqrt2$<br>"
         r"ゆえに　$\boldsymbol{a=2\sqrt2-2}$ のとき最小値 $\boldsymbol{12-8\sqrt2}$",
  "note": r"最大値が最小になるのは，2つの候補（山の高さ $a^2$ と右端の値 $4-4a$）が等しくなるとき（図）。一方を小さくしようとすると他方が大きくなる「つり合い」の考え方で，最大値の最小値の問題の典型である。",
  "ex": r"$a$ を実数の定数とし，$0\leqq x\leqq1$ における関数 $|x^2-ax|$ の最大値を $M(a)$ とする。$M(a)$ の最小値と，そのときの $a$ の値を求めよ。",
  "exa": r"$a=2\sqrt2-2$ のとき最小値 $3-2\sqrt2$"},
]})


def _v6():
    E = 1e-9
    sol = set(solve(x**2 - 2 * x - 3 - 4, x)) | set(solve(x**2 - 2 * x - 3 + 4, x))
    assert sol == {1, 1 + 2 * sqrt(2), 1 - 2 * sqrt(2)}
    sol = set(solve(x**2 - 4 * x - 3, x)) | set(solve(x**2 - 4 * x + 3, x))
    assert sol == {1, 3, 2 + sqrt(7), 2 - sqrt(7)}
    def nroots(F, lo, hi, n=200000):            # 符号変化と零点で解の個数を数える（数値）
        vs = [F(lo + (hi - lo) * i / n) for i in range(n + 1)]
        return sum(1 for i in range(n) if vs[i] == 0 or vs[i] * vs[i + 1] < 0)
    assert nroots(lambda u: abs(u * u - 4 * u) - 3, -5, 9) == 4
    def chk(f, lo, hi, M, m, extra=()):
        Mx, mn = _mx(f, lo, hi, extra=extra)
        assert abs(Mx - M) < E and abs(mn - m) < E
    chk(lambda u: u * u - 4 * abs(u) + 3, -1, 3, 3, -1, extra=[0, 2])
    chk(lambda u: u * u - 2 * abs(u - 1), -2, 2, 2, -3, extra=[-1, 1])
    for u in [1, 4]:
        assert abs(u * u - 4) == 3 * u
    for u in [-1, 2, 4]:
        assert abs(u * u - 2 * u - 3) == u + 1
    assert nroots(lambda u: abs(u * u - 4) - 3 * u, -10, 10, n=200001) == 2
    pts = [i / 64 + 1 / 997 for i in range(-640, 641)] + list(range(-10, 11))
    for u in pts:
        assert (abs(u * u - 4) < 3 * u) == (1 < u < 4)
        assert (abs(u * u - 2 * u - 3) > u + 1) == (u < -1 or -1 < u < 2 or u > 4)
    # x|x-2| の最大値
    r2 = math.sqrt(2)
    for i in range(1, 401):
        A = i / 100
        M = _mx(lambda u: u * abs(u - 2), 0, A, n=800, extra=[1])[0]
        Mf = -A * A + 2 * A if A < 1 else (1 if A <= 1 + r2 else A * A - 2 * A)
        assert abs(M - Mf) < E
        M = _mx(lambda u: u * abs(u - 4), 0, 2 * A, n=800, extra=[2])[0]
        B = 2 * A
        Mf = -B * B + 4 * B if B < 2 else (4 if B <= 2 + 2 * r2 else B * B - 4 * B)
        assert abs(M - Mf) < 1e-8
    assert abs((1 + r2) ** 2 - 2 * (1 + r2) - 1) < E
    # |x^2-2ax| の最大値の最小
    Ms = []
    for i in range(-200, 401):
        A = i / 100
        M = _mx(lambda u: abs(u * u - 2 * A * u), 0, 2, n=800, extra=[A])[0]
        Mf = 4 - 4 * A if A <= _A6 else (A * A if A <= 2 else 4 * A - 4)
        assert abs(M - Mf) < E
        Ms.append(M)
    assert min(Ms) >= 12 - 8 * r2 - E
    assert abs(_mx(lambda u: abs(u * u - 2 * _A6 * u), 0, 2, extra=[_A6])[0] - (12 - 8 * r2)) < E
    assert abs(_A6**2 - (12 - 8 * r2)) < E and simplify((2 * sqrt(2) - 2) ** 2 + 4 * (2 * sqrt(2) - 2) - 4) == 0
    M2 = [_mx(lambda u: abs(u * u - A * u), 0, 1, n=400, extra=[A / 2])[0] for A in [j / 1000 for j in range(-500, 3001)]]
    assert min(M2) >= 3 - 2 * r2 - E and abs(_mx(lambda u: abs(u * u - _A6 * u), 0, 1, extra=[_A6 / 2])[0] - (3 - 2 * r2)) < E


# ================================================================ 節7
SEC.append({"title": "2次方程式の解の配置",
"base": r"""$f(x)=x^2+bx+c$（下に凸）とし，$f(x)=0$ の判別式を $D$，グラフの軸を $x=p$ とする。<br>
・2つの解がともに $k$ より大きい ⇔ $D\geqq0,\ p>k,\ f(k)>0$（ともに $k$ より小さいときは $p<k$ にかえる）<br>
・2つの解の間に $k$ がある（一方が $k$ より大きく，他方が小さい）⇔ $f(k)<0$<br>
・$\alpha<x<\beta$ に2つの解（重解を含む）をもつ ⇔ $D\geqq0,\ \alpha<p<\beta,\ f(\alpha)>0,\ f(\beta)>0$<br>
・「異なる2つの解」なら $D>0$ とする。判別式・軸の位置・端点での値の符号の3つに注目し，グラフで考える。""",
"items": [
 {"lv": 2, "title": "2つの解がともに正・異符号",
  "q": r"2次方程式 $x^2-2ax+a+6=0$ が次の条件を満たすような定数 $a$ の値の範囲を求めよ。<br>(1) 異なる2つの正の解をもつ。　　(2) 正の解と負の解を1つずつもつ。",
  "hint": r"$f(x)=x^2-2ax+a+6$ のグラフが $x$ 軸の正の部分と異なる2点で交わる条件を，判別式・軸・$f(0)$ の符号で表す。(2) は $f(0)<0$ だけでよい。",
  "sol": r"$f(x)=x^2-2ax+a+6=(x-a)^2-a^2+a+6$ とおく。<br>"
         r"(1) $y=f(x)$ のグラフが $x$ 軸の正の部分と異なる2点で交わる条件は<br>"
         r"[1] $\dfrac D4=a^2-a-6=(a+2)(a-3)>0$ より $a<-2,\ 3<a$<br>"
         r"[2] 軸 $x=a$ について $a>0$<br>"
         r"[3] $f(0)=a+6>0$ より $a>-6$<br>"
         r"[1]～[3] の共通範囲を求めて　$\boldsymbol{a>3}$<br>"
         r"(2) グラフが $x$ 軸の正の部分と負の部分で1回ずつ交わる条件は $f(0)<0$ だから，$a+6<0$ より　$\boldsymbol{a<-6}$",
  "note": r"(2) で $f(0)<0$ なら下に凸のグラフは必ず $x$ 軸と2点で交わるので，判別式の条件は不要。解と係数の関係（数学II）を使えば，(1) は「$D>0$，2解の和 $2a>0$，2解の積 $a+6>0$」と同じ条件になる。",
  "ex": r"2次方程式 $x^2+2(a-1)x+a+5=0$ が (1) 異なる2つの負の解をもつ，(2) 正の解と負の解を1つずつもつ，ような定数 $a$ の値の範囲をそれぞれ求めよ。",
  "exa": r"(1) $a>4$　(2) $a<-5$"},
 {"lv": 3, "title": "2つの解がそれぞれ指定された区間にある",
  "q": r"2次方程式 $x^2-2ax+3a-2=0$ が，$0<x<1$ と $1<x<2$ の範囲にそれぞれ1つずつ解をもつような定数 $a$ の値の範囲を求めよ。",
  "hint": r"下に凸のグラフが $x=0$ で正，$x=1$ で負，$x=2$ で正となればよい。このとき判別式や軸の条件は自動的に満たされる。",
  "sol": r"$f(x)=x^2-2ax+3a-2$ とおく。$y=f(x)$ のグラフが $0<x<1,\ 1<x<2$ の範囲でそれぞれ $x$ 軸と交わる条件は<br>"
         r"$f(0)=3a-2>0$，$f(1)=a-1<0$，$f(2)=2-a>0$<br>"
         r"よって $a>\dfrac23,\ a<1,\ a<2$ より　$\boldsymbol{\dfrac23<a<1}$",
  "note": r"下に凸のグラフが「正 → 負 → 正」と変化すれば，その各区間で必ず $x$ 軸と交わる（交点はちょうど2つ）から，端点の符号だけで決まる。区間の端が解になる場合を含めるかどうかは，問題文の不等号で判断する。",
  "ex": r"2次方程式 $x^2-ax+a-3=0$ が，$-1<x<0$ と $2<x<3$ の範囲にそれぞれ1つずつ解をもつような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$1<a<3$"},
 {"lv": 3, "title": "区間内に2つの解をもつ条件",
  "q": r"2次方程式 $x^2-2ax+a+2=0$ が，$0<x<3$ の範囲に異なる2つの解をもつような定数 $a$ の値の範囲を求めよ。",
  "hint": r"グラフが区間 $0<x<3$ で $x$ 軸と異なる2点で交わる条件は，判別式 $>0$，軸が区間内，両端での値が正，の4つ。",
  "sol": r"$f(x)=x^2-2ax+a+2=(x-a)^2-a^2+a+2$ とおく。条件は<br>"
         r"[1] $\dfrac D4=a^2-a-2=(a+1)(a-2)>0$ より $a<-1,\ 2<a$<br>"
         r"[2] 軸 $x=a$ について $0<a<3$<br>"
         r"[3] $f(0)=a+2>0$ より $a>-2$<br>"
         r"[4] $f(3)=11-5a>0$ より $a<\dfrac{11}5$<br>"
         r"[1]～[4] の共通範囲を求めて　$\boldsymbol{2<a<\dfrac{11}5}$",
  "note": r"4つの条件のどれか1つでも欠けると誤る。例えば [2] を落とすと $-2<a<-1$ も含まれてしまうが，このとき軸は負で，2つの解はともに負になっている。",
  "ex": r"2次方程式 $x^2-2ax+2a+3=0$ の異なる2つの解がともに $1$ より大きくなるような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$a>3$"},
 {"lv": 4, "title": "区間内に少なくとも1つの解をもつ条件",
  "q": r"2次方程式 $x^2-2ax+a+2=0$ が，$1\leqq x\leqq3$ の範囲に少なくとも1つの解をもつような定数 $a$ の値の範囲を求めよ。",
  "hint": r"「少なくとも1つ」は，(i) 区間内に1つ・外に1つ（端点での値が異符号），(ii) 端点が解，(iii) 区間内に2つ（重解を含む）に分ける。$a$ を分離して，放物線と定点を通る直線の共有点として考える方法もある（検討）。",
  "sol": r"$f(x)=x^2-2ax+a+2$ とおくと $f(1)=3-a,\ f(3)=11-5a$，軸は $x=a$，$\dfrac D4=(a+1)(a-2)$。<br>"
         r"[1] $f(1)f(3)<0$ のとき，区間内にちょうど1つの解をもつ。$(3-a)(11-5a)<0$ より $\dfrac{11}5<a<3$<br>"
         r"[2] $f(1)=0$ のとき $a=3$ で，$f(x)=x^2-6x+5=(x-1)(x-5)$ より解 $x=1$ は区間内にある。<br>"
         r"$f(3)=0$ のとき $a=\dfrac{11}5$ で，$f(x)=(x-3)\left(x-\dfrac75\right)$ より解 $x=3$ は区間内にある。<br>"
         r"[3] $1<x<3$ に2つの解（重解を含む）をもつとき　$\dfrac D4\geqq0,\ 1<a<3,\ f(1)>0,\ f(3)>0$<br>"
         r"すなわち「$a\leqq-1$ または $2\leqq a$」かつ $1<a<3$ かつ $a<3$ かつ $a<\dfrac{11}5$ より　$2\leqq a<\dfrac{11}5$<br>"
         r"[1]～[3] を合わせて　$\boldsymbol{2\leqq a\leqq3}$",
  "note": r"【別解】方程式を $x^2+2=a(2x-1)$ と変形すると，解は放物線 $y=x^2+2$ と直線 $y=a(2x-1)$ の共有点の $x$ 座標である。直線は $a$ によらず点 $\left(\dfrac12,\,0\right)$ を通り，傾きは $2a$。放物線の $1\leqq x\leqq3$ の部分（点 $(1,\,3)$ から点 $(3,\,11)$ まで）と共有点をもつのは，直線が $x=2$ で接するとき（$a=2$）から点 $(1,\,3)$ を通るとき（$a=3$）までで，$2\leqq a\leqq3$ となる。",
  "ex": r"2次方程式 $x^2+ax+a+3=0$ が，$0\leqq x\leqq2$ の範囲に少なくとも1つの解をもつような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$-3\leqq a\leqq-2$"},
 {"lv": 4, "title": "2つの2次方程式の解が交互に並ぶ条件",
  "q": r"$a$ を定数とする。2つの2次方程式 $x^2+x+a=0$ ……①，$x^2+ax+1=0$ ……② がそれぞれ異なる2つの実数解をもち，それら4つの解が数直線上で交互に並ぶような $a$ の値の範囲を求めよ。",
  "hint": r"$f(x)=x^2+x+a,\ g(x)=x^2+ax+1$ の差 $f(x)-g(x)=(1-a)(x-1)$ は1次式で，2つの放物線は $x=1$ でしか交わらない。② の解の間を $g(x)<0$ で表し，① の解 $\alpha_1,\ \alpha_2$ について $g(\alpha_1)g(\alpha_2)<0$ を調べる。",
  "sol": r"$f(x)=x^2+x+a,\ g(x)=x^2+ax+1$ とおく。$a=1$ のとき ①，② は同じ方程式で条件を満たさないから $a\neq1$。<br>"
         r"① が異なる2つの実数解 $\alpha_1<\alpha_2$，② が異なる2つの実数解 $\beta_1<\beta_2$ をもつとする。$g(x)=(x-\beta_1)(x-\beta_2)$ だから，$g(x)<0$ ⇔ $\beta_1<x<\beta_2$。<br>"
         r"4つの解が交互に並ぶ ⇔ $\alpha_1,\ \alpha_2$ の一方だけが $\beta_1<x<\beta_2$ にあり，他方は $\beta_1\leqq x\leqq\beta_2$ の外にある ⇔ $g(\alpha_1)g(\alpha_2)<0$<br>"
         r"ここで $f(\alpha_i)=0$ より　$g(\alpha_i)=f(\alpha_i)-\{f(\alpha_i)-g(\alpha_i)\}=-(1-a)(\alpha_i-1)$　$(i=1,\ 2)$<br>"
         r"また $f(x)=(x-\alpha_1)(x-\alpha_2)$ より $(\alpha_1-1)(\alpha_2-1)=f(1)$ だから<br>"
         r"$g(\alpha_1)g(\alpha_2)=(1-a)^2(\alpha_1-1)(\alpha_2-1)=(1-a)^2f(1)=(1-a)^2(a+2)$<br>"
         r"よって，交互に並ぶ条件は $a+2<0$，すなわち $a<-2$。<br>"
         r"逆に $a<-2$ のとき，① の判別式 $1-4a>0$，② の判別式 $a^2-4>0$ で，ともに異なる2つの実数解をもち，上の議論から解は交互に並ぶ。<br>"
         r"以上より　$\boldsymbol{a<-2}$",
  "note": r"図形的には，2つの放物線 $y=f(x),\ y=g(x)$ はただ1点 $x=1$ で交わり，その交点が $x$ 軸より下にある（$f(1)=g(1)<0$）ことが条件。交点の左右で $f$ と $g$ の大小が入れかわるので，解が交互に並ぶ。",
  "ex": r"$a$ を定数とする。2つの2次方程式 $x^2-2x+a=0,\ x^2+ax-2=0$ がそれぞれ異なる2つの実数解をもち，それらが数直線上で交互に並ぶような $a$ の値の範囲を求めよ。",
  "exa": r"$a<-2,\ -2<a<1$"},
]})


def _qr(p, q, r):              # p x^2 + q x + r = 0 の実数解（昇順, float）。D<0 なら []
    D = q * q - 4 * p * r
    if D < 0:
        return []
    s = math.sqrt(D)
    return sorted([(-q - s) / (2 * p), (-q + s) / (2 * p)])


def _v7():
    G = [Fr(i, 16) for i in range(-160, 161)]
    for A in G:
        Af = float(A)
        D = A * A - A - 6
        rs = _qr(1, -2 * Af, Af + 6)
        assert (D > 0 and min(rs) > 0) == (A > 3)
        assert (A + 6 < 0) == (bool(rs) and rs[0] < 0 < rs[1] and D > 0) or A + 6 == 0
        D2 = (A - 1) ** 2 - (A + 5)
        rs = _qr(1, 2 * (Af - 1), Af + 5)
        assert (D2 > 0 and max(rs) < 0) == (A > 4)
        assert (A + 5 < 0) == (D2 > 0 and rs[0] < 0 < rs[1])
        # 端点の符号（区間に1つずつ）：f(0)>0, f(1)<0, f(2)>0
        f = lambda u: u * u - 2 * A * u + 3 * A - 2
        assert (f(0) > 0 and f(1) < 0 and f(2) > 0) == (Fr(2, 3) < A < 1)
        if Fr(2, 3) < A < 1:
            r1, r2 = _qr(1, -2 * Af, 3 * Af - 2); assert 0 < r1 < 1 < r2 < 2
        f = lambda u: u * u - A * u + A - 3
        assert (f(-1) > 0 and f(0) < 0 and f(2) < 0 and f(3) > 0) == (1 < A < 3)
        # 区間内に2つ
        D = A * A - A - 2
        ok = D > 0 and 0 < A < 3 and A + 2 > 0 and 11 - 5 * A > 0
        assert ok == (2 < A < Fr(11, 5))
        rs = _qr(1, -2 * Af, Af + 2)
        if D > 0:
            assert (0 < rs[0] and rs[1] < 3) == ok
        D = A * A - 2 * A - 3
        rs = _qr(1, -2 * Af, 2 * Af + 3)
        assert (D > 0 and rs[0] > 1) == (A > 3)
        # 少なくとも1つ（[1,3], [0,2]）：厳密に解を数える
        Ar = R(A.numerator, A.denominator)
        n = _cnt_roots(x**2 - 2 * Ar * x + Ar + 2, x, 1, 3)
        assert (n >= 1) == (2 <= A <= 3)
        n = _cnt_roots(x**2 + Ar * x + Ar + 3, x, 0, 2)
        assert (n >= 1) == (-3 <= A <= -2)
        # 交互に並ぶ
        def inter(p1, p2):
            if len(p1) < 2 or len(p2) < 2 or p1[0] == p1[1] or p2[0] == p2[1]:
                return False
            if any(abs(u - v) < 1e-9 for u in p1 for v in p2):      # 共通解があれば交互ではない
                return False
            s = sorted([(v, 0) for v in p1] + [(v, 1) for v in p2])
            return [w for _, w in s] in ([0, 1, 0, 1], [1, 0, 1, 0])
        D1, D2 = 1 - 4 * A, A * A - 4
        p1 = _qr(1, 1, Af) if D1 > 0 else []; p2 = _qr(1, Af, 1) if D2 > 0 else []
        assert inter(p1, p2) == (A < -2)
        D1, D2 = 4 - 4 * A, A * A + 8
        p1 = _qr(1, -2, Af) if D1 > 0 else []; p2 = _qr(1, Af, -2) if D2 > 0 else []
        assert inter(p1, p2) == (A < 1 and A != -2)
    assert expand((x - 3) * (x - R(7, 5)) - (x**2 - 2 * R(11, 5) * x + R(11, 5) + 2)) == 0
    assert expand((x**2 + x + a) - (x**2 + a * x + 1) - (1 - a) * (x - 1)) == 0


# ================================================================ 節8
SEC.append({"title": "文字定数の分離と方程式の解の個数",
"base": r"""・方程式 $f(x)=a$ の実数解は，$y=f(x)$ のグラフと直線 $y=a$ の共有点の $x$ 座標。解の個数は共有点の個数で，直線 $y=a$ を上下に動かして調べる（文字定数の分離）。<br>
・置き換え $t=g(x)$ をしたら，$t$ の範囲と，1つの $t$ に対応する $x$ の個数を必ず調べる。<br>
・文字が $a(x-p)$ の形で入るときは，定点 $(p,\,0)$ を通る直線 $y=a(x-p)$ を回転させて考えることもできる。""",
"items": [
 {"lv": 3, "title": "区間における解の個数（グラフと直線 $y=a$）",
  "q": r"$a$ を定数とする。方程式 $x^2-4x+3-a=0$ の $0\leqq x\leqq3$ における異なる実数解の個数を，$a$ の値によって分類せよ。",
  "hint": r"$x^2-4x+3=a$ と変形し，$y=x^2-4x+3\ (0\leqq x\leqq3)$ のグラフと直線 $y=a$ の共有点の個数を調べる。端での値 $3$（$x=0$），$0$（$x=3$）と頂点の値 $-1$ が境目になる。",
  "sol": _svg((-0.7, 4.0), (-1.8, 3.8), W=175, H=145,
              curves=[(lambda u: u * u - 4 * u + 3, 0, 3)],
              segs=[((0, -1), (2, -1)), ((2, 0), (2, -1)), ((0, 3), (4.0, 3))],
              pts=[(0, 3), (3, 0), (2, -1)],
              xt=[(1, "1"), (2, ""), (3, "3")], yt=[(3, "3"), (-1, "−1")],
              txt=[(2, 0, "2", 0, -4), (3.5, 3, "y=3", 0, -4)])
         + r"方程式は $x^2-4x+3=a$ と同値。$f(x)=x^2-4x+3=(x-2)^2-1$ とおくと，実数解の個数は，$y=f(x)\ (0\leqq x\leqq3)$ のグラフと直線 $y=a$ の共有点の個数に等しい。<br>"
         r"$f(0)=3,\ f(2)=-1,\ f(3)=0$ で，グラフは右の図。直線 $y=a$ を上下に動かすと<br>"
         r"$a<-1$ のとき0個，$a=-1$ のとき1個，$-1<a\leqq0$ のとき2個，$0<a\leqq3$ のとき1個，$3<a$ のとき0個<br>"
         r"よって　$\boldsymbol{a<-1,\ 3<a}$ のとき $\boldsymbol{0}$ 個，$\boldsymbol{a=-1,\ 0<a\leqq3}$ のとき $\boldsymbol{1}$ 個，$\boldsymbol{-1<a\leqq0}$ のとき $\boldsymbol{2}$ 個",
  "note": r"端点の扱いが要点。$a=0$ のとき解は $x=1,\ 3$ の2個（$x=3$ は区間に含まれる），$a=3$ のとき解は $x=0$ の1個（もう1つの解 $x=4$ は区間外）。解の配置の条件（判別式・軸・端点）で場合分けするより，グラフで考えるほうがはるかに見通しがよい。",
  "ex": r"$a$ を定数とする。方程式 $x^2+2x-a=0$ の $-2<x\leqq1$ における異なる実数解の個数を，$a$ の値によって分類せよ。",
  "exa": r"$a<-1,\ 3<a$ のとき0個；$a=-1,\ 0\leqq a\leqq3$ のとき1個；$-1<a<0$ のとき2個"},
 {"lv": 3, "title": "複2次方程式の解の個数（置き換えと対応する個数）",
  "q": r"$a$ を定数とする。方程式 $x^4-4x^2+3-a=0$ の異なる実数解の個数を，$a$ の値によって分類せよ。",
  "hint": r"$t=x^2$ とおくと $t^2-4t+3=a\ (t\geqq0)$。$t>0$ の解1つには $x=\pm\sqrt t$ の2つが対応し，$t=0$ には $x=0$ の1つだけが対応する。",
  "sol": _svg((-0.7, 4.8), (-1.8, 4.0), W=175, H=145,
              curves=[(lambda u: u * u - 4 * u + 3, 0, 4.8)],
              segs=[((0, -1), (2, -1)), ((2, 0), (2, -1)), ((0, 3), (4.8, 3)), ((4, 0), (4, 3))],
              pts=[(0, 3), (2, -1), (4, 3)],
              xt=[(2, ""), (4, "4")], yt=[(3, "3"), (-1, "−1")], txt=[(2, 0, "2", 0, -4)], xl="t")
         + r"$t=x^2$ とおくと $t\geqq0$ で，方程式は　$t^2-4t+3=a$ ……①<br>"
         r"① の解のうち，$t>0$ であるもの1つに対して $x=\pm\sqrt t$ の2個，$t=0$ に対して $x=0$ の1個の解が対応する。<br>"
         r"$g(t)=t^2-4t+3=(t-2)^2-1\ (t\geqq0)$ のグラフ（右の図）と直線 $y=a$ の共有点を調べると<br>"
         r"[1] $a<-1$ のとき　① の解はなく，0個<br>"
         r"[2] $a=-1$ のとき　$t=2$ のみで，$x=\pm\sqrt2$ の2個<br>"
         r"[3] $-1<a<3$ のとき　$0<t<2,\ 2<t<4$ に1つずつで，4個<br>"
         r"[4] $a=3$ のとき　$t=0,\ 4$ で，$x=0,\ \pm2$ の3個<br>"
         r"[5] $a>3$ のとき　$t>4$ に1つ（もう1つは $t<0$）で，2個<br>"
         r"よって　$\boldsymbol{a<-1}$ のとき $\boldsymbol{0}$ 個，$\boldsymbol{a=-1,\ 3<a}$ のとき $\boldsymbol{2}$ 個，$\boldsymbol{a=3}$ のとき $\boldsymbol{3}$ 個，$\boldsymbol{-1<a<3}$ のとき $\boldsymbol{4}$ 個",
  "note": r"$y=x^4-4x^2+3$ のグラフ（$y$ 軸に関して対称）と直線 $y=a$ の共有点を数えても同じ結果になる。置き換えたら「1つの $t$ に何個の $x$ が対応するか」を必ず確認する。",
  "ex": r"$a$ を定数とする。方程式 $x^4-2x^2-a=0$ の異なる実数解の個数を，$a$ の値によって分類せよ。",
  "exa": r"$a<-1$ のとき0個，$a=-1$ のとき2個，$-1<a<0$ のとき4個，$a=0$ のとき3個，$a>0$ のとき2個"},
 {"lv": 4, "title": "絶対値を含む方程式の解の個数（直線の平行移動）",
  "q": r"$k$ を定数とする。方程式 $|x^2-2x-3|=x+k$ の異なる実数解の個数を，$k$ の値によって分類せよ。",
  "hint": r"$y=|x^2-2x-3|$ のグラフと傾き $1$ の直線 $y=x+k$ の共有点を数える。直線を平行移動していくと，折れ目の点 $(-1,\,0),\ (3,\,0)$ を通るときと，折り返した部分 $y=-x^2+2x+3$ に接するときに個数が変わる。",
  "sol": _svg((-2.3, 4.6), (-1.2, 7.4), W=190, H=165,
              curves=[(lambda u: abs(u * u - 2 * u - 3), -2.3, 4.6)],
              segs=[((-2.3, -5.3), (4.6, 1.6), "#888"), ((-2.3, -1.3), (4.6, 5.6), "#888"), ((-2.3, 0.95), (4.6, 7.85), "#888")],
              pts=[(-1, 0), (3, 0), (0.5, 3.75)],
              xt=[(-1, "−1"), (3, "3"), (1, "1")])
         + r"$y=|x^2-2x-3|$ のグラフは，$x\leqq-1,\ 3\leqq x$ で $y=x^2-2x-3$，$-1<x<3$ で $y=-x^2+2x+3$（右の図。破線は $k=-3,\ 1,\ \dfrac{13}4$ のときの直線）。これと直線 $y=x+k$ の共有点の個数を調べる。<br>"
         r"・直線が点 $(3,\,0)$ を通るのは $k=-3$，点 $(-1,\,0)$ を通るのは $k=1$。<br>"
         r"・$-x^2+2x+3=x+k$，すなわち $x^2-x+k-3=0$ が重解をもつ条件は，判別式 $1-4(k-3)=0$ より $k=\dfrac{13}4$。重解 $x=\dfrac12$ は $-1<x<3$ を満たすから，このとき直線は折り返した部分に接する。<br>"
         r"・$y=x^2-2x-3$ に傾き $1$ の直線が接するのは $x^2-3x-3-k=0$ が重解 $x=\dfrac32$ をもつときだが，$x=\dfrac32$ は $x\leqq-1,\ 3\leqq x$ を満たさないので，この部分に接することはない。<br>"
         r"直線 $y=x+k$ を $k$ の小さいほうから平行移動していくと，共有点の個数は<br>"
         r"$\boldsymbol{k<-3}$ のとき $\boldsymbol{0}$ 個，$\boldsymbol{k=-3}$ のとき $\boldsymbol{1}$ 個，$\boldsymbol{-3<k<1}$ のとき $\boldsymbol{2}$ 個，$\boldsymbol{k=1}$ のとき $\boldsymbol{3}$ 個，<br>"
         r"$\boldsymbol{1<k<\dfrac{13}4}$ のとき $\boldsymbol{4}$ 個，$\boldsymbol{k=\dfrac{13}4}$ のとき $\boldsymbol{3}$ 個，$\boldsymbol{k>\dfrac{13}4}$ のとき $\boldsymbol{2}$ 個",
  "note": r"式で確かめる：$3\leqq x$ の部分との共有点は $k\geqq-3$ のとき1個，$x\leqq-1$ の部分とは $k\geqq1$ のとき1個，$-1<x<3$ の部分とは $-3<k\leqq1$ のとき1個，$1<k<\dfrac{13}4$ のとき2個，$k=\dfrac{13}4$ のとき1個。これらを合計すると上の結果になる。",
  "ex": r"$k$ を定数とする。方程式 $|x^2-4|=2x+k$ の異なる実数解の個数を，$k$ の値によって分類せよ。",
  "exa": r"$k<-4$ のとき0個，$k=-4$ のとき1個，$-4<k<4$ のとき2個，$k=4$ のとき3個，$4<k<5$ のとき4個，$k=5$ のとき3個，$k>5$ のとき2個"},
 {"lv": 5, "title": "置き換えと定点を通る直線による解の個数（区間つき4次方程式）",
  "q": r"$a$ を定数とする。$x$ の方程式 $(x^2-2x)^2-2a(x^2-2x)+a+2=0$ の $0\leqq x\leqq3$ における異なる実数解の個数を，$a$ の値によって分類せよ。",
  "hint": r"$t=x^2-2x$ とおく。$0\leqq x\leqq3$ のとき $-1\leqq t\leqq3$ で，1つの $t$ に対応する $x$ の個数が $t$ の範囲によって変わる（1個または2個）。$t$ の方程式を $t^2+2=a(2t-1)$ と変形し，放物線 $u=t^2+2$ と定点 $\left(\dfrac12,\,0\right)$ を通る直線 $u=a(2t-1)$ の共有点として調べる。",
  "sol": _svg((-1.5, 3.3), (-1.0, 12.0), W=210, H=195,
              curves=[(lambda u: u * u + 2, -1, 3), (lambda u: u * u + 2, -1.5, -1, "#999", 0.9, True), (lambda u: u * u + 2, 3, 3.3, "#999", 0.9, True)],
              segs=[((-1.5, 4), (3.3, -5.6), "#888"), ((-1.5, 8), (3.3, -11.2), "#888"),
                    ((-1.5, -8), (3.3, 11.2), "#888"), ((-1.5, -8.8), (3.3, 12.32), "#888")],
              pts=[(0.5, 0), (-1, 3), (0, 2), (2, 6), (3, 11)],
              xt=[(-1, "−1"), (2, "2"), (3, "3")], xl="t", yl="u",
              txt=[(0.5, 0, "P", 6, -3, "start"), (-1.45, 3.9, "a=−1", 1, 26, "start"), (-1.45, 7.8, "a=−2", 1, -4, "start"),
                   (2.1, 6.0, "a=2", 5, 13, "start"), (2.95, 11.0, "a=11/5", -7, -2, "end")])
         + r"$t=x^2-2x=(x-1)^2-1$ とおく。$0\leqq x\leqq3$ のとき $-1\leqq t\leqq3$ で，$x=1\pm\sqrt{1+t}$ のうち $0\leqq x\leqq3$ を満たすものを数えると，1つの $t$ に対応する $x$ の個数は<br>"
         r"$t=-1$ のとき1個（$x=1$），$-1<t\leqq0$ のとき2個，$0<t\leqq3$ のとき1個（$x=1+\sqrt{1+t}$ のみ）……(＊)<br>"
         r"方程式は $t^2-2at+a+2=0$，すなわち $t^2+2=a(2t-1)$ ……① となる。$g(t)=t^2-2at+a+2$ とおく。① の解は，放物線 $u=t^2+2$ と，定点 $\mathrm{P}\left(\dfrac12,\,0\right)$ を通る傾き $2a$ の直線 $u=a(2t-1)$ の共有点の $t$ 座標である（右の図）。<br>"
         r"$g(t)=0$ の判別式は $\dfrac D4=a^2-a-2=(a+1)(a-2)$ で，$a=-1$ のとき重解 $t=-1$，$a=2$ のとき重解 $t=2$（直線が接する）。また $g(-1)=3a+3,\ g(0)=a+2,\ g(3)=11-5a$。<br>"
         r"[1] $-1<a<2$ のとき　$D<0$ で解なし。0個<br>"
         r"[2] $a=-1$ のとき　$t=-1$ のみで，(＊) より1個<br>"
         r"[3] $a<-1$ のとき　$g(-1)<0$ だから，① の解は $t<-1$ に1つ，$t>-1$ に1つ（$t_2$ とする）。<br>"
         r"　$-2<a<-1$ なら $g(0)>0$ で $-1<t_2<0$，$a=-2$ なら $t_2=0$，$a<-2$ なら $g(0)<0<g(3)$ で $0<t_2<3$。<br>"
         r"　よって (＊) より　$-2\leqq a<-1$ のとき2個，$a<-2$ のとき1個<br>"
         r"[4] $a=2$ のとき　$t=2$ のみで，1個<br>"
         r"[5] $a>2$ のとき　$D>0$，軸 $t=a>0$，$g(0)=a+2>0$ より，2つの解はともに正。<br>"
         r"　$2<a\leqq\dfrac{11}5$ なら $g(3)\geqq0$ かつ軸 $t=a<3$ だから，2つの解はともに $0<t\leqq3$ にあり，2個。<br>"
         r"　$a>\dfrac{11}5$ なら $g(3)<0$ で，解は $0<t<3$ に1つ，$t>3$ に1つだから，1個。<br>"
         r"以上より　$\boldsymbol{-1<a<2}$ のとき $\boldsymbol{0}$ 個，$\boldsymbol{a<-2,\ a=-1,\ a=2,\ \dfrac{11}5<a}$ のとき $\boldsymbol{1}$ 個，<br>"
         r"$\boldsymbol{-2\leqq a<-1,\ 2<a\leqq\dfrac{11}5}$ のとき $\boldsymbol{2}$ 個",
  "note": r"「$x$ と $t$ の対応の個数（重み）」と「$t$ の方程式の解の配置」の2段階に分けて整理するのが要点。図では，直線を点 $\mathrm{P}$ のまわりに回転させたとき，① 接する（$a=-1,\ 2$），② 重みが変わる点 $(0,\,2)$ を通る（$a=-2$），③ 端点 $(3,\,11)$ を通る（$a=\dfrac{11}5$），の各瞬間が個数の変わり目になっている。$a=\dfrac{t^2+2}{2t-1}$ と分離すると分数関数のグラフが必要になるが，定点を通る直線にすれば数学I の範囲で処理できる。",
  "ex": r"$a$ を定数とする。$x$ の方程式 $(x^2-4x)^2-a(x^2-4x)+4=0$ の $0\leqq x\leqq5$ における異なる実数解の個数を，$a$ の値によって分類せよ。",
  "exa": r"$-4<a<4$ のとき0個；$a=4,\ \dfrac{29}5<a$ のとき1個；$a<-5,\ a=-4,\ 4<a\leqq\dfrac{29}5$ のとき2個；$a=-5$ のとき3個；$-5<a<-4$ のとき4個"},
]})


def _v8():
    def RA(F):
        return R(F.numerator, F.denominator)
    for A in [Fr(i, 8) for i in range(-24, 41)]:
        n = _cnt_roots(x**2 - 4 * x + 3 - RA(A), x, 0, 3)
        e = 0 if (A < -1 or A > 3) else (1 if (A == -1 or 0 < A <= 3) else 2)
        assert n == e, (A, n)
        n = _cnt_roots(x**2 + 2 * x - RA(A), x, -2, 1, lo_open=True)
        e = 0 if (A < -1 or A > 3) else (1 if (A == -1 or 0 <= A <= 3) else 2)
        assert n == e, (A, n)
        n = _cnt_roots(x**4 - 4 * x**2 + 3 - RA(A), x)
        e = 0 if A < -1 else (2 if (A == -1 or A > 3) else (3 if A == 3 else 4))
        assert n == e, (A, n)
        n = _cnt_roots(x**4 - 2 * x**2 - RA(A), x)
        e = 0 if A < -1 else (2 if (A == -1 or A > 0) else (3 if A == 0 else 4))
        assert n == e, (A, n)
    import numpy as np
    def cnt_num(coef, lo, hi):    # 数値解（境目以外の a で使う）：区間内の相異なる実数解の個数
        rs = sorted(r.real for r in np.roots(coef) if abs(r.imag) < 1e-7 and lo - 1e-9 <= r.real <= hi + 1e-9)
        return len([r for j, r in enumerate(rs) if j == 0 or r - rs[j - 1] > 1e-6])
    def cnt_abs_num(p, q, r, m, kk):    # |p x^2 + q x + r| = m x + kk（数値）
        S = []
        for sg in (1, -1):
            for u in _qr(sg * p, sg * q - m, sg * r - kk):
                if sg * (p * u * u + q * u + r) >= -1e-12 and m * u + kk >= -1e-12:
                    S.append(u)
        S.sort()
        return len([u for j, u in enumerate(S) if j == 0 or u - S[j - 1] > 1e-7])
    def cnt_abs(P, L):            # |P(x)| = L(x) の相異なる実数解（厳密）
        S = set()
        for sgn in (1, -1):
            for r in solve(sgn * P - L, x):
                if r.is_real and simplify(sgn * P.subs(x, r)) >= 0 and simplify(L.subs(x, r)) >= 0:
                    S.add(simplify(r))
        return len(S)
    for K in [Fr(i, 40) for i in range(-240, 281)]:
        exact = K in (-3, 1, Fr(13, 4), -4, 4, 5) or K.denominator <= 2
        n = cnt_abs(x**2 - 2 * x - 3, x + RA(K)) if exact else cnt_abs_num(1, -2, -3, 1, float(K))
        e = (0 if K < -3 else 1 if K == -3 else 2 if K < 1 else 3 if K == 1 else 4 if K < Fr(13, 4) else 3 if K == Fr(13, 4) else 2)
        assert n == e, (K, n)
        n = cnt_abs(x**2 - 4, 2 * x + RA(K)) if exact else cnt_abs_num(1, 0, -4, 2, float(K))
        e = (0 if K < -4 else 1 if K == -4 else 2 if K < 4 else 3 if K == 4 else 4 if K < 5 else 3 if K == 5 else 2)
        assert n == e, (K, n)
    for K in [i / 40 + 1 / 4093 for i in range(-240, 281)]:      # 8-3 検討の各部分ごとの個数
        right = sum(1 for u in _qr(1, -3, -3 - K) if u >= 3)
        left = sum(1 for u in _qr(1, -3, -3 - K) if u <= -1)
        mid = sum(1 for u in _qr(1, -1, K - 3) if -1 < u < 3)
        assert right == (1 if K >= -3 else 0) and left == (1 if K >= 1 else 0)
        assert mid == (1 if -3 < K <= 1 else 2 if 1 < K < 13 / 4 else 0)
    for i in range(-40, 121):                                    # 8-4 の (＊)
        T = Fr(i, 40)
        n = _cnt_roots(x**2 - 2 * x - RA(T), x, 0, 3)
        assert n == (1 if T == -1 else 2 if -1 < T <= 0 else 1 if 0 < T <= 3 else 0)
    gg = t**2 - 2 * a * t + a + 2
    assert [expand(gg.subs(t, v)) for v in (-1, 0, 3)] == [3 * a + 3, a + 2, 11 - 5 * a]
    # 区間つき4次方程式（x について厳密に数える）
    for A in [Fr(i, 40) for i in range(-160, 161)]:
        Ar = RA(A); T = x**2 - 2 * x
        if A in (-2, -1, 2, Fr(11, 5)) or A.denominator <= 4:
            n = _cnt_roots(expand(T**2 - 2 * Ar * T + Ar + 2), x, 0, 3)
        else:
            Af = float(A); n = cnt_num([1, -4, 4 - 2 * Af, 4 * Af, Af + 2], 0, 3)
        e = (0 if -1 < A < 2 else 1 if (A < -2 or A == -1 or A == 2 or A > Fr(11, 5)) else 2)
        assert n == e, (A, n)
    for A in [Fr(i, 40) for i in range(-320, 321)]:
        Ar = RA(A); T = x**2 - 4 * x
        if A in (-5, -4, 4, Fr(29, 5)) or A.denominator <= 2:
            n = _cnt_roots(expand(T**2 - Ar * T + 4), x, 0, 5)
        else:
            Af = float(A); n = cnt_num([1, -8, 16 - Af, 4 * Af, 4], 0, 5)
        e = (0 if -4 < A < 4 else 1 if (A == 4 or A > Fr(29, 5)) else 3 if A == -5 else 4 if -5 < A < -4 else 2)
        assert n == e, (A, n)
    assert expand((x**2 - 2 * x) ** 2 + 2 - a * (2 * (x**2 - 2 * x) - 1) - ((x**2 - 2 * x) ** 2 - 2 * a * (x**2 - 2 * x) + a + 2)) == 0


#@@END
CH = {"no": 2, "sections": SEC}


def verify():
    for name in sorted(k for k in globals() if re.fullmatch(r"_v\d+", k)):
        globals()[name]()
    items = [it for s in SEC for it in s["items"]]
    cnt = {L: sum(1 for it in items if it["lv"] == L) for L in range(1, 6)}
    for s in SEC:                                  # 節の中は易しい順
        lv = [it["lv"] for it in s["items"]]
        assert lv == sorted(lv), s["title"]
    if len(SEC) >= 8:
        assert 47 <= len(items) <= 53, len(items)
        assert cnt[5] >= 5, cnt
        assert 4 <= len(SEC) <= 9
    return len(items), cnt
