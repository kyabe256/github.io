"""問題集 第16章 数列。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {16: {
"goal": r"等差・等比・$\Sigma$ 計算を確実に。漸化式は「型」を見抜いて一般項へ。数学的帰納法と評価で、数列の性質を論証できるようにする。",
"items": [
 {"lv": "A", "q": r"第5項が $17$、第12項が $45$ である等差数列 $\{a_n\}$ の一般項を求めよ。また、初項から第20項までの和を求めよ。",
  "a": r"$a_n=4n-3$、和 $780$",
  "s": r"初項 $a$、公差 $d$ とすると $a+4d=17,\ a+11d=45$。引いて $7d=28$、$d=4$、$a=1$。$a_n=1+4(n-1)=4n-3$。<br>$a_{20}=77$ なので和は $\frac{20(1+77)}{2}=780$。<br><b>ポイント</b>：等差数列の和は $\frac{項数\times(初項+末項)}{2}$。"},
 {"lv": "A", "q": r"第2項が $6$、第5項が $48$ である実数の等比数列 $\{a_n\}$ について、初項から第 $n$ 項までの和 $S_n$ を求めよ。また、$S_n\gt1000$ となる最小の自然数 $n$ を求めよ。",
  "a": r"$S_n=3(2^n-1)$、$n=9$",
  "s": r"初項 $a$、公比 $r$ とすると $ar=6,\ ar^4=48$。割って $r^3=8$、$r$ は実数なので $r=2$、$a=3$。$S_n=\frac{3(2^n-1)}{2-1}=3(2^n-1)$。<br>$3(2^n-1)\gt1000 \iff 2^n\gt\frac{1003}{3}=334.3\cdots$。$2^8=256,\ 2^9=512$ より $n=9$。<br><b>ポイント</b>：$r^3=8$ の実数解は $r=2$ のみ（虚数解を考えない根拠は「実数の等比数列」）。"},
 {"lv": "A", "q": r"次の和を求めよ。(1) $\displaystyle\sum_{k=1}^{n}(2k-1)^2$　(2) $\displaystyle\sum_{k=1}^{n}\frac{1}{(2k-1)(2k+1)}$",
  "a": r"(1) $\frac{n(2n-1)(2n+1)}{3}$　(2) $\frac{n}{2n+1}$",
  "s": r"(1) $\sum(4k^2-4k+1)=4\cdot\frac{n(n+1)(2n+1)}{6}-4\cdot\frac{n(n+1)}{2}+n=\frac{n}{3}\{2(n+1)(2n+1)-6(n+1)+3\}=\frac n3(4n^2-1)=\frac{n(2n-1)(2n+1)}{3}$。<br>(2) $\frac{1}{(2k-1)(2k+1)}=\frac12\left(\frac{1}{2k-1}-\frac{1}{2k+1}\right)$ より、隣どうしが消えて $\frac12\left(1-\frac{1}{2n+1}\right)=\frac{n}{2n+1}$。<br><b>ポイント</b>：分数の和は部分分数分解して「差の形」にし、途中を消す。"},
 {"lv": "A", "q": r"数列 $1,\ 2,\ 5,\ 10,\ 17,\ \cdots$ の一般項 $a_n$ を求めよ。",
  "a": r"$a_n=n^2-2n+2$",
  "s": r"階差数列は $1,\ 3,\ 5,\ 7,\ \cdots$ で、$b_n=2n-1$。$n\geqq2$ のとき $a_n=1+\sum_{k=1}^{n-1}(2k-1)=1+(n-1)^2=n^2-2n+2$。これは $n=1$ のとき $1$ となり成り立つ。<br><b>ポイント</b>：階差数列の公式は $n\geqq2$ で成り立つ式。$n=1$ のときを必ず確かめる。"},
 {"lv": "B", "tag": "典型", "q": r"次の条件で定まる数列 $\{a_n\}$ の一般項を求めよ。<br>(1) $a_1=1,\ a_{n+1}=3a_n-4$　(2) $a_1=1,\ a_{n+1}=2a_n+3^n$",
  "a": r"(1) $a_n=2-3^{n-1}$　(2) $a_n=3^n-2^n$",
  "s": r"(1) $\alpha=3\alpha-4$ の解 $\alpha=2$ を使って $a_{n+1}-2=3(a_n-2)$。$\{a_n-2\}$ は初項 $-1$、公比 $3$ の等比数列なので $a_n-2=-3^{n-1}$。<br>(2) 両辺を $2^{n+1}$ で割ると $\frac{a_{n+1}}{2^{n+1}}=\frac{a_n}{2^n}+\frac12\left(\frac32\right)^n$。$b_n=\frac{a_n}{2^n}$ とおくと $b_1=\frac12$、階差が $\frac12\left(\frac32\right)^n$ なので $n\geqq2$ で $b_n=\frac12+\sum_{k=1}^{n-1}\frac12\left(\frac32\right)^k=\frac12+\frac12\cdot\frac{\frac32\left\{\left(\frac32\right)^{n-1}-1\right\}}{\frac32-1}=\left(\frac32\right)^n-1$（$n=1$ でも成立）。よって $a_n=2^nb_n=3^n-2^n$。<br>（確認）$a_2=2\cdot1+3=5=9-4$。<br><b>ポイント</b>：$a_{n+1}=pa_n+q$ は特性方程式、$a_{n+1}=pa_n+r^n$ は $p^{n+1}$（または $r^{n+1}$）で割って階差型・1次型に直す。"},
 {"lv": "B", "tag": "典型", "q": r"数列 $\{a_n\}$ の初項から第 $n$ 項までの和 $S_n$ が $S_n=2a_n+n$ を満たすとき、一般項 $a_n$ を求めよ。",
  "a": r"$a_n=1-2^n$",
  "s": r"$n=1$ とすると $a_1=2a_1+1$ より $a_1=-1$。<br>$S_{n+1}=2a_{n+1}+n+1$ から $S_n=2a_n+n$ を引くと $a_{n+1}=2a_{n+1}-2a_n+1$、すなわち $a_{n+1}=2a_n-1$。<br>$a_{n+1}-1=2(a_n-1)$、$a_1-1=-2$ より $a_n-1=-2\cdot2^{n-1}=-2^n$。<br>（確認）$S_2=a_1+a_2=-1-3=-4$、$2a_2+2=-4$。<br><b>ポイント</b>：$S_n$ を含む関係式は、$n$ と $n+1$ の式を引いて $a_{n+1}=S_{n+1}-S_n$ を作る。初項は $S_1=a_1$ から別に求める。"},
 {"lv": "B", "tag": "頻出", "q": r"$S_n=\displaystyle\sum_{k=1}^{n}k\cdot2^{k-1}$ を求めよ。",
  "a": r"$S_n=(n-1)2^n+1$",
  "s": r"$S_n=1+2\cdot2+3\cdot2^2+\cdots+n\cdot2^{n-1}$、$2S_n=1\cdot2+2\cdot2^2+\cdots+(n-1)2^{n-1}+n\cdot2^n$。<br>辺々引いて $S_n-2S_n=1+2+2^2+\cdots+2^{n-1}-n\cdot2^n=(2^n-1)-n\cdot2^n$。<br>よって $S_n=n\cdot2^n-2^n+1=(n-1)2^n+1$。（確認）$n=3$：$1+4+12=17=2\cdot8+1$。<br><b>ポイント</b>：(等差)×(等比) の和は、公比倍した式を1つずらして引く。最後の項 $n\cdot2^n$ の符号に注意。"},
 {"lv": "B", "tag": "群数列", "q": r"分母が等しいものを1つの群として、次のように並べた数列を考える。<br>$\frac11\ \Big|\ \frac12,\ \frac22\ \Big|\ \frac13,\ \frac23,\ \frac33\ \Big|\ \frac14,\ \cdots$<br>(1) 第100項を求めよ。(2) 初項から第100項までの和を求めよ。",
  "a": r"(1) $\frac{9}{14}$　(2) $\frac{773}{14}$",
  "s": r"第 $k$ 群は $\frac1k,\ \frac2k,\ \cdots,\ \frac kk$ の $k$ 項。第 $m$ 群の終わりまでの項数は $\frac{m(m+1)}{2}$。<br>(1) $\frac{13\cdot14}{2}=91\lt100\leqq105=\frac{14\cdot15}{2}$ なので、第100項は第14群の $100-91=9$ 番目で $\frac{9}{14}$。<br>(2) 第 $k$ 群の和は $\frac{1+2+\cdots+k}{k}=\frac{k+1}{2}$。第1〜13群の和は $\sum_{k=1}^{13}\frac{k+1}{2}=\frac{91+13}{2}=52$。第14群の最初の9項の和は $\frac{1+2+\cdots+9}{14}=\frac{45}{14}$。合計 $52+\frac{45}{14}=\frac{773}{14}$。<br><b>ポイント</b>：群数列は「第 $m$ 群の末項が全体の第何項か」を先に式にし、不等式で群を特定する。"},
 {"lv": "B", "tag": "3項間漸化式", "q": r"$a_1=1,\ a_2=4,\ a_{n+2}=5a_{n+1}-6a_n$ で定まる数列 $\{a_n\}$ の一般項を求めよ。",
  "a": r"$a_n=2\cdot3^{n-1}-2^{n-1}$",
  "s": r"$x^2=5x-6$ の解は $x=2,\ 3$。よって<br>$a_{n+2}-2a_{n+1}=3(a_{n+1}-2a_n)$ より $a_{n+1}-2a_n=(a_2-2a_1)3^{n-1}=2\cdot3^{n-1}$ …①<br>$a_{n+2}-3a_{n+1}=2(a_{n+1}-3a_n)$ より $a_{n+1}-3a_n=(a_2-3a_1)2^{n-1}=2^{n-1}$ …②<br>①−② で $a_n=2\cdot3^{n-1}-2^{n-1}$。（確認）$a_3=5\cdot4-6\cdot1=14=18-4$。<br><b>ポイント</b>：特性方程式の2解 $\alpha,\beta$ で2通りの等比数列を作り、引き算で $a_n$ を取り出す。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$a_1=2,\ a_{n+1}=\dfrac{3a_n+1}{a_n+3}$ で定まる数列 $\{a_n\}$ について、(1) すべての $n$ で $a_n\gt0$ であることを示せ。(2) $b_n=\dfrac{a_n-1}{a_n+1}$ とおくとき、$b_{n+1}$ を $b_n$ で表せ。(3) 一般項 $a_n$ を求めよ。",
  "a": r"(2) $b_{n+1}=\frac12b_n$　(3) $a_n=\dfrac{3\cdot2^{n-1}+1}{3\cdot2^{n-1}-1}$",
  "s": r"(1) 数学的帰納法。$a_1=2\gt0$。$a_k\gt0$ と仮定すると $3a_k+1\gt0,\ a_k+3\gt0$ なので $a_{k+1}\gt0$。■（特に $a_n+1\neq0$、$a_n+3\neq0$ で、$b_n$ も漸化式も定義できる。）<br>(2) $a_{n+1}-1=\frac{3a_n+1-(a_n+3)}{a_n+3}=\frac{2(a_n-1)}{a_n+3}$、$a_{n+1}+1=\frac{4(a_n+1)}{a_n+3}$。割って $b_{n+1}=\frac{2(a_n-1)}{4(a_n+1)}=\frac12b_n$。<br>(3) $b_1=\frac{2-1}{2+1}=\frac13$ より $b_n=\frac13\left(\frac12\right)^{n-1}=\frac{1}{3\cdot2^{n-1}}$。$b_n=\frac{a_n-1}{a_n+1}$ を $a_n$ について解くと $a_n=\frac{1+b_n}{1-b_n}$（$b_n\neq1$ は $b_n\leqq\frac13$ から明らか）。分母分子に $3\cdot2^{n-1}$ をかけて $a_n=\frac{3\cdot2^{n-1}+1}{3\cdot2^{n-1}-1}$。<br>（確認）$a_2=\frac{7}{5}$、公式でも $\frac{6+1}{6-1}=\frac75$。<br><b>ポイント</b>：分数型 $a_{n+1}=\frac{pa_n+q}{ra_n+s}$ は、$x=\frac{px+q}{rx+s}$ の解（ここでは $\pm1$）$\alpha,\beta$ を使った $\frac{a_n-\alpha}{a_n-\beta}$ が等比数列になる。割り算をする前に分母が $0$ にならないことを確認しておく。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$a_1=1,\ a_{n+1}=a_n+\dfrac{1}{a_n}$ で定まる数列 $\{a_n\}$ について、(1) $n\geqq2$ のとき $a_n^2\gt2n-1$ であることを示せ。(2) $a_{50}$ の整数部分を求めよ。",
  "a": r"(2) $10$",
  "s": r"$a_1\gt0$ で、$a_n\gt0$ なら $a_{n+1}\gt0$ なので、すべての $n$ で $a_n\gt0$。<br>(1) 漸化式を2乗して $a_{k+1}^2=a_k^2+2+\frac{1}{a_k^2}$。$k=1,2,\cdots,n-1$ について加えると $a_n^2=a_1^2+2(n-1)+\sum_{k=1}^{n-1}\frac{1}{a_k^2}=2n-1+\sum_{k=1}^{n-1}\frac{1}{a_k^2}$。$n\geqq2$ のとき右辺の和は正なので $a_n^2\gt2n-1$。■<br>(2) $a_{50}^2=99+\sum_{k=1}^{49}\frac{1}{a_k^2}$。<br>下から：$k=1$ の項が $\frac{1}{a_1^2}=1$ で、他の項は正なので $a_{50}^2\gt100$。<br>上から：$k\geqq2$ では (1) より $a_k^2\gt2k-1\geqq3$、$\frac{1}{a_k^2}\lt\frac13$。よって $\sum_{k=1}^{49}\frac1{a_k^2}\lt1+\frac{48}{3}=17$、$a_{50}^2\lt116\lt121$。<br>以上より $10\lt a_{50}\lt11$ で、整数部分は $10$。<br><b>ポイント</b>：直接一般項が求まらない漸化式は、2乗して「和の形」にし、上下から評価する。評価は目的（整数部分）に必要な精度だけでよい。"},
]}}

def verify():
    n, k = symbols("n k", integer=True, positive=True)
    a, d = symbols("a d")
    s = solve([a+4*d-17, a+11*d-45], [a, d])
    assert s == {a: 1, d: 4}
    assert sum(4*i-3 for i in range(1, 21)) == 780
    # A2
    assert all(3*2**(i-1) == v for i, v in [(2, 6), (5, 48)])
    Sn = lambda m: sum(3*2**(i-1) for i in range(1, m+1))
    assert all(Sn(m) == 3*(2**m-1) for m in range(1, 12))
    assert min(m for m in range(1, 20) if Sn(m) > 1000) == 9
    # A3
    assert simplify(summation((2*k-1)**2, (k, 1, n)) - n*(2*n-1)*(2*n+1)/3) == 0
    assert simplify(summation(1/((2*k-1)*(2*k+1)), (k, 1, n)) - n/(2*n+1)) == 0
    # A4
    seq = [1, 2, 5, 10, 17]
    assert [m**2-2*m+2 for m in range(1, 6)] == seq
    # B1
    def gen(a1, f, N=12):
        v = [a1]
        for m in range(1, N):
            v.append(f(v[-1], m))
        return v
    assert gen(1, lambda x, m: 3*x-4) == [2-3**(m-1) for m in range(1, 13)]
    assert gen(1, lambda x, m: 2*x+3**m) == [3**m-2**m for m in range(1, 13)]
    b = Rational(1, 2) + summation(Rational(1, 2)*Rational(3, 2)**k, (k, 1, n-1))
    assert simplify(b - (Rational(3, 2)**n-1)) == 0
    # B2
    an = [1-2**m for m in range(1, 15)]
    assert all(sum(an[:m]) == 2*an[m-1]+m for m in range(1, 15))
    # B3
    assert simplify(summation(k*2**(k-1), (k, 1, n)) - ((n-1)*2**n+1)) == 0
    # B4
    seq = [Rational(i, g) for g in range(1, 20) for i in range(1, g+1)]
    assert seq[99] == Rational(9, 14) and sum(seq[:100]) == Rational(773, 14)
    # B5
    v = [1, 4]
    for _ in range(12):
        v.append(5*v[-1]-6*v[-2])
    assert v == [2*3**(m-1)-2**(m-1) for m in range(1, 15)]
    # C1
    x = symbols("x")
    assert solve(x-(3*x+1)/(x+3), x) == [-1, 1]
    bb = symbols("bb")
    an1 = lambda t: (3*t+1)/(t+3)
    assert simplify(((an1(x)-1)/(an1(x)+1)) - Rational(1, 2)*(x-1)/(x+1)) == 0
    v = [Integer(2)]
    for _ in range(12):
        v.append(an1(v[-1]))
    assert v == [Rational(3*2**(m-1)+1, 3*2**(m-1)-1) for m in range(1, 14)]
    # C2（有理数のままだと分母が爆発するので 60 桁の浮動小数で）
    import mpmath
    mpmath.mp.dps = 60
    v = [mpmath.mpf(1)]
    for _ in range(49):
        v.append(v[-1]+1/v[-1])
    a50 = v[49]
    assert int(mpmath.floor(a50)) == 10
    for m in range(2, 51):
        assert v[m-1]**2 > 2*m-1
    assert abs(a50**2 - (99 + sum(1/t**2 for t in v[:49]))) < mpmath.mpf(10)**-40
    assert 100 < a50**2 < 116
