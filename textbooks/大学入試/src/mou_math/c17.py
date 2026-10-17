"""第17章 統計的な推測（数学B）"""
from fractions import Fraction as Fr
from itertools import combinations, permutations, product
from math import comb, sqrt, erf, isclose
import random
import re

# 正規分布表の値（問題文で与える）
PZ = {"0.4": "0.1554", "0.5": "0.1915", "1": "0.3413", "1.28": "0.3997", "1.5": "0.4332",
      "1.96": "0.475", "2": "0.4772", "2.2": "0.4861", "2.5": "0.4938", "2.58": "0.495"}


def zt(*us):
    return (r"ただし、$Z$ を標準正規分布 $N(0,\ 1)$ に従う確率変数として、"
            + "，".join(f"$P(0\\leqq Z\\leqq{u})={PZ[u]}$" for u in us) + " とする。")


def tb(*rows):
    s = "<table>"
    for r in rows:
        s += "<tr><th>" + r[0] + "</th>" + "".join("<td>" + c + "</td>" for c in r[1:]) + "</tr>"
    return s + "</table>"


SEC = []

# ---------------------------------------------------------------- 節1
SEC.append({"title": "確率変数と確率分布",
"base": r"""・確率変数 $X$ のとる値 $x_1,\ x_2,\ \cdots,\ x_n$ と、それぞれの値をとる確率 $p_1,\ p_2,\ \cdots,\ p_n$（$p_k\geqq0$，$p_1+\cdots+p_n=1$）との対応を $X$ の確率分布という。<br>
・期待値（平均）$E(X)=\displaystyle\sum_{k=1}^n x_kp_k=m$，分散 $V(X)=\displaystyle\sum_{k=1}^n (x_k-m)^2p_k=E(X^2)-\{E(X)\}^2$，標準偏差 $\sigma(X)=\sqrt{V(X)}$<br>
・$a,\ b$ が定数のとき　$E(aX+b)=aE(X)+b$，$V(aX+b)=a^2V(X)$，$\sigma(aX+b)=|a|\sigma(X)$""",
"items": [
 {"lv": 1, "title": "確率分布と期待値・分散",
  "q": r"赤玉 $4$ 個と白玉 $3$ 個が入った袋から $3$ 個の玉を同時に取り出し、その中の赤玉の個数を $X$ とする。$X$ の確率分布を求めよ。また、$X$ の期待値・分散・標準偏差を求めよ。",
  "hint": r"$X$ のとる値は $0,\ 1,\ 2,\ 3$。各値をとる確率を組合せの数で求めて表にまとめる（確率の和が $1$ になることで検算できる）。分散は定義式より $E(X^2)-\{E(X)\}^2$ で計算するほうが速い。",
  "sol": r"玉の取り出し方は全部で ${}_7\mathrm{C}_3=35$ 通りあり、$X=k$ となるのは赤玉 $k$ 個・白玉 $3-k$ 個を選ぶ ${}_4\mathrm{C}_k\cdot{}_3\mathrm{C}_{3-k}$ 通りである。よって $X$ の確率分布は次の表のようになる。"
         + tb([r"$X$", "$0$", "$1$", "$2$", "$3$", "計"],
              [r"$P$", r"$\dfrac{1}{35}$", r"$\dfrac{12}{35}$", r"$\dfrac{18}{35}$", r"$\dfrac{4}{35}$", "$1$"])
         + r"$E(X)=0\cdot\dfrac{1}{35}+1\cdot\dfrac{12}{35}+2\cdot\dfrac{18}{35}+3\cdot\dfrac{4}{35}=\dfrac{60}{35}=\boldsymbol{\dfrac{12}{7}}$<br>"
           r"$E(X^2)=0^2\cdot\dfrac{1}{35}+1^2\cdot\dfrac{12}{35}+2^2\cdot\dfrac{18}{35}+3^2\cdot\dfrac{4}{35}=\dfrac{120}{35}=\dfrac{24}{7}$<br>"
           r"$V(X)=\dfrac{24}{7}-\left(\dfrac{12}{7}\right)^2=\dfrac{168-144}{49}=\boldsymbol{\dfrac{24}{49}}$，$\sigma(X)=\sqrt{\dfrac{24}{49}}=\boldsymbol{\dfrac{2\sqrt6}{7}}$",
  "note": r"一般に、$N$ 個中 $M$ 個が赤玉の袋から $n$ 個を同時に取り出すとき、赤玉の個数の期待値は $\dfrac{nM}{N}$ になる（17.2 節の「和に分ける」方法で示せる）。本問では $\dfrac{3\cdot4}{7}=\dfrac{12}{7}$ で一致する。",
  "ex": r"赤玉 $5$ 個と白玉 $3$ 個が入った袋から $2$ 個の玉を同時に取り出すとき、取り出した赤玉の個数 $X$ の期待値と分散を求めよ。",
  "exa": r"$E(X)=\dfrac54$，$V(X)=\dfrac{45}{112}$"},
 {"lv": 2, "title": "1次式で変換した確率変数（平均・標準偏差の調整）",
  "q": r"確率変数 $X$ の確率分布が次の表で与えられている。"
       + tb([r"$X$", "$1$", "$2$", "$3$", "$4$", "$5$", "計"],
            [r"$P$", r"$\dfrac{1}{16}$", r"$\dfrac{1}{4}$", r"$\dfrac{3}{8}$", r"$\dfrac{1}{4}$", r"$\dfrac{1}{16}$", "$1$"])
       + r"(1) $E(X)$，$V(X)$ を求めよ。<br>(2) $a,\ b$ を定数（$a\gt0$）とし、$Y=aX+b$ とする。$E(Y)=50$，$\sigma(Y)=10$ となるように $a,\ b$ の値を定めよ。<br>(3) (2) のとき、$P(Y\geqq60)$ を求めよ。",
  "hint": r"(2) は公式 $E(aX+b)=aE(X)+b$，$\sigma(aX+b)=|a|\sigma(X)$ を使えば、$Y$ の分布を作り直さずに済む。(3) は $Y\geqq60$ を $X$ の条件に直す。",
  "sol": r"(1) $E(X)=1\cdot\dfrac{1}{16}+2\cdot\dfrac{4}{16}+3\cdot\dfrac{6}{16}+4\cdot\dfrac{4}{16}+5\cdot\dfrac{1}{16}=\dfrac{48}{16}=\boldsymbol{3}$<br>"
         r"$V(X)=(1-3)^2\cdot\dfrac{1}{16}+(2-3)^2\cdot\dfrac{4}{16}+(3-3)^2\cdot\dfrac{6}{16}+(4-3)^2\cdot\dfrac{4}{16}+(5-3)^2\cdot\dfrac{1}{16}=\dfrac{4+4+0+4+4}{16}=\boldsymbol{1}$<br>"
         r"(2) $\sigma(X)=1$ で $a\gt0$ だから $\sigma(Y)=a\sigma(X)=a=10$。また $E(Y)=aE(X)+b=30+b=50$ より $b=20$。よって $\boldsymbol{a=10,\ b=20}$<br>"
         r"(3) $Y=10X+20\geqq60\iff X\geqq4$ だから　$P(Y\geqq60)=P(X=4)+P(X=5)=\dfrac{4}{16}+\dfrac{1}{16}=\boldsymbol{\dfrac{5}{16}}$",
  "note": r"$Z=\dfrac{X-E(X)}{\sigma(X)}$ とおくと $E(Z)=0$，$\sigma(Z)=1$ となる（標準化）。本問の $Y=10Z+50$ は偏差値と同じ変換である。分散は $V(aX+b)=a^2V(X)$ で、定数 $b$ を加えても変わらない。",
  "ex": r"確率変数 $X$ のとる値が $0,\ 1,\ 2$ で、それぞれの確率が $\dfrac14,\ \dfrac12,\ \dfrac14$ である。$Y=aX+b$（$a\gt0$）の期待値が $0$、分散が $1$ となるように定数 $a,\ b$ の値を定めよ。",
  "exa": r"$a=\sqrt2,\ b=-\sqrt2$"},
 {"lv": 3, "title": "確率に文字を含む分布（Σの公式の利用）",
  "q": r"$n$ を $2$ 以上の整数とする。確率変数 $X$ のとる値が $1,\ 2,\ \cdots,\ n$ で、$P(X=k)=ck$（$k=1,\ 2,\ \cdots,\ n$，$c$ は定数）であるとき、$c$ の値と $E(X)$，$V(X)$ を求めよ。",
  "hint": r"確率の総和が $1$ であることから $c$ が決まる。$E(X)$，$E(X^2)$ はそれぞれ $\sum k^2$，$\sum k^3$ の公式で計算できる。",
  "sol": r"確率の総和は $1$ なので　$\displaystyle\sum_{k=1}^n ck=c\cdot\dfrac{n(n+1)}{2}=1$　よって　$\boldsymbol{c=\dfrac{2}{n(n+1)}}$<br>"
         r"$E(X)=\displaystyle\sum_{k=1}^n k\cdot ck=c\cdot\dfrac{n(n+1)(2n+1)}{6}=\boldsymbol{\dfrac{2n+1}{3}}$<br>"
         r"$E(X^2)=\displaystyle\sum_{k=1}^n k^2\cdot ck=c\left\{\dfrac{n(n+1)}{2}\right\}^2=\dfrac{n(n+1)}{2}$<br>"
         r"$V(X)=\dfrac{n(n+1)}{2}-\dfrac{(2n+1)^2}{9}=\dfrac{9n^2+9n-2(4n^2+4n+1)}{18}=\dfrac{n^2+n-2}{18}=\boldsymbol{\dfrac{(n-1)(n+2)}{18}}$",
  "note": r"$n=2$ のとき $P(X=1)=\dfrac13$，$P(X=2)=\dfrac23$ で、直接計算すると $E(X)=\dfrac53$，$V(X)=3-\dfrac{25}{9}=\dfrac29$ となり、公式と一致する。文字を含む答えは小さい $n$ で確かめるとよい。",
  "ex": r"$n$ を $2$ 以上の整数とする。確率変数 $X$ のとる値が $1,\ 2,\ \cdots,\ n$ で、$P(X=k)=c(n+1-k)$（$c$ は定数）であるとき、$c$ の値と $E(X)$，$V(X)$ を求めよ。",
  "exa": r"$c=\dfrac{2}{n(n+1)}$，$E(X)=\dfrac{n+2}{3}$，$V(X)=\dfrac{(n-1)(n+2)}{18}$"},
 {"lv": 4, "title": "取り出した数の最大値の期待値",
  "q": r"$n$ を $3$ 以上の整数とする。$1$ から $n$ までの番号が $1$ つずつ書かれた $n$ 枚のカードから $3$ 枚を同時に取り出し、その中の最大の番号を $X$ とする。<br>(1) $P(X=k)$（$3\leqq k\leqq n$）を求めよ。<br>(2) $E(X)$ を求めよ。",
  "hint": r"(1)「最大が $k$」は「$k$ を含み、残り $2$ 枚は $1$ 〜 $k-1$ から選ぶ」ことと同じ。(2) $k\cdot{}_{k-1}\mathrm{C}_2=3\cdot{}_k\mathrm{C}_3$ と変形し、${}_k\mathrm{C}_3={}_{k+1}\mathrm{C}_4-{}_k\mathrm{C}_4$ を用いて差の形にすれば和が求まる。",
  "sol": r"(1) $X=k$ となるのは、番号 $k$ のカードを取り出し、残りの $2$ 枚を $1$ 〜 $k-1$ の $k-1$ 枚から選ぶときだから<br>"
         r"$P(X=k)=\boldsymbol{\dfrac{{}_{k-1}\mathrm{C}_2}{{}_n\mathrm{C}_3}=\dfrac{3(k-1)(k-2)}{n(n-1)(n-2)}}$<br>"
         r"(2) $k\cdot{}_{k-1}\mathrm{C}_2=\dfrac{k(k-1)(k-2)}{2}=3\cdot{}_k\mathrm{C}_3$ である。また、${}_{k+1}\mathrm{C}_4={}_k\mathrm{C}_4+{}_k\mathrm{C}_3$ より ${}_k\mathrm{C}_3={}_{k+1}\mathrm{C}_4-{}_k\mathrm{C}_4$（ただし ${}_3\mathrm{C}_4=0$ と定める）だから<br>"
         r"$\displaystyle\sum_{k=3}^n{}_k\mathrm{C}_3=\sum_{k=3}^n\left({}_{k+1}\mathrm{C}_4-{}_k\mathrm{C}_4\right)={}_{n+1}\mathrm{C}_4$<br>"
         r"よって　$E(X)=\displaystyle\sum_{k=3}^n k\cdot\dfrac{{}_{k-1}\mathrm{C}_2}{{}_n\mathrm{C}_3}=\dfrac{3\cdot{}_{n+1}\mathrm{C}_4}{{}_n\mathrm{C}_3}=3\cdot\dfrac{(n+1)n(n-1)(n-2)}{24}\cdot\dfrac{6}{n(n-1)(n-2)}=\boldsymbol{\dfrac{3(n+1)}{4}}$",
  "note": r"同様に $r$ 枚を取り出すと、最大の番号の期待値は $\dfrac{r(n+1)}{r+1}$ になる。また、番号 $k$ を $n+1-k$ に付け替える対称性から、最小の番号の期待値は $(n+1)-\dfrac{3(n+1)}{4}=\dfrac{n+1}{4}$。$\sum k(k-1)(k-2)$ を展開して $\sum k^3$ などの公式で計算してもよいが、上の方法が速い。",
  "ex": r"$n$ を $2$ 以上の整数とする。$1$ から $n$ までの番号が書かれた $n$ 枚のカードから $2$ 枚を同時に取り出し、小さいほうの番号を $Y$ とする。$E(Y)$ を求めよ。",
  "exa": r"$\dfrac{n+1}{3}$"},
]})

