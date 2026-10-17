"""問題集 第11章 金属元素。CH に問題、verify() で反応式・工業的製法の量的関係・電解精錬の計算と、推定問題の解が一通りに決まることを検算する。"""
import re
from itertools import permutations, combinations

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


def _t(s):
    """SVG 用：'H_2S' の '_2' を下付きにする"""
    out, low = [], False
    for part in re.split(r"(_\d)", s):
        if part.startswith("_"):
            out.append(f'<tspan dy="3" font-size="8">{part[1]}</tspan>'); low = True
        elif part:
            out.append(f'<tspan dy="-3">{part}</tspan>' if low else part); low = False
    return "".join(out)


def fig_flow():
    """系統分析の流れ図（座標は計算で決める）"""
    ops = ["① 希塩酸を加える", "② H_2S を通じる", "③ 煮沸 → 希硝酸 → NH_3 水を過剰に", "④ H_2S を通じる", "⑤ (NH_4)_2CO_3 水溶液を加える"]
    W, bx, bw, bh, row, top = 440, 14, 150, 22, 62, 6
    cx = bx + bw / 2
    o = [f'<svg class="fig" width="{W}" height="{top + row * 5 + bh + 8}" viewBox="0 0 {W} {top + row * 5 + bh + 8}" '
         'xmlns="http://www.w3.org/2000/svg" font-size="11">',
         '<defs><marker id="ar11" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">'
         '<path d="M0,0 L8,4 L0,8 z" fill="#333"/></marker></defs>']
    labels = ["試料水溶液"] + ["ろ液"] * 5
    for k in range(6):
        y = top + row * k
        o.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="3" fill="#fff" stroke="#333"/>'
                 f'<text x="{cx}" y="{y + 15}" text-anchor="middle">{labels[k]}</text>')
        if k == 5:
            break
        y1, y2 = y + bh, y + row
        yb = y1 + 30
        o.append(f'<line x1="{cx}" y1="{y1}" x2="{cx}" y2="{y2 - 1}" stroke="#333" marker-end="url(#ar11)"/>')
        o.append(f'<text x="{cx + 8}" y="{y1 + 14}">{_t(ops[k])}</text>')
        o.append(f'<line x1="{cx}" y1="{yb}" x2="{W - 92}" y2="{yb}" stroke="#333" marker-end="url(#ar11)"/>')
        o.append(f'<rect x="{W - 88}" y="{yb - 11}" width="74" height="{bh}" rx="3" fill="#f3ecf8" stroke="#333"/>'
                 f'<text x="{W - 51}" y="{yb + 4}" text-anchor="middle">沈殿 {"ABCDE"[k]}</text>')
    o.append("</svg>")
    return "".join(o)


