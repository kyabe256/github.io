"""問題集 第2章 力と運動の法則。CH に問題、verify() で答えを sympy で検算する。"""
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


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _arc(cx, cy, r, a1, a2, c="#555"):
    """角 a1→a2（度、反時計回り、y 軸は上向きとして）の円弧"""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{c}" stroke-width="1"/>'


def _box(cx, cy, w, h, ang=0, label="", fill="#e8eef8"):
    """中心 (cx,cy)、幅 w・高さ h、画面上で ang 度（反時計回り）傾けた箱"""
    s = (f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({-ang})"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" '
         f'fill="{fill}" stroke="#333" stroke-width="1.2"/></g>')
    return s + (_tx(cx, cy + 4, label, 11, anchor="middle") if label else "")


def _ceil(x1, x2, y):
    s = [_ln(x1, y, x2, y, "#333", 1.6)]
    x = x1
    while x < x2 - 1:
        s.append(_ln(x + 6, y - 6, x, y, "#777", 0.8))
        x += 8
    return "".join(s)


def _pul(cx, cy, r=8):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#fff" stroke="#333" stroke-width="1.2"/><circle cx="{cx:.1f}" cy="{cy:.1f}" r="1.6" fill="#333"/>'


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _fig_two_strings():
    kx, ky, top = 120, 92, 20
    d = ky - top
    p1 = (kx - d * math.tan(math.radians(30)), top)
    p2 = (kx + d * math.tan(math.radians(60)), top)
    s = [_ceil(p1[0] - 20, p2[0] + 10, top), _ln(kx, ky, *p1, "#1d4e89", 1.4), _ln(kx, ky, *p2, "#1d4e89", 1.4),
         _ln(kx, ky, kx, ky - 50, "#999", 1, "3,2"), _ln(kx, ky, kx, ky + 22, "#333", 1.2),
         _box(kx, ky + 32, 40, 20, 0, "2.0 kg"), _arc(kx, ky, 26, 90, 120), _arc(kx, ky, 20, 30, 90),
         _tx(kx - 20, ky - 30, "30°", 10, anchor="middle"), _tx(kx + 20, ky - 24, "60°", 10, anchor="start"),
         _tx(kx - 34, ky - 50, "糸1", 10, anchor="end"), _tx(kx + 80, ky - 40, "糸2", 10)]
    return _svg(270, 140, s)


def _fig_incline_pulley():
    th = math.radians(30)
    x0, y0, base = 20, 150, 200
    tx_, ty_ = x0 + base, y0 - base * math.tan(th)
    u = (math.cos(th), -math.sin(th))          # 斜面に沿って上向き（画面座標）
    n = (-math.sin(th), -math.cos(th))         # 斜面から外向き
    sA = 110
    bx, by = x0 + sA * u[0], y0 + sA * u[1]
    h = 18
    cx, cy = bx + n[0] * h / 2, by + n[1] * h / 2
    fx, fy = cx + 15 * u[0], cy + 15 * u[1]  # 箱の前面中央（糸の付け根）
    r = 7
    L = base / math.cos(th) + 16
    pcx, pcy = x0 + L * u[0] + n[0] * (h / 2 - r), y0 + L * u[1] + n[1] * (h / 2 - r)
    tpx, tpy = pcx + n[0] * r, pcy + n[1] * r  # 糸が滑車に接する点
    s = [f'<polygon points="{x0},{y0} {tx_:.1f},{y0} {tx_:.1f},{ty_:.1f}" fill="#f2f2f2" stroke="#333" stroke-width="1.2"/>',
         _ln(10, y0, 268, y0, "#333", 1.2), _ln(tx_, ty_, pcx, pcy, "#333", 2),
         _box(cx, cy, 30, h, 30, "A"), _ln(fx, fy, tpx, tpy, "#1d4e89", 1.2),
         _ln(pcx + r, pcy, pcx + r, 100, "#1d4e89", 1.2), _pul(pcx, pcy, r), _box(pcx + r, 110, 20, 20, 0, "B"),
         _arc(x0, y0, 30, 0, 30), _tx(x0 + 36, y0 - 6, "30°", 10)]
    return _svg(270, 160, s)