# ---------------------------------------------------------------- 節2
SEC.append({"title": "確率変数の和と積",
"base": r"""・$2$ つの確率変数 $X,\ Y$ について、つねに $E(X+Y)=E(X)+E(Y)$，$E(aX+bY)=aE(X)+bE(Y)$（$3$ つ以上でも同様）<br>
・$X,\ Y$ が独立（すべての $a,\ b$ について $P(X=a,\ Y=b)=P(X=a)P(Y=b)$）のとき<br>　$E(XY)=E(X)E(Y)$，$V(aX+bY)=a^2V(X)+b^2V(Y)$（$a,\ b$ は定数）<br>
・個数を表す確率変数は、事象 $A_i$ が起これば $1$、起こらなければ $0$ をとる確率変数 $X_i$ の和 $X=X_1+\cdots+X_n$ に分けると扱いやすい。$E(X_i)=P(A_i)$，$X_i^2=X_i$ である。""",
"items": [
 {"lv": 1, "title": "独立な確率変数の和と積の期待値・分散",
  "q": r"$1$ 個のさいころと $2$ 枚の硬貨を同時に投げる。さいころの出た目を $X$、硬貨の表が出た枚数を $Y$ とする。<br>(1) $E(X)$，$V(X)$，$E(Y)$，$V(Y)$ を求めよ。<br>(2) $E(X+2Y)$，$V(X+2Y)$，$E(XY)$ を求めよ。",
  "hint": r"$X$ と $Y$ は別々の試行で決まるので独立である。和の期待値はいつでも分けられ、和の分散と積の期待値は独立性を使って分けられる。",
  "sol": r"(1) $E(X)=\dfrac{1+2+\cdots+6}{6}=\boldsymbol{\dfrac72}$，$E(X^2)=\dfrac{1^2+2^2+\cdots+6^2}{6}=\dfrac{91}{6}$ より　$V(X)=\dfrac{91}{6}-\dfrac{49}{4}=\boldsymbol{\dfrac{35}{12}}$<br>"
         r"$Y$ が $0,\ 1,\ 2$ をとる確率はそれぞれ $\dfrac14,\ \dfrac12,\ \dfrac14$ なので　$E(Y)=\boldsymbol{1}$，$E(Y^2)=1^2\cdot\dfrac12+2^2\cdot\dfrac14=\dfrac32$ より　$V(Y)=\dfrac32-1^2=\boldsymbol{\dfrac12}$<br>"
         r"(2) $E(X+2Y)=E(X)+2E(Y)=\dfrac72+2=\boldsymbol{\dfrac{11}{2}}$<br>"
         r"$X$ と $Y$ は独立なので　$V(X+2Y)=V(X)+2^2V(Y)=\dfrac{35}{12}+2=\boldsymbol{\dfrac{59}{12}}$，$E(XY)=E(X)E(Y)=\boldsymbol{\dfrac72}$",
  "note": r"独立でないときは、$E(XY)=E(X)E(Y)$ や $V(X+Y)=V(X)+V(Y)$ は一般には成り立たない。例えば $1,\ 2,\ 3$ のカードから $1$ 枚ずつ戻さずに $2$ 枚引き、$1$ 枚目の数を $X$、$2$ 枚目の数を $Y$ とすると、$E(X)=E(Y)=2$ だが<br>　$E(XY)=\dfrac{2+3+2+6+3+6}{6}=\dfrac{11}{3}\neq4$<br>である。",
  "ex": r"さいころを $2$ 回投げ、$1$ 回目の目を $X$、$2$ 回目の目を $Y$ とする。$E(3X-2Y)$，$V(3X-2Y)$，$E(XY)$ を求めよ。",
  "exa": r"$E(3X-2Y)=\dfrac72$，$V(3X-2Y)=\dfrac{455}{12}$，$E(XY)=\dfrac{49}{4}$"},
 {"lv": 3, "title": "和に分けて期待値を求める（出る目の種類の数）",
  "q": r"$1$ 個のさいころを $n$ 回投げるとき、出た目の種類の数を $X$ とする。例えば $n=4$ で $1,\ 3,\ 3,\ 6$ と出れば $X=3$ である。$E(X)$ を $n$ で表せ。",
  "hint": r"$X$ の確率分布を直接求めるのは大変である。目 $k$ ごとに「$k$ の目が少なくとも $1$ 回出れば $1$、出なければ $0$」をとる確率変数 $X_k$ を考えると $X=X_1+\cdots+X_6$ となり、期待値は各 $E(X_k)$ の和で求まる。",
  "sol": r"$k=1,\ 2,\ \cdots,\ 6$ に対し、$k$ の目が少なくとも $1$ 回出れば $X_k=1$，$1$ 回も出なければ $X_k=0$ とおく。出た目の種類の数は値 $1$ をとる $X_k$ の個数だから　$X=X_1+X_2+\cdots+X_6$<br>"
         r"$k$ の目が $n$ 回とも出ない確率は $\left(\dfrac56\right)^n$ なので　$E(X_k)=1\cdot P(X_k=1)=1-\left(\dfrac56\right)^n$<br>"
         r"期待値の和の性質（独立でなくても成り立つ）より　$E(X)=E(X_1)+\cdots+E(X_6)=\boldsymbol{6\left\{1-\left(\dfrac56\right)^n\right\}}$",
  "note": r"$X_1,\ \cdots,\ X_6$ は独立ではない（例えば $n=1$ なら必ず $X_1+\cdots+X_6=1$）が、期待値の和の性質は独立性を必要としない。$n=2$ では $6\left(1-\dfrac{25}{36}\right)=\dfrac{11}{6}$ で、$X=1$（確率 $\dfrac16$）、$X=2$（確率 $\dfrac56$）から直接計算した値と一致する。",
  "ex": r"$10$ 種類のカードのうちどれか $1$ 枚が等しい確率で入っている菓子を $n$ 個買うとき、手に入るカードの種類の数の期待値を求めよ。",
  "exa": r"$10\left\{1-\left(\dfrac{9}{10}\right)^n\right\}$"},
 {"lv": 4, "title": "独立でない確率変数の和の分散（一致の個数）",
  "q": r"$n$ 人（$n\geqq2$）がそれぞれプレゼントを $1$ 個ずつ持ち寄り、それらをよく混ぜて $1$ 人に $1$ 個ずつ無作為に配る（$n!$ 通りの配り方が同様に確からしい）。自分が持ってきたプレゼントを受け取る人数を $X$ とする。<br>(1) $E(X)$ を求めよ。<br>(2) $V(X)$ を求めよ。",
  "hint": r"人 $i$ が自分のプレゼントを受け取れば $1$ となる $X_i$ の和に分ける。$X_i$ どうしは独立でないので $V(X)=\sum V(X_i)$ は使えない。$X^2=\sum X_i^2+2\sum_{i\lt j}X_iX_j$ と展開して $E(X^2)$ を計算する。",
  "sol": r"人 $i$（$i=1,\ \cdots,\ n$）が自分のプレゼントを受け取るとき $X_i=1$，そうでないとき $X_i=0$ とすると　$X=X_1+\cdots+X_n$<br>"
         r"(1) 人 $i$ が自分のものを受け取る配り方は、残り $n-1$ 個の配り方の $(n-1)!$ 通りだから $E(X_i)=\dfrac{(n-1)!}{n!}=\dfrac1n$。よって　$E(X)=n\cdot\dfrac1n=\boldsymbol{1}$<br>"
         r"(2) $X_i^2=X_i$ に注意すると　$X^2=\displaystyle\sum_{i=1}^n X_i+2\sum_{i\lt j}X_iX_j$<br>"
         r"$i\neq j$ のとき、$X_iX_j=1$ となるのは $i,\ j$ がともに自分のものを受け取るときで、その配り方は $(n-2)!$ 通りだから<br>　$E(X_iX_j)=\dfrac{(n-2)!}{n!}=\dfrac{1}{n(n-1)}$<br>"
         r"組 $(i,\ j)$（$i\lt j$）は ${}_n\mathrm{C}_2$ 個あるので　$E(X^2)=1+2\cdot\dfrac{n(n-1)}{2}\cdot\dfrac{1}{n(n-1)}=2$<br>"
         r"よって　$V(X)=E(X^2)-\{E(X)\}^2=2-1=\boldsymbol{1}$",
  "note": r"もし $X_i$ が独立なら $V(X)=n\cdot\dfrac1n\left(1-\dfrac1n\right)=1-\dfrac1n$ となるはずだが、実際の値 $1$ とは異なる。独立でない和の分散は $V(X)=\sum V(X_i)+2\sum_{i\lt j}\{E(X_iX_j)-E(X_i)E(X_j)\}$ で、後半の項が効いてくる。期待値も分散も $n$ によらないことに注意しよう。",
  "ex": r"$3$ つの箱 A，B，C に、区別のつく $4$ 個の玉を $1$ 個ずつ無作為に入れる（各玉はどの箱にも確率 $\dfrac13$ で入り、玉の入り方は互いに独立）。空の箱の個数 $Y$ の期待値と分散を求めよ。",
  "exa": r"$E(Y)=\dfrac{16}{27}$，$V(Y)=\dfrac{230}{729}$"},
 {"lv": 5, "title": "共分散の不等式と和の分散の最大・最小",
  "q": r"確率変数 $X,\ Y$ の期待値をそれぞれ $m_1,\ m_2$，標準偏差をそれぞれ $\sigma_1,\ \sigma_2$（ともに正）とし、$C=E\bigl((X-m_1)(Y-m_2)\bigr)$ とおく。ただし、$X$ と $Y$ は独立とは限らない。<br>"
       r"(1) $V(X+Y)=\sigma_1^2+\sigma_2^2+2C$ を示せ。<br>(2) $|C|\leqq\sigma_1\sigma_2$ を示せ。<br>(3) $V(X)=4$，$V(Y)=9$ を満たす確率変数 $X,\ Y$ の組をすべて考えるとき、$V(X+Y)$ の最大値と最小値を求めよ。",
  "hint": r"(2) は「分散は負にならない」ことを、実数 $t$ を含む確率変数 $tX+Y$ に用いる。$V(tX+Y)$ は $t$ の $2$ 次式で、すべての $t$ で $0$ 以上だから判別式が $0$ 以下になる。(3) は (1)(2) で範囲を絞り、等号が成り立つ $X,\ Y$ を具体的に作って最大・最小を確定させる。",
  "sol": r"(1) $E(X+Y)=m_1+m_2$ だから、期待値の和の性質を用いて<br>"
         r"$V(X+Y)=E\bigl(\{(X-m_1)+(Y-m_2)\}^2\bigr)$<br>"
         r"$\qquad=E\bigl((X-m_1)^2\bigr)+2E\bigl((X-m_1)(Y-m_2)\bigr)+E\bigl((Y-m_2)^2\bigr)=\sigma_1^2+\sigma_2^2+2C$<br>"
         r"(2) $t$ を実数とする。$E(tX+Y)=tm_1+m_2$ なので、(1) と同様に<br>"
         r"$V(tX+Y)=E\bigl(\{t(X-m_1)+(Y-m_2)\}^2\bigr)=\sigma_1^2t^2+2Ct+\sigma_2^2$<br>"
         r"分散は $0$ 以上の値をとる確率変数 $\{t(X-m_1)+(Y-m_2)\}^2$ の期待値だから、すべての実数 $t$ に対して<br>　$\sigma_1^2t^2+2Ct+\sigma_2^2\geqq0$<br>$\sigma_1^2\gt0$ なので、この $t$ の $2$ 次式の判別式 $D$ について $\dfrac D4=C^2-\sigma_1^2\sigma_2^2\leqq0$。よって　$|C|\leqq\sigma_1\sigma_2$<br>"
         r"(3) $\sigma_1=2$，$\sigma_2=3$ だから、(1)(2) より $V(X+Y)=13+2C$，$-6\leqq C\leqq6$。ゆえに $1\leqq V(X+Y)\leqq25$。<br>"
         r"逆に、$X$ を $2,\ -2$ をそれぞれ確率 $\dfrac12$ でとる確率変数とすると $E(X)=0$，$V(X)=4$ である。<br>"
         r"・$Y=\dfrac32X$ とすると $V(Y)=\dfrac94\cdot4=9$ で、$V(X+Y)=V\left(\dfrac52X\right)=\dfrac{25}{4}\cdot4=25$<br>"
         r"・$Y=-\dfrac32X$ とすると $V(Y)=9$ で、$V(X+Y)=V\left(-\dfrac12X\right)=\dfrac14\cdot4=1$<br>"
         r"したがって　最大値 $\boldsymbol{25}$，最小値 $\boldsymbol{1}$",
  "note": r"$r=\dfrac{C}{\sigma_1\sigma_2}$ は数学 I で学んだ相関係数と同じ形で、(2) は $-1\leqq r\leqq1$ を意味する。$X,\ Y$ が独立なら $C=E(X-m_1)E(Y-m_2)=0$ となり、$V(X+Y)=V(X)+V(Y)$ が得られる。また (1)(2) から $\sigma(X+Y)\leqq\sigma_1+\sigma_2$（標準偏差の三角不等式）も導ける。",
  "ex": r"確率変数 $X,\ Y,\ W$ の期待値を $m_1,\ m_2,\ m_3$ とする。$X,\ Y,\ W$ の分散がいずれも $1$ で、$E\bigl((X-m_1)(Y-m_2)\bigr)=E\bigl((Y-m_2)(W-m_3)\bigr)=E\bigl((W-m_3)(X-m_1)\bigr)=c$ であるとき、$c\geqq-\dfrac12$ であることを示せ。",
  "exa": r"(1) と同様に $V(X+Y+W)=1+1+1+2(c+c+c)=3+6c$。これが $0$ 以上であることから $c\geqq-\dfrac12$"},
]})

