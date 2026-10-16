"""問題集 第23章 微分法（数学III）。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {23: {
"goal": r"積・商・合成関数の微分と、三角・指数・対数関数の導関数を速く正確に。微分係数の定義に戻る問題（微分可能性・極限・関数方程式）も扱えるようにする。",
"items": [
 {"lv": "A", "q": r"次の関数を微分せよ。(1) $y=(x^2+1)(2x-3)$　(2) $y=\dfrac{x}{x^2+1}$　(3) $y=\sqrt{2x+1}$",
  "a": r"(1) $y'=6x^2-6x+2$　(2) $y'=\frac{1-x^2}{(x^2+1)^2}$　(3) $y'=\frac{1}{\sqrt{2x+1}}$",
  "s": r"(1) 積の微分：$2x(2x-3)+(x^2+1)\cdot2=6x^2-6x+2$。<br>(2) 商の微分：$\frac{1\cdot(x^2+1)-x\cdot2x}{(x^2+1)^2}=\frac{1-x^2}{(x^2+1)^2}$。<br>(3) 合成関数の微分：$\frac{1}{2\sqrt{2x+1}}\cdot2=\frac{1}{\sqrt{2x+1}}$。<br><b>ポイント</b>：$\left(\frac fg\right)'=\frac{f'g-fg'}{g^2}$（分子の順番に注意）。合成関数は「外の微分 × 中の微分」。"},
 {"lv": "A", "q": r"次の関数を微分せよ。(1) $y=\sin^2x$　(2) $y=e^{-x}\cos x$　(3) $y=\log(x^2+1)$　(4) $y=x\log x$",
  "a": r"(1) $\sin2x$　(2) $-e^{-x}(\sin x+\cos x)$　(3) $\frac{2x}{x^2+1}$　(4) $\log x+1$",
  "s": r"(1) $2\sin x\cos x=\sin2x$。<br>(2) $-e^{-x}\cos x+e^{-x}(-\sin x)=-e^{-x}(\sin x+\cos x)$。<br>(3) $\frac{(x^2+1)'}{x^2+1}=\frac{2x}{x^2+1}$。<br>(4) $1\cdot\log x+x\cdot\frac1x=\log x+1$。<br><b>ポイント</b>：$(\log f(x))'=\frac{f'(x)}{f(x)}$、$(e^{f(x)})'=f'(x)e^{f(x)}$。この本では $\log$ は自然対数（底 $e$）を表す。"},
 {"lv": "A", "q": r"対数微分法を用いて、次の関数を微分せよ。(1) $y=x^x\ (x\gt0)$　(2) $y=\sqrt{\dfrac{x+1}{x-1}}\ (x\gt1)$",
  "a": r"(1) $y'=x^x(\log x+1)$　(2) $y'=-\frac{1}{(x-1)\sqrt{x^2-1}}$",
  "s": r"(1) $y\gt0$ なので両辺の対数をとって $\log y=x\log x$。両辺を $x$ で微分して $\frac{y'}{y}=\log x+1$、$y'=x^x(\log x+1)$。<br>(2) $\log y=\frac12\{\log(x+1)-\log(x-1)\}$。微分して $\frac{y'}{y}=\frac12\left(\frac{1}{x+1}-\frac{1}{x-1}\right)=-\frac{1}{x^2-1}$。<br>$y'=-\frac{1}{x^2-1}\sqrt{\frac{x+1}{x-1}}=-\frac{\sqrt{x+1}}{(x-1)(x+1)\sqrt{x-1}}=-\frac{1}{(x-1)\sqrt{x^2-1}}$。<br><b>ポイント</b>：$x^x$ のように底にも指数にも $x$ がある関数や、積・商・累乗根が重なった関数は、対数をとってから微分する。"},
 {"lv": "A", "q": r"(1) $x=t^2,\ y=t^3$ のとき、$\dfrac{dy}{dx}$ を $t$ で表せ（$t\neq0$）。(2) 円 $x^2+y^2=25$ 上の点 $(3,\ 4)$ における接線の方程式を、$\dfrac{dy}{dx}$ を求めて導け。",
  "a": r"(1) $\frac{3t}{2}$　(2) $3x+4y=25$",
  "s": r"(1) $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}=\frac{3t^2}{2t}=\frac{3t}{2}$。<br>(2) 両辺を $x$ で微分すると $2x+2y\frac{dy}{dx}=0$、$y\neq0$ で $\frac{dy}{dx}=-\frac xy$。点 $(3,4)$ で $-\frac34$。接線は $y-4=-\frac34(x-3)$、すなわち $3x+4y=25$。<br><b>ポイント</b>：陰関数の微分では、$y$ を $x$ の関数とみて $(y^2)'=2y\,y'$ とする。"},
 {"lv": "B", "tag": "微分可能性", "q": r"関数 $f(x)=\begin{cases}ax^2+b & (x\leqq1)\\ \log x & (x\gt1)\end{cases}$ が $x=1$ で微分可能となるように、定数 $a,\ b$ の値を定めよ。",
  "a": r"$a=\frac12,\ b=-\frac12$",
  "s": r"微分可能なら連続なので、$\lim_{x\to1+0}\log x=0=f(1)=a+b$。<br>微分可能 ⇔ 左側・右側の微分係数が一致：<br>左側 $\lim_{h\to-0}\frac{a(1+h)^2+b-(a+b)}{h}=\lim_{h\to-0}(2a+ah)=2a$、<br>右側 $\lim_{h\to+0}\frac{\log(1+h)-(a+b)}{h}=\lim_{h\to+0}\frac{\log(1+h)}{h}=1$（$a+b=0$ を使った）。<br>$2a=1$ より $a=\frac12$、$b=-\frac12$。<br><b>ポイント</b>：つなぎ目での微分可能性は「① 連続（値がつながる）」と「② 左右の微分係数が等しい（傾きがつながる）」の2条件。①を先に使わないと右側の極限が有限にならない。"},
 {"lv": "B", "tag": "定義の利用", "q": r"関数 $f(x)$ は $x=a$ で微分可能とする。次の極限を $a,\ f(a),\ f'(a)$ で表せ。<br>(1) $\displaystyle\lim_{h\to0}\frac{f(a+2h)-f(a-h)}{h}$　(2) $\displaystyle\lim_{x\to a}\frac{x^2f(a)-a^2f(x)}{x-a}$",
  "a": r"(1) $3f'(a)$　(2) $2af(a)-a^2f'(a)$",
  "s": r"(1) $f(a)$ を引いて足す：$\frac{f(a+2h)-f(a)}{2h}\cdot2+\frac{f(a-h)-f(a)}{-h}\cdot1\to2f'(a)+f'(a)=3f'(a)$。<br>(2) 分子 $=x^2f(a)-a^2f(a)+a^2f(a)-a^2f(x)=(x^2-a^2)f(a)-a^2\{f(x)-f(a)\}$。<br>$x-a$ で割ると $(x+a)f(a)-a^2\cdot\frac{f(x)-f(a)}{x-a}\to2af(a)-a^2f'(a)$。<br><b>ポイント</b>：微分係数の定義 $\frac{f(a+\square)-f(a)}{\square}$ の形（$\square$ がそろっていること）を、$f(a)$ を引いて足す工夫で作る。"},
 {"lv": "B", "tag": "逆関数の微分", "q": r"(1) $y=\sin x\ \left(-\frac\pi2\lt x\lt\frac\pi2\right)$ の逆関数を $y=g(x)$ とするとき、$g'(x)$ を $x$ の式で表せ。(2) $f(x)=x^3+x+1$ の逆関数を $h(x)$ とするとき、$h'(3)$ を求めよ。",
  "a": r"(1) $g'(x)=\frac{1}{\sqrt{1-x^2}}\ (-1\lt x\lt1)$　(2) $h'(3)=\frac14$",
  "s": r"(1) $y=g(x)$ ⇔ $x=\sin y\ \left(-\frac\pi2\lt y\lt\frac\pi2\right)$。$\frac{dx}{dy}=\cos y\gt0$ で、$\cos y=\sqrt{1-\sin^2y}=\sqrt{1-x^2}$。$\frac{dy}{dx}=\frac{1}{dx/dy}=\frac{1}{\sqrt{1-x^2}}$。<br>(2) $f'(x)=3x^2+1\gt0$ で $f$ は増加し、逆関数をもつ。$f(1)=3$ より $h(3)=1$。$h'(3)=\frac{1}{f'(h(3))}=\frac{1}{f'(1)}=\frac14$。<br><b>ポイント</b>：$\frac{dy}{dx}=\frac{1}{dx/dy}$。逆関数の式が求められなくても、対応する点さえ分かれば微分係数は求まる。$\cos y\gt0$ となる範囲であることを確認して根号を外す。"},
 {"lv": "B", "tag": "高次導関数", "q": r"(1) $y=e^x\sin x$ のとき、$y''-2y'+2y=0$ が成り立つことを示せ。(2) $y=xe^x$ の第 $n$ 次導関数を求めよ。",
  "a": r"(2) $y^{(n)}=(x+n)e^x$",
  "s": r"(1) $y'=e^x\sin x+e^x\cos x=e^x(\sin x+\cos x)$、$y''=e^x(\sin x+\cos x)+e^x(\cos x-\sin x)=2e^x\cos x$。<br>$y''-2y'+2y=2e^x\cos x-2e^x(\sin x+\cos x)+2e^x\sin x=0$。■<br>(2) $y'=(x+1)e^x,\ y''=(x+2)e^x$ から $y^{(n)}=(x+n)e^x$ と推測し、帰納法で示す。$n=1$ で成立。$y^{(k)}=(x+k)e^x$ なら $y^{(k+1)}=e^x+(x+k)e^x=(x+k+1)e^x$。■<br><b>ポイント</b>：第 $n$ 次導関数は、いくつか計算して形を予想し、数学的帰納法で証明する。"},
 {"lv": "B", "tag": "接線", "q": r"(1) 原点から曲線 $y=\log x$ に引いた接線の方程式を求めよ。(2) 曲線 $y=ax^2$ と曲線 $y=\log x$ が接する（共有点をもち、その点で共通の接線をもつ）ような正の定数 $a$ の値と、接点の座標を求めよ。",
  "a": r"(1) $y=\frac1ex$　(2) $a=\frac{1}{2e}$、接点 $\left(\sqrt e,\ \frac12\right)$",
  "s": r"(1) 接点を $(t,\ \log t)$ とすると接線は $y=\frac1t(x-t)+\log t$。原点を通るので $0=-1+\log t$、$t=e$。接線は $y=\frac1ex$。<br>(2) 接点の $x$ 座標を $t\ (t\gt0)$ とすると、$at^2=\log t$ かつ $2at=\frac1t$。2つ目から $at^2=\frac12$、よって $\log t=\frac12$、$t=\sqrt e$、$a=\frac{1}{2t^2}=\frac{1}{2e}$。接点は $\left(\sqrt e,\ \frac12\right)$。<br><b>ポイント</b>：2曲線 $y=f(x),\ y=g(x)$ が $x=t$ で接する ⇔ $f(t)=g(t)$ かつ $f'(t)=g'(t)$。"},
 {"lv": "C", "tag": "関数方程式", "q": r"関数 $f(x)$ はすべての実数 $x,\ y$ について $f(x+y)=f(x)+f(y)+2xy$ を満たし、$x=0$ で微分可能で $f'(0)=1$ である。(1) $f(0)$ を求めよ。(2) $f(x)$ はすべての $x$ で微分可能であることを示し、$f'(x)$ を求めよ。(3) $f(x)$ を求めよ。",
  "a": r"(1) $0$　(2) $f'(x)=2x+1$　(3) $f(x)=x^2+x$",
  "s": r"(1) $x=y=0$ とすると $f(0)=2f(0)$ より $f(0)=0$。<br>(2) $\frac{f(x+h)-f(x)}{h}=\frac{f(h)+2xh}{h}=\frac{f(h)-f(0)}{h}+2x\to f'(0)+2x=1+2x\ (h\to0)$。極限が存在するので $f(x)$ は任意の $x$ で微分可能で、$f'(x)=2x+1$。■<br>(3) $f(x)=x^2+x+C$ と表され、$f(0)=0$ より $C=0$。$f(x)=x^2+x$（実際に $f(x+y)=f(x)+f(y)+2xy$ を満たす）。<br><b>ポイント</b>：関数方程式では、まず特別な値（$x=y=0$ など）を代入する。一般の点での微分可能性は、定義式に関数方程式を使って $x=0$ での微分係数に帰着させる。"},
 {"lv": "C", "tag": "帰納法", "q": r"$f(x)=e^x\sin x$ とする。(1) すべての自然数 $n$ について $f^{(n)}(x)=(\sqrt2)^ne^x\sin\left(x+\dfrac{n\pi}{4}\right)$ が成り立つことを示せ。(2) $f^{(8)}(0)$ と $f^{(10)}(0)$ を求めよ。",
  "a": r"(2) $f^{(8)}(0)=0,\ f^{(10)}(0)=32$",
  "s": r"(1) 数学的帰納法。$n=1$：$f'(x)=e^x(\sin x+\cos x)=\sqrt2e^x\sin\left(x+\frac\pi4\right)$ で成立（三角関数の合成）。<br>$n=k$ で成立すると仮定すると、<br>$f^{(k+1)}(x)=(\sqrt2)^k\left\{e^x\sin\left(x+\frac{k\pi}{4}\right)+e^x\cos\left(x+\frac{k\pi}{4}\right)\right\}=(\sqrt2)^ke^x\cdot\sqrt2\sin\left(x+\frac{k\pi}{4}+\frac\pi4\right)=(\sqrt2)^{k+1}e^x\sin\left(x+\frac{(k+1)\pi}{4}\right)$。<br>よって $n=k+1$ でも成立。■<br>(2) $f^{(n)}(0)=(\sqrt2)^n\sin\frac{n\pi}{4}$。$f^{(8)}(0)=16\sin2\pi=0$、$f^{(10)}(0)=32\sin\frac{5\pi}{2}=32$。<br><b>ポイント</b>：$\sin\theta+\cos\theta=\sqrt2\sin\left(\theta+\frac\pi4\right)$ により、「微分する」ことが「$\sqrt2$ 倍して $\frac\pi4$ 進める」ことになる。"},
]}}

def verify():
    x, t, a, b, h = symbols("x t a b h", real=True)
    eq = lambda u, v: simplify(u-v) == 0
    assert eq(diff((x**2+1)*(2*x-3), x), 6*x**2-6*x+2)
    assert eq(diff(x/(x**2+1), x), (1-x**2)/(x**2+1)**2)
    assert eq(diff(sqrt(2*x+1), x), 1/sqrt(2*x+1))
    assert eq(diff(sin(x)**2, x), sin(2*x)) and eq(diff(exp(-x)*cos(x), x), -exp(-x)*(sin(x)+cos(x)))
    assert eq(diff(log(x**2+1), x), 2*x/(x**2+1)) and eq(diff(x*log(x), x), log(x)+1)
    xp = symbols("xp", positive=True)
    assert eq(diff(xp**xp, xp), xp**xp*(log(xp)+1))
    x1 = symbols("x1")
    yy = sqrt((x1+1)/(x1-1))
    for v in [2, 3, Rational(7, 2), 10]:
        assert eq(diff(yy, x1).subs(x1, v), (-1/((x1-1)*sqrt(x1**2-1))).subs(x1, v))
    # A4
    assert eq(diff(t**3, t)/diff(t**2, t), 3*t/2)
    assert expand(4-Rational(3, 4)*(x-3) - (25-3*x)/4) == 0
    # B1
    sol = solve([a+b, 2*a-1], [a, b])
    assert sol == {a: Rational(1, 2), b: Rational(-1, 2)}
    f1 = Rational(1, 2)*x**2-Rational(1, 2)
    assert limit((f1.subs(x, 1+h)-f1.subs(x, 1))/h, h, 0, "-") == 1
    assert limit((log(1+h)-f1.subs(x, 1))/h, h, 0, "+") == 1
    # B2
    for f in [sin(x)*x+x**3, exp(2*x), log(x+5)]:
        av = Rational(1, 3)
        L1 = limit((f.subs(x, av+2*h)-f.subs(x, av-h))/h, h, 0)
        assert eq(L1, 3*diff(f, x).subs(x, av))
        y = symbols("y")
        L2 = limit((y**2*f.subs(x, av)-av**2*f.subs(x, y))/(y-av), y, av)
        assert eq(L2, 2*av*f.subs(x, av)-av**2*diff(f, x).subs(x, av))
    # B3
    assert eq(diff(asin(x), x), 1/sqrt(1-x**2))
    F = x**3+x+1
    assert F.subs(x, 1) == 3 and 1/diff(F, x).subs(x, 1) == Rational(1, 4)
    # B4
    y = exp(x)*sin(x)
    assert eq(diff(y, x, 2)-2*diff(y, x)+2*y, 0) and eq(diff(y, x, 2), 2*exp(x)*cos(x))
    for n in range(1, 8):
        assert eq(diff(x*exp(x), x, n), (x+n)*exp(x))
    # B5
    tt = symbols("tt", positive=True)
    assert solve(-1+log(tt), tt) == [E]
    sol = solve([a*tt**2-log(tt), 2*a*tt-1/tt], [a, tt], dict=True)
    assert sol == [{a: 1/(2*E), tt: sqrt(E)}]
    # C1
    f = x**2+x
    y = symbols("y")
    assert expand(f.subs(x, x+y) - (f+f.subs(x, y)+2*x*y)) == 0 and diff(f, x).subs(x, 0) == 1
    # C2
    for n in range(1, 13):
        assert eq(diff(exp(x)*sin(x), x, n), sqrt(2)**n*exp(x)*sin(x+n*pi/4))
    assert diff(exp(x)*sin(x), x, 8).subs(x, 0) == 0 and diff(exp(x)*sin(x), x, 10).subs(x, 0) == 32
