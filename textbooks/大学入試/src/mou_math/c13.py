"""第13章 指数関数・対数関数（数学II）"""
import math
import random
from fractions import Fraction as Fr

SEC = []
VS = []          # 各節の検算関数


def _v(f):
    VS.append(f)
    return f


# ---------------------------------------------------------------- 節1
SEC.append({"title": "指数の拡張と指数法則",
"base": r"""・$a>0$，$m,\ n$ は正の整数：$a^0=1$，$a^{-n}=\dfrac1{a^n}$，$a^{\frac mn}=\sqrt[n]{a^m}=\left(\sqrt[n]{a}\right)^m$<br>
・指数法則（$a>0,\ b>0$，$r,\ s$ は有理数）：$a^ra^s=a^{r+s}$，$(a^r)^s=a^{rs}$，$(ab)^r=a^rb^r$<br>
・$a>0$ のとき $\sqrt[n]{a}$ は $x^n=a$ を満たす正の数 $x$。$n$ が奇数なら $\sqrt[n]{-a}=-\sqrt[n]{a}$<br>
・$t=a^x+a^{-x}$ のとき　$a^{2x}+a^{-2x}=t^2-2$，$a^{3x}+a^{-3x}=t^3-3t$""",
"items": [
 {"lv": 1, "title": "累乗根と有理数の指数の計算",
  "q": r"次の計算をせよ。ただし、(3) では $a>0$ とする。<br>(1) $\sqrt[3]{24}+\sqrt[3]{-81}-\sqrt[3]{3}$　　(2) $8^{\frac23}\times4^{-\frac34}\div2^{-\frac12}$　　(3) $\sqrt{a\sqrt{a\sqrt{a}}}$",
  "hint": r"累乗根は中身を素因数分解して $\sqrt[3]{k^3m}=k\sqrt[3]{m}$ の形に簡単にする。積・商は底を素数（ここでは $2$）にそろえ、指数の足し算・引き算に直す。根号が重なっているときも $a^{\frac mn}$ の形に直すと計算できる。",
  "sol": r"(1) $\sqrt[3]{24}=\sqrt[3]{2^3\cdot3}=2\sqrt[3]{3}$，$\sqrt[3]{-81}=-\sqrt[3]{3^3\cdot3}=-3\sqrt[3]{3}$ より<br>"
         r"　与式 $=2\sqrt[3]{3}-3\sqrt[3]{3}-\sqrt[3]{3}=\boldsymbol{-2\sqrt[3]{3}}$<br>"
         r"(2) $8^{\frac23}=(2^3)^{\frac23}=2^2$，$4^{-\frac34}=(2^2)^{-\frac34}=2^{-\frac32}$ より<br>"
         r"　与式 $=2^{2-\frac32-\left(-\frac12\right)}=2^{1}=\boldsymbol{2}$<br>"
         r"(3) 内側から順に指数で表すと $a\sqrt a=a^{\frac32}$，$\sqrt{a\sqrt a}=a^{\frac34}$，$a\sqrt{a\sqrt a}=a^{\frac74}$ より<br>"
         r"　与式 $=\left(a^{\frac74}\right)^{\frac12}=\boldsymbol{a^{\frac78}}$　$\left(=\sqrt[8]{a^7}\right)$",
  "note": r"(3) の指数は $\dfrac12+\dfrac14+\dfrac18$ になっている。根号のまま変形しようとすると見通しが悪いので、指数に直すのが原則。",
  "ex": r"次の計算をせよ。ただし、(3) では $a>0$ とする。<br>(1) $\sqrt[3]{16}-\sqrt[3]{54}+\sqrt[3]{250}$　　(2) $27^{\frac23}\div9^{-\frac14}\times3^{-\frac52}$　　(3) $\sqrt[3]{a\sqrt{a}}\div\sqrt[4]{a^3}$",
  "exa": r"(1) $4\sqrt[3]{2}$　(2) $1$　(3) $a^{-\frac14}$"},
 {"lv": 2, "title": r"$a^{\frac12}+a^{-\frac12}$ の値から式の値を求める",
  "q": r"$a>0$，$a^{\frac12}+a^{-\frac12}=3$ のとき、次の式の値を求めよ。<br>(1) $a+a^{-1}$　　(2) $a^{\frac32}+a^{-\frac32}$　　(3) $a^{\frac12}-a^{-\frac12}$",
  "hint": r"$a^{\frac12}=x$ とおくと $a^{-\frac12}=\dfrac1x$ で、$x+\dfrac1x=3$ からの対称式の計算になる（$x\cdot\dfrac1x=1$）。(3) は2乗して求め、符号が決まるかどうかを調べる。",
  "sol": r"(1) $a+a^{-1}=\left(a^{\frac12}+a^{-\frac12}\right)^2-2a^{\frac12}a^{-\frac12}=3^2-2=\boldsymbol{7}$<br>"
         r"(2) $a^{\frac32}+a^{-\frac32}=\left(a^{\frac12}+a^{-\frac12}\right)^3-3a^{\frac12}a^{-\frac12}\left(a^{\frac12}+a^{-\frac12}\right)=27-3\cdot3=\boldsymbol{18}$<br>"
         r"(3) $\left(a^{\frac12}-a^{-\frac12}\right)^2=a-2+a^{-1}=7-2=5$ より　$a^{\frac12}-a^{-\frac12}=\pm\sqrt5$<br>"
         r"ここで $x=a^{\frac12}$ は $x+\dfrac1x=3$，すなわち $x^2-3x+1=0$ の解で $x=\dfrac{3\pm\sqrt5}{2}$（どちらも正）。<br>"
         r"$x=\dfrac{3+\sqrt5}{2}$ のとき $x-\dfrac1x=\sqrt5$，$x=\dfrac{3-\sqrt5}{2}$ のとき $x-\dfrac1x=-\sqrt5$ で、どちらも起こり得るから　$\boldsymbol{\pm\sqrt5}$",
  "note": r"条件 $a^{\frac12}+a^{-\frac12}=3$ だけでは $a>1$ か $0<a<1$ かが決まらない。差の値を求めるときは、両方の場合が実際に起こるかを確かめる。「$a>1$」などの条件があれば符号は1つに決まる。",
  "ex": r"$2^{x}+2^{-x}=4$ のとき、$4^{x}+4^{-x}$ と $8^{x}+8^{-x}$ の値を求めよ。",
  "exa": r"$4^x+4^{-x}=14$，$8^x+8^{-x}=52$"},
 {"lv": 3, "title": "指数を含む式の根号を外す",
  "q": r"$n$ を正の整数とし、$x=\dfrac12\left(5^{\frac1n}-5^{-\frac1n}\right)$ とする。$\left(x+\sqrt{1+x^2}\right)^n$ の値を求めよ。",
  "hint": r"$5^{\frac1n}=t$ とおくと $x=\dfrac12\left(t-\dfrac1t\right)$。$1+x^2$ が $\dfrac14\left(t+\dfrac1t\right)^2$ という完全平方になることに気づけば、根号が外れる。",
  "sol": r"$t=5^{\frac1n}$ とおくと $t>0$ で、$x=\dfrac12\left(t-t^{-1}\right)$。<br>"
         r"$1+x^2=1+\dfrac14\left(t^2-2+t^{-2}\right)=\dfrac14\left(t^2+2+t^{-2}\right)=\dfrac14\left(t+t^{-1}\right)^2$<br>"
         r"$t+t^{-1}>0$ であるから　$\sqrt{1+x^2}=\dfrac12\left(t+t^{-1}\right)$<br>"
         r"よって　$x+\sqrt{1+x^2}=\dfrac12\left(t-t^{-1}\right)+\dfrac12\left(t+t^{-1}\right)=t=5^{\frac1n}$<br>"
         r"ゆえに　$\left(x+\sqrt{1+x^2}\right)^n=\left(5^{\frac1n}\right)^n=\boldsymbol{5}$",
  "note": r"$\sqrt{A^2}=|A|$ なので、根号を外すときは $A$ の符号を確認する（ここでは $t+t^{-1}>0$）。$x=\dfrac12\left(t+t^{-1}\right)$ の形なら $x^2-1=\dfrac14\left(t-t^{-1}\right)^2$ となり、同様に処理できる。",
  "ex": r"$n$ を正の整数とし、$x=\dfrac12\left(3^{\frac1n}+3^{-\frac1n}\right)$ とする。$\left(x-\sqrt{x^2-1}\right)^n$ の値を求めよ。",
  "exa": r"$\dfrac13$"},
]})


@_v
def v1():
    c = lambda v: math.copysign(abs(v) ** (1 / 3), v)
    assert abs(c(24) + c(-81) - c(3) - (-2 * c(3))) < 1e-12
    assert Fr(2) - Fr(3, 2) + Fr(1, 2) == 1 and abs(8 ** (2 / 3) * 4 ** (-3 / 4) / 2 ** (-1 / 2) - 2) < 1e-12
    for a in [0.3, 2.0, 7.5]:
        assert abs(math.sqrt(a * math.sqrt(a * math.sqrt(a))) - a ** (7 / 8)) < 1e-12
        assert abs(c(a * math.sqrt(a)) / a ** 0.75 - a ** (-0.25)) < 1e-12
    assert abs(c(16) - c(54) + c(250) - 4 * c(2)) < 1e-12
    assert abs(27 ** (2 / 3) / 9 ** (-1 / 4) * 3 ** (-5 / 2) - 1) < 1e-12
    # 例題2
    for xs in [(3 + 5 ** 0.5) / 2, (3 - 5 ** 0.5) / 2]:
        a = xs * xs
        assert abs(a ** 0.5 + a ** -0.5 - 3) < 1e-12
        assert abs(a + 1 / a - 7) < 1e-10 and abs(a ** 1.5 + a ** -1.5 - 18) < 1e-9
        assert abs(abs(a ** 0.5 - a ** -0.5) - 5 ** 0.5) < 1e-12
    assert {round(x - 1 / x, 9) for x in [(3 + 5 ** 0.5) / 2, (3 - 5 ** 0.5) / 2]} == {round(5 ** 0.5, 9), round(-5 ** 0.5, 9)}
    u = 2 + 3 ** 0.5  # 2^x = u で 2^x+2^{-x}=4
    assert abs(u + 1 / u - 4) < 1e-12 and abs(u ** 2 + u ** -2 - 14) < 1e-9 and abs(u ** 3 + u ** -3 - 52) < 1e-9
    # 例題3
    for n in range(1, 12):
        t = 5 ** (1 / n); x = (t - 1 / t) / 2
        assert abs((x + math.sqrt(1 + x * x)) ** n - 5) < 1e-9
        t = 3 ** (1 / n); x = (t + 1 / t) / 2
        assert abs((x - math.sqrt(x * x - 1)) ** n - 1 / 3) < 1e-6


# ---------------------------------------------------------------- 節2
def _fig_b2():
    """y = 2^(3-x) + 1 のグラフ"""
    ox, oy, sx, sy = 30, 150, 24, 12.5
    P = lambda x, y: (ox + sx * x, oy - sy * y)
    pts, x = [], -0.12
    while x <= 7.0001:
        X, Y = P(x, 2 ** (3 - x) + 1)
        pts.append(f"{X:.1f},{Y:.1f}")
        x += 0.1
    ay, y9, p3 = P(0, 1)[1], P(0, 9)[1], P(3, 2)
    return (f'<svg class="fig" width="210" height="165" viewBox="0 0 210 165">'
            f'<line x1="4" y1="{oy}" x2="204" y2="{oy}" stroke="#333" stroke-width="1"/>'
            f'<line x1="{ox}" y1="160" x2="{ox}" y2="6" stroke="#333" stroke-width="1"/>'
            f'<text x="198" y="{oy + 11}" font-size="11">x</text><text x="{ox + 4}" y="13" font-size="11">y</text>'
            f'<text x="{ox - 11}" y="{oy + 11}" font-size="10">O</text>'
            f'<line x1="4" y1="{ay:.1f}" x2="204" y2="{ay:.1f}" stroke="#888" stroke-dasharray="4,3"/>'
            f'<text x="{ox - 9}" y="{ay + 3:.1f}" font-size="10">1</text>'
            f'<path d="M{" L".join(pts)}" fill="none" stroke="#16367a" stroke-width="1.6"/>'
            f'<circle cx="{ox}" cy="{y9:.1f}" r="2" fill="#16367a"/><text x="{ox - 10}" y="{y9 + 4:.1f}" font-size="10">9</text>'
            f'<circle cx="{p3[0]:.1f}" cy="{p3[1]:.1f}" r="2" fill="#16367a"/>'
            f'<line x1="{p3[0]:.1f}" y1="{p3[1]:.1f}" x2="{p3[0]:.1f}" y2="{oy}" stroke="#888" stroke-dasharray="2,2"/>'
            f'<text x="{p3[0] - 3:.1f}" y="{oy + 11}" font-size="10">3</text>'
            f'<text x="{p3[0] + 4:.1f}" y="{p3[1] - 4:.1f}" font-size="10">(3, 2)</text></svg>')


