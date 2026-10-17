"""問題集 第14章 有機化合物の構造決定。CH に問題、verify() で分子式・分子量を計算し、
候補の構造をすべて分子グラフで列挙して、問題の条件をすべて満たすものが1つに決まることを確認する。"""

from itertools import combinations_with_replacement

# ---- 検算用の小道具（このファイルだけで完結させる） ----
import re
from collections import Counter
from itertools import permutations, combinations


def sf(x, n=2):
    """有効数字 n 桁に丸める"""
    return float(f"{x:.{n}g}")


def fml(s):
    """化学式 → 元素ごとの原子数（( ) [ ] と水和水 . に対応）"""
    s = s.replace("[", "(").replace("]", ")")
    total = Counter()
    for p in s.split("."):
        m = re.match(r"^(\d*)(.*)$", p)
        k, p = int(m.group(1) or 1), m.group(2)
        st, i = [Counter()], 0
        while i < len(p):
            if p[i] == "(":
                st.append(Counter()); i += 1
            elif p[i] == ")":
                d = re.match(r"\d*", p[i + 1:]).group(0); i += 1 + len(d)
                top = st.pop()
                for e, c in top.items():
                    st[-1][e] += c * int(d or 1)
            else:
                g = re.match(r"([A-Z][a-z]?)(\d*)", p[i:]); assert g, p
                st[-1][g.group(1)] += int(g.group(2) or 1); i += len(g.group(0))
        for e, c in st[0].items():
            total[e] += c * k
    return total


def eq(s):
    """'2H2 + O2 -> 2H2O' の原子数と電荷のつり合いを確かめる（イオンは Fe{3+}、電子は e{-}）"""
    def side(t):
        tot, chg = Counter(), 0
        for term in t.split(" + "):
            m = re.match(r"^\s*(\d*)\s*([^{}\s]+)(\{(\d*)([+-])\})?\s*$", term)
            k, f = int(m.group(1) or 1), m.group(2)
            if m.group(3):
                chg += k * int(m.group(4) or 1) * (1 if m.group(5) == "+" else -1)
            if f != "e":
                for e, c in fml(f).items():
                    tot[e] += k * c
        return +tot, chg
    l, r = s.split("->")
    assert side(l) == side(r), s


def mw(f, A):
    return sum(A[e] * c for e, c in fml(f).items())


def du(f):
    """不飽和度"""
    c = fml(f)
    return (2 * c["C"] + 2 + c["N"] - c["H"] - c["Cl"] - c["Br"]) // 2


def chk(ch):
    """形式の点検：A4・B4〜5・C2、空欄なし、$ の対応、$ の中に % や $$ がない、論述の字数"""
    for no, v in ch.items():
        lv = Counter(it["lv"] for it in v["items"])
        assert lv["A"] == 4 and lv["B"] in (4, 5) and lv["C"] == 2 and len(v["items"]) == sum(lv.values()), (no, lv)
        assert v["goal"]
        for it in v["items"]:
            for k in ("lv", "tag", "q", "a", "s"):
                assert it.get(k), (no, k, it["q"][:30])
                t = it[k]
                assert t.count("$") % 2 == 0 and "$$" not in t, (no, k, t[:40])
                assert not any("%" in x for x in t.split("$")[1::2]), (no, k, t[:40])
            assert "<b>ポイント</b>" in it["s"], it["q"][:30]
            for body, n, lim in re.findall(r"解答例：(.*?)（(\d+)字／(\d+)字以内）", it["a"] + it["s"]):
                assert len(body) == int(n) <= int(lim), (len(body), n, lim, body)


def strut(ch, st=r"\rule[-0.85em]{0pt}{2.4em}"):
    """\\dfrac を含む行が上下の行の分数とぶつからないよう、見えない支柱を入れる"""
    for v in ch.values():
        for it in v["items"]:
            for k in ("q", "a", "s"):
                it[k] = it[k].replace(r"\dfrac", st + r"\dfrac")
    return ch
# ---- 分子グラフ（H は省略。結合次数は2倍で持つ：単結合2、二重4、三重6、ベンゼン環3） ----
VAL = {"C": 4, "O": 2, "N": 3, "S": 2, "Cl": 1, "Br": 1}
HET = {"O", "N", "S", "Cl", "Br"}


class Mol:
    def __init__(self, atoms, bonds):
        self.a, self.b = list(atoms), dict(bonds)

    def adj(self):
        ad = [[] for _ in self.a]
        for (i, j), o in self.b.items():
            ad[i].append((j, o)); ad[j].append((i, o))
        return ad

    def free(self, i):
        return 2 * VAL[self.a[i]] - sum(o for (p, q), o in self.b.items() if i in (p, q))

    def h(self, i):
        return self.free(i) // 2

    def nH(self):
        return sum(self.h(i) for i in range(len(self.a)))


def canon(m, extra=None):
    """色の細分化＋個別化による正準形（同じ構造なら同じ値）"""
    n, ad = len(m.a), m.adj()
    init = [(m.a[i], m.h(i), tuple(sorted(o for _, o in ad[i])), extra[i] if extra else 0) for i in range(n)]
    ks = sorted(set(init)); col0 = [ks.index(x) for x in init]

    def refine(col):
        while True:
            sig = [(col[i], tuple(sorted((o, col[j]) for j, o in ad[i]))) for i in range(n)]
            k2 = sorted(set(sig)); new = [k2.index(s) for s in sig]
            if len(k2) == len(set(col)):
                return new
            col = new
    best = [None]

    def search(col):
        col = refine(col)
        if len(set(col)) == n:
            s = tuple(sorted((min(col[i], col[j]), max(col[i], col[j]), o) for (i, j), o in m.b.items()))
            if best[0] is None or s < best[0]:
                best[0] = s
            return
        cnt = Counter(col); c = min(k for k, v in cnt.items() if v > 1)
        for i in range(n):
            if col[i] == c:
                new = [2 * x for x in col]; new[i] = 2 * c - 1
                search(new)
    search(col0)
    return (tuple(sorted(init)), best[0])


def benzene():
    return Mol(["C"] * 6, {**{(i, i + 1): 3 for i in range(5)}, (0, 5): 3})


