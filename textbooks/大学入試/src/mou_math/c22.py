"""第22章 極限（数学III）"""
import math, random
from fractions import Fraction as F
from sympy import (symbols, sqrt, Rational, limit, oo, simplify, expand, summation, sin, cos, tan,
                   exp, log, pi, E, Abs, cbrt, binomial, factor, nsimplify, real_roots, Poly, S, N as SN)

SEC = []

# ---------------------------------------------------------------- 節1
SEC.append({"title": r"数列の極限（不定形の極限）",
"base": r"""・数列 $\{a_n\}$ が $\alpha$ に収束するとき $\displaystyle\lim_{n\to\infty}a_n=\alpha$。収束しない数列は発散する（$+\infty$ に発散・$-\infty$ に発散・振動）。<br>
・$\lim a_n=\alpha,\ \lim b_n=\beta$ のとき　$\lim(a_n\pm b_n)=\alpha\pm\beta$，$\lim a_nb_n=\alpha\beta$，$\displaystyle\lim\frac{a_n}{b_n}=\frac{\alpha}{\beta}$（$\beta\neq0$）<br>
・不定形 $\dfrac{\infty}{\infty}$：分母の最高次の項で分子・分母を割る。不定形 $\infty-\infty$（根号を含む）：有理化する。<br>
・$k>0$ のとき $\displaystyle\lim_{n\to\infty}\frac{1}{n^k}=0$""",
"items": [
 {"lv": 1, "title": r"不定形の極限（最高次の項で割る・有理化）",
  "q": r"次の極限を調べよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{3n^2-2n+5}{2n^2+n-1}$　(2) $\displaystyle\lim_{n\to\infty}\frac{n^3+1}{4n^2-n}$　(3) $\displaystyle\lim_{n\to\infty}\left(\sqrt{n^2+4n}-n\right)$",
  "hint": r"(1)(2) は $\dfrac{\infty}{\infty}$ の形なので、<b>分母の最高次の項 $n^2$ で分子・分母を割る</b>。(3) は $\infty-\infty$ の形。$\dfrac{\sqrt{n^2+4n}+n}{\sqrt{n^2+4n}+n}$ を掛けて分子を有理化する。",
  "sol": r"(1) 分子・分母を $n^2$ で割ると　$\dfrac{3-\frac2n+\frac5{n^2}}{2+\frac1n-\frac1{n^2}}\to\dfrac{3}{2}$　よって　$\boldsymbol{\dfrac32}$<br>"
         r"(2) 分子・分母を $n^2$ で割ると　$\dfrac{n+\frac1{n^2}}{4-\frac1n}$　分子 $\to\infty$，分母 $\to4$ であるから　$\boldsymbol{\infty}$（正の無限大に発散）<br>"
         r"(3) $\sqrt{n^2+4n}-n=\dfrac{(n^2+4n)-n^2}{\sqrt{n^2+4n}+n}=\dfrac{4n}{\sqrt{n^2+4n}+n}=\dfrac{4}{\sqrt{1+\frac4n}+1}\to\dfrac{4}{1+1}=\boldsymbol{2}$",
  "note": r"(3) を「$\infty-\infty=0$」とするのは誤り。$\sqrt{n^2+4n}=\sqrt{(n+2)^2-4}$ は $n+2$ にほぼ等しいので、差は $2$ に近づくと見当がつく。",
  "ex": r"次の極限を調べよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{(2n-1)(n+3)}{3n^2+2}$　(2) $\displaystyle\lim_{n\to\infty}\frac{1-n^2}{2n+1}$　(3) $\displaystyle\lim_{n\to\infty}\left(\sqrt{n^2+n}-\sqrt{n^2-n}\right)$",
  "exa": r"(1) $\dfrac23$　(2) $-\infty$　(3) $1$"},
 {"lv": 2, "title": r"3乗根を含む不定形（$a^3-b^3$ の公式で有理化）",
  "q": r"$\displaystyle\lim_{n\to\infty}\left(\sqrt[3]{n^3+2n^2}-n\right)$ を求めよ。",
  "hint": r"平方根のときの有理化にあたるのは　$a-b=\dfrac{a^3-b^3}{a^2+ab+b^2}$。$a=\sqrt[3]{n^3+2n^2}$，$b=n$ とすると、分子の $a^3-b^3$ から 3 乗根が消える。",
  "sol": r"$a=\sqrt[3]{n^3+2n^2}$ とおくと $a^3-n^3=2n^2$ であるから<br>"
         r"$a-n=\dfrac{a^3-n^3}{a^2+an+n^2}=\dfrac{2n^2}{a^2+an+n^2}$<br>"
         r"分子・分母を $n^2$ で割ると、$\dfrac{a}{n}=\sqrt[3]{1+\frac2n}\to1$ より<br>"
         r"$a-n=\dfrac{2}{\left(\frac an\right)^2+\frac an+1}\to\dfrac{2}{1+1+1}=\boldsymbol{\dfrac23}$",
  "note": r"一般に $\sqrt[3]{n^3+pn^2}-n\to\dfrac p3$。$\sqrt[3]{n^3+pn^2}=n\sqrt[3]{1+\frac pn}$ は $n\left(1+\frac{p}{3n}\right)=n+\frac p3$ にほぼ等しい、と見当をつけられる（近似式は第24章）。",
  "ex": r"$\displaystyle\lim_{n\to\infty}\left(\sqrt[3]{n^3-3n^2+1}-n\right)$ を求めよ。",
  "exa": r"$-1$"},
 {"lv": 2, "title": r"和で表された数列の極限（和を求めてから極限）",
  "q": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{1^2+2^2+\cdots+n^2}{n(1+2+\cdots+n)}$　(2) $\displaystyle\lim_{n\to\infty}\left\{\sqrt{1+2+\cdots+n}-\sqrt{1+2+\cdots+(n-1)}\right\}$",
  "hint": r"項の個数が $n$ とともに増える和は、そのままでは極限の計算ができない。<b>まず和の公式で $n$ の式にしてから</b>極限をとる。(2) は和を求めたあと有理化する。",
  "sol": r"(1) $\displaystyle\sum_{k=1}^{n}k^2=\frac{n(n+1)(2n+1)}{6}$，$\displaystyle\sum_{k=1}^{n}k=\frac{n(n+1)}{2}$ であるから<br>"
         r"与式 $=\dfrac{n(n+1)(2n+1)}{6}\cdot\dfrac{2}{n\cdot n(n+1)}=\dfrac{2n+1}{3n}=\dfrac{2+\frac1n}{3}\to\boldsymbol{\dfrac23}$<br>"
         r"(2) $1+2+\cdots+n=\dfrac{n(n+1)}{2}$，$1+2+\cdots+(n-1)=\dfrac{n(n-1)}{2}$ で、その差は $n$ である。よって<br>"
         r"与式 $=\dfrac{n}{\sqrt{\frac{n(n+1)}{2}}+\sqrt{\frac{n(n-1)}{2}}}$　分子・分母を $n$ で割ると<br>"
         r"$=\dfrac{1}{\sqrt{\frac12\left(1+\frac1n\right)}+\sqrt{\frac12\left(1-\frac1n\right)}}\to\dfrac{1}{\frac{1}{\sqrt2}+\frac{1}{\sqrt2}}=\boldsymbol{\dfrac{\sqrt2}{2}}$",
  "note": r"$\displaystyle\lim_{n\to\infty}(1^2+2^2+\cdots+n^2)$ と $\displaystyle\lim_{n\to\infty}n(1+2+\cdots+n)$ を別々に求めることはできない（どちらも発散）。",
  "ex": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{1^3+2^3+\cdots+n^3}{n(1^2+2^2+\cdots+n^2)}$　(2) $\displaystyle\lim_{n\to\infty}\left(\sqrt{2+4+6+\cdots+2n}-n\right)$",
  "exa": r"(1) $\dfrac34$　(2) $\dfrac12$"},
 {"lv": 3, "title": r"極限値から係数を決定する（数列）",
  "q": r"$a>0$ とする。$\displaystyle\lim_{n\to\infty}\left(\sqrt{an^2+bn+1}-3n\right)=2$ が成り立つように、定数 $a,\ b$ の値を定めよ。",
  "hint": r"$a\neq9$ だと $\sqrt{an^2}$ と $3n$ の「主要部」が打ち消し合わず、$\pm\infty$ に発散してしまう。まず <b>$n$ でくくって $a$ を決め（必要条件）</b>、次に有理化して $b$ を決める。",
  "sol": r"$\sqrt{an^2+bn+1}-3n=n\left(\sqrt{a+\frac bn+\frac1{n^2}}-3\right)$<br>"
         r"$a\neq9$ とすると、かっこ内は $\sqrt a-3\neq0$ に収束するから、全体は $+\infty$ または $-\infty$ に発散し、条件に反する。よって $a=9$ が必要。<br>"
         r"$a=9$ のとき<br>"
         r"$\sqrt{9n^2+bn+1}-3n=\dfrac{bn+1}{\sqrt{9n^2+bn+1}+3n}=\dfrac{b+\frac1n}{\sqrt{9+\frac bn+\frac1{n^2}}+3}\to\dfrac{b}{6}$<br>"
         r"$\dfrac b6=2$ より $b=12$。このとき確かに極限値は $2$ である。<br>"
         r"よって　$\boldsymbol{a=9,\ b=12}$",
  "note": r"「必要条件で候補を絞る → 実際に条件を満たすか確かめる（十分性）」という流れは、極限値から係数を決める問題の定石。ここでは $b$ を求める計算自体が十分性の確認を兼ねている。",
  "ex": r"$a>0$ とする。$\displaystyle\lim_{n\to\infty}\left(\sqrt{an^2+bn}-2n\right)=\frac32$ が成り立つように、定数 $a,\ b$ の値を定めよ。",
  "exa": r"$a=4,\ b=6$"},
]})