SEC.append({"title": "指数関数のグラフと大小",
"base": r"""・$y=a^x$（$a>0,\ a\neq1$）：定義域は実数全体、値域は $y>0$。点 $(0,\ 1)$ を通り、$x$ 軸が漸近線<br>
・$a>1$ のとき増加：$p<q\iff a^p<a^q$。　$0<a<1$ のとき減少：$p<q\iff a^p>a^q$<br>
・$y=a^{x-p}+q$ のグラフは $y=a^x$ のグラフを $x$ 軸方向に $p$，$y$ 軸方向に $q$ だけ平行移動したもの。$y=a^{-x}$ のグラフは $y=a^x$ と $y$ 軸に関して対称<br>
・底がそろわない累乗根の大小は、正の数 $A,\ B$ について $A<B\iff A^k<B^k$（$k$ は正の整数）を使って根号を外す""",
"items": [
 {"lv": 1, "title": "底をそろえて累乗の大小を比べる",
  "q": r"次の各組の数を小さい順に並べよ。<br>(1) $\sqrt[3]{4},\ \ \sqrt[5]{8},\ \ \left(\dfrac12\right)^{-\frac12},\ \ \sqrt[4]{8}$　　(2) $\sqrt{\dfrac13},\ \ \sqrt[3]{\dfrac19},\ \ \sqrt[4]{\dfrac1{27}}$",
  "hint": r"すべてを同じ底の累乗 $2^{r}$，$\left(\dfrac13\right)^{r}$ で表し、指数 $r$ の大小に直す。底が $1$ より大きいか小さいかで、大小の向きが変わる。",
  "sol": r"(1) $\sqrt[3]{4}=2^{\frac23}$，$\sqrt[5]{8}=2^{\frac35}$，$\left(\dfrac12\right)^{-\frac12}=2^{\frac12}$，$\sqrt[4]{8}=2^{\frac34}$<br>"
         r"指数は $\dfrac12<\dfrac35<\dfrac23<\dfrac34$ で、底 $2>1$ だから　$\boldsymbol{\left(\dfrac12\right)^{-\frac12}<\sqrt[5]{8}<\sqrt[3]{4}<\sqrt[4]{8}}$<br>"
         r"(2) $\sqrt{\dfrac13}=\left(\dfrac13\right)^{\frac12}$，$\sqrt[3]{\dfrac19}=\left(\dfrac13\right)^{\frac23}$，$\sqrt[4]{\dfrac1{27}}=\left(\dfrac13\right)^{\frac34}$<br>"
         r"指数は $\dfrac12<\dfrac23<\dfrac34$ で、底 $\dfrac13<1$ だから大小が逆になり　$\boldsymbol{\sqrt[4]{\dfrac1{27}}<\sqrt[3]{\dfrac19}<\sqrt{\dfrac13}}$",
  "note": r"(2) で「指数の大きい方が大きい」としてしまう誤りが多い。$\left(\dfrac13\right)^1=\dfrac13<\left(\dfrac13\right)^0=1$ のような簡単な例で向きを確かめるとよい。",
  "ex": r"次の各組の数を小さい順に並べよ。<br>(1) $\sqrt[3]{9},\ \ \sqrt[4]{27},\ \ \left(\dfrac13\right)^{-\frac58}$　　(2) $\sqrt[3]{0.25},\ \ \sqrt{0.5},\ \ \sqrt[5]{0.125}$",
  "exa": r"(1) $\left(\dfrac13\right)^{-\frac58}<\sqrt[3]{9}<\sqrt[4]{27}$　(2) $\sqrt[3]{0.25}<\sqrt[5]{0.125}<\sqrt{0.5}$"},
 {"lv": 2, "title": "指数関数のグラフの移動",
  "q": r"関数 $y=8\cdot2^{-x}+1$ のグラフは、$y=2^x$ のグラフをどのように移動したものか。また、このグラフの漸近線と、$y$ 軸との交点の座標を求め、グラフをかけ。",
  "hint": r"$8=2^3$ を使って $y=2^{-(x-3)}+1$ の形に直す。$x$ を $-x$ にするのが $y$ 軸対称、$x$ を $x-3$，$y$ を $y-1$ にするのが平行移動。",
  "sol": _fig_b2() +
         r"$y=8\cdot2^{-x}+1=2^{3-x}+1=2^{-(x-3)}+1$<br>"
         r"$y=2^{-x}$ のグラフは $y=2^x$ のグラフを $y$ 軸に関して対称移動したもので、$y=2^{-(x-3)}+1$ はそれを $x$ 軸方向に $3$，$y$ 軸方向に $1$ だけ平行移動したものである。<br>"
         r"よって <b>$y=2^x$ のグラフを $y$ 軸に関して対称移動し、さらに $x$ 軸方向に $3$，$y$ 軸方向に $1$ だけ平行移動したもの</b>。<br>"
         r"漸近線は直線 $\boldsymbol{y=1}$。$x=0$ とすると $y=8+1=9$ より、$y$ 軸との交点は $\boldsymbol{(0,\ 9)}$。グラフは右の図（$x$ が増加すると $y$ は減少して $1$ に近づく）。",
  "note": r"移動の順序に注意。先に $x$ 軸方向に $3$ だけ平行移動して $y=2^{x-3}$ とし、その後 $y$ 軸に関して対称移動すると $y=2^{-x-3}$ になり、別のグラフになる。",
  "ex": r"関数 $y=\dfrac19\cdot3^{x}-2$ のグラフは、$y=3^x$ のグラフをどのように移動したものか。また、漸近線と、$y$ 軸との交点の座標を求めよ。",
  "exa": r"$x$ 軸方向に $2$，$y$ 軸方向に $-2$ だけ平行移動したもの。漸近線 $y=-2$，交点 $\left(0,\ -\dfrac{17}{9}\right)$"},
 {"lv": 3, "title": "底も根号の指数も異なる数の大小",
  "q": r"$\sqrt{2},\ \ \sqrt[3]{3},\ \ \sqrt[5]{5},\ \ \sqrt[6]{6}$ を小さい順に並べよ。",
  "hint": r"底をそろえることはできない。2数ずつ、根号の指数の最小公倍数乗をして整数どうしの比較に直す。4数を一度に $30$ 乗するより、2数ずつ比べる方が計算が軽い。",
  "sol": r"どれも正の数なので、2数ずつ同じ正の整数乗して比べる。<br>"
         r"$\left(\sqrt2\right)^6=2^3=8$，$\left(\sqrt[3]{3}\right)^6=3^2=9$ より　$\sqrt2<\sqrt[3]{3}$<br>"
         r"$\left(\sqrt2\right)^{10}=2^5=32$，$\left(\sqrt[5]{5}\right)^{10}=5^2=25$ より　$\sqrt[5]{5}<\sqrt2$<br>"
         r"$\left(\sqrt[5]{5}\right)^{30}=5^6=15625$，$\left(\sqrt[6]{6}\right)^{30}=6^5=7776$ より　$\sqrt[6]{6}<\sqrt[5]{5}$<br>"
         r"以上より　$\boldsymbol{\sqrt[6]{6}<\sqrt[5]{5}<\sqrt2<\sqrt[3]{3}}$",
  "note": r"$\sqrt[n]{n}$ は $n=3$ のとき最大で、$n\geqq3$ では $n$ が大きいほど小さくなる（数学IIIの微分で示せる）。$\sqrt[4]{4}=\sqrt2$ であることも合わせて覚えておくと見通しがよい。",
  "ex": r"$2^{30},\ \ 3^{20},\ \ 5^{12},\ \ 7^{10}$ を小さい順に並べよ。",
  "exa": r"$5^{12}<7^{10}<2^{30}<3^{20}$（$2$ 乗の形 $\left(2^{15}\right)^2,\ \left(3^{10}\right)^2,\ \left(5^6\right)^2,\ \left(7^5\right)^2$ で比べる）"},
]})


@_v
def v2():
    vals = {"(1/2)^-1/2": 0.5 ** -0.5, "5r8": 8 ** 0.2, "3r4": 4 ** (1 / 3), "4r8": 8 ** 0.25}
    assert sorted(vals, key=vals.get) == ["(1/2)^-1/2", "5r8", "3r4", "4r8"]
    v = {"2r": (1 / 3) ** 0.5, "3r": (1 / 9) ** (1 / 3), "4r": (1 / 27) ** 0.25}
    assert sorted(v, key=v.get) == ["4r", "3r", "2r"]
    v = {"3r9": 9 ** (1 / 3), "4r27": 27 ** 0.25, "p": (1 / 3) ** (-5 / 8)}
    assert sorted(v, key=v.get) == ["p", "3r9", "4r27"]
    v = {"3r": 0.25 ** (1 / 3), "2r": 0.5 ** 0.5, "5r": 0.125 ** 0.2}
    assert sorted(v, key=v.get) == ["3r", "5r", "2r"]
    # グラフの移動
    for x in [-2, -0.5, 0, 1.3, 4]:
        assert abs(8 * 2 ** -x + 1 - (2 ** (-(x - 3)) + 1)) < 1e-12
        assert abs(3 ** x / 9 - 2 - (3 ** (x - 2) - 2)) < 1e-12
    assert 8 * 2 ** 0 + 1 == 9 and 2 ** (3 - 3) + 1 == 2 and Fr(1, 9) - 2 == Fr(-17, 9)
    # 4数の比較
    assert 2 ** 3 < 3 ** 2 and 5 ** 2 < 2 ** 5 and 6 ** 5 < 5 ** 6
    v = {"s2": 2 ** 0.5, "c3": 3 ** (1 / 3), "f5": 5 ** 0.2, "s6": 6 ** (1 / 6)}
    assert sorted(v, key=v.get) == ["s6", "f5", "s2", "c3"]
    v = {"2": 2 ** 30, "3": 3 ** 20, "5": 5 ** 12, "7": 7 ** 10}
    assert sorted(v, key=v.get) == ["5", "7", "2", "3"]


# ---------------------------------------------------------------- 節3
SEC.append({"title": "指数方程式・指数不等式",
"base": r"""・底をそろえる：$a>0,\ a\neq1$ のとき　$a^p=a^q\iff p=q$<br>
・不等式は底と $1$ の大小で向きが決まる：$a>1$ なら $a^p<a^q\iff p<q$，$0<a<1$ なら $a^p<a^q\iff p>q$<br>
・$a^x=t$ とおき換えると $t$ の方程式・不等式になる。このとき<b>$t>0$</b>（$x$ に範囲があれば $t$ の範囲もそれに応じて変わる）<br>
・$t=a^x$ の正の値1つに $x$ がちょうど1つ対応するので、「$x$ の解の個数」＝「$t$ の正の解の個数」""",
"items": [
 {"lv": 1, "title": "底をそろえる指数方程式・不等式",
  "q": r"次の方程式・不等式を解け。<br>(1) $8^{x}=4\sqrt2$　　(2) $9^{x}=27^{x-1}$　　(3) $\left(\dfrac13\right)^{x}\geqq9\sqrt3$",
  "hint": r"両辺を同じ底の累乗 $a^p$ の形で表し、指数を比べる。不等式では底が $1$ より小さいと不等号の向きが変わる。",
  "sol": r"(1) $8^x=2^{3x}$，$4\sqrt2=2^{2}\cdot2^{\frac12}=2^{\frac52}$ より $3x=\dfrac52$。よって　$\boldsymbol{x=\dfrac56}$<br>"
         r"(2) $9^x=3^{2x}$，$27^{x-1}=3^{3x-3}$ より $2x=3x-3$。よって　$\boldsymbol{x=3}$<br>"
         r"(3) $9\sqrt3=3^{\frac52}=\left(\dfrac13\right)^{-\frac52}$ より　$\left(\dfrac13\right)^{x}\geqq\left(\dfrac13\right)^{-\frac52}$<br>"
         r"底 $\dfrac13$ は $1$ より小さいから　$\boldsymbol{x\leqq-\dfrac52}$",
  "note": r"(3) は底を $3$ にそろえて $3^{-x}\geqq3^{\frac52}$ から $-x\geqq\dfrac52$ としてもよい。どちらの方法でも、最後に $x=-3$ などを代入して向きを確かめると安心。",
  "ex": r"次の方程式・不等式を解け。<br>(1) $27^{x}=\dfrac{1}{9\sqrt3}$　　(2) $4^{x+1}=8^{x}$　　(3) $(0.5)^{2x}>\left(\dfrac14\right)^{3}$",
  "exa": r"(1) $x=-\dfrac56$　(2) $x=2$　(3) $x<3$"},
 {"lv": 2, "title": "おき換えて2次方程式・2次不等式にする",
  "q": r"次の方程式・不等式を解け。<br>(1) $4^{x}-3\cdot2^{x+1}+8=0$　　(2) $9^{x}-10\cdot3^{x}+9\leqq0$",
  "hint": r"$4^x=\left(2^x\right)^2$，$2^{x+1}=2\cdot2^x$ だから、$2^x=t$ とおくと $t$ の2次式になる。$t>0$ の条件を忘れない。",
  "sol": r"(1) $2^x=t$ とおくと $t>0$ で、方程式は $t^2-6t+8=0$，すなわち $(t-2)(t-4)=0$<br>"
         r"$t=2,\ 4$（どちらも $t>0$ を満たす）。$2^x=2,\ 2^x=2^2$ より　$\boldsymbol{x=1,\ 2}$<br>"
         r"(2) $3^x=t$ とおくと $t>0$ で、不等式は $t^2-10t+9\leqq0$，すなわち $(t-1)(t-9)\leqq0$<br>"
         r"よって $1\leqq t\leqq9$（これは $t>0$ を満たす）。$3^0\leqq3^x\leqq3^2$ で、底 $3>1$ より　$\boldsymbol{0\leqq x\leqq2}$",
  "note": r"$t$ の解に負の値（例えば $t=-3$）が出たら $2^x=-3$ を満たす $x$ はないので捨てる。不等式では $t>0$ との共通部分をとってから $x$ に戻す。",
  "ex": r"次の方程式・不等式を解け。<br>(1) $9^{x}-2\cdot3^{x+1}-27=0$　　(2) $4^{x}-5\cdot2^{x+1}+16>0$",
  "exa": r"(1) $x=2$　(2) $x<1,\ 3<x$"},
 {"lv": 3, "title": "連立指数方程式（積と商をつくる）",
  "q": r"連立方程式 $2^{x}\cdot3^{y}=12,\ \ 3^{x}\cdot2^{y}=18$ を解け。",
  "hint": r"2式を掛けると $(2\cdot3)^{x}(3\cdot2)^{y}=6^{x+y}$，割ると $\left(\dfrac23\right)^{x-y}$ が現れる。和 $x+y$ と差 $x-y$ が求まれば $x,\ y$ が決まる。",
  "sol": r"2式の辺々を掛けると　$2^{x}3^{x}\cdot2^{y}3^{y}=12\cdot18$，すなわち $6^{x+y}=216=6^3$<br>"
         r"よって　$x+y=3$ …①<br>"
         r"第1式を第2式で割ると　$\left(\dfrac23\right)^{x}\left(\dfrac32\right)^{y}=\dfrac{12}{18}$，すなわち $\left(\dfrac23\right)^{x-y}=\dfrac23$<br>"
         r"よって　$x-y=1$ …②<br>"
         r"①，② より　$\boldsymbol{x=2,\ y=1}$（このとき $2^2\cdot3=12$，$3^2\cdot2=18$ で確かに成り立つ）",
  "note": r"両辺の $2$ を底とする対数をとると $x+y\log_{2}3=2+\log_{2}3$，$x\log_{2}3+y=1+2\log_{2}3$ という $x,\ y$ の連立1次方程式になり、$\log_{2}3\neq1$ を用いて解いても同じ結果を得る。",
  "ex": r"連立方程式 $2^{x}\cdot5^{y}=40,\ \ 5^{x}\cdot2^{y}=250$ を解け。",
  "exa": r"$x=3,\ y=1$"},
 {"lv": 4, "title": "指数方程式の実数解の個数（解の配置）",
  "q": r"$a$ を実数の定数とする。$x$ の方程式 $4^{x}-a\cdot2^{x+1}+a+6=0$ の異なる実数解の個数を、$a$ の値によって分類せよ。",
  "hint": r"$2^x=t$ とおくと、$t>0$ の値1つに $x$ がただ1つ対応する。よって <b>2次方程式 $t^2-2at+a+6=0$ の異なる正の解の個数</b>を調べればよい。2解の積・和・判別式の符号で分類する。",
  "sol": r"$2^x=t$ とおくと $t>0$ で、$t$ と $x$ は1対1に対応する。方程式は<br>"
         r"　$t^2-2at+a+6=0$ …①<br>"
         r"となり、求める個数は①の異なる正の解の個数に等しい。①の判別式を $D$ とすると $\dfrac D4=a^2-a-6=(a+2)(a-3)$，また①の2解の和は $2a$，積は $a+6$。<br>"
         r"(i) $a<-6$ のとき：2解の積 $a+6<0$ より、①は正の解と負の解を1つずつもつ。→ <b>1個</b><br>"
         r"(ii) $a=-6$ のとき：①は $t^2+12t=0$ で $t=0,\ -12$。正の解はない。→ <b>0個</b><br>"
         r"(iii) $a>-6$ のとき：積 $a+6>0$ より、実数解をもつならその2解は同符号。<br>"
         r"　・$-6<a\leqq-2$：$D\geqq0$ だが、和 $2a<0$ より解はともに負。→ 0個<br>"
         r"　・$-2<a<3$：$D<0$ で実数解をもたない。→ 0個<br>"
         r"　・$a=3$：重解 $t=a=3>0$。→ 1個<br>"
         r"　・$a>3$：$D>0$，和 $2a>0$，積 $>0$ より、異なる2つの正の解をもつ。→ 2個<br>"
         r"以上より　$\boldsymbol{a<-6}$ <b>のとき1個，</b>$\boldsymbol{-6\leqq a<3}$ <b>のとき0個，</b>$\boldsymbol{a=3}$ <b>のとき1個，</b>$\boldsymbol{a>3}$ <b>のとき2個</b>",
  "note": r"文字定数を分離して $a(2t-1)=t^2+6$ とし、$t>0$ の範囲で曲線 $y=\dfrac{t^2+6}{2t-1}$ と直線 $y=a$ の共有点を数える方法もある。どちらの方法でも、最初に「$t=2^x>0$ と $x$ は1対1」を確認することが大切。$t=2^x+2^{-x}$ のようなおき換えでは1対1にならない（1つの $t>2$ に $x$ が2つ対応する）ので注意。",
  "ex": r"$a$ を実数の定数とする。$x$ の方程式 $9^{x}-2a\cdot3^{x}+a+2=0$ の異なる実数解の個数を、$a$ の値によって分類せよ。",
  "exa": r"$a<-2$ のとき1個，$-2\leqq a<2$ のとき0個，$a=2$ のとき1個，$a>2$ のとき2個"},
]})