# ---------------------------------------------------------------- 節3
SEC.append({"title": "二項分布",
"base": r"""・$1$ 回の試行で事象 $A$ の起こる確率が $p$ のとき、この試行を $n$ 回繰り返して $A$ の起こる回数 $X$ の分布を二項分布 $B(n,\ p)$ という：$P(X=k)={}_n\mathrm{C}_kp^kq^{n-k}$（$k=0,\ 1,\ \cdots,\ n$，$q=1-p$）<br>
・$E(X)=np$，$V(X)=npq$，$\sigma(X)=\sqrt{npq}$<br>
・$i$ 回目に $A$ が起これば $1$、起こらなければ $0$ をとる $X_i$ を用いると $X=X_1+\cdots+X_n$（$X_i$ は互いに独立で $E(X_i)=p$，$V(X_i)=pq$）""",
"items": [
 {"lv": 1, "title": "二項分布の確率・期待値・分散",
  "q": r"$1$ 個のさいころを $5$ 回投げるとき、$3$ の倍数の目が出る回数を $X$ とする。<br>(1) $P(X=2)$ を求めよ。<br>(2) $X$ の期待値・分散・標準偏差を求めよ。",
  "hint": r"各回で $3$ の倍数の目（$3,\ 6$）が出る確率は $\dfrac13$ で、$5$ 回の試行は独立だから、$X$ は二項分布 $B\left(5,\ \dfrac13\right)$ に従う。",
  "sol": r"$X$ は二項分布 $B\left(5,\ \dfrac13\right)$ に従う。<br>"
         r"(1) $P(X=2)={}_5\mathrm{C}_2\left(\dfrac13\right)^2\left(\dfrac23\right)^3=10\cdot\dfrac19\cdot\dfrac{8}{27}=\boldsymbol{\dfrac{80}{243}}$<br>"
         r"(2) $E(X)=5\cdot\dfrac13=\boldsymbol{\dfrac53}$，$V(X)=5\cdot\dfrac13\cdot\dfrac23=\boldsymbol{\dfrac{10}{9}}$，$\sigma(X)=\sqrt{\dfrac{10}{9}}=\boldsymbol{\dfrac{\sqrt{10}}{3}}$",
  "note": r"確率分布の表を作って計算しても同じ値になるが、$n$ が大きいと表を作るのは現実的でない。二項分布であることを見抜いて公式を使うのが基本である。",
  "ex": r"硬貨を $6$ 回投げるとき、表が出る回数を $X$ とする。$P(X=4)$ と、$X$ の期待値・分散・標準偏差を求めよ。",
  "exa": r"$P(X=4)=\dfrac{15}{64}$，$E(X)=3$，$V(X)=\dfrac32$，$\sigma(X)=\dfrac{\sqrt6}{2}$"},
 {"lv": 3, "title": "平均・分散からの決定と確率が最大となる値",
  "q": r"確率変数 $X$ は二項分布 $B(n,\ p)$ に従い、$E(X)=6$，$V(X)=\dfrac{21}{5}$ である。<br>(1) $n,\ p$ の値を求めよ。<br>(2) $P(X=k)$ が最大となる $k$ の値を求めよ。",
  "hint": r"(1) $np$ と $np(1-p)$ の比から $1-p$ が出る。(2) $p_k=P(X=k)$ の大小は、隣り合う項の比 $\dfrac{p_{k+1}}{p_k}$ と $1$ の大小で調べる（${}_n\mathrm{C}_k$ の比はきれいに約分できる）。",
  "sol": r"(1) $np=6$，$np(1-p)=\dfrac{21}{5}$ より $1-p=\dfrac{21}{5}\div6=\dfrac{7}{10}$。よって　$\boldsymbol{p=\dfrac{3}{10}}$，$\boldsymbol{n=20}$<br>"
         r"(2) $p_k={}_{20}\mathrm{C}_k\left(\dfrac{3}{10}\right)^k\left(\dfrac{7}{10}\right)^{20-k}$（$0\leqq k\leqq20$）とおく。$0\leqq k\leqq19$ のとき<br>"
         r"$\dfrac{p_{k+1}}{p_k}=\dfrac{{}_{20}\mathrm{C}_{k+1}}{{}_{20}\mathrm{C}_k}\cdot\dfrac{3}{7}=\dfrac{20-k}{k+1}\cdot\dfrac37=\dfrac{3(20-k)}{7(k+1)}$<br>"
         r"$\dfrac{p_{k+1}}{p_k}\gt1\iff60-3k\gt7k+7\iff k\lt5.3$ であり、$\dfrac{p_{k+1}}{p_k}=1$ となる整数 $k$ はない。<br>"
         r"よって $p_0\lt p_1\lt\cdots\lt p_5\lt p_6$，$p_6\gt p_7\gt\cdots\gt p_{20}$ となり、最大となるのは　$\boldsymbol{k=6}$",
  "note": r"一般に $B(n,\ p)$ では $(n+1)p-1\leqq k\leqq(n+1)p$ を満たす整数 $k$ で確率が最大になる（本問は $(n+1)p=6.3$）。$(n+1)p$ が整数のときは、$k=(n+1)p-1$ と $k=(n+1)p$ の $2$ つで最大になる。最大となる $k$ は期待値 $np$ のすぐ近くにある。",
  "ex": r"確率変数 $X$ は二項分布 $B(n,\ p)$ に従い、$E(X)=10$，$V(X)=\dfrac{15}{2}$ である。$n,\ p$ の値と、$P(X=k)$ が最大となる $k$ の値を求めよ。",
  "exa": r"$n=40$，$p=\dfrac14$，$k=10$"},
 {"lv": 3, "title": "二項分布の期待値・分散を定義から導く",
  "q": r"確率変数 $X$ が二項分布 $B(n,\ p)$ に従うとする（$n\geqq2$，$0\lt p\lt1$，$q=1-p$）。<br>(1) $1\leqq k\leqq n$ のとき $k\,{}_n\mathrm{C}_k=n\,{}_{n-1}\mathrm{C}_{k-1}$ が成り立つことを示し、これを用いて $E(X)=np$ を示せ。<br>(2) $E\bigl(X(X-1)\bigr)=n(n-1)p^2$ を示し、$V(X)=npq$ を導け。",
  "hint": r"二項定理 $\displaystyle\sum_{j=0}^N{}_N\mathrm{C}_jp^jq^{N-j}=(p+q)^N=1$ が使える形にするため、$k\,{}_n\mathrm{C}_k$ を ${}_{n-1}\mathrm{C}_{k-1}$ に、$k(k-1)\,{}_n\mathrm{C}_k$ を ${}_{n-2}\mathrm{C}_{k-2}$ に直す。$V(X)$ は $E(X^2)=E\bigl(X(X-1)\bigr)+E(X)$ を利用する。",
  "sol": r"(1) $k\,{}_n\mathrm{C}_k=k\cdot\dfrac{n!}{k!(n-k)!}=n\cdot\dfrac{(n-1)!}{(k-1)!(n-k)!}=n\,{}_{n-1}\mathrm{C}_{k-1}$<br>"
         r"$k=0$ の項は $0$ なので、$j=k-1$ とおいて<br>"
         r"$E(X)=\displaystyle\sum_{k=1}^nk\,{}_n\mathrm{C}_kp^kq^{n-k}=\sum_{k=1}^n n\,{}_{n-1}\mathrm{C}_{k-1}p^kq^{n-k}=np\sum_{j=0}^{n-1}{}_{n-1}\mathrm{C}_jp^jq^{n-1-j}=np(p+q)^{n-1}=np$<br>"
         r"(2) $2\leqq k\leqq n$ のとき、(1) の関係を $2$ 回用いて　$k(k-1)\,{}_n\mathrm{C}_k=(k-1)\cdot n\,{}_{n-1}\mathrm{C}_{k-1}=n(n-1)\,{}_{n-2}\mathrm{C}_{k-2}$<br>"
         r"$k=0,\ 1$ の項は $0$ なので、$j=k-2$ とおいて<br>"
         r"$E\bigl(X(X-1)\bigr)=\displaystyle\sum_{k=2}^n n(n-1)\,{}_{n-2}\mathrm{C}_{k-2}p^kq^{n-k}=n(n-1)p^2\sum_{j=0}^{n-2}{}_{n-2}\mathrm{C}_jp^jq^{n-2-j}=n(n-1)p^2(p+q)^{n-2}=n(n-1)p^2$<br>"
         r"よって　$V(X)=E(X^2)-\{E(X)\}^2=E\bigl(X(X-1)\bigr)+E(X)-\{E(X)\}^2=n(n-1)p^2+np-n^2p^2=np(1-p)=npq$",
  "note": r"基本事項のように $X=X_1+\cdots+X_n$ と独立な確率変数の和に分ければ、$E(X)=np$，$V(X)=n\cdot pq$ はすぐに得られる。また、恒等式 $(px+q)^n=\displaystyle\sum_{k=0}^n{}_n\mathrm{C}_kp^kq^{n-k}x^k$ の両辺を $x$ で微分して $x=1$ とおくと $E(X)$ が、$2$ 回微分して $x=1$ とおくと $E\bigl(X(X-1)\bigr)$ が得られる。",
  "ex": r"$n\geqq3$ のとき、$E\bigl(X(X-1)(X-2)\bigr)=n(n-1)(n-2)p^3$ を示せ。",
  "exa": r"$3\leqq k\leqq n$ で $k(k-1)(k-2)\,{}_n\mathrm{C}_k=n(n-1)(n-2)\,{}_{n-3}\mathrm{C}_{k-3}$ を用い、和を $n(n-1)(n-2)p^3(p+q)^{n-3}$ にまとめる。"},
 {"lv": 5, "title": "二項分布の和の分布と同点の確率の評価",
  "q": r"$n,\ m$ を自然数、$0\lt p\lt1$，$q=1-p$ とする。互いに独立な確率変数 $X,\ Y$ があり、$X$ は二項分布 $B(n,\ p)$ に、$Y$ は $B(m,\ p)$ に従う。<br>"
       r"(1) $X+Y$ は二項分布 $B(n+m,\ p)$ に従うことを示せ。<br>(2) $m=n$，$p=\dfrac12$ のとき、$P(X=Y)$ を $n$ で表せ。<br>"
       r"(3) (2) の確率を $a_n$ とする。すべての自然数 $n$ に対して $a_n\leqq\dfrac{1}{\sqrt{3n+1}}$ が成り立つことを示せ。",
  "hint": r"(1) $P(X+Y=k)$ を $X$ の値で場合分けして独立性を使う。現れる和 $\sum{}_n\mathrm{C}_i\,{}_m\mathrm{C}_{k-i}$ は「$n+m$ 人から $k$ 人を選ぶ方法を、一方の組から選ぶ人数で分類したもの」と読める。(2) $X=Y$ のままでは和の形にならない。$Y'=n-Y$ とおくと $X=Y\iff X+Y'=n$。(3) $\dfrac{a_{n+1}}{a_n}$ を求め、数学的帰納法で示す。",
  "sol": r"(1) $k$ を $0\leqq k\leqq n+m$ の整数とする。$X$ と $Y$ は独立だから<br>"
         r"$P(X+Y=k)=\displaystyle\sum_i P(X=i)P(Y=k-i)=\sum_i{}_n\mathrm{C}_i\,{}_m\mathrm{C}_{k-i}\,p^kq^{n+m-k}$<br>"
         r"ここで和は $0\leqq i\leqq n$，$0\leqq k-i\leqq m$ を満たす整数 $i$ についてとる。A 組 $n$ 人と B 組 $m$ 人の計 $n+m$ 人から $k$ 人を選ぶ方法は ${}_{n+m}\mathrm{C}_k$ 通りあり、これを A 組から選ぶ人数 $i$ で分類すると、それぞれ ${}_n\mathrm{C}_i\,{}_m\mathrm{C}_{k-i}$ 通りだから $\displaystyle\sum_i{}_n\mathrm{C}_i\,{}_m\mathrm{C}_{k-i}={}_{n+m}\mathrm{C}_k$。<br>"
         r"よって $P(X+Y=k)={}_{n+m}\mathrm{C}_kp^kq^{n+m-k}$ となり、$X+Y$ は $B(n+m,\ p)$ に従う。<br>"
         r"(2) $Y'=n-Y$ とおく。$j=0,\ 1,\ \cdots,\ n$ に対して $P(Y'=j)=P(Y=n-j)={}_n\mathrm{C}_{n-j}\left(\dfrac12\right)^n={}_n\mathrm{C}_j\left(\dfrac12\right)^n$ なので、$Y'$ も $B\left(n,\ \dfrac12\right)$ に従う。また $P(X=i,\ Y'=j)=P(X=i,\ Y=n-j)=P(X=i)P(Y'=j)$ より、$X$ と $Y'$ は独立である。<br>"
         r"(1) より $X+Y'$ は $B\left(2n,\ \dfrac12\right)$ に従い、$X=Y\iff X+Y'=n$ だから　$a_n=P(X+Y'=n)=\boldsymbol{\dfrac{{}_{2n}\mathrm{C}_n}{4^n}}$<br>"
         r"(3) $\dfrac{a_{n+1}}{a_n}=\dfrac{(2n+2)!}{\{(n+1)!\}^2}\cdot\dfrac{(n!)^2}{(2n)!}\cdot\dfrac14=\dfrac{(2n+2)(2n+1)}{4(n+1)^2}=\dfrac{2n+1}{2n+2}$<br>"
         r"[1] $n=1$ のとき　$a_1=\dfrac24=\dfrac12=\dfrac{1}{\sqrt4}$ で成り立つ（等号）。<br>"
         r"[2] $n=k$ のとき $a_k\leqq\dfrac1{\sqrt{3k+1}}$ と仮定すると　$a_{k+1}=\dfrac{2k+1}{2k+2}a_k\leqq\dfrac{2k+1}{(2k+2)\sqrt{3k+1}}$<br>"
         r"ここで $(2k+2)^2(3k+1)-(2k+1)^2(3k+4)=(12k^3+28k^2+20k+4)-(12k^3+28k^2+19k+4)=k\gt0$ より $\dfrac{(2k+1)^2}{(2k+2)^2(3k+1)}\lt\dfrac1{3k+4}$，すなわち $\dfrac{2k+1}{(2k+2)\sqrt{3k+1}}\lt\dfrac1{\sqrt{3k+4}}$。<br>"
         r"よって $a_{k+1}\lt\dfrac{1}{\sqrt{3(k+1)+1}}$ となり、$n=k+1$ のときも成り立つ。<br>"
         r"[1]，[2] より、すべての自然数 $n$ に対して $a_n\leqq\dfrac1{\sqrt{3n+1}}$",
  "note": r"例えば $2$ 人が公正な硬貨を $100$ 回ずつ投げて表の回数を比べると、同点になる確率は $\dfrac1{\sqrt{301}}\lt0.058$ 以下である。なお、より弱い $a_n\leqq\dfrac1{\sqrt{2n}}$ を直接帰納法で示そうとすると、$(2k+1)^2\leqq2k(2k+2)$ が必要になって失敗する。帰納法では、示す命題を少し強めたほうが仮定も強く使えて、かえってうまくいくことがある。",
  "ex": r"互いに独立な確率変数 $X,\ Y$ があり、$X$ は $B\left(n,\ \dfrac12\right)$ に、$Y$ は $B\left(n+1,\ \dfrac12\right)$ に従う。$P(X\lt Y)$ を求めよ。",
  "exa": r"$\dfrac12$（$Y'=n+1-Y$ とおくと $X+Y'$ は $B\left(2n+1,\ \dfrac12\right)$ に従い、$X\lt Y\iff X+Y'\leqq n$）"},
]})

# ---------------------------------------------------------------- 節4
def _fig_sum():
    """x+y<=t の部分（t<=1 と t>=1）を示す図"""
    s, oy, W, H = 80, 100, 240, 128
    out = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    for ox, t, cap in ((24, 0.6, "t ≦ 1 のとき"), (144, 1.4, "t ≧ 1 のとき")):
        X = lambda x: ox + s * x
        Y = lambda y: oy - s * y
        pts = [(0, 0), (t, 0), (0, t)] if t <= 1 else [(0, 0), (1, 0), (1, t - 1), (t - 1, 1), (0, 1)]
        out.append('<polygon points="' + " ".join(f"{X(a):.1f},{Y(b):.1f}" for a, b in pts) + '" fill="#cfdcf5" stroke="none"/>')
        out.append(f'<rect x="{X(0)}" y="{Y(1)}" width="{s}" height="{s}" fill="none" stroke="#333" stroke-width="1"/>')
        x0, x1 = max(-0.08, t - 1.12), min(t + 0.08, 1.12)
        out.append(f'<line x1="{X(x0):.1f}" y1="{Y(t - x0):.1f}" x2="{X(x1):.1f}" y2="{Y(t - x1):.1f}" stroke="#16367a" stroke-width="1.4"/>')
        out.append(f'<text x="{X(0) - 10}" y="{oy + 10}" font-size="10">O</text>')
        out.append(f'<text x="{X(1) - 3}" y="{oy + 11}" font-size="10">1</text>')
        out.append(f'<text x="{X(0) - 9}" y="{Y(1) + 4}" font-size="10">1</text>')
        if t <= 1:
            out.append(f'<text x="{X(t) - 3}" y="{oy + 11}" font-size="10" font-style="italic">t</text>')
            out.append(f'<text x="{X(0) - 9}" y="{Y(t) + 4}" font-size="10" font-style="italic">t</text>')
            out.append(f'<text x="{X(0.42):.1f}" y="{Y(0.42):.1f}" font-size="10" font-style="italic">x+y=t</text>')
        else:
            out.append(f'<text x="{X(t - 1) - 7:.1f}" y="{Y(1) - 3}" font-size="10" font-style="italic">t−1</text>')
        out.append(f'<text x="{X(0.5) - 24:.1f}" y="{oy + 24}" font-size="10">{cap}</text>')
    out.append("</svg>")
    return "".join(out)


