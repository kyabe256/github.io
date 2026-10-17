"""第21章 2次曲線・媒介変数・極座標（数学C）"""
import math, random
from sympy import (symbols, sqrt, Rational, simplify, expand, factor, cos, sin, pi, solve,
                   Poly, nsimplify, together, cancel, S, trigsimp, expand_trig)

# ---------------------------------------------------------------- 図の道具（座標は Python で計算）
FS = 'font-family="Liberation Serif,DejaVu Serif,serif"'
HALO = 'stroke="#fff" stroke-width="2.6" stroke-linejoin="round" paint-order="stroke"'
BLUE, RED, GRAY, GREEN, FILL = "#1f3f8f", "#c0392b", "#777", "#2e7d4f", "#dbe4f6"


class Fig:
    def __init__(s, xmin, xmax, ymin, ymax, sc, pad=10, sy=None):
        s.x0, s.x1, s.y0, s.y1, s.sc, s.pad = xmin, xmax, ymin, ymax, sc, pad
        s.sy = sy or sc
        s.W = round((xmax - xmin) * sc + 2 * pad)
        s.H = round((ymax - ymin) * s.sy + 2 * pad)
        s.el = []

    def p(s, x, y):
        return s.pad + (x - s.x0) * s.sc, s.pad + (s.y1 - y) * s.sy

    def inside(s, x, y, m=0.0):
        return s.x0 - m <= x <= s.x1 + m and s.y0 - m <= y <= s.y1 + m

    def _d(s, dash):
        return f' stroke-dasharray="{dash}"' if dash else ""

    def arrow(s, a, b):
        (x1, y1), (x2, y2) = s.p(*a), s.p(*b)
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
        s.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#444" stroke-width="0.9"/>')
        s.el.append(f'<polygon points="{x2+ux:.1f},{y2+uy:.1f} {x2-6*ux-3*uy:.1f},{y2-6*uy+3*ux:.1f} {x2-6*ux+3*uy:.1f},{y2-6*uy-3*ux:.1f}" fill="#444"/>')

    def axes(s, lx="x", ly="y", o=True):
        s.arrow((s.x0, 0), (s.x1, 0)); s.arrow((0, s.y0), (0, s.y1))
        s.text(s.x1, 0, lx, -5, 13, it=True)
        s.text(0, s.y1, ly, 5, 9, it=True)
        if o:
            s.text(0, 0, "O", -11, 12)

    def seg(s, a, b, col=BLUE, w=1.2, dash=None):
        (x1, y1), (x2, y2) = s.p(*a), s.p(*b)
        s.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{s._d(dash)}/>')

    def lineq(s, a, b, c, col=GRAY, w=1.0, dash="4 3"):
        """直線 ax+by=c を枠内に描く"""
        P = []
        if abs(b) > 1e-12:
            for x in (s.x0, s.x1):
                P.append((x, (c - a * x) / b))
        if abs(a) > 1e-12:
            for y in (s.y0, s.y1):
                P.append(((c - b * y) / a, y))
        P = [q for q in P if s.inside(*q, 1e-9)]
        P = sorted(set((round(x, 9), round(y, 9)) for x, y in P))
        if len(P) >= 2:
            s.seg(P[0], P[-1], col, w, dash)

    def curve(s, f, t0, t1, n=240, col=BLUE, w=1.4, dash=None, clip=True):
        segs, cur = [], []
        for k in range(n + 1):
            x, y = f(t0 + (t1 - t0) * k / n)
            if (not clip) or s.inside(x, y, 0.02):
                cur.append(s.p(x, y))
            else:
                if len(cur) > 1:
                    segs.append(cur)
                cur = []
        if len(cur) > 1:
            segs.append(cur)
        for c in segs:
            pts = " ".join("%.1f,%.1f" % q for q in c)
            s.el.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{w}"{s._d(dash)}/>')

    def poly(s, P, fill=FILL, col=BLUE, w=1.1, op=0.6):
        pts = " ".join("%.1f,%.1f" % s.p(*q) for q in P)
        s.el.append(f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op}" stroke="{col}" stroke-width="{w}"/>')

    def circle(s, c, r, col=BLUE, w=1.2, dash=None):
        x, y = s.p(*c)
        s.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*s.sc:.1f}" fill="none" stroke="{col}" stroke-width="{w}"{s._d(dash)}/>')

    def dot(s, x, y, col="#222", r=2.2):
        X, Y = s.p(x, y)
        s.el.append(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r}" fill="{col}"/>')

    def text(s, x, y, t, dx=0, dy=0, it=False, size=11, anchor="start", col="#222"):
        X, Y = s.p(x, y); st = ' font-style="italic"' if it else ""
        s.el.append(f'<text x="{X+dx:.1f}" y="{Y+dy:.1f}" font-size="{size}"{st} text-anchor="{anchor}" fill="{col}" {FS} {HALO}>{t}</text>')

    def svg(s):
        assert s.W <= 260, s.W
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" '
                f'xmlns="http://www.w3.org/2000/svg">' + "".join(s.el) + "</svg>")


def ell(a, b, cx=0.0, cy=0.0, rot=0.0):
    cr, sr = math.cos(rot), math.sin(rot)
    return lambda t: (cx + a * math.cos(t) * cr - b * math.sin(t) * sr, cy + a * math.cos(t) * sr + b * math.sin(t) * cr)


def close(a, b, e=1e-9):
    return abs(a - b) < e


SEC = []


# ---------------------------------------------------------------- 節1
def fig_parab():
    f = Fig(-3.6, 3.0, -5.2, 5.2, 12)
    f.axes()
    f.curve(lambda t: (-t * t / 8, t), -5.2, 5.2)
    f.lineq(1, 0, 2, col=RED, w=1.1, dash="4 3")
    f.dot(-2, 0, col=RED)
    f.text(-2, 0, "F", -4, -6, anchor="end")
    f.text(2, -4.6, "x=2", 3, 0, it=True, size=10)
    f.text(2, 0, "2", 3, 12, size=10)
    return f.svg()


def fig_hyp():
    f = Fig(-8.2, 8.2, -5.0, 5.0, 13.5)
    f.lineq(3, -4, 0); f.lineq(3, 4, 0)
    f.seg((-4, -3), (4, -3), GRAY, 0.7, "2 2"); f.seg((-4, 3), (4, 3), GRAY, 0.7, "2 2")
    f.seg((-4, -3), (-4, 3), GRAY, 0.7, "2 2"); f.seg((4, -3), (4, 3), GRAY, 0.7, "2 2")
    f.axes()
    f.curve(lambda t: (4 * math.cosh(t), 3 * math.sinh(t)), -1.6, 1.6)
    f.curve(lambda t: (-4 * math.cosh(t), 3 * math.sinh(t)), -1.6, 1.6)
    for x in (5, -5):
        f.dot(x, 0, col=RED)
    f.text(5, 0, "5", 2, 12, size=10); f.text(-5, 0, "−5", -2, 12, size=10, anchor="end")
    f.text(4, 0, "4", -9, 12, size=10); f.text(-4, 0, "−4", 3, 12, size=10)
    f.text(6.6, 4.95, "y=3x/4", -2, 10, it=True, size=10, anchor="end")
    return f.svg()


def fig_locus1():
    f = Fig(-4.3, 6.3, -5.3, 5.3, 14)
    f.axes()
    f.circle((1, 0), 5, col=GRAY, w=1.0)
    f.circle((-1, 0), 1, col=GRAY, w=1.0)
    f.curve(ell(3, math.sqrt(8)), 0, 2 * math.pi, col=BLUE, w=1.5)
    f.circle((0, math.sqrt(8)), 2, col=RED, w=1.0, dash="3 2")
    f.dot(0, math.sqrt(8), col=RED)
    f.text(0, math.sqrt(8), "P", 4, -4)
    f.dot(1, 0); f.dot(-1, 0)
    f.text(1, 0, "F", 2, 12, size=10); f.text(-1, 0, "F′", -2, 12, size=10, anchor="end")
    f.text(4.0, -3.2, "C₂", 0, 0, size=10)
    return f.svg()


SEC.append({"title": r"放物線・楕円・双曲線",
"base": r"""・放物線 $y^2=4px$（$p\neq0$）：焦点 $(p,\ 0)$，準線 $x=-p$。$x^2=4py$ なら焦点 $(0,\ p)$，準線 $y=-p$。放物線上の点から焦点までの距離と準線までの距離は等しい。<br>
・楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$（$a>b>0$）：焦点 $(\pm\sqrt{a^2-b^2},\ 0)$，長軸の長さ $2a$，短軸の長さ $2b$，2焦点からの距離の和 $=2a$。<br>
・双曲線 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$（$a>0,\ b>0$）：焦点 $(\pm\sqrt{a^2+b^2},\ 0)$，頂点 $(\pm a,\ 0)$，2焦点からの距離の差 $=2a$，漸近線 $y=\pm\dfrac bax$。$\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=-1$ は焦点が $y$ 軸上にある。<br>
・楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ は、円 $x^2+y^2=a^2$ を $x$ 軸をもとにして $y$ 軸方向に $\dfrac ba$ 倍したものである。""",
"items": [
 {"lv": 1, "title": r"放物線の焦点と準線",
  "q": r"(1) 放物線 $y^2=-8x$ の焦点の座標と準線の方程式を求め、概形をかけ。<br>(2) 焦点が $(0,\ 3)$，準線が直線 $y=-3$ である放物線の方程式を求めよ。",
  "hint": r"(1) 標準形 $y^2=4px$ と係数を比べて $p$ を読み取る。(2) 定義「焦点までの距離＝準線までの距離」をそのまま式にするのが確実。",
  "sol": fig_parab() + r"(1) $y^2=4\cdot(-2)x$ より $p=-2$。<br>焦点 $\boldsymbol{(-2,\ 0)}$，準線 $\boldsymbol{x=2}$<br>概形は右の図（左に開く）。<br>"
         r"(2) 放物線上の点を $\mathrm{P}(x,\ y)$ とすると、焦点 $(0,\ 3)$ までの距離と準線 $y=-3$ までの距離が等しいから<br>$\sqrt{x^2+(y-3)^2}=|y+3|$<br>両辺を2乗して $x^2+y^2-6y+9=y^2+6y+9$<br>よって　$\boldsymbol{x^2=12y}$",
  "note": r"$y^2=4px$ は $p>0$ なら右に、$p<0$ なら左に開く。焦点と準線は頂点（原点）をはさんで反対側に、頂点から等しい距離 $|p|$ のところにある。",
  "ex": r"(1) 放物線 $x^2=-2y$ の焦点の座標と準線の方程式を求めよ。<br>(2) 焦点が $(3,\ 0)$，準線が直線 $x=-3$ である放物線の方程式を求めよ。",
  "exa": r"(1) 焦点 $\left(0,\ -\dfrac12\right)$，準線 $y=\dfrac12$　(2) $y^2=12x$"},
 {"lv": 1, "title": r"楕円の焦点・長軸・短軸",
  "q": r"(1) 楕円 $4x^2+9y^2=36$ の長軸・短軸の長さと焦点の座標を求めよ。<br>(2) 2点 $(0,\ 4)$，$(0,\ -4)$ を焦点とし、焦点からの距離の和が $10$ である楕円の方程式を求めよ。",
  "hint": r"(1) 右辺を $1$ にして標準形に直す。原点から焦点までの距離 $c$ は、長い方の半径を $a$，短い方を $b$ として $c^2=a^2-b^2$。(2) 焦点が $y$ 軸上にあるので $\dfrac{x^2}{b^2}+\dfrac{y^2}{a^2}=1$（$a>b>0$）とおく。",
  "sol": r"(1) 両辺を $36$ で割ると $\dfrac{x^2}{9}+\dfrac{y^2}{4}=1$。$a=3,\ b=2$ であるから<br>長軸の長さ $\boldsymbol{6}$，短軸の長さ $\boldsymbol{4}$<br>$\sqrt{9-4}=\sqrt5$ より　焦点 $\boldsymbol{(\sqrt5,\ 0),\ (-\sqrt5,\ 0)}$<br>"
         r"(2) 求める楕円を $\dfrac{x^2}{b^2}+\dfrac{y^2}{a^2}=1$（$a>b>0$）とおく。距離の和について $2a=10$ より $a=5$。焦点が $(0,\ \pm4)$ であるから $a^2-b^2=16$，よって $b^2=9$。<br>求める方程式は　$\boldsymbol{\dfrac{x^2}{9}+\dfrac{y^2}{25}=1}$",
  "note": r"(2) で短軸の端 $(\pm3,\ 0)$ から2焦点までの距離はともに $a=5$ であり、$3^2+4^2=5^2$ が成り立つ。$a^2=b^2+c^2$ はこの直角三角形で覚えておくとよい。",
  "ex": r"(1) 楕円 $25x^2+16y^2=400$ の長軸・短軸の長さと焦点の座標を求めよ。<br>(2) 2点 $(2,\ 0)$，$(-2,\ 0)$ を焦点とし、点 $(2,\ 3)$ を通る楕円の方程式を求めよ。",
  "exa": r"(1) 長軸 $10$，短軸 $8$，焦点 $(0,\ \pm3)$　(2) $\dfrac{x^2}{16}+\dfrac{y^2}{12}=1$"},
 {"lv": 1, "title": r"双曲線の頂点・焦点・漸近線",
  "q": r"双曲線 $9x^2-16y^2=144$ の頂点と焦点の座標、漸近線の方程式を求め、概形をかけ。",
  "hint": r"標準形 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$ に直す。焦点は $c^2=a^2+b^2$（楕円とは符号が違う）。漸近線は右辺の $1$ を $0$ にした $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=0$ から得られる。",
  "sol": fig_hyp() + r"両辺を $144$ で割ると $\dfrac{x^2}{16}-\dfrac{y^2}{9}=1$<br>$a=4,\ b=3$，$c=\sqrt{16+9}=5$ であるから<br>頂点 $\boldsymbol{(4,\ 0),\ (-4,\ 0)}$<br>焦点 $\boldsymbol{(5,\ 0),\ (-5,\ 0)}$<br>"
         r"漸近線は $\dfrac{x^2}{16}-\dfrac{y^2}{9}=0$ より　$\boldsymbol{y=\pm\dfrac34x}$<br>概形は右の図（赤い点が焦点）。",
  "note": r"4点 $(\pm a,\ \pm b)$ を頂点とする長方形（図の点線）の対角線が漸近線になる。原点から焦点までの距離 $c$ は、この長方形の対角線の長さの半分に等しい。",
  "ex": r"双曲線 $x^2-4y^2=-4$ の頂点と焦点の座標、漸近線の方程式を求めよ。",
  "exa": r"頂点 $(0,\ \pm1)$，焦点 $(0,\ \pm\sqrt5)$，漸近線 $y=\pm\dfrac12x$"},
 {"lv": 2, "title": r"条件から双曲線の方程式を決める",
  "q": r"次の条件を満たす双曲線の方程式を求めよ。<br>(1) 焦点が $(\sqrt5,\ 0)$，$(-\sqrt5,\ 0)$ で、漸近線が2直線 $y=\pm2x$<br>(2) 漸近線が2直線 $y=\pm\dfrac12x$ で、点 $(4,\ \sqrt3)$ を通る",
  "hint": r"(1) $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$ とおき、$a^2+b^2=5$，$\dfrac ba=2$ を解く。(2) 焦点が $x$ 軸上か $y$ 軸上か分からないので、漸近線が $y=\pm\dfrac12x$ である双曲線を $\dfrac{x^2}{4}-y^2=k$（$k\neq0$）とまとめて表す。",
  "sol": r"(1) 焦点が $x$ 軸上にあるから $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$（$a>0,\ b>0$）とおける。<br>$a^2+b^2=5$，$\dfrac ba=2$ より $5a^2=5$，$a=1,\ b=2$。<br>よって　$\boldsymbol{x^2-\dfrac{y^2}{4}=1}$<br>"
         r"(2) 漸近線 $y=\pm\dfrac12x$ は $\dfrac{x^2}{4}-y^2=0$ とまとめられるから、求める双曲線は $\dfrac{x^2}{4}-y^2=k$（$k\neq0$）と表せる。点 $(4,\ \sqrt3)$ を通るから $k=4-3=1$。<br>よって　$\boldsymbol{\dfrac{x^2}{4}-y^2=1}$",
  "note": r"$\dfrac{x^2}{4}-y^2=k$ は $k>0$ なら焦点が $x$ 軸上、$k<0$ なら $y$ 軸上の双曲線になる。たとえば点 $(1,\ 1)$ を通るなら $k=-\dfrac34$ で、$y^2-\dfrac{x^2}{4}=\dfrac34$ となる。",
  "ex": r"次の条件を満たす双曲線の方程式を求めよ。<br>(1) 焦点が $(4,\ 0)$，$(-4,\ 0)$ で、点 $(4,\ 6)$ を通る<br>(2) 漸近線が2直線 $y=\pm3x$ で、点 $(1,\ 1)$ を通る",
  "exa": r"(1) $\dfrac{x^2}{4}-\dfrac{y^2}{12}=1$　(2) $9x^2-y^2=8$"},
 {"lv": 3, "title": r"2円に接する円の中心の軌跡",
  "q": r"円 $C_1:(x+1)^2+y^2=1$ に外接し、円 $C_2:(x-1)^2+y^2=25$ に内接する円の中心 $\mathrm{P}$ の軌跡を求めよ。",
  "hint": r"動く円の半径を $r$ とおくと、外接・内接の条件は「中心間の距離＝半径の和・差」。$r$ を消すと2定点からの距離の和が一定となり、楕円の定義が現れる。最後に逆の確認（半径が正になるか）を忘れない。",
  "sol": fig_locus1() + r"$C_1,\ C_2$ の中心を $\mathrm{F'}(-1,\ 0)$，$\mathrm{F}(1,\ 0)$ とする。$\mathrm{F'F}+1=3<5$ だから $C_1$ は $C_2$ の内部にある。<br>"
         r"中心 $\mathrm{P}$，半径 $r$ の円が条件を満たすとき<br>$\mathrm{PF'}=r+1$，$\mathrm{PF}=5-r$<br>辺々加えて $\mathrm{PF'}+\mathrm{PF}=6$。<br>"
         r"よって $\mathrm{P}$ は2点 $\mathrm{F},\ \mathrm{F'}$ を焦点とし、距離の和が $6$ の楕円上にある。$a=3$，$c=1$，$b^2=9-1=8$ より、この楕円は $\dfrac{x^2}{9}+\dfrac{y^2}{8}=1$。<br>"
         r"逆に、この楕円上の任意の点 $\mathrm{P}$ をとり $r=\mathrm{PF'}-1$ とおく。$\mathrm{PF'}+\mathrm{PF}=6$ と $|\mathrm{PF'}-\mathrm{PF}|\leqq\mathrm{FF'}=2$ より $2\leqq\mathrm{PF'}\leqq4$，よって $1\leqq r\leqq3$ で $r>0$。さらに $\mathrm{PF}=6-\mathrm{PF'}=5-r$ であるから、中心 $\mathrm{P}$，半径 $r$ の円は $C_1$ に外接し、$C_2$ に内接する。<br>"
         r"以上より、求める軌跡は　楕円 $\boldsymbol{\dfrac{x^2}{9}+\dfrac{y^2}{8}=1}$",
  "note": r"2円の両方に外接する円の中心なら「距離の差が一定」となり、双曲線の片方の枝が軌跡になる。図は $\mathrm{P}(0,\ 2\sqrt2)$，$r=2$ の場合。",
  "ex": r"2円 $(x+3)^2+y^2=4$，$(x-3)^2+y^2=1$ の両方に外接する円の中心の軌跡を求めよ。",
  "exa": r"双曲線 $4x^2-\dfrac{4}{35}y^2=1$ の $x>0$ の部分"},
]})


def _v1():
    x, y, t = symbols("x y t", real=True)
    for _ in range(50):
        Y = random.uniform(-5, 5); X = -Y * Y / 8
        assert close(math.hypot(X + 2, Y), abs(X - 2))
        X = random.uniform(-5, 5); Y = X * X / 12
        assert close(math.hypot(X, Y - 3), abs(Y + 3))
        X = random.uniform(-5, 5); Y = -X * X / 2
        assert close(math.hypot(X, Y + 0.5), abs(Y - 0.5))
        Y = random.uniform(-5, 5); X = Y * Y / 12
        assert close(math.hypot(X - 3, Y), abs(X + 3))
    # 楕円
    assert sqrt(9 - 4) == sqrt(5)
    for _ in range(50):
        th = random.uniform(0, 2 * math.pi); X, Y = 3 * math.cos(th), 5 * math.sin(th)
        assert close(math.hypot(X, Y - 4) + math.hypot(X, Y + 4), 10)
    assert sqrt(25 - 16) == 3                       # x^2/16+y^2/25: 焦点 (0,±3)
    assert math.hypot(0, 3) + math.hypot(4, 3) == 8 and Rational(4, 16) + Rational(9, 12) == 1
    assert 16 - 12 == 4                             # c=2
    # 双曲線
    assert sqrt(16 + 9) == 5 and sqrt(1 + 4) == sqrt(5)
    # 双曲線の決定
    assert 1 + 4 == 5 and Rational(16, 4) - 3 == 1
    assert Rational(1, 4) - 1 == Rational(-3, 4)
    assert abs(math.hypot(4 + 4, 6) - math.hypot(4 - 4, 6)) == 4 and 4 + 12 == 16 and Rational(16, 4) - Rational(36, 12) == 1
    assert 9 * 1 - 1 == 8
    # 軌跡
    for _ in range(300):
        th = random.uniform(0, 2 * math.pi); X, Y = 3 * math.cos(th), math.sqrt(8) * math.sin(th)
        r = math.hypot(X + 1, Y) - 1
        assert 1 - 1e-9 <= r <= 3 + 1e-9 and close(math.hypot(X - 1, Y), 5 - r)
    assert close(math.hypot(0 + 1, math.sqrt(8)) - 1, 2)
    for _ in range(300):
        u = random.uniform(-3, 3); X, Y = 0.5 * math.cosh(u), math.sqrt(35) / 2 * math.sinh(u)
        assert close(4 * X * X - 4 * Y * Y / 35, 1)
        r = math.hypot(X - 3, Y) - 1
        assert r > 0 and close(math.hypot(X + 3, Y), 2 + r)


