"""第1章 数と式（数学I） 担当 M01。節ごとに SEC.append(...) と検算関数 VER.append(...) を置く。"""
from sympy import symbols, expand, factor, sqrt, Rational, simplify, N, Integer
from fractions import Fraction as Fr
import math
import random

SEC = []
VER = []

x, y, z, a, b, c, d, t = symbols("x y z a b c d t")


def close(e1, e2, tol=1e-40):
    return abs(N(e1 - e2, 60)) < tol


# ---------------------------------------------------------------- 節1
SEC.append({"title": r"式の展開",
"base": r"""・乗法公式：$(a\pm b)^2=a^2\pm2ab+b^2$，$(a+b)(a-b)=a^2-b^2$，$(x+a)(x+b)=x^2+(a+b)x+ab$，$(ax+b)(cx+d)=acx^2+(ad+bc)x+bd$<br>
・3次の乗法公式：$(a\pm b)^3=a^3\pm3a^2b+3ab^2\pm b^3$，$(a\pm b)(a^2\mp ab+b^2)=a^3\pm b^3$<br>
・$(a+b+c)^2=a^2+b^2+c^2+2ab+2bc+2ca$<br>
・式の一部を1つの文字におき換える、掛ける順序や組合せを工夫する、の2つが計算を軽くする基本。""",
"items": [
 {"lv": 1, "title": r"乗法公式による展開",
  "q": r"次の式を展開せよ。<br>(1) $(3x-2y)^2$　(2) $(2a+3b)(2a-3b)$　(3) $(x+4)(x-7)$<br>(4) $(3x+2)(4x-5)$　(5) $(x+2)^3$　(6) $(x-3)(x^2+3x+9)$",
  "hint": r"どの公式の形かを見きわめてあてはめる。(4) は $(ax+b)(cx+d)$ の公式で、$x$ の係数は $ad+bc$（外側どうしの積＋内側どうしの積）。(5)(6) は3次の乗法公式。",
  "sol": r"(1) $(3x)^2-2\cdot3x\cdot2y+(2y)^2=\boldsymbol{9x^2-12xy+4y^2}$<br>"
         r"(2) $(2a)^2-(3b)^2=\boldsymbol{4a^2-9b^2}$<br>"
         r"(3) $x^2+(4-7)x+4\cdot(-7)=\boldsymbol{x^2-3x-28}$<br>"
         r"(4) $3\cdot4x^2+\{3\cdot(-5)+2\cdot4\}x+2\cdot(-5)=\boldsymbol{12x^2-7x-10}$<br>"
         r"(5) $x^3+3\cdot x^2\cdot2+3\cdot x\cdot2^2+2^3=\boldsymbol{x^3+6x^2+12x+8}$<br>"
         r"(6) $(x-3)(x^2+x\cdot3+3^2)=x^3-3^3=\boldsymbol{x^3-27}$",
  "note": r"(4) で $x$ の係数を $3\cdot4$ や $2\cdot(-5)$ と掛け違える誤りが多い。展開したら、$x=1$ などを代入して両辺の値が一致するか確かめるとよい（(4) は左辺 $5\cdot(-1)=-5$，右辺 $12-7-10=-5$）。",
  "ex": r"次の式を展開せよ。<br>(1) $(4a+3b)^2$　(2) $(5x-1)(2x+3)$　(3) $(3x-2)^3$　(4) $(2a+1)(4a^2-2a+1)$",
  "exa": r"(1) $16a^2+24ab+9b^2$　(2) $10x^2+13x-3$　(3) $27x^3-54x^2+36x-8$　(4) $8a^3+1$"},
 {"lv": 2, "title": r"おき換えによる展開",
  "q": r"次の式を展開せよ。<br>(1) $(a+b-c)(a-b+c)$　(2) $(x^2+x+1)(x^2-x+1)$　(3) $(2x-y+3)^2$",
  "hint": r"共通な部分と、符号だけが違う部分を見つける。(1) は $a+(b-c)$ と $a-(b-c)$，(2) は $(x^2+1)+x$ と $(x^2+1)-x$ の積とみれば和と差の積の公式が使える。(3) は $(a+b+c)^2$ の公式。",
  "sol": r"(1) $b-c=A$ とおくと<br>$(a+A)(a-A)=a^2-A^2=a^2-(b-c)^2=\boldsymbol{a^2-b^2+2bc-c^2}$<br>"
         r"(2) $x^2+1=B$ とおくと<br>$(B+x)(B-x)=B^2-x^2=(x^2+1)^2-x^2=\boldsymbol{x^4+x^2+1}$<br>"
         r"(3) $(a+b+c)^2$ の公式で $a=2x,\ b=-y,\ c=3$ として<br>"
         r"$(2x)^2+(-y)^2+3^2+2\cdot2x\cdot(-y)+2\cdot(-y)\cdot3+2\cdot3\cdot2x=\boldsymbol{4x^2+y^2-4xy+12x-6y+9}$",
  "note": r"(2) の結果を逆に読むと $x^4+x^2+1=(x^2+x+1)(x^2-x+1)$ という因数分解になる（次の節の複2次式）。(1) で $a+b$ と $-c$ のように組むと共通部分ができない。<b>符号がそろっている項</b>と<b>符号が逆の項</b>に分けて組むのがこつ。",
  "ex": r"次の式を展開せよ。<br>(1) $(x+y+z)(x-y-z)$　(2) $(x^2-2x+3)(x^2+2x+3)$　(3) $(a-2b+c)^2$",
  "exa": r"(1) $x^2-y^2-2yz-z^2$　(2) $x^4+2x^2+9$　(3) $a^2+4b^2+c^2-4ab-4bc+2ca$"},
 {"lv": 2, "title": r"展開式の特定の項の係数",
  "q": r"$(x^3-2x^2+3x-1)(2x^2+x-5)$ を展開したときの、$x^3$ の係数と $x^2$ の係数を求めよ。",
  "hint": r"全部を展開する必要はない。左の式の項を1つ固定し、次数の和が $3$（または $2$）になる右の式の項を選んで、その積だけを拾い出す。",
  "sol": r"$x^3$ の項が現れるのは $x^3\cdot(-5)$，$(-2x^2)\cdot x$，$3x\cdot2x^2$ の3組で<br>"
         r"$-5x^3-2x^3+6x^3=-x^3$　よって $x^3$ の係数は $\boldsymbol{-1}$<br>"
         r"$x^2$ の項が現れるのは $(-2x^2)\cdot(-5)$，$3x\cdot x$，$(-1)\cdot2x^2$ の3組で<br>"
         r"$10x^2+3x^2-2x^2=11x^2$　よって $x^2$ の係数は $\boldsymbol{11}$",
  "note": r"左の式の項を次数の高い順に固定して、相手の項を1つずつ決めていくと、組の漏れや重複がない。3つ以上の式の積でも同じ考え方で係数を求められる。",
  "ex": r"$(2x^2-x+3)(x^3+4x^2-2x+1)$ を展開したときの、$x^3$ の係数と $x^2$ の係数を求めよ。",
  "exa": r"$x^3$ の係数 $-5$，$x^2$ の係数 $16$"},
 {"lv": 3, "title": r"組合せと順序を工夫する展開",
  "q": r"次の式を展開せよ。<br>(1) $(x+1)(x+2)(x+3)(x+4)$　(2) $(1-x)(1+x)(1+x^2)(1+x^4)(1+x^8)$",
  "hint": r"(1) 定数項の和が等しくなるように $(x+1)(x+4)$ と $(x+2)(x+3)$ を組にすると、どちらにも $x^2+5x$ が現れ、おき換えができる。(2) 左から順に「和と差の積」をくり返す。",
  "sol": r"(1) $(x+1)(x+4)=x^2+5x+4$，$(x+2)(x+3)=x^2+5x+6$。$x^2+5x=X$ とおくと<br>"
         r"与式 $=(X+4)(X+6)=X^2+10X+24=(x^2+5x)^2+10(x^2+5x)+24$<br>"
         r"$=x^4+10x^3+25x^2+10x^2+50x+24=\boldsymbol{x^4+10x^3+35x^2+50x+24}$<br>"
         r"(2) $(1-x)(1+x)=1-x^2$，$(1-x^2)(1+x^2)=1-x^4$，$(1-x^4)(1+x^4)=1-x^8$ より<br>"
         r"与式 $=(1-x^8)(1+x^8)=\boldsymbol{1-x^{16}}$",
  "note": r"(1) で $(x+1)(x+2)$ と $(x+3)(x+4)$ を組むと共通な式が現れず、計算が重くなる。「定数項の和をそろえる」が組み方の目安。この組み方は、$(x+1)(x+2)(x+3)(x+4)-24$ のような式の因数分解にもそのまま使える。",
  "ex": r"次の式を展開せよ。<br>(1) $(x-1)(x-3)(x+2)(x+4)$　(2) $(x+y)(x-y)(x^2+y^2)(x^4+y^4)$",
  "exa": r"(1) $x^4+2x^3-13x^2-14x+24$　(2) $x^8-y^8$"},
]})


def _v1():
    E = lambda u, v: expand(u - v) == 0
    assert E((3*x-2*y)**2, 9*x**2-12*x*y+4*y**2)
    assert E((2*a+3*b)*(2*a-3*b), 4*a**2-9*b**2)
    assert E((x+4)*(x-7), x**2-3*x-28)
    assert E((3*x+2)*(4*x-5), 12*x**2-7*x-10)
    assert E((x+2)**3, x**3+6*x**2+12*x+8)
    assert E((x-3)*(x**2+3*x+9), x**3-27)
    assert E((4*a+3*b)**2, 16*a**2+24*a*b+9*b**2)
    assert E((5*x-1)*(2*x+3), 10*x**2+13*x-3)
    assert E((3*x-2)**3, 27*x**3-54*x**2+36*x-8)
    assert E((2*a+1)*(4*a**2-2*a+1), 8*a**3+1)
    # おき換え
    assert E((a+b-c)*(a-b+c), a**2-b**2+2*b*c-c**2)
    assert E((x**2+x+1)*(x**2-x+1), x**4+x**2+1)
    assert E((2*x-y+3)**2, 4*x**2+y**2-4*x*y+12*x-6*y+9)
    assert E((x+y+z)*(x-y-z), x**2-y**2-2*y*z-z**2)
    assert E((x**2-2*x+3)*(x**2+2*x+3), x**4+2*x**2+9)
    assert E((a-2*b+c)**2, a**2+4*b**2+c**2-4*a*b-4*b*c+2*c*a)
    # 係数
    P = expand((x**3-2*x**2+3*x-1)*(2*x**2+x-5))
    assert P.coeff(x, 3) == -1 and P.coeff(x, 2) == 11
    P = expand((2*x**2-x+3)*(x**3+4*x**2-2*x+1))
    assert P.coeff(x, 3) == -5 and P.coeff(x, 2) == 16
    # 組合せ
    assert E((x+1)*(x+4), x**2+5*x+4) and E((x+2)*(x+3), x**2+5*x+6)
    assert E((x+1)*(x+2)*(x+3)*(x+4), x**4+10*x**3+35*x**2+50*x+24)
    assert E((1-x)*(1+x)*(1+x**2)*(1+x**4)*(1+x**8), 1-x**16)
    assert E((x-1)*(x-3)*(x+2)*(x+4), x**4+2*x**3-13*x**2-14*x+24)
    assert E((x+y)*(x-y)*(x**2+y**2)*(x**4+y**4), x**8-y**8)


VER.append(_v1)

# ---------------------------------------------------------------- 節2
SEC.append({"title": r"因数分解",
"base": r"""・手順：① 共通因数をくくり出す　② 公式の形を探す　③ たすきがけ　④ 共通な式をおき換える　⑤ 最も次数の低い文字について整理する<br>
・$a^2-b^2=(a+b)(a-b)$，$acx^2+(ad+bc)x+bd=(ax+b)(cx+d)$，$a^3\pm b^3=(a\pm b)(a^2\mp ab+b^2)$<br>
・$a^3+b^3+c^3-3abc=(a+b+c)(a^2+b^2+c^2-ab-bc-ca)$<br>
・複2次式は平方の差 $A^2-B^2$ の形をつくる。対称式・交代式は1つの文字について整理する。""",
"items": [
 {"lv": 1, "title": r"共通因数・公式・たすきがけ",
  "q": r"次の式を因数分解せよ。<br>(1) $9a^2-12ab+4b^2$　(2) $2x^3-18x$　(3) $6x^2-7x-20$　(4) $3x^2+10xy-8y^2$",
  "hint": r"まず共通因数をくくり出し、次に公式 $A^2-2AB+B^2$，$A^2-B^2$ の形を探す。それでも残る2次式はたすきがけ。",
  "sol": r"(1) $(3a)^2-2\cdot3a\cdot2b+(2b)^2=\boldsymbol{(3a-2b)^2}$<br>"
         r"(2) $2x(x^2-9)=\boldsymbol{2x(x+3)(x-3)}$<br>"
         r"(3) $6=2\cdot3$，$-20=(-5)\cdot4$ と分けると $2\cdot4+(-5)\cdot3=-7$ となるから　$\boldsymbol{(2x-5)(3x+4)}$<br>"
         r"(4) $3=3\cdot1$，$-8y^2=(-2y)\cdot4y$ と分けると $3\cdot4y+(-2y)\cdot1=10y$ となるから　$\boldsymbol{(3x-2y)(x+4y)}$",
  "note": r"(2) で $2x(x^2-9)$ のまま終えるのは不完全。因数分解は、それ以上分解できないところまで行う。たすきがけでは、$x^2$ の係数を正にそろえ、定数項の分け方を符号も含めて順に試す。",
  "ex": r"次の式を因数分解せよ。<br>(1) $8x^2-2x-15$　(2) $12a^2-5ab-2b^2$　(3) $3x^3-12xy^2$",
  "exa": r"(1) $(2x-3)(4x+5)$　(2) $(3a-2b)(4a+b)$　(3) $3x(x+2y)(x-2y)$"},
 {"lv": 2, "title": r"おき換え・3次の公式による因数分解",
  "q": r"次の式を因数分解せよ。<br>(1) $(x^2+2x)^2-2(x^2+2x)-3$　(2) $8x^3-27y^3$<br>(3) $x^6-64$　(4) $(x+1)(x+2)(x+3)(x+4)-24$",
  "hint": r"(1) $x^2+2x=X$ とおく。(3) は $(x^3)^2-8^2$ とみて和と差の積にしてから3次の公式。(4) は定数項の和がそろうように $(x+1)(x+4)$ と $(x+2)(x+3)$ を組にする。",
  "sol": r"(1) $x^2+2x=X$ とおくと $X^2-2X-3=(X-3)(X+1)$<br>$=(x^2+2x-3)(x^2+2x+1)=\boldsymbol{(x+3)(x-1)(x+1)^2}$<br>"
         r"(2) $(2x)^3-(3y)^3=\boldsymbol{(2x-3y)(4x^2+6xy+9y^2)}$<br>"
         r"(3) $(x^3+8)(x^3-8)=\boldsymbol{(x+2)(x^2-2x+4)(x-2)(x^2+2x+4)}$<br>"
         r"(4) $(x+1)(x+4)=x^2+5x+4$，$(x+2)(x+3)=x^2+5x+6$。$x^2+5x=X$ とおくと<br>"
         r"$(X+4)(X+6)-24=X^2+10X=X(X+10)=\boldsymbol{x(x+5)(x^2+5x+10)}$",
  "note": r"(3) を $(x^2)^3-4^3=(x^2-4)(x^4+4x^2+16)$ とすると、さらに $x^4+4x^2+16=(x^2+4)^2-(2x)^2$ と複2次式の変形が必要になる。2乗の差が使えるときは先に使うほうが速い。(4) の $x^2+5x+10$ は整数の範囲ではこれ以上分解できない。",
  "ex": r"次の式を因数分解せよ。<br>(1) $(x^2-3x)^2-2(x^2-3x)-8$　(2) $x^6-1$　(3) $(x+1)(x+3)(x+5)(x+7)+15$",
  "exa": r"(1) $(x+1)(x-1)(x-2)(x-4)$　(2) $(x+1)(x-1)(x^2+x+1)(x^2-x+1)$　(3) $(x+2)(x+6)(x^2+8x+10)$"},
 {"lv": 2, "title": r"1つの文字について整理する",
  "q": r"次の式を因数分解せよ。<br>(1) $x^3-2x^2y-x+2y$　(2) $2x^2+5xy+2y^2+4x-y-6$",
  "hint": r"(1) は $y$ について1次式なので、$y$ について整理する（最も次数の低い文字で整理）。(2) は $x,\ y$ のどちらも2次なので $x$ について整理し、定数項（$y$ の式）を先に因数分解してからたすきがけ。",
  "sol": r"(1) $y$ について整理すると<br>与式 $=-2y(x^2-1)+x(x^2-1)=(x^2-1)(x-2y)=\boldsymbol{(x+1)(x-1)(x-2y)}$<br>"
         r"(2) $x$ について整理すると<br>与式 $=2x^2+(5y+4)x+(2y^2-y-6)=2x^2+(5y+4)x+(y-2)(2y+3)$<br>"
         r"$2$ を $2\cdot1$，定数項を $(y-2)(2y+3)$ と分けると $2(2y+3)+(y-2)\cdot1=5y+4$ となるから<br>"
         r"与式 $=\{2x+(y-2)\}\{x+(2y+3)\}=\boldsymbol{(2x+y-2)(x+2y+3)}$",
  "note": r"次数が同じなら、どの文字で整理してもよいが、係数が簡単になる文字を選ぶ。(2) では、整理した後の「定数項」$2y^2-y-6$ の因数分解が鍵になる。",
  "ex": r"次の式を因数分解せよ。<br>(1) $a^2b+a^2-b-1$　(2) $x^2+3xy+2y^2-x-3y-2$",
  "exa": r"(1) $(a+1)(a-1)(b+1)$　(2) $(x+y-2)(x+2y+1)$"},
 {"lv": 3, "title": r"複2次式の因数分解（平方の差をつくる）",
  "q": r"次の式を、係数が整数の範囲で因数分解せよ。<br>(1) $x^4-13x^2+36$　(2) $x^4-7x^2+9$　(3) $4x^4+1$",
  "hint": r"まず $x^2=X$ とおいて $X$ の2次式として因数分解できるか試す（(1)）。できなければ、$x^4$ の項と定数項から平方 $(x^2\pm q)^2$ をつくり、残りが $(\ \ )x^2$ の平方になるようにして $A^2-B^2$ の形にする（(2)(3)）。",
  "sol": r"(1) $(x^2-4)(x^2-9)=\boldsymbol{(x+2)(x-2)(x+3)(x-3)}$<br>"
         r"(2) $x^4-6x^2+9-x^2=(x^2-3)^2-x^2=\boldsymbol{(x^2+x-3)(x^2-x-3)}$<br>"
         r"(3) $4x^4+4x^2+1-4x^2=(2x^2+1)^2-(2x)^2=\boldsymbol{(2x^2+2x+1)(2x^2-2x+1)}$",
  "note": r"(2) で $(x^2+3)^2-13x^2$ と変形すると、$13$ が平方数でないので整数係数にならない。$x^4+px^2+q^2$ は、$(x^2+q)^2$ と $(x^2-q)^2$ のうち、残りの $x^2$ の係数が「負の平方数」になるほうを使う。",
  "ex": r"次の式を、係数が整数の範囲で因数分解せよ。<br>(1) $x^4+3x^2+4$　(2) $x^4-11x^2+1$",
  "exa": r"(1) $(x^2+x+2)(x^2-x+2)$　(2) $(x^2+3x-1)(x^2-3x-1)$"},
 {"lv": 3, "title": r"対称式・交代式の因数分解",
  "q": r"次の式を因数分解せよ。<br>(1) $(a+b)(b+c)(c+a)+abc$　(2) $a^2(b-c)+b^2(c-a)+c^2(a-b)$",
  "hint": r"どちらも $a,\ b,\ c$ について同じ次数（2次以上）なので、1つの文字 $a$ について整理する。(2) は文字を入れかえると符号が変わる「交代式」で、$(a-b)(b-c)(c-a)$ を因数にもつ。",
  "sol": r"(1) $a$ について整理すると<br>与式 $=(b+c)\{a^2+(b+c)a+bc\}+abc=(b+c)a^2+\{(b+c)^2+bc\}a+bc(b+c)$<br>"
         r"$a^2$ の係数を $(b+c)\cdot1$，定数項を $bc\cdot(b+c)$ と分けると $(b+c)(b+c)+bc\cdot1$ が $a$ の係数に一致するから<br>"
         r"与式 $=\{(b+c)a+bc\}\{a+(b+c)\}=\boldsymbol{(a+b+c)(ab+bc+ca)}$<br>"
         r"(2) $a$ について整理すると<br>与式 $=(b-c)a^2-(b^2-c^2)a+bc(b-c)=(b-c)\{a^2-(b+c)a+bc\}$<br>"
         r"$=(b-c)(a-b)(a-c)=\boldsymbol{-(a-b)(b-c)(c-a)}$",
  "note": r"答えは輪環の順 $(a-b)(b-c)(c-a)$ にそろえて書くのが普通。$a-c=-(c-a)$ なので符号に注意する。交代式は $a=b$ とおくと $0$ になるので、$a-b$ を因数にもつ、という見通しも立てられる。",
  "ex": r"次の式を因数分解せよ。<br>(1) $ab(a+b)+bc(b+c)+ca(c+a)+2abc$　(2) $a(b^2-c^2)+b(c^2-a^2)+c(a^2-b^2)$",
  "exa": r"(1) $(a+b)(b+c)(c+a)$　(2) $(a-b)(b-c)(c-a)$"},
 {"lv": 4, "title": r"$a^3+b^3+c^3-3abc$ の因数分解とその利用",
  "q": r"(1) $a^3+b^3+c^3-3abc$ を因数分解せよ。<br>(2) $x^3+y^3+3xy-1$ を因数分解せよ。",
  "hint": r"(1) $a^3+b^3=(a+b)^3-3ab(a+b)$ を使って $a+b$ のかたまりをつくると、$(a+b)^3+c^3$ に3次の公式が使える。(2) は $-1=(-1)^3$，$3xy=-3\cdot x\cdot y\cdot(-1)$ とみると (1) の形。",
  "sol": r"(1) $a^3+b^3+c^3-3abc=(a+b)^3-3ab(a+b)+c^3-3abc$<br>"
         r"$=\{(a+b)^3+c^3\}-3ab(a+b+c)$<br>"
         r"$=(a+b+c)\{(a+b)^2-(a+b)c+c^2\}-3ab(a+b+c)$<br>"
         r"$=(a+b+c)(a^2+2ab+b^2-ac-bc+c^2-3ab)$<br>"
         r"$=\boldsymbol{(a+b+c)(a^2+b^2+c^2-ab-bc-ca)}$<br>"
         r"(2) $x^3+y^3+(-1)^3-3\cdot x\cdot y\cdot(-1)$ なので、(1) で $a=x,\ b=y,\ c=-1$ として<br>"
         r"与式 $=\boldsymbol{(x+y-1)(x^2+y^2-xy+x+y+1)}$",
  "note": r"$a^2+b^2+c^2-ab-bc-ca=\dfrac12\{(a-b)^2+(b-c)^2+(c-a)^2\}$ と変形できる。よって実数 $a,\ b,\ c$ について $a^3+b^3+c^3=3abc$ となるのは「$a+b+c=0$ または $a=b=c$」のときに限る。また $a,\ b,\ c\geqq0$ のとき $a^3+b^3+c^3\geqq3abc$（相加平均と相乗平均の関係の3変数版）も分かる。",
  "ex": r"$x^3-8y^3+18xy+27$ を因数分解せよ。",
  "exa": r"$(x-2y+3)(x^2+4y^2+2xy-3x+6y+9)$"},
 {"lv": 4, "title": r"1次式の積に因数分解できる条件",
  "q": r"$x^2+3xy+2y^2-3x-5y+k$ が $x,\ y$ の1次式の積に因数分解できるように、定数 $k$ の値を定めよ。また、そのときの因数分解の結果を求めよ。",
  "hint": r"2次の部分 $x^2+3xy+2y^2=(x+y)(x+2y)$ に着目する。1次式の積に分解できるなら、$(x+y+p)(x+2y+q)$（$p,\ q$ は定数）の形になるはず。展開して係数を比べる。",
  "sol": r"与式が1次式の積に分解できるとき、2次の項だけを取り出すと $x^2+3xy+2y^2=(x+y)(x+2y)$ であるから、与式は<br>"
         r"$(x+y+p)(x+2y+q)$　（$p,\ q$ は定数）<br>と表せる。これを展開すると<br>"
         r"$x^2+3xy+2y^2+(p+q)x+(2p+q)y+pq$<br>"
         r"与式と係数を比べて　$p+q=-3$，$2p+q=-5$，$pq=k$<br>"
         r"はじめの2式から $p=-2,\ q=-1$。よって $k=pq=\boldsymbol{2}$<br>"
         r"このとき　$x^2+3xy+2y^2-3x-5y+2=\boldsymbol{(x+y-2)(x+2y-1)}$",
  "note": r"<b>別解</b>（判別式）：$x$ について整理した $x^2+(3y-3)x+(2y^2-5y+k)$ を $x$ の2次式とみる。これが $x,\ y$ の1次式の積になるには、判別式 $D=(3y-3)^2-4(2y^2-5y+k)=y^2+2y+9-4k$ が $y$ の1次式の平方（完全平方式）になればよい。$D=(y+1)^2+8-4k$ より $8-4k=0$，$k=2$。2次の部分が因数分解できない式ではこちらを使う。",
  "ex": r"$2x^2-xy-y^2+x+5y+k$ が $x,\ y$ の1次式の積に因数分解できるように定数 $k$ の値を定め、そのときの因数分解の結果を求めよ。",
  "exa": r"$k=-6$，$(2x+y-3)(x-y+2)$"},
]})