def grow(start, target):
    """start の分子に target の原子がそろうまで1個ずつ単結合でつなぐ（ヘテロ原子どうしは結合させない）"""
    cur = {canon(m): m for m in start}
    for _ in range(sum(target.values()) - len(start[0].a)):
        nxt = {}
        for m in cur.values():
            rem = target - Counter(m.a)
            for el in rem:
                for i in range(len(m.a)):
                    if m.free(i) >= 2 and not (el in HET and m.a[i] in HET):
                        m2 = Mol(m.a + [el], {**m.b, (i, len(m.a)): 2})
                        nxt.setdefault(canon(m2), m2)
        cur = nxt
    return list(cur.values())


def unsat(ms, k, kinds):
    """不飽和を k 個加える。kinds: CC（C=C, C≡C）, CO（C=O）, ring（環）"""
    cur = {canon(m): m for m in ms}
    for _ in range(k):
        nxt = {}
        for m in cur.values():
            n = len(m.a)
            for i in range(n):
                if m.free(i) < 2:
                    continue
                for j in range(i + 1, n):
                    if m.free(j) < 2:
                        continue
                    o, pr = m.b.get((i, j)), {m.a[i], m.a[j]}
                    if o is None:
                        if "ring" not in kinds or (m.a[i] in HET and m.a[j] in HET):
                            continue
                        nb = {**m.b, (i, j): 2}
                    elif pr == {"C"} and "CC" in kinds and o in (2, 4):
                        nb = {**m.b, (i, j): o + 2}
                    elif pr == {"C", "O"} and "CO" in kinds and o == 2:
                        nb = {**m.b, (i, j): 4}
                    else:
                        continue
                    m2 = Mol(m.a, nb); nxt.setdefault(canon(m2), m2)
        cur = nxt
    return list(cur.values())


def isomers(f, kinds=("CC", "CO", "ring"), arom=False):
    """分子式 f の構造異性体（arom=True ならベンゼン環を1つもつもの）"""
    c = fml(f); H = c.pop("H", 0)
    ms = grow([benzene()] if arom else [Mol(["C"], {})], Counter(c))
    ms = unsat(ms, du(f) - (4 if arom else 0), kinds)
    return [m for m in ms if m.nH() == H]


def smi(s):
    """簡易 SMILES（C c O N S Cl Br, = #, 枝, 環番号）→ Mol"""
    atoms, bonds, stack, prev, bo, ring, i = [], {}, [], None, 2, {}, 0
    while i < len(s):
        ch = s[i]
        if ch == "(":
            stack.append(prev); i += 1; continue
        if ch == ")":
            prev = stack.pop(); i += 1; continue
        if ch in "=#":
            bo = 4 if ch == "=" else 6; i += 1; continue
        if ch.isdigit():
            if ch in ring:
                j, bj = ring.pop(ch); o = bo if bo != 2 else bj
                if atoms[j] == atoms[prev] == "c" and o == 2:
                    o = 3
                bonds[tuple(sorted((j, prev)))] = o
            else:
                ring[ch] = (prev, bo)
            bo = 2; i += 1; continue
        el = s[i:i + 2] if s[i:i + 2] in ("Cl", "Br") else ch
        i += len(el); atoms.append(el); k = len(atoms) - 1
        if prev is not None:
            bonds[(prev, k)] = 3 if (atoms[prev] == el == "c" and bo == 2) else bo
        prev, bo = k, 2
    return Mol(["C" if x == "c" else x for x in atoms], bonds)


def C(s):
    return canon(smi(s))


def sub(m, idx):
    idx = sorted(idx); mp = {o: n for n, o in enumerate(idx)}
    return Mol([m.a[i] for i in idx], {(mp[i], mp[j]): o for (i, j), o in m.b.items() if i in mp and j in mp}), mp


def reach(m, s, ban=(), banb=None):
    ad, seen, st = m.adj(), {s}, [s]
    while st:
        x = st.pop()
        for y, _ in ad[x]:
            if y in ban or y in seen or (banb and {x, y} == set(banb)):
                continue
            seen.add(y); st.append(y)
    return seen


def comps(m):
    left, out = set(range(len(m.a))), []
    while left:
        r = reach(m, min(left)); left -= r; out.append(sub(m, r)[0])
    return out


def branch(m, c, j):
    sm, mp = sub(m, reach(m, j, ban={c}))
    return canon(sm, [1 if i == mp[j] else 0 for i in range(len(sm.a))])


def asym(m):
    """不斉炭素原子の数"""
    ad, n = m.adj(), 0
    for i, el in enumerate(m.a):
        if el != "C" or any(o != 2 for _, o in ad[i]) or m.h(i) > 1:
            continue
        subs = [branch(m, i, j) for j, _ in ad[i]] + ["H"] * m.h(i)
        n += len(set(subs)) == 4
    return n


def cistrans(m):
    """シス-トランス異性を生じる（環に含まれない）C=C の数"""
    ad, n = m.adj(), 0
    for (i, j), o in m.b.items():
        if o != 4 or m.a[i] != "C" or m.a[j] != "C" or j in reach(m, i, banb=(i, j)):
            continue
        ok = True
        for x, y in ((i, j), (j, i)):
            oth = [k for k, _ in ad[x] if k != y]
            if m.h(x) == 2 or (m.h(x) == 0 and branch(m, x, oth[0]) == branch(m, x, oth[1])):
                ok = False
        n += ok
    return n


def nstereo(ms):
    """構造異性体のリスト → 立体異性体を区別した数（ここで扱う分子は立体要素が高々1つ）"""
    t = 0
    for m in ms:
        k = asym(m) + cistrans(m); assert k <= 1
        t += 2 ** k
    return t


def carbonyl(m, c):
    return any(m.a[k] == "O" and o == 4 for k, o in m.adj()[c])


def groups(m):
    """官能基の数え上げ"""
    ad, g = m.adj(), Counter()
    for i, el in enumerate(m.a):
        if el == "C" and carbonyl(m, i):
            sO = [j for j, o in ad[i] if m.a[j] == "O" and o == 2]
            if sO:
                g["COOH" if m.h(sO[0]) == 1 else "ester"] += 1
            else:
                g["CHO" if m.h(i) >= 1 else "ketone"] += 1
        if el == "O" and all(o == 2 for _, o in ad[i]):
            cs = [j for j, _ in ad[i]]
            if m.h(i) == 1:
                c = cs[0]
                if carbonyl(m, c):
                    continue
                if any(o == 3 for _, o in ad[c]):
                    g["phenol"] += 1
                elif any(o != 2 for _, o in ad[c]):
                    g["enol"] += 1
                elif sum(m.a[k] == "O" for k, _ in ad[c]) > 1:
                    g["unstable"] += 1
                else:
                    g["alc%d" % sum(m.a[k] == "C" for k, _ in ad[c])] += 1
            elif len(cs) == 2 and not any(carbonyl(m, c) for c in cs):
                g["ether"] += 1
    for (i, j), o in m.b.items():
        if m.a[i] == m.a[j] == "C" and o in (4, 6):
            g["C=C" if o == 4 else "C#C"] += 1
    return g


