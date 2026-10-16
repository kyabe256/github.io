"""問題集 第13章 指数関数・対数関数。CH に問題、verify() で答えを sympy・整数計算で検算する。"""
from sympy import *

CH = {13: {
"goal": "指数法則・対数の性質を正確に使い、底をそろえる・置き換える・真数条件を確認するの3点を習慣にする。常用対数で桁数や最高位の数を求め、大小比較を論証できるようにする。",
"items": [
 {"lv": "A", "q": r"次の計算をせよ。ただし $a>0,\ b>0$ とする。<br>(1) $8^{\frac23}\times4^{-\frac12}$　(2) $\sqrt[3]{24}+\sqrt[3]{81}-\sqrt[3]{3}$　(3) $\left(a^{\frac12}b^{-\frac13}\right)^6$",
  "a": r"(1) $2$　(2) $4\sqrt[3]3$　(3) $\frac{a^3}{b^2}$",
  "s": r"(1) $(2^3)^{\frac23}\times(2^2)^{-\frac12}=2^2\times2^{-1}=2$。(2) $\sqrt[3]{24}=2\sqrt[3]3,\ \sqrt[3]{81}=3\sqrt[3]3$ より $2\sqrt[3]3+3\sqrt[3]3-\sqrt[3]3=4\sqrt[3]3$。(3) $a^3b^{-2}=\frac{a^3}{b^2}$。<br><b>ポイント</b>：底を素数にそろえ、指数の計算に持ち込む。"},
 {"lv": "A", "q": r"次の値を求めよ。<br>(1) $\log_212-\log_23$　(2) $\log_3\sqrt{27}$　(3) $\log_29\cdot\log_38$　(4) $2\log_{10}5+\log_{10}4$",
  "a": r"(1) $2$　(2) $\frac32$　(3) $6$　(4) $2$",
  "s": r"(1) $\log_2\frac{12}3=\log_24=2$。(2) $\sqrt{27}=3^{\frac32}$ より $\frac32$。(3) 底の変換公式で $\frac{2\log3}{\log2}\cdot\frac{3\log2}{\log3}=6$。(4) $\log_{10}(25\cdot4)=\log_{10}100=2$。<br><b>ポイント</b>：異なる底の積は、底の変換公式で共通の底（どれでもよい）にそろえる。"},
 {"lv": "A", "q": r"次の方程式・不等式を解け。<br>(1) $4^x-3\cdot2^x-4=0$　(2) $\left(\dfrac13\right)^x>9$",
  "a": r"(1) $x=2$　(2) $x<-2$",
  "s": r"(1) $t=2^x\ (>0)$ とおくと $t^2-3t-4=0$、$(t-4)(t+1)=0$。$t>0$ より $t=4$、$x=2$。<br>(2) $3^{-x}>3^2$。底 $3>1$ なので $-x>2$、$x<-2$。<br><b>ポイント</b>：置き換えたら $t>0$ を忘れない。底が $1$ より小さいときは不等号の向きが逆になる（(2) は底を $3$ にそろえて回避した）。"},
 {"lv": "A", "q": r"次の方程式・不等式を解け。<br>(1) $\log_2(x-1)+\log_2(x+1)=3$　(2) $\log_{\frac12}(x-2)\geqq-1$",
  "a": r"(1) $x=3$　(2) $2<x\leqq4$",
  "s": r"(1) 真数条件 $x-1>0,\ x+1>0$ より $x>1$。$\log_2(x-1)(x+1)=\log_28$ より $x^2-1=8$、$x=\pm3$。$x>1$ より $x=3$。<br>(2) 真数条件 $x>2$。$-1=\log_{\frac12}2$ で、底 $\frac12<1$ なので $x-2\leqq2$、$x\leqq4$。よって $2<x\leqq4$。<br><b>ポイント</b>：対数の方程式・不等式は、最初に真数条件を書く。"},
 {"lv": "B", "tag": "大小比較", "q": r"(1) $\sqrt2,\ \sqrt[3]3,\ \sqrt[5]5$ を小さい順に並べよ。<br>(2) $\log_23,\ \log_34,\ \dfrac32$ を小さい順に並べよ。",
  "a": r"(1) $\sqrt[5]5<\sqrt2<\sqrt[3]3$　(2) $\log_34<\frac32<\log_23$",
  "s": r"(1) どれも正なので30乗して比べる。$(\sqrt2)^{30}=2^{15}=32768$、$(\sqrt[3]3)^{30}=3^{10}=59049$、$(\sqrt[5]5)^{30}=5^6=15625$。<br>(2) $2\log_23=\log_29>\log_28=3$ より $\log_23>\frac32$。$2\log_34=\log_316<\log_327=3$ より $\log_34<\frac32$。<br><b>ポイント</b>：累乗根は指数の最小公倍数乗して整数にする。対数は「2倍して整数と比べる」など、間にはさむ値を見つける。"},
 {"lv": "B", "tag": "常用対数", "q": r"$\log_{10}2=0.3010,\ \log_{10}3=0.4771$ とする。<br>(1) $6^{30}$ は何桁の整数か。また、最高位の数字を求めよ。<br>(2) $\left(\dfrac13\right)^{20}$ を小数で表すと、小数第何位に初めて $0$ でない数字が現れるか。また、その数字を求めよ。",
  "a": r"(1) 24桁、最高位は $2$　(2) 小数第10位、数字は $2$",
  "s": r"(1) $\log_{10}6^{30}=30(0.3010+0.4771)=23.343$。よって $10^{23}<6^{30}<10^{24}$ で24桁。$6^{30}=10^{23}\cdot10^{0.343}$ で、$\log_{10}2=0.3010<0.343<0.4771=\log_{10}3$ より $2<10^{0.343}<3$。最高位は $2$。<br>(2) $\log_{10}\left(\frac13\right)^{20}=-20\times0.4771=-9.542=-10+0.458$。$\left(\frac13\right)^{20}=10^{-10}\cdot10^{0.458}$ で、$0.3010<0.458<0.4771$ より $2<10^{0.458}<3$。小数第10位に初めて $2$ が現れる。<br><b>ポイント</b>：$\log_{10}N$ の整数部分が桁、小数部分が最高位の数字を決める。負のときは小数部分が $0$ 以上になるように $-10+0.458$ と書き直す。"},
 {"lv": "B", "q": r"次の関数の最大値と最小値、およびそのときの $x$ の値を求めよ。<br>(1) $y=4^x-2^{x+2}+5\ (-1\leqq x\leqq2)$<br>(2) $y=(\log_2x)^2-\log_2x^4+3\ (1\leqq x\leqq8)$",
  "a": r"(1) 最大値 $5$（$x=2$）、最小値 $1$（$x=1$）　(2) 最大値 $3$（$x=1$）、最小値 $-1$（$x=4$）",
  "s": r"(1) $t=2^x$ とおくと $\frac12\leqq t\leqq4$、$y=t^2-4t+5=(t-2)^2+1$。$t=2$（$x=1$）で最小値 $1$。端は $t=\frac12$ で $\frac{13}4$、$t=4$ で $5$ なので、最大値は $5$（$x=2$）。<br>(2) $s=\log_2x$ とおくと $0\leqq s\leqq3$、$\log_2x^4=4s$ より $y=s^2-4s+3=(s-2)^2-1$。$s=2$（$x=4$）で最小値 $-1$。端は $s=0$ で $3$、$s=3$ で $0$ なので、最大値は $3$（$x=1$）。<br><b>ポイント</b>：置き換えた文字の変域を、もとの変域から正確に求める。"},
 {"lv": "B", "q": r"$a$ を定数とする。関数 $y=4^x+4^{-x}-2a(2^x+2^{-x})$ について、<br>(1) $t=2^x+2^{-x}$ とおくとき、$t$ のとりうる値の範囲を求め、$y$ を $t$ で表せ。<br>(2) $y$ の最小値を $a$ で表せ。",
  "a": r"(1) $t\geqq2$、$y=t^2-2at-2$　(2) $a\leqq2$ のとき $2-4a$、$a>2$ のとき $-a^2-2$",
  "s": r"(1) $2^x>0,\ 2^{-x}>0$ なので、相加・相乗平均の関係より $t\geqq2\sqrt{2^x\cdot2^{-x}}=2$（等号は $x=0$）。$t$ は $2$ 以上のすべての値をとる。$t^2=4^x+2+4^{-x}$ より $4^x+4^{-x}=t^2-2$、$y=t^2-2-2at=t^2-2at-2$。<br>(2) $y=(t-a)^2-a^2-2\ (t\geqq2)$。軸 $t=a$ が $a\leqq2$ なら $t=2$ で最小値 $4-4a-2=2-4a$。$a>2$ なら $t=a$ で最小値 $-a^2-2$。<br><b>ポイント</b>：$2^x+2^{-x}$ の置き換えでは $t\geqq2$ が変域。相加・相乗平均で範囲を出す。"},
 {"lv": "B", "q": r"(1) 連立方程式 $\log_2x+\log_2y=3,\ x+y=6$ を解け。<br>(2) 正の数 $x,\ y$ が $xy=100$ を満たすとき、$(\log_{10}x)(\log_{10}y)$ の最大値と、そのときの $x,\ y$ を求めよ。",
  "a": r"(1) $(x,y)=(2,4),\ (4,2)$　(2) 最大値 $1$（$x=y=10$）",
  "s": r"(1) 真数条件 $x>0,\ y>0$。$\log_2xy=3$ より $xy=8$。$x+y=6,\ xy=8$ より $x,y$ は $u^2-6u+8=0$ の2解 $2,4$。<br>(2) $X=\log_{10}x,\ Y=\log_{10}y$ とおくと $X+Y=2$。$XY=X(2-X)=-(X-1)^2+1\leqq1$。等号は $X=1$、すなわち $x=10,\ y=10$。<br><b>ポイント</b>：積の条件は対数をとると和の条件になる。"},
 {"lv": "C", "tag": "論証", "q": r"(1) 実数 $x,\ y,\ z$ が $2^x=3^y=6^z$ を満たし、$xyz\neq0$ であるとき、$\dfrac1x+\dfrac1y=\dfrac1z$ を証明せよ。<br>(2) 正の数 $x,\ y,\ z$ が $2^x=3^y=5^z$ を満たすとき、$2x,\ 3y,\ 5z$ を小さい順に並べよ。",
  "a": r"(1) 略　(2) $3y<2x<5z$",
  "s": r"(1) $2^x=3^y=6^z=k$ とおく。$x\neq0$ より $k\neq1$、$k>0$。常用対数をとって $x=\frac{\log k}{\log2},\ y=\frac{\log k}{\log3},\ z=\frac{\log k}{\log6}$（$\log k\neq0$）。$\frac1x+\frac1y=\frac{\log2+\log3}{\log k}=\frac{\log6}{\log k}=\frac1z$。■<br>(2) $k=2^x=3^y=5^z$ とおくと、$x>0$ より $k>1$、$\log k>0$。<br>$2x=\frac{2\log k}{\log2}=\frac{\log k}{\log\sqrt2}$、$3y=\frac{\log k}{\log\sqrt[3]3}$、$5z=\frac{\log k}{\log\sqrt[5]5}$。<br>問題 13-5 (1) より $\sqrt[5]5<\sqrt2<\sqrt[3]3$ で、これらは $1$ より大きいから $0<\log\sqrt[5]5<\log\sqrt2<\log\sqrt[3]3$。分子 $\log k$ は共通で正なので、分母が大きいほど小さい。よって $3y<2x<5z$。<br><b>ポイント</b>：「$=k$ とおいて対数をとる」のが定石。比べたい量を「共通の正の数 $\div$ 何か」の形にそろえると、分母の大小比較に帰着する。"},
 {"lv": "C", "tag": "証明", "q": r"(1) $\log_{10}2$ は無理数であることを証明せよ。<br>以下、$0.3010<\log_{10}2<0.3011$ であることを用いてよい。<br>(2) $2^{100}$ の桁数と最高位の数字を求めよ。<br>(3) $2^n$ が20桁の整数となるような正の整数 $n$ をすべて求めよ。",
  "a": r"(1) 略　(2) 31桁、最高位は $1$　(3) $n=64,\ 65,\ 66$",
  "s": r"(1) $\log_{10}2>0$ なので、有理数と仮定すると $\log_{10}2=\frac pq$（$p,q$ は正の整数）と表せる。$10^{\frac pq}=2$ より $10^p=2^q$、すなわち $2^p5^p=2^q$。左辺は $5$ の倍数だが右辺は $5$ の倍数でないので矛盾。よって無理数。■<br>(2) $30.10<100\log_{10}2<30.11$ より $10^{30}<2^{100}<10^{31}$ で31桁。また $2^{100}=10^{30}\cdot10^{100\log_{10}2-30}$ で、指数は $0.11$ より小さく、$0.11<0.3010<\log_{10}2$ なので $1<10^{100\log_{10}2-30}<2$。最高位は $1$。<br>(3) 20桁 $\iff10^{19}\leqq2^n<10^{20}\iff19\leqq n\log_{10}2<20$。<br>$n\leqq63$ なら $n\log_{10}2<63\times0.3011=18.9693<19$ で不適。$n\geqq67$ なら $n\log_{10}2>67\times0.3010=20.167>20$ で不適。$n=64$ のとき $64\times0.3010=19.264<64\log_{10}2$、$n=66$ のとき $66\log_{10}2<66\times0.3011=19.8726$ なので、$n=64,65,66$ はすべて条件を満たす。<br><b>ポイント</b>：近似値の幅（上からと下からの評価）を使い分けて、境目の $n$ を確実に判定する。$\log_{10}2$ が無理数なので、$n\log_{10}2$ が整数になることはなく、等号の心配はない。"},
]}}


