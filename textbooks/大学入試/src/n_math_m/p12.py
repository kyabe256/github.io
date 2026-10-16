"""問題集 第12章 三角関数。CH に問題、verify() で答えを sympy・数値で検算する。"""
from sympy import *


def _fig_sin():
    """y=-s^2+s+1 (-1<=s<=1) と y=1, y=5/4"""
    ox, oy, sx, sy = 100, 82, 70, 44
    X = lambda s: ox + sx * s
    Y = lambda y: oy - sy * y
    f = lambda s: -s * s + s + 1
    pts = " ".join(f"{X(-1 + i * 0.02):.1f},{Y(f(-1 + i * 0.02)):.1f}" for i in range(101))
    s = ['<svg class="fig" width="210" height="140" viewBox="0 0 210 140">',
         f'<line x1="{X(-1.3)}" y1="{Y(0)}" x2="{X(1.4)}" y2="{Y(0)}" stroke="#333"/>',
         f'<line x1="{X(0)}" y1="{Y(-1.2)}" x2="{X(0)}" y2="{Y(1.6)}" stroke="#333"/>',
         f'<polyline points="{pts}" fill="none" stroke="#1f3f8f" stroke-width="1.8"/>',
         f'<line x1="{X(-1.3)}" y1="{Y(1.25)}" x2="{X(1.3)}" y2="{Y(1.25)}" stroke="#c0392b" stroke-dasharray="4,3"/>',
         f'<line x1="{X(-1.3)}" y1="{Y(1)}" x2="{X(1.3)}" y2="{Y(1)}" stroke="#d27a00" stroke-dasharray="4,3"/>',
         f'<line x1="{X(1)}" y1="{Y(0)}" x2="{X(1)}" y2="{Y(1)}" stroke="#999" stroke-dasharray="2,2"/>',
         f'<line x1="{X(-1)}" y1="{Y(0)}" x2="{X(-1)}" y2="{Y(-1)}" stroke="#999" stroke-dasharray="2,2"/>',
         f'<circle cx="{X(1)}" cy="{Y(1)}" r="2.5" fill="#1f3f8f"/>',
         f'<circle cx="{X(-1)}" cy="{Y(-1)}" r="2.5" fill="#1f3f8f"/>',
         f'<text x="{X(1.32)}" y="{Y(1.25) + 4}" font-size="10">5/4</text>',
         f'<text x="{X(1.32)}" y="{Y(1) + 4}" font-size="10">1</text>',
         f'<text x="{X(1) - 3}" y="{Y(0) + 12}" font-size="10">1</text>',
         f'<text x="{X(-1) - 7}" y="{Y(0) + 12}" font-size="10">−1</text>',
         f'<text x="{X(0) - 11}" y="{Y(0) + 12}" font-size="10">O</text>',
         f'<text x="{X(1.35)}" y="{Y(0) + 13}" font-size="11">s</text>',
         f'<text x="{X(0) + 4}" y="{Y(1.5)}" font-size="11">y</text>',
         f'<text x="{X(-1) + 4}" y="{Y(-1) + 4}" font-size="10">−1</text>',
         '</svg>']
    return "".join(s)