# ---------------------------------------------------------------- 節2
SEC.append({"title": r"$r^n$ を含む極限・はさみうちの原理",
"base": r"""・数列 $\{r^n\}$ の極限：$r>1$ のとき $\infty$，$r=1$ のとき $1$，$|r|<1$ のとき $0$，$r\leqq-1$ のとき振動。<b>$\{r^n\}$ が収束 ⇔ $-1<r\leqq1$</b><br>
・はさみうちの原理：$a_n\leqq c_n\leqq b_n$ かつ $\lim a_n=\lim b_n=\alpha$ ならば $\lim c_n=\alpha$。また $a_n\leqq b_n$，$\lim a_n=\infty$ ならば $\lim b_n=\infty$<br>
・評価によく使う不等式：$|\sin\theta|\leqq1$，$x-1<[x]\leqq x$（$[x]$ は $x$ を超えない最大の整数），<br>
　$h>0$ のとき $(1+h)^n\geqq1+nh+\dfrac{n(n-1)}{2}h^2$（二項定理の初めの3項）""",
"items": [
 {"lv": 1, "title": r"$r^n$ を含む数列の極限（底が最大の項で割る）",
  "q": r"次の極限を調べよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{4^{n+1}-3^n}{4^n+2^n}$　(2) $\displaystyle\lim_{n\to\infty}\frac{3^n-(-2)^n}{3^{n+1}+2^n}$　(3) $\displaystyle\lim_{n\to\infty}(3^n-5^n)$",
  "hint": r"<b>分母（(3) では式全体）の中で底の絶対値が最大のもの</b>で割る（くくる）と、残りは $|r|<1$ の $r^n$ になって $0$ に収束する。",
  "sol": r"(1) 分子・分母を $4^n$ で割ると　$\dfrac{4-\left(\frac34\right)^n}{1+\left(\frac12\right)^n}\to\dfrac{4-0}{1+0}=\boldsymbol{4}$<br>"
         r"(2) 分子・分母を $3^n$ で割ると　$\dfrac{1-\left(-\frac23\right)^n}{3+\left(\frac23\right)^n}\to\dfrac{1-0}{3+0}=\boldsymbol{\dfrac13}$<br>"
         r"(3) $3^n-5^n=5^n\left\{\left(\dfrac35\right)^n-1\right\}$ で、$5^n\to\infty$，$\left(\dfrac35\right)^n-1\to-1$ であるから　$\boldsymbol{-\infty}$",
  "note": r"(2) の $\left(-\frac23\right)^n$ は符号を変えながら $0$ に近づく。$|r|<1$ なら $r$ が負でも $r^n\to0$ である。",
  "ex": r"次の極限を調べよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{5^n-3^{n+1}}{5^{n+1}+2^n}$　(2) $\displaystyle\lim_{n\to\infty}\frac{2^{2n}-3^n}{3^n+1}$　(3) $\displaystyle\lim_{n\to\infty}\{2^n-(-3)^n\}$",
  "exa": r"(1) $\dfrac15$　(2) $\infty$　(3) 振動する（極限はない）"},
 {"lv": 2, "title": r"$r^n$ を含む極限（$r$ の値で場合分け）",
  "q": r"$r\neq-1$ とする。$\displaystyle\lim_{n\to\infty}\frac{r^{n+1}+2}{r^n+1}$ を求めよ。",
  "hint": r"$r^n$ の極限は $|r|<1$，$r=1$，$|r|>1$ で異なる（$r=-1$ は除かれている）。$|r|>1$ のときは分子・分母を $r^n$ で割り、$\left(\frac1r\right)^n\to0$ を使う。",
  "sol": r"[1] $|r|<1$ のとき　$r^n\to0$，$r^{n+1}\to0$ より　与式 $=\dfrac{0+2}{0+1}=2$<br>"
         r"[2] $r=1$ のとき　$\dfrac{1+2}{1+1}=\dfrac32$<br>"
         r"[3] $|r|>1$ のとき　分子・分母を $r^n$ で割ると、$\left|\frac1r\right|<1$ より<br>"
         r"$\dfrac{r+2\left(\frac1r\right)^n}{1+\left(\frac1r\right)^n}\to\dfrac{r+0}{1+0}=r$<br>"
         r"よって　$|r|<1$ のとき $\boldsymbol{2}$，$r=1$ のとき $\boldsymbol{\dfrac32}$，$|r|>1$ のとき $\boldsymbol{r}$",
  "note": r"$r=-1$ のとき $n$ が奇数で分母が $0$ になるので除外されている。この極限を $r$ の関数とみると、$r=1$ の左側で $2$，右側で $r\to1$ となり、$r=1$ で不連続になる（22.7 節の題材）。",
  "ex": r"$\displaystyle\lim_{n\to\infty}\frac{1-r^{2n}}{1+r^{2n}}$ を求めよ。",
  "exa": r"$|r|<1$ のとき $1$，$|r|=1$ のとき $0$，$|r|>1$ のとき $-1$"},
 {"lv": 2, "title": r"はさみうちの原理（三角関数・ガウス記号）",
  "q": r"次の極限を求めよ。ただし $[x]$ は $x$ を超えない最大の整数を表す。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{n\sin n}{n^2+1}$　(2) $\displaystyle\lim_{n\to\infty}\frac{[\sqrt3\,n]}{n}$",
  "hint": r"$\sin n$ や $[\sqrt3\,n]$ は簡単な式で表せないが、$|\sin n|\leqq1$，$x-1<[x]\leqq x$ のように<b>不等式ではさめる</b>。両側が同じ値に収束すれば、はさみうちの原理が使える。",
  "sol": r"(1) $|\sin n|\leqq1$ より　$0\leqq\left|\dfrac{n\sin n}{n^2+1}\right|\leqq\dfrac{n}{n^2+1}$<br>"
         r"$\dfrac{n}{n^2+1}=\dfrac{\frac1n}{1+\frac1{n^2}}\to0$ であるから、はさみうちの原理により $\left|\dfrac{n\sin n}{n^2+1}\right|\to0$。よって　$\boldsymbol{0}$<br>"
         r"(2) $\sqrt3\,n-1<[\sqrt3\,n]\leqq\sqrt3\,n$ の各辺を $n$ で割ると　$\sqrt3-\dfrac1n<\dfrac{[\sqrt3\,n]}{n}\leqq\sqrt3$<br>"
         r"$\sqrt3-\dfrac1n\to\sqrt3$ であるから　$\displaystyle\lim_{n\to\infty}\frac{[\sqrt3\,n]}{n}=\boldsymbol{\sqrt3}$",
  "note": r"$\sin n$ は収束しないので、(1) を $\lim\sin n\cdot\lim\dfrac{n}{n^2+1}$ と分けてはいけない。$|a_n|\to0$ と $a_n\to0$ は同値である。",
  "ex": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{n\to\infty}\frac{\sqrt n\cos n}{n+1}$　(2) $\displaystyle\lim_{n\to\infty}\frac{[\,5n+\sqrt n\,]}{2n}$",
  "exa": r"(1) $0$　(2) $\dfrac52$"},
 {"lv": 3, "title": r"二項定理による評価（$\frac{n^2}{2^n}\to0$）",
  "q": r"(1) $n\geqq3$ のとき、$2^n\geqq\dfrac{n(n-1)(n-2)}{6}$ であることを示せ。<br>(2) $\displaystyle\lim_{n\to\infty}\frac{n^2}{2^n}$ を求めよ。",
  "hint": r"$\dfrac{\infty}{\infty}$ の形だが、$2^n$ は割り算で処理できない。$2^n=(1+1)^n$ を<b>二項定理で展開し、一部の項だけ残して下から評価</b>する。分子の $n^2$ より次数の高い $n^3$ の項を残すのがポイント。",
  "sol": r"(1) $n\geqq3$ のとき、二項定理より<br>"
         r"$2^n=(1+1)^n={}_n\mathrm{C}_0+{}_n\mathrm{C}_1+\cdots+{}_n\mathrm{C}_n\geqq{}_n\mathrm{C}_3=\dfrac{n(n-1)(n-2)}{6}$　（各項は正）<br>"
         r"(2) $n\geqq3$ のとき、(1) より<br>"
         r"$0<\dfrac{n^2}{2^n}\leqq\dfrac{6n^2}{n(n-1)(n-2)}=\dfrac{6n}{(n-1)(n-2)}=\dfrac{\frac6n}{\left(1-\frac1n\right)\left(1-\frac2n\right)}$<br>"
         r"右辺 $\to0$ であるから、はさみうちの原理により　$\displaystyle\lim_{n\to\infty}\frac{n^2}{2^n}=\boldsymbol{0}$",
  "note": r"同様に、$r>1$，$k$ が自然数のとき $\dfrac{n^k}{r^n}\to0$（$r=1+h$ とおき $(1+h)^n\geqq{}_n\mathrm{C}_{k+1}h^{k+1}$ を使う）。「指数関数は多項式より速く増大する」という重要な事実で、後の無限級数でも使う。特に $\dfrac{n}{2^n}\to0$ である（$0<\frac{n}{2^n}\leqq\frac{n^2}{2^n}$）。",
  "ex": r"$(1.1)^n=(1+0.1)^n$ に二項定理を用いて、$\displaystyle\lim_{n\to\infty}\frac{n}{(1.1)^n}$ を求めよ。",
  "exa": r"$0$（$n\geqq2$ で $(1.1)^n\geqq\frac{n(n-1)}{2}\cdot0.01$ より $0<\frac{n}{(1.1)^n}\leqq\frac{200}{n-1}$）"},
 {"lv": 3, "title": r"和のはさみうち（各項を最大・最小の項で評価）",
  "q": r"$\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}\frac{1}{\sqrt{n^2+k}}$ を求めよ。",
  "hint": r"この和は公式で計算できない。$1\leqq k\leqq n$ で各項は $k=n$ のとき最小、$k=1$ のとき最大なので、<b>「（最小の項）$\times n$ ≦ 和 ≦（最大の項）$\times n$」</b>ではさむ。",
  "sol": r"$1\leqq k\leqq n$ のとき　$n^2+1\leqq n^2+k\leqq n^2+n$ より　$\dfrac{1}{\sqrt{n^2+n}}\leqq\dfrac{1}{\sqrt{n^2+k}}\leqq\dfrac{1}{\sqrt{n^2+1}}$<br>"
         r"$k=1,\ 2,\ \cdots,\ n$ について辺々を加えると<br>"
         r"$\dfrac{n}{\sqrt{n^2+n}}\leqq\displaystyle\sum_{k=1}^{n}\frac{1}{\sqrt{n^2+k}}\leqq\dfrac{n}{\sqrt{n^2+1}}$<br>"
         r"$\dfrac{n}{\sqrt{n^2+n}}=\dfrac{1}{\sqrt{1+\frac1n}}\to1$，$\dfrac{n}{\sqrt{n^2+1}}=\dfrac{1}{\sqrt{1+\frac1{n^2}}}\to1$<br>"
         r"よって、はさみうちの原理により　$\displaystyle\lim_{n\to\infty}\sum_{k=1}^{n}\frac{1}{\sqrt{n^2+k}}=\boldsymbol{1}$",
  "note": r"この評価がうまくいくのは、最大の項と最小の項の比が $1$ に近づくから。$\displaystyle\sum_{k=1}^{n}\frac{1}{n+k}$ では同じ評価をすると $\frac12$ と $1$ になり、はさめない（区分求積法で $\log2$ と求まる。第25章）。",
  "ex": r"$\displaystyle\lim_{n\to\infty}\sum_{k=1}^{2n}\frac{1}{\sqrt{n^2+k}}$ を求めよ。",
  "exa": r"$2$"},
 {"lv": 4, "title": r"$\sqrt[n]{n}\to1$ とその応用（$n$ 乗根の極限）",
  "q": r"(1) $\displaystyle\lim_{n\to\infty}\sqrt[n]{n}=1$ を示せ。<br>(2) $\displaystyle\lim_{n\to\infty}\sqrt[n]{{}_{2n}\mathrm{C}_n}$ を求めよ。",
  "hint": r"(1) $\sqrt[n]{n}=1+h_n$（$h_n>0$）とおくと $n=(1+h_n)^n$。右辺を二項定理で<b>$h_n^2$ の項だけ残して</b>評価すると $h_n$ が上からおさえられる。<br>(2) ${}_{2n}\mathrm{C}_n$ は ${}_{2n}\mathrm{C}_0,\ \cdots,\ {}_{2n}\mathrm{C}_{2n}$（和が $4^n$）の中で最大。これで ${}_{2n}\mathrm{C}_n$ を $4^n$ と $\frac{4^n}{2n+1}$ ではさむ。",
  "sol": r"(1) $n\geqq2$ とする。$n>1$ より $\sqrt[n]{n}>1$ なので、$\sqrt[n]{n}=1+h_n$（$h_n>0$）とおける。二項定理より<br>"
         r"$n=(1+h_n)^n\geqq1+nh_n+\dfrac{n(n-1)}{2}h_n^2>\dfrac{n(n-1)}{2}h_n^2$　よって　$0<h_n<\sqrt{\dfrac{2}{n-1}}$<br>"
         r"$\sqrt{\dfrac{2}{n-1}}\to0$ より $h_n\to0$。したがって $\displaystyle\lim_{n\to\infty}\sqrt[n]{n}=1$　（終）<br>"
         r"(2) $0\leqq k\leqq2n-1$ のとき $\dfrac{{}_{2n}\mathrm{C}_{k+1}}{{}_{2n}\mathrm{C}_k}=\dfrac{2n-k}{k+1}$ は、$k\leqq n-1$ で $1$ より大きく、$k\geqq n$ で $1$ より小さい。よって ${}_{2n}\mathrm{C}_k$ は $k=n$ で最大である。<br>"
         r"$\displaystyle\sum_{k=0}^{2n}{}_{2n}\mathrm{C}_k=2^{2n}=4^n$ で、項は $2n+1$ 個あるから　$\dfrac{4^n}{2n+1}\leqq{}_{2n}\mathrm{C}_n\leqq4^n$<br>"
         r"各辺の $n$ 乗根をとると　$\dfrac{4}{\sqrt[n]{2n+1}}\leqq\sqrt[n]{{}_{2n}\mathrm{C}_n}\leqq4$<br>"
         r"$n\geqq3$ のとき　$1<\sqrt[n]{2n+1}\leqq\sqrt[n]{3n}=\sqrt[n]{3}\,\sqrt[n]{n}\leqq\sqrt[n]{n}\cdot\sqrt[n]{n}$（$3\leqq n$ より）で、(1) より右辺 $\to1$。よって $\sqrt[n]{2n+1}\to1$<br>"
         r"はさみうちの原理により　$\displaystyle\lim_{n\to\infty}\sqrt[n]{{}_{2n}\mathrm{C}_n}=\boldsymbol{4}$",
  "note": r"$a>0$ の定数なら $\sqrt[n]{a}\to1$，また $\sqrt[n]{n^k}=(\sqrt[n]{n})^k\to1$。したがって $n$ 乗根の極限では「多項式程度の因子」は無視できる。(2) は ${}_{2n}\mathrm{C}_n$ が「ほぼ $4^n$ の大きさ」であることを示している。",
  "ex": r"$\displaystyle\lim_{n\to\infty}\sqrt[n]{n^3+2^n}$ を求めよ。",
  "exa": r"$2$（$n\geqq2$ で $2^n<n^3+2^n<n^3\cdot2^n$ を利用）"},
 {"lv": 5, "title": r"はさみうちの精密化（$n(S_n-1)$ の極限）",
  "q": r"$S_n=\displaystyle\sum_{k=1}^{n}\frac{n}{n^2+k}$ とする。<br>(1) $\displaystyle\lim_{n\to\infty}S_n$ を求めよ。<br>(2) $\displaystyle\lim_{n\to\infty}n(S_n-1)$ を求めよ。",
  "hint": r"(1) は各項を最大・最小の項ではさめばよい。しかしその評価では $n(S_n-1)$ は $-1$ と $0$ にしかはさめず、(2) には粗すぎる。<br>そこで $\dfrac{n}{n^2+k}=\dfrac1n\cdot\dfrac{1}{1+t}$（$t=\frac{k}{n^2}$）と見て、<b>$1-t<\dfrac{1}{1+t}<1-t+t^2$</b> という一段精密な評価を使う。",
  "sol": r"(1) $1\leqq k\leqq n$ のとき $\dfrac{n}{n^2+n}\leqq\dfrac{n}{n^2+k}\leqq\dfrac{n}{n^2+1}$。辺々加えて　$\dfrac{n^2}{n^2+n}\leqq S_n\leqq\dfrac{n^2}{n^2+1}$<br>"
         r"両端はともに $1$ に収束するから　$\displaystyle\lim_{n\to\infty}S_n=\boldsymbol{1}$<br>"
         r"(2) $t>0$ のとき、$(1+t)(1-t)=1-t^2<1$，$(1+t)(1-t+t^2)=1+t^3>1$ より　$1-t<\dfrac{1}{1+t}<1-t+t^2$<br>"
         r"$\dfrac{n}{n^2+k}=\dfrac1n\cdot\dfrac{1}{1+\frac{k}{n^2}}$ に $t=\dfrac{k}{n^2}$ として用いると<br>"
         r"$\dfrac1n\left(1-\dfrac{k}{n^2}\right)<\dfrac{n}{n^2+k}<\dfrac1n\left(1-\dfrac{k}{n^2}+\dfrac{k^2}{n^4}\right)$<br>"
         r"$k=1,\ \cdots,\ n$ について加える。$\displaystyle\sum_{k=1}^{n}\frac1n\left(1-\frac{k}{n^2}\right)=1-\frac{1}{n^3}\cdot\frac{n(n+1)}{2}=1-\frac{n+1}{2n^2}$，$\displaystyle\sum_{k=1}^{n}\frac{k^2}{n^5}=\frac{(n+1)(2n+1)}{6n^4}$ より<br>"
         r"$-\dfrac{n+1}{2n^2}<S_n-1<-\dfrac{n+1}{2n^2}+\dfrac{(n+1)(2n+1)}{6n^4}$<br>"
         r"各辺に $n$ を掛けると　$-\dfrac{n+1}{2n}<n(S_n-1)<-\dfrac{n+1}{2n}+\dfrac{(n+1)(2n+1)}{6n^3}$<br>"
         r"$-\dfrac{n+1}{2n}=-\dfrac12\left(1+\dfrac1n\right)\to-\dfrac12$，$\dfrac{(n+1)(2n+1)}{6n^3}=\dfrac{\left(1+\frac1n\right)\left(2+\frac1n\right)}{6n}\to0$<br>"
         r"よって、はさみうちの原理により　$\displaystyle\lim_{n\to\infty}n(S_n-1)=\boldsymbol{-\dfrac12}$",
  "note": r"(2) の結果は「$S_n$ は $1-\dfrac{1}{2n}$ にほぼ等しい」ことを意味する。はさみうちでは、<b>求めたい量の分だけ精密な評価</b>が必要になる。評価式 $1-t<\frac{1}{1+t}<1-t+t^2$ は、等比数列の和 $\frac{1}{1+t}=1-t+t^2-\cdots$ を途中で打ち切ったものと見ると覚えやすい。",
  "ex": r"$T_n=\displaystyle\sum_{k=1}^{n}\frac{n}{n^2+2k}$ とするとき、$\displaystyle\lim_{n\to\infty}n(T_n-1)$ を求めよ。",
  "exa": r"$-1$"},
]})