# ---------------------------------------------------------------- 節2
def fig_rot():
    f = Fig(-2.2, 2.2, -2.0, 2.0, 32)
    f.lineq(1, -1, 0, col=GRAY, w=0.8, dash="3 3")
    f.axes()
    f.curve(ell(2, 1, rot=math.pi / 4), 0, 2 * math.pi)
    c = math.sqrt(6) / 2
    f.dot(c, c, col=RED); f.dot(-c, -c, col=RED)
    f.text(c, c, "F", 5, 3); f.text(-c, -c, "F′", 5, 9)
    f.text(1.9, 1.95, "y=x", -2, 10, it=True, size=10, anchor="end")
    return f.svg()


SEC.append({"title": r"2次曲線の平行移動と回転",
"base": r"""・曲線 $F(x,\ y)=0$ を $x$ 軸方向に $p$，$y$ 軸方向に $q$ だけ平行移動した曲線は $F(x-p,\ y-q)=0$。$ax^2+by^2+cx+dy+e=0$ の形の式は、平方完成して標準形を平行移動した形に直す。焦点・頂点・漸近線も同じだけ平行移動する。<br>
・点 $(X,\ Y)$ を原点のまわりに $\theta$ 回転した点は $(X\cos\theta-Y\sin\theta,\ X\sin\theta+Y\cos\theta)$。<br>
・曲線 $F(x,\ y)=0$ を原点のまわりに $\theta$ 回転した曲線は $F(x\cos\theta+y\sin\theta,\ -x\sin\theta+y\cos\theta)=0$（点 $(x,\ y)$ を $-\theta$ 回転した点がもとの曲線上にある）。$xy$ の項を含む2次曲線は、回転して $xy$ の項を消し、標準形にする。""",
"items": [
 {"lv": 1, "title": r"平行移動した2次曲線（平方完成）",
  "q": r"方程式 $4x^2+9y^2-16x+54y+61=0$ はどのような曲線を表すか。また、その焦点の座標を求めよ。",
  "hint": r"$x,\ y$ それぞれについて平方完成し、標準形 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ を平行移動した形に直す。焦点も同じだけ平行移動する。",
  "sol": r"$4(x^2-4x)+9(y^2+6y)+61=0$<br>$4(x-2)^2-16+9(y+3)^2-81+61=0$<br>$4(x-2)^2+9(y+3)^2=36$<br>よって　$\dfrac{(x-2)^2}{9}+\dfrac{(y+3)^2}{4}=1$<br>"
         r"これは楕円 $\dfrac{x^2}{9}+\dfrac{y^2}{4}=1$ を $x$ 軸方向に $2$，$y$ 軸方向に $-3$ だけ平行移動したもので、<b>中心 $(2,\ -3)$，長軸の長さ $6$，短軸の長さ $4$ の楕円</b>である。<br>"
         r"もとの楕円の焦点 $(\pm\sqrt5,\ 0)$ を同じだけ移して　焦点 $\boldsymbol{(2+\sqrt5,\ -3),\ (2-\sqrt5,\ -3)}$",
  "note": r"平方完成した結果、右辺が $0$ なら1点、負なら表す図形がない。たとえば $4x^2+9y^2-16x+54y+97=0$ は $4(x-2)^2+9(y+3)^2=0$ となり、点 $(2,\ -3)$ だけを表す。",
  "ex": r"方程式 $x^2-4y^2+6x+8y+1=0$ はどのような曲線を表すか。焦点の座標と漸近線の方程式も求めよ。",
  "exa": r"双曲線 $\dfrac{(x+3)^2}{4}-(y-1)^2=1$（中心 $(-3,\ 1)$）；焦点 $(-3\pm\sqrt5,\ 1)$，漸近線 $y-1=\pm\dfrac12(x+3)$"},
 {"lv": 2, "title": r"焦点・準線などから方程式を求める（平行移動）",
  "q": r"(1) 焦点が $(2,\ 1)$，準線が直線 $x=-2$ である放物線の方程式を求めよ。<br>(2) 2つの焦点が $(1,\ 2)$，$(1,\ -4)$ で、長軸の長さが $10$ である楕円の方程式を求めよ。",
  "hint": r"(1) 定義から直接式を立てる。(2) 中心（2焦点の中点）を求め、中心が原点にある楕円を平行移動したものと考える。",
  "sol": r"(1) 放物線上の点 $(x,\ y)$ について $\sqrt{(x-2)^2+(y-1)^2}=|x+2|$。<br>2乗して $(y-1)^2=(x+2)^2-(x-2)^2=8x$<br>よって　$\boldsymbol{(y-1)^2=8x}$<br>"
         r"(2) 中心は2焦点の中点 $(1,\ -1)$ である。焦点は中心から $y$ 軸方向に $c=3$ だけ離れているから、長軸は $y$ 軸に平行で、$a=5$，$b^2=a^2-c^2=16$。<br>"
         r"中心が原点のときは $\dfrac{x^2}{16}+\dfrac{y^2}{25}=1$ であるから、これを平行移動して<br>$\boldsymbol{\dfrac{(x-1)^2}{16}+\dfrac{(y+1)^2}{25}=1}$",
  "note": r"(1) の放物線は $y^2=8x$（焦点 $(2,\ 0)$，準線 $x=-2$）を $y$ 軸方向に $1$ だけ平行移動したもの。頂点は、焦点から準線に下ろした垂線の中点 $(0,\ 1)$ である。",
  "ex": r"(1) 焦点が $(1,\ 3)$，準線が直線 $y=-1$ である放物線の方程式を求めよ。<br>(2) 2つの焦点が $(-1,\ 1)$，$(5,\ 1)$ で、頂点の1つが $(4,\ 1)$ である双曲線の方程式を求めよ。",
  "exa": r"(1) $(x-1)^2=8(y-1)$　(2) $\dfrac{(x-2)^2}{4}-\dfrac{(y-1)^2}{5}=1$"},
 {"lv": 3, "title": r"曲線の回転と $xy$ の項の消去",
  "q": r"曲線 $5x^2-6xy+5y^2=8$ を原点のまわりに $\dfrac\pi4$ だけ回転した曲線の方程式を求めよ。また、それを利用して、もとの曲線の焦点の座標を求めよ。",
  "hint": r"回転後の曲線上の点 $(x,\ y)$ を逆に $-\dfrac\pi4$ 回転した点が、もとの曲線上にあると考えて代入する。$\dfrac\pi4$ の回転では $x^2+y^2$ が変わらないことを使うと計算が速い。",
  "sol": fig_rot() + r"回転後の曲線上の点を $(x,\ y)$ とし、これを原点のまわりに $-\dfrac\pi4$ 回転した点を $(u,\ v)$ とすると<br>"
         r"$u=\dfrac{x+y}{\sqrt2}$，$v=\dfrac{-x+y}{\sqrt2}$<br>$(u,\ v)$ がもとの曲線上にあるから $5u^2-6uv+5v^2=8$。<br>"
         r"$u^2+v^2=x^2+y^2$，$uv=\dfrac{y^2-x^2}{2}$ より<br>$5(x^2+y^2)-3(y^2-x^2)=8$，$8x^2+2y^2=8$<br>よって　$\boldsymbol{x^2+\dfrac{y^2}{4}=1}$<br>"
         r"これは焦点が $(0,\ \pm\sqrt3)$ の楕円である。もとの曲線はこれを $-\dfrac\pi4$ 回転したものだから、焦点も $(0,\ \sqrt3)$ を $-\dfrac\pi4$ 回転した点 $\left(\sqrt3\sin\dfrac\pi4,\ \sqrt3\cos\dfrac\pi4\right)$ と、その原点対称の点になる。<br>"
         r"焦点 $\boldsymbol{\left(\dfrac{\sqrt6}2,\ \dfrac{\sqrt6}2\right),\ \left(-\dfrac{\sqrt6}2,\ -\dfrac{\sqrt6}2\right)}$",
  "note": r"もとの楕円は直線 $y=x$ の方向に長軸（長さ $4$），$y=-x$ の方向に短軸（長さ $2$）をもつ（右の図）。一般に $Ax^2+Bxy+Cy^2=k$ に $x=u\cos\theta-v\sin\theta$，$y=u\sin\theta+v\cos\theta$ を代入すると $uv$ の係数は $B\cos2\theta-(A-C)\sin2\theta$ になるので、これが $0$ になる $\theta$ を選べば $xy$ の項が消える。$A=C$ なら $\theta=\pm\dfrac\pi4$。",
  "ex": r"曲線 $7x^2-6\sqrt3xy+13y^2=16$ を原点のまわりに $-\dfrac\pi6$ だけ回転した曲線の方程式を求め、もとの曲線の焦点の座標を求めよ。",
  "exa": r"$\dfrac{x^2}{4}+y^2=1$；焦点 $\left(\dfrac32,\ \dfrac{\sqrt3}2\right),\ \left(-\dfrac32,\ -\dfrac{\sqrt3}2\right)$"},
 {"lv": 4, "title": r"直角双曲線 $xy=1$ 上の三角形の垂心",
  "q": r"双曲線 $xy=1$ 上の相異なる3点 $\mathrm{A},\ \mathrm{B},\ \mathrm{C}$ を頂点とする三角形の垂心 $\mathrm{H}$ も、この双曲線上にあることを示せ。",
  "hint": r"$xy=1$ は $x^2-y^2=2$ を $\dfrac\pi4$ 回転した双曲線（漸近線が直交する直角双曲線）である。点を $\left(a,\ \dfrac1a\right)$ と1文字で表すと、2点を結ぶ直線の傾きが $-\dfrac1{ab}$ と簡単になる。2本の垂線の交点を求めればよい。",
  "sol": r"$\mathrm{A}\left(a,\ \dfrac1a\right)$，$\mathrm{B}\left(b,\ \dfrac1b\right)$，$\mathrm{C}\left(c,\ \dfrac1c\right)$（$a,\ b,\ c$ は相異なる $0$ でない実数）とおく。<br>"
         r"直線 $\mathrm{BC}$ の傾きは　$\dfrac{\frac1c-\frac1b}{c-b}=\dfrac{b-c}{bc(c-b)}=-\dfrac1{bc}$<br>"
         r"よって、$\mathrm{A}$ を通り $\mathrm{BC}$ に垂直な直線は傾き $bc$ で　$y=bc(x-a)+\dfrac1a$ …①<br>"
         r"同様に、$\mathrm{B}$ を通り $\mathrm{CA}$ に垂直な直線は　$y=ca(x-b)+\dfrac1b$ …②<br>"
         r"①－②より　$0=c(b-a)x+\dfrac1a-\dfrac1b=c(b-a)x+\dfrac{b-a}{ab}$<br>"
         r"$a\neq b$，$c\neq0$ より　$x=-\dfrac1{abc}$<br>"
         r"①に代入して　$y=bc\left(-\dfrac1{abc}-a\right)+\dfrac1a=-\dfrac1a-abc+\dfrac1a=-abc$<br>"
         r"垂心 $\mathrm{H}$ は①と②の交点であるから $\mathrm{H}\left(-\dfrac1{abc},\ -abc\right)$。<br>"
         r"$\left(-\dfrac1{abc}\right)\cdot(-abc)=1$ であるから、$\mathrm{H}$ は双曲線 $xy=1$ 上にある。（証明終わり）",
  "note": r"$\mathrm{H}$ の座標は $a,\ b,\ c$ について対称な式なので、3本目の垂線を使っても同じ点になる。3点が同じ枝（たとえば $a,\ b,\ c>0$）にあれば $abc>0$ となり、$\mathrm{H}$ は第3象限、つまりもう一方の枝にある。$\angle\mathrm{A}=90^\circ$ なら $\mathrm{H}=\mathrm{A}$ で、このとき $a^2bc=-1$ が成り立つ。",
  "ex": r"3点 $\mathrm{A}(1,\ 1)$，$\mathrm{B}\left(2,\ \dfrac12\right)$，$\mathrm{C}\left(3,\ \dfrac13\right)$ を頂点とする三角形の垂心の座標を求めよ。",
  "exa": r"$\left(-\dfrac16,\ -6\right)$"},
]})


def _orth(A, B, C):
    """垂心（sympy で厳密）"""
    x, y = symbols("x y")
    e1 = (x - A[0]) * (C[0] - B[0]) + (y - A[1]) * (C[1] - B[1])
    e2 = (x - B[0]) * (A[0] - C[0]) + (y - B[1]) * (A[1] - C[1])
    s = solve([e1, e2], [x, y], dict=True)[0]
    return simplify(s[x]), simplify(s[y])


def _v2():
    x, y, u, v = symbols("x y u v")
    assert expand(4*(x-2)**2 + 9*(y+3)**2 - 36) == 4*x**2 + 9*y**2 - 16*x + 54*y + 61
    assert expand(4*(x-2)**2 + 9*(y+3)**2) == 4*x**2 + 9*y**2 - 16*x + 54*y + 97
    assert expand((x+3)**2 - 4*(y-1)**2 - 4) == x**2 - 4*y**2 + 6*x + 8*y + 1
    # 練習：中心(-3,1), a=2, b=1, c=√5
    assert sqrt(4 + 1) == sqrt(5)
    assert expand((x-2)**2 + (y-1)**2 - (x+2)**2 - ((y-1)**2 - 8*x)) == 0
    assert expand((x-1)**2 + (y-3)**2 - (y+1)**2 - ((x-1)**2 - 8*(y-1))) == 0
    for _ in range(100):
        th = random.uniform(0, 2 * math.pi)
        X, Y = 1 + 4 * math.cos(th), -1 + 5 * math.sin(th)
        assert close(math.hypot(X - 1, Y - 2) + math.hypot(X - 1, Y + 4), 10)
        w = random.uniform(-2, 2)
        X, Y = 2 + 2 * math.cosh(w), 1 + math.sqrt(5) * math.sinh(w)
        assert close(math.hypot(X + 1, Y - 1) - math.hypot(X - 5, Y - 1), 4)
    # 回転（例題）
    U, V = (x + y) / sqrt(2), (-x + y) / sqrt(2)
    assert expand(5*U**2 - 6*U*V + 5*V**2 - 8 - (8*x**2 + 2*y**2 - 8)) == 0
    c = math.sqrt(6) / 2
    for _ in range(100):
        th = random.uniform(0, 2 * math.pi); X0, Y0 = math.cos(th), 2 * math.sin(th)   # x^2+y^2/4=1
        X, Y = X0 * math.cos(-math.pi/4) - Y0 * math.sin(-math.pi/4), X0 * math.sin(-math.pi/4) + Y0 * math.cos(-math.pi/4)
        assert close(5*X*X - 6*X*Y + 5*Y*Y, 8)
        assert close(math.hypot(X - c, Y - c) + math.hypot(X + c, Y + c), 4)
    # 回転（練習）：-π/6 回転 → 点 (x,y) を +π/6 回転した点がもとの曲線上
    cs, sn = sqrt(3) / 2, Rational(1, 2)
    U, V = x * cs - y * sn, x * sn + y * cs
    assert expand(7*U**2 - 6*sqrt(3)*U*V + 13*V**2 - 16 - (4*x**2 + 16*y**2 - 16)) == 0
    for _ in range(100):
        th = random.uniform(0, 2 * math.pi); X0, Y0 = 2 * math.cos(th), math.sin(th)
        a = math.pi / 6
        X, Y = X0 * math.cos(a) - Y0 * math.sin(a), X0 * math.sin(a) + Y0 * math.cos(a)
        assert close(7*X*X - 6*math.sqrt(3)*X*Y + 13*Y*Y, 16)
        assert close(math.hypot(X - 1.5, Y - math.sqrt(3)/2) + math.hypot(X + 1.5, Y + math.sqrt(3)/2), 4)
    # 一般の uv 係数
    A_, B_, C_, t = symbols("A B C t")
    Q = expand(A_*(u*cos(t) - v*sin(t))**2 + B_*(u*cos(t) - v*sin(t))*(u*sin(t) + v*cos(t)) + C_*(u*sin(t) + v*cos(t))**2)
    co = Q.coeff(u, 1).coeff(v, 1)
    assert simplify(co - (B_*cos(2*t) - (A_ - C_)*sin(2*t))) == 0
    # 垂心
    a, b, cc = symbols("a b c", nonzero=True)
    for _ in range(20):
        p, q, r = random.sample([Rational(k, 3) for k in range(-12, 13) if k != 0], 3)
        H = _orth((p, 1/p), (q, 1/q), (r, 1/r))
        assert H == (-1/(p*q*r), -p*q*r) and simplify(H[0]*H[1]) == 1
    assert _orth((1, 1), (2, Rational(1, 2)), (3, Rational(1, 3))) == (Rational(-1, 6), -6)

# ---------------------------------------------------------------- 節3
def fig_tan_ext():
    f = Fig(-2.5, 2.8, -1.4, 2.5, 36)
    f.axes()
    f.curve(ell(2, 1), 0, 2 * math.pi)
    f.lineq(1, 0, 2, col=RED, w=1.1, dash=None)
    f.lineq(3, -8, -10, col=RED, w=1.1, dash=None)
    f.dot(2, 2); f.text(2, 2, "A", 5, -2)
    f.dot(2, 0, col=RED); f.dot(-1.2, 0.8, col=RED)
    f.text(2, 0, "2", 4, 12, size=10)
    return f.svg()


def fig_asym():
    f = Fig(-0.9, 5.0, -1.3, 2.6, 36)
    f.poly([(0, 0), (4.4503, 2.2252), (0.8986, -0.4493)], op=0.55)
    f.lineq(1, -2, 0); f.lineq(1, 2, 0)
    f.axes()
    f.curve(lambda t: (2 * math.cosh(t), math.sinh(t)), -1.6, 1.6)
    x0, y0 = 2 * math.cosh(0.8), math.sinh(0.8)
    f.lineq(x0 / 4, -y0, 1, col=RED, w=1.1, dash=None)
    f.dot(x0, y0, col=RED); f.text(x0, y0, "P", 5, 10)
    f.dot(4.4503, 2.2252); f.text(4.4503, 2.2252, "Q", -12, -3)
    f.dot(0.8986, -0.4493); f.text(0.8986, -0.4493, "R", -4, 13)
    return f.svg()


def _g15(y):
    return 4 * y * y + y - 4


def fig_kg():
    f = Fig(-1.35, 1.45, -4.45, 1.6, 64, sy=26)
    for k, lab in ((1, "1"), (-1, "−1"), (-65 / 16, "−65/16")):
        f.seg((-1.3, k), (1.3, k), GRAY, 0.7, "3 2")
        f.text(0, k, lab, -3, -3 if k > -4 else 12, size=9.5, anchor="end")
    f.seg((-1, -4.3), (-1, 1.3), GRAY, 0.6, "2 2"); f.seg((1, -4.3), (1, 1.3), GRAY, 0.6, "2 2")
    f.axes("y", "k", o=False)
    f.curve(lambda t: (t, _g15(t)), -1, 1, col=BLUE, w=1.6)
    f.dot(-1, -1, col=BLUE, r=2.6); f.dot(1, 1, col=BLUE, r=2.6)
    f.text(-1, 0, "−1", -2, 12, size=9.5, anchor="end"); f.text(1, 0, "1", 3, 12, size=9.5)
    return f.svg()


def _rect_vertices(a, b, ph):
    p1 = math.sqrt(a*a*math.cos(ph)**2 + b*b*math.sin(ph)**2)
    p2 = math.sqrt(a*a*math.sin(ph)**2 + b*b*math.cos(ph)**2)
    V = []
    for s1, s2 in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        u, v = s1 * p1, s2 * p2            # x cosφ + y sinφ = u, -x sinφ + y cosφ = v
        V.append((u * math.cos(ph) - v * math.sin(ph), u * math.sin(ph) + v * math.cos(ph)))
    return V, p1, p2


def fig_rect():
    f = Fig(-2.55, 2.55, -2.45, 2.45, 34)
    f.circle((0, 0), math.sqrt(5), col=GRAY, w=0.9, dash="3 2")
    V, _, _ = _rect_vertices(2, 1, math.pi / 6)
    f.poly(V, op=0.35, col=RED, w=1.1)
    f.axes()
    f.curve(ell(2, 1), 0, 2 * math.pi, w=1.5)
    for q in V:
        f.dot(*q, col=RED)
    return f.svg()


