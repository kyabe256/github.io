"""問題集 第15章 積分法（数学II）。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {15: {
"goal": r"不定積分・定積分を速く正確に。定積分で表された関数を微分で処理し、面積は「上−下」と $\frac16$ 公式を使い分ける。",
"items": [
 {"lv": "A", "q": r"次の計算をせよ。(1) $\displaystyle\int(3x^2-4x+1)\,dx$　(2) $\displaystyle\int_{-1}^{2}(x^2+2x-1)\,dx$　(3) $\displaystyle\int_{-2}^{2}(x^3+3x^2-x+1)\,dx$",
  "a": r"(1) $x^3-2x^2+x+C$（$C$ は積分定数）　(2) $3$　(3) $20$",
  "s": r"(1) 項ごとに $\int x^n dx=\frac{x^{n+1}}{n+1}+C$。<br>(2) $\left[\frac{x^3}{3}+x^2-x\right]_{-1}^{2}=\left(\frac83+4-2\right)-\left(-\frac13+1+1\right)=\frac{14}{3}-\frac53=3$。<br>(3) 奇関数 $x^3,\ -x$ の部分は $0$。偶関数の部分は $2$ 倍：$2\int_0^2(3x^2+1)dx=2\left[x^3+x\right]_0^2=2\cdot10=20$。<br><b>ポイント</b>：区間が $-a$ から $a$ のときは、奇数次の項を消し偶数次の項を $2\int_0^a$ にする。"},
 {"lv": "A", "q": r"$f'(x)=6x^2-2x+1$、$f(1)=3$ を満たす関数 $f(x)$ を求めよ。",
  "a": r"$f(x)=2x^3-x^2+x+1$",
  "s": r"$f(x)=\int(6x^2-2x+1)dx=2x^3-x^2+x+C$。$f(1)=2-1+1+C=2+C=3$ より $C=1$。<br><b>ポイント</b>：不定積分の積分定数は、与えられた条件（初期条件）で決める。"},
 {"lv": "A", "q": r"次の図形の面積を求めよ。(1) 放物線 $y=x^2-2x-3$ と $x$ 軸で囲まれた図形　(2) 放物線 $y=x^2$ と直線 $y=x+2$ で囲まれた図形",
  "a": r"(1) $\frac{32}{3}$　(2) $\frac92$",
  "s": r"(1) $x^2-2x-3=(x+1)(x-3)$。$-1\leqq x\leqq3$ で $y\leqq0$ なので $S=-\int_{-1}^{3}(x+1)(x-3)dx=\frac{(3-(-1))^3}{6}=\frac{64}{6}=\frac{32}{3}$。<br>(2) $x^2=x+2$ より $x=-1,\ 2$。$S=\int_{-1}^{2}\{(x+2)-x^2\}dx=-\int_{-1}^{2}(x+1)(x-2)dx=\frac{3^3}{6}=\frac92$。<br><b>ポイント</b>：$\displaystyle\int_\alpha^\beta(x-\alpha)(x-\beta)dx=-\frac{(\beta-\alpha)^3}{6}$（$\frac16$ 公式）。放物線と直線で囲まれた面積は交点の $x$ 座標の差だけで決まる。"},
 {"lv": "A", "q": r"関数 $F(x)=\displaystyle\int_1^x(t^2-3t+2)\,dt$ の極値を求めよ。",
  "a": r"$x=1$ で極大値 $0$、$x=2$ で極小値 $-\frac16$",
  "s": r"$F'(x)=x^2-3x+2=(x-1)(x-2)$。$F'$ の符号は $x=1$ の前後で $+\to-$、$x=2$ の前後で $-\to+$。<br>$F(1)=\int_1^1(\cdots)dt=0$。$F(2)=\int_1^2(t-1)(t-2)dt=-\frac{(2-1)^3}{6}=-\frac16$。<br><b>ポイント</b>：$\dfrac{d}{dx}\displaystyle\int_a^x f(t)\,dt=f(x)$。上端と下端が等しい定積分は $0$。"},
 {"lv": "B", "tag": "典型", "q": r"等式 $f(x)=3x^2-2x\displaystyle\int_0^1 f(t)\,dt+\int_0^2 f(t)\,dt$ を満たす関数 $f(x)$ を求めよ。",
  "a": r"$f(x)=3x^2-7x+6$",
  "s": r"定積分は定数なので $a=\int_0^1f(t)dt,\ b=\int_0^2f(t)dt$ とおくと $f(x)=3x^2-2ax+b$。<br>$a=\int_0^1(3t^2-2at+b)dt=1-a+b$ より $2a-b=1$。<br>$b=\int_0^2(3t^2-2at+b)dt=8-4a+2b$ より $b=4a-8$。<br>代入して $2a-(4a-8)=1$、$a=\frac72$、$b=6$。よって $f(x)=3x^2-7x+6$。<br>（確認）$\int_0^1f=1-\frac72+6=\frac72$、$\int_0^2f=8-14+12=6$。<br><b>ポイント</b>：積分区間が定数の定積分は「定数」とおく。$x$ を含む式（$\int_0^x$ など）と区別すること。"},
 {"lv": "B", "tag": "典型", "q": r"等式 $\displaystyle\int_a^x f(t)\,dt=x^3-3x+2$ がすべての $x$ について成り立つような関数 $f(x)$ と定数 $a$ の値を求めよ。",
  "a": r"$f(x)=3x^2-3$、$a=1,\ -2$",
  "s": r"両辺を $x$ で微分して $f(x)=3x^2-3$。また $x=a$ を代入すると左辺は $0$ なので $a^3-3a+2=0$、$(a-1)^2(a+2)=0$ より $a=1,\ -2$。<br>（確認）$\int_1^x(3t^2-3)dt=x^3-3x+2$、$\int_{-2}^x(3t^2-3)dt=x^3-3x-(-8+6)=x^3-3x+2$。<br><b>ポイント</b>：「微分する」と「$x=a$ を代入する」の2つで $f$ と $a$ が決まる。"},
 {"lv": "B", "tag": "頻出", "q": r"点 $\mathrm{A}(1,\ -3)$ から放物線 $C:\ y=x^2$ に引いた2本の接線と $C$ で囲まれた図形の面積を求めよ。",
  "a": r"$\frac{16}{3}$",
  "s": r"$C$ 上の点 $(t,t^2)$ における接線は $y=2tx-t^2$。A を通るので $-3=2t-t^2$、$t^2-2t-3=0$、$t=-1,\ 3$。接線は $\ell_1:\ y=-2x-1$（接点 $x=-1$）、$\ell_2:\ y=6x-9$（接点 $x=3$）。2接線の交点は A で、その $x$ 座標は $1$（接点の $x$ 座標の平均）。<br>$S=\int_{-1}^{1}\{x^2-(-2x-1)\}dx+\int_1^3\{x^2-(6x-9)\}dx=\int_{-1}^{1}(x+1)^2dx+\int_1^3(x-3)^2dx$<br>$=\left[\frac{(x+1)^3}{3}\right]_{-1}^{1}+\left[\frac{(x-3)^3}{3}\right]_1^3=\frac83+\frac83=\frac{16}{3}$。<br><b>ポイント</b>：放物線と接線の差は $(x-\text{接点})^2$ の形。$\int(x-p)^2dx=\frac{(x-p)^3}{3}+C$ を使うと展開せずに計算できる。"},
 {"lv": "B", "tag": "場合分け", "q": r"$a\geqq0$ とする。$S(a)=\displaystyle\int_0^1|x^2-a^2|\,dx$ を $a$ の式で表し、$S(a)$ の最小値を求めよ。",
  "a": r"$S(a)=\frac43a^3-a^2+\frac13\ (0\leqq a\leqq1),\ a^2-\frac13\ (a\gt1)$；最小値 $\frac14$（$a=\frac12$）",
  "s": r"<b>$0\leqq a\leqq1$ のとき</b>：$0\leqq x\leqq a$ で $x^2-a^2\leqq0$、$a\leqq x\leqq1$ で $\geqq0$。<br>$S(a)=\int_0^a(a^2-x^2)dx+\int_a^1(x^2-a^2)dx=\frac23a^3+\left\{\frac{1-a^3}{3}-a^2(1-a)\right\}=\frac43a^3-a^2+\frac13$。<br><b>$a\gt1$ のとき</b>：$0\leqq x\leqq1$ で $x^2-a^2\lt0$ なので $S(a)=\int_0^1(a^2-x^2)dx=a^2-\frac13$。<br>最小値：$0\leqq a\leqq1$ で $S'(a)=4a^2-2a=2a(2a-1)$ より $a=\frac12$ で極小かつ最小、$S\left(\frac12\right)=\frac16-\frac14+\frac13=\frac14$。$a\gt1$ では $S(a)\gt1-\frac13=\frac23$ で増加。よって最小値 $\frac14$（$a=\frac12$）。<br><b>ポイント</b>：絶対値の中身の符号が変わる点 $x=a$ が積分区間に入るかどうかで場合分け。"},
 {"lv": "B", "tag": "典型", "q": r"曲線 $C:\ y=x^3-x$ 上の点 $(1,\ 0)$ における接線を $\ell$ とする。$C$ と $\ell$ で囲まれた図形の面積を求めよ。",
  "a": r"$\frac{27}{4}$",
  "s": r"$y'=3x^2-1$ より $\ell:\ y=2(x-1)=2x-2$。$x^3-x-(2x-2)=x^3-3x+2=(x-1)^2(x+2)$ なので、$C$ と $\ell$ は $x=1$ で接し、$x=-2$ で交わる。$-2\leqq x\leqq1$ で $(x-1)^2(x+2)\geqq0$ より $C$ が上。<br>$S=\int_{-2}^{1}(x-1)^2(x+2)dx$。$x+2=(x-1)+3$ と変形して $\int_{-2}^{1}\{(x-1)^3+3(x-1)^2\}dx=\left[\frac{(x-1)^4}{4}+(x-1)^3\right]_{-2}^{1}=0-\left(\frac{81}{4}-27\right)=\frac{27}{4}$。<br><b>ポイント</b>：一般に $\int_\alpha^\beta(x-\alpha)^2(x-\beta)dx=-\frac{(\beta-\alpha)^4}{12}$。今回は $\frac{3^4}{12}=\frac{27}{4}$ と一致する。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"放物線 $C:\ y=x^2$ 上の2点 P、Q を結ぶ線分と $C$ で囲まれた図形の面積が $\frac43$ であるように P、Q が動く。(1) 線分 PQ の中点 M の軌跡を求めよ。(2) P、Q における $C$ の接線の交点 T の軌跡を求めよ。",
  "a": r"(1) 放物線 $y=x^2+1$　(2) 放物線 $y=x^2-1$",
  "s": r"P、Q の $x$ 座標を $\alpha,\ \beta\ (\alpha\lt\beta)$ とする。直線 PQ を $y=mx+n$ とすると $x^2-(mx+n)=(x-\alpha)(x-\beta)$ なので、面積は $\int_\alpha^\beta\{(mx+n)-x^2\}dx=\frac{(\beta-\alpha)^3}{6}$。これが $\frac43$ ⇔ $(\beta-\alpha)^3=8$ ⇔ $\beta-\alpha=2$。<br>(1) M$(X,Y)$ とすると $X=\frac{\alpha+\beta}{2}$、$\alpha=X-1,\ \beta=X+1$。$Y=\frac{\alpha^2+\beta^2}{2}=\frac{(X-1)^2+(X+1)^2}{2}=X^2+1$。$X$ はすべての実数をとるので、軌跡は放物線 $y=x^2+1$。<br>(2) P、Q の接線 $y=2\alpha x-\alpha^2$、$y=2\beta x-\beta^2$ の交点は、引いて $2(\alpha-\beta)x=\alpha^2-\beta^2$ より $x=\frac{\alpha+\beta}{2}=X$、$y=\alpha\beta=(X-1)(X+1)=X^2-1$。軌跡は放物線 $y=x^2-1$。<br><b>ポイント</b>：面積条件が「$\beta-\alpha$ 一定」に言い換えられるのが $\frac16$ 公式の強み。中点 M と交点 T は同じ $x$ 座標をもつ。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"放物線 $C:\ y=x^2$ 上の点 $\mathrm{P}(t,\ t^2)\ (t\gt0)$ における $C$ の法線（P を通り、P における接線に垂直な直線）が、$C$ と再び交わる点を Q とする。線分 PQ と $C$ で囲まれた図形の面積 $S(t)$ の最小値と、そのときの $t$ を求めよ。",
  "a": r"最小値 $\frac43$（$t=\frac12$）",
  "s": r"P における接線の傾きは $2t$ なので、法線は $y-t^2=-\frac{1}{2t}(x-t)$。$C$ との交点の $x$ 座標は $x^2+\frac{1}{2t}x-t^2-\frac12=0$ の解で、1つは $t$。解と係数の関係（和 $=-\frac1{2t}$）より、Q の $x$ 座標は $q=-t-\frac{1}{2t}$。<br>$\frac16$ 公式より $S(t)=\frac{(t-q)^3}{6}=\frac16\left(2t+\frac{1}{2t}\right)^3$。<br>$t\gt0$ なので相加平均・相乗平均の関係より $2t+\frac{1}{2t}\geqq2\sqrt{2t\cdot\frac{1}{2t}}=2$、等号は $2t=\frac1{2t}$ すなわち $t=\frac12$ のとき。<br>よって $S(t)\geqq\frac{2^3}{6}=\frac43$ で、最小値 $\frac43$（$t=\frac12$）。<br><b>ポイント</b>：面積を「交点の $x$ 座標の差」の関数にすれば、最小化は差の最小化に帰着する。解と係数の関係で、もう1つの交点を因数分解なしで求められる。"},
]}}

def verify():
    x, t, a, C = symbols("x t a C", real=True)
    assert expand(integrate(3*x**2-4*x+1, x) - (x**3-2*x**2+x)) == 0
    assert integrate(x**2+2*x-1, (x, -1, 2)) == 3
    assert integrate(x**3+3*x**2-x+1, (x, -2, 2)) == 20 and 2*integrate(3*x**2+1, (x, 0, 2)) == 20
    f = 2*x**3-x**2+x+1
    assert expand(diff(f, x)-(6*x**2-2*x+1)) == 0 and f.subs(x, 1) == 3
    assert integrate(-(x**2-2*x-3), (x, -1, 3)) == Rational(32, 3)
    assert integrate(x+2-x**2, (x, -1, 2)) == Rational(9, 2)
    F = integrate(t**2-3*t+2, (t, 1, x))
    assert expand(diff(F, x)-(x-1)*(x-2)) == 0 and F.subs(x, 1) == 0 and F.subs(x, 2) == Rational(-1, 6)
    # B1
    f = 3*x**2-7*x+6
    assert integrate(f, (x, 0, 1)) == Rational(7, 2) and integrate(f, (x, 0, 2)) == 6
    assert expand(f - (3*x**2-2*x*Rational(7, 2)+6)) == 0
    # B2
    for av in [1, -2]:
        assert expand(integrate(3*t**2-3, (t, av, x)) - (x**3-3*x+2)) == 0
    assert expand((a-1)**2*(a+2) - (a**3-3*a+2)) == 0
    # B3
    assert solve(t**2-2*t-3, t) == [-1, 3]
    S = integrate(x**2-(-2*x-1), (x, -1, 1)) + integrate(x**2-(6*x-9), (x, 1, 3))
    assert S == Rational(16, 3) and Rational(4**3, 12) == S
    # B4
    ap = symbols("ap", positive=True)
    S1 = integrate(ap**2-x**2, (x, 0, ap)) + integrate(x**2-ap**2, (x, ap, 1))
    assert expand(S1 - (Rational(4, 3)*ap**3-ap**2+Rational(1, 3))) == 0
    assert expand(integrate(ap**2-x**2, (x, 0, 1)) - (ap**2-Rational(1, 3))) == 0
    assert S1.subs(ap, Rational(1, 2)) == Rational(1, 4)
    for av in [Rational(1, 5), Rational(1, 2), Rational(4, 5), 1, Rational(3, 2)]:
        import mpmath
        val = mpmath.quad(lambda u: abs(u**2-float(av)**2), [0, min(float(av), 1), 1])
        expect = Rational(4, 3)*av**3-av**2+Rational(1, 3) if av <= 1 else av**2-Rational(1, 3)
        assert abs(val - float(expect)) < 1e-9 and expect >= Rational(1, 4)
    # B5
    assert expand(x**3-x-(2*x-2) - (x-1)**2*(x+2)) == 0
    assert integrate((x-1)**2*(x+2), (x, -2, 1)) == Rational(27, 4) == Rational(3**4, 12)
    al, be = symbols("al be", real=True)
    assert simplify(integrate((x-al)**2*(x-be), (x, al, be)) + (be-al)**4/12) == 0
    assert simplify(integrate((x-al)*(x-be), (x, al, be)) + (be-al)**3/6) == 0
    # C1
    X = symbols("X", real=True)
    assert expand(((X-1)**2+(X+1)**2)/2 - (X**2+1)) == 0
    # 数値例：alpha=0.5, beta=2.5 で面積 4/3
    al0, be0 = Rational(1, 2), Rational(5, 2)
    m, n = al0+be0, -al0*be0
    assert integrate(m*x+n-x**2, (x, al0, be0)) == Rational(4, 3)
    tx = solve(2*al0*x-al0**2-(2*be0*x-be0**2), x)[0]
    assert tx == (al0+be0)/2 and 2*al0*tx-al0**2 == al0*be0 == tx**2-1
    # C2
    tp = symbols("tp", positive=True)
    roots = solve(x**2 + x/(2*tp) - tp**2 - Rational(1, 2), x)
    assert any(simplify(r - tp) == 0 for r in roots)
    q = [r for r in roots if simplify(r-tp) != 0][0]
    assert simplify(q - (-tp-1/(2*tp))) == 0
    # 法線と放物線の囲む面積
    line = tp**2 - (x-tp)/(2*tp)
    Sx = integrate(line - x**2, (x, q, tp))
    assert simplify(Sx - (2*tp+1/(2*tp))**3/6) == 0
    assert simplify(Sx.subs(tp, Rational(1, 2)) - Rational(4, 3)) == 0
    assert minimum((2*tp+1/(2*tp))**3/6, tp, Interval.open(0, oo)) == Rational(4, 3)
