"""第5章 場合の数（数学A）。答えはすべて verify() の中で全列挙（itertools）などで検算する。"""
import itertools
from itertools import permutations, combinations, product, combinations_with_replacement
from math import comb, factorial, gcd

SEC = []
VCHECKS = []   # 節ごとの検算関数


def ncount(it):
    return sum(1 for _ in it)


# ---------------------------------------------------------------- 節1
SEC.append({"title": "集合の要素の個数と和・積の法則",
"base": r"""・$n(A\cup B)=n(A)+n(B)-n(A\cap B)$<br>
・$n(A\cup B\cup C)=n(A)+n(B)+n(C)-n(A\cap B)-n(B\cap C)-n(C\cap A)+n(A\cap B\cap C)$<br>
・補集合：$n(\overline{A})=n(U)-n(A)$，ド・モルガンの法則 $\overline{A\cup B}=\overline{A}\cap\overline{B}$<br>
・和の法則：同時には起こらない場合の数は<b>足す</b>。積の法則：続けて起こる場合の数は<b>掛ける</b><br>
・$N=p^aq^br^c$（$p,\ q,\ r$ は異なる素数）の正の約数の個数は $(a+1)(b+1)(c+1)$，総和は $(1+p+\cdots+p^a)(1+q+\cdots+q^b)(1+r+\cdots+r^c)$""",
"items": [
 {"lv": 1, "title": "倍数の個数（2つの集合の包除）",
  "q": r"1 から 300 までの整数のうち、次のような数の個数を求めよ。<br>(1) 4 の倍数または 6 の倍数　(2) 4 の倍数でも 6 の倍数でもない数　(3) 4 の倍数であるが 6 の倍数でない数",
  "hint": r"4 の倍数の集合を $A$，6 の倍数の集合を $B$ とする。$A\cap B$ は <b>最小公倍数 12 の倍数</b>の集合。(2) はド・モルガンの法則で $\overline{A\cup B}$，(3) は $A$ から $A\cap B$ を除いたもの。",
  "sol": r"1 から 300 までの整数全体の集合を $U$，そのうち 4 の倍数の集合を $A$，6 の倍数の集合を $B$ とすると、$A\cap B$ は 12 の倍数の集合である。<br>"
         r"$300=4\cdot75=6\cdot50=12\cdot25$ より　$n(A)=75,\ n(B)=50,\ n(A\cap B)=25$<br>"
         r"(1) $n(A\cup B)=75+50-25=\boldsymbol{100}$（個）<br>"
         r"(2) $n(\overline{A}\cap\overline{B})=n(\overline{A\cup B})=300-100=\boldsymbol{200}$（個）<br>"
         r"(3) $n(A\cap\overline{B})=n(A)-n(A\cap B)=75-25=\boldsymbol{50}$（個）",
  "note": r"4 と 6 の公倍数は最小公倍数 12 の倍数である。$4\times6=24$ の倍数としてしまうと $n(A\cap B)=12$ となり誤り。",
  "ex": r"1 から 500 までの整数のうち、次のような数の個数を求めよ。<br>(1) 6 の倍数または 9 の倍数　(2) 6 の倍数でも 9 の倍数でもない数　(3) 6 の倍数であるが 9 の倍数でない数",
  "exa": r"(1) 111 個　(2) 389 個　(3) 56 個"},
 {"lv": 1, "title": "和の法則と積の法則（さいころの目）",
  "q": r"大小 2 個のさいころを投げるとき、次の場合は何通りあるか。<br>(1) 目の和が 4 の倍数になる　(2) 目の積が偶数になる　(3) 大の目が小の目より大きい",
  "hint": r"(1) 和が 4，8，12 の場合は同時には起こらないから<b>和の法則</b>。(2) 「積が偶数」は場合が多いので、余事象「積が奇数（2 つとも奇数）」を<b>積の法則</b>で数える。(3) 目が異なる場合を、大小の関係で半分に分ける。",
  "sol": r"大の目を $a$，小の目を $b$ とし、$(a,\ b)$ で表す。<br>"
         r"(1) 和が 4：$(1,3),(2,2),(3,1)$ の 3 通り。和が 8：$(2,6),(3,5),(4,4),(5,3),(6,2)$ の 5 通り。和が 12：$(6,6)$ の 1 通り。<br>"
         r"これらは同時には起こらないから　$3+5+1=\boldsymbol{9}$（通り）<br>"
         r"(2) 目の出方は全部で $6\times6=36$ 通り。積が奇数となるのは $a,\ b$ がともに奇数のときで $3\times3=9$ 通り。<br>よって積が偶数となるのは　$36-9=\boldsymbol{27}$（通り）<br>"
         r"(3) $a\neq b$ となるのは $36-6=30$ 通りで、$a>b$ と $a<b$ は $a$ と $b$ を入れかえると 1 対 1 に対応するから　$30\div2=\boldsymbol{15}$（通り）",
  "note": r"「少なくとも一方が偶数」のように場合が多いときは余事象を考える。(3) のように対称性を使うと、書き出さずに数えられる。",
  "ex": r"大小 2 個のさいころを投げるとき、次の場合は何通りあるか。<br>(1) 目の和が 5 の倍数になる　(2) 目の積が 3 の倍数になる　(3) 2 つの目の差が 2 以上になる",
  "exa": r"(1) 7 通り　(2) 20 通り　(3) 20 通り"},
 {"lv": 2, "title": "3つの集合の包除（いずれでも割り切れない数）",
  "q": r"1 から 1000 までの整数のうち、次のような数の個数を求めよ。<br>(1) 2，3，5 の少なくとも 1 つで割り切れる数　(2) 2，3，5 のいずれでも割り切れない数<br>(3) 2 で割り切れるが、3 でも 5 でも割り切れない数",
  "hint": r"2，3，5 の倍数の集合を $A,\ B,\ C$ として、3 つの集合の和集合の要素の個数の公式を使う。$A\cap B$ は 6 の倍数、$A\cap B\cap C$ は 30 の倍数の集合。",
  "sol": r"2，3，5 の倍数の集合をそれぞれ $A,\ B,\ C$ とする。1000 以下の $k$ の倍数の個数は、$1000\div k$ の整数部分であるから<br>"
         r"$n(A)=500,\ n(B)=333,\ n(C)=200$，$n(A\cap B)=166$（6 の倍数），$n(B\cap C)=66$（15 の倍数），$n(C\cap A)=100$（10 の倍数），$n(A\cap B\cap C)=33$（30 の倍数）<br>"
         r"(1) $n(A\cup B\cup C)=500+333+200-166-66-100+33=\boldsymbol{734}$（個）<br>"
         r"(2) $1000-734=\boldsymbol{266}$（個）<br>"
         r"(3) $A$ の要素のうち $B\cup C$ に属さないものの個数であるから<br>"
         r"$n(A)-n(A\cap(B\cup C))=n(A)-\{n(A\cap B)+n(A\cap C)-n(A\cap B\cap C)\}=500-(166+100-33)=\boldsymbol{267}$（個）",
  "note": r"(2) を $1000\left(1-\dfrac12\right)\left(1-\dfrac13\right)\left(1-\dfrac15\right)$ と計算すると $\dfrac{800}{3}$ となり整数にならない。1000 が 30 で割り切れないからである。範囲の上端が 30 の倍数のとき（例えば 1 から 900 まで）は、この積の形で $900\cdot\dfrac12\cdot\dfrac23\cdot\dfrac45=240$ と計算できる。",
  "ex": r"1 から 600 までの整数のうち、次のような数の個数を求めよ。<br>(1) 2，3，7 の少なくとも 1 つで割り切れる数　(2) 2，3，7 のいずれでも割り切れない数<br>(3) 2 で割り切れるが、3 でも 7 でも割り切れない数",
  "exa": r"(1) 429 個　(2) 171 個　(3) 172 個"},
 {"lv": 2, "title": "共通部分の要素の個数の最大・最小",
  "q": r"ある学級の生徒 40 人に、数学と英語が好きかどうかを調べたところ、数学が好きな生徒は 28 人、英語が好きな生徒は 21 人であった。<br>"
       r"(1) 数学と英語の両方が好きな生徒の人数 $x$ のとり得る値の範囲を求めよ。<br>(2) どちらも好きでない生徒が 5 人であるとき、数学だけが好きな生徒の人数を求めよ。",
  "hint": r"$n(A\cup B)=n(A)+n(B)-n(A\cap B)$ と $n(A\cup B)\leqq n(U)$，$n(A\cap B)\leqq n(A),\ n(B)$ から範囲を絞る。範囲のすべての値が実際にとれることも確かめる。",
  "sol": r"数学、英語が好きな生徒の集合を $A,\ B$ とすると $n(A)=28,\ n(B)=21,\ n(A\cap B)=x$。<br>"
         r"(1) $n(A\cup B)=28+21-x=49-x$ で、$n(A\cup B)\leqq40$ より $x\geqq9$。また $A\cap B\subset B$ より $x\leqq21$。<br>"
         r"逆に $9\leqq x\leqq21$ の整数 $x$ に対し、両方好き $x$ 人、数学だけ $28-x$ 人、英語だけ $21-x$ 人、どちらも好きでない $x-9$ 人とすれば、どの人数も 0 以上で合計 40 人となり条件を満たす。<br>"
         r"よって　$\boldsymbol{9\leqq x\leqq21}$<br>"
         r"(2) $n(A\cup B)=40-5=35$ であるから $49-x=35$，$x=14$。数学だけが好きな生徒は $28-14=\boldsymbol{14}$（人）",
  "note": r"最小値は「$A$ と $B$ をできるだけ重ねない（$A\cup B=U$）」とき、最大値は「小さい方の集合がもう一方に含まれる」ときに実現する。",
  "ex": r"生徒 50 人のうち、問題 A を正解した者が 34 人、問題 B を正解した者が 29 人であった。<br>(1) 両方を正解した人数 $x$ のとり得る値の範囲を求めよ。<br>(2) どちらも正解しなかった者が 7 人のとき、B だけを正解した人数を求めよ。",
  "exa": r"(1) $13\leqq x\leqq29$　(2) 9 人"},
 {"lv": 2, "title": "約数の個数と総和",
  "q": r"720 の正の約数について、次のものを求めよ。<br>(1) 個数　(2) 総和　(3) 奇数であるものの総和",
  "hint": r"素因数分解 $720=2^4\cdot3^2\cdot5$ から、約数は $2^a3^b5^c$（$0\leqq a\leqq4,\ 0\leqq b\leqq2,\ 0\leqq c\leqq1$）と表せる。総和は、積 $(1+2+\cdots+2^4)(1+3+3^2)(1+5)$ を展開した各項が約数 1 つずつに対応することを使う。",
  "sol": r"$720=2^4\cdot3^2\cdot5$ より、正の約数は $2^a\cdot3^b\cdot5^c$（$a=0,1,2,3,4$；$b=0,1,2$；$c=0,1$）と表される。<br>"
         r"(1) $a,\ b,\ c$ の選び方は積の法則により　$5\times3\times2=\boldsymbol{30}$（個）<br>"
         r"(2) $(1+2+2^2+2^3+2^4)(1+3+3^2)(1+5)$ を展開すると、$2^a3^b5^c$ の形の項がちょうど 1 つずつ現れるから、総和は<br>"
         r"$31\times13\times6=\boldsymbol{2418}$<br>"
         r"(3) 奇数の約数は $a=0$ のもので、総和は　$(1+3+3^2)(1+5)=13\times6=\boldsymbol{78}$",
  "note": r"偶数の約数の総和は $2418-78=2340$，あるいは $(2+2^2+2^3+2^4)(1+3+3^2)(1+5)=30\times13\times6=2340$ と求められる。",
  "ex": r"1080 の正の約数について、(1) 個数　(2) 総和　(3) 奇数であるものの総和 を求めよ。",
  "exa": r"(1) 32 個　(2) 3600　(3) 240"},
 {"lv": 3, "title": "互いに素な整数の個数と総和",
  "q": r"1 から 720 までの整数のうち、720 と互いに素であるものについて、(1) 個数　(2) 総和 を求めよ。",
  "hint": r"$720=2^4\cdot3^2\cdot5$ と互いに素 $\iff$ 2，3，5 のいずれでも割り切れない。(1) は 3 つの集合の包除。(2) は $k$ と $720-k$ を<b>組にする</b>と和が一定になることを利用する。",
  "sol": r"$720=2^4\cdot3^2\cdot5$ であるから、$k$ が 720 と互いに素であることは、$k$ が 2，3，5 のいずれでも割り切れないことと同値である。<br>"
         r"(1) 2，3，5 の倍数の集合を $A,\ B,\ C$ とすると<br>"
         r"$n(A)=360,\ n(B)=240,\ n(C)=144,\ n(A\cap B)=120,\ n(B\cap C)=48,\ n(C\cap A)=72,\ n(A\cap B\cap C)=24$<br>"
         r"$n(A\cup B\cup C)=360+240+144-120-48-72+24=528$ より、求める個数は　$720-528=\boldsymbol{192}$（個）<br>"
         r"(2) $k$ と 720 の公約数は $720-k$ と 720 の公約数でもあり、逆も成り立つ。よって $k$ が 720 と互いに素 $\iff$ $720-k$ が 720 と互いに素。<br>"
         r"720 と互いに素な数は $1\leqq k\leqq719$ にあり、$k=360$ は互いに素でないから、$k\neq720-k$。したがって 192 個は、和が 720 になる 2 数の組 96 組に分けられ、総和は<br>"
         r"$720\times96=\boldsymbol{69120}$",
  "note": r"一般に $N=p^aq^br^c$ と互いに素な $N$ 以下の自然数の個数は $N\left(1-\dfrac1p\right)\left(1-\dfrac1q\right)\left(1-\dfrac1r\right)$（$720\cdot\dfrac12\cdot\dfrac23\cdot\dfrac45=192$）。(2) の組にする考え方から、$N\geqq3$ のとき総和はつねに $\dfrac{N}{2}\times$（個数）となる。",
  "ex": r"1 から 600 までの整数のうち、600 と互いに素であるものについて、(1) 個数　(2) 総和 を求めよ。",
  "exa": r"(1) 160 個　(2) 48000"},
]})


def v1():
    U = range(1, 301)
    A = {k for k in U if k % 4 == 0}; B = {k for k in U if k % 6 == 0}
    assert (len(A), len(B), len(A & B)) == (75, 50, 25)
    assert len(A | B) == 100 and 300 - len(A | B) == 200 and len(A - B) == 50
    U = range(1, 501)
    A = {k for k in U if k % 6 == 0}; B = {k for k in U if k % 9 == 0}
    assert len(A | B) == 111 and 500 - len(A | B) == 389 and len(A - B) == 56
    D = list(product(range(1, 7), repeat=2))
    assert ncount(d for d in D if sum(d) % 4 == 0) == 9
    assert ncount(d for d in D if d[0] * d[1] % 2 == 0) == 27
    assert ncount(d for d in D if d[0] > d[1]) == 15
    assert ncount(d for d in D if sum(d) % 5 == 0) == 7
    assert ncount(d for d in D if d[0] * d[1] % 3 == 0) == 20
    assert ncount(d for d in D if abs(d[0] - d[1]) >= 2) == 20

    def three(N, p, q, r):
        U = range(1, N + 1)
        A = {k for k in U if k % p == 0}; B = {k for k in U if k % q == 0}; C = {k for k in U if k % r == 0}
        return len(A | B | C), N - len(A | B | C), len(A - B - C), (len(A), len(B), len(C), len(A & B), len(B & C), len(C & A), len(A & B & C))
    r = three(1000, 2, 3, 5)
    assert r[:3] == (734, 266, 267) and r[3] == (500, 333, 200, 166, 66, 100, 33)
    assert 500 - (166 + 100 - 33) == 267
    assert three(600, 2, 3, 7)[:3] == (429, 171, 172)
    assert three(900, 2, 3, 5)[1] == 240
    # 共通部分の最大・最小（人数の割り当てが可能な x）
    ok = [x for x in range(0, 41) if min(x, 28 - x, 21 - x, 40 - (28 + 21 - x)) >= 0]
    assert min(ok) == 9 and max(ok) == 21 and ok == list(range(9, 22))
    assert 49 - 35 == 14 and 28 - 14 == 14
    ok = [x for x in range(0, 51) if min(x, 34 - x, 29 - x, 50 - (34 + 29 - x)) >= 0]
    assert (min(ok), max(ok)) == (13, 29)
    x = 34 + 29 - (50 - 7); assert x == 20 and 29 - x == 9
    # 約数
    def divs(n): return [d for d in range(1, n + 1) if n % d == 0]
    d = divs(720)
    assert len(d) == 30 and sum(d) == 2418 and sum(x for x in d if x % 2) == 78 == 13 * 6
    assert 31 * 13 * 6 == 2418 and sum(x for x in d if x % 2 == 0) == 2340 == 30 * 13 * 6
    assert 720 == 2**4 * 3**2 * 5
    d = divs(1080)
    assert 1080 == 2**3 * 3**3 * 5 and len(d) == 32 and sum(d) == 3600 and sum(x for x in d if x % 2) == 240
    # 互いに素
    co = [k for k in range(1, 721) if gcd(k, 720) == 1]
    assert len(co) == 192 and sum(co) == 69120 == 720 * 96
    assert 360 + 240 + 144 - 120 - 48 - 72 + 24 == 528
    co = [k for k in range(1, 601) if gcd(k, 600) == 1]
    assert len(co) == 160 and sum(co) == 48000


VCHECKS.append(v1)


# ---------------------------------------------------------------- 立方体などの回転群（検算用）
def closure(gens):
    n = len(gens[0])
    G = {tuple(range(n))}
    frontier = list(G)
    while frontier:
        new = []
        for g in frontier:
            for h in gens:
                k = tuple(h[g[i]] for i in range(n))
                if k not in G:
                    G.add(k); new.append(k)
        frontier = new
    return G


# 立方体の面：0 上, 1 下, 2 前, 3 後, 4 左, 5 右（g[i] は面 i の移り先）
CUBE = closure([(0, 1, 5, 4, 2, 3),      # 上下軸のまわりの 90°：前→右→後→左→前
                (2, 3, 1, 0, 4, 5)])     # 左右軸のまわりの 90°：上→前→下→後→上
# 正四面体の面 0〜3（回転群は偶置換全体）
TETRA = closure([(1, 2, 0, 3), (0, 2, 3, 1)])
# 正三角柱の面：0 上, 1 下, 2,3,4 側面
PRISM = closure([(0, 1, 3, 4, 2), (1, 0, 2, 4, 3)])


def orbits(colorings, G):
    seen = set()
    for c in colorings:
        seen.add(min(tuple(c[g.index(i)] for i in range(len(c))) for g in G))
    return len(seen)


def circ_classes(seqs, reflect=False):
    """列（円形に並べたもの）を回転（と裏返し）で同一視したときの類の数"""
    seen = set()
    for s in seqs:
        s = tuple(s); n = len(s)
        cand = [s[i:] + s[:i] for i in range(n)]
        if reflect:
            r = s[::-1]; cand += [r[i:] + r[:i] for i in range(n)]
        seen.add(min(cand))
    return len(seen)


# ---------------------------------------------------------------- 節2
FIG_PAINT = (r'<svg class="fig" width="150" height="150" viewBox="0 0 160 160">'
             r'<rect x="10" y="10" width="140" height="140" fill="none" stroke="#222" stroke-width="1.5"/>'
             r'<rect x="50" y="50" width="60" height="60" fill="none" stroke="#222" stroke-width="1.5"/>'
             r'<path d="M10 10 L50 50 M150 10 L110 50 M150 150 L110 110 M10 150 L50 110" stroke="#222" stroke-width="1.5"/>'
             r'<g font-size="12" text-anchor="middle"><text x="80" y="84">A</text><text x="80" y="34">B</text>'
             r'<text x="131" y="84">C</text><text x="80" y="135">D</text><text x="29" y="84">E</text></g></svg>')

