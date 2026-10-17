"""問題集 第13章 光。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
from math import sin as _sin, cos as _cos, tan as _tan, asin as _asin, atan2 as _atan2, radians as _rad
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
SUB = lambda s: f'<tspan dy="3" font-size="8">{s}</tspan>'


def _fig_wedge():
    """くさび形空気層（角度は誇張）。"""
    x0, x1, yb, D = 40, 280, 96, 22
    b = [f'<rect x="{x0-8}" y="{yb}" width="{x1-x0+30}" height="12" fill="#e3edf7" stroke="#222" stroke-width="1"/>']
    # 上のガラス板（接触点 O から金属線の上まで傾く）
    ang = _atan2(D, x1 - x0)
    th = 12
    p = [(x0 - 8, yb + 8 * _sin(ang)), (x1 + 22, yb - D - 22 * _sin(ang)),
         (x1 + 22 + th * _sin(ang), yb - D - 22 * _sin(ang) - th * _cos(ang)), (x0 - 8 + th * _sin(ang), yb + 8 * _sin(ang) - th * _cos(ang))]
    b.append('<polygon points="' + " ".join(f"{a:.1f},{c:.1f}" for a, c in p) + '" fill="#e3edf7" stroke="#222" stroke-width="1"/>')
    b.append(f'<circle cx="{x1:.1f}" cy="{yb - D/2:.1f}" r="{D/2:.1f}" fill="#888" stroke="#222"/>')
    b.append(_t(x1 + 20, yb - D / 2 + 4, "金属線", 10, "start"))
    b.append(_t(x0 + 4, yb + 26, "O（接触点）", 10, "start"))
    b.append(_arrow(x0, yb + 32, x1, yb + 32, 0.8, hs=5) + _arrow(x1, yb + 32, x0, yb + 32, 0.8, hs=5))
    b.append(_t((x0 + x1) / 2, yb + 45, I("L") + " = 10.0 cm", 10))
    b.append(_ln(x1, yb + 22, x1, yb + 36, 0.6) + _ln(x0, yb + 28, x0, yb + 36, 0.6))
    for xx in (100, 150, 200):
        b.append(_arrow(xx, 6, xx, 40, 1.0, "#c0392b", 5))
    b.append(_t(212, 18, "単色光（真上から）", 10, "start"))
    return _svg(330, 150, b)


def _fig_young():
    """光源スリット S0、複スリット S1・S2、スクリーン。"""
    xs0, xs, xsc, yc, h = 34, 130, 310, 86, 22
    s1, s2 = yc - h, yc + h
    py = yc - 52
    b = [_ln(xs, 14, xs, s1 - 3, 3), _ln(xs, s1 + 3, xs, s2 - 3, 3), _ln(xs, s2 + 3, xs, 158, 3),
         _ln(xs0, 30, xs0, yc - 3, 3), _ln(xs0, yc + 3, xs0, 142, 3),
         _ln(xsc, 10, xsc, 162, 2.2, "", "#666"),
         _ln(xs0, yc, xs, s1, 0.8, "", "#1d4e89"), _ln(xs0, yc, xs, s2, 0.8, "", "#1d4e89"),
         _ln(xs, s1, xsc, py, 0.9, "", "#1d4e89"), _ln(xs, s2, xsc, py, 0.9, "", "#1d4e89"),
         _ln(xs, yc, xsc, yc, 0.7, "4,3", "#666"),
         _dot(xsc, py, 2.6), _dot(xsc, yc, 2.2),
         _t(xs0 - 4, yc - 8, "S" + SUB("0"), 11, "end"), _t(xs - 6, s1 - 6, "S" + SUB("1"), 11, "end"),
         _t(xs - 6, s2 + 14, "S" + SUB("2"), 11, "end"), _t(xsc + 6, py + 4, "P", 11, "start"),
         _t(xsc + 6, yc + 4, "O", 11, "start"), _t(xsc - 6, 14, "スクリーン", 10, "end"),
         _arrow(xs0, 174, xs, 174, 0.8, hs=5), _arrow(xs, 174, xs0, 174, 0.8, hs=5), _t((xs0 + xs) / 2, 170, I("l"), 11),
         _arrow(xs, 174, xsc, 174, 0.8, hs=5), _arrow(xsc, 174, xs, 174, 0.8, hs=5), _t((xs + xsc) / 2, 170, I("L"), 11),
         _t(xs + 12, yc + 4, I("d"), 11, "start"),
         _arrow(xsc - 14, yc, xsc - 14, py, 0.8, hs=5), _t(xsc - 18, (yc + py) / 2 + 4, I("x"), 11, "end")]
    b.append(_ln(xs + 6, s1, xs + 6, s2, 0.6))
    return _svg(340, 182, b)


def _fig_film():
    """斜めに入射した光の、薄膜の上面と下面での反射。"""
    n, i = 1.5, _rad(40)
    r = _asin(_sin(i) / n)
    yt, d, px = 70, 46, 110
    yb = yt + d
    qx = px + d * _tan(r); rx = px + 2 * d * _tan(r)
    di = (_sin(i), _cos(i))
    k = 2 * d * _tan(r) * _sin(i)
    sx, sy = rx - k * di[0], yt - k * di[1]
    L = 64
    b = [f'<rect x="20" y="{yt}" width="300" height="{d}" fill="#fbeed5"/>',
         _ln(20, yt, 320, yt, 1.1), _ln(20, yb, 320, yb, 1.1),
         _t(300, yt - 6, "空気", 10, "end"), _t(300, yt + d / 2 + 4, "膜 " + I("n"), 10, "end"), _t(300, yb + 14, "水", 10, "end"),
         _arrow(px - L * di[0], yt - L * di[1], px, yt, 1.1, "#1d4e89"),
         _ln(px, yt, qx, yb, 1.1, "", "#1d4e89"), _ln(qx, yb, rx, yt, 1.1, "", "#1d4e89"),
         _arrow(sx - L * di[0] * 0.55, sy - L * di[1] * 0.55, sx, sy, 1.1, "#c0392b"),
         _ln(sx, sy, rx, yt, 1.1, "", "#c0392b"),
         _arrow(rx, yt, rx + 58 * di[0], yt - 58 * di[1], 1.1, "#222"),
         _ln(px, sy - 2, px, yb + 10, 0.7, "3,3", "#666"),
         _ln(px, yt, sx, sy, 0.8, "2,2", "#222"),
         _dot(px, yt, 2.2), _dot(qx, yb, 2.2), _dot(rx, yt, 2.2), _dot(sx, sy, 2.2),
         _t(px - 6, yt + 14, "P", 11, "end"), _t(qx, yb + 14, "Q", 11), _t(rx + 2, yt + 14, "R", 11, "start"),
         _t(sx + 6, sy - 2, "S", 11, "start"),
         _t(px - 8, yt - 24, I("i"), 11, "end"), _t(px + 6, yt + 30, I("r"), 11, "start"),
         _arrow(40, yt, 40, yb, 0.8, hs=5), _arrow(40, yb, 40, yt, 0.8, hs=5), _t(36, yt + d / 2 + 4, I("d"), 11, "end")]
    return _svg(330, 140, b)


FIG_B3 = _fig_wedge()
FIG_C1 = _fig_young()
FIG_C2 = _fig_film()

CH = {13: {
"goal": r"屈折の法則・全反射・レンズの式を使いこなす。干渉は「光路差」と「反射による位相の変化」を整理してから条件式を立てられるようにする。",
"items": [
 {"lv": "A", "tag": "屈折率", "q": r"真空中の光の速さを $3.0\times10^8\,\mathrm{m/s}$ とする。真空中での波長が $600\,\mathrm{nm}$ の光が、屈折率 $1.5$ のガラスに入る。<br>(1) ガラス中での光の速さを求めよ。<br>(2) この光の振動数と、ガラス中での波長を求めよ。<br>(3) この光が厚さ $3.0\,\mathrm{cm}$ のガラス板を垂直に通り抜けるのにかかる時間と、ガラス板中の光学距離（光路長）を求めよ。",
  "a": r"(1) $2.0\times10^8\,\mathrm{m/s}$　(2) $5.0\times10^{14}\,\mathrm{Hz}$、$4.0\times10^2\,\mathrm{nm}$　(3) $1.5\times10^{-10}\,\mathrm s$、$4.5\,\mathrm{cm}$",
  "s": r"(1) $v=\dfrac cn=\dfrac{3.0\times10^8}{1.5}=2.0\times10^8\,\mathrm{m/s}$。<br>(2) $f=\dfrac c{\lambda_0}=\dfrac{3.0\times10^8}{600\times10^{-9}}=5.0\times10^{14}\,\mathrm{Hz}$（ガラス中でも同じ）。$\lambda=\dfrac{\lambda_0}n=400\,\mathrm{nm}$。<br>(3) $t=\dfrac{0.030}{2.0\times10^8}=1.5\times10^{-10}\,\mathrm s$。光学距離は $nl=1.5\times3.0=4.5\,\mathrm{cm}$（同じ時間に真空中を進む距離）。<br><b>ポイント</b>：媒質中では速さと波長が $\dfrac1n$ 倍、振動数は不変。光学距離 $nl$ を使うと、媒質中の経路も真空中の長さに換算して比べられる。"},
 {"lv": "A", "tag": "全反射", "q": r"水の屈折率を $\dfrac43$ とする。<br>(1) 水から空気へ光が進むときの臨界角を $\theta_c$ として、$\sin\theta_c$ を求めよ。<br>(2) 深さ $0.60\,\mathrm m$ の水槽の底に点光源を置いた。水面から光が出てくる範囲は円になる。その半径を求めよ。$\sqrt7=2.65$ とする。<br>(3) この光源を真上から見ると、水面から何 m の深さにあるように見えるか。見る向きは鉛直に近く、角度は小さいとする。",
  "a": r"(1) $\dfrac34$　(2) $0.68\,\mathrm m$　(3) $0.45\,\mathrm m$",
  "s": r"(1) 屈折角 $90^\circ$ となる入射角が臨界角。$\dfrac43\sin\theta_c=1\cdot\sin90^\circ$ より $\sin\theta_c=\dfrac34$。<br>(2) 入射角が $\theta_c$ 以上の光は全反射して出てこない。円の半径は $r=h\tan\theta_c$。$\cos\theta_c=\sqrt{1-\frac9{16}}=\dfrac{\sqrt7}4$ より $\tan\theta_c=\dfrac3{\sqrt7}$。$r=0.60\times\dfrac{3}{2.65}\fallingdotseq0.68\,\mathrm m$。<br>(3) 水中で鉛直と角 $\alpha$ をなす光が、空気中で角 $\beta$ で出るとする（$\sin\beta=n\sin\alpha$）。見かけの深さ $h'$ は $h'\tan\beta=h\tan\alpha$ を満たし、角が小さいとき $\tan\fallingdotseq\sin$ なので $h'=h\dfrac{\sin\alpha}{\sin\beta}=\dfrac hn=0.60\times\dfrac34=0.45\,\mathrm m$。<br><b>ポイント</b>：全反射は屈折率の大きい側から小さい側へ進むときだけ起こる。真上から見た見かけの深さは $\dfrac hn$。"},
 {"lv": "A", "tag": "レンズ", "q": r"焦点距離 $10\,\mathrm{cm}$ の凸レンズがある。<br>(1) レンズの前方 $15\,\mathrm{cm}$ の位置に物体を置いた。像の位置、倍率、像の種類（実像・虚像、正立・倒立）を答えよ。<br>(2) 物体をレンズの前方 $6.0\,\mathrm{cm}$ の位置に置いたときについて、同じことを答えよ。",
  "a": r"(1) 後方 $30\,\mathrm{cm}$、$2.0$ 倍、倒立の実像　(2) 前方 $15\,\mathrm{cm}$（物体と同じ側）、$2.5$ 倍、正立の虚像",
  "s": r"レンズの式 $\dfrac1a+\dfrac1b=\dfrac1f$、倍率 $m=\left|\dfrac ba\right|$。<br>(1) $\dfrac1{15}+\dfrac1b=\dfrac1{10}$ より $b=30\,\mathrm{cm}$（$b\gt0$：後方に実像、倒立）。$m=\dfrac{30}{15}=2.0$。<br>(2) $\dfrac1{6.0}+\dfrac1b=\dfrac1{10}$ より $\dfrac1b=-\dfrac1{15}$、$b=-15\,\mathrm{cm}$。$b\lt0$ なのでレンズの前方 $15\,\mathrm{cm}$ に正立の虚像。$m=\dfrac{15}{6.0}=2.5$（虫めがねの使い方）。<br><b>ポイント</b>：$b\gt0$ なら後方の倒立実像、$b\lt0$ なら前方の正立虚像。物体が焦点の内側にあると虚像になる。"},
 {"lv": "A", "tag": "ヤングの実験", "q": r"間隔 $d=0.20\,\mathrm{mm}$ の複スリットに波長 $600\,\mathrm{nm}$ の単色光を当て、$L=1.0\,\mathrm m$ 離れたスクリーン上に干渉じまをつくる。<br>(1) スクリーンの中央 O から $x$ の位置での経路差が $\dfrac{dx}L$ で近似できるものとして、明線の間隔を求めよ。<br>(2) 波長 $480\,\mathrm{nm}$ の光に替えると、明線の間隔はいくらになるか。<br>(3) 波長 $600\,\mathrm{nm}$ のままで明線の間隔を $6.0\,\mathrm{mm}$ にするには、スリット間隔をいくらにすればよいか。",
  "a": r"(1) $3.0\,\mathrm{mm}$　(2) $2.4\,\mathrm{mm}$　(3) $0.10\,\mathrm{mm}$",
  "s": r"(1) 明線の条件 $\dfrac{dx}L=m\lambda$ より $x_m=\dfrac{mL\lambda}d$、間隔 $\Delta x=\dfrac{L\lambda}d=\dfrac{1.0\times600\times10^{-9}}{0.20\times10^{-3}}=3.0\times10^{-3}\,\mathrm m$。<br>(2) $\Delta x\propto\lambda$ より $3.0\times\dfrac{480}{600}=2.4\,\mathrm{mm}$。<br>(3) $\Delta x\propto\dfrac1d$ より $d=0.20\times\dfrac{3.0}{6.0}=0.10\,\mathrm{mm}$。<br><b>ポイント</b>：$\Delta x=\dfrac{L\lambda}d$。「$L$ と $\lambda$ に比例、$d$ に反比例」を式から読みとれるようにする。"},
 {"lv": "B", "tag": "回折格子", "q": r"$1\,\mathrm{mm}$ あたり 500 本の溝がある回折格子に、波長 $500\,\mathrm{nm}$ の単色光を垂直に当て、格子から $1.0\,\mathrm m$ 離れた、格子に平行なスクリーンで観察する。スクリーンは十分に大きい。<br>(1) 格子定数 $d$ を求めよ。<br>(2) 1 次の回折光の回折角を $\theta_1$ として、$\sin\theta_1$ を求めよ。<br>(3) スクリーン上での、中央の明線と 1 次の明線の距離を求めよ。$\sqrt{15}=3.87$ とする。<br>(4) スクリーン上に現れる明線は、中央の明線を含めて全部で何本か。<br>(5) 白色光を当てると、1 次のスペクトルのうち中央に近い側は何色になるか。",
  "a": r"(1) $2.0\times10^{-6}\,\mathrm m$　(2) $0.25$　(3) $0.26\,\mathrm m$　(4) $7$ 本　(5) 紫色",
  "s": r"(1) $d=\dfrac{1\times10^{-3}}{500}=2.0\times10^{-6}\,\mathrm m$。<br>(2) 明線の条件 $d\sin\theta=m\lambda$ より $\sin\theta_1=\dfrac{500\times10^{-9}}{2.0\times10^{-6}}=0.25$。<br>(3) $\cos\theta_1=\sqrt{1-0.25^2}=\dfrac{\sqrt{15}}4$、$\tan\theta_1=\dfrac1{\sqrt{15}}$。距離は $1.0\times\tan\theta_1=\dfrac{1}{3.87}\fallingdotseq0.26\,\mathrm m$（回折角が大きいので $\tan\theta\fallingdotseq\sin\theta$ の近似は使えない）。<br>(4) $\sin\theta=\dfrac{m\lambda}d=0.25m\lt1$ より $|m|\leqq3$（$m=4$ では $\theta=90^\circ$ でスクリーンに届かない）。$m=0,\ \pm1,\ \pm2,\ \pm3$ の 7 本。<br>(5) $\sin\theta\propto\lambda$ なので、波長の短い紫が中央に近い。<br><b>ポイント</b>：回折格子は回折角が大きいので、$x=L\tan\theta$ を正しく使う。見える次数の上限は $\sin\theta\lt1$ から決める。"},
 {"lv": "B", "tag": "薄膜の干渉", "q": r"可視光の波長を $400\,\mathrm{nm}$〜$700\,\mathrm{nm}$ とする。<br>空気中にある屈折率 $1.33$、厚さ $300\,\mathrm{nm}$ のせっけん膜に、白色光を垂直に当てて反射光を観察する。<br>(1) 膜の上面での反射と下面での反射のそれぞれで、光の位相は反転するか。<br>(2) 反射光が強め合う条件を、膜の厚さ $d$、屈折率 $n$、真空中の波長 $\lambda$、整数 $m\ (\geqq0)$ で表せ。<br>(3) 反射光が強め合う可視光の波長を求めよ。<br>(4) 次に、屈折率 $1.50$ のガラスの表面に屈折率 $1.38$ の薄膜をつけて、垂直に入射する波長 $550\,\mathrm{nm}$ の光の反射を弱めたい。膜の厚さの最小値を求めよ。",
  "a": r"(1) 上面では反転する、下面では反転しない　(2) $2nd=\left(m+\dfrac12\right)\lambda$　(3) $532\,\mathrm{nm}$　(4) $99.6\,\mathrm{nm}\ (\fallingdotseq1.0\times10^2\,\mathrm{nm})$",
  "s": r"(1) 屈折率の小さい側から大きい側への境界で反射すると位相が $\pi$ ずれる（反転）。上面（空気→膜）は反転、下面（膜→空気）は反転しない。<br>(2) 光路差は $2nd$。反射による位相のずれが片方だけなので、条件が入れかわって $2nd=\left(m+\dfrac12\right)\lambda$ で強め合う。<br>(3) $2nd=2\times1.33\times300=798\,\mathrm{nm}$。$\lambda=\dfrac{798}{m+0.5}$ は $m=0,1,2$ で $1596,\ 532,\ 319.2\,\mathrm{nm}$。可視光は $532\,\mathrm{nm}$（緑色）。<br>(4) 空気→膜（$1.00\to1.38$）も膜→ガラス（$1.38\to1.50$）も反転するので、ずれは打ち消しあい、弱め合う条件は $2nd=\left(m+\dfrac12\right)\lambda$。最小は $m=0$ で $d=\dfrac{\lambda}{4n}=\dfrac{550}{4\times1.38}\fallingdotseq99.6\,\mathrm{nm}$。<br><b>ポイント</b>：干渉条件は (i) 光路差、(ii) 反射による反転の回数、の 2 つで決まる。反転が 1 回なら「強め合い・弱め合い」の条件が入れかわる。"},
 {"lv": "B", "tag": "くさび形空気層", "q": r"図のように 2 枚の平面ガラス板を重ね、一端 O を接触させ、O から $L=10.0\,\mathrm{cm}$ の位置に細い金属線をはさんだ。真上から波長 $600\,\mathrm{nm}$ の単色光を当てて真上から見ると、平行な暗線が間隔 $1.50\,\mathrm{mm}$ で等間隔に並んで見えた。" + FIG_B3 + r"(1) 接触点 O の位置は明線か暗線か。理由とともに答えよ。<br>(2) 金属線の直径 $D$ を求めよ。<br>(3) ガラス板の間を屈折率 $1.33$ の水で満たすと、暗線の間隔はいくらになるか。",
  "a": r"(1) 暗線（解説参照）　(2) $2.0\times10^{-5}\,\mathrm m$　(3) $1.13\,\mathrm{mm}$",
  "s": r"(1) O では空気層の厚さが 0 で経路差 0。上のガラスの下面（ガラス→空気）では反転せず、下のガラスの上面（空気→ガラス）で反射すると反転するので、2 つの反射光は逆位相で弱め合う。よって暗線。<br>(2) O から $x$ の位置の空気層の厚さは $\dfrac{Dx}L$。暗線の条件は $2\cdot\dfrac{Dx}L=m\lambda$ なので、間隔は $\Delta x=\dfrac{L\lambda}{2D}$。$D=\dfrac{L\lambda}{2\Delta x}=\dfrac{0.100\times600\times10^{-9}}{2\times1.50\times10^{-3}}=2.0\times10^{-5}\,\mathrm m$。<br>(3) 水（$1.33\lt1.50$）でも反転の様子は同じで、光路差が $2n\dfrac{Dx}L$ になる。$\Delta x'=\dfrac{\Delta x}n=\dfrac{1.50}{1.33}\fallingdotseq1.13\,\mathrm{mm}$。<br><b>ポイント</b>：くさびの縞の間隔は「厚さが $\dfrac{\lambda}{2n}$ 増えるごとに 1 本」。$D$ や $\lambda$ の測定に使われる。"},
 {"lv": "B", "tag": "ニュートンリング", "q": r"曲率半径 $R=2.0\,\mathrm m$ の平凸レンズの凸面を平面ガラスの上に置き、真上から波長 $600\,\mathrm{nm}$ の単色光を当て、反射光を真上から観察すると、同心円状の明暗の環が見えた。<br>(1) 中心から距離 $r$ の位置の空気層の厚さ $d$ が、$d\fallingdotseq\dfrac{r^2}{2R}$ と近似できることを示せ（$d\ll R$）。<br>(2) 暗環ができる条件を、$r,\ R,\ \lambda$ と整数 $m$ で表せ。<br>(3) 中心の暗点を除いて、中心から数えて 5 番目の暗環の半径を求めよ。<br>(4) 平面ガラスの下側から透過光を観察すると、中心は明るいか暗いか。",
  "a": r"(1) 解説参照　(2) $\dfrac{r^2}R=m\lambda$（$m=0,1,2,\cdots$）　(3) $2.4\times10^{-3}\,\mathrm m$　(4) 明るい",
  "s": r"(1) レンズの球面の中心から見た三平方の定理より $(R-d)^2+r^2=R^2$、$r^2=2Rd-d^2$。$d\ll R$ なので $d^2$ を無視して $d\fallingdotseq\dfrac{r^2}{2R}$。<br>(2) 光路差は $2d=\dfrac{r^2}R$。反転は下の平面ガラスの上面（空気→ガラス）での 1 回だけなので、暗環の条件は $\dfrac{r^2}R=m\lambda$。<br>(3) 中心（$m=0$）が暗点なので、5 番目の暗環は $m=5$。$r=\sqrt{5R\lambda}=\sqrt{5\times2.0\times600\times10^{-9}}=\sqrt{6.0\times10^{-6}}\fallingdotseq2.4\times10^{-3}\,\mathrm m$。<br>(4) 透過光では、そのまま通り抜ける光と、空気層の中で 2 回反射してから通り抜ける光が干渉する。2 回の反射（平面ガラスの上面と、レンズの下面）はどちらも空気→ガラスの境界での反射なので、それぞれ反転し、合わせると位相のずれはなくなる。中心では経路差も 0 なので強め合い、明るい。反射光で暗い所は透過光では明るく、明暗が逆になる（エネルギー保存とも合う）。<br><b>ポイント</b>：ニュートンリングの半径は $\sqrt m$ に比例し、外側ほど環の間隔がつまる。反射光と透過光では明暗が逆になる。"},
 {"lv": "B", "tag": "レンズの組合せ", "q": r"焦点距離 $10\,\mathrm{cm}$ の凸レンズ $\mathrm{L_1}$ の前方 $15\,\mathrm{cm}$ に物体を置く。$\mathrm{L_1}$ の後方 $50\,\mathrm{cm}$ の位置に、焦点距離 $10\,\mathrm{cm}$ の凸レンズ $\mathrm{L_2}$ を光軸をそろえて置く。<br>(1) $\mathrm{L_1}$ だけによる像の位置を求めよ。<br>(2) $\mathrm{L_2}$ による最終的な像の位置を求め、実像か虚像かを答えよ。<br>(3) 最終的な像の倍率を求め、物体に対して正立か倒立かを答えよ。<br>(4) $\mathrm{L_2}$ を焦点距離 $10\,\mathrm{cm}$ の凹レンズに替えると、最終的な像はどこにできるか。",
  "a": r"(1) $\mathrm{L_1}$ の後方 $30\,\mathrm{cm}$　(2) $\mathrm{L_2}$ の後方 $20\,\mathrm{cm}$、実像　(3) $2.0$ 倍、正立　(4) $\mathrm{L_2}$ の前方（$\mathrm{L_1}$ 側）$6.7\,\mathrm{cm}$ の位置（虚像）",
  "s": r"(1) $\dfrac1{15}+\dfrac1b=\dfrac1{10}$ より $b=30\,\mathrm{cm}$。<br>(2) この像は $\mathrm{L_2}$ の前方 $50-30=20\,\mathrm{cm}$ にあり、$\mathrm{L_2}$ の物体になる。$\dfrac1{20}+\dfrac1{b'}=\dfrac1{10}$ より $b'=20\,\mathrm{cm}$。後方にできるので実像。<br>(3) 倍率は $\dfrac{30}{15}\times\dfrac{20}{20}=2.0$。$\mathrm{L_1}$ で倒立、$\mathrm{L_2}$ でさらに倒立するので、物体に対しては正立。<br>(4) 凹レンズは $f=-10\,\mathrm{cm}$ として $\dfrac1{20}+\dfrac1{b''}=-\dfrac1{10}$ より $b''=-\dfrac{20}3\fallingdotseq-6.7\,\mathrm{cm}$。$\mathrm{L_2}$ の前方 $6.7\,\mathrm{cm}$ に虚像ができる。<br><b>ポイント</b>：組合せレンズは「1 枚目の像を 2 枚目の物体」として順に計算する。倍率は掛け算、倒立の回数で向きが決まる。"},
 {"lv": "C", "tag": "総合・ヤングの実験の応用", "q": r"図のように、単スリット $\mathrm{S_0}$、その $l=0.20\,\mathrm m$ 後方に間隔 $d=0.50\,\mathrm{mm}$ の複スリット $\mathrm{S_1}$、$\mathrm{S_2}$、さらに $L=1.0\,\mathrm m$ 後方にスクリーンを置き、波長 $500\,\mathrm{nm}$ の単色光で干渉じまをつくる。はじめ $\mathrm{S_0}$ は $\mathrm{S_1S_2}$ の垂直二等分線上にあり、O はその線とスクリーンの交点である。経路差は、スクリーン上では $\dfrac{dx}L$、$\mathrm{S_0}$ 側では $\mathrm{S_0}$ のずれを $s$ として $\dfrac{ds}l$ で近似できる。" + FIG_C1 + r"(1) 明線の間隔を求めよ。<br>(2) $\mathrm{S_1}$ の直後を、厚さ $6.0\,\mu\mathrm m$、屈折率 $1.5$ の薄いガラス板でおおった。中央の明線（全経路の光路差が 0 の明線）は、$\mathrm{S_1}$ 側・$\mathrm{S_2}$ 側のどちらへ何 mm 移動するか。<br>(3) ガラス板を取り除き、$\mathrm{S_0}$ を $\mathrm{S_1}$ 側へ $s=0.10\,\mathrm{mm}$ ずらした。中央の明線はどちらへ何 mm 移動するか。<br>(4) $\mathrm{S_0}$ を元に戻し、ガラス板もない状態で、装置全体を屈折率 $\dfrac43$ の水中に入れると、明線の間隔はいくらになるか。<br>(5) (2) のガラス板をつけたまま、$\mathrm{S_0}$ をずらして中央の明線を O に戻したい。$\mathrm{S_0}$ をどちら側へ何 mm ずらせばよいか。",
  "a": r"(1) $1.0\,\mathrm{mm}$　(2) $\mathrm{S_1}$ 側へ $6.0\,\mathrm{mm}$　(3) $\mathrm{S_2}$ 側へ $0.50\,\mathrm{mm}$　(4) $0.75\,\mathrm{mm}$　(5) $\mathrm{S_1}$ 側へ $1.2\,\mathrm{mm}$",
  "s": r"スクリーン上の位置 $x$ は $\mathrm{S_1}$ 側を正にとる。$\mathrm{S_2P}-\mathrm{S_1P}\fallingdotseq\dfrac{dx}L$。<br>(1) $\Delta x=\dfrac{L\lambda}d=\dfrac{1.0\times500\times10^{-9}}{0.50\times10^{-3}}=1.0\times10^{-3}\,\mathrm m$。<br>(2) $\mathrm{S_1}$ を通る経路の光路長が $(n-1)t=0.5\times6.0\,\mu\mathrm m=3.0\,\mu\mathrm m$ 増える。全光路差 0 の条件は $\mathrm{S_1P}+(n-1)t=\mathrm{S_2P}$、すなわち $\dfrac{dx}L=(n-1)t$。$x=\dfrac{L(n-1)t}d=\dfrac{1.0\times3.0\times10^{-6}}{0.50\times10^{-3}}=6.0\times10^{-3}\,\mathrm m$。$x\gt0$ なので $\mathrm{S_1}$ 側へ $6.0\,\mathrm{mm}$（明線 6 本分）。<br>(3) $\mathrm{S_0}$ が $\mathrm{S_1}$ 側へ $s$ ずれると $\mathrm{S_0S_2}-\mathrm{S_0S_1}\fallingdotseq\dfrac{ds}l$。条件 $\mathrm{S_0S_1}+\mathrm{S_1P}=\mathrm{S_0S_2}+\mathrm{S_2P}$ より $\dfrac{dx}L=-\dfrac{ds}l$、$x=-\dfrac{Ls}l=-\dfrac{1.0\times0.10}{0.20}=-0.50\,\mathrm{mm}$。$\mathrm{S_2}$ 側へ $0.50\,\mathrm{mm}$。<br>(4) 水中では波長が $\dfrac{\lambda}n$ になるので $\Delta x=\dfrac{1.0}{4/3}=0.75\,\mathrm{mm}$。<br>(5) O（$x=0$）で全光路差 0 にするには $\mathrm{S_0S_1}+(n-1)t=\mathrm{S_0S_2}$、すなわち $\dfrac{ds}l=(n-1)t$。$s=\dfrac{l(n-1)t}d=\dfrac{0.20\times3.0\times10^{-6}}{0.50\times10^{-3}}=1.2\times10^{-3}\,\mathrm m$。$\mathrm{S_0S_2}\gt\mathrm{S_0S_1}$ となる向き、すなわち $\mathrm{S_1}$ 側へ $1.2\,\mathrm{mm}$（(3) より $\mathrm{S_0}$ を $\mathrm{S_1}$ 側へずらすと縞は $\mathrm{S_2}$ 側へ動くので、(2) の移動を打ち消せる）。<br><b>ポイント</b>：中央の明線は「光源からスクリーンまでの全光路差が 0 の点」。ガラス板は光路を $(n-1)t$ 延ばし、縞はその側へ動く。光源をずらすと縞は逆側へ動く。"},
 {"lv": "C", "tag": "総合・斜め入射の薄膜", "q": r"水（屈折率 $1.33$）の上に、屈折率 $n=1.50$、厚さ $d=0.30\,\mu\mathrm m$ の油膜が一様に広がっている。空気中から入射角 $i$ で光を当て、反射光を観察する。可視光の波長を $400\,\mathrm{nm}$〜$700\,\mathrm{nm}$ とする。" + FIG_C2 + r"(1) 図のように、点 P で膜に入り、下面の Q で反射して上面の R から出る光と、R で直接反射する光を比べる。P から入射光に垂直に引いた線と、R へ向かう光との交点を S とする。膜内の屈折角を $r$ として、2 つの光の光路差が $2nd\cos r$ になることを示せ。<br>(2) 上面・下面での反射による位相の変化を考えて、反射光が強め合う条件を書け。<br>(3) 真上から見る（$i=0$）とき、強め合う可視光の波長を求めよ。<br>(4) $\sin i=0.90$ の向きから見るとき、強め合う可視光の波長を求めよ。<br>(5) 見る向きを真上から斜めに傾けていくと、強め合う色は波長の長い側・短い側のどちらへ移るか。理由とともに答えよ。",
  "a": r"(1) 解説参照　(2) $2nd\cos r=\left(m+\dfrac12\right)\lambda$（$m=0,1,2,\cdots$）　(3) $600\,\mathrm{nm}$　(4) $480\,\mathrm{nm}$　(5) 短い側（$\cos r$ が小さくなり光路差が減るため）",
  "s": r"(1) 光路差 $=n(\mathrm{PQ}+\mathrm{QR})-\mathrm{SR}$。$\mathrm{PQ}=\mathrm{QR}=\dfrac d{\cos r}$、$\mathrm{PR}=2d\tan r$。$\mathrm{SR}=\mathrm{PR}\sin i=2d\tan r\cdot n\sin r$（屈折の法則 $\sin i=n\sin r$）。<br>よって光路差 $=\dfrac{2nd}{\cos r}-\dfrac{2nd\sin^2r}{\cos r}=\dfrac{2nd(1-\sin^2r)}{\cos r}=2nd\cos r$。<br>(2) 上面（空気→油：$1.00\to1.50$）で反転、下面（油→水：$1.50\to1.33$）では反転しない。反転が 1 回なので、$2nd\cos r=\left(m+\dfrac12\right)\lambda$ で強め合う。<br>(3) $2nd=2\times1.50\times300=900\,\mathrm{nm}$。$\lambda=\dfrac{900}{m+0.5}=1800,\ 600,\ 360,\ \cdots$ より $600\,\mathrm{nm}$（橙色）。<br>(4) $\sin r=\dfrac{0.90}{1.50}=0.60$、$\cos r=0.80$。$2nd\cos r=720\,\mathrm{nm}$。$\lambda=\dfrac{720}{m+0.5}=1440,\ 480,\ 288,\ \cdots$ より $480\,\mathrm{nm}$（青色）。<br>(5) $i$ を大きくすると $r$ も大きくなって $\cos r$ が減り、光路差 $2nd\cos r$ が短くなる。同じ $m$ で強め合う波長は短くなるので、色は短い波長側へ移る。シャボン玉や油膜の色が見る角度で変わるのはこのため。<br><b>ポイント</b>：斜め入射の光路差 $2nd\cos r$ は、膜内の往復 $\dfrac{2nd}{\cos r}$ から、空気中の余分な距離 SR を引いたもの。$\cos i$ ではなく<b>膜内の屈折角</b> $r$ の $\cos$ であることに注意。"},
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
    # A1
    c, n, l0 = R(3, 1) * 10 ** 8, R(3, 2), R(600) * R(1, 10 ** 9)
    assert c / n == 2 * 10 ** 8 and c / l0 == 5 * 10 ** 14 and l0 / n == R(400, 10 ** 9)
    assert R(3, 100) / (c / n) == R(15, 10 ** 11) and n * 3 == R(9, 2)
    # A2
    n = R(4, 3)
    sc = 1 / n
    assert sc == R(3, 4)
    tc = sc / sqrt(1 - sc ** 2)
    assert simplify(tc - 3 / sqrt(7)) == 0
    _sf(0.60 * 3 / 2.65, 0.68, 2); _sf(R(6, 10) * tc, 0.68, 2)
    assert R(6, 10) / n == R(45, 100)
    # A3
    a, b, f = symbols("a b f")
    lens = lambda a, f: 1 / (R(1) / f - R(1) / a)
    assert lens(15, 10) == 30 and lens(6, 10) == -15 and R(30, 15) == 2 and R(15, 6) == R(5, 2)
    # A4
    dx = lambda L, lam, d: L * lam / d
    assert dx(1, R(600, 10 ** 9), R(2, 10 ** 4)) == R(3, 1000)
    assert dx(1, R(480, 10 ** 9), R(2, 10 ** 4)) == R(24, 10 ** 4)
    assert solve(Eq(dx(1, R(600, 10 ** 9), symbols("d")), R(6, 1000)))[0] == R(1, 10 ** 4)
    # B1
    d = R(1, 1000) / 500; lam = R(500, 10 ** 9)
    assert d == R(2, 10 ** 6) and lam / d == R(1, 4)
    s1 = lam / d; t1 = s1 / sqrt(1 - s1 ** 2)
    assert simplify(t1 - 1 / sqrt(15)) == 0
    _sf(t1, 0.26, 2); _sf(1 / 3.87, 0.26, 2)
    assert len([m for m in range(-10, 11) if abs(m * lam / d) < 1]) == 7
    # B2
    opd = 2 * R(133, 100) * 300
    wl = [opd / (m + R(1, 2)) for m in range(0, 6)]
    assert [w for w in wl if 400 <= w <= 700] == [532]
    _sf(R(550) / (4 * R(138, 100)), 99.6, 3)
    # B3
    D = R(1, 10) * R(600, 10 ** 9) / (2 * R(15, 10000))
    assert D == R(2, 10 ** 5)
    _sf(R(150, 100) / R(133, 100), 1.13, 3)
    # B4
    Rr, d_, r_ = symbols("R d r", positive=True)
    exact = solve(Eq((Rr - d_) ** 2 + r_ ** 2, Rr ** 2), d_)
    small = [e for e in exact if limit(e.subs(r_, 0), Rr, 2) == 0][0]
    assert simplify(series(small, r_, 0, 3).removeO() - r_ ** 2 / (2 * Rr)) == 0
    _sf(sqrt(5 * 2 * R(600, 10 ** 9)), 0.0024, 2)
    # B5
    b1 = lens(15, 10); b2 = lens(50 - b1, 10); b3 = lens(50 - b1, -10)
    assert b1 == 30 and b2 == 20 and R(b1, 15) * R(b2, 20) == 2 and b3 == R(-20, 3)
    _sf(-b3, 6.7, 2)
    # C1
    L, lam, d, l, t, n = 1, R(500, 10 ** 9), R(5, 10 ** 4), R(2, 10), R(6, 10 ** 6), R(3, 2)
    assert L * lam / d == R(1, 1000)
    assert L * (n - 1) * t / d == R(6, 1000)
    assert L * R(1, 10 ** 4) / l == R(5, 10 ** 4)
    assert (L * lam / d) / R(4, 3) == R(75, 10 ** 5)
    assert l * (n - 1) * t / d == R(12, 10 ** 4)
    # C2
    n, d = R(3, 2), 300
    ii, rr = symbols("i r", positive=True)
    dd, nn = symbols("d n", positive=True)
    opd = nn * 2 * dd / cos(rr) - 2 * dd * tan(rr) * nn * sin(rr)
    assert simplify(opd - 2 * nn * dd * cos(rr)) == 0
    wl0 = [2 * n * d / (m + R(1, 2)) for m in range(6)]
    assert [w for w in wl0 if 400 <= w <= 700] == [600]
    sr = R(9, 10) / n; cr = sqrt(1 - sr ** 2)
    assert sr == R(3, 5) and cr == R(4, 5)
    wl1 = [2 * n * d * cr / (m + R(1, 2)) for m in range(6)]
    assert [w for w in wl1 if 400 <= w <= 700] == [480]
