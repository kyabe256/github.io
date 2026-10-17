"""問題集 第14章 静電場とコンデンサー。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
from math import sin as _sin, cos as _cos, atan2 as _atan2, sqrt as _sqrt
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

def _dot(x, y, r=2.6, col="#222"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'

I = lambda s: f'<tspan font-family="Liberation Serif,serif" font-style="italic" font-size="12.5">{s}</tspan>'
SUB = lambda s: f'<tspan dy="3" font-size="8">{s}</tspan>'

# 回路記号（導線を先に描き、その上に白で消してから記号を重ねる）
def _wire(pts, w=1.2):
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="#222" stroke-width="{w}"/>'

def _C(cx, cy, vert):
    """コンデンサー。vert=True は縦の導線上（極板は水平）"""
    if vert:
        return (f'<rect x="{cx-12}" y="{cy-4}" width="24" height="8" fill="#fff"/>' +
                _ln(cx - 11, cy - 4, cx + 11, cy - 4, 2.2) + _ln(cx - 11, cy + 4, cx + 11, cy + 4, 2.2))
    return (f'<rect x="{cx-4}" y="{cy-12}" width="8" height="24" fill="#fff"/>' +
            _ln(cx - 4, cy - 11, cx - 4, cy + 11, 2.2) + _ln(cx + 4, cy - 11, cx + 4, cy + 11, 2.2))

def _E(cx, cy, vert, plus_first=True):
    """電池。長い細線が正極。vert=True は縦の導線上。plus_first=True なら上（左）が正極"""
    a, b = (-3.5, 3.5) if plus_first else (3.5, -3.5)
    if vert:
        return (f'<rect x="{cx-13}" y="{cy-4}" width="26" height="8" fill="#fff"/>' +
                _ln(cx - 12, cy + a, cx + 12, cy + a, 1.3) + _ln(cx - 6, cy + b, cx + 6, cy + b, 3.2))
    return (f'<rect x="{cx-4}" y="{cy-13}" width="8" height="26" fill="#fff"/>' +
            _ln(cx + a, cy - 12, cx + a, cy + 12, 1.3) + _ln(cx + b, cy - 6, cx + b, cy + 6, 3.2))

def _S(x1, y1, x2, y2):
    """開いたスイッチ（導線 (x1,y1)-(x2,y2) 上）"""
    a = _atan2(y2 - y1, x2 - x1) - 0.45
    L = _sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    xm, ym = (min(x1, x2) - 2, min(y1, y2) - 2)
    return (f'<rect x="{xm+3:.1f}" y="{ym-1:.1f}" width="{abs(x2-x1)+0.1:.1f}" height="{abs(y2-y1)+6:.1f}" fill="#fff"/>' if y1 == y2 else
            f'<rect x="{xm-1:.1f}" y="{ym+3:.1f}" width="{abs(x2-x1)+6:.1f}" height="{abs(y2-y1)+0.1:.1f}" fill="#fff"/>') + \
        _ln(x1, y1, x1 + L * 0.95 * _cos(a), y1 + L * 0.95 * _sin(a), 1.3) + \
        f'<circle cx="{x1}" cy="{y1}" r="2.4" fill="#fff" stroke="#222"/><circle cx="{x2}" cy="{y2}" r="2.4" fill="#fff" stroke="#222"/>'


def _fig_charges():
    """+Q が A(-a,0), B(a,0) に、P(0, √3 a)。"""
    a, ox, oy = 62, 165, 166
    py = oy - _sqrt(3) * a
    b = [_ln(ox - a - 40, oy, ox + a + 50, oy, 0.8, "", "#888"), _ln(ox, oy + 10, ox, py - 46, 0.8, "", "#888"),
         _t(ox + a + 52, oy + 4, I("x"), 11, "start"), _t(ox + 6, py - 40, I("y"), 11, "start"),
         _ln(ox - a, oy, ox, py, 0.9, "4,3", "#666"), _ln(ox + a, oy, ox, py, 0.9, "4,3", "#666"),
         _dot(ox - a, oy, 5, "#c0392b"), _dot(ox + a, oy, 5, "#c0392b"), _dot(ox, py, 2.8), _dot(ox, oy, 2.4),
         _t(ox - a, oy + 18, "A（+" + I("Q") + "）"), _t(ox + a, oy + 18, "B（+" + I("Q") + "）"),
         _t(ox - 6, oy + 16, "O", 11, "end"), _t(ox + 8, py + 4, "P", 11, "start"),
         _t(ox - a / 2, oy + 16, I("a")), _t(ox + a / 2, oy + 16, I("a")),
         _t(ox - 30, (oy + py) / 2 - 4, "2" + I("a"), 11, "end")]
    return _svg(330, 188, b)


def _fig_circuit():
    """電池 E、S1、C1・C2 の直列、C2 に S2 を介して C3 を並列。"""
    yt, yb, xb, xc, x3 = 30, 170, 40, 180, 290
    yp = 100
    b = [_wire([(xb, yp), (xb, yt), (xc, yt), (xc, yb), (xb, yb), (xb, yp)]),
         _wire([(xc, yp), (x3, yp), (x3, yb), (xc, yb)]),
         _E(xb, yp, True, True), _S(84, yt, 114, yt), _C(xc, 65, True), _C(xc, 135, True),
         _S(220, yp, 250, yp), _C(x3, 135, True), _dot(xc, yp), _dot(xc, yb),
         _t(xb - 16, yp + 4, I("E"), 12, "end"), _t(xb + 16, yp - 6, "+", 11, "start"),
         _t(99, yt - 10, "S" + SUB("1")), _t(235, yp - 12, "S" + SUB("2")),
         _t(xc + 16, 69, "C" + SUB("1"), 11, "start"), _t(xc + 16, 139, "C" + SUB("2"), 11, "start"),
         _t(x3 + 16, 139, "C" + SUB("3"), 11, "start"), _t(xc - 8, yp - 6, "P", 11, "end")]
    return _svg(330, 184, b)


FIG_B1 = _fig_charges()
FIG_C2 = _fig_circuit()

CH = {14: {
"goal": r"クーロンの法則・電場・電位を「向きをもつ量」と「向きをもたない量」に分けて扱う。コンデンサーは「電気量の保存」と「電位差の和」で式を立て、エネルギーの出入りを電池の仕事まで含めて追えるようにする。",
"items": [
 {"lv": "A", "tag": "クーロンの法則", "q": r"クーロンの法則の比例定数を $k=9.0\times10^9\,\mathrm{N\cdot m^2/C^2}$ とする。距離 $0.30\,\mathrm m$ 離れた点 A、B に、それぞれ $+2.0\times10^{-6}\,\mathrm C$、$-3.0\times10^{-6}\,\mathrm C$ の点電荷を置く。<br>(1) 2 つの電荷の間にはたらく静電気力の大きさを求め、引力か斥力かを答えよ。<br>(2) 2 つの電荷の電気量をどちらも 2 倍にし、距離も 2 倍にすると、静電気力の大きさはいくらになるか。<br>(3) (1) の状態で、AB の中点 M に $+1.0\times10^{-6}\,\mathrm C$ の点電荷を置く。この電荷が受ける静電気力の向きと大きさを求めよ。",
  "a": r"(1) $0.60\,\mathrm N$、引力　(2) $0.60\,\mathrm N$　(3) B の向きに $2.0\,\mathrm N$",
  "s": r"(1) $F=k\dfrac{q_1q_2}{r^2}=9.0\times10^9\times\dfrac{2.0\times10^{-6}\times3.0\times10^{-6}}{0.30^2}=0.60\,\mathrm N$。異符号なので引力。<br>(2) 分子が 4 倍、分母も 4 倍なので変わらず $0.60\,\mathrm N$。<br>(3) M は A、B から $0.15\,\mathrm m$。A から受ける力は斥力で B の向きに $9.0\times10^9\times\dfrac{2.0\times10^{-6}\times1.0\times10^{-6}}{0.15^2}=0.80\,\mathrm N$。B から受ける力は引力で B の向きに $1.2\,\mathrm N$。合わせて B の向きに $2.0\,\mathrm N$。<br><b>ポイント</b>：力はベクトル。それぞれの電荷から受ける力の<b>向き</b>を先に図に描いてから、大きさを足し引きする。"},
 {"lv": "A", "tag": "電場と電位", "q": r"$k=9.0\times10^9\,\mathrm{N\cdot m^2/C^2}$ とし、無限遠を電位の基準とする。点 O に $+4.0\times10^{-9}\,\mathrm C$ の点電荷を固定する。<br>(1) O から $0.20\,\mathrm m$ の点 A の電場の強さと電位を求めよ。<br>(2) O から $0.10\,\mathrm m$ の点 B の電位を求めよ。<br>(3) $+1.0\times10^{-9}\,\mathrm C$ の小さな電荷を、A から B までゆっくり運ぶのに必要な外力の仕事を求めよ。",
  "a": r"(1) $9.0\times10^2\,\mathrm{N/C}$、$1.8\times10^2\,\mathrm V$　(2) $3.6\times10^2\,\mathrm V$　(3) $1.8\times10^{-7}\,\mathrm J$",
  "s": r"(1) $E=k\dfrac Q{r^2}=9.0\times10^9\times\dfrac{4.0\times10^{-9}}{0.20^2}=9.0\times10^2\,\mathrm{N/C}$、$V=k\dfrac Qr=\dfrac{36}{0.20}=1.8\times10^2\,\mathrm V$。<br>(2) $V_\mathrm B=\dfrac{36}{0.10}=3.6\times10^2\,\mathrm V$。<br>(3) ゆっくり運ぶので、外力の仕事は位置エネルギーの増加に等しい。$W=q(V_\mathrm B-V_\mathrm A)=1.0\times10^{-9}\times180=1.8\times10^{-7}\,\mathrm J$。<br><b>ポイント</b>：電場は $\dfrac1{r^2}$、電位は $\dfrac1r$ に比例。電荷を運ぶ仕事は「電荷 × 電位差」で、経路によらない。"},
 {"lv": "A", "tag": "一様な電場", "q": r"間隔 $2.0\,\mathrm{cm}$ の平行な 2 枚の金属板の間に、$100\,\mathrm V$ の電圧をかけた。電気素量を $1.6\times10^{-19}\,\mathrm C$、電子の質量を $9.1\times10^{-31}\,\mathrm{kg}$ とする。<br>(1) 極板間の電場の強さを求めよ。<br>(2) 極板間で電子が受ける力の大きさを求めよ。<br>(3) 負極板の近くで静止していた電子が正極板に達するときの運動エネルギーと速さを求めよ。",
  "a": r"(1) $5.0\times10^3\,\mathrm{V/m}$　(2) $8.0\times10^{-16}\,\mathrm N$　(3) $1.6\times10^{-17}\,\mathrm J$、$5.9\times10^6\,\mathrm{m/s}$",
  "s": r"(1) $E=\dfrac Vd=\dfrac{100}{0.020}=5.0\times10^3\,\mathrm{V/m}$。<br>(2) $F=eE=1.6\times10^{-19}\times5.0\times10^3=8.0\times10^{-16}\,\mathrm N$。<br>(3) 電場がする仕事 $eV=1.6\times10^{-19}\times100=1.6\times10^{-17}\,\mathrm J$ が運動エネルギーになる（$100\,\mathrm{eV}$）。$v=\sqrt{\dfrac{2eV}m}=\sqrt{\dfrac{2\times1.6\times10^{-17}}{9.1\times10^{-31}}}\fallingdotseq5.9\times10^6\,\mathrm{m/s}$。<br><b>ポイント</b>：一様な電場では $E=\dfrac Vd$（単位 $\mathrm{V/m}=\mathrm{N/C}$）。加速された電荷の運動エネルギーは、途中の経路によらず $qV$。"},
 {"lv": "A", "tag": "コンデンサーの接続", "q": r"(1) 電気容量 $2.0\,\mu\mathrm F$ と $3.0\,\mu\mathrm F$ のコンデンサーを、並列につないだときと直列につないだときの合成容量を求めよ。<br>(2) この 2 つを直列にして $10\,\mathrm V$ の電池につないだ。それぞれのコンデンサーの電気量と電圧を求めよ。<br>(3) 電気容量 $C_0$ の平行板コンデンサーの極板間隔を半分にし、極板間を比誘電率 $2.0$ の誘電体で満たすと、電気容量はいくらになるか。",
  "a": r"(1) 並列 $5.0\,\mu\mathrm F$、直列 $1.2\,\mu\mathrm F$　(2) どちらも $12\,\mu\mathrm C$。$2.0\,\mu\mathrm F$ が $6.0\,\mathrm V$、$3.0\,\mu\mathrm F$ が $4.0\,\mathrm V$　(3) $4C_0$",
  "s": r"(1) 並列 $C=C_1+C_2=5.0\,\mu\mathrm F$。直列 $\dfrac1C=\dfrac1{2.0}+\dfrac1{3.0}$ より $C=1.2\,\mu\mathrm F$。<br>(2) 直列では電気量が共通で $Q=1.2\times10=12\,\mu\mathrm C$。$V_1=\dfrac{12}{2.0}=6.0\,\mathrm V$、$V_2=\dfrac{12}{3.0}=4.0\,\mathrm V$（和が $10\,\mathrm V$）。<br>(3) $C=\dfrac{\varepsilon_r\varepsilon_0S}{d}$ で $\varepsilon_r$ が 2 倍、$d$ が $\dfrac12$ 倍なので $4C_0$。<br><b>ポイント</b>：直列は「電気量が等しい」、並列は「電圧が等しい」。直列では容量の小さいほうに大きな電圧がかかる。"},
 {"lv": "B", "tag": "電場の重ね合わせ", "q": r"図のように、$xy$ 平面上の点 $\mathrm A(-a,\ 0)$、$\mathrm B(a,\ 0)$ に、それぞれ電気量 $+Q\ (Q\gt0)$ の点電荷を固定する。点 $\mathrm P(0,\ \sqrt3a)$、原点を O とし、クーロンの法則の比例定数を $k$、無限遠を電位の基準とする。重力は考えない。" + FIG_B1 + r"(1) P における電場の向きと強さを求めよ。<br>(2) P と O の電位をそれぞれ求めよ。<br>(3) 正の点電荷 $q$ を、P から O までゆっくり運ぶのに必要な外力の仕事を求めよ。<br>(4) 質量 $m$、電気量 $q\ (q\gt0)$ の小球を P に置いて静かに放すと、小球は $y$ 軸の正の向きに動き出す。十分遠くへ行ったときの小球の速さを求めよ。",
  "a": r"(1) $y$ 軸の正の向き、$\dfrac{\sqrt3kQ}{4a^2}$　(2) $V_\mathrm P=\dfrac{kQ}a$、$V_\mathrm O=\dfrac{2kQ}a$　(3) $\dfrac{kQq}a$　(4) $\sqrt{\dfrac{2kQq}{ma}}$",
  "s": r"(1) $\mathrm{AP}=\mathrm{BP}=2a$。各電荷がつくる電場の強さは $\dfrac{kQ}{4a^2}$ で、向きは A→P、B→P。$x$ 成分は打ち消しあい、$y$ 成分は $\dfrac{kQ}{4a^2}\times\dfrac{\sqrt3a}{2a}$ ずつ。合計 $\dfrac{\sqrt3kQ}{4a^2}$、$y$ 軸の正の向き。<br>(2) 電位はスカラーなので和をとる。$V_\mathrm P=2\times\dfrac{kQ}{2a}=\dfrac{kQ}a$、$V_\mathrm O=2\times\dfrac{kQ}a=\dfrac{2kQ}a$。<br>(3) $W=q(V_\mathrm O-V_\mathrm P)=\dfrac{kQq}a$。<br>(4) 力学的エネルギー保存：$qV_\mathrm P=\dfrac12mv^2+0$ より $v=\sqrt{\dfrac{2kQq}{ma}}$。<br><b>ポイント</b>：電場はベクトルの和（成分で）、電位はただの和。速さを問われたら、力を積み重ねるより「静電気力の位置エネルギー $qV$」を使う。"},
 {"lv": "B", "tag": "極板間隔の変化", "q": r"極板間隔 $d$、電気容量 $C_0$ の平行板コンデンサー（極板間は真空）を、起電力 $V$ の電池で十分に充電した。<br>(1) 電池を切り離してから、極板間隔をゆっくり $2d$ に広げた。極板間の電圧・電場の強さ・静電エネルギーを求めよ。また、外力のした仕事を求めよ。<br>(2) (1) とは別に、電池をつないだまま極板間隔をゆっくり $d$ から $2d$ に広げた。極板の電気量の変化、電池のした仕事、静電エネルギーの変化、外力のした仕事を求めよ。",
  "a": r"(1) 電圧 $2V$、電場 $\dfrac Vd$（変わらない）、エネルギー $C_0V^2$、外力の仕事 $\dfrac12C_0V^2$　(2) 電気量 $-\dfrac12C_0V$、電池の仕事 $-\dfrac12C_0V^2$、エネルギーの変化 $-\dfrac14C_0V^2$、外力の仕事 $\dfrac14C_0V^2$",
  "s": r"(1) 電気量 $Q=C_0V$ は一定。容量は $\dfrac{C_0}2$ になるので電圧は $\dfrac{Q}{C_0/2}=2V$。電場は $\dfrac{2V}{2d}=\dfrac Vd$ で変わらない（電場は極板の電荷密度だけで決まる）。エネルギーは $\dfrac{Q^2}{2(C_0/2)}=C_0V^2$。電池がないので、外力の仕事はエネルギーの増加 $C_0V^2-\dfrac12C_0V^2=\dfrac12C_0V^2$。<br>(2) 電圧 $V$ が一定。電気量は $C_0V\to\dfrac12C_0V$ と $\dfrac12C_0V$ 減る（電池に戻る）。電池の仕事は $V\Delta Q=-\dfrac12C_0V^2$。エネルギーは $\dfrac12C_0V^2\to\dfrac14C_0V^2$ で $-\dfrac14C_0V^2$。<br>エネルギーの収支「外力の仕事 $+$ 電池の仕事 $=$ 静電エネルギーの変化」より、外力の仕事 $=-\dfrac14C_0V^2-\left(-\dfrac12C_0V^2\right)=\dfrac14C_0V^2$（極板は引き合うので、広げるには正の仕事が必要）。<br><b>ポイント</b>：電池を切り離せば $Q$ 一定、つないだままなら $V$ 一定。電池がつながっているときは、電池の仕事 $V\Delta Q$ をエネルギー収支に必ず入れる。"},
 {"lv": "B", "tag": "誘電体・導体の挿入", "q": r"面積 $S$、間隔 $d$ の平行板コンデンサー（極板間は真空、電気容量 $C_0$）の極板間に、次のものを極板と平行に入れる。それぞれの場合の電気容量を $C_0$ で表せ。<br>(1) 面積 $S$、厚さ $\dfrac d2$、比誘電率 $3$ の誘電体の板<br>(2) 面積 $S$、厚さ $\dfrac d2$ の金属板（極板には触れない）<br>(3) 面積 $\dfrac S2$、厚さ $d$、比誘電率 $3$ の誘電体の板（極板間の半分を満たす）<br>(4) (1) の状態で極板間に電圧 $V$ をかけたとき、真空の部分と誘電体の部分にかかる電圧をそれぞれ求めよ。",
  "a": r"(1) $\dfrac32C_0$　(2) $2C_0$　(3) $2C_0$　(4) 真空部分 $\dfrac34V$、誘電体部分 $\dfrac14V$",
  "s": r"(1) 真空の層（厚さ $\dfrac d2$）と誘電体の層の直列とみなす。容量はそれぞれ $2C_0$、$3\times2C_0=6C_0$。$\dfrac1C=\dfrac1{2C_0}+\dfrac1{6C_0}$ より $C=\dfrac32C_0$。<br>(2) 金属板の中は電場 0 で、真空の部分の厚さが合計 $\dfrac d2$ になったのと同じ。$C=\dfrac{\varepsilon_0S}{d/2}=2C_0$。<br>(3) 面積 $\dfrac S2$ の真空部分（$\dfrac12C_0$）と誘電体部分（$\dfrac32C_0$）の並列。$C=2C_0$。<br>(4) 直列なので電気量が共通。$Q=\dfrac32C_0V$。真空部分 $\dfrac{Q}{2C_0}=\dfrac34V$、誘電体部分 $\dfrac Q{6C_0}=\dfrac14V$。<br><b>ポイント</b>：極板と平行な層は「直列」、極板間を横に分けると「並列」。金属板は「その厚さの分だけ間隔が縮む」。"},
 {"lv": "B", "tag": "電荷の再配分", "q": r"(1) 電気容量 $2.0\,\mu\mathrm F$ のコンデンサー $\mathrm{C_1}$ を $12\,\mathrm V$ で充電して電池から切り離し、充電されていない電気容量 $4.0\,\mu\mathrm F$ のコンデンサー $\mathrm{C_2}$ と、極板どうしを導線でつないだ。共通の電圧を求めよ。また、この間に失われた静電エネルギーを求めよ。<br>(2) (1) とは別に、$\mathrm{C_1}$ を $12\,\mathrm V$、$\mathrm{C_2}$ を $3.0\,\mathrm V$ で充電し、それぞれ電池から切り離してから、正の極板と負の極板をつなぐ向き（異符号の極板どうし）でつないだ。共通の電圧と、$\mathrm{C_1}$ の電気量を求めよ。",
  "a": r"(1) $4.0\,\mathrm V$、$9.6\times10^{-5}\,\mathrm J$　(2) $2.0\,\mathrm V$、$4.0\times10^{-6}\,\mathrm C$",
  "s": r"(1) つないだ極板の電気量の和は保存する：$Q=2.0\times12=24\,\mu\mathrm C$。並列で $6.0\,\mu\mathrm F$ になるので $V=\dfrac{24}{6.0}=4.0\,\mathrm V$。エネルギーは $\dfrac12\times2.0\times10^{-6}\times12^2=144\,\mu\mathrm J$ から $\dfrac12\times6.0\times10^{-6}\times4.0^2=48\,\mu\mathrm J$ になり、$96\,\mu\mathrm J=9.6\times10^{-5}\,\mathrm J$ 失われる。導線の抵抗によるジュール熱や電磁波として出ていく。<br>(2) $\mathrm{C_1}$ は $24\,\mu\mathrm C$、$\mathrm{C_2}$ は $12\,\mu\mathrm C$。異符号の極板どうしをつなぐと、つないだ一方の組の電気量の和は $+24-12=+12\,\mu\mathrm C$。$V=\dfrac{12}{6.0}=2.0\,\mathrm V$、$\mathrm{C_1}$ の電気量は $2.0\times2.0=4.0\,\mu\mathrm C$。<br><b>ポイント</b>：電池から切り離されたコンデンサーをつなぐ問題は「孤立した極板の組の電気量の和は保存」。符号に注意して足し合わせる。"},
 {"lv": "B", "tag": "電気力線とガウスの法則", "q": r"電気力線を、電場の強さが $E\,[\mathrm{N/C}]$ の所で電場に垂直な面 $1\,\mathrm{m^2}$ あたり $E$ 本の割合で引くことにする。クーロンの法則の比例定数を $k$ とする。<br>(1) 点電荷 $Q\ (\gt0)$ から出る電気力線の総数を求めよ。<br>(2) 面密度 $\sigma\ (\gt0)$ で一様に帯電した十分に広い平面がある。平面の外の電場の強さを求めよ。<br>(3) 面密度 $+\sigma$ と $-\sigma$ に帯電した十分に広い 2 枚の平面を、間隔 $d$ で平行に置く。2 枚の間と外側の電場の強さ、2 枚の間の電位差を求めよ。<br>(4) 半径 $R$ の中空の導体球に電荷 $Q\ (\gt0)$ を与えた。中心から距離 $r$ の点の電場の強さを、$r\lt R$ と $r\gt R$ に分けて求めよ。また、球の中心の電位を求めよ（無限遠を基準）。",
  "a": r"(1) $4\pi kQ$ 本　(2) $2\pi k\sigma$　(3) 間 $4\pi k\sigma$、外 $0$、電位差 $4\pi k\sigma d$　(4) $r\lt R$：$0$、$r\gt R$：$\dfrac{kQ}{r^2}$、中心の電位 $\dfrac{kQ}R$",
  "s": r"(1) 半径 $r$ の球面で $E=\dfrac{kQ}{r^2}$。本数は $E\times4\pi r^2=4\pi kQ$（$r$ によらない）。<br>(2) 面積 $A$ の部分から $4\pi k\sigma A$ 本の電気力線が出て、平面の両側に半分ずつ垂直に出る。片側で $1\,\mathrm{m^2}$ あたり $2\pi k\sigma$ 本なので $E=2\pi k\sigma$。<br>(3) (2) の電場を重ね合わせる。間では同じ向きで $4\pi k\sigma$、外側では逆向きで打ち消しあって 0。電位差は $4\pi k\sigma d$。$k=\dfrac1{4\pi\varepsilon_0}$ を使うと $E=\dfrac\sigma{\varepsilon_0}$、$V=\dfrac{\sigma d}{\varepsilon_0}$ で、$Q=\sigma S$ とすると $C=\dfrac{\varepsilon_0S}d$ が導ける。<br>(4) 電荷は導体の外側の表面に分布し、導体内部（中空部分も含む）の電場は 0。外では電気力線が点電荷と同じように広がるので $\dfrac{kQ}{r^2}$。内部は電場 0 なので電位は一定で、表面の電位 $\dfrac{kQ}R$ に等しい。<br><b>ポイント</b>：電気力線の総数 $4\pi kQ=\dfrac Q{\varepsilon_0}$ と「本数 ÷ 面積 $=E$」を組み合わせると、対称性のよい電場はすぐ求まる（ガウスの法則）。"},
 {"lv": "C", "tag": "総合・誘電体にはたらく力", "q": r"縦 $l$、横 $w$ の長方形の極板 2 枚を間隔 $d$ で向かい合わせたコンデンサーがある。極板と同じ大きさで厚さ $d$、比誘電率 $\varepsilon_r\ (\gt1)$ の誘電体の板を、縦の向きに $x\ (0\leqq x\leqq l)$ だけ極板間に差しこむ。真空の誘電率を $\varepsilon_0$ とし、極板の端の影響と摩擦は無視する。<br>(1) 電気容量 $C(x)$ を求めよ。<br>(2) コンデンサーを起電力 $V$ の電池につないだまま、誘電体を $x$ から $x+\Delta x$ までゆっくり押しこむ。極板の電気量の増加 $\Delta Q$、電池のした仕事 $W_\mathrm b$、静電エネルギーの増加 $\Delta U$ を求めよ。<br>(3) (2) で外力のした仕事 $W$ を求めよ。また、誘電体が極板間から受ける力の向きと大きさを答えよ。<br>(4) 次に、$x=0$ の状態で電池につないで充電し、電池を切り離した。その後、誘電体を $x$ まで差しこんだ状態で誘電体が受ける力の大きさ $F(x)$ を、$V$ などを用いて表せ。",
  "a": r"(1) $C(x)=\dfrac{\varepsilon_0w\{l+(\varepsilon_r-1)x\}}d$　(2) $\Delta Q=\dfrac{\varepsilon_0w(\varepsilon_r-1)V}d\Delta x$、$W_\mathrm b=\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2}d\Delta x$、$\Delta U=\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2}{2d}\Delta x$　(3) $W=-\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2}{2d}\Delta x$。極板間に引きこまれる向きに大きさ $\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2}{2d}$　(4) $F(x)=\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2l^2}{2d\{l+(\varepsilon_r-1)x\}^2}$",
  "s": r"(1) 誘電体のある部分（幅 $w$、長さ $x$）と真空の部分（長さ $l-x$）の並列。$C=\dfrac{\varepsilon_r\varepsilon_0wx}d+\dfrac{\varepsilon_0w(l-x)}d=\dfrac{\varepsilon_0w\{l+(\varepsilon_r-1)x\}}d$。<br>(2) $\Delta C=\dfrac{\varepsilon_0w(\varepsilon_r-1)}d\Delta x$。$V$ 一定なので $\Delta Q=V\Delta C$、$W_\mathrm b=V\Delta Q=V^2\Delta C$、$\Delta U=\dfrac12V^2\Delta C$。<br>(3) $W+W_\mathrm b=\Delta U$ より $W=\Delta U-W_\mathrm b=-\dfrac12V^2\Delta C\lt0$。外力の仕事が負なので、外力は押しこむ向きと逆向き、すなわち誘電体を引き止める向きにはたらいている。ゆっくり動かすとき外力と静電気力はつりあうので、誘電体は極板間に引きこまれる向きに $F=\dfrac{|W|}{\Delta x}=\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2}{2d}$ の力を受ける（$x$ によらない）。<br>(4) 電気量 $Q_0=C(0)V=\dfrac{\varepsilon_0wlV}d$ が一定。$U=\dfrac{Q_0^2}{2C}$ で、$\Delta U=-\dfrac{Q_0^2}{2C^2}\Delta C$。電池がないので外力の仕事 $=\Delta U\lt0$。やはり引きこまれる向きの力で、$F=\dfrac{Q_0^2}{2C^2}\cdot\dfrac{\Delta C}{\Delta x}=\dfrac{Q_0^2\varepsilon_0w(\varepsilon_r-1)}{2dC^2}=\dfrac{\varepsilon_0w(\varepsilon_r-1)V^2l^2}{2d\{l+(\varepsilon_r-1)x\}^2}$。<br><b>ポイント</b>：力を直接求めにくいときは「ゆっくり動かしたときの外力の仕事 $=-$（受ける力）$\times\Delta x$」を使う。電池がつながっていれば、電池の仕事 $V\Delta Q$ を忘れない。"},
 {"lv": "C", "tag": "総合・コンデンサー回路", "q": r"図の回路で、電池の起電力は $E=12\,\mathrm V$、コンデンサーの電気容量は $\mathrm{C_1}=3.0\,\mu\mathrm F$、$\mathrm{C_2}=6.0\,\mu\mathrm F$、$\mathrm{C_3}=2.0\,\mu\mathrm F$ である。はじめ、すべてのコンデンサーは電荷をもたず、スイッチ $\mathrm{S_1}$、$\mathrm{S_2}$ は開いている。電池の内部抵抗は無視する。" + FIG_C2 + r"(1) $\mathrm{S_1}$ を閉じて十分時間がたった。$\mathrm{C_1}$ の電気量と、$\mathrm{C_1}$、$\mathrm{C_2}$ の電圧を求めよ。<br>(2) 次に $\mathrm{S_1}$ を開き、$\mathrm{S_2}$ を閉じて十分時間がたった。$\mathrm{C_2}$ の電圧と $\mathrm{C_3}$ の電気量を求めよ。また、この操作で失われた静電エネルギーを求めよ。<br>(3) 次に $\mathrm{S_2}$ を開き、$\mathrm{S_1}$ を閉じて十分時間がたった。$\mathrm{C_1}$、$\mathrm{C_2}$ の電気量を求めよ。<br>(4) (3) の操作の間に電池がした仕事と、回路で発生したジュール熱を求めよ。",
  "a": r"(1) $24\,\mu\mathrm C$、$\mathrm{C_1}$：$8.0\,\mathrm V$、$\mathrm{C_2}$：$4.0\,\mathrm V$　(2) $3.0\,\mathrm V$、$6.0\,\mu\mathrm C$、$12\,\mu\mathrm J$　(3) $\mathrm{C_1}$：$26\,\mu\mathrm C$、$\mathrm{C_2}$：$20\,\mu\mathrm C$　(4) 電池の仕事 $24\,\mu\mathrm J$、ジュール熱 $1.0\,\mu\mathrm J$",
  "s": r"$\mathrm{C_1}$ の下の極板・$\mathrm{C_2}$ の上の極板・点 P をまとめて「P 側の極板」と呼ぶ。<br>(1) 直列の合成容量 $\dfrac{3.0\times6.0}{3.0+6.0}=2.0\,\mu\mathrm F$。$Q=2.0\times12=24\,\mu\mathrm C$。$V_1=\dfrac{24}{3.0}=8.0\,\mathrm V$、$V_2=\dfrac{24}{6.0}=4.0\,\mathrm V$。P 側の極板の電気量は $-24+24=0$。<br>(2) $\mathrm{S_1}$ が開いているので $\mathrm{C_1}$ の電気量は変わらない。$\mathrm{C_2}$ の $24\,\mu\mathrm C$ が $\mathrm{C_2}$ と $\mathrm{C_3}$（並列 $8.0\,\mu\mathrm F$）に分かれ、$V=\dfrac{24}{8.0}=3.0\,\mathrm V$、$Q_2=18\,\mu\mathrm C$、$Q_3=6.0\,\mu\mathrm C$。エネルギーは $\dfrac{24^2}{2\times6.0}=48\,\mu\mathrm J$ から $\dfrac{18^2}{2\times6.0}+\dfrac{6.0^2}{2\times2.0}=27+9=36\,\mu\mathrm J$ になり、$12\,\mu\mathrm J$ 失われる。<br>(3) $\mathrm{S_2}$ を開くと $\mathrm{C_3}$ は $6.0\,\mu\mathrm C$ を持ったまま切り離される。P 側の極板の電気量は $-24+18=-6.0\,\mu\mathrm C$ で、これ以降保存する。$\mathrm{C_1}$、$\mathrm{C_2}$ の（上側の極板の）電気量を $Q_1$、$Q_2$ とすると<br>電気量保存：$-Q_1+Q_2=-6.0$、電圧：$\dfrac{Q_1}{3.0}+\dfrac{Q_2}{6.0}=12$。<br>解いて $Q_1=26\,\mu\mathrm C$、$Q_2=20\,\mu\mathrm C$。<br>(4) 電池を通った電気量は $\mathrm{C_1}$ の上の極板の増加分 $26-24=2.0\,\mu\mathrm C$。電池の仕事 $12\times2.0=24\,\mu\mathrm J$。静電エネルギーは $\dfrac{24^2}{6.0}+27=123\,\mu\mathrm J$ から $\dfrac{26^2}{6.0}+\dfrac{20^2}{12}=146\,\mu\mathrm J$ に $23\,\mu\mathrm J$ 増えた。ジュール熱 $=24-23=1.0\,\mu\mathrm J$。<br><b>ポイント</b>：スイッチの切り替えでは、(i) 孤立した極板の組を見つけてその電気量の和を保存させ、(ii) 閉回路の電位差の和の式と連立する。エネルギーは「電池の仕事 $=$ 静電エネルギーの増加 $+$ ジュール熱」。"},
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
    k = 9 * 10 ** 9
    # A1
    q1, q2, r = R(2, 10 ** 6), R(3, 10 ** 6), R(3, 10)
    assert k * q1 * q2 / r ** 2 == R(6, 10)
    assert k * (2 * q1) * (2 * q2) / (2 * r) ** 2 == R(6, 10)
    q3, rm = R(1, 10 ** 6), R(15, 100)
    assert k * q1 * q3 / rm ** 2 + k * q2 * q3 / rm ** 2 == 2
    # A2
    Q = R(4, 10 ** 9)
    assert k * Q / R(2, 10) ** 2 == 900 and k * Q / R(2, 10) == 180 and k * Q / R(1, 10) == 360
    assert R(1, 10 ** 9) * (360 - 180) == R(18, 10 ** 8)
    # A3
    e, m = R(16, 10 ** 20), R(91, 10 ** 32)
    E = 100 / R(2, 100)
    assert E == 5000 and e * E == R(8, 10 ** 16) and e * 100 == R(16, 10 ** 18)
    _sf(sqrt(2 * e * 100 / m), 5.9e6, 2)
    # A4
    assert 2 + 3 == 5 and R(2 * 3, 2 + 3) == R(6, 5)
    Qs = R(6, 5) * 10
    assert Qs == 12 and Qs / 2 == 6 and Qs / 3 == 4
    assert R(2) / R(1, 2) == 4
    # B1
    kk, QQ, a, q, mm = symbols("k Q a q m", positive=True)
    P = Matrix([0, sqrt(3) * a])
    Ef = zeros(2, 1)
    for src in (Matrix([-a, 0]), Matrix([a, 0])):
        dvec = P - src
        Ef += kk * QQ * dvec / (dvec.norm() ** 3)
    assert simplify(Ef[0]) == 0 and simplify(Ef[1] - sqrt(3) * kk * QQ / (4 * a ** 2)) == 0
    VP = sum(kk * QQ / (P - s).norm() for s in (Matrix([-a, 0]), Matrix([a, 0])))
    VO = 2 * kk * QQ / a
    assert simplify(VP - kk * QQ / a) == 0
    assert simplify(q * (VO - VP) - kk * QQ * q / a) == 0
    v = sqrt(2 * kk * QQ * q / (mm * a))
    assert simplify(mm * v ** 2 / 2 - q * VP) == 0
    # B2
    C0, V = symbols("C_0 V", positive=True)
    Q0 = C0 * V
    U0 = C0 * V ** 2 / 2
    U1 = Q0 ** 2 / (2 * (C0 / 2))
    assert simplify(Q0 / (C0 / 2) - 2 * V) == 0 and simplify(U1 - C0 * V ** 2) == 0 and simplify(U1 - U0 - C0 * V ** 2 / 2) == 0
    dQ = C0 * V / 2 - C0 * V
    Wb = V * dQ
    dU = (C0 / 2) * V ** 2 / 2 - U0
    assert simplify(dQ + C0 * V / 2) == 0 and simplify(Wb + C0 * V ** 2 / 2) == 0 and simplify(dU + C0 * V ** 2 / 4) == 0
    assert simplify(dU - Wb - C0 * V ** 2 / 4) == 0
    # B3
    c_vac, c_die = 2 * C0, 3 * 2 * C0
    Cs = 1 / (1 / c_vac + 1 / c_die)
    assert simplify(Cs - R(3, 2) * C0) == 0
    assert simplify(C0 / 2 + 3 * C0 / 2 - 2 * C0) == 0
    Qc = Cs * V
    assert simplify(Qc / c_vac - R(3, 4) * V) == 0 and simplify(Qc / c_die - V / 4) == 0
    # B4
    Q1 = 2 * 12
    Vc = R(Q1, 2 + 4)
    assert Vc == 4 and R(1, 2) * 2 * 12 ** 2 - R(1, 2) * 6 * Vc ** 2 == 96
    Vd = R(2 * 12 - 4 * 3, 6)
    assert Vd == 2 and 2 * Vd == 4
    # B5
    rr, sig, dd, Rs = symbols("r sigma d R", positive=True)
    assert simplify(kk * QQ / rr ** 2 * 4 * pi * rr ** 2 - 4 * pi * kk * QQ) == 0
    Ep = 4 * pi * kk * sig / 2
    assert simplify(2 * Ep - 4 * pi * kk * sig) == 0
    eps0 = 1 / (4 * pi * kk)
    S = symbols("S", positive=True)
    Cpp = sig * S / (4 * pi * kk * sig * dd)
    assert simplify(Cpp - eps0 * S / dd) == 0
    # C1
    e0, w, l, d, er, x, dx = symbols("epsilon_0 w l d epsilon_r x Delta_x", positive=True)
    Cx = er * e0 * w * x / d + e0 * w * (l - x) / d
    assert simplify(Cx - e0 * w * (l + (er - 1) * x) / d) == 0
    dC = simplify(Cx.subs(x, x + dx) - Cx)
    assert simplify(dC - e0 * w * (er - 1) * dx / d) == 0
    dQ = V * dC; Wb = V * dQ; dU = V ** 2 * dC / 2
    W = dU - Wb
    assert simplify(W + e0 * w * (er - 1) * V ** 2 * dx / (2 * d)) == 0
    Q0 = Cx.subs(x, 0) * V
    U = Q0 ** 2 / (2 * Cx)
    Fx = -diff(U, x)        # 引きこまれる向きの力（U が減る向き）
    assert simplify(Fx - e0 * w * (er - 1) * V ** 2 * l ** 2 / (2 * d * (l + (er - 1) * x) ** 2)) == 0
    # C2
    c1, c2, c3, E = 3, 6, 2, 12
    Q = R(c1 * c2, c1 + c2) * E
    assert Q == 24 and R(Q, c1) == 8 and R(Q, c2) == 4
    V2 = R(Q, c2 + c3)
    assert V2 == 3 and c2 * V2 == 18 and c3 * V2 == 6
    assert R(Q ** 2, 2 * c2) - (R((c2 * V2) ** 2, 2 * c2) + R((c3 * V2) ** 2, 2 * c3)) == 12
    Q1, Q2 = symbols("Q1 Q2")
    sol = solve([Eq(-Q1 + Q2, -Q + c2 * V2), Eq(Q1 / c1 + Q2 / c2, E)], [Q1, Q2])
    assert sol[Q1] == 26 and sol[Q2] == 20
    Wbat = E * (sol[Q1] - Q)
    Ubefore = R(Q ** 2, 2 * c1) + R(18 ** 2, 2 * c2)
    Uafter = R(26 ** 2, 2 * c1) + R(20 ** 2, 2 * c2)
    assert Wbat == 24 and Ubefore == 123 and Uafter == 146 and Wbat - (Uafter - Ubefore) == 1
