"""問題集 第11章 図形と方程式。CH に問題、verify() で答えを sympy・数値で検算する。"""
from sympy import *


def _U(x):  # 通過領域の上側の境界
    return 0 if x < 0 else (x * x if x <= 1 else 2 * x - 1)


def _L(x):  # 下側の境界
    return 2 * x - 1 if x <= 0.5 else 0


def _fig_region():
    u, ox, oy = 36, 52, 92
    X = lambda x: ox + u * x
    Y = lambda y: oy - u * y
    xs = [-0.6 + i * 0.025 for i in range(89)]  # -0.6〜1.6
    up = [f"{X(x):.1f},{Y(_U(x)):.1f}" for x in xs]
    lo = [f"{X(x):.1f},{Y(_L(x)):.1f}" for x in reversed(xs)]
    s = ['<svg class="fig" width="210" height="186" viewBox="0 0 210 186">',
         f'<polygon points="{" ".join(up + lo)}" fill="#cfdcf5" stroke="none"/>',
         f'<polyline points="{" ".join(up)}" fill="none" stroke="#1f3f8f" stroke-width="1.5"/>',
         f'<polyline points="{" ".join(lo)}" fill="none" stroke="#1f3f8f" stroke-width="1.5"/>',
         f'<line x1="{X(-0.9)}" y1="{Y(0)}" x2="{X(2.0)}" y2="{Y(0)}" stroke="#333"/>',
         f'<line x1="{X(0)}" y1="{Y(-2.4)}" x2="{X(0)}" y2="{Y(2.4)}" stroke="#333"/>',
         f'<polyline points="{" ".join(f"{X(x):.1f},{Y(x * x):.1f}" for x in [-0.6 + i * 0.05 for i in range(45)])}" fill="none" stroke="#999" stroke-dasharray="3,3"/>',
         f'<text x="{X(0) - 11}" y="{Y(0) + 12}" font-size="10">O</text>',
         f'<text x="{X(1) - 3}" y="{Y(0) + 12}" font-size="10">1</text>',
         f'<text x="{X(0.5) - 7}" y="{Y(0) - 11}" font-size="9">1/2</text>',
         f'<text x="{X(0) + 4}" y="{Y(-1) + 4}" font-size="10">−1</text>',
         f'<text x="{X(1.9)}" y="{Y(0) + 13}" font-size="11">x</text>',
         f'<text x="{X(0) + 4}" y="{Y(2.3)}" font-size="11">y</text>',
         f'<text x="{X(1.68)}" y="{Y(2.2) + 4}" font-size="10">y=2x−1</text>',
         f'<text x="{X(-0.95)}" y="{Y(0.55)}" font-size="10">y=x²</text>',
         '</svg>']
    return "".join(s)


