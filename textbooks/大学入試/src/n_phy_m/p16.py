"""問題集 第16章 電流と磁場・電磁誘導。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
from math import sin as _sin, cos as _cos, atan2 as _atan2, radians as _rad
from sympy import *


# ---------------- 図 ----------------
def _svg(w, h, body):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(body) + "</svg>"

def _t(x, y, s, size=11, anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}">{s}</text>'

def _ln(x1, y1, x2, y2, w=1.0, dash="", col="#222"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'

def _arrow(x1, y1, x2, y2, w=1.1, col="#222", hs=6.0):
    a = _atan2(y2 - y1, x2 - x1)
    bx, by = x2 - hs * _cos(a), y2 - hs * _sin(a)
    px, py = 0.42 * hs * _sin(a), -0.42 * hs * _cos(a)
    return (_ln(x1, y1, bx, by, w, col=col) +
            f'<polygon points="{x2:.1f},{y2:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{col}"/>')

def _curve(pts, w=1.6, col="#1d4e89"):
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{col}" stroke-width="{w}"/>'

def _dot(x, y, r=2.6, col="#222"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'

I = lambda s: f'<tspan font-family="Liberation Serif,serif" font-style="italic" font-size="12.5">{s}</tspan>'

def _odot(x, y):   # 紙面の裏から表の向き
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="none" stroke="#888" stroke-width="0.9"/>' + _dot(x, y, 1.2, "#888")

def _cross(x, y):  # 紙面の表から裏の向き
    return _ln(x - 3.5, y - 3.5, x + 3.5, y + 3.5, 0.9, "", "#888") + _ln(x - 3.5, y + 3.5, x + 3.5, y - 3.5, 0.9, "", "#888")


def _fig_rails():
    y1, y2, xr, xb = 46, 136, 46, 214
    b = []
    for gx in range(80, 290, 34):
        for gy in (68, 91, 114):
            if abs(gx - xb) > 10:
                b.append(_odot(gx, gy))
    b += [_ln(xr, y1, 330, y1, 2), _ln(xr, y2, 330, y2, 2), _ln(xr, y1, xr, y2, 1.2),
          f'<rect x="{xr-5.5}" y="{(y1+y2)/2-15}" width="11" height="30" fill="#fff" stroke="#222" stroke-width="1.2"/>',
          _ln(xb, y1 - 8, xb, y2 + 8, 3.2, "", "#1d4e89"),
          _arrow(xb + 6, y2 + 16, xb + 46, y2 + 16, 1.3), _t(xb + 52, y2 + 20, I("v"), 11, "start"),
          _t(xb, y1 - 12, "P"), _t(xb, y2 + 20, "Q"), _t(xr - 10, (y1 + y2) / 2 + 4, I("R"), 12, "end"),
          _arrow(312, (y1 + y2) / 2, 312, y1 + 2, 0.8, hs=5) + _arrow(312, (y1 + y2) / 2, 312, y2 - 2, 0.8, hs=5),
          _t(318, (y1 + y2) / 2 + 4, I("l"), 12, "start"),
          _t(330, 16, "磁場 " + I("B") + "：紙面の裏から表の向き（鉛直上向き）", 10, "end")]
    return _svg(340, 166, b)


def _fig_coil():
    a, x0, xf, yc = 40, 40, 150, 80
    b = [f'<rect x="{xf}" y="{yc-56}" width="{3*a}" height="112" fill="#f2f5fa" stroke="#888" stroke-dasharray="4,3"/>']
    for gx in range(xf + 12, xf + 3 * a, 24):
        for gy in range(yc - 44, yc + 50, 24):
            b.append(_cross(gx, gy))
    b += [f'<rect x="{x0}" y="{yc-a/2}" width="{a}" height="{a}" fill="none" stroke="#1d4e89" stroke-width="2"/>',
          _arrow(x0 + a + 6, yc, x0 + a + 40, yc, 1.3), _t(x0 + a + 23, yc - 6, I("v")),
          _t(x0 + a / 2, yc + a / 2 + 14, I("a")), _t(x0 - 6, yc + 4, I("a"), 11, "end"),
          _arrow(xf, yc + 70, xf + 3 * a, yc + 70, 0.8, hs=5) + _arrow(xf + 3 * a, yc + 70, xf, yc + 70, 0.8, hs=5),
          _t(xf + 1.5 * a, yc + 66, "3" + I("a")), _t(xf + 3 * a + 8, yc - 40, I("B"), 12, "start"),
          _t(xf + 3 * a + 8, yc - 26, "（紙面の表から裏）", 9, "start")]
    return _svg(360, 162, b)


def _fig_region():
    ox, oy, d = 50, 150, 110
    r = 2 * d
    al = _rad(30)
    b = [f'<rect x="{ox}" y="20" width="{d}" height="{oy-20}" fill="#f2f5fa"/>',
         _ln(ox, 20, ox, oy + 10, 1.0, "", "#666"), _ln(ox + d, 20, ox + d, oy + 10, 1.0, "4,3", "#666")]
    for gx in range(ox + 14, ox + d, 24):
        al_g = _asin_safe((gx - ox) / r)
        ycur = oy - r * (1 - _cos(al_g))
        for gy in range(34, oy - 4, 24):
            if abs(gy - ycur) > 10:
                b.append(_cross(gx, gy))
    b += [_arrow(14, oy, 330, oy, 0.9), _arrow(ox, oy + 10, ox, 4, 0.9),
          _t(328, oy + 14, I("x"), 11, "end"), _t(ox - 6, 14, I("y"), 11, "end"), _t(ox - 4, oy + 14, "O", 11, "end"),
          _t(ox + d, oy + 14, I("d"))]
    pts = [(ox + r * _sin(al * k / 30), oy - r * (1 - _cos(al * k / 30))) for k in range(31)]
    b.append(_curve(pts, 1.8, "#c0392b"))
    ex, ey = pts[-1]
    b.append(_arrow(ex, ey, ex + 90 * _cos(al), ey - 90 * _sin(al), 1.6, "#c0392b"))
    b.append(_arrow(16, oy - 0.1, ox - 2, oy - 0.1, 1.6, "#c0392b"))
    b.append(_t(26, oy - 6, I("v"), 11))
    b.append(_t(ox + d / 2, 13, "磁場 " + I("B") + "（紙面の表から裏）", 9))
    return _svg(340, 170, b)


def _asin_safe(x):
    from math import asin
    return asin(max(-1.0, min(1.0, x)))


FIG_B1 = _fig_rails()
FIG_B4 = _fig_coil()
FIG_C2 = _fig_region()

CH = {16: {
"goal": r"電流がつくる磁場と、電流・荷電粒子が磁場から受ける力の向きを確実に決める。誘導起電力は「磁束の変化」と「$vBl$」の 2 通りで求め、エネルギー保存で検算する習慣をつける。",
"items": [
 {"lv": "A", "tag": "電流がつくる磁場", "q": r"真空の透磁率を $\mu_0=4\pi\times10^{-7}\,\mathrm{N/A^2}$ とする。<br>(1) 十分に長い直線の導線に $5.0\,\mathrm A$ の電流を流す。導線から $0.10\,\mathrm m$ の点の磁場の強さ $H$ と磁束密度 $B$ を求めよ。<br>(2) 半径 $0.10\,\mathrm m$ の 1 巻きの円形の導線に $5.0\,\mathrm A$ の電流を流す。円の中心の磁場の強さを求めよ。<br>(3) $1\,\mathrm m$ あたりの巻数が $2.0\times10^3$ の十分に長いソレノイドに $2.0\,\mathrm A$ の電流を流す。内部の磁場の強さと磁束密度を求めよ。",
  "a": r"(1) $8.0\,\mathrm{A/m}$、$1.0\times10^{-5}\,\mathrm T$　(2) $25\,\mathrm{A/m}$　(3) $4.0\times10^3\,\mathrm{A/m}$、$5.0\times10^{-3}\,\mathrm T$",
  "s": r"(1) $H=\dfrac I{2\pi r}=\dfrac{5.0}{2\pi\times0.10}\fallingdotseq8.0\,\mathrm{A/m}$。$B=\mu_0H=4\pi\times10^{-7}\times\dfrac{5.0}{2\pi\times0.10}=1.0\times10^{-5}\,\mathrm T$。<br>(2) $H=\dfrac I{2r}=\dfrac{5.0}{2\times0.10}=25\,\mathrm{A/m}$。<br>(3) $H=nI=2.0\times10^3\times2.0=4.0\times10^3\,\mathrm{A/m}$、$B=\mu_0H\fallingdotseq5.0\times10^{-3}\,\mathrm T$。向きはいずれも右ねじの法則で決まる。<br><b>ポイント</b>：直線 $\dfrac I{2\pi r}$、円の中心 $\dfrac I{2r}$、ソレノイド $nI$ の 3 つは確実に。$B=\mu_0H$。"},
 {"lv": "A", "tag": "電流が受ける力", "q": r"(1) 磁束密度 $0.50\,\mathrm T$ の一様な磁場に垂直に置いた長さ $0.20\,\mathrm m$ の導線に、$3.0\,\mathrm A$ の電流を流す。導線が受ける力の大きさを求めよ。<br>(2) (1) の導線を、磁場となす角が $30^\circ$ になるように置くと、力の大きさはいくらになるか。<br>(3) 真空中で $0.050\,\mathrm m$ 離して平行に張った 2 本の長い導線に、同じ向きに $10\,\mathrm A$ ずつ電流を流す。導線 $1\,\mathrm m$ あたりが受ける力の大きさを求め、引力か斥力かを答えよ。$\mu_0=4\pi\times10^{-7}\,\mathrm{N/A^2}$ とする。",
  "a": r"(1) $0.30\,\mathrm N$　(2) $0.15\,\mathrm N$　(3) $4.0\times10^{-4}\,\mathrm N$、引力",
  "s": r"(1) $F=IBl=3.0\times0.50\times0.20=0.30\,\mathrm N$。<br>(2) 磁場に垂直な成分だけがきくので $F=IBl\sin30^\circ=0.15\,\mathrm N$。<br>(3) 一方の電流がもう一方の位置につくる磁束密度は $B=\dfrac{\mu_0I}{2\pi r}$。$F=IB\cdot1=\dfrac{\mu_0I^2}{2\pi r}=\dfrac{4\pi\times10^{-7}\times10^2}{2\pi\times0.050}=4.0\times10^{-4}\,\mathrm N$。同じ向きの電流は引き合う。<br><b>ポイント</b>：力の向きはフレミングの左手の法則（または $\vec F=I\vec l\times\vec B$）。平行電流は「同じ向きなら引力、逆向きなら斥力」。"},
 {"lv": "A", "tag": "ローレンツ力", "q": r"陽子（質量 $1.67\times10^{-27}\,\mathrm{kg}$、電気量 $1.60\times10^{-19}\,\mathrm C$）が、磁束密度 $0.50\,\mathrm T$ の一様な磁場に垂直に、速さ $2.0\times10^6\,\mathrm{m/s}$ で入射した。重力は無視する。<br>(1) 等速円運動の半径を求めよ。<br>(2) 円運動の周期を求めよ。<br>(3) 入射の速さを 2 倍にすると、半径と周期はそれぞれ何倍になるか。<br>(4) 陽子が 1 周する間にローレンツ力がする仕事を求めよ。",
  "a": r"(1) $4.2\times10^{-2}\,\mathrm m$　(2) $1.3\times10^{-7}\,\mathrm s$　(3) 半径 2 倍、周期 1 倍（変わらない）　(4) $0$",
  "s": r"(1) $m\dfrac{v^2}r=qvB$ より $r=\dfrac{mv}{qB}=\dfrac{1.67\times10^{-27}\times2.0\times10^6}{1.60\times10^{-19}\times0.50}\fallingdotseq4.2\times10^{-2}\,\mathrm m$。<br>(2) $T=\dfrac{2\pi r}v=\dfrac{2\pi m}{qB}\fallingdotseq1.3\times10^{-7}\,\mathrm s$。<br>(3) $r\propto v$、$T$ は $v$ によらない。<br>(4) ローレンツ力はつねに速度に垂直なので、仕事は 0（速さは変わらない）。<br><b>ポイント</b>：$r=\dfrac{mv}{qB}$、$T=\dfrac{2\pi m}{qB}$。周期が速さによらないことがサイクロトロンの原理になる。"},
 {"lv": "A", "tag": "電磁誘導", "q": r"(1) 巻数 200、断面積 $0.010\,\mathrm{m^2}$ のコイルを貫く一様な磁場の磁束密度が、$0.10\,\mathrm s$ の間に $0.20\,\mathrm T$ から $0.50\,\mathrm T$ まで一定の割合で増加した。コイルに生じる誘導起電力の大きさを求めよ。<br>(2) (1) のコイルの両端に $30\,\Omega$ の抵抗をつなぐと、流れる電流はいくらか（コイルの抵抗は無視）。また、誘導電流がコイルの内部につくる磁場は、もとの磁場と同じ向きか逆向きか。<br>(3) 自己インダクタンス $0.40\,\mathrm H$ のコイルを流れる電流が、$0.050\,\mathrm s$ の間に一定の割合で $2.0\,\mathrm A$ 増加した。コイルに生じる自己誘導起電力の大きさを求めよ。",
  "a": r"(1) $6.0\,\mathrm V$　(2) $0.20\,\mathrm A$、逆向き　(3) $16\,\mathrm V$",
  "s": r"(1) 磁束の変化は $\Delta\Phi=(0.50-0.20)\times0.010=3.0\times10^{-3}\,\mathrm{Wb}$。$V=N\dfrac{\Delta\Phi}{\Delta t}=200\times\dfrac{3.0\times10^{-3}}{0.10}=6.0\,\mathrm V$。<br>(2) $I=\dfrac{6.0}{30}=0.20\,\mathrm A$。レンツの法則より、誘導電流は磁束の増加を妨げる向き、すなわちもとの磁場と逆向きの磁場をつくる。<br>(3) $V=L\dfrac{\Delta I}{\Delta t}=0.40\times\dfrac{2.0}{0.050}=16\,\mathrm V$。<br><b>ポイント</b>：$V=N\dfrac{\Delta\Phi}{\Delta t}$、向きは「変化を妨げる向き」。自己誘導も同じで、電流の変化を妨げる向きに起電力が生じる。"},
 {"lv": "B", "tag": "導体棒の誘導起電力", "q": r"図は、水平に置いた 2 本の平行なレール（間隔 $l=0.50\,\mathrm m$）を上から見たものである。レールの左端は抵抗 $R=2.0\,\Omega$ でつながれ、鉛直上向きに磁束密度 $B=0.40\,\mathrm T$ の一様な磁場がある。レールに垂直に置いた導体棒 PQ を、外力で右向きに一定の速さ $v=3.0\,\mathrm{m/s}$ で動かす。レールと棒の抵抗、摩擦は無視する。" + FIG_B1 + r"(1) 棒に生じる誘導起電力の大きさを求めよ。<br>(2) 棒を流れる電流の大きさと向き（P→Q か Q→P か）を求めよ。また、P と Q のどちらの電位が高いか。<br>(3) 棒を一定の速さで動かすのに必要な外力の大きさを求めよ。<br>(4) 外力の仕事率と、抵抗で発生するジュール熱の仕事率を求めて比べよ。",
  "a": r"(1) $0.60\,\mathrm V$　(2) $0.30\,\mathrm A$、P→Q、Q が高い　(3) $0.060\,\mathrm N$　(4) どちらも $0.18\,\mathrm W$ で等しい",
  "s": r"(1) $V=vBl=3.0\times0.40\times0.50=0.60\,\mathrm V$。<br>(2) $I=\dfrac VR=0.30\,\mathrm A$。棒の中の正電荷が受けるローレンツ力 $\vec F=q\vec v\times\vec B$ は、図で下向き（P→Q）。よって電流は棒の中を P→Q に流れる。棒は電池のはたらきをし、電流が出ていく Q 側が正極で電位が高い。（レンツの法則で確かめると、回路を貫く上向きの磁束が増えるので、上から見て時計回りの電流が流れ、棒の中では P→Q になる。）<br>(3) 電流が磁場から受ける力 $IBl=0.30\times0.40\times0.50=0.060\,\mathrm N$ は左向き（運動を妨げる向き）。等速なので外力は右向きに $0.060\,\mathrm N$。<br>(4) 外力の仕事率 $Fv=0.060\times3.0=0.18\,\mathrm W$、ジュール熱 $I^2R=0.30^2\times2.0=0.18\,\mathrm W$。外力の仕事がすべてジュール熱になる。<br><b>ポイント</b>：動く導体棒は「起電力 $vBl$ の電池」に置きかえる。電流が受ける力はつねに運動を妨げる向きで、エネルギー保存 $Fv=I^2R$ が成り立つ。"},
 {"lv": "B", "tag": "斜面上の導体棒", "q": r"傾き $30^\circ$ のなめらかな斜面上に、間隔 $l=0.70\,\mathrm m$ の 2 本の平行なレールが斜面に沿って置かれ、上端が抵抗 $R=0.50\,\Omega$ でつながれている。斜面に垂直に磁束密度 $B=0.50\,\mathrm T$ の一様な磁場がある。質量 $m=0.10\,\mathrm{kg}$ の導体棒をレールに垂直に置いて静かに放すと、棒はレールに垂直なまま斜面を下った。重力加速度の大きさを $9.8\,\mathrm{m/s^2}$ とし、レールと棒の抵抗、自己誘導は無視する。<br>(1) 棒の速さが $v$ のとき、棒を流れる電流と、棒が磁場から受ける力の大きさと向きを、$v,\ B,\ l,\ R$ で表せ。<br>(2) 棒の速さはやがて一定になる。その速さ（終端速度）を求めよ。<br>(3) 終端速度で動いているときの電流と、抵抗で 1 s あたりに発生するジュール熱を求め、重力の仕事率と比べよ。<br>(4) 速さが $0.50\,\mathrm{m/s}$ のときの棒の加速度の大きさを求めよ。",
  "a": r"(1) 電流 $\dfrac{vBl}R$、力 $\dfrac{B^2l^2v}R$（斜面に沿って上向き）　(2) $2.0\,\mathrm{m/s}$　(3) $1.4\,\mathrm A$、$0.98\,\mathrm J$。重力の仕事率 $0.98\,\mathrm W$ と等しい　(4) $3.7\,\mathrm{m/s^2}$",
  "s": r"(1) 起電力 $vBl$、電流 $I=\dfrac{vBl}R$。力 $IBl=\dfrac{B^2l^2v}R$ で、運動を妨げる向き（斜面に沿って上向き）。<br>(2) 斜面方向の運動方程式 $ma=mg\sin30^\circ-\dfrac{B^2l^2v}R$。$a=0$ となる速さは $v_\mathrm f=\dfrac{mgR\sin30^\circ}{B^2l^2}=\dfrac{0.10\times9.8\times0.50\times0.50}{0.50^2\times0.70^2}=2.0\,\mathrm{m/s}$。<br>(3) $I=\dfrac{2.0\times0.50\times0.70}{0.50}=1.4\,\mathrm A$、$I^2R=0.98\,\mathrm W$ なので 1 s あたり $0.98\,\mathrm J$。重力の仕事率 $mg\sin30^\circ\cdot v_\mathrm f=0.49\times2.0=0.98\,\mathrm W$ に等しい（重力の位置エネルギーの減少がすべてジュール熱になる）。<br>(4) $a=9.8\times0.50-\dfrac{0.50^2\times0.70^2\times0.50}{0.10\times0.50}=4.9-1.225\fallingdotseq3.7\,\mathrm{m/s^2}$。<br><b>ポイント</b>：電磁誘導による力は速さに比例するので、空気抵抗と同じように終端速度がある。終端速度では「重力の仕事率 $=$ ジュール熱」。"},
 {"lv": "B", "tag": "荷電粒子の運動", "q": r"電気量 $q=1.6\times10^{-19}\,\mathrm C$ の正イオンが、紙面上で右向きに進み、強さ $E=2.0\times10^4\,\mathrm{V/m}$ の一様な電場と、紙面の裏から表の向きで磁束密度 $B=0.10\,\mathrm T$ の一様な磁場が重なった領域に入った。重力は無視する。<br>(1) イオンが直進するときの速さを求めよ。<br>(2) このとき、電場の向きは紙面上で上向き・下向きのどちらか。<br>(3) 直進したイオンは、次に磁束密度 $B'=0.20\,\mathrm T$ の磁場だけの領域に垂直に入り、半円をえがいた。イオンの質量が $2.4\times10^{-26}\,\mathrm{kg}$ のとき、円運動の半径を求めよ。<br>(4) 同じ電気量で、(3) の領域で半径 $0.20\,\mathrm m$ の円をえがいたイオンの質量を求めよ。",
  "a": r"(1) $2.0\times10^5\,\mathrm{m/s}$　(2) 上向き　(3) $0.15\,\mathrm m$　(4) $3.2\times10^{-26}\,\mathrm{kg}$",
  "s": r"(1) 電場からの力 $qE$ とローレンツ力 $qvB$ がつりあえば直進する。$v=\dfrac EB=\dfrac{2.0\times10^4}{0.10}=2.0\times10^5\,\mathrm{m/s}$。この速さのイオンだけが通り抜ける（速度選別器）。<br>(2) 右向きの速度と紙面の裏から表の向きの磁場では、正イオンが受けるローレンツ力 $q\vec v\times\vec B$ は下向き。電場からの力は上向きでなければならないので、電場は上向き。<br>(3) $r=\dfrac{mv}{qB'}=\dfrac{2.4\times10^{-26}\times2.0\times10^5}{1.6\times10^{-19}\times0.20}=0.15\,\mathrm m$。<br>(4) $r\propto m$ なので $m=2.4\times10^{-26}\times\dfrac{0.20}{0.15}=3.2\times10^{-26}\,\mathrm{kg}$。<br><b>ポイント</b>：速度選別器 $v=\dfrac EB$ で速さをそろえると、半径 $r=\dfrac{mv}{qB'}$ が質量に比例する（質量分析器）。"},
 {"lv": "B", "tag": "コイルの出入り", "q": r"図のように、1 辺 $a=0.10\,\mathrm m$、抵抗 $0.50\,\Omega$ の正方形の 1 巻きコイルが、紙面上を右向きに一定の速さ $0.20\,\mathrm{m/s}$ で進み、幅 $3a$ の一様な磁場（磁束密度 $0.50\,\mathrm T$、紙面の表から裏の向き）の領域を通り抜ける。コイルの辺は領域の境界と平行に保たれ、自己誘導は無視する。" + FIG_B4 + r"(1) コイルが磁場に入りつつあるとき、コイルに生じる誘導起電力と誘導電流の大きさを求めよ。また、電流の向きは紙面上で時計回り・反時計回りのどちらか。<br>(2) (1) のとき、コイルを一定の速さで動かすのに必要な外力の大きさを求めよ。<br>(3) コイル全体が磁場の中にあるとき、電流はいくらか。<br>(4) コイルが磁場に入り始めてから完全に出るまでに発生するジュール熱の合計を求めよ。また、出ていくときの電流の向きを答えよ。",
  "a": r"(1) $1.0\times10^{-2}\,\mathrm V$、$2.0\times10^{-2}\,\mathrm A$、反時計回り　(2) $1.0\times10^{-3}\,\mathrm N$　(3) $0$　(4) $2.0\times10^{-4}\,\mathrm J$、時計回り",
  "s": r"(1) 磁場の中にある右の辺だけが起電力 $Bav=0.50\times0.10\times0.20=1.0\times10^{-2}\,\mathrm V$ を生じる。$I=\dfrac{1.0\times10^{-2}}{0.50}=2.0\times10^{-2}\,\mathrm A$。紙面の表から裏への磁束が増えるので、それを妨げる表向きの磁場をつくる向き、すなわち反時計回り。<br>(2) 右の辺が受ける力 $IBa=2.0\times10^{-2}\times0.50\times0.10=1.0\times10^{-3}\,\mathrm N$（左向き）とつりあう外力が必要。<br>(3) コイルを貫く磁束が変化しないので、起電力も電流も 0。<br>(4) 入るときと出るときにそれぞれ $\dfrac av=0.50\,\mathrm s$ ずつ電流が流れる。$2\times I^2R\times0.50=2\times(2.0\times10^{-2})^2\times0.50\times0.50=2.0\times10^{-4}\,\mathrm J$。外力の仕事 $1.0\times10^{-3}\times(0.10+0.10)$ と一致する。出るときは磁束が減るので、それを補う向き（時計回り）。<br><b>ポイント</b>：誘導起電力が生じるのは「磁束が変化している間」だけ。入るときと出るときで電流の向きは逆になる。"},
 {"lv": "B", "tag": "自己誘導・相互誘導", "q": r"起電力 $E=6.0\,\mathrm V$ の電池（内部抵抗は無視）、抵抗 $R=3.0\,\Omega$、自己インダクタンス $L=0.50\,\mathrm H$ のコイル（抵抗は無視）、スイッチを直列につなぐ。<br>(1) スイッチを閉じた直後の電流、コイルに生じる自己誘導起電力の大きさ、電流の増加の割合 $\dfrac{\Delta I}{\Delta t}$ を求めよ。<br>(2) 十分時間がたったときの電流と、コイルに蓄えられたエネルギーを求めよ。<br>(3) 電流が $1.0\,\mathrm A$ のときの $\dfrac{\Delta I}{\Delta t}$ を求めよ。<br>(4) このコイルとの相互インダクタンスが $0.20\,\mathrm H$ の 2 次コイルがある。スイッチを閉じた直後に 2 次コイルに生じる誘導起電力の大きさを求めよ。",
  "a": r"(1) $0$、$6.0\,\mathrm V$、$12\,\mathrm{A/s}$　(2) $2.0\,\mathrm A$、$1.0\,\mathrm J$　(3) $6.0\,\mathrm{A/s}$　(4) $2.4\,\mathrm V$",
  "s": r"(1) コイルは電流の急な変化を妨げるので、直後の電流は 0。抵抗の電圧も 0 なので、コイルの自己誘導起電力は電池と同じ $6.0\,\mathrm V$。$L\dfrac{\Delta I}{\Delta t}=6.0$ より $\dfrac{\Delta I}{\Delta t}=12\,\mathrm{A/s}$。<br>(2) 十分後は電流が変化せず、コイルは導線と同じ。$I=\dfrac ER=2.0\,\mathrm A$、$U=\dfrac12LI^2=1.0\,\mathrm J$。<br>(3) $E=RI+L\dfrac{\Delta I}{\Delta t}$ より $\dfrac{\Delta I}{\Delta t}=\dfrac{6.0-3.0\times1.0}{0.50}=6.0\,\mathrm{A/s}$。<br>(4) $V_2=M\dfrac{\Delta I}{\Delta t}=0.20\times12=2.4\,\mathrm V$。<br><b>ポイント</b>：コイルは「直後は断線（電流が 0 のまま）、十分後は導線」。回路の式は $E=RI+L\dfrac{\Delta I}{\Delta t}$。"},
 {"lv": "C", "tag": "総合・導体棒と運動量", "q": r"水平で十分に長い 2 本の平行なレール（間隔 $l$）が、鉛直上向きで磁束密度 $B$ の一様な磁場の中にある。質量 $m$ の導体棒をレールに垂直に置く。摩擦、自己誘導、レールと棒の抵抗は無視する。<br>［Ⅰ］レールの一端を抵抗値 $R$ の抵抗でつなぎ、棒に右向きの初速 $v_0$ を与えた。<br>(1) 棒の速さが $v$ のとき、棒が受ける力の大きさを求めよ。<br>(2) 棒が止まるまでに抵抗で発生するジュール熱を求めよ。<br>(3) 短い時間 $\Delta t$ の間の運動量の変化を考えて、棒が止まるまでに進む距離 $x$ を求めよ。<br>(4) 棒が止まるまでに抵抗を流れた電気量を求めよ。<br>［Ⅱ］抵抗を電気容量 $C$ のコンデンサー（はじめ電荷 0）にかえ、棒に右向きの初速 $v_0$ を与えた。回路にはごく小さな抵抗があり、やがて電流は 0 になった。<br>(5) 十分時間がたった後の棒の速さ $v_1$ と、コンデンサーの電気量を求めよ。<br>(6) この間に回路で発生したジュール熱を求めよ。",
  "a": r"(1) $\dfrac{B^2l^2v}R$　(2) $\dfrac12mv_0^2$　(3) $\dfrac{mv_0R}{B^2l^2}$　(4) $\dfrac{mv_0}{Bl}$　(5) $v_1=\dfrac{mv_0}{m+CB^2l^2}$、電気量 $\dfrac{CBlmv_0}{m+CB^2l^2}$　(6) $\dfrac{mv_0^2}2\cdot\dfrac{CB^2l^2}{m+CB^2l^2}$",
  "s": r"(1) 起電力 $vBl$、電流 $\dfrac{vBl}R$、力 $IBl=\dfrac{B^2l^2v}R$（運動と逆向き）。<br>(2) 運動エネルギーがすべてジュール熱になる：$\dfrac12mv_0^2$。<br>(3) $m\Delta v=-\dfrac{B^2l^2}Rv\Delta t=-\dfrac{B^2l^2}R\Delta x$。これを足し合わせると $m(0-v_0)=-\dfrac{B^2l^2}Rx$、$x=\dfrac{mv_0R}{B^2l^2}$。<br>(4) $\Delta q=I\Delta t=\dfrac{Bl}R\Delta x$ を足して $q=\dfrac{Blx}R=\dfrac{mv_0}{Bl}$。（(3) の式を $m\Delta v=-Bl\,I\Delta t=-Bl\Delta q$ と見ても同じ。）<br>(5) 電流が 0 になるのは、コンデンサーの電圧が起電力 $v_1Bl$ に等しくなったとき：$Q=CBlv_1$。棒が受ける力積の合計は $-Bl\sum I\Delta t=-BlQ$ なので $mv_1-mv_0=-BlQ=-CB^2l^2v_1$。よって $v_1=\dfrac{mv_0}{m+CB^2l^2}$、$Q=\dfrac{CBlmv_0}{m+CB^2l^2}$。<br>(6) $\dfrac12mv_0^2-\dfrac12mv_1^2-\dfrac{Q^2}{2C}$。$\dfrac12mv_1^2+\dfrac{Q^2}{2C}=\dfrac12(m+CB^2l^2)v_1^2=\dfrac{m^2v_0^2}{2(m+CB^2l^2)}$ なので、ジュール熱 $=\dfrac{mv_0^2}2\cdot\dfrac{CB^2l^2}{m+CB^2l^2}$（抵抗の値によらない）。<br><b>ポイント</b>：速さに比例する力を受ける運動では、「力積 $=$ 運動量の変化」を $\Delta x$ や $\Delta q$ で書きかえると、時間を追わずに距離や電気量が求まる。"},
 {"lv": "C", "tag": "総合・磁場領域の通過", "q": r"図のように、$0\leqq x\leqq d$ の領域だけに、紙面の表から裏の向きで磁束密度 $B$ の一様な磁場がある。質量 $m$、電気量 $q\ (\gt0)$ の粒子が、原点 O から $x$ 軸の正の向きに速さ $v$ で磁場に入る。重力は無視する。" + FIG_C2 + r"(1) 磁場中での円運動の半径 $r$ と周期 $T$ を求めよ。また、粒子は $y$ 軸の正・負どちらの側へ曲がるか。<br>(2) 粒子が $x=d$ の境界から磁場の外へ出るための $v$ の条件を求めよ。<br>(3) $r=2d$ のとき、粒子が $x=d$ の境界を通過する点の $y$ 座標、そのときの速度の向きと $x$ 軸のなす角、磁場中にいた時間を求めよ。<br>(4) $r\lt d$ のとき、粒子が再び $y$ 軸を通過する点の $y$ 座標と、それまでの時間を求めよ。",
  "a": r"(1) $r=\dfrac{mv}{qB}$、$T=\dfrac{2\pi m}{qB}$、正の側　(2) $v\gt\dfrac{qBd}m$　(3) $y=(2-\sqrt3)d$、$30^\circ$、$\dfrac{\pi m}{6qB}$　(4) $y=\dfrac{2mv}{qB}$、$\dfrac{\pi m}{qB}$",
  "s": r"(1) $m\dfrac{v^2}r=qvB$ より $r=\dfrac{mv}{qB}$、$T=\dfrac{2\pi m}{qB}$。O で速度は $+x$ 向き、磁場は紙面の表から裏なので、ローレンツ力 $q\vec v\times\vec B$ は $+y$ 向き。円の中心は $(0,\ r)$ で、粒子は正の側へ曲がる。<br>(2) 円は中心 $(0,\ r)$、半径 $r$ なので、$x$ 座標の最大値は $r$。$x=d$ に届くには $r\gt d$、すなわち $v\gt\dfrac{qBd}m$。<br>(3) 中心角 $\alpha$ だけ回った点は $(r\sin\alpha,\ r(1-\cos\alpha))$。$r\sin\alpha=d$ より $\sin\alpha=\dfrac12$、$\alpha=30^\circ$。$y=2d\left(1-\dfrac{\sqrt3}2\right)=(2-\sqrt3)d$。速度の向きは回った角だけ変わるので、$x$ 軸と $30^\circ$。時間は $\dfrac{30^\circ}{360^\circ}T=\dfrac{\pi m}{6qB}$。<br>(4) 半円をえがいて $(0,\ 2r)$ に戻る。$y=\dfrac{2mv}{qB}$、時間は $\dfrac T2=\dfrac{\pi m}{qB}$。そのときの速度は $-x$ 向き。<br><b>ポイント</b>：磁場中の円運動は、まず「円の中心」を決める（速度に垂直で、力の向きに $r$ 離れた点）。出口の位置・向き・時間は中心角で表せる。"},
]}}


def _form():
    for no, ch in CH.items():
        lv = [it["lv"] for it in ch["items"]]
        assert lv.count("A") == 4 and lv.count("B") in (4, 5) and lv.count("C") == 2, lv
        for it in ch["items"]:
            for k in ("q", "a", "s", "tag"):
                assert it[k].strip(), (no, k)
            assert it["q"].count("$") % 2 == 0 and it["a"].count("$") % 2 == 0 and it["s"].count("$") % 2 == 0
            assert "<b>ポイント</b>" in it["s"]


def _sf(x, v, n):
    """x を有効数字 n 桁に丸めると v になることを確かめる"""
    assert float(f"{float(x):.{n}g}") == v, (float(x), v)


def verify():
    _form()
    R = Rational
    mu0 = 4 * pi * R(1, 10 ** 7)
    # A1
    H1 = 5 / (2 * pi * R(1, 10))
    _sf(H1, 8.0, 2)
    assert simplify(mu0 * H1 - R(1, 10 ** 5)) == 0
    assert 5 / (2 * R(1, 10)) == 25
    H3 = 2000 * 2
    assert H3 == 4000
    _sf(mu0 * H3, 5.0e-3, 2)
    # A2
    assert 3 * R(1, 2) * R(1, 5) == R(3, 10) and R(3, 10) * sin(pi / 6) == R(3, 20)
    assert simplify(mu0 * 10 * 10 / (2 * pi * R(5, 100)) - R(4, 10 ** 4)) == 0
    # A3
    m, q, B, v = 1.67e-27, 1.60e-19, 0.50, 2.0e6
    _sf(m * v / (q * B), 4.2e-2, 2); _sf(2 * 3.141592653589793 * m / (q * B), 1.3e-7, 2)
    # A4
    assert 200 * R(3, 10) * R(1, 100) / R(1, 10) == 6 and R(6, 30) == R(1, 5)
    assert R(4, 10) * 2 / R(5, 100) == 16
    # B1
    l, B, Rr, v = R(1, 2), R(2, 5), 2, 3
    emf = v * B * l
    I = emf / Rr
    assert emf == R(3, 5) and I == R(3, 10) and I * B * l == R(6, 100)
    assert I * B * l * v == I ** 2 * Rr == R(18, 100)
    # 向き：v=+x, B=+z（紙面の裏から表）→ v×B = -y（図で下向き、P→Q）
    assert Matrix([1, 0, 0]).cross(Matrix([0, 0, 1])) == Matrix([0, -1, 0])
    # B2
    m, g, th, l, B, Rr = R(1, 10), R(98, 10), pi / 6, R(7, 10), R(1, 2), R(1, 2)
    vf = m * g * Rr * sin(th) / (B ** 2 * l ** 2)
    assert vf == 2
    I = vf * B * l / Rr
    assert I == R(7, 5) and I ** 2 * Rr == R(98, 100) and m * g * sin(th) * vf == R(98, 100)
    a = g * sin(th) - B ** 2 * l ** 2 * R(1, 2) / (m * Rr)
    assert a == R(49, 10) - R(1225, 1000)
    _sf(a, 3.7, 2)
    # B3
    E, B, Bp, q = R(2, 1) * 10 ** 4, R(1, 10), R(2, 10), R(16, 10 ** 20)
    v = E / B
    assert v == 2 * 10 ** 5
    assert R(24, 10 ** 27) * v / (q * Bp) == R(15, 100)
    assert R(2, 10) * q * Bp / v == R(32, 10 ** 27)
    # 正イオン：v=+x, B=+z → 力 -y（下向き）なので電場は上向き
    assert Matrix([1, 0, 0]).cross(Matrix([0, 0, 1]))[1] < 0
    # B4
    a, Rr, v, B = R(1, 10), R(1, 2), R(1, 5), R(1, 2)
    emf = B * a * v; I = emf / Rr
    assert emf == R(1, 100) and I == R(2, 100) and I * B * a == R(1, 1000)
    assert 2 * I ** 2 * Rr * (a / v) == R(2, 10 ** 4) == I * B * a * 2 * a
    # B5
    E, Rr, L, M = 6, 3, R(1, 2), R(1, 5)
    assert E / L == 12 and R(E, Rr) == 2 and L * 2 ** 2 / 2 == 1 and (E - Rr * 1) / L == 6 and M * 12 == R(12, 5)
    # C1
    m, v0, B, l, Rr, C, x = symbols("m v_0 B l R C x", positive=True)
    t = symbols("t", positive=True)
    vt = v0 * exp(-B ** 2 * l ** 2 * t / (m * Rr))
    assert simplify(m * diff(vt, t) + B ** 2 * l ** 2 * vt / Rr) == 0
    X = integrate(vt, (t, 0, oo))
    assert simplify(X - m * v0 * Rr / (B ** 2 * l ** 2)) == 0
    assert simplify(B * l * X / Rr - m * v0 / (B * l)) == 0
    heat = integrate((vt * B * l) ** 2 / Rr, (t, 0, oo))
    assert simplify(heat - m * v0 ** 2 / 2) == 0
    v1 = symbols("v1", positive=True)
    s1 = solve(Eq(m * v1 - m * v0, -B * l * C * B * l * v1), v1)[0]
    assert simplify(s1 - m * v0 / (m + C * B ** 2 * l ** 2)) == 0
    Qf = C * B * l * s1
    J = m * v0 ** 2 / 2 - m * s1 ** 2 / 2 - Qf ** 2 / (2 * C)
    assert simplify(J - m * v0 ** 2 / 2 * C * B ** 2 * l ** 2 / (m + C * B ** 2 * l ** 2)) == 0
    # C2
    d, qq, BB, mm = symbols("d q B m", positive=True)
    r = 2 * d
    al = asin(d / r)
    assert al == pi / 6
    assert simplify(r * (1 - cos(al)) - (2 - sqrt(3)) * d) == 0
    T = 2 * pi * mm / (qq * BB)
    assert simplify(al / (2 * pi) * T - pi * mm / (6 * qq * BB)) == 0
    # 力の向き：v=+x, B=-z（表から裏）→ v×B = +y
    assert Matrix([1, 0, 0]).cross(Matrix([0, 0, -1])) == Matrix([0, 1, 0])
