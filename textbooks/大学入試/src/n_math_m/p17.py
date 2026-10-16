"""問題集 第17章 統計的な推測。CH に問題、verify() で答えを sympy / Fraction で検算する。"""
from sympy import *
from fractions import Fraction as Fr

CH = {17: {
"goal": r"期待値・分散の計算、二項分布と正規分布の標準化を確実に。推定は「標本平均 $\pm1.96\times$ 標準偏差」、検定は「仮説 → 標準化 → 棄却域」の型を身につける。",
"items": [
 {"lv": "A", "q": r"袋の中に、1 と書かれた札が3枚、2 と書かれた札が2枚、3 と書かれた札が1枚入っている。1枚取り出したときの数を $X$ とする。$X$ の期待値 $E(X)$、分散 $V(X)$ を求めよ。また、$Y=3X+2$ の期待値と分散を求めよ。",
  "a": r"$E(X)=\frac53,\ V(X)=\frac59$；$E(Y)=7,\ V(Y)=5$",
  "s": r"$P(X=1)=\frac12,\ P(X=2)=\frac13,\ P(X=3)=\frac16$。<br>$E(X)=1\cdot\frac12+2\cdot\frac13+3\cdot\frac16=\frac53$。$E(X^2)=\frac12+\frac43+\frac96=\frac{10}{3}$ より $V(X)=E(X^2)-\{E(X)\}^2=\frac{10}{3}-\frac{25}{9}=\frac59$。<br>$E(Y)=3E(X)+2=7$、$V(Y)=3^2V(X)=5$。<br><b>ポイント</b>：$E(aX+b)=aE(X)+b$、$V(aX+b)=a^2V(X)$。分散では $b$ が消え、$a$ は2乗になる。"},
 {"lv": "A", "q": r"1個のさいころを 180 回投げるとき、1の目が出る回数を $X$ とする。$X$ の期待値、分散、標準偏差を求めよ。",
  "a": r"期待値 $30$、分散 $25$、標準偏差 $5$",
  "s": r"$X$ は二項分布 $B\left(180,\ \frac16\right)$ に従う。$E(X)=np=180\cdot\frac16=30$、$V(X)=np(1-p)=180\cdot\frac16\cdot\frac56=25$、$\sigma(X)=5$。<br><b>ポイント</b>：$B(n,p)$ の期待値 $np$、分散 $np(1-p)$ は公式として即答できるように。"},
 {"lv": "A", "q": r"確率変数 $X$ が正規分布 $N(50,\ 10^2)$ に従うとき、$P(40\leqq X\leqq70)$ を求めよ。ただし、標準正規分布に従う $Z$ について $P(0\leqq Z\leqq1)=0.3413$、$P(0\leqq Z\leqq2)=0.4772$ とする。",
  "a": r"$0.8185$",
  "s": r"$Z=\frac{X-50}{10}$ と標準化すると $Z$ は $N(0,1)$ に従う。$40\leqq X\leqq70 \iff -1\leqq Z\leqq2$。<br>対称性より $P(-1\leqq Z\leqq2)=P(0\leqq Z\leqq1)+P(0\leqq Z\leqq2)=0.3413+0.4772=0.8185$。<br><b>ポイント</b>：$Z=\frac{X-m}{\sigma}$ で標準化し、$0$ をまたぐ区間は $0$ で分けて表の値を足す。"},
 {"lv": "A", "q": r"母平均 $60$、母標準偏差 $12$ の母集団から、大きさ $36$ の無作為標本を抽出する。標本平均 $\overline{X}$ の期待値と標準偏差を求めよ。また、$P(\overline{X}\geqq63)$ の近似値を求めよ。ただし $P(0\leqq Z\leqq1.5)=0.4332$ とする。",
  "a": r"$E(\overline{X})=60,\ \sigma(\overline{X})=2$、$P(\overline{X}\geqq63)\fallingdotseq0.0668$",
  "s": r"$E(\overline{X})=60$、$\sigma(\overline{X})=\frac{12}{\sqrt{36}}=2$。標本の大きさが大きいので $\overline{X}$ は近似的に $N(60,\ 2^2)$ に従う。$Z=\frac{\overline{X}-60}{2}$ とすると、$\overline{X}\geqq63 \iff Z\geqq1.5$。$P(Z\geqq1.5)=0.5-0.4332=0.0668$。<br><b>ポイント</b>：標本平均の標準偏差は $\frac{\sigma}{\sqrt n}$。標本を大きくするほど $\overline{X}$ は母平均の近くに集まる。"},
 {"lv": "B", "tag": "正規近似", "q": r"1枚の硬貨を 400 回投げるとき、表が 220 回以上出る確率の近似値を求めよ。ただし $P(0\leqq Z\leqq2)=0.4772$ とする。",
  "a": r"$0.0228$",
  "s": r"表の回数 $X$ は $B\left(400,\ \frac12\right)$ に従い、$E(X)=200$、$\sigma(X)=\sqrt{400\cdot\frac12\cdot\frac12}=10$。$n$ が大きいので $X$ は近似的に $N(200,\ 10^2)$ に従う。$Z=\frac{X-200}{10}$ とすると $X\geqq220 \iff Z\geqq2$。<br>$P(Z\geqq2)=0.5-0.4772=0.0228$。<br><b>ポイント</b>：二項分布 $B(n,p)$ は $n$ が大きいとき $N(np,\ np(1-p))$ で近似できる。"},
 {"lv": "B", "tag": "母平均の推定", "q": r"ある工場で作る部品から 100 個を無作為に抽出して長さを測ったところ、平均は $52.4$ mm であった。母標準偏差を $8$ mm として、この部品の長さの母平均 $m$ に対する信頼度95%の信頼区間を求めよ（小数第2位を四捨五入）。ただし $P(0\leqq Z\leqq1.96)=0.475$ とする。",
  "a": r"$50.8\leqq m\leqq54.0$",
  "s": r"$\overline{X}$ は近似的に $N\left(m,\ \frac{8^2}{100}\right)$ に従い、標準偏差は $\frac{8}{10}=0.8$。$P(|Z|\leqq1.96)=0.95$ より、信頼区間は $\overline{X}-1.96\times0.8\leqq m\leqq\overline{X}+1.96\times0.8$。<br>$1.96\times0.8=1.568$ なので $52.4-1.568=50.832$、$52.4+1.568=53.968$。よって $50.8\leqq m\leqq54.0$。<br><b>ポイント</b>：信頼度95%の信頼区間は $\left[\overline{X}-1.96\frac{\sigma}{\sqrt n},\ \overline{X}+1.96\frac{\sigma}{\sqrt n}\right]$。信頼度95%とは、「この方法で標本をとって区間を作ることをくり返すと、約95%の区間が $m$ を含む」という意味である（$m$ は定数で、変動するのは区間のほう）。"},
 {"lv": "B", "tag": "母比率の推定", "q": r"ある市で有権者 400 人を無作為に選んで調査したところ、160 人がある政策に賛成した。この市の有権者全体の賛成の割合 $p$ に対する信頼度95%の信頼区間を求めよ（小数第4位を四捨五入）。ただし $P(0\leqq Z\leqq1.96)=0.475$、$\sqrt6=2.449$ とする。",
  "a": r"$0.352\leqq p\leqq0.448$",
  "s": r"標本比率 $R=\frac{160}{400}=0.4$。標本が大きいので、$R$ の標準偏差を $\sqrt{\frac{R(1-R)}{n}}=\sqrt{\frac{0.4\times0.6}{400}}=\frac{\sqrt{0.24}}{20}=\frac{\sqrt6}{100}=0.02449$ で近似する。<br>$1.96\times0.02449=0.0480\cdots$ なので、$0.4-0.0480=0.3520$、$0.4+0.0480=0.4480$。信頼区間は $0.352\leqq p\leqq0.448$。<br><b>ポイント</b>：母比率の推定では、未知の $p$ の代わりに標本比率 $R$ を使って標準偏差 $\sqrt{\frac{R(1-R)}{n}}$ を求める。"},
 {"lv": "B", "tag": "仮説検定（両側）", "q": r"あるさいころを 720 回投げたところ、1の目が 140 回出た。このさいころは1の目の出る確率が $\frac16$ ではないといえるか。有意水準5%で検定せよ。ただし $P(0\leqq Z\leqq1.96)=0.475$ とする。",
  "a": r"帰無仮説は棄却され、1の目の出る確率は $\frac16$ ではないといえる",
  "s": r"帰無仮説 $H_0$：1の目の出る確率は $\frac16$、対立仮説 $H_1$：$\frac16$ ではない（両側検定）。<br>$H_0$ のもとで、1の目の回数 $X$ は $B\left(720,\ \frac16\right)$ に従い、$E(X)=120$、$\sigma(X)=\sqrt{720\cdot\frac16\cdot\frac56}=10$。近似的に $N(120,\ 10^2)$ に従うので、$Z=\frac{X-120}{10}$ の有意水準5%の棄却域は $|Z|\geqq1.96$。<br>$X=140$ のとき $Z=2$ で棄却域に入る。よって $H_0$ を棄却し、1の目の出る確率は $\frac16$ ではないと判断する。<br><b>ポイント</b>：「確率が異なるか」は両側検定、「大きいか（小さいか）」は片側検定。棄却されないときは「$H_0$ が正しい」とはいわず、「異なるとはいえない」と答える。"},
 {"lv": "B", "tag": "仮説検定（片側）", "q": r"ある菓子の重さは、従来、平均 $200$ g、標準偏差 $6$ g であった。製法を変えたあと 36 個を無作為に抽出したところ、平均は $198.2$ g であった。標準偏差は変わらないものとして、重さの平均は減ったといえるか。有意水準5%で検定せよ。ただし $P(Z\geqq1.645)=0.05$ とする。",
  "a": r"帰無仮説は棄却され、平均は減ったといえる",
  "s": r"帰無仮説 $H_0$：$m=200$、対立仮説 $H_1$：$m\lt200$（片側検定）。<br>$H_0$ のもとで $\overline{X}$ は近似的に $N\left(200,\ \frac{6^2}{36}\right)=N(200,\ 1^2)$ に従う。$Z=\frac{\overline{X}-200}{1}$ の有意水準5%の棄却域は $Z\leqq-1.645$。<br>$\overline{X}=198.2$ のとき $Z=-1.8\leqq-1.645$ で棄却域に入る。よって $H_0$ を棄却し、平均は減ったと判断する。<br><b>ポイント</b>：片側検定では、棄却域を対立仮説の側だけにとる。同じデータでも、両側検定（棄却域 $|Z|\geqq1.96$）なら棄却されない点に注意。"},
 {"lv": "C", "tag": "連続型確率変数", "q": r"確率変数 $X$ のとる値の範囲が $0\leqq x\leqq2$ で、確率密度関数が $f(x)=ax(2-x)$（$a$ は定数）であるとする。<br>(1) $a$ の値を求めよ。(2) $X$ の期待値 $E(X)$ と分散 $V(X)$ を求めよ。(3) この分布に従う母集団から大きさ 125 の無作為標本を抽出するとき、標本平均 $\overline{X}$ が $0.92\leqq\overline{X}\leqq1.08$ を満たす確率の近似値を求めよ。ただし $P(0\leqq Z\leqq2)=0.4772$ とする。",
  "a": r"(1) $a=\frac34$　(2) $E(X)=1,\ V(X)=\frac15$　(3) $0.9544$",
  "s": r"(1) $\int_0^2ax(2-x)dx=a\left[x^2-\frac{x^3}{3}\right]_0^2=\frac43a=1$ より $a=\frac34$。<br>(2) $E(X)=\int_0^2x f(x)dx=\frac34\int_0^2(2x^2-x^3)dx=\frac34\left(\frac{16}{3}-4\right)=1$（グラフが $x=1$ に関して対称であることからも分かる）。$E(X^2)=\frac34\int_0^2(2x^3-x^4)dx=\frac34\left(8-\frac{32}{5}\right)=\frac65$。$V(X)=\frac65-1^2=\frac15$。<br>(3) $E(\overline{X})=1$、$\sigma(\overline{X})=\sqrt{\frac{V(X)}{125}}=\sqrt{\frac{1}{625}}=\frac{1}{25}=0.04$。$\overline{X}$ は近似的に $N(1,\ 0.04^2)$ に従う。$Z=\frac{\overline{X}-1}{0.04}$ とすると $0.92\leqq\overline{X}\leqq1.08 \iff -2\leqq Z\leqq2$。確率は $2\times0.4772=0.9544$。<br><b>ポイント</b>：確率密度関数は「全体の積分 $=1$」で定数を決める。$E(X)=\int xf(x)dx$、$V(X)=\int x^2f(x)dx-\{E(X)\}^2$。母集団分布が正規分布でなくても、$n$ が大きければ $\overline{X}$ は近似的に正規分布に従う（中心極限定理）。"},
 {"lv": "C", "tag": "標本の大きさ", "q": r"ある工場の製品の不良品の割合 $p$ を、信頼度95%で推定したい。信頼区間の幅を $0.04$ 以下にするには、標本の大きさ $n$ をいくら以上にすればよいか。(1) 過去の調査から $p$ は $0.1$ 程度と分かっている場合　(2) $p$ について何も分かっていない場合　のそれぞれについて答えよ。ただし $P(0\leqq Z\leqq1.96)=0.475$ とし、標本比率 $R$ が $p$ に近いものとして $R(1-R)$ を $p(1-p)$ で置き換えてよい。",
  "a": r"(1) $n\geqq865$　(2) $n\geqq2401$",
  "s": r"信頼区間の幅は $2\times1.96\sqrt{\frac{p(1-p)}{n}}$。これが $0.04$ 以下 ⇔ $\sqrt n\geqq\frac{2\times1.96}{0.04}\sqrt{p(1-p)}=98\sqrt{p(1-p)}$ ⇔ $n\geqq98^2p(1-p)=9604\,p(1-p)$。<br>(1) $p=0.1$ のとき $9604\times0.09=864.36$。$n$ は整数なので $n\geqq865$。<br>(2) $p(1-p)=\frac14-\left(p-\frac12\right)^2\leqq\frac14$（等号は $p=\frac12$）。$p$ がどんな値でも条件を満たすには $n\geqq9604\times\frac14=2401$ であればよく、$p=\frac12$ の場合を考えるとこれより小さい $n$ では足りない。よって $n\geqq2401$。<br><b>ポイント</b>：幅は $\frac{1}{\sqrt n}$ に比例するので、幅を半分にするには標本を4倍にする必要がある。$p$ が未知のときは $p(1-p)\leqq\frac14$ で安全側に見積もる。"},
]}}