def _npos(b, c):
    """t^2 + b t + c = 0 の異なる正の実数解の個数（b, c は Fraction）"""
    d = b * b - 4 * c
    if d < 0:
        return 0
    if d == 0:
        return 1 if -b / 2 > 0 else 0
    r = math.sqrt(d)
    return sum(1 for t in ((-b - r) / 2, (-b + r) / 2) if t > 1e-12)


@_v
def v3():
    assert Fr(5, 6) * 3 == Fr(5, 2) and 2 * 3 == 3 * 3 - 3 and 3 * Fr(-5, 6) == Fr(-5, 2) and 2 * (2 + 1) == 3 * 2
    xs = [k / 40 for k in range(-400, 401)]
    for x in xs:
        if abs(x + 2.5) > 1e-9:
            assert ((1 / 3) ** x >= 9 * 3 ** 0.5) == (x <= -2.5)
        if abs(x - 3) > 1e-9:
            assert (0.5 ** (2 * x) > 0.25 ** 3) == (x < 3)
        if min(abs(x), abs(x - 2)) > 1e-9:
            assert (9 ** x - 10 * 3 ** x + 9 <= 0) == (0 <= x <= 2)
        if min(abs(x - 1), abs(x - 3)) > 1e-9:
            assert (4 ** x - 10 * 2 ** x + 16 > 0) == (x < 1 or x > 3)
    for x in [1, 2]:
        assert 4 ** x - 3 * 2 ** (x + 1) + 8 == 0
    assert 9 ** 2 - 2 * 3 ** 3 - 27 == 0 and _npos(Fr(-6), Fr(8)) == 2 and _npos(Fr(-6), Fr(-27)) == 1
    # 連立
    assert 2 ** 2 * 3 == 12 and 3 ** 2 * 2 == 18 and 2 ** 3 * 5 == 40 and 5 ** 3 * 2 == 250
    l3 = math.log2(3)  # 係数行列 [[1,l3],[l3,1]] は正則
    assert abs(1 - l3 * l3) > 0.1
    # 解の個数（4^x - 2a 2^x + a + 6 = 0）
    def cls1(a):
        return 1 if a < -6 else (0 if a < 3 else (1 if a == 3 else 2))
    def cls2(a):
        return 1 if a < -2 else (0 if a < 2 else (1 if a == 2 else 2))
    for k in range(-1200, 1201):
        a = Fr(k, 100)
        assert _npos(-2 * a, a + 6) == cls1(a), a
        assert _npos(-2 * a, a + 2) == cls2(a), a
    # x の個数として直接確認（数値で符号変化を数える）
    for a in [-8, -6, -4, 0, 2.9, 3, 3.5, 6]:
        f = lambda x: 4 ** x - 2 * a * 2 ** x + a + 6
        g = [f(-30 + k * 0.0005) for k in range(80001)]
        ch = sum(1 for i in range(len(g) - 1) if g[i] * g[i + 1] < 0 or g[i] == 0)
        if a != 3:
            assert ch == cls1(Fr(a).limit_denominator(100)), (a, ch)
    assert abs(4 ** math.log2(3) - 6 * 3 + 3 + 6) < 1e-9   # a=3 の重解 t=3


# ---------------------------------------------------------------- 節4
SEC.append({"title": "対数とその性質・底の変換",
"base": r"""・$a>0,\ a\neq1,\ M>0$ のとき　$a^p=M\iff p=\log_{a}M$（$M$ を真数という）。特に $\log_{a}1=0$，$\log_{a}a=1$，$a^{\log_{a}M}=M$<br>
・$\log_{a}MN=\log_{a}M+\log_{a}N$，$\log_{a}\dfrac MN=\log_{a}M-\log_{a}N$，$\log_{a}M^r=r\log_{a}M$<br>
・底の変換：$\log_{a}b=\dfrac{\log_{c}b}{\log_{c}a}$（$c>0,\ c\neq1$）。特に $\log_{a}b=\dfrac1{\log_{b}a}$，$\log_{a^m}b^n=\dfrac nm\log_{a}b$""",
"items": [
 {"lv": 1, "title": "対数の計算",
  "q": r"次の式を簡単にせよ。<br>(1) $\log_{\sqrt2}8$　　(2) $2\log_{3}6-\log_{3}\dfrac43$　　(3) $\dfrac12\log_{2}\dfrac89+\log_{2}\sqrt{18}$　　(4) $9^{\log_{3}2}$",
  "hint": r"(1) は $8$ を底 $\sqrt2$ の累乗で表す。(2)(3) は性質を使って1つの対数 $\log_{a}M$ にまとめる。(4) は $a^{\log_{a}M}=M$ が使える形に直す。",
  "sol": r"(1) $8=2^3=\left(\sqrt2\right)^6$ より　$\log_{\sqrt2}8=\boldsymbol{6}$<br>"
         r"(2) 与式 $=\log_{3}36-\log_{3}\dfrac43=\log_{3}\left(36\times\dfrac34\right)=\log_{3}27=\boldsymbol{3}$<br>"
         r"(3) 与式 $=\log_{2}\sqrt{\dfrac89}+\log_{2}\sqrt{18}=\log_{2}\sqrt{\dfrac89\times18}=\log_{2}\sqrt{16}=\log_{2}4=\boldsymbol{2}$<br>"
         r"(4) $9^{\log_{3}2}=\left(3^2\right)^{\log_{3}2}=\left(3^{\log_{3}2}\right)^2=2^2=\boldsymbol{4}$",
  "note": r"(2) は $\log_{3}6=\log_{3}2+1$，$\log_{3}\dfrac43=2\log_{3}2-1$ と分解し、$\log_{3}2$ を文字のように扱って $2(\log_{3}2+1)-(2\log_{3}2-1)=3$ と計算してもよい。",
  "ex": r"次の式を簡単にせよ。<br>(1) $\log_{\frac13}9\sqrt3$　　(2) $\log_{2}24-\dfrac12\log_{2}9$　　(3) $3\log_{5}\sqrt[3]{10}-\log_{5}\dfrac{2}{25}$　　(4) $25^{\log_{5}3}$",
  "exa": r"(1) $-\dfrac52$　(2) $3$　(3) $3$　(4) $9$"},
 {"lv": 1, "title": "底の変換公式",
  "q": r"次の式を簡単にせよ。<br>(1) $\log_{8}32$　　(2) $\log_{2}3\cdot\log_{3}5\cdot\log_{5}8$　　(3) $\log_{4}9\cdot\log_{27}16$",
  "hint": r"底がばらばらのときは、底の変換公式で<b>すべて同じ底</b>（ここでは $2$）にそろえる。",
  "sol": r"(1) $\log_{8}32=\dfrac{\log_{2}32}{\log_{2}8}=\boldsymbol{\dfrac53}$<br>"
         r"(2) 与式 $=\log_{2}3\cdot\dfrac{\log_{2}5}{\log_{2}3}\cdot\dfrac{\log_{2}8}{\log_{2}5}=\log_{2}8=\boldsymbol{3}$<br>"
         r"(3) $\log_{4}9=\dfrac{\log_{2}9}{\log_{2}4}=\dfrac{2\log_{2}3}{2}=\log_{2}3$，$\log_{27}16=\dfrac{\log_{2}16}{\log_{2}27}=\dfrac{4}{3\log_{2}3}$<br>"
         r"よって　与式 $=\log_{2}3\cdot\dfrac{4}{3\log_{2}3}=\boldsymbol{\dfrac43}$",
  "note": r"(2) は $\log_{a}b\cdot\log_{b}c=\log_{a}c$ の形をつないだもの。(3) は公式 $\log_{a^m}b^n=\dfrac nm\log_{a}b$ を使うと $\log_{2^2}3^2=\log_{2}3$，$\log_{3^3}2^4=\dfrac43\log_{3}2$ とすぐにわかる。",
  "ex": r"次の式を簡単にせよ。<br>(1) $\log_{9}27$　　(2) $\log_{3}4\cdot\log_{4}5\cdot\log_{5}9$　　(3) $\log_{25}8\cdot\log_{4}125$",
  "exa": r"(1) $\dfrac32$　(2) $2$　(3) $\dfrac94$"},
 {"lv": 2, "title": "対数を与えられた文字で表す",
  "q": r"$\log_{2}3=a,\ \log_{3}5=b$ とするとき、$\log_{15}40$ を $a,\ b$ で表せ。",
  "hint": r"与えられた対数の底がそろっていないので、すべて底 $2$ で表す。$\log_{2}5=\log_{2}3\cdot\log_{3}5$ がポイント。",
  "sol": r"$\log_{2}5=\dfrac{\log_{3}5}{\log_{3}2}=\log_{2}3\cdot\log_{3}5=ab$<br>"
         r"よって　$\log_{15}40=\dfrac{\log_{2}40}{\log_{2}15}=\dfrac{\log_{2}\left(2^3\cdot5\right)}{\log_{2}(3\cdot5)}=\dfrac{3+\log_{2}5}{\log_{2}3+\log_{2}5}=\boldsymbol{\dfrac{ab+3}{a(b+1)}}$",
  "note": r"底を $3$ にそろえて $\log_{3}2=\dfrac1a$ を使っても同じ式になる。どの底にそろえるかは、与えられた対数の底のどれか（ここでは $2$）を選ぶのが基本。",
  "ex": r"$\log_{2}3=a,\ \log_{3}7=b$ とするとき、$\log_{42}56$ を $a,\ b$ で表せ。",
  "exa": r"$\dfrac{ab+3}{ab+a+1}$"},
 {"lv": 2, "title": r"$a^x=b^y=c$ の形の条件",
  "q": r"$2^{x}=5^{y}=100$ のとき、$\dfrac1x+\dfrac1y$ の値を求めよ。",
  "hint": r"指数の条件は、対数の定義で $x=\log_{2}100$ のように書き直す。逆数は底の変換 $\dfrac1{\log_{a}b}=\log_{b}a$ で処理できる。",
  "sol": r"$x=\log_{2}100$，$y=\log_{5}100$ であるから　$\dfrac1x=\log_{100}2$，$\dfrac1y=\log_{100}5$<br>"
         r"よって　$\dfrac1x+\dfrac1y=\log_{100}2+\log_{100}5=\log_{100}10=\boldsymbol{\dfrac12}$",
  "note": r"各辺の常用対数をとって $x\log_{10}2=y\log_{10}5=2$ とし、$\dfrac1x+\dfrac1y=\dfrac{\log_{10}2+\log_{10}5}{2}=\dfrac12$ としてもよい。共通の値が文字のときは、それが $1$ でないこと（$x\neq0$ から従う）を確認してから底にする。",
  "ex": r"$3^{x}=4^{y}=12^{z}$（$xyz\neq0$）のとき、$\dfrac1x+\dfrac1y-\dfrac1z$ の値を求めよ。",
  "exa": r"$0$"},
 {"lv": 3, "title": "対数の値が無理数であることの証明と値の評価",
  "q": r"(1) $\log_{2}3$ は無理数であることを証明せよ。<br>(2) $\dfrac32<\log_{2}3<\dfrac53$ であることを示せ。",
  "hint": r"(1) 有理数 $\dfrac mn$ と仮定して指数の式 $2^m=3^n$ に直し、偶奇で矛盾を導く（背理法）。(2) $\log_{2}3>\dfrac32\iff3>2^{\frac32}\iff3^2>2^3$ のように、整数の累乗の大小に直す。",
  "sol": r"(1) $\log_{2}3>\log_{2}1=0$ である。$\log_{2}3$ が有理数であると仮定すると、正の整数 $m,\ n$ を用いて $\log_{2}3=\dfrac mn$ と表せる。<br>"
         r"このとき $2^{\frac mn}=3$ より $2^m=3^n$。$m\geqq1$ より左辺は偶数、右辺は奇数であるから矛盾する。<br>"
         r"よって、$\log_{2}3$ は無理数である。■<br>"
         r"(2) $3^2=9>8=2^3$ より $3>2^{\frac32}$。底 $2>1$ より $\log_{2}3>\log_{2}2^{\frac32}=\dfrac32$<br>"
         r"$3^3=27<32=2^5$ より $3<2^{\frac53}$。よって $\log_{2}3<\dfrac53$<br>"
         r"ゆえに　$\dfrac32<\log_{2}3<\dfrac53$　■",
  "note": r"(1) で「正の整数 $m,\ n$」とおけるのは $\log_{2}3>0$ だから。$m=0$ の可能性を残すと「$2^m$ は偶数」がいえなくなる。(2) のような評価はさらに精密にでき、$3^5=243<256=2^8$ から $\log_{2}3<\dfrac85$ も得られる。",
  "ex": r"$\log_{3}5$ は無理数であることを証明せよ。また、$\dfrac75<\log_{3}5<\dfrac32$ であることを示せ。",
  "exa": r"$\log_{3}5=\dfrac mn$（$m,\ n$ は正の整数）とすると $3^m=5^n$ で、左辺は $3$ の倍数、右辺は $3$ の倍数でなく矛盾。評価は $5^5=3125>2187=3^7$，$5^2=25<27=3^3$ から従う。"},
]})


@_v
def v4():
    L = lambda b, x: math.log(x) / math.log(b)
    near = lambda u, v: abs(u - v) < 1e-12
    assert near(L(2 ** 0.5, 8), 6) and near(2 * L(3, 6) - L(3, 4 / 3), 3)
    assert near(0.5 * L(2, 8 / 9) + L(2, 18 ** 0.5), 2) and near(9 ** L(3, 2), 4)
    assert near(L(1 / 3, 9 * 3 ** 0.5), -2.5) and near(L(2, 24) - 0.5 * L(2, 9), 3)
    assert near(3 * L(5, 10 ** (1 / 3)) - L(5, 2 / 25), 3) and near(25 ** L(5, 3), 9)
    assert near(L(8, 32), 5 / 3) and near(L(2, 3) * L(3, 5) * L(5, 8), 3) and near(L(4, 9) * L(27, 16), 4 / 3)
    assert near(L(9, 27), 1.5) and near(L(3, 4) * L(4, 5) * L(5, 9), 2) and near(L(25, 8) * L(4, 125), 9 / 4)
    a, b = L(2, 3), L(3, 5)
    assert near(L(15, 40), (a * b + 3) / (a * (b + 1)))
    a, b = L(2, 3), L(3, 7)
    assert near(L(42, 56), (a * b + 3) / (a * b + a + 1))
    x, y = L(2, 100), L(5, 100)
    assert near(1 / x + 1 / y, 0.5)
    for k in [0.2, 0.7, 5.0, 123.0]:
        x, y, z = L(3, k), L(4, k), L(12, k)
        assert abs(1 / x + 1 / y - 1 / z) < 1e-12
    # 評価
    assert 3 ** 2 > 2 ** 3 and 3 ** 3 < 2 ** 5 and 1.5 < L(2, 3) < 5 / 3 and 3 ** 5 < 2 ** 8
    assert 5 ** 5 == 3125 > 3 ** 7 == 2187 and 5 ** 2 < 3 ** 3 and 1.4 < L(3, 5) < 1.5
    for m in range(1, 60):          # 2^m = 3^n, 3^m = 5^n となる正の整数はない
        for n in range(1, 60):
            assert 2 ** m != 3 ** n and 3 ** m != 5 ** n