def _fig_wedge():
    th = math.radians(30)
    x0, x1, y0 = 40, 210, 112
    top = y0 - (x1 - x0) * math.tan(th)
    u = (math.cos(th), math.sin(th))     # 斜面を下る向き（画面座標）
    n = (math.sin(th), -math.cos(th))    # 斜面から外向き
    sb = 70
    bx, by = x0 + sb * u[0], top + sb * u[1]
    s = [_ln(10, y0, 262, y0, "#333", 1.2),
         f'<polygon points="{x0},{y0} {x1},{y0} {x0},{top:.1f}" fill="#f2f2f2" stroke="#333" stroke-width="1.2"/>',
         _box(bx + n[0] * 9, by + n[1] * 9, 24, 18, -30, "m"), _tx(80, 100, "M", 12, True),
         _arc(x1, y0, 30, 150, 180), _tx(x1 - 40, y0 - 5, "θ", 11, True)]
    return _svg(270, 120, s)


def _fig_movable():
    top = 15
    s = [_ceil(40, 150, top), _ln(70, top, 70, 110, "#1d4e89", 1.2), _ln(90, 110, 90, 35, "#1d4e89", 1.2),
         _ln(110, 35, 110, 92, "#1d4e89", 1.2), _ln(100, top, 100, 35, "#333", 1.4), _pul(100, 35, 10),
         _pul(80, 110, 10), _ln(80, 110, 80, 132, "#333", 1.2), _box(110, 102, 22, 20, 0, "A"),
         _box(80, 142, 24, 20, 0, "B"), _tx(117, 40, "定滑車", 10), _tx(66, 114, "動滑車", 10, anchor="end")]
    return _svg(180, 160, s)