SEC.append({"title": "連続型確率変数",
"base": r"""・連続型確率変数 $X$（とる値の範囲 $\alpha\leqq X\leqq\beta$）の確率密度関数 $f(x)$：<br>　$f(x)\geqq0$，$\displaystyle\int_\alpha^\beta f(x)\,dx=1$，$\displaystyle P(a\leqq X\leqq b)=\int_a^b f(x)\,dx$<br>
・$E(X)=\displaystyle\int_\alpha^\beta xf(x)\,dx=m$，$V(X)=\displaystyle\int_\alpha^\beta(x-m)^2f(x)\,dx=\int_\alpha^\beta x^2f(x)\,dx-m^2$<br>
・連続型では $P(X=a)=0$ なので、不等号に等号を含めても含めなくても確率は変わらない。""",
"items": [
 {"lv": 1, "title": "確率密度関数の決定と確率・期待値・分散",
  "q": r"確率変数 $X$ のとる値の範囲が $0\leqq X\leqq3$ で、その確率密度関数が $f(x)=ax(3-x)$（$a$ は定数）であるとする。<br>(1) $a$ の値を求めよ。<br>(2) $P(0\leqq X\leqq1)$ を求めよ。<br>(3) $E(X)$，$V(X)$ を求めよ。",
  "hint": r"全確率が $1$，すなわち $\displaystyle\int_0^3f(x)\,dx=1$ から $a$ が決まる。確率・期待値・分散はすべて定積分で計算する。",
  "sol": r"(1) $\displaystyle\int_0^3ax(3-x)\,dx=a\left[\dfrac{3}{2}x^2-\dfrac{x^3}{3}\right]_0^3=a\left(\dfrac{27}{2}-9\right)=\dfrac92a=1$ より　$\boldsymbol{a=\dfrac29}$（このとき $0\leqq x\leqq3$ で $f(x)\geqq0$）<br>"
         r"(2) $P(0\leqq X\leqq1)=\dfrac29\left[\dfrac32x^2-\dfrac{x^3}{3}\right]_0^1=\dfrac29\cdot\dfrac76=\boldsymbol{\dfrac{7}{27}}$<br>"
         r"(3) $E(X)=\dfrac29\displaystyle\int_0^3(3x^2-x^3)\,dx=\dfrac29\left[x^3-\dfrac{x^4}{4}\right]_0^3=\dfrac29\cdot\dfrac{27}{4}=\boldsymbol{\dfrac32}$<br>"
         r"$\displaystyle\int_0^3x^2f(x)\,dx=\dfrac29\int_0^3(3x^3-x^4)\,dx=\dfrac29\left[\dfrac{3}{4}x^4-\dfrac{x^5}{5}\right]_0^3=\dfrac29\cdot\dfrac{243}{20}=\dfrac{27}{10}$<br>"
         r"$V(X)=\dfrac{27}{10}-\left(\dfrac32\right)^2=\boldsymbol{\dfrac{9}{20}}$",
  "note": r"$y=f(x)$ のグラフは直線 $x=\dfrac32$ に関して対称なので、計算しなくても $E(X)=\dfrac32$ とわかる。",
  "ex": r"確率変数 $X$ のとる値の範囲が $0\leqq X\leqq2$ で、確率密度関数が $f(x)=a(2-x)$ であるとき、$a$ の値と $P(X\geqq1)$，$E(X)$，$V(X)$ を求めよ。",
  "exa": r"$a=\dfrac12$，$P(X\geqq1)=\dfrac14$，$E(X)=\dfrac23$，$V(X)=\dfrac29$"},
 {"lv": 3, "title": "条件から確率密度関数を定める・中央値",
  "q": r"確率変数 $X$ のとる値の範囲が $0\leqq X\leqq1$ で、確率密度関数が $f(x)=ax+b$（$a,\ b$ は定数）であり、$E(X)=\dfrac{7}{12}$ である。<br>(1) $a,\ b$ の値を求めよ。<br>(2) $V(X)$ を求めよ。<br>(3) $P(X\leqq t)=\dfrac12$ となる $t$ の値（$X$ の中央値）を求めよ。",
  "hint": r"全確率が $1$ であることと期待値の条件から、$a,\ b$ の連立方程式が得られる。求めた $f(x)$ が $0\leqq x\leqq1$ で $f(x)\geqq0$ を満たすことの確認を忘れない。",
  "sol": r"(1) $\displaystyle\int_0^1(ax+b)\,dx=\dfrac a2+b=1$，$\displaystyle E(X)=\int_0^1x(ax+b)\,dx=\dfrac a3+\dfrac b2=\dfrac7{12}$<br>"
         r"第 $1$ 式より $b=1-\dfrac a2$。第 $2$ 式に代入して $\dfrac a3+\dfrac12-\dfrac a4=\dfrac7{12}$，$\dfrac{a}{12}=\dfrac1{12}$。よって　$\boldsymbol{a=1,\ b=\dfrac12}$<br>"
         r"このとき $0\leqq x\leqq1$ で $f(x)=x+\dfrac12\gt0$ となり、確率密度関数の条件を満たす。<br>"
         r"(2) $\displaystyle\int_0^1x^2\left(x+\dfrac12\right)dx=\dfrac14+\dfrac16=\dfrac5{12}$ より　$V(X)=\dfrac{5}{12}-\left(\dfrac{7}{12}\right)^2=\dfrac{60-49}{144}=\boldsymbol{\dfrac{11}{144}}$<br>"
         r"(3) $0\leqq t\leqq1$ のとき $P(X\leqq t)=\displaystyle\int_0^t\left(x+\dfrac12\right)dx=\dfrac{t^2+t}{2}$。$\dfrac{t^2+t}{2}=\dfrac12$ より $t^2+t-1=0$。$0\leqq t\leqq1$ より　$t=\boldsymbol{\dfrac{\sqrt5-1}{2}}$",
  "note": r"中央値 $\dfrac{\sqrt5-1}{2}\fallingdotseq0.618$ は期待値 $\dfrac7{12}\fallingdotseq0.583$ と一致しない。また、$f(x)\geqq0$ の確認は省けない。例えば $E(X)=\dfrac34$ とすると $a=3,\ b=-\dfrac12$ となり $f(0)\lt0$ なので、そのような確率密度関数は存在しない（$f(x)=ax+b$ の形では $\dfrac13\leqq E(X)\leqq\dfrac23$ に限られる）。",
  "ex": r"確率変数 $X$ のとる値の範囲が $0\leqq X\leqq2$ で、確率密度関数が $f(x)=ax+b$ であり、$E(X)=\dfrac76$ である。$a,\ b$ の値、$V(X)$、および $P(X\leqq t)=\dfrac12$ となる $t$ の値を求めよ。",
  "exa": r"$a=b=\dfrac14$，$V(X)=\dfrac{11}{36}$，$t=\sqrt5-1$"},
 {"lv": 4, "title": "一様分布に従う確率変数の和の分布（面積の利用）",
  "q": r"確率変数 $X,\ Y$ は互いに独立で、いずれもとる値の範囲が $0$ 以上 $1$ 以下、確率密度関数が定数 $1$（一様分布）である。このとき、点 $(X,\ Y)$ が正方形 $0\leqq x\leqq1$，$0\leqq y\leqq1$ 内の領域 $D$ に入る確率は $D$ の面積に等しいとしてよい。$Z=X+Y$ とする。<br>"
       r"(1) $0\leqq t\leqq2$ に対し、$F(t)=P(Z\leqq t)$ を求めよ。<br>(2) $Z$ の確率密度関数 $g(t)$ を求め、$E(Z)$，$V(Z)$ を求めよ。",
  "hint": r"$Z\leqq t$ は、点 $(X,\ Y)$ が直線 $x+y=t$ の下側（境界を含む）にあることと同じ。$t\leqq1$ と $t\geqq1$ で図形の形が変わる。$F(b)-F(a)=\displaystyle\int_a^bg(t)\,dt$ となる $g$ が確率密度関数だから、$g(t)=F'(t)$ とすればよい。",
  "sol": _fig_sum()
         + r"(1) $0\leqq t\leqq1$ のとき、正方形のうち $x+y\leqq t$ を満たす部分は、直角をはさむ $2$ 辺の長さが $t$ の直角二等辺三角形だから　$F(t)=\boldsymbol{\dfrac{t^2}{2}}$<br>"
           r"$1\leqq t\leqq2$ のとき、正方形から直角をはさむ $2$ 辺の長さが $2-t$ の直角二等辺三角形を除いた部分だから　$F(t)=\boldsymbol{1-\dfrac{(2-t)^2}{2}}$<br>"
           r"(2) $g(t)=F'(t)$ とおくと　$g(t)=\begin{cases}t & (0\leqq t\leqq1)\\ 2-t & (1\leqq t\leqq2)\end{cases}$<br>"
           r"$g(t)\geqq0$ で、$0\leqq a\lt b\leqq2$ に対して $P(a\lt Z\leqq b)=F(b)-F(a)=\displaystyle\int_a^bg(t)\,dt$ だから、これが $Z$ の確率密度関数 $\boldsymbol{g(t)}$ である。<br>"
           r"$E(Z)=\displaystyle\int_0^1t^2\,dt+\int_1^2t(2-t)\,dt=\dfrac13+\left[t^2-\dfrac{t^3}3\right]_1^2=\dfrac13+\dfrac23=\boldsymbol{1}$<br>"
           r"$\displaystyle\int_0^2t^2g(t)\,dt=\int_0^1t^3\,dt+\int_1^2t^2(2-t)\,dt=\dfrac14+\left[\dfrac{2t^3}{3}-\dfrac{t^4}{4}\right]_1^2=\dfrac14+\dfrac{11}{12}=\dfrac76$<br>"
           r"$V(Z)=\dfrac76-1^2=\boldsymbol{\dfrac16}$",
  "note": r"$E(X)=\dfrac12$，$V(X)=\dfrac1{12}$ だから、$E(Z)=E(X)+E(Y)$，$V(Z)=V(X)+V(Y)$ が確かに成り立っている。一様分布に従う確率変数の和は一様分布ではなく、グラフが三角形の分布になる。さらに多くの独立な確率変数を加えていくと、その分布は正規分布に近づく。",
  "ex": r"同じ設定で、$X$ と $Y$ のうち小さくないほうを $W$ とする。$0\leqq t\leqq1$ に対する $P(W\leqq t)$ と、$W$ の確率密度関数、$E(W)$ を求めよ。",
  "exa": r"$P(W\leqq t)=t^2$，確率密度関数は $2t$（$0\leqq t\leqq1$），$E(W)=\dfrac23$"},
]})

# ---------------------------------------------------------------- 節5
SEC.append({"title": "正規分布",
"base": r"""・平均 $m$、標準偏差 $\sigma$ の正規分布 $N(m,\ \sigma^2)$ の確率密度関数は $f(x)=\dfrac{1}{\sqrt{2\pi}\,\sigma}e^{-\frac{(x-m)^2}{2\sigma^2}}$ で、そのグラフは直線 $x=m$ に関して対称な山形である。<br>
・$X$ が $N(m,\ \sigma^2)$ に従うとき、$Z=\dfrac{X-m}{\sigma}$ は標準正規分布 $N(0,\ 1)$ に従う（標準化）。確率は正規分布表の値 $P(0\leqq Z\leqq u)$ を用いて求める。<br>
・$X$ が二項分布 $B(n,\ p)$ に従うとき、$n$ が大きければ $X$ は近似的に正規分布 $N(np,\ npq)$ に従う（$q=1-p$）。""",
"items": [
 {"lv": 1, "title": "標準化による確率の計算",
  "q": r"確率変数 $X$ が正規分布 $N(50,\ 10^2)$ に従うとき、次の確率を求めよ。<br>(1) $P(40\leqq X\leqq65)$　　(2) $P(X\geqq70)$<br>" + zt("1", "1.5", "2"),
  "hint": r"$Z=\dfrac{X-50}{10}$ と標準化して、$X$ の範囲を $Z$ の範囲に直す。$N(0,\ 1)$ のグラフが $y$ 軸に関して対称であることと、$P(Z\geqq0)=0.5$ を使う。",
  "sol": r"$Z=\dfrac{X-50}{10}$ とおくと、$Z$ は $N(0,\ 1)$ に従う。<br>"
         r"(1) $40\leqq X\leqq65\iff-1\leqq Z\leqq1.5$ だから<br>"
         r"$P(40\leqq X\leqq65)=P(-1\leqq Z\leqq0)+P(0\leqq Z\leqq1.5)=P(0\leqq Z\leqq1)+P(0\leqq Z\leqq1.5)=0.3413+0.4332=\boldsymbol{0.7745}$<br>"
         r"(2) $X\geqq70\iff Z\geqq2$ だから　$P(X\geqq70)=0.5-P(0\leqq Z\leqq2)=0.5-0.4772=\boldsymbol{0.0228}$",
  "note": r"$P(|X-m|\leqq\sigma)\fallingdotseq0.683$，$P(|X-m|\leqq2\sigma)\fallingdotseq0.954$，$P(|X-m|\leqq3\sigma)\fallingdotseq0.997$ はよく使うので覚えておくとよい。",
  "ex": r"確率変数 $X$ が $N(60,\ 8^2)$ に従うとき、$P(52\leqq X\leqq76)$ と $P(X\geqq72)$ を求めよ。" + zt("1", "1.5", "2"),
  "exa": r"$P(52\leqq X\leqq76)=0.8185$，$P(X\geqq72)=0.0668$"},
 {"lv": 2, "title": "二項分布の正規分布による近似",
  "q": r"$1$ 個のさいころを $720$ 回投げるとき、$1$ の目が出る回数を $X$ とする。$P(110\leqq X\leqq140)$ の近似値を、正規分布による近似を用いて求めよ。" + zt("1", "2"),
  "hint": r"$X$ は二項分布 $B\left(720,\ \dfrac16\right)$ に従う。期待値と標準偏差を求め、$X$ が近似的に正規分布 $N(np,\ npq)$ に従うとみて標準化する。",
  "sol": r"$X$ は $B\left(720,\ \dfrac16\right)$ に従うから　$E(X)=720\cdot\dfrac16=120$，$\sigma(X)=\sqrt{720\cdot\dfrac16\cdot\dfrac56}=\sqrt{100}=10$<br>"
         r"$720$ は十分大きいので $X$ は近似的に $N(120,\ 10^2)$ に従い、$Z=\dfrac{X-120}{10}$ は近似的に $N(0,\ 1)$ に従う。<br>"
         r"$110\leqq X\leqq140\iff-1\leqq Z\leqq2$ だから　$P(110\leqq X\leqq140)\fallingdotseq0.3413+0.4772=\boldsymbol{0.8185}$",
  "note": r"二項分布のまま $\sum$ で正確に計算するのは現実的でないので、$n$ が大きいときは正規分布で近似する。$X$ は整数値しかとらないので、より精密には $P(109.5\leqq X\leqq140.5)$ として近似する方法（半整数補正）もある。",
  "ex": r"硬貨を $400$ 回投げるとき、表が出る回数を $X$ とする。$P(190\leqq X\leqq215)$ の近似値を求めよ。" + zt("1", "1.5"),
  "exa": r"$0.7745$"},
 {"lv": 2, "title": "割合から平均・標準偏差を求める（正規分布の逆算）",
  "q": r"ある試験の得点 $X$ は正規分布 $N(m,\ \sigma^2)$ に従うとみなせる。受験者のうち、$80$ 点以上の者は $2.28\%$，$50$ 点以下の者は $15.87\%$ であった。<br>(1) $m,\ \sigma$ を求めよ。<br>(2) 受験者 $1000$ 人のうち上位 $100$ 人に入るには、およそ何点以上とればよいか。整数で答えよ。<br>" + zt("1", "1.28", "2"),
  "hint": r"割合を標準正規分布の確率に直し、正規分布表から $\dfrac{80-m}{\sigma}$，$\dfrac{50-m}{\sigma}$ の値を読み取る。(2) は $P(Z\geqq u)=0.1$ となる $u$ を表から逆に読む。",
  "sol": r"$Z=\dfrac{X-m}{\sigma}$ は $N(0,\ 1)$ に従う。<br>"
         r"(1) $P(Z\geqq2)=0.5-0.4772=0.0228$，$P(Z\leqq-1)=0.5-0.3413=0.1587$ だから　$\dfrac{80-m}{\sigma}=2$，$\dfrac{50-m}{\sigma}=-1$<br>"
         r"すなわち $80-m=2\sigma$，$m-50=\sigma$。辺々加えて $30=3\sigma$ より　$\boldsymbol{\sigma=10,\ m=60}$<br>"
         r"(2) 上位 $100$ 人は全体の $10\%$ だから、$P(Z\geqq u)=0.1$，すなわち $P(0\leqq Z\leqq u)=0.4$ となる $u$ を求めると $u\fallingdotseq1.28$。<br>"
         r"$X=60+10Z$ で、$Z\geqq1.28\iff X\geqq72.8$ だから、およそ $\boldsymbol{73}$ 点以上とればよい。",
  "note": r"「$80$ 点以上が $2.28\%$」と聞いたら、直ちに「$80$ 点は平均より $2\sigma$ 上」と読めるようにしておくとよい。$1\sigma$，$2\sigma$ に対応する $15.87\%$，$2.28\%$ は頻出である。",
  "ex": r"確率変数 $X$ が $N(m,\ \sigma^2)$ に従い、$P(X\geqq78)=0.0668$，$P(X\leqq50)=0.0228$ である。$m,\ \sigma$ と $P(X\geqq74)$ を求めよ。" + zt("1", "1.5", "2"),
  "exa": r"$m=66$，$\sigma=8$，$P(X\geqq74)=0.1587$"},
 {"lv": 4, "title": "独立な正規分布に従う確率変数の和",
  "q": r"ある製品 $1$ 個の重さ（g）は正規分布 $N(200,\ 2^2)$ に、これを詰める箱の重さ（g）は $N(100,\ 8^2)$ に従う。製品 $9$ 個を $1$ 箱に詰めたときの総重量を $W$（g）とする。ただし、製品・箱の重さはすべて互いに独立とし、「互いに独立な確率変数 $X,\ Y$ がそれぞれ正規分布に従うとき、$aX+bY$（$a,\ b$ は定数）も正規分布に従う」ことを用いてよい。<br>"
       r"(1) $W$ の期待値と標準偏差を求めよ。<br>(2) $P(W\geqq1920)$ を求めよ。<br>(3) 箱の重さの標準偏差だけを $s$（g）に変える（$s\gt0$，箱の重さの平均は $100$ のまま）。$P(W\geqq1920)\leqq0.0062$ となるような $s$ の値の範囲を求めよ。<br>" + zt("2", "2.5"),
  "hint": r"$W=X_1+\cdots+X_9+B$ と独立な確率変数の和で表す。期待値は和になり、分散も（独立なので）和になる。「$9X_1+B$」と取り違えないこと。",
  "sol": r"製品の重さを $X_1,\ \cdots,\ X_9$，箱の重さを $B$ とすると $W=X_1+\cdots+X_9+B$ で、これらは互いに独立である。<br>"
         r"(1) $E(W)=9\cdot200+100=\boldsymbol{1900}$，$V(W)=9\cdot2^2+8^2=100$ より　$\sigma(W)=\boldsymbol{10}$<br>"
         r"(2) 与えられた性質を繰り返し用いると、$W$ は $N(1900,\ 10^2)$ に従う。$Z=\dfrac{W-1900}{10}$ とおくと<br>"
         r"$P(W\geqq1920)=P(Z\geqq2)=0.5-0.4772=\boldsymbol{0.0228}$<br>"
         r"(3) $V(W)=36+s^2$ となり、$W$ は $N(1900,\ 36+s^2)$ に従うから　$P(W\geqq1920)=P\left(Z\geqq\dfrac{20}{\sqrt{36+s^2}}\right)$<br>"
         r"$P(Z\geqq2.5)=0.5-0.4938=0.0062$ で、$P(Z\geqq u)$ は $u$ が大きいほど小さいから、条件は $\dfrac{20}{\sqrt{36+s^2}}\geqq2.5$，すなわち $\sqrt{36+s^2}\leqq8$，$s^2\leqq28$。<br>"
         r"$s\gt0$ より　$\boldsymbol{0\lt s\leqq2\sqrt7}$",
  "note": r"もし製品 $1$ 個の重さを $9$ 倍したもの $9X_1+B$ なら、分散は $81\cdot2^2+8^2=388$ と大きくなる。独立な $9$ 個の和では、それぞれのばらつきが打ち消し合うため分散は $9$ 倍（標準偏差は $3$ 倍）にしかならない。標本平均の標準偏差が $\dfrac{\sigma}{\sqrt n}$ になるのも同じ理由である。",
  "ex": r"A さん、B さんの通学時間（分）はそれぞれ正規分布 $N(30,\ 3^2)$，$N(32,\ 4^2)$ に従い、互いに独立である。ある日、A さんの通学時間が B さんより短い確率を求めよ。ただし、例題と同じ性質を用いてよく、$Z$ を標準正規分布に従う確率変数として $P(0\leqq Z\leqq0.4)=0.1554$ とする。",
  "exa": r"$0.6554$（B さんの時間から A さんの時間を引いた差は $N(2,\ 5^2)$ に従う）"},
]})

