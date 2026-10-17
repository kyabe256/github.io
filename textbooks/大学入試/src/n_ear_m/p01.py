"""問題集 第1章 地球の形と内部構造。CH に問題、verify() で数値を Python で検算する。問題はすべて書き下ろし。"""
import math
import re


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) <= 0.5 * 10 ** e * (1 + 1e-9), (x, shown, n)


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


def _tx(x, y, s, size=11, anchor="start", c="#222", it=False):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


# 1-6 の走時（P 波）：地殻 V1、マントル V2、地殻の厚さ H
V1, V2, H = 6.4, 8.0, 30.0
T0 = 2 * H * math.sqrt(1 - (V1 / V2) ** 2) / V1      # 屈折波の切片 [s]
XC = T0 / (1 / V1 - 1 / V2)                          # 折れ曲がりの距離 [km]
X_D = [32, 64, 96, 128, 160]                         # 直接波が初動の観測点
X_H = [240, 280, 320]                                # 屈折波が初動の観測点


def _t(x):
    return min(x / V1, x / V2 + T0)


def _fig_tt():
    ox, oy, sx, sy = 46, 172, 0.8, 3.0
    X = lambda x: ox + sx * x
    Y = lambda t: oy - sy * t
    p = []
    for x in range(40, 321, 40):
        p.append(_ln(X(x), Y(0), X(x), Y(50), "#ddd", 0.8))
    for t in range(10, 51, 10):
        p.append(_ln(X(0), Y(t), X(320), Y(t), "#ddd", 0.8))
    p += [_ar(X(0), Y(0), X(340), Y(0)), _ar(X(0), Y(0), X(0), Y(55))]
    p.append(f'<polyline points="{X(0):.1f},{Y(0):.1f} {X(XC):.1f},{Y(_t(XC)):.1f} {X(320):.1f},{Y(_t(320)):.1f}" '
             f'fill="none" stroke="#7a4a1f" stroke-width="1.6"/>')
    for x in X_D + X_H:
        p.append(f'<circle cx="{X(x):.1f}" cy="{Y(round(_t(x), 1)):.1f}" r="3" fill="#fff" stroke="#222" stroke-width="1.2"/>')
    for x in range(80, 321, 80):
        p.append(_tx(X(x), Y(0) + 13, str(x), 10, "middle"))
    for t in range(10, 51, 10):
        p.append(_tx(X(0) - 5, Y(t) + 4, str(t), 10, "end"))
    p += [_tx(X(0) - 5, Y(0) + 13, "0", 10, "end"), _tx(X(340), Y(0) + 26, "震央距離 x [km]", 11, "end"),
          _tx(X(0) + 6, Y(54), "走時 t [s]", 11)]
    return _svg(330, 205, p)


def _fig_core():
    cx, cy, R = 120, 98, 88
    d = 103 / 2
    r = R * math.cos(math.radians(d))
    S = (cx + R * math.cos(math.radians(270 - d)), cy - R * math.sin(math.radians(270 - d)))
    P = (cx + R * math.cos(math.radians(270 + d)), cy - R * math.sin(math.radians(270 + d)))
    a1, a2 = 270 - d, 270 + d
    rr = 20
    q1 = (cx + rr * math.cos(math.radians(a1)), cy - rr * math.sin(math.radians(a1)))
    q2 = (cx + rr * math.cos(math.radians(a2)), cy - rr * math.sin(math.radians(a2)))
    p = [f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="#f7efe6" stroke="#333" stroke-width="1.4"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="#e3c9a8" stroke="#333" stroke-width="1.2"/>',
         _ln(S[0], S[1], P[0], P[1], "#c0392b", 1.6),
         _ln(cx, cy, S[0], S[1], "#666", 1, "4,3"), _ln(cx, cy, P[0], P[1], "#666", 1, "4,3"),
         f'<path d="M{q1[0]:.1f},{q1[1]:.1f} A{rr},{rr} 0 0 0 {q2[0]:.1f},{q2[1]:.1f}" fill="none" stroke="#333" stroke-width="1"/>',
         f'<circle cx="{S[0]:.1f}" cy="{S[1]:.1f}" r="3" fill="#c0392b"/>', f'<circle cx="{P[0]:.1f}" cy="{P[1]:.1f}" r="3" fill="#c0392b"/>',
         f'<circle cx="{cx}" cy="{cy}" r="2" fill="#333"/>',
         _tx(cx, cy - 6, "O", 10, "middle"), _tx(cx - 8, cy + 32, "Δ", 11, "end"),
         _tx(S[0] - 6, S[1] + 12, "震源", 10, "end"), _tx(P[0] + 6, P[1] + 12, "到達点", 10),
         _tx(cx, cy - r + 18, "核", 11, "middle"), _tx(cx, cy - R + 16, "マントル", 10, "middle"),
         _tx(cx + R * 0.5 * math.cos(math.radians(30)) + 2, cy - R * 0.5 * math.sin(math.radians(30)) - 4, "R", 11, it=True), _tx(cx + 5, cy + r * 0.8, "r", 11, it=True),
         _ln(cx, cy, cx + R * math.cos(math.radians(30)), cy - R * math.sin(math.radians(30)), "#999", 0.8),
         _ln(cx, cy, cx, cy + r, "#999", 0.8)]
    return _svg(250, 196, p)


