"""問題集 第21章 2次曲線・媒介変数・極座標。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {21: {
"goal": r"放物線・楕円・双曲線の標準形と焦点・漸近線を即答できるようにする。接線と弦は「代入して判別式・解と係数の関係」、最大最小は媒介変数、焦点がからむ問題は極座標で。",
"items": [
 {"lv": "A", "q": r"次の曲線の焦点の座標を求めよ。(1) 楕円 $\dfrac{x^2}{25}+\dfrac{y^2}{9}=1$（長軸・短軸の長さも答えよ）　(2) 双曲線 $\dfrac{x^2}{16}-\dfrac{y^2}{9}=1$（漸近線の方程式も答えよ）",
  "a": r"(1) 焦点 $(\pm4,\ 0)$、長軸 $10$、短軸 $6$　(2) 焦点 $(\pm5,\ 0)$、漸近線 $y=\pm\frac34x$",
  "s": r"(1) $a=5,\ b=3$ で $c=\sqrt{a^2-b^2}=4$。長軸 $2a=10$、短軸 $2b=6$。<br>(2) $c=\sqrt{a^2+b^2}=\sqrt{16+9}=5$。漸近線は $\frac{x^2}{16}-\frac{y^2}{9}=0$ より $y=\pm\frac34x$。<br><b>ポイント</b>：楕円は $c^2=a^2-b^2$、双曲線は $c^2=a^2+b^2$。符号を取り違えない。"},
 {"lv": "A", "q": r"(1) 放物線 $y^2=8x$ の焦点と準線を求めよ。(2) 焦点が $(0,\ -2)$、準線が直線 $y=2$ である放物線の方程式を求めよ。",
  "a": r"(1) 焦点 $(2,\ 0)$、準線 $x=-2$　(2) $x^2=-8y$",
  "s": r"(1) $y^2=4px$ で $4p=8$、$p=2$。<br>(2) 点 $(x,y)$ から焦点までの距離と準線までの距離が等しい：$\sqrt{x^2+(y+2)^2}=|y-2|$。2乗して $x^2+y^2+4y+4=y^2-4y+4$、$x^2=-8y$。<br><b>ポイント</b>：放物線の定義「焦点と準線から等距離」に戻れば、向きの異なる放物線も同じ手順で求められる。"},
 {"lv": "A", "q": r"次の媒介変数表示が表す曲線の方程式を $x,\ y$ で表せ。(1) $x=2\cos\theta+1,\ y=3\sin\theta-2$　(2) $x=t^2+1,\ y=2t$",
  "a": r"(1) $\frac{(x-1)^2}{4}+\frac{(y+2)^2}{9}=1$　(2) $y^2=4(x-1)$",
  "s": r"(1) $\cos\theta=\frac{x-1}{2},\ \sin\theta=\frac{y+2}{3}$ を $\cos^2\theta+\sin^2\theta=1$ に代入。中心 $(1,-2)$ の楕円。<br>(2) $t=\frac y2$ を代入して $x=\frac{y^2}{4}+1$。放物線 $y^2=4x$ を $x$ 軸方向に1だけ平行移動したもの。<br><b>ポイント</b>：三角関数の媒介変数は $\cos^2\theta+\sin^2\theta=1$ で消去。$x$ の範囲に制限がつく場合（例 $x=t^2$ なら $x\geqq0$）にも注意する。"},
 {"lv": "A", "q": r"(1) 極座標 $\left(2,\ \frac{2}{3}\pi\right)$ の点を直交座標で、直交座標 $(1,\ -1)$ の点を極座標（$0\leqq\theta\lt2\pi$）で表せ。(2) 極方程式 $r=4\cos\theta$ を直交座標の方程式で表せ。",
  "a": r"(1) $(-1,\ \sqrt3)$、$\left(\sqrt2,\ \frac74\pi\right)$　(2) $(x-2)^2+y^2=4$",
  "s": r"(1) $x=2\cos\frac23\pi=-1,\ y=2\sin\frac23\pi=\sqrt3$。$(1,-1)$ は $r=\sqrt2$、$\theta=\frac74\pi$。<br>(2) 両辺に $r$ をかけて $r^2=4r\cos\theta$、$x^2+y^2=4x$。中心 $(2,0)$、半径2の円（極 O を通る）。<br><b>ポイント</b>：$x=r\cos\theta,\ y=r\sin\theta,\ r^2=x^2+y^2$。$r$ をかけて $r\cos\theta$ や $r^2$ の形を作る。"},
 {"lv": "B", "tag": "接線", "q": r"点 $\mathrm{A}(0,\ 2)$ から楕円 $\dfrac{x^2}{4}+y^2=1$ に引いた接線の方程式と、接点の座標を求めよ。",
  "a": r"$y=\frac{\sqrt3}{2}x+2$（接点 $\left(-\sqrt3,\ \frac12\right)$）、$y=-\frac{\sqrt3}{2}x+2$（接点 $\left(\sqrt3,\ \frac12\right)$）",
  "s": r"$x=0$（$y$ 軸）は接線でないので、接線を $y=mx+2$ とおく。代入して $\frac{x^2}{4}+(mx+2)^2=1$、$\left(\frac14+m^2\right)x^2+4mx+3=0$。<br>接する ⇔ 重解：$\frac{D}{4}=4m^2-3\left(\frac14+m^2\right)=m^2-\frac34=0$、$m=\pm\frac{\sqrt3}{2}$。<br>重解は $x=-\frac{2m}{\frac14+m^2}=-2m$（$\frac14+m^2=1$）。$m=\frac{\sqrt3}{2}$ のとき $x=-\sqrt3$、$y=-\frac32+2=\frac12$。$m=-\frac{\sqrt3}{2}$ のとき $(\sqrt3,\ \frac12)$。<br>（別解）接点を $(x_1,y_1)$ とすると接線は $\frac{x_1x}{4}+y_1y=1$。A を通るので $2y_1=1$、$y_1=\frac12$、$x_1=\pm\sqrt3$。<br><b>ポイント</b>：曲線上の点 $(x_1,y_1)$ における楕円の接線は $\frac{x_1x}{a^2}+\frac{y_1y}{b^2}=1$。外の点から引く接線は、接点をおくか、傾きをおいて判別式 $=0$。"},
 {"lv": "B", "tag": "弦の中点", "q": r"楕円 $\dfrac{x^2}{4}+y^2=1$ と直線 $y=x+k$ が異なる2点 P、Q で交わるような $k$ の値の範囲を求めよ。また、$k$ がこの範囲を動くとき、線分 PQ の中点 M の軌跡を求めよ。",
  "a": r"$-\sqrt5\lt k\lt\sqrt5$；直線 $y=-\frac14x$ の $-\frac{4\sqrt5}{5}\lt x\lt\frac{4\sqrt5}{5}$ の部分",
  "s": r"代入して $\frac{x^2}{4}+(x+k)^2=1$、$5x^2+8kx+4k^2-4=0$。異なる2点 ⇔ $\frac D4=16k^2-5(4k^2-4)=20-4k^2\gt0$ ⇔ $-\sqrt5\lt k\lt\sqrt5$。<br>中点 M$(X,Y)$：解と係数の関係より $X=\frac{x_1+x_2}{2}=-\frac{4k}{5}$、$Y=X+k=\frac k5$。$k=-\frac{5X}{4}$ を代入して $Y=-\frac X4$。<br>$k$ の範囲から $-\frac{4\sqrt5}{5}\lt X\lt\frac{4\sqrt5}{5}$。<br><b>ポイント</b>：軌跡では、媒介変数 $k$ を消去したあと、$k$ の範囲を $X$ の範囲に翻訳するのを忘れない。"},
 {"lv": "B", "tag": "媒介変数で最大最小", "q": r"点 $\mathrm{P}(x,\ y)$ が楕円 $\dfrac{x^2}{9}+\dfrac{y^2}{4}=1$ 上を動くとき、(1) $x+y$ の最大値・最小値と、最大となる点 P を求めよ。(2) $xy$ の最大値を求めよ。",
  "a": r"(1) 最大値 $\sqrt{13}$（$\mathrm{P}\left(\frac{9}{\sqrt{13}},\ \frac{4}{\sqrt{13}}\right)$）、最小値 $-\sqrt{13}$　(2) $3$",
  "s": r"$x=3\cos\theta,\ y=2\sin\theta\ (0\leqq\theta\lt2\pi)$ とおく。<br>(1) $x+y=3\cos\theta+2\sin\theta=\sqrt{13}\sin(\theta+\alpha)$（$\sin\alpha=\frac{3}{\sqrt{13}},\ \cos\alpha=\frac{2}{\sqrt{13}}$）。最大値 $\sqrt{13}$、最小値 $-\sqrt{13}$。最大のとき $\theta+\alpha=\frac\pi2$ で、$\cos\theta=\sin\alpha=\frac{3}{\sqrt{13}},\ \sin\theta=\cos\alpha=\frac{2}{\sqrt{13}}$。$\mathrm{P}\left(\frac{9}{\sqrt{13}},\ \frac{4}{\sqrt{13}}\right)$。<br>(2) $xy=6\sin\theta\cos\theta=3\sin2\theta\leqq3$。等号は $\theta=\frac\pi4$ などで成立。最大値 $3$。<br><b>ポイント</b>：楕円上の点は $(a\cos\theta,\ b\sin\theta)$ とおくと、1変数の三角関数の問題になる。"},
 {"lv": "B", "tag": "双曲線の性質", "q": r"双曲線 $C:\ x^2-y^2=1$ 上の点 $\mathrm{P}(x_0,\ y_0)$ における接線が、2本の漸近線と交わる点を Q、R とする。(1) P は線分 QR の中点であることを示せ。(2) $\triangle\mathrm{OQR}$ の面積は P によらず一定であることを示し、その値を求めよ。",
  "a": r"(2) 面積は $1$",
  "s": r"P における接線は $x_0x-y_0y=1$、漸近線は $y=x,\ y=-x$。<br>$y=x$ との交点：$(x_0-y_0)x=1$。$x_0^2-y_0^2=1$ より $x_0-y_0\neq0$ で、$\mathrm{Q}\left(\frac{1}{x_0-y_0},\ \frac{1}{x_0-y_0}\right)$。同様に $\mathrm{R}\left(\frac{1}{x_0+y_0},\ -\frac{1}{x_0+y_0}\right)$。<br>(1) $(x_0-y_0)(x_0+y_0)=1$ より $\frac{1}{x_0-y_0}=x_0+y_0,\ \frac{1}{x_0+y_0}=x_0-y_0$。よって $\mathrm{Q}(x_0+y_0,\ x_0+y_0),\ \mathrm{R}(x_0-y_0,\ -x_0+y_0)$ で、中点は $(x_0,\ y_0)=\mathrm{P}$。■<br>(2) $\triangle\mathrm{OQR}=\frac12|x_\mathrm{Q}y_\mathrm{R}-x_\mathrm{R}y_\mathrm{Q}|=\frac12|(x_0+y_0)(-x_0+y_0)-(x_0-y_0)(x_0+y_0)|=\frac12\cdot|-2(x_0^2-y_0^2)|=1$。■<br><b>ポイント</b>：双曲線上の点の条件 $x_0^2-y_0^2=1$ を「$(x_0-y_0)(x_0+y_0)=1$」と因数分解して使うと、分数が消えて見通しがよくなる。"},
 {"lv": "B", "tag": "極方程式", "q": r"極方程式 $r=\dfrac{6}{2-\cos\theta}$ で表される曲線を、直交座標の方程式で表せ。また、それはどのような曲線か。",
  "a": r"$\frac{(x-2)^2}{16}+\frac{y^2}{12}=1$。中心 $(2,0)$ の楕円で、極 O はその焦点の1つ",
  "s": r"分母を払って $2r-r\cos\theta=6$、$2r=x+6$。両辺を2乗して $4(x^2+y^2)=(x+6)^2$、$3x^2-12x+4y^2=36$、$3(x-2)^2+4y^2=48$。よって $\frac{(x-2)^2}{16}+\frac{y^2}{12}=1$。<br>（2乗で増える解はない：楕円上で $x\geqq-2$ なので $x+6\gt0$ となり、$2r=x+6$ を満たす $r\gt0$ がとれる。）<br>$a=4,\ b=2\sqrt3,\ c=\sqrt{16-12}=2$ なので、焦点は $(2\pm2,\ 0)$、すなわち $(0,0)$ と $(4,0)$。<br><b>ポイント</b>：$r=\frac{ek}{1-e\cos\theta}$ の形は、極を焦点とする2次曲線（$0\lt e\lt1$ で楕円、$e=1$ で放物線、$e\gt1$ で双曲線）。ここでは $r=\frac{3}{1-\frac12\cos\theta}$ で $e=\frac12$。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"楕円 $E:\ \dfrac{x^2}{4}+y^2=1$ の外部の点 $\mathrm{P}(p,\ q)$ から $E$ に引いた2本の接線が直交するような点 P の軌跡を求めよ。",
  "a": r"円 $x^2+y^2=5$",
  "s": r"<b>(i) $p\neq\pm2$ のとき</b>：P を通る直線 $x=p$ は接線でないので、接線は $y=m(x-p)+q$ と表せる。$E$ に代入して $\left(\frac14+m^2\right)x^2+2m(q-mp)x+(q-mp)^2-1=0$。<br>接する ⇔ $\frac D4=m^2(q-mp)^2-\left(\frac14+m^2\right)\{(q-mp)^2-1\}=0$ ⇔ $-\frac14(q-mp)^2+\frac14+m^2=0$ ⇔ $(p^2-4)m^2-2pqm+(q^2-1)=0$ …①。<br>2本の接線の傾きは①の2解 $m_1,m_2$ で、直交 ⇔ $m_1m_2=-1$ ⇔ $\frac{q^2-1}{p^2-4}=-1$ ⇔ $p^2+q^2=5$。逆に $p^2+q^2=5$ のとき、①の2解の積は $-1\lt0$ なので①は異なる2実解をもち、確かに直交する2接線が引ける。<br><b>(ii) $p=\pm2$ のとき</b>：直線 $x=\pm2$ は接線。これと直交するもう1本は水平な接線 $y=\pm1$ でなければならず、$q=\pm1$。点 $(\pm2,\ \pm1)$ も $p^2+q^2=5$ を満たす。<br>以上より、軌跡は円 $x^2+y^2=5$。<br><b>ポイント</b>：直交 ⇔ 傾きの積 $-1$ を「傾き $m$ の2次方程式の解と係数の関係」で処理する。傾きが存在しない（$y$ 軸に平行な）接線の場合を別に調べるのを忘れない。一般に楕円 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ では円 $x^2+y^2=a^2+b^2$ になる（準円）。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"楕円 $E:\ \dfrac{(x-2)^2}{16}+\dfrac{y^2}{12}=1$ の焦点 $\mathrm{F}(0,\ 0)$ を通る直線が $E$ と交わる2点を P、Q とする。<br>(1) F を極とする極座標で、$E$ の極方程式は $r=\dfrac{6}{2-\cos\theta}$ であることを示せ。<br>(2) $\dfrac{1}{\mathrm{FP}}+\dfrac{1}{\mathrm{FQ}}$ は直線のとり方によらず一定であることを示せ。<br>(3) 弦 PQ の長さの最大値と最小値を求めよ。",
  "a": r"(2) $\frac23$　(3) 最大値 $8$、最小値 $6$",
  "s": r"(1) $E$ の式を整理すると $3x^2-12x+4y^2=36$。$x=r\cos\theta,\ y=r\sin\theta$ を代入して $3r^2\cos^2\theta-12r\cos\theta+4r^2\sin^2\theta=36$、$4r^2=r^2\cos^2\theta+12r\cos\theta+36=(r\cos\theta+6)^2$。$E$ 上では $x\geqq-2$ より $r\cos\theta+6=x+6\gt0$ なので、$2r=r\cos\theta+6$、$r=\frac{6}{2-\cos\theta}$。■<br>(2) P の偏角を $\theta$ とすると Q の偏角は $\theta+\pi$。$\mathrm{FP}=\frac{6}{2-\cos\theta}$、$\mathrm{FQ}=\frac{6}{2-\cos(\theta+\pi)}=\frac{6}{2+\cos\theta}$。<br>$\frac{1}{\mathrm{FP}}+\frac{1}{\mathrm{FQ}}=\frac{(2-\cos\theta)+(2+\cos\theta)}{6}=\frac23$（一定）。■<br>(3) $\mathrm{PQ}=\mathrm{FP}+\mathrm{FQ}=\frac{6(2+\cos\theta)+6(2-\cos\theta)}{4-\cos^2\theta}=\frac{24}{4-\cos^2\theta}$。$0\leqq\cos^2\theta\leqq1$ より、最大値は $\cos^2\theta=1$ のとき $\frac{24}{3}=8$（長軸）、最小値は $\cos\theta=0$ のとき $\frac{24}{4}=6$（$x$ 軸に垂直な弦）。<svg class='fig' width='175' height='150' viewBox='0 0 175 150'><line x1='4' y1='75' x2='171' y2='75' stroke='#555'/><line x1='50' y1='146' x2='50' y2='4' stroke='#555'/><text x='163' y='88' font-size='11'>x</text><text x='55' y='13' font-size='11'>y</text><polyline points='146.0,75.0 145.9,72.1 145.6,69.2 145.2,66.3 144.6,63.5 143.8,60.7 142.9,57.9 141.7,55.1 140.5,52.5 139.0,49.8 137.4,47.3 135.7,44.8 133.8,42.4 131.7,40.1 129.6,37.9 127.3,35.8 124.8,33.8 122.3,31.9 119.6,30.2 116.9,28.5 114.0,27.0 111.1,25.6 108.0,24.4 104.9,23.3 101.8,22.3 98.6,21.5 95.3,20.8 92.0,20.3 88.7,19.9 85.3,19.7 82.0,19.6 78.7,19.7 75.3,19.9 72.0,20.3 68.7,20.8 65.4,21.5 62.2,22.3 59.1,23.3 56.0,24.4 52.9,25.6 50.0,27.0 47.1,28.5 44.4,30.2 41.7,31.9 39.2,33.8 36.7,35.8 34.4,37.9 32.3,40.1 30.2,42.4 28.3,44.8 26.6,47.3 25.0,49.8 23.5,52.5 22.3,55.1 21.1,57.9 20.2,60.7 19.4,63.5 18.8,66.3 18.4,69.2 18.1,72.1 18.0,75.0 18.1,77.9 18.4,80.8 18.8,83.7 19.4,86.5 20.2,89.3 21.1,92.1 22.3,94.9 23.5,97.5 25.0,100.2 26.6,102.7 28.3,105.2 30.2,107.6 32.3,109.9 34.4,112.1 36.7,114.2 39.2,116.2 41.7,118.1 44.4,119.8 47.1,121.5 50.0,123.0 52.9,124.4 56.0,125.6 59.1,126.7 62.2,127.7 65.4,128.5 68.7,129.2 72.0,129.7 75.3,130.1 78.7,130.3 82.0,130.4 85.3,130.3 88.7,130.1 92.0,129.7 95.3,129.2 98.6,128.5 101.8,127.7 104.9,126.7 108.0,125.6 111.1,124.4 114.0,123.0 116.9,121.5 119.6,119.8 122.3,118.1 124.8,116.2 127.3,114.2 129.6,112.1 131.7,109.9 133.8,107.6 135.7,105.2 137.4,102.7 139.0,100.2 140.5,97.5 141.7,94.9 142.9,92.1 143.8,89.3 144.6,86.5 145.2,83.7 145.6,80.8 145.9,77.9 146.0,75.0' fill='none' stroke='#1f3f8f' stroke-width='1.5'/><line x1='88.6' y1='19.9' x2='28.6' y2='105.6' stroke='#c0392b' stroke-width='1.3'/><circle cx='50' cy='75' r='2.2' fill='#1e1e1e'/><text x='36' y='88' font-size='11' fill='#1e1e1e' text-anchor='start'>F</text><circle cx='114' cy='75' r='1.8' fill='#777'/><text x='110' y='88' font-size='10' fill='#777' text-anchor='start'>4</text><circle cx='88.6' cy='19.9' r='2.2' fill='#1e1e1e'/><text x='92.6' y='16.9' font-size='11' fill='#1e1e1e' text-anchor='start'>P</text><circle cx='28.6' cy='105.6' r='2.2' fill='#1e1e1e'/><text x='16.6' y='117.6' font-size='11' fill='#1e1e1e' text-anchor='start'>Q</text><text x='60' y='71' font-size='10' fill='#c0392b' text-anchor='start'>θ</text></svg><b>ポイント</b>：焦点を通る弦は、焦点を極とする極座標で「$\theta$ と $\theta+\pi$」の2点として扱うと計算が一気に簡単になる。"},
]}}

def verify():
    x, y, t, m, p, q = symbols("x y t m p q", real=True)
    th = symbols("theta", real=True)
    assert sqrt(25-9) == 4 and sqrt(16+9) == 5
    # A2
    assert expand(x**2+(y+2)**2-(y-2)**2 - (x**2+8*y)) == 0
    # A3
    X, Y = 2*cos(th)+1, 3*sin(th)-2
    assert simplify((X-1)**2/4+(Y+2)**2/9 - 1) == 0
    assert expand((2*t)**2 - 4*((t**2+1)-1)) == 0
    # A4
    assert (2*cos(2*pi/3), 2*sin(2*pi/3)) == (-1, sqrt(3))
    assert sqrt(2)*cos(7*pi/4) == 1 and sqrt(2)*sin(7*pi/4) == -1
    r = 4*cos(th)
    assert simplify((r*cos(th)-2)**2+(r*sin(th))**2 - 4) == 0
    # B1
    e = expand(x**2/4+(m*x+2)**2-1)
    disc = discriminant(e, x)
    assert set(solve(disc, m)) == {sqrt(3)/2, -sqrt(3)/2}
    for mv, xv in [(sqrt(3)/2, -sqrt(3)), (-sqrt(3)/2, sqrt(3))]:
        rr = solve(e.subs(m, mv), x)
        assert rr == [xv] and simplify(mv*xv+2 - Rational(1, 2)) == 0
    # B2
    k = symbols("k", real=True)
    e = expand(4*(x**2/4+(x+k)**2-1))
    assert expand(e - (5*x**2+8*k*x+4*k**2-4)) == 0
    assert expand(discriminant(e, x)/4 - (20-4*k**2)) == 0
    rr = solve(e, x)
    Xm = simplify((rr[0]+rr[1])/2)
    assert simplify(Xm + 4*k/5) == 0 and simplify((Xm+k) + Xm/4) == 0
    assert simplify(Rational(4, 5)*sqrt(5) - 4*sqrt(5)/5) == 0
    # B3
    f = 3*cos(th)+2*sin(th)
    assert simplify(maximum(f, th, Interval(0, 2*pi)) - sqrt(13)) == 0
    assert simplify(minimum(f, th, Interval(0, 2*pi)) + sqrt(13)) == 0
    P0 = (9/sqrt(13), 4/sqrt(13))
    assert simplify(P0[0]**2/9+P0[1]**2/4 - 1) == 0 and simplify(P0[0]+P0[1]-sqrt(13)) == 0
    assert maximum(6*sin(th)*cos(th), th, Interval(0, 2*pi)) == 3
    # B4
    x0, y0 = symbols("x0 y0", real=True)
    for (xv, yv) in [(Rational(5, 4), Rational(3, 4)), (Rational(5, 3), -Rational(4, 3)), (-Rational(13, 5), Rational(12, 5))]:
        assert xv**2-yv**2 == 1
        Q = (1/(xv-yv), 1/(xv-yv)); R = (1/(xv+yv), -1/(xv+yv))
        assert xv*Q[0]-yv*Q[1] == 1 and xv*R[0]-yv*R[1] == 1
        assert ((Q[0]+R[0])/2, (Q[1]+R[1])/2) == (xv, yv)
        assert abs(Q[0]*R[1]-R[0]*Q[1])/2 == 1
    # B5
    rr = 6/(2-cos(th))
    assert simplify((rr*cos(th)-2)**2/16+(rr*sin(th))**2/12 - 1) == 0
    assert expand(3*(x-2)**2+4*y**2-48 - (3*x**2-12*x+4*y**2-36)) == 0
    assert expand(4*(x**2+y**2)-(x+6)**2 - (3*x**2-12*x+4*y**2-36)) == 0
    # C1
    e = expand(x**2/4+(m*(x-p)+q)**2-1)
    D = expand(discriminant(e, x))
    assert expand(D/4 - (-Rational(1, 4)*(q-m*p)**2+Rational(1, 4)+m**2)) == 0
    assert expand(D + ((p**2-4)*m**2-2*p*q*m+q**2-1)) == 0
    # 数値確認：円上の点から引いた接線は直交
    for (pv, qv) in [(1, 2), (sqrt(5), 0), (-Rational(3, 5)*sqrt(5), Rational(4, 5)*sqrt(5))]:
        assert simplify(pv**2+qv**2-5) == 0
        ms = solve((pv**2-4)*m**2-2*pv*qv*m+qv**2-1, m)
        assert len(ms) == 2 and simplify(ms[0]*ms[1]+1) == 0
        for mv in ms:
            ee = expand(x**2/4+(mv*(x-pv)+qv)**2-1)
            assert simplify(discriminant(ee, x)) == 0
    # C2
    FP = 6/(2-cos(th)); FQ = 6/(2-cos(th+pi))
    assert simplify(1/FP+1/FQ - Rational(2, 3)) == 0
    assert simplify(FP+FQ - 24/(4-cos(th)**2)) == 0
    assert (FP+FQ).subs(th, 0) == 8 and (FP+FQ).subs(th, pi/2) == 6
    c = symbols("c", real=True)
    assert maximum(24/(4-c**2), c, Interval(-1, 1)) == 8 and minimum(24/(4-c**2), c, Interval(-1, 1)) == 6
