"""問題集 第22章 極限。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {22: {
"goal": r"不定形（$\frac\infty\infty$、$\infty-\infty$、$\frac00$）の処理と、無限等比級数・部分和の極限を確実に。はさみうちの原理で、一般項が求まらない数列の極限も扱えるようにする。",
"items": [
 {"lv": "A", "q": r"次の極限を求めよ。(1) $\displaystyle\lim_{n\to\infty}\frac{3n^2-n}{2n^2+5}$　(2) $\displaystyle\lim_{n\to\infty}\left(\sqrt{n^2+3n}-n\right)$　(3) $\displaystyle\lim_{n\to\infty}\frac{3^{n+1}-2^n}{3^n+2^n}$",
  "a": r"(1) $\frac32$　(2) $\frac32$　(3) $3$",
  "s": r"(1) 分母分子を $n^2$ で割って $\frac{3-\frac1n}{2+\frac{5}{n^2}}\to\frac32$。<br>(2) 有理化して $\frac{3n}{\sqrt{n^2+3n}+n}=\frac{3}{\sqrt{1+\frac3n}+1}\to\frac32$。<br>(3) 分母分子を $3^n$ で割って $\frac{3-\left(\frac23\right)^n}{1+\left(\frac23\right)^n}\to3$。<br><b>ポイント</b>：最も強く発散する項（$n^2$、$3^n$ など）で割る。$\infty-\infty$ は有理化。"},
 {"lv": "A", "q": r"(1) 無限級数 $\displaystyle\sum_{n=1}^{\infty}3\left(-\frac12\right)^{n-1}$ の和を求めよ。(2) 無限等比級数 $\displaystyle\sum_{n=1}^{\infty}(x-1)^n$ が収束するような $x$ の値の範囲と、そのときの和を求めよ。",
  "a": r"(1) $2$　(2) $0\lt x\lt2$、和 $\frac{x-1}{2-x}$",
  "s": r"(1) 初項 $3$、公比 $-\frac12$（$|r|\lt1$）なので $\frac{3}{1-\left(-\frac12\right)}=2$。<br>(2) 初項 $x-1$、公比 $x-1$。収束 ⇔ 初項 $=0$ または $|x-1|\lt1$。初項 $=0$（$x=1$）は $|x-1|\lt1$ に含まれるので、$0\lt x\lt2$。和は $\frac{x-1}{1-(x-1)}=\frac{x-1}{2-x}$。<br><b>ポイント</b>：無限等比級数 $\sum ar^{n-1}$ は「$a=0$ または $|r|\lt1$」で収束し、和は $\frac{a}{1-r}$。初項 $0$ の場合を忘れない。"},
 {"lv": "A", "q": r"次の極限を求めよ。(1) $\displaystyle\lim_{x\to2}\frac{x^2-4}{x^2-3x+2}$　(2) $\displaystyle\lim_{x\to0}\frac{\sin3x}{x}$　(3) $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^2}$　(4) $\displaystyle\lim_{x\to\infty}\left(\sqrt{x^2+x}-x\right)$",
  "a": r"(1) $4$　(2) $3$　(3) $\frac12$　(4) $\frac12$",
  "s": r"(1) $\frac{(x-2)(x+2)}{(x-2)(x-1)}=\frac{x+2}{x-1}\to4$。<br>(2) $\frac{\sin3x}{3x}\cdot3\to1\cdot3=3$。<br>(3) 分母分子に $1+\cos x$ をかけて $\frac{\sin^2x}{x^2(1+\cos x)}=\left(\frac{\sin x}{x}\right)^2\cdot\frac{1}{1+\cos x}\to\frac12$。<br>(4) 有理化して $\frac{x}{\sqrt{x^2+x}+x}=\frac{1}{\sqrt{1+\frac1x}+1}\to\frac12$。<br><b>ポイント</b>：三角関数の極限は $\displaystyle\lim_{\theta\to0}\frac{\sin\theta}{\theta}=1$ の形を作る。$1-\cos x$ は $1+\cos x$ をかけて $\sin^2x$ にする。"},
 {"lv": "A", "q": r"次の極限を求めよ。(1) $\displaystyle\lim_{x\to0}(1+2x)^{\frac1x}$　(2) $\displaystyle\lim_{n\to\infty}\left(1+\frac1n\right)^{3n}$　(3) $\displaystyle\lim_{x\to0}\frac{e^{2x}-1}{x}$",
  "a": r"(1) $e^2$　(2) $e^3$　(3) $2$",
  "s": r"(1) $(1+2x)^{\frac1x}=\left\{(1+2x)^{\frac{1}{2x}}\right\}^2\to e^2$。<br>(2) $\left\{\left(1+\frac1n\right)^n\right\}^3\to e^3$。<br>(3) $\frac{e^{2x}-1}{2x}\cdot2\to1\cdot2=2$。<br><b>ポイント</b>：$\displaystyle\lim_{t\to0}(1+t)^{\frac1t}=e$、$\displaystyle\lim_{t\to0}\frac{e^t-1}{t}=1$。指数の部分を「$t$ の逆数」にそろえる。"},
 {"lv": "B", "tag": "漸化式と極限", "q": r"$a_1=1,\ a_{n+1}=\dfrac13a_n+2$ で定まる数列 $\{a_n\}$ について、$\displaystyle\lim_{n\to\infty}a_n$ を求めよ。また、無限級数 $\displaystyle\sum_{n=1}^{\infty}(a_n-3)$ の和を求めよ。",
  "a": r"$\lim a_n=3$、$\sum(a_n-3)=-3$",
  "s": r"$\alpha=\frac13\alpha+2$ より $\alpha=3$。$a_{n+1}-3=\frac13(a_n-3)$、$a_1-3=-2$ より $a_n-3=-2\left(\frac13\right)^{n-1}$。<br>$\left(\frac13\right)^{n-1}\to0$ なので $\lim a_n=3$。<br>$\sum_{n=1}^{\infty}(a_n-3)$ は初項 $-2$、公比 $\frac13$ の無限等比級数で、和は $\frac{-2}{1-\frac13}=-3$。<br><b>ポイント</b>：$a_{n+1}=pa_n+q$（$|p|\lt1$）の極限は、特性方程式の解 $\alpha$。"},
 {"lv": "B", "tag": "極限で定まる関数", "q": r"関数 $f(x)=\displaystyle\lim_{n\to\infty}\frac{x^{2n+1}-x+1}{x^{2n}+1}$ を求め、$f(x)$ が連続でない $x$ の値を答えよ。",
  "a": r"$|x|\lt1$ で $f(x)=1-x$、$|x|\gt1$ で $f(x)=x$、$f(\pm1)=\frac12$；不連続なのは $x=\pm1$",
  "s": r"<b>$|x|\lt1$</b>：$x^{2n}\to0,\ x^{2n+1}\to0$ なので $f(x)=1-x$。<br><b>$|x|\gt1$</b>：分母分子を $x^{2n}$ で割ると $\frac{x-\frac{x-1}{x^{2n}}}{1+\frac{1}{x^{2n}}}\to x$。<br><b>$x=1$</b>：$\frac{1-1+1}{2}=\frac12$。<b>$x=-1$</b>：$\frac{-1+1+1}{2}=\frac12$。<br>$x=1$ で、左からの極限は $1-1=0$、右からの極限は $1$ で一致しないので不連続。$x=-1$ で、左からの極限は $-1$、右からの極限は $1-(-1)=2$ で不連続。他の点では多項式なので連続。<br><b>ポイント</b>：$x^n$ を含む極限は $|x|\lt1,\ x=1,\ x=-1,\ |x|\gt1$ で場合分け。境目で左右の極限と関数値を比べる。"},
 {"lv": "B", "tag": "部分和", "q": r"次の無限級数の和を求めよ。(1) $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$　(2) $\displaystyle\sum_{n=1}^{\infty}\frac{2n+1}{n^2(n+1)^2}$",
  "a": r"(1) $\frac34$　(2) $1$",
  "s": r"(1) $\frac{1}{n(n+2)}=\frac12\left(\frac1n-\frac{1}{n+2}\right)$。部分和は $S_n=\frac12\left(1+\frac12-\frac{1}{n+1}-\frac{1}{n+2}\right)\to\frac12\cdot\frac32=\frac34$。<br>(2) $\frac{1}{n^2}-\frac{1}{(n+1)^2}=\frac{(n+1)^2-n^2}{n^2(n+1)^2}=\frac{2n+1}{n^2(n+1)^2}$。部分和は $1-\frac{1}{(n+1)^2}\to1$。<br><b>ポイント</b>：無限級数は部分和 $S_n$ を求めてから $n\to\infty$。1つおきに消える形（$\frac1n-\frac1{n+2}$）は、残る項が最初と最後に2つずつある。"},
 {"lv": "B", "tag": "図形と級数", "q": r"座標平面上で、点 P が原点 O から出発し、東（$x$ 軸の正の向き）へ $1$ 進み、次に左へ $90^\circ$ 向きを変えて $\frac12$ 進み、また左へ $90^\circ$ 向きを変えて $\frac14$ 進む、という動きを限りなく続ける（進む距離は毎回 $\frac12$ 倍）。P が限りなく近づく点の座標を求めよ。",
  "a": r"$\left(\frac45,\ \frac25\right)$",
  "s": r"$x$ 座標：$1-\frac14+\frac1{16}-\cdots$ は初項 $1$、公比 $-\frac14$ の無限等比級数で $\frac{1}{1+\frac14}=\frac45$。<br>$y$ 座標：$\frac12-\frac18+\frac1{32}-\cdots=\frac{\frac12}{1+\frac14}=\frac25$。<br>（別解）複素数平面で、$n$ 回目の移動は $\left(\frac i2\right)^{n-1}$。和は $\frac{1}{1-\frac i2}=\frac{2}{2-i}=\frac{2(2+i)}{5}=\frac45+\frac25i$。<br><b>ポイント</b>：$x$ 成分と $y$ 成分に分けると、それぞれが無限等比級数になる。回転が入る動きは複素数の等比級数で一気に計算できる。"},
 {"lv": "B", "tag": "定数の決定", "q": r"$\displaystyle\lim_{x\to1}\frac{a\sqrt{x+3}-b}{x-1}=\frac12$ が成り立つように、定数 $a,\ b$ の値を定めよ。",
  "a": r"$a=2,\ b=4$",
  "s": r"$x\to1$ で分母 $\to0$ なので、極限が有限値であるためには分子 $\to0$ が必要：$2a-b=0$、$b=2a$。<br>このとき $\frac{a(\sqrt{x+3}-2)}{x-1}=\frac{a(x+3-4)}{(x-1)(\sqrt{x+3}+2)}=\frac{a}{\sqrt{x+3}+2}\to\frac a4$。$\frac a4=\frac12$ より $a=2$、$b=4$。<br><b>ポイント</b>：「分母 $\to0$ で極限が有限 ⇒ 分子 $\to0$」は必要条件。求めた値で実際に極限が $\frac12$ になることを計算で確かめる（ここでは同時に確認している）。"},
 {"lv": "C", "tag": "はさみうち", "q": r"$a_1=1,\ a_{n+1}=\sqrt{a_n+2}$ で定まる数列 $\{a_n\}$ について、<br>(1) すべての $n$ で $1\leqq a_n\lt2$ であることを示せ。<br>(2) $2-a_{n+1}\leqq\dfrac13(2-a_n)$ を示せ。<br>(3) $\displaystyle\lim_{n\to\infty}a_n$ を求めよ。",
  "a": r"(3) $2$",
  "s": r"(1) 数学的帰納法。$a_1=1$ で成立。$1\leqq a_k\lt2$ なら $3\leqq a_k+2\lt4$ で $\sqrt3\leqq a_{k+1}\lt2$、特に $1\leqq a_{k+1}\lt2$。■<br>(2) $2-a_{n+1}=2-\sqrt{a_n+2}=\frac{4-(a_n+2)}{2+\sqrt{a_n+2}}=\frac{2-a_n}{2+a_{n+1}}$。(1) より $2+a_{n+1}\geqq3$、$2-a_n\gt0$ なので $2-a_{n+1}\leqq\frac13(2-a_n)$。■<br>(3) (2) をくり返し用いて $0\lt2-a_n\leqq\left(\frac13\right)^{n-1}(2-a_1)=\left(\frac13\right)^{n-1}$。$\left(\frac13\right)^{n-1}\to0$ なので、はさみうちの原理より $2-a_n\to0$、$\lim a_n=2$。<br><b>ポイント</b>：極限の予想値 $\alpha$（$\alpha=\sqrt{\alpha+2}$ の解 $\alpha=2$）との差 $|a_n-\alpha|$ が等比的に小さくなることを示す。有理化で差どうしの関係式を作るのが定石。"},
 {"lv": "C", "tag": "論証", "q": r"$S_n=\displaystyle\sum_{k=1}^{n}\frac1k$ とする。<br>(1) 自然数 $m$ について $S_{2^m}\geqq1+\dfrac m2$ を示せ。<br>(2) 無限級数 $\displaystyle\sum_{k=1}^{\infty}\frac1k$ は発散することを示せ。<br>(3) $S_n\gt10$ となる自然数 $n$ を1つ具体的に挙げよ（最小である必要はない）。",
  "a": r"(3) 例：$n=2^{19}=524288$",
  "s": r"(1) $S_{2^m}=1+\sum_{j=1}^{m}T_j$、$T_j=\frac{1}{2^{j-1}+1}+\frac{1}{2^{j-1}+2}+\cdots+\frac{1}{2^j}$ と分ける。$T_j$ は $2^{j-1}$ 個の項からなり、どの項も最後の項 $\frac{1}{2^j}$ 以上なので $T_j\geqq2^{j-1}\cdot\frac{1}{2^j}=\frac12$。よって $S_{2^m}\geqq1+\frac m2$。■<br>(2) $S_n$ は $n$ について増加し、(1) より $S_{2^m}\to\infty\ (m\to\infty)$。任意の $M$ に対して $1+\frac m2\gt M$ となる $m$ をとれば、$n\geqq2^m$ で $S_n\geqq S_{2^m}\gt M$。よって $\lim S_n=\infty$ で、級数は発散する。■<br>(3) $1+\frac m2\gt10$ ⇔ $m\gt18$。$m=19$ とすると $S_{2^{19}}\geqq1+\frac{19}{2}=10.5\gt10$。よって $n=2^{19}=524288$ は条件を満たす。<br><b>ポイント</b>：$\lim\frac1k=0$ でも $\sum\frac1k$ は発散する。「一般項 $\to0$」は級数が収束するための必要条件にすぎない。項を $2$ のべきごとにまとめて下から評価するのが定石。"},
]}}

def verify():
    n, x = symbols("n x", positive=True)
    assert limit((3*n**2-n)/(2*n**2+5), n, oo) == Rational(3, 2)
    assert limit(sqrt(n**2+3*n)-n, n, oo) == Rational(3, 2)
    assert limit((3**(n+1)-2**n)/(3**n+2**n), n, oo) == 3
    # A2
    assert summation(3*Rational(-1, 2)**(n-1), (n, 1, oo)) == 2
    xx = symbols("xx", real=True)
    assert simplify((xx-1)/(1-(xx-1)) - (xx-1)/(2-xx)) == 0
    assert solve_univariate_inequality(Abs(xx-1) < 1, xx, relational=False) == Interval.open(0, 2)
    # A3
    y = symbols("y")
    assert limit((y**2-4)/(y**2-3*y+2), y, 2) == 4
    assert limit(sin(3*y)/y, y, 0) == 3 and limit((1-cos(y))/y**2, y, 0) == Rational(1, 2)
    assert limit(sqrt(x**2+x)-x, x, oo) == Rational(1, 2)
    # A4
    assert limit((1+2*y)**(1/y), y, 0) == E**2 and limit((1+1/n)**(3*n), n, oo) == E**3
    assert limit((exp(2*y)-1)/y, y, 0) == 2
    # B1
    a = [Integer(1)]
    for _ in range(15):
        a.append(a[-1]/3+2)
    assert all(a[k-1] == 3-2*Rational(1, 3)**(k-1) for k in range(1, 16))
    assert summation(-2*Rational(1, 3)**(n-1), (n, 1, oo)) == -3
    # B2
    g = lambda v, N: (v**(2*N+1)-v+1)/(v**(2*N)+1)   # 整数 N を大きくして極限値に近づくことを確認
    for v0, lim0 in [(Rational(1, 2), Rational(1, 2)), (Rational(-1, 3), Rational(4, 3)), (3, 3), (-2, -2), (Rational(9, 10), Rational(1, 10)), (Rational(-11, 10), Rational(-11, 10))]:
        assert abs(g(v0, 400) - lim0) < Rational(1, 10**10)
    assert (1**(2*5+1)-1+1)/Rational(1**(10)+1) == Rational(1, 2) and ((-1)**11+1+1)/Rational((-1)**10+1) == Rational(1, 2)
    # B3
    assert summation(1/(n*(n+2)), (n, 1, oo)) == Rational(3, 4)
    assert simplify(1/n**2-1/(n+1)**2 - (2*n+1)/(n**2*(n+1)**2)) == 0
    assert summation((2*n+1)/(n**2*(n+1)**2), (n, 1, oo)) == 1
    # B4
    assert summation(Rational(-1, 4)**(n-1), (n, 1, oo)) == Rational(4, 5)
    assert summation(Rational(1, 2)*Rational(-1, 4)**(n-1), (n, 1, oo)) == Rational(2, 5)
    assert simplify(1/(1-I/2) - (Rational(4, 5)+Rational(2, 5)*I)) == 0
    # B5
    aa, bb = 2, 4
    assert limit((aa*sqrt(y+3)-bb)/(y-1), y, 1) == Rational(1, 2)
    # C1
    import mpmath
    mpmath.mp.dps = 30
    v = [mpmath.mpf(1)]
    for _ in range(30):
        v.append(mpmath.sqrt(v[-1]+2))
    for k in range(30):
        assert 1 <= v[k] < 2
        assert 2-v[k+1] <= (2-v[k])/3 + mpmath.mpf(10)**-25
        assert 2-v[k] <= mpmath.mpf(1)/3**k + mpmath.mpf(10)**-25
    t = symbols("t", positive=True)
    assert simplify((2-sqrt(t+2)) - (2-t)/(2+sqrt(t+2))) == 0
    # C2
    from fractions import Fraction as Fr
    for m in range(1, 13):
        S = sum(Fr(1, k) for k in range(1, 2**m+1))
        assert S >= 1+Fr(m, 2)
    # S_{2^19} > 10（調和数の近似 ln n + γ で確認）
    H = mpmath.harmonic(2**19)
    assert H > 10.5 and 1+Fr(19, 2) == Fr(21, 2) and 2**19 == 524288