# ---------------------------------------------------------------- 節3
SEC.append({"title": r"無限級数",
"base": r"""・無限級数 $\displaystyle\sum_{n=1}^{\infty}a_n$ は、部分和 $S_n=\displaystyle\sum_{k=1}^{n}a_k$ の極限で定める。$\lim S_n=S$ のとき収束して和は $S$，$\{S_n\}$ が発散するとき無限級数は発散する。<br>
・無限等比級数 $\displaystyle\sum_{n=1}^{\infty}ar^{n-1}$ は、$a\neq0$ のとき <b>$|r|<1$ ならば収束して和 $\dfrac{a}{1-r}$</b>，$|r|\geqq1$ ならば発散。$a=0$ なら収束して和 $0$。<br>
・$\displaystyle\sum a_n$ が収束 ⇒ $\lim a_n=0$。したがって $\lim a_n=0$ でなければ発散する（逆は成り立たない）。<br>
・$\sum a_n$，$\sum b_n$ がともに収束するとき　$\sum(pa_n+qb_n)=p\sum a_n+q\sum b_n$""",
"items": [
 {"lv": 1, "title": r"無限等比級数の和と循環小数",
  "q": r"(1) 無限等比級数 $6-4+\dfrac83-\cdots$ の和を求めよ。<br>(2) $\displaystyle\sum_{n=1}^{\infty}\frac{2^n+(-1)^n}{3^n}$ を求めよ。<br>(3) 循環小数 $0.1\dot{2}\dot{3}$ を分数で表せ。",
  "hint": r"初項と公比を読みとり、<b>$|$公比$|<1$ を確認してから</b>公式 $\dfrac{a}{1-r}$ を使う。(2) は収束する2つの無限等比級数に分ける。(3) は $0.1+0.023+0.00023+\cdots$ と見る。",
  "sol": r"(1) 初項 $6$，公比 $-\dfrac23$ で $\left|-\dfrac23\right|<1$ より収束し、和は　$\dfrac{6}{1-\left(-\frac23\right)}=\boldsymbol{\dfrac{18}{5}}$<br>"
         r"(2) $\displaystyle\sum_{n=1}^{\infty}\left(\frac23\right)^n$ は公比 $\frac23$，$\displaystyle\sum_{n=1}^{\infty}\left(-\frac13\right)^n$ は公比 $-\frac13$ でともに収束し<br>"
         r"$\displaystyle\sum_{n=1}^{\infty}\left(\frac23\right)^n=\frac{\frac23}{1-\frac23}=2$，$\displaystyle\sum_{n=1}^{\infty}\left(-\frac13\right)^n=\frac{-\frac13}{1+\frac13}=-\frac14$　よって　与式 $=2-\dfrac14=\boldsymbol{\dfrac74}$<br>"
         r"(3) $0.1\dot{2}\dot{3}=0.1+0.023+0.00023+\cdots$ で、$0.1$ より後ろは初項 $\dfrac{23}{1000}$，公比 $\dfrac{1}{100}$ の無限等比級数であるから<br>"
         r"$0.1\dot{2}\dot{3}=\dfrac{1}{10}+\dfrac{\frac{23}{1000}}{1-\frac{1}{100}}=\dfrac{1}{10}+\dfrac{23}{990}=\dfrac{122}{990}=\boldsymbol{\dfrac{61}{495}}$",
  "note": r"(2) で和を2つに分けてよいのは、<b>分けた2つの級数がともに収束する</b>から。収束を確かめずに分けると誤ることがある（例：$\sum\{1+(-1)\}=0$ だが $\sum1$，$\sum(-1)$ はともに発散）。",
  "ex": r"(1) 無限等比級数 $\sqrt2+1+\dfrac{1}{\sqrt2}+\cdots$ の和を求めよ。<br>(2) $\displaystyle\sum_{n=1}^{\infty}\frac{3^n-2^n}{4^n}$ を求めよ。<br>(3) 循環小数 $0.\dot{2}\dot{7}$ を分数で表せ。",
  "exa": r"(1) $2\sqrt2+2$　(2) $2$　(3) $\dfrac{3}{11}$"},
 {"lv": 1, "title": r"部分和を求めて調べる無限級数（差の形に分解）",
  "q": r"次の無限級数の収束・発散を調べ、収束する場合はその和を求めよ。<br>(1) $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$　(2) $\displaystyle\sum_{n=1}^{\infty}\frac{1}{\sqrt{n+1}+\sqrt{n}}$",
  "hint": r"無限級数は部分和 $S_n$ の極限。<b>一般項を「差」の形に変形</b>すると、部分和で途中の項が消えて $S_n$ が求まる。(1) は部分分数分解、(2) は有理化。",
  "sol": r"(1) $\dfrac{1}{k(k+2)}=\dfrac12\left(\dfrac1k-\dfrac{1}{k+2}\right)$ より<br>"
         r"$S_n=\dfrac12\left\{\left(1-\dfrac13\right)+\left(\dfrac12-\dfrac14\right)+\cdots+\left(\dfrac1n-\dfrac1{n+2}\right)\right\}=\dfrac12\left(1+\dfrac12-\dfrac1{n+1}-\dfrac1{n+2}\right)$<br>"
         r"$\displaystyle\lim_{n\to\infty}S_n=\frac12\cdot\frac32=\frac34$　よって　<b>収束し、和は $\boldsymbol{\dfrac34}$</b><br>"
         r"(2) $\dfrac{1}{\sqrt{k+1}+\sqrt k}=\sqrt{k+1}-\sqrt k$ より<br>"
         r"$S_n=(\sqrt2-1)+(\sqrt3-\sqrt2)+\cdots+(\sqrt{n+1}-\sqrt n)=\sqrt{n+1}-1\to\infty$　よって　<b>発散する</b>",
  "note": r"(2) は一般項が $0$ に収束するのに、無限級数は発散する例。「$\lim a_n=0$」は収束の必要条件にすぎない。",
  "ex": r"次の無限級数の収束・発散を調べ、収束する場合はその和を求めよ。<br>(1) $\displaystyle\sum_{n=1}^{\infty}\frac{1}{(3n-2)(3n+1)}$　(2) $\displaystyle\sum_{n=1}^{\infty}\log\frac{n+1}{n}$",
  "exa": r"(1) 収束し、和は $\dfrac13$　(2) 発散する（$S_n=\log(n+1)\to\infty$）"},
 {"lv": 2, "title": r"無限等比級数が収束する条件（収束する $x$ の範囲と和）",
  "q": r"無限級数 $x+x(1-x)+x(1-x)^2+\cdots+x(1-x)^{n-1}+\cdots$ が収束するような実数 $x$ の値の範囲を求めよ。また、そのときの和を求めよ。",
  "hint": r"初項 $x$，公比 $1-x$ の無限等比級数。収束するのは<b>「初項 $=0$」または「$|$公比$|<1$」</b>のとき。初項 $0$ の場合を落とさないこと。",
  "sol": r"初項 $x$，公比 $1-x$ の無限等比級数である。<br>"
         r"[1] $x=0$ のとき　すべての項が $0$ で、収束して和は $0$<br>"
         r"[2] $x\neq0$ のとき　収束する条件は $|1-x|<1$，すなわち $0<x<2$。このとき和は　$\dfrac{x}{1-(1-x)}=1$<br>"
         r"よって　<b>収束する範囲は $\boldsymbol{0\leqq x<2}$，和は $x=0$ のとき $\boldsymbol{0}$，$0<x<2$ のとき $\boldsymbol{1}$</b>",
  "note": r"和を $x$ の関数 $f(x)$（$0\leqq x<2$）とみると、$f(0)=0$，$0<x<2$ で $f(x)=1$ となり、$x=0$ で不連続である。各項は $x$ の連続関数なのに、無限個加えると連続でなくなることがある。",
  "ex": r"無限級数 $\displaystyle\sum_{n=1}^{\infty}\frac{x^2}{(1+x^2)^{n-1}}$ が収束するような実数 $x$ の値の範囲と、そのときの和を求めよ。",
  "exa": r"すべての実数 $x$ で収束し、和は $x\neq0$ のとき $1+x^2$，$x=0$ のとき $0$"},
 {"lv": 2, "title": r"かっこのついた級数とはずした級数",
  "q": r"次の無限級数の収束・発散を調べ、収束する場合はその和を求めよ。<br>(1) $\left(1-\dfrac23\right)+\left(\dfrac23-\dfrac35\right)+\left(\dfrac35-\dfrac47\right)+\cdots$<br>(2) $1-\dfrac23+\dfrac23-\dfrac35+\dfrac35-\dfrac47+\cdots$",
  "hint": r"(1) は第 $n$ 項が $\left(\dfrac{n}{2n-1}-\dfrac{n+1}{2n+1}\right)$ の級数。(2) はかっこをはずしたので、1つ1つの分数が「項」になり部分和の列が変わる。<b>部分和を $S_{2n-1}$ と $S_{2n}$ に分けて</b>調べる。",
  "sol": r"(1) 第 $k$ 項は $\dfrac{k}{2k-1}-\dfrac{k+1}{2k+1}$ であるから、部分和は<br>"
         r"$S_n=\left(1-\dfrac23\right)+\left(\dfrac23-\dfrac35\right)+\cdots+\left(\dfrac{n}{2n-1}-\dfrac{n+1}{2n+1}\right)=1-\dfrac{n+1}{2n+1}$<br>"
         r"$\dfrac{n+1}{2n+1}=\dfrac{1+\frac1n}{2+\frac1n}\to\dfrac12$ より $S_n\to\dfrac12$。よって　<b>収束し、和は $\boldsymbol{\dfrac12}$</b><br>"
         r"(2) 第 $n$ 項までの部分和を $T_n$ とすると<br>"
         r"$T_{2n}=1-\dfrac{n+1}{2n+1}$，$T_{2n-1}=T_{2n}+\dfrac{n+1}{2n+1}=1$<br>"
         r"$n\to\infty$ のとき $T_{2n}\to\dfrac12$，$T_{2n-1}\to1$ で、極限が一致しないから　<b>発散する</b>",
  "note": r"(2) は、第 $2n$ 項 $-\dfrac{n+1}{2n+1}$ が $-\dfrac12$ に収束し、一般項が $0$ に収束しないことからも発散とわかる。無限級数では、<b>かっこを勝手にはずしたりつけたりしてはいけない</b>。",
  "ex": r"次の無限級数の収束・発散を調べ、収束する場合はその和を求めよ。<br>(1) $\left(\dfrac12-\dfrac23\right)+\left(\dfrac23-\dfrac34\right)+\left(\dfrac34-\dfrac45\right)+\cdots$<br>(2) $\dfrac12-\dfrac23+\dfrac23-\dfrac34+\dfrac34-\dfrac45+\cdots$",
  "exa": r"(1) 収束し、和は $-\dfrac12$　(2) 発散する"},
 {"lv": 3, "title": r"（等差）×（等比）型の無限級数",
  "q": r"無限級数 $\displaystyle\sum_{n=1}^{\infty}\frac{n}{2^n}=\frac12+\frac{2}{2^2}+\frac{3}{2^3}+\cdots$ の和を求めよ。",
  "hint": r"部分和 $S_n$ は「（等差）×（等比）の和」なので、<b>$S_n-\frac12S_n$ を計算</b>して等比数列の和に帰着させる。極限では $\dfrac{n}{2^n}\to0$（22.2 節）を使う。",
  "sol": r"$S_n=\dfrac12+\dfrac2{2^2}+\dfrac3{2^3}+\cdots+\dfrac{n}{2^n}$ とおくと<br>"
         r"$\dfrac12S_n=\dfrac1{2^2}+\dfrac2{2^3}+\cdots+\dfrac{n-1}{2^n}+\dfrac{n}{2^{n+1}}$<br>"
         r"辺々引くと　$\dfrac12S_n=\dfrac12+\dfrac1{2^2}+\cdots+\dfrac1{2^n}-\dfrac{n}{2^{n+1}}=1-\dfrac1{2^n}-\dfrac{n}{2^{n+1}}$<br>"
         r"よって　$S_n=2-\dfrac{2}{2^n}-\dfrac{n}{2^n}=2-\dfrac{n+2}{2^n}$<br>"
         r"$\dfrac{n}{2^n}\to0$，$\dfrac{1}{2^n}\to0$ であるから　$\displaystyle\sum_{n=1}^{\infty}\frac{n}{2^n}=\lim_{n\to\infty}S_n=\boldsymbol{2}$",
  "note": r"一般に $|r|<1$ のとき $\displaystyle\sum_{n=1}^{\infty}nr^{n-1}=\frac{1}{(1-r)^2}$（$nr^n\to0$ は二項定理による評価で示せる）。$S_n$ を求めずに「$S=\sum\frac{n}{2^n}$ とおいて $S-\frac12S$」とするのは、$S$ が収束することを先に示していないので答案としては不十分。",
  "ex": r"無限級数 $\displaystyle\sum_{n=1}^{\infty}\frac{2n-1}{3^n}$ の和を求めよ。",
  "exa": r"$1$"},
 {"lv": 4, "title": r"図形と無限等比級数（角に内接する円の列）",
  "q": r"""1辺の長さが $1$ の正三角形 ABC の内接円を $C_0$ とする。辺 AB，AC に接し、$C_0$ に外接する円のうち小さい方を $C_1$ とし、さらに AB，AC に接し $C_1$ に外接する円のうち小さい方を $C_2$ とする。以下同様に $C_3,\ C_4,\ \cdots$ をつくる。頂点 B，C の近くにも同様に円の列をつくるとき、$C_0$ とこれらすべての円の面積の和を求めよ。<svg class="fig" width="194" height="179" viewBox="0 0 194 179"><polygon points="97.0,17.0 12.0,164.2 182.0,164.2" fill="none" stroke="#1f3f8f" stroke-width="1.2"/><circle cx="97.0" cy="115.1" r="49.1" fill="#dbe4f6" stroke="#1f3f8f" stroke-width="1"/><circle cx="97.0" cy="49.7" r="16.4" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="97.0" cy="27.9" r="5.5" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="97.0" cy="20.6" r="1.8" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="40.3" cy="147.9" r="16.4" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="21.4" cy="158.8" r="5.5" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="15.1" cy="162.4" r="1.8" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="153.7" cy="147.9" r="16.4" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="172.6" cy="158.8" r="5.5" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><circle cx="178.9" cy="162.4" r="1.8" fill="#f6dede" stroke="#c0392b" stroke-width="0.8"/><text x="93.0" y="12.0" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">A</text><text x="9.0" y="176.2" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">B</text><text x="177.0" y="176.2" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">C</text><text x="91.0" y="119.1" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">C<tspan font-size="8" dy="2" font-style="normal">0</tspan></text><text x="116.4" y="53.7" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">C<tspan font-size="8" dy="2" font-style="normal">1</tspan></text></svg>""",
  "hint": r"2辺 AB，AC に接する円の中心は ∠A の二等分線上にある。<b>半径 $r$ と「A から中心までの距離」の関係</b>を使えば、隣り合う円の半径の比（公比）が一定であることがわかる。",
  "sol": r"AB，AC に接する半径 $r$ の円の中心 P は ∠A の二等分線上にあり、∠PAB $=30^\circ$ であるから　$\mathrm{AP}=\dfrac{r}{\sin30^\circ}=2r$<br>"
         r"$C_k$ の半径を $r_k$ とする（$C_0$ も AB，AC に接するので同様）。$C_k$ と $C_{k+1}$ は外接し、$C_{k+1}$ の中心の方が A に近いから、中心間の距離について<br>"
         r"$2r_k-2r_{k+1}=r_k+r_{k+1}$　よって　$r_{k+1}=\dfrac13r_k$<br>"
         r"$r_0$ は内接円の半径で $r_0=\dfrac{\sqrt3}{6}$，$r_0^2=\dfrac1{12}$。$C_k$ の面積は $\pi r_0^2\left(\dfrac19\right)^k$ である。<br>"
         r"頂点 A の近くの円 $C_1,\ C_2,\ \cdots$ の面積の和は、初項 $\dfrac{\pi r_0^2}{9}$，公比 $\dfrac19$ の無限等比級数で　$\dfrac{\frac{\pi r_0^2}{9}}{1-\frac19}=\dfrac{\pi r_0^2}{8}$<br>"
         r"B，C の近くも同じであるから、求める和は　$\pi r_0^2+3\cdot\dfrac{\pi r_0^2}{8}=\dfrac{11}{8}\pi r_0^2=\dfrac{11}{8}\cdot\dfrac{\pi}{12}=\boldsymbol{\dfrac{11}{96}\pi}$",
  "note": r"図形の無限等比級数では、<b>第 $k$ 番目と第 $k+1$ 番目の関係（相似比）</b>を1つ求めれば十分。面積の公比は長さの公比の2乗になる。角が $2\alpha$ なら $\mathrm{AP}=\dfrac{r}{\sin\alpha}$ から公比は $\dfrac{1-\sin\alpha}{1+\sin\alpha}$ となる。",
  "ex": r"1辺の長さが $2$ の正方形の内接円を $C_0$ とし、正方形の各頂点の近くに、例題と同様に、その頂点をはさむ2辺に接し前の円に外接する円の列をつくる。$C_0$ とこれらすべての円の面積の和を求めよ。",
  "exa": r"$\dfrac{(3\sqrt2-2)\pi}{2}$（半径の公比 $3-2\sqrt2$）"},
 {"lv": 5, "title": r"ガウス記号を含む無限級数（区間ごとにまとめる）",
  "q": r"正の整数 $n$ に対して $a_n=\dfrac{[\log_2n]}{n(n+1)}$ とする。ただし $[x]$ は $x$ を超えない最大の整数を表す。無限級数 $\displaystyle\sum_{n=1}^{\infty}a_n$ の和を求めよ。",
  "hint": r"$[\log_2n]$ は $2^k\leqq n<2^{k+1}$ の範囲で一定値 $k$ をとる。<b>この範囲ごとにまとめる</b>と、$\frac{1}{n(n+1)}=\frac1n-\frac1{n+1}$ の和は途中が消えて簡単になる。まず $N=2^m-1$ の部分和を求め、一般の $N$ は $a_n\geqq0$（部分和の単調性）を使ってはさむ。",
  "sol": r"部分和を $S_N=\displaystyle\sum_{n=1}^{N}a_n$ とする。<br>"
         r"整数 $k\geqq0$ に対し、$2^k\leqq n\leqq2^{k+1}-1$ のとき $k\leqq\log_2n<k+1$ より $[\log_2n]=k$。また<br>"
         r"$\displaystyle\sum_{n=2^k}^{2^{k+1}-1}\frac{1}{n(n+1)}=\sum_{n=2^k}^{2^{k+1}-1}\left(\frac1n-\frac1{n+1}\right)=\frac1{2^k}-\frac1{2^{k+1}}=\frac{1}{2^{k+1}}$<br>"
         r"よって、$m\geqq1$ に対し　$S_{2^m-1}=\displaystyle\sum_{k=0}^{m-1}\frac{k}{2^{k+1}}=\frac12\sum_{k=1}^{m-1}\frac{k}{2^k}$<br>"
         r"この節の（等差）×（等比）型の例題で求めた $\displaystyle\sum_{k=1}^{j}\frac{k}{2^k}=2-\frac{j+2}{2^j}$ に $j=m-1$ を代入して　$S_{2^m-1}=\dfrac12\left(2-\dfrac{m+1}{2^{m-1}}\right)=1-\dfrac{m+1}{2^m}$<br>"
         r"次に、一般の $N$ について考える。$N\geqq1$ に対し $2^m-1\leqq N<2^{m+1}-1$ となる整数 $m\geqq1$ をとる。$a_n\geqq0$ より $S_N$ は $N$ について単調に増加するから<br>"
         r"$S_{2^m-1}\leqq S_N\leqq S_{2^{m+1}-1}$　すなわち　$1-\dfrac{m+1}{2^m}\leqq S_N\leqq1-\dfrac{m+2}{2^{m+1}}$<br>"
         r"$N\to\infty$ のとき $m\to\infty$ で、$\dfrac{m+1}{2^m}\to0$，$\dfrac{m+2}{2^{m+1}}\to0$。はさみうちの原理により $S_N\to1$<br>"
         r"よって　$\displaystyle\sum_{n=1}^{\infty}a_n=\boldsymbol{1}$",
  "note": r"「ガウス記号が一定になる区間ごとにまとめる → 区切りの部分和を求める → 途中の $N$ は単調性ではさむ」は、桁数や $[\sqrt n]$ などを含む級数の定石。最後のはさむ手順を省くと、部分和の列の一部（$N=2^m-1$）しか調べていないことになる。",
  "ex": r"$\displaystyle\sum_{n=1}^{\infty}\frac{[\log_3n]}{n(n+1)}$ を求めよ。",
  "exa": r"$\dfrac12$"},
]})