SEC.append({"title": r"2次曲線と直線（共有点・接線・弦）",
"base": r"""・2次曲線と直線の共有点は、連立して1文字を消去した方程式の実数解に対応する。2次方程式になれば判別式 $D$ で判定：$D>0$ なら2点、$D=0$ なら接する、$D<0$ なら共有点なし。双曲線で2次の係数が $0$ になる（直線が漸近線に平行な）ときは1点で交わる。<br>
・曲線上の点 $(x_1,\ y_1)$ における接線：楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ なら $\dfrac{x_1x}{a^2}+\dfrac{y_1y}{b^2}=1$，双曲線 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=\pm1$ なら $\dfrac{x_1x}{a^2}-\dfrac{y_1y}{b^2}=\pm1$，放物線 $y^2=4px$ なら $y_1y=2p(x+x_1)$。<br>
・弦の中点は、解と係数の関係で $x_1+x_2$ を求めて得る。傾き $m$ の直線上の弦の長さは $\sqrt{1+m^2}\,|x_1-x_2|$。""",
"items": [
 {"lv": 1, "title": r"曲線上の点における接線",
  "q": r"次の曲線上の点における接線の方程式を求めよ。<br>(1) 楕円 $\dfrac{x^2}{8}+\dfrac{y^2}{2}=1$，点 $(2,\ 1)$<br>(2) 双曲線 $x^2-\dfrac{y^2}{4}=1$，点 $(\sqrt2,\ 2)$<br>(3) 放物線 $y^2=8x$，点 $(2,\ 4)$",
  "hint": r"接線の公式は、曲線の式の $x^2$ を $x_1x$ に、$y^2$ を $y_1y$ に（放物線 $y^2=4px$ では $x$ を $\dfrac{x+x_1}2$ に）置き換えた形。点が曲線上にあることを先に確かめる。",
  "sol": r"(1) $\dfrac48+\dfrac12=1$ より点は楕円上にある。接線は $\dfrac{2x}{8}+\dfrac{1\cdot y}{2}=1$，すなわち　$\boldsymbol{x+2y=4}$<br>"
         r"(2) $2-\dfrac44=1$ より点は双曲線上にある。接線は $\sqrt2x-\dfrac{2y}{4}=1$，すなわち　$\boldsymbol{y=2\sqrt2x-2}$<br>"
         r"(3) $4^2=8\cdot2$ より点は放物線上にある。$y^2=4\cdot2x$ で $p=2$ だから、接線は $4y=2\cdot2(x+2)$，すなわち　$\boldsymbol{y=x+2}$",
  "note": r"楕円の接線の公式は、円 $x^2+y^2=a^2$ の接線 $x_1x+y_1y=a^2$ を $y$ 軸方向に $\dfrac ba$ 倍すると得られる（拡大・縮小で「1点だけを共有する」関係は保たれる）。(1) を確かめるには、$x=4-2y$ を楕円の式に代入して $(y-1)^2=0$ と重解になることを見ればよい。",
  "ex": r"次の曲線上の点における接線の方程式を求めよ。<br>(1) 楕円 $\dfrac{x^2}{12}+\dfrac{y^2}{4}=1$，点 $(3,\ -1)$　(2) 放物線 $x^2=4y$，点 $(4,\ 4)$",
  "exa": r"(1) $x-y=4$　(2) $y=2x-4$"},
 {"lv": 2, "title": r"双曲線と直線の共有点の個数",
  "q": r"双曲線 $x^2-4y^2=4$ と直線 $y=mx+1$ の共有点の個数を、定数 $m$ の値によって調べよ。",
  "hint": r"代入して $x$ の方程式にする。$x^2$ の係数 $1-4m^2$ が $0$ になる場合（直線が漸近線に平行）は1次方程式になるので、判別式を使う前に分けて考える。",
  "sol": r"代入して $x^2-4(mx+1)^2=4$，すなわち　$(1-4m^2)x^2-8mx-8=0$ …①<br>"
         r"[1] $1-4m^2=0$，すなわち $m=\pm\dfrac12$ のとき<br>①は $-8mx-8=0$ となり、解は $x=-\dfrac1m$ の1個。共有点は1個。<br>"
         r"[2] $m\neq\pm\dfrac12$ のとき<br>①の判別式を $D$ とすると　$\dfrac D4=16m^2+8(1-4m^2)=8(1-2m^2)$<br>"
         r"$D>0\iff-\dfrac1{\sqrt2}<m<\dfrac1{\sqrt2}$ で2個，$D=0\iff m=\pm\dfrac1{\sqrt2}$ で1個（接する），$D<0$ で0個。<br>"
         r"$\dfrac12<\dfrac1{\sqrt2}$ に注意してまとめると<br>"
         r"$\boldsymbol{-\dfrac1{\sqrt2}<m<\dfrac1{\sqrt2}}$ かつ $\boldsymbol{m\neq\pm\dfrac12}$ のとき $\boldsymbol{2}$ 個<br>"
         r"$\boldsymbol{m=\pm\dfrac12,\ \pm\dfrac1{\sqrt2}}$ のとき $\boldsymbol{1}$ 個<br>"
         r"$\boldsymbol{m<-\dfrac1{\sqrt2},\ \dfrac1{\sqrt2}<m}$ のとき $\boldsymbol{0}$ 個",
  "note": r"$m=\pm\dfrac12$ のとき、直線は漸近線 $y=\pm\dfrac12x$ に平行で、双曲線と1点で交わるが接してはいない。双曲線では「共有点が1個 ⇒ 接する」とは限らない。",
  "ex": r"楕円 $x^2+4y^2=4$ と直線 $y=mx+2$ の共有点の個数を、定数 $m$ の値によって調べよ。",
  "exa": r"$m<-\dfrac{\sqrt3}2,\ \dfrac{\sqrt3}2<m$ のとき2個；$m=\pm\dfrac{\sqrt3}2$ のとき1個；$-\dfrac{\sqrt3}2<m<\dfrac{\sqrt3}2$ のとき0個"},
 {"lv": 2, "title": r"曲線外の点から引いた接線",
  "q": r"点 $\mathrm{A}(2,\ 2)$ から楕円 $\dfrac{x^2}{4}+y^2=1$ に引いた接線の方程式と、接点の座標を求めよ。",
  "hint": r"接点を $(x_1,\ y_1)$ とおき、接線の公式 $\dfrac{x_1x}{4}+y_1y=1$ が $\mathrm{A}$ を通る条件と、接点が楕円上にある条件を連立する。傾きを $m$ とおく方法では、$y$ 軸に平行な接線を見落としやすい。",
  "sol": fig_tan_ext() + r"接点を $(x_1,\ y_1)$ とすると、接線は $\dfrac{x_1x}{4}+y_1y=1$。<br>"
         r"これが $\mathrm{A}(2,\ 2)$ を通るから $\dfrac{x_1}{2}+2y_1=1$，よって $x_1=2-4y_1$ …①<br>"
         r"また $\dfrac{x_1^2}{4}+y_1^2=1$ …②<br>"
         r"①を②に代入して $(1-2y_1)^2+y_1^2=1$，$5y_1^2-4y_1=0$<br>"
         r"よって $y_1=0,\ \dfrac45$，①より $x_1=2,\ -\dfrac65$。<br>"
         r"接点 $(2,\ 0)$ のとき，接線は $\dfrac{2x}{4}=1$ より　$\boldsymbol{x=2}$<br>"
         r"接点 $\left(-\dfrac65,\ \dfrac45\right)$ のとき，接線は $-\dfrac{3x}{10}+\dfrac{4y}{5}=1$ より　$\boldsymbol{3x-8y+10=0}$<br>"
         r"接点は　$\boldsymbol{(2,\ 0),\ \left(-\dfrac65,\ \dfrac45\right)}$",
  "note": r"傾きを $m$ として $y-2=m(x-2)$ を楕円の式に代入し、重解条件を立てると $\dfrac D4=32m-12=0$ となって $m=\dfrac38$ しか得られない。$x=2$ は傾きをもたない接線なので、別に調べる必要がある。",
  "ex": r"点 $(0,\ 2)$ から双曲線 $x^2-y^2=1$ に引いた接線の方程式を求めよ。",
  "exa": r"$y=\sqrt5x+2,\ y=-\sqrt5x+2$"},
 {"lv": 3, "title": r"弦の中点の軌跡と弦の長さの最大",
  "q": r"楕円 $x^2+4y^2=4$ と直線 $y=x+k$ が異なる2点 $\mathrm{P},\ \mathrm{Q}$ で交わるとする。<br>(1) 定数 $k$ の値の範囲を求めよ。<br>(2) $k$ が (1) の範囲を動くとき、線分 $\mathrm{PQ}$ の中点 $\mathrm{M}$ の軌跡を求めよ。<br>(3) 線分 $\mathrm{PQ}$ の長さの最大値を求めよ。",
  "hint": r"交点の $x$ 座標 $x_1,\ x_2$ は2次方程式の2解。中点は解と係数の関係で $\dfrac{x_1+x_2}{2}$ を求め、$k$ を消去する（$k$ の範囲から $x$ の範囲が制限される）。弦の長さは $\sqrt{1+1^2}\,|x_1-x_2|$ で、$(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2$。",
  "sol": r"代入して $x^2+4(x+k)^2=4$，すなわち　$5x^2+8kx+4k^2-4=0$ …①<br>①の2解を $x_1,\ x_2$ とする。<br>"
         r"(1) ①の判別式を $D$ とすると　$\dfrac D4=16k^2-5(4k^2-4)=4(5-k^2)>0$<br>よって　$\boldsymbol{-\sqrt5<k<\sqrt5}$<br>"
         r"(2) $\mathrm{M}(X,\ Y)$ とすると、$x_1+x_2=-\dfrac{8k}5$ より $X=-\dfrac{4k}5$，$Y=X+k=\dfrac k5$。<br>"
         r"$k=5Y$ を代入して $X=-4Y$。また $-\sqrt5<k<\sqrt5$ より $-\dfrac{4\sqrt5}5<X<\dfrac{4\sqrt5}5$。<br>"
         r"求める軌跡は　<b>直線 $y=-\dfrac14x$ の $-\dfrac{4\sqrt5}{5}<x<\dfrac{4\sqrt5}{5}$ の部分</b><br>"
         r"(3) $(x_1-x_2)^2=(x_1+x_2)^2-4x_1x_2=\dfrac{64k^2}{25}-\dfrac{4(4k^2-4)}{5}=\dfrac{16(5-k^2)}{25}$<br>"
         r"$\mathrm{PQ}^2=(1+1^2)(x_1-x_2)^2=\dfrac{32(5-k^2)}{25}$<br>"
         r"これは $k=0$ のとき最大で、最大値は　$\mathrm{PQ}=\sqrt{\dfrac{160}{25}}=\boldsymbol{\dfrac{4\sqrt{10}}5}$",
  "note": r"中点の軌跡は楕円の中心（原点）を通る直線になる。一般に楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ の傾き $m$（$m\neq0$）の平行な弦の中点は、直線 $y=-\dfrac{b^2}{a^2m}x$ 上にある。",
  "ex": r"楕円 $2x^2+y^2=2$ と直線 $y=2x+k$ が異なる2点 $\mathrm{P},\ \mathrm{Q}$ で交わるとき、$k$ の値の範囲、線分 $\mathrm{PQ}$ の中点の軌跡、$\mathrm{PQ}$ の長さの最大値を求めよ。",
  "exa": r"$-\sqrt6<k<\sqrt6$；直線 $y=-x$ の $-\dfrac{\sqrt6}3<x<\dfrac{\sqrt6}3$ の部分；$\dfrac{2\sqrt{15}}3$"},
 {"lv": 3, "title": r"双曲線の接線と漸近線が作る三角形",
  "q": r"双曲線 $\dfrac{x^2}{4}-y^2=1$ 上の点 $\mathrm{P}(x_0,\ y_0)$ における接線と、2本の漸近線との交点を $\mathrm{Q},\ \mathrm{R}$ とする。原点を $\mathrm{O}$ とするとき、次のことを示せ。<br>(1) $\mathrm{P}$ は線分 $\mathrm{QR}$ の中点である。<br>(2) $\triangle\mathrm{OQR}$ の面積は $\mathrm{P}$ の位置によらず一定である。",
  "hint": r"接線 $\dfrac{x_0x}{4}-y_0y=1$ と漸近線 $y=\pm\dfrac12x$ の交点を求める。$x_0^2-4y_0^2=4$，すなわち $(x_0-2y_0)(x_0+2y_0)=4$ を使うと、交点の座標が簡単になる。",
  "sol": fig_asym() + r"接線は　$\dfrac{x_0x}{4}-y_0y=1$ …①<br>$\mathrm{P}$ は双曲線上にあるから<br>$(x_0-2y_0)(x_0+2y_0)=x_0^2-4y_0^2=4$ …②<br>特に $x_0\pm2y_0\neq0$ である。<br>"
         r"漸近線 $y=\dfrac12x$ と①の交点は、$\dfrac{(x_0-2y_0)x}{4}=1$ より $x=\dfrac4{x_0-2y_0}=x_0+2y_0$（②による）。よって $\mathrm{Q}\left(x_0+2y_0,\ \dfrac{x_0+2y_0}2\right)$。<br>"
         r"漸近線 $y=-\dfrac12x$ と①の交点は、同様に $x=\dfrac4{x_0+2y_0}=x_0-2y_0$ で $\mathrm{R}\left(x_0-2y_0,\ -\dfrac{x_0-2y_0}2\right)$。<br>"
         r"(1) 線分 $\mathrm{QR}$ の中点の座標は $\left(\dfrac{(x_0+2y_0)+(x_0-2y_0)}{2},\ \dfrac{(x_0+2y_0)-(x_0-2y_0)}{4}\right)=(x_0,\ y_0)$ で、$\mathrm{P}$ と一致する。<br>"
         r"(2) $\triangle\mathrm{OQR}=\dfrac12\left|(x_0+2y_0)\cdot\left(-\dfrac{x_0-2y_0}2\right)-(x_0-2y_0)\cdot\dfrac{x_0+2y_0}2\right|$<br>$=\dfrac12\left|-(x_0^2-4y_0^2)\right|=\dfrac12\cdot4=2$<br>"
         r"よって、面積は $2$ で一定である。（証明終わり）",
  "note": r"一般に双曲線 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$ では、接線と2本の漸近線で囲まれる三角形の面積はつねに $ab$ になる。(1) は「接点は、接線のうち2本の漸近線の間にはさまれた部分の中点」と言い換えられる。",
  "ex": r"双曲線 $\dfrac{x^2}{9}-\dfrac{y^2}{4}=1$ 上の点における接線と2本の漸近線で囲まれる三角形の面積を求めよ。",
  "exa": r"$6$"},
 {"lv": 4, "title": r"楕円と放物線の共有点の個数（文字定数の分離）",
  "q": r"楕円 $\dfrac{x^2}{4}+y^2=1$ と放物線 $y=x^2+k$ の共有点の個数を、定数 $k$ の値によって調べよ。",
  "hint": r"$x^2=y-k$ を使って $x$ を消去すると $y$ の2次方程式になる。ただし、$y$ の値1つに対して共有点が2個（$x=\pm$ の2つ）か1個（$x=0$）かに注意する。$k$ を分離して、$k=g(y)$ のグラフと直線 $k=c$ の共有点で考える。",
  "sol": fig_kg() + r"共有点 $(x,\ y)$ は　$x^2=y-k$ …①，$\dfrac{x^2}4+y^2=1$ …②<br>を満たす。②より $x^2=4(1-y^2)$ …③ であるから、①と③より<br>"
         r"$k=4y^2+y-4$ …④　かつ　$x^2=4(1-y^2)$<br>"
         r"逆に、④を満たす $y$ で $-1\leqq y\leqq1$ のものに対し、$x=\pm2\sqrt{1-y^2}$ とすれば①②が成り立つ。<br>"
         r"よって、④を満たす $y$（$-1\leqq y\leqq1$）1つにつき、$-1<y<1$ なら共有点は2個，$y=\pm1$ なら $x=0$ の1個である。<br>"
         r"$g(y)=4y^2+y-4=4\left(y+\dfrac18\right)^2-\dfrac{65}{16}$ とおくと<br>$g(-1)=-1$，$g(1)=1$，$g\left(-\dfrac18\right)=-\dfrac{65}{16}$<br>"
         r"$-1\leqq y\leqq1$ における $k=g(y)$ のグラフ（右の図）と直線 $k=c$ の共有点を調べて、共有点の個数は<br>"
         r"$k<-\dfrac{65}{16}$ のとき $\boldsymbol{0}$ 個<br>"
         r"$k=-\dfrac{65}{16}$ のとき（$y=-\dfrac18$）$\boldsymbol{2}$ 個<br>"
         r"$-\dfrac{65}{16}<k<-1$ のとき（$-1<y<1$ の $y$ が2つ）$\boldsymbol{4}$ 個<br>"
         r"$k=-1$ のとき（$y=-1,\ \dfrac34$）$\boldsymbol{3}$ 個<br>"
         r"$-1<k<1$ のとき（$-1<y<1$ の $y$ が1つ）$\boldsymbol{2}$ 個<br>"
         r"$k=1$ のとき（$y=1$）$\boldsymbol{1}$ 個<br>"
         r"$1<k$ のとき $\boldsymbol{0}$ 個",
  "note": r"$y$ の値1つに共有点が何個対応するかを見落とすと、$k=-1$ や $k=1$ で個数を誤る。また①の $y-k\geqq0$ という条件は、④から $y-k=4(1-y^2)$ となるので、$-1\leqq y\leqq1$ に含まれている。",
  "ex": r"楕円 $\dfrac{x^2}{2}+y^2=1$ と放物線 $y=x^2+k$ の共有点の個数を、定数 $k$ の値によって調べよ。",
  "exa": r"$k<-\dfrac{17}8$ で0個，$k=-\dfrac{17}8$ で2個，$-\dfrac{17}8<k<-1$ で4個，$k=-1$ で3個，$-1<k<1$ で2個，$k=1$ で1個，$1<k$ で0個"},
 {"lv": 5, "title": r"楕円に外接する長方形（直交する接線・面積と周の範囲）",
  "q": r"$a>b>0$ とする。楕円 $E:\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ に外接する長方形（4辺を含む直線がすべて $E$ に接する長方形）について、次の問いに答えよ。<br>"
       r"(1) $p>0$ とする。直線 $x\cos\varphi+y\sin\varphi=p$ が $E$ に接するための条件は $p^2=a^2\cos^2\varphi+b^2\sin^2\varphi$ であることを示せ。<br>"
       r"(2) 長方形の4つの頂点は、つねに円 $x^2+y^2=a^2+b^2$ 上にあることを示せ。<br>"
       r"(3) 長方形の面積 $S$ と周の長さ $L$ のとり得る値の範囲をそれぞれ求めよ。",
  "hint": r"接線を傾き $m$ で表すと、$y$ 軸に平行な接線を別に扱わなければならない。法線の向き $\varphi$ と原点からの距離 $p$ で直線を表すと、すべての向きを一度に扱える。(1) は $E$ 上の点 $(a\cos t,\ b\sin t)$ における接線と係数を比べる。(3) は $\sin^22\varphi$ だけの式にまとめる。",
  "sol": fig_rect() + r"(1) $E$ の接線は、接点を $(a\cos t,\ b\sin t)$ として $\dfrac{\cos t}{a}x+\dfrac{\sin t}{b}y=1$ と表される。<br>"
         r"直線 $x\cos\varphi+y\sin\varphi=p$ がこれと一致するのは、$\dfrac{\cos t}{a}=\dfrac{\cos\varphi}{p}$，$\dfrac{\sin t}{b}=\dfrac{\sin\varphi}{p}$，すなわち<br>"
         r"$\cos t=\dfrac{a\cos\varphi}{p}$，$\sin t=\dfrac{b\sin\varphi}{p}$<br>"
         r"を満たす $t$ が存在するときである。その条件は $\left(\dfrac{a\cos\varphi}{p}\right)^2+\left(\dfrac{b\sin\varphi}{p}\right)^2=1$，すなわち<br>"
         r"$p^2=a^2\cos^2\varphi+b^2\sin^2\varphi$<br>"
         r"(2) 法線の向きが $\varphi$ の接線は、(1) より $x\cos\varphi+y\sin\varphi=\pm p_1$（$p_1=\sqrt{a^2\cos^2\varphi+b^2\sin^2\varphi}$）の2本である（向き $\varphi+\pi$ のものが $-p_1$ の方）。"
         r"長方形の向かい合う辺は平行な2接線、隣り合う辺は法線の向きが直交する接線だから、ある $\varphi$ を用いて4辺は<br>"
         r"$x\cos\varphi+y\sin\varphi=\pm p_1$，$-x\sin\varphi+y\cos\varphi=\pm p_2$<br>"
         r"（$p_2=\sqrt{a^2\sin^2\varphi+b^2\cos^2\varphi}$，向き $\varphi+\dfrac\pi2$ に (1) を用いた）と表される。<br>"
         r"頂点 $(x,\ y)$ はそれぞれから1つずつの式を満たすから、2乗して加えると<br>"
         r"$x^2+y^2=(x\cos\varphi+y\sin\varphi)^2+(-x\sin\varphi+y\cos\varphi)^2=p_1^2+p_2^2=a^2+b^2$<br>"
         r"よって、頂点は円 $x^2+y^2=a^2+b^2$ 上にある。<br>"
         r"(3) 長方形の2辺の長さは、平行な2接線の距離 $2p_1,\ 2p_2$ である。<br>"
         r"$p_1^2p_2^2=(a^2\cos^2\varphi+b^2\sin^2\varphi)(a^2\sin^2\varphi+b^2\cos^2\varphi)$<br>"
         r"$=a^2b^2(\cos^4\varphi+\sin^4\varphi)+(a^4+b^4)\sin^2\varphi\cos^2\varphi$<br>"
         r"$=a^2b^2(1-2\sin^2\varphi\cos^2\varphi)+(a^4+b^4)\sin^2\varphi\cos^2\varphi$<br>"
         r"$=a^2b^2+\dfrac{(a^2-b^2)^2}{4}\sin^22\varphi$<br>"
         r"$\varphi$ は任意の値をとれて $0\leqq\sin^22\varphi\leqq1$ だから<br>"
         r"$a^2b^2\leqq p_1^2p_2^2\leqq a^2b^2+\dfrac{(a^2-b^2)^2}4=\dfrac{(a^2+b^2)^2}4$<br>"
         r"$S=4p_1p_2$ より　$\boldsymbol{4ab\leqq S\leqq2(a^2+b^2)}$<br>"
         r"また $(p_1+p_2)^2=p_1^2+p_2^2+2p_1p_2=a^2+b^2+2p_1p_2$ で、$ab\leqq p_1p_2\leqq\dfrac{a^2+b^2}2$ より<br>"
         r"$(a+b)^2\leqq(p_1+p_2)^2\leqq2(a^2+b^2)$<br>"
         r"$L=4(p_1+p_2)$ より　$\boldsymbol{4(a+b)\leqq L\leqq4\sqrt{2(a^2+b^2)}}$<br>"
         r"いずれも最小は $\varphi=0$（辺が座標軸に平行）のとき、最大は $\varphi=\dfrac\pi4$（正方形）のときである。",
  "note": r"(2) の円を楕円の準円という。(2) から「楕円の外部の点から引いた2本の接線が直交するとき、その点は円 $x^2+y^2=a^2+b^2$ 上にある」こともわかる。傾き $m$ の接線 $y=mx\pm\sqrt{a^2m^2+b^2}$ を使って解く場合は、$y$ 軸に平行な接線の場合を別に確かめる必要がある。図は $a=2,\ b=1,\ \varphi=\dfrac\pi6$ の場合。",
  "ex": r"楕円 $\dfrac{x^2}{16}+y^2=1$ に外接する長方形について、頂点がつねにのる円の方程式と、長方形の面積の最大値・最小値を求めよ。",
  "exa": r"円 $x^2+y^2=17$；最大値 $34$（正方形のとき），最小値 $16$"},
]})


