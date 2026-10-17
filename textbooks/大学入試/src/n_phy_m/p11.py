"""問題集 第11章 波の性質。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
from math import sin as _sin, cos as _cos, pi as _pi, atan2 as _atan2, radians as _rad
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


def _fig_wave(sign=1, labels=True):
    """y = sign*0.10 sin(pi x/2)（0<=x<=8 m）の t=0 の波形。1 m ごとに補助線。"""
    ox, oy, sx, sy = 40, 70, 30, 400
    X = lambda x: ox + sx * x
    Y = lambda y: oy - sy * y
    b = []
    for i in range(1, 9):
        b.append(_ln(X(i), Y(0.10), X(i), Y(-0.10), 0.6, "2,2", "#999"))
        b.append(_t(X(i), Y(-0.10) + 26, str(i), 10))
    b.append(_ln(X(0), Y(0.10), X(8), Y(0.10), 0.6, "2,2", "#999"))
    b.append(_ln(X(0), Y(-0.10), X(8), Y(-0.10), 0.6, "2,2", "#999"))
    b.append(_arrow(X(0) - 6, oy, X(8) + 22, oy))
    b.append(_arrow(X(0), Y(-0.10) - (-14), X(0), Y(0.10) - 18))
    b.append(_t(X(8) + 30, oy + 15, I("x") + " [m]", 11, "end"))
    b.append(_t(X(0) - 5, Y(0.10) - 12, I("y") + " [m]", 11, "end"))
    b.append(_t(X(0) - 4, Y(0.10) + 4, "0.10", 10, "end"))
    b.append(_t(X(0) - 4, Y(-0.10) + 4, "−0.10", 10, "end"))
    b.append(_t(X(0) - 4, oy + 14, "O", 10, "end"))
    pts = [(X(k / 40), Y(sign * 0.10 * _sin(_pi * (k / 40) / 2))) for k in range(321)]
    b.append(_curve(pts))
    b.append(_arrow(X(6.0), Y(0.10) - 9, X(7.6), Y(0.10) - 9, 1.4))
    b.append(_t(X(5.9), Y(0.10) - 5, "進む向き", 10, "end"))
    if labels:
        for x, nm, dx, dy in [(1, "a", 0, -7), (2, "b", 8, -6), (3, "c", 0, 16), (4, "d", -8, -6)]:
            y = sign * 0.10 * _sin(_pi * x / 2)
            b.append(_dot(X(x), Y(y)))
            b.append(_t(X(x) + dx, Y(y) + dy, nm, 11))
    return _svg(330, 150, b)


def _fig_yt():
    """原点の振動 y = 0.050 sin(pi t)（0<=t<=4 s）。"""
    ox, oy, sx, sy = 46, 62, 55, 800
    X = lambda t: ox + sx * t
    Y = lambda y: oy - sy * y
    b = []
    for i in range(1, 5):
        b.append(_ln(X(i), Y(0.05), X(i), Y(-0.05), 0.6, "2,2", "#999"))
        b.append(_t(X(i), Y(-0.05) + 16, f"{i}.0", 10))
    b.append(_ln(X(0), Y(0.05), X(4), Y(0.05), 0.6, "2,2", "#999"))
    b.append(_ln(X(0), Y(-0.05), X(4), Y(-0.05), 0.6, "2,2", "#999"))
    b.append(_arrow(X(0) - 6, oy, X(4) + 24, oy))
    b.append(_arrow(X(0), Y(-0.05) + 12, X(0), Y(0.05) - 16))
    b.append(_t(X(4) + 32, oy + 15, I("t") + " [s]", 11, "end"))
    b.append(_t(X(0) - 5, Y(0.05) - 10, I("y") + " [m]", 11, "end"))
    b.append(_t(X(0) - 4, Y(0.05) + 4, "0.050", 10, "end"))
    b.append(_t(X(0) - 4, Y(-0.05) + 4, "−0.050", 10, "end"))
    b.append(_t(X(0) - 4, oy + 14, "O", 10, "end"))
    pts = [(X(k / 40), Y(0.05 * _sin(_pi * k / 40))) for k in range(161)]
    b.append(_curve(pts))
    return _svg(330, 130, b)


def _fig_two():
    """2 波源 S1, S2 と遠方の点 P の向き（角 θ）。"""
    s1, s2, yb = 110, 210, 130
    m = (s1 + s2) / 2
    th = _rad(30)
    px, py = m + 118 * _sin(th), yb - 118 * _cos(th)
    b = [_ln(m, yb + 8, m, 14, 0.9, "4,3", "#666"),
         _ln(s1 - 30, yb, s2 + 30, yb, 0.8, "", "#999"),
         _ln(s1, yb, px, py, 1.0), _ln(s2, yb, px, py, 1.0), _ln(m, yb, px, py, 1.2, "", "#1d4e89"),
         _dot(s1, yb, 3.2), _dot(s2, yb, 3.2), _dot(m, yb, 2.2), _dot(px, py, 3.0, "#1d4e89"),
         _t(s1, yb + 18, "S" + SUB("1")), _t(s2, yb + 18, "S" + SUB("2")), _t(m, yb + 18, "M"),
         _t(px + 10, py - 4, "P（十分遠方）", 11, "start")]
    r = 30
    arc = [(m + r * _sin(a / 20 * th), yb - r * _cos(a / 20 * th)) for a in range(21)]
    b.append(_curve(arc, 0.9, "#222"))
    b.append(_t(m + 40 * _sin(th / 2), yb - 40 * _cos(th / 2) + 4, I("θ")))
    return _svg(320, 152, b)


FIG_A2 = _fig_wave(1, True)
FIG_A3 = _fig_wave(-1, False)
FIG_B2 = _fig_yt()
FIG_C2 = _fig_two()

CH = {11: {
"goal": r"$y$-$x$ グラフと $y$-$t$ グラフを読み分け、波の式を立てられるようにする。反射・定常波・干渉・屈折を、位相と経路差で説明できるようにする。",
"items": [
 {"lv": "A", "tag": "基本計算", "q": r"振動数 $5.0\,\mathrm{Hz}$ で振動する波源から、$x$ 軸の正の向きに速さ $2.0\,\mathrm{m/s}$ で正弦波が送り出されている。<br>(1) 波の周期 $T$ と波長 $\lambda$ を求めよ。<br>(2) $3.0\,\mathrm s$ の間に、波源は何回振動するか。また、その間に波の先端は何 m 進むか。<br>(3) 媒質のある点が 1 回振動する間に、波は何 m 進むか。",
  "a": r"(1) $T=0.20\,\mathrm s$、$\lambda=0.40\,\mathrm m$　(2) $15$ 回、$6.0\,\mathrm m$　(3) $0.40\,\mathrm m$",
  "s": r"(1) $T=\dfrac1f=\dfrac1{5.0}=0.20\,\mathrm s$。$v=f\lambda$ より $\lambda=\dfrac vf=\dfrac{2.0}{5.0}=0.40\,\mathrm m$。<br>(2) 振動の回数は $ft=5.0\times3.0=15$ 回。波の先端が進む距離は $vt=2.0\times3.0=6.0\,\mathrm m$。これは $15\lambda$ に等しく、1 回の振動で 1 波長分の波が送り出されることがわかる。<br>(3) 1 回振動する時間は $T$ で、その間に波は $vT=\lambda=0.40\,\mathrm m$ 進む。<br><b>ポイント</b>：波は 1 周期で 1 波長進む（$v=\dfrac\lambda T=f\lambda$）。媒質そのものは波と一緒に進まず、その場で振動するだけである。"},
 {"lv": "A", "tag": "グラフの読み取り", "q": r"図は、$x$ 軸の正の向きに速さ $2.0\,\mathrm{m/s}$ で進む正弦波の、時刻 $t=0$ における波形である。" + FIG_A2 + r"(1) 振幅・波長・周期を求めよ。<br>(2) $t=0$ において、媒質の速さが 0 の点と、$y$ 軸の正の向きに最大の速さで動いている点を、a〜d からそれぞれすべて選べ。<br>(3) $x=0$ の点の、時刻 $t=0.50\,\mathrm s$ における変位を求めよ。",
  "a": r"(1) 振幅 $0.10\,\mathrm m$、波長 $4.0\,\mathrm m$、周期 $2.0\,\mathrm s$　(2) 速さ 0：a、c　正の向きに最大：b　(3) $-0.10\,\mathrm m$",
  "s": r"(1) 図から振幅 $0.10\,\mathrm m$、波長 $4.0\,\mathrm m$。$T=\dfrac\lambda v=\dfrac{4.0}{2.0}=2.0\,\mathrm s$。<br>(2) 波形を進む向きに少しずらした「少し後の波形」を描いて比べる。山の a と谷の c は、この瞬間に速さ 0（単振動の端）。b には少し後に左側の山の部分がやって来るので上向き（正の向き）に最大の速さで動き、d には谷の部分が来るので下向きに最大の速さで動く。<br>(3) $0.50\,\mathrm s=\dfrac T4$ の間に、波形は $vt=1.0\,\mathrm m$ だけ右へ進む。$x=0$ には、$t=0$ に $x=-1.0\,\mathrm m$ にあった変位がやって来る。波形を左へのばすと、$x=-1.0\,\mathrm m$ は谷 c（$x=3.0\,\mathrm m$）から 1 波長左の点なので谷。よって $-0.10\,\mathrm m$。<br><b>ポイント</b>：$y$-$x$ グラフで媒質の動きを問われたら、「少し後の波形」を重ねて描く。変位を問われたら「波形を $vt$ だけ平行移動」する。"},
 {"lv": "A", "tag": "縦波", "q": r"$x$ 軸方向に進む縦波がある。媒質の $x$ 軸の正の向きの変位を $y$ 軸の正の向きにとって横波のように表したところ、ある時刻の波形は図のようになった（$y=-0.10\sin\dfrac{\pi x}{2}$、単位は m）。" + FIG_A3 + r"(1) $0\leqq x\leqq8\,\mathrm m$ で、媒質が最も密な位置をすべて答えよ。<br>(2) 最も疎な位置をすべて答えよ。<br>(3) この縦波が $x$ 軸の正の向きに進んでいるとき、この時刻に、変位が 0 で $x$ 軸の正の向きに最大の速さで動いている点の位置をすべて答えよ。",
  "a": r"(1) $x=0,\ 4,\ 8\,\mathrm m$　(2) $x=2,\ 6\,\mathrm m$　(3) $x=0,\ 4,\ 8\,\mathrm m$",
  "s": r"(1)(2) グラフの $y$ を、$x$ 軸方向の変位の矢印に戻して考える。$0\lt x\lt2$ では $y\lt0$ なので媒質は左へ、$2\lt x\lt4$ では $y\gt0$ なので右へずれている。すると $x=2$ の点からは両側の媒質が離れていくので疎、$x=4$ には両側から媒質が集まるので密。同様に $x=0,\ 8$ も密、$x=6$ は疎。<br>(3) 少し後の波形（右へ少しずらした波形）を描くと、$x=0,\ 4,\ 8$ の点の変位は正になる。よってこれらの点は $x$ 軸の正の向きに最大の速さで動いている。<br><b>ポイント</b>：横波表示では、$y=0$ の点のうち「右下がりの点が密、右上がりの点が疎」（正の向きの変位を上にとったとき）。正の向きに進む縦波では、密の点の媒質は進む向きに動いている。"},
 {"lv": "A", "tag": "屈折", "q": r"水面波が、深い領域Ⅰから浅い領域Ⅱへ、入射角 $60^\circ$ で境界に入射し、屈折角 $30^\circ$ で進んだ。領域Ⅰでの波の速さは $0.40\,\mathrm{m/s}$、振動数は $2.0\,\mathrm{Hz}$ である。$\sqrt3=1.73$ とする。<br>(1) 領域Ⅰに対する領域Ⅱの屈折率 $n_{12}$ を求めよ。<br>(2) 領域Ⅱでの波の速さ・振動数・波長を求めよ。",
  "a": r"(1) $\sqrt3\fallingdotseq1.7$　(2) 速さ $0.23\,\mathrm{m/s}$、振動数 $2.0\,\mathrm{Hz}$、波長 $0.12\,\mathrm m$",
  "s": r"(1) $n_{12}=\dfrac{\sin60^\circ}{\sin30^\circ}=\dfrac{\sqrt3/2}{1/2}=\sqrt3$。<br>(2) 屈折の法則 $\dfrac{\sin i}{\sin r}=\dfrac{v_1}{v_2}=\dfrac{\lambda_1}{\lambda_2}=n_{12}$ より $v_2=\dfrac{0.40}{\sqrt3}\fallingdotseq0.23\,\mathrm{m/s}$。振動数は境界の前後で変わらないので $2.0\,\mathrm{Hz}$。波長は $\lambda_2=\dfrac{v_2}{f}=\dfrac{0.40}{2.0\sqrt3}\fallingdotseq0.12\,\mathrm m$（$\lambda_1=0.20\,\mathrm m$ の $\frac1{\sqrt3}$ 倍）。<br><b>ポイント</b>：屈折で変わるのは速さと波長。振動数は波源で決まり、境界を越えても変わらない（境界の点は入射波と同じ回数だけ振動し、それが向こう側の波源になる）。"},
 {"lv": "B", "tag": "波の式", "q": r"$x$ 軸上を進む正弦波の変位 $y$ が、$y=0.020\sin\pi(4.0t-0.50x)$ と表される（$x,\ y$ の単位は m、$t$ の単位は s）。<br>(1) 振幅・振動数・波長・速さを求め、波の進む向きを答えよ。<br>(2) $x=1.0\,\mathrm m$ の点の変位 $y$ を、$t$ の式で表せ。<br>(3) $x=1.0\,\mathrm m$ の点の変位が、$t\gt0$ ではじめて $+0.020\,\mathrm m$ になる時刻を求めよ。<br>(4) 時刻 $t=0$ において、$0\leqq x\lt8.0\,\mathrm m$ の範囲で、変位が 0 で $y$ 軸の正の向きに動いている点の位置をすべて求めよ。",
  "a": r"(1) 振幅 $0.020\,\mathrm m$、振動数 $2.0\,\mathrm{Hz}$、波長 $4.0\,\mathrm m$、速さ $8.0\,\mathrm{m/s}$、$x$ 軸の正の向き　(2) $y=-0.020\cos4.0\pi t$　(3) $0.25\,\mathrm s$　(4) $x=0,\ 4.0\,\mathrm m$",
  "s": r"(1) $\pi(4.0t-0.50x)=2\pi\left(\dfrac{t}{0.50}-\dfrac{x}{4.0}\right)$ と変形し、$y=A\sin2\pi\left(\dfrac tT-\dfrac x\lambda\right)$ と比べる。$A=0.020\,\mathrm m$、$T=0.50\,\mathrm s$ より $f=2.0\,\mathrm{Hz}$、$\lambda=4.0\,\mathrm m$、$v=\dfrac\lambda T=8.0\,\mathrm{m/s}$。$t$ の項と $x$ の項の符号が逆なので、$x$ 軸の正の向きに進む。<br>(2) $y=0.020\sin(4.0\pi t-0.50\pi)=-0.020\cos4.0\pi t$。<br>(3) $-0.020\cos4.0\pi t=0.020$ より $\cos4.0\pi t=-1$。はじめて成り立つのは $4.0\pi t=\pi$、すなわち $t=0.25\,\mathrm s$。<br>(4) $t=0$ の波形は $y=-0.020\sin0.50\pi x$。変位 0 の点は $x=0,\ 2.0,\ 4.0,\ 6.0\,\mathrm m$。波形を正の向きに少しずらすと、$x=0$ と $x=4.0$ には、すぐ左側の $y\gt0$ の部分（$-2.0\lt x\lt0$、$2.0\lt x\lt4.0$）がやって来るので上向きに動く。$x=2.0,\ 6.0$ は下向き。<br><b>ポイント</b>：波の式は $2\pi\left(\dfrac tT-\dfrac x\lambda\right)$ の形に直して読む。符号が「$t$ と $x$ で逆なら正の向き、同じなら負の向き」に進む。"},
 {"lv": "B", "tag": "y-t グラフ", "q": r"原点 O の媒質の変位 $y$ が、図のように時間変化している。この振動が、$x$ 軸の正の向きに速さ $2.0\,\mathrm{m/s}$ で伝わっていく。" + FIG_B2 + r"(1) 波長を求めよ。<br>(2) 位置 $x\,[\mathrm m]$（$x\geqq0$）、時刻 $t\,[\mathrm s]$ における変位 $y\,[\mathrm m]$ を式で表せ。<br>(3) $x=3.0\,\mathrm m$ の点の、時刻 $t=1.0\,\mathrm s$ における変位を求めよ。<br>(4) 時刻 $t=1.0\,\mathrm s$ において、$0\leqq x\leqq4.0\,\mathrm m$ の範囲で、媒質が $y$ 軸の正の向きに最大の速さで動いている点の位置を求めよ。",
  "a": r"(1) $4.0\,\mathrm m$　(2) $y=0.050\sin\pi\left(t-\dfrac x{2.0}\right)$　(3) $-0.050\,\mathrm m$　(4) $x=2.0\,\mathrm m$",
  "s": r"(1) グラフから周期 $T=2.0\,\mathrm s$。$\lambda=vT=4.0\,\mathrm m$。<br>(2) 原点の振動は $y=0.050\sin\pi t$。位置 $x$ には、原点の振動が $\dfrac xv$ だけ遅れて伝わるので、$y=0.050\sin\pi\left(t-\dfrac x{2.0}\right)$。<br>(3) $y=0.050\sin\pi(1.0-1.5)=0.050\sin\left(-\dfrac\pi2\right)=-0.050\,\mathrm m$。<br>(4) 位置 $x$ の点の時刻 $t$ の状態は、原点の時刻 $t-\dfrac x{2.0}$ の状態と同じ。グラフより原点が正の向きに最大の速さで動くのは、$y=0$ を増加しながら通過する時刻 $0,\ 2.0,\ \cdots\,\mathrm s$（および $-2.0\,\mathrm s,\ \cdots$）。$1.0-\dfrac x{2.0}=0$ より $x=2.0\,\mathrm m$（$1.0-\dfrac x{2.0}=-2.0$ とすると $x=6.0\,\mathrm m$ で範囲外）。<br><b>ポイント</b>：「位置 $x$ の点は、原点の振動を $\dfrac xv$ 遅れてくり返す」。$y$-$t$ グラフから波の式を立てるときは、この遅れを $t$ から引く。"},
 {"lv": "B", "tag": "反射と定常波", "q": r"振幅 $0.030\,\mathrm m$、波長 $0.40\,\mathrm m$、振動数 $5.0\,\mathrm{Hz}$ の正弦波が $x$ 軸の正の向きに進み、$x=1.00\,\mathrm m$ の位置にある反射端で反射する。入射波と反射波が重なって定常波ができた。<br>(1) 反射端が固定端のとき、$0\leqq x\leqq1.00\,\mathrm m$ の範囲にある節の位置をすべて求めよ。<br>(2) 反射端が自由端のとき、同じ範囲にある節の位置をすべて求めよ。<br>(3) 定常波の腹の振幅を求めよ。<br>(4) 媒質全体の変位が同時に 0 になる瞬間は、何 s ごとに訪れるか。",
  "a": r"(1) $x=0,\ 0.20,\ 0.40,\ 0.60,\ 0.80,\ 1.00\,\mathrm m$　(2) $x=0.10,\ 0.30,\ 0.50,\ 0.70,\ 0.90\,\mathrm m$　(3) $0.060\,\mathrm m$　(4) $0.10\,\mathrm s$ ごと",
  "s": r"(1) 固定端は節になる。隣り合う節の間隔は $\dfrac\lambda2=0.20\,\mathrm m$ なので、$x=1.00$ から $0.20\,\mathrm m$ ごとに節がある。<br>(2) 自由端は腹になる。節は腹から $\dfrac\lambda4=0.10\,\mathrm m$ 離れた位置から $0.20\,\mathrm m$ ごとにある。<br>(3) 腹では入射波と反射波がつねに同位相で重なるので、振幅は $2\times0.030=0.060\,\mathrm m$。<br>(4) 定常波の各点は周期 $T=\dfrac1{5.0}=0.20\,\mathrm s$ で単振動し、全体が一直線（変位 0）になるのは 1 周期に 2 回。よって $\dfrac T2=0.10\,\mathrm s$ ごと。<br><b>ポイント</b>：固定端＝節、自由端＝腹。節と節（腹と腹）の間隔は $\dfrac\lambda2$、節と腹の間隔は $\dfrac\lambda4$。"},
 {"lv": "B", "tag": "干渉", "q": r"水面上の 2 点 $\mathrm{S_1}$、$\mathrm{S_2}$ は $8.0\,\mathrm{cm}$ 離れており、同位相・同振幅で波長 $2.0\,\mathrm{cm}$ の波を出している。波の減衰は無視する。<br>(1) 線分 $\mathrm{S_1S_2}$ 上（両端を除く）で、強め合う点は何個あるか。<br>(2) $\mathrm{S_1P}=12.0\,\mathrm{cm}$、$\mathrm{S_2P}=7.0\,\mathrm{cm}$ の点 P は、強め合う点か弱め合う点か。<br>(3) 2 つの波源を逆位相で振動させると、(1)・(2) の答えはそれぞれどうなるか。",
  "a": r"(1) $7$ 個　(2) 弱め合う点　(3) (1) は $8$ 個、P は強め合う点",
  "s": r"(1) $\mathrm{S_1}$ から $x\,[\mathrm{cm}]$ の点では経路差 $|x-(8.0-x)|=|2x-8.0|$。同位相の波源では、経路差 $=m\lambda$（$m$ は整数）で強め合う。$|2x-8.0|=0,\ 2.0,\ 4.0,\ 6.0$ より $x=1.0,\ 2.0,\ \cdots,\ 7.0$ の 7 個（間隔 $\dfrac\lambda2=1.0\,\mathrm{cm}$）。<br>(2) 経路差 $12.0-7.0=5.0\,\mathrm{cm}=2.5\lambda$ で、半波長の奇数倍なので弱め合う。<br>(3) 逆位相では条件が入れかわり、経路差 $=\left(m+\dfrac12\right)\lambda$ で強め合う。$|2x-8.0|=1.0,\ 3.0,\ 5.0,\ 7.0$ より $x=0.5,\ 1.5,\ \cdots,\ 7.5$ の 8 個。P は経路差 $2.5\lambda$ なので強め合う。<br><b>ポイント</b>：「経路差が $\lambda$ の整数倍なら強め合う」は同位相の波源のときだけ。逆位相なら強め合いと弱め合いの条件が入れかわる。"},
 {"lv": "B", "tag": "屈折と全反射", "q": r"水面波が、浅い領域Ⅰ（速さ $0.20\,\mathrm{m/s}$）から深い領域Ⅱ（速さ $0.40\,\mathrm{m/s}$）へ進む。波の振動数は $4.0\,\mathrm{Hz}$ である。<br>(1) 領域Ⅰ、Ⅱでの波長をそれぞれ求めよ。<br>(2) 入射角が $20^\circ$ のとき、屈折角 $r$ の $\sin r$ の値を求めよ。$\sin20^\circ=0.34$ とする。<br>(3) 臨界角を求めよ。<br>(4) 入射角が $40^\circ$ のとき、境界で波はどうなるか。",
  "a": r"(1) Ⅰ $0.050\,\mathrm m$、Ⅱ $0.10\,\mathrm m$　(2) $0.68$　(3) $30^\circ$　(4) 全反射し、領域Ⅱへは進まない",
  "s": r"(1) $\lambda=\dfrac vf$ より $\lambda_1=\dfrac{0.20}{4.0}=0.050\,\mathrm m$、$\lambda_2=\dfrac{0.40}{4.0}=0.10\,\mathrm m$。<br>(2) $\dfrac{\sin20^\circ}{\sin r}=\dfrac{v_1}{v_2}=\dfrac12$ より $\sin r=2\times0.34=0.68$。<br>(3) 屈折角が $90^\circ$ になる入射角 $\theta_c$ が臨界角。$\sin\theta_c=\dfrac{v_1}{v_2}=\dfrac12$ より $\theta_c=30^\circ$。<br>(4) $\sin40^\circ\gt\sin30^\circ$ なので、$\sin r=2\sin40^\circ\gt1$ となる $r$ はない。屈折波はできず、すべて反射する（全反射）。<br><b>ポイント</b>：全反射は、速さが遅い媒質から速い媒質へ進むときだけ起こる。臨界角は $\sin\theta_c=\dfrac{v_{\text{遅}}}{v_{\text{速}}}$。"},
 {"lv": "C", "tag": "総合・波の式", "q": r"$x$ 軸の正の向きに進む入射波 $y_1=A\sin2\pi\left(\dfrac tT-\dfrac x\lambda\right)$ が、$x=L$ にある固定端で反射し、入射波と反射波が $x\lt L$ の範囲で重なっている。<br>(1) 反射波の変位 $y_2$ を、$x,\ t$ の式で表せ。<br>(2) 合成波 $y=y_1+y_2$ を、位置だけで決まる部分と時刻だけで決まる部分の積の形に変形せよ。<br>(3) 節の位置が満たす条件を、$L-x$ を用いて表せ。<br>(4) $L=1.5\,\mathrm m$、$\lambda=0.60\,\mathrm m$、$A=0.020\,\mathrm m$ のとき、$x=0$ と $x=0.20\,\mathrm m$ での振幅をそれぞれ求めよ。",
  "a": r"(1) $y_2=-A\sin2\pi\left(\dfrac tT-\dfrac{2L-x}\lambda\right)$　(2) $y=2A\sin\dfrac{2\pi(L-x)}{\lambda}\cos2\pi\left(\dfrac tT-\dfrac L\lambda\right)$　(3) $L-x=n\cdot\dfrac\lambda2$（$n=0,1,2,\cdots$）　(4) $x=0$：$0$（節）、$x=0.20\,\mathrm m$：$0.020\sqrt3\fallingdotseq0.035\,\mathrm m$",
  "s": r"(1) 入射波が固定端につくる振動は $A\sin2\pi\left(\dfrac tT-\dfrac L\lambda\right)$。固定端では合成変位がつねに 0 なので、反射波の $x=L$ での変位はその符号を変えたもの（位相が $\pi$ ずれる）。反射波は負の向きに進み、$x=L$ から位置 $x$ まで $L-x$ 進むのに $\dfrac{L-x}{v}$ かかるので<br>$y_2=-A\sin2\pi\left(\dfrac tT-\dfrac L\lambda-\dfrac{L-x}\lambda\right)=-A\sin2\pi\left(\dfrac tT-\dfrac{2L-x}\lambda\right)$。<br>(2) $\sin\alpha-\sin\beta=2\cos\dfrac{\alpha+\beta}2\sin\dfrac{\alpha-\beta}2$ を使う。$\dfrac{\alpha+\beta}2=2\pi\left(\dfrac tT-\dfrac L\lambda\right)$、$\dfrac{\alpha-\beta}2=\dfrac{2\pi(L-x)}\lambda$ より<br>$y=2A\sin\dfrac{2\pi(L-x)}{\lambda}\cos2\pi\left(\dfrac tT-\dfrac L\lambda\right)$。<br>各点が振幅 $2A\left|\sin\dfrac{2\pi(L-x)}\lambda\right|$ で同じ周期 $T$ の単振動をし、波形は進まない。これが定常波である。<br>(3) 振幅 0 の条件 $\sin\dfrac{2\pi(L-x)}\lambda=0$ より $L-x=n\cdot\dfrac\lambda2$。固定端から半波長ごとに節がある。<br>(4) $x=0$：$\dfrac{2\pi\times1.5}{0.60}=5\pi$ で $\sin5\pi=0$ なので振幅 0（節）。$x=0.20$：$\dfrac{2\pi\times1.3}{0.60}=\dfrac{13}{3}\pi$、$\sin\dfrac{13}3\pi=\sin\dfrac\pi3=\dfrac{\sqrt3}2$ なので振幅 $2A\times\dfrac{\sqrt3}2=0.020\sqrt3\fallingdotseq0.035\,\mathrm m$。<br><b>ポイント</b>：固定端反射は「反射点で位相が $\pi$ ずれる」＝反射波の式に負号がつく。自由端なら負号はつかず、合成すると $\cos\dfrac{2\pi(L-x)}\lambda$ の形になって反射端が腹になる。"},
 {"lv": "C", "tag": "総合・干渉", "q": r"水面上の 2 点 $\mathrm{S_1}$、$\mathrm{S_2}$ が $d=7.0\,\mathrm{cm}$ 離れていて、同位相・同振幅で波長 $\lambda=2.0\,\mathrm{cm}$ の波を出している。波の減衰は無視する。" + FIG_C2 + r"(1) 線分 $\mathrm{S_1S_2}$ 上で振幅が最大になる点の位置を、$\mathrm{S_1}$ からの距離ですべて求めよ。また、隣り合う 2 点の間隔を答えよ。<br>(2) 直線 $\mathrm{S_1S_2}$ 上で、線分 $\mathrm{S_1S_2}$ の外側にある点では、波はどうなっているか。理由とともに答えよ。<br>(3) $\mathrm{S_1S_2}$ の中点 M から十分遠い点 P を、図のように MP が $\mathrm{S_1S_2}$ の垂直二等分線と角 $\theta$ をなす向きにとる。経路差は $d\sin\theta$ で近似できる。P が強め合う点となる $\sin\theta$ の値をすべて求めよ。また、水面上の腹線（強め合う点を連ねた線）は何本あるか。<br>(4) $\mathrm{S_2}$ を $\mathrm{S_1}$ と逆位相で振動させると、線分 $\mathrm{S_1S_2}$ と交わる腹線は何本になるか。また、(2) の点はどうなるか。",
  "a": r"(1) $0.5,\ 1.5,\ 2.5,\ 3.5,\ 4.5,\ 5.5,\ 6.5\,\mathrm{cm}$、間隔 $1.0\,\mathrm{cm}$　(2) 経路差がつねに $d=3.5\lambda$ なので、つねに弱め合う（振幅 0）　(3) $\sin\theta=0,\ \pm\dfrac27,\ \pm\dfrac47,\ \pm\dfrac67$、$7$ 本　(4) $6$ 本、強め合う（振幅最大）",
  "s": r"(1) $\mathrm{S_1}$ から $x$ の点の経路差は $|2x-7.0|$。$|2x-7.0|=m\lambda=0,\ 2.0,\ 4.0,\ 6.0$ より $x=3.5\pm0,\ \pm1.0,\ \pm2.0,\ \pm3.0$。7 点で、間隔は $\dfrac\lambda2=1.0\,\mathrm{cm}$。線分上では $\mathrm{S_1}$ から右向きの波と $\mathrm{S_2}$ から左向きの波が重なり、定常波ができていると見ることもできる。<br>(2) たとえば $\mathrm{S_1}$ の外側で $\mathrm{S_1}$ から $s$ の点では、$\mathrm{S_2}$ までの距離は $s+d$ で、経路差はつねに $d=7.0\,\mathrm{cm}=3.5\lambda$。半波長の奇数倍なので、外側の直線上のすべての点で弱め合い、振幅 0 になる（$\mathrm{S_2}$ の外側も同じ）。<br>(3) $d\sin\theta=m\lambda$ より $\sin\theta=\dfrac{2.0m}{7.0}=\dfrac{2m}7$。$|\sin\theta|\leqq1$ より $m=0,\ \pm1,\ \pm2,\ \pm3$。腹線は 7 本で、(1) の 7 点を 1 本ずつ通る。<br>(4) 逆位相では経路差 $=\left(m+\dfrac12\right)\lambda$ で強め合う。線分上では $|2x-7.0|=1.0,\ 3.0,\ 5.0$ より $x=1.0,\ 2.0,\ \cdots,\ 6.0$ の 6 本（$|2x-7.0|=7.0$ は波源そのもの）。外側の点は経路差 $3.5\lambda$ が強め合いの条件を満たすので、振幅最大になる。<br><b>ポイント</b>：腹線の本数は、線分上の強め合う点を数えるのが確実。遠方の向きは $d\sin\theta=m\lambda$ で、$|\sin\theta|\leqq1$ から本数の上限が決まる。"},
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
    x, t = symbols("x t", real=True)
    # A1
    f, v = 5, 2
    assert Rational(1, f) == Rational(1, 5) and Rational(v, f) == Rational(2, 5)
    assert f * 3 == 15 and v * 3 == 6
    # A2: y = 0.10 sin(2π(x - v t)/λ)
    lam, v = 4, 2
    y = Rational(1, 10) * sin(2 * pi * (x - v * t) / lam)
    assert lam / v == 2
    vel = diff(y, t)
    assert vel.subs({x: 1, t: 0}) == 0 and vel.subs({x: 3, t: 0}) == 0
    assert vel.subs({x: 2, t: 0}) > 0 and vel.subs({x: 4, t: 0}) < 0
    assert y.subs({x: 0, t: Rational(1, 2)}) == -Rational(1, 10)
    # A3: y = -0.10 sin(πx/2) を縦波表示。密 = 変位が集まる点（dy/dx < 0 で y=0）
    yl = -Rational(1, 10) * sin(pi * x / 2)
    dense = [p for p in range(0, 9) if yl.subs(x, p) == 0 and diff(yl, x).subs(x, p) < 0]
    sparse = [p for p in range(0, 9) if yl.subs(x, p) == 0 and diff(yl, x).subs(x, p) > 0]
    assert dense == [0, 4, 8] and sparse == [2, 6]
    ylt = -Rational(1, 10) * sin(pi * (x - 2 * t) / 2)   # 正の向きに進む
    assert [p for p in range(0, 9) if diff(ylt, t).subs({x: p, t: 0}) > 0 and ylt.subs({x: p, t: 0}) == 0] == [0, 4, 8]
    # A4
    n12 = sin(pi / 3) / sin(pi / 6)
    assert simplify(n12 - sqrt(3)) == 0
    _sf(0.40 / 1.73, 0.23, 2); _sf(0.40 / 1.73 / 2.0, 0.12, 2)
    # B1
    yb = Rational(2, 100) * sin(pi * (4 * t - Rational(1, 2) * x))
    assert simplify(yb - Rational(2, 100) * sin(2 * pi * (t / Rational(1, 2) - x / 4))) == 0
    assert simplify(yb.subs(x, 1) + Rational(2, 100) * cos(4 * pi * t)) == 0
    ts = solve(Eq(-cos(4 * pi * t), 1), t)
    assert min(s for s in ts if s > 0) == Rational(1, 4)
    yb0 = yb.subs(t, 0); vb0 = diff(yb, t).subs(t, 0)
    assert [p for p in range(0, 8) if yb0.subs(x, p) == 0 and vb0.subs(x, p) > 0] == [0, 4]
    # B2
    y2 = Rational(5, 100) * sin(pi * (t - x / 2))
    assert y2.subs({x: 3, t: 1}) == -Rational(5, 100)
    v2 = diff(y2, t).subs(t, 1)
    vmax = Rational(5, 100) * pi
    assert [p for p in [Rational(k, 10) for k in range(0, 41)] if v2.subs(x, p) == vmax] == [2]
    # B3
    L, lam = Rational(1), Rational(2, 5)
    fixed = [L - k * lam / 2 for k in range(6)]
    assert sorted(fixed) == [0, Rational(1, 5), Rational(2, 5), Rational(3, 5), Rational(4, 5), 1]
    free = sorted(L - lam / 4 - k * lam / 2 for k in range(5))
    assert free == [Rational(k, 10) for k in (1, 3, 5, 7, 9)]
    assert Rational(1, 5) / 2 == Rational(1, 10)
    # B4
    pts = [Rational(k, 10) for k in range(1, 80)]
    assert len([p for p in pts if (abs(2 * p - 8) / 2).is_integer]) == 7
    assert len([p for p in pts if (abs(2 * p - 8) / 2 - Rational(1, 2)).is_integer]) == 8
    assert Rational(12 - 7, 2) == Rational(5, 2)
    # B5
    assert Rational(20, 400) == Rational(1, 20)
    _sf(2 * 0.34, 0.68, 2)
    assert asin(Rational(1, 2)) == pi / 6 and 2 * sin(rad(40)).evalf() > 1
    # C1
    A, T, Lm, lam = symbols("A T L lambda", positive=True)
    y1 = A * sin(2 * pi * (t / T - x / lam))
    y2c = -A * sin(2 * pi * (t / T - (2 * Lm - x) / lam))
    assert simplify((y1 + y2c).subs(x, Lm)) == 0
    target = 2 * A * sin(2 * pi * (Lm - x) / lam) * cos(2 * pi * (t / T - Lm / lam))
    assert simplify(expand_trig(expand(y1 + y2c - target))) == 0 or \
        all(abs(N((y1 + y2c - target).subs({A: 1, T: 1.3, Lm: 1.7, lam: 0.6, x: xx, t: tt}))) < 1e-12
            for xx in (0.1, 0.37, 1.2) for tt in (0.05, 0.4, 0.9))
    amp = lambda xx: 2 * Rational(2, 100) * Abs(sin(2 * pi * (Rational(3, 2) - xx) / Rational(3, 5)))
    assert amp(0) == 0 and simplify(amp(Rational(1, 5)) - Rational(2, 100) * sqrt(3)) == 0
    _sf(0.02 * 3 ** 0.5, 0.035, 2)
    # C2
    pts = [Rational(k, 10) for k in range(1, 70)]
    anti = [p for p in pts if (abs(2 * p - 7) / 2).is_integer]
    assert anti == [Rational(k, 2) for k in (1, 3, 5, 7, 9, 11, 13)]
    assert Rational(7, 2) - Rational(1, 2) == 3   # 外側の経路差 3.5λ（半波長の奇数倍）
    ms = [m for m in range(-5, 6) if abs(Rational(2 * m, 7)) <= 1]
    assert ms == [-3, -2, -1, 0, 1, 2, 3]
    opp = [p for p in pts if (abs(2 * p - 7) / 2 - Rational(1, 2)).is_integer]
    assert opp == [1, 2, 3, 4, 5, 6]