# ---------------------------------------------------------------- 節5
def _fig_e6():
    """log_x y < log_y x の表す領域"""
    ox, oy, sc, M = 20, 168, 45, 3.3
    Q = lambda x, y: (ox + sc * x, oy - sc * y)
    poly = lambda ps: " ".join(f"{Q(*p)[0]:.1f},{Q(*p)[1]:.1f}" for p in ps)
    N = 40
    r1 = [(1, 0)] + [(1 + (M - 1) * i / N, 1 / (1 + (M - 1) * i / N)) for i in range(N + 1)] + [(M, 0)]
    r2 = [(1, 1), (M, M), (M, 1)]
    r3 = [(1 / M + (1 - 1 / M) * i / N, 1 / (1 / M + (1 - 1 / M) * i / N)) for i in range(N + 1)] + [(1, M)]
    r4 = [(0, 0), (1, 1), (0, 1)]
    cur = [(1 / M + (M - 1 / M) * i / 120, 1 / (1 / M + (M - 1 / M) * i / 120)) for i in range(121)]
    cpath = "M" + " L".join(f"{Q(*p)[0]:.1f},{Q(*p)[1]:.1f}" for p in cur)
    f = 'fill="#3d6fd1" fill-opacity="0.28" stroke="none"'
    X1, Y1 = Q(1, 0)[0], Q(0, 1)[1]
    return (f'<svg class="fig" width="200" height="185" viewBox="0 0 200 185">'
            f'<polygon points="{poly(r1)}" {f}/><polygon points="{poly(r2)}" {f}/>'
            f'<polygon points="{poly(r3)}" {f}/><polygon points="{poly(r4)}" {f}/>'
            f'<line x1="{ox}" y1="{oy}" x2="196" y2="{oy}" stroke="#333"/><line x1="{ox}" y1="{oy}" x2="{ox}" y2="4" stroke="#333"/>'
            f'<text x="190" y="{oy + 12}" font-size="11">x</text><text x="{ox + 4}" y="11" font-size="11">y</text>'
            f'<text x="{ox - 11}" y="{oy + 12}" font-size="10">O</text>'
            f'<line x1="{X1:.1f}" y1="{oy}" x2="{X1:.1f}" y2="{Q(0, M)[1]:.1f}" stroke="#555" stroke-dasharray="4,3"/>'
            f'<line x1="{ox}" y1="{Y1:.1f}" x2="{Q(M, 0)[0]:.1f}" y2="{Y1:.1f}" stroke="#555" stroke-dasharray="4,3"/>'
            f'<line x1="{ox}" y1="{oy}" x2="{Q(M, M)[0]:.1f}" y2="{Q(M, M)[1]:.1f}" stroke="#16367a" stroke-dasharray="4,3"/>'
            f'<path d="{cpath}" fill="none" stroke="#16367a" stroke-dasharray="4,3"/>'
            f'<text x="{X1 - 3:.1f}" y="{oy + 12}" font-size="10">1</text><text x="{ox - 9}" y="{Y1 + 4:.1f}" font-size="10">1</text>'
            f'<text x="{Q(2.45, 2.95)[0]:.1f}" y="{Q(2.45, 2.95)[1]:.1f}" font-size="10">y=x</text>'
            f'<text x="{Q(2.2, 0.62)[0]:.1f}" y="{Q(2.2, 0.62)[1]:.1f}" font-size="10">y=1/x</text></svg>')


SEC.append({"title": "対数関数と対数方程式・対数不等式",
"base": r"""・$y=\log_{a}x$ は $y=a^x$ の逆関数で、グラフは直線 $y=x$ に関して対称。定義域は $x>0$，$y$ 軸が漸近線<br>
・$a>1$ のとき増加：$0<p<q\iff\log_{a}p<\log_{a}q$。　$0<a<1$ のとき減少：$0<p<q\iff\log_{a}p>\log_{a}q$<br>
・まず<b>真数条件（真数 $>0$）と底の条件（底 $>0$，底 $\neq1$）</b>を書き出し、底をそろえて $\log_{a}M=\log_{a}N$，$\log_{a}M<\log_{a}N$ の形にする<br>
・底が文字のときは $a>1$ と $0<a<1$ で場合を分ける""",
"items": [
 {"lv": 1, "title": "対数方程式の基本（真数条件）",
  "q": r"次の方程式を解け。<br>(1) $\log_{3}(2x-1)=2$　　(2) $\log_{2}(x+1)+\log_{2}(x-2)=2$",
  "hint": r"最初に真数条件を書く。(2) は左辺を1つの対数にまとめ、右辺も $2=\log_{2}4$ と対数で表して真数を比べる。",
  "sol": r"(1) 真数条件は $2x-1>0$。対数の定義より $2x-1=3^2=9$，よって $x=5$（真数条件を満たす）。　$\boldsymbol{x=5}$<br>"
         r"(2) 真数条件は $x+1>0$ かつ $x-2>0$，すなわち $x>2$ …①<br>"
         r"方程式は $\log_{2}(x+1)(x-2)=\log_{2}4$ となるから　$(x+1)(x-2)=4$<br>"
         r"$x^2-x-6=0$ より $(x-3)(x+2)=0$，$x=3,\ -2$。①より　$\boldsymbol{x=3}$",
  "note": r"(2) で真数条件を忘れると $x=-2$ も答えにしてしまう。$\log_{2}(x+1)+\log_{2}(x-2)$ と $\log_{2}(x+1)(x-2)$ は定義される $x$ の範囲が違う（後者は $x<-1$ でも定義される）ことが原因である。",
  "ex": r"次の方程式を解け。<br>(1) $\log_{\frac12}(x+3)=-2$　　(2) $\log_{3}x+\log_{3}(x-8)=2$",
  "exa": r"(1) $x=1$　(2) $x=9$"},
 {"lv": 2, "title": "底をそろえる対数方程式",
  "q": r"次の方程式を解け。<br>(1) $\log_{2}(x-2)=\log_{4}(x+10)$　　(2) $\log_{2}x-\log_{x}8=2$",
  "hint": r"底の変換公式で底を $2$ にそろえる。(2) は $\log_{x}8=\dfrac{3}{\log_{2}x}$ となるので、$\log_{2}x=t$ とおくと $t$ の分数方程式。底 $x$ の条件 $x>0,\ x\neq1$ も忘れない。",
  "sol": r"(1) 真数条件は $x-2>0$ かつ $x+10>0$，すなわち $x>2$。<br>"
         r"$\log_{4}(x+10)=\dfrac{\log_{2}(x+10)}{\log_{2}4}=\dfrac12\log_{2}(x+10)$ より、方程式は $2\log_{2}(x-2)=\log_{2}(x+10)$<br>"
         r"よって $(x-2)^2=x+10$，$x^2-5x-6=0$，$(x-6)(x+1)=0$。$x>2$ より　$\boldsymbol{x=6}$<br>"
         r"(2) 真数・底の条件は $x>0,\ x\neq1$。$\log_{2}x=t$ とおくと $t\neq0$ で、$\log_{x}8=\dfrac{\log_{2}8}{\log_{2}x}=\dfrac3t$<br>"
         r"$t-\dfrac3t=2$ の両辺に $t$ を掛けて $t^2-2t-3=0$，$(t-3)(t+1)=0$ より $t=3,\ -1$<br>"
         r"$\log_{2}x=3,\ -1$ より　$\boldsymbol{x=8,\ \dfrac12}$（どちらも条件を満たす）",
  "note": r"(1) で $2\log_{2}(x-2)=\log_{2}(x-2)^2$ と変形できるのは $x-2>0$ のときだけ。真数条件を先に確定させておけば、この変形を安心して使える。",
  "ex": r"次の方程式を解け。<br>(1) $\log_{3}(x+1)=\log_{9}(5x+11)$　　(2) $\log_{3}x+2\log_{x}3=3$",
  "exa": r"(1) $x=5$　(2) $x=3,\ 9$"},
 {"lv": 2, "title": "対数不等式（底と1の大小）",
  "q": r"次の不等式を解け。<br>(1) $\log_{2}(x-2)+\log_{2}(x-3)\leqq1$　　(2) $\log_{\frac12}(x-1)\geqq\log_{\frac14}(x+5)$",
  "hint": r"真数条件を求めてから、両辺を同じ底の対数にする。底が $1$ より小さいときは、真数の大小が逆になる。最後に真数条件との共通部分をとる。",
  "sol": r"(1) 真数条件は $x-2>0$ かつ $x-3>0$，すなわち $x>3$ …①<br>"
         r"不等式は $\log_{2}(x-2)(x-3)\leqq\log_{2}2$。底 $2>1$ より $(x-2)(x-3)\leqq2$<br>"
         r"$x^2-5x+4\leqq0$，$(x-1)(x-4)\leqq0$ より $1\leqq x\leqq4$。①との共通部分をとって　$\boldsymbol{3<x\leqq4}$<br>"
         r"(2) 真数条件は $x-1>0$ かつ $x+5>0$，すなわち $x>1$ …②<br>"
         r"$\log_{\frac14}(x+5)=\dfrac{\log_{\frac12}(x+5)}{\log_{\frac12}\frac14}=\dfrac12\log_{\frac12}(x+5)$ より、不等式は<br>"
         r"　$2\log_{\frac12}(x-1)\geqq\log_{\frac12}(x+5)$，すなわち $\log_{\frac12}(x-1)^2\geqq\log_{\frac12}(x+5)$<br>"
         r"底 $\dfrac12<1$ より $(x-1)^2\leqq x+5$，$x^2-3x-4\leqq0$，$(x+1)(x-4)\leqq0$ より $-1\leqq x\leqq4$<br>"
         r"②との共通部分をとって　$\boldsymbol{1<x\leqq4}$",
  "note": r"(2) は底を $2$ にそろえて $-\log_{2}(x-1)\geqq-\dfrac12\log_{2}(x+5)$ としてもよい。両辺に $-2$ を掛けると不等号の向きが変わり、同じ結論になる。",
  "ex": r"次の不等式を解け。<br>(1) $\log_{3}(x-1)+\log_{3}(x+1)<1$　　(2) $\log_{\frac13}(x-2)\geqq\log_{\frac19}(x+4)$",
  "exa": r"(1) $1<x<2$　(2) $2<x\leqq5$"},
 {"lv": 3, "title": "両辺の対数をとる方程式",
  "q": r"方程式 $x^{\log_{10}x}=\dfrac{x^{3}}{100}$ を解け。",
  "hint": r"指数部分に $\log$ があるので、両辺の常用対数をとる。$\log_{10}x^{\log_{10}x}=(\log_{10}x)^2$ となり、$\log_{10}x=t$ とおくと $t$ の2次方程式になる。",
  "sol": r"左辺が定義されるためには $x>0$ である。このとき両辺は正であるから、両辺の常用対数をとって<br>"
         r"　$\log_{10}x^{\log_{10}x}=\log_{10}\dfrac{x^{3}}{100}$，すなわち $(\log_{10}x)^2=3\log_{10}x-2$<br>"
         r"$\log_{10}x=t$ とおくと $t^2-3t+2=0$，$(t-1)(t-2)=0$ より $t=1,\ 2$<br>"
         r"よって　$\boldsymbol{x=10,\ 100}$",
  "note": r"$x^{\log_{a}x}$ の形は「底 $a$ の対数をとる」のが定石。$x=10$ のとき両辺はともに $10$，$x=100$ のとき両辺はともに $10^4$ となり、確かに解である。",
  "ex": r"方程式 $x^{\log_{2}x}=\dfrac{x^{4}}{8}$ を解け。",
  "exa": r"$x=2,\ 8$"},
 {"lv": 3, "title": "底に文字を含む対数不等式",
  "q": r"$a$ を $1$ でない正の定数とする。不等式 $2\log_{a}(x-1)>\log_{a}(x+5)$ を解け。",
  "hint": r"$\log_{a}M>\log_{a}N$ から $M,\ N$ の大小を導くとき、$a>1$ なら $M>N$，$0<a<1$ なら $M<N$。$a$ の値で場合を分ける。",
  "sol": r"真数条件は $x-1>0$ かつ $x+5>0$，すなわち $x>1$ …①<br>"
         r"①のもとで、不等式は $\log_{a}(x-1)^2>\log_{a}(x+5)$ と同値。<br>"
         r"(i) $a>1$ のとき：$(x-1)^2>x+5$，$x^2-3x-4>0$，$(x+1)(x-4)>0$ より $x<-1,\ 4<x$。①と合わせて $x>4$<br>"
         r"(ii) $0<a<1$ のとき：$(x-1)^2<x+5$，$(x+1)(x-4)<0$ より $-1<x<4$。①と合わせて $1<x<4$<br>"
         r"よって　$\boldsymbol{a>1}$ <b>のとき</b> $\boldsymbol{x>4}$，$\boldsymbol{0<a<1}$ <b>のとき</b> $\boldsymbol{1<x<4}$",
  "note": r"$x=4$ のときは両辺が等しくなるので、どちらの場合にも含まれない。場合分けの結果を並べると、$x>1,\ x\neq4$ の範囲が $a$ の値によって2つに分かれていることがわかる。",
  "ex": r"$a$ を $1$ でない正の定数とする。不等式 $\log_{a}(x+1)+\log_{a}(x-1)<\log_{a}3$ を解け。",
  "exa": r"$a>1$ のとき $1<x<2$，$0<a<1$ のとき $x>2$"},
 {"lv": 4, "title": "底と真数に変数を含む不等式の表す領域",
  "q": r"不等式 $\log_{x}y<\log_{y}x$ を満たす点 $(x,\ y)$ の存在範囲を図示せよ。",
  "hint": r"底の条件・真数条件から $x>0,\ x\neq1,\ y>0,\ y\neq1$。$t=\log_{x}y$ とおくと $\log_{y}x=\dfrac1t$ で、分数不等式 $t<\dfrac1t$ を解く。最後に、$\log_{x}$ が増加か減少かで $x>1$，$0<x<1$ に分けて $y$ の条件に戻す。",
  "sol": _fig_e6() +
         r"底・真数の条件より $x>0,\ x\neq1,\ y>0,\ y\neq1$。<br>"
         r"$t=\log_{x}y$ とおくと $t\neq0$ で、$\log_{y}x=\dfrac1t$。$t<\dfrac1t$ の両辺に $t^2\ (>0)$ を掛けて<br>"
         r"　$t^3<t$，$t(t+1)(t-1)<0$ より　$t<-1$ または $0<t<1$<br>"
         r"(i) $x>1$ のとき（$\log_{x}$ は増加）<br>"
         r"　$t<-1\iff\log_{x}y<\log_{x}\dfrac1x\iff y<\dfrac1x$<br>"
         r"　$0<t<1\iff\log_{x}1<\log_{x}y<\log_{x}x\iff1<y<x$<br>"
         r"(ii) $0<x<1$ のとき（$\log_{x}$ は減少）<br>"
         r"　$t<-1\iff\log_{x}y<\log_{x}\dfrac1x\iff y>\dfrac1x$<br>"
         r"　$0<t<1\iff\log_{x}1<\log_{x}y<\log_{x}x\iff x<y<1$<br>"
         r"よって求める範囲は<br>"
         r"　$x>1$ のとき $0<y<\dfrac1x$ または $1<y<x$；$0<x<1$ のとき $y>\dfrac1x$ または $x<y<1$<br>"
         r"で、右の図の色のついた部分。<b>ただし境界線（直線 $x=1,\ y=1,\ y=x$，曲線 $y=\dfrac1x$ と座標軸）は含まない。</b>",
  "note": r"両辺に $t$ を掛けると $t$ の符号で場合分けが必要になる。$t^2$ を掛ければ向きを気にせずに済む。$\log_{x}y=\dfrac{\log_{2}y}{\log_{2}x}$ として、$X=\log_{2}x,\ Y=\log_{2}y$ の平面で考える方法もある（$Y<-X$ や $0<Y<X$ などの直線で区切られた領域になる）。",
  "ex": r"不等式 $\log_{x}y+2>3\log_{y}x$ を満たす点 $(x,\ y)$ の存在範囲を、$x,\ y$ の不等式で表せ。",
  "exa": r"$x>1$ のとき $\dfrac1{x^3}<y<1$ または $y>x$；$0<x<1$ のとき $1<y<\dfrac1{x^3}$ または $0<y<x$"},
]})


