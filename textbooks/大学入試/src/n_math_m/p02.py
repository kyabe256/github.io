"""問題集 第2章 2次関数。CH に問題、verify() で答えを sympy・総当たりで検算する。"""
from sympy import *


def _fig_abs():
    """y=|x^2-2x-3| と y=k のグラフ（座標は計算で出す）"""
    ox, oy, sx, sy = 72, 138, 30, 22
    X = lambda x: ox + sx * x
    Y = lambda y: oy - sy * y
    pts = " ".join(f"{X(-2.1 + i * 0.05):.1f},{Y(abs((-2.1 + i * 0.05) ** 2 - 2 * (-2.1 + i * 0.05) - 3)):.1f}" for i in range(125))
    s = [f'<svg class="fig" width="240" height="160" viewBox="0 0 240 160">',
         f'<line x1="{X(-2.3)}" y1="{Y(0)}" x2="{X(4.6)}" y2="{Y(0)}" stroke="#333"/>',
         f'<line x1="{X(0)}" y1="{Y(-0.8)}" x2="{X(0)}" y2="{Y(5.9)}" stroke="#333"/>',
         f'<polyline points="{pts}" fill="none" stroke="#1f3f8f" stroke-width="1.8"/>',
         f'<line x1="{X(-2.3)}" y1="{Y(4)}" x2="{X(4.6)}" y2="{Y(4)}" stroke="#c0392b" stroke-dasharray="4,3"/>',
         f'<line x1="{X(-2.3)}" y1="{Y(2)}" x2="{X(4.6)}" y2="{Y(2)}" stroke="#d27a00" stroke-dasharray="4,3"/>',
         f'<text x="{X(4.65)}" y="{Y(4) + 4}" font-size="10">y=4</text>',
         f'<text x="{X(4.65)}" y="{Y(2) + 4}" font-size="10">y=k</text>',
         f'<text x="{X(4.4)}" y="{Y(0) + 13}" font-size="11">x</text>',
         f'<text x="{X(0) + 4}" y="{Y(5.7)}" font-size="11">y</text>',
         f'<text x="{X(0) - 11}" y="{Y(0) + 12}" font-size="10">O</text>',
         f'<text x="{X(-1) - 9}" y="{Y(0) + 12}" font-size="10">−1</text>',
         f'<text x="{X(3) - 3}" y="{Y(0) + 12}" font-size="10">3</text>',
         f'<text x="{X(1) - 3}" y="{Y(0) + 12}" font-size="10">1</text>',
         f'<line x1="{X(1)}" y1="{Y(0)}" x2="{X(1)}" y2="{Y(4)}" stroke="#999" stroke-dasharray="2,2"/>',
         '</svg>']
    return "".join(s)


