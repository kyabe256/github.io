"""問題集 第1章 物質の構成と化学結合。CH に問題、verify() で数値・電子配置・形式を検算する。"""
import re
from math import log10, floor, sqrt, pi


# ---------- 図（座標は Python で計算） ----------
def _f(s):
    """'H2O' → 下付き数字つきの SVG テキスト"""
    out, low = [], False
    for ch in re.findall(r"\d+|\D+", s):
        if ch.isdigit():
            out.append(f'<tspan dy="3" font-size="8">{ch}</tspan>')
            low = True
        else:
            out.append(f'<tspan dy="-3">{ch}</tspan>' if low else ch)
            low = False
    return "".join(out)


def fig_bp():
    data = [("14族", "●", [("CH4", -161.5), ("SiH4", -112), ("GeH4", -88.5), ("SnH4", -52)]),
            ("15族", "▲", [("NH3", -33.3), ("PH3", -87.7), ("AsH3", -62.5), ("SbH3", -17)]),
            ("16族", "■", [("H2O", 100), ("H2S", -60.3), ("H2Se", -41.3), ("H2Te", -2.2)]),
            ("17族", "◆", [("HF", 19.5), ("HCl", -85.1), ("HBr", -66.8), ("HI", -35.4)])]
    W, H, x0, x1, y0, y1 = 400, 250, 52, 340, 12, 218
    X = lambda p: x0 + (p - 1.6) / 3.8 * (x1 - x0)
    Y = lambda t: y1 - (t + 180) / 300 * (y1 - y0)
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-size="10">',
         f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="#000"/>']
    for t in range(-150, 121, 50):
        o.append(f'<line x1="{x0}" y1="{Y(t):.1f}" x2="{x1}" y2="{Y(t):.1f}" stroke="#ddd"/>'
                 f'<text x="{x0-4}" y="{Y(t)+3:.1f}" text-anchor="end">{str(t).replace("-", "−")}</text>')
    # 右端（第5周期）のラベルは重ならないように 12px 以上離す
    ends = sorted([(Y(pts[-1][1]), pts[-1][0]) for _, _, pts in data])
    ly_end = {}
    prev = -1e9
    for y, nm in ends:
        prev = max(y, prev + 12)
        ly_end[nm] = prev
    for p in range(2, 6):
        o.append(f'<text x="{X(p):.1f}" y="{y1+13}" text-anchor="middle">{p}</text>')
    o.append(f'<text x="{(x0+x1)/2}" y="{H-4}" text-anchor="middle">周期</text>')
    o.append(f'<text x="12" y="{(y0+y1)/2}" transform="rotate(-90 12 {(y0+y1)/2})" text-anchor="middle">沸点〔℃〕</text>')
    for name, mk, pts in data:
        xy = [(X(p), Y(t)) for p, (_, t) in zip(range(2, 6), pts)]
        o.append('<polyline fill="none" stroke="#000" stroke-width="1.2" points="' +
                 " ".join(f"{x:.1f},{y:.1f}" for x, y in xy) + '"/>')
        for (x, y) in xy:
            o.append(f'<text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" font-size="11">{mk}</text>')
        fx, fy = xy[0]
        o.append(f'<text x="{fx-9:.1f}" y="{fy+4:.1f}" text-anchor="end">{_f(pts[0][0])}</text>')
        lx, ly = xy[-1]
        o.append(f'<text x="{lx+9:.1f}" y="{ly_end[pts[-1][0]]+4:.1f}">{_f(pts[-1][0])}</text>')
    o.append(f'<text x="{x1-4}" y="{y1-6}" text-anchor="end" font-size="9">●14族 ▲15族 ■16族 ◆17族</text>')
    o.append("</svg>")
    return "".join(o)


def cube_svg(atoms, bonds=(), kinds=None, note=""):
    """立方体の単位格子（斜投影）。atoms: [(x,y,z,種類)]、y が奥行き"""
    s, d, ox, oy = 110, 0.45, 26, 152
    P = lambda x, y, z: (ox + s * (x + d * 0.87 * y), oy - s * (z + d * 0.5 * y))
    W, H = 210, 172 + (14 if note else 0)
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-size="10">']
    cs = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
    for a in cs:
        for b in cs:
            if a < b and sum(abs(p - q) for p, q in zip(a, b)) == 1:
                (xa, ya), (xb, yb) = P(*a), P(*b)
                o.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#777"/>')
    for a, b in bonds:
        (xa, ya), (xb, yb) = P(*a), P(*b)
        o.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="#000" stroke-width="2"/>')
    for x, y, z, k in sorted(atoms, key=lambda t: (-t[1], t[2])):
        r, fill = kinds[k]
        X, Yp = P(x, y, z)
        o.append(f'<circle cx="{X:.1f}" cy="{Yp:.1f}" r="{r}" fill="{fill}" stroke="#000"/>')
    if note:
        o.append(f'<text x="{W/2}" y="{H-4}" text-anchor="middle">{note}</text>')
    o.append("</svg>")
    return "".join(o)