# ---------------------------------------------------------------- 節6
SEC.append({"title": "標本平均の分布と推定",
"base": r"""・母平均 $m$，母標準偏差 $\sigma$ の母集団から大きさ $n$ の無作為標本を（復元）抽出するとき、標本平均 $\overline{X}$ について<br>
　$E(\overline{X})=m$，$\sigma(\overline{X})=\dfrac{\sigma}{\sqrt n}$　（$n$ が大きいとき、$\overline{X}$ は近似的に $N\left(m,\ \dfrac{\sigma^2}{n}\right)$ に従う）<br>
・母平均の推定（信頼度 $95\%$）：$\sigma$ が不明なら、$n$ が大きいとき標本の標準偏差で代用する。<br>
　$\overline{X}-1.96\cdot\dfrac{\sigma}{\sqrt n}\leqq m\leqq\overline{X}+1.96\cdot\dfrac{\sigma}{\sqrt n}$<br>
・母比率の推定（信頼度 $95\%$）：標本比率を $R$ として<br>
　$R-1.96\sqrt{\dfrac{R(1-R)}{n}}\leqq p\leqq R+1.96\sqrt{\dfrac{R(1-R)}{n}}$<br>
・$P(0\leqq Z\leqq1.96)=0.475$，$P(0\leqq Z\leqq2.58)=0.495$ より、信頼度 $95\%$，$99\%$ ではそれぞれ係数 $1.96$，$2.58$ を用いる。""",
"items": [
 {"lv": 1, "title": "母集団分布と標本平均の期待値・標準偏差",
  "q": r"$1,\ 2,\ 3,\ 4$ の数字を書いたカードが、それぞれ $1$ 枚、$2$ 枚、$3$ 枚、$4$ 枚の計 $10$ 枚ある。これを母集団とし、カードの数字を変量とする。<br>(1) 母平均 $m$ と母標準偏差 $\sigma$ を求めよ。<br>(2) この母集団から復元抽出で大きさ $100$ の標本を抽出するとき、標本平均 $\overline{X}$ の期待値と標準偏差を求めよ。<br>(3) (2) のとき、$P(\overline{X}\geqq3.15)$ の近似値を求めよ。" + zt("1.5"),
  "hint": r"母集団から $1$ 枚取り出したときの数字の分布（母集団分布）の期待値・標準偏差が、母平均・母標準偏差である。標本平均には公式 $E(\overline{X})=m$，$\sigma(\overline{X})=\dfrac{\sigma}{\sqrt n}$ を使い、(3) は正規分布で近似する。",
  "sol": r"(1) 母集団分布は次の表のようになる。"
         + tb([r"$X$", "$1$", "$2$", "$3$", "$4$", "計"],
              [r"$P$", r"$\dfrac{1}{10}$", r"$\dfrac{2}{10}$", r"$\dfrac{3}{10}$", r"$\dfrac{4}{10}$", "$1$"])
         + r"$m=\dfrac{1\cdot1+2\cdot2+3\cdot3+4\cdot4}{10}=\boldsymbol{3}$，$\dfrac{1^2\cdot1+2^2\cdot2+3^2\cdot3+4^2\cdot4}{10}=10$ より $\sigma^2=10-3^2=1$，$\boldsymbol{\sigma=1}$<br>"
           r"(2) $E(\overline{X})=m=\boldsymbol{3}$，$\sigma(\overline{X})=\dfrac{1}{\sqrt{100}}=\boldsymbol{\dfrac{1}{10}}$<br>"
           r"(3) $n=100$ は大きいので、$\overline{X}$ は近似的に $N\left(3,\ \left(\dfrac1{10}\right)^2\right)$ に従う。$Z=10(\overline{X}-3)$ とおくと $\overline{X}\geqq3.15\iff Z\geqq1.5$ だから<br>"
           r"$P(\overline{X}\geqq3.15)\fallingdotseq0.5-0.4332=\boldsymbol{0.0668}$",
  "note": r"母集団分布が正規分布でなくても、$n$ が大きければ標本平均は近似的に正規分布に従う。$\sigma(\overline{X})$ は $\sqrt n$ に反比例するので、ばらつきを半分にするには標本の大きさを $4$ 倍にする必要がある。",
  "ex": r"$0$ を書いたカードが $1$ 枚、$1$ を書いたカードが $2$ 枚、$2$ を書いたカードが $1$ 枚ある。これを母集団として復元抽出で大きさ $50$ の標本をとるとき、標本平均 $\overline{X}$ の期待値と標準偏差、および $P(\overline{X}\leqq0.8)$ の近似値を求めよ。" + zt("2"),
  "exa": r"$E(\overline{X})=1$，$\sigma(\overline{X})=\dfrac1{10}$，$P(\overline{X}\leqq0.8)\fallingdotseq0.0228$"},
 {"lv": 2, "title": "母平均の推定",
  "q": r"ある工場で製造された電池から $400$ 個を無作為抽出して寿命を調べたところ、平均値は $52.3$ 時間、標準偏差は $8.0$ 時間であった。この工場で製造された電池全体の寿命の平均 $m$ を、信頼度 $95\%$ で推定せよ。ただし、小数第 $2$ 位を四捨五入して答えよ。",
  "hint": r"標本の大きさ $400$ は大きいので、母標準偏差の代わりに標本の標準偏差 $8.0$ を用いてよい。$\overline{X}\pm1.96\cdot\dfrac{\sigma}{\sqrt n}$ を計算する。",
  "sol": r"標本の大きさ $n=400$ は大きいので、母標準偏差を標本の標準偏差 $8.0$ で代用すると<br>　$1.96\cdot\dfrac{8.0}{\sqrt{400}}=1.96\cdot0.4=0.784$<br>"
         r"よって $52.3-0.784\leqq m\leqq52.3+0.784$，すなわち $51.516\leqq m\leqq53.084$。<br>"
         r"小数第 $2$ 位を四捨五入して　$\boldsymbol{[51.5,\ 53.1]}$（単位は時間）",
  "note": r"「信頼度 $95\%$」とは、標本のとり方を変えて同じ方法で区間を何度も作ると、そのうち約 $95\%$ が $m$ を含むという意味である。$m$ は定数なので、「$m$ がこの区間に入る確率が $95\%$」という言い方は正確ではない。信頼度 $99\%$ なら係数 $2.58$ を用い、区間は広くなる。",
  "ex": r"ある地域の高校 $2$ 年生男子から $100$ 人を無作為抽出して身長を測ったところ、平均値 $168.2$ cm、標準偏差 $6.0$ cm であった。この地域の高校 $2$ 年生男子全体の平均身長を、信頼度 $95\%$ で推定せよ（小数第 $2$ 位を四捨五入）。",
  "exa": r"$[167.0,\ 169.4]$（cm）"},
 {"lv": 2, "title": "母比率の推定",
  "q": r"ある市の有権者から無作為に $400$ 人を選んで調査したところ、ある政策に賛成の人は $160$ 人であった。この市の有権者全体の賛成率 $p$ を、信頼度 $95\%$ で推定せよ。ただし、$\sqrt6=2.449$ とし、小数第 $3$ 位を四捨五入して答えよ。",
  "hint": r"標本比率 $R=0.4$ を用いて $\sqrt{\dfrac{R(1-R)}{n}}$ を計算し、$R\pm1.96\sqrt{\dfrac{R(1-R)}{n}}$ を求める。",
  "sol": r"標本比率は　$R=\dfrac{160}{400}=0.4$<br>"
         r"$\sqrt{\dfrac{R(1-R)}{n}}=\sqrt{\dfrac{0.4\cdot0.6}{400}}=\dfrac{\sqrt{0.24}}{20}=\dfrac{\sqrt6}{100}=0.02449$<br>"
         r"$1.96\cdot0.02449=0.0480$ なので　$0.4-0.0480\leqq p\leqq0.4+0.0480$<br>"
         r"小数第 $3$ 位を四捨五入して　$\boldsymbol{[0.35,\ 0.45]}$",
  "note": r"母比率の推定は、標本中の賛成者数 $X$ が二項分布 $B(n,\ p)$ に従い、$R=\dfrac Xn$ が近似的に $N\left(p,\ \dfrac{p(1-p)}{n}\right)$ に従うことに基づく。$p$ は未知なので、標準偏差の中の $p$ を $R$ で置き換えている。",
  "ex": r"ある工場の製品から $900$ 個を無作為抽出したところ、$270$ 個が規格を満たしていた。製品全体で規格を満たすものの割合を、信頼度 $95\%$ で推定せよ。ただし、$\sqrt{21}=4.583$ とし、小数第 $3$ 位を四捨五入せよ。",
  "exa": r"$[0.27,\ 0.33]$"},
 {"lv": 3, "title": "推定の精度と必要な標本の大きさ",
  "q": r"ある製品の不良率 $p$ を信頼度 $95\%$ で推定するとき、信頼区間の幅を $0.04$ 以下にしたい。<br>(1) 不良率はおよそ $0.2$ であることがわかっている。標本比率を $0.2$ とみなすとき、標本の大きさ $n$ を少なくともいくらにすればよいか。<br>(2) 不良率の見当がまったくつかないとき、標本比率 $R$ がどんな値になっても信頼区間の幅が $0.04$ 以下となるようにするには、$n$ を少なくともいくらにすればよいか。",
  "hint": r"信頼区間の幅は $2\times1.96\sqrt{\dfrac{R(1-R)}{n}}$。(2) は $R(1-R)$ の最大値を考え、最も不利な場合でも条件を満たすようにする。",
  "sol": r"信頼区間の幅は $2\cdot1.96\sqrt{\dfrac{R(1-R)}{n}}$ なので、条件は $3.92\sqrt{\dfrac{R(1-R)}{n}}\leqq0.04$<br>"
         r"すなわち　$\sqrt n\geqq98\sqrt{R(1-R)}$ …… ①<br>"
         r"(1) $R=0.2$ のとき $\sqrt{R(1-R)}=\sqrt{0.16}=0.4$ だから、① は $\sqrt n\geqq39.2$，$n\geqq1536.64$。<br>"
         r"よって、$n$ は $\boldsymbol{1537}$ 以上にすればよい。<br>"
         r"(2) $R(1-R)=\dfrac14-\left(R-\dfrac12\right)^2\leqq\dfrac14$ で、等号は $R=\dfrac12$ のとき成り立つ。<br>"
         r"よって ① がどんな $R$ でも成り立つ条件は　$\sqrt n\geqq98\cdot\dfrac12=49$，$n\geqq2401$<br>"
         r"$n$ は $\boldsymbol{2401}$ 以上にすればよい。",
  "note": r"母平均の推定でも同様で、幅 $2\cdot1.96\cdot\dfrac{\sigma}{\sqrt n}$ を $\dfrac1k$ にするには $n$ を $k^2$ 倍にしなければならない。(2) のように「最も不利な場合」で考えるのは、事前の情報がないときの標準的な方針である。",
  "ex": r"母比率 $p$ を信頼度 $95\%$ で推定するとき、信頼区間の幅を $0.06$ 以下にしたい。(1) 標本比率を $0.3$ とみなすとき、(2) 標本比率がどんな値でもよいようにするとき、それぞれ標本の大きさは少なくともいくらにすればよいか。ただし、$\sqrt{0.21}=0.4583$ とする。",
  "exa": r"(1) $897$　(2) $1068$"},
 {"lv": 5, "title": "チェビシェフの不等式と大数の法則",
  "q": r"(1) 確率変数 $X$ のとる値が $x_1,\ x_2,\ \cdots,\ x_r$ で、$E(X)=m$，$V(X)=\sigma^2$ とする。任意の正の数 $c$ に対して<br>"
       r"　$P(|X-m|\geqq c)\leqq\dfrac{\sigma^2}{c^2}$<br>が成り立つことを示せ。<br>"
       r"(2) 表が出る確率が $p$（$0\lt p\lt1$）の硬貨を $n$ 回投げ、表が出た回数の割合を $R$ とする。$p$ の値によらず<br>"
       r"　$P\left(|R-p|\geqq\dfrac1{20}\right)\leqq\dfrac{100}{n}$<br>が成り立つことを示せ。<br>"
       r"(3) $p$ の値によらず「$|R-p|\lt\dfrac1{20}$ となる確率が $0.99$ 以上」であることが (2) の不等式から保証されるような $n$ の最小値を求めよ。",
  "hint": r"(1) 分散の定義式 $\sum(x_k-m)^2p_k$ のうち、$|x_k-m|\geqq c$ を満たす項だけを残すと値は小さくなり、残した項では $(x_k-m)^2\geqq c^2$ である。(2) 表の回数 $X$ は $B(n,\ p)$ に従うので、$R=\dfrac Xn$ の期待値・分散がわかる。$p(1-p)\leqq\dfrac14$ で $p$ によらない評価にする。",
  "sol": r"(1) $P(X=x_k)=p_k$ とし、$|x_k-m|\geqq c$ を満たす $k$ 全体の集合を $A$ とすると　$P(|X-m|\geqq c)=\displaystyle\sum_{k\in A}p_k$<br>"
         r"各項が $0$ 以上であることと、$k\in A$ では $(x_k-m)^2\geqq c^2$ であることから<br>"
         r"$\sigma^2=\displaystyle\sum_{k=1}^r(x_k-m)^2p_k\geqq\sum_{k\in A}(x_k-m)^2p_k\geqq\sum_{k\in A}c^2p_k=c^2P(|X-m|\geqq c)$<br>"
         r"$c^2\gt0$ で割って　$P(|X-m|\geqq c)\leqq\dfrac{\sigma^2}{c^2}$（$A$ が空集合のときは左辺が $0$ で明らかに成り立つ）<br>"
         r"(2) 表の出た回数を $X$ とすると、$X$ は $B(n,\ p)$ に従い $R=\dfrac Xn$ だから　$E(R)=\dfrac{np}{n}=p$，$V(R)=\dfrac{np(1-p)}{n^2}=\dfrac{p(1-p)}{n}$<br>"
         r"(1) を $R$ と $c=\dfrac1{20}$ に用いると　$P\left(|R-p|\geqq\dfrac1{20}\right)\leqq\dfrac{p(1-p)}{n}\cdot400$<br>"
         r"$p(1-p)=\dfrac14-\left(p-\dfrac12\right)^2\leqq\dfrac14$ だから　$P\left(|R-p|\geqq\dfrac1{20}\right)\leqq\dfrac{100}{n}$<br>"
         r"(3) (2) より　$P\left(|R-p|\lt\dfrac1{20}\right)=1-P\left(|R-p|\geqq\dfrac1{20}\right)\geqq1-\dfrac{100}{n}$<br>"
         r"$1-\dfrac{100}{n}\geqq0.99\iff n\geqq10000$ だから、求める最小値は　$\boldsymbol{n=10000}$",
  "note": r"(2) と同様にして、任意の正の数 $\varepsilon$ に対し $P(|R-p|\geqq\varepsilon)\leqq\dfrac{1}{4n\varepsilon^2}$ となり、$n\to\infty$ のとき右辺は $0$ に近づく。すなわち、試行回数を増やせば、相対度数 $R$ が確率 $p$ に近い値をとる確率は $1$ に近づく（大数の法則）。一方、正規分布で近似すると、最も不利な $p=\dfrac12$ の場合でも $2.58\cdot\dfrac{1}{2\sqrt n}\leqq\dfrac1{20}$，すなわち $n\geqq665.64$ で足りる。チェビシェフの不等式は評価が粗いが、近似を使わず、どんな分布にも成り立つことが強みである。",
  "ex": r"さいころを $n$ 回投げ、$1$ の目が出た回数の割合を $R$ とする。(1) の不等式を用いて $P\left(\left|R-\dfrac16\right|\geqq\dfrac1{30}\right)\leqq\dfrac{125}{n}$ を示せ。また、これによって $P\left(\left|R-\dfrac16\right|\lt\dfrac1{30}\right)\geqq0.95$ が保証される $n$ の最小値を求めよ。",
  "exa": r"$V(R)=\dfrac{5}{36n}$ より右辺は $\dfrac{5}{36n}\cdot900=\dfrac{125}{n}$。最小値は $n=2500$"},
]})

