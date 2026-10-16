"""問題集 第10章 複素数と方程式。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {10: {
"goal": "複素数の計算と2次方程式の判別式、解と係数の関係、剰余の定理・因数定理を使って高次方程式を扱う。$\\omega$ の性質と対称式の扱いを自在にする。",
"items": [
 {"lv": "A", "q": r"次の計算をせよ。ただし $i$ は虚数単位とする。<br>(1) $(2+3i)(1-2i)$　(2) $\dfrac{1+2i}{2-i}$　(3) $(1+i)^8$",
  "a": r"(1) $8-i$　(2) $i$　(3) $16$",
  "s": r"(1) $2-4i+3i-6i^2=8-i$。(2) 分母の共役 $2+i$ を分母分子に掛けて $\frac{(1+2i)(2+i)}{5}=\frac{2+5i+2i^2}{5}=\frac{5i}5=i$。(3) $(1+i)^2=2i$ より $(1+i)^8=(2i)^4=16i^4=16$。<br><b>ポイント</b>：割り算は分母の共役複素数を掛けて実数化。累乗は2乗をつくってから。"},
 {"lv": "A", "q": r"(1) 2次方程式 $x^2-2x+5=0$ を解け。<br>(2) 2次方程式 $x^2+2kx+k+6=0$ が虚数解をもつような定数 $k$ の値の範囲を求めよ。",
  "a": r"(1) $x=1\pm2i$　(2) $-2<k<3$",
  "s": r"(1) $x=1\pm\sqrt{1-5}=1\pm2i$。(2) $\frac D4=k^2-(k+6)=(k-3)(k+2)<0$ より $-2<k<3$。<br><b>ポイント</b>：虚数解をもつ $\iff$ 判別式 $D<0$（係数が実数のとき）。"},
 {"lv": "A", "q": r"2次方程式 $x^2-3x+5=0$ の2つの解を $\alpha,\ \beta$ とするとき、次の値を求めよ。<br>(1) $\alpha^2+\beta^2$　(2) $\alpha^3+\beta^3$　(3) $\dfrac\beta\alpha+\dfrac\alpha\beta$<br>(4) また、$\alpha+1,\ \beta+1$ を2つの解とする2次方程式を1つ作れ。",
  "a": r"(1) $-1$　(2) $-18$　(3) $-\frac15$　(4) $x^2-5x+9=0$",
  "s": r"解と係数の関係より $\alpha+\beta=3,\ \alpha\beta=5$。<br>(1) $9-10=-1$。(2) $(\alpha+\beta)^3-3\alpha\beta(\alpha+\beta)=27-45=-18$。(3) $\frac{\alpha^2+\beta^2}{\alpha\beta}=-\frac15$。<br>(4) 和 $(\alpha+1)+(\beta+1)=5$、積 $\alpha\beta+(\alpha+\beta)+1=9$ より $x^2-5x+9=0$。<br><b>ポイント</b>：$\alpha^2+\beta^2$ が負になるのは $\alpha,\beta$ が虚数だから。対称式は基本対称式で表せる。"},
 {"lv": "A", "q": r"3次方程式 $x^3-3x^2+4x-2=0$ を解け。",
  "a": r"$x=1,\ 1\pm i$",
  "s": r"$P(x)=x^3-3x^2+4x-2$ とおくと $P(1)=1-3+4-2=0$ なので、因数定理より $P(x)$ は $x-1$ を因数にもつ。割り算して $P(x)=(x-1)(x^2-2x+2)$。$x^2-2x+2=0$ より $x=1\pm i$。<br><b>ポイント</b>：整数係数なら、有理数解の候補は「（定数項の約数）÷（最高次の係数の約数）」に $\pm$ をつけたもの。ここでは $\pm1,\pm2$ を代入してみる。"},
 {"lv": "B", "tag": "1の3乗根", "q": r"$\omega$ を $1$ の3乗根のうち虚数であるものの1つとする。次の値を求めよ。<br>(1) $\omega^{100}+\omega^{50}+1$　(2) $(\omega+2)(\omega^2+2)$　(3) $(1+\omega)^{10}$ を $a\omega+b$（$a,\ b$ は実数）の形で表せ。",
  "a": r"(1) $0$　(2) $3$　(3) $-\omega-1$",
  "s": r"$\omega^3=1$ かつ $\omega\neq1$ より、$(\omega-1)(\omega^2+\omega+1)=0$ から $\omega^2+\omega+1=0$。<br>(1) $100=3\cdot33+1,\ 50=3\cdot16+2$ より $\omega^{100}=\omega,\ \omega^{50}=\omega^2$。与式 $=\omega+\omega^2+1=0$。<br>(2) $\omega^3+2(\omega^2+\omega)+4=1-2+4=3$。<br>(3) $1+\omega=-\omega^2$ より $(1+\omega)^{10}=\omega^{20}=\omega^{2}=-\omega-1$。<br><b>ポイント</b>：$\omega$ は「$\omega^3=1$」と「$\omega^2+\omega+1=0$」の2つで処理する。"},
 {"lv": "B", "q": r"3次方程式 $x^3-2x^2+3x-4=0$ の3つの解を $\alpha,\ \beta,\ \gamma$ とする。次の値を求めよ。<br>(1) $\alpha^2+\beta^2+\gamma^2$　(2) $(1+\alpha)(1+\beta)(1+\gamma)$　(3) $\alpha^3+\beta^3+\gamma^3$",
  "a": r"(1) $-2$　(2) $10$　(3) $2$",
  "s": r"$\alpha+\beta+\gamma=2,\ \alpha\beta+\beta\gamma+\gamma\alpha=3,\ \alpha\beta\gamma=4$。<br>(1) $2^2-2\cdot3=-2$。<br>(2) $P(x)=x^3-2x^2+3x-4=(x-\alpha)(x-\beta)(x-\gamma)$ に $x=-1$ を代入すると $P(-1)=-(1+\alpha)(1+\beta)(1+\gamma)$。$P(-1)=-1-2-3-4=-10$ なので、求める値は $10$。<br>(3) 各解は $x^3=2x^2-3x+4$ を満たすので、和をとって $\sum\alpha^3=2\sum\alpha^2-3\sum\alpha+12=-4-6+12=2$。<br><b>ポイント</b>：$(k-\alpha)(k-\beta)(k-\gamma)=P(k)$ は解と係数の関係を経由しない近道。高次の対称式は「もとの方程式で次数を下げる」。"},
 {"lv": "B", "q": r"$a,\ b$ を実数とする。3次方程式 $x^3+ax^2+bx+10=0$ が $1+2i$ を解にもつとき、$a,\ b$ の値と他の解を求めよ。",
  "a": r"$a=0,\ b=1$、他の解は $1-2i,\ -2$",
  "s": r"係数が実数なので、共役な $1-2i$ も解。この2数を解とする2次方程式は $x^2-2x+5=0$。よって $x^3+ax^2+bx+10=(x^2-2x+5)(x+c)$ と表せる。右辺 $=x^3+(c-2)x^2+(5-2c)x+5c$。定数項を比べて $5c=10$、$c=2$。$a=c-2=0,\ b=5-2c=1$。残りの解は $x=-c=-2$。<br>（別解）$x=1+2i$ を代入し、実部・虚部がともに $0$ となる条件から $a,b$ を求めてもよい。<br><b>ポイント</b>：実数係数の方程式の虚数解は、共役とペアで現れる。"},
 {"lv": "B", "q": r"(1) $x^{50}$ を $x^2-3x+2$ で割った余りを求めよ。<br>(2) $x^{100}$ を $x^2+x+1$ で割った余りを求めよ。",
  "a": r"(1) $(2^{50}-1)x-2^{50}+2$　(2) $x$",
  "s": r"(1) $x^{50}=(x-1)(x-2)Q(x)+ax+b$ とおく。$x=1$ で $1=a+b$、$x=2$ で $2^{50}=2a+b$。$a=2^{50}-1,\ b=2-2^{50}$。<br>(2) $x^{100}=(x^2+x+1)Q(x)+ax+b$ に $x=\omega$（$\omega^2+\omega+1=0$ の解）を代入すると $\omega^{100}=\omega$ なので $\omega=a\omega+b$。$a,b$ は実数で $\omega$ は虚数だから $a=1,\ b=0$。余りは $x$。<br>（別解）$x^3-1=(x-1)(x^2+x+1)$ より $x^3$ は $x^2+x+1$ で割った余りの計算では $1$ とみなせるので、$x^{100}=(x^3)^{33}x$ の余りは $x$。<br><b>ポイント</b>：割る式の解を代入する。解が虚数なら「$a,b$ 実数で実部・虚部比較」。"},
 {"lv": "B", "q": r"2つの2次方程式 $x^2+(a-1)x+a^2=0$ …①、$x^2+2ax-2a=0$ …② について、次の条件を満たす実数 $a$ の値の範囲を求めよ。<br>(1) ①、② がともに虚数解をもつ。　(2) ①、② の少なくとも一方が虚数解をもつ。<br>(3) ①、② の一方だけが虚数解をもつ。",
  "a": r"(1) $-2<a<-1$　(2) $a<0,\ \frac13<a$　(3) $a\leqq-2,\ -1\leqq a<0,\ \frac13<a$",
  "s": r"①の判別式 $D_1=(a-1)^2-4a^2=-(3a-1)(a+1)$。$D_1<0\iff a<-1,\ \frac13<a$。<br>②の判別式 $\frac{D_2}4=a^2+2a=a(a+2)$。$D_2<0\iff-2<a<0$。<br>(1) 共通部分 $-2<a<-1$。(2) 和集合 $a<0,\ \frac13<a$。(3) (2) から (1) を除いて $a\leqq-2,\ -1\leqq a<0,\ \frac13<a$。<br><b>ポイント</b>：「ともに」は共通部分、「少なくとも一方」は和集合、「一方だけ」はその差。数直線に2つの範囲を描いて読む。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"3次方程式 $x^3-3x+1=0$ の3つの解を $\alpha,\ \beta,\ \gamma$ とする。<br>(1) $\alpha^2,\ \beta^2,\ \gamma^2$ を解とする3次方程式 $Q(x)=0$（$x^3$ の係数は $1$）を求めよ。<br>(2) $P(x)=x^3-3x+1$ とする。$P(t^2-2)=Q(t^2)$ が $t$ の恒等式であることを示し、$\alpha^2-2$ も $P(x)=0$ の解であることを示せ。<br>(3) $\alpha^5+\beta^5+\gamma^5$ の値を求めよ。",
  "a": r"(1) $x^3-6x^2+9x-1=0$　(2) 略　(3) $-15$",
  "s": r"$\alpha+\beta+\gamma=0,\ \alpha\beta+\beta\gamma+\gamma\alpha=-3,\ \alpha\beta\gamma=-1$。<br>(1) $\sum\alpha^2=0-2(-3)=6$。$\sum\alpha^2\beta^2=(\alpha\beta+\beta\gamma+\gamma\alpha)^2-2\alpha\beta\gamma(\alpha+\beta+\gamma)=9$。$\alpha^2\beta^2\gamma^2=1$。よって $Q(x)=x^3-6x^2+9x-1$。<br>(2) $P(t^2-2)=(t^2-2)^3-3(t^2-2)+1=t^6-6t^4+12t^2-8-3t^2+6+1=t^6-6t^4+9t^2-1=Q(t^2)$。■ $t=\alpha$ とおくと、(1) より $Q(\alpha^2)=0$ なので $P(\alpha^2-2)=0$。■<br>(3) $p_k=\alpha^k+\beta^k+\gamma^k$ とおく。各解は $x^3=3x-1$ を満たすので、$x^{k+3}=3x^{k+1}-x^k$ を足して $p_{k+3}=3p_{k+1}-p_k$。$p_0=3,\ p_1=0,\ p_2=6$ から $p_3=3p_1-p_0=-3$、$p_4=3p_2-p_1=18$、$p_5=3p_3-p_2=-15$。<br><b>ポイント</b>：解の累乗和は「方程式で次数を下げる」漸化式で順に求める。(2) は、解が $2\cos\frac{2\pi}9$ などで表され、$\alpha^2-2$ が2倍角に対応していることの代数的な表れ。"},
 {"lv": "C", "tag": "論証", "q": r"$\omega$ を $1$ の3乗根のうち虚数であるものの1つとし、$n$ を正の整数とする。<br>(1) $\omega^{2n}+\omega^n+1$ の値を求めよ。<br>(2) $x^{2n}+x^n+1$ が $x^2+x+1$ で割り切れるための $n$ の条件を求めよ。<br>(3) $x^{2n}+x^n+1$ が $x^2+x+1$ で割り切れないとき、余りを求めよ。",
  "a": r"(1) $n$ が3の倍数のとき $3$、そうでないとき $0$　(2) $n$ が3の倍数でない　(3) $3$",
  "s": r"$\omega^3=1,\ \omega^2+\omega+1=0$、また $x^2+x+1=(x-\omega)(x-\omega^2)$ で $\omega\neq\omega^2$。<br>(1) $n=3m$ なら $\omega^n=1$ で値は $3$。$n=3m+1$ なら $\omega^{2n}+\omega^n+1=\omega^2+\omega+1=0$。$n=3m+2$ なら $\omega^{2n}=\omega^{6m+4}=\omega,\ \omega^n=\omega^2$ で値は $0$。<br>(2) $f(x)=x^{2n}+x^n+1$ が $(x-\omega)(x-\omega^2)$ で割り切れる $\iff f(\omega)=f(\omega^2)=0$。$f$ は実数係数なので $f(\omega^2)=f(\overline\omega)=\overline{f(\omega)}$ となり、$f(\omega)=0$ だけ調べればよい。(1) より $n$ が3の倍数でないこと。<br>(3) (2) より $n$ は3の倍数。$x^3-1=(x-1)(x^2+x+1)$ なので $x^3=(x^2+x+1)(x-1)+1$、よって $x^{3m}$ を $x^2+x+1$ で割った余りは $1$ で、$f(x)$ の余りは $1+1+1=3$。（余りを $ax+b$ とおいて $x=\omega$ を代入しても $a\omega+b=3$ から $a=0,\ b=3$。）<br><b>ポイント</b>：割り切れる条件は「割る式の解をすべて代入して $0$」。重解がないことと、実数係数なら共役の解は自動的に満たすことを確認する。"},
]}}


def verify():
    x, k, a, b, c, t = symbols("x k a b c t")
    # A1
    assert expand((2+3*I)*(1-2*I)) == 8-I
    assert simplify((1+2*I)/(2-I)) == I
    assert expand((1+I)**8) == 16
    # A2
    assert set(solve(x**2-2*x+5, x)) == {1-2*I, 1+2*I}
    assert solve_univariate_inequality(k**2-(k+6) < 0, k, relational=False) == Interval.open(-2, 3)
    # A3
    r1, r2 = solve(x**2-3*x+5, x)
    assert simplify(r1**2+r2**2+1) == 0 and simplify(r1**3+r2**3+18) == 0
    assert simplify(r2/r1+r1/r2+Rational(1, 5)) == 0
    assert expand((x-(r1+1))*(x-(r2+1))) == x**2-5*x+9
    # A4
    assert factor(x**3-3*x**2+4*x-2) == (x-1)*(x**2-2*x+2)
    assert set(solve(x**3-3*x**2+4*x-2, x)) == {1, 1-I, 1+I}
    # B1
    for w in [(-1+sqrt(3)*I)/2, (-1-sqrt(3)*I)/2]:
        assert simplify(expand(w**100+w**50+1)) == 0
        assert simplify(expand((w+2)*(w**2+2))-3) == 0
        assert simplify(expand((1+w)**10-(-w-1))) == 0
    # B2
    P = x**3-2*x**2+3*x-4
    rs = Poly(P, x).nroots(n=30)
    assert abs(sum(r**2 for r in rs)+2) < 1e-20
    assert abs(prod([1+r for r in rs])-10) < 1e-20
    assert abs(sum(r**3 for r in rs)-2) < 1e-20
    assert P.subs(x, -1) == -10
    # B3
    ar, br = symbols("ar br", real=True)
    sol = solve([e for e in (expand((1+2*I)**3+ar*(1+2*I)**2+br*(1+2*I)+10)).as_real_imag()], [ar, br])
    assert sol == {ar: 0, br: 1}
    assert set(solve(x**3+x+10, x)) == {1+2*I, 1-2*I, -2}
    assert expand((x**2-2*x+5)*(x+2)) == x**3+x+10
    # B4
    assert rem(x**50, x**2-3*x+2, x) == expand((2**50-1)*x-2**50+2)
    assert rem(x**100, x**2+x+1, x) == x
    # B5
    for av in [Rational(n, 12) for n in range(-48, 24)]:
        D1 = (av-1)**2-4*av**2; D2 = av**2+2*av
        both = D1 < 0 and D2 < 0; some = D1 < 0 or D2 < 0; one = some and not both
        assert both == (-2 < av < -1), av
        assert some == (av < 0 or av > Rational(1, 3)), av
        assert one == (av <= -2 or -1 <= av < 0 or av > Rational(1, 3)), av
    assert expand((a-1)**2-4*a**2 + (3*a-1)*(a+1)) == 0
    # C1
    P = x**3-3*x+1; Q = x**3-6*x**2+9*x-1
    rs = Poly(P, x).nroots(n=40)
    rq = Poly(Q, x).nroots(n=40)
    assert all(min(abs(r**2-q) for q in rq) < 1e-30 for r in rs)
    assert expand(P.subs(x, t**2-2) - Q.subs(x, t**2)) == 0
    assert all(min(abs(r**2-2-s) for s in rs) < 1e-30 for r in rs)
    assert abs(sum(r**5 for r in rs)+15) < 1e-30
    p = [3, 0, 6]
    for kk in range(3):
        p.append(3*p[kk+1]-p[kk])
    assert p[3:] == [-3, 18, -15]
    cs = [2*cos(2*pi*j/9).evalf(40) for j in (1, 2, 4)]
    assert all(min(abs(r-cv) for cv in cs) < 1e-30 for r in rs)
    # C2
    w = (-1+sqrt(3)*I)/2
    for n in range(1, 25):
        val = simplify(expand(w**(2*n)+w**n+1))
        assert val == (3 if n % 3 == 0 else 0)
        rr = rem(x**(2*n)+x**n+1, x**2+x+1, x)
        assert rr == (3 if n % 3 == 0 else 0)
