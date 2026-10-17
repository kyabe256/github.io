"""第19章 空間ベクトル（数学C）  担当 M19"""
import math

# ---------------------------------------------------------------- 図の道具（座標は Python で計算）
_INK, _HID, _ACC, _FILL = "#222", "#777", "#c0392b", "#d6e3f7"


def _pj(p, az, el):
    """正射影：z 軸のまわりに az 度回し、仰角 el 度から見る。(画面x, 画面y上向き)"""
    a, e = math.radians(az), math.radians(el)
    x, y, z = p
    x1 = x * math.cos(a) - y * math.sin(a)
    y1 = x * math.sin(a) + y * math.cos(a)
    return x1, y1 * math.sin(e) + z * math.cos(e)


def _fit(pts, W, H, pad):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    s = min((W - 2 * pad) / ((x1 - x0) or 1), (H - 2 * pad) / ((y1 - y0) or 1))
    ox, oy = (W - s * (x0 + x1)) / 2, (H + s * (y0 + y1)) / 2
    return (lambda q: (ox + s * q[0], oy - s * q[1])), s


def _ln(p, q, col=_INK, w=1.1, dash=False):
    d = ' stroke-dasharray="3,2"' if dash else ""
    return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'


def _tx(p, s, dx=0, dy=0, size=11, col=_INK):
    return f'<text x="{p[0] + dx:.1f}" y="{p[1] + dy + 4:.1f}" font-size="{size}" text-anchor="middle" font-family="serif" fill="{col}">{s}</text>'


def _dot(p, col=_INK, r=1.7):
    return f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{col}"/>'


def _poly(ps, fill=_FILL, op=0.85):
    pts = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in ps)
    return f'<polygon points="{pts}" fill="{fill}" fill-opacity="{op}" stroke="none"/>'


def _edges_vis(P, faces, view):
    allv = sorted({v for f in faces for v in f})
    edges = {}
    if not allv:
        return edges
    cen = [sum(P[v][i] for v in allv) / len(allv) for i in range(3)]
    for f in faces:
        A, B, C = P[f[0]], P[f[1]], P[f[2]]
        u = [B[i] - A[i] for i in range(3)]
        w = [C[i] - A[i] for i in range(3)]
        n = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        fc = [sum(P[v][i] for v in f) / len(f) for i in range(3)]
        if sum(n[i] * (fc[i] - cen[i]) for i in range(3)) < 0:
            n = [-c for c in n]
        vis = sum(n[i] * view[i] for i in range(3)) > 1e-9
        for i in range(len(f)):
            key = tuple(sorted((f[i], f[(i + 1) % len(f)])))
            edges[key] = edges.get(key, False) or vis
    return edges


def fig3d(P, faces=(), hl=(), dhl=(), thin=(), polys=(), dots=(), lab=(), off=None,
          W=200, H=160, az=-30, el=20, pad=13, faces2=()):
    """P: 名前→座標。faces: 凸多面体の面（頂点名の列）。見えない辺は自動で破線。
    hl / dhl: 強調する線分（実線 / 破線）、thin: 細い補助線、polys: 塗る多角形、lab: ラベルを付ける点"""
    off = off or {}
    T, _ = _fit([_pj(v, az, el) for v in P.values()], W, H, pad)
    S = {k: T(_pj(v, az, el)) for k, v in P.items()}
    a, e = math.radians(az), math.radians(el)
    view = (-math.cos(e) * math.sin(a), -math.cos(e) * math.cos(a), math.sin(e))
    edges = _edges_vis(P, faces, view)
    out = [_poly([S[k] for k in pg], fill) for pg, fill in polys]
    for (p, q), vis in _edges_vis(P, faces2, view).items():
        out.append(_ln(S[p], S[q], "#888", 0.8, not vis))
    for (p, q), vis in edges.items():
        if not vis:
            out.append(_ln(S[p], S[q], _HID, 0.9, True))
    for (p, q), vis in edges.items():
        if vis:
            out.append(_ln(S[p], S[q]))
    for p, q in thin:
        out.append(_ln(S[p], S[q], _HID, 0.8))
    for p, q in dhl:
        out.append(_ln(S[p], S[q], _ACC, 1.2, True))
    for p, q in hl:
        out.append(_ln(S[p], S[q], _ACC, 1.5))
    for k in dots:
        out.append(_dot(S[k]))
    cx = sum(S[k][0] for k in S) / len(S)
    cy = sum(S[k][1] for k in S) / len(S)
    for k in lab:
        if k in off:
            dx, dy = off[k]
        else:
            vx, vy = S[k][0] - cx, S[k][1] - cy
            r = math.hypot(vx, vy) or 1
            dx, dy = 9 * vx / r, 9 * vy / r
        out.append(_tx(S[k], k.replace("'", "′"), dx, dy))
    return f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>"


def fig2d(items, box, W=200, H=150, pad=12):
    """平面の図。box=(x0,x1,y0,y1)（数学の座標）。items: ('l',p,q,col,dash) ('c',c,r) ('t',p,s,dx,dy) ('d',p) ('pg',[pts])"""
    x0, x1, y0, y1 = box
    T, s = _fit([(x0, y0), (x1, y1)], W, H, pad)
    out = []
    for it in items:
        k = it[0]
        if k == "pg":
            out.append(_poly([T(p) for p in it[1]], it[2] if len(it) > 2 else _FILL))
        elif k == "l":
            col = it[3] if len(it) > 3 else _INK
            dash = it[4] if len(it) > 4 else False
            w = it[5] if len(it) > 5 else 1.1
            out.append(_ln(T(it[1]), T(it[2]), col, w, dash))
        elif k == "c":
            c = T(it[1])
            out.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{it[2] * s:.1f}" fill="{it[3] if len(it) > 3 else "none"}" stroke="{_INK}" stroke-width="1.1"/>')
        elif k == "t":
            out.append(_tx(T(it[1]), it[2], it[3], it[4], it[5] if len(it) > 5 else 11))
        elif k == "d":
            out.append(_dot(T(it[1])))
    return f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>"


SEC = []

# ---------------------------------------------------------------- 節1
SEC.append({"title": "空間座標とベクトルの成分",
"base": r"""・2点 $\mathrm{A}(a_1,\ a_2,\ a_3)$，$\mathrm{B}(b_1,\ b_2,\ b_3)$ について　$\overrightarrow{\mathrm{AB}}=(b_1-a_1,\ b_2-a_2,\ b_3-a_3)$，$\mathrm{AB}=\sqrt{(b_1-a_1)^2+(b_2-a_2)^2+(b_3-a_3)^2}$<br>
・$\vec{a}=(a_1,\ a_2,\ a_3)$ の大きさは $|\vec{a}|=\sqrt{a_1^2+a_2^2+a_3^2}$。$\vec{a}$ と同じ向きの単位ベクトルは $\dfrac{\vec{a}}{|\vec{a}|}$<br>
・平行条件：$\vec{a}\neq\vec{0},\ \vec{b}\neq\vec{0}$ のとき　$\vec{a}\parallel\vec{b}\iff\vec{b}=k\vec{a}$ となる実数 $k$ がある<br>
・同じ平面上にない3つのベクトル $\vec{a},\ \vec{b},\ \vec{c}$ を用いると、任意のベクトル $\vec{p}$ は $\vec{p}=s\vec{a}+t\vec{b}+u\vec{c}$ の形にただ1通りに表される""",
"items": [
 {"lv": 1, "title": "対称な点の座標と等距離にある点",
  "q": r"点 $\mathrm{A}(2,\ -3,\ 4)$ について、次の点の座標を求めよ。<br>(1) $xy$ 平面に関して対称な点　(2) $y$ 軸に関して対称な点　(3) 原点に関して対称な点<br>(4) 2点 $\mathrm{A}$，$\mathrm{B}(0,\ 1,\ 2)$ から等距離にある $y$ 軸上の点",
  "hint": r"$xy$ 平面に関して対称 → $z$ 座標だけ符号が変わる。$y$ 軸に関して対称 → $y$ 座標はそのままで $x,\ z$ 座標の符号が変わる。(4) は $y$ 軸上の点を $\mathrm{P}(0,\ t,\ 0)$ とおき、$\mathrm{PA}^2=\mathrm{PB}^2$ をつくる（2乗すれば根号が消える）。",
  "sol": r"(1) $\boldsymbol{(2,\ -3,\ -4)}$　(2) $\boldsymbol{(-2,\ -3,\ -4)}$　(3) $\boldsymbol{(-2,\ 3,\ -4)}$<br>"
         r"(4) 求める点を $\mathrm{P}(0,\ t,\ 0)$ とする。$\mathrm{PA}=\mathrm{PB}$ より $\mathrm{PA}^2=\mathrm{PB}^2$ であるから<br>"
         r"$2^2+(t+3)^2+4^2=0^2+(t-1)^2+2^2$<br>"
         r"$t^2+6t+29=t^2-2t+5$　より　$8t=-24$，$t=-3$<br>よって　$\boldsymbol{\mathrm{P}(0,\ -3,\ 0)}$",
  "note": r"2点 A，B から等距離にある点全体は、線分 AB の中点を通り AB に垂直な平面（垂直二等分面）である。(4) はこの平面と $y$ 軸の交点を求めたことになる。",
  "ex": r"点 $\mathrm{P}(-3,\ 1,\ 2)$ について、(1) $zx$ 平面　(2) $x$ 軸　(3) 原点 に関して対称な点の座標を求めよ。また、(4) 2点 $\mathrm{P}$，$\mathrm{Q}(1,\ 2,\ 0)$ から等距離にある $z$ 軸上の点の座標を求めよ。",
  "exa": r"(1) $(-3,\ -1,\ 2)$　(2) $(-3,\ -1,\ -2)$　(3) $(3,\ -1,\ -2)$　(4) $\left(0,\ 0,\ \dfrac94\right)$"},
 {"lv": 1, "title": "成分による計算・単位ベクトル・平行条件",
  "q": r"$\vec{a}=(1,\ -2,\ 2)$，$\vec{b}=(3,\ 0,\ -4)$ とする。<br>(1) $2\vec{a}-\vec{b}$ を成分で表し、その大きさを求めよ。<br>(2) $\vec{a}$ と同じ向きの単位ベクトルを求めよ。<br>(3) $\vec{c}=(x,\ 4,\ y)$ が $\vec{a}$ に平行になるような $x,\ y$ の値を求めよ。",
  "hint": r"成分ごとに計算する。平行条件は $\vec{c}=k\vec{a}$ とおいて成分を比較し、値の分かっている成分からまず $k$ を決める。",
  "sol": r"(1) $2\vec{a}-\vec{b}=(2-3,\ -4-0,\ 4+4)=\boldsymbol{(-1,\ -4,\ 8)}$，$|2\vec{a}-\vec{b}|=\sqrt{1+16+64}=\boldsymbol{9}$<br>"
         r"(2) $|\vec{a}|=\sqrt{1+4+4}=3$ より　$\dfrac{\vec{a}}{|\vec{a}|}=\boldsymbol{\left(\dfrac13,\ -\dfrac23,\ \dfrac23\right)}$<br>"
         r"(3) $\vec{c}\neq\vec{0}$ であるから、$\vec{c}=k\vec{a}$ となる実数 $k$ がある。$(x,\ 4,\ y)=(k,\ -2k,\ 2k)$ より $4=-2k$，$k=-2$<br>よって　$\boldsymbol{x=-2,\ y=-4}$",
  "note": r"「$\vec{a}$ に平行な単位ベクトル」と問われたら、逆向きのもの $-\dfrac{\vec{a}}{|\vec{a}|}$ も含めて2つ答える。",
  "ex": r"$\vec{a}=(2,\ 2,\ 1)$，$\vec{b}=(4,\ 0,\ -1)$ とする。(1) $\vec{a}-2\vec{b}$ の成分と大きさ　(2) $\vec{a}$ と逆向きの単位ベクトル　(3) $\vec{c}=(x,\ -6,\ y)$ が $\vec{a}$ に平行になる $x,\ y$ の値 を求めよ。",
  "exa": r"(1) $(-6,\ 2,\ 3)$，大きさ $7$　(2) $\left(-\dfrac23,\ -\dfrac23,\ -\dfrac13\right)$　(3) $x=-6,\ y=-3$"},
 {"lv": 2, "title": "ベクトルを3つのベクトルで表す",
  "q": r"$\vec{a}=(1,\ 1,\ 0)$，$\vec{b}=(0,\ 1,\ 1)$，$\vec{c}=(1,\ 0,\ 1)$ のとき、$\vec{p}=(5,\ 1,\ 2)$ を $s\vec{a}+t\vec{b}+u\vec{c}$（$s,\ t,\ u$ は実数）の形で表せ。",
  "hint": r"右辺を成分で表して $\vec{p}$ と成分を比較すると、$s,\ t,\ u$ の連立1次方程式になる。この問題のように対称な形なら、3式を辺々加えると速い。",
  "sol": r"$s\vec{a}+t\vec{b}+u\vec{c}=(s+u,\ s+t,\ t+u)$ であるから、$\vec{p}$ と成分を比較して<br>"
         r"$s+u=5$ …①，$s+t=1$ …②，$t+u=2$ …③<br>"
         r"①＋②＋③ より $2(s+t+u)=8$，すなわち $s+t+u=4$。これと③，①，② から $s=2$，$t=-1$，$u=3$<br>"
         r"よって　$\boldsymbol{\vec{p}=2\vec{a}-\vec{b}+3\vec{c}}$",
  "note": r"$\vec{a},\ \vec{b},\ \vec{c}$ が同じ平面上にない（1次独立である）から、表し方はただ1通りである。3つのベクトルが同じ平面上にあると、連立方程式は解をもたないか、解が無数にある。",
  "ex": r"$\vec{a}=(1,\ 0,\ 1)$，$\vec{b}=(2,\ 1,\ 0)$，$\vec{c}=(0,\ 1,\ 1)$ のとき、$\vec{p}=(4,\ 0,\ 1)$ を $s\vec{a}+t\vec{b}+u\vec{c}$ の形で表せ。",
  "exa": r"$\vec{p}=2\vec{a}+\vec{b}-\vec{c}$"},
 {"lv": 2, "title": "ベクトルの大きさの最小値",
  "q": r"$\vec{a}=(2,\ 3,\ 1)$，$\vec{b}=(1,\ 1,\ 1)$ とする。実数 $t$ が変化するとき、$|\vec{a}+t\vec{b}|$ の最小値と、そのときの $t$ の値を求めよ。",
  "hint": r"$|\vec{a}+t\vec{b}|$ のままでは扱いにくいので、2乗して $t$ の2次関数とみて平方完成する。",
  "sol": r"$\vec{a}+t\vec{b}=(2+t,\ 3+t,\ 1+t)$ であるから<br>"
         r"$|\vec{a}+t\vec{b}|^2=(2+t)^2+(3+t)^2+(1+t)^2=3t^2+12t+14=3(t+2)^2+2$<br>"
         r"よって $|\vec{a}+t\vec{b}|^2$ は $t=-2$ のとき最小値 $2$ をとる。$|\vec{a}+t\vec{b}|\geqq0$ であるから、$|\vec{a}+t\vec{b}|$ は<br>"
         r"$\boldsymbol{t=-2}$ のとき最小値 $\boldsymbol{\sqrt2}$ をとる。",
  "note": r"$t=-2$ のとき $\vec{a}-2\vec{b}=(0,\ 1,\ -1)$ で、$(\vec{a}-2\vec{b})\cdot\vec{b}=0$ となる。O を始点とする $\vec{a}+t\vec{b}$ の終点は、$\vec{a}$ の終点を通り $\vec{b}$ に平行な直線上を動き、長さが最小になるのは $\vec{b}$ と垂直になるとき（本章「垂線の足と正射影」の節）。",
  "ex": r"$\vec{a}=(3,\ -1,\ 2)$，$\vec{b}=(1,\ -1,\ 0)$ のとき、$|\vec{a}+t\vec{b}|$ の最小値とそのときの実数 $t$ の値を求めよ。",
  "exa": r"$t=-2$ のとき最小値 $\sqrt6$"},
]})

# ---------------------------------------------------------------- 節2
def _tet_pts():
    r = 1 / math.sqrt(3)
    ang = {"A": 215, "B": 325, "C": 95}
    P = {k: (r * math.cos(math.radians(v)), r * math.sin(math.radians(v)), 0) for k, v in ang.items()}
    P["O"] = (0, 0, math.sqrt(2 / 3))
    return P


def _fig_tet_mn():
    P = _tet_pts()
    P["M"] = tuple((P["O"][i] + P["A"][i]) / 2 for i in range(3))
    P["N"] = tuple((P["B"][i] + P["C"][i]) / 2 for i in range(3))
    return fig3d(P, faces=["OAB", "OBC", "OCA", "ABC"], hl=[("M", "N")], dots=["M", "N"],
                 lab=["O", "A", "B", "C", "M", "N"], off={"M": (-8, -3), "N": (8, 5)}, W=170, H=150, az=-35, el=22)