@_v
def v5():
    L = lambda b, x: math.log(x) / math.log(b)
    assert 2 * 5 - 1 == 9 and math.isclose(L(2, 4) + L(2, 1), 2) and math.isclose(L(0.5, 4), -2)
    assert math.isclose(L(3, 9) + L(3, 1), 2)
    assert (6 - 2) ** 2 == 6 + 10 and (5 + 1) ** 2 == 5 * 5 + 11
    assert math.isclose(L(2, 8) - L(8, 8), 2) and math.isclose(L(2, 0.5) - L(0.5, 8), 2)
    assert math.isclose(L(3, 3) + 2 * L(3, 3), 3) and math.isclose(L(3, 9) + 2 * L(9, 3), 3)
    # 方程式の解がそれだけであることの数値確認
    def roots(f, lo, hi, n=200000):
        r, g = [], [f(lo + (hi - lo) * k / n) for k in range(n + 1)]
        for k in range(n):
            if g[k] == 0 or g[k] * g[k + 1] < 0:
                r.append(lo + (hi - lo) * k / n)
        return r
    assert len(roots(lambda x: L(2, x + 1) + L(2, x - 2) - 2, 2.000001, 50)) == 1
    assert len(roots(lambda x: L(2, x - 2) - L(4, x + 10), 2.000001, 100)) == 1
    assert len(roots(lambda x: L(10, x) ** 2 - 3 * L(10, x) + 2, 0.001, 1000)) == 2
    for x in [10, 100]:
        assert math.isclose(x ** math.log10(x), x ** 3 / 100)
    for x in [2, 8]:
        assert math.isclose(x ** math.log2(x), x ** 4 / 8)
    # 不等式
    for k in range(1, 4000):
        x = k / 400
        if x > 3 and abs(x - 4) > 1e-9:
            assert (L(2, x - 2) + L(2, x - 3) <= 1) == (x <= 4)
        if x > 1 and abs(x - 4) > 1e-9:
            assert (L(0.5, x - 1) >= L(0.25, x + 5)) == (x <= 4)
            for a in [3.0, 1.7, 0.4, 0.9]:
                assert (2 * L(a, x - 1) > L(a, x + 5)) == ((x > 4) if a > 1 else (x < 4))
        if x > 1 and abs(x - 2) > 1e-9:
            assert (L(3, x - 1) + L(3, x + 1) < 1) == (x < 2)
            for a in [3.0, 0.4]:
                assert (L(a, x + 1) + L(a, x - 1) < L(a, 3)) == ((x < 2) if a > 1 else (x > 2))
        if x > 2 and abs(x - 5) > 1e-9:
            assert (L(1 / 3, x - 2) >= L(1 / 9, x + 4)) == (x <= 5)
    assert math.isclose(L(2, 2) + L(2, 1), 1) and math.isclose(L(0.5, 3), L(0.25, 9))
    # 領域
    random.seed(13)
    for _ in range(40000):
        x, y = random.uniform(0.01, 4), random.uniform(0.01, 4)
        if min(abs(x - 1), abs(y - 1), abs(y - x), abs(y - 1 / x)) < 1e-6:
            continue
        lhs = L(x, y) < L(y, x)
        reg = (0 < y < 1 / x or 1 < y < x) if x > 1 else (y > 1 / x or x < y < 1)
        assert lhs == reg
        if min(abs(y - x ** -3), abs(y - x)) < 1e-6:
            continue
        lhs = L(x, y) + 2 > 3 * L(y, x)
        reg = (x ** -3 < y < 1 or y > x) if x > 1 else (1 < y < x ** -3 or 0 < y < x)
        assert lhs == reg


# ---------------------------------------------------------------- 節6
SEC.append({"title": "対数の大小比較",
"base": r"""・同じ底にそろえる：底が $1$ より大きければ真数の大小と一致し、$1$ より小さければ逆になる<br>
・数と対数の比較は、数を対数で表す：$\dfrac32=\log_{2}2^{\frac32}=\log_{2}2\sqrt2$<br>
・底が異なる対数は、間に入る有理数 $\dfrac pq$ を探し、$\log_{a}b>\dfrac pq\iff b^q>a^p$（$a>1,\ p,\ q>0$）で整数の累乗の比較に直す<br>
・$\log_{a}b\cdot\log_{a}c$ の形は、相加平均・相乗平均の関係 $\sqrt{AB}\leqq\dfrac{A+B}{2}=\dfrac{\log_{a}bc}{2}$ で評価できることがある""",
"items": [
 {"lv": 2, "title": "底をそろえて対数の大小を比べる",
  "q": r"次の各組の数を小さい順に並べよ。<br>(1) $\dfrac32,\ \ \log_{2}3,\ \ \log_{4}10$　　(2) $\log_{\frac13}2,\ \ \log_{\frac19}5,\ \ -\dfrac12$",
  "hint": r"底を $2$ や $\dfrac13$ にそろえ、数も同じ底の対数で表して真数を比べる。$\log_{4}10=\dfrac12\log_{2}10=\log_{2}\sqrt{10}$ のように、係数は真数の指数にしてしまう。",
  "sol": r"(1) $\dfrac32=\log_{2}2^{\frac32}=\log_{2}\sqrt8$，$\log_{2}3=\log_{2}\sqrt9$，$\log_{4}10=\dfrac{\log_{2}10}{\log_{2}4}=\dfrac12\log_{2}10=\log_{2}\sqrt{10}$<br>"
         r"$\sqrt8<\sqrt9<\sqrt{10}$ で底 $2>1$ だから　$\boldsymbol{\dfrac32<\log_{2}3<\log_{4}10}$<br>"
         r"(2) $\log_{\frac19}5=\dfrac{\log_{\frac13}5}{\log_{\frac13}\frac19}=\dfrac12\log_{\frac13}5=\log_{\frac13}\sqrt5$，$-\dfrac12=\log_{\frac13}\left(\dfrac13\right)^{-\frac12}=\log_{\frac13}\sqrt3$<br>"
         r"$\sqrt3<2<\sqrt5$ で底 $\dfrac13<1$ だから大小が逆になり　$\boldsymbol{\log_{\frac19}5<\log_{\frac13}2<-\dfrac12}$",
  "note": r"(2) は底を $3$ にそろえて $\log_{\frac13}2=-\log_{3}2$，$\log_{\frac19}5=-\log_{3}\sqrt5$，$-\dfrac12=-\log_{3}\sqrt3$ としてもよい。負の符号がつくので、真数の大小と逆になる。",
  "ex": r"次の各組の数を小さい順に並べよ。<br>(1) $\log_{3}5,\ \ \log_{9}20,\ \ \dfrac32$　　(2) $\log_{0.5}3,\ \ \log_{0.25}10,\ \ -\dfrac32$",
  "exa": r"(1) $\log_{9}20<\log_{3}5<\dfrac32$　(2) $\log_{0.25}10<\log_{0.5}3<-\dfrac32$"},
 {"lv": 3, "title": "底が異なる対数の大小（間に有理数をはさむ）",
  "q": r"$\log_{2}3$ と $\log_{3}5$ の大小を比較せよ。",
  "hint": r"底も真数も違うので、そのままでは比べられない。どちらも $1.5$ 前後の値なので、$\dfrac32$ との大小をそれぞれ調べ、$\dfrac32$ を間にはさむ。",
  "sol": r"$3^2=9>8=2^3$ より $3>2^{\frac32}$。底 $2>1$ より　$\log_{2}3>\dfrac32$<br>"
         r"$5^2=25<27=3^3$ より $5<3^{\frac32}$。底 $3>1$ より　$\log_{3}5<\dfrac32$<br>"
         r"よって　$\boldsymbol{\log_{3}5<\log_{2}3}$",
  "note": r"はさむ有理数は、$2<3<4$ から $1<\log_{2}3<2$ のような粗い評価から始め、$2^3$ と $3^2$，$3^3$ と $5^2$ のように小さい累乗を並べて探す。常用対数の近似値を使う方法もあるが、2つの値が近いときは誤差に注意が必要になる。",
  "ex": r"$\log_{3}7$ と $\log_{4}10$ の大小を比較せよ。",
  "exa": r"$\log_{4}10<\log_{3}7$（$3^5=243<343=7^3$ より $\log_{3}7>\dfrac53$，$4^5=1024>10^3$ より $\log_{4}10<\dfrac53$）"},
 {"lv": 4, "title": r"$2^x=3^y=5^z$ のときの大小",
  "q": r"正の数 $x,\ y,\ z$ が $2^{x}=3^{y}=5^{z}$ を満たすとき、$2x,\ 3y,\ 5z$ の大小を比較せよ。",
  "hint": r"共通の値を $k$ とおくと $k>1$。$x,\ y,\ z$ を常用対数で表し、差 $2x-3y$，$5z-2x$ の符号を調べる。分子は $\log_{10}\dfrac98$ のように $1$ との大小がわかる形になる。",
  "sol": r"$2^x=3^y=5^z=k$ とおくと、$x>0$ より $k>2^0=1$ で、$\log_{10}k>0$。各辺の常用対数をとると<br>"
         r"　$x=\dfrac{\log_{10}k}{\log_{10}2}$，$y=\dfrac{\log_{10}k}{\log_{10}3}$，$z=\dfrac{\log_{10}k}{\log_{10}5}$<br>"
         r"$2x-3y=\log_{10}k\left(\dfrac{2}{\log_{10}2}-\dfrac{3}{\log_{10}3}\right)=\log_{10}k\cdot\dfrac{2\log_{10}3-3\log_{10}2}{\log_{10}2\cdot\log_{10}3}=\log_{10}k\cdot\dfrac{\log_{10}\frac98}{\log_{10}2\cdot\log_{10}3}>0$<br>"
         r"$5z-2x=\log_{10}k\left(\dfrac{5}{\log_{10}5}-\dfrac{2}{\log_{10}2}\right)=\log_{10}k\cdot\dfrac{5\log_{10}2-2\log_{10}5}{\log_{10}2\cdot\log_{10}5}=\log_{10}k\cdot\dfrac{\log_{10}\frac{32}{25}}{\log_{10}2\cdot\log_{10}5}>0$<br>"
         r"（$\log_{10}2,\ \log_{10}3,\ \log_{10}5$ はいずれも正，$\dfrac98>1$，$\dfrac{32}{25}>1$ を用いた）<br>"
         r"よって　$\boldsymbol{3y<2x<5z}$",
  "note": r"$2x=\dfrac{\log_{10}k}{\log_{10}\sqrt2}=\log_{\sqrt2}k$，$3y=\log_{\sqrt[3]{3}}k$，$5z=\log_{\sqrt[5]{5}}k$ と見ると、$k>1$ のとき底が大きいほど値は小さい。指数関数の節で調べた $\sqrt[5]{5}<\sqrt2<\sqrt[3]{3}$ と、ちょうど逆の順になる。",
  "ex": r"正の数 $x,\ y,\ z$ が $3^{x}=4^{y}=6^{z}$ を満たすとき、$3x,\ 4y,\ 6z$ の大小を比較せよ。",
  "exa": r"$3x<4y<6z$"},
 {"lv": 4, "title": r"$\log_{n}(n+1)$ の大小（相加平均・相乗平均の利用）",
  "q": r"$n$ を $2$ 以上の整数とするとき、$\log_{n}(n+1)>\log_{n+1}(n+2)$ が成り立つことを証明せよ。",
  "hint": r"底を $n+1$ にそろえると $\log_{n}(n+1)=\dfrac{1}{\log_{n+1}n}$。示す式は $\log_{n+1}n\cdot\log_{n+1}(n+2)<1$ と同値で、この積は相加平均・相乗平均の関係で上から評価できる。",
  "sol": r"$A=\log_{n+1}n$，$B=\log_{n+1}(n+2)$ とおく。$n\geqq2$ より底 $n+1>1$，真数 $n>1$，$n+2>1$ であるから　$A>0$，$B>0$<br>"
         r"$\log_{n}(n+1)=\dfrac{1}{\log_{n+1}n}=\dfrac1A$ であるから、示すべき不等式は $\dfrac1A>B$，すなわち $AB<1$ と同値である。<br>"
         r"相加平均と相乗平均の関係より　$\sqrt{AB}\leqq\dfrac{A+B}{2}=\dfrac{\log_{n+1}n(n+2)}{2}$<br>"
         r"ここで $n(n+2)=(n+1)^2-1<(n+1)^2$ で底 $n+1>1$ だから　$\log_{n+1}n(n+2)<\log_{n+1}(n+1)^2=2$<br>"
         r"よって $\sqrt{AB}<1$，すなわち $AB<1$。ゆえに　$\log_{n}(n+1)>\log_{n+1}(n+2)$　■",
  "note": r"この結果から $\log_{2}3>\log_{3}4>\log_{4}5>\cdots$ がわかる。相加平均・相乗平均の関係は $A>0,\ B>0$ のときに使えるので、正であることを先に確認した。$n=1$ は底が $1$ になるので除いている。",
  "ex": r"$n$ を $3$ 以上の整数とするとき、$\log_{n}(n-1)\cdot\log_{n}(n+1)<1$ を証明せよ。また、これを用いて $\log_{5}6$ と $\log_{6}7$ の大小を比較せよ。",
  "exa": r"両者は正で、相加平均・相乗平均の関係より $\sqrt{\log_{n}(n-1)\log_{n}(n+1)}\leqq\dfrac12\log_{n}(n^2-1)<\dfrac12\log_{n}n^2=1$。$n=6$ として $\log_{6}5\cdot\log_{6}7<1$ より $\log_{6}7<\log_{5}6$"},
 {"lv": 5, "title": "非常に近い2つの対数の大小",
  "q": r"$\log_{6}10$ と $\log_{5}8$ の大小を比較せよ。ただし、常用対数の近似値は用いないこと。",
  "hint": r"2つの値はともに $1.29$ 前後で非常に近い。まず簡単な有理数ではさむと、どちらも $\dfrac54$ と $\dfrac43$ の間にあることがわかる。そこで、その間の分数 $\dfrac{5+4}{4+3}=\dfrac97$ を試す。$\log_{6}10<\dfrac97\iff10^7<6^9$ のように整数の比較に直し、$6^9=216^3$，$8^7=2^{21}$ を利用する。",
  "sol": r"<b>粗い評価</b>　$6^4=1296>10^3$，$6^5=7776<10^4$ より $\dfrac54<\log_{6}10<\dfrac43$。<br>"
         r"また $8^3=512<625=5^4$，$8^4=4096>3125=5^5$ より $\dfrac54<\log_{5}8<\dfrac43$。これでは大小が決まらない。<br>"
         r"<b>$\dfrac97$ との比較</b>　$6^9=\left(6^3\right)^3=216^3=10077696>10^7$ より $6^{\frac97}>10$。底 $6>1$ より　$\log_{6}10<\dfrac97$<br>"
         r"一方 $8^7=2^{21}=2097152$，$5^9=1953125$ より $8^7>5^9$ で、$8>5^{\frac97}$。底 $5>1$ より　$\log_{5}8>\dfrac97$<br>"
         r"よって　$\boldsymbol{\log_{6}10<\log_{5}8}$",
  "note": r"(i) 分数 $\dfrac ab<\dfrac cd$（$b,\ d>0$）の間には必ず $\dfrac{a+c}{b+d}$ がある（中間数）。はさめなければ、さらに中間数をとっていけばよい。<br>"
          r"(ii) $8^7>5^9\iff2^{21}>5^9\iff2^{30}>10^9$ であり、これは $2^{10}=1024>10^3$ から直ちにわかる。$6^9>10^7$ も $216^3>200^3\times1.25=10^7$ と見れば計算が軽い（$1.08^3>1.25$）。<br>"
          r"(iii) $\log_{10}2=0.3010,\ \log_{10}3=0.4771$ を使うと $\log_{6}10\fallingdotseq1.285$，$\log_{5}8\fallingdotseq1.292$ で、差は $0.007$ ほどしかない。近似値で答える場合でも、誤差がこの差より十分小さいことを示さなければ論証にならない。",
  "ex": r"$\log_{6}8$ と $\log_{7}10$ の大小を比較せよ。ただし、常用対数の近似値は用いないこと。",
  "exa": r"$\log_{6}8<\dfrac76<\log_{7}10$（$6^7=279936>262144=8^6$，$7^7=823543<10^6$）"},
]})