CORNERS = [(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)]
FACES = [(0.5, 0.5, 0), (0.5, 0.5, 1), (0.5, 0, 0.5), (0.5, 1, 0.5), (0, 0.5, 0.5), (1, 0.5, 0.5)]
K1 = {0: (8, "#e8e8e8")}
FIG_BCC = cube_svg([(*c, 0) for c in CORNERS] + [(0.5, 0.5, 0.5, 0)], kinds=K1, note="体心立方格子")
FIG_FCC = cube_svg([(*c, 0) for c in CORNERS + FACES], kinds=K1, note="面心立方格子")
_half = [(i / 2, j / 2, k / 2) for i in range(3) for j in range(3) for k in range(3)]
FIG_NACL = cube_svg([(*p, int(round(2 * sum(p))) % 2) for p in _half],
                    kinds={0: (8, "#ffffff"), 1: (4.5, "#555")}, note="○ Cl⁻　● Na⁺")
_tet = [(0.25, 0.25, 0.25), (0.75, 0.75, 0.25), (0.75, 0.25, 0.75), (0.25, 0.75, 0.75)]
_dbonds = [(t, p) for t in _tet for p in CORNERS + FACES
           if abs(sqrt(sum((a - b) ** 2 for a, b in zip(t, p))) - sqrt(3) / 4) < 1e-9]
FIG_DIA = cube_svg([(*c, 0) for c in CORNERS + FACES] + [(*t, 1) for t in _tet], bonds=_dbonds,
                   kinds={0: (6, "#ffffff"), 1: (6, "#888")}, note="ダイヤモンドの単位格子（●は内部の原子）")


