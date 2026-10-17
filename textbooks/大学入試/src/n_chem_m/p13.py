"""問題集 第13章 芳香族化合物。CH に問題、verify() で反応式・収率・分配平衡を計算し、
異性体はベンゼン環を土台にした分子グラフの全列挙（官能基・置換体の数・側鎖の酸化）で確認する。"""

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

CH = {13: {
"goal": "ベンゼンの置換反応と、フェノール・芳香族カルボン酸・アニリンの反応を「流れ」で整理する。酸の強弱を使った抽出分離と、ベンゼン環をもつ異性体の数え上げを確実にする。",
"items": [
 {"lv": "A", "tag": "ベンゼンの反応",
  "q": r"ベンゼンに次の (1)〜(5) の操作を行ったときに得られる有機化合物の名称を答え、それぞれの反応が置換反応・付加反応のどちらであるかを答えよ。<br>(1) 濃硝酸と濃硫酸の混合物を加えて約 60 ℃ に温める。<br>(2) 濃硫酸を加えて加熱する。<br>(3) 鉄粉（または塩化鉄(III)）を触媒として塩素を通じる。<br>(4) ニッケルを触媒として、高温・高圧で水素を反応させる。<br>(5) 紫外線を当てながら塩素を反応させる。",
  "a": r"(1) ニトロベンゼン、置換　(2) ベンゼンスルホン酸、置換　(3) クロロベンゼン、置換　(4) シクロヘキサン、付加　(5) 1,2,3,4,5,6-ヘキサクロロシクロヘキサン、付加",
  "s": r"(1) $\mathrm{C_6H_6 + HNO_3 \to C_6H_5NO_2 + H_2O}$（ニトロ化）。(2) $\mathrm{C_6H_6 + H_2SO_4 \to C_6H_5SO_3H + H_2O}$（スルホン化）。(3) $\mathrm{C_6H_6 + Cl_2 \to C_6H_5Cl + HCl}$（ハロゲン化）。(4) $\mathrm{C_6H_6 + 3H_2 \to C_6H_{12}}$。(5) $\mathrm{C_6H_6 + 3Cl_2 \to C_6H_6Cl_6}$。<br>ベンゼン環は安定で、ふつうは環の構造を保つ置換反応が起こる。付加反応は高温・高圧や光など、特別な条件でだけ起こる。<br><b>ポイント</b>：「触媒（Fe・$\mathrm{FeCl_3}$）＋ $\mathrm{Cl_2}$ → 置換」「光 ＋ $\mathrm{Cl_2}$ → 付加」の区別は頻出。"},
 {"lv": "A", "tag": "正誤（フェノール）",
  "q": r"フェノールに関する次の記述①〜⑥のうち、誤りを含むものをすべて選べ。<br>① フェノールの水溶液に塩化鉄(III) 水溶液を加えると、紫色を呈する。<br>② フェノールは炭酸より強い酸なので、炭酸水素ナトリウム水溶液に溶けて二酸化炭素を発生する。<br>③ ナトリウムフェノキシドの水溶液に二酸化炭素を通じると、フェノールが遊離する。<br>④ フェノールの水溶液に臭素水を加えると、2,4,6-トリブロモフェノールの白色沈殿が生じる。<br>⑤ フェノールは水酸化ナトリウム水溶液と反応しない。<br>⑥ フェノールは工業的にはクメン法でつくられ、同時にアセトンが得られる。",
  "a": r"②、⑤",
  "s": r"② 誤：酸の強さは カルボン酸 ＞ 炭酸 ＞ フェノール。フェノールは $\mathrm{NaHCO_3}$ と反応しない。③ 正：弱い酸の塩に強い酸を加えると弱い酸が遊離する。$\mathrm{C_6H_5ONa + CO_2 + H_2O \to C_6H_5OH + NaHCO_3}$。⑤ 誤：フェノールは弱酸で、$\mathrm{C_6H_5OH + NaOH \to C_6H_5ONa + H_2O}$ のように中和する。④ 正：$\mathrm{C_6H_5OH + 3Br_2 \to C_6H_2Br_3OH + 3HBr}$。<br><b>ポイント</b>：酸の強さの順「塩酸・硫酸 ＞ カルボン酸 ＞ 炭酸 ＞ フェノール」は、抽出・遊離の問題すべての土台になる。"},
 {"lv": "A", "tag": "異性体（芳香族）",
  "q": r"分子式 $\mathrm{C_7H_8O}$ で表され、ベンゼン環をもつ化合物について答えよ。<br>(1) 構造異性体は何種類あるか。すべての名称を答えよ。<br>(2) (1) のうち、塩化鉄(III) 水溶液で呈色するものは何種類か。<br>(3) (1) のうち、ナトリウムと反応しないものの名称を答えよ。",
  "a": r"(1) 5種類：$o$-クレゾール、$m$-クレゾール、$p$-クレゾール、ベンジルアルコール、アニソール（メチルフェニルエーテル）　(2) 3種類　(3) アニソール",
  "s": r"ベンゼン環 $\mathrm{C_6}$ のほかに C 1個と O 1個。① 置換基2つ（$\mathrm{-CH_3}$ と $\mathrm{-OH}$）：オルト・メタ・パラの3種類（クレゾール）。② 置換基1つ：$\mathrm{-CH_2OH}$（ベンジルアルコール）、$\mathrm{-OCH_3}$（アニソール）。<br>(2) ベンゼン環に直接 $\mathrm{-OH}$ が結合したフェノール類（クレゾール3種）。<br>(3) $\mathrm{-OH}$ をもたないエーテル。ベンジルアルコールはアルコールなのでナトリウムと反応するが、塩化鉄(III) では呈色しない。<br><b>ポイント</b>：芳香族の異性体は「置換基1つ」「置換基2つ（$o$・$m$・$p$）」「置換基3つ」と、置換基の数で場合分けする。"},
 {"lv": "A", "tag": "アニリン",
  "q": r"ニトロベンゼンにスズと濃塩酸を加えて加熱し、反応後に水酸化ナトリウム水溶液を加えると、アニリンが遊離する。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{N}=14$、$\mathrm{O}=16$ とする。<br>(1) スズと濃塩酸で還元した直後、アニリンはどのような化合物として溶液中に存在するか。<br>(2) アニリンの検出に用いる、さらし粉水溶液を加えたときの呈色を答えよ。<br>(3) アニリンに無水酢酸を作用させて得られる化合物の名称と、生じた結合の名称を答えよ。<br>(4) ニトロベンゼン 24.6 g からアニリンが 14.0 g 得られた。収率は何 % か。",
  "a": r"(1) アニリン塩酸塩 $\mathrm{C_6H_5NH_3Cl}$　(2) 赤紫色　(3) アセトアニリド、アミド結合　(4) 75.3 %",
  "s": r"(1) $\mathrm{2C_6H_5NO_2 + 3Sn + 14HCl \to 2C_6H_5NH_3Cl + 3SnCl_4 + 4H_2O}$。アニリンは塩基なので、酸性の溶液中では塩になっている。$\mathrm{C_6H_5NH_3Cl + NaOH \to C_6H_5NH_2 + NaCl + H_2O}$ で遊離させる（弱塩基の遊離）。<br>(3) $\mathrm{C_6H_5NH_2 + (CH_3CO)_2O \to C_6H_5NHCOCH_3 + CH_3COOH}$（アセチル化）。<br>(4) $\mathrm{C_6H_5NO_2}=123$、$\mathrm{C_6H_5NH_2}=93$。理論量は $\dfrac{24.6}{123}\times93=18.6\ \mathrm{g}$、収率は $\dfrac{14.0}{18.6}\times100=75.3$ %。<br><b>ポイント</b>：収率 ＝ 実際の量 ÷ 理論量。理論量は「出発物質の物質量 × 係数比 × 生成物のモル質量」。"},
 {"lv": "B", "tag": "抽出による分離",
  "q": r"アニリン、フェノール、安息香酸、トルエンを含むジエチルエーテル溶液について、分液ろうとを用いて次の操作を行った。<br>操作1：希塩酸を加えてよく振り混ぜ、水層 I とエーテル層に分けた。<br>操作2：エーテル層に炭酸水素ナトリウム水溶液を加えて振り混ぜると気体が発生した。水層 II とエーテル層に分けた。<br>操作3：エーテル層に水酸化ナトリウム水溶液を加えて振り混ぜ、水層 III とエーテル層 IV に分けた。<br>(1) 水層 I〜III およびエーテル層 IV に含まれる芳香族化合物を、存在する形（化学式）で答えよ。<br>(2) 操作2の反応を化学反応式で表せ。<br>(3) 水層 I からアニリンを取り出す方法を答えよ。<br>(4) 操作2と操作3の順序を逆にすると、どのような不都合が生じるか。",
  "a": r"(1) I：$\mathrm{C_6H_5NH_3Cl}$、II：$\mathrm{C_6H_5COONa}$、III：$\mathrm{C_6H_5ONa}$、IV：$\mathrm{C_6H_5CH_3}$　(2) $\mathrm{C_6H_5COOH + NaHCO_3 \to C_6H_5COONa + H_2O + CO_2}$　(3) 水酸化ナトリウム水溶液を加えてアニリンを遊離させ、エーテルを加えて抽出する。(4) 水酸化ナトリウム水溶液で安息香酸とフェノールがどちらも塩になって水層に移り、分離できない。",
  "s": r"有機化合物は塩（イオン）になると水層に、分子のままならエーテル層に入る。<br>操作1：塩基のアニリンだけが $\mathrm{C_6H_5NH_2 + HCl \to C_6H_5NH_3Cl}$ で塩になる。<br>操作2：炭酸より強い酸（安息香酸）だけが反応する。炭酸より弱いフェノールは反応しない。<br>操作3：フェノールが $\mathrm{C_6H_5OH + NaOH \to C_6H_5ONa + H_2O}$ で塩になる。中性のトルエンはエーテル層に残る。<br>(3) 水層 II・III からも同様に、塩酸を加えて安息香酸やフェノールを遊離させてエーテルで抽出できる。<br><b>ポイント</b>：分離の順序は「酸の強さの違い」を使う。弱い塩基（$\mathrm{NaHCO_3}$）でカルボン酸だけを取り出してから、強い塩基（$\mathrm{NaOH}$）でフェノールを取り出す。"},
 {"lv": "B", "tag": "サリチル酸",
  "q": r"サリチル酸（$o$-ヒドロキシ安息香酸）に、(a) 無水酢酸を作用させると化合物 A が、(b) メタノールと少量の濃硫酸を加えて加熱すると化合物 B が得られる。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$ とする。<br>(1) A、B の名称と示性式、および (a)、(b) の反応の名称を答えよ。<br>(2) サリチル酸・A・B のうち、(ア) 塩化鉄(III) 水溶液で呈色するもの、(イ) 炭酸水素ナトリウム水溶液と反応して気体を発生するもの、をそれぞれすべて選べ。<br>(3) サリチル酸 13.8 g から A が 15.3 g 得られた。収率は何 % か。<br>(4) サリチル酸は、ナトリウムフェノキシドに高温・高圧で二酸化炭素を反応させ、得られた塩に希硫酸を作用させてつくる。2つの反応を化学反応式で表せ。",
  "a": r"(1) A：アセチルサリチル酸 $\mathrm{C_6H_4(OCOCH_3)COOH}$、B：サリチル酸メチル $\mathrm{C_6H_4(OH)COOCH_3}$。(a) アセチル化、(b) エステル化　(2) (ア) サリチル酸、B　(イ) サリチル酸、A　(3) 85.0 %　(4) $\mathrm{C_6H_5ONa + CO_2 \to C_6H_4(OH)COONa}$、$\mathrm{2C_6H_4(OH)COONa + H_2SO_4 \to 2C_6H_4(OH)COOH + Na_2SO_4}$",
  "s": r"(1) (a) フェノール性の $\mathrm{-OH}$ がアセチル化される（解熱鎮痛剤）。(b) $\mathrm{-COOH}$ がエステル化される（消炎鎮痛剤の湿布薬）。<br>(2) (ア) フェノール性 $\mathrm{-OH}$ が残っているもの。A ではそれがエステルになっている。(イ) $\mathrm{-COOH}$ が残っているもの。B ではそれがエステルになっている。<br>(3) $\mathrm{C_7H_6O_3}=138$、$\mathrm{C_9H_8O_4}=180$。理論量 $\dfrac{13.8}{138}\times180=18.0\ \mathrm{g}$、収率 $\dfrac{15.3}{18.0}\times100=85.0$ %。<br><b>ポイント</b>：サリチル酸は $\mathrm{-OH}$ と $\mathrm{-COOH}$ の両方をもつ。どちらが反応したかで、塩化鉄(III)・炭酸水素ナトリウムへの反応が決まる。"},
 {"lv": "B", "tag": "ジアゾ化・カップリング",
  "q": r"アニリンを希塩酸に溶かし、氷冷しながら亜硝酸ナトリウム水溶液を加えると化合物 A が生じる。A の水溶液をナトリウムフェノキシドの水溶液に加えると、橙赤色の化合物 B（$p$-ヒドロキシアゾベンゼン）が生じる。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{N}=14$、$\mathrm{O}=16$ とする。<br>(1) A の名称を答え、A および B が生じる反応を化学反応式で表せ。また、それぞれの反応の名称を答えよ。<br>(2) A の水溶液を温めると気体が発生する。この反応を化学反応式で表し、A の反応を氷冷して行う理由を答えよ。<br>(3) アニリン 4.65 g から B をつくった。A を経た全体の収率が 80 % のとき、得られる B の質量を求めよ。",
  "a": r"(1) 塩化ベンゼンジアゾニウム。$\mathrm{C_6H_5NH_2 + 2HCl + NaNO_2 \to C_6H_5N_2Cl + NaCl + 2H_2O}$（ジアゾ化）、$\mathrm{C_6H_5N_2Cl + C_6H_5ONa \to C_6H_5{-}N{=}N{-}C_6H_4{-}OH + NaCl}$（ジアゾカップリング）　(2) $\mathrm{C_6H_5N_2Cl + H_2O \to C_6H_5OH + N_2 + HCl}$。A は温度が上がると分解してしまうから。(3) 7.92 g",
  "s": r"(1) B はアゾ基 $\mathrm{-N{=}N-}$ をもつアゾ化合物で、染料（アゾ染料）に用いられる。カップリングはフェノキシドのパラ位で起こる。<br>(2) 5 ℃ 程度より高いと、ジアゾニウム塩は水と反応して窒素を出しながらフェノールに変わる。<br>(3) アニリン $\mathrm{C_6H_7N}=93$ より $\dfrac{4.65}{93}=0.0500\ \mathrm{mol}$。B は $\mathrm{C_{12}H_{10}N_2O}=198$ で、$0.0500\times0.80\times198=7.92\ \mathrm{g}$。<br><b>ポイント</b>：ジアゾ化は「冷やして」、温めるとフェノールと $\mathrm{N_2}$。この対比が実験問題でよく問われる。"},
 {"lv": "B", "tag": "異性体と側鎖の酸化",
  "q": r"分子式 $\mathrm{C_8H_{10}}$ で表される芳香族炭化水素 A〜D がある。<br>・ベンゼン環の水素原子1個を塩素原子で置換した化合物は、A では1種類、B では2種類、C と D ではそれぞれ3種類ある。<br>・過マンガン酸カリウムで十分に酸化すると、D からは分子量 122 の化合物 E が、C からは化合物 F が得られた。<br>・B を酸化して得られる化合物 G を加熱すると、分子内で脱水して化合物 H が得られた。<br>$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$ とする。<br>(1) A〜D の名称を答えよ。<br>(2) E〜H の名称を答えよ。<br>(3) A を酸化して得られる化合物は、ある合成繊維の原料になる。その化合物と合成繊維の名称を答えよ。",
  "a": r"(1) A $p$-キシレン、B $o$-キシレン、C $m$-キシレン、D エチルベンゼン　(2) E 安息香酸、F イソフタル酸、G フタル酸、H 無水フタル酸　(3) テレフタル酸、ポリエチレンテレフタラート",
  "s": r"$\mathrm{C_8H_{10}}$ の芳香族炭化水素は、エチルベンゼンと $o$-、$m$-、$p$-キシレンの4種類。環の H を置換した化合物の数は、$p$-キシレン 1（環の H がすべて等価）、$o$-キシレン 2、$m$-キシレン 3、エチルベンゼン 3（$o$・$m$・$p$）。<br>側鎖の炭化水素基は長さによらず $\mathrm{-COOH}$ になる。エチルベンゼン → 安息香酸 $\mathrm{C_6H_5COOH}$（122）。$m$-キシレン → イソフタル酸。$o$-キシレン → フタル酸 → 加熱で無水フタル酸（隣り合う $\mathrm{-COOH}$ どうしが脱水）。<br>(3) テレフタル酸とエチレングリコールの縮合重合で PET が得られる。<br><b>ポイント</b>：置換体の数は「対称性で等価な位置」をまとめて数える。$\mathrm{KMnO_4}$ 酸化で、置換基の数と位置（$o$・$m$・$p$）がわかる。"},
 {"lv": "B", "tag": "正誤（芳香族化合物）",
  "q": r"芳香族化合物に関する次の記述①〜⑥のうち、誤りを含むものを2つ選べ。<br>① ベンゼン分子の炭素原子間の結合の長さは、すべて等しい。<br>② トルエンを過マンガン酸カリウムで酸化すると、安息香酸が得られる。<br>③ 酸の強さは、安息香酸 ＞ 炭酸 ＞ フェノール の順である。<br>④ アニリンは水によく溶け、その水溶液は強い塩基性を示す。<br>⑤ ニトロベンゼンは、水より密度が小さい淡黄色の液体である。<br>⑥ アセトアニリドは分子内にアミド結合をもつ。",
  "a": r"④、⑤",
  "s": r"① 正：単結合と二重結合の中間的な結合で、正六角形の平面分子。④ 誤：アニリンは水に少し溶けるだけで、塩基性は弱い（酸とは塩をつくる）。⑤ 誤：ニトロベンゼンは水より密度が大きく（約 1.2 $\mathrm{g/cm^3}$）、水に沈む。⑥ 正：$\mathrm{-NH{-}CO-}$ がアミド結合。<br><b>ポイント</b>：アニリンは「弱塩基・水に溶けにくい・酸に溶ける」。強塩基と混同しない。"},
 {"lv": "C", "tag": "構造決定（芳香族）",
  "q": r"分子式 $\mathrm{C_8H_{10}O}$ で表され、ベンゼン環をもつ化合物について答えよ。<br>(1) 構造異性体のうち、(a) ナトリウムと反応するが塩化鉄(III) 水溶液で呈色しないもの、(b) 塩化鉄(III) 水溶液で呈色するもの、(c) ナトリウムと反応しないもの、はそれぞれ何種類あるか。<br>(2) 化合物 A〜C は次の性質をもつ。A〜C の示性式（または構造の説明）と名称を答えよ。<br>　A：ナトリウムと反応するが、塩化鉄(III) 水溶液で呈色しない。ヨードホルム反応を示す。<br>　B：ナトリウムと反応するが、塩化鉄(III) 水溶液で呈色しない。穏やかに酸化するとアルデヒドが得られ、過マンガン酸カリウムで十分に酸化するとテレフタル酸が得られる。<br>　C：ナトリウムと反応しない。ベンゼン環の水素原子1個を臭素原子で置換した化合物は2種類ある。<br>(3) A に存在する立体異性体の種類を答えよ。<br>(4) A を分子内で脱水させて得られる化合物の名称と、それを付加重合させて得られる高分子化合物の名称を答えよ。",
  "a": r"(1) (a) 5種類　(b) 9種類　(c) 5種類　(2) A：$\mathrm{C_6H_5CH(OH)CH_3}$、1-フェニルエタノール　B：$p$-$\mathrm{CH_3C_6H_4CH_2OH}$、$p$-メチルベンジルアルコール　C：$p$-$\mathrm{CH_3C_6H_4OCH_3}$、$p$-メチルアニソール（4-メチルフェニルメチルエーテル）　(3) 鏡像異性体（1組）　(4) スチレン、ポリスチレン",
  "s": r"(1) ベンゼン環のほかに C 2個と O 1個。<br>(a) アルコール：置換基1つでは $\mathrm{-CH(OH)CH_3}$、$\mathrm{-CH_2CH_2OH}$ の2種類、置換基2つ（$\mathrm{-CH_3}$ と $\mathrm{-CH_2OH}$）で $o$・$m$・$p$ の3種類、計5種類。<br>(b) フェノール類：$\mathrm{-OH}$ と $\mathrm{-C_2H_5}$ で3種類、$\mathrm{-OH}$ と $\mathrm{-CH_3}$ 2個で6種類、計9種類（2つの $\mathrm{CH_3}$ を $o$・$m$・$p$ に置いてから、残りの位置に OH を置くと $2+3+1=6$）。<br>(c) エーテル：$\mathrm{-OC_2H_5}$、$\mathrm{-CH_2OCH_3}$、および $\mathrm{-OCH_3}$ と $\mathrm{-CH_3}$ の $o$・$m$・$p$ で、計5種類。総数は19種類。<br>(2) A：アルコールで $\mathrm{CH_3CH(OH)-}$ をもつのは 1-フェニルエタノールだけ。B：第一級アルコールで、パラ位に炭素の置換基を2つもつ。C：エーテル5種類のうち、環の H の種類が2種類なのは $p$-メチルアニソールだけ（エトキシベンゼンとベンジルメチルエーテルは3種類、$o$-・$m$-メチルアニソールは4種類）。<br>(3) A の $\mathrm{C^*H(OH)}$ は $\mathrm{C_6H_5}$、$\mathrm{CH_3}$、$\mathrm{OH}$、$\mathrm{H}$ が結合した不斉炭素原子。<br>(4) $\mathrm{C_6H_5CH(OH)CH_3 \to C_6H_5CH{=}CH_2 + H_2O}$。<br><b>ポイント</b>：芳香族の構造決定は「Na（−OH の有無）」「$\mathrm{FeCl_3}$（フェノール性か）」「酸化生成物（置換基の位置）」「置換体の数（対称性）」の4つの情報で絞り込む。"},
 {"lv": "C", "tag": "分配平衡と抽出",
  "q": r"安息香酸 HA は水とジエチルエーテルの両方に溶ける。水層では $\mathrm{HA \rightleftarrows H^+ + A^-}$（電離定数 $K_\mathrm{a}=6.4\times10^{-5}\ \mathrm{mol/L}$）が成り立ち、エーテル層には HA 分子だけが溶ける。また、両層の HA 分子の濃度の比 $\dfrac{[\mathrm{HA}]_\text{エーテル}}{[\mathrm{HA}]_\text{水}}=80$ は一定とする。<br>(1) 水層の pH が 2.0 に保たれているとき、水層の $\dfrac{[\mathrm{A^-}]}{[\mathrm{HA}]}$ を求めよ。<br>(2) 安息香酸を含む水溶液 100 mL（pH を 2.0 に保つ）を、エーテル 100 mL と振り混ぜた。安息香酸の何 % がエーテル層に移るか。有効数字2桁で答えよ。<br>(3) 水層の pH を 7.0、8.0 に保って (2) と同じ操作を行うと、それぞれ何 % がエーテル層に移るか。有効数字2桁で答えよ。<br>(4) トルエンと安息香酸を含むエーテル溶液に炭酸水素ナトリウム水溶液（pH 約 8）を加えて振り混ぜると、安息香酸を水層に移すことができる。その理由を (3) の結果をもとに説明せよ。<br>(5) pH 2.0 の条件で、エーテル 100 mL で1回抽出する場合と、エーテル 50 mL ずつで2回抽出する場合について、水層に残る安息香酸の割合をそれぞれ有効数字2桁で求めよ。",
  "a": r"(1) $6.4\times10^{-3}$　(2) 99 %　(3) pH 7.0：11 %、pH 8.0：1.2 %　(4) pH 8 では安息香酸のほとんどが $\mathrm{A^-}$ になり、エーテルに溶ける分子 HA が少ないので、大部分が水層にとどまるから。(5) 1回：1.2 %、2回：0.060 %",
  "s": r"(1) $\dfrac{[\mathrm{A^-}]}{[\mathrm{HA}]}=\dfrac{K_\mathrm{a}}{[\mathrm{H^+}]}=\dfrac{6.4\times10^{-5}}{1.0\times10^{-2}}=6.4\times10^{-3}$。<br>(2) 水層の安息香酸の全濃度は $[\mathrm{HA}]+[\mathrm{A^-}]=[\mathrm{HA}](1+6.4\times10^{-3})$。体積が等しいので、エーテル層：水層 ＝ $80:1.0064$。エーテル層の割合は $\dfrac{80}{81.0064}\times100=98.8\fallingdotseq99$ %。<br>(3) pH 7.0 では $\dfrac{K_\mathrm{a}}{[\mathrm{H^+}]}=640$ なので、エーテル層：水層 ＝ $80:641$、$\dfrac{80}{721}\times100=11$ %。pH 8.0 では $\dfrac{K_\mathrm{a}}{[\mathrm{H^+}]}=6400$、$\dfrac{80}{80+6401}\times100=1.2$ %。<br>(4) 塩基性にすると $\mathrm{HA}$ が $\mathrm{A^-}$（安息香酸イオン）になり、水層に残る。トルエンは電離しないのでエーテル層に残り、分離できる。<br>(5) 見かけの分配比 $D=\dfrac{80}{1.0064}=79.5$。1回（体積比 1）：水層に残る割合 $\dfrac{1}{1+79.5}=1.2\times10^{-2}$ → 1.2 %。2回（1回ごとの体積比 0.5）：$\left(\dfrac{1}{1+79.5\times0.5}\right)^2=(2.45\times10^{-2})^2=6.0\times10^{-4}$ → 0.060 %。<br><b>ポイント</b>：抽出のしやすさは「分子形の割合」で決まり、pH で調節できる。同じ量の溶媒なら、分けて何回も抽出した方が効率がよい。"},
]}}
strut(CH)


