"""書式の見本（第1章 数と式 の一部）。本番の c01.py ではない。構成と書き方だけを参考にすること。
節ごとに SEC.append(...) を足していき、最後に CH と verify を置く。節を書き終えるたびに保存する。"""
from sympy import symbols, expand, factor, sqrt, Rational, simplify
import random

SEC = []

# ---------------------------------------------------------------- 節1
SEC.append({"title": "式の展開と因数分解",
"base": r"""・乗法公式：$(a+b)^2=a^2+2ab+b^2$，$(a+b)(a-b)=a^2-b^2$，$(x+a)(x+b)=x^2+(a+b)x+ab$，$(ax+b)(cx+d)=acx^2+(ad+bc)x+bd$<br>
・因数分解の手順：① 共通因数をくくる　② 公式の形を探す　③ たすきがけ　④ 最も次数の低い文字について整理する""",
"items": [
 {"lv": 1, "title": "たすきがけによる因数分解",
  "q": r"$6x^2+x-12$ を因数分解せよ。",
  "hint": r"$x^2$ の係数 $6$ と定数項 $-12$ をそれぞれ2数の積に分け、「たすき」に掛けた和が $x$ の係数 $1$ になる組を探す。",
  "sol": r"$6=2\cdot3$，$-12=3\cdot(-4)$ と分けると $2\cdot(-4)+3\cdot3=1$ となる。<br>よって　$6x^2+x-12=\boldsymbol{(2x+3)(3x-4)}$",
  "note": r"展開して元に戻ることを確かめる習慣をつけよう：$(2x+3)(3x-4)=6x^2-8x+9x-12$。",
  "ex": r"$8x^2-2x-15$ を因数分解せよ。",
  "exa": r"$(2x-3)(4x+5)$"},
 {"lv": 3, "title": "複2次式の因数分解（平方の差をつくる）",
  "q": r"$x^4-6x^2+1$ を、係数が整数の範囲で因数分解せよ。",
  "hint": r"$x^2=X$ とおいても $X^2-6X+1$ は整数の範囲で因数分解できない。そこで $(x^2+a)^2-(bx)^2$ の形（平方の差）をつくる。",
  "sol": r"$x^4-6x^2+1=(x^4-2x^2+1)-4x^2=(x^2-1)^2-(2x)^2$<br>$=\boldsymbol{(x^2+2x-1)(x^2-2x-1)}$",
  "note": r"$x^4+4=(x^2+2)^2-(2x)^2$ のように、真ん中の項を足して引く方法は入試頻出。",
  "ex": r"$x^4+4$ を、係数が整数の範囲で因数分解せよ。",
  "exa": r"$(x^2+2x+2)(x^2-2x+2)$"},
]})

# ---------------------------------------------------------------- 節2
SEC.append({"title": "対称式と式の値",
"base": r"""・$x+y$，$xy$ で表す：$x^2+y^2=(x+y)^2-2xy$，$x^3+y^3=(x+y)^3-3xy(x+y)$<br>
・実数 $x,\ y$ が存在する条件：$x,\ y$ は $t^2-(x+y)t+xy=0$ の2解なので、判別式 $(x+y)^2-4xy\geqq0$""",
"items": [
 {"lv": 4, "title": "対称式の値域（実数条件に注意）",
  "q": r"実数 $x,\ y$ が $x^2+xy+y^2=1$ を満たすとき、$x^2-xy+y^2$ のとり得る値の範囲を求めよ。",
  "hint": r"$x+y=s$，$xy=p$ とおくと条件も目標の式も $s,\ p$ で表せる。ただし $s,\ p$ は自由には動けない。<b>$x,\ y$ が実数である条件 $s^2-4p\geqq0$</b> を必ず加える。",
  "sol": r"$x+y=s,\ xy=p$ とおく。条件より $s^2-p=1$，すなわち $p=s^2-1$。<br>"
         r"$x,\ y$ は $t^2-st+p=0$ の実数解なので $s^2-4p\geqq0$。$p=s^2-1$ を代入して $s^2-4(s^2-1)\geqq0$，よって $0\leqq s^2\leqq\dfrac43$。<br>"
         r"$x^2-xy+y^2=s^2-3p=s^2-3(s^2-1)=3-2s^2$ で、$0\leqq s^2\leqq\dfrac43$ のとき $\dfrac13\leqq3-2s^2\leqq3$。<br>"
         r"$s^2=\dfrac43$（例えば $x=y=\dfrac1{\sqrt3}$）のとき最小、$s=0$（$x=1,\ y=-1$）のとき最大となるから　$\boldsymbol{\dfrac13\leqq x^2-xy+y^2\leqq3}$",
  "note": r"実数条件を忘れると $s$ が任意の値をとれるように見え、「$3$ 以下」という誤答になる。等号が成り立つ $x,\ y$ を具体的に示すと確実。",
  "ex": r"実数 $x,\ y$ が $x^2+y^2=2$ を満たすとき、$x+y+xy$ のとり得る値の範囲を求めよ。",
  "exa": r"$-\dfrac32\leqq x+y+xy\leqq3$"},
]})

CH = {"no": 1, "sections": SEC}


def verify():
    x, y = symbols("x y")
    assert expand((2*x+3)*(3*x-4)) == 6*x**2 + x - 12
    assert expand((2*x-3)*(4*x+5)) == 8*x**2 - 2*x - 15
    assert expand((x**2+2*x-1)*(x**2-2*x-1)) == x**4 - 6*x**2 + 1
    assert expand((x**2+2*x+2)*(x**2-2*x+2)) == x**4 + 4
    # 対称式の値域：条件を満たす点を多数とり、範囲の端と内側を確認
    import math
    vals = []
    for k in range(20000):
        th = 2 * math.pi * k / 20000          # x^2+xy+y^2=1 の媒介変数表示
        u, v = math.cos(th) / math.sqrt(3), math.sqrt(3) * math.sin(th)  # x=u-v/√3, y=u+v/√3 とおくと条件は 3u^2+v^2/3=1
        X, Y = u - v / math.sqrt(3), u + v / math.sqrt(3)
        assert abs(X*X + X*Y + Y*Y - 1) < 1e-9
        vals.append(X*X - X*Y + Y*Y)
    assert abs(min(vals) - 1/3) < 1e-6 and abs(max(vals) - 3) < 1e-6
    # 練習：x^2+y^2=2 → x+y+xy = s + (s^2-2)/2, |s|<=2
    vals = [2**0.5*math.cos(t) + 2**0.5*math.sin(t) + 2*math.cos(t)*math.sin(t) for t in [2*math.pi*k/20000 for k in range(20000)]]
    assert abs(min(vals) + 1.5) < 1e-6 and abs(max(vals) - 3) < 1e-6
