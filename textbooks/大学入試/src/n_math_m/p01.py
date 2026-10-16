"""問題集 第1章 数と式。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {1: {
"goal": "展開・因数分解を速く正確に。対称式・二重根号・絶対値の処理を自在に。",
"items": [
 {"lv": "A", "q": r"次の式を因数分解せよ。(1) $x^3-27$　(2) $x^2-y^2+4y-4$　(3) $6x^2+7x-3$",
  "a": r"(1) $(x-3)(x^2+3x+9)$　(2) $(x+y-2)(x-y+2)$　(3) $(2x+3)(3x-1)$",
  "s": r"(1) $a^3-b^3=(a-b)(a^2+ab+b^2)$。(2) $x^2-(y^2-4y+4)=x^2-(y-2)^2$ と平方の差にする。(3) たすきがけ：$2\times3$ と $3\times(-1)$ の組で $2\cdot(-1)+3\cdot3=7$。"},
 {"lv": "A", "q": r"$x=\sqrt5+\sqrt3,\ y=\sqrt5-\sqrt3$ のとき、$x^2+y^2$、$\dfrac yx+\dfrac xy$ の値を求めよ。",
  "a": r"$x^2+y^2=16$、$\frac yx+\frac xy=8$",
  "s": r"$x+y=2\sqrt5,\ xy=5-3=2$。$x^2+y^2=(x+y)^2-2xy=20-4=16$。$\frac yx+\frac xy=\frac{x^2+y^2}{xy}=\frac{16}{2}=8$。"},
 {"lv": "A", "q": r"$\sqrt{8+2\sqrt{15}}$、$\sqrt{6-\sqrt{32}}$ をそれぞれ簡単にせよ。",
  "a": r"$\sqrt5+\sqrt3$、$2-\sqrt2$",
  "s": r"$8=5+3,\ 15=5\times3$ より $\sqrt5+\sqrt3$。$\sqrt{32}=2\sqrt8$ なので $6=4+2,\ 8=4\times2$ より $\sqrt4-\sqrt2=2-\sqrt2$。"},
 {"lv": "A", "q": r"不等式 $|3x-2|\leqq 7$ を解け。",
  "a": r"$-\frac53\leqq x\leqq3$",
  "s": r"$-7\leqq3x-2\leqq7$ より $-5\leqq3x\leqq9$。"},
 {"lv": "B", "q": r"$(x+1)(x+2)(x+3)(x+4)-24$ を因数分解せよ。",
  "a": r"$x(x+5)(x^2+5x+10)$",
  "s": r"組み合わせを工夫：$(x+1)(x+4)=x^2+5x+4$、$(x+2)(x+3)=x^2+5x+6$。$t=x^2+5x$ とおくと $(t+4)(t+6)-24=t^2+10t=t(t+10)$。よって $(x^2+5x)(x^2+5x+10)=x(x+5)(x^2+5x+10)$。<br><b>ポイント</b>：4つの1次式の積は、定数項の和が等しくなるペアを作ると共通部分が現れる。"},
 {"lv": "B", "q": r"$\dfrac{1}{2-\sqrt3}$ の整数部分を $a$、小数部分を $b$ とするとき、$a,\ b$ の値と $b^2+2b$ の値を求めよ。",
  "a": r"$a=3,\ b=\sqrt3-1,\ b^2+2b=2$",
  "s": r"$\frac{1}{2-\sqrt3}=\frac{2+\sqrt3}{(2-\sqrt3)(2+\sqrt3)}=2+\sqrt3$。$1\lt\sqrt3\lt2$ より $3\lt2+\sqrt3\lt4$ なので $a=3$、$b=(2+\sqrt3)-3=\sqrt3-1$。$b^2+2b=b(b+2)=(\sqrt3-1)(\sqrt3+1)=2$。<br><b>ポイント</b>：小数部分は式のまま扱い、因数分解して和と差の積を作ると計算が楽。"},
 {"lv": "B", "q": r"方程式 $|x+1|+|x-2|=x+5$ を解け。",
  "a": r"$x=-\frac43,\ 6$",
  "s": r"境目は $x=-1,2$。$x\lt-1$：$-(x+1)-(x-2)=-2x+1=x+5$ より $x=-\frac43$（$\lt-1$ で適）。$-1\leqq x\lt2$：$3=x+5$ より $x=-2$（範囲外で不適）。$x\geqq2$：$2x-1=x+5$ より $x=6$（適）。"},
 {"lv": "B", "q": r"$a$ を定数とする。不等式 $ax-2\gt x+a$ を解け。",
  "a": r"$a\gt1$：$x\gt\frac{a+2}{a-1}$、$a\lt1$：$x\lt\frac{a+2}{a-1}$、$a=1$：解なし",
  "s": r"$(a-1)x\gt a+2$。$a-1$ の符号で場合分け。$a=1$ のとき $0\gt3$ となり成り立たないので解なし。"},
 {"lv": "C", "q": r"$a+b+c=0$ のとき、$a^3+b^3+c^3=3abc$ を証明せよ。また、これを用いて $(x-y)^3+(y-z)^3+(z-x)^3$ を因数分解せよ。",
  "a": r"$3(x-y)(y-z)(z-x)$",
  "s": r"$a^3+b^3+c^3-3abc=(a+b+c)(a^2+b^2+c^2-ab-bc-ca)$ で、$a+b+c=0$ なら右辺 $=0$。■ 後半：$a=x-y,\ b=y-z,\ c=z-x$ とおくと $a+b+c=0$ なので、求める式 $=3(x-y)(y-z)(z-x)$。"},
 {"lv": "C", "q": r"$\sqrt3$ が無理数であることを証明せよ。また、有理数 $p,q$ が $(2+\sqrt3)p+(1-\sqrt3)q=5+\sqrt3$ を満たすとき、$p,q$ を求めよ。",
  "a": r"$p=2,\ q=1$",
  "s": r"$\sqrt3=\frac mn$（$m,n$ は互いに素な自然数）と仮定すると $m^2=3n^2$。$m^2$ が3の倍数なので $m$ も3の倍数（3の倍数でない整数の2乗は3で割って1余る）。$m=3k$ とおくと $n^2=3k^2$ となり $n$ も3の倍数。$m,n$ が互いに素であることに矛盾するので、$\sqrt3$ は無理数。■<br>後半：整理すると $(2p+q-5)+(p-q-1)\sqrt3=0$。もし $p-q-1\neq0$ なら $\sqrt3=-\frac{2p+q-5}{p-q-1}$ は有理数となり矛盾。よって $p-q-1=0$、さらに $2p+q-5=0$。連立して $p=2,\ q=1$。<br><b>ポイント</b>：「有理数 $a,b$ と無理数 $\sqrt3$ で $a+b\sqrt3=0\Rightarrow a=b=0$」は、理由を一言添えて使う。"},
]}}

def verify():
    x, y, z = symbols("x y z")
    assert expand((x-3)*(x**2+3*x+9) - (x**3-27)) == 0
    assert expand((x+y-2)*(x-y+2) - (x**2-y**2+4*y-4)) == 0
    assert expand((2*x+3)*(3*x-1) - (6*x**2+7*x-3)) == 0
    X, Y = sqrt(5)+sqrt(3), sqrt(5)-sqrt(3)
    assert simplify(X**2+Y**2-16) == 0 and simplify(Y/X+X/Y-8) == 0
    assert simplify(sqrt(8+2*sqrt(15)) - (sqrt(5)+sqrt(3))) == 0
    assert simplify(sqrt(6-sqrt(32)) - (2-sqrt(2))) == 0
    assert expand((x+1)*(x+2)*(x+3)*(x+4)-24 - x*(x+5)*(x**2+5*x+10)) == 0
    assert expand((x-y)**3+(y-z)**3+(z-x)**3 - 3*(x-y)*(y-z)*(z-x)) == 0
    b = sqrt(3)-1
    assert simplify(1/(2-sqrt(3)) - (3+b)) == 0 and simplify(b**2+2*b-2) == 0
    p, q = 2, 1
    assert simplify((2+sqrt(3))*p+(1-sqrt(3))*q-(5+sqrt(3))) == 0
    for v in [Rational(-4, 3), 6]:
        assert abs(v+1)+abs(v-2) == v+5
