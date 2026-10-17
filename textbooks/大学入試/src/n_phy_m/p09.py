"""問題集 第9章 熱と気体の分子運動。CH に問題、verify() で答えを sympy で検算する。"""
import math
from sympy import *


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) < 0.5 * 10 ** e * (1 - 1e-9), (x, shown, n)


def _eq(a, b):
    assert simplify(a - b) == 0, (a, b)


def _ln(x1, y1, x2, y2, c="#333", w=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _spring(x1, x2, y, n=8, amp=5):
    pts = [(x1, y), (x1 + 4, y)]
    w = (x2 - x1 - 8) / n
    for i in range(n):
        pts.append((x1 + 4 + w * (i + 0.5), y + (amp if i % 2 == 0 else -amp)))
    pts += [(x2 - 4, y), (x2, y)]
    return f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="#333" stroke-width="1.1"/>'


def _fig_spring_piston():
    x0, x1, y0, y1, px, wx = 20, 178, 34, 90, 108, 246
    ym = (y0 + y1) / 2
    s = [f'<svg class="fig" width="262" height="112" viewBox="0 0 262 112">',
         f'<rect x="{x0}" y="{y0}" width="{px - x0}" height="{y1 - y0}" fill="#eef3fa" stroke="none"/>',
         _ln(x0, y0, x1, y0, "#333", 2), _ln(x0, y1, x1, y1, "#333", 2), _ln(x0, y0, x0, y1, "#333", 2),
         f'<rect x="{px}" y="{y0 + 1}" width="8" height="{y1 - y0 - 2}" fill="#999" stroke="#333" stroke-width="1"/>',
         _spring(px + 8, wx, ym, 10), _ln(wx, y0 - 6, wx, y1 + 6, "#333", 1.6)]
    for yy in range(y0 - 4, y1 + 6, 8):
        s.append(_ln(wx, yy, wx + 6, yy - 6, "#777", 0.8))
    s += [_tx((x0 + px) / 2, ym + 4, "気体", 11, anchor="middle"), _ln(x0, y1 + 10, px, y1 + 10, "#777", 0.8),
          _tx((x0 + px) / 2, y1 + 22, "L", 11, True, anchor="middle"), _tx(px + 4, y0 - 6, "ピストン", 10),
          _tx(190, y1 + 16, "大気 p₀", 10), '</svg>']
    return "".join(s)


CH = {9: {
"goal": r"熱量 $Q=mc\Delta T$ と熱量の保存、理想気体の状態方程式 $pV=nRT$。気体分子運動論で圧力を分子の運動に結びつけ、「分子の平均運動エネルギー $\frac32kT$」「単原子分子の内部エネルギー $U=\frac32nRT$」を導く。<br>（数値は有効数字2桁。気体定数 $R=8.31\,\mathrm{J/(mol\cdot K)}$、水の比熱 $4.2\,\mathrm{J/(g\cdot K)}$、重力加速度の大きさ $9.8\,\mathrm{m/s^2}$ とする。気体はすべて理想気体とする。）",
"items": [
 {"lv": "A", "tag": "熱量と比熱",
  "q": r"(1) 質量 $200\,\mathrm{g}$ の水の温度を $20\,{}^\circ\mathrm{C}$ から $80\,{}^\circ\mathrm{C}$ に上げるのに必要な熱量を求めよ。<br>(2) この水の熱容量を求めよ。<br>(3) 消費電力 $500\,\mathrm{W}$ のヒーターで発生する熱がすべて水に与えられるとすると、(1) の加熱に何秒かかるか。",
  "a": r"(1) $5.0\times10^4\,\mathrm{J}$　(2) $8.4\times10^2\,\mathrm{J/K}$　(3) $1.0\times10^2\,\mathrm{s}$",
  "s": r"(1) $Q=mc\Delta T=200\times4.2\times60=5.04\times10^4\fallingdotseq5.0\times10^4\,\mathrm{J}$。<br>(2) $C=mc=200\times4.2=840\fallingdotseq8.4\times10^2\,\mathrm{J/K}$。<br>(3) $t=\frac{5.04\times10^4}{500}\fallingdotseq1.0\times10^2\,\mathrm{s}$。<br><b>ポイント</b>：比熱は「1 g を 1 K 上げる熱量」、熱容量は「その物体全体を 1 K 上げる熱量」。温度差は ℃ でも K でも同じ値。"},
 {"lv": "A", "tag": "熱平衡",
  "q": r"熱は外部に逃げず、容器の熱容量は無視できるものとする。<br>(1) $80\,{}^\circ\mathrm{C}$ の水 $100\,\mathrm{g}$ と $20\,{}^\circ\mathrm{C}$ の水 $200\,\mathrm{g}$ を混ぜたときの温度を求めよ。<br>(2) $100\,{}^\circ\mathrm{C}$ に熱した質量 $100\,\mathrm{g}$ の金属球を、$20\,{}^\circ\mathrm{C}$ の水 $200\,\mathrm{g}$ に入れたところ、全体が $25\,{}^\circ\mathrm{C}$ になった。この金属の比熱を求めよ。",
  "a": r"(1) $40\,{}^\circ\mathrm{C}$　(2) $0.56\,\mathrm{J/(g\cdot K)}$",
  "s": r"高温の物体が失った熱量＝低温の物体が得た熱量（熱量の保存）。<br>(1) $100\times4.2\times(80-t)=200\times4.2\times(t-20)$ より $80-t=2t-40$、$t=40\,{}^\circ\mathrm{C}$。<br>(2) $100\times c\times(100-25)=200\times4.2\times(25-20)$ より $c=\frac{4200}{7500}=0.56\,\mathrm{J/(g\cdot K)}$。<br><b>ポイント</b>：式は「失った熱＝得た熱」の形にして、温度差を正の量で書くと符号ミスをしない。"},
 {"lv": "A", "tag": "状態方程式",
  "q": r"(1) $0.50\,\mathrm{mol}$ の気体を、$27\,{}^\circ\mathrm{C}$ で体積 $1.0\times10^{-2}\,\mathrm{m^3}$ の容器に入れたときの圧力を求めよ。<br>(2) 体積を一定に保って $127\,{}^\circ\mathrm{C}$ にしたときの圧力を求めよ。<br>(3) (1) の状態から温度を一定に保って体積を $\frac12$ にしたときの圧力を求めよ。",
  "a": r"(1) $1.2\times10^5\,\mathrm{Pa}$　(2) $1.7\times10^5\,\mathrm{Pa}$　(3) $2.5\times10^5\,\mathrm{Pa}$",
  "s": r"温度は絶対温度に直す：$27\,{}^\circ\mathrm{C}=300\,\mathrm{K}$、$127\,{}^\circ\mathrm{C}=400\,\mathrm{K}$。<br>(1) $p=\frac{nRT}{V}=\frac{0.50\times8.31\times300}{1.0\times10^{-2}}\fallingdotseq1.2\times10^5\,\mathrm{Pa}$。<br>(2) 体積一定では $p\propto T$ なので $1.246\times10^5\times\frac{400}{300}\fallingdotseq1.7\times10^5\,\mathrm{Pa}$。<br>(3) 温度一定では $pV$ 一定（ボイルの法則）：$1.246\times10^5\times2\fallingdotseq2.5\times10^5\,\mathrm{Pa}$。<br><b>ポイント</b>：状態方程式・シャルルの法則では必ず絶対温度 $T\,[\mathrm K]$ を使う。"},
 {"lv": "A", "tag": "分子の速さと内部エネルギー",
  "q": r"アボガドロ定数を $N_A$ とする。<br>(1) 絶対温度 $T$ の気体の分子1個の平均運動エネルギーを、$R,\ N_A,\ T$ で表せ。<br>(2) 窒素分子（モル質量 $2.8\times10^{-2}\,\mathrm{kg/mol}$）の $300\,\mathrm{K}$ での2乗平均速度 $\sqrt{\overline{v^2}}$ を求めよ。<br>(3) 同じ温度のヘリウム（モル質量 $4.0\times10^{-3}\,\mathrm{kg/mol}$）の2乗平均速度は、窒素の何倍か。<br>(4) $1.0\,\mathrm{mol}$ の単原子分子理想気体の、$300\,\mathrm{K}$ での内部エネルギーを求めよ。",
  "a": r"(1) $\frac{3RT}{2N_A}$　(2) $5.2\times10^2\,\mathrm{m/s}$　(3) $\sqrt7\fallingdotseq2.6$ 倍　(4) $3.7\times10^3\,\mathrm{J}$",
  "s": r"(1) $\frac12m\overline{v^2}=\frac32kT=\frac{3RT}{2N_A}$（$k=\frac{R}{N_A}$ はボルツマン定数）。<br>(2) 両辺に $N_A$ をかけると $\frac12M\overline{v^2}=\frac32RT$（$M=mN_A$ はモル質量）。$\sqrt{\overline{v^2}}=\sqrt{\frac{3RT}{M}}=\sqrt{\frac{3\times8.31\times300}{2.8\times10^{-2}}}\fallingdotseq5.2\times10^2\,\mathrm{m/s}$。<br>(3) $\sqrt{\overline{v^2}}\propto\frac{1}{\sqrt M}$ なので $\sqrt{\frac{28}{4.0}}=\sqrt7\fallingdotseq2.6$ 倍。<br>(4) $U=\frac32nRT=\frac32\times1.0\times8.31\times300\fallingdotseq3.7\times10^3\,\mathrm{J}$。<br><b>ポイント</b>：同じ温度なら分子の平均運動エネルギーは気体の種類によらない。軽い分子ほど速い。"},
 {"lv": "B", "tag": "気体分子運動論",
  "q": r"一辺 $L$ の立方体の容器に、質量 $m$ の分子が $N$ 個入っている。分子どうしは衝突せず、壁とは弾性衝突するものとする。速度の $x$ 成分が $v_x$ の1個の分子について考える。<br>(1) $x$ 軸に垂直な壁 S に1回衝突するとき、壁 S が分子から受ける力積の大きさを求めよ。<br>(2) この分子が単位時間あたりに壁 S に衝突する回数を求めよ。<br>(3) この分子が壁 S に及ぼす平均の力の大きさを求めよ。<br>(4) 分子の速さの2乗の平均を $\overline{v^2}$ とし、$\overline{v_x^2}=\frac13\overline{v^2}$ が成り立つとして、気体の圧力 $p$ を $N,\ m,\ \overline{v^2},\ V$（$V=L^3$）で表せ。<br>(5) 状態方程式 $pV=nRT$（$n=\frac N{N_A}$）と比べて、分子1個の平均運動エネルギーを、ボルツマン定数 $k=\frac{R}{N_A}$ と $T$ で表せ。",
  "a": r"(1) $2mv_x$　(2) $\frac{v_x}{2L}$　(3) $\frac{mv_x^2}{L}$　(4) $p=\frac{Nm\overline{v^2}}{3V}$　(5) $\frac12m\overline{v^2}=\frac32kT$",
  "s": r"(1) 弾性衝突で $v_x$ が $-v_x$ になるので、分子の運動量の変化は $-2mv_x$。壁が受ける力積はその反作用で $2mv_x$。<br>(2) 次に壁 S に当たるまでに $x$ 方向に $2L$ 進むので、衝突の時間間隔は $\frac{2L}{v_x}$、単位時間あたりの回数は $\frac{v_x}{2L}$。<br>(3) 単位時間あたりの力積が平均の力：$2mv_x\times\frac{v_x}{2L}=\frac{mv_x^2}{L}$。<br>(4) $N$ 個分の力は $\frac{Nm\overline{v_x^2}}{L}=\frac{Nm\overline{v^2}}{3L}$。面積 $L^2$ で割って $p=\frac{Nm\overline{v^2}}{3L^3}=\frac{Nm\overline{v^2}}{3V}$。<br>(5) $pV=\frac13Nm\overline{v^2}=\frac{N}{N_A}RT$ より $\frac12m\overline{v^2}=\frac32\cdot\frac{R}{N_A}T=\frac32kT$。<br><b>ポイント</b>：「1回の力積 × 単位時間の回数 ＝ 平均の力」が分子運動論の核心。温度は分子の平均運動エネルギーの目安である。"},
 {"lv": "B", "tag": "つながった容器",
  "q": r"容積 $2.0\,\mathrm{L}$ の容器 A と容積 $3.0\,\mathrm{L}$ の容器 B が、コックのついた細い管でつながれている（管の容積は無視する）。初めコックは閉じていて、A には $3.0\times10^5\,\mathrm{Pa}$、B には $1.0\times10^5\,\mathrm{Pa}$ の同じ種類の気体が入っており、温度はどちらも $300\,\mathrm{K}$ である。<br>(1) コックを開き、温度を $300\,\mathrm{K}$ に保ったときの圧力を求めよ。<br>(2) その後、コックを開いたまま、A を $400\,\mathrm{K}$、B を $300\,\mathrm{K}$ に保ったときの圧力を求めよ。<br>(3) (2) のとき、A と B に入っている気体の物質量の比を求めよ。",
  "a": r"(1) $1.8\times10^5\,\mathrm{Pa}$　(2) $2.0\times10^5\,\mathrm{Pa}$　(3) $1:2$",
  "s": r"物質量は $n=\frac{pV}{RT}$ で、全体の物質量は保存される。<br>(1) 温度が同じなので $pV$ の和が保存：$p\times5.0=3.0\times10^5\times2.0+1.0\times10^5\times3.0$ より $p=1.8\times10^5\,\mathrm{Pa}$。<br>(2) 圧力は共通の $p'$。$\frac{p'\times2.0}{R\times400}+\frac{p'\times3.0}{R\times300}=\frac{1.8\times10^5\times5.0}{R\times300}$ より $p'(0.0050+0.010)=3.0\times10^3$、$p'=2.0\times10^5\,\mathrm{Pa}$。<br>(3) $n_A:n_B=\frac{2.0}{400}:\frac{3.0}{300}=1:2$。<br><b>ポイント</b>：コックでつながれた容器は「圧力が等しい」「全物質量が一定」の2条件で解く。体積の単位は両辺でそろっていれば L のままでよい。"},
 {"lv": "B", "tag": "ピストンとシリンダー",
  "q": r"断面積 $S=1.0\times10^{-2}\,\mathrm{m^2}$ のシリンダーを鉛直に立て、なめらかに動く質量 $M=10\,\mathrm{kg}$ のピストンで気体を閉じこめた。大気圧は $p_0=1.0\times10^5\,\mathrm{Pa}$ である。初め、気体の温度は $300\,\mathrm{K}$、シリンダーの底からピストンまでの距離は $0.30\,\mathrm{m}$ であった。<br>(1) 気体の圧力を求めよ。<br>(2) 気体を $360\,\mathrm{K}$ まで温めたときの、底からピストンまでの距離を求めよ。<br>(3) 初めの状態にもどし、温度を $300\,\mathrm{K}$ に保ったまま、シリンダーをゆっくり上下逆さにした（ピストンは外れないものとする）。このときの気体の圧力と、底からピストンまでの距離を求めよ。",
  "a": r"(1) $1.1\times10^5\,\mathrm{Pa}$　(2) $0.36\,\mathrm{m}$　(3) $9.0\times10^4\,\mathrm{Pa}$、$0.37\,\mathrm{m}$",
  "s": r"(1) ピストンのつりあい：$pS=p_0S+Mg$ より $p=p_0+\frac{Mg}{S}=1.0\times10^5+\frac{98}{1.0\times10^{-2}}=1.098\times10^5\fallingdotseq1.1\times10^5\,\mathrm{Pa}$。<br>(2) ピストンが自由に動くので圧力は一定。体積は $T$ に比例：$0.30\times\frac{360}{300}=0.36\,\mathrm{m}$。<br>(3) 逆さにすると、ピストンの重さは気体を引き伸ばす向きにはたらく：$p'S+Mg=p_0S$ より $p'=p_0-\frac{Mg}{S}=9.02\times10^4\fallingdotseq9.0\times10^4\,\mathrm{Pa}$。温度一定なので $pV$ 一定：$x=0.30\times\frac{1.098}{0.902}\fallingdotseq0.37\,\mathrm{m}$。<br><b>ポイント</b>：ピストンの問題は、まずピストンにはたらく力のつりあいで気体の圧力を決める。"},
 {"lv": "B", "tag": "融解熱を含む熱量の保存",
  "q": r"$0\,{}^\circ\mathrm{C}$ の氷 $50\,\mathrm{g}$ を、$40\,{}^\circ\mathrm{C}$ の水 $300\,\mathrm{g}$ に入れた。氷の融解熱を $3.34\times10^2\,\mathrm{J/g}$ とし、熱は外部に逃げないものとする。<br>(1) 氷がすべてとけて $0\,{}^\circ\mathrm{C}$ の水になるのに必要な熱量を求めよ。<br>(2) $40\,{}^\circ\mathrm{C}$ の水が $0\,{}^\circ\mathrm{C}$ になるまでに放出できる熱量を求め、氷がすべてとけることを確かめよ。<br>(3) 最終的な温度を求めよ。",
  "a": r"(1) $1.7\times10^4\,\mathrm{J}$　(2) $5.0\times10^4\,\mathrm{J}$（(1) より大きいので氷はすべてとける）　(3) $23\,{}^\circ\mathrm{C}$",
  "s": r"(1) $50\times334=1.67\times10^4\fallingdotseq1.7\times10^4\,\mathrm{J}$。<br>(2) $300\times4.2\times40=5.04\times10^4\fallingdotseq5.0\times10^4\,\mathrm{J}$。これは (1) より大きいので、氷はすべてとけ、さらにとけた水の温度も上がる。<br>(3) 最終温度を $t$ とする。水が失った熱 $300\times4.2\times(40-t)$ ＝ 氷がとけるのに使った熱 $16700$ ＋ とけた水 $50\,\mathrm g$ が $0$ から $t$ まで上がる熱 $50\times4.2\times t$。<br>$50400-1260t=16700+210t$ より $t=\frac{33700}{1470}\fallingdotseq23\,{}^\circ\mathrm{C}$。<br><b>ポイント</b>：状態変化があるときは、まず「全部とけるか」を熱量の大小で判断してから式を立てる。とけた水も温度が上がることを忘れない。"},
 {"lv": "B", "tag": "断熱容器での混合",
  "q": r"断熱材で囲まれた容器 A（体積 $2.0\times10^{-2}\,\mathrm{m^3}$）と容器 B（体積 $3.0\times10^{-2}\,\mathrm{m^3}$）が、コックのついた細い管でつながれている。A には $1.0\,\mathrm{mol}$、$300\,\mathrm{K}$ の、B には $2.0\,\mathrm{mol}$、$450\,\mathrm{K}$ の、同じ種類の単原子分子理想気体が入っている。コックを開いて十分に時間がたった。<br>(1) 混合前の気体全体の内部エネルギーを求めよ。<br>(2) 混合後の温度を求めよ。<br>(3) 混合後の圧力を求めよ。",
  "a": r"(1) $1.5\times10^4\,\mathrm{J}$　(2) $400\,\mathrm{K}$　(3) $2.0\times10^5\,\mathrm{Pa}$",
  "s": r"(1) $U=\frac32R(n_AT_A+n_BT_B)=\frac32\times8.31\times(300+900)\fallingdotseq1.5\times10^4\,\mathrm{J}$。<br>(2) 断熱容器で、容器の体積は変わらないので気体は外部と熱も仕事もやりとりしない。内部エネルギーの和が保存される：$\frac32R(1.0\times300+2.0\times450)=\frac32R\times3.0\times T$ より $T=400\,\mathrm{K}$。<br>(3) $p=\frac{nRT}{V}=\frac{3.0\times8.31\times400}{5.0\times10^{-2}}\fallingdotseq2.0\times10^5\,\mathrm{Pa}$。<br><b>ポイント</b>：断熱・体積一定の系では内部エネルギーの和が一定。単原子分子なら $U=\frac32nRT$ なので、混合後の温度は物質量で重みをつけた平均になる。"},
 {"lv": "C", "tag": "球形容器の分子運動論",
  "q": r"半径 $r$ の球形の容器に、質量 $m$ の分子が $N$ 個入っている。分子どうしは衝突せず、壁とは弾性衝突するものとする。ある分子が速さ $v$ で、壁の法線（球の半径方向）と角 $\theta$ をなす向きに壁に衝突した。<br>(1) 1回の衝突で分子が壁に与える力積の大きさを求めよ。<br>(2) この分子は、次の衝突でも同じ角 $\theta$ で壁に当たる。その理由を述べ、衝突から次の衝突までに進む距離と、単位時間あたりの衝突回数を求めよ。<br>(3) この分子が壁全体に及ぼす力の大きさ（時間平均）を求め、それが $\theta$ によらないことを示せ。<br>(4) 気体の圧力 $p$ を、$N,\ m,\ \overline{v^2}$ と容器の体積 $V$ で表し、立方体の容器の場合と一致することを確かめよ。",
  "a": r"(1) $2mv\cos\theta$　(2) 距離 $2r\cos\theta$、回数 $\frac{v}{2r\cos\theta}$　(3) $\frac{mv^2}{r}$　(4) $p=\frac{Nm\overline{v^2}}{3V}$",
  "s": r"(1) 速度の法線成分 $v\cos\theta$ が逆向きになり、接線成分は変わらない。力積の大きさは $2mv\cos\theta$。<br>(2) 弦とその両端への2本の半径がつくる三角形は二等辺三角形なので、弦の両端で半径（法線）となす角は等しい。また、弾性衝突では反射後も法線となす角は $\theta$ のまま。よって、次の衝突でも同じ角 $\theta$ で当たる。弦の長さは $2r\cos\theta$（中心から弦までの距離は $r\sin\theta$）。衝突の時間間隔は $\frac{2r\cos\theta}{v}$、単位時間の回数は $\frac{v}{2r\cos\theta}$。<br>(3) $2mv\cos\theta\times\frac{v}{2r\cos\theta}=\frac{mv^2}{r}$ で、$\theta$ によらない。<br>(4) $N$ 個の分子が壁全体に及ぼす力は $\frac{Nm\overline{v^2}}{r}$。壁の面積 $4\pi r^2$ で割ると $p=\frac{Nm\overline{v^2}}{4\pi r^3}=\frac{Nm\overline{v^2}}{3\cdot\frac43\pi r^3}=\frac{Nm\overline{v^2}}{3V}$。立方体の場合と同じ式になる。<br><b>ポイント</b>：容器の形によらず $pV=\frac13Nm\overline{v^2}$。球形容器では「速度の成分の平均 $\frac13$」を使わずに導ける。"},
 {"lv": "C", "tag": "ばねつきピストン",
  "q": r"断面積 $S=1.0\times10^{-2}\,\mathrm{m^2}$ のシリンダーを水平に置き、なめらかに動くピストンで単原子分子理想気体を閉じこめる。ピストンの外側は大気（圧力 $p_0=1.0\times10^5\,\mathrm{Pa}$）で、ピストンはばね定数 $k=4.0\times10^3\,\mathrm{N/m}$ のばねで外側の壁とつながれている。初め、ばねは自然長、気体の温度は $T_0=300\,\mathrm{K}$、シリンダーの底からピストンまでの距離は $L=0.20\,\mathrm{m}$ であった。気体をゆっくり温めると、ピストンは外側へ移動した。<br>" + _fig_spring_piston() +
       r"(1) ピストンが $x$ だけ移動したときの気体の圧力 $p$ を $x$ の式で表せ（$x$ の単位は $\mathrm m$）。<br>(2) $x=0.10\,\mathrm{m}$ になったときの気体の温度を求めよ。<br>(3) その間の気体の内部エネルギーの変化を求めよ。<br>(4) 気体の圧力 $p$ と体積 $V$ の関係を式で表し、$p$-$V$ グラフがどのような線になるか答えよ。",
  "a": r"(1) $p=1.0\times10^5+4.0\times10^5x\ [\mathrm{Pa}]$　(2) $6.3\times10^2\,\mathrm{K}$　(3) $3.3\times10^2\,\mathrm{J}$　(4) $p=p_0+\frac{k}{S^2}(V-SL)$、右上がりの直線",
  "s": r"(1) ピストンが $x$ 移動すると、ばねは $x$ 縮んでピストンを内向きに $kx$ で押す。ピストンのつりあい：$pS=p_0S+kx$ より $p=p_0+\frac{kx}{S}=1.0\times10^5+4.0\times10^5x$。<br>(2) $x=0.10$ で $p=1.4\times10^5\,\mathrm{Pa}$、$V=S(L+x)=3.0\times10^{-3}\,\mathrm{m^3}$。初めは $p_0V_0=1.0\times10^5\times2.0\times10^{-3}=200\,\mathrm{J}$。$\frac{pV}{T}$ 一定より $T=300\times\frac{1.4\times10^5\times3.0\times10^{-3}}{200}=300\times\frac{420}{200}=630\fallingdotseq6.3\times10^2\,\mathrm{K}$。<br>(3) $U=\frac32nRT=\frac32pV$ なので $\Delta U=\frac32(420-200)=330\fallingdotseq3.3\times10^2\,\mathrm{J}$。<br>(4) $x=\frac{V-SL}{S}$ を代入して $p=p_0+\frac{k}{S^2}(V-SL)$。$V$ の1次式なので、$p$-$V$ グラフは右上がりの直線（傾き $\frac{k}{S^2}=4.0\times10^7\,\mathrm{Pa/m^3}$）。<br><b>ポイント</b>：単原子分子では $U=\frac32nRT=\frac32pV$。物質量がわからなくても $pV$ の値から内部エネルギーが求まる。"},
]}}


def verify():
    g = Rational(98, 10)
    R = Rational(831, 100)
    c = Rational(42, 10)
    # 9-1
    Q = 200 * c * 60
    _near(Q, 5.0e4); _near(200 * c, 8.4e2); _near(Q / 500, 1.0e2)
    # 9-2
    t = symbols("t")
    assert solve(Eq(100 * c * (80 - t), 200 * c * (t - 20)), t) == [40]
    cm = solve(Eq(100 * symbols("c") * 75, 200 * c * 5), symbols("c"))[0]
    assert cm == Rational(56, 100)
    # 9-3
    p1 = Rational(1, 2) * R * 300 / Rational(1, 100)
    _near(p1, 1.2e5); _near(p1 * Rational(4, 3), 1.7e5); _near(p1 * 2, 2.5e5)
    # 9-4
    _near(sqrt(3 * R * 300 / Rational(28, 1000)), 5.2e2); _near(sqrt(7), 2.6); _near(Rational(3, 2) * R * 300, 3.7e3)
    _eq(sqrt(Rational(28, 1000) / Rational(4, 1000)), sqrt(7))
    # 9-5 分子運動論
    m, vx, L, N, v2, NA, Rs, T = symbols("m v_x L N v2 N_A R T", positive=True)
    Fav = 2 * m * vx * vx / (2 * L)
    _eq(Fav, m * vx ** 2 / L)
    p = N * m * (v2 / 3) / L / L ** 2
    _eq(p, N * m * v2 / (3 * L ** 3))
    ke = solve(Eq(p * L ** 3, N / NA * Rs * T), v2)[0] * m / 2
    _eq(ke, Rational(3, 2) * Rs / NA * T)
    # 9-6
    p = symbols("p")
    pa = solve(Eq(p * 5, 3 * 10 ** 5 * 2 + 10 ** 5 * 3), p)[0]
    assert pa == 18 * 10 ** 4
    pb = solve(Eq(p * 2 / 400 + p * 3 / 300, pa * 5 / 300), p)[0]
    assert pb == 2 * 10 ** 5
    assert Rational(2, 400) / Rational(3, 300) == Rational(1, 2)
    # 9-7
    S, M, p0 = Rational(1, 100), 10, 10 ** 5
    pg = p0 + M * g / S
    _near(pg, 1.1e5); assert Rational(3, 10) * Rational(360, 300) == Rational(36, 100)
    pq = p0 - M * g / S
    _near(pq, 9.0e4); _near(Rational(3, 10) * pg / pq, 0.37)
    # 9-8
    Lf = Rational(334)
    _near(50 * Lf, 1.7e4); _near(300 * c * 40, 5.0e4); assert 300 * c * 40 > 50 * Lf
    tf = solve(Eq(300 * c * (40 - t), 50 * Lf + 50 * c * t), t)[0]
    _near(tf, 23)
    # 9-9
    U0 = Rational(3, 2) * R * (1 * 300 + 2 * 450)
    _near(U0, 1.5e4)
    Tf = solve(Eq(U0, Rational(3, 2) * R * 3 * T), T)[0]
    assert Tf == 400
    _near(3 * R * 400 / Rational(5, 100), 2.0e5)
    # 9-10 球形容器
    v, r, th = symbols("v r theta", positive=True)
    chord = 2 * r * cos(th)
    F1 = 2 * m * v * cos(th) * v / chord
    _eq(F1, m * v ** 2 / r)
    pr = N * m * v2 / r / (4 * pi * r ** 2)
    _eq(pr, N * m * v2 / (3 * Rational(4, 3) * pi * r ** 3))
    # 弦の長さ：中心から弦までの距離 r sinθ
    for tv in (0.2, 0.7, 1.3):
        assert abs(2 * math.sqrt(1 - math.sin(tv) ** 2) - 2 * math.cos(tv)) < 1e-12
    # 9-11 ばねつきピストン
    S, k, L, T0 = Rational(1, 100), 4000, Rational(2, 10), 300
    x = symbols("x")
    px = p0 + k * x / S
    _eq(px, 10 ** 5 + 4 * 10 ** 5 * x)
    p1, V1 = px.subs(x, Rational(1, 10)), S * (L + Rational(1, 10))
    T1 = T0 * p1 * V1 / (p0 * S * L)
    assert T1 == 630; _near(T1, 6.3e2)
    dU = Rational(3, 2) * (p1 * V1 - p0 * S * L)
    assert dU == 330
    V = symbols("V")
    _eq(px.subs(x, (V - S * L) / S), p0 + k / S ** 2 * (V - S * L)); assert k / S ** 2 == 4 * 10 ** 7