SEC.append({"title": "空間ベクトルの内積",
"base": r"""・$\vec{a}$ と $\vec{b}$ のなす角を $\theta$（$0^\circ\leqq\theta\leqq180^\circ$）とすると　$\vec{a}\cdot\vec{b}=|\vec{a}||\vec{b}|\cos\theta=a_1b_1+a_2b_2+a_3b_3$<br>
・$\vec{a}\neq\vec{0},\ \vec{b}\neq\vec{0}$ のとき　$\vec{a}\perp\vec{b}\iff\vec{a}\cdot\vec{b}=0$<br>
・$\overrightarrow{\mathrm{AB}}=\vec{p},\ \overrightarrow{\mathrm{AC}}=\vec{q}$ のとき　$\triangle\mathrm{ABC}=\dfrac12\sqrt{|\vec{p}|^2|\vec{q}|^2-(\vec{p}\cdot\vec{q})^2}$<br>
・計算法則は平面と同じ：$|\vec{a}+\vec{b}|^2=|\vec{a}|^2+2\vec{a}\cdot\vec{b}+|\vec{b}|^2$，$-|\vec{a}||\vec{b}|\leqq\vec{a}\cdot\vec{b}\leqq|\vec{a}||\vec{b}|$""",
"items": [
 {"lv": 1, "title": "成分による内積となす角",
  "q": r"(1) $\vec{a}=(2,\ -1,\ 1)$，$\vec{b}=(1,\ 1,\ 2)$ のなす角 $\theta$ を求めよ。<br>(2) 3点 $\mathrm{A}(1,\ 2,\ 3)$，$\mathrm{B}(2,\ 1,\ 3)$，$\mathrm{C}(0,\ 2,\ 4)$ について、$\angle\mathrm{BAC}$ の大きさを求めよ。",
  "hint": r"$\cos\theta=\dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}||\vec{b}|}$ を使う。(2) の $\angle\mathrm{BAC}$ は $\overrightarrow{\mathrm{AB}}$ と $\overrightarrow{\mathrm{AC}}$ のなす角（始点を A にそろえる）。",
  "sol": r"(1) $\vec{a}\cdot\vec{b}=2-1+2=3$，$|\vec{a}|=\sqrt6$，$|\vec{b}|=\sqrt6$ より　$\cos\theta=\dfrac36=\dfrac12$<br>$0^\circ\leqq\theta\leqq180^\circ$ より　$\boldsymbol{\theta=60^\circ}$<br>"
         r"(2) $\overrightarrow{\mathrm{AB}}=(1,\ -1,\ 0)$，$\overrightarrow{\mathrm{AC}}=(-1,\ 0,\ 1)$ より　$\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}}=-1$，$|\overrightarrow{\mathrm{AB}}|=|\overrightarrow{\mathrm{AC}}|=\sqrt2$<br>"
         r"$\cos\angle\mathrm{BAC}=\dfrac{-1}{\sqrt2\cdot\sqrt2}=-\dfrac12$　よって　$\boldsymbol{\angle\mathrm{BAC}=120^\circ}$",
  "note": r"(2) で $\overrightarrow{\mathrm{BA}}$ と $\overrightarrow{\mathrm{AC}}$ のように始点がそろっていないベクトルの内積を使うと、補角の $60^\circ$ を答えてしまう。",
  "ex": r"(1) $\vec{a}=(1,\ -1,\ 0)$，$\vec{b}=(1,\ -2,\ 2)$ のなす角を求めよ。(2) 3点 $\mathrm{A}(0,\ 1,\ 2)$，$\mathrm{B}(1,\ 3,\ 4)$，$\mathrm{C}(-1,\ 1,\ 1)$ について $\angle\mathrm{BAC}$ を求めよ。",
  "exa": r"(1) $45^\circ$　(2) $135^\circ$"},
 {"lv": 2, "title": "2つのベクトルに垂直な単位ベクトル",
  "q": r"2つのベクトル $\vec{a}=(1,\ -2,\ 2)$，$\vec{b}=(2,\ -1,\ -2)$ の両方に垂直な単位ベクトルを求めよ。",
  "hint": r"求めるベクトルを $\vec{e}=(x,\ y,\ z)$ とおき、$\vec{e}\cdot\vec{a}=0$，$\vec{e}\cdot\vec{b}=0$，$|\vec{e}|=1$ の3式を連立する。まず前の2式から $x,\ y,\ z$ の比を出す。",
  "sol": r"$\vec{e}=(x,\ y,\ z)$ とおく。<br>$\vec{e}\cdot\vec{a}=0$ より $x-2y+2z=0$ …①，$\vec{e}\cdot\vec{b}=0$ より $2x-y-2z=0$ …②<br>"
         r"①＋② より $3x-3y=0$，$y=x$。①に代入して $z=\dfrac x2$。<br>"
         r"$|\vec{e}|=1$ より　$x^2+x^2+\dfrac{x^2}4=1$，$\dfrac94x^2=1$，$x=\pm\dfrac23$<br>"
         r"よって　$\boldsymbol{\vec{e}=\left(\dfrac23,\ \dfrac23,\ \dfrac13\right),\ \left(-\dfrac23,\ -\dfrac23,\ -\dfrac13\right)}$",
  "note": r"両方に垂直なベクトルは $(2,\ 2,\ 1)$ の実数倍に限られ、向きが2通りあるので答えも2つ。$\vec{a},\ \vec{b}$ に平行な平面の法線ベクトル（本章「直線と平面の方程式」の節）を求める計算と同じである。",
  "ex": r"2つのベクトル $\vec{a}=(1,\ 1,\ 0)$，$\vec{b}=(0,\ 1,\ 2)$ の両方に垂直で、大きさが $6$ のベクトルを求めよ。",
  "exa": r"$(4,\ -4,\ 2)$，$(-4,\ 4,\ -2)$"},
 {"lv": 2, "title": "空間の三角形の面積",
  "q": r"3点 $\mathrm{A}(1,\ 0,\ 0)$，$\mathrm{B}(0,\ 2,\ 0)$，$\mathrm{C}(0,\ 0,\ 3)$ を頂点とする $\triangle\mathrm{ABC}$ の面積 $S$ を求めよ。",
  "hint": r"$\overrightarrow{\mathrm{AB}}$，$\overrightarrow{\mathrm{AC}}$ の大きさと内積を求め、$S=\dfrac12\sqrt{|\overrightarrow{\mathrm{AB}}|^2|\overrightarrow{\mathrm{AC}}|^2-(\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}})^2}$ に代入する。この式は $S=\dfrac12\mathrm{AB}\cdot\mathrm{AC}\sin A$ と $\sin A=\sqrt{1-\cos^2A}$ から導かれる。",
  "sol": r"$\overrightarrow{\mathrm{AB}}=(-1,\ 2,\ 0)$，$\overrightarrow{\mathrm{AC}}=(-1,\ 0,\ 3)$ より<br>"
         r"$|\overrightarrow{\mathrm{AB}}|^2=5$，$|\overrightarrow{\mathrm{AC}}|^2=10$，$\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}}=1$<br>"
         r"よって　$S=\dfrac12\sqrt{5\cdot10-1^2}=\dfrac12\sqrt{49}=\boldsymbol{\dfrac72}$",
  "note": r"成分で $\overrightarrow{\mathrm{AB}}=(p_1,\ p_2,\ p_3)$，$\overrightarrow{\mathrm{AC}}=(q_1,\ q_2,\ q_3)$ とすると　$S=\dfrac12\sqrt{(p_2q_3-p_3q_2)^2+(p_3q_1-p_1q_3)^2+(p_1q_2-p_2q_1)^2}$<br>とも表せる。この問題では $\dfrac12\sqrt{6^2+3^2+2^2}=\dfrac72$。",
  "ex": r"3点 $\mathrm{A}(1,\ 1,\ 0)$，$\mathrm{B}(2,\ 3,\ 1)$，$\mathrm{C}(0,\ 2,\ 3)$ を頂点とする三角形の面積を求めよ。",
  "exa": r"$\dfrac{5\sqrt2}2$"},
 {"lv": 3, "title": "正四面体における内積（長さ・角・垂直）",
  "q": _fig_tet_mn() + r"1辺の長さが $1$ の正四面体 OABC において、辺 OA の中点を M，辺 BC の中点を N とし、$\overrightarrow{\mathrm{OA}}=\vec{a}$，$\overrightarrow{\mathrm{OB}}=\vec{b}$，$\overrightarrow{\mathrm{OC}}=\vec{c}$ とする。<br>(1) $\mathrm{OA}\perp\mathrm{BC}$ を示せ。<br>(2) 線分 MN の長さを求めよ。<br>(3) $\overrightarrow{\mathrm{MN}}$ と $\overrightarrow{\mathrm{OB}}$ のなす角 $\theta$ を求めよ。",
  "hint": r"各面は正三角形なので $|\vec{a}|=|\vec{b}|=|\vec{c}|=1$，$\vec{a}\cdot\vec{b}=\vec{b}\cdot\vec{c}=\vec{c}\cdot\vec{a}=1\cdot1\cdot\cos60^\circ=\dfrac12$。すべてのベクトルを $\vec{a},\ \vec{b},\ \vec{c}$ で表せば、長さも角も内積の計算に帰着する。",
  "sol": r"$|\vec{a}|=|\vec{b}|=|\vec{c}|=1$，$\vec{a}\cdot\vec{b}=\vec{b}\cdot\vec{c}=\vec{c}\cdot\vec{a}=\dfrac12$ である。<br>"
         r"(1) $\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{BC}}=\vec{a}\cdot(\vec{c}-\vec{b})=\vec{a}\cdot\vec{c}-\vec{a}\cdot\vec{b}=\dfrac12-\dfrac12=0$　よって $\mathrm{OA}\perp\mathrm{BC}$　$\blacksquare$<br>"
         r"(2) $\overrightarrow{\mathrm{MN}}=\dfrac{\vec{b}+\vec{c}}2-\dfrac{\vec{a}}2=\dfrac{-\vec{a}+\vec{b}+\vec{c}}2$ であり<br>"
         r"$|-\vec{a}+\vec{b}+\vec{c}|^2=|\vec{a}|^2+|\vec{b}|^2+|\vec{c}|^2-2\vec{a}\cdot\vec{b}+2\vec{b}\cdot\vec{c}-2\vec{c}\cdot\vec{a}=3-1+1-1=2$<br>"
         r"よって　$\boldsymbol{\mathrm{MN}=\dfrac{\sqrt2}2}$<br>"
         r"(3) $\overrightarrow{\mathrm{MN}}\cdot\overrightarrow{\mathrm{OB}}=\dfrac{-\vec{a}\cdot\vec{b}+|\vec{b}|^2+\vec{b}\cdot\vec{c}}2=\dfrac12\left(-\dfrac12+1+\dfrac12\right)=\dfrac12$<br>"
         r"$\cos\theta=\dfrac{\frac12}{\frac{\sqrt2}2\cdot1}=\dfrac1{\sqrt2}$　より　$\boldsymbol{\theta=45^\circ}$",
  "note": r"(1) と同様に $\mathrm{OB}\perp\mathrm{CA}$，$\mathrm{OC}\perp\mathrm{AB}$ も成り立つ（正四面体の向かい合う辺は垂直）。また $\overrightarrow{\mathrm{MN}}\cdot\vec{a}=0$，$\overrightarrow{\mathrm{MN}}\cdot\overrightarrow{\mathrm{BC}}=0$ となり、MN は OA と BC の両方に垂直である。",
  "ex": r"1辺の長さが $2$ の正四面体 OABC において、$\triangle\mathrm{ABC}$ の重心を G とする。(1) 線分 OG の長さ　(2) $\cos\angle\mathrm{AOG}$ を求めよ。",
  "exa": r"(1) $\dfrac{2\sqrt6}3$　(2) $\dfrac{\sqrt6}3$"},
 {"lv": 3, "title": "球面上の点と内積の最大・最小",
  "q": r"原点 O を中心とする半径 $1$ の球面上を点 P が動く。2点 $\mathrm{A}(1,\ 2,\ 4)$，$\mathrm{B}(1,\ 2,\ 0)$ に対して、$\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}$ の最大値と最小値、およびそのときの点 P の座標を求めよ。",
  "hint": r"$\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}$ を展開すると、P によって変化するのは $(\vec{a}+\vec{b})\cdot\vec{p}$ の部分だけ。$|\vec{p}|=1$ のもとでのその範囲は、なす角を考えればすぐ分かる。",
  "sol": r"$\vec{p}=\overrightarrow{\mathrm{OP}}$，$\vec{a}=\overrightarrow{\mathrm{OA}}$，$\vec{b}=\overrightarrow{\mathrm{OB}}$ とおくと　$|\vec{p}|=1$，$\vec{a}\cdot\vec{b}=1+4+0=5$，$\vec{a}+\vec{b}=(2,\ 4,\ 4)$，$|\vec{a}+\vec{b}|=6$<br>"
         r"$\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}=(\vec{a}-\vec{p})\cdot(\vec{b}-\vec{p})=\vec{a}\cdot\vec{b}-(\vec{a}+\vec{b})\cdot\vec{p}+|\vec{p}|^2=6-(\vec{a}+\vec{b})\cdot\vec{p}$<br>"
         r"$\vec{a}+\vec{b}$ と $\vec{p}$ のなす角を $\varphi$ とすると $(\vec{a}+\vec{b})\cdot\vec{p}=6\cos\varphi$ で、$-6\leqq6\cos\varphi\leqq6$。よって　$0\leqq\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}\leqq12$<br>"
         r"最大値 $\boldsymbol{12}$ をとるのは $\varphi=180^\circ$，すなわち $\vec{p}=-\dfrac{\vec{a}+\vec{b}}6$ のときで　$\boldsymbol{\mathrm{P}\left(-\dfrac13,\ -\dfrac23,\ -\dfrac23\right)}$<br>"
         r"最小値 $\boldsymbol{0}$ をとるのは $\varphi=0^\circ$，すなわち $\vec{p}=\dfrac{\vec{a}+\vec{b}}6$ のときで　$\boldsymbol{\mathrm{P}\left(\dfrac13,\ \dfrac23,\ \dfrac23\right)}$",
  "note": r"AB の中点 $\mathrm{M}(1,\ 2,\ 2)$ を使うと $\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}=\mathrm{PM}^2-\left(\dfrac{\mathrm{AB}}2\right)^2=\mathrm{PM}^2-4$ と変形できる。$\mathrm{OM}=3$ より $2\leqq\mathrm{PM}\leqq4$ で、同じ結果になる（最大・最小は直線 OM と球面の交点）。",
  "ex": r"原点を中心とする半径 $1$ の球面上を点 P が動くとき、2点 $\mathrm{A}(3,\ 1,\ 2)$，$\mathrm{B}(1,\ 1,\ 2)$ に対する $\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $15$，最小値 $3$"},
]})

# ---------------------------------------------------------------- 節3
def _fig_ppd():
    a, b, c = (2.0, 0, 0), (0.6, 1.4, 0), (0.2, 0.15, 1.3)
    add = lambda *vs: tuple(sum(v[i] for v in vs) for i in range(3))
    P = {"O": (0, 0, 0), "A": a, "B": b, "C": c, "D": add(a, b), "E": add(a, c), "F": add(b, c), "G": add(a, b, c)}
    P["P"] = tuple(P["G"][i] / 3 for i in range(3))
    P["Q"] = tuple(2 * P["G"][i] / 3 for i in range(3))
    return fig3d(P, faces=["OADB", "CEGF", "OAEC", "ADGE", "DBFG", "BOCF"],
                 polys=[("ABC", _FILL), ("DEF", "#f3dccf")], thin=[("A", "B"), ("B", "C"), ("C", "A"), ("D", "E"), ("E", "F"), ("F", "D")],
                 hl=[("O", "G")], dots=["P", "Q"], lab=["O", "A", "B", "C", "D", "E", "F", "G", "P", "Q"],
                 off={"P": (-9, 5), "Q": (8, -4)}, W=200, H=150, az=10, el=25)


def _fig_tet_lmn():
    P = {"O": (-0.2, 0.0, 1.3), "A": (-0.8, -0.5, 0), "B": (0.7, -0.5, 0), "C": (0.5, 0.7, 0)}
    lin = lambda p, q, t: tuple(P[p][i] + t * (P[q][i] - P[p][i]) for i in range(3))
    P["L"], P["M"], P["N"] = lin("O", "A", 1 / 2), lin("O", "B", 2 / 3), lin("O", "C", 1 / 3)
    P["G"] = tuple((P["A"][i] + P["B"][i] + P["C"][i]) / 3 for i in range(3))
    P["P"] = lin("O", "G", 6 / 13)
    return fig3d(P, faces=["OAB", "OBC", "OCA", "ABC"], polys=[("LMN", _FILL)],
                 thin=[("L", "M"), ("M", "N"), ("N", "L")], hl=[("O", "G")], dots=["L", "M", "N", "G", "P"],
                 lab=["O", "A", "B", "C", "L", "M", "N", "G", "P"], off={"G": (2, 9), "P": (-6, -5), "M": (9, 3)},
                 W=170, H=150, az=-15, el=22)


SEC.append({"title": "位置ベクトルと一直線上・同一平面上の点",
"base": r"""・2点 $\mathrm{A}(\vec{a}),\ \mathrm{B}(\vec{b})$ を結ぶ線分を $m:n$ に内分する点は $\dfrac{n\vec{a}+m\vec{b}}{m+n}$，外分する点は $\dfrac{-n\vec{a}+m\vec{b}}{m-n}$<br>
・$\triangle\mathrm{ABC}$ の重心は $\dfrac{\vec{a}+\vec{b}+\vec{c}}3$，四面体 ABCD の重心は $\dfrac{\vec{a}+\vec{b}+\vec{c}+\vec{d}}4$<br>
・3点 A，B，C が一直線上にある $\iff$ $\overrightarrow{\mathrm{AC}}=k\overrightarrow{\mathrm{AB}}$ となる実数 $k$ がある<br>
・点 P が平面 ABC 上にある $\iff$ $\overrightarrow{\mathrm{AP}}=s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$ $\iff$ $\overrightarrow{\mathrm{OP}}=\alpha\overrightarrow{\mathrm{OA}}+\beta\overrightarrow{\mathrm{OB}}+\gamma\overrightarrow{\mathrm{OC}}$，$\alpha+\beta+\gamma=1$<br>
・$\vec{a},\ \vec{b},\ \vec{c}$ が同じ平面上にないとき、それらによる表し方はただ1通り（係数を比較してよい）""",
"items": [
 {"lv": 1, "title": "分点と重心の座標",
  "q": r"2点 $\mathrm{A}(1,\ -2,\ 3)$，$\mathrm{B}(4,\ 1,\ -3)$ について、(1) 線分 AB を $2:1$ に内分する点 P　(2) 線分 AB を $2:1$ に外分する点 Q　の座標を求めよ。<br>(3) 点 $\mathrm{C}(-2,\ 4,\ 3)$ に対し、$\triangle\mathrm{ABC}$ の重心 G の座標を求めよ。",
  "hint": r"平面のときと同じ公式を、$x,\ y,\ z$ の各座標に用いる。外分は「$m:n$ の $n$ を $-n$ にした内分」と考える。",
  "sol": r"(1) $\left(\dfrac{1\cdot1+2\cdot4}3,\ \dfrac{1\cdot(-2)+2\cdot1}3,\ \dfrac{1\cdot3+2\cdot(-3)}3\right)=\boldsymbol{(3,\ 0,\ -1)}$<br>"
         r"(2) $\left(\dfrac{-1\cdot1+2\cdot4}{2-1},\ \dfrac{-1\cdot(-2)+2\cdot1}{2-1},\ \dfrac{-1\cdot3+2\cdot(-3)}{2-1}\right)=\boldsymbol{(7,\ 4,\ -9)}$<br>"
         r"(3) $\left(\dfrac{1+4-2}3,\ \dfrac{-2+1+4}3,\ \dfrac{3-3+3}3\right)=\boldsymbol{(1,\ 1,\ 1)}$",
  "note": r"$2:1$ に外分する点 Q は、B が線分 AQ の中点になる位置にある。実際、A と Q の中点は $(4,\ 1,\ -3)$ で B に一致し、検算になる。",
  "ex": r"2点 $\mathrm{A}(2,\ 0,\ -1)$，$\mathrm{B}(-1,\ 3,\ 5)$ について、線分 AB を (1) $1:2$ に内分する点　(2) $1:2$ に外分する点 の座標を求めよ。(3) $\mathrm{C}(3,\ 1,\ 0)$，$\mathrm{D}(0,\ -4,\ 4)$ に対し、四面体 ABCD の重心の座標を求めよ。",
  "exa": r"(1) $(1,\ 1,\ 1)$　(2) $(5,\ -3,\ -7)$　(3) $(1,\ 0,\ 2)$"},
 {"lv": 1, "title": "3点が一直線上にある条件",
  "q": r"3点 $\mathrm{A}(1,\ 2,\ -1)$，$\mathrm{B}(3,\ -1,\ 1)$，$\mathrm{C}(x,\ y,\ 5)$ が一直線上にあるとき、$x,\ y$ の値を求めよ。また、このとき点 C は線分 AB をどのような比に分ける点か。",
  "hint": r"$\overrightarrow{\mathrm{AC}}=k\overrightarrow{\mathrm{AB}}$ とおいて成分を比較する。値の分かっている $z$ 成分から $k$ が決まる。",
  "sol": r"3点が一直線上にあるから、$\overrightarrow{\mathrm{AC}}=k\overrightarrow{\mathrm{AB}}$ となる実数 $k$ がある。<br>"
         r"$\overrightarrow{\mathrm{AB}}=(2,\ -3,\ 2)$，$\overrightarrow{\mathrm{AC}}=(x-1,\ y-2,\ 6)$ より　$x-1=2k$，$y-2=-3k$，$6=2k$<br>"
         r"よって $k=3$ で　$\boldsymbol{x=7,\ y=-7}$<br>"
         r"$\overrightarrow{\mathrm{AC}}=3\overrightarrow{\mathrm{AB}}$ より、C は線分 AB の B を越えた延長上にあり、$\mathrm{AC}:\mathrm{CB}=3:2$。よって C は線分 AB を $\boldsymbol{3:2}$ に外分する点である。",
  "note": r"成分の比が等しいとして $\dfrac{x-1}2=\dfrac{y-2}{-3}=\dfrac62$ と書いてもよいが、成分に $0$ があると分数の形が使えないので、$k$ を用いる方が安全である。",
  "ex": r"3点 $\mathrm{A}(2,\ -1,\ 3)$，$\mathrm{B}(0,\ 1,\ 4)$，$\mathrm{C}(x,\ -3,\ y)$ が一直線上にあるとき、$x,\ y$ の値を求めよ。また、C は線分 AB をどのような比に分ける点か。",
  "exa": r"$x=4,\ y=2$；C は線分 AB を $1:2$ に外分する点"},
 {"lv": 2, "title": "4点が同じ平面上にある条件",
  "q": r"4点 $\mathrm{A}(1,\ 1,\ 0)$，$\mathrm{B}(2,\ 0,\ 1)$，$\mathrm{C}(0,\ 1,\ 2)$，$\mathrm{D}(x,\ 0,\ 3)$ が同じ平面上にあるとき、$x$ の値を求めよ。",
  "hint": r"A，B，C は一直線上にないので平面 ABC が定まる。D がその上にある条件は $\overrightarrow{\mathrm{AD}}=s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$ となる実数 $s,\ t$ が存在すること。未知数 $x,\ s,\ t$ の3つに対して式も3つある。",
  "sol": r"$\overrightarrow{\mathrm{AB}}=(1,\ -1,\ 1)$，$\overrightarrow{\mathrm{AC}}=(-1,\ 0,\ 2)$ は平行でないから、3点 A，B，C は一直線上になく、平面 ABC が定まる。<br>"
         r"D が平面 ABC 上にあるための条件は、$\overrightarrow{\mathrm{AD}}=s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$ となる実数 $s,\ t$ が存在することである。<br>"
         r"$(x-1,\ -1,\ 3)=(s-t,\ -s,\ s+2t)$ より　$x-1=s-t$ …①，$-1=-s$ …②，$3=s+2t$ …③<br>"
         r"②より $s=1$，③より $t=1$，①より $x-1=0$　よって　$\boldsymbol{x=1}$",
  "note": r"本章「直線と平面の方程式」の節の方法なら、平面 ABC の方程式 $2x+3y+z-5=0$ を求め、D の座標を代入して $2x+3-5=0$ としてもよい。",
  "ex": r"4点 $\mathrm{A}(0,\ 1,\ 2)$，$\mathrm{B}(1,\ 2,\ 0)$，$\mathrm{C}(2,\ 0,\ 1)$，$\mathrm{D}(x,\ 2,\ 2)$ が同じ平面上にあるとき、$x$ の値を求めよ。",
  "exa": r"$x=-1$"},
 {"lv": 3, "title": "平行六面体の対角線と平面の交点",
  "q": _fig_ppd() + r"平行六面体 OADB-CEGF において、$\overrightarrow{\mathrm{OA}}=\vec{a}$，$\overrightarrow{\mathrm{OB}}=\vec{b}$，$\overrightarrow{\mathrm{OC}}=\vec{c}$ とする（$\overrightarrow{\mathrm{OD}}=\vec{a}+\vec{b}$，$\overrightarrow{\mathrm{OE}}=\vec{a}+\vec{c}$，$\overrightarrow{\mathrm{OF}}=\vec{b}+\vec{c}$，$\overrightarrow{\mathrm{OG}}=\vec{a}+\vec{b}+\vec{c}$）。対角線 OG と平面 ABC の交点を P，平面 DEF の交点を Q とする。<br>(1) $\overrightarrow{\mathrm{OP}}$ を $\vec{a},\ \vec{b},\ \vec{c}$ で表せ。<br>(2) 2点 P，Q は対角線 OG を3等分することを示せ。",
  "hint": r"P は直線 OG 上にあるので $\overrightarrow{\mathrm{OP}}=k\overrightarrow{\mathrm{OG}}$ とおける。これを $\overrightarrow{\mathrm{OA}},\ \overrightarrow{\mathrm{OB}},\ \overrightarrow{\mathrm{OC}}$ で表したとき、P が平面 ABC 上にある条件は「係数の和が $1$」。Q についても $\overrightarrow{\mathrm{OD}},\ \overrightarrow{\mathrm{OE}},\ \overrightarrow{\mathrm{OF}}$ で表す。",
  "sol": r"(1) P は直線 OG 上にあるから、$\overrightarrow{\mathrm{OP}}=k\overrightarrow{\mathrm{OG}}=k\vec{a}+k\vec{b}+k\vec{c}$（$k$ は実数）とおける。<br>"
         r"P は平面 ABC 上にあり、$\vec{a},\ \vec{b},\ \vec{c}$ は同じ平面上にないから、係数の和について $k+k+k=1$，$k=\dfrac13$<br>"
         r"よって　$\boldsymbol{\overrightarrow{\mathrm{OP}}=\dfrac13(\vec{a}+\vec{b}+\vec{c})}$<br>"
         r"(2) 同様に $\overrightarrow{\mathrm{OQ}}=l\overrightarrow{\mathrm{OG}}$ とおくと<br>"
         r"$\overrightarrow{\mathrm{OQ}}=\dfrac l2\{(\vec{a}+\vec{b})+(\vec{a}+\vec{c})+(\vec{b}+\vec{c})\}=\dfrac l2\overrightarrow{\mathrm{OD}}+\dfrac l2\overrightarrow{\mathrm{OE}}+\dfrac l2\overrightarrow{\mathrm{OF}}$<br>"
         r"$\overrightarrow{\mathrm{OD}},\ \overrightarrow{\mathrm{OE}},\ \overrightarrow{\mathrm{OF}}$ も同じ平面上にない（$\vec{a},\ \vec{b},\ \vec{c}$ を逆に表せる）から、Q が平面 DEF 上にある条件は $\dfrac{3l}2=1$，$l=\dfrac23$。<br>"
         r"よって $\overrightarrow{\mathrm{OP}}=\dfrac13\overrightarrow{\mathrm{OG}}$，$\overrightarrow{\mathrm{OQ}}=\dfrac23\overrightarrow{\mathrm{OG}}$ であり、$\mathrm{OP}=\mathrm{PQ}=\mathrm{QG}$。すなわち P，Q は対角線 OG を3等分する。　$\blacksquare$",
  "note": r"(1) から P は $\triangle\mathrm{ABC}$ の重心、同様に Q は $\triangle\mathrm{DEF}$ の重心でもある。立方体の場合は、対角線 OG は2つの正三角形 ABC，DEF に垂直に交わる。",
  "ex": r"平行六面体 OADB-CEGF において、辺 OA，OB，OC の中点をそれぞれ L，M，N とする。対角線 OG と平面 LMN の交点を R とするとき、$\mathrm{OR}:\mathrm{RG}$ を求めよ。",
  "exa": r"$1:5$"},
 {"lv": 3, "title": "四面体の辺上の3点を通る平面と直線の交点",
  "q": _fig_tet_lmn() + r"四面体 OABC において、辺 OA の中点を L，辺 OB を $2:1$ に内分する点を M，辺 OC を $1:2$ に内分する点を N とし、$\triangle\mathrm{ABC}$ の重心を G とする。直線 OG と平面 LMN の交点を P とするとき、$\overrightarrow{\mathrm{OP}}$ を $\vec{a}=\overrightarrow{\mathrm{OA}},\ \vec{b}=\overrightarrow{\mathrm{OB}},\ \vec{c}=\overrightarrow{\mathrm{OC}}$ で表し、$\mathrm{OP}:\mathrm{PG}$ を求めよ。",
  "hint": r"$\overrightarrow{\mathrm{OP}}=k\overrightarrow{\mathrm{OG}}$ とおき、$\vec{a}=2\overrightarrow{\mathrm{OL}}$ のように書き直して $\overrightarrow{\mathrm{OL}},\ \overrightarrow{\mathrm{OM}},\ \overrightarrow{\mathrm{ON}}$ で表す。平面 LMN 上にある条件は係数の和が $1$。",
  "sol": r"$\overrightarrow{\mathrm{OL}}=\dfrac12\vec{a}$，$\overrightarrow{\mathrm{OM}}=\dfrac23\vec{b}$，$\overrightarrow{\mathrm{ON}}=\dfrac13\vec{c}$ より　$\vec{a}=2\overrightarrow{\mathrm{OL}}$，$\vec{b}=\dfrac32\overrightarrow{\mathrm{OM}}$，$\vec{c}=3\overrightarrow{\mathrm{ON}}$<br>"
         r"P は直線 OG 上にあるから、$\overrightarrow{\mathrm{OP}}=k\overrightarrow{\mathrm{OG}}=\dfrac k3(\vec{a}+\vec{b}+\vec{c})$（$k$ は実数）とおけて<br>"
         r"$\overrightarrow{\mathrm{OP}}=\dfrac{2k}3\overrightarrow{\mathrm{OL}}+\dfrac k2\overrightarrow{\mathrm{OM}}+k\overrightarrow{\mathrm{ON}}$<br>"
         r"P は平面 LMN 上にあり、$\overrightarrow{\mathrm{OL}},\ \overrightarrow{\mathrm{OM}},\ \overrightarrow{\mathrm{ON}}$ は同じ平面上にないから、係数の和が $1$：$\dfrac{2k}3+\dfrac k2+k=\dfrac{13k}6=1$，$k=\dfrac6{13}$<br>"
         r"よって　$\boldsymbol{\overrightarrow{\mathrm{OP}}=\dfrac2{13}(\vec{a}+\vec{b}+\vec{c})}$。また $\overrightarrow{\mathrm{OP}}=\dfrac6{13}\overrightarrow{\mathrm{OG}}$ より　$\boldsymbol{\mathrm{OP}:\mathrm{PG}=6:7}$",
  "note": r"別解：P は平面 LMN 上にあるので $\overrightarrow{\mathrm{OP}}=\overrightarrow{\mathrm{OL}}+s\overrightarrow{\mathrm{LM}}+t\overrightarrow{\mathrm{LN}}$ とおき、$k\overrightarrow{\mathrm{OG}}$ と $\vec{a},\ \vec{b},\ \vec{c}$ の係数を比較してもよい（未知数3つ・式3つ）。一般に $\mathrm{OL}=l\,\mathrm{OA}$，$\mathrm{OM}=m\,\mathrm{OB}$，$\mathrm{ON}=n\,\mathrm{OC}$ のとき　$\dfrac{\mathrm{OP}}{\mathrm{OG}}=\dfrac3{\frac1l+\frac1m+\frac1n}$。",
  "ex": r"四面体 OABC において、辺 OA を $1:2$ に内分する点を L，辺 OB の中点を M，辺 OC を $3:1$ に内分する点を N，$\triangle\mathrm{ABC}$ の重心を G とする。直線 OG と平面 LMN の交点を P とするとき、$\overrightarrow{\mathrm{OP}}$ を $\vec{a},\ \vec{b},\ \vec{c}$ で表し、$\mathrm{OP}:\mathrm{PG}$ を求めよ。",
  "exa": r"$\overrightarrow{\mathrm{OP}}=\dfrac3{19}(\vec{a}+\vec{b}+\vec{c})$，$\mathrm{OP}:\mathrm{PG}=9:10$"},
]})