CH = {12: {
"goal": "弧度法・加法定理・2倍角・合成を正確に使う。三角関数を含む方程式・最大最小は「1種類の三角関数（または $\\sin\\theta+\\cos\\theta$）に置き換え、変域に注意する」が基本方針。",
"items": [
 {"lv": "A", "q": r"(1) $150^\circ$ を弧度法で表せ。<br>(2) 半径 $4$、中心角 $\dfrac{3}{4}\pi$ の扇形の弧の長さと面積を求めよ。<br>(3) $\cos\left(-\dfrac{11}{3}\pi\right)$、$\tan\dfrac54\pi$ の値を求めよ。",
  "a": r"(1) $\frac56\pi$　(2) 弧の長さ $3\pi$、面積 $6\pi$　(3) $\frac12$、$1$",
  "s": r"(1) $150\times\frac{\pi}{180}=\frac56\pi$。(2) 弧の長さ $r\theta=4\cdot\frac34\pi=3\pi$、面積 $\frac12r^2\theta=\frac12\cdot16\cdot\frac34\pi=6\pi$。(3) $-\frac{11}3\pi+4\pi=\frac\pi3$ なので $\cos\frac\pi3=\frac12$。$\tan\frac54\pi=\tan\left(\pi+\frac\pi4\right)=\tan\frac\pi4=1$。<br><b>ポイント</b>：$\cos$ は周期 $2\pi$、$\tan$ は周期 $\pi$。"},
 {"lv": "A", "q": r"加法定理を用いて、次の値を求めよ。<br>(1) $\sin75^\circ$　(2) $\cos105^\circ$　(3) $\tan15^\circ$",
  "a": r"(1) $\frac{\sqrt6+\sqrt2}{4}$　(2) $\frac{\sqrt2-\sqrt6}{4}$　(3) $2-\sqrt3$",
  "s": r"(1) $\sin(45^\circ+30^\circ)=\frac{\sqrt2}2\cdot\frac{\sqrt3}2+\frac{\sqrt2}2\cdot\frac12=\frac{\sqrt6+\sqrt2}4$。<br>(2) $\cos(60^\circ+45^\circ)=\frac12\cdot\frac{\sqrt2}2-\frac{\sqrt3}2\cdot\frac{\sqrt2}2=\frac{\sqrt2-\sqrt6}4$。<br>(3) $\tan(45^\circ-30^\circ)=\frac{1-\frac1{\sqrt3}}{1+\frac1{\sqrt3}}=\frac{\sqrt3-1}{\sqrt3+1}=\frac{(\sqrt3-1)^2}{2}=2-\sqrt3$。"},
 {"lv": "A", "q": r"$0\leqq\theta<2\pi$ のとき、次の方程式・不等式を解け。<br>(1) $2\cos^2\theta+3\sin\theta-3=0$　(2) $2\cos\theta+\sqrt2<0$",
  "a": r"(1) $\theta=\frac\pi6,\ \frac\pi2,\ \frac56\pi$　(2) $\frac34\pi<\theta<\frac54\pi$",
  "s": r"(1) $2(1-\sin^2\theta)+3\sin\theta-3=0$ より $2\sin^2\theta-3\sin\theta+1=0$、$(2\sin\theta-1)(\sin\theta-1)=0$。$\sin\theta=\frac12$ から $\theta=\frac\pi6,\frac56\pi$、$\sin\theta=1$ から $\theta=\frac\pi2$。<br>(2) $\cos\theta<-\frac{\sqrt2}2$。単位円で $x$ 座標が $-\frac{\sqrt2}2$ より小さい部分なので $\frac34\pi<\theta<\frac54\pi$。<br><b>ポイント</b>：不等式は単位円上で「$x$ 座標（$\cos$）や $y$ 座標（$\sin$）がどこにあるか」を図で読む。"},
 {"lv": "A", "q": r"$\sqrt3\sin\theta+\cos\theta$ を $r\sin(\theta+\alpha)$（$r>0,\ -\pi<\alpha\leqq\pi$）の形に表せ。また、$0\leqq\theta\leqq\pi$ における最大値と最小値を求めよ。",
  "a": r"$2\sin\left(\theta+\frac\pi6\right)$、最大値 $2$（$\theta=\frac\pi3$）、最小値 $-1$（$\theta=\pi$）",
  "s": r"$r=\sqrt{3+1}=2$、$\cos\alpha=\frac{\sqrt3}2,\ \sin\alpha=\frac12$ より $\alpha=\frac\pi6$。$0\leqq\theta\leqq\pi$ のとき $\frac\pi6\leqq\theta+\frac\pi6\leqq\frac76\pi$ なので $-\frac12\leqq\sin\left(\theta+\frac\pi6\right)\leqq1$。最大値 $2$（$\theta+\frac\pi6=\frac\pi2$）、最小値 $-1$（$\theta+\frac\pi6=\frac76\pi$）。<br><b>ポイント</b>：合成したら、角 $\theta+\alpha$ の変域を先に求める。"},
 {"lv": "B", "q": r"$\dfrac\pi2<\theta<\pi$ で $\sin\theta=\dfrac35$ のとき、$\sin2\theta,\ \cos2\theta,\ \tan\dfrac\theta2$ の値を求めよ。",
  "a": r"$\sin2\theta=-\frac{24}{25}$、$\cos2\theta=\frac{7}{25}$、$\tan\frac\theta2=3$",
  "s": r"$\cos\theta=-\frac45$（第2象限）。$\sin2\theta=2\cdot\frac35\cdot\left(-\frac45\right)=-\frac{24}{25}$、$\cos2\theta=1-2\sin^2\theta=1-\frac{18}{25}=\frac7{25}$。<br>$\frac\pi4<\frac\theta2<\frac\pi2$ なので $\tan\frac\theta2>0$。半角の公式 $\tan^2\frac\theta2=\frac{1-\cos\theta}{1+\cos\theta}=\frac{9/5}{1/5}=9$ より $\tan\frac\theta2=3$。<br><b>ポイント</b>：半角は $\frac\theta2$ の範囲で符号を決める。$\tan\frac\theta2=\frac{\sin\theta}{1+\cos\theta}$ を使えば符号も自動的に出る。"},
 {"lv": "B", "tag": "頻出", "q": r"$0\leqq\theta<2\pi$ のとき、関数 $y=\cos2\theta+2\sin\theta$ の最大値と最小値、およびそのときの $\theta$ の値を求めよ。",
  "a": r"最大値 $\frac32$（$\theta=\frac\pi6,\ \frac56\pi$）、最小値 $-3$（$\theta=\frac32\pi$）",
  "s": r"$\cos2\theta=1-2\sin^2\theta$。$s=\sin\theta$ とおくと $-1\leqq s\leqq1$ で $y=-2s^2+2s+1=-2\left(s-\frac12\right)^2+\frac32$。<br>最大：$s=\frac12$ で $\frac32$（$\theta=\frac\pi6,\frac56\pi$）。最小：軸から遠い $s=-1$ で $-2-2+1=-3$（$\theta=\frac32\pi$）。<br><b>ポイント</b>：2倍角で $\sin$ だけの2次関数にし、$s$ の変域 $-1\leqq s\leqq1$ で考える。"},
 {"lv": "B", "q": r"$0\leqq\theta<2\pi$ のとき、$y=2\sin\theta\cos\theta+2(\sin\theta+\cos\theta)-1$ について、<br>(1) $t=\sin\theta+\cos\theta$ とおくとき、$t$ のとりうる値の範囲を求め、$y$ を $t$ で表せ。<br>(2) $y$ の最大値と最小値、およびそのときの $\theta$ を求めよ。",
  "a": r"(1) $-\sqrt2\leqq t\leqq\sqrt2$、$y=t^2+2t-2$　(2) 最大値 $2\sqrt2$（$\theta=\frac\pi4$）、最小値 $-3$（$\theta=\pi,\ \frac32\pi$）",
  "s": r"(1) $t=\sqrt2\sin\left(\theta+\frac\pi4\right)$ より $-\sqrt2\leqq t\leqq\sqrt2$。$t^2=1+2\sin\theta\cos\theta$ なので $2\sin\theta\cos\theta=t^2-1$、$y=t^2-1+2t-1=t^2+2t-2$。<br>(2) $y=(t+1)^2-3$。最小は $t=-1$ で $-3$：$\sin\left(\theta+\frac\pi4\right)=-\frac1{\sqrt2}$ より $\theta+\frac\pi4=\frac54\pi,\frac74\pi$、$\theta=\pi,\frac32\pi$。最大は軸から遠い $t=\sqrt2$ で $2+2\sqrt2-2=2\sqrt2$：$\theta=\frac\pi4$。<br><b>ポイント</b>：$\sin\theta+\cos\theta$ と $\sin\theta\cos\theta$ が混在したら $t=\sin\theta+\cos\theta$。$t$ の範囲は合成で求める。"},
 {"lv": "B", "tag": "解の個数", "q": r"$a$ を定数とする。$\theta$ の方程式 $\cos^2\theta+\sin\theta=a\ (0\leqq\theta<2\pi)$ について、<br>(1) 解をもつような $a$ の値の範囲を求めよ。<br>(2) 異なる解の個数がちょうど4個となる $a$ の値の範囲を求めよ。<br>(3) 異なる解の個数がちょうど3個となる $a$ の値を求めよ。",
  "a": r"(1) $-1\leqq a\leqq\frac54$　(2) $1<a<\frac54$　(3) $a=1$",
  "s": r"$s=\sin\theta$ とおくと $1-s^2+s=a$。$f(s)=-s^2+s+1=-\left(s-\frac12\right)^2+\frac54\ (-1\leqq s\leqq1)$ のグラフと直線 $y=a$ の共有点を考える。$f(-1)=-1,\ f(1)=1$。" + _fig_sin() + r"$0\leqq\theta<2\pi$ では、$-1<s<1$ の $s$ 1つに $\theta$ が2個、$s=\pm1$ には $\theta$ が1個ずつ対応する。<br>(1) 値域は $-1\leqq a\leqq\frac54$。<br>(2) $-1<s<1$ の範囲に共有点が2個あればよく、図より $1<a<\frac54$。<br>(3) $a=1$ のとき $s=0,\ 1$ で、$\theta$ は $2+1=3$ 個。（$a=\frac54$ では $s=\frac12$ のみで2個、$-1<a<1$ では $-1<s<0$ の1個のみで2個、$a=-1$ では1個。）<br><b>ポイント</b>：置き換えたら「$s$ の個数」と「$\theta$ の個数」の対応（$s=\pm1$ だけ1対1）を必ず確認する。"},
 {"lv": "B", "q": r"(1) 2直線 $y=3x$ と $y=\dfrac12x$ のなす鋭角 $\theta$ を求めよ。<br>(2) 原点を通り、直線 $y=2x$ と $\dfrac\pi4$ の角をなす直線の方程式を求めよ。",
  "a": r"(1) $\frac\pi4$　(2) $y=-3x,\ y=\frac13x$",
  "s": r"(1) 2直線と $x$ 軸の正の向きのなす角を $\alpha,\beta$ とすると $\tan\alpha=3,\ \tan\beta=\frac12$。$\tan(\alpha-\beta)=\frac{3-\frac12}{1+3\cdot\frac12}=1$ より $\theta=\frac\pi4$。<br>(2) $\tan\alpha=2$ として、求める直線の傾きは $\tan\left(\alpha\pm\frac\pi4\right)$。$\frac{2+1}{1-2}=-3$、$\frac{2-1}{1+2}=\frac13$。<br><b>ポイント</b>：直線のなす角は「傾き $=\tan$（$x$ 軸となす角）」として $\tan$ の加法定理。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"(1) 加法定理を用いて、$\sin3\theta=3\sin\theta-4\sin^3\theta$ を証明せよ。<br>(2) $\theta=\dfrac\pi5$ のとき、$\sin3\theta=\sin2\theta$ が成り立つことを示せ。<br>(3) $\cos\dfrac\pi5$ と $\cos\dfrac{2\pi}5$ の値を求めよ。",
  "a": r"(1)(2) 略　(3) $\cos\frac\pi5=\frac{1+\sqrt5}4$、$\cos\frac{2\pi}5=\frac{\sqrt5-1}4$",
  "s": r"(1) $\sin3\theta=\sin(2\theta+\theta)=\sin2\theta\cos\theta+\cos2\theta\sin\theta=2\sin\theta\cos^2\theta+(1-2\sin^2\theta)\sin\theta=2\sin\theta(1-\sin^2\theta)+\sin\theta-2\sin^3\theta=3\sin\theta-4\sin^3\theta$。■<br>(2) $5\theta=\pi$ より $3\theta=\pi-2\theta$。$\sin3\theta=\sin(\pi-2\theta)=\sin2\theta$。■<br>(3) $3\sin\theta-4\sin^3\theta=2\sin\theta\cos\theta$。$\sin\theta\neq0$ で割って $3-4\sin^2\theta=2\cos\theta$、$3-4(1-\cos^2\theta)=2\cos\theta$、$4\cos^2\theta-2\cos\theta-1=0$。$\cos\theta=\frac{1\pm\sqrt5}{4}$、$\cos\frac\pi5>0$ より $\cos\frac\pi5=\frac{1+\sqrt5}4$。<br>$\cos\frac{2\pi}5=2\cos^2\frac\pi5-1=2\cdot\frac{6+2\sqrt5}{16}-1=\frac{\sqrt5-1}4$。<br><b>ポイント</b>：$5\theta=\pi$ を「$3\theta=\pi-2\theta$」と分けると、3倍角と2倍角で $\cos\theta$ の2次方程式になる。正五角形の対角線と辺の比（黄金比）とも関係する値。"},
 {"lv": "C", "tag": "証明", "q": r"(1) 加法定理を用いて、$\cos A+\cos B=2\cos\dfrac{A+B}2\cos\dfrac{A-B}2$ を示せ。<br>(2) $\triangle\mathrm{ABC}$ において $\cos A+\cos B+\cos C\leqq\dfrac32$ であることを証明し、等号が成り立つのはどのようなときか答えよ。<br>(3) $\triangle\mathrm{ABC}$ において $\cos A+\cos B+\cos C>1$ であることを証明せよ。",
  "a": r"(1) 略　(2) 等号は正三角形のとき　(3) 略",
  "s": r"(1) $p=\frac{A+B}2,\ q=\frac{A-B}2$ とおくと $A=p+q,\ B=p-q$。$\cos(p+q)+\cos(p-q)=2\cos p\cos q$。■<br>(2) $A+B=\pi-C$ より $\cos\frac{A+B}2=\cos\left(\frac\pi2-\frac C2\right)=\sin\frac C2$。また $\cos C=1-2\sin^2\frac C2$。$s=\sin\frac C2\ (>0)$ とおくと<br>$\cos A+\cos B+\cos C=2s\cos\frac{A-B}2+1-2s^2\leqq2s+1-2s^2=-2\left(s-\frac12\right)^2+\frac32\leqq\frac32$。<br>（$s>0$ と $\cos\frac{A-B}2\leqq1$ を用いた。）等号は $\cos\frac{A-B}2=1$ かつ $s=\frac12$、すなわち $A=B$ かつ $C=\frac\pi3$ のとき、つまり正三角形のとき。■<br>(3) (2) の式を $1+2s\left(\cos\frac{A-B}2-s\right)$ と変形する。$s=\cos\frac{A+B}2$ なので、加法定理より $\cos\frac{A-B}2-\cos\frac{A+B}2=2\sin\frac A2\sin\frac B2$。よって $\cos A+\cos B+\cos C=1+4\sin\frac A2\sin\frac B2\sin\frac C2$。$0<\frac A2,\frac B2,\frac C2<\frac\pi2$ より各 $\sin$ は正なので、$1$ より大きい。■<br><b>ポイント</b>：3つの角の和が $\pi$ という条件は、2つを和積でまとめ、残りの1つの半角で表すと1変数の評価になる。"},
]}}