def _v2():
    F = lambda u, v: expand(u - v) == 0
    assert F((3*a-2*b)**2, 9*a**2-12*a*b+4*b**2)
    assert F(2*x*(x+3)*(x-3), 2*x**3-18*x)
    assert F((2*x-5)*(3*x+4), 6*x**2-7*x-20) and 2*4 + (-5)*3 == -7
    assert F((3*x-2*y)*(x+4*y), 3*x**2+10*x*y-8*y**2)
    assert F((2*x-3)*(4*x+5), 8*x**2-2*x-15)
    assert F((3*a-2*b)*(4*a+b), 12*a**2-5*a*b-2*b**2)
    assert F(3*x*(x+2*y)*(x-2*y), 3*x**3-12*x*y**2)
    # おき換え
    assert F((x+3)*(x-1)*(x+1)**2, (x**2+2*x)**2-2*(x**2+2*x)-3)
    assert F((2*x-3*y)*(4*x**2+6*x*y+9*y**2), 8*x**3-27*y**3)
    assert F((x+2)*(x**2-2*x+4)*(x-2)*(x**2+2*x+4), x**6-64)
    assert F(x*(x+5)*(x**2+5*x+10), (x+1)*(x+2)*(x+3)*(x+4)-24)
    assert factor(x**2+5*x+10) == x**2+5*x+10
    assert F((x+1)*(x-1)*(x-2)*(x-4), (x**2-3*x)**2-2*(x**2-3*x)-8)
    assert F((x+1)*(x-1)*(x**2+x+1)*(x**2-x+1), x**6-1)
    assert F((x+2)*(x+6)*(x**2+8*x+10), (x+1)*(x+3)*(x+5)*(x+7)+15)
    # 1文字について整理
    assert F((x+1)*(x-1)*(x-2*y), x**3-2*x**2*y-x+2*y)
    assert F((y-2)*(2*y+3), 2*y**2-y-6)
    assert F((2*x+y-2)*(x+2*y+3), 2*x**2+5*x*y+2*y**2+4*x-y-6)
    assert F((a+1)*(a-1)*(b+1), a**2*b+a**2-b-1)
    assert F((x+y-2)*(x+2*y+1), x**2+3*x*y+2*y**2-x-3*y-2)
    # 複2次
    assert F((x+2)*(x-2)*(x+3)*(x-3), x**4-13*x**2+36)
    assert F((x**2+x-3)*(x**2-x-3), x**4-7*x**2+9)
    assert F((2*x**2+2*x+1)*(2*x**2-2*x+1), 4*x**4+1)
    assert F((x**2+x+2)*(x**2-x+2), x**4+3*x**2+4)
    assert F((x**2+3*x-1)*(x**2-3*x-1), x**4-11*x**2+1)
    for e in (x**2+x-3, 2*x**2+2*x+1, x**2+x+2, x**2+3*x-1):
        assert factor(e) == e          # これ以上分解できない
    # 対称式・交代式
    assert F((a+b+c)*(a*b+b*c+c*a), (a+b)*(b+c)*(c+a)+a*b*c)
    assert F(-(a-b)*(b-c)*(c-a), a**2*(b-c)+b**2*(c-a)+c**2*(a-b))
    assert F((b-c)*(a-b)*(a-c), a**2*(b-c)+b**2*(c-a)+c**2*(a-b))
    assert F((a+b)*(b+c)*(c+a), a*b*(a+b)+b*c*(b+c)+c*a*(c+a)+2*a*b*c)
    assert F((a-b)*(b-c)*(c-a), a*(b**2-c**2)+b*(c**2-a**2)+c*(a**2-b**2))
    # a^3+b^3+c^3-3abc
    assert F((a+b+c)*(a**2+b**2+c**2-a*b-b*c-c*a), a**3+b**3+c**3-3*a*b*c)
    assert F((a+b+c)*(a**2+2*a*b+b**2-a*c-b*c+c**2-3*a*b), a**3+b**3+c**3-3*a*b*c)
    assert F((x+y-1)*(x**2+y**2-x*y+x+y+1), x**3+y**3+3*x*y-1)
    assert F((x-2*y+3)*(x**2+4*y**2+2*x*y-3*x+6*y+9), x**3-8*y**3+18*x*y+27)
    assert F(a**2+b**2+c**2-a*b-b*c-c*a, Rational(1, 2)*((a-b)**2+(b-c)**2+(c-a)**2))
    # 1次式の積の条件
    p, q, k = symbols("p q k")
    E1 = expand((x+y+p)*(x+2*y+q))
    assert E1.coeff(x, 1).coeff(y, 0) == p+q and E1.coeff(y, 1).coeff(x, 0) == 2*p+q
    assert (-2) + (-1) == -3 and 2*(-2) + (-1) == -5
    assert F((x+y-2)*(x+2*y-1), x**2+3*x*y+2*y**2-3*x-5*y+2)
    assert F((3*y-3)**2-4*(2*y**2-5*y+k), y**2+2*y+9-4*k)
    assert F((2*x+y-3)*(x-y+2), 2*x**2-x*y-y**2+x+5*y-6)
    E2 = expand((2*x+y+p)*(x-y+q))
    # 2q+p=1, q-p=5 → p=-3, q=2
    assert E2.subs({p: -3, q: 2}) == expand(2*x**2-x*y-y**2+x+5*y-6)


VER.append(_v2)