TAB_TT = ('<table><tr><th>震央距離 $x$ [km]</th>' + "".join(f"<td>{x}</td>" for x in X_D + X_H) + '</tr>'
          '<tr><th>走時 $t$ [s]</th>' + "".join(f"<td>{_t(x):.1f}</td>" for x in X_D + X_H) + '</tr></table>')
TANS = [16, 17, 40, 41, 42]
TAB_TAN = ('<table><tr><th>$\\theta$</th>' + "".join(f"<td>${d}^\\circ$</td>" for d in TANS) + '</tr>'
           '<tr><th>$\\tan\\theta$</th>' + "".join(f"<td>{math.tan(math.radians(d)):.3f}</td>" for d in TANS) + '</tr></table>')


def B(s):
    return f'<div class="bun">{s}</div>'


CH = {1: {
"goal": r"エラトステネスの方法、偏平率と重力、走時曲線・シャドーゾーンからわかる内部構造、アイソスタシー、地磁気の要素を、数値を使って説明できるようにする。<br>（数値は特に指示がなければ有効数字2桁で答えよ。）",
"items": [
 {"lv": "A", "tag": "計算",
  "q": r"同じ経線上にある2地点 A, B（B は A の真北）の間の距離は $880\,\mathrm{km}$ である。ある日、太陽の南中高度を測ると、A で $62.5^\circ$、B で $54.5^\circ$ であった。太陽光線は平行に届くものとする。<br>(1) A と B の緯度の差は何度か。<br>(2) 地球の全周の長さを求めよ。<br>(3) 地球の半径を求めよ。円周率は 3.14 とする。",
  "a": r"(1) $8.0^\circ$　(2) $4.0\times10^4\,\mathrm{km}$　(3) $6.3\times10^3\,\mathrm{km}$",
  "s": r"(1) 太陽光線が平行なので、南中高度の差は2地点の緯度の差（中心角）に等しい。$62.5^\circ-54.5^\circ=8.0^\circ$。北にある B のほうが南中高度が低い。<br>(2) 中心角 $8.0^\circ$ に対する弧の長さが $880\,\mathrm{km}$ なので、全周 $L=880\times\dfrac{360}{8.0}=3.96\times10^4\fallingdotseq4.0\times10^4\,\mathrm{km}$。<br>(3) $R=\dfrac{L}{2\pi}=\dfrac{3.96\times10^4}{2\times3.14}=6.31\times10^3\fallingdotseq6.3\times10^3\,\mathrm{km}$。<br><b>ポイント</b>：弧の長さは中心角に比例する（$\ell:L=\theta:360^\circ$）。エラトステネスは、2地点の南中高度の差を中心角に置きかえて地球の大きさを求めた。"},
 {"lv": "A", "tag": "計算",
  "q": r"地球を回転楕円体とみなすと、赤道半径は $6378\,\mathrm{km}$、極半径は $6357\,\mathrm{km}$ である。<br>(1) 偏平率を $\dfrac1n$ の形で求めよ（$n$ は整数に丸める）。<br>(2) 緯度差 $1^\circ$ あたりの経線の長さは、赤道付近と極付近のどちらが長いか。理由とともに答えよ。",
  "a": r"(1) $\frac{1}{304}$（約 $\frac{1}{300}$）　(2) 極付近（極付近は曲がり方がゆるやかで、曲率半径が大きいから）",
  "s": r"(1) 偏平率 $=\dfrac{a-b}{a}=\dfrac{6378-6357}{6378}=\dfrac{21}{6378}=\dfrac{1}{303.7}$ より $\dfrac{1}{304}$。地球はほぼ球だが、わずかに赤道方向にふくらんでいる。<br>(2) 緯度は鉛直線（楕円体に垂直な線）と赤道面のなす角で決まる。偏平な楕円は極付近で平たく（曲がり方がゆるやか）、鉛直線の向きを $1^\circ$ 変えるのに長い距離を進む必要がある。実際、緯度 $1^\circ$ あたりの経線の長さは赤道付近で約 $110.6\,\mathrm{km}$、極付近で約 $111.7\,\mathrm{km}$ である。18 世紀の測量でこの差が確かめられ、地球が赤道方向にふくらんだ形であることがわかった。<br><b>ポイント</b>：「極付近ほど緯度 $1^\circ$ の長さが長い」⇔「地球は極方向につぶれた形」。逆に覚えないように、平たい所ほど曲がり方がゆるやか、と理由で覚える。"},
 {"lv": "A", "tag": "空欄補充",
  "q": "次の文の空欄に適する語や数値を入れよ。ただし（ウ）は ① 5〜10　② 30〜60　③ 300〜600 から選べ。" + B("地球の内部は、表面から順に地殻・（ア）・外核・内核に分けられる。地殻と（ア）の境界は（イ）不連続面とよばれ、ここで地震波の速度が急に大きくなる。地殻の厚さは、海洋地殻が 5〜10 km 程度、大陸地殻が（ウ）km 程度である。（ア）は主に（エ）岩のような岩石からなり、核は主に（オ）からなる。外核は（カ）体であるため（キ）波が伝わらない。（ア）と核の境界の深さは約（ク）km である。"),
  "a": "ア マントル　イ モホロビチッチ（モホ）　ウ ②　エ かんらん　オ 鉄（とニッケル）　カ 液　キ S　ク 2900",
  "s": "地殻は大陸で厚く（30〜60 km 程度）、海洋で薄い（5〜10 km 程度）。マントルはかんらん岩質の固体で、深さ約 2900 km から下が核である。外核は液体の鉄（とニッケル）が主成分で、ずれの変形を伝える S 波は液体中を伝わらない。内核は固体である。<br><b>ポイント</b>：境界の名前（モホロビチッチ不連続面）・深さ（約 2900 km）・状態（外核は液体、内核は固体）をセットで覚える。"},
 {"lv": "A", "tag": "計算",
  "q": r"ある地点で地磁気を測定したところ、全磁力が $4.6\times10^4\,\mathrm{nT}$、伏角が $49^\circ$、偏角が西偏 $7.0^\circ$ であった。<br>(1) 水平分力と鉛直分力の大きさを求めよ。$\cos49^\circ=0.656,\ \sin49^\circ=0.755$ とする。<br>(2) 方位磁針の N 極は、真北に対してどちらにずれた向きをさすか。<br>(3) 地磁気の三要素とよばれる3つの量の組を1つ答えよ。",
  "a": r"(1) 水平分力 $3.0\times10^4\,\mathrm{nT}$、鉛直分力 $3.5\times10^4\,\mathrm{nT}$　(2) 西へ $7.0^\circ$ ずれた向き　(3) 偏角・伏角・水平分力",
  "s": r"(1) 全磁力 $F$ を水平と鉛直に分解する。水平分力 $H=F\cos I=4.6\times10^4\times0.656=3.0\times10^4\,\mathrm{nT}$、鉛直分力 $Z=F\sin I=4.6\times10^4\times0.755=3.5\times10^4\,\mathrm{nT}$。<br>(2) 偏角は、磁針の N 極がさす向き（磁北）と真北のなす角。西偏なので西へずれる。<br>(3) 地磁気の向きと強さは3つの量で決まる。偏角・伏角・水平分力の組がよく使われる（水平分力の代わりに全磁力を用いることもある）。<br><b>ポイント</b>：伏角は水平面から下向きに測った角。北半球では N 極が下を向き、伏角は北ほど大きく、磁北極で $90^\circ$ になる。"},
 {"lv": "B", "tag": "計算",
  "q": r"地球を半径 $6.4\times10^6\,\mathrm{m}$ の球とし、自転周期を $8.6\times10^4\,\mathrm{s}$ とする。円周率は 3.14 とする。<br>(1) 赤道上で、質量 $1.0\,\mathrm{kg}$ の物体にはたらく遠心力の大きさを求めよ。<br>(2) (1) は、この物体にはたらく万有引力（$9.8\,\mathrm{N}$ とする）の何 % か。<br>(3) 緯度 $60^\circ$ の地点で、同じ物体にはたらく遠心力の大きさを求めよ。<br>(4) 重力の大きさが赤道より極で大きい理由を2つ答えよ。",
  "a": r"(1) $3.4\times10^{-2}\,\mathrm{N}$　(2) $0.35\,\%$　(3) $1.7\times10^{-2}\,\mathrm{N}$　(4) 極では遠心力がはたらかない。地球が偏平で、極は地球の中心に近く万有引力が大きい。",
  "s": r"(1) 角速度 $\omega=\dfrac{2\pi}{T}=\dfrac{2\times3.14}{8.6\times10^4}=7.30\times10^{-5}\,\mathrm{rad/s}$。遠心力 $f=mR\omega^2=1.0\times6.4\times10^6\times(7.30\times10^{-5})^2=3.4\times10^{-2}\,\mathrm{N}$。<br>(2) $\dfrac{3.4\times10^{-2}}{9.8}\times100=0.35\,\%$。遠心力は万有引力に比べてごく小さい。<br>(3) 自転軸からの距離が $R\cos60^\circ=\dfrac R2$ になるので、遠心力も半分の $1.7\times10^{-2}\,\mathrm{N}$。<br>(4) 重力は万有引力と遠心力の合力。極では自転軸からの距離が0で遠心力がはたらかない。また、地球は赤道方向にふくらんでいて極は中心に近いので、万有引力そのものも極のほうが大きい。<br><b>ポイント</b>：遠心力の大きさは自転軸からの距離 $R\cos\varphi$ に比例する。重力の緯度変化は「遠心力」と「偏平」の2つの理由で説明する。"},
 {"lv": "B", "tag": "走時曲線の読み取り",
  "q": r"ある地域の地表で人工地震を起こし、震央距離 $x$ と P 波の初動の到達時間（走時）$t$ を測定した（表・図）。地下は、P 波速度 $V_1$ の地殻（厚さ $H$）の下に P 波速度 $V_2$ のマントルがあるものとする。" + TAB_TT + _fig_tt() +
       r"(1) $V_1,\ V_2$ を求めよ。<br>(2) 走時曲線が折れ曲がる点の震央距離 $x_c$ を求めよ。<br>(3) $H=\dfrac{x_c}{2}\sqrt{\dfrac{V_2-V_1}{V_2+V_1}}$ の関係を用いて、地殻の厚さ $H$ を求めよ。<br>(4) $x_c$ より遠い観測点では、地殻だけを通る直接波より、マントルを経由する波のほうが先に届く。その理由を簡潔に説明せよ。",
  "a": r"(1) $V_1=6.4\,\mathrm{km/s}$、$V_2=8.0\,\mathrm{km/s}$　(2) $1.8\times10^2\,\mathrm{km}$　(3) $30\,\mathrm{km}$　(4) 遠回りになっても、地震波の速いマントル中を長い距離進むほうが早く着くから。",
  "s": r"(1) 近い観測点では直線の傾きの逆数が速度：$V_1=\dfrac{160}{25.0}=6.4\,\mathrm{km/s}$。遠い観測点では $40\,\mathrm{km}$ 進むごとに走時が $5.0\,\mathrm{s}$ 増えるので $V_2=\dfrac{40}{5.0}=8.0\,\mathrm{km/s}$。<br>(2) 遠い側の直線は $t=35.6+\dfrac{x-240}{8.0}=\dfrac{x}{8.0}+5.6$。これと $t=\dfrac{x}{6.4}$ の交点は $x\left(\dfrac{1}{6.4}-\dfrac{1}{8.0}\right)=5.6$ より $x_c=\dfrac{5.6}{0.03125}=179\fallingdotseq1.8\times10^2\,\mathrm{km}$。<br>(3) $H=\dfrac{180}{2}\sqrt{\dfrac{8.0-6.4}{8.0+6.4}}=90\times\sqrt{\dfrac19}=30\,\mathrm{km}$。<br>(4) マントルを経由する波は、地殻を斜めに下ってマントル上部を進み、再び地殻を上がってくる。震央距離が大きいほど速いマントル中を進む部分の割合が大きくなり、遠回りの不利を上回る。<br><b>ポイント</b>：走時曲線の<b>傾きの逆数＝速度</b>。折れ曲がる距離 $x_c$ が大きいほど地殻が厚い。モホロビチッチはこの折れ曲がりから地殻とマントルの境界を発見した。"},
 {"lv": "B", "tag": "計算・論述",
  "q": r"ある地震の震央から中心角で約 $103^\circ$ より遠くでは S 波が観測されず、P 波は約 $103^\circ$〜$143^\circ$ の範囲でほとんど観測されない。<br>(1) 地球の全周を $4.0\times10^4\,\mathrm{km}$ として、中心角 $103^\circ$ は地表に沿って何 km か。<br>(2) S 波が中心角 $103^\circ$ より遠くで観測されないことから、核についてどのようなことがわかるか。理由とともに40字以内で述べよ。<br>(3) P 波がほとんど届かない範囲（シャドーゾーン）ができる理由を、50字以内で述べよ。",
  "a": r"(1) $1.1\times10^4\,\mathrm{km}$　(2) 解答例：S波は液体中を伝わらないので、核の外側の部分（外核）は液体であることがわかる。（39字）　(3) 解答例：P波はマントルから核に入るとき速度が急に小さくなって大きく屈折するので、届かない範囲ができる。（47字）",
  "s": r"(1) $4.0\times10^4\times\dfrac{103}{360}=1.1\times10^4\,\mathrm{km}$。<br>(2) S 波は横波（ずれの変形を伝える波）で、液体中を伝わらない。$103^\circ$ より遠い地点へは核を通る経路しかないので、核の少なくとも外側（外核）は液体である。<br>(3) 核に入った P 波は速度が小さくなるため、境界で屈折して核の中心側へ曲がる。そのため $103^\circ$〜$143^\circ$ の範囲には P 波がほとんど届かない。この範囲でも弱い P 波が観測されることから、内核の存在が発見された（レーマン）。<br><b>ポイント</b>：S 波の影 ⇒ 外核は液体。P 波の影 ⇒ 核で P 波が遅くなって屈折する。2つの影を混同しない。"},
 {"lv": "B", "tag": "計算",
  "q": r"地殻の密度を $2.7\,\mathrm{g/cm^3}$、マントルの密度を $3.3\,\mathrm{g/cm^3}$ とし、アイソスタシーが成り立っているとする。<br>(1) 海抜 0 m の平野の地殻の厚さが $30\,\mathrm{km}$ のとき、標高 $2.0\,\mathrm{km}$ の高原の地殻の厚さを求めよ。<br>(2) 厚さ $2.0\,\mathrm{km}$ の氷床（密度 $0.90\,\mathrm{g/cm^3}$）におおわれていた地域で、氷床がすべてとけた。アイソスタシーが回復したとき、地表は何 m 隆起するか。",
  "a": r"(1) $41\,\mathrm{km}$　(2) $5.5\times10^2\,\mathrm{m}$",
  "s": r"(1) 高原の地殻がマントルに $r$ [km] だけ深く入りこんでいる（根）とする。根の底の深さで、単位面積あたりの上にのる質量が等しいので、$2.7\times(2.0+30+r)=2.7\times30+3.3r$。$0.6r=2.7\times2.0$ より $r=9.0\,\mathrm{km}$。地殻の厚さは $2.0+30+9.0=41\,\mathrm{km}$。<br>(2) 失われた氷の質量（単位面積あたり $0.90\times2.0$）の分だけ、まわりからマントルが流れこんで地表が $\Delta$ 上がる：$3.3\Delta=0.90\times2.0$ より $\Delta=0.545\,\mathrm{km}\fallingdotseq5.5\times10^2\,\mathrm{m}$。スカンジナビア半島などでは、最終氷期の氷床がとけたあと、現在も隆起が続いている。<br><b>ポイント</b>：アイソスタシーは「ある深さ（補償面）より上の質量が、どこでも等しい」。高い山ほど深い根をもつ。"},
 {"lv": "B", "tag": "計算",
  "q": r"地球の磁場を、地球の中心に置いた棒磁石の磁場とみなすと、磁気緯度 $\varphi$ の地点の伏角 $I$ には $\tan I=2\tan\varphi$ の関係がある。<br>(1) 磁気赤道と磁北極での伏角はそれぞれ何度か。<br>(2) 伏角が $60^\circ$ の地点の磁気緯度を求めよ。$\tan60^\circ=1.73$ とし、下の表から最も近い角を選べ。<br>(3) ある溶岩が固まったときに記録された残留磁気の伏角は $30^\circ$ であった（$\tan30^\circ=0.577$）。この溶岩ができた当時の、その場所の磁気緯度を表から選べ。" + TAB_TAN,
  "a": r"(1) 磁気赤道 $0^\circ$、磁北極 $90^\circ$　(2) $41^\circ$　(3) $16^\circ$",
  "s": r"(1) $\varphi=0$ なら $\tan I=0$ で $I=0^\circ$（磁針は水平）。$\varphi\to90^\circ$ で $\tan I\to\infty$、$I=90^\circ$（磁針は真下を向く）。<br>(2) $\tan\varphi=\dfrac{\tan60^\circ}{2}=\dfrac{1.73}{2}=0.865$。表で最も近いのは $\tan41^\circ=0.869$。<br>(3) $\tan\varphi=\dfrac{0.577}{2}=0.289$ より $\varphi\fallingdotseq16^\circ$。岩石に残された磁気（古地磁気）から当時の緯度がわかり、大陸が移動してきたことの証拠になる。<br><b>ポイント</b>：伏角は磁気緯度とともに大きくなる。古地磁気の伏角から「その岩石ができた当時の緯度」が推定できる。"},
 {"lv": "C", "tag": "計算・論述",
  "q": r"万有引力定数を $G=6.7\times10^{-11}\,\mathrm{N\cdot m^2/kg^2}$、地表の重力加速度の大きさを $g=9.8\,\mathrm{m/s^2}$、地球の半径を $R=6.4\times10^6\,\mathrm{m}$、円周率を 3.14 とし、遠心力は無視する。<br>(1) 地球の質量 $M$ を求めよ。<br>(2) 地球の平均密度を $\mathrm{g/cm^3}$ の単位で求めよ。<br>(3) 地表付近の岩石の密度は $2.7\,\mathrm{g/cm^3}$ 程度である。(2) と比べて、地球内部についてどのようなことが推定できるか。30字以内で述べよ。<br>(4) 地球を、半径 $0.55R$ の核と、その外側の密度 $4.5\,\mathrm{g/cm^3}$ の層（マントルと地殻）の2層からなるとみなす。地球の平均密度を $5.5\,\mathrm{g/cm^3}$ として、核の平均密度を求めよ。$0.55^3=0.166$ とする。",
  "a": r"(1) $6.0\times10^{24}\,\mathrm{kg}$　(2) $5.5\,\mathrm{g/cm^3}$　(3) 解答例：地球の内部には、地表の岩石より密度の大きい物質がある。（27字）　(4) 約 $11\,\mathrm{g/cm^3}$",
  "s": r"(1) 地表の物体にはたらく重力は万有引力なので $mg=\dfrac{GMm}{R^2}$。$M=\dfrac{gR^2}{G}=\dfrac{9.8\times(6.4\times10^6)^2}{6.7\times10^{-11}}=6.0\times10^{24}\,\mathrm{kg}$。<br>(2) 体積 $V=\dfrac43\pi R^3=\dfrac43\times3.14\times(6.4\times10^6)^3=1.10\times10^{21}\,\mathrm{m^3}$。$\rho=\dfrac MV=5.5\times10^3\,\mathrm{kg/m^3}=5.5\,\mathrm{g/cm^3}$。<br>(3) 平均が表面の岩石の2倍ほどあるので、内部（特に中心部）に密度の大きい物質が集まっている。<br>(4) 体積の割合は核が $0.166$、外側の層が $1-0.166=0.834$。$\rho_c\times0.166+4.5\times0.834=5.5$ より $\rho_c=\dfrac{5.5-3.75}{0.166}=10.5\fallingdotseq11\,\mathrm{g/cm^3}$。鉄の密度（地表で約 $7.9\,\mathrm{g/cm^3}$）は高圧下でさらに大きくなるので、核が主に鉄からなるという考えと矛盾しない。鉄隕石（隕鉄）の存在や、地球磁場の存在も、鉄の核を支持する。<br><b>ポイント</b>：平均密度は「質量÷体積」。$M=gR^2/G$ は万有引力と重力の等置から一行で出る。"},
 {"lv": "C", "tag": "計算・論述",
  "q": r"図のように、震源から出た地震波の波線が核の表面に接して地表に達する場合を考える。地球の半径を $R$、核の半径を $r$、震源と到達点が地球の中心 O に対してなす角を $\Delta$ とする。" + _fig_core() +
       r"(1) 地震波が地球内部を直進すると仮定して、$r$ を $R$ と $\Delta$ で表せ。<br>(2) S 波が観測されなくなる $\Delta=103^\circ$ を (1) の式に用いて、核の半径を求めよ。$R=6.4\times10^3\,\mathrm{km}$、$\cos51.5^\circ=0.623$ とする。<br>(3) 実際の核の半径は約 $3.5\times10^3\,\mathrm{km}$ で、(2) の値より小さい。この違いが生じる理由を、マントル中の地震波の速度に注目して60字以内で述べよ。",
  "a": r"(1) $r=R\cos\dfrac{\Delta}{2}$　(2) $4.0\times10^3\,\mathrm{km}$　(3) 解答例：マントルでは深いほど地震波が速く波線は下に凸に曲がるので、直進する場合より近い地点に達し、核を大きく見積もるから。（57字）",
  "s": r"(1) 波線（弦）は核に接するので、O から弦に下ろした垂線の長さが $r$。この垂線は中心角 $\Delta$ を二等分するので $r=R\cos\dfrac\Delta2$。<br>(2) $r=6.4\times10^3\times\cos51.5^\circ=6.4\times10^3\times0.623=4.0\times10^3\,\mathrm{km}$。<br>(3) マントルでは深くなるほど地震波の速度が大きいので、波線は屈折して少しずつ地表側へ曲がり、下に凸の曲線になる。核に接する波線は、直進する場合より震源に近い地点で地表に達する。したがって、観測された $103^\circ$ を直進の式に当てはめると、核の半径を実際より大きく見積もってしまう。<br><b>ポイント</b>：実際の地震波は直進せず、速度の変化に応じて屈折する。単純なモデルで求めた値と実際の値の違いを、仮定のどこが現実と違うかから説明する。"},
]}}