CH = {11: {
"goal": "金属イオンの反応（沈殿の色・錯イオン・炎色反応・両性）を系統的に整理し、系統分析と工業的製法（溶融塩電解・アンモニアソーダ法・接触法・オストワルト法・電解精錬）を反応式と量的関係で説明できるようにする。",
"items": [
 {"lv": "A", "tag": "沈殿の色",
  "q": r"次の (1)〜(7) の操作で生じる沈殿の化学式と色を答えよ。<br>(1) $\mathrm{Ag^+}$ を含む水溶液に希塩酸を加える。<br>(2) $\mathrm{Pb^{2+}}$ を含む水溶液にクロム酸カリウム水溶液を加える。<br>(3) $\mathrm{Cu^{2+}}$ を含む水溶液（酸性）に硫化水素を通じる。<br>(4) $\mathrm{Fe^{3+}}$ を含む水溶液に水酸化ナトリウム水溶液を加える。<br>(5) $\mathrm{Ba^{2+}}$ を含む水溶液に希硫酸を加える。<br>(6) $\mathrm{Zn^{2+}}$ を含む塩基性の水溶液に硫化水素を通じる。<br>(7) $\mathrm{Ag^+}$ を含む水溶液に少量の水酸化ナトリウム水溶液を加える。",
  "a": r"(1) $\mathrm{AgCl}$ 白　(2) $\mathrm{PbCrO_4}$ 黄　(3) $\mathrm{CuS}$ 黒　(4) $\mathrm{Fe(OH)_3}$（水酸化鉄(III)）赤褐　(5) $\mathrm{BaSO_4}$ 白　(6) $\mathrm{ZnS}$ 白　(7) $\mathrm{Ag_2O}$ 褐（暗褐）",
  "s": r"(7) $\mathrm{Ag^+}$ の水酸化物は不安定で、ただちに $\mathrm{2Ag^+ + 2OH^- \to Ag_2O + H_2O}$ となり酸化銀が沈殿する。(6) 硫化物は多くが黒色だが、$\mathrm{ZnS}$ は白色、$\mathrm{CdS}$ は黄色、$\mathrm{MnS}$ は淡赤色。(2) $\mathrm{PbCrO_4}$ の黄色、$\mathrm{Ag_2CrO_4}$ の赤褐色はよく出る。<br><b>ポイント</b>：沈殿は「陰イオン（$\mathrm{Cl^-}$・$\mathrm{SO_4^{2-}}$・$\mathrm{CrO_4^{2-}}$・$\mathrm{S^{2-}}$・$\mathrm{OH^-}$）ごと」に、沈殿する陽イオンと色を表にして覚える。"},
 {"lv": "A", "tag": "アルカリ金属・炎色反応",
  "q": r"(1) 次の元素の炎色反応の色を答えよ。$\mathrm{Na}$、$\mathrm{K}$、$\mathrm{Ca}$、$\mathrm{Ba}$、$\mathrm{Cu}$<br>(2) ナトリウムを石油（灯油）中に保存する理由を答えよ。また、ナトリウムと水の反応を化学反応式で表せ。<br>(3) 水酸化ナトリウムの固体を空気中に放置すると、表面がぬれ、やがて白い粉末が生じる。それぞれの現象の名称または変化を答えよ。",
  "a": r"(1) $\mathrm{Na}$ 黄、$\mathrm{K}$ 赤紫、$\mathrm{Ca}$ 橙赤、$\mathrm{Ba}$ 黄緑、$\mathrm{Cu}$ 青緑　(2) 空気中の酸素や水と反応するのを防ぐため。$\mathrm{2Na + 2H_2O \to 2NaOH + H_2}$　(3) 潮解（水蒸気を吸収して溶ける）、$\mathrm{CO_2}$ を吸収して炭酸ナトリウムになる。",
  "s": r"(1) ほかに $\mathrm{Li}$ 赤、$\mathrm{Sr}$ 紅（深赤）。$\mathrm{Mg}$ と $\mathrm{Be}$ は炎色反応を示さない。(2) アルカリ金属は還元力が強く、常温の水と激しく反応する。石油とは反応せず、石油より密度が大きいので沈んで空気から遮断される。(3) $\mathrm{2NaOH + CO_2 \to Na_2CO_3 + H_2O}$。<br><b>ポイント</b>：アルカリ金属は「1価の陽イオンになりやすい → 強い還元剤 → 石油中に保存」と、理由をつないで覚える。"},
 {"lv": "A", "tag": "錯イオン",
  "q": r"次の錯イオンについて、名称・配位数・形を答えよ。<br>(1) $\mathrm{[Ag(NH_3)_2]^+}$　(2) $\mathrm{[Cu(NH_3)_4]^{2+}}$　(3) $\mathrm{[Zn(NH_3)_4]^{2+}}$　(4) $\mathrm{[Fe(CN)_6]^{4-}}$<br>また、(2) の水溶液の色を答えよ。",
  "a": r"(1) ジアンミン銀(I)イオン、2、直線形　(2) テトラアンミン銅(II)イオン、4、正方形　(3) テトラアンミン亜鉛(II)イオン、4、正四面体形　(4) ヘキサシアニド鉄(II)酸イオン、6、正八面体形。(2) の水溶液は深青色。",
  "s": r"名称は「配位子の数（ジ・テトラ・ヘキサ）＋配位子名（アンミン・シアニド・ヒドロキシド）＋中心金属（酸化数）」。陰イオンの錯イオンは「〜酸イオン」とする。配位数2は直線形、4は正方形（$\mathrm{Cu^{2+}}$）または正四面体形（$\mathrm{Zn^{2+}}$）、6は正八面体形。(2) は $\mathrm{Cu^{2+}}$ を含む水溶液にアンモニア水を過剰に加えると生じる。<br><b>ポイント</b>：配位数4の形は $\mathrm{Cu^{2+}}$ が正方形、$\mathrm{Zn^{2+}}$ が正四面体形。入試で区別が問われる。"},
 {"lv": "A", "tag": "溶融塩電解",
  "q": r"アルミニウムは、融解した氷晶石 $\mathrm{Na_3AlF_6}$ に酸化アルミニウムを溶かし、炭素電極を用いて溶融塩電解することでつくられる。$\mathrm{Al}=27.0$、ファラデー定数を $9.65\times10^4\ \mathrm{C/mol}$ とする。<br>(1) 陰極で起こる反応を、電子 $\mathrm{e^-}$ を含むイオン反応式で表せ。<br>(2) $9.65\times10^4$ A の電流で 1.00 時間電気分解したとき、得られるアルミニウムの質量は何 kg か。<br>(3) 氷晶石を用いる理由を答えよ。<br>(4) アルミニウムを、塩化アルミニウムの水溶液の電気分解ではつくれない理由を答えよ。",
  "a": r"(1) $\mathrm{Al^{3+} + 3e^- \to Al}$　(2) 32.4 kg　(3) 酸化アルミニウムの融点（約 2000 ℃）を下げるため。(4) アルミニウムはイオン化傾向が大きく、水溶液では $\mathrm{Al^{3+}}$ ではなく水が還元されて水素が発生するから。",
  "s": r"(2) 電気量は $9.65\times10^4\times3600\ \mathrm{C}$、電子は $\dfrac{9.65\times10^4\times3600}{9.65\times10^4}=3600\ \mathrm{mol}$。$\mathrm{Al}$ は $\dfrac{3600}{3}=1200\ \mathrm{mol}$、$1200\times27.0=3.24\times10^4\ \mathrm{g}=32.4\ \mathrm{kg}$。<br>(3) 純粋な $\mathrm{Al_2O_3}$ の融点は非常に高く、融解に多量のエネルギーがいる。<br>陽極では $\mathrm{C + O^{2-} \to CO + 2e^-}$、$\mathrm{C + 2O^{2-} \to CO_2 + 4e^-}$ が起こり、炭素電極は消耗する。<br><b>ポイント</b>：$\mathrm{Li}$〜$\mathrm{Al}$（イオン化傾向の大きい金属）の単体は溶融塩電解でつくる。電子の物質量 → 金属の物質量は「価数で割る」。"},
 {"lv": "B", "tag": "工業的製法（アンモニアソーダ法）",
  "q": r"炭酸ナトリウムは、次の反応を組み合わせたアンモニアソーダ法（ソルベー法）で工業的に製造される。<br>① $\mathrm{NaCl + H_2O + NH_3 + CO_2 \to NaHCO_3 + NH_4Cl}$<br>② $\mathrm{2NaHCO_3 \to Na_2CO_3 + H_2O + CO_2}$<br>③ $\mathrm{CaCO_3 \to CaO + CO_2}$<br>④ $\mathrm{CaO + H_2O \to Ca(OH)_2}$<br>⑤ $\mathrm{Ca(OH)_2 + 2NH_4Cl \to CaCl_2 + 2H_2O + 2NH_3}$<br>$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、$\mathrm{Na}=23$、$\mathrm{Cl}=35.5$、$\mathrm{Ca}=40$ とする。<br>(1) ①〜⑤ をまとめて1つの化学反応式で表せ（$\mathrm{NH_3}$ と $\mathrm{CO_2}$ はすべて再利用されるものとする）。<br>(2) 炭酸ナトリウム 5.30 t を製造するのに必要な塩化ナトリウムと炭酸カルシウムの質量は、それぞれ何 t か。<br>(3) ① で $\mathrm{NaHCO_3}$ が沈殿として得られる理由と、$\mathrm{NH_3}$ を先に溶かしてから $\mathrm{CO_2}$ を通じる理由を答えよ。",
  "a": r"(1) $\mathrm{2NaCl + CaCO_3 \to Na_2CO_3 + CaCl_2}$　(2) $\mathrm{NaCl}$ 5.85 t、$\mathrm{CaCO_3}$ 5.00 t　(3) $\mathrm{NaHCO_3}$ は水への溶解度が比較的小さいから。$\mathrm{CO_2}$ は塩基性の水溶液によく溶けるから。",
  "s": r"(1) ①×2＋②＋③＋④＋⑤ をつくると、$\mathrm{NaHCO_3}$、$\mathrm{NH_4Cl}$、$\mathrm{CaO}$、$\mathrm{Ca(OH)_2}$、$\mathrm{NH_3}$、$\mathrm{CO_2}$、$\mathrm{H_2O}$ がすべて消える。<br>(2) $\mathrm{Na_2CO_3}=106$ より $\dfrac{5.30\times10^6}{106}=5.00\times10^4\ \mathrm{mol}$。$\mathrm{NaCl}$ はその2倍で $1.00\times10^5\times58.5=5.85\times10^6\ \mathrm{g}$、$\mathrm{CaCO_3}$ は同じ物質量で $5.00\times10^4\times100=5.00\times10^6\ \mathrm{g}$。<br>(3) ① の溶液中では $\mathrm{Na^+}$・$\mathrm{HCO_3^-}$・$\mathrm{NH_4^+}$・$\mathrm{Cl^-}$ のうち、溶けにくい $\mathrm{NaHCO_3}$ が析出する。$\mathrm{CO_2}$ は酸性酸化物なので、先にアンモニアで塩基性にしておくと多量に吸収される。<br><b>ポイント</b>：多段階の工業的製法は、中間生成物が消えるように係数をそろえて足し合わせ、全体の反応式で量的関係を計算する。"},
 {"lv": "B", "tag": "工業的製法（接触法・オストワルト法）",
  "q": r"$\mathrm{H}=1.0$、$\mathrm{N}=14$、$\mathrm{O}=16$、$\mathrm{S}=32$ とする。<br>[I] 接触法では、硫黄を燃焼させて $\mathrm{SO_2}$ とし、触媒を用いて $\mathrm{SO_3}$ に酸化したのち、$\mathrm{SO_3}$ を濃硫酸に吸収させて発煙硫酸とし、これを希硫酸で薄めて濃硫酸にする。<br>(1) $\mathrm{SO_2}$ を $\mathrm{SO_3}$ にする反応の化学反応式と、用いる触媒の化学式を答えよ。<br>(2) $\mathrm{SO_3}$ を直接水に吸収させない理由を答えよ。<br>(3) 硫黄 1.60 t からつくられる 98.0 % 硫酸は何 t か（硫黄はすべて硫酸になるものとする）。<br>[II] オストワルト法では、次の反応で硝酸をつくる。<br>　① $\mathrm{4NH_3 + 5O_2 \to 4NO + 6H_2O}$（白金触媒）　② $\mathrm{2NO + O_2 \to 2NO_2}$　③ $\mathrm{3NO_2 + H_2O \to 2HNO_3 + NO}$<br>(4) ③ で生じる $\mathrm{NO}$ はすべて ② で再利用されるとして、全体を1つの化学反応式で表せ。<br>(5) 63.0 % 硝酸 1.00 t をつくるのに必要なアンモニアは何 kg か。",
  "a": r"(1) $\mathrm{2SO_2 + O_2 \to 2SO_3}$、$\mathrm{V_2O_5}$　(2) $\mathrm{SO_3}$ と水の反応は発熱が激しく、硫酸の霧が生じて吸収しにくいから。(3) 5.00 t　(4) $\mathrm{NH_3 + 2O_2 \to HNO_3 + H_2O}$　(5) 170 kg",
  "s": r"(3) S 1 mol から $\mathrm{H_2SO_4}$ 1 mol。$\dfrac{1.60\times10^6}{32}=5.00\times10^4\ \mathrm{mol}$、$\mathrm{H_2SO_4}$ は $5.00\times10^4\times98=4.90\times10^6\ \mathrm{g}$。98.0 % 硫酸は $\dfrac{4.90\times10^6}{0.980}=5.00\times10^6\ \mathrm{g}=5.00\ \mathrm{t}$。<br>(4) ①＋②×3＋③×2 で $\mathrm{NO}$ と $\mathrm{NO_2}$ を消すと $\mathrm{4NH_3 + 8O_2 \to 4HNO_3 + 4H_2O}$、4で割る。<br>(5) $\mathrm{HNO_3}$ は $\dfrac{1.00\times10^6\times0.630}{63}=1.00\times10^4\ \mathrm{mol}$。$\mathrm{NH_3}$ も $1.00\times10^4\ \mathrm{mol}$ で、$1.70\times10^5\ \mathrm{g}=170\ \mathrm{kg}$。N の酸化数は $\mathrm{NH_3}$ −3 → $\mathrm{NO}$ +2 → $\mathrm{NO_2}$ +4 → $\mathrm{HNO_3}$ +5。<br><b>ポイント</b>：「原料の元素が最終的にすべて製品に入る」ときは、元素の物質量の保存だけで計算できる（S → $\mathrm{H_2SO_4}$、N → $\mathrm{HNO_3}$）。"},
 {"lv": "B", "tag": "系統分析",
  "q": r"$\mathrm{Ag^+}$、$\mathrm{Cu^{2+}}$、$\mathrm{Fe^{3+}}$、$\mathrm{Zn^{2+}}$、$\mathrm{Ca^{2+}}$ を含む硝酸塩の水溶液について、図の操作①〜⑤を順に行い、沈殿 A〜E をろ過で分離した。" + fig_flow() +
       r"(1) 沈殿 A〜E の化学式と色を答えよ。<br>(2) 操作②で $\mathrm{Zn^{2+}}$ が沈殿しない理由を答えよ。<br>(3) 操作③で、煮沸する理由と希硝酸を加える理由をそれぞれ答えよ。<br>(4) 操作③で $\mathrm{Zn^{2+}}$ が沈殿しないのはなぜか。イオン反応式を用いて説明せよ。",
  "a": r"(1) A $\mathrm{AgCl}$ 白、B $\mathrm{CuS}$ 黒、C $\mathrm{Fe(OH)_3}$ 赤褐、D $\mathrm{ZnS}$ 白、E $\mathrm{CaCO_3}$ 白　(2) 酸性では $[\mathrm{S^{2-}}]$ が小さく、$\mathrm{ZnS}$ の溶解度積に達しないから。(3) 煮沸：$\mathrm{H_2S}$ を追い出すため（残ると塩基性にしたとき $\mathrm{ZnS}$ が沈殿してしまう）。希硝酸：$\mathrm{H_2S}$ で還元された $\mathrm{Fe^{2+}}$ を $\mathrm{Fe^{3+}}$ に戻すため。(4) $\mathrm{Zn(OH)_2 + 4NH_3 \to [Zn(NH_3)_4]^{2+} + 2OH^-}$ により錯イオンとなって溶けるから。",
  "s": r"② では $\mathrm{2Fe^{3+} + H_2S \to 2Fe^{2+} + S + 2H^+}$ も起こり、沈殿 B には少量の硫黄が混じる。③ の後のろ液は $\mathrm{[Zn(NH_3)_4]^{2+}}$ を含む塩基性の溶液で、④ で $\mathrm{H_2S}$ を通じると $[\mathrm{S^{2-}}]$ が大きくなり $\mathrm{ZnS}$ が沈殿する。$\mathrm{Ca^{2+}}$ は塩化物・硫化物・水酸化物（アンモニア水程度の塩基性）では沈殿せず、最後に炭酸塩として沈殿する。<br><b>ポイント</b>：系統分析は「$\mathrm{Cl^-}$ → 酸性で $\mathrm{H_2S}$ → $\mathrm{NH_3}$ 水 → 塩基性で $\mathrm{H_2S}$ → $\mathrm{CO_3^{2-}}$」の順。各操作の「前処理（煮沸・酸化）」の理由が頻出。"},
 {"lv": "B", "tag": "正誤（遷移元素）",
  "q": r"遷移元素とその化合物、および工業的製法に関する次の記述①〜⑥のうち、誤りを含むものを2つ選べ。<br>① クロム酸カリウム水溶液に硫酸を加えると、黄色から赤橙色に変わる。このときクロムの酸化数は +6 から +3 に変化する。<br>② 硫酸酸性の二クロム酸カリウム水溶液は強い酸化剤で、還元されると $\mathrm{Cr^{3+}}$ を含む緑色の溶液になる。<br>③ 過マンガン酸カリウム水溶液は赤紫色で、硫酸酸性で還元剤と反応すると、ほぼ無色の $\mathrm{Mn^{2+}}$ を生じる。<br>④ $\mathrm{Fe^{2+}}$ を含む水溶液にヘキサシアニド鉄(III)酸カリウム水溶液を加えると、濃青色の沈殿が生じる。<br>⑤ $\mathrm{Fe^{3+}}$ を含む水溶液にチオシアン酸カリウム水溶液を加えると、濃青色の沈殿が生じる。<br>⑥ ハーバー・ボッシュ法では、四酸化三鉄を主成分とする触媒を用い、高温・高圧で窒素と水素からアンモニアを合成する。",
  "a": r"①、⑤",
  "s": r"① 誤：$\mathrm{2CrO_4^{2-} + 2H^+ \rightleftarrows Cr_2O_7^{2-} + H_2O}$ は酸化還元反応ではなく、Cr の酸化数は +6 のまま。② 正：$\mathrm{Cr_2O_7^{2-} + 14H^+ + 6e^- \to 2Cr^{3+} + 7H_2O}$。③ 正：$\mathrm{MnO_4^- + 8H^+ + 5e^- \to Mn^{2+} + 4H_2O}$。④ 正：$\mathrm{Fe^{3+}}$ にヘキサシアニド鉄(II)酸カリウムを加えたときも濃青色沈殿が生じる。⑤ 誤：沈殿ではなく血赤色の溶液になる。⑥ 正：$\mathrm{N_2 + 3H_2 \rightleftarrows 2NH_3}$ は発熱反応で、低温ほど平衡は右に移るが反応が遅いため、触媒を用いて高温（約 500 ℃）・高圧で行う。<br><b>ポイント</b>：$\mathrm{Fe^{2+}}$ と $\mathrm{Fe^{3+}}$ の検出は「シアニド鉄酸イオンの価数がイオンと逆の組合せで濃青色沈殿」「$\mathrm{SCN^-}$ は $\mathrm{Fe^{3+}}$ だけ血赤色」。"},
 {"lv": "B", "tag": "金属の推定",
  "q": r"金属 A〜F は、$\mathrm{Na}$、$\mathrm{Al}$、$\mathrm{Zn}$、$\mathrm{Fe}$、$\mathrm{Cu}$、$\mathrm{Ag}$ のいずれかである。<br>(a) A は常温の水と激しく反応して水素を発生する。<br>(b) B、C、D は希塩酸に溶けて水素を発生するが、E、F は希塩酸に溶けない。<br>(c) B と C は水酸化ナトリウム水溶液にも溶けて水素を発生するが、D は溶けない。<br>(d) B を希塩酸に溶かした溶液にアンモニア水を加えていくと白色沈殿が生じ、さらに加えると沈殿は溶けた。C で同じ操作をすると、白色沈殿は溶けなかった。<br>(e) E と F をそれぞれ希硝酸に溶かし、塩酸を加えると、F の溶液だけに白色沈殿が生じた。<br>(1) A〜F の元素記号を答えよ。<br>(2) C と水酸化ナトリウム水溶液の反応を化学反応式で表せ。<br>(3) D を濃硝酸に入れても、ほとんど溶けない。この状態を何というか。",
  "a": r"(1) A $\mathrm{Na}$、B $\mathrm{Zn}$、C $\mathrm{Al}$、D $\mathrm{Fe}$、E $\mathrm{Cu}$、F $\mathrm{Ag}$　(2) $\mathrm{2Al + 2NaOH + 6H_2O \to 2Na[Al(OH)_4] + 3H_2}$　(3) 不動態",
  "s": r"(b) イオン化傾向が $\mathrm{H_2}$ より小さい $\mathrm{Cu}$・$\mathrm{Ag}$ が E・F。(c) 両性金属 $\mathrm{Al}$・$\mathrm{Zn}$ が B・C で、D は $\mathrm{Fe}$。(d) 過剰のアンモニア水に溶けるのは $\mathrm{Zn(OH)_2}$（$\mathrm{[Zn(NH_3)_4]^{2+}}$ になる）で、$\mathrm{Al(OH)_3}$ は溶けない。よって B が $\mathrm{Zn}$、C が $\mathrm{Al}$。(e) $\mathrm{AgCl}$ の白色沈殿が生じる F が $\mathrm{Ag}$。$\mathrm{Zn}$ と $\mathrm{NaOH}$ の反応は $\mathrm{Zn + 2NaOH + 2H_2O \to Na_2[Zn(OH)_4] + H_2}$。<br><b>ポイント</b>：両性金属（$\mathrm{Al}$・$\mathrm{Zn}$・$\mathrm{Sn}$・$\mathrm{Pb}$）のうち $\mathrm{Al}$ と $\mathrm{Zn}$ の区別は「過剰のアンモニア水に溶けるか」。"},
 {"lv": "C", "tag": "電解精錬",
  "q": r"不純物として鉄と銀を含む粗銅を陽極、純銅を陰極とし、硫酸酸性の硫酸銅(II) 水溶液を 2.00 A の電流で 9650 秒間電気分解した。その結果、陰極の質量は 6.40 g 増加し、陽極の質量は 6.42 g 減少した。また、陽極の下に陽極泥が 0.10 g たまった。陽極では銅と鉄だけが酸化されて溶け出し、銀はすべて陽極泥になったものとする。$\mathrm{Fe}=56$、$\mathrm{Cu}=64$、ファラデー定数を $9.65\times10^4\ \mathrm{C/mol}$ とする。<br>(1) 流れた電子の物質量を求め、陰極で析出した銅の質量が 6.40 g であることを確かめよ。<br>(2) 陽極で溶け出した銅と鉄の物質量をそれぞれ求めよ。<br>(3) 電気分解の前後で、水溶液中の $\mathrm{Cu^{2+}}$ の物質量は何 mol 減少したか。<br>(4) 溶けた部分の粗銅に含まれていた銀の質量の割合は何 % か。<br>(5) 鉄が陰極に析出せず、銀が陽極で溶け出さない理由を、イオン化傾向を用いて説明せよ。",
  "a": r"(1) 0.200 mol　(2) 銅 0.0900 mol、鉄 0.0100 mol　(3) 0.0100 mol　(4) 1.6 %　(5) 鉄は銅よりイオン化傾向が大きく、$\mathrm{Fe^{2+}}$ は $\mathrm{Cu^{2+}}$ より還元されにくいので水溶液中に残る。銀は銅よりイオン化傾向が小さく酸化されにくいので、陽極の銅が溶けると単体のまま落ちる。",
  "s": r"(1) $\dfrac{2.00\times9650}{9.65\times10^4}=0.200\ \mathrm{mol}$。陰極 $\mathrm{Cu^{2+} + 2e^- \to Cu}$ より $\mathrm{Cu}$ は 0.100 mol、$0.100\times64=6.40\ \mathrm{g}$ で一致する。<br>(2) 溶け出した金属の質量は $6.42-0.10=6.32\ \mathrm{g}$。銅 $x$ mol、鉄 $y$ mol とすると、どちらも2価なので $x+y=0.100$、質量から $64x+56y=6.32$。解いて $x=0.0900$、$y=0.0100$。<br>(3) 陰極で 0.100 mol 析出し、陽極から 0.0900 mol 溶け出したので、$\mathrm{Cu^{2+}}$ は 0.0100 mol 減る（代わりに $\mathrm{Fe^{2+}}$ が 0.0100 mol 増える）。<br>(4) $\dfrac{0.10}{6.42}\times100=1.6$ %。<br><b>ポイント</b>：電解精錬では「陽極の減少量 ＝ 溶けた金属 ＋ 陽極泥」「陰極の増加量 ＝ 銅だけ」。電子の物質量と質量の2式を連立する。"},
 {"lv": "C", "tag": "未知試料の推定",
  "q": r"水溶液 X には、$\mathrm{Ag^+}$、$\mathrm{Pb^{2+}}$、$\mathrm{Cu^{2+}}$、$\mathrm{Fe^{3+}}$、$\mathrm{Al^{3+}}$、$\mathrm{Zn^{2+}}$、$\mathrm{Ca^{2+}}$、$\mathrm{Ba^{2+}}$ のうち3種類の陽イオンが含まれている。X について次の実験を行った。<br>実験1：X に希塩酸を加えても、沈殿は生じなかった。<br>実験2：X にアンモニア水を少量加えると白色沈殿が生じた。さらにアンモニア水を過剰に加えると、沈殿の一部は溶けたが白色沈殿 P が残り、溶液は無色であった。<br>実験3：P をろ過して取り出し、水酸化ナトリウム水溶液を過剰に加えると、P はすべて溶けた。<br>実験4：実験2のろ液に硫化水素を通じると、白色沈殿 Q が生じた。<br>実験5：X の炎色反応は橙赤色であった。<br>(1) X に含まれる3種類の陽イオンを答えよ。<br>(2) P、Q の化学式を答えよ。<br>(3) 実験2で溶けた沈殿の変化と、実験3の変化をイオン反応式で表せ。<br>(4) 実験2でアンモニア水の代わりに水酸化ナトリウム水溶液を過剰に加えると、X に含まれる2種類のイオンを分離できない。その理由を述べよ。",
  "a": r"(1) $\mathrm{Al^{3+}}$、$\mathrm{Zn^{2+}}$、$\mathrm{Ca^{2+}}$　(2) P $\mathrm{Al(OH)_3}$、Q $\mathrm{ZnS}$　(3) $\mathrm{Zn(OH)_2 + 4NH_3 \to [Zn(NH_3)_4]^{2+} + 2OH^-}$、$\mathrm{Al(OH)_3 + OH^- \to [Al(OH)_4]^-}$　(4) $\mathrm{Al(OH)_3}$ も $\mathrm{Zn(OH)_2}$ も両性水酸化物で、過剰の水酸化ナトリウム水溶液にどちらも溶けるから。",
  "s": r"実験1：$\mathrm{Ag^+}$・$\mathrm{Pb^{2+}}$ はない（$\mathrm{AgCl}$・$\mathrm{PbCl_2}$ の白色沈殿が生じない）。<br>実験2：$\mathrm{Cu^{2+}}$ なら青白色の沈殿や深青色の溶液、$\mathrm{Fe^{3+}}$ なら赤褐色の沈殿になるので、どちらもない。白色の水酸化物になるのは $\mathrm{Al^{3+}}$ と $\mathrm{Zn^{2+}}$。過剰のアンモニア水に溶けずに残る白色沈殿 P は $\mathrm{Al(OH)_3}$（実験3で両性を確認）。一部が溶けたのは $\mathrm{Zn(OH)_2}$。<br>実験4：ろ液は塩基性なので $\mathrm{ZnS}$ の白色沈殿が生じ、$\mathrm{Zn^{2+}}$ の存在が確かめられる。<br>実験5：橙赤色は $\mathrm{Ca}$（$\mathrm{Ba}$ は黄緑色）。$\mathrm{Ca^{2+}}$ はアンモニア水では沈殿しないので、実験2の結果と矛盾しない。<br><b>ポイント</b>：推定問題は「ある」と言える根拠と「ない」と言える根拠を実験ごとに書き出す。3種類と指定されていれば、最後に個数を確認する。"},
]}}
strut(CH)