CH = {1: {
"goal": "原子の構造・電子配置から周期表の傾向を説明し、結合の種類と物質の性質を結びつける。単位格子の計算（原子数・密度・半径・充填率）を確実に。",
"items": [
 {"lv": "A", "tag": "分離・精製",
  "q": r"次の (1)〜(5) の操作として最も適切なものを、下の語群から1つずつ選べ。<br>(1) 海水から純粋な水を得る。<br>(2) 原油からガソリン・灯油・軽油などを、沸点の違いによって分ける。<br>(3) ヨウ素と砂の混合物から、ヨウ素だけを取り出す。<br>(4) 少量の塩化ナトリウムを含む硝酸カリウムから、純粋な硝酸カリウムを得る。<br>(5) 茶葉に熱湯を注いで、香りやうま味の成分を溶かし出す。<br>語群：ろ過　蒸留　分留　昇華法　再結晶　抽出　クロマトグラフィー",
  "a": r"(1) 蒸留　(2) 分留　(3) 昇華法　(4) 再結晶　(5) 抽出",
  "s": r"(1) 加熱して出てきた水蒸気を冷却して集める。(2) 沸点の異なる液体の混合物を、温度範囲ごとに分けて取り出す蒸留を分留という。(3) ヨウ素は加熱すると固体から直接気体になる（昇華）。冷やした面に固体として集める。(4) 硝酸カリウムは温度による溶解度の変化が大きく、塩化ナトリウムは小さい。高温の水に溶かして冷却すると、硝酸カリウムだけが結晶として出てくる。(5) 目的の成分をよく溶かす溶媒で溶かし出す操作が抽出。ろ過（固体と液体を分ける）とクロマトグラフィー（吸着されやすさの違いで分ける）は、ここでは使わない。<br><b>ポイント</b>：「どの性質の違いを利用するか」（沸点・昇華性・溶解度の温度変化・溶媒への溶けやすさ）で操作を選ぶ。"},
 {"lv": "A", "tag": "原子の構造",
  "q": r"(1) $\mathrm{{}^{37}_{17}Cl}$ の陽子の数・中性子の数・電子の数を答えよ。<br>(2) $\mathrm{{}^{24}_{12}Mg^{2+}}$ の陽子の数・中性子の数・電子の数を答えよ。<br>(3) 天然の塩素は、$\mathrm{{}^{35}Cl}$（相対質量 34.97）が 75.8%、$\mathrm{{}^{37}Cl}$（相対質量 36.97）が 24.2% の割合で存在する。塩素の原子量を小数第1位まで求めよ。",
  "a": r"(1) 陽子 17、中性子 20、電子 17　(2) 陽子 12、中性子 12、電子 10　(3) 35.5",
  "s": r"質量数＝陽子の数＋中性子の数、原子番号＝陽子の数。(1) 中性子は $37-17=20$。原子は電気的に中性なので電子は 17。(2) 中性子は $24-12=12$。2価の陽イオンは電子を2個失っているので、電子は $12-2=10$。(3) 原子量は同位体の相対質量の平均：$34.97\times0.758+36.97\times0.242=26.51+8.95=35.46\fallingdotseq35.5$。<br><b>ポイント</b>：原子量は「同位体の相対質量 × 存在比」の和。イオンでは電子の数だけが変わり、陽子・中性子の数は変わらない。"},
 {"lv": "A", "tag": "電子配置",
  "q": r"(1) 次の原子・イオンの電子配置を、例にならって示せ。　例：$\mathrm{Na}$　K2 L8 M1<br>(ア) $\mathrm{O}$　(イ) $\mathrm{Al}$　(ウ) $\mathrm{S^{2-}}$　(エ) $\mathrm{K^+}$<br>(2) (ア)〜(エ) のうち、アルゴン原子と同じ電子配置をもつものをすべて選べ。<br>(3) $\mathrm{S^{2-}}$ と $\mathrm{K^+}$ では、どちらのイオン半径が大きいか。理由とともに答えよ。",
  "a": r"(1) (ア) K2 L6　(イ) K2 L8 M3　(ウ) K2 L8 M8　(エ) K2 L8 M8　(2) (ウ)、(エ)　(3) $\mathrm{S^{2-}}$（陽子の数が少なく、電子を引きつける力が弱いから）",
  "s": r"(ア) O は電子8個。(イ) Al は13個。(ウ) S は16個で、電子を2個受け取って18個。(エ) K は19個で、1個失って18個。(ウ)(エ) はどちらも18個で、Ar と同じ K2 L8 M8 になる。(3) 電子配置が同じイオンどうしでは、原子核の正電荷（陽子の数）が大きいほど電子を強く引きつけ、半径は小さくなる。陽子の数は S が16、K が19 なので、$\mathrm{S^{2-}}$ の方が大きい。<br><b>ポイント</b>：同じ電子配置のイオンの大きさは、陽子の数（原子番号）が小さいほど大きい。"},
 {"lv": "A", "tag": "結晶の分類",
  "q": r"次の物質 (ア)〜(オ) について、下の問いに答えよ。<br>(ア) ダイヤモンド　(イ) 塩化ナトリウム　(ウ) 銅　(エ) ドライアイス　(オ) 二酸化ケイ素<br>(1) それぞれの結晶の種類を、イオン結晶・共有結合の結晶・金属結晶・分子結晶から選べ。<br>(2) 固体の状態で電気をよく導くものを選べ。<br>(3) 常圧で加熱すると、液体を経ずに気体になるものを選べ。<br>(4) 固体では電気を導かないが、融解した液体や水溶液にすると電気を導くものを選べ。",
  "a": r"(1) (ア) 共有結合の結晶　(イ) イオン結晶　(ウ) 金属結晶　(エ) 分子結晶　(オ) 共有結合の結晶　(2) (ウ)　(3) (エ)　(4) (イ)",
  "s": r"金属結晶は自由電子が結晶中を動けるので、固体のままで電気を導く。イオン結晶ではイオンが決まった位置に固定されているので固体では導かないが、融解・溶解するとイオンが動けるようになり導く。分子結晶は分子どうしが弱い分子間力で集まっているだけなので融点が低く、ドライアイスは常圧で約 −78 ℃ で昇華する。ダイヤモンドや二酸化ケイ素は原子が共有結合で立体的につながっており、きわめて硬く融点も高い。<br><b>ポイント</b>：粒子の種類と結合（イオン・共有・金属・分子間力）から、融点・電気伝導性・硬さを判断する。"},
 {"lv": "B", "tag": "正誤",
  "q": r"イオン化エネルギーと電子親和力に関する次の記述 ①〜⑤ のうち、誤りを含むものを2つ選べ。また、①が誤りであることを示す例を、第2周期の元素から1組あげよ。<br>① 同じ周期では、原子番号が大きくなるほど第一イオン化エネルギーは必ず大きくなる。<br>② 各周期で第一イオン化エネルギーが最大の原子は、貴ガスの原子である。<br>③ アルカリ金属では、原子番号が大きいほど第一イオン化エネルギーは小さい。<br>④ 電子親和力が大きい原子ほど、陽イオンになりやすい。<br>⑤ ナトリウムの第二イオン化エネルギーは、第一イオン化エネルギーよりはるかに大きい。",
  "a": r"①、④（①の例：$\mathrm{Be}$ より $\mathrm{B}$ の方が小さい。$\mathrm{N}$ と $\mathrm{O}$ の組でもよい）",
  "s": r"① 誤り。周期表の右へ行くほど大きくなる傾向はあるが、$\mathrm{Be}\to\mathrm{B}$、$\mathrm{N}\to\mathrm{O}$ では小さくなる（電子が入る軌道のエネルギーや電子どうしの反発の違いによる）。② 正しい。貴ガスは閉殻で安定な電子配置をもち、電子を取り去りにくい。③ 正しい。原子番号が大きいほど最外殻が原子核から遠くなり、最外殻電子を取り去りやすい。④ 誤り。電子親和力が大きい原子は、電子を受け取って<b>陰イオン</b>になりやすい。陽イオンになりやすいのは、第一イオン化エネルギーが小さい原子である。⑤ 正しい。$\mathrm{Na^+}$ は Ne と同じ閉殻の電子配置で、2個目の電子は内側の殻から取り去ることになる。<br><b>ポイント</b>：イオン化エネルギー小 → 陽イオンになりやすい、電子親和力大 → 陰イオンになりやすい。周期表の傾向には「例外」もあることを押さえる。"},
 {"lv": "B", "tag": "分子の形と極性",
  "q": r"次の分子について、下の問いに答えよ。<br>$\mathrm{CO_2}$　$\mathrm{H_2O}$　$\mathrm{NH_3}$　$\mathrm{CH_4}$　$\mathrm{CCl_4}$　$\mathrm{HCl}$　$\mathrm{CH_3Cl}$<br>(1) $\mathrm{CO_2}$、$\mathrm{H_2O}$、$\mathrm{NH_3}$、$\mathrm{CH_4}$ の分子の形を答えよ。<br>(2) 極性分子をすべて選べ。<br>(3) $\mathrm{CO_2}$ は $\mathrm{C{=}O}$ 結合に極性があるにもかかわらず、無極性分子である。その理由を述べよ。",
  "a": r"(1) $\mathrm{CO_2}$ 直線形、$\mathrm{H_2O}$ 折れ線形、$\mathrm{NH_3}$ 三角錐形、$\mathrm{CH_4}$ 正四面体形　(2) $\mathrm{H_2O}$、$\mathrm{NH_3}$、$\mathrm{HCl}$、$\mathrm{CH_3Cl}$　(3) 直線形で、2つの $\mathrm{C{=}O}$ 結合の極性が反対向きに等しく、打ち消し合うから。",
  "s": r"電気陰性度の異なる原子間の結合には極性がある。分子全体の極性は、結合の極性（向きをもつ量）を合わせたもので決まる。$\mathrm{CH_4}$・$\mathrm{CCl_4}$ は正四面体の中心から4方向に同じ結合が出ているので打ち消し合い、無極性。$\mathrm{CH_3Cl}$ は4本のうち1本だけが $\mathrm{C{-}Cl}$ なので打ち消し合わず、極性分子。$\mathrm{H_2O}$（結合角 約 105°）、$\mathrm{NH_3}$（約 107°）も形が対称でないため極性分子。$\mathrm{HCl}$ のような異なる原子の二原子分子は必ず極性分子。<br><b>ポイント</b>：まず分子の形を決め、次に結合の極性が打ち消し合うかを考える。"},
 {"lv": "B", "tag": "グラフ読解",
  "q": r"図は、14〜17族元素の水素化合物の沸点を周期ごとに示したものである。<br>" + fig_bp() +
       r"(1) 14族の水素化合物では、周期が大きくなるほど沸点が高くなる。その理由を述べよ。<br>(2) $\mathrm{H_2O}$、$\mathrm{HF}$、$\mathrm{NH_3}$ の沸点が、同族の他の水素化合物に比べて著しく高い理由を述べよ。<br>(3) $\mathrm{H_2O}$ の沸点が $\mathrm{HF}$ より高い理由を、1分子あたりの水素結合の数に着目して説明せよ。<br>(4) $\mathrm{SiH_4}$ と $\mathrm{H_2S}$ は分子量がほぼ等しい（32 と 34）が、沸点は $\mathrm{H_2S}$ の方が高い。理由を述べよ。",
  "a": r"(1) 分子量が大きいほどファンデルワールス力が強くなるから。(2) F・O・N は電気陰性度が大きく、分子間で水素結合をつくるから。(3) 1分子あたりの水素結合は、$\mathrm{H_2O}$ が平均2本、$\mathrm{HF}$ が平均1本で、$\mathrm{H_2O}$ の方が多いから。(4) $\mathrm{SiH_4}$ は無極性分子、$\mathrm{H_2S}$ は極性分子で、$\mathrm{H_2S}$ には極性による引力もはたらくから。",
  "s": r"(1) 14族の水素化合物はすべて正四面体形の無極性分子で、分子間にはファンデルワールス力だけがはたらく。分子量（分子の大きさ）が大きいほどこの力は強い。(2) 電気陰性度の大きい F・O・N に結合した H は強く正に帯電し、隣の分子の F・O・N の非共有電子対との間に水素結合ができる。沸点はおよそ $\mathrm{H_2O}$ 100 ℃、$\mathrm{HF}$ 20 ℃、$\mathrm{NH_3}$ −33 ℃。(3) $\mathrm{H_2O}$ は H を2個、非共有電子対を2組もち、1分子が4本の水素結合にかかわる（1本は2分子で共有するので、1分子あたり平均2本）。$\mathrm{HF}$ は H が1個なので平均1本。1本あたりの強さは $\mathrm{HF}$ の方が大きいが、本数の差が効く。(4) $\mathrm{H_2S}$ は折れ線形の極性分子。<br><b>ポイント</b>：沸点の比較は「水素結合の有無 → 分子量（ファンデルワールス力）→ 極性」の順に考える。"},
 {"lv": "B", "tag": "単位格子の計算",
  "q": r"鉄の結晶は下図の体心立方格子をとり、単位格子の一辺の長さは $2.87\times10^{-8}\ \mathrm{cm}$ である。$\mathrm{Fe}=56$、アボガドロ定数 $6.0\times10^{23}\ /\mathrm{mol}$、$\sqrt3=1.73$、$\pi=3.14$、$2.87^3=23.6$ とする。" + FIG_BCC +
       r"(1) 単位格子に含まれる原子の数と、配位数を答えよ。<br>(2) 鉄の密度〔$\mathrm{g/cm^3}$〕を有効数字2桁で求めよ。<br>(3) 鉄原子を球とみなし、最も近い原子どうしが接しているとして、原子の半径〔cm〕を有効数字3桁で求めよ。<br>(4) 充填率（単位格子の体積に占める原子の体積の割合）は何%か。整数で答えよ。",
  "a": r"(1) 2個、配位数 8　(2) $7.9\ \mathrm{g/cm^3}$　(3) $1.24\times10^{-8}\ \mathrm{cm}$　(4) 68%",
  "s": r"(1) 頂点の原子は8個の単位格子で共有されるので $\frac18\times8=1$、中心に1個で、合計2個。中心の原子は8個の頂点の原子と接する。(2) 密度＝単位格子の質量÷体積＝$\dfrac{56\times2}{6.0\times10^{23}}\div(2.87\times10^{-8})^3=\dfrac{112}{6.0\times10^{23}\times23.6\times10^{-24}}\fallingdotseq7.9\ \mathrm{g/cm^3}$。(3) 原子は立方体の対角線（長さ $\sqrt3a$）上で接するので $4r=\sqrt3a$。$r=\dfrac{1.73\times2.87\times10^{-8}}{4}\fallingdotseq1.24\times10^{-8}\ \mathrm{cm}$。(4) $\dfrac{2\times\frac43\pi r^3}{a^3}$ に $r=\frac{\sqrt3}{4}a$ を代入すると $\dfrac{\sqrt3\pi}{8}=\dfrac{1.73\times3.14}{8}\fallingdotseq0.68$。<br><b>ポイント</b>：「どこで原子が接しているか」で $r$ と $a$ の関係が決まる（体心立方：立方体の対角線 $4r=\sqrt3a$、面心立方：面の対角線 $4r=\sqrt2a$）。"},
 {"lv": "B", "tag": "イオン結晶",
  "q": r"塩化ナトリウムの結晶は下図の単位格子をもつ。単位格子の一辺を $5.6\times10^{-8}\ \mathrm{cm}$、$\mathrm{Na}=23$、$\mathrm{Cl}=35.5$、アボガドロ定数 $6.0\times10^{23}\ /\mathrm{mol}$、$5.6^3=176$ とする。" + FIG_NACL +
       r"(1) 単位格子に含まれる $\mathrm{Na^+}$ と $\mathrm{Cl^-}$ の数を答えよ。<br>(2) 1個の $\mathrm{Na^+}$ に最も近い位置にある $\mathrm{Cl^-}$ は何個か。<br>(3) 塩化ナトリウムの密度〔$\mathrm{g/cm^3}$〕を有効数字2桁で求めよ。<br>(4) $\mathrm{Cl^-}$ の半径を $1.7\times10^{-8}\ \mathrm{cm}$ とすると、$\mathrm{Na^+}$ の半径は何 cm か。ただし、$\mathrm{Na^+}$ と $\mathrm{Cl^-}$ は単位格子の辺上で接しているものとする。<br>(5) 酸化マグネシウム $\mathrm{MgO}$ も同じ型の結晶であるが、融点（約 2800 ℃）は塩化ナトリウム（801 ℃）よりはるかに高い。その理由を述べよ。",
  "a": r"(1) $\mathrm{Na^+}$ 4個、$\mathrm{Cl^-}$ 4個　(2) 6個　(3) $2.2\ \mathrm{g/cm^3}$　(4) $1.1\times10^{-8}\ \mathrm{cm}$　(5) $\mathrm{MgO}$ はイオンの価数が2で、イオン間の距離も短いため、イオン間にはたらく静電気的な引力（クーロン力）がはるかに強いから。",
  "s": r"(1) $\mathrm{Cl^-}$：頂点 $\frac18\times8$＋面の中心 $\frac12\times6=4$。$\mathrm{Na^+}$：辺の中点 $\frac14\times12$＋中心 $1=4$。(2) 中心の $\mathrm{Na^+}$ は上下・左右・前後の6個の面の中心の $\mathrm{Cl^-}$ に囲まれる。(3) $\dfrac{58.5\times4}{6.0\times10^{23}\times176\times10^{-24}}=\dfrac{234}{105.6}\fallingdotseq2.2\ \mathrm{g/cm^3}$。(4) 一辺の上に $\mathrm{Cl^-}$・$\mathrm{Na^+}$・$\mathrm{Cl^-}$ が並ぶので $a=2(r_++r_-)$。$r_+=\frac{5.6}{2}\times10^{-8}-1.7\times10^{-8}=1.1\times10^{-8}\ \mathrm{cm}$。(5) クーロン力は電荷の積に比例し、距離が小さいほど強い。$\mathrm{Mg^{2+}}$ と $\mathrm{O^{2-}}$ は電荷の積が $\mathrm{Na^+}$ と $\mathrm{Cl^-}$ の4倍で、イオン半径も小さい。<br><b>ポイント</b>：イオン結晶の融点は「イオンの価数が大きいほど、イオン半径が小さいほど高い」。"},
 {"lv": "C", "tag": "総合",
  "q": r"銅の結晶は下図の面心立方格子で、単位格子の一辺の長さは $3.6\times10^{-8}\ \mathrm{cm}$、密度は $8.9\ \mathrm{g/cm^3}$ である。$\mathrm{Cu}=63.5$、$\sqrt2=1.41$、$\pi=3.14$、$3.6^3=46.7$ とする。" + FIG_FCC +
       r"(1) 単位格子に含まれる原子の数と、配位数を答えよ。<br>(2) 上の値から、アボガドロ定数を有効数字2桁で求めよ。<br>(3) 銅原子の半径〔cm〕を有効数字2桁で求めよ。<br>(4) 充填率は何%か（整数）。体心立方格子と比べて大きいか小さいか。<br>(5) 単位格子の中心には、6個の銅原子に囲まれたすき間がある。このすき間に、まわりの銅原子と接するように入る球の最大の半径は、銅原子の半径の何倍か。有効数字2桁で答えよ。",
  "a": r"(1) 4個、配位数 12　(2) $6.1\times10^{23}\ /\mathrm{mol}$　(3) $1.3\times10^{-8}\ \mathrm{cm}$　(4) 74%、体心立方格子（68%）より大きい　(5) 0.41倍",
  "s": r"(1) 頂点 $\frac18\times8=1$、面の中心 $\frac12\times6=3$ で4個。ある原子に最も近い原子は12個。(2) 密度 $d=\dfrac{4M}{N_\mathrm{A}a^3}$ より $N_\mathrm{A}=\dfrac{4M}{da^3}=\dfrac{4\times63.5}{8.9\times46.7\times10^{-24}}\fallingdotseq6.1\times10^{23}\ /\mathrm{mol}$。(3) 面の対角線上で接するので $4r=\sqrt2a$、$r=\dfrac{1.41\times3.6\times10^{-8}}{4}\fallingdotseq1.3\times10^{-8}\ \mathrm{cm}$。(4) $\dfrac{4\times\frac43\pi r^3}{a^3}=\dfrac{\sqrt2\pi}{6}=\dfrac{1.41\times3.14}{6}\fallingdotseq0.74$。面心立方格子と六方最密構造は最も密な詰まり方（最密充填）で、充填率は 74%。(5) 中心から面の中心の原子までの距離は $\frac a2$。入る球の半径を $x$ とすると $x+r=\frac a2$。$a=2\sqrt2r$ を代入して $x=(\sqrt2-1)r\fallingdotseq0.41r$。<br><b>ポイント</b>：密度の式 $d=\dfrac{(\text{単位格子中の原子数})\times M}{N_\mathrm{A}a^3}$ は、どの量を求めるときにも使える。すき間の問題は「どの原子どうしが一直線に並んで接するか」を図で確かめる。"},
 {"lv": "C", "tag": "総合・論述",
  "q": r"ダイヤモンドの単位格子は、面心立方格子の位置にある炭素原子に加えて、単位格子を8等分した小さな立方体のうち1つおきの4個の中心にも炭素原子がある構造である（下図）。単位格子の一辺は $3.56\times10^{-8}\ \mathrm{cm}$、$\mathrm{C}=12$、アボガドロ定数 $6.0\times10^{23}\ /\mathrm{mol}$、$3.56^3=45.1$、$\sqrt3=1.73$ とする。" + FIG_DIA +
       r"(1) 単位格子に含まれる炭素原子の数を答えよ。<br>(2) ダイヤモンドの密度〔$\mathrm{g/cm^3}$〕を有効数字2桁で求めよ。<br>(3) 隣り合う炭素原子間の距離（結合距離）〔cm〕を有効数字3桁で求めよ。<br>(4) 黒鉛はダイヤモンドと同じ炭素の同素体であるが、やわらかく、電気をよく導く。この違いを、原子の結合のしかたに着目して100字以内で説明せよ。",
  "a": r"(1) 8個　(2) $3.5\ \mathrm{g/cm^3}$　(3) $1.54\times10^{-8}\ \mathrm{cm}$　(4) 解答例：ダイヤモンドは各炭素原子が4個の原子と共有結合した立体網目構造で、硬く電気を導かない。黒鉛は3個の原子と結合した平面層が弱い分子間力で重なるのではがれやすく、残りの価電子が層内を動けるので電気を導く。（100字）",
  "s": r"(1) 面心立方格子の位置に4個、内部に4個で8個。(2) $\dfrac{12\times8}{6.0\times10^{23}\times45.1\times10^{-24}}=\dfrac{96}{27.06}\fallingdotseq3.5\ \mathrm{g/cm^3}$。(3) 内部の原子は、一辺 $\frac a2$ の小立方体の中心にあり、その小立方体の4つの頂点の原子と結合している。距離は小立方体の対角線 $\frac{\sqrt3}{2}a$ の半分で $\frac{\sqrt3}{4}a=\dfrac{1.73\times3.56\times10^{-8}}{4}\fallingdotseq1.54\times10^{-8}\ \mathrm{cm}$。(4) 黒鉛では各炭素原子の4個の価電子のうち3個が共有結合に使われ、正六角形が連なった平面層をつくる。残りの1個は層全体に広がって動けるため、層に平行な方向に電気をよく導く。<br><b>ポイント</b>：同素体の性質の違いは「何個の原子と、どんな形に結合しているか」で説明する。"},
]}}


