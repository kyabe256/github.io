"""問題集 第5章 場合の数。CH に問題、verify() で答えを全列挙・総当たりで検算する。"""
from itertools import permutations, product, combinations
from math import comb, factorial
from sympy import symbols, simplify


def _fig_grid():
    """(0,0)→(5,4) の格子。P(2,1), Q(3,3) に印"""
    u, ox, oy = 28, 22, 128
    X = lambda i: ox + u * i
    Y = lambda j: oy - u * j
    s = ['<svg class="fig" width="200" height="150" viewBox="0 0 200 150">']
    for i in range(6):
        s.append(f'<line x1="{X(i)}" y1="{Y(0)}" x2="{X(i)}" y2="{Y(4)}" stroke="#555"/>')
    for j in range(5):
        s.append(f'<line x1="{X(0)}" y1="{Y(j)}" x2="{X(5)}" y2="{Y(j)}" stroke="#555"/>')
    for (i, j, name, dx, dy) in [(0, 0, "A", -14, 14), (5, 4, "B", 6, -4), (2, 1, "P", 4, -5), (3, 3, "Q", 4, -5)]:
        s.append(f'<circle cx="{X(i)}" cy="{Y(j)}" r="3.2" fill="#1f3f8f"/>')
        s.append(f'<text x="{X(i) + dx}" y="{Y(j) + dy}" font-size="11">{name}</text>')
    s.append('</svg>')
    return "".join(s)


