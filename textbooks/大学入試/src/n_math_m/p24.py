"""問題集 第24章 微分法の応用。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {24: {
"goal": r"増減・凹凸・漸近線からグラフをかき、最大最小・方程式の解の個数・不等式の証明に使う。平均値の定理で、差を微分係数に置きかえる発想を身につける。",
"items": [
 {"lv": "A", "q": r"関数 $y=xe^{-x}$ の増減、極値、グラフの凹凸、変曲点を調べよ。また $\displaystyle\lim_{x\to\infty}xe^{-x}=0$ を用いて漸近線を答えよ。",
  "a": r"$x=1$ で極大値 $\frac1e$；$x\lt2$ で上に凸、$x\gt2$ で下に凸、変曲点 $\left(2,\ \frac{2}{e^2}\right)$；漸近線 $y=0$",
  "s": r"$y'=e^{-x}-xe^{-x}=(1-x)e^{-x}$、$y''=-e^{-x}-(1-x)e^{-x}=(x-2)e^{-x}$。<br>$x\lt1$ で増加、$x\gt1$ で減少し、$x=1$ で極大値 $\frac1e$。$y''$ の符号から $x\lt2$ で上に凸、$x\gt2$ で下に凸、変曲点 $\left(2,\ \frac2{e^2}\right)$。<br>$x\to\infty$ で $y\to0$ なので $x$ 軸（$y=0$）が漸近線。$x\to-\infty$ では $y\to-\infty$。<br><b>ポイント</b>：$e^{-x}$ は常に正なので、$y',\ y''$ の符号は多項式部分だけで決まる。"},
 {"lv": "A", "q": r"関数 $f(x)=x+2\cos x\ (0\leqq x\leqq\pi)$ の最大値と最小値を求めよ。",
  "a": r"最大値 $\frac\pi6+\sqrt3$（$x=\frac\pi6$）、最小値 $\frac{5}{6}\pi-\sqrt3$（$x=\frac56\pi$）",
  "s": r"$f'(x)=1-2\sin x$。$f'(x)=0$ より $\sin x=\frac12$、$x=\frac\pi6,\ \frac56\pi$。$0\leqq x\lt\frac\pi6$ で増加、$\frac\pi6\lt x\lt\frac56\pi$ で減少、$\frac56\pi\lt x\leqq\pi$ で増加。<br>$f(0)=2$、$f\left(\frac\pi6\right)=\frac\pi6+\sqrt3$、$f\left(\frac56\pi\right)=\frac56\pi-\sqrt3$、$f(\pi)=\pi-2$。<br>最大の候補：$\frac\pi6+\sqrt3\gt2\gt\pi-2$（$\sqrt3\gt1.7,\ \frac\pi6\gt0.5$）。最小の候補：$\left(\frac56\pi-\sqrt3\right)-(\pi-2)=2-\sqrt3-\frac\pi6\lt0$（$2-\sqrt3\lt0.27\lt\frac\pi6$）。<br><b>ポイント</b>：極値と端点の値の大小は、差をとって $\pi\fallingdotseq3.14,\ \sqrt3\fallingdotseq1.73$ で評価する。"},
 {"lv": "A", "q": r"関数 $y=\dfrac{x^2+1}{x-1}$ のグラフの漸近線を求めよ。また、極値を求めよ。",
  "a": r"漸近線 $x=1,\ y=x+1$；$x=1-\sqrt2$ で極大値 $2-2\sqrt2$、$x=1+\sqrt2$ で極小値 $2+2\sqrt2$",
  "s": r"割り算して $y=x+1+\frac{2}{x-1}$。$x\to1\pm0$ で $y\to\pm\infty$ なので $x=1$ が漸近線。$x\to\pm\infty$ で $y-(x+1)=\frac{2}{x-1}\to0$ なので $y=x+1$ も漸近線。<br>$y'=1-\frac{2}{(x-1)^2}=\frac{(x-1)^2-2}{(x-1)^2}$。$y'=0$ より $x=1\pm\sqrt2$。<br>$x=1-\sqrt2$：$y=2-\sqrt2+\frac{2}{-\sqrt2}=2-2\sqrt2$（極大）。$x=1+\sqrt2$：$y=2+\sqrt2+\sqrt2=2+2\sqrt2$（極小）。<br><b>ポイント</b>：分数関数は「多項式＋真分数式」に分けると、斜めの漸近線と微分の両方が楽になる。極大値が極小値より小さいこともある。"},
 {"lv": "A", "q": r"(1) 座標平面上を動く点 P の時刻 $t$ における座標が $(2\cos t,\ \sin t)$ であるとき、$t=\frac\pi3$ における P の速さと加速度の大きさを求めよ。(2) 1次の近似式を用いて $\sqrt{1.02}$ の近似値を求めよ。",
  "a": r"(1) 速さ $\frac{\sqrt{13}}{2}$、加速度の大きさ $\frac{\sqrt7}{2}$　(2) $1.01$",
  "s": r"(1) 速度 $\vec v=(-2\sin t,\ \cos t)$、加速度 $\vec\alpha=(-2\cos t,\ -\sin t)$。$t=\frac\pi3$ で $\vec v=\left(-\sqrt3,\ \frac12\right)$、$|\vec v|=\sqrt{3+\frac14}=\frac{\sqrt{13}}2$。$\vec\alpha=\left(-1,\ -\frac{\sqrt3}{2}\right)$、$|\vec\alpha|=\sqrt{1+\frac34}=\frac{\sqrt7}{2}$。<br>(2) $|h|$ が小さいとき $f(a+h)\fallingdotseq f(a)+f'(a)h$。$f(x)=\sqrt x,\ a=1,\ h=0.02$ で $\sqrt{1.02}\fallingdotseq1+\frac12\cdot0.02=1.01$。<br><b>ポイント</b>：速度は位置の微分、加速度は速度の微分。近似式は接線で曲線を近似している。"},
 {"lv": "B", "tag": "不等式の証明", "q": r"(1) $x\gt0$ のとき、$e^x\gt1+x+\dfrac{x^2}{2}$ が成り立つことを示せ。(2) (1)を用いて $\displaystyle\lim_{x\to\infty}\frac{x}{e^x}=0$ を示せ。",
  "a": r"証明（解説参照）",
  "s": r"(1) $f(x)=e^x-1-x-\frac{x^2}{2}$ とおく。$f'(x)=e^x-1-x$、$f''(x)=e^x-1$。<br>$x\gt0$ で $f''(x)\gt0$ なので $f'(x)$ は $x\geqq0$ で増加し、$f'(x)\gt f'(0)=0$。よって $f(x)$ も $x\geqq0$ で増加し、$x\gt0$ で $f(x)\gt f(0)=0$。■<br>(2) $x\gt0$ のとき (1) より $e^x\gt\frac{x^2}{2}$ なので $0\lt\frac{x}{e^x}\lt\frac2x$。$x\to\infty$ で $\frac2x\to0$ なので、はさみうちの原理より $\frac{x}{e^x}\to0$。■<br><b>ポイント</b>：1回の微分で符号が決まらないときは、もう一度微分する（$f''\to f'\to f$ の順に符号を決める）。不等式は極限の「はさみうち」の道具にもなる。"},
 {"lv": "B", "tag": "解の個数", "q": r"$a$ を定数とする。方程式 $e^x=ax$ の異なる実数解の個数を調べよ。",
  "a": r"$a\lt0$ で1個、$0\leqq a\lt e$ で0個、$a=e$ で1個、$a\gt e$ で2個",
  "s": r"$x=0$ は解でない（$e^0=1\neq0$）ので、$x\neq0$ で $a=\frac{e^x}{x}$ と変形し、$y=g(x)=\frac{e^x}{x}$ と直線 $y=a$ の共有点を数える。<br>$g'(x)=\frac{e^x(x-1)}{x^2}$。$x\lt0$ では $g'\lt0$ で減少、$g(x)\lt0$。$\lim_{x\to-\infty}g(x)=0$、$\lim_{x\to-0}g(x)=-\infty$。$x\gt0$ では $x=1$ で最小値 $g(1)=e$、$\lim_{x\to+0}g(x)=\infty$、$\lim_{x\to\infty}g(x)=\infty$。<svg class='fig' width='230' height='190' viewBox='0 0 230 190'><line x1='4' y1='120' x2='226' y2='120' stroke='#555'/><line x1='115' y1='186' x2='115' y2='4' stroke='#555'/><text x='218' y='133' font-size='11'>x</text><text x='103' y='13' font-size='11'>y</text><polyline points='11.0,120.1 12.3,120.1 13.6,120.1 14.9,120.1 16.2,120.2 17.5,120.2 18.8,120.2 20.1,120.2 21.4,120.2 22.7,120.2 24.0,120.2 25.3,120.2 26.6,120.3 27.9,120.3 29.2,120.3 30.5,120.3 31.8,120.3 33.1,120.4 34.4,120.4 35.7,120.4 37.0,120.4 38.3,120.5 39.6,120.5 40.9,120.5 42.2,120.6 43.5,120.6 44.8,120.6 46.1,120.7 47.4,120.7 48.7,120.8 50.0,120.9 51.3,120.9 52.6,121.0 53.9,121.1 55.2,121.1 56.5,121.2 57.8,121.3 59.1,121.4 60.4,121.5 61.7,121.6 63.0,121.8 64.3,121.9 65.6,122.0 66.9,122.2 68.2,122.4 69.5,122.6 70.8,122.8 72.1,123.0 73.4,123.3 74.7,123.6 76.0,123.9 77.3,124.2 78.6,124.6 79.9,125.0 81.2,125.5 82.5,126.0 83.8,126.5 85.1,127.2 86.4,127.9 87.7,128.7 89.0,129.6 90.3,130.6 91.6,131.7 92.9,133.1 94.2,134.6 95.5,136.4 96.8,138.4 98.1,140.9 99.4,143.8 100.7,147.3 102.0,151.5 103.3,156.8 104.6,163.6 105.9,172.3 107.2,184.2' fill='none' stroke='#1f3f8f' stroke-width='1.5'/><polyline points='123.3,8.1 123.8,12.6 124.4,16.5 124.9,19.9 125.4,23.0 125.9,25.8 126.4,28.2 127.0,30.5 127.5,32.5 128.0,34.3 128.5,35.9 129.0,37.4 129.6,38.7 130.1,39.9 130.6,41.0 131.1,42.0 131.6,43.0 132.2,43.8 132.7,44.5 133.2,45.2 133.7,45.8 134.2,46.4 134.8,46.8 135.3,47.3 135.8,47.7 136.3,48.0 136.8,48.3 137.4,48.6 137.9,48.8 138.4,48.9 138.9,49.1 139.4,49.2 140.0,49.3 140.5,49.3 141.0,49.3 141.5,49.3 142.0,49.3 142.6,49.2 143.1,49.1 143.6,49.0 144.1,48.9 144.6,48.7 145.2,48.5 145.7,48.3 146.2,48.1 146.7,47.8 147.2,47.5 147.8,47.3 148.3,46.9 148.8,46.6 149.3,46.3 149.8,45.9 150.4,45.5 150.9,45.1 151.4,44.7 151.9,44.2 152.4,43.8 153.0,43.3 153.5,42.8 154.0,42.3 154.5,41.8 155.0,41.2 155.6,40.7 156.1,40.1 156.6,39.5 157.1,38.9 157.6,38.3 158.2,37.6 158.7,37.0 159.2,36.3 159.7,35.6 160.2,34.9 160.8,34.1 161.3,33.4 161.8,32.6 162.3,31.8 162.8,31.0 163.4,30.2 163.9,29.4 164.4,28.5 164.9,27.6 165.4,26.7 166.0,25.8 166.5,24.9 167.0,23.9 167.5,23.0 168.0,22.0 168.6,21.0 169.1,19.9 169.6,18.9 170.1,17.8 170.6,16.7 171.2,15.6 171.7,14.5 172.2,13.3 172.7,12.2 173.2,11.0 173.8,9.8 174.3,8.5 174.8,7.2 175.3,6.0 175.8,4.7' fill='none' stroke='#1f3f8f' stroke-width='1.5'/><line x1='4' y1='49.3' x2='226' y2='49.3' stroke='#c0392b' stroke-dasharray='4,3'/><text x='8' y='45.3' font-size='10' fill='#c0392b' text-anchor='start'>y=e</text><circle cx='141' cy='49.3' r='2.2' fill='#1e1e1e'/><text x='145' y='62.3' font-size='10' fill='#1e1e1e' text-anchor='start'>(1, e)</text><text x='104' y='133' font-size='10' fill='#1e1e1e' text-anchor='start'>O</text></svg>よって、$a\lt0$ で1個、$0\leqq a\lt e$ で0個、$a=e$ で1個（$x=1$）、$a\gt e$ で2個。<br><b>ポイント</b>：文字定数を分離して $y=g(x)$ と水平線の交点にする。グラフの端の様子（$x\to\pm\infty$、分母 $\to0$）は極限で調べる。"},
 {"lv": "B", "tag": "最大最小の応用", "q": r"半径1の球に内接する直円錐のうち、体積が最大となるものの高さと、そのときの体積を求めよ。",
  "a": r"高さ $\frac43$、体積 $\frac{32}{81}\pi$",
  "s": r"直円錐の高さを $h\ (0\lt h\lt2)$、底面の半径を $r$ とする。球の中心から底面までの距離は $|h-1|$ なので、$r^2+(h-1)^2=1$、$r^2=2h-h^2$。<br>$V=\frac13\pi r^2h=\frac\pi3(2h^2-h^3)$。$V'=\frac\pi3(4h-3h^2)=\frac\pi3h(4-3h)$ より、$0\lt h\lt\frac43$ で増加、$\frac43\lt h\lt2$ で減少。<br>最大は $h=\frac43$ で、$V=\frac\pi3\left(2\cdot\frac{16}{9}-\frac{64}{27}\right)=\frac\pi3\cdot\frac{32}{27}=\frac{32}{81}\pi$。<br><b>ポイント</b>：変数を1つ（ここでは高さ $h$）に決め、他の量をそれで表す。変数の範囲を明示してから増減表を作る。"},
 {"lv": "B", "tag": "平均値の定理", "q": r"(1) $0\lt a\lt b$ のとき、$\dfrac{b-a}{b}\lt\log\dfrac ba\lt\dfrac{b-a}{a}$ を示せ。(2) $\displaystyle\lim_{x\to\infty}x\{\log(x+1)-\log x\}$ を求めよ。",
  "a": r"(2) $1$",
  "s": r"(1) $f(x)=\log x$ は $a\leqq x\leqq b$ で連続、$a\lt x\lt b$ で微分可能なので、平均値の定理より $\frac{\log b-\log a}{b-a}=\frac1c$、$a\lt c\lt b$ を満たす $c$ がある。$\frac1b\lt\frac1c\lt\frac1a$ なので、各辺に $b-a\gt0$ をかけて示された。■<br>(2) $x\gt0$ で (1) を $a=x,\ b=x+1$ に用いると $\frac{1}{x+1}\lt\log(x+1)-\log x\lt\frac1x$。各辺に $x$ をかけて $\frac{x}{x+1}\lt x\{\log(x+1)-\log x\}\lt1$。$\frac{x}{x+1}\to1$ なので、はさみうちの原理より極限は $1$。<br>（別解）$x\log\left(1+\frac1x\right)=\log\left(1+\frac1x\right)^x\to\log e=1$。<br><b>ポイント</b>：「$f(b)-f(a)$」の形を見たら平均値の定理で $f'(c)(b-a)$ に置きかえ、$c$ の範囲で評価する。"},
 {"lv": "B", "tag": "変曲点", "q": r"曲線 $y=x^4+ax^3+6x^2+1$ が変曲点を2つもつような定数 $a$ の値の範囲を求めよ。また、$a=5$ のときの変曲点の $x$ 座標を求めよ。",
  "a": r"$a\lt-4,\ 4\lt a$；$a=5$ のとき $x=-2,\ -\frac12$",
  "s": r"$y''=12x^2+6ax+12=6(2x^2+ax+2)$。変曲点は $y''$ の符号が変わる点なので、2つもつ ⇔ $2x^2+ax+2=0$ が異なる2実解をもつ ⇔ 判別式 $a^2-16\gt0$ ⇔ $a\lt-4,\ 4\lt a$。<br>（重解のときは $y''\geqq0$ で符号が変わらず、変曲点はない。）<br>$a=5$：$2x^2+5x+2=(2x+1)(x+2)=0$ より $x=-2,\ -\frac12$。<br><b>ポイント</b>：変曲点 ⇔ $f''(x)$ の符号が変わる点。$f''(a)=0$ だけでは不十分（例：$y=x^4$ の原点）。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$f(x)=\dfrac{\log x}{x}\ (x\gt0)$ とする。<br>(1) $f(x)$ の最大値を求めよ。<br>(2) $e^\pi$ と $\pi^e$ の大小を比べよ。<br>(3) $m^n=n^m,\ m\lt n$ を満たす自然数の組 $(m,\ n)$ をすべて求めよ。",
  "a": r"(1) $\frac1e$（$x=e$）　(2) $e^\pi\gt\pi^e$　(3) $(m,\ n)=(2,\ 4)$",
  "s": r"(1) $f'(x)=\frac{1-\log x}{x^2}$。$0\lt x\lt e$ で増加、$x\gt e$ で減少。最大値 $f(e)=\frac1e$。<br>(2) $\pi\neq e$ なので $f(\pi)\lt f(e)$、$\frac{\log\pi}{\pi}\lt\frac1e$。両辺に $e\pi\gt0$ をかけて $e\log\pi\lt\pi$、$\log\pi^e\lt\log e^\pi$。よって $\pi^e\lt e^\pi$。<br>(3) $m^n=n^m$ ⇔ $n\log m=m\log n$ ⇔ $f(m)=f(n)$。$f$ は $(0,e]$ で増加、$[e,\infty)$ で減少するので、$f(m)=f(n),\ m\lt n$ なら $m\lt e\lt n$。$m$ は $1$ か $2$。<br>$m=1$：$f(1)=0$、$x\gt1$ で $f(x)\gt0$ なので $f(n)=0$ となる $n\gt1$ はない。<br>$m=2$：$f(4)=\frac{\log4}{4}=\frac{\log2}{2}=f(2)$。$x\gt e$ で $f$ は減少なので、$f(n)=f(2)$ となる $n\gt e$ は $n=4$ だけ。<br>よって $(m,n)=(2,4)$。<br><b>ポイント</b>：$a^b$ と $b^a$ の比較は、対数をとって $\frac{\log a}{a}$ と $\frac{\log b}{b}$ の比較に直す。同じ関数値をとる2点は、極大点の両側にある。"},
 {"lv": "C", "tag": "平均値の定理と極限", "q": r"(1) 方程式 $\cos x=x$ は $0\lt x\lt1$ の範囲にただ1つの実数解 $\alpha$ をもつことを示せ。<br>(2) $x_1=0,\ x_{n+1}=\cos x_n$ で定まる数列について、すべての $n$ で $0\leqq x_n\leqq1$ であり、$|x_{n+1}-\alpha|\leqq(\sin1)|x_n-\alpha|$ であることを示せ。<br>(3) $\displaystyle\lim_{n\to\infty}x_n=\alpha$ を示せ。",
  "a": r"証明（解説参照）。$\alpha\fallingdotseq0.739$",
  "s": r"(1) $g(x)=\cos x-x$ とおくと $g'(x)=-\sin x-1\leqq0$ で、等号は孤立した点だけなので $g$ は減少関数。$g(0)=1\gt0$、$g(1)=\cos1-1\lt0$ なので、中間値の定理より $g(\alpha)=0$ となる $\alpha$ が $0\lt\alpha\lt1$ にただ1つある。■<br>(2) $0\leqq x_n\leqq1$ を帰納法で示す。$x_1=0$。$0\leqq x_k\leqq1$ なら $\cos1\leqq\cos x_k\leqq1$ で、$\cos1\gt0$ より $0\leqq x_{k+1}\leqq1$。<br>$x_n\neq\alpha$ のとき、平均値の定理より $\cos x_n-\cos\alpha=-\sin c\cdot(x_n-\alpha)$ となる $c$ が $x_n$ と $\alpha$ の間にある。$0\lt c\lt1$ なので $0\lt\sin c\lt\sin1$。$x_{n+1}-\alpha=\cos x_n-\cos\alpha$ より $|x_{n+1}-\alpha|\leqq(\sin1)|x_n-\alpha|$（$x_n=\alpha$ なら両辺 $0$）。■<br>(3) くり返し用いて $0\leqq|x_n-\alpha|\leqq(\sin1)^{n-1}|x_1-\alpha|=(\sin1)^{n-1}\alpha$。$0\lt\sin1\lt1$ より右辺 $\to0$。はさみうちの原理より $x_n\to\alpha$。■<br><b>ポイント</b>：$x_{n+1}=f(x_n)$ の収束は、平均値の定理で $|f(x_n)-f(\alpha)|=|f'(c)||x_n-\alpha|$ とし、$|f'(c)|\leqq r\lt1$ を示すのが定石。そのために $x_n$ の範囲を先に押さえておく。"},
]}}

def verify():
    x, h, a, r = symbols("x h a r", real=True)
    eq = lambda u, v: simplify(u-v) == 0
    y = x*exp(-x)
    assert eq(diff(y, x), (1-x)*exp(-x)) and eq(diff(y, x, 2), (x-2)*exp(-x))
    assert y.subs(x, 1) == exp(-1) and y.subs(x, 2) == 2*exp(-2) and limit(y, x, oo) == 0
    # A2
    f = x+2*cos(x)
    assert set(solve(diff(f, x), x)) == {pi/6, 5*pi/6}
    vals = {v: f.subs(x, v) for v in [0, pi/6, 5*pi/6, pi]}
    assert max(vals.values(), key=lambda t: float(t)) == pi/6+sqrt(3)
    assert min(vals.values(), key=lambda t: float(t)) == 5*pi/6-sqrt(3)
    # A3
    y = (x**2+1)/(x-1)
    assert eq(y, x+1+2/(x-1)) and limit(y-(x+1), x, oo) == 0
    assert set(solve(diff(y, x), x)) == {1-sqrt(2), 1+sqrt(2)}
    assert eq(y.subs(x, 1-sqrt(2)), 2-2*sqrt(2)) and eq(y.subs(x, 1+sqrt(2)), 2+2*sqrt(2))
    assert diff(y, x, 2).subs(x, 1+sqrt(2)) > 0 and diff(y, x, 2).subs(x, 1-sqrt(2)) < 0
    # A4
    t = symbols("t", real=True)
    P = Matrix([2*cos(t), sin(t)])
    v = P.diff(t); acc = v.diff(t)
    assert eq(v.subs(t, pi/3).norm(), sqrt(13)/2) and eq(acc.subs(t, pi/3).norm(), sqrt(7)/2)
    assert abs(sqrt(1.02) - 1.01) < 1e-4
    # B1
    f = exp(x)-1-x-x**2/2
    for xv in [Rational(1, 10), 1, 3, 10]:
        assert f.subs(x, xv) > 0
    assert limit(x/exp(x), x, oo) == 0
    # B2
    g = exp(x)/x
    assert eq(diff(g, x), exp(x)*(x-1)/x**2) and g.subs(x, 1) == E
    assert limit(g, x, -oo) == 0 and limit(g, x, 0, "-") == -oo and limit(g, x, 0, "+") == oo
    import mpmath
    def count(av):
        rts = set()
        for x0 in [-10, -3, -1, -0.3, 0.2, 0.6, 1, 1.5, 3, 6]:
            try:
                rt = mpmath.findroot(lambda u: mpmath.exp(u)-av*u, x0)
                if abs(mpmath.exp(rt)-av*rt) < 1e-12:
                    rts.add(round(float(rt), 6))
            except Exception:
                pass
        return len(rts)
    assert count(-2) == 1 and count(1) == 0 and count(2.5) == 0 and count(4) == 2
    # B3
    hh = symbols("hh", positive=True)
    V = pi/3*(2*hh**2-hh**3)
    assert solve(diff(V, hh), hh) == [Rational(4, 3)] and eq(V.subs(hh, Rational(4, 3)), 32*pi/81)
    # B4
    for (av, bv) in [(1, 2), (Rational(1, 3), 5), (2, 7)]:
        L = log(Rational(bv)/av)
        assert (bv-av)/Rational(bv) < L < (bv-av)/Rational(av)
    assert limit(x*(log(x+1)-log(x)), x, oo) == 1
    # B5
    y = x**4+a*x**3+6*x**2+1
    assert expand(diff(y, x, 2) - 6*(2*x**2+a*x+2)) == 0
    assert expand(discriminant(2*x**2+a*x+2, x) - (a**2-16)) == 0
    assert set(solve(diff(y, x, 2).subs(a, 5), x)) == {-2, Rational(-1, 2)}
    # C1
    xp = symbols("xp", positive=True)
    f = log(xp)/xp
    assert solve(diff(f, xp), xp) == [E] and f.subs(xp, E) == 1/E
    assert exp(pi) > pi**E
    sols = [(m, n) for m in range(1, 60) for n in range(m+1, 60) if m**n == n**m]
    assert sols == [(2, 4)]
    # C2
    al = mpmath.findroot(lambda u: mpmath.cos(u)-u, 0.7)
    assert 0 < al < 1 and abs(al-0.739085) < 1e-6
    xs = [mpmath.mpf(0)]
    for _ in range(60):
        xs.append(mpmath.cos(xs[-1]))
    s1 = mpmath.sin(1)
    for k in range(60):
        assert 0 <= xs[k] <= 1
        assert abs(xs[k+1]-al) <= s1*abs(xs[k]-al) + 1e-30
    assert abs(xs[-1]-al) < 1e-4