def alcohol(g):
    return sum(v for k, v in g.items() if k.startswith("alc"))


def tollens(m):
    """銀鏡反応（ホルミル基 -CHO。ギ酸・ギ酸エステルを含む）"""
    return any(m.a[i] == "C" and carbonyl(m, i) and m.h(i) >= 1 for i in range(len(m.a)))


def iodoform(m):
    """CH3CO-R, CH3CH(OH)-R（R は H か炭素）"""
    ad = m.adj()
    for i, el in enumerate(m.a):
        if el != "C" or m.h(i) != 3 or len(ad[i]) != 1 or m.a[ad[i][0][0]] != "C":
            continue
        x = ad[i][0][0]
        nb = [(k, o) for k, o in ad[x] if k != i]
        dO = [k for k, o in nb if m.a[k] == "O" and o == 4]
        sO = [k for k, o in nb if m.a[k] == "O" and o == 2]
        rest = [k for k, o in nb if m.a[k] != "O"]
        if not all(m.a[k] == "C" for k in rest):
            continue
        if dO and not sO:
            return True
        if not dO and len(sO) == 1 and m.h(sO[0]) == 1 and m.h(x) >= 1 and all(o == 2 for _, o in ad[x]):
            return True
    return False


def hydrolyze(m):
    """エステルを加水分解 → [酸, アルコール（またはフェノール）]"""
    ad = m.adj()
    for i in range(len(m.a)):
        if m.a[i] == "C" and carbonyl(m, i):
            for j, o in ad[i]:
                if m.a[j] == "O" and o == 2 and m.h(j) == 0:
                    b = {k: v for k, v in m.b.items() if set(k) != {i, j}}
                    n = len(m.a); b[(i, n)] = 2
                    m2 = Mol(m.a + ["O"], b)
                    acid = sub(m2, reach(m2, i))[0]; alc = sub(m2, reach(m2, j))[0]
                    return acid, alc
    return None


def dehydrate(m):
    """アルコールの分子内脱水で生じるアルケン（構造異性体のリスト）"""
    ad, out = m.adj(), {}
    for o in range(len(m.a)):
        if m.a[o] == "O" and m.h(o) == 1:
            a = ad[o][0][0]
            for bta, bo in ad[a]:
                if m.a[bta] == "C" and bo == 2 and m.h(bta) >= 1:
                    b = {k: v for k, v in m.b.items() if o not in k}
                    b[tuple(sorted((a, bta)))] = 4
                    m2 = sub(Mol(m.a, b), [k for k in range(len(m.a)) if k != o])[0]
                    out.setdefault(canon(m2), m2)
    return list(out.values())


def add_atom(m, i, el="Cl"):
    return Mol(m.a + [el], {**m.b, (i, len(m.a)): 2})


def nsubst(m, ring=False, el="Cl"):
    """H 1個を el で置換した化合物の数（ring=True ならベンゼン環の H だけ）"""
    ad, s = m.adj(), set()
    for i in range(len(m.a)):
        if m.a[i] == "C" and m.h(i) >= 1 and (not ring or any(o == 3 for _, o in ad[i])):
            s.add(canon(add_atom(m, i, el)))
    return len(s)


def hydrogenate(m):
    return Mol(m.a, {k: (2 if (o in (4, 6) and m.a[k[0]] == m.a[k[1]] == "C") else o) for k, o in m.b.items()})


def ozonolysis(m, mols=False):
    """C=C を切って両側を C=O にする → 生成物の正準形のリスト（mols=True なら分子のリスト）"""
    for (i, j), o in m.b.items():
        if o == 4 and m.a[i] == m.a[j] == "C":
            b = {k: v for k, v in m.b.items() if k != (i, j)}
            n = len(m.a); b[(i, n)] = 4; b[(j, n + 1)] = 4
            ps = comps(Mol(m.a + ["O", "O"], b))
            return ps if mols else sorted(canon(x) for x in ps)
    return None


def ring_subs(m):
    """ベンゼン環（原子0〜5）の各位置に結合した原子の元素（なければ None）"""
    ad, r = m.adj(), []
    for p in range(6):
        oth = [k for k, o in ad[p] if k >= 6]
        r.append(m.a[oth[0]] if oth else None)
    return r