CH = {5: {
"goal": "「区別するか・順序を考えるか・重複を許すか」を判断して、順列・組合せ・重複組合せを使い分ける。数えにくいときは補集合・包除原理・漸化式に切り替える。",
"items": [
 {"lv": "A", "q": r"(1) $1$ から $100$ までの整数のうち、$3$ でも $5$ でも割り切れないものは何個あるか。<br>(2) $360$ の正の約数の個数と、その総和を求めよ。",
  "a": r"(1) $53$ 個　(2) 個数 $24$、総和 $1170$",
  "s": r"(1) 3の倍数 $33$ 個、5の倍数 $20$ 個、15の倍数 $6$ 個。3または5で割り切れるものは $33+20-6=47$ 個なので、$100-47=53$ 個。<br>(2) $360=2^3\cdot3^2\cdot5$。個数は $(3+1)(2+1)(1+1)=24$。総和は $(1+2+4+8)(1+3+9)(1+5)=15\cdot13\cdot6=1170$。<br><b>ポイント</b>：「〜でない」は全体から引く。約数の総和は各素因数の「べきの和」の積を展開した形になっている。"},
 {"lv": "A", "q": r"6個の数字 $0,1,2,3,4,5$ から異なる4個を選んで並べ、4桁の整数をつくる。<br>(1) 4桁の整数は全部で何個できるか。　(2) そのうち偶数は何個あるか。",
  "a": r"(1) $300$ 個　(2) $156$ 個",
  "s": r"(1) 千の位は $0$ 以外の5通り、残り3つの位は残りの5個から並べて ${}_5\mathrm{P}_3=60$ 通り。$5\times60=300$。<br>(2) 一の位が $0$ のとき：残りから3個並べて ${}_5\mathrm{P}_3=60$ 個。一の位が $2$ または $4$ のとき：千の位は $0$ と一の位の数字以外の4通り、百・十の位は残り4個から ${}_4\mathrm{P}_2=12$ 通りで、$2\times4\times12=96$ 個。合計 $156$ 個。<br><b>ポイント</b>：$0$ を含むときは「先頭に $0$ が来ない」条件があるので、制約の強い位から決める。"},
 {"lv": "A", "q": r"A, B を含む6人が円形のテーブルに着席する。<br>(1) 座り方は全部で何通りか。　(2) A と B が隣り合う座り方は何通りか。　(3) A と B が隣り合わない座り方は何通りか。",
  "a": r"(1) $120$ 通り　(2) $48$ 通り　(3) $72$ 通り",
  "s": r"(1) 円順列 $(6-1)!=120$。(2) A と B をひとまとめにして5人の円順列 $4!=24$、まとめた中の並び方 $2$ 通りで $48$。(3) $120-48=72$。<br>（別解）A の位置を固定すると、B は A の両隣以外の3か所、残り4人は $4!$ 通りで $3\times24=72$。<br><b>ポイント</b>：円順列は「1人を固定して残りを並べる」と考えると、条件つきでも数えやすい。"},
 {"lv": "A", "q": r"男子5人、女子4人の中から4人を選ぶ。<br>(1) 男子2人、女子2人を選ぶ方法は何通りか。　(2) 女子が少なくとも1人含まれる選び方は何通りか。",
  "a": r"(1) $60$ 通り　(2) $121$ 通り",
  "s": r"(1) ${}_5\mathrm{C}_2\times{}_4\mathrm{C}_2=10\times6=60$。(2) 全体 ${}_9\mathrm{C}_4=126$ から、男子だけの ${}_5\mathrm{C}_4=5$ を引いて $121$。<br><b>ポイント</b>：「少なくとも1人」は余事象（1人もいない）を引く。"},
 {"lv": "B", "q": r"SUCCESS の7文字を1列に並べる。<br>(1) 並べ方は全部で何通りか。　(2) S が3つ連続する並べ方は何通りか。<br>(3) 2つの C が隣り合わない並べ方は何通りか。",
  "a": r"(1) $420$ 通り　(2) $60$ 通り　(3) $300$ 通り",
  "s": r"S が3個、C が2個、U と E が1個ずつ。<br>(1) $\frac{7!}{3!\,2!}=420$。(2) SSS を1文字とみて、SSS・U・C・C・E の並べ方 $\frac{5!}{2!}=60$。(3) CC が隣り合う並べ方は CC を1文字とみて $\frac{6!}{3!}=120$ なので、$420-120=300$。<br>（別解）S, S, S, U, E を先に並べて $\frac{5!}{3!}=20$ 通り。その間と両端の6か所から2か所を選んで C を入れて ${}_6\mathrm{C}_2=15$ 通り。$20\times15=300$。<br><b>ポイント</b>：「隣り合う」はまとめて1つ、「隣り合わない」は余事象か「間に入れる」。"},
 {"lv": "B", "tag": "頻出", "q": r"下の図のような碁盤の目状の道がある。A から B まで、右または上に進む最短経路を考える。" + _fig_grid() + r"(1) 最短経路は全部で何通りか。　(2) P を通る最短経路は何通りか。<br>(3) P を通り、Q を通らない最短経路は何通りか。",
  "a": r"(1) $126$ 通り　(2) $60$ 通り　(3) $33$ 通り",
  "s": r"右を $\to$、上を $\uparrow$ とすると、A から B は $\to5$ 個と $\uparrow4$ 個の並べ方。<br>(1) $\frac{9!}{5!\,4!}=126$。<br>(2) A→P は $\to2,\uparrow1$ で $3$ 通り、P→B は $\to3,\uparrow3$ で $20$ 通り。$3\times20=60$。<br>(3) P と Q の両方を通る経路は、A→P $3$ 通り、P→Q（$\to1,\uparrow2$）$3$ 通り、Q→B（$\to2,\uparrow1$）$3$ 通りで $27$ 通り。$60-27=33$。<br><b>ポイント</b>：通過点で経路を区切って積をとる。「通らない」は「通る」を引く。"},
 {"lv": "B", "q": r"$x+y+z=10$ を満たす次の整数の組 $(x,y,z)$ の個数を求めよ。<br>(1) $x,\ y,\ z$ は $0$ 以上の整数　(2) $x,\ y,\ z$ は正の整数　(3) $x,\ y,\ z$ は $x<y<z$ を満たす正の整数",
  "a": r"(1) $66$ 個　(2) $36$ 個　(3) $4$ 個",
  "s": r"(1) 10個の○と2本の｜の並べ方に対応させて ${}_{12}\mathrm{C}_2=66$。<br>(2) $x=x'+1$ などとおくと $x'+y'+z'=7\ (x',y',z'\geqq0)$ となり ${}_9\mathrm{C}_2=36$。（10個の○の間9か所から仕切り2か所を選ぶと考えてもよい。）<br>(3) $x<y<z$ より $3x+3<x+y+z=10$、$x\leqq2$。$x=1$：$y+z=9,\ 2\leqq y<z$ より $(y,z)=(2,7),(3,6),(4,5)$。$x=2$：$y+z=8,\ 3\leqq y<z$ より $(3,5)$。計 $4$ 個。<br><b>ポイント</b>：大小関係つきは、最小の文字の範囲を先に絞ってから書き出す。"},
 {"lv": "B", "tag": "組分け", "q": r"9人を次のように分ける方法は何通りか。<br>(1) 3つの部屋 A, B, C に3人ずつ入れる。　(2) 3人ずつの3つの組に分ける。<br>(3) 2人、2人、5人の3つの組に分ける。",
  "a": r"(1) $1680$ 通り　(2) $280$ 通り　(3) $378$ 通り",
  "s": r"(1) ${}_9\mathrm{C}_3\times{}_6\mathrm{C}_3\times{}_3\mathrm{C}_3=84\times20\times1=1680$。<br>(2) (1) で部屋の区別をなくす。3組の並べ方 $3!$ 通りが同じ分け方になるので $\frac{1680}{6}=280$。<br>(3) 5人の組を選び ${}_9\mathrm{C}_5=126$、残り4人を2人ずつに分けると ${}_4\mathrm{C}_2\div2!=3$。$126\times3=378$。<br><b>ポイント</b>：人数が同じ組が $k$ 個あれば $k!$ で割る。人数が違う組は区別がつくので割らない。"},
 {"lv": "B", "q": r"男子 A を含む男子4人と、女子 B を含む女子4人が円形に並ぶ。<br>(1) 男女が交互に並ぶ並び方は何通りか。<br>(2) 男女が交互に並び、さらに A と B が隣り合う並び方は何通りか。",
  "a": r"(1) $144$ 通り　(2) $72$ 通り",
  "s": r"(1) 男子4人の円順列 $3!=6$ 通り。男子の間の4か所に女子4人を並べて $4!=24$ 通り。$6\times24=144$。<br>(2) 男子の円順列 $6$ 通りのそれぞれで、A の両隣の2か所のどちらかに B を入れて $2$ 通り、残りの女子3人を3か所に並べて $3!=6$ 通り。$6\times2\times6=72$。<br><b>ポイント</b>：交互に並べるときは、先に一方を円順列で並べ、他方はできた「すき間」に並べる（すき間は区別がつくので普通の順列）。"},
 {"lv": "C", "tag": "包除原理", "q": r"$n$ を $3$ 以上の整数とする。$n$ 人を部屋に入れる。ただし、どの部屋にも少なくとも1人は入るものとする。<br>(1) 3つの部屋 A, B, C に入れる方法の数を $n$ で表せ。<br>(2) $n=6$ のとき、6人を区別のない3つの組に分ける方法は何通りか。<br>(3) 6人を4つの部屋 A, B, C, D に入れる方法は何通りか。",
  "a": r"(1) $3^n-3\cdot2^n+3$　(2) $90$ 通り　(3) $1560$ 通り",
  "s": r"(1) 空室を許すと $3^n$ 通り。このうち A が空の入れ方は $2^n$ 通り（B, C も同様）、A と B がともに空の入れ方は $1$ 通り（他の2部屋の組も同様）、3部屋とも空になることはない。包除原理より、少なくとも1部屋が空の入れ方は $3\cdot2^n-3\cdot1$ 通り。よって $3^n-3\cdot2^n+3$。<br>(2) $n=6$ で $729-192+3=540$ 通り。部屋の区別をなくすと、空の組がないので3組の名前の付け方 $3!$ 通りがすべて異なる部屋割りに対応する。$540\div6=90$。<br>(3) 包除原理で $4^6-{}_4\mathrm{C}_1\,3^6+{}_4\mathrm{C}_2\,2^6-{}_4\mathrm{C}_3\,1^6=4096-2916+384-4=1560$。<br><b>ポイント</b>：「どの部屋も空でない」は「少なくとも1つ空」の余事象。$k$ 部屋が空の場合を ${}_m\mathrm{C}_k$ 倍して符号を交互に足し引きする。"},
 {"lv": "C", "tag": "漸化式", "q": r"$n$ 人がそれぞれプレゼントを1つずつ持ち寄って交換し、全員が1つずつ受け取る。全員が自分以外の人のプレゼントを受け取る受け取り方の数を $W(n)$ とする（$W(1)=0,\ W(2)=1$）。<br>(1) $W(3),\ W(4)$ を求めよ。<br>(2) $n\geqq3$ のとき $W(n)=(n-1)\{W(n-1)+W(n-2)\}$ が成り立つことを示せ。<br>(3) 5人のとき、全員が他人のプレゼントを受け取る受け取り方の数と、ちょうど2人だけが自分のプレゼントを受け取る受け取り方の数を求めよ。",
  "a": r"(1) $W(3)=2,\ W(4)=9$　(2) 略　(3) $44$ 通り、$20$ 通り",
  "s": r"(1) 3人 1,2,3 では、1 が 2 のものを受け取ると 2→3, 3→1 と決まり、1 が 3 のものなら 3→2, 2→1 と決まるので $W(3)=2$。4人では、1 が 2 のものを受け取るとき、2, 3, 4 が受け取るものは順に $(1,4,3),\ (3,4,1),\ (4,1,3)$ の3通り。1 が 3, 4 のものを受け取る場合も同様に3通りずつなので $W(4)=9$。<br>(2) 人 1 が人 $k$ のプレゼントを受け取るとする（$k$ の選び方 $n-1$ 通り）。<br>・人 $k$ が人 1 のプレゼントを受け取る場合：残り $n-2$ 人が互いに他人のものを受け取るので $W(n-2)$ 通り。<br>・人 $k$ が人 1 のプレゼントを受け取らない場合：人 1 のプレゼントを「人 $k$ が受け取ってはいけないもの」とみなすと、人 1 以外の $n-1$ 人がそれぞれ受け取ってはいけないもの以外を受け取る方法になり $W(n-1)$ 通り。<br>よって $W(n)=(n-1)\{W(n-1)+W(n-2)\}$。■<br>(3) $W(5)=4(9+2)=44$。ちょうど2人が自分のものを受け取る：その2人の選び方 ${}_5\mathrm{C}_2=10$、残り3人が全員他人のものを受け取る $W(3)=2$ で $20$ 通り。<br><b>ポイント</b>：直接数えにくいものは「最初の1人の行き先」で場合分けして漸化式を立てる。"},
]}}


