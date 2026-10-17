"""第14章 微分法（数学II）。節ごとに SEC.append(...)、各節の検算は _vN()、最後に CH と verify()。"""
import math
import random
from fractions import Fraction as Fr
from sympy import (symbols, Rational, sqrt, expand, factor, diff, limit, simplify, solve, Poly,
                   rem, S, Symbol)

SEC = []

# ---------------------------------------------------------------- 図・表の道具
C1, C2, CG, CF = "#16367a", "#d9701e", "#888888", "#cfdcf3"
DASH = ' stroke-dasharray="3,2"'


class _F:
    """数学座標で描いて SVG 文字列にする小さな道具（座標は Python で計算）。"""

    def __init__(s, W, H, xr, yr, m=9):
        s.W, s.H, s.m = W, H, m
        s.x0, s.x1 = xr
        s.y0, s.y1 = yr
        s.o = []

    def X(s, x):
        return round(s.m + (x - s.x0) / (s.x1 - s.x0) * (s.W - 2 * s.m), 1)

    def Y(s, y):
        return round(s.m + (s.y1 - y) / (s.y1 - s.y0) * (s.H - 2 * s.m), 1)

    def axes(s, xl="x", yl="y", o="O"):
        X0, Y0 = s.X(0), s.Y(0)
        xa, xb, ya, yb = s.X(s.x0), s.X(s.x1), s.Y(s.y0), s.Y(s.y1)
        s.o.append(f'<line x1="{xa}" y1="{Y0}" x2="{xb}" y2="{Y0}" stroke="#333" stroke-width="0.8"/>')
        s.o.append(f'<polygon points="{xb + 3},{Y0} {xb - 3},{Y0 - 2.6} {xb - 3},{Y0 + 2.6}" fill="#333"/>')
        s.o.append(f'<line x1="{X0}" y1="{ya}" x2="{X0}" y2="{yb}" stroke="#333" stroke-width="0.8"/>')
        s.o.append(f'<polygon points="{X0},{yb - 3} {X0 - 2.6},{yb + 3} {X0 + 2.6},{yb + 3}" fill="#333"/>')
        s.o.append(f'<text x="{xb - 1}" y="{Y0 - 4}" text-anchor="end" font-style="italic" font-family="serif" font-size="11">{xl}</text>')
        s.o.append(f'<text x="{X0 + 5}" y="{yb + 6}" font-style="italic" font-family="serif" font-size="11">{yl}</text>')
        if o:
            s.o.append(f'<text x="{X0 - 3}" y="{Y0 + 10}" text-anchor="end" font-style="italic" font-family="serif" font-size="10">{o}</text>')

    def curve(s, f, a, b, col=C1, w=1.5, dash="", n=240):
        segs, cur, prev = [], [], None
        for i in range(n + 1):
            x = a + (b - a) * i / n
            y = f(x)
            ins = s.y0 <= y <= s.y1
            if prev is not None and ins != prev[2]:
                px, py, _ = prev
                yb = s.y1 if max(py, y) > s.y1 else s.y0
                xb = px + (x - px) * (yb - py) / (y - py)
                cur.append((xb, yb))
                if not ins:
                    segs.append(cur)
                    cur = []
            if ins:
                cur.append((x, y))
            prev = (x, y, ins)
        if cur:
            segs.append(cur)
        for sg in segs:
            if len(sg) > 1:
                s.o.append(f'<polyline fill="none" stroke="{col}" stroke-width="{w}"{dash} points="'
                           + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in sg) + '"/>')

    def seg(s, p, q, col=CG, w=0.8, dash=DASH):
        s.o.append(f'<line x1="{s.X(p[0])}" y1="{s.Y(p[1])}" x2="{s.X(q[0])}" y2="{s.Y(q[1])}" stroke="{col}" stroke-width="{w}"{dash}/>')

    def pt(s, x, y, col=C1, r=1.9, fill=None):
        f = col if fill is None else fill
        s.o.append(f'<circle cx="{s.X(x)}" cy="{s.Y(y)}" r="{r}" fill="{f}" stroke="{col}" stroke-width="0.9"/>')

    def txt(s, x, y, t, dx=0, dy=0, anc="middle", it=False, size=10, col="#222"):
        st = ' font-style="italic" font-family="serif"' if it else ""
        s.o.append(f'<text x="{round(s.X(x) + dx, 1)}" y="{round(s.Y(y) + dy, 1)}" text-anchor="{anc}" font-size="{size}" fill="{col}"{st}>{t}</text>')

    def poly(s, pts, fill=CF, op=0.85):
        s.o.append(f'<polygon points="' + " ".join(f"{s.X(p)},{s.Y(q)}" for p, q in pts)
                   + f'" fill="{fill}" fill-opacity="{op}" stroke="none"/>')

    def band(s, lo, hi, a, b, n=120):
        """a≦x≦b で lo(x)＜y＜hi(x) の部分を塗る（枠で切る）。"""
        cl = lambda v: min(max(v, s.y0), s.y1)
        xs = [a + (b - a) * i / n for i in range(n + 1)]
        s.poly([(x, cl(hi(x))) for x in xs] + [(x, cl(lo(x))) for x in reversed(xs)])

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" font-size="10">'
                + "".join(s.o) + "</svg>")


def _tb(*rows):
    """増減表。rows の各行は [見出し, セル, ...]（すべて raw 文字列）。"""
    h = "<table>"
    for r in rows:
        h += "<tr><th>" + r[0] + "</th>" + "".join("<td>" + c + "</td>" for c in r[1:]) + "</tr>"
    return h + "</table>"


UP, DN = r"$\nearrow$", r"$\searrow$"

# ---------------------------------------------------------------- 節1
SEC.append({"title": "微分係数と導関数",
"base": r"""・平均変化率 $\dfrac{f(b)-f(a)}{b-a}$，微分係数 $f'(a)=\displaystyle\lim_{h\to0}\dfrac{f(a+h)-f(a)}{h}=\lim_{x\to a}\dfrac{f(x)-f(a)}{x-a}$<br>
・導関数 $f'(x)=\displaystyle\lim_{h\to0}\dfrac{f(x+h)-f(x)}{h}$。公式：$(x^n)'=nx^{n-1}$（$n$ は自然数），$(c)'=0$（$c$ は定数），$\{kf(x)+lg(x)\}'=kf'(x)+lg'(x)$<br>
・$\{(ax+b)^n\}'=na(ax+b)^{n-1}$（展開して確かめられる）<br>
・整式 $f(x)$ が $(x-a)^2$ で割り切れる $\iff$ $f(a)=0$ かつ $f'(a)=0$""",
"items": [
 {"lv": 1, "title": "平均変化率と微分係数の定義",
  "q": r"関数 $f(x)=x^2-3x$ について、次の問いに答えよ。<br>(1) $x$ の値が $1$ から $1+h$ まで変化するときの平均変化率を求めよ。ただし、$h\neq0$ とする。<br>(2) 微分係数の定義に従って、$f'(1)$ を求めよ。<br>(3) 導関数の定義に従って、$f'(x)$ を求めよ。",
  "hint": r"平均変化率は（$y$ の増加量）÷（$x$ の増加量）。その $h\to0$ のときの極限が微分係数である。分母の $h$ を約分してから極限をとる。",
  "sol": r"(1) $f(1+h)-f(1)=\{(1+h)^2-3(1+h)\}-(1^2-3\cdot1)=(h^2-h-2)-(-2)=h^2-h$<br>"
         r"よって、平均変化率は　$\dfrac{h^2-h}{h}=\boldsymbol{h-1}$<br>"
         r"(2) $f'(1)=\displaystyle\lim_{h\to0}\dfrac{f(1+h)-f(1)}{h}=\lim_{h\to0}(h-1)=\boldsymbol{-1}$<br>"
         r"(3) $f(x+h)-f(x)=\{(x+h)^2-3(x+h)\}-(x^2-3x)=2xh+h^2-3h$ であるから<br>"
         r"$f'(x)=\displaystyle\lim_{h\to0}\dfrac{2xh+h^2-3h}{h}=\lim_{h\to0}(2x-3+h)=\boldsymbol{2x-3}$",
  "note": r"(3) の結果に $x=1$ を代入すると $f'(1)=-1$ となり、(2) と一致する。$h\to0$ は「$h$ を $0$ と異なる値をとりながら $0$ に限りなく近づける」ことで、$h=0$ を代入するのではない（$h=0$ では分母が $0$ になる）。だから、先に約分して分母の $h$ を消しておく。",
  "ex": r"関数 $f(x)=x^3+x$ について、微分係数の定義に従って $f'(2)$ を求めよ。",
  "exa": r"$f'(2)=13$"},
 {"lv": 1, "title": "導関数の計算（展開してから微分する）",
  "q": r"次の関数を微分せよ。ただし、(4) は $r$ について微分せよ。<br>(1) $y=2x^3-5x^2+3x-7$　　(2) $y=(2x-1)(x^2+3)$<br>(3) $y=(3x+2)^3$　　(4) $V=\dfrac43\pi r^3$",
  "hint": r"積や累乗の形はまず展開し、各項を $(x^n)'=nx^{n-1}$ で微分する。(4) のように $x$ 以外の文字の関数でも、何が変数かを意識すれば同じように微分できる。",
  "sol": r"(1) $y'=2\cdot3x^2-5\cdot2x+3=\boldsymbol{6x^2-10x+3}$<br>"
         r"(2) $y=2x^3-x^2+6x-3$ より　$y'=\boldsymbol{6x^2-2x+6}$<br>"
         r"(3) $y=27x^3+54x^2+36x+8$ より　$y'=\boldsymbol{81x^2+108x+36}$<br>"
         r"(4) $\dfrac{dV}{dr}=\dfrac43\pi\cdot3r^2=\boldsymbol{4\pi r^2}$",
  "note": r"(3) は公式 $\{(ax+b)^n\}'=na(ax+b)^{n-1}$ を使うと $y'=3\cdot3(3x+2)^2=9(3x+2)^2$ と速い（展開すると $81x^2+108x+36$ に一致する）。(4) の結果は球の表面積に等しい。半径が少し増えたときの体積の増加は「表面積×厚さ」にほぼ等しいからである。",
  "ex": r"次の関数を微分せよ。ただし、(4) は $t$ について微分し、$v_0,\ g$ は定数とする。<br>(1) $y=-x^3+4x^2-x+5$　　(2) $y=(x+2)(3x^2-x)$<br>(3) $y=(1-2x)^3$　　(4) $h=v_0t-\dfrac12gt^2$",
  "exa": r"(1) $y'=-3x^2+8x-1$　(2) $y'=9x^2+10x-2$　(3) $y'=-24x^2+24x-6$　(4) $\dfrac{dh}{dt}=v_0-gt$"},
 {"lv": 1, "title": "微分係数の条件から関数を決定する",
  "q": r"2次関数 $f(x)=ax^2+bx+c$ が $f(1)=4$，$f'(1)=1$，$f'(-1)=-7$ を満たすとき、定数 $a,\ b,\ c$ の値を求めよ。",
  "hint": r"導関数 $f'(x)=2ax+b$ を求め、3つの条件を $a,\ b,\ c$ の連立方程式に直す。",
  "sol": r"$f'(x)=2ax+b$ であるから、条件より<br>"
         r"$f'(1)=2a+b=1$ …①，$f'(-1)=-2a+b=-7$ …②，$f(1)=a+b+c=4$ …③<br>"
         r"①，②より $a=2$，$b=-3$。③より $c=5$。<br>よって　$\boldsymbol{a=2,\ b=-3,\ c=5}$",
  "ex": r"3次関数 $f(x)=x^3+ax^2+bx+c$ が $f(0)=2$，$f'(1)=0$，$f'(2)=5$ を満たすとき、定数 $a,\ b,\ c$ の値を求めよ。",
  "exa": r"$a=-2,\ b=1,\ c=2$"},
 {"lv": 2, "title": "微分係数の定義を利用する極限",
  "q": r"関数 $f(x)$ の $x=a$ における微分係数 $f'(a)$ が存在するとき、次の極限値を $a,\ f(a),\ f'(a)$ を用いて表せ。<br>"
       r"(1) $\displaystyle\lim_{h\to0}\dfrac{f(a+3h)-f(a-h)}{h}$　　(2) $\displaystyle\lim_{x\to a}\dfrac{x^2f(a)-a^2f(x)}{x-a}$",
  "hint": r"定義の形 $\dfrac{f(a+k)-f(a)}{k}\ (k\to0)$ をつくる。(1) は分子で $f(a)$ を引いて足し、分母をそれぞれ $3h$，$-h$ に合わせる。(2) は分子で $a^2f(a)$ を引いて足す。",
  "sol": r"(1) $\dfrac{f(a+3h)-f(a-h)}{h}=\dfrac{f(a+3h)-f(a)}{h}-\dfrac{f(a-h)-f(a)}{h}$<br>"
         r"$=3\cdot\dfrac{f(a+3h)-f(a)}{3h}+\dfrac{f(a-h)-f(a)}{-h}$<br>"
         r"$h\to0$ のとき $3h\to0$，$-h\to0$ であるから、求める極限値は　$3f'(a)+f'(a)=\boldsymbol{4f'(a)}$<br>"
         r"(2) $x^2f(a)-a^2f(x)=(x^2-a^2)f(a)-a^2\{f(x)-f(a)\}$ であるから<br>"
         r"$\dfrac{x^2f(a)-a^2f(x)}{x-a}=(x+a)f(a)-a^2\cdot\dfrac{f(x)-f(a)}{x-a}$<br>"
         r"$x\to a$ として、求める極限値は　$\boldsymbol{2af(a)-a^2f'(a)}$",
  "note": r"定義の式では、分子が「$f(a+k)-f(a)$」の形で、分母がその $k$ と同じでなければならない。(1) を分母が $h$ のまま「$f'(a)$ の定義の形」とみて $f'(a)$ と答えるのはよくある誤りである。",
  "ex": r"関数 $f(x)$ の $x=a$ における微分係数 $f'(a)$ が存在するとき、次の極限値を $a,\ f(a),\ f'(a)$ を用いて表せ。<br>"
        r"(1) $\displaystyle\lim_{h\to0}\dfrac{f(a+2h)-f(a-3h)}{h}$　　(2) $\displaystyle\lim_{x\to a}\dfrac{xf(a)-af(x)}{x-a}$",
  "exa": r"(1) $5f'(a)$　(2) $f(a)-af'(a)$"},
 {"lv": 3, "title": "導関数を含む等式から整式を決定する（次数の決定）",
  "q": r"整式 $f(x)$ が、すべての実数 $x$ について $f(x)f'(x)=2x^3-3x^2+x$ を満たすとき、$f(x)$ を求めよ。",
  "hint": r"まず $f(x)$ の次数を決める。$f(x)$ が $n$ 次（$n\geqq1$）なら $f(x)f'(x)$ は $2n-1$ 次になる。次数が決まれば、係数を文字でおいて恒等式の係数を比較する。",
  "sol": r"$f(x)$ が定数のとき、$f'(x)=0$ より左辺は $0$ となり、不適。<br>"
         r"$f(x)$ の次数を $n\ (n\geqq1)$，$x^n$ の係数を $p\ (p\neq0)$ とすると、$f'(x)$ の最高次の項は $npx^{n-1}$ であるから、左辺の最高次の項は $np^2x^{2n-1}$ である。右辺は3次式であるから $2n-1=3$，よって $n=2$。<br>"
         r"$f(x)=ax^2+bx+c\ (a\neq0)$ とおくと、$f'(x)=2ax+b$ で<br>"
         r"$f(x)f'(x)=2a^2x^3+3abx^2+(b^2+2ac)x+bc$<br>"
         r"これが $2x^3-3x^2+x$ と恒等的に等しいから、係数を比較して<br>"
         r"$2a^2=2$ …①，$3ab=-3$ …②，$b^2+2ac=1$ …③，$bc=0$ …④<br>"
         r"②より $ab=-1$ であるから $b\neq0$，よって④より $c=0$。このとき③は $b^2=1$。①より $a=\pm1$ で、$ab=-1$ と合わせて $(a,\ b)=(1,\ -1),\ (-1,\ 1)$。<br>"
         r"したがって　$\boldsymbol{f(x)=x^2-x,\ \ -x^2+x}$",
  "note": r"次数が分からない整式は、<b>最高次の項に注目して次数を決める</b>のが定石である。左辺 $f(x)f'(x)$ は $f(x)$ を $-f(x)$ に変えても変わらないので、答えが $\pm$ の対で現れる。",
  "ex": r"整式 $f(x)$ が、すべての実数 $x$ について $f(x)f'(x)=8x^3+6x^2-3x-1$ を満たすとき、$f(x)$ を求めよ。",
  "exa": r"$f(x)=2x^2+x-1,\ \ -2x^2-x+1$"},
 {"lv": 3, "title": r"$(x-a)^2$ で割ったときの余り（微分の利用）",
  "q": r"(1) 整式 $f(x)$ が $(x-a)^2$ で割り切れるための必要十分条件は、$f(a)=0$ かつ $f'(a)=0$ であることを証明せよ。<br>"
       r"(2) $n$ を2以上の自然数とする。$x^n$ を $(x-1)^2$ で割ったときの余りを求めよ。",
  "hint": r"$f(x)$ を $(x-a)^2$ で割った商を $Q(x)$，余りを $px+q$ とおき、$f(a)$ と $f'(a)$ を $p,\ q$ で表す。$g(x)=(x-a)^2Q(x)$ の $x=a$ における微分係数は、定義に戻ると $0$ と分かる。",
  "sol": r"(1) $f(x)$ を $(x-a)^2$ で割った商を $Q(x)$，余りを $px+q$ とすると　$f(x)=(x-a)^2Q(x)+px+q$<br>"
         r"$g(x)=(x-a)^2Q(x)$ とおくと $g(a)=0$ で<br>"
         r"$g'(a)=\displaystyle\lim_{x\to a}\dfrac{g(x)-g(a)}{x-a}=\lim_{x\to a}(x-a)Q(x)=0$<br>"
         r"$f(x)=g(x)+px+q$ であるから　$f(a)=pa+q$，$f'(a)=g'(a)+p=p$<br>"
         r"よって　$f(a)=f'(a)=0\iff p=0,\ pa+q=0\iff p=q=0$<br>"
         r"$p=q=0$ は $f(x)$ が $(x-a)^2$ で割り切れることにほかならないから、示された。<br>"
         r"(2) $x^n=(x-1)^2Q(x)+px+q$ とおく。$f(x)=x^n$ とすると、(1) の計算から $f(1)=p+q$，$f'(1)=p$。<br>"
         r"$f(1)=1$，$f'(1)=n\cdot1^{n-1}=n$ であるから $p=n$，$q=1-n$。<br>"
         r"よって、余りは　$\boldsymbol{nx-n+1}$",
  "note": r"(2) は二項定理でも求められる：$x^n=\{(x-1)+1\}^n=1+n(x-1)+{}_n\mathrm{C}_2(x-1)^2+\cdots$ で、${}_n\mathrm{C}_2(x-1)^2$ 以降の項は $(x-1)^2$ で割り切れるから、余りは $1+n(x-1)$。(1) の性質は「接する」の言いかえ（第2節）や3次関数の性質（第6節）でくり返し使う。",
  "ex": r"$n$ を2以上の自然数とする。$x^n$ を $(x+1)^2$ で割ったときの余りを求めよ。",
  "exa": r"$(-1)^{n-1}(nx+n-1)$"},
]})