def _nroots(poly_expr, var):
    """多項式の相異なる実数解の個数（厳密）"""
    P = Poly(expand(poly_expr), var)
    return len(set(P.real_roots()))


def _cq(P):
    """1次または2次の多項式（無理数係数可）の相異なる実数解の個数"""
    if P.degree() == 1:
        return 1
    assert P.degree() == 2
    D = simplify(P.discriminant())
    return 2 if D > 0 else (1 if D == 0 else 0)


def _v3():
    x, y, k, m = symbols("x y k m", real=True)
    # 接線：重解になること
    def tangent_ok(curve, line_y=None, line_x=None):
        if line_y is not None:
            e = expand(curve.subs(y, line_y))
            P = Poly(e, x)
        else:
            e = expand(curve.subs(x, line_x))
            P = Poly(e, y)
        return P.degree() == 2 and simplify(P.discriminant()) == 0
    assert tangent_ok(x**2/8 + y**2/2 - 1, line_x=4 - 2*y)
    assert tangent_ok(x**2 - y**2/4 - 1, line_y=2*sqrt(2)*x - 2)
    assert tangent_ok(y**2 - 8*x, line_y=x + 2)
    assert tangent_ok(x**2/12 + y**2/4 - 1, line_y=x - 4)
    assert tangent_ok(x**2 - 4*y, line_y=2*x - 4)
    assert expand((x**2/8 + y**2/2 - 1).subs(x, 4 - 2*y)) == expand((y - 1)**2)
    # 共有点の個数（双曲線と直線）
    def cnt(curve, line, mv):
        return _nroots(curve.subs(y, line).subs(m, mv) * 1, x)
    hyp = x**2 - 4*y**2 - 4
    tests = {Rational(1, 2): 1, -Rational(1, 2): 1, 1/sqrt(2): 1, -1/sqrt(2): 1, 0: 2, Rational(3, 5): 2, Rational(-2, 5): 2,
             Rational(3, 4): 0, -1: 0, 5: 0}
    for mv, c in tests.items():
        e = expand(hyp.subs(y, mv*x + 1))
        P = Poly(e, x)
        assert _cq(P) == c, (mv, _cq(P))
    el = x**2 + 4*y**2 - 4
    for mv, c in {sqrt(3)/2: 1, -sqrt(3)/2: 1, 1: 2, -2: 2, Rational(1, 2): 0, 0: 0}.items():
        P = Poly(expand(el.subs(y, mv*x + 2)), x)
        assert _cq(P) == c
    # 曲線外からの接線
    assert tangent_ok(x**2/4 + y**2 - 1, line_y=(3*x + 10)/8)
    D4 = expand((8*m*(2 - 2*m))**2/4 - (1 + 4*m**2)*(4*(2 - 2*m)**2 - 4))
    assert D4 == 32*m - 12
    assert Rational(-6, 5)**2/4 + Rational(4, 5)**2 == 1 and 3*2 - 8*2 + 10 == 0
    for sg in (1, -1):
        assert tangent_ok(x**2 - y**2 - 1, line_y=sg*sqrt(5)*x + 2)
    # 弦の中点・長さ
    P = Poly(expand(el.subs(y, x + k)), x)
    a2, a1, a0 = P.all_coeffs()
    assert (a2, a1, a0) == (5, 8*k, 4*k**2 - 4)
    assert expand(a1**2/4 - a2*a0) == 4*(5 - k**2)
    assert expand((a1/a2)**2 - 4*a0/a2 - Rational(16, 25)*(5 - k**2)) == 0
    assert sqrt(Rational(32*5, 25)) == 4*sqrt(10)/5
    for kv in [Rational(j, 7) for j in range(-15, 16)]:
        X = -a1.subs(k, kv) / (2*a2); Y = X + kv
        assert Y == -X/4
    el2 = 2*x**2 + y**2 - 2
    P = Poly(expand(el2.subs(y, 2*x + k)), x)
    a2, a1, a0 = P.all_coeffs()
    assert expand(a1**2/4 - a2*a0) == 12 - 2*k**2
    for kv in [Rational(j, 7) for j in range(-15, 16)]:
        X = -a1.subs(k, kv) / (2*a2); assert 2*X + kv == -X
    assert sqrt(5 * (Rational(48, 36))) == 2*sqrt(15)/3
    # 双曲線の接線と漸近線
    for _ in range(50):
        t = random.uniform(-2, 2); sg = random.choice([1, -1])
        x0, y0 = sg * 2 * math.cosh(t), math.sinh(t)
        Q = (x0 + 2*y0, (x0 + 2*y0)/2); R = (x0 - 2*y0, -(x0 - 2*y0)/2)
        assert close(x0*Q[0]/4 - y0*Q[1], 1) and close(x0*R[0]/4 - y0*R[1], 1)
        assert close((Q[0] + R[0])/2, x0) and close((Q[1] + R[1])/2, y0)
        assert close(abs(Q[0]*R[1] - R[0]*Q[1])/2, 2)
        x0, y0 = sg * 3 * math.cosh(t), 2 * math.sinh(t)    # 練習
        # 漸近線 y=±(2/3)x との交点を直接解く
        q = 1 / (x0/9 - y0*2/12); r = 1 / (x0/9 + y0*2/12)
        Qp, Rp = (q, 2*q/3), (r, -2*r/3)
        assert close(abs(Qp[0]*Rp[1] - Rp[0]*Qp[1])/2, 6, 1e-7)
    # 楕円と放物線の共有点の個数：直接 x の4次方程式の実数解の個数で確認
    def count(kv, A):
        e = expand(x**2/A + (x**2 + kv)**2 - 1)
        return len(set(Poly(e, x).real_roots()))
    def predicted(kv, vmin):
        if kv < vmin: return 0
        if kv == vmin: return 2
        if kv < -1: return 4
        if kv == -1: return 3
        if kv < 1: return 2
        if kv == 1: return 1
        return 0
    for A, vmin in ((4, Rational(-65, 16)), (2, Rational(-17, 8))):
        ks = [vmin - Rational(1, 10), vmin, vmin + Rational(1, 100), Rational(-3, 2), -1, Rational(-1, 2), 0, Rational(9, 10), 1, Rational(11, 10), 3]
        for kv in ks:
            assert count(kv, A) == predicted(kv, vmin), (A, kv)
    assert Rational(4, 64) - Rational(1, 8) - 4 == Rational(-65, 16) and factor(4*y**2 + y - 3) == (y + 1)*(4*y - 3)
    assert 2*Rational(1, 16) - Rational(1, 4) - 2 == Rational(-17, 8)
    # 外接長方形
    a, b, ph, t, p = symbols("a b phi t p", positive=True)
    for _ in range(30):
        A_, B_ = random.uniform(1.2, 4), random.uniform(0.3, 1.1); f_ = random.uniform(0, 2*math.pi)
        p1 = math.sqrt(A_*A_*math.cos(f_)**2 + B_*B_*math.sin(f_)**2)
        # 直線 x cosφ + y sinφ = p が楕円に接する ⇔ 判別式 0（数値で確認）
        c_, s_ = math.cos(f_), math.sin(f_)
        if abs(s_) > 0.1:
            # y = (p - x c)/s を代入した x の2次式の判別式
            qa = B_*B_*s_*s_ + A_*A_*c_*c_; qb = -2*A_*A_*p1*c_; qc = A_*A_*p1*p1 - A_*A_*B_*B_*s_*s_
            assert abs(qb*qb - 4*qa*qc) < 1e-7 * (1 + abs(qb*qb))
        V, P1, P2 = _rect_vertices(A_, B_, f_)
        for vx, vy in V:
            assert close(vx*vx + vy*vy, A_*A_ + B_*B_, 1e-9)
    e1 = (a**2*cos(ph)**2 + b**2*sin(ph)**2)*(a**2*sin(ph)**2 + b**2*cos(ph)**2) - (a**2*b**2 + (a**2 - b**2)**2/4*sin(2*ph)**2)
    assert simplify(expand(expand_trig(e1))) == 0
    Ss, Ls = [], []
    for j in range(4001):
        f_ = math.pi/2 * j / 4000
        _, P1, P2 = _rect_vertices(2, 1, f_)
        Ss.append(4*P1*P2); Ls.append(4*(P1 + P2))
    assert close(min(Ss), 8, 1e-9) and close(max(Ss), 10, 1e-6)
    assert close(min(Ls), 12, 1e-9) and close(max(Ls), 4*math.sqrt(10), 1e-6)
    Ss = [4*_rect_vertices(4, 1, math.pi/2*j/4000)[1]*_rect_vertices(4, 1, math.pi/2*j/4000)[2] for j in range(4001)]
    assert close(min(Ss), 16, 1e-9) and close(max(Ss), 34, 1e-6)

# ---------------------------------------------------------------- 節4
def fig_focal_parab():
    f = Fig(-1.7, 4.8, -2.6, 4.6, 24)
    f.lineq(1, 0, -1, col=GRAY, w=1.0, dash="4 3")
    f.axes()
    f.curve(lambda t: (t * t, 2 * t), -2.3, 2.3)
    f.seg((4, 4), (0.25, -1), col=BLUE, w=1.1)
    f.lineq(1, -2, -4, col=RED, w=1.0, dash=None)        # 2y = x + 4
    f.lineq(2, 1, -0.5, col=RED, w=1.0, dash=None)       # y = -2x - 1/2
    f.dot(1, 0); f.text(1, 0, "F", 3, 12, size=10)
    f.dot(4, 4); f.text(4, 4, "A", -12, -2)
    f.dot(0.25, -1); f.text(0.25, -1, "B", 5, 10)
    f.dot(-1, 1.5, col=RED)
    f.text(-1, -2.5, "x=−1", 3, 0, it=True, size=10)
    return f.svg()


def fig_confocal():
    f = Fig(-3.3, 3.3, -2.45, 2.45, 33)
    f.axes()
    f.curve(ell(3, math.sqrt(5)), 0, 2 * math.pi)
    r2 = math.sqrt(2)
    f.curve(lambda t: (r2 * math.cosh(t), r2 * math.sinh(t)), -1.4, 1.4, col=GREEN)
    f.curve(lambda t: (-r2 * math.cosh(t), r2 * math.sinh(t)), -1.4, 1.4, col=GREEN)
    x0, y0 = math.sqrt(4.5), math.sqrt(2.5)
    for nx, ny in ((x0 / 9, y0 / 5), (x0 / 2, -y0 / 2)):
        L = math.hypot(nx, ny); dx, dy = -ny / L * 0.9, nx / L * 0.9
        f.seg((x0 - dx, y0 - dy), (x0 + dx, y0 + dy), col=RED, w=1.1)
    f.dot(x0, y0, col=RED); f.text(x0, y0, "P", 6, -4)
    f.dot(2, 0); f.dot(-2, 0)
    f.text(2, 0, "F", 2, 12, size=10); f.text(-2, 0, "F′", -2, 12, size=10, anchor="end")
    return f.svg()


SEC.append({"title": r"離心率・準線と焦点の性質",
"base": r"""・定点 $\mathrm{F}$ と、$\mathrm{F}$ を通らない定直線 $l$ に対し、$\mathrm{PF}:\mathrm{PH}=e:1$（$\mathrm{H}$ は $\mathrm{P}$ から $l$ に下ろした垂線の足）を満たす点 $\mathrm{P}$ の軌跡は、$0<e<1$ のとき楕円、$e=1$ のとき放物線、$e>1$ のとき双曲線。$e$ を離心率、$l$ を準線という。<br>
・楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$（$a>b>0$）、双曲線 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$ で焦点を $(\pm c,\ 0)$ とすると、離心率は $e=\dfrac ca$，焦点 $(\pm c,\ 0)$ に対応する準線は $x=\pm\dfrac{a^2}{c}$。<br>
・焦点半径：楕円上の点 $\mathrm{P}(x,\ y)$ について $\mathrm{PF}=a-ex$，$\mathrm{PF'}=a+ex$（$\mathrm{F}(c,\ 0)$，$\mathrm{F'}(-c,\ 0)$）。放物線 $y^2=4px$（$p>0$）上の点では $\mathrm{PF}=x+p$。""",
"items": [
 {"lv": 2, "title": r"離心率と準線から2次曲線を求める",
  "q": r"点 $\mathrm{F}(1,\ 0)$ からの距離と直線 $l:x=4$ からの距離の比が $1:2$ である点 $\mathrm{P}$ の軌跡を求めよ。また、この曲線の離心率と、もう1つの焦点の座標およびそれに対応する準線の方程式を求めよ。",
  "hint": r"$\mathrm{P}(x,\ y)$ とおいて $2\mathrm{PF}=\mathrm{PH}$ を式にする。得られた楕円について、$e=\dfrac ca$，準線 $x=\pm\dfrac{a^2}{c}$ を確かめる。",
  "sol": r"$\mathrm{P}(x,\ y)$ から $l$ に下ろした垂線の足を $\mathrm{H}$ とすると、$\mathrm{PF}:\mathrm{PH}=1:2$ より $2\mathrm{PF}=\mathrm{PH}$。<br>"
         r"$2\sqrt{(x-1)^2+y^2}=|x-4|$<br>2乗して $4(x^2-2x+1+y^2)=x^2-8x+16$，$3x^2+4y^2=12$<br>"
         r"よって、軌跡は　楕円 $\boldsymbol{\dfrac{x^2}{4}+\dfrac{y^2}{3}=1}$<br>"
         r"$a=2$，$b=\sqrt3$，$c=\sqrt{4-3}=1$ より、離心率は $e=\dfrac ca=\boldsymbol{\dfrac12}$（与えられた比と一致する）。<br>"
         r"楕円は $y$ 軸に関して対称だから、もう1つの焦点は $\boldsymbol{(-1,\ 0)}$，対応する準線は $\boldsymbol{x=-4}$（$=-\dfrac{a^2}{c}$）。",
  "note": r"離心率 $e$ が $0$ に近いほど楕円は円に近く、$1$ に近いほど細長くなる。$e=\dfrac ca$ は曲線の形だけで決まり、拡大・縮小しても変わらない。",
  "ex": r"点 $\mathrm{F}(4,\ 0)$ からの距離と直線 $x=1$ からの距離の比が $2:1$ である点の軌跡を求めよ。また、もう1つの焦点の座標とそれに対応する準線の方程式を求めよ。",
  "exa": r"双曲線 $\dfrac{x^2}{4}-\dfrac{y^2}{12}=1$；焦点 $(-4,\ 0)$，準線 $x=-1$"},
 {"lv": 3, "title": r"焦点からの距離（焦点半径）と最大・最小",
  "q": r"楕円 $\dfrac{x^2}{4}+y^2=1$ の2つの焦点を $\mathrm{F}(\sqrt3,\ 0)$，$\mathrm{F'}(-\sqrt3,\ 0)$ とし、楕円上の点 $\mathrm{P}(x,\ y)$ をとる。<br>(1) $\mathrm{PF},\ \mathrm{PF'}$ を $x$ で表せ。<br>(2) $\mathrm{PF}\cdot\mathrm{PF'}$ の最大値と最小値を求めよ。<br>(3) $\mathrm{P}$ が長軸の両端以外を動くとき、$\angle\mathrm{FPF'}$ の最大値を求めよ。",
  "hint": r"(1) $y^2=1-\dfrac{x^2}4$ を代入すると $\mathrm{PF}^2$ が完全平方式になる。(3) 余弦定理で $\cos\angle\mathrm{FPF'}$ を $\mathrm{PF}\cdot\mathrm{PF'}$ で表す。$\mathrm{PF}+\mathrm{PF'}=4$ が一定であることを使う。",
  "sol": r"(1) $\mathrm{PF}^2=(x-\sqrt3)^2+y^2=x^2-2\sqrt3x+3+1-\dfrac{x^2}{4}$<br>$=\dfrac34x^2-2\sqrt3x+4=\left(2-\dfrac{\sqrt3}2x\right)^2$<br>"
         r"$-2\leqq x\leqq2$ より $2-\dfrac{\sqrt3}2x>0$ であるから　$\boldsymbol{\mathrm{PF}=2-\dfrac{\sqrt3}{2}x}$<br>"
         r"$\mathrm{PF'}=4-\mathrm{PF}$ より　$\boldsymbol{\mathrm{PF'}=2+\dfrac{\sqrt3}{2}x}$<br>"
         r"(2) $\mathrm{PF}\cdot\mathrm{PF'}=4-\dfrac34x^2$ で、$-2\leqq x\leqq2$ より<br><b>最大値 $4$（$x=0$ のとき），最小値 $1$（$x=\pm2$ のとき）</b><br>"
         r"(3) $\theta=\angle\mathrm{FPF'}$，$t=\mathrm{PF}\cdot\mathrm{PF'}$ とおく。$\mathrm{FF'}=2\sqrt3$ であり、余弦定理より<br>"
         r"$\cos\theta=\dfrac{\mathrm{PF}^2+\mathrm{PF'}^2-12}{2t}=\dfrac{(\mathrm{PF}+\mathrm{PF'})^2-2t-12}{2t}=\dfrac{16-2t-12}{2t}=\dfrac2t-1$<br>"
         r"$\mathrm{P}$ が長軸の両端以外のとき $-2<x<2$ で $1<t\leqq4$ だから　$\cos\theta\geqq\dfrac24-1=-\dfrac12$<br>"
         r"等号は $t=4$，すなわち $\mathrm{P}(0,\ \pm1)$ のとき成り立つ。$0<\theta<\pi$ で $\cos\theta$ は減少するから、$\angle\mathrm{FPF'}$ の最大値は　$\boldsymbol{\dfrac23\pi}$",
  "note": r"一般に楕円上の点 $\mathrm{P}(x,\ y)$ では $\mathrm{PF}=a-ex$，$\mathrm{PF'}=a+ex$（$e$ は離心率）が成り立つ。これは「$\mathrm{PF}$ は、$\mathrm{P}$ から準線 $x=\dfrac ae$ までの距離 $\dfrac ae-x$ の $e$ 倍」という離心率の定義そのものである。",
  "ex": r"楕円 $\dfrac{x^2}{8}+\dfrac{y^2}{4}=1$ の2つの焦点を $\mathrm{F},\ \mathrm{F'}$，楕円上の点を $\mathrm{P}$ とするとき、$\mathrm{PF}\cdot\mathrm{PF'}$ の最大値・最小値と、$\mathrm{P}$ が長軸の両端以外を動くときの $\angle\mathrm{FPF'}$ の最大値を求めよ。",
  "exa": r"最大値 $8$，最小値 $4$；$\angle\mathrm{FPF'}$ の最大値 $\dfrac\pi2$"},
 {"lv": 3, "title": r"放物線の焦点を通る弦の性質",
  "q": r"放物線 $y^2=4x$ の焦点 $\mathrm{F}$ を通る直線が、この放物線と2点 $\mathrm{A},\ \mathrm{B}$ で交わる。<br>(1) $\dfrac1{\mathrm{FA}}+\dfrac1{\mathrm{FB}}$ は一定であることを示せ。<br>(2) $\mathrm{A},\ \mathrm{B}$ における放物線の接線は直交し、その交点は準線上にあることを示せ。",
  "hint": r"放物線上の点を $(t^2,\ 2t)$ と媒介変数で表すと計算が楽になる。$\mathrm{A},\ \mathrm{F},\ \mathrm{B}$ が一直線上にある条件は $ab=-1$ という簡単な形になる。焦点までの距離は準線までの距離に等しい。",
  "sol": fig_focal_parab() + r"$\mathrm{F}(1,\ 0)$，準線は $x=-1$。<br>$\mathrm{A}(a^2,\ 2a)$，$\mathrm{B}(b^2,\ 2b)$（$a\neq b$）とおける。<br>"
         r"直線 $\mathrm{AB}$ の方程式は<br>$2x-(a+b)y+2ab=0$<br>である（$\mathrm{A},\ \mathrm{B}$ の座標を代入すると成り立つ）。<br>"
         r"これが $\mathrm{F}(1,\ 0)$ を通るから $2+2ab=0$，すなわち　$ab=-1$ …①<br>"
         r"(1) 放物線上の点から焦点までの距離は準線までの距離に等しいから、$\mathrm{FA}=a^2+1$，$\mathrm{FB}=b^2+1$。①より $b^2=\dfrac1{a^2}$ なので<br>"
         r"$\dfrac1{\mathrm{FA}}+\dfrac1{\mathrm{FB}}=\dfrac1{a^2+1}+\dfrac{a^2}{1+a^2}=1$（一定）<br>"
         r"(2) 点 $(t^2,\ 2t)$ における接線は $2ty=2(x+t^2)$，すなわち $ty=x+t^2$。①より $a,\ b\neq0$ だから、$\mathrm{A},\ \mathrm{B}$ における接線の傾きは $\dfrac1a,\ \dfrac1b$ で、その積は $\dfrac1{ab}=-1$。よって2接線は直交する。<br>"
         r"また、$ay=x+a^2$，$by=x+b^2$ を辺々引いて $(a-b)y=a^2-b^2$，$y=a+b$。さらに $x=ay-a^2=ab=-1$。<br>"
         r"よって、交点 $(-1,\ a+b)$ は準線 $x=-1$ 上にある。（証明終わり）",
  "note": r"一般に $y^2=4px$（$p>0$）では $\dfrac1{\mathrm{FA}}+\dfrac1{\mathrm{FB}}=\dfrac1p$。焦点弦の長さは $\mathrm{AB}=a^2+b^2+2=a^2+\dfrac1{a^2}+2\geqq4$ で、最小になるのは $x$ 軸に垂直な弦（通径）のとき。逆に、準線上の点から引いた2本の接線は直交し、2つの接点を結ぶ弦は焦点を通る。",
  "ex": r"放物線 $y^2=8x$ の焦点 $\mathrm{F}$ を通る直線が放物線と2点 $\mathrm{A},\ \mathrm{B}$ で交わるとき、$\dfrac1{\mathrm{FA}}+\dfrac1{\mathrm{FB}}$ の値と、$\mathrm{AB}$ の長さの最小値を求めよ。",
  "exa": r"$\dfrac12$；$8$"},
 {"lv": 4, "title": r"焦点を共有する楕円と双曲線は直交する",
  "q": r"$a>b>0$，$A>0$，$B>0$ とする。楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ と双曲線 $\dfrac{x^2}{A^2}-\dfrac{y^2}{B^2}=1$ の焦点が一致しているとき、2曲線の各交点において、それぞれの曲線の接線は直交することを示せ。",
  "hint": r"焦点が一致する条件は $a^2-b^2=A^2+B^2$。交点 $(x_0,\ y_0)$ における2本の接線の法線ベクトル $\left(\dfrac{x_0}{a^2},\ \dfrac{y_0}{b^2}\right)$，$\left(\dfrac{x_0}{A^2},\ -\dfrac{y_0}{B^2}\right)$ の内積が $0$ になることを、2曲線の式を辺々引いて示す。",
  "sol": fig_confocal() + r"焦点が一致するから $a^2-b^2=A^2+B^2$，すなわち<br>$A^2-a^2=-(b^2+B^2)$ …①<br>"
         r"交点を $(x_0,\ y_0)$ とすると<br>$\dfrac{x_0^2}{a^2}+\dfrac{y_0^2}{b^2}=1$，$\dfrac{x_0^2}{A^2}-\dfrac{y_0^2}{B^2}=1$<br>辺々引いて<br>"
         r"$x_0^2\left(\dfrac1{a^2}-\dfrac1{A^2}\right)+y_0^2\left(\dfrac1{b^2}+\dfrac1{B^2}\right)=0$<br>"
         r"①より $\dfrac1{a^2}-\dfrac1{A^2}=\dfrac{A^2-a^2}{a^2A^2}=-\dfrac{b^2+B^2}{a^2A^2}$，また $\dfrac1{b^2}+\dfrac1{B^2}=\dfrac{b^2+B^2}{b^2B^2}$ であるから<br>"
         r"$(b^2+B^2)\left(-\dfrac{x_0^2}{a^2A^2}+\dfrac{y_0^2}{b^2B^2}\right)=0$<br>"
         r"$b^2+B^2>0$ より　$\dfrac{x_0^2}{a^2A^2}-\dfrac{y_0^2}{b^2B^2}=0$ …②<br>"
         r"交点における楕円の接線 $\dfrac{x_0x}{a^2}+\dfrac{y_0y}{b^2}=1$ の法線ベクトルは $\vec{n_1}=\left(\dfrac{x_0}{a^2},\ \dfrac{y_0}{b^2}\right)$，双曲線の接線 $\dfrac{x_0x}{A^2}-\dfrac{y_0y}{B^2}=1$ の法線ベクトルは $\vec{n_2}=\left(\dfrac{x_0}{A^2},\ -\dfrac{y_0}{B^2}\right)$ である。双曲線上の点では $|x_0|\geqq A>0$ だから、どちらも $\vec{0}$ ではない。<br>"
         r"②より $\vec{n_1}\cdot\vec{n_2}=\dfrac{x_0^2}{a^2A^2}-\dfrac{y_0^2}{b^2B^2}=0$ であるから、2本の接線は直交する。（証明終わり）",
  "note": r"楕円の接線は $\angle\mathrm{FPF'}$ の外角を、双曲線の接線は $\angle\mathrm{FPF'}$ を二等分する（2次曲線の光学的性質）。内角の二等分線と外角の二等分線は直交するので、この結果はその性質からも説明できる。図は $\dfrac{x^2}{9}+\dfrac{y^2}{5}=1$ と $x^2-y^2=2$（焦点 $(\pm2,\ 0)$）の場合。",
  "ex": r"楕円 $\dfrac{x^2}{6}+\dfrac{y^2}{2}=1$ と焦点を共有し、点 $(\sqrt3,\ 1)$ を通る双曲線の方程式を求めよ。また、点 $(\sqrt3,\ 1)$ における2曲線の接線の方程式を求め、それらが直交することを確かめよ。",
  "exa": r"$x^2-y^2=2$；接線 $x+\sqrt3y=2\sqrt3$ と $\sqrt3x-y=2$（傾き $-\dfrac1{\sqrt3}$ と $\sqrt3$ の積が $-1$）"},
]})