CH = {11: {
"goal": "点・直線・円の方程式を正確に扱い、距離の公式・円と直線の位置関係・軌跡・領域の処理を身につける。文字定数を含む図形は「固定して考える」「通過する条件を方程式の実数解に言い換える」。",
"items": [
 {"lv": "A", "q": r"2点 $\mathrm A(1,\,2),\ \mathrm B(5,\,-4)$ について、線分 $\mathrm{AB}$ の長さ、線分 $\mathrm{AB}$ を $2:1$ に内分する点、$2:1$ に外分する点の座標を求めよ。",
  "a": r"$\mathrm{AB}=2\sqrt{13}$、内分点 $\left(\frac{11}{3},\,-2\right)$、外分点 $(9,\,-10)$",
  "s": r"$\mathrm{AB}=\sqrt{4^2+(-6)^2}=\sqrt{52}=2\sqrt{13}$。内分点：$\left(\frac{1\cdot1+2\cdot5}{3},\ \frac{1\cdot2+2\cdot(-4)}{3}\right)=\left(\frac{11}3,\,-2\right)$。外分点：$\left(\frac{-1\cdot1+2\cdot5}{2-1},\ \frac{-1\cdot2+2\cdot(-4)}{2-1}\right)=(9,\,-10)$。<br><b>ポイント</b>：$m:n$ の外分は内分の公式で $n$ を $-n$ に置き換える。"},
 {"lv": "A", "q": r"(1) 点 $(2,\,3)$ を通り、直線 $2x-y+1=0$ に平行な直線、垂直な直線の方程式をそれぞれ求めよ。<br>(2) 点 $(2,\,3)$ と直線 $3x+4y-3=0$ の距離を求めよ。",
  "a": r"(1) 平行 $2x-y-1=0$、垂直 $x+2y-8=0$　(2) $3$",
  "s": r"(1) 傾きは $2$。平行：$y-3=2(x-2)$ より $2x-y-1=0$。垂直：傾き $-\frac12$ で $y-3=-\frac12(x-2)$ より $x+2y-8=0$。<br>(2) $\frac{|3\cdot2+4\cdot3-3|}{\sqrt{3^2+4^2}}=\frac{15}5=3$。<br><b>ポイント</b>：$ax+by+c=0$ に平行な直線は $ax+by+c'=0$、垂直な直線は $bx-ay+c''=0$ とおける。"},
 {"lv": "A", "q": r"(1) 円 $x^2+y^2-4x+6y-12=0$ の中心と半径を求めよ。<br>(2) 3点 $(0,\,0),\ (4,\,0),\ (0,\,2)$ を通る円の方程式を求め、その中心と半径を答えよ。",
  "a": r"(1) 中心 $(2,\,-3)$、半径 $5$　(2) $x^2+y^2-4x-2y=0$、中心 $(2,\,1)$、半径 $\sqrt5$",
  "s": r"(1) $(x-2)^2+(y+3)^2=12+4+9=25$。<br>(2) $x^2+y^2+lx+my+n=0$ に代入：$(0,0)$ から $n=0$、$(4,0)$ から $16+4l=0$、$l=-4$、$(0,2)$ から $4+2m=0$、$m=-2$。$(x-2)^2+(y-1)^2=5$。<br><b>ポイント</b>：3点を通る円は一般形 $x^2+y^2+lx+my+n=0$ に代入。直角三角形なら斜辺が直径になることも使える（ここでは $(4,0)$ と $(0,2)$ が直径の両端）。"},
 {"lv": "A", "q": r"円 $x^2+y^2=5$ について、<br>(1) 円上の点 $(1,\,2)$ における接線の方程式を求めよ。<br>(2) 直線 $y=x+k$ が円と共有点をもつような定数 $k$ の値の範囲を求めよ。",
  "a": r"(1) $x+2y=5$　(2) $-\sqrt{10}\leqq k\leqq\sqrt{10}$",
  "s": r"(1) 円 $x^2+y^2=r^2$ 上の点 $(x_1,y_1)$ における接線は $x_1x+y_1y=r^2$ なので $x+2y=5$。<br>(2) 中心 $(0,0)$ と直線 $x-y+k=0$ の距離 $\frac{|k|}{\sqrt2}$ が半径 $\sqrt5$ 以下：$|k|\leqq\sqrt{10}$。<br><b>ポイント</b>：円と直線の位置関係は「中心と直線の距離 $d$ と半径 $r$ の比較」が計算が軽い。"},
 {"lv": "B", "tag": "軌跡", "q": r"2点 $\mathrm A(-2,\,0),\ \mathrm B(4,\,0)$ からの距離の比が $\mathrm{PA}:\mathrm{PB}=2:1$ である点 $\mathrm P$ の軌跡を求めよ。",
  "a": r"中心 $(6,\,0)$、半径 $4$ の円 $(x-6)^2+y^2=16$",
  "s": r"$\mathrm P(x,y)$ とすると $\mathrm{PA}=2\mathrm{PB}$ より $\mathrm{PA}^2=4\mathrm{PB}^2$：$(x+2)^2+y^2=4\{(x-4)^2+y^2\}$。整理して $3x^2-36x+3y^2+60=0$、$x^2-12x+y^2+20=0$、$(x-6)^2+y^2=16$。逆にこの円上の点は条件を満たす。<br>（確認：$\mathrm{AB}$ を $2:1$ に内分する点 $(2,0)$ と外分する点 $(10,0)$ がこの円の直径の両端。）<br><b>ポイント</b>：距離の比が一定（$\neq1$）の点の軌跡は円（アポロニウスの円）。距離は2乗して根号を外す。"},
 {"lv": "B", "q": r"点 $(3,\,1)$ から円 $x^2+y^2=5$ に引いた2本の接線の方程式と、2つの接点を通る直線の方程式を求めよ。",
  "a": r"接線 $x+2y=5,\ 2x-y=5$、接点を通る直線 $3x+y=5$",
  "s": r"接点を $(a,b)$ とすると接線は $ax+by=5$。これが $(3,1)$ を通るので $3a+b=5$。また $a^2+b^2=5$。$b=5-3a$ を代入して $10a^2-30a+20=0$、$a^2-3a+2=0$、$a=1,2$。接点 $(1,2),\ (2,-1)$、接線 $x+2y=5,\ 2x-y=5$。<br>接点はどちらも $3a+b=5$ を満たすので、2接点を通る直線は $3x+y=5$。<br><b>ポイント</b>：接点を文字でおき、「接線が通る」条件と「接点が円上」の条件を連立。接点を結ぶ直線（極線）は $x_0x+y_0y=r^2$ とすぐ書ける。"},
 {"lv": "B", "q": r"円 $C:\ x^2+y^2-2x-4y-20=0$ と直線 $\ell:\ 4x+3y-25=0$ について、<br>(1) $C$ の中心と $\ell$ の距離を求めよ。　(2) $\ell$ が $C$ から切り取る弦の長さを求めよ。<br>(3) その弦の中点の座標を求めよ。",
  "a": r"(1) $3$　(2) $8$　(3) $\left(\frac{17}5,\,\frac{19}5\right)$",
  "s": r"$C:\ (x-1)^2+(y-2)^2=25$、中心 $(1,2)$、半径 $5$。<br>(1) $\frac{|4+6-25|}{5}=3$。(2) 三平方の定理で $2\sqrt{5^2-3^2}=8$。<br>(3) 中点は中心から $\ell$ に下ろした垂線の足。$\ell$ の法線方向 $(4,3)$ に沿って $(1+4t,\ 2+3t)$ を $\ell$ に代入：$4(1+4t)+3(2+3t)=25$、$25t=15$、$t=\frac35$。中点は $\left(\frac{17}5,\ \frac{19}5\right)$。<br><b>ポイント</b>：弦の長さは交点を求めず「半径・距離・半弦」の直角三角形で。弦の中点は中心からの垂線の足。"},
 {"lv": "B", "q": r"2つの円 $C_1:\ x^2+y^2=4$、$C_2:\ x^2+y^2-2x-4y+1=0$ について、<br>(1) 2円の交点を通る直線の方程式と、共通弦の長さを求めよ。<br>(2) 2円の交点と点 $(0,\,1)$ を通る円の方程式を求めよ。",
  "a": r"(1) $2x+4y-5=0$、長さ $\sqrt{11}$　(2) $x^2+y^2-6x-12y+11=0$",
  "s": r"$C_2:\ (x-1)^2+(y-2)^2=4$。中心間の距離 $\sqrt5$ は $0<\sqrt5<4$ なので2点で交わる。<br>(1) $C_1-C_2$ より $2x+4y-5=0$（交点はこの直線上にある）。原点との距離は $\frac5{\sqrt{20}}=\frac{\sqrt5}2$ なので弦の長さは $2\sqrt{4-\frac54}=\sqrt{11}$。<br>(2) 2円の交点を通る円は $x^2+y^2-4+k(2x+4y-5)=0$ と表せる。$(0,1)$ を代入して $1-4+k(4-5)=0$、$k=-3$。$x^2+y^2-6x-12y+11=0$。<br><b>ポイント</b>：「$f=0$ と $g=0$ の交点を通る図形」は $f+kg=0$ とおく。$k$ によらず交点を通ることが根拠。"},
 {"lv": "B", "tag": "領域", "q": r"連立不等式 $x\geqq0,\ y\geqq0,\ x+2y\leqq8,\ 3x+y\leqq9$ の表す領域を $D$ とする。点 $(x,y)$ が $D$ 内を動くとき、<br>(1) $x+y$ の最大値を求めよ。　(2) $x^2+y^2$ の最大値と最小値を求めよ。<br>(3) $a$ を実数とする。$ax+y$ が点 $(2,\,3)$ で最大値をとるような $a$ の範囲を求めよ。",
  "a": r"(1) $5$（$(2,3)$）　(2) 最大値 $16$（$(0,4)$）、最小値 $0$（$(0,0)$）　(3) $\frac12\leqq a\leqq3$",
  "s": r"$D$ は4点 $(0,0),\ (3,0),\ (2,3),\ (0,4)$ を頂点とする四角形（周を含む）。$(2,3)$ は2直線 $x+2y=8$ と $3x+y=9$ の交点。<br>(1) $x+y=k$ は傾き $-1$ の直線。傾き $-1$ は2辺の傾き $-\frac12$ と $-3$ の間なので、頂点 $(2,3)$ を通るとき $k$ が最大で $5$。<br>(2) $x^2+y^2$ は原点からの距離の2乗。最も遠いのは頂点のうち $(0,4)$（$16$、他は $9,\ 13$）、最も近いのは原点で $0$。<br>(3) 直線 $y=-ax+k$ の傾き $-a$ が、$(2,3)$ で交わる2辺の傾き $-3$ 以上 $-\frac12$ 以下であればよい。$-3\leqq-a\leqq-\frac12$ より $\frac12\leqq a\leqq3$。（各頂点での値 $0,\ 3a,\ 2a+3,\ 4$ を比べても同じ結果。）<br><b>ポイント</b>：1次式の最大・最小は「傾きの比較」。境界の直線の傾きと目的の直線の傾きを並べて判断する。"},
 {"lv": "C", "tag": "軌跡", "q": r"放物線 $y=x^2$ と、点 $(1,\,0)$ を通る傾き $m$ の直線 $\ell$ が異なる2点 $\mathrm P,\ \mathrm Q$ で交わるとする。<br>(1) $m$ の値の範囲を求めよ。　(2) 線分 $\mathrm{PQ}$ の中点 $\mathrm M$ の軌跡を求めよ。",
  "a": r"(1) $m<0,\ 4<m$　(2) 放物線 $y=2x^2-2x$ の $x<0,\ 2<x$ の部分",
  "s": r"(1) $\ell:\ y=m(x-1)$。$x^2=m(x-1)$ すなわち $x^2-mx+m=0$ …① が異なる2実数解をもつ条件は $D=m^2-4m>0$、$m<0,\ 4<m$。<br>(2) ①の2解を $\alpha,\beta$ とすると $\mathrm M$ の $x$ 座標は $X=\frac{\alpha+\beta}2=\frac m2$、$\mathrm M$ は $\ell$ 上にあるので $Y=m(X-1)$。$m=2X$ を代入して $Y=2X(X-1)=2X^2-2X$。$m$ の範囲から $X<0,\ 2<X$。<br>よって軌跡は放物線 $y=2x^2-2x$ のうち $x<0,\ 2<x$ の部分。<br><b>ポイント</b>：媒介変数 $m$ を消去したら、$m$ のとりうる範囲を $X$ の範囲に翻訳して「除外点・除外部分」を必ず書く。"},
 {"lv": "C", "tag": "通過領域", "q": r"$a$ が $0\leqq a\leqq1$ の範囲を動くとき、直線 $\ell_a:\ y=2ax-a^2$ が通過する領域を求め、図示せよ。",
  "a": r"$x\leqq0$ のとき $2x-1\leqq y\leqq0$、$0\leqq x\leqq\frac12$ のとき $2x-1\leqq y\leqq x^2$、$\frac12\leqq x\leqq1$ のとき $0\leqq y\leqq x^2$、$x\geqq1$ のとき $0\leqq y\leqq2x-1$",
  "s": r"$x$ を固定し、$a$ を $0\leqq a\leqq1$ で動かしたときの $y=f(a)=2ax-a^2=-(a-x)^2+x^2$ の値域を求める（点 $(x,y)$ を通る $\ell_a$ が存在する $\iff$ $y$ がこの値域に入る）。$f(0)=0,\ f(1)=2x-1$。<br>・$x\leqq0$：$f$ は $[0,1]$ で減少。$2x-1\leqq y\leqq0$。<br>・$0\leqq x\leqq1$：最大は頂点 $f(x)=x^2$、最小は $f(0),\ f(1)$ の小さい方。$x\leqq\frac12$ なら $2x-1$、$x\geqq\frac12$ なら $0$。<br>・$x\geqq1$：$f$ は $[0,1]$ で増加。$0\leqq y\leqq2x-1$。<br>図の色の部分（境界を含む）。" + _fig_region() + r"直線 $y=0$（$a=0$）と $y=2x-1$（$a=1$）は放物線 $y=x^2$ の $x=0,\ x=1$ における接線で、$\ell_a$ は $y=x^2$ の $x=a$ における接線になっている。<br><b>ポイント</b>：通過領域は「$x$ を固定して $y$ の値域を調べる」（または「$a$ の方程式が範囲内に解をもつ条件」）。端点 $a=0,1$ と頂点 $a=x$ のどれが最大・最小を与えるかで場合分けする。"},
]}}


