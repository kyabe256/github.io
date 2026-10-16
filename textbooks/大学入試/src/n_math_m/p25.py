"""問題集 第25章 積分法（数学III）。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {25: {
"goal": r"置換積分・部分積分・部分分数分解を使い分け、定積分を正確に計算する。漸化式・対称性・評価（不等式）を使う定積分にも慣れる。",
"items": [
 {"lv": "A", "q": r"次の不定積分を求めよ。(1) $\displaystyle\int\left(x+\frac1x\right)^2dx$　(2) $\displaystyle\int\left(e^{2x}+\frac{1}{2x+1}\right)dx$　(3) $\displaystyle\int\sin^2x\,dx$",
  "a": r"(1) $\frac{x^3}{3}+2x-\frac1x+C$　(2) $\frac12e^{2x}+\frac12\log|2x+1|+C$　(3) $\frac x2-\frac{\sin2x}{4}+C$（$C$ は積分定数）",
  "s": r"(1) 展開して $\int\left(x^2+2+\frac{1}{x^2}\right)dx=\frac{x^3}{3}+2x-\frac1x+C$。<br>(2) $\int e^{ax}dx=\frac1ae^{ax}$、$\int\frac{dx}{ax+b}=\frac1a\log|ax+b|$。<br>(3) 半角の公式 $\sin^2x=\frac{1-\cos2x}{2}$ で次数を下げる。<br><b>ポイント</b>：$\sin^2x,\ \cos^2x$ は半角の公式、$\sin x\cos x$ は2倍角の公式で1次にしてから積分する。"},
 {"lv": "A", "q": r"次の定積分を求めよ。(1) $\displaystyle\int_0^1x(x^2+1)^3dx$　(2) $\displaystyle\int_0^{\frac\pi2}\sin x\cos^2x\,dx$　(3) $\displaystyle\int_1^e\frac{\log x}{x}dx$",
  "a": r"(1) $\frac{15}{8}$　(2) $\frac13$　(3) $\frac12$",
  "s": r"(1) $u=x^2+1$ とおくと $du=2x\,dx$、$x:0\to1$ で $u:1\to2$。$\int_1^2\frac{u^3}{2}du=\left[\frac{u^4}{8}\right]_1^2=\frac{16-1}{8}=\frac{15}{8}$。<br>(2) $u=\cos x$、$du=-\sin x\,dx$、$u:1\to0$。$\int_1^0(-u^2)du=\int_0^1u^2du=\frac13$。<br>(3) $u=\log x$、$du=\frac{dx}{x}$、$u:0\to1$。$\int_0^1u\,du=\frac12$。<br><b>ポイント</b>：「$f(g(x))g'(x)$」の形を見つけたら $u=g(x)$ とおく。定積分の置換では積分区間も変える。"},
 {"lv": "A", "q": r"次の定積分を求めよ。(1) $\displaystyle\int_0^1xe^x\,dx$　(2) $\displaystyle\int_1^e\log x\,dx$　(3) $\displaystyle\int_0^{\pi}x\sin x\,dx$",
  "a": r"(1) $1$　(2) $1$　(3) $\pi$",
  "s": r"(1) $\left[xe^x\right]_0^1-\int_0^1e^xdx=e-(e-1)=1$。<br>(2) $\log x=1\cdot\log x$ とみて $\left[x\log x\right]_1^e-\int_1^ex\cdot\frac1xdx=e-(e-1)=1$。<br>(3) $\left[-x\cos x\right]_0^\pi+\int_0^\pi\cos x\,dx=\pi+0=\pi$。<br><b>ポイント</b>：部分積分 $\int f g'=fg-\int f'g$ では、微分すると簡単になるほう（$x$、$\log x$）を $f$ に選ぶ。"},
 {"lv": "A", "q": r"次の定積分を求めよ。(1) $\displaystyle\int_0^1\frac{dx}{1+x^2}$　(2) $\displaystyle\int_0^{\sqrt3}\frac{dx}{\sqrt{4-x^2}}$",
  "a": r"(1) $\frac\pi4$　(2) $\frac\pi3$",
  "s": r"(1) $x=\tan\theta$ とおくと $dx=\frac{d\theta}{\cos^2\theta}$、$\theta:0\to\frac\pi4$。$1+\tan^2\theta=\frac{1}{\cos^2\theta}$ より $\int_0^{\frac\pi4}d\theta=\frac\pi4$。<br>(2) $x=2\sin\theta$ とおくと $dx=2\cos\theta\,d\theta$、$\theta:0\to\frac\pi3$。$0\leqq\theta\leqq\frac\pi3$ で $\cos\theta\gt0$ なので $\sqrt{4-4\sin^2\theta}=2\cos\theta$。$\int_0^{\frac\pi3}\frac{2\cos\theta}{2\cos\theta}d\theta=\frac\pi3$。<br><b>ポイント</b>：$\frac{1}{a^2+x^2}$ は $x=a\tan\theta$、$\sqrt{a^2-x^2}$ は $x=a\sin\theta$。根号を外すときに $\cos\theta$ の符号を確認する。"},
 {"lv": "B", "tag": "部分分数", "q": r"次の定積分を求めよ。(1) $\displaystyle\int_2^3\frac{dx}{x^2-1}$　(2) $\displaystyle\int_0^1\frac{x^2}{x+1}dx$",
  "a": r"(1) $\frac12\log\frac32$　(2) $\log2-\frac12$",
  "s": r"(1) $\frac{1}{x^2-1}=\frac12\left(\frac{1}{x-1}-\frac{1}{x+1}\right)$。$\frac12\left[\log\frac{x-1}{x+1}\right]_2^3=\frac12\left(\log\frac12-\log\frac13\right)=\frac12\log\frac32$。<br>(2) 割り算して $\frac{x^2}{x+1}=x-1+\frac{1}{x+1}$。$\left[\frac{x^2}{2}-x+\log(x+1)\right]_0^1=\frac12-1+\log2=\log2-\frac12$。<br><b>ポイント</b>：分数関数は、(分子の次数) $\geqq$ (分母の次数) なら割り算、そのあと分母を因数分解して部分分数に分ける。"},
 {"lv": "B", "tag": "部分積分2回", "q": r"$I=\displaystyle\int_0^{\pi}e^x\sin x\,dx$ を求めよ。",
  "a": r"$\frac{e^\pi+1}{2}$",
  "s": r"部分積分で $I=\left[e^x\sin x\right]_0^\pi-\int_0^\pi e^x\cos x\,dx=-\int_0^\pi e^x\cos x\,dx$。<br>もう一度部分積分して $\int_0^\pi e^x\cos x\,dx=\left[e^x\cos x\right]_0^\pi+\int_0^\pi e^x\sin x\,dx=(-e^\pi-1)+I$。<br>よって $I=e^\pi+1-I$、$I=\frac{e^\pi+1}{2}$。<br>（別解）$\{e^x(\sin x-\cos x)\}'=2e^x\sin x$ より $I=\frac12\left[e^x(\sin x-\cos x)\right]_0^\pi=\frac12(e^\pi+1)$。<br><b>ポイント</b>：$e^x\sin x$ 型は2回の部分積分でもとの積分 $I$ が再び現れるので、$I$ についての方程式として解く。"},
 {"lv": "B", "tag": "定積分と微分", "q": r"(1) $F(x)=\displaystyle\int_0^x(x-t)e^t\,dt$ とする。$F'(x)$ と $F(x)$ を求めよ。(2) $x\gt0$ のとき、$\dfrac{d}{dx}\displaystyle\int_x^{2x}\log t\,dt$ を求めよ。",
  "a": r"(1) $F'(x)=e^x-1$、$F(x)=e^x-x-1$　(2) $\log4x$",
  "s": r"(1) $x$ は積分変数 $t$ と無関係なので外に出す：$F(x)=x\int_0^xe^tdt-\int_0^xte^tdt$。積の微分と $\frac{d}{dx}\int_0^xg(t)dt=g(x)$ より $F'(x)=\int_0^xe^tdt+xe^x-xe^x=e^x-1$。$F(0)=0$ なので $F(x)=\int_0^x(e^s-1)ds=e^x-x-1$。<br>(2) $\log t$ の原始関数を $G(t)$ とすると $\int_x^{2x}\log t\,dt=G(2x)-G(x)$。微分して $2\log2x-\log x=\log\frac{4x^2}{x}=\log4x$。<br><b>ポイント</b>：被積分関数に $x$ が含まれるときは、まず $x$ を積分の外に出す。上端・下端が $x$ の関数なら合成関数の微分：$\frac{d}{dx}\int_{a}^{g(x)}f(t)dt=f(g(x))g'(x)$。"},
 {"lv": "B", "tag": "漸化式", "q": r"$I_n=\displaystyle\int_0^{\frac\pi2}\sin^nx\,dx\ (n=0,1,2,\cdots)$ とする。(1) $n\geqq2$ のとき $I_n=\dfrac{n-1}{n}I_{n-2}$ を示せ。(2) $I_4,\ I_5$ を求めよ。",
  "a": r"(2) $I_4=\frac{3}{16}\pi,\ I_5=\frac{8}{15}$",
  "s": r"(1) $\sin^nx=\sin^{n-1}x\cdot\sin x$ とみて部分積分：$I_n=\left[-\sin^{n-1}x\cos x\right]_0^{\frac\pi2}+(n-1)\int_0^{\frac\pi2}\sin^{n-2}x\cos^2x\,dx$。<br>第1項は $0$。$\cos^2x=1-\sin^2x$ より $I_n=(n-1)(I_{n-2}-I_n)$、$nI_n=(n-1)I_{n-2}$。■<br>(2) $I_0=\frac\pi2,\ I_1=1$。$I_4=\frac34\cdot\frac12\cdot\frac\pi2=\frac{3}{16}\pi$、$I_5=\frac45\cdot\frac23\cdot1=\frac{8}{15}$。<br><b>ポイント</b>：$\sin^n x$ の積分は、1つだけ $\sin x$ を残して部分積分し、$\cos^2x=1-\sin^2x$ でもとの形に戻す。"},
 {"lv": "B", "tag": "対称性", "q": r"$I=\displaystyle\int_0^{\frac\pi2}\frac{\sin x}{\sin x+\cos x}dx$、$J=\displaystyle\int_0^{\frac\pi2}\frac{\cos x}{\sin x+\cos x}dx$ とする。$I=J$ を示し、$I$ の値を求めよ。",
  "a": r"$I=\frac\pi4$",
  "s": r"$I$ で $x=\frac\pi2-t$ とおくと $dx=-dt$、$x:0\to\frac\pi2$ で $t:\frac\pi2\to0$。$\sin x=\cos t,\ \cos x=\sin t$ より $I=\int_{\frac\pi2}^0\frac{\cos t}{\cos t+\sin t}(-dt)=\int_0^{\frac\pi2}\frac{\cos t}{\sin t+\cos t}dt=J$。■<br>一方 $I+J=\int_0^{\frac\pi2}1\,dx=\frac\pi2$ なので $I=\frac\pi4$。<br><b>ポイント</b>：直接積分しにくいときは、$x=a+b-t$ の置換（区間の折り返し）で「相方」の積分を作り、和や差をとる。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"(1) 連続関数 $f(x)$ について、$\displaystyle\int_0^\pi xf(\sin x)\,dx=\frac\pi2\int_0^\pi f(\sin x)\,dx$ を示せ。<br>(2) $\displaystyle\int_0^\pi\frac{x\sin x}{1+\cos^2x}dx$ を求めよ。",
  "a": r"(2) $\frac{\pi^2}{4}$",
  "s": r"(1) $K=\int_0^\pi xf(\sin x)dx$ で $x=\pi-t$ とおくと、$\sin(\pi-t)=\sin t$ より $K=\int_0^\pi(\pi-t)f(\sin t)dt=\pi\int_0^\pi f(\sin t)dt-K$。よって $K=\frac\pi2\int_0^\pi f(\sin x)dx$。■<br>(2) $\frac{\sin x}{1+\cos^2x}=\frac{\sin x}{2-\sin^2x}$ は $\sin x$ の関数なので、(1)より 与式 $=\frac\pi2\int_0^\pi\frac{\sin x}{1+\cos^2x}dx$。<br>$u=\cos x$ とおくと $du=-\sin x\,dx$、$u:1\to-1$ で $\int_{-1}^{1}\frac{du}{1+u^2}$。さらに $u=\tan\theta$ とおくと $\int_{-\frac\pi4}^{\frac\pi4}d\theta=\frac\pi2$。<br>よって 与式 $=\frac\pi2\cdot\frac\pi2=\frac{\pi^2}{4}$。<br><b>ポイント</b>：$x$ が掛かっていて原始関数が求まらない積分も、$x\to\pi-x$ の置換で $x$ を消せる。置換を2段階（$\cos x\to u\to\tan\theta$）重ねる構成も入試頻出。"},
 {"lv": "C", "tag": "評価と極限", "q": r"$R_n=\displaystyle\int_0^1\frac{x^n}{1+x}dx\ (n=1,2,3,\cdots)$ とする。<br>(1) $0\leqq R_n\leqq\dfrac{1}{n+1}$ を示せ。<br>(2) $\displaystyle\sum_{k=1}^{n}\frac{(-1)^{k-1}}{k}=\log2+(-1)^{n-1}R_n$ を示せ。<br>(3) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}\frac{(-1)^{k-1}}{k}$ を求めよ。",
  "a": r"(3) $\log2$",
  "s": r"(1) $0\leqq x\leqq1$ で $0\leqq\frac{x^n}{1+x}\leqq x^n$。積分して $0\leqq R_n\leqq\int_0^1x^ndx=\frac{1}{n+1}$。■<br>(2) 等比数列の和の公式より $1-x+x^2-\cdots+(-x)^{n-1}=\frac{1-(-x)^n}{1+x}$、すなわち $\frac{1}{1+x}=\sum_{k=1}^{n}(-x)^{k-1}+\frac{(-x)^n}{1+x}$。<br>$0$ から $1$ まで積分すると $\log2=\sum_{k=1}^{n}\frac{(-1)^{k-1}}{k}+(-1)^nR_n$。移項して示された。■<br>(3) (1) とはさみうちの原理より $R_n\to0$。(2) より $\lim_{n\to\infty}\sum_{k=1}^n\frac{(-1)^{k-1}}{k}=\log2$。<br><b>ポイント</b>：無限級数の和を、定積分の「余り」の評価で求める典型。被積分関数を簡単な関数ではさんで積分すると、定積分の大きさが評価できる。"},
]}}

def verify():
    x, t, C = symbols("x t C", real=True)
    xp = symbols("xp", positive=True)
    eq = lambda u, v: simplify(u-v) == 0
    assert eq(diff(xp**3/3+2*xp-1/xp, xp), (xp+1/xp)**2)
    assert eq(diff(exp(2*xp)/2+log(2*xp+1)/2, xp), exp(2*xp)+1/(2*xp+1))
    assert eq(diff(x/2-sin(2*x)/4, x), sin(x)**2)
    # A2
    assert integrate(x*(x**2+1)**3, (x, 0, 1)) == Rational(15, 8)
    assert integrate(sin(x)*cos(x)**2, (x, 0, pi/2)) == Rational(1, 3)
    assert integrate(log(xp)/xp, (xp, 1, E)) == Rational(1, 2)
    # A3
    assert integrate(x*exp(x), (x, 0, 1)) == 1 and integrate(log(xp), (xp, 1, E)) == 1
    assert integrate(x*sin(x), (x, 0, pi)) == pi
    # A4
    assert integrate(1/(1+x**2), (x, 0, 1)) == pi/4
    assert integrate(1/sqrt(4-x**2), (x, 0, sqrt(3))) == pi/3
    # B1
    assert eq(integrate(1/(x**2-1), (x, 2, 3)), log(Rational(3, 2))/2)
    assert eq(integrate(x**2/(x+1), (x, 0, 1)), log(2)-Rational(1, 2))
    assert eq(x**2/(x+1), x-1+1/(x+1))
    # B2
    assert eq(integrate(exp(x)*sin(x), (x, 0, pi)), (exp(pi)+1)/2)
    assert eq(diff(exp(x)*(sin(x)-cos(x)), x), 2*exp(x)*sin(x))
    # B3
    F = integrate((x-t)*exp(t), (t, 0, x))
    assert eq(F, exp(x)-x-1) and eq(diff(F, x), exp(x)-1)
    G = integrate(log(t), (t, xp, 2*xp))
    assert eq(diff(G, xp), log(4*xp))
    # B4
    I = [pi/2, Integer(1)]
    for n in range(2, 8):
        I.append(Rational(n-1, n)*I[n-2])
    for n in range(0, 8):
        assert eq(integrate(sin(x)**n, (x, 0, pi/2)), I[n])
    assert I[4] == 3*pi/16 and I[5] == Rational(8, 15)
    # B5
    import mpmath
    Iv = mpmath.quad(lambda u: mpmath.sin(u)/(mpmath.sin(u)+mpmath.cos(u)), [0, mpmath.pi/2])
    Jv = mpmath.quad(lambda u: mpmath.cos(u)/(mpmath.sin(u)+mpmath.cos(u)), [0, mpmath.pi/2])
    assert abs(Iv-mpmath.pi/4) < 1e-12 and abs(Jv-Iv) < 1e-12
    # C1
    K = mpmath.quad(lambda u: u*mpmath.sin(u)/(1+mpmath.cos(u)**2), [0, mpmath.pi])
    assert abs(K-mpmath.pi**2/4) < 1e-12
    assert integrate(1/(1+t**2), (t, -1, 1)) == pi/2
    assert eq(sin(x)/(1+cos(x)**2), sin(x)/(2-sin(x)**2))
    # (1) の等式を別の f で数値確認
    f = lambda s: mpmath.exp(s)+s**3
    L = mpmath.quad(lambda u: u*f(mpmath.sin(u)), [0, mpmath.pi]); R = mpmath.pi/2*mpmath.quad(lambda u: f(mpmath.sin(u)), [0, mpmath.pi])
    assert abs(L-R) < 1e-12
    # C2
    n = symbols("n", integer=True, positive=True)
    for nv in range(1, 9):
        Rn = integrate(x**nv/(1+x), (x, 0, 1))
        assert 0 <= Rn <= Rational(1, nv+1)
        S = sum(Rational((-1)**(k-1), k) for k in range(1, nv+1))
        assert eq(S, log(2)+(-1)**(nv-1)*Rn)
    assert eq(summation((-1)**(n-1)/n, (n, 1, oo)), log(2))