# ---------------------------------------------------------------- 節3
SEC.append({"title": r"実数と平方根",
"base": r"""・有限小数・循環小数は分数で表せる（有理数）。循環小数 $x$ は、循環節の長さが $n$ なら $10^nx-x$ をつくって循環部分を消す。<br>
・$\sqrt{a^2}=|a|$。$|a|=a\ (a\geqq0)$，$|a|=-a\ (a<0)$<br>
・二重根号：$a>0,\ b>0$ のとき $\sqrt{(a+b)+2\sqrt{ab}}=\sqrt a+\sqrt b$，$a>b>0$ のとき $\sqrt{(a+b)-2\sqrt{ab}}=\sqrt a-\sqrt b$<br>
・分母の有理化：$\dfrac{1}{\sqrt a+\sqrt b}=\dfrac{\sqrt a-\sqrt b}{a-b}$（$a\neq b$）<br>
・実数 $x$ の整数部分は $n\leqq x<n+1$ を満たす整数 $n$，小数部分は $x-n$（$0\leqq x-n<1$）""",
"items": [
 {"lv": 1, "title": r"循環小数を分数で表す",
  "q": r"次の循環小数を分数で表せ。<br>(1) $0.\dot{3}\dot{6}$　(2) $1.2\dot{3}\dot{4}$",
  "hint": r"循環節の長さが $2$ なので、$100x$ と $x$ の差をとると、小数点以下の循環部分が消える。",
  "sol": r"(1) $x=0.3636\cdots$ とおくと $100x=36.3636\cdots$。辺々引いて $99x=36$<br>"
         r"よって $x=\dfrac{36}{99}=\boldsymbol{\dfrac{4}{11}}$<br>"
         r"(2) $x=1.23434\cdots$ とおくと $100x=123.43434\cdots$。辺々引いて $99x=122.2$<br>"
         r"よって $x=\dfrac{1222}{990}=\boldsymbol{\dfrac{611}{495}}$",
  "note": r"逆に、分数を小数で表すと、有限小数か循環小数になる（割り算の余りは分母より小さい有限種類しかないから）。$0.\dot{9}=1$ も同じ方法で分かる：$x=0.999\cdots$ とすると $10x-x=9$。",
  "ex": r"次の循環小数を分数で表せ。<br>(1) $0.\dot{1}2\dot{3}$　(2) $0.4\dot{5}$",
  "exa": r"(1) $\dfrac{41}{333}$　(2) $\dfrac{41}{90}$"},
 {"lv": 1, "title": r"根号を含む式の計算と分母の有理化",
  "q": r"次の式を計算せよ。<br>(1) $\sqrt{50}-\sqrt{18}+\sqrt8$　(2) $(2\sqrt3-\sqrt2)(\sqrt3+2\sqrt2)$　(3) $\dfrac{\sqrt3}{\sqrt3-\sqrt2}-\dfrac{\sqrt2}{\sqrt3+\sqrt2}$",
  "hint": r"(1) $\sqrt{a^2b}=a\sqrt b$ で根号の中をできるだけ小さな自然数にする。(3) 通分すると、分母は $(\sqrt3-\sqrt2)(\sqrt3+\sqrt2)=3-2=1$ になる。",
  "sol": r"(1) $5\sqrt2-3\sqrt2+2\sqrt2=\boldsymbol{4\sqrt2}$<br>"
         r"(2) $2\cdot3+4\sqrt6-\sqrt6-2\cdot2=\boldsymbol{2+3\sqrt6}$<br>"
         r"(3) $\dfrac{\sqrt3(\sqrt3+\sqrt2)-\sqrt2(\sqrt3-\sqrt2)}{(\sqrt3-\sqrt2)(\sqrt3+\sqrt2)}=\dfrac{3+\sqrt6-\sqrt6+2}{1}=\boldsymbol{5}$",
  "note": r"分母の有理化は、分母と分子に「分母の符号違いの式」を掛け、$(\sqrt a+\sqrt b)(\sqrt a-\sqrt b)=a-b$ によって根号を消す。",
  "ex": r"次の式を計算せよ。<br>(1) $\sqrt{48}-\sqrt{27}+\sqrt{12}$　(2) $\dfrac{1}{2-\sqrt3}+\dfrac{1}{2+\sqrt3}$　(3) $(\sqrt5+\sqrt2)^2-(\sqrt5-\sqrt2)^2$",
  "exa": r"(1) $3\sqrt3$　(2) $4$　(3) $4\sqrt{10}$"},
 {"lv": 2, "title": r"$\sqrt{a^2}=|a|$ と場合分け",
  "q": r"$P=\sqrt{x^2-2x+1}+\sqrt{x^2+4x+4}$ を、次の各場合について、根号と絶対値記号を用いずに表せ。<br>(1) $x\geqq1$　(2) $-2\leqq x<1$　(3) $x<-2$",
  "hint": r"$\sqrt{(x-1)^2}=x-1$ としてよいのは $x-1\geqq0$ のときだけ。一般には $\sqrt{A^2}=|A|$ なので、絶対値の中身の符号で場合を分ける。",
  "sol": r"$P=\sqrt{(x-1)^2}+\sqrt{(x+2)^2}=|x-1|+|x+2|$<br>"
         r"(1) $x\geqq1$ のとき、$x-1\geqq0$，$x+2>0$ より　$P=(x-1)+(x+2)=\boldsymbol{2x+1}$<br>"
         r"(2) $-2\leqq x<1$ のとき、$x-1<0$，$x+2\geqq0$ より　$P=-(x-1)+(x+2)=\boldsymbol{3}$<br>"
         r"(3) $x<-2$ のとき、$x-1<0$，$x+2<0$ より　$P=-(x-1)-(x+2)=\boldsymbol{-2x-1}$",
  "note": r"「$\sqrt{(x-1)^2}=x-1$」とする誤りが非常に多い。$x=0$ を代入すると左辺は $1$，右辺は $-1$ で、誤りとすぐ分かる。",
  "ex": r"$Q=\sqrt{a^2+6a+9}-\sqrt{a^2-4a+4}$ を、(1) $a\geqq2$　(2) $-3\leqq a<2$　(3) $a<-3$ の各場合について、根号と絶対値記号を用いずに表せ。",
  "exa": r"(1) $5$　(2) $2a+1$　(3) $-5$"},
 {"lv": 2, "title": r"二重根号をはずす",
  "q": r"次の式の二重根号をはずして簡単にせよ。<br>(1) $\sqrt{7+2\sqrt{10}}$　(2) $\sqrt{8-\sqrt{48}}$　(3) $\sqrt{2+\sqrt3}$",
  "hint": r"$\sqrt{p\pm2\sqrt q}$ の形にして、和が $p$，積が $q$ となる2つの正の数を探す。(2) は $\sqrt{48}=2\sqrt{12}$。(3) は中の根号の前に $2$ がないので、$\dfrac{\sqrt{4+2\sqrt3}}{\sqrt2}$ と変形する。",
  "sol": r"(1) 和 $7$，積 $10$ の2数は $5,\ 2$ なので　$\sqrt{(\sqrt5+\sqrt2)^2}=\boldsymbol{\sqrt5+\sqrt2}$<br>"
         r"(2) $\sqrt{8-2\sqrt{12}}$。和 $8$，積 $12$ の2数は $6,\ 2$ なので　$\sqrt{(\sqrt6-\sqrt2)^2}=\boldsymbol{\sqrt6-\sqrt2}$<br>"
         r"(3) $\sqrt{2+\sqrt3}=\sqrt{\dfrac{4+2\sqrt3}{2}}=\dfrac{\sqrt{(\sqrt3+1)^2}}{\sqrt2}=\dfrac{\sqrt3+1}{\sqrt2}=\boldsymbol{\dfrac{\sqrt6+\sqrt2}{2}}$",
  "note": r"(2) で $\sqrt2-\sqrt6$ と書くと負の数になり誤り。$\sqrt{(a+b)-2\sqrt{ab}}$ は、大きいほうから小さいほうを引いた $\sqrt a-\sqrt b\ (a>b)$ である（$\sqrt{A^2}=|A|$ だから）。",
  "ex": r"次の式の二重根号をはずして簡単にせよ。<br>(1) $\sqrt{9-2\sqrt{14}}$　(2) $\sqrt{4-\sqrt{15}}$",
  "exa": r"(1) $\sqrt7-\sqrt2$　(2) $\dfrac{\sqrt{10}-\sqrt6}{2}$"},
 {"lv": 3, "title": r"3つの項を含む分母の有理化",
  "q": r"次の式の分母を有理化せよ。<br>(1) $\dfrac{1}{1+\sqrt2+\sqrt3}$　(2) $\dfrac{1}{\sqrt2+\sqrt3+\sqrt5}$",
  "hint": r"2つの項を組にして $(A+B)(A-B)=A^2-B^2$ を使い、まず根号の種類を減らす。どの2項を組にするかは、1回目の結果が簡単になるほうを選ぶ。(2) は $2+3=5$ に着目して $\sqrt2+\sqrt3$ を組にする。",
  "sol": r"(1) 分母・分子に $(1+\sqrt2)-\sqrt3$ を掛けると<br>"
         r"$\dfrac{1+\sqrt2-\sqrt3}{(1+\sqrt2)^2-3}=\dfrac{1+\sqrt2-\sqrt3}{2\sqrt2}=\dfrac{(1+\sqrt2-\sqrt3)\sqrt2}{4}=\boldsymbol{\dfrac{2+\sqrt2-\sqrt6}{4}}$<br>"
         r"(2) 分母・分子に $(\sqrt2+\sqrt3)-\sqrt5$ を掛けると<br>"
         r"$\dfrac{\sqrt2+\sqrt3-\sqrt5}{(\sqrt2+\sqrt3)^2-5}=\dfrac{\sqrt2+\sqrt3-\sqrt5}{2\sqrt6}=\dfrac{(\sqrt2+\sqrt3-\sqrt5)\sqrt6}{12}=\boldsymbol{\dfrac{2\sqrt3+3\sqrt2-\sqrt{30}}{12}}$",
  "note": r"(2) で $\sqrt3+\sqrt5$ を組にすると、1回目の分母が $2-(8+2\sqrt{15})=-6-2\sqrt{15}$ となり、2回目の有理化が重くなる。1回目で定数項が消える組を選ぶと速い。",
  "ex": r"$\dfrac{2}{1-\sqrt2+\sqrt3}$ の分母を有理化せよ。",
  "exa": r"$\dfrac{2-\sqrt2+\sqrt6}{2}$"},
 {"lv": 3, "title": r"整数部分・小数部分と式の値",
  "q": r"$\dfrac{2}{3-\sqrt7}$ の整数部分を $a$，小数部分を $b$ とする。<br>(1) $a,\ b$ の値を求めよ。　(2) $b^2+4b$ の値を求めよ。　(3) $\dfrac ab$ の整数部分を求めよ。",
  "hint": r"まず分母を有理化し、$\sqrt7$ を整数ではさむ。小数部分は「もとの数 − 整数部分」で、正確な値で表す。(2) は $b+2=\sqrt7$ を2乗すると根号が消える。(3) は $\sqrt7$ を小数第1位まで評価する。",
  "sol": r"(1) $\dfrac{2}{3-\sqrt7}=\dfrac{2(3+\sqrt7)}{9-7}=3+\sqrt7$。$2<\sqrt7<3$ より $5<3+\sqrt7<6$<br>"
         r"よって　$\boldsymbol{a=5,\ b=(3+\sqrt7)-5=\sqrt7-2}$<br>"
         r"(2) $b+2=\sqrt7$ の両辺を2乗して $b^2+4b+4=7$。よって $b^2+4b=\boldsymbol{3}$<br>"
         r"(3) $\dfrac ab=\dfrac{5}{\sqrt7-2}=\dfrac{5(\sqrt7+2)}{7-4}=\dfrac{5(\sqrt7+2)}{3}$<br>"
         r"$2.6^2=6.76$，$2.7^2=7.29$ より $2.6<\sqrt7<2.7$。よって $\dfrac{5\cdot4.6}{3}<\dfrac ab<\dfrac{5\cdot4.7}{3}$，すなわち $7.66\cdots<\dfrac ab<7.83\cdots$<br>"
         r"したがって $\dfrac ab$ の整数部分は $\boldsymbol{7}$",
  "note": r"小数部分を $0.6457\cdots$ のような近似値で答えるのは誤り。(3) のように整数部分だけを求めるときは、評価の精度が足りているか（両端の整数部分が一致するか）を確かめる。精度が足りなければ $2.64<\sqrt7<2.65$ のように細かくする。",
  "ex": r"$\dfrac{1}{\sqrt5-2}$ の整数部分を $a$，小数部分を $b$ とする。$a,\ b$ の値と $b^2+4b$ の値を求めよ。また、$\dfrac ab$ の整数部分を求めよ。",
  "exa": r"$a=4,\ b=\sqrt5-2$，$b^2+4b=1$，$\dfrac ab$ の整数部分は $16$"},
 {"lv": 5, "title": r"根号の和の整数部分（平方数の余りによる評価）",
  "q": r"実数 $x$ に対し、$x$ を超えない最大の整数を $[x]$ で表す。$n$ を自然数とする。<br>"
       r"(1) $\sqrt{4n+1}<\sqrt n+\sqrt{n+1}<\sqrt{4n+2}$ を示せ。<br>"
       r"(2) $[\sqrt n+\sqrt{n+1}]=[\sqrt{4n+3}]$ を示せ。<br>"
       r"(3) $[\sqrt n+\sqrt{n+1}]=20$ となる自然数 $n$ をすべて求めよ。",
  "hint": r"(1) 各辺を2乗して比べ、$2\sqrt{n^2+n}$ を $2n$ と $2n+1$ ではさむ。(2) $\sqrt n+\sqrt{n+1}$ と $\sqrt{4n+3}$ の間に整数が入り込まないことを示す。入り込むとその整数の平方が $4n+2$ か $4n+3$ になるが、<b>平方数を $4$ で割った余りは $0$ か $1$</b> である。",
  "sol": r"(1) $(\sqrt n+\sqrt{n+1})^2=2n+1+2\sqrt{n^2+n}$<br>"
         r"$n^2<n^2+n<n^2+n+\dfrac14=\left(n+\dfrac12\right)^2$ より　$n<\sqrt{n^2+n}<n+\dfrac12$<br>"
         r"よって $4n+1<(\sqrt n+\sqrt{n+1})^2<4n+2$。各辺は正であるから、$\sqrt{4n+1}<\sqrt n+\sqrt{n+1}<\sqrt{4n+2}$　■<br>"
         r"(2) $m=[\sqrt n+\sqrt{n+1}]$ とおくと　$m\leqq\sqrt n+\sqrt{n+1}<m+1$ ……①<br>"
         r"①と (1) より $m<\sqrt{4n+2}<\sqrt{4n+3}$ であるから、$[\sqrt{4n+3}]\geqq m$。<br>"
         r"もし $[\sqrt{4n+3}]\geqq m+1$ とすると、$m+1\leqq\sqrt{4n+3}$ より $(m+1)^2\leqq4n+3$。<br>"
         r"一方、①と (1) より $m+1>\sqrt n+\sqrt{n+1}>\sqrt{4n+1}$ なので $(m+1)^2>4n+1$。<br>"
         r"よって $(m+1)^2$ は $4n+2$ か $4n+3$ で、$4$ で割った余りは $2$ か $3$ になる。<br>"
         r"ところが整数 $k$ について、$k=2l$ なら $k^2=4l^2$，$k=2l+1$ なら $k^2=4(l^2+l)+1$ であるから、平方数を $4$ で割った余りは $0$ か $1$ である。これは矛盾。<br>"
         r"したがって $[\sqrt{4n+3}]=m$，すなわち $[\sqrt n+\sqrt{n+1}]=[\sqrt{4n+3}]$　■<br>"
         r"(3) (2) より、条件は $[\sqrt{4n+3}]=20$，すなわち $20\leqq\sqrt{4n+3}<21$ と同値である。<br>"
         r"$400\leqq4n+3<441$ より $\dfrac{397}{4}\leqq n<\dfrac{438}{4}$，すなわち $99.25\leqq n<109.5$<br>"
         r"よって　$\boldsymbol{n=100,\ 101,\ 102,\ \cdots,\ 109}$（$10$ 個）",
  "note": r"(1) だけで分かるのは $[\sqrt n+\sqrt{n+1}]=[\sqrt{4n+1}]$ まで（$4n+1$ と $4n+2$ の間に平方数がないため）。$\sqrt{4n+3}$ まで広げられるのは、平方数の $4$ で割った余りという整数の性質による。結局 $[\sqrt n+\sqrt{n+1}]=[\sqrt{4n+1}]=[\sqrt{4n+2}]=[\sqrt{4n+3}]$ が成り立つ。ただし $\sqrt{4n+4}$ まで広げると、$n+1$ が平方数のとき成り立たない（$n=3$ のとき $[\sqrt3+2]=3$，$[\sqrt{16}]=4$）。",
  "ex": r"$n$ を自然数とし、$[x]$ は $x$ を超えない最大の整数を表す。<br>(1) $\sqrt{4n+3}<\sqrt n+\sqrt{n+2}<\sqrt{4n+4}$ を示せ。<br>(2) $[\sqrt n+\sqrt{n+2}]=[\sqrt{4n+2}]$ を示せ。<br>(3) $[\sqrt n+\sqrt{n+2}]=30$ となる自然数 $n$ の個数を求めよ。",
  "exa": r"(1) 2乗すると $2n+2+2\sqrt{n^2+2n}$ で、$n+\dfrac12<\sqrt{n^2+2n}<n+1$　(2) $m=[\sqrt n+\sqrt{n+2}]$ が $\sqrt{4n+2}$ より大きいとすると $4n+2<m^2<4n+4$ より $m^2=4n+3$ となり、平方数を $4$ で割った余りが $0$ か $1$ であることに矛盾　(3) $15$ 個（$n=225,\ \cdots,\ 239$）"},
]})


def _v3():
    # 循環小数
    def rep(intpart, nonrep, rep_):        # 例: 1.2(34) → intpart="1", nonrep="2", rep_="34"
        k, r = len(nonrep), len(rep_)
        A = int(intpart + nonrep + rep_)
        B = int(intpart + nonrep)
        return Fr(A - B, (10**r - 1) * 10**k)
    assert rep("0", "", "36") == Fr(4, 11) == Fr(36, 99)
    assert rep("1", "2", "34") == Fr(611, 495) == Fr(1222, 990)
    assert 99 * Fr(611, 495) == Fr(1222, 10) and 99 * Fr(4, 11) == 36
    assert rep("0", "", "123") == Fr(41, 333) and rep("0", "4", "5") == Fr(41, 90)
    # 根号の計算
    s2, s3, s5, s6, s7 = sqrt(2), sqrt(3), sqrt(5), sqrt(6), sqrt(7)
    assert simplify(sqrt(50)-sqrt(18)+sqrt(8) - 4*s2) == 0
    assert expand((2*s3-s2)*(s3+2*s2)) == 2+3*s6
    assert simplify(s3/(s3-s2) - s2/(s3+s2) - 5) == 0
    assert simplify(sqrt(48)-sqrt(27)+sqrt(12) - 3*s3) == 0
    assert simplify(1/(2-s3)+1/(2+s3) - 4) == 0
    assert expand((s5+s2)**2-(s5-s2)**2) == 4*sqrt(10)
    # √(a^2)=|a|
    for X in [Fr(k, 7) for k in range(-60, 60)]:
        P = abs(X-1) + abs(X+2)
        if X >= 1: assert P == 2*X+1
        elif X >= -2: assert P == 3
        else: assert P == -2*X-1
        Q = abs(X+3) - abs(X-2)
        if X >= 2: assert Q == 5
        elif X >= -3: assert Q == 2*X+1
        else: assert Q == -5
    assert expand((x-1)**2) == x**2-2*x+1 and expand((x+2)**2) == x**2+4*x+4
    # 二重根号
    assert expand((s5+s2)**2) == 7+2*sqrt(10)
    assert expand((s6-s2)**2) == 8-sqrt(48) and N(s6-s2) > 0
    assert expand(((s6+s2)/2)**2) == 2+s3
    assert expand((s7-s2)**2) == 9-2*sqrt(14)
    assert expand(((sqrt(10)-s6)/2)**2) == 4-sqrt(15)
    # 3項の有理化
    assert close(1/(1+s2+s3), (2+s2-s6)/4)
    assert expand((1+s2+s3)*(1+s2-s3)) == 2*s2
    assert close(1/(s2+s3+s5), (2*s3+3*s2-sqrt(30))/12)
    assert expand((s2+s3+s5)*(s2+s3-s5)) == 2*s6
    assert close(2/(1-s2+s3), (2-s2+s6)/2)
    # 整数部分・小数部分
    v = 2/(3-s7)
    assert close(v, 3+s7) and math.floor(N(v, 30)) == 5
    bb = s7-2
    assert expand(bb**2+4*bb) == 3
    assert math.floor(N(5/bb, 30)) == 7 and 2.6**2 < 7 < 2.7**2
    assert 7 < 5*4.6/3 and 5*4.7/3 < 8
    v = 1/(s5-2)
    assert close(v, s5+2) and math.floor(N(v, 30)) == 4
    bb = s5-2
    assert expand(bb**2+4*bb) == 1 and math.floor(N(4/bb, 30)) == 16
    # ★5：[√n+√(n+1)] = [√(4n+1)] = [√(4n+3)]
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    fl = lambda D: int(D.to_integral_value(rounding="ROUND_FLOOR"))
    for n in range(1, 3000):
        s = Decimal(n).sqrt() + Decimal(n+1).sqrt()
        m = fl(s)
        assert m == math.isqrt(4*n+1) == math.isqrt(4*n+2) == math.isqrt(4*n+3)
        assert Decimal(4*n+1).sqrt() < s < Decimal(4*n+2).sqrt()
        s2_ = Decimal(n).sqrt() + Decimal(n+2).sqrt()
        assert fl(s2_) == math.isqrt(4*n+2) == math.isqrt(4*n+3)
        assert Decimal(4*n+3).sqrt() < s2_ < Decimal(4*n+4).sqrt()
    sol = [n for n in range(1, 3000) if fl(Decimal(n).sqrt() + Decimal(n+1).sqrt()) == 20]
    assert sol == list(range(100, 110))
    sol = [n for n in range(1, 3000) if fl(Decimal(n).sqrt() + Decimal(n+2).sqrt()) == 30]
    assert sol == list(range(225, 240)) and len(sol) == 15
    assert fl(Decimal(3).sqrt() + 2) == 3 and math.isqrt(16) == 4
    assert {k*k % 4 for k in range(200)} == {0, 1}


VER.append(_v3)