def verify():
    x, y, k, m, t, a = symbols("x y k m t a", real=True)
    # A1
    A = Matrix([1, 2]); B = Matrix([5, -4])
    assert (B-A).norm() == 2*sqrt(13)
    assert (A+2*B)/3 == Matrix([Rational(11, 3), -2]) and (-A+2*B)/1 == Matrix([9, -10])
    # A2
    assert 2*2-3-1 == 0 and 2+2*3-8 == 0
    assert Matrix([2, -1]).dot(Matrix([1, 2])) == 0  # 法線ベクトルが直交 → 2直線は垂直
    assert Matrix([2, -1, 0]).cross(Matrix([2, -1, 0])) == Matrix([0, 0, 0])  # 法線が平行 → 平行
    assert Rational(abs(3*2+4*3-3), 5) == 3
    # A3
    assert expand((x-2)**2+(y+3)**2-25 - (x**2+y**2-4*x+6*y-12)) == 0
    c = x**2+y**2-4*x-2*y
    assert all(c.subs({x: p, y: q}) == 0 for p, q in [(0, 0), (4, 0), (0, 2)])
    assert expand((x-2)**2+(y-1)**2-5 - c) == 0
    # A4
    sol = solve([x**2+y**2-5, x+2*y-5], [x, y], dict=True)
    assert sol == [{x: 1, y: 2}]
    for kv, n in [(sqrt(10), 1), (-sqrt(10), 1), (3, 2), (4, 0)]:
        assert len(solve([x**2+y**2-5, y-x-kv], [x, y], dict=True)) == n
    # B1
    lhs = (x+2)**2+y**2-4*((x-4)**2+y**2)
    assert expand(lhs + 3*((x-6)**2+y**2-16)) == 0
    for p, q in [(2, 0), (10, 0), (6, 4), (6, -4)]:
        assert (p+2)**2+q**2 == 4*((p-4)**2+q**2)
    # B2
    sol = solve([x**2+y**2-5, 3*x+y-5], [x, y], dict=True)
    assert {(s[x], s[y]) for s in sol} == {(1, 2), (2, -1)}
    assert 3+2*1 == 5 and 2*3-1 == 5
    # B3
    assert expand((x-1)**2+(y-2)**2-25 - (x**2+y**2-2*x-4*y-20)) == 0
    pts = solve([x**2+y**2-2*x-4*y-20, 4*x+3*y-25], [x, y], dict=True)
    P1, P2 = [Matrix([s[x], s[y]]) for s in pts]
    assert simplify((P1-P2).norm()-8) == 0 and (P1+P2)/2 == Matrix([Rational(17, 5), Rational(19, 5)])
    # B4
    c1 = x**2+y**2-4; c2 = x**2+y**2-2*x-4*y+1
    pts = solve([c1, c2], [x, y], dict=True)
    assert len(pts) == 2
    P1, P2 = [Matrix([s[x], s[y]]) for s in pts]
    assert all(simplify(2*s[x]+4*s[y]-5) == 0 for s in pts)
    assert simplify((P1-P2).norm()-sqrt(11)) == 0
    c3 = x**2+y**2-6*x-12*y+11
    assert c3.subs({x: 0, y: 1}) == 0 and all(simplify(c3.subs(s)) == 0 for s in pts)
    assert expand(c1-3*(2*x+4*y-5) - c3) == 0
    # B5
    V = [(0, 0), (3, 0), (2, 3), (0, 4)]
    inD = lambda p, q: p >= 0 and q >= 0 and p+2*q <= 8 and 3*p+q <= 9
    assert all(inD(*v) for v in V)
    grid = [(Rational(i, 10), Rational(j, 10)) for i in range(0, 41) for j in range(0, 41) if inD(Rational(i, 10), Rational(j, 10))]
    assert max(p+q for p, q in grid) == 5
    assert max(p*p+q*q for p, q in grid) == 16 and min(p*p+q*q for p, q in grid) == 0
    for av in [Rational(n, 8) for n in range(-40, 40)]:
        vals = [av*p+q for p, q in V]
        assert (av*2+3 == max(vals)) == (Rational(1, 2) <= av <= 3), av
    # C1
    assert solve_univariate_inequality(m**2-4*m > 0, m, relational=False) == Union(Interval.open(-oo, 0), Interval.open(4, oo))
    for mv in [-3, -1, Rational(-1, 2), 5, 7, 10]:
        r1, r2 = solve(x**2-mv*x+mv, x)
        X = (r1+r2)/2; Y = mv*(X-1)
        assert simplify(Y-(2*X**2-2*X)) == 0 and (X < 0 or X > 2)
    for mv in [0, 1, 2, 3, 4]:
        assert mv**2-4*mv <= 0
    # C2: 格子点 (x,y) について、0<=a<=1 の範囲に y=2ax-a^2 の解 a があるかを直接判定
    import math
    def passes(xv, yv):
        # a^2 - 2 x a + y = 0 の実数解が [0,1] にあるか
        D = xv*xv-yv
        if D < 0:
            return False
        r = math.sqrt(D)
        return any(-1e-12 <= av <= 1+1e-12 for av in (xv-r, xv+r))
    def region(xv, yv):
        if xv <= 0: return 2*xv-1-1e-12 <= yv <= 1e-12
        if xv <= 0.5: return 2*xv-1-1e-12 <= yv <= xv*xv+1e-12
        if xv <= 1: return -1e-12 <= yv <= xv*xv+1e-12
        return -1e-12 <= yv <= 2*xv-1+1e-12
    for i in range(-30, 41):
        for j in range(-60, 61):
            xv, yv = i/20+0.0013, j/20+0.0007
            assert passes(xv, yv) == region(xv, yv), (xv, yv)
    # 図の境界関数が答えと一致
    assert _U(-0.5) == 0 and _U(0.5) == 0.25 and _U(1.5) == 2.0 and _L(-0.5) == -2.0 and _L(0.75) == 0