# ---------------------------------------------------------------- 節4
SEC.append({"title": r"漸化式と極限",
"base": r"""・一般項が求められる漸化式は、<b>一般項を求めてから極限をとる</b>。$a_{n+1}=pa_n+q$ は $\alpha=p\alpha+q$ を満たす $\alpha$ を用いて $a_{n+1}-\alpha=p(a_n-\alpha)$。<br>
・一般項が求められないときは、極限の候補 $\alpha$（$a_{n+1}=f(a_n)$ なら $\alpha=f(\alpha)$ の解）を求め、<br>
　$|a_{n+1}-\alpha|\leqq r|a_n-\alpha|$（$0<r<1$）を示す。すると $|a_n-\alpha|\leqq r^{n-1}|a_1-\alpha|\to0$ となり $a_n\to\alpha$。<br>
・隣接3項間漸化式 $a_{n+2}=pa_{n+1}+qa_n$ は、$t^2=pt+q$ の解 $\alpha,\ \beta$ を用いて $a_{n+2}-\alpha a_{n+1}=\beta(a_{n+1}-\alpha a_n)$ と変形する。""",
"items": [
 {"lv": 1, "title": r"$a_{n+1}=pa_n+q$ 型の漸化式と極限",
  "q": r"$a_1=1,\ a_{n+1}=\dfrac13a_n+2$ で定まる数列 $\{a_n\}$ の極限を求めよ。",
  "hint": r"$\alpha=\dfrac13\alpha+2$ を満たす $\alpha=3$ を使って $a_{n+1}-3=\dfrac13(a_n-3)$ と変形し、<b>一般項を求めてから</b>極限をとる。",
  "sol": r"$\alpha=\dfrac13\alpha+2$ を解くと $\alpha=3$。漸化式は　$a_{n+1}-3=\dfrac13(a_n-3)$ と変形できる。<br>"
         r"数列 $\{a_n-3\}$ は初項 $a_1-3=-2$，公比 $\dfrac13$ の等比数列であるから　$a_n=3-2\left(\dfrac13\right)^{n-1}$<br>"
         r"$\left(\dfrac13\right)^{n-1}\to0$ より　$\displaystyle\lim_{n\to\infty}a_n=\boldsymbol{3}$",
  "note": r"「極限 $\alpha$ が存在すると仮定して $\alpha=\frac13\alpha+2$」と解くだけでは不十分。極限が存在する保証がないからである。例えば $a_1=1,\ a_{n+1}=2a_n-3$ でも $\alpha=3$ が得られるが、実際は $a_n=3-2^n\to-\infty$ となる。",
  "ex": r"$a_1=0,\ a_{n+1}=-\dfrac12a_n+3$ で定まる数列 $\{a_n\}$ の極限を求めよ。",
  "exa": r"$2$（$a_n=2-2\left(-\frac12\right)^{n-1}$）"},
 {"lv": 3, "title": r"分数型の漸化式と極限",
  "q": r"$a_1=2,\ a_{n+1}=\dfrac{2a_n+1}{a_n+2}$ で定まる数列 $\{a_n\}$ の一般項と極限を求めよ。",
  "hint": r"$x=\dfrac{2x+1}{x+2}$ の解は $x=\pm1$。<b>$b_n=\dfrac{a_n-1}{a_n+1}$ とおくと等比数列</b>になる。$a_{n+1}-1$ と $a_{n+1}+1$ をそれぞれ $a_n$ で表して割る。",
  "sol": r"$a_1>0$ で、$a_n>0$ ならば $a_{n+1}>0$ であるから、すべての $n$ で $a_n>0$（よって分母は $0$ にならない）。<br>"
         r"$a_{n+1}-1=\dfrac{2a_n+1-(a_n+2)}{a_n+2}=\dfrac{a_n-1}{a_n+2}$，$a_{n+1}+1=\dfrac{2a_n+1+(a_n+2)}{a_n+2}=\dfrac{3(a_n+1)}{a_n+2}$<br>"
         r"辺々割ると　$\dfrac{a_{n+1}-1}{a_{n+1}+1}=\dfrac13\cdot\dfrac{a_n-1}{a_n+1}$<br>"
         r"$b_n=\dfrac{a_n-1}{a_n+1}$ とおくと $b_1=\dfrac13$，$b_{n+1}=\dfrac13b_n$ より　$b_n=\left(\dfrac13\right)^n$<br>"
         r"$b_n=\dfrac{a_n-1}{a_n+1}$ を $a_n$ について解くと $a_n=\dfrac{1+b_n}{1-b_n}$ であるから<br>"
         r"$a_n=\dfrac{1+\frac{1}{3^n}}{1-\frac{1}{3^n}}=\boldsymbol{\dfrac{3^n+1}{3^n-1}}$，　$\displaystyle\lim_{n\to\infty}a_n=\lim_{n\to\infty}\frac{1+\frac1{3^n}}{1-\frac1{3^n}}=\boldsymbol{1}$",
  "note": r"$x=\dfrac{ax+b}{cx+d}$ が異なる2解 $\alpha,\ \beta$ をもつときは $\dfrac{a_n-\alpha}{a_n-\beta}$ が等比数列、重解 $\alpha$ のときは $\dfrac{1}{a_n-\alpha}$ が等差数列になる。極限は、公比の絶対値が $1$ より小さければ一方の解 $\alpha$ になる。",
  "ex": r"$a_1=3,\ a_{n+1}=\dfrac{3a_n+4}{a_n+3}$ で定まる数列 $\{a_n\}$ の一般項と極限を求めよ。",
  "exa": r"$a_n=\dfrac{2(5^n+1)}{5^n-1}$，極限は $2$"},
 {"lv": 4, "title": r"一般項が求められない漸化式（範囲を押さえて評価）",
  "q": r"$a_1=\dfrac32,\ a_{n+1}=\dfrac{a_n^2+2}{3}$ で定まる数列 $\{a_n\}$ の極限を求めよ。",
  "hint": r"一般項は求められない。極限の候補は $\alpha=\dfrac{\alpha^2+2}{3}$ の解 $\alpha=1,\ 2$ の2つ。<b>まず $a_n$ の範囲を帰納法で押さえ</b>、それを使って $|a_{n+1}-\alpha|\leqq r|a_n-\alpha|$（$0<r<1$）の形の評価を導く。",
  "sol": r"$\alpha=\dfrac{\alpha^2+2}{3}$ を解くと $\alpha=1,\ 2$。<br>"
         r"まず、すべての $n$ で $1<a_n\leqq\dfrac32$ であることを数学的帰納法で示す。$n=1$ では成り立つ。$1<a_k\leqq\dfrac32$ ならば $1<a_k^2\leqq\dfrac94$ より<br>"
         r"$1<a_{k+1}=\dfrac{a_k^2+2}{3}\leqq\dfrac{\frac94+2}{3}=\dfrac{17}{12}<\dfrac32$<br>"
         r"となり、$n=k+1$ でも成り立つ。<br>"
         r"次に　$a_{n+1}-1=\dfrac{a_n^2-1}{3}=\dfrac{a_n+1}{3}(a_n-1)$　で、$a_n-1>0$，$0<\dfrac{a_n+1}{3}\leqq\dfrac{\frac32+1}{3}=\dfrac56$ より<br>"
         r"$0<a_{n+1}-1\leqq\dfrac56(a_n-1)$<br>"
         r"これをくり返し用いて　$0<a_n-1\leqq\left(\dfrac56\right)^{n-1}(a_1-1)=\dfrac12\left(\dfrac56\right)^{n-1}$<br>"
         r"$\left(\dfrac56\right)^{n-1}\to0$ であるから、はさみうちの原理により　$\displaystyle\lim_{n\to\infty}a_n=\boldsymbol{1}$",
  "note": r"候補が2つあるとき、どちらに収束するかは初項で決まる。$a_{n+1}-2=\dfrac{(a_n+2)(a_n-2)}{3}$ なので、$a_1>2$ なら $a_n-2\geqq\left(\frac43\right)^{n-1}(a_1-2)$ となって $a_n\to\infty$。また $a_{n+1}-a_n=\dfrac{(a_n-1)(a_n-2)}{3}$ から、例題では $\{a_n\}$ は減少している。$y=\frac{x^2+2}{3}$ と $y=x$ のグラフで、点が階段状に動く様子をかくと見通しがよい。",
  "ex": r"$a_1=2,\ a_{n+1}=\dfrac{a_n^2+3}{4}$ で定まる数列 $\{a_n\}$ の極限を求めよ。",
  "exa": r"$1$（$1<a_n\leqq2$ を示し、$0<a_{n+1}-1\leqq\frac34(a_n-1)$）"},
 {"lv": 4, "title": r"隣接3項間漸化式と比の極限（確率への応用）",
  "q": r"1枚の硬貨を $n$ 回投げるとき、表が2回以上続けて出ることがない確率を $p_n$ とする。<br>(1) $n$ 回の表裏の出方のうち、表が2回以上続けて出ないものの総数を $a_n$ とする。$a_{n+2}=a_{n+1}+a_n$ を示せ。<br>(2) $\displaystyle\lim_{n\to\infty}\frac{p_{n+1}}{p_n}$ を求めよ。",
  "hint": r"(1) 最後（$n+2$ 回目）が裏か表かで場合分けする。表なら直前は必ず裏。<br>(2) $p_n=\dfrac{a_n}{2^n}$ なので $\dfrac{a_{n+1}}{a_n}$ の極限を調べる。$t^2=t+1$ の解 $\alpha,\ \beta$ で $a_{n+1}-\alpha a_n=\beta^{n-1}(a_2-\alpha a_1)$ と変形し、<b>両辺を $a_n$ で割る</b>。",
  "sol": r"(1) $n+2$ 回の出方で条件を満たすもののうち、<br>"
         r"・$n+2$ 回目が裏のもの：$n+1$ 回目までが条件を満たせばよく、$a_{n+1}$ 通り<br>"
         r"・$n+2$ 回目が表のもの：$n+1$ 回目は裏で、$n$ 回目までが条件を満たせばよく、$a_n$ 通り<br>"
         r"よって　$a_{n+2}=a_{n+1}+a_n$　（終）　なお $a_1=2$，$a_2=3$<br>"
         r"(2) $t^2=t+1$ の解を $\alpha=\dfrac{1+\sqrt5}{2}$，$\beta=\dfrac{1-\sqrt5}{2}$ とすると $\alpha+\beta=1$，$\alpha\beta=-1$ であるから、漸化式は<br>"
         r"$a_{n+2}-\alpha a_{n+1}=\beta(a_{n+1}-\alpha a_n)$　と変形でき<br>"
         r"$a_{n+1}-\alpha a_n=\beta^{n-1}(a_2-\alpha a_1)=(2-\sqrt5)\beta^{n-1}$<br>"
         r"両辺を $a_n$ で割ると　$\dfrac{a_{n+1}}{a_n}-\alpha=\dfrac{(2-\sqrt5)\beta^{n-1}}{a_n}$<br>"
         r"(1) より $a_{n+2}>a_{n+1}$ で $a_2>a_1$ なので、$\{a_n\}$ は増加し $a_n\geqq2$。また $|\beta|=\dfrac{\sqrt5-1}{2}<1$ であるから<br>"
         r"$\left|\dfrac{a_{n+1}}{a_n}-\alpha\right|\leqq\dfrac{(\sqrt5-2)|\beta|^{n-1}}{2}\to0$　よって　$\dfrac{a_{n+1}}{a_n}\to\alpha$<br>"
         r"$p_n=\dfrac{a_n}{2^n}$ より　$\displaystyle\lim_{n\to\infty}\frac{p_{n+1}}{p_n}=\lim_{n\to\infty}\frac{a_{n+1}}{2a_n}=\frac{\alpha}{2}=\boldsymbol{\frac{1+\sqrt5}{4}}$",
  "note": r"一般項は $a_n=\dfrac{\alpha^{n+2}-\beta^{n+2}}{\sqrt5}$（フィボナッチ数列）で、これを使って比の極限を求めてもよい。$\frac{a_{n+1}}{a_n}\to\alpha$（黄金比）は、$|\alpha|>|\beta|$ のとき「絶対値の大きい方の解」が支配的になることを表している。",
  "ex": r"0，1，2 の数字を重複を許して $n$ 個並べた列のうち、0 が2個以上続けて並ぶことがないものの個数を $c_n$ とする。$\displaystyle\lim_{n\to\infty}\frac{c_{n+1}}{c_n}$ を求めよ。",
  "exa": r"$1+\sqrt3$（$c_1=3,\ c_2=8,\ c_{n+2}=2c_{n+1}+2c_n$）"},
 {"lv": 5, "title": r"0 に収束する速さ（$na_n$ の極限）",
  "q": r"$a_1=\dfrac12,\ a_{n+1}=a_n-a_n^2$ で定まる数列 $\{a_n\}$ について、次の問いに答えよ。<br>(1) すべての $n$ について $0<a_n\leqq\dfrac{1}{n+1}$ であることを示せ。<br>(2) $\displaystyle\lim_{n\to\infty}na_n$ を求めよ。",
  "hint": r"$a_n\to0$ だが、その速さを知りたい。<b>逆数をとる</b>と　$\dfrac{1}{a_{n+1}}=\dfrac{1}{a_n(1-a_n)}=\dfrac1{a_n}+\dfrac{1}{1-a_n}$　となり、$\dfrac1{a_{n+1}}-\dfrac1{a_n}$ はほぼ $1$。これを足し合わせると $\dfrac1{a_n}$ はほぼ $n$ で、上下からの評価に (1) を再利用する。",
  "sol": r"(1) まず $0<a_n\leqq\dfrac12$ を帰納法で示す。$n=1$ で成り立ち、$0<a_k\leqq\dfrac12$ ならば $a_{k+1}=a_k(1-a_k)$ で $\dfrac12\leqq1-a_k<1$ より $0<a_{k+1}<a_k\leqq\dfrac12$。<br>"
         r"次に $\dfrac{1}{a_{n+1}}=\dfrac{1}{a_n(1-a_n)}=\dfrac{1}{a_n}+\dfrac{1}{1-a_n}$ で、$0<1-a_n<1$ より $\dfrac{1}{1-a_n}>1$。よって　$\dfrac1{a_{n+1}}-\dfrac1{a_n}>1$<br>"
         r"$n\geqq2$ のとき、これを $1$ から $n-1$ まで加えて $\dfrac1{a_n}>\dfrac1{a_1}+(n-1)=n+1$。$n=1$ では $\dfrac1{a_1}=2$。よって $\dfrac{1}{a_n}\geqq n+1$，すなわち $0<a_n\leqq\dfrac{1}{n+1}$　（終）<br>"
         r"(2) $\dfrac{1}{1-a_k}=1+\dfrac{a_k}{1-a_k}$ で、$1-a_k\geqq\dfrac12$ と (1) より $\dfrac{a_k}{1-a_k}\leqq2a_k\leqq\dfrac{2}{k+1}$。よって<br>"
         r"$\dfrac1{a_{k+1}}-\dfrac1{a_k}\leqq1+\dfrac{2}{k+1}$<br>"
         r"$k=1$ から $n-1$ まで加えると（$n\geqq2$）　$\dfrac1{a_n}\leqq2+(n-1)+2\displaystyle\sum_{j=2}^{n}\frac1j=n+1+2\sum_{j=2}^{n}\frac1j$<br>"
         r"ここで $j\geqq1$ のとき　$\dfrac1j\leqq\dfrac{1}{\sqrt j}=\dfrac{2}{\sqrt j+\sqrt j}<\dfrac{2}{\sqrt j+\sqrt{j-1}}=2(\sqrt j-\sqrt{j-1})$　であるから<br>"
         r"$\displaystyle\sum_{j=2}^{n}\frac1j<2\sum_{j=2}^{n}(\sqrt j-\sqrt{j-1})=2(\sqrt n-1)<2\sqrt n$<br>"
         r"(1) と合わせて　$n+1\leqq\dfrac1{a_n}<n+1+4\sqrt n$　（$n=1$ でも成り立つ）<br>"
         r"よって　$\dfrac{n}{n+1+4\sqrt n}<na_n\leqq\dfrac{n}{n+1}$<br>"
         r"$\dfrac{n}{n+1+4\sqrt n}=\dfrac{1}{1+\frac1n+\frac{4}{\sqrt n}}\to1$，$\dfrac{n}{n+1}\to1$ であるから、はさみうちの原理により　$\displaystyle\lim_{n\to\infty}na_n=\boldsymbol{1}$",
  "note": r"$a_n\fallingdotseq\dfrac1n$ という「収束の速さ」がわかった。上からの評価で $\sum\frac1j$ を $2\sqrt n$ という粗い値でおさえても、$n$ で割れば消えるので十分である。<b>逆数の差が一定値に近づく</b>ことに着目するのは、$a_{n+1}=a_n-a_n^2$ のように $0$ にゆっくり近づく数列の典型的な扱い方。",
  "ex": r"$a_1=1,\ a_{n+1}=\dfrac{a_n}{1+a_n^2}$ で定まる数列 $\{a_n\}$ について、$\displaystyle\lim_{n\to\infty}\sqrt n\,a_n$ を求めよ。",
  "exa": r"$\dfrac{\sqrt2}{2}$（$\frac{1}{a_{n+1}^2}=\frac{1}{a_n^2}+2+a_n^2$ から $2n-1\leqq\frac{1}{a_n^2}<2n-1+2\sqrt n$）"},
]})

# ---------------------------------------------------------------- 節5
SEC.append({"title": r"関数の極限",
"base": r"""・$\displaystyle\lim_{x\to a}f(x)=\alpha$：$x$ が $a$ と異なる値をとりながら $a$ に限りなく近づくとき、$f(x)$ が $\alpha$ に限りなく近づく。<br>
・右側極限 $\displaystyle\lim_{x\to a+0}f(x)$ と左側極限 $\displaystyle\lim_{x\to a-0}f(x)$ が一致するとき、またそのときに限り $\displaystyle\lim_{x\to a}f(x)$ が存在する。<br>
・不定形 $\dfrac00$：因数分解して約分する、または有理化する。$x\to-\infty$ は $x=-t$ とおき $t\to\infty$ に直す（$\sqrt{x^2}=|x|=-x$ に注意）。<br>
・$\displaystyle\lim_{x\to a}\frac{f(x)}{g(x)}$ が有限の値で $\displaystyle\lim_{x\to a}g(x)=0$ ならば　$\displaystyle\lim_{x\to a}f(x)=0$""",
"items": [
 {"lv": 1, "title": r"関数の極限（約分・有理化）",
  "q": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{x\to2}\frac{x^3-8}{x^2-3x+2}$　(2) $\displaystyle\lim_{x\to0}\frac{\sqrt{1+x}-\sqrt{1-x}}{x}$　(3) $\displaystyle\lim_{x\to\infty}\frac{2x^2-1}{x^2+3x}$",
  "hint": r"(1)(2) はそのまま代入すると $\dfrac00$。(1) は<b>分子・分母に共通な因数 $x-2$ で約分</b>、(2) は分子を有理化して $x$ を約分する。(3) は $x^2$ で分子・分母を割る。",
  "sol": r"(1) $\dfrac{x^3-8}{x^2-3x+2}=\dfrac{(x-2)(x^2+2x+4)}{(x-1)(x-2)}=\dfrac{x^2+2x+4}{x-1}\to\dfrac{4+4+4}{1}=\boldsymbol{12}$<br>"
         r"(2) $\dfrac{\sqrt{1+x}-\sqrt{1-x}}{x}=\dfrac{(1+x)-(1-x)}{x(\sqrt{1+x}+\sqrt{1-x})}=\dfrac{2}{\sqrt{1+x}+\sqrt{1-x}}\to\dfrac22=\boldsymbol{1}$<br>"
         r"(3) $\dfrac{2x^2-1}{x^2+3x}=\dfrac{2-\frac1{x^2}}{1+\frac3x}\to\boldsymbol{2}$",
  "note": r"$x\to2$ では $x\neq2$ なので、$x-2$ で約分してよい。約分した後の式は $x=2$ で値をもつ（連続）ので、代入して極限が求まる。",
  "ex": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{x\to-1}\frac{x^3+1}{x^2-1}$　(2) $\displaystyle\lim_{x\to3}\frac{\sqrt{x+1}-2}{x-3}$　(3) $\displaystyle\lim_{x\to\infty}\frac{3x-1}{\sqrt{x^2+1}}$",
  "exa": r"(1) $-\dfrac32$　(2) $\dfrac14$　(3) $3$"},
 {"lv": 2, "title": r"片側からの極限・$x\to-\infty$ の極限",
  "q": r"(1) $\displaystyle\lim_{x\to1+0}\frac{x^2-1}{|x-1|}$，$\displaystyle\lim_{x\to1-0}\frac{x^2-1}{|x-1|}$ を求め、$\displaystyle\lim_{x\to1}\frac{x^2-1}{|x-1|}$ が存在するかどうか調べよ。<br>(2) $\displaystyle\lim_{x\to-\infty}\left(\sqrt{x^2+3x}+x\right)$ を求めよ。",
  "hint": r"(1) 絶対値は $x>1$ と $x<1$ で外し方が変わるので、<b>右側と左側の極限を別々に</b>求める。(2) $x\to-\infty$ では $x=-t$ とおいて $t\to\infty$ の問題に直すと、符号の誤りを防げる。",
  "sol": r"(1) $x>1$ のとき $|x-1|=x-1$ より　$\dfrac{x^2-1}{|x-1|}=x+1\to2$　よって　$\displaystyle\lim_{x\to1+0}\frac{x^2-1}{|x-1|}=\boldsymbol{2}$<br>"
         r"$x<1$ のとき $|x-1|=-(x-1)$ より　$\dfrac{x^2-1}{|x-1|}=-(x+1)\to-2$　よって　$\displaystyle\lim_{x\to1-0}\frac{x^2-1}{|x-1|}=\boldsymbol{-2}$<br>"
         r"右側極限と左側極限が一致しないから、$\displaystyle\lim_{x\to1}\frac{x^2-1}{|x-1|}$ は<b>存在しない</b>。<br>"
         r"(2) $x=-t$ とおくと、$x\to-\infty$ のとき $t\to\infty$ で<br>"
         r"$\sqrt{x^2+3x}+x=\sqrt{t^2-3t}-t=\dfrac{(t^2-3t)-t^2}{\sqrt{t^2-3t}+t}=\dfrac{-3t}{\sqrt{t^2-3t}+t}=\dfrac{-3}{\sqrt{1-\frac3t}+1}\to\boldsymbol{-\dfrac32}$",
  "note": r"(2) を $x$ のまま計算するなら、$x<0$ で $\sqrt{x^2}=-x$ なので $\sqrt{x^2+3x}=-x\sqrt{1+\frac3x}$ となる。これを $x\sqrt{1+\frac3x}$ とすると誤った答え（$-\infty$）になる。",
  "ex": r"(1) $\displaystyle\lim_{x\to0}\frac{|x|}{x^2+x}$ が存在するかどうか調べよ。<br>(2) $\displaystyle\lim_{x\to-\infty}\left(\sqrt{x^2-2x+3}+x\right)$ を求めよ。",
  "exa": r"(1) 右側極限 $1$，左側極限 $-1$ で、存在しない　(2) $1$"},
 {"lv": 3, "title": r"極限値から係数を決定する（関数）",
  "q": r"$\displaystyle\lim_{x\to2}\frac{a\sqrt{x+2}+b}{x-2}=1$ が成り立つように、定数 $a,\ b$ の値を定めよ。",
  "hint": r"$x\to2$ で分母 $\to0$。それでも極限値が有限なのだから、<b>分子 $\to0$ でなければならない</b>（必要条件）。これで $b$ を $a$ で表し、有理化して極限を計算する。",
  "sol": r"$\displaystyle\lim_{x\to2}(x-2)=0$ であるから　$\displaystyle\lim_{x\to2}(a\sqrt{x+2}+b)=\lim_{x\to2}\frac{a\sqrt{x+2}+b}{x-2}\cdot(x-2)=1\cdot0=0$<br>"
         r"よって $2a+b=0$，すなわち $b=-2a$ が必要。このとき<br>"
         r"$\dfrac{a\sqrt{x+2}-2a}{x-2}=\dfrac{a\{(x+2)-4\}}{(x-2)(\sqrt{x+2}+2)}=\dfrac{a}{\sqrt{x+2}+2}\to\dfrac a4$<br>"
         r"$\dfrac a4=1$ より $a=4$，$b=-8$。このとき確かに極限値は $1$ である。<br>"
         r"よって　$\boldsymbol{a=4,\ b=-8}$",
  "note": r"「分母 $\to0$ かつ極限値が有限 ⇒ 分子 $\to0$」は必要条件にすぎないので、最後に極限値を実際に計算して条件を満たすことを確かめる（十分性）。分母 $\to0$ で分子 $\to0$ でないと、極限は $\pm\infty$ になるか存在しない。",
  "ex": r"$\displaystyle\lim_{x\to1}\frac{ax^2+bx+3}{x-1}=4$ が成り立つように、定数 $a,\ b$ の値を定めよ。",
  "exa": r"$a=7,\ b=-10$"},
]})

