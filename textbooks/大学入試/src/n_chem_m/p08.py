"""問題集 第8章 反応速度と化学平衡。CH に問題、verify() で速度・平衡の計算と形式を検算する。"""
from math import log10, floor, log, exp, sqrt

B = '<div class="bun">'
KI = r"(\text{気})"
R = 8.3e3   # Pa·L/(K·mol)

# エネルギー図の値（kJ）。反応物 H2+I2 を基準 0 とする
E_TS, E_CAT, E_PROD = 174, 49, -9


def _sub(s):
    """'H2+I2' → 下付き数字の SVG テキスト"""
    out, low = [], False
    for ch in s:
        if ch.isdigit() and out and not out[-1].endswith(" "):
            out.append(f'<tspan dy="3" font-size="8">{ch}</tspan>'); low = True
        else:
            out.append(f'<tspan dy="-3">{ch}</tspan>' if low else ch); low = False
    return "".join(out)


def fig_energy():
    """H2 + I2 → 2HI のエネルギー図（模式図。高さは値に比例しない）"""
    W, H = 380, 215
    yR, yP, yT, yC = 165, 188, 28, 118
    sol = f"M40,{yR} L120,{yR} C165,{yR} 170,{yT} 205,{yT} C240,{yT} 245,{yP} 290,{yP} L345,{yP}"
    cat = f"M120,{yR} C165,{yR} 170,{yC} 205,{yC} C240,{yC} 245,{yP} 290,{yP}"
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-size="10">',
         f'<line x1="30" y1="{H-22}" x2="{W-10}" y2="{H-22}" stroke="#000"/><line x1="30" y1="{H-22}" x2="30" y2="8" stroke="#000"/>',
         f'<text x="{W-10}" y="{H-10}" text-anchor="end">反応の進行</text>',
         f'<text x="35" y="14" font-size="9">エネルギー</text>',
         f'<line x1="70" y1="{yT}" x2="205" y2="{yT}" stroke="#888" stroke-dasharray="2,3"/>',
         f'<line x1="100" y1="{yC}" x2="205" y2="{yC}" stroke="#888" stroke-dasharray="2,3"/>',
         f'<line x1="120" y1="{yR}" x2="365" y2="{yR}" stroke="#888" stroke-dasharray="2,3"/>',
         f'<path d="{sol}" fill="none" stroke="#000" stroke-width="1.6"/>',
         f'<path d="{cat}" fill="none" stroke="#000" stroke-width="1.3" stroke-dasharray="5,3"/>',
         f'<text x="44" y="{yR+14}">{_sub("H2 + I2")}</text>',
         f'<text x="296" y="{yP-5}">{_sub("2HI")}</text>']
    def arrow(x, y1, y2, lab, side):
        tip = 5 if y2 > y1 else -5
        anc, dx = ("end", -4) if side < 0 else ("start", 4)
        return (f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="#000"/>'
                f'<path d="M{x-3},{y2-tip} L{x},{y2} L{x+3},{y2-tip}" fill="none" stroke="#000"/>'
                f'<text x="{x+dx}" y="{(y1+y2)/2+3}" text-anchor="{anc}">{lab}</text>')
    o.append(arrow(75, yR, yT, f"{E_TS} kJ", 1))
    o.append(arrow(105, yR, yC, f"{E_CAT} kJ", 1))
    o.append(arrow(355, yR, yP, f"{abs(E_PROD)} kJ", -1))
    o.append(f'<text x="262" y="60" font-size="9">実線：触媒なし</text><text x="262" y="73" font-size="9">破線：触媒あり</text>')
    o.append(f'<text x="{W/2}" y="{H-1}" text-anchor="middle" font-size="9">（模式図。高さは値に比例していない）</text>')
    o.append("</svg>")
    return "".join(o)


C_B4 = "低温ほど平衡はアンモニア側にかたよるが反応が遅すぎるので、触媒を用い、速度と収率のつり合う温度で反応させるから。"

TBL_B1 = ('<table><tr><th>実験</th><th>[A]〔mol/L〕</th><th>[B]〔mol/L〕</th><th>初速度 $v$〔mol/(L·s)〕</th></tr>'
          '<tr><td>1</td><td>0.10</td><td>0.10</td><td>$2.0\\times10^{-4}$</td></tr>'
          '<tr><td>2</td><td>0.20</td><td>0.10</td><td>$8.0\\times10^{-4}$</td></tr>'
          '<tr><td>3</td><td>0.20</td><td>0.30</td><td>$2.4\\times10^{-3}$</td></tr></table>')
N2O5 = [(0, 0.800), (300, 0.566), (600, 0.400), (900, 0.283), (1200, 0.200)]
TBL_C2 = ('<table><tr><th>時間〔s〕</th>' + "".join(f"<td>{t}</td>" for t, _ in N2O5) + '</tr>'
          '<tr><th>$[\\mathrm{N_2O_5}]$〔mol/L〕</th>' + "".join(f"<td>{c:.3f}</td>" for _, c in N2O5) + '</tr></table>')