CH = {2: {
"goal": "平方完成でグラフを正確につかむ。軸と区間の位置関係による場合分け、解の配置、グラフを使った解の個数の判定を身につける。",
"items": [
 {"lv": "A", "q": r"2次関数 $y=2x^2-8x+5$ について、次の問いに答えよ。<br>(1) グラフの頂点と軸を求めよ。<br>(2) $0\leqq x\leqq3$ における最大値と最小値を求めよ。<br>(3) グラフを $x$ 軸方向に $-1$、$y$ 軸方向に $3$ だけ平行移動した放物線の方程式を求めよ。",
  "a": r"(1) 頂点 $(2,-3)$、軸 $x=2$　(2) 最大値 $5$（$x=0$）、最小値 $-3$（$x=2$）　(3) $y=2x^2-4x+2$",
  "s": r"(1) $y=2(x^2-4x)+5=2(x-2)^2-3$。(2) 軸 $x=2$ は区間に含まれるので最小値は $-3$。端の値は $x=0$ で $5$、$x=3$ で $-1$ なので、軸から遠い $x=0$ で最大値 $5$。(3) $x$ を $x+1$ に、$y$ を $y-3$ に置き換えて $y-3=2(x+1-2)^2-3$、すなわち $y=2(x-1)^2=2x^2-4x+2$。頂点が $(2,-3)$ から $(1,0)$ に移ると考えても同じ。<br><b>ポイント</b>：平行移動は「頂点の移動」で考えると速く確実。"},
 {"lv": "A", "q": r"3点 $(-1,\,0),\ (3,\,0),\ (0,\,6)$ を通る放物線をグラフとする2次関数を求めよ。また、その最大値を求めよ。",
  "a": r"$y=-2x^2+4x+6$、最大値 $8$（$x=1$）",
  "s": r"$x$ 軸との交点が $x=-1,3$ なので $y=a(x+1)(x-3)$ とおける。$(0,6)$ を通るから $-3a=6$、$a=-2$。$y=-2(x+1)(x-3)=-2x^2+4x+6=-2(x-1)^2+8$。<br><b>ポイント</b>：$x$ 軸との交点がわかっているときは $y=a(x-\alpha)(x-\beta)$ とおくと未知数が1つで済む。"},
 {"lv": "A", "q": r"次の2次不等式を解け。<br>(1) $x^2-x-6<0$　(2) $2x^2-3x-2\geqq0$　(3) $x^2-4x+5>0$　(4) $4x^2-4x+1\leqq0$",
  "a": r"(1) $-2<x<3$　(2) $x\leqq-\frac12,\ 2\leqq x$　(3) すべての実数　(4) $x=\frac12$",
  "s": r"(1) $(x+2)(x-3)<0$。(2) $(2x+1)(x-2)\geqq0$ より、2解 $-\frac12,\ 2$ の外側。(3) $(x-2)^2+1>0$ は常に成り立つ。(4) $(2x-1)^2\leqq0$ を満たすのは $2x-1=0$ のときだけ。<br><b>ポイント</b>：判別式が $0$ 以下のときは平方完成してグラフと $x$ 軸の位置を見る。"},
 {"lv": "A", "q": r"2次方程式 $x^2+2(k-1)x+k+5=0$ が重解をもつような定数 $k$ の値と、そのときの重解を求めよ。",
  "a": r"$k=4$ のとき重解 $x=-3$、$k=-1$ のとき重解 $x=2$",
  "s": r"$\frac D4=(k-1)^2-(k+5)=k^2-3k-4=(k-4)(k+1)=0$ より $k=4,\,-1$。重解は $x=-(k-1)$ なので、$k=4$ のとき $x=-3$、$k=-1$ のとき $x=2$。<br><b>ポイント</b>：重解は解の公式で根号の中が $0$ のときの値 $x=-\frac{b}{2a}$。"},
 {"lv": "B", "tag": "頻出", "q": r"$a$ を定数とする。関数 $f(x)=x^2-2ax+3\ (0\leqq x\leqq2)$ について、<br>(1) 最小値 $m(a)$ を求めよ。　(2) 最大値 $M(a)$ を求めよ。",
  "a": r"(1) $a<0$ のとき $3$、$0\leqq a\leqq2$ のとき $3-a^2$、$a>2$ のとき $7-4a$<br>(2) $a<1$ のとき $7-4a$、$a\geqq1$ のとき $3$",
  "s": r"$f(x)=(x-a)^2+3-a^2$、軸は $x=a$。$f(0)=3,\ f(2)=7-4a$。<br>(1) 軸が区間の左（$a<0$）なら $x=0$ で最小、区間内（$0\leqq a\leqq2$）なら頂点で最小 $3-a^2$、右（$a>2$）なら $x=2$ で最小 $7-4a$。<br>(2) 最大は軸から遠い端でとる。区間の中央 $x=1$ と軸を比べ、$a<1$ なら $x=2$ で $7-4a$、$a>1$ なら $x=0$ で $3$、$a=1$ のときは両端で $3$。<br><b>ポイント</b>：最小は「軸が区間の左・中・右」、最大は「軸が区間の中央の左・右」で場合分けする。"},
 {"lv": "B", "tag": "解の配置", "q": r"2次方程式 $x^2-2ax+a+6=0$ について、次の条件を満たす定数 $a$ の値の範囲を求めよ。<br>(1) 異なる2つの正の解をもつ。<br>(2) 1つの解は $1$ より大きく、他の解は $1$ より小さい。",
  "a": r"(1) $a>3$　(2) $a>7$",
  "s": r"$f(x)=x^2-2ax+a+6$ とおく。<br>(1) 次の3条件を同時に満たせばよい。判別式：$\frac D4=a^2-a-6=(a-3)(a+2)>0$ より $a<-2,\ 3<a$。軸：$a>0$。端点：$f(0)=a+6>0$ より $a>-6$。共通部分は $a>3$。<br>(2) 下に凸の放物線が $x=1$ の左右で $x$ 軸と交わる条件は $f(1)<0$。$f(1)=1-2a+a+6=7-a<0$ より $a>7$。<br><b>ポイント</b>：解の配置は「判別式・軸・端点の値」の3点セット。ただし「ある値をはさむ」ときは $f(k)<0$ だけでよい。"},
 {"lv": "B", "q": r"$a$ を定数とする。$x$ の不等式 $x^2-(a+2)x+2a<0$ を満たす整数 $x$ がちょうど3個となるような $a$ の値の範囲を求めよ。",
  "a": r"$-2\leqq a<-1,\ \ 5<a\leqq6$",
  "s": r"左辺は $(x-2)(x-a)$ と因数分解できる。<br>・$a>2$ のとき解は $2<x<a$。整数 $3,4,5$ の3個だけを含むには $5<a\leqq6$（$a=6$ のとき $6$ は含まれない）。<br>・$a<2$ のとき解は $a<x<2$。整数 $1,0,-1$ の3個だけを含むには $-2\leqq a<-1$。<br>・$a=2$ のときは $(x-2)^2<0$ となり解なし。<br><b>ポイント</b>：端点を含むかどうか（等号の有無）は、境目の値を実際に代入して確かめる。"},
 {"lv": "B", "q": r"$x\geqq0,\ y\geqq0,\ x+y=3$ のとき、$2x^2+y^2$ の最大値と最小値、およびそのときの $x,\ y$ の値を求めよ。",
  "a": r"最大値 $18$（$x=3,\ y=0$）、最小値 $6$（$x=1,\ y=2$）",
  "s": r"$y=3-x$ を代入。$y\geqq0$ より $x\leqq3$ なので変域は $0\leqq x\leqq3$。$2x^2+(3-x)^2=3x^2-6x+9=3(x-1)^2+6$。$x=1$ で最小値 $6$（$y=2$）。端は $x=0$ で $9$、$x=3$ で $18$ なので、最大値は $18$（$y=0$）。<br><b>ポイント</b>：1文字を消去したら、残った文字の<b>変域</b>を必ず求める。"},
 {"lv": "B", "tag": "グラフの利用", "q": r"$k$ を定数とする。方程式 $|x^2-2x-3|=k$ の異なる実数解の個数を調べよ。",
  "a": r"$k<0$ のとき $0$ 個、$k=0$ のとき $2$ 個、$0<k<4$ のとき $4$ 個、$k=4$ のとき $3$ 個、$k>4$ のとき $2$ 個",
  "s": r"$y=|x^2-2x-3|$ のグラフと直線 $y=k$ の共有点の個数を数える。$x^2-2x-3=(x-1)^2-4$ なので、$x$ 軸より下にある部分（$-1<x<3$）を折り返すと、$x=1$ で高さ $4$ の山ができる。" + _fig_abs() + r"図より、$0<k<4$ では4点、$k=4$ では山の頂上を含めて3点、$k=0$ と $k>4$ では2点で交わる。<br><b>ポイント</b>：文字定数を含む方程式は「定数 $=k$」の形に分離し、グラフと水平線の交点で数える。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$a$ を実数とする。区間 $a\leqq x\leqq a+1$ における $f(x)=x^2-4x+5$ の最大値を $M(a)$、最小値を $m(a)$ とする。<br>(1) $m(a)$ を求めよ。　(2) $M(a)$ を求めよ。<br>(3) $M(a)-m(a)$ の最小値と、そのときの $a$ の値を求めよ。",
  "a": r"(1) $a<1$：$a^2-2a+2$、$1\leqq a\leqq2$：$1$、$a>2$：$a^2-4a+5$　(2) $a<\frac32$：$a^2-4a+5$、$a\geqq\frac32$：$a^2-2a+2$　(3) 最小値 $\frac14$（$a=\frac32$）",
  "s": r"$f(x)=(x-2)^2+1$、軸 $x=2$。<br>(1) $a+1<2$ すなわち $a<1$ なら $m=f(a+1)=(a-1)^2+1$。$1\leqq a\leqq2$ なら軸を含み $m=1$。$a>2$ なら $m=f(a)=(a-2)^2+1$。<br>(2) 区間の中央 $a+\frac12$ と軸 $2$ を比べる。$a<\frac32$ なら左端が軸から遠く $M=f(a)$、$a\geqq\frac32$ なら $M=f(a+1)$（$a=\frac32$ では両端で等しい）。<br>(3) $g(a)=M(a)-m(a)$ は<br>$a<1$：$\{(a-2)^2+1\}-\{(a-1)^2+1\}=3-2a\ (>1)$<br>$1\leqq a<\frac32$：$(a-2)^2$（$1$ から $\frac14$ へ減少）<br>$\frac32\leqq a\leqq2$：$(a-1)^2$（$\frac14$ から $1$ へ増加）<br>$a>2$：$\{(a-1)^2+1\}-\{(a-2)^2+1\}=2a-3\ (>1)$<br>よって $a=\frac32$ で最小値 $\frac14$。このとき区間 $\frac32\leqq x\leqq\frac52$ は軸に関して対称になっている。<br><b>ポイント</b>：区間が動くときも「軸との位置関係」で場合分け。最大と最小で境目が違うので、境目を全部並べてから $g(a)$ を組み立てる。"},
 {"lv": "C", "tag": "証明", "q": r"実数 $a,\ b$ に対して $f(x)=x^2+ax+b$ とする。<br>(1) $f(0)-2f(1)+f(2)$ の値を求めよ。<br>(2) $|f(0)|,\ |f(1)|,\ |f(2)|$ のうち少なくとも1つは $\frac12$ 以上であることを証明せよ。<br>(3) $|f(0)|,\ |f(1)|,\ |f(2)|$ がすべて $\frac12$ 以下となるような $a,\ b$ を求めよ。",
  "a": r"(1) $2$　(2) 略（背理法）　(3) $a=-2,\ b=\frac12$",
  "s": r"(1) $f(0)=b,\ f(1)=1+a+b,\ f(2)=4+2a+b$ より $f(0)-2f(1)+f(2)=b-2-2a-2b+4+2a+b=2$。<br>(2) 3つすべてが $\frac12$ より小さいと仮定する。三角不等式より $2=|f(0)-2f(1)+f(2)|\leqq|f(0)|+2|f(1)|+|f(2)|<\frac12+1+\frac12=2$ となり矛盾。よって少なくとも1つは $\frac12$ 以上。■<br>(3) すべて $\frac12$ 以下なら $2\leqq|f(0)|+2|f(1)|+|f(2)|\leqq2$ なので等号が成立する。各項が $\frac12$ 以下だから $|f(0)|=|f(1)|=|f(2)|=\frac12$。さらに三角不等式の等号が成り立つので $f(0),\ -2f(1),\ f(2)$ は同符号で、その和 $2$ が正だからすべて正。よって $f(0)=\frac12,\ f(1)=-\frac12,\ f(2)=\frac12$。$b=\frac12$、$1+a+b=-\frac12$ より $a=-2$。このとき $f(2)=4-4+\frac12=\frac12$ も満たす。$f(x)=(x-1)^2-\frac12$ である。<br><b>ポイント</b>：係数を消す1次結合 $f(0)-2f(1)+f(2)$ を見つけるのが鍵。「少なくとも1つ」は背理法で全部を否定する。"},
]}}