SEC.append({"title": "順列・円順列・重複順列",
"base": r"""・異なる $n$ 個から $r$ 個取って並べる順列：${}_n\mathrm{P}_r=n(n-1)\cdots(n-r+1)=\dfrac{n!}{(n-r)!}$<br>
・円順列：異なる $n$ 個を円形に並べる方法は $(n-1)!$ 通り（1 つを固定して残りを並べる）。じゅず順列（裏返して一致するものも同じ）は $\dfrac{(n-1)!}{2}$ 通り（$n\geqq3$）<br>
・重複順列：$n$ 種類のものから重複を許して $r$ 個並べる方法は $n^r$ 通り<br>
・「隣り合う」ものはまとめて 1 つとみなし、「隣り合わない」ものは他を先に並べてその間と両端に入れる""",
"items": [
 {"lv": 1, "title": "隣り合う・隣り合わない順列",
  "q": r"男子 4 人と女子 3 人が 1 列に並ぶとき、次の並び方は何通りあるか。<br>(1) 女子 3 人が続いて並ぶ　(2) 女子どうしが隣り合わない　(3) 両端が男子である",
  "hint": r"(1) 女子 3 人をひとまとめにして 1 人とみなし、まとめた中の並び方を掛ける。(2) 先に男子を並べ、男子の間と両端の 5 か所から 3 か所を選んで女子を 1 人ずつ入れる。(3) 制限のある両端から先に決める。",
  "sol": r"(1) 女子 3 人をまとめて 1 人とみなすと、5 人の並び方は $5!$ 通り。まとめた女子 3 人の並び方は $3!$ 通り。<br>よって　$5!\times3!=120\times6=\boldsymbol{720}$（通り）<br>"
         r"(2) 男子 4 人の並び方は $4!$ 通り。男子の間と両端の 5 か所のうち 3 か所に女子 3 人を 1 人ずつ並べる方法は ${}_5\mathrm{P}_3$ 通り。<br>よって　$4!\times{}_5\mathrm{P}_3=24\times60=\boldsymbol{1440}$（通り）<br>"
         r"(3) 両端に男子を並べる方法は ${}_4\mathrm{P}_2=12$ 通り。残り 5 人を間に並べる方法は $5!=120$ 通り。<br>よって　$12\times120=\boldsymbol{1440}$（通り）",
  "note": r"(2) を「全体 $-$ (1)」とするのは誤り。全体から引くと「女子 3 人が続く」以外の並び方になり、女子 2 人だけが隣り合う並び方が残ってしまう。",
  "ex": r"男子 5 人と女子 2 人が 1 列に並ぶとき、次の並び方は何通りあるか。<br>(1) 女子 2 人が隣り合う　(2) 女子 2 人が隣り合わない　(3) 両端が男子である",
  "exa": r"(1) 1440 通り　(2) 3600 通り　(3) 2400 通り"},
 {"lv": 1, "title": "重複順列（数字の列・部屋割り）",
  "q": r"(1) 1，2，3 の 3 種類の数字を用いて 5 桁の整数をつくる。同じ数字を何回使ってもよいとき、整数は何個できるか。<br>"
       r"(2) 5 人を 2 つの部屋 A，B に入れる方法は何通りか。空室があってもよい場合と、空室ができない場合のそれぞれについて答えよ。<br>"
       r"(3) 5 人を 2 つのグループに分ける方法は何通りか。",
  "hint": r"1 人ずつ（1 桁ずつ）「どれを選ぶか」を決めると考え、<b>重複順列</b> $n^r$ を使う。空室なしは、全員が同じ部屋に入る場合を除く。(3) はグループに区別がないので、(2) の部屋 A，B の区別をなくす。",
  "sol": r"(1) 各位の数字の選び方が 3 通りずつあるから　$3^5=\boldsymbol{243}$（個）<br>"
         r"(2) 各人の部屋の選び方が 2 通りずつあるから、空室があってもよい場合は　$2^5=\boldsymbol{32}$（通り）<br>"
         r"このうち、全員が A に入る場合と全員が B に入る場合が空室のできる場合であるから、空室ができない場合は　$32-2=\boldsymbol{30}$（通り）<br>"
         r"(3) (2) の空室ができない入れ方で部屋 A，B の区別をなくすと、同じ分け方が 2 通りずつ現れるから　$30\div2=\boldsymbol{15}$（通り）",
  "note": r"(3) で $32\div2=16$ とすると、「5 人と 0 人」に分ける場合（グループにならない）を含んでしまう。",
  "ex": r"(1) 0，1，2 の 3 種類の数字を用いて 5 桁の整数をつくる。同じ数字を何回使ってもよいとき、何個できるか。<br>"
        r"(2) 6 人を 2 つの部屋 A，B に入れる方法は、空室があってもよい場合、空室ができない場合のそれぞれ何通りか。<br>(3) 6 人を 2 つのグループに分ける方法は何通りか。",
  "exa": r"(1) 162 個　(2) 64 通り，62 通り　(3) 31 通り"},
 {"lv": 2, "title": "0 を含む数字で整数をつくる",
  "q": r"0，1，2，3，4，5 の 6 個の数字から異なる 4 個を選んで並べ、4 桁の整数をつくる。<br>(1) 4 桁の整数は全部で何個できるか。　(2) 偶数は何個できるか。　(3) 3 の倍数は何個できるか。",
  "hint": r"千の位に 0 は置けない。(2) は一の位が 0 か、2・4 かで場合分けする（0 を使う位置が変わるため）。(3) は「各位の数の和が 3 の倍数」を使い、使う 4 個の数字の組を先に決める。",
  "sol": r"(1) 千の位は 0 以外の 5 通り、残りの 3 つの位は残り 5 個から 3 個を並べて ${}_5\mathrm{P}_3=60$ 通り。　$5\times60=\boldsymbol{300}$（個）<br>"
         r"(2) 一の位が 0 のとき：残り 3 つの位は ${}_5\mathrm{P}_3=60$ 通り。<br>"
         r"一の位が 2 または 4 のとき：千の位は 0 と一の位の数字以外の 4 通り、百・十の位は残り 4 個から ${}_4\mathrm{P}_2=12$ 通りで、$2\times4\times12=96$ 通り。<br>"
         r"よって　$60+96=\boldsymbol{156}$（個）<br>"
         r"(3) 3 の倍数となるのは、4 個の数字の和が 3 の倍数のときである。6 個の数字の和は $0+1+2+3+4+5=15$ なので、使わない 2 個の数字の和が 3 の倍数となればよい。<br>"
         r"使わない 2 個は $\{0,3\},\ \{1,2\},\ \{1,5\},\ \{2,4\},\ \{4,5\}$ の 5 組。<br>"
         r"$\{0,3\}$ を使わないとき、$1,2,4,5$ の並べ方は $4!=24$ 通り。<br>"
         r"他の 4 組のときは使う数字に 0 を含み、0 を千の位に置かないから $4!-3!=18$ 通りずつ。<br>"
         r"よって　$24+4\times18=\boldsymbol{96}$（個）",
  "note": r"(2) で「一の位が偶数 3 通り」と一括りにすると、0 を一の位に使ったかどうかで千の位の選び方が変わるため誤る。0 の扱いが変わるところで場合を分けるのが鉄則。",
  "ex": r"0，1，2，3，4 の 5 個の数字から異なる 3 個を選んで 3 桁の整数をつくる。(1) 全部で何個できるか。　(2) 偶数は何個か。　(3) 3 の倍数は何個か。",
  "exa": r"(1) 48 個　(2) 30 個　(3) 20 個"},
 {"lv": 2, "title": "辞書式に並べる",
  "q": r"a，b，c，d，e の 5 文字を 1 列に並べてできる 120 個の文字列を、辞書式（アルファベット順）に 1 番目 abcde から 120 番目 edcba まで並べる。<br>(1) cbeda は何番目か。　(2) 75 番目の文字列は何か。",
  "hint": r"先頭の文字ごとに $4!=24$ 個ずつのかたまりになる。先頭から順に「その文字より前にくる文字列が何個あるか」を数える。",
  "sol": r"(1) cbeda より前にあるものを数える。<br>"
         r"a□□□□，b□□□□ の形：$2\times4!=48$ 個。ca□□□ の形：$3!=6$ 個。cba□□，cbd□□ の形：$2\times2!=4$ 個。<br>"
         r"cbe□□ の形は cbead，cbeda の順なので、cbeda はその 2 番目。<br>"
         r"よって　$48+6+4+2=\boldsymbol{60}$（番目）<br>"
         r"(2) a，b，c で始まるものが $3\times24=72$ 個あるから、73 番目から d で始まる。<br>"
         r"da□□□ の形は $3!=6$ 個で 73〜78 番目にあたり、小さい順に dabce，dabec，dacbe，… と続く。<br>"
         r"よって 75 番目は　$\boldsymbol{\mathrm{dacbe}}$",
  "note": r"「何番目か」は<b>それより前にあるものの個数 $+1$</b>。最後の数個は書き出すのが確実である。",
  "ex": r"1，2，3，4，5 の 5 個の数字を 1 回ずつ使ってできる 5 桁の整数を小さい順に並べる。(1) 35142 は何番目か。　(2) 100 番目の数は何か。",
  "exa": r"(1) 68 番目　(2) 51342"},
 {"lv": 2, "title": "円順列とじゅず順列",
  "q": r"大人 4 人と子ども 4 人の計 8 人が、円形のテーブルのまわりに等間隔に並んだ 8 つの席に座る。回転して一致する座り方は同じとみなす。<br>"
       r"(1) 座り方は全部で何通りか。　(2) 大人と子どもが交互に座る座り方は何通りか。　(3) 大人 A と子ども B が向かい合って座る座り方は何通りか。<br>"
       r"(4) また、色の異なる 8 個の玉に糸を通して首飾りをつくる方法は何通りか。",
  "hint": r"円順列は<b>1 人を固定</b>して残りを並べる。(2) 大人 4 人を円形に並べたあと、間の 4 席に子どもを並べる。(3) A を固定すると B の席が決まる。(4) 首飾りは裏返すと一致するものが 2 つずつあるので、じゅず順列。",
  "sol": r"(1) 1 人を固定し、残り 7 人を並べると考えて　$(8-1)!=7!=\boldsymbol{5040}$（通り）<br>"
         r"(2) 大人 4 人の円順列は $(4-1)!=6$ 通り。大人の間の 4 席に子ども 4 人を並べる方法は $4!=24$ 通り（大人の位置が決まっているので、ここは普通の順列）。<br>よって　$6\times24=\boldsymbol{144}$（通り）<br>"
         r"(3) A の席を固定すると、B の席は A の正面に決まる。残り 6 席に 6 人を並べて　$6!=\boldsymbol{720}$（通り）<br>"
         r"(4) 円順列 $7!$ 通りのうち、裏返して一致するものが 2 つずつあるから　$\dfrac{7!}{2}=\boldsymbol{2520}$（通り）",
  "note": r"(2) で子どもの並べ方も円順列 $(4-1)!$ としてしまう誤りが多い。回転の重なりは最初の大人の並べ方ですでに除かれている。",
  "ex": r"男子 3 人と女子 3 人が円形のテーブルに等間隔に座る（回転して一致するものは同じ）。(1) 男女が交互に座る座り方は何通りか。　(2) 男子 A と女子 B が隣り合う座り方は何通りか。<br>(3) 色の異なる 6 個の玉で首飾りをつくる方法は何通りか。",
  "exa": r"(1) 12 通り　(2) 48 通り　(3) 60 通り"},
 {"lv": 2, "title": "領域の塗り分け",
  "q": FIG_PAINT + r"図のように、正方形を中央の正方形 A と、そのまわりの 4 つの台形 B，C，D，E の 5 つの領域に分ける。境界線を共有して隣り合う領域は異なる色で塗るとき、異なる 5 色の絵の具を用いた塗り方は、次の場合それぞれ何通りあるか。<br>"
       r"(1) 5 色すべてを使う　(2) ちょうど 4 色を使う　(3) 何色を使ってもよい",
  "hint": r"最も多くの領域と隣り合う A から塗る。B，C，D，E は輪の形に隣り合い、B と D、C と E は隣り合わない。<b>B と D が同じ色か異なる色か</b>で場合を分ける。",
  "sol": r"A は他の 4 領域すべてと隣り合い、B，C，D，E は B−C−D−E−B の順に輪のように隣り合う。<br>"
         r"(1) A の色は 5 通り。B，C，D，E には残りの 4 色を 1 色ずつ塗るから $4!=24$ 通り。　$5\times24=\boldsymbol{120}$（通り）<br>"
         r"(2) 使う 4 色の選び方は 5 通り、A の色はそのうち 4 通り。B，C，D，E には残り 3 色をすべて使う。<br>"
         r"・B と D が同色のとき：その色は 3 通り。C，E はそれと異なる 2 色を 1 色ずつ使い（C と E が同色だと 2 色しか使わない）2 通り。$3\times2=6$ 通り<br>"
         r"・B と D が異なる色のとき：$3\times2=6$ 通り。C，E はともに B，D と異なる残りの 1 色。6 通り<br>"
         r"よって　$5\times4\times(6+6)=\boldsymbol{240}$（通り）<br>"
         r"(3) A の色は 5 通り。B，C，D，E は A 以外の 4 色で塗る。<br>"
         r"・B と D が同色のとき：B（＝D）が 4 通り、C，E はそれぞれ B と異なる 3 通りで $4\times3\times3=36$ 通り<br>"
         r"・B と D が異なる色のとき：B が 4 通り、D が 3 通り、C，E はそれぞれ B，D と異なる 2 通りで $4\times3\times2\times2=48$ 通り<br>"
         r"よって　$5\times(36+48)=\boldsymbol{420}$（通り）",
  "note": r"(3) のうち、ちょうど 3 色を使う塗り方は、A が 5 通り、B＝D，C＝E の 2 色が $4\times3$ 通りで 60 通り。$120+240+60=420$ となり、(1)〜(3) の結果が確かめられる。",
  "ex": r"例題の図の 5 つの領域を、隣り合う領域が異なる色になるように塗る。(1) 異なる 4 色をすべて使って塗る方法は何通りか。　(2) 異なる 6 色のうち何色を使ってもよいとき、塗り方は何通りか。",
  "exa": r"(1) 48 通り　(2) 1560 通り"},
 {"lv": 3, "title": "立方体の面の塗り分け",
  "q": r"立方体の 6 つの面に色を塗る。ただし、立方体を回転させて一致する塗り方は同じとみなす。<br>"
       r"(1) 異なる 6 色をすべて使って塗る方法は何通りか。<br>(2) 異なる 5 色をすべて使い、隣り合う面は異なる色になるように塗る方法は何通りか。",
  "hint": r"回転で同じになるものを除くため、<b>1 つの色の面を上面に固定</b>する。すると残る自由な回転は上下を軸とする回転だけになり、側面 4 面は円順列で数えられる。(2) は同じ色の 2 面が向かい合うことに注意し、上下を入れかえる回転も残るのでじゅず順列になる。",
  "sol": r"(1) ある 1 色（例えば赤）の面を上面に固定する。下面の色は残り 5 色から 5 通り。<br>"
         r"側面の 4 面は上下を軸とする回転で移り合うので、残り 4 色の円順列で $(4-1)!=6$ 通り。<br>よって　$5\times6=\boldsymbol{30}$（通り）<br>"
         r"(2) 6 面を 5 色で塗るので、ちょうど 1 色が 2 面に使われる。その 2 面は隣り合わないから、向かい合う 2 面である。<br>"
         r"2 面に使う色の選び方は 5 通りで、その色を上面と下面に塗る。側面の 4 面に残り 4 色を塗るが、上下を軸とする回転のほか、上下をひっくり返す回転でも上下の色は変わらないので、側面の並びは裏返したものも同じになる。<br>"
         r"よって側面はじゅず順列で $\dfrac{(4-1)!}{2}=3$ 通り。　$5\times3=\boldsymbol{15}$（通り）",
  "note": r"(1) は「$6!$ 通りの塗り方が、回転で 24 通りずつ重なる」と考えて $\dfrac{6!}{24}=30$ とも求められる（立方体を一致させる回転は、上面の選び方 6 通り $\times$ 前面の選び方 4 通り $=24$ 通り）。(2) では同じ塗り方を与える回転があるので、この割り算は使えない。",
  "ex": r"(1) 正三角柱の 5 つの面（上下の正三角形と 3 つの側面）を、異なる 5 色をすべて使って塗る方法は何通りか。ただし、回転させて一致するものは同じとみなす。<br>"
        r"(2) 立方体の 6 つの面を、異なる 4 色をすべて使い、隣り合う面は異なる色になるように塗る方法は何通りか（回転で一致するものは同じ）。",
  "exa": r"(1) 20 通り　(2) 6 通り"},
 {"lv": 4, "title": "円卓で夫婦が隣り合わない（包除の利用）",
  "q": r"3 組の夫婦 6 人が、円形のテーブルのまわりに等間隔に並んだ 6 つの席に座る。どの夫婦も隣り合わない座り方は何通りか。ただし、回転して一致する座り方は同じとみなす。",
  "hint": r"「どの夫婦も隣り合わない」を直接数えるのは難しい。夫婦 $i$ が隣り合う座り方の集合を $A_i$ として、<b>余事象 $A_1\cup A_2\cup A_3$ を包除で数える</b>。隣り合う夫婦はひとまとめにして円順列を使う。",
  "sol": r"座り方は全部で $(6-1)!=120$ 通り。夫婦 $i$（$i=1,2,3$）が隣り合う座り方の集合を $A_i$ とする。<br>"
         r"$n(A_1)$：夫婦 1 をまとめて 1 人とみなすと 5 人の円順列で $4!$ 通り、夫婦の並び方が 2 通りで $4!\times2=48$。$n(A_2),\ n(A_3)$ も同じ。<br>"
         r"$n(A_1\cap A_2)$：2 組をそれぞれまとめると 4 人の円順列 $3!$ 通り、各夫婦の並び方 $2^2$ 通りで $3!\times4=24$。他の 2 組の場合も同じ。<br>"
         r"$n(A_1\cap A_2\cap A_3)$：3 人の円順列 $2!$ 通り、並び方 $2^3$ 通りで $2!\times8=16$。<br>"
         r"$n(A_1\cup A_2\cup A_3)=3\times48-3\times24+16=88$<br>"
         r"よって、どの夫婦も隣り合わない座り方は　$120-88=\boldsymbol{32}$（通り）",
  "note": r"夫婦の数が増えても同じ方法で数えられ、$n$ 組のときは $\displaystyle\sum_{k=0}^{n}(-1)^k\,{}_n\mathrm{C}_k\,2^k\,(2n-k-1)!$ となる。男女交互という条件がつくと、さらに難しい問題になる（5.7 節）。",
  "ex": r"4 組の夫婦 8 人が円形のテーブルのまわりに等間隔に座る。どの夫婦も隣り合わない座り方は何通りか（回転して一致するものは同じとみなす）。",
  "exa": r"1488 通り"},
 {"lv": 5, "title": "立方体を3色以下で塗る（回転で同じものを除く）",
  "q": r"立方体の各面を、赤・青・黄の 3 色のいずれかで塗る。使わない色があってもよく、隣り合う面が同じ色でもよい。立方体を回転させて一致する塗り方は同じとみなすとき、塗り方は何通りあるか。",
  "hint": r"色ごとの面の数の組（例えば 3 面・2 面・1 面）で分類し、それぞれについて<b>面の配置の型</b>（同色の面が向かい合うか隣り合うか）を調べ、色の割り当て方を掛ける。$3^6$ を 24 で割るのは誤り（回転で動かない塗り方があるため）。",
  "sol": r"3 色の面の数を多い順に並べた組で分類する。立方体の 2 面は「向かい合う」か「隣り合う」かのどちらかである。<br>"
         r"(i) $(6)$：1 色だけ。色の選び方 3 通り。<br>"
         r"(ii) $(5,1)$：1 面だけの色の面の配置は 1 通り。色の割り当て $3\times2=6$ 通り。<br>"
         r"(iii) $(4,2)$：2 面の色の 2 面が向かい合うか隣り合うかの 2 通り。色の割り当て $3\times2=6$ 通りで $12$ 通り。<br>"
         r"(iv) $(4,1,1)$：1 面ずつの 2 色の面が向かい合うか隣り合うかの 2 通り。この 2 面の色を入れかえたものは、向かい合うときは上下をひっくり返す回転で、隣り合うときは 2 面の共通の辺の中点と向かいの辺の中点を結ぶ直線のまわりの $180^\circ$ 回転で一致する。4 面の色の選び方 3 通りで $2\times3=6$ 通り。<br>"
         r"(v) $(3,3)$：一方の色の 3 面は、1 つの頂点に集まる 3 面（向かい合う 2 面を含まない）か、向かい合う 2 面とその間の 1 面かの 2 通り。どちらの場合も残りの 3 面は同じ形で、色を入れかえたものと回転で一致する。使う 2 色の選び方 3 通りで $2\times3=6$ 通り。<br>"
         r"(vi) $(3,2,1)$：1 面の色の面を上面に置く。下面が 2 面の色のとき、側面は 3 面の色 3 つと 2 面の色 1 つで 1 通り。下面が 3 面の色のとき、側面は 2 色が 2 面ずつで、2 面の色の 2 面が隣り合うか向かい合うかの 2 通り。計 3 通り。色の割り当て $3!=6$ 通りで $3\times6=18$ 通り。<br>"
         r"(vii) $(2,2,2)$：同色の 2 面が向かい合う色の数で分ける。<br>"
         r"　・3 色とも向かい合う：3 組の向かい合う面に 3 色を割り当てるが、どの割り当ても回転で移り合う（$90^\circ$ 回転で 2 組を入れかえられる）ので 1 通り。<br>"
         r"　・ちょうど 1 色が向かい合う：その色（3 通り）を上下に塗ると、側面は同色が隣り合うように 2 面ずつ塗られ、上下軸のまわりの回転ですべて一致するので 3 通り。<br>"
         r"　・どの色も向かい合わない：赤を上面と前面に塗る。左右の面は向かい合うので青と黄が 1 面ずつ、下面と後面も青と黄が 1 面ずつで、$2\times2=4$ 通り。赤の 2 面を赤の 2 面に移す回転は、何もしない回転と、上面と前面の共通の辺の中点および下面と後面の共通の辺の中点を通る直線のまわりの $180^\circ$ 回転だけである。後者は上面と前面、下面と後面、左面と右面をそれぞれ入れかえるので、4 通りは 2 通りずつ一致する。よって 2 通り。<br>"
         r"　ちょうど 2 色が向かい合うことはない（残りの 2 面も向かい合う 2 面になるから）。計 $1+3+2=6$ 通り。<br>"
         r"以上より　$3+6+12+6+6+18+6=\boldsymbol{57}$（通り）",
  "note": r"回転で一致するものも別々に数えると塗り方は $3^6=729$ 通りあるが、全面赤のように回転しても変わらない塗り方は 24 通りずつ重なってはいない。重なり方が塗り方によって違うので $729\div24$ のような割り算はできない（実際 729 は 24 で割り切れない）。色の数の組ごとに型を調べるのが確実である。",
  "ex": r"正四面体の各面を、異なる 4 色のいずれかで塗る（使わない色があってもよく、隣り合う面が同じ色でもよい）。回転させて一致する塗り方は同じとみなすとき、塗り方は何通りあるか。",
  "exa": r"36 通り"},
]})


