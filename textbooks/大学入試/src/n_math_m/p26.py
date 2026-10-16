"""問題集 第26章 積分法の応用。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {26: {
"goal": r"面積・体積・曲線の長さを、図をかいて正しい積分の式に立てる。区分求積法と、面積の比較による不等式の評価も身につける。",
"items": [
 {"lv": "A", "q": r"次の図形の面積を求めよ。(1) 曲線 $y=\sin x\ (0\leqq x\leqq\pi)$ と $x$ 軸で囲まれた図形　(2) 曲線 $y=\log x$、$x$ 軸、直線 $x=e$ で囲まれた図形",
  "a": r"(1) $2$　(2) $1$",
  "s": r"(1) $\int_0^\pi\sin x\,dx=\left[-\cos x\right]_0^\pi=1+1=2$。<br>(2) $1\leqq x\leqq e$ で $\log x\geqq0$。$\int_1^e\log x\,dx=\left[x\log x-x\right]_1^e=0-(-1)=1$。<br><b>ポイント</b>：曲線と $x$ 軸の交点（積分区間の端）を先に求め、区間内での上下関係を確かめてから積分する。"},
 {"lv": "A", "q": r"次の図形を $x$ 軸のまわりに1回転してできる立体の体積を求めよ。(1) 曲線 $y=\sqrt x$、$x$ 軸、直線 $x=4$ で囲まれた図形　(2) 曲線 $y=\sin x\ (0\leqq x\leqq\pi)$ と $x$ 軸で囲まれた図形",
  "a": r"(1) $8\pi$　(2) $\frac{\pi^2}{2}$",
  "s": r"(1) $V=\pi\int_0^4(\sqrt x)^2dx=\pi\left[\frac{x^2}{2}\right]_0^4=8\pi$。<br>(2) $V=\pi\int_0^\pi\sin^2x\,dx=\pi\int_0^\pi\frac{1-\cos2x}{2}dx=\pi\cdot\frac\pi2=\frac{\pi^2}{2}$。<br><b>ポイント</b>：$x$ 軸回転の体積は $V=\pi\int_a^by^2dx$（断面の円の面積 $\pi y^2$ を積分）。"},
 {"lv": "A", "q": r"曲線 $y=\dfrac23x^{\frac32}\ (0\leqq x\leqq3)$ の長さを求めよ。",
  "a": r"$\frac{14}{3}$",
  "s": r"$y'=x^{\frac12}$ より $1+(y')^2=1+x$。$L=\int_0^3\sqrt{1+x}\,dx=\left[\frac23(1+x)^{\frac32}\right]_0^3=\frac23(8-1)=\frac{14}{3}$。<br><b>ポイント</b>：曲線の長さは $L=\int_a^b\sqrt{1+\{f'(x)\}^2}dx$。根号の中がきれいになるように作られた問題が多い。"},
 {"lv": "A", "q": r"次の極限を求めよ。(1) $\displaystyle\lim_{n\to\infty}\frac1n\sum_{k=1}^{n}\left(\frac kn\right)^2$　(2) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}\frac{n}{n^2+k^2}$　(3) $\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}\frac{1}{n+k}$",
  "a": r"(1) $\frac13$　(2) $\frac\pi4$　(3) $\log2$",
  "s": r"区分求積法 $\displaystyle\lim_{n\to\infty}\frac1n\sum_{k=1}^nf\left(\frac kn\right)=\int_0^1f(x)dx$ を使う。<br>(1) $\int_0^1x^2dx=\frac13$。<br>(2) $\frac{n}{n^2+k^2}=\frac1n\cdot\frac{1}{1+\left(\frac kn\right)^2}$ より $\int_0^1\frac{dx}{1+x^2}=\frac\pi4$（$x=\tan\theta$ で置換）。<br>(3) $\frac{1}{n+k}=\frac1n\cdot\frac{1}{1+\frac kn}$ より $\int_0^1\frac{dx}{1+x}=\log2$。<br><b>ポイント</b>：$\frac1n$ をくくり出し、残りを $\frac kn$ だけの式にする。"},
 {"lv": "B", "tag": "2曲線の間", "q": r"2曲線 $y=\sin x,\ y=\cos x$ の $\frac\pi4\leqq x\leqq\frac54\pi$ の部分で囲まれた図形の面積を求めよ。",
  "a": r"$2\sqrt2$",
  "s": r"$\sin x=\cos x$ となるのは $x=\frac\pi4,\ \frac54\pi$ で、その間では $\sin x\geqq\cos x$。<br>$S=\int_{\frac\pi4}^{\frac54\pi}(\sin x-\cos x)dx=\left[-\cos x-\sin x\right]_{\frac\pi4}^{\frac54\pi}=\left(\frac{\sqrt2}{2}+\frac{\sqrt2}{2}\right)-\left(-\frac{\sqrt2}{2}-\frac{\sqrt2}{2}\right)=2\sqrt2$。<br><b>ポイント</b>：2曲線の間の面積は $\int(\text{上}-\text{下})dx$。$x$ 軸の上下は関係ない。"},
 {"lv": "B", "tag": "接線と面積", "q": r"原点から曲線 $C:\ y=\log x$ に引いた接線を $\ell$ とする。$C$、$\ell$ および $x$ 軸で囲まれた図形の面積を求めよ。",
  "a": r"$\frac e2-1$",
  "s": r"接点を $(t,\ \log t)$ とすると接線 $y=\frac1t(x-t)+\log t$ が原点を通るので $\log t=1$、$t=e$。$\ell:\ y=\frac xe$、接点 $(e,\ 1)$。<svg class='fig' width='210' height='135' viewBox='0 0 210 135'><polygon points='25,95 160.9,45 160.9,45.0 158.1,46.1 155.2,47.2 152.3,48.3 149.5,49.4 146.6,50.6 143.7,51.8 140.9,53.0 138.0,54.2 135.1,55.5 132.3,56.8 129.4,58.2 126.5,59.6 123.7,61.0 120.8,62.5 118.0,64.0 115.1,65.6 112.2,67.2 109.4,68.8 106.5,70.6 103.6,72.4 100.8,74.2 97.9,76.1 95.0,78.1 92.2,80.2 89.3,82.4 86.5,84.7 83.6,87.1 80.7,89.6 77.9,92.2 75.0,95.0' fill='#cfe0ff' stroke='none'/><line x1='4' y1='95' x2='206' y2='95' stroke='#555'/><line x1='25' y1='131' x2='25' y2='4' stroke='#555'/><text x='198' y='108' font-size='11'>x</text><text x='30' y='13' font-size='11'>y</text><polyline points='50.0,129.7 52.5,124.9 55.0,120.5 57.5,116.5 60.0,112.8 62.5,109.4 65.0,106.2 67.5,103.1 70.0,100.3 72.5,97.6 75.0,95.0 77.5,92.6 80.0,90.2 82.5,88.0 85.0,85.9 87.5,83.8 90.0,81.9 92.5,80.0 95.0,78.2 97.5,76.4 100.0,74.7 102.5,73.1 105.0,71.5 107.5,70.0 110.0,68.5 112.5,67.0 115.0,65.6 117.5,64.2 120.0,62.9 122.5,61.6 125.0,60.3 127.5,59.1 130.0,57.9 132.5,56.7 135.0,55.6 137.5,54.5 140.0,53.4 142.5,52.3 145.0,51.2 147.5,50.2 150.0,49.2 152.5,48.2 155.0,47.2 157.5,46.3 160.0,45.3 162.5,44.4 165.0,43.5 167.5,42.6 170.0,41.8 172.5,40.9 175.0,40.1 177.5,39.2 180.0,38.4 182.5,37.6 185.0,36.8 187.5,36.1 190.0,35.3 192.5,34.6 195.0,33.8 197.5,33.1 200.0,32.4 202.5,31.7 205.0,31.0 207.5,30.3' fill='none' stroke='#1f3f8f' stroke-width='1.5'/><line x1='15.0' y1='98.7' x2='200.0' y2='30.6' stroke='#c0392b' stroke-width='1.3'/><circle cx='160.9' cy='45' r='2.2' fill='#1e1e1e'/><text x='126.9' y='37' font-size='10' fill='#1e1e1e' text-anchor='start'>(e, 1)</text><text x='72' y='108' font-size='10' fill='#1e1e1e' text-anchor='start'>1</text><text x='14' y='108' font-size='10' fill='#1e1e1e' text-anchor='start'>O</text><text x='162.5' y='72.5' font-size='10' fill='#1f3f8f' text-anchor='start'>y=log x</text><text x='47.5' y='55.0' font-size='10' fill='#c0392b' text-anchor='start'>y=x/e</text></svg>求める図形は、$\ell$ と $x$ 軸と直線 $x=e$ で囲まれた直角三角形から、$C$ と $x$ 軸と $x=e$ で囲まれた部分を除いたもの。<br>$S=\frac12\cdot e\cdot1-\int_1^e\log x\,dx=\frac e2-1$。<br><b>ポイント</b>：図形が「三角形 − 曲線の下の部分」のように分けられるときは、引き算で計算すると積分が1回で済む。"},
 {"lv": "B", "tag": "y 軸回転", "q": r"(1) 曲線 $y=\log x$、$x$ 軸、$y$ 軸、直線 $y=1$ で囲まれた図形を $y$ 軸のまわりに1回転してできる立体の体積を求めよ。<br>(2) 曲線 $y=\sin x\ (0\leqq x\leqq\pi)$ と $x$ 軸で囲まれた図形を $y$ 軸のまわりに1回転してできる立体の体積を求めよ。",
  "a": r"(1) $\frac\pi2(e^2-1)$　(2) $2\pi^2$",
  "s": r"(1) $y=\log x$ ⇔ $x=e^y$。図形は $0\leqq y\leqq1,\ 0\leqq x\leqq e^y$ なので $V=\pi\int_0^1(e^y)^2dy=\pi\left[\frac{e^{2y}}{2}\right]_0^1=\frac\pi2(e^2-1)$。<br>(2) 高さ $y\ (0\leqq y\leqq1)$ での断面は、外側の半径 $x_2$（$\frac\pi2\leqq x_2\leqq\pi$）、内側の半径 $x_1$（$0\leqq x_1\leqq\frac\pi2$）の円環。$V=\pi\int_0^1x_2^2dy-\pi\int_0^1x_1^2dy$。<br>$y=\sin x,\ dy=\cos x\,dx$ で置換すると、$x_2$ は $x:\pi\to\frac\pi2$、$x_1$ は $x:0\to\frac\pi2$ に対応し、<br>$V=\pi\int_\pi^{\frac\pi2}x^2\cos x\,dx-\pi\int_0^{\frac\pi2}x^2\cos x\,dx=-\pi\int_0^\pi x^2\cos x\,dx$。<br>部分積分で $\int_0^\pi x^2\cos x\,dx=\left[x^2\sin x\right]_0^\pi-2\int_0^\pi x\sin x\,dx=0-2\pi=-2\pi$。よって $V=2\pi^2$。<br>（参考）薄い円筒に分けて考える公式 $V=2\pi\int_a^bx\,f(x)\,dx$ を使うと $2\pi\int_0^\pi x\sin x\,dx=2\pi\cdot\pi$ ですぐに確かめられる。<br><b>ポイント</b>：$y$ 軸回転は $V=\pi\int x^2dy$。$x$ を $y$ で表せないときは、置換積分で $x$ の積分に直す。"},
 {"lv": "B", "tag": "媒介変数", "q": r"サイクロイド $x=t-\sin t,\ y=1-\cos t\ (0\leqq t\leqq2\pi)$ について、(1) 曲線の長さを求めよ。(2) 曲線と $x$ 軸で囲まれた図形の面積を求めよ。",
  "a": r"(1) $8$　(2) $3\pi$",
  "s": r"(1) $\frac{dx}{dt}=1-\cos t,\ \frac{dy}{dt}=\sin t$。$\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2=2-2\cos t=4\sin^2\frac t2$。$0\leqq t\leqq2\pi$ で $\sin\frac t2\geqq0$ なので $L=\int_0^{2\pi}2\sin\frac t2\,dt=\left[-4\cos\frac t2\right]_0^{2\pi}=8$。<br>(2) $x$ は $t$ について増加（$\frac{dx}{dt}\geqq0$）し、$y\geqq0$。$S=\int_0^{2\pi}y\,dx=\int_0^{2\pi}(1-\cos t)^2dt=\int_0^{2\pi}\left(1-2\cos t+\frac{1+\cos2t}{2}\right)dt=2\pi+\pi=3\pi$。<br><b>ポイント</b>：媒介変数表示の曲線の長さは $\int\sqrt{\left(\frac{dx}{dt}\right)^2+\left(\frac{dy}{dt}\right)^2}dt$、面積は $\int y\frac{dx}{dt}dt$。根号は半角の公式で外す。"},
 {"lv": "B", "tag": "速度と道のり", "q": r"数直線上を動く点 P の時刻 $t$ における速度が $v(t)=\sin t-\dfrac12$ である。$t=0$ から $t=\pi$ までの間の、P の位置の変化量と、P が動いた道のり を求めよ。",
  "a": r"変化量 $2-\frac\pi2$、道のり $2\sqrt3-2-\frac\pi6$",
  "s": r"位置の変化量 $=\int_0^\pi v(t)dt=\left[-\cos t-\frac t2\right]_0^\pi=(1-\frac\pi2)-(-1)=2-\frac\pi2$。<br>道のりは $\int_0^\pi|v(t)|dt$。$v(t)\geqq0$ ⇔ $\frac\pi6\leqq t\leqq\frac56\pi$。原始関数 $F(t)=-\cos t-\frac t2$ を使って<br>$-\{F(\tfrac\pi6)-F(0)\}+\{F(\tfrac56\pi)-F(\tfrac\pi6)\}-\{F(\pi)-F(\tfrac56\pi)\}=F(0)-2F(\tfrac\pi6)+2F(\tfrac56\pi)-F(\pi)$。<br>$F(0)=-1$、$F(\frac\pi6)=-\frac{\sqrt3}{2}-\frac\pi{12}$、$F(\frac56\pi)=\frac{\sqrt3}{2}-\frac{5\pi}{12}$、$F(\pi)=1-\frac\pi2$ を代入して $-1+\sqrt3+\frac\pi6+\sqrt3-\frac{5\pi}{6}-1+\frac\pi2=2\sqrt3-2-\frac\pi6$（$\fallingdotseq0.94$）。<br><b>ポイント</b>：位置の変化量は $\int v\,dt$、道のりは $\int|v|\,dt$。速度の符号が変わる時刻で区間を分ける。"},
 {"lv": "C", "tag": "面積と不等式", "q": r"$H_n=\displaystyle\sum_{k=1}^{n}\frac1k$ とする。<br>(1) 自然数 $n$ について $\log(n+1)\lt H_n\leqq1+\log n$ を示せ。<br>(2) $\displaystyle\lim_{n\to\infty}\frac{H_n}{\log n}$ を求めよ。",
  "a": r"(2) $1$",
  "s": r"(1) $y=\frac1x$ は $x\gt0$ で減少関数。$k\leqq x\leqq k+1$ で $\frac{1}{k+1}\leqq\frac1x\leqq\frac1k$（等号は端点のみ）なので、積分して $\frac{1}{k+1}\lt\int_k^{k+1}\frac{dx}{x}\lt\frac1k$。<br>左の不等式：$\frac1k\gt\int_k^{k+1}\frac{dx}{x}$ を $k=1,\cdots,n$ で加えて $H_n\gt\int_1^{n+1}\frac{dx}{x}=\log(n+1)$。<br>右の不等式：$n\geqq2$ のとき $\frac{1}{k+1}\lt\int_k^{k+1}\frac{dx}{x}$ を $k=1,\cdots,n-1$ で加えて $H_n-1\lt\int_1^n\frac{dx}{x}=\log n$。$n=1$ では $H_1=1=1+\log1$。■<br>(2) $n\geqq2$ のとき $\log n\gt0$ で、$\frac{\log(n+1)}{\log n}\lt\frac{H_n}{\log n}\lt\frac{1}{\log n}+1$。$\frac{\log(n+1)}{\log n}=1+\frac{\log\left(1+\frac1n\right)}{\log n}\to1$、$\frac{1}{\log n}+1\to1$。はさみうちの原理より極限は $1$。<br><b>ポイント</b>：和 $\sum f(k)$ を、幅1の長方形の面積の和とみて定積分と比べる。減少関数なら、長方形の高さを左端でとるか右端でとるかで上下からはさめる。"},
 {"lv": "C", "tag": "断面積と体積", "q": r"底面が円 $x^2+y^2\leqq1\ (z=0)$ の直円柱を、$x$ 軸を通り底面と $45^\circ$ の角をなす平面 $z=y$ で切る。底面のうち $y\geqq0$ の部分と平面 $z=y$ の間にはさまれた、くさび形の立体を $K$ とする。<br>(1) $K$ を平面 $x=t\ (-1\leqq t\leqq1)$ で切った断面の面積を求め、$K$ の体積を求めよ。<br>(2) $K$ の表面のうち、円柱の側面の一部である曲面の面積を求めよ。",
  "a": r"(1) 断面積 $\frac{1-t^2}{2}$、体積 $\frac23$　(2) $2$",
  "s": r"(1) 平面 $x=t$ による断面は、$0\leqq y\leqq\sqrt{1-t^2},\ 0\leqq z\leqq y$ の直角二等辺三角形。面積 $\frac12(1-t^2)$。<br>$V=\int_{-1}^{1}\frac{1-t^2}{2}dt=\frac12\left(2-\frac23\right)=\frac23$。<br>（別解）平面 $y=s$ で切ると、断面は横 $2\sqrt{1-s^2}$、高さ $s$ の長方形。$V=\int_0^12s\sqrt{1-s^2}ds=\left[-\frac23(1-s^2)^{\frac32}\right]_0^1=\frac23$。<br>(2) 円柱の側面上の点を $(\cos\theta,\ \sin\theta,\ z)\ (0\leqq\theta\leqq\pi)$ と表す。曲面は $0\leqq z\leqq\sin\theta$ の部分。側面を切り開くと、横軸に弧の長さ $\theta$（半径1なので弧長 $=\theta$）、縦軸に $z$ をとった平面図形 $0\leqq z\leqq\sin\theta\ (0\leqq\theta\leqq\pi)$ になる。面積は $\int_0^\pi\sin\theta\,d\theta=2$。<br><b>ポイント</b>：回転体でない立体は「断面積を求めて積分」。どの向きの平面で切ると断面が簡単になるかを考え、2通りで検算できるとよい。曲面の面積は、展開図にできるなら平面図形の面積に直す。"},
]}}

def verify():
    x, t, y = symbols("x t y", real=True)
    xp = symbols("xp", positive=True)
    eq = lambda u, v: simplify(u-v) == 0
    assert integrate(sin(x), (x, 0, pi)) == 2 and integrate(log(xp), (xp, 1, E)) == 1
    assert pi*integrate(x, (x, 0, 4)) == 8*pi and eq(pi*integrate(sin(x)**2, (x, 0, pi)), pi**2/2)
    f = Rational(2, 3)*xp**Rational(3, 2)
    assert eq(integrate(sqrt(1+diff(f, xp)**2), (xp, 0, 3)), Rational(14, 3))
    n, k = symbols("n k", integer=True, positive=True)
    assert limit(summation((k/n)**2, (k, 1, n))/n, n, oo) == Rational(1, 3)
    assert integrate(1/(1+x**2), (x, 0, 1)) == pi/4 and integrate(1/(1+x), (x, 0, 1)) == log(2)
    import mpmath
    N = 20000
    assert abs(sum(N/(N**2+kk**2) for kk in range(1, N+1)) - float(pi/4)) < 1e-4
    assert abs(sum(1/(N+kk) for kk in range(1, N+1)) - float(log(2))) < 1e-4
    # B1
    assert eq(integrate(sin(x)-cos(x), (x, pi/4, 5*pi/4)), 2*sqrt(2))
    # B2
    assert eq(E/2 - integrate(log(xp), (xp, 1, E)), E/2-1)
    S = integrate(xp/E, (xp, 0, 1)) + integrate(xp/E-log(xp), (xp, 1, E))
    assert eq(S, E/2-1)
    # B3
    assert eq(pi*integrate(exp(2*y), (y, 0, 1)), pi*(E**2-1)/2)
    assert integrate(x**2*cos(x), (x, 0, pi)) == -2*pi
    V1 = pi*integrate((pi-asin(y))**2 - asin(y)**2, (y, 0, 1))
    assert eq(V1, 2*pi**2) and eq(2*pi*integrate(x*sin(x), (x, 0, pi)), 2*pi**2)
    # B4
    X, Y = t-sin(t), 1-cos(t)
    assert eq(diff(X, t)**2+diff(Y, t)**2, 4*sin(t/2)**2)
    assert integrate(2*sin(t/2), (t, 0, 2*pi)) == 8
    assert integrate(Y*diff(X, t), (t, 0, 2*pi)) == 3*pi
    # B5
    v = sin(t)-Rational(1, 2)
    assert eq(integrate(v, (t, 0, pi)), 2-pi/2)
    dist = -integrate(v, (t, 0, pi/6))+integrate(v, (t, pi/6, 5*pi/6))-integrate(v, (t, 5*pi/6, pi))
    assert eq(dist, 2*sqrt(3)-2-pi/6)
    Fv = -cos(t)-t/2
    vals = [Fv.subs(t, a) for a in (0, pi/6, 5*pi/6, pi)]
    assert eq(vals[0], -1) and eq(vals[1], -sqrt(3)/2-pi/12) and eq(vals[2], sqrt(3)/2-5*pi/12) and eq(vals[3], 1-pi/2)
    assert eq(vals[0]-2*vals[1]+2*vals[2]-vals[3], 2*sqrt(3)-2-pi/6)
    assert abs(mpmath.quad(lambda u: abs(mpmath.sin(u)-0.5), [0, mpmath.pi/6, 5*mpmath.pi/6, mpmath.pi]) - float(2*sqrt(3)-2-pi/6)) < 1e-12
    # C1
    for nv in [1, 2, 5, 10, 100, 1000]:
        H = sum(mpmath.mpf(1)/kk for kk in range(1, nv+1))
        assert mpmath.log(nv+1) < H <= 1+mpmath.log(nv) + 1e-30
    assert limit(log(n+1)/log(n), n, oo) == 1
    # C2
    tt = symbols("tt", real=True)
    assert integrate((1-tt**2)/2, (tt, -1, 1)) == Rational(2, 3)
    s = symbols("s", positive=True)
    assert integrate(2*s*sqrt(1-s**2), (s, 0, 1)) == Rational(2, 3)
    th = symbols("th")
    assert integrate(sin(th), (th, 0, pi)) == 2
    # モンテカルロ風の格子点で体積を粗く確認
    cnt = 0; M = 60
    for i in range(M):
        for j in range(M):
            for l in range(M):
                px = -1+2*(i+0.5)/M; py = (j+0.5)/M; pz = (l+0.5)/M
                if px*px+py*py <= 1 and pz <= py:
                    cnt += 1
    vol = cnt*(2/M)*(1/M)*(1/M)
    assert abs(vol-2/3) < 0.02