# ---------------------------------------------------------------- 節4
def _fig_right_tet():
    p, q, r = 1.25, 1.6, 1.25
    P = {"O": (0, 0, 0), "A": (p, 0, 0), "B": (0, q, 0), "C": (0, 0, r)}
    n = (1 / p, 1 / q, 1 / r)
    nn = sum(c * c for c in n)
    P["H"] = tuple(c / nn for c in n)
    B, C, A = P["B"], P["C"], P["A"]
    d = [C[i] - B[i] for i in range(3)]
    lam = sum((A[i] - B[i]) * d[i] for i in range(3)) / sum(c * c for c in d)
    P["K"] = tuple(B[i] + lam * d[i] for i in range(3))
    return fig3d(P, faces=["OAB", "OBC", "OCA", "ABC"], dhl=[("O", "H")], thin=[("A", "K")], dots=["H", "K"],
                 lab=["O", "A", "B", "C", "H"], off={"H": (-9, -2), "O": (3, 10)}, W=160, H=140, az=-150, el=25)


SEC.append({"title": "垂線の足と正射影",
"base": r"""・点 P から直線 $\vec{p}=\vec{a}+t\vec{u}$ に下ろした垂線の足 H：$\overrightarrow{\mathrm{OH}}=\vec{a}+t\vec{u}$ とおき、$\overrightarrow{\mathrm{PH}}\cdot\vec{u}=0$ から $t$ を決める<br>
・点 P から平面 ABC に下ろした垂線の足 H：$\overrightarrow{\mathrm{AH}}=s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$ とおき、$\overrightarrow{\mathrm{PH}}\cdot\overrightarrow{\mathrm{AB}}=0$，$\overrightarrow{\mathrm{PH}}\cdot\overrightarrow{\mathrm{AC}}=0$ から $s,\ t$ を決める（直線が平面に垂直 $\iff$ 平面上の平行でない2つのベクトルに垂直）<br>
・$\vec{b}$ の $\vec{a}$ 方向への正射影ベクトルは $\dfrac{\vec{a}\cdot\vec{b}}{|\vec{a}|^2}\vec{a}$<br>
・ねじれの位置にある2直線上の点 P，Q の距離 PQ が最小 $\iff$ PQ が2直線の両方に垂直（共通垂線）""",
"items": [
 {"lv": 2, "title": "点から直線に下ろした垂線の足",
  "q": r"2点 $\mathrm{A}(1,\ 0,\ 2)$，$\mathrm{B}(3,\ 1,\ 0)$ を通る直線を $\ell$ とする。点 $\mathrm{P}(6,\ 4,\ 0)$ から $\ell$ に下ろした垂線の足 H の座標と、点 P と直線 $\ell$ の距離を求めよ。",
  "hint": r"H は直線 AB 上にあるので $\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OA}}+t\overrightarrow{\mathrm{AB}}$ と表せる。$\overrightarrow{\mathrm{PH}}\perp\overrightarrow{\mathrm{AB}}$ から $t$ を決める。",
  "sol": r"$\overrightarrow{\mathrm{AB}}=(2,\ 1,\ -2)$。H は $\ell$ 上にあるから、実数 $t$ を用いて<br>"
         r"$\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OA}}+t\overrightarrow{\mathrm{AB}}=(1+2t,\ t,\ 2-2t)$，$\overrightarrow{\mathrm{PH}}=(2t-5,\ t-4,\ 2-2t)$<br>"
         r"$\overrightarrow{\mathrm{PH}}\cdot\overrightarrow{\mathrm{AB}}=0$ より　$2(2t-5)+(t-4)-2(2-2t)=9t-18=0$，$t=2$<br>"
         r"よって　$\boldsymbol{\mathrm{H}(5,\ 2,\ -2)}$。$\overrightarrow{\mathrm{PH}}=(-1,\ -2,\ -2)$ より、求める距離は　$\mathrm{PH}=\sqrt{1+4+4}=\boldsymbol{3}$",
  "note": r"$\mathrm{PH}^2=(2t-5)^2+(t-4)^2+(2-2t)^2=9t^2-36t+45=9(t-2)^2+9$ の最小値を求めても同じ結果になる（最小となる $t$ で $\overrightarrow{\mathrm{PH}}\perp\overrightarrow{\mathrm{AB}}$ となる）。",
  "ex": r"2点 $\mathrm{A}(0,\ 1,\ 1)$，$\mathrm{B}(1,\ 3,\ -1)$ を通る直線に、点 $\mathrm{P}(1,\ 0,\ 5)$ から下ろした垂線の足 H の座標と、P と直線の距離を求めよ。",
  "exa": r"$\mathrm{H}(-1,\ -1,\ 3)$，距離 $3$"},
 {"lv": 3, "title": "原点から平面に下ろした垂線の足",
  "q": r"3点 $\mathrm{A}(1,\ 0,\ 0)$，$\mathrm{B}(0,\ 2,\ 0)$，$\mathrm{C}(0,\ 0,\ 2)$ の定める平面に、原点 O から垂線 OH を下ろす。<br>(1) 点 H の座標を求めよ。　(2) 線分 OH の長さを用いて、$\triangle\mathrm{ABC}$ の面積を求めよ。",
  "hint": r"H は平面 ABC 上の点なので $\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OA}}+s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$。OH が平面に垂直 $\iff$ $\overrightarrow{\mathrm{AB}},\ \overrightarrow{\mathrm{AC}}$ の両方に垂直。(2) は四面体 OABC の体積を2通りに表す。",
  "sol": r"(1) $\overrightarrow{\mathrm{AB}}=(-1,\ 2,\ 0)$，$\overrightarrow{\mathrm{AC}}=(-1,\ 0,\ 2)$。H は平面 ABC 上にあるから<br>"
         r"$\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OA}}+s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}=(1-s-t,\ 2s,\ 2t)$<br>"
         r"$\overrightarrow{\mathrm{OH}}\cdot\overrightarrow{\mathrm{AB}}=0$ より $-(1-s-t)+4s=0$，すなわち $5s+t=1$<br>"
         r"$\overrightarrow{\mathrm{OH}}\cdot\overrightarrow{\mathrm{AC}}=0$ より $-(1-s-t)+4t=0$，すなわち $s+5t=1$<br>"
         r"これを解いて $s=t=\dfrac16$。よって　$\boldsymbol{\mathrm{H}\left(\dfrac23,\ \dfrac13,\ \dfrac13\right)}$<br>"
         r"(2) $\mathrm{OH}=\sqrt{\dfrac49+\dfrac19+\dfrac19}=\dfrac{\sqrt6}3$。四面体 OABC の体積 $V$ は、$\triangle\mathrm{OAB}$ を底面、OC を高さとみて　$V=\dfrac13\cdot\left(\dfrac12\cdot1\cdot2\right)\cdot2=\dfrac23$<br>"
         r"$\triangle\mathrm{ABC}$ を底面とみると $V=\dfrac13\cdot\triangle\mathrm{ABC}\cdot\mathrm{OH}$ であるから　$\triangle\mathrm{ABC}=\dfrac{3V}{\mathrm{OH}}=\dfrac2{\frac{\sqrt6}3}=\boldsymbol{\sqrt6}$",
  "note": r"(2) は三角形の面積の公式 $\dfrac12\sqrt{|\overrightarrow{\mathrm{AB}}|^2|\overrightarrow{\mathrm{AC}}|^2-(\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}})^2}=\dfrac12\sqrt{25-1}=\sqrt6$ で確かめられる。次の節の平面の方程式を使えば、平面 ABC は $2x+y+z=2$ で、H は法線ベクトル $(2,\ 1,\ 1)$ の実数倍としてすぐに求まる。",
  "ex": r"3点 $\mathrm{A}(4,\ 0,\ 0)$，$\mathrm{B}(0,\ 2,\ 0)$，$\mathrm{C}(0,\ 0,\ 4)$ の定める平面に原点 O から垂線 OH を下ろす。H の座標と $\triangle\mathrm{ABC}$ の面積を求めよ。",
  "exa": r"$\mathrm{H}\left(\dfrac23,\ \dfrac43,\ \dfrac23\right)$，面積 $4\sqrt6$"},
 {"lv": 3, "title": "内積で与えられた四面体の高さと体積",
  "q": r"四面体 OABC において $\mathrm{OA}=\mathrm{OB}=1$，$\mathrm{OC}=2$，$\angle\mathrm{AOB}=90^\circ$，$\angle\mathrm{BOC}=\angle\mathrm{COA}=60^\circ$ とし、$\vec{a}=\overrightarrow{\mathrm{OA}},\ \vec{b}=\overrightarrow{\mathrm{OB}},\ \vec{c}=\overrightarrow{\mathrm{OC}}$ とする。頂点 C から平面 OAB に垂線 CH を下ろす。<br>(1) $\overrightarrow{\mathrm{OH}}$ を $\vec{a},\ \vec{b}$ で表せ。　(2) 四面体 OABC の体積 $V$ を求めよ。",
  "hint": r"成分は与えられていないが、内積 $\vec{a}\cdot\vec{b}$ などはすべて分かる。$\overrightarrow{\mathrm{OH}}=s\vec{a}+t\vec{b}$ とおけば、$\overrightarrow{\mathrm{CH}}\cdot\vec{a}=0$，$\overrightarrow{\mathrm{CH}}\cdot\vec{b}=0$ は内積の計算だけで処理できる。",
  "sol": r"$|\vec{a}|=|\vec{b}|=1$，$|\vec{c}|=2$，$\vec{a}\cdot\vec{b}=0$，$\vec{b}\cdot\vec{c}=\vec{c}\cdot\vec{a}=1\cdot2\cdot\cos60^\circ=1$<br>"
         r"(1) H は平面 OAB 上にあるから $\overrightarrow{\mathrm{OH}}=s\vec{a}+t\vec{b}$ とおける。$\overrightarrow{\mathrm{CH}}=s\vec{a}+t\vec{b}-\vec{c}$ で<br>"
         r"$\overrightarrow{\mathrm{CH}}\cdot\vec{a}=s|\vec{a}|^2+t\vec{a}\cdot\vec{b}-\vec{c}\cdot\vec{a}=s-1=0$，$\overrightarrow{\mathrm{CH}}\cdot\vec{b}=s\vec{a}\cdot\vec{b}+t|\vec{b}|^2-\vec{b}\cdot\vec{c}=t-1=0$<br>"
         r"よって $s=t=1$ で　$\boldsymbol{\overrightarrow{\mathrm{OH}}=\vec{a}+\vec{b}}$<br>"
         r"(2) $|\overrightarrow{\mathrm{CH}}|^2=|\vec{a}+\vec{b}-\vec{c}|^2=|\vec{a}|^2+|\vec{b}|^2+|\vec{c}|^2+2\vec{a}\cdot\vec{b}-2\vec{b}\cdot\vec{c}-2\vec{c}\cdot\vec{a}=1+1+4+0-2-2=2$<br>"
         r"よって $\mathrm{CH}=\sqrt2$。$\triangle\mathrm{OAB}=\dfrac12\cdot1\cdot1=\dfrac12$ より　$V=\dfrac13\cdot\dfrac12\cdot\sqrt2=\boldsymbol{\dfrac{\sqrt2}6}$",
  "note": r"$\overrightarrow{\mathrm{OH}}=\vec{a}+\vec{b}$ より、H は正方形 OAHB の頂点の位置にあり、$\triangle\mathrm{OAB}$ の外部にある。垂線の足が底面の三角形の内部にあるとは限らないので、図からの思い込みは禁物。",
  "ex": r"四面体 OABC において $\mathrm{OA}=\mathrm{OB}=\mathrm{OC}=2$，$\angle\mathrm{AOB}=90^\circ$，$\angle\mathrm{BOC}=\angle\mathrm{COA}=60^\circ$ とする。C から平面 OAB に下ろした垂線の足を H とするとき、$\overrightarrow{\mathrm{OH}}$ を $\vec{a}=\overrightarrow{\mathrm{OA}},\ \vec{b}=\overrightarrow{\mathrm{OB}}$ で表し、四面体 OABC の体積を求めよ。",
  "exa": r"$\overrightarrow{\mathrm{OH}}=\dfrac12\vec{a}+\dfrac12\vec{b}$，体積 $\dfrac{2\sqrt2}3$"},
 {"lv": 3, "title": "ねじれの位置にある2直線の距離（共通垂線）",
  "q": r"2直線 $\ell:\ (x,\ y,\ z)=(-1,\ -2,\ 0)+s(1,\ 1,\ 0)$，$m:\ (x,\ y,\ z)=(2,\ -3,\ -1)+t(0,\ 1,\ 1)$ がある（$s,\ t$ は実数）。$\ell$ 上の点 P と $m$ 上の点 Q の距離 PQ の最小値と、そのときの P，Q の座標を求めよ。",
  "hint": r"PQ が最小になるのは、PQ が $\ell,\ m$ の両方に垂直なとき（共通垂線）。$\overrightarrow{\mathrm{PQ}}\cdot\vec{u}=0$，$\overrightarrow{\mathrm{PQ}}\cdot\vec{v}=0$ から $s,\ t$ を求め、それで最小になることは $\mathrm{PQ}^2$ を分解して確かめる。",
  "sol": r"$\vec{u}=(1,\ 1,\ 0)$，$\vec{v}=(0,\ 1,\ 1)$ とする。$\mathrm{P}(-1+s,\ -2+s,\ 0)$，$\mathrm{Q}(2,\ -3+t,\ -1+t)$ とおくと<br>"
         r"$\overrightarrow{\mathrm{PQ}}=(3-s,\ -1-s+t,\ -1+t)$<br>"
         r"$\overrightarrow{\mathrm{PQ}}\cdot\vec{u}=(3-s)+(-1-s+t)=2-2s+t$，$\overrightarrow{\mathrm{PQ}}\cdot\vec{v}=(-1-s+t)+(-1+t)=-2-s+2t$<br>"
         r"これらを $0$ とすると $s=2$，$t=2$ で、このときの点を $\mathrm{P_0}(1,\ 0,\ 0)$，$\mathrm{Q_0}(2,\ -1,\ 1)$ とすると $\overrightarrow{\mathrm{P_0Q_0}}=(1,\ -1,\ 1)$。<br>"
         r"一般の P，Q については $\overrightarrow{\mathrm{PQ}}=\overrightarrow{\mathrm{P_0Q_0}}+(t-2)\vec{v}-(s-2)\vec{u}$ で、$\overrightarrow{\mathrm{P_0Q_0}}$ は $\vec{u},\ \vec{v}$ の両方に垂直だから<br>"
         r"$\mathrm{PQ}^2=|\overrightarrow{\mathrm{P_0Q_0}}|^2+|(t-2)\vec{v}-(s-2)\vec{u}|^2\geqq|\overrightarrow{\mathrm{P_0Q_0}}|^2=3$<br>"
         r"等号は $s=t=2$ のとき成り立つ。よって PQ の最小値は $\boldsymbol{\sqrt3}$ で、このとき　$\boldsymbol{\mathrm{P}(1,\ 0,\ 0),\ \mathrm{Q}(2,\ -1,\ 1)}$",
  "note": r"$\mathrm{PQ}^2=(3-s)^2+(t-s-1)^2+(t-1)^2$ を、まず $s$ について、次に $t$ について平方完成しても求まる（2変数の2次式の最小）。最小値が正で、$\vec{u}$ と $\vec{v}$ が平行でないから、$\ell$ と $m$ はねじれの位置にある。",
  "ex": r"2直線 $\ell:\ (x,\ y,\ z)=s(1,\ 0,\ 1)$，$m:\ (x,\ y,\ z)=(-3,\ 0,\ 3)+t(1,\ 1,\ 0)$ 上の点 P，Q について、PQ の最小値と、そのときの P，Q の座標を求めよ。",
  "exa": r"最小値 $2\sqrt3$（$\mathrm{P}(1,\ 0,\ 1)$，$\mathrm{Q}(-1,\ 2,\ 3)$）"},
 {"lv": 4, "title": "直角四面体の垂線の足（垂心と長さの関係）",
  "q": _fig_right_tet() + r"四面体 OABC において、OA，OB，OC は互いに垂直で、$\mathrm{OA}=p$，$\mathrm{OB}=q$，$\mathrm{OC}=r$ とする。O から平面 ABC に垂線 OH を下ろす。<br>(1) H は $\triangle\mathrm{ABC}$ の垂心であることを示せ。<br>(2) $\dfrac1{\mathrm{OH}^2}=\dfrac1{p^2}+\dfrac1{q^2}+\dfrac1{r^2}$ を示せ。",
  "hint": r"(1) $\mathrm{AH}\perp\mathrm{BC}$ を示せばよい（$\mathrm{BH}\perp\mathrm{CA}$ も同様）。$\overrightarrow{\mathrm{AH}}=\overrightarrow{\mathrm{OH}}-\overrightarrow{\mathrm{OA}}$ と分け、OH が平面 ABC に垂直、OA が平面 OBC に垂直であることを使う。(2) H は平面 ABC 上にあるので $\overrightarrow{\mathrm{OH}}=\alpha\vec{a}+\beta\vec{b}+\gamma\vec{c}$（$\alpha+\beta+\gamma=1$）とおく。",
  "sol": r"$\vec{a}=\overrightarrow{\mathrm{OA}},\ \vec{b}=\overrightarrow{\mathrm{OB}},\ \vec{c}=\overrightarrow{\mathrm{OC}}$ とおくと　$\vec{a}\cdot\vec{b}=\vec{b}\cdot\vec{c}=\vec{c}\cdot\vec{a}=0$，$|\vec{a}|=p$，$|\vec{b}|=q$，$|\vec{c}|=r$<br>"
         r"(1) OH は平面 ABC に垂直だから $\overrightarrow{\mathrm{OH}}\cdot\overrightarrow{\mathrm{BC}}=0$。また $\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{BC}}=\vec{a}\cdot(\vec{c}-\vec{b})=0$。よって<br>"
         r"$\overrightarrow{\mathrm{AH}}\cdot\overrightarrow{\mathrm{BC}}=(\overrightarrow{\mathrm{OH}}-\overrightarrow{\mathrm{OA}})\cdot\overrightarrow{\mathrm{BC}}=0$　同様に　$\overrightarrow{\mathrm{BH}}\cdot\overrightarrow{\mathrm{CA}}=0$<br>"
         r"ここで $\overrightarrow{\mathrm{OA}}\cdot\overrightarrow{\mathrm{AB}}=\vec{a}\cdot(\vec{b}-\vec{a})=-p^2\neq0$ より OA は平面 ABC に垂直でないから $\mathrm{H}\neq\mathrm{A}$，同様に $\mathrm{H}\neq\mathrm{B}$。したがって H は、平面 ABC 上で A から BC に引いた垂線と、B から CA に引いた垂線の両方の上にあり、$\triangle\mathrm{ABC}$ の垂心である。　$\blacksquare$<br>"
         r"(2) H は平面 ABC 上にあるから $\overrightarrow{\mathrm{OH}}=\alpha\vec{a}+\beta\vec{b}+\gamma\vec{c}$，$\alpha+\beta+\gamma=1$ とおける。<br>"
         r"$\overrightarrow{\mathrm{OH}}\cdot\overrightarrow{\mathrm{AB}}=\overrightarrow{\mathrm{OH}}\cdot(\vec{b}-\vec{a})=\beta q^2-\alpha p^2=0$，同様に $\overrightarrow{\mathrm{OH}}\cdot\overrightarrow{\mathrm{AC}}=\gamma r^2-\alpha p^2=0$<br>"
         r"よって $\alpha p^2=\beta q^2=\gamma r^2$。この値を $k$ とおくと $\alpha=\dfrac k{p^2}$，$\beta=\dfrac k{q^2}$，$\gamma=\dfrac k{r^2}$ で、$\alpha+\beta+\gamma=1$ より　$k\left(\dfrac1{p^2}+\dfrac1{q^2}+\dfrac1{r^2}\right)=1$<br>"
         r"一方　$\mathrm{OH}^2=|\alpha\vec{a}+\beta\vec{b}+\gamma\vec{c}|^2=\alpha^2p^2+\beta^2q^2+\gamma^2r^2=k(\alpha+\beta+\gamma)=k$<br>"
         r"ゆえに　$\dfrac1{\mathrm{OH}^2}=\dfrac1k=\dfrac1{p^2}+\dfrac1{q^2}+\dfrac1{r^2}$　$\blacksquare$",
  "note": r"(2) と体積 $V=\dfrac{pqr}6=\dfrac13\cdot\triangle\mathrm{ABC}\cdot\mathrm{OH}$ から　$\triangle\mathrm{ABC}^2=\triangle\mathrm{OAB}^2+\triangle\mathrm{OBC}^2+\triangle\mathrm{OCA}^2$（三平方の定理の空間版）が導かれる。座標を $\mathrm{A}(p,\ 0,\ 0)$ などと定め、平面 ABC の方程式 $\dfrac xp+\dfrac yq+\dfrac zr=1$ と点と平面の距離の公式（次の節）を使っても (2) が示せる。",
  "ex": r"四面体 OABC において OA，OB，OC は互いに垂直で、$\mathrm{OA}=2$，$\mathrm{OB}=3$，$\mathrm{OC}=6$ である。O と平面 ABC の距離、および $\triangle\mathrm{ABC}$ の面積を求めよ。",
  "exa": r"距離 $\dfrac{3\sqrt{14}}7$，面積 $3\sqrt{14}$"},
]})

