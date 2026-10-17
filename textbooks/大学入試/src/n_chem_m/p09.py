"""問題集 第9章 電離平衡。CH に問題、verify() で数値（pH・濃度・溶解度積）を Python で検算する。"""
from math import log10, sqrt

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

CH = {9: {
"goal": "電離定数・加水分解定数・溶解度積を、近似が使える条件とともに使いこなす。緩衝液の pH と沈殿の生成を、式を立てて判断できるようにする。",
"items": [
 {"lv": "A", "tag": "弱酸の pH",
  "q": r"25 ℃ で、0.10 $\mathrm{mol/L}$ の酢酸水溶液について次の問いに答えよ。ただし、酢酸の電離定数は $K_\mathrm{a}=2.7\times10^{-5}\ \mathrm{mol/L}$、$\log_{10}3=0.48$ とし、酢酸の電離度は1に比べて十分小さいものとする。<br>(1) 酢酸の電離度 $\alpha$ を求めよ。<br>(2) この水溶液の pH を小数第1位まで求めよ。",
  "a": r"(1) $1.6\times10^{-2}$　(2) 2.8",
  "s": r"(1) 濃度を $c$ とすると、$\mathrm{CH_3COOH \rightleftarrows CH_3COO^- + H^+}$ で $[\mathrm{CH_3COO^-}]=[\mathrm{H^+}]=c\alpha$、$[\mathrm{CH_3COOH}]=c(1-\alpha)$。$K_\mathrm{a}=\dfrac{c\alpha^2}{1-\alpha}\fallingdotseq c\alpha^2$ より $\alpha=\sqrt{\dfrac{K_\mathrm{a}}{c}}=\sqrt{2.7\times10^{-4}}=1.6\times10^{-2}$。1に比べて十分小さいので、近似は妥当。<br>(2) $[\mathrm{H^+}]=c\alpha=\sqrt{cK_\mathrm{a}}=\sqrt{2.7\times10^{-6}}$。$2.7\times10^{-6}=3^3\times10^{-7}$ なので $\mathrm{pH}=-\dfrac12\log_{10}(3^3\times10^{-7})=-\dfrac12(1.44-7)=2.78\fallingdotseq2.8$。<br><b>ポイント</b>：$\alpha\ll1$ のとき $\alpha=\sqrt{K_\mathrm{a}/c}$、$[\mathrm{H^+}]=\sqrt{cK_\mathrm{a}}$。平方根の対数は「係数 $\frac12$」で処理する。"},
 {"lv": "A", "tag": "弱塩基の pH",
  "q": r"25 ℃ で、0.050 $\mathrm{mol/L}$ のアンモニア水について、(1) アンモニアの電離度、(2) pH（小数第1位まで）を求めよ。ただし、アンモニアの電離定数は $K_\mathrm{b}=1.8\times10^{-5}\ \mathrm{mol/L}$、水のイオン積は $K_\mathrm{w}=1.0\times10^{-14}\ (\mathrm{mol/L})^2$、$\log_{10}3=0.48$ とし、電離度は1に比べて十分小さいものとする。",
  "a": r"(1) $1.9\times10^{-2}$　(2) 11.0",
  "s": r"$\mathrm{NH_3 + H_2O \rightleftarrows NH_4^+ + OH^-}$ で、$K_\mathrm{b}=\dfrac{[\mathrm{NH_4^+}][\mathrm{OH^-}]}{[\mathrm{NH_3}]}\fallingdotseq c\alpha^2$。<br>(1) $\alpha=\sqrt{K_\mathrm{b}/c}=\sqrt{3.6\times10^{-4}}=1.9\times10^{-2}$。<br>(2) $[\mathrm{OH^-}]=\sqrt{cK_\mathrm{b}}=\sqrt{9.0\times10^{-7}}$。$\mathrm{pOH}=-\dfrac12(\log_{10}9-7)=-\dfrac12(0.96-7)=3.02$、$\mathrm{pH}=14-3.02=10.98\fallingdotseq11.0$。<br><b>ポイント</b>：塩基は $[\mathrm{OH^-}]$ を先に求め、$\mathrm{pH}=14-\mathrm{pOH}$（25 ℃）で換算する。"},
 {"lv": "A", "tag": "溶解度積",
  "q": r"25 ℃ における塩化銀の溶解度積を $K_\mathrm{sp}=1.8\times10^{-10}\ (\mathrm{mol/L})^2$ とする。$\mathrm{AgCl}=143.5$、$\sqrt{1.8}=1.34$ として、次の問いに答えよ。<br>(1) 純水 1.0 L に溶ける塩化銀の物質量と質量を求めよ。<br>(2) 0.10 $\mathrm{mol/L}$ の塩化ナトリウム水溶液 1.0 L に溶ける塩化銀の物質量を求めよ。ただし、溶液の体積変化は無視する。",
  "a": r"(1) $1.3\times10^{-5}\ \mathrm{mol}$、$1.9\times10^{-3}\ \mathrm{g}$　(2) $1.8\times10^{-9}\ \mathrm{mol}$",
  "s": r"(1) 溶けた $\mathrm{AgCl}$ を $s\ (\mathrm{mol/L})$ とすると $[\mathrm{Ag^+}]=[\mathrm{Cl^-}]=s$、$s^2=1.8\times10^{-10}$ より $s=1.34\times10^{-5}\ \mathrm{mol/L}$。質量は $1.34\times10^{-5}\times143.5=1.9\times10^{-3}\ \mathrm{g}$。<br>(2) $[\mathrm{Cl^-}]\fallingdotseq0.10\ \mathrm{mol/L}$（溶けた $\mathrm{AgCl}$ による増加は無視できる）なので、$[\mathrm{Ag^+}]=\dfrac{1.8\times10^{-10}}{0.10}=1.8\times10^{-9}\ \mathrm{mol/L}$。これが溶けた $\mathrm{AgCl}$ の量で、純水のときの約1万分の1になる（共通イオン効果）。<br><b>ポイント</b>：溶解度積は温度だけで決まる一定値。共通イオンがあると、もう一方のイオンの濃度が小さく抑えられる。"},
 {"lv": "A", "tag": "塩の水溶液の性質",
  "q": r"次の塩の水溶液を、酸性・中性・塩基性に分類せよ。<br>(ア) $\mathrm{CH_3COONa}$　(イ) $\mathrm{NH_4Cl}$　(ウ) $\mathrm{NaCl}$　(エ) $\mathrm{Na_2CO_3}$　(オ) $\mathrm{NaHSO_4}$　(カ) $\mathrm{KNO_3}$　(キ) $\mathrm{NaHCO_3}$　(ク) $\mathrm{CuSO_4}$",
  "a": r"酸性：イ、オ、ク　中性：ウ、カ　塩基性：ア、エ、キ",
  "s": r"弱酸の陰イオンは $\mathrm{CH_3COO^- + H_2O \rightleftarrows CH_3COOH + OH^-}$ のように加水分解して塩基性（ア・エ・キ）。$\mathrm{NaHCO_3}$ は酸性塩だが、$\mathrm{HCO_3^-}$ の加水分解の方が電離より起こりやすく弱塩基性。弱塩基の陽イオンは $\mathrm{NH_4^+ \rightleftarrows NH_3 + H^+}$ で酸性（イ）。$\mathrm{Cu^{2+}}$ も水和水から $\mathrm{H^+}$ を出して弱酸性（ク）。$\mathrm{NaHSO_4}$ は $\mathrm{HSO_4^- \to H^+ + SO_4^{2-}}$ と電離して酸性（オ、加水分解ではない）。強酸と強塩基の正塩（ウ・カ）は中性。<br><b>ポイント</b>：「もとの酸・塩基の強弱」で判断する。酸性塩だから酸性、とは限らない（$\mathrm{NaHCO_3}$ は塩基性）。"},
 {"lv": "B", "tag": "緩衝液",
  "q": r"0.10 $\mathrm{mol/L}$ 酢酸水溶液 200 mL と 0.10 $\mathrm{mol/L}$ 酢酸ナトリウム水溶液 100 mL を混合した溶液 X がある。酢酸の電離定数を $K_\mathrm{a}=2.7\times10^{-5}\ \mathrm{mol/L}$、$\log_{10}2=0.30$、$\log_{10}3=0.48$、$K_\mathrm{w}=1.0\times10^{-14}\ (\mathrm{mol/L})^2$ とする。<br>(1) X の pH を小数第1位まで求めよ。<br>(2) X に固体の水酸化ナトリウム $2.0\times10^{-3}$ mol を加えて溶かした。pH を小数第1位まで求めよ。体積変化は無視する。<br>(3) 純水 300 mL に同じ量の水酸化ナトリウムを溶かしたときの pH を求め、(2) と比べて X の pH がほとんど変化しない理由を説明せよ。",
  "a": r"(1) 4.3　(2) 4.4　(3) 11.8。加えた $\mathrm{OH^-}$ が $\mathrm{CH_3COOH}$ と中和して消費され、$[\mathrm{CH_3COOH}]/[\mathrm{CH_3COO^-}]$ の比が少し変わるだけだから。",
  "s": r"緩衝液では $\mathrm{CH_3COOH}$ の電離も $\mathrm{CH_3COO^-}$ の加水分解もごくわずかなので、$[\mathrm{H^+}]=K_\mathrm{a}\times\dfrac{[\mathrm{CH_3COOH}]}{[\mathrm{CH_3COO^-}]}=K_\mathrm{a}\times\dfrac{n_\text{酸}}{n_\text{塩}}$（同じ溶液中なので物質量比でよい）。<br>(1) $n_\text{酸}=0.020\ \mathrm{mol}$、$n_\text{塩}=0.010\ \mathrm{mol}$。$[\mathrm{H^+}]=2.7\times10^{-5}\times2=5.4\times10^{-5}$。$\log_{10}5.4=\log_{10}(2\times3^3\div10)=0.30+1.44-1=0.74$ より $\mathrm{pH}=5-0.74=4.26\fallingdotseq4.3$。<br>(2) $\mathrm{CH_3COOH + OH^- \to CH_3COO^- + H_2O}$ で、酸 $0.018\ \mathrm{mol}$、塩 $0.012\ \mathrm{mol}$。$[\mathrm{H^+}]=2.7\times10^{-5}\times\dfrac{3}{2}=4.05\times10^{-5}$。$\log_{10}4.05=\log_{10}(3^4\div20)=1.92-1.30=0.62$ より $\mathrm{pH}=4.38\fallingdotseq4.4$。<br>(3) $[\mathrm{OH^-}]=\dfrac{2.0\times10^{-3}}{0.300}=\dfrac{2}{3}\times10^{-2}$。$\mathrm{pOH}=-(0.30-0.48-2)=2.18$、$\mathrm{pH}=11.82\fallingdotseq11.8$。純水では pH が約7から約12へ大きく変わるのに、X では 0.1 程度しか変わらない。<br><b>ポイント</b>：緩衝液の pH は「酸と塩の物質量比」で決まる。加えた酸・塩基は、まず緩衝成分との中和として処理する。"},
 {"lv": "B", "tag": "滴定曲線",
  "q": r"0.10 $\mathrm{mol/L}$ 酢酸水溶液 20.0 mL に、0.10 $\mathrm{mol/L}$ 水酸化ナトリウム水溶液を少しずつ加えて滴定した。$K_\mathrm{a}=2.7\times10^{-5}\ \mathrm{mol/L}$、$K_\mathrm{w}=1.0\times10^{-14}\ (\mathrm{mol/L})^2$、$\log_{10}2=0.30$、$\log_{10}3=0.48$ とする。<br>(1) 水酸化ナトリウム水溶液を 10.0 mL 加えたときの pH を小数第1位まで求めよ。<br>(2) 中和点（20.0 mL 加えたとき）の pH を小数第1位まで求めよ。<br>(3) この滴定の指示薬として、メチルオレンジ（変色域 pH 3.1〜4.4）とフェノールフタレイン（変色域 pH 8.0〜9.8）のどちらが適するか。理由とともに答えよ。",
  "a": r"(1) 4.6　(2) 8.6　(3) フェノールフタレイン。中和点が塩基性側（pH 約 8.6）にあり、その付近で pH が急変するから。",
  "s": r"(1) 半分だけ中和された点では $[\mathrm{CH_3COOH}]=[\mathrm{CH_3COO^-}]$ なので $[\mathrm{H^+}]=K_\mathrm{a}$。$\mathrm{pH}=-\log_{10}(2.7\times10^{-5})=5-(1.44-1)=4.56\fallingdotseq4.6$。<br>(2) 中和点では $\mathrm{CH_3COONa}$ の水溶液。$[\mathrm{CH_3COO^-}]=\dfrac{0.10\times0.0200}{0.0400}=0.050\ \mathrm{mol/L}$。加水分解 $\mathrm{CH_3COO^- + H_2O \rightleftarrows CH_3COOH + OH^-}$ の定数は $K_\mathrm{h}=\dfrac{[\mathrm{CH_3COOH}][\mathrm{OH^-}]}{[\mathrm{CH_3COO^-}]}=\dfrac{K_\mathrm{w}}{K_\mathrm{a}}$（分母分子に $[\mathrm{H^+}]$ をかけるとわかる）。$[\mathrm{OH^-}]=\sqrt{cK_\mathrm{w}/K_\mathrm{a}}$ だから<br>$\log_{10}[\mathrm{OH^-}]=\dfrac12\{(0.70-2)-14-(0.44-5)\}=\dfrac12(-10.74)=-5.37$（$\log_{10}5=1-0.30=0.70$）。$\mathrm{pOH}=5.37$、$\mathrm{pH}=8.63\fallingdotseq8.6$。<br>(3) メチルオレンジは pH 4 前後で変色し、これは (1) のあたりの緩衝領域なので、中和点よりはるかに手前で色が変わってしまう。<br><b>ポイント</b>：弱酸の滴定では「半中和点で pH = p$K_\mathrm{a}$」「中和点は塩の加水分解で塩基性」の2点をおさえれば、滴定曲線の形が描ける。"},
 {"lv": "B", "tag": "硫化物の沈殿",
  "q": r"$\mathrm{Cu^{2+}}$ と $\mathrm{Zn^{2+}}$ をそれぞれ 0.010 $\mathrm{mol/L}$ 含む水溶液に硫化水素を通じて飽和させた（$[\mathrm{H_2S}]=0.10\ \mathrm{mol/L}$）。硫化水素の2段階の電離をまとめた式 $\mathrm{H_2S \rightleftarrows 2H^+ + S^{2-}}$ の平衡定数を $K=1.2\times10^{-21}\ (\mathrm{mol/L})^2$、溶解度積を $\mathrm{CuS}$：$6.5\times10^{-30}\ (\mathrm{mol/L})^2$、$\mathrm{ZnS}$：$2.0\times10^{-18}\ (\mathrm{mol/L})^2$（この問題での値）、$\log_{10}2=0.30$、$\log_{10}3=0.48$ とする。<br>(1) pH 1.0 のときの $[\mathrm{S^{2-}}]$ を求めよ。<br>(2) pH 1.0 で沈殿するのはどちらか。また、そのとき溶液中に残る $[\mathrm{Cu^{2+}}]$ を求めよ。<br>(3) pH をいくらより大きくすると $\mathrm{ZnS}$ が沈殿し始めるか。小数第1位まで求めよ。",
  "a": r"(1) $1.2\times10^{-20}\ \mathrm{mol/L}$　(2) $\mathrm{CuS}$、$[\mathrm{Cu^{2+}}]=5.4\times10^{-10}\ \mathrm{mol/L}$　(3) 3.1",
  "s": r"(1) $[\mathrm{S^{2-}}]=\dfrac{K[\mathrm{H_2S}]}{[\mathrm{H^+}]^2}=\dfrac{1.2\times10^{-21}\times0.10}{(0.10)^2}=1.2\times10^{-20}\ \mathrm{mol/L}$。<br>(2) どちらも $[\mathrm{M^{2+}}][\mathrm{S^{2-}}]=0.010\times1.2\times10^{-20}=1.2\times10^{-22}$。$\mathrm{CuS}$ の $K_\mathrm{sp}$ より大きいので $\mathrm{CuS}$ は沈殿し、$\mathrm{ZnS}$ の $K_\mathrm{sp}$ より小さいので $\mathrm{ZnS}$ は沈殿しない。残る $[\mathrm{Cu^{2+}}]=\dfrac{6.5\times10^{-30}}{1.2\times10^{-20}}=5.4\times10^{-10}\ \mathrm{mol/L}$ で、ほぼ完全に沈殿している。<br>(3) 沈殿し始める条件は $[\mathrm{S^{2-}}]=\dfrac{2.0\times10^{-18}}{0.010}=2.0\times10^{-16}$。$[\mathrm{H^+}]^2=\dfrac{1.2\times10^{-22}}{2.0\times10^{-16}}=6.0\times10^{-7}$。$\mathrm{pH}=-\dfrac12\log_{10}(6.0\times10^{-7})=-\dfrac12(0.78-7)=3.11\fallingdotseq3.1$。<br><b>ポイント</b>：$[\mathrm{S^{2-}}]$ は $[\mathrm{H^+}]^2$ に反比例する。酸性では $\mathrm{S^{2-}}$ が少なく、溶解度積の小さい硫化物だけが沈殿する。これが系統分析で酸性と塩基性で $\mathrm{H_2S}$ を使い分ける理由。"},
 {"lv": "B", "tag": "正誤",
  "q": r"電離平衡に関する次の記述①〜⑤のうち、正しいものを2つ選べ。温度は一定とする。<br>① 酢酸水溶液を水で薄めると、酢酸の電離度は大きくなる。<br>② 酢酸水溶液に酢酸ナトリウムを加えると、酢酸の電離定数は小さくなる。<br>③ 塩化銀の飽和水溶液に塩化ナトリウムを加えても、塩化銀の溶解度積の値は変わらない。<br>④ 同じ濃度・同じ体積の塩酸と酢酸水溶液を中和するのに必要な水酸化ナトリウムの物質量は、塩酸の方が多い。<br>⑤ 緩衝液には、どれだけ多量の強酸を加えても、pH はほとんど変化しない。",
  "a": r"①、③",
  "s": r"① 正：$\alpha=\sqrt{K_\mathrm{a}/c}$ で、$c$ が小さいほど $\alpha$ は大きい（ルシャトリエの原理でも説明できる）。② 誤：電離定数は温度だけで決まる。共通イオン効果で小さくなるのは電離度。③ 正：溶解度積も温度だけで決まる。④ 誤：中和に必要な塩基の量は酸の物質量と価数で決まり、強弱には関係しない。⑤ 誤：加えた強酸の量が $\mathrm{CH_3COO^-}$ などの緩衝成分の量を超えると、pH は大きく下がる（緩衝能には限りがある）。<br><b>ポイント</b>：「定数（$K_\mathrm{a}$・$K_\mathrm{sp}$）は温度だけで決まる」「変わるのは電離度や溶解量」を区別する。"},
 {"lv": "B", "tag": "沈殿の判定と量",
  "q": r"$2.0\times10^{-4}\ \mathrm{mol/L}$ の硝酸銀水溶液 100 mL と、$1.0\times10^{-3}\ \mathrm{mol/L}$ の塩化ナトリウム水溶液 100 mL を混合した。$\mathrm{AgCl}$ の溶解度積を $1.8\times10^{-10}\ (\mathrm{mol/L})^2$、$\mathrm{AgCl}=143.5$ とする。<br>(1) 混合した直後（沈殿が生じる前）の $[\mathrm{Ag^+}][\mathrm{Cl^-}]$ を求め、沈殿が生じるかどうか判定せよ。<br>(2) 平衡に達したときの $[\mathrm{Ag^+}]$ を求めよ。<br>(3) 生じた塩化銀の質量を求めよ。",
  "a": r"(1) $5.0\times10^{-8}\ (\mathrm{mol/L})^2$、溶解度積より大きいので沈殿が生じる　(2) $4.5\times10^{-7}\ \mathrm{mol/L}$　(3) $2.9\times10^{-3}\ \mathrm{g}$",
  "s": r"(1) 混合で体積が2倍になるので $[\mathrm{Ag^+}]=1.0\times10^{-4}$、$[\mathrm{Cl^-}]=5.0\times10^{-4}\ \mathrm{mol/L}$。積は $5.0\times10^{-8}\gt1.8\times10^{-10}$。<br>(2) $\mathrm{Ag^+}$ はほとんど沈殿し、$\mathrm{Cl^-}$ は約 $5.0\times10^{-4}-1.0\times10^{-4}=4.0\times10^{-4}\ \mathrm{mol/L}$ 残る。$[\mathrm{Ag^+}]=\dfrac{1.8\times10^{-10}}{4.0\times10^{-4}}=4.5\times10^{-7}\ \mathrm{mol/L}$（はじめの 0.45 % で、「ほとんど沈殿」の仮定は妥当）。<br>(3) 沈殿した $\mathrm{Ag^+}$ は $(1.0\times10^{-4}-4.5\times10^{-7})\times0.200=1.99\times10^{-5}\ \mathrm{mol}$。<br>質量は $1.99\times10^{-5}\times143.5=2.9\times10^{-3}\ \mathrm{g}$。<br><b>ポイント</b>：沈殿の判定は「混合後の濃度」で積を計算して $K_\mathrm{sp}$ と比べる。体積が変わることを忘れない。"},
 {"lv": "C", "tag": "近似が使えない弱酸",
  "q": r"25 ℃ で、$1.0\times10^{-4}\ \mathrm{mol/L}$ の酢酸水溶液について考える。$K_\mathrm{a}=2.7\times10^{-5}\ \mathrm{mol/L}$、$\log_{10}2=0.30$、$\log_{10}3=0.48$、$\sqrt{1.15}=1.07$ とし、水の電離は無視する。<br>(1) 「電離度は1に比べて十分小さい」と仮定して電離度を求めよ。また、この仮定が成り立たないことを説明せよ。<br>(2) 近似を用いずに電離度を求めよ。<br>(3) この水溶液の pH を小数第1位まで求め、(1) の仮定で計算した pH と比べよ。<br>(4) 弱酸の水溶液を薄めていくと電離度が1に近づく理由を、平衡定数の式を用いて説明せよ。",
  "a": r"(1) 0.52。1に比べて小さくないので $1-\alpha\fallingdotseq1$ とできない。(2) 0.40　(3) 4.4（近似では 4.3）　(4) $\dfrac{\alpha^2}{1-\alpha}=\dfrac{K_\mathrm{a}}{c}$ で、$c$ が小さくなると右辺が大きくなり、左辺も大きくなるには $\alpha$ が1に近づく必要があるから。",
  "s": r"(1) $\alpha=\sqrt{K_\mathrm{a}/c}=\sqrt{0.27}=0.52$。0.5 程度の値は「1に比べて十分小さい」とはいえない。<br>(2) $K_\mathrm{a}=\dfrac{c\alpha^2}{1-\alpha}$ を変形して $\alpha^2+\dfrac{K_\mathrm{a}}{c}\alpha-\dfrac{K_\mathrm{a}}{c}=0$、$\dfrac{K_\mathrm{a}}{c}=0.27$。<br>$\alpha=\dfrac{-0.27+\sqrt{0.27^2+4\times0.27}}{2}=\dfrac{-0.27+\sqrt{1.1529}}{2}=\dfrac{-0.27+1.07}{2}=0.40$。<br>(3) $[\mathrm{H^+}]=c\alpha=4.0\times10^{-5}$、$\mathrm{pH}=5-2\log_{10}2=4.40\fallingdotseq4.4$。近似では $[\mathrm{H^+}]=\sqrt{2.7\times10^{-9}}=\sqrt{27}\times10^{-5}$、$\mathrm{pH}=5-\frac32\times0.48=4.28\fallingdotseq4.3$ で、0.1 ずれる。なお $[\mathrm{H^+}]=4.0\times10^{-5}$ は水の電離による $10^{-7}$ 程度より十分大きく、水の電離の無視は妥当。<br>(4) $\dfrac{\alpha^2}{1-\alpha}$ は $\alpha$ が1に近づくほど限りなく大きくなる増加関数である。<br><b>ポイント</b>：近似 $\alpha=\sqrt{K_\mathrm{a}/c}$ は、求めた $\alpha$ が 0.05 程度以下のときに使う。近似の結果が大きいときは二次方程式に戻る。"},
 {"lv": "C", "tag": "沈殿滴定（モール法）",
  "q": r"塩化物イオンを含む試料水溶液 10.0 mL に指示薬としてクロム酸カリウム水溶液を少量加え、$5.00\times10^{-2}\ \mathrm{mol/L}$ の硝酸銀水溶液で滴定した。はじめ白色沈殿が生じ、12.0 mL 加えたところで赤褐色の沈殿が生じ始めたので、ここを終点とした。$\mathrm{AgCl}$ の溶解度積を $1.8\times10^{-10}\ (\mathrm{mol/L})^2$、$\mathrm{Ag_2CrO_4}$ の溶解度積を $3.6\times10^{-12}\ (\mathrm{mol/L})^3$、終点での $[\mathrm{CrO_4^{2-}}]$ を $4.0\times10^{-3}\ \mathrm{mol/L}$ とし、指示薬による体積変化は無視する。<br>(1) 試料中の $[\mathrm{Cl^-}]$ を求めよ。<br>(2) 終点での $[\mathrm{Ag^+}]$ と $[\mathrm{Cl^-}]$ を求めよ。<br>(3) 終点で溶液中に残っている $\mathrm{Cl^-}$ の物質量は、はじめの何 % か。<br>(4) この滴定を強い酸性の溶液や強い塩基性の溶液で行うと正しい結果が得られない。それぞれの理由を述べよ。",
  "a": r"(1) $6.00\times10^{-2}\ \mathrm{mol/L}$　(2) $[\mathrm{Ag^+}]=3.0\times10^{-5}\ \mathrm{mol/L}$、$[\mathrm{Cl^-}]=6.0\times10^{-6}\ \mathrm{mol/L}$　(3) 0.022 %　(4) 酸性：$\mathrm{CrO_4^{2-}}$ が $\mathrm{Cr_2O_7^{2-}}$ に変わって減り、$\mathrm{Ag_2CrO_4}$ の沈殿が遅れる。塩基性：$\mathrm{Ag^+}$ が $\mathrm{Ag_2O}$ として沈殿し、硝酸銀が余分に消費される。",
  "s": r"(1) $\mathrm{Ag^+ + Cl^- \to AgCl}$ より $[\mathrm{Cl^-}]=\dfrac{5.00\times10^{-2}\times12.0}{10.0}=6.00\times10^{-2}\ \mathrm{mol/L}$。<br>(2) はじめに $\mathrm{AgCl}$ が沈殿し始める $[\mathrm{Ag^+}]$ は $\dfrac{1.8\times10^{-10}}{6.00\times10^{-2}}=3.0\times10^{-9}$、$\mathrm{Ag_2CrO_4}$ は $\sqrt{\dfrac{3.6\times10^{-12}}{4.0\times10^{-3}}}=3.0\times10^{-5}\ \mathrm{mol/L}$ なので、先に $\mathrm{AgCl}$ が沈殿する。赤褐色の沈殿が生じ始める終点では $[\mathrm{Ag^+}]=\sqrt{9.0\times10^{-10}}=3.0\times10^{-5}\ \mathrm{mol/L}$、$[\mathrm{Cl^-}]=\dfrac{1.8\times10^{-10}}{3.0\times10^{-5}}=6.0\times10^{-6}\ \mathrm{mol/L}$。<br>(3) 終点の体積は 22.0 mL。残る $\mathrm{Cl^-}$ は $6.0\times10^{-6}\times0.0220=1.32\times10^{-7}\ \mathrm{mol}$、はじめは $6.00\times10^{-4}\ \mathrm{mol}$。$\dfrac{1.32\times10^{-7}}{6.00\times10^{-4}}\times100=0.022$ %。ほぼすべての $\mathrm{Cl^-}$ が沈殿した時点で終点になることがわかる。<br>(4) 酸性では $\mathrm{2CrO_4^{2-} + 2H^+ \rightleftarrows Cr_2O_7^{2-} + H_2O}$ の平衡が右へ移る。塩基性では $\mathrm{2Ag^+ + 2OH^- \to Ag_2O + H_2O}$。<br><b>ポイント</b>：2種類の沈殿が競合するときは、「それぞれが沈殿し始める $[\mathrm{Ag^+}]$」を比べて順番を決める。$\mathrm{Ag_2CrO_4}$ は $[\mathrm{Ag^+}]^2$ で効くことに注意。"},
]}}
strut(CH)