def verify():
    # A1
    assert sum(1 for n in range(1, 101) if n % 3 and n % 5) == 53
    dv = [d for d in range(1, 361) if 360 % d == 0]
    assert len(dv) == 24 and sum(dv) == 1170
    # A2
    nums = [p for p in permutations(range(6), 4) if p[0] != 0]
    assert len(nums) == 300 and sum(1 for p in nums if p[3] % 2 == 0) == 156
    # A3: A を席0に固定して残り5人を並べる
    seats = list(permutations("BCDEF"))
    assert len(seats) == 120
    adj = sum(1 for s in seats if s.index("B") in (0, 4))
    assert adj == 48 and 120-adj == 72
    # A4
    boys, girls = range(5), range(5, 9)
    ch = list(combinations(range(9), 4))
    assert sum(1 for c in ch if sum(1 for v in c if v in girls) == 2) == 60
    assert sum(1 for c in ch if any(v in girls for v in c)) == 121
    # B1
    words = set(permutations("SUCCESS"))
    assert len(words) == 420
    assert sum(1 for w in words if "SSS" in "".join(w)) == 60
    assert sum(1 for w in words if "CC" not in "".join(w)) == 300
    # B2: 経路を全列挙
    paths = set(permutations("RRRRRUUUU"))
    def visits(p):
        x = y = 0; pts = {(0, 0)}
        for c in p:
            if c == "R": x += 1
            else: y += 1
            pts.add((x, y))
        return pts
    allp = [visits(p) for p in paths]
    assert len(allp) == 126
    assert sum(1 for v in allp if (2, 1) in v) == 60
    assert sum(1 for v in allp if (2, 1) in v and (3, 3) not in v) == 33
    # B3
    assert sum(1 for x, y in product(range(11), repeat=2) if x+y <= 10) == 66
    assert sum(1 for x, y in product(range(1, 11), repeat=2) if x+y <= 9) == 36
    assert sum(1 for x, y in product(range(1, 11), repeat=2) if 10-x-y > y > x) == 4
    # B4
    groups = set(); groups3 = set()
    rooms = 0
    for A in combinations(range(9), 3):
        rest = [v for v in range(9) if v not in A]
        for B in combinations(rest, 3):
            rooms += 1
            C = tuple(v for v in rest if v not in B)
            groups.add(frozenset([frozenset(A), frozenset(B), frozenset(C)]))
    assert rooms == 1680 and len(groups) == 280
    for F in combinations(range(9), 5):
        rest = [v for v in range(9) if v not in F]
        for T in combinations(rest, 2):
            U = tuple(v for v in rest if v not in T)
            groups3.add(frozenset([frozenset(F), frozenset(T), frozenset(U)]))
    assert len(groups3) == 378
    # B5: 男子 A を席0に固定し、残り7人を並べる（男子 1,2,3 女子 B=4,5,6,7）
    alt = alt_adj = 0
    for p in permutations(range(1, 8)):
        s = (0,) + p
        if all((s[i] < 4) != (s[(i+1) % 8] < 4) for i in range(8)):
            alt += 1
            if s[1] == 4 or s[7] == 4:
                alt_adj += 1
    assert alt == 144 and alt_adj == 72
    # C1
    def onto(n, m):
        return sum(1 for f in product(range(m), repeat=n) if len(set(f)) == m)
    for n in range(3, 8):
        assert onto(n, 3) == 3**n-3*2**n+3
    assert onto(6, 3) == 540 and onto(6, 3)//6 == 90
    # 区別のない3組を直接数える（集合の分割）
    parts = set()
    for f in product(range(3), repeat=6):
        if len(set(f)) == 3:
            parts.add(frozenset(frozenset(i for i in range(6) if f[i] == k) for k in range(3)))
    assert len(parts) == 90
    assert onto(6, 4) == 1560 == 4**6-4*3**6+6*2**6-4
    # C2
    def W(n): return sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n)))
    assert W(3) == 2 and W(4) == 9 and W(5) == 44
    # 1 が 2 のものを受け取るとき、(2,3,4) の受け取るもの
    assert [p for p in permutations([1, 3, 4]) if p[1] != 3 and p[2] != 4] == [(1, 4, 3), (3, 4, 1), (4, 1, 3)]
    for n in range(3, 8):
        assert W(n) == (n-1)*(W(n-1)+W(n-2))
    assert sum(1 for p in permutations(range(5)) if sum(p[i] == i for i in range(5)) == 2) == 20 == comb(5, 2)*W(3)