def verify():
    P = {1: Fr(1, 2), 2: Fr(1, 3), 3: Fr(1, 6)}
    assert P == {1: Fr(3, 6), 2: Fr(2, 6), 3: Fr(1, 6)}
    E = sum(k*p for k, p in P.items()); E2 = sum(k*k*p for k, p in P.items())
    assert E == Fr(5, 3) and E2 == Fr(10, 3) and E2-E**2 == Fr(5, 9)
    EY = sum((3*k+2)*p for k, p in P.items()); VY = sum((3*k+2)**2*p for k, p in P.items())-EY**2
    assert EY == 7 and VY == 5
    # A2
    assert 180*Fr(1, 6) == 30 and 180*Fr(1, 6)*Fr(5, 6) == 25
    # 標準正規分布の表の値（4桁）
    z = symbols("z")
    Phi = lambda a: float((erf(a/sqrt(2))/2).evalf(20))   # P(0<=Z<=a)
    for a, v in [(1, 0.3413), (2, 0.4772), (1.5, 0.4332), (1.96, 0.475)]:
        assert abs(Phi(a)-v) < 5e-5, (a, Phi(a))
    assert abs((0.5-Phi(1.645)) - 0.05) < 1e-4
    # A3, A4, B1
    assert abs(0.3413+0.4772-0.8185) < 1e-12
    assert 12/sqrt(36) == 2 and (63-60)/2 == 1.5 and abs(0.5-0.4332-0.0668) < 1e-12
    assert sqrt(400*Rational(1, 4)) == 10 and (220-200)/10 == 2 and abs(0.5-0.4772-0.0228) < 1e-12
    # 二項分布の正確な値との比較（近似として妥当な程度）
    exact = sum(binomial(400, k) for k in range(220, 401))/Integer(2)**400
    assert abs(float(exact) - 0.0228) < 0.01
    # B2
    lo, hi = 52.4-1.96*0.8, 52.4+1.96*0.8
    assert abs(lo-50.832) < 1e-9 and abs(hi-53.968) < 1e-9 and round(lo, 1) == 50.8 and round(hi, 1) == 54.0
    # B3
    sd = sqrt(Rational(4, 10)*Rational(6, 10)/400)
    assert simplify(sd - sqrt(6)/100) == 0
    e = 1.96*0.02449
    assert abs(e-0.0480) < 1e-4 and round(0.4-e, 3) == 0.352 and round(0.4+e, 3) == 0.448
    # B4
    assert 720*Fr(1, 6) == 120 and 720*Fr(1, 6)*Fr(5, 6) == 100 and (140-120)/10 == 2 >= 1.96
    # B5
    zz = (198.2-200)/(6/6)
    assert abs(zz+1.8) < 1e-9 and zz <= -1.645 and abs(zz) < 1.96
    # C1
    x, a = symbols("x a", positive=True)
    av = solve(integrate(a*x*(2-x), (x, 0, 2))-1, a)[0]
    assert av == Rational(3, 4)
    f = av*x*(2-x)
    EX = integrate(x*f, (x, 0, 2)); EX2 = integrate(x**2*f, (x, 0, 2))
    assert EX == 1 and EX2 == Rational(6, 5) and EX2-EX**2 == Rational(1, 5)
    assert sqrt(Rational(1, 5)/125) == Rational(1, 25)
    assert abs((1.08-1)/0.04 - 2) < 1e-9 and abs(2*0.4772-0.9544) < 1e-12
    # C2
    assert (2*1.96/0.04)**2 - 9604 < 1e-6 and abs(9604*0.09-864.36) < 1e-9
    import math
    assert math.ceil(9604*0.09) == 865 and 9604/4 == 2401
    p = symbols("p")
    assert expand(p*(1-p) - (Rational(1, 4)-(p-Rational(1, 2))**2)) == 0
    # n=2401, p=1/2 で幅がちょうど 0.04、n=2400 では超える
    w = lambda n, pp: 2*1.96*math.sqrt(pp*(1-pp)/n)
    assert abs(w(2401, 0.5)-0.04) < 1e-12 and w(2400, 0.5) > 0.04
    assert w(865, 0.1) <= 0.04 < w(864, 0.1)