def _ang(P, F1, F2):
    u = (F1[0] - P[0], F1[1] - P[1]); v = (F2[0] - P[0], F2[1] - P[1])
    return math.acos(max(-1, min(1, (u[0]*v[0] + u[1]*v[1]) / (math.hypot(*u) * math.hypot(*v)))))


def _v4():
    x, y = symbols("x y", real=True)
    assert expand(4*((x-1)**2 + y**2) - (x-4)**2) == 3*x**2 + 4*y**2 - 12
    assert expand((x-4)**2 + y**2 - 4*(x-1)**2) == -(3*x**2 - y**2 - 12)
    assert sqrt(4 + 12) == 4 and Rational(4, 4) == 1          # 練習：c=4, a^2/c=1, e=2
    # 焦点半径
    assert expand((x - sqrt(3))**2 + 1 - x**2/4 - (2 - sqrt(3)*x/2)**2) == 0
    assert expand((2 - sqrt(3)*x/2)*(2 + sqrt(3)*x/2)) == 4 - Rational(3, 4)*x**2
    angs = []
    for j in range(1, 20000):
        th = math.pi * j / 20000
        P = (2*math.cos(th), math.sin(th))
        angs.append(_ang(P, (math.sqrt(3), 0), (-math.sqrt(3), 0)))
        X = P[0]; pf = math.hypot(P[0] - math.sqrt(3), P[1])
        assert close(pf, 2 - math.sqrt(3)/2*X)
    assert close(max(angs), 2*math.pi/3, 1e-6)
    prods, angs = [], []
    for j in range(1, 20000):
        th = math.pi * j / 20000
        P = (2*math.sqrt(2)*math.cos(th), 2*math.sin(th))
        prods.append(math.hypot(P[0]-2, P[1]) * math.hypot(P[0]+2, P[1]))
        angs.append(_ang(P, (2, 0), (-2, 0)))
    assert close(max(prods), 8, 1e-6) and abs(min(prods) - 4) < 1e-5 and close(max(angs), math.pi/2, 1e-6)
    # 放物線の焦点弦
    a = symbols("a", nonzero=True)
    b = -1/a
    assert simplify(1/(a**2 + 1) + 1/(b**2 + 1)) == 1
    for _ in range(50):
        av = random.uniform(-4, 4)
        if abs(av) < 0.05: continue
        bv = -1/av
        A, B = (av*av, 2*av), (bv*bv, 2*bv)
        assert abs((A[0]-1)*(B[1]) - (B[0]-1)*A[1]) < 1e-8          # A, F, B 一直線
        assert close(2*A[0] - (av+bv)*A[1] + 2*av*bv, 0) and close(2*B[0] - (av+bv)*B[1] + 2*av*bv, 0)
        assert close(1/math.hypot(A[0]-1, A[1]) + 1/math.hypot(B[0]-1, B[1]), 1)
        assert close((1/av)*(1/bv), -1)
        X, Y = av*bv, av + bv
        assert close(av*Y, X + av*av) and close(bv*Y, X + bv*bv) and close(X, -1)
    # 練習：y^2=8x, F(2,0) を通る傾き角 φ の直線
    Ls, Ss = [], []
    for j in range(1, 4000):
        ph = math.pi * j / 4000
        c, s = math.cos(ph), math.sin(ph)
        # (2+rc)^... 点 (2 + r c, r s) を代入: r^2 s^2 - 8 r c - 16 = 0
        qa, qb, qc = s*s, -8*c, -16.0
        D = math.sqrt(qb*qb - 4*qa*qc)
        r1, r2 = (-qb + D)/(2*qa), (-qb - D)/(2*qa)
        Ss.append(1/abs(r1) + 1/abs(r2)); Ls.append(abs(r1 - r2))
    assert all(close(v, 0.5, 1e-9) for v in Ss) and close(min(Ls), 8, 1e-6)
    # 共焦点
    for _ in range(50):
        av, bv = random.uniform(2, 5), random.uniform(0.5, 1.5)
        c2 = av*av - bv*bv
        B2 = random.uniform(0.1, c2 - 0.1); A2 = c2 - B2
        # 交点：x^2/a^2 + y^2/b^2 = 1, x^2/A2 - y^2/B2 = 1
        M = [[1/av**2, 1/bv**2], [1/A2, -1/B2]]
        det = M[0][0]*M[1][1] - M[0][1]*M[1][0]
        X2 = (M[1][1] - M[0][1]) / det; Y2 = (M[0][0] - M[1][0]) / det
        assert X2 > 0 and Y2 > 0
        x0, y0 = math.sqrt(X2), math.sqrt(Y2)
        assert close(x0*x0/(av*av*A2) - y0*y0/(bv*bv*B2), 0)
    assert close(4.5/9 + 2.5/5, 1) and close(4.5 - 2.5, 2)
    # 練習
    A2 = symbols("A2", positive=True)
    sols = solve(3/A2 - 1/(4 - A2) - 1, A2)
    assert set(sols) == {2, 6}
    assert 3 - 1 == 2 and Rational(3, 6) + Rational(1, 2) == 1
    assert (-(sqrt(3)/6)/(Rational(1, 2))) * sqrt(3) == -1
    assert expand(6*(sqrt(3)*x/6 + y/2) - 3*(x + sqrt(3)*y)/sqrt(3)) == 0

# ---------------------------------------------------------------- 節5
def fig_cycloid():
    f = Fig(-0.3, 7.0, -0.4, 2.35, 31)
    f.axes()
    f.curve(lambda t: (t - math.sin(t), 1 - math.cos(t)), 0, 2 * math.pi, w=1.5)
    th = 2 * math.pi / 3
    Q = (th, 1); P = (th - math.sin(th), 1 - math.cos(th))
    f.circle(Q, 1, col=GRAY, w=1.0)
    f.seg(Q, P, col=RED, w=1.1); f.seg(Q, (th, 0), col=GRAY, w=0.8, dash="2 2")
    f.dot(*Q); f.dot(*P, col=RED); f.dot(th, 0)
    f.text(*Q, "Q", 4, -3, size=10); f.text(*P, "P", -11, -3); f.text(th, 0, "T", 3, 12, size=10)
    f.text(math.pi, 0, "π", 3, 12, size=10, it=True); f.text(2 * math.pi, 0, "2π", -6, 12, size=10, it=True)
    f.seg((math.pi, 0), (math.pi, 0.08), col="#444", w=0.9)
    return f.svg()


def _tri_area(P):
    (x1, y1), (x2, y2), (x3, y3) = P
    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) / 2


def fig_tri_ell():
    f = Fig(-2.35, 2.35, -1.3, 1.3, 46)
    f.axes()
    f.curve(ell(2, 1), 0, 2 * math.pi, w=1.5)
    T1 = [(2 * math.cos(2 * k * math.pi / 3), math.sin(2 * k * math.pi / 3)) for k in range(3)]
    T2 = [(2 * math.cos(1.1 + 2 * k * math.pi / 3), math.sin(1.1 + 2 * k * math.pi / 3)) for k in range(3)]
    f.poly(T1, op=0.5, col=BLUE, w=1.1)
    f.poly(T2, fill="none", op=0, col=RED, w=1.0)
    for q in T1:
        f.dot(*q)
    f.text(*T1[0], "A", 3, -5); f.text(*T1[1], "B", -12, -2); f.text(*T1[2], "C", -12, 10)
    return f.svg()