# ---------------------------------------------------------------- 節4
SEC.append({"title": r"式の値と対称式",
"base": r"""・2変数の対称式は基本対称式 $x+y$，$xy$ で表せる：$x^2+y^2=(x+y)^2-2xy$，$x^3+y^3=(x+y)^3-3xy(x+y)$<br>
・$x^2+\dfrac1{x^2}=\left(x+\dfrac1x\right)^2-2$，$x^3+\dfrac1{x^3}=\left(x+\dfrac1x\right)^3-3\left(x+\dfrac1x\right)$<br>
・3変数：$a^2+b^2+c^2=(a+b+c)^2-2(ab+bc+ca)$<br>
・実数 $x,\ y$ が存在する条件：$x,\ y$ は $t^2-(x+y)t+xy=0$ の2つの実数解なので $(x+y)^2-4xy\geqq0$<br>
・次数下げ：$x$ が満たす2次の関係式（例 $x^2=x+1$）を使って高次の式の次数を下げる。""",
"items": [
 {"lv": 1, "title": r"$x+\dfrac1x$ の値から式の値を求める",
  "q": r"$x+\dfrac1x=3$ のとき、次の式の値を求めよ。<br>(1) $x^2+\dfrac1{x^2}$　(2) $x^3+\dfrac1{x^3}$　(3) $x^4+\dfrac1{x^4}$",
  "hint": r"$x\cdot\dfrac1x=1$ なので、$x$ と $\dfrac1x$ の対称式は和 $x+\dfrac1x$ だけで表せる。",
  "sol": r"(1) $x^2+\dfrac1{x^2}=\left(x+\dfrac1x\right)^2-2\cdot x\cdot\dfrac1x=9-2=\boldsymbol{7}$<br>"
         r"(2) $x^3+\dfrac1{x^3}=\left(x+\dfrac1x\right)^3-3\cdot x\cdot\dfrac1x\left(x+\dfrac1x\right)=27-9=\boldsymbol{18}$<br>"
         r"(3) $x^4+\dfrac1{x^4}=\left(x^2+\dfrac1{x^2}\right)^2-2=49-2=\boldsymbol{47}$",
  "note": r"(2) は $\left(x^2+\dfrac1{x^2}\right)\left(x+\dfrac1x\right)=x^3+\dfrac1{x^3}+x+\dfrac1x$ を使って $7\cdot3-3=18$ としてもよい。",
  "ex": r"$x-\dfrac1x=2$ のとき、$x^2+\dfrac1{x^2}$ と $x^3-\dfrac1{x^3}$ の値を求めよ。",
  "exa": r"$x^2+\dfrac1{x^2}=6$，$x^3-\dfrac1{x^3}=14$"},
 {"lv": 2, "title": r"根号を含む数の対称式の値",
  "q": r"$x=\dfrac{\sqrt5+\sqrt3}{\sqrt5-\sqrt3}$，$y=\dfrac{\sqrt5-\sqrt3}{\sqrt5+\sqrt3}$ のとき、次の式の値を求めよ。<br>(1) $x+y,\ xy$　(2) $x^2+y^2$　(3) $x^3+y^3$　(4) $x^5+y^5$",
  "hint": r"$x,\ y$ を別々に代入するのではなく、まず $x+y$ と $xy$ を求め、求める式をそれらで表す。(4) は低い次数の対称式の積から余分な項を引く。",
  "sol": r"$x=\dfrac{(\sqrt5+\sqrt3)^2}{5-3}=\dfrac{8+2\sqrt{15}}{2}=4+\sqrt{15}$，同様に $y=4-\sqrt{15}$<br>"
         r"(1) $x+y=\boldsymbol{8}$，$xy=\dfrac{\sqrt5+\sqrt3}{\sqrt5-\sqrt3}\cdot\dfrac{\sqrt5-\sqrt3}{\sqrt5+\sqrt3}=\boldsymbol{1}$<br>"
         r"(2) $x^2+y^2=(x+y)^2-2xy=64-2=\boldsymbol{62}$<br>"
         r"(3) $x^3+y^3=(x+y)^3-3xy(x+y)=512-24=\boldsymbol{488}$<br>"
         r"(4) $(x^2+y^2)(x^3+y^3)=x^5+y^5+x^2y^2(x+y)$ より<br>"
         r"$x^5+y^5=62\cdot488-1^2\cdot8=30256-8=\boldsymbol{30248}$",
  "note": r"$x^n+y^n$ は、$(x+y)(x^{n-1}+y^{n-1})=x^n+y^n+xy(x^{n-2}+y^{n-2})$ を使って次々に求めることもできる。この例題では $x^4+y^4=8\cdot488-62=3842$，$x^5+y^5=8\cdot3842-488=30248$。",
  "ex": r"$x=\dfrac{1}{2+\sqrt3}$，$y=\dfrac{1}{2-\sqrt3}$ のとき、$x^2+y^2$，$x^3+y^3$，$x^4+y^4$ の値を求めよ。",
  "exa": r"$x^2+y^2=14$，$x^3+y^3=52$，$x^4+y^4=194$"},
 {"lv": 3, "title": r"次数を下げて式の値を求める",
  "q": r"$x=\dfrac{1+\sqrt5}{2}$ とする。<br>(1) $x^2=x+1$ が成り立つことを示せ。<br>(2) $P=x^5-2x^4+2x^3-3x^2+x+4$ の値を求めよ。<br>(3) $x^5$ の整数部分を求めよ。",
  "hint": r"$x$ をそのまま5乗するのは大変。$2x-1=\sqrt5$ を2乗すると根号の消えた関係式 $x^2=x+1$ が得られる。これで $x^2$ を $x+1$ に置き換えていけば、どんな高次の式も $px+q$ の形まで次数が下がる。",
  "sol": r"(1) $2x-1=\sqrt5$ の両辺を2乗して $4x^2-4x+1=5$。よって $x^2=x+1$　■<br>"
         r"(2) (1) を繰り返し用いると<br>"
         r"$x^3=x\cdot x^2=x^2+x=2x+1$，$x^4=x\cdot x^3=2x^2+x=3x+2$，$x^5=x\cdot x^4=3x^2+2x=5x+3$<br>"
         r"$P=(5x+3)-2(3x+2)+2(2x+1)-3(x+1)+x+4=x+2=\boldsymbol{\dfrac{5+\sqrt5}{2}}$<br>"
         r"(3) $x^5=5x+3=\dfrac{5+5\sqrt5}{2}+3=\dfrac{11+5\sqrt5}{2}$<br>"
         r"$2.2^2=4.84$，$2.3^2=5.29$ より $2.2<\sqrt5<2.3$ なので $11<5\sqrt5<11.5$<br>"
         r"よって $11<x^5<11.25$ で、$x^5$ の整数部分は $\boldsymbol{11}$",
  "note": r"整式の割り算（数学II）を使えば、$P$ を $x^2-x-1$ で割った余り $x+2$ が $P$ の値になる。次数下げはその代わりになる方法である。$x^n=F_nx+F_{n-1}$ と表したときの係数 $1,\ 1,\ 2,\ 3,\ 5,\ \cdots$ はフィボナッチ数になっている。",
  "ex": r"$x=1+\sqrt2$ のとき、$x^2=2x+1$ を用いて $x^4-2x^3-x^2+3x+1$ の値を求めよ。また、$x^4$ の整数部分を求めよ。",
  "exa": r"$4+3\sqrt2$；$x^4=17+12\sqrt2$ の整数部分は $33$（$1.414<\sqrt2<1.415$ で評価）"},
 {"lv": 4, "title": r"対称式の値域（実数条件）",
  "q": r"実数 $x,\ y$ が $x^2+xy+y^2=3$ を満たすとき、次の式のとり得る値の範囲を求めよ。<br>(1) $x+y$　(2) $x^2-3xy+y^2$",
  "hint": r"$x+y=s$，$xy=p$ とおくと、条件も目標の式も $s,\ p$ で表せる。ただし $s,\ p$ は自由には動けない。<b>$x,\ y$ が実数である条件 $s^2-4p\geqq0$</b> を必ず加える。",
  "sol": r"$x+y=s,\ xy=p$ とおくと、条件は $s^2-p=3$，すなわち $p=s^2-3$ ……①<br>"
         r"$x,\ y$ は $t$ の2次方程式 $t^2-st+p=0$ の2つの実数解であるから、判別式について $s^2-4p\geqq0$。①を代入して $s^2-4(s^2-3)\geqq0$，すなわち $s^2\leqq4$。<br>"
         r"逆に $-2\leqq s\leqq2$ のとき、$t^2-st+s^2-3=0$ は実数解をもち、その2解を $x,\ y$ とすると $x+y=s,\ xy=s^2-3$ で、$x^2+xy+y^2=s^2-p=3$ を満たす。<br>"
         r"(1) よって　$\boldsymbol{-2\leqq x+y\leqq2}$<br>"
         r"(2) $x^2-3xy+y^2=s^2-5p=s^2-5(s^2-3)=15-4s^2$<br>"
         r"$0\leqq s^2\leqq4$ より $-1\leqq15-4s^2\leqq15$。最小値 $-1$ は $s=\pm2$（例えば $x=y=1$），最大値 $15$ は $s=0$（例えば $x=\sqrt3,\ y=-\sqrt3$）のときにとるから<br>"
         r"$\boldsymbol{-1\leqq x^2-3xy+y^2\leqq15}$",
  "note": r"実数条件を忘れると $s$ がいくらでも大きくなれるように見え、(2) の最小値が求まらない。求める式が $s$ の2次式になる場合（練習）は、平方完成して $s$ の範囲での最大・最小を調べる。",
  "ex": r"実数 $x,\ y$ が $x^2+y^2=4$ を満たすとき、$x+y+xy$ のとり得る値の範囲を求めよ。",
  "exa": r"$-\dfrac52\leqq x+y+xy\leqq2+2\sqrt2$"},
 {"lv": 5, "title": r"3変数の対称式と実数条件・微分を使わない最大最小",
  "q": r"実数 $a,\ b,\ c$ が $a+b+c=0$，$a^2+b^2+c^2=6$ を満たしている。<br>"
       r"(1) $ab+bc+ca$ の値と、$c$ のとり得る値の範囲を求めよ。<br>"
       r"(2) $abc$ の最大値と最小値を求めよ。<br>"
       r"(3) $a^5+b^5+c^5$ の最大値を求めよ。",
  "hint": r"(1) $a+b$ も $ab$ も $c$ で表せる。$a,\ b$ が実数である条件から $c$ の範囲が出る。(2) $abc$ は $c$ の3次式。最大値の候補 $k$ に見当をつけ（$a=b$ となる場合など）、$k-abc$ を因数分解して符号を調べる。(3) $a,\ b,\ c$ はどれも $t^3-3t-abc=0$ を満たすことを使って次数を下げる。",
  "sol": r"(1) $2(ab+bc+ca)=(a+b+c)^2-(a^2+b^2+c^2)=0-6$ より　$ab+bc+ca=\boldsymbol{-3}$<br>"
         r"$a+b=-c$，$ab=-3-c(a+b)=c^2-3$。よって $a,\ b$ は $t$ の2次方程式 $t^2+ct+c^2-3=0$ の2つの実数解であるから　$c^2-4(c^2-3)\geqq0$，$c^2\leqq4$<br>"
         r"逆に $-2\leqq c\leqq2$ のとき、この2次方程式の実数解を $a,\ b$ とすると $a+b+c=0$，$ab+bc+ca=(c^2-3)+c(a+b)=-3$ で、$a^2+b^2+c^2=0^2-2\cdot(-3)=6$ を満たす。<br>"
         r"よって　$\boldsymbol{-2\leqq c\leqq2}$<br>"
         r"(2) $abc=(c^2-3)c=c^3-3c$。$-2\leqq c\leqq2$ のとき<br>"
         r"$2-abc=-(c^3-3c-2)=-(c-2)(c+1)^2\geqq0$，　$abc+2=c^3-3c+2=(c-1)^2(c+2)\geqq0$<br>"
         r"よって $-2\leqq abc\leqq2$。$abc=2$ となるのは $c=2$ または $c=-1$ のときで、例えば $(a,\ b,\ c)=(-1,\ -1,\ 2)$。$abc=-2$ となるのは例えば $(a,\ b,\ c)=(1,\ 1,\ -2)$。<br>"
         r"したがって　最大値 $\boldsymbol{2}$，最小値 $\boldsymbol{-2}$<br>"
         r"(3) $abc=r$ とおくと<br>$(t-a)(t-b)(t-c)=t^3-(a+b+c)t^2+(ab+bc+ca)t-abc=t^3-3t-r$<br>"
         r"この式で $t=a$ とおくと左辺は $0$ なので $a^3=3a+r$。同様に $b^3=3b+r$，$c^3=3c+r$。<br>"
         r"よって $a^5=a^2\cdot a^3=3a^3+ra^2=3(3a+r)+ra^2=9a+3r+ra^2$。$b,\ c$ も同様で、辺々加えると<br>"
         r"$a^5+b^5+c^5=9(a+b+c)+9r+r(a^2+b^2+c^2)=0+9r+6r=15abc$<br>"
         r"(2) より $abc\leqq2$ なので $a^5+b^5+c^5\leqq30$。等号は $(a,\ b,\ c)=(-1,\ -1,\ 2)$ などで成り立つ。<br>"
         r"よって最大値は　$\boldsymbol{30}$",
  "note": r"(2) の「候補の値 $k$ との差を因数分解する」方法は、3次式の最大・最小を微分なしで示す強力な手段である。$c^3-3c-2$ が $(c+1)^2$ を因数にもつのは、$c=-1$ でも最大になる（$a,\ b,\ c$ の役割を入れかえた $(2,\ -1,\ -1)$）からである。(3) と同様にして $a^3+b^3+c^3=3abc$，$a^4+b^4+c^4=18$ も得られる。",
  "ex": r"実数 $a,\ b,\ c$ が $a+b+c=0$，$a^2+b^2+c^2=2$ を満たすとき、$c$ のとり得る値の範囲と、$a^3+b^3+c^3$ の最大値を求めよ。",
  "exa": r"$-\dfrac{2\sqrt3}{3}\leqq c\leqq\dfrac{2\sqrt3}{3}$，最大値 $\dfrac{2\sqrt3}{3}$"},
]})


def _v4():
    s2, s3, s5 = sqrt(2), sqrt(3), sqrt(5)
    X = (3+s5)/2                       # x+1/x=3
    assert close(X+1/X, 3)
    assert close(X**2+X**-2, 7) and close(X**3+X**-3, 18) and close(X**4+X**-4, 47)
    X = 1+s2                           # x-1/x=2
    assert close(X-1/X, 2) and close(X**2+X**-2, 6) and close(X**3-X**-3, 14)
    # 根号を含む対称式
    X, Y = (s5+sqrt(3))/(s5-sqrt(3)), (s5-sqrt(3))/(s5+sqrt(3))
    assert close(X, 4+sqrt(15)) and close(Y, 4-sqrt(15))
    assert close(X+Y, 8) and close(X*Y, 1) and close(X**2+Y**2, 62) and close(X**3+Y**3, 488)
    assert close(X**4+Y**4, 3842) and close(X**5+Y**5, 30248) and 62*488 == 30256
    X, Y = 1/(2+s3), 1/(2-s3)
    assert close(X**2+Y**2, 14) and close(X**3+Y**3, 52) and close(X**4+Y**4, 194)
    # 次数下げ
    X = (1+s5)/2
    assert expand(X**2-X-1) == 0
    P = X**5-2*X**4+2*X**3-3*X**2+X+4
    assert close(P, (5+s5)/2) and close(X**5, 5*X+3) and close(X**4, 3*X+2) and close(X**3, 2*X+1)
    assert math.floor(N(X**5, 30)) == 11 and close(X**5, (11+5*s5)/2) and 2.2**2 < 5 < 2.3**2
    X = 1+s2
    assert expand(X**2-2*X-1) == 0
    assert close(X**4-2*X**3-X**2+3*X+1, 4+3*s2) and close(X**4, 17+12*s2)
    assert math.floor(N(X**4, 30)) == 33 and 1.414**2 < 2 < 1.415**2 and 33 < 17+12*1.414 and 17+12*1.415 < 34
    # 値域：x^2+xy+y^2=3 → x=u-v, y=u+v, 3u^2+v^2=3
    S, T = [], []
    M = 40000
    for k in range(M):
        th = 2*math.pi*k/M
        u, v = math.cos(th), math.sqrt(3)*math.sin(th)
        X_, Y_ = u-v, u+v
        assert abs(X_*X_+X_*Y_+Y_*Y_-3) < 1e-9
        S.append(X_+Y_); T.append(X_*X_-3*X_*Y_+Y_*Y_)
    assert abs(min(S)+2) < 1e-6 and abs(max(S)-2) < 1e-6
    assert abs(min(T)+1) < 1e-6 and abs(max(T)-15) < 1e-6
    assert 1+1+1 == 3 and 1-3+1 == -1
    U = [2*math.cos(2*math.pi*k/M)+2*math.sin(2*math.pi*k/M)+4*math.cos(2*math.pi*k/M)*math.sin(2*math.pi*k/M) for k in range(M)]
    assert abs(min(U)+2.5) < 1e-6 and abs(max(U)-(2+2*math.sqrt(2))) < 1e-6
    # ★5：a+b+c=0, a^2+b^2+c^2=6 は a=2cos(θ), b=2cos(θ+2π/3), c=2cos(θ+4π/3)
    C_, R, F5 = [], [], []
    for k in range(M):
        th = 2*math.pi*k/M
        A_, B_, Cc = 2*math.cos(th), 2*math.cos(th+2*math.pi/3), 2*math.cos(th+4*math.pi/3)
        assert abs(A_+B_+Cc) < 1e-9 and abs(A_*A_+B_*B_+Cc*Cc-6) < 1e-9
        assert abs(A_*B_+B_*Cc+Cc*A_+3) < 1e-9
        C_.append(Cc); R.append(A_*B_*Cc); F5.append(A_**5+B_**5+Cc**5)
        assert abs(A_**5+B_**5+Cc**5-15*A_*B_*Cc) < 1e-8
        assert abs(A_**4+B_**4+Cc**4-18) < 1e-8 and abs(A_**3+B_**3+Cc**3-3*A_*B_*Cc) < 1e-8
    assert abs(min(C_)+2) < 1e-6 and abs(max(C_)-2) < 1e-6
    assert abs(min(R)+2) < 1e-6 and abs(max(R)-2) < 1e-6 and abs(max(F5)-30) < 1e-5
    assert expand(-(c-2)*(c+1)**2 - (2-(c**3-3*c))) == 0
    assert expand((c-1)**2*(c+2) - (c**3-3*c+2)) == 0
    assert (-1)**5+(-1)**5+2**5 == 30 and (-1)*(-1)*2 == 2
    # 記号的に：c=-(a+b) のとき a^5+b^5+c^5 = -5ab(a+b)(a^2+ab+b^2)
    assert expand(a**5+b**5+(-a-b)**5 + 5*a*b*(a+b)*(a**2+a*b+b**2)) == 0
    # 練習：a^2+b^2+c^2=2 → 振幅 2/√3
    A0 = 2/math.sqrt(3)
    C_, G = [], []
    for k in range(M):
        th = 2*math.pi*k/M
        A_, B_, Cc = A0*math.cos(th), A0*math.cos(th+2*math.pi/3), A0*math.cos(th+4*math.pi/3)
        assert abs(A_*A_+B_*B_+Cc*Cc-2) < 1e-9
        C_.append(Cc); G.append(A_**3+B_**3+Cc**3)
    assert abs(max(C_)-2*math.sqrt(3)/3) < 1e-6 and abs(min(C_)+2*math.sqrt(3)/3) < 1e-6
    assert abs(max(G)-2*math.sqrt(3)/3) < 1e-6
    tt = 1/sqrt(3)
    assert expand((c-2*tt)*(c+tt)**2 - (c**3-c-2/(3*sqrt(3)))) == 0


VER.append(_v4)