# ---------------------------------------------------------------- 節6
SEC.append({"title": r"三角関数・指数関数・対数関数の極限",
"base": r"""・$\displaystyle\lim_{x\to0}\frac{\sin x}{x}=1$（$x$ は弧度法）。これから　$\displaystyle\lim_{x\to0}\frac{\tan x}{x}=1$，$\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^2}=\frac12$<br>
・$\displaystyle e=\lim_{n\to\infty}\left(1+\frac1n\right)^n=\lim_{x\to\pm\infty}\left(1+\frac1x\right)^x=\lim_{h\to0}(1+h)^{\frac1h}$　（$e=2.71828\cdots$）<br>
・$\displaystyle\lim_{x\to0}\frac{\log(1+x)}{x}=1$，$\displaystyle\lim_{x\to0}\frac{e^x-1}{x}=1$（$\log$ は自然対数）<br>
・置き換え：$x\to a$ の極限は $t=x-a$ とおいて $t\to0$ に、$x\to\infty$ は $t=\frac1x$ とおいて $t\to+0$ に直せる。""",
"items": [
 {"lv": 1, "title": r"$\frac{\sin x}{x}\to1$ を用いる極限",
  "q": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{x\to0}\frac{\sin3x}{\sin5x}$　(2) $\displaystyle\lim_{x\to0}\frac{1-\cos x}{x^2}$　(3) $\displaystyle\lim_{x\to\pi}\frac{\sin x}{x-\pi}$",
  "hint": r"<b>$\dfrac{\sin\bigcirc}{\bigcirc}$ の形</b>（$\bigcirc\to0$）をつくる。(2) は分子・分母に $1+\cos x$ を掛けて $\sin^2x$ を出す。(3) は $x\to\pi$ なので $t=x-\pi$ とおいて $t\to0$ の形に直す。",
  "sol": r"(1) $\dfrac{\sin3x}{\sin5x}=\dfrac{\sin3x}{3x}\cdot\dfrac{5x}{\sin5x}\cdot\dfrac35\to1\cdot1\cdot\dfrac35=\boldsymbol{\dfrac35}$<br>"
         r"(2) $\dfrac{1-\cos x}{x^2}=\dfrac{1-\cos^2x}{x^2(1+\cos x)}=\left(\dfrac{\sin x}{x}\right)^2\cdot\dfrac{1}{1+\cos x}\to1\cdot\dfrac12=\boldsymbol{\dfrac12}$<br>"
         r"(3) $t=x-\pi$ とおくと $x\to\pi$ のとき $t\to0$。$\sin x=\sin(t+\pi)=-\sin t$ より<br>"
         r"$\dfrac{\sin x}{x-\pi}=\dfrac{-\sin t}{t}\to\boldsymbol{-1}$",
  "note": r"$\dfrac{\sin x}{x}\to1$ は $x$ が<b>弧度法</b>のときに限る。(1) で「$\sin3x\to3x$ に置き換える」ような書き方は答案では避け、必ず $\dfrac{\sin3x}{3x}$ の形をつくって示す。",
  "ex": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{x\to0}\frac{\tan2x}{x}$　(2) $\displaystyle\lim_{x\to0}\frac{1-\cos2x}{x\sin x}$　(3) $\displaystyle\lim_{x\to\infty}x\sin\frac1x$",
  "exa": r"(1) $2$　(2) $2$　(3) $1$"},
 {"lv": 2, "title": r"$e$ の定義を用いる極限",
  "q": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{n\to\infty}\left(1+\frac{2}{n}\right)^n$　(2) $\displaystyle\lim_{x\to0}(1-3x)^{\frac1x}$　(3) $\displaystyle\lim_{n\to\infty}\left(\frac{n}{n+1}\right)^{n}$",
  "hint": r"$1^\infty$ の形の不定形。<b>$(1+h)^{\frac1h}$（$h\to0$）や $\left(1+\frac1x\right)^x$（$x\to\infty$）の形をつくり</b>、外側に残った指数をあとで処理する。",
  "sol": r"(1) $\left(1+\dfrac2n\right)^n=\left\{\left(1+\dfrac{1}{\frac n2}\right)^{\frac n2}\right\}^2$ で、$\dfrac n2\to\infty$ より　$\to e^2$。よって　$\boldsymbol{e^2}$<br>"
         r"(2) $h=-3x$ とおくと $x\to0$ のとき $h\to0$ で、$\dfrac1x=-\dfrac3h$ より<br>"
         r"$(1-3x)^{\frac1x}=(1+h)^{-\frac3h}=\left\{(1+h)^{\frac1h}\right\}^{-3}\to e^{-3}$。よって　$\boldsymbol{\dfrac{1}{e^3}}$<br>"
         r"(3) $\left(\dfrac{n}{n+1}\right)^n=\dfrac{1}{\left(1+\frac1n\right)^n}\to\boldsymbol{\dfrac1e}$",
  "note": r"「$1+\frac2n\to1$ だから $1^n=1$」は誤り。底が $1$ に近づく速さと指数が大きくなる速さの兼ね合いで値が決まる。一般に $\displaystyle\lim_{x\to\infty}\left(1+\frac ax\right)^x=e^a$。",
  "ex": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{n\to\infty}\left(1-\frac1{2n}\right)^{n}$　(2) $\displaystyle\lim_{x\to0}(1+2x)^{\frac3x}$　(3) $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^{2n+1}$",
  "exa": r"(1) $\dfrac{1}{\sqrt e}$　(2) $e^6$　(3) $e^2$"},
 {"lv": 3, "title": r"指数関数・対数関数の極限",
  "q": r"(1) $\displaystyle\lim_{x\to0}\frac{\log(1+x)}{x}=1$，$\displaystyle\lim_{x\to0}\frac{e^x-1}{x}=1$ を示せ。<br>次の極限を求めよ。<br>(2) $\displaystyle\lim_{x\to0}\frac{e^{3x}-e^{x}}{\log(1+2x)}$　(3) $\displaystyle\lim_{x\to0}\frac{2^x-1}{x}$",
  "hint": r"(1) $\dfrac{\log(1+x)}{x}=\log(1+x)^{\frac1x}$ と $e$ の定義を結びつける。$\dfrac{e^x-1}{x}$ は $t=e^x-1$ とおいて前半に帰着。<br>(2)(3) は分子・分母を $x$ で割り、<b>(1) の2つの基本形をつくる</b>。$2^x=e^{x\log2}$ と底を $e$ に直す。",
  "sol": r"(1) $\dfrac{\log(1+x)}{x}=\log(1+x)^{\frac1x}$ で、$(1+x)^{\frac1x}\to e$ であり $\log$ は連続であるから　$\to\log e=1$<br>"
         r"次に $t=e^x-1$ とおくと $x=\log(1+t)$ で、$x\to0$ のとき $t\to0$（$x\neq0$ なら $t\neq0$）。よって<br>"
         r"$\dfrac{e^x-1}{x}=\dfrac{t}{\log(1+t)}=\dfrac{1}{\frac{\log(1+t)}{t}}\to\dfrac11=1$　（終）<br>"
         r"(2) 分子・分母を $x$ で割ると　$\dfrac{\frac{e^{3x}-1}{x}-\frac{e^x-1}{x}}{\frac{\log(1+2x)}{x}}$<br>"
         r"$\dfrac{e^{3x}-1}{x}=3\cdot\dfrac{e^{3x}-1}{3x}\to3$，$\dfrac{e^x-1}{x}\to1$，$\dfrac{\log(1+2x)}{x}=2\cdot\dfrac{\log(1+2x)}{2x}\to2$<br>"
         r"よって　与式 $=\dfrac{3-1}{2}=\boldsymbol{1}$<br>"
         r"(3) $2^x=e^{x\log2}$ であり、$x\to0$ のとき $x\log2\to0$ であるから<br>"
         r"$\dfrac{2^x-1}{x}=\log2\cdot\dfrac{e^{x\log2}-1}{x\log2}\to\boldsymbol{\log2}$",
  "note": r"一般に $a>0$ のとき $\displaystyle\lim_{x\to0}\frac{a^x-1}{x}=\log a$。これらの極限は、第23章で $(e^x)'=e^x$，$(\log x)'=\dfrac1x$ を導く根拠になる。",
  "ex": r"次の極限を求めよ。<br>(1) $\displaystyle\lim_{x\to0}\frac{\log(1+3x)}{\sin x}$　(2) $\displaystyle\lim_{x\to0}\frac{3^x-2^x}{x}$　(3) $\displaystyle\lim_{x\to\infty}x\{\log(x+2)-\log x\}$",
  "exa": r"(1) $3$　(2) $\log\dfrac32$　(3) $2$"},
 {"lv": 3, "title": r"図形と三角関数の極限",
  "q": r"""中心 O，半径 $1$ の円周上に2点 A，P を $\angle\mathrm{AOP}=\theta$（$0<\theta<\frac{\pi}{2}$）となるようにとり、A における円の接線と直線 OP の交点を T とする。△APT の面積を $S(\theta)$ とするとき、$\displaystyle\lim_{\theta\to+0}\frac{S(\theta)}{\theta^3}$ を求めよ。<svg class="fig" width="170" height="168" viewBox="0 0 170 168"><polyline points="140.0,150.0 139.7,141.8 138.9,133.6 137.4,125.5 135.4,117.5 132.9,109.6 129.8,102.0 126.2,94.6 122.1,87.5 117.5,80.6 112.4,74.2 106.9,68.0 101.0,62.3 94.6,57.0 88.0,52.2 81.0,47.8 73.7,43.9 66.2,40.6 58.5,37.8 50.5,35.5 42.5,33.8" fill="none" stroke="#1f3f8f" stroke-width="1.1"/><polygon points="140.0,150.0 115.0,77.4 140.0,57.8" fill="#f6dede" stroke="#c0392b" stroke-width="1"/><line x1="22.0" y1="150.0" x2="140.0" y2="150.0" stroke="#333" stroke-width="1"/><line x1="22.0" y1="150.0" x2="140.0" y2="57.8" stroke="#333" stroke-width="1"/><line x1="140.0" y1="154.7" x2="140.0" y2="17.8" stroke="#777" stroke-width="0.9"/><polyline points="44.0,150.0 44.0,148.5 43.8,147.1 43.6,145.7 43.2,144.2 42.8,142.8 42.3,141.5 41.7,140.1 41.0,138.9 40.2,137.6 39.3,136.5" fill="none" stroke="#333" stroke-width="0.8"/><text x="45.8" y="146.8" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">θ</text><text x="12.0" y="162.0" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">O</text><text x="144.0" y="162.0" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">A</text><text x="107.5" y="66.5" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">P</text><text x="145.0" y="61.8" font-family="Liberation Serif,DejaVu Serif,serif" font-size="11" font-style="italic">T</text><circle cx="22.0" cy="150.0" r="1.6" fill="#000"/><circle cx="140.0" cy="150.0" r="1.6" fill="#000"/><circle cx="115.0" cy="77.4" r="1.6" fill="#000"/><circle cx="140.0" cy="57.8" r="1.6" fill="#000"/></svg>""",
  "hint": r"△APT＝△OAT－△OAP と見ると、面積は $\tan\theta$，$\sin\theta$ で表せる。$\tan\theta-\sin\theta=\tan\theta(1-\cos\theta)$ と<b>積の形に変形して</b>、$\dfrac{\tan\theta}{\theta}$ と $\dfrac{1-\cos\theta}{\theta^2}$ をつくる。",
  "sol": r"$\mathrm{OA}=1$，$\mathrm{AT}=\tan\theta$ で、P から OA までの距離は $\sin\theta$ であるから<br>"
         r"$S(\theta)=\triangle\mathrm{OAT}-\triangle\mathrm{OAP}=\dfrac12\tan\theta-\dfrac12\sin\theta=\dfrac12\tan\theta(1-\cos\theta)$<br>"
         r"よって　$\dfrac{S(\theta)}{\theta^3}=\dfrac12\cdot\dfrac{\tan\theta}{\theta}\cdot\dfrac{1-\cos\theta}{\theta^2}\to\dfrac12\cdot1\cdot\dfrac12=\boldsymbol{\dfrac14}$",
  "note": r"$\tan\theta-\sin\theta$ を $\dfrac{\tan\theta}{\theta}-\dfrac{\sin\theta}{\theta}\to1-1=0$ と分けると、$\theta^3$ で割った極限は分からない。差の形は<b>積の形に直して</b>から基本の極限を使う。結果から、$\theta$ が小さいとき $S(\theta)\fallingdotseq\dfrac{\theta^3}{4}$。",
  "ex": r"半径 $1$ の円に内接する正 $n$ 角形、外接する正 $n$ 角形の面積をそれぞれ $S_n,\ T_n$ とするとき、$\displaystyle\lim_{n\to\infty}n^2(T_n-S_n)$ を求めよ。",
  "exa": r"$\pi^3$（$T_n-S_n=n\tan\frac{\pi}{n}\sin^2\frac{\pi}{n}$）"},
 {"lv": 4, "title": r"漸化式と三角関数の極限（$2\cos\theta$ の置き換え）",
  "q": r"$a_1=0,\ a_{n+1}=\sqrt{2+a_n}$ で定まる数列 $\{a_n\}$ について、次の問いに答えよ。<br>(1) $a_n$ を $n$ の式で表せ。<br>(2) $\displaystyle\lim_{n\to\infty}4^n(2-a_n)$ を求めよ。",
  "hint": r"(1) 半角の公式から $0\leqq\theta\leqq\pi$ で $\sqrt{2+2\cos\theta}=2\cos\dfrac\theta2$。$a_1=0=2\cos\dfrac\pi2$ なので、<b>$a_n=2\cos\theta_n$ の形</b>を予想して帰納法で示す。<br>(2) $2-a_n$ を $\sin^2$ で表し、$\dfrac{\sin t}{t}$ の形をつくる。",
  "sol": r"(1) $0\leqq\theta\leqq\pi$ のとき、$2+2\cos\theta=4\cos^2\dfrac\theta2$ かつ $\cos\dfrac\theta2\geqq0$ であるから　$\sqrt{2+2\cos\theta}=2\cos\dfrac\theta2$<br>"
         r"$a_n=2\cos\dfrac{\pi}{2^n}$ …① を帰納法で示す。$a_1=0=2\cos\dfrac\pi2$ より $n=1$ で成り立つ。$n=k$ で成り立つとすると、$0<\dfrac{\pi}{2^k}\leqq\dfrac\pi2$ より<br>"
         r"$a_{k+1}=\sqrt{2+2\cos\dfrac{\pi}{2^k}}=2\cos\dfrac{\pi}{2^{k+1}}$　となり、$n=k+1$ でも成り立つ。よって　$\boldsymbol{a_n=2\cos\dfrac{\pi}{2^n}}$<br>"
         r"(2) $2-a_n=2\left(1-\cos\dfrac{\pi}{2^n}\right)=4\sin^2\dfrac{\pi}{2^{n+1}}$<br>"
         r"$t_n=\dfrac{\pi}{2^{n+1}}$ とおくと $t_n\to0$ で、$4^n=\dfrac{4^{n+1}}{4}=\dfrac{\pi^2}{4t_n^2}$ であるから<br>"
         r"$4^n(2-a_n)=\dfrac{\pi^2}{4t_n^2}\cdot4\sin^2t_n=\pi^2\left(\dfrac{\sin t_n}{t_n}\right)^2\to\boldsymbol{\pi^2}$",
  "note": r"(1) から $a_n\to2$ はすぐ分かるが、(2) は「$2$ にどれくらいの速さで近づくか」を表し、$2-a_n\fallingdotseq\dfrac{\pi^2}{4^n}$ となる。$\sqrt{2+x}$ の形の漸化式は $2\cos\theta$ で、$\sqrt{2-x}$ や $x^2-2$ の形も $2\cos\theta$ や $2\sin\theta$ の置き換えでうまくいくことが多い。",
  "ex": r"$a_1=1,\ a_{n+1}=\sqrt{2+a_n}$ で定まる数列 $\{a_n\}$ について、$\displaystyle\lim_{n\to\infty}4^n(2-a_n)$ を求めよ。",
  "exa": r"$\dfrac{4\pi^2}{9}$（$a_n=2\cos\frac{\pi}{3\cdot2^{n-1}}$）"},
 {"lv": 5, "title": r"三角関数を含む無限級数（倍角の公式で差の形をつくる）",
  "q": r"$\theta$ を実数の定数とする。無限級数 $\displaystyle\sum_{n=1}^{\infty}4^n\sin^4\frac{\theta}{2^n}$ の和を求めよ。",
  "hint": r"このままでは部分和が求まらない。2倍角の公式 $\sin^22x=4\sin^2x\cos^2x=4\sin^2x-4\sin^4x$ から $4\sin^4x=4\sin^2x-\sin^22x$。$x=\dfrac{\theta}{2^n}$ とすると、<b>一般項が「隣り合う項の差」</b>の形になる。",
  "sol": r"$\sin^22x=4\sin^2x(1-\sin^2x)=4\sin^2x-4\sin^4x$ より　$4\sin^4x=4\sin^2x-\sin^22x$<br>"
         r"$x=\dfrac{\theta}{2^n}$ とし、両辺に $4^{n-1}$ を掛けると<br>"
         r"$4^n\sin^4\dfrac{\theta}{2^n}=4^n\sin^2\dfrac{\theta}{2^n}-4^{n-1}\sin^2\dfrac{\theta}{2^{n-1}}$<br>"
         r"$b_n=4^n\sin^2\dfrac{\theta}{2^n}$（$n\geqq0$）とおくと、一般項は $b_n-b_{n-1}$ であるから、部分和は<br>"
         r"$S_N=\displaystyle\sum_{n=1}^{N}(b_n-b_{n-1})=b_N-b_0=4^N\sin^2\frac{\theta}{2^N}-\sin^2\theta$<br>"
         r"$\theta\neq0$ のとき　$4^N\sin^2\dfrac{\theta}{2^N}=\theta^2\left(\dfrac{\sin\frac{\theta}{2^N}}{\frac{\theta}{2^N}}\right)^2\to\theta^2$（$\frac{\theta}{2^N}\to0$）<br>"
         r"$\theta=0$ のときは $b_N=0=\theta^2$。いずれの場合も $S_N\to\theta^2-\sin^2\theta$<br>"
         r"よって　$\displaystyle\sum_{n=1}^{\infty}4^n\sin^4\frac{\theta}{2^n}=\boldsymbol{\theta^2-\sin^2\theta}$",
  "note": r"部分和が $b_N-b_0$ の形になれば、$b_N$ の極限だけで和が決まる。倍角・半角の公式は、三角関数の級数や積（$\cos\frac\theta2\cos\frac\theta4\cdots\cos\frac{\theta}{2^n}$ など）で「差の形」「比の形」をつくる代表的な道具である。各項が $0$ 以上であることから、副産物として $\sin^2\theta\leqq\theta^2$，すなわち $|\sin\theta|\leqq|\theta|$ も得られる。",
  "ex": r"$\theta$ を実数の定数とする。無限級数 $\displaystyle\sum_{n=1}^{\infty}3^{n-1}\sin^3\frac{\theta}{3^n}$ の和を求めよ。",
  "exa": r"$\dfrac{\theta-\sin\theta}{4}$（3倍角の公式より $4\sin^3x=3\sin x-\sin3x$）"},
]})