def _v1():
    x, h, a = symbols("x h a")
    f = x**2 - 3*x
    assert expand((f.subs(x, 1 + h) - f.subs(x, 1)) / h * h) == expand((h - 1) * h)
    assert expand(f.subs(x, 1 + h)) == h**2 - h - 2 and f.subs(x, 1) == -2
    assert limit((f.subs(x, 1 + h) - f.subs(x, 1)) / h, h, 0) == -1
    assert expand(f.subs(x, x + h) - f) == expand(2*x*h + h**2 - 3*h)
    assert simplify(limit((f.subs(x, x + h) - f) / h, h, 0) - (2*x - 3)) == 0
    g = x**3 + x
    assert limit((g.subs(x, 2 + h) - g.subs(x, 2)) / h, h, 0) == 13
    # 1.2
    assert diff(2*x**3 - 5*x**2 + 3*x - 7, x) == 6*x**2 - 10*x + 3
    assert expand((2*x - 1)*(x**2 + 3)) == 2*x**3 - x**2 + 6*x - 3
    assert expand(diff((2*x - 1)*(x**2 + 3), x)) == 6*x**2 - 2*x + 6
    assert expand((3*x + 2)**3) == 27*x**3 + 54*x**2 + 36*x + 8
    assert expand(diff((3*x + 2)**3, x)) == 81*x**2 + 108*x + 36 == expand(9*(3*x + 2)**2)
    r, t, v0, gg = symbols("r t v0 g")
    assert diff(Rational(4, 3)*S.Pi*r**3, r) == 4*S.Pi*r**2
    assert expand(diff(-x**3 + 4*x**2 - x + 5, x)) == -3*x**2 + 8*x - 1
    assert expand(diff((x + 2)*(3*x**2 - x), x)) == 9*x**2 + 10*x - 2
    assert expand(diff((1 - 2*x)**3, x)) == -24*x**2 + 24*x - 6
    assert diff(v0*t - gg*t**2/2, t) == v0 - gg*t
    # 1.3
    A, B, Cc = symbols("A B C")
    F = A*x**2 + B*x + Cc
    sol = solve([F.subs(x, 1) - 4, diff(F, x).subs(x, 1) - 1, diff(F, x).subs(x, -1) + 7], [A, B, Cc], dict=True)
    assert sol == [{A: 2, B: -3, Cc: 5}]
    F = x**3 + A*x**2 + B*x + Cc
    sol = solve([F.subs(x, 0) - 2, diff(F, x).subs(x, 1), diff(F, x).subs(x, 2) - 5], [A, B, Cc], dict=True)
    assert sol == [{A: -2, B: 1, Cc: 2}]
    # 1.4 いろいろな整式 f と点 a で極限を計算
    random.seed(14)
    for _ in range(6):
        cs = [random.randint(-5, 5) for _ in range(5)]
        fx = sum(c * x**k for k, c in enumerate(cs))
        av = Rational(random.randint(-9, 9), random.randint(1, 4))
        fa, fpa = fx.subs(x, av), diff(fx, x).subs(x, av)
        assert limit((fx.subs(x, av + 3*h) - fx.subs(x, av - h)) / h, h, 0) == 4 * fpa
        assert limit((x**2 * fa - av**2 * fx) / (x - av), x, av) == 2*av*fa - av**2 * fpa
        assert limit((fx.subs(x, av + 2*h) - fx.subs(x, av - 3*h)) / h, h, 0) == 5 * fpa
        assert limit((x * fa - av * fx) / (x - av), x, av) == fa - av * fpa
    # 1.5 係数比較の連立を解く
    for rhs, ans in [(2*x**3 - 3*x**2 + x, {x**2 - x, -x**2 + x}),
                     (8*x**3 + 6*x**2 - 3*x - 1, {2*x**2 + x - 1, -2*x**2 - x + 1})]:
        F = A*x**2 + B*x + Cc
        eqs = Poly(expand(F * diff(F, x) - rhs), x).all_coeffs()
        sols = solve(eqs, [A, B, Cc], dict=True)
        assert {expand(F.subs(s)) for s in sols} == ans
        for p in ans:
            assert expand(p * diff(p, x) - rhs) == 0
    assert expand((A*x**2 + B*x + Cc)*(2*A*x + B)) == expand(2*A**2*x**3 + 3*A*B*x**2 + (B**2 + 2*A*Cc)*x + B*Cc)
    # 1.6
    for n in range(2, 25):
        assert rem(x**n, (x - 1)**2, x) == n*x - n + 1
        assert expand(rem(x**n, (x + 1)**2, x) - (-1)**(n - 1) * (n*x + n - 1)) == 0


# ---------------------------------------------------------------- 節2
_f = _F(200, 172, (-1.75, 1.75), (-2.3, 2.3))
_f.band(lambda x: -x, lambda x: x**3 - x, 0, 1.75)
_f.band(lambda x: x**3 - x, lambda x: -x, -1.75, 0)
_f.axes()
_f.curve(lambda x: x**3 - x, -1.75, 1.75)
_f.curve(lambda x: -x, -1.75, 1.75, col=C2, w=1.2)
_f.txt(1, 0, "1", dy=11)
_f.txt(-1, 0, "−1", dy=-4)
_f.txt(1.5, 2.1, "y=x³−x", dx=-6, anc="end", it=True, col=C1)
_f.txt(-1.7, 1.75, "y=−x", dx=2, dy=-3, anc="start", it=True, col=C2)
FIG27 = _f.svg()

_f = _F(190, 150, (-0.55, 1.15), (-0.85, 2.3))
_f.axes("t", "Y")
_f.curve(lambda t: 9*t**4 - 8*t**3, -0.55, 1.15)
_f.seg((-0.55, -16/27), (1.15, -16/27))
_f.seg((2/3, 0), (2/3, -16/27))
_f.seg((-0.55, 1.3), (1.15, 1.3), col=C2, w=1.1, dash="")
_f.txt(-0.53, 1.3, "Y=4c", dy=-4, anc="start", it=True, col=C2)
_f.pt(2/3, -16/27)
_f.txt(2/3, 0, "2/3", dy=-4)
_f.txt(0, -16/27, "−16/27", dx=-3, dy=-3, anc="end")
FIG28 = _f.svg()

_f = _F(200, 140, (-1.4, 1.4), (-1.5, 0.62))
_f.axes("t", "Y")
_f.curve(lambda t: -3*t**4 + 2*t**2, -1.4, 1.4)
_f.seg((-1.4, 1/3), (1.4, 1/3))
_f.seg((-1.4, -1), (1.4, -1))
for _s in (1, -1):
    _f.pt(_s / math.sqrt(3), 1/3)
    _f.pt(_s, -1)
    _f.seg((_s, 0), (_s, -1))
_f.txt(1, 0, "1", dy=-4)
_f.txt(-1, 0, "−1", dy=-4)
_f.txt(0, 1/3, "1/3", dx=3, dy=-3, anc="start")
_f.txt(0, -1, "−1", dx=-3, dy=11, anc="end")
FIG29 = _f.svg()

SEC.append({"title": "接線",
"base": r"""・曲線 $y=f(x)$ 上の点 $(a,\ f(a))$ における接線：$y-f(a)=f'(a)(x-a)$<br>
・曲線外の点 $(p,\ q)$ を通る接線：接点を $(t,\ f(t))$ とおいて接線の方程式をつくり、$(p,\ q)$ を通る条件から $t$ を求める<br>
・2曲線 $y=f(x)$，$y=g(x)$ が $x=t$ の点で接する $\iff$ $f(t)=g(t)$ かつ $f'(t)=g'(t)$<br>
・直線 $y=mx+n$ が曲線 $y=f(x)$ に $x=t$ の点で接する $\iff$ $f(x)-(mx+n)$ が $(x-t)^2$ で割り切れる""",
"items": [
 {"lv": 1, "title": "曲線上の点における接線",
  "q": r"曲線 $y=x^3-2x^2+1$ 上の点 $(2,\ 1)$ における接線の方程式を求めよ。",
  "hint": r"点 $(a,\ f(a))$ における接線の傾きは微分係数 $f'(a)$ である。",
  "sol": r"$y'=3x^2-4x$ であるから、$x=2$ における微分係数は $3\cdot2^2-4\cdot2=4$。<br>"
         r"よって、接線の方程式は $y-1=4(x-2)$，すなわち　$\boldsymbol{y=4x-7}$",
  "note": r"点 $(a,\ f(a))$ を通り、その点における接線に垂直な直線を<b>法線</b>という。$f'(a)\neq0$ のとき、法線の方程式は $y-f(a)=-\dfrac1{f'(a)}(x-a)$。この例題では $y=-\dfrac14x+\dfrac32$ となる。",
  "ex": r"曲線 $y=-x^3+3x$ 上の点 $(2,\ -2)$ における接線の方程式を求めよ。",
  "exa": r"$y=-9x+16$"},
 {"lv": 1, "title": "傾きが与えられた接線",
  "q": r"曲線 $y=x^3-3x$ の接線のうち、傾きが $9$ であるものの方程式を求めよ。",
  "hint": r"接点の $x$ 座標を $t$ とおき、$f'(t)=9$ から $t$ を求める。接点が1つとは限らない。",
  "sol": r"$y'=3x^2-3$。接点の $x$ 座標を $t$ とすると、$3t^2-3=9$ より $t^2=4$，$t=\pm2$。<br>"
         r"$t=2$ のとき、接点は $(2,\ 2)$ で、接線は $y-2=9(x-2)$，すなわち $y=9x-16$<br>"
         r"$t=-2$ のとき、接点は $(-2,\ -2)$ で、接線は $y+2=9(x+2)$，すなわち $y=9x+16$<br>"
         r"よって　$\boldsymbol{y=9x-16,\ \ y=9x+16}$",
  "ex": r"曲線 $y=x^3+3x^2$ の接線のうち、傾きが $9$ であるものの方程式を求めよ。",
  "exa": r"$y=9x-5,\ \ y=9x+27$"},
 {"lv": 2, "title": "曲線外の点・曲線上の点を通る接線",
  "q": r"曲線 $C:y=x^3-3x$ について、次の接線の方程式を求めよ。<br>(1) 点 $(2,\ -6)$ から $C$ に引いた接線　　(2) $C$ 上の点 $\mathrm{A}(2,\ 2)$ を通る $C$ の接線",
  "hint": r"接点を $(t,\ t^3-3t)$ とおいて接線の方程式をつくり、それが与えられた点を通る条件から $t$ を求める。(2) は「A における接線」だけとは限らない。",
  "sol": r"$y'=3x^2-3$ より、$C$ 上の点 $(t,\ t^3-3t)$ における接線の方程式は<br>"
         r"$y-(t^3-3t)=(3t^2-3)(x-t)$，すなわち　$y=(3t^2-3)x-2t^3$ …①<br>"
         r"(1) ①が点 $(2,\ -6)$ を通るとき　$-6=2(3t^2-3)-2t^3$<br>"
         r"整理して $t^3-3t^2=0$，$t^2(t-3)=0$ より $t=0,\ 3$。①に代入して　$\boldsymbol{y=-3x,\ \ y=24x-54}$<br>"
         r"(2) ①が点 $(2,\ 2)$ を通るとき　$2=2(3t^2-3)-2t^3$<br>"
         r"整理して $t^3-3t^2+4=0$，$(t+1)(t-2)^2=0$ より $t=-1,\ 2$。①に代入して　$\boldsymbol{y=2,\ \ y=9x-16}$",
  "note": r"(2) の $t=2$ は A における接線、$t=-1$ は点 $(-1,\ 2)$ で接して A を通る接線である。「A における接線」と「A を通る接線」の違いに注意しよう。$t^3-3t^2+4=0$ が $t=2$ を重解にもつのは偶然ではなく、A における接線が A で $C$ に接していることの表れである。",
  "ex": r"曲線 $y=x^3-2x$ について、次の接線の方程式を求めよ。<br>(1) 点 $(0,\ 2)$ から引いた接線　　(2) 曲線上の点 $(1,\ -1)$ を通る接線",
  "exa": r"(1) $y=x+2$　(2) $y=x-2,\ \ y=-\dfrac54x+\dfrac14$"},
 {"lv": 2, "title": "2つの放物線の共通接線",
  "q": r"2つの放物線 $y=x^2$ と $y=-x^2+6x-5$ の両方に接する直線の方程式を求めよ。",
  "hint": r"一方の放物線の接線を接点の $x$ 座標 $t$ で表し、それがもう一方の放物線に接する条件（連立してできる2次方程式の判別式 $=0$）を考える。",
  "sol": r"放物線 $y=x^2$ 上の点 $(t,\ t^2)$ における接線は、$y'=2x$ より<br>"
         r"$y=2t(x-t)+t^2$，すなわち　$y=2tx-t^2$ …①<br>"
         r"①が放物線 $y=-x^2+6x-5$ に接するのは、$-x^2+6x-5=2tx-t^2$，すなわち<br>"
         r"$x^2+2(t-3)x+5-t^2=0$<br>が重解をもつときである。判別式を $D$ とすると<br>"
         r"$\dfrac D4=(t-3)^2-(5-t^2)=2t^2-6t+4=2(t-1)(t-2)=0$<br>"
         r"よって $t=1,\ 2$ で、①に代入して　$\boldsymbol{y=2x-1,\ \ y=4x-4}$",
  "note": r"別解：2つ目の放物線上の点 $(s,\ -s^2+6s-5)$ における接線 $y=(-2s+6)x+s^2-5$ と①が一致する条件 $2t=-2s+6$，$-t^2=s^2-5$ を解いてもよい（$(t,\ s)=(1,\ 2),\ (2,\ 1)$）。一方が3次以上の曲線のときは判別式が使えないので、この「接線の一致」の方法を使う。",
  "ex": r"2つの放物線 $y=x^2+1$ と $y=-x^2-2x$ の両方に接する直線の方程式を求めよ。",
  "exa": r"$y=1,\ \ y=-2x$"},
 {"lv": 3, "title": "2曲線が接する条件",
  "q": r"2曲線 $y=x^3-x$ と $y=x^2+a$ が接するような定数 $a$ の値と、そのときの接点の座標を求めよ。ただし、2曲線がある点で接するとは、その点を共有し、その点における2曲線の接線が一致することをいう。",
  "hint": r"接点の $x$ 座標を $t$ とおくと、「$y$ 座標が等しい」「接線の傾き（微分係数）が等しい」の2式が成り立つ。",
  "sol": r"$f(x)=x^3-x$，$g(x)=x^2+a$ とおくと　$f'(x)=3x^2-1$，$g'(x)=2x$<br>"
         r"2曲線が $x=t$ の点で接する条件は　$f(t)=g(t)$ …①，$f'(t)=g'(t)$ …②<br>"
         r"②より $3t^2-1=2t$，$(t-1)(3t+1)=0$，よって $t=1,\ -\dfrac13$。<br>"
         r"①より $a=t^3-t-t^2$ であるから<br>"
         r"$t=1$ のとき $a=-1$ で、接点は $(1,\ 0)$<br>"
         r"$t=-\dfrac13$ のとき $a=-\dfrac1{27}+\dfrac13-\dfrac19=\dfrac5{27}$ で、接点は $\left(-\dfrac13,\ \dfrac8{27}\right)$<br>"
         r"よって　$\boldsymbol{a=-1}$ のとき接点 $\boldsymbol{(1,\ 0)}$，$\boldsymbol{a=\dfrac5{27}}$ のとき接点 $\boldsymbol{\left(-\dfrac13,\ \dfrac8{27}\right)}$",
  "note": r"「接する」は「$x^3-x=x^2+a$，すなわち $h(x)=x^3-x^2-x-a=0$ が重解をもつ」と言いかえられる。重解 $t$ の条件 $h(t)=h'(t)=0$（第1節の割り切れる条件）は①，②と同じ式である。",
  "ex": r"2曲線 $y=x^3$ と $y=3x^2+a$ が接するような定数 $a$ の値と、そのときの接点の座標を求めよ。",
  "exa": r"$a=0$ のとき接点 $(0,\ 0)$，$a=-4$ のとき接点 $(2,\ 8)$"},
 {"lv": 4, "title": "4次関数のグラフに2点で接する直線",
  "q": r"$a$ を定数とする。曲線 $C:y=x^4-2x^3+ax^2$ に異なる2点で接する直線が存在するような $a$ の値の範囲を求めよ。また、そのとき、その直線の方程式を $a$ で表せ。",
  "hint": r"直線 $y=mx+n$ が $C$ と $x=\alpha$ の点で接する $\iff$ $x^4-2x^3+ax^2-(mx+n)$ が $(x-\alpha)^2$ で割り切れる。異なる2点 $\alpha,\ \beta$ で接するなら、この4次式は $(x-\alpha)^2(x-\beta)^2$ に等しい。$\alpha+\beta$，$\alpha\beta$ を文字でおいて係数を比較する。",
  "sol": r"直線 $\ell:y=mx+n$ と $C$ が $x=\alpha$ の点で接するのは、$h(x)=x^4-2x^3+ax^2-(mx+n)$ について $h(\alpha)=h'(\alpha)=0$，すなわち $h(x)$ が $(x-\alpha)^2$ で割り切れるときである。<br>"
         r"よって、$\ell$ が $C$ と異なる2点 $x=\alpha,\ \beta$ で接する $\iff$ $h(x)$ が $(x-\alpha)^2(x-\beta)^2$ で割り切れる $\iff$ $h(x)=(x-\alpha)^2(x-\beta)^2$（$h(x)$ は $x^4$ の係数が $1$ の4次式だから）。<br>"
         r"$\alpha+\beta=s$，$\alpha\beta=p$ とおくと、$(x-\alpha)(x-\beta)=x^2-sx+p$ であり<br>"
         r"$(x^2-sx+p)^2=x^4-2sx^3+(s^2+2p)x^2-2spx+p^2$<br>"
         r"これが $h(x)=x^4-2x^3+ax^2-mx-n$ と一致する条件は<br>"
         r"$-2s=-2$，$s^2+2p=a$，$-2sp=-m$，$p^2=-n$<br>"
         r"よって　$s=1$，$p=\dfrac{a-1}2$，$m=2sp=a-1$，$n=-p^2=-\dfrac{(a-1)^2}4$<br>"
         r"$\alpha,\ \beta$ は $X^2-sX+p=0$ の2解であるから、これらが異なる実数である条件は<br>"
         r"$s^2-4p=1-2(a-1)=3-2a>0$，すなわち $a<\dfrac32$<br>"
         r"したがって、求める範囲は $\boldsymbol{a<\dfrac32}$ で、直線の方程式は　$\boldsymbol{y=(a-1)x-\dfrac{(a-1)^2}4}$",
  "note": r"この条件は「$f(x)=x^4-2x^3+ax^2$ が極値を3つもつ」条件（$f'(x)=2x(2x^2-3x+a)=0$ が異なる3実数解をもつ：$a<\dfrac98$，$a\neq0$）とは一致しない。たとえば $a=\dfrac65$ のとき、$f(x)$ の極値は $x=0$ での極小値だけだが、$C$ に2点で接する直線 $y=\dfrac15x-\dfrac1{100}$ が存在する。",
  "ex": r"$a$ を定数とする。曲線 $y=x^4-4x^3+ax^2$ に異なる2点で接する直線が存在するような $a$ の値の範囲を求めよ。また、そのとき、その直線の方程式を $a$ で表せ。",
  "exa": r"$a<6$，$y=2(a-4)x-\dfrac{(a-4)^2}4$"},
 {"lv": 4, "title": "3次関数のグラフに引ける接線の本数",
  "q": r"点 $\mathrm{P}(a,\ b)$ から曲線 $C:y=x^3-x$ に3本の接線が引けるような点 P の存在範囲を図示せよ。",
  "hint": r"接点の $x$ 座標 $t$ についての3次方程式をつくる。3次関数のグラフでは異なる接点の接線は一致しないので、接線の本数はこの方程式の異なる実数解の個数に等しい。3次方程式が異なる3つの実数解をもつ $\iff$ 極値をもち、極大値と極小値が異符号。",
  "sol": FIG27 + r"$y'=3x^2-1$ より、$C$ 上の点 $(t,\ t^3-t)$ における接線は<br>"
         r"$y=(3t^2-1)(x-t)+t^3-t$，すなわち　$y=(3t^2-1)x-2t^3$<br>"
         r"これが P を通るとき　$b=(3t^2-1)a-2t^3$，すなわち<br>"
         r"$2t^3-3at^2+a+b=0$ …①<br>"
         r"異なる $t_1,\ t_2$ に対する接線が一致したとすると、切片を比べて $t_1^3=t_2^3$，よって $t_1=t_2$ となり矛盾する。よって、異なる接点の接線は異なり、<b>接線の本数は①の異なる実数解の個数</b>に等しい。<br>"
         r"$g(t)=2t^3-3at^2+a+b$ とおくと　$g'(t)=6t^2-6at=6t(t-a)$<br>"
         r"①が異なる3つの実数解をもつ条件は、$g(t)$ が極値をもち、2つの極値が異符号であること、すなわち<br>"
         r"$a\neq0$ かつ $g(0)g(a)<0$<br>"
         r"$g(0)=a+b$，$g(a)=-a^3+a+b$ であるから　$(b+a)(b-a^3+a)<0$<br>"
         r"（$a=0$ のとき左辺は $b^2\geqq0$ となるから、$a\neq0$ はこの不等式に含まれている。）<br>"
         r"よって　$\begin{cases}b>-a\\ b<a^3-a\end{cases}$ または $\begin{cases}b<-a\\ b>a^3-a\end{cases}$<br>"
         r"求める範囲は、<b>曲線 $y=x^3-x$ と直線 $y=-x$ で挟まれた右図の塗った部分</b>で、境界線を含まない。",
  "note": r"直線 $y=-x$ は $C$ の対称の中心である原点における接線である。P が $C$ 上または直線 $y=-x$ 上（原点を除く）にあれば接線は2本、それ以外の点（原点を含む）からは1本となる。一般の3次関数でも「グラフと、対称の中心における接線とで挟まれた部分から3本」が成り立つ。",
  "ex": r"点 $\mathrm{P}(a,\ b)$ から曲線 $y=x^3-3x^2$ に3本の接線が引けるような点 P の存在範囲を求めよ。",
  "exa": r"$(b+3a-1)(b-a^3+3a^2)<0$，すなわち曲線 $y=x^3-3x^2$ と直線 $y=-3x+1$ で挟まれた部分（境界を含まない）"},
 {"lv": 4, "title": "3次曲線と放物線の共通接線の本数",
  "q": r"$c$ を定数とする。曲線 $y=x^3$ と放物線 $y=x^2+c$ の両方に接する直線の本数を、$c$ の値によって分類せよ。",
  "hint": r"3次曲線の接線を接点の $x$ 座標 $t$ で表し、それが放物線に接する条件（判別式 $=0$）から $c$ と $t$ の関係式をつくる。$4c=h(t)$ の形に分離して $t$ の個数を数え、異なる $t$ が同じ直線を与えないことも確かめる。",
  "sol": FIG28 + r"曲線 $y=x^3$ 上の点 $(t,\ t^3)$ における接線は　$y=3t^2x-2t^3$ …①<br>"
         r"①が放物線 $y=x^2+c$ に接するのは、$x^2+c=3t^2x-2t^3$，すなわち $x^2-3t^2x+2t^3+c=0$ が重解をもつときで<br>"
         r"（判別式）$=9t^4-4(2t^3+c)=0$　すなわち　$4c=9t^4-8t^3$ …②<br>"
         r"①の切片 $-2t^3$ が等しければ $t$ も等しいから、異なる $t$ は異なる直線を与える。よって、求める本数は②を満たす実数 $t$ の個数に等しい。<br>"
         r"$h(t)=9t^4-8t^3$ とおくと　$h'(t)=36t^3-24t^2=12t^2(3t-2)$<br>"
         + _tb([r"$t$", r"$\cdots$", r"$0$", r"$\cdots$", r"$\dfrac23$", r"$\cdots$"],
               [r"$h'(t)$", r"$-$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$h(t)$", DN, r"$0$", DN, r"極小 $-\dfrac{16}{27}$", UP])
         + r"$h(t)$ は $t\leqq\dfrac23$ で減少し、$t\geqq\dfrac23$ で増加する。最小値は $h\left(\dfrac23\right)=\dfrac{16}9-\dfrac{64}{27}=-\dfrac{16}{27}$ で、$|t|$ が大きいとき $h(t)$ はいくらでも大きくなる。<br>"
         r"$Y=h(t)$ のグラフと直線 $Y=4c$ の共有点の個数を考えて<br>"
         r"$\boldsymbol{c>-\dfrac4{27}}$ のとき <b>2本</b>，$\boldsymbol{c=-\dfrac4{27}}$ のとき <b>1本</b>，$\boldsymbol{c<-\dfrac4{27}}$ のとき <b>0本</b>",
  "note": r"$t=0$ で $h'(t)=0$ となるが、その前後で $h'(t)$ の符号は変わらないので、$h(0)$ は極値ではない。たとえば $c=0$ のときの2本は、$y=0$（$t=0$）と $t=\dfrac89$ に対する接線である。",
  "ex": r"$c$ を定数とする。曲線 $y=x^3$ と放物線 $y=-x^2+c$ の両方に接する直線の本数を、$c$ の値によって分類せよ。",
  "exa": r"$c<\dfrac4{27}$ のとき2本，$c=\dfrac4{27}$ のとき1本，$c>\dfrac4{27}$ のとき0本"},
 {"lv": 5, "title": "4次関数のグラフに引ける接線の本数（2点で接する直線に注意）",
  "q": r"$b$ を定数とする。点 $\mathrm{A}(0,\ b)$ から曲線 $C:y=x^4-2x^2$ に引ける接線の本数を、$b$ の値によって分類せよ。",
  "hint": r"接点の $x$ 座標 $t$ の方程式の実数解を数えるが、4次関数では<b>異なる2点で接する直線</b>があり得るので、「接点の個数＝接線の本数」とは限らない。まず、$C$ に2点で接する直線を求めておく。",
  "sol": FIG29 + r"$y'=4x^3-4x$ より、$C$ 上の点 $(t,\ t^4-2t^2)$ における接線は<br>"
         r"$y=(4t^3-4t)(x-t)+t^4-2t^2$，すなわち　$y=(4t^3-4t)x-3t^4+2t^2$ …①<br>"
         r"①が A を通る条件は　$b=-3t^4+2t^2$ …②<br>"
         r"<b>[1] 異なる接点が同じ接線を与える場合</b>　直線 $y=mx+n$ が $C$ と異なる2点 $x=\alpha,\ \beta$ で接するとき、第1節の性質から $x^4-2x^2-(mx+n)=(x-\alpha)^2(x-\beta)^2$。$\alpha+\beta=s$，$\alpha\beta=p$ とおき、$(x^2-sx+p)^2=x^4-2sx^3+(s^2+2p)x^2-2spx+p^2$ と係数を比較すると<br>"
         r"$-2s=0$，$s^2+2p=-2$，$-2sp=-m$，$p^2=-n$　より　$s=0,\ p=-1,\ m=0,\ n=-1$<br>"
         r"よって、2点で接する直線は $y=-1$（接点の $x$ 座標は $\pm1$）だけである。したがって、①で異なる $t$ が同じ直線を与えるのは、$t=1$ と $t=-1$ の組だけである。<br>"
         r"<b>[2] ②の実数解の個数</b>　$g(t)=-3t^4+2t^2$ とおくと　$g'(t)=-12t^3+4t=-4t(3t^2-1)$<br>"
         + _tb([r"$t$", r"$\cdots$", r"$-\dfrac1{\sqrt3}$", r"$\cdots$", r"$0$", r"$\cdots$", r"$\dfrac1{\sqrt3}$", r"$\cdots$"],
               [r"$g'(t)$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$", r"$0$", r"$-$"],
               [r"$g(t)$", UP, r"極大 $\dfrac13$", DN, r"極小 $0$", UP, r"極大 $\dfrac13$", DN])
         + r"$g(-t)=g(t)$ であり、$g(\pm1)=-1$。$Y=g(t)$ のグラフ（右図）と直線 $Y=b$ の共有点を考えて、②の異なる実数解の個数は<br>"
         r"$b>\dfrac13$：0個，$b=\dfrac13$：2個，$0<b<\dfrac13$：4個，$b=0$：3個，$b<0$：2個<br>"
         r"<b>[3] 接線の本数</b>　[1]より、解の個数と接線の本数が異なるのは、②の解に $t=1,\ -1$ がともに含まれる場合、すなわち $b=g(1)=-1$ のときだけで、このとき2つの解が同じ接線 $y=-1$ を与える。<br>"
         r"以上から、接線の本数は<br>"
         r"$\boldsymbol{b>\dfrac13}$ のとき <b>0本</b>，$\boldsymbol{b=\dfrac13}$ のとき <b>2本</b>，$\boldsymbol{0<b<\dfrac13}$ のとき <b>4本</b>，$\boldsymbol{b=0}$ のとき <b>3本</b>，<br>"
         r"$\boldsymbol{-1<b<0}$，$\boldsymbol{b<-1}$ のとき <b>2本</b>，$\boldsymbol{b=-1}$ のとき <b>1本</b>",
  "note": r"3次関数のグラフでは異なる接点の接線は一致しない（この節の3本の接線の例題）が、4次関数では一致することがある。点 $(0,\ -1)$ からは、2つの接点 $(\pm1,\ -1)$ をもつ1本の接線 $y=-1$ しか引けない。「接点の個数」と「接線の本数」のずれは、最難関レベルの問題でよく問われる落とし穴である。",
  "ex": r"$b$ を定数とする。点 $(0,\ b)$ から曲線 $y=x^4-8x^2$ に引ける接線の本数を、$b$ の値によって分類せよ。",
  "exa": r"$b>\dfrac{16}3$：0本，$b=\dfrac{16}3$：2本，$0<b<\dfrac{16}3$：4本，$b=0$：3本，$-16<b<0$，$b<-16$：2本，$b=-16$：1本"},
]})