# ---------------------------------------------------------------- 節5
SEC.append({"title": r"1次不等式",
"base": r"""・不等式の両辺に同じ数を足しても引いても、不等号の向きは変わらない。正の数を掛ける・割るときも変わらない。<b>負の数を掛ける・割るときは向きが逆になる</b>。<br>
・連立不等式は、それぞれの不等式の解の共通範囲（数直線で確認）。$A<B<C$ は「$A<B$ かつ $B<C$」。<br>
・文字係数の不等式 $ax>b$：$a>0$ なら $x>\dfrac ba$，$a<0$ なら $x<\dfrac ba$，$a=0$ なら $b<0$ のときすべての実数、$b\geqq0$ のとき解なし。<br>
・$[x]$（$x$ を超えない最大の整数）は、$[x]=n\iff n\leqq x<n+1$（$n$ は整数）と不等式に直して扱う。""",
"items": [
 {"lv": 1, "title": r"1次不等式を解く",
  "q": r"次の不等式を解け。<br>(1) $3x-7>5x+1$　(2) $\dfrac{2x-1}{3}-\dfrac{x-2}{4}\leqq1$　(3) $0.3x-1.2<0.5x+0.4$",
  "hint": r"$x$ の項を左辺に、定数項を右辺に集めて $ax>b$ の形にする。分数・小数は、両辺に正の数を掛けて係数を整数にしてから解く。$x$ の係数が負のとき、割ると不等号の向きが変わる。",
  "sol": r"(1) $3x-5x>1+7$ より $-2x>8$。両辺を $-2$ で割って　$\boldsymbol{x<-4}$<br>"
         r"(2) 両辺に $12$ を掛けて $4(2x-1)-3(x-2)\leqq12$，$5x+2\leqq12$，$5x\leqq10$。よって　$\boldsymbol{x\leqq2}$<br>"
         r"(3) 両辺に $10$ を掛けて $3x-12<5x+4$，$-2x<16$。よって　$\boldsymbol{x>-8}$",
  "note": r"(1) で $-2x>8$ から $x>-4$ とする誤りが多い。負の数で割るときは不等号の向きを逆にする。$x=-5$ などを代入して、もとの不等式を満たすか確かめるとよい。",
  "ex": r"次の不等式を解け。<br>(1) $2(x-3)\geqq5x+6$　(2) $\dfrac{x+1}{2}-\dfrac{2x-1}{3}>\dfrac16$",
  "exa": r"(1) $x\leqq-4$　(2) $x<4$"},
 {"lv": 2, "title": r"連立不等式と $A<B<C$ 型の不等式",
  "q": r"(1) 連立不等式 $\begin{cases}4x-3>2x+1\\ 3(x-1)\leqq x+9\end{cases}$ を解け。また、それを満たす整数 $x$ をすべて求めよ。<br>(2) 不等式 $3x-4\leqq x+6<4x$ を解け。",
  "hint": r"それぞれの不等式を解き、数直線上で共通範囲を求める。端の値を含むか（$\leqq$ か $<$ か）に注意。(2) は「$3x-4\leqq x+6$ かつ $x+6<4x$」として解く。",
  "sol": r"(1) $4x-3>2x+1$ より $x>2$ ……①　$3x-3\leqq x+9$ より $x\leqq6$ ……②<br>"
         r"①，②の共通範囲は　$\boldsymbol{2<x\leqq6}$。これを満たす整数は　$\boldsymbol{x=3,\ 4,\ 5,\ 6}$<br>"
         r"(2) $3x-4\leqq x+6$ より $x\leqq5$。$x+6<4x$ より $x>2$。よって　$\boldsymbol{2<x\leqq5}$",
  "note": r"(2) を「$3x-4<4x$ かつ $x+6<4x$」のように組んではいけない。$A<B<C$ から $A<C$ は導かれるが、$A<C$ と $B<C$ だけでは $A<B$ は保証されない。",
  "ex": r"(1) 連立不等式 $\begin{cases}2x+5\geqq5x-4\\ 3x+2>x-4\end{cases}$ を満たす整数 $x$ の個数を求めよ。<br>(2) 不等式 $x-1<2x+3\leqq6-x$ を解け。",
  "exa": r"(1) $-3<x\leqq3$ より $6$ 個　(2) $-4<x\leqq1$"},
 {"lv": 2, "title": r"文字係数の1次不等式",
  "q": r"$a$ を定数とする。次の不等式を解け。<br>(1) $ax+2>x+a+1$　(2) $ax\leqq a^2$",
  "hint": r"$(x$ の係数$)\times x>($定数$)$ の形に整理し、$x$ の係数の符号で場合分けする。係数が $0$ になる場合を忘れない。",
  "sol": r"(1) 整理すると $(a-1)x>a-1$<br>"
         r"[1] $a-1>0$，すなわち $a>1$ のとき　$x>1$<br>"
         r"[2] $a-1=0$，すなわち $a=1$ のとき　$0\cdot x>0$ となり、これを満たす $x$ はない<br>"
         r"[3] $a-1<0$，すなわち $a<1$ のとき　$x<1$<br>"
         r"よって　$\boldsymbol{a>1}$ <b>のとき</b> $\boldsymbol{x>1}$，$\boldsymbol{a=1}$ <b>のとき解なし</b>，$\boldsymbol{a<1}$ <b>のとき</b> $\boldsymbol{x<1}$<br>"
         r"(2) [1] $a>0$ のとき、両辺を $a$ で割って　$x\leqq a$<br>"
         r"[2] $a=0$ のとき　$0\cdot x\leqq0$ となり、すべての実数 $x$ で成り立つ<br>"
         r"[3] $a<0$ のとき、両辺を $a$ で割って　$x\geqq a$<br>"
         r"よって　$\boldsymbol{a>0}$ <b>のとき</b> $\boldsymbol{x\leqq a}$，$\boldsymbol{a=0}$ <b>のとき解はすべての実数</b>，$\boldsymbol{a<0}$ <b>のとき</b> $\boldsymbol{x\geqq a}$",
  "note": r"$(a-1)x>a-1$ の両辺を $a-1$ で割って、いきなり「$x>1$」とするのは $a>1$ のときしか正しくない。文字で割るときは、その文字の式の符号と $0$ になる場合を必ず調べる。",
  "ex": r"$a$ を定数とする。不等式 $ax+1>x+a^2$ を解け。",
  "exa": r"$a>1$ のとき $x>a+1$，$a=1$ のとき解なし，$a<1$ のとき $x<a+1$"},
 {"lv": 3, "title": r"1次不等式の応用（過不足の問題）",
  "q": r"何人かの生徒に鉛筆を配る。1人に5本ずつ配ると12本余る。また、1人に7本ずつ配ると、最後の1人だけは7本より少なくなるが、1本以上は配ることができる。生徒の人数と鉛筆の本数として考えられるものをすべて求めよ。",
  "hint": r"生徒の人数を $n$ として鉛筆の本数を $n$ で表す。「最後の1人に配る本数」を $n$ の式で表し、条件を連立不等式にする。$n$ は自然数であることを使う。",
  "sol": r"生徒を $n$ 人とすると、鉛筆の本数は $5n+12$ 本。<br>"
         r"1人に7本ずつ $(n-1)$ 人に配ったとき、最後の1人に配る本数は $(5n+12)-7(n-1)=19-2n$（本）<br>"
         r"条件より $1\leqq19-2n<7$。<br>"
         r"$1\leqq19-2n$ より $n\leqq9$，$19-2n<7$ より $n>6$。よって $6<n\leqq9$ で、$n$ は自然数だから $n=7,\ 8,\ 9$<br>"
         r"したがって　<b>生徒7人・鉛筆47本，生徒8人・鉛筆52本，生徒9人・鉛筆57本</b>",
  "note": r"「1本以上」を落として $19-2n<7$ だけにすると、$n\geqq10$ も含まれてしまう（$n=10$ では鉛筆が $62$ 本で、9人に7本ずつ配ると $63$ 本必要になり足りない）。文章題では、得られた答えが問題文の条件をすべて満たすか確かめる。",
  "ex": r"何人かの生徒が長いすに座る。1脚に4人ずつ座ると8人が座れない。1脚に6人ずつ座ると、最後の1脚だけは1人以上6人未満になり、空いている長いすはない。長いすの数と生徒の人数として考えられるものをすべて求めよ。",
  "exa": r"長いす5脚・生徒28人，長いす6脚・生徒32人"},
 {"lv": 4, "title": r"文字係数の連立不等式と整数解",
  "q": r"$a$ を定数とする。$x$ の連立不等式 $\begin{cases}(a-1)x\geqq a^2-1\\ 2x-3<x+2\end{cases}$ について、次の問いに答えよ。<br>"
       r"(1) 連立不等式を解け。<br>"
       r"(2) 連立不等式を満たす整数 $x$ がちょうど2個となるような $a$ の値の範囲を求めよ。<br>"
       r"(3) 連立不等式を満たす整数 $x$ の最大値が $-3$ となるような $a$ の値の範囲を求めよ。",
  "hint": r"$a^2-1=(a-1)(a+1)$ に着目し、$x$ の係数 $a-1$ の符号（正・$0$・負）で場合分けする。(2)(3) は各場合の解を数直線にかき、整数がどこまで入るかを、境界の $a$ の値を代入して確かめる。",
  "sol": r"第2式より $x<5$ ……①。第1式は $(a-1)x\geqq(a-1)(a+1)$ ……②<br>"
         r"[1] $a>1$ のとき、②は $x\geqq a+1$。①と合わせて、$a+1<5$ なら $a+1\leqq x<5$，$a+1\geqq5$ なら解なし。<br>"
         r"[2] $a=1$ のとき、②は $0\cdot x\geqq0$ ですべての $x$ で成り立つから、解は $x<5$。<br>"
         r"[3] $a<1$ のとき、②は $x\leqq a+1$。$a+1<2<5$ なので、解は $x\leqq a+1$。<br>"
         r"(1) $\boldsymbol{a<1}$ <b>のとき</b> $\boldsymbol{x\leqq a+1}$，$\boldsymbol{a=1}$ <b>のとき</b> $\boldsymbol{x<5}$，$\boldsymbol{1<a<4}$ <b>のとき</b> $\boldsymbol{a+1\leqq x<5}$，$\boldsymbol{a\geqq4}$ <b>のとき解なし</b><br>"
         r"(2) $a\leqq1$ のときは整数解が無数にあり、$a\geqq4$ のときは解がない。よって $1<a<4$ で、$a+1\leqq x<5$ を満たす整数がちょうど2個、すなわち $3,\ 4$ となればよい。<br>"
         r"その条件は $2<a+1\leqq3$。よって　$\boldsymbol{1<a\leqq2}$<br>"
         r"（$a=2$ のとき $3\leqq x<5$ で整数は $3,\ 4$ の2個。$a=1$ は不適。）<br>"
         r"(3) $a\geqq1$ のときは、整数解があればその最大値は $4$ なので不適。$a<1$ のとき、$x\leqq a+1$ を満たす整数の最大値が $-3$ となる条件は $-3\leqq a+1<-2$，すなわち $-4\leqq a<-3$。これは $a<1$ を満たす。<br>"
         r"よって　$\boldsymbol{-4\leqq a<-3}$",
  "note": r"場合分けをしたら、各場合が問いの条件を満たしうるかを先に判断すると見通しがよい。(2) では $a\leqq1$ の場合（整数解が無数）がすぐ除かれ、(3) では逆に $a<1$ の場合だけが候補になる。境界の値は必ず代入して確かめる。",
  "ex": r"$a$ を定数とする。$x$ の連立不等式 $\begin{cases}(a+2)x<a^2-4\\ x>-3\end{cases}$ について、(1) 連立不等式を解け。(2) 連立不等式を満たす整数 $x$ がちょうど3個となるような $a$ の値の範囲を求めよ。",
  "exa": r"(1) $a>-1$ のとき $-3<x<a-2$，$-2\leqq a\leqq-1$ のとき解なし，$a<-2$ のとき $x>-3$　(2) $2<a\leqq3$"},
 {"lv": 5, "title": r"ガウス記号を含む方程式（小数部分で場合分け）",
  "q": r"実数 $x$ に対し、$x$ を超えない最大の整数を $[x]$ で表す。<br>"
       r"(1) 方程式 $[x]+[2x]+[3x]=2024$ を解け。<br>"
       r"(2) 方程式 $[x]+[2x]+[3x]=2026$ は実数解をもたないことを示せ。<br>"
       r"(3) $1$ 以上 $1000$ 以下の整数のうち、$[x]+[2x]+[3x]$ の値として現れるもの（ある実数 $x$ に対してその値になるもの）の個数を求めよ。",
  "hint": r"$x$ を整数部分 $n$ と小数部分 $t$ に分けると、$[2x]=2n+[2t]$ などより $[x]+[2x]+[3x]=6n+([2t]+[3t])$。$[2t]+[3t]$ は $t$ の区間によって $0,\ 1,\ 2,\ 3$ のどれかに決まる。",
  "sol": r"$n=[x]$，$t=x-n$ とおくと、$n$ は整数で $0\leqq t<1$。整数 $m$ と実数 $u$ について $[m+u]=m+[u]$ であるから<br>"
         r"$[x]+[2x]+[3x]=n+(2n+[2t])+(3n+[3t])=6n+f(t)$，　ただし $f(t)=[2t]+[3t]$<br>"
         r"$0\leqq t<\dfrac13$ のとき $f(t)=0+0=0$，　$\dfrac13\leqq t<\dfrac12$ のとき $f(t)=0+1=1$<br>"
         r"$\dfrac12\leqq t<\dfrac23$ のとき $f(t)=1+1=2$，　$\dfrac23\leqq t<1$ のとき $f(t)=1+2=3$<br>"
         r"よって $[x]+[2x]+[3x]$ は $6n+r$（$r=0,\ 1,\ 2,\ 3$）の形の整数であり、$6$ で割った余りは $r=f(t)$ である。……(*)<br>"
         r"(1) $2024=6\cdot337+2$ なので、(*) より $n=337$，$f(t)=2$，すなわち $\dfrac12\leqq t<\dfrac23$。<br>"
         r"$x=337+t$ であるから　$\boldsymbol{\dfrac{675}{2}\leqq x<\dfrac{1013}{3}}$<br>"
         r"(2) $2026=6\cdot337+4$ で、$6$ で割った余りが $4$ である。(*) より $[x]+[2x]+[3x]$ を $6$ で割った余りは $0,\ 1,\ 2,\ 3$ のいずれかなので、$2026$ に等しくなることはない。よって実数解をもたない。　■<br>"
         r"(3) (*) と、$t=0,\ \dfrac13,\ \dfrac12,\ \dfrac23$ で $f(t)=0,\ 1,\ 2,\ 3$ のすべてが実現することから、現れる値は「$6$ で割った余りが $0,\ 1,\ 2,\ 3$ の整数」全体である。<br>"
         r"$1$ から $996=6\cdot166$ までは、連続する $6$ 個の整数の組が $166$ 組あり、各組に適するものが $4$ 個ずつあるので $664$ 個。$997,\ 998,\ 999,\ 1000$ を $6$ で割った余りは $1,\ 2,\ 3,\ 4$ なので、適するのは $3$ 個。<br>"
         r"よって　$664+3=\boldsymbol{667}$ <b>個</b>",
  "note": r"$[x]+[2x]+[3x]$ は $x$ とともに階段状に増えるが、$x$ が整数を通過する瞬間に $[x],\ [2x],\ [3x]$ が同時に増えるため、値が $6n+3$ から $6n+6$ へ跳び、$6n+4,\ 6n+5$ が抜ける。ガウス記号の問題では「整数部分と小数部分に分ける」「小数部分の区間で場合分けする」が定石である。",
  "ex": r"$[x]$ を $x$ を超えない最大の整数とする。<br>(1) 方程式 $[x]+[3x]=50$ を解け。<br>(2) 方程式 $[x]+[3x]=2027$ は実数解をもたないことを示せ。<br>(3) $1$ 以上 $1000$ 以下の整数のうち、$[x]+[3x]$ の値として現れるものの個数を求めよ。",
  "exa": r"(1) $\dfrac{38}{3}\leqq x<13$　(2) $[x]+[3x]=4[x]+[3t]$（$t$ は $x$ の小数部分）を $4$ で割った余りは $0,\ 1,\ 2$ のいずれかで、$2027$ の余り $3$ にはならない　(3) $750$ 個"},
]})


def _v5():
    grid = [Fr(k, 12) for k in range(-240, 241)]
    for X in grid:
        assert (3*X-7 > 5*X+1) == (X < -4)
        assert ((2*X-1)/3 - (X-2)/4 <= 1) == (X <= 2)
        assert (Fr(3, 10)*X - Fr(12, 10) < Fr(5, 10)*X + Fr(4, 10)) == (X > -8)
        assert (2*(X-3) >= 5*X+6) == (X <= -4)
        assert ((X+1)/2 - (2*X-1)/3 > Fr(1, 6)) == (X < 4)
        assert ((4*X-3 > 2*X+1) and (3*(X-1) <= X+9)) == (2 < X <= 6)
        assert (3*X-4 <= X+6 < 4*X) == (2 < X <= 5)
        assert ((2*X+5 >= 5*X-4) and (3*X+2 > X-4)) == (-3 < X <= 3)
        assert (X-1 < 2*X+3 <= 6-X) == (-4 < X <= 1)
    assert [n for n in range(-10, 11) if 4*n-3 > 2*n+1 and 3*(n-1) <= n+9] == [3, 4, 5, 6]
    assert len([n for n in range(-10, 11) if 2*n+5 >= 5*n-4 and 3*n+2 > n-4]) == 6
    # 文字係数
    for A in [Fr(k, 4) for k in range(-20, 21)]:
        for X in grid:
            s1 = A*X+2 > X+A+1
            assert s1 == ((A > 1 and X > 1) or (A < 1 and X < 1))
            s2 = A*X <= A*A
            assert s2 == ((A > 0 and X <= A) or A == 0 or (A < 0 and X >= A))
            s3 = A*X+1 > X+A*A
            assert s3 == ((A > 1 and X > A+1) or (A < 1 and X < A+1))
    # 過不足
    ok = [(n, 5*n+12) for n in range(1, 200) if 7*(n-1) < 5*n+12 and 1 <= 5*n+12-7*(n-1) < 7]
    assert ok == [(7, 47), (8, 52), (9, 57)]
    assert 5*10+12 < 7*9
    ok = [(m, 4*m+8) for m in range(1, 200) if 1 <= 4*m+8-6*(m-1) < 6]
    assert ok == [(5, 28), (6, 32)]
    # 文字係数の連立と整数解
    BIG = 400
    def sols(A):
        return [n for n in range(-BIG, BIG) if (A-1)*n >= A*A-1 and 2*n-3 < n+2]
    two, mx = [], []
    for A in [Fr(k, 8) for k in range(-80, 81)]:
        S = sols(A)
        for X in grid:          # (1) の解の確認
            sat = (A-1)*X >= A*A-1 and 2*X-3 < X+2
            exp = (X <= A+1) if A < 1 else (X < 5) if A == 1 else (A+1 <= X < 5) if A < 4 else False
            assert sat == exp
        if len(S) == 2: two.append(A)
        if S and len(S) < BIG and max(S) == -3: mx.append(A)
        if S and min(S) > -BIG and max(S) == -3: mx.append(A)
    assert all(1 < A <= 2 for A in two) and Fr(2) in two and Fr(9, 8) in two and Fr(1) not in two
    assert len(two) == 8
    mx = sorted(set(mx))
    assert mx and all(-4 <= A < -3 for A in mx) and Fr(-4) in mx and Fr(-3) not in mx and len(mx) == 8
    # 練習
    three = []
    for A in [Fr(k, 8) for k in range(-80, 81)]:
        S = [n for n in range(-BIG, BIG) if (A+2)*n < A*A-4 and n > -3]
        for X in grid:
            sat = (A+2)*X < A*A-4 and X > -3
            exp = (-3 < X < A-2) if A > -1 else False if A >= -2 else (X > -3)
            assert sat == exp
        if len(S) == 3: three.append(A)
    assert all(2 < A <= 3 for A in three) and Fr(3) in three and len(three) == 8
    # ガウス記号
    fl = math.floor
    g = lambda X: fl(X) + fl(2*X) + fl(3*X)
    vals = {}
    for k in range(-60, 6*1100):          # g は区間 [k/6,(k+1)/6) で一定
        X = Fr(k, 6)
        assert g(X) == g(X + Fr(1, 13)) == g(X + Fr(1, 7))
        vals.setdefault(g(X), []).append(k)
    assert vals[2024] == [2025] and Fr(2025, 6) == Fr(675, 2) and Fr(2026, 6) == Fr(1013, 3)
    assert 2026 not in vals
    assert len([m for m in range(1, 1001) if m in vals]) == 667
    h = lambda X: fl(X) + fl(3*X)
    hv = {}
    for k in range(-30, 3*1100):          # h は区間 [k/3,(k+1)/3) で一定
        X = Fr(k, 3)
        assert h(X) == h(X + Fr(1, 7))
        hv.setdefault(h(X), []).append(k)
    assert hv[50] == [38] and 2027 not in hv
    assert len([m for m in range(1, 1001) if m in hv]) == 750