# ---------------------------------------------------------------- 節5
def _fig_unfold():
    sub = lambda c: f'{c}<tspan dy="3" font-size="8">1</tspan>'
    it = [("l", (-0.8, 0), (7.2, 0), _HID), ("l", (0, 3), (6, -6), _ACC, False, 1.4),
          ("l", (0, 3), (0, 0), _HID, True, 0.8), ("l", (6, -6), (6, 0), _HID, True, 0.8),
          ("d", (0, 3)), ("d", (6, -6)), ("d", (2, 0)),
          ("t", (0, 3), sub("A"), -10, -2), ("t", (6, -6), sub("B"), 11, 0), ("t", (2, 0), "X", 6, -10),
          ("t", (0, 0), "0", -5, 8, 9), ("t", (6, 0), "6", 6, -8, 9), ("t", (0, 1.5), "3", -7, 0, 9), ("t", (6, -3), "6", 7, 0, 9)]
    return fig2d(it, (-1, 7.5, -6.5, 3.5), W=150, H=135)


SEC.append({"title": "直線と平面の方程式（発展）",
"base": r"""・点 $\mathrm{A}(x_1,\ y_1,\ z_1)$ を通り $\vec{n}=(a,\ b,\ c)$ に垂直な平面：$a(x-x_1)+b(y-y_1)+c(z-z_1)=0$。平面 $ax+by+cz+d=0$ の法線ベクトルは $(a,\ b,\ c)$<br>
・点 A を通り $\vec{u}=(l,\ m,\ n)$ に平行な直線：$(x,\ y,\ z)=(x_1,\ y_1,\ z_1)+t(l,\ m,\ n)$（$t$ は実数）<br>
・点 $(x_0,\ y_0,\ z_0)$ と平面 $ax+by+cz+d=0$ の距離は　$\dfrac{|ax_0+by_0+cz_0+d|}{\sqrt{a^2+b^2+c^2}}$（垂線の足を $(x_0,\ y_0,\ z_0)+k(a,\ b,\ c)$ とおいて導ける）<br>
・2点が平面 $ax+by+cz+d=0$ の同じ側にある $\iff$ 2点の座標を代入した $ax+by+cz+d$ の値が同符号<br>
（平面・直線の方程式と点と平面の距離は、教科書では発展として扱われるが、入試では頻出である）""",
"items": [
 {"lv": 1, "title": "平面の方程式と直線との交点",
  "q": r"(1) 点 $\mathrm{A}(1,\ 2,\ -1)$ を通り、$\vec{n}=(2,\ -1,\ 3)$ に垂直な平面 $\alpha$ の方程式を求めよ。<br>(2) 2点 $\mathrm{B}(2,\ 1,\ 0)$，$\mathrm{C}(3,\ 2,\ -1)$ を通る直線と平面 $\alpha$ の交点の座標を求めよ。",
  "hint": r"(1) 平面上の点 $\mathrm{P}(x,\ y,\ z)$ について $\overrightarrow{\mathrm{AP}}\cdot\vec{n}=0$。(2) 直線上の点を媒介変数 $t$ で表し、平面の方程式に代入する。",
  "sol": r"(1) 平面 $\alpha$ 上の点を $\mathrm{P}(x,\ y,\ z)$ とすると $\overrightarrow{\mathrm{AP}}\cdot\vec{n}=0$ より<br>"
         r"$2(x-1)-(y-2)+3(z+1)=0$　すなわち　$\boldsymbol{2x-y+3z+3=0}$<br>"
         r"(2) $\overrightarrow{\mathrm{BC}}=(1,\ 1,\ -1)$ より、直線 BC 上の点は $(x,\ y,\ z)=(2+t,\ 1+t,\ -t)$（$t$ は実数）と表せる。$\alpha$ の方程式に代入して<br>"
         r"$2(2+t)-(1+t)+3(-t)+3=0$，$6-2t=0$，$t=3$　よって交点は　$\boldsymbol{(5,\ 4,\ -3)}$",
  "note": r"$t$ の1次方程式が「$0\cdot t=$（$0$ でない数）」となるときは直線と平面は平行で交点がなく、「$0\cdot t=0$」となるときは直線が平面に含まれる。",
  "ex": r"(1) 点 $\mathrm{A}(3,\ 0,\ -2)$ を通り $\vec{n}=(1,\ 2,\ -2)$ に垂直な平面の方程式を求めよ。(2) 2点 $\mathrm{B}(2,\ 1,\ 1)$，$\mathrm{C}(4,\ 3,\ -1)$ を通る直線と (1) の平面の交点の座標を求めよ。",
  "exa": r"(1) $x+2y-2z-7=0$　(2) $(3,\ 2,\ 0)$"},
 {"lv": 2, "title": "3点を通る平面と点と平面の距離",
  "q": r"3点 $\mathrm{A}(1,\ 0,\ 1)$，$\mathrm{B}(2,\ 1,\ 0)$，$\mathrm{C}(0,\ 2,\ 1)$ を通る平面を $\alpha$ とする。<br>(1) 平面 $\alpha$ の方程式を求めよ。<br>(2) 点 $\mathrm{P}(2,\ 0,\ 5)$ と平面 $\alpha$ の距離、および P から $\alpha$ に下ろした垂線の足 H の座標を求めよ。",
  "hint": r"(1) 法線ベクトル $\vec{n}=(a,\ b,\ c)$ を $\vec{n}\cdot\overrightarrow{\mathrm{AB}}=0$，$\vec{n}\cdot\overrightarrow{\mathrm{AC}}=0$ から求める（$a,\ b,\ c$ の比が決まればよい）。(2) 距離は公式で。H は P を通り $\vec{n}$ に平行な直線上にあるので $\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OP}}+k\vec{n}$ とおく。",
  "sol": r"(1) $\overrightarrow{\mathrm{AB}}=(1,\ 1,\ -1)$，$\overrightarrow{\mathrm{AC}}=(-1,\ 2,\ 0)$。$\alpha$ の法線ベクトルを $\vec{n}=(a,\ b,\ c)$ とすると<br>"
         r"$a+b-c=0$，$-a+2b=0$　より　$a=2b$，$c=3b$<br>"
         r"$b=1$ として $\vec{n}=(2,\ 1,\ 3)$。$\alpha$ は A を通るから $2(x-1)+y+3(z-1)=0$，すなわち　$\boldsymbol{2x+y+3z-5=0}$<br>"
         r"(2) 距離は　$\dfrac{|2\cdot2+0+3\cdot5-5|}{\sqrt{4+1+9}}=\dfrac{14}{\sqrt{14}}=\boldsymbol{\sqrt{14}}$<br>"
         r"H は $\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OP}}+k\vec{n}=(2+2k,\ k,\ 5+3k)$ とおけて、$\alpha$ 上にあるから<br>"
         r"$2(2+2k)+k+3(5+3k)-5=0$，$14+14k=0$，$k=-1$　よって　$\boldsymbol{\mathrm{H}(0,\ -1,\ 2)}$",
  "note": r"3点の座標を $ax+by+cz+d=0$ に代入して連立してもよいが、法線ベクトルから求める方が計算が少ない。$\mathrm{PH}=|k||\vec{n}|=\sqrt{14}$ は距離の公式の結果と一致する。",
  "ex": r"3点 $\mathrm{A}(1,\ 2,\ 0)$，$\mathrm{B}(0,\ 1,\ 1)$，$\mathrm{C}(2,\ 0,\ 1)$ を通る平面の方程式を求めよ。また、点 $\mathrm{P}(2,\ 1,\ 5)$ とこの平面の距離と、P から平面に下ろした垂線の足の座標を求めよ。",
  "exa": r"$x+2y+3z-5=0$，距離 $\sqrt{14}$，垂線の足 $(1,\ -1,\ 2)$"},
 {"lv": 3, "title": "平面に関する対称点と距離の和の最小",
  "q": r"平面 $\alpha:\ x-y+z=5$ と2点 $\mathrm{A}(1,\ 2,\ 3)$，$\mathrm{B}(3,\ 0,\ 0)$ がある。<br>(1) 平面 $\alpha$ に関して A と対称な点 $\mathrm{A'}$ の座標を求めよ。<br>(2) 点 P が $\alpha$ 上を動くとき、$\mathrm{AP}+\mathrm{PB}$ の最小値と、そのときの P の座標を求めよ。",
  "hint": r"(1) $\mathrm{AA'}$ は $\alpha$ に垂直で、$\mathrm{AA'}$ の中点が $\alpha$ 上にある。(2) A，B が $\alpha$ の同じ側にあることを確かめ、$\mathrm{AP}=\mathrm{A'P}$ を使って折れ線を1本の線分にする（平面図形の「対称点」と同じ発想）。",
  "sol": r"$f(x,\ y,\ z)=x-y+z-5$ とおく。<br>"
         r"(1) $\mathrm{AA'}$ は $\alpha$ の法線ベクトル $\vec{n}=(1,\ -1,\ 1)$ に平行だから、$\overrightarrow{\mathrm{OA'}}=\overrightarrow{\mathrm{OA}}+k\vec{n}=(1+k,\ 2-k,\ 3+k)$ とおける。<br>"
         r"$\mathrm{AA'}$ の中点 $\left(1+\dfrac k2,\ 2-\dfrac k2,\ 3+\dfrac k2\right)$ が $\alpha$ 上にあるから　$\left(1+\dfrac k2\right)-\left(2-\dfrac k2\right)+\left(3+\dfrac k2\right)=5$，$2+\dfrac{3k}2=5$，$k=2$<br>"
         r"よって　$\boldsymbol{\mathrm{A'}(3,\ 0,\ 5)}$<br>"
         r"(2) $f(\mathrm{A})=1-2+3-5=-3<0$，$f(\mathrm{B})=3-0+0-5=-2<0$ より、A，B は $\alpha$ に関して同じ側にあり、$\mathrm{A'}$ は反対側にある。<br>"
         r"$\alpha$ 上の点 P について $\mathrm{AP}=\mathrm{A'P}$ であるから　$\mathrm{AP}+\mathrm{PB}=\mathrm{A'P}+\mathrm{PB}\geqq\mathrm{A'B}$<br>"
         r"等号は P が線分 $\mathrm{A'B}$ と $\alpha$ の交点のとき成り立つ。$\overrightarrow{\mathrm{A'B}}=(0,\ 0,\ -5)$ より $\mathrm{A'B}=5$。<br>"
         r"線分 $\mathrm{A'B}$ 上の点 $(3,\ 0,\ 5-5w)$（$0\leqq w\leqq1$）を $\alpha$ の方程式に代入して $3+5-5w=5$，$w=\dfrac35$<br>"
         r"よって　最小値 $\boldsymbol{5}$，このとき $\boldsymbol{\mathrm{P}(3,\ 0,\ 2)}$",
  "note": r"A と B が $\alpha$ に関して反対側にあるときは、線分 AB と $\alpha$ の交点で最小値 AB をとる（対称点は不要）。$f$ の符号で同じ側か反対側かを必ず確かめる。",
  "ex": r"平面 $x+y+z=3$ と2点 $\mathrm{A}(1,\ 2,\ 3)$，$\mathrm{B}(4,\ 0,\ 1)$ がある。点 P がこの平面上を動くとき、$\mathrm{AP}+\mathrm{PB}$ の最小値とそのときの P の座標を求めよ。",
  "exa": r"最小値 $5$，$\mathrm{P}(2,\ 0,\ 1)$（A の対称点は $(-1,\ 0,\ 1)$）"},
 {"lv": 4, "title": "直線上の点と2定点の距離の和の最小",
  "q": r"原点 O と点 $(1,\ 2,\ 2)$ を通る直線を $\ell$ とし、2点 $\mathrm{A}(2,\ 1,\ -2)$，$\mathrm{B}(-2,\ 8,\ 2)$ をとる。点 P が $\ell$ 上を動くとき、$\mathrm{AP}+\mathrm{PB}$ の最小値と、そのときの P の座標を求めよ。",
  "hint": r"$\mathrm{P}(t,\ 2t,\ 2t)$ とおくと、$\mathrm{AP},\ \mathrm{PB}$ はそれぞれ $\sqrt{(3t-\alpha)^2+\beta^2}$ の形に整理できる。これを座標平面上の2点間の距離とみて、平面での折れ線の最短問題に直す（$\ell$ のまわりに B を回転して、$\ell$ と A を含む平面に移す発想）。",
  "sol": _fig_unfold() + r"$\mathrm{P}(t,\ 2t,\ 2t)$ とおくと<br>"
         r"$\mathrm{AP}^2=(t-2)^2+(2t-1)^2+(2t+2)^2=9t^2+9$<br>"
         r"$\mathrm{BP}^2=(t+2)^2+(2t-8)^2+(2t-2)^2=9t^2-36t+72=9(t-2)^2+36$<br>"
         r"よって　$\mathrm{AP}+\mathrm{PB}=\sqrt{(3t)^2+3^2}+\sqrt{(3t-6)^2+6^2}$<br>"
         r"$xy$ 平面上に3点 $\mathrm{X}(3t,\ 0)$，$\mathrm{A_1}(0,\ 3)$，$\mathrm{B_1}(6,\ -6)$ をとると（右図）<br>"
         r"$\mathrm{AP}+\mathrm{PB}=\mathrm{A_1X}+\mathrm{XB_1}\geqq\mathrm{A_1B_1}=\sqrt{6^2+9^2}=3\sqrt{13}$<br>"
         r"$\mathrm{A_1},\ \mathrm{B_1}$ は $x$ 軸の反対側にあるから、等号は X が線分 $\mathrm{A_1B_1}$ と $x$ 軸の交点 $(2,\ 0)$ のとき、すなわち $3t=2$，$t=\dfrac23$ のとき成り立つ。<br>"
         r"よって　最小値 $\boldsymbol{3\sqrt{13}}$，このとき $\boldsymbol{\mathrm{P}\left(\dfrac23,\ \dfrac43,\ \dfrac43\right)}$",
  "note": r"$3t$ は $\ell$ 上で O から P までの符号つきの距離（$|(1,\ 2,\ 2)|=3$），$3$ と $6$ はそれぞれ A，B と $\ell$ の距離である（垂線の足は $\mathrm{O}$ と $(2,\ 4,\ 4)$）。上の平面図は、B を $\ell$ のまわりに回転して、$\ell$ と A を含む平面上の $\ell$ に関して A と反対側に移したものにあたる。微分を使って根号の和を調べるより、はるかに簡潔である。",
  "ex": r"原点 O と点 $(2,\ 1,\ 2)$ を通る直線 $\ell$ と、2点 $\mathrm{A}(1,\ 2,\ -2)$，$\mathrm{B}(6,\ -3,\ 0)$ がある。点 P が $\ell$ 上を動くとき、$\mathrm{AP}+\mathrm{PB}$ の最小値とそのときの P の座標を求めよ。",
  "exa": r"最小値 $3\sqrt{10}$，$\mathrm{P}\left(\dfrac23,\ \dfrac13,\ \dfrac23\right)$"},
]})

# ---------------------------------------------------------------- 節6
def _fig_shadow():
    it = [("l", (-3.7, 0), (2.0, 0), _INK), ("l", (0, -0.25), (0, 3.4), _HID, False, 0.8),
          ("l", (-3, 0), (1, 0), _ACC, False, 3.2),
          ("c", (0, 1), 1, "#eef2fa"),
          ("l", (1, 3), (-3, 0), _HID, True, 0.9), ("l", (1, 3), (1, 0), _HID, True, 0.9),
          ("d", (1, 3)), ("d", (0, 1)), ("t", (1, 3), "L", 8, -4), ("t", (0, 1), "C", 7, 2),
          ("t", (-3, 0), "−3", 0, 10, 10), ("t", (1, 0), "1", 3, 10, 10), ("t", (0, 0), "O", -7, 9, 10),
          ("t", (2.0, 0), "x", 4, -7, 10), ("t", (0, 3.4), "z", 7, 2, 10)]
    return fig2d(it, (-3.8, 2.2, -0.4, 3.5), W=180, H=120)