# ---------------------------------------------------------------- 節7
SEC.append({"title": "仮説検定",
"base": r"""・仮説検定の手順：① 主張したいことに反する仮説（帰無仮説）を立てる　② 帰無仮説が正しいとして、観測された結果（またはそれより極端な結果）が起こる確率を調べる　③ その確率が有意水準以下である（検定に用いる値が棄却域に入る）なら帰無仮説を棄却し、主張は正しいと判断する。<br>
・有意水準 $5\%$ の棄却域（$Z$ は標準化した値）：両側検定 $|Z|\geqq1.96$，片側検定（大きい側）$Z\geqq1.645$<br>
・帰無仮説が棄却されないときは「主張が正しいとは判断できない」と結論する（帰無仮説が正しいと示されたわけではない）。""",
"items": [
 {"lv": 2, "title": "母比率の両側検定",
  "q": r"ある硬貨を $400$ 回投げたところ、表が $222$ 回出た。この硬貨は表と裏の出やすさに偏りがあると判断してよいか。有意水準 $5\%$ で検定せよ。" + zt("1.96"),
  "hint": r"「偏りがある」を主張したいので、帰無仮説は「表の出る確率は $\dfrac12$」。表の回数を正規分布で近似して標準化し、両側検定の棄却域 $|Z|\geqq1.96$ に入るか調べる。",
  "sol": r"表の出る確率を $p$ とし、帰無仮説を「$p=\dfrac12$」とする。<br>"
         r"帰無仮説が正しいとき、表の回数 $X$ は $B\left(400,\ \dfrac12\right)$ に従い　$E(X)=200$，$\sigma(X)=\sqrt{400\cdot\dfrac12\cdot\dfrac12}=10$<br>"
         r"$400$ は大きいので、$Z=\dfrac{X-200}{10}$ は近似的に $N(0,\ 1)$ に従う。有意水準 $5\%$ の棄却域は $|Z|\geqq1.96$ である。<br>"
         r"$X=222$ のとき $Z=\dfrac{222-200}{10}=2.2$ で、棄却域に入る。<br>"
         r"よって帰無仮説は棄却され、<b>偏りがあると判断してよい</b>。",
  "note": r"「偏りがある」は表が出やすい場合も出にくい場合も含むので、両側検定を用いる。$Z=2.2$ は、公正な硬貨なら $P(|Z|\geqq2.2)\fallingdotseq0.028$ の確率でしか起こらない珍しい結果ということである。",
  "ex": r"さいころを $720$ 回投げたところ、$1$ の目が $138$ 回出た。このさいころは $1$ の目の出る確率が $\dfrac16$ ではないと判断してよいか。有意水準 $5\%$ で検定せよ。",
  "exa": r"$Z=\dfrac{138-120}{10}=1.8\lt1.96$ で棄却されない。$1$ の目の出る確率が $\dfrac16$ ではないとは判断できない。"},
 {"lv": 3, "title": "母平均の片側検定",
  "q": r"ある菓子 $1$ 袋の内容量は、従来の製法では平均 $100$ g であった。新しい製法で作った袋から無作為に $64$ 袋を抽出して調べたところ、内容量の平均は $100.9$ g、標準偏差は $4$ g であった。新しい製法で平均内容量は増えたと判断してよいか。有意水準 $5\%$ で検定せよ。ただし、$Z$ を標準正規分布に従う確率変数として $P(Z\geqq1.645)=0.05$ とする。",
  "hint": r"主張は「増えた（$m\gt100$）」なので片側検定を行う。帰無仮説 $m=100$ のもとで、標本平均 $\overline{X}$ は近似的に $N\left(100,\ \dfrac{4^2}{64}\right)$ に従う（母標準偏差は標本の標準偏差で代用）。",
  "sol": r"新しい製法での母平均を $m$ とし、帰無仮説を「$m=100$」、対立仮説を「$m\gt100$」とする。<br>"
         r"帰無仮説が正しいとき、標本の大きさ $64$ は大きいので、母標準偏差を $4$ で代用すると、$\overline{X}$ は近似的に<br>"
         r"　$N\left(100,\ \left(\dfrac{4}{\sqrt{64}}\right)^2\right)$，すなわち $N(100,\ 0.5^2)$<br>に従う。"
         r"$Z=\dfrac{\overline{X}-100}{0.5}$ とおくと、有意水準 $5\%$ の棄却域は $Z\geqq1.645$ である。<br>"
         r"$\overline{X}=100.9$ のとき $Z=\dfrac{0.9}{0.5}=1.8$ で、棄却域に入る。<br>"
         r"よって帰無仮説は棄却され、<b>平均内容量は増えたと判断してよい</b>。",
  "note": r"同じデータでも、「内容量が変わった」かどうかの両側検定なら棄却域は $|Z|\geqq1.96$ で、$Z=1.8$ では棄却されない。片側検定か両側検定かは、データを見る前に主張の内容から決めておく必要がある。",
  "ex": r"従来の種の発芽率は $80\%$ であった。改良した種 $400$ 粒をまいたところ $332$ 粒が発芽した。改良によって発芽率が上がったと判断してよいか。有意水準 $5\%$ で検定せよ。ただし、$P(Z\geqq1.645)=0.05$ とする。",
  "exa": r"$Z=\dfrac{332-320}{8}=1.5\lt1.645$ で棄却されない。上がったとは判断できない。"},
 {"lv": 4, "title": "二項分布の確率を直接用いる検定と棄却域",
  "q": r"A と B があるゲームを繰り返し行う。A は「自分のほうが強い（$1$ 回のゲームで A が勝つ確率は $\dfrac12$ より大きい）」と主張している。ゲームに引き分けはなく、各回の勝敗は独立とする。<br>"
       r"(1) $10$ 回のゲームで A が $8$ 回勝った。A の主張は正しいと判断してよいか。有意水準 $5\%$ で検定せよ。<br>"
       r"(2) $10$ 回のゲームを行うとき、有意水準 $5\%$ の棄却域を「A の勝ち数 $X$ が $k$ 以上」の形で求めよ。<br>"
       r"(3) 実際には A が $1$ 回のゲームで勝つ確率が $\dfrac45$ であるとき、$10$ 回のゲームで A の勝ち数が (2) の棄却域に入る確率を、小数第 $3$ 位を四捨五入して求めよ。",
  "hint": r"回数が少ないので正規分布で近似せず、帰無仮説「A が勝つ確率は $\dfrac12$」のもとで $P(X\geqq8)$ などを二項分布で正確に計算する。主張は「大きい」なので片側検定であり、大きい側の極端な結果の確率を有意水準と比べる。",
  "sol": r"A が勝つ確率を $p$ とし、帰無仮説を「$p=\dfrac12$」とする。帰無仮説が正しいとき、A の勝ち数 $X$ は $B\left(10,\ \dfrac12\right)$ に従い　$P(X=k)=\dfrac{{}_{10}\mathrm{C}_k}{1024}$<br>"
         r"(1) $P(X\geqq8)=\dfrac{{}_{10}\mathrm{C}_8+{}_{10}\mathrm{C}_9+{}_{10}\mathrm{C}_{10}}{1024}=\dfrac{45+10+1}{1024}=\dfrac{56}{1024}\fallingdotseq0.0547$<br>"
         r"これは $0.05$ より大きいので帰無仮説は棄却されず、<b>A の主張が正しいとは判断できない</b>。<br>"
         r"(2) $P(X\geqq9)=\dfrac{10+1}{1024}=\dfrac{11}{1024}\fallingdotseq0.0107\leqq0.05$，$P(X\geqq8)\fallingdotseq0.0547\gt0.05$ であり、$P(X\geqq k)$ は $k$ が大きいほど小さい。<br>"
         r"よって $P(X\geqq k)\leqq0.05$ となる最小の $k$ は $9$ で、棄却域は　$\boldsymbol{X\geqq9}$<br>"
         r"(3) $X$ が $B\left(10,\ \dfrac45\right)$ に従うとき<br>"
         r"$P(X\geqq9)={}_{10}\mathrm{C}_9\left(\dfrac45\right)^9\cdot\dfrac15+\left(\dfrac45\right)^{10}=\left(\dfrac45\right)^9\left(2+\dfrac45\right)=\dfrac{14\cdot4^9}{5^{10}}\fallingdotseq\boldsymbol{0.38}$",
  "note": r"(3) より、A が実際にかなり強くても、$10$ 回の対戦では約 $62\%$ の確率で「強いとは判断できない」という結果になる。帰無仮説が棄却されないことは、帰無仮説が正しいことを意味しない。判断の精度を上げるには、対戦回数を増やす必要がある。",
  "ex": r"同じ設定で $12$ 回のゲームを行ったところ、A が $10$ 回勝った。有意水準 $5\%$ で、A の主張は正しいと判断してよいか。また、$12$ 回のゲームでの有意水準 $5\%$ の棄却域を「$X$ が $k$ 以上」の形で求めよ。",
  "exa": r"$P(X\geqq10)=\dfrac{79}{4096}\fallingdotseq0.019\leqq0.05$ より正しいと判断してよい。棄却域は $X\geqq10$（$P(X\geqq9)=\dfrac{299}{4096}\fallingdotseq0.073$）"},
]})

# ================================================================ END SECTIONS

CH = {"no": 17, "sections": SEC}


def _E(d):
    return sum(x * p for x, p in d.items())


def _V(d):
    m = _E(d)
    return sum((x - m) ** 2 * p for x, p in d.items())


def _dist(vals):
    """値のリスト（同様に確からしい）→ 分布 dict"""
    d = {}
    for v in vals:
        d[v] = d.get(v, 0) + Fr(1, len(vals))
    return d