VER.append(_v5)

# ---------------------------------------------------------------- 節6
SEC.append({"title": r"絶対値を含む方程式・不等式",
"base": r"""・$|A|=A\ (A\geqq0)$，$|A|=-A\ (A<0)$。$|x-a|$ は数直線上の2点 $x,\ a$ の距離。<br>
・$c>0$ のとき　$|x|=c\iff x=\pm c$，　$|x|<c\iff-c<x<c$，　$|x|>c\iff x<-c$ または $c<x$<br>
・絶対値が2つ以上あるときは、中身が $0$ になる $x$ の値で区間を分けて場合分けする。各区間で得た解のうち、その区間に入るものだけを採用し、最後にすべてを合わせる。<br>
・$y=|x-p|+|x-q|$ などのグラフは折れ線。方程式の解の個数はグラフと直線の共有点の個数として調べられる。""",
"items": [
 {"lv": 2, "title": r"絶対値を含む方程式・不等式の基本",
  "q": r"次の方程式・不等式を解け。<br>(1) $|2x-3|=5$　(2) $|x+1|\geqq4$　(3) $|x-4|=3x$",
  "hint": r"(1)(2) は右辺が正の定数なので、基本事項の公式が使える。(3) は右辺に $x$ を含むので、中身 $x-4$ の符号で場合分けし、各場合の範囲に入る解だけを残す。",
  "sol": r"(1) $2x-3=\pm5$ より　$\boldsymbol{x=4,\ -1}$<br>"
         r"(2) $x+1\leqq-4$ または $4\leqq x+1$ より　$\boldsymbol{x\leqq-5,\ 3\leqq x}$<br>"
         r"(3) [1] $x\geqq4$ のとき　$x-4=3x$ より $x=-2$。これは $x\geqq4$ を満たさない。<br>"
         r"[2] $x<4$ のとき　$-(x-4)=3x$ より $x=1$。これは $x<4$ を満たす。<br>"
         r"よって　$\boldsymbol{x=1}$",
  "note": r"(3) を $x-4=\pm3x$ と解くと $x=-2,\ 1$ が出るが、$x=-2$ では右辺 $3x$ が負になるので不適。右辺に文字があるときは公式をそのまま使わず、場合分けするか、右辺 $\geqq0$ の確認をする。",
  "ex": r"次の方程式・不等式を解け。<br>(1) $|3x+1|<5$　(2) $|2x-1|=x+4$",
  "exa": r"(1) $-2<x<\dfrac43$　(2) $x=-1,\ 5$"},
 {"lv": 3, "title": r"絶対値を2つ含む方程式・不等式",
  "q": r"次の方程式・不等式を解け。<br>(1) $|x+1|+|x-2|=x+5$　(2) $|x-1|+2|x+2|<9$",
  "hint": r"中身が $0$ になる $x$ の値（(1) は $-1,\ 2$，(2) は $-2,\ 1$）で数直線を3つの区間に分け、それぞれの区間で絶対値をはずす。",
  "sol": r"(1) [1] $x<-1$ のとき　$-(x+1)-(x-2)=x+5$，$-2x+1=x+5$ より $x=-\dfrac43$。これは $x<-1$ を満たす。<br>"
         r"[2] $-1\leqq x<2$ のとき　$(x+1)-(x-2)=x+5$，$3=x+5$ より $x=-2$。これは $-1\leqq x<2$ を満たさない。<br>"
         r"[3] $x\geqq2$ のとき　$(x+1)+(x-2)=x+5$，$2x-1=x+5$ より $x=6$。これは $x\geqq2$ を満たす。<br>"
         r"よって　$\boldsymbol{x=-\dfrac43,\ 6}$<br>"
         r"(2) [1] $x<-2$ のとき　$-(x-1)-2(x+2)<9$，$-3x-3<9$ より $x>-4$。$x<-2$ と合わせて $-4<x<-2$<br>"
         r"[2] $-2\leqq x<1$ のとき　$-(x-1)+2(x+2)<9$，$x+5<9$ より $x<4$。合わせて $-2\leqq x<1$<br>"
         r"[3] $x\geqq1$ のとき　$(x-1)+2(x+2)<9$，$3x+3<9$ より $x<2$。合わせて $1\leqq x<2$<br>"
         r"[1]〜[3] を合わせて　$\boldsymbol{-4<x<2}$",
  "note": r"方程式では各区間の解を並べ、不等式では各区間で得た範囲の<b>和集合</b>をとる。(2) は、折れ線 $y=|x-1|+2|x+2|$ が直線 $y=9$ より下にある $x$ の範囲と考えてもよい。",
  "ex": r"次の方程式・不等式を解け。<br>(1) $|x-1|+|x+3|=6$　(2) $2|x|+|x-3|\leqq6$",
  "exa": r"(1) $x=-4,\ 2$　(2) $-1\leqq x\leqq3$"},
 {"lv": 4, "title": r"絶対値を含む方程式の解の個数（定点を通る直線）",
  "q": r"$a$ を定数とする。$x$ の方程式 $|x-1|+|x-3|=a(x+1)$ の異なる実数解の個数を調べよ。",
  "hint": r"左辺を $f(x)$ とおくと、$y=f(x)$ のグラフは折れ線。右辺 $y=a(x+1)$ は $a$ によらず点 $(-1,\ 0)$ を通る傾き $a$ の直線。直線を回転させて、折れ線の「角」を通るときや、折れ線の辺と平行になるときを境目として調べる。",
  "sol": r"<svg class='fig' width='220' height='160' viewBox='0 0 220 160'><line x1='10' y1='133.7' x2='212' y2='133.7' stroke='#333' stroke-width='0.8'/><line x1='61.7' y1='152' x2='61.7' y2='8' stroke='#333' stroke-width='0.8'/><text x='204' y='144.7' font-size='10'>x</text><text x='64.7' y='16' font-size='10'>y</text><text x='63.7' y='144.7' font-size='10'>O</text><polyline points='35.8,8.0 85.2,93.2 132.1,93.2 181.5,8.0' fill='none' stroke='#16367a' stroke-width='1.7'/><line x1='38.2' y1='133.7' x2='209.7' y2='59.7' stroke='#d9701e' stroke-width='1' stroke-dasharray='4,2'/><text x='179.7' y='69.7' font-size='10' fill='#d9701e'>a=1/2</text><line x1='38.2' y1='133.7' x2='160.3' y2='28.3' stroke='#d9701e' stroke-width='1' stroke-dasharray='4,2'/><text x='136.3' y='26.3' font-size='10' fill='#d9701e'>a=1</text><line x1='38.2' y1='133.7' x2='106.3' y2='16.1' stroke='#d9701e' stroke-width='1' stroke-dasharray='4,2'/><text x='108.3' y='20.1' font-size='10' fill='#d9701e'>a=2</text><circle cx='38.2' cy='133.7' r='2.3' fill='#d9701e'/><text x='29.2' y='144.7' font-size='10'>A</text><text x='82.2' y='144.7' font-size='10'>1</text><line x1='85.2' y1='93.2' x2='85.2' y2='133.7' stroke='#999' stroke-width='0.6' stroke-dasharray='2,2'/><circle cx='85.2' cy='93.2' r='1.8' fill='#16367a'/><text x='129.1' y='144.7' font-size='10'>3</text><line x1='132.1' y1='93.2' x2='132.1' y2='133.7' stroke='#999' stroke-width='0.6' stroke-dasharray='2,2'/><circle cx='132.1' cy='93.2' r='1.8' fill='#16367a'/><text x='52.7' y='97.2' font-size='10'>2</text><line x1='61.7' y1='93.2' x2='85.2' y2='93.2' stroke='#999' stroke-width='0.6' stroke-dasharray='2,2'/><text x='11.2' y='68.8' font-size='10' fill='#16367a'>y=f(x)</text></svg>$f(x)=|x-1|+|x-3|$ とおくと<br>"
         r"$x<1$ のとき $f(x)=-2x+4$，$1\leqq x\leqq3$ のとき $f(x)=2$，$x>3$ のとき $f(x)=2x-4$<br>"
         r"実数解の個数は、$y=f(x)$ のグラフと、点 $\mathrm{A}(-1,\ 0)$ を通る傾き $a$ の直線 $y=a(x+1)$ の共有点の個数に等しい（図）。各区間ごとに解を調べる。<br>"
         r"(i) $x<1$ のとき　$-2x+4=a(x+1)$ より $(a+2)x=4-a$。$a=-2$ なら解はない。$a\neq-2$ なら $x=\dfrac{4-a}{a+2}$ で、これが $x<1$ を満たす条件は、$a+2>0$ のとき $4-a<a+2$ より $a>1$，$a+2<0$ のとき $4-a>a+2$ より $a<1$（つねに成立）。よって $a<-2$ または $a>1$ のとき1個。<br>"
         r"(ii) $1\leqq x\leqq3$ のとき　$a(x+1)=2$。$a\leqq0$ なら解はない。$a>0$ なら $x=\dfrac2a-1$ で、$1\leqq\dfrac2a-1\leqq3$ より $\dfrac12\leqq a\leqq1$ のとき1個。<br>"
         r"(iii) $x>3$ のとき　$2x-4=a(x+1)$ より $(2-a)x=a+4$。$a=2$ なら解はない。$a<2$ なら $x=\dfrac{a+4}{2-a}>3$ より $a+4>6-3a$，$a>\dfrac12$。$a>2$ なら $a+4<6-3a$ より $a<\dfrac12$ となり不適。よって $\dfrac12<a<2$ のとき1個。<br>"
         r"(i)〜(iii) の解は属する区間が異なるので、個数を合計して<br>"
         r"$\boldsymbol{a<-2}$ <b>のとき1個</b>，$\boldsymbol{-2\leqq a<\dfrac12}$ <b>のとき0個</b>，$\boldsymbol{a=\dfrac12}$ <b>のとき1個</b>，$\boldsymbol{\dfrac12<a<2}$ <b>のとき2個</b>，$\boldsymbol{a\geqq2}$ <b>のとき1個</b>",
  "note": r"図で見ると、境目の傾きは、角 $(3,\ 2)$ を通る $a=\dfrac12$，角 $(1,\ 2)$ を通る $a=1$，右の辺と平行な $a=2$，左の辺と平行な $a=-2$ である。$a=1$ では直線が角 $(1,\ 2)$ を通るが、(i) と (ii) で同じ点を重複して数えないように区間の端の扱いをそろえることが大切（この解答では $x=1$ を (ii) に入れている）。",
  "ex": r"$a$ を定数とする。$x$ の方程式 $|x-1|+|x-3|=a(x-5)$ の異なる実数解の個数を調べよ。",
  "exa": r"$a\leqq-2$ のとき1個，$-2<a<-\dfrac12$ のとき2個，$a=-\dfrac12$ のとき1個，$-\dfrac12<a\leqq2$ のとき0個，$a>2$ のとき1個"},
 {"lv": 5, "title": r"絶対値を含む不等式の証明（対称性で場合を絞る）",
  "q": r"実数 $a,\ b,\ c$ に対して、次の不等式が成り立つことを証明せよ。<br>$|a|+|b|+|c|+|a+b+c|\geqq|a+b|+|b+c|+|c+a|$",
  "hint": r"7つの絶対値の中身の符号をすべて組み合わせて調べるのは無理。①$a,\ b,\ c$ を一斉に $-a,\ -b,\ -c$ にかえても、②$a,\ b,\ c$ を入れかえても、不等式は変わらない、という2つの対称性で場合を絞る。3つの数のうち2つは同符号であることに着目する。",
  "sol": r"$(a,\ b,\ c)$ を $(-a,\ -b,\ -c)$ にかえても両辺は変わらない。また、$a,\ b,\ c$ をどのように入れかえても両辺は変わらない。<br>"
         r"3つの数 $a,\ b,\ c$ のうち、少なくとも2つは「ともに $0$ 以上」または「ともに負」である。後者の場合は全体の符号を反転すれば前者になるから、$a\geqq0,\ b\geqq0$ の場合に示せば十分である。さらに $a,\ b$ を入れかえて $0\leqq a\leqq b$ としてよい。<br>"
         r"[1] $c\geqq0$ のとき：すべての絶対値がそのままはずれ、両辺とも $2(a+b+c)$ となって等号が成り立つ。<br>"
         r"[2] $c<0$ のとき：$c=-d\ (d>0)$ とおく。$|a+b|=a+b$ であるから<br>"
         r"(左辺)$-$(右辺)$=a+b+d+|a+b-d|-(a+b)-|b-d|-|a-d|=d+|a+b-d|-|a-d|-|b-d|$<br>"
         r"これを $D$ とおき、$0\leqq a\leqq b\leqq a+b$ と $d$ の大小で分ける。<br>"
         r"(i) $0<d\leqq a$ のとき　$D=d+(a+b-d)-(a-d)-(b-d)=2d>0$<br>"
         r"(ii) $a<d\leqq b$ のとき　$a+b-d\geqq a\geqq0$ より　$D=d+(a+b-d)-(d-a)-(b-d)=2a\geqq0$<br>"
         r"(iii) $b<d\leqq a+b$ のとき　$D=d+(a+b-d)-(d-a)-(d-b)=2(a+b-d)\geqq0$<br>"
         r"(iv) $a+b<d$ のとき　$D=d-(a+b-d)-(d-a)-(d-b)=0$<br>"
         r"いずれの場合も $D\geqq0$ である。以上により、不等式は成り立つ。　■",
  "note": r"等号は、$a,\ b,\ c$ がすべて $0$ 以上（またはすべて $0$ 以下）のときや、(iv) のように1つの数が他の2数と逆符号で絶対値がそれらの和以上のとき（例：$a=1,\ b=2,\ c=-5$）などに成り立つ。この不等式は Hlawka（フラウカ）の不等式の1次元版で、平面ベクトルでも成り立つ。「一般性を失わずに $a\geqq0,\ b\geqq0$ としてよい」のように<b>対称性で場合を減らす論法</b>は、場合分けの多い証明で威力を発揮する。",
  "ex": r"実数 $a,\ b,\ c$ に対して、不等式 $|a|+|b|+|c|\leqq|a+b-c|+|b+c-a|+|c+a-b|$ を証明せよ。",
  "exa": r"$p=b+c-a,\ q=c+a-b,\ r=a+b-c$ とおくと $a=\dfrac{q+r}{2}$，$b=\dfrac{r+p}{2}$，$c=\dfrac{p+q}{2}$。$|a|\leqq\dfrac{|q|+|r|}{2}$ などの3式を辺々加える"},
]})


def _v6():
    grid = [Fr(k, 12) for k in range(-360, 361)]
    root = lambda f: [X for X in grid if f(X)]
    assert root(lambda X: abs(2*X-3) == 5) == [-1, 4]
    assert root(lambda X: abs(X-4) == 3*X) == [1]
    assert root(lambda X: abs(2*X-1) == X+4) == [-1, 5]
    assert root(lambda X: abs(X+1)+abs(X-2) == X+5) == [Fr(-4, 3), 6]
    assert root(lambda X: abs(X-1)+abs(X+3) == 6) == [-4, 2]
    for X in grid:
        assert (abs(X+1) >= 4) == (X <= -5 or X >= 3)
        assert (abs(3*X+1) < 5) == (-2 < X < Fr(4, 3))
        assert (abs(X-1)+2*abs(X+2) < 9) == (-4 < X < 2)
        assert (2*abs(X)+abs(X-3) <= 6) == (-1 <= X <= 3)
    # 解の個数：区間ごとに厳密に解く（f(x)=|x-1|+|x-3|, 直線 y=a(x-p)）
    def count(A, p):
        S = set()
        # x<1: -2x+4 = A(x-p) → (A+2)x = 4+A p
        if A+2 != 0:
            X = (4+A*p)/(A+2)
            if X < 1: S.add(X)
        # 1<=x<=3: 2 = A(x-p)
        if A != 0:
            X = Fr(2)/A + p
            if 1 <= X <= 3: S.add(X)
        # x>3: 2x-4 = A(x-p) → (2-A)x = 4 - A p
        if A != 2:
            X = (4-A*p)/(2-A)
            if X > 3: S.add(X)
        for X in S:
            assert abs(X-1)+abs(X-3) == A*(X-p)
        return len(S)
    for A in [Fr(k, 16) for k in range(-160, 161)] + [Fr(1, 2), Fr(1), Fr(2), Fr(-2)]:
        n = count(A, Fr(-1))
        exp = 1 if A < -2 else 0 if A < Fr(1, 2) else 1 if A == Fr(1, 2) else 2 if A < 2 else 1
        assert n == exp, (A, n)
        n = count(A, Fr(5))
        exp = 1 if A <= -2 else 2 if A < Fr(-1, 2) else 1 if A == Fr(-1, 2) else 0 if A <= 2 else 1
        assert n == exp, (A, n)
    # 例題の解答の各区間の条件
    for A in [Fr(k, 16) for k in range(-160, 161)]:
        if A != -2:
            assert (((4-A)/(A+2)) < 1) == (A < -2 or A > 1)
        if A > 0:
            assert (1 <= 2/A-1 <= 3) == (Fr(1, 2) <= A <= 1)
        if A != 2:
            assert (((A+4)/(2-A)) > 3) == (Fr(1, 2) < A < 2)
    # ★5 Hlawka：ランダム検証と、各場合の D の式
    rnd = random.Random(1)
    for _ in range(100000):
        A, B, C = [rnd.uniform(-5, 5) for _ in range(3)]
        assert abs(A)+abs(B)+abs(C)+abs(A+B+C) >= abs(A+B)+abs(B+C)+abs(C+A) - 1e-12
        assert abs(A)+abs(B)+abs(C) <= abs(A+B-C)+abs(B+C-A)+abs(C+A-B) + 1e-12
    for A in range(0, 7):
        for B in range(A, 7):
            for Dd in [Fr(k, 4) for k in range(1, 60)]:
                Dv = Dd + abs(A+B-Dd) - abs(A-Dd) - abs(B-Dd)
                LHS = abs(A)+abs(B)+abs(-Dd)+abs(A+B-Dd)
                RHS = abs(A+B)+abs(B-Dd)+abs(A-Dd)
                assert LHS - RHS == Dv
                if Dd <= A: assert Dv == 2*Dd
                elif Dd <= B: assert Dv == 2*A
                elif Dd <= A+B: assert Dv == 2*(A+B-Dd)
                else: assert Dv == 0
    for A, B, C in [(1, 2, -5)]:
        assert abs(A)+abs(B)+abs(C)+abs(A+B+C) == abs(A+B)+abs(B+C)+abs(C+A)


VER.append(_v6)