def verify():
    items = CH[1]["items"]
    # 1-1 エラトステネス
    d = 62.5 - 54.5
    L = 880 * 360 / d
    _near(d, 8.0); _near(L, 4.0e4); _near(L / (2 * 3.14), 6.3e3)
    assert abs(L - 3.96e4) < 1 and abs(L / (2 * 3.14) - 6.31e3) < 5
    # 1-2 偏平率と緯度1°の長さ（極で a^2/b、赤道で b^2/a が曲率半径）
    a, b = 6378, 6357
    assert round(a / (a - b)) == 304 and abs(a / (a - b) - 303.7) < 0.05
    _near(a * a / b * math.pi / 180, 111.7, 4); _near(b * b / a * math.pi / 180, 110.6, 4)
    # 1-4 地磁気の分解
    assert abs(math.cos(math.radians(49)) - 0.656) < 5e-4 and abs(math.sin(math.radians(49)) - 0.755) < 5e-4
    _near(4.6e4 * 0.656, 3.0e4); _near(4.6e4 * 0.755, 3.5e4)
    # 1-5 遠心力
    w = 2 * 3.14 / 8.6e4
    _near(w, 7.30e-5, 3)
    f = 6.4e6 * w ** 2
    _near(f, 3.4e-2); _near(f / 9.8 * 100, 0.35); _near(f * math.cos(math.radians(60)), 1.7e-2)
    _near(3.4e-2 / 9.8 * 100, 0.35)
    # 1-6 走時曲線
    tt = [round(_t(x), 1) for x in X_D + X_H]
    assert tt == [5.0, 10.0, 15.0, 20.0, 25.0, 35.6, 40.6, 45.6], tt
    assert abs(160 / 25.0 - V1) < 1e-12 and abs(40 / (40.6 - 35.6) - V2) < 1e-9
    xc = (35.6 - 240 / 8.0) / (1 / 6.4 - 1 / 8.0)
    _near(xc, 179, 3); _near(xc, 1.8e2); _near(XC, 1.8e2)
    assert abs(1 / 6.4 - 1 / 8.0 - 0.03125) < 1e-12
    Hc = 180 / 2 * math.sqrt((8.0 - 6.4) / (8.0 + 6.4))
    assert abs(Hc - 30) < 1e-9 and abs(XC / 2 * math.sqrt((V2 - V1) / (V2 + V1)) - H) < 1e-9
    assert all(_t(x) == x / V1 for x in X_D) and all(_t(x) == x / V2 + T0 for x in X_H)
    # 1-7 中心角を距離に
    _near(4.0e4 * 103 / 360, 1.1e4)
    # 1-8 アイソスタシー
    r = 2.7 * 2.0 / (3.3 - 2.7)
    assert abs(r - 9.0) < 1e-9 and abs(2.0 + 30 + r - 41) < 1e-9
    assert abs(2.7 * (2.0 + 30 + r) - (2.7 * 30 + 3.3 * r)) < 1e-9
    up = 0.90 * 2.0 / 3.3 * 1000
    _near(up, 5.5e2); _near(up / 1000, 0.545, 3)
    # 1-9 伏角と磁気緯度
    tans = {dd: math.tan(math.radians(dd)) for dd in TANS}
    t2 = 1.73 / 2
    assert min(TANS, key=lambda dd: abs(tans[dd] - t2)) == 41
    t3 = 0.577 / 2
    assert min(TANS, key=lambda dd: abs(tans[dd] - t3)) == 16
    _near(math.degrees(math.atan(math.tan(math.radians(60)) / 2)), 41)
    _near(math.degrees(math.atan(math.tan(math.radians(30)) / 2)), 16)
    # 1-10 地球の質量・密度・核の密度
    M = 9.8 * (6.4e6) ** 2 / 6.7e-11
    V = 4 / 3 * 3.14 * (6.4e6) ** 3
    _near(M, 6.0e24); _near(V, 1.10e21, 3); _near(M / V / 1000, 5.5)
    assert abs(0.55 ** 3 - 0.166) < 5e-4
    rc = (5.5 - 4.5 * (1 - 0.166)) / 0.166
    _near(rc, 10.5, 3); _near(rc, 11); _near(4.5 * 0.834, 3.75, 3)
    # 1-11 直進波線と核の半径
    assert abs(math.cos(math.radians(51.5)) - 0.623) < 5e-4
    _near(6.4e3 * 0.623, 4.0e3)
    # ---- 形式の点検 ----
    _form(items)


def _form(items):
    lv = [it["lv"] for it in items]
    assert lv == sorted(lv) and lv.count("A") == 4 and lv.count("B") in (4, 5) and lv.count("C") == 2, lv
    for it in items:
        for k in ("lv", "tag", "q", "a", "s"):
            assert it.get(k), k
        assert "<b>ポイント</b>" in it["s"]
        for k in ("q", "a", "s"):
            assert "$$" not in it[k] and it[k].count("$") % 2 == 0, (k, it["q"][:30])
        lims = [int(m) for m in re.findall(r"(\d+)字以内", it["q"])]
        ess = re.findall(r"解答例：(.*?)（(\d+)字）", it["a"])
        assert len(lims) == len(ess), (lims, ess)
        for (body, n), lim in zip(ess, lims):
            assert len(body) == int(n) <= lim, (len(body), n, lim, body)
