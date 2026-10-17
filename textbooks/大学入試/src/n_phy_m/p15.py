"""問題集 第15章 直流回路。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
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

def _curve(pts, w=1.6, col="#1d4e89"):
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{col}" stroke-width="{w}"/>'

def _dot(x, y, r=2.6, col="#222"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'

I = lambda s: f'<tspan font-family="Liberation Serif,serif" font-style="italic" font-size="12.5">{s}</tspan>'
SUB = lambda s: f'<tspan dy="3" font-size="8">{s}</tspan>'

# 回路記号（導線を先に描き、その上に記号を重ねる）
def _wire(pts, w=1.2):
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="#222" stroke-width="{w}"/>'

def _R(cx, cy, vert):
    if vert:
        return f'<rect x="{cx-5.5}" y="{cy-15}" width="11" height="30" fill="#fff" stroke="#222" stroke-width="1.2"/>'
    return f'<rect x="{cx-15}" y="{cy-5.5}" width="30" height="11" fill="#fff" stroke="#222" stroke-width="1.2"/>'

def _C(cx, cy, vert):
    if vert:
        return (f'<rect x="{cx-12}" y="{cy-4}" width="24" height="8" fill="#fff"/>' +
                _ln(cx - 11, cy - 4, cx + 11, cy - 4, 2.2) + _ln(cx - 11, cy + 4, cx + 11, cy + 4, 2.2))
    return (f'<rect x="{cx-4}" y="{cy-12}" width="8" height="24" fill="#fff"/>' +
            _ln(cx - 4, cy - 11, cx - 4, cy + 11, 2.2) + _ln(cx + 4, cy - 11, cx + 4, cy + 11, 2.2))

def _E(cx, cy, vert, plus_first=True):
    """電池。長い細線が正極。plus_first=True なら上（左）が正極"""
    a, b = (-3.5, 3.5) if plus_first else (3.5, -3.5)
    if vert:
        return (f'<rect x="{cx-13}" y="{cy-4}" width="26" height="8" fill="#fff"/>' +
                _ln(cx - 12, cy + a, cx + 12, cy + a, 1.3) + _ln(cx - 6, cy + b, cx + 6, cy + b, 3.2))
    return (f'<rect x="{cx-4}" y="{cy-13}" width="8" height="26" fill="#fff"/>' +
            _ln(cx + a, cy - 12, cx + a, cy + 12, 1.3) + _ln(cx + b, cy - 6, cx + b, cy + 6, 3.2))

def _S(x1, y1, x2, y2):
    """開いたスイッチ（水平または鉛直の導線上）"""
    a = _atan2(y2 - y1, x2 - x1) - 0.45
    L = _sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if y1 == y2:
        er = f'<rect x="{min(x1,x2)+1:.1f}" y="{y1-3:.1f}" width="{abs(x2-x1):.1f}" height="6" fill="#fff"/>'
    else:
        er = f'<rect x="{x1-3:.1f}" y="{min(y1,y2)+1:.1f}" width="6" height="{abs(y2-y1):.1f}" fill="#fff"/>'
    return (er + _ln(x1, y1, x1 + L * 0.95 * _cos(a), y1 + L * 0.95 * _sin(a), 1.3) +
            f'<circle cx="{x1}" cy="{y1}" r="2.4" fill="#fff" stroke="#222"/><circle cx="{x2}" cy="{y2}" r="2.4" fill="#fff" stroke="#222"/>')


def _fig_kirchhoff():
    yt, yb = 30, 150
    xs = (110, 220, 330)
    b = [_wire([(xs[0], yt), (xs[2], yt), (xs[2], yb), (xs[0], yb), (xs[0], yt)]), _wire([(xs[1], yt), (xs[1], yb)]),
         _R(xs[0], 62, True), _E(xs[0], 116, True, True), _R(xs[1], 90, True), _R(xs[2], 62, True), _E(xs[2], 116, True, True),
         _dot(xs[1], yt), _dot(xs[1], yb),
         _t(xs[0] - 10, 66, "R" + SUB("1") + " 2.0 Ω", 11, "end"), _t(xs[0] - 16, 120, "E" + SUB("1") + " 10 V", 11, "end"),
         _t(xs[1] + 10, 94, "R" + SUB("3") + " 4.0 Ω", 11, "start"),
         _t(xs[2] + 10, 66, "R" + SUB("2") + " 2.0 Ω", 11, "start"), _t(xs[2] + 16, 120, "E" + SUB("2") + " 4.0 V", 11, "start"),
         _t(xs[0] + 14, 110, "+", 10, "start"), _t(xs[2] - 14, 110, "+", 10, "end"),
         _t(xs[1], yt - 8, "a"), _t(xs[1], yb + 16, "b")]
    return _svg(420, 166, b)


def _fig_bridge():
    yt, yb, xl, xr, xe = 30, 160, 110, 250, 40
    ym = (yt + yb) / 2
    b = [_wire([(xl, yt), (xr, yt), (xr, yb), (xl, yb), (xl, yt)]), _wire([(xl, yt), (xe, yt), (xe, yb), (xl, yb)]),
         _wire([(xl, ym), (xr, ym)]),
         _R(xl, (yt + ym) / 2, True), _R(xl, (ym + yb) / 2, True), _R(xr, (yt + ym) / 2, True), _R(xr, (ym + yb) / 2, True),
         _E(xe, ym, True, True),
         f'<circle cx="{(xl+xr)/2}" cy="{ym}" r="10" fill="#fff" stroke="#222" stroke-width="1.2"/>', _t((xl + xr) / 2, ym + 4, "G", 11),
         _dot(xl, ym), _dot(xr, ym), _dot(xl, yt), _dot(xl, yb),
         _t(xl - 9, (yt + ym) / 2 + 4, "R" + SUB("1"), 11, "end"), _t(xl - 9, (ym + yb) / 2 + 4, "R" + SUB("2"), 11, "end"),
         _t(xr + 9, (yt + ym) / 2 + 4, "R" + SUB("3"), 11, "start"), _t(xr + 9, (ym + yb) / 2 + 4, "R" + I("x"), 11, "start"),
         _t(xl + 6, ym - 6, "C", 11, "start"), _t(xr - 6, ym - 6, "D", 11, "end"),
         _t((xl + xr) / 2, yt - 6, "A"), _t((xl + xr) / 2, yb + 15, "B"), _t(xe - 16, ym + 4, I("E"), 12, "end")]
    return _svg(330, 176, b)


def _fig_rc():
    yt, yb, xe, xr, xc = 30, 150, 40, 200, 290
    ym = (yt + yb) / 2
    b = [_wire([(xe, ym), (xe, yt), (xc, yt), (xc, yb), (xe, yb), (xe, ym)]), _wire([(xr, yt), (xr, yb)]),
         _E(xe, ym, True, True), _S(70, yt, 100, yt), _R(145, yt, False), _R(xr, ym, True), _C(xc, ym, True),
         _dot(xr, yt), _dot(xr, yb),
         _t(xe - 16, ym + 4, I("E"), 12, "end"), _t(85, yt - 10, "S"), _t(145, yt - 11, "R" + SUB("1")),
         _t(xr + 10, ym + 4, "R" + SUB("2"), 11, "start"), _t(xc + 16, ym + 4, I("C"), 12, "start")]
    return _svg(330, 164, b)


def _fig_iv():
    ox, oy, sx, sy = 46, 160, 24, 400
    X = lambda v: ox + sx * v
    Y = lambda i: oy - sy * i
    b = []
    for v in range(1, 11):
        b.append(_ln(X(v), Y(0), X(v), Y(0.35), 0.5, "", "#bbb" if v % 2 else "#999"))
    for k in range(1, 8):
        b.append(_ln(X(0), Y(0.05 * k), X(10), Y(0.05 * k), 0.5, "", "#bbb" if k % 2 else "#999"))
    for v in range(0, 11, 2):
        b.append(_t(X(v), oy + 14, str(v), 10))
    for k in (2, 4, 6):
        b.append(_t(X(0) - 4, Y(0.05 * k) + 4, f"{0.05*k:.2f}", 10, "end"))
    b.append(_arrow(X(0), oy, X(10) + 18, oy))
    b.append(_arrow(X(0), oy, X(0), Y(0.35) - 14))
    b.append(_t(X(10) + 20, oy + 30, "電圧 " + I("V") + " [V]", 10, "end"))
    b.append(_t(X(0) + 6, Y(0.35) - 6, "電流 " + I("I") + " [A]", 10, "start"))
    pts = [(X(v / 20), Y(0.10 * (v / 20) ** 0.5)) for v in range(0, 201)]
    b.append(_curve(pts, 1.8))
    return _svg(330, 196, b)


def _fig_bridge_c():
    yt, yb, xl, xr, xe = 20, 180, 110, 270, 40
    yc, y5 = 88, 112
    b = [_wire([(xl, yt), (xr, yt), (xr, yb), (xl, yb), (xl, yt)]), _wire([(xl, yt), (xe, yt), (xe, yb), (xl, yb)]),
         _wire([(xl, yc), (xr, yc)]), _wire([(xl, y5), (xr, y5)]),
         _R(xl, 52, True), _R(xl, 148, True), _R(xr, 52, True), _R(xr, 148, True),
         _E(xe, 76, True, True), _S(xe, 120, xe, 150), _C((xl + xr) / 2, yc, False), _S(140, y5, 170, y5), _R(215, y5, False),
         _dot(xl, yc), _dot(xl, y5), _dot(xr, yc), _dot(xr, y5), _dot(xl, yt), _dot(xl, yb),
         _t(xl - 9, 56, "R" + SUB("1"), 11, "end"), _t(xl - 9, 152, "R" + SUB("2"), 11, "end"),
         _t(xr + 9, 56, "R" + SUB("3"), 11, "start"), _t(xr + 9, 152, "R" + SUB("4"), 11, "start"),
         _t(xe - 16, 80, I("E"), 12, "end"), _t(xe - 10, 140, "S" + SUB("1"), 11, "end"),
         _t((xl + xr) / 2, yc - 15, I("C"), 12), _t(155, y5 + 17, "S" + SUB("2"), 11), _t(215, y5 + 19, "R" + SUB("5"), 11),
         _t(xl - 9, 104, "P", 11, "end"), _t(xr + 9, 104, "Q", 11, "start")]
    return _svg(330, 194, b)


FIG_B1 = _fig_kirchhoff()
FIG_B2 = _fig_bridge()
FIG_B4 = _fig_rc()
FIG_B5 = _fig_iv()
FIG_C2 = _fig_bridge_c()

CH = {15: {
"goal": r"合成抵抗とキルヒホッフの法則で電流・電位を決め、電力とジュール熱、計器の内部抵抗、コンデンサーを含む回路、非線形抵抗・半導体素子の扱いを身につける。",
"items": [
 {"lv": "A", "tag": "抵抗率と電力", "q": r"抵抗率 $1.7\times10^{-8}\,\Omega\cdot\mathrm m$ の銅でできた、長さ $100\,\mathrm m$、断面積 $2.0\,\mathrm{mm^2}$ の導線がある。<br>(1) この導線の抵抗を求めよ。<br>(2) この導線に $2.0\,\mathrm A$ の電流を流したとき、導線の両端の電圧と、導線で消費される電力を求めよ。<br>(3) 同じ銅で、長さが 3 倍、直径が 2 倍の導線をつくると、抵抗はいくらになるか。",
  "a": r"(1) $0.85\,\Omega$　(2) $1.7\,\mathrm V$、$3.4\,\mathrm W$　(3) $0.64\,\Omega$",
  "s": r"(1) $R=\rho\dfrac lS=1.7\times10^{-8}\times\dfrac{100}{2.0\times10^{-6}}=0.85\,\Omega$（$1\,\mathrm{mm^2}=10^{-6}\,\mathrm{m^2}$）。<br>(2) $V=RI=0.85\times2.0=1.7\,\mathrm V$、$P=VI=3.4\,\mathrm W$。<br>(3) 直径 2 倍で断面積は 4 倍。$R'=0.85\times\dfrac34\fallingdotseq0.64\,\Omega$。<br><b>ポイント</b>：$R=\rho\dfrac lS$。面積は直径の 2 乗に比例する。単位 $\mathrm{mm^2}$ の換算（$10^{-6}$）に注意。"},
 {"lv": "A", "tag": "合成抵抗", "q": r"$4.0\,\Omega$ の抵抗 $R_1$ と $12\,\Omega$ の抵抗 $R_2$ を並列につないだものに、$3.0\,\Omega$ の抵抗 $R_3$ を直列につなぎ、内部抵抗の無視できる起電力 $12\,\mathrm V$ の電池につないだ。<br>(1) 合成抵抗を求めよ。<br>(2) $R_3$ を流れる電流と、$R_1$、$R_2$ を流れる電流をそれぞれ求めよ。<br>(3) $R_3$ で消費される電力と、回路全体で消費される電力を求めよ。",
  "a": r"(1) $6.0\,\Omega$　(2) $R_3$：$2.0\,\mathrm A$、$R_1$：$1.5\,\mathrm A$、$R_2$：$0.50\,\mathrm A$　(3) $12\,\mathrm W$、$24\,\mathrm W$",
  "s": r"(1) 並列部分 $\dfrac{4.0\times12}{4.0+12}=3.0\,\Omega$、全体 $3.0+3.0=6.0\,\Omega$。<br>(2) $I=\dfrac{12}{6.0}=2.0\,\mathrm A$。並列部分の電圧は $2.0\times3.0=6.0\,\mathrm V$ なので $I_1=\dfrac{6.0}{4.0}=1.5\,\mathrm A$、$I_2=\dfrac{6.0}{12}=0.50\,\mathrm A$（和が $2.0\,\mathrm A$）。<br>(3) $P_3=I^2R_3=12\,\mathrm W$、全体 $EI=24\,\mathrm W$。<br><b>ポイント</b>：並列部分は「電圧が共通」、電流は抵抗に反比例して分かれる。答えが出たら電流の和や電力の和で検算する。"},
 {"lv": "A", "tag": "電流計・電圧計", "q": r"(1) 内部抵抗 $0.90\,\Omega$、最大目盛り $10\,\mathrm{mA}$ の電流計で、最大 $100\,\mathrm{mA}$ までの電流を測りたい。どのような抵抗を、どのようにつなげばよいか。<br>(2) 内部抵抗 $1.0\,\mathrm{k\Omega}$、最大目盛り $1.0\,\mathrm V$ の電圧計で、最大 $10\,\mathrm V$ までの電圧を測りたい。どのような抵抗を、どのようにつなげばよいか。",
  "a": r"(1) $0.10\,\Omega$ の抵抗（分流器）を並列につなぐ　(2) $9.0\,\mathrm{k\Omega}$ の抵抗（倍率器）を直列につなぐ",
  "s": r"(1) $100\,\mathrm{mA}$ のうち $10\,\mathrm{mA}$ を電流計に、残り $90\,\mathrm{mA}$ を並列の抵抗に流す。電圧が等しいので $0.90\times10=R\times90$、$R=0.10\,\Omega$。<br>(2) 最大目盛りのとき電圧計に流れる電流は $\dfrac{1.0}{1.0\times10^3}=1.0\,\mathrm{mA}$。残りの $9.0\,\mathrm V$ を直列の抵抗が受け持つので $R=\dfrac{9.0}{1.0\times10^{-3}}=9.0\,\mathrm{k\Omega}$。<br><b>ポイント</b>：測定範囲を $n$ 倍にするには、電流計は $\dfrac{r}{n-1}$ を並列、電圧計は $(n-1)r$ を直列。"},
 {"lv": "A", "tag": "電池の内部抵抗", "q": r"起電力 $E$、内部抵抗 $r$ の電池に、$5.0\,\Omega$ の抵抗をつなぐと $0.50\,\mathrm A$、$2.0\,\Omega$ の抵抗をつなぐと $1.0\,\mathrm A$ の電流が流れた。<br>(1) $E$ と $r$ を求めよ。<br>(2) $5.0\,\Omega$ をつないだときの電池の端子電圧を求めよ。<br>(3) 外部の抵抗 $R$ で消費される電力が最大になる $R$ と、そのときの電力を求めよ。",
  "a": r"(1) $E=3.0\,\mathrm V$、$r=1.0\,\Omega$　(2) $2.5\,\mathrm V$　(3) $R=1.0\,\Omega$、$2.25\,\mathrm W$",
  "s": r"(1) $E=0.50(5.0+r)=1.0(2.0+r)$ より $r=1.0\,\Omega$、$E=3.0\,\mathrm V$。<br>(2) $V=E-rI=3.0-1.0\times0.50=2.5\,\mathrm V$（$=5.0\times0.50$）。<br>(3) $P=\left(\dfrac E{R+r}\right)^2R=\dfrac{E^2}{R+2r+\frac{r^2}R}$。相加平均と相乗平均の関係より $R+\dfrac{r^2}R\geqq2r$（等号は $R=r$）。$R=1.0\,\Omega$ で最大 $\dfrac{E^2}{4r}=2.25\,\mathrm W$。<br><b>ポイント</b>：端子電圧は $V=E-rI$。外部抵抗の消費電力は $R=r$ のとき最大になる。"},
 {"lv": "B", "tag": "キルヒホッフの法則", "q": r"図の回路で、電池の内部抵抗は無視できる。" + FIG_B1 + r"(1) $R_1$、$R_2$、$R_3$ を流れる電流の大きさと向きをそれぞれ求めよ。<br>(2) 点 b に対する点 a の電位を求めよ。<br>(3) $R_3$ で消費される電力、電池 $E_1$ が供給する電力を求めよ。また、電池 $E_2$ では電気エネルギーはどうなっているか。",
  "a": r"(1) $R_1$：$2.2\,\mathrm A$ 上向き、$R_2$：$0.80\,\mathrm A$ 下向き、$R_3$：$1.4\,\mathrm A$ 下向き　(2) $5.6\,\mathrm V$　(3) $7.84\,\mathrm W$、$22\,\mathrm W$。$E_2$ は充電され、$3.2\,\mathrm W$ のエネルギーを受け取っている",
  "s": r"b の電位を 0、a の電位を $V$ とする。左の枝を上向きに流れる電流は $I_1=\dfrac{10-V}{2.0}$、右の枝を上向きに流れる電流は $I_2=\dfrac{4.0-V}{2.0}$、$R_3$ を下向きに流れる電流は $I_3=\dfrac V{4.0}$。<br>a での電流の保存 $I_1+I_2=I_3$ より $\dfrac{14-2V}{2.0}=\dfrac V{4.0}$、$V=5.6\,\mathrm V$。<br>(1) $I_1=2.2\,\mathrm A$（上向き）、$I_2=-0.80\,\mathrm A$ すなわち $R_2$ を下向きに $0.80\,\mathrm A$、$I_3=1.4\,\mathrm A$（下向き）。<br>(2) $5.6\,\mathrm V$。<br>(3) $P_3=1.4^2\times4.0=7.84\,\mathrm W$。$E_1$ は $10\times2.2=22\,\mathrm W$ を供給。$E_2$ には正極から電流が入るので充電され、$4.0\times0.80=3.2\,\mathrm W$ を受け取る。検算：ジュール熱の合計 $2.2^2\times2.0+0.80^2\times2.0+7.84=18.8\,\mathrm W=22-3.2$。<br><b>ポイント</b>：未知数は「電位」でおくと式が少なくてすむ。電流が負に出たら、仮定と逆向きに流れていると読みかえる。"},
 {"lv": "B", "tag": "ホイートストンブリッジ", "q": r"図の回路で、$R_1=10\,\Omega$、$R_2=20\,\Omega$、$R_3=15\,\Omega$ である。電池の起電力は $E=9.0\,\mathrm V$、内部抵抗は無視できる。" + FIG_B2 + r"(1) 検流計 G に電流が流れないとき、$R_1,\ R_2,\ R_3,\ R_x$ の間に成り立つ関係を導け。<br>(2) G に電流が流れないときの $R_x$ を求めよ。<br>(3) $R_x$ を $20\,\Omega$ にかえ、G を取り外した。点 D に対する点 C の電位を求めよ。<br>(4) (3) のとき、電池を流れる電流を求めよ。",
  "a": r"(1) $\dfrac{R_1}{R_2}=\dfrac{R_3}{R_x}$　(2) $30\,\Omega$　(3) $\dfrac67\,\mathrm V\fallingdotseq0.86\,\mathrm V$　(4) $0.56\,\mathrm A$",
  "s": r"(1) G に電流が流れないとき、C と D は同電位。$R_1$ と $R_2$ には同じ電流 $I_1$、$R_3$ と $R_x$ には同じ電流 $I_2$ が流れ、$R_1I_1=R_3I_2$、$R_2I_1=R_xI_2$。辺々割って $\dfrac{R_1}{R_2}=\dfrac{R_3}{R_x}$。<br>(2) $R_x=\dfrac{R_2R_3}{R_1}=\dfrac{20\times15}{10}=30\,\Omega$。<br>(3) B の電位を 0 とすると、$V_\mathrm C=9.0\times\dfrac{20}{10+20}=6.0\,\mathrm V$、$V_\mathrm D=9.0\times\dfrac{20}{15+20}=\dfrac{36}7\,\mathrm V$。$V_\mathrm C-V_\mathrm D=\dfrac67\fallingdotseq0.86\,\mathrm V$（C が高い）。<br>(4) $\dfrac{9.0}{30}+\dfrac{9.0}{35}\fallingdotseq0.30+0.26=0.56\,\mathrm A$。<br><b>ポイント</b>：ブリッジのつりあいは「向かい合う抵抗の積が等しい」（$R_1R_x=R_2R_3$）。つりあっていないときは、各枝の電位を分圧で出して比べる。"},
 {"lv": "B", "tag": "半導体・ダイオード", "q": r"(1) 次の文のうち、誤っているものを 1 つ選び、正しく直せ。<br>ア　ケイ素にリン（価電子 5 個）をわずかに加えると n 型半導体になり、おもに自由電子が電流を運ぶ。<br>イ　ケイ素にホウ素（価電子 3 個）をわずかに加えると p 型半導体になり、おもに正孔（ホール）が電流を運ぶ。<br>ウ　半導体の抵抗率は、温度が上がると大きくなる。<br>エ　pn 接合ダイオードは、p 型側を電池の正極側につないだとき（順方向）に電流をよく流す。<br>(2) 起電力 $6.0\,\mathrm V$ の電池（内部抵抗は無視）に、ダイオード $\mathrm{D_1}$ と $2.0\,\mathrm{k\Omega}$ の抵抗を直列にした枝と、ダイオード $\mathrm{D_2}$ と $3.0\,\mathrm{k\Omega}$ の抵抗を直列にした枝を、並列につないだ。$\mathrm{D_1}$ は順方向、$\mathrm{D_2}$ は逆方向の向きである。ダイオードは理想的で、順方向では抵抗 0、逆方向では電流を流さないとする。電池を流れる電流を求めよ。また、電池の向きを逆にしたときの電流を求めよ。<br>(3) (2) のはじめの向きで、$\mathrm{D_1}$ が電流を流すとき両端に一定の電圧 $0.60\,\mathrm V$ がかかるとすると、電池を流れる電流はいくらか。",
  "a": r"(1) ウ。温度が上がると抵抗率は小さくなる　(2) $3.0\,\mathrm{mA}$、逆向きでは $2.0\,\mathrm{mA}$　(3) $2.7\,\mathrm{mA}$",
  "s": r"(1) 半導体では、温度が上がると熱運動によってキャリア（自由電子と正孔）が増えるので、抵抗率は小さくなる（金属は逆に大きくなる）。ア・イ・エは正しい。<br>(2) はじめの向きでは $\mathrm{D_1}$ の枝だけに電流が流れ $\dfrac{6.0}{2.0\times10^3}=3.0\times10^{-3}\,\mathrm A$。逆向きでは $\mathrm{D_2}$ の枝だけに流れ $\dfrac{6.0}{3.0\times10^3}=2.0\times10^{-3}\,\mathrm A$。<br>(3) 抵抗にかかる電圧は $6.0-0.60=5.4\,\mathrm V$。$\dfrac{5.4}{2.0\times10^3}=2.7\times10^{-3}\,\mathrm A$。<br><b>ポイント</b>：ダイオードは「順方向なら導線（または一定の電圧降下）、逆方向なら断線」と置きかえて回路を解く。"},
 {"lv": "B", "tag": "コンデンサーを含む回路", "q": r"図の回路で、$E=12\,\mathrm V$（内部抵抗は無視）、$R_1=20\,\Omega$、$R_2=40\,\Omega$、$C=5.0\,\mu\mathrm F$ である。はじめ S は開いていて、コンデンサーに電荷はない。" + FIG_B4 + r"(1) S を閉じた直後に $R_1$ を流れる電流を求めよ。<br>(2) S を閉じて十分時間がたったときの、$R_1$ を流れる電流、コンデンサーの電圧と電気量、静電エネルギーを求めよ。<br>(3) その後 S を開いた。開いた直後に $R_2$ を流れる電流と、開いてから十分時間がたつまでに $R_2$ で発生するジュール熱を求めよ。",
  "a": r"(1) $0.60\,\mathrm A$　(2) $0.20\,\mathrm A$、$8.0\,\mathrm V$、$4.0\times10^{-5}\,\mathrm C$、$1.6\times10^{-4}\,\mathrm J$　(3) $0.20\,\mathrm A$、$1.6\times10^{-4}\,\mathrm J$",
  "s": r"(1) 閉じた直後はコンデンサーの電圧が 0 で、導線と同じ。$R_2$ の両端の電圧も 0 なので $R_2$ には流れず、$I=\dfrac{12}{20}=0.60\,\mathrm A$。<br>(2) 十分時間がたつとコンデンサーには電流が流れない。$I=\dfrac{12}{20+40}=0.20\,\mathrm A$。コンデンサーの電圧は $R_2$ の電圧 $40\times0.20=8.0\,\mathrm V$、$Q=5.0\times10^{-6}\times8.0=4.0\times10^{-5}\,\mathrm C$、$U=\dfrac12CV^2=1.6\times10^{-4}\,\mathrm J$。<br>(3) S を開くと、コンデンサーは $R_2$ だけを通って放電する。直後の電圧は $8.0\,\mathrm V$ のままなので電流は $\dfrac{8.0}{40}=0.20\,\mathrm A$。蓄えられていた $1.6\times10^{-4}\,\mathrm J$ がすべて $R_2$ のジュール熱になる。<br><b>ポイント</b>：コンデンサーは「直後は電圧が変わらない（電荷 0 なら導線）」「十分後は電流 0（断線）」と置きかえる。"},
 {"lv": "B", "tag": "非線形抵抗", "q": r"図は、ある電球の電圧 $V$ と電流 $I$ の関係（特性曲線）である。電池の内部抵抗は無視できる。" + FIG_B5 + r"(1) この電球を $9.0\,\mathrm V$ で使うときの消費電力と、そのときの電球の抵抗を求めよ。<br>(2) この電球と $10\,\Omega$ の抵抗を直列にして、起電力 $12\,\mathrm V$ の電池につないだ。電球を流れる電流と電球にかかる電圧を求めよ。<br>(3) この電球 2 個を並列にしたものに $5.0\,\Omega$ の抵抗を直列につなぎ、起電力 $6.0\,\mathrm V$ の電池につないだ。電球 1 個を流れる電流と電球の電圧を求めよ。",
  "a": r"(1) $2.7\,\mathrm W$、$30\,\Omega$　(2) $0.30\,\mathrm A$、$9.0\,\mathrm V$　(3) $0.20\,\mathrm A$、$4.0\,\mathrm V$",
  "s": r"(1) グラフより $9.0\,\mathrm V$ で $0.30\,\mathrm A$。$P=9.0\times0.30=2.7\,\mathrm W$、$R=\dfrac{9.0}{0.30}=30\,\Omega$。<br>(2) 電球の電圧を $V$、電流を $I$ とすると $12=V+10I$、すなわち $I=1.2-\dfrac V{10}$。この直線（$(0,\ 1.2)$ と $(12,\ 0)$ を通る）を特性曲線と同じグラフにかき、交点を読むと $V=9.0\,\mathrm V$、$I=0.30\,\mathrm A$。<br>(3) 抵抗には $2I$ が流れるので $6.0=V+5.0\times2I$、$I=0.60-\dfrac V{10}$。交点は $V=4.0\,\mathrm V$、$I=0.20\,\mathrm A$。<br><b>ポイント</b>：電球のように抵抗が一定でない素子は、オームの法則で解かず「回路の式（直線）と特性曲線の交点」で求める。電球の抵抗は電流が大きいほど（温度が高いほど）大きい。"},
 {"lv": "C", "tag": "総合・充電とエネルギー", "q": r"内部抵抗の無視できる電池（起電力 $E$）、抵抗値 $R$ の抵抗、電気容量 $C$ のコンデンサー（はじめ電荷 0）、スイッチを直列につなぐ。<br>(1) スイッチを閉じた直後の電流と、コンデンサーの電圧が $V$ になったときの電流を求めよ。<br>(2) 十分時間がたつまでに電池がした仕事 $W$、コンデンサーに蓄えられた静電エネルギー $U$、抵抗で発生したジュール熱 $J$ を求めよ。$J$ は $R$ によらないことを確かめよ。<br>(3) 次に、別の方法で充電する。電荷 0 のコンデンサーを、まず起電力 $\dfrac E2$ の電池で十分に充電し、続いて電池を起電力 $E$ のものにかえて十分に充電する。それぞれの段階で抵抗に発生するジュール熱と、その合計を求めよ。<br>(4) 起電力を $\dfrac En,\ \dfrac{2E}n,\ \cdots,\ E$ と $n$ 段階で上げて充電すると、ジュール熱の合計はいくらになるか。$n$ を大きくするとどうなるか。",
  "a": r"(1) $\dfrac ER$、$\dfrac{E-V}R$　(2) $W=CE^2$、$U=\dfrac12CE^2$、$J=\dfrac12CE^2$　(3) 1 段階目 $\dfrac18CE^2$、2 段階目 $\dfrac18CE^2$、合計 $\dfrac14CE^2$　(4) $\dfrac{CE^2}{2n}$。$n$ を大きくすると 0 に近づく",
  "s": r"(1) 直後はコンデンサーの電圧 0 なので $\dfrac ER$。電圧 $V$ のときは抵抗の電圧が $E-V$ で $\dfrac{E-V}R$。<br>(2) 電池を通った電気量は $CE$ なので $W=E\cdot CE=CE^2$。$U=\dfrac12CE^2$。$J=W-U=\dfrac12CE^2$ で $R$ を含まない（$R$ が小さいと電流は大きいが短時間で終わる）。<br>(3) 1 段階目：電池の仕事 $\dfrac E2\cdot\dfrac{CE}2=\dfrac{CE^2}4$、$U_1=\dfrac12C\left(\dfrac E2\right)^2=\dfrac{CE^2}8$、ジュール熱 $\dfrac{CE^2}8$。<br>2 段階目：電気量が $\dfrac{CE}2$ 増えるので電池の仕事 $E\cdot\dfrac{CE}2=\dfrac{CE^2}2$、エネルギーの増加 $\dfrac12CE^2-\dfrac18CE^2=\dfrac38CE^2$、ジュール熱 $\dfrac18CE^2$。合計 $\dfrac14CE^2$（一度に充電したときの半分）。<br>(4) $k$ 段階目では電池の仕事 $\dfrac{kE}n\cdot\dfrac{CE}n$、エネルギーの増加 $\dfrac12C\dfrac{E^2}{n^2}\{k^2-(k-1)^2\}=\dfrac{(2k-1)CE^2}{2n^2}$。ジュール熱は $\dfrac{kCE^2}{n^2}-\dfrac{(2k-1)CE^2}{2n^2}=\dfrac{CE^2}{2n^2}$（$k$ によらない）。合計 $n\times\dfrac{CE^2}{2n^2}=\dfrac{CE^2}{2n}$。$n\to\infty$ で 0 に近づく。<br><b>ポイント</b>：ジュール熱は直接求めず「電池の仕事 $-$ 静電エネルギーの増加」で出す。電池の仕事は（起電力）×（通った電気量）。"},
 {"lv": "C", "tag": "総合・ブリッジとコンデンサー", "q": r"図の回路で、$E=12\,\mathrm V$（内部抵抗は無視）、$R_1=2.0\,\Omega$、$R_2=4.0\,\Omega$、$R_3=4.0\,\Omega$、$R_4=2.0\,\Omega$、$R_5=2.0\,\Omega$、$C=3.0\,\mu\mathrm F$ である。はじめ $\mathrm{S_1}$、$\mathrm{S_2}$ は開いていて、コンデンサーに電荷はない。" + FIG_C2 + r"(1) $\mathrm{S_1}$ を閉じて十分時間がたった。コンデンサーの電圧と電気量を求めよ。また、P 側と Q 側のどちらの極板が正に帯電しているか。<br>(2) 続いて $\mathrm{S_2}$ を閉じた。閉じた直後に $R_5$ を流れる電流を求めよ。<br>(3) $\mathrm{S_2}$ を閉じて十分時間がたった。$R_5$ を流れる電流と、コンデンサーの電気量を求めよ。<br>(4) その後、$\mathrm{S_2}$ を閉じたまま $\mathrm{S_1}$ を開いた。開いてから十分時間がたつまでに $R_5$ で発生するジュール熱を求めよ。",
  "a": r"(1) $4.0\,\mathrm V$、$1.2\times10^{-5}\,\mathrm C$、P 側　(2) $2.0\,\mathrm A$　(3) $\dfrac67\,\mathrm A\fallingdotseq0.86\,\mathrm A$、$\dfrac{36}7\,\mu\mathrm C\fallingdotseq5.1\times10^{-6}\,\mathrm C$　(4) $\dfrac{648}{245}\,\mu\mathrm J\fallingdotseq2.6\times10^{-6}\,\mathrm J$",
  "s": r"電池の負極側（下の導線）の電位を 0 とする。<br>(1) コンデンサーに電流は流れないので、左右の枝はそれぞれ直列。$V_\mathrm P=12\times\dfrac{4.0}{6.0}=8.0\,\mathrm V$、$V_\mathrm Q=12\times\dfrac{2.0}{6.0}=4.0\,\mathrm V$。電圧 $4.0\,\mathrm V$、$Q=3.0\times4.0=12\,\mu\mathrm C$。電位の高い P 側が正。<br>(2) 直後のコンデンサーの電圧は $4.0\,\mathrm V$ のまま。$R_5$ はコンデンサーと並列なので $\dfrac{4.0}{2.0}=2.0\,\mathrm A$。<br>(3) P、Q の電位を $x$、$y$ とすると、電流の保存より<br>P：$\dfrac{12-x}{2.0}=\dfrac x{4.0}+\dfrac{x-y}{2.0}$、Q：$\dfrac{12-y}{4.0}+\dfrac{x-y}{2.0}=\dfrac y{2.0}$。<br>整理して $5x-2y=24$、$2x-5y=-12$。解いて $x=\dfrac{48}7$、$y=\dfrac{36}7$。$R_5$ の電流 $\dfrac{x-y}{2.0}=\dfrac67\fallingdotseq0.86\,\mathrm A$、コンデンサーの電気量 $3.0\times\dfrac{12}7=\dfrac{36}7\fallingdotseq5.1\,\mu\mathrm C$。<br>(4) 蓄えられたエネルギーは $\dfrac12\times3.0\times10^{-6}\times\left(\dfrac{12}7\right)^2=\dfrac{216}{49}\,\mu\mathrm J$。$\mathrm{S_1}$ を開くと電池の枝が切れ、P–Q 間は $R_5$（$2.0\,\Omega$）、$R_1+R_3$（$6.0\,\Omega$）、$R_2+R_4$（$6.0\,\Omega$）の 3 本の並列になる。どの瞬間も 3 本の電圧は等しいので、ジュール熱は抵抗に反比例して分かれ、$R_5$ の割合は $\dfrac{1/2.0}{1/2.0+1/6.0+1/6.0}=\dfrac35$。$\dfrac{216}{49}\times\dfrac35=\dfrac{648}{245}\fallingdotseq2.6\,\mu\mathrm J$。<br><b>ポイント</b>：定常状態ではコンデンサーを断線とみなし、電位を未知数にして電流の保存を立てる。放電の熱の分配は「並列なら電圧共通 → 電力は $\dfrac{V^2}R$ に比例」で決まる。"},
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
    Rw = R(17, 10 ** 9) * 100 / R(2, 10 ** 6)
    assert Rw == R(85, 100) and Rw * 2 == R(17, 10) and Rw * 4 == R(34, 10)
    _sf(Rw * 3 / 4, 0.64, 2)
    # A2
    par = R(4 * 12, 16)
    assert par == 3 and par + 3 == 6
    I = R(12, 6); Vp = I * par
    assert I == 2 and Vp / 4 == R(3, 2) and Vp / 12 == R(1, 2) and I ** 2 * 3 == 12 and 12 * I == 24
    # A3
    assert R(9, 10) * 10 / (100 - 10) == R(1, 10)
    assert R(9) / R(1, 1000) == 9000
    # A4
    E, r = symbols("E r")
    sol = solve([Eq(E, R(1, 2) * (5 + r)), Eq(E, 1 * (2 + r))], [E, r])
    assert sol[E] == 3 and sol[r] == 1
    Rv = symbols("R", positive=True)
    P = (3 / (Rv + 1)) ** 2 * Rv
    crit = solve(diff(P, Rv), Rv)
    assert crit == [1] and P.subs(Rv, 1) == R(9, 4)
    assert 3 - 1 * R(1, 2) == R(5, 2)
    # B1
    V = symbols("V")
    Vs = solve(Eq((10 - V) / 2 + (4 - V) / 2, V / 4), V)[0]
    assert Vs == R(28, 5)
    I1, I2, I3 = (10 - Vs) / 2, (4 - Vs) / 2, Vs / 4
    assert I1 == R(11, 5) and I2 == R(-4, 5) and I3 == R(7, 5)
    assert I3 ** 2 * 4 == R(784, 100) and 10 * I1 == 22 and 4 * (-I2) == R(16, 5)
    assert I1 ** 2 * 2 + I2 ** 2 * 2 + I3 ** 2 * 4 == 22 - R(16, 5)
    # B2
    assert R(20 * 15, 10) == 30
    Vc, Vd = 9 * R(20, 30), 9 * R(20, 35)
    assert Vc - Vd == R(6, 7)
    _sf(Vc - Vd, 0.86, 2); _sf(R(9, 30) + R(9, 35), 0.56, 2)
    # B3
    assert R(6, 2000) == R(3, 1000) and R(6, 3000) == R(2, 1000) and (6 - R(6, 10)) / 2000 == R(27, 10000)
    # B4
    E, R1, R2, C = 12, 20, 40, R(5, 10 ** 6)
    assert R(E, R1) == R(3, 5)
    Is = R(E, R1 + R2); Vc = Is * R2
    assert Is == R(1, 5) and Vc == 8 and C * Vc == R(4, 10 ** 5) and C * Vc ** 2 / 2 == R(16, 10 ** 5)
    assert Vc / R2 == R(1, 5)
    # B5
    f = lambda v: R(1, 10) * sqrt(v)
    assert f(9) == R(3, 10) and 9 * f(9) == R(27, 10) and 9 / f(9) == 30
    v = symbols("v", positive=True)
    assert solve(Eq(12, v + 10 * f(v)), v) == [9]
    assert solve(Eq(6, v + 5 * 2 * f(v)), v) == [4] and f(4) == R(1, 5)
    # C1
    Ee, Rr, Cc, Vv = symbols("E R C V", positive=True)
    n, k = symbols("n k", positive=True, integer=True)
    W = Ee * Cc * Ee; U = Cc * Ee ** 2 / 2
    assert simplify(W - U - Cc * Ee ** 2 / 2) == 0
    h1 = (Ee / 2) * (Cc * Ee / 2) - Cc * (Ee / 2) ** 2 / 2
    h2 = Ee * (Cc * Ee / 2) - (Cc * Ee ** 2 / 2 - Cc * (Ee / 2) ** 2 / 2)
    assert simplify(h1 - Cc * Ee ** 2 / 8) == 0 and simplify(h2 - Cc * Ee ** 2 / 8) == 0
    hk = (k * Ee / n) * (Cc * Ee / n) - Cc * Ee ** 2 / (2 * n ** 2) * (k ** 2 - (k - 1) ** 2)
    assert simplify(hk - Cc * Ee ** 2 / (2 * n ** 2)) == 0
    assert simplify(summation(hk, (k, 1, n)) - Cc * Ee ** 2 / (2 * n)) == 0
    # C2
    assert 12 * R(4, 6) == 8 and 12 * R(2, 6) == 4 and 3 * 4 == 12 and R(4, 2) == 2
    x, y = symbols("x y")
    s = solve([Eq((12 - x) / 2, x / 4 + (x - y) / 2), Eq((12 - y) / 4 + (x - y) / 2, y / 2)], [x, y])
    assert s[x] == R(48, 7) and s[y] == R(36, 7)
    dv = s[x] - s[y]
    assert dv / 2 == R(6, 7) and 3 * dv == R(36, 7)
    _sf(dv / 2, 0.86, 2); _sf(3 * dv, 5.1, 2)
    Ue = R(1, 2) * 3 * dv ** 2
    frac = R(1, 2) / (R(1, 2) + R(1, 6) + R(1, 6))
    assert Ue == R(216, 49) and frac == R(3, 5) and Ue * frac == R(648, 245)
    _sf(Ue * frac, 2.6, 2)