def _v1():
    # 例題：赤4白3から3個
    balls = "RRRRWWW"
    d = _dist([sum(balls[i] == "R" for i in c) for c in combinations(range(7), 3)])
    assert d == {0: Fr(1, 35), 1: Fr(12, 35), 2: Fr(18, 35), 3: Fr(4, 35)}
    assert _E(d) == Fr(12, 7) and sum(x * x * p for x, p in d.items()) == Fr(24, 7) and _V(d) == Fr(24, 49)
    assert isclose(sqrt(24 / 49), 2 * sqrt(6) / 7)
    assert Fr(3 * 4, 7) == _E(d)
    # 練習：赤5白3から2個
    balls = "RRRRRWWW"
    d = _dist([sum(balls[i] == "R" for i in c) for c in combinations(range(8), 2)])
    assert _E(d) == Fr(5, 4) and _V(d) == Fr(45, 112)
    # 例題：1次変換
    d = {1: Fr(1, 16), 2: Fr(1, 4), 3: Fr(3, 8), 4: Fr(1, 4), 5: Fr(1, 16)}
    assert sum(d.values()) == 1 and _E(d) == 3 and _V(d) == 1
    assert sum(x * p for x, p in d.items()) * 16 == 48
    dy = {10 * x + 20: p for x, p in d.items()}
    assert _E(dy) == 50 and _V(dy) == 100
    assert sum(p for y, p in dy.items() if y >= 60) == Fr(5, 16)
    # 練習
    d = {0: 0.25, 1: 0.5, 2: 0.25}
    a, b = sqrt(2), -sqrt(2)
    dy = {a * x + b: p for x, p in d.items()}
    assert abs(_E(dy)) < 1e-12 and abs(_V(dy) - 1) < 1e-12
    # 例題：P(X=k)=ck
    for n in range(2, 41):
        c = Fr(2, n * (n + 1))
        d = {k: c * k for k in range(1, n + 1)}
        assert sum(d.values()) == 1
        assert _E(d) == Fr(2 * n + 1, 3) and _V(d) == Fr((n - 1) * (n + 2), 18)
        assert sum(k * k * p for k, p in d.items()) == Fr(n * (n + 1), 2)
        assert 9 * n * n + 9 * n - 2 * (4 * n * n + 4 * n + 1) == n * n + n - 2 == (n - 1) * (n + 2)
        d2 = {k: c * (n + 1 - k) for k in range(1, n + 1)}
        assert sum(d2.values()) == 1 and _E(d2) == Fr(n + 2, 3) and _V(d2) == Fr((n - 1) * (n + 2), 18)
    d = {1: Fr(1, 3), 2: Fr(2, 3)}
    assert _E(d) == Fr(5, 3) and _V(d) == Fr(2, 9) and 3 - Fr(25, 9) == Fr(2, 9)
    # 例題：最大値の期待値
    for n in range(3, 16):
        mx = [max(c) for c in combinations(range(1, n + 1), 3)]
        d = _dist(mx)
        for k in range(3, n + 1):
            assert d[k] == Fr(comb(k - 1, 2), comb(n, 3)) == Fr(3 * (k - 1) * (k - 2), n * (n - 1) * (n - 2))
            assert k * comb(k - 1, 2) == 3 * comb(k, 3) and comb(k, 3) == comb(k + 1, 4) - comb(k, 4)
        assert sum(comb(k, 3) for k in range(3, n + 1)) == comb(n + 1, 4)
        assert _E(d) == Fr(3 * (n + 1), 4) == Fr(3 * comb(n + 1, 4), comb(n, 3))
        assert _E(_dist([min(c) for c in combinations(range(1, n + 1), 3)])) == Fr(n + 1, 4)
        for r in (2, 4):
            if r <= n:
                assert _E(_dist([max(c) for c in combinations(range(1, n + 1), r)])) == Fr(r * (n + 1), r + 1)
    for n in range(2, 16):
        assert _E(_dist([min(c) for c in combinations(range(1, n + 1), 2)])) == Fr(n + 1, 3)


def _joint_rand(rng, nvar, nsupp):
    """ランダムな同時分布 {(x1,..,xk): 確率}（Fraction）"""
    pts = {}
    for _ in range(nsupp):
        key = tuple(rng.randint(-5, 6) for _ in range(nvar))
        pts[key] = pts.get(key, 0) + rng.randint(1, 9)
    tot = sum(pts.values())
    return {k: Fr(v, tot) for k, v in pts.items()}


def _EJ(J, f):
    return sum(f(*k) * p for k, p in J.items())


def _v2():
    # 例題：さいころ1個と硬貨2枚
    J = {}
    for x, c1, c2 in product(range(1, 7), (0, 1), (0, 1)):
        J[(x, c1 + c2)] = J.get((x, c1 + c2), 0) + Fr(1, 24)
    EX, EY = _EJ(J, lambda x, y: x), _EJ(J, lambda x, y: y)
    VX = _EJ(J, lambda x, y: x * x) - EX ** 2
    VY = _EJ(J, lambda x, y: y * y) - EY ** 2
    assert (EX, VX, EY, VY) == (Fr(7, 2), Fr(35, 12), 1, Fr(1, 2))
    assert _EJ(J, lambda x, y: x * x) == Fr(91, 6) and _EJ(J, lambda x, y: y * y) == Fr(3, 2)
    S = _EJ(J, lambda x, y: x + 2 * y)
    assert S == Fr(11, 2) and _EJ(J, lambda x, y: (x + 2 * y - S) ** 2) == Fr(59, 12)
    assert _EJ(J, lambda x, y: x * y) == Fr(7, 2)
    # 検討：1,2,3 から非復元
    pr = list(permutations((1, 2, 3), 2))
    assert sum(Fr(a * b, len(pr)) for a, b in pr) == Fr(11, 3)
    # 練習：さいころ2回
    J = {(x, y): Fr(1, 36) for x in range(1, 7) for y in range(1, 7)}
    S = _EJ(J, lambda x, y: 3 * x - 2 * y)
    assert S == Fr(7, 2) and _EJ(J, lambda x, y: (3 * x - 2 * y - S) ** 2) == Fr(455, 12)
    assert _EJ(J, lambda x, y: x * y) == Fr(49, 4)
    # 例題：目の種類の数
    for n in range(1, 7):
        e = Fr(sum(len(set(s)) for s in product(range(6), repeat=n)), 6 ** n)
        assert e == 6 * (1 - Fr(5, 6) ** n)
    assert 6 * (1 - Fr(25, 36)) == Fr(11, 6) == Fr(1, 6) * 1 + Fr(5, 6) * 2
    # 練習：10種類
    for n in range(1, 5):
        e = Fr(sum(len(set(s)) for s in product(range(10), repeat=n)), 10 ** n)
        assert e == 10 * (1 - Fr(9, 10) ** n)
    # 例題：一致の個数
    for n in range(2, 8):
        fx = [sum(p[i] == i for i in range(n)) for p in permutations(range(n))]
        d = _dist(fx)
        assert _E(d) == 1 and _V(d) == 1
        assert 1 + 2 * Fr(n * (n - 1), 2) * Fr(1, n * (n - 1)) == 2
    # 練習：空箱の数
    d = _dist([3 - len(set(s)) for s in product(range(3), repeat=4)])
    assert _E(d) == Fr(16, 27) and _V(d) == Fr(230, 729)
    # ★5：共分散の不等式（ランダムな同時分布で恒等式・不等式を確認）
    rng = random.Random(17)
    for _ in range(300):
        J = _joint_rand(rng, 2, rng.randint(2, 7))
        m1, m2 = _EJ(J, lambda x, y: x), _EJ(J, lambda x, y: y)
        v1 = _EJ(J, lambda x, y: (x - m1) ** 2)
        v2 = _EJ(J, lambda x, y: (y - m2) ** 2)
        C = _EJ(J, lambda x, y: (x - m1) * (y - m2))
        assert _EJ(J, lambda x, y: (x + y - m1 - m2) ** 2) == v1 + v2 + 2 * C
        t = Fr(rng.randint(-20, 20), rng.randint(1, 7))
        assert _EJ(J, lambda x, y: (t * x + y - t * m1 - m2) ** 2) == v1 * t * t + 2 * C * t + v2
        assert C * C <= v1 * v2
        if v1 > 0 and v2 > 0:  # V(X)=4, V(Y)=9 に調整して V(X+Y) が [1,25] に入る
            s1, s2 = 2 / sqrt(v1), 3 / sqrt(v2)
            val = float(4 + 9 + 2 * C * s1 * s2)
            assert 1 - 1e-9 <= val <= 25 + 1e-9
    for k in (Fr(3, 2), Fr(-3, 2)):
        J = {(2, 2 * k): Fr(1, 2), (-2, -2 * k): Fr(1, 2)}
        assert _EJ(J, lambda x, y: x * x) == 4 and _EJ(J, lambda x, y: y * y) == 9
        assert _EJ(J, lambda x, y: (x + y) ** 2) == (25 if k > 0 else 1)
    # 練習：3変数
    for _ in range(200):
        J = _joint_rand(rng, 3, rng.randint(2, 7))
        m = [_EJ(J, lambda *a, i=i: a[i]) for i in range(3)]
        cov = lambda i, j: _EJ(J, lambda *a: (a[i] - m[i]) * (a[j] - m[j]))
        assert _EJ(J, lambda *a: (sum(a) - sum(m)) ** 2) == cov(0, 0) + cov(1, 1) + cov(2, 2) + 2 * (cov(0, 1) + cov(1, 2) + cov(0, 2))


def _binom(n, p):
    return {k: comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(n + 1)}


def _v3():
    from sympy import symbols, expand, binomial as sbin, sqrt as ssqrt, Rational
    d = _binom(5, Fr(1, 3))
    assert d[2] == Fr(80, 243) and _E(d) == Fr(5, 3) and _V(d) == Fr(10, 9)
    d = _binom(6, Fr(1, 2))
    assert d[4] == Fr(15, 64) and _E(d) == 3 and _V(d) == Fr(3, 2) and isclose(sqrt(1.5), sqrt(6) / 2)
    # 平均・分散から n, p、最頻値
    for E, V, ans in ((6, Fr(21, 5), (20, Fr(3, 10), 6)), (10, Fr(15, 2), (40, Fr(1, 4), 10))):
        q = Fr(V) / E
        p = 1 - q
        n = Fr(E) / p
        assert n.denominator == 1 and (int(n), p) == ans[:2]
        d = _binom(int(n), p)
        mx = max(d.values())
        assert [k for k in d if d[k] == mx] == [ans[2]]
        assert _E(d) == E and _V(d) == V
    assert Fr(21, 5) / 6 == Fr(7, 10)
    for k in range(20):
        assert (Fr(3 * (20 - k), 7 * (k + 1)) > 1) == (k <= 5) and Fr(3 * (20 - k), 7 * (k + 1)) != 1
    # 定義から E, V（記号計算）
    P = symbols("p")
    for n in range(2, 11):
        terms = [sbin(n, k) * P ** k * (1 - P) ** (n - k) for k in range(n + 1)]
        assert expand(sum(k * t for k, t in enumerate(terms)) - n * P) == 0
        assert expand(sum(k * (k - 1) * t for k, t in enumerate(terms)) - n * (n - 1) * P ** 2) == 0
        EX2 = sum(k * k * t for k, t in enumerate(terms))
        assert expand(EX2 - (n * P) ** 2 - n * P * (1 - P)) == 0
        if n >= 3:
            assert expand(sum(k * (k - 1) * (k - 2) * t for k, t in enumerate(terms)) - n * (n - 1) * (n - 2) * P ** 3) == 0
        for k in range(1, n + 1):
            assert k * comb(n, k) == n * comb(n - 1, k - 1)
        for k in range(2, n + 1):
            assert k * (k - 1) * comb(n, k) == n * (n - 1) * comb(n - 2, k - 2)
        for k in range(3, n + 1):
            assert k * (k - 1) * (k - 2) * comb(n, k) == n * (n - 1) * (n - 2) * comb(n - 3, k - 3)
    # ★5 (1) 和の分布
    for p in (Fr(1, 3), Fr(2, 7)):
        for n in range(1, 7):
            for m in range(1, 7):
                dx, dy = _binom(n, p), _binom(m, p)
                conv = {}
                for i, a in dx.items():
                    for j, b in dy.items():
                        conv[i + j] = conv.get(i + j, 0) + a * b
                assert conv == _binom(n + m, p)
                for k in range(n + m + 1):
                    assert sum(comb(n, i) * comb(m, k - i) for i in range(max(0, k - m), min(n, k) + 1)) == comb(n + m, k)
    # (2) P(X=Y)
    h = Fr(1, 2)
    a = {}
    for n in range(1, 11):
        dx = _binom(n, h)
        a[n] = sum(dx[i] * dx[i] for i in range(n + 1))
        assert a[n] == Fr(comb(2 * n, n), 4 ** n)
    # (3) 評価
    k = symbols("k")
    assert expand((2 * k + 2) ** 2 * (3 * k + 1) - (2 * k + 1) ** 2 * (3 * k + 4) - k) == 0
    assert expand((2 * k + 2) ** 2 * (3 * k + 1) - (12 * k ** 3 + 28 * k ** 2 + 20 * k + 4)) == 0
    assert expand((2 * k + 1) ** 2 * (3 * k + 4) - (12 * k ** 3 + 28 * k ** 2 + 19 * k + 4)) == 0
    an = Fr(1, 2)
    for n in range(1, 401):
        assert an == Fr(comb(2 * n, n), 4 ** n)
        assert an * an * (3 * n + 1) <= 1 and (an * an * (3 * n + 1) == 1) == (n == 1)
        assert an * an * 2 * n <= 1
        an = an * Fr(2 * n + 1, 2 * n + 2)
    assert float(Fr(comb(200, 100), 4 ** 100)) < 1 / sqrt(301) < 0.058
    for kk in range(1, 50):
        assert (2 * kk + 1) ** 2 > 2 * kk * (2 * kk + 2)
    # 練習：P(X<Y)=1/2
    for n in range(1, 11):
        dx, dy = _binom(n, h), _binom(n + 1, h)
        assert sum(dx[i] * dy[j] for i in dx for j in dy if i < j) == Fr(1, 2)


