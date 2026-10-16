"""問題集 第6章 確率。CH に問題、verify() で答えを Fraction と全列挙で検算する。"""
from fractions import Fraction as Fr
from itertools import product, combinations, permutations
from math import comb

CH = {6: {
"goal": "「同様に確からしい」根元事象を正しく設定する。余事象・反復試行・条件付き確率・期待値を、問題文の言い回しから素早く選べるようにする。",
"items": [
 {"lv": "A", "q": r"大小2個のさいころを同時に投げる。次の確率を求めよ。<br>(1) 目の和が $8$ である。　(2) 目の積が偶数である。　(3) 少なくとも一方が $6$ の目である。",
  "a": r"(1) $\frac{5}{36}$　(2) $\frac34$　(3) $\frac{11}{36}$",
  "s": r"全事象は $36$ 通り。(1) $(2,6),(3,5),(4,4),(5,3),(6,2)$ の5通り。(2) 余事象「積が奇数」は両方奇数で $9$ 通りなので $1-\frac9{36}=\frac34$。(3) 余事象「どちらも6でない」は $25$ 通りなので $1-\frac{25}{36}=\frac{11}{36}$。<br><b>ポイント</b>：「少なくとも」「積が偶数」は余事象が速い。"},
 {"lv": "A", "q": r"赤玉4個と白玉3個が入った袋から、同時に3個の玉を取り出す。<br>(1) 赤玉2個、白玉1個である確率を求めよ。　(2) 白玉が少なくとも1個含まれる確率を求めよ。",
  "a": r"(1) $\frac{18}{35}$　(2) $\frac{31}{35}$",
  "s": r"全事象は ${}_7\mathrm{C}_3=35$ 通り。(1) ${}_4\mathrm{C}_2\times{}_3\mathrm{C}_1=18$ 通りで $\frac{18}{35}$。(2) 余事象「3個とも赤」は ${}_4\mathrm{C}_3=4$ 通りなので $1-\frac4{35}=\frac{31}{35}$。<br><b>ポイント</b>：同じ色の玉も区別して数えると、各取り出し方が同様に確からしくなる。"},
 {"lv": "A", "q": r"1枚の硬貨を6回投げる。<br>(1) 表がちょうど4回出る確率を求めよ。　(2) 表が4回以上出る確率を求めよ。",
  "a": r"(1) $\frac{15}{64}$　(2) $\frac{11}{32}$",
  "s": r"(1) 反復試行の確率 ${}_6\mathrm{C}_4\left(\frac12\right)^6=\frac{15}{64}$。(2) $\frac{{}_6\mathrm{C}_4+{}_6\mathrm{C}_5+{}_6\mathrm{C}_6}{64}=\frac{15+6+1}{64}=\frac{22}{64}=\frac{11}{32}$。<br><b>ポイント</b>：$n$ 回中 $r$ 回起こる確率は ${}_n\mathrm{C}_rp^r(1-p)^{n-r}$。"},
 {"lv": "A", "q": r"当たりくじ3本を含む10本のくじがある。A, B の2人がこの順に1本ずつ引く。ただし引いたくじはもとに戻さない。<br>(1) B が当たる確率を求めよ。　(2) A, B がともに当たる確率を求めよ。<br>(3) B が当たったとき、A も当たっていた条件付き確率を求めよ。",
  "a": r"(1) $\frac{3}{10}$　(2) $\frac{1}{15}$　(3) $\frac29$",
  "s": r"(1) A が当たって B も当たる $\frac3{10}\cdot\frac29$ と、A がはずれて B が当たる $\frac7{10}\cdot\frac39$ の和で $\frac{6+21}{90}=\frac3{10}$。(2) $\frac3{10}\cdot\frac29=\frac1{15}$。(3) $P_B(A)=\frac{P(A\cap B)}{P(B)}=\frac{1/15}{3/10}=\frac29$。<br><b>ポイント</b>：くじ引きは順番によらず当たる確率は同じ。条件付き確率は「条件の事象を全体とみなす」。"},
 {"lv": "B", "tag": "期待値", "q": r"2個のさいころを同時に投げ、出た目のうち大きい方（同じ目ならその目）を $X$ とする。<br>(1) $X=k\ (k=1,2,\cdots,6)$ となる確率を求めよ。　(2) $X$ の期待値を求めよ。",
  "a": r"(1) $\frac{2k-1}{36}$　(2) $\frac{161}{36}$",
  "s": r"(1) $X\leqq k$ となるのは2個とも $k$ 以下のときで $\frac{k^2}{36}$。$P(X=k)=P(X\leqq k)-P(X\leqq k-1)=\frac{k^2-(k-1)^2}{36}=\frac{2k-1}{36}$。<br>(2) $E(X)=\sum_{k=1}^6k\cdot\frac{2k-1}{36}=\frac{1+6+15+28+45+66}{36}=\frac{161}{36}$。<br><b>ポイント</b>：最大値の確率は「最大値 $\leqq k$」の差で求めるのが定石。"},
 {"lv": "B", "q": r"数直線上の原点に点 P がある。硬貨を投げて表が出れば P を $+1$、裏が出れば $-1$ だけ動かす。硬貨を6回投げたとき、次の確率を求めよ。<br>(1) P が座標 $2$ の点にある。　(2) P が原点にある。<br>(3) P が原点にあり、しかも途中で一度も座標が負にならない。",
  "a": r"(1) $\frac{15}{64}$　(2) $\frac{5}{16}$　(3) $\frac{5}{64}$",
  "s": r"表が $a$ 回なら座標は $a-(6-a)=2a-6$。<br>(1) $2a-6=2$ より $a=4$：${}_6\mathrm{C}_4/64=\frac{15}{64}$。(2) $a=3$：$\frac{20}{64}=\frac5{16}$。<br>(3) 表を $+$、裏を $-$ と書くと、途中の和がつねに $0$ 以上となる並びは<br>$+++---,\ ++-+--,\ ++--+-,\ +-++--,\ +-+-+-$ の5通り。よって $\frac5{64}$。<br><b>ポイント</b>：位置は「表の回数」で決まる。途中経過に条件があるときは、並びを系統的に書き出す。"},
 {"lv": "B", "tag": "原因の確率", "q": r"ある製品は工場 A と工場 B で作られ、全体の $60\%$ が A、$40\%$ が B の製品である。A の製品の $2\%$、B の製品の $5\%$ が不良品である。<br>(1) 製品全体から1個取り出したとき、それが不良品である確率を求めよ。<br>(2) 取り出した1個が不良品であったとき、それが工場 A の製品である確率を求めよ。",
  "a": r"(1) $\frac{4}{125}$（$0.032$）　(2) $\frac38$",
  "s": r"(1) $0.6\times0.02+0.4\times0.05=0.012+0.02=0.032=\frac4{125}$。<br>(2) $P_E(A)=\frac{P(A\cap E)}{P(E)}=\frac{0.012}{0.032}=\frac38$（$E$ は不良品である事象）。<br><b>ポイント</b>：「結果から原因を問う」ときは、樹形図で各経路の確率を出し、該当経路の割合をとる。"},
 {"lv": "B", "q": r"4人が1回だけじゃんけんをする。各人はグー・チョキ・パーを等確率で出すものとする。<br>(1) 1人だけが勝つ確率を求めよ。　(2) ちょうど2人が勝つ確率を求めよ。<br>(3) あいこになる確率を求めよ。",
  "a": r"(1) $\frac4{27}$　(2) $\frac29$　(3) $\frac{13}{27}$",
  "s": r"全事象は $3^4=81$ 通り。勝負がつくのは出た手がちょうど2種類のとき。<br>(1) 勝つ人の選び方 $4$ 通り、勝つ手の選び方 $3$ 通りで $12$ 通り、$\frac{12}{81}=\frac4{27}$。<br>(2) ${}_4\mathrm{C}_2\times3=18$ 通りで $\frac{18}{81}=\frac29$。<br>(3) 勝者が $k$ 人（$k=1,2,3$）の場合は合わせて $({}_4\mathrm{C}_1+{}_4\mathrm{C}_2+{}_4\mathrm{C}_3)\times3=42$ 通り。あいこは $1-\frac{42}{81}=\frac{39}{81}=\frac{13}{27}$。<br><b>ポイント</b>：じゃんけんは「勝つ人の集合」と「勝つ手」を決めれば1通りに決まる。あいこは余事象で。"},
 {"lv": "B", "q": r"1個のさいころを3回投げる。<br>(1) 出た目の最大値が $4$ である確率を求めよ。<br>(2) 出た目の最小値が $2$ で、最大値が $5$ である確率を求めよ。",
  "a": r"(1) $\frac{37}{216}$　(2) $\frac{1}{12}$",
  "s": r"(1) 「最大値 $\leqq4$」から「最大値 $\leqq3$」を除いて $\frac{4^3-3^3}{216}=\frac{37}{216}$。<br>(2) 3回とも $2$ 以上 $5$ 以下（$4^3=64$ 通り）のうち、$2$ を1回も含まないもの（$3^3$ 通り）と $5$ を1回も含まないもの（$3^3$ 通り）を除き、両方とも含まないもの（$2^3$ 通り）を戻す。$64-27-27+8=18$ 通りで $\frac{18}{216}=\frac1{12}$。<br><b>ポイント</b>：最大・最小を同時に指定するときは包除原理。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"1個のさいころを $n$ 回投げるとき（$n\geqq3$）、$1$ の目がちょうど3回出る確率を $p_n$ とする。<br>(1) $\dfrac{p_{n+1}}{p_n}$ を $n$ の式で表せ。<br>(2) $p_n$ を最大にする $n$ をすべて求めよ。",
  "a": r"(1) $\frac{5(n+1)}{6(n-2)}$　(2) $n=17,\ 18$",
  "s": r"(1) $p_n={}_n\mathrm{C}_3\left(\frac16\right)^3\left(\frac56\right)^{n-3}$。${}_{n+1}\mathrm{C}_3\div{}_n\mathrm{C}_3=\frac{(n+1)n(n-1)}{n(n-1)(n-2)}=\frac{n+1}{n-2}$ なので $\frac{p_{n+1}}{p_n}=\frac{n+1}{n-2}\cdot\frac56=\frac{5(n+1)}{6(n-2)}$。<br>(2) $\frac{p_{n+1}}{p_n}>1\iff5(n+1)>6(n-2)\iff n<17$。$n=17$ のとき比は $\frac{90}{90}=1$、$n>17$ では $1$ より小さい。よって $p_3<p_4<\cdots<p_{17}=p_{18}>p_{19}>\cdots$ となり、最大となるのは $n=17,\ 18$。<br><b>ポイント</b>：確率の最大は「隣どうしの比と $1$ の大小」で増減を調べる。比がちょうど $1$ になる $n$ があると、最大を与える $n$ は2つ。"},
 {"lv": "C", "tag": "条件付き確率", "q": r"A, B の2人が試合を繰り返し、先に3勝した方を優勝とする。1試合で A が勝つ確率は $\frac23$、B が勝つ確率は $\frac13$ で、引き分けはない。<br>(1) A が優勝する確率を求めよ。　(2) 優勝が決まるまでの試合数の期待値を求めよ。<br>(3) A が優勝したとき、試合数が5であった条件付き確率を求めよ。",
  "a": r"(1) $\frac{64}{81}$　(2) $\frac{107}{27}$　(3) $\frac14$",
  "s": r"$p=\frac23,\ q=\frac13$ とする。A が第 $k$ 試合で優勝するのは、第 $k-1$ 試合までに A が2勝し、第 $k$ 試合に A が勝つとき。<br>(1) 3試合：$p^3=\frac8{27}$。4試合：${}_3\mathrm{C}_2p^3q=\frac8{27}$。5試合：${}_4\mathrm{C}_2p^3q^2=\frac{16}{81}$。合計 $\frac{24+24+16}{81}=\frac{64}{81}$。<br>(2) どちらかが優勝する確率は、3試合：$p^3+q^3=\frac13$、4試合：$3(p^3q+pq^3)=\frac{10}{27}$、5試合：$6(p^3q^2+p^2q^3)=\frac{8}{27}$（和は $1$）。期待値は $3\cdot\frac{9}{27}+4\cdot\frac{10}{27}+5\cdot\frac8{27}=\frac{107}{27}$。<br>(3) $\frac{16/81}{64/81}=\frac14$。<br><b>ポイント</b>：「最後の試合は優勝者が勝つ」ので、組合せは最後の1試合を除いた部分だけで数える。${}_4\mathrm{C}_3$ などとしてしまうミスに注意。"},
]}}