SEC.append({"title": r"媒介変数表示",
"base": r"""・円 $x^2+y^2=r^2$：$x=r\cos\theta,\ y=r\sin\theta$。楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$：$x=a\cos\theta,\ y=b\sin\theta$。双曲線 $\dfrac{x^2}{a^2}-\dfrac{y^2}{b^2}=1$：$x=\dfrac{a}{\cos\theta},\ y=b\tan\theta$。放物線 $y^2=4px$：$x=pt^2,\ y=2pt$。<br>
・サイクロイド（半径 $a$ の円が $x$ 軸上を滑らずに転がるときの、円周上の定点の軌跡）：$x=a(\theta-\sin\theta),\ y=a(1-\cos\theta)$。<br>
・媒介変数を消去したら、$x,\ y$ の動く範囲（$\cos\theta$ の範囲、除かれる点など）を確かめる。曲線上の点を媒介変数で表すと、最大・最小が1変数の問題になる。""",
"items": [
 {"lv": 1, "title": r"媒介変数を消去して曲線を求める",
  "q": r"次の式で表される点 $(x,\ y)$ はどのような曲線を描くか。<br>(1) $x=t-1,\ y=t^2+2t$　(2) $x=2\cos\theta+1,\ y=3\sin\theta-2$　(3) $x=\cos\theta,\ y=\cos2\theta$",
  "hint": r"(1) は $t$ について解いて代入、(2) は $\cos^2\theta+\sin^2\theta=1$ を使う。(3) は2倍角の公式で消去できるが、$x=\cos\theta$ の範囲から曲線の一部になる。",
  "sol": r"(1) $t=x+1$ を代入して $y=(x+1)^2+2(x+1)=x^2+4x+3$。$t$ が実数全体を動くとき $x$ も実数全体を動くから<br><b>放物線 $y=x^2+4x+3$</b><br>"
         r"(2) $\cos\theta=\dfrac{x-1}2$，$\sin\theta=\dfrac{y+2}3$ を $\cos^2\theta+\sin^2\theta=1$ に代入して<br><b>楕円 $\dfrac{(x-1)^2}{4}+\dfrac{(y+2)^2}{9}=1$</b><br>"
         r"(3) $y=2\cos^2\theta-1=2x^2-1$。$x=\cos\theta$ は $-1\leqq x\leqq1$ のすべての値をとるから<br><b>放物線 $y=2x^2-1$ の $-1\leqq x\leqq1$ の部分</b>",
  "note": r"(3) のように三角関数で表された媒介変数を消去すると、得られた方程式の表す曲線の一部しか描かないことがある。消去したあとに $x,\ y$ の範囲を必ず確かめる。",
  "ex": r"次の式で表される点 $(x,\ y)$ はどのような曲線を描くか。<br>(1) $x=2t+1,\ y=4t^2-1$　(2) $x=3\cos\theta-1,\ y=2\sin\theta+1$　(3) $x=\sin\theta,\ y=\cos2\theta$",
  "exa": r"(1) 放物線 $y=x^2-2x$　(2) 楕円 $\dfrac{(x+1)^2}{9}+\dfrac{(y-1)^2}{4}=1$　(3) 放物線 $y=1-2x^2$ の $-1\leqq x\leqq1$ の部分"},
 {"lv": 2, "title": r"分数式・三角関数による媒介変数表示",
  "q": r"次の式で表される点 $(x,\ y)$ はどのような図形を描くか。<br>(1) $x=\dfrac{1-t^2}{1+t^2},\ y=\dfrac{2t}{1+t^2}$（$t$ は実数）<br>(2) $x=\dfrac2{\cos\theta},\ y=3\tan\theta$（$\cos\theta\neq0$）",
  "hint": r"(1) $x^2+y^2$ を計算する。ただし、円周上のすべての点が現れるとは限らないので、逆に円周上の点を表す $t$ が存在するかを調べる。(2) $\dfrac1{\cos^2\theta}-\tan^2\theta=1$ を使う。",
  "sol": r"(1) $x^2+y^2=\dfrac{(1-t^2)^2+4t^2}{(1+t^2)^2}=\dfrac{(1+t^2)^2}{(1+t^2)^2}=1$<br>"
         r"また $x=\dfrac{2}{1+t^2}-1>-1$ であるから、点 $(-1,\ 0)$ は現れない。<br>"
         r"逆に、円 $x^2+y^2=1$ 上の点 $(x,\ y)$ で $x\neq-1$ のものに対し $t=\dfrac{y}{1+x}$ とおくと<br>$1+t^2=\dfrac{(1+x)^2+y^2}{(1+x)^2}=\dfrac{2(1+x)}{(1+x)^2}=\dfrac{2}{1+x}$<br>"
         r"より　$\dfrac{1-t^2}{1+t^2}=\dfrac2{1+t^2}-1=x$，$\dfrac{2t}{1+t^2}=t(1+x)=y$<br>となり、この点は現れる。<br>"
         r"よって　<b>円 $x^2+y^2=1$ から点 $(-1,\ 0)$ を除いたもの</b><br>"
         r"(2) $\dfrac{x^2}4-\dfrac{y^2}9=\dfrac1{\cos^2\theta}-\tan^2\theta=1$<br>"
         r"逆に、$\dfrac{x^2}4-\dfrac{y^2}9=1$ 上の点 $(x,\ y)$ に対し、$\cos\theta=\dfrac2x$，$\sin\theta=\dfrac{2y}{3x}$ とおくと<br>$\cos^2\theta+\sin^2\theta=\dfrac4{x^2}\left(1+\dfrac{y^2}9\right)=\dfrac4{x^2}\cdot\dfrac{x^2}4=1$<br>"
         r"だから、このような $\theta$ が存在し、$\dfrac{2}{\cos\theta}=x$，$3\tan\theta=3\cdot\dfrac{\sin\theta}{\cos\theta}=y$ となる。<br>"
         r"よって　<b>双曲線 $\dfrac{x^2}{4}-\dfrac{y^2}{9}=1$ 全体</b>",
  "note": r"(1) で $t=\tan\dfrac\varphi2$（$-\pi<\varphi<\pi$）とおくと $x=\cos\varphi,\ y=\sin\varphi$ となる。点 $(-1,\ 0)$ は $\varphi=\pi$ に対応し、$t$ をどれだけ大きくしても届かない。この表示は、円周上の有理点（座標がともに有理数の点）を調べるときにも使われる。",
  "ex": r"次の式で表される点 $(x,\ y)$ はどのような図形を描くか。<br>(1) $x=\dfrac{2(1-t^2)}{1+t^2},\ y=\dfrac{6t}{1+t^2}$（$t$ は実数）　(2) $x=\tan\theta,\ y=\dfrac1{\cos\theta}$（$\cos\theta\neq0$）",
  "exa": r"(1) 楕円 $\dfrac{x^2}4+\dfrac{y^2}9=1$ から点 $(-2,\ 0)$ を除いたもの　(2) 双曲線 $y^2-x^2=1$ 全体"},
 {"lv": 2, "title": r"サイクロイドの媒介変数表示",
  "q": r"半径 $1$ の円 $C$ が、$x$ 軸に接しながら $x$ 軸の正の向きに滑ることなく転がる。はじめ原点 $\mathrm{O}$ にあった $C$ 上の点 $\mathrm{P}$ の座標を、$C$ が回転した角 $\theta$ を用いて表せ。また、$\theta=\dfrac23\pi$ のときの $\mathrm{P}$ の座標を求めよ。",
  "hint": r"滑らずに転がるので、円が $\theta$ だけ回転したとき $x$ 軸上を進んだ距離は弧の長さ $\theta$ に等しい。中心の座標を求め、中心から見た $\mathrm{P}$ の向き（はじめ真下で、時計回りに $\theta$ 回転）を考える。",
  "sol": fig_cycloid() + r"円が $\theta$ だけ回転したとき、$x$ 軸との接点を $\mathrm{T}$，中心を $\mathrm{Q}$ とする。滑らないから $\mathrm{OT}$ は弧 $\mathrm{TP}$ の長さ $\theta$ に等しく　$\mathrm{Q}(\theta,\ 1)$<br>"
         r"$\overrightarrow{\mathrm{QP}}$ ははじめ真下の向き（$x$ 軸の正の向きから $-\dfrac\pi2$）で、円は時計回りに $\theta$ 回転するから、$\overrightarrow{\mathrm{QP}}$ の向きは $-\dfrac\pi2-\theta$ である。<br>"
         r"$\overrightarrow{\mathrm{QP}}=\left(\cos\left(-\dfrac\pi2-\theta\right),\ \sin\left(-\dfrac\pi2-\theta\right)\right)=(-\sin\theta,\ -\cos\theta)$<br>"
         r"よって　$\boldsymbol{x=\theta-\sin\theta,\ y=1-\cos\theta}$<br>"
         r"$\theta=\dfrac23\pi$ のとき　$\mathrm{P}\boldsymbol{\left(\dfrac23\pi-\dfrac{\sqrt3}2,\ \dfrac32\right)}$",
  "note": r"$\theta$ が $0$ から $2\pi$ まで動くと $\mathrm{P}$ はアーチを1つ描き、$\theta=\pi$ で最高点 $(\pi,\ 2)$ に達する。円が定円の外側（内側）を転がるときの軌跡はエピサイクロイド（ハイポサイクロイド）とよばれ、同じように「中心の位置」と「中心から見た向き」を求めて表す。",
  "ex": r"半径 $2$ の円が $x$ 軸に接しながら $x$ 軸の正の向きに滑ることなく転がる。はじめ原点にあった円周上の点 $\mathrm{P}$ の座標を、円の回転角 $\theta$ で表せ。また、$\theta=\dfrac\pi2$ のときの $\mathrm{P}$ の座標と、$0\leqq\theta\leqq2\pi$ で $\mathrm{P}$ の $y$ 座標が最大となるときの $\mathrm{P}$ の座標を求めよ。",
  "exa": r"$x=2(\theta-\sin\theta),\ y=2(1-\cos\theta)$；$(\pi-2,\ 2)$；$(2\pi,\ 4)$"},
 {"lv": 3, "title": r"媒介変数表示を用いた最大・最小（楕円と直線の距離）",
  "q": r"楕円 $\dfrac{x^2}{9}+\dfrac{y^2}{4}=1$ 上の点 $\mathrm{P}$ と直線 $l:2x+3y=12$ の距離の最大値と最小値、およびそのときの $\mathrm{P}$ の座標を求めよ。",
  "hint": r"$\mathrm{P}(3\cos\theta,\ 2\sin\theta)$ とおくと、距離は $\theta$ の三角関数で表され、三角関数の合成で最大・最小がわかる。絶対値の中の符号を確認する。",
  "sol": r"$\mathrm{P}(3\cos\theta,\ 2\sin\theta)$（$0\leqq\theta<2\pi$）とおくと、点と直線の距離の公式より<br>"
         r"$d=\dfrac{|6\cos\theta+6\sin\theta-12|}{\sqrt{2^2+3^2}}=\dfrac{\left|6\sqrt2\sin\left(\theta+\dfrac\pi4\right)-12\right|}{\sqrt{13}}$<br>"
         r"$6\sqrt2\sin\left(\theta+\dfrac\pi4\right)\leqq6\sqrt2<12$ であるから　$d=\dfrac{12-6\sqrt2\sin\left(\theta+\dfrac\pi4\right)}{\sqrt{13}}$<br>"
         r"$\dfrac\pi4\leqq\theta+\dfrac\pi4<\dfrac94\pi$ より、$\theta=\dfrac\pi4$ のとき $\sin\left(\theta+\dfrac\pi4\right)=1$ で最小、$\theta=\dfrac54\pi$ のとき $\sin\left(\theta+\dfrac\pi4\right)=-1$ で最大となる。<br>"
         r"<b>最大値 $\dfrac{(12+6\sqrt2)\sqrt{13}}{13}$</b>　（$\mathrm{P}\left(-\dfrac{3\sqrt2}2,\ -\sqrt2\right)$ のとき）<br>"
         r"<b>最小値 $\dfrac{(12-6\sqrt2)\sqrt{13}}{13}$</b>　（$\mathrm{P}\left(\dfrac{3\sqrt2}2,\ \sqrt2\right)$ のとき）",
  "note": r"$6\sqrt2<12$ は、$l$ と楕円が共有点をもたないことを表している。最大・最小となる点における楕円の接線は $2x+3y=\pm6\sqrt2$ で、どちらも $l$ に平行である。このことから「$l$ に平行な接線を求める」という解き方もできる。",
  "ex": r"楕円 $\dfrac{x^2}{4}+y^2=1$ 上の点 $\mathrm{P}$ と直線 $x+2y=6$ の距離の最大値と最小値、およびそのときの $\mathrm{P}$ の座標を求めよ。",
  "exa": r"最大値 $\dfrac{6\sqrt5+2\sqrt{10}}5$（$\mathrm{P}\left(-\sqrt2,\ -\dfrac{\sqrt2}2\right)$），最小値 $\dfrac{6\sqrt5-2\sqrt{10}}5$（$\mathrm{P}\left(\sqrt2,\ \dfrac{\sqrt2}2\right)$）"},
 {"lv": 4, "title": r"楕円上の点と頂点の距離の最大（文字係数の場合分け）",
  "q": r"$a>0$ とする。楕円 $\dfrac{x^2}{a^2}+y^2=1$ 上の点 $\mathrm{P}$ と点 $\mathrm{B}(0,\ -1)$ の距離の最大値を求めよ。",
  "hint": r"$\mathrm{P}(x,\ y)$ として $x^2=a^2(1-y^2)$ を代入すると、$\mathrm{BP}^2$ は $y$（$-1\leqq y\leqq1$）の2次関数になる。2次の係数 $1-a^2$ の符号と、軸 $y=\dfrac1{a^2-1}$ が区間に入るかどうかで場合分けする。",
  "sol": r"$\mathrm{P}(x,\ y)$ とすると $x^2=a^2(1-y^2)$，$-1\leqq y\leqq1$ であり<br>"
         r"$\mathrm{BP}^2=a^2(1-y^2)+(y+1)^2=(1-a^2)y^2+2y+a^2+1$<br>これを $f(y)$ とおく。$f(1)=4$，$f(-1)=0$ である。<br>"
         r"[1] $0<a\leqq1$ のとき<br>$1-a^2\geqq0$ で、$f(y)$ は下に凸の2次関数または1次関数だから、最大値は区間の端での値の大きい方 $f(1)=4$。<br>"
         r"[2] $a>1$ のとき<br>$f(y)=-(a^2-1)\left(y-\dfrac1{a^2-1}\right)^2+\dfrac1{a^2-1}+a^2+1$<br>で上に凸、軸は $y=\dfrac1{a^2-1}$（$>0$）。<br>"
         r"(i) $\dfrac1{a^2-1}\geqq1$，すなわち $1<a\leqq\sqrt2$ のとき：$f(y)$ は $-1\leqq y\leqq1$ で増加し、最大値 $f(1)=4$。<br>"
         r"(ii) $\dfrac1{a^2-1}<1$，すなわち $a>\sqrt2$ のとき：最大値は $f\left(\dfrac1{a^2-1}\right)=\dfrac1{a^2-1}+a^2+1=\dfrac{a^4}{a^2-1}$。<br>"
         r"以上より、$\mathrm{BP}$ の最大値は<br>"
         r"$\boldsymbol{0<a\leqq\sqrt2}$ のとき $\boldsymbol{2}$，　$\boldsymbol{a>\sqrt2}$ のとき $\boldsymbol{\dfrac{a^2}{\sqrt{a^2-1}}}$",
  "note": r"$a>\sqrt2$ のとき、$\mathrm{B}$ から最も遠い点は反対側の頂点 $(0,\ 1)$ ではなく、その両側の2点 $\left(\pm\dfrac{a^2\sqrt{a^2-2}}{a^2-1},\ \dfrac1{a^2-1}\right)$ になる。「端点で最大」と思い込まず、軸の位置で場合分けすることが大切。",
  "ex": r"$a>0$ とする。楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{4}=1$ 上の点 $\mathrm{P}$ と点 $\mathrm{B}(0,\ -2)$ の距離の最大値を求めよ。",
  "exa": r"$0<a\leqq2\sqrt2$ のとき $4$，$a>2\sqrt2$ のとき $\dfrac{a^2}{\sqrt{a^2-4}}$"},
 {"lv": 5, "title": r"楕円に内接する三角形の面積（重心が中心のとき・最大値）",
  "q": r"楕円 $E:\dfrac{x^2}{4}+y^2=1$ 上の相異なる3点 $\mathrm{A},\ \mathrm{B},\ \mathrm{C}$ を頂点とする三角形について、次の問いに答えよ。<br>(1) $\triangle\mathrm{ABC}$ の重心が原点 $\mathrm{O}$ であるとき、$\triangle\mathrm{ABC}$ の面積は一定であることを示し、その値を求めよ。<br>(2) $\triangle\mathrm{ABC}$ の面積の最大値を求めよ。",
  "hint": r"$\mathrm{A}(2\cos\alpha,\ \sin\alpha)$ などと表し、$x$ 座標を $\dfrac12$ 倍して $E$ を単位円に移す。この変換で重心は重心に移り、面積はちょうど $\dfrac12$ 倍になる。単位円に内接する三角形の問題に帰着させ、(2) は正弦定理・積和公式・相加平均と相乗平均の関係で評価する。",
  "sol": fig_tri_ell() + r"$\mathrm{A}(2\cos\alpha,\ \sin\alpha)$，$\mathrm{B}(2\cos\beta,\ \sin\beta)$，$\mathrm{C}(2\cos\gamma,\ \sin\gamma)$ とおき、単位円上の3点 $\mathrm{A'}(\cos\alpha,\ \sin\alpha)$，$\mathrm{B'}(\cos\beta,\ \sin\beta)$，$\mathrm{C'}(\cos\gamma,\ \sin\gamma)$ を考える。<br>"
         r"3点 $(x_k,\ y_k)$（$k=1,\ 2,\ 3$）を頂点とする三角形の面積は $\dfrac12|(x_2-x_1)(y_3-y_1)-(x_3-x_1)(y_2-y_1)|$ で、$x$ 座標だけを $\dfrac12$ 倍するとこの値は $\dfrac12$ 倍になるから<br>"
         r"$\triangle\mathrm{ABC}=2\triangle\mathrm{A'B'C'}$ …①<br>"
         r"(1) 重心が $\mathrm{O}$ だから $\cos\alpha+\cos\beta+\cos\gamma=0$，$\sin\alpha+\sin\beta+\sin\gamma=0$。すなわち、$\vec{a}=\overrightarrow{\mathrm{OA'}}$，$\vec{b}=\overrightarrow{\mathrm{OB'}}$，$\vec{c}=\overrightarrow{\mathrm{OC'}}$ とおくと $\vec{a}+\vec{b}+\vec{c}=\vec{0}$。<br>"
         r"$|\vec{a}+\vec{b}|^2=|-\vec{c}|^2$ より $2+2\vec{a}\cdot\vec{b}=1$，$\vec{a}\cdot\vec{b}=-\dfrac12$。同様に $\vec{b}\cdot\vec{c}=\vec{c}\cdot\vec{a}=-\dfrac12$。<br>"
         r"よって $|\vec{a}-\vec{b}|^2=2-2\vec{a}\cdot\vec{b}=3$ などから $\mathrm{A'B'}=\mathrm{B'C'}=\mathrm{C'A'}=\sqrt3$。$\triangle\mathrm{A'B'C'}$ は1辺 $\sqrt3$ の正三角形で、面積は $\dfrac{\sqrt3}4\cdot3=\dfrac{3\sqrt3}4$。<br>"
         r"①より　$\triangle\mathrm{ABC}=\boldsymbol{\dfrac{3\sqrt3}{2}}$（一定）<br>"
         r"(2) $\triangle\mathrm{A'B'C'}$ の内角を $P,\ Q,\ R$ とする。外接円の半径が $1$ だから、正弦定理より $\mathrm{B'C'}=2\sin P$，$\mathrm{C'A'}=2\sin Q$。よって<br>"
         r"$\triangle\mathrm{A'B'C'}=\dfrac12\cdot\mathrm{C'A'}\cdot\mathrm{B'C'}\cdot\sin R=2\sin P\sin Q\sin R$<br>"
         r"$P+Q=\pi-R$ より $\sin P\sin Q=\dfrac12\{\cos(P-Q)-\cos(P+Q)\}\leqq\dfrac12(1+\cos R)$ だから<br>"
         r"$\triangle\mathrm{A'B'C'}\leqq(1+\cos R)\sin R$<br>"
         r"$t=\cos R$（$-1<t<1$）とおくと、$1+t>0$，$3-3t>0$ であり、相加平均と相乗平均の関係より<br>"
         r"$\{(1+t)\sin R\}^2=(1+t)^3(1-t)=\dfrac13(1+t)^3(3-3t)\leqq\dfrac13\left\{\dfrac{3(1+t)+(3-3t)}{4}\right\}^4=\dfrac13\left(\dfrac32\right)^4=\dfrac{27}{16}$<br>"
         r"よって $\triangle\mathrm{A'B'C'}\leqq\dfrac{3\sqrt3}4$。等号は $P=Q$ かつ $1+t=3-3t$（$t=\dfrac12$，$R=\dfrac\pi3$），すなわち正三角形のときに成り立つ。<br>"
         r"①より $\triangle\mathrm{ABC}\leqq\dfrac{3\sqrt3}{2}$ で、たとえば $\mathrm{A}(2,\ 0)$，$\mathrm{B}\left(-1,\ \dfrac{\sqrt3}2\right)$，$\mathrm{C}\left(-1,\ -\dfrac{\sqrt3}2\right)$ のとき等号が成り立つ。<br>"
         r"よって、最大値は　$\boldsymbol{\dfrac{3\sqrt3}{2}}$",
  "note": r"$x$ 軸方向（$y$ 軸方向）の拡大・縮小は、直線を直線に、中点や重心を中点や重心に移し、面積を一定の倍率で変える。そのため楕円に内接・外接する図形の問題は、円の問題に直して考えるとよい。一般に楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ に内接する三角形の面積の最大値は $\dfrac{3\sqrt3}4ab$ で、最大となるのは重心が楕円の中心にあるときに限る。図の赤い三角形も重心が $\mathrm{O}$ で、面積は青い三角形と等しい。",
  "ex": r"楕円 $\dfrac{x^2}{9}+\dfrac{y^2}{4}=1$ に内接する三角形の面積の最大値を求めよ。",
  "exa": r"$\dfrac{9\sqrt3}{2}$"},
]})


def _v5():
    x, y, t, th = symbols("x y t theta", real=True)
    assert expand(((x+1)**2 + 2*(x+1)) - (x**2 + 4*x + 3)) == 0
    assert expand((2*cos(th))**2/4 + (3*sin(th))**2/9).rewrite(cos).simplify() == 1
    assert simplify(expand_trig(cos(2*th)) - (2*cos(th)**2 - 1)) == 0
    assert expand(((x - 1)/2*2)**2 - 1 - (x**2 - 2*x)) == 0
    assert simplify(expand_trig(cos(2*th)) - (1 - 2*sin(th)**2)) == 0
    # 分数式の媒介変数
    X, Y = (1 - t**2)/(1 + t**2), 2*t/(1 + t**2)
    assert simplify(X**2 + Y**2 - 1) == 0 and simplify(X - (2/(1 + t**2) - 1)) == 0
    for _ in range(100):
        ph = random.uniform(-3.1, 3.1); xx, yy = math.cos(ph), math.sin(ph)
        tt = yy / (1 + xx)
        assert close((1 - tt*tt)/(1 + tt*tt), xx, 1e-7) and close(2*tt/(1 + tt*tt), yy, 1e-7)
        u = random.uniform(-3, 3); sg = random.choice([1, -1])
        xx, yy = sg*2*math.cosh(u), 3*math.sinh(u)
        c_, s_ = 2/xx, 2*yy/(3*xx)
        assert close(c_*c_ + s_*s_, 1) and close(2/c_, xx) and close(3*s_/c_, yy)
    X, Y = 2*(1 - t**2)/(1 + t**2), 6*t/(1 + t**2)
    assert simplify(X**2/4 + Y**2/9 - 1) == 0
    assert simplify(1/cos(th)**2 - (sin(th)/cos(th))**2) == 1
    # サイクロイド
    for a in (1, 2):
        for _ in range(50):
            T = random.uniform(0, 7)
            Q = (a*T, a); P = (a*(T - math.sin(T)), a*(1 - math.cos(T)))
            assert close(math.hypot(P[0] - Q[0], P[1] - Q[1]), a)
            # 中心から見た向きは -π/2 - T
            assert close(P[0] - Q[0], a*math.cos(-math.pi/2 - T)) and close(P[1] - Q[1], a*math.sin(-math.pi/2 - T))
    T = 2*pi/3
    assert simplify(T - sin(T) - (2*pi/3 - sqrt(3)/2)) == 0 and 1 - cos(T) == Rational(3, 2)
    T = pi/2
    assert 2*(T - sin(T)) == pi - 2 and 2*(1 - cos(T)) == 2
    ys = [2*(1 - math.cos(2*math.pi*j/1000)) for j in range(1001)]
    assert close(max(ys), 4) and ys.index(max(ys)) == 500
    # 楕円と直線の距離
    def dist_range(a_, b_, A, B, C):
        best = []
        for j in range(200000):
            T = 2*math.pi*j/200000
            px, py = a_*math.cos(T), b_*math.sin(T)
            best.append((abs(A*px + B*py - C)/math.hypot(A, B), px, py))
        return min(best), max(best)
    mn, mx = dist_range(3, 2, 2, 3, 12)
    assert close(mn[0], (12 - 6*math.sqrt(2))*math.sqrt(13)/13, 1e-8) and close(mx[0], (12 + 6*math.sqrt(2))*math.sqrt(13)/13, 1e-8)
    assert close(mn[1], 3*math.sqrt(2)/2, 1e-4) and close(mn[2], math.sqrt(2), 1e-4)
    assert close(mx[1], -3*math.sqrt(2)/2, 1e-4) and close(mx[2], -math.sqrt(2), 1e-4)
    mn, mx = dist_range(2, 1, 1, 2, 6)
    assert close(mn[0], (6*math.sqrt(5) - 2*math.sqrt(10))/5, 1e-8) and close(mx[0], (6*math.sqrt(5) + 2*math.sqrt(10))/5, 1e-8)
    assert close(mn[1], math.sqrt(2), 1e-4) and close(mn[2], math.sqrt(2)/2, 1e-4)
    # 接線 2x+3y=6√2：点 (3√2/2, √2) における接線
    assert close((3*math.sqrt(2)/2)/9 * 12/math.sqrt(2), 2) and close(math.sqrt(2)/4 * 12/math.sqrt(2), 3)
    # 楕円上の点と頂点の距離の最大
    a = symbols("a", positive=True)
    f = (1 - a**2)*y**2 + 2*y + a**2 + 1
    assert expand(f - (a**2*(1 - y**2) + (y + 1)**2)) == 0
    assert simplify(f.subs(y, 1/(a**2 - 1)) - a**4/(a**2 - 1)) == 0
    assert simplify(expand(-(a**2 - 1)*(y - 1/(a**2 - 1))**2 + 1/(a**2 - 1) + a**2 + 1 - f)) == 0
    def maxBP(av, bv):
        m = 0; arg = None
        for j in range(100001):
            T = 2*math.pi*j/100000
            d = math.hypot(av*math.cos(T), bv*math.sin(T) + bv)
            if d > m: m, arg = d, (av*math.cos(T), bv*math.sin(T))
        return m, arg
    for av in (0.5, 1.0, 1.2, math.sqrt(2), 1.6, 2.0, 3.0):
        m, arg = maxBP(av, 1)
        pred = 2 if av <= math.sqrt(2) + 1e-12 else av*av/math.sqrt(av*av - 1)
        assert close(m, pred, 1e-6), (av, m, pred)
        if av > 1.5:
            assert close(abs(arg[0]), av*av*math.sqrt(av*av - 2)/(av*av - 1), 1e-3) and close(arg[1], 1/(av*av - 1), 1e-3)
    for av in (1.0, 2.0, 2.5, 2*math.sqrt(2), 3.0, 4.0):
        m, _ = maxBP(av, 2)
        pred = 4 if av <= 2*math.sqrt(2) + 1e-12 else av*av/math.sqrt(av*av - 4)
        assert close(m, pred, 1e-6), (av, m, pred)
    # 楕円に内接する三角形
    for _ in range(200):
        al = random.uniform(0, 2*math.pi)
        P = [(2*math.cos(al + 2*k*math.pi/3), math.sin(al + 2*k*math.pi/3)) for k in range(3)]
        assert close(sum(q[0] for q in P), 0) and close(sum(q[1] for q in P), 0)
        assert close(_tri_area(P), 3*math.sqrt(3)/2)
    best = 0
    for _ in range(100000):
        T = [random.uniform(0, 2*math.pi) for _ in range(3)]
        P = [(2*math.cos(s), math.sin(s)) for s in T]
        A_ = _tri_area(P); best = max(best, A_)
        assert A_ <= 3*math.sqrt(3)/2 + 1e-12
        P = [(3*math.cos(s), 2*math.sin(s)) for s in T]
        assert _tri_area(P) <= 9*math.sqrt(3)/2 + 1e-12
    assert best > 3*math.sqrt(3)/2 - 0.01
    assert close(_tri_area([(2, 0), (-1, math.sqrt(3)/2), (-1, -math.sqrt(3)/2)]), 3*math.sqrt(3)/2)
    tt = symbols("tt")
    assert expand((1 + tt)**3*(1 - tt) - Rational(1, 3)*(1 + tt)**3*(3 - 3*tt)) == 0
    assert Rational(1, 3)*Rational(3, 2)**4 == Rational(27, 16) and sqrt(Rational(27, 16)) == 3*sqrt(3)/4
    for _ in range(2000):
        R_ = random.uniform(0.01, math.pi - 0.01)
        assert (1 + math.cos(R_))*math.sin(R_) <= 3*math.sqrt(3)/4 + 1e-12