def verify():
    th, s, t, A, B = symbols("theta s t A B", real=True)
    # A1
    assert 150*pi/180 == 5*pi/6 and 4*Rational(3, 4)*pi == 3*pi and Rational(1, 2)*16*Rational(3, 4)*pi == 6*pi
    assert cos(-Rational(11, 3)*pi) == Rational(1, 2) and tan(Rational(5, 4)*pi) == 1
    # A2
    assert simplify(sin(rad(75))-(sqrt(6)+sqrt(2))/4) == 0
    assert simplify(cos(rad(105))-(sqrt(2)-sqrt(6))/4) == 0
    assert simplify(tan(rad(15))-(2-sqrt(3))) == 0
    assert simplify((sqrt(3)-1)/(sqrt(3)+1) - (2-sqrt(3))) == 0
    # A3
    sols = solveset(2*cos(th)**2+3*sin(th)-3, th, Interval.Ropen(0, 2*pi))
    assert sols == FiniteSet(pi/6, pi/2, 5*pi/6)
    sol2 = solveset(2*cos(th)+sqrt(2) < 0, th, Interval.Ropen(0, 2*pi))
    assert sol2 == Interval.open(3*pi/4, 5*pi/4)
    # A4
    assert simplify(expand_trig(2*sin(th+pi/6)) - (sqrt(3)*sin(th)+cos(th))) == 0
    f = sqrt(3)*sin(th)+cos(th)
    assert maximum(f, th, Interval(0, pi)) == 2 and minimum(f, th, Interval(0, pi)) == -1
    assert f.subs(th, pi/3) == 2 and f.subs(th, pi) == -1
    # B1
    sv = Rational(3, 5); cv = -Rational(4, 5)
    assert 2*sv*cv == -Rational(24, 25) and 1-2*sv**2 == Rational(7, 25) and sv/(1+cv) == 3
    th0 = pi-asin(Rational(3, 5))
    assert abs(N(tan(th0/2))-3) < 1e-12 and abs(N(sin(2*th0))+0.96) < 1e-12
    # B2
    y = cos(2*th)+2*sin(th)
    assert expand(expand_trig(y).subs(cos(th)**2, 1-sin(th)**2)).subs(sin(th), s) == -2*s**2+2*s+1
    assert maximum(y, th, Interval.Ropen(0, 2*pi)) == Rational(3, 2) and minimum(y, th, Interval.Ropen(0, 2*pi)) == -3
    assert y.subs(th, pi/6) == Rational(3, 2) and y.subs(th, 5*pi/6) == Rational(3, 2) and y.subs(th, 3*pi/2) == -3
    # B3
    y3 = 2*sin(th)*cos(th)+2*(sin(th)+cos(th))-1
    assert simplify(y3 - ((sin(th)+cos(th))**2+2*(sin(th)+cos(th))-2)) == 0
    import math
    vals = [(math.sin(2*x)+2*(math.sin(x)+math.cos(x))-1, x) for x in [2*math.pi*i/20000 for i in range(20000)]]
    mx, mn = max(vals), min(vals)
    assert abs(mx[0]-2*math.sqrt(2)) < 1e-6 and abs(mx[1]-math.pi/4) < 1e-3 and abs(mn[0]+3) < 1e-6
    for xv in [pi, 3*pi/2]:
        assert simplify(y3.subs(th, xv)+3) == 0
    assert simplify(y3.subs(th, pi/4)-2*sqrt(2)) == 0
    # B4: 解の個数を数値的に数える
    def count(av):
        rs = []
        for r in solve(-s**2+s+1-av, s):
            if r.is_real and -1 <= r <= 1:
                rs.append(r)
        n = 0
        for r in set(rs):
            n += 1 if r in (1, -1) else 2
        return n
    table = {Rational(-3, 2): 0, -1: 1, Rational(-1, 2): 2, 0: 2, Rational(1, 2): 2, 1: 3, Rational(9, 8): 4, Rational(6, 5): 4, Rational(5, 4): 2, Rational(3, 2): 0}
    for av, n in table.items():
        assert count(av) == n, av
    # B5
    assert Rational(3-Rational(1, 2))/(1+Rational(3, 2)) == 1
    assert Rational(2+1, 1-2) == -3 and Rational(2-1, 1+2) == Rational(1, 3)
    # C1
    assert simplify(expand_trig(sin(3*th)) - (3*sin(th)-4*sin(th)**3)) == 0
    assert simplify(sin(3*pi/5)-sin(2*pi/5)) == 0
    c = symbols("c")
    assert set(solve(4*c**2-2*c-1, c)) == {(1+sqrt(5))/4, (1-sqrt(5))/4}
    assert simplify(cos(pi/5)-(1+sqrt(5))/4) == 0 and simplify(cos(2*pi/5)-(sqrt(5)-1)/4) == 0
    assert simplify(2*((1+sqrt(5))/4)**2-1 - (sqrt(5)-1)/4) == 0
    # C2
    assert simplify(expand_trig(cos((A+B)/2+(A-B)/2)+cos((A+B)/2-(A-B)/2)) - 2*cos((A+B)/2)*cos((A-B)/2)) == 0
    assert simplify(expand_trig(cos((A-B)/2)-cos((A+B)/2) - 2*sin(A/2)*sin(B/2))) == 0
    import random
    random.seed(5)
    for _ in range(2000):
        a1, b1 = random.random()*math.pi, random.random()*math.pi
        if a1+b1 >= math.pi:
            continue
        c1 = math.pi-a1-b1
        tot = math.cos(a1)+math.cos(b1)+math.cos(c1)
        assert 1 < tot <= 1.5+1e-12
        assert abs(tot-(1+4*math.sin(a1/2)*math.sin(b1/2)*math.sin(c1/2))) < 1e-12
    assert abs(3*math.cos(math.pi/3)-1.5) < 1e-15