def verify():
    x, a, b, k = symbols("x a b k", real=True)
    # A1
    f = 2*x**2-8*x+5
    assert expand(2*(x-2)**2-3 - f) == 0
    assert max(f.subs(x, v) for v in [0, 2, 3]) == 5 and min(f.subs(x, v) for v in [0, 2, 3]) == -3
    assert expand(f.subs(x, x+1)+3 - (2*x**2-4*x+2)) == 0
    # A2
    g = -2*x**2+4*x+6
    assert all(g.subs(x, p) == q for p, q in [(-1, 0), (3, 0), (0, 6)])
    assert expand(-2*(x-1)**2+8 - g) == 0
    # A3
    assert solve_univariate_inequality(x**2-x-6 < 0, x, relational=False) == Interval.open(-2, 3)
    assert solve_univariate_inequality(2*x**2-3*x-2 >= 0, x, relational=False) == Union(Interval(-oo, Rational(-1, 2)), Interval(2, oo))
    assert solve_univariate_inequality(x**2-4*x+5 > 0, x, relational=False) == Reals
    assert solve_univariate_inequality(4*x**2-4*x+1 <= 0, x, relational=False) == FiniteSet(Rational(1, 2))
    # A4
    assert set(solve((k-1)**2-(k+5), k)) == {4, -1}
    assert solve(x**2+2*(4-1)*x+4+5, x) == [-3] and solve(x**2+2*(-1-1)*x-1+5, x) == [2]
    # B1: 区間 [0,2] の最小・最大を多数の a で直接比較
    def mm(av):
        fx = lambda t: t**2-2*av*t+3
        cand = [0, 2] + ([av] if 0 <= av <= 2 else [])
        vals = [fx(c) for c in cand]
        return min(vals), max(vals)
    for av in [Rational(n, 4) for n in range(-12, 21)]:
        m_, M_ = mm(av)
        m_f = 3 if av < 0 else (3-av**2 if av <= 2 else 7-4*av)
        M_f = 7-4*av if av < 1 else 3
        assert m_ == m_f and M_ == M_f, av
    # B2: 実際に解を求めて条件を判定
    for av in [Rational(n, 4) for n in range(-40, 60)]:
        r = Poly(x**2-2*av*x+av+6, x).nroots()
        real = [complex(t).real for t in r if abs(complex(t).imag) < 1e-12]
        c1 = len(real) == 2 and abs(real[0]-real[1]) > 1e-12 and min(real) > 0
        c2 = len(real) == 2 and min(real) < 1 < max(real)
        assert c1 == (av > 3), av
        assert c2 == (av > 7), av
    # B3: 整数解の個数を総当たり
    def cnt(av):
        return sum(1 for n in range(-20, 21) if (n-2)*(n-av) < 0)
    for av in [Rational(n, 8) for n in range(-40, 80)]:
        ok = (-2 <= av < -1) or (5 < av <= 6)
        assert (cnt(av) == 3) == ok, av
    assert expand((x-2)*(x-a) - (x**2-(a+2)*x+2*a)) == 0
    # B4
    h = 2*x**2+(3-x)**2
    assert expand(h - (3*(x-1)**2+6)) == 0 and h.subs(x, 3) == 18 and h.subs(x, 0) == 9
    # B5: 解の個数を数値的に数える
    def nsol(kv):
        s = set()
        for sgn in [1, -1]:
            for r in solve(x**2-2*x-3-sgn*kv, x):
                if r.is_real and simplify(Abs(r**2-2*r-3)-kv) == 0:
                    s.add(r)
        return len(s)
    for kv, n in [(-1, 0), (0, 2), (1, 4), (Rational(7, 2), 4), (4, 3), (5, 2), (10, 2)]:
        assert nsol(kv) == n, kv
    # C1
    F = lambda t: t**2-4*t+5
    def MmC(av):
        cand = [av, av+1] + ([2] if av <= 2 <= av+1 else [])
        vals = [F(c) for c in cand]
        return max(vals), min(vals)
    best = None
    for av in [Rational(n, 20) for n in range(-40, 100)]:
        M_, m_ = MmC(av)
        m_f = av**2-2*av+2 if av < 1 else (1 if av <= 2 else av**2-4*av+5)
        M_f = av**2-4*av+5 if av < Rational(3, 2) else av**2-2*av+2
        assert m_ == m_f and M_ == M_f, av
        g_ = M_-m_
        if best is None or g_ < best[0]:
            best = (g_, av)
    assert best == (Rational(1, 4), Rational(3, 2))
    assert expand((a-2)**2+1-((a-1)**2+1) - (3-2*a)) == 0
    # C2
    fx = lambda t: t**2+a*t+b
    assert expand(fx(0)-2*fx(1)+fx(2)) == 2
    assert solve([fx(0)-Rational(1, 2), fx(1)+Rational(1, 2)], [a, b]) == {a: -2, b: Rational(1, 2)}
    assert fx(2).subs({a: -2, b: Rational(1, 2)}) == Rational(1, 2)
