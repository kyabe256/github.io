"""問題集 第12章 有機化合物の基礎と脂肪族化合物。CH に問題、verify() で元素分析・量的関係を計算し、
異性体は分子グラフの数え上げ（構造異性体を全列挙 → 官能基・不斉炭素・シス-トランス・反応生成物を判定）で確認する。"""
from math import sqrt

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

CH = {12: {
"goal": "元素分析から分子式を決め、構造異性体・立体異性体を漏れなく数え上げる。アルコール・アルデヒド・カルボン酸・エステル・油脂の反応を、量的関係まで扱えるようにする。",
"items": [
 {"lv": "A", "tag": "元素分析",
  "q": r"炭素・水素・酸素からなる化合物 30.0 mg を完全燃焼させたところ、二酸化炭素 66.0 mg と水 36.0 mg が得られた。この化合物の分子量は 60 である。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$ とする。<br>(1) 組成式を求めよ。<br>(2) 分子式を求めよ。<br>(3) この分子式で表される構造異性体をすべて示性式で示せ。",
  "a": r"(1) $\mathrm{C_3H_8O}$　(2) $\mathrm{C_3H_8O}$　(3) $\mathrm{CH_3CH_2CH_2OH}$、$\mathrm{CH_3CH(OH)CH_3}$、$\mathrm{CH_3OCH_2CH_3}$",
  "s": r"(1) C：$66.0\times\dfrac{12}{44}=18.0\ \mathrm{mg}$、H：$36.0\times\dfrac{2.0}{18}=4.0\ \mathrm{mg}$、O：$30.0-18.0-4.0=8.0\ \mathrm{mg}$。物質量の比は $\mathrm{C:H:O}=\dfrac{18.0}{12}:\dfrac{4.0}{1.0}:\dfrac{8.0}{16}=1.5:4.0:0.50=3:8:1$。<br>(2) 組成式量 60 が分子量と等しいので、分子式も $\mathrm{C_3H_8O}$。<br>(3) 不飽和度 0 で、O が C–O–H（アルコール）か C–O–C（エーテル）。アルコールは OH の位置で2種類、エーテルは1種類で計3種類。<br><b>ポイント</b>：O の質量は「試料 − C − H」で求める。分子式が決まったら、まず不飽和度を計算して官能基の候補をしぼる。"},
 {"lv": "A", "tag": "異性体",
  "q": r"分子式 $\mathrm{C_4H_9Cl}$ で表される化合物について、(1) 構造異性体の数、(2) 不斉炭素原子をもつ化合物の示性式、(3) 立体異性体（鏡像異性体）も区別したときの異性体の総数、を答えよ。",
  "a": r"(1) 4　(2) $\mathrm{CH_3C^*HClCH_2CH_3}$（2-クロロブタン）　(3) 5",
  "s": r"炭素骨格は直鎖 C–C–C–C と枝分かれ C–C(C)–C の2通り。直鎖では Cl の位置が端か内側かで2種類、枝分かれでも端（$\mathrm{(CH_3)_2CHCH_2Cl}$）か中央（$\mathrm{(CH_3)_3CCl}$）かで2種類、計4種類。<br>不斉炭素原子は4つの異なる原子・原子団（$\mathrm{H}$、$\mathrm{Cl}$、$\mathrm{CH_3}$、$\mathrm{C_2H_5}$）が結合した 2-クロロブタンの C2 だけ。鏡像異性体が1組あるので総数は $4+1=5$。<br><b>ポイント</b>：異性体は「炭素骨格を決める → 置換基の位置を対称性で重複なく置く」の順に数える。"},
 {"lv": "A", "tag": "官能基の検出",
  "q": r"次の化合物（ア）〜（カ）のうち、(a) 銀鏡反応を示すもの、(b) ヨードホルム反応を示すもの、(c) 炭酸水素ナトリウム水溶液を加えると気体が発生するもの、をそれぞれすべて選べ。<br>（ア）メタノール　（イ）エタノール　（ウ）アセトアルデヒド　（エ）アセトン　（オ）酢酸　（カ）ギ酸",
  "a": r"(a) ウ、カ　(b) イ、ウ、エ　(c) オ、カ",
  "s": r"(a) ホルミル基 $\mathrm{-CHO}$ をもつもの。ギ酸 $\mathrm{HCOOH}$ は分子内に $\mathrm{-CHO}$ の構造をもつので還元性がある。<br>(b) $\mathrm{CH_3CO-R}$ または $\mathrm{CH_3CH(OH)-R}$（R は H または炭化水素基）の構造をもつもの。エタノールは $\mathrm{CH_3CH(OH)-H}$ にあたる。酢酸は $\mathrm{CH_3CO-}$ をもつが、R が $\mathrm{OH}$ なので示さない。<br>(c) 炭酸より強い酸（カルボン酸）が $\mathrm{RCOOH + NaHCO_3 \to RCOONa + H_2O + CO_2}$ で $\mathrm{CO_2}$ を発生する。<br><b>ポイント</b>：ギ酸は「カルボン酸なのに還元性がある」、酢酸は「$\mathrm{CH_3CO-}$ をもつのにヨードホルム反応を示さない」。例外として必ずおさえる。"},
 {"lv": "A", "tag": "アセチレンの反応",
  "q": r"(1) アセチレンに次の物質を付加させたときに得られる化合物の名称を答えよ。<br>　① 水（硫酸水銀(II) を触媒とする）　② 塩化水素　③ 酢酸<br>(2) アセチレン3分子が重合して得られる化合物の名称を答えよ。<br>(3) 炭化カルシウム 3.20 g に十分な量の水を加えて発生したアセチレンに、臭素を付加させる。付加しうる臭素は最大何 g か。$\mathrm{C}=12$、$\mathrm{Ca}=40$、$\mathrm{Br}=80$ とする。",
  "a": r"(1) ① アセトアルデヒド　② 塩化ビニル　③ 酢酸ビニル　(2) ベンゼン　(3) 16.0 g",
  "s": r"(1) ① まず不安定なビニルアルコール $\mathrm{CH_2{=}CHOH}$ が生じ、ただちにアセトアルデヒド $\mathrm{CH_3CHO}$ に変わる。② $\mathrm{CH_2{=}CHCl}$。③ $\mathrm{CH_2{=}CHOCOCH_3}$。②③ はそれぞれポリ塩化ビニル・ポリ酢酸ビニルの単量体。<br>(3) $\mathrm{CaC_2 + 2H_2O \to Ca(OH)_2 + C_2H_2}$。$\mathrm{CaC_2}=64$ より $\mathrm{C_2H_2}$ は $\dfrac{3.20}{64}=0.0500\ \mathrm{mol}$。三重結合には $\mathrm{Br_2}$ が2分子付加する（$\mathrm{C_2H_2 + 2Br_2 \to CHBr_2CHBr_2}$）ので、$0.100\times160=16.0\ \mathrm{g}$。<br><b>ポイント</b>：付加する $\mathrm{H_2}$・$\mathrm{Br_2}$ の物質量は「二重結合1つに1分子、三重結合1つに2分子」。"},
 {"lv": "B", "tag": "異性体（アルケン）",
  "q": r"分子式 $\mathrm{C_4H_8}$ で表される化合物について答えよ。<br>(1) 立体異性体も区別すると、異性体は全部で何種類あるか。また、そのうち環をもつものの名称を答えよ。<br>(2) 水素を付加させるとブタンになるものを、立体異性体も区別してすべて答えよ。<br>(3) シス-トランス異性体が存在する化合物の名称を答えよ。<br>(4) 1-ブテン、2-ブテン、2-メチルプロペンにそれぞれ臭素を付加させた。得られる化合物のうち、不斉炭素原子をもつものの名称と、1分子中の不斉炭素原子の数を答えよ。",
  "a": r"(1) 6種類。シクロブタン、メチルシクロプロパン　(2) 1-ブテン、シス-2-ブテン、トランス-2-ブテン　(3) 2-ブテン　(4) 1,2-ジブロモブタン（1個）、2,3-ジブロモブタン（2個）",
  "s": r"$\mathrm{C_4H_8}$ の不飽和度は1で、二重結合1つか環1つ。アルケンは $\mathrm{CH_2{=}CHCH_2CH_3}$、$\mathrm{CH_3CH{=}CHCH_3}$（シスとトランス）、$\mathrm{CH_2{=}C(CH_3)_2}$ の4種類、シクロアルカンは2種類で、計6種類。<br>(2) 直鎖の骨格をもつアルケン。2-メチルプロペンからは 2-メチルプロパンが生じる。<br>(3) 二重結合の両端の炭素にそれぞれ異なる原子・原子団が結合しているもの。1-ブテンは片方の炭素に H が2個、2-メチルプロペンは片方の炭素に $\mathrm{CH_3}$ が2個結合しているので存在しない。<br>(4) $\mathrm{CH_2BrC^*HBrCH_2CH_3}$、$\mathrm{CH_3C^*HBrC^*HBrCH_3}$。$\mathrm{CH_2BrCBr(CH_3)_2}$ の C は $\mathrm{CH_3}$ を2個もつので不斉炭素ではない。<br><b>ポイント</b>：「分子式 $\mathrm{C}_n\mathrm{H}_{2n}$ ＝ アルケン」と決めつけない。不飽和度1は環の可能性も必ず考える。"},
 {"lv": "B", "tag": "アルコールの反応",
  "q": r"分子式 $\mathrm{C_4H_{10}O}$ で表される化合物について答えよ。<br>(1) 構造異性体は何種類あるか。そのうち、ナトリウムと反応しないものは何種類か。<br>(2) $\mathrm{C_4H_{10}O}$ のアルコール A〜D は、次の性質をもつ。A〜D の示性式を答えよ。<br>　・A は硫酸酸性の二クロム酸カリウム水溶液で酸化されにくい。<br>　・B を酸化するとケトンが得られる。B は不斉炭素原子をもつ。<br>　・C と D を酸化するとアルデヒドを経てカルボン酸が得られる。C の炭素骨格は枝分かれをもたない。<br>(3) A〜D のうち、ヨードホルム反応を示すものを選べ。<br>(4) B を濃硫酸と加熱して分子内で脱水させると、何種類のアルケンが得られるか。シス-トランス異性体を区別して答えよ。",
  "a": r"(1) 7種類、3種類　(2) A $\mathrm{(CH_3)_3COH}$　B $\mathrm{CH_3CH(OH)CH_2CH_3}$　C $\mathrm{CH_3CH_2CH_2CH_2OH}$　D $\mathrm{(CH_3)_2CHCH_2OH}$　(3) B　(4) 3種類",
  "s": r"(1) アルコール4種類（第一級2・第二級1・第三級1）とエーテル3種類（$\mathrm{CH_3OCH_2CH_2CH_3}$、$\mathrm{CH_3OCH(CH_3)_2}$、$\mathrm{C_2H_5OC_2H_5}$）。エーテルは $\mathrm{-OH}$ をもたないのでナトリウムと反応しない。<br>(2) 第三級アルコールは酸化されにくい（A）。第二級はケトンに（B）、第一級はアルデヒドからカルボン酸に（C・D）酸化される。<br>(3) $\mathrm{CH_3CH(OH)-}$ をもつのは B だけ。A は OH のついた炭素に H がない。<br>(4) OH のついた C2 の隣の C1 または C3 から H がとれる。C1 からは 1-ブテン、C3 からは 2-ブテン（シスとトランス）で、計3種類。<br><b>ポイント</b>：アルコールの級数（OH のついた炭素に結合した炭素の数）で、酸化生成物が決まる。"},
 {"lv": "B", "tag": "エステル化と平衡",
  "q": r"酢酸 0.50 mol とエタノール 0.50 mol に少量の濃硫酸を加えて加熱したところ、平衡に達した。この温度でのエステル化の平衡定数を $K=4.0$ とする。<br>(1) この反応を化学反応式で表せ。<br>(2) 平衡に達したときの酢酸エチルの物質量を求めよ。<br>(3) エタノールを 1.0 mol に増やして同じ操作をすると、生じる酢酸エチルは何 mol か。$\sqrt3=1.73$ とする。<br>(4) 濃硫酸のはたらきを答えよ。また、反応後の混合物を炭酸水素ナトリウム水溶液で洗う理由を答えよ。",
  "a": r"(1) $\mathrm{CH_3COOH + C_2H_5OH \rightleftarrows CH_3COOC_2H_5 + H_2O}$　(2) 0.33 mol　(3) 0.42 mol　(4) 触媒（および脱水剤）としてはたらく。残っている酢酸（と硫酸）を塩にして水層に移し、除くため。",
  "s": r"(2) 生じたエステルを $x$ mol とすると、体積 $V$ は消えるので $K=\dfrac{x\cdot x}{(0.50-x)^2}=4.0$。$\dfrac{x}{0.50-x}=2$ より $x=\dfrac13\fallingdotseq0.33\ \mathrm{mol}$。<br>(3) $\dfrac{x^2}{(0.50-x)(1.0-x)}=4.0$ を整理すると $3x^2-6x+2=0$。$x=\dfrac{3-\sqrt3}{3}=\dfrac{3-1.73}{3}=0.42\ \mathrm{mol}$（もう一つの解 1.58 は 0.50 を超えるので不適）。エタノールを増やすと平衡が右へ移り、エステルが増える。<br>(4) エステル化は可逆反応で、濃硫酸は反応を速める触媒。生じた水を吸収して平衡を右へ移すはたらきもある。<br><b>ポイント</b>：エステル化の平衡定数では体積が約分される（係数の和が両辺で等しい）。二次方程式の解は「物質量が負にならない」条件で選ぶ。"},
 {"lv": "B", "tag": "油脂の計算",
  "q": r"1種類の脂肪酸だけからなる油脂 A がある。A 4.42 g を完全にけん化するのに、水酸化カリウム 0.840 g を要した。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、$\mathrm{K}=39$、$\mathrm{I}=127$ とする。<br>(1) A の分子量を求めよ。<br>(2) A を構成する脂肪酸を、次から選べ。<br>　ステアリン酸 $\mathrm{C_{17}H_{35}COOH}$、オレイン酸 $\mathrm{C_{17}H_{33}COOH}$、リノール酸 $\mathrm{C_{17}H_{31}COOH}$、リノレン酸 $\mathrm{C_{17}H_{29}COOH}$<br>(3) A 4.42 g に付加するヨウ素は最大何 g か。<br>(4) A のけん化価（油脂 1 g をけん化するのに必要な KOH の mg 数）とヨウ素価（油脂 100 g に付加する $\mathrm{I_2}$ の g 数）を求めよ。",
  "a": r"(1) 884　(2) オレイン酸　(3) 3.81 g　(4) けん化価 190、ヨウ素価 86.2",
  "s": r"(1) 油脂はエステル結合を3つもち、1 mol のけん化に KOH 3 mol を要する。$\mathrm{KOH}=56$ より $\dfrac{0.840}{56}=0.0150\ \mathrm{mol}$、A は $0.00500\ \mathrm{mol}$、分子量 $\dfrac{4.42}{0.00500}=884$。<br>(2) 脂肪酸の分子量を $M$ とすると、グリセリン（92）＋脂肪酸3分子 − 水3分子 で $3M+92-54=884$、$M=282$。オレイン酸（$\mathrm{C_{18}H_{34}O_2}$）が該当。<br>(3) オレイン酸は C=C を1個もつので、A 1分子に C=C は3個。$\mathrm{I_2}$ は $0.00500\times3=0.0150\ \mathrm{mol}$、$0.0150\times254=3.81\ \mathrm{g}$。<br>(4) けん化価 $\dfrac{840\ \mathrm{mg}}{4.42}=190$、ヨウ素価 $\dfrac{3.81}{4.42}\times100=86.2$。<br><b>ポイント</b>：けん化価は分子量の目安（大きいほど分子量が小さい）、ヨウ素価は C=C の数の目安（大きいほど不飽和）。"},
 {"lv": "B", "tag": "論述（セッケン）",
  "q": r"高級脂肪酸のナトリウム塩 $\mathrm{RCOONa}$ はセッケンとして用いられる。<br>(1) セッケンの水溶液が弱い塩基性を示す理由を、イオン反応式を用いて説明せよ。<br>(2) セッケンが油汚れを落とすしくみを、「疎水基」「親水基」の語を用いて 80 字以内で説明せよ。<br>(3) セッケンを硬水（$\mathrm{Ca^{2+}}$ や $\mathrm{Mg^{2+}}$ を多く含む水）中で使うと泡立ちが悪く、洗浄力が落ちる。理由を 40 字以内で答えよ。<br>(4) 硫酸ドデシルナトリウム $\mathrm{C_{12}H_{25}OSO_3Na}$ などの合成洗剤が、硬水中や酸性の水溶液中でも使える理由を答えよ。",
  "a": r"(1) $\mathrm{RCOO^- + H_2O \rightleftarrows RCOOH + OH^-}$ の加水分解が起こるから。(2) 解答例：セッケン分子は疎水基を油に向け、親水基を外側の水に向けて油滴を取り囲み、ミセルとして水中に分散させる。この乳化作用で油汚れが繊維から離れる。（70字／80字以内）(3) 解答例：カルシウムイオンやマグネシウムイオンと水に溶けにくい塩をつくって沈殿するから。（39字／40字以内）　(4) 強酸と強塩基からなる塩なので加水分解せず中性で、カルシウム塩も水に溶けやすいから。",
  "s": r"(1) $\mathrm{RCOOH}$ は弱酸なので、その陰イオンは水から $\mathrm{H^+}$ を受け取り、$\mathrm{OH^-}$ が生じる。そのため羊毛や絹（タンパク質）は傷みやすい。<br>(2) 長い炭化水素基 R が疎水基、$\mathrm{-COO^-}$ が親水基。水の表面に並んで表面張力を下げ、繊維のすき間にしみこみやすくするはたらき（界面活性）もある。<br>(3) $\mathrm{2RCOO^- + Ca^{2+} \to (RCOO)_2Ca}$。酸性の水溶液では $\mathrm{RCOOH}$ が遊離して、やはり洗浄力を失う。<br>(4) 硫酸エステルの塩やスルホン酸塩は、強酸の陰イオンなので $\mathrm{H^+}$ と結びつきにくい。<br><b>ポイント</b>：セッケンと合成洗剤の違いは「もとの酸の強さ」で説明できる（弱酸の塩か強酸の塩か）。"},
 {"lv": "C", "tag": "構造決定（アルコール）",
  "q": r"分子式 $\mathrm{C_5H_{12}O}$ で表されるアルコールについて、次の問いに答えよ。<br>(1) 構造異性体は何種類あるか。<br>(2) (1) のうち、不斉炭素原子をもつものは何種類か。<br>(3) アルコール A は次の性質をもつ。A の示性式と名称を答えよ。<br>　ア　硫酸酸性の二クロム酸カリウム水溶液で酸化するとケトンが得られる。<br>　イ　ヨードホルム反応を示す。<br>　ウ　濃硫酸と加熱して分子内脱水させると、シス-トランス異性体を区別して数えて3種類のアルケンが得られる。<br>(4) (1) のアルコールのうち、二クロム酸カリウムで酸化されにくいものの名称を答えよ。また、それを分子内脱水して得られるアルケンをすべて示性式で示せ。",
  "a": r"(1) 8種類　(2) 3種類　(3) $\mathrm{CH_3CH(OH)CH_2CH_2CH_3}$、2-ペンタノール　(4) 2-メチル-2-ブタノール。$\mathrm{CH_2{=}C(CH_3)CH_2CH_3}$、$\mathrm{(CH_3)_2C{=}CHCH_3}$",
  "s": r"(1) 炭素骨格は3通り。直鎖 C–C–C–C–C に OH をつける位置は3通り（1-、2-、3-ペンタノール）、C–C(C)–C–C は4通り（2-メチル-1-ブタノール、2-メチル-2-ブタノール、3-メチル-2-ブタノール、3-メチル-1-ブタノール）、C–C(C)(C)–C は1通り（2,2-ジメチル-1-プロパノール）で、計8種類。<br>(2) 2-ペンタノール $\mathrm{CH_3C^*H(OH)CH_2CH_2CH_3}$、2-メチル-1-ブタノール $\mathrm{HOCH_2C^*H(CH_3)CH_2CH_3}$、3-メチル-2-ブタノール $\mathrm{CH_3C^*H(OH)CH(CH_3)_2}$ の3種類。<br>(3) ア より第二級アルコール：2-ペンタノール、3-ペンタノール、3-メチル-2-ブタノール。イ より $\mathrm{CH_3CH(OH)-}$ をもつ：2-ペンタノールと 3-メチル-2-ブタノール。ウ：2-ペンタノールからは 1-ペンテンと 2-ペンテン（シス・トランス）の3種類、3-メチル-2-ブタノールからは 3-メチル-1-ブテンと 2-メチル-2-ブテンの2種類。よって A は 2-ペンタノール。<br>(4) 第三級アルコールは 2-メチル-2-ブタノール $\mathrm{(CH_3)_2C(OH)CH_2CH_3}$ だけ。隣の $\mathrm{CH_3}$ から H がとれると 2-メチル-1-ブテン、$\mathrm{CH_2}$ からとれると 2-メチル-2-ブテン（どちらもシス-トランス異性体はない）。<br><b>ポイント</b>：条件を1つずつ使って候補を表にし、消していく。脱水生成物の数は「OH の隣の、H をもつ炭素」の種類で決まり、シス-トランス異性体の有無も確認する。"},
 {"lv": "C", "tag": "構造決定（炭化水素）",
  "q": r"鎖式炭化水素 X 0.10 mol を完全燃焼させたところ、二酸化炭素 0.50 mol と水 0.40 mol が生じた。<br>(1) X の分子式を求めよ。<br>(2) X 1 mol には水素が最大 2 mol 付加する。また、末端に三重結合（$\mathrm{-C{\equiv}C{-}H}$）をもつ化合物はアンモニア性硝酸銀水溶液と反応して白色沈殿を生じることが知られており、X もこの反応を示した。(1) の分子式をもち、三重結合を1つもつ鎖式の化合物をすべて示性式で示せ。<br>(3) X に水素を完全に付加させた化合物 Y の水素原子1個を塩素原子で置換した化合物には、3種類の構造異性体がある。X の示性式を答えよ。<br>(4) X に、硫酸水銀(II) を触媒として水1分子を付加させると化合物 Z が得られた。Z は銀鏡反応を示さず、ヨードホルム反応を示した。Z の示性式を答えよ。",
  "a": r"(1) $\mathrm{C_5H_8}$　(2) $\mathrm{CH{\equiv}CCH_2CH_2CH_3}$、$\mathrm{CH_3C{\equiv}CCH_2CH_3}$、$\mathrm{CH{\equiv}CCH(CH_3)_2}$　(3) $\mathrm{CH{\equiv}CCH_2CH_2CH_3}$　(4) $\mathrm{CH_3COCH_2CH_2CH_3}$",
  "s": r"(1) 1 mol あたり C 5 mol、H $0.40\times2\div0.10=8$ mol で $\mathrm{C_5H_8}$（不飽和度2）。<br>(2) 水素が 2 mol 付加するので、三重結合1つまたは二重結合2つ。三重結合をもつものは、直鎖で位置が2通り（1-ペンチン、2-ペンチン）と、枝分かれの 3-メチル-1-ブチンの3種類。<br>(3) 白色沈殿を生じるのは末端に三重結合をもつ 1-ペンチンと 3-メチル-1-ブチン。水素付加物はそれぞれペンタンと 2-メチルブタン。一塩素置換体はペンタンが 1-、2-、3-クロロペンタンの3種類、2-メチルブタンは4種類なので、X は 1-ペンチン。<br>(4) $\mathrm{H_2O}$ が付加すると、OH が二重結合の炭素についた不安定な化合物（エノール）を経てカルボニル化合物になる。アルデヒド（ペンタナール）ではなく、ヨードホルム反応を示すので $\mathrm{CH_3CO-}$ をもつ 2-ペンタノン。<br><b>ポイント</b>：燃焼の結果 → 分子式 → 不飽和度 → 候補の列挙 → 反応で絞り込み、の順に進める。置換体の数は「等価でない H の種類の数」。"},
]}}
strut(CH)