def verify():
    import math
    import random
    x, a, b, t, s = symbols("x a b t s", positive=True)
    # A1
    assert Integer(8)**Rational(2, 3)*Integer(4)**Rational(-1, 2) == 2
    assert simplify(cbrt(24)+cbrt(81)-cbrt(3) - 4*cbrt(3)) == 0
    assert simplify((a**Rational(1, 2)*b**Rational(-1, 3))**6 - a**3/b**2) == 0
    # A2
    assert simplify(log(12, 2)-log(3, 2)) == 2
    assert simplify(log(sqrt(27), 3)) == Rational(3, 2)
    assert simplify(log(9, 2)*log(8, 3)) == 6
    assert simplify(2*log(5, 10)+log(4, 10)) == 2
    # A3
    xr = symbols("xr", real=True)
    assert solve(4**xr-3*2**xr-4, xr) == [2]
    iv = solve_univariate_inequality(Rational(1, 3)**xr > 9, xr, relational=False)
    assert iv.left == -oo and simplify(iv.right+2) == 0 and iv.right_open
    # A4
    assert [v for v in solve((xr-1)*(xr+1)-8, xr) if v > 1] == [3]
    for xv in [Rational(n, 4) for n in range(9, 30)]:
        ok = xv > 2 and log(xv-2)/log(Rational(1, 2)) >= -1
        assert bool(ok) == (2 < xv <= 4), xv
    # B1
    assert 5**6 < 2**15 < 3**10
    assert 9 > 8 and 16 < 27 and N(log(4, 3)) < 1.5 < N(log(3, 2))
    # B2
    v = 6**30
    assert len(str(v)) == 24 and str(v)[0] == "2"
    assert abs(30*(0.3010+0.4771)-23.343) < 1e-9
    d = Rational(1, 3**20)
    # 小数第10位に初めて 0 でない数字（2）が現れる
    frac = (d*10**10)
    assert 2 <= frac < 3
    assert abs(-20*0.4771-(-10+0.458)) < 1e-9
    # B3
    for xv in [Rational(n, 4) for n in range(-4, 9)]:
        y1 = 4**xv-2**(xv+2)+5
        assert y1 >= 1 - 1e-12 and y1 <= 5
    tt = symbols("tt")
    assert expand(tt**2-4*tt+5 - ((tt-2)**2+1)) == 0
    assert (Integer(4)**1-2**3+5) == 1 and (Integer(4)**2-2**4+5) == 5 and Integer(4)**-1-2**0*2+5 == Rational(13, 4)
    assert ((tt-2)**2+1).subs(tt, Rational(1, 2)) == Rational(13, 4) and ((tt-2)**2+1).subs(tt, 4) == 5
    for xv in [1, 2, 4, 8]:
        y2 = log(xv, 2)**2-log(xv**4, 2)+3
        assert simplify(y2 - {1: 3, 2: 0, 4: -1, 8: 0}[xv]) == 0
    # B4
    u = symbols("u", positive=True)  # u=2^x とすると 4^x=u^2
    assert expand(u**2+u**-2 - ((u+1/u)**2-2)) == 0
    assert all(abs(4**xv+4**-xv-((2**xv+2**-xv)**2-2)) < 1e-9 for xv in [-1.5, -0.3, 0, 0.7, 2.2])
    for avv in [Rational(n, 2) for n in range(-6, 12)]:
        mn = min((tt0**2-2*float(avv)*tt0-2) for tt0 in [2+i/1000 for i in range(0, 20001)])
        ex = 2-4*avv if avv <= 2 else -avv**2-2
        assert abs(mn-float(ex)) < 1e-5, avv
    # B5
    sol = solve([a*b-8, a+b-6], [a, b], dict=True)
    assert {(q[a], q[b]) for q in sol} == {(2, 4), (4, 2)}
    Xv = symbols("Xv", real=True)
    assert maximum(Xv*(2-Xv), Xv) == 1
    # C1
    random.seed(7)
    for _ in range(100):
        k = random.uniform(0.1, 50)
        if abs(k-1) < 1e-3:
            continue
        xx, yy, zz = math.log(k)/math.log(2), math.log(k)/math.log(3), math.log(k)/math.log(6)
        assert abs(1/xx+1/yy-1/zz) < 1e-9
    for _ in range(100):
        k = random.uniform(1.0001, 1e6)
        xx, yy, zz = math.log(k, 2), math.log(k, 3), math.log(k, 5)
        assert 3*yy < 2*xx < 5*zz
    # C2
    assert 0.3010 < math.log10(2) < 0.3011
    assert len(str(2**100)) == 31 and str(2**100)[0] == "1"
    assert [n for n in range(1, 200) if len(str(2**n)) == 20] == [64, 65, 66]
    assert abs(63*0.3011-18.9693) < 1e-9 and abs(67*0.3010-20.167) < 1e-9
    assert abs(64*0.3010-19.264) < 1e-9 and abs(66*0.3011-19.8726) < 1e-9