# ---------------------------------------------------------------- 節7
SEC.append({"title": r"集合",
"base": r"""・$A\cap B$（共通部分），$A\cup B$（和集合），$\overline{A}$（補集合），$A\subset B$（$A$ は $B$ の部分集合），$\varnothing$（空集合）<br>
・ド・モルガンの法則：$\overline{A\cup B}=\overline{A}\cap\overline{B}$，$\overline{A\cap B}=\overline{A}\cup\overline{B}$<br>
・有限集合は要素を書き並べるかベン図で、不等式で表された集合は数直線で考える。端の値を含むか（黒丸・白丸）に注意。<br>
・空集合 $\varnothing$ はすべての集合の部分集合である。""",
"items": [
 {"lv": 1, "title": r"共通部分・和集合・補集合とド・モルガンの法則",
  "q": r"$U=\{1,\ 2,\ 3,\ \cdots,\ 10\}$ を全体集合とし、$10$ の正の約数全体の集合を $A$，$U$ に属する奇数全体の集合を $B$ とする。次の集合を求めよ。<br>(1) $A\cap B$　(2) $A\cup B$　(3) $\overline{A}\cap\overline{B}$　(4) $\overline{A}\cup B$",
  "hint": r"まず $A,\ B$ の要素を書き並べる。(3) はド・モルガンの法則により $\overline{A}\cap\overline{B}=\overline{A\cup B}$ なので、(2) の結果の補集合をとればよい。",
  "sol": r"$A=\{1,\ 2,\ 5,\ 10\}$，$B=\{1,\ 3,\ 5,\ 7,\ 9\}$<br>"
         r"(1) $A\cap B=\boldsymbol{\{1,\ 5\}}$<br>"
         r"(2) $A\cup B=\boldsymbol{\{1,\ 2,\ 3,\ 5,\ 7,\ 9,\ 10\}}$<br>"
         r"(3) $\overline{A}\cap\overline{B}=\overline{A\cup B}=\boldsymbol{\{4,\ 6,\ 8\}}$<br>"
         r"(4) $\overline{A}=\{3,\ 4,\ 6,\ 7,\ 8,\ 9\}$ であるから　$\overline{A}\cup B=\boldsymbol{\{1,\ 3,\ 4,\ 5,\ 6,\ 7,\ 8,\ 9\}}$",
  "note": r"(4) は $\overline{A}\cup B=\overline{A\cap\overline{B}}$ とも書けるので、$A\cap\overline{B}=\{2,\ 10\}$ の補集合として求めてもよい。ベン図をかくと、どの部分が求める集合かが一目で分かる。",
  "ex": r"実数全体を全体集合とし、$A=\{x\mid-1\leqq x<4\}$，$B=\{x\mid x>2\}$ とする。次の集合を求めよ。<br>(1) $A\cap B$　(2) $\overline{A}\cap B$　(3) $\overline{A\cup B}$",
  "exa": r"(1) $\{x\mid2<x<4\}$　(2) $\{x\mid x\geqq4\}$　(3) $\{x\mid x<-1\}$"},
 {"lv": 2, "title": r"条件を満たすように集合の要素を決める",
  "q": r"$a$ を実数とし、$A=\{1,\ 5,\ a^2-1\}$，$B=\{5,\ a+5,\ a^2-2a+4\}$ とする。$A\cap B=\{5,\ 8\}$ となるような $a$ の値を求めよ。また、そのときの $A\cup B$ を求めよ。",
  "hint": r"$8\in A$ であることから $a$ の候補をしぼる（必要条件）。候補ごとに $B$ を具体的に書き、本当に $A\cap B=\{5,\ 8\}$ となるかを確かめる（十分性の確認）。",
  "sol": r"$8\in A\cap B$ より $8\in A$。$1\neq8,\ 5\neq8$ なので $a^2-1=8$，すなわち $a=\pm3$<br>"
         r"[1] $a=3$ のとき　$A=\{1,\ 5,\ 8\}$，$B=\{5,\ 8,\ 7\}$ で、$A\cap B=\{5,\ 8\}$ となり適する。<br>"
         r"[2] $a=-3$ のとき　$A=\{1,\ 5,\ 8\}$，$B=\{5,\ 2,\ 19\}$ で、$A\cap B=\{5\}$ となり不適。<br>"
         r"よって　$\boldsymbol{a=3}$，$A\cup B=\boldsymbol{\{1,\ 5,\ 7,\ 8\}}$",
  "note": r"候補を出した後で元の条件に戻して確かめないと、不適な $a=-3$ を答えに含めてしまう。「必要条件で候補を絞り、十分性を確かめる」は、この先の多くの問題で使う考え方である。",
  "ex": r"$a$ を実数とし、$A=\{2,\ 3,\ a^2+a\}$，$B=\{3,\ a+4,\ a^2+1\}$ とする。$A\cap B=\{3,\ 6\}$ となるような $a$ の値と、そのときの $A\cup B$ を求めよ。",
  "exa": r"$a=2$，$A\cup B=\{2,\ 3,\ 5,\ 6\}$"},
 {"lv": 3, "title": r"不等式で表された集合の包含関係（空集合に注意）",
  "q": r"実数全体を全体集合とし、$A=\{x\mid|x-1|<3\}$，$B=\{x\mid a-1\leqq x\leqq2a+1\}$ とする（$a$ は定数）。<br>(1) $B\subset A$ となるような $a$ の値の範囲を求めよ。<br>(2) $A\cap B=\varnothing$ となるような $a$ の値の範囲を求めよ。",
  "hint": r"$A=\{x\mid-2<x<4\}$。$B$ は $a-1>2a+1$，すなわち $a<-2$ のとき空集合になる。空集合はどんな集合の部分集合でもあり、どんな集合とも共通部分をもたない。$B\neq\varnothing$ のときは数直線で端点の位置を比べる。",
  "sol": r"$|x-1|<3$ より $-2<x<4$ なので、$A=\{x\mid-2<x<4\}$<br>"
         r"$a-1>2a+1$，すなわち $a<-2$ のとき $B=\varnothing$，$a\geqq-2$ のとき $B\neq\varnothing$ である。<br>"
         r"(1) $a<-2$ のとき、$B=\varnothing$ なので $B\subset A$ が成り立つ。<br>"
         r"$a\geqq-2$ のとき、$B\subset A$ となる条件は $-2<a-1$ かつ $2a+1<4$，すなわち $-1<a<\dfrac32$。これは $a\geqq-2$ を満たす。<br>"
         r"よって　$\boldsymbol{a<-2,\ -1<a<\dfrac32}$<br>"
         r"(2) $a<-2$ のとき、$B=\varnothing$ なので $A\cap B=\varnothing$。<br>"
         r"$a\geqq-2$ のとき、$A\cap B=\varnothing$ となる条件は $2a+1\leqq-2$ または $4\leqq a-1$，すなわち $a\leqq-\dfrac32$ または $a\geqq5$。$a\geqq-2$ と合わせて $-2\leqq a\leqq-\dfrac32,\ 5\leqq a$。<br>"
         r"よって　$\boldsymbol{a\leqq-\dfrac32,\ 5\leqq a}$",
  "note": r"$B=\varnothing$ の場合を見落とすと、(1) の答えが $-1<a<\dfrac32$ だけになってしまう。端点の等号は、$A$ の端が「含まない」（白丸）、$B$ の端が「含む」（黒丸）ことから判断する。例えば $a=-\dfrac32$ のとき $B=\left\{x\ \middle|\ -\dfrac52\leqq x\leqq-2\right\}$ で、$x=-2$ は $A$ に属さないので $A\cap B=\varnothing$ となる。",
  "ex": r"実数全体を全体集合とし、$A=\{x\mid|x+1|\leqq2\}$，$B=\{x\mid2a<x<a+2\}$ とする（$a$ は定数）。(1) $B\subset A$ となるような $a$ の値の範囲を求めよ。(2) $A\cap B=\varnothing$ となるような $a$ の値の範囲を求めよ。",
  "exa": r"(1) $-\dfrac32\leqq a\leqq-1,\ 2\leqq a$　(2) $a\leqq-5,\ \dfrac12\leqq a$"},
]})


def _v7():
    U = set(range(1, 11))
    A = {n for n in U if 10 % n == 0}
    B = {n for n in U if n % 2 == 1}
    assert A == {1, 2, 5, 10} and B == {1, 3, 5, 7, 9}
    assert A & B == {1, 5} and A | B == {1, 2, 3, 5, 7, 9, 10}
    assert (U-A) & (U-B) == U-(A | B) == {4, 6, 8}
    assert (U-A) | B == {1, 3, 4, 5, 6, 7, 8, 9} == U-(A & (U-B)) and A & (U-B) == {2, 10}
    grid = [Fr(k, 32) for k in range(-640, 641)]
    for X in grid:
        inA, inB = -1 <= X < 4, X > 2
        assert (inA and inB) == (2 < X < 4)
        assert ((not inA) and inB) == (X >= 4)
        assert (not (inA or inB)) == (X < -1)
    # 要素の決定
    sols = []
    for k in range(-50, 51):
        A_ = {1, 5, k*k-1}; B_ = {5, k+5, k*k-2*k+4}
        if A_ & B_ == {5, 8}: sols.append((k, A_ | B_))
    assert sols == [(3, {1, 5, 7, 8})]
    assert {5, -3+5, 9+6+4} == {5, 2, 19}
    sols = []
    for k in range(-50, 51):
        A_ = {2, 3, k*k+k}; B_ = {3, k+4, k*k+1}
        if A_ & B_ == {3, 6}: sols.append((k, A_ | B_))
    assert sols == [(2, {2, 3, 5, 6})]
    # 実数解の候補（a^2-1=8, a^2+a=6）以外に解がないこと：方程式の解は ±3, 2,-3 のみ
    from sympy import solve
    assert sorted(solve(a**2-1-8, a)) == [-3, 3] and sorted(solve(a**2+a-6, a)) == [-3, 2]
    # 包含関係：区間の端点は 1/8 刻み → x を 1/32 刻みで調べる
    def test(A, Bfun, aset):
        sub, emp = [], []
        for a_ in aset:
            inB = [X for X in grid if Bfun(X, a_)]
            if all(A(X) for X in inB): sub.append(a_)
            if not any(A(X) for X in inB): emp.append(a_)
        return sub, emp
    aset = [Fr(k, 8) for k in range(-64, 65)]
    sub, emp = test(lambda X: abs(X-1) < 3, lambda X, a_: a_-1 <= X <= 2*a_+1, aset)
    assert sub == [a_ for a_ in aset if a_ < -2 or -1 < a_ < Fr(3, 2)]
    assert emp == [a_ for a_ in aset if a_ <= Fr(-3, 2) or a_ >= 5]
    sub, emp = test(lambda X: abs(X+1) <= 2, lambda X, a_: 2*a_ < X < a_+2, aset)
    assert sub == [a_ for a_ in aset if Fr(-3, 2) <= a_ <= -1 or a_ >= 2]
    assert emp == [a_ for a_ in aset if a_ <= -5 or a_ >= Fr(1, 2)]


VER.append(_v7)