def _nroots(p, var):
    """有理数係数の多項式 p の異なる実数解の個数（厳密）。"""
    q = Poly(expand(p), var)
    if q.degree() <= 0:
        return 0
    return q.sqf_part().count_roots()


def _v2():
    x, t, a, b, c = symbols("x t a b c")

    def tl(f, t0):
        return expand(diff(f, x).subs(x, t0) * (x - t0) + f.subs(x, t0))

    def touches(q, L):  # 2次式 q と直線 L が接する
        P = Poly(expand(q - L), x).all_coeffs()
        return P[1]**2 - 4*P[0]*P[2] == 0
    # 2.1
    assert (x**3 - 2*x**2 + 1).subs(x, 2) == 1 and tl(x**3 - 2*x**2 + 1, 2) == 4*x - 7
    assert expand(-(x - 2) / 4 + 1) == -x/4 + Rational(3, 2)
    assert (-x**3 + 3*x).subs(x, 2) == -2 and tl(-x**3 + 3*x, 2) == -9*x + 16
    # 2.2
    f = x**3 - 3*x
    ts = solve(diff(f, x) - 9, x)
    assert set(ts) == {2, -2} and {tl(f, s) for s in ts} == {9*x - 16, 9*x + 16}
    f2 = x**3 + 3*x**2
    assert {tl(f2, s) for s in solve(diff(f2, x) - 9, x)} == {9*x - 5, 9*x + 27}
    # 2.3
    T = tl(f, t)
    assert expand(T - ((3*t**2 - 3)*x - 2*t**3)) == 0
    ts = solve(T.subs(x, 2) + 6, t)
    assert set(ts) == {0, 3} and {tl(f, s) for s in ts} == {-3*x, 24*x - 54}
    assert expand(-(T.subs(x, 2) - 2) / 2 - (t + 1)*(t - 2)**2) == 0
    assert {tl(f, s) for s in solve(T.subs(x, 2) - 2, t)} == {S(2), 9*x - 16}
    g = x**3 - 2*x
    Tg = tl(g, t)
    assert [tl(g, s) for s in solve(Tg.subs(x, 0) - 2, t) if s.is_real] == [x + 2]
    assert {tl(g, s) for s in solve(Tg.subs(x, 1) + 1, t)} == {x - 2, -Rational(5, 4)*x + Rational(1, 4)}
    # 2.4
    T1 = 2*t*x - t**2
    assert expand(((2*t - 6)**2 - 4*(5 - t**2)) / 4 - 2*(t - 1)*(t - 2)) == 0
    L = {T1.subs(t, s) for s in solve((2*t - 6)**2 - 4*(5 - t**2), t)}
    assert L == {2*x - 1, 4*x - 4}
    assert all(touches(x**2, l) and touches(-x**2 + 6*x - 5, l) for l in L)
    s_ = symbols("s_")
    assert expand(tl(-x**2 + 6*x - 5, s_) - ((-2*s_ + 6)*x + s_**2 - 5)) == 0
    assert set(map(tuple, solve([2*t + 2*s_ - 6, -t**2 - s_**2 + 5], [t, s_]))) == {(1, 2), (2, 1)}
    T1 = tl(x**2 + 1, t)
    L = set()
    for s in solve(Poly(expand(-x**2 - 2*x - T1), x).discriminant(), t):
        L.add(T1.subs(t, s))
    assert L == {S(1), -2*x} and all(touches(x**2 + 1, l) and touches(-x**2 - 2*x, l) for l in L)
    # 2.5
    sol = solve([x**3 - x - (x**2 + a), 3*x**2 - 1 - 2*x], [x, a], dict=True)
    assert {(s[x], s[a], (s[x]**3 - s[x])) for s in sol} == {(1, -1, 0), (Rational(-1, 3), Rational(5, 27), Rational(8, 27))}
    sol = solve([x**3 - (3*x**2 + a), 3*x**2 - 6*x], [x, a], dict=True)
    assert {(s[x], s[a], s[x]**3) for s in sol} == {(0, 0, 0), (2, -4, 8)}
    # 2.6
    sv, pv, mv, nv = symbols("sv pv mv nv")
    for f4, ans_p, ans_L, bound in [(x**4 - 2*x**3 + a*x**2, (a - 1)/2, (a - 1)*x - (a - 1)**2/4, Rational(3, 2)),
                                    (x**4 - 4*x**3 + a*x**2, (a - 4)/2, 2*(a - 4)*x - (a - 4)**2/4, 6)]:
        eqs = Poly(expand(f4 - (mv*x + nv) - (x**2 - sv*x + pv)**2), x).all_coeffs()
        sol = solve(eqs, [sv, pv, mv, nv], dict=True)
        assert len(sol) == 1 and simplify(sol[0][pv] - ans_p) == 0
        assert simplify(sol[0][mv]*x + sol[0][nv] - ans_L) == 0
        assert expand(f4 - ans_L - (x**2 - sol[0][sv]*x + ans_p)**2) == 0
        dsc = sol[0][sv]**2 - 4*ans_p  # >0 ⇔ a<bound
        assert solve(dsc, a) == [bound] and dsc.subs(a, bound - 1) > 0
    a65 = Rational(6, 5)
    fp = diff(x**4 - 2*x**3 + a65*x**2, x)
    assert expand(fp - 2*x*(2*x**2 - 3*x + a65)) == 0 and _nroots(fp, x) == 1
    assert ((a65 - 1), -(a65 - 1)**2/4) == (Rational(1, 5), Rational(-1, 100))
    # 2.7（厳密な実数解の個数で領域を確認）
    assert expand(tl(x**3 - x, t).subs(x, a) - b + (2*t**3 - 3*a*t**2 + a + b)) == 0
    assert expand(tl(x**3 - 3*x**2, t).subs(x, a) - b + (2*t**3 - 3*(a + 1)*t**2 + 6*a*t + b)) == 0
    random.seed(27)
    for _ in range(250):
        A_ = Rational(random.randint(-40, 40), 16)
        B_ = Rational(random.randint(-60, 60), 16)
        n1 = _nroots(2*t**3 - 3*A_*t**2 + A_ + B_, t)
        pr = (B_ + A_) * (B_ - A_**3 + A_)
        assert (n1 == 3) == (pr < 0)
        assert (n1 == 2) == (pr == 0 and A_ != 0)
        n2 = _nroots(2*t**3 - 3*(A_ + 1)*t**2 + 6*A_*t + B_, t)
        assert (n2 == 3) == ((B_ + 3*A_ - 1) * (B_ - A_**3 + 3*A_**2) < 0)
    # 2.8
    assert expand((3*t**2)**2 - 4*(2*t**3 + c) - (9*t**4 - 8*t**3 - 4*c)) == 0
    assert expand(Poly(expand(-x**2 + c - (3*t**2*x - 2*t**3)), x).discriminant() - (9*t**4 + 8*t**3 + 4*c)) == 0
    hmin = (9*t**4 - 8*t**3).subs(t, Rational(2, 3))
    assert hmin == Rational(-16, 27) and solve(9*t**4 - 8*t**3, t) == [0, Rational(8, 9)]
    for cv in [Rational(k, 108) for k in range(-40, 41, 2)] + [Rational(-4, 27), Rational(4, 27)]:
        n = _nroots(9*t**4 - 8*t**3 - 4*cv, t)
        assert n == (2 if cv > Rational(-4, 27) else 1 if cv == Rational(-4, 27) else 0)
        n = _nroots(9*t**4 + 8*t**3 + 4*cv, t)
        assert n == (2 if cv < Rational(4, 27) else 1 if cv == Rational(4, 27) else 0)
    # 2.9（接線を実際に並べて本数を数える）
    for f4, top, dbl in [(x**4 - 2*x**2, Rational(1, 3), -1), (x**4 - 8*x**2, Rational(16, 3), -16)]:
        eqs = Poly(expand(f4 - (mv*x + nv) - (x**2 - sv*x + pv)**2), x).all_coeffs()
        sol = solve(eqs, [sv, pv, mv, nv], dict=True)
        assert len(sol) == 1 and sol[0][mv] == 0 and sol[0][nv] == dbl and sol[0][sv] == 0
        T = tl(f4, t)
        gt = T.subs(x, 0)
        assert max(gt.subs(t, s) for s in solve(diff(gt, t), t)) == top
        for bv in [top + 1, top, top / 2, S(0), S(dbl) / 2, S(dbl), S(dbl) * 2, S(dbl) - Rational(1, 3)]:
            rts = [r for r in Poly(gt - bv, t).real_roots()]
            lines = {(round(float(diff(f4, x).subs(x, r)), 9), round(float(bv), 9)) for r in set(rts)}
            exp_ = (0 if bv > top else 2 if bv == top else 4 if bv > 0 else 3 if bv == 0
                    else 1 if bv == dbl else 2)
            assert len(lines) == exp_, (f4, bv, len(lines))


# ---------------------------------------------------------------- 節3
_f = _F(170, 150, (-0.7, 4.7), (-3.0, 3.2))
_f.axes()
_f.curve(lambda x: x**3 - 6*x**2 + 9*x - 2, -0.7, 4.7)
_f.seg((1, 0), (1, 2))
_f.seg((0, 2), (1, 2))
_f.seg((3, 0), (3, -2))
_f.seg((0, -2), (3, -2))
_f.pt(1, 2)
_f.pt(3, -2)
_f.pt(0, -2)
_f.txt(1, 0, "1", dy=11)
_f.txt(3, 0, "3", dy=-4)
_f.txt(0, 2, "2", dx=-3, dy=4, anc="end")
_f.txt(0, -2, "−2", dx=-3, dy=4, anc="end")
FIG31 = _f.svg()

_f = _F(170, 160, (-1.75, 2.85), (-30, 14))
_f.axes()
_f.curve(lambda x: 3*x**4 - 4*x**3 - 12*x**2 + 5, -1.75, 2.85)
_f.seg((2, 0), (2, -27))
_f.seg((0, -27), (2, -27))
_f.pt(-1, 0)
_f.pt(0, 5)
_f.pt(2, -27)
_f.txt(-1, 0, "−1", dy=11)
_f.txt(2, 0, "2", dy=-4)
_f.txt(0, 5, "5", dx=4, dy=-2, anc="start")
_f.txt(0, -27, "−27", dx=-3, dy=4, anc="end")
FIG32 = _f.svg()

_f = _F(190, 170, (-4.3, 4.3), (-4.2, 5.4))
_f.band(lambda a: 2*abs(a) - 3, lambda a: a*a/3, -3, 3)
_f.axes("a", "b")
_f.curve(lambda a: a*a/3, -4.0, 4.0)
_f.curve(lambda a: 2*a - 3, -0.6, 4.2, col=C2, w=1.1)
_f.curve(lambda a: -2*a - 3, -4.2, 0.6, col=C2, w=1.1)
_f.seg((3, 0), (3, 3))
_f.seg((-3, 0), (-3, 3))
_f.pt(3, 3, fill="#fff")
_f.pt(-3, 3, fill="#fff")
_f.txt(3, 0, "3", dy=11)
_f.txt(-3, 0, "−3", dy=11)
_f.txt(0, -3, "−3", dx=-3, dy=3, anc="end")
_f.txt(3.9, 5.0, "b=a²/3", dx=-4, anc="end", it=True, col=C1)
FIG37 = _f.svg()