CH = {14: {
"goal": "元素分析 → 分子式 → 不飽和度 → 官能基 → 骨格 の順に情報を整理する。候補を漏れなく数え上げてから、反応の結果で1つずつ消していく解き方を身につける。",
"items": [
 {"lv": "A", "tag": "組成式・分子式",
  "q": r"炭素・水素・酸素からなる化合物の成分元素の質量百分率は、C 58.8 %、H 9.8 %、O 31.4 % であった。この化合物の分子量は 100 から 110 の間にある。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$ とする。<br>(1) 組成式を求めよ。<br>(2) 分子式を求めよ。<br>(3) 不飽和度（分子中の二重結合と環の数の和）を求めよ。",
  "a": r"(1) $\mathrm{C_5H_{10}O_2}$　(2) $\mathrm{C_5H_{10}O_2}$　(3) 1",
  "s": r"(1) 100 g あたりの物質量の比は $\mathrm{C:H:O}=\dfrac{58.8}{12}:\dfrac{9.8}{1.0}:\dfrac{31.4}{16}=4.90:9.8:1.96=2.5:5:1=5:10:2$。<br>(2) 組成式量は 102 で、100〜110 の範囲にあるので分子式も $\mathrm{C_5H_{10}O_2}$。<br>(3) 不飽和度 $=\dfrac{2\times5+2-10}{2}=1$（O の数は関係しない）。C=O を1つもつエステルやカルボン酸などが候補になる。<br><b>ポイント</b>：比が 2.5 のように半端なときは、全体を2倍して整数にする。不飽和度は $\dfrac{2n_\mathrm{C}+2+n_\mathrm{N}-n_\mathrm{H}-n_\mathrm{X}}{2}$（X はハロゲン）。"},
 {"lv": "A", "tag": "異性体",
  "q": r"分子式 $\mathrm{C_3H_6Cl_2}$ で表される化合物について、(1) 構造異性体をすべて示性式で示し、(2) そのうち不斉炭素原子をもつものを選べ。",
  "a": r"(1) $\mathrm{CHCl_2CH_2CH_3}$、$\mathrm{CH_2ClCHClCH_3}$、$\mathrm{CH_2ClCH_2CH_2Cl}$、$\mathrm{CH_3CCl_2CH_3}$　(2) $\mathrm{CH_2ClC^*HClCH_3}$（1,2-ジクロロプロパン）",
  "s": r"(1) Cl 2個を、炭素骨格 C1–C2–C3 の同じ炭素に置く場合（C1 か C2：2通り）と、異なる炭素に置く場合（C1 と C2、C1 と C3：2通り）で、計4種類。<br>(2) 1,2-ジクロロプロパンの C2 には H、Cl、$\mathrm{CH_3}$、$\mathrm{CH_2Cl}$ の4つの異なる原子・原子団が結合している。<br><b>ポイント</b>：二置換体は「同じ炭素に2つ」と「別々の炭素に1つずつ」に分けて数えると漏れがない。"},
 {"lv": "A", "tag": "不飽和度",
  "q": r"(1) 次の分子式の化合物の不飽和度を求めよ。<br>　(ア) $\mathrm{C_6H_6}$　(イ) $\mathrm{C_4H_6}$　(ウ) $\mathrm{C_3H_5Cl}$　(エ) $\mathrm{C_8H_8O_2}$　(オ) $\mathrm{C_5H_{11}N}$　(カ) $\mathrm{C_6H_{12}O_6}$<br>(2) 分子式 $\mathrm{C_4H_6}$ で表される鎖式化合物の構造異性体をすべて示性式で示せ。",
  "a": r"(1) (ア) 4　(イ) 2　(ウ) 1　(エ) 5　(オ) 1　(カ) 1　(2) $\mathrm{CH{\equiv}CCH_2CH_3}$、$\mathrm{CH_3C{\equiv}CCH_3}$、$\mathrm{CH_2{=}CHCH{=}CH_2}$、$\mathrm{CH_2{=}C{=}CHCH_3}$",
  "s": r"(1) (ア) ベンゼン環（環1＋二重結合3）で4。(ウ) Cl は H と同じに数える。(エ) ベンゼン環4＋C=O 1。(オ) N は1個につき H を1個減らして数える（$\frac{10+2+1-11}{2}=1$）。(カ) グルコースの鎖状構造では C=O が1つ（環状構造では環が1つ）。<br>(2) 不飽和度2の鎖式化合物は、三重結合1つ（1-ブチン、2-ブチン）か二重結合2つ（1,3-ブタジエン、1,2-ブタジエン）。<br><b>ポイント</b>：不飽和度 4 以上で C が 6 以上なら、まずベンゼン環を疑う。"},
 {"lv": "A", "tag": "反応と部分構造",
  "q": r"化合物について次の (1)〜(6) の結果が得られたとき、推定できる部分構造を下のア〜カから1つずつ選べ。<br>(1) アンモニア性硝酸銀水溶液と加熱すると、銀が析出する。<br>(2) ヨウ素と水酸化ナトリウム水溶液と温めると、黄色沈殿が生じる。<br>(3) 塩化鉄(III) 水溶液を加えると、紫色を呈する。<br>(4) 炭酸水素ナトリウム水溶液を加えると、気体が発生する。<br>(5) 臭素水を加えると、臭素の赤褐色が消える。<br>(6) ナトリウムを加えると気体が発生するが、(3) と (4) の反応は示さない。<br>ア ホルミル基　イ $\mathrm{CH_3CO-}$ または $\mathrm{CH_3CH(OH)-}$　ウ フェノール性ヒドロキシ基　エ カルボキシ基　オ 炭素原子間の二重結合または三重結合　カ アルコール性ヒドロキシ基",
  "a": r"(1) ア　(2) イ　(3) ウ　(4) エ　(5) オ　(6) カ",
  "s": r"(1) 銀鏡反応（ギ酸やギ酸エステルも示す）。(2) ヨードホルム反応で $\mathrm{CHI_3}$ の黄色沈殿。(4) 炭酸より強い酸。(5) 付加反応。(6) $\mathrm{-OH}$ をもつがフェノール性でもカルボキシ基でもないので、アルコール。<br><b>ポイント</b>：構造決定の問題文に出てくる反応は限られている。「反応 → 部分構造」の対応を即答できるようにしておく。"},
 {"lv": "B", "tag": "構造決定（エステル）",
  "q": r"分子式 $\mathrm{C_5H_{10}O_2}$ で表されるエステルについて答えよ。<br>(1) エステルの構造異性体は何種類あるか。<br>(2) エステル A を加水分解すると、カルボン酸 B とアルコール C が得られた。B は銀鏡反応を示さなかった。C はヨードホルム反応を示し、C を酸化するとケトンが得られた。A、B、C の示性式を答えよ。<br>(3) (1) のエステルのうち、加水分解で得られるカルボン酸が銀鏡反応を示すものは何種類か。<br>(4) (1) のエステルのうち、分子内に不斉炭素原子をもつものの示性式を答えよ。",
  "a": r"(1) 9種類　(2) A $\mathrm{CH_3COOCH(CH_3)_2}$　B $\mathrm{CH_3COOH}$　C $\mathrm{CH_3CH(OH)CH_3}$　(3) 4種類　(4) $\mathrm{HCOOC^*H(CH_3)CH_2CH_3}$",
  "s": r"(1) $\mathrm{R{-}COO{-}R'}$ の炭素数の組で分ける。$\mathrm{HCOO{-}C_4H_9}$：4種類（ブチル基が4種類）、$\mathrm{CH_3COO{-}C_3H_7}$：2種類、$\mathrm{C_2H_5COO{-}C_2H_5}$：1種類、$\mathrm{C_3H_7COO{-}CH_3}$：2種類で、計9種類。<br>(2) C はヨードホルム反応を示す（$\mathrm{CH_3CH(OH)-}$ をもつ）第二級アルコール。エステルの候補になるアルコールはエタノール・2-プロパノール・2-ブタノールだが、エタノールは酸化するとアルデヒドになる。2-ブタノールのエステルはギ酸エステルで、B（ギ酸）が銀鏡反応を示してしまう。よって C は 2-プロパノール、B は酢酸。<br>(3) ギ酸エステル（ブチル基4種類）。<br>(4) ギ酸 2-ブチル（sec-ブチル）の C2 が不斉炭素原子。<br><b>ポイント</b>：エステルの構造決定は「加水分解生成物の酸とアルコールを別々に決めて、つなぐ」。ギ酸エステルは銀鏡反応を示すことに注意。"},
 {"lv": "B", "tag": "構造決定（オゾン分解）",
  "q": r"アルケンをオゾンで分解した後に適切な処理をすると、二重結合が切れて $\mathrm{R^1R^2C{=}CR^3R^4 \to R^1R^2C{=}O + O{=}CR^3R^4}$（R は炭化水素基または H）のようにカルボニル化合物が得られる。分子式 $\mathrm{C_6H_{12}}$ の鎖式アルケン X をこの方法で分解したところ、1種類の化合物 Y だけが得られた。Y は銀鏡反応を示さず、ヨードホルム反応を示した。<br>(1) 分子式 $\mathrm{C_6H_{12}}$ の鎖式アルケンのうち、この分解で1種類の化合物だけを与えるものを、シス-トランス異性体を区別せずにすべて示性式で示せ。<br>(2) X と Y の示性式を答えよ。<br>(3) (1) のうち X でないものには、シス-トランス異性体がある。それを分解して得られる化合物の名称と、銀鏡反応およびヨードホルム反応の結果を答えよ。<br>(4) X に臭素を付加させた化合物は不斉炭素原子をもつか。",
  "a": r"(1) $\mathrm{CH_3CH_2CH{=}CHCH_2CH_3}$、$\mathrm{(CH_3)_2C{=}C(CH_3)_2}$　(2) X $\mathrm{(CH_3)_2C{=}C(CH_3)_2}$、Y $\mathrm{CH_3COCH_3}$　(3) プロパナール（プロピオンアルデヒド）。銀鏡反応を示し、ヨードホルム反応は示さない。(4) もたない",
  "s": r"(1) 1種類だけが得られるのは、二重結合の両側が同じ原子団になっている場合。C 6個を3個ずつに分けると、片側は $\mathrm{CH_3CH_2CH{=}}$ か $\mathrm{(CH_3)_2C{=}}$ の2通りなので、3-ヘキセンと 2,3-ジメチル-2-ブテンの2種類。<br>(2) Y が銀鏡反応を示さない（アルデヒドでない）ので、Y はケトンのアセトン。<br>(3) 3-ヘキセン → $\mathrm{CH_3CH_2CHO}$ 2分子。$\mathrm{CH_3CO-}$ をもたないのでヨードホルム反応は示さない。<br>(4) $\mathrm{(CH_3)_2CBr{-}CBr(CH_3)_2}$ の C は $\mathrm{CH_3}$ を2個もつので不斉炭素原子ではない。<br><b>ポイント</b>：オゾン分解の生成物を「C=O の側からつなぎ直す」と、もとのアルケンの二重結合の位置がわかる。"},
 {"lv": "B", "tag": "構造決定（芳香族エステル）",
  "q": r"分子式 $\mathrm{C_8H_8O_2}$ で表され、ベンゼン環をもつエステルについて答えよ。<br>(1) このようなエステルは何種類あるか。すべて示性式で示せ。<br>(2) エステル A を加水分解すると、化合物 B と C が得られた。B は塩化鉄(III) 水溶液で呈色し、C は銀鏡反応を示した。また、B のベンゼン環の水素原子1個を臭素原子で置換した化合物は2種類あった。A、B、C の名称を答えよ。<br>(3) (1) のエステルのうち、加水分解によってフェノール類が生じるものは何種類か。",
  "a": r"(1) 6種類：$\mathrm{C_6H_5COOCH_3}$、$\mathrm{CH_3COOC_6H_5}$、$\mathrm{HCOOCH_2C_6H_5}$、$\mathrm{HCOOC_6H_4CH_3}$（$o$・$m$・$p$）　(2) A ギ酸 $p$-メチルフェニル（$p$-クレゾールのギ酸エステル）、B $p$-クレゾール、C ギ酸　(3) 4種類",
  "s": r"(1) ベンゼン環（不飽和度4）とエステル（C=O で1）で不飽和度5。ベンゼン環に置換基1つ：安息香酸メチル、酢酸フェニル、ギ酸ベンジルの3種類。置換基2つ（$\mathrm{HCOO-}$ と $\mathrm{-CH_3}$）：$o$・$m$・$p$ の3種類。計6種類。<br>(2) C は銀鏡反応を示すカルボン酸なのでギ酸。B は $\mathrm{CH_3C_6H_4OH}$（クレゾール）で、環の H の種類が2種類なのはパラ体（OH の隣の2つと、$\mathrm{CH_3}$ の隣の2つ）。$o$-・$m$-クレゾールでは4種類。<br>(3) 酢酸フェニルと、ギ酸メチルフェニル3種類。<br><b>ポイント</b>：芳香族エステルは「ベンゼン環が酸側にあるか、アルコール（フェノール）側にあるか」で場合分けする。"},
 {"lv": "B", "tag": "分子量の測定と構造",
  "q": r"炭素・水素・酸素からなる液体 X の成分元素の質量百分率は、C 40.0 %、H 6.7 % であった。X 0.30 g を 127 ℃、$1.0\times10^5$ Pa ですべて気体にすると、体積は 166 mL であった。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、気体定数 $R=8.3\times10^3\ \mathrm{Pa\cdot L/(K\cdot mol)}$ とする。<br>(1) X の分子量を求めよ。<br>(2) X の分子式を求めよ。<br>(3) X は炭酸水素ナトリウム水溶液とも、ナトリウムとも反応しなかったが、銀鏡反応を示した。X の示性式と名称を答えよ。<br>(4) X の構造異性体のうち、炭酸水素ナトリウム水溶液と反応するものの名称を答えよ。",
  "a": r"(1) 60　(2) $\mathrm{C_2H_4O_2}$　(3) $\mathrm{HCOOCH_3}$、ギ酸メチル　(4) 酢酸",
  "s": r"(1) $M=\dfrac{wRT}{PV}=\dfrac{0.30\times8.3\times10^3\times400}{1.0\times10^5\times0.166}=60$。<br>(2) O は 53.3 %。$\mathrm{C:H:O}=\dfrac{40.0}{12}:\dfrac{6.7}{1.0}:\dfrac{53.3}{16}=3.33:6.7:3.33=1:2:1$ で組成式 $\mathrm{CH_2O}$（30）。分子量 60 より $\mathrm{C_2H_4O_2}$。<br>(3) 安定な候補は、酢酸 $\mathrm{CH_3COOH}$、ギ酸メチル $\mathrm{HCOOCH_3}$、ヒドロキシアセトアルデヒド $\mathrm{HOCH_2CHO}$ の3つ。$\mathrm{NaHCO_3}$ と反応しないので酢酸ではなく、Na と反応しない（$\mathrm{-OH}$ がない）ので $\mathrm{HOCH_2CHO}$ でもない。ギ酸メチルは $\mathrm{HCO-}$ の部分で銀鏡反応を示す。<br><b>ポイント</b>：分子量は気体の状態方程式（蒸気密度）や凝固点降下から求める。組成式と組み合わせて分子式を決める。"},
 {"lv": "B", "tag": "アルケンの反応",
  "q": r"分子式 $\mathrm{C_5H_{10}}$ で表される鎖式アルケンについて答えよ。<br>(1) シス-トランス異性体を区別すると、何種類あるか。<br>(2) 水素を付加させると 2-メチルブタンになるものの示性式をすべて答えよ。<br>(3) 臭素を付加させると、1分子中に不斉炭素原子を2個もつ化合物が生じるものの名称を答えよ。<br>(4) 14-6 と同じオゾン分解を行うとアセトンが得られるものの示性式を答えよ。また、そのとき同時に得られる化合物の名称を答えよ。",
  "a": r"(1) 6種類　(2) $\mathrm{CH_2{=}C(CH_3)CH_2CH_3}$、$\mathrm{(CH_3)_2C{=}CHCH_3}$、$\mathrm{CH_2{=}CHCH(CH_3)_2}$　(3) 2-ペンテン（シス形・トランス形とも）　(4) $\mathrm{(CH_3)_2C{=}CHCH_3}$、アセトアルデヒド",
  "s": r"(1) 直鎖：1-ペンテン、2-ペンテン（シス・トランス）。枝分かれ：2-メチル-1-ブテン、2-メチル-2-ブテン、3-メチル-1-ブテン。計6種類。<br>(2) 枝分かれのある3種類。<br>(3) 2-ペンテン → $\mathrm{CH_3C^*HBrC^*HBrCH_2CH_3}$（2個）。1-ペンテン → $\mathrm{CH_2BrC^*HBrCH_2CH_2CH_3}$（1個）、2-メチル-1-ブテン → $\mathrm{CH_2BrC^*Br(CH_3)CH_2CH_3}$（1個）、2-メチル-2-ブテン → $\mathrm{(CH_3)_2CBrC^*HBrCH_3}$（1個）、3-メチル-1-ブテン → $\mathrm{CH_2BrC^*HBrCH(CH_3)_2}$（1個）。<br>(4) 二重結合の一方の炭素に $\mathrm{CH_3}$ が2個結合している必要がある：$\mathrm{(CH_3)_2C{=}CHCH_3 \to CH_3COCH_3 + CH_3CHO}$。<br><b>ポイント</b>：付加生成物の不斉炭素原子は、もとの二重結合の炭素に注目して判定する。"},
 {"lv": "C", "tag": "総合（芳香族エステル）",
  "q": r"炭素・水素・酸素からなる芳香族化合物 A 16.4 mg を完全燃焼させると、二酸化炭素 44.0 mg と水 10.8 mg が生じた。A の分子量は 164 である。A を水酸化ナトリウム水溶液とともに加熱して加水分解した後、反応液を酸性にすると、芳香族化合物 B と化合物 C が得られた。<br>・B は炭酸水素ナトリウム水溶液と反応して気体を発生したが、塩化鉄(III) 水溶液では呈色しなかった。<br>・B を過マンガン酸カリウムで十分に酸化すると化合物 D（$\mathrm{C_8H_6O_4}$）が得られた。D はエチレングリコールとの縮合重合で、合成繊維の原料となる。<br>・C はヨードホルム反応を示した。また、C を二クロム酸カリウムの硫酸酸性溶液で穏やかに酸化すると、銀鏡反応を示す化合物が得られた。<br>$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$ とする。<br>(1) A の分子式を求めよ。<br>(2) B、C、D の名称を答えよ。<br>(3) A の示性式と名称を答えよ。<br>(4) A 1.64 g を完全に加水分解するのに必要な 1.00 $\mathrm{mol/L}$ 水酸化ナトリウム水溶液の体積は何 mL か。<br>(5) B の構造異性体のうち、ベンゼン環をもつカルボン酸は B を含めて何種類あるか。",
  "a": r"(1) $\mathrm{C_{10}H_{12}O_2}$　(2) B $p$-トルイル酸（4-メチル安息香酸）、C エタノール、D テレフタル酸　(3) $p$-$\mathrm{CH_3C_6H_4COOC_2H_5}$、$p$-トルイル酸エチル　(4) 10.0 mL　(5) 4種類",
  "s": r"(1) C：$44.0\times\frac{12}{44}=12.0\ \mathrm{mg}$（1.00 mmol）、H：$10.8\times\frac{2.0}{18}=1.20\ \mathrm{mg}$（1.20 mmol）、O：$16.4-12.0-1.20=3.2\ \mathrm{mg}$（0.20 mmol）。$\mathrm{C:H:O}=5:6:1$、組成式 $\mathrm{C_5H_6O}$（82）、分子量 164 より $\mathrm{C_{10}H_{12}O_2}$（不飽和度5：ベンゼン環＋C=O）。<br>(2) C：ヨードホルム反応を示し、酸化でアルデヒドになる第一級アルコールはエタノールだけ（2-プロパノールなどはケトンになる）。D：PET の原料のテレフタル酸（$p$-$\mathrm{C_6H_4(COOH)_2}$）。B はベンゼン環のパラ位に炭素原子で結合した置換基を2つもち、一方が $\mathrm{-COOH}$。A の C 10個から C（2個）を除いた C 8個なので、もう一方は $\mathrm{-CH_3}$。<br>(3) B と C のエステル。<br>(4) A は $\dfrac{1.64}{164}=0.0100\ \mathrm{mol}$ で、エステル結合1つにつき NaOH 1 mol を要するので 10.0 mL。<br>(5) $\mathrm{C_8H_8O_2}$ でベンゼン環をもつカルボン酸は、フェニル酢酸 $\mathrm{C_6H_5CH_2COOH}$ と $o$-・$m$-・$p$-トルイル酸の4種類。<br><b>ポイント</b>：加水分解生成物は「炭素数の合計がもとのエステルと一致する」ことを使って、部分構造の大きさを確定させる。"},
 {"lv": "C", "tag": "総合（油脂の構造）",
  "q": r"グリセリン $\mathrm{C_3H_5(OH)_3}$ と脂肪酸からなる油脂 A について、次の実験を行った。<br>・A 8.78 g を完全にけん化するのに、水酸化カリウム 1.68 g を要した。<br>・A 8.78 g に、ヨウ素は最大 15.2 g 付加した。<br>・A を加水分解すると、グリセリンと2種類の脂肪酸 X、Y が物質量の比 1：2 で得られた。<br>・A は不斉炭素原子をもつ。<br>脂肪酸は、ステアリン酸 $\mathrm{C_{17}H_{35}COOH}$、オレイン酸 $\mathrm{C_{17}H_{33}COOH}$、リノール酸 $\mathrm{C_{17}H_{31}COOH}$、リノレン酸 $\mathrm{C_{17}H_{29}COOH}$ のいずれかとする。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、$\mathrm{K}=39$、$\mathrm{I}=127$ とする。<br>(1) A の分子量を求めよ。<br>(2) A 1分子中に含まれる炭素原子間の二重結合の数を求めよ。<br>(3) X（1 の方）と Y（2 の方）の名称を答えよ。<br>(4) グリセリンの3つの炭素のうち、どの位置の炭素に X が結合しているか。A が不斉炭素原子をもつことを用いて説明せよ。<br>(5) A に水素を完全に付加させた油脂は不斉炭素原子をもつか。理由とともに答えよ。",
  "a": r"(1) 878　(2) 6　(3) X ステアリン酸、Y リノレン酸　(4) 端の炭素（1位）。X が中央にあると、中央の炭素に結合する2つの $\mathrm{-CH_2OCOR}$ が同じになり不斉炭素原子とならないから。(5) もたない。脂肪酸がすべてステアリン酸になり、中央の炭素に結合する2つの原子団が同じになるから。",
  "s": r"(1) KOH は $\dfrac{1.68}{56}=0.0300\ \mathrm{mol}$、A はその $\frac13$ の 0.0100 mol。分子量 $\dfrac{8.78}{0.0100}=878$。<br>(2) $\mathrm{I_2}$ は $\dfrac{15.2}{254}=0.0598\fallingdotseq0.0600\ \mathrm{mol}$。A 1 mol に $\mathrm{I_2}$ 6 mol が付加するので C=C は6個。（分子量からも確かめられる：ステアリン酸3分子の油脂は 890 で、C=C 1個ごとに H 2個分の 2 だけ小さくなるので $\frac{890-878}{2}=6$。）<br>(3) 各脂肪酸の C=C は ステアリン酸 0、オレイン酸 1、リノール酸 2、リノレン酸 3。3分子で合計6になる組は (0,3,3)、(1,2,3)、(2,2,2) で、2種類が 1：2 になるのは (0,3,3) だけ。<br>(4) 中央の炭素には H、$\mathrm{-OCOR}$ と2つの $\mathrm{-CH_2OCOR'}$ が結合する。両端の R' が異なるとき（一方の端が X、中央ともう一方の端が Y のとき）だけ不斉炭素原子になる。X が中央にある Y–X–Y の並びでは、両端がどちらも Y なので不斉炭素原子にならない。<br><b>ポイント</b>：油脂の問題は「けん化 → 分子量」「$\mathrm{I_2}$（$\mathrm{H_2}$）の付加 → C=C の数」「加水分解 → 脂肪酸の組」「不斉炭素 → 並び順」と、情報ごとに決まるものを整理する。"},
]}}
strut(CH)