def verify():
    chk(CH)
    # A1
    Ka, c = 2.7e-5, 0.10
    assert sf(sqrt(Ka / c)) == 1.6e-2
    assert abs((3 * 0.48 - 7) / -2 - 2.78) < 1e-9 and sf(-log10(sqrt(c * Ka)), 2) == 2.8
    assert abs(2.7e-6 - 3 ** 3 * 1e-7) < 1e-18
    # A2
    Kb, c = 1.8e-5, 0.050
    assert sf(sqrt(Kb / c)) == 1.9e-2
    poh = -(0.96 - 7) / 2; assert abs(poh - 3.02) < 1e-9 and round(14 - poh, 1) == 11.0
    assert round(14 + log10(sqrt(c * Kb)), 1) == 11.0
    # A3
    s = sqrt(1.8e-10); assert sf(s) == 1.3e-5 and sf(1.34e-5 * 143.5) == 1.9e-3 and sf(1.8e-10 / 0.10) == 1.8e-9
    # B1
    Ka = 2.7e-5
    assert abs(0.30 + 1.44 - 1 - 0.74) < 1e-9 and round(5 - 0.74, 1) == 4.3 and round(-log10(Ka * 0.020 / 0.010), 1) == 4.3
    assert abs(4 * 0.48 - 1.30 - 0.62) < 1e-9 and round(5 - 0.62, 1) == 4.4
    assert round(-log10(Ka * 0.018 / 0.012), 1) == 4.4
    assert abs(-(0.30 - 0.48 - 2) - 2.18) < 1e-9 and round(14 + log10(2.0e-3 / 0.300), 1) == 11.8
    # B2
    assert round(-log10(2.7e-5), 2) == 4.57 and abs(5 - (1.44 - 1) - 4.56) < 1e-9   # 4.56〜4.57 → 4.6
    co = 0.10 * 0.0200 / 0.0400; assert abs(co - 0.050) < 1e-12
    assert abs(((0.70 - 2) - 14 - (0.44 - 5)) / 2 + 5.37) < 1e-9
    assert round(14 + log10(sqrt(co * 1.0e-14 / 2.7e-5)), 1) == 8.6
    # B3
    S = 1.2e-21 * 0.10 / 0.10 ** 2; assert sf(S) == 1.2e-20
    assert 0.010 * S > 6.5e-30 and 0.010 * S < 2.0e-18 and sf(6.5e-30 / S) == 5.4e-10
    h2 = 1.2e-21 * 0.10 / (2.0e-18 / 0.010); assert sf(h2) == 6.0e-7
    assert round(-log10(sqrt(h2)), 1) == 3.1 and abs(-(0.78 - 7) / 2 - 3.11) < 1e-9
    # B5
    ag, cl = 1.0e-4, 5.0e-4
    assert sf(ag * cl) == 5.0e-8 and ag * cl > 1.8e-10
    y = (-(cl - ag) + sqrt((cl - ag) ** 2 + 4 * 1.8e-10)) / 2   # 厳密解
    assert sf(y) == 4.5e-7 and sf(1.8e-10 / 4.0e-4) == 4.5e-7
    assert sf((ag - y) * 0.200, 3) == 1.99e-5 and sf((ag - y) * 0.200 * 143.5) == 2.9e-3
    # C1
    r = 2.7e-5 / 1.0e-4
    assert sf(sqrt(r)) == 0.52
    al = (-r + sqrt(r * r + 4 * r)) / 2; assert sf(al) == 0.40 and abs(r * r + 4 * r - 1.1529) < 1e-9
    assert abs(al ** 2 / (1 - al) - r) < 1e-12
    assert round(-log10(1.0e-4 * al), 1) == 4.4 and round(5 - 2 * 0.30, 2) == 4.40
    assert round(-log10(sqrt(2.7e-9)), 1) == 4.3 and abs(5 - 1.5 * 0.48 - 4.28) < 1e-9
    # C2
    assert sf(5.00e-2 * 12.0 / 10.0, 3) == 6.00e-2
    assert sf(1.8e-10 / 6.00e-2) == 3.0e-9
    agE = sqrt(3.6e-12 / 4.0e-3); assert sf(agE) == 3.0e-5 and sf(1.8e-10 / agE) == 6.0e-6
    left = 6.0e-6 * 0.0220; assert sf(left, 3) == 1.32e-7
    assert sf(left / 6.00e-4 * 100) == 0.022
    eq("2CrO4{2-} + 2H{+} -> Cr2O7{2-} + H2O"); eq("2Ag{+} + 2OH{-} -> Ag2O + H2O")