@_v
def v6():
    L = lambda b, x: math.log(x) / math.log(b)
    def order(d):
        return sorted(d, key=d.get)
    assert order({"a": 1.5, "b": L(2, 3), "c": L(4, 10)}) == ["a", "b", "c"]
    assert order({"a": L(1 / 3, 2), "b": L(1 / 9, 5), "c": -0.5}) == ["b", "a", "c"]
    assert order({"a": L(3, 5), "b": L(9, 20), "c": 1.5}) == ["b", "a", "c"]
    assert order({"a": L(0.5, 3), "b": L(0.25, 10), "c": -1.5}) == ["b", "a", "c"]
    assert math.isclose(L(4, 10), L(2, 10 ** 0.5)) and math.isclose(L(1 / 9, 5), L(1 / 3, 5 ** 0.5))
    assert 3 ** 2 > 2 ** 3 and 5 ** 2 < 3 ** 3 and L(3, 5) < 1.5 < L(2, 3)
    assert 3 ** 5 == 243 < 7 ** 3 == 343 and 4 ** 5 == 1024 > 10 ** 3 and L(4, 10) < 5 / 3 < L(3, 7)
    # 2^x=3^y=5^z
    for k in [1.01, 2.0, 37.0, 1e6]:
        x, y, z = L(2, k), L(3, k), L(5, k)
        assert 3 * y < 2 * x < 5 * z
        x, y, z = L(3, k), L(4, k), L(6, k)
        assert 3 * x < 4 * y < 6 * z
    assert Fr(9, 8) > 1 and Fr(32, 25) > 1
    # log_n(n+1) の減少
    for n in range(2, 3000):
        assert L(n, n + 1) > L(n + 1, n + 2)
        assert n * (n + 2) < (n + 1) ** 2
    for n in range(3, 3000):
        assert L(n, n - 1) * L(n, n + 1) < 1
    assert L(6, 7) < L(5, 6)
    # 近い2数
    assert 6 ** 4 > 10 ** 3 and 6 ** 5 < 10 ** 4 and 8 ** 3 < 5 ** 4 and 8 ** 4 > 5 ** 5
    assert 216 ** 3 == 6 ** 9 == 10077696 > 10 ** 7 and 8 ** 7 == 2 ** 21 == 2097152 and 5 ** 9 == 1953125
    assert 1.25 < L(6, 10) < 9 / 7 < L(5, 8) < 4 / 3
    assert (8 ** 7 > 5 ** 9) == (2 ** 30 > 10 ** 9) and 216 ** 3 > 200 ** 3 * Fr(5, 4) and Fr(108, 100) ** 3 > Fr(5, 4)
    assert abs(L(5, 8) - L(6, 10) - 0.007) < 0.001
    assert 6 ** 7 == 279936 > 8 ** 6 == 262144 and 7 ** 7 == 823543 < 10 ** 6 and L(6, 8) < 7 / 6 < L(7, 10)


# ---------------------------------------------------------------- 節7
SEC.append({"title": "指数関数・対数関数の最大・最小",
"base": r"""・$a^x=t$ や $\log_{a}x=t$ とおき換えて、2次関数の最大・最小に帰着させる。<b>$t$ の変域</b>を必ず求める<br>
・$t=a^x+a^{-x}$ とおくと、相加平均・相乗平均の関係より $t\geqq2$（等号は $x=0$）で、$a^{2x}+a^{-2x}=t^2-2$<br>
・条件つきの最大・最小は $X=\log_{a}x,\ Y=\log_{a}y$ とおき、条件と式を $X,\ Y$ で表す<br>
・$2^x,\ 2^y$ の対称式は、和 $s$ と積 $p$ で表し、<b>$2^x,\ 2^y$ が正の実数である条件</b>（$s^2\geqq4p,\ s>0,\ p>0$）を加える""",
"items": [
 {"lv": 2, "title": "おき換えによる最大・最小",
  "q": r"次の関数の最大値と最小値を求めよ。また、そのときの $x$ の値を求めよ。<br>(1) $y=4^{x}-2^{x+2}+5\ \ (-1\leqq x\leqq2)$　　(2) $y=\left(\log_{2}\dfrac{x}{2}\right)\left(\log_{2}\dfrac{x}{8}\right)\ \ (1\leqq x\leqq32)$",
  "hint": r"(1) は $2^x=t$，(2) は $\log_{2}x=t$ とおくと $t$ の2次関数。$x$ の範囲から $t$ の範囲を求め、軸と区間の位置関係を見る。",
  "sol": r"(1) $2^x=t$ とおく。$-1\leqq x\leqq2$ より　$\dfrac12\leqq t\leqq4$<br>"
         r"$y=t^2-4t+5=(t-2)^2+1$。$t=4$ のとき $y=5$，$t=\dfrac12$ のとき $y=\dfrac94$ であるから<br>"
         r"　$t=4$，すなわち $\boldsymbol{x=2}$ <b>のとき最大値</b> $\boldsymbol{5}$；$t=2$，すなわち $\boldsymbol{x=1}$ <b>のとき最小値</b> $\boldsymbol{1}$<br>"
         r"(2) $\log_{2}x=t$ とおく。$1\leqq x\leqq32$ より　$0\leqq t\leqq5$<br>"
         r"$y=(t-1)(t-3)=t^2-4t+3=(t-2)^2-1$。$t=5$ のとき $y=8$，$t=0$ のとき $y=3$ であるから<br>"
         r"　$t=5$，すなわち $\boldsymbol{x=32}$ <b>のとき最大値</b> $\boldsymbol{8}$；$t=2$，すなわち $\boldsymbol{x=4}$ <b>のとき最小値</b> $\boldsymbol{-1}$",
  "note": r"最大値は区間の両端の値を比べて決める。答えは $t$ ではなく $x$ の値で答えることを忘れない。",
  "ex": r"次の関数の最大値と最小値を求めよ。また、そのときの $x$ の値を求めよ。<br>(1) $y=9^{x}-2\cdot3^{x+1}+4\ \ (0\leqq x\leqq2)$　　(2) $y=(\log_{3}3x)\left(\log_{3}\dfrac{x}{27}\right)\ \ (1\leqq x\leqq81)$",
  "exa": r"(1) $x=2$ で最大値 $31$，$x=1$ で最小値 $-5$　(2) $x=81$ で最大値 $5$，$x=3$ で最小値 $-4$"},
 {"lv": 3, "title": "条件つきの対数の最大・最小",
  "q": r"$x\geqq1,\ y\geqq1,\ xy^{2}=64$ のとき、$\log_{2}x\cdot\log_{2}y$ の最大値と最小値を求めよ。また、そのときの $x,\ y$ の値を求めよ。",
  "hint": r"$X=\log_{2}x,\ Y=\log_{2}y$ とおくと、条件は $X+2Y=6,\ X\geqq0,\ Y\geqq0$ という1次の条件になる。$X$ を消去すれば $Y$ の2次関数。",
  "sol": r"$X=\log_{2}x,\ Y=\log_{2}y$ とおく。$x\geqq1,\ y\geqq1$ より $X\geqq0,\ Y\geqq0$。<br>"
         r"条件の両辺の $2$ を底とする対数をとって　$X+2Y=6$，すなわち $X=6-2Y$<br>"
         r"$X\geqq0$ より $Y\leqq3$ であるから　$0\leqq Y\leqq3$<br>"
         r"$XY=(6-2Y)Y=-2Y^2+6Y=-2\left(Y-\dfrac32\right)^2+\dfrac92$<br>"
         r"よって $Y=\dfrac32$（$X=3$）のとき最大、$Y=0,\ 3$ のとき最小となる。<br>"
         r"　<b>最大値</b> $\boldsymbol{\dfrac92}$（$\boldsymbol{x=8,\ y=2\sqrt2}$），<b>最小値</b> $\boldsymbol{0}$（$\boldsymbol{x=64,\ y=1}$ または $\boldsymbol{x=1,\ y=8}$）",
  "note": r"$X$ と $Y$ の変域を両方確認する。$X\geqq0$ を忘れて $Y\geqq0$ だけで考えると、最小値がないという誤答になる。最大値は相加平均・相乗平均の関係 $X\cdot2Y\leqq\left(\dfrac{X+2Y}{2}\right)^2=9$ からも求められる。",
  "ex": r"$x\geqq1,\ y\geqq1,\ x^{2}y=27$ のとき、$\log_{3}x\cdot\log_{3}y$ の最大値と最小値を求めよ。また、そのときの $x,\ y$ の値を求めよ。",
  "exa": r"最大値 $\dfrac98$（$x=3^{\frac34},\ y=3\sqrt3$），最小値 $0$（$x=1,\ y=27$ または $x=3\sqrt3,\ y=1$）"},
 {"lv": 3, "title": "$t=2^x+2^{-x}$ とおく最小値",
  "q": r"関数 $y=4^{x}+4^{-x}-6\left(2^{x}+2^{-x}\right)+10$ の最小値と、そのときの $x$ の値を求めよ。",
  "hint": r"$t=2^x+2^{-x}$ とおくと $4^x+4^{-x}=t^2-2$。$t$ の変域は相加平均・相乗平均の関係から $t\geqq2$。最小値を与える $t$ から $x$ に戻すときは、$2^x$ の2次方程式を解く。",
  "sol": r"$t=2^x+2^{-x}$ とおく。$2^x>0,\ 2^{-x}>0$ であるから、相加平均・相乗平均の関係より<br>"
         r"　$t\geqq2\sqrt{2^x\cdot2^{-x}}=2$（等号は $2^x=2^{-x}$，すなわち $x=0$ のとき）<br>"
         r"また、$t\geqq2$ のどの値に対しても $u+\dfrac1u=t$ を満たす $u>0$ があり、$x=\log_{2}u$ とすればよいから、$t$ は $2$ 以上のすべての値をとる。<br>"
         r"$4^x+4^{-x}=\left(2^x+2^{-x}\right)^2-2=t^2-2$ より　$y=t^2-2-6t+10=t^2-6t+8=(t-3)^2-1$<br>"
         r"$t\geqq2$ の範囲で、$y$ は $t=3$ のとき最小値 $-1$ をとる。<br>"
         r"$t=3$ のとき $2^x=u$ とおくと $u+\dfrac1u=3$，$u^2-3u+1=0$ より $u=\dfrac{3\pm\sqrt5}{2}$（ともに正）<br>"
         r"よって　<b>最小値</b> $\boldsymbol{-1}$（$\boldsymbol{x=\log_{2}\dfrac{3\pm\sqrt5}{2}}$）",
  "note": r"$\dfrac{3+\sqrt5}{2}\cdot\dfrac{3-\sqrt5}{2}=1$ なので、2つの $x$ の値は互いに符号が反対である。$y$ は $x$ を $-x$ にしても変わらない（偶関数）ことと対応している。",
  "ex": r"関数 $y=9^{x}+9^{-x}-8\left(3^{x}+3^{-x}\right)+10$ の最小値と、そのときの $x$ の値を求めよ。",
  "exa": r"最小値 $-8$（$x=\log_{3}\left(2\pm\sqrt3\right)$）"},
 {"lv": 4, "title": "文字を含む関数の最小値（軸の位置で場合分け）",
  "q": r"$a$ を実数の定数とする。関数 $f(x)=4^{x}+4^{-x}-2a\left(2^{x}+2^{-x}\right)$ の最小値 $m(a)$ を求めよ。また、$m(a)=-11$ となる $a$ の値を求めよ。",
  "hint": r"$t=2^x+2^{-x}\ (t\geqq2)$ とおくと、$f$ は $t$ の2次関数 $(t-a)^2-a^2-2$。軸 $t=a$ が区間 $t\geqq2$ に入るかどうかで場合を分ける。",
  "sol": r"$t=2^x+2^{-x}$ とおくと、前の例題と同様に $t$ は $2$ 以上のすべての値をとる。<br>"
         r"$f(x)=t^2-2-2at=(t-a)^2-a^2-2$。これを $g(t)$ とおく（$t\geqq2$）。<br>"
         r"(i) $a\geqq2$ のとき：軸 $t=a$ は区間内にあるから、$g(t)$ は $t=a$ で最小。　$m(a)=-a^2-2$<br>"
         r"(ii) $a<2$ のとき：$t\geqq2$ で $g(t)$ は増加するから、$t=2$ で最小。　$m(a)=g(2)=2-4a$<br>"
         r"よって　$\boldsymbol{m(a)=-a^2-2\ (a\geqq2),\ \ m(a)=2-4a\ (a<2)}$<br>"
         r"$m(a)=-11$ となる $a$：(i) $-a^2-2=-11$ より $a^2=9$，$a\geqq2$ より $a=3$。(ii) $2-4a=-11$ より $a=\dfrac{13}{4}$ で、$a<2$ を満たさない。<br>"
         r"ゆえに　$\boldsymbol{a=3}$",
  "note": r"$m(a)$ のグラフをかくと、$a<2$ では直線、$a\geqq2$ では放物線の一部で、$a=2$ でつながっている（ともに $-6$）。場合分けの境目の値を両方の式に代入して一致することを確かめると、計算の誤りに気づきやすい。",
  "ex": r"$a$ を実数の定数とする。関数 $f(x)=9^{x}+9^{-x}-4a\left(3^{x}+3^{-x}\right)+1$ の最小値 $m(a)$ を求めよ。また、$m(a)=-17$ となる $a$ の値を求めよ。",
  "exa": r"$m(a)=-4a^2-1\ (a\geqq1)$，$m(a)=3-8a\ (a<1)$；$a=2$"},
 {"lv": 5, "title": "指数の対称式の値域（正の実数条件と増減）",
  "q": r"実数 $x,\ y$ が $4^{x}+4^{y}=2^{x+1}+2^{y+1}$ を満たしながら動くとき、<br>(1) $s=2^{x}+2^{y}$ のとり得る値の範囲を求めよ。<br>(2) $8^{x}+8^{y}$ のとり得る値の範囲を求めよ。",
  "hint": r"$X=2^x,\ Y=2^y$ とおくと $X>0,\ Y>0$ で、条件は $X^2+Y^2=2(X+Y)$。和 $s$ と積 $p=XY$ で表し、<b>$X,\ Y$ が正の実数として存在する条件</b>を求める。(2) は $s$ の3次式になる。微分を使わずに増減を調べるには、$s_1<s_2$ に対して差 $F(s_2)-F(s_1)$ の符号を調べる。",
  "sol": r"(1) $X=2^x,\ Y=2^y$ とおくと $X>0,\ Y>0$ で、条件は $X^2+Y^2=2(X+Y)$。$s=X+Y,\ p=XY$ とおくと<br>"
         r"　$s^2-2p=2s$ より　$p=\dfrac{s^2-2s}{2}$ …①<br>"
         r"$X,\ Y$ は $u$ の2次方程式 $u^2-su+p=0$ の2解であるから、正の実数 $X,\ Y$ が存在する条件は<br>"
         r"　$s^2-4p\geqq0$，$s>0$，$p>0$<br>"
         r"①を代入すると　$s^2-4p=-s^2+4s=s(4-s)\geqq0$，$p=\dfrac{s(s-2)}{2}>0$<br>"
         r"$s>0$ のもとで、これらは $s\leqq4$ かつ $s>2$。逆に $2<s\leqq4$ なら正の $X,\ Y$ が定まり、$x=\log_{2}X,\ y=\log_{2}Y$ が条件を満たす。<br>"
         r"よって　$\boldsymbol{2<s\leqq4}$<br>"
         r"(2) $8^x+8^y=X^3+Y^3=s^3-3ps=s^3-\dfrac{3s(s^2-2s)}{2}=-\dfrac12s^3+3s^2$。これを $F(s)$ とおく。<br>"
         r"$2<s_1<s_2\leqq4$ のとき<br>"
         r"　$F(s_2)-F(s_1)=3\left(s_2^2-s_1^2\right)-\dfrac12\left(s_2^3-s_1^3\right)=(s_2-s_1)\left\{3(s_1+s_2)-\dfrac12\left(s_1^2+s_1s_2+s_2^2\right)\right\}$<br>"
         r"ここで $s_1<4,\ s_2\leqq4$ より $s_1^2<4s_1$，$s_1s_2\leqq4s_1$，$s_2^2\leqq4s_2$ であるから<br>"
         r"　$s_1^2+s_1s_2+s_2^2<8s_1+4s_2=6(s_1+s_2)-2(s_2-s_1)<6(s_1+s_2)$<br>"
         r"よって $\{\ \}$ 内は正で、$F(s_2)>F(s_1)$。すなわち $F(s)$ は $2<s\leqq4$ で増加する。<br>"
         r"$F(2)=-4+12=8$，$F(4)=-32+48=16$ であり、$F(s)$ は連続に変化するから、$F(s)$ のとり得る値の範囲は $8<F(s)\leqq16$。<br>"
         r"よって　$\boldsymbol{8<8^x+8^y\leqq16}$（最大値 $16$ は $x=y=1$ のとき。最小値はない）",
  "note": r"$XY$ 平面で見ると、条件は円 $(X-1)^2+(Y-1)^2=2$ のうち $X>0,\ Y>0$ の部分、すなわち点 $(2,\ 0)$ から $(2,\ 2)$ を通って $(0,\ 2)$ に至る弧（両端を除く）であり、$s$ はこの弧と直線 $X+Y=s$ が共有点をもつ範囲として $2<s\leqq4$ と求めることもできる。$p>0$ の条件を落とすと「$0<s\leqq4$」という誤答になる。(2) は数学IIの微分を学ぶと、$F'(s)=\dfrac32s(4-s)\geqq0$ から増加がすぐにわかる。",
  "ex": r"実数 $x,\ y$ が $9^{x}+9^{y}=3^{x+1}+3^{y+1}$ を満たしながら動くとき、(1) $3^{x}+3^{y}$，(2) $27^{x}+27^{y}$ のとり得る値の範囲をそれぞれ求めよ。",
  "exa": r"(1) $3<3^x+3^y\leqq6$　(2) $27<27^x+27^y\leqq54$"},
]})