# ---------------------------------------------------------------- 節7
SEC.append({"title": r"関数の連続性と中間値の定理",
"base": r"""・$f(x)$ が $x=a$ で連続 ⇔ $\displaystyle\lim_{x\to a}f(x)=f(a)$（右側極限・左側極限がともに存在して $f(a)$ に等しい）<br>
・連続関数の和・差・積・商（分母 $\neq0$）・合成関数は連続。整式・分数関数・無理関数・三角関数・指数関数・対数関数は、定義域で連続。<br>
・<b>中間値の定理</b>：$f(x)$ が閉区間 $[a,\ b]$ で連続で $f(a)\neq f(b)$ ならば、$f(a)$ と $f(b)$ の間の任意の値 $k$ に対して $f(c)=k$ となる $c$ が $a<c<b$ に少なくとも1つある。<br>
　特に $f(a)$ と $f(b)$ が異符号ならば、方程式 $f(x)=0$ は $a<x<b$ に少なくとも1つの実数解をもつ。""",
"items": [
 {"lv": 1, "title": r"関数の連続性の判定",
  "q": r"(1) $x\neq1$ のとき $f(x)=\dfrac{x^2+x-2}{x-1}$，$f(1)=a$ で定まる関数 $f(x)$ が $x=1$ で連続となるように、定数 $a$ の値を定めよ。<br>(2) 関数 $g(x)=x[x]$，$h(x)=(x-1)[x]$ は、それぞれ $x=1$ で連続かどうか調べよ。ただし $[x]$ は $x$ を超えない最大の整数を表す。",
  "hint": r"$x=a$ で連続 ⇔ $\displaystyle\lim_{x\to a}f(x)=f(a)$。(2) は $[x]$ が $x=1$ の右と左で値が変わる（$1\leqq x<2$ で $1$，$0\leqq x<1$ で $0$）ので、<b>右側極限と左側極限を別々に</b>調べる。",
  "sol": r"(1) $x\neq1$ のとき　$f(x)=\dfrac{(x+2)(x-1)}{x-1}=x+2$　より　$\displaystyle\lim_{x\to1}f(x)=3$<br>"
         r"$x=1$ で連続となる条件は $\displaystyle\lim_{x\to1}f(x)=f(1)$ であるから　$\boldsymbol{a=3}$<br>"
         r"(2) $1\leqq x<2$ で $[x]=1$，$0\leqq x<1$ で $[x]=0$ である。<br>"
         r"$\displaystyle\lim_{x\to1+0}g(x)=\lim_{x\to1+0}x=1$，$\displaystyle\lim_{x\to1-0}g(x)=\lim_{x\to1-0}0=0$　で一致しないから、<b>$g(x)$ は $x=1$ で連続でない</b>。<br>"
         r"$\displaystyle\lim_{x\to1+0}h(x)=\lim_{x\to1+0}(x-1)=0$，$\displaystyle\lim_{x\to1-0}h(x)=0$，$h(1)=0\cdot1=0$　であるから、<b>$h(x)$ は $x=1$ で連続である</b>。",
  "note": r"$[x]$ は整数値で不連続だが、その点で $0$ になる因数 $(x-1)$ を掛けると、とびが打ち消されて連続になる。連続かどうかは「グラフがつながっているか」をイメージすると判断しやすい。",
  "ex": r"(1) $x\neq1$ のとき $f(x)=\dfrac{\sqrt{x+3}-2}{x-1}$，$f(1)=a$ で定まる関数 $f(x)$ が $x=1$ で連続となるような $a$ の値を求めよ。<br>(2) 関数 $g(x)=x-[x]$ は $x=2$ で連続かどうか調べよ。",
  "exa": r"(1) $a=\dfrac14$　(2) 連続でない（右側極限 $0$，左側極限 $1$）"},
 {"lv": 2, "title": r"中間値の定理による実数解の存在",
  "q": r"(1) 方程式 $\cos x=x$ は、$0<x<\dfrac{\pi}{2}$ の範囲に少なくとも1つの実数解をもつことを示せ。<br>(2) 方程式 $x^3-3x+1=0$ は、異なる3つの実数解をもつことを示せ。",
  "hint": r"$f(x)=0$ の形にし、<b>区間の両端で $f(x)$ が異符号</b>になることを確かめて中間値の定理を使う。(2) は符号が変わる区間を3つ見つける（解が入る区間が重ならなければ解は異なる）。",
  "sol": r"(1) $f(x)=\cos x-x$ とおくと、$f(x)$ は閉区間 $\left[0,\ \dfrac\pi2\right]$ で連続で<br>"
         r"$f(0)=1>0$，$f\left(\dfrac\pi2\right)=-\dfrac\pi2<0$<br>"
         r"よって中間値の定理により、$f(c)=0$ となる $c$ が $0<c<\dfrac\pi2$ に存在する。すなわち、方程式は $0<x<\dfrac\pi2$ に少なくとも1つの実数解をもつ。（終）<br>"
         r"(2) $f(x)=x^3-3x+1$ は連続で　$f(-2)=-1<0$，$f(0)=1>0$，$f(1)=-1<0$，$f(2)=3>0$<br>"
         r"中間値の定理により、$-2<x<0$，$0<x<1$，$1<x<2$ の各区間に $f(x)=0$ の解が少なくとも1つずつある。これらの区間は共通部分をもたないから、方程式は異なる3つの実数解をもつ。（終）",
  "note": r"中間値の定理は解の<b>存在</b>を保証するだけで、個数や値は教えてくれない。(2) では3次方程式の実数解は高々3個なので、ちょうど3個とわかる。また<b>閉区間で連続</b>という仮定は必要：$f(x)=\dfrac1x$ は $f(-1)<0<f(1)$ だが、$f(x)=0$ の解はない。",
  "ex": r"(1) 方程式 $e^x+x=0$ は $-1<x<0$ の範囲に少なくとも1つの実数解をもつことを示せ。<br>(2) 方程式 $x^4-4x^2+x+1=0$ は異なる4つの実数解をもつことを示せ。",
  "exa": r"(1) $f(x)=e^x+x$ は連続で $f(-1)=\frac1e-1<0$，$f(0)=1>0$　(2) $f(x)=x^4-4x^2+x+1$ で $f(-3)>0,\ f(-1)<0,\ f(0)>0,\ f(1)<0,\ f(2)>0$ より、4つの区間に1つずつ解がある"},
 {"lv": 3, "title": r"極限で定義された関数の連続性",
  "q": r"関数 $f(x)=\displaystyle\lim_{n\to\infty}\frac{x^{2n+1}-x^2+ax+b}{x^{2n}+1}$ が、すべての実数 $x$ で連続となるように、定数 $a,\ b$ の値を定めよ。",
  "hint": r"$x^{2n}$ の極限は $|x|<1$ で $0$，$|x|>1$ で $\infty$，$x=\pm1$ で $1$。<b>$|x|<1$，$|x|>1$，$x=1$，$x=-1$ に分けて $f(x)$ を求め</b>、つなぎ目 $x=\pm1$ での連続の条件を調べる。",
  "sol": r"[1] $|x|<1$ のとき　$x^{2n}\to0$，$x^{2n+1}\to0$ より　$f(x)=-x^2+ax+b$<br>"
         r"[2] $|x|>1$ のとき　分子・分母を $x^{2n}$ で割ると、$\left(\dfrac1{x^2}\right)^n\to0$ より<br>"
         r"$f(x)=\displaystyle\lim_{n\to\infty}\frac{x+(-x^2+ax+b)\left(\frac{1}{x^2}\right)^n}{1+\left(\frac{1}{x^2}\right)^n}=x$<br>"
         r"[3] $x=1$ のとき　$f(1)=\dfrac{1-1+a+b}{2}=\dfrac{a+b}{2}$　　[4] $x=-1$ のとき　$f(-1)=\dfrac{-1-1-a+b}{2}=\dfrac{b-a-2}{2}$<br>"
         r"$|x|<1$，$|x|>1$ では $f(x)$ は整式で表されるので連続。よって $x=\pm1$ で連続となる条件を求めればよい。<br>"
         r"$x=1$：$\displaystyle\lim_{x\to1-0}f(x)=-1+a+b$，$\displaystyle\lim_{x\to1+0}f(x)=1$ で、$-1+a+b=1=\dfrac{a+b}{2}$ より　$a+b=2$<br>"
         r"$x=-1$：$\displaystyle\lim_{x\to-1+0}f(x)=-1-a+b$，$\displaystyle\lim_{x\to-1-0}f(x)=-1$ で、$-1-a+b=-1=\dfrac{b-a-2}{2}$ より　$b-a=0$<br>"
         r"よって　$\boldsymbol{a=1,\ b=1}$",
  "note": r"各 $n$ に対する関数 $\dfrac{x^{2n+1}-x^2+ax+b}{x^{2n}+1}$ はすべて連続でも、その極限の関数は一般には連続とは限らない。$x=\pm1$ では $x^{2n}=1$ となるので、必ず別に代入して値を求める。",
  "ex": r"関数 $f(x)=\displaystyle\lim_{n\to\infty}\frac{x^{2n+2}+ax+b}{x^{2n}+1}$ が、すべての実数 $x$ で連続となるように、定数 $a,\ b$ の値を定めよ。",
  "exa": r"$a=0,\ b=1$"},
 {"lv": 4, "title": r"中間値の定理の応用（$f(c)=f(c+1)$ となる $c$ の存在）",
  "q": r"関数 $f(x)$ は $0\leqq x\leqq2$ で連続で、$f(0)=f(2)$ を満たす。このとき、$f(c)=f(c+1)$ となる $c$ が $0\leqq c\leqq1$ の範囲に存在することを示せ。",
  "hint": r"$g(x)=f(x+1)-f(x)$（$0\leqq x\leqq1$）とおき、$g(c)=0$ となる $c$ を探す。$g(0)$ と $g(1)$ を<b>足すと $f(1)$ が消えて $0$</b> になるので、$g(0)$ と $g(1)$ は異符号か、ともに $0$。",
  "sol": r"$g(x)=f(x+1)-f(x)$（$0\leqq x\leqq1$）とおくと、$g(x)$ は $0\leqq x\leqq1$ で連続である。<br>"
         r"$g(0)+g(1)=\{f(1)-f(0)\}+\{f(2)-f(1)\}=f(2)-f(0)=0$　より　$g(1)=-g(0)$<br>"
         r"[1] $g(0)=0$ のとき　$c=0$ とすればよい。<br>"
         r"[2] $g(0)\neq0$ のとき　$g(0)g(1)=-g(0)^2<0$ より $g(0)$ と $g(1)$ は異符号であるから、中間値の定理により $g(c)=0$ となる $c$ が $0<c<1$ に存在する。<br>"
         r"いずれの場合も $f(c+1)=f(c)$ となる $c$ が $0\leqq c\leqq1$ に存在する。（終）",
  "note": r"グラフでいえば「両端の高さが等しい連続なグラフには、長さ $1$（区間の長さの半分）の水平な弦が必ずある」という主張。同様に、区間の長さの $\frac1n$ の水平な弦は必ず存在する（練習）。一方、区間の長さの $\frac25$ のように $\frac1n$ の形でない長さでは、成り立たない例がある。",
  "ex": r"関数 $f(x)$ は $0\leqq x\leqq1$ で連続で、$f(0)=f(1)$ を満たす。このとき、$f(c)=f\left(c+\dfrac13\right)$ となる $c$ が $0\leqq c\leqq\dfrac23$ の範囲に存在することを示せ。",
  "exa": r"$g(x)=f\left(x+\frac13\right)-f(x)$ とおくと $g(0)+g\left(\frac13\right)+g\left(\frac23\right)=f(1)-f(0)=0$。3つの値の中に $0$ があればよく、なければ正のものと負のものがあるので、その間で中間値の定理を使う"},
 {"lv": 5, "title": r"方程式の解で定まる数列の極限",
  "q": r"2以上の整数 $n$ に対して、方程式 $x^n+x^{n-1}+\cdots+x=1$ を考える。<br>(1) この方程式はただ1つの正の解をもつことを示せ。その解を $x_n$ とするとき、$\dfrac12<x_n<\dfrac23$ であることを示せ。<br>(2) $\displaystyle\lim_{n\to\infty}x_n$ を求めよ。<br>(3) $\displaystyle\lim_{n\to\infty}2^n(2x_n-1)$ を求めよ。",
  "hint": r"(1) 左辺は $x\geqq0$ で増加する連続関数なので、中間値の定理と単調性を使う。(2) $x_n\neq1$ なので等比数列の和の公式が使え、<b>$2x_n-1=x_n^{n+1}$</b> という簡単な関係が出る。(3) $2^n(2x_n-1)=\frac12(2x_n)^{n+1}$ で、$2x_n=1+x_n^{n+1}$。<b>$(1+\varepsilon)^m$ が $1$ に近づくには $m\varepsilon\to0$ が効く</b>ので、$(n+1)x_n^{n+1}\to0$ を示して評価する。",
  "sol": r"(1) $f(x)=x+x^2+\cdots+x^n$ とおく。$f(x)$ は連続で、$x\geqq0$ で各項 $x^k$ が増加するから $f(x)$ も増加する。<br>"
         r"$f(0)=0<1$，$f(1)=n>1$ であるから、中間値の定理により $f(x)=1$ の解が $0<x<1$ にあり、増加することから正の解はただ1つである。<br>"
         r"また、$f\left(\dfrac12\right)=1-\left(\dfrac12\right)^n<1$，$f\left(\dfrac23\right)=\dfrac{\frac23\left\{1-\left(\frac23\right)^n\right\}}{1-\frac23}=2\left\{1-\left(\dfrac23\right)^n\right\}\geqq2\left(1-\dfrac49\right)=\dfrac{10}{9}>1$<br>"
         r"$f(x)$ は増加するから　$\dfrac12<x_n<\dfrac23$　（終）<br>"
         r"(2) $0<x_n<1$ より　$f(x_n)=\dfrac{x_n(1-x_n^n)}{1-x_n}=1$　よって $x_n-x_n^{n+1}=1-x_n$，すなわち<br>"
         r"$2x_n-1=x_n^{n+1}$　…①<br>"
         r"(1) より $0<x_n^{n+1}<\left(\dfrac23\right)^{n+1}\to0$ であるから $2x_n-1\to0$。よって　$\displaystyle\lim_{n\to\infty}x_n=\boldsymbol{\dfrac12}$<br>"
         r"(3) $\varepsilon_n=x_n^{n+1}$ とおくと、①より $2x_n=1+\varepsilon_n$ で　$2^n(2x_n-1)=2^nx_n^{n+1}=\dfrac12(2x_n)^{n+1}=\dfrac12(1+\varepsilon_n)^{n+1}$<br>"
         r"まず $(n+1)\varepsilon_n\to0$ を示す。$m\geqq2$ のとき二項定理より $\left(\dfrac32\right)^m=\left(1+\dfrac12\right)^m\geqq\dfrac{m(m-1)}{2}\cdot\dfrac14$ であるから<br>"
         r"$0<(n+1)\varepsilon_n<(n+1)\left(\dfrac23\right)^{n+1}\leqq\dfrac{8}{n}\to0$<br>"
         r"次に、$0<\varepsilon<1$，$m\varepsilon<1$ のとき　$1<(1+\varepsilon)^m<\dfrac{1}{1-m\varepsilon}$ …② を示す。<br>"
         r"$(1+\varepsilon)(1-\varepsilon)=1-\varepsilon^2<1$ より $1+\varepsilon<\dfrac{1}{1-\varepsilon}$，よって $(1+\varepsilon)^m<\dfrac{1}{(1-\varepsilon)^m}$。<br>"
         r"また $(1-\varepsilon)^m\geqq1-m\varepsilon$ が帰納法で示せる（$(1-\varepsilon)^{k+1}\geqq(1-k\varepsilon)(1-\varepsilon)=1-(k+1)\varepsilon+k\varepsilon^2\geqq1-(k+1)\varepsilon$）。これらから②が成り立つ。<br>"
         r"$(n+1)\varepsilon_n\to0$ より、十分大きい $n$ で $(n+1)\varepsilon_n<1$ となり、②から<br>"
         r"$1<(1+\varepsilon_n)^{n+1}<\dfrac{1}{1-(n+1)\varepsilon_n}\to1$<br>"
         r"よって $(1+\varepsilon_n)^{n+1}\to1$ で　$\displaystyle\lim_{n\to\infty}2^n(2x_n-1)=\boldsymbol{\dfrac12}$",
  "note": r"(3) の結果は $x_n\fallingdotseq\dfrac12+\dfrac{1}{2^{n+2}}$ を意味し、$x_n$ が $\frac12$ に非常に速く近づくことがわかる。「$1+\varepsilon_n\to1$ だから $(1+\varepsilon_n)^{n+1}\to1$」とするのは誤り（$1^\infty$ の不定形。$\left(1+\frac1n\right)^{n+1}\to e$ が反例）。$m\varepsilon\to0$ を確かめて②のように評価するのが確実である。",
  "ex": r"3以上の整数 $n$ に対して、方程式 $x^n+x^{n-1}+\cdots+x=2$ のただ1つの正の解を $y_n$ とする。$\displaystyle\lim_{n\to\infty}y_n$ と $\displaystyle\lim_{n\to\infty}\left(\frac32\right)^n(3y_n-2)$ を求めよ。",
  "exa": r"$\displaystyle\lim y_n=\frac23$，$\displaystyle\lim\left(\frac32\right)^n(3y_n-2)=\frac23$（$3y_n-2=y_n^{n+1}$ を利用）"},
]})