# ---------------------------------------------------------------- 節6
def fig_cardioid():
    f = Fig(-3.25, 1.9, -2.8, 3.05, 31)
    f.axes()
    f.circle((0, 0), 1, col=GRAY, w=1.0)
    f.curve(lambda t: (1 + 2 * (1 - math.cos(t)) * math.cos(t), 2 * (1 - math.cos(t)) * math.sin(t)), 0, 2 * math.pi, w=1.5)
    th = 2 * math.pi / 3
    Q = (2 * math.cos(th), 2 * math.sin(th)); T = (math.cos(th), math.sin(th))
    P = (2 * math.cos(th) - math.cos(2 * th), 2 * math.sin(th) - math.sin(2 * th))
    f.circle(Q, 1, col=RED, w=1.0, dash="3 2")
    f.seg(Q, P, col=RED, w=1.0); f.seg(Q, T, col=RED, w=1.0); f.seg((1, 0), P, col=GREEN, w=0.9, dash="3 2")
    f.dot(*Q); f.dot(*T); f.dot(*P, col=RED); f.dot(1, 0)
    f.text(*Q, "Q", -12, 4, size=10); f.text(*T, "T", 4, 11, size=10); f.text(*P, "P", -6, -4, anchor="end"); f.text(1, 0, "A", 3, 12, size=10)
    return f.svg()


def fig_perp_ell():
    f = Fig(-2.3, 2.3, -1.3, 1.3, 46)
    f.circle((0, 0), 2 / math.sqrt(5), col=GRAY, w=0.9, dash="3 2")
    f.axes()
    f.curve(ell(2, 1), 0, 2 * math.pi, w=1.5)
    th = 0.45
    r1 = 1 / math.sqrt(math.cos(th) ** 2 / 4 + math.sin(th) ** 2)
    r2 = 1 / math.sqrt(math.sin(th) ** 2 / 4 + math.cos(th) ** 2)
    P = (r1 * math.cos(th), r1 * math.sin(th)); Q = (-r2 * math.sin(th), r2 * math.cos(th))
    f.seg((0, 0), P, col=RED, w=1.0); f.seg((0, 0), Q, col=RED, w=1.0)
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    f.seg((P[0] - 0.25 * dx, P[1] - 0.25 * dy), (Q[0] + 0.25 * dx, Q[1] + 0.25 * dy), col=BLUE, w=1.1)
    f.dot(*P, col=RED); f.dot(*Q, col=RED)
    f.text(*P, "P", 4, -4); f.text(*Q, "Q", -6, -4, anchor="end")
    return f.svg()


def _chord_pts(A, B, fx, th):
    """楕円 x^2/A+y^2/B=1 と、(fx,0) を通る向き th の直線の交点のパラメータ r（2つ）"""
    c, s = math.cos(th), math.sin(th)
    qa = c * c / A + s * s / B; qb = 2 * fx * c / A; qc = fx * fx / A - 1
    D = math.sqrt(qb * qb - 4 * qa * qc)
    return (-qb + D) / (2 * qa), (-qb - D) / (2 * qa)


def fig_focal_ell():
    f = Fig(-2.3, 2.3, -1.95, 1.95, 44)
    f.axes()
    f.curve(ell(2, math.sqrt(3)), 0, 2 * math.pi, w=1.5)
    th = 0.6
    for ang, n1, n2, d1 in ((th, "A", "B", (4, -3)), (th + math.pi / 2, "C", "D", (-12, -3))):
        r1, r2 = _chord_pts(4, 3, 1, ang)
        P1 = (1 + r1 * math.cos(ang), r1 * math.sin(ang)); P2 = (1 + r2 * math.cos(ang), r2 * math.sin(ang))
        f.seg(P1, P2, col=RED, w=1.1)
        f.dot(*P1, col=RED); f.dot(*P2, col=RED)
        f.text(*P1, n1, d1[0], d1[1], size=10); f.text(*P2, n2, -12 if n2 == "B" else 5, 11, size=10)
    f.dot(1, 0); f.text(1, 0, "F", 4, 12, size=10)
    return f.svg()


SEC.append({"title": r"極座標と極方程式",
"base": r"""・極座標 $(r,\ \theta)$ と直交座標 $(x,\ y)$ の関係：$x=r\cos\theta,\ y=r\sin\theta$，$r^2=x^2+y^2$。<br>
・極方程式の例：原点中心・半径 $a$ の円 $r=a$；中心 $(a,\ 0)$・半径 $a$ の円 $r=2a\cos\theta$；極からの距離が $p$ で、極から下ろした垂線の向きが $\alpha$ の直線 $r\cos(\theta-\alpha)=p$。<br>
・2次曲線の極方程式：焦点を極とし、離心率を $e$，対応する準線を $x=-d$（$d>0$）とすると $r=\dfrac{ed}{1-e\cos\theta}$（準線が $x=d$ なら $r=\dfrac{ed}{1+e\cos\theta}$）。焦点からの距離や、焦点を通る弦の長さを扱うときに有効。""",
"items": [
 {"lv": 1, "title": r"極座標と直交座標の変換",
  "q": r"(1) 極座標が $\left(2,\ \dfrac23\pi\right)$，$\left(\sqrt2,\ -\dfrac\pi4\right)$ である点の直交座標を求めよ。<br>(2) 直交座標が $(-\sqrt3,\ 1)$，$(0,\ -2)$ である点の極座標 $(r,\ \theta)$ を求めよ。ただし $r>0$，$0\leqq\theta<2\pi$ とする。<br>(3) 極座標が $\mathrm{A}\left(3,\ \dfrac\pi6\right)$，$\mathrm{B}\left(4,\ \dfrac\pi2\right)$ である2点について、線分 $\mathrm{AB}$ の長さと $\triangle\mathrm{OAB}$ の面積を求めよ（$\mathrm{O}$ は極）。",
  "hint": r"$x=r\cos\theta,\ y=r\sin\theta$。逆は $r=\sqrt{x^2+y^2}$ を求め、$\cos\theta=\dfrac xr,\ \sin\theta=\dfrac yr$ から $\theta$ を決める。(3) は $\angle\mathrm{AOB}$ が偏角の差になるので、余弦定理と面積の公式が使える。",
  "sol": r"(1) $\left(2\cos\dfrac23\pi,\ 2\sin\dfrac23\pi\right)=\boldsymbol{(-1,\ \sqrt3)}$，$\left(\sqrt2\cos\left(-\dfrac\pi4\right),\ \sqrt2\sin\left(-\dfrac\pi4\right)\right)=\boldsymbol{(1,\ -1)}$<br>"
         r"(2) $(-\sqrt3,\ 1)$ について：$r=\sqrt{3+1}=2$，$\cos\theta=-\dfrac{\sqrt3}2,\ \sin\theta=\dfrac12$ より $\theta=\dfrac56\pi$。よって $\boldsymbol{\left(2,\ \dfrac56\pi\right)}$<br>"
         r"$(0,\ -2)$ について：$r=2$，$\cos\theta=0,\ \sin\theta=-1$ より $\theta=\dfrac32\pi$。よって $\boldsymbol{\left(2,\ \dfrac32\pi\right)}$<br>"
         r"(3) $\angle\mathrm{AOB}=\dfrac\pi2-\dfrac\pi6=\dfrac\pi3$ であるから、余弦定理より<br>$\mathrm{AB}^2=3^2+4^2-2\cdot3\cdot4\cos\dfrac\pi3=13$，$\mathrm{AB}=\boldsymbol{\sqrt{13}}$<br>"
         r"$\triangle\mathrm{OAB}=\dfrac12\cdot3\cdot4\sin\dfrac\pi3=\boldsymbol{3\sqrt3}$",
  "note": r"極座標では、同じ点が $\left(2,\ \dfrac56\pi+2n\pi\right)$（$n$ は整数）のように何通りにも表される。偏角の範囲を指定して1通りに決める。",
  "ex": r"(1) 極座標が $\left(4,\ \dfrac76\pi\right)$ の点の直交座標を求めよ。<br>(2) 直交座標が $(1,\ -1)$ の点の極座標を求めよ（$r>0$，$0\leqq\theta<2\pi$）。<br>(3) 極座標が $\mathrm{A}\left(2,\ \dfrac\pi{12}\right)$，$\mathrm{B}\left(3,\ \dfrac34\pi\right)$ の2点について、$\mathrm{AB}$ の長さと $\triangle\mathrm{OAB}$ の面積を求めよ。",
  "exa": r"(1) $(-2\sqrt3,\ -2)$　(2) $\left(\sqrt2,\ \dfrac74\pi\right)$　(3) $\mathrm{AB}=\sqrt{19}$，$\triangle\mathrm{OAB}=\dfrac{3\sqrt3}2$"},
 {"lv": 2, "title": r"極方程式と直交座標の方程式の書き換え",
  "q": r"(1) 極方程式 $r\cos\left(\theta-\dfrac\pi3\right)=2$，$r=2\cos\theta+2\sqrt3\sin\theta$ を、それぞれ直交座標の方程式で表し、どのような図形か答えよ。<br>(2) 円 $(x-3)^2+y^2=9$ を極方程式で表せ。",
  "hint": r"加法定理で展開し、$r\cos\theta=x$，$r\sin\theta=y$，$r^2=x^2+y^2$ に置き換える。$r=\cdots$ の形は両辺に $r$ を掛けると置き換えやすい。",
  "sol": r"(1) $r\cos\left(\theta-\dfrac\pi3\right)=\dfrac12r\cos\theta+\dfrac{\sqrt3}2r\sin\theta=2$ より $\dfrac12x+\dfrac{\sqrt3}2y=2$。<br>よって　<b>直線 $x+\sqrt3y=4$</b><br>"
         r"$r=2\cos\theta+2\sqrt3\sin\theta$ の両辺に $r$ を掛けて $r^2=2r\cos\theta+2\sqrt3r\sin\theta$，すなわち $x^2+y^2=2x+2\sqrt3y$。<br>"
         r"よって　<b>円 $(x-1)^2+(y-\sqrt3)^2=4$</b>（中心 $(1,\ \sqrt3)$，半径 $2$）<br>"
         r"（$r$ を掛けたときに加わる極 $r=0$ は、もとの方程式でも $\theta=-\dfrac\pi6$ のとき表されている。）<br>"
         r"(2) $x^2+y^2=6x$ より $r^2=6r\cos\theta$。$r=0$ は $r=6\cos\theta$ で $\theta=\dfrac\pi2$ とした場合に含まれるから<br>$\boldsymbol{r=6\cos\theta}$",
  "note": r"$r\cos(\theta-\alpha)=p$ は、極から直線に下ろした垂線の長さが $p$，その垂線の向きが $\alpha$ である直線を表す。(1) の直線 $x+\sqrt3y=4$ は、原点からの距離が $2$，垂線の向きが $\dfrac\pi3$ になっている。",
  "ex": r"(1) 極方程式 $r\sin\left(\theta+\dfrac\pi6\right)=1$，$r=4\cos\theta-2\sin\theta$ を直交座標の方程式で表せ。<br>(2) 円 $x^2+(y-2)^2=4$ を極方程式で表せ。",
  "exa": r"(1) $x+\sqrt3y=2$；$(x-2)^2+(y+1)^2=5$　(2) $r=4\sin\theta$"},
 {"lv": 3, "title": r"2次曲線の極方程式（焦点を極とする）",
  "q": r"(1) 極方程式 $r=\dfrac{6}{2+\cos\theta}$ を直交座標の方程式で表し、どのような曲線か答えよ。<br>(2) 放物線 $y^2=4(x+1)$ を、原点を極、$x$ 軸の正の部分を始線とする極方程式で表せ。",
  "hint": r"(1) $2r=6-r\cos\theta=6-x$ として両辺を2乗する。(2) 原点はこの放物線の焦点である。「焦点までの距離＝準線までの距離」を極座標で書くとすぐに求まる。",
  "sol": r"(1) 分母を払って $2r=6-r\cos\theta=6-x$。両辺を2乗して<br>$4(x^2+y^2)=(6-x)^2$，$3x^2+12x+4y^2=36$，$3(x+2)^2+4y^2=48$<br>"
         r"すなわち　$\boldsymbol{\dfrac{(x+2)^2}{16}+\dfrac{y^2}{12}=1}$<br>"
         r"（$r>0$ より $6-x>0$ が必要だが、この楕円上では $x\leqq2$ なので常に成り立つ。）<br>"
         r"これは中心 $(-2,\ 0)$，$a=4$，$b=2\sqrt3$，$c=\sqrt{16-12}=2$ の楕円で、焦点は $(0,\ 0)$，$(-4,\ 0)$。極は焦点の1つで、離心率は $e=\dfrac ca=\dfrac12$ である。<br>"
         r"(2) $y^2=4(x+1)$ は $y^2=4x$ を $x$ 軸方向に $-1$ だけ平行移動したもので、焦点は $(0,\ 0)$，準線は $x=-2$。<br>"
         r"放物線上の点 $\mathrm{P}(r,\ \theta)$ について、焦点（極）までの距離 $r$ と準線までの距離 $r\cos\theta+2$ が等しいから $r=r\cos\theta+2$。<br>"
         r"よって　$\boldsymbol{r=\dfrac{2}{1-\cos\theta}}$",
  "note": r"(1) は $r=\dfrac{3}{1+\frac12\cos\theta}$ と書けて、$e=\dfrac12$，準線は $x=6$。楕円・放物線・双曲線が、離心率 $e$ の値だけを変えた1つの式で表されるのが極方程式の利点である（$0<e<1$ で楕円，$e=1$ で放物線，$e>1$ で双曲線）。",
  "ex": r"(1) 極方程式 $r=\dfrac{4}{3-\cos\theta}$ を直交座標の方程式で表せ。<br>(2) 放物線 $y^2=-8(x-2)$ を、原点を極、$x$ 軸の正の部分を始線とする極方程式で表せ。",
  "exa": r"(1) $\dfrac{4}{9}\left(x-\dfrac12\right)^2+\dfrac{y^2}{2}=1$　(2) $r=\dfrac{4}{1+\cos\theta}$"},
 {"lv": 4, "title": r"円の外側を転がる円（カージオイド）と極方程式",
  "q": r"円 $O:x^2+y^2=1$ の外側を、半径 $1$ の円 $C$ が $O$ に外接しながら、滑ることなく反時計回りに転がる。はじめ $C$ の中心は $(2,\ 0)$ にあり、$C$ 上の点 $\mathrm{P}$ は $\mathrm{A}(1,\ 0)$ にある。$C$ の中心が原点のまわりに角 $\theta$ だけ回ったとき、次の問いに答えよ。<br>(1) $\mathrm{P}$ の座標を $\theta$ で表せ。<br>(2) $\mathrm{A}$ を極、$x$ 軸の正の向きを始線とする極座標で、$\mathrm{P}$ の軌跡を極方程式で表せ。<br>(3) $\mathrm{P}$ の $y$ 座標の最大値を求めよ。",
  "hint": r"接点 $\mathrm{T}$ は $(\cos\theta,\ \sin\theta)$。滑らないので、$O$ 上の弧 $\mathrm{AT}$ と $C$ 上の弧 $\mathrm{TP}$ の長さはともに $\theta$。$C$ の中心から見た $\mathrm{P}$ の向きは、$\mathrm{T}$ の向き $\theta+\pi$ からさらに $\theta$ 回った $2\theta+\pi$ になる。(3) は相加平均と相乗平均の関係を使う。",
  "sol": fig_cardioid() + r"(1) $C$ の中心を $\mathrm{Q}$ とすると $\mathrm{Q}(2\cos\theta,\ 2\sin\theta)$，接点は $\mathrm{T}(\cos\theta,\ \sin\theta)$ で、$\mathrm{Q}$ から見た $\mathrm{T}$ の向きは $\theta+\pi$。<br>"
         r"滑らないから、$C$ 上の弧 $\mathrm{TP}$ の長さは $O$ 上の弧 $\mathrm{AT}$ の長さ $\theta$ に等しく、$\angle\mathrm{TQP}=\theta$。$\mathrm{P}$ はすでに $O$ と接し終えた側（$\mathrm{A}$ の側）にあるから、$\mathrm{Q}$ から見た $\mathrm{P}$ の向きは $\theta+\pi$ から反時計回りに $\theta$ 回った $2\theta+\pi$ である。<br>"
         r"$\overrightarrow{\mathrm{QP}}=(\cos(2\theta+\pi),\ \sin(2\theta+\pi))=(-\cos2\theta,\ -\sin2\theta)$ より<br>"
         r"$\boldsymbol{\mathrm{P}(2\cos\theta-\cos2\theta,\ 2\sin\theta-\sin2\theta)}$<br>"
         r"(2) $\cos2\theta=2\cos^2\theta-1$，$\sin2\theta=2\sin\theta\cos\theta$ より<br>"
         r"$\overrightarrow{\mathrm{AP}}=(2\cos\theta-2\cos^2\theta,\ 2\sin\theta-2\sin\theta\cos\theta)=2(1-\cos\theta)(\cos\theta,\ \sin\theta)$<br>"
         r"$2(1-\cos\theta)\geqq0$ だから、$\mathrm{A}$ を極とすると $\mathrm{P}$ は極からの距離 $2(1-\cos\theta)$，偏角 $\theta$ の点である。よって、極方程式は　$\boldsymbol{r=2(1-\cos\theta)}$<br>"
         r"(3) $y=2\sin\theta(1-\cos\theta)$。$y$ の最大を調べるには $y>0$，すなわち $0<\theta<\pi$ の場合を考えればよい。$c=\cos\theta$（$-1<c<1$）とおくと<br>"
         r"$y^2=4(1-c^2)(1-c)^2=4(1+c)(1-c)^3=\dfrac43(3+3c)(1-c)^3$<br>"
         r"$3+3c>0$，$1-c>0$ であり、相加平均と相乗平均の関係より<br>"
         r"$(3+3c)(1-c)^3\leqq\left\{\dfrac{(3+3c)+3(1-c)}{4}\right\}^4=\left(\dfrac32\right)^4=\dfrac{81}{16}$<br>"
         r"よって $y^2\leqq\dfrac43\cdot\dfrac{81}{16}=\dfrac{27}4$，$y\leqq\dfrac{3\sqrt3}2$。等号は $3+3c=1-c$，すなわち $c=-\dfrac12$（$\theta=\dfrac23\pi$）のとき成り立つ。<br>"
         r"最大値は　$\boldsymbol{\dfrac{3\sqrt3}2}$",
  "note": r"この曲線をカージオイド（心臓形）といい、エピサイクロイドの一種である。$\mathrm{AP}=2(1-\cos\theta)$ は $\theta=\pi$ のとき最大値 $4$ をとる。図は $\theta=\dfrac23\pi$ の位置（(3) で $y$ が最大になる位置）。",
  "ex": r"円 $x^2+y^2=4$ の外側を、半径 $2$ の円が外接しながら滑ることなく反時計回りに転がる。はじめ転がる円の中心は $(4,\ 0)$，円上の点 $\mathrm{P}$ は $\mathrm{A}(2,\ 0)$ にある。中心が原点のまわりに $\theta$ だけ回ったときの $\mathrm{P}$ の座標、$\mathrm{A}$ を極とする $\mathrm{P}$ の軌跡の極方程式、$\mathrm{AP}$ の最大値を求めよ。",
  "exa": r"$\mathrm{P}(4\cos\theta-2\cos2\theta,\ 4\sin\theta-2\sin2\theta)$；$r=4(1-\cos\theta)$；$8$"},
 {"lv": 5, "title": r"楕円上の直交する2点と極座標（定円に接する弦・面積の範囲）",
  "q": r"楕円 $E:\dfrac{x^2}{4}+y^2=1$ 上の2点 $\mathrm{P},\ \mathrm{Q}$ が、原点 $\mathrm{O}$ に対して $\angle\mathrm{POQ}=\dfrac\pi2$ を満たしながら動く。<br>(1) $\dfrac1{\mathrm{OP}^2}+\dfrac1{\mathrm{OQ}^2}$ は一定であることを示せ。<br>(2) 直線 $\mathrm{PQ}$ はある定円につねに接することを示せ。<br>(3) $\triangle\mathrm{OPQ}$ の面積の最大値と最小値を求めよ。",
  "hint": r"$\mathrm{O}$ を極とする極座標で $\mathrm{P}(r_1,\ \theta)$，$\mathrm{Q}\left(r_2,\ \theta+\dfrac\pi2\right)$ とおくと、直交条件が偏角の差になり、楕円の式から $\dfrac1{r_1^2},\ \dfrac1{r_2^2}$ が $\theta$ の簡単な式になる。(2) は直角三角形 $\mathrm{OPQ}$ の斜辺に下ろした垂線の長さを考える。",
  "sol": fig_perp_ell() + r"必要なら $\mathrm{P}$ と $\mathrm{Q}$ を入れかえて、$\mathrm{P}(r_1\cos\theta,\ r_1\sin\theta)$，$\mathrm{Q}\left(r_2\cos\left(\theta+\dfrac\pi2\right),\ r_2\sin\left(\theta+\dfrac\pi2\right)\right)=(-r_2\sin\theta,\ r_2\cos\theta)$（$r_1,\ r_2>0$）とおける。<br>"
         r"$\mathrm{P}$ が $E$ 上にあるから $\dfrac{r_1^2\cos^2\theta}4+r_1^2\sin^2\theta=1$，すなわち $\dfrac1{r_1^2}=\dfrac{\cos^2\theta}4+\sin^2\theta$。<br>"
         r"同様に $\dfrac1{r_2^2}=\dfrac{\sin^2\theta}4+\cos^2\theta$。<br>"
         r"(1) $\dfrac1{\mathrm{OP}^2}+\dfrac1{\mathrm{OQ}^2}=\dfrac1{r_1^2}+\dfrac1{r_2^2}=\dfrac14+1=\dfrac54$（一定）<br>"
         r"(2) $\mathrm{O}$ から直線 $\mathrm{PQ}$ に下ろした垂線の長さを $h$ とすると、直角三角形 $\mathrm{OPQ}$ の面積を2通りに表して $h\cdot\mathrm{PQ}=r_1r_2$。$\mathrm{PQ}^2=r_1^2+r_2^2$ より<br>"
         r"$\dfrac1{h^2}=\dfrac{r_1^2+r_2^2}{r_1^2r_2^2}=\dfrac1{r_1^2}+\dfrac1{r_2^2}=\dfrac54$，$h=\dfrac2{\sqrt5}$<br>"
         r"$h$ が一定だから、直線 $\mathrm{PQ}$ はつねに円 $\boldsymbol{x^2+y^2=\dfrac45}$ に接する。<br>"
         r"(3) $\triangle\mathrm{OPQ}=\dfrac12r_1r_2$ である。<br>"
         r"$\dfrac1{r_1^2r_2^2}=\left(\dfrac{\cos^2\theta}4+\sin^2\theta\right)\left(\dfrac{\sin^2\theta}4+\cos^2\theta\right)=\dfrac{\cos^4\theta+\sin^4\theta}{4}+\dfrac{17}{16}\sin^2\theta\cos^2\theta$<br>"
         r"$=\dfrac{1-2\sin^2\theta\cos^2\theta}{4}+\dfrac{17}{16}\sin^2\theta\cos^2\theta=\dfrac14+\dfrac9{16}\sin^2\theta\cos^2\theta=\dfrac14+\dfrac9{64}\sin^22\theta$<br>"
         r"$0\leqq\sin^22\theta\leqq1$ より $\dfrac14\leqq\dfrac1{r_1^2r_2^2}\leqq\dfrac{25}{64}$，すなわち $\dfrac85\leqq r_1r_2\leqq2$。<br>"
         r"よって　<b>最大値 $1$</b>（$\theta=0$ など、$\mathrm{P},\ \mathrm{Q}$ が楕円の頂点のとき），<b>最小値 $\dfrac45$</b>（$\theta=\dfrac\pi4$ などのとき）",
  "note": r"一般に楕円 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$ では $\dfrac1{\mathrm{OP}^2}+\dfrac1{\mathrm{OQ}^2}=\dfrac1{a^2}+\dfrac1{b^2}$ となり、直線 $\mathrm{PQ}$ は円 $x^2+y^2=\dfrac{a^2b^2}{a^2+b^2}$ に接する。直交座標のまま $\mathrm{P},\ \mathrm{Q}$ を扱うと計算が重いが、極座標では「原点からの距離」と「向き」が分かれるので、直交条件が偏角の差 $\dfrac\pi2$ として簡単に表せる。",
  "ex": r"楕円 $\dfrac{x^2}{9}+\dfrac{y^2}{3}=1$ 上の2点 $\mathrm{P},\ \mathrm{Q}$ が $\angle\mathrm{POQ}=\dfrac\pi2$ を満たして動くとき、$\dfrac1{\mathrm{OP}^2}+\dfrac1{\mathrm{OQ}^2}$ の値、直線 $\mathrm{PQ}$ がつねに接する円の方程式、$\triangle\mathrm{OPQ}$ の面積の最大値と最小値を求めよ。",
  "exa": r"$\dfrac49$；$x^2+y^2=\dfrac94$；最大値 $\dfrac{3\sqrt3}2$，最小値 $\dfrac94$"},
 {"lv": 5, "title": r"直交する焦点弦の長さの和（2次曲線の極方程式）",
  "q": r"楕円 $E:\dfrac{x^2}{4}+\dfrac{y^2}{3}=1$ の焦点 $\mathrm{F}(1,\ 0)$ を通り、互いに直交する2直線が $E$ と交わる点を、それぞれ $\mathrm{A},\ \mathrm{B}$ および $\mathrm{C},\ \mathrm{D}$ とする。<br>(1) $\mathrm{F}$ を極、$x$ 軸の正の向きを始線とする極座標で、$E$ の極方程式を求めよ。<br>(2) $\dfrac1{\mathrm{AB}}+\dfrac1{\mathrm{CD}}$ は一定であることを示せ。<br>(3) $\mathrm{AB}+\mathrm{CD}$ のとり得る値の範囲を求めよ。",
  "hint": r"点 $(1+r\cos\theta,\ r\sin\theta)$ を楕円の式に代入すると、$r$ の2次方程式が因数分解できる。焦点弦 $\mathrm{AB}$ は偏角 $\theta$ と $\theta+\pi$ の2点を結ぶので、$\mathrm{AB}=r(\theta)+r(\theta+\pi)$。(3) は $\cos^2\theta$ と $\sin^2\theta$ の対称性を使って $\sin^22\theta$ の式にする。",
  "sol": fig_focal_ell() + r"(1) $E$ 上の点を $(1+r\cos\theta,\ r\sin\theta)$（$r>0$）とおいて $3x^2+4y^2=12$ に代入すると<br>"
         r"$3(1+r\cos\theta)^2+4r^2\sin^2\theta=12$<br>$r^2(3\cos^2\theta+4\sin^2\theta)+6r\cos\theta-9=0$<br>"
         r"$3\cos^2\theta+4\sin^2\theta=4-\cos^2\theta$ より<br>$r^2(2+\cos\theta)(2-\cos\theta)+6r\cos\theta-9=0$<br>"
         r"$\{r(2+\cos\theta)-3\}\{r(2-\cos\theta)+3\}=0$<br>"
         r"$r>0$ より $r(2-\cos\theta)+3>0$ だから　$\boldsymbol{r=\dfrac{3}{2+\cos\theta}}$<br>"
         r"(2) 直線 $\mathrm{AB}$ の向きを $\theta$ とすると、$\mathrm{A},\ \mathrm{B}$ は偏角 $\theta,\ \theta+\pi$ の点であるから<br>"
         r"$\mathrm{AB}=\dfrac3{2+\cos\theta}+\dfrac3{2-\cos\theta}=\dfrac{12}{4-\cos^2\theta}$<br>"
         r"$\mathrm{C},\ \mathrm{D}$ は偏角 $\theta+\dfrac\pi2,\ \theta+\dfrac32\pi$ の点で、$\cos\left(\theta+\dfrac\pi2\right)=-\sin\theta$ だから、同様に $\mathrm{CD}=\dfrac{12}{4-\sin^2\theta}$。<br>"
         r"よって　$\dfrac1{\mathrm{AB}}+\dfrac1{\mathrm{CD}}=\dfrac{(4-\cos^2\theta)+(4-\sin^2\theta)}{12}=\dfrac7{12}$（一定）<br>"
         r"(3) $X=4-\cos^2\theta$，$Y=4-\sin^2\theta$ とおくと $X+Y=7$ で<br>"
         r"$\mathrm{AB}+\mathrm{CD}=12\left(\dfrac1X+\dfrac1Y\right)=\dfrac{12(X+Y)}{XY}=\dfrac{84}{XY}$<br>"
         r"$XY=16-4(\cos^2\theta+\sin^2\theta)+\sin^2\theta\cos^2\theta=12+\dfrac14\sin^22\theta$<br>"
         r"$0\leqq\sin^22\theta\leqq1$ より $12\leqq XY\leqq\dfrac{49}4$。よって $\dfrac{84\cdot4}{49}\leqq\mathrm{AB}+\mathrm{CD}\leqq\dfrac{84}{12}$，すなわち<br>"
         r"$\boldsymbol{\dfrac{48}7\leqq\mathrm{AB}+\mathrm{CD}\leqq7}$<br>"
         r"（最大は $\theta=0$ で長軸 $4$ と通径 $3$ の組のとき、最小は $\theta=\dfrac\pi4$ のとき。）",
  "note": r"一般に焦点を極とする極方程式 $r=\dfrac{l}{1+e\cos\theta}$ を用いると、焦点弦の長さは $\dfrac{2l}{1-e^2\cos^2\theta}$ となり、直交する2本の焦点弦について $\dfrac1{\mathrm{AB}}+\dfrac1{\mathrm{CD}}=\dfrac{2-e^2}{2l}$ が一定になる。焦点からの距離を扱う問題では、焦点を極にとるのが定石である。",
  "ex": r"楕円 $\dfrac{x^2}{2}+y^2=1$ の焦点 $\mathrm{F}(1,\ 0)$ を通り互いに直交する2直線が楕円と交わる点を、それぞれ $\mathrm{A},\ \mathrm{B}$ および $\mathrm{C},\ \mathrm{D}$ とする。$\mathrm{F}$ を極とする楕円の極方程式、$\dfrac1{\mathrm{AB}}+\dfrac1{\mathrm{CD}}$ の値、$\mathrm{AB}+\mathrm{CD}$ のとり得る値の範囲を求めよ。",
  "exa": r"$r=\dfrac{1}{\sqrt2+\cos\theta}$；$\dfrac{3\sqrt2}4$；$\dfrac{8\sqrt2}3\leqq\mathrm{AB}+\mathrm{CD}\leqq3\sqrt2$"},
]})