CH = {8: {
"goal": "反応速度式と速度定数・活性化エネルギーを数値で扱い、平衡定数（濃度・圧平衡定数）の計算とルシャトリエの原理による平衡移動の判断を確実にする。",
"items": [
 {"lv": "A", "tag": "反応速度",
  "q": r"過酸化水素の分解 $\mathrm{2H_2O_2\to2H_2O+O_2}$ で、$\mathrm{H_2O_2}$ の濃度は反応開始時に 0.80 mol/L、60 秒後に 0.68 mol/L であった。<br>(1) この 60 秒間の $\mathrm{H_2O_2}$ の平均の分解速度を求めよ。<br>(2) 同じ時間の $\mathrm{O_2}$ の平均の生成速度を求めよ。<br>(3) この反応の速度が $v=k[\mathrm{H_2O_2}]$ で表されるとして、この間の平均の濃度を用いて速度定数 $k$ を求めよ。<br>(4) 温度を 10 K 上げるごとに反応速度が 2 倍になるとすると、温度を 30 K 上げると反応速度は何倍になるか。",
  "a": r"(1) $2.0\times10^{-3}\ \mathrm{mol/(L\cdot s)}$　(2) $1.0\times10^{-3}\ \mathrm{mol/(L\cdot s)}$　(3) $2.7\times10^{-3}\ /\mathrm{s}$　(4) 8 倍",
  "s": r"(1) $v=-\dfrac{\Delta[\mathrm{H_2O_2}]}{\Delta t}=\dfrac{0.80-0.68}{60}=2.0\times10^{-3}\ \mathrm{mol/(L\cdot s)}$。(2) 係数の比 $\mathrm{H_2O_2}:\mathrm{O_2}=2:1$ より、$\frac12$ 倍。(3) 平均の濃度 $\frac{0.80+0.68}{2}=0.74\ \mathrm{mol/L}$。$k=\frac{2.0\times10^{-3}}{0.74}\fallingdotseq2.7\times10^{-3}\ /\mathrm{s}$。(4) $2^3=8$ 倍。<br><b>ポイント</b>：反応速度は「単位時間あたりの濃度の変化量」。物質によって変化量が係数比で異なるので、どの物質で表した速度かを確認する。"},
 {"lv": "A", "tag": "活性化エネルギー",
  "q": r"図は、$\mathrm{H_2" + KI + r"+I_2" + KI + r"\to2HI" + KI + r"}$ の反応の進行にともなうエネルギーの変化を示したものである。" + fig_energy() +
       r"(1) 触媒がないときの、正反応の活性化エネルギーを求めよ。<br>(2) 触媒がないときの、逆反応 $\mathrm{2HI\to H_2+I_2}$ の活性化エネルギーを求めよ。<br>(3) 正反応の反応エンタルピー $\Delta H$ を、符号をつけて答えよ。<br>(4) 触媒を用いたときの、逆反応の活性化エネルギーを求めよ。<br>(5) 触媒を加えても変化しないものを、次からすべて選べ。<br>反応速度　活性化エネルギー　反応エンタルピー　平衡定数",
  "a": r"(1) 174 kJ　(2) 183 kJ　(3) $\Delta H=-9\ \mathrm{kJ}$　(4) 58 kJ　(5) 反応エンタルピー、平衡定数",
  "s": r"(1) 反応物から遷移状態（活性化状態）までの高さ。(2) 生成物から遷移状態までの高さなので $174+9=183\ \mathrm{kJ}$。(3) 生成物の方が 9 kJ 低いので発熱反応、$\Delta H=-9\ \mathrm{kJ}$。(4) $49+9=58\ \mathrm{kJ}$。(5) 触媒は活性化エネルギーの小さい別の経路をつくり、正反応も逆反応も速くする。はじめと終わりの状態は変わらないので、反応エンタルピーは変わらない。正逆両方が同じ割合で速くなるので、平衡に達するまでの時間は短くなるが、平衡定数（平衡の位置）は変わらない。<br><b>ポイント</b>：逆反応の活性化エネルギー＝正反応の活性化エネルギー－$\Delta H$。触媒が変えるのは「速さ」だけで、「到達点」は変えない。"},
 {"lv": "A", "tag": "平衡定数",
  "q": r"容積 10 L の容器に水素 1.0 mol とヨウ素 1.0 mol を入れて一定温度に保つと、$\mathrm{H_2+I_2\rightleftarrows2HI}$ の平衡に達し、ヨウ化水素が 1.6 mol 生じた。<br>(1) 平衡時の水素とヨウ素の物質量を求めよ。<br>(2) この温度での平衡定数 $K$ を求めよ。<br>(3) 同じ容器・同じ温度で、ヨウ化水素 2.0 mol だけを入れて平衡に達したとき、水素の物質量を求めよ。<br>(4) この温度での $\mathrm{2HI\rightleftarrows H_2+I_2}$ の平衡定数を求めよ。",
  "a": r"(1) どちらも 0.20 mol　(2) 64　(3) 0.20 mol　(4) $1.6\times10^{-2}$",
  "s": r"(1) HI 1.6 mol が生じるのに $\mathrm{H_2}$、$\mathrm{I_2}$ は 0.80 mol ずつ反応するので、残りは 0.20 mol ずつ。(2) $K=\dfrac{[\mathrm{HI}]^2}{[\mathrm{H_2}][\mathrm{I_2}]}=\dfrac{(1.6/10)^2}{(0.20/10)(0.20/10)}=64$。この反応では両辺の係数の和が等しいので、体積は約分されて消える。(3) $\mathrm{H_2}$ を $x$ mol とすると $\mathrm{I_2}$ も $x$ mol、HI は $(2.0-2x)$ mol。$\dfrac{(2.0-2x)^2}{x^2}=64$ より $\dfrac{2.0-2x}{x}=8$、$x=0.20$。(1) と同じ平衡状態になる。(4) 逆反応の平衡定数は逆数で $\frac1{64}\fallingdotseq1.6\times10^{-2}$。<br><b>ポイント</b>：平衡の計算は「はじめ・変化量・平衡時」の表をつくる。同じ組成なら、どちら側から始めても同じ平衡状態に達する。"},
 {"lv": "A", "tag": "ルシャトリエの原理",
  "q": r"$\mathrm{N_2" + KI + r"+3H_2" + KI + r"\to2NH_3" + KI + r"}\quad\Delta H=-92\ \mathrm{kJ}$ で表される反応が、ある条件で平衡状態にある。次の操作をすると、平衡はどちらに移動するか。「右」「左」「移動しない」で答えよ。<br>(1) 温度を一定に保って圧縮する。　(2) 圧力を一定に保って加熱する。　(3) 触媒を加える。<br>(4) 温度・体積を一定に保ってアルゴンを加える。　(5) 温度・全圧を一定に保ってアルゴンを加える。<br>(6) 温度・体積を一定に保って、生じたアンモニアの一部を取り除く。",
  "a": r"(1) 右　(2) 左　(3) 移動しない　(4) 移動しない　(5) 左　(6) 右",
  "s": r"ルシャトリエの原理：平衡状態の条件を変えると、その変化をやわらげる向きに平衡が移動する。(1) 圧力の増加をやわらげる＝気体分子の数が減る右向き（$4\to2$）。(2) 加熱をやわらげる＝吸熱の向き＝左。(3) 触媒は平衡を移動させない。(4) 体積一定でアルゴンを加えても、各成分の分圧（濃度）は変わらない。(5) 全圧一定でアルゴンを加えると体積が増え、各成分の分圧の和が下がるので、分子の数が増える左向き。(6) 生成物を減らすと、それを補う右向き。<br><b>ポイント</b>：貴ガスを加えるときは「体積一定 → 移動しない」「全圧一定 → 反応に関わる気体の分圧が下がるので、減圧と同じ」。"},
 {"lv": "B", "tag": "反応速度式の決定",
  "q": r"反応 $\mathrm{2A+B\to C}$ について、反応物の濃度を変えて初速度 $v$ を測定し、次の結果を得た。" + TBL_B1 +
       r"反応速度式を $v=k[\mathrm{A}]^x[\mathrm{B}]^y$ とする。<br>(1) $x$、$y$ を求めよ。<br>(2) 速度定数 $k$ を、単位をつけて求めよ。<br>(3) $[\mathrm{A}]=0.30\ \mathrm{mol/L}$、$[\mathrm{B}]=0.20\ \mathrm{mol/L}$ のときの初速度を求めよ。<br>(4) 反応速度式の次数（$x$、$y$）は、化学反応式の係数から決めることはできない。その理由を簡潔に述べよ。",
  "a": r"(1) $x=2$、$y=1$　(2) $k=0.20\ \mathrm{L^2/(mol^2\cdot s)}$　(3) $3.6\times10^{-3}\ \mathrm{mol/(L\cdot s)}$　(4) 多くの反応はいくつかの段階（素反応）を経て進み、速度式はそれらのしくみで決まるので、実験によって求める必要があるから。",
  "s": r"(1) 実験1と2：[B] が同じで [A] が2倍になると $v$ は4倍 → $2^x=4$、$x=2$。実験2と3：[A] が同じで [B] が3倍になると $v$ は3倍 → $y=1$。(2) 実験1より $k=\dfrac{2.0\times10^{-4}}{0.10^2\times0.10}=0.20$。単位は $\dfrac{\mathrm{mol/(L\cdot s)}}{(\mathrm{mol/L})^3}=\mathrm{L^2/(mol^2\cdot s)}$。(3) $0.20\times0.30^2\times0.20=3.6\times10^{-3}$。(4) この反応では係数と次数がたまたま一致しているが、一般には一致しない。<br><b>ポイント</b>：一方の濃度だけを変えた2つの実験を比べて、次数を1つずつ決める。$k$ の単位は次数によって変わる。"},
 {"lv": "B", "tag": "アレニウスの式",
  "q": r"速度定数 $k$ と絶対温度 $T$ の関係は、アレニウスの式 $k=Ae^{-\frac{E_\mathrm{a}}{RT}}$（$A$ は定数、$E_\mathrm{a}$ は活性化エネルギー）で表される。気体定数 $R=8.3\ \mathrm{J/(K\cdot mol)}$、$\log_e2=0.69$ とする。<br>(1) ある反応の速度定数は、温度を 300 K から 310 K にすると 2 倍になった。この反応の活性化エネルギー〔kJ/mol〕を求めよ。<br>(2) 300 K でこの反応に触媒を加えると、活性化エネルギーが 10 kJ/mol 小さくなった。反応速度は何倍になるか。$e^{4.0}=55$ とし、$A$ は変わらないものとする。<br>(3) 温度を上げると反応速度が大きくなる理由を、分子の運動エネルギーの分布と関連づけて説明せよ。",
  "a": r"(1) 53 kJ/mol　(2) 55 倍　(3) 温度が高くなると、活性化エネルギー以上の運動エネルギーをもつ分子の割合が大きく増え、反応できる衝突の回数が増えるから。",
  "s": r"(1) 両辺の自然対数をとると $\log_ek=\log_eA-\dfrac{E_\mathrm{a}}{RT}$。2つの温度で差をとって $\log_e\dfrac{k_{310}}{k_{300}}=\dfrac{E_\mathrm{a}}{R}\left(\dfrac1{300}-\dfrac1{310}\right)$。$0.69=\dfrac{E_\mathrm{a}}{8.3}\times\dfrac{10}{300\times310}$ より $E_\mathrm{a}=\dfrac{0.69\times8.3\times93000}{10}\fallingdotseq5.3\times10^4\ \mathrm{J/mol}$。(2) $\dfrac{k'}{k}=e^{\frac{10\times10^3}{8.3\times300}}=e^{4.0}=55$。(3) 温度が少し上がるだけでも、分布の「すそ」の高エネルギー側の分子が急増する（衝突の回数自体の増加はわずか）。<br><b>ポイント</b>：アレニウスの式は対数をとって2点の差で使う。活性化エネルギーが大きい反応ほど、温度による速度の変化が大きい。"},
 {"lv": "B", "tag": "濃度平衡定数と圧平衡定数",
  "q": r"容積 5.0 L の容器に四酸化二窒素 $\mathrm{N_2O_4}$ 0.50 mol を入れて 350 K に保つと、$\mathrm{N_2O_4\rightleftarrows2NO_2}$ の平衡に達し、$\mathrm{N_2O_4}$ の 40% が解離した。$R=8.3\times10^3\ \mathrm{Pa\cdot L/(K\cdot mol)}$ とする。<br>(1) 平衡時の $\mathrm{N_2O_4}$ と $\mathrm{NO_2}$ の物質量を求めよ。<br>(2) 濃度平衡定数 $K_\mathrm{c}$ を、単位をつけて求めよ。<br>(3) 平衡時の全圧を求めよ。<br>(4) 圧平衡定数 $K_\mathrm{p}$ を、単位をつけて求めよ。<br>(5) $K_\mathrm{p}$ と $K_\mathrm{c}$ の間に成り立つ関係式を示し、(2)(4) の値で成り立っていることを確かめよ。",
  "a": r"(1) $\mathrm{N_2O_4}$ 0.30 mol、$\mathrm{NO_2}$ 0.40 mol　(2) $K_\mathrm{c}=0.11\ \mathrm{mol/L}$　(3) $4.1\times10^5\ \mathrm{Pa}$　(4) $K_\mathrm{p}=3.1\times10^5\ \mathrm{Pa}$　(5) $K_\mathrm{p}=K_\mathrm{c}RT$。$0.107\times8.3\times10^3\times350\fallingdotseq3.1\times10^5$ で一致する。",
  "s": r"(1) 解離した $\mathrm{N_2O_4}$ は $0.50\times0.40=0.20\ \mathrm{mol}$。残り 0.30 mol、$\mathrm{NO_2}$ は $2\times0.20=0.40\ \mathrm{mol}$。(2) $[\mathrm{N_2O_4}]=0.060$、$[\mathrm{NO_2}]=0.080\ \mathrm{mol/L}$。$K_\mathrm{c}=\dfrac{0.080^2}{0.060}=0.107\fallingdotseq0.11\ \mathrm{mol/L}$。(3) 合計 0.70 mol なので $P=\dfrac{0.70\times8.3\times10^3\times350}{5.0}\fallingdotseq4.1\times10^5\ \mathrm{Pa}$。(4) 分圧は $p_{\mathrm{NO_2}}=4.07\times10^5\times\frac{0.40}{0.70}=2.32\times10^5$、$p_{\mathrm{N_2O_4}}=1.74\times10^5\ \mathrm{Pa}$。$K_\mathrm{p}=\dfrac{(2.32\times10^5)^2}{1.74\times10^5}\fallingdotseq3.1\times10^5\ \mathrm{Pa}$。(5) $p=\frac nVRT=[\ ]RT$ を代入すると、$K_\mathrm{p}=\dfrac{([\mathrm{NO_2}]RT)^2}{[\mathrm{N_2O_4}]RT}=K_\mathrm{c}RT$。<br><b>ポイント</b>：$K_\mathrm{p}=K_\mathrm{c}(RT)^{\Delta n}$（$\Delta n$：気体分子の数の増加量）。この反応では $\Delta n=2-1=1$。"},
 {"lv": "B", "tag": "論述",
  "q": r"(1) 赤褐色の二酸化窒素 $\mathrm{NO_2}$ と無色の四酸化二窒素 $\mathrm{N_2O_4}$ の平衡混合気体を注射器に入れ、温度を一定に保ってすばやく圧縮した。圧縮した直後と、しばらくたったあとの色の変化を、理由とともに説明せよ。<br>(2) この平衡混合気体を冷却すると、色が薄くなった。$\mathrm{2NO_2\to N_2O_4}$ の反応エンタルピー $\Delta H$ の符号を答えよ。<br>(3) アンモニアの工業的製法（ハーバー・ボッシュ法）では、アンモニアの生成が発熱反応であるにもかかわらず、約 400〜500 ℃ の高温で反応させる。その理由を60字以内で述べよ。",
  "a": r"(1) 圧縮した直後は、$\mathrm{NO_2}$ の濃度が大きくなるので色が濃くなる。その後、気体分子の数が減る $\mathrm{N_2O_4}$ 生成の向きに平衡が移動するので、色はやや薄くなる（ただし、圧縮前よりは濃い）。　(2) 負　(3) 解答例：" + C_B4 + "（" + str(len(C_B4)) + "字）",
  "s": r"(1) 平衡の移動は、圧縮による変化を「やわらげる」だけで、打ち消しはしない。そのため最終的な $\mathrm{NO_2}$ の濃度は圧縮前より大きい。(2) 冷却すると発熱の向きに平衡が移動する。色が薄くなった（$\mathrm{N_2O_4}$ が増えた）ので、$\mathrm{N_2O_4}$ 生成の向きが発熱、$\Delta H\lt0$。(3) 平衡の面だけなら低温・高圧が有利だが、低温では反応が遅すぎて実用にならない。そこで四酸化三鉄を主成分とする触媒を用い、$2\times10^7$〜$3\times10^7\ \mathrm{Pa}$ 程度の高圧で反応させる。<br><b>ポイント</b>：工業的な条件は「平衡（収率）」と「速度」の両方から決まる。平衡の移動は、加えた変化を部分的にやわらげるだけである。"},
 {"lv": "B", "tag": "解離度と圧平衡定数",
  "q": r"五塩化リンは、$\mathrm{PCl_5" + KI + r"\rightleftarrows PCl_3" + KI + r"+Cl_2" + KI + r"}$ のように解離し、ある温度での圧平衡定数は $K_\mathrm{p}=1.2\times10^5\ \mathrm{Pa}$ である。はじめに $\mathrm{PCl_5}$ を $n$ mol とり、その解離度を $\alpha$ とする。<br>(1) 平衡時の気体の全物質量を、$n$、$\alpha$ を用いて表せ。<br>(2) 全圧を $P$ として、$K_\mathrm{p}$ を $\alpha$ と $P$ で表せ。<br>(3) 全圧を $3.6\times10^5\ \mathrm{Pa}$ に保ったときの $\alpha$ を求めよ。<br>(4) 同じ温度で、全圧を $1.2\times10^5\ \mathrm{Pa}$ に保ったときの $\alpha$ を求めよ。$\sqrt2=1.414$ とする。<br>(5) (3)(4) の結果を、ルシャトリエの原理で説明せよ。",
  "a": r"(1) $n(1+\alpha)$　(2) $K_\mathrm{p}=\dfrac{\alpha^2}{1-\alpha^2}P$　(3) 0.50　(4) 0.71　(5) 全圧を下げると、気体分子の数が増える向き（解離の向き）に平衡が移動するので、解離度が大きくなる。",
  "s": r"(1) $\mathrm{PCl_5}$ $n(1-\alpha)$、$\mathrm{PCl_3}$ と $\mathrm{Cl_2}$ が $n\alpha$ ずつで、合計 $n(1+\alpha)$。(2) 分圧はモル分率×全圧：$p_{\mathrm{PCl_3}}=p_{\mathrm{Cl_2}}=\dfrac{\alpha}{1+\alpha}P$、$p_{\mathrm{PCl_5}}=\dfrac{1-\alpha}{1+\alpha}P$。$K_\mathrm{p}=\dfrac{\alpha^2P}{(1+\alpha)(1-\alpha)}=\dfrac{\alpha^2}{1-\alpha^2}P$。(3) $\dfrac{\alpha^2}{1-\alpha^2}=\dfrac{1.2\times10^5}{3.6\times10^5}=\frac13$ より $\alpha^2=\frac14$、$\alpha=0.50$。(4) $\dfrac{\alpha^2}{1-\alpha^2}=1$ より $\alpha^2=\frac12$、$\alpha=\frac{\sqrt2}{2}\fallingdotseq0.71$。<br><b>ポイント</b>：解離平衡は「全物質量 $n(1+\alpha)$ → モル分率 → 分圧」の順に式を立てると、$n$ が消えて $\alpha$ と $P$ だけの式になる。"},
 {"lv": "C", "tag": "総合",
  "q": r"窒素 1.0 mol と水素 3.0 mol を、ある温度で全圧を $2.0\times10^7\ \mathrm{Pa}$ に保ちながら触媒の存在下で反応させると、$\mathrm{N_2+3H_2\rightleftarrows2NH_3}$ の平衡に達し、平衡混合気体中のアンモニアの物質量の割合は $\frac13$ であった。<br>(1) 平衡時の $\mathrm{N_2}$、$\mathrm{H_2}$、$\mathrm{NH_3}$ の物質量を求めよ。<br>(2) 平衡時の各気体の分圧を求めよ。<br>(3) 圧平衡定数 $K_\mathrm{p}$ を、単位をつけて求めよ。<br>(4) 同じ温度で、全圧を $4.0\times10^7\ \mathrm{Pa}$ に保って同様に反応させたとき、平衡混合気体中のアンモニアの物質量の割合は何%になるか。整数で答えよ。$\sqrt7=2.65$ とする。",
  "a": r"(1) $\mathrm{N_2}$ 0.50 mol、$\mathrm{H_2}$ 1.5 mol、$\mathrm{NH_3}$ 1.0 mol　(2) $\mathrm{N_2}$ $3.3\times10^6\ \mathrm{Pa}$、$\mathrm{H_2}$ $1.0\times10^7\ \mathrm{Pa}$、$\mathrm{NH_3}$ $6.7\times10^6\ \mathrm{Pa}$　(3) $1.3\times10^{-14}\ \mathrm{Pa^{-2}}$　(4) 45%",
  "s": r"(1) $\mathrm{N_2}$ が $x$ mol 反応すると、$\mathrm{N_2}$ $1.0-x$、$\mathrm{H_2}$ $3.0-3x$、$\mathrm{NH_3}$ $2x$、合計 $4.0-2x$。$\dfrac{2x}{4.0-2x}=\frac13$ より $x=0.50$。(2) 合計 3.0 mol。$p_{\mathrm{N_2}}=2.0\times10^7\times\frac{0.50}{3.0}\fallingdotseq3.3\times10^6$、$p_{\mathrm{H_2}}=1.0\times10^7$、$p_{\mathrm{NH_3}}\fallingdotseq6.7\times10^6\ \mathrm{Pa}$。(3) $K_\mathrm{p}=\dfrac{p_{\mathrm{NH_3}}^2}{p_{\mathrm{N_2}}\,p_{\mathrm{H_2}}^3}=\dfrac{(\frac{2}{3}\times10^7)^2}{\frac{1}{3}\times10^7\times(1.0\times10^7)^3}=\frac43\times10^{-14}\fallingdotseq1.3\times10^{-14}\ \mathrm{Pa^{-2}}$。(4) 全圧 $P$ のもとで $x$ mol 反応したとすると、モル分率は $\mathrm{NH_3}$ $\dfrac{x}{2-x}$、$\mathrm{N_2}$ $\dfrac{1-x}{2(2-x)}$、$\mathrm{H_2}$ $\dfrac{3(1-x)}{2(2-x)}$ で、$K_\mathrm{p}P^2=\dfrac{16x^2(2-x)^2}{27(1-x)^4}$。両辺の平方根をとると $\dfrac{x(2-x)}{(1-x)^2}=\dfrac{3\sqrt3}{4}P\sqrt{K_\mathrm{p}}$ で、右辺は $P$ に比例する。$P=2.0\times10^7$ のとき $x=0.50$ で左辺は 3 なので、$P=4.0\times10^7$ では 6 になる。$u=1-x$ とおくと $x(2-x)=1-u^2$ なので $\dfrac{1-u^2}{u^2}=6$、$u=\dfrac1{\sqrt7}$。アンモニアの割合は $\dfrac{x}{2-x}=\dfrac{1-u}{1+u}=\dfrac{\sqrt7-1}{\sqrt7+1}=\dfrac{1.65}{3.65}\fallingdotseq0.45$。<br><b>ポイント</b>：全圧一定の平衡では、モル分率×全圧で分圧を表す。同じ温度なら $K_\mathrm{p}$ は一定なので、条件を変えた平衡は「$K_\mathrm{p}$ が同じ」という式で解く。加圧でアンモニアの割合が増える（ルシャトリエの原理）ことも数値で確かめられる。"},
 {"lv": "C", "tag": "一次反応・総合",
  "q": B + r"五酸化二窒素は $\mathrm{2N_2O_5\to4NO_2+O_2}$ のように分解する。ある温度で、容積 1.0 L の容器中の $\mathrm{N_2O_5}$ の濃度を測定し、次の表を得た。</div>" + TBL_C2 +
       r"この反応の速度式は $v=k[\mathrm{N_2O_5}]$ で表される（一次反応）。一次反応では、濃度 $[\mathrm{A}]$ と時間 $t$ の間に $[\mathrm{A}]=[\mathrm{A}]_0e^{-kt}$（$[\mathrm{A}]_0$ は $t=0$ の濃度）が成り立つ。$\log_e2=0.693$ とする。<br>(1) 0〜300 秒の間の $\mathrm{N_2O_5}$ の平均の分解速度を求めよ。<br>(2) 表から、濃度が半分になるのにかかる時間（半減期）を読み取り、それが濃度によらず一定であることを確かめよ。<br>(3) 半減期と速度定数 $k$ の関係式を導き、$k$ を有効数字2桁で求めよ。<br>(4) 1200 秒までに発生した $\mathrm{O_2}$ の物質量を求めよ。<br>(5) $\mathrm{N_2O_5}$ の濃度が 0.0500 mol/L になるのは何秒後か。<br>(6) この反応は、化学反応式の係数が2であるのに一次反応である。このことから、反応速度式についてどのようなことがいえるか。",
  "a": r"(1) $7.8\times10^{-4}\ \mathrm{mol/(L\cdot s)}$　(2) 600 秒（0.800 → 0.400 も 0.400 → 0.200 も 600 秒、0.566 → 0.283 も 600 秒）　(3) $k=\dfrac{\log_e2}{t_{1/2}}$、$k=1.2\times10^{-3}\ /\mathrm{s}$　(4) 0.300 mol　(5) 2400 秒後　(6) 反応速度式の次数は化学反応式の係数とは一致するとは限らず、実験で決まる。",
  "s": r"(1) $\dfrac{0.800-0.566}{300}=7.8\times10^{-4}\ \mathrm{mol/(L\cdot s)}$。(3) $[\mathrm{A}]=\frac12[\mathrm{A}]_0$ となる時間 $t_{1/2}$ では $\frac12=e^{-kt_{1/2}}$、$kt_{1/2}=\log_e2$。$k=\dfrac{0.693}{600}=1.155\times10^{-3}\fallingdotseq1.2\times10^{-3}\ /\mathrm{s}$。初期濃度によらず半減期が一定なのは一次反応の特徴。参考：(1) の速度を平均濃度 $\frac{0.800+0.566}{2}=0.683$ で割っても $1.14\times10^{-3}$ となり、$1.155\times10^{-3}$ に近い値が得られる。(4) 分解した $\mathrm{N_2O_5}$ は $(0.800-0.200)\times1.0=0.600\ \mathrm{mol}$。係数比 $2:1$ より $\mathrm{O_2}$ は 0.300 mol。(5) $0.0500=0.800\times\left(\frac12\right)^4$ なので、半減期4回分で $600\times4=2400$ 秒。(6) $\mathrm{N_2O_5}$ の分解は、1分子が分かれる遅い段階を含むいくつかの段階からなり、その遅い段階が全体の速さを決めている。<br><b>ポイント</b>：一次反応は「半減期が一定」。半減期 $n$ 回で濃度は $\left(\frac12\right)^n$ 倍になる。"},
]}}