SEC.append({"title": "球面の方程式",
"base": r"""・中心 $(a,\ b,\ c)$，半径 $r$ の球面：$(x-a)^2+(y-b)^2+(z-c)^2=r^2$。展開すると $x^2+y^2+z^2+Ax+By+Cz+D=0$ の形<br>
・2点 A，B を直径の両端とする球面：中心は AB の中点、半径は $\dfrac{\mathrm{AB}}2$（球面上の点 P について $\overrightarrow{\mathrm{AP}}\cdot\overrightarrow{\mathrm{BP}}=0$ と表してもよい）<br>
・球面と平面：中心と平面の距離を $d$ とすると、$d<r$ のとき交わりは円で、その中心は球の中心から平面に下ろした垂線の足、半径は $\sqrt{r^2-d^2}$。$d=r$ のとき接する<br>
・球面と直線：直線上の点を $t$ で表して代入し、$t$ の2次方程式の実数解を調べる""",
"items": [
 {"lv": 1, "title": "球面の方程式の決定と中心・半径",
  "q": r"(1) 中心が $(1,\ -2,\ 3)$，半径が $4$ の球面の方程式を求めよ。<br>(2) 2点 $\mathrm{A}(3,\ -1,\ 2)$，$\mathrm{B}(-1,\ 3,\ 0)$ を直径の両端とする球面の方程式を求めよ。<br>(3) 球面 $x^2+y^2+z^2-4x+2y-6z+5=0$ の中心の座標と半径を求めよ。",
  "hint": r"円の方程式と同様に考える。(2) は中心が AB の中点、半径が AB の半分。(3) は $x,\ y,\ z$ それぞれについて平方完成する。",
  "sol": r"(1) $\boldsymbol{(x-1)^2+(y+2)^2+(z-3)^2=16}$<br>"
         r"(2) 中心は AB の中点 $(1,\ 1,\ 1)$，半径は $\dfrac{\mathrm{AB}}2=\dfrac{\sqrt{16+16+4}}2=3$。よって　$\boldsymbol{(x-1)^2+(y-1)^2+(z-1)^2=9}$<br>"
         r"(3) $(x-2)^2+(y+1)^2+(z-3)^2=4+1+9-5=9$　よって　中心 $\boldsymbol{(2,\ -1,\ 3)}$，半径 $\boldsymbol{3}$",
  "note": r"(3) の形の方程式で、平方完成した右辺が負になれば表す図形はなく、$0$ なら1点を表す。",
  "ex": r"(1) 中心が $(-2,\ 0,\ 1)$ で原点を通る球面の方程式を求めよ。(2) 2点 $\mathrm{A}(0,\ 2,\ -1)$，$\mathrm{B}(4,\ -2,\ 1)$ を直径の両端とする球面の方程式を求めよ。(3) 球面 $x^2+y^2+z^2+2x-4z-4=0$ の中心と半径を求めよ。",
  "exa": r"(1) $(x+2)^2+y^2+(z-1)^2=5$　(2) $(x-2)^2+y^2+z^2=9$　(3) 中心 $(-1,\ 0,\ 2)$，半径 $3$"},
 {"lv": 2, "title": "4点を通る球面",
  "q": r"4点 $\mathrm{O}(0,\ 0,\ 0)$，$\mathrm{A}(3,\ 1,\ 0)$，$\mathrm{B}(0,\ 3,\ 1)$，$\mathrm{C}(2,\ 0,\ -2)$ を通る球面の方程式を求めよ。また、その中心の座標と半径を求めよ。",
  "hint": r"中心も半径も分からないので、展開した形 $x^2+y^2+z^2+ax+by+cz+d=0$ とおいて4点の座標を代入する。O を通ることから $d=0$ がすぐに分かる。",
  "sol": r"求める球面を $x^2+y^2+z^2+ax+by+cz+d=0$ とおく。O を通るから $d=0$。A，B，C を通るから<br>"
         r"$10+3a+b=0$ …①，$10+3b+c=0$ …②，$8+2a-2c=0$ …③<br>"
         r"①より $b=-3a-10$，②より $c=-3b-10=9a+20$。③に代入して $8+2a-18a-40=0$，$a=-2$<br>"
         r"よって $b=-4$，$c=2$ で　$\boldsymbol{x^2+y^2+z^2-2x-4y+2z=0}$<br>"
         r"$(x-1)^2+(y-2)^2+(z+1)^2=6$ より　中心 $\boldsymbol{(1,\ 2,\ -1)}$，半径 $\boldsymbol{\sqrt6}$",
  "note": r"4点が同じ平面上にないとき、4点を通る球面（四面体の外接球面）はただ1つ定まる。4点が同じ平面上にあるときは、4点が1つの円周上にあれば球面は無数にあり、そうでなければ存在しない。",
  "ex": r"4点 $\mathrm{O}(0,\ 0,\ 0)$，$\mathrm{A}(4,\ 0,\ 0)$，$\mathrm{B}(3,\ 1,\ 2)$，$\mathrm{C}(1,\ 0,\ 3)$ を通る球面の方程式と、その中心・半径を求めよ。",
  "exa": r"$x^2+y^2+z^2-4x+2y-2z=0$，中心 $(2,\ -1,\ 1)$，半径 $\sqrt6$"},
 {"lv": 2, "title": "3つの座標平面に接する球面",
  "q": r"点 $(1,\ 2,\ 5)$ を通り、3つの座標平面（$xy$ 平面，$yz$ 平面，$zx$ 平面）のすべてに接する球面の方程式を求めよ。",
  "hint": r"3つの座標平面に接する球面の中心は、各座標平面からの距離がすべて半径 $r$ に等しい。通る点の座標がすべて正であることから、中心は $(r,\ r,\ r)$ とおける。",
  "sol": r"半径を $r$ とする。球面は $xy$ 平面に接するから $xy$ 平面の一方の側にあり、点 $(1,\ 2,\ 5)$ を通るので $z\geqq0$ の側にある。よって中心の $z$ 座標は $r$。同様に $x$ 座標，$y$ 座標も $r$ で、中心は $(r,\ r,\ r)$ となり、球面は $(x-r)^2+(y-r)^2+(z-r)^2=r^2$。<br>"
         r"点 $(1,\ 2,\ 5)$ を通るから　$(1-r)^2+(2-r)^2+(5-r)^2=r^2$<br>"
         r"$2r^2-16r+30=0$，$r^2-8r+15=0$，$(r-3)(r-5)=0$，$r=3,\ 5$<br>"
         r"よって　$\boldsymbol{(x-3)^2+(y-3)^2+(z-3)^2=9,\ \ (x-5)^2+(y-5)^2+(z-5)^2=25}$",
  "note": r"通る点の座標に負のものがあるときは、その符号に合わせて中心の座標の符号を決める。$r$ の2次方程式が実数解をもたなければ、条件を満たす球面は存在しない。",
  "ex": r"点 $(1,\ -4,\ 5)$ を通り、3つの座標平面のすべてに接する球面の方程式を求めよ。",
  "exa": r"$(x-3)^2+(y+3)^2+(z-3)^2=9$，$(x-7)^2+(y+7)^2+(z-7)^2=49$"},
 {"lv": 3, "title": "球面と平面の交わりの円・接する平面",
  "q": r"球面 $S:\ x^2+y^2+z^2-2x+4y-6z-11=0$ と平面 $\alpha:\ 2x-y+2z=1$ がある。<br>(1) $S$ と $\alpha$ の交わりは円である。その中心の座標と半径を求めよ。<br>(2) $\alpha$ に平行で、$S$ に接する平面の方程式を求めよ。",
  "hint": r"球の中心 C から平面に下ろした垂線の足が交わりの円の中心で、半径は三平方の定理で $\sqrt{r^2-d^2}$。(2) は「中心と平面の距離 $=$ 半径」。",
  "sol": r"$S$ は $(x-1)^2+(y+2)^2+(z-3)^2=25$ より、中心 $\mathrm{C}(1,\ -2,\ 3)$，半径 $5$。<br>"
         r"(1) C と $\alpha$ の距離は　$d=\dfrac{|2+2+6-1|}{\sqrt{4+1+4}}=\dfrac93=3$<br>"
         r"交わりの円の中心は、C から $\alpha$ に下ろした垂線の足 H である。$\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OC}}+k(2,\ -1,\ 2)=(1+2k,\ -2-k,\ 3+2k)$ を $\alpha$ の方程式に代入して<br>"
         r"$2(1+2k)-(-2-k)+2(3+2k)=1$，$10+9k=1$，$k=-1$　より　$\mathrm{H}(-1,\ -1,\ 1)$<br>"
         r"半径は $\sqrt{5^2-3^2}=4$。よって　中心 $\boldsymbol{(-1,\ -1,\ 1)}$，半径 $\boldsymbol{4}$<br>"
         r"(2) 求める平面を $2x-y+2z+e=0$ とおく。C との距離が半径 $5$ に等しいから<br>"
         r"$\dfrac{|2+2+6+e|}3=5$，$|10+e|=15$，$e=5,\ -25$　よって　$\boldsymbol{2x-y+2z+5=0,\ \ 2x-y+2z-25=0}$",
  "note": r"接点は C から各平面に下ろした垂線の足で、$\overrightarrow{\mathrm{OC}}\pm\dfrac53(2,\ -1,\ 2)$ と表せる。",
  "ex": r"球面 $x^2+y^2+z^2+4x-2y-4z=0$ と平面 $x+y+z=4$ の交わりの円の中心と半径を求めよ。また、平面 $x+y+z=4$ に平行でこの球面に接する平面の方程式を求めよ。",
  "exa": r"中心 $(-1,\ 2,\ 3)$，半径 $\sqrt6$；$x+y+z=1\pm3\sqrt3$"},
 {"lv": 3, "title": "球面と直線の交点・外部の点から引いた接線",
  "q": r"球面 $S:\ x^2+y^2+z^2=9$ がある。<br>(1) 直線 $\ell:\ (x,\ y,\ z)=(4,\ 2,\ 3)+t(1,\ 0,\ 1)$ と $S$ の交点の座標と、$S$ によって切り取られる $\ell$ の線分の長さを求めよ。<br>(2) 点 $\mathrm{A}(0,\ 0,\ 5)$ から $S$ に接線を引くとき、接点の全体はある平面上の円になる。その平面の方程式と円の半径を求めよ。",
  "hint": r"(1) 直線上の点を $S$ の方程式に代入して $t$ の2次方程式を解く。(2) 接点を T とすると、接線は半径 OT に垂直：$\overrightarrow{\mathrm{OT}}\cdot\overrightarrow{\mathrm{AT}}=0$。これと $|\overrightarrow{\mathrm{OT}}|=3$ を組み合わせる。",
  "sol": r"(1) $(4+t)^2+2^2+(3+t)^2=9$ より　$2t^2+14t+20=0$，$t^2+7t+10=0$，$(t+2)(t+5)=0$，$t=-2,\ -5$<br>"
         r"よって交点は　$\boldsymbol{(2,\ 2,\ 1),\ (-1,\ 2,\ -2)}$。線分の長さは　$\sqrt{3^2+0^2+3^2}=\boldsymbol{3\sqrt2}$<br>"
         r"(2) T を $S$ 上の点とする。直線 AT が T で $S$ に接する $\iff$ $\mathrm{AT}\perp\mathrm{OT}$ $\iff$ $\overrightarrow{\mathrm{OT}}\cdot\overrightarrow{\mathrm{AT}}=0$ である。$\mathrm{T}(x,\ y,\ z)$ とすると<br>"
         r"$\overrightarrow{\mathrm{OT}}\cdot(\overrightarrow{\mathrm{OT}}-\overrightarrow{\mathrm{OA}})=|\overrightarrow{\mathrm{OT}}|^2-\overrightarrow{\mathrm{OT}}\cdot\overrightarrow{\mathrm{OA}}=9-5z$<br>"
         r"よって、接点となる条件は $z=\dfrac95$ で、接点の全体は平面 $\boldsymbol{z=\dfrac95}$ と $S$ の交わりの円である。<br>"
         r"その半径は　$\sqrt{9-\left(\dfrac95\right)^2}=\sqrt{\dfrac{144}{25}}=\boldsymbol{\dfrac{12}5}$",
  "note": r"接線の長さは $\mathrm{AT}=\sqrt{\mathrm{OA}^2-\mathrm{OT}^2}=\sqrt{25-9}=4$ で、円の半径は直角三角形 OAT の斜辺 OA への高さ $\dfrac{\mathrm{OT}\cdot\mathrm{AT}}{\mathrm{OA}}=\dfrac{3\cdot4}5$ としても求まる。(1) で直線と球面が接する条件は、$t$ の2次方程式の判別式が $0$ となること。",
  "ex": r"球面 $x^2+y^2+z^2=25$ について、(1) 直線 $(x,\ y,\ z)=(5,\ 4,\ -2)+t(1,\ 0,\ -1)$ との交点と、切り取られる線分の長さを求めよ。(2) 点 $(0,\ 0,\ 13)$ から引いた接線の接点の全体が乗る平面の方程式と、その円の半径を求めよ。",
  "exa": r"(1) $(3,\ 4,\ 0)$，$(0,\ 4,\ 3)$，長さ $3\sqrt2$　(2) 平面 $z=\dfrac{25}{13}$，半径 $\dfrac{60}{13}$"},
 {"lv": 4, "title": "点光源による球の影",
  "q": _fig_shadow() + r"中心 $\mathrm{C}(0,\ 0,\ 1)$，半径 $1$ の球が $xy$ 平面上に置かれている。点 $\mathrm{L}(1,\ 0,\ 3)$ に点光源があるとき、球によって $xy$ 平面上にできる影の部分（光の当たらない部分）を表す不等式を求めよ。また、影の部分に含まれる点の $x$ 座標の範囲を求めよ。（図は $xz$ 平面による切り口）",
  "hint": r"$xy$ 平面上の点 $\mathrm{Q}(X,\ Y,\ 0)$ が影 $\iff$ 線分 LQ が球と共有点をもつ。直線 LQ 上の点を $\overrightarrow{\mathrm{OL}}+s\overrightarrow{\mathrm{LQ}}$ とおき、「球の中心までの距離が $1$ 以下」となる $s$ が存在する条件を判別式で表す。",
  "sol": r"$xy$ 平面上の点 $\mathrm{Q}(X,\ Y,\ 0)$ が影の部分にあるのは、線分 LQ が球（内部を含む）と共有点をもつときである。<br>"
         r"直線 LQ 上の点 R を $\overrightarrow{\mathrm{OR}}=\overrightarrow{\mathrm{OL}}+s\overrightarrow{\mathrm{LQ}}$（$s$ は実数）と表す。R の $z$ 座標は $3-3s$ で、球は $0\leqq z\leqq2$ の範囲にあるから、直線 LQ と球の共有点では $\dfrac13\leqq s\leqq1$ となり、それは線分 LQ 上にある。よって「直線 LQ が球と共有点をもつ」条件を求めればよい。<br>"
         r"$\overrightarrow{\mathrm{CL}}=(1,\ 0,\ 2)$，$\overrightarrow{\mathrm{LQ}}=(X-1,\ Y,\ -3)$ より、$m=(X-1)^2+Y^2+9$ とおくと<br>"
         r"$|\overrightarrow{\mathrm{CR}}|^2=|\overrightarrow{\mathrm{CL}}+s\overrightarrow{\mathrm{LQ}}|^2=ms^2+2(X-7)s+5$<br>"
         r"$|\overrightarrow{\mathrm{CR}}|^2\leqq1$ となる実数 $s$ が存在する条件は、$ms^2+2(X-7)s+4\leqq0$ を満たす $s$ が存在すること、すなわち（$m>0$ より）判別式について<br>"
         r"$(X-7)^2-4m\geqq0$　より　$X^2-14X+49-4\{(X-1)^2+Y^2+9\}\geqq0$<br>"
         r"整理して $3X^2+6X+4Y^2-9\leqq0$，すなわち $3(X+1)^2+4Y^2\leqq12$。よって影の部分は<br>"
         r"$\boldsymbol{\dfrac{(x+1)^2}4+\dfrac{y^2}3\leqq1}$<br>"
         r"この不等式を満たす点では $(x+1)^2\leqq4$ であり、$y=0$ のとき $x=-3,\ 1$ もとるから、$x$ 座標の範囲は　$\boldsymbol{-3\leqq x\leqq1}$",
  "note": r"影の境界は楕円（2次曲線）である。図の切り口で、L から円に引いた2本の接線が $x$ 軸と $x=-3,\ 1$ で交わることからも $x$ 座標の範囲が確かめられる。光源の真下の点 $(1,\ 0,\ 0)$ が影の端になるのは、L を通る鉛直な直線 $x=1,\ y=0$ が球に接しているからである。",
  "ex": r"同じ球について、光源を $\mathrm{L}(0,\ 2,\ 4)$ に移したとき、$xy$ 平面上にできる影の部分を表す不等式と、影に含まれる点の $y$ 座標の範囲を求めよ。",
  "exa": r"$\dfrac{x^2}2+\dfrac{(y+1)^2}3\leqq1$，$-1-\sqrt3\leqq y\leqq-1+\sqrt3$"},
]})

# ---------------------------------------------------------------- 節7
def _fig_box_tet():
    P = {"A": (0, 0, 0), "1": (4, 0, 0), "B": (4, 3, 0), "2": (0, 3, 0),
         "3": (0, 0, 2), "C": (4, 0, 2), "4": (4, 3, 2), "D": (0, 3, 2)}
    box = ["A1B2", "3C4D", "A1C3", "2B4D", "A2D3", "1B4C"]
    return fig3d(P, faces=["ABC", "ABD", "ACD", "BCD"], faces2=box, lab=["A", "B", "C", "D"],
                 off={"A": (0, 10), "B": (6, -8), "C": (8, -3), "D": (-8, -3)}, W=170, H=130, az=35, el=30)


def _fig_cube_hex():
    t = 1.5
    P = {"O": (0, 0, 0), "1": (1, 0, 0), "2": (1, 1, 0), "3": (0, 1, 0),
         "4": (0, 0, 1), "5": (1, 0, 1), "6": (1, 1, 1), "7": (0, 1, 1)}
    hexv = [(1, t - 1, 0), (t - 1, 1, 0), (0, 1, t - 1), (0, t - 1, 1), (t - 1, 0, 1), (1, 0, t - 1)]
    for i, v in enumerate(hexv):
        P["h%d" % i] = v
    cube = ["O123", "4567", "O154", "3267", "O374", "1265"]
    hx = ["h%d" % i for i in range(6)]
    return fig3d(P, faces2=cube, polys=[(hx, _FILL)], hl=[(hx[i], hx[(i + 1) % 6]) for i in range(6)],
                 lab=["O"], off={"O": (-5, 9)}, W=150, H=140, az=30, el=20)


SEC.append({"title": "四面体の体積と空間図形",
"base": r"""・四面体の体積は　$V=\dfrac13\times$（底面積）$\times$（高さ）。高さは垂線の足や点と平面の距離で求める<br>
・底面積は　$\triangle\mathrm{OAB}=\dfrac12\sqrt{|\vec{a}|^2|\vec{b}|^2-(\vec{a}\cdot\vec{b})^2}$　を使えば、4頂点の座標から体積が求まる<br>
・四面体 OABC の辺 OA，OB，OC 上の点 P，Q，R について、四面体 OPQR と四面体 OABC の体積比は　$\dfrac{\mathrm{OP}}{\mathrm{OA}}\cdot\dfrac{\mathrm{OQ}}{\mathrm{OB}}\cdot\dfrac{\mathrm{OR}}{\mathrm{OC}}$<br>
・対称性のある立体は、直方体・立方体に埋め込む、座標をうまく設定する、などの工夫で計算が軽くなる""",
"items": [
 {"lv": 2, "title": "4頂点の座標から四面体の体積",
  "q": r"4点 $\mathrm{A}(1,\ 1,\ 1)$，$\mathrm{B}(3,\ 1,\ 2)$，$\mathrm{C}(1,\ 3,\ 0)$，$\mathrm{D}(0,\ -4,\ -3)$ を頂点とする四面体 ABCD の体積 $V$ を求めよ。",
  "hint": r"$\triangle\mathrm{ABC}$ を底面とし、D と平面 ABC の距離を高さとする。平面 ABC の方程式は法線ベクトルから求める。",
  "sol": r"$\overrightarrow{\mathrm{AB}}=(2,\ 0,\ 1)$，$\overrightarrow{\mathrm{AC}}=(0,\ 2,\ -1)$ より　$|\overrightarrow{\mathrm{AB}}|^2=5$，$|\overrightarrow{\mathrm{AC}}|^2=5$，$\overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}}=-1$<br>"
         r"$\triangle\mathrm{ABC}=\dfrac12\sqrt{5\cdot5-(-1)^2}=\dfrac12\sqrt{24}=\sqrt6$<br>"
         r"平面 ABC の法線ベクトルを $\vec{n}=(a,\ b,\ c)$ とすると $2a+c=0$，$2b-c=0$。$c=2$ として $\vec{n}=(-1,\ 1,\ 2)$<br>"
         r"平面 ABC：$-(x-1)+(y-1)+2(z-1)=0$，すなわち $x-y-2z+2=0$<br>"
         r"D と平面 ABC の距離は　$h=\dfrac{|0+4+6+2|}{\sqrt{1+1+4}}=\dfrac{12}{\sqrt6}=2\sqrt6$<br>"
         r"よって　$V=\dfrac13\cdot\sqrt6\cdot2\sqrt6=\boldsymbol{4}$",
  "note": r"検算用の公式：$\overrightarrow{\mathrm{AB}}=(a_1,\ a_2,\ a_3)$，$\overrightarrow{\mathrm{AC}}=(b_1,\ b_2,\ b_3)$，$\overrightarrow{\mathrm{AD}}=(c_1,\ c_2,\ c_3)$ のとき<br>$V=\dfrac16|a_1b_2c_3+a_2b_3c_1+a_3b_1c_2-a_3b_2c_1-a_2b_1c_3-a_1b_3c_2|$。この問題では $\dfrac16|-24|=4$。",
  "ex": r"4点 $\mathrm{A}(1,\ 2,\ 0)$，$\mathrm{B}(0,\ 1,\ 1)$，$\mathrm{C}(2,\ 0,\ 1)$，$\mathrm{D}(3,\ 3,\ 2)$ を頂点とする四面体の体積を求めよ。",
  "exa": r"$\dfrac53$"},
 {"lv": 4, "title": "向かい合う辺が等しい四面体（直方体に埋め込む）",
  "q": _fig_box_tet() + r"四面体 ABCD において、$\mathrm{AB}=\mathrm{CD}=5$，$\mathrm{AC}=\mathrm{BD}=2\sqrt5$，$\mathrm{AD}=\mathrm{BC}=\sqrt{13}$ である。この四面体の体積 $V$ を求めよ。",
  "hint": r"向かい合う辺の長さが等しい四面体は、直方体の頂点を1つおきに結んで作ることができる（各辺が直方体の面の対角線になる）。直方体の3辺の長さを求めれば、体積は直方体から4つの角の三角錐を除いて求まる。",
  "sol": r"3辺の長さが $p,\ q,\ r$ の直方体 $0\leqq x\leqq p$，$0\leqq y\leqq q$，$0\leqq z\leqq r$ の4頂点<br>"
         r"$\mathrm{A_1}(0,\ 0,\ 0)$，$\mathrm{B_1}(p,\ q,\ 0)$，$\mathrm{C_1}(p,\ 0,\ r)$，$\mathrm{D_1}(0,\ q,\ r)$<br>"
         r"を考えると　$\mathrm{A_1B_1}^2=\mathrm{C_1D_1}^2=p^2+q^2$，$\mathrm{A_1C_1}^2=\mathrm{B_1D_1}^2=p^2+r^2$，$\mathrm{A_1D_1}^2=\mathrm{B_1C_1}^2=q^2+r^2$<br>"
         r"そこで $p^2+q^2=25$，$p^2+r^2=20$，$q^2+r^2=13$ とすると、辺々加えて $p^2+q^2+r^2=29$ より $r^2=4$，$q^2=9$，$p^2=16$ で、$p=4$，$q=3$，$r=2$ ととれる。<br>"
         r"このとき四面体 $\mathrm{A_1B_1C_1D_1}$ の6辺の長さは四面体 ABCD の対応する辺と等しい。四面体は、底面の三角形（3辺で決まる）と、残りの頂点から底面の3頂点までの距離とで、平面に関する対称移動を除いて決まるから、2つの四面体は合同である。<br>"
         r"四面体 $\mathrm{A_1B_1C_1D_1}$ は、直方体から4つの頂点 $(p,\ 0,\ 0)$，$(0,\ q,\ 0)$，$(0,\ 0,\ r)$，$(p,\ q,\ r)$ の部分の三角錐（体積はそれぞれ $\dfrac16pqr$）を除いたものだから<br>"
         r"$V=pqr-4\cdot\dfrac16pqr=\dfrac13pqr=\dfrac13\cdot4\cdot3\cdot2=\boldsymbol{8}$",
  "note": r"4つの面はすべて合同な三角形（3辺が $5,\ 2\sqrt5,\ \sqrt{13}$）で、このような四面体を等面四面体という。$p^2,\ q^2,\ r^2$ がすべて正になることが必要で、それは各面が鋭角三角形であることと同値である。たとえば3辺が $3,\ 4,\ 5$ の直角三角形4枚では四面体はつくれない。",
  "ex": r"四面体 ABCD において、$\mathrm{AB}=\mathrm{CD}=\sqrt5$，$\mathrm{AC}=\mathrm{BD}=\sqrt{10}$，$\mathrm{AD}=\mathrm{BC}=\sqrt{13}$ のとき、体積を求めよ。",
  "exa": r"$2$（$1\times2\times3$ の直方体に埋め込める）"},
 {"lv": 4, "title": "重心を通る平面で切り取る四面体の体積の範囲",
  "q": r"1辺の長さが $1$ の正四面体 OABC の辺 OA，OB，OC 上（端点 O を除く）に、それぞれ点 P，Q，R を $\mathrm{OP}=p$，$\mathrm{OQ}=q$，$\mathrm{OR}=r$ となるようにとる。平面 PQR が正四面体 OABC の重心 G を通るとき<br>(1) $\dfrac1p+\dfrac1q+\dfrac1r=4$ を示せ。<br>(2) 四面体 OPQR の体積 $V$ の最大値と最小値を求めよ。",
  "hint": r"(1) $\overrightarrow{\mathrm{OG}}=\dfrac14(\vec{a}+\vec{b}+\vec{c})$ を $\overrightarrow{\mathrm{OP}}=p\vec{a}$ などで書き直し、係数の和 $=1$。(2) $V=pqr\,V_0$（$V_0$ は正四面体の体積）。$x=\dfrac1p$ などとおくと、$x+y+z=4$，$x,\ y,\ z\geqq1$ のもとで $xyz$ の範囲を調べる問題になる。",
  "sol": r"$\vec{a}=\overrightarrow{\mathrm{OA}}$，$\vec{b}=\overrightarrow{\mathrm{OB}}$，$\vec{c}=\overrightarrow{\mathrm{OC}}$ とおく。$0<p\leqq1$，$0<q\leqq1$，$0<r\leqq1$ である。<br>"
         r"(1) $\overrightarrow{\mathrm{OG}}=\dfrac14(\vec{a}+\vec{b}+\vec{c})=\dfrac1{4p}\overrightarrow{\mathrm{OP}}+\dfrac1{4q}\overrightarrow{\mathrm{OQ}}+\dfrac1{4r}\overrightarrow{\mathrm{OR}}$<br>"
         r"G は平面 PQR 上にあり、$\overrightarrow{\mathrm{OP}},\ \overrightarrow{\mathrm{OQ}},\ \overrightarrow{\mathrm{OR}}$ は同じ平面上にないから、係数の和は $1$：$\dfrac1{4p}+\dfrac1{4q}+\dfrac1{4r}=1$。よって　$\dfrac1p+\dfrac1q+\dfrac1r=4$　$\blacksquare$<br>"
         r"(2) 正四面体 OABC の体積は $V_0=\dfrac13\cdot\dfrac{\sqrt3}4\cdot\dfrac{\sqrt6}3=\dfrac{\sqrt2}{12}$ で、$V=pqr\,V_0$ である。<br>"
         r"$x=\dfrac1p,\ y=\dfrac1q,\ z=\dfrac1r$ とおくと　$x+y+z=4$，$x\geqq1,\ y\geqq1,\ z\geqq1$，$pqr=\dfrac1{xyz}$<br>"
         r"[$V$ の最小] 相加平均と相乗平均の関係より　$xyz\leqq\left(\dfrac{x+y+z}3\right)^3=\dfrac{64}{27}$（等号は $x=y=z=\dfrac43$）。よって $pqr\geqq\dfrac{27}{64}$<br>"
         r"[$V$ の最大] $x=1+\alpha,\ y=1+\beta,\ z=1+\gamma$ とおくと $\alpha,\ \beta,\ \gamma\geqq0$，$\alpha+\beta+\gamma=1$ で<br>"
         r"$xyz=1+(\alpha+\beta+\gamma)+(\alpha\beta+\beta\gamma+\gamma\alpha)+\alpha\beta\gamma\geqq2$<br>"
         r"（等号は $\alpha,\ \beta,\ \gamma$ のうち2つが $0$ のとき、たとえば $x=2,\ y=z=1$）。よって $pqr\leqq\dfrac12$<br>"
         r"以上より　最大値 $\boldsymbol{\dfrac12\cdot\dfrac{\sqrt2}{12}=\dfrac{\sqrt2}{24}}$（$p=\dfrac12,\ q=r=1$ など），最小値 $\boldsymbol{\dfrac{27}{64}\cdot\dfrac{\sqrt2}{12}=\dfrac{9\sqrt2}{256}}$（$p=q=r=\dfrac34$）",
  "note": r"$V$ が最大になるのは、Q，R がそれぞれ頂点 B，C に一致し、P が辺 OA の中点のときなど（平面 PQR は辺 BC と G を含む平面）。端点まで動ける（$x\geqq1$）という範囲の条件が最大値を決めており、範囲を忘れると最大値が求まらない。",
  "ex": r"1辺の長さが $1$ の正四面体 OABC の辺 OA，OB，OC 上（端点 O を除く）に点 P，Q，R をとる。平面 PQR が $\overrightarrow{\mathrm{OK}}=\dfrac15(\overrightarrow{\mathrm{OA}}+\overrightarrow{\mathrm{OB}}+\overrightarrow{\mathrm{OC}})$ で定まる点 K を通るとき、四面体 OPQR の体積の最大値と最小値を求めよ。",
  "exa": r"最大値 $\dfrac{\sqrt2}{36}$，最小値 $\dfrac{9\sqrt2}{500}$"},
 {"lv": 4, "title": "立方体の切り口の面積の最大",
  "q": _fig_cube_hex() + r"立方体 $K:\ 0\leqq x\leqq1,\ 0\leqq y\leqq1,\ 0\leqq z\leqq1$ を平面 $x+y+z=t$（$0<t<3$）で切ったときの切り口の面積を $S(t)$ とする。<br>(1) $S(t)$ を $t$ で表せ。　(2) $S(t)$ の最大値を求めよ。<br>（図は $t=\dfrac32$ のときの切り口）",
  "hint": r"平面 $x+y+z=t$ の $x,\ y,\ z\geqq0$ の部分は正三角形。そこから、立方体からはみ出す部分（$x>1$ など）を除く。はみ出す部分も正三角形になる。$t$ と $3-t$ で対称になることにも注目する。",
  "sol": r"平面 $x+y+z=t$ の $x\geqq0,\ y\geqq0,\ z\geqq0$ の部分を $T(t)$ とする。$T(t)$ は3点 $(t,\ 0,\ 0)$，$(0,\ t,\ 0)$，$(0,\ 0,\ t)$ を頂点とする1辺 $\sqrt2t$ の正三角形で、面積は $\dfrac{\sqrt3}4(\sqrt2t)^2=\dfrac{\sqrt3}2t^2$。<br>"
         r"[1] $0<t\leqq1$ のとき　$T(t)$ はすべて $K$ に含まれるから　$S(t)=\dfrac{\sqrt3}2t^2$<br>"
         r"[2] $1\leqq t\leqq2$ のとき　$T(t)$ のうち $x>1$ の部分は、$x'=x-1$ とおくと $x'+y+z=t-1$（$x'>0,\ y\geqq0,\ z\geqq0$）となり、1辺 $\sqrt2(t-1)$ の正三角形（面積 $\dfrac{\sqrt3}2(t-1)^2$）である。$y>1$，$z>1$ の部分も同様で、$t\leqq2$ よりこれら3つの部分は重ならない（たとえば $x>1$ かつ $y>1$ なら $x+y+z>2$）。よって<br>"
         r"$S(t)=\dfrac{\sqrt3}2\{t^2-3(t-1)^2\}=\dfrac{\sqrt3}2(-2t^2+6t-3)$<br>"
         r"[3] $2\leqq t<3$ のとき　点 $(x,\ y,\ z)$ を点 $(1-x,\ 1-y,\ 1-z)$ に移す対称移動で、$K$ は自分自身に、平面 $x+y+z=t$ は平面 $x+y+z=3-t$ に移るから　$S(t)=S(3-t)=\dfrac{\sqrt3}2(3-t)^2$<br>"
         r"以上より　$\boldsymbol{S(t)=\dfrac{\sqrt3}2t^2\ (0<t\leqq1),\ \ \dfrac{\sqrt3}2(-2t^2+6t-3)\ (1\leqq t\leqq2),\ \ \dfrac{\sqrt3}2(3-t)^2\ (2\leqq t<3)}$<br>"
         r"(2) $1\leqq t\leqq2$ では $-2t^2+6t-3=-2\left(t-\dfrac32\right)^2+\dfrac32$ であり、$0<t\leqq1$，$2\leqq t<3$ では $S(t)\leqq\dfrac{\sqrt3}2$ である。よって $S(t)$ は $t=\dfrac32$ のとき最大値 $\boldsymbol{\dfrac{3\sqrt3}4}$ をとる。",
  "note": r"$t=\dfrac32$ のとき、切り口は立方体の中心を通る1辺 $\dfrac{\sqrt2}2$ の正六角形である。別解として、切り口を $xy$ 平面に正射影した図形の面積を、2平面のなす角 $\theta$（$\cos\theta=\dfrac1{\sqrt3}$）の $\cos\theta$ で割ってもよい：$t=\dfrac32$ では正射影の面積が $1-2\cdot\dfrac18=\dfrac34$ で、$\dfrac34\div\dfrac1{\sqrt3}=\dfrac{3\sqrt3}4$。",
  "ex": r"同じ立方体 $K$ を平面 $x+y+z=t$（$1\leqq t\leqq2$）で切った切り口の周の長さは、$t$ によらず一定であることを示し、その値を求めよ。",
  "exa": r"六角形の辺は $\sqrt2(t-1)$ と $\sqrt2(2-t)$ が3本ずつで、周は $3\sqrt2(t-1)+3\sqrt2(2-t)=3\sqrt2$（一定）"},
]})