def _v6():
    x, y, th, r = symbols("x y theta r", real=True)
    def pc(rr, t):
        return (rr*math.cos(t), rr*math.sin(t))
    assert all(close(u, v) for u, v in zip(pc(2, 2*math.pi/3), (-1, math.sqrt(3))))
    assert all(close(u, v) for u, v in zip(pc(math.sqrt(2), -math.pi/4), (1, -1)))
    assert all(close(u, v) for u, v in zip(pc(2, 5*math.pi/6), (-math.sqrt(3), 1)))
    assert all(close(u, v) for u, v in zip(pc(2, 3*math.pi/2), (0, -2)))
    assert all(close(u, v) for u, v in zip(pc(4, 7*math.pi/6), (-2*math.sqrt(3), -2)))
    assert all(close(u, v) for u, v in zip(pc(math.sqrt(2), 7*math.pi/4), (1, -1)))
    def ab_area(r1, t1, r2, t2):
        P, Q = pc(r1, t1), pc(r2, t2)
        return math.hypot(P[0]-Q[0], P[1]-Q[1]), abs(P[0]*Q[1] - P[1]*Q[0])/2
    d, S_ = ab_area(3, math.pi/6, 4, math.pi/2); assert close(d, math.sqrt(13)) and close(S_, 3*math.sqrt(3))
    d, S_ = ab_area(2, math.pi/12, 3, 3*math.pi/4); assert close(d, math.sqrt(19)) and close(S_, 3*math.sqrt(3)/2)
    # 極方程式の書き換え
    X, Y = r*cos(th), r*sin(th)
    assert simplify(expand_trig(r*cos(th - pi/3)) - (X/2 + sqrt(3)*Y/2)) == 0
    assert simplify(expand_trig(r*sin(th + pi/6)) - (X + sqrt(3)*Y)/2) == 0
    for _ in range(100):
        t = random.uniform(0, 2*math.pi)
        rr = 2*math.cos(t) + 2*math.sqrt(3)*math.sin(t); P = pc(rr, t)
        assert close((P[0]-1)**2 + (P[1]-math.sqrt(3))**2, 4)
        rr = 6*math.cos(t); P = pc(rr, t); assert close((P[0]-3)**2 + P[1]**2, 9)
        rr = 4*math.cos(t) - 2*math.sin(t); P = pc(rr, t); assert close((P[0]-2)**2 + (P[1]+1)**2, 5)
        rr = 4*math.sin(t); P = pc(rr, t); assert close(P[0]**2 + (P[1]-2)**2, 4)
        # 2次曲線の極方程式
        rr = 6/(2 + math.cos(t)); P = pc(rr, t); assert close((P[0]+2)**2/16 + P[1]**2/12, 1)
        rr = 4/(3 - math.cos(t)); P = pc(rr, t); assert close(4*(P[0]-0.5)**2/9 + P[1]**2/2, 1)
        if abs(math.cos(t) - 1) > 1e-3:
            rr = 2/(1 - math.cos(t)); P = pc(rr, t); assert close(P[1]**2, 4*(P[0]+1), 1e-6*(1+rr*rr))
        if abs(math.cos(t) + 1) > 1e-3:
            rr = 4/(1 + math.cos(t)); P = pc(rr, t); assert close(P[1]**2, -8*(P[0]-2), 1e-6*(1+rr*rr))
    assert 2*math.cos(-math.pi/6) + 2*math.sqrt(3)*math.sin(-math.pi/6) < 1e-12
    assert expand(4*(x**2 + y**2) - (6 - x)**2 - (3*(x+2)**2 + 4*y**2 - 48)) == 0
    assert expand(9*(x**2 + y**2) - (4 + x)**2 - 18*(Rational(4, 9)*(x - Rational(1, 2))**2 + y**2/2 - 1)) == 0
    # カージオイド：P の向き 2θ+π が「滑らない」ことを、任意の物質点の接地時の速度 0 で確認
    for _ in range(100):
        f0 = random.uniform(0, 2*math.pi); T = -f0   # 方向 π+f0+2θ の点が接点になるのは θ=-f0
        v = (-2*math.sin(T) - 2*math.sin(math.pi + f0 + 2*T), 2*math.cos(T) + 2*math.cos(math.pi + f0 + 2*T))
        assert close(v[0], 0) and close(v[1], 0)
        P = (2*math.cos(T) + math.cos(math.pi + f0 + 2*T), 2*math.sin(T) + math.sin(math.pi + f0 + 2*T))
        assert close(P[0], math.cos(T)) and close(P[1], math.sin(T))      # そのとき接点 T と一致
    for _ in range(100):
        t = random.uniform(0, 2*math.pi)
        P = (2*math.cos(t) - math.cos(2*t), 2*math.sin(t) - math.sin(2*t))
        assert close(math.hypot(P[0] - 2*math.cos(t), P[1] - 2*math.sin(t)), 1)
        rr = 2*(1 - math.cos(t)); assert close(P[0] - 1, rr*math.cos(t)) and close(P[1], rr*math.sin(t))
        P2 = (4*math.cos(t) - 2*math.cos(2*t), 4*math.sin(t) - 2*math.sin(2*t))
        rr = 4*(1 - math.cos(t)); assert close(P2[0] - 2, rr*math.cos(t)) and close(P2[1], rr*math.sin(t))
    ys = [2*math.sin(t)*(1 - math.cos(t)) for t in [2*math.pi*j/300000 for j in range(300000)]]
    assert close(max(ys), 3*math.sqrt(3)/2, 1e-9)
    c = symbols("c")
    assert expand(4*(1 - c**2)*(1 - c)**2 - Rational(4, 3)*(3 + 3*c)*(1 - c)**3) == 0
    assert Rational(4, 3)*Rational(81, 16) == Rational(27, 4)
    # 直交する2点
    def perp(A, B):
        S1, S2, H = [], [], []
        for j in range(20000):
            t = 2*math.pi*j/20000
            r1 = 1/math.sqrt(math.cos(t)**2/A + math.sin(t)**2/B)
            r2 = 1/math.sqrt(math.sin(t)**2/A + math.cos(t)**2/B)
            P, Q = pc(r1, t), pc(r2, t + math.pi/2)
            assert close(P[0]**2/A + P[1]**2/B, 1) and close(Q[0]**2/A + Q[1]**2/B, 1)
            S1.append(1/r1**2 + 1/r2**2)
            H.append(abs(P[0]*Q[1] - P[1]*Q[0]) / math.hypot(P[0]-Q[0], P[1]-Q[1]))
            S2.append(r1*r2/2)
        return S1, H, S2
    S1, H, S2 = perp(4, 1)
    assert all(close(v, 1.25) for v in S1) and all(close(h, 2/math.sqrt(5)) for h in H)
    assert close(max(S2), 1, 1e-9) and close(min(S2), 0.8, 1e-9)
    S1, H, S2 = perp(9, 3)
    assert all(close(v, 4/9) for v in S1) and all(close(h, 1.5) for h in H)
    assert close(max(S2), 3*math.sqrt(3)/2, 1e-9) and close(min(S2), 9/4, 1e-9)
    t = symbols("t")
    e1 = (cos(t)**2/4 + sin(t)**2)*(sin(t)**2/4 + cos(t)**2) - (Rational(1, 4) + Rational(9, 64)*sin(2*t)**2)
    assert simplify(expand(expand_trig(e1))) == 0
    # 直交する焦点弦
    rr = symbols("rr")
    assert expand((rr*(2 + cos(th)) - 3)*(rr*(2 - cos(th)) + 3) - (rr**2*(3*cos(th)**2 + 4*sin(th)**2) + 6*rr*cos(th) - 9)).subs(sin(th)**2, 1 - cos(th)**2).expand() == 0
    assert expand((rr*(sqrt(2) + cos(th)) - 1)*(rr*(sqrt(2) - cos(th)) + 1) - (rr**2*(2 - cos(th)**2) + 2*rr*cos(th) - 1)) == 0
    def focal(A, B, fx, inv, lo, hi):
        sums = []
        for j in range(20000):
            a1 = math.pi*j/20000
            r1, r2 = _chord_pts(A, B, fx, a1); AB = abs(r1 - r2)
            r3, r4 = _chord_pts(A, B, fx, a1 + math.pi/2); CD = abs(r3 - r4)
            assert close(1/AB + 1/CD, inv)
            sums.append(AB + CD)
        assert close(min(sums), lo, 1e-9) and close(max(sums), hi, 1e-9)
    focal(4, 3, 1, 7/12, 48/7, 7)
    focal(2, 1, 1, 3*math.sqrt(2)/4, 8*math.sqrt(2)/3, 3*math.sqrt(2))
    for _ in range(50):
        t_ = random.uniform(0, 2*math.pi)
        rr_ = 3/(2 + math.cos(t_)); assert close((1 + rr_*math.cos(t_))**2/4 + (rr_*math.sin(t_))**2/3, 1)
        rr_ = 1/(math.sqrt(2) + math.cos(t_)); assert close((1 + rr_*math.cos(t_))**2/2 + (rr_*math.sin(t_))**2, 1)

# ================================================================ 章のまとめ
CH = {"no": 21, "sections": SEC}


def verify():
    random.seed(21)
    g = globals()
    for k in range(1, 10):
        if f"_v{k}" in g:
            g[f"_v{k}"]()
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert 27 <= len(items) <= 33, len(items)
    assert cnt[5] >= 3 and all(cnt[k] >= 3 for k in range(1, 6)), cnt
    assert 4 <= len(SEC) <= 9
    for sec in SEC:                       # 節の中は易しい順
        lvs = [it["lv"] for it in sec["items"]]
        assert lvs == sorted(lvs), sec["title"]
    for it in items:
        for k in ("title", "q", "hint", "sol", "ex", "exa"):
            assert it.get(k), (it["title"], k)
        for k in ("q", "hint", "sol", "note", "ex", "exa"):
            assert "$$" not in it.get(k, ""), (it["title"], k)
            assert it.get(k, "").count("$") % 2 == 0, (it["title"], k)