def v2():
    P = list(permutations(range(7)))          # 0〜3 男子, 4〜6 女子
    girl = lambda p, i: p[i] >= 4
    def girls_block(p):
        idx = [i for i in range(7) if p[i] >= 4]; return idx[-1] - idx[0] == 2
    assert ncount(p for p in P if girls_block(p)) == 720
    assert ncount(p for p in P if all(not (girl(p, i) and girl(p, i + 1)) for i in range(6))) == 1440
    assert ncount(p for p in P if p[0] < 4 and p[6] < 4) == 1440
    # 練習：0〜4 男子, 5,6 女子
    assert ncount(p for p in P if abs(p.index(5) - p.index(6)) == 1) == 1440
    assert ncount(p for p in P if abs(p.index(5) - p.index(6)) != 1) == 3600
    assert ncount(p for p in P if p[0] < 5 and p[6] < 5) == 2400
    # 重複順列
    assert ncount(product("123", repeat=5)) == 243
    assert ncount(p for p in product("012", repeat=5) if p[0] != "0") == 162
    for n, a, b, c in [(5, 32, 30, 15), (6, 64, 62, 31)]:
        R = list(product("AB", repeat=n))
        assert len(R) == a and ncount(r for r in R if len(set(r)) == 2) == b
        parts = {frozenset([frozenset(i for i in range(n) if r[i] == "A"), frozenset(i for i in range(n) if r[i] == "B")]) for r in R if len(set(r)) == 2}
        assert len(parts) == c
    # 0 を含む数字の整数
    N4 = [p for p in permutations(range(6), 4) if p[0] != 0]
    assert len(N4) == 300 and ncount(p for p in N4 if p[3] % 2 == 0) == 156 and ncount(p for p in N4 if sum(p) % 3 == 0) == 96
    assert 24 + 4 * 18 == 96
    N3 = [p for p in permutations(range(5), 3) if p[0] != 0]
    assert len(N3) == 48 and ncount(p for p in N3 if p[2] % 2 == 0) == 30 and ncount(p for p in N3 if sum(p) % 3 == 0) == 20
    # 辞書式
    L = ["".join(p) for p in sorted(permutations("abcde"))]
    assert L.index("cbeda") + 1 == 60 and L[74] == "dacbe" and L[0] == "abcde" and L[119] == "edcba"
    L = ["".join(p) for p in sorted(permutations("12345"))]
    assert L.index("35142") + 1 == 68 and L[99] == "51342"
    # 円順列：8 人（0〜3 大人, 0 が A；4〜7 子ども, 4 が B）。席 0〜7 に p[s] が座る
    def canon(p):
        k = p.index(0); return p[k:] + p[:k]
    C8 = {canon(p) for p in permutations(range(8))}
    assert len(C8) == 5040
    assert ncount(c for c in C8 if all((c[i] < 4) != (c[(i + 1) % 8] < 4) for i in range(8))) == 144
    assert ncount(c for c in C8 if c[4] == 4) == 720       # A は席 0，正面は席 4
    assert circ_classes(permutations(range(8)), reflect=True) == 2520
    C6 = {canon(p) for p in permutations(range(6))}      # 0〜2 男子(0 が A), 3〜5 女子(3 が B)
    assert ncount(c for c in C6 if all((c[i] < 3) != (c[(i + 1) % 6] < 3) for i in range(6))) == 12
    assert ncount(c for c in C6 if c[1] == 3 or c[5] == 3) == 48
    assert circ_classes(permutations(range(6)), reflect=True) == 60
    # 塗り分け A,B,C,D,E = 0..4
    adj = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (2, 3), (3, 4), (4, 1)]
    def paints(k):
        return [c for c in product(range(k), repeat=5) if all(c[a] != c[b] for a, b in adj)]
    P5 = paints(5)
    assert len(P5) == 420 and ncount(c for c in P5 if len(set(c)) == 5) == 120 and ncount(c for c in P5 if len(set(c)) == 4) == 240
    assert ncount(c for c in P5 if len(set(c)) == 3) == 60
    assert ncount(c for c in paints(4) if len(set(c)) == 4) == 48 and len(paints(6)) == 1560
    # 立方体の塗り分け
    assert len(CUBE) == 24 and len(TETRA) == 12 and len(PRISM) == 6
    assert orbits(list(permutations(range(6))), CUBE) == 30
    cadj = [(a, b) for a in range(6) for b in range(a + 1, 6) if {a, b} not in ({0, 1}, {2, 3}, {4, 5})]
    five = [c for c in product(range(5), repeat=6) if len(set(c)) == 5 and all(c[a] != c[b] for a, b in cadj)]
    assert orbits(five, CUBE) == 15
    assert orbits(list(permutations(range(5))), PRISM) == 20
    four = [c for c in product(range(4), repeat=6) if len(set(c)) == 4 and all(c[a] != c[b] for a, b in cadj)]
    assert orbits(four, CUBE) == 6
    # 夫婦が隣り合わない（席を円形に、人 0 を席 0 に固定）
    def couples(n):
        cnt = 0
        for q in permutations(range(1, 2 * n)):
            c = (0,) + q
            if all(c[i] // 2 != c[(i + 1) % (2 * n)] // 2 for i in range(2 * n)):
                cnt += 1
        return cnt
    assert couples(3) == 32 and couples(4) == 1488
    assert 120 - (3 * 48 - 3 * 24 + 16) == 32
    assert sum((-1)**k * comb(4, k) * 2**k * factorial(8 - k - 1) for k in range(5)) == 1488
    # 3 色以下の立方体
    allc = list(product(range(3), repeat=6))
    assert orbits(allc, CUBE) == 57
    def by_type(t):
        return orbits([c for c in allc if tuple(sorted([c.count(i) for i in range(3) if c.count(i)], reverse=True)) == t], CUBE)
    assert [by_type(t) for t in [(6,), (5, 1), (4, 2), (4, 1, 1), (3, 3), (3, 2, 1), (2, 2, 2)]] == [3, 6, 12, 6, 6, 18, 6]
    assert orbits(list(product(range(4), repeat=4)), TETRA) == 36


VCHECKS.append(v2)


# ---------------------------------------------------------------- 節3
SEC.append({"title": "組合せと組分け",
"base": r"""・異なる $n$ 個から $r$ 個取る組合せ：${}_n\mathrm{C}_r=\dfrac{{}_n\mathrm{P}_r}{r!}=\dfrac{n!}{r!\,(n-r)!}$，${}_n\mathrm{C}_r={}_n\mathrm{C}_{n-r}$<br>
・組分け：まず組に名前をつけて（区別して）数え、組に区別がないときは、人数が同じ組の数を $k$ として $k!$ で割る<br>
・「少なくとも 1 つ」は余事象を考える。条件が複雑なときは、<b>1 対 1 に対応する数えやすいもの</b>に置きかえる""",
"items": [
 {"lv": 1, "title": "組合せの基本（少なくとも1人を含む）",
  "q": r"男子 6 人、女子 4 人の中から 4 人の委員を選ぶとき、次の選び方は何通りあるか。<br>(1) 選び方の総数　(2) 男子 2 人、女子 2 人を選ぶ　(3) 女子を少なくとも 1 人含む　(4) 特定の男子 A を含み、特定の女子 B を含まない",
  "hint": r"選ぶ順序は関係ないので組合せ。(2) は男子の選び方と女子の選び方の積。(3) は余事象「全員男子」を全体から引く。(4) は A を先に入れ、B を除いた残りから選ぶ。",
  "sol": r"(1) ${}_{10}\mathrm{C}_4=\boldsymbol{210}$（通り）<br>"
         r"(2) ${}_6\mathrm{C}_2\times{}_4\mathrm{C}_2=15\times6=\boldsymbol{90}$（通り）<br>"
         r"(3) 全員男子の選び方は ${}_6\mathrm{C}_4=15$ 通りなので　$210-15=\boldsymbol{195}$（通り）<br>"
         r"(4) A を選び、A，B 以外の 8 人から 3 人を選べばよいから　${}_8\mathrm{C}_3=\boldsymbol{56}$（通り）",
  "note": r"(3) を「女子 1 人を先に選んで ${}_4\mathrm{C}_1$，残り 9 人から 3 人で ${}_9\mathrm{C}_3$」と ${}_4\mathrm{C}_1\times{}_9\mathrm{C}_3=336$ とするのは誤り。女子を 2 人以上含む選び方を重複して数えている。",
  "ex": r"男子 7 人、女子 5 人の中から 5 人を選ぶとき、(1) 選び方の総数　(2) 男子 3 人、女子 2 人を選ぶ　(3) 女子を少なくとも 1 人含む　(4) 特定の男子 A を含み、特定の女子 B を含まない 選び方はそれぞれ何通りか。",
  "exa": r"(1) 792 通り　(2) 350 通り　(3) 771 通り　(4) 210 通り"},
 {"lv": 2, "title": "組分け（組の区別の有無）",
  "q": r"9 人を次のように分ける方法は何通りあるか。<br>(1) 3 人ずつ A，B，C の 3 つの部屋に入れる　(2) 3 人ずつの 3 組に分ける<br>(3) 2 人、3 人、4 人の 3 組に分ける　(4) 2 人、2 人、5 人の 3 組に分ける",
  "hint": r"部屋（名前のついた組）に入れる方法をまず数える。組に区別がないときは、<b>人数が同じ組どうしを入れかえても同じ分け方</b>なので、その入れかえの数で割る。人数がすべて異なる組は、人数で区別がつく。",
  "sol": r"(1) A に入る 3 人を選び、残り 6 人から B に入る 3 人を選ぶと、C に入る 3 人は決まる。<br>　${}_9\mathrm{C}_3\times{}_6\mathrm{C}_3=84\times20=\boldsymbol{1680}$（通り）<br>"
         r"(2) (1) の入れ方で部屋の区別をなくすと、1 つの分け方に部屋の名前のつけ方 $3!$ 通りが対応するから　$1680\div3!=\boldsymbol{280}$（通り）<br>"
         r"(3) 組の人数がすべて異なるので、組は人数で区別できる。　${}_9\mathrm{C}_2\times{}_7\mathrm{C}_3=36\times35=\boldsymbol{1260}$（通り）<br>"
         r"(4) 2 人の組 2 つは区別がつかないので、区別して数えた ${}_9\mathrm{C}_2\times{}_7\mathrm{C}_2$ を $2!$ で割る。<br>　$\dfrac{36\times21}{2}=\boldsymbol{378}$（通り）",
  "note": r"(2) で $3!$ で割るのを忘れる、(4) で 2 で割るのを忘れる、(3) で不要な割り算をする、の 3 つが典型的な誤り。「名前をつけて数える → 名前の重なりで割る」と覚える。",
  "ex": r"8 人を次のように分ける方法は何通りあるか。(1) 4 人ずつの 2 組に分ける　(2) 2 人ずつの 4 組に分ける　(3) 2 人、3 人、3 人の 3 組に分ける",
  "exa": r"(1) 35 通り　(2) 105 通り　(3) 280 通り"},
 {"lv": 3, "title": "隣り合わない数の選び方（直線と円周）",
  "q": r"(1) 1 から 20 までの 20 個の整数から、どの 2 つも連続しないように 3 個を選ぶ方法は何通りか。<br>"
       r"(2) 円周上に等間隔に並んだ 20 個の点から、どの 2 点も隣り合わないように 3 点を選ぶ方法は何通りか。",
  "hint": r"(1) 選んだ数を $a<b<c$ とし、$b-1,\ c-2$ と<b>ずらす</b>と「連続しない」条件が消え、ふつうの組合せに 1 対 1 に対応する。(2) は円周を 1 か所で切って直線の場合に帰着する。特定の点 $\mathrm{P}_1$ を選ぶか選ばないかで分ける。",
  "sol": r"(1) 選ぶ 3 数を $a<b<c$ とすると、条件は $b\geqq a+2,\ c\geqq b+2$。$a'=a,\ b'=b-1,\ c'=c-2$ とおくと<br>"
         r"$1\leqq a'<b'<c'\leqq18$<br>"
         r"となり、逆にこれを満たす $(a',b',c')$ から $(a,b,c)=(a',b'+1,c'+2)$ により条件を満たす 3 数が 1 つずつ得られる。よって、1 から 18 までの整数から異なる 3 数を選ぶ方法と 1 対 1 に対応し　${}_{18}\mathrm{C}_3=\boldsymbol{816}$（通り）<br>"
         r"(2) 点を順に $\mathrm{P}_1,\ \mathrm{P}_2,\ \cdots,\ \mathrm{P}_{20}$ とする。<br>"
         r"・$\mathrm{P}_1$ を選ぶとき：$\mathrm{P}_2,\ \mathrm{P}_{20}$ は選べない。直線状に並ぶ $\mathrm{P}_3,\ \cdots,\ \mathrm{P}_{19}$ の 17 個から隣り合わない 2 個を選ぶ。(1) と同様に $b'=b-1$ とずらすと 16 個から 2 個を選ぶことになり　${}_{16}\mathrm{C}_2=120$ 通り<br>"
         r"・$\mathrm{P}_1$ を選ばないとき：直線状に並ぶ $\mathrm{P}_2,\ \cdots,\ \mathrm{P}_{20}$ の 19 個から隣り合わない 3 個を選ぶ。(1) と同様に　${}_{17}\mathrm{C}_3=680$ 通り<br>"
         r"よって　$120+680=\boldsymbol{800}$（通り）",
  "note": r"一般に、直線上の $n$ 個から隣り合わない $k$ 個を選ぶ方法は ${}_{n-k+1}\mathrm{C}_k$ 通り（選ばない $n-k$ 個の間と両端の $n-k+1$ か所から $k$ か所を選ぶ、と考えてもよい）。円周上では ${}_{n-k}\mathrm{C}_k+{}_{n-k-1}\mathrm{C}_{k-1}$ 通りとなる。(2) は「$\mathrm{P}_1$ を含む選び方 120 通り」を 20 倍すると各選び方を 3 回ずつ数えるので、$120\times20\div3=800$ としてもよい。",
  "ex": r"(1) 1 から 15 までの整数から、どの 2 つも連続しないように 4 個を選ぶ方法は何通りか。<br>(2) 円周上に等間隔に並んだ 15 個の点から、どの 2 点も隣り合わないように 4 点を選ぶ方法は何通りか。",
  "exa": r"(1) 495 通り　(2) 450 通り"},
 {"lv": 3, "title": "和や積が倍数になる選び方（余りで分類）",
  "q": r"1 から 30 までの 30 個の整数から異なる 3 個を選ぶ。<br>(1) 3 個の数の和が 3 の倍数になる選び方は何通りか。　(2) 3 個の数の積が 9 の倍数になる選び方は何通りか。",
  "hint": r"(1) 3 で割った余りが 0，1，2 の数はそれぞれ 10 個ずつ。和が 3 の倍数になる<b>余りの組合せ</b>を考える。(2) 積が 9 の倍数 $\iff$ 素因数 3 を合わせて 2 個以上含む。条件が複雑なので<b>余事象</b>（3 を 1 個以下しか含まない）を数える。",
  "sol": r"(1) 3 で割った余りが 0，1，2 である数の集合を $R_0,\ R_1,\ R_2$ とすると、どれも 10 個ずつ。<br>"
         r"3 数の余りの和が 3 の倍数になるのは、3 数が同じ集合から選ばれる場合と、$R_0,\ R_1,\ R_2$ から 1 個ずつ選ばれる場合である。<br>"
         r"$3\times{}_{10}\mathrm{C}_3+10^3=3\times120+1000=\boldsymbol{1360}$（通り）<br>"
         r"(2) 3 の倍数は 10 個あり、そのうち 9 の倍数は 9，18，27 の 3 個、9 の倍数でない 3 の倍数は 7 個。3 の倍数でない数は 20 個。<br>"
         r"積が 9 の倍数にならないのは、次の場合である。<br>"
         r"・3 の倍数を含まない：${}_{20}\mathrm{C}_3=1140$ 通り<br>"
         r"・3 の倍数をちょうど 1 個含み、それが 9 の倍数でない：$7\times{}_{20}\mathrm{C}_2=7\times190=1330$ 通り<br>"
         r"選び方の総数は ${}_{30}\mathrm{C}_3=4060$ 通りであるから　$4060-1140-1330=\boldsymbol{1590}$（通り）",
  "note": r"(2) を直接数えるなら「9 の倍数を含む」か「3 の倍数を 2 個以上含む」の和集合を考えることになり、重なりの処理が面倒になる。「何の倍数か」の条件は、素因数の個数で言いかえてから余事象を考えるのが定石。",
  "ex": r"1 から 20 までの整数から異なる 3 個を選ぶ。(1) 3 個の和が 3 の倍数になる選び方は何通りか。　(2) 3 個の積が 4 の倍数になる選び方は何通りか。",
  "exa": r"(1) 384 通り　(2) 795 通り"},
 {"lv": 5, "title": "マス目に○を置く（各行・各列にちょうど2個）",
  "q": r"5×5 のマス目の 25 個のマスのうち 10 個に○を書く。どの行にも、どの列にもちょうど 2 個の○があるような書き方は何通りあるか。ただし、回転や裏返しで一致するものも異なるものとして数える。",
  "hint": r"1 行ずつ決めていくと場合分けが膨大になる。<b>各行の 2 個の○を横の線分で、各列の 2 個の○を縦の線分で結ぶ</b>と、○は横と縦の線分が交互に現れる閉じた折れ線（ループ）に分かれる。ループが何行・何列を通るかで分類し、ループの個数を順列で数える。",
  "sol": r"各行の 2 個の○を横の線分で、各列の 2 個の○を縦の線分で結ぶ。どの○からも横と縦の線分が 1 本ずつ出ているので、線分をたどると横・縦が交互に現れてもとの○に戻る。こうして○全体はいくつかの閉じた折れ線（ループ）に分かれ、各行・各列はちょうど 1 つのループに属する。<br>"
         r"1 つのループが通る行の数と列の数は等しい。これを $k$ とすると、ループは $2k$ 個の○を含み、$k\geqq2$ である。逆に、5 つの行と 5 つの列を、行と列の数が等しい組（2 つ以上ずつ）に分け、各組でループを 1 つずつ作れば、条件を満たす書き方が 1 つ決まる。<br>"
         r"<b>ループの個数</b>　指定された $k$ 行と $k$ 列を通るループの個数を $L_k$ とする。ループは<br>"
         r"行 $r_1$ → 列 $c_1$ → 行 $r_2$ → 列 $c_2$ → $\cdots$ → 行 $r_k$ → 列 $c_k$ → 行 $r_1$<br>"
         r"とたどることで表され、○は $(r_1,c_1),\ (r_2,c_1),\ (r_2,c_2),\ \cdots,\ (r_k,c_k),\ (r_1,c_k)$ の $2k$ マスにある。$r_1$ を指定された行のうち最も上の行とすると、$r_2,\cdots,r_k$ の順序が $(k-1)!$ 通り、$c_1,\cdots,c_k$ の順序が $k!$ 通り。同じループを逆向きにたどったものも同じループを表すから<br>"
         r"$L_k=\dfrac{k!\,(k-1)!}{2}$　より　$L_2=1,\ L_3=6,\ L_5=\dfrac{120\times24}{2}=1440$<br>"
         r"<b>分類</b>　5 を 2 以上の整数の和に分けると $5$，$2+3$ の 2 通り。<br>"
         r"(i) ループ 1 つ（5 行 5 列）：$L_5=1440$ 通り<br>"
         r"(ii) 2 行 2 列のループと 3 行 3 列のループ：2 行 2 列のループが通る行と列の選び方は ${}_5\mathrm{C}_2\times{}_5\mathrm{C}_2=100$ 通りで、$100\times L_2\times L_3=600$ 通り<br>"
         r"よって　$1440+600=\boldsymbol{2040}$（通り）",
  "note": r"$L_2=1$ のループは 2 行 2 列の交わる 4 マスすべてに○がある形である。同じ方法で 4×4 のマス目の場合は、$4$ と $2+2$ に分けて $L_4+\dfrac{{}_4\mathrm{C}_2\times{}_4\mathrm{C}_2}{2}\times L_2^{\,2}=72+18=90$ 通りとなる（2+2 では 2 つのループに区別がないので 2 で割る）。",
  "ex": r"6×6 のマス目の 36 個のマスのうち 12 個に○を書く。どの行にも、どの列にもちょうど 2 個の○があるような書き方は何通りあるか（回転や裏返しで一致するものも区別する）。",
  "exa": r"67950 通り"},
]})


def two_per_line(n):
    """n×n で各行各列ちょうど 2 個（各行の 2 列を列の残り容量を見ながら全部たどる）"""
    pairs = list(combinations(range(n), 2))
    def rec(r, cap):
        if r == n:
            return 1
        t = 0
        for a, b in pairs:
            if cap[a] and cap[b]:
                cap[a] -= 1; cap[b] -= 1
                t += rec(r + 1, cap)
                cap[a] += 1; cap[b] += 1
        return t
    return rec(0, [2] * n)


def v3():
    people = ["M%d" % i for i in range(6)] + ["F%d" % i for i in range(4)]
    S = list(combinations(people, 4))
    assert len(S) == 210
    assert ncount(s for s in S if sum(p[0] == "M" for p in s) == 2) == 90
    assert ncount(s for s in S if any(p[0] == "F" for p in s)) == 195
    assert ncount(s for s in S if "M0" in s and "F0" not in s) == 56
    assert comb(4, 1) * comb(9, 3) == 336
    people = ["M%d" % i for i in range(7)] + ["F%d" % i for i in range(5)]
    S = list(combinations(people, 5))
    assert len(S) == 792 and ncount(s for s in S if sum(p[0] == "M" for p in s) == 3) == 350
    assert ncount(s for s in S if any(p[0] == "F" for p in s)) == 771 and ncount(s for s in S if "M0" in s and "F0" not in s) == 210
    # 組分け
    def partitions(n, sizes, labeled):
        k = len(sizes); res = set()
        for lab in product(range(k), repeat=n):
            blocks = [frozenset(i for i in range(n) if lab[i] == j) for j in range(k)]
            if sorted(len(b) for b in blocks) != sorted(sizes):
                continue
            if labeled:
                if [len(b) for b in blocks] == list(sizes): res.add(tuple(blocks))
            else:
                res.add(frozenset(blocks))
        return len(res)
    assert partitions(9, (3, 3, 3), True) == 1680 and partitions(9, (3, 3, 3), False) == 280
    assert partitions(9, (2, 3, 4), False) == 1260 and partitions(9, (2, 2, 5), False) == 378
    assert partitions(8, (4, 4), False) == 35 and partitions(8, (2, 2, 2, 2), False) == 105 and partitions(8, (2, 3, 3), False) == 280
    # 隣り合わない
    def lin(n, k): return ncount(c for c in combinations(range(n), k) if all(c[i + 1] - c[i] >= 2 for i in range(k - 1)))
    def cir(n, k): return ncount(c for c in combinations(range(n), k) if all((c[(i + 1) % k] - c[i]) % n >= 2 for i in range(k)))
    assert lin(20, 3) == 816 == comb(18, 3) and cir(20, 3) == 800
    assert ncount(c for c in combinations(range(20), 3) if 0 in c and all((c[(i + 1) % 3] - c[i]) % 20 >= 2 for i in range(3))) == 120
    assert lin(17, 2) == 120 and lin(19, 3) == 680
    assert lin(15, 4) == 495 and cir(15, 4) == 450
    # 和・積
    S = list(combinations(range(1, 31), 3))
    assert len(S) == 4060 and ncount(s for s in S if sum(s) % 3 == 0) == 1360
    assert ncount(s for s in S if s[0] * s[1] * s[2] % 9 == 0) == 1590
    assert ncount(s for s in S if all(x % 3 for x in s)) == 1140
    assert ncount(s for s in S if sum(x % 3 == 0 for x in s) == 1 and all(x % 9 for x in s)) == 1330
    S = list(combinations(range(1, 21), 3))
    assert ncount(s for s in S if sum(s) % 3 == 0) == 384 and ncount(s for s in S if s[0] * s[1] * s[2] % 4 == 0) == 795
    # マス目（5×5 は全列挙、ほかは全探索）
    rows5 = list(combinations(range(5), 2))
    cnt = 0
    for R in product(rows5, repeat=5):
        col = [0] * 5
        for a, b in R:
            col[a] += 1; col[b] += 1
        if col == [2] * 5:
            cnt += 1
    assert cnt == 2040 == two_per_line(5)
    L = lambda k: factorial(k) * factorial(k - 1) // 2
    assert L(5) + comb(5, 2)**2 * L(2) * L(3) == 2040
    assert two_per_line(3) == 6 == L(3) and two_per_line(4) == 90 == L(4) + comb(4, 2)**2 // 2
    assert two_per_line(6) == 67950 == L(6) + comb(6, 2)**2 * L(4) + comb(6, 3)**2 // 2 * L(3)**2 + 15 * 15 * 6


VCHECKS.append(v3)


# ---------------------------------------------------------------- 節4（図は座標を計算して作る）
def grid_paths(W, H, removed=(), avoid=()):
    """格子 (0,0)→(W,H) の最短経路数を各点について求める（removed: 通れない区間, avoid: 通れない点）"""
    rem = {frozenset(e) for e in removed}
    N = {}
    for x in range(W + 1):
        for y in range(H + 1):
            if (x, y) in avoid:
                N[(x, y)] = 0; continue
            if (x, y) == (0, 0):
                N[(x, y)] = 1; continue
            s = 0
            if x > 0 and frozenset([(x - 1, y), (x, y)]) not in rem: s += N[(x - 1, y)]
            if y > 0 and frozenset([(x, y - 1), (x, y)]) not in rem: s += N[(x, y - 1)]
            N[(x, y)] = s
    return N


def grid_fig(W, H, removed=(), pond=None, cross=(), pts=(), nums=None, sp=30, ox=24, oy=18):
    X = lambda x: ox + sp * x
    Y = lambda y: oy + sp * (H - y)
    w, h = X(W) + 24, Y(0) + 22
    rem = {frozenset(e) for e in removed}
    out = [f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
    if pond:
        (x0, y0), (x1, y1) = pond
        out.append(f'<rect x="{X(x0)}" y="{Y(y1)}" width="{sp * (x1 - x0)}" height="{sp * (y1 - y0)}" fill="#cfe3f5"/>')
    seg = []
    for x in range(W + 1):
        for y in range(H + 1):
            for (dx, dy) in ((1, 0), (0, 1)):
                a, b = (x, y), (x + dx, y + dy)
                if b[0] > W or b[1] > H or frozenset([a, b]) in rem:
                    continue
                seg.append(f'M{X(a[0])} {Y(a[1])} L{X(b[0])} {Y(b[1])}')
    out.append(f'<path d="{" ".join(seg)}" stroke="#333" stroke-width="1.2" fill="none"/>')
    for (a, b) in cross:
        mx, my = (X(a[0]) + X(b[0])) / 2, (Y(a[1]) + Y(b[1])) / 2
        out.append(f'<path d="M{mx - 4} {my - 4} L{mx + 4} {my + 4} M{mx - 4} {my + 4} L{mx + 4} {my - 4}" stroke="#c0392b" stroke-width="2"/>')
    out.append(f'<g font-size="12"><text x="{X(0) - 16}" y="{Y(0) + 15}">A</text><text x="{X(W) + 5}" y="{Y(H) - 4}">B</text>')
    for (name, (x, y)) in pts:
        out.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="3" fill="#16367a"/><text x="{X(x) + 4}" y="{Y(y) - 4}">{name}</text>')
    out.append('</g>')
    if nums:
        out.append('<g font-size="10" fill="#1f5fbf" text-anchor="end">')
        for (x, y), v in sorted(nums.items()):
            if (x, y) in ((0, 0),) or v == 0 and pond:
                continue
            out.append(f'<text x="{X(x) - 2}" y="{Y(y) - 2}">{v}</text>')
        out.append('</g>')
    out.append('</svg>')
    return "".join(out)


G43_REM = [((3, 1), (3, 2)), ((3, 2), (3, 3)), ((2, 2), (3, 2)), ((3, 2), (4, 2))]   # 池の中の道
G43_X = [((1, 1), (1, 2))]                                                             # 通行止め
G43_N = grid_paths(6, 4, removed=G43_REM + G43_X, avoid={(3, 2)})
FIG42 = grid_fig(6, 4, pts=[("P", (2, 1)), ("Q", (4, 2))])
FIG43Q = grid_fig(6, 4, removed=G43_REM, pond=((2, 1), (4, 3)), cross=G43_X)
FIG43S = grid_fig(6, 4, removed=G43_REM, pond=((2, 1), (4, 3)), cross=G43_X, nums={k: v for k, v in G43_N.items() if k != (3, 2)})

SEC.append({"title": "同じものを含む順列と最短経路",
"base": r"""・$a$ が $p$ 個、$b$ が $q$ 個、$c$ が $r$ 個（$p+q+r=n$）の並べ方は $\dfrac{n!}{p!\,q!\,r!}={}_n\mathrm{C}_p\times{}_{n-p}\mathrm{C}_q$ 通り<br>
・並ぶ順序が指定されたものは、同じものとみなして並べ、あとで順に割り当てる<br>
・最短経路：右へ $m$ 回、上へ $n$ 回進む経路は ${}_{m+n}\mathrm{C}_m$ 通り（→ $m$ 個と ↑ $n$ 個の並べ方）<br>
・通れない道があるときは、各交差点に「そこまでの経路数」を書き込む（左の点の数 $+$ 下の点の数）。これを<b>加え上げ</b>という""",
"items": [
 {"lv": 1, "title": "同じものを含む順列（順序の指定を含む）",
  "q": r"SUCCESS の 7 文字を 1 列に並べる。<br>(1) 並べ方は全部で何通りか。　(2) 3 個の S が続いて並ぶ並べ方は何通りか。　(3) U が E より左にある並べ方は何通りか。",
  "hint": r"S が 3 個、C が 2 個、U と E が 1 個ずつ。(2) は SSS をまとめて 1 文字とみなす。(3) は U，E を<b>同じ文字 □ とみなして</b>並べ、左の □ を U、右の □ を E とする。",
  "sol": r"(1) S 3 個、C 2 個、U 1 個、E 1 個の並べ方で　$\dfrac{7!}{3!\,2!}=\boldsymbol{420}$（通り）<br>"
         r"(2) SSS を 1 文字とみなすと、SSS，C，C，U，E の 5 文字の並べ方で　$\dfrac{5!}{2!}=\boldsymbol{60}$（通り）<br>"
         r"(3) U，E を同じ文字 □ とみなすと、S 3 個、C 2 個、□ 2 個の並べ方は $\dfrac{7!}{3!\,2!\,2!}=210$ 通り。その各々で左の □ を U、右の □ を E とすれば、条件を満たす並べ方がちょうど 1 つずつ得られる。よって　$\boldsymbol{210}$ 通り",
  "note": r"(3) は「U が E より左」と「E が U より左」が U と E の入れかえで 1 対 1 に対応することから、$420\div2=210$ としてもよい。3 文字以上の順序を指定するときは □ の方法が便利。",
  "ex": r"ADDITION の 8 文字を 1 列に並べる。(1) 並べ方は全部で何通りか。　(2) 2 個の D が隣り合う並べ方は何通りか。　(3) A，T，O が左からこの順に並ぶ（間に他の文字があってもよい）並べ方は何通りか。",
  "exa": r"(1) 10080 通り　(2) 2520 通り　(3) 1680 通り"},
 {"lv": 2, "title": "最短経路の個数（通る点・通らない点）",
  "q": FIG42 + r"図のような碁盤目状の道がある。A 地点から B 地点まで遠回りしないで行く道順について、次のものは何通りあるか。<br>"
       r"(1) 道順の総数　(2) P 地点を通る道順　(3) P 地点も Q 地点も通らない道順",
  "hint": r"右へ 6 回、上へ 4 回進むので、→ 6 個と ↑ 4 個の並べ方。P を通る道順は「A→P」と「P→B」の積。(3) は P を通る集合と Q を通る集合の<b>和集合の補集合</b>として包除を使う。",
  "sol": r"右へ 1 区画進むことを →、上へ 1 区画進むことを ↑ で表す。<br>"
         r"(1) → 6 個、↑ 4 個の並べ方で　${}_{10}\mathrm{C}_4=\boldsymbol{210}$（通り）<br>"
         r"(2) A→P は → 2 個、↑ 1 個で ${}_3\mathrm{C}_1=3$ 通り、P→B は → 4 個、↑ 3 個で ${}_7\mathrm{C}_3=35$ 通り。　$3\times35=\boldsymbol{105}$（通り）<br>"
         r"(3) Q を通る道順は、A→Q が ${}_6\mathrm{C}_2=15$ 通り、Q→B が ${}_4\mathrm{C}_2=6$ 通りで $90$ 通り。<br>"
         r"P と Q の両方を通る道順は、A→P，P→Q，Q→B がそれぞれ $3,\ {}_3\mathrm{C}_1=3,\ 6$ 通りで $54$ 通り。<br>"
         r"よって、P または Q を通る道順は $105+90-54=141$ 通りで、求める道順は　$210-141=\boldsymbol{69}$（通り）",
  "note": r"「P を通らない」を直接数えるより、「全体 $-$ P を通る」が速い。2 点以上の条件では包除を使う。",
  "ex": r"座標空間で、$x$ 軸、$y$ 軸、$z$ 軸の正の向きのいずれかに 1 ずつ進んで、原点 O から点 $(3,2,2)$ まで行く最短の道順について、(1) 総数　(2) 点 $(1,1,1)$ を通る道順　(3) 点 $(1,1,1)$ も点 $(2,1,1)$ も通らない道順 はそれぞれ何通りか。",
  "exa": r"(1) 210 通り　(2) 72 通り　(3) 102 通り"},
 {"lv": 3, "title": "通れない道がある最短経路（加え上げ）",
  "q": FIG43Q + r"図のような道がある。色をつけた部分は池で、池の中に道はない（池のまわりの道は通れる）。また、× 印の区間は通行止めである。A 地点から B 地点まで遠回りしないで行く道順は何通りあるか。",
  "hint": r"通れない部分が複数あり、包除では重なりの処理が面倒になる。各交差点に「A からそこまでの道順の数」を書き込んでいく<b>加え上げ</b>を使う。ある交差点の数は、左隣と下隣から来る道順の数の和（通れない区間からは来ない）。",
  "sol": FIG43S + r"A から各交差点までの道順の数を、左下から順に書き込む（右図）。各交差点の数は「左の交差点の数 $+$ 下の交差点の数」であるが、池の中の区間や × 印の区間を通って来る分は足さない。<br>"
         r"特に、× 印の区間の上端の点には左からの 1 だけが入り、池の上辺の中央の点には左からの 6 だけ、池の右辺の中央の点には下からの 5 だけが入る。<br>"
         r"このようにして B 地点まで書き込むと、B の数は 88 となる。<br>よって　$\boldsymbol{88}$ 通り",
  "note": r"包除でも解ける。池の中の区間を通る道順は、必ず池の中心の点を通る。全体は ${}_{10}\mathrm{C}_4=210$ 通りで、池の中心を通る道順は ${}_5\mathrm{C}_2\times{}_5\mathrm{C}_2=100$ 通り、× 印の区間を通る道順は $2\times{}_7\mathrm{C}_2=42$ 通り、その両方を通る道順は $2\times1\times{}_5\mathrm{C}_2=20$ 通り。よって $210-(100+42-20)=88$ 通り。通れない部分が多い場合や形が複雑な場合は、加え上げの方が確実である。",
  "ex": r"座標平面上で、$x$ 軸の正の向きまたは $y$ 軸の正の向きに 1 ずつ進んで、原点 O から点 $(5,4)$ まで行く最短の道順のうち、点 $(2,2)$ を通らず、点 $(3,1)$ と点 $(3,2)$ を結ぶ区間も通らないものは何通りか。",
  "exa": r"42 通り"},
 {"lv": 3, "title": "同じものを含む中から取り出して並べる",
  "q": r"1，1，1，2，2，3，3，4 の 8 枚のカードから 4 枚を取り出して 1 列に並べ、4 桁の整数をつくる。整数は何個できるか。",
  "hint": r"取り出した 4 枚の<b>数字の組（同じ数字が何枚ずつか）で場合分け</b>し、それぞれ同じものを含む順列で並べる。同じ数字を何枚まで使えるかに注意。",
  "sol": r"取り出す 4 枚の数字の組で分類する。<br>"
         r"(i) 4 枚とも異なる：$\{1,2,3,4\}$ の 1 組で、並べ方は $4!=24$ 通り<br>"
         r"(ii) 同じ数字 2 枚と異なる数字 2 枚：2 枚使う数字は 1，2，3 のいずれかで 3 通り、残り 2 枚は他の 3 種類から 2 種類で ${}_3\mathrm{C}_2=3$ 通り。組は 9 組で、並べ方は $\dfrac{4!}{2!}=12$ 通りずつ。$9\times12=108$ 通り<br>"
         r"(iii) 同じ数字 2 枚ずつ 2 組：1，2，3 から 2 種類で 3 組、並べ方は $\dfrac{4!}{2!\,2!}=6$ 通りずつ。$3\times6=18$ 通り<br>"
         r"(iv) 同じ数字 3 枚と 1 枚：3 枚使えるのは 1 だけで、残り 1 枚は 2，3，4 の 3 組。並べ方は $\dfrac{4!}{3!}=4$ 通りずつ。$3\times4=12$ 通り<br>"
         r"よって　$24+108+18+12=\boldsymbol{162}$（個）",
  "note": r"(ii) で、2 枚使う数字に 4 を含めないように注意（4 は 1 枚しかない）。4 枚とも同じ数字は使えない。",
  "ex": r"PEPPER の 6 文字から 4 文字を取り出して 1 列に並べる方法は何通りあるか。",
  "exa": r"38 通り"},
 {"lv": 4, "title": "同じものを含む円順列・じゅず順列",
  "q": r"回転して一致する並べ方は同じとみなす。<br>(1) 白玉 4 個、赤玉 2 個、青玉 1 個を円形に並べる方法は何通りか。<br>(2) 白玉 4 個と黒玉 4 個を円形に並べる方法は何通りか。<br>(3) (2) の 8 個の玉に糸を通して首飾りをつくる方法は何通りか（裏返して一致するものも同じとみなす）。",
  "hint": r"(1) 1 個しかない青玉を固定すれば、残りは 1 列に並べるのと同じ。(2) はそのような玉がないので固定できない。白玉と白玉の間にある<b>黒玉の個数の列</b>で並べ方を表し、回転で一致する列をまとめて数える。(3) は列を逆順にしたものが一致するかを調べる。",
  "sol": r"(1) 青玉を固定すると、残り 6 個を青玉の次から時計回りに 1 列に並べることと同じになる。　$\dfrac{6!}{4!\,2!}=\boldsymbol{15}$（通り）<br>"
         r"(2) 白玉を時計回りにたどり、隣り合う白玉の間にある黒玉の個数を順に $b_1,\ b_2,\ b_3,\ b_4$ とする（$b_i\geqq0$，$b_1+b_2+b_3+b_4=4$）。並べ方は、この列を<b>巡回的にずらしたものを同じとみなした</b>ものと 1 対 1 に対応する。数の組で分類すると<br>"
         r"・$\{4,0,0,0\}$：1 通り<br>"
         r"・$\{3,1,0,0\}$：3 を先頭にすると、残りの並びは $(1,0,0),\ (0,1,0),\ (0,0,1)$ の 3 通り<br>"
         r"・$\{2,2,0,0\}$：$(2,2,0,0)$，$(2,0,2,0)$ の 2 通り（$(2,0,0,2)$ は $(2,2,0,0)$ をずらしたもの）<br>"
         r"・$\{2,1,1,0\}$：2 を先頭にすると、残りの並びは $(1,1,0),\ (1,0,1),\ (0,1,1)$ の 3 通り<br>"
         r"・$\{1,1,1,1\}$：1 通り<br>"
         r"よって　$1+3+2+3+1=\boldsymbol{10}$（通り）<br>"
         r"(3) 首飾りを裏返すと、列は逆順になる。逆順にしたものが（ずらしても）自分自身と一致しないのは<br>"
         r"$(3,1,0,0)$ と $(3,0,0,1)$，$(2,1,1,0)$ と $(2,0,1,1)$<br>"
         r"の 4 通りで、各組の 2 つは互いに逆順をずらしたものになっているから、首飾りとしては同じになる。他の 6 通りは逆順にしても（ずらせば）自分自身と一致する。<br>よって　$10-2=\boldsymbol{8}$（通り）",
  "note": r"(2) の別解：1 列に並べる方法 ${}_8\mathrm{C}_4=70$ 通りを、回転による重なりで分類する。WBWBWBWB 型（ずらすと 2 種類の列になる）が 1 通り、WWBBWWBB 型（4 種類の列）が 1 通りで、残り $70-2-4=64$ 通りは 8 種類ずつ重なるから $64\div8=8$ 通り。計 $8+1+1=10$ 通り。$70\div8$ のように単純に割れないのは、回転で自分自身に戻る並べ方があるためである。",
  "ex": r"回転して一致するものは同じとみなす。(1) 白玉 5 個、赤玉 2 個、青玉 1 個を円形に並べる方法は何通りか。(2) 白玉 6 個と黒玉 3 個を円形に並べる方法は何通りか。(3) (2) の 9 個の玉で首飾りをつくる方法は何通りか（裏返して一致するものも同じ）。",
  "exa": r"(1) 21 通り　(2) 10 通り　(3) 7 通り"},
 {"lv": 4, "title": "対角線を越えない最短経路（対称移動の利用）",
  "q": r"座標平面上で、点 $(0,0)$ から出発し、$x$ 軸の正の向きに 1 進むか $y$ 軸の正の向きに 1 進むことを繰り返して、点 $(6,6)$ まで行く。途中で $y>x$ となる点を一度も通らない進み方は何通りあるか。",
  "hint": r"全体から「$y>x$ となる点を通る」進み方を引く。そのような進み方は必ず直線 $y=x+1$ 上の点を通るので、<b>最初にその直線に触れるまでの部分を直線 $y=x+1$ に関して対称移動</b>すると、点 $(-1,1)$ から出発する進み方と 1 対 1 に対応する。",
  "sol": r"進み方の総数は、→ 6 個と ↑ 6 個の並べ方で ${}_{12}\mathrm{C}_6=924$ 通り。<br>"
         r"1 回の移動で $y-x$ は $1$ だけ増えるか減るかするから、$y>x$ となる点を通る進み方は、$y-x=1$ となる点、すなわち直線 $\ell:y=x+1$ 上の点を必ず通る。このような進み方について、最初に $\ell$ 上に来た点を T とし、$(0,0)$ から T までの部分を $\ell$ に関して対称移動する。<br>"
         r"$\ell$ に関する対称移動は $(a,b)\mapsto(b-1,\ a+1)$ で、$(0,0)$ は $(-1,1)$ に移り、→ と ↑ が入れかわる。こうして、$(-1,1)$ から $(6,6)$ まで行く進み方が 1 つ得られる。<br>"
         r"逆に、$(-1,1)$ から $(6,6)$ まで行く進み方は、出発点で $y-x=2$、到着点で $y-x=0$ なので必ず $\ell$ 上の点を通り、最初の通過点までを対称移動すれば、$y>x$ となる点を通る $(0,0)$ からの進み方に戻る。よってこの対応は 1 対 1 である。<br>"
         r"$(-1,1)$ から $(6,6)$ へは → 7 個、↑ 5 個で ${}_{12}\mathrm{C}_5=792$ 通り。<br>"
         r"したがって　$924-792=\boldsymbol{132}$（通り）",
  "note": r"加え上げでも求められる。$y\leqq x$ の範囲の格子点に経路数を書き込むと、直線 $y=x$ 上の点 $(n,n)$ の数は $n=0,1,2,\cdots,6$ に対して $1,\ 1,\ 2,\ 5,\ 14,\ 42,\ 132$ となる（カタラン数）。一般に $(n,n)$ までの個数は ${}_{2n}\mathrm{C}_n-{}_{2n}\mathrm{C}_{n-1}=\dfrac{{}_{2n}\mathrm{C}_n}{n+1}$ で、投票の開票で一方がつねに他方以上である並び方の数などとも同じ構造をもつ。",
  "ex": r"点 $(0,0)$ から、$x$ 軸の正の向きまたは $y$ 軸の正の向きに 1 ずつ進んで点 $(7,4)$ まで行く。途中で $y>x$ となる点を一度も通らない進み方は何通りあるか。",
  "exa": r"165 通り"},
]})


def v4():
    def msperm(s): return len(set(permutations(s)))
    P = set(permutations("SUCCESS"))
    assert len(P) == 420 and ncount(p for p in P if "SSS" in "".join(p)) == 60
    assert ncount(p for p in P if p.index("U") < p.index("E")) == 210
    P = set(permutations("ADDITION"))
    assert len(P) == 10080 and ncount(p for p in P if "DD" in "".join(p)) == 2520
    assert ncount(p for p in P if p.index("A") < p.index("T") < p.index("O")) == 1680
    # 最短経路（上へ進む位置を選ぶ全列挙）
    def walks(W, H):
        for ups in combinations(range(W + H), H):
            x = y = 0; path = [(0, 0)]
            for i in range(W + H):
                if i in ups: y += 1
                else: x += 1
                path.append((x, y))
            yield path
    Wk = list(walks(6, 4))
    assert len(Wk) == 210 and ncount(w for w in Wk if (2, 1) in w) == 105 and ncount(w for w in Wk if (4, 2) in w) == 90
    assert ncount(w for w in Wk if (2, 1) in w and (4, 2) in w) == 54 and ncount(w for w in Wk if (2, 1) not in w and (4, 2) not in w) == 69
    # 空間
    W3 = []
    for seq in set(permutations("xxxyyzz")):
        p = [0, 0, 0]; path = [(0, 0, 0)]
        for c in seq:
            p["xyz".index(c)] += 1; path.append(tuple(p))
        W3.append(path)
    assert len(W3) == 210 and ncount(w for w in W3 if (1, 1, 1) in w) == 72
    assert ncount(w for w in W3 if (1, 1, 1) not in w and (2, 1, 1) not in w) == 102
    # 加え上げの問題：全経路を列挙して、通れない区間を含まないものを数える
    bad = {frozenset(e) for e in G43_REM + G43_X}
    good = [w for w in Wk if all(frozenset([w[i], w[i + 1]]) not in bad for i in range(10))]
    assert len(good) == 88 == G43_N[(6, 4)]
    assert ncount(w for w in Wk if (3, 2) in w) == 100
    Wk2 = list(walks(5, 4))
    ex43 = ncount(w for w in Wk2 if (2, 2) not in w and all({w[i], w[i + 1]} != {(3, 1), (3, 2)} for i in range(9)))
    assert ex43 == grid_paths(5, 4, removed=[((3, 1), (3, 2))], avoid={(2, 2)})[(5, 4)]
    assert ex43 == 42
    assert ncount(w for w in Wk if any({w[i], w[i + 1]} == {(1, 1), (1, 2)} for i in range(10))) == 42
    assert ncount(w for w in Wk if (3, 2) in w and any({w[i], w[i + 1]} == {(1, 1), (1, 2)} for i in range(10))) == 20
    assert [G43_N[(1, 2)], G43_N[(3, 3)], G43_N[(4, 2)]] == [1, 6, 5]
    # 取り出して並べる
    assert len(set(permutations("11122334", 4))) == 162
    assert len(set(permutations("PEPPER", 4))) == 38
    # 同じものを含む円順列
    def arr(bag): return set(permutations(bag))
    assert circ_classes(arr("WWWWRRB")) == 15
    assert circ_classes(arr("WWWWBBBB")) == 10 and circ_classes(arr("WWWWBBBB"), reflect=True) == 8
    assert circ_classes(arr("WWWWWRRB")) == 21
    assert circ_classes(arr("WWWWWWBBB")) == 10 and circ_classes(arr("WWWWWWBBB"), reflect=True) == 7
    # 対角線を越えない
    def below(W, H):
        return ncount(w for w in walks(W, H) if all(y <= x for x, y in w))
    assert below(6, 6) == 132 == comb(12, 6) - comb(12, 5) and below(7, 4) == 165 == comb(11, 4) - comb(11, 3)
    assert [below(n, n) for n in range(7)] == [1, 1, 2, 5, 14, 42, 132]


VCHECKS.append(v4)


# ---------------------------------------------------------------- 節5
SEC.append({"title": "重複組合せと整数解の個数",
"base": r"""・$n$ 種類のものから重複を許して $r$ 個取る組合せ（重複組合せ）は、○ $r$ 個と仕切り｜$n-1$ 本の並べ方で ${}_{n+r-1}\mathrm{C}_{r}$ 通り（${}_n\mathrm{H}_r$ と書くこともある）<br>
・$x_1+x_2+\cdots+x_n=r$ の 0 以上の整数解は ${}_{n+r-1}\mathrm{C}_{n-1}$ 個、正の整数解は ${}_{r-1}\mathrm{C}_{n-1}$ 個（○ の間の $r-1$ か所から仕切りの位置を選ぶ）<br>
・$x\geqq k$ のような下限は $x=x'+k$ とおきかえる。不等式 $x+y+z\leqq r$ は、残りを $w$ として等式にする<br>
・$a\leqq b\leqq c$ の組は「重複を許して選んで小さい順に並べる」と 1 対 1 に対応する""",
"items": [
 {"lv": 1, "title": "重複組合せの基本",
  "q": r"(1) りんご、みかん、かきの 3 種類の果物を合わせて 6 個買う。どの果物も十分な数があり、買わない種類があってもよいとき、買い方は何通りあるか。<br>"
       r"(2) (1) で、どの種類も少なくとも 1 個は買うとき、買い方は何通りあるか。<br>"
       r"(3) $1\leqq a\leqq b\leqq c\leqq6$ を満たす整数の組 $(a,\ b,\ c)$ は何個あるか。",
  "hint": r"(1) 6 個の果物を ○、種類の区切りを｜で表すと、○ 6 個と｜2 本の並べ方に対応する。(2) 先に 1 個ずつ買っておく。(3) 1〜6 から重複を許して 3 個選べば、小さい順に並べることで $(a,b,c)$ が 1 つ決まる。",
  "sol": r"(1) 例えば ○○｜○｜○○○ を「りんご 2 個、みかん 1 個、かき 3 個」と対応させると、買い方は ○ 6 個と｜2 本の並べ方と 1 対 1 に対応する。<br>"
         r"　${}_8\mathrm{C}_2=\boldsymbol{28}$（通り）<br>"
         r"(2) 先に 3 種類を 1 個ずつ買い、残り 3 個を (1) と同様に選ぶ。　${}_5\mathrm{C}_2=\boldsymbol{10}$（通り）<br>"
         r"(3) 1，2，…，6 の 6 種類の数から重複を許して 3 個選び、小さい順に $a,\ b,\ c$ とすれば、条件を満たす組が 1 つ得られ、逆も成り立つ。よって 6 種類から重複を許して 3 個取る組合せの数で<br>"
         r"　${}_{6+3-1}\mathrm{C}_3={}_8\mathrm{C}_3=\boldsymbol{56}$（個）",
  "note": r"(3) で $1\leqq a<b<c\leqq6$ なら、異なる 3 数を選ぶので ${}_6\mathrm{C}_3=20$ 個。等号の有無で「重複を許すか」が変わる。",
  "ex": r"(1) 4 種類のケーキから合わせて 7 個を選ぶ方法は何通りか（選ばない種類があってもよい）。(2) (1) で、どの種類も少なくとも 1 個は選ぶ方法は何通りか。<br>(3) $0\leqq a\leqq b\leqq c\leqq d\leqq5$ を満たす整数の組 $(a,b,c,d)$ は何個あるか。",
  "exa": r"(1) 120 通り　(2) 20 通り　(3) 126 個"},
 {"lv": 2, "title": "方程式の整数解の個数",
  "q": r"次の個数を求めよ。<br>(1) $x+y+z=10$ を満たす 0 以上の整数の組 $(x,y,z)$　(2) $x+y+z=10$ を満たす正の整数の組 $(x,y,z)$<br>"
       r"(3) $x+y+z=10,\ x\geqq2,\ y\geqq1,\ z\geqq3$ を満たす整数の組 $(x,y,z)$　(4) $(a+b+c)^{10}$ を展開したときの異なる項の個数",
  "hint": r"(1) ○ 10 個と｜2 本の並べ方。(2) $x=x'+1$ などとおきかえて (1) の形にするか、○ 10 個の<b>間の 9 か所から 2 か所</b>を選んで仕切る。(3) 下限の分だけずらす。(4) 項 $a^pb^qc^r$ の指数の組 $(p,q,r)$ を数える。",
  "sol": r"(1) ○ 10 個と｜2 本の並べ方で　${}_{12}\mathrm{C}_2=\boldsymbol{66}$（個）<br>"
         r"(2) $x=x'+1,\ y=y'+1,\ z=z'+1$ とおくと $x'+y'+z'=7$（$x',y',z'\geqq0$）。　${}_9\mathrm{C}_2=\boldsymbol{36}$（個）<br>"
         r"(3) $x=x'+2,\ y=y'+1,\ z=z'+3$ とおくと $x'+y'+z'=4$（$x',y',z'\geqq0$）。　${}_6\mathrm{C}_2=\boldsymbol{15}$（個）<br>"
         r"(4) 展開した項は $a^pb^qc^r$（$p+q+r=10,\ p,q,r\geqq0$）の形で、異なる $(p,q,r)$ は異なる項を与えるから、(1) と同じく　$\boldsymbol{66}$（個）",
  "note": r"(2) は「○ を 10 個並べ、間の 9 か所から 2 か所を選んで仕切る」と考えても ${}_9\mathrm{C}_2$ が得られる（仕切りが隣り合わず、両端にも来ないので各変数が 1 以上になる）。",
  "ex": r"次の個数を求めよ。(1) $x+y+z+w=12$ を満たす 0 以上の整数の組　(2) $x+y+z+w=12$ を満たす正の整数の組<br>(3) $x+y+z+w=12,\ x\geqq1,\ y\geqq1,\ z\geqq2,\ w\geqq2$ を満たす整数の組　(4) $(a+b+c+d)^8$ を展開したときの異なる項の個数",
  "exa": r"(1) 455 個　(2) 165 個　(3) 84 個　(4) 165 個"},
 {"lv": 3, "title": "上限つき・不等式・係数つきの整数解",
  "q": r"次の個数を求めよ。<br>(1) $x+y+z\leqq10$ を満たす 0 以上の整数の組 $(x,y,z)$<br>"
       r"(2) $x+y+z=10,\ 0\leqq x\leqq5,\ 0\leqq y\leqq5,\ 0\leqq z\leqq5$ を満たす整数の組 $(x,y,z)$<br>"
       r"(3) $x+2y+3z=20$ を満たす 0 以上の整数の組 $(x,y,z)$",
  "hint": r"(1) 余り $w=10-(x+y+z)$ を加えて等式にする。(2) 上限は直接扱いにくいので、<b>上限を超えるもの（$x\geqq6$ など）を引く</b>。(3) 係数があると重複組合せは使えない。係数の大きい $z$ を固定して数える。",
  "sol": r"(1) $w=10-(x+y+z)$ とおくと、条件は $x+y+z+w=10$（$x,y,z,w\geqq0$）と同値。　${}_{13}\mathrm{C}_3=\boldsymbol{286}$（個）<br>"
         r"(2) 上限を考えなければ ${}_{12}\mathrm{C}_2=66$ 個。このうち $x\geqq6$ となるものは、$x=x'+6$ とおくと $x'+y+z=4$ で ${}_6\mathrm{C}_2=15$ 個。$y\geqq6$，$z\geqq6$ も同様に 15 個ずつ。2 つ以上が 6 以上になると和が 12 以上となるので、そのような組はない。<br>"
         r"よって　$66-3\times15=\boldsymbol{21}$（個）<br>"
         r"(3) $3z\leqq20$ より $z=0,1,\cdots,6$。$z$ を固定すると $x+2y=20-3z$ で、$y$ は $0\leqq y\leqq\dfrac{20-3z}{2}$ の整数（$x$ は $y$ から決まる）。$y$ の個数は<br>"
         r"$z=0$：11，$z=1$：9，$z=2$：8，$z=3$：6，$z=4$：5，$z=5$：3，$z=6$：2<br>"
         r"よって　$11+9+8+6+5+3+2=\boldsymbol{44}$（個）",
  "note": r"(1) は $x+y+z=k$（$k=0,1,\cdots,10$）の個数 ${}_{k+2}\mathrm{C}_2$ を足して $\displaystyle\sum_{k=0}^{10}{}_{k+2}\mathrm{C}_2=286$ としても求められるが、$w$ を加える方が速い。(2) の上限の処理は包除そのもので、2 つ以上が上限を超える場合があるときは足し戻しが必要になる。",
  "ex": r"次の個数を求めよ。(1) $x+y+z+w\leqq8$ を満たす 0 以上の整数の組　(2) $x+y+z=12,\ 0\leqq x,\ y,\ z\leqq6$ を満たす整数の組<br>(3) $x+2y+4z=16$ を満たす 0 以上の整数の組",
  "exa": r"(1) 495 個　(2) 28 個　(3) 25 個"},
 {"lv": 4, "title": "和の分割（大小の順を指定した整数解）",
  "q": r"(1) $x+y+z=20,\ 1\leqq x\leqq y\leqq z$ を満たす整数の組 $(x,y,z)$ は何個あるか。<br>"
       r"(2) 区別のない 20 個の玉を、区別のない 3 個の箱に入れる方法は何通りあるか。ただし、空の箱があってもよい。",
  "hint": r"大小の順が指定されると重複組合せは使えない。<b>最小の $x$ を固定</b>すると $y$ の範囲が $x\leqq y\leqq\dfrac{20-x}{2}$ と決まる。(2) は箱の中の玉の個数を小さい順に並べると (1) と同じ形になり、0 個の箱を許す分だけ増える。",
  "sol": r"(1) $3x\leqq x+y+z=20$ より $1\leqq x\leqq6$。$x$ を固定すると、$y\leqq z=20-x-y$ より $x\leqq y\leqq\dfrac{20-x}{2}$。<br>"
         r"$x=1$：$1\leqq y\leqq9$ で 9 個　$x=2$：$2\leqq y\leqq9$ で 8 個　$x=3$：$3\leqq y\leqq8$ で 6 個<br>"
         r"$x=4$：$4\leqq y\leqq8$ で 5 個　$x=5$：$5\leqq y\leqq7$ で 3 個　$x=6$：$6\leqq y\leqq7$ で 2 個<br>"
         r"よって　$9+8+6+5+3+2=\boldsymbol{33}$（個）<br>"
         r"(2) 箱に区別がないので、入れ方は 3 個の箱の玉の個数を小さい順に並べた組 $(x,y,z)$（$0\leqq x\leqq y\leqq z,\ x+y+z=20$）と 1 対 1 に対応する。<br>"
         r"$x\geqq1$ のものは (1) より 33 個。$x=0$ のものは $y+z=20,\ 0\leqq y\leqq z$ より $y=0,1,\cdots,10$ の 11 個。<br>"
         r"よって　$33+11=\boldsymbol{44}$（通り）",
  "note": r"(1) の別解：正の整数解は全部で ${}_{19}\mathrm{C}_2=171$ 個。3 数がすべて異なる組 $\{x,y,z\}$ は並べ方が 6 通りずつ、ちょうど 2 数が等しい組は 3 通りずつ現れる（3 数すべて等しい組はない）。2 数が等しい組は $\{a,a,20-2a\}$（$a=1,\cdots,9$）の 9 個なので、すべて異なる組は $(171-27)\div6=24$ 個。よって $24+9=33$ 個。",
  "ex": r"(1) $x+y+z=15,\ 1\leqq x\leqq y\leqq z$ を満たす整数の組は何個あるか。<br>(2) 区別のない 15 個の玉を、区別のない 3 個の箱に入れる方法は何通りあるか（空の箱があってもよい）。",
  "exa": r"(1) 19 個　(2) 27 通り"},
]})


def v5():
    # 重複組合せ
    assert ncount(c for c in product(range(7), repeat=3) if sum(c) == 6) == 28
    assert ncount(c for c in product(range(1, 7), repeat=3) if sum(c) == 6) == 10
    assert ncount(c for c in product(range(1, 7), repeat=3) if c[0] <= c[1] <= c[2]) == 56 == ncount(combinations_with_replacement(range(1, 7), 3))
    assert ncount(c for c in product(range(1, 7), repeat=3) if c[0] < c[1] < c[2]) == 20
    assert ncount(c for c in product(range(8), repeat=4) if sum(c) == 7) == 120
    assert ncount(c for c in product(range(1, 8), repeat=4) if sum(c) == 7) == 20
    assert ncount(c for c in product(range(6), repeat=4) if c[0] <= c[1] <= c[2] <= c[3]) == 126
    # 整数解
    T = [c for c in product(range(11), repeat=3) if sum(c) == 10]
    assert len(T) == 66 and ncount(c for c in T if min(c) >= 1) == 36 and ncount(c for c in T if c[0] >= 2 and c[1] >= 1 and c[2] >= 3) == 15
    from sympy import symbols, expand, Poly
    a, b, c, d = symbols("a b c d")
    assert len(Poly(expand((a + b + c)**10), a, b, c).terms()) == 66
    T = [t for t in product(range(13), repeat=4) if sum(t) == 12]
    assert len(T) == 455 and ncount(t for t in T if min(t) >= 1) == 165
    assert ncount(t for t in T if t[0] >= 1 and t[1] >= 1 and t[2] >= 2 and t[3] >= 2) == 84
    assert len(Poly(expand((a + b + c + d)**8), a, b, c, d).terms()) == 165
    # 上限・不等式・係数
    assert ncount(t for t in product(range(11), repeat=3) if sum(t) <= 10) == 286 == sum(comb(k + 2, 2) for k in range(11))
    assert ncount(t for t in product(range(6), repeat=3) if sum(t) == 10) == 21
    S = [t for t in product(range(21), range(11), range(7)) if t[0] + 2 * t[1] + 3 * t[2] == 20]
    assert len(S) == 44 and [ncount(t for t in S if t[2] == z) for z in range(7)] == [11, 9, 8, 6, 5, 3, 2]
    assert ncount(t for t in product(range(9), repeat=4) if sum(t) <= 8) == 495
    assert ncount(t for t in product(range(7), repeat=3) if sum(t) == 12) == 28
    assert ncount(t for t in product(range(17), range(9), range(5)) if t[0] + 2 * t[1] + 4 * t[2] == 16) == 25
    # 分割
    P = [t for t in product(range(21), repeat=3) if sum(t) == 20 and t[0] <= t[1] <= t[2]]
    assert ncount(t for t in P if t[0] >= 1) == 33 and len(P) == 44
    assert [ncount(t for t in P if t[0] == x) for x in range(1, 7)] == [9, 8, 6, 5, 3, 2]
    assert ncount(t for t in product(range(1, 21), repeat=3) if sum(t) == 20 and len(set(t)) == 3) == 24 * 6
    # 区別のない箱：20 個の玉の 3 箱への入れ方を、箱の並べかえで同一視して数える
    assert len({tuple(sorted(t)) for t in product(range(21), repeat=3) if sum(t) == 20}) == 44
    P = [t for t in product(range(16), repeat=3) if sum(t) == 15 and t[0] <= t[1] <= t[2]]
    assert ncount(t for t in P if t[0] >= 1) == 19 and len(P) == 27


VCHECKS.append(v5)


# ---------------------------------------------------------------- 節6
SEC.append({"title": "図形の個数",
"base": r"""・どの 3 点も一直線上にない $n$ 個の点から 3 点を選ぶと、三角形が ${}_n\mathrm{C}_3$ 個できる。一直線上の 3 点があるときは、その選び方を引く<br>
・凸 $n$ 角形の対角線の本数は ${}_n\mathrm{C}_2-n=\dfrac{n(n-3)}{2}$<br>
・平行線の組でできる平行四辺形は、各組から 2 本ずつ選ぶ方法の数に等しい<br>
・円に内接する三角形は、1 辺が直径 $\iff$ 直角三角形。3 頂点が半円より短い弧の上にある $\iff$ 鈍角三角形""",
"items": [
 {"lv": 1, "title": "正多角形の対角線と三角形",
  "q": r"正十角形について、次のものを求めよ。<br>(1) 対角線の本数　(2) 3 個の頂点を結んでできる三角形の個数　(3) (2) のうち、正十角形と 1 辺だけを共有する三角形の個数<br>(4) (2) のうち、正十角形と辺を共有しない三角形の個数",
  "hint": r"(1) 2 頂点を結ぶ線分から辺を除く。(3) 共有する辺を先に決め、3 つめの頂点がその辺の隣の頂点にならないようにする。(4) は全体から「1 辺だけ共有」と「2 辺を共有」を引く。",
  "sol": r"(1) 10 個の頂点から 2 個を選んで結ぶ線分 ${}_{10}\mathrm{C}_2=45$ 本から、辺 10 本を除いて　$45-10=\boldsymbol{35}$（本）<br>"
         r"(2) ${}_{10}\mathrm{C}_3=\boldsymbol{120}$（個）<br>"
         r"(3) 共有する辺の選び方は 10 通り。3 つめの頂点は、その辺の両端とそれぞれに隣り合う頂点の計 4 個以外の 6 個から選ぶ。　$10\times6=\boldsymbol{60}$（個）<br>"
         r"(4) 2 辺を共有する三角形は、隣り合う 3 頂点を結ぶもので、真ん中の頂点の選び方より 10 個。3 辺を共有する三角形はない。<br>"
         r"よって　$120-60-10=\boldsymbol{50}$（個）",
  "note": r"一般に正 $n$ 角形（$n\geqq6$）で辺を共有しない三角形は ${}_n\mathrm{C}_3-n(n-4)-n=\dfrac{n(n-4)(n-5)}{6}$ 個。$n=10$ で $\dfrac{10\cdot6\cdot5}{6}=50$。",
  "ex": r"正十二角形について、(1) 対角線の本数　(2) 3 頂点を結んでできる三角形の個数　(3) 正十二角形と 1 辺だけを共有する三角形の個数　(4) 辺を共有しない三角形の個数 を求めよ。",
  "exa": r"(1) 54 本　(2) 220 個　(3) 96 個　(4) 112 個"},
 {"lv": 2, "title": "平行線でできる平行四辺形・碁盤目の長方形と正方形",
  "q": r"(1) 平行な 4 本の直線と、それらと交わる平行な 7 本の直線がある。これらの直線で囲まれる平行四辺形は何個あるか。<br>"
       r"(2) 縦 4 マス、横 5 マスの碁盤目（1 マスは正方形）がある。碁盤目の線で囲まれる長方形（正方形を含む）は何個あるか。<br>(3) (2) の長方形のうち、正方形は何個あるか。",
  "hint": r"平行四辺形（長方形）は、<b>向きの異なる 2 組の平行線からそれぞれ 2 本ずつ</b>選ぶと 1 つ決まる。正方形は辺の長さが等しいという条件がつくので、1 辺の長さで分けて数える。",
  "sol": r"(1) 4 本から 2 本、7 本から 2 本を選ぶと、平行四辺形が 1 つ決まる。　${}_4\mathrm{C}_2\times{}_7\mathrm{C}_2=6\times21=\boldsymbol{126}$（個）<br>"
         r"(2) 横の線は 5 本、縦の線は 6 本あるから　${}_5\mathrm{C}_2\times{}_6\mathrm{C}_2=10\times15=\boldsymbol{150}$（個）<br>"
         r"(3) 1 辺が $k$ マス（$k=1,2,3,4$）の正方形は、横に $6-k$ 通り、縦に $5-k$ 通りの位置があるから<br>"
         r"$5\times4+4\times3+3\times2+2\times1=20+12+6+2=\boldsymbol{40}$（個）",
  "note": r"(3) で、斜めに傾いた正方形は碁盤目の線で囲まれていないので数えない。格子点を頂点とする正方形を数える問題では、傾いた正方形も含まれることに注意する。",
  "ex": r"(1) 平行な 6 本の直線と、それらと交わる平行な 6 本の直線で囲まれる平行四辺形は何個あるか。<br>(2) 縦 5 マス、横 6 マスの碁盤目の線で囲まれる長方形は何個あるか。　(3) (2) のうち正方形は何個あるか。",
  "exa": r"(1) 225 個　(2) 315 個　(3) 70 個"},
 {"lv": 3, "title": "格子点を頂点とする三角形の個数",
  "q": r"座標平面上の 16 個の点 $(x,\ y)$（$x,\ y$ はそれぞれ 0，1，2，3 のいずれか）から 3 点を選ぶ。<br>(1) 3 点が一直線上にあるような選び方は何通りか。　(2) 3 点を頂点とする三角形は何個できるか。",
  "hint": r"一直線上の 3 点を、<b>直線の傾きで分類</b>して漏れなく数える。傾きが $0$，$\pm1$，および $y$ 軸に平行なもの以外に 3 点を通る直線があるかを確かめる。",
  "sol": r"(1) 3 点を通る直線の向きで分類する。<br>"
         r"・$x$ 軸に平行：4 点を通る直線が 4 本で、$4\times{}_4\mathrm{C}_3=16$ 通り<br>"
         r"・$y$ 軸に平行：同様に 16 通り<br>"
         r"・傾き 1：4 点を通る直線 $y=x$ が 1 本で 4 通り、3 点を通る直線 $y=x\pm1$ が 2 本で 2 通り。計 6 通り<br>"
         r"・傾き $-1$：同様に 6 通り<br>"
         r"・その他の傾き：$y$ 軸に平行でない直線の傾きを $\dfrac{q}{p}$（$p,\ q$ は互いに素な整数、$p>0$）とすると、この直線上の格子点は $x$ 座標が $p$、$y$ 座標が $q$ ずつ変わるごとに並ぶ。3 点を含むと、両端の点の $x$ 座標の差は $2p$ 以上、$y$ 座標の差は $2|q|$ 以上となり、どちらも 3 以下だから $p=1,\ |q|\leqq1$。よって傾きは $0,\ \pm1$ に限られ、上で数えたもの以外にはない。<br>"
         r"よって　$16+16+6+6=\boldsymbol{44}$（通り）<br>"
         r"(2) 16 個の点から 3 個を選ぶ ${}_{16}\mathrm{C}_3=560$ 通りから、一直線上にある 44 通りを除いて　$560-44=\boldsymbol{516}$（個）",
  "note": r"(1) の「その他の傾き」は、例えば傾き 2 の直線上の格子点は $x$ 座標が 1 増えるごとに $y$ 座標が 2 増えるので、3 点を含むには $y$ 座標の幅が 4 必要になり、この範囲（幅 3）には収まらない、と考えてもよい。点の範囲が広がると傾き $\pm2,\ \pm\dfrac12$ なども現れる。",
  "ex": r"座標平面上の 25 個の点 $(x,\ y)$（$x,\ y$ はそれぞれ 0，1，2，3，4 のいずれか）から 3 点を選んでできる三角形は何個あるか。",
  "exa": r"2148 個（一直線上の 3 点の選び方は 152 通り）"},
 {"lv": 4, "title": "正多角形でできる鋭角・直角・鈍角三角形",
  "q": r"正十二角形の 3 個の頂点を結んでできる三角形のうち、(1) 直角三角形　(2) 鈍角三角形　(3) 鋭角三角形 はそれぞれ何個あるか。",
  "hint": r"正十二角形の外接円を考え、頂点が円周を 12 等分していると見る。三角形の各角の大きさは、その<b>向かい側の弧に対する円周角</b>で決まる。鈍角三角形は 3 頂点が半円より短い弧の上に並ぶので、「最初の頂点」を決めて数える。",
  "sol": r"正十二角形の外接円の円周は、頂点によって 12 等分される（1 区画の中心角は $30^\circ$）。三角形の 3 頂点が円周を $a,\ b,\ c$ 区画（$a+b+c=12$，$a,b,c\geqq1$）の弧に分けるとき、円周角の定理より各角は $15a^\circ,\ 15b^\circ,\ 15c^\circ$ である。<br>"
         r"(1) 直角三角形 $\iff$ $a,\ b,\ c$ のどれかが 6 $\iff$ 1 辺が直径。直径は 6 本あり、残りの頂点は 10 個から選ぶので　$6\times10=\boldsymbol{60}$（個）<br>"
         r"(2) 鈍角三角形 $\iff$ $a,\ b,\ c$ のどれかが 7 以上 $\iff$ 3 頂点が 5 区画以内の弧の上にある。7 以上の弧はただ 1 つなので、その弧の終わりの頂点を「最初の頂点」P とすれば、残りの 2 頂点は P から時計回りに続く 5 個の頂点から選ばれる。逆に、このように選んだ 3 頂点は 7 区画以上の弧を残すので鈍角三角形になる。P の選び方 12 通り、残りの選び方 ${}_5\mathrm{C}_2=10$ 通りで　$12\times10=\boldsymbol{120}$（個）<br>"
         r"(3) 三角形は全部で ${}_{12}\mathrm{C}_3=220$ 個なので　$220-60-120=\boldsymbol{40}$（個）",
  "note": r"鋭角三角形 $\iff$ 外接円の中心が三角形の内部にある。(3) は $a,\ b,\ c$ がすべて 5 以下となる $(a,b,c)$ が 10 組あり、各三角形が「どの頂点から数え始めるか」で 3 回ずつ現れるので $\dfrac{12\times10}{3}=40$ と直接求めることもできる。",
  "ex": r"正十四角形の 3 個の頂点を結んでできる三角形のうち、(1) 直角三角形　(2) 鈍角三角形　(3) 鋭角三角形 はそれぞれ何個あるか。",
  "exa": r"(1) 84 個　(2) 210 個　(3) 70 個"},
 {"lv": 5, "title": "凸多角形の三角形分割",
  "q": r"凸八角形の頂点を順に $\mathrm{P}_1,\ \mathrm{P}_2,\ \cdots,\ \mathrm{P}_8$ とする。八角形の内部で互いに交わらない 5 本の対角線を引いて、八角形を 6 個の三角形に分割する。<br>"
       r"(1) 分割の方法は何通りあるか。<br>(2) 分割してできる三角形のうち、八角形の辺を 1 本も含まないもの（内部の三角形）が少なくとも 1 個ある分割の方法は何通りあるか。",
  "hint": r"(1) 1 本の辺 $\mathrm{P}_1\mathrm{P}_8$ を含む三角形に注目すると、その三角形の左右に<b>より小さい多角形が 2 つ</b>できる。小さい多角形の分割の数を順に求めていく。(2) は余事象。内部の三角形がない分割は、「両側に辺を 2 本含む三角形（耳）」から出発して三角形を 1 個ずつつけ加えると考えると数えられる。",
  "sol": r"(1) 凸 $n$ 角形を交わらない対角線で三角形に分割する方法を $T_n$ 通りとし、$T_2=1$ と定める（線分は分割しないことを 1 通りとみなす）。<br>"
         r"凸 $n$ 角形 $\mathrm{P}_1\mathrm{P}_2\cdots\mathrm{P}_n$ の辺 $\mathrm{P}_1\mathrm{P}_n$ を含む三角形はちょうど 1 つあり、その 3 つめの頂点を $\mathrm{P}_k$（$2\leqq k\leqq n-1$）とする。この三角形の両側は $k$ 角形 $\mathrm{P}_1\cdots\mathrm{P}_k$ と $(n-k+1)$ 角形 $\mathrm{P}_k\cdots\mathrm{P}_n$ で、それぞれを独立に分割すればよい。よって<br>"
         r"$T_n=T_2T_{n-1}+T_3T_{n-2}+\cdots+T_{n-1}T_2$<br>"
         r"$T_3=1$ から順に<br>"
         r"$T_4=1+1=2$，$T_5=2+1+2=5$，$T_6=5+2+2+5=14$，$T_7=14+5+4+5+14=42$，<br>"
         r"$T_8=42+14+10+10+14+42=\boldsymbol{132}$（通り）<br>"
         r"(2) 内部の三角形がない分割を数える。このとき 6 個の三角形はどれも八角形の辺を 1 本または 2 本含む。辺は全部で 8 本だから、2 本含む三角形（耳）を $e$ 個とすると $2e+(6-e)=8$ より $e=2$。<br>"
         r"1 つの耳 $\mathrm{P}_{i-1}\mathrm{P}_i\mathrm{P}_{i+1}$ から始める。それまでに得た三角形を合わせた図形が多角形 $\mathrm{P}_a\mathrm{P}_{a+1}\cdots\mathrm{P}_b$ のとき、対角線 $\mathrm{P}_a\mathrm{P}_b$ の反対側にある三角形は八角形の辺を含むので、3 つめの頂点は $\mathrm{P}_{a-1}$ か $\mathrm{P}_{b+1}$（添字は 8 を法として考える）である。<br>"
         r"耳の次の 2 個目から 5 個目までの三角形でそれぞれ 2 通りずつの選び方があり、6 個目は残る 1 頂点で決まる（これがもう 1 つの耳）。逆にこのように選べば内部の三角形がない分割が得られる。<br>"
         r"出発する耳の頂点 $\mathrm{P}_i$ の選び方は 8 通りで、各分割は 2 つの耳のどちらから出発するかで 2 回ずつ数えられるから、内部の三角形がない分割は　$\dfrac{8\times2^4}{2}=64$ 通り<br>"
         r"よって　$132-64=\boldsymbol{68}$（通り）",
  "note": r"$T_n$ は $1,\ 2,\ 5,\ 14,\ 42,\ 132,\ \cdots$ と、5.4 節の「対角線を越えない最短経路」と同じカタラン数になる。内部の三角形がない分割は、一般の凸 $n$ 角形では $n\cdot2^{n-5}$ 通り（$n\geqq5$）。",
  "ex": r"凸七角形を、内部で交わらない 4 本の対角線で 5 個の三角形に分割する。(1) 分割の方法は何通りか。　(2) 七角形の辺を 1 本も含まない三角形が少なくとも 1 個ある分割の方法は何通りか。",
  "exa": r"(1) 42 通り　(2) 14 通り"},
]})


def triangulations(n):
    """凸 n 角形の三角形分割を、交わらない n-3 本の対角線の組として全列挙し、三角形の組を返す"""
    diags = [(i, j) for i in range(n) for j in range(i + 2, n) if not (i == 0 and j == n - 1)]
    def cross(d, e):
        (a, b), (c, d2) = d, e
        return (a < c < b < d2) or (c < a < d2 < b)
    res = []
    for S in combinations(diags, n - 3):
        if any(cross(S[i], S[j]) for i in range(len(S)) for j in range(i + 1, len(S))):
            continue
        E = set(S) | {(i, i + 1) for i in range(n - 1)} | {(0, n - 1)}
        tris = [t for t in combinations(range(n), 3) if (t[0], t[1]) in E and (t[1], t[2]) in E and (t[0], t[2]) in E]
        assert len(tris) == n - 2
        res.append(tris)
    return res


def v6():
    import math
    def ngon_counts(n):
        side = lambda i, j: (j - i) % n in (1, n - 1)
        T = list(combinations(range(n), 3))
        k = [sum(side(a, b) for a, b in combinations(t, 2)) for t in T]
        return comb(n, 2) - n, len(T), k.count(1), k.count(0), k.count(2)
    assert ngon_counts(10) == (35, 120, 60, 50, 10) and ngon_counts(12)[:4] == (54, 220, 96, 112)
    assert 10 * 6 * 5 // 6 == 50
    # 平行線・碁盤目
    assert comb(4, 2) * comb(7, 2) == 126 and comb(6, 2)**2 == 225
    def rects(h, w):
        R = [(x1, x2, y1, y2) for x1, x2 in combinations(range(w + 1), 2) for y1, y2 in combinations(range(h + 1), 2)]
        return len(R), ncount(r for r in R if r[1] - r[0] == r[3] - r[2])
    assert rects(4, 5) == (150, 40) and rects(5, 6) == (315, 70)
    # 格子点の三角形
    def lattice(m):
        pts = [(x, y) for x in range(m) for y in range(m)]
        col = ncount(t for t in combinations(pts, 3) if (t[1][0] - t[0][0]) * (t[2][1] - t[0][1]) == (t[2][0] - t[0][0]) * (t[1][1] - t[0][1]))
        return col, comb(m * m, 3) - col
    assert lattice(4) == (44, 516) and lattice(5) == (152, 2148)
    # 鋭角・直角・鈍角（座標で内積を計算）
    def kinds(n):
        P = [(math.cos(2 * math.pi * k / n), math.sin(2 * math.pi * k / n)) for k in range(n)]
        r = o = a = 0
        for t in combinations(range(n), 3):
            dots = []
            for i in range(3):
                A, B, C = P[t[i]], P[t[(i + 1) % 3]], P[t[(i + 2) % 3]]
                dots.append((B[0] - A[0]) * (C[0] - A[0]) + (B[1] - A[1]) * (C[1] - A[1]))
            if any(abs(d) < 1e-9 for d in dots): r += 1
            elif any(d < 0 for d in dots): o += 1
            else: a += 1
        return r, o, a
    assert kinds(12) == (60, 120, 40) and kinds(14) == (84, 210, 70)
    assert ncount(t for t in product(range(1, 12), repeat=3) if sum(t) == 12 and max(t) <= 5) == 10
    # 三角形分割
    Tn = {2: 1}
    for n in range(3, 9):
        Tn[n] = 1 if n == 3 else sum(Tn[k] * Tn[n - k + 1] for k in range(2, n))
    assert [Tn[n] for n in range(3, 9)] == [1, 2, 5, 14, 42, 132]
    for n, tot, inner in [(8, 132, 68), (7, 42, 14), (6, 14, 2)]:
        TR = triangulations(n)
        assert len(TR) == tot == Tn[n]
        side = lambda i, j: (j - i) % n in (1, n - 1)
        has_inner = ncount(tr for tr in TR if any(not any(side(a, b) for a, b in combinations(t, 2)) for t in tr))
        assert has_inner == inner and tot - inner == n * 2**(n - 5)
        # 内部の三角形がない分割では耳がちょうど 2 個
        for tr in TR:
            ks = [sum(side(a, b) for a, b in combinations(t, 2)) for t in tr]
            if 0 not in ks:
                assert ks.count(2) == 2


VCHECKS.append(v6)


# ---------------------------------------------------------------- 節7
SEC.append({"title": "完全順列と漸化的な数え上げ",
"base": r"""・完全順列：$1,\ 2,\ \cdots,\ n$ の並べかえで、どの $k$ も $k$ 番目にこないもの。個数を $W_n$ とすると $W_2=1,\ W_3=2,\ W_4=9,\ W_5=44$ で、$W_n=(n-1)(W_{n-1}+W_{n-2})$ が成り立つ<br>
・漸化的な数え上げ：「最初（または最後）の 1 手」で場合を分け、<b>同じ形の小さい場合の数</b>で表して、小さい方から順に計算する<br>
・円形に並んだものは、1 か所で切って直線状にした場合と比べ、両端が「同じ」か「異なる」かで場合を分ける""",
"items": [
 {"lv": 3, "title": "完全順列（プレゼント交換）",
  "q": r"5 人がそれぞれプレゼントを 1 個ずつ持ち寄り、それらを集めてから 5 人に 1 個ずつ配り直す。<br>(1) 全員が自分以外の人のプレゼントを受け取る配り方は何通りか。<br>(2) ちょうど 2 人が自分のプレゼントを受け取る配り方は何通りか。",
  "hint": r"$n$ 人の場合の数を $W_n$ とし、「人 1 が受け取るプレゼントの持ち主 $k$」で場合を分ける。人 $k$ が人 1 のプレゼントを受け取るかどうかで、人数の少ない場合 $W_{n-2}$，$W_{n-1}$ に帰着する。",
  "sol": r"(1) $n$ 人で全員が自分以外のプレゼントを受け取る配り方を $W_n$ 通りとする。$W_1=0,\ W_2=1,\ W_3=2$。<br>"
         r"$n\geqq3$ のとき、人 1 が人 $k$（$k\neq1$）のプレゼントを受け取るとする。$k$ の選び方は $n-1$ 通り。<br>"
         r"・人 $k$ が人 1 のプレゼントを受け取る場合：残り $n-2$ 人の配り方で $W_{n-2}$ 通り。<br>"
         r"・人 $k$ が人 1 のプレゼントを受け取らない場合：人 1 のプレゼントを「人 $k$ が受け取れないもの」、すなわち人 $k$ 自身のものとみなせば、人 1 以外の $n-1$ 人の完全順列と同じで $W_{n-1}$ 通り。<br>"
         r"よって　$W_n=(n-1)(W_{n-1}+W_{n-2})$<br>"
         r"$W_4=3(W_3+W_2)=3\times3=9$，$W_5=4(W_4+W_3)=4\times11=\boldsymbol{44}$（通り）<br>"
         r"(2) 自分のプレゼントを受け取る 2 人の選び方は ${}_5\mathrm{C}_2=10$ 通りで、残り 3 人は全員が自分以外のものを受け取るから $W_3=2$ 通り。<br>"
         r"よって　$10\times2=\boldsymbol{20}$（通り）",
  "note": r"包除による求め方：人 $i$ が自分のものを受け取る配り方の集合を $A_i$ とすると、$k$ 人を指定してその全員が自分のものを受け取る配り方は $(5-k)!$ 通りだから<br>$W_5=5!-{}_5\mathrm{C}_1\,4!+{}_5\mathrm{C}_2\,3!-{}_5\mathrm{C}_3\,2!+{}_5\mathrm{C}_4\,1!-{}_5\mathrm{C}_5\,0!=120-120+60-20+5-1=44$。",
  "ex": r"6 人でプレゼント交換をする。(1) 全員が自分以外の人のプレゼントを受け取る配り方は何通りか。　(2) ちょうど 2 人が自分のプレゼントを受け取る配り方は何通りか。",
  "exa": r"(1) 265 通り　(2) 135 通り"},
 {"lv": 3, "title": "階段の上り方（漸化的な数え上げと組合せ）",
  "q": r"階段を、1 歩で 1 段または 2 段上る。<br>(1) 10 段の階段を上る方法は何通りあるか。<br>(2) 10 段の階段を上る方法のうち、2 段上りが 2 歩以上続かないものは何通りあるか。",
  "hint": r"(1) $n$ 段を上る方法を $a_n$ 通りとし、<b>最初の 1 歩</b>が 1 段か 2 段かで分けると $a_n=a_{n-1}+a_{n-2}$。(2) 2 段上りの歩数 $k$ を固定し、1 段上りの間と両端に 2 段上りを入れる（隣り合わない選び方）。",
  "sol": r"(1) $n$ 段の階段を上る方法を $a_n$ 通りとする。最初の 1 歩が 1 段なら残り $n-1$ 段で $a_{n-1}$ 通り、2 段なら残り $n-2$ 段で $a_{n-2}$ 通りだから<br>"
         r"$a_n=a_{n-1}+a_{n-2}$（$n\geqq3$），$a_1=1,\ a_2=2$<br>"
         r"順に $a_3=3,\ a_4=5,\ a_5=8,\ a_6=13,\ a_7=21,\ a_8=34,\ a_9=55,\ a_{10}=\boldsymbol{89}$（通り）<br>"
         r"(2) 2 段上りを $k$ 歩とすると、1 段上りは $10-2k$ 歩。2 段上りが続かないのは、1 段上り $10-2k$ 歩の間と両端の $11-2k$ か所から $k$ か所を選んで 2 段上りを 1 歩ずつ入れる場合だから ${}_{11-2k}\mathrm{C}_k$ 通り。<br>"
         r"$k=0$：1，$k=1$：${}_9\mathrm{C}_1=9$，$k=2$：${}_7\mathrm{C}_2=21$，$k=3$：${}_5\mathrm{C}_3=10$，$k\geqq4$：$11-2k<k$ なので 0<br>"
         r"よって　$1+9+21+10=\boldsymbol{41}$（通り）",
  "note": r"(1) も 2 段上りの歩数 $k$ で分けると、$k$ 歩の 2 段上りと $10-2k$ 歩の 1 段上りの並べ方 ${}_{10-k}\mathrm{C}_k$ の和として $1+9+28+35+15+1=89$ と求められる。漸化式を使う方法は、条件が「直前の 1 歩」に関するときに特に強い。",
  "ex": r"(1) 1 歩で 1 段、2 段、3 段のいずれかを上るとき、8 段の階段を上る方法は何通りか。<br>(2) 1 歩で 1 段または 2 段上るとき、12 段の階段を上る方法のうち、2 段上りが 2 歩以上続かないものは何通りか。",
  "exa": r"(1) 81 通り　(2) 88 通り"},
 {"lv": 4, "title": "円形に並んだ領域の塗り分け",
  "q": r"円を、中心を通る線分で 6 つの合同な扇形に分け、時計回りに 1 から 6 までの番号をつける。隣り合う扇形が異なる色になるように、異なる 4 色のうち何色かを用いて塗る方法は何通りあるか（番号のついた扇形を区別して数える）。",
  "hint": r"円形のままでは最初と最後がつながっていて数えにくい。扇形 1 と扇形 $n$ の間を<b>切り離して直線状</b>にすると $4\cdot3^{n-1}$ 通り。そのうち扇形 1 と $n$ が同じ色になるものは、2 つを 1 つにまとめた $n-1$ 個の場合に対応する。",
  "sol": r"$n$ 個（$n\geqq3$）の扇形が円形に並ぶとき、条件を満たす塗り方を $a_n$ 通りとする。<br>"
         r"扇形 $1,\ 2,\ \cdots,\ n$ を、扇形 $i$ と $i+1$（$i=1,\cdots,n-1$）だけが異なる色になるように塗る方法は、扇形 1 が 4 通り、以後それぞれ直前と異なる 3 通りで $4\cdot3^{n-1}$ 通り。このうち<br>"
         r"・扇形 $n$ と扇形 1 が異なる色のもの：円形の条件を満たし、$a_n$ 通り<br>"
         r"・扇形 $n$ と扇形 1 が同じ色のもの：扇形 $n$ と 1 を 1 つの扇形にまとめると、$n-1$ 個の扇形の円形の塗り分けと 1 対 1 に対応し、$a_{n-1}$ 通り（$n\geqq4$）<br>"
         r"よって　$a_n+a_{n-1}=4\cdot3^{n-1}$（$n\geqq4$）<br>"
         r"$a_3=4\cdot3\cdot2=24$ から順に<br>"
         r"$a_4=108-24=84$，$a_5=324-84=240$，$a_6=972-240=\boldsymbol{732}$（通り）",
  "note": r"一般に、$k$ 色で $n$ 個の扇形を塗り分ける方法は $(k-1)^n+(-1)^n(k-1)$ 通りとなる（$k=4,\ n=6$ で $3^6+3=732$）。5.2 節の「領域の塗り分け」で B と D が同色か異色かで分けたのは、この方法の $n=4$ の場合にあたる。",
  "ex": r"円を同心円で中央の円と外側の輪に分け、さらに輪を中心を通る線分で 5 つの合同な部分に分ける（計 6 つの領域）。隣り合う領域が異なる色になるように、異なる 5 色のうち何色かを用いて塗る方法は何通りあるか（回転して一致するものも区別する）。",
  "exa": r"1200 通り"},
 {"lv": 5, "title": "夫婦の円卓（男女交互で夫婦は隣り合わない）",
  "q": r"5 組の夫婦 10 人が、円形のテーブルのまわりに等間隔に並んだ 10 個の席に座る。男女が交互に座り、どの夫婦も隣り合わないような座り方は何通りあるか。ただし、回転して一致する座り方は同じとみなす。",
  "hint": r"まず男性 5 人を 1 つおきの席に座らせる（円順列）。次に、男性の間の 5 席に妻たちを座らせるが、各妻には座れない席が 2 つずつある。その<b>禁止された 10 個の「妻と席の組」が円形につながる</b>ことに注目し、包除と、円周上で隣り合わないものを選ぶ数え方（5.3 節）を組み合わせる。",
  "sol": r"男性 5 人の座り方は、円順列で $(5-1)!=24$ 通り。男性の席が決まったとして、時計回りに男性を $\mathrm{M}_1,\ \cdots,\ \mathrm{M}_5$，$\mathrm{M}_i$ の妻を $\mathrm{W}_i$ とし、$\mathrm{M}_i$ と $\mathrm{M}_{i+1}$ の間の席を $\mathrm{S}_i$ とする（$\mathrm{M}_6=\mathrm{M}_1$，$\mathrm{S}_0=\mathrm{S}_5$）。$\mathrm{W}_i$ が座れないのは $\mathrm{S}_{i-1}$ と $\mathrm{S}_i$ である。<br>"
         r"「$\mathrm{W}_i$ が $\mathrm{S}_j$ に座る」という禁止された 10 個の事象を、次の順に円形に並べる。<br>"
         r"$(\mathrm{W}_1,\mathrm{S}_5),\ (\mathrm{W}_1,\mathrm{S}_1),\ (\mathrm{W}_2,\mathrm{S}_1),\ (\mathrm{W}_2,\mathrm{S}_2),\ \cdots,\ (\mathrm{W}_5,\mathrm{S}_4),\ (\mathrm{W}_5,\mathrm{S}_5)$<br>"
         r"（最後の次は最初に戻る）。隣り合う 2 つは同じ妻か同じ席を含むので同時には起こらず、隣り合わない 2 つは妻も席も異なる。<br>"
         r"<b>包除</b>　5 人の妻の座り方 $5!=120$ 通りから、禁止された事象が少なくとも 1 つ起こるものを除く。3 つの集合の場合と同様に、事象を $k$ 個指定してそれらがすべて起こる座り方の数を、$k$ が奇数なら引き、偶数なら足す。指定した $k$ 個が<b>円形の並びで互いに隣り合わないとき</b>、それらは同時に起こり、残り $5-k$ 人の座り方は $(5-k)!$ 通り。隣り合うものを含むときは 0 通り。<br>"
         r"円形に並んだ 10 個から隣り合わない $k$ 個を選ぶ方法の数 $c_k$ は、特定の 1 個を選ぶか選ばないかで分けて（5.3 節）<br>"
         r"$c_k={}_{10-k}\mathrm{C}_k+{}_{9-k}\mathrm{C}_{k-1}$　より　$c_1=10,\ c_2=28+7=35,\ c_3=35+15=50,\ c_4=15+10=25,\ c_5=1+1=2$<br>"
         r"よって、妻の座り方は<br>"
         r"$5!-c_1\cdot4!+c_2\cdot3!-c_3\cdot2!+c_4\cdot1!-c_5\cdot0!=120-240+210-100+25-2=13$（通り）<br>"
         r"したがって　$24\times13=\boldsymbol{312}$（通り）",
  "note": r"$c_5=2$ は、10 個から 1 つおきに選ぶ 2 通り（すべての妻が夫の右隣、またはすべての妻が夫の左隣）にあたる。$n$ 組の場合の妻の座り方の数は $n=3,4,5,6$ で $1,\ 2,\ 13,\ 80$ となり、「メナージュ問題」として知られる。",
  "ex": r"4 組の夫婦 8 人が、円形のテーブルのまわりに等間隔に並んだ 8 個の席に座る。男女が交互に座り、どの夫婦も隣り合わない座り方は何通りあるか（回転して一致するものは同じとみなす）。",
  "exa": r"12 通り"},
 {"lv": 5, "title": "長方形のドミノ敷き詰め（補助の図形を使う）",
  "q": r"縦 3 マス、横 8 マスの長方形のマス目を、1×2 の長方形のタイル 12 枚で、すき間なく重ならないように敷き詰める方法は何通りあるか。ただし、タイルは縦にも横にも置けるものとする。",
  "hint": r"左端の列の埋め方で場合を分けると、長方形でない図形（隅が 1 マス欠けた図形）が現れる。そこで<b>「縦 3 横 $n$ の長方形」と「その左上隅を除いた図形」の 2 種類</b>の敷き詰め方を同時に考え、互いの関係を立てて小さい方から順に計算する。",
  "sol": r"縦 3 マス・横 $n$ マスの長方形を $R_n$，$R_n$ から左上隅の 1 マスを除いた図形を $S_n$ とし、敷き詰め方をそれぞれ $a_n$ 通り、$b_n$ 通りとする（上下を反転すれば、左下隅を除いた図形の敷き詰め方も $b_n$ 通り）。マスの数を考えると $a_n$ は $n$ が偶数、$b_n$ は $n$ が奇数のときだけ考えればよい。<br>"
         r"<b>$R_n$ の場合</b>　左端の列の中央のマスを覆うタイルで分ける。<br>"
         r"・横置き：左端の列の上・下のマスも横置きしかなく、左の 2 列が埋まって残りは $R_{n-2}$。$a_{n-2}$ 通り<br>"
         r"・上のマスと縦置き：左端の列の下のマスは横置きになり、残りは左下隅が欠けた縦 3 横 $n-1$ の図形。$b_{n-1}$ 通り<br>"
         r"・下のマスと縦置き：同様に $b_{n-1}$ 通り<br>"
         r"よって　$a_n=a_{n-2}+2b_{n-1}$<br>"
         r"<b>$S_n$ の場合</b>　左端の列は中央と下の 2 マス。下のマスを覆うタイルで分ける。<br>"
         r"・中央のマスと縦置き：残りは $R_{n-1}$。$a_{n-1}$ 通り<br>"
         r"・横置き：中央のマスも横置きになる。すると 2 列目の上のマスは、左が欠け、下が埋まっているので横置き（2 列目と 3 列目）しかなく、残りは左上隅が欠けた縦 3 横 $n-2$ の図形。$b_{n-2}$ 通り<br>"
         r"よって　$b_n=a_{n-1}+b_{n-2}$<br>"
         r"<b>計算</b>　$b_1=1$（縦置き 1 枚），$a_2=3$（3 枚とも横置き、または縦 2 枚と横 1 枚を上下どちらかに）。<br>"
         r"$b_3=a_2+b_1=4$，$a_4=a_2+2b_3=11$，$b_5=a_4+b_3=15$，$a_6=a_4+2b_5=41$，$b_7=a_6+b_5=56$，<br>"
         r"$a_8=a_6+2b_7=41+112=\boldsymbol{153}$（通り）",
  "note": r"2 種類の量を交互に使うのがこの問題の要点で、$S_n$ を導入しないと場合分けが終わらない。2 つの関係から $b$ を消去すると $a_n=4a_{n-2}-a_{n-4}$ となり、$a_2,\ a_4,\ a_6,\ a_8$ は $3,\ 11,\ 41,\ 153$。",
  "ex": r"縦 3 マス、横 10 マスの長方形のマス目を、1×2 のタイル 15 枚ですき間なく重ならないように敷き詰める方法は何通りあるか。",
  "exa": r"571 通り"},
]})


def domino(h, w):
    """h×w の長方形を 1×2 のタイルで敷き詰める方法を、空いている最初のマスから置いて全探索する"""
    filled = [[False] * w for _ in range(h)]
    def rec():
        for c in range(w):
            for r in range(h):
                if not filled[r][c]:
                    t = 0
                    if r + 1 < h and not filled[r + 1][c]:
                        filled[r][c] = filled[r + 1][c] = True; t += rec(); filled[r][c] = filled[r + 1][c] = False
                    if c + 1 < w and not filled[r][c + 1]:
                        filled[r][c] = filled[r][c + 1] = True; t += rec(); filled[r][c] = filled[r][c + 1] = False
                    return t
        return 1
    return rec()


def v7():
    def der(n): return ncount(p for p in permutations(range(n)) if all(p[i] != i for i in range(n)))
    assert [der(n) for n in range(2, 7)] == [1, 2, 9, 44, 265]
    assert ncount(p for p in permutations(range(5)) if sum(p[i] == i for i in range(5)) == 2) == 20
    assert ncount(p for p in permutations(range(6)) if sum(p[i] == i for i in range(6)) == 2) == 135
    assert sum((-1)**k * comb(5, k) * factorial(5 - k) for k in range(6)) == 44
    # 階段（歩幅の列を全列挙）
    def climbs(n, steps):
        out = []
        def rec(rest, seq):
            if rest == 0: out.append(tuple(seq)); return
            for s in steps:
                if s <= rest: rec(rest - s, seq + [s])
        rec(n, []); return out
    C10 = climbs(10, (1, 2))
    assert len(C10) == 89 and ncount(c for c in C10 if all(not (c[i] == 2 and c[i + 1] == 2) for i in range(len(c) - 1))) == 41
    assert sum(comb(10 - k, k) for k in range(6)) == 89
    assert len(climbs(8, (1, 2, 3))) == 81
    C12 = climbs(12, (1, 2))
    assert ncount(c for c in C12 if all(not (c[i] == 2 and c[i + 1] == 2) for i in range(len(c) - 1))) == 88
    # 扇形の塗り分け
    def ring(n, k): return ncount(c for c in product(range(k), repeat=n) if all(c[i] != c[(i + 1) % n] for i in range(n)))
    assert [ring(n, 4) for n in (3, 4, 5, 6)] == [24, 84, 240, 732]
    assert all(ring(n, k) == (k - 1)**n + (-1)**n * (k - 1) for n in (3, 4, 5, 6) for k in (3, 4, 5))
    ex = ncount(c for c in product(range(5), repeat=6) if all(c[i] != c[(i + 1) % 5] for i in range(5)) and all(c[5] != c[i] for i in range(5)))
    assert ex == 1200
    # 夫婦の円卓：人 0 を席 0 に固定して全列挙（男 0,2,4,..., 夫婦は 2j と 2j+1）
    def menage(n):
        cnt = 0
        for q in permutations(range(1, 2 * n)):
            c = (0,) + q
            if all((c[i] % 2) != (c[(i + 1) % (2 * n)] % 2) and c[i] // 2 != c[(i + 1) % (2 * n)] // 2 for i in range(2 * n)):
                cnt += 1
        return cnt
    assert menage(5) == 312 and menage(4) == 12
    def ck(m, k):
        if k <= 1:
            return comb(m, k)
        return ncount(c for c in combinations(range(m), k) if all((c[(i + 1) % k] - c[i]) % m >= 2 for i in range(k)))
    assert [ck(10, k) for k in range(6)] == [1, 10, 35, 50, 25, 2]
    assert sum((-1)**k * ck(10, k) * factorial(5 - k) for k in range(6)) == 13
    assert sum((-1)**k * ck(8, k) * factorial(4 - k) for k in range(5)) == 2
    def wives(n):   # 男性を固定し、W_i は S_{i-1}, S_i に座れない
        return ncount(p for p in permutations(range(n)) if all(p[i] not in ((i - 1) % n, i) for i in range(n)))
    assert [wives(n) for n in (3, 4, 5, 6)] == [1, 2, 13, 80]
    # ドミノ
    assert [domino(3, n) for n in (2, 4, 6, 8, 10)] == [3, 11, 41, 153, 571]
    a, b = {0: 1}, {1: 1}
    for n in range(2, 11):
        if n % 2 == 0: a[n] = a[n - 2] + 2 * b[n - 1]
        else: b[n] = a[n - 1] + b[n - 2]
    assert [a[n] for n in (2, 4, 6, 8, 10)] == [3, 11, 41, 153, 571] and [b[n] for n in (1, 3, 5, 7)] == [1, 4, 15, 56]
    assert all(a[n] == 4 * a[n - 2] - a[n - 4] for n in (4, 6, 8, 10))


VCHECKS.append(v7)


# ---------------------------------------------------------------- 節8
SEC.append({"title": "分配の問題",
"base": r"""・区別のある $r$ 個を区別のある $n$ 個の箱に入れる：$n^r$ 通り。空の箱をつくらないときは包除で<br>
　$n^r-{}_n\mathrm{C}_1(n-1)^r+{}_n\mathrm{C}_2(n-2)^r-\cdots$<br>
・箱に区別がないときは、空の箱がなければ（区別がある場合）$\div\,n!$<br>
・区別のない玉を区別のある箱へ：重複組合せ。区別のない玉を区別のない箱へ：和の分け方を書き出す<br>
・集合の組を数えるときは、<b>各要素をベン図のどの部分に入れるか</b>（要素の分配）を考える""",
"items": [
 {"lv": 3, "title": "玉と箱（区別の有無による4つの型）",
  "q": r"7 個の玉を 3 個の箱に入れる。どの箱にも少なくとも 1 個の玉を入れるとき、次の場合の入れ方は何通りあるか。<br>"
       r"(1) 玉も箱も区別する　(2) 玉は区別するが、箱は区別しない　(3) 玉は区別しないが、箱は区別する　(4) 玉も箱も区別しない",
  "hint": r"(1) は重複順列 $3^7$ から空の箱があるものを包除で引く。(2) は (1) の箱の区別をなくす（空の箱がないので $3!$ で割れる）。(3) は ○ の間に仕切りを入れる。(4) は 7 を 3 つの正の整数の和に分ける方法を書き出す。",
  "sol": r"(1) 箱を A，B，C とする。各玉の入れ方は 3 通りで、全部で $3^7=2187$ 通り。A が空になる入れ方は $2^7=128$ 通り（B，C が空の場合も同じ）。A と B が空になる入れ方は 1 通り（他の 2 組も同じ）。3 つとも空にはならない。<br>"
         r"空の箱がある入れ方は $3\times128-3\times1=381$ 通りなので　$2187-381=\boldsymbol{1806}$（通り）<br>"
         r"(2) 空の箱がないので 3 つの箱の中身はすべて異なり、(1) の入れ方は箱の名前のつけ方 $3!$ 通りずつが同じ分け方になる。　$1806\div6=\boldsymbol{301}$（通り）<br>"
         r"(3) 7 個の ○ の間の 6 か所から 2 か所を選んで仕切ると、左から A，B，C の個数が決まる。　${}_6\mathrm{C}_2=\boldsymbol{15}$（通り）<br>"
         r"(4) 7 を 3 つの正の整数の和に分ける方法（順序は考えない）は<br>"
         r"$5+1+1,\ 4+2+1,\ 3+3+1,\ 3+2+2$　の　$\boldsymbol{4}$ 通り",
  "note": r"空の箱を許す場合、(2) は $\div3!$ ができない（空の箱が 2 つあると、箱の入れかえで同じものになるのが $3!$ 通りより少ない）。その場合は「空でない箱が 1 個、2 個、3 個」に分けて数える。",
  "ex": r"6 個の玉を 3 個の箱に、どの箱にも少なくとも 1 個入れる。(1) 玉も箱も区別する　(2) 玉は区別し箱は区別しない　(3) 玉は区別せず箱は区別する　(4) 玉も箱も区別しない ときの入れ方は、それぞれ何通りか。",
  "exa": r"(1) 540 通り　(2) 90 通り　(3) 10 通り　(4) 3 通り"},
 {"lv": 4, "title": "2種類のものを分ける（全員が受け取る条件）",
  "q": r"同じ種類のりんご 6 個と、同じ種類のみかん 3 個を、A，B，C の 3 人に分ける。<br>"
       r"(1) 1 個ももらわない人がいてもよいとき、分け方は何通りあるか。<br>(2) どの人も少なくとも 1 個（りんごでもみかんでもよい）はもらうとき、分け方は何通りあるか。",
  "hint": r"(1) りんごとみかんは独立に分けられるので、それぞれの重複組合せの積。(2) 「先に 1 個ずつ配る」は使えない（何を配るかが決まらない）。<b>余事象「1 個ももらわない人がいる」を包除</b>で数える。",
  "sol": r"(1) りんご 6 個の分け方は ${}_8\mathrm{C}_2=28$ 通り、みかん 3 個の分け方は ${}_5\mathrm{C}_2=10$ 通り。　$28\times10=\boldsymbol{280}$（通り）<br>"
         r"(2) A が 1 個ももらわない分け方は、りんごを B，C に分ける 7 通りと、みかんを B，C に分ける 4 通りで $7\times4=28$ 通り。B，C についても同じ。<br>"
         r"A，B がともに 1 個ももらわない分け方は、C が全部もらう 1 通り。他の 2 人の組も同じ。3 人ともにもらわないことはない。<br>"
         r"1 個ももらわない人がいる分け方は $3\times28-3\times1=81$ 通りなので　$280-81=\boldsymbol{199}$（通り）",
  "note": r"「まず 1 個ずつ配ってから残りを分ける」と考えると、配る 1 個がりんごかみかんかで場合が分かれ、しかも同じ分け方を重複して数えてしまう。全員が受け取る条件は、余事象と包除で処理するのが確実である。",
  "ex": r"同じ種類のりんご 5 個と、同じ種類のみかん 4 個を、A，B，C の 3 人に分ける。(1) 1 個ももらわない人がいてもよい分け方は何通りか。　(2) どの人も少なくとも 1 個はもらう分け方は何通りか。",
  "exa": r"(1) 315 通り　(2) 228 通り"},
 {"lv": 4, "title": "要素の分配と部分集合の組",
  "q": r"集合 $U=\{1,\ 2,\ 3,\ 4,\ 5,\ 6\}$ の部分集合 $A,\ B,\ C$ について、次の個数を求めよ。<br>"
       r"(1) $A\subset B$ となる組 $(A,\ B)$　(2) $A\cap B$ がちょうど 1 個の要素からなる組 $(A,\ B)$<br>"
       r"(3) $A\cup B\cup C=U$ かつ $A\cap B\cap C=\varnothing$ となる組 $(A,\ B,\ C)$<br>"
       r"(4) (3) の条件を満たし、さらに $A,\ B,\ C$ がいずれも空集合でない組 $(A,\ B,\ C)$",
  "hint": r"集合の組を直接数えるより、<b>各要素がベン図のどの部分に入るか</b>を決めると考える方が見通しがよい。要素ごとに独立に選べるので重複順列になる。(4) は「空集合のものがある」を包除で引く。",
  "sol": r"(1) 各要素について、「$A$ に属する（このとき $B$ にも属する）」「$B$ だけに属する」「どちらにも属さない」の 3 通りがあり、各要素の選び方で組 $(A,B)$ が 1 つ決まる。　$3^6=\boldsymbol{729}$（個）<br>"
         r"(2) $A\cap B$ に属する要素の選び方が 6 通り。残り 5 個の要素は「$A$ だけ」「$B$ だけ」「どちらにも属さない」の 3 通りずつ。　$6\times3^5=\boldsymbol{1458}$（個）<br>"
         r"(3) 各要素は $A,\ B,\ C$ の少なくとも 1 つに属し、3 つすべてには属さない。属する集合の組は $\{A\},\ \{B\},\ \{C\},\ \{A,B\},\ \{B,C\},\ \{C,A\}$ の 6 通り。　$6^6=\boldsymbol{46656}$（個）<br>"
         r"(4) (3) のうち $A=\varnothing$ となるものは、各要素の行き先が $\{B\},\ \{C\},\ \{B,C\}$ の 3 通りで $3^6=729$ 個。$B=\varnothing$，$C=\varnothing$ も同様。$A=B=\varnothing$ となるものは、すべての要素が $C$ だけに属する 1 個。他の 2 組も同様。3 つとも空集合にはならない。<br>"
         r"空集合のものがある組は $3\times729-3\times1=2184$ 個なので　$46656-2184=\boldsymbol{44472}$（個）",
  "note": r"$A\subset B$ は $A=B$ の場合も含む。(1) を「$B$ を先に選び（要素 $k$ 個なら ${}_6\mathrm{C}_k$ 通り），$A$ をその部分集合から選ぶ（$2^k$ 通り）」と考えると $\displaystyle\sum_{k=0}^{6}{}_6\mathrm{C}_k2^k=(1+2)^6=3^6$ となり、二項定理（数学 II）の考え方とつながる。",
  "ex": r"集合 $U=\{1,2,3,4,5\}$ の部分集合 $A,\ B,\ C$ について、次の個数を求めよ。(1) $A\subset B\subset C$ となる組 $(A,B,C)$　(2) $A\cap B=\varnothing$ となる組 $(A,B)$<br>"
        r"(3) $A\cup B=U$ かつ $A\cap B\neq\varnothing$ となる組 $(A,B)$　(4) $A\cup B\cup C=U$ で、$A,\ B,\ C$ のどの 2 つも共通部分をもたず、どれも空集合でない組 $(A,B,C)$",
  "exa": r"(1) 1024 個　(2) 243 個　(3) 211 個　(4) 150 個"},
]})


def v8():
    # 玉と箱
    for n, ans in [(7, (1806, 301, 15, 4)), (6, (540, 90, 10, 3))]:
        L = [f for f in product(range(3), repeat=n) if len(set(f)) == 3]
        unl = {frozenset(frozenset(i for i in range(n) if f[i] == j) for j in range(3)) for f in L}
        comp = [t for t in product(range(1, n + 1), repeat=3) if sum(t) == n]
        assert (len(L), len(unl), len(comp), len({tuple(sorted(t)) for t in comp})) == ans
    assert 3**7 - (3 * 2**7 - 3) == 1806
    # 2 種類の果物：(りんごの分け方, みかんの分け方) の全列挙
    def fruit(r, m):
        R = [t for t in product(range(r + 1), repeat=3) if sum(t) == r]
        M = [t for t in product(range(m + 1), repeat=3) if sum(t) == m]
        return len(R) * len(M), ncount(1 for x in R for y in M if all(x[i] + y[i] >= 1 for i in range(3)))
    assert fruit(6, 3) == (280, 199) and fruit(5, 4) == (315, 228)
    # 部分集合の組（U の部分集合をビットで表して全列挙）
    n = 6; full = (1 << n) - 1; S = range(1 << n)
    pc = lambda x: bin(x).count("1")
    assert ncount(1 for a in S for b in S if a & b == a) == 729
    assert ncount(1 for a in S for b in S if pc(a & b) == 1) == 1458
    T = [(a, b, c) for a in S for b in S for c in S if a | b | c == full and a & b & c == 0]
    assert len(T) == 46656 and ncount(t for t in T if all(t)) == 44472
    n = 5; full = (1 << n) - 1; S = range(1 << n)
    assert ncount(1 for a in S for b in S for c in S if a & b == a and b & c == b) == 1024
    assert ncount(1 for a in S for b in S if a & b == 0) == 243
    assert ncount(1 for a in S for b in S if a | b == full and a & b) == 211
    assert ncount(1 for a in S for b in S for c in S if a | b | c == full and not (a & b or b & c or c & a) and a and b and c) == 150


VCHECKS.append(v8)

CH = {"no": 5, "sections": SEC}


def verify():
    for f in VCHECKS:
        f()
    items = [it for s in SEC for it in s["items"]]
    lv = [it["lv"] for it in items]
    assert len(SEC) == 8 and 4 <= len(SEC) <= 9
    assert 37 <= len(items) <= 43, len(items)
    assert [lv.count(k) for k in range(1, 6)] == [8, 11, 11, 8, 5] and lv.count(5) >= 3
    for s in SEC:   # 節の中は易しい順
        L = [it["lv"] for it in s["items"]]
        assert L == sorted(L), s["title"]
    for it in items:
        for k in ("q", "hint", "sol", "ex", "exa"):
            assert it[k] and "$$" not in it[k]