CH = {"no": 22, "sections": SEC}


def verify():
    n = symbols("n", positive=True, integer=True)
    x = symbols("x", real=True)

    def L(e, v, var=None, pt=oo, d="+"):
        var = n if var is None else var
        r = limit(e, var, pt, d) if pt not in (oo, -oo) else limit(e, var, pt)
        assert simplify(r - v) == 0 if v not in (oo, -oo) else r == v, (e, r, v)

    def num(f, v, big=10**6, tol=1e-4):
        assert abs(f(big) - v) < tol, (f(big), v)

    # ---- 節1
    L((3*n**2-2*n+5)/(2*n**2+n-1), Rational(3, 2)); L((n**3+1)/(4*n**2-n), oo); L(sqrt(n**2+4*n)-n, 2)
    num(lambda m: 4/(math.sqrt(1+4/m)+1), 2)
    L((2*n-1)*(n+3)/(3*n**2+2), Rational(2, 3)); L((1-n**2)/(2*n+1), -oo); L(sqrt(n**2+n)-sqrt(n**2-n), 1)
    L(cbrt(n**3+2*n**2)-n, Rational(2, 3)); L((n**3-3*n**2+1)**Rational(1, 3)-n, -1)
    num(lambda m: (m**3+2*m**2)**(1/3)-m, 2/3, big=10**4)
    k = symbols("k", positive=True, integer=True)
    s1, s2, s3 = summation(k, (k, 1, n)), summation(k**2, (k, 1, n)), summation(k**3, (k, 1, n))
    L(s2/(n*s1), Rational(2, 3)); assert simplify(s2/(n*s1) - (2*n+1)/(3*n)) == 0
    assert simplify(s1 - s1.subs(n, n-1) - n) == 0
    L(sqrt(s1)-sqrt(s1.subs(n, n-1)), sqrt(2)/2)
    L(s3/(n*s2), Rational(3, 4)); L(sqrt(summation(2*k, (k, 1, n)))-n, Rational(1, 2))
    L(sqrt(9*n**2+12*n+1)-3*n, 2); L(sqrt(4*n**2+6*n)-2*n, Rational(3, 2))
    for a in (1, 4, 8, 10, 16):          # a≠9 なら発散
        assert limit(sqrt(a*n**2+12*n+1)-3*n, n, oo) in (oo, -oo)

    # ---- 節2
    L((4**(n+1)-3**n)/(4**n+2**n), 4); L(3**n-5**n, -oo)
    L((5**n-3**(n+1))/(5**(n+1)+2**n), Rational(1, 5)); L((2**(2*n)-3**n)/(3**n+1), oo)
    for m in (400, 401):   # (-2)^n を含むものは Fraction で厳密に計算
        assert abs(F(3**m-(-2)**m, 3**(m+1)+2**m) - F(1, 3)) < F(1, 10**60)
    v = [2**m-(-3)**m for m in range(2, 30)]          # 振動：符号が交互で絶対値は増大
    assert all(v[i]*v[i+1] < 0 and abs(v[i+1]) > abs(v[i]) for i in range(len(v)-1))
    f6 = lambda r, m: (r**(m+1)+2)/(r**m+1)
    for r, val in ((F(1, 2), 2), (F(-1, 2), 2), (F(0), 2), (F(1), F(3, 2)), (F(2), 2), (F(-3), -3), (F(5, 4), F(5, 4))):
        assert abs(f6(r, 600) - val) < F(1, 10**40) and abs(f6(r, 601) - val) < F(1, 10**40)
    g6 = lambda r, m: (1-r**(2*m))/(1+r**(2*m))
    for r, val in ((F(1, 3), 1), (F(-2, 3), 1), (F(1), 0), (F(-1), 0), (F(3, 2), -1), (F(-5), -1)):
        assert abs(g6(r, 600) - val) < F(1, 10**40)
    num(lambda m: m*math.sin(m)/(m*m+1), 0, tol=1e-5)
    for m in (10**5, 10**6, 10**7):
        assert abs(math.isqrt(3*m*m)/m - math.sqrt(3)) < 2/m          # [√3 n] = isqrt(3n^2)
        assert abs(math.floor(5*m+math.sqrt(m))/(2*m) - 2.5) < 1/math.sqrt(m)
        assert abs(math.sqrt(m)*math.cos(m)/(m+1)) <= 1/math.sqrt(m)
    for m in range(3, 300):
        assert 6*2**m >= m*(m-1)*(m-2)
    for m in range(2, 300):
        assert F(11, 10)**m >= F(m*(m-1), 2)*F(1, 100)
    L(n**2/2**n, 0); L(6*n/((n-1)*(n-2)), 0); L(n/(Rational(11, 10))**n, 0)
    for m in (10**4, 10**5):
        s = math.fsum(1/math.sqrt(m*m+j) for j in range(1, m+1)); assert abs(s-1) < 1e-3
        s = math.fsum(1/math.sqrt(m*m+j) for j in range(1, 2*m+1)); assert abs(s-2) < 3e-3
    L(n/sqrt(n**2+n), 1); L(n/sqrt(n**2+1), 1); L(2*n/sqrt(n**2+2*n), 2); L(2*n/sqrt(n**2+1), 2)
    L(n**(1/n), 1)
    for m in range(2, 60):
        h = m**(1/m)-1
        assert h < math.sqrt(2/(m-1)) and (1+h)**m >= m*(m-1)/2*h*h
        c = math.comb(2*m, m)
        assert all(math.comb(2*m, j) <= c for j in range(2*m+1))
        assert 4**m <= (2*m+1)*c <= (2*m+1)*4**m
        if m >= 3:
            assert (2*m+1)**(1/m) <= (m**(1/m))**2 + 1e-12
        assert 2**m < m**3+2**m < m**3*2**m
    for m in (2000, 20000):
        lc = (math.lgamma(2*m+1)-2*math.lgamma(m+1))/m
        assert abs(math.exp(lc)-4) < 0.02
        assert abs(math.exp(math.log(m**3+2**m)/m) - 2) < 1e-6
    # ★5：n(S_n-1) → -1/2 と練習 n(T_n-1) → -1
    t = symbols("t", positive=True)
    assert expand((1+t)*(1-t)) == 1-t**2 and expand((1+t)*(1-t+t**2)) == 1+t**3
    assert simplify(summation((1-k/n**2)/n, (k, 1, n)) - (1-(n+1)/(2*n**2))) == 0
    assert simplify(summation(k**2/n**5, (k, 1, n)) - (n+1)*(2*n+1)/(6*n**4)) == 0
    L(-(n+1)/(2*n), Rational(-1, 2)); L((n+1)*(2*n+1)/(6*n**3), 0)
    for m in (5, 17, 60):
        Sm = sum(F(m, m*m+j) for j in range(1, m+1))
        lo, hi = -F(m+1, 2*m), -F(m+1, 2*m)+F((m+1)*(2*m+1), 6*m**3)
        assert lo < m*(Sm-1) < hi
        assert F(m*m, m*m+m) <= Sm <= F(m*m, m*m+1)
    for m in (10**5, 10**6):
        Sm = math.fsum(m/(m*m+j) for j in range(1, m+1)); assert abs(m*(Sm-1)+0.5) < 1e-4
        Tm = math.fsum(m/(m*m+2*j) for j in range(1, m+1)); assert abs(m*(Tm-1)+1) < 1e-4
    L(-(n+1)/n, -1); L(n*summation(4*k**2/n**5, (k, 1, n)), 0)

    # ---- 節3
    j = symbols("j", positive=True, integer=True)
    assert F(6)/(1-F(-2, 3)) == F(18, 5)
    assert abs(sum(6*(-2/3)**i for i in range(200)) - 3.6) < 1e-12
    assert summation((2**j+(-1)**j)/3**j, (j, 1, oo)) == Rational(7, 4)
    assert F(1, 10)+F(23, 1000)/(1-F(1, 100)) == F(61, 495) and str(61*10**12//495) == "123232323232"
    assert simplify(sqrt(2)/(1-1/sqrt(2)) - (2*sqrt(2)+2)) == 0
    assert summation((3**j-2**j)/4**j, (j, 1, oo)) == 2 and F(27, 99) == F(3, 11)
    assert summation(1/(j*(j+2)), (j, 1, oo)) == Rational(3, 4)
    for m in range(1, 40):
        assert sum(F(1, i*(i+2)) for i in range(1, m+1)) == F(1, 2)*(1+F(1, 2)-F(1, m+1)-F(1, m+2))
        assert sum(F(1, (3*i-2)*(3*i+1)) for i in range(1, m+1)) == F(1, 3)*(1-F(1, 3*m+1))
        assert abs(sum(1/(math.sqrt(i+1)+math.sqrt(i)) for i in range(1, m+1)) - (math.sqrt(m+1)-1)) < 1e-12
        assert abs(sum(math.log((i+1)/i) for i in range(1, m+1)) - math.log(m+1)) < 1e-12
    assert summation(1/((3*j-2)*(3*j+1)), (j, 1, oo)) == Rational(1, 3)
    for xv, val in ((0.0, 0), (0.3, 1), (1.0, 1), (1.9, 1)):
        assert abs(sum(xv*(1-xv)**i for i in range(3000)) - val) < 1e-9
    for xv in (2.0, 2.5, -0.1):                    # 範囲外では発散（項が 0 に収束しない）
        assert abs(xv*(1-xv)**300) >= abs(xv)
    for xv in (0.5, -1.0, 3.0):
        assert abs(sum(xv**2*(1/(1+xv**2))**i for i in range(4000)) - (1+xv**2)) < 1e-9
    for m in range(1, 60):     # かっこの級数
        Sm = sum(F(i, 2*i-1)-F(i+1, 2*i+1) for i in range(1, m+1)); assert Sm == 1-F(m+1, 2*m+1)
        terms = [F(1)] + sum([[-F(i+1, 2*i+1), F(i+1, 2*i+1)] for i in range(1, m+1)], [])
        T = [sum(terms[:q]) for q in range(1, len(terms)+1)]
        assert T[2*m-2] == 1 and T[2*m-1] == 1-F(m+1, 2*m+1)
        Um = sum(F(i, i+1)-F(i+1, i+2) for i in range(1, m+1)); assert Um == F(1, 2)-F(m+1, m+2)
        terms = [F(1, 2)] + sum([[-F(i+1, i+2), F(i+1, i+2)] for i in range(1, m+1)], [])
        T = [sum(terms[:q]) for q in range(1, len(terms)+1)]
        assert T[2*m-2] == F(1, 2) and T[2*m-1] == F(1, 2)-F(m+1, m+2)
    L(1-(n+1)/(2*n+1), Rational(1, 2)); L(Rational(1, 2)-(n+1)/(n+2), Rational(-1, 2))
    for m in range(1, 60):
        assert sum(F(i, 2**i) for i in range(1, m+1)) == 2-F(m+2, 2**m)
    assert summation(j/2**j, (j, 1, oo)) == 2 and summation((2*j-1)/3**j, (j, 1, oo)) == 1
    # 図形と無限等比級数：中心間距離で外接を確認
    r0 = math.sqrt(3)/6; r1 = r0/3
    assert abs((2*r0-2*r1) - (r0+r1)) < 1e-15 and abs(2*r0 - 1/math.sqrt(3)) < 1e-15
    tot = math.pi*r0**2*(1+3*(1/9)/(1-1/9)); assert abs(tot - 11*math.pi/96) < 1e-14
    q = (3-2*sqrt(2))**2
    assert simplify((sqrt(2)-1)/(sqrt(2)+1) - (3-2*sqrt(2))) == 0
    assert simplify(pi*(1+4*q/(1-q)) - (3*sqrt(2)-2)*pi/2) == 0
    rr = 1.0; ratio = 3-2*math.sqrt(2)                 # 正方形：頂点から中心まで √2 r
    assert abs(math.sqrt(2)*(rr-rr*ratio) - (rr+rr*ratio)) < 1e-14
    for al in (math.pi/6, math.pi/4):
        rho = (1-math.sin(al))/(1+math.sin(al))
        assert abs((1-rho)/math.sin(al) - (1+rho)) < 1e-14
    # ★5 ガウス記号を含む級数
    Sg, Np = F(0), 1
    pref = [F(0)]
    for nn in range(1, 2**13):
        pref.append(pref[-1] + F(nn.bit_length()-1, nn*(nn+1)))
    for m in range(1, 13):
        assert pref[2**m-1] == 1-F(m+1, 2**m)
    for NN in random.Random(22).sample(range(1, 2**12), 200):
        m = (NN+1).bit_length()-1
        assert 2**m-1 <= NN < 2**(m+1)-1 and pref[2**m-1] <= pref[NN] <= pref[2**(m+1)-1]
        assert pref[2**(m+1)-1] == 1-F(m+2, 2**(m+1))
    assert summation(j/2**(j+1), (j, 0, oo)) == 1
    def lg3(v):
        e = 0
        while 3**(e+1) <= v:
            e += 1
        return e
    s3 = math.fsum(lg3(nn)/(nn*(nn+1)) for nn in range(1, 3**11))
    assert abs(s3 - 0.5) < 1e-3 and summation(2*j/3**(j+1), (j, 0, oo)) == Rational(1, 2)
    assert sum(F(1, i*(i+1)) for i in range(3**3, 3**4)) == F(2, 3**4)

    # ---- 節4
    import mpmath
    a, b, c = F(1), F(0), F(1)
    for m in range(1, 40):
        assert a == 3-2*F(1, 3)**(m-1) and b == 2-2*F(-1, 2)**(m-1) and c == 3-2**m
        a, b, c = a/3+2, -b/2+3, 2*c-3
    a, b = F(2), F(3)
    for m in range(1, 25):
        assert a == F(3**m+1, 3**m-1) and b == F(2*(5**m+1), 5**m-1)
        a, b = (2*a+1)/(a+2), (3*b+4)/(b+3)
    L((3**n+1)/(3**n-1), 1); L(2*(5**n+1)/(5**n-1), 2)
    a1 = symbols("alpha")
    assert set(__import__("sympy").solve(a1**2-3*a1+2, a1)) == {1, 2}
    with mpmath.workdps(300):
        a, b, c = mpmath.mpf(3)/2, mpmath.mpf(2), mpmath.mpf(3)
        for m in range(1, 200):
            assert 1 < a <= mpmath.mpf(3)/2 and 0 < a-1 <= mpmath.mpf(1)/2*(mpmath.mpf(5)/6)**(m-1)
            assert 1 < b <= 2 and 0 < b-1 <= (mpmath.mpf(3)/4)**(m-1)
            if m < 12:
                assert c-2 >= (mpmath.mpf(4)/3)**(m-1)        # a_1=3 のとき発散
                c = (c**2+2)/3
            na = (a**2+2)/3
            assert (na < a) and abs((na-1) - (a+1)/3*(a-1)) < mpmath.mpf(10)**-250
            a, b = na, (b**2+3)/4
        assert a-1 < mpmath.mpf(10)**-30 and b-1 < mpmath.mpf(10)**-20
    # 硬貨：表が続かない出方の数
    import itertools
    cnt = [sum(1 for w in itertools.product((0, 1), repeat=m) if all(not (w[i] and w[i+1]) for i in range(m-1))) for m in range(1, 17)]
    assert cnt[:2] == [2, 3] and all(cnt[i+2] == cnt[i+1]+cnt[i] for i in range(len(cnt)-2))
    cnt3 = [sum(1 for w in itertools.product((0, 1, 2), repeat=m) if all(not (w[i] == 0 and w[i+1] == 0) for i in range(m-1))) for m in range(1, 10)]
    assert cnt3[:2] == [3, 8] and all(cnt3[i+2] == 2*cnt3[i+1]+2*cnt3[i] for i in range(len(cnt3)-2))
    al, be = (1+sqrt(5))/2, (1-sqrt(5))/2
    assert simplify(al+be-1) == 0 and simplify(al*be+1) == 0 and simplify(3-2*al-(2-sqrt(5))) == 0
    assert simplify(3-2*be - al**3) == 0 and simplify(3-2*al - be**3) == 0
    A = [2, 3]; C3 = [3, 8]
    for m in range(200):
        A.append(A[-1]+A[-2]); C3.append(2*C3[-1]+2*C3[-2])
    with mpmath.workdps(60):
        alm, bem = (1+mpmath.sqrt(5))/2, (1-mpmath.sqrt(5))/2
        for m in range(1, 120):
            assert abs(A[m]-alm*A[m-1] - (2-mpmath.sqrt(5))*bem**(m-1)) < mpmath.mpf(10)**-30
            assert A[m-1] == int(mpmath.nint((alm**(m+2)-bem**(m+2))/mpmath.sqrt(5)))
    assert abs(F(A[150], 2*A[149]) - (1+5**0.5)/4) < 1e-15 and abs(F(C3[150], C3[149]) - (1+3**0.5)) < 1e-14
    # ★5：n a_n → 1
    aa = symbols("a", positive=True)
    assert simplify(1/(aa*(1-aa)) - (1/aa+1/(1-aa))) == 0
    assert simplify((1+aa**2)**2/aa**2 - (1/aa**2+2+aa**2)) == 0
    a, b, hs = 0.5, 1.0, 0.0
    for m in range(1, 10**6+1):
        assert 1/a >= m+1-1e-9 and 1/a < m+1+4*math.sqrt(m) and 0 < a <= 0.5
        assert 1/b**2 >= 2*m-1-1e-9 and 1/b**2 < 2*m-1+2*math.sqrt(m)
        if m >= 2:
            hs += 1/m
            if m < 10**4:
                assert hs < 2*(math.sqrt(m)-1)
        a, b = a-a*a, b/(1+b*b)
    m = 10**6+1
    assert abs(m*a-1) < 1e-4 and abs(math.sqrt(m)*b - 1/math.sqrt(2)) < 1e-4
    L(n/(n+1+4*sqrt(n)), 1); L(n/(n+1), 1); L(n/(2*n-1+2*sqrt(n)), Rational(1, 2)); L(n/(2*n-1), Rational(1, 2))

    # ---- 節5
    LX = lambda e, v, pt, d="+": L(e, v, var=x, pt=pt, d=d)
    LX((x**3-8)/(x**2-3*x+2), 12, 2); LX((x**3-8)/(x**2-3*x+2), 12, 2, "-")
    LX((sqrt(1+x)-sqrt(1-x))/x, 1, 0); LX((sqrt(1+x)-sqrt(1-x))/x, 1, 0, "-"); LX((2*x**2-1)/(x**2+3*x), 2, oo)
    LX((x**3+1)/(x**2-1), Rational(-3, 2), -1); LX((x**3+1)/(x**2-1), Rational(-3, 2), -1, "-")
    LX((sqrt(x+1)-2)/(x-3), Rational(1, 4), 3); LX((3*x-1)/sqrt(x**2+1), 3, oo)
    LX((x**2-1)/Abs(x-1), 2, 1, "+"); LX((x**2-1)/Abs(x-1), -2, 1, "-"); LX(sqrt(x**2+3*x)+x, Rational(-3, 2), -oo)
    LX(Abs(x)/(x**2+x), 1, 0, "+"); LX(Abs(x)/(x**2+x), -1, 0, "-"); LX(sqrt(x**2-2*x+3)+x, 1, -oo)
    num(lambda X: math.sqrt(X*X+3*X)+X, -1.5, big=-10**6)
    LX((4*sqrt(x+2)-8)/(x-2), 1, 2); LX((4*sqrt(x+2)-8)/(x-2), 1, 2, "-")
    assert expand((x-1)*(7*x-3)) == 7*x**2-10*x+3
    LX((7*x**2-10*x+3)/(x-1), 4, 1); LX((7*x**2-10*x+3)/(x-1), 4, 1, "-")
    aa_, bb_ = symbols("a_ b_")
    assert __import__("sympy").solve([2*aa_+bb_, aa_/4-1], [aa_, bb_]) == {aa_: 4, bb_: -8}

    # ---- 節6
    for d in ("+", "-"):
        LX(sin(3*x)/sin(5*x), Rational(3, 5), 0, d); LX((1-cos(x))/x**2, Rational(1, 2), 0, d)
        LX(sin(x)/(x-pi), -1, pi, d); LX(tan(2*x)/x, 2, 0, d); LX((1-cos(2*x))/(x*sin(x)), 2, 0, d)
        LX((1-3*x)**(1/x), exp(-3), 0, d); LX((1+2*x)**(3/x), exp(6), 0, d)
        LX(log(1+x)/x, 1, 0, d); LX((exp(x)-1)/x, 1, 0, d)
        LX((exp(3*x)-exp(x))/log(1+2*x), 1, 0, d); LX((2**x-1)/x, log(2), 0, d)
        LX(log(1+3*x)/sin(x), 3, 0, d); LX((3**x-2**x)/x, log(Rational(3, 2)), 0, d)
    LX(x*sin(1/x), 1, oo); LX(x*(log(x+2)-log(x)), 2, oo)
    L((1+2/n)**n, exp(2)); L((n/(n+1))**n, exp(-1)); L((1-1/(2*n))**n, exp(Rational(-1, 2))); L((1+1/n)**(2*n+1), exp(2))
    num(lambda m: (1+2/m)**m, math.e**2, big=10**7, tol=1e-5); num(lambda m: (1-1/(2*m))**m, math.exp(-0.5), big=10**7, tol=1e-6)
    # 図形：座標で △APT の面積を確認
    th = symbols("theta", positive=True)
    for tv in (0.3, 0.7, 1.2):
        Ax, Ay, Px, Py, Tx, Ty = 1, 0, math.cos(tv), math.sin(tv), 1, math.tan(tv)
        area = abs((Px-Ax)*(Ty-Ay)-(Tx-Ax)*(Py-Ay))/2
        assert abs(area - math.tan(tv)*(1-math.cos(tv))/2) < 1e-12
    assert simplify(tan(th)-sin(th) - tan(th)*(1-cos(th))) == 0
    L(tan(th)*(1-cos(th))/2/th**3, Rational(1, 4), var=th, pt=0)
    tq = symbols("t", positive=True)       # 練習：t=π/n
    L(pi**3*tan(tq)*sin(tq)**2/tq**3, pi**3, var=tq, pt=0)
    for m in (6, 50, 10**5):
        Sm, Tm = m/2*math.sin(2*math.pi/m), m*math.tan(math.pi/m)
        assert abs((Tm-Sm) - m*math.tan(math.pi/m)*math.sin(math.pi/m)**2) < 1e-9
    assert abs(m**2*(m*math.tan(math.pi/m)-m/2*math.sin(2*math.pi/m)) - math.pi**3) < 1e-3
    # 2cos の置き換え
    with mpmath.workdps(80):
        a, b = mpmath.mpf(0), mpmath.mpf(1)
        for m in range(1, 60):
            assert abs(a - 2*mpmath.cos(mpmath.pi/2**m)) < mpmath.mpf(10)**-70
            assert abs(b - 2*mpmath.cos(mpmath.pi/(3*2**(m-1)))) < mpmath.mpf(10)**-70
            assert abs((2-a) - 4*mpmath.sin(mpmath.pi/2**(m+1))**2) < mpmath.mpf(10)**-70
            a, b = mpmath.sqrt(2+a), mpmath.sqrt(2+b)
        assert abs(4**60*(2-a) - mpmath.pi**2) < 1e-30 and abs(4**60*(2-b) - 4*mpmath.pi**2/9) < 1e-30
    L(pi**2*(sin(tq)/tq)**2, pi**2, var=tq, pt=0)
    # ★5：倍角公式で差の形
    xx = symbols("x", real=True)
    assert simplify(expand((4*sin(xx)**2-sin(2*xx)**2-4*sin(xx)**4).rewrite(cos).expand(trig=True))) == 0
    assert simplify((3*sin(xx)-sin(3*xx)-4*sin(xx)**3).expand(trig=True)) == 0
    for tv in (0.0, 0.4, 2.0, -3.0, 10.0):
        s4 = math.fsum(4**m*math.sin(tv/2**m)**4 for m in range(1, 60))
        s3 = math.fsum(3**(m-1)*math.sin(tv/3**m)**3 for m in range(1, 40))
        assert abs(s4 - (tv*tv-math.sin(tv)**2)) < 1e-9 and abs(s3 - (tv-math.sin(tv))/4) < 1e-12
        for N_ in (1, 2, 5, 9):
            assert abs(math.fsum(4**m*math.sin(tv/2**m)**4 for m in range(1, N_+1)) - (4**N_*math.sin(tv/2**N_)**2-math.sin(tv)**2)) < 1e-9

    # ---- 節7
    LX((x**2+x-2)/(x-1), 3, 1); LX((x**2+x-2)/(x-1), 3, 1, "-"); LX((sqrt(x+3)-2)/(x-1), Rational(1, 4), 1)
    LX((sqrt(x+3)-2)/(x-1), Rational(1, 4), 1, "-")
    for e_ in (1e-6, 1e-9):
        assert abs((1+e_)*math.floor(1+e_) - 1) < 1e-5 and (1-e_)*math.floor(1-e_) == 0
        assert abs(e_*math.floor(1+e_)) < 1e-5 and abs(-e_*math.floor(1-e_)) < 1e-5
        g_ = lambda X: X-math.floor(X)
        assert g_(2+e_) < 1e-5 and abs(g_(2-e_)-1) < 1e-5 and g_(2) == 0
    assert math.cos(0)-0 > 0 and math.cos(math.pi/2)-math.pi/2 < 0
    cub = x**3-3*x+1; qua = x**4-4*x**2+x+1
    assert [cub.subs(x, v) for v in (-2, 0, 1, 2)] == [-1, 1, -1, 3]
    assert [qua.subs(x, v) for v in (-3, -1, 0, 1, 2)] == [43, -3, 1, -1, 3]
    assert len(real_roots(Poly(cub, x))) == 3 and len(set(real_roots(Poly(qua, x)))) == 4
    assert math.exp(-1)-1 < 0 and math.exp(0)+0 > 0
    def flim(fn, X, m=400):
        return fn(X, m)
    f35 = lambda X, m: (X**(2*m+1)-X**2+X+1)/(X**(2*m)+1)
    p35 = lambda X: -X**2+X+1 if abs(X) < 1 else (X if abs(X) > 1 else (F(1) if X == 1 else F(-1)))
    f35e = lambda X, m: (X**(2*m+2)+0*X+1)/(X**(2*m)+1)
    p35e = lambda X: 1 if abs(X) <= 1 else X**2
    for X in (F(0), F(1, 2), F(-9, 10), F(1), F(-1), F(11, 10), F(-3), F(5, 4)):
        assert abs(f35(X, 400) - p35(X)) < F(1, 10**15) and abs(f35e(X, 400) - p35e(X)) < F(1, 10**15)
    A_, B_ = symbols("A_ B_")
    sol = __import__("sympy").solve([-1+A_+B_-1, (A_+B_)/2-1, -1-A_+B_+1, (B_-A_-2)/2+1], [A_, B_])
    assert sol == {A_: 1, B_: 1}
    sol = __import__("sympy").solve([A_+B_-1, (1+A_+B_)/2-1, -A_+B_-1, (1-A_+B_)/2-1], [A_, B_])
    assert sol == {A_: 0, B_: 1}
    # 中間値の定理の応用：ランダムな連続関数で確かめる
    rnd = random.Random(2022)
    def bisect(g, lo, hi):
        glo = g(lo)
        for _ in range(80):
            mid = (lo+hi)/2
            if (g(mid) > 0) == (glo > 0):
                lo, glo = mid, g(mid)
            else:
                hi = mid
        return lo
    for trial in range(200):
        cs = [(rnd.uniform(-2, 2), rnd.uniform(0.3, 9), rnd.uniform(0, 6.3)) for _ in range(4)]
        p_ = lambda X: sum(cA*math.sin(w*X+ph) for cA, w, ph in cs)
        for Lh, h in ((2.0, 1.0), (1.0, 1/3)):
            f_ = lambda X: p_(X)-(p_(Lh)-p_(0))*X/Lh       # f(0)=f(L)
            g = lambda X: f_(X+h)-f_(X)
            pts = [k*h for k in range(round(Lh/h))]
            assert abs(sum(g(t_) for t_ in pts)) < 1e-9
            vals = [g(t_) for t_ in pts]
            i0 = next((i for i in range(len(vals)) if abs(vals[i]) < 1e-15), None)
            if i0 is None:
                i = next(i for i in range(len(vals)) for j in range(len(vals)) if vals[i]*vals[j] < 0 and i < j)
                j = next(j for j in range(i+1, len(vals)) if vals[i]*vals[j] < 0)
                c_ = bisect(g, pts[i], pts[j])
                assert 0 <= c_ <= Lh-h and abs(g(c_)) < 1e-9
    # ★5：x^n+…+x=1 の正の解
    with mpmath.workdps(60):
        def root(m, rhs):
            fx = lambda X: sum(X**k for k in range(1, m+1)) - rhs
            lo, hi = mpmath.mpf(0), mpmath.mpf(1)
            for _ in range(200):
                mid = (lo+hi)/2
                if fx(mid) > 0:
                    hi = mid
                else:
                    lo = mid
            return lo
        for m in list(range(2, 61)) + [150]:
            xm = root(m, 1)
            assert mpmath.mpf(1)/2 < xm < mpmath.mpf(2)/3
            assert abs((2*xm-1) - xm**(m+1)) < mpmath.mpf(10)**-50
            eps = xm**(m+1)
            assert (m+1)*eps < (m+1)*(mpmath.mpf(2)/3)**(m+1) <= mpmath.mpf(8)/m
            if (m+1)*eps < 1 and m <= 40:
                assert 1 < (1+eps)**(m+1) < 1/(1-(m+1)*eps)
            if m >= 3:
                ym = root(m, 2)
                assert abs((3*ym-2) - ym**(m+1)) < mpmath.mpf(10)**-50
                if m >= 4:
                    assert ym <= mpmath.mpf(4)/5
        assert abs(xm-mpmath.mpf(1)/2) < 1e-40 and abs(2**150*(2*xm-1) - mpmath.mpf(1)/2) < 1e-20
        assert abs(ym-mpmath.mpf(2)/3) < 1e-20 and abs(mpmath.mpf(3)**150/2**150*(3*ym-2) - mpmath.mpf(2)/3) < 1e-10
        for m in range(1, 40):
            assert 2*(1-(mpmath.mpf(2)/3)**m) >= (mpmath.mpf(10)/9 if m >= 2 else 0)
            ev = mpmath.mpf(1)/7
            assert (1-ev)**m >= 1-m*ev
    L((Rational(2, 3))**(n+1)*(n+1), 0)

    # ---- 例題数と難易度の配分
    items = [it for s in SEC for it in s["items"]]
    lv = [it["lv"] for it in items]
    assert 32 <= len(items) <= 38, len(items)
    assert lv.count(5) >= 3 and all(lv.count(v) >= 3 for v in range(1, 6))
    assert all(it[k] for it in items for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"))
    for s_ in SEC:
        lvs = [it["lv"] for it in s_["items"]]
        assert lvs == sorted(lvs), s_["title"]
    assert 4 <= len(SEC) <= 9
    print("c22:", len(items), "題", {v: lv.count(v) for v in range(1, 6)})