SEC.append({"title": "関数の増減と極値",
"base": r"""・$f'(x)>0$ となる区間で $f(x)$ は増加し、$f'(x)<0$ となる区間で減少する<br>
・$f'(x)$ の符号が $x=a$ の前後で正から負に変われば $f(a)$ は極大値、負から正に変われば極小値<br>
・$f'(a)=0$ は $f(a)$ が極値であるための必要条件であるが、十分条件ではない（例：$f(x)=x^3$ の $x=0$）<br>
・3次関数 $f(x)$ が極値をもつ $\iff$ 2次方程式 $f'(x)=0$ が異なる2つの実数解をもつ（判別式 $D>0$）""",
"items": [
 {"lv": 1, "title": "3次関数の増減とグラフ",
  "q": r"関数 $y=x^3-6x^2+9x-2$ の増減を調べ、極値を求めよ。また、そのグラフをかけ。",
  "hint": r"$y'=0$ となる $x$ を求め、その前後での $y'$ の符号を増減表にまとめる。グラフは極値をとる点と $y$ 軸との交点を目安にしてかく。",
  "sol": FIG31 + r"$y'=3x^2-12x+9=3(x-1)(x-3)$<br>$y'=0$ とすると $x=1,\ 3$。増減表は次のようになる。<br>"
         + _tb([r"$x$", r"$\cdots$", r"$1$", r"$\cdots$", r"$3$", r"$\cdots$"],
               [r"$y'$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$y$", UP, r"極大 $2$", DN, r"極小 $-2$", UP])
         + r"よって、$x=1$ で<b>極大値 $\boldsymbol{2}$</b>，$x=3$ で<b>極小値 $\boldsymbol{-2}$</b> をとる。<br>グラフは右の図のようになる（$y$ 軸との交点は $(0,\ -2)$）。",
  "note": r"$f'(x)=0$ を満たす $x$ でも、前後で符号が変わらなければ極値ではない。たとえば $y=x^3+3x^2+3x$ は $y'=3(x+1)^2\geqq0$ で、つねに増加し、極値をもたない。また、この例題のグラフは点 $(2,\ 0)$ に関して対称になっている（第6節）。",
  "ex": r"関数 $y=-x^3+3x^2+1$ の増減を調べ、極値を求めよ。また、そのグラフをかけ。",
  "exa": r"$x=2$ で極大値 $5$，$x=0$ で極小値 $1$（グラフは略）"},
 {"lv": 2, "title": "4次関数の増減とグラフ",
  "q": r"関数 $y=3x^4-4x^3-12x^2+5$ の極値を求め、グラフの概形をかけ。",
  "hint": r"$y'$ は3次式になる。因数分解して $y'=0$ の3つの解を求め、増減表をつくる。",
  "sol": FIG32 + r"$y'=12x^3-12x^2-24x=12x(x+1)(x-2)$<br>$y'=0$ とすると $x=-1,\ 0,\ 2$<br>"
         + _tb([r"$x$", r"$\cdots$", r"$-1$", r"$\cdots$", r"$0$", r"$\cdots$", r"$2$", r"$\cdots$"],
               [r"$y'$", r"$-$", r"$0$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$y$", DN, r"極小 $0$", UP, r"極大 $5$", DN, r"極小 $-27$", UP])
         + r"よって、$x=-1$ で<b>極小値 $\boldsymbol{0}$</b>，$x=0$ で<b>極大値 $\boldsymbol{5}$</b>，$x=2$ で<b>極小値 $\boldsymbol{-27}$</b> をとる。<br>グラフは右の図のようになる。",
  "note": r"極小値が $0$ なので、グラフは $x=-1$ で $x$ 軸に接する。実際、$3x^4-4x^3-12x^2+5=(x+1)^2(3x^2-10x+5)$ と因数分解できる。$x^4$ の係数が正の4次関数は、$y'=0$ が異なる3つの実数解をもつとき W 字形になり、そうでないときは極小値を1つだけもつ形になる。",
  "ex": r"関数 $y=-x^4+4x^3-4x^2+1$ の極値を求め、グラフの概形をかけ。",
  "exa": r"$x=0,\ 2$ で極大値 $1$，$x=1$ で極小値 $0$（グラフは M 字形，略）"},
 {"lv": 2, "title": "極値の条件から係数を決定する（十分性の確認）",
  "q": r"関数 $f(x)=x^3+ax^2+bx+c$ が $x=-1$ で極大値 $5$ をとり、$x=3$ で極小値をとるとき、定数 $a,\ b,\ c$ の値と極小値を求めよ。",
  "hint": r"$x=-1,\ 3$ で極値をとる $\Longrightarrow$ $f'(-1)=f'(3)=0$。これは必要条件なので、求めた値で実際に極大・極小となることを増減表で確かめる（十分性）。",
  "sol": r"$f'(x)=3x^2+2ax+b$。$x=-1,\ 3$ で極値をとるから　$f'(-1)=0$，$f'(3)=0$<br>"
         r"すなわち　$3-2a+b=0$，$27+6a+b=0$　これを解いて　$a=-3,\ b=-9$<br>"
         r"さらに $f(-1)=5$ より $-1+a-b+c=5$，よって $c=0$。<br>"
         r"逆に、このとき $f(x)=x^3-3x^2-9x$，$f'(x)=3x^2-6x-9=3(x+1)(x-3)$ で、増減表は<br>"
         + _tb([r"$x$", r"$\cdots$", r"$-1$", r"$\cdots$", r"$3$", r"$\cdots$"],
               [r"$f'(x)$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$f(x)$", UP, r"極大 $5$", DN, r"極小 $-27$", UP])
         + r"となり、確かに $x=-1$ で極大値 $5$，$x=3$ で極小値をとる。<br>"
         r"よって　$\boldsymbol{a=-3,\ b=-9,\ c=0}$，極小値は $f(3)=27-27-27=\boldsymbol{-27}$",
  "note": r"$f'(\alpha)=0$ は「$x=\alpha$ で極値をとる」ための必要条件にすぎない。たとえば「$x=1$ で極値をとる」という条件だけから係数を決めると、$f'(x)=3(x-1)^2$ となって極値をとらない場合が混ざることがある。必ず増減表で十分性を確かめよう。",
  "ex": r"関数 $f(x)=ax^3+bx^2+cx+d$ が $x=0$ で極大値 $4$ をとり、$x=2$ で極小値 $0$ をとるとき、定数 $a,\ b,\ c,\ d$ の値を求めよ。",
  "exa": r"$a=1,\ b=-3,\ c=0,\ d=4$"},
 {"lv": 2, "title": "極値をもつ条件・つねに増加する条件",
  "q": r"$a$ を定数とし、$f(x)=x^3+ax^2+(a+6)x+1$ とする。<br>(1) $f(x)$ が極値をもつような $a$ の値の範囲を求めよ。<br>(2) $f(x)$ がつねに増加するような $a$ の値の範囲を求めよ。",
  "hint": r"$f'(x)$ は2次式。極値をもつ $\iff$ $f'(x)$ の符号が変わる $\iff$ $f'(x)=0$ が異なる2つの実数解をもつ。つねに増加 $\iff$ すべての $x$ で $f'(x)\geqq0$。",
  "sol": r"$f'(x)=3x^2+2ax+a+6$。$f'(x)=0$ の判別式を $D$ とすると<br>"
         r"$\dfrac D4=a^2-3(a+6)=a^2-3a-18=(a+3)(a-6)$<br>"
         r"(1) $f(x)$ が極値をもつのは、$f'(x)$ の符号が変化するとき、すなわち $D>0$ のときである。<br>"
         r"$(a+3)(a-6)>0$ より　$\boldsymbol{a<-3,\ 6<a}$<br>"
         r"(2) $f(x)$ がつねに増加するのは、すべての $x$ で $f'(x)\geqq0$ となるとき、すなわち $D\leqq0$ のときである。<br>"
         r"$(a+3)(a-6)\leqq0$ より　$\boldsymbol{-3\leqq a\leqq6}$",
  "note": r"$D=0$ のとき $f'(x)=3(x-p)^2$ の形で、$f'(x)=0$ となるのは $x=p$ だけである。このように1点を除いて $f'(x)>0$ なら $f(x)$ は増加する（極値はもたない）ので、(2) では等号を含める。",
  "ex": r"$a$ を定数とし、$f(x)=-x^3+ax^2-3ax+2$ とする。(1) $f(x)$ が極値をもつような $a$ の値の範囲、(2) $f(x)$ がつねに減少するような $a$ の値の範囲を求めよ。",
  "exa": r"(1) $a<0,\ 9<a$　(2) $0\leqq a\leqq9$"},
 {"lv": 3, "title": "4次関数が極大値をもつ条件",
  "q": r"関数 $f(x)=x^4+4ax^3+6x^2$ が極大値をもつような定数 $a$ の値の範囲を求めよ。",
  "hint": r"$f'(x)$ は $x^3$ の係数が正の3次式。極大値をもつには $f'(x)$ の符号が「正から負」に変わる所が必要で、それは $f'(x)=0$ が異なる3つの実数解をもつときに限られる。",
  "sol": r"$f'(x)=4x^3+12ax^2+12x=4x(x^2+3ax+3)$。$g(x)=x^2+3ax+3$ とおく。<br>"
         r"[1] $g(x)=0$ が異なる2つの実数解をもつとき、$g(0)=3\neq0$ よりそれらは $0$ と異なるから、$f'(x)=0$ は異なる3つの実数解をもつ。それらを $p<q<r$ とすると $f'(x)=4(x-p)(x-q)(x-r)$ で、$f'(x)$ の符号は $x=q$ の前後で正から負に変わる。よって、$f(x)$ は $x=q$ で極大値をとる。<br>"
         r"[2] $g(x)=0$ の判別式が $0$ 以下のとき、すべての $x$ で $g(x)\geqq0$ であり、$g(x)=0$ となる $x$ は高々1つ。よって、$f'(x)$ は $x<0$ で $0$ 以下、$x>0$ で $0$ 以上（$0$ となるのは高々1点）となり、$f(x)$ は $x\leqq0$ で減少、$x\geqq0$ で増加する。極大値はもたない。<br>"
         r"よって、求める条件は、$g(x)=0$ の判別式について　$9a^2-12>0$，すなわち $a^2>\dfrac43$<br>"
         r"したがって　$\boldsymbol{a<-\dfrac{2\sqrt3}3,\ \dfrac{2\sqrt3}3<a}$",
  "note": r"$x^4$ の係数が正の4次関数は、最小値をとる点で必ず極小値をもつので、「極値をもつ」条件は問題にならない。「極大値をもつ」は「極値を3つもつ」と同じ意味である。$f'(x)=x\cdot g(x)$ の形のときは、$g(0)\neq0$ の確認を忘れないこと（練習を参照）。",
  "ex": r"関数 $f(x)=x^4-4x^3+2ax^2$ が極大値をもつような定数 $a$ の値の範囲を求めよ。",
  "exa": r"$a<0,\ 0<a<\dfrac94$"},
 {"lv": 3, "title": "極大値と極小値の差（解と係数の関係）",
  "q": r"関数 $f(x)=x^3-6x^2+3ax$ の極大値と極小値の差が $4$ となるような定数 $a$ の値を求めよ。",
  "hint": r"$f'(x)=0$ の2解 $\alpha,\ \beta$ を具体的に求めず、解と係数の関係で $f(\alpha)-f(\beta)$ を計算する。$(\alpha-\beta)$ をくくり出し、残りを $\alpha+\beta,\ \alpha\beta$ で表す。",
  "sol": r"$f'(x)=3x^2-12x+3a=3(x^2-4x+a)$<br>"
         r"$f(x)$ が極値をもつ条件は、$x^2-4x+a=0$ が異なる2つの実数解をもつことで　$\dfrac D4=4-a>0$，$a<4$ …①<br>"
         r"このとき、2解を $\alpha,\ \beta\ (\alpha<\beta)$ とすると、$x^3$ の係数が正であるから $f(\alpha)$ が極大値、$f(\beta)$ が極小値で、$\alpha+\beta=4$，$\alpha\beta=a$。<br>"
         r"$f(\alpha)-f(\beta)=(\alpha^3-\beta^3)-6(\alpha^2-\beta^2)+3a(\alpha-\beta)$<br>"
         r"$=(\alpha-\beta)\{(\alpha+\beta)^2-\alpha\beta-6(\alpha+\beta)+3a\}$<br>"
         r"$=(\alpha-\beta)(16-a-24+3a)=2(\beta-\alpha)(4-a)$<br>"
         r"$(\beta-\alpha)^2=(\alpha+\beta)^2-4\alpha\beta=16-4a$ で、$\beta-\alpha>0$ より $\beta-\alpha=2\sqrt{4-a}$。<br>"
         r"よって　$f(\alpha)-f(\beta)=4(4-a)\sqrt{4-a}=4\left(\sqrt{4-a}\right)^3$<br>"
         r"これが $4$ に等しいから $\left(\sqrt{4-a}\right)^3=1$，$\sqrt{4-a}=1$，$a=3$（①を満たす）。<br>"
         r"よって　$\boldsymbol{a=3}$",
  "note": r"$a=3$ のとき $f(x)=x^3-6x^2+9x$ で、極大値 $f(1)=4$，極小値 $f(3)=0$ となり、確かに差は $4$ である。一般に、$x^3$ の係数が $p\ (p\neq0)$ の3次関数が $x=\alpha,\ \beta$ で極値をとるとき　$|f(\alpha)-f(\beta)|=\dfrac{|p|}2|\beta-\alpha|^3$　が成り立つ（積分を使うと簡単に示せる：第15章）。",
  "ex": r"関数 $f(x)=x^3-3x^2+ax$ の極大値と極小値の差が $32$ となるような定数 $a$ の値を求めよ。",
  "exa": r"$a=-9$"},
 {"lv": 4, "title": r"極値をとる $x$ が区間内にある条件（解の配置）",
  "q": r"関数 $f(x)=x^3+ax^2+bx$ が極大値と極小値をもち、それらをとる $x$ の値がともに $-1<x<1$ の範囲にあるような点 $(a,\ b)$ の存在範囲を図示せよ。",
  "hint": r"2次方程式 $f'(x)=0$ が $-1<x<1$ の範囲に異なる2つの実数解をもつ条件（2次方程式の解の配置）を考える。判別式・軸の位置・区間の端での符号の3つを調べる。",
  "sol": FIG37 + r"$f'(x)=3x^2+2ax+b$。条件は、2次方程式 $f'(x)=0$ が $-1<x<1$ の範囲に異なる2つの実数解をもつことである。$Y=f'(x)$ のグラフは下に凸の放物線で、軸は直線 $x=-\dfrac a3$ であるから、条件は<br>"
         r"(i) $\dfrac D4=a^2-3b>0$　(ii) $-1<-\dfrac a3<1$<br>"
         r"(iii) $f'(-1)=3-2a+b>0$　(iv) $f'(1)=3+2a+b>0$<br>"
         r"すなわち　$b<\dfrac{a^2}3$，$-3<a<3$，$b>2a-3$，$b>-2a-3$<br>"
         r"ここで、放物線 $b=\dfrac{a^2}3$ と直線 $b=2a-3$ は、$\dfrac{a^2}3-(2a-3)=\dfrac{(a-3)^2}3$ より点 $(3,\ 3)$ で接し、同様に直線 $b=-2a-3$ とは点 $(-3,\ 3)$ で接する。<br>"
         r"求める範囲は<b>右の図の塗った部分</b>で、境界線を含まない。",
  "note": r"(ii) の軸の条件を落とすと、$a>3$ の側で放物線と直線 $b=2a-3$ に挟まれた部分なども含まれてしまう。たとえば $(a,\ b)=\left(4,\ \dfrac{26}5\right)$ は (i)，(iii)，(iv) を満たすが、$f'(x)=0$ の2解はともに $-1$ より小さい。",
  "ex": r"関数 $f(x)=x^3+ax^2+bx$ が極大値と極小値をもち、それらをとる $x$ の値がともに $0<x<2$ の範囲にあるような点 $(a,\ b)$ の存在範囲を求めよ。",
  "exa": r"$-6<a<0$，$b>0$，$b>-4a-12$，$b<\dfrac{a^2}3$（放物線 $b=\dfrac{a^2}3$ と2直線 $b=0$，$b=-4a-12$ で囲まれた部分，境界を含まない）"},
]})


def _signs(fp, var):
    """fp の実数解で区切った各区間での符号の列。"""
    rts = sorted(set(Poly(fp, var).real_roots()), key=float)
    xs = [float(r) for r in rts]
    probes = ([xs[0] - 1] if xs else [0.0]) + [(xs[i] + xs[i + 1]) / 2 for i in range(len(xs) - 1)] + ([xs[-1] + 1] if xs else [])
    return [1 if float(fp.subs(var, p)) > 0 else -1 for p in probes], rts


def _v3():
    x, a = symbols("x a")
    # 3.1
    f = x**3 - 6*x**2 + 9*x - 2
    assert expand(diff(f, x) - 3*(x - 1)*(x - 3)) == 0 and f.subs(x, 1) == 2 and f.subs(x, 3) == -2
    assert _signs(diff(f, x), x)[0] == [1, -1, 1]
    assert expand(diff(x**3 + 3*x**2 + 3*x, x) - 3*(x + 1)**2) == 0
    g = -x**3 + 3*x**2 + 1
    assert _signs(diff(g, x), x) == ([-1, 1, -1], [0, 2]) and g.subs(x, 2) == 5 and g.subs(x, 0) == 1
    # 3.2
    f = 3*x**4 - 4*x**3 - 12*x**2 + 5
    assert expand(diff(f, x) - 12*x*(x + 1)*(x - 2)) == 0
    assert _signs(diff(f, x), x) == ([-1, 1, -1, 1], [-1, 0, 2])
    assert [f.subs(x, v) for v in (-1, 0, 2)] == [0, 5, -27]
    assert expand((x + 1)**2*(3*x**2 - 10*x + 5) - f) == 0
    g = -x**4 + 4*x**3 - 4*x**2 + 1
    assert _signs(diff(g, x), x) == ([1, -1, 1, -1], [0, 1, 2]) and [g.subs(x, v) for v in (0, 1, 2)] == [1, 0, 1]
    # 3.3
    A, B, C, D = symbols("A B C D")
    F = x**3 + A*x**2 + B*x + C
    sol = solve([diff(F, x).subs(x, -1), diff(F, x).subs(x, 3), F.subs(x, -1) - 5], [A, B, C], dict=True)
    assert sol == [{A: -3, B: -9, C: 0}]
    F0 = F.subs(sol[0])
    assert _signs(diff(F0, x), x) == ([1, -1, 1], [-1, 3]) and F0.subs(x, 3) == -27
    F = A*x**3 + B*x**2 + C*x + D
    sol = solve([diff(F, x).subs(x, 0), diff(F, x).subs(x, 2), F.subs(x, 0) - 4, F.subs(x, 2)], [A, B, C, D], dict=True)
    assert sol == [{A: 1, B: -3, C: 0, D: 4}]
    assert _signs(diff(F.subs(sol[0]), x), x) == ([1, -1, 1], [0, 2])
    # 3.4
    assert expand((2*a)**2/4 - 3*(a + 6) - (a + 3)*(a - 6)) == 0
    assert expand((2*a)**2/4 - (-3)*(-3*a) - a*(a - 9)) == 0
    for av in range(-6, 12):
        fp = 3*x**2 + 2*av*x + av + 6
        n = _nroots(fp, x)
        assert (n == 2) == (av < -3 or av > 6)
        gp = -3*x**2 + 2*av*x - 3*av
        assert (_nroots(gp, x) == 2) == (av < 0 or av > 9)
    # 3.5（f' の符号が + から - に変わる点があるか）
    def has_max(fp):
        sg, _ = _signs(fp, x)
        return any(sg[i] == 1 and sg[i + 1] == -1 for i in range(len(sg) - 1))
    for k in range(-40, 41):
        av = Rational(k, 16)
        assert has_max(diff(x**4 + 4*av*x**3 + 6*x**2, x)) == (av**2 > Rational(4, 3))
        assert has_max(diff(x**4 - 4*x**3 + 2*av*x**2, x)) == (av < Rational(9, 4) and av != 0)
    assert expand(diff(x**4 + 4*x**3*2/sqrt(3) + 6*x**2, x) - 4*x*(x + sqrt(3))**2) == 0  # 境界では極大なし
    # 3.6
    random.seed(36)
    for _ in range(8):
        av = Rational(random.randint(-30, 39), 10)
        al, be = sorted(solve(x**2 - 4*x + av, x), key=float)
        f = x**3 - 6*x**2 + 3*av*x
        assert abs(float(f.subs(x, al) - f.subs(x, be)) - 4 * float(4 - av)**1.5) < 1e-9
        assert abs(float(f.subs(x, al) - f.subs(x, be)) - 0.5 * float(be - al)**3) < 1e-9
    f = x**3 - 6*x**2 + 9*x
    assert f.subs(x, 1) - f.subs(x, 3) == 4
    f = x**3 - 3*x**2 - 9*x
    assert f.subs(x, -1) - f.subs(x, 3) == 32 and expand(diff(f, x) - 3*(x + 1)*(x - 3)) == 0
    for av in [Rational(k, 2) for k in range(-40, 6)]:
        rr = solve(3*x**2 - 6*x + av, x)
        if len(rr) == 2 and all(r.is_real for r in rr):
            f = x**3 - 3*x**2 + av*x
            dif = abs(simplify(f.subs(x, rr[0]) - f.subs(x, rr[1])))
            assert (simplify(dif - 32) == 0) == (av == -9)
    # 3.7（2解がともに開区間にあるかを厳密に数える）
    def inside2(p, lo, hi):
        q = Poly(p, x)
        if q.discriminant() <= 0:
            return False
        sq = q.sqf_part()
        n = sq.count_roots(lo, hi) - (1 if q.eval(lo) == 0 else 0) - (1 if q.eval(hi) == 0 else 0)
        return n == 2
    random.seed(37)
    for _ in range(400):
        av, bv = Rational(random.randint(-90, 90), 20), Rational(random.randint(-100, 120), 20)
        fp = 3*x**2 + 2*av*x + bv
        cond = (-3 < av < 3) and (bv < av**2 / 3) and (bv > 2*av - 3) and (bv > -2*av - 3)
        assert inside2(fp, -1, 1) == cond
        cond2 = (-6 < av < 0) and (bv > 0) and (bv > -4*av - 12) and (bv < av**2 / 3)
        assert inside2(fp, 0, 2) == cond2
    av, bv = Rational(4), Rational(26, 5)
    rr = [float(r) for r in Poly(3*x**2 + 8*x + bv, x).real_roots()]
    assert av**2 - 3*bv > 0 and 3 - 2*av + bv > 0 and 3 + 2*av + bv > 0 and max(rr) < -1
    assert expand(a**2/3 - (2*a - 3) - (a - 3)**2/3) == 0