# ---------------------------------------------------------------- 節8
SEC.append({"title": r"命題と論証",
"base": r"""・命題「$p\Longrightarrow q$」が真のとき、$q$ は $p$ であるための<b>必要条件</b>、$p$ は $q$ であるための<b>十分条件</b>。$p\Longleftrightarrow q$ のとき<b>必要十分条件</b>（同値）。<br>
・条件 $p,\ q$ を満たすものの集合を $P,\ Q$ とすると　「$p\Longrightarrow q$ が真」$\iff P\subset Q$。偽を示すには反例を1つあげる。<br>
・否定：「$p$ かつ $q$」の否定は「$\overline{p}$ または $\overline{q}$」、「すべての $x$ について $p$」の否定は「ある $x$ について $\overline{p}$」（「または」「ある」も同様に入れかわる）。<br>
・対偶「$\overline{q}\Longrightarrow\overline{p}$」の真偽はもとの命題と一致する。背理法：結論を否定して矛盾を導く。""",
"items": [
 {"lv": 1, "title": r"必要条件・十分条件の判定",
  "q": r"$x,\ y$ は実数とする。次の（　）に、「必要条件であるが十分条件ではない」「十分条件であるが必要条件ではない」「必要十分条件である」「必要条件でも十分条件でもない」のうち、最も適するものを入れよ。<br>"
       r"(1) $x=2$ は $x^2=4$ であるための（　）。<br>"
       r"(2) $xy>0$ は「$x>0$ かつ $y>0$」であるための（　）。<br>"
       r"(3) $x^2+y^2=0$ は「$x=0$ かつ $y=0$」であるための（　）。<br>"
       r"(4) $|x|<1$ は $x<1$ であるための（　）。",
  "hint": r"「$p\Longrightarrow q$」と「$q\Longrightarrow p$」の真偽をそれぞれ調べる。偽であることは反例を1つあげて示す。",
  "sol": r"(1) 「$x=2\Longrightarrow x^2=4$」は真。「$x^2=4\Longrightarrow x=2$」は偽（反例 $x=-2$）。<br>よって　<b>十分条件であるが必要条件ではない</b><br>"
         r"(2) 「$xy>0$ ならば $x>0$ かつ $y>0$」は偽（反例 $x=y=-1$）。「$x>0$ かつ $y>0$ ならば $xy>0$」は真。<br>よって　<b>必要条件であるが十分条件ではない</b><br>"
         r"(3) $x^2\geqq0,\ y^2\geqq0$ であるから、$x^2+y^2=0$ となるのは $x^2=y^2=0$ のとき、すなわち $x=y=0$ のときに限る。逆も成り立つ。<br>よって　<b>必要十分条件である</b><br>"
         r"(4) 「$|x|<1\Longrightarrow x<1$」は真（$|x|<1$ は $-1<x<1$）。「$x<1\Longrightarrow|x|<1$」は偽（反例 $x=-2$）。<br>よって　<b>十分条件であるが必要条件ではない</b>",
  "note": r"集合で考えると見通しがよい。(4) は $P=\{x\mid-1<x<1\}$，$Q=\{x\mid x<1\}$ として $P\subset Q$ かつ $P\neq Q$ なので、$p$ は $q$ の十分条件であるが必要条件ではない。「小さい集合（狭い条件）は十分条件、大きい集合（広い条件）は必要条件」と覚えるとよい。",
  "ex": r"$x$ は実数、$n$ は自然数とする。（　）に例題と同じ4つのうち最も適するものを入れよ。<br>(1) $x^2=x$ は $x=1$ であるための（　）。<br>(2) $n$ が $6$ の倍数であることは、$n$ が $3$ の倍数であるための（　）。<br>(3) $x>2$ は $x^2>4$ であるための（　）。",
  "exa": r"(1) 必要条件であるが十分条件ではない　(2) 十分条件であるが必要条件ではない　(3) 十分条件であるが必要条件ではない"},
 {"lv": 2, "title": r"「すべて」「ある」を含む命題の否定",
  "q": r"(1)〜(3) の命題の否定を述べ、もとの命題とその否定の真偽をそれぞれ答えよ。また、(4) の条件の否定を述べよ。<br>"
       r"(1) すべての実数 $x$ について $x^2+1>2x$<br>"
       r"(2) ある自然数 $n$ について $n^2=2n+8$<br>"
       r"(3) すべての実数 $x$ に対して、ある実数 $y$ が存在して $x+y=0$<br>"
       r"(4) $x\geqq1$ かつ $y<2$　（$x,\ y$ は実数）",
  "hint": r"「すべての $x$ について $p$」の否定は「ある $x$ について $\overline{p}$」、「ある $x$ について $p$」の否定は「すべての $x$ について $\overline{p}$」。(3) のように重なっているときは、外側から順に「すべて」と「ある」を入れかえる。「かつ」と「または」は否定で入れかわる。",
  "sol": r"(1) 否定：「ある実数 $x$ について $x^2+1\leqq2x$」<br>"
         r"$x^2+1-2x=(x-1)^2$ は $x=1$ のとき $0$ になるので、$x=1$ では $x^2+1>2x$ が成り立たない。よって もとの命題は<b>偽</b>、否定は<b>真</b>。<br>"
         r"(2) 否定：「すべての自然数 $n$ について $n^2\neq2n+8$」<br>"
         r"$n=4$ のとき $n^2=16=2n+8$ であるから、もとの命題は<b>真</b>、否定は<b>偽</b>。<br>"
         r"(3) 否定：「ある実数 $x$ が存在して、すべての実数 $y$ について $x+y\neq0$」<br>"
         r"どんな実数 $x$ に対しても $y=-x$ とすれば $x+y=0$ となるから、もとの命題は<b>真</b>、否定は<b>偽</b>。<br>"
         r"(4) 否定：「$\boldsymbol{x<1}$ <b>または</b> $\boldsymbol{y\geqq2}$」",
  "note": r"否定の真偽は、もとの命題の真偽のちょうど逆になる。「すべて」の命題が偽であることは反例を1つ、「ある」の命題が真であることは例を1つあげれば示せる。(3) の $x$ と $y$ の順序を入れかえた「ある実数 $y$ が存在して、すべての実数 $x$ について $x+y=0$」は偽であり、意味がまったく違う。",
  "ex": r"次の命題の否定を述べ、もとの命題の真偽を答えよ。<br>(1) すべての実数 $x$ について $|x|\geqq x$<br>(2) ある整数 $n$ について $n^2+n$ は奇数<br>(3) ある実数 $x$ が存在して、すべての実数 $y$ について $xy=0$",
  "exa": r"(1) 否定「ある実数 $x$ について $|x|<x$」，もとの命題は真　(2) 否定「すべての整数 $n$ について $n^2+n$ は偶数」，もとの命題は偽　(3) 否定「すべての実数 $x$ に対して、ある実数 $y$ が存在して $xy\neq0$」，もとの命題は真（$x=0$）"},
 {"lv": 3, "title": r"対偶を利用した証明",
  "q": r"次の命題を証明せよ。<br>(1) 整数 $n$ について、$n^2$ が $3$ の倍数ならば、$n$ は $3$ の倍数である。<br>(2) 実数 $x,\ y$ について、$x+y>2$ ならば、$x>1$ または $y>1$ である。",
  "hint": r"結論が「$3$ の倍数である」「$x>1$ または $y>1$」のように直接示しにくいときは、対偶を考える。対偶の仮定は「$n=3k+1$ または $3k+2$」「$x\leqq1$ かつ $y\leqq1$」となり、扱いやすい。",
  "sol": r"(1) 対偶「$n$ が $3$ の倍数でないならば、$n^2$ は $3$ の倍数でない」を示す。<br>"
         r"$n$ が $3$ の倍数でないとき、整数 $k$ を用いて $n=3k+1$ または $n=3k+2$ と表せる。<br>"
         r"$n=3k+1$ のとき　$n^2=9k^2+6k+1=3(3k^2+2k)+1$<br>"
         r"$n=3k+2$ のとき　$n^2=9k^2+12k+4=3(3k^2+4k+1)+1$<br>"
         r"いずれの場合も $n^2$ を $3$ で割った余りは $1$ で、$n^2$ は $3$ の倍数でない。対偶が真であるから、もとの命題も真である。　■<br>"
         r"(2) 対偶「$x\leqq1$ かつ $y\leqq1$ ならば $x+y\leqq2$」を示す。$x\leqq1$，$y\leqq1$ の辺々を加えると $x+y\leqq2$ となるから、対偶は真。よって、もとの命題も真である。　■",
  "note": r"(1) の結果は、次の例題で $\sqrt3$ が無理数であることを示すときに使う。対偶法は「結論が否定の形」「結論が『または』を含む」ときに特に有効である。",
  "ex": r"次の命題を証明せよ。<br>(1) 整数 $n$ について、$n^2$ が $5$ の倍数ならば、$n$ は $5$ の倍数である。<br>(2) 実数 $x,\ y$ について、$x^2+y^2<2$ ならば、$x<1$ または $y<1$ である。",
  "exa": r"(1) 対偶：$n=5k\pm1,\ 5k\pm2$ のとき $n^2=5(5k^2\pm2k)+1,\ 5(5k^2\pm4k)+4$ で $5$ の倍数でない　(2) 対偶：$x\geqq1$ かつ $y\geqq1$ ならば $x^2\geqq1,\ y^2\geqq1$ より $x^2+y^2\geqq2$"},
 {"lv": 3, "title": r"背理法による無理数の証明",
  "q": r"(1) $\sqrt3$ が無理数であることを証明せよ。<br>(2) $\sqrt2+\sqrt3$ が無理数であることを証明せよ。ただし、$\sqrt6$ が無理数であることは用いてよい。",
  "hint": r"「無理数である」とは「有理数でない」という否定の形の主張なので、直接は示しにくい。有理数であると仮定して矛盾を導く（背理法）。(1) では前の例題 (1) の結果を使う。",
  "sol": r"(1) $\sqrt3$ が有理数であると仮定すると、互いに素な自然数 $m,\ n$ を用いて $\sqrt3=\dfrac mn$ と表せる。<br>"
         r"このとき $m^2=3n^2$ より $m^2$ は $3$ の倍数であるから、前の例題 (1) より $m$ は $3$ の倍数である。$m=3k$（$k$ は自然数）とおくと $9k^2=3n^2$，すなわち $n^2=3k^2$ となり、同様に $n$ も $3$ の倍数である。<br>"
         r"これは $m,\ n$ が互いに素であることに矛盾する。よって $\sqrt3$ は無理数である。　■<br>"
         r"(2) $\sqrt2+\sqrt3$ が有理数であると仮定し、$\sqrt2+\sqrt3=r$（$r$ は有理数）とおく。<br>"
         r"両辺を2乗して $5+2\sqrt6=r^2$，すなわち $\sqrt6=\dfrac{r^2-5}{2}$<br>"
         r"右辺は有理数であるから、$\sqrt6$ が無理数であることに矛盾する。よって $\sqrt2+\sqrt3$ は無理数である。　■",
  "note": r"(2) は $\sqrt3=r-\sqrt2$ と変形して2乗すると $3=r^2-2\sqrt2r+2$ より $\sqrt2=\dfrac{r^2-1}{2r}$（$r>0$ なので割ってよい）となり、$\sqrt2$ が無理数であることだけを使って示すこともできる。有理数どうしの和・差・積・商（$0$ で割る場合を除く）は有理数である、という事実が背理法の矛盾を生む。",
  "ex": r"(1) $\sqrt5$ が無理数であることを証明せよ。ただし、整数 $n$ について $n^2$ が $5$ の倍数ならば $n$ は $5$ の倍数であることは用いてよい。<br>(2) $\sqrt5-\sqrt2$ が無理数であることを証明せよ。ただし、$\sqrt{10}$ が無理数であることは用いてよい。",
  "exa": r"(1) $\sqrt5=\dfrac mn$（$m,\ n$ は互いに素な自然数）とおくと $m^2=5n^2$ から $m,\ n$ がともに $5$ の倍数となり矛盾　(2) $\sqrt5-\sqrt2=r$（有理数）とすると、2乗して $\sqrt{10}=\dfrac{7-r^2}{2}$ が有理数となり矛盾"},
 {"lv": 4, "title": r"背理法：3数がすべて正であることの証明",
  "q": r"実数 $a,\ b,\ c$ が $a+b+c>0$，$ab+bc+ca>0$，$abc>0$ を満たすならば、$a,\ b,\ c$ はすべて正であることを証明せよ。",
  "hint": r"「すべて正」の否定は「少なくとも1つは $0$ 以下」。$abc>0$ から $0$ になるものはなく、負の数は偶数個、すなわちちょうど2個に限られる。文字の対称性から $b<0,\ c<0$ として矛盾を導く。",
  "sol": r"$a,\ b,\ c$ のうち少なくとも1つが $0$ 以下であると仮定する。<br>"
         r"$abc>0$ より、$a,\ b,\ c$ はどれも $0$ ではないので、少なくとも1つは負である。積 $abc$ が正であるから負の数は偶数個で、ちょうど2個である。条件はどれも $a,\ b,\ c$ について対称であるから、$a>0,\ b<0,\ c<0$ としてよい。<br>"
         r"$a+b+c>0$ より $a>-(b+c)$。ここで $b+c<0$ であるから、両辺に $b+c$ を掛けると不等号の向きが変わり　$a(b+c)<-(b+c)^2$<br>"
         r"よって　$ab+bc+ca=a(b+c)+bc<-(b+c)^2+bc=-(b^2+bc+c^2)$<br>"
         r"$b^2+bc+c^2=\left(b+\dfrac c2\right)^2+\dfrac34c^2>0$（$c\neq0$）であるから、$ab+bc+ca<0$ となり、$ab+bc+ca>0$ に矛盾する。<br>"
         r"したがって、$a,\ b,\ c$ はすべて正である。　■",
  "note": r"逆（$a,\ b,\ c>0$ ならば3つの式はすべて正）は明らかなので、「$a,\ b,\ c$ がすべて正 $\iff$ $a+b+c>0,\ ab+bc+ca>0,\ abc>0$」が成り立つ。$a,\ b,\ c$ を解とする3次方程式の係数の符号から、解がすべて正であることを判定するときに使われる。",
  "ex": r"正の実数 $a,\ b,\ c$ に対し、$a(1-b),\ b(1-c),\ c(1-a)$ のうち少なくとも1つは $\dfrac14$ 以下であることを証明せよ。",
  "exa": r"3つとも $\dfrac14$ より大きいと仮定すると $0<a,\ b,\ c<1$ で、3式の積から $a(1-a)\cdot b(1-b)\cdot c(1-c)>\dfrac1{64}$。一方 $x(1-x)=\dfrac14-\left(x-\dfrac12\right)^2\leqq\dfrac14$ より左辺は $\dfrac1{64}$ 以下で矛盾"},
 {"lv": 5, "title": r"$1,\ \sqrt2,\ \sqrt3,\ \sqrt6$ の1次独立性",
  "q": r"$\sqrt2,\ \sqrt3,\ \sqrt6$ が無理数であることは用いてよい。<br>"
       r"(1) 有理数 $p,\ q,\ r$ が $p+q\sqrt2=r\sqrt3$ を満たすならば、$p=q=r=0$ であることを示せ。<br>"
       r"(2) 有理数 $a,\ b,\ c,\ d$ が $a+b\sqrt2+c\sqrt3+d\sqrt6=0$ を満たすならば、$a=b=c=d=0$ であることを示せ。<br>"
       r"(3) $\dfrac{1}{1+\sqrt2+\sqrt3}=a+b\sqrt2+c\sqrt3+d\sqrt6$ を満たす有理数 $a,\ b,\ c,\ d$ をすべて求めよ。",
  "hint": r"(1) 両辺を2乗すると $\sqrt2$ の係数 $2pq$ が現れる。$pq\neq0$ なら $\sqrt2$ が有理数になってしまうので $pq=0$。あとは $p=0$，$q=0$ で場合分け。(2) $(a+b\sqrt2)+(c+d\sqrt2)\sqrt3=0$ とみて、$c+d\sqrt2\neq0$ なら $\sqrt3=P+Q\sqrt2$（$P,\ Q$ は有理数）の形になり (1) に矛盾。(3) は (2) から「表し方がただ1通り」であることが分かる。",
  "sol": r"(1) 両辺を2乗して　$p^2+2q^2+2pq\sqrt2=3r^2$<br>"
         r"$pq\neq0$ とすると $\sqrt2=\dfrac{3r^2-p^2-2q^2}{2pq}$ は有理数となり矛盾。よって $pq=0$。<br>"
         r"[1] $q=0$ のとき　$p=r\sqrt3$。$r\neq0$ なら $\sqrt3=\dfrac pr$ が有理数となり矛盾するので $r=0$，したがって $p=0$。<br>"
         r"[2] $p=0$ のとき　$q\sqrt2=r\sqrt3$。$r\neq0$ なら両辺に $\sqrt2$ を掛けて $2q=r\sqrt6$，$\sqrt6=\dfrac{2q}{r}$ が有理数となり矛盾するので $r=0$。すると $q\sqrt2=0$ より $q=0$。<br>"
         r"いずれの場合も $p=q=r=0$ である。　■<br>"
         r"(2) 条件は $(a+b\sqrt2)+(c+d\sqrt2)\sqrt3=0$ ……①　と書ける。<br>"
         r"$c+d\sqrt2\neq0$ と仮定する。このとき $c-d\sqrt2\neq0$ でもある（$d\neq0$ なら $c=d\sqrt2$ は $\sqrt2$ が無理数であることに反し、$d=0$ なら $c\neq0$）。よって $c^2-2d^2=(c+d\sqrt2)(c-d\sqrt2)\neq0$ であり、①から<br>"
         r"$\sqrt3=-\dfrac{a+b\sqrt2}{c+d\sqrt2}=-\dfrac{(a+b\sqrt2)(c-d\sqrt2)}{c^2-2d^2}=P+Q\sqrt2$，　$P=-\dfrac{ac-2bd}{c^2-2d^2}$，$Q=-\dfrac{bc-ad}{c^2-2d^2}$<br>"
         r"$P,\ Q$ は有理数であるから、$P+Q\sqrt2=1\cdot\sqrt3$ に (1) を用いると $1=0$ となり矛盾。<br>"
         r"したがって $c+d\sqrt2=0$，すなわち $c+d\sqrt2=0\cdot\sqrt3$ で、(1) より $c=d=0$。すると①は $a+b\sqrt2=0\cdot\sqrt3$ となり、再び (1) より $a=b=0$。　■<br>"
         r"(3) 分母・分子に $(1+\sqrt2)-\sqrt3$ を掛けると<br>"
         r"$\dfrac{1+\sqrt2-\sqrt3}{(1+\sqrt2)^2-3}=\dfrac{1+\sqrt2-\sqrt3}{2\sqrt2}=\dfrac{2+\sqrt2-\sqrt6}{4}=\dfrac12+\dfrac14\sqrt2+0\cdot\sqrt3-\dfrac14\sqrt6$<br>"
         r"また、有理数 $a,\ b,\ c,\ d$ と $a',\ b',\ c',\ d'$ がともに条件を満たせば、辺々引いて $(a-a')+(b-b')\sqrt2+(c-c')\sqrt3+(d-d')\sqrt6=0$ となり、(2) より $a=a',\ b=b',\ c=c',\ d=d'$。よって表し方はただ1通りで<br>"
         r"$\boldsymbol{a=\dfrac12,\ b=\dfrac14,\ c=0,\ d=-\dfrac14}$",
  "note": r"(2) は「$1,\ \sqrt2,\ \sqrt3,\ \sqrt6$ は有理数の範囲で1次独立である」という主張で、これによって $a+b\sqrt2+c\sqrt3+d\sqrt6$ の形の数について「係数比較」が許される。(1) だけでは $\sqrt3$ の係数が有理数の場合しか扱えないので、(2) では $c+d\sqrt2$ を1つの数とみて有理化し、(1) が使える形に持ち込むのが鍵である。$\sqrt2+\sqrt3+\sqrt6$ が無理数であることなども (2) から直ちに分かる。",
  "ex": r"$\sqrt3,\ \sqrt5,\ \sqrt{15}$ が無理数であることは用いてよい。有理数 $a,\ b,\ c,\ d$ が $a+b\sqrt3+c\sqrt5+d\sqrt{15}=0$ を満たすならば、$a=b=c=d=0$ であることを証明せよ。",
  "exa": r"まず「有理数 $p,\ q,\ r$ が $p+q\sqrt3=r\sqrt5$ ならば $p=q=r=0$」を2乗して示す。次に $c+d\sqrt3\neq0$ なら $\sqrt5=-\dfrac{a+b\sqrt3}{c+d\sqrt3}$ を有理化して $P+Q\sqrt3$（$P,\ Q$ は有理数）の形となり矛盾。よって $c=d=0$，さらに $a=b=0$"},
]})


def _v8():
    grid = [Fr(k, 8) for k in range(-40, 41)]
    imp = lambda P, Q, dom: all(Q(*v) for v in dom if P(*v))
    D1 = [(X,) for X in grid]
    D2 = [(X, Y) for X in grid for Y in grid]
    # (1)
    assert imp(lambda X: X == 2, lambda X: X*X == 4, D1) and not imp(lambda X: X*X == 4, lambda X: X == 2, D1)
    assert imp(lambda X, Y: X > 0 and Y > 0, lambda X, Y: X*Y > 0, D2) and not imp(lambda X, Y: X*Y > 0, lambda X, Y: X > 0 and Y > 0, D2)
    assert all((X*X+Y*Y == 0) == (X == 0 and Y == 0) for X, Y in D2)
    assert imp(lambda X: abs(X) < 1, lambda X: X < 1, D1) and not imp(lambda X: X < 1, lambda X: abs(X) < 1, D1)
    assert imp(lambda X: X == 1, lambda X: X*X == X, D1) and not imp(lambda X: X*X == X, lambda X: X == 1, D1)
    N_ = [(n,) for n in range(1, 200)]
    assert imp(lambda n: n % 6 == 0, lambda n: n % 3 == 0, N_) and not imp(lambda n: n % 3 == 0, lambda n: n % 6 == 0, N_)
    assert imp(lambda X: X > 2, lambda X: X*X > 4, D1) and not imp(lambda X: X*X > 4, lambda X: X > 2, D1)
    # (2) すべて・ある
    assert expand(x**2+1-2*x - (x-1)**2) == 0 and not (1+1 > 2)
    assert [n for n in range(1, 1000) if n*n == 2*n+8] == [4]
    assert all(abs(X) >= X for X in grid) and all((n*n+n) % 2 == 0 for n in range(-500, 500))
    assert all(0*Y == 0 for Y in grid)
    # (3) 対偶
    for k in range(-50, 50):
        assert (3*k+1)**2 == 3*(3*k*k+2*k)+1 and (3*k+2)**2 == 3*(3*k*k+4*k+1)+1
        for s_ in (1, -1):
            assert (5*k+s_)**2 == 5*(5*k*k+2*s_*k)+1 and (5*k+2*s_)**2 == 5*(5*k*k+4*s_*k)+4
    assert all((n*n % 3 == 0) <= (n % 3 == 0) for n in range(-300, 300))
    assert all((n*n % 5 == 0) <= (n % 5 == 0) for n in range(-300, 300))
    rnd = random.Random(2)
    for _ in range(20000):
        X, Y = rnd.uniform(-3, 3), rnd.uniform(-3, 3)
        if X + Y > 2: assert X > 1 or Y > 1
        if X*X + Y*Y < 2: assert X < 1 or Y < 1
    # (4) 背理法
    assert expand((sqrt(2)+sqrt(3))**2) == 5+2*sqrt(6)
    assert expand((sqrt(5)-sqrt(2))**2) == 7-2*sqrt(10)
    r_ = symbols("r")
    assert expand((r_-sqrt(2))**2 - 3) == r_**2-2*sqrt(2)*r_-1
    # (5) 3数の正
    assert expand(a*(b+c)+b*c - (-(b+c)**2+b*c) - (a+b+c)*(b+c)) == 0
    assert expand(-(b+c)**2+b*c + (b**2+b*c+c**2)) == 0
    assert expand(b**2+b*c+c**2 - ((b+c/2)**2 + Rational(3, 4)*c**2)) == 0
    for _ in range(200000):
        A, B, C = rnd.uniform(-3, 3), rnd.uniform(-3, 3), rnd.uniform(-3, 3)
        if A+B+C > 0 and A*B+B*C+C*A > 0 and A*B*C > 0:
            assert A > 0 and B > 0 and C > 0
        A, B, C = rnd.uniform(0, 2), rnd.uniform(0, 2), rnd.uniform(0, 2)
        assert min(A*(1-B), B*(1-C), C*(1-A)) <= 0.25 + 1e-12
    assert expand(x*(1-x) - (Rational(1, 4)-(x-Rational(1, 2))**2)) == 0
    # (6) 1次独立
    p, q, r = symbols("p q r")
    assert expand((p+q*sqrt(2))**2) == p**2+2*q**2+2*p*q*sqrt(2)
    assert expand((a+b*sqrt(2))*(c-d*sqrt(2))) == expand((a*c-2*b*d)+(b*c-a*d)*sqrt(2))
    assert expand((c+d*sqrt(2))*(c-d*sqrt(2))) == c**2-2*d**2
    s2, s3, s6 = sqrt(2), sqrt(3), sqrt(6)
    assert close(1/(1+s2+s3), Rational(1, 2)+s2/4-s6/4)
    vals = {}
    for A in range(-3, 4):
        for B in range(-3, 4):
            for C in range(-3, 4):
                for Dd in range(-3, 4):
                    v = A+B*math.sqrt(2)+C*math.sqrt(3)+Dd*math.sqrt(6)
                    if (A, B, C, Dd) != (0, 0, 0, 0):
                        assert abs(v) > 1e-3
                    w = A+B*math.sqrt(3)+C*math.sqrt(5)+Dd*math.sqrt(15)
                    if (A, B, C, Dd) != (0, 0, 0, 0):
                        assert abs(w) > 1e-3


VER.append(_v8)

CH = {"no": 1, "sections": SEC}


def verify():
    for f in VER:
        f()
    items = [it for s in SEC for it in s["items"]]
    lv = [it["lv"] for it in items]
    cnt = {k: lv.count(k) for k in range(1, 6)}
    assert 37 <= len(items) <= 43, len(items)
    assert 4 <= len(SEC) <= 9
    assert cnt[5] >= 5 and cnt[4] >= 6 and cnt[1] >= 7 and cnt[2] >= 9 and cnt[3] >= 9, cnt
    for s_ in SEC:
        assert s_["title"] and s_["base"] and s_["items"]
        for it in s_["items"]:
            for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
                assert it.get(k) not in (None, ""), (it["title"], k)
            assert all("$$" not in t_ for t_ in (it["q"], it["sol"], it["hint"], it.get("note", ""), it["ex"], it["exa"])), it["title"]
            assert all(t_.count("$") % 2 == 0 for t_ in (it["q"], it["sol"], it["hint"], it.get("note", ""), it["ex"], it["exa"], it["title"]))
    print("例題数", len(items), cnt)