# ---------------------------------------------------------------- 節8
def _fig_kite_tet():
    xx = yy = 2 / math.sqrt(3)
    h = math.sqrt(1 - (xx * xx + yy * yy) / 4)
    P = {"A": (xx / 2, 0, 0), "B": (-xx / 2, 0, 0), "C": (0, yy / 2, h), "D": (0, -yy / 2, h), "M": (0, 0, 0), "N": (0, 0, h)}
    return fig3d(P, faces=["ABC", "ABD", "ACD", "BCD"], thin=[("C", "M"), ("D", "M")], hl=[("M", "N")], dots=["M", "N"],
                 lab=["A", "B", "C", "D", "M", "N"], off={"M": (0, 10), "N": (0, -9)}, W=170, H=130, az=-150, el=16)


def _fig_two_balls():
    r2 = (2 - math.sqrt(3)) / 2
    w = math.sqrt(2)
    it = [("pg", [(0, 0), (w, 0), (w, 1), (0, 1)], "#f6f6f6"),
          ("l", (0, 0), (w, 0)), ("l", (w, 0), (w, 1)), ("l", (w, 1), (0, 1)), ("l", (0, 1), (0, 0)),
          ("l", (0, 0), (w, 1), _HID, True, 0.8),
          ("c", (w / 2, 0.5), 0.5, "#dde7f6"), ("c", (w * (1 - r2), 1 - r2), r2, "#f3dccf"),
          ("t", (w / 2, 0.5), "1/2", 0, 0, 9), ("t", (0, 0), "O", -7, 5, 10)]
    return fig2d(it, (-0.08, w + 0.08, -0.08, 1.08), W=170, H=125)


SEC.append({"title": "空間図形の総合問題（最難関）",
"base": r"""・対称性を見抜いて座標や基準のベクトルを設定する（中点・重心・外心を基準にとる）<br>
・評価の道具：単位ベクトル $\vec{e}$ に対して $|\vec{v}|\geqq\vec{e}\cdot\vec{v}$，三角不等式，相加平均と相乗平均，$|\vec{a}+\vec{b}+\cdots|^2\geqq0$<br>
・最大・最小は「一部を固定して最適化し、最後に固定したものを動かす」。等号が同時に成り立つかを必ず確かめる<br>
・空間の4つのベクトルは必ず1次従属：同じ平面上にない3つのベクトルで、残りの1つが表せる""",
"items": [
 {"lv": 5, "title": "4辺の長さが1の四面体の体積の最大",
  "q": _fig_kite_tet() + r"四面体 ABCD において $\mathrm{AC}=\mathrm{AD}=\mathrm{BC}=\mathrm{BD}=1$ とし、$\mathrm{AB}=x$，$\mathrm{CD}=y$ とする。$x,\ y$ が変化するとき、四面体 ABCD の体積 $V$ の最大値と、そのときの $x,\ y$ の値を求めよ。",
  "hint": r"AB の中点 M，CD の中点 N をとる。$\mathrm{CA}=\mathrm{CB}$，$\mathrm{DA}=\mathrm{DB}$ から $\mathrm{AB}\perp\mathrm{CM}$，$\mathrm{AB}\perp\mathrm{DM}$ で、AB は平面 CDM に垂直。四面体を平面 CDM で2つに分けると、体積が $x,\ y$ で表せる。2変数は $x^2+y^2$ を固定して考える。",
  "sol": r"AB の中点を M，CD の中点を N とする。$\triangle\mathrm{CAB}$，$\triangle\mathrm{DAB}$ は二等辺三角形だから $\mathrm{CM}\perp\mathrm{AB}$，$\mathrm{DM}\perp\mathrm{AB}$ で、AB は平面 CDM に垂直である。<br>"
         r"$\mathrm{CM}=\mathrm{DM}=\sqrt{1-\dfrac{x^2}4}$ で、$\triangle\mathrm{MCD}$ は二等辺三角形だから $\mathrm{MN}\perp\mathrm{CD}$，$\mathrm{MN}=\sqrt{1-\dfrac{x^2}4-\dfrac{y^2}4}$<br>"
         r"四面体を平面 CDM で2つの三角錐 A-MCD，B-MCD に分けると、高さはそれぞれ $\mathrm{AM}=\mathrm{BM}=\dfrac x2$ だから<br>"
         r"$V=\dfrac13\cdot\triangle\mathrm{MCD}\cdot\mathrm{AB}=\dfrac13\cdot\dfrac12y\sqrt{1-\dfrac{x^2+y^2}4}\cdot x=\dfrac{xy}6\sqrt{1-\dfrac{x^2+y^2}4}$<br>"
         r"四面体ができる条件は $x>0,\ y>0,\ x^2+y^2<4$ である（$\mathrm{MN}>0$ が必要。逆にこのとき、$h=\sqrt{1-\frac{x^2+y^2}4}$ として $\mathrm{A}\left(\frac x2,\ 0,\ 0\right)$，$\mathrm{B}\left(-\frac x2,\ 0,\ 0\right)$，$\mathrm{C}\left(0,\ \frac y2,\ h\right)$，$\mathrm{D}\left(0,\ -\frac y2,\ h\right)$ が条件を満たす）。<br>"
         r"$s=x^2+y^2$（$0<s<4$）とおく。$xy\leqq\dfrac{x^2+y^2}2=\dfrac s2$（等号は $x=y$）より<br>"
         r"$V^2=\dfrac{x^2y^2}{36}\left(1-\dfrac s4\right)\leqq\dfrac{s^2}{144}\cdot\dfrac{4-s}4=\dfrac{s^2(4-s)}{576}$<br>"
         r"$f(s)=4s^2-s^3$ とすると $f'(s)=8s-3s^2=s(8-3s)$ で、$0<s<4$ において $f(s)$ は $s=\dfrac83$ で増加から減少に変わり、最大値 $f\left(\dfrac83\right)=\dfrac{64}9\cdot\dfrac43=\dfrac{256}{27}$ をとる。<br>"
         r"よって　$V^2\leqq\dfrac{256}{27\cdot576}=\dfrac4{243}$，$V\leqq\dfrac2{9\sqrt3}=\dfrac{2\sqrt3}{27}$<br>"
         r"等号は $x=y$ かつ $x^2+y^2=\dfrac83$，すなわち $x=y=\dfrac2{\sqrt3}$ のとき成り立つ。<br>"
         r"以上より　$\boldsymbol{x=y=\dfrac{2\sqrt3}3}$ のとき最大値 $\boldsymbol{\dfrac{2\sqrt3}{27}}$",
  "note": r"$f(s)$ の最大は相加平均と相乗平均の関係 $s\cdot s\cdot(8-2s)\leqq\left(\dfrac{s+s+(8-2s)}3\right)^3$ でも示せる。一般に、ねじれの位置にある2辺の長さが $a,\ b$，距離が $d$，なす角が $\theta$ の四面体の体積は $\dfrac16abd\sin\theta$ であり、この問題は $a=x,\ b=y,\ d=\mathrm{MN},\ \theta=90^\circ$ の場合にあたる。",
  "ex": r"四面体 ABCD において $\mathrm{AC}=\mathrm{AD}=\mathrm{BC}=\mathrm{BD}=1$，$\mathrm{AB}=x$，$\mathrm{CD}=y$ とする。$x+y=2$ を満たしながら $x,\ y$ が変化するとき、体積の最大値を求めよ。",
  "exa": r"$x=y=1$（正四面体）のとき最大値 $\dfrac{\sqrt2}{12}$"},
 {"lv": 5, "title": "正四面体の4頂点までの距離の和の最小",
  "q": r"1辺の長さが $1$ の正四面体 ABCD と空間内の点 P について、$\mathrm{PA}+\mathrm{PB}+\mathrm{PC}+\mathrm{PD}$ の最小値を求めよ。",
  "hint": r"正四面体の重心 O から各頂点へ向かう単位ベクトルの和は $\vec{0}$ になる。各 $\mathrm{PA}=|\overrightarrow{\mathrm{PA}}|$ を、その単位ベクトルとの内積で下から評価すると、P に関する項がちょうど打ち消し合う。",
  "sol": r"正四面体の重心を O とし、$\vec{a}=\overrightarrow{\mathrm{OA}}$，$\vec{b}=\overrightarrow{\mathrm{OB}}$，$\vec{c}=\overrightarrow{\mathrm{OC}}$，$\vec{d}=\overrightarrow{\mathrm{OD}}$ とおく。重心の定義から $\vec{a}+\vec{b}+\vec{c}+\vec{d}=\vec{0}$。<br>"
         r"[O から各頂点までの距離] $\triangle\mathrm{BCD}$ の重心を $\mathrm{G_1}$ とすると $\overrightarrow{\mathrm{OG_1}}=\dfrac{\vec{b}+\vec{c}+\vec{d}}3=-\dfrac13\vec{a}$ より、O は線分 $\mathrm{AG_1}$ を $3:1$ に内分する。$\mathrm{AB}=\mathrm{AC}=\mathrm{AD}$ より、A から平面 BCD に下ろした垂線の足は $\triangle\mathrm{BCD}$ の外心、すなわち重心 $\mathrm{G_1}$ で、$\mathrm{G_1B}=\dfrac1{\sqrt3}$ より $\mathrm{AG_1}=\sqrt{1-\dfrac13}=\dfrac{\sqrt6}3$。よって $\mathrm{OA}=\dfrac34\cdot\dfrac{\sqrt6}3=\dfrac{\sqrt6}4$。他の頂点についても同様で、$|\vec{a}|=|\vec{b}|=|\vec{c}|=|\vec{d}|=\dfrac{\sqrt6}4$。これを $R$ とおく。<br>"
         r"[評価] $\vec{e}_1=\dfrac{\vec{a}}R$，$\vec{e}_2=\dfrac{\vec{b}}R$，$\vec{e}_3=\dfrac{\vec{c}}R$，$\vec{e}_4=\dfrac{\vec{d}}R$ は単位ベクトルで、$\vec{e}_1+\vec{e}_2+\vec{e}_3+\vec{e}_4=\vec{0}$。<br>"
         r"$\vec{p}=\overrightarrow{\mathrm{OP}}$ とすると、$|\vec{e}_1|=1$ より　$\mathrm{PA}=|\vec{a}-\vec{p}|\geqq\vec{e}_1\cdot(\vec{a}-\vec{p})=R-\vec{e}_1\cdot\vec{p}$<br>"
         r"B，C，D についても同様の不等式をつくって辺々加えると<br>"
         r"$\mathrm{PA}+\mathrm{PB}+\mathrm{PC}+\mathrm{PD}\geqq4R-(\vec{e}_1+\vec{e}_2+\vec{e}_3+\vec{e}_4)\cdot\vec{p}=4R=\sqrt6$<br>"
         r"P が O に一致するとき $\mathrm{PA}+\mathrm{PB}+\mathrm{PC}+\mathrm{PD}=4R=\sqrt6$ となるから、求める最小値は　$\boldsymbol{\sqrt6}$（P が正四面体の重心のとき）",
  "note": r"$|\vec{v}|\geqq\vec{e}\cdot\vec{v}$ の等号は $\vec{v}$ が $\vec{e}$ と同じ向き（または $\vec{0}$）のときで、4つ同時に成り立つのは P＝O のときに限る。平面で正三角形の頂点までの距離の和が中心で最小になることの空間版である。この方法は「各頂点へ向かう単位ベクトルの和が $\vec{0}$ になる点」があればどんな配置にも使える。",
  "ex": r"1辺の長さが $1$ の正八面体の6個の頂点と、空間内の点 P との距離の和の最小値を求めよ。",
  "exa": r"$3\sqrt2$（P が正八面体の中心のとき。中心から各頂点までの距離は $\dfrac{\sqrt2}2$）"},
 {"lv": 5, "title": "どの2つも等しい角をなす単位ベクトル",
  "q": r"空間内の相異なる4つの単位ベクトル $\vec{a},\ \vec{b},\ \vec{c},\ \vec{d}$ があり、どの2つのなす角も同じ大きさ $\theta$ である。<br>(1) $\cos\theta$ の値を求めよ。<br>(2) 空間内の相異なる5つの単位ベクトルで、どの2つのなす角も等しいものは存在しないことを示せ。",
  "hint": r"$t=\cos\theta$ とおくと、異なる2つの内積はすべて $t$。空間では同じ平面上にない3つのベクトルで任意のベクトルが表せるので、まず $\vec{a},\ \vec{b},\ \vec{c}$ が同じ平面上にないことを示し、$\vec{d}=x\vec{a}+y\vec{b}+z\vec{c}$ とおいて内積をとる。",
  "sol": r"$t=\cos\theta$ とおく。異なる2つのベクトルの内積はすべて $t$ であり、相異なる単位ベクトルだから $t\neq1$。<br>"
         r"(1) [$\vec{a},\ \vec{b},\ \vec{c}$ は同じ平面上にない]　$|\vec{a}+\vec{b}+\vec{c}|^2=3+6t\geqq0$ より $t\geqq-\dfrac12$。よって $-1<t<1$ で、$\vec{a}$ と $\vec{b}$ は平行でない。<br>"
         r"仮に $\vec{c}$ が $\vec{a},\ \vec{b}$ と同じ平面上にあるとすると、$\vec{c}=x\vec{a}+y\vec{b}$ と表せる。$\vec{a},\ \vec{b}$ との内積をとって $t=x+yt$，$t=xt+y$。辺々引いて $(x-y)(1-t)=0$ より $x=y$，よって $x=\dfrac t{1+t}$。<br>"
         r"さらに $1=|\vec{c}|^2=\vec{c}\cdot(x\vec{a}+x\vec{b})=2xt=\dfrac{2t^2}{1+t}$ より $2t^2-t-1=0$，$(2t+1)(t-1)=0$，$t=-\dfrac12$。このとき $|\vec{a}+\vec{b}+\vec{c}|^2=0$ より $\vec{a}+\vec{b}+\vec{c}=\vec{0}$ となるが、$\vec{d}$ との内積をとると $0=3t=-\dfrac32$ となり矛盾する。<br>"
         r"[$\cos\theta$ の決定]　よって $\vec{d}=x\vec{a}+y\vec{b}+z\vec{c}$ と表せる。$\vec{a},\ \vec{b},\ \vec{c}$ との内積をとると<br>"
         r"$t=x+(y+z)t$，$t=y+(z+x)t$，$t=z+(x+y)t$<br>"
         r"第1式と第2式の差から $(x-y)(1-t)=0$ で $x=y$，同様に $y=z$。よって $x=y=z$ で $t=x(1+2t)$。ここで $1+2t=0$ とすると $t=0$ となり不合理だから $x=\dfrac t{1+2t}$。<br>"
         r"$1=|\vec{d}|^2=\vec{d}\cdot(x\vec{a}+x\vec{b}+x\vec{c})=3xt=\dfrac{3t^2}{1+2t}$ より　$3t^2-2t-1=0$，$(3t+1)(t-1)=0$<br>"
         r"$t\neq1$ より　$\boldsymbol{\cos\theta=-\dfrac13}$<br>"
         r"（実際、$\dfrac1{\sqrt3}(1,\ 1,\ 1)$，$\dfrac1{\sqrt3}(1,\ -1,\ -1)$，$\dfrac1{\sqrt3}(-1,\ 1,\ -1)$，$\dfrac1{\sqrt3}(-1,\ -1,\ 1)$ はこの条件を満たす。）<br>"
         r"(2) 相異なる5つの単位ベクトル $\vec{a},\ \vec{b},\ \vec{c},\ \vec{d},\ \vec{e}$ のどの2つのなす角も $\theta$ であったとする。(1) を $\vec{a},\ \vec{b},\ \vec{c},\ \vec{d}$ に用いると $\cos\theta=-\dfrac13$ で<br>"
         r"$|\vec{a}+\vec{b}+\vec{c}+\vec{d}|^2=4+12\cdot\left(-\dfrac13\right)=0$　より　$\vec{d}=-(\vec{a}+\vec{b}+\vec{c})$<br>"
         r"同様に $\vec{a},\ \vec{b},\ \vec{c},\ \vec{e}$ に用いると $\vec{e}=-(\vec{a}+\vec{b}+\vec{c})$。よって $\vec{d}=\vec{e}$ となり、相異なることに矛盾する。　$\blacksquare$",
  "note": r"(1) の4つのベクトルは、正四面体の重心から4頂点へ向かう向きである（$\cos\theta=-\dfrac13$，$\theta\fallingdotseq109.5^\circ$）。平面では、どの2つのなす角も等しい相異なる単位ベクトルは最大3つ（$120^\circ$ ずつ）、空間では最大4つである。",
  "ex": r"空間内の相異なる3つの単位ベクトル $\vec{a},\ \vec{b},\ \vec{c}$ のどの2つのなす角も $\theta$ であるとき、$\cos\theta$ のとり得る値の範囲を求めよ。また、$\vec{a}+\vec{b}+\vec{c}=\vec{0}$ となるのはどのようなときか。",
  "exa": r"$-\dfrac12\leqq\cos\theta<1$；$\cos\theta=-\dfrac12$（$\theta=120^\circ$）のとき"},
 {"lv": 5, "title": "球に内接する四面体の体積の最大",
  "q": r"半径 $1$ の球面上に4点 A，B，C，D がある。四面体 ABCD の体積の最大値を求めよ。",
  "hint": r"まず底面 BCD を含む平面を固定する。その平面と球の中心 O の距離を $h$ とすると、底面は半径 $\sqrt{1-h^2}$ の円に内接し、高さは $1+h$ 以下。円に内接する三角形の面積の最大（正三角形）を示し、最後に $h$ の3次関数を最大化する。",
  "sol": r"[1] 半径 $\rho$ の円に内接する三角形の面積は $\dfrac{3\sqrt3}4\rho^2$ 以下である。<br>"
         r"　三角形の内角を $A,\ B,\ C$ とすると、正弦定理より辺の長さは $2\rho\sin A$ などで、面積は $S=\dfrac12(2\rho\sin A)(2\rho\sin B)\sin C=2\rho^2\sin A\sin B\sin C$。<br>"
         r"　$\sin A\sin B=\dfrac12\{\cos(A-B)-\cos(A+B)\}\leqq\dfrac12(1+\cos C)$ より　$S\leqq\rho^2\sin C(1+\cos C)$<br>"
         r"　$u=\cos C$（$-1<u<1$）とおくと　$\{\sin C(1+\cos C)\}^2=(1-u^2)(1+u)^2=(1-u)(1+u)^3=g(u)$<br>"
         r"　$g'(u)=-(1+u)^3+3(1-u)(1+u)^2=2(1+u)^2(1-2u)$ より、$g(u)$ は $u=\dfrac12$ で最大値 $\dfrac12\cdot\dfrac{27}8=\dfrac{27}{16}$ をとる。よって $S\leqq\dfrac{3\sqrt3}4\rho^2$（等号は $A=B$，$C=60^\circ$，すなわち正三角形のとき）。<br>"
         r"[2] 球の中心を O とし、平面 BCD と O の距離を $h$（$0\leqq h<1$）とする。平面 BCD と球面の交わりは半径 $\sqrt{1-h^2}$ の円で、B，C，D はその上にあるから、[1] より $\triangle\mathrm{BCD}\leqq\dfrac{3\sqrt3}4(1-h^2)$。<br>"
         r"　O から平面 BCD に下ろした垂線の足を H，平面 BCD の単位法線ベクトルを $\vec{n}$ とすると、A と平面 BCD の距離は<br>"
         r"　$|\overrightarrow{\mathrm{HA}}\cdot\vec{n}|=|(\overrightarrow{\mathrm{HO}}+\overrightarrow{\mathrm{OA}})\cdot\vec{n}|\leqq\mathrm{OH}+\mathrm{OA}=h+1$<br>"
         r"　よって　$V\leqq\dfrac13\cdot\dfrac{3\sqrt3}4(1-h^2)(1+h)=\dfrac{\sqrt3}4(1-h)(1+h)^2$<br>"
         r"[3] $k(h)=(1-h)(1+h)^2$ とすると $k'(h)=-(1+h)^2+2(1-h)(1+h)=(1+h)(1-3h)$ より、$0\leqq h<1$ で $k(h)$ は $h=\dfrac13$ のとき最大値 $\dfrac23\cdot\dfrac{16}9=\dfrac{32}{27}$ をとる。よって　$V\leqq\dfrac{\sqrt3}4\cdot\dfrac{32}{27}=\dfrac{8\sqrt3}{27}$<br>"
         r"[4] 等号は、$h=\dfrac13$ で $\triangle\mathrm{BCD}$ が正三角形、A が平面 BCD から最も遠い球面上の点のときに成り立つ。このとき底面の円の半径は $\dfrac{2\sqrt2}3$，$\mathrm{BC}=\sqrt3\cdot\dfrac{2\sqrt2}3=\dfrac{2\sqrt6}3$，高さは $\dfrac43$，$\mathrm{AB}=\sqrt{\left(\dfrac{2\sqrt2}3\right)^2+\left(\dfrac43\right)^2}=\dfrac{2\sqrt6}3$ で、この四面体（正四面体）は実際に存在する。<br>"
         r"以上より、最大値は　$\boldsymbol{\dfrac{8\sqrt3}{27}}$",
  "note": r"「底面を含む平面を固定 → 底面積と高さをそれぞれ最大化 → 固定したもの（$h$）を動かす」という2段階の最大化が要点。[2] の2つの評価の等号が同時に成り立つこと（[4]）を確かめて初めて最大値といえる。",
  "ex": r"半径 $1$ の球面上に4点 A，B，C，D があり、平面 BCD と球の中心の距離が $\dfrac12$ である。四面体 ABCD の体積の最大値を求めよ。",
  "exa": r"$\dfrac{9\sqrt3}{32}$"},
 {"lv": 5, "title": "立方体に入る2つの球の体積の和の最大",
  "q": r"1辺の長さが $1$ の立方体の内部（表面を含む）に、互いに重ならない（接してもよい）2つの球を入れる。2つの球の体積の和の最大値を求めよ。",
  "hint": r"立方体を $0\leqq x,\ y,\ z\leqq1$ とし、半径 $r_1,\ r_2$ の球の中心がとれる範囲を考える。2つの中心の距離の最大値（対角線方向）から「2球が入る」ための $r_1,\ r_2$ の必要十分条件を求め、その条件のもとで $r_1^3+r_2^3$ を最大化する。",
  "sol": _fig_two_balls() + r"立方体を $K:\ 0\leqq x,\ y,\ z\leqq1$ とし、2つの球の半径を $r_1,\ r_2$（$r_1\geqq r_2>0$），中心を $\mathrm{C_1}(x_1,\ y_1,\ z_1)$，$\mathrm{C_2}(x_2,\ y_2,\ z_2)$ とする。<br>"
         r"[1] 入る条件　半径 $r$ の球が $K$ に入る $\iff$ 中心の各座標が $r$ 以上 $1-r$ 以下（$r\leqq\dfrac12$ が必要）。2球が重ならない $\iff$ $\mathrm{C_1C_2}\geqq r_1+r_2$。<br>"
         r"　$r_1\leqq x_1\leqq1-r_1$，$r_2\leqq x_2\leqq1-r_2$ より $|x_1-x_2|\leqq1-r_1-r_2$。$y,\ z$ についても同様だから　$\mathrm{C_1C_2}\leqq\sqrt3(1-r_1-r_2)$<br>"
         r"　よって2球が入るならば $r_1+r_2\leqq\sqrt3(1-r_1-r_2)$，すなわち $r_1+r_2\leqq\dfrac{\sqrt3}{\sqrt3+1}=\dfrac{3-\sqrt3}2$。逆に $r_1\leqq\dfrac12$ かつ $r_1+r_2\leqq\dfrac{3-\sqrt3}2$ ならば、$\mathrm{C_1}(r_1,\ r_1,\ r_1)$，$\mathrm{C_2}(1-r_2,\ 1-r_2,\ 1-r_2)$ とすると $\mathrm{C_1C_2}=\sqrt3(1-r_1-r_2)\geqq r_1+r_2$ で、2球が入る。<br>"
         r"　したがって条件は　$r_2\leqq r_1\leqq\dfrac12$，$r_1+r_2\leqq c$　（$c=\dfrac{3-\sqrt3}2$）<br>"
         r"[2] 最大化　体積の和は $\dfrac{4\pi}3(r_1^3+r_2^3)$。$\sigma=r_1+r_2$ とおくと　$r_1^3+r_2^3=\sigma^3-3\sigma r_1r_2$<br>"
         r"　$\sigma$ を固定すると、$r_1r_2=r_1(\sigma-r_1)$ は $r_1\geqq\dfrac\sigma2$ の範囲で減少するから、$r_1^3+r_2^3$ は $r_1$ が大きいほど大きい。<br>"
         r"　(i) $\sigma\leqq\dfrac12$ のとき　$r_1^3+r_2^3<\sigma^3\leqq\dfrac18$<br>"
         r"　(ii) $\dfrac12<\sigma\leqq c$ のとき　$r_1\leqq\dfrac12$ だから　$r_1^3+r_2^3\leqq\left(\dfrac12\right)^3+\left(\sigma-\dfrac12\right)^3\leqq\dfrac18+\left(c-\dfrac12\right)^3$<br>"
         r"　$c-\dfrac12=\dfrac{2-\sqrt3}2$，$(2-\sqrt3)^3=26-15\sqrt3$ より　$\dfrac18+\left(c-\dfrac12\right)^3=\dfrac{1+26-15\sqrt3}8=\dfrac{27-15\sqrt3}8$<br>"
         r"　これは $\dfrac18$ より大きく、$r_1=\dfrac12$，$r_2=\dfrac{2-\sqrt3}2$ のとき実現する（右図は対角面での切り口）。<br>"
         r"よって求める最大値は　$\dfrac{4\pi}3\cdot\dfrac{27-15\sqrt3}8=\boldsymbol{\dfrac{(9-5\sqrt3)\pi}2}$",
  "note": r"大きい方の球を立方体に内接させ（半径 $\dfrac12$）、小さい球を隅に押し込むのが最大。2球を同じ大きさ（半径 $\dfrac{3-\sqrt3}4$）にすると体積の和はずっと小さい。$\sigma$ を固定すると $r_1^3+r_2^3$ は「差が大きいほど大きい」ことが鍵で、「和が一定なら等しいとき最大」という思い込みは誤りである。",
  "ex": r"1辺の長さが $1$ の立方体の内部（表面を含む）に、互いに重ならない2つの球を入れる。2つの球の表面積の和の最大値を求めよ。",
  "exa": r"$4(2-\sqrt3)\pi$（半径 $\dfrac12$ と $\dfrac{2-\sqrt3}2$ のとき）"},
]})