def verify():
    chk(CH)
    for e in ["Ag{+} + Cl{-} -> AgCl", "Pb{2+} + CrO4{2-} -> PbCrO4", "Cu{2+} + H2S -> CuS + 2H{+}",
              "Fe{3+} + 3OH{-} -> Fe(OH)3", "Ba{2+} + SO4{2-} -> BaSO4", "Zn{2+} + S{2-} -> ZnS",
              "2Ag{+} + 2OH{-} -> Ag2O + H2O", "2Na + 2H2O -> 2NaOH + H2", "2NaOH + CO2 -> Na2CO3 + H2O",
              "Al{3+} + 3e{-} -> Al", "C + O{2-} -> CO + 2e{-}", "C + 2O{2-} -> CO2 + 4e{-}",
              "2SO2 + O2 -> 2SO3", "S + O2 -> SO2", "SO3 + H2O -> H2SO4", "NH3 + 2O2 -> HNO3 + H2O",
              "2Fe{3+} + H2S -> 2Fe{2+} + S + 2H{+}", "Zn(OH)2 + 4NH3 -> [Zn(NH3)4]{2+} + 2OH{-}",
              "2CrO4{2-} + 2H{+} -> Cr2O7{2-} + H2O", "Cr2O7{2-} + 14H{+} + 6e{-} -> 2Cr{3+} + 7H2O",
              "MnO4{-} + 8H{+} + 5e{-} -> Mn{2+} + 4H2O", "N2 + 3H2 -> 2NH3",
              "2Al + 2NaOH + 6H2O -> 2Na[Al(OH)4] + 3H2", "Zn + 2NaOH + 2H2O -> Na2[Zn(OH)4] + H2",
              "Al(OH)3 + OH{-} -> [Al(OH)4]{-}", "Cu{2+} + 2e{-} -> Cu"]:
        eq(e)
    # 多段階の反応を足し合わせて全体の式になることの確認（化学種ごとに相殺）
    def net(steps):
        tot = Counter()
        for k, s in steps:
            l, r = s.split("->")
            for t in l.split(" + "):
                m = re.match(r"\s*(\d*)(\S+)", t); tot[m.group(2)] -= k * int(m.group(1) or 1)
            for t in r.split(" + "):
                m = re.match(r"\s*(\d*)(\S+)", t); tot[m.group(2)] += k * int(m.group(1) or 1)
        return {x: v for x, v in tot.items() if v}
    sol = [(2, "NaCl + H2O + NH3 + CO2 -> NaHCO3 + NH4Cl"), (1, "2NaHCO3 -> Na2CO3 + H2O + CO2"),
           (1, "CaCO3 -> CaO + CO2"), (1, "CaO + H2O -> Ca(OH)2"), (1, "Ca(OH)2 + 2NH4Cl -> CaCl2 + 2H2O + 2NH3")]
    for _, s in sol:
        eq(s)
    assert net(sol) == {"NaCl": -2, "CaCO3": -1, "Na2CO3": 1, "CaCl2": 1}
    ost = [(1, "4NH3 + 5O2 -> 4NO + 6H2O"), (3, "2NO + O2 -> 2NO2"), (2, "3NO2 + H2O -> 2HNO3 + NO")]
    for _, s in ost:
        eq(s)
    assert net(ost) == {"NH3": -4, "O2": -8, "HNO3": 4, "H2O": 4}
    A = {"H": 1.0, "C": 12, "N": 14, "O": 16, "Na": 23, "S": 32, "Cl": 35.5, "Ca": 40}
    # A4
    ne = 9.65e4 * 3600 / 9.65e4; assert ne == 3600 and sf(ne / 3 * 27.0 / 1000, 3) == 32.4
    # B1
    n = 5.30e6 / mw("Na2CO3", A); assert abs(n - 5.00e4) < 1e-6
    assert sf(2 * n * mw("NaCl", A) / 1e6, 3) == 5.85 and sf(n * mw("CaCO3", A) / 1e6, 3) == 5.00
    # B2
    s = 1.60e6 / 32; assert sf(s * mw("H2SO4", A) / 0.980 / 1e6, 3) == 5.00
    h = 1.00e6 * 0.630 / mw("HNO3", A); assert abs(h - 1.00e4) < 1e-6 and sf(h * mw("NH3", A) / 1000, 3) == 170
    # B5 金属の推定：条件を満たす割り当てが1通り
    P = {"Na": dict(w=1, hcl=1, naoh=1, nh3=0, agcl=0), "Al": dict(w=0, hcl=1, naoh=1, nh3=0, agcl=0),
         "Zn": dict(w=0, hcl=1, naoh=1, nh3=1, agcl=0), "Fe": dict(w=0, hcl=1, naoh=0, nh3=0, agcl=0),
         "Cu": dict(w=0, hcl=0, naoh=0, nh3=0, agcl=0), "Ag": dict(w=0, hcl=0, naoh=0, nh3=0, agcl=1)}
    sols = []
    for pm in permutations(P):
        a, b, c, d, e, f = (P[x] for x in pm)
        if (a["w"] and not any(x["w"] for x in (b, c, d, e, f)) and b["hcl"] and c["hcl"] and d["hcl"]
                and not e["hcl"] and not f["hcl"] and b["naoh"] and c["naoh"] and not d["naoh"]
                and b["nh3"] and not c["nh3"] and f["agcl"] and not e["agcl"]):
            sols.append(pm)
    assert sols == [("Na", "Zn", "Al", "Fe", "Cu", "Ag")]
    # C1
    ne = 2.00 * 9650 / 9.65e4; assert abs(ne - 0.200) < 1e-12 and sf(ne / 2 * 64, 3) == 6.40
    y = (0.100 * 64 - (6.42 - 0.10)) / (64 - 56); x = 0.100 - y
    assert sf(x, 3) == 0.0900 and sf(y, 3) == 0.0100 and sf(0.100 - x, 3) == 0.0100
    assert sf(0.10 / 6.42 * 100) == 1.6
    # C2 未知試料：3種類の組合せのうち実験結果と合うものは1通り
    ions = ["Ag", "Pb", "Cu", "Fe", "Al", "Zn", "Ca", "Ba"]
    hcl = {"Ag", "Pb"}
    small = {"Ag": "褐", "Pb": "白", "Cu": "青白", "Fe": "赤褐", "Al": "白", "Zn": "白"}   # 少量の NH3 水
    dissolve = {"Ag", "Cu", "Zn"}                       # 過剰の NH3 水で溶ける
    naoh_dis = {"Al", "Pb", "Zn"}                       # 両性
    h2s = {"Ag": "黒", "Cu": "黒", "Zn": "白"}            # 塩基性で H2S
    flame = {"Ca": "橙赤", "Ba": "黄緑", "Cu": "青緑"}
    ok = []
    for X in combinations(ions, 3):
        if set(X) & hcl:
            continue
        pp = [i for i in X if i in small]
        if not pp or {small[i] for i in pp} != {"白"}:
            continue
        P_ = [i for i in pp if i not in dissolve]; dis = [i for i in pp if i in dissolve]
        if not P_ or not dis or "Cu" in X:
            continue
        if not all(i in naoh_dis for i in P_):
            continue
        filt = [i for i in X if i not in P_]
        if {h2s[i] for i in filt if i in h2s} != {"白"}:
            continue
        if {flame[i] for i in X if i in flame} != {"橙赤"}:
            continue
        ok.append(X)
    assert ok == [("Al", "Zn", "Ca")]
