"""問題集 第10章 非金属元素。CH に問題、verify() で反応式のつり合い・量的関係・気体の推定の一意性を検算する。"""
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

CH = {10: {
"goal": "気体の製法・捕集法・乾燥剤を反応式とセットで整理する。ハロゲン・硫黄・窒素・ケイ素の化合物の性質を、酸化還元と量的関係まで含めて説明できるようにする。",
"items": [
 {"lv": "A", "tag": "気体の製法",
  "q": r"次の (1)〜(5) の操作で発生する気体の化学式と、その捕集法（水上置換・上方置換・下方置換）を答えよ。また、(1)〜(3) の反応を化学反応式で表せ。<br>(1) 塩化ナトリウムに濃硫酸を加えて加熱する。<br>(2) 塩化アンモニウムと水酸化カルシウムの混合物を加熱する。<br>(3) 銅に希硝酸を加える。<br>(4) 硫化鉄(II) に希硫酸を加える。<br>(5) 過酸化水素水に酸化マンガン(IV) を加える。",
  "a": r"(1) $\mathrm{HCl}$、下方置換　(2) $\mathrm{NH_3}$、上方置換　(3) $\mathrm{NO}$、水上置換　(4) $\mathrm{H_2S}$、下方置換　(5) $\mathrm{O_2}$、水上置換",
  "s": r"(1) $\mathrm{NaCl + H_2SO_4 \to NaHSO_4 + HCl}$（揮発性の酸の遊離）。(2) $\mathrm{2NH_4Cl + Ca(OH)_2 \to CaCl_2 + 2H_2O + 2NH_3}$（弱塩基の遊離）。(3) $\mathrm{3Cu + 8HNO_3 \to 3Cu(NO_3)_2 + 4H_2O + 2NO}$。(4) $\mathrm{FeS + H_2SO_4 \to FeSO_4 + H_2S}$（弱酸の遊離）。(5) $\mathrm{2H_2O_2 \to 2H_2O + O_2}$（$\mathrm{MnO_2}$ は触媒）。<br>水に溶けにくい気体（$\mathrm{NO}$・$\mathrm{O_2}$）は水上置換。水に溶ける気体は、空気（平均分子量 約29）より軽い $\mathrm{NH_3}$（17）が上方置換、重い $\mathrm{HCl}$（36.5）・$\mathrm{H_2S}$（34）が下方置換。<br><b>ポイント</b>：捕集法は「水に溶けるか」→「空気より重いか」の順に判断する。"},
 {"lv": "A", "tag": "正誤（ハロゲン）",
  "q": r"ハロゲンとその化合物に関する次の記述①〜⑥のうち、誤りを含むものをすべて選べ。<br>① フッ素は水と激しく反応して酸素を発生する。<br>② 臭化カリウム水溶液に塩素を通じると、臭素が遊離する。<br>③ ヨウ化カリウム水溶液に臭素水を加えても、変化は起こらない。<br>④ フッ化水素酸はガラスを溶かすので、ポリエチレンの容器に保存する。<br>⑤ ハロゲン化水素の水溶液は、いずれも強酸である。<br>⑥ フッ化銀は水に溶けにくい。",
  "a": r"③、⑤、⑥",
  "s": r"① 正：$\mathrm{2F_2 + 2H_2O \to 4HF + O_2}$。② 正：酸化力は $\mathrm{F_2 \gt Cl_2 \gt Br_2 \gt I_2}$ で、$\mathrm{2KBr + Cl_2 \to 2KCl + Br_2}$。③ 誤：$\mathrm{Br_2}$ の方が $\mathrm{I_2}$ より酸化力が強いので $\mathrm{2KI + Br_2 \to 2KBr + I_2}$ が起こり、溶液は褐色になる。④ 正：$\mathrm{SiO_2 + 6HF \to H_2SiF_6 + 2H_2O}$。⑤ 誤：フッ化水素酸は弱酸（$\mathrm{HF}$ 分子どうしの水素結合や $\mathrm{H{-}F}$ 結合の強さのため電離しにくい）。⑥ 誤：$\mathrm{AgCl}$・$\mathrm{AgBr}$・$\mathrm{AgI}$ は水に溶けにくいが、$\mathrm{AgF}$ はよく溶ける。<br><b>ポイント</b>：フッ素とその化合物は「例外」が多い（弱酸、ガラスを溶かす、銀塩が水に溶ける、沸点が高い）。"},
 {"lv": "A", "tag": "濃硫酸の性質",
  "q": r"次の (1)〜(4) の現象と最も関係の深い濃硫酸の性質を、下のア〜エから1つずつ選べ。また、(2) の反応を化学反応式で表せ。<br>(1) スクロースに濃硫酸をかけると黒くなる。<br>(2) 加熱した濃硫酸に銅を入れると、気体が発生して銅が溶ける。<br>(3) 塩化ナトリウムに濃硫酸を加えて加熱すると、塩化水素が発生する。<br>(4) 濃硫酸は、塩素などの気体の乾燥剤に用いられる。<br>ア 不揮発性　イ 吸湿性　ウ 脱水作用　エ 酸化作用",
  "a": r"(1) ウ　(2) エ、$\mathrm{Cu + 2H_2SO_4 \to CuSO_4 + SO_2 + 2H_2O}$　(3) ア　(4) イ",
  "s": r"(1) 有機化合物から H と O を水の形で奪う（$\mathrm{C_{12}H_{22}O_{11} \to 12C + 11H_2O}$）。(2) 熱濃硫酸は酸化力が強く、イオン化傾向が水素より小さい銅も溶かす。硫黄の酸化数は +6 から +4 に減少。(3) 沸点の高い（不揮発性の）酸が、揮発性の酸を追い出す。(4) 水分を吸収する性質。吸湿性は「空気中の水蒸気を吸う」、脱水作用は「化合物から H と O を奪う」と区別する。<br><b>ポイント</b>：希硫酸は強酸としてはたらくだけで、酸化作用・脱水作用・吸湿性は濃硫酸（熱濃硫酸）の性質。"},
 {"lv": "A", "tag": "乾燥剤",
  "q": r"気体の乾燥剤として、濃硫酸・塩化カルシウム・ソーダ石灰がよく用いられる。<br>(1) アンモニアの乾燥に用いることができるものはどれか。<br>(2) 濃硫酸を乾燥剤として用いることができない気体を、次から2つ選べ。<br>　$\mathrm{NH_3}$、$\mathrm{HCl}$、$\mathrm{Cl_2}$、$\mathrm{H_2S}$、$\mathrm{CO_2}$、$\mathrm{O_2}$<br>(3) (2) の気体のうち、ソーダ石灰を乾燥剤として用いることができないものをすべて選べ。",
  "a": r"(1) ソーダ石灰　(2) $\mathrm{NH_3}$、$\mathrm{H_2S}$　(3) $\mathrm{HCl}$、$\mathrm{Cl_2}$、$\mathrm{H_2S}$、$\mathrm{CO_2}$",
  "s": r"(1) 濃硫酸（酸性）とは中和し、塩化カルシウムとは $\mathrm{CaCl_2\cdot8NH_3}$ のような化合物をつくるので使えない。<br>(2) $\mathrm{NH_3}$ は塩基性で中和する。$\mathrm{H_2S}$ は還元性が強く、濃硫酸に酸化される。<br>(3) ソーダ石灰（$\mathrm{CaO}$ と $\mathrm{NaOH}$）は塩基性なので、酸性の気体（$\mathrm{HCl}$・$\mathrm{H_2S}$・$\mathrm{CO_2}$）や塩基と反応する $\mathrm{Cl_2}$ には使えない。$\mathrm{O_2}$ はどの乾燥剤でもよい。<br><b>ポイント</b>：乾燥剤は「酸性の気体には酸性・中性の乾燥剤、塩基性の気体には塩基性の乾燥剤」。例外は $\mathrm{NH_3}$ と $\mathrm{CaCl_2}$、$\mathrm{H_2S}$ と濃硫酸。"},
 {"lv": "B", "tag": "実験（塩素の製法）",
  "q": r"酸化マンガン(IV) に濃塩酸を加えて加熱し、発生した気体を洗気びん A（水）、洗気びん B（濃硫酸）の順に通してから捕集した。$\mathrm{Mn}=55$、$\mathrm{O}=16$、0 ℃、$1.013\times10^5\ \mathrm{Pa}$ における気体のモル体積を 22.4 L/mol とする。<br>(1) この反応の化学反応式を書け。<br>(2) 洗気びん A、B はそれぞれ何を取り除くためのものか。また、A と B の順序を逆にすると不都合な理由を述べよ。<br>(3) 適する捕集法を答えよ。<br>(4) 酸化マンガン(IV) 4.35 g が完全に反応したとき、発生する塩素の体積（0 ℃、$1.013\times10^5$ Pa）を求めよ。<br>(5) 反応した塩化水素のうち、還元剤としてはたらいたものの割合を求めよ。",
  "a": r"(1) $\mathrm{MnO_2 + 4HCl \to MnCl_2 + Cl_2 + 2H_2O}$　(2) A：塩化水素、B：水蒸気。逆にすると、乾燥させた後に水を通るので再び水蒸気を含んでしまう。(3) 下方置換　(4) 1.12 L　(5) $\frac12$",
  "s": r"(2) 濃塩酸から揮発した $\mathrm{HCl}$ は水によく溶けるので水で除き、最後に濃硫酸で乾燥させる。(3) $\mathrm{Cl_2}$ は水に溶け、空気より重い（分子量 71）。<br>(4) $\mathrm{MnO_2}=87$ より $\dfrac{4.35}{87}=0.0500\ \mathrm{mol}$。$\mathrm{Cl_2}$ も 0.0500 mol で、$0.0500\times22.4=1.12\ \mathrm{L}$。<br>(5) 4 mol の $\mathrm{HCl}$ のうち、$\mathrm{Cl_2}$ になる（酸化数 −1 → 0）のは 2 mol。残りの 2 mol は $\mathrm{MnCl_2}$ の $\mathrm{Cl^-}$ として残り、酸としてはたらいている。<br><b>ポイント</b>：洗気びんは「水 → 濃硫酸」の順。乾燥は必ず最後に行う。"},
 {"lv": "B", "tag": "逆滴定（二酸化硫黄）",
  "q": r"空気中の二酸化硫黄を定量するため、空気 10.0 L（0 ℃、$1.013\times10^5$ Pa に換算した体積）を、$1.00\times10^{-3}\ \mathrm{mol/L}$ のヨウ素水溶液 20.0 mL（ヨウ化カリウムを含む）に通じて、$\mathrm{SO_2}$ をすべて反応させた。<br>　$\mathrm{SO_2 + I_2 + 2H_2O \to H_2SO_4 + 2HI}$<br>残ったヨウ素を、デンプンを指示薬として $2.00\times10^{-3}\ \mathrm{mol/L}$ のチオ硫酸ナトリウム水溶液で滴定したところ、12.0 mL を要した。<br>　$\mathrm{I_2 + 2Na_2S_2O_3 \to 2NaI + Na_2S_4O_6}$<br>(1) 最初の反応で、$\mathrm{SO_2}$ は酸化剤・還元剤のどちらとしてはたらいたか。<br>(2) 空気 10.0 L に含まれていた $\mathrm{SO_2}$ の物質量を求めよ。<br>(3) 空気中の $\mathrm{SO_2}$ の体積の割合を求めよ（0 ℃、$1.013\times10^5$ Pa でのモル体積 22.4 L/mol）。<br>(4) $\mathrm{SO_2}$ が酸化剤としてはたらく反応の例を、化学反応式で1つ示せ。",
  "a": r"(1) 還元剤　(2) $8.00\times10^{-6}\ \mathrm{mol}$　(3) $1.79\times10^{-5}$（17.9 ppm）　(4) $\mathrm{SO_2 + 2H_2S \to 3S + 2H_2O}$",
  "s": r"(1) S の酸化数が +4 → +6 に増加している。<br>(2) はじめの $\mathrm{I_2}$：$1.00\times10^{-3}\times0.0200=2.00\times10^{-5}\ \mathrm{mol}$。残った $\mathrm{I_2}$：$\dfrac{2.00\times10^{-3}\times0.0120}{2}=1.20\times10^{-5}\ \mathrm{mol}$。$\mathrm{SO_2}$ と反応した $\mathrm{I_2}$ は $8.00\times10^{-6}$ mol で、$\mathrm{SO_2}$ も $8.00\times10^{-6}\ \mathrm{mol}$。<br>(3) $\dfrac{8.00\times10^{-6}\times22.4}{10.0}=1.79\times10^{-5}$。<br>(4) 相手が $\mathrm{H_2S}$ のような強い還元剤のときは、$\mathrm{SO_2}$ が酸化剤になる（S の酸化数 +4 → 0）。<br><b>ポイント</b>：逆滴定は「加えた全量 − 余った量 ＝ 反応した量」。チオ硫酸イオンとヨウ素は 2：1 で反応する。"},
 {"lv": "B", "tag": "計算（銅と硝酸）",
  "q": r"銅 1.92 g を、(a) 希硝酸、(b) 濃硝酸 とそれぞれ過不足なく反応させた。$\mathrm{Cu}=64$、0 ℃、$1.013\times10^5$ Pa における気体のモル体積を 22.4 L/mol とする。<br>(1) (a)、(b) の反応を化学反応式で表せ。<br>(2) (a)、(b) で発生する気体の体積（0 ℃、$1.013\times10^5$ Pa）をそれぞれ求めよ。<br>(3) (a)、(b) で反応した硝酸の物質量と、そのうち酸化剤としてはたらいた硝酸の割合をそれぞれ求めよ。<br>(4) 鉄やアルミニウムは希硝酸には溶けるが、濃硝酸にはほとんど溶けない。この理由を述べよ。",
  "a": r"(1) (a) $\mathrm{3Cu + 8HNO_3 \to 3Cu(NO_3)_2 + 4H_2O + 2NO}$　(b) $\mathrm{Cu + 4HNO_3 \to Cu(NO_3)_2 + 2H_2O + 2NO_2}$　(2) (a) 0.448 L　(b) 1.34 L　(3) (a) 0.0800 mol、$\frac14$　(b) 0.120 mol、$\frac12$　(4) 表面に緻密な酸化物の被膜ができ、内部が保護される（不動態）から。",
  "s": r"$\mathrm{Cu}$ は $\dfrac{1.92}{64}=0.0300\ \mathrm{mol}$。<br>(2) (a) $\mathrm{NO}$ は $0.0300\times\frac23=0.0200\ \mathrm{mol}$、$0.0200\times22.4=0.448\ \mathrm{L}$。(b) $\mathrm{NO_2}$ は $0.0600\ \mathrm{mol}$、$1.344\fallingdotseq1.34\ \mathrm{L}$。<br>(3) (a) $0.0300\times\frac83=0.0800\ \mathrm{mol}$。8 mol のうち $\mathrm{NO}$ になる（N の酸化数 +5 → +2）のは 2 mol。(b) $0.0300\times4=0.120\ \mathrm{mol}$。4 mol のうち $\mathrm{NO_2}$ になる（+5 → +4）のは 2 mol。残りは $\mathrm{Cu(NO_3)_2}$ の $\mathrm{NO_3^-}$ として残る。<br><b>ポイント</b>：反応式は半反応式（希硝酸 $\mathrm{HNO_3 + 3H^+ + 3e^- \to NO + 2H_2O}$、濃硝酸 $\mathrm{HNO_3 + H^+ + e^- \to NO_2 + H_2O}$）と $\mathrm{Cu \to Cu^{2+} + 2e^-}$ から組み立てると確実。"},
 {"lv": "B", "tag": "論述（ケイ素）",
  "q": r"(1) 二酸化炭素は常温で気体なのに、二酸化ケイ素は融点が約 1700 ℃ の固体である。この違いを、結晶の構造にふれて 60 字以内で説明せよ。<br>(2) 二酸化ケイ素からシリカゲルをつくる過程について、次の反応を化学反応式で表せ。<br>　① 二酸化ケイ素を水酸化ナトリウムとともに融解すると、ケイ酸ナトリウムが生じる。<br>　② ケイ酸ナトリウムの水溶液（水ガラス）に塩酸を加えると、ケイ酸が生じる。<br>(3) ケイ酸を加熱・乾燥して得られるシリカゲルが乾燥剤として用いられる理由を、50 字以内で説明せよ。",
  "a": r"(1) 解答例：二酸化炭素は分子間力で集まった分子結晶だが、二酸化ケイ素は原子が共有結合で立体的につながった共有結合の結晶だから。（57字／60字以内）　(2) ① $\mathrm{SiO_2 + 2NaOH \to Na_2SiO_3 + H_2O}$　② $\mathrm{Na_2SiO_3 + 2HCl \to H_2SiO_3 + 2NaCl}$　(3) 解答例：多孔質で表面積が大きく、表面のヒドロキシ基が水分子と水素結合して水を吸着するから。（41字／50字以内）",
  "s": r"(1) $\mathrm{CO_2}$ は分子（$\mathrm{O{=}C{=}O}$）の集まりで、融解・沸騰には弱い分子間力を切るだけでよい。$\mathrm{SiO_2}$ は Si 原子1個が4個の O 原子と、O 原子1個が2個の Si 原子と共有結合した巨大な立体網目で、融解には共有結合を切る必要がある。<br>(2) ① 酸性酸化物と塩基の反応。② 弱酸の塩に強酸を加えると弱酸が遊離する。<br>(3) シリカゲルは $\mathrm{Si{-}OH}$ を表面にもつ多孔質の固体。<br><b>ポイント</b>：同族でも、C は二重結合をつくって小さな分子になり、Si は単結合で網目をつくる。構造の違いが性質の違いを生む。"},
 {"lv": "B", "tag": "気体の推定",
  "q": r"次の A〜F は、$\mathrm{H_2}$、$\mathrm{O_2}$、$\mathrm{N_2}$、$\mathrm{Cl_2}$、$\mathrm{HCl}$、$\mathrm{NH_3}$、$\mathrm{H_2S}$、$\mathrm{NO}$、$\mathrm{NO_2}$、$\mathrm{CO}$、$\mathrm{CO_2}$、$\mathrm{SO_2}$ のいずれかである。<br>A：黄緑色で刺激臭があり、湿ったヨウ化カリウムデンプン紙を青紫色にする。<br>B：赤褐色で、水に溶けて強い酸性を示す。<br>C：無色で刺激臭があり、濃塩酸をつけたガラス棒を近づけると白煙を生じる。<br>D：無色で腐卵臭があり、酢酸鉛(II) 水溶液をしみこませたろ紙を黒くする。<br>E：無色・無臭で、石灰水に通じると白濁する。<br>F：無色で刺激臭があり、水溶液は弱い酸性を示す。また、D と反応して黄色の固体を生じる。<br>(1) A〜F の化学式を答えよ。<br>(2) C の白煙、および D と F の反応を、化学反応式で表せ。<br>(3) E を石灰水に通じ続けると、白濁が消える。この変化を化学反応式で表せ。",
  "a": r"(1) A $\mathrm{Cl_2}$　B $\mathrm{NO_2}$　C $\mathrm{NH_3}$　D $\mathrm{H_2S}$　E $\mathrm{CO_2}$　F $\mathrm{SO_2}$　(2) $\mathrm{NH_3 + HCl \to NH_4Cl}$、$\mathrm{SO_2 + 2H_2S \to 3S + 2H_2O}$　(3) $\mathrm{CaCO_3 + CO_2 + H_2O \to Ca(HCO_3)_2}$",
  "s": r"A：有色の気体は $\mathrm{Cl_2}$（黄緑）と $\mathrm{NO_2}$（赤褐）だけ。$\mathrm{Cl_2 + 2KI \to 2KCl + I_2}$ で、$\mathrm{I_2}$ がデンプンと反応する。B：$\mathrm{3NO_2 + H_2O \to 2HNO_3 + NO}$。C：塩基性の気体は $\mathrm{NH_3}$ だけ。D：$\mathrm{PbS}$（黒）が生じる。E：石灰水を白濁させるのは $\mathrm{CO_2}$ と $\mathrm{SO_2}$ だが、無臭なので $\mathrm{CO_2}$。F：刺激臭のある弱酸性の気体で、$\mathrm{H_2S}$ を酸化して硫黄を生じる。<br>(3) $\mathrm{Ca(OH)_2 + CO_2 \to CaCO_3 + H_2O}$ で白濁し、さらに $\mathrm{CO_2}$ を通じると水に溶ける炭酸水素カルシウムになる。<br><b>ポイント</b>：気体の推定は「色 → におい → 水溶液の液性 → 特有の反応」の順に候補をしぼる。"},
 {"lv": "C", "tag": "総合（オゾン）",
  "q": r"酸素 1.00 L に無声放電を行ったところ、酸素の一部がオゾンに変化し、気体の体積は同温・同圧で 0.940 L になった。気体の体積はすべて 0 ℃、$1.013\times10^5$ Pa で測定したものとし、このときの気体のモル体積を 22.4 L/mol とする。<br>(1) 生じたオゾンの体積を求めよ。<br>(2) 放電後の気体中のオゾンの体積百分率を求めよ。<br>(3) 放電後の気体をすべて中性のヨウ化カリウム水溶液に通じたところ、オゾンはすべて次のように反応した。<br>　$\mathrm{O_3 + 2KI + H_2O \to I_2 + O_2 + 2KOH}$<br>遊離したヨウ素を 0.100 $\mathrm{mol/L}$ のチオ硫酸ナトリウム水溶液で滴定すると、何 mL を要するか（$\mathrm{I_2 + 2Na_2S_2O_3 \to 2NaI + Na_2S_4O_6}$）。<br>(4) (3) で水溶液を通過して出てくる気体の体積は何 L か。気体の水への溶解と水蒸気は無視する。また、(3) の反応後の水溶液の液性を答えよ。",
  "a": r"(1) 0.120 L　(2) 12.8 %　(3) 107 mL　(4) 0.940 L（変化しない）、塩基性",
  "s": r"(1) $\mathrm{3O_2 \to 2O_3}$ では、体積 3 の $\mathrm{O_2}$ が体積 2 の $\mathrm{O_3}$ になり、体積は 1 減る。減少量 0.060 L から $\mathrm{O_3}$ は $0.060\times2=0.120\ \mathrm{L}$。<br>(2) $\dfrac{0.120}{0.940}\times100=12.8$ %。<br>(3) $\mathrm{O_3}$ は $\dfrac{0.120}{22.4}=5.36\times10^{-3}\ \mathrm{mol}$。$\mathrm{I_2}$ も同じ物質量で、チオ硫酸ナトリウムはその2倍の $1.071\times10^{-2}\ \mathrm{mol}$。体積は $\dfrac{1.071\times10^{-2}}{0.100}\ \mathrm{L}=107\ \mathrm{mL}$。<br>(4) $\mathrm{O_3}$ 1 分子が $\mathrm{O_2}$ 1 分子に置きかわるだけなので、気体の物質量は変わらず 0.940 L（すべて $\mathrm{O_2}$）。$\mathrm{KOH}$ が生じるので塩基性になる。<br><b>ポイント</b>：気体の体積変化の問題は、反応式の係数から「体積の増減」を直接読み取る。$\mathrm{O_3 \to I_2 \to 2S_2O_3^{2-}}$ の物質量の対応を一本の線でつなぐ。"},
 {"lv": "C", "tag": "実験考察（噴水実験）",
  "q": r"乾いた丸底フラスコ（内容積 498 mL）に、27 ℃、$1.0\times10^5$ Pa でアンモニアを満たし、ゴム栓にスポイト（水入り）とガラス管を取りつけた。ガラス管の先をフェノールフタレイン溶液を加えた水につけ、スポイトの水をフラスコ内に押し出したところ、水が勢いよく噴き上がり、フラスコ内は水で完全に満たされた。気体定数を $R=8.3\times10^3\ \mathrm{Pa\cdot L/(K\cdot mol)}$、27 ℃ におけるアンモニアの電離定数を $K_\mathrm{b}=1.8\times10^{-5}\ \mathrm{mol/L}$ とし、水の蒸気圧と水柱による圧力は無視する。<br>(1) 水が噴き上がる理由を 60 字以内で説明せよ。<br>(2) 噴き上がった水は何色になるか。<br>(3) フラスコ内にできたアンモニア水のモル濃度を求めよ。アンモニアはすべて溶けたものとする。<br>(4) (3) のアンモニア水におけるアンモニアの電離度を求めよ。<br>(5) フラスコを、アンモニアが体積で 75 % を占める空気との混合気体（27 ℃、$1.0\times10^5$ Pa）で満たして同じ実験を行うと、水はフラスコの内容積の何 % まで入るか。また、できたアンモニア水の濃度は (3) と比べてどうなるか。<br>(6) アンモニアの代わりに塩化水素を用い、水に BTB 溶液を加えて同じ実験を行った。噴き上がった水は何色になるか。",
  "a": r"(1) 解答例：スポイトの水にアンモニアが溶けてフラスコ内の圧力が下がり、外の水が大気圧に押されてフラスコ内に入るから。（52字／60字以内）　(2) 赤色　(3) $4.0\times10^{-2}\ \mathrm{mol/L}$　(4) $2.1\times10^{-2}$　(5) 75 %、変わらない　(6) 黄色",
  "s": r"(1) アンモニアは水への溶解度が非常に大きく、少量の水に多量に溶ける。入った水にさらに溶けるので、噴水は続く。<br>(2) アンモニア水は塩基性なので、フェノールフタレインが赤色を示す。<br>(3) $n=\dfrac{PV}{RT}=\dfrac{1.0\times10^5\times0.498}{8.3\times10^3\times300}=2.0\times10^{-2}\ \mathrm{mol}$。溶液の体積は 0.498 L なので $c=\dfrac{n}{V}=\dfrac{P}{RT}=4.0\times10^{-2}\ \mathrm{mol/L}$。<br>(4) $\alpha=\sqrt{\dfrac{K_\mathrm{b}}{c}}=\sqrt{\dfrac{1.8\times10^{-5}}{4.0\times10^{-2}}}=\sqrt{4.5\times10^{-4}}=2.1\times10^{-2}$（1に比べて十分小さい）。<br>(5) 空気は水にほとんど溶けずに残り、フラスコ内の圧力が外の圧力と等しくなるまで水が入る。空気の分圧ははじめ $0.25\times10^5$ Pa なので、$1.0\times10^5$ Pa では内容積の 25 % を占め、水は 75 % まで入る。アンモニアの物質量も水の体積も 0.75 倍になるので、濃度は $\dfrac{P_{\mathrm{NH_3}}}{RT}\div0.75=\dfrac{P}{RT}$ で変わらない。<br>(6) 塩酸は酸性なので、BTB は黄色を示す。<br><b>ポイント</b>：噴水実験に使えるのは「水に非常によく溶ける気体」（$\mathrm{NH_3}$、$\mathrm{HCl}$）。水が入る量は「溶けずに残る気体の体積」で決まる。"},
]}}
strut(CH)