CH = {"no": 19, "sections": SEC}


def verify():
    from sympy import Matrix, Rational as R, sqrt, symbols, solve, expand, simplify, factor, pi
    import random
    V = lambda *a: Matrix(a)
    d2 = lambda p, q: sum((p[i] - q[i]) ** 2 for i in range(3))
    t, s, u, x, y, z, k = symbols("t s u x y z k", real=True)
    # ---- 節1
    A = V(2, -3, 4)
    assert (A[0], A[1], -A[2]) == (2, -3, -4) and (-A[0], A[1], -A[2]) == (-2, -3, -4) and tuple(-A) == (-2, 3, -4)
    assert expand(2**2 + (t + 3)**2 + 4**2 - (t**2 + 6*t + 29)) == 0 and expand((t - 1)**2 + 2**2 - (t**2 - 2*t + 5)) == 0
    assert solve(d2(V(0, t, 0), A) - d2(V(0, t, 0), V(0, 1, 2)), t) == [-3]
    Pp = V(-3, 1, 2)
    assert (Pp[0], -Pp[1], Pp[2]) == (-3, -1, 2) and (Pp[0], -Pp[1], -Pp[2]) == (-3, -1, -2) and tuple(-Pp) == (3, -1, -2)
    assert solve(d2(V(0, 0, t), Pp) - d2(V(0, 0, t), V(1, 2, 0)), t) == [R(9, 4)]
    a, b = V(1, -2, 2), V(3, 0, -4)
    assert 2*a - b == V(-1, -4, 8) and (2*a - b).norm() == 9 and a / a.norm() == V(R(1, 3), R(-2, 3), R(2, 3))
    assert V(-2, 4, -4) == -2 * a
    a, b = V(2, 2, 1), V(4, 0, -1)
    assert a - 2*b == V(-6, 2, 3) and (a - 2*b).norm() == 7 and -a / a.norm() == V(R(-2, 3), R(-2, 3), R(-1, 3))
    assert V(-6, -6, -3) == -3 * a
    sol = solve(list(s*V(1, 1, 0) + t*V(0, 1, 1) + u*V(1, 0, 1) - V(5, 1, 2)), [s, t, u])
    assert sol == {s: 2, t: -1, u: 3}
    sol = solve(list(s*V(1, 0, 1) + t*V(2, 1, 0) + u*V(0, 1, 1) - V(4, 0, 1)), [s, t, u])
    assert sol == {s: 2, t: 1, u: -1}
    f = expand(((V(2, 3, 1) + t*V(1, 1, 1)).T * (V(2, 3, 1) + t*V(1, 1, 1)))[0])
    assert f == 3*t**2 + 12*t + 14 and expand(3*(t + 2)**2 + 2 - f) == 0 and (V(2, 3, 1) - 2*V(1, 1, 1)) == V(0, 1, -1)
    f = expand(((V(3, -1, 2) + t*V(1, -1, 0)).T * (V(3, -1, 2) + t*V(1, -1, 0)))[0])
    assert expand(2*(t + 2)**2 + 6 - f) == 0
    # ---- 節2
    cosang = lambda p, q: simplify((p.T * q)[0] / (p.norm() * q.norm()))
    assert cosang(V(2, -1, 1), V(1, 1, 2)) == R(1, 2)
    A, B, C = V(1, 2, 3), V(2, 1, 3), V(0, 2, 4)
    assert B - A == V(1, -1, 0) and C - A == V(-1, 0, 1) and cosang(B - A, C - A) == R(-1, 2)
    assert simplify(cosang(V(1, -1, 0), V(1, -2, 2)) - 1/sqrt(2)) == 0
    A, B, C = V(0, 1, 2), V(1, 3, 4), V(-1, 1, 1)
    assert simplify(cosang(B - A, C - A) + 1/sqrt(2)) == 0
    e = V(R(2, 3), R(2, 3), R(1, 3))
    for vec in (V(1, -2, 2), V(2, -1, -2)):
        assert (e.T * vec)[0] == 0
    assert e.norm() == 1
    sol = solve([x - 2*y + 2*z, 2*x - y - 2*z, x**2 + y**2 + z**2 - 1], [x, y, z])
    assert sorted(sol) == sorted([(R(2, 3), R(2, 3), R(1, 3)), (R(-2, 3), R(-2, 3), R(-1, 3))])
    sol = solve([x + y, y + 2*z, x**2 + y**2 + z**2 - 36], [x, y, z])
    assert sorted(sol) == sorted([(4, -4, 2), (-4, 4, -2)])
    area = lambda A, B, C: sqrt(((B - A).T*(B - A))[0]*((C - A).T*(C - A))[0] - ((B - A).T*(C - A))[0]**2) / 2
    assert area(V(1, 0, 0), V(0, 2, 0), V(0, 0, 3)) == R(7, 2) and (V(-1, 2, 0).cross(V(-1, 0, 3))) == V(6, 3, 2)
    assert simplify(area(V(1, 1, 0), V(2, 3, 1), V(0, 2, 3)) - 5*sqrt(2)/2) == 0
    # 正四面体（1辺1）を座標で
    O, A, B, C = V(0, 0, 0), V(1, 0, 0), V(R(1, 2), sqrt(3)/2, 0), V(R(1, 2), sqrt(3)/6, sqrt(R(2, 3)))
    for P_, Q_ in ((O, A), (O, B), (O, C), (A, B), (B, C), (C, A)):
        assert simplify((P_ - Q_).norm() - 1) == 0
    assert simplify((A.T * (C - B))[0]) == 0
    M, N = A / 2, (B + C) / 2
    assert simplify((N - M).norm() - sqrt(2)/2) == 0 and simplify(cosang(N - M, B) - 1/sqrt(2)) == 0
    assert simplify(((N - M).T*A)[0]) == 0 and simplify(((N - M).T*(C - B))[0]) == 0
    O2, A2, B2, C2 = 2*O, 2*A, 2*B, 2*C
    G = (A2 + B2 + C2) / 3
    assert simplify(G.norm() - 2*sqrt(6)/3) == 0 and simplify(cosang(A2, G) - sqrt(6)/3) == 0
    # 球面上の点：数値サンプリング＋端点
    def pab(p, a, b):
        return sum((a[i] - p[i])*(b[i] - p[i]) for i in range(3))
    random.seed(19)
    for (a_, b_, lo, hi, pmax, pmin) in (((1, 2, 4), (1, 2, 0), 0, 12, (-R(1, 3), -R(2, 3), -R(2, 3)), (R(1, 3), R(2, 3), R(2, 3))),
                                         ((3, 1, 2), (1, 1, 2), 3, 15, None, None)):
        vals = []
        for _ in range(20000):
            g = [random.gauss(0, 1) for _ in range(3)]
            nr = math.sqrt(sum(c*c for c in g))
            vals.append(pab([c/nr for c in g], a_, b_))
        assert lo - 1e-9 <= min(vals) < lo + 0.05 and hi - 0.05 < max(vals) <= hi + 1e-9
        if pmax:
            assert pab(pmax, a_, b_) == hi and pab(pmin, a_, b_) == lo and sum(c*c for c in pmax) == 1
        m = [(a_[i] + b_[i]) / 2 for i in range(3)]
        assert sum(c*c for c in m) == 9
    # ---- 節3
    A, B, C = V(1, -2, 3), V(4, 1, -3), V(-2, 4, 3)
    assert (A + 2*B) / 3 == V(3, 0, -1) and (-A + 2*B) / (2 - 1) == V(7, 4, -9) and (A + B + C) / 3 == V(1, 1, 1)
    assert (A + V(7, 4, -9)) / 2 == B
    A, B, C, D = V(2, 0, -1), V(-1, 3, 5), V(3, 1, 0), V(0, -4, 4)
    assert (2*A + B) / 3 == V(1, 1, 1) and (-2*A + B) / (1 - 2) == V(5, -3, -7) and (A + B + C + D) / 4 == V(1, 0, 2)
    def collinear(A, B, Cxy):
        return solve(list(Cxy - A - k*(B - A)), dict=True)
    sol = collinear(V(1, 2, -1), V(3, -1, 1), V(x, y, 5))
    assert sol == [{k: 3, x: 7, y: -7}]
    sol = collinear(V(2, -1, 3), V(0, 1, 4), V(x, -3, y))
    assert sol == [{k: -1, x: 4, y: 2}]
    def coplanar_x(A, B, C, D):
        return solve(list(D - A - s*(B - A) - t*(C - A)), dict=True)
    assert coplanar_x(V(1, 1, 0), V(2, 0, 1), V(0, 1, 2), V(x, 0, 3)) == [{s: 1, t: 1, x: 1}]
    assert coplanar_x(V(0, 1, 2), V(1, 2, 0), V(2, 0, 1), V(x, 2, 2))[0][x] == -1
    n_ = (V(2, 0, 1) - V(1, 1, 0)).cross(V(0, 1, 2) - V(1, 1, 0))
    assert n_ == V(-2, -3, -1) and (n_.T * (V(1, 0, 3) - V(1, 1, 0)))[0] == 0
    # 交点：ランダムな a, b, c で厳密に解く
    random.seed(3)
    for _ in range(5):
        a, b, c = [V(*[random.randint(-5, 5) for _ in range(3)]) for _ in range(3)]
        if Matrix.hstack(a, b, c).det() == 0:
            continue
        def meet(dirv, P0, P1, P2):   # 直線 O + k*dirv と平面 P0P1P2 の交点の k
            return solve(list(k*dirv - P0 - s*(P1 - P0) - t*(P2 - P0)), [k, s, t])[k]
        g = a + b + c
        assert meet(g, a, b, c) == R(1, 3) and meet(g, a + b, a + c, b + c) == R(2, 3) and meet(g, a/2, b/2, c/2) == R(1, 6)
        assert meet(g/3, a/2, 2*b/3, c/3) == R(6, 13) and meet(g/3, a/3, b/2, 3*c/4) == R(9, 19)
    # ---- 節4
    def foot_line(Pt, A, B):
        tt = solve(((A + t*(B - A) - Pt).T * (B - A))[0], t)[0]
        return A + tt*(B - A), tt
    H, tt = foot_line(V(6, 4, 0), V(1, 0, 2), V(3, 1, 0))
    assert tt == 2 and H == V(5, 2, -2) and (H - V(6, 4, 0)).norm() == 3
    assert expand((2*t - 5)**2 + (t - 4)**2 + (2 - 2*t)**2 - 9*(t - 2)**2 - 9) == 0
    H, tt = foot_line(V(1, 0, 5), V(0, 1, 1), V(1, 3, -1))
    assert H == V(-1, -1, 3) and (H - V(1, 0, 5)).norm() == 3
    def foot_plane(Pt, A, B, C):
        Hs = A + s*(B - A) + t*(C - A)
        sol = solve([((Hs - Pt).T*(B - A))[0], ((Hs - Pt).T*(C - A))[0]], [s, t])
        return Hs.subs(sol), sol
    H, sol = foot_plane(V(0, 0, 0), V(1, 0, 0), V(0, 2, 0), V(0, 0, 2))
    assert sol == {s: R(1, 6), t: R(1, 6)} and H == V(R(2, 3), R(1, 3), R(1, 3)) and simplify(H.norm() - sqrt(6)/3) == 0
    assert simplify(3*R(2, 3)/H.norm() - sqrt(6)) == 0 and area(V(1, 0, 0), V(0, 2, 0), V(0, 0, 2)) == sqrt(6)
    H, sol = foot_plane(V(0, 0, 0), V(4, 0, 0), V(0, 2, 0), V(0, 0, 4))
    assert H == V(R(2, 3), R(4, 3), R(2, 3)) and simplify(3*R(16, 3)/H.norm() - 4*sqrt(6)) == 0
    assert simplify(area(V(4, 0, 0), V(0, 2, 0), V(0, 0, 4)) - 4*sqrt(6)) == 0
    # 内積で与えられた四面体：内積を満たす座標で実現
    for a, b, c, Hexp, Vexp in ((V(1, 0, 0), V(0, 1, 0), V(1, 1, sqrt(2)), (1, 1), sqrt(2)/6),
                                (V(2, 0, 0), V(0, 2, 0), V(1, 1, sqrt(2)), (R(1, 2), R(1, 2)), 2*sqrt(2)/3)):
        assert simplify(c.norm() - 2) == 0 and (a.T*b)[0] == 0 and simplify((b.T*c)[0] - b.norm()*2*R(1, 2)) == 0 and simplify((a.T*c)[0] - a.norm()*2*R(1, 2)) == 0
        H, sol = foot_plane(c, V(0, 0, 0), a, b)
        assert (sol[s], sol[t]) == Hexp
        assert simplify(abs(Matrix.hstack(a, b, c).det())/6 - Vexp) == 0
    # ねじれの位置
    for base1, u1, base2, v1, P0, Q0, dmin in ((V(-1, -2, 0), V(1, 1, 0), V(2, -3, -1), V(0, 1, 1), V(1, 0, 0), V(2, -1, 1), sqrt(3)),
                                               (V(0, 0, 0), V(1, 0, 1), V(-3, 0, 3), V(1, 1, 0), V(1, 0, 1), V(-1, 2, 3), 2*sqrt(3))):
        PQ = base2 + t*v1 - base1 - s*u1
        sol = solve([(PQ.T*u1)[0], (PQ.T*v1)[0]], [s, t])
        assert base1 + sol[s]*u1 == P0 and base2 + sol[t]*v1 == Q0 and simplify((Q0 - P0).norm() - dmin) == 0
        b1, b2, uf, vf = ([float(c) for c in w] for w in (base1, base2, u1, v1))
        f2 = lambda ss, tt: sum((b2[m] + tt*vf[m] - b1[m] - ss*uf[m])**2 for m in range(3))
        best = min(f2(i/20, j/20) for i in range(-60, 100) for j in range(-60, 100))
        assert abs(best - float(dmin)**2) < 1e-9
    assert expand((3 - s)**2 + (t - s - 1)**2 + (t - 1)**2 - sum(c**2 for c in (V(2, -3, -1) + t*V(0, 1, 1) - V(-1, -2, 0) - s*V(1, 1, 0)))) == 0
    # 直角四面体（記号 p,q,r で）
    p_, q_, r_ = symbols("p q r", positive=True)
    a, b, c = V(p_, 0, 0), V(0, q_, 0), V(0, 0, r_)
    al, be = symbols("alpha beta")
    Hs = al*a + be*b + (1 - al - be)*c
    sol = solve([(Hs.T*(b - a))[0], (Hs.T*(c - a))[0]], [al, be])
    H = simplify(Hs.subs(sol))
    assert simplify(1/(H.T*H)[0] - (1/p_**2 + 1/q_**2 + 1/r_**2)) == 0
    assert simplify(((H - a).T*(c - b))[0]) == 0 and simplify(((H - b).T*(a - c))[0]) == 0
    Hn = H.subs({p_: 2, q_: 3, r_: 6})
    assert simplify(Hn.norm() - 3*sqrt(14)/7) == 0 and simplify(area(V(2, 0, 0), V(0, 3, 0), V(0, 0, 6)) - 3*sqrt(14)) == 0
    # ---- 節5
    X = V(x, y, z)
    plane = lambda n, A: expand((n.T*(X - A))[0])
    assert plane(V(2, -1, 3), V(1, 2, -1)) == 2*x - y + 3*z + 3
    f = 2*x - y + 3*z + 3
    tt = solve(f.subs({x: 2 + t, y: 1 + t, z: -t}), t)
    assert tt == [3] and (2 + 3, 1 + 3, -3) == (5, 4, -3)
    assert plane(V(1, 2, -2), V(3, 0, -2)) == x + 2*y - 2*z - 7
    f = x + 2*y - 2*z - 7
    tt = solve(f.subs({x: 2 + 2*t, y: 1 + 2*t, z: 1 - 2*t}), t)[0]
    assert (2 + 2*tt, 1 + 2*tt, 1 - 2*tt) == (3, 2, 0)
    def dist_foot(n, d0, Pt):
        val = (n.T*Pt)[0] + d0
        kk = -R(val, (n.T*n)[0])
        return abs(val)/n.norm(), Pt + kk*n
    for A, B, C, Pt, n_exp, d_exp, H_exp in ((V(1, 0, 1), V(2, 1, 0), V(0, 2, 1), V(2, 0, 5), V(2, 1, 3), -5, V(0, -1, 2)),
                                             (V(1, 2, 0), V(0, 1, 1), V(2, 0, 1), V(2, 1, 5), V(1, 2, 3), -5, V(1, -1, 2))):
        n_ = (B - A).cross(C - A)
        g_ = n_ / n_[0] * n_exp[0]
        assert g_ == n_exp and all((n_exp.T*Q)[0] + d_exp == 0 for Q in (A, B, C))
        dd, H = dist_foot(n_exp, d_exp, Pt)
        assert simplify(dd - sqrt(14)) == 0 and H == H_exp
    # 対称点と和の最小（平面を2変数で表して数値探索）
    for n_, d0, A, B, Ap, mn, Pmin in ((V(1, -1, 1), -5, V(1, 2, 3), V(3, 0, 0), V(3, 0, 5), 5, V(3, 0, 2)),
                                        (V(1, 1, 1), -3, V(1, 2, 3), V(4, 0, 1), V(-1, 0, 1), 5, V(2, 0, 1))):
        fA, fB = (n_.T*A)[0] + d0, (n_.T*B)[0] + d0
        assert fA*fB > 0
        assert A - 2*fA/(n_.T*n_)[0]*n_ == Ap and (n_.T*((A + Ap)/2))[0] + d0 == 0
        assert (Ap - B).norm() == mn and (n_.T*Pmin)[0] + d0 == 0 and (A - Pmin).norm() + (Pmin - B).norm() == mn
        e1 = V(1, 1, 0) if n_[2] != 0 else V(0, 0, 1)
        e1 = e1 - (e1.T*n_)[0]/(n_.T*n_)[0]*n_
        e2 = n_.cross(e1)
        best = 1e9
        pf, e1f, e2f, Af, Bf = ([float(c) for c in w] for w in (Pmin, e1, e2, A, B))
        for i in range(-60, 61):
            for j in range(-60, 61):
                Q = [pf[m] + i/20*e1f[m] + j/20*e2f[m] for m in range(3)]
                best = min(best, math.dist(Q, Af) + math.dist(Q, Bf))
        assert abs(best - mn) < 1e-9
    # 直線上の点と2定点
    for u_, A, B, mn, tmin in ((V(1, 2, 2), V(2, 1, -2), V(-2, 8, 2), 3*sqrt(13), R(2, 3)),
                               (V(2, 1, 2), V(1, 2, -2), V(6, -3, 0), 3*sqrt(10), R(1, 3))):
        Pt = t*u_
        fa, fb = expand(((Pt - A).T*(Pt - A))[0]), expand(((Pt - B).T*(Pt - B))[0])
        assert expand(fa - 9*t**2 - 9) == 0
        ca, cb = [float(fa.coeff(t, m)) for m in range(3)], [float(fb.coeff(t, m)) for m in range(3)]
        F = lambda tv: math.sqrt(ca[0] + ca[1]*tv + ca[2]*tv*tv) + math.sqrt(cb[0] + cb[1]*tv + cb[2]*tv*tv)
        vals = [(F(i/1000), i/1000) for i in range(-2000, 4000)]
        assert abs(min(vals)[0] - float(mn)) < 1e-6 and abs(min(vals)[1] - float(tmin)) < 2e-3
        assert simplify(sqrt(fa.subs(t, tmin)) + sqrt(fb.subs(t, tmin)) - mn) == 0
    assert expand((t + 2)**2 + (2*t - 8)**2 + (2*t - 2)**2 - 9*(t - 2)**2 - 36) == 0
    # ---- 節6
    sph = lambda c, r2: expand((x - c[0])**2 + (y - c[1])**2 + (z - c[2])**2 - r2)
    assert sph((2, -1, 3), 9) == x**2 + y**2 + z**2 - 4*x + 2*y - 6*z + 5
    assert sph((-1, 0, 2), 9) == x**2 + y**2 + z**2 + 2*x - 4*z - 4
    assert (V(3, -1, 2) + V(-1, 3, 0))/2 == V(1, 1, 1) and (V(3, -1, 2) - V(-1, 3, 0)).norm() == 6
    assert (V(0, 2, -1) + V(4, -2, 1))/2 == V(2, 0, 0) and (V(0, 2, -1) - V(4, -2, 1)).norm() == 6
    assert V(-2, 0, 1).norm()**2 == 5
    a_, b_, c_, d_ = symbols("a_ b_ c_ d_")
    for pts, ans in (((V(0, 0, 0), V(3, 1, 0), V(0, 3, 1), V(2, 0, -2)), (-2, -4, 2, 0)),
                     ((V(0, 0, 0), V(4, 0, 0), V(3, 1, 2), V(1, 0, 3)), (-4, 2, -2, 0))):
        assert Matrix.hstack(pts[1] - pts[0], pts[2] - pts[0], pts[3] - pts[0]).det() != 0
        eqs = [(P_.T*P_)[0] + a_*P_[0] + b_*P_[1] + c_*P_[2] + d_ for P_ in pts]
        sol = solve(eqs, [a_, b_, c_, d_])
        assert (sol[a_], sol[b_], sol[c_], sol[d_]) == ans
    assert expand(10 + 3*a_ + b_ - ((V(3, 1, 0).T*V(3, 1, 0))[0] + 3*a_ + b_)) == 0
    assert sph((1, 2, -1), 6) == x**2 + y**2 + z**2 - 2*x - 4*y + 2*z and sph((2, -1, 1), 6) == x**2 + y**2 + z**2 - 4*x + 2*y - 2*z
    r_ = symbols("r_", positive=True)
    assert sorted(solve((1 - r_)**2 + (2 - r_)**2 + (5 - r_)**2 - r_**2, r_)) == [3, 5]
    assert sorted(solve((1 - r_)**2 + (-4 + r_)**2 + (5 - r_)**2 - r_**2, r_)) == [3, 7]
    assert expand((1 - r_)**2 + (2 - r_)**2 + (5 - r_)**2 - r_**2 - (2*r_**2 - 16*r_ + 30)) == 0
    # 球面と平面
    for Cc, rr, n_, d0, Hexp, rad, tang in ((V(1, -2, 3), 5, V(2, -1, 2), -1, V(-1, -1, 1), 4, (5, -25)),
                                           (V(-2, 1, 2), 3, V(1, 1, 1), -4, V(-1, 2, 3), sqrt(6), None)):
        val = (n_.T*Cc)[0] + d0
        dd = abs(val)/n_.norm()
        H = Cc - val/(n_.T*n_)[0]*n_
        assert H == Hexp and simplify(sqrt(rr**2 - dd**2) - rad) == 0
        ee = symbols("ee")
        sol = solve(((n_.T*Cc)[0] + ee)**2 - rr**2*(n_.T*n_)[0], ee)
        if tang:
            assert sorted(sol) == sorted(tang)
        else:
            assert sorted(sol, key=lambda q: float(q)) == sorted([-1 - 3*sqrt(3), -1 + 3*sqrt(3)], key=lambda q: float(q))
    assert sph((1, -2, 3), 25) == x**2 + y**2 + z**2 - 2*x + 4*y - 6*z - 11 and sph((-2, 1, 2), 9) == x**2 + y**2 + z**2 + 4*x - 2*y - 4*z
    # 球面と直線、接点の円
    for rr2, base, dv, sols, pts in ((9, V(4, 2, 3), V(1, 0, 1), [-5, -2], (V(2, 2, 1), V(-1, 2, -2))),
                                     (25, V(5, 4, -2), V(1, 0, -1), [-5, -2], (V(3, 4, 0), V(0, 4, 3)))):
        Pt = base + t*dv
        assert sorted(solve((Pt.T*Pt)[0] - rr2, t)) == sols
        assert {tuple(Pt.subs(t, q)) for q in sols} == {tuple(q) for q in pts} and simplify((pts[0] - pts[1]).norm() - 3*sqrt(2)) == 0
    for rr2, h, zt, rad in ((9, 5, R(9, 5), R(12, 5)), (25, 13, R(25, 13), R(60, 13))):
        assert sqrt(rr2 - zt**2) == rad
        for th in range(0, 360, 30):
            Tt = (float(rad)*math.cos(math.radians(th)), float(rad)*math.sin(math.radians(th)), float(zt))
            assert abs(sum(c*c for c in Tt) - rr2) < 1e-9
            assert abs(Tt[0]**2 + Tt[1]**2 + Tt[2]*(Tt[2] - h)) < 1e-9
    # 影：格子点で「線分 LQ が球と交わる」と不等式を比較
    def seg_hits(Lp, Q):
        Cc = (0, 0, 1)
        d = [Q[i] - Lp[i] for i in range(3)]
        w = [Lp[i] - Cc[i] for i in range(3)]
        dd = sum(c*c for c in d)
        sp = max(0.0, min(1.0, -sum(w[i]*d[i] for i in range(3))/dd))
        return sum((w[i] + sp*d[i])**2 for i in range(3)) <= 1
    for Lp, ineq, rng, ax in (((1, 0, 3), lambda X, Y: (X + 1)**2/4 + Y**2/3, (-3, 1), 0),
                              ((0, 2, 4), lambda X, Y: X**2/2 + (Y + 1)**2/3, (-1 - math.sqrt(3), -1 + math.sqrt(3)), 1)):
        ext = []
        for i in range(-90, 61):
            for j in range(-90, 61):
                X, Y = i/20, j/20
                val = ineq(X, Y)
                if abs(val - 1) > 1e-6:
                    assert seg_hits(Lp, (X, Y, 0)) == (val < 1)
                if val <= 1:
                    ext.append((X, Y)[ax])
        assert abs(min(ext) - rng[0]) < 0.06 and abs(max(ext) - rng[1]) < 0.06
    XX, YY, ss = symbols("XX YY ss")
    mm = (XX - 1)**2 + YY**2 + 9
    assert expand((V(1, 0, 2) + ss*V(XX - 1, YY, -3)).T*(V(1, 0, 2) + ss*V(XX - 1, YY, -3)))[0] == expand(mm*ss**2 + 2*(XX - 7)*ss + 5)
    assert expand(-((XX - 7)**2 - 4*mm) - (3*XX**2 + 6*XX + 4*YY**2 - 9)) == 0
    mm2 = XX**2 + (YY - 2)**2 + 16
    kk2 = expand((V(0, 2, 3).T*V(XX, YY - 2, -4))[0])
    assert expand(-(kk2**2 - mm2*12) - 4*(3*XX**2 + 2*(YY + 1)**2 - 6)) == 0
    # ---- 節7
    def vol(A, B, C, D):
        return abs(Matrix.hstack(B - A, C - A, D - A).det()) / 6
    A, B, C, D = V(1, 1, 1), V(3, 1, 2), V(1, 3, 0), V(0, -4, -3)
    assert vol(A, B, C, D) == 4 and Matrix.hstack(B - A, C - A, D - A).det() == -24 and area(A, B, C) == sqrt(6)
    assert all(Q[0] - Q[1] - 2*Q[2] + 2 == 0 for Q in (A, B, C)) and D[0] - D[1] - 2*D[2] + 2 == 12
    assert simplify(R(1, 3)*sqrt(6)*12/sqrt(6) - 4) == 0
    assert vol(V(1, 2, 0), V(0, 1, 1), V(2, 0, 1), V(3, 3, 2)) == R(5, 3)
    for (pp, qq, rr), (e1, e2, e3), Vv in (((4, 3, 2), (25, 20, 13), 8), ((1, 2, 3), (5, 10, 13), 2)):
        A1, B1, C1, D1 = V(0, 0, 0), V(pp, qq, 0), V(pp, 0, rr), V(0, qq, rr)
        dist2 = lambda P_, Q_: ((P_ - Q_).T*(P_ - Q_))[0]
        assert dist2(A1, B1) == dist2(C1, D1) == e1 and dist2(A1, C1) == dist2(B1, D1) == e2 and dist2(A1, D1) == dist2(B1, C1) == e3
        assert vol(A1, B1, C1, D1) == Vv == R(pp*qq*rr, 3)
    assert 5**2 == 25 and (2*sqrt(5))**2 == 20 and sqrt(13)**2 == 13
    # 正四面体を切る平面
    O, A, B, C = V(0, 0, 0), V(1, 0, 0), V(R(1, 2), sqrt(3)/2, 0), V(R(1, 2), sqrt(3)/6, sqrt(R(2, 3)))
    V0 = vol(O, A, B, C)
    assert simplify(V0 - sqrt(2)/12) == 0
    pp, qq = symbols("pp qq", positive=True)
    for c4, lo, hi in ((4, R(27, 64), R(1, 2)), (5, R(27, 125), R(1, 3))):
        rr = 1/(c4 - 1/pp - 1/qq)
        G = (A + B + C)/c4
        Pp, Qq, Rr = pp*A, qq*B, rr*C
        assert simplify(Matrix.hstack(Qq - Pp, Rr - Pp, G - Pp).det()) == 0
        mn, mx = 10, 0
        Ng = 240
        for i in range(Ng + 1):
          for j in range(Ng + 1 - i):
            al, be = i/Ng, j/Ng
            ga = 1 - al - be
            sc = c4 - 3
            X_, Y_, Z_ = 1 + sc*al, 1 + sc*be, 1 + sc*ga
            pr = 1/(X_*Y_*Z_)
            mn, mx = min(mn, pr), max(mx, pr)
            assert abs(X_ + Y_ + Z_ - c4) < 1e-12
        assert lo - 1e-12 <= mn < lo + 1e-3 and hi - 1e-3 < mx <= hi + 1e-12
        assert R(1, 1)/(R(c4, 3)**3) == lo and R(1, 1)/(c4 - 2) == hi
    assert simplify(R(1, 2)*sqrt(2)/12 - sqrt(2)/24) == 0 and simplify(R(27, 64)*sqrt(2)/12 - 9*sqrt(2)/256) == 0
    assert simplify(R(1, 3)*sqrt(2)/12 - sqrt(2)/36) == 0 and simplify(R(27, 125)*sqrt(2)/12 - 9*sqrt(2)/500) == 0
    # 立方体の切り口（数値で多角形を作って面積・周長）
    def section(tv):
        cube = [(i, j, k_) for i in (0, 1) for j in (0, 1) for k_ in (0, 1)]
        pts = []
        for P_ in cube:
            for Q_ in cube:
                if P_ < Q_ and sum(abs(P_[m] - Q_[m]) for m in range(3)) == 1:
                    fp, fq = sum(P_) - tv, sum(Q_) - tv
                    if fp == 0:
                        pts.append(P_)
                    elif fp*fq < 0:
                        lam = fp/(fp - fq)
                        pts.append(tuple(P_[m] + lam*(Q_[m] - P_[m]) for m in range(3)))
        pts = list(set(tuple(round(c, 12) for c in q) for q in pts))
        cx = [sum(q[m] for q in pts)/len(pts) for m in range(3)]
        e1 = (1/math.sqrt(2), -1/math.sqrt(2), 0)
        e2 = (1/math.sqrt(6), 1/math.sqrt(6), -2/math.sqrt(6))
        pts.sort(key=lambda q: math.atan2(sum((q[m] - cx[m])*e2[m] for m in range(3)), sum((q[m] - cx[m])*e1[m] for m in range(3))))
        uv = [(sum(q[m]*e1[m] for m in range(3)), sum(q[m]*e2[m] for m in range(3))) for q in pts]
        ar = abs(sum(uv[i][0]*uv[i - 1][1] - uv[i - 1][0]*uv[i][1] for i in range(len(uv))))/2
        per = sum(math.dist(pts[i], pts[i - 1]) for i in range(len(pts)))
        return ar, per
    Sf = lambda tv: math.sqrt(3)/2*(tv**2 if tv <= 1 else (-2*tv**2 + 6*tv - 3 if tv <= 2 else (3 - tv)**2))
    best = 0
    for i in range(1, 300):
        tv = i/100
        ar, per = section(tv)
        assert abs(ar - Sf(tv)) < 1e-9
        if 1 <= tv <= 2:
            assert abs(per - 3*math.sqrt(2)) < 1e-9
        best = max(best, ar)
    assert abs(best - 3*math.sqrt(3)/4) < 1e-12 and abs(section(1.5)[0] - 3*math.sqrt(3)/4) < 1e-12
    # ---- 節8
    xs_, ys_ = symbols("xs_ ys_", positive=True)
    hh = sqrt(1 - (xs_**2 + ys_**2)/4)
    A, B, C, D = V(xs_/2, 0, 0), V(-xs_/2, 0, 0), V(0, ys_/2, hh), V(0, -ys_/2, hh)
    for P_, Q_ in ((A, C), (A, D), (B, C), (B, D)):
        assert simplify(((P_ - Q_).T*(P_ - Q_))[0] - 1) == 0
    Vf = simplify(Matrix.hstack(B - A, C - A, D - A).det()/6)
    assert simplify(Vf**2 - (xs_*ys_/6)**2*(1 - (xs_**2 + ys_**2)/4)) == 0
    Vn = lambda a, b: a*b/6*math.sqrt(max(0.0, 1 - (a*a + b*b)/4))
    best = max((Vn(i/400, j/400), i, j) for i in range(1, 800) for j in range(1, 800) if i*i + j*j < 4*160000)
    assert abs(best[0] - 2*math.sqrt(3)/27) < 1e-6 and abs(best[1]/400 - 2/math.sqrt(3)) < 0.01
    assert simplify(abs(Vf.subs({xs_: 2/sqrt(3), ys_: 2/sqrt(3)})) - 2*sqrt(3)/27) == 0
    assert R(256, 27*576) == R(4, 243) and simplify(sqrt(R(4, 243)) - 2*sqrt(3)/27) == 0
    best = max(Vn(i/1000, 2 - i/1000) for i in range(1, 2000))
    assert abs(best - math.sqrt(2)/12) < 1e-9
    # 距離の和の最小
    T4 = [V(1, 1, 1), V(1, -1, -1), V(-1, 1, -1), V(-1, -1, 1)]
    sc = 1/(T4[0] - T4[1]).norm()
    T4 = [sc*q for q in T4]
    assert all(simplify((T4[i] - T4[j]).norm() - 1) == 0 for i in range(4) for j in range(i))
    assert simplify(T4[0].norm() - sqrt(6)/4) == 0 and sum(T4, V(0, 0, 0)) == V(0, 0, 0)
    oc = 1/sqrt(2)
    O6 = [V(oc, 0, 0), V(-oc, 0, 0), V(0, oc, 0), V(0, -oc, 0), V(0, 0, oc), V(0, 0, -oc)]
    assert simplify((O6[0] - O6[2]).norm() - 1) == 0
    for pts, mn in ((T4, math.sqrt(6)), (O6, 3*math.sqrt(2))):
        fp = [[float(c) for c in q] for q in pts]
        F = lambda P_: sum(math.dist(P_, q) for q in fp)
        assert abs(F((0, 0, 0)) - mn) < 1e-12
        random.seed(7)
        for _ in range(3000):
            P_ = [random.uniform(-1.5, 1.5) for _ in range(3)]
            assert F(P_) >= mn - 1e-12
        cur = [0.9, -0.7, 0.4]
        step = 0.5
        while step > 1e-7:
            moved = False
            for dlt in ((step, 0, 0), (-step, 0, 0), (0, step, 0), (0, -step, 0), (0, 0, step), (0, 0, -step)):
                cand = [cur[m] + dlt[m] for m in range(3)]
                if F(cand) < F(cur):
                    cur, moved = cand, True
            if not moved:
                step /= 2
        assert abs(F(cur) - mn) < 1e-9
    # 等角の単位ベクトル
    U = [q/sqrt(3) for q in (V(1, 1, 1), V(1, -1, -1), V(-1, 1, -1), V(-1, -1, 1))]
    assert all((U[i].T*U[i])[0] == 1 for i in range(4)) and all((U[i].T*U[j])[0] == R(-1, 3) for i in range(4) for j in range(i))
    tt_ = symbols("tt_")
    assert sorted(solve(2*tt_**2 - tt_ - 1, tt_)) == [R(-1, 2), 1] and sorted(solve(3*tt_**2 - 2*tt_ - 1, tt_)) == [R(-1, 3), 1]
    xx_ = symbols("xx_")
    sol = solve([xx_ + 2*xx_*tt_ - tt_, 3*xx_*tt_ - 1], [xx_, tt_], dict=True)
    assert {so[tt_] for so in sol} == {R(-1, 3), 1}
    Gm = Matrix(4, 4, lambda i, j: 1 if i == j else tt_)
    assert factor(Gm.det()) == factor((1 - tt_)**3*(1 + 3*tt_))
    Gm3 = Matrix(3, 3, lambda i, j: 1 if i == j else tt_)
    assert factor(Gm3.det()) == factor((1 - tt_)**2*(1 + 2*tt_))
    for tv in (-0.5, -0.3, 0, 0.4, 0.99):
        rr = math.sqrt((1 - tv)*2/3)
        hz = math.sqrt(1 - rr*rr)
        vs = [(rr*math.cos(2*math.pi*i/3), rr*math.sin(2*math.pi*i/3), hz) for i in range(3)]
        for i in range(3):
            for j in range(i):
                assert abs(sum(vs[i][m]*vs[j][m] for m in range(3)) - tv) < 1e-12
    # 球に内接する四面体
    uu, hv = symbols("uu hv")
    g_ = (1 - uu)*(1 + uu)**3
    assert factor(expand(g_.diff(uu) - 2*(1 + uu)**2*(1 - 2*uu))) == 0 and g_.subs(uu, R(1, 2)) == R(27, 16)
    k_ = (1 - hv)*(1 + hv)**2
    assert expand(k_.diff(hv) - (1 + hv)*(1 - 3*hv)) == 0 and k_.subs(hv, R(1, 3)) == R(32, 27)
    assert simplify(sqrt(3)/4*R(32, 27) - 8*sqrt(3)/27) == 0 and simplify(vol(*U) - 8*sqrt(3)/27) == 0
    assert simplify(sqrt(3)/4*k_.subs(hv, R(1, 2)) - 9*sqrt(3)/32) == 0
    def volf(P4):
        a, b, c, d = P4
        u1 = [b[m] - a[m] for m in range(3)]; u2 = [c[m] - a[m] for m in range(3)]; u3 = [d[m] - a[m] for m in range(3)]
        return abs(u1[0]*(u2[1]*u3[2] - u2[2]*u3[1]) - u1[1]*(u2[0]*u3[2] - u2[2]*u3[0]) + u1[2]*(u2[0]*u3[1] - u2[1]*u3[0]))/6
    def rsph():
        g = [random.gauss(0, 1) for _ in range(3)]
        n = math.sqrt(sum(c*c for c in g))
        return [c/n for c in g]
    random.seed(11)
    vmax = max(volf([rsph() for _ in range(4)]) for _ in range(30000))
    assert vmax <= 8*math.sqrt(3)/27 + 1e-12 and vmax > 0.9*8*math.sqrt(3)/27
    rc = math.sqrt(3)/2
    tri = [(rc*math.cos(2*math.pi*i/3), rc*math.sin(2*math.pi*i/3), -0.5) for i in range(3)]
    assert abs(volf(tri + [(0, 0, 1)]) - 9*math.sqrt(3)/32) < 1e-12
    for _ in range(20000):
        th = [random.uniform(0, 2*math.pi) for _ in range(3)]
        P4 = [(rc*math.cos(q), rc*math.sin(q), -0.5) for q in th] + [rsph()]
        assert volf(P4) <= 9*math.sqrt(3)/32 + 1e-12
    # 立方体の2球
    cc = (3 - sqrt(3))/2
    assert simplify(sqrt(3)/(sqrt(3) + 1) - cc) == 0 and expand((2 - sqrt(3))**3) == 26 - 15*sqrt(3)
    assert simplify(R(1, 8) + (cc - R(1, 2))**3 - (27 - 15*sqrt(3))/8) == 0
    assert simplify(R(4, 3)*pi*(27 - 15*sqrt(3))/8 - (9 - 5*sqrt(3))*pi/2) == 0
    cf = float(cc)
    best3 = best2 = 0
    N = 600
    for i in range(1, N + 1):
        r1 = 0.5*i/N
        for j in range(0, i + 1):
            r2 = r1*j/i
            if r1 + r2 <= cf + 1e-15:
                best3 = max(best3, r1**3 + r2**3)
                best2 = max(best2, r1**2 + r2**2)
    assert abs(best3 - (27 - 15*math.sqrt(3))/8) < 2e-3 and best3 <= (27 - 15*math.sqrt(3))/8 + 1e-12
    r2s = (2 - math.sqrt(3))/2
    assert abs(math.sqrt(3)*(1 - 0.5 - r2s) - (0.5 + r2s)) < 1e-12
    assert abs(4*math.pi*(0.25 + r2s**2) - 4*(2 - math.sqrt(3))*math.pi) < 1e-12 and abs(4*math.pi*best2 - 4*(2 - math.sqrt(3))*math.pi) < 0.02
    random.seed(5)
    for _ in range(20000):
        r1, r2 = random.uniform(0, 0.5), random.uniform(0, 0.5)
        c1 = [random.uniform(r1, 1 - r1) for _ in range(3)]
        c2 = [random.uniform(r2, 1 - r2) for _ in range(3)]
        if r1 + r2 < 1:
            assert math.dist(c1, c2) <= math.sqrt(3)*(1 - r1 - r2) + 1e-12
    # ---- 例題数と難易度の配分
    items = [it for sec in SEC for it in sec["items"]]
    cnt = {lv: sum(1 for it in items if it["lv"] == lv) for lv in range(1, 6)}
    assert 4 <= len(SEC) <= 9 and 32 <= len(items) <= 38, len(items)
    assert cnt == {1: 7, 2: 10, 3: 10, 4: 6, 5: 5}, cnt
    for sec in SEC:
        lvs = [it["lv"] for it in sec["items"]]
        assert lvs == sorted(lvs), sec["title"]
        for it in sec["items"]:
            for key in ("title", "q", "hint", "sol", "ex", "exa"):
                assert it.get(key), (it["title"], key)
                assert "$$" not in it[key]