def verify():
    chk(CH)
    A = {"H": 1.0, "C": 12, "O": 16, "K": 39, "I": 127}
    # A1
    r = (58.8 / 12, 9.8 / 1.0, 31.4 / 16); assert [round(x / r[2] * 2) for x in r] == [5, 10, 2]
    assert all(abs(x / r[2] * 2 - k) < 0.02 for x, k in zip(r, (5, 10, 2)))
    assert 100 < mw("C5H10O2", A) == 102 < 110 and du("C5H10O2") == 1
    # A2
    m = isomers("C3H6Cl2"); assert len(m) == 4 and [canon(x) for x in m if asym(x)] == [C("ClCC(Cl)C")]
    # A3
    assert [du(f) for f in ["C6H6", "C4H6", "C3H5Cl", "C8H8O2", "C5H11N", "C6H12O6"]] == [4, 2, 1, 5, 1, 1]
    assert {canon(x) for x in isomers("C4H6", kinds=("CC",))} == {C("C#CCC"), C("CC#CC"), C("C=CC=C"), C("C=C=CC")}
    # B1
    e5 = [x for x in isomers("C5H10O2", kinds=("CO",)) if groups(x)["ester"]]; assert len(e5) == 9
    hit = []
    for x in e5:
        ac, al = hydrolyze(x)
        if not tollens(ac) and iodoform(al) and "alc2" in groups(al):
            hit.append(x)
    assert [canon(x) for x in hit] == [C("CC(=O)OC(C)C")]
    assert sum(1 for x in e5 if tollens(hydrolyze(x)[0])) == 4
    assert [canon(x) for x in e5 if asym(x)] == [C("O=COC(C)CC")]
    cand = {canon(hydrolyze(x)[1]) for x in e5 if iodoform(hydrolyze(x)[1])}
    assert cand == {C("CCO"), C("CC(C)O"), C("CC(O)CC")}
    # B2
    al6 = isomers("C6H12", kinds=("CC",)); one = [x for x in al6 if len(set(ozonolysis(x))) == 1]
    assert {canon(x) for x in one} == {C("CCC=CCC"), C("CC(C)=C(C)C")}
    X = [x for x in one if all(iodoform(y) and not tollens(y) for y in ozonolysis(x, mols=True))]
    assert [canon(x) for x in X] == [C("CC(C)=C(C)C")] and ozonolysis(X[0])[0] == C("CC(=O)C")
    assert ozonolysis(smi("CCC=CCC"))[0] == C("CCC=O") and tollens(smi("CCC=O")) and not iodoform(smi("CCC=O"))
    assert cistrans(smi("CCC=CCC")) == 1 and asym(smi("CC(C)(Br)C(C)(C)Br")) == 0
    # B3
    e8 = [x for x in isomers("C8H8O2", arom=True, kinds=("CO",)) if groups(x)["ester"]]; assert len(e8) == 6
    hitA, phe = [], 0
    for x in e8:
        p, q = hydrolyze(x)
        arom = [y for y in (p, q) if any(o == 3 for o in y.b.values())][0]
        other = q if arom is p else p
        if groups(arom)["phenol"]:
            phe += 1
            if tollens(other) and nsubst(arom, ring=True, el="Br") == 2:
                hitA.append(x)
    assert phe == 4 and [canon(x) for x in hitA] == [C("O=COc1ccc(C)cc1")]
    # B4
    M = 0.30 * 8.3e3 * 400 / (1.0e5 * 0.166); assert round(M) == 60 and abs(M - 60) < 0.05
    r = (40.0 / 12, 6.7 / 1.0, 53.3 / 16); assert [round(x / r[0]) for x in r] == [1, 2, 1] and mw("C2H4O2", A) == 60
    c2 = isomers("C2H4O2", kinds=("CO",)); assert len(c2) == 3
    ok = [x for x in c2 if not groups(x)["COOH"] and not alcohol(groups(x)) and tollens(x)]
    assert [canon(x) for x in ok] == [C("O=COC")]
    assert [canon(x) for x in c2 if groups(x)["COOH"]] == [C("CC(=O)O")]
    # B5
    a5 = isomers("C5H10", kinds=("CC",)); assert nstereo(a5) == 6
    assert {canon(x) for x in a5 if canon(hydrogenate(x)) == C("CC(C)CC")} == {C("C=C(C)CC"), C("CC(C)=CC"), C("C=CC(C)C")}

    def brom(x):  # C=C に Br2 を付加
        (i, j) = next(k for k, o in x.b.items() if o == 4)
        y = Mol(x.a, {**x.b, (i, j): 2}); y = add_atom(y, i, "Br"); return add_atom(y, j, "Br")
    assert [canon(x) for x in a5 if asym(brom(x)) == 2] == [C("CC=CCC")]
    assert sorted(asym(brom(x)) for x in a5) == [1, 1, 1, 1, 2]
    ace = [x for x in a5 if C("CC(C)=O") in ozonolysis(x)]
    assert [canon(x) for x in ace] == [C("CC(C)=CC")] and sorted(ozonolysis(ace[0])) == sorted([C("CC(C)=O"), C("CC=O")])
    # C1
    c, h = 44.0 * 12 / 44, 10.8 * 2.0 / 18; o = 16.4 - c - h
    assert (c / 12, round(h / 1.0, 6), round(o / 16, 6)) == (1.0, 1.2, 0.2) and mw("C10H12O2", A) == 164
    e10 = [x for x in isomers("C10H12O2", arom=True, kinds=("CO",)) if groups(x)["ester"]]
    hit = []
    for x in e10:
        ac, al = hydrolyze(x)
        if len(ac.a) < 6 or not all(ac.b.get((i, i + 1)) == 3 for i in range(5)):
            continue                                   # B はベンゼン環をもつカルボン酸
        if groups(ac)["phenol"] or not iodoform(al) or "alc1" not in groups(al):
            continue
        rs = ring_subs(ac); pos = [p for p, e in enumerate(rs) if e]
        if len(pos) == 2 and (pos[1] - pos[0]) == 3 and all(rs[p] == "C" for p in pos):
            hit.append(x)
    assert [canon(x) for x in hit] == [C("CCOC(=O)c1ccc(C)cc1")]
    assert sf(1.64 / 164 / 1.00 * 1000, 3) == 10.0
    assert sum(1 for x in isomers("C8H8O2", arom=True, kinds=("CO",)) if groups(x)["COOH"]) == 4
    # C2
    nK = 1.68 / 56; nA = nK / 3; MA = 8.78 / nA; assert abs(MA - 878) < 1e-6
    assert sf(15.2 / 254, 2) == 0.060 and sf(nA * 6 * 254, 3) == 15.2
    FA = {"ステアリン酸": ("C18H36O2", 0), "オレイン酸": ("C18H34O2", 1), "リノール酸": ("C18H32O2", 2), "リノレン酸": ("C18H30O2", 3)}
    gly = mw("C3H8O3", A)
    combos = [cb for cb in combinations_with_replacement(FA, 3)
              if abs(gly + sum(mw(FA[k][0], A) for k in cb) - 54 - MA) < 1e-6]
    assert all(sum(FA[k][1] for k in cb) == 6 for cb in combos) and len(combos) == 3
    two = [cb for cb in combos if sorted(Counter(cb).values()) == [1, 2]]
    assert two == [("ステアリン酸", "リノレン酸", "リノレン酸")]
    st = "C(=O)" + "C" * 17
    ln = "C(=O)CCCCCCCC=CCC=CCC=CCC"
    assert len(ln.replace("(=O)", "").replace("=", "")) == 18
    tri = lambda a, b, c: smi(f"C(O{a})C(O{b})CO{c}")
    t1, t2 = tri(st, ln, ln), tri(ln, st, ln)
    hc = lambda x: Counter({**Counter(x.a), "H": x.nH()})
    assert hc(t1) == fml("C57H98O6") and abs(mw("C57H98O6", A) - 878) < 1e-9
    assert asym(t1) == 1 and asym(t2) == 0
    assert asym(hydrogenate(t1)) == 0 and asym(hydrogenate(t2)) == 0
