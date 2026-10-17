"""問題集 第1章 運動の表し方。CH に問題、verify() で答えを sympy で検算する。"""
import math
from sympy import *


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) < 0.5 * 10 ** e * (1 - 1e-9), (x, shown, n)


def _eq(a, b):
    assert simplify(a - b) == 0, (a, b)


# ---- 図（座標は計算で出す） ----
def _ln(x1, y1, x2, y2, c="#333", w=1.2, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>'


def _ar(x1, y1, x2, y2, c="#333", w=1.2, hs=6):
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - hs * math.cos(a - 0.4), y2 - hs * math.sin(a - 0.4))
    p2 = (x2 - hs * math.cos(a + 0.4), y2 - hs * math.sin(a + 0.4))
    return (_ln(x1, y1, x2, y2, c, w) +
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>')


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _arc(cx, cy, r, a1, a2, c="#555"):
    """角 a1→a2（度、反時計回り、y 軸は上向きとして）の円弧"""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{c}" stroke-width="1"/>'


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


VT = [(0, 0), (4, 8), (10, 8), (14, 0)]   # 1-4 の v-t グラフの折れ点 (t[s], v[m/s])


def _fig_vt():
    ox, oy, sx, sy = 42, 140, 15, 12
    X = lambda t: ox + sx * t
    Y = lambda v: oy - sy * v
    p = [_ar(X(0), Y(0), X(16.2), Y(0)), _ar(X(0), Y(0), X(0), Y(10.6))]
    p.append(f'<polyline points="{" ".join(f"{X(t):.1f},{Y(v):.1f}" for t, v in VT)}" fill="none" stroke="#1d4e89" stroke-width="2"/>')
    for t in (4, 10):
        p.append(_ln(X(t), Y(0), X(t), Y(8), "#999", 1, "3,2"))
    p.append(_ln(X(0), Y(8), X(4), Y(8), "#999", 1, "3,2"))
    p += [_tx(X(4), Y(0) + 13, "4.0", 10, anchor="middle"), _tx(X(10), Y(0) + 13, "10", 10, anchor="middle"),
          _tx(X(14), Y(0) + 13, "14", 10, anchor="middle"), _tx(X(0) - 5, Y(8) + 4, "8.0", 10, anchor="end"),
          _tx(X(0) - 5, Y(0) + 12, "O", 10, anchor="end"), _tx(X(16.2), Y(0) + 14, "t [s]", 11, anchor="end"),
          _tx(X(0) + 5, Y(10.4), "v [m/s]", 11)]
    return _svg(300, 162, p)


def _fig_slope():
    ox, oy, S = 25, 150, 300.0
    b, th = 30, 60          # 斜面の角、投げ上げの向き（水平から）
    T = 2 / math.sqrt(3)    # v0=g=1 のときの落下時刻
    pts = []
    for i in range(41):
        t = T * i / 40
        x, y = math.cos(math.radians(th)) * t, math.sin(math.radians(th)) * t - t * t / 2
        pts.append(f"{ox + S * x:.1f},{oy - S * y:.1f}")
    lx, ly = ox + S * math.cos(math.radians(th)) * T, oy - S * (math.sin(math.radians(th)) * T - T * T / 2)
    p = [_ln(8, oy, 280, oy, "#333", 1.2),
         _ln(ox, oy, ox + 250 * math.cos(math.radians(b)), oy - 250 * math.sin(math.radians(b)), "#333", 1.6),
         f'<polyline points="{" ".join(pts)}" fill="none" stroke="#1d4e89" stroke-width="1.6" stroke-dasharray="5,3"/>',
         _ar(ox, oy, ox + 58 * math.cos(math.radians(th)), oy - 58 * math.sin(math.radians(th)), "#c0392b", 1.6),
         _arc(ox, oy, 34, 0, b), _arc(ox, oy, 22, b, th),
         _tx(ox + 40, oy - 6, "β", 11, True), _tx(ox + 22, oy - 25, "φ", 11, True),
         _tx(ox + 12, oy - 50, "v₀", 11, True, c="#c0392b", anchor="end"),
         _tx(ox - 4, oy + 13, "O", 11, anchor="middle"),
         f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="2.6" fill="#1d4e89"/>', _tx(lx + 4, ly + 14, "P", 11)]
    return _svg(285, 165, p)


CH = {1: {
"goal": r"等加速度直線運動の3式と $v$-$t$ グラフ（傾き＝加速度、面積＝変位）を使いこなす。相対速度・放物運動は向き（成分）に分けて考える。<br>（特に断りがなければ、数値は有効数字2桁で答え、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$ とする。空気抵抗は無視する。）",
"items": [
 {"lv": "A", "tag": "等加速度直線運動",
  "q": r"$x$ 軸上を正の向きに速さ $4.0\,\mathrm{m/s}$ で進んでいた物体が、時刻 $t=0$ から一定の加速度 $2.0\,\mathrm{m/s^2}$ で $3.0\,\mathrm{s}$ 間加速した。<br>(1) $t=3.0\,\mathrm{s}$ での速度を求めよ。<br>(2) この $3.0\,\mathrm{s}$ 間の変位を求めよ。<br>(3) その後、物体は一定の加速度で減速し、さらに $25\,\mathrm{m}$ 進んで静止した。このときの加速度を求めよ。",
  "a": r"(1) 正の向きに $10\,\mathrm{m/s}$　(2) 正の向きに $21\,\mathrm{m}$　(3) $-2.0\,\mathrm{m/s^2}$（負の向きに大きさ $2.0\,\mathrm{m/s^2}$）",
  "s": r"(1) $v=v_0+at=4.0+2.0\times3.0=10\,\mathrm{m/s}$。<br>(2) $x=v_0t+\frac12at^2=4.0\times3.0+\frac12\times2.0\times3.0^2=21\,\mathrm{m}$。<br>(3) 時間がわからないので $v^2-v_0^2=2ax$ を使う。$0^2-10^2=2a\times25$ より $a=-2.0\,\mathrm{m/s^2}$。<br><b>ポイント</b>：3式のうち、問題に出てこない量（ここでは時間）を含まない式を選ぶ。加速度の符号は向きを表す。"},
 {"lv": "A", "tag": "鉛直投げ上げ",
  "q": r"地面から小球を鉛直上向きに初速 $14\,\mathrm{m/s}$ で投げ上げた。<br>(1) 最高点に達するまでの時間を求めよ。<br>(2) 最高点の地面からの高さを求めよ。<br>(3) 投げてから地面にもどるまでの時間と、もどる直前の速さを求めよ。",
  "a": r"(1) $1.4\,\mathrm{s}$　(2) $10\,\mathrm{m}$　(3) $2.9\,\mathrm{s}$、$14\,\mathrm{m/s}$",
  "s": r"鉛直上向きを正とすると、加速度は $-9.8\,\mathrm{m/s^2}$。<br>(1) 最高点では $v=0$ なので、$0=14-9.8t$ より $t=\frac{14}{9.8}\fallingdotseq1.4\,\mathrm{s}$。<br>(2) $0^2-14^2=2\times(-9.8)\times h$ より $h=10\,\mathrm{m}$。<br>(3) 地面にもどるとき $y=0$ なので、$14t-4.9t^2=0$。$t\neq0$ より $t=\frac{14}{4.9}\fallingdotseq2.9\,\mathrm{s}$。このときの速度は $v=14-9.8\times\frac{14}{4.9}=-14\,\mathrm{m/s}$ で、下向きに速さ $14\,\mathrm{m/s}$。<br><b>ポイント</b>：投げ上げは「初速 $v_0$、加速度 $-g$ の等加速度運動」として1本の式で扱える。上昇と下降は時間も速さも対称になる。"},
 {"lv": "A", "tag": "相対速度",
  "q": r"東向きに $15\,\mathrm{m/s}$ で走る自動車 A に乗った人から見た、次の自動車の速度（相対速度）を求めよ。<br>(1) 西向きに $10\,\mathrm{m/s}$ で走る自動車 B<br>(2) 北向きに $20\,\mathrm{m/s}$ で走る自動車 C（大きさと向き）",
  "a": r"(1) 西向きに $25\,\mathrm{m/s}$　(2) $25\,\mathrm{m/s}$、北から西へ角 $\theta$（$\tan\theta=\frac34$、$\theta\fallingdotseq37^\circ$）の向き",
  "s": r"A から見た相手の速度は $\vec v_{\text{相手}}-\vec v_{\mathrm A}$。<br>(1) 東向きを正として $-10-15=-25\,\mathrm{m/s}$。西向きに $25\,\mathrm{m/s}$。<br>(2) $\vec v_{\mathrm C}-\vec v_{\mathrm A}$ は「北向き $20\,\mathrm{m/s}$」と「西向き $15\,\mathrm{m/s}$」の合成。大きさ $\sqrt{20^2+15^2}=25\,\mathrm{m/s}$、向きは北から西へ $\theta$（$\tan\theta=\frac{15}{20}=\frac34$）。<br><b>ポイント</b>：「自分の速度を逆向きにして相手の速度に足す」と考えると、ベクトルの図がかきやすい。"},
 {"lv": "A", "tag": "v-t グラフ",
  "q": r"直線上を運動する物体の速度 $v$ と時刻 $t$ の関係が図のようになった。<br>" + _fig_vt() +
       r"(1) $0\sim4.0\,\mathrm{s}$ の加速度を求めよ。　(2) $10\sim14\,\mathrm{s}$ の加速度を求めよ。<br>(3) $0\sim14\,\mathrm{s}$ の間に進んだ距離を求めよ。　(4) この $14\,\mathrm{s}$ 間の平均の速さを求めよ。",
  "a": r"(1) $2.0\,\mathrm{m/s^2}$　(2) $-2.0\,\mathrm{m/s^2}$　(3) $80\,\mathrm{m}$　(4) $5.7\,\mathrm{m/s}$",
  "s": r"(1) 傾き $\frac{8.0-0}{4.0}=2.0\,\mathrm{m/s^2}$。<br>(2) 傾き $\frac{0-8.0}{14-10}=-2.0\,\mathrm{m/s^2}$（運動の向きと逆向き）。<br>(3) グラフと $t$ 軸で囲まれた台形の面積：$\frac12\times(14+6.0)\times8.0=80\,\mathrm{m}$。<br>(4) $\frac{80}{14}\fallingdotseq5.7\,\mathrm{m/s}$。<br><b>ポイント</b>：$v$-$t$ グラフの傾きが加速度、面積が変位。$v<0$ の部分があれば、その面積は負の変位として数える。"},
 {"lv": "B", "tag": "水平投射",
  "q": r"高さ $19.6\,\mathrm{m}$ のがけの上から、小石を水平に速さ $7.0\,\mathrm{m/s}$ で投げ出した。<br>(1) 地面に達するまでの時間を求めよ。<br>(2) 投げ出した点の真下から着地点までの水平距離を求めよ。<br>(3) 着地直前の速さを求めよ。<br>(4) 着地直前の速度が水平面となす角を $\theta$ とするとき、$\tan\theta$ を求めよ。",
  "a": r"(1) $2.0\,\mathrm{s}$　(2) $14\,\mathrm{m}$　(3) $21\,\mathrm{m/s}$　(4) $2.8$",
  "s": r"水平方向は速さ $7.0\,\mathrm{m/s}$ の等速直線運動、鉛直方向は自由落下。<br>(1) $19.6=\frac12\times9.8\,t^2$ より $t=2.0\,\mathrm{s}$。<br>(2) $7.0\times2.0=14\,\mathrm{m}$。<br>(3) 鉛直成分 $v_y=9.8\times2.0=19.6\,\mathrm{m/s}$。$v=\sqrt{7.0^2+19.6^2}\fallingdotseq21\,\mathrm{m/s}$。<br>(4) $\tan\theta=\frac{v_y}{v_x}=\frac{19.6}{7.0}=2.8$。<br><b>ポイント</b>：落下時間は高さだけで決まり、水平方向の初速によらない。水平と鉛直は別々に式を立てる。"},
 {"lv": "B", "tag": "斜方投射",
  "q": r"水平な地面上の点から、小球を速さ $v_0$、水平となす角 $\theta$（$0^\circ<\theta<90^\circ$）で投げ上げた。重力加速度の大きさを $g$ とする。<br>(1) 最高点に達するまでの時間と、最高点の高さ $H$ を求めよ。<br>(2) 地面に落ちるまでの水平到達距離 $R$ を求めよ。<br>(3) $v_0$ を一定にして $\theta$ を変えるとき、$R$ が最大になる $\theta$ と、そのときの $\frac RH$ の値を求めよ。<br>(4) $R$ が最大値の半分になる $\theta$ をすべて求めよ。",
  "a": r"(1) $\frac{v_0\sin\theta}{g}$、$H=\frac{v_0^2\sin^2\theta}{2g}$　(2) $R=\frac{v_0^2\sin2\theta}{g}$　(3) $\theta=45^\circ$、$\frac RH=4$　(4) $\theta=15^\circ,\ 75^\circ$",
  "s": r"初速度の成分は、水平 $v_0\cos\theta$、鉛直 $v_0\sin\theta$。<br>(1) 速度の鉛直成分が $0$ になる時刻 $t_1=\frac{v_0\sin\theta}{g}$。$0^2-(v_0\sin\theta)^2=-2gH$ より $H=\frac{v_0^2\sin^2\theta}{2g}$。<br>(2) 落下するまでの時間は対称性から $2t_1$。$R=v_0\cos\theta\cdot\frac{2v_0\sin\theta}{g}=\frac{v_0^2\sin2\theta}{g}$。<br>(3) $\sin2\theta=1$ すなわち $\theta=45^\circ$ で最大 $R=\frac{v_0^2}{g}$。このとき $H=\frac{v_0^2}{2g}\cdot\frac12=\frac{v_0^2}{4g}$ なので $\frac RH=4$。<br>(4) $\sin2\theta=\frac12$、$0^\circ<2\theta<180^\circ$ より $2\theta=30^\circ,\ 150^\circ$。<br><b>ポイント</b>：$R$ は $\sin2\theta$ に比例するので、$\theta$ と $90^\circ-\theta$ で同じ距離になる。"},
 {"lv": "B", "tag": "相対速度",
  "q": r"川幅 $120\,\mathrm{m}$、流れの速さ $3.0\,\mathrm{m/s}$ のまっすぐな川を、静水での速さが $5.0\,\mathrm{m/s}$ の船で渡る。流れの速さは川のどこでも同じとする。<br>(1) 船首を岸に垂直な向きに向けて進むとき、対岸に着くまでの時間と、その間に下流へ流される距離を求めよ。<br>(2) 出発点の真向かいの点に着くには、船首をどの向きに向ければよいか。また、そのとき対岸に着くまでの時間を求めよ。",
  "a": r"(1) $24\,\mathrm{s}$、$72\,\mathrm{m}$　(2) 岸に垂直な向きから上流側へ角 $\theta$（$\sin\theta=\frac35$、$\theta\fallingdotseq37^\circ$）、$30\,\mathrm{s}$",
  "s": r"岸から見た船の速度＝（水に対する船の速度）＋（流れの速度）。<br>(1) 岸に垂直な成分は $5.0\,\mathrm{m/s}$ なので $t=\frac{120}{5.0}=24\,\mathrm{s}$。この間に流れによって $3.0\times24=72\,\mathrm{m}$ 下流へ移動する。<br>(2) 合成速度を岸に垂直にするには、船の速度の上流向きの成分 $5.0\sin\theta$ が流れの $3.0\,\mathrm{m/s}$ を打ち消せばよい。$\sin\theta=\frac35$。このとき岸に垂直な成分は $5.0\cos\theta=5.0\times\frac45=4.0\,\mathrm{m/s}$ なので $t=\frac{120}{4.0}=30\,\mathrm{s}$。<br><b>ポイント</b>：「最短時間」なら船首を岸に垂直に、「真向かいに着く（最短距離）」なら合成速度を岸に垂直に。条件が違うことに注意。"},
 {"lv": "B", "tag": "2物体の出会い",
  "q": r"高さ $20\,\mathrm{m}$ のビルの屋上から小球 A を静かに放すと同時に、その真下の地面から小球 B を初速 $v_0$ で鉛直上向きに投げ上げたところ、2球は空中で出会った。<br>(1) 投げてから出会うまでの時間を $v_0$ を用いて表せ。<br>(2) B が上昇中に A と出会うための $v_0$ の条件を求めよ。<br>(3) $v_0=20\,\mathrm{m/s}$ のとき、出会う点の地面からの高さを求めよ。",
  "a": r"(1) $\frac{20}{v_0}$（$v_0$ は $\mathrm{m/s}$ の数値、時間は $\mathrm s$）　(2) $v_0>14\,\mathrm{m/s}$　(3) $15\,\mathrm{m}$",
  "s": r"A から見た B の運動（相対運動）を考える。A も B も加速度は下向き $g$ なので、相対加速度は $0$。B は A から見て、初めの距離 $20\,\mathrm{m}$ を速さ $v_0$ で等速で近づいてくる。<br>(1) $t=\frac{20}{v_0}$。<br>(2) B が最高点に達する時刻 $\frac{v_0}{g}$ より前に出会えばよい。$\frac{20}{v_0}<\frac{v_0}{9.8}$ より $v_0^2>196$、$v_0>14\,\mathrm{m/s}$。<br>(3) $t=\frac{20}{20}=1.0\,\mathrm{s}$。この間に A は $\frac12\times9.8\times1.0^2=4.9\,\mathrm{m}$ 落ちるので、高さは $20-4.9\fallingdotseq15\,\mathrm{m}$。<br><b>ポイント</b>：重力だけを受けて運動する物体どうしは、互いに相手から見ると等速直線運動をしている。"},
 {"lv": "B", "tag": "v-t グラフの活用",
  "q": r"駅 P を発車した電車が、一定の加速度 $1.0\,\mathrm{m/s^2}$ で速さ $20\,\mathrm{m/s}$ まで加速し、しばらく等速で走ったのち、一定の加速度で減速して、減速を始めてから $25\,\mathrm{s}$ 後に駅 Q に停車した。PQ 間の距離は $1850\,\mathrm{m}$ である。<br>(1) 減速中の加速度の大きさを求めよ。<br>(2) 加速している間と減速している間に進んだ距離をそれぞれ求めよ。<br>(3) P から Q までの所要時間を求めよ。<br>(4) P から Q までの平均の速さを求めよ。",
  "a": r"(1) $0.80\,\mathrm{m/s^2}$　(2) 加速中 $200\,\mathrm{m}$、減速中 $250\,\mathrm{m}$　(3) $115\,\mathrm{s}$　(4) $16\,\mathrm{m/s}$",
  "s": r"$v$-$t$ グラフは台形になる。<br>(1) $\frac{20}{25}=0.80\,\mathrm{m/s^2}$。<br>(2) 加速にかかる時間は $\frac{20}{1.0}=20\,\mathrm{s}$。距離は三角形の面積で、加速中 $\frac12\times20\times20=200\,\mathrm{m}$、減速中 $\frac12\times25\times20=250\,\mathrm{m}$。<br>(3) 等速で走る距離は $1850-200-250=1400\,\mathrm{m}$、時間は $\frac{1400}{20}=70\,\mathrm{s}$。合計 $20+70+25=115\,\mathrm{s}$。<br>(4) $\frac{1850}{115}\fallingdotseq16\,\mathrm{m/s}$。<br><b>ポイント</b>：加速・等速・減速が続く運動は、$v$-$t$ グラフをかいて面積で距離を求めるのが速い。"},
 {"lv": "C", "tag": "放物運動の重ね合わせ",
  "q": r"水平な地面上の点 O から、水平距離 $L$、高さ $H$ の点に小球 P を支えておく。時刻 $0$ に P を静かに放すと同時に、O から小球 Q を、P のある向き（直線 OP の向き）に速さ $v_0$ で投げ出した。重力加速度の大きさを $g$ とする。<br>(1) 重力がないとしたときの P, Q の運動と比べることにより、P が地面に落ちる前であれば Q は必ず P に命中することを示せ。<br>(2) 命中するまでの時間を求めよ。<br>(3) P が地面に落ちる前に命中するための $v_0$ の条件を求めよ。<br>(4) $L=30\,\mathrm{m}$、$H=40\,\mathrm{m}$ のとき、(3) の条件を数値で表せ。",
  "a": r"(1) 解説参照　(2) $\frac{\sqrt{L^2+H^2}}{v_0}$　(3) $v_0>\sqrt{\frac{g(L^2+H^2)}{2H}}$　(4) $v_0>17.5\,\mathrm{m/s}$",
  "s": r"(1) 重力がなければ、P は静止したまま、Q は直線 OP 上を等速で進むので、時刻 $t_1=\frac{\sqrt{L^2+H^2}}{v_0}$ に P の位置に達する。重力があると、P, Q はどちらも「重力がないときの位置」から鉛直下向きに $\frac12gt^2$ だけずれる。同じ時刻のずれは2球で等しいので、時刻 $t_1$ に2球は同じ点にあり、命中する。<br>(2) $t_1=\frac{\sqrt{L^2+H^2}}{v_0}$。<br>(3) 時刻 $t_1$ での P の高さが正であればよい。$H-\frac12g\,t_1^2>0$ より $v_0^2>\frac{g(L^2+H^2)}{2H}$。<br>(4) $v_0^2>\frac{9.8\times(30^2+40^2)}{2\times40}=306.25$ より $v_0>17.5\,\mathrm{m/s}$。<br><b>ポイント</b>：放物運動は「初速度の向きの等速直線運動」と「自由落下」の重ね合わせ。同時に動き出した物体の自由落下の部分は等しいので、相対的には直線運動になる。"},
 {"lv": "C", "tag": "斜面への斜方投射",
  "q": r"図のように、傾斜角 $\beta=30^\circ$ の斜面の下端 O から、小球を斜面を含む鉛直面内で、斜面となす角 $\varphi$ の向きに速さ $v_0$ で投げ上げたところ、小球は斜面上の点 P に落ちた。重力加速度の大きさを $g$ とし、斜面に沿って上向きに $x$ 軸、斜面に垂直上向きに $y$ 軸をとる。<br>" + _fig_slope() +
       r"(1) 小球の加速度の $x$ 成分と $y$ 成分を求めよ。<br>(2) 投げてから P に落ちるまでの時間 $T$ と、OP 間の距離 $\ell$ を $v_0,\ g,\ \varphi$ で表せ。<br>(3) $v_0$ を一定にして $\varphi$ を変えるとき、$\ell$ が最大になる $\varphi$ と、$\ell$ の最大値を求めよ。<br>(4) 小球が斜面に垂直に衝突するための $\tan\varphi$ の値を求めよ。",
  "a": r"(1) $x$ 成分 $-\frac g2$、$y$ 成分 $-\frac{\sqrt3}{2}g$　(2) $T=\frac{4v_0\sin\varphi}{\sqrt3\,g}$、$\ell=\frac{8v_0^2\sin\varphi\cos(\varphi+30^\circ)}{3g}$　(3) $\varphi=30^\circ$、$\frac{2v_0^2}{3g}$　(4) $\tan\varphi=\frac{\sqrt3}{2}$",
  "s": r"(1) 重力加速度を斜面方向と垂直方向に分解する。$a_x=-g\sin30^\circ=-\frac g2$、$a_y=-g\cos30^\circ=-\frac{\sqrt3}{2}g$。<br>(2) $y$ 方向：初速 $v_0\sin\varphi$、加速度 $-\frac{\sqrt3}{2}g$。$y=0$ にもどる時刻は $T=\frac{2v_0\sin\varphi}{\frac{\sqrt3}{2}g}=\frac{4v_0\sin\varphi}{\sqrt3\,g}$。<br>$x$ 方向：$\ell=v_0\cos\varphi\cdot T-\frac12\cdot\frac g2T^2=\frac{4v_0^2\sin\varphi\cos\varphi}{\sqrt3\,g}-\frac{4v_0^2\sin^2\varphi}{3g}=\frac{4v_0^2\sin\varphi}{3g}(\sqrt3\cos\varphi-\sin\varphi)$。$\sqrt3\cos\varphi-\sin\varphi=2\cos(\varphi+30^\circ)$ より $\ell=\frac{8v_0^2\sin\varphi\cos(\varphi+30^\circ)}{3g}$。<br>(3) 積和の公式 $2\sin\varphi\cos(\varphi+30^\circ)=\sin(2\varphi+30^\circ)-\sin30^\circ$ より $\ell=\frac{4v_0^2}{3g}\left\{\sin(2\varphi+30^\circ)-\frac12\right\}$。$2\varphi+30^\circ=90^\circ$、すなわち $\varphi=30^\circ$（水平から $60^\circ$）で最大値 $\frac{4v_0^2}{3g}\cdot\frac12=\frac{2v_0^2}{3g}$。<br>(4) 斜面に垂直に衝突するのは、時刻 $T$ で速度の $x$ 成分が $0$ のとき。$v_0\cos\varphi-\frac g2T=0$ に $T$ を代入して $v_0\cos\varphi=\frac{2v_0\sin\varphi}{\sqrt3}$、$\tan\varphi=\frac{\sqrt3}{2}$。<br><b>ポイント</b>：斜面が関係する放物運動は、斜面に沿った軸と垂直な軸をとると「斜面に落ちる＝$y=0$」が簡単に書ける。そのかわり、両方向に加速度の成分がある。"},
]}}


def verify():
    g = Rational(98, 10)
    # 1-1
    v = 4 + 2 * 3
    assert v == 10 and 4 * 3 + Rational(1, 2) * 2 * 9 == 21
    a = symbols("a")
    assert solve(Eq(0 - v ** 2, 2 * a * 25), a) == [-2]
    # 1-2
    t1 = 14 / g
    _near(t1, 1.4); assert 14 ** 2 / (2 * g) == 10
    t2 = solve(14 * symbols("t") - g / 2 * symbols("t") ** 2, symbols("t"))
    T = max(t2); _near(T, 2.9); assert 14 - g * T == -14
    # 1-3
    assert sqrt(20 ** 2 + 15 ** 2) == 25
    _near(math.degrees(math.atan(15 / 20)), 37)
    # 1-4 v-t グラフ（台形の面積）
    area = sum((VT[i + 1][0] - VT[i][0]) * (VT[i + 1][1] + VT[i][1]) / 2 for i in range(3))
    assert area == 80 and (VT[1][1] - VT[0][1]) / (VT[1][0] - VT[0][0]) == 2 and (VT[3][1] - VT[2][1]) / (VT[3][0] - VT[2][0]) == -2
    _near(area / 14, 5.7)
    # 1-5 水平投射
    t = sqrt(2 * Rational(196, 10) / g)
    assert t == 2 and 7 * t == 14
    vy = g * t
    _near(sqrt(49 + vy ** 2), 21); assert vy / 7 == Rational(28, 10)
    # 1-6 斜方投射
    v0, gg, th = symbols("v0 g theta", positive=True)
    t1 = v0 * sin(th) / gg
    H = v0 * sin(th) * t1 - gg * t1 ** 2 / 2
    _eq(H, v0 ** 2 * sin(th) ** 2 / (2 * gg))
    R = v0 * cos(th) * 2 * t1
    _eq(R, v0 ** 2 * sin(2 * th) / gg)
    _eq((R / H).subs(th, pi / 4), 4)
    sols = solve(Eq(sin(2 * th), Rational(1, 2)), th)
    assert set(sols) == {pi / 12, 5 * pi / 12}
    # 1-7 川
    assert Rational(120, 5) == 24 and 3 * 24 == 72
    s = Rational(3, 5); c = sqrt(1 - s ** 2)
    assert 5 * c == 4 and 120 / (5 * c) == 30
    _near(math.degrees(math.asin(0.6)), 37)
    # 1-8 出会い：A の位置 20 - g t^2/2、B の位置 v0 t - g t^2/2
    tt, vv = symbols("t v", positive=True)
    tm = solve(Eq(20 - g * tt ** 2 / 2, vv * tt - g * tt ** 2 / 2), tt)[0]
    _eq(tm, 20 / vv)
    vmin = solve(Eq(tm, vv / g), vv)[0]
    assert vmin == 14
    _near(20 - g * tm.subs(vv, 20) ** 2 / 2, 15)
    # 1-9 電車
    ta = Rational(20, 1); xa = Rational(1, 2) * 20 * ta; xd = Rational(1, 2) * 25 * 20
    assert Rational(20, 25) == Rational(8, 10) and xa == 200 and xd == 250
    tc = (1850 - xa - xd) / 20
    assert tc == 70 and ta + tc + 25 == 115
    _near(Rational(1850, 115), 16)
    # 1-10 命中
    L, Hh, V = symbols("L H v0", positive=True)
    D = sqrt(L ** 2 + Hh ** 2)
    t1 = D / V
    cos_a, sin_a = L / D, Hh / D
    # Q の位置と P の位置が時刻 t1 で一致
    xq, yq = V * cos_a * t1, V * sin_a * t1 - gg * t1 ** 2 / 2
    assert simplify(xq - L) == 0 and simplify(yq - (Hh - gg * t1 ** 2 / 2)) == 0
    cond = solve(Eq(Hh - gg * t1 ** 2 / 2, 0), V)
    _eq(cond[0], sqrt(gg * (L ** 2 + Hh ** 2) / (2 * Hh)))
    assert cond[0].subs({gg: g, L: 30, Hh: 40}) == Rational(35, 2)
    # 1-11 斜面への投射（x, y 軸を斜面方向に）
    ph = symbols("phi", positive=True)
    b = pi / 6
    ax, ay = -gg * sin(b), -gg * cos(b)
    T = 2 * v0 * sin(ph) / (-ay)
    _eq(T, 4 * v0 * sin(ph) / (sqrt(3) * gg))
    ell = v0 * cos(ph) * T + ax * T ** 2 / 2
    _eq(ell, 8 * v0 ** 2 * sin(ph) * cos(ph + pi / 6) / (3 * gg))
    dl = diff(ell, ph)
    assert simplify(dl.subs(ph, pi / 6)) == 0
    _eq(ell.subs(ph, pi / 6), 2 * v0 ** 2 / (3 * gg))
    # 水平・鉛直の座標でも落下点が斜面上にあり距離が一致することを確認（数値）
    for phv in (0.3, pi / 6, 0.8):
        thv = float(phv) + math.pi / 6
        Tn = float(T.subs({v0: 1, gg: 1, ph: phv}))
        X, Y = math.cos(thv) * Tn, math.sin(thv) * Tn - Tn ** 2 / 2
        assert abs(Y - X * math.tan(math.pi / 6)) < 1e-12
        assert abs(math.hypot(X, Y) - float(ell.subs({v0: 1, gg: 1, ph: phv}))) < 1e-12
    tp = solve(Eq(v0 * cos(ph) + ax * T, 0), ph)
    assert any(simplify(tan(s_) - sqrt(3) / 2) == 0 for s_ in tp)