def verify():
    chk(CH)
    A = {"H": 1.0, "C": 12, "N": 14, "O": 16, "Na": 23, "S": 32, "Cl": 35.5, "Sn": 119}
    for e in ["C6H6 + HNO3 -> C6H5NO2 + H2O", "C6H6 + H2SO4 -> C6H5SO3H + H2O", "C6H6 + Cl2 -> C6H5Cl + HCl",
              "C6H6 + 3H2 -> C6H12", "C6H6 + 3Cl2 -> C6H6Cl6", "C6H5ONa + CO2 + H2O -> C6H5OH + NaHCO3",
              "C6H5OH + NaOH -> C6H5ONa + H2O", "C6H5OH + 3Br2 -> C6H2Br3OH + 3HBr",
              "2C6H5NO2 + 3Sn + 14HCl -> 2C6H5NH3Cl + 3SnCl4 + 4H2O", "C6H5NH3Cl + NaOH -> C6H5NH2 + NaCl + H2O",
              "C6H5NH2 + (CH3CO)2O -> C6H5NHCOCH3 + CH3COOH", "C6H5NH2 + HCl -> C6H5NH3Cl",
              "C6H5COOH + NaHCO3 -> C6H5COONa + H2O + CO2", "C6H5ONa + CO2 -> C6H4(OH)COONa",
              "2C6H4(OH)COONa + H2SO4 -> 2C6H4(OH)COOH + Na2SO4",
              "C6H4(OH)COOH + (CH3CO)2O -> C6H4(OCOCH3)COOH + CH3COOH",
              "C6H4(OH)COOH + CH3OH -> C6H4(OH)COOCH3 + H2O",
              "C6H5NH2 + 2HCl + NaNO2 -> C6H5N2Cl + NaCl + 2H2O", "C6H5N2Cl + C6H5ONa -> C6H5N2C6H4OH + NaCl",
              "C6H5N2Cl + H2O -> C6H5OH + N2 + HCl", "C6H4(COOH)2 -> C8H4O3 + H2O",
              "C6H5CH(OH)CH3 -> C6H5CHCH2 + H2O"]:
        eq(e)
    # A3
    m = isomers("C7H8O", arom=True); g = [groups(x) for x in m]
    assert len(m) == 5 and sum(1 for x in g if x["phenol"]) == 3
    assert [canon(x) for x, y in zip(m, g) if not (y["phenol"] or alcohol(y))] == [C("COc1ccccc1")]
    # A4
    th = 24.6 / mw("C6H5NO2", A) * mw("C6H7N", A); assert sf(th, 3) == 18.6 and sf(14.0 / 18.6 * 100, 3) == 75.3
    # B2
    sal, asp, mes = smi("OC(=O)c1ccccc1O"), smi("OC(=O)c1ccccc1OC(C)=O"), smi("COC(=O)c1ccccc1O")
    assert [bool(groups(x)["phenol"]) for x in (sal, asp, mes)] == [True, False, True]
    assert [bool(groups(x)["COOH"]) for x in (sal, asp, mes)] == [True, True, False]
    assert mw("C7H6O3", A) == 138 and mw("C9H8O4", A) == 180
    assert sf(13.8 / 138 * 180, 3) == 18.0 and sf(15.3 / 18.0 * 100, 3) == 85.0
    # B3
    assert mw("C6H7N", A) == 93 and mw("C12H10N2O", A) == 198 and sf(4.65 / 93 * 0.80 * 198, 3) == 7.92
    # B4
    c8 = isomers("C8H10", arom=True); assert len(c8) == 4
    ns = {canon(x): nsubst(x, ring=True) for x in c8}
    assert ns == {C("Cc1ccc(C)cc1"): 1, C("Cc1ccccc1C"): 2, C("Cc1cccc(C)c1"): 3, C("CCc1ccccc1"): 3}

    def oxid(x):  # 側鎖（炭素で結合）をすべて -COOH にした分子式
        k = sum(1 for e in ring_subs(x) if e == "C")
        return f"C{6 + k}H6O{2 * k}", [p for p, e in enumerate(ring_subs(x)) if e == "C"]
    oxs = {canon(x): oxid(x) for x in c8}
    assert [k for k, (f, _) in oxs.items() if mw(f, A) == 122] == [C("CCc1ccccc1")]
    pos = {k: (p[1] - p[0]) % 6 for k, (f, p) in oxs.items() if len(p) == 2}
    assert pos == {C("Cc1ccc(C)cc1"): 3, C("Cc1ccccc1C"): 1, C("Cc1cccc(C)c1"): 2}
    # C1
    m = isomers("C8H10O", arom=True); g = [groups(x) for x in m]
    na_nofe = [x for x, y in zip(m, g) if alcohol(y) and not y["phenol"]]
    phen = [x for x, y in zip(m, g) if y["phenol"]]; eth = [x for x, y in zip(m, g) if y["ether"]]
    assert (len(na_nofe), len(phen), len(eth), len(m)) == (5, 9, 5, 19)
    a_ = [x for x in na_nofe if iodoform(x)]; assert [canon(x) for x in a_] == [C("CC(O)c1ccccc1")] and asym(a_[0]) == 1
    b_ = [x for x in na_nofe if "alc1" in groups(x) and sorted(oxid(x)[1]) in ([0, 3], [1, 4], [2, 5])
          and oxid(x)[0] == "C8H6O4" and all(e in (None, "C") for e in ring_subs(x))]
    assert [canon(x) for x in b_] == [C("Cc1ccc(CO)cc1")]
    c_ = [x for x in eth if nsubst(x, ring=True, el="Br") == 2]; assert [canon(x) for x in c_] == [C("Cc1ccc(OC)cc1")]
    assert sorted(nsubst(x, ring=True, el="Br") for x in eth) == [2, 3, 3, 4, 4]
    # C2
    Ka, KD = 6.4e-5, 80
    r2 = Ka / 1.0e-2; assert sf(r2) == 6.4e-3 and sf(KD / (KD + 1 + r2) * 100) == 99
    r7 = Ka / 1.0e-7; assert sf(r7) == 640 and sf(KD / (KD + 1 + r7) * 100) == 11
    r8 = Ka / 1.0e-8; assert sf(r8) == 6400 and sf(KD / (KD + 1 + r8) * 100) == 1.2
    D = KD / (1 + r2); assert sf(D, 3) == 79.5
    assert sf(1 / (1 + D) * 100) == 1.2 and sf((1 / (1 + D * 0.5)) ** 2 * 100) == 0.060