@_v
def v7():
    def mm(f, lo, hi, n=20000):
        v = [f(lo + (hi - lo) * k / n) for k in range(n + 1)]
        return max(v), min(v)
    M, m = mm(lambda x: 4 ** x - 2 ** (x + 2) + 5, -1, 2)
    assert math.isclose(M, 5) and math.isclose(m, 1, abs_tol=1e-6)
    assert 4 ** 2 - 2 ** 4 + 5 == 5 and 4 - 8 + 5 == 1
    M, m = mm(lambda x: math.log2(x / 2) * math.log2(x / 8), 1, 32, 200000)
    assert math.isclose(M, 8) and math.isclose(m, -1, abs_tol=1e-6)
    M, m = mm(lambda x: 9 ** x - 2 * 3 ** (x + 1) + 4, 0, 2)
    assert math.isclose(M, 31) and math.isclose(m, -5, abs_tol=1e-6)
    L3 = lambda x: math.log(x) / math.log(3)
    M, m = mm(lambda x: L3(3 * x) * L3(x / 27), 1, 81, 400000)
    assert math.isclose(M, 5) and math.isclose(m, -4, abs_tol=1e-6)
    # 条件つき
    M, m = mm(lambda Y: (6 - 2 * Y) * Y, 0, 3)
    assert math.isclose(M, 4.5) and m == 0
    x, y = 8, 2 * 2 ** 0.5
    assert math.isclose(x * y * y, 64) and math.isclose(math.log2(x) * math.log2(y), 4.5)
    M, m = mm(lambda X: X * (3 - 2 * X), 0, 1.5)
    assert math.isclose(M, 9 / 8) and abs(m) < 1e-12
    x, y = 3 ** 0.75, 3 * 3 ** 0.5
    assert math.isclose(x * x * y, 27) and math.isclose(L3(x) * L3(y), 9 / 8)
    assert math.isclose((3 * 3 ** 0.5) ** 2 * 1, 27)
    # t = 2^x + 2^-x
    f = lambda x: 4 ** x + 4 ** -x - 6 * (2 ** x + 2 ** -x) + 10
    M, m = mm(f, -6, 6, 200000)
    assert math.isclose(m, -1, abs_tol=1e-6)
    for u in [(3 + 5 ** 0.5) / 2, (3 - 5 ** 0.5) / 2]:
        assert math.isclose(f(math.log2(u)), -1)
    g = lambda x: 9 ** x + 9 ** -x - 8 * (3 ** x + 3 ** -x) + 10
    M, m = mm(g, -6, 6, 200000)
    assert math.isclose(m, -8, abs_tol=1e-6)
    for u in [2 + 3 ** 0.5, 2 - 3 ** 0.5]:
        assert math.isclose(g(L3(u)), -8)
    # m(a)
    for a in [k / 4 for k in range(-20, 30)]:
        h = lambda t: t * t - 2 - 2 * a * t
        _, m = mm(h, 2, 40, 76000)
        assert math.isclose(m, (-a * a - 2) if a >= 2 else (2 - 4 * a), abs_tol=1e-5)
        h = lambda t: t * t - 2 - 4 * a * t + 1
        _, m = mm(h, 2, 60, 116000)
        assert math.isclose(m, (-4 * a * a - 1) if a >= 1 else (3 - 8 * a), abs_tol=1e-5)
    assert -3 ** 2 - 2 == -11 and Fr(13, 4) >= 2 and -4 * 2 ** 2 - 1 == -17 and Fr(5, 2) >= 1
    assert -2 ** 2 - 2 == 2 - 4 * 2 == -6
    # 対称式（円弧のパラメータ表示）
    for c in [2, 3]:          # X^2+Y^2 = c(X+Y)
        r = c / 2 ** 0.5
        S, F = [], []
        for k in range(1, 200000):
            th = 2 * math.pi * k / 200000
            X, Y = c / 2 + r * math.cos(th), c / 2 + r * math.sin(th)
            if X > 1e-9 and Y > 1e-9:
                assert abs(X * X + Y * Y - c * (X + Y)) < 1e-9
                S.append(X + Y); F.append(X ** 3 + Y ** 3)
        assert math.isclose(max(S), 2 * c) and abs(min(S) - c) < 1e-3 and min(S) > c
        assert math.isclose(max(F), 2 * c ** 3) and abs(min(F) - c ** 3) < 0.05 and min(F) > c ** 3
    Fs = lambda s: -s ** 3 / 2 + 3 * s * s
    assert Fs(2) == 8 and Fs(4) == 16
    for _ in range(20000):
        s1, s2 = sorted(random.uniform(2, 4) for _ in range(2))
        if s2 - s1 < 1e-9:
            continue
        assert s1 * s1 + s1 * s2 + s2 * s2 < 8 * s1 + 4 * s2 < 6 * (s1 + s2) and Fs(s2) > Fs(s1)
    assert -27 / 2 + 81 / 2 == 27 and -216 / 2 + 9 * 36 / 2 == 54


# ---------------------------------------------------------------- 節8
_T46 = (r'<table><tr><th>$r$</th>' + "".join(f"<td>${r}$</td>" for r in range(10)) + "</tr>"
        r'<tr><th>$2^r$</th>' + "".join(f"<td>${2 ** r}$</td>" for r in range(10)) + "</tr>"
        r'<tr><th>$M$ の最高位</th>' + "".join(f"<td>{d}</td>" for d in ["$1$", "$2$", "$4$", "$8$", "$1$", "$3$", "$6$ か $7$", "$1$", "$2$", "$5$"]) + "</tr></table>")

