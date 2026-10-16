"""問題集 第9章 式と証明。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *
from math import comb

CH = {9: {
"goal": "二項定理・整式の割り算・剰余の定理・恒等式を道具として使いこなす。不等式の証明では「差をとって平方の和」「相加平均と相乗平均」「コーシー・シュワルツ」を使い分け、等号成立条件まで書く。",
"items": [
 {"lv": "A", "q": r"$\left(2x-\dfrac1x\right)^6$ の展開式における定数項と、$x^2$ の係数を求めよ。",
  "a": r"定数項 $-160$、$x^2$ の係数 $240$",
  "s": r"一般項は ${}_6\mathrm{C}_k(2x)^{6-k}\left(-\frac1x\right)^k={}_6\mathrm{C}_k\,2^{6-k}(-1)^kx^{6-2k}$。<br>定数項：$6-2k=0$ より $k=3$。${}_6\mathrm{C}_3\cdot2^3\cdot(-1)^3=20\cdot8\cdot(-1)=-160$。<br>$x^2$：$6-2k=2$ より $k=2$。${}_6\mathrm{C}_2\cdot2^4=15\cdot16=240$。<br><b>ポイント</b>：一般項を $x$ の指数でまとめてから、指数の条件で $k$ を決める。符号 $(-1)^k$ を忘れない。"},
 {"lv": "A", "q": r"(1) $2x^3-3x^2+4x-5$ を $x^2-x+2$ で割った商と余りを求めよ。<br>(2) $x^3+ax^2+bx-6$ が $x^2-x-2$ で割り切れるとき、定数 $a,\ b$ の値を求めよ。",
  "a": r"(1) 商 $2x-1$、余り $-x-3$　(2) $a=2,\ b=-5$",
  "s": r"(1) $2x^3-3x^2+4x-5=(x^2-x+2)(2x-1)+(-x-3)$。（$(x^2-x+2)(2x-1)=2x^3-3x^2+5x-2$ を引くと $-x-3$。）<br>(2) $x^2-x-2=(x-2)(x+1)$ なので、$P(x)=x^3+ax^2+bx-6$ について $P(2)=0,\ P(-1)=0$。$8+4a+2b-6=0$、$-1+a-b-6=0$ より $2a+b=-1,\ a-b=7$、$a=2,\ b=-5$。このとき $P(x)=(x-2)(x+1)(x+3)$。<br><b>ポイント</b>：割る式が因数分解できれば、因数定理で条件を立てるのが速い。"},
 {"lv": "A", "q": r"(1) 等式 $x^3=a(x-1)^3+b(x-1)^2+c(x-1)+d$ が $x$ についての恒等式となるように、定数 $a,\ b,\ c,\ d$ の値を定めよ。<br>(2) 等式 $\dfrac{1}{x(x+2)}=\dfrac ax+\dfrac{b}{x+2}$ が恒等式となるように、定数 $a,\ b$ の値を定めよ。",
  "a": r"(1) $a=1,\ b=3,\ c=3,\ d=1$　(2) $a=\frac12,\ b=-\frac12$",
  "s": r"(1) $t=x-1$ とおくと $x^3=(t+1)^3=t^3+3t^2+3t+1$ なので $a=1,\ b=3,\ c=3,\ d=1$。<br>(2) 分母を払って $1=a(x+2)+bx=(a+b)x+2a$。係数を比較して $a+b=0,\ 2a=1$、$a=\frac12,\ b=-\frac12$。<br><b>ポイント</b>：$(x-1)$ のべきで表すときは $x-1=t$ とおき換える。分数式は分母を払ってから係数比較（または数値代入）。"},
 {"lv": "A", "q": r"(1) $x>0$ のとき、$x+\dfrac9x$ の最小値を求めよ。<br>(2) $x>0,\ y>0$ のとき、$\left(x+\dfrac1y\right)\left(y+\dfrac4x\right)$ の最小値を求めよ。",
  "a": r"(1) $6$（$x=3$）　(2) $9$（$xy=2$）",
  "s": r"(1) 相加平均と相乗平均の関係より $x+\frac9x\geqq2\sqrt{x\cdot\frac9x}=6$。等号は $x=\frac9x$、$x=3$ のとき。<br>(2) 展開して $xy+4+1+\frac4{xy}=xy+\frac4{xy}+5\geqq2\sqrt4+5=9$。等号は $xy=\frac{4}{xy}$、$xy=2$ のとき。<br><b>ポイント</b>：(2) で $x+\frac1y\geqq2\sqrt{\frac xy}$ と $y+\frac4x\geqq2\sqrt{\frac{4y}x}$ を掛けて「最小値 $8$」とするのは誤り（2つの等号が同時には成り立たないので、$8$ にはならない）。展開してから使う。"},
 {"lv": "B", "tag": "剰余の定理", "q": r"整式 $P(x)$ を $x-1$ で割ると余りは $3$、$x+2$ で割ると余りは $-3$ である。<br>(1) $P(x)$ を $(x-1)(x+2)$ で割った余りを求めよ。<br>(2) さらに $P(x)$ を $(x-1)^2$ で割った余りが $x+2$ であるとき、$P(x)$ を $(x-1)^2(x+2)$ で割った余りを求めよ。",
  "a": r"(1) $2x+1$　(2) $-\frac13x^2+\frac53x+\frac53$",
  "s": r"(1) $P(x)=(x-1)(x+2)Q(x)+ax+b$ とおく。$P(1)=a+b=3$、$P(-2)=-2a+b=-3$ より $a=2,\ b=1$。<br>(2) 余りは2次以下で、$(x-1)^2$ で割った余りが $x+2$ になるから $P(x)=(x-1)^2(x+2)R(x)+k(x-1)^2+x+2$ とおける。$P(-2)=9k+0=-3$ より $k=-\frac13$。余りは $-\frac13(x-1)^2+x+2=-\frac13x^2+\frac53x+\frac53$。<br><b>ポイント</b>：3次式で割った余りは、重なっている因数 $(x-1)^2$ で割った余り $x+2$ を利用して $k(x-1)^2+x+2$ とおくと、未知数が1つで済む。"},
 {"lv": "B", "tag": "証明", "q": r"次の不等式を証明せよ。また、等号が成り立つのはどのようなときか。<br>(1) $a^2+b^2+c^2\geqq ab+bc+ca$（$a,\ b,\ c$ は実数）<br>(2) $\sqrt a+\sqrt b\leqq\sqrt{2(a+b)}$（$a\geqq0,\ b\geqq0$）",
  "a": r"(1) 等号は $a=b=c$　(2) 等号は $a=b$",
  "s": r"(1) (左辺)$-$(右辺)$=\frac12\{(a-b)^2+(b-c)^2+(c-a)^2\}\geqq0$。等号は $a=b=c$ のとき。■<br>(2) 両辺とも $0$ 以上なので、2乗の差を考える。$2(a+b)-(\sqrt a+\sqrt b)^2=a+b-2\sqrt{ab}=(\sqrt a-\sqrt b)^2\geqq0$。よって $(\sqrt a+\sqrt b)^2\leqq2(a+b)$ で、両辺が $0$ 以上だから $\sqrt a+\sqrt b\leqq\sqrt{2(a+b)}$。等号は $a=b$ のとき。■<br><b>ポイント</b>：根号を含む不等式は「両辺が $0$ 以上」を確かめてから2乗して比べる。"},
 {"lv": "B", "q": r"(1) $\dfrac x2=\dfrac y3=\dfrac z4\ (\neq0)$ のとき、$\dfrac{xy+yz+zx}{x^2+y^2+z^2}$ の値を求めよ。<br>(2) $a+b+c=0,\ abc\neq0$ のとき、$a\left(\dfrac1b+\dfrac1c\right)+b\left(\dfrac1c+\dfrac1a\right)+c\left(\dfrac1a+\dfrac1b\right)$ の値を求めよ。",
  "a": r"(1) $\frac{26}{29}$　(2) $-3$",
  "s": r"(1) 比の値を $k\ (\neq0)$ とおくと $x=2k,\ y=3k,\ z=4k$。与式 $=\frac{(6+12+8)k^2}{(4+9+16)k^2}=\frac{26}{29}$。<br>(2) 与式を分母ごとにまとめると $\frac{b+c}a+\frac{c+a}b+\frac{a+b}c$。$b+c=-a$ などを代入して $-1-1-1=-3$。<br><b>ポイント</b>：比例式は「$=k$ とおく」。条件式は1文字消去か、条件の形（ここでは $b+c=-a$）が現れるように式をまとめる。"},
 {"lv": "B", "q": r"(1) $x>1$ のとき、$x+\dfrac{4}{x-1}$ の最小値を求めよ。<br>(2) $x>0$ のとき、$\dfrac{x}{x^2+x+4}$ の最大値を求めよ。",
  "a": r"(1) $5$（$x=3$）　(2) $\frac15$（$x=2$）",
  "s": r"(1) $x-1>0$ なので $x+\frac4{x-1}=(x-1)+\frac4{x-1}+1\geqq2\sqrt4+1=5$。等号は $(x-1)^2=4$、$x>1$ より $x=3$。<br>(2) 分母・分子を $x\ (>0)$ で割ると $\frac1{x+\frac4x+1}$。$x+\frac4x\geqq4$（等号は $x=2$）なので分母 $\geqq5$、与式 $\leqq\frac15$。<br><b>ポイント</b>：相加・相乗平均は「積が定数」になる2項を作ってから使う。そのための変形（$x-1$ をつくる、分子で割る）が勝負。"},
 {"lv": "B", "tag": "コーシー・シュワルツ", "q": r"(1) 実数 $a,\ b,\ x,\ y$ について $(a^2+b^2)(x^2+y^2)\geqq(ax+by)^2$ を証明せよ。<br>(2) 実数 $x,\ y$ が $x^2+y^2=1$ を満たすとき、$3x+4y$ の最大値とそのときの $x,\ y$ を求めよ。<br>(3) 実数 $x,\ y,\ z$ が $x+2y+2z=6$ を満たすとき、$x^2+y^2+z^2$ の最小値とそのときの $x,\ y,\ z$ を求めよ。",
  "a": r"(1) 略　(2) 最大値 $5$（$x=\frac35,\ y=\frac45$）　(3) 最小値 $4$（$x=\frac23,\ y=z=\frac43$）",
  "s": r"(1) (左辺)$-$(右辺)$=a^2y^2+b^2x^2-2abxy=(ay-bx)^2\geqq0$。等号は $ay=bx$ のとき。■<br>(2) (1) より $(3^2+4^2)(x^2+y^2)\geqq(3x+4y)^2$、$(3x+4y)^2\leqq25$、$3x+4y\leqq5$。等号は $3y=4x$ かつ $3x+4y=5$ のときで $x=\frac35,\ y=\frac45$（$x^2+y^2=1$ を満たす）。<br>(3) 3文字でも $(a^2+b^2+c^2)(x^2+y^2+z^2)-(ax+by+cz)^2=(ay-bx)^2+(bz-cy)^2+(cx-az)^2\geqq0$ が成り立つ。$(1+4+4)(x^2+y^2+z^2)\geqq(x+2y+2z)^2=36$ より $x^2+y^2+z^2\geqq4$。等号は $x:y:z=1:2:2$ のときで、$x=t,\ y=z=2t$ を条件に代入して $9t=6$、$t=\frac23$。<br><b>ポイント</b>：1次式の条件のもとで2乗の和を評価するときはコーシー・シュワルツ。図形的には「原点から直線（平面）までの距離」と同じ。"},
 {"lv": "C", "tag": "二項定理", "q": r"(1) $11^{10}$ を $1000$ で割った余りを求めよ。<br>(2) 正の整数 $n$ について、$\displaystyle\sum_{k=1}^{n}k\,{}_n\mathrm{C}_k=n\cdot2^{n-1}$ を証明せよ。<br>(3) $n\geqq2$ のとき、$\displaystyle\sum_{k=1}^{n}k^2\,{}_n\mathrm{C}_k$ を $n$ の式で表せ。",
  "a": r"(1) $601$　(2) 略　(3) $n(n+1)2^{n-2}$",
  "s": r"(1) $11^{10}=(1+10)^{10}=\sum_{k=0}^{10}{}_{10}\mathrm{C}_k10^k$。$k\geqq3$ の項は $1000$ の倍数なので、余りは $1+10\cdot10+45\cdot100=4601$ を $1000$ で割った余りで $601$。<br>(2) $k\,{}_n\mathrm{C}_k=k\cdot\frac{n!}{k!(n-k)!}=n\cdot\frac{(n-1)!}{(k-1)!(n-k)!}=n\,{}_{n-1}\mathrm{C}_{k-1}$。よって $\sum_{k=1}^nk\,{}_n\mathrm{C}_k=n\sum_{j=0}^{n-1}{}_{n-1}\mathrm{C}_j=n\cdot2^{n-1}$（二項定理で $(1+1)^{n-1}$）。■<br>(3) $k^2{}_n\mathrm{C}_k=k\cdot n\,{}_{n-1}\mathrm{C}_{k-1}=n\{(k-1)+1\}{}_{n-1}\mathrm{C}_{k-1}$。$(k-1){}_{n-1}\mathrm{C}_{k-1}=(n-1){}_{n-2}\mathrm{C}_{k-2}$（$k\geqq2$）を使うと<br>$\sum k^2{}_n\mathrm{C}_k=n(n-1)\sum_{j=0}^{n-2}{}_{n-2}\mathrm{C}_j+n\sum_{j=0}^{n-1}{}_{n-1}\mathrm{C}_j=n(n-1)2^{n-2}+n\cdot2^{n-1}=n(n+1)2^{n-2}$。<br>（例：$n=10$ で $110\cdot256=28160$。）<br><b>ポイント</b>：$k\,{}_n\mathrm{C}_k=n\,{}_{n-1}\mathrm{C}_{k-1}$ は「$n$ 人から $k$ 人の委員を選び、その中から委員長を1人選ぶ」数え方を2通りにした式。"},
 {"lv": "C", "tag": "証明", "q": r"$a,\ b,\ c$ を正の数とする。<br>(1) $(a+b+c)\left(\dfrac1a+\dfrac1b+\dfrac1c\right)\geqq9$ を証明せよ。<br>(2) 正の数 $x,\ y,\ z$ について $x^3+y^3+z^3\geqq3xyz$ を証明し、これを用いて $a+b+c=1$ のとき $abc\leqq\dfrac1{27}$ であることを示せ。<br>(3) $a+b+c=1$ のとき、$\left(1+\dfrac1a\right)\left(1+\dfrac1b\right)\left(1+\dfrac1c\right)\geqq64$ を証明せよ。",
  "a": r"略（いずれも等号は $a=b=c$、(2)(3) では $a=b=c=\frac13$）",
  "s": r"(1) 展開すると $3+\left(\frac ab+\frac ba\right)+\left(\frac bc+\frac cb\right)+\left(\frac ca+\frac ac\right)$。各かっこは相加・相乗平均の関係より $2$ 以上なので、全体は $9$ 以上。■<br>(2) $x^3+y^3+z^3-3xyz=(x+y+z)(x^2+y^2+z^2-xy-yz-zx)=\frac12(x+y+z)\{(x-y)^2+(y-z)^2+(z-x)^2\}\geqq0$。■ $x=\sqrt[3]a,\ y=\sqrt[3]b,\ z=\sqrt[3]c$ とおくと $a+b+c\geqq3\sqrt[3]{abc}$。$a+b+c=1$ なら $\sqrt[3]{abc}\leqq\frac13$、$abc\leqq\frac1{27}$。■<br>(3) 展開すると $1+\left(\frac1a+\frac1b+\frac1c\right)+\left(\frac1{ab}+\frac1{bc}+\frac1{ca}\right)+\frac1{abc}$。ここで $\frac1{ab}+\frac1{bc}+\frac1{ca}=\frac{a+b+c}{abc}=\frac1{abc}$ なので、与式 $=1+\left(\frac1a+\frac1b+\frac1c\right)+\frac2{abc}$。(1) より $\frac1a+\frac1b+\frac1c\geqq9$、(2) より $\frac2{abc}\geqq54$。よって与式 $\geqq1+9+54=64$。等号は $a=b=c=\frac13$。■<br><b>ポイント</b>：条件 $a+b+c=1$ を「$1$ を $a+b+c$ に置き換える」形で使うと、各部分を既知の不等式で評価できる。"},
]}}


def verify():
    x, y, z, a, b, c, d, k, t = symbols("x y z a b c d k t")
    # A1
    e = expand((2*x-1/x)**6)
    assert e.coeff(x, 0) == -160 and e.coeff(x, 2) == 240
    # A2
    q, r = div(2*x**3-3*x**2+4*x-5, x**2-x+2, x)
    assert q == 2*x-1 and r == -x-3
    assert expand((x**2-x+2)*(2*x-1)) == 2*x**3-3*x**2+5*x-2
    sol = solve([8+4*a+2*b-6, -1+a-b-6], [a, b])
    assert sol == {a: 2, b: -5}
    assert expand((x-2)*(x+1)*(x+3) - (x**3+2*x**2-5*x-6)) == 0
    # A3
    sol = solve(Poly(x**3-(a*(x-1)**3+b*(x-1)**2+c*(x-1)+d), x).all_coeffs(), [a, b, c, d])
    assert sol == {a: 1, b: 3, c: 3, d: 1}
    assert simplify(1/(x*(x+2)) - (Rational(1, 2)/x - Rational(1, 2)/(x+2))) == 0
    # A4
    f = x+9/x
    assert solve(diff(f, x), x) == [-3, 3] and f.subs(x, 3) == 6
    g = expand((x+1/y)*(y+4/x))
    assert simplify(g - (x*y+4/(x*y)+5)) == 0
    assert g.subs({x: 1, y: 2}) == 9 and g.subs({x: 2, y: 1}) == 9
    # B1
    sol = solve([a+b-3, -2*a+b+3], [a, b])
    assert sol == {a: 2, b: 1}
    R = -Rational(1, 3)*(x-1)**2+x+2
    assert expand(R) == -x**2/3+Rational(5, 3)*x+Rational(5, 3)
    assert R.subs(x, 1) == 3 and R.subs(x, -2) == -3
    assert rem(R, (x-1)**2, x) == x+2
    # 具体例：P(x)=(x-1)^2(x+2)(x+5)+R(x) が条件をすべて満たす
    Pex = (x-1)**2*(x+2)*(x+5)+R
    assert rem(Pex, x-1, x) == 3 and rem(Pex, x+2, x) == -3 and rem(Pex, (x-1)*(x+2), x) == 2*x+1
    # B2
    assert expand(a**2+b**2+c**2-(a*b+b*c+c*a) - ((a-b)**2+(b-c)**2+(c-a)**2)/2) == 0
    p, s = symbols("p s", nonnegative=True)
    assert expand(2*(p**2+s**2)-(p+s)**2 - (p-s)**2) == 0
    # B3
    assert Rational(6+12+8, 4+9+16) == Rational(26, 29)
    expr = a*(1/b+1/c)+b*(1/c+1/a)+c*(1/a+1/b)
    assert simplify(expr.subs(c, -a-b)) == -3
    # B4
    h = x+4/(x-1)
    assert [v for v in solve(diff(h, x), x) if v > 1] == [3] and h.subs(x, 3) == 5
    h2 = x/(x**2+x+4)
    assert [v for v in solve(diff(h2, x), x) if v > 0] == [2] and h2.subs(x, 2) == Rational(1, 5)
    # B5
    assert expand((a**2+b**2)*(x**2+y**2)-(a*x+b*y)**2 - (a*y-b*x)**2) == 0
    X, Y = Rational(3, 5), Rational(4, 5)
    assert X**2+Y**2 == 1 and 3*X+4*Y == 5
    th = symbols("th")
    assert simplify(maximum(3*cos(th)+4*sin(th), th, Interval(0, 2*pi)) - 5) == 0
    A_, B_, C_ = symbols("A_ B_ C_")
    lhs = (A_**2+B_**2+C_**2)*(x**2+y**2+z**2)-(A_*x+B_*y+C_*z)**2
    assert expand(lhs - ((A_*y-B_*x)**2+(B_*z-C_*y)**2+(C_*x-A_*z)**2)) == 0
    # ラグランジュで最小を確認
    lam = symbols("lam")
    L = x**2+y**2+z**2-lam*(x+2*y+2*z-6)
    sol = solve([diff(L, v) for v in (x, y, z, lam)], [x, y, z, lam], dict=True)[0]
    assert (sol[x], sol[y], sol[z]) == (Rational(2, 3), Rational(4, 3), Rational(4, 3))
    assert sol[x]**2+sol[y]**2+sol[z]**2 == 4
    # C1
    assert pow(11, 10, 1000) == 601 and 1+10*10+45*100 == 4601
    for n in range(1, 15):
        assert sum(kk*comb(n, kk) for kk in range(1, n+1)) == n*2**(n-1)
        assert all(kk*comb(n, kk) == n*comb(n-1, kk-1) for kk in range(1, n+1))
    for n in range(2, 15):
        assert sum(kk*kk*comb(n, kk) for kk in range(1, n+1)) == n*(n+1)*2**(n-2)
    assert 10*11*2**8 == 28160
    # C2
    assert expand(x**3+y**3+z**3-3*x*y*z - (x+y+z)*((x-y)**2+(y-z)**2+(z-x)**2)/2) == 0
    E3 = expand((1+1/a)*(1+1/b)*(1+1/c))
    assert simplify(E3 - (1+(1/a+1/b+1/c)+(1/(a*b)+1/(b*c)+1/(c*a))+1/(a*b*c))) == 0
    assert simplify((1/(a*b)+1/(b*c)+1/(c*a)) - (a+b+c)/(a*b*c)) == 0
    third = Rational(1, 3)
    assert E3.subs({a: third, b: third, c: third}) == 64
    import random
    random.seed(3)
    for _ in range(300):
        u, v = sorted([random.random(), random.random()])
        A1, B1, C1 = u, v-u, 1-v
        if min(A1, B1, C1) < 1e-6:
            continue
        assert (A1+B1+C1)*(1/A1+1/B1+1/C1) >= 9-1e-9
        assert A1*B1*C1 <= 1/27+1e-12
        assert (1+1/A1)*(1+1/B1)*(1+1/C1) >= 64-1e-9