CH = {2: {
"goal": r"物体にはたらく力をもれなく図示し、つりあいの式・運動方程式を立てる。摩擦は「静止摩擦（最大摩擦力以下）」と「動摩擦（一定）」を区別し、連結物体は物体ごとに式を立てる。<br>（数値は有効数字2桁、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$。糸・滑車・ばねの質量は無視する。）",
"items": [
 {"lv": "A", "tag": "力のつりあい",
  "q": r"質量 $2.0\,\mathrm{kg}$ のおもりを、天井に結んだ2本の軽い糸1、2でつるしたところ、図のように糸1は鉛直から $30^\circ$、糸2は反対側に鉛直から $60^\circ$ 傾いて静止した。糸1、糸2の張力の大きさ $T_1,\ T_2$ を求めよ。" + _fig_two_strings(),
  "a": r"$T_1\fallingdotseq17\,\mathrm{N}$、$T_2=9.8\,\mathrm{N}$",
  "s": r"おもりの重さは $mg=2.0\times9.8=19.6\,\mathrm{N}$。結び目にはたらく力のつりあいを考える。<br>水平方向：$T_1\sin30^\circ=T_2\sin60^\circ$ より $T_1=\sqrt3\,T_2$。<br>鉛直方向：$T_1\cos30^\circ+T_2\cos60^\circ=mg$。代入すると $\frac32T_2+\frac12T_2=2T_2=mg$。<br>よって $T_2=\frac{mg}{2}=9.8\,\mathrm{N}$、$T_1=\frac{\sqrt3}{2}mg\fallingdotseq17\,\mathrm{N}$。<br>（2本の糸は直交しているので、重力を糸の方向に分解して $T_1=mg\cos30^\circ$、$T_2=mg\cos60^\circ$ としてもよい。）<br><b>ポイント</b>：つりあいは直交する2方向に分けて式を立てる。"},
 {"lv": "A", "tag": "摩擦力と運動方程式",
  "q": r"あらい水平面上に置いた質量 $4.0\,\mathrm{kg}$ の物体を水平に引く。物体と面の間の静止摩擦係数を $0.50$、動摩擦係数を $0.20$ とする。<br>(1) 物体を動かし始めるのに必要な力の大きさの最小値を求めよ。<br>(2) 水平に大きさ $24\,\mathrm{N}$ の力で引き続けるときの加速度の大きさを求めよ。<br>(3) (2) で、静止した状態から引き始めて $4.0\,\mathrm{s}$ 後の速さを求めよ。",
  "a": r"(1) $20\,\mathrm{N}$（$19.6\,\mathrm{N}$）　(2) $4.0\,\mathrm{m/s^2}$　(3) $16\,\mathrm{m/s}$",
  "s": r"垂直抗力は $N=4.0\times9.8=39.2\,\mathrm{N}$。<br>(1) 最大摩擦力 $\mu N=0.50\times39.2=19.6\,\mathrm{N}$ をこえる力が必要。<br>(2) $24\,\mathrm{N}>19.6\,\mathrm{N}$ なので動く。動摩擦力は $\mu'N=0.20\times39.2=7.84\,\mathrm{N}$。運動方程式 $4.0a=24-7.84$ より $a=4.04\fallingdotseq4.0\,\mathrm{m/s^2}$。<br>(3) $v=at=4.04\times4.0\fallingdotseq16\,\mathrm{m/s}$。<br><b>ポイント</b>：動き出すかどうかは最大摩擦力 $\mu N$ と比べて判断し、動いている間は動摩擦力 $\mu'N$ を使う。"},
 {"lv": "A", "tag": "斜面上の運動",
  "q": r"傾斜角 $30^\circ$ の斜面上に質量 $m$ の物体を置く。重力加速度の大きさを $g$ とする。<br>(1) 斜面がなめらかなとき、物体の加速度の大きさと、物体が斜面から受ける垂直抗力の大きさを求めよ。<br>(2) 斜面があらく、物体と斜面の間の動摩擦係数が $0.10$ のとき、すべり下りる物体の加速度の大きさを数値で求めよ。<br>(3) 一般に、傾斜角 $\theta$ のあらい斜面上で物体が静止し続けるための、静止摩擦係数 $\mu$ の条件を求めよ。",
  "a": r"(1) $\frac g2$、$\frac{\sqrt3}{2}mg$　(2) $4.1\,\mathrm{m/s^2}$　(3) $\mu\geqq\tan\theta$",
  "s": r"重力を、斜面に平行な成分 $mg\sin\theta$ と垂直な成分 $mg\cos\theta$ に分解する。<br>(1) 斜面方向の運動方程式 $ma=mg\sin30^\circ$ より $a=\frac g2$。垂直方向のつりあいより $N=mg\cos30^\circ=\frac{\sqrt3}{2}mg$。<br>(2) $ma=mg\sin30^\circ-0.10\times mg\cos30^\circ$ より $a=9.8\times(0.50-0.10\times0.866)\fallingdotseq4.1\,\mathrm{m/s^2}$。<br>(3) 静止に必要な摩擦力 $mg\sin\theta$ が最大摩擦力 $\mu mg\cos\theta$ 以下であればよい。$\mu\geqq\tan\theta$。<br><b>ポイント</b>：斜面では「斜面に平行」と「斜面に垂直」の2方向に分ける。垂直抗力は $mg$ ではなく $mg\cos\theta$。"},
 {"lv": "A", "tag": "作用・反作用",
  "q": r"なめらかな水平面上に、質量 $3.0\,\mathrm{kg}$ の物体 A と質量 $2.0\,\mathrm{kg}$ の物体 B を接して置き、A を水平に大きさ $10\,\mathrm{N}$ の力で押して、B といっしょに動かした。<br>(1) A, B の加速度の大きさを求めよ。<br>(2) A が B を押す力の大きさを求めよ。<br>(3) B が A を押す力の大きさと向きを答えよ。また、この力と (2) の力の関係を表す法則の名前を答えよ。",
  "a": r"(1) $2.0\,\mathrm{m/s^2}$　(2) $4.0\,\mathrm{N}$　(3) $4.0\,\mathrm{N}$、A を押す $10\,\mathrm{N}$ の力と逆向き、作用・反作用の法則",
  "s": r"(1) A と B をひとまとめにすると、水平方向の外力は $10\,\mathrm{N}$ だけ。$(3.0+2.0)a=10$ より $a=2.0\,\mathrm{m/s^2}$。<br>(2) B だけに注目すると、水平方向の力は A から押される力 $F$ だけ。$2.0\times2.0=F$ より $F=4.0\,\mathrm{N}$。<br>(3) 作用・反作用の法則により、大きさは等しく $4.0\,\mathrm{N}$、向きは逆。確かに A の運動方程式 $3.0\times2.0=10-4.0$ も成り立つ。<br><b>ポイント</b>：作用・反作用は「2つの物体が互いに及ぼしあう力」、つりあいは「1つの物体にはたらく力どうし」の関係。"},
 {"lv": "B", "tag": "滑車でつないだ2物体",
  "q": r"なめらかに回る滑車に軽い糸をかけ、両端に質量 $M$ の物体 A と質量 $m$ の物体 B（$M>m$）をつるして静かに放した。重力加速度の大きさを $g$ とする。<br>(1) A の加速度の大きさ $a$ と、糸の張力の大きさ $T$ を $M,\ m,\ g$ で表せ。<br>(2) $M=3.0\,\mathrm{kg}$、$m=2.0\,\mathrm{kg}$ のとき、$a$ と $T$ の値を求めよ。<br>(3) (2) のとき、滑車を天井につるしている糸の張力の大きさを求め、A と B の重さの和と比べよ。",
  "a": r"(1) $a=\frac{M-m}{M+m}g$、$T=\frac{2Mm}{M+m}g$　(2) $a\fallingdotseq2.0\,\mathrm{m/s^2}$、$T\fallingdotseq24\,\mathrm{N}$　(3) $47\,\mathrm{N}$（重さの和 $49\,\mathrm{N}$ より小さい）",
  "s": r"(1) A は下向き、B は上向きに、同じ大きさ $a$ で加速する。<br>A：$Ma=Mg-T$、B：$ma=T-mg$。<br>辺々加えて $(M+m)a=(M-m)g$、$a=\frac{M-m}{M+m}g$。B の式に代入して $T=m(g+a)=\frac{2Mm}{M+m}g$。<br>(2) $a=\frac15\times9.8=1.96\fallingdotseq2.0\,\mathrm{m/s^2}$、$T=\frac{12}{5}\times9.8=23.52\fallingdotseq24\,\mathrm{N}$。<br>(3) 滑車には下向きに張力 $T$ が2本分はたらくので $2T=47.04\fallingdotseq47\,\mathrm{N}$。A と B の重さの和 $5.0\times9.8=49\,\mathrm{N}$ より小さい。<br><b>ポイント</b>：全体の重心が下向きに加速しているので、支える力は重さの和より小さくなる。"},
 {"lv": "B", "tag": "静止摩擦と連結物体",
  "q": r"あらい水平な机の上に質量 $3.0\,\mathrm{kg}$ の物体 A を置き、A につけた軽い糸を机の端の滑車にかけ、他端におもり B をつるす。糸の A 側の部分は水平である。A と机の間の静止摩擦係数を $0.50$、動摩擦係数を $0.20$ とする。<br>(1) A が動き出さないための、B の質量の最大値を求めよ。<br>(2) B の質量を $2.0\,\mathrm{kg}$ にしたとき、A の加速度の大きさと糸の張力の大きさを求めよ。",
  "a": r"(1) $1.5\,\mathrm{kg}$　(2) $2.7\,\mathrm{m/s^2}$、$14\,\mathrm{N}$",
  "s": r"(1) 静止しているとき、張力は B の重さ $m_Bg$ に等しく、これが A にはたらく静止摩擦力とつりあう。静止摩擦力は最大摩擦力 $0.50\times3.0g$ 以下なので $m_Bg\leqq1.5g$、$m_B\leqq1.5\,\mathrm{kg}$。<br>(2) $2.0>1.5$ なので動く。加速度を $a$、張力を $T$ とする。<br>A：$3.0a=T-0.20\times3.0\times9.8$、B：$2.0a=2.0\times9.8-T$。<br>辺々加えて $5.0a=19.6-5.88=13.72$、$a\fallingdotseq2.7\,\mathrm{m/s^2}$。$T=2.0\times(9.8-2.744)\fallingdotseq14\,\mathrm{N}$。<br><b>ポイント</b>：連結物体は物体ごとに運動方程式を立て、加えて張力を消去する。張力は B の重さ $19.6\,\mathrm{N}$ より小さいことも確かめておく。"},
 {"lv": "B", "tag": "重ねた2物体",
  "q": r"なめらかな水平面上に質量 $M=3.0\,\mathrm{kg}$ の板 B を置き、その上に質量 $m=1.0\,\mathrm{kg}$ の小物体 A をのせる。A と B の間の静止摩擦係数は $0.40$、動摩擦係数は $0.20$ である。B に水平右向きの力 $F$ を加える。<br>(1) A と B が一体となって動くための $F$ の最大値を求めよ。<br>(2) $F=24\,\mathrm{N}$ のとき、A と B の加速度の大きさをそれぞれ求めよ。<br>(3) (2) のとき、静止状態から力を加え始めてから、A が B に対して $1.0\,\mathrm{m}$ すべるまでの時間を求めよ。ただし A は B から落ちないものとする。",
  "a": r"(1) $16\,\mathrm{N}$　(2) A：$2.0\,\mathrm{m/s^2}$、B：$7.3\,\mathrm{m/s^2}$　(3) $0.61\,\mathrm{s}$",
  "s": r"(1) 一体で動くときの加速度は $a=\frac{F}{M+m}$。A を加速させる力は B からの静止摩擦力 $f=ma$ だけで、$f\leqq0.40mg$ より $a\leqq0.40g$。よって $F\leqq0.40g(M+m)=0.40\times9.8\times4.0=15.68\fallingdotseq16\,\mathrm{N}$。<br>(2) $24\,\mathrm{N}$ は (1) の値をこえるので、A は B に対してすべる。A にはたらく動摩擦力は右向きに $0.20mg=1.96\,\mathrm{N}$ で、$a_A=0.20g=1.96\fallingdotseq2.0\,\mathrm{m/s^2}$。B にはその反作用が左向きにはたらき、$3.0a_B=24-1.96$ より $a_B\fallingdotseq7.3\,\mathrm{m/s^2}$。<br>(3) B から見た A の加速度は左向きに $a_B-a_A=7.347-1.96\fallingdotseq5.39\,\mathrm{m/s^2}$。$1.0=\frac12\times5.39\,t^2$ より $t\fallingdotseq0.61\,\mathrm{s}$。<br><b>ポイント</b>：まず「一体で動く」と仮定して必要な静止摩擦力を求め、最大摩擦力と比べる。すべるなら各物体に動摩擦力を入れて別々に解く。"},
 {"lv": "B", "tag": "空気抵抗と終端速度",
  "q": r"質量 $m$ の雨滴が、速さ $v$ に比例する空気の抵抗力 $kv$（$k$ は正の定数）を受けながら、鉛直に落下する。重力加速度の大きさを $g$ とする。<br>(1) 速さが $v$ のときの加速度の大きさを求めよ。<br>(2) 十分時間がたつと雨滴の速さは一定になる。この速さ（終端速度）$v_f$ を求めよ。また、$m=4.0\times10^{-6}\,\mathrm{kg}$、$k=1.0\times10^{-5}\,\mathrm{kg/s}$ のときの $v_f$ の値を求めよ。<br>(3) 速さが $v_f$ の半分のときの加速度の大きさを求めよ。<br>(4) $k$ が同じで質量が2倍の雨滴の終端速度は、何倍になるか。",
  "a": r"(1) $g-\frac{kv}{m}$　(2) $v_f=\frac{mg}{k}$、$3.9\,\mathrm{m/s}$　(3) $\frac g2$　(4) 2倍",
  "s": r"(1) 下向きを正として運動方程式 $ma=mg-kv$ より $a=g-\frac{kv}{m}$。<br>(2) 速さが一定のとき $a=0$ なので、$mg=kv_f$ より $v_f=\frac{mg}{k}=\frac{4.0\times10^{-6}\times9.8}{1.0\times10^{-5}}\fallingdotseq3.9\,\mathrm{m/s}$。<br>(3) $v=\frac{v_f}{2}=\frac{mg}{2k}$ を代入して $a=g-\frac g2=\frac g2$。<br>(4) $v_f=\frac{mg}{k}$ は $m$ に比例するので2倍。<br>（$v$-$t$ グラフは、原点での傾きが $g$ で、しだいに傾きが小さくなり $v=v_f$ に近づく曲線になる。）<br><b>ポイント</b>：終端速度は「重力＝抵抗力」のつりあいの条件から求める。"},
 {"lv": "B", "tag": "斜面と静止摩擦の範囲",
  "q": r"図のように、傾斜角 $30^\circ$ のあらい斜面上に質量 $M=2.0\,\mathrm{kg}$ の物体 A を置き、斜面の上端の滑車にかけた軽い糸でおもり B（質量 $m$）とつなぐ。A 側の糸は斜面に平行である。A と斜面の間の静止摩擦係数を $\frac{\sqrt3}{6}$ とする。<br>" + _fig_incline_pulley() +
       r"(1) A が静止したままであるための $m$ の範囲を求めよ。<br>(2) $m=1.2\,\mathrm{kg}$ のとき、A にはたらく静止摩擦力の大きさと向きを求めよ。",
  "a": r"(1) $0.50\,\mathrm{kg}\leqq m\leqq1.5\,\mathrm{kg}$　(2) $2.0\,\mathrm{N}$、斜面に沿って下向き",
  "s": r"最大摩擦力は $\mu Mg\cos30^\circ=\frac{\sqrt3}{6}\cdot\frac{\sqrt3}{2}Mg=\frac14Mg$。張力は B の重さ $mg$ に等しい。<br>(1) A がすべり下りようとする限界（摩擦力は斜面上向き）：$mg+\frac14Mg=Mg\sin30^\circ$ より $m=\frac14M=0.50\,\mathrm{kg}$。<br>A がすべり上がろうとする限界（摩擦力は斜面下向き）：$mg=Mg\sin30^\circ+\frac14Mg$ より $m=\frac34M=1.5\,\mathrm{kg}$。<br>よって $0.50\,\mathrm{kg}\leqq m\leqq1.5\,\mathrm{kg}$。<br>(2) 張力 $1.2\times9.8=11.76\,\mathrm{N}$ が $Mg\sin30^\circ=9.8\,\mathrm{N}$ より大きいので、A は斜面を上がろうとし、摩擦力は斜面下向き。大きさは $11.76-9.8=1.96\fallingdotseq2.0\,\mathrm{N}$（最大摩擦力 $4.9\,\mathrm{N}$ 以下で静止できる）。<br><b>ポイント</b>：静止摩擦力の向きは「すべろうとする向きの逆」。向きが決まらないときは、上向き・下向きの両方の限界を調べる。"},
 {"lv": "C", "tag": "動く三角台",
  "q": r"なめらかな水平面上に、傾斜角 $\theta$ のなめらかな斜面をもつ質量 $M$ の三角台を置き、斜面上に質量 $m$ の小物体をのせる。重力加速度の大きさを $g$ とする。<br>" + _fig_wedge() +
       r"(1) 三角台に水平方向の力を加えて一定の加速度で動かしたところ、小物体は三角台に対して静止したままであった。このときの加速度の大きさ $a_0$ と、加えた力の大きさ $F$ を求めよ。<br>(2) 次に、力を加えずに三角台を自由に動けるようにして、小物体を静かに放した。三角台の加速度の大きさを $A$、小物体と斜面の間の垂直抗力の大きさを $N$ とする。小物体は斜面から離れないので、小物体の加速度の「斜面に垂直な成分」は、三角台の加速度の斜面に垂直な成分 $A\sin\theta$ に等しい。これを用いて、小物体の斜面に垂直な方向の運動方程式と、三角台の水平方向の運動方程式を立て、$A$ と $N$ を求めよ。<br>(3) $M=3m$、$\theta=30^\circ$ のとき、$A$ を $g$ で、$N$ を $mg$ で表せ。",
  "a": r"(1) $a_0=g\tan\theta$、$F=(M+m)g\tan\theta$　(2) $A=\frac{mg\sin\theta\cos\theta}{M+m\sin^2\theta}$、$N=\frac{Mmg\cos\theta}{M+m\sin^2\theta}$　(3) $A=\frac{\sqrt3}{13}g$、$N=\frac{6\sqrt3}{13}mg$",
  "s": r"(1) 小物体は三角台と同じ加速度 $a_0$ で水平に運動する。小物体にはたらく力は重力と垂直抗力 $N_0$ だけ。鉛直：$N_0\cos\theta=mg$、水平：$N_0\sin\theta=ma_0$。よって $a_0=g\tan\theta$（斜面が向いている側へ）。全体では $F=(M+m)a_0=(M+m)g\tan\theta$。<br>(2) 小物体はすべり下り、三角台はその反対側へ動く。<br>小物体（斜面に垂直な方向、斜面に押しつける向きを正）：$mA\sin\theta=mg\cos\theta-N$<br>三角台（水平方向）：$MA=N\sin\theta$<br>第2式の $A=\frac{N\sin\theta}{M}$ を第1式に代入して $N\left(1+\frac{m\sin^2\theta}{M}\right)=mg\cos\theta$。<br>$N=\frac{Mmg\cos\theta}{M+m\sin^2\theta}$、$A=\frac{mg\sin\theta\cos\theta}{M+m\sin^2\theta}$。<br>(3) $\sin\theta=\frac12,\ \cos\theta=\frac{\sqrt3}{2}$、$M+m\sin^2\theta=\frac{13}{4}m$。$A=\frac{\frac{\sqrt3}{4}mg}{\frac{13}{4}m}=\frac{\sqrt3}{13}g$、$N=\frac{3m\cdot mg\cdot\frac{\sqrt3}{2}}{\frac{13}{4}m}=\frac{6\sqrt3}{13}mg$。<br>（三角台が動くので、$N$ は台を固定したときの $mg\cos\theta=\frac{\sqrt3}{2}mg$ より小さい。）<br><b>ポイント</b>：物体どうしが接して動くときは、「接触面に垂直な方向の加速度成分が等しい」という束縛条件を立てると未知数が減る。"},
 {"lv": "C", "tag": "動滑車",
  "q": r"図のように、天井に固定した定滑車と、動滑車がある。糸の一端を天井に固定し、動滑車の下を通して定滑車にかけ、他端に質量 $m_1$ の物体 A をつるす。動滑車には質量 $m_2$ の物体 B をつるす。糸はすべて鉛直で、動滑車の質量は無視する。<br>" + _fig_movable() +
       r"(1) A が下向きに加速度の大きさ $a$ で動くとき、B の加速度の大きさはいくらか。理由も述べよ。<br>(2) A と B の運動方程式を立て、$a$ と糸の張力の大きさ $T$ を $m_1,\ m_2,\ g$ で表せ。また、A が下向きに動くための条件を求めよ。<br>(3) $m_1=m_2=2.0\,\mathrm{kg}$ のとき、$a$、B の加速度の大きさ、$T$ の値を求めよ。<br>(4) (3) のとき、静かに放してから A が $1.0\,\mathrm{m}$ 下降したときの B の速さを求めよ。",
  "a": r"(1) $\frac a2$　(2) $a=\frac{2(2m_1-m_2)}{4m_1+m_2}g$、$T=\frac{3m_1m_2}{4m_1+m_2}g$、$2m_1>m_2$　(3) $a\fallingdotseq3.9\,\mathrm{m/s^2}$、B は $2.0\,\mathrm{m/s^2}$、$T\fallingdotseq12\,\mathrm{N}$　(4) $1.4\,\mathrm{m/s}$",
  "s": r"(1) A が $x$ 下がると、糸の長さは一定なので、動滑車を支える2本の糸の部分の長さの和が $x$ だけ短くなり、1本あたり $\frac x2$ 短くなる。よって B は $\frac x2$ 上がる。加速度も半分で $\frac a2$（上向き）。<br>(2) A（下向き正）：$m_1a=m_1g-T$<br>B（上向き正、動滑車には上向きに張力が2本）：$m_2\cdot\frac a2=2T-m_2g$<br>第1式より $T=m_1(g-a)$。第2式に代入して $\left(2m_1+\frac{m_2}{2}\right)a=(2m_1-m_2)g$、$a=\frac{2(2m_1-m_2)}{4m_1+m_2}g$。$T=m_1(g-a)=\frac{3m_1m_2}{4m_1+m_2}g$。<br>$a>0$ となる条件は $2m_1>m_2$。<br>(3) $a=\frac{2\times2.0}{10}\times9.8=3.92\fallingdotseq3.9\,\mathrm{m/s^2}$、B は $1.96\fallingdotseq2.0\,\mathrm{m/s^2}$、$T=\frac{12}{10}\times9.8=11.76\fallingdotseq12\,\mathrm{N}$。<br>(4) B は $0.50\,\mathrm{m}$ 上昇する。$v^2=2\times1.96\times0.50$ より $v\fallingdotseq1.4\,\mathrm{m/s}$。<br><b>ポイント</b>：動滑車の問題は、まず糸の長さが一定という条件から「変位・速度・加速度の関係」を出す。張力は糸のどこでも同じ $T$。"},
]}}