def _v4():
    from sympy import symbols, integrate, Rational as R, solve, sqrt as ssqrt, simplify, diff
    x, a, b, t = symbols("x a b t")
    # 例題：ax(3-x)
    av = solve(integrate(a * x * (3 - x), (x, 0, 3)) - 1, a)[0]
    assert av == R(2, 9) and integrate(x * (3 - x), (x, 0, 3)) == R(9, 2)
    f = av * x * (3 - x)
    assert integrate(f, (x, 0, 1)) == R(7, 27) and R(3, 2) - R(1, 3) == R(7, 6)
    m = integrate(x * f, (x, 0, 3))
    assert m == R(3, 2) and integrate(3 * x ** 2 - x ** 3, (x, 0, 3)) == R(27, 4)
    assert integrate(3 * x ** 3 - x ** 4, (x, 0, 3)) == R(243, 20) and integrate(x * x * f, (x, 0, 3)) == R(27, 10)
    assert integrate(x * x * f, (x, 0, 3)) - m ** 2 == R(9, 20)
    # 練習：a(2-x)
    av = solve(integrate(a * (2 - x), (x, 0, 2)) - 1, a)[0]
    f = av * (2 - x)
    m = integrate(x * f, (x, 0, 2))
    assert (av, integrate(f, (x, 1, 2)), m, integrate(x * x * f, (x, 0, 2)) - m ** 2) == (R(1, 2), R(1, 4), R(2, 3), R(2, 9))
    # 例題：ax+b, E=7/12
    for (lo, hi, E, ab, V, med) in ((0, 1, R(7, 12), (1, R(1, 2)), R(11, 144), (ssqrt(5) - 1) / 2),
                                    (0, 2, R(7, 6), (R(1, 4), R(1, 4)), R(11, 36), ssqrt(5) - 1)):
        sol = solve([integrate(a * x + b, (x, lo, hi)) - 1, integrate(x * (a * x + b), (x, lo, hi)) - E], [a, b])
        assert (sol[a], sol[b]) == ab
        f = sol[a] * x + sol[b]
        assert min(f.subs(x, lo), f.subs(x, hi)) > 0
        assert simplify(integrate(x * x * f, (x, lo, hi)) - E ** 2 - V) == 0
        assert simplify(integrate(f, (x, lo, med)) - R(1, 2)) == 0 and lo <= float(med) <= hi
        roots = [r for r in solve(integrate(f, (x, lo, t)) - R(1, 2), t) if lo <= float(r) <= hi]
        assert len(roots) == 1 and simplify(roots[0] - med) == 0
    assert integrate(x * x * (x + R(1, 2)), (x, 0, 1)) == R(5, 12)
    # 検討：E=3/4 → a=3, b=-1/2、E の範囲 [1/3, 2/3]
    sol = solve([a / 2 + b - 1, a / 3 + b / 2 - R(3, 4)], [a, b])
    assert sol[a] == 3 and sol[b] == R(-1, 2)
    for av in (R(-2), R(2)):
        assert R(1, 2) + av / 12 in (R(1, 3), R(2, 3))
    # 例題：一様分布の和
    F1, F2 = t ** 2 / 2, 1 - (2 - t) ** 2 / 2
    assert F1.subs(t, 1) == F2.subs(t, 1) == R(1, 2) and F2.subs(t, 2) == 1 and F1.subs(t, 0) == 0
    g1, g2 = diff(F1, t), diff(F2, t)
    assert simplify(g1 - t) == 0 and simplify(g2 - (2 - t)) == 0
    assert integrate(g1, (t, 0, 1)) + integrate(g2, (t, 1, 2)) == 1
    E = integrate(t * g1, (t, 0, 1)) + integrate(t * g2, (t, 1, 2))
    E2 = integrate(t * t * g1, (t, 0, 1)) + integrate(t * t * g2, (t, 1, 2))
    assert E == 1 and integrate(t * (2 - t), (t, 1, 2)) == R(2, 3)
    assert integrate(t * t * (2 - t), (t, 1, 2)) == R(11, 12) and E2 == R(7, 6) and E2 - E ** 2 == R(1, 6)
    assert R(1, 12) * 2 == R(1, 6)
    # 面積の式を数値積分で確認：正方形内で x+y<=t の部分
    N = 20000
    for tv in (0.2, 0.6, 1.0, 1.4, 1.9):
        area = sum(min(max(tv - (i + 0.5) / N, 0), 1) for i in range(N)) / N
        ex = tv * tv / 2 if tv <= 1 else 1 - (2 - tv) ** 2 / 2
        assert abs(area - ex) < 1e-6
    # 練習：最大値
    Fw = t ** 2
    gw = diff(Fw, t)
    assert integrate(gw, (t, 0, 1)) == 1 and integrate(t * gw, (t, 0, 1)) == R(2, 3)
    rng = random.Random(4)
    for tv in (0.3, 0.7):
        cnt = sum(max(rng.random(), rng.random()) <= tv for _ in range(100000))
        assert abs(cnt / 100000 - tv * tv) < 0.01


def _p(u):
    """P(0<=Z<=u) を表の値（Fraction）で返す"""
    return Fr(PZ[u])


def _phi(u):
    return 0.5 * erf(u / sqrt(2))


def _binom_sum(n, p, lo, hi):
    return float(sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(lo, hi + 1)))


def _v5():
    # 正規分布表の値
    for u, v in PZ.items():
        tol = 6e-5 if len(v) == 6 else 6e-4
        assert abs(_phi(float(u)) - float(v)) < tol, u
    h = Fr(1, 2)
    # 例題：N(50,10^2)
    assert (Fr(40 - 50, 10), Fr(65 - 50, 10), Fr(70 - 50, 10)) == (-1, Fr(3, 2), 2)
    assert _p("1") + _p("1.5") == Fr("0.7745") and h - _p("2") == Fr("0.0228")
    assert round(2 * _phi(1), 3) == 0.683 and round(2 * _phi(2), 3) == 0.954 and round(2 * _phi(3), 3) == 0.997
    # 練習：N(60,8^2)
    assert (Fr(52 - 60, 8), Fr(76 - 60, 8), Fr(72 - 60, 8)) == (-1, 2, Fr(3, 2))
    assert _p("1") + _p("2") == Fr("0.8185") and h - _p("1.5") == Fr("0.0668")
    # 例題：正規近似 B(720,1/6)
    n, p = 720, Fr(1, 6)
    assert n * p == 120 and n * p * (1 - p) == 100
    assert (Fr(110 - 120, 10), Fr(140 - 120, 10)) == (-1, 2)
    assert abs(_binom_sum(n, p, 110, 140) - 0.8185) < 0.03
    # 練習：B(400,1/2)
    assert 400 * h == 200 and 400 * h * h == 100 and (Fr(190 - 200, 10), Fr(215 - 200, 10)) == (-1, Fr(3, 2))
    assert _p("1") + _p("1.5") == Fr("0.7745") and abs(_binom_sum(400, h, 190, 215) - 0.7745) < 0.03
    # 例題：逆算
    assert h - _p("2") == Fr("0.0228") and h - _p("1") == Fr("0.1587")
    sig = Fr(80 - 50, 3)
    m = 50 + sig
    assert (sig, m) == (10, 60) and (80 - m) / sig == 2 and (50 - m) / sig == -1
    assert abs(float(_p("1.28")) - 0.4) < 5e-4 and round(60 + 1.28 * 10) == 73 and isclose(60 + 1.28 * 10, 72.8)
    # 練習：78 で 1.5σ 上、50 で 2σ 下
    assert h - _p("1.5") == Fr("0.0668") and h - _p("2") == Fr("0.0228")
    sig = Fr(78 - 50, Fr(7, 2))
    m = 50 + 2 * sig
    assert (sig, m) == (8, 66) and (78 - m) / sig == Fr(3, 2) and (74 - m) / sig == 1 and h - _p("1") == Fr("0.1587")
    # 例題：独立な正規分布の和
    assert 9 * 200 + 100 == 1900 and 9 * 4 + 64 == 100 and Fr(1920 - 1900, 10) == 2
    assert h - _p("2.5") == Fr("0.0062")
    assert isclose(20 / sqrt(36 + 28), 2.5) and isclose(sqrt(28), 2 * sqrt(7))
    for s in (0.5, 3.0, 5.29, 2 * sqrt(7) - 1e-9):
        assert 20 / sqrt(36 + s * s) >= 2.5
    for s in (2 * sqrt(7) + 1e-6, 6.0):
        assert 20 / sqrt(36 + s * s) < 2.5
    assert 81 * 4 + 64 == 388
    # 練習：B-A ~ N(2, 5^2)
    assert 9 + 16 == 25 and Fr(0 - 2, 5) == Fr(-2, 5) and h + _p("0.4") == Fr("0.6554")


def _r(x, nd):
    """10進の四捨五入（Fraction）"""
    q = Fr(x) * 10 ** nd
    return Fr(int(q + Fr(1, 2)), 10 ** nd)


def _v6():
    h = Fr(1, 2)
    # 例題：母集団 1,2,2,3,3,3,4,4,4,4
    pop = [1] * 1 + [2] * 2 + [3] * 3 + [4] * 4
    d = _dist(pop)
    assert _E(d) == 3 and sum(x * x * p for x, p in d.items()) == 10 and _V(d) == 1
    assert Fr(1, 10) ** 2 == _V(d) / 100 and (Fr("3.15") - 3) * 10 == Fr(3, 2) and h - _p("1.5") == Fr("0.0668")
    # 練習：0,1,1,2
    d = _dist([0, 1, 1, 2])
    assert _E(d) == 1 and _V(d) == h and _V(d) / 50 == Fr(1, 100) and (Fr("0.8") - 1) * 10 == -2
    assert h - _p("2") == Fr("0.0228")
    # 母平均の推定
    w = Fr("1.96") * 8 / 20
    assert w == Fr("0.784") and (Fr("52.3") - w, Fr("52.3") + w) == (Fr("51.516"), Fr("53.084"))
    assert (_r(Fr("52.3") - w, 1), _r(Fr("52.3") + w, 1)) == (Fr("51.5"), Fr("53.1"))
    w = Fr("1.96") * 6 / 10
    assert (_r(Fr("168.2") - w, 1), _r(Fr("168.2") + w, 1)) == (Fr("167.0"), Fr("169.4"))
    # 母比率の推定
    assert isclose(sqrt(0.24) / 20, sqrt(6) / 100) and abs(sqrt(6) - 2.449) < 5e-4
    w = Fr("1.96") * Fr("0.02449")
    assert _r(w, 4) == Fr("0.0480")
    assert (_r(Fr("0.4") - w, 2), _r(Fr("0.4") + w, 2)) == (Fr("0.35"), Fr("0.45"))
    w2 = 1.96 * sqrt(0.24 / 400)
    assert (round(0.4 - w2, 2), round(0.4 + w2, 2)) == (0.35, 0.45)
    assert abs(sqrt(21) - 4.583) < 5e-4 and isclose(sqrt(0.21 / 900), sqrt(21) / 300)
    w = Fr("1.96") * Fr("4.583") / 300
    assert (_r(Fr("0.3") - w, 2), _r(Fr("0.3") + w, 2)) == (Fr("0.27"), Fr("0.33"))
    # 標本の大きさ
    c = Fr("3.92") / Fr("0.04")
    assert c == 98 and c * Fr("0.4") == Fr("39.2") and (c * Fr("0.4")) ** 2 == Fr("1536.64")
    nmin = lambda bound: int(bound) + (0 if Fr(int(bound)) == bound else 1)
    assert nmin(c * c * Fr("0.16")) == 1537 and nmin(c * c / 4) == 2401
    for n, ok in ((1536, False), (1537, True)):
        assert (3.92 * sqrt(0.16 / n) <= 0.04) == ok
    for n, ok in ((2400, False), (2401, True)):
        assert (Fr("3.92") ** 2 * Fr(1, 4) / n <= Fr("0.04") ** 2) == ok
    c = Fr("3.92") / Fr("0.06")
    assert nmin(c * c * Fr("0.21")) == 897 and nmin((c * Fr("0.4583")) ** 2) == 897 and nmin(c * c / 4) == 1068
    # ★5 チェビシェフ
    rng = random.Random(26)
    for _ in range(300):
        J = _joint_rand(rng, 1, rng.randint(1, 8))
        d = {k[0]: p for k, p in J.items()}
        m, V = _E(d), _V(d)
        for cc in (Fr(1, 2), Fr(1), Fr(3, 2), Fr(2), Fr(7, 2)):
            assert sum(p for x, p in d.items() if abs(x - m) >= cc) <= V / cc ** 2
    for n in (10, 40, 100, 300, 1000):
        for p in (Fr(1, 10), Fr(3, 10), Fr(1, 2), Fr(77, 100)):
            dd = _binom(n, p)
            prob = sum(q for k, q in dd.items() if abs(Fr(k, n) - p) >= Fr(1, 20))
            assert prob <= p * (1 - p) / n * 400 <= Fr(100, n)
            assert _E({Fr(k, n): q for k, q in dd.items()}) == p and _V({Fr(k, n): q for k, q in dd.items()}) == p * (1 - p) / n
    assert 1 - Fr(100, 10000) == Fr(99, 100) and 1 - Fr(100, 9999) < Fr(99, 100)
    assert isclose((2.58 / 2 * 20) ** 2, 665.64)
    # 練習：さいころ
    for n in (30, 600, 2500):
        V = Fr(1, 6) * Fr(5, 6) / n
        assert V == Fr(5, 36 * n) and V * 900 == Fr(125, n)
    assert 1 - Fr(125, 2500) == Fr(95, 100) and 1 - Fr(125, 2499) < Fr(95, 100)


def _v7():
    h = Fr(1, 2)
    # 両側検定
    assert 400 * h == 200 and 400 * h * h == 100 and Fr(222 - 200, 10) == Fr("2.2") > Fr("1.96")
    assert abs(2 * (0.5 - _phi(2.2)) - 0.028) < 5e-4
    assert 720 * Fr(1, 6) == 120 and 720 * Fr(1, 6) * Fr(5, 6) == 100 and Fr(138 - 120, 10) == Fr("1.8") < Fr("1.96")
    # 片側検定
    assert abs((0.5 - _phi(1.645)) - 0.05) < 1e-4
    assert Fr(4) / 8 == h and (Fr("100.9") - 100) / h == Fr("1.8") and Fr("1.645") <= Fr("1.8") < Fr("1.96")
    assert 400 * Fr(8, 10) == 320 and 400 * Fr(8, 10) * Fr(2, 10) == 64 and Fr(332 - 320, 8) == Fr("1.5") < Fr("1.645")
    # 二項分布による検定
    d = _binom(10, h)
    tail = lambda dd, k: sum(q for j, q in dd.items() if j >= k)
    assert tail(d, 8) == Fr(56, 1024) and tail(d, 9) == Fr(11, 1024)
    assert round(float(tail(d, 8)), 4) == 0.0547 and round(float(tail(d, 9)), 4) == 0.0107
    assert min(k for k in range(11) if tail(d, k) <= Fr(5, 100)) == 9
    assert comb(10, 8) + comb(10, 9) + comb(10, 10) == 56
    d8 = _binom(10, Fr(4, 5))
    pw = tail(d8, 9)
    assert pw == Fr(4, 5) ** 9 * (2 + Fr(4, 5)) == Fr(14 * 4 ** 9, 5 ** 10) and round(float(pw), 2) == 0.38
    assert round(float(1 - pw), 2) == 0.62
    d = _binom(12, h)
    assert tail(d, 10) == Fr(79, 4096) and tail(d, 9) == Fr(299, 4096)
    assert round(float(tail(d, 10)), 3) == 0.019 and round(float(tail(d, 9)), 3) == 0.073
    assert min(k for k in range(13) if tail(d, k) <= Fr(5, 100)) == 10


def _text_check():
    cjk = re.compile(r"[぀-ヿ一-鿿！-～]")
    for s in SEC:
        fields = [s["title"], s["base"]] + [it[k] for it in s["items"] for k in it if k != "lv"]
        for f in fields:
            assert "$$" not in f, f[:40]
            assert f.count("$") % 2 == 0, f[:60]
            for m in re.findall(r"\$([^$]*)\$", f):
                assert not cjk.search(m), m


def verify():
    g = globals()
    for k in sorted(k for k in g if k.startswith("_v") and k[2:].isdigit()):
        g[k]()
    _text_check()
    # 例題数と難易度の配分（目標 25±3、★5 は3題以上）
    items = [it for s in SEC for it in s["items"]]
    assert 4 <= len(SEC) <= 9
    assert 22 <= len(items) <= 28, len(items)
    cnt = {k: sum(it["lv"] == k for it in items) for k in range(1, 6)}
    assert cnt == {1: 6, 2: 6, 3: 7, 4: 5, 5: 3}, cnt
    assert cnt[5] >= 3
    for s in SEC:  # 節の中は易しい順
        lv = [it["lv"] for it in s["items"]]
        assert lv == sorted(lv), s["title"]
    for it in items:
        for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
            assert it.get(k) not in (None, ""), (it["title"], k)
        if it["lv"] >= 3:
            assert it.get("note"), it["title"]
