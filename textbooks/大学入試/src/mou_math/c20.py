"""第20章 複素数平面（数学C）"""
import math, cmath, random
from sympy import (symbols, I, sqrt, simplify, expand, Rational, cos, sin, pi, binomial,
                   re as sre, im as sim, conjugate, Poly, rem, solve, nsimplify, expand_trig, Abs)

# ---------------------------------------------------------------- 図の道具（座標は Python で計算）
FS = 'font-family="Liberation Serif,DejaVu Serif,serif"'
HALO = 'stroke="#fff" stroke-width="2.6" stroke-linejoin="round" paint-order="stroke"'
BLUE, RED, GRAY, FILL = "#1f3f8f", "#c0392b", "#777", "#dbe4f6"


class Fig:
    def __init__(s, xmin, xmax, ymin, ymax, sc, pad=10):
        s.xmin, s.ymax, s.sc, s.pad = xmin, ymax, sc, pad
        s.W = round((xmax - xmin) * sc + 2 * pad)
        s.H = round((ymax - ymin) * sc + 2 * pad)
        s.el = []

    def p(s, z):
        z = complex(z)
        return s.pad + (z.real - s.xmin) * s.sc, s.pad + (s.ymax - z.imag) * s.sc

    def pts(s, zs):
        return " ".join("%.1f,%.1f" % s.p(z) for z in zs)

    def arrow(s, a, b):
        (x1, y1), (x2, y2) = s.p(a), s.p(b)
        L = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / L, (y2 - y1) / L
        s.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#444" stroke-width="0.9"/>')
        s.el.append(f'<polygon points="{x2+ux:.1f},{y2+uy:.1f} {x2-6*ux-3*uy:.1f},{y2-6*uy+3*ux:.1f} {x2-6*ux+3*uy:.1f},{y2-6*uy-3*ux:.1f}" fill="#444"/>')

    def axes(s, x0, x1, y0, y1, lx="x", ly="y"):
        s.arrow(complex(x0, 0), complex(x1, 0)); s.arrow(complex(0, y0), complex(0, y1))
        s.text(complex(x1, 0), lx, -4, 13, it=True)
        s.text(complex(0, y1), ly, 5, 8, it=True)
        s.text(0, "O", -11, 12)

    def line(s, a, b, col=BLUE, w=1.2, dash=None):
        (x1, y1), (x2, y2) = s.p(a), s.p(b)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>')

    def poly(s, zs, fill=FILL, col=BLUE, w=1.2, dash=None, op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.el.append(f'<polygon points="{s.pts(zs)}" fill="{fill}" fill-opacity="{op}" stroke="{col}" stroke-width="{w}"{d}/>')

    def pline(s, zs, col=BLUE, w=1.3, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        s.el.append(f'<polyline points="{s.pts(zs)}" fill="none" stroke="{col}" stroke-width="{w}"{d}/>')

    def circle(s, c, r, col=BLUE, w=1.2, dash=None, fill="none"):
        x, y = s.p(c); d = f' stroke-dasharray="{dash}"' if dash else ""
        s.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r*s.sc:.1f}" fill="{fill}" stroke="{col}" stroke-width="{w}"{d}/>')

    def dot(s, z, col="#222", r=2.2):
        x, y = s.p(z)
        s.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>')

    def text(s, z, t, dx=0, dy=0, it=False, size=11, anchor="start", col="#222"):
        x, y = s.p(z); st = ' font-style="italic"' if it else ""
        s.el.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="{size}"{st} text-anchor="{anchor}" fill="{col}" {FS} {HALO}>{t}</text>')

    def svg(s):
        return (f'<svg class="fig" width="{s.W}" height="{s.H}" viewBox="0 0 {s.W} {s.H}" '
                f'xmlns="http://www.w3.org/2000/svg">' + "".join(s.el) + "</svg>")


SEC = []

# ---------------------------------------------------------------- 節1
SEC.append({"title": "複素数平面・共役複素数・絶対値",
"base": r"""・複素数 $z=a+bi$ を座標平面上の点 $(a,\ b)$ に対応させた平面を<b>複素数平面</b>という（$x$ 軸を実軸、$y$ 軸を虚軸という）。<br>
・共役複素数 $\overline{z}=a-bi$ は $z$ と実軸に関して対称な点。$\overline{\alpha\pm\beta}=\overline{\alpha}\pm\overline{\beta}$，$\overline{\alpha\beta}=\overline{\alpha}\,\overline{\beta}$，$\overline{\left(\dfrac{\alpha}{\beta}\right)}=\dfrac{\overline{\alpha}}{\overline{\beta}}$<br>
・$z$ が実数 $\iff\overline{z}=z$　　$z$ が純虚数 $\iff\overline{z}=-z$ かつ $z\neq0$<br>
・絶対値 $|z|=\sqrt{a^2+b^2}$，$|z|^2=z\overline{z}$，$|\alpha\beta|=|\alpha||\beta|$，$\left|\dfrac\alpha\beta\right|=\dfrac{|\alpha|}{|\beta|}$。2点 $\alpha,\ \beta$ 間の距離は $|\beta-\alpha|$<br>
・2点 $\alpha,\ \beta$ を結ぶ線分を $m:n$ に内分する点は $\dfrac{n\alpha+m\beta}{m+n}$，外分する点は $\dfrac{-n\alpha+m\beta}{m-n}$""",
"items": [
 {"lv": 1, "title": "2点間の距離・内分点・外分点",
  "q": r"複素数平面上の2点 $\mathrm{A}(2+3i)$，$\mathrm{B}(-4+i)$ について、次のものを求めよ。<br>(1) 2点 A，B 間の距離　(2) 線分 AB を $1:2$ に内分する点　(3) 線分 AB を $2:1$ に外分する点",
  "hint": r"点 $\alpha$ と点 $\beta$ の距離は $|\beta-\alpha|$。内分点・外分点は、座標平面と同じ公式を複素数のまま使えばよい。",
  "sol": r"(1) $\mathrm{AB}=|(-4+i)-(2+3i)|=|-6-2i|=\sqrt{36+4}=\boldsymbol{2\sqrt{10}}$<br>"
         r"(2) $\dfrac{2(2+3i)+1\cdot(-4+i)}{1+2}=\dfrac{7i}{3}$ より　$\boldsymbol{\dfrac73i}$<br>"
         r"(3) $\dfrac{-1\cdot(2+3i)+2(-4+i)}{2-1}=\boldsymbol{-10-i}$",
  "note": r"複素数の和・差・実数倍は、平面ベクトルの演算と同じ規則にしたがう。$\beta-\alpha$ は $\overrightarrow{\mathrm{AB}}$ に対応し、3点 $\mathrm{A}(\alpha)$，$\mathrm{B}(\beta)$，$\mathrm{C}(\gamma)$ を頂点とする三角形の重心は $\dfrac{\alpha+\beta+\gamma}3$ である。",
  "ex": r"2点 $\mathrm{A}(1-2i)$，$\mathrm{B}(5+4i)$ について、(1) 2点 A，B 間の距離　(2) 線分 AB を $3:1$ に内分する点　(3) 線分 AB を $1:3$ に外分する点 を求めよ。",
  "exa": r"(1) $2\sqrt{13}$　(2) $4+\dfrac52i$　(3) $-1-5i$"},
 {"lv": 1, "title": "共役複素数と絶対値の計算",
  "q": r"$z=\dfrac{1+3i}{2-i}$ のとき、$z$，$\overline{z}$，$|z|$ を求めよ。また、$z+\overline{z}$，$z\overline{z}$ の値を求めよ。",
  "hint": r"分母の共役複素数 $2+i$ を分母・分子に掛けて $a+bi$ の形にする。絶対値は $\left|\dfrac\alpha\beta\right|=\dfrac{|\alpha|}{|\beta|}$ を使うと速い。",
  "sol": r"$z=\dfrac{(1+3i)(2+i)}{(2-i)(2+i)}=\dfrac{2+i+6i+3i^2}{5}=\boldsymbol{\dfrac{-1+7i}5}$，　$\overline{z}=\boldsymbol{\dfrac{-1-7i}5}$<br>"
         r"$|z|=\dfrac{|1+3i|}{|2-i|}=\dfrac{\sqrt{10}}{\sqrt5}=\boldsymbol{\sqrt2}$<br>"
         r"$z+\overline{z}=\boldsymbol{-\dfrac25}$，　$z\overline{z}=|z|^2=\boldsymbol{2}$",
  "note": r"$z=a+bi$ のとき $z+\overline{z}=2a$，$z\overline{z}=a^2+b^2$ はともに実数である。$z$，$\overline{z}$ は2次方程式 $t^2-(z+\overline z)t+z\overline z=0$，すなわち $5t^2+2t+10=0$ の2つの解になっている。",
  "ex": r"$z=\dfrac{4+2i}{1+i}$ のとき、$z$，$\overline{z}$，$|z|$，$z+\overline{z}$，$z\overline{z}$ を求めよ。",
  "exa": r"$z=3-i$，$\overline z=3+i$，$|z|=\sqrt{10}$，$z+\overline z=6$，$z\overline z=10$"},
 {"lv": 2, "title": "共役複素数の利用（実数となる条件）",
  "q": r"虚数 $z$ について、$z+\dfrac1z$ が実数であるとき、$|z|=1$ であることを示せ。",
  "hint": r"「$w$ が実数 $\iff\overline{w}=w$」を用いて、$z$ と $\overline{z}$ の関係式をつくる。$z$ が虚数であることは $z\neq\overline{z}$ として使う。",
  "sol": r"$z+\dfrac1z$ が実数であるから　$\overline{\left(z+\dfrac1z\right)}=z+\dfrac1z$　すなわち　$\overline{z}+\dfrac1{\overline{z}}=z+\dfrac1z$<br>"
         r"よって　$(z-\overline{z})+\left(\dfrac1z-\dfrac1{\overline{z}}\right)=0$<br>"
         r"$\dfrac1z-\dfrac1{\overline z}=\dfrac{\overline z-z}{z\overline z}$ であるから　$(z-\overline z)\left(1-\dfrac1{z\overline z}\right)=0$<br>"
         r"$z$ は虚数であるから $z\neq\overline z$。ゆえに $z\overline z=1$，すなわち $|z|^2=1$ で、$|z|>0$ より $\boldsymbol{|z|=1}$ である。",
  "note": r"逆に $|z|=1$ ならば $\dfrac1z=\overline z$ より $z+\dfrac1z=z+\overline z$ は実数となる。<br>"
          r"別解：$z=a+bi$（$a,\ b$ は実数，$b\neq0$）とおくと、$z+\dfrac1z$ の虚部は $b-\dfrac{b}{a^2+b^2}$ である。これが $0$ であることと $b\neq0$ から $a^2+b^2=1$。",
  "ex": r"虚数 $z$ について、$z+\dfrac4z$ が実数であるとき、$|z|$ を求めよ。",
  "exa": r"$|z|=2$"},
 {"lv": 2, "title": r"$|z|^2=z\overline{z}$ を用いる計算",
  "q": r"複素数 $\alpha,\ \beta$ が $|\alpha|=2$，$|\beta|=3$，$|\alpha-\beta|=4$ を満たすとき、次の値を求めよ。<br>(1) $\alpha\overline{\beta}+\overline{\alpha}\beta$　(2) $|\alpha+\beta|$　(3) $|2\alpha+\beta|$",
  "hint": r"絶対値は2乗して $|z|^2=z\overline z$ により展開する。$\alpha\overline\beta+\overline\alpha\beta$ がひとかたまりで現れるので、これを先に求める。",
  "sol": r"(1) $|\alpha-\beta|^2=(\alpha-\beta)(\overline\alpha-\overline\beta)=|\alpha|^2-(\alpha\overline\beta+\overline\alpha\beta)+|\beta|^2$<br>"
         r"　よって $16=4-(\alpha\overline\beta+\overline\alpha\beta)+9$ より　$\alpha\overline\beta+\overline\alpha\beta=\boldsymbol{-3}$<br>"
         r"(2) $|\alpha+\beta|^2=|\alpha|^2+(\alpha\overline\beta+\overline\alpha\beta)+|\beta|^2=4-3+9=10$　よって　$|\alpha+\beta|=\boldsymbol{\sqrt{10}}$<br>"
         r"(3) $|2\alpha+\beta|^2=(2\alpha+\beta)(2\overline\alpha+\overline\beta)=4|\alpha|^2+2(\alpha\overline\beta+\overline\alpha\beta)+|\beta|^2=16-6+9=19$<br>"
         r"　よって　$|2\alpha+\beta|=\boldsymbol{\sqrt{19}}$",
  "note": r"(1)，(2) の式から $|\alpha+\beta|^2+|\alpha-\beta|^2=2(|\alpha|^2+|\beta|^2)$ が成り立つ（平行四辺形の対角線についての中線定理）。$\alpha\overline\beta+\overline\alpha\beta$ は $\alpha\overline\beta$ の実部の2倍で、$\alpha,\ \beta$ に対応するベクトル $\vec{a},\ \vec{b}$ の内積 $\vec{a}\cdot\vec{b}$ の2倍にあたる。",
  "ex": r"複素数 $\alpha,\ \beta$ が $|\alpha|=1$，$|\beta|=2$，$|\alpha+\beta|=2$ を満たすとき、$|\alpha-\beta|$，$|2\alpha-\beta|$ の値を求めよ。",
  "exa": r"$|\alpha-\beta|=\sqrt6$，$|2\alpha-\beta|=\sqrt{10}$"},
 {"lv": 3, "title": r"絶対値が 1 の複素数（$\overline{\alpha}=\dfrac1\alpha$ の利用）",
  "q": r"複素数 $\alpha,\ \beta,\ \gamma$ が $|\alpha|=|\beta|=|\gamma|=1$ を満たすとき、$w=\dfrac{(\alpha+\beta)(\beta+\gamma)(\gamma+\alpha)}{\alpha\beta\gamma}$ は実数であることを示せ。",
  "hint": r"$|\alpha|=1\iff\alpha\overline\alpha=1\iff\overline\alpha=\dfrac1\alpha$。共役をとると $\alpha,\ \beta,\ \gamma$ がそれぞれの逆数に置き換わるので、$\overline w=w$ を示せばよい。",
  "sol": r"$|\alpha|=1$ より $\alpha\overline\alpha=1$，すなわち $\overline\alpha=\dfrac1\alpha$。同様に $\overline\beta=\dfrac1\beta$，$\overline\gamma=\dfrac1\gamma$。よって<br>"
         r"$\overline{w}=\dfrac{(\overline\alpha+\overline\beta)(\overline\beta+\overline\gamma)(\overline\gamma+\overline\alpha)}{\overline\alpha\,\overline\beta\,\overline\gamma}=\left(\dfrac1\alpha+\dfrac1\beta\right)\left(\dfrac1\beta+\dfrac1\gamma\right)\left(\dfrac1\gamma+\dfrac1\alpha\right)\alpha\beta\gamma$<br>"
         r"$\phantom{\overline{w}}=\dfrac{\alpha+\beta}{\alpha\beta}\cdot\dfrac{\beta+\gamma}{\beta\gamma}\cdot\dfrac{\gamma+\alpha}{\gamma\alpha}\cdot\alpha\beta\gamma=\dfrac{(\alpha+\beta)(\beta+\gamma)(\gamma+\alpha)}{\alpha\beta\gamma}=w$<br>"
         r"$\overline w=w$ であるから、$w$ は実数である。",
  "note": r"同じ考え方で、$|\alpha|=|\beta|=1$，$\alpha\neq\beta$ のとき $\dfrac{\alpha+\beta}{\alpha-\beta}$ は純虚数または $0$ であることも示せる（共役をとると $-1$ 倍になる）。図形的には、単位円上の2点 $\alpha,\ \beta$ と $0,\ \alpha+\beta$ がひし形をつくり、その対角線が直交することを表している。",
  "ex": r"$|\alpha|=|\beta|=1$，$\alpha\beta\neq-1$ のとき、$\dfrac{\alpha+\beta}{1+\alpha\beta}$ は実数であることを示せ。",
  "exa": r"共役をとると $\dfrac{\frac1\alpha+\frac1\beta}{1+\frac1{\alpha\beta}}=\dfrac{\alpha+\beta}{\alpha\beta+1}$ となり、もとの式に等しい。"},
]})


def cl(a, b, e=1e-9):
    return abs(complex(a) - complex(b)) < e


def Z(e):
    return simplify(expand(e)) == 0


def runit():
    return cmath.exp(1j * random.uniform(0, 2 * math.pi))


def _v1():
    A, B = 2 + 3j, -4 + 1j
    assert cl(abs(B - A), 2 * math.sqrt(10)) and cl((2 * A + B) / 3, 7j / 3) and cl((-A + 2 * B) / (2 - 1), -10 - 1j)
    A, B = 1 - 2j, 5 + 4j
    assert cl(abs(B - A), 2 * math.sqrt(13)) and cl((A + 3 * B) / 4, 4 + 2.5j) and cl((-3 * A + B) / (1 - 3), -1 - 5j)
    z = (1 + 3 * I) / (2 - I)
    assert simplify(z - (-1 + 7 * I) / 5) == 0 and simplify(Abs(z) - sqrt(2)) == 0
    assert simplify(z + conjugate(z) + Rational(2, 5)) == 0 and simplify(z * conjugate(z) - 2) == 0
    assert expand(5 * z**2 + 2 * z + 10) == 0
    z = (4 + 2 * I) / (1 + I)
    assert simplify(z - (3 - I)) == 0
    # 虚数 z で z+4/z が実数 ⇔ |z|=2
    a, b = symbols("a b", real=True)
    z = a + b * I
    assert simplify(sim(z + 4 / z) - b * (a**2 + b**2 - 4) / (a**2 + b**2)) == 0
    assert simplify(sim(z + 1 / z) - b * (a**2 + b**2 - 1) / (a**2 + b**2)) == 0
    for _ in range(100):
        u = runit()
        assert abs((u + 1 / u).imag) < 1e-12 and abs((2 * u + 4 / (2 * u)).imag) < 1e-12
    # |α|=2,|β|=3,|α-β|=4 の具体例：α=2, β=3e^{iθ}, cosθ=-1/4
    th = math.acos(-0.25)
    al, be = 2, 3 * cmath.exp(1j * th)
    assert cl(abs(al - be), 4) and cl(al * be.conjugate() + al * be, -3)
    assert cl(abs(al + be), math.sqrt(10)) and cl(abs(2 * al + be), math.sqrt(19))
    al, be = 1, 2 * cmath.exp(1j * th)
    assert cl(abs(al + be), 2) and cl(abs(al - be), math.sqrt(6)) and cl(abs(2 * al - be), math.sqrt(10))
    for _ in range(200):
        al, be, ga = runit(), runit(), runit()
        w = (al + be) * (be + ga) * (ga + al) / (al * be * ga)
        assert abs(w.imag) < 1e-9
        assert abs(((al + be) / (1 + al * be)).imag) < 1e-7
        assert abs(((al + be) / (al - be)).real) < 1e-7


# ---------------------------------------------------------------- 節2
SEC.append({"title": "極形式と積・商",
"base": r"""・$z\neq0$ を $z=r(\cos\theta+i\sin\theta)$（$r=|z|>0$）と表すことを<b>極形式</b>といい、$\theta$ を<b>偏角</b> $\arg z$ という（$2\pi$ の整数倍の違いを除いて定まる）。<br>
・$z_1=r_1(\cos\theta_1+i\sin\theta_1)$，$z_2=r_2(\cos\theta_2+i\sin\theta_2)$ のとき<br>
　$z_1z_2=r_1r_2\{\cos(\theta_1+\theta_2)+i\sin(\theta_1+\theta_2)\}$，　$\dfrac{z_1}{z_2}=\dfrac{r_1}{r_2}\{\cos(\theta_1-\theta_2)+i\sin(\theta_1-\theta_2)\}$<br>
・すなわち　$|z_1z_2|=|z_1||z_2|$，$\arg z_1z_2=\arg z_1+\arg z_2$，$\arg\dfrac{z_1}{z_2}=\arg z_1-\arg z_2$<br>
・$\overline{z}=r\{\cos(-\theta)+i\sin(-\theta)\}$，$\dfrac1z=\dfrac1r\{\cos(-\theta)+i\sin(-\theta)\}$""",
"items": [
 {"lv": 1, "title": "極形式で表す",
  "q": r"次の複素数を極形式で表せ。ただし、偏角 $\theta$ は $0\leqq\theta<2\pi$ とする。<br>(1) $-1+\sqrt3\,i$　(2) $-2-2i$　(3) $-3i$",
  "hint": r"まず絶対値 $r$ を求め、$\cos\theta=\dfrac{a}{r}$，$\sin\theta=\dfrac{b}{r}$ となる $\theta$ を探す。点の位置（どの象限か）を図で確認するとよい。",
  "sol": r"(1) $r=\sqrt{1+3}=2$，$\cos\theta=-\dfrac12$，$\sin\theta=\dfrac{\sqrt3}2$ より $\theta=\dfrac23\pi$。　$\boldsymbol{2\left(\cos\dfrac23\pi+i\sin\dfrac23\pi\right)}$<br>"
         r"(2) $r=2\sqrt2$，$\cos\theta=\sin\theta=-\dfrac1{\sqrt2}$ より $\theta=\dfrac54\pi$。　$\boldsymbol{2\sqrt2\left(\cos\dfrac54\pi+i\sin\dfrac54\pi\right)}$<br>"
         r"(3) $r=3$，$\cos\theta=0$，$\sin\theta=-1$ より $\theta=\dfrac32\pi$。　$\boldsymbol{3\left(\cos\dfrac32\pi+i\sin\dfrac32\pi\right)}$",
  "note": r"極形式では $r>0$ であり、$\cos$ と $\sin$ の角が同じで、間の符号が $+$ でなければならない。たとえば $-2(\cos\theta+i\sin\theta)$ や $2(\cos\theta-i\sin\theta)$ は極形式ではなく、それぞれ $2\{\cos(\theta+\pi)+i\sin(\theta+\pi)\}$，$2\{\cos(-\theta)+i\sin(-\theta)\}$ と直す。",
  "ex": r"次の複素数を極形式で表せ（$0\leqq\theta<2\pi$）。(1) $\sqrt3-i$　(2) $-5$　(3) $\dfrac{1-i}{\sqrt2}$",
  "exa": r"(1) $2\left(\cos\dfrac{11}6\pi+i\sin\dfrac{11}6\pi\right)$　(2) $5(\cos\pi+i\sin\pi)$　(3) $\cos\dfrac74\pi+i\sin\dfrac74\pi$"},
 {"lv": 2, "title": "積・商の極形式と三角関数の値",
  "q": r"$\alpha=1+i$，$\beta=\sqrt3+i$ とする。<br>(1) $\alpha$，$\beta$，$\alpha\beta$ を極形式で表せ。<br>(2) (1) を利用して、$\cos\dfrac5{12}\pi$，$\sin\dfrac5{12}\pi$ の値を求めよ。",
  "hint": r"積の絶対値は絶対値の積、積の偏角は偏角の和。一方で $\alpha\beta$ を直接展開し、実部と虚部を比べる。",
  "sol": r"(1) $\boldsymbol{\alpha=\sqrt2\left(\cos\dfrac\pi4+i\sin\dfrac\pi4\right)}$，$\boldsymbol{\beta=2\left(\cos\dfrac\pi6+i\sin\dfrac\pi6\right)}$ より<br>"
         r"　$\alpha\beta=\boldsymbol{2\sqrt2\left(\cos\dfrac5{12}\pi+i\sin\dfrac5{12}\pi\right)}$<br>"
         r"(2) 一方、$\alpha\beta=(1+i)(\sqrt3+i)=(\sqrt3-1)+(\sqrt3+1)i$。(1) と実部・虚部を比べて<br>"
         r"　$2\sqrt2\cos\dfrac5{12}\pi=\sqrt3-1$，　$2\sqrt2\sin\dfrac5{12}\pi=\sqrt3+1$<br>"
         r"よって　$\cos\dfrac5{12}\pi=\dfrac{\sqrt3-1}{2\sqrt2}=\boldsymbol{\dfrac{\sqrt6-\sqrt2}4}$，　$\sin\dfrac5{12}\pi=\boldsymbol{\dfrac{\sqrt6+\sqrt2}4}$",
  "note": r"「積の偏角は偏角の和」という性質は、三角関数の加法定理そのものである。実際、$(\cos\theta_1+i\sin\theta_1)(\cos\theta_2+i\sin\theta_2)$ を展開して実部・虚部を比べると、$\cos(\theta_1+\theta_2)$，$\sin(\theta_1+\theta_2)$ の加法定理が得られる。",
  "ex": r"例題と同じ $\alpha,\ \beta$ について、$\dfrac\alpha\beta$ を利用して $\cos\dfrac\pi{12}$，$\sin\dfrac\pi{12}$ の値を求めよ。",
  "exa": r"$\cos\dfrac\pi{12}=\dfrac{\sqrt6+\sqrt2}4$，$\sin\dfrac\pi{12}=\dfrac{\sqrt6-\sqrt2}4$"},
 {"lv": 3, "title": "三角関数を含む式の極形式（半角の公式）",
  "q": r"$z=1+\cos\theta+i\sin\theta$ を極形式で表せ。ただし、(1) $0<\theta<\pi$　(2) $\pi<\theta<2\pi$ のそれぞれの場合について答えよ。",
  "hint": r"半角の公式 $1+\cos\theta=2\cos^2\dfrac\theta2$，$\sin\theta=2\sin\dfrac\theta2\cos\dfrac\theta2$ で $2\cos\dfrac\theta2$ をくくり出す。極形式では絶対値が正でなければならないので、$\cos\dfrac\theta2$ の符号で場合分けする。",
  "sol": r"$z=2\cos^2\dfrac\theta2+2i\sin\dfrac\theta2\cos\dfrac\theta2=2\cos\dfrac\theta2\left(\cos\dfrac\theta2+i\sin\dfrac\theta2\right)$ …①<br>"
         r"(1) $0<\dfrac\theta2<\dfrac\pi2$ より $\cos\dfrac\theta2>0$ であるから、① がそのまま極形式である。<br>"
         r"　$\boldsymbol{z=2\cos\dfrac\theta2\left(\cos\dfrac\theta2+i\sin\dfrac\theta2\right)}$<br>"
         r"(2) $\dfrac\pi2<\dfrac\theta2<\pi$ より $\cos\dfrac\theta2<0$ であるから、① を $z=-2\cos\dfrac\theta2\left(-\cos\dfrac\theta2-i\sin\dfrac\theta2\right)$ と書き直す。<br>"
         r"　$-\cos\dfrac\theta2=\cos\left(\dfrac\theta2+\pi\right)$，$-\sin\dfrac\theta2=\sin\left(\dfrac\theta2+\pi\right)$，$-2\cos\dfrac\theta2>0$ より<br>"
         r"　$\boldsymbol{z=-2\cos\dfrac\theta2\left\{\cos\left(\dfrac\theta2+\pi\right)+i\sin\left(\dfrac\theta2+\pi\right)\right\}}$",
  "note": r"図形的には、4点 $0,\ 1,\ z,\ \cos\theta+i\sin\theta$ がひし形の頂点となり、対角線が角を2等分するので、偏角が $\dfrac\theta2$（(2) では $\dfrac\theta2+\pi$）になる。$|z|=2\left|\cos\dfrac\theta2\right|$ もこの図から分かる。",
  "ex": r"$0<\theta<\pi$ のとき、$z=1-\cos\theta+i\sin\theta$ を極形式で表せ。",
  "exa": r"$z=2\sin\dfrac\theta2\left\{\cos\left(\dfrac\pi2-\dfrac\theta2\right)+i\sin\left(\dfrac\pi2-\dfrac\theta2\right)\right\}$"},
 {"lv": 3, "title": "偏角の和（複素数の積で角の和を求める）",
  "q": r"$\tan\alpha=\dfrac12$，$\tan\beta=\dfrac13$，$0<\alpha<\dfrac\pi2$，$0<\beta<\dfrac\pi2$ のとき、$\alpha+\beta$ の値を、複素数の積を利用して求めよ。",
  "hint": r"偏角が $\alpha$ である複素数として $2+i$，偏角が $\beta$ である複素数として $3+i$ がとれる。積の偏角は偏角の和になる。",
  "sol": r"$0<\alpha<\dfrac\pi2$，$\tan\alpha=\dfrac12$ より $\cos\alpha=\dfrac2{\sqrt5}$，$\sin\alpha=\dfrac1{\sqrt5}$ であるから　$2+i=\sqrt5(\cos\alpha+i\sin\alpha)$<br>"
         r"同様に　$3+i=\sqrt{10}(\cos\beta+i\sin\beta)$。よって<br>"
         r"　$(2+i)(3+i)=5\sqrt2\{\cos(\alpha+\beta)+i\sin(\alpha+\beta)\}$<br>"
         r"一方、$(2+i)(3+i)=5+5i=5\sqrt2\left(\cos\dfrac\pi4+i\sin\dfrac\pi4\right)$ であるから　$\alpha+\beta=\dfrac\pi4+2n\pi$（$n$ は整数）<br>"
         r"$0<\alpha+\beta<\pi$ より　$\boldsymbol{\alpha+\beta=\dfrac\pi4}$",
  "note": r"加法定理 $\tan(\alpha+\beta)=\dfrac{\frac12+\frac13}{1-\frac12\cdot\frac13}=1$ からも求まるが、角が3つ以上になると複素数の積のほうが見通しがよい（練習）。有名な例として、$\tan\alpha=\dfrac15$，$\tan\beta=\dfrac1{239}$（$\alpha,\ \beta$ は鋭角）のとき、$(5+i)^4(239-i)=114244(1+i)$ と偏角の範囲から $4\alpha-\beta=\dfrac\pi4$（マチンの公式）が得られる。",
  "ex": r"$\tan\alpha=\dfrac12$，$\tan\beta=\dfrac15$，$\tan\gamma=\dfrac18$ で、$\alpha,\ \beta,\ \gamma$ がいずれも $0$ と $\dfrac\pi2$ の間にあるとき、$\alpha+\beta+\gamma$ の値を求めよ。",
  "exa": r"$(2+i)(5+i)(8+i)=65+65i$ より　$\alpha+\beta+\gamma=\dfrac\pi4$"},
]})


def _arg(z):
    return cmath.phase(z) % (2 * math.pi)


def _v2():
    for z, r, t in [(-1 + 3**0.5 * 1j, 2, 2 * math.pi / 3), (-2 - 2j, 2 * 2**0.5, 5 * math.pi / 4), (-3j, 3, 3 * math.pi / 2),
                    (3**0.5 - 1j, 2, 11 * math.pi / 6), (-5, 5, math.pi), ((1 - 1j) / 2**0.5, 1, 7 * math.pi / 4)]:
        assert cl(abs(z), r) and abs(_arg(z) - t) < 1e-9
    assert Z(expand((1 + I) * (sqrt(3) + I)) - ((sqrt(3) - 1) + (sqrt(3) + 1) * I))
    assert simplify(cos(5 * pi / 12) - (sqrt(6) - sqrt(2)) / 4) == 0 and simplify(sin(5 * pi / 12) - (sqrt(6) + sqrt(2)) / 4) == 0
    assert simplify(expand((1 + I) * (sqrt(3) - I) / 4) - ((sqrt(3) + 1) + (sqrt(3) - 1) * I) / 4) == 0
    assert simplify(cos(pi / 12) - (sqrt(6) + sqrt(2)) / 4) == 0 and simplify(sin(pi / 12) - (sqrt(6) - sqrt(2)) / 4) == 0
    assert cl((1 + 1j) * (3**0.5 + 1j), 2 * 2**0.5 * cmath.exp(5j * math.pi / 12))
    for k in range(1, 400):
        th = math.pi * k / 400
        z = 1 + math.cos(th) + 1j * math.sin(th)
        r = 2 * math.cos(th / 2); assert r > 0 and cl(z, r * cmath.exp(1j * th / 2))
        z2 = 1 - math.cos(th) + 1j * math.sin(th)
        r = 2 * math.sin(th / 2); assert r > 0 and cl(z2, r * cmath.exp(1j * (math.pi / 2 - th / 2)))
        th = math.pi + th
        z = 1 + math.cos(th) + 1j * math.sin(th)
        r = -2 * math.cos(th / 2); assert r > 0 and cl(z, r * cmath.exp(1j * (th / 2 + math.pi)))
    assert (2 + 1j) * (3 + 1j) == 5 + 5j and (2 + 1j) * (5 + 1j) * (8 + 1j) == 65 + 65j
    assert abs(math.atan(1 / 2) + math.atan(1 / 3) - math.pi / 4) < 1e-12
    assert abs(math.atan(1 / 2) + math.atan(1 / 5) + math.atan(1 / 8) - math.pi / 4) < 1e-12
    assert Z((5 + I)**4 * (239 - I) - 114244 * (1 + I))
    assert abs(4 * math.atan(1 / 5) - math.atan(1 / 239) - math.pi / 4) < 1e-12


# ---------------------------------------------------------------- 節3
SEC.append({"title": "ド・モアブルの定理",
"base": r"""・<b>ド・モアブルの定理</b>：整数 $n$ に対して　$(\cos\theta+i\sin\theta)^n=\cos n\theta+i\sin n\theta$<br>
・$z=r(\cos\theta+i\sin\theta)$ ならば　$z^n=r^n(\cos n\theta+i\sin n\theta)$（$n$ は整数）<br>
・$z=\cos\theta+i\sin\theta$ のとき　$z^n+\dfrac1{z^n}=2\cos n\theta$，$z^n-\dfrac1{z^n}=2i\sin n\theta$<br>
・二項定理と組み合わせると、$\cos n\theta$，$\sin n\theta$ を $\cos\theta$，$\sin\theta$ で表す公式や、三角関数を含む和が求められる""",
"items": [
 {"lv": 1, "title": "ド・モアブルの定理による累乗の計算",
  "q": r"次の式を計算せよ。<br>(1) $(1+\sqrt3\,i)^6$　(2) $(1-i)^{10}$　(3) $\left(\dfrac{1+i}{\sqrt3-i}\right)^{12}$",
  "hint": r"極形式に直してからド・モアブルの定理を使う。(3) は分数のまま展開せず、商の極形式（絶対値は商、偏角は差）を先に求める。",
  "sol": r"(1) $1+\sqrt3\,i=2\left(\cos\dfrac\pi3+i\sin\dfrac\pi3\right)$ より　$(1+\sqrt3\,i)^6=2^6(\cos2\pi+i\sin2\pi)=\boldsymbol{64}$<br>"
         r"(2) $1-i=\sqrt2\left\{\cos\left(-\dfrac\pi4\right)+i\sin\left(-\dfrac\pi4\right)\right\}$ より<br>"
         r"　$(1-i)^{10}=(\sqrt2)^{10}\left\{\cos\left(-\dfrac52\pi\right)+i\sin\left(-\dfrac52\pi\right)\right\}=32(0-i)=\boldsymbol{-32i}$<br>"
         r"(3) $1+i=\sqrt2\left(\cos\dfrac\pi4+i\sin\dfrac\pi4\right)$，$\sqrt3-i=2\left\{\cos\left(-\dfrac\pi6\right)+i\sin\left(-\dfrac\pi6\right)\right\}$ より<br>"
         r"　$\dfrac{1+i}{\sqrt3-i}=\dfrac1{\sqrt2}\left(\cos\dfrac5{12}\pi+i\sin\dfrac5{12}\pi\right)$<br>"
         r"　よって　$\left(\dfrac{1+i}{\sqrt3-i}\right)^{12}=\left(\dfrac1{\sqrt2}\right)^{12}(\cos5\pi+i\sin5\pi)=\boldsymbol{-\dfrac1{64}}$",
  "note": r"(2) は $(1-i)^2=-2i$ を使って $(1-i)^{10}=(-2i)^5=-32i^5=-32i$ としてもよい。指数が大きいときや分数式のときは、極形式に直すのが確実である。",
  "ex": r"次の式を計算せよ。(1) $(\sqrt3+i)^7$　(2) $\dfrac1{(1+i)^8}$　(3) $\left(\dfrac{\sqrt3+i}{1-i}\right)^6$",
  "exa": r"(1) $-64\sqrt3-64i$　(2) $\dfrac1{16}$　(3) $8i$"},
 {"lv": 2, "title": r"$z^n$ が実数・純虚数となる自然数 $n$",
  "q": r"$z=\dfrac{1+\sqrt3\,i}{1+i}$ とする。<br>(1) $z^n$ が実数となる最小の自然数 $n$ と、そのときの $z^n$ の値を求めよ。<br>(2) $z^n$ が純虚数となる最小の自然数 $n$ と、そのときの $z^n$ の値を求めよ。",
  "hint": r"$z$ を極形式で表すと $z^n=r^n(\cos n\theta+i\sin n\theta)$。実数 $\iff\sin n\theta=0$，純虚数 $\iff\cos n\theta=0$。",
  "sol": r"$z=\dfrac{2\left(\cos\frac\pi3+i\sin\frac\pi3\right)}{\sqrt2\left(\cos\frac\pi4+i\sin\frac\pi4\right)}=\sqrt2\left(\cos\dfrac\pi{12}+i\sin\dfrac\pi{12}\right)$ より　$z^n=(\sqrt2)^n\left(\cos\dfrac{n\pi}{12}+i\sin\dfrac{n\pi}{12}\right)$<br>"
         r"(1) $z^n$ が実数 $\iff\sin\dfrac{n\pi}{12}=0\iff\dfrac{n\pi}{12}=k\pi$（$k$ は整数）$\iff n=12k$<br>"
         r"　最小の自然数は $\boldsymbol{n=12}$ で、$z^{12}=(\sqrt2)^{12}(\cos\pi+i\sin\pi)=\boldsymbol{-64}$<br>"
         r"(2) $z^n$ が純虚数 $\iff\cos\dfrac{n\pi}{12}=0\iff\dfrac{n\pi}{12}=\dfrac\pi2+k\pi\iff n=6+12k$（$k$ は整数）<br>"
         r"　最小の自然数は $\boldsymbol{n=6}$ で、$z^6=(\sqrt2)^6\left(\cos\dfrac\pi2+i\sin\dfrac\pi2\right)=\boldsymbol{8i}$",
  "note": r"純虚数は「実部が $0$ で、虚部が $0$ でない数」である。$z\neq0$ ならば $z^n\neq0$ なので、$\cos n\theta=0$ だけを調べればよい。",
  "ex": r"$z=\dfrac{-1+i}{\sqrt3+i}$ について、$z^n$ が実数となる最小の自然数 $n$ と、純虚数となる最小の自然数 $n$ を求め、それぞれのときの $z^n$ の値を求めよ。",
  "exa": r"実数：$n=12$，$z^{12}=-\dfrac1{64}$　　純虚数：$n=6$，$z^6=-\dfrac i8$"},
 {"lv": 3, "title": r"$z+\dfrac1z$ の値から $z^n+\dfrac1{z^n}$ を求める",
  "q": r"複素数 $z$ が $z+\dfrac1z=\sqrt3$ を満たすとき、$z^{10}+\dfrac1{z^{10}}$ の値を求めよ。",
  "hint": r"分母を払うと $z^2-\sqrt3z+1=0$。解くと $|z|=1$ の虚数になるので、$z=\cos\theta+i\sin\theta$ とおけば $z^n+\dfrac1{z^n}=2\cos n\theta$ となる。",
  "sol": r"$z\neq0$ であり、分母を払うと $z^2-\sqrt3z+1=0$。よって<br>"
         r"　$z=\dfrac{\sqrt3\pm i}2=\cos\left(\pm\dfrac\pi6\right)+i\sin\left(\pm\dfrac\pi6\right)$（複号同順）<br>"
         r"$z=\cos\theta+i\sin\theta$ のとき、ド・モアブルの定理より $\dfrac1{z^{10}}=z^{-10}=\cos(-10\theta)+i\sin(-10\theta)$ であるから<br>"
         r"　$z^{10}+\dfrac1{z^{10}}=2\cos10\theta$<br>"
         r"$\theta=\pm\dfrac\pi6$ のどちらでも　$z^{10}+\dfrac1{z^{10}}=2\cos\left(\pm\dfrac53\pi\right)=2\cdot\dfrac12=\boldsymbol{1}$",
  "note": r"$a_n=z^n+\dfrac1{z^n}$ とおくと、$a_n$ に $z+\dfrac1z$ を掛けることにより $a_{n+1}=\sqrt3a_n-a_{n-1}$ が成り立つので、漸化式で順に求めることもできる。$z^{12}=1$ であるから、$a_n$ は周期 $12$ をもつ。",
  "ex": r"複素数 $z$ が $z+\dfrac1z=\sqrt2$ を満たすとき、$z^{20}+\dfrac1{z^{20}}$ の値を求めよ。",
  "exa": r"$-2$"},
 {"lv": 3, "title": r"ド・モアブルの定理と $n$ 倍角の公式",
  "q": r"(1) ド・モアブルの定理を用いて、$\cos5\theta$ を $\cos\theta$ の式で表せ。<br>(2) $\cos^2\dfrac\pi{10}$ の値を求めよ。",
  "hint": r"$(\cos\theta+i\sin\theta)^5$ を二項定理で展開した式の実部が $\cos5\theta$。(2) は $\theta=\dfrac\pi{10}$ のとき $\cos5\theta=0$ となることを使い、出てくる2次方程式の2解のどちらかを大小で決める。",
  "sol": r"(1) $c=\cos\theta$，$s=\sin\theta$ とおく。ド・モアブルの定理と二項定理により<br>"
         r"　$\cos5\theta+i\sin5\theta=(c+is)^5=\displaystyle\sum_{k=0}^5{}_5\mathrm{C}_kc^{5-k}(is)^k$<br>"
         r"実部を比べて　$\cos5\theta=c^5-10c^3s^2+5cs^4$<br>"
         r"$s^2=1-c^2$ を代入して　$\cos5\theta=c^5-10c^3(1-c^2)+5c(1-c^2)^2=\boldsymbol{16\cos^5\theta-20\cos^3\theta+5\cos\theta}$<br>"
         r"(2) $\theta=\dfrac\pi{10}$ のとき $\cos5\theta=\cos\dfrac\pi2=0$ であるから、$c=\cos\dfrac\pi{10}$ は $16c^5-20c^3+5c=0$ を満たす。$c\neq0$ より<br>"
         r"　$16c^4-20c^2+5=0$　　よって　$c^2=\dfrac{10\pm\sqrt{100-80}}{16}=\dfrac{5\pm\sqrt5}8$<br>"
         r"$0<\dfrac\pi{10}<\dfrac\pi4$ より $c^2>\cos^2\dfrac\pi4=\dfrac12$ であり、$\dfrac{5-\sqrt5}8<\dfrac12<\dfrac{5+\sqrt5}8$ であるから<br>"
         r"　$\cos^2\dfrac\pi{10}=\boldsymbol{\dfrac{5+\sqrt5}8}$",
  "note": r"虚部を比べると $\sin5\theta=\sin\theta\,(16\cos^4\theta-12\cos^2\theta+1)$ も得られる。もう一方の解 $\dfrac{5-\sqrt5}8$ は $\cos^2\dfrac{3}{10}\pi$ である（$\theta=\dfrac3{10}\pi$ のときも $\cos5\theta=0$）。",
  "ex": r"(1) ド・モアブルの定理を用いて、$\cos4\theta$ を $\cos\theta$ の式で表せ。(2) $\cos^2\dfrac\pi8$ の値を求めよ。",
  "exa": r"(1) $8\cos^4\theta-8\cos^2\theta+1$　(2) $\dfrac{2+\sqrt2}4$"},
 {"lv": 4, "title": "二項係数と三角関数の和（実部・虚部の利用）",
  "q": r"$n$ を自然数とするとき、次の和を $n$ の式で表せ。<br>$\displaystyle S=\sum_{k=0}^{n}{}_n\mathrm{C}_k\cos\frac{k\pi}3$，　$\displaystyle T=\sum_{k=0}^{n}{}_n\mathrm{C}_k\sin\frac{k\pi}3$",
  "hint": r"$S$ と $T$ を組にした $S+iT$ を考える。$\omega=\cos\dfrac\pi3+i\sin\dfrac\pi3$ とおくと、ド・モアブルの定理により $\cos\dfrac{k\pi}3+i\sin\dfrac{k\pi}3=\omega^k$ となり、二項定理が使える。",
  "sol": r"$\omega=\cos\dfrac\pi3+i\sin\dfrac\pi3$ とおくと、ド・モアブルの定理より $\omega^k=\cos\dfrac{k\pi}3+i\sin\dfrac{k\pi}3$。よって、二項定理により<br>"
         r"　$S+iT=\displaystyle\sum_{k=0}^n{}_n\mathrm{C}_k\omega^k=(1+\omega)^n$<br>"
         r"$1+\omega=\dfrac32+\dfrac{\sqrt3}2i=\sqrt3\left(\cos\dfrac\pi6+i\sin\dfrac\pi6\right)$ であるから　$(1+\omega)^n=3^{\frac n2}\left(\cos\dfrac{n\pi}6+i\sin\dfrac{n\pi}6\right)$<br>"
         r"$S,\ T$ は実数であるから、実部・虚部を比べて<br>"
         r"　$\boldsymbol{S=3^{\frac n2}\cos\dfrac{n\pi}6}$，　$\boldsymbol{T=3^{\frac n2}\sin\dfrac{n\pi}6}$",
  "note": r"同様に、半角の公式による変形 $1+\cos\theta+i\sin\theta=2\cos\dfrac\theta2\left(\cos\dfrac\theta2+i\sin\dfrac\theta2\right)$ を用いると、$\displaystyle\sum_{k=0}^n{}_n\mathrm{C}_k\cos k\theta=\left(2\cos\dfrac\theta2\right)^n\cos\dfrac{n\theta}2$ が得られる。和を「ある複素数の実部」とみる発想は、$\displaystyle\sum_{k=1}^n\cos k\theta$ を等比数列の和として求めるときにも使う。",
  "ex": r"$n$ を自然数とするとき、${}_n\mathrm{C}_0-{}_n\mathrm{C}_2+{}_n\mathrm{C}_4-{}_n\mathrm{C}_6+\cdots$ $\left(=\displaystyle\sum_{k=0}^n{}_n\mathrm{C}_k\cos\dfrac{k\pi}2\right)$ を $n$ の式で表せ。",
  "exa": r"$2^{\frac n2}\cos\dfrac{n\pi}4$"},
]})


def _v3():
    assert Z((1 + sqrt(3) * I)**6 - 64) and Z((1 - I)**10 + 32 * I)
    assert Z(((1 + I) / (sqrt(3) - I))**12 + Rational(1, 64))
    assert Z((sqrt(3) + I)**7 - (-64 * sqrt(3) - 64 * I)) and Z(1 / (1 + I)**8 - Rational(1, 16))
    assert Z(((sqrt(3) + I) / (1 - I))**6 - 8 * I)
    assert Z((1 - I)**2 + 2 * I)

    def first(z, real):
        for n in range(1, 100):
            w = z**n
            if (abs(w.imag) if real else abs(w.real)) < 1e-9 * abs(w):
                return n, w
    z = (1 + 3**0.5 * 1j) / (1 + 1j)
    n, w = first(z, True); assert n == 12 and cl(w, -64, 1e-7)
    n, w = first(z, False); assert n == 6 and cl(w, 8j, 1e-8)
    z = (-1 + 1j) / (3**0.5 + 1j)
    n, w = first(z, True); assert n == 12 and cl(w, -1 / 64)
    n, w = first(z, False); assert n == 6 and cl(w, -1j / 8)
    for z in [(3**0.5 + 1j) / 2, (3**0.5 - 1j) / 2]:
        assert cl(z + 1 / z, 3**0.5) and cl(z**10 + z**-10, 1) and cl(z**12, 1)
    for z in [(1 + 1j) / 2**0.5, (1 - 1j) / 2**0.5]:
        assert cl(z + 1 / z, 2**0.5) and cl(z**20 + z**-20, -2)
    for _ in range(50):
        t = random.uniform(-3, 3); c = math.cos(t)
        assert abs(math.cos(5 * t) - (16 * c**5 - 20 * c**3 + 5 * c)) < 1e-12
        assert abs(math.sin(5 * t) - math.sin(t) * (16 * c**4 - 12 * c**2 + 1)) < 1e-12
        assert abs(math.cos(4 * t) - (8 * c**4 - 8 * c**2 + 1)) < 1e-12
        zz = complex(math.cos(t), math.sin(t))**5
        c5, s = math.cos(t), math.sin(t)
        assert abs(zz.real - (c5**5 - 10 * c5**3 * s**2 + 5 * c5 * s**4)) < 1e-12
    assert Z(cos(pi / 10)**2 - (5 + sqrt(5)) / 8) and Z(cos(3 * pi / 10)**2 - (5 - sqrt(5)) / 8)
    assert Z(cos(pi / 8)**2 - (2 + sqrt(2)) / 4)
    for n in range(1, 30):
        S = sum(math.comb(n, k) * math.cos(k * math.pi / 3) for k in range(n + 1))
        T = sum(math.comb(n, k) * math.sin(k * math.pi / 3) for k in range(n + 1))
        assert abs(S - 3**(n / 2) * math.cos(n * math.pi / 6)) < 1e-6 * 3**(n / 2)
        assert abs(T - 3**(n / 2) * math.sin(n * math.pi / 6)) < 1e-6 * 3**(n / 2)
        U = sum((-1)**(k // 2) * math.comb(n, k) for k in range(0, n + 1, 2))
        assert abs(U - 2**(n / 2) * math.cos(n * math.pi / 4)) < 1e-6
        th = random.uniform(-3, 3)
        V = sum(math.comb(n, k) * math.cos(k * th) for k in range(n + 1))
        assert abs(V - (2 * math.cos(th / 2))**n * math.cos(n * th / 2)) < 1e-6 * 2**n


# ---------------------------------------------------------------- 節4
def fig_cuberoots():
    f = Fig(-2.75, 2.75, -2.6, 2.65, 27)
    R = [2 * cmath.exp(1j * (math.pi / 6 + 2 * k * math.pi / 3)) for k in range(3)]
    f.circle(0, 2, col=GRAY, w=0.9, dash="3 2")
    f.poly(R, fill=FILL, col=BLUE, w=1.1, op=0.7)
    f.axes(-2.7, 2.7, -2.55, 2.6)
    for z in R:
        f.dot(z, col=RED)
    f.text(R[0], "√3+i", 2, -6)
    f.text(R[1], "−√3+i", -2, -6, anchor="end")
    f.text(R[2], "−2i", 6, 12)
    f.text(2, "2", 3, 12)
    return f.svg()


SEC.append({"title": r"$n$ 乗根と方程式",
"base": r"""・$z^n=\alpha$（$\alpha=r(\cos\varphi+i\sin\varphi)$，$r>0$）の解は　$z=\sqrt[n]{r}\left(\cos\dfrac{\varphi+2k\pi}n+i\sin\dfrac{\varphi+2k\pi}n\right)$（$k=0,\ 1,\ \cdots,\ n-1$）の $n$ 個。<br>
　これらは原点を中心とする半径 $\sqrt[n]{r}$ の円に内接する正 $n$ 角形の頂点である。<br>
・<b>1 の $n$ 乗根</b>：$\omega=\cos\dfrac{2\pi}n+i\sin\dfrac{2\pi}n$ とすると、$z^n=1$ の解は $1,\ \omega,\ \omega^2,\ \cdots,\ \omega^{n-1}$<br>
・$z^n-1=(z-1)(z^{n-1}+\cdots+z+1)$ より $1+\omega+\omega^2+\cdots+\omega^{n-1}=0$。また $z^n-1=(z-1)(z-\omega)\cdots(z-\omega^{n-1})$<br>
・$|\omega|=1$ より $\overline{\omega}=\dfrac1\omega=\omega^{n-1}$""",
"items": [
 {"lv": 1, "title": r"$z^n=\alpha$ の解と図示",
  "q": r"方程式 $z^3=8i$ を解け。また、解を表す点を複素数平面上に図示せよ。",
  "hint": r"$z=r(\cos\theta+i\sin\theta)$ とおき、ド・モアブルの定理で $z^3$ を表して、右辺の極形式と絶対値・偏角を比べる。偏角は $2k\pi$ の違いを含めて比べる。",
  "sol": fig_cuberoots() +
         r"$z=r(\cos\theta+i\sin\theta)$（$r>0$）とおくと、ド・モアブルの定理より $z^3=r^3(\cos3\theta+i\sin3\theta)$。<br>"
         r"また $8i=8\left(\cos\dfrac\pi2+i\sin\dfrac\pi2\right)$ であるから、絶対値と偏角を比べて<br>"
         r"　$r^3=8$，$3\theta=\dfrac\pi2+2k\pi$（$k$ は整数）<br>"
         r"$r>0$ より $r=2$。$\theta=\dfrac\pi6+\dfrac{2k\pi}3$ で、$0\leqq\theta<2\pi$ の範囲では $k=0,\ 1,\ 2$ に対して $\theta=\dfrac\pi6,\ \dfrac56\pi,\ \dfrac32\pi$。<br>"
         r"よって　$\boldsymbol{z=\sqrt3+i,\ -\sqrt3+i,\ -2i}$<br>"
         r"これらは原点を中心とする半径 $2$ の円に内接する正三角形の頂点である（右図）。",
  "note": r"偏角の比較で「$+2k\pi$」を忘れると解が1つしか得られない。$k$ を $3$ 以上にしても同じ点がくり返し現れるだけなので、$k=0,\ 1,\ 2$ で尽くされる。",
  "ex": r"方程式 $z^4=-16$ を解け。",
  "exa": r"$z=\pm\sqrt2\pm\sqrt2\,i$（複号任意）"},
 {"lv": 2, "title": r"$z^n=\alpha$ の解（$\alpha$ が虚数の場合）",
  "q": r"方程式 $z^4=-8+8\sqrt3\,i$ を解け。",
  "hint": r"右辺を極形式で表し、絶対値と偏角を比べる。$k=0,\ 1,\ 2,\ 3$ の4つの解を求める。",
  "sol": r"$-8+8\sqrt3\,i=16\left(\cos\dfrac23\pi+i\sin\dfrac23\pi\right)$。$z=r(\cos\theta+i\sin\theta)$（$r>0$）とおくと<br>"
         r"　$r^4(\cos4\theta+i\sin4\theta)=16\left(\cos\dfrac23\pi+i\sin\dfrac23\pi\right)$<br>"
         r"よって $r^4=16$，$4\theta=\dfrac23\pi+2k\pi$（$k$ は整数）であり、$r=2$，$\theta=\dfrac\pi6+\dfrac{k\pi}2$<br>"
         r"$0\leqq\theta<2\pi$ では $\theta=\dfrac\pi6,\ \dfrac23\pi,\ \dfrac76\pi,\ \dfrac53\pi$ であるから<br>"
         r"　$\boldsymbol{z=\sqrt3+i,\ -1+\sqrt3\,i,\ -\sqrt3-i,\ 1-\sqrt3\,i}$",
  "note": r"4つの解は原点を中心とする半径 $2$ の円に内接する正方形の頂点で、1つの解に $i$ を掛けるごとに $\dfrac\pi2$ 回転して次の解が得られる。一般に $z^n=\alpha$ の1つの解を $z_0$ とすると、解全体は $z_0,\ z_0\omega,\ \cdots,\ z_0\omega^{n-1}$（$\omega=\cos\dfrac{2\pi}n+i\sin\dfrac{2\pi}n$）である。",
  "ex": r"方程式 $z^4=-8-8\sqrt3\,i$ を解け。",
  "exa": r"$z=\pm(1+\sqrt3\,i),\ \pm(\sqrt3-i)$"},
 {"lv": 2, "title": "共役複素数を含む方程式",
  "q": r"方程式 $z^2=\overline{z}$ を満たす複素数 $z$ をすべて求めよ。",
  "hint": r"両辺の絶対値をとると $|z|$ が決まる。$|z|=1$ ならば $\overline z=\dfrac1z$ と書き換えられ、$z$ だけの方程式になる。",
  "sol": r"両辺の絶対値をとると $|z|^2=|\overline z|=|z|$ より $|z|(|z|-1)=0$，よって $|z|=0$ または $|z|=1$。<br>"
         r"(i) $|z|=0$ のとき $z=0$ で、これは方程式を満たす。<br>"
         r"(ii) $|z|=1$ のとき $\overline z=\dfrac1z$ であるから $z^2=\dfrac1z$，すなわち $z^3=1$。<br>"
         r"　$z^3-1=(z-1)(z^2+z+1)=0$ より $z=1,\ \dfrac{-1\pm\sqrt3\,i}2$。これらはいずれも $|z|=1$，$z^3=1$ を満たすから $z^2=\dfrac1z=\overline z$ となり、適する。<br>"
         r"以上より　$\boldsymbol{z=0,\ 1,\ \dfrac{-1\pm\sqrt3\,i}2}$",
  "note": r"別解：$z=x+yi$（$x,\ y$ は実数）とおくと $x^2-y^2=x$，$2xy=-y$。第2式から $y=0$ または $x=-\dfrac12$ として解いても同じ結果になる。極形式 $z=r(\cos\theta+i\sin\theta)$ を使えば $r^2=r$，$2\theta=-\theta+2k\pi$ となる。",
  "ex": r"方程式 $z^3=\overline z$ を満たす複素数 $z$ をすべて求めよ。",
  "exa": r"$z=0,\ \pm1,\ \pm i$"},
 {"lv": 3, "title": r"1 の 5 乗根と $\cos\dfrac{2\pi}5$",
  "q": r"$\omega=\cos\dfrac{2\pi}5+i\sin\dfrac{2\pi}5$ とする。<br>(1) $\omega^4+\omega^3+\omega^2+\omega+1=0$ であることを示せ。<br>(2) $t=\omega+\overline{\omega}$ とおくとき、$t$ の満たす2次方程式を求めよ。<br>(3) $\cos\dfrac{2\pi}5$ の値を求めよ。",
  "hint": r"(1) $\omega^5=1$ と因数分解。(2) $\overline\omega=\dfrac1\omega$ を用い、係数が左右対称な式を $\omega^2$ で割って $\omega+\dfrac1\omega$ で表す。",
  "sol": r"(1) ド・モアブルの定理より $\omega^5=\cos2\pi+i\sin2\pi=1$。$\omega^5-1=(\omega-1)(\omega^4+\omega^3+\omega^2+\omega+1)=0$ で、$\omega\neq1$ であるから<br>"
         r"　$\omega^4+\omega^3+\omega^2+\omega+1=0$<br>"
         r"(2) $|\omega|=1$ より $\overline\omega=\dfrac1\omega$，よって $t=\omega+\dfrac1\omega$。(1) の両辺を $\omega^2$（$\neq0$）で割ると<br>"
         r"　$\omega^2+\omega+1+\dfrac1\omega+\dfrac1{\omega^2}=0$　すなわち　$\left(\omega+\dfrac1\omega\right)^2-2+\left(\omega+\dfrac1\omega\right)+1=0$<br>"
         r"よって　$\boldsymbol{t^2+t-1=0}$<br>"
         r"(3) $t=\omega+\overline\omega=2\cos\dfrac{2\pi}5>0$ であるから $t=\dfrac{-1+\sqrt5}2$。よって　$\cos\dfrac{2\pi}5=\dfrac t2=\boldsymbol{\dfrac{\sqrt5-1}4}$",
  "note": r"$\omega^4+\omega^3+\omega^2+\omega+1=0$ は係数が左右対称な方程式（相反方程式）で、$\omega^2$ で割って $t=\omega+\dfrac1\omega$ とおくのが定石である。$t^2+t-1=0$ のもう1つの解 $\dfrac{-1-\sqrt5}2$ は $\omega^2+\overline{\omega^2}=2\cos\dfrac{4\pi}5$ である。",
  "ex": r"$\omega=\cos\dfrac{2\pi}7+i\sin\dfrac{2\pi}7$，$\alpha=\omega+\omega^2+\omega^4$，$\beta=\omega^3+\omega^5+\omega^6$ とする。$\alpha+\beta$，$\alpha\beta$ の値を求め、$\alpha$ の値を求めよ。",
  "exa": r"$\alpha+\beta=-1$，$\alpha\beta=2$，$\alpha=\dfrac{-1+\sqrt7\,i}2$（$\alpha$ の虚部 $\sin\dfrac{2\pi}7+\sin\dfrac{4\pi}7-\sin\dfrac{\pi}7$ は正）"},
 {"lv": 3, "title": r"1 の $n$ 乗根を含む分数式の和",
  "q": r"$\omega=\cos\dfrac{2\pi}9+i\sin\dfrac{2\pi}9$ とするとき、$\displaystyle S=\sum_{k=1}^{8}\frac1{1-\omega^k}$ の値を求めよ。",
  "hint": r"$\omega^9=1$ より $\omega^{9-k}=\dfrac1{\omega^k}$。$k$ の項と $9-k$ の項を組にすると、和が簡単になる。",
  "sol": r"$\omega^9=1$ であり、$k=1,\ 2,\ \cdots,\ 8$ に対して $\omega^k\neq1$ である。$\omega^{9-k}=\dfrac{\omega^9}{\omega^k}=\dfrac1{\omega^k}$ であるから<br>"
         r"　$\dfrac1{1-\omega^k}+\dfrac1{1-\omega^{9-k}}=\dfrac1{1-\omega^k}+\dfrac1{1-\frac1{\omega^k}}=\dfrac1{1-\omega^k}+\dfrac{\omega^k}{\omega^k-1}=\dfrac{1-\omega^k}{1-\omega^k}=1$<br>"
         r"$S$ の8個の項を $(k,\ 9-k)=(1,\ 8),\ (2,\ 7),\ (3,\ 6),\ (4,\ 5)$ の4組に分けると、各組の和が $1$ であるから　$S=\boldsymbol{4}$",
  "note": r"別解：$\theta=\dfrac{2k\pi}9$ とおき分母を実数化すると $\dfrac1{1-(\cos\theta+i\sin\theta)}=\dfrac12+\dfrac i2\cdot\dfrac{\sin\theta}{1-\cos\theta}$ となるので、どの項も実部が $\dfrac12$ で、虚部は $k$ と $9-k$ で打ち消し合う。一般に $\omega=\cos\dfrac{2\pi}n+i\sin\dfrac{2\pi}n$ のとき $\displaystyle\sum_{k=1}^{n-1}\frac1{1-\omega^k}=\frac{n-1}2$ である。",
  "ex": r"$\omega=\cos\dfrac{2\pi}7+i\sin\dfrac{2\pi}7$ とするとき、$\displaystyle\sum_{k=1}^{6}\frac{\omega^k}{1+\omega^k}$ の値を求めよ。",
  "exa": r"$3$"},
 {"lv": 4, "title": r"正 $n$ 角形の頂点を結ぶ線分の長さの積",
  "q": r"原点 O を中心とする半径 1 の円に内接する正 $n$ 角形 $\mathrm{A}_0\mathrm{A}_1\cdots\mathrm{A}_{n-1}$（$n\geqq3$）がある。<br>"
       r"(1) $\mathrm{A}_0\mathrm{A}_1\cdot\mathrm{A}_0\mathrm{A}_2\cdot\cdots\cdot\mathrm{A}_0\mathrm{A}_{n-1}=n$ であることを示せ。<br>"
       r"(2) $\displaystyle P_n=\sin\frac{\pi}{n}\sin\frac{2\pi}{n}\cdots\sin\frac{(n-1)\pi}{n}$ を $n$ の式で表せ。",
  "hint": r"頂点を 1 の $n$ 乗根 $1,\ \omega,\ \cdots,\ \omega^{n-1}$ に対応させる。$z^n-1=(z-1)(z-\omega)\cdots(z-\omega^{n-1})$ の両辺を $z-1$ で割った恒等式に $z=1$ を代入する。",
  "sol": r"複素数平面上で、$\mathrm{A}_k$ が $\omega^k$（$\omega=\cos\dfrac{2\pi}n+i\sin\dfrac{2\pi}n$）を表すように置いてよい。<br>"
         r"(1) $1,\ \omega,\ \cdots,\ \omega^{n-1}$ は $z^n=1$ の異なる $n$ 個の解であるから　$z^n-1=(z-1)(z-\omega)(z-\omega^2)\cdots(z-\omega^{n-1})$<br>"
         r"一方 $z^n-1=(z-1)(z^{n-1}+z^{n-2}+\cdots+z+1)$ であるから、2つの右辺を比べて（多項式として $z-1$ で割って）<br>"
         r"　$z^{n-1}+z^{n-2}+\cdots+z+1=(z-\omega)(z-\omega^2)\cdots(z-\omega^{n-1})$（恒等式）<br>"
         r"$z=1$ を代入して　$n=(1-\omega)(1-\omega^2)\cdots(1-\omega^{n-1})$<br>"
         r"両辺の絶対値をとると、$\mathrm{A}_0\mathrm{A}_k=|1-\omega^k|$ であるから　$\mathrm{A}_0\mathrm{A}_1\cdot\mathrm{A}_0\mathrm{A}_2\cdot\cdots\cdot\mathrm{A}_0\mathrm{A}_{n-1}=n$<br>"
         r"(2) $\theta_k=\dfrac{2k\pi}n$ とおくと　$|1-\omega^k|^2=(1-\cos\theta_k)^2+\sin^2\theta_k=2-2\cos\theta_k=4\sin^2\dfrac{k\pi}n$<br>"
         r"$0<\dfrac{k\pi}n<\pi$ より $\sin\dfrac{k\pi}n>0$ であるから $|1-\omega^k|=2\sin\dfrac{k\pi}n$。(1) より $2^{n-1}P_n=n$，よって　$\boldsymbol{P_n=\dfrac{n}{2^{n-1}}}$",
  "note": r"たとえば $n=7$ とすると $\sin\dfrac\pi7\sin\dfrac{2\pi}7\cdots\sin\dfrac{6\pi}7=\dfrac7{64}$ で、$\sin\dfrac{k\pi}7=\sin\dfrac{(7-k)\pi}7$ より $\sin\dfrac\pi7\sin\dfrac{2\pi}7\sin\dfrac{3\pi}7=\dfrac{\sqrt7}8$ が得られる。また恒等式に $z=-1$ を代入すると、$n$ が奇数のとき $|1+\omega|\,|1+\omega^2|\cdots|1+\omega^{n-1}|=1$ も分かる。",
  "ex": r"例題と同じ正 $n$ 角形について、円周上の点 $\mathrm{P}(z)$ に対し $\mathrm{PA}_0\cdot\mathrm{PA}_1\cdot\cdots\cdot\mathrm{PA}_{n-1}=|z^n-1|$ であることを示し、P が円周上を動くときのこの積の最大値を求めよ。",
  "exa": r"$z^n-1=(z-1)(z-\omega)\cdots(z-\omega^{n-1})$ の両辺の絶対値をとる。$|z^n-1|\leqq|z^n|+1=2$ より最大値は $2$（$z^n=-1$ のとき）"},
 {"lv": 5, "title": r"正 $n$ 角形の頂点と円周上の点の距離の累乗和",
  "q": r"$n$ を 3 以上の整数とし、$\omega=\cos\dfrac{2\pi}n+i\sin\dfrac{2\pi}n$，$\mathrm{A}_k(\omega^k)$（$k=0,\ 1,\ \cdots,\ n-1$）とする。点 $\mathrm{P}(z)$ が単位円 $|z|=1$ 上を動くとき、次の問いに答えよ。<br>"
       r"(1) $\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,2}$，$\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,4}$ は P の位置によらない一定の値であることを示し、その値を求めよ。<br>"
       r"(2) $\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,6}$ が P の位置によらない一定の値となるような $n$ をすべて求めよ。",
  "hint": r"$|z|=1$ のとき $u_k=z\omega^{-k}$ とおくと $\overline{u_k}=\dfrac1{u_k}$ で、$\mathrm{PA}_k^{\,2}=2-\left(u_k+\dfrac1{u_k}\right)$ と1つの文字で書ける。和 $\displaystyle\sum_{k=0}^{n-1}\omega^{mk}$ は $m$ が $n$ の倍数のときだけ $0$ にならないことを使い、展開した式の項ごとに和をとる。",
  "sol": r"<b>準備</b>　整数 $m$ に対して $\displaystyle\sum_{k=0}^{n-1}\omega^{mk}$ は、$m$ が $n$ の倍数のとき $n$ であり、そうでないときは $\omega^m\neq1$ より $\dfrac{(\omega^m)^n-1}{\omega^m-1}=0$ である。<br>"
         r"$|z|=1$ のとき $u_k=z\omega^{-k}$ とおくと、$|u_k|=1$ より $\overline{u_k}=\dfrac1{u_k}=\overline z\,\omega^k$ であり<br>"
         r"　$\mathrm{PA}_k^{\,2}=(z-\omega^k)(\overline z-\omega^{-k})=2-z\omega^{-k}-\overline z\omega^k=2-\left(u_k+\dfrac1{u_k}\right)$<br>"
         r"自然数 $m$ に対して $v_{m,k}=u_k^{\,m}+u_k^{-m}$ とおく。$\displaystyle\sum_{k=0}^{n-1}u_k^{\,m}=z^m\sum_{k=0}^{n-1}\omega^{-mk}$，$\displaystyle\sum_{k=0}^{n-1}u_k^{-m}=\overline z^{\,m}\sum_{k=0}^{n-1}\omega^{mk}$ であるから<br>"
         r"　$m$ が $n$ の倍数でないとき $\displaystyle\sum_{k=0}^{n-1}v_{m,k}=0$，$m$ が $n$ の倍数のとき $\displaystyle\sum_{k=0}^{n-1}v_{m,k}=n(z^m+\overline z^{\,m})$ …①<br>"
         r"また $v_{1,k}^{\ 2}=v_{2,k}+2$，$v_{1,k}^{\ 3}=v_{3,k}+3v_{1,k}$ である。<br>"
         r"(1) $\mathrm{PA}_k^{\,2}=2-v_{1,k}$，$\mathrm{PA}_k^{\,4}=(2-v_{1,k})^2=4-4v_{1,k}+(v_{2,k}+2)=6-4v_{1,k}+v_{2,k}$<br>"
         r"$n\geqq3$ より $1,\ 2$ は $n$ の倍数でないから、① より $\displaystyle\sum_k v_{1,k}=\sum_k v_{2,k}=0$。よって<br>"
         r"　$\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,2}=\boldsymbol{2n}$，$\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,4}=\boldsymbol{6n}$（P によらず一定）<br>"
         r"(2) $\mathrm{PA}_k^{\,6}=(2-v_{1,k})^3=8-12v_{1,k}+6(v_{2,k}+2)-(v_{3,k}+3v_{1,k})=20-15v_{1,k}+6v_{2,k}-v_{3,k}$<br>"
         r"$1,\ 2$ は $n$ の倍数でないから　$\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,6}=20n-\sum_{k=0}^{n-1}v_{3,k}$<br>"
         r"・$n\geqq4$ のとき、$3$ は $n$ の倍数でないから $\displaystyle\sum_k v_{3,k}=0$ で、和は $20n$（一定）である。<br>"
         r"・$n=3$ のとき、① より $\displaystyle\sum_k v_{3,k}=3(z^3+\overline z^{\,3})$ であるから、和は $60-3(z^3+\overline z^{\,3})$ となる。<br>"
         r"　$z=1$ のとき $54$，$z=-1$ のとき $66$ であり、一定ではない。<br>"
         r"よって、求める $n$ は　$\boldsymbol{n\geqq4}$（4 以上のすべての整数）",
  "note": r"$2-u-\dfrac1u=-\dfrac{(u-1)^2}u$ より $\mathrm{PA}_k^{\,2m}=(-1)^m\dfrac{(u_k-1)^{2m}}{u_k^{\,m}}$ で、展開すると $u_k^{\,j}$（$-m\leqq j\leqq m$）の項が現れ、定数項は ${}_{2m}\mathrm{C}_m$ である。したがって $\displaystyle\sum_k\mathrm{PA}_k^{\,2m}$ は $m\leqq n-1$ のとき一定値 $n\cdot{}_{2m}\mathrm{C}_m$ をとり（$m=1,\ 2,\ 3$ で $2n,\ 6n,\ 20n$），$m\geqq n$ のときは $z^n+\overline z^{\,n}$ の項が残って一定でない。",
  "ex": r"例題と同じ設定で、$\displaystyle\sum_{k=0}^{n-1}\mathrm{PA}_k^{\,8}$ が P の位置によらない一定の値となるような $n$ をすべて求め、そのときの値を求めよ。",
  "exa": r"$n\geqq5$，値は $70n$"},
]})


def _v4():
    for z in [sqrt(3) + I, -sqrt(3) + I, -2 * I]:
        assert Z(z**3 - 8 * I)
    for a in (1, -1):
        for b in (1, -1):
            assert Z((sqrt(2) * a + sqrt(2) * b * I)**4 + 16)
    for z in [sqrt(3) + I, -1 + sqrt(3) * I, -sqrt(3) - I, 1 - sqrt(3) * I]:
        assert Z(z**4 - (-8 + 8 * sqrt(3) * I))
    for z in [1 + sqrt(3) * I, -1 - sqrt(3) * I, sqrt(3) - I, -sqrt(3) + I]:
        assert Z(z**4 - (-8 - 8 * sqrt(3) * I))
    x, y = symbols("x y", real=True)
    s1 = solve([x**2 - y**2 - x, 2 * x * y + y], [x, y], dict=True)
    got = sorted((round(float(d[x]), 9), round(float(d[y]), 9)) for d in s1)
    assert got == sorted([(0.0, 0.0), (1.0, 0.0), (-0.5, round(3**0.5 / 2, 9)), (-0.5, -round(3**0.5 / 2, 9))])
    w = expand((x + I * y)**3)
    s2 = solve([sre(w) - x, sim(w) + y], [x, y], dict=True)
    got = sorted((round(float(d[x]), 9), round(float(d[y]), 9)) for d in s2)
    assert got == sorted([(0.0, 0.0), (1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)])
    om = cmath.exp(2j * math.pi / 5)
    assert cl(sum(om**k for k in range(5)), 0) and cl((om + 1 / om)**2 + (om + 1 / om) - 1, 0)
    assert Z(cos(2 * pi / 5) - (sqrt(5) - 1) / 4)
    assert cl(om**2 + om**-2, (-1 - 5**0.5) / 2)
    om = cmath.exp(2j * math.pi / 7)
    al, be = om + om**2 + om**4, om**3 + om**5 + om**6
    assert cl(al + be, -1) and cl(al * be, 2) and cl(al, (-1 + 7**0.5 * 1j) / 2)
    assert math.sin(2 * math.pi / 7) + math.sin(4 * math.pi / 7) - math.sin(math.pi / 7) > 0
    om = cmath.exp(2j * math.pi / 9)
    assert cl(sum(1 / (1 - om**k) for k in range(1, 9)), 4)
    om = cmath.exp(2j * math.pi / 7)
    assert cl(sum(om**k / (1 + om**k) for k in range(1, 7)), 3)
    for n in range(3, 25):
        om = cmath.exp(2j * math.pi / n)
        assert cl(sum(1 / (1 - om**k) for k in range(1, n)), (n - 1) / 2, 1e-8)
        pr = 1
        for k in range(1, n):
            pr *= abs(1 - om**k)
        assert abs(pr - n) < 1e-8
        assert abs(math.prod(math.sin(k * math.pi / n) for k in range(1, n)) - n / 2**(n - 1)) < 1e-12
        if n % 2:
            assert abs(math.prod(abs(1 + om**k) for k in range(1, n)) - 1) < 1e-8
        for _ in range(5):
            zz = runit()
            assert abs(math.prod(abs(zz - om**k) for k in range(n)) - abs(zz**n - 1)) < 1e-8
        assert max(abs(cmath.exp(1j * 2 * math.pi * j / 3000)**n - 1) for j in range(3000)) <= 2 + 1e-12
        th = math.pi / n
        assert abs(abs(cmath.exp(1j * th)**n - 1) - 2) < 1e-12
    assert abs(math.sin(math.pi / 7) * math.sin(2 * math.pi / 7) * math.sin(3 * math.pi / 7) - 7**0.5 / 8) < 1e-12
    # 距離の累乗和
    u = symbols("u")
    assert Z((2 - u - 1 / u)**3 - (20 - 15 * (u + 1 / u) + 6 * (u**2 + u**-2) - (u**3 + u**-3)))
    assert Z((2 - u - 1 / u)**4 - (70 - 56 * (u + 1 / u) + 28 * (u**2 + u**-2) - 8 * (u**3 + u**-3) + (u**4 + u**-4)))

    def psum(n, m, zz):
        om = cmath.exp(2j * math.pi / n)
        return sum(abs(zz - om**k)**(2 * m) for k in range(n))
    for n in range(3, 10):
        vals = {m: [psum(n, m, cmath.exp(1j * t)) for t in [0.1 * j for j in range(63)]] for m in range(1, 9)}
        for m in range(1, 9):
            const = max(vals[m]) - min(vals[m]) < 1e-6
            assert const == (m <= n - 1)
            if const:
                assert abs(vals[m][0] - n * math.comb(2 * m, m)) < 1e-6
    assert abs(psum(3, 3, 1) - 54) < 1e-9 and abs(psum(3, 3, -1) - 66) < 1e-9
    for t in [0.3, 1.1, 2.0]:
        zz = cmath.exp(1j * t)
        assert abs(psum(3, 3, zz) - (60 - 6 * (zz**3).real)) < 1e-9
    for n in range(3, 10):
        v = [psum(n, 4, cmath.exp(0.1j * j)) for j in range(63)]
        assert (max(v) - min(v) < 1e-6) == (n >= 5)
        if n >= 5:
            assert abs(v[0] - 70 * n) < 1e-6


# ---------------------------------------------------------------- 節5
RHO = complex(0.5, 3**0.5 / 2)          # cos(π/3)+i sin(π/3)


def fig_squares():
    A, B, C = 0, complex(-1.2, -2), complex(1.6, -2)
    E, G = -1j * B, 1j * C
    D, F, M = B + E, C + G, (B + C) / 2
    f = Fig(-3.45, 3.85, -2.35, 1.95, 31)
    f.poly([A, B, D, E], fill="#eef2fa", col=BLUE, w=1.0)
    f.poly([A, C, F, G], fill="#eef2fa", col=BLUE, w=1.0)
    f.poly([A, B, C], fill=FILL, col=BLUE, w=1.3)
    f.line(A, M, col=RED, w=1.4); f.line(E, G, col=RED, w=1.4)
    for z, t, dx, dy in [(A, "A", -4, -6), (B, "B", -5, 12), (C, "C", 2, 12), (D, "D", -11, 4), (E, "E", -6, -5),
                         (F, "F", 4, 4), (G, "G", 2, -5), (M, "M", -4, 13)]:
        f.dot(z, r=1.8); f.text(z, t, dx, dy)
    return f.svg()


def napoleon(a, b, c, inner=False):
    L = complex(0.5, -3**0.5 / 6)
    if inner:
        L = L.conjugate()
    return b + L * (c - b), c + L * (a - c), a + L * (b - a)


def fig_napoleon():
    A, B, C = complex(1.2, 1.4), 0, 3
    ext = [B + RHO.conjugate() * (C - B), C + RHO.conjugate() * (A - C), A + RHO.conjugate() * (B - A)]
    P, Q, R = napoleon(A, B, C)
    xs = [z.real for z in ext + [A, B, C]]; ys = [z.imag for z in ext + [A, B, C]]
    f = Fig(min(xs) - 0.3, max(xs) + 0.35, min(ys) - 0.25, max(ys) + 0.25, 40)
    for (u, v), w in zip([(B, C), (C, A), (A, B)], ext):
        f.poly([u, w, v], fill="#f1f4fa", col="#8a94a8", w=1.0)
    f.poly([A, B, C], fill=FILL, col=BLUE, w=1.3)
    f.poly([P, Q, R], fill="none", col=RED, w=1.4)
    for z, t, dx, dy in [(A, "A", -3, -6), (B, "B", -11, 4), (C, "C", 4, 4), (P, "P", 4, 4), (Q, "Q", 4, -3), (R, "R", -11, -2)]:
        f.dot(z, r=1.8); f.text(z, t, dx, dy)
    return f.svg()


SEC.append({"title": "回転と図形への応用",
"base": r"""・$\cos\theta+i\sin\theta$ を掛けると原点のまわりに $\theta$ 回転、$r(\cos\theta+i\sin\theta)$ を掛けると $\theta$ 回転して原点からの距離が $r$ 倍になる。<br>
・点 $\beta$ を点 $\alpha$ のまわりに $\theta$ 回転した点 $\gamma$：$\gamma-\alpha=(\cos\theta+i\sin\theta)(\beta-\alpha)$<br>
・異なる3点 $\mathrm{A}(\alpha)$，$\mathrm{B}(\beta)$，$\mathrm{C}(\gamma)$ について、$\dfrac{\gamma-\alpha}{\beta-\alpha}=r(\cos\theta+i\sin\theta)$ ならば $\dfrac{\mathrm{AC}}{\mathrm{AB}}=r$ で、半直線 AB から半直線 AC へ測った角が $\theta$<br>
・3点 A，B，C が一直線上 $\iff\dfrac{\gamma-\alpha}{\beta-\alpha}$ が実数　　$\mathrm{AB}\perp\mathrm{AC}\iff\dfrac{\gamma-\alpha}{\beta-\alpha}$ が純虚数<br>
・証明問題では、基準の点を原点にとり、頂点が反時計回りに並ぶように置くと計算が簡単になる""",
"items": [
 {"lv": 1, "title": "点の回転と拡大",
  "q": r"$\alpha=3+i$，$\beta=1+2i$ とする。次の点を表す複素数を求めよ。<br>(1) 点 $\alpha$ を原点のまわりに $\dfrac\pi3$ だけ回転した点<br>(2) 点 $\alpha$ を原点のまわりに $-\dfrac\pi4$ だけ回転し、原点からの距離を $\sqrt2$ 倍した点<br>(3) 点 $\alpha$ を点 $\beta$ のまわりに $\dfrac\pi2$ だけ回転した点",
  "hint": r"原点のまわりの $\theta$ 回転は $\cos\theta+i\sin\theta$ を掛けること。点 $\beta$ のまわりの回転は、$\beta$ が原点に来るように平行移動してから回転し、もとに戻す。",
  "sol": r"(1) $\left(\cos\dfrac\pi3+i\sin\dfrac\pi3\right)(3+i)=\left(\dfrac12+\dfrac{\sqrt3}2i\right)(3+i)=\boldsymbol{\dfrac{3-\sqrt3}2+\dfrac{1+3\sqrt3}2i}$<br>"
         r"(2) $\sqrt2\left\{\cos\left(-\dfrac\pi4\right)+i\sin\left(-\dfrac\pi4\right)\right\}=1-i$ であるから　$(1-i)(3+i)=\boldsymbol{4-2i}$<br>"
         r"(3) 求める点を $\gamma$ とすると　$\gamma-\beta=\left(\cos\dfrac\pi2+i\sin\dfrac\pi2\right)(\alpha-\beta)=i(2-i)=1+2i$<br>"
         r"　よって　$\gamma=\beta+(1+2i)=\boldsymbol{2+4i}$",
  "note": r"点 $\beta$ のまわりの回転の式 $\gamma-\beta=(\cos\theta+i\sin\theta)(\alpha-\beta)$ は「$\overrightarrow{\mathrm{BA}}$ を $\theta$ 回転したものが $\overrightarrow{\mathrm{BC}}$」と読む。これが図形への応用の出発点になる。",
  "ex": r"$\alpha=2-2i$，$\beta=-1+i$ とする。(1) 点 $\alpha$ を原点のまわりに $\dfrac23\pi$ 回転した点　(2) 点 $\alpha$ を原点のまわりに $\dfrac\pi6$ 回転し、原点からの距離を $2$ 倍した点　(3) 点 $\alpha$ を点 $\beta$ のまわりに $-\dfrac\pi2$ 回転した点 を求めよ。",
  "exa": r"(1) $(-1+\sqrt3)+(1+\sqrt3)i$　(2) $(2\sqrt3+2)+(2-2\sqrt3)i$　(3) $-4-2i$"},
 {"lv": 2, "title": "正三角形・正方形の頂点",
  "q": r"複素数平面上の2点 $\mathrm{A}(1+i)$，$\mathrm{B}(3+2i)$ に対して、$\triangle\mathrm{ABC}$ が正三角形となるような点 $\mathrm{C}(\gamma)$ を求めよ。",
  "hint": r"C は、点 B を点 A のまわりに $\dfrac\pi3$ または $-\dfrac\pi3$ 回転した点である。",
  "sol": r"点 C は点 B を点 A のまわりに $\pm\dfrac\pi3$ 回転した点であるから<br>"
         r"　$\gamma-(1+i)=\left\{\cos\left(\pm\dfrac\pi3\right)+i\sin\left(\pm\dfrac\pi3\right)\right\}\{(3+2i)-(1+i)\}=\left(\dfrac12\pm\dfrac{\sqrt3}2i\right)(2+i)$<br>"
         r"　$\phantom{\gamma-(1+i)}=\left(1\mp\dfrac{\sqrt3}2\right)+\left(\dfrac12\pm\sqrt3\right)i$（複号同順）<br>"
         r"よって　$\boldsymbol{\gamma=\dfrac{4-\sqrt3}2+\dfrac{3+2\sqrt3}2i,\ \ \dfrac{4+\sqrt3}2+\dfrac{3-2\sqrt3}2i}$",
  "note": r"正三角形は、直線 AB のどちら側に C があるかで2通りある。正方形や直角二等辺三角形でも同様に、回転角 $\pm\dfrac\pi2$ や $\pm\dfrac\pi4$（長さは $\sqrt2$ 倍または $\dfrac1{\sqrt2}$ 倍）を使う。",
  "ex": r"2点 $\mathrm{A}(2+i)$，$\mathrm{B}(4+5i)$ を頂点とする正方形 ABCD がある。頂点 A，B，C，D がこの順に反時計回りに並ぶとき、頂点 C，D を表す複素数を求めよ。",
  "exa": r"$\mathrm{C}(7i)$，$\mathrm{D}(-2+3i)$"},
 {"lv": 2, "title": "角の大きさ・3点が一直線上にある条件・垂直条件",
  "q": r"(1) 3点 $\mathrm{A}(1+i)$，$\mathrm{B}(4+2i)$，$\mathrm{C}(3+5i)$ について、$\angle\mathrm{BAC}$ の大きさと $\dfrac{\mathrm{AC}}{\mathrm{AB}}$ を求めよ。<br>"
       r"(2) 3点 $\mathrm{A}(2+i)$，$\mathrm{B}(4-i)$，$\mathrm{C}(a+4i)$（$a$ は実数）について、3点 A，B，C が一直線上にあるような $a$ の値と、$\mathrm{AB}\perp\mathrm{AC}$ となるような $a$ の値を求めよ。",
  "hint": r"$\dfrac{\gamma-\alpha}{\beta-\alpha}$ を計算する。その絶対値が $\dfrac{\mathrm{AC}}{\mathrm{AB}}$，偏角が $\angle\mathrm{BAC}$。一直線上 $\iff$ 実数，垂直 $\iff$ 純虚数。",
  "sol": r"(1) $\dfrac{\gamma-\alpha}{\beta-\alpha}=\dfrac{2+4i}{3+i}=\dfrac{(2+4i)(3-i)}{10}=\dfrac{10+10i}{10}=1+i=\sqrt2\left(\cos\dfrac\pi4+i\sin\dfrac\pi4\right)$<br>"
         r"　よって　$\boldsymbol{\angle\mathrm{BAC}=\dfrac\pi4}$，$\boldsymbol{\dfrac{\mathrm{AC}}{\mathrm{AB}}=\sqrt2}$<br>"
         r"(2) $\dfrac{\gamma-\alpha}{\beta-\alpha}=\dfrac{(a-2)+3i}{2-2i}=\dfrac{\{(a-2)+3i\}(2+2i)}{8}=\dfrac{(2a-10)+(2a+2)i}{8}$<br>"
         r"　3点が一直線上にある $\iff$ これが実数 $\iff2a+2=0$　　よって　$\boldsymbol{a=-1}$<br>"
         r"　$\mathrm{AB}\perp\mathrm{AC}\iff$ これが純虚数 $\iff2a-10=0$ かつ $2a+2\neq0$　　よって　$\boldsymbol{a=5}$",
  "note": r"$\arg\dfrac{\gamma-\alpha}{\beta-\alpha}$ は半直線 AB から半直線 AC へ反時計回りに測った角で、負の値になるときは時計回りに測った角を表す。三角形の内角として大きさだけが問題のときは、その絶対値（$0$ から $\pi$ の範囲にとる）を答える。",
  "ex": r"(1) 3点 $\mathrm{A}(1+2i)$，$\mathrm{B}(2+4i)$，$\mathrm{C}(-2+i)$ について、$\angle\mathrm{BAC}$ の大きさを求めよ。(2) 3点 $\mathrm{A}(1-i)$，$\mathrm{B}(3+i)$，$\mathrm{C}(a-3i)$（$a$ は実数）が一直線上にあるような $a$ の値と、$\mathrm{AB}\perp\mathrm{AC}$ となるような $a$ の値を求めよ。",
  "exa": r"(1) $\dfrac34\pi$　(2) 一直線上：$a=-1$，垂直：$a=3$"},
 {"lv": 3, "title": "等式から三角形の形状を決める",
  "q": r"異なる3点 $\mathrm{A}(\alpha)$，$\mathrm{B}(\beta)$，$\mathrm{C}(\gamma)$ を頂点とする $\triangle\mathrm{ABC}$ について、次の問いに答えよ。<br>"
       r"(1) $\gamma-\alpha=(1+\sqrt3\,i)(\beta-\alpha)$ が成り立つとき、$\triangle\mathrm{ABC}$ の3つの角の大きさを求めよ。<br>"
       r"(2) $\alpha^2+\beta^2+\gamma^2=\alpha\beta+\beta\gamma+\gamma\alpha$ が成り立つとき、$\triangle\mathrm{ABC}$ は正三角形であることを示せ。",
  "hint": r"どちらも $\dfrac{\gamma-\alpha}{\beta-\alpha}$ の値を求めれば、2辺の比とその間の角が分かる。(2) は $\beta-\alpha=u$，$\gamma-\alpha=v$ とおいて式を $u,\ v$ で表す。",
  "sol": r"(1) $\dfrac{\gamma-\alpha}{\beta-\alpha}=1+\sqrt3\,i=2\left(\cos\dfrac\pi3+i\sin\dfrac\pi3\right)$ より　$\mathrm{AC}=2\mathrm{AB}$，$\angle\mathrm{BAC}=\dfrac\pi3$<br>"
         r"　$\mathrm{AB}=k$ とすると、余弦定理より $\mathrm{BC}^2=k^2+4k^2-2\cdot k\cdot2k\cos\dfrac\pi3=3k^2$<br>"
         r"　$\mathrm{AB}^2+\mathrm{BC}^2=4k^2=\mathrm{CA}^2$ より $\angle\mathrm{B}=\dfrac\pi2$。よって　$\boldsymbol{\angle\mathrm{A}=\dfrac\pi3,\ \angle\mathrm{B}=\dfrac\pi2,\ \angle\mathrm{C}=\dfrac\pi6}$<br>"
         r"(2) $u=\beta-\alpha$，$v=\gamma-\alpha$ とおくと $u\neq0$，$v\neq0$ で、$\beta=\alpha+u$，$\gamma=\alpha+v$ を代入して整理すると<br>"
         r"　$\alpha^2+\beta^2+\gamma^2-\alpha\beta-\beta\gamma-\gamma\alpha=u^2-uv+v^2$<br>"
         r"よって条件は $u^2-uv+v^2=0$。両辺を $u^2$ で割り $t=\dfrac vu$ とおくと $t^2-t+1=0$ より<br>"
         r"　$t=\dfrac{1\pm\sqrt3\,i}2=\cos\left(\pm\dfrac\pi3\right)+i\sin\left(\pm\dfrac\pi3\right)$<br>"
         r"すなわち $\dfrac{\gamma-\alpha}{\beta-\alpha}=\cos\left(\pm\dfrac\pi3\right)+i\sin\left(\pm\dfrac\pi3\right)$ であるから、$\mathrm{AC}=\mathrm{AB}$，$\angle\mathrm{BAC}=\dfrac\pi3$。<br>"
         r"2辺が等しくその間の角が $\dfrac\pi3$ の三角形は正三角形であるから、$\triangle\mathrm{ABC}$ は正三角形である。",
  "note": r"逆に正三角形ならば (2) の等式が成り立つ。この等式は $(\alpha-\beta)^2+(\beta-\gamma)^2+(\gamma-\alpha)^2=0$ とも書ける。また、$\omega=\dfrac{-1+\sqrt3\,i}2$ を用いると $\alpha^2+\beta^2+\gamma^2-\alpha\beta-\beta\gamma-\gamma\alpha=(\alpha+\beta\omega+\gamma\omega^2)(\alpha+\beta\omega^2+\gamma\omega)$ と因数分解でき、2つの因子が三角形の2つの向きに対応する。",
  "ex": r"異なる3点 $\mathrm{A}(\alpha)$，$\mathrm{B}(\beta)$，$\mathrm{C}(\gamma)$ が $2\alpha^2+\beta^2+\gamma^2-2\alpha\beta-2\alpha\gamma=0$ を満たすとき、$\triangle\mathrm{ABC}$ はどのような三角形か。",
  "exa": r"$(\beta-\alpha)^2+(\gamma-\alpha)^2=0$ より $\dfrac{\gamma-\alpha}{\beta-\alpha}=\pm i$。$\angle\mathrm{A}=\dfrac\pi2$ の直角二等辺三角形"},
 {"lv": 4, "title": "外心を原点とする三角形の垂心",
  "q": r"原点 O を外心とする $\triangle\mathrm{ABC}$ の頂点を $\mathrm{A}(\alpha)$，$\mathrm{B}(\beta)$，$\mathrm{C}(\gamma)$ とし、外接円の半径を $r$ とする。点 $\mathrm{H}(h)$ を $h=\alpha+\beta+\gamma$ で定める。<br>"
       r"(1) H は $\triangle\mathrm{ABC}$ の垂心であることを示せ。<br>"
       r"(2) H が外接円の周上にあるならば、$\triangle\mathrm{ABC}$ は直角三角形であることを示せ。",
  "hint": r"$|\alpha|=r$ より $\overline\alpha=\dfrac{r^2}\alpha$。垂直は「比が純虚数」で示す。(2) は $h\overline h=r^2$ を $\alpha,\ \beta,\ \gamma$ の式に直し、$(\alpha+\beta)(\beta+\gamma)(\gamma+\alpha)=(\alpha+\beta+\gamma)(\alpha\beta+\beta\gamma+\gamma\alpha)-\alpha\beta\gamma$ を使う。",
  "sol": r"$|\alpha|=|\beta|=|\gamma|=r$ より　$\overline\alpha=\dfrac{r^2}\alpha$，$\overline\beta=\dfrac{r^2}\beta$，$\overline\gamma=\dfrac{r^2}\gamma$<br>"
         r"(1) $h-\alpha=\beta+\gamma$ である。$\beta+\gamma=0$ のときは $h=\alpha$ で、BC が外接円の直径となるから $\angle\mathrm{A}=\dfrac\pi2$ であり、垂心は A に一致する。<br>"
         r"$\beta+\gamma\neq0$ のとき、$w=\dfrac{h-\alpha}{\gamma-\beta}=\dfrac{\beta+\gamma}{\gamma-\beta}$ とおくと<br>"
         r"　$\overline w=\dfrac{\overline\beta+\overline\gamma}{\overline\gamma-\overline\beta}=\dfrac{\frac{r^2}\beta+\frac{r^2}\gamma}{\frac{r^2}\gamma-\frac{r^2}\beta}=\dfrac{\gamma+\beta}{\beta-\gamma}=-w$<br>"
         r"$w\neq0$ であるから $w$ は純虚数で、$\mathrm{AH}\perp\mathrm{BC}$。同様に、$\gamma+\alpha\neq0$ のとき $\mathrm{BH}\perp\mathrm{CA}$ であり、$\gamma+\alpha=0$ のときは $h=\beta$ で垂心は B に一致する。<br>"
         r"いずれの場合も H は2本の垂線の交点（または直角の頂点）であるから、H は $\triangle\mathrm{ABC}$ の垂心である。<br>"
         r"(2) $|h|=r$ より $h\overline h=r^2$。$\overline h=\overline\alpha+\overline\beta+\overline\gamma=\dfrac{r^2(\alpha\beta+\beta\gamma+\gamma\alpha)}{\alpha\beta\gamma}$ であるから<br>"
         r"　$\dfrac{r^2(\alpha+\beta+\gamma)(\alpha\beta+\beta\gamma+\gamma\alpha)}{\alpha\beta\gamma}=r^2$　すなわち　$(\alpha+\beta+\gamma)(\alpha\beta+\beta\gamma+\gamma\alpha)-\alpha\beta\gamma=0$<br>"
         r"左辺は $(\alpha+\beta)(\beta+\gamma)(\gamma+\alpha)$ に等しいから　$(\alpha+\beta)(\beta+\gamma)(\gamma+\alpha)=0$<br>"
         r"たとえば $\alpha+\beta=0$ ならば AB は外接円の直径で $\angle\mathrm{C}=\dfrac\pi2$ となる。他の場合も同様で、$\triangle\mathrm{ABC}$ は直角三角形である。",
  "note": r"重心 $\mathrm{G}\left(\dfrac{\alpha+\beta+\gamma}3\right)$ について $\overrightarrow{\mathrm{OH}}=3\overrightarrow{\mathrm{OG}}$ であるから、外心 O，重心 G，垂心 H は一直線上にあり、$\mathrm{OG}:\mathrm{GH}=1:2$ である（オイラー線）。(2) の逆も成り立つ（直角三角形の垂心は直角の頂点で、外接円の周上にある）。",
  "ex": r"例題と同じ設定で、$\alpha+\beta+\gamma=0$ ならば $\triangle\mathrm{ABC}$ は正三角形であることを示せ。",
  "exa": r"$\gamma=-(\alpha+\beta)$ より $|\alpha+\beta|^2=r^2$，よって $\alpha\overline\beta+\overline\alpha\beta=-r^2$ で $|\alpha-\beta|^2=3r^2$。同様に他の2辺も $\sqrt3\,r$ となる。"},
 {"lv": 4, "title": "正方形を外側につくった図形の証明",
  "q": fig_squares() +
       r"$\triangle\mathrm{ABC}$ の辺 AB，AC をそれぞれ1辺とする正方形 ABDE，ACFG を $\triangle\mathrm{ABC}$ の外側につくる。辺 BC の中点を M とするとき、$\mathrm{AM}\perp\mathrm{EG}$ かつ $\mathrm{EG}=2\mathrm{AM}$ であることを示せ。",
  "hint": r"A を原点にとり、A，B，C が反時計回りに並ぶように置く。E は B を A のまわりに $-\dfrac\pi2$ 回転した点，G は C を A のまわりに $\dfrac\pi2$ 回転した点。$g-e$ と $m$ の比を調べる。",
  "sol": r"A を原点とし、A，B，C がこの順に反時計回りに並ぶように複素数平面上に置く（時計回りのときは実軸に関して折り返して考えればよい）。$\mathrm{B}(\beta)$，$\mathrm{C}(\gamma)$，$\mathrm{E}(e)$，$\mathrm{G}(g)$，$\mathrm{M}(m)$ とする。<br>"
         r"A，B，C が反時計回りであるから、C は $\overrightarrow{\mathrm{AB}}$ を $\dfrac\pi2$ 回転した向きの側にあり、外側の正方形の頂点 E は B を A のまわりに $-\dfrac\pi2$ 回転した点である。よって $e=-i\beta$。<br>"
         r"同様に、B は $\overrightarrow{\mathrm{AC}}$ を $-\dfrac\pi2$ 回転した向きの側にあるから、G は C を A のまわりに $\dfrac\pi2$ 回転した点で $g=i\gamma$。また $m=\dfrac{\beta+\gamma}2$（$m\neq0$）である。よって<br>"
         r"　$g-e=i\gamma+i\beta=i(\beta+\gamma)=2i\,m$　すなわち　$\dfrac{g-e}{m}=2i$<br>"
         r"$2i$ は純虚数であるから $\mathrm{AM}\perp\mathrm{EG}$，また $|g-e|=2|m|$ より $\mathrm{EG}=2\mathrm{AM}$ である。",
  "note": r"$ie=\beta$，$i\gamma=g$ であるから、$\triangle\mathrm{AEC}$ を A のまわりに $\dfrac\pi2$ 回転すると $\triangle\mathrm{ABG}$ に重なる。これから $\mathrm{EC}=\mathrm{BG}$，$\mathrm{EC}\perp\mathrm{BG}$ も分かる。また $\angle\mathrm{EAG}=\pi-\angle\mathrm{BAC}$ より、$\triangle\mathrm{AEG}$ と $\triangle\mathrm{ABC}$ の面積は等しい。",
  "ex": r"例題と同じ図で、正方形 ABDE，ACFG の中心をそれぞれ P，Q とするとき、$\triangle\mathrm{MPQ}$ は $\angle\mathrm{M}=\dfrac\pi2$ の直角二等辺三角形であることを示せ。",
  "exa": r"A を原点とすると $p=\dfrac{(1-i)\beta}2$，$q=\dfrac{(1+i)\gamma}2$，$m=\dfrac{\beta+\gamma}2$ で、$p-m=i(q-m)$ が成り立つ。"},
 {"lv": 5, "title": "回転による図形の論証（ナポレオンの定理と面積の差）",
  "q": fig_napoleon() +
       r"$\triangle\mathrm{ABC}$ の各辺を1辺とする正三角形を $\triangle\mathrm{ABC}$ の外側に3つつくり、辺 BC，CA，AB 上の正三角形の重心をそれぞれ P，Q，R とする。また、各辺を1辺とする正三角形を、その辺に関して $\triangle\mathrm{ABC}$ と同じ側に3つつくり、それらの重心をそれぞれ $\mathrm{P'}$，$\mathrm{Q'}$，$\mathrm{R'}$ とする。<br>"
       r"(1) $\triangle\mathrm{PQR}$ は正三角形であることを示せ。<br>"
       r"(2) $\mathrm{P'}$，$\mathrm{Q'}$，$\mathrm{R'}$ は正三角形の3頂点となるか、または1点に一致することを示せ。さらに、$\triangle\mathrm{PQR}$ の面積から $\triangle\mathrm{P'Q'R'}$ の面積を引いた差は、$\triangle\mathrm{ABC}$ の面積に等しいことを示せ（1点に一致するときは $\triangle\mathrm{P'Q'R'}$ の面積を $0$ とする）。",
  "hint": r"A，B，C を反時計回りに置くと、辺 BC の外側の正三角形の重心は、B から $\overrightarrow{\mathrm{BC}}$ を $-\dfrac\pi6$ 回転して $\dfrac1{\sqrt3}$ 倍した位置にある。これを $L=\dfrac12-\dfrac{\sqrt3}6i$ で表し、$r-p$ が $q-p$ の $\dfrac\pi3$ 回転であることを係数の比較で示す。面積は1辺の2乗の差に帰着させ、平行移動で C を原点にして計算する。",
  "sol": r"A，B，C がこの順に反時計回りに並ぶように複素数平面上に置き（時計回りのときは実軸に関して折り返せばよい）、$\mathrm{A}(a)$，$\mathrm{B}(b)$，$\mathrm{C}(c)$，$\mathrm{P}(p)$ などとする。<br>"
         r"1辺の長さ $s$ の正三角形の重心は、頂点から距離 $\dfrac s{\sqrt3}$ の位置にあり、頂点から出る辺と $\dfrac\pi6$ の角をなす。$\triangle\mathrm{ABC}$ は反時計回りなので、辺 BC の外側は $\overrightarrow{\mathrm{BC}}$ を $-\dfrac\pi2$ 回転した向きの側である。よって<br>"
         r"　$L=\dfrac1{\sqrt3}\left\{\cos\left(-\dfrac\pi6\right)+i\sin\left(-\dfrac\pi6\right)\right\}=\dfrac12-\dfrac{\sqrt3}6i$ とおくと　$p=b+L(c-b)$，$q=c+L(a-c)$，$r=a+L(b-a)$<br>"
         r"$1-L=\overline L$，$1-2L=\dfrac{\sqrt3}3i$ に注意して整理すると<br>"
         r"　$q-p=La-\overline Lb+\dfrac{\sqrt3}3i\,c$，　$r-p=\overline La-\dfrac{\sqrt3}3i\,b-Lc$ …①<br>"
         r"(1) $\rho=\cos\dfrac\pi3+i\sin\dfrac\pi3=\dfrac{1+\sqrt3\,i}2$ とおくと、直接計算により<br>"
         r"　$\rho L=\overline L$，　$\rho\overline L=\dfrac{\sqrt3}3i$，　$\rho\cdot\dfrac{\sqrt3}3i=-L$ …②<br>"
         r"よって ① より $\rho(q-p)=\overline La-\dfrac{\sqrt3}3i\,b-Lc=r-p$。すなわち R は Q を P のまわりに $\dfrac\pi3$ 回転した点であり、$\triangle\mathrm{PQR}$ は正三角形である。<br>"
         r"(2) 内側の正三角形では回転の向きが逆になるから、$L$ を $\overline L$ に置き換えて $p'=b+\overline L(c-b)$，$q'=c+\overline L(a-c)$，$r'=a+\overline L(b-a)$。同様に整理して<br>"
         r"　$q'-p'=\overline La-Lb-\dfrac{\sqrt3}3i\,c$，　$r'-p'=La+\dfrac{\sqrt3}3i\,b-\overline Lc$ …③<br>"
         r"② の共役をとると $\overline\rho\,\overline L=L$，$\overline\rho L=-\dfrac{\sqrt3}3i$，$\overline\rho\cdot\left(-\dfrac{\sqrt3}3i\right)=-\overline L$ であるから、③ より $\overline\rho(q'-p')=r'-p'$。<br>"
         r"よって $q'=p'$ ならば $r'=p'$ で3点は一致し、$q'\neq p'$ ならば $\mathrm{R'}$ は $\mathrm{Q'}$ を $\mathrm{P'}$ のまわりに $-\dfrac\pi3$ 回転した点で、$\triangle\mathrm{P'Q'R'}$ は正三角形である。<br>"
         r"<b>面積</b>　1辺 $s$ の正三角形の面積は $\dfrac{\sqrt3}4s^2$ であるから、$\triangle\mathrm{ABC}$ の面積を $S$ として、$D=|q-p|^2-|q'-p'|^2=\dfrac4{\sqrt3}S$ を示せばよい。<br>"
         r"①，③ の $a,\ b,\ c$ の係数の和はどちらも $0$ なので、$a,\ b,\ c$ を同じ複素数だけずらしても $q-p$，$q'-p'$ は変わらない。そこで $c=0$ としてよく、$q-p=La-\overline Lb$，$q'-p'=\overline La-Lb$。$|L|^2=\dfrac13$ より<br>"
         r"　$|La-\overline Lb|^2=\dfrac13(|a|^2+|b|^2)-(L^2a\overline b+\overline L^2\,\overline ab)$，　$|\overline La-Lb|^2=\dfrac13(|a|^2+|b|^2)-(\overline L^2a\overline b+L^2\,\overline ab)$<br>"
         r"よって $D=(L^2-\overline L^2)(\overline ab-a\overline b)$。ここで $L^2-\overline L^2=(L+\overline L)(L-\overline L)=-\dfrac{\sqrt3}3i$ であり、$\overline ab$ の虚部を $y$ とすると $\overline ab-a\overline b=2yi$ であるから　$D=\dfrac{2\sqrt3}3y$<br>"
         r"一方、C（原点），A，B はこの順に反時計回りに並ぶから、$\theta=\angle\mathrm{ACB}$（$0<\theta<\pi$）として $\dfrac ba=\dfrac{|b|}{|a|}(\cos\theta+i\sin\theta)$，よって $\overline ab=|a|^2\cdot\dfrac ba=|a||b|(\cos\theta+i\sin\theta)$ となり、$y=|a||b|\sin\theta=2S$。<br>"
         r"ゆえに $D=\dfrac{4\sqrt3}3S=\dfrac4{\sqrt3}S$ で　$\triangle\mathrm{PQR}-\triangle\mathrm{P'Q'R'}=\dfrac{\sqrt3}4D=S=\triangle\mathrm{ABC}$",
  "note": r"(1) は<b>ナポレオンの定理</b>とよばれる。$p+q+r=a+b+c$ であるから、$\triangle\mathrm{PQR}$ の重心は $\triangle\mathrm{ABC}$ の重心と一致する（$\mathrm{P'}$，$\mathrm{Q'}$，$\mathrm{R'}$ についても同様）。$\triangle\mathrm{ABC}$ が正三角形のときは、内側の3つの正三角形はどれも $\triangle\mathrm{ABC}$ 自身なので $\mathrm{P'}$，$\mathrm{Q'}$，$\mathrm{R'}$ は1点に一致し、$\triangle\mathrm{PQR}$ の面積が $\triangle\mathrm{ABC}$ の面積に等しくなる。",
  "ex": r"$\triangle\mathrm{ABC}$ の外側に正三角形 BCD，CAE，ABF をつくる。$\mathrm{AD}=\mathrm{BE}=\mathrm{CF}$ であり、直線 AD と直線 BE のなす角は $\dfrac\pi3$ であることを示せ。",
  "exa": r"A，B，C を反時計回りに置き $\rho=\cos\dfrac\pi3+i\sin\dfrac\pi3$ とすると $d=b+\overline\rho(c-b)$，$e=c+\overline\rho(a-c)$。$1-\overline\rho=\rho$，$\overline\rho^{\,2}=-\rho$ を用いると $e-b=\left(\cos\dfrac23\pi+i\sin\dfrac23\pi\right)(d-a)$ となり、$\mathrm{BE}=\mathrm{AD}$，なす角は $\dfrac\pi3$。CF も同様。"},
]})


def _ccw():
    while True:
        a, b, c = [complex(random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(3)]
        cr = ((b - a).conjugate() * (c - a)).imag
        if cr > 0.3:
            return a, b, c


def _v5():
    a, b = 3 + 1j, 1 + 2j
    assert cl(RHO * a, (3 - 3**0.5) / 2 + (1 + 3 * 3**0.5) / 2 * 1j) and cl((1 - 1j) * a, 4 - 2j) and cl(b + 1j * (a - b), 2 + 4j)
    assert cl(2**0.5 * cmath.exp(-1j * math.pi / 4), 1 - 1j)
    a, b = 2 - 2j, -1 + 1j
    assert cl(cmath.exp(2j * math.pi / 3) * a, (-1 + 3**0.5) + (1 + 3**0.5) * 1j)
    assert cl(2 * cmath.exp(1j * math.pi / 6) * a, (2 * 3**0.5 + 2) + (2 - 2 * 3**0.5) * 1j) and cl(b - 1j * (a - b), -4 - 2j)
    A, B = 1 + 1j, 3 + 2j
    for g in [(4 - 3**0.5) / 2 + (3 + 2 * 3**0.5) / 2 * 1j, (4 + 3**0.5) / 2 + (3 - 2 * 3**0.5) / 2 * 1j]:
        assert cl(abs(g - A), abs(B - A)) and cl(abs(g - B), abs(B - A))
    A, B, C, D = 2 + 1j, 4 + 5j, 7j, -2 + 3j
    assert cl(D - A, 1j * (B - A)) and cl(C - D, B - A) and ((B - A).conjugate() * (D - A)).imag > 0
    A, B, C = 1 + 1j, 4 + 2j, 3 + 5j
    assert cl((C - A) / (B - A), 1 + 1j)
    av = symbols("a", real=True)
    w = expand((((av - 2) + 3 * I) * (2 + 2 * I)) / 8)
    assert Z(w - ((2 * av - 10) + (2 * av + 2) * I) / 8)
    assert solve(sim(w), av) == [-1] and solve(sre(w), av) == [5]
    A, B, C = 1 + 2j, 2 + 4j, -2 + 1j
    assert cl((C - A) / (B - A), -1 + 1j) and abs(cmath.phase((C - A) / (B - A)) - 3 * math.pi / 4) < 1e-12
    w = expand((((av - 1) - 2 * I) / (2 + 2 * I)))
    assert solve(sim(w), av) == [-1] and solve(sre(w), av) == [3]
    # 形状決定
    al, be, ga, uu, vv = symbols("alpha beta gamma u v")
    E = al**2 + be**2 + ga**2 - al * be - be * ga - ga * al
    assert Z(E.subs({be: al + uu, ga: al + vv}) - (uu**2 - uu * vv + vv**2))
    om = Rational(-1, 2) + sqrt(3) / 2 * I
    assert Z((al + be * om + ga * om**2) * (al + be * om**2 + ga * om) - E)
    assert Z((al - be)**2 + (be - ga)**2 + (ga - al)**2 - 2 * E)
    assert Z((2 * al**2 + be**2 + ga**2 - 2 * al * be - 2 * al * ga) - ((be - al)**2 + (ga - al)**2))
    A, B, C = 0, 1, 1 + 3**0.5 * 1j
    ang = lambda P, Q, R: abs(cmath.phase((R - P) / (Q - P)))
    assert cl(C - A, (1 + 3**0.5 * 1j) * (B - A))
    assert abs(ang(A, B, C) - math.pi / 3) < 1e-12 and abs(ang(B, C, A) - math.pi / 2) < 1e-12 and abs(ang(C, A, B) - math.pi / 6) < 1e-12
    # 外心原点の垂心
    a1, b1, c1 = symbols("a b c")
    assert Z((a1 + b1) * (b1 + c1) * (c1 + a1) - ((a1 + b1 + c1) * (a1 * b1 + b1 * c1 + c1 * a1) - a1 * b1 * c1))
    for _ in range(200):
        r = random.uniform(0.5, 3)
        al_, be_, ga_ = [r * runit() for _ in range(3)]
        h = al_ + be_ + ga_
        assert abs(((h - al_) / (ga_ - be_)).real) < 1e-7 and abs(((h - be_) / (al_ - ga_)).real) < 1e-7
        assert cl(h.conjugate(), r * r * (al_ * be_ + be_ * ga_ + ga_ * al_) / (al_ * be_ * ga_), 1e-8)
        assert abs(abs(al_ - be_ + 0j)**2 - (2 * r * r - (al_ * be_.conjugate() + al_.conjugate() * be_).real)) < 1e-8
        al_, be_, ga_ = r * runit(), None, r * runit()
        be_ = -al_
        assert abs(abs(al_ + be_ + ga_) - r) < 1e-9
        al_ = r * runit(); be_ = al_ * cmath.exp(2j * math.pi / 3); ga_ = -(al_ + be_)
        assert abs(abs(ga_) - r) < 1e-9 and abs(abs(al_ - be_)**2 - 3 * r * r) < 1e-8
    # 正方形・ナポレオン
    cross = lambda P, Q, R: ((Q - P).conjugate() * (R - P)).imag
    for _ in range(300):
        a, b, c = _ccw()
        bb, cc = b - a, c - a
        e, g, m = -1j * bb, 1j * cc, (bb + cc) / 2
        assert cl(g - e, 2j * m) and cross(0, bb, e) * cross(0, bb, cc) < 0 and cross(0, cc, g) * cross(0, cc, bb) < 0
        p, q = (1 - 1j) * bb / 2, (1 + 1j) * cc / 2
        assert cl(p, (bb + e) / 2) and cl(q, (cc + g) / 2) and cl(p - m, 1j * (q - m))
        assert cl(1j * e, bb) and abs(abs(cross(0, e, g)) - abs(cross(0, bb, cc))) < 1e-9
        P, Q, R = napoleon(a, b, c)
        assert cross(b, c, P) * cross(b, c, a) < 0 and cross(c, a, Q) * cross(c, a, b) < 0
        assert cl(R - P, RHO * (Q - P)) and cl(P + Q + R, a + b + c)
        P2, Q2, R2 = napoleon(a, b, c, inner=True)
        assert cross(b, c, P2) * cross(b, c, a) > 0
        assert cl(R2 - P2, RHO.conjugate() * (Q2 - P2))
        S = cross(a, b, c) / 2
        assert abs(3**0.5 / 4 * (abs(Q - P)**2 - abs(Q2 - P2)**2) - S) < 1e-9
        d, e2, f2 = b + RHO.conjugate() * (c - b), c + RHO.conjugate() * (a - c), a + RHO.conjugate() * (b - a)
        assert cl(e2 - b, cmath.exp(2j * math.pi / 3) * (d - a)) and cl(f2 - c, cmath.exp(2j * math.pi / 3) * (e2 - b))
        assert abs(abs(d - a) - abs(e2 - b)) < 1e-9 and abs(abs(d - a) - abs(f2 - c)) < 1e-9
    L = Rational(1, 2) - sqrt(3) / 6 * I; Lb = conjugate(L); rho = (1 + sqrt(3) * I) / 2
    assert Z(rho * L - Lb) and Z(rho * Lb - sqrt(3) / 3 * I) and Z(rho * sqrt(3) / 3 * I + L) and Z(1 - L - Lb) and Z(1 - 2 * L - sqrt(3) / 3 * I)
    assert Z(L - Lb + sqrt(3) / 3 * I) and Z(L * Lb - Rational(1, 3)) and Z(L**2 - Lb**2 + sqrt(3) / 3 * I)
    assert Z(L - (cos(-pi / 6) + I * sin(-pi / 6)) / sqrt(3))
    a1, b1, c1 = symbols("a b c")
    p_, q_, r_ = b1 + L * (c1 - b1), c1 + L * (a1 - c1), a1 + L * (b1 - a1)
    assert Z(q_ - p_ - (L * a1 - Lb * b1 + sqrt(3) / 3 * I * c1)) and Z(r_ - p_ - (Lb * a1 - sqrt(3) / 3 * I * b1 - L * c1))
    p_, q_, r_ = b1 + Lb * (c1 - b1), c1 + Lb * (a1 - c1), a1 + Lb * (b1 - a1)
    assert Z(q_ - p_ - (Lb * a1 - L * b1 - sqrt(3) / 3 * I * c1)) and Z(r_ - p_ - (L * a1 + sqrt(3) / 3 * I * b1 - Lb * c1))
    rb = conjugate(rho)
    assert Z(1 - rb - rho) and Z(rb**2 + rho)
    # 正三角形 ABC のとき内側の重心は一致
    a, b, c = 0, 1, RHO
    P2, Q2, R2 = napoleon(a, b, c, inner=True)
    assert cl(P2, Q2) and cl(Q2, R2)


# ---------------------------------------------------------------- 節6
def fig_quadrant():
    f = Fig(-1.45, 2.65, -0.6, 2.2, 38)
    f.poly([0, 2.45, complex(2.45, 2.05), 2.05j], fill=FILL, col="none", w=0)
    f.axes(-1.4, 2.6, -0.55, 2.15, lx="x", ly="y")
    f.line(0, 2.45, col=BLUE, w=2.0); f.line(0, 2.05j, col=BLUE, w=2.0)
    f.dot(1, r=1.6); f.dot(1j, r=1.6)
    f.text(1, "1", -3, 13); f.text(1j, "i", -9, 4, it=True)
    f.circle(-1, 0.06, col="#222", w=1.0, fill="#fff"); f.text(-1, "−1", -8, 13)
    f.text(complex(1.2, 1.1), "x≧0, y≧0", -26, 4, size=10, it=True)
    return f.svg()


def fig_halfellipse():
    f = Fig(-3.0, 3.1, -0.45, 1.95, 36)
    a, b = 2.5, 1.5
    arc = [complex(a * math.cos(math.pi * k / 60), b * math.sin(math.pi * k / 60)) for k in range(61)]
    f.poly(arc, fill=FILL, col=BLUE, w=1.4)
    for r in (1.3, 1.6):
        f.pline([complex((r + 1 / r) * math.cos(math.pi * k / 60), (r - 1 / r) * math.sin(math.pi * k / 60)) for k in range(61)],
                col=GRAY, w=0.8, dash="3 2")
    f.axes(-2.95, 3.0, -0.4, 1.9)
    f.line(-2.5, 2.5, col=BLUE, w=1.8)
    for x in (-2, 2):
        f.dot(x, col=RED, r=2.0)
    f.text(2, "2", -3, 13); f.text(-2, "−2", -7, 13)
    f.text(2.5, "5/2", -2, 13, size=10); f.text(-2.5, "−5/2", -16, 13, size=10)
    f.text(1.5j, "3/2", 3, -4, size=10)
    return f.svg()


SEC.append({"title": "方程式の表す図形と軌跡",
"base": r"""・$|z-\alpha|=r$：点 $\alpha$ を中心とする半径 $r$ の円　　$|z-\alpha|=|z-\beta|$：2点 $\alpha,\ \beta$ を結ぶ線分の垂直二等分線<br>
・$|z-\alpha|=k|z-\beta|$（$k>0$，$k\neq1$）：2点 $\alpha,\ \beta$ を $k:1$ に内分する点と外分する点を直径の両端とする円（アポロニウスの円）<br>
・$z\overline{z}+\overline{\beta}z+\beta\overline{z}+c=0$（$c$ は実数）は $(z+\beta)(\overline z+\overline\beta)=\beta\overline\beta-c$，すなわち $|z+\beta|^2=|\beta|^2-c$ と変形できる<br>
・$w=f(z)$ の描く図形：$z$ を $w$ で表し（$z=g(w)$），$z$ の満たす条件に代入して $w$ の条件を求める。$w$ がとり得ない値（除外点）に注意し、逆に条件を満たす $w$ がすべて実際にとれることを確かめる""",
"items": [
 {"lv": 1, "title": "方程式の表す図形（円・垂直二等分線）",
  "q": r"次の方程式を満たす点 $z$ 全体は、どのような図形か。<br>(1) $|z-2i|=3$　(2) $|z-1|=|z+i|$　(3) $|2z-1+i|=4$",
  "hint": r"$|z-\alpha|=r$ は点 $\alpha$ からの距離が $r$，$|z-\alpha|=|z-\beta|$ は2点 $\alpha,\ \beta$ から等距離。(3) は両辺を $2$ で割って $|z-\alpha|$ の形にする。",
  "sol": r"(1) 点 $2i$ からの距離が $3$ である点全体であるから、<b>点 $2i$ を中心とする半径 $3$ の円</b><br>"
         r"(2) $|z-1|=|z-(-i)|$ より、2点 $1,\ -i$ から等距離にある点全体で、<b>2点 $1,\ -i$ を結ぶ線分の垂直二等分線</b>（直線 $y=-x$）<br>"
         r"(3) $|2z-1+i|=2\left|z-\dfrac{1-i}2\right|$ であるから $\left|z-\dfrac{1-i}2\right|=2$。よって <b>点 $\dfrac{1-i}2$ を中心とする半径 $2$ の円</b>",
  "note": r"(2) は $z=x+yi$ とおくと $(x-1)^2+y^2=x^2+(y+1)^2$ より $y=-x$ となる。図形の意味から直接読み取るのが速いが、迷ったら $x,\ y$ で表して確かめるとよい。",
  "ex": r"次の方程式を満たす点 $z$ 全体はどのような図形か。(1) $|z+3-i|=2$　(2) $|z-3|=|z-i|$　(3) $|3z+6i|=6$",
  "exa": r"(1) 点 $-3+i$ を中心とする半径 $2$ の円　(2) 2点 $3,\ i$ を結ぶ線分の垂直二等分線（直線 $y=3x-4$）　(3) 点 $-2i$ を中心とする半径 $2$ の円"},
 {"lv": 2, "title": r"アポロニウスの円・$z\overline z$ を含む方程式",
  "q": r"次の方程式を満たす点 $z$ 全体は、どのような図形か。<br>(1) $|z-3|=2|z|$　(2) $z\overline z+(2+i)z+(2-i)\overline z+1=0$",
  "hint": r"(1) 両辺を2乗して $|z|^2=z\overline z$ で展開し、$|z-\alpha|^2=k$ の形に直す。(2) $(z+\beta)(\overline z+\overline\beta)=z\overline z+\overline\beta z+\beta\overline z+\beta\overline\beta$ を利用する。",
  "sol": r"(1) 両辺を2乗して $|z-3|^2=4|z|^2$，すなわち $(z-3)(\overline z-3)=4z\overline z$<br>"
         r"　展開して整理すると $3z\overline z+3z+3\overline z-9=0$，よって $z\overline z+z+\overline z-3=0$<br>"
         r"　$(z+1)(\overline z+1)=4$ より $|z+1|^2=4$，$|z+1|=2$。よって <b>点 $-1$ を中心とする半径 $2$ の円</b><br>"
         r"(2) $(z+2-i)(\overline z+2+i)=z\overline z+(2+i)z+(2-i)\overline z+5$ であるから、方程式は<br>"
         r"　$(z+2-i)(\overline z+2+i)=4$，すなわち $|z+2-i|^2=4$ と変形できる。<br>"
         r"　よって $|z-(-2+i)|=2$ で、<b>点 $-2+i$ を中心とする半径 $2$ の円</b>",
  "note": r"(1) は2点 $3,\ 0$ からの距離の比が $2:1$ である点の軌跡（アポロニウスの円）である。2点を結ぶ線分を $2:1$ に内分する点 $1$ と外分する点 $-3$ を直径の両端とする円になっていることが確かめられる。",
  "ex": r"次の方程式を満たす点 $z$ 全体はどのような図形か。(1) $|z-4i|=3|z|$　(2) $z\overline z-(1+3i)z-(1-3i)\overline z+6=0$",
  "exa": r"(1) 点 $-\dfrac12i$ を中心とする半径 $\dfrac32$ の円　(2) 点 $1-3i$ を中心とする半径 $2$ の円"},
 {"lv": 3, "title": r"$w=f(z)$ の描く図形（1次分数式）",
  "q": r"点 $z$ が原点を中心とする半径 $2$ の円周上を動くとき、$w=\dfrac{z+1}{z-1}$ で表される点 $w$ はどのような図形を描くか。",
  "hint": r"$z$ について解いて $z=\dfrac{w+1}{w-1}$ とし、$z$ の満たす条件 $|z|=2$ に代入する。$w$ がとり得ない値（ここでは $w=1$）に注意する。",
  "sol": r"$|z|=2$ より $z\neq1$。$w=\dfrac{z+1}{z-1}$ より $w(z-1)=z+1$，すなわち $(w-1)z=w+1$。<br>"
         r"$w=1$ とすると $0=2$ となり不合理なので $w\neq1$ で　$z=\dfrac{w+1}{w-1}$<br>"
         r"$|z|=2$ に代入すると $\dfrac{|w+1|}{|w-1|}=2$ より $|w+1|=2|w-1|$。両辺を2乗して<br>"
         r"　$(w+1)(\overline w+1)=4(w-1)(\overline w-1)$　　$w\overline w+w+\overline w+1=4w\overline w-4w-4\overline w+4$<br>"
         r"　$3w\overline w-5w-5\overline w+3=0$　すなわち　$w\overline w-\dfrac53w-\dfrac53\overline w+1=0$<br>"
         r"よって $\left(w-\dfrac53\right)\left(\overline w-\dfrac53\right)=\dfrac{25}9-1=\dfrac{16}9$，$\left|w-\dfrac53\right|=\dfrac43$<br>"
         r"この円は点 $1$ を通らない（$\left|1-\dfrac53\right|=\dfrac23\neq\dfrac43$）。逆に、この円周上の点 $w$ に対して $z=\dfrac{w+1}{w-1}$ とおくと $|z|=2$ であるから、求める図形は<br>"
         r"　<b>点 $\dfrac53$ を中心とする半径 $\dfrac43$ の円</b>",
  "note": r"1次分数式 $w=\dfrac{az+b}{cz+d}$ によって、円や直線は円または直線に移る。$z$ の動く円周上に分母を $0$ にする点があるときは、像が直線になる。たとえば $|z|=1$，$z\neq1$ のとき、$|w+1|=|w-1|$ より $w=\dfrac{z+1}{z-1}$ は虚軸全体を描く。",
  "ex": r"点 $z$ が虚軸上を動くとき、$w=\dfrac{z+1}{z-1}$ で表される点 $w$ はどのような図形を描くか。",
  "exa": r"原点を中心とする半径 $1$ の円（ただし点 $1$ を除く）"},
 {"lv": 4, "title": "不等式で表される領域の像",
  "q": r"複素数 $z$ が、$|z|\leqq1$，$z$ の虚部が $0$ 以上，$z\neq1$ を満たしながら動くとき、$w=\dfrac{1+z}{1-z}$ で表される点 $w$ の存在範囲を求め、図示せよ。",
  "hint": r"$z=\dfrac{w-1}{w+1}$ と逆に解き、$z$ についての条件を1つずつ $w$ の条件に言い換える。虚部は分母を実数化して調べる。",
  "sol": fig_quadrant() +
         r"$w(1-z)=1+z$ より $(w+1)z=w-1$。$w=-1$ とすると $0=-2$ で不合理だから $w\neq-1$ で　$z=\dfrac{w-1}{w+1}$<br>"
         r"$w=x+yi$（$x,\ y$ は実数）とおく。<br>"
         r"・$|z|\leqq1\iff|w-1|\leqq|w+1|\iff(w-1)(\overline w-1)\leqq(w+1)(\overline w+1)$<br>"
         r"　$\iff-(w+\overline w)\leqq w+\overline w\iff w+\overline w\geqq0\iff x\geqq0$<br>"
         r"・$z=\dfrac{(w-1)(\overline w+1)}{|w+1|^2}=\dfrac{|w|^2+(w-\overline w)-1}{|w+1|^2}$ で、$w-\overline w=2yi$ であるから、$z$ の虚部は $\dfrac{2y}{|w+1|^2}$。<br>"
         r"　よって　$z$ の虚部が $0$ 以上 $\iff y\geqq0$<br>"
         r"また、$z=\dfrac{w-1}{w+1}=1$ となる $w$ はない。逆に、$x\geqq0$，$y\geqq0$ である任意の $w$ に対して $z=\dfrac{w-1}{w+1}$ は3つの条件を満たし、$w=\dfrac{1+z}{1-z}$ となる。<br>"
         r"以上より、求める範囲は　$\boldsymbol{x\geqq0,\ y\geqq0}$（$w$ の実部・虚部がともに $0$ 以上）で、<b>右図の色のついた部分（境界を含む）</b>である。",
  "note": r"境界の対応を見ると、半円周（$|z|=1$，虚部が $0$ 以上，$z\neq1$）は虚軸の $y\geqq0$ の部分へ、直径の部分（$-1\leqq z<1$ の実数）は実軸の $x\geqq0$ の部分へ移る。たとえば $z=-1$ は $w=0$ に、$z=i$ は $w=i$ に対応する。",
  "ex": r"複素数 $z$ が、実部が正かつ虚部が正という条件を満たしながら動くとき、$w=\dfrac{z-1}{z+1}$ で表される点 $w$ の存在範囲を求めよ。",
  "exa": r"$|w|<1$ かつ $w$ の虚部が正（原点を中心とする半径 $1$ の円の内部のうち実軸より上の部分。境界を含まない）"},
 {"lv": 5, "title": r"像の図形（$w=z+\dfrac1z$ による半円環の像）",
  "q": r"複素数 $z$ が $1\leqq|z|\leqq2$ を満たし、かつ $z$ の虚部が $0$ 以上であるように動くとき、$w=z+\dfrac1z$ で表される点 $w$ の存在範囲を求め、図示せよ。",
  "hint": r"$|z|=r$ を固定すると、$|w-2|=\dfrac{|z-1|^2}{|z|}$，$|w+2|=\dfrac{|z+1|^2}{|z|}$ より $|w-2|+|w+2|=2\left(r+\dfrac1r\right)$ となり、$w$ は2点 $\pm2$ を焦点とする楕円上にある。逆に、条件を満たす $w$ が実際にとれることは、$z$ の2次方程式 $z^2-wz+1=0$ の解で確かめる。",
  "sol": fig_halfellipse() +
         r"$z=r(\cos\theta+i\sin\theta)$（$1\leqq r\leqq2$，$0\leqq\theta\leqq\pi$）とおく。<br>"
         r"<b>[1] $w$ の満たす条件</b>　$w-2=\dfrac{z^2-2z+1}z=\dfrac{(z-1)^2}z$，$w+2=\dfrac{(z+1)^2}z$ であり、$|z-1|^2+|z+1|^2=2(|z|^2+1)$ であるから<br>"
         r"　$|w-2|+|w+2|=\dfrac{|z-1|^2+|z+1|^2}{|z|}=\dfrac{2(r^2+1)}{r}=2\left(r+\dfrac1r\right)$ …①<br>"
         r"また　$w=r(\cos\theta+i\sin\theta)+\dfrac1r(\cos\theta-i\sin\theta)=\left(r+\dfrac1r\right)\cos\theta+i\left(r-\dfrac1r\right)\sin\theta$ …②<br>"
         r"$r+\dfrac1r$ は $r\geqq1$ で増加するから $2\leqq r+\dfrac1r\leqq\dfrac52$。よって ① より $|w-2|+|w+2|\leqq5$。また ② より $w$ の虚部 $\left(r-\dfrac1r\right)\sin\theta$ は $0$ 以上である。<br>"
         r"<b>[2] 逆の確認</b>　$w$ が「$|w-2|+|w+2|\leqq5$ かつ虚部が $0$ 以上」を満たすとする。$z$ の2次方程式 $z^2-wz+1=0$ の2解 $z_1,\ z_2$ は $z_1z_2=1$ を満たすから、どちらも $0$ でなく $z_k+\dfrac1{z_k}=w$ であり、$|z_1||z_2|=1$ より $|z_1|\geqq1$ としてよい。<br>"
         r"$z_1=r(\cos\theta_1+i\sin\theta_1)$ とすると、① より $2\left(r+\dfrac1r\right)\leqq5$，$2r^2-5r+2\leqq0$，$(2r-1)(r-2)\leqq0$ で、$r\geqq1$ と合わせて $1\leqq r\leqq2$。<br>"
         r"・$r>1$ のとき：② と同様に $w$ の虚部は $\left(r-\dfrac1r\right)\sin\theta_1$ で、これが $0$ 以上かつ $r-\dfrac1r>0$ より $\sin\theta_1\geqq0$。すなわち $z_1$ の虚部は $0$ 以上。<br>"
         r"・$r=1$ のとき：$z_2=\dfrac1{z_1}=\overline{z_1}$ も $|z_2|=1$ で、$z_1,\ z_2$ の少なくとも一方は虚部が $0$ 以上。<br>"
         r"いずれの場合も、条件を満たす $z$ で $z+\dfrac1z=w$ となるものが存在する。<br>"
         r"<b>[3] 図示</b>　2点 $2,\ -2$ からの距離の和が $5$ である点の軌跡は、焦点 $(\pm2,\ 0)$，長軸の長さ $5$ の楕円で、短軸の長さの半分は $\sqrt{\left(\frac52\right)^2-2^2}=\dfrac32$ である。<br>"
         r"よって $w=x+yi$ の存在範囲は　$\boldsymbol{\dfrac{4x^2}{25}+\dfrac{4y^2}9\leqq1,\ y\geqq0}$　で、<b>右図の色のついた部分（境界を含む）</b>である。",
  "note": r"$r$ を固定すると ② は楕円 $\dfrac{x^2}{\left(r+\frac1r\right)^2}+\dfrac{y^2}{\left(r-\frac1r\right)^2}=1$ の上半分（$r=1$ のときは線分 $-2\leqq x\leqq2$）を表し、$\left(r+\frac1r\right)^2-\left(r-\frac1r\right)^2=4$ より焦点はつねに $\pm2$ である（図の点線）。焦点を共有する楕円は互いに交わらず、$r$ が増えると外側へ広がるので、これらが範囲を埋めつくす。① はこの事実を一挙に示している。",
  "ex": r"複素数 $z$ が $|z|\geqq2$ を満たしながら動くとき、$w=z+\dfrac1z$ で表される点 $w$ の存在範囲を求めよ。",
  "exa": r"$w=x+yi$ として　$\dfrac{4x^2}{25}+\dfrac{4y^2}9\geqq1$（楕円の周および外部）"},
]})


def _v6():
    x, y = symbols("x y", real=True)
    zz = x + I * y

    def A2(e):
        return expand(e * conjugate(e))
    assert Z(A2(zz - 1) - A2(zz + I) - (-2 * x - 2 * y))
    assert Z(A2(zz - 3) - A2(zz - I) - (-6 * x + 2 * y + 8))
    assert Z(A2(2 * zz - 1 + I) - 4 * A2(zz - (1 - I) / 2)) and Z(A2(3 * zz + 6 * I) - 9 * A2(zz + 2 * I))
    assert Z(A2(zz - 3) - 4 * A2(zz) + 3 * ((x + 1)**2 + y**2 - 4))
    assert Z(zz * conjugate(zz) + (2 + I) * zz + (2 - I) * conjugate(zz) + 1 - ((x + 2)**2 + (y - 1)**2 - 4))
    assert Z(A2(zz - 4 * I) - 9 * A2(zz) + 8 * (x**2 + (y + Rational(1, 2))**2 - Rational(9, 4)))
    assert Z(zz * conjugate(zz) - (1 + 3 * I) * zz - (1 - 3 * I) * conjugate(zz) + 6 - ((x - 1)**2 + (y + 3)**2 - 4))
    for k in range(200):
        z = 2 * cmath.exp(2j * math.pi * k / 200)
        w = (z + 1) / (z - 1)
        assert abs(abs(w - 5 / 3) - 4 / 3) < 1e-9
        w = 5 / 3 + 4 / 3 * cmath.exp(2j * math.pi * k / 200)
        assert abs(abs((w + 1) / (w - 1)) - 2) < 1e-9
        t = math.tan(math.pi * (k + 0.5) / 200 - math.pi / 2)
        w = (1j * t + 1) / (1j * t - 1)
        assert abs(abs(w) - 1) < 1e-9 and abs(w - 1) > 1e-6
        w = cmath.exp(1j * (2 * math.pi * (k + 0.5) / 200))
        assert abs(((w + 1) / (w - 1)).real) < 1e-9
        z = cmath.exp(1j * (2 * math.pi * (k + 0.5) / 200))
        assert abs(((z + 1) / (z - 1)).real) < 1e-9
    # 領域の像
    for _ in range(3000):
        z = cmath.rect(random.uniform(0, 1), random.uniform(0, math.pi))
        if abs(z - 1) < 1e-6:
            continue
        w = (1 + z) / (1 - z)
        assert w.real >= -1e-9 and w.imag >= -1e-9
        w = complex(random.uniform(0, 50), random.uniform(0, 50))
        z = (w - 1) / (w + 1)
        assert abs(z) <= 1 + 1e-12 and z.imag >= -1e-12 and cl((1 + z) / (1 - z), w, 1e-7)
        w = complex(random.uniform(-5, 5), random.uniform(-5, 5))
        if w.real < -1e-3 or w.imag < -1e-3:
            z = (w - 1) / (w + 1)
            assert abs(z) > 1 or z.imag < 0
        z = complex(random.uniform(1e-3, 9), random.uniform(1e-3, 9))
        w = (z - 1) / (z + 1)
        assert abs(w) < 1 and w.imag > 0
        w = cmath.rect(random.uniform(0, 0.999), random.uniform(1e-3, math.pi - 1e-3))
        z = (1 + w) / (1 - w)
        assert z.real > 0 and z.imag > 0
    assert cl((1 + 1j) / (1 - 1j), 1j)
    # w = z + 1/z
    inside = lambda w: 4 * w.real**2 / 25 + 4 * w.imag**2 / 9 <= 1 + 1e-9
    for _ in range(3000):
        r, t = random.uniform(1, 2), random.uniform(0, math.pi)
        z = cmath.rect(r, t)
        w = z + 1 / z
        assert inside(w) and w.imag >= -1e-12
        assert abs(abs(w - 2) + abs(w + 2) - 2 * (r + 1 / r)) < 1e-9
        assert abs(abs(z - 1)**2 + abs(z + 1)**2 - 2 * (abs(z)**2 + 1)) < 1e-9
        w = complex(random.uniform(-2.6, 2.6), random.uniform(0, 1.6))
        roots = [(w + s * cmath.sqrt(w * w - 4)) / 2 for s in (1, -1)]
        ok = any(1 - 1e-9 <= abs(z) <= 2 + 1e-9 and z.imag >= -1e-9 for z in roots)
        assert ok == inside(w) or abs(4 * w.real**2 / 25 + 4 * w.imag**2 / 9 - 1) < 1e-6
        r = random.uniform(2, 20); z = cmath.rect(r, random.uniform(0, 2 * math.pi)); w = z + 1 / z
        assert 4 * w.real**2 / 25 + 4 * w.imag**2 / 9 >= 1 - 1e-9
        w = complex(random.uniform(-30, 30), random.uniform(-30, 30))
        roots = [(w + s * cmath.sqrt(w * w - 4)) / 2 for s in (1, -1)]
        assert any(abs(z) >= 2 - 1e-9 for z in roots) == (4 * w.real**2 / 25 + 4 * w.imag**2 / 9 >= 1 - 1e-9) or \
            abs(4 * w.real**2 / 25 + 4 * w.imag**2 / 9 - 1) < 1e-6


# ---------------------------------------------------------------- 節7
def fig_dist():
    C, A = 1 + 1j, 4 + 5j
    u = (A - C) / abs(A - C)
    f = Fig(-0.45, 4.75, -0.4, 5.45, 25)
    f.axes(-0.4, 4.7, -0.35, 5.4)
    f.circle(C, 1, col=BLUE, w=1.3)
    f.line(C - u, A, col=GRAY, w=0.9, dash="3 2")
    f.dot(C, r=1.8); f.dot(A, r=2.0)
    f.dot(C - u, col=RED); f.dot(C + u, col=RED)
    f.text(C, "1+i", 5, 12); f.text(A, "4+5i", -36, 4)
    return f.svg()


def fig_tangent():
    C = complex(3**0.5, 1)
    f = Fig(-0.35, 3.25, -0.4, 2.4, 44)
    f.axes(-0.3, 3.2, -0.35, 2.35)
    f.circle(C, 1, col=BLUE, w=1.3)
    T1, T2 = complex(3**0.5, 0), complex(3**0.5 / 2, 1.5)
    f.line(0, 3.1, col=RED, w=1.3); f.line(0, T2 * 1.45, col=RED, w=1.3)
    f.line(0, 1.5 * C, col=GRAY, w=0.9, dash="3 2"); f.line(C, T2, col=GRAY, w=0.8)
    for z in (C, T1, T2, C / 2, 1.5 * C):
        f.dot(z, r=1.8)
    f.text(C, "C", 3, -4); f.text(T1, "√3", -6, 13); f.text(T2, "T", -12, -1)
    return f.svg()


TBL36 = (r'<table><tr><th>$t$</th><td>$-1$</td><td>$\cdots$</td><td>$-\frac12$</td><td>$\cdots$</td><td>$\frac23$</td><td>$\cdots$</td><td>$1$</td></tr>'
         r'<tr><th>$g^{\prime}(t)$</th><td></td><td>$+$</td><td>$0$</td><td>$-$</td><td>$0$</td><td>$+$</td><td></td></tr>'
         r'<tr><th>$g(t)$</th><td>$4$</td><td>$\nearrow$</td><td>$13$</td><td>$\searrow$</td><td>$\frac8{27}$</td><td>$\nearrow$</td><td>$4$</td></tr></table>')

SEC.append({"title": "最大・最小",
"base": r"""・三角不等式：$\big||\alpha|-|\beta|\big|\leqq|\alpha+\beta|\leqq|\alpha|+|\beta|$（$\beta$ を $-\beta$ にかえても成り立つ）<br>
・円 $|z-\gamma|=r$ 上の点 $z$ と、円の外部の点 $\alpha$ との距離 $|z-\alpha|$ は、直線 $\gamma\alpha$ と円の交点で最大値 $|\alpha-\gamma|+r$，最小値 $|\alpha-\gamma|-r$ をとる<br>
・偏角の範囲は、原点から円に引いた接線を考える<br>
・$|z|=1$ のときの $|f(z)|$ の最大・最小：$|f(z)|^2=f(z)\overline{f(z)}$ を $\overline z=\dfrac1z$ で整理し、$z^k+\overline z^{\,k}=2\cos k\theta$ により $\cos\theta$ の関数にする""",
"items": [
 {"lv": 2, "title": "円周上の点と定点の距離の最大・最小",
  "q": r"複素数 $z$ が $|z-1-i|=1$ を満たすとき、$|z-4-5i|$ の最大値と最小値を求めよ。また、そのときの $z$ を求めよ。",
  "hint": r"$z$ は点 $1+i$ を中心とする半径 $1$ の円周上を動く。$|z-4-5i|$ は点 $4+5i$ との距離であるから、円の中心と点 $4+5i$ を結ぶ直線と円との交点で最大・最小となる。式では三角不等式で示せる。",
  "sol": fig_dist() +
         r"点 $z$ は中心 $1+i$，半径 $1$ の円周上にあり、$|(4+5i)-(1+i)|=|3+4i|=5$ である。三角不等式より<br>"
         r"　$|z-(4+5i)|=|\{z-(1+i)\}-(3+4i)|\leqq|z-(1+i)|+|3+4i|=1+5=6$<br>"
         r"　$|z-(4+5i)|\geqq|3+4i|-|z-(1+i)|=5-1=4$<br>"
         r"等号は、$z-(1+i)$ が $3+4i$ と逆向き（最大）または同じ向き（最小）のときに成り立つ。すなわち<br>"
         r"　最大：$z=(1+i)-\dfrac{3+4i}5=\dfrac25+\dfrac15i$，　最小：$z=(1+i)+\dfrac{3+4i}5=\dfrac85+\dfrac95i$<br>"
         r"よって　最大値 $\boldsymbol{6}$（$z=\dfrac25+\dfrac15i$），最小値 $\boldsymbol{4}$（$z=\dfrac85+\dfrac95i$）",
  "note": r"図形的には、円の中心と点 $4+5i$ を結ぶ直線と円の2つの交点で最大・最小となる（図の赤い点）。点が円の外部にあることを確認しておく。点が円の内部にあるときは、最小値は（半径）$-$（中心との距離）になる。",
  "ex": r"複素数 $z$ が $|z-2i|=2$ を満たすとき、$|z-6+6i|$ の最大値と最小値、およびそのときの $z$ を求めよ。",
  "exa": r"最大値 $12$（$z=-\dfrac65+\dfrac{18}5i$），最小値 $8$（$z=\dfrac65+\dfrac25i$）"},
 {"lv": 3, "title": "絶対値・偏角のとり得る値の範囲",
  "q": r"複素数 $z$ が $|z-\sqrt3-i|=1$ を満たすとき、$|z|$ の最大値と最小値、および $\arg z$ のとり得る値の範囲を求めよ。ただし $0\leqq\arg z<2\pi$ とする。",
  "hint": r"$|z|$ は原点との距離、$\arg z$ は原点から点 $z$ へ向かう半直線の向き。円の中心と原点を結ぶ直線、および原点から円に引いた接線を考える。",
  "sol": fig_tangent() +
         r"点 $z$ は中心 $\mathrm{C}(\sqrt3+i)$，半径 $1$ の円周上にある。$\mathrm{OC}=|\sqrt3+i|=2>1$ で、O は円の外部にある。<br>"
         r"<b>$|z|$ について</b>　$\mathrm{OC}-1\leqq|z|\leqq\mathrm{OC}+1$ で、等号は直線 OC と円の交点で成り立つ。よって<br>"
         r"　最大値 $\boldsymbol{3}$（$z=\dfrac32(\sqrt3+i)$），最小値 $\boldsymbol{1}$（$z=\dfrac12(\sqrt3+i)$）<br>"
         r"<b>$\arg z$ について</b>　原点から円に引いた接線の接点を T とすると、$\angle\mathrm{OTC}=\dfrac\pi2$，$\mathrm{CT}=1$，$\mathrm{OC}=2$ より $\angle\mathrm{COT}=\dfrac\pi6$。<br>"
         r"$\arg(\sqrt3+i)=\dfrac\pi6$ であるから、$\arg z$ は $\dfrac\pi6-\dfrac\pi6$ から $\dfrac\pi6+\dfrac\pi6$ までのすべての値をとる。よって<br>"
         r"　$\boldsymbol{0\leqq\arg z\leqq\dfrac\pi3}$<br>"
         r"（$\arg z=0$ となるのは $z=\sqrt3$，$\arg z=\dfrac\pi3$ となるのは $z=\dfrac{\sqrt3}2+\dfrac32i$ のとき）",
  "note": r"円周上の点の偏角は、原点から引いた2本の接線の間の範囲を動く。原点が円の内部にあるときは、偏角はすべての値をとる。",
  "ex": r"複素数 $z$ が $|z-2-2i|=\sqrt2$ を満たすとき、$|z|$ の最大値と最小値、および $\arg z$ のとり得る値の範囲を求めよ（$0\leqq\arg z<2\pi$）。",
  "exa": r"最大値 $3\sqrt2$，最小値 $\sqrt2$，$\dfrac\pi{12}\leqq\arg z\leqq\dfrac5{12}\pi$"},
 {"lv": 4, "title": r"$|z|=1$ のときの $|f(z)|$ の最大・最小",
  "q": r"複素数 $z$ が $|z|=1$ を満たしながら動くとき、$|z^3-z+2|$ の最大値と最小値を求めよ。",
  "hint": r"$|f(z)|^2=f(z)\overline{f(z)}$ とし、$z\overline z=1$ を用いて展開する。$z=\cos\theta+i\sin\theta$ とおくと $z^k+\overline z^{\,k}=2\cos k\theta$ で、$t=\cos\theta$ の3次関数になる（$-1\leqq t\leqq1$）。",
  "sol": r"$|z|=1$ より $z\overline z=1$。$z=\cos\theta+i\sin\theta$ とおくと、ド・モアブルの定理より $z^k+\overline z^{\,k}=2\cos k\theta$ である。<br>"
         r"$|z^3-z+2|^2=(z^3-z+2)(\overline z^{\,3}-\overline z+2)$<br>"
         r"$\phantom{|z^3-z+2|^2}=z^3\overline z^{\,3}-z^3\overline z+2z^3-z\overline z^{\,3}+z\overline z-2z+2\overline z^{\,3}-2\overline z+4$<br>"
         r"$\phantom{|z^3-z+2|^2}=6-(z^2+\overline z^{\,2})+2(z^3+\overline z^{\,3})-2(z+\overline z)=6-2\cos2\theta+4\cos3\theta-4\cos\theta$<br>"
         r"$t=\cos\theta$ とおくと、$\cos2\theta=2t^2-1$，$\cos3\theta=4t^3-3t$ より<br>"
         r"　$|z^3-z+2|^2=16t^3-4t^2-16t+8=g(t)$　（$-1\leqq t\leqq1$）<br>"
         r"$g'(t)=48t^2-8t-16=8(2t+1)(3t-2)$ より、増減表は次のようになる。" + TBL36 +
         r"よって $g(t)$ の最大値は $13$，最小値は $\dfrac8{27}$ であり、$|z^3-z+2|$ の<br>"
         r"　最大値 $\boldsymbol{\sqrt{13}}$（$z=-\dfrac12\pm\dfrac{\sqrt3}2i$ のとき），最小値 $\boldsymbol{\dfrac{2\sqrt6}9}$（$z=\dfrac23\pm\dfrac{\sqrt5}3i$ のとき）",
  "note": r"$|f(z)|$ の最大・最小は、2乗して $f(z)\overline{f(z)}$ を計算するのが基本である。$z^k+\overline z^{\,k}=2\cos k\theta$ により $\cos\theta$ の多項式になるが、$t=\cos\theta$ の範囲 $-1\leqq t\leqq1$ を忘れないこと。$f(z)$ が因数分解できるときは、$|f(z)|=|z-\alpha||z-\beta|\cdots$ と距離の積とみる方法もある（練習）。",
  "ex": r"複素数 $z$ が $|z|=1$ を満たしながら動くとき、$|z^3-3z+2|$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $3\sqrt3$（$z=-\dfrac12\pm\dfrac{\sqrt3}2i$），最小値 $0$（$z=1$）"},
 {"lv": 5, "title": r"単位円周上での多項式の値の評価（1 の $n$ 乗根の利用）",
  "q": r"$n$ を自然数とし、$P(z)=z^n+a_{n-1}z^{n-1}+\cdots+a_1z+a_0$（$a_0,\ a_1,\ \cdots,\ a_{n-1}$ は複素数）とする。<br>また、$N=n+1$，$\omega=\cos\dfrac{2\pi}N+i\sin\dfrac{2\pi}N$ とする。<br>"
       r"(1) $\displaystyle\sum_{k=0}^{n}\omega^{-nk}P(\omega^k)=n+1$ であることを示せ。<br>"
       r"(2) $|z|=1$ を満たす $z$ で、$|P(z)|\geqq1$ となるものが存在することを示せ。<br>"
       r"(3) $|z|=1$ を満たすすべての $z$ に対して $|P(z)|\leqq1$ が成り立つならば、$P(z)=z^n$ であることを示せ。",
  "hint": r"1 の $N$ 乗根について $\displaystyle\sum_{k=0}^{N-1}\omega^{mk}$ は $m$ が $N$ の倍数のときだけ $0$ でない。(2) は (1) と三角不等式。(3) は、変数を回転させた多項式 $\varepsilon^{-n}P(\varepsilon z)$（$|\varepsilon|=1$）にも (1) を使い、「絶対値が $1$ 以下の $N$ 個の複素数の和が $N$ ならば、すべて $1$ に等しい」ことを用いる。",
  "sol": r"$a_n=1$ とおくと $P(z)=\displaystyle\sum_{j=0}^na_jz^j$ である。<br>"
         r"(1) 整数 $m$ に対して、$m$ が $N$ の倍数のとき $\displaystyle\sum_{k=0}^{n}\omega^{mk}=N$，そうでないとき $\omega^m\neq1$ より $\displaystyle\sum_{k=0}^{n}\omega^{mk}=\dfrac{(\omega^{m})^N-1}{\omega^m-1}=0$ である。よって<br>"
         r"　$\displaystyle\sum_{k=0}^n\omega^{-nk}P(\omega^k)=\sum_{j=0}^na_j\sum_{k=0}^n\omega^{(j-n)k}$<br>"
         r"$j=n$ のとき内側の和は $N$。$0\leqq j\leqq n-1$ のとき $-n\leqq j-n\leqq-1$ で、$j-n$ は $N=n+1$ の倍数でないから内側の和は $0$。ゆえに<br>"
         r"　$\displaystyle\sum_{k=0}^n\omega^{-nk}P(\omega^k)=N\cdot a_n=n+1$<br>"
         r"(2) 仮に、$|z|=1$ を満たすすべての $z$ で $|P(z)|<1$ であるとすると、$|\omega^k|=1$ であるから、(1) と三角不等式より<br>"
         r"　$\displaystyle n+1=\left|\sum_{k=0}^n\omega^{-nk}P(\omega^k)\right|\leqq\sum_{k=0}^n|P(\omega^k)|<n+1$<br>"
         r"となり矛盾する。よって、$|z|=1$ かつ $|P(z)|\geqq1$ となる $z$ が存在する（$\omega^k$ のうち少なくとも1つがそうである）。<br>"
         r"(3) $\varepsilon$ を $|\varepsilon|=1$ である任意の複素数とし、$Q(z)=\varepsilon^{-n}P(\varepsilon z)$ とおく。$Q(z)$ の $z^n$ の係数は $\varepsilon^{-n}\cdot\varepsilon^n=1$ であるから、$Q$ も $P$ と同じ形の多項式で、(1) を $Q$ に用いると<br>"
         r"　$\displaystyle\sum_{k=0}^nc_k=n+1$　ただし　$c_k=\omega^{-nk}Q(\omega^k)=(\varepsilon\omega^k)^{-n}P(\varepsilon\omega^k)$<br>"
         r"$|\varepsilon\omega^k|=1$ であるから、仮定より $|c_k|=|P(\varepsilon\omega^k)|\leqq1$。$c_k$ の実部を $x_k$ とすると $x_k\leqq|c_k|\leqq1$ で、$\displaystyle\sum_{k=0}^nx_k=n+1$ であるから、すべての $k$ で $x_k=1$。<br>"
         r"このとき $1=x_k\leqq|c_k|\leqq1$ より $|c_k|=1$ で、$c_k$ の虚部は $0$，すなわち $c_k=1$。特に $k=0$ として $\varepsilon^{-n}P(\varepsilon)=1$，すなわち $P(\varepsilon)=\varepsilon^n$。<br>"
         r"$\varepsilon$ は単位円周上の任意の点であるから、$n-1$ 次以下の多項式 $P(z)-z^n$ は無数の $z$ で値 $0$ をとり、恒等的に $0$ である。よって $P(z)=z^n$。",
  "note": r"(2)，(3) をまとめると、$z^n$ の係数が $1$ の $n$ 次式 $P(z)$ について、単位円周上での $|P(z)|$ の最大値は $1$ 以上で、$1$ に等しくなるのは $P(z)=z^n$ のときに限る。調べる点を $z=\pm1$ だけにすると失敗する（たとえば $P(z)=z^2-1$ は $z=\pm1$ で $0$）。$n+1$ 個の点 $\omega^k$ での値に重み $\omega^{-nk}$ をつけて加えると $z^n$ 以外の項がすべて消える、という1の累乗根の性質がポイントである。",
  "ex": r"$a,\ b$ を複素数とし、$\omega=\dfrac{-1+\sqrt3\,i}2$，$P(z)=z^2+az+b$ とする。$P(1)+\omega P(\omega)+\omega^2P(\omega^2)$ を計算し、3つの値 $|P(1)|,\ |P(\omega)|,\ |P(\omega^2)|$ のうち少なくとも1つは $1$ 以上であることを示せ。",
  "exa": r"$P(1)+\omega P(\omega)+\omega^2P(\omega^2)=3+a(1+\omega+\omega^2)+b(1+\omega+\omega^2)=3$。三角不等式より3つの絶対値の和は $3$ 以上。"},
]})


def _v7():
    N = 20000
    U = [cmath.exp(2j * math.pi * k / N) for k in range(N)]
    d = [abs(1 + 1j + u - (4 + 5j)) for u in U]
    assert abs(max(d) - 6) < 1e-6 and abs(min(d) - 4) < 1e-6
    for z, v in [(0.4 + 0.2j, 6), (1.6 + 1.8j, 4)]:
        assert cl(abs(z - 1 - 1j), 1) and cl(abs(z - 4 - 5j), v)
    d = [abs(2j + 2 * u - (6 - 6j)) for u in U]
    assert abs(max(d) - 12) < 1e-6 and abs(min(d) - 8) < 1e-6
    for z, v in [(-1.2 + 3.6j, 12), (1.2 + 0.4j, 8)]:
        assert cl(abs(z - 2j), 2) and cl(abs(z - 6 + 6j), v)
    C = complex(3**0.5, 1)
    m = [abs(C + u) for u in U]; a = [cmath.phase(C + u) for u in U]
    assert abs(max(m) - 3) < 1e-6 and abs(min(m) - 1) < 1e-6
    assert min(a) > -1e-6 and abs(min(a)) < 1e-4 and abs(max(a) - math.pi / 3) < 1e-4 and max(a) < math.pi / 3 + 1e-6
    for z in [3**0.5, complex(3**0.5 / 2, 1.5), 1.5 * C, 0.5 * C]:
        assert cl(abs(z - C), 1)
    C = 2 + 2j
    m = [abs(C + 2**0.5 * u) for u in U]; a = [cmath.phase(C + 2**0.5 * u) for u in U]
    assert abs(max(m) - 3 * 2**0.5) < 1e-6 and abs(min(m) - 2**0.5) < 1e-6
    assert abs(min(a) - math.pi / 12) < 1e-4 and abs(max(a) - 5 * math.pi / 12) < 1e-4
    t = symbols("t")
    g = 16 * t**3 - 4 * t**2 - 16 * t + 8
    assert Z(g.diff(t) - 8 * (2 * t + 1) * (3 * t - 2))
    assert g.subs(t, -1) == 4 and g.subs(t, Rational(-1, 2)) == 13 and g.subs(t, Rational(2, 3)) == Rational(8, 27) and g.subs(t, 1) == 4
    v = [abs(u**3 - u + 2) for u in U]
    assert abs(max(v) - 13**0.5) < 1e-6 and abs(min(v) - 2 * 6**0.5 / 9) < 1e-6
    for u in U[:200]:
        c = u.real
        assert abs(abs(u**3 - u + 2)**2 - (16 * c**3 - 4 * c**2 - 16 * c + 8)) < 1e-9
    for z in [complex(-0.5, 3**0.5 / 2), complex(-0.5, -3**0.5 / 2)]:
        assert cl(abs(z**3 - z + 2), 13**0.5)
    for z in [complex(2 / 3, 5**0.5 / 3), complex(2 / 3, -5**0.5 / 3)]:
        assert cl(abs(z**3 - z + 2), 2 * 6**0.5 / 9) and cl(abs(z), 1)
    assert Z(Rational(8, 27) - (2 * sqrt(6) / 9)**2)
    v = [abs(u**3 - 3 * u + 2) for u in U]
    assert abs(max(v) - 3 * 3**0.5) < 1e-6 and min(v) < 1e-6
    zz = symbols("z")
    assert Z(zz**3 - 3 * zz + 2 - (zz - 1)**2 * (zz + 2))
    assert cl(abs(complex(-0.5, 3**0.5 / 2)**3 - 3 * complex(-0.5, 3**0.5 / 2) + 2), 3 * 3**0.5)
    # 単位円周上の多項式
    for n in range(1, 9):
        Nn = n + 1
        om = cmath.exp(2j * math.pi / Nn)
        for _ in range(30):
            co = [complex(random.gauss(0, 2), random.gauss(0, 2)) for _ in range(n)] + [1]
            P = lambda z: sum(c * z**j for j, c in enumerate(co))
            s = sum(om**(-n * k) * P(om**k) for k in range(Nn))
            assert cl(s, n + 1, 1e-7)
            assert max(abs(P(om**k)) for k in range(Nn)) >= 1 - 1e-12
            eps = runit()
            s = sum((eps * om**k)**(-n) * P(eps * om**k) for k in range(Nn))
            assert cl(s, n + 1, 1e-7)
    assert abs(1**2 - 1) == 0 and abs((-1)**2 - 1) == 0 and abs((1j)**2 - 1) == 2
    om = cmath.exp(2j * math.pi / 3)
    assert cl(om, complex(-0.5, 3**0.5 / 2))
    for _ in range(50):
        a_, b_ = complex(random.gauss(0, 3), random.gauss(0, 3)), complex(random.gauss(0, 3), random.gauss(0, 3))
        P = lambda z: z * z + a_ * z + b_
        assert cl(P(1) + om * P(om) + om**2 * P(om**2), 3, 1e-9)


CH = {"no": 20, "sections": SEC}


def verify():
    random.seed(20)
    for f in [_v1, _v2, _v3, _v4, _v5, _v6, _v7]:
        f()
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert 4 <= len(SEC) <= 9 and 32 <= len(items) <= 38, (len(SEC), len(items))
    assert cnt[5] >= 3 and cnt[1] >= 5 and cnt[2] >= 7 and cnt[3] >= 7 and cnt[4] >= 5, cnt
    for s in SEC:
        lv = [it["lv"] for it in s["items"]]
        assert lv == sorted(lv), s["title"]
        for it in s["items"]:
            for k in ("q", "hint", "sol", "ex", "exa"):
                assert it[k].count("$") % 2 == 0 and "$$" not in it[k], (it["title"], k)
            assert all(" width=" not in seg or int(seg.split('width="')[1].split('"')[0]) <= 260
                       for seg in (it["q"] + it["sol"]).split("<svg")[1:]), it["title"]