def verify():
    chk(CH)
    A = {"H": 1.0, "C": 12, "O": 16, "K": 39, "I": 127, "Ca": 40, "Br": 80}
    # A1
    c, h = 66.0 * 12 / 44, 36.0 * 2.0 / 18; o = 30.0 - c - h
    assert (c, h, round(o, 6)) == (18.0, 4.0, 8.0) and (c / 12, h / 1.0, o / 16) == (1.5, 4.0, 0.5)
    assert mw("C3H8O", A) == 60
    m3 = isomers("C3H8O"); assert len(m3) == 3
    assert {canon(m) for m in m3} == {C("CCCO"), C("CC(O)C"), C("COCC")}
    # A2
    m = isomers("C4H9Cl"); assert len(m) == 4 and nstereo(m) == 5
    assert [canon(x) for x in m if asym(x)] == [C("CC(Cl)CC")]
    # A3
    T = {"ア": "CO", "イ": "CCO", "ウ": "CC=O", "エ": "CC(=O)C", "オ": "CC(=O)O", "カ": "O=CO"}
    assert [k for k, s in T.items() if tollens(smi(s))] == ["ウ", "カ"]
    assert [k for k, s in T.items() if iodoform(smi(s))] == ["イ", "ウ", "エ"]
    assert [k for k, s in T.items() if groups(smi(s))["COOH"]] == ["オ", "カ"]
    # A4
    for e in ["CaC2 + 2H2O -> Ca(OH)2 + C2H2", "C2H2 + 2Br2 -> C2H2Br4", "C2H2 + H2O -> C2H4O",
              "C2H2 + HCl -> C2H3Cl", "C2H2 + C2H4O2 -> C4H6O2", "3C2H2 -> C6H6"]:
        eq(e)
    assert sf(3.20 / mw("CaC2", A) * 2 * 160, 3) == 16.0
    # B1
    c4 = isomers("C4H8", kinds=("CC", "ring")); assert len(c4) == 5 and nstereo(c4) == 6
    ringed = [x for x in c4 if not groups(x)["C=C"]]
    assert {canon(x) for x in ringed} == {C("C1CCC1"), C("CC1CC1")}
    butane = C("CCCC")
    alk = [x for x in c4 if groups(x)["C=C"]]
    assert sum(2 ** cistrans(x) for x in alk if canon(hydrogenate(x)) == butane) == 3
    assert [canon(x) for x in alk if cistrans(x)] == [C("CC=CC")]
    assert asym(smi("BrCC(Br)CC")) == 1 and asym(smi("CC(Br)C(Br)C")) == 2 and asym(smi("BrCC(Br)(C)C")) == 0
    # B2
    c4o = isomers("C4H10O"); gs = [groups(x) for x in c4o]
    assert len(c4o) == 7 and sum(1 for g in gs if g["ether"]) == 3
    alcs = [x for x, g in zip(c4o, gs) if alcohol(g)]; assert len(alcs) == 4
    lv = {canon(x): next(k for k in groups(x) if k.startswith("alc")) for x in alcs}
    assert [k for k, v in lv.items() if v == "alc3"] == [C("CC(C)(C)O")]
    sec = [x for x in alcs if lv[canon(x)] == "alc2"]; assert [canon(x) for x in sec] == [C("CC(O)CC")] and asym(sec[0]) == 1
    assert {k for k, v in lv.items() if v == "alc1"} == {C("CCCCO"), C("CC(C)CO")}
    assert [canon(x) for x in alcs if iodoform(x)] == [C("CC(O)CC")]
    assert sum(2 ** cistrans(x) for x in dehydrate(sec[0])) == 3
    # B3
    x = 1 / 3; assert abs(x * x / (0.50 - x) ** 2 - 4.0) < 1e-12 and sf(x) == 0.33
    r = (3 - sqrt(3)) / 3; assert abs(3 * r * r - 6 * r + 2) < 1e-12 and abs(r * r / ((0.5 - r) * (1.0 - r)) - 4) < 1e-9
    assert sf(r) == 0.42 and round((3 - 1.73) / 3, 2) == 0.42 and (3 + sqrt(3)) / 3 > 0.50
    eq("C2H4O2 + C2H6O -> C4H8O2 + H2O")
    # B4
    nk = 0.840 / 56; nA = nk / 3; MA = 4.42 / nA; assert abs(MA - 884) < 1e-6
    acids = {"ステアリン酸": "C18H36O2", "オレイン酸": "C18H34O2", "リノール酸": "C18H32O2", "リノレン酸": "C18H30O2"}
    hit = [k for k, f in acids.items() if abs(3 * mw(f, A) + mw("C3H8O3", A) - 3 * 18 - MA) < 1e-6]
    assert hit == ["オレイン酸"]
    assert sf(nA * 3 * 254, 3) == 3.81 and sf(840 / 4.42, 3) == 190 and sf(3.81 / 4.42 * 100, 3) == 86.2
    # C1
    c5 = isomers("C5H12O"); al = [x for x in c5 if alcohol(groups(x))]
    assert len(al) == 8 and sum(1 for x in al if asym(x)) == 3
    lv = lambda x: next(k for k in groups(x) if k.startswith("alc"))
    cand = [x for x in al if lv(x) == "alc2" and iodoform(x)]
    assert {canon(x) for x in cand} == {C("CC(O)CCC"), C("CC(O)C(C)C")}
    hitA = [x for x in cand if sum(2 ** cistrans(y) for y in dehydrate(x)) == 3]
    assert [canon(x) for x in hitA] == [C("CC(O)CCC")]
    ter = [x for x in al if lv(x) == "alc3"]; assert [canon(x) for x in ter] == [C("CC(C)(O)CC")]
    d = dehydrate(ter[0]); assert {canon(y) for y in d} == {C("C=C(C)CC"), C("CC(C)=CC")} and all(cistrans(y) == 0 for y in d)
    # C2
    assert (0.50 / 0.10, 0.40 * 2 / 0.10) == (5.0, 8.0) and du("C5H8") == 2
    c58 = [x for x in isomers("C5H8", kinds=("CC",)) if groups(x)["C#C"]]
    assert {canon(x) for x in c58} == {C("C#CCCC"), C("CC#CCC"), C("C#CC(C)C")}
    term = [x for x in c58 if any(x.a[i] == "C" and x.h(i) == 1 and any(o == 6 for _, o in x.adj()[i]) for i in range(len(x.a)))]
    hitX = [x for x in term if nsubst(hydrogenate(x)) == 3]
    assert [canon(x) for x in hitX] == [C("C#CCCC")]
    assert nsubst(smi("CC(C)CC")) == 4
    Z = smi("CC(=O)CCC"); assert iodoform(Z) and not tollens(Z) and tollens(smi("O=CCCCC"))