# ---------------------------------------------------------------- 節4
_f = _F(170, 150, (-0.5, 4.8), (-1.0, 6.6))
_f.axes()
_f.curve(lambda x: x**3 - 6*x**2 + 9*x, -0.5, 4.8)
_f.seg((0, 4), (4.6, 4))
_f.seg((1, 0), (1, 4))
_f.seg((4, 0), (4, 4))
_f.pt(1, 4)
_f.pt(4, 4)
_f.pt(3, 0)
_f.txt(1, 0, "1", dy=11)
_f.txt(3, 0, "3", dy=11)
_f.txt(4, 0, "4", dy=11)
_f.txt(0, 4, "4", dx=-3, dy=4, anc="end")
FIG44 = _f.svg()

_f = _F(180, 150, (-1.5, 2.65), (-4.6, 1.0))
_f.axes("a", "b")
_f.curve(lambda a: -a**4 + 2*a**3, -1.5, -1.0, w=1.8)
_f.curve(lambda a: 2*a - 1, -1.0, 0.5, w=1.8)
_f.curve(lambda a: 0.0, 0.5, 2.0, w=2.4)
_f.curve(lambda a: -a**4 + 2*a**3, 2.0, 2.65, w=1.8)
_f.seg((-1, 0), (-1, -3))
_f.seg((-1, -3), (0, -3))
_f.pt(-1, -3)
_f.pt(0.5, 0)
_f.pt(2, 0)
_f.txt(-1, 0, "−1", dy=-4)
_f.txt(0.5, 0, "1/2", dy=-4)
_f.txt(2, 0, "2", dy=-4)
_f.txt(0, -3, "−3", dx=3, dy=4, anc="start")
_f.txt(0, -1, "−1", dx=3, dy=6, anc="start")
FIG47 = _f.svg()