def verify():
    chk(CH)
    for e in ["NaCl + H2SO4 -> NaHSO4 + HCl", "2NH4Cl + Ca(OH)2 -> CaCl2 + 2H2O + 2NH3",
              "3Cu + 8HNO3 -> 3Cu(NO3)2 + 4H2O + 2NO", "FeS + H2SO4 -> FeSO4 + H2S", "2H2O2 -> 2H2O + O2",
              "2F2 + 2H2O -> 4HF + O2", "2KBr + Cl2 -> 2KCl + Br2", "2KI + Br2 -> 2KBr + I2",
              "SiO2 + 6HF -> H2SiF6 + 2H2O", "Cu + 2H2SO4 -> CuSO4 + SO2 + 2H2O", "C12H22O11 -> 12C + 11H2O",
              "MnO2 + 4HCl -> MnCl2 + Cl2 + 2H2O", "SO2 + I2 + 2H2O -> H2SO4 + 2HI",
              "I2 + 2Na2S2O3 -> 2NaI + Na2S4O6", "SO2 + 2H2S -> 3S + 2H2O",
              "Cu + 4HNO3 -> Cu(NO3)2 + 2H2O + 2NO2", "HNO3 + 3H{+} + 3e{-} -> NO + 2H2O",
              "HNO3 + H{+} + e{-} -> NO2 + H2O", "SiO2 + 2NaOH -> Na2SiO3 + H2O",
              "Na2SiO3 + 2HCl -> H2SiO3 + 2NaCl", "NH3 + HCl -> NH4Cl", "CaCO3 + CO2 + H2O -> Ca(HCO3)2",
              "Ca(OH)2 + CO2 -> CaCO3 + H2O", "Cl2 + 2KI -> 2KCl + I2", "3NO2 + H2O -> 2HNO3 + NO",
              "3O2 -> 2O3", "O3 + 2KI + H2O -> I2 + O2 + 2KOH", "CaCl2 + 8NH3 -> CaCl2.8NH3"]:
        eq(e)
    A = {"H": 1.0, "N": 14, "O": 16, "Cl": 35.5, "S": 32, "Mn": 55, "Cu": 64}
    assert mw("NH3", A) < 29 < mw("HCl", A) and mw("H2S", A) > 29 and mw("Cl2", A) == 71
    # B1
    n = 4.35 / mw("MnO2", A); assert abs(n - 0.0500) < 1e-12 and sf(n * 22.4, 3) == 1.12
    # B2
    i0 = 1.00e-3 * 0.0200; il = 2.00e-3 * 0.0120 / 2
    so2 = i0 - il; assert sf(so2, 3) == 8.00e-6 and sf(so2 * 22.4 / 10.0, 3) == 1.79e-5
    # B3
    cu = 1.92 / 64
    assert sf(cu * 2 / 3 * 22.4, 3) == 0.448 and sf(cu * 2 * 22.4, 3) == 1.34
    assert sf(cu * 8 / 3, 3) == 0.0800 and sf(cu * 4, 3) == 0.120
    # B4 字数は chk で点検
    # B5 気体の推定が一通りに決まること
    G = {  # 色, におい, 水溶液（acid/base/none）, 特有の性質
        "H2": ("無", 0, "none", set()), "O2": ("無", 0, "none", set()), "N2": ("無", 0, "none", set()),
        "Cl2": ("黄緑", 1, "acid", {"KI"}), "HCl": ("無", 1, "strong", {"NH3smoke"}),
        "NH3": ("無", 1, "base", {"HClsmoke"}), "H2S": ("無", 1, "weak", {"PbS", "red"}),
        "NO": ("無", 0, "none", set()), "NO2": ("赤褐", 1, "strong", {"KI"}), "CO": ("無", 0, "none", set()),
        "CO2": ("無", 0, "weak", {"lime"}), "SO2": ("無", 1, "weak", {"lime", "ox_H2S", "red"})}
    clue = {"A": lambda g: g[0] == "黄緑" and "KI" in g[3], "B": lambda g: g[0] == "赤褐" and g[2] == "strong",
            "C": lambda g: g[1] and "HClsmoke" in g[3], "D": lambda g: g[1] and "PbS" in g[3],
            "E": lambda g: g[0] == "無" and not g[1] and "lime" in g[3],
            "F": lambda g: g[0] == "無" and g[1] and g[2] == "weak" and "ox_H2S" in g[3]}
    ans = {"A": "Cl2", "B": "NO2", "C": "NH3", "D": "H2S", "E": "CO2", "F": "SO2"}
    for k, f in clue.items():
        assert [x for x, g in G.items() if f(g)] == [ans[k]], k
    # C1
    o3 = 2 * (1.00 - 0.940); assert sf(o3, 3) == 0.120 and sf(o3 / 0.940 * 100, 3) == 12.8
    nt = o3 / 22.4 * 2; assert sf(nt / 0.100 * 1000, 3) == 107
    # C2
    n = 1.0e5 * 0.498 / (8.3e3 * 300); assert abs(n - 0.0200) < 1e-9
    c = n / 0.498; assert sf(c) == 4.0e-2 and sf(sqrt(1.8e-5 / c)) == 2.1e-2 and sf(sqrt(1.8e-5 / 4.0e-2)) == 2.1e-2
    n2 = 0.75 * n; v2 = 0.498 * (1 - 0.25); assert abs(n2 / v2 - c) < 1e-12