def verify():
    items = CH[8]["items"]
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

    # A1
    v = (0.80 - 0.68) / 60; eq(v, 2.0e-3); eq(v / 2, 1.0e-3); eq(v / 0.74, 2.7e-3); assert 2 ** 3 == 8
    # A2 エネルギー図
    assert E_TS - E_PROD == 183 and E_CAT - E_PROD == 58 and E_PROD == -9
    # A3 HI の平衡
    K = (1.6 / 10) ** 2 / ((0.20 / 10) * (0.20 / 10)); eq(K, 64)
    x = 2.0 / (sqrt(K) + 2); eq(x, 0.20); eq(1 / K, 1.6e-2)
    # B1 速度式
    data = [(0.10, 0.10, 2.0e-4), (0.20, 0.10, 8.0e-4), (0.20, 0.30, 2.4e-3)]
    xo = log(data[1][2] / data[0][2]) / log(2); yo = log(data[2][2] / data[1][2]) / log(3)
    assert abs(xo - 2) < 1e-9 and abs(yo - 1) < 1e-9
    k = data[0][2] / (0.10 ** 2 * 0.10); eq(k, 0.20)
    for a, b, vv in data:
        assert abs(k * a * a * b - vv) < 1e-12
    eq(k * 0.30 ** 2 * 0.20, 3.6e-3)
    # B2 アレニウス
    Ea = 0.69 * 8.3 / (1 / 300 - 1 / 310); eq(Ea / 1000, 53)
    Ea_true = log(2) * 8.314 / (1 / 300 - 1 / 310); assert 53e3 < Ea_true < 54e3
    eq(10e3 / (8.3 * 300), 4.0); eq(exp(10e3 / (8.3 * 300)), 55)
    # B3 N2O4
    n4, n2 = 0.50 * 0.60, 0.50 * 0.40 * 2
    Kc = (n2 / 5.0) ** 2 / (n4 / 5.0); eq(Kc, 0.11)
    P = (n4 + n2) * R * 350 / 5.0; eq(P, 4.1e5)
    Kp = (P * n2 / 0.70) ** 2 / (P * n4 / 0.70); eq(Kp, 3.1e5)
    assert abs(Kp - Kc * R * 350) < 1e-6 * Kp
    eq(P * n2 / 0.70, 2.32e5, 3); eq(P * n4 / 0.70, 1.74e5, 3); eq(Kc, 0.107, 3)
    # B4 字数
    assert len(C_B4) <= 60, len(C_B4)
    # B5 PCl5
    Kp5 = 1.2e5
    a3 = sqrt(1 / (1 + 3.6e5 / Kp5)); eq(a3, 0.50)
    a4 = sqrt(1 / (1 + 1.2e5 / Kp5)); eq(a4, 0.71); eq(1.414 / 2, 0.71)
    for a, Pt in [(a3, 3.6e5), (a4, 1.2e5)]:
        assert abs(a * a / (1 - a * a) * Pt - Kp5) < 1e-6 * Kp5
    # C1 アンモニア
    x = 0.50; tot = 4.0 - 2 * x; assert abs(2 * x / tot - 1 / 3) < 1e-12
    Pt = 2.0e7; pn, ph, pa = Pt * (1 - x) / tot, Pt * (3 - 3 * x) / tot, Pt * 2 * x / tot
    eq(pn, 3.3e6); eq(ph, 1.0e7); eq(pa, 6.7e6)
    Kpn = pa ** 2 / (pn * ph ** 3); eq(Kpn, 1.3e-14); assert abs(Kpn - 4 / 3 * 1e-14) < 1e-20
    # 4.0×10^7 Pa：Kp 一定の式を二分法で解いて比べる
    f = lambda x, P: 16 * x * x * (2 - x) ** 2 / (27 * (1 - x) ** 4) - Kpn * P * P
    lo, hi = 0.0, 0.999
    for _ in range(100):
        mid = (lo + hi) / 2
        if f(mid, 4.0e7) < 0:
            lo = mid
        else:
            hi = mid
    xr = lo; u = 1 / sqrt(7)
    assert abs(xr - (1 - u)) < 1e-9 and abs(x * (2 - x) / (1 - x) ** 2 - 3) < 1e-12
    assert round(100 * xr / (2 - xr)) == 45 and round(100 * 1.65 / 3.65) == 45
    # C2 一次反応
    kk = log(2) / 600
    for t, c in N2O5:
        assert abs(0.800 * exp(-kk * t) - c) < 6e-4, (t, c)
    eq((0.800 - 0.566) / 300, 7.8e-4); eq(0.693 / 600, 1.2e-3); eq(0.693 / 600, 1.155e-3, 4)
    eq((0.800 - 0.200) * 1.0 / 2, 0.300, 3); assert abs(0.800 * 0.5 ** 4 - 0.0500) < 1e-12 and 600 * 4 == 2400
    eq((0.800 - 0.566) / 300 / ((0.800 + 0.566) / 2), 1.14e-3, 3)