SEC.append({"title": "最大・最小",
"base": r"""・区間 $a\leqq x\leqq b$ における最大・最小：区間内の極値と区間の両端の値を比べる<br>
・文字を含むときは、「極値をとる $x$ が区間内にあるか」「極値と端の値のどちらが大きいか」で場合分けする<br>
・$f'(\alpha)=0$ のとき、$f(x)=f(\alpha)$ の他の解は、$f(x)-f(\alpha)$ が $(x-\alpha)^2$ で割り切れることを使って求める<br>
・置き換えをしたら、新しい変数の変域を必ず確認する""",
"items": [
 {"lv": 1, "title": "区間における最大・最小",
  "q": r"関数 $f(x)=x^3-3x^2\ (-1\leqq x\leqq4)$ の最大値と最小値を求めよ。",
  "hint": r"区間内の極値と、区間の両端の値を比べる。",
  "sol": r"$f'(x)=3x^2-6x=3x(x-2)$ より、増減表は次のようになる。<br>"
         + _tb([r"$x$", r"$-1$", r"$\cdots$", r"$0$", r"$\cdots$", r"$2$", r"$\cdots$", r"$4$"],
               [r"$f'(x)$", "", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$", ""],
               [r"$f(x)$", r"$-4$", UP, r"極大 $0$", DN, r"極小 $-4$", UP, r"$16$"])
         + r"よって　<b>最大値 $\boldsymbol{16}$（$x=4$），最小値 $\boldsymbol{-4}$（$x=-1,\ 2$）</b>",
  "note": r"最大・最小を答えるときは、そのときの $x$ の値も書く。この例題では $f(-1)=f(2)=-4$ で、最小値をとる $x$ が2つある。",
  "ex": r"関数 $f(x)=2x^3-3x^2-12x\ (-2\leqq x\leqq3)$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $7$（$x=-1$），最小値 $-20$（$x=2$）"},
 {"lv": 2, "title": "最大・最小の応用（容積の最大）",
  "q": r"1辺の長さが $12\ \mathrm{cm}$ の正方形の厚紙の四隅から、1辺の長さが $x\ \mathrm{cm}$ の正方形を切り取り、残りを折り曲げてふたのない直方体の箱をつくる。箱の容積 $V$ の最大値と、そのときの $x$ の値を求めよ。",
  "hint": r"$V$ を $x$ の式で表し、$x$ の変域（辺の長さが正）を確認してから増減を調べる。",
  "sol": r"箱の底面は1辺 $12-2x$ の正方形、高さは $x$ であるから、$x>0$，$12-2x>0$ より $0<x<6$ で<br>"
         r"$V=x(12-2x)^2=4x^3-48x^2+144x$<br>"
         r"$V'=12x^2-96x+144=12(x-2)(x-6)$<br>"
         + _tb([r"$x$", r"$0$", r"$\cdots$", r"$2$", r"$\cdots$", r"$6$"],
               [r"$V'$", "", r"$+$", r"$0$", r"$-$", ""],
               [r"$V$", "", UP, r"極大 $128$", DN, ""])
         + r"よって、$V$ は $\boldsymbol{x=2}$ のとき<b>最大値 $\boldsymbol{128\ \mathrm{cm}^3}$</b> をとる。",
  "note": r"変域が $0<x<6$ のように端を含まない区間でも、その内部でただ1つの極値（極大値）をとれば、それが最大値である。",
  "ex": r"縦 $8\ \mathrm{cm}$，横 $5\ \mathrm{cm}$ の長方形の厚紙の四隅から1辺 $x\ \mathrm{cm}$ の正方形を切り取り、ふたのない箱をつくる。容積の最大値とそのときの $x$ の値を求めよ。",
  "exa": r"$x=1$ のとき最大値 $18\ \mathrm{cm}^3$"},
 {"lv": 2, "title": "置き換えによる最大・最小（三角関数）",
  "q": r"$0\leqq\theta<2\pi$ のとき、関数 $y=2\cos^3\theta+3\cos2\theta$ の最大値と最小値を求めよ。また、そのときの $\theta$ の値を求めよ。",
  "hint": r"$\cos2\theta=2\cos^2\theta-1$ で $\cos\theta$ だけの式にし、$t=\cos\theta$ とおく。<b>$t$ の変域 $-1\leqq t\leqq1$</b> で3次関数の最大・最小を調べる。",
  "sol": r"$t=\cos\theta$ とおくと、$0\leqq\theta<2\pi$ より $-1\leqq t\leqq1$。<br>"
         r"$y=2t^3+3(2t^2-1)=2t^3+6t^2-3$，$y'=6t^2+12t=6t(t+2)$<br>"
         + _tb([r"$t$", r"$-1$", r"$\cdots$", r"$0$", r"$\cdots$", r"$1$"],
               [r"$y'$", "", r"$-$", r"$0$", r"$+$", ""],
               [r"$y$", r"$1$", DN, r"極小 $-3$", UP, r"$5$"])
         + r"よって、$y$ は $t=1$ で最大値 $5$，$t=0$ で最小値 $-3$ をとる。<br>"
         r"$t=1$ となるのは $\theta=0$，$t=0$ となるのは $\theta=\dfrac\pi2,\ \dfrac32\pi$ のときであるから<br>"
         r"<b>最大値 $\boldsymbol{5}$（$\boldsymbol{\theta=0}$），最小値 $\boldsymbol{-3}$（$\boldsymbol{\theta=\dfrac\pi2,\ \dfrac32\pi}$）</b>",
  "note": r"指数関数 $t=2^x\ (t>0)$ や $t=\sin\theta+\cos\theta\ (-\sqrt2\leqq t\leqq\sqrt2)$ などの置き換えでも、同じように3次関数の最大・最小に帰着できる。どの場合も、新しい変数の変域を最初に確認しよう。",
  "ex": r"$0\leqq\theta<2\pi$ のとき、関数 $y=2\sin^3\theta+3\cos2\theta$ の最大値と最小値、およびそのときの $\theta$ の値を求めよ。",
  "exa": r"最大値 $3$（$\theta=0,\ \pi$），最小値 $-5$（$\theta=\dfrac32\pi$）"},
 {"lv": 3, "title": "区間の端が動くときの最大値",
  "q": r"$a>0$ とする。関数 $f(x)=x^3-6x^2+9x$ の $0\leqq x\leqq a$ における最大値 $M(a)$ を求めよ。",
  "hint": r"極大値 $f(1)=4$ と区間の右端の値 $f(a)$ の大小で場合分けする。$f(x)=4$ となる $x$ を、$f(x)-4$ が $(x-1)^2$ で割り切れることを使って求めておく。",
  "sol": FIG44 + r"$f'(x)=3x^2-12x+9=3(x-1)(x-3)$ より、$f(x)$ は $x\leqq1$ で増加、$1\leqq x\leqq3$ で減少、$x\geqq3$ で増加し、極大値 $f(1)=4$，極小値 $f(3)=0$。<br>"
         r"また、$f(x)=4$ とすると $x^3-6x^2+9x-4=0$，$(x-1)^2(x-4)=0$ より $x=1,\ 4$。<br>"
         r"(i) $0<a<1$ のとき、$f(x)$ は $0\leqq x\leqq a$ で増加するから　$M(a)=f(a)$<br>"
         r"(ii) $1\leqq a\leqq4$ のとき、$x\leqq4$ では $f(x)-4=(x-1)^2(x-4)\leqq0$ であるから　$M(a)=f(1)=4$<br>"
         r"(iii) $a>4$ のとき、$x\leqq4$ では $f(x)\leqq4$ で、$4\leqq x\leqq a$ では $f(x)$ は増加し $f(a)>f(4)=4$ であるから　$M(a)=f(a)$<br>"
         r"以上から<br>"
         r"$\boldsymbol{0<a<1,\ 4<a}$ のとき $\boldsymbol{M(a)=a^3-6a^2+9a}$，$\boldsymbol{1\leqq a\leqq4}$ のとき $\boldsymbol{M(a)=4}$",
  "note": r"$f'(1)=0$ より $f(x)-f(1)$ は $(x-1)^2$ で割り切れる（第1節）。このように「極値と同じ値をとるもう1つの点」を因数分解で求めるのが、区間が動く問題の定石である。なお、この関数では $x\geqq0$ で $f(x)=x(x-3)^2\geqq0$ なので、最小値はつねに $f(0)=0$ である。",
  "ex": r"$a>0$ とする。関数 $f(x)=2x^3-9x^2+12x$ の $0\leqq x\leqq a$ における最大値 $M(a)$ を求めよ。",
  "exa": r"$0<a<1,\ \dfrac52<a$ のとき $M(a)=2a^3-9a^2+12a$，$1\leqq a\leqq\dfrac52$ のとき $M(a)=5$"},
 {"lv": 3, "title": "係数に文字を含む関数の最大・最小",
  "q": r"$a>0$ とする。関数 $f(x)=x^3-3a^2x$ の $0\leqq x\leqq1$ における最大値と最小値を求めよ。",
  "hint": r"最小値は、極小となる $x=a$ が区間の内部にあるかどうかで場合分けする。最大値は両端の値 $f(0)$，$f(1)$ の大小で決まる。",
  "sol": r"$f'(x)=3x^2-3a^2=3(x+a)(x-a)$ であるから、$x\geqq0$ において、$f(x)$ は $0\leqq x\leqq a$ で減少、$x\geqq a$ で増加する。<br>"
         r"$f(0)=0$，$f(a)=-2a^3$，$f(1)=1-3a^2$<br>"
         r"<b>最小値</b>　(i) $0<a<1$ のとき、極小値をとる $x=a$ が区間内にあるから、最小値は $f(a)=-2a^3$<br>"
         r"(ii) $a\geqq1$ のとき、$f(x)$ は $0\leqq x\leqq1$ で減少するから、最小値は $f(1)=1-3a^2$<br>"
         r"<b>最大値</b>　$0\leqq x\leqq1$ で $f(x)$ は減少してから増加する（または減少するだけ）ので、最大値は $f(0)$ と $f(1)$ の大きい方である。$f(1)-f(0)=1-3a^2$ であるから、$0<a<\dfrac{\sqrt3}3$ のとき $f(1)>f(0)$，$a\geqq\dfrac{\sqrt3}3$ のとき $f(1)\leqq f(0)$。<br>"
         r"以上から<br>"
         r"最大値は　$\boldsymbol{0<a<\dfrac{\sqrt3}3}$ のとき $\boldsymbol{1-3a^2}$（$x=1$），$\boldsymbol{a\geqq\dfrac{\sqrt3}3}$ のとき $\boldsymbol{0}$（$x=0$。$a=\dfrac{\sqrt3}3$ のときは $x=0,\ 1$）<br>"
         r"最小値は　$\boldsymbol{0<a<1}$ のとき $\boldsymbol{-2a^3}$（$x=a$），$\boldsymbol{a\geqq1}$ のとき $\boldsymbol{1-3a^2}$（$x=1$）",
  "note": r"最大値と最小値では場合分けの境目が異なる（$\dfrac{\sqrt3}3$ と $1$）。「どの値とどの値を比べるのか」を増減表から読みとってから場合分けしよう。",
  "ex": r"$a$ を実数の定数とする。関数 $f(x)=x^3-3ax$ の $0\leqq x\leqq2$ における最小値を求めよ。",
  "exa": r"$a\leqq0$ のとき $0$，$0<a<4$ のとき $-2a\sqrt a$，$a\geqq4$ のとき $8-6a$"},
 {"lv": 4, "title": "絶対値を含む関数の最大値とその最小値",
  "q": r"$a$ を実数とし、$0\leqq x\leqq1$ における $|x^3-3ax|$ の最大値を $M(a)$ とする。$M(a)$ を求めよ。また、$M(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "hint": r"$g(x)=x^3-3ax$ の $0\leqq x\leqq1$ における最大値と最小値を求めれば、$|g(x)|$ の最大値はそれらの絶対値の大きい方である。$\sqrt a=t$ とおくと、大小比較が因数分解でできる。",
  "sol": r"$g(x)=x^3-3ax$ とおくと　$g(0)=0$，$g(1)=1-3a$，$g'(x)=3(x^2-a)$<br>"
         r"(i) $a\leqq0$ のとき　$g'(x)\geqq0$ より $g(x)$ は増加し、$0\leqq g(x)\leqq g(1)$。よって $M(a)=1-3a$<br>"
         r"(ii) $a\geqq1$ のとき　$0\leqq x\leqq1$ で $g'(x)\leqq0$ より $g(x)$ は減少し、$g(1)\leqq g(x)\leqq0$。よって $M(a)=3a-1$<br>"
         r"(iii) $0<a<1$ のとき　$g(x)$ は $0\leqq x\leqq\sqrt a$ で減少、$\sqrt a\leqq x\leqq1$ で増加する。$g(x)$ の最大値・最小値は $g(0)=0$，$g(\sqrt a)=-2a\sqrt a$，$g(1)=1-3a$ のいずれかであり、$|g(x)|$ の最大値はそれらの絶対値の最大のものであるから　$M(a)=\max\{2a\sqrt a,\ |1-3a|\}$<br>"
         r"$t=\sqrt a\ (0<t<1)$ とおくと<br>"
         r"$2a\sqrt a-(1-3a)=2t^3+3t^2-1=(t+1)^2(2t-1)$<br>"
         r"$2a\sqrt a-(3a-1)=2t^3-3t^2+1=(t-1)^2(2t+1)>0$<br>"
         r"よって、$2a\sqrt a>3a-1$ はつねに成り立ち、$2a\sqrt a\geqq1-3a\iff t\geqq\dfrac12\iff a\geqq\dfrac14$。<br>"
         r"したがって　$0<a<\dfrac14$ のとき $M(a)=1-3a$，$\dfrac14\leqq a<1$ のとき $M(a)=2a\sqrt a$<br>"
         r"以上をまとめて　$M(a)=\begin{cases}1-3a & \left(a\leqq\dfrac14\right)\\ 2a\sqrt a & \left(\dfrac14\leqq a\leqq1\right)\\ 3a-1 & (a\geqq1)\end{cases}$<br>"
         r"$M(a)$ は $a\leqq\dfrac14$ で減少、$a\geqq\dfrac14$ で増加するから、<b>最小値は $\boldsymbol{M\left(\dfrac14\right)=\dfrac14}$</b>（$\boldsymbol{a=\dfrac14}$）",
  "note": r"$a=\dfrac14$ のとき $g(x)=x^3-\dfrac34x$ は、$0\leqq x\leqq1$ において $x=\dfrac12$ で最小値 $-\dfrac14$，$x=1$ で最大値 $\dfrac14$ をとり、$|g(x)|$ は2か所で同時に最大値に達する。「最大値の最小」は、このように2つの候補が等しくなるところで起こることが多い（次の例題も参照）。",
  "ex": r"$a$ を実数とし、$0\leqq x\leqq2$ における $|x^3-3ax|$ の最大値を $M(a)$ とする。$M(a)$ を求めよ。また、$M(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "exa": r"$a\leqq1$ のとき $M(a)=8-6a$，$1\leqq a\leqq4$ のとき $M(a)=2a\sqrt a$，$a\geqq4$ のとき $M(a)=6a-8$。最小値 $2$（$a=1$）"},
 {"lv": 5, "title": "文字定数を含む4次関数の最小値",
  "q": r"$a$ を実数の定数とする。関数 $f(x)=3x^4-4(a+1)x^3+6ax^2$ の最小値を $m(a)$ とする。<br>(1) $m(a)$ を $a$ の式で表せ。<br>(2) $b=m(a)$ のグラフの概形をかけ。",
  "hint": r"$f'(x)=12x(x-1)(x-a)$ となる。極値をとる $x$ の候補 $0,\ 1,\ a$ の大小で場合分けし、2つの極小値を比べる。比較では差 $f(a)-f(1)$ を因数分解する（$a=1$ で $0$ になることに着目）。",
  "sol": r"(1) $f'(x)=12x^3-12(a+1)x^2+12ax=12x(x-1)(x-a)$<br>"
         r"$f(0)=0$，$f(1)=2a-1$，$f(a)=3a^4-4a^4-4a^3+6a^3=-a^4+2a^3=a^3(2-a)$<br>"
         r"$x^4$ の係数が正であるから、最小値は極小値のうちで最も小さいもの（極小値が1つならそれ）である。<br>"
         r"[1] $a<0$ のとき　$a<0<1$ で、$f'(x)$ の符号は $x<a$ で負、$a<x<0$ で正、$0<x<1$ で負、$x>1$ で正。極小値は $f(a)$ と $f(1)$ で<br>"
         r"$f(a)-f(1)=-a^4+2a^3-2a+1=-(a-1)^3(a+1)$<br>"
         r"$a<0$ では $-(a-1)^3>0$ であるから、$f(a)-f(1)$ は $a+1$ と同符号。<br>"
         r"よって　$a\leqq-1$ のとき $m(a)=f(a)=-a^4+2a^3$，$-1\leqq a<0$ のとき $m(a)=f(1)=2a-1$<br>"
         r"[2] $a=0$ のとき　$f'(x)=12x^2(x-1)$ で、極小値は $f(1)=-1$ だけ。$m(0)=-1$<br>"
         r"[3] $0<a<1$ のとき　極小値は $f(0)=0$ と $f(1)=2a-1$。<br>"
         r"$0<a\leqq\dfrac12$ のとき $m(a)=2a-1$，$\dfrac12\leqq a<1$ のとき $m(a)=0$<br>"
         r"[4] $a=1$ のとき　$f'(x)=12x(x-1)^2$ で、極小値は $f(0)=0$ だけ。$m(1)=0$<br>"
         r"[5] $a>1$ のとき　$0<1<a$ で、極小値は $f(0)=0$ と $f(a)=a^3(2-a)$。<br>"
         r"$1<a\leqq2$ のとき $m(a)=0$，$a\geqq2$ のとき $m(a)=-a^4+2a^3$<br>"
         r"以上をまとめて　$m(a)=\begin{cases}-a^4+2a^3 & (a\leqq-1,\ 2\leqq a)\\ 2a-1 & \left(-1\leqq a\leqq\dfrac12\right)\\ 0 & \left(\dfrac12\leqq a\leqq2\right)\end{cases}$<br>"
         + FIG47 + r"(2) $k(a)=-a^4+2a^3$ とおくと $k'(a)=-4a^3+6a^2=-2a^2(2a-3)$ で、$k(a)$ は $a\leqq\dfrac32$ で増加、$a\geqq\dfrac32$ で減少する。$k(-1)=-3$，$k(2)=0$ であるから、$b=m(a)$ のグラフは右の図の太線のようになる。",
  "note": r"$a=1$ のとき極値をとる $x$ のうち $1$ と $a$ が一致するので、差 $f(a)-f(1)$ は $a-1$ を因数にもつ（実際は $(a-1)^3$ まで因数にもつ）。場合分けの境目 $a=-1,\ \dfrac12,\ 2$ は、いずれも「2つの極小値が等しくなる $a$」である。",
  "ex": r"$a$ を実数の定数とする。関数 $f(x)=3x^4-4(a+2)x^3+12ax^2$ の最小値 $m(a)$ を $a$ の式で表せ。",
  "exa": r"$a\leqq-2,\ 4\leqq a$ のとき $m(a)=-a^4+4a^3$，$-2\leqq a\leqq1$ のとき $m(a)=16a-16$，$1\leqq a\leqq4$ のとき $m(a)=0$"},
 {"lv": 5, "title": "最大値の最小（3次式の一様な近似）",
  "q": r"$a,\ b,\ c$ を実数とし、$-1\leqq x\leqq1$ における $|x^3+ax^2+bx+c|$ の最大値を $M$ とする。<br>(1) $M\geqq\dfrac14$ であることを証明せよ。<br>(2) $M=\dfrac14$ となるような $a,\ b,\ c$ の値を求めよ。",
  "hint": r"(1) うまく選んだ数点での値を組み合わせて、$a,\ b,\ c$ が消える式をつくる。点の候補は、最良と予想される $x^3-\dfrac34x$ が $\pm\dfrac14$ をとる $x=\pm1,\ \pm\dfrac12$。(2) 等号が成り立つ条件から4点での値が決まり、2次以下の整式の一致に持ち込める。",
  "sol": r"$f(x)=x^3+ax^2+bx+c$ とおく。<br>"
         r"(1) $f(1)-f(-1)=2+2b$，$f\left(\dfrac12\right)-f\left(-\dfrac12\right)=\dfrac14+b$ であるから<br>"
         r"$f(1)-f(-1)-2f\left(\dfrac12\right)+2f\left(-\dfrac12\right)=2+2b-2\left(\dfrac14+b\right)=\dfrac32$ …①<br>"
         r"$x=\pm1,\ \pm\dfrac12$ は $-1\leqq x\leqq1$ にあるから<br>"
         r"$f(1)\leqq M$，$-f(-1)\leqq M$，$-f\left(\dfrac12\right)\leqq M$，$f\left(-\dfrac12\right)\leqq M$ …②<br>"
         r"②を、後ろの2式は2倍して辺々加えると、①より $\dfrac32\leqq6M$。よって $M\geqq\dfrac14$ である。<br>"
         r"(2) $M=\dfrac14$ のとき、(1) で $\dfrac32\leqq6M=\dfrac32$ となるから、②の4つの不等式はすべて等号が成り立つ。すなわち<br>"
         r"$f(1)=\dfrac14$，$f(-1)=-\dfrac14$，$f\left(\dfrac12\right)=-\dfrac14$，$f\left(-\dfrac12\right)=\dfrac14$<br>"
         r"ここで $h(x)=x^3-\dfrac34x$ とおくと、$h(1)=\dfrac14$，$h(-1)=-\dfrac14$，$h\left(\dfrac12\right)=-\dfrac14$，$h\left(-\dfrac12\right)=\dfrac14$ である。<br>"
         r"よって、$f(x)-h(x)=ax^2+\left(b+\dfrac34\right)x+c$ は2次以下の整式で、4つの異なる値 $x=\pm1,\ \pm\dfrac12$ で $0$ になるから、恒等的に $0$ である。したがって $a=0$，$b=-\dfrac34$，$c=0$ が必要。<br>"
         r"逆に、$f(x)=h(x)=x^3-\dfrac34x$ のとき、$f'(x)=3x^2-\dfrac34=3\left(x+\dfrac12\right)\left(x-\dfrac12\right)$ で<br>"
         + _tb([r"$x$", r"$-1$", r"$\cdots$", r"$-\dfrac12$", r"$\cdots$", r"$\dfrac12$", r"$\cdots$", r"$1$"],
               [r"$f'(x)$", "", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$", ""],
               [r"$f(x)$", r"$-\dfrac14$", UP, r"$\dfrac14$", DN, r"$-\dfrac14$", UP, r"$\dfrac14$"])
         + r"となるから、$-1\leqq x\leqq1$ で $-\dfrac14\leqq f(x)\leqq\dfrac14$，すなわち $M=\dfrac14$ である。<br>"
         r"よって　$\boldsymbol{a=0,\ b=-\dfrac34,\ c=0}$",
  "note": r"$h(x)=x^3-\dfrac34x=\dfrac14(4x^3-3x)$ で、$x=\cos\theta$ とおくと3倍角の公式より $h(\cos\theta)=\dfrac14\cos3\theta$ となる。$\cos3\theta$ が $\pm1$ を交互にとる $\theta=0,\ \dfrac\pi3,\ \dfrac{2\pi}3,\ \pi$ が、$x=1,\ \dfrac12,\ -\dfrac12,\ -1$ に対応している（チェビシェフの多項式）。点の選び方の発見法として覚えておくとよい。",
  "ex": r"$a,\ b,\ c$ を実数とし、$0\leqq x\leqq1$ における $|x^3+ax^2+bx+c|$ の最大値を $M$ とする。$M\geqq\dfrac1{32}$ を示し、$M=\dfrac1{32}$ となる $a,\ b,\ c$ の値を求めよ。",
  "exa": r"$f(1)-f(0)-2f\left(\dfrac34\right)+2f\left(\dfrac14\right)=\dfrac3{16}\leqq6M$ から示せる。$a=-\dfrac32,\ b=\dfrac9{16},\ c=-\dfrac1{32}$"},
]})


def _grid(f, lo, hi, n=4000):
    return [f(lo + (hi - lo) * i / n) for i in range(n + 1)]


def _v4():
    x, a, b, c = symbols("x a b c")
    # 4.1
    v = _grid(lambda u: u**3 - 3*u**2, -1, 4)
    assert abs(max(v) - 16) < 1e-9 and abs(min(v) + 4) < 1e-9
    assert [(x**3 - 3*x**2).subs(x, k) for k in (-1, 0, 2, 4)] == [-4, 0, -4, 16]
    v = _grid(lambda u: 2*u**3 - 3*u**2 - 12*u, -2, 3)
    assert abs(max(v) - 7) < 1e-9 and abs(min(v) + 20) < 1e-9
    # 4.2
    V = x*(12 - 2*x)**2
    assert expand(V - (4*x**3 - 48*x**2 + 144*x)) == 0 and expand(diff(V, x) - 12*(x - 2)*(x - 6)) == 0
    assert V.subs(x, 2) == 128 and abs(max(_grid(lambda u: u*(12 - 2*u)**2, 0, 6, 6000)) - 128) < 1e-6
    V = x*(8 - 2*x)*(5 - 2*x)
    assert expand(diff(V, x) - 4*(3*x - 10)*(x - 1)) == 0 and V.subs(x, 1) == 18
    assert abs(max(_grid(lambda u: u*(8 - 2*u)*(5 - 2*u), 0, 2.5)) - 18) < 1e-6
    # 4.3
    N = 7200
    th = [2*math.pi*k/N for k in range(N)]
    ys = [2*math.cos(t)**3 + 3*math.cos(2*t) for t in th]
    assert abs(max(ys) - 5) < 1e-9 and abs(min(ys) + 3) < 1e-9
    assert {k for k in range(N) if abs(ys[k] - 5) < 1e-9} == {0}
    assert {k for k in range(N) if abs(ys[k] + 3) < 1e-9} == {N // 4, 3 * N // 4}
    ys = [2*math.sin(t)**3 + 3*math.cos(2*t) for t in th]
    assert abs(max(ys) - 3) < 1e-9 and abs(min(ys) + 5) < 1e-9
    assert {k for k in range(N) if abs(ys[k] - 3) < 1e-9} == {0, N // 2}
    assert {k for k in range(N) if abs(ys[k] + 5) < 1e-9} == {3 * N // 4}
    # 4.4
    assert expand((x - 1)**2*(x - 4) - (x**3 - 6*x**2 + 9*x - 4)) == 0
    assert expand((x - 1)**2*(2*x - 5) - (2*x**3 - 9*x**2 + 12*x - 5)) == 0
    for k in range(1, 60):
        av = k / 10
        M = max(_grid(lambda u: u**3 - 6*u**2 + 9*u, 0, av, 3000))
        ex = 4 if 1 <= av <= 4 else av**3 - 6*av**2 + 9*av
        assert abs(M - ex) < 1e-5, av
        M = max(_grid(lambda u: 2*u**3 - 9*u**2 + 12*u, 0, av, 3000))
        ex = 5 if 1 <= av <= 2.5 else 2*av**3 - 9*av**2 + 12*av
        assert abs(M - ex) < 1e-5, av
    # 4.5
    for k in range(1, 50):
        av = k / 20
        v = _grid(lambda u: u**3 - 3*av**2*u, 0, 1, 4000)
        mx = 1 - 3*av**2 if av < 3**0.5 / 3 else 0
        mn = -2*av**3 if av < 1 else 1 - 3*av**2
        assert abs(max(v) - mx) < 1e-6 and abs(min(v) - mn) < 1e-6
    for k in range(-20, 70):
        av = k / 10
        mn = min(_grid(lambda u: u**3 - 3*av*u, 0, 2, 4000))
        ex = 0 if av <= 0 else (-2*av*av**0.5 if av < 4 else 8 - 6*av)
        assert abs(mn - ex) < 1e-5, av
    # 4.6
    t = symbols("t")
    assert expand(2*t**3 + 3*t**2 - 1 - (t + 1)**2*(2*t - 1)) == 0
    assert expand(2*t**3 - 3*t**2 + 1 - (t - 1)**2*(2*t + 1)) == 0
    def M6(av, L):
        return max(abs(u) for u in _grid(lambda s: s**3 - 3*av*s, 0, L, 4000))
    def F6(av):
        return 1 - 3*av if av <= 0.25 else (2*av*av**0.5 if av <= 1 else 3*av - 1)
    def F6b(av):
        return 8 - 6*av if av <= 1 else (2*av*av**0.5 if av <= 4 else 6*av - 8)
    for k in range(-40, 80):
        av = k / 40
        assert abs(M6(av, 1) - F6(av)) < 1e-5, av
        assert abs(M6(av * 4, 2) - F6b(av * 4)) < 1e-4, av
    assert min(F6(k / 4000) for k in range(-2000, 6000)) == F6(0.25) == 0.25
    assert abs(min(F6b(k / 1000) for k in range(-2000, 6000)) - 2) < 1e-12 and F6b(1) == 2
    # 4.7
    f4 = 3*x**4 - 4*(a + 1)*x**3 + 6*a*x**2
    assert expand(diff(f4, x) - 12*x*(x - 1)*(x - a)) == 0
    assert f4.subs(x, 1) == 2*a - 1 and expand(f4.subs(x, a) - (-a**4 + 2*a**3)) == 0
    assert expand(f4.subs(x, a) - f4.subs(x, 1) + (a - 1)**3*(a + 1)) == 0
    g4 = 3*x**4 - 4*(a + 2)*x**3 + 12*a*x**2
    assert expand(diff(g4, x) - 12*x*(x - 2)*(x - a)) == 0
    assert expand(g4.subs(x, 2) - (16*a - 16)) == 0 and expand(g4.subs(x, a) - (-a**4 + 4*a**3)) == 0
    assert expand(g4.subs(x, a) - g4.subs(x, 2) + (a - 2)**3*(a + 2)) == 0
    def m7(av):
        return -av**4 + 2*av**3 if (av <= -1 or av >= 2) else (2*av - 1 if av <= 0.5 else 0)
    def m7b(av):
        return -av**4 + 4*av**3 if (av <= -2 or av >= 4) else (16*av - 16 if av <= 1 else 0)
    for k in range(-60, 121):
        av = k / 40
        fl = (lambda u, av=av: 3*u**4 - 4*(av + 1)*u**3 + 6*av*u**2)
        lo, hi = min(av, 0) - 0.5, max(av, 1) + 0.5
        mn = min(_grid(fl, lo, hi, 6000))
        ex = min(fl(0), fl(1), fl(av))
        assert abs(ex - m7(av)) < 1e-9 and mn >= ex - 1e-9 and mn - ex < 1e-4, av
        av2 = 2 * av
        gl = (lambda u, av=av2: 3*u**4 - 4*(av + 2)*u**3 + 12*av*u**2)
        lo, hi = min(av2, 0) - 0.5, max(av2, 2) + 0.5
        mn = min(_grid(gl, lo, hi, 8000))
        ex = min(gl(0), gl(2), gl(av2))
        assert abs(ex - m7b(av2)) < 1e-9 and mn >= ex - 1e-9 and mn - ex < 1e-3, av2
    k_ = -a**4 + 2*a**3
    assert expand(diff(k_, a) + 2*a**2*(2*a - 3)) == 0 and k_.subs(a, -1) == -3 and k_.subs(a, 2) == 0
    # 4.8
    f3 = x**3 + a*x**2 + b*x + c
    comb = lambda F, p: F.subs(x, p[0]) - F.subs(x, p[1]) - 2*F.subs(x, p[2]) + 2*F.subs(x, p[3])
    assert expand(comb(f3, (1, -1, Rational(1, 2), Rational(-1, 2)))) == Rational(3, 2)
    assert expand(comb(f3, (1, 0, Rational(3, 4), Rational(1, 4)))) == Rational(3, 16)
    h3 = x**3 - Rational(3, 4)*x
    assert [h3.subs(x, p) for p in (1, -1, Rational(1, 2), Rational(-1, 2))] == [Rational(1, 4), Rational(-1, 4), Rational(-1, 4), Rational(1, 4)]
    assert abs(max(abs(u) for u in _grid(lambda s: s**3 - 0.75*s, -1, 1)) - 0.25) < 1e-12
    h4 = x**3 - Rational(3, 2)*x**2 + Rational(9, 16)*x - Rational(1, 32)
    assert [h4.subs(x, p) for p in (1, 0, Rational(3, 4), Rational(1, 4))] == [Rational(1, 32), Rational(-1, 32), Rational(-1, 32), Rational(1, 32)]
    assert abs(max(abs(u) for u in _grid(lambda s: s**3 - 1.5*s**2 + 9/16*s - 1/32, 0, 1)) - 1/32) < 1e-12
    random.seed(48)
    for _ in range(300):
        A_, B_, C_ = (random.uniform(-2, 2) for _ in range(3))
        assert max(abs(u) for u in _grid(lambda s: s**3 + A_*s**2 + B_*s + C_, -1, 1, 400)) >= 0.25 - 1e-12
        assert max(abs(u) for u in _grid(lambda s: s**3 + A_*s**2 + B_*s + C_, 0, 1, 400)) >= 1/32 - 1e-12


# ---------------------------------------------------------------- 節5
_f = _F(170, 150, (-1.4, 3.6), (-5.4, 2.4))
_f.axes()
_f.curve(lambda x: x**3 - 3*x**2, -1.4, 3.6)
_f.seg((-1.4, -4), (3.6, -4))
_f.seg((2, 0), (2, -4))
_f.seg((-1.4, -2), (3.6, -2), col=C2, w=1.1, dash="")
_f.pt(2, -4)
_f.txt(2, 0, "2", dy=-4)
_f.txt(3, 0, "3", dy=-4)
_f.txt(0, -4, "−4", dx=-3, dy=11, anc="end")
_f.txt(-1.35, -2, "y=a", dy=-4, anc="start", it=True, col=C2)
FIG52 = _f.svg()

_f = _F(170, 150, (-2.5, 2.5), (-3.0, 3.0))
_f.axes()
_f.curve(lambda x: x**3 - 3*x, -2.5, 2.5)
_f.seg((-2.5, 2), (2.5, 2))
_f.seg((-2.5, -2), (2.5, -2))
for _p in ((-1, 2), (2, 2), (1, -2), (-2, -2)):
    _f.pt(*_p)
_f.txt(-2, 0, "−2", dy=-4)
_f.txt(2, 0, "2", dy=11)
_f.txt(0, 2, "2", dx=3, dy=-3, anc="start")
_f.txt(0, -2, "−2", dx=-3, dy=11, anc="end")
FIG56 = _f.svg()

_f = _F(200, 160, (-0.035, 0.43), (-0.34, 0.34))
_f.band(lambda a: -2*a**1.5, lambda a: 2*a**1.5, 0, 0.25)
_f.band(lambda a: -(1 - 3*a), lambda a: 1 - 3*a, 0.25, 1/3)
_f.axes("a", "b")
_f.curve(lambda a: 2*a**1.5, 0, 0.29, dash=DASH, w=1.2)
_f.curve(lambda a: -2*a**1.5, 0, 0.29, dash=DASH, w=1.2)
_f.curve(lambda a: 1 - 3*a, 0.2, 0.25, col=C2, w=0.9, dash=DASH)
_f.curve(lambda a: -(1 - 3*a), 0.2, 0.25, col=C2, w=0.9, dash=DASH)
_f.curve(lambda a: 1 - 3*a, 0.25, 1/3, col=C2, w=1.6)
_f.curve(lambda a: -(1 - 3*a), 0.25, 1/3, col=C2, w=1.6)
_f.seg((0, 0.25), (0.25, 0.25))
_f.seg((0, -0.25), (0.25, -0.25))
_f.seg((0.25, -0.25), (0.25, 0.25))
_f.pt(0.25, 0.25, fill="#fff")
_f.pt(0.25, -0.25, fill="#fff")
_f.pt(1/3, 0, col=C2)
_f.txt(0.25, 0, "1/4", dx=-9, dy=11)
_f.txt(1/3, 0, "1/3", dx=6, dy=11)
_f.txt(0, 0.25, "1/4", dx=-3, dy=4, anc="end")
_f.txt(0, -0.25, "−1/4", dx=-3, dy=4, anc="end")
_f.txt(0.3, 0.31, "b=2a√a", anc="end", it=True, col=C1)
FIG58 = _f.svg()

SEC.append({"title": "方程式・不等式への応用",
"base": r"""・方程式 $f(x)=0$ の実数解の個数 ＝ $y=f(x)$ のグラフと $x$ 軸の共有点の個数<br>
・定数 $a$ を含む方程式は $g(x)=a$ の形に分離し、$y=g(x)$ のグラフと直線 $y=a$ の共有点の個数を調べる<br>
・3次方程式 $f(x)=0$ が異なる3つの実数解をもつ $\iff$ $f(x)$ が極値をもち、（極大値）×（極小値）$<0$<br>
・不等式 $f(x)\geqq g(x)$ の証明：$F(x)=f(x)-g(x)$ の最小値が $0$ 以上であることを示す""",
"items": [
 {"lv": 1, "title": "3次方程式の実数解の個数",
  "q": r"方程式 $x^3-3x+1=0$ の異なる実数解の個数を求めよ。",
  "hint": r"$f(x)=x^3-3x+1$ とおき、$y=f(x)$ のグラフと $x$ 軸の共有点の個数を、極値の符号から調べる。",
  "sol": r"$f(x)=x^3-3x+1$ とおくと　$f'(x)=3x^2-3=3(x+1)(x-1)$<br>"
         + _tb([r"$x$", r"$\cdots$", r"$-1$", r"$\cdots$", r"$1$", r"$\cdots$"],
               [r"$f'(x)$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$f(x)$", UP, r"極大 $3$", DN, r"極小 $-1$", UP])
         + r"極大値 $3>0$，極小値 $-1<0$ であるから、$y=f(x)$ のグラフは $x$ 軸と3点で交わる。<br>"
         r"よって、異なる実数解の個数は　$\boldsymbol{3}$ 個",
  "note": r"$f(-2)=-1<0$，$f(0)=1>0$，$f(2)=3>0$ も合わせると、3つの解は $-2<x<-1$，$0<x<1$，$1<x<2$ の範囲に1つずつあることも分かる。",
  "ex": r"方程式 $2x^3-3x^2-12x+20=0$ の異なる実数解の個数を求めよ。",
  "exa": r"2個（極小値が $0$ で、$2x^3-3x^2-12x+20=(x-2)^2(2x+5)$）"},
 {"lv": 2, "title": "定数を分離して実数解の個数を調べる",
  "q": r"$a$ を定数とする。方程式 $x^3-3x^2-a=0$ の異なる実数解の個数を調べよ。",
  "hint": r"$x^3-3x^2=a$ と定数 $a$ を分離し、曲線 $y=x^3-3x^2$ と直線 $y=a$ の共有点の個数を調べる。",
  "sol": FIG52 + r"方程式は $x^3-3x^2=a$ と同値であるから、実数解の個数は、曲線 $y=x^3-3x^2$ と直線 $y=a$ の共有点の個数に等しい。<br>"
         r"$f(x)=x^3-3x^2$ とおくと　$f'(x)=3x^2-6x=3x(x-2)$<br>"
         + _tb([r"$x$", r"$\cdots$", r"$0$", r"$\cdots$", r"$2$", r"$\cdots$"],
               [r"$f'(x)$", r"$+$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$f(x)$", UP, r"極大 $0$", DN, r"極小 $-4$", UP])
         + r"グラフ（右図）より、異なる実数解の個数は<br>"
         r"$\boldsymbol{a<-4,\ 0<a}$ のとき <b>1個</b>，$\boldsymbol{a=-4,\ 0}$ のとき <b>2個</b>，$\boldsymbol{-4<a<0}$ のとき <b>3個</b>",
  "note": r"直線 $y=a$ は $x$ 軸に平行なので、上下に動かして共有点を数えればよい。定数をうまく分離できないときは、この節の後の例題のように極値の符号を調べる。",
  "ex": r"$a$ を定数とする。方程式 $2x^3+3x^2-12x-a=0$ の異なる実数解の個数を調べよ。",
  "exa": r"$a<-7,\ 20<a$ のとき1個，$a=-7,\ 20$ のとき2個，$-7<a<20$ のとき3個"},
 {"lv": 2, "title": "不等式の証明（微分の利用）",
  "q": r"$x\geqq0$ のとき、不等式 $x^3+4\geqq3x^2$ が成り立つことを証明せよ。また、等号が成り立つときの $x$ の値を求めよ。",
  "hint": r"（左辺）−（右辺）を $F(x)$ とおき、$x\geqq0$ における $F(x)$ の最小値が $0$ 以上であることを示す。",
  "sol": r"$F(x)=x^3+4-3x^2$ とおくと　$F'(x)=3x^2-6x=3x(x-2)$<br>$x\geqq0$ における増減表は<br>"
         + _tb([r"$x$", r"$0$", r"$\cdots$", r"$2$", r"$\cdots$"],
               [r"$F'(x)$", r"$0$", r"$-$", r"$0$", r"$+$"],
               [r"$F(x)$", r"$4$", DN, r"極小 $0$", UP])
         + r"よって、$x\geqq0$ において $F(x)$ は $x=2$ で最小値 $0$ をとるから、$F(x)\geqq0$，すなわち $x^3+4\geqq3x^2$ が成り立つ。<br>"
         r"等号が成り立つのは　$\boldsymbol{x=2}$ のとき",
  "note": r"$F(x)=x^3-3x^2+4=(x+1)(x-2)^2$ と因数分解できるので、$x\geqq-1$ で $F(x)\geqq0$ が直接分かる。微分による方法は、因数分解できない場合にも使えるのが強みである。",
  "ex": r"$x\geqq0$ のとき、不等式 $x^3+16\geqq12x$ が成り立つことを証明せよ。また、等号が成り立つときの $x$ の値を求めよ。",
  "exa": r"$F(x)=x^3-12x+16$ は $x\geqq0$ で $x=2$ のとき最小値 $0$（$F(x)=(x-2)^2(x+4)$）。等号は $x=2$ のとき"},
 {"lv": 3, "title": "文字を含む3次方程式の実数解の個数（極値の積）",
  "q": r"$a$ を実数の定数とする。$x$ の方程式 $x^3-3ax^2+4a=0$ の異なる実数解の個数を求めよ。",
  "hint": r"定数 $a$ を分離すると $a=\dfrac{x^3}{3x^2-4}$ のような分数関数になり、数学IIの範囲ではグラフがかけない。そこで $f(x)=x^3-3ax^2+4a$ の極値を求め、（極大値）×（極小値）の符号で判定する。",
  "sol": r"$f(x)=x^3-3ax^2+4a$ とおくと　$f'(x)=3x^2-6ax=3x(x-2a)$<br>"
         r"[1] $a=0$ のとき　方程式は $x^3=0$ で、実数解は $x=0$ の1個。<br>"
         r"[2] $a\neq0$ のとき　$f(x)$ は $x=0$ と $x=2a$ で極値をとり、その値は<br>"
         r"$f(0)=4a$，$f(2a)=8a^3-12a^3+4a=4a(1-a^2)$<br>"
         r"3次関数のグラフと $x$ 軸の共有点の個数は、2つの極値の積が負なら3個、$0$ なら2個、正なら1個である。<br>"
         r"$f(0)f(2a)=16a^2(1-a^2)$ で、$16a^2>0$ であるから<br>"
         r"$|a|>1$ のとき3個，$|a|=1$ のとき2個，$0<|a|<1$ のとき1個<br>"
         r"以上から<br>"
         r"$\boldsymbol{a<-1,\ 1<a}$ のとき <b>3個</b>，$\boldsymbol{a=\pm1}$ のとき <b>2個</b>，$\boldsymbol{-1<a<1}$ のとき <b>1個</b>",
  "note": r"極値の積が $0$ のときは一方の極値が $0$ で、グラフが $x$ 軸に接する（重解をもつ）。たとえば $a=1$ のとき $x^3-3x^2+4=(x+1)(x-2)^2$ となる。",
  "ex": r"$a$ を実数の定数とする。$x$ の方程式 $x^3-3ax+a=0$ の異なる実数解の個数を求めよ。",
  "exa": r"$a>\dfrac14$ のとき3個，$a=\dfrac14$ のとき2個，$a<\dfrac14$ のとき1個"},
 {"lv": 3, "title": "不等式がつねに成り立つ条件",
  "q": r"$x\geqq0$ を満たすすべての $x$ に対して、不等式 $x^3+2\geqq3ax$ が成り立つような定数 $a$ の値の範囲を求めよ。",
  "hint": r"$F(x)=x^3-3ax+2$ の $x\geqq0$ における最小値が $0$ 以上となる条件を求める。極小となる $x=\sqrt a$ があるかどうか（$a$ の符号）で場合分けする。",
  "sol": r"$F(x)=x^3-3ax+2$ とおくと　$F'(x)=3x^2-3a$<br>"
         r"[1] $a\leqq0$ のとき　$F'(x)\geqq0$ より $F(x)$ は増加するから、$x\geqq0$ で $F(x)\geqq F(0)=2>0$。よって条件を満たす。<br>"
         r"[2] $a>0$ のとき　$F'(x)=3(x+\sqrt a)(x-\sqrt a)$ で、$x\geqq0$ では $F(x)$ は $x=\sqrt a$ で最小値<br>"
         r"$F(\sqrt a)=a\sqrt a-3a\sqrt a+2=2-2a\sqrt a$<br>"
         r"をとる。条件は $2-2a\sqrt a\geqq0$，すなわち $(\sqrt a)^3\leqq1$ で、$\sqrt a\leqq1$，よって $0<a\leqq1$。<br>"
         r"[1]，[2] より　$\boldsymbol{a\leqq1}$",
  "note": r"定数 $a$ を分離して「$x>0$ で $3a\leqq x^2+\dfrac2x$」としてもよいが、右辺は分数関数で、数学IIの微分では扱えない。ただし、相加平均と相乗平均の関係を使えば $x^2+\dfrac1x+\dfrac1x\geqq3\sqrt[3]{x^2\cdot\dfrac1x\cdot\dfrac1x}=3$（等号は $x=1$）から $a\leqq1$ が得られる。",
  "ex": r"$a>0$ とする。$x\geqq0$ を満たすすべての $x$ に対して、不等式 $x^3-3a^2x+16\geqq0$ が成り立つような $a$ の値の範囲を求めよ。",
  "exa": r"$0<a\leqq2$"},
 {"lv": 4, "title": "合成関数を含む方程式の実数解の個数",
  "q": r"$f(x)=x^3-3x$ とする。$a$ を定数とするとき、$x$ の方程式 $f(f(x))=a$ の異なる実数解の個数を求めよ。",
  "hint": r"$u=f(x)$ とおき、まず $f(u)=a$ を満たす $u$ を調べ、次に各 $u$ に対して $f(x)=u$ を満たす $x$ の個数を数える。異なる $u$ からは異なる $x$ が得られるので、個数は足し合わせればよい。",
  "sol": FIG56 + r"$f'(x)=3(x+1)(x-1)$ より、$f(x)$ は $x\leqq-1$ で増加、$-1\leqq x\leqq1$ で減少、$x\geqq1$ で増加し、極大値 $f(-1)=2$，極小値 $f(1)=-2$。<br>"
         r"また、$f(x)-2=(x+1)^2(x-2)$，$f(x)+2=(x-1)^2(x+2)$ より<br>"
         r"$-2\leqq x\leqq2$ のとき $|f(x)|\leqq2$，$|x|>2$ のとき $|f(x)|>2$ …①<br>"
         r"グラフ（右図）より、方程式 $f(x)=u$ の異なる実数解の個数は<br>"
         r"$|u|<2$ のとき3個，$|u|=2$ のとき2個，$|u|>2$ のとき1個 …②<br>"
         r"$u=f(x)$ とおくと、方程式は $f(u)=a$ となる。異なる $u$ に対応する $x$ は異なる（$x$ が同じなら $u=f(x)$ も同じ）から、$f(u)=a$ の各解 $u$ について②の個数を合計すればよい。<br>"
         r"(i) $|a|>2$ のとき　①より $f(u)=a$ の解は $|u|>2$ の範囲にあり、そこで $f(u)$ は単調に変化するから、解 $u$ はただ1つ。②より1個。<br>"
         r"(ii) $a=2$ のとき　$(u+1)^2(u-2)=0$ より $u=-1,\ 2$。②より $3+2=5$ 個。$a=-2$ のときも同様に $u=1,\ -2$ で5個。<br>"
         r"(iii) $|a|<2$ のとき　①より $f(u)=a$ の解は $-2<u<2$ にあり、$f(u)$ は $-2\leqq u\leqq-1$，$-1\leqq u\leqq1$，$1\leqq u\leqq2$ のそれぞれで $-2$ と $2$ の間を単調に変化するから、解は3つ。各解は $|u|<2$ を満たすから、②より $3\times3=9$ 個。<br>"
         r"以上から<br>"
         r"$\boldsymbol{|a|<2}$ のとき <b>9個</b>，$\boldsymbol{|a|=2}$ のとき <b>5個</b>，$\boldsymbol{|a|>2}$ のとき <b>1個</b>",
  "note": r"$x=2\cos\theta\ (0\leqq\theta\leqq\pi)$ とおくと、3倍角の公式から $f(x)=2\cos3\theta$，$f(f(x))=2\cos9\theta$ となる。$|a|<2$ のとき $\cos9\theta=\dfrac a2$ を満たす $\theta$ は $0<\theta<\pi$ に9個あり（$9\theta$ が $(k-1)\pi$ から $k\pi$ まで動く各区間に1個）、①より $|x|>2$ に解はないから、9個という答えが別の方法でも確かめられる。",
  "ex": r"$f(x)=x^3-3x^2$ とする。$a$ を定数とするとき、$x$ の方程式 $f(f(x))=a$ の異なる実数解の個数を求めよ。",
  "exa": r"$a<-112$：1個，$a=-112$：2個，$-112<a<-4$：3個，$a=-4$：4個，$-4<a<0$：5個，$a=0$：3個，$a>0$：1個"},
 {"lv": 4, "title": "3次方程式の3つの解の範囲（解と係数の関係）",
  "q": r"$a$ を定数とし、3次方程式 $x^3-3x-a=0$ が異なる3つの実数解 $\alpha,\ \beta,\ \gamma\ (\alpha<\beta<\gamma)$ をもつとする。<br>(1) $a$ の値の範囲を求めよ。また、$-2<\alpha<-1<\beta<1<\gamma<2$ であることを示せ。<br>(2) $\gamma-\alpha$ のとり得る値の範囲を求めよ。",
  "hint": r"(1) は曲線 $y=x^3-3x$ と直線 $y=a$ の交点で考える。(2) は解と係数の関係から $(\gamma-\alpha)^2$ を真ん中の解 $\beta$ だけで表し、$\beta$ の動く範囲を調べる。",
  "sol": r"(1) $f(x)=x^3-3x$ とおくと、$f'(x)=3(x+1)(x-1)$ より極大値 $f(-1)=2$，極小値 $f(1)=-2$。方程式は $f(x)=a$ であり、曲線 $y=f(x)$ と直線 $y=a$ が3点で交わる条件は　$\boldsymbol{-2<a<2}$<br>"
         r"このとき、$f(-2)=-2$，$f(2)=2$ で、$f(x)$ は $-2\leqq x\leqq-1$ で $-2$ から $2$ まで増加、$-1\leqq x\leqq1$ で $2$ から $-2$ まで減少、$1\leqq x\leqq2$ で $-2$ から $2$ まで増加する。よって、$f(x)=a$ はこれら3つの区間の内部に1つずつ解をもつ。3次方程式の解は3個以下であるから、これらが $\alpha,\ \beta,\ \gamma$ であり、$-2<\alpha<-1<\beta<1<\gamma<2$ である。<br>"
         r"(2) 解と係数の関係より　$\alpha+\beta+\gamma=0$，$\alpha\beta+\beta\gamma+\gamma\alpha=-3$<br>"
         r"よって $\alpha+\gamma=-\beta$，$\alpha\gamma=-3-\beta(\alpha+\gamma)=\beta^2-3$ であるから<br>"
         r"$(\gamma-\alpha)^2=(\alpha+\gamma)^2-4\alpha\gamma=\beta^2-4(\beta^2-3)=12-3\beta^2$<br>"
         r"$a$ が $-2<a<2$ の範囲を動くとき、$\beta$ は $-1<\beta<1$ のすべての値をとる（$-1<\beta<1$ の任意の $\beta$ に対し、$a=f(\beta)$ とすれば $-2<a<2$ で、(1) より $\beta$ は真ん中の解になる）。<br>"
         r"よって $0\leqq\beta^2<1$ より $9<(\gamma-\alpha)^2\leqq12$。$\gamma-\alpha>0$ であるから　$\boldsymbol{3<\gamma-\alpha\leqq2\sqrt3}$",
  "note": r"最大値 $2\sqrt3$ をとるのは $\beta=0$，すなわち $a=0$（解は $-\sqrt3,\ 0,\ \sqrt3$）のときである。$\gamma-\alpha$ が $3$ に近づくのは $a$ が $\pm2$ に近づき、2つの解が重解に近づく場合で、重解になると「異なる3つの解」ではなくなるので $3$ は含まれない。",
  "ex": r"$a$ を定数とし、3次方程式 $x^3-12x-a=0$ が異なる3つの実数解 $\alpha,\ \beta,\ \gamma\ (\alpha<\beta<\gamma)$ をもつとする。$a$ の値の範囲と、$\gamma-\alpha$ のとり得る値の範囲を求めよ。",
  "exa": r"$-16<a<16$，$6<\gamma-\alpha\leqq4\sqrt3$"},
 {"lv": 5, "title": "3次方程式の解の配置（2つの文字を含む）",
  "q": r"3次方程式 $x^3-3ax+b=0$ が $-1\leqq x\leqq1$ の範囲に異なる3つの実数解をもつような点 $(a,\ b)$ の存在範囲を図示せよ。また、このとき $b$ のとり得る値の範囲を求めよ。",
  "hint": r"$f(x)=x^3-3ax+b$ のグラフが $-1\leqq x\leqq1$ で $x$ 軸と3回交わる条件を、(i) 極値をとる $x$ が区間内にある，(ii) 極大値が正で極小値が負，(iii) 区間の端での符号，の3つに分解する（2次方程式の解の配置と同じ発想）。",
  "sol": FIG58 + r"$f(x)=x^3-3ax+b$ とおくと　$f'(x)=3x^2-3a$<br>"
         r"異なる3つの実数解をもつには極値をもつことが必要で、$a>0$。このとき $f(x)$ は $x=-\sqrt a$ で極大、$x=\sqrt a$ で極小となる。求める条件は、次の (i)〜(iii) がすべて成り立つことである。<br>"
         r"(i) $-1<-\sqrt a$ かつ $\sqrt a<1$，すなわち $0<a<1$<br>"
         r"(ii) $f(-\sqrt a)=2a\sqrt a+b>0$ かつ $f(\sqrt a)=-2a\sqrt a+b<0$，すなわち $|b|<2a\sqrt a$<br>"
         r"(iii) $f(-1)=-1+3a+b\leqq0$ かつ $f(1)=1-3a+b\geqq0$，すなわち $|b|\leqq1-3a$<br>"
         r"［理由］異なる3解 $x_1<x_2<x_3$ が $-1\leqq x\leqq1$ にあれば、増減から $x_1<-\sqrt a<x_2<\sqrt a<x_3$ となり (i)，(ii) が成り立つ。また $f(x)$ は $x\leqq-\sqrt a$ で増加するから $f(-1)\leqq f(x_1)=0$，同様に $f(1)\geqq0$ となり (iii) も成り立つ。逆に (i)〜(iii) が成り立てば、$-1\leqq x<-\sqrt a$，$-\sqrt a<x<\sqrt a$，$\sqrt a<x\leqq1$ に1つずつ解がある。<br>"
         r"(iii) より $1-3a\geqq0$，$a\leqq\dfrac13$ であるから、(i) は $a>0$ だけでよい。<br>"
         r"曲線 $b=2a\sqrt a$ と直線 $b=1-3a$ の交点は、$t=\sqrt a$ として $2t^3+3t^2-1=(t+1)^2(2t-1)=0$ より $t=\dfrac12$，すなわち点 $\left(\dfrac14,\ \dfrac14\right)$ で、$0<a<\dfrac14$ では $2a\sqrt a<1-3a$，$a>\dfrac14$ では $2a\sqrt a>1-3a$ である。<br>"
         r"よって、求める範囲は<br>"
         r"$0<a\leqq\dfrac14$ のとき $|b|<2a\sqrt a$，$\dfrac14<a\leqq\dfrac13$ のとき $|b|\leqq1-3a$<br>"
         r"で、<b>右の図の塗った部分</b>である。ただし、曲線 $b=\pm2a\sqrt a$ 上の点（2点 $\left(\dfrac14,\ \pm\dfrac14\right)$ を含む）と原点は含まず、線分 $b=\pm(1-3a)\ \left(\dfrac14<a\leqq\dfrac13\right)$ 上の点は含む。<br>"
         r"<b>$b$ の範囲</b>　この範囲では、$0<a\leqq\dfrac14$ のとき $|b|<2a\sqrt a\leqq\dfrac14$，$\dfrac14<a\leqq\dfrac13$ のとき $|b|\leqq1-3a<\dfrac14$ であるから、$|b|<\dfrac14$。逆に $|b|<\dfrac14$ ならば、点 $\left(\dfrac14,\ b\right)$ はこの範囲に含まれる。<br>"
         r"よって　$\boldsymbol{-\dfrac14<b<\dfrac14}$",
  "note": r"$(a,\ b)=\left(\dfrac14,\ \pm\dfrac14\right)$ のとき、方程式は $\left(x\mp\dfrac12\right)^2(x\pm1)=0$（複号同順）となって重解をもつので、除かれる。$|b|<\dfrac14$ という結論は、前節の「最大値の最小」の例題で見た $\left|x^3-\dfrac34x\right|\leqq\dfrac14$ と関係が深い。",
  "ex": r"3次方程式 $x^3-3ax+b=0$ が $-2\leqq x\leqq2$ の範囲に異なる3つの実数解をもつような点 $(a,\ b)$ の存在範囲を求めよ。また、このとき $b$ のとり得る値の範囲を求めよ。",
  "exa": r"$0<a\leqq1$ のとき $|b|<2a\sqrt a$，$1<a\leqq\dfrac43$ のとき $|b|\leqq8-6a$。$b$ の範囲は $-2<b<2$"},
]})


def _v5():
    x, a = symbols("x a")
    # 5.1
    assert _nroots(x**3 - 3*x + 1, x) == 3
    assert _nroots(2*x**3 - 3*x**2 - 12*x + 20, x) == 2 and expand((x - 2)**2*(2*x + 5) - (2*x**3 - 3*x**2 - 12*x + 20)) == 0
    f = x**3 - 3*x + 1
    assert [f.subs(x, k) for k in (-2, -1, 0, 1, 2)] == [-1, 3, 1, -1, 3]
    # 5.2, 5.4
    for k in range(-60, 61):
        av = Rational(k, 8)
        n = _nroots(x**3 - 3*x**2 - av, x)
        assert n == (2 if av in (0, -4) else 3 if -4 < av < 0 else 1)
        n = _nroots(2*x**3 + 3*x**2 - 12*x - av * 4, x)
        b4 = av * 4
        assert n == (2 if b4 in (-7, 20) else 3 if -7 < b4 < 20 else 1)
        av2 = av / 4
        n = _nroots(x**3 - 3*av2*x**2 + 4*av2, x)
        assert n == (3 if abs(av2) > 1 else 2 if abs(av2) == 1 else 1), av2
        n = _nroots(x**3 - 3*av2*x + av2, x)
        assert n == (3 if av2 > Rational(1, 4) else 2 if av2 == Rational(1, 4) else 1), av2
    assert _nroots(x**3 - 3*x + Rational(1, 4), x) == 3 and _nroots(x**3 - Rational(3, 4)*x + Rational(1, 4), x) == 2
    assert expand((x + 1)*(x - 2)**2 - (x**3 - 3*x**2 + 4)) == 0
    # 5.3
    assert expand((x + 1)*(x - 2)**2 - (x**3 + 4 - 3*x**2)) == 0
    assert expand((x - 2)**2*(x + 4) - (x**3 + 16 - 12*x)) == 0
    v = _grid(lambda u: u**3 + 4 - 3*u**2, 0, 10, 5000)
    assert min(v) >= -1e-12 and abs(min(v)) < 1e-12
    v = _grid(lambda u: u**3 + 16 - 12*u, 0, 10, 5000)
    assert min(v) >= -1e-12 and abs(min(v)) < 1e-12
    # 5.5
    for k in range(-30, 60):
        av = k / 20
        mn = min(_grid(lambda u: u**3 - 3*av*u + 2, 0, 4, 8000))
        ex = 2 if av <= 0 else 2 - 2*av**1.5
        assert abs(mn - ex) < 1e-5 and ((ex >= 0) == (av <= 1))
        if av > 0:
            bv = av * 2
            mn = min(_grid(lambda u: u**3 - 3*bv**2*u + 16, 0, 8, 8000))
            assert abs(mn - (16 - 2*bv**3)) < 1e-3 and ((16 - 2*bv**3 >= 0) == (bv <= 2))
    # 5.6（合成した9次方程式の実数解を厳密に数える）
    f = lambda u: u**3 - 3*u
    for av in [Rational(k, 4) for k in range(-12, 13)] + [Rational(19, 10), Rational(-21, 10)]:
        n = _nroots(f(f(x)) - av, x)
        assert n == (9 if abs(av) < 2 else 5 if abs(av) == 2 else 1), av
    g = lambda u: u**3 - 3*u**2
    assert g(-4) == -112 and g(-1) == -4
    for av in [S(-200), S(-112), S(-111), S(-50), S(-5), S(-4), Rational(-39, 10), S(-2), Rational(-1, 10), S(0), Rational(1, 10), S(3)]:
        n = _nroots(g(g(x)) - av, x)
        exp_ = (1 if av < -112 else 2 if av == -112 else 3 if av < -4 else 4 if av == -4 else 5 if av < 0 else 3 if av == 0 else 1)
        assert n == exp_, (av, n)
    # 5.7
    import numpy as np
    random.seed(57)
    vals = []
    for _ in range(400):
        av = random.uniform(-1.999, 1.999)
        r = sorted(np.roots([1, 0, -3, -av]).real)
        al, be, ga = r
        assert -2 < al < -1 < be < 1 < ga < 2
        assert abs((ga - al)**2 - (12 - 3*be**2)) < 1e-8
        vals.append(ga - al)
    assert 3 < min(vals) and max(vals) <= 2*3**0.5 + 1e-12
    r = sorted(np.roots([1, 0, -3, 0]).real)
    assert abs(r[2] - r[0] - 2*3**0.5) < 1e-12
    for _ in range(200):
        av = random.uniform(-15.99, 15.99)
        r = sorted(np.roots([1, 0, -12, -av]).real)
        assert abs((r[2] - r[0])**2 - (48 - 3*r[1]**2)) < 1e-7 and 6 < r[2] - r[0] <= 4*3**0.5 + 1e-12
    # 5.8（[-L, L] 内の異なる実数解の個数を厳密に数え、領域と照合）
    def n_in(p, L):
        q = Poly(p, x).sqf_part()
        return q.count_roots(-L, L)
    t = symbols("t")
    assert expand(2*t**3 + 3*t**2 - 1 - (t + 1)**2*(2*t - 1)) == 0
    assert expand(2*t**3 + 6*t**2 - 8 - 2*(t - 1)*(t + 2)**2) == 0
    def reg1(av, bv):
        if av <= 0:
            return False
        if av <= Rational(1, 4):
            return bv**2 < 4*av**3
        return av <= Rational(1, 3) and abs(bv) <= 1 - 3*av
    def reg2(av, bv):
        if av <= 0:
            return False
        if av <= 1:
            return bv**2 < 4*av**3
        return av <= Rational(4, 3) and abs(bv) <= 8 - 6*av
    random.seed(58)
    pts = [(Rational(random.randint(-10, 150), 360), Rational(random.randint(-120, 120), 360)) for _ in range(500)]
    pts += [(Rational(1, 4), Rational(1, 4)), (Rational(1, 4), Rational(-1, 4)), (Rational(1, 3), 0), (Rational(3, 10), Rational(1, 10)),
            (Rational(3, 10), Rational(1, 10) + Rational(1, 1000)), (Rational(1, 4), Rational(249, 1000))]
    for av, bv in pts:
        p = x**3 - 3*av*x + bv
        assert (n_in(p, 1) == 3) == reg1(av, bv), (av, bv)
        assert (n_in(x**3 - 3*(4*av)*x + 8*bv, 2) == 3) == reg2(4*av, 8*bv), (av, bv)
        if reg1(av, bv):
            assert abs(bv) < Rational(1, 4)
    assert all(reg1(Rational(1, 4), Rational(k, 100)) for k in range(-24, 25))
    assert expand((x - Rational(1, 2))**2*(x + 1) - (x**3 - Rational(3, 4)*x + Rational(1, 4))) == 0


# ---------------------------------------------------------------- 節6
_f = _F(180, 165, (-2.25, 2.25), (-2.6, 2.6))
_f.axes()
_f.curve(lambda x: x**3 - 3*x, -2.25, 2.25)
_P6 = {"P": 1.8, "Q": -1.2, "R": -1.8, "S": 1.2}
_V6 = [(_P6[k], _P6[k]**3 - 3*_P6[k]) for k in "PQRS"]
for _i in range(4):
    _f.seg(_V6[_i], _V6[(_i + 1) % 4], col=C2, w=1.2, dash="")
_f.seg(_V6[0], _V6[2])
_f.seg(_V6[1], _V6[3])
for (_xx, _yy), _nm, _dx, _dy in zip(_V6, "PQRS", (6, -2, -6, 4), (-2, -5, 3, 11)):
    _f.pt(_xx, _yy)
    _f.txt(_xx, _yy, _nm, dx=_dx, dy=_dy, anc="middle", size=11)
_f.pt(0, 0, col=C2)
_f.txt(0, 0, "K", dx=-7, dy=-4, size=11, col=C2)
FIG63 = _f.svg()

SEC.append({"title": "3次関数のグラフの性質",
"base": r"""・3次関数 $f(x)=ax^3+bx^2+cx+d$ のグラフは、点 $\left(p,\ f(p)\right)$ $\left(p=-\dfrac b{3a}\right)$ に関して対称（この点をグラフの対称の中心という）<br>
・極値をもつとき、極大点と極小点の中点は対称の中心である<br>
・$x=t$ の点における接線とグラフの他の共有点の $x$ 座標 $s$ は、3次方程式の3解 $t,\ t,\ s$ の和から $2t+s=-\dfrac ba$ として求まる""",
"items": [
 {"lv": 2, "title": "3次関数のグラフの対称性",
  "q": r"(1) 3次関数 $f(x)=ax^3+bx^2+cx+d\ (a\neq0)$ のグラフは、点 $\mathrm{K}(p,\ f(p))$ $\left(p=-\dfrac b{3a}\right)$ に関して対称であることを示せ。<br>(2) 曲線 $y=x^3-6x^2+9x-2$ の対称の中心の座標を求めよ。",
  "hint": r"$f(p+h)$ を $h$ について整理すると、$p=-\dfrac b{3a}$ のとき $h^2$ の項が消えて $f(p)+kh+ah^3$ の形になる。これから $f(p+h)+f(p-h)=2f(p)$ が分かる。",
  "sol": r"(1) $f(p+h)=a(p+h)^3+b(p+h)^2+c(p+h)+d$ を $h$ について整理すると<br>"
         r"$f(p+h)=f(p)+(3ap^2+2bp+c)h+(3ap+b)h^2+ah^3$<br>"
         r"$p=-\dfrac b{3a}$ のとき $3ap+b=0$ であるから、$k=3ap^2+2bp+c$ とおくと　$f(p+h)=f(p)+kh+ah^3$<br>"
         r"$h$ を $-h$ に変えて $f(p-h)=f(p)-kh-ah^3$ であるから、すべての $h$ について　$f(p+h)+f(p-h)=2f(p)$<br>"
         r"よって、グラフ上の任意の点 $(p+h,\ f(p+h))$ の K に関する対称点 $(p-h,\ 2f(p)-f(p+h))=(p-h,\ f(p-h))$ もグラフ上にある。すなわち、グラフは K に関して対称である。<br>"
         r"(2) $p=-\dfrac{-6}{3\cdot1}=2$，$f(2)=8-24+18-2=0$ より、対称の中心は　$\boldsymbol{(2,\ 0)}$",
  "note": r"K はグラフの<b>変曲点</b>（数学IIIで学ぶ）でもある。$k=f'(p)$ であり、K における接線は $y=f(p)+k(x-p)$。極値をもつとき、極大点と極小点は K に関して対称で、その中点が K になる（第3節の最初の例題では、極大点 $(1,\ 2)$ と極小点 $(3,\ -2)$ の中点が $(2,\ 0)$）。",
  "ex": r"曲線 $y=-x^3+3x^2+1$ の対称の中心の座標を求め、極大点と極小点の中点がそれと一致することを確かめよ。",
  "exa": r"$(1,\ 3)$。極大点 $(2,\ 5)$ と極小点 $(0,\ 1)$ の中点は $(1,\ 3)$"},
 {"lv": 3, "title": "接線が曲線と再び交わる点・平行な2接線",
  "q": r"曲線 $C:y=x^3-3x^2+2$ について、次の問いに答えよ。<br>(1) $C$ 上の点 $\mathrm{P}(t,\ t^3-3t^2+2)$ における接線が、$C$ と P 以外の点 Q で交わるとき、Q の $x$ 座標を $t$ で表せ。また、そのような Q が存在しない $t$ の値を求めよ。<br>(2) $C$ 上の異なる2点 R，S における接線が平行であるとき、線分 RS の中点は R，S のとり方によらない定点であることを示せ。",
  "hint": r"(1) 曲線の式から接線の式を引いた3次式は $(x-t)^2$ で割り切れる。残りの1次因数を $x^2$ の係数の比較（3解の和）で決める。(2) 傾きが等しい条件 $f'(r)=f'(s)$ から $r+s$ が一定になる。",
  "sol": r"$f(x)=x^3-3x^2+2$ とおくと　$f'(x)=3x^2-6x$<br>"
         r"(1) P における接線を $y=\ell(x)$ とすると、$g(x)=f(x)-\ell(x)$ は $x^3$ の係数が $1$ の3次式で、$g(t)=0$，$g'(t)=f'(t)-f'(t)=0$ であるから、$(x-t)^2$ で割り切れる（第1節）。よって<br>"
         r"$g(x)=(x-t)^2(x-s)$<br>とおける。$\ell(x)$ は1次式であるから、両辺の $x^2$ の係数を比べて $-3=-(2t+s)$，よって $s=3-2t$。<br>"
         r"Q が存在するのは $s\neq t$，すなわち $3-2t\neq t$ より $t\neq1$ のときで、Q の $x$ 座標は　$\boldsymbol{3-2t}$<br>"
         r"Q が存在しないのは　$\boldsymbol{t=1}$　のときである（このとき $g(x)=(x-1)^3$）。<br>"
         r"(2) R，S の $x$ 座標を $r,\ s\ (r\neq s)$ とする。接線が平行であるから $f'(r)=f'(s)$ で<br>"
         r"$3r^2-6r=3s^2-6s$，$3(r-s)(r+s-2)=0$，$r\neq s$ より $r+s=2$<br>"
         r"ここで $f(1+h)=(1+h)^3-3(1+h)^2+2=h^3-3h$ であるから、$f(1+h)+f(1-h)=0$。$r=1+h$ とおくと $s=1-h$ であるから<br>"
         r"$\dfrac{r+s}2=1$，$\dfrac{f(r)+f(s)}2=\dfrac{f(1+h)+f(1-h)}2=0$<br>"
         r"よって、線分 RS の中点は定点 $\boldsymbol{(1,\ 0)}$ である。",
  "note": r"定点 $(1,\ 0)$ は $C$ の対称の中心である。(1) で $t=1$ のとき、接線は $C$ と P だけを共有し（3重解）、P で曲線を横切る。一般に、$y=ax^3+bx^2+\cdots$ では Q の $x$ 座標は $-\dfrac ba-2t$ となる。",
  "ex": r"曲線 $y=x^3+3x^2-x$ 上の点 P（$x$ 座標 $t$）における接線が P 以外で曲線と交わる点 Q の $x$ 座標を求めよ。また、この曲線上の異なる2点における接線が平行であるとき、2点を結ぶ線分の中点の座標を求めよ。",
  "exa": r"Q の $x$ 座標は $-2t-3$（$t\neq-1$）。中点は $(-1,\ 3)$"},
 {"lv": 5, "title": "3次関数のグラフに4頂点をもつ平行四辺形",
  "q": r"3次関数 $y=f(x)$ のグラフ $C$ 上に4つの頂点をもつ平行四辺形 PQRS があるとき、その対角線の交点 M は $C$ の対称の中心であることを証明せよ。",
  "hint": r"平行四辺形の対角線は互いに他を2等分するので、R，S はそれぞれ P，Q の M に関する対称点である。$C$ を M に関して対称移動した曲線を考えると、P，Q，R，S はすべて2曲線の共有点になる。共有点の $x$ 座標を表す方程式の次数に注目する。",
  "sol": FIG63 + r"$f(x)=ax^3+bx^2+cx+d\ (a\neq0)$，$p=-\dfrac b{3a}$ とし、$C$ の対称の中心を $\mathrm{K}(p,\ f(p))$ とする。この節の最初の例題より、$k=f'(p)$ として、任意の実数 $X$ に対し<br>"
         r"$f(p+X)=f(p)+kX+aX^3$ …①<br>"
         r"M の座標を $(m,\ n)$ とする。平行四辺形の対角線は互いに他を2等分するから、R は P の、S は Q の M に関する対称点である。点 $(x,\ y)$ の M に関する対称点は $(2m-x,\ 2n-y)$ であるから、$\mathrm{P}(x_1,\ f(x_1))$ の対称点 $\mathrm{R}(2m-x_1,\ 2n-f(x_1))$ が $C$ 上にあることより<br>"
         r"$f(x_1)+f(2m-x_1)=2n$<br>"
         r"すなわち、$x_1$ は方程式 $F(x)=f(x)+f(2m-x)-2n=0$ の解である。$F(2m-x)=F(x)$ であるから $2m-x_1$ も解であり、Q，S についても同様。よって、P，Q，R，S の $x$ 座標はすべて $F(x)=0$ の解である。<br>"
         r"P，Q，R，S は関数のグラフ上の異なる4点であるから、それらの $x$ 座標は互いに異なる。よって、$F(x)=0$ は異なる4つの実数解をもつ。<br>"
         r"ここで $x=p+X$，$m=p+\mu$ とおくと $2m-x=p+(2\mu-X)$ であり、①より<br>"
         r"$F(x)=2f(p)+2k\mu+a\{X^3+(2\mu-X)^3\}-2n$<br>"
         r"$=6a\mu X^2-12a\mu^2X+8a\mu^3+2k\mu+2f(p)-2n$<br>"
         r"もし $\mu\neq0$ なら、$6a\mu\neq0$ より $F(x)=0$ は $X$ の2次方程式となり、解は高々2個で矛盾する。よって $\mu=0$，すなわち $m=p$。<br>"
         r"このとき $F(x)=2f(p)-2n$（定数）であり、$F(x)=0$ は解をもつから $n=f(p)$。<br>"
         r"したがって M は K と一致し、M は $C$ の対称の中心である。",
  "note": r"逆に、K と異なる $C$ 上の2点 P，Q（P，Q，K は一直線上にないもの）をとり、K に関する対称点をそれぞれ R，S とすると、$C$ は K に関して対称だから R，S も $C$ 上にあり、対角線が K で互いに2等分されるので PQRS は平行四辺形になる。つまり、3次関数のグラフに4頂点をもつ平行四辺形は無数にあり、その中心はすべて K である。",
  "ex": r"3次関数 $y=f(x)$ のグラフ $C$ を、点 $\mathrm{M}(m,\ n)$ に関して対称移動した曲線を $C'$ とする。M が $C$ の対称の中心でないとき、$C$ と $C'$ の共有点は2個以下であることを示せ。",
  "exa": r"共有点の $x$ 座標は $f(x)+f(2m-x)=2n$ の解。$m$ が対称の中心の $x$ 座標 $p$ と異なれば、これは2次方程式。$m=p$ なら $n\neq f(p)$ となり解をもたない。"},
]})


def _v6():
    x, h, a, b, c, d, X, mu, k, n = symbols("x h a b c d X mu k n")
    f = a*x**3 + b*x**2 + c*x + d
    p = -b / (3*a)
    fph = f.subs(x, p + h)
    assert simplify(fph - (f.subs(x, p) + (3*a*p**2 + 2*b*p + c)*h + a*h**3)) == 0
    assert simplify(fph + f.subs(x, p - h) - 2*f.subs(x, p)) == 0
    assert simplify(diff(f, x).subs(x, p) - (3*a*p**2 + 2*b*p + c)) == 0
    g = x**3 - 6*x**2 + 9*x - 2
    assert g.subs(x, 2) == 0 and expand(g.subs(x, 2 + h) + g.subs(x, 2 - h)) == 0
    g = -x**3 + 3*x**2 + 1
    assert g.subs(x, 1) == 3 and set(solve(diff(g, x), x)) == {0, 2} and (g.subs(x, 0), g.subs(x, 2)) == (1, 5)
    assert expand(g.subs(x, 1 + h) + g.subs(x, 1 - h)) == 6
    # 6.2
    t, s = symbols("t s")
    f = x**3 - 3*x**2 + 2
    l = expand(diff(f, x).subs(x, t)*(x - t) + f.subs(x, t))
    assert expand(f - l - (x - t)**2*(x - (3 - 2*t))) == 0
    assert expand((f - l).subs(t, 1) - (x - 1)**3) == 0
    assert expand(f.subs(x, 1 + h) - (h**3 - 3*h)) == 0
    assert expand(diff(f, x).subs(x, t) - diff(f, x).subs(x, s) - 3*(t - s)*(t + s - 2)) == 0
    f = x**3 + 3*x**2 - x
    l = expand(diff(f, x).subs(x, t)*(x - t) + f.subs(x, t))
    assert expand(f - l - (x - t)**2*(x - (-2*t - 3))) == 0
    assert f.subs(x, -1) == 3 and expand(f.subs(x, -1 + h) + f.subs(x, -1 - h)) == 6
    assert simplify((diff(f, x).subs(x, t) - diff(f, x).subs(x, s)) / (t - s) - 3*(t + s + 2)) == 0
    # 6.3
    pp = symbols("pp")
    F = lambda u: n + k*(u - pp) + a*(u - pp)**3      # 対称の中心 (pp, n) をもつ一般の3次関数の形（①）
    m_ = pp + mu
    expr = F(pp + X) + F(2*m_ - (pp + X)) - 2*symbols("nn")
    target = 6*a*mu*X**2 - 12*a*mu**2*X + 8*a*mu**3 + 2*k*mu + 2*n - 2*symbols("nn")
    assert expand(expr - target) == 0
    # 一般の3次式は①の形に書ける
    ff = a*x**3 + b*x**2 + c*x + d
    pv = -b / (3*a)
    assert simplify(ff - (ff.subs(x, pv) + diff(ff, x).subs(x, pv)*(x - pv) + a*(x - pv)**3)) == 0
    # 図の平行四辺形：中心が原点で、4頂点が y=x^3-3x 上
    V = [(u, u**3 - 3*u) for u in (1.8, -1.2, -1.8, 1.2)]
    assert all(abs(V[i][0] + V[i + 2][0]) < 1e-12 and abs(V[i][1] + V[i + 2][1]) < 1e-12 for i in range(2))
    # f(x)+f(2m-x)-2n は高々2次で、x^2 の係数は 6a(m-p)。m=p なら定数 2f(p)-2n（練習の内容）
    m = symbols("m")
    Fx = Poly(expand(ff + ff.subs(x, 2*m - x) - 2*n), x)
    assert Fx.degree() == 2 and simplify(Fx.all_coeffs()[0] - 6*a*(m - pv)) == 0
    assert simplify(expand(ff + ff.subs(x, 2*pv - x) - 2*n) - (2*ff.subs(x, pv) - 2*n)) == 0


# ---------------------------------------------------------------- 章のまとめと検算
CH = {"no": 14, "sections": SEC}


def verify():
    for v in [g for k, g in sorted(globals().items()) if k.startswith("_v") and callable(g)]:
        v()
    items = [it for s in SEC for it in s["items"]]
    lv = [it["lv"] for it in items]
    assert 37 <= len(items) <= 43, len(items)              # 目標 40±3
    assert lv.count(5) >= 5 and lv.count(4) >= 6            # ★5 は5題（最低3題）
    assert lv.count(1) >= 7 and lv.count(2) >= 9 and lv.count(3) >= 9
    assert 4 <= len(SEC) <= 9 and all(it["lv"] in (1, 2, 3, 4, 5) for it in items)
    for s_ in SEC:                                            # 節の中は易しい順
        ls = [it["lv"] for it in s_["items"]]
        assert ls == sorted(ls), s_["title"]
    for it in items:
        for k_ in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
            assert it.get(k_) not in (None, ""), (it["title"], k_)
        for k_ in ("q", "hint", "sol", "note", "ex", "exa", "title"):
            assert it.get(k_, "").count("$") % 2 == 0, (it["title"], k_)
            assert "$$" not in it.get(k_, ""), (it["title"], k_)
    print("c14:", len(items), "題", {k: lv.count(k) for k in range(1, 6)})