def verify():
    D = list(product(range(1, 7), repeat=2))
    P = lambda cond, S: Fr(sum(1 for w in S if cond(w)), len(S))
    # A1
    assert P(lambda w: sum(w) == 8, D) == Fr(5, 36)
    assert P(lambda w: w[0]*w[1] % 2 == 0, D) == Fr(3, 4)
    assert P(lambda w: 6 in w, D) == Fr(11, 36)
    # A2
    balls = list(combinations(range(7), 3))  # 0〜3 が赤、4〜6 が白
    col = lambda i: "R" if i < 4 else "W"
    assert P(lambda c: sum(col(i) == "R" for i in c) == 2, balls) == Fr(18, 35)
    assert P(lambda c: any(col(i) == "W" for i in c), balls) == Fr(31, 35)
    # A3
    C6 = list(product([0, 1], repeat=6))
    assert P(lambda w: sum(w) == 4, C6) == Fr(15, 64) and P(lambda w: sum(w) >= 4, C6) == Fr(11, 32)
    # A4
    draws = list(permutations(range(10), 2))  # 0,1,2 が当たり
    hit = lambda i: i < 3
    pB = P(lambda d: hit(d[1]), draws); pAB = P(lambda d: hit(d[0]) and hit(d[1]), draws)
    assert pB == Fr(3, 10) and pAB == Fr(1, 15) and pAB/pB == Fr(2, 9)
    # B1
    for k in range(1, 7):
        assert P(lambda w: max(w) == k, D) == Fr(2*k-1, 36)
    assert sum(Fr(max(w), 36) for w in D) == Fr(161, 36)
    # B2
    def path(w):
        s = 0; m = 0
        for c in w:
            s += 1 if c else -1; m = min(m, s)
        return s, m
    assert P(lambda w: path(w)[0] == 2, C6) == Fr(15, 64)
    assert P(lambda w: path(w)[0] == 0, C6) == Fr(5, 16)
    good = sorted("".join("+" if c else "-" for c in w) for w in C6 if path(w) == (0, 0))
    assert P(lambda w: path(w) == (0, 0), C6) == Fr(5, 64)
    assert set(good) == {"+++---", "++-+--", "++--+-", "+-++--", "+-+-+-"}
    # B3
    pE = Fr(6, 10)*Fr(2, 100)+Fr(4, 10)*Fr(5, 100)
    assert pE == Fr(4, 125) and Fr(6, 10)*Fr(2, 100)/pE == Fr(3, 8)
    # B4
    J = list(product(range(3), repeat=4))  # 0 グー 1 チョキ 2 パー（i は (i+1)%3 に勝つ）
    def winners(w):
        s = set(w)
        if len(s) != 2: return 0
        a, b = s
        win = a if (a+1) % 3 == b else b
        return sum(1 for v in w if v == win)
    assert P(lambda w: winners(w) == 1, J) == Fr(4, 27)
    assert P(lambda w: winners(w) == 2, J) == Fr(2, 9)
    assert P(lambda w: winners(w) == 0, J) == Fr(13, 27)
    # B5
    D3 = list(product(range(1, 7), repeat=3))
    assert P(lambda w: max(w) == 4, D3) == Fr(37, 216)
    assert P(lambda w: min(w) == 2 and max(w) == 5, D3) == Fr(1, 12)
    # C1
    p = lambda n: comb(n, 3)*Fr(1, 6)**3*Fr(5, 6)**(n-3)
    for n in range(3, 40):
        assert p(n+1)/p(n) == Fr(5*(n+1), 6*(n-2))
    vals = {n: p(n) for n in range(3, 80)}
    mx = max(vals.values())
    assert [n for n, v in vals.items() if v == mx] == [17, 18]
    # C2: 5試合分の勝敗を全列挙して、優勝決定までを計算
    pa, pb = Fr(2, 3), Fr(1, 3)
    winA = Fr(0); EX = Fr(0); A5 = Fr(0)
    for w in product([0, 1], repeat=5):  # 1 なら A の勝ち
        pr = Fr(1)
        a = b = 0
        for i, c in enumerate(w):
            pr *= pa if c else pb
            a += c; b += 1-c
            if a == 3 or b == 3:
                break
        # 5試合の列のうち、決着後の試合は重複して数えないよう決着後の試合の確率をかけて合計を保つ
        for c in w[i+1:]:
            pr *= pa if c else pb
        if a == 3:
            winA += pr
            if i == 4: A5 += pr
        EX += (i+1)*pr
    assert winA == Fr(64, 81) and EX == Fr(107, 27) and A5/winA == Fr(1, 4)
    q3 = pa**3+pb**3; q4 = 3*(pa**3*pb+pa*pb**3); q5 = 6*(pa**3*pb**2+pa**2*pb**3)
    assert (q3, q4, q5) == (Fr(1, 3), Fr(10, 27), Fr(8, 27)) and q3+q4+q5 == 1
