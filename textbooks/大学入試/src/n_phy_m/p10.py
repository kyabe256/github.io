"""問題集 第10章 気体の状態変化と熱力学。CH に問題、verify() で答えを sympy で検算する。"""
import math
from sympy import *


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) < 0.5 * 10 ** e * (1 - 1e-9), (x, shown, n)


def _eq(a, b):
    assert simplify(a - b) == 0, (a, b)


# ---- p-V グラフ（座標は計算で出す） ----
def _ln(x1, y1, x2, y2, c="#333", w=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def _head(x, y, ang, c, hs=7):
    p1 = (x - hs * math.cos(ang - 0.4), y - hs * math.sin(ang - 0.4))
    p2 = (x - hs * math.cos(ang + 0.4), y - hs * math.sin(ang + 0.4))
    return f'<polygon points="{x:.1f},{y:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>'


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _pv(pts, names, vt, pt, vmax, pmax, vlab="V", plab="p", w=250, h=172, offs=None):
    ox, oy = 44, h - 26
    sx, sy = (w - 80) / vmax, (h - 46) / pmax
    X = lambda v: ox + sx * v
    Y = lambda p: oy - sy * p
    s = [f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
         _ln(ox, oy, w - 14, oy), _head(w - 14, oy, 0, "#333"), _ln(ox, oy, ox, 10), _head(ox, 10, -math.pi / 2, "#333"),
         _tx(w - 14, oy + 16, vlab, 11, anchor="end"), _tx(ox + 6, 14, plab, 11), _tx(ox - 5, oy + 13, "O", 10, anchor="end")]
    for v, lab in vt:
        s += [_ln(X(v), oy, X(v), Y(max(p for vv, p in pts if abs(vv - v) < 1e-9) if any(abs(vv - v) < 1e-9 for vv, p in pts) else 0), "#aaa", 0.8, "3,2"),
              _tx(X(v), oy + 14, lab, 10, anchor="middle")]
    for p, lab in pt:
        s += [_ln(ox, Y(p), X(min(v for v, pp in pts if abs(pp - p) < 1e-9)), Y(p), "#aaa", 0.8, "3,2"),
              _tx(ox - 5, Y(p) + 4, lab, 10, anchor="end")]
    n = len(pts)
    path = " ".join(f"{X(v):.1f},{Y(p):.1f}" for v, p in pts)
    s.append(f'<polygon points="{path}" fill="#e8eef8" stroke="#1d4e89" stroke-width="1.8"/>')
    for i in range(n):
        (v1, p1), (v2, p2) = pts[i], pts[(i + 1) % n]
        mx, my = (X(v1) + X(v2)) / 2, (Y(p1) + Y(p2)) / 2
        ang = math.atan2(Y(p2) - Y(p1), X(v2) - X(v1))
        s.append(_head(mx + 4 * math.cos(ang), my + 4 * math.sin(ang), ang, "#1d4e89"))
    offs = offs or [(-10, 14)] * n
    for (v, p), nm, (dx, dy) in zip(pts, names, offs):
        s += [f'<circle cx="{X(v):.1f}" cy="{Y(p):.1f}" r="2.6" fill="#1d4e89"/>', _tx(X(v) + dx, Y(p) + dy, nm, 11)]
    s.append("</svg>")
    return "".join(s)


FIG_A4 = _pv([(1, 1), (1, 3), (4, 3), (4, 1)], "ABCD", [(1, "1.0"), (4, "4.0")], [(1, "1.0"), (3, "3.0")], 4.6, 3.6,
             offs=[(-12, 14), (-12, -4), (4, -4), (4, 14)])
FIG_B3 = _pv([(1, 1), (1, 2), (3, 2), (3, 1)], "ABCD", [(1, "V₀"), (3, "3V₀")], [(1, "p₀"), (2, "2p₀")], 3.6, 2.5,
             offs=[(-12, 14), (-12, -4), (4, -4), (4, 14)])
FIG_C1 = _pv([(1, 1), (1, 3), (3, 1)], "ABC", [(1, "V₀"), (3, "3V₀")], [(1, "p₀"), (3, "3p₀")], 3.6, 3.5,
             offs=[(-12, 14), (-12, -4), (4, -4)])


CH = {10: {
"goal": r"熱力学第1法則 $\Delta U=Q+W$（$Q$：気体が吸収した熱、$W$：気体がされた仕事）。単原子分子理想気体では $\Delta U=\frac32nR\Delta T$。仕事は $p$-$V$ グラフの面積、断熱変化は $pV^{\gamma}=$ 一定、熱効率は $e=\frac{W_{\text{正味}}}{Q_{\text{吸収}}}$。<br>（数値は有効数字2桁、気体定数 $R=8.31\,\mathrm{J/(mol\cdot K)}$ とする。気体はすべて理想気体とする。）",
"items": [
 {"lv": "A", "tag": "熱力学第1法則",
  "q": r"(1) 気体に $500\,\mathrm{J}$ の熱を与えたところ、気体は外部に $200\,\mathrm{J}$ の仕事をした。気体の内部エネルギーの変化を求めよ。<br>(2) 気体を断熱的に圧縮し、外部から $150\,\mathrm{J}$ の仕事をした。内部エネルギーの変化を求めよ。また、気体の温度は上がるか、下がるか。<br>(3) 気体が等温変化をして、外部に $300\,\mathrm{J}$ の仕事をした。気体が吸収した熱量を求めよ。",
  "a": r"(1) $+300\,\mathrm{J}$（増加）　(2) $+150\,\mathrm{J}$、上がる　(3) $300\,\mathrm{J}$",
  "s": r"(1) された仕事は $W=-200\,\mathrm{J}$。$\Delta U=Q+W=500-200=300\,\mathrm{J}$。<br>(2) 断熱なので $Q=0$。$\Delta U=0+150=150\,\mathrm{J}$。理想気体の内部エネルギーは温度だけで決まるので、温度は上がる。<br>(3) 等温なので $\Delta U=0$。$0=Q+(-300)$ より $Q=300\,\mathrm{J}$。<br><b>ポイント</b>：「した仕事」と「された仕事」は符号が逆。理想気体では「温度一定 ⇔ $\Delta U=0$」。"},
 {"lv": "A", "tag": "定圧変化",
  "q": r"単原子分子理想気体 $2.0\,\mathrm{mol}$ を、圧力を一定に保って $300\,\mathrm{K}$ から $400\,\mathrm{K}$ に温めた。<br>(1) 気体が外部にした仕事を求めよ。<br>(2) 内部エネルギーの変化を求めよ。<br>(3) 気体が吸収した熱量を求めよ。",
  "a": r"(1) $1.7\times10^3\,\mathrm{J}$　(2) $2.5\times10^3\,\mathrm{J}$　(3) $4.2\times10^3\,\mathrm{J}$",
  "s": r"(1) 定圧では $W_{\text{した}}=p\Delta V=nR\Delta T=2.0\times8.31\times100\fallingdotseq1.7\times10^3\,\mathrm{J}$。<br>(2) $\Delta U=\frac32nR\Delta T=\frac32\times1662\fallingdotseq2.5\times10^3\,\mathrm{J}$。<br>(3) $Q=\Delta U+W_{\text{した}}=\frac52nR\Delta T=4155\fallingdotseq4.2\times10^3\,\mathrm{J}$。<br><b>ポイント</b>：定圧変化では、吸収した熱の一部（単原子分子では $\frac25$）が外部への仕事に使われる。"},
 {"lv": "A", "tag": "モル比熱",
  "q": r"単原子分子理想気体について答えよ。<br>(1) 定積モル比熱 $C_V$ と定圧モル比熱 $C_p$ を $R$ で表せ。<br>(2) 比熱比 $\gamma=\frac{C_p}{C_V}$ を求めよ。<br>(3) $1.0\,\mathrm{mol}$ の温度を、体積一定で $10\,\mathrm{K}$ 上げるのに必要な熱量と、圧力一定で $10\,\mathrm{K}$ 上げるのに必要な熱量を求めよ。",
  "a": r"(1) $C_V=\frac32R$、$C_p=\frac52R$　(2) $\frac53$　(3) $1.2\times10^2\,\mathrm{J}$、$2.1\times10^2\,\mathrm{J}$",
  "s": r"(1) 定積では仕事をしないので $Q=\Delta U=\frac32nR\Delta T$、$C_V=\frac32R$。定圧では仕事 $nR\Delta T$ の分だけ多く必要で $C_p=C_V+R=\frac52R$。<br>(2) $\gamma=\frac{5/2}{3/2}=\frac53$。<br>(3) 体積一定：$1.0\times\frac32\times8.31\times10\fallingdotseq1.2\times10^2\,\mathrm{J}$。圧力一定：$1.0\times\frac52\times8.31\times10\fallingdotseq2.1\times10^2\,\mathrm{J}$。<br><b>ポイント</b>：$C_p-C_V=R$（マイヤーの関係）は、単原子分子に限らず理想気体で成り立つ。"},
 {"lv": "A", "tag": "p-V グラフと仕事",
  "q": r"一定量の気体の状態を、図のように A→B→C→D→A と変化させた。A→B と C→D は定積変化、B→C と D→A は定圧変化である。横軸は体積 $V$（単位 $10^{-3}\,\mathrm{m^3}$）、縦軸は圧力 $p$（単位 $10^5\,\mathrm{Pa}$）の目盛りである。<br>" + FIG_A4 +
       r"(1) B→C で気体が外部にした仕事を求めよ。<br>(2) D→A で気体が外部にした仕事を求めよ。<br>(3) 1サイクルで気体が外部にした正味の仕事を求めよ。",
  "a": r"(1) $9.0\times10^2\,\mathrm{J}$　(2) $-3.0\times10^2\,\mathrm{J}$（外部から $3.0\times10^2\,\mathrm{J}$ の仕事をされた）　(3) $6.0\times10^2\,\mathrm{J}$",
  "s": r"(1) $p\Delta V=3.0\times10^5\times(4.0-1.0)\times10^{-3}=9.0\times10^2\,\mathrm{J}$。<br>(2) $1.0\times10^5\times(1.0-4.0)\times10^{-3}=-3.0\times10^2\,\mathrm{J}$。<br>(3) 定積変化では仕事は $0$。正味の仕事は $900-300=6.0\times10^2\,\mathrm{J}$（長方形の面積）。<br><b>ポイント</b>：$p$-$V$ グラフで時計回りのサイクルは、囲まれた面積だけ外部に正の仕事をする（熱機関）。"},
 {"lv": "B", "tag": "断熱変化",
  "q": r"単原子分子理想気体 $1.0\,\mathrm{mol}$（比熱比 $\gamma=\frac53$）を、温度 $400\,\mathrm{K}$ の状態から断熱的にゆっくり膨張させ、体積を8倍にした。<br>(1) 膨張後の温度を求めよ。<br>(2) 膨張後の圧力は、初めの圧力の何倍か。<br>(3) この間に気体が外部にした仕事を求めよ。",
  "a": r"(1) $1.0\times10^2\,\mathrm{K}$　(2) $\frac{1}{32}$ 倍　(3) $3.7\times10^3\,\mathrm{J}$",
  "s": r"(1) 断熱変化では $TV^{\gamma-1}=$ 一定（$\gamma-1=\frac23$）。$T=400\times\left(\frac18\right)^{\frac23}=400\times\frac14=100\,\mathrm{K}$。<br>(2) $pV^{\gamma}=$ 一定より $\left(\frac18\right)^{\frac53}=\frac1{32}$ 倍。<br>(3) $Q=0$ なので、した仕事＝内部エネルギーの減少：$\frac32\times1.0\times8.31\times(400-100)\fallingdotseq3.7\times10^3\,\mathrm{J}$。<br><b>ポイント</b>：断熱膨張では、外部への仕事を内部エネルギーでまかなうので温度が下がる。仕事は $\Delta U$ から求めると速い。"},
 {"lv": "B", "tag": "真空への膨張と断熱膨張",
  "q": r"断熱材でできた容器を仕切り板で体積の等しい2つの部屋に分け、一方に温度 $T_0$、圧力 $p_0$ の単原子分子理想気体を入れ、他方は真空にした。<br>(1) 仕切り板を急に取り除いた。十分時間がたった後の気体の温度と圧力を求めよ。<br>(2) 同じ初めの状態から、今度は仕切り板の代わりになめらかに動く断熱ピストンを使い、ピストンを外から支えながらゆっくり動かして、気体の体積を2倍にした。このときの圧力を $p_0$ で表し、$T_0=300\,\mathrm{K}$ として温度を求めよ（$2^{\frac23}=1.59$ とする）。<br>(3) (1) と (2) で温度が異なる理由を説明せよ。",
  "a": r"(1) $T_0$、$\frac{p_0}{2}$　(2) $0.31p_0$、$1.9\times10^2\,\mathrm{K}$　(3) 解説参照",
  "s": r"(1) 真空中への膨張では、気体は何も押さないので仕事をしない（$W=0$）。断熱なので $Q=0$。よって $\Delta U=0$ で温度は $T_0$ のまま。体積が2倍なので $p=\frac{p_0}{2}$。<br>(2) ゆっくりした断熱膨張なので $pV^{\frac53}=$ 一定：$p=\frac{p_0}{2^{5/3}}=\frac{p_0}{2\times1.59}\fallingdotseq0.31p_0$。$TV^{\frac23}=$ 一定：$T=\frac{300}{1.59}\fallingdotseq1.9\times10^2\,\mathrm{K}$。<br>(3) (2) では気体がピストンを押して外部に正の仕事をし、断熱なのでその分だけ内部エネルギーが減る。(1) では仕事をしないので内部エネルギーは変わらない。<br><b>ポイント</b>：「断熱」でも、外部に仕事をするかどうかで温度変化が違う。真空への膨張（自由膨張）は $pV^{\gamma}=$ 一定に従わない。"},
 {"lv": "B", "tag": "熱機関の効率",
  "q": r"単原子分子理想気体を、図の A→B→C→D→A のサイクルで変化させる。A は $(V_0,\ p_0)$、B は $(V_0,\ 2p_0)$、C は $(3V_0,\ 2p_0)$、D は $(3V_0,\ p_0)$ である。<br>" + FIG_B3 +
       r"(1) 各過程で気体が吸収する熱量を $p_0V_0$ で表せ（放出する場合は負とする）。<br>(2) 1サイクルで気体がした正味の仕事を求めよ。<br>(3) このサイクルの熱効率を求めよ。",
  "a": r"(1) A→B：$\frac32p_0V_0$、B→C：$10p_0V_0$、C→D：$-\frac92p_0V_0$、D→A：$-5p_0V_0$　(2) $2p_0V_0$　(3) $\frac{4}{23}\fallingdotseq0.17$",
  "s": r"単原子分子では $U=\frac32nRT=\frac32pV$。<br>A→B（定積）：$Q=\Delta U=\frac32(2p_0V_0-p_0V_0)=\frac32p_0V_0$。<br>B→C（定圧）：$\Delta U=\frac32(6-2)p_0V_0=6p_0V_0$、した仕事 $2p_0\times2V_0=4p_0V_0$、$Q=10p_0V_0$。<br>C→D（定積）：$Q=\frac32(3-6)p_0V_0=-\frac92p_0V_0$。<br>D→A（定圧）：$\Delta U=\frac32(1-3)p_0V_0=-3p_0V_0$、した仕事 $-2p_0V_0$、$Q=-5p_0V_0$。<br>(2) 長方形の面積 $p_0\times2V_0=2p_0V_0$（熱の総和 $\frac32+10-\frac92-5=2$ とも一致）。<br>(3) 吸収した熱は $Q_{\text{吸収}}=\frac32+10=\frac{23}{2}p_0V_0$。$e=\frac{2}{23/2}=\frac4{23}\fallingdotseq0.17$。<br><b>ポイント</b>：熱効率の分母は「吸収した熱だけの和」。放出した熱を差し引いた正味の熱ではない。"},
 {"lv": "B", "tag": "マイヤーの関係",
  "q": r"物質量 $n$ の理想気体について考える。<br>(1) 体積一定で温度を $\Delta T$ 上げるのに必要な熱量を、定積モル比熱 $C_V$ で表せ。また、このときの内部エネルギーの変化を求めよ。<br>(2) 圧力一定で温度を $\Delta T$ 上げるとき、気体がする仕事と吸収する熱量を $n,\ R,\ C_V,\ \Delta T$ で表せ。ただし、理想気体の内部エネルギーは温度だけで決まることを用いよ。<br>(3) 定圧モル比熱 $C_p$ と $C_V$ の関係を求めよ。<br>(4) 二原子分子の理想気体では、常温で $C_V=\frac52R$ である。比熱比 $\gamma$ を求めよ。",
  "a": r"(1) $nC_V\Delta T$、$\Delta U=nC_V\Delta T$　(2) 仕事 $nR\Delta T$、熱量 $n(C_V+R)\Delta T$　(3) $C_p=C_V+R$　(4) $\frac75=1.4$",
  "s": r"(1) 体積一定では仕事は $0$ なので $Q=\Delta U=nC_V\Delta T$。<br>(2) 仕事は $p\Delta V=nR\Delta T$（状態方程式）。内部エネルギーは温度だけで決まるので、定圧でも同じ $\Delta T$ なら $\Delta U=nC_V\Delta T$。$Q=\Delta U+p\Delta V=n(C_V+R)\Delta T$。<br>(3) $nC_p\Delta T=n(C_V+R)\Delta T$ より $C_p=C_V+R$。<br>(4) $C_p=\frac72R$、$\gamma=\frac{7/2}{5/2}=\frac75=1.4$。<br><b>ポイント</b>：「内部エネルギーは温度だけの関数」なので、どんな変化でも $\Delta U=nC_V\Delta T$ が使える。"},
 {"lv": "B", "tag": "直線的な変化",
  "q": r"単原子分子理想気体 $1\,\mathrm{mol}$ の状態を、$p$-$V$ グラフ上で原点を通る直線にそって、状態 A $(V_0,\ p_0)$ から状態 B $(2V_0,\ 2p_0)$ までゆっくり変化させた。<br>(1) 気体が外部にした仕事を求めよ。<br>(2) 内部エネルギーの変化を求めよ。<br>(3) 気体が吸収した熱量を求めよ。<br>(4) この変化のモル比熱（$1\,\mathrm{mol}$ の温度を $1\,\mathrm{K}$ 上げるのに必要な熱量）を $R$ で表せ。",
  "a": r"(1) $\frac32p_0V_0$　(2) $\frac92p_0V_0$　(3) $6p_0V_0$　(4) $2R$",
  "s": r"(1) 台形の面積：$\frac12(p_0+2p_0)\times V_0=\frac32p_0V_0$。<br>(2) $\Delta U=\frac32\Delta(pV)=\frac32(4p_0V_0-p_0V_0)=\frac92p_0V_0$。<br>(3) $Q=\Delta U+W_{\text{した}}=6p_0V_0$。<br>(4) $\Delta T=\frac{\Delta(pV)}{R}=\frac{3p_0V_0}{R}$。モル比熱は $\frac{Q}{\Delta T}=\frac{6p_0V_0}{3p_0V_0/R}=2R$。<br><b>ポイント</b>：モル比熱は変化のしかたで変わる（定積 $\frac32R$、定圧 $\frac52R$、この変化は $2R$）。"},
 {"lv": "C", "tag": "三角形のサイクル",
  "q": r"単原子分子理想気体 $1\,\mathrm{mol}$ を、$p$-$V$ グラフ上の3点 A $(V_0,\ p_0)$、B $(V_0,\ 3p_0)$、C $(3V_0,\ p_0)$ を結ぶ A→B（定積）→C（直線）→A（定圧）のサイクルで変化させる。A の温度を $T_0$ とする。<br>" + FIG_C1 +
       r"(1) A→B、C→A で気体が吸収する熱量を $p_0V_0$ で表せ（放出は負）。<br>(2) B→C の過程全体で、気体がする仕事、内部エネルギーの変化、吸収する熱量（正味）を求めよ。<br>(3) B→C の途中で温度が最も高くなる点の体積と、その温度を $T_0$ で表せ。<br>(4) B→C の途中、体積が $V$ から $V+\Delta V$（$\Delta V$ は微小）に変わる間に気体が吸収する熱量 $\Delta Q$ を、$x=\frac{V}{V_0}$ を用いて表せ（$\Delta V$ の2乗の項は無視する）。これを用いて、B→C で熱の吸収が放出に変わる点の体積を求めよ。<br>(5) このサイクルの熱効率を求めよ。",
  "a": r"(1) A→B：$3p_0V_0$、C→A：$-5p_0V_0$　(2) 仕事 $4p_0V_0$、$\Delta U=0$、熱量 $4p_0V_0$　(3) $2V_0$、$4T_0$　(4) $\Delta Q=p_0(10-4x)\Delta V$、$\frac52V_0$　(5) $\frac4{15}\fallingdotseq0.27$",
  "s": r"$U=\frac32pV$、$p_0V_0=RT_0$。直線 BC は $p=p_0(4-x)$（$x=\frac V{V_0}$）。<br>(1) A→B：$\frac32(3-1)p_0V_0=3p_0V_0$。C→A（定圧圧縮）：$\Delta U=\frac32(1-3)p_0V_0=-3p_0V_0$、した仕事 $p_0(V_0-3V_0)=-2p_0V_0$、$Q=-5p_0V_0$。<br>(2) 仕事は台形の面積 $\frac12(3p_0+p_0)\times2V_0=4p_0V_0$。B と C はどちらも $pV=3p_0V_0$ なので $\Delta U=0$。$Q=4p_0V_0$。<br>(3) $pV=p_0V_0(4x-x^2)=p_0V_0\{4-(x-2)^2\}$ は $x=2$ で最大 $4p_0V_0$。体積 $2V_0$、温度 $4T_0$。<br>(4) $\Delta Q=\Delta U+p\Delta V=\frac32\Delta(pV)+p\Delta V$。$\Delta(pV)\fallingdotseq p\Delta V+V\Delta p$、直線上では $\Delta p=-\frac{p_0}{V_0}\Delta V$ なので $\Delta(pV)=p_0(4-2x)\Delta V$。よって $\Delta Q=\frac32p_0(4-2x)\Delta V+p_0(4-x)\Delta V=p_0(10-4x)\Delta V$。$\Delta V>0$ なので、$x<\frac52$ で吸収、$x>\frac52$ で放出。変わる点の体積は $\frac52V_0$。<br>（温度が最高の点 $2V_0$ を過ぎても、しばらくは熱を吸収している。）<br>(5) B から $x=\frac52$ の点 M までに吸収する熱：M は $p=\frac32p_0$、$V=\frac52V_0$ で $pV=\frac{15}{4}p_0V_0$。$\Delta U=\frac32\left(\frac{15}{4}-3\right)p_0V_0=\frac98p_0V_0$、仕事（台形）$\frac12\left(3+\frac32\right)p_0\times\frac32V_0=\frac{27}{8}p_0V_0$。吸収 $\frac98+\frac{27}8=\frac92p_0V_0$。<br>サイクルで吸収する熱は $3+\frac92=\frac{15}{2}p_0V_0$、正味の仕事は三角形の面積 $\frac12\times2V_0\times2p_0=2p_0V_0$。$e=\frac{2}{15/2}=\frac4{15}\fallingdotseq0.27$。<br><b>ポイント</b>：直線変化の途中では吸熱と放熱が入れかわることがある。正味の熱量 $4p_0V_0$ を吸収熱として効率を計算すると誤り（$\frac{2}{7}$ になってしまう）。"},
 {"lv": "C", "tag": "断熱変化を含むサイクル",
  "q": r"単原子分子理想気体 $n\,\mathrm{mol}$（$\gamma=\frac53$）を、次のサイクルで変化させる。状態 A（体積 $V_1$、温度 $T_A$）から断熱圧縮して体積 $V_2=\frac{V_1}{8}$ の状態 B にし、B から体積一定で加熱して状態 C にし、C から断熱膨張して体積 $V_1$ の状態 D にし、D から体積一定で冷却して A にもどす。<br>(1) 状態 B の温度 $T_B$ を $T_A$ で表せ。<br>(2) 状態 C の温度が $T_C=8T_A$ のとき、状態 D の温度 $T_D$ を求めよ。<br>(3) B→C で吸収する熱量 $Q_1$、D→A で放出する熱量 $Q_2$、1サイクルの正味の仕事 $W$ を $nRT_A$ で表せ。<br>(4) 熱効率を求めよ。また、一般に圧縮比 $\varepsilon=\frac{V_1}{V_2}$ の場合の熱効率を $\varepsilon$ で表し、$T_C$ によらないことを示せ。",
  "a": r"(1) $4T_A$　(2) $2T_A$　(3) $Q_1=6nRT_A$、$Q_2=\frac32nRT_A$、$W=\frac92nRT_A$　(4) $\frac34$、$e=1-\varepsilon^{-\frac23}$",
  "s": r"断熱変化では $TV^{\gamma-1}=TV^{\frac23}=$ 一定。<br>(1) $T_B=T_A\left(\frac{V_1}{V_2}\right)^{\frac23}=8^{\frac23}T_A=4T_A$。<br>(2) $T_D=T_C\left(\frac{V_2}{V_1}\right)^{\frac23}=\frac{8T_A}{4}=2T_A$。<br>(3) 定積変化では $Q=\frac32nR\Delta T$。$Q_1=\frac32nR(8-4)T_A=6nRT_A$、$Q_2=\frac32nR(2-1)T_A=\frac32nRT_A$。断熱過程では熱の出入りがないので $W=Q_1-Q_2=\frac92nRT_A$。<br>(4) $e=\frac{W}{Q_1}=\frac{9/2}{6}=\frac34$。一般に $T_B=\varepsilon^{\frac23}T_A$、$T_C=\varepsilon^{\frac23}T_D$ なので $e=1-\frac{Q_2}{Q_1}=1-\frac{T_D-T_A}{T_C-T_B}=1-\frac{T_D-T_A}{\varepsilon^{2/3}(T_D-T_A)}=1-\varepsilon^{-\frac23}$。$T_C$ を含まない。<br><b>ポイント</b>：2本の断熱線が同じ体積比で結ばれていると、$\frac{T_B}{T_A}=\frac{T_C}{T_D}$ が成り立つ。これがガソリンエンジンのモデル（オットーサイクル）で、効率は圧縮比で決まる。"},
]}}


def verify():
    R = Rational(831, 100)
    # 10-1
    assert 500 - 200 == 300 and 0 + 150 == 150
    # 10-2
    W = 2 * R * 100
    _near(W, 1.7e3); _near(Rational(3, 2) * W, 2.5e3); _near(Rational(5, 2) * W, 4.2e3)
    # 10-3
    assert Rational(5, 2) / Rational(3, 2) == Rational(5, 3)
    _near(Rational(3, 2) * R * 10, 1.2e2); _near(Rational(5, 2) * R * 10, 2.1e2)
    # 10-4
    assert 3 * 10 ** 5 * 3 * Rational(1, 1000) == 900 and 10 ** 5 * (-3) * Rational(1, 1000) == -300
    # 10-5
    T = 400 * Rational(1, 8) ** Rational(2, 3)
    assert T == 100 and Rational(1, 8) ** Rational(5, 3) == Rational(1, 32)
    _near(Rational(3, 2) * R * 300, 3.7e3)
    # 10-6
    _near(1 / (2 * 1.59), 0.31); _near(300 / 1.59, 1.9e2)
    _near(1 / 2 ** (5 / 3), 0.31); _near(300 / 2 ** (2 / 3), 1.9e2)
    # 10-7 長方形サイクル（U=3/2 pV、単位 p0V0）
    pts = [(1, 1), (1, 2), (3, 2), (3, 1)]
    Qs = []
    for i in range(4):
        (v1, p1), (v2, p2) = pts[i], pts[(i + 1) % 4]
        dU = Rational(3, 2) * (p2 * v2 - p1 * v1)
        Wd = Rational(p1 + p2, 2) * (v2 - v1)
        Qs.append(dU + Wd)
    assert Qs == [Rational(3, 2), 10, Rational(-9, 2), -5] and sum(Qs) == 2
    e = 2 / sum(q for q in Qs if q > 0)
    assert e == Rational(4, 23); _near(e, 0.17)
    # 10-8
    assert Rational(7, 2) / Rational(5, 2) == Rational(7, 5)
    # 10-9
    W = Rational(1, 2) * (1 + 2) * 1
    dU = Rational(3, 2) * (4 - 1)
    assert W == Rational(3, 2) and dU == Rational(9, 2) and W + dU == 6 and (W + dU) / 3 == 2
    # 10-10 三角形サイクル：B→C を積分で確認
    x = symbols("x")
    p = 4 - x                       # 単位 p0
    dQ = Rational(3, 2) * diff(p * x, x) + p      # dQ/dx（単位 p0V0）
    _eq(dQ, 10 - 4 * x)
    assert solve(dQ, x) == [Rational(5, 2)]
    assert solve(diff(p * x, x), x) == [2] and (p * x).subs(x, 2) == 4
    Qab = Rational(3, 2) * (3 - 1)
    Qca = Rational(3, 2) * (1 - 3) + (1 - 3) * 1
    assert Qab == 3 and Qca == -5
    Qbc = integrate(dQ, (x, 1, 3))
    assert Qbc == 4 and integrate(p, (x, 1, 3)) == 4
    Qin = Qab + integrate(dQ, (x, 1, Rational(5, 2)))
    assert integrate(dQ, (x, 1, Rational(5, 2))) == Rational(9, 2)
    assert Rational(3, 2) * (Rational(15, 4) - 3) + Rational(1, 2) * (3 + Rational(3, 2)) * Rational(3, 2) == Rational(9, 2)
    assert Qab + Qbc + Qca == 2
    e = 2 / Qin
    assert e == Rational(4, 15); _near(e, 0.27); assert 2 / (Qab + Qbc) == Rational(2, 7)
    # 10-11 オットーサイクル
    TA, n, Rs, eps = symbols("T_A n R epsilon", positive=True)
    TB = TA * 8 ** Rational(2, 3); _eq(TB, 4 * TA)
    TC = 8 * TA; TD = TC * Rational(1, 8) ** Rational(2, 3); _eq(TD, 2 * TA)
    Q1 = Rational(3, 2) * n * Rs * (TC - TB); Q2 = Rational(3, 2) * n * Rs * (TD - TA)
    _eq(Q1, 6 * n * Rs * TA); _eq(Q2, Rational(3, 2) * n * Rs * TA); _eq(Q1 - Q2, Rational(9, 2) * n * Rs * TA)
    _eq((Q1 - Q2) / Q1, Rational(3, 4))
    TDs = symbols("T_D", positive=True)
    eg = 1 - (TDs - TA) / (eps ** Rational(2, 3) * TDs - eps ** Rational(2, 3) * TA)
    _eq(eg, 1 - eps ** Rational(-2, 3))
    assert (1 - eps ** Rational(-2, 3)).subs(eps, 8) == Rational(3, 4)