SEC.append({"title": "常用対数（桁数・最高位・小数首位）とその応用",
"base": r"""・正の数 $N$ の整数部分が $n$ 桁 $\iff10^{n-1}\leqq N<10^{n}\iff n-1\leqq\log_{10}N<n$<br>
・$N$ の小数第 $n$ 位に初めて $0$ でない数字が現れる $\iff10^{-n}\leqq N<10^{-n+1}\iff-n\leqq\log_{10}N<-n+1$<br>
・$\log_{10}N=n+\alpha$（$n$ は整数，$0\leqq\alpha<1$）のとき、$\log_{10}k\leqq\alpha<\log_{10}(k+1)$ を満たす整数 $k$ が $N$ の最高位の数字<br>
・$\log_{10}5=1-\log_{10}2$，$\log_{10}0.8=3\log_{10}2-1$ のように、与えられた値から必要な常用対数をつくる""",
"items": [
 {"lv": 1, "title": "桁数と小数首位",
  "q": r"$\log_{10}2=0.3010,\ \log_{10}3=0.4771$ とする。<br>(1) $6^{30}$ は何桁の整数か。<br>(2) $\left(\dfrac23\right)^{30}$ を小数で表すと、小数第何位に初めて $0$ でない数字が現れるか。",
  "hint": r"常用対数をとり、$n-1\leqq\log_{10}N<n$ となる整数 $n$ を求める。負の数のときは、$-5.283$ が $-6$ と $-5$ の間にあることに注意。",
  "sol": r"(1) $\log_{10}6^{30}=30(\log_{10}2+\log_{10}3)=30\times0.7781=23.343$<br>"
         r"$23\leqq\log_{10}6^{30}<24$ より $10^{23}\leqq6^{30}<10^{24}$。よって　$\boldsymbol{24}$ <b>桁</b><br>"
         r"(2) $\log_{10}\left(\dfrac23\right)^{30}=30(\log_{10}2-\log_{10}3)=30\times(-0.1761)=-5.283$<br>"
         r"$-6\leqq-5.283<-5$ より $10^{-6}\leqq\left(\dfrac23\right)^{30}<10^{-5}$。よって　<b>小数第</b> $\boldsymbol{6}$ <b>位</b>",
  "note": r"$10^{-6}=0.000001$ は小数第6位に初めて $1$ が現れる数なので、$10^{-6}\leqq N<10^{-5}$ なら小数第6位。$-5.283$ の整数部分を「$-5$」と考えて小数第5位とする誤りが多い。",
  "ex": r"$\log_{10}2=0.3010,\ \log_{10}3=0.4771$ とする。(1) $12^{20}$ は何桁の整数か。(2) $\left(\dfrac16\right)^{20}$ は、小数第何位に初めて $0$ でない数字が現れるか。",
  "exa": r"(1) $22$ 桁　(2) 小数第 $16$ 位"},
 {"lv": 2, "title": "くり返し減少する量（常用対数の応用）",
  "q": r"$\log_{10}2=0.3010$ とする。光がある種類のガラス板を1枚通過するごとに、その強さが $20\%$ ずつ失われる。光の強さを最初の $1\%$ 以下にするには、このガラス板を少なくとも何枚重ねればよいか。",
  "hint": r"$n$ 枚通過後の強さは最初の $(0.8)^n$ 倍。不等式 $(0.8)^n\leqq0.01$ の両辺の常用対数をとる。$\log_{10}0.8<0$ で割るので不等号の向きが変わる。",
  "sol": r"$n$ 枚重ねたとき、光の強さは最初の $(0.8)^n$ 倍になる。$(0.8)^n\leqq0.01$ となる最小の自然数 $n$ を求める。<br>"
         r"両辺の常用対数をとると　$n\log_{10}0.8\leqq-2$<br>"
         r"$\log_{10}0.8=\log_{10}\dfrac{2^3}{10}=3\times0.3010-1=-0.0970$ より　$-0.0970n\leqq-2$<br>"
         r"$n\geqq\dfrac{2}{0.0970}=20.6\cdots$。よって　$\boldsymbol{21}$ <b>枚</b>",
  "note": r"「$20\%$ ずつ失われる」は「毎回 $0.8$ 倍になる」こと。$1-0.2\times n$ のように引き算で考えるのは誤り。$(0.8)^{20}=0.0115\cdots$，$(0.8)^{21}=0.0092\cdots$ である。",
  "ex": r"$\log_{10}2=0.3010,\ \log_{10}3=0.4771,\ \log_{10}7=0.8451$ とする。年利 $5\%$ の1年ごとの複利で預金したとき、元利合計が初めて元金の $3$ 倍を超えるのは何年後か。",
  "exa": r"$23$ 年後（$\log_{10}1.05=0.0212$，$n>22.5\cdots$）"},
 {"lv": 3, "title": "桁数と最高位の数字",
  "q": r"$\log_{10}2=0.3010,\ \log_{10}3=0.4771,\ \log_{10}7=0.8451$ とする。$3^{50}$ は何桁の整数か。また、$3^{50}$ の最高位の数字と一の位の数字を求めよ。",
  "hint": r"$\log_{10}3^{50}=23.855$ の整数部分 $23$ で桁数が、小数部分 $0.855$ で最高位の数字が決まる。$0.855$ が $\log_{10}k$ と $\log_{10}(k+1)$ のどの間にあるかを調べる。一の位は周期性を使う。",
  "sol": r"$\log_{10}3^{50}=50\times0.4771=23.855$ より $10^{23}<3^{50}<10^{24}$。よって　$\boldsymbol{24}$ <b>桁</b><br>"
         r"また $3^{50}=10^{23.855}=10^{0.855}\times10^{23}$ である。<br>"
         r"$\log_{10}7=0.8451$，$\log_{10}8=3\log_{10}2=0.9030$ で、$0.8451<0.855<0.9030$ より $7<10^{0.855}<8$<br>"
         r"よって、最高位の数字は　$\boldsymbol{7}$<br>"
         r"一の位：$3^1,\ 3^2,\ 3^3,\ 3^4,\ \cdots$ の一の位は $3,\ 9,\ 7,\ 1$ をくり返す。$50=4\times12+2$ より、一の位の数字は　$\boldsymbol{9}$",
  "note": r"最高位の数字を調べるには、小数部分と $\log_{10}2,\ \log_{10}3,\ \cdots,\ \log_{10}9$ の値を比べる。$\log_{10}4=0.6020$，$\log_{10}5=0.6990$，$\log_{10}6=0.7781$，$\log_{10}8=0.9030$，$\log_{10}9=0.9542$ は与えられた値から作れる。実際 $3^{50}=717897987691852588770249$ である。",
  "ex": r"$\log_{10}2=0.3010,\ \log_{10}3=0.4771,\ \log_{10}7=0.8451$ とする。$7^{30}$ は何桁の整数か。また、最高位の数字と一の位の数字を求めよ。",
  "exa": r"$26$ 桁，最高位の数字 $2$，一の位の数字 $9$"},
 {"lv": 4, "title": "$2^n$ と $5^n$ の桁数の和",
  "q": r"$n$ を正の整数とする。$2^{n}$ の桁数と $5^{n}$ の桁数の和は $n+1$ であることを証明せよ。",
  "hint": r"$2^n$ が $a$ 桁、$5^n$ が $b$ 桁なら $10^{a-1}\leqq2^n<10^a$，$10^{b-1}\leqq5^n<10^b$。辺々を掛けると $10^n$ がはさまれる。等号が成り立たない（$2^n$ は $10$ の累乗でない）ことが鍵。",
  "sol": r"$2^n$ を $a$ 桁、$5^n$ を $b$ 桁の整数とすると　$10^{a-1}\leqq2^n<10^a$，$10^{b-1}\leqq5^n<10^b$<br>"
         r"$n\geqq1$ のとき、$2^n$ は素因数 $5$ をもたないから、$10$ の累乗 $10^m=2^m5^m$（$m\geqq1$）にはならず、また $2^n\neq1$ である。よって $2^n\neq10^{a-1}$ で、$10^{a-1}<2^n$。同様に $5^n$ は素因数 $2$ をもたないから $10^{b-1}<5^n$。<br>"
         r"したがって　$10^{a-1}<2^n<10^a$，$10^{b-1}<5^n<10^b$<br>"
         r"辺々を掛けると　$10^{a+b-2}<2^n5^n=10^n<10^{a+b}$<br>"
         r"よって $a+b-2<n<a+b$ で、$n$ は整数だから $n=a+b-1$。ゆえに　$a+b=n+1$　■",
  "note": r"常用対数で言い換えると、$[x]$ を $x$ を超えない最大の整数として $[n\log_{10}2]+[n\log_{10}5]=n-1$ ということ。$n\log_{10}2+n\log_{10}5=n$ は整数で、$n\log_{10}2$ が整数でないことが本質である。",
  "ex": r"$n$ を正の整数とする。$2^{n}$ と $5^{n}$ の最高位の数字が一致するならば、その数字は $3$ であることを証明せよ（例えば $2^5=32$，$5^5=3125$）。",
  "exa": r"$2^n=A\cdot10^p$，$5^n=B\cdot10^q$（$1<A<10,\ 1<B<10$，$p,\ q$ は整数）とおくと $AB=10^{n-p-q}$ で $1<AB<100$ より $AB=10$。最高位を $d$ とすると $d\leqq A,\ B<d+1$ より $d^2\leqq10<(d+1)^2$，よって $d=3$"},
 {"lv": 5, "title": "最高位の数字が $1$ になる個数",
  "q": r"$\log_{10}2=0.3010$ とする。$2^{1},\ 2^{2},\ 2^{3},\ \cdots,\ 2^{100}$ のうち、最高位の数字が $1$ であるものはいくつあるか。",
  "hint": r"100個の小数部分を1つずつ調べるのは無理。$2^{n-1}$ を2倍して $2^n$ をつくるとき、<b>桁数が1つ増えるのは、ちょうど $2^n$ の最高位の数字が $1$ になるとき</b>であることを示せば、個数は「桁数が増える回数」に等しくなる。",
  "sol": r"$n\geqq1$ とし、$2^{n-1}$ が $k$ 桁であるとする。$10^{k-1}\leqq2^{n-1}<10^{k}$ より　$2\cdot10^{k-1}\leqq2^{n}<2\cdot10^{k}$<br>"
         r"・$2^n<10^k$ のとき：$2\cdot10^{k-1}\leqq2^n<10^k$ より、$2^n$ は $k$ 桁で、最高位の数字は $2$ 以上。<br>"
         r"・$2^n\geqq10^k$ のとき：$10^k\leqq2^n<2\cdot10^k$ より、$2^n$ は $k+1$ 桁で、最高位の数字は $1$。<br>"
         r"よって、$2^n$ の最高位の数字が $1$ であるのは、$2^n$ の桁数が $2^{n-1}$ の桁数より1つ増えるときであり、そのときに限る。また、桁数が一度に2つ以上増えることはない。<br>"
         r"$2^0=1$ は $1$ 桁である。また $\log_{10}2^{100}=100\times0.3010=30.10$ より $10^{30}<2^{100}<10^{31}$ で、$2^{100}$ は $31$ 桁。<br>"
         r"$2^0,\ 2^1,\ \cdots,\ 2^{100}$ と進む間に桁数は $1$ から $31$ まで1つずつ増えるから、桁数が増える $n$（$1\leqq n\leqq100$）はちょうど $31-1=30$ 個ある。<br>"
         r"ゆえに、最高位の数字が $1$ であるものは　$\boldsymbol{30}$ <b>個</b>",
  "note": r"$\log_{10}2$ の真の値は $0.30102\cdots$ で、$100$ 倍しても誤差は $0.005$ 程度。$30.10$ の小数部分 $0.10$ に比べて十分小さいので、「$31$ 桁」は近似値によらず確実である。同じ考え方で、$2^1$ から $2^N$ までに最高位が $1$ のものは「$2^N$ の桁数 $-1$」個ある。",
  "ex": r"$\log_{10}2=0.3010$ とする。$5^{1},\ 5^{2},\ \cdots,\ 5^{100}$ のうち、最高位の数字が $5$ 以上であるものはいくつあるか。",
  "exa": r"$31$ 個（桁数が増えるのは最高位が $1\sim4$ のときで、$5^{100}$ は $70$ 桁より $69$ 回。$100-69=31$）"},
 {"lv": 5, "title": "最高位の数字が $7$ となる最小の指数",
  "q": r"$2^{n}$ の最高位の数字が $7$ となるような正の整数 $n$ のうち、最小のものを求めよ。ただし、$2^{10}=1024$ を利用してよいが、常用対数の近似値は用いないこと。",
  "hint": r"$n=10k+r\ (0\leqq r\leqq9)$ と分けると $2^n=2^r\cdot1.024^k\cdot10^{3k}$。$1.024^k$ は $k$ が小さいうちは $1$ に近いので、最高位の数字は $2^r$ でほぼ決まる。どの $r$ で、いつ $7$ が現れ得るかを不等式で絞り込む。",
  "sol": r"$n=10k+r$（$k\geqq0$，$0\leqq r\leqq9$ の整数）とおく。$2^{10}=1024=1.024\times10^3$ より<br>"
         r"　$2^n=2^r\cdot1024^k=M\times10^{3k}$，$M=2^r\cdot1.024^k$<br>"
         r"であるから、$2^n$ の最高位の数字は $M$ の最高位の数字に等しい。<br>"
         r"$k\leqq4$ のとき、$1\leqq1.024^k\leqq1.024^4=1.099511627776<1.1$ であるから　$2^r\leqq M<1.1\times2^r$<br>"
         r"これより、$k\leqq4$ における $M$ の最高位の数字は次のようになる。<br>" + _T46 +
         r"$r=6$ のとき $64\leqq M<70.4$ で、最高位が $7$ になるのは $M\geqq70$，すなわち $1.024^k\geqq\dfrac{70}{64}=1.09375$ のときである。<br>"
         r"$1.024^3=1.073741824<1.09375$，$1.024^4=1.099511627776>1.09375$<br>"
         r"よって $n\leqq49$（$k\leqq4$）の範囲で最高位が $7$ となるのは $k=4,\ r=6$，すなわち $n=46$ のときだけである（$M=64\times1.0995\cdots=70.36\cdots$）。<br>"
         r"ゆえに、求める最小の $n$ は　$\boldsymbol{n=46}$",
  "note": r"常用対数で考えると、$46\log_{10}2$ の小数部分と $\log_{10}7$ の比較になる。$\log_{10}2=0.3010,\ \log_{10}7=0.8451$ を使うと $46\times0.3010=13.846$ で、小数部分 $0.846$ と $0.8451$ の差は $0.001$ 未満しかない。一方、近似値の誤差は $46$ 倍されて最大 $0.0023$ 程度になり得るので、4桁の近似値だけでは結論が確定しない。整数の計算で議論すると確実である。実際 $2^{46}=70368744177664$。",
  "ex": r"$2^{n}$ の最高位の数字が $9$ となるような正の整数 $n$ のうち、最小のものを求めよ（$2^{10}=1024$ を利用してよい）。",
  "exa": r"$n=53$（$k\leqq4$ では最高位 $9$ は現れず、$k=5$ で $r=3$ のとき $M=8\times1.024^5=9.007\cdots$）"},
]})


def _lead(N):
    return int(str(N)[0])


@_v
def v8():
    nd = lambda N: len(str(N))
    # 桁数・小数首位
    assert nd(6 ** 30) == 24 == math.floor(30 * (0.3010 + 0.4771)) + 1
    v = Fr(2, 3) ** 30
    assert Fr(1, 10 ** 6) <= v < Fr(1, 10 ** 5) and math.floor(30 * (0.3010 - 0.4771)) == -6
    assert nd(12 ** 20) == 22 == math.floor(20 * 1.0791) + 1
    v = Fr(1, 6) ** 20
    assert Fr(1, 10 ** 16) <= v < Fr(1, 10 ** 15) and math.floor(20 * -0.7781) == -16
    # 応用
    n = 1
    while Fr(4, 5) ** n > Fr(1, 100):
        n += 1
    assert n == 21 == math.ceil(2 / 0.0970) and abs((3 * 0.3010 - 1) + 0.0970) < 1e-12
    n = 1
    while Fr(21, 20) ** n <= 3:
        n += 1
    l105 = 0.4771 + (1 - 0.3010) + 0.8451 - 2
    assert n == 23 == math.floor(0.4771 / l105) + 1 and abs(l105 - 0.0212) < 1e-9
    # 最高位
    N = 3 ** 50
    assert nd(N) == 24 and _lead(N) == 7 and N % 10 == 9 and str(N) == "717897987691852588770249"
    assert 0.8451 < round(50 * 0.4771, 4) - 23 < 0.9030
    N = 7 ** 30
    assert nd(N) == 26 and _lead(N) == 2 and N % 10 == 9 and 0.3010 < round(30 * 0.8451, 4) - 25 < 0.4771
    # 2^n と 5^n
    for n in range(1, 2500):
        a, b = 2 ** n, 5 ** n
        assert nd(a) + nd(b) == n + 1
        if _lead(a) == _lead(b):
            assert _lead(a) == 3
    assert _lead(2 ** 5) == _lead(5 ** 5) == 3
    # 最高位が 1 の個数
    for n in range(1, 1500):
        assert (_lead(2 ** n) == 1) == (nd(2 ** n) == nd(2 ** (n - 1)) + 1)
        assert nd(2 ** n) - nd(2 ** (n - 1)) in (0, 1)
        assert (_lead(5 ** n) <= 4) == (nd(5 ** n) == nd(5 ** (n - 1)) + 1)
    assert sum(1 for n in range(1, 101) if _lead(2 ** n) == 1) == 30 == nd(2 ** 100) - 1
    assert nd(2 ** 100) == 31 == math.floor(100 * 0.3010) + 1
    assert sum(1 for n in range(1, 101) if _lead(5 ** n) >= 5) == 31 and nd(5 ** 100) == 70 == math.floor(100 * 0.6990) + 1
    # 最高位が 7, 9 となる最小の n
    assert min(n for n in range(1, 200) if _lead(2 ** n) == 7) == 46 and 2 ** 46 == 70368744177664
    assert min(n for n in range(1, 200) if _lead(2 ** n) == 9) == 53
    q = Fr(1024, 1000)
    assert q ** 3 == Fr(1073741824, 10 ** 9) and q ** 4 == Fr(1099511627776, 10 ** 12)
    assert q ** 3 < Fr(70, 64) < q ** 4 < Fr(11, 10) and Fr(70, 64) == Fr(109375, 100000)
    for k in range(5):
        for r in range(10):
            M = 2 ** r * q ** k
            assert 2 ** r <= M < Fr(11, 10) * 2 ** r
            lead = _lead(2 ** (10 * k + r))
            exp = [1, 2, 4, 8, 1, 3, None, 1, 2, 5][r]
            assert lead == exp if exp else lead in (6, 7)
            assert lead != 9
    assert 8 * q ** 5 > 9 and abs(8 * float(q) ** 5 - 9.007) < 1e-3 and _lead(2 ** 53) == 9
    assert abs(46 * 0.3010 - 13 - 0.8451) < 0.001 and 46 * 0.00005 < 0.0024


CH = {"no": 13, "sections": SEC}


def verify():
    for f in VS:
        f()
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert 4 <= len(SEC) <= 9 and abs(len(items) - 35) <= 3, len(items)
    assert cnt[5] >= 3 and all(cnt[k] >= 4 for k in range(1, 5)), cnt
    for s in SEC:                        # 節の中は易しい順
        lv = [it["lv"] for it in s["items"]]
        assert lv == sorted(lv), s["title"]
    for it in items:
        for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
            assert it.get(k), (it["title"], k)
        for k in ("q", "hint", "sol", "note", "ex", "exa"):
            t = it.get(k, "")
            assert "$$" not in t and t.count("$") % 2 == 0, (it["title"], k)
    print("c13:", len(SEC), "節", len(items), "題", cnt)