def verify():
    g = Rational(98, 10)
    # 2-1
    T1, T2 = symbols("T1 T2")
    m = 2
    sol = solve([T1 * sin(pi / 6) - T2 * sin(pi / 3), T1 * cos(pi / 6) + T2 * cos(pi / 3) - m * g], [T1, T2])
    _near(sol[T1], 17); assert sol[T2] == Rational(98, 10)
    # 2-2
    N = 4 * g
    _near(Rational(1, 2) * N, 20); assert Rational(1, 2) * N == Rational(196, 10) < 24
    a = (24 - Rational(2, 10) * N) / 4
    _near(a, 4.0); _near(a * 4, 16)
    # 2-3
    mm, gg, th, mu = symbols("m g theta mu", positive=True)
    _near(9.8 * (0.5 - 0.1 * math.cos(math.pi / 6)), 4.1)
    # 2-4
    a = Rational(10, 5)
    assert a == 2 and 2 * a == 4 and 3 * a == 10 - 4
    # 2-5 アトウッド
    M, m_, aa, TT = symbols("M m a T", positive=True)
    s = solve([M * aa - (M * gg - TT), m_ * aa - (TT - m_ * gg)], [aa, TT])
    _eq(s[aa], (M - m_) * gg / (M + m_)); _eq(s[TT], 2 * M * m_ * gg / (M + m_))
    an, Tn = s[aa].subs({M: 3, m_: 2, gg: g}), s[TT].subs({M: 3, m_: 2, gg: g})
    _near(an, 2.0); _near(Tn, 24); _near(2 * Tn, 47); assert 2 * Tn < 5 * g
    # 2-6
    assert Rational(5, 10) * 3 == Rational(3, 2)
    a, T = symbols("a T")
    s = solve([3 * a - (T - Rational(2, 10) * 3 * g), 2 * a - (2 * g - T)], [a, T])
    _near(s[a], 2.7); _near(s[T], 14)
    # 2-7 重ねた物体
    Fmax = Rational(4, 10) * g * 4
    _near(Fmax, 16); assert 24 > Fmax
    aA = Rational(2, 10) * g; aB = (24 - Rational(2, 10) * 1 * g) / 3
    _near(aA, 2.0); _near(aB, 7.3)
    t = sqrt(2 * 1 / (aB - aA)); _near(t, 0.61)
    # 2-8 終端速度
    k, v = symbols("k v", positive=True)
    acc = gg - k * v / mm
    vf = solve(acc, v)[0]
    _eq(vf, mm * gg / k)
    _near(vf.subs({mm: 4.0e-6, gg: 9.8, k: 1.0e-5}), 3.9)
    _eq(acc.subs(v, vf / 2), gg / 2)
    _eq(vf.subs(mm, 2 * mm) / vf, 2)
    # 2-9 斜面の静止範囲
    Mv = 2
    fmax = sqrt(3) / 6 * Mv * g * cos(pi / 6)
    _eq(fmax, Mv * g / 4)
    mlo = solve(Eq(m_ * g + fmax, Mv * g * sin(pi / 6)), m_)[0]
    mhi = solve(Eq(m_ * g, Mv * g * sin(pi / 6) + fmax), m_)[0]
    assert mlo == Rational(1, 2) and mhi == Rational(3, 2)
    f = Rational(12, 10) * g - Mv * g * sin(pi / 6)
    _near(f, 2.0); assert 0 < f <= fmax
    # 2-10 動く三角台：地上での運動方程式を一般に解いて比較
    A_, b_, N_ = symbols("A b N")
    # 三角台は左へ A、小物体の台に対する加速度は斜面に沿って下向き b。n=(sin,cos) は斜面の外向き法線
    eqs = [mm * (-A_ + b_ * cos(th)) - N_ * sin(th),        # 小物体 x
           mm * (-b_ * sin(th)) - (N_ * cos(th) - mm * gg),  # 小物体 y
           M * (-A_) + N_ * sin(th)]                          # 三角台 x
    s = solve(eqs, [A_, b_, N_], dict=True)[0]
    _eq(s[A_], mm * gg * sin(th) * cos(th) / (M + mm * sin(th) ** 2))
    _eq(s[N_], M * mm * gg * cos(th) / (M + mm * sin(th) ** 2))
    A3 = s[A_].subs({M: 3 * mm, th: pi / 6}); N3 = s[N_].subs({M: 3 * mm, th: pi / 6})
    _eq(A3, sqrt(3) * gg / 13); _eq(N3, 6 * sqrt(3) * mm * gg / 13)
    # (1) 台に対して静止
    N0, a0 = symbols("N0 a0")
    s1 = solve([N0 * cos(th) - mm * gg, N0 * sin(th) - mm * a0], [N0, a0], dict=True)[0]
    _eq(s1[a0], gg * tan(th))
    # 2-11 動滑車
    m1, m2 = symbols("m1 m2", positive=True)
    s = solve([m1 * aa - (m1 * gg - TT), m2 * aa / 2 - (2 * TT - m2 * gg)], [aa, TT])
    _eq(s[aa], 2 * (2 * m1 - m2) * gg / (4 * m1 + m2)); _eq(s[TT], 3 * m1 * m2 * gg / (4 * m1 + m2))
    an = s[aa].subs({m1: 2, m2: 2, gg: g}); Tn = s[TT].subs({m1: 2, m2: 2, gg: g})
    _near(an, 3.9); _near(an / 2, 2.0); _near(Tn, 12)
    _near(sqrt(2 * an / 2 * Rational(1, 2)), 1.4)