def verify():
    items = CH[1]["items"]
    lv = [it["lv"] for it in items]
    assert lv == sorted(lv) and lv.count("A") == 4 and 4 <= lv.count("B") <= 5 and lv.count("C") == 2
    for it in items:
        for k in ("tag", "q", "a", "s"):
            assert it[k].strip(), k
        for k in ("q", "a", "s"):
            assert it[k].count("$") % 2 == 0 and "$$" not in it[k], it[k][:30]
        assert "<b>ポイント</b>" in it["s"]

    def sig(x, n=2):
        return round(x, n - 1 - int(floor(log10(abs(x)))))

    def eq(x, v, n=2):
        assert abs(sig(x, n) - v) <= 1e-9 * abs(v), (x, sig(x, n), v)

    # A2 原子の構造・原子量
    assert (17, 37 - 17, 17) == (17, 20, 17) and (12, 24 - 12, 12 - 2) == (12, 12, 10)
    aw = 34.97 * 0.758 + 36.97 * 0.242
    assert round(aw, 1) == 35.5 and round(34.97 * 0.758, 2) == 26.51 and round(36.97 * 0.242, 2) == 8.95
    # A3 電子配置（Z≦20 は K2 L8 M8 N… の順に入る）
    def conf(n):
        out = []
        for cap in (2, 8, 8, 2):
            out.append(min(cap, n)); n -= out[-1]
        return [c for c in out if c]
    assert conf(8) == [2, 6] and conf(13) == [2, 8, 3] and conf(16 + 2) == [2, 8, 8] and conf(19 - 1) == [2, 8, 8]
    assert conf(18) == conf(16 + 2) == conf(19 - 1)
    # B3 分子量
    assert round(28.1 + 4 * 1.0) == 32 and round(2 * 1.0 + 32.1) == 34
    # B4 鉄（体心立方）
    a = 2.87e-8
    assert round(2.87 ** 3, 1) == 23.6
    eq(2 * 56 / (6.0e23 * 23.6e-24), 7.9)
    eq(1.73 * a / 4, 1.24e-8, 3)
    assert round(1.73 * 3.14 / 8, 2) == 0.68
    assert abs(sqrt(3) * pi / 8 - 0.680) < 1e-3
    # B5 NaCl
    half = [(i / 2, j / 2, k / 2) for i in range(3) for j in range(3) for k in range(3)]
    def share(p):  # 単位格子内に含まれる割合
        f = 1.0
        for c in p:
            f *= 0.5 if c in (0, 1) else 1.0
        return f
    ncl = sum(share(p) for p in half if int(round(2 * sum(p))) % 2 == 0)
    nna = sum(share(p) for p in half if int(round(2 * sum(p))) % 2 == 1)
    assert ncl == 4 and nna == 4
    assert round(5.6 ** 3) == 176
    eq(58.5 * 4 / (6.0e23 * 176e-24), 2.2)
    eq(5.6e-8 / 2 - 1.7e-8, 1.1e-8)
    # C1 銅（面心立方）
    assert round(3.6 ** 3, 1) == 46.7
    eq(4 * 63.5 / (8.9 * 46.7e-24), 6.1e23)
    eq(1.41 * 3.6e-8 / 4, 1.3e-8)
    assert round(1.41 * 3.14 / 6, 2) == 0.74
    r = sqrt(2) / 4
    eq((0.5 - r) / r, 0.41)
    # 面心立方の最近接原子数 12、体心立方 8
    fcc = [(x + dx, y + dy, z + dz) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)
           for dx, dy, dz in [(0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)]]
    d = sorted(sqrt(sum(c * c for c in p)) for p in fcc if p != (0, 0, 0))
    assert sum(1 for v in d if abs(v - d[0]) < 1e-9) == 12
    bcc = [(x + dx, y + dy, z + dz) for x in range(-1, 2) for y in range(-1, 2) for z in range(-1, 2)
           for dx, dy, dz in [(0, 0, 0), (0.5, 0.5, 0.5)]]
    d = sorted(sqrt(sum(c * c for c in p)) for p in bcc if p != (0, 0, 0))
    assert sum(1 for v in d if abs(v - d[0]) < 1e-9) == 8
    # C2 ダイヤモンド
    assert len(_tet) + 4 == 8 and len(_dbonds) == 16   # 内部の4原子がそれぞれ4本
    assert round(3.56 ** 3, 1) == 45.1
    eq(12 * 8 / (6.0e23 * 45.1e-24), 3.5)
    eq(1.73 * 3.56e-8 / 4, 1.54e-8, 3)
    m = re.search(r"解答例：(.*?)（(\d+)字）", items[10]["a"])
    assert len(m.group(1)) == int(m.group(2)) <= 100, len(m.group(1))
