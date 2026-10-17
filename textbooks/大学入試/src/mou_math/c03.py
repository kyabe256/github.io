"""第3章 図形と計量（数学I）　担当 M03
節ごとに SEC.append(...)。図（SVG）の座標は下の作図用関数で計算する。最後に CH と verify。"""
import math

# ================================================================ 作図用の小さな道具
def _n(v):
    s = f"{v:.1f}"
    return "0.0" if s == "-0.0" else s


class _Fig:
    def __init__(self, w, h):
        self.w, self.h, self.e = w, h, []

    def L(self, p, q, dash=False, sw=1.2, col="#222"):
        d = ' stroke-dasharray="3,2"' if dash else ""
        self.e.append(f'<line x1="{_n(p[0])}" y1="{_n(p[1])}" x2="{_n(q[0])}" y2="{_n(q[1])}" stroke="{col}" stroke-width="{sw}"{d}/>')

    def PL(self, pts, close=True, fill="none", dash=False, sw=1.2, col="#222"):
        d = ' stroke-dasharray="3,2"' if dash else ""
        tag = "polygon" if close else "polyline"
        pp = " ".join(f"{_n(x)},{_n(y)}" for x, y in pts)
        self.e.append(f'<{tag} points="{pp}" fill="{fill}" stroke="{col}" stroke-width="{sw}" stroke-linejoin="round"{d}/>')

    def C(self, c, r, fill="none", dash=False, sw=1.2, col="#222"):
        d = ' stroke-dasharray="3,2"' if dash else ""
        self.e.append(f'<circle cx="{_n(c[0])}" cy="{_n(c[1])}" r="{_n(r)}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{d}/>')

    def E(self, c, rx, ry, dash=False, sw=1.2, col="#222"):
        d = ' stroke-dasharray="3,2"' if dash else ""
        self.e.append(f'<ellipse cx="{_n(c[0])}" cy="{_n(c[1])}" rx="{_n(rx)}" ry="{_n(ry)}" fill="none" stroke="{col}" stroke-width="{sw}"{d}/>')

    def path(self, d, fill="none", dash=False, sw=1.2, col="#222"):
        dd = ' stroke-dasharray="3,2"' if dash else ""
        self.e.append(f'<path d="{d}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{dd}/>')

    def dot(self, p, r=1.8, col="#222"):
        self.e.append(f'<circle cx="{_n(p[0])}" cy="{_n(p[1])}" r="{r}" fill="{col}"/>')

    def T(self, p, s, dx=0, dy=0, size=11, it=False, anchor="middle", col="#222"):
        st = ' font-style="italic" font-family="serif"' if it else ""
        self.e.append(f'<text x="{_n(p[0] + dx)}" y="{_n(p[1] + dy + size * 0.36)}" font-size="{size}" text-anchor="{anchor}" fill="{col}"{st}>{s}</text>')

    def right(self, v, p, q, s=6):
        u1, u2 = _unit(v, p), _unit(v, q)
        a = (v[0] + s * u1[0], v[1] + s * u1[1])
        b = (a[0] + s * u2[0], a[1] + s * u2[1])
        c = (v[0] + s * u2[0], v[1] + s * u2[1])
        self.PL([a, b, c], close=False, sw=0.8)

    def arc(self, v, p, q, r=12, label=None, lr=None, size=10, it=False):
        u1, u2 = _unit(v, p), _unit(v, q)
        a = (v[0] + r * u1[0], v[1] + r * u1[1])
        b = (v[0] + r * u2[0], v[1] + r * u2[1])
        sweep = 1 if u1[0] * u2[1] - u1[1] * u2[0] > 0 else 0
        self.path(f"M{_n(a[0])},{_n(a[1])} A{_n(r)},{_n(r)} 0 0 {sweep} {_n(b[0])},{_n(b[1])}", sw=0.8)
        if label:
            m = _unit((0, 0), (u1[0] + u2[0], u1[1] + u2[1]))
            rr = lr if lr else r + 9
            self.T((v[0] + rr * m[0], v[1] + rr * m[1]), label, size=size, it=it)

    def svg(self):
        return (f'<svg class="fig" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'xmlns="http://www.w3.org/2000/svg">' + "".join(self.e) + "</svg>")


def _unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    l = math.hypot(dx, dy)
    return (dx / l, dy / l)


def _mid(p, q, t=0.5):
    return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)


def _proj(ox, oy, s, k=0.5, ang=35):
    """斜投影：空間の点 (x, y, z) → 図の座標。x 右、y 奥、z 上。
    戻り値 (P, view)：view は見る人の方向（面の表裏＝辺の見え隠れの判定に使う）。"""
    ca, sa = math.cos(math.radians(ang)) * k, math.sin(math.radians(ang)) * k
    return (lambda x, y, z: (ox + s * (x + ca * y), oy - s * (z + sa * y))), (ca, -1.0, sa)


def _sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def _cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def _dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def _solid(f, P, view, V, faces, sw=1.2, col="#222"):
    """凸多面体の辺を描く。両側の面がともに裏向きの辺は破線。V: 名前→座標, faces: 名前の列。"""
    cen = tuple(sum(V[k][i] for k in V) / len(V) for i in range(3))
    edges = {}
    for fc in faces:
        n = _cross(_sub(V[fc[1]], V[fc[0]]), _sub(V[fc[2]], V[fc[0]]))
        m = tuple(sum(V[k][i] for k in fc) / len(fc) for i in range(3))
        if _dot(n, _sub(m, cen)) < 0:
            n = tuple(-a for a in n)
        vis = _dot(n, view) > 1e-9
        for i in range(len(fc)):
            e = tuple(sorted((fc[i], fc[(i + 1) % len(fc)])))
            edges.setdefault(e, []).append(vis)
    for (a, b), vs in sorted(edges.items(), key=lambda kv: any(kv[1])):
        f.L(P(*V[a]), P(*V[b]), dash=not any(vs), sw=sw, col=col)


def _vlabels(f, P, V, names, d=9, size=11, extra=None):
    """頂点名を、投影図の重心から外向きに d px 離して書く。"""
    pts = {k: P(*V[k]) for k in names}
    cx = sum(p[0] for p in pts.values()) / len(pts); cy = sum(p[1] for p in pts.values()) / len(pts)
    for k, p in pts.items():
        u = _unit((cx, cy), p)
        dx, dy = (extra or {}).get(k, (0, 0))
        f.T(p, k, u[0] * d + dx, u[1] * d + dy, size=size)


# ---------------------------------------------------------------- 図：節1
def _fig_c1():  # 直角三角形 ABC（C=90°, AB=4, BC=3）
    s, ox, oy = 27, 18, 100
    T = lambda x, y: (ox + s * x, oy - s * y)
    r7 = math.sqrt(7)
    A, C, B = T(0, 0), T(r7, 0), T(r7, 3)
    f = _Fig(118, 116)
    f.PL([A, C, B])
    f.right(C, A, B)
    f.T(A, "A", -8, 6); f.T(C, "C", 7, 7); f.T(B, "B", 7, -5)
    f.T(_mid(A, B), "4", -8, -7); f.T(_mid(C, B), "3", 8, 0)
    return f.svg()


def _fig_tower():  # 2地点からの仰角
    s, ox, oy = 100, 18, 118
    T = lambda x, y: (ox + s * x, oy - s * y)
    r3 = math.sqrt(3)
    A, B, Q, P = T(0, 0), T(r3 - 1, 0), T(r3, 0), T(r3, 1)
    f = _Fig(214, 138)
    f.L(T(-0.08, 0), T(r3 + 0.12, 0))
    f.L(Q, P, sw=2.2)
    f.L(A, P, sw=0.9); f.L(B, P, sw=0.9)
    f.arc(A, Q, P, r=22, label="30°", lr=33, size=9)
    f.arc(B, Q, P, r=15, label="45°", lr=26, size=9)
    f.right(Q, A, P, s=6)
    for p, t, dx, dy in ((A, "A", 0, 9), (B, "B", 0, 9), (Q, "Q", 0, 9), (P, "P", 0, -9)):
        f.dot(p); f.T(p, t, dx, dy)
    f.T(_mid(A, B), "20 m", 0, 10, size=10)
    f.T(_mid(Q, P), "h", 9, 0, it=True)
    return f.svg()


def _fig_15():  # 15°の三角比
    s, ox, oy = 47, 14, 66
    r3 = math.sqrt(3)
    T = lambda x, y: (ox + s * (x + r3 + 2), oy - s * y)
    C, A, B, D = T(0, 0), T(0, 1), T(-r3, 0), T(-r3 - 2, 0)
    f = _Fig(214, 90)
    f.PL([D, C, A]); f.L(B, A)
    f.right(C, B, A, s=6)
    f.arc(B, C, A, r=16, label="30°", lr=26, size=9)
    f.arc(D, C, A, r=34, label="15°", lr=44, size=9)
    f.T(D, "D", -2, 9); f.T(B, "B", 0, 9); f.T(C, "C", 3, 9); f.T(A, "A", 0, -9)
    f.T(_mid(D, B), "2", 0, 8, size=10); f.T(_mid(B, A), "2", -7, -10, size=10)
    f.T(_mid(C, A), "1", 7, 0, size=10)
    return f.svg()


SEC = []

# ---------------------------------------------------------------- 節1
SEC.append({"title": "鋭角の三角比",
"base": r"""・直角三角形で、鋭角 $\theta$ の対辺を $y$、隣辺を $x$、斜辺を $r$ とすると　$\sin\theta=\dfrac{y}{r}$，$\cos\theta=\dfrac{x}{r}$，$\tan\theta=\dfrac{y}{x}$<br>
・相互関係：$\tan\theta=\dfrac{\sin\theta}{\cos\theta}$，$\sin^2\theta+\cos^2\theta=1$，$1+\tan^2\theta=\dfrac{1}{\cos^2\theta}$<br>
・余角の公式：$\sin(90^\circ-\theta)=\cos\theta$，$\cos(90^\circ-\theta)=\sin\theta$，$\tan(90^\circ-\theta)=\dfrac{1}{\tan\theta}$<br>
・$30^\circ,\ 45^\circ,\ 60^\circ$ の三角比は、辺の比が $1:1:\sqrt2$，$1:\sqrt3:2$ の直角三角形から読み取る。""",
"items": [
 {"lv": 1, "title": "辺の長さから三角比を求める",
  "q": _fig_c1() + r"$\angle\mathrm{C}=90^\circ$ の直角三角形 $\mathrm{ABC}$ において、$\mathrm{AB}=4$，$\mathrm{BC}=3$ のとき、$\sin A$，$\cos A$，$\tan A$ の値を求めよ。",
  "hint": r"まず三平方の定理で残りの辺 $\mathrm{AC}$ を求める。角 $A$ から見て、斜辺は $\mathrm{AB}$、対辺は $\mathrm{BC}$、隣辺は $\mathrm{AC}$ である。",
  "sol": r"三平方の定理より　$\mathrm{AC}=\sqrt{\mathrm{AB}^2-\mathrm{BC}^2}=\sqrt{16-9}=\sqrt7$<br>"
         r"よって　$\sin A=\dfrac{\mathrm{BC}}{\mathrm{AB}}=\boldsymbol{\dfrac34}$，$\cos A=\dfrac{\mathrm{AC}}{\mathrm{AB}}=\boldsymbol{\dfrac{\sqrt7}{4}}$，$\tan A=\dfrac{\mathrm{BC}}{\mathrm{AC}}=\dfrac{3}{\sqrt7}=\boldsymbol{\dfrac{3\sqrt7}{7}}$",
  "note": r"三角比は直角三角形の<b>辺の比</b>なので、三角形の大きさによらず角だけで決まる。$\sin^2A+\cos^2A=\dfrac{9}{16}+\dfrac{7}{16}=1$ となることで検算できる。",
  "ex": r"$\angle\mathrm{B}=90^\circ$ の直角三角形 $\mathrm{ABC}$ において、$\mathrm{AB}=2$，$\mathrm{BC}=\sqrt5$ のとき、$\sin C$，$\cos C$，$\tan C$ の値を求めよ。",
  "exa": r"$\sin C=\dfrac23$，$\cos C=\dfrac{\sqrt5}{3}$，$\tan C=\dfrac{2\sqrt5}{5}$"},
 {"lv": 1, "title": "相互関係による三角比の決定（鋭角）",
  "q": r"$\theta$ は鋭角とする。<br>(1) $\cos\theta=\dfrac25$ のとき、$\sin\theta$，$\tan\theta$ の値を求めよ。<br>(2) $\tan\theta=3$ のとき、$\cos\theta$，$\sin\theta$ の値を求めよ。",
  "hint": r"(1) は $\sin^2\theta+\cos^2\theta=1$ を使う。鋭角なので $\sin\theta>0$。(2) は $\tan\theta$ から $\cos\theta$ が直接出る $1+\tan^2\theta=\dfrac{1}{\cos^2\theta}$ を使い、$\sin\theta=\tan\theta\cos\theta$ とする。",
  "sol": r"(1) $\sin^2\theta=1-\cos^2\theta=1-\dfrac{4}{25}=\dfrac{21}{25}$。$\sin\theta>0$ より　$\sin\theta=\boldsymbol{\dfrac{\sqrt{21}}{5}}$<br>"
         r"$\tan\theta=\dfrac{\sin\theta}{\cos\theta}=\dfrac{\sqrt{21}}{5}\div\dfrac25=\boldsymbol{\dfrac{\sqrt{21}}{2}}$<br>"
         r"(2) $\dfrac{1}{\cos^2\theta}=1+\tan^2\theta=10$ より $\cos^2\theta=\dfrac{1}{10}$。$\cos\theta>0$ より　$\cos\theta=\dfrac{1}{\sqrt{10}}=\boldsymbol{\dfrac{\sqrt{10}}{10}}$<br>"
         r"$\sin\theta=\tan\theta\cos\theta=3\cdot\dfrac{\sqrt{10}}{10}=\boldsymbol{\dfrac{3\sqrt{10}}{10}}$",
  "note": r"(2) は、底辺 $1$、高さ $3$ の直角三角形をかいて斜辺 $\sqrt{10}$ を求めてもよい。鋭角なら図による方法が速いが、$0^\circ\sim180^\circ$ に拡張すると符号の判断が必要になる（次の節）。",
  "ex": r"$\theta$ は鋭角とする。(1) $\sin\theta=\dfrac23$ のとき、$\cos\theta$，$\tan\theta$ の値を求めよ。(2) $\tan\theta=\dfrac12$ のとき、$\cos\theta$，$\sin\theta$ の値を求めよ。",
  "exa": r"(1) $\cos\theta=\dfrac{\sqrt5}{3}$，$\tan\theta=\dfrac{2\sqrt5}{5}$　(2) $\cos\theta=\dfrac{2\sqrt5}{5}$，$\sin\theta=\dfrac{\sqrt5}{5}$"},
 {"lv": 2, "title": "余角の公式を使う式の値",
  "q": r"次の式の値を求めよ。<br>(1) $\sin25^\circ\cos65^\circ+\cos25^\circ\sin65^\circ$　　(2) $\tan10^\circ\tan20^\circ\tan70^\circ\tan80^\circ$<br>(3) $\triangle\mathrm{ABC}$ において　$\sin\dfrac{A+B}{2}-\cos\dfrac{C}{2}$",
  "hint": r"$65^\circ=90^\circ-25^\circ$ のように和が $90^\circ$ になる角の組を見つけ、余角の公式で角をそろえる。(3) は $A+B+C=180^\circ$ を使う。",
  "sol": r"(1) $\cos65^\circ=\cos(90^\circ-25^\circ)=\sin25^\circ$，$\sin65^\circ=\sin(90^\circ-25^\circ)=\cos25^\circ$ だから<br>"
         r"　与式 $=\sin^225^\circ+\cos^225^\circ=\boldsymbol{1}$<br>"
         r"(2) $\tan70^\circ=\tan(90^\circ-20^\circ)=\dfrac{1}{\tan20^\circ}$，$\tan80^\circ=\dfrac{1}{\tan10^\circ}$ だから<br>"
         r"　与式 $=\tan10^\circ\tan20^\circ\cdot\dfrac{1}{\tan20^\circ}\cdot\dfrac{1}{\tan10^\circ}=\boldsymbol{1}$<br>"
         r"(3) $A+B=180^\circ-C$ より $\dfrac{A+B}{2}=90^\circ-\dfrac{C}{2}$。$\dfrac C2$ は鋭角だから　$\sin\dfrac{A+B}{2}=\sin\left(90^\circ-\dfrac C2\right)=\cos\dfrac C2$<br>"
         r"　よって　与式 $=\boldsymbol{0}$",
  "note": r"$\tan\theta\tan(90^\circ-\theta)=1$，$\sin^2\theta+\sin^2(90^\circ-\theta)=1$ は頻出の形。三角形の内角の問題では、$A+B+C=180^\circ$ から余角・補角の関係を作るのが定石である。",
  "ex": r"次の式の値を求めよ。(1) $\cos^215^\circ+\cos^235^\circ+\cos^255^\circ+\cos^275^\circ$　(2) $\dfrac{\sin40^\circ}{\cos50^\circ}-\tan40^\circ\tan50^\circ$",
  "exa": r"(1) $2$　(2) $0$"},
 {"lv": 2, "title": "測量（2地点からの仰角）",
  "q": _fig_tower() + r"水平な地面に垂直に立つ塔 $\mathrm{PQ}$（$\mathrm{Q}$ は根元）がある。$\mathrm{Q}$ を通る直線上に、$\mathrm{Q}$ から遠い順に2地点 $\mathrm{A}$，$\mathrm{B}$ があり、$\mathrm{AB}=20\,\mathrm{m}$ である。$\mathrm{A}$，$\mathrm{B}$ から塔の先端 $\mathrm{P}$ を見上げた角（仰角）がそれぞれ $30^\circ$，$45^\circ$ のとき、塔の高さを求めよ。ただし、目の高さは考えない。",
  "hint": r"高さを $h$ とおき、2つの直角三角形 $\mathrm{PAQ}$，$\mathrm{PBQ}$ で水平距離 $\mathrm{AQ}$，$\mathrm{BQ}$ を $h$ で表す。その差が $\mathrm{AB}$ である。",
  "sol": r"塔の高さを $h\,\mathrm{m}$ とする。<br>直角三角形 $\mathrm{PBQ}$ で　$\mathrm{BQ}=\dfrac{h}{\tan45^\circ}=h$，直角三角形 $\mathrm{PAQ}$ で　$\mathrm{AQ}=\dfrac{h}{\tan30^\circ}=\sqrt3h$<br>"
         r"$\mathrm{AQ}-\mathrm{BQ}=\mathrm{AB}$ より　$(\sqrt3-1)h=20$<br>"
         r"$h=\dfrac{20}{\sqrt3-1}=\dfrac{20(\sqrt3+1)}{(\sqrt3-1)(\sqrt3+1)}=10(\sqrt3+1)$<br>"
         r"よって、塔の高さは　$\boldsymbol{10(\sqrt3+1)\,\mathrm{m}}$（約 $27.3\,\mathrm{m}$）",
  "note": r"$\triangle\mathrm{PAB}$ で $\angle\mathrm{APB}=45^\circ-30^\circ=15^\circ$ だから、正弦定理で $\mathrm{PB}$ を求めてから $h=\mathrm{PB}\sin45^\circ$ としてもよい。その場合は $\sin15^\circ$ の値が必要になる（この節の最後の例題）。",
  "ex": r"例題と同じ状況で、$\mathrm{A}$，$\mathrm{B}$ からの仰角がそれぞれ $30^\circ$，$60^\circ$、$\mathrm{AB}=30\,\mathrm{m}$ のとき、塔の高さを求めよ。",
  "exa": r"$15\sqrt3\,\mathrm{m}$"},
 {"lv": 3, "title": "図形を利用して 15° の三角比を求める",
  "q": _fig_15() + r"$\angle\mathrm{C}=90^\circ$，$\angle\mathrm{B}=30^\circ$，$\mathrm{AC}=1$ の直角三角形 $\mathrm{ABC}$ がある。辺 $\mathrm{CB}$ の $\mathrm{B}$ の側の延長上に $\mathrm{BD}=\mathrm{BA}$ となる点 $\mathrm{D}$ をとる。これを利用して、$\tan15^\circ$，$\sin15^\circ$，$\cos15^\circ$ の値を求めよ。",
  "hint": r"$\mathrm{BD}=\mathrm{BA}$ から $\triangle\mathrm{ABD}$ は二等辺三角形。外角の性質で $\angle\mathrm{ADB}=15^\circ$ が分かるので、直角三角形 $\mathrm{ACD}$ の3辺を求めれば三角比が読める。",
  "sol": r"$\mathrm{AC}=1$，$\angle\mathrm{B}=30^\circ$ より　$\mathrm{AB}=2$，$\mathrm{BC}=\sqrt3$<br>"
         r"$\triangle\mathrm{ABD}$ は $\mathrm{BA}=\mathrm{BD}$ の二等辺三角形で、$\angle\mathrm{ABC}$ はその外角だから<br>"
         r"　$\angle\mathrm{BAD}+\angle\mathrm{BDA}=30^\circ$，$\angle\mathrm{BAD}=\angle\mathrm{BDA}$　より　$\angle\mathrm{ADC}=15^\circ$<br>"
         r"$\mathrm{CD}=\mathrm{CB}+\mathrm{BD}=2+\sqrt3$，$\mathrm{AD}^2=\mathrm{AC}^2+\mathrm{CD}^2=1+(7+4\sqrt3)=8+4\sqrt3$<br>"
         r"$\mathrm{AD}=\sqrt{8+2\sqrt{12}}=\sqrt6+\sqrt2$　（$6+2=8$，$6\times2=12$）<br>"
         r"直角三角形 $\mathrm{ACD}$ で $\angle\mathrm{D}=15^\circ$ だから<br>"
         r"$\tan15^\circ=\dfrac{\mathrm{AC}}{\mathrm{CD}}=\dfrac{1}{2+\sqrt3}=\boldsymbol{2-\sqrt3}$，$\sin15^\circ=\dfrac{\mathrm{AC}}{\mathrm{AD}}=\dfrac{1}{\sqrt6+\sqrt2}=\boldsymbol{\dfrac{\sqrt6-\sqrt2}{4}}$<br>"
         r"$\cos15^\circ=\dfrac{\mathrm{CD}}{\mathrm{AD}}=\dfrac{2+\sqrt3}{\sqrt6+\sqrt2}=\dfrac{(2+\sqrt3)(\sqrt6-\sqrt2)}{4}=\boldsymbol{\dfrac{\sqrt6+\sqrt2}{4}}$",
  "note": r"$\angle\mathrm{DAC}=75^\circ$ だから、同じ図から $\sin75^\circ=\cos15^\circ=\dfrac{\sqrt6+\sqrt2}{4}$，$\tan75^\circ=2+\sqrt3$ も得られる。二重根号は $\sqrt{a+b+2\sqrt{ab}}=\sqrt a+\sqrt b$（$a,\ b>0$）ではずす。",
  "ex": r"$\angle\mathrm{C}=90^\circ$，$\mathrm{AC}=\mathrm{BC}=1$ の直角二等辺三角形 $\mathrm{ABC}$ の辺 $\mathrm{CB}$ の $\mathrm{B}$ の側の延長上に、$\mathrm{BD}=\mathrm{BA}$ となる点 $\mathrm{D}$ をとる。これを利用して、$\tan22.5^\circ$，$\cos22.5^\circ$ の値を求めよ。",
  "exa": r"$\tan22.5^\circ=\sqrt2-1$，$\cos22.5^\circ=\dfrac{\sqrt{2+\sqrt2}}{2}$"},
]})

# ---------------------------------------------------------------- 図：節2
def _fig_cnt():  # y = -t^2 + t + 1 (0≦t≦1) と直線 y = a
    sx, sy, ox, oy = 128, 92, 22, 146
    T = lambda t, y: (ox + sx * t, oy - sy * y)
    f = _Fig(214, 160)
    f.L(T(-0.08, 0), T(1.32, 0), sw=0.9); f.L(T(0, -0.06), T(0, 1.5), sw=0.9)
    f.T(T(1.32, 0), "t", 0, 9, it=True); f.T(T(0, 1.5), "y", 8, 2, it=True); f.T(T(0, 0), "O", -7, 7, size=10)
    f.L(T(0, 1.25), T(1.22, 1.25), dash=True, sw=0.7)
    f.L(T(0, 1), T(1.22, 1), dash=True, sw=0.7)
    f.L(T(1, 0), T(1, 1), dash=True, sw=0.7); f.L(T(0.5, 0), T(0.5, 1.25), dash=True, sw=0.7)
    f.PL([T(k / 40, -(k / 40) ** 2 + k / 40 + 1) for k in range(41)], close=False, sw=1.6)
    a = 1.14
    f.L(T(-0.02, a), T(1.24, a), sw=1.0, col="#c0392b")
    f.T(T(1.24, a), "y=a", 3, 0, size=10, it=True, anchor="start", col="#c0392b")
    f.T(T(0, 1.25), "5/4", -3, -1, size=9, anchor="end"); f.T(T(0, 1), "1", -3, 3, size=9, anchor="end")
    f.T(T(0.5, 0), "1/2", 0, 8, size=9); f.T(T(1, 0), "1", 0, 8, size=9)
    for t0 in (0, 1):
        f.dot(T(t0, 1), r=2)
    return f.svg()


# ---------------------------------------------------------------- 節2
SEC.append({"title": "三角比の拡張（0°〜180°）と方程式・不等式",
"base": r"""・原点 $\mathrm{O}$ を中心とする半径 $r$ の半円（$y\geqq0$）上の点 $\mathrm{P}(x,\ y)$ について、$x$ 軸の正の向きと $\mathrm{OP}$ のなす角を $\theta$（$0^\circ\leqq\theta\leqq180^\circ$）とすると　$\sin\theta=\dfrac yr$，$\cos\theta=\dfrac xr$，$\tan\theta=\dfrac yx$（$\theta\neq90^\circ$）<br>
・$0\leqq\sin\theta\leqq1$，$-1\leqq\cos\theta\leqq1$。$\theta$ が鈍角のとき $\cos\theta<0$，$\tan\theta<0$。$\tan\theta$ は直線 $\mathrm{OP}$ の傾きに等しい<br>
・補角の公式：$\sin(180^\circ-\theta)=\sin\theta$，$\cos(180^\circ-\theta)=-\cos\theta$，$\tan(180^\circ-\theta)=-\tan\theta$。相互関係はそのまま成り立つ<br>
・方程式・不等式は単位円（半径 $1$）の上で考える。$\sin\theta=k$ の解は、$0\leqq k<1$ なら2個、$k=1$ なら1個。$\cos\theta=k$（$-1\leqq k\leqq1$）の解は1個""",
"items": [
 {"lv": 1, "title": "鈍角の三角比と補角の公式",
  "q": r"次の値を求めよ。<br>(1) $\sin135^\circ$，$\cos120^\circ$，$\tan150^\circ$　　(2) $\sin^2100^\circ+\sin^2170^\circ$　　(3) $\tan25^\circ\tan115^\circ$",
  "hint": r"(1) は単位円上の点の座標を読む。(2)(3) は補角の公式で鋭角の三角比に直し、さらに余角の公式で角をそろえる。",
  "sol": r"(1) 単位円上で、$135^\circ$，$120^\circ$，$150^\circ$ に対応する点はそれぞれ $\left(-\dfrac{1}{\sqrt2},\ \dfrac{1}{\sqrt2}\right)$，$\left(-\dfrac12,\ \dfrac{\sqrt3}{2}\right)$，$\left(-\dfrac{\sqrt3}{2},\ \dfrac12\right)$ だから<br>"
         r"　$\sin135^\circ=\boldsymbol{\dfrac{\sqrt2}{2}}$，$\cos120^\circ=\boldsymbol{-\dfrac12}$，$\tan150^\circ=\dfrac{1}{2}\div\left(-\dfrac{\sqrt3}{2}\right)=\boldsymbol{-\dfrac{\sqrt3}{3}}$<br>"
         r"(2) $\sin100^\circ=\sin(180^\circ-80^\circ)=\sin80^\circ$，$\sin170^\circ=\sin10^\circ=\sin(90^\circ-80^\circ)=\cos80^\circ$<br>"
         r"　与式 $=\sin^280^\circ+\cos^280^\circ=\boldsymbol{1}$<br>"
         r"(3) $\tan115^\circ=\tan(180^\circ-65^\circ)=-\tan65^\circ=-\tan(90^\circ-25^\circ)=-\dfrac{1}{\tan25^\circ}$<br>"
         r"　与式 $=\tan25^\circ\cdot\left(-\dfrac{1}{\tan25^\circ}\right)=\boldsymbol{-1}$",
  "note": r"補角と余角の公式を組み合わせると $\sin(90^\circ+\theta)=\cos\theta$，$\cos(90^\circ+\theta)=-\sin\theta$，$\tan(90^\circ+\theta)=-\dfrac{1}{\tan\theta}$ も得られる。",
  "ex": r"次の値を求めよ。(1) $\sin150^\circ$，$\cos135^\circ$，$\tan120^\circ$　(2) $\cos^2100^\circ+\cos^2170^\circ$　(3) $\tan40^\circ\tan130^\circ$",
  "exa": r"(1) $\dfrac12$，$-\dfrac{\sqrt2}{2}$，$-\sqrt3$　(2) $1$　(3) $-1$"},
 {"lv": 1, "title": "三角比を含む方程式",
  "q": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、次の方程式を解け。<br>(1) $2\sin\theta=\sqrt3$　　(2) $\sqrt2\cos\theta+1=0$　　(3) $\sqrt3\tan\theta+1=0$",
  "hint": r"単位円上で、(1) は $y$ 座標が $\dfrac{\sqrt3}{2}$ の点、(2) は $x$ 座標が $-\dfrac{1}{\sqrt2}$ の点、(3) は直線 $\mathrm{OP}$ の傾きが $-\dfrac{1}{\sqrt3}$ となる点を探す。",
  "sol": r"(1) $\sin\theta=\dfrac{\sqrt3}{2}$。単位円上で $y$ 座標が $\dfrac{\sqrt3}{2}$ の点は2つあり　$\theta=\boldsymbol{60^\circ,\ 120^\circ}$<br>"
         r"(2) $\cos\theta=-\dfrac{1}{\sqrt2}$。$x$ 座標が $-\dfrac{1}{\sqrt2}$ の点は1つで　$\theta=\boldsymbol{135^\circ}$<br>"
         r"(3) $\tan\theta=-\dfrac{1}{\sqrt3}$。直線 $\mathrm{OP}$ の傾きが $-\dfrac{1}{\sqrt3}$ となるのは　$\theta=\boldsymbol{150^\circ}$",
  "note": r"$\sin\theta=k$（$0<k<1$）の解は $\theta$ と $180^\circ-\theta$ の組で現れる。$\sin\theta=1$ は $\theta=90^\circ$ のみ、$\sin\theta=0$ は $\theta=0^\circ,\ 180^\circ$ の2つ。",
  "ex": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、次の方程式を解け。(1) $2\sin\theta=1$　(2) $2\cos\theta+\sqrt3=0$　(3) $\tan\theta=-\sqrt3$",
  "exa": r"(1) $\theta=30^\circ,\ 150^\circ$　(2) $\theta=150^\circ$　(3) $\theta=120^\circ$"},
 {"lv": 2, "title": "相互関係による三角比の決定（鈍角を含む）",
  "q": r"$0^\circ\leqq\theta\leqq180^\circ$ とする。<br>(1) $\sin\theta=\dfrac13$ のとき、$\cos\theta$，$\tan\theta$ の値を求めよ。<br>(2) $\tan\theta=-2$ のとき、$\cos\theta$，$\sin\theta$ の値を求めよ。",
  "hint": r"(1) $\sin\theta>0$ だけでは $\theta$ が鋭角か鈍角か決まらないので、$\cos\theta$ の符号で場合を分ける。(2) $\tan\theta<0$ から $\theta$ は鈍角と決まり、$\cos\theta<0$ である。",
  "sol": r"(1) $\cos^2\theta=1-\sin^2\theta=\dfrac89$ より　$\cos\theta=\pm\dfrac{2\sqrt2}{3}$<br>"
         r"$\theta$ が鋭角のとき　$\cos\theta=\dfrac{2\sqrt2}{3}$，$\tan\theta=\dfrac13\div\dfrac{2\sqrt2}{3}=\dfrac{\sqrt2}{4}$<br>"
         r"$\theta$ が鈍角のとき　$\cos\theta=-\dfrac{2\sqrt2}{3}$，$\tan\theta=-\dfrac{\sqrt2}{4}$<br>"
         r"よって　$\boldsymbol{\cos\theta=\dfrac{2\sqrt2}{3},\ \tan\theta=\dfrac{\sqrt2}{4}}$　または　$\boldsymbol{\cos\theta=-\dfrac{2\sqrt2}{3},\ \tan\theta=-\dfrac{\sqrt2}{4}}$<br>"
         r"(2) $\dfrac{1}{\cos^2\theta}=1+\tan^2\theta=5$ より $\cos^2\theta=\dfrac15$。$\tan\theta<0$ より $90^\circ<\theta<180^\circ$ だから $\cos\theta<0$<br>"
         r"　$\cos\theta=-\dfrac{1}{\sqrt5}=\boldsymbol{-\dfrac{\sqrt5}{5}}$，$\sin\theta=\tan\theta\cos\theta=(-2)\cdot\left(-\dfrac{\sqrt5}{5}\right)=\boldsymbol{\dfrac{2\sqrt5}{5}}$",
  "note": r"$0^\circ\leqq\theta\leqq180^\circ$ では、$\cos\theta$ や $\tan\theta$ の値から $\theta$ は1つに決まるが、$\sin\theta$ の値からは2つの $\theta$ が対応する。$\sin\theta$ が与えられたときだけ答えが2通りになる。",
  "ex": r"$0^\circ\leqq\theta\leqq180^\circ$ とする。(1) $\sin\theta=\dfrac34$ のとき、$\cos\theta$，$\tan\theta$ の値を求めよ。(2) $\tan\theta=-\dfrac13$ のとき、$\cos\theta$，$\sin\theta$ の値を求めよ。",
  "exa": r"(1) $\cos\theta=\pm\dfrac{\sqrt7}{4}$，$\tan\theta=\pm\dfrac{3\sqrt7}{7}$（複号同順）　(2) $\cos\theta=-\dfrac{3\sqrt{10}}{10}$，$\sin\theta=\dfrac{\sqrt{10}}{10}$"},
 {"lv": 2, "title": "三角比を含む不等式",
  "q": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、次の不等式を解け。<br>(1) $2\sin\theta>1$　　(2) $\tan\theta\geqq-1$　　(3) $2\sin^2\theta+\cos\theta-1>0$",
  "hint": r"まず等号が成り立つ $\theta$ を求め、単位円上でどちら側が不等式を満たすかを見る。(3) は $\sin^2\theta=1-\cos^2\theta$ で $\cos\theta$ だけの2次不等式にする。$\tan\theta$ は $\theta=90^\circ$ で定義されないことに注意。",
  "sol": r"(1) $\sin\theta>\dfrac12$。単位円上で $y$ 座標が $\dfrac12$ より大きい部分だから　$\boldsymbol{30^\circ<\theta<150^\circ}$<br>"
         r"(2) $0^\circ\leqq\theta<90^\circ$ では $\tan\theta\geqq0$ だから常に成り立つ。$90^\circ<\theta\leqq180^\circ$ では、直線 $\mathrm{OP}$ の傾き $\tan\theta$ は $\theta$ が大きいほど大きく、$\tan135^\circ=-1$ だから $135^\circ\leqq\theta\leqq180^\circ$<br>"
         r"　よって　$\boldsymbol{0^\circ\leqq\theta<90^\circ,\ 135^\circ\leqq\theta\leqq180^\circ}$<br>"
         r"(3) $2(1-\cos^2\theta)+\cos\theta-1>0$ より　$2\cos^2\theta-\cos\theta-1<0$，$(2\cos\theta+1)(\cos\theta-1)<0$<br>"
         r"　よって $-\dfrac12<\cos\theta<1$。これを満たす $\theta$ は　$\boldsymbol{0^\circ<\theta<120^\circ}$",
  "note": r"(2) で $\theta=90^\circ$ を含めないこと、(3) で $\cos\theta<1$ から $\theta=0^\circ$ が除かれることに注意する。端の点を含むかどうかは、等号の有無と定義域で1つずつ確認する。",
  "ex": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、次の不等式を解け。(1) $\sqrt2\cos\theta\leqq1$　(2) $\tan\theta<\sqrt3$　(3) $2\cos^2\theta-\sin\theta-1<0$",
  "exa": r"(1) $45^\circ\leqq\theta\leqq180^\circ$　(2) $0^\circ\leqq\theta<60^\circ,\ 90^\circ<\theta\leqq180^\circ$　(3) $30^\circ<\theta<150^\circ$"},
 {"lv": 3, "title": "sinθ+cosθ の値から式の値を求める",
  "q": r"$0^\circ\leqq\theta\leqq180^\circ$ で、$\sin\theta+\cos\theta=\dfrac13$ のとき、次の値を求めよ。<br>(1) $\sin\theta\cos\theta$　　(2) $\sin^3\theta+\cos^3\theta$　　(3) $\sin\theta-\cos\theta$",
  "hint": r"$\sin\theta,\ \cos\theta$ の対称式は、和と積で表せる。(1) は与式を2乗する。(3) は2乗した値から求めるが、<b>符号</b>を $\sin\theta\geqq0$ と (1) の積の符号から決める。",
  "sol": r"(1) 両辺を2乗して　$\sin^2\theta+2\sin\theta\cos\theta+\cos^2\theta=\dfrac19$，$1+2\sin\theta\cos\theta=\dfrac19$　より　$\sin\theta\cos\theta=\boldsymbol{-\dfrac49}$<br>"
         r"(2) $\sin^3\theta+\cos^3\theta=(\sin\theta+\cos\theta)^3-3\sin\theta\cos\theta(\sin\theta+\cos\theta)=\dfrac{1}{27}+3\cdot\dfrac49\cdot\dfrac13=\boldsymbol{\dfrac{13}{27}}$<br>"
         r"(3) $(\sin\theta-\cos\theta)^2=1-2\sin\theta\cos\theta=1+\dfrac89=\dfrac{17}{9}$<br>"
         r"$0^\circ\leqq\theta\leqq180^\circ$ では $\sin\theta\geqq0$ で、$\sin\theta\cos\theta<0$ だから $\sin\theta>0$，$\cos\theta<0$。よって $\sin\theta-\cos\theta>0$ で<br>"
         r"　$\sin\theta-\cos\theta=\boldsymbol{\dfrac{\sqrt{17}}{3}}$",
  "note": r"(1) と (3) を連立すると $\sin\theta=\dfrac{1+\sqrt{17}}{6}$，$\cos\theta=\dfrac{1-\sqrt{17}}{6}$ となり、$\tan\theta=-\dfrac{9+\sqrt{17}}{8}$ も求まる。符号の決定に $\sin\theta\geqq0$ と積の符号を使うのが定石。",
  "ex": r"$0^\circ\leqq\theta\leqq180^\circ$ で $\sin\theta-\cos\theta=\dfrac12$ のとき、$\sin\theta\cos\theta$，$\sin^3\theta-\cos^3\theta$，$\sin\theta+\cos\theta$ の値を求めよ。",
  "exa": r"$\sin\theta\cos\theta=\dfrac38$，$\sin^3\theta-\cos^3\theta=\dfrac{11}{16}$，$\sin\theta+\cos\theta=\dfrac{\sqrt7}{2}$"},
 {"lv": 3, "title": "三角比の2次式の最大・最小",
  "q": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、関数 $y=\sin^2\theta+\cos\theta$ の最大値と最小値、およびそのときの $\theta$ の値を求めよ。",
  "hint": r"$\sin^2\theta=1-\cos^2\theta$ で $\cos\theta$ だけの式にし、$\cos\theta=t$ とおいて2次関数の最大・最小にする。<b>$t$ の変域 $-1\leqq t\leqq1$</b> を必ず書く。",
  "sol": r"$\cos\theta=t$ とおくと、$0^\circ\leqq\theta\leqq180^\circ$ より　$-1\leqq t\leqq1$<br>"
         r"$y=(1-t^2)+t=-\left(t-\dfrac12\right)^2+\dfrac54$<br>"
         r"$-1\leqq t\leqq1$ において、$y$ は $t=\dfrac12$ で最大値 $\dfrac54$、軸から遠い端 $t=-1$ で最小値 $-1$ をとる。<br>"
         r"$t=\dfrac12$ のとき $\theta=60^\circ$，$t=-1$ のとき $\theta=180^\circ$ だから<br>"
         r"　$\boldsymbol{\theta=60^\circ}$ のとき最大値 $\boldsymbol{\dfrac54}$，$\boldsymbol{\theta=180^\circ}$ のとき最小値 $\boldsymbol{-1}$",
  "note": r"$\sin\theta=t$ とおく場合は変域が $0\leqq t\leqq1$ になる。置き換えた文字の変域を $\theta$ の範囲から正しく求めることが要点である。",
  "ex": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、関数 $y=\sin^2\theta-\sqrt3\cos\theta$ の最大値と最小値、およびそのときの $\theta$ の値を求めよ。",
  "exa": r"$\theta=150^\circ$ のとき最大値 $\dfrac74$，$\theta=0^\circ$ のとき最小値 $-\sqrt3$"},
 {"lv": 4, "title": "方程式の解の個数（文字定数を分離する）",
  "q": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、$\theta$ についての方程式 $\cos^2\theta+\sin\theta=a$ の異なる解の個数を、定数 $a$ の値によって分類せよ。",
  "hint": r"$\sin\theta=t$ とおくと $0\leqq t\leqq1$。ただし、<b>$t$ の1つの値に対応する $\theta$ の個数</b>が一定でない（$0\leqq t<1$ なら2個、$t=1$ なら1個）。$y=f(t)$ のグラフと直線 $y=a$ の共有点を、$t=1$ かどうかに注意して数える。",
  "sol": _fig_cnt() + r"$\sin\theta=t$ とおくと $0\leqq t\leqq1$ で、方程式は　$1-t^2+t=a$<br>"
         r"$t$ の値に対応する $\theta$ の個数は　$0\leqq t<1$ のとき2個（$t=0$ なら $\theta=0^\circ,\ 180^\circ$）、$t=1$ のとき1個（$\theta=90^\circ$）<br>"
         r"$f(t)=-t^2+t+1=-\left(t-\dfrac12\right)^2+\dfrac54$ とおくと　$f(0)=f(1)=1$，$f\left(\dfrac12\right)=\dfrac54$<br>"
         r"$y=f(t)$（$0\leqq t\leqq1$）のグラフと直線 $y=a$ の共有点を調べて<br>"
         r"・$a<1$，$\dfrac54<a$ のとき　共有点なし → $0$ 個<br>"
         r"・$a=\dfrac54$ のとき　$t=\dfrac12$ → $\theta=30^\circ,\ 150^\circ$ の $2$ 個<br>"
         r"・$1<a<\dfrac54$ のとき　$0<t<\dfrac12$，$\dfrac12<t<1$ に1つずつ → $2+2=4$ 個<br>"
         r"・$a=1$ のとき　$t=0,\ 1$ → $\theta=0^\circ,\ 180^\circ,\ 90^\circ$ の $3$ 個<br>"
         r"答　$\boldsymbol{a<1,\ \dfrac54<a}$ のとき $\boldsymbol{0}$ 個，$\boldsymbol{a=1}$ のとき $\boldsymbol{3}$ 個，$\boldsymbol{1<a<\dfrac54}$ のとき $\boldsymbol{4}$ 個，$\boldsymbol{a=\dfrac54}$ のとき $\boldsymbol{2}$ 個",
  "note": r"答えるのは $t$ の個数ではなく $\theta$ の個数である。$t=1$（$\theta=90^\circ$）だけ対応する $\theta$ が1個になることが、$a=1$ のとき「3個」という答えを生む。定数 $a$ を右辺に分離してグラフと直線の共有点を見るのが定石。",
  "ex": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、$\theta$ についての方程式 $2\cos^2\theta+3\sin\theta=a$ の異なる解の個数を、定数 $a$ の値によって分類せよ。",
  "exa": r"$a<2,\ \dfrac{25}{8}<a$ のとき $0$ 個，$2\leqq a<3$ のとき $2$ 個，$a=3$ のとき $3$ 個，$3<a<\dfrac{25}{8}$ のとき $4$ 個，$a=\dfrac{25}{8}$ のとき $2$ 個"},
]})

# ---------------------------------------------------------------- 節3
SEC.append({"title": "正弦定理と余弦定理",
"base": r"""・$\triangle\mathrm{ABC}$ で $\mathrm{BC}=a$，$\mathrm{CA}=b$，$\mathrm{AB}=c$，外接円の半径を $R$ とする。<br>
・正弦定理：$\dfrac{a}{\sin A}=\dfrac{b}{\sin B}=\dfrac{c}{\sin C}=2R$。特に　$a:b:c=\sin A:\sin B:\sin C$<br>
・余弦定理：$a^2=b^2+c^2-2bc\cos A$，$\cos A=\dfrac{b^2+c^2-a^2}{2bc}$（他の角も同様）<br>
・使い分け：「2角と1辺」「外接円の半径」→ 正弦定理，「2辺とその間の角」「3辺」→ 余弦定理<br>
・角の大小：$A$ が鋭角 $\iff b^2+c^2>a^2$，直角 $\iff b^2+c^2=a^2$，鈍角 $\iff b^2+c^2<a^2$""",
"items": [
 {"lv": 1, "title": "正弦定理（外接円の半径と辺）",
  "q": r"$\triangle\mathrm{ABC}$ において、$a=6$，$A=45^\circ$，$B=60^\circ$ のとき、外接円の半径 $R$ と $b$ を求めよ。",
  "hint": r"辺 $a$ とその対角 $A$ がそろっているので、正弦定理 $\dfrac{a}{\sin A}=2R$ がすぐ使える。",
  "sol": r"正弦定理より　$2R=\dfrac{a}{\sin A}=\dfrac{6}{\sin45^\circ}=6\sqrt2$　よって　$R=\boldsymbol{3\sqrt2}$<br>"
         r"$b=2R\sin B=6\sqrt2\cdot\dfrac{\sqrt3}{2}=\boldsymbol{3\sqrt6}$",
  "note": r"$C=180^\circ-(45^\circ+60^\circ)=75^\circ$ で、$\sin75^\circ=\dfrac{\sqrt6+\sqrt2}{4}$（3.1 節）を使えば $c=2R\sin C=3+3\sqrt3$ も求まる。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$b=4$，$B=30^\circ$，$C=135^\circ$ のとき、外接円の半径 $R$ と $c$ を求めよ。",
  "exa": r"$R=4$，$c=4\sqrt2$"},
 {"lv": 1, "title": "余弦定理（2辺とその間の角から辺を求める）",
  "q": r"$\triangle\mathrm{ABC}$ において、$b=3$，$c=5$，$A=120^\circ$ のとき、$a$ を求めよ。",
  "hint": r"2辺 $b,\ c$ とその間の角 $A$ が与えられているので、余弦定理 $a^2=b^2+c^2-2bc\cos A$ を使う。$\cos120^\circ<0$ の符号に注意。",
  "sol": r"余弦定理より　$a^2=3^2+5^2-2\cdot3\cdot5\cos120^\circ=9+25-30\cdot\left(-\dfrac12\right)=49$<br>"
         r"$a>0$ より　$a=\boldsymbol{7}$",
  "note": r"$A$ が鈍角のときは $-2bc\cos A>0$ となり、$a^2>b^2+c^2$。鈍角の対辺が最大辺になることと整合している。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$a=4$，$c=3\sqrt2$，$B=45^\circ$ のとき、$b$ を求めよ。",
  "exa": r"$b=\sqrt{10}$"},
 {"lv": 1, "title": "余弦定理（3辺から角を求める）",
  "q": r"$\triangle\mathrm{ABC}$ において、$a=7$，$b=5$，$c=8$ のとき、$A$ を求めよ。",
  "hint": r"3辺が分かっているので、余弦定理を $\cos A=\dfrac{b^2+c^2-a^2}{2bc}$ の形で使う。",
  "sol": r"$\cos A=\dfrac{5^2+8^2-7^2}{2\cdot5\cdot8}=\dfrac{40}{80}=\dfrac12$　　$0^\circ<A<180^\circ$ より　$A=\boldsymbol{60^\circ}$",
  "note": r"$0^\circ<A<180^\circ$ では $\cos A$ の値から $A$ がただ1つに決まる。角を求めるときは、正弦定理（$\sin$ の値からは2通り）より余弦定理のほうが安全である。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$a=1$，$b=\sqrt2$，$c=\sqrt5$ のとき、$C$ を求めよ。",
  "exa": r"$C=135^\circ$"},
 {"lv": 2, "title": "正弦の比から辺の比・角を求める",
  "q": r"$\triangle\mathrm{ABC}$ において、$\sin A:\sin B:\sin C=3:5:7$ が成り立つとき、次の問いに答えよ。<br>(1) この三角形の最大の角の大きさを求めよ。　(2) 最小の角を $\theta$ とするとき、$\cos\theta$ の値を求めよ。",
  "hint": r"正弦定理から $a:b:c=\sin A:\sin B:\sin C$。$a=3k,\ b=5k,\ c=7k$（$k>0$）とおけば余弦定理が使える。最大の角は最大の辺の対角。",
  "sol": r"正弦定理より $a:b:c=\sin A:\sin B:\sin C=3:5:7$ だから、$a=3k$，$b=5k$，$c=7k$（$k>0$）とおける。<br>"
         r"(1) 最大の辺は $c$ だから最大の角は $C$。$\cos C=\dfrac{9k^2+25k^2-49k^2}{2\cdot3k\cdot5k}=-\dfrac12$　よって　$C=\boldsymbol{120^\circ}$<br>"
         r"(2) 最小の辺は $a$ だから最小の角は $A$。$\cos A=\dfrac{25k^2+49k^2-9k^2}{2\cdot5k\cdot7k}=\dfrac{65}{70}=\boldsymbol{\dfrac{13}{14}}$",
  "note": r"比が与えられたら $k$ を使って実際の長さとして置くと、計算の途中で $k$ が約分されて消える。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$(b+c):(c+a):(a+b)=4:5:6$ のとき、$\sin A:\sin B:\sin C$ と、最大の角の大きさを求めよ。",
  "exa": r"$\sin A:\sin B:\sin C=7:5:3$，最大の角は $A=120^\circ$"},
]})


# ---------------------------------------------------------------- 図：節4
def _fig_ssa():  # 2辺と1角：三角形が2つできる
    s, ox, oy = 44, 14, 96
    r3 = math.sqrt(3)
    T = lambda x, y: (ox + s * x, oy - s * y)
    A, C, B1, B2 = T(0, 0), T(r3, r3), T(r3 - 1, 0), T(r3 + 1, 0)
    f = _Fig(150, 112)
    f.L(A, T(3.05, 0)); f.L(A, C)
    f.L(C, B1); f.L(C, B2)
    f.path("M" + " L".join(f"{_n(T(r3 + 2 * math.cos(math.radians(a)), r3 + 2 * math.sin(math.radians(a)))[0])},{_n(T(r3 + 2 * math.cos(math.radians(a)), r3 + 2 * math.sin(math.radians(a)))[1])}" for a in range(232, 312, 2)), dash=True, sw=0.7)
    f.arc(A, T(1, 0), C, r=14, label="45°", lr=24, size=9)
    f.T(A, "A", -7, 4); f.T(C, "C", 0, -9); f.T(B1, "B₁", -1, 9, size=10); f.T(B2, "B₂", 2, 9, size=10)
    f.T(_mid(A, C), "√6", -9, -5, size=10); f.T(_mid(C, B1), "2", -7, 0, size=10); f.T(_mid(C, B2), "2", 7, 0, size=10)
    for p in (B1, B2):
        f.dot(p)
    return f.svg()


def _fig_2b():  # A=2B と角の二等分線
    s, ox, oy = 25, 10, 100
    T = lambda x, y: (ox + s * x, oy - s * y)
    ax, ay = 45 / 12, math.sqrt(25 - (45 / 12) ** 2)
    B, C, A, D = T(0, 0), T(6, 0), T(ax, ay), T(10 / 3, 0)
    f = _Fig(170, 114)
    f.PL([A, B, C]); f.L(A, D)
    f.arc(B, C, A, r=18, label="●", lr=25, size=6)
    f.arc(A, B, D, r=22, label="●", lr=29, size=6)
    f.arc(A, D, C, r=22, label="●", lr=29, size=6)
    f.T(A, "A", 0, -9); f.T(B, "B", -7, 4); f.T(C, "C", 7, 4); f.T(D, "D", 0, 9)
    return f.svg()


# ---------------------------------------------------------------- 節4
SEC.append({"title": "三角形の解法と形状",
"base": r"""・三角形を解く：与えられた要素（3辺／2辺と間の角／1辺と両端の角）に応じて、正弦定理・余弦定理を使い分けて残りの辺と角を求める。<br>
・2辺と、その間でない角が与えられると、三角形が2つ決まることがある。余弦定理で残りの辺の2次方程式を作ると見落としがない。<br>
・正弦定理で角を求めると $\sin B=\dfrac{\sqrt3}{2}$ から $B=60^\circ,\ 120^\circ$ の2候補が出る。辺の大小（大きい辺の対角は大きい）や角の和で吟味する。<br>
・形状の決定：$\sin A=\dfrac{a}{2R}$，$\cos A=\dfrac{b^2+c^2-a^2}{2bc}$ などを代入して<b>辺だけの関係</b>にし、因数分解する。""",
"items": [
 {"lv": 2, "title": "2辺とその間の角から三角形を解く",
  "q": r"$\triangle\mathrm{ABC}$ において、$b=2$，$c=\sqrt3+1$，$A=60^\circ$ のとき、$a$，$B$，$C$ を求めよ。",
  "hint": r"まず余弦定理で $a$ を求める。次に $B$ を求めるが、$\sin B$ からでは2通りの候補が出るので、$\cos B$ を余弦定理で求めると1つに決まる。",
  "sol": r"余弦定理より　$a^2=2^2+(\sqrt3+1)^2-2\cdot2(\sqrt3+1)\cos60^\circ=4+(4+2\sqrt3)-2(\sqrt3+1)=6$　　$a>0$ より　$a=\boldsymbol{\sqrt6}$<br>"
         r"$\cos B=\dfrac{c^2+a^2-b^2}{2ca}=\dfrac{(4+2\sqrt3)+6-4}{2(\sqrt3+1)\sqrt6}=\dfrac{2\sqrt3(\sqrt3+1)}{2\sqrt6(\sqrt3+1)}=\dfrac{\sqrt3}{\sqrt6}=\dfrac{1}{\sqrt2}$<br>"
         r"よって　$B=\boldsymbol{45^\circ}$，$C=180^\circ-(60^\circ+45^\circ)=\boldsymbol{75^\circ}$",
  "note": r"正弦定理を使うなら $\sin B=\dfrac{b\sin A}{a}=\dfrac{1}{\sqrt2}$ で、$B=45^\circ$ または $135^\circ$。$b<c$ より $B<C$ なので $B$ は最大角ではなく、$B=135^\circ$ だと $A+B>180^\circ$ にもなるから $B=45^\circ$ と吟味する。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$a=\sqrt6-\sqrt2$，$b=2$，$C=135^\circ$ のとき、$c$，$A$，$B$ を求めよ。",
  "exa": r"$c=2\sqrt2$，$A=15^\circ$，$B=30^\circ$"},
 {"lv": 3, "title": "2辺と1つの対角から三角形を解く（解が2つ）",
  "q": r"$\triangle\mathrm{ABC}$ において、$a=2$，$b=\sqrt6$，$A=45^\circ$ のとき、$c$，$B$，$C$ を求めよ。",
  "hint": r"与えられた角 $A$ は辺 $a$ の対角で、2辺 $a,\ b$ の間の角ではない。そこで残りの辺 $c$ を未知数として余弦定理 $a^2=b^2+c^2-2bc\cos A$ を立てると、$c$ の2次方程式になる。正の解が2つあれば三角形も2つある。",
  "sol": _fig_ssa() + r"余弦定理より　$2^2=(\sqrt6)^2+c^2-2\sqrt6\,c\cos45^\circ$<br>"
         r"$c^2-2\sqrt3\,c+2=0$　より　$c=\sqrt3\pm1$（ともに正）<br>"
         r"(i) $c=\sqrt3+1$ のとき　$\cos B=\dfrac{c^2+a^2-b^2}{2ca}=\dfrac{(4+2\sqrt3)+4-6}{4(\sqrt3+1)}=\dfrac{2(\sqrt3+1)}{4(\sqrt3+1)}=\dfrac12$<br>"
         r"　よって $B=60^\circ$，$C=180^\circ-(45^\circ+60^\circ)=75^\circ$<br>"
         r"(ii) $c=\sqrt3-1$ のとき　$\cos B=\dfrac{(4-2\sqrt3)+4-6}{4(\sqrt3-1)}=\dfrac{-2(\sqrt3-1)}{4(\sqrt3-1)}=-\dfrac12$<br>"
         r"　よって $B=120^\circ$，$C=180^\circ-(45^\circ+120^\circ)=15^\circ$<br>"
         r"答　$\boldsymbol{c=\sqrt3+1,\ B=60^\circ,\ C=75^\circ}$　または　$\boldsymbol{c=\sqrt3-1,\ B=120^\circ,\ C=15^\circ}$",
  "note": r"図のように、点 $\mathrm{C}$ を中心とする半径 $a=2$ の円が、$\mathrm{A}$ から出る半直線と2点 $\mathrm{B_1}$，$\mathrm{B_2}$ で交わるため三角形が2つできる。正弦定理で $\sin B=\dfrac{\sqrt3}{2}$ とすると $B=60^\circ,\ 120^\circ$ がともに適することになり、同じ結論になる。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$a=1$，$b=\sqrt3$，$A=30^\circ$ のとき、$c$，$B$，$C$ を求めよ。",
  "exa": r"$c=2,\ B=60^\circ,\ C=90^\circ$　または　$c=1,\ B=120^\circ,\ C=30^\circ$"},
 {"lv": 3, "title": "辺と角の関係式から三角形の形状を決定する",
  "q": r"$\triangle\mathrm{ABC}$ において $a\cos A=b\cos B$ が成り立つとき、この三角形はどのような形か。",
  "hint": r"余弦定理で $\cos A,\ \cos B$ を辺で表し、<b>辺だけの式</b>にする。分母を払って整理し、因数分解して「$\cdots=0$ または $\cdots=0$」の形にする。",
  "sol": r"余弦定理より　$a\cdot\dfrac{b^2+c^2-a^2}{2bc}=b\cdot\dfrac{c^2+a^2-b^2}{2ca}$<br>"
         r"両辺に $2abc$ を掛けて　$a^2(b^2+c^2-a^2)=b^2(c^2+a^2-b^2)$<br>"
         r"展開して整理すると　$a^2c^2-b^2c^2-a^4+b^4=0$<br>"
         r"$c^2(a^2-b^2)-(a^2+b^2)(a^2-b^2)=0$，$(a^2-b^2)(c^2-a^2-b^2)=0$<br>"
         r"よって　$a=b$　または　$c^2=a^2+b^2$　（$a,\ b>0$）<br>"
         r"ゆえに　$\boldsymbol{\mathrm{BC}=\mathrm{CA}}$ <b>の二等辺三角形 または</b> $\boldsymbol{C=90^\circ}$ <b>の直角三角形</b>",
  "note": r"「または」なので、両方を満たす直角二等辺三角形も含まれる。両辺を $\cos$ で割ったり、$a^2-b^2$ で割ったりすると、一方の場合を落とすので注意。",
  "ex": r"$\triangle\mathrm{ABC}$ において $\sin A=2\sin B\cos C$ が成り立つとき、この三角形はどのような形か。",
  "exa": r"$\mathrm{CA}=\mathrm{AB}$ の二等辺三角形（$b=c$）"},
 {"lv": 3, "title": "鈍角三角形となる条件",
  "q": r"3辺の長さが $3,\ 4,\ x$ である三角形が鈍角三角形となるような、$x$ の値の範囲を求めよ。",
  "hint": r"まず三角形が存在する条件 $|4-3|<x<4+3$。鈍角は<b>最大辺の対角</b>にしかできないので、最大辺が $x$ か $4$ かで場合を分け、「最大辺$^2>$ 他の2辺の平方の和」を使う。",
  "sol": r"三角形が存在する条件は　$1<x<7$　…①<br>"
         r"(i) $x\geqq4$ のとき、最大辺は $x$。その対角が鈍角となる条件は　$x^2>3^2+4^2=25$ より $x>5$。①とあわせて　$5<x<7$<br>"
         r"(ii) $x<4$ のとき、最大辺は $4$。その対角が鈍角となる条件は　$4^2>3^2+x^2$ より $x^2<7$，$0<x<\sqrt7$。①とあわせて　$1<x<\sqrt7$<br>"
         r"よって　$\boldsymbol{1<x<\sqrt7,\ 5<x<7}$",
  "note": r"「鈍角三角形」は鈍角が1つあればよい。$x$ が最大辺になるとは限らないので、場合分けを忘れると $1<x<\sqrt7$ の部分を落とす。",
  "ex": r"3辺の長さが $2,\ 3,\ x$ である三角形が鋭角三角形となるような、$x$ の値の範囲を求めよ。",
  "exa": r"$\sqrt5<x<\sqrt{13}$"},
 {"lv": 4, "title": "角の条件 A=2B から辺の関係を導く",
  "q": r"$\triangle\mathrm{ABC}$ において $A=2B$ であるとする。<br>(1) $a^2=b(b+c)$ が成り立つことを証明せよ。<br>(2) $b=4$，$c=5$ のとき、$a$ と $\cos B$ の値を求めよ。",
  "hint": r"$\angle\mathrm{A}$ の二等分線を引くと、$B$ と等しい角が2つでき、<b>二等辺三角形と相似な三角形</b>が現れる。相似比から線分の長さを $a,\ b,\ c$ で表す。",
  "sol": _fig_2b() + r"(1) $\angle\mathrm{A}$ の二等分線と辺 $\mathrm{BC}$ の交点を $\mathrm{D}$ とすると　$\angle\mathrm{BAD}=\angle\mathrm{CAD}=\dfrac A2=B$<br>"
         r"$\triangle\mathrm{DAB}$ で $\angle\mathrm{DAB}=\angle\mathrm{DBA}$ だから　$\mathrm{DA}=\mathrm{DB}$　…①<br>"
         r"$\triangle\mathrm{CAD}$ と $\triangle\mathrm{CBA}$ で、$\angle\mathrm{C}$ は共通、$\angle\mathrm{CAD}=B=\angle\mathrm{CBA}$ だから　$\triangle\mathrm{CAD}\sim\triangle\mathrm{CBA}$<br>"
         r"よって $\mathrm{CA}:\mathrm{CB}=\mathrm{CD}:\mathrm{CA}=\mathrm{AD}:\mathrm{BA}$，すなわち　$b:a=\mathrm{CD}:b=\mathrm{AD}:c$<br>"
         r"ゆえに　$\mathrm{CD}=\dfrac{b^2}{a}$，$\mathrm{AD}=\dfrac{bc}{a}$。①より $\mathrm{BD}=\dfrac{bc}{a}$<br>"
         r"$\mathrm{BD}+\mathrm{DC}=\mathrm{BC}$ だから　$\dfrac{bc}{a}+\dfrac{b^2}{a}=a$　　よって　$a^2=b(b+c)$　（証明終）<br>"
         r"(2) (1) より $a^2=4(4+5)=36$，$a>0$ より　$a=\boldsymbol{6}$<br>"
         r"余弦定理より　$\cos B=\dfrac{c^2+a^2-b^2}{2ca}=\dfrac{25+36-16}{2\cdot5\cdot6}=\boldsymbol{\dfrac34}$",
  "note": r"逆に $a^2=b(b+c)$ ならば $A=2B$ も成り立つ。(2) の三角形では $\cos A=\dfrac{16+25-36}{2\cdot4\cdot5}=\dfrac18$ で、数学IIで学ぶ2倍角の公式 $\cos2B=2\cos^2B-1=\dfrac18$ と一致する。",
  "ex": r"$\triangle\mathrm{ABC}$ において $A=2B$，$b=9$，$c=7$ のとき、$a$ と $\cos B$ の値を求めよ。",
  "exa": r"$a=12$，$\cos B=\dfrac23$"},
]})

# ---------------------------------------------------------------- 図：節5・節6
def _fig_bis():  # 角の二等分線 AD（AB=3, AC=6, A=120°）
    s, ox, oy = 21, 84, 124
    r3 = math.sqrt(3)
    T = lambda x, y: (ox + s * x, oy - s * y)
    A, B, C, D = T(0, 0), T(3, 0), T(-3, 3 * r3), T(1, r3)
    f = _Fig(160, 138)
    f.PL([A, B, C]); f.L(A, D)
    f.arc(A, B, D, r=12, label="60°", lr=24, size=9)
    f.arc(A, D, C, r=15, label="60°", lr=27, size=9)
    f.T(A, "A", -2, 9); f.T(B, "B", 7, 4); f.T(C, "C", -7, -3); f.T(D, "D", 8, -2)
    f.T(_mid(A, B), "3", 0, 8, size=10); f.T(_mid(A, C), "6", -8, 3, size=10)
    return f.svg()


def _cyc(sides, R):
    """円（半径 R）に内接し、辺が sides の四角形の頂点の中心角（度）。中心が外にある場合も扱う。"""
    ang = [2 * math.degrees(math.asin(x / (2 * R))) for x in sides]
    if abs(sum(ang) - 360) > 1e-6:
        i = sides.index(max(sides))
        ang[i] = 360 - (sum(ang) - ang[i])
    assert abs(sum(ang) - 360) < 1e-6 and min(ang) > 0
    return ang


def _fig_cyc(sides, R, start, s, names="ABCD", diag=((0, 2),), lab=None, P=None):
    """円に内接する四角形の図。辺の長さは円の外側に書く。P=(dx,dy) なら対角線の交点 P を示す。"""
    ang = _cyc(sides, R)
    m = 17
    w = h = int(2 * R * s + 2 * m)
    T = lambda x, y: (w / 2 + s * x, h / 2 - s * y)
    th, pts, dirs = start, [], []
    for k in range(4):
        pts.append((R * math.cos(math.radians(th)), R * math.sin(math.radians(th))))
        dirs.append(th)
        th -= ang[k]                           # 時計回りに A→B→C→D
    f = _Fig(w, h)
    f.C(T(0, 0), R * s, sw=0.9)
    V = [T(*p) for p in pts]
    f.PL(V)
    for i, j in diag:
        f.L(V[i], V[j], sw=0.9)
    for k in range(4):
        a = math.radians(dirs[k]); rr = R + 8.5 / s
        f.T(T(rr * math.cos(a), rr * math.sin(a)), names[k])
    if lab:   # 辺の長さは、各辺の中点から四角形の外側へ 8px の位置
        cx, cy = sum(v[0] for v in V) / 4, sum(v[1] for v in V) / 4
        for k in range(4):
            p0, p1 = V[k], V[(k + 1) % 4]
            mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
            u = _unit(p0, p1); nx, ny = -u[1], u[0]
            if nx * (mx - cx) + ny * (my - cy) < 0:
                nx, ny = -nx, -ny
            f.T((mx + 8 * nx, my + 8 * ny), lab[k], size=10)
    if P:  # 対角線の交点
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = pts
        den = (x1 - x3) * (y2 - y4) - (y1 - y3) * (x2 - x4)
        t = ((x1 - x2) * (y2 - y4) - (y1 - y2) * (x2 - x4)) / den
        q = T(x1 + t * (x3 - x1), y1 + t * (y3 - y1))
        f.dot(q); f.T(q, "P", P[0], P[1], size=10)
    return f.svg()


# ---------------------------------------------------------------- 節5
SEC.append({"title": "三角形の面積・内接円・外接円",
"base": r"""・面積：$S=\dfrac12bc\sin A=\dfrac12ca\sin B=\dfrac12ab\sin C$（2辺とその間の角）<br>
・3辺から面積：余弦定理で $\cos A$ → $\sin A=\sqrt{1-\cos^2A}$ → $S$。ヘロンの公式 $S=\sqrt{s(s-a)(s-b)(s-c)}$（$2s=a+b+c$）も使える<br>
・内接円の半径 $r$：$S=\dfrac12r(a+b+c)$　　外接円の半径 $R$：$\dfrac{a}{\sin A}=2R$，$S=\dfrac{abc}{4R}$<br>
・角の二等分線の長さ：$\angle\mathrm{A}$ の二等分線を $\mathrm{AD}$ とすると　$\triangle\mathrm{ABD}+\triangle\mathrm{ACD}=\triangle\mathrm{ABC}$　（面積で式を立てる）""",
"items": [
 {"lv": 1, "title": "2辺とその間の角から面積を求める",
  "q": r"(1) $\triangle\mathrm{ABC}$ において、$b=4$，$c=5$，$A=120^\circ$ のとき、面積 $S$ を求めよ。<br>(2) $\mathrm{AB}=4$，$\mathrm{AD}=6$，$\angle\mathrm{A}=135^\circ$ の平行四辺形 $\mathrm{ABCD}$ の面積を求めよ。",
  "hint": r"$S=\dfrac12bc\sin A$ を使う。平行四辺形は対角線で合同な2つの三角形に分かれるので、面積は $\mathrm{AB}\cdot\mathrm{AD}\sin A$。",
  "sol": r"(1) $S=\dfrac12\cdot4\cdot5\sin120^\circ=10\cdot\dfrac{\sqrt3}{2}=\boldsymbol{5\sqrt3}$<br>"
         r"(2) 対角線 $\mathrm{BD}$ で $\triangle\mathrm{ABD}\equiv\triangle\mathrm{CDB}$ に分かれるから<br>"
         r"　（面積）$=2\cdot\dfrac12\cdot4\cdot6\sin135^\circ=24\cdot\dfrac{\sqrt2}{2}=\boldsymbol{12\sqrt2}$",
  "note": r"$\sin(180^\circ-\theta)=\sin\theta$ なので、鈍角でも鋭角でも面積の公式は同じ形。平行四辺形では隣り合う角のどちらを使っても同じ値になる。",
  "ex": r"(1) $\triangle\mathrm{ABC}$ において、$a=6$，$b=2\sqrt3$，$C=150^\circ$ のとき、面積を求めよ。(2) $\mathrm{AB}=5$，$\mathrm{AD}=4$，$\angle\mathrm{B}=120^\circ$ の平行四辺形 $\mathrm{ABCD}$ の面積を求めよ。",
  "exa": r"(1) $3\sqrt3$　(2) $10\sqrt3$"},
 {"lv": 2, "title": "3辺から面積・内接円・外接円の半径を求める",
  "q": r"$\triangle\mathrm{ABC}$ において、$a=5$，$b=6$，$c=7$ のとき、次のものを求めよ。<br>(1) $\cos C$　　(2) 面積 $S$　　(3) 内接円の半径 $r$　　(4) 外接円の半径 $R$",
  "hint": r"余弦定理で $\cos C$ → $\sin C$ → 面積の順。$r$ は $S=\dfrac12r(a+b+c)$、$R$ は正弦定理 $\dfrac{c}{\sin C}=2R$ から。",
  "sol": r"(1) $\cos C=\dfrac{a^2+b^2-c^2}{2ab}=\dfrac{25+36-49}{60}=\boldsymbol{\dfrac15}$<br>"
         r"(2) $\sin C>0$ より $\sin C=\sqrt{1-\dfrac{1}{25}}=\dfrac{2\sqrt6}{5}$　　$S=\dfrac12ab\sin C=\dfrac12\cdot5\cdot6\cdot\dfrac{2\sqrt6}{5}=\boldsymbol{6\sqrt6}$<br>"
         r"(3) $S=\dfrac12r(a+b+c)$ より　$6\sqrt6=\dfrac12r\cdot18$　　$r=\boldsymbol{\dfrac{2\sqrt6}{3}}$<br>"
         r"(4) $2R=\dfrac{c}{\sin C}=7\cdot\dfrac{5}{2\sqrt6}=\dfrac{35}{2\sqrt6}$　　$R=\dfrac{35}{4\sqrt6}=\boldsymbol{\dfrac{35\sqrt6}{24}}$",
  "note": r"ヘロンの公式では $s=9$ で $S=\sqrt{9\cdot4\cdot3\cdot2}=6\sqrt6$。また、辺 $\mathrm{BC}$ の中点を $\mathrm{M}$ とすると、$\cos B=\dfrac{19}{35}$ と余弦定理から中線の長さ $\mathrm{AM}=\sqrt{7^2+\left(\dfrac52\right)^2-2\cdot7\cdot\dfrac52\cdot\dfrac{19}{35}}=\dfrac{\sqrt{145}}{2}$ も求まる。",
  "ex": r"$\triangle\mathrm{ABC}$ において、$a=4$，$b=5$，$c=6$ のとき、$\cos A$，面積 $S$，内接円の半径 $r$，外接円の半径 $R$ を求めよ。",
  "exa": r"$\cos A=\dfrac34$，$S=\dfrac{15\sqrt7}{4}$，$r=\dfrac{\sqrt7}{2}$，$R=\dfrac{8\sqrt7}{7}$"},
 {"lv": 2, "title": "角の二等分線の長さ（面積の利用）",
  "q": _fig_bis() + r"$\triangle\mathrm{ABC}$ において $\mathrm{AB}=3$，$\mathrm{AC}=6$，$A=120^\circ$ とする。$\angle\mathrm{A}$ の二等分線と辺 $\mathrm{BC}$ の交点を $\mathrm{D}$ とするとき、次のものを求めよ。<br>(1) 線分 $\mathrm{AD}$ の長さ　　(2) 線分 $\mathrm{BD}$ の長さ",
  "hint": r"$\mathrm{AD}=x$ とおき、$\triangle\mathrm{ABD}+\triangle\mathrm{ACD}=\triangle\mathrm{ABC}$ を面積の公式で表す。$\angle\mathrm{BAD}=\angle\mathrm{CAD}=60^\circ$。(2) は面積比が底辺の比 $\mathrm{BD}:\mathrm{DC}$ に等しいことを使う。",
  "sol": r"(1) $\mathrm{AD}=x$ とおく。$\triangle\mathrm{ABD}+\triangle\mathrm{ACD}=\triangle\mathrm{ABC}$ より<br>"
         r"　$\dfrac12\cdot3x\sin60^\circ+\dfrac12\cdot6x\sin60^\circ=\dfrac12\cdot3\cdot6\sin120^\circ$<br>"
         r"　$\dfrac{9\sqrt3}{4}x=\dfrac{9\sqrt3}{2}$　　よって　$\mathrm{AD}=\boldsymbol{2}$<br>"
         r"(2) 余弦定理より　$\mathrm{BC}^2=9+36-2\cdot3\cdot6\cos120^\circ=63$，$\mathrm{BC}=3\sqrt7$<br>"
         r"$\triangle\mathrm{ABD}$ と $\triangle\mathrm{ACD}$ は高さが共通なので　$\mathrm{BD}:\mathrm{DC}=\triangle\mathrm{ABD}:\triangle\mathrm{ACD}=\dfrac12\cdot3x\sin60^\circ:\dfrac12\cdot6x\sin60^\circ=1:2$<br>"
         r"　よって　$\mathrm{BD}=\dfrac13\mathrm{BC}=\boldsymbol{\sqrt7}$",
  "note": r"(2) の比 $\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}$ は数学Aの「角の二等分線の定理」そのものである。$A=120^\circ$ のときは一般に $\dfrac1{\mathrm{AD}}=\dfrac1{\mathrm{AB}}+\dfrac1{\mathrm{AC}}$ が成り立つ（$\dfrac13+\dfrac16=\dfrac12$）。",
  "ex": r"$\triangle\mathrm{ABC}$ において $\mathrm{AB}=3$，$\mathrm{AC}=6$，$A=60^\circ$ とする。$\angle\mathrm{A}$ の二等分線と辺 $\mathrm{BC}$ の交点を $\mathrm{D}$ とするとき、$\mathrm{AD}$，$\mathrm{BD}$ の長さを求めよ。",
  "exa": r"$\mathrm{AD}=2\sqrt3$，$\mathrm{BD}=\sqrt3$"},
 {"lv": 3, "title": "面積と1辺・1角から残りの辺と内接円の半径を求める",
  "q": r"$\triangle\mathrm{ABC}$ において $A=60^\circ$，$a=7$ で、面積が $10\sqrt3$ である。$b>c$ のとき、$b,\ c$ と内接円の半径 $r$ を求めよ。",
  "hint": r"面積の式から $bc$、余弦定理から $b^2+c^2-bc$ が分かる。$b^2+c^2=(b+c)^2-2bc$ として $b+c$ を求めれば、$b,\ c$ は和と積が分かった2数として2次方程式の解になる。",
  "sol": r"面積より　$\dfrac12bc\sin60^\circ=10\sqrt3$　　よって　$bc=40$<br>"
         r"余弦定理より　$49=b^2+c^2-2bc\cos60^\circ=(b+c)^2-3bc=(b+c)^2-120$<br>"
         r"$(b+c)^2=169$，$b+c>0$ より　$b+c=13$<br>"
         r"$b,\ c$ は $t^2-13t+40=0$ の2解で、$(t-5)(t-8)=0$。$b>c$ より　$\boldsymbol{b=8,\ c=5}$<br>"
         r"$S=\dfrac12r(a+b+c)$ より　$10\sqrt3=\dfrac12r\cdot20$　　$r=\boldsymbol{\sqrt3}$",
  "note": r"「和と積」に持ち込むのは、$b,\ c$ の対称式だけが分かっているときの定石。実数条件 $(b+c)^2-4bc=169-160\geqq0$ も満たしている。",
  "ex": r"$\triangle\mathrm{ABC}$ において $A=120^\circ$，$a=7$ で、面積が $\dfrac{15\sqrt3}{4}$ である。$b>c$ のとき、$b,\ c$ と内接円の半径 $r$ を求めよ。",
  "exa": r"$b=5$，$c=3$，$r=\dfrac{\sqrt3}{2}$"},
]})

# ---------------------------------------------------------------- 節6
SEC.append({"title": "円に内接する四角形・四角形の面積",
"base": r"""・円に内接する四角形 $\mathrm{ABCD}$ では対角の和が $180^\circ$：$\cos D=-\cos B$，$\sin D=\sin B$<br>
・対角線 $\mathrm{AC}$ を $\triangle\mathrm{ABC}$，$\triangle\mathrm{ACD}$ の両方で余弦定理により表し、等しいとおくと $\cos B$ が求まる。<br>
・四角形の面積：対角線の長さ $p,\ q$、そのなす角 $\theta$ のとき　$S=\dfrac12pq\sin\theta$<br>
・対角線の交点 $\mathrm{P}$ について　$\mathrm{AP}:\mathrm{PC}=\triangle\mathrm{ABD}:\triangle\mathrm{CBD}$（底辺 $\mathrm{BD}$ が共通な三角形の面積比）""",
"items": [
 {"lv": 2, "title": "対角線と四角形の面積",
  "q": r"(1) 凸四角形 $\mathrm{ABCD}$ の対角線の長さを $p,\ q$、そのなす角を $\theta$ とすると、面積 $S$ は $S=\dfrac12pq\sin\theta$ で表されることを示せ。<br>(2) 対角線の長さが $6$ と $8$ である凸四角形の面積の最大値を求めよ。",
  "hint": r"対角線の交点 $\mathrm{O}$ で四角形を4つの三角形に分け、それぞれ $\dfrac12\times$(2辺)$\times\sin$ で表して加える。$\mathrm{O}$ のまわりの角は $\theta$ と $180^\circ-\theta$ で、正弦は等しい。",
  "sol": r"(1) 対角線 $\mathrm{AC}$，$\mathrm{BD}$ の交点を $\mathrm{O}$ とし、$\mathrm{OA}=x_1$，$\mathrm{OC}=x_2$，$\mathrm{OB}=y_1$，$\mathrm{OD}=y_2$，$\angle\mathrm{AOB}=\theta$ とする。<br>"
         r"$\angle\mathrm{BOC}=\angle\mathrm{DOA}=180^\circ-\theta$，$\angle\mathrm{COD}=\theta$ で、$\sin(180^\circ-\theta)=\sin\theta$ だから<br>"
         r"　$S=\triangle\mathrm{OAB}+\triangle\mathrm{OBC}+\triangle\mathrm{OCD}+\triangle\mathrm{ODA}=\dfrac12(x_1y_1+y_1x_2+x_2y_2+y_2x_1)\sin\theta$<br>"
         r"　$=\dfrac12(x_1+x_2)(y_1+y_2)\sin\theta=\dfrac12pq\sin\theta$　（証明終）<br>"
         r"(2) (1) より $S=\dfrac12\cdot6\cdot8\sin\theta=24\sin\theta\leqq24$。等号は $\theta=90^\circ$（例えば対角線が $6,\ 8$ のひし形）で成り立つから、最大値は $\boldsymbol{24}$",
  "note": r"(1) の公式は、なす角が $\theta$ でも $180^\circ-\theta$ でも同じ値を与える。対角線が垂直な四角形（ひし形・正方形など）では $S=\dfrac12pq$。",
  "ex": r"(1) 対角線の長さが $5,\ 7$ で、そのなす角が $30^\circ$ の四角形の面積を求めよ。(2) 対角線の長さの和が $10$ である凸四角形の面積の最大値を求めよ。",
  "exa": r"(1) $\dfrac{35}{4}$　(2) $\dfrac{25}{2}$"},
 {"lv": 3, "title": "円に内接する四角形の対角線と面積",
  "q": _fig_cyc([2, 3, 5, 3], math.sqrt(57) / 3, 150, 22, lab=["2", "3", "5", "3"]) +
       r"円に内接する四角形 $\mathrm{ABCD}$ において、$\mathrm{AB}=2$，$\mathrm{BC}=3$，$\mathrm{CD}=5$，$\mathrm{DA}=3$ である。次のものを求めよ。<br>(1) $B$ の大きさ　(2) 対角線 $\mathrm{AC}$ の長さ　(3) 四角形 $\mathrm{ABCD}$ の面積 $S$　(4) 外接円の半径 $R$",
  "hint": r"$B+D=180^\circ$ より $\cos D=-\cos B$。$\mathrm{AC}^2$ を $\triangle\mathrm{ABC}$ と $\triangle\mathrm{ACD}$ の2通りに余弦定理で表して等置する。",
  "sol": r"(1) 四角形が円に内接するから $D=180^\circ-B$，$\cos D=-\cos B$。余弦定理より<br>"
         r"　$\triangle\mathrm{ABC}$：$\mathrm{AC}^2=2^2+3^2-2\cdot2\cdot3\cos B=13-12\cos B$<br>"
         r"　$\triangle\mathrm{ACD}$：$\mathrm{AC}^2=5^2+3^2-2\cdot5\cdot3\cos D=34+30\cos B$<br>"
         r"　$13-12\cos B=34+30\cos B$ より $\cos B=-\dfrac12$　　よって　$B=\boldsymbol{120^\circ}$<br>"
         r"(2) $\mathrm{AC}^2=13-12\cdot\left(-\dfrac12\right)=19$　　$\mathrm{AC}=\boldsymbol{\sqrt{19}}$<br>"
         r"(3) $\sin D=\sin B=\dfrac{\sqrt3}{2}$ だから　$S=\dfrac12\cdot2\cdot3\cdot\dfrac{\sqrt3}{2}+\dfrac12\cdot5\cdot3\cdot\dfrac{\sqrt3}{2}=\dfrac{6\sqrt3}{4}+\dfrac{15\sqrt3}{4}=\boldsymbol{\dfrac{21\sqrt3}{4}}$<br>"
         r"(4) 外接円は $\triangle\mathrm{ABC}$ の外接円だから、正弦定理より　$2R=\dfrac{\mathrm{AC}}{\sin B}=\dfrac{2\sqrt{19}}{\sqrt3}$　　$R=\dfrac{\sqrt{19}}{\sqrt3}=\boldsymbol{\dfrac{\sqrt{57}}{3}}$",
  "note": r"四角形の外接円は、4頂点のうちどの3点を選んでできる三角形の外接円とも一致する。この事実が (4) を三角形の問題に帰着させる。",
  "ex": r"円に内接する四角形 $\mathrm{ABCD}$ において、$\mathrm{AB}=1$，$\mathrm{BC}=3$，$\mathrm{CD}=4$，$\mathrm{DA}=3$ のとき、$B$ の大きさ、対角線 $\mathrm{AC}$ の長さ、面積 $S$、外接円の半径 $R$ を求めよ。",
  "exa": r"$B=120^\circ$，$\mathrm{AC}=\sqrt{13}$，$S=\dfrac{15\sqrt3}{4}$，$R=\dfrac{\sqrt{39}}{3}$"},
 {"lv": 4, "title": "円に内接する四角形の2本の対角線と交点の分ける比",
  "q": _fig_cyc([5, 3, 3, 8], 7 / math.sqrt(3), 160, 14.5, diag=((0, 2), (1, 3)), lab=["5", "3", "3", "8"], P=(-2, 9)) +
       r"円に内接する四角形 $\mathrm{ABCD}$ において、$\mathrm{AB}=5$，$\mathrm{BC}=3$，$\mathrm{CD}=3$，$\mathrm{DA}=8$ である。対角線 $\mathrm{AC}$，$\mathrm{BD}$ の交点を $\mathrm{P}$ とする。<br>(1) $\mathrm{AC}$ の長さを求めよ。　(2) $\mathrm{BD}$ の長さを求めよ。<br>(3) $\mathrm{AP}:\mathrm{PC}$ および $\mathrm{BP}:\mathrm{PD}$ を求めよ。",
  "hint": r"(1)(2) は対角の和が $180^\circ$ であることを使い、各対角線を2通りに表す。(3) は $\mathrm{AP}:\mathrm{PC}$ を「底辺 $\mathrm{BD}$ を共有する2つの三角形の面積比」とみる。$\sin A=\sin C$ なので面積比は辺の積の比になる。",
  "sol": r"(1) $\cos D=-\cos B$ だから　$\mathrm{AC}^2=25+9-30\cos B=9+64+48\cos B$<br>"
         r"　$\cos B=-\dfrac{39}{78}=-\dfrac12$，$\mathrm{AC}^2=34+15=49$　　$\mathrm{AC}=\boldsymbol{7}$<br>"
         r"(2) $\cos C=-\cos A$ だから　$\mathrm{BD}^2=25+64-80\cos A=9+9+18\cos A$<br>"
         r"　$98\cos A=71$ より $\cos A=\dfrac{71}{98}$。$\mathrm{BD}^2=18+18\cdot\dfrac{71}{98}=\dfrac{18\cdot169}{98}=\dfrac{9\cdot169}{49}$　　$\mathrm{BD}=\boldsymbol{\dfrac{39}{7}}$<br>"
         r"(3) $\triangle\mathrm{ABD}$ と $\triangle\mathrm{CBD}$ は底辺 $\mathrm{BD}$ が共通で、高さの比は $\mathrm{AP}:\mathrm{PC}$ に等しい。$\sin C=\sin A$ だから<br>"
         r"　$\mathrm{AP}:\mathrm{PC}=\dfrac12\cdot5\cdot8\sin A:\dfrac12\cdot3\cdot3\sin C=\boldsymbol{40:9}$<br>"
         r"同様に、$\triangle\mathrm{ABC}$ と $\triangle\mathrm{ADC}$（底辺 $\mathrm{AC}$ が共通）で $\sin D=\sin B$ だから<br>"
         r"　$\mathrm{BP}:\mathrm{PD}=\dfrac12\cdot5\cdot3\sin B:\dfrac12\cdot8\cdot3\sin D=15:24=\boldsymbol{5:8}$",
  "note": r"$\mathrm{AC}\cdot\mathrm{BD}=7\cdot\dfrac{39}{7}=39=\mathrm{AB}\cdot\mathrm{CD}+\mathrm{AD}\cdot\mathrm{BC}=15+24$ が成り立っている（トレミーの定理）。(3) から $\mathrm{AP}=\dfrac{40}{7}$，$\mathrm{BP}=\dfrac{15}{7}$ なども分かる。",
  "ex": r"円に内接する四角形 $\mathrm{ABCD}$ において、$\mathrm{AB}=3$，$\mathrm{BC}=5$，$\mathrm{CD}=5$，$\mathrm{DA}=8$ である。対角線 $\mathrm{AC}$，$\mathrm{BD}$ の長さと、交点 $\mathrm{P}$ について $\mathrm{AP}:\mathrm{PC}$，$\mathrm{BP}:\mathrm{PD}$ を求めよ。",
  "exa": r"$\mathrm{AC}=7$，$\mathrm{BD}=\dfrac{55}{7}$，$\mathrm{AP}:\mathrm{PC}=24:25$，$\mathrm{BP}:\mathrm{PD}=3:8$"},
 {"lv": 5, "title": "円に内接する四角形の面積公式と四角形の面積の最大",
  "q": r"(1) 円に内接する四角形 $\mathrm{ABCD}$ において $\mathrm{AB}=a$，$\mathrm{BC}=b$，$\mathrm{CD}=c$，$\mathrm{DA}=d$，$s=\dfrac{a+b+c+d}{2}$ とすると、面積 $S$ は $S=\sqrt{(s-a)(s-b)(s-c)(s-d)}$ で表されることを証明せよ。<br>(2) 4辺の長さが $\mathrm{AB}=2$，$\mathrm{BC}=3$，$\mathrm{CD}=4$，$\mathrm{DA}=5$ である凸四角形 $\mathrm{ABCD}$ の面積の最大値を求めよ。",
  "hint": r"(1) $B=\theta$ として $\cos\theta$ を辺で表し、$16S^2=4(ab+cd)^2\sin^2\theta=4(ab+cd)^2-\{2(ab+cd)\cos\theta\}^2$ を<b>平方の差</b>として2回因数分解する。(2) $B$，$D$ を独立に動かし、$\mathrm{AC}^2$ の2通りの表示と面積の式を<b>2乗して加える</b>。$\cos B\cos D-\sin B\sin D\geqq-1$ を示せば評価できる。",
  "sol": r"(1) $B=\theta$ とすると $D=180^\circ-\theta$。$\mathrm{AC}^2=a^2+b^2-2ab\cos\theta=c^2+d^2+2cd\cos\theta$ より<br>"
         r"　$2(ab+cd)\cos\theta=a^2+b^2-c^2-d^2$　…①<br>"
         r"$S=\triangle\mathrm{ABC}+\triangle\mathrm{ACD}=\dfrac12ab\sin\theta+\dfrac12cd\sin\theta=\dfrac12(ab+cd)\sin\theta$ だから、①を用いて<br>"
         r"$16S^2=4(ab+cd)^2(1-\cos^2\theta)=\{2(ab+cd)\}^2-(a^2+b^2-c^2-d^2)^2$<br>"
         r"$=\{2(ab+cd)+a^2+b^2-c^2-d^2\}\{2(ab+cd)-a^2-b^2+c^2+d^2\}$<br>"
         r"$=\{(a+b)^2-(c-d)^2\}\{(c+d)^2-(a-b)^2\}$<br>"
         r"$=(a+b+c-d)(a+b-c+d)(a-b+c+d)(-a+b+c+d)$<br>"
         r"ここで $a+b+c-d=2(s-d)$，$a+b-c+d=2(s-c)$，$a-b+c+d=2(s-b)$，$-a+b+c+d=2(s-a)$ だから<br>"
         r"$16S^2=16(s-a)(s-b)(s-c)(s-d)$。$S>0$ より　$S=\sqrt{(s-a)(s-b)(s-c)(s-d)}$　（証明終）<br>"
         r"(2) $B=\beta$，$D=\delta$（$0^\circ<\beta,\ \delta<180^\circ$）とおく。$\mathrm{AC}^2=13-12\cos\beta=41-40\cos\delta$ より<br>"
         r"　$6\cos\beta-20\cos\delta=-14$　…②<br>"
         r"また $S=\dfrac12\cdot2\cdot3\sin\beta+\dfrac12\cdot4\cdot5\sin\delta$ より　$2S=6\sin\beta+20\sin\delta$　…③<br>"
         r"②$^2$＋③$^2$ より　$196+4S^2=36+400-240(\cos\beta\cos\delta-\sin\beta\sin\delta)$　…④<br>"
         r"ここで $(\cos\beta+\cos\delta)^2+(\sin\beta-\sin\delta)^2\geqq0$ を展開すると $2+2(\cos\beta\cos\delta-\sin\beta\sin\delta)\geqq0$ だから<br>"
         r"　$\cos\beta\cos\delta-\sin\beta\sin\delta\geqq-1$　…⑤<br>"
         r"④，⑤より $196+4S^2\leqq676$，$S^2\leqq120$，$S\leqq2\sqrt{30}$。<br>"
         r"等号は $\cos\delta=-\cos\beta$ かつ $\sin\delta=\sin\beta$、すなわち $\delta=180^\circ-\beta$（円に内接する）のとき。このとき②は $26\cos\beta=-14$，$\cos\beta=-\dfrac{7}{13}$ となり、$-1<-\dfrac{7}{13}<1$ だからこの $\beta$ で $\triangle\mathrm{ABC}$ を作り、$\mathrm{AC}$ に関して $\mathrm{B}$ と反対側に $\angle\mathrm{D}=180^\circ-\beta$ の $\triangle\mathrm{ACD}$ を作れば実現できる。<br>"
         r"よって、最大値は　$\boldsymbol{2\sqrt{30}}$　（(1) の公式でも $s=7$，$\sqrt{5\cdot4\cdot3\cdot2}=2\sqrt{30}$）",
  "note": r"一般に、4辺の長さが与えられた凸四角形の面積は、円に内接するときに最大となる（(2) と同じ議論が文字のまま通る）。$d\to0$ とすると (1) は三角形のヘロンの公式になる。",
  "ex": r"4辺の長さが $\mathrm{AB}=1$，$\mathrm{BC}=2$，$\mathrm{CD}=3$，$\mathrm{DA}=4$ である凸四角形 $\mathrm{ABCD}$ の面積の最大値を求めよ。",
  "exa": r"$2\sqrt6$（円に内接し $\cos B=-\dfrac57$ のとき）"},
]})

# ---------------------------------------------------------------- 図：節7
def _fig_tower3d():  # 空間の測量
    P, view = _proj(16, 142, 2.2, k=0.9, ang=40)
    aq = 20 * math.sqrt(6); h = 20 * math.sqrt(2)
    A, B = (0, 0, 0), (60, 0, 0)
    Q = (aq * math.cos(math.radians(75)), aq * math.sin(math.radians(75)), 0); Pt = (Q[0], Q[1], h)
    f = _Fig(170, 156)
    f.PL([P(*A), P(*B), P(*Q)], sw=1.0)
    f.L(P(*Q), P(*Pt), sw=2.2); f.L(P(*A), P(*Pt), sw=0.9)
    arc = lambda c, pts: f.PL([P(*c)] and [P(*q) for q in pts], close=False, sw=0.8)
    r = 9
    arc(A, [(r * math.cos(math.radians(t)), r * math.sin(math.radians(t)), 0) for t in range(0, 76, 3)])
    arc(B, [(60 + r * math.cos(math.radians(t)), r * math.sin(math.radians(t)), 0) for t in range(135, 181, 3)])
    u = (math.cos(math.radians(75)), math.sin(math.radians(75)))
    r2 = 14
    arc(A, [(r2 * math.cos(math.radians(t)) * u[0], r2 * math.cos(math.radians(t)) * u[1], r2 * math.sin(math.radians(t))) for t in range(0, 31, 3)])
    f.T(P(6, 3, 0), "75°", 8, 1, size=9); f.T(P(55, 3, 0), "45°", -9, -1, size=9); f.T(P(*A), "30°", 3, -22, size=9)
    for q, t, dx, dy in ((A, "A", -6, 6), (B, "B", 7, 5), (Q, "Q", 7, 5), (Pt, "P", 0, -8)):
        f.dot(P(*q), r=1.6); f.T(P(*q), t, dx, dy)
    f.T(_mid(P(*A), P(*B)), "60 m", 0, 9, size=10)
    return f.svg()


def _fig_box():  # 直方体と △BDE
    P, view = _proj(16, 120, 46, k=0.5, ang=35)
    ab, ad, ae = 1, 2, 2       # AB を奥行き、AD を横、AE を高さにとる
    V = {"A": (0, 0, 0), "B": (0, ab, 0), "C": (ad, ab, 0), "D": (ad, 0, 0),
         "E": (0, 0, ae), "F": (0, ab, ae), "G": (ad, ab, ae), "H": (ad, 0, ae)}
    faces = ["ABCD", "EFGH", "ABFE", "BCGF", "CDHG", "DAEH"]
    f = _Fig(140, 136)
    f.PL([P(*V[k]) for k in "BDE"], fill="#dfe8f7", sw=1.4)
    _solid(f, P, view, V, faces, sw=1.0)
    f.PL([P(*V[k]) for k in "BDE"], sw=1.4)
    _vlabels(f, P, V, "ABCDEFGH", d=8, size=10)
    return f.svg()


def _fig_tetra():  # 正四面体と垂線 AH
    P, view = _proj(14, 116, 15, k=0.5, ang=35)
    r3, r6 = math.sqrt(3), math.sqrt(6)
    V = {"B": (0, 3 * r3, 0), "C": (3, 0, 0), "D": (6, 3 * r3, 0), "A": (3, 2 * r3, 2 * r6)}
    H = (3, 2 * r3, 0)
    f = _Fig(150, 130)
    _solid(f, P, view, V, ["ABC", "ABD", "ACD", "BCD"])
    f.L(P(*V["A"]), P(*H), dash=True, sw=0.9); f.dot(P(*H), r=1.5)
    f.T(P(*H), "H", 6, 4, size=10)
    _vlabels(f, P, V, "ABCD", d=8)
    return f.svg()


def _fig_sector():  # 円錐の展開図
    s, R = 14.5, 6
    O = (95, 12)
    T = lambda r, a: (O[0] + s * r * math.cos(math.radians(a)), O[1] - s * r * math.sin(math.radians(a)))
    f = _Fig(190, 116)
    A, A2, M = T(R, 210), T(R, 330), T(3, 330)
    f.L(O, A); f.L(O, A2)
    f.PL([T(R, a) for a in range(210, 331, 4)], close=False)
    f.L(A, M, sw=1.6, col="#c0392b")
    f.arc(O, A, A2, r=14, label="120°", lr=24, size=9)
    f.T(O, "O", 0, -8); f.T(A, "A", -7, 4); f.T(A2, "A′", 9, 4); f.dot(M); f.T(M, "M", 2, -9)
    f.T(_mid(O, A), "6", -7, -5, size=10); f.T(_mid(O, M), "3", 4, -7, size=10)
    return f.svg()


def _fig_pyr():  # 正四角錐と側面のなす角
    P, view = _proj(84, 86, 16, k=0.5, ang=35)
    V = {"A": (-3, -3, 0), "B": (3, -3, 0), "C": (3, 3, 0), "D": (-3, 3, 0), "O": (0, 0, 4)}
    f = _Fig(168, 112)
    _solid(f, P, view, V, ["ABCD", "OAB", "OBC", "OCD", "ODA"])
    E = tuple(V["B"][i] + 9 / 17 * (V["O"][i] - V["B"][i]) for i in range(3))
    f.L(P(*V["A"]), P(*E), sw=0.9, col="#c0392b"); f.L(P(*V["C"]), P(*E), sw=0.9, col="#c0392b", dash=True)
    f.L(P(*V["A"]), P(*V["C"]), sw=0.7, dash=True)
    f.L(P(*V["O"]), P(0, 0, 0), sw=0.7, dash=True); f.dot(P(0, 0, 0), r=1.4); f.T(P(0, 0, 0), "H", 7, 3, size=10)
    f.dot(P(*E), r=1.5); f.T(P(*E), "E", 8, -1, size=10)
    _vlabels(f, P, V, "ABCDO", d=8)
    return f.svg()


def _fig_boxtet():  # 等面四面体を直方体に埋め込む
    P, view = _proj(16, 128, 17, k=0.5, ang=35)
    p, q, r = math.sqrt(19), math.sqrt(6), math.sqrt(30)
    BX = {"1": (0, 0, 0), "2": (p, 0, 0), "3": (p, q, 0), "4": (0, q, 0), "5": (0, 0, r), "6": (p, 0, r), "7": (p, q, r), "8": (0, q, r)}
    f = _Fig(124, 140)
    _solid(f, P, view, BX, ["1234", "5678", "1265", "2376", "3487", "4158"], sw=0.7, col="#888")
    V = {"A": (0, 0, 0), "B": (p, q, 0), "C": (0, q, r), "D": (p, 0, r)}
    _solid(f, P, view, V, ["ABC", "ABD", "ACD", "BCD"], sw=1.5)
    _vlabels(f, P, V, "ABCD", d=8)
    f.T(_mid(P(*BX["1"]), P(*BX["2"])), "p", 0, 8, size=10, it=True)
    f.T(_mid(P(*BX["2"]), P(*BX["3"])), "q", 9, 6, size=10, it=True)
    f.T(_mid(P(*BX["2"]), P(*BX["6"])), "r", 7, 0, size=10, it=True)
    return f.svg()


# ---------------------------------------------------------------- 節7
SEC.append({"title": "空間図形への応用",
"base": r"""・空間図形は、必要な平面で切った<b>断面の三角形</b>を取り出し、正弦定理・余弦定理を使う。<br>
・四面体（錐体）の体積 $V=\dfrac13\times$（底面積）$\times$（高さ）。体積を2通りに表すと、点と平面の距離が求まる。内接球の半径 $r$ は　$V=\dfrac13r\times$（表面積）<br>
・$\mathrm{OA}=\mathrm{OB}=\mathrm{OC}$ の四面体 $\mathrm{OABC}$ では、$\mathrm{O}$ から平面 $\mathrm{ABC}$ に下ろした垂線の足は $\triangle\mathrm{ABC}$ の外心。<br>
・正四面体（1辺 $a$）：高さ $\dfrac{\sqrt6}{3}a$，体積 $\dfrac{\sqrt2}{12}a^3$。側面上の最短経路は展開図の線分。""",
"items": [
 {"lv": 2, "title": "空間の測量（2地点と仰角）",
  "q": _fig_tower3d() + r"水平な地面上の2地点 $\mathrm{A}$，$\mathrm{B}$ は $60\,\mathrm{m}$ 離れている。地面に垂直に立つ塔 $\mathrm{PQ}$ の根元 $\mathrm{Q}$ について $\angle\mathrm{QAB}=75^\circ$，$\angle\mathrm{QBA}=45^\circ$ であり、$\mathrm{A}$ から塔の先端 $\mathrm{P}$ を見上げた仰角は $30^\circ$ であった。塔の高さ $\mathrm{PQ}$ を求めよ。",
  "hint": r"地面上の $\triangle\mathrm{ABQ}$ は2角と1辺が分かるので正弦定理で $\mathrm{AQ}$ を求める。次に、鉛直な面の上の直角三角形 $\mathrm{PAQ}$ で仰角を使う。",
  "sol": r"$\triangle\mathrm{ABQ}$ で　$\angle\mathrm{AQB}=180^\circ-(75^\circ+45^\circ)=60^\circ$<br>"
         r"正弦定理より　$\dfrac{\mathrm{AQ}}{\sin45^\circ}=\dfrac{60}{\sin60^\circ}$　　$\mathrm{AQ}=60\cdot\dfrac{\sqrt2}{2}\cdot\dfrac{2}{\sqrt3}=\dfrac{60\sqrt2}{\sqrt3}=20\sqrt6$<br>"
         r"$\triangle\mathrm{PAQ}$ は $\angle\mathrm{PQA}=90^\circ$，$\angle\mathrm{PAQ}=30^\circ$ の直角三角形だから<br>"
         r"　$\mathrm{PQ}=\mathrm{AQ}\tan30^\circ=\dfrac{20\sqrt6}{\sqrt3}=\boldsymbol{20\sqrt2\,\mathrm{m}}$",
  "note": r"空間の問題でも、使う三角形は「水平面上の三角形」と「鉛直面上の直角三角形」の2つに分けて考える。",
  "ex": r"例題と同じ状況で、$\mathrm{AB}=100\,\mathrm{m}$，$\angle\mathrm{QAB}=60^\circ$，$\angle\mathrm{QBA}=75^\circ$，$\mathrm{B}$ から $\mathrm{P}$ を見上げた仰角が $45^\circ$ のとき、塔の高さを求めよ。",
  "exa": r"$50\sqrt6\,\mathrm{m}$"},
 {"lv": 3, "title": "直方体の切り口の三角形と点と平面の距離",
  "q": _fig_box() + r"直方体 $\mathrm{ABCD}$-$\mathrm{EFGH}$ において、$\mathrm{AB}=1$，$\mathrm{AD}=2$，$\mathrm{AE}=2$ である。<br>(1) $\cos\angle\mathrm{DBE}$ の値を求めよ。<br>(2) $\triangle\mathrm{BDE}$ の面積 $S$ を求めよ。<br>(3) 頂点 $\mathrm{A}$ から平面 $\mathrm{BDE}$ に下ろした垂線の長さ $h$ を求めよ。",
  "hint": r"$\triangle\mathrm{BDE}$ の3辺は各面の対角線なので三平方の定理で求まる。(3) は四面体 $\mathrm{ABDE}$ の体積を、底面 $\triangle\mathrm{ABD}$ と底面 $\triangle\mathrm{BDE}$ の2通りで表す。",
  "sol": r"$\mathrm{BD}=\sqrt{1^2+2^2}=\sqrt5$，$\mathrm{BE}=\sqrt{1^2+2^2}=\sqrt5$，$\mathrm{DE}=\sqrt{2^2+2^2}=2\sqrt2$<br>"
         r"(1) $\cos\angle\mathrm{DBE}=\dfrac{5+5-8}{2\sqrt5\cdot\sqrt5}=\boldsymbol{\dfrac15}$<br>"
         r"(2) $\sin\angle\mathrm{DBE}=\sqrt{1-\dfrac{1}{25}}=\dfrac{2\sqrt6}{5}$　　$S=\dfrac12\cdot\sqrt5\cdot\sqrt5\cdot\dfrac{2\sqrt6}{5}=\boldsymbol{\sqrt6}$<br>"
         r"(3) 四面体 $\mathrm{ABDE}$ の体積 $V$ は、底面 $\triangle\mathrm{ABD}$（面積 $1$）、高さ $\mathrm{AE}=2$ とみて　$V=\dfrac13\cdot1\cdot2=\dfrac23$<br>"
         r"底面を $\triangle\mathrm{BDE}$ とみると $V=\dfrac13Sh$ だから　$h=\dfrac{3V}{S}=\dfrac{2}{\sqrt6}=\boldsymbol{\dfrac{\sqrt6}{3}}$",
  "note": r"「体積を2通りに表す」ことで、垂線の足の位置を求めずに距離が分かる。この直方体の角の部分の四面体は、3辺が互いに垂直な四面体であり、後の例題の公式でも確かめられる。",
  "ex": r"直方体 $\mathrm{ABCD}$-$\mathrm{EFGH}$ において、$\mathrm{AB}=\mathrm{AD}=1$，$\mathrm{AE}=2$ である。$\cos\angle\mathrm{BED}$，$\triangle\mathrm{BDE}$ の面積、頂点 $\mathrm{A}$ から平面 $\mathrm{BDE}$ に下ろした垂線の長さを求めよ。",
  "exa": r"$\cos\angle\mathrm{BED}=\dfrac45$，面積 $\dfrac32$，垂線の長さ $\dfrac23$"},
 {"lv": 3, "title": "正四面体の高さ・体積・内接球・外接球",
  "q": r"1辺の長さが $6$ の正四面体 $\mathrm{ABCD}$ について、次のものを求めよ。<br>(1) 頂点 $\mathrm{A}$ から底面 $\mathrm{BCD}$ に下ろした垂線 $\mathrm{AH}$ の長さ　(2) 体積 $V$<br>(3) 内接球の半径 $r$　(4) 外接球の半径 $R$",
  "hint": r"$\mathrm{AB}=\mathrm{AC}=\mathrm{AD}$ だから $\mathrm{H}$ は $\triangle\mathrm{BCD}$ の外心で、$\mathrm{BH}$ は正弦定理で求まる。内接球は体積を4つの三角錐に分けて、外接球は中心が $\mathrm{AH}$ 上にあることを使う。",
  "sol": _fig_tetra() + r"(1) $\triangle\mathrm{ABH}$，$\triangle\mathrm{ACH}$，$\triangle\mathrm{ADH}$ は斜辺が $6$ で $\mathrm{AH}$ を共有する直角三角形なので合同。よって $\mathrm{BH}=\mathrm{CH}=\mathrm{DH}$ で、$\mathrm{H}$ は $\triangle\mathrm{BCD}$ の外心。<br>"
         r"正弦定理より $\mathrm{BH}=\dfrac{6}{2\sin60^\circ}=2\sqrt3$　　$\mathrm{AH}=\sqrt{6^2-(2\sqrt3)^2}=\boldsymbol{2\sqrt6}$<br>"
         r"(2) $\triangle\mathrm{BCD}=\dfrac12\cdot6^2\sin60^\circ=9\sqrt3$　　$V=\dfrac13\cdot9\sqrt3\cdot2\sqrt6=\boldsymbol{18\sqrt2}$<br>"
         r"(3) 内接球の中心 $\mathrm{I}$ と各面を底面とする4つの三角錐に分けると　$V=4\cdot\dfrac13\cdot9\sqrt3\cdot r=12\sqrt3\,r$<br>"
         r"　$r=\dfrac{18\sqrt2}{12\sqrt3}=\boldsymbol{\dfrac{\sqrt6}{2}}$<br>"
         r"(4) 外接球の中心 $\mathrm{O}$ は $\mathrm{B}$，$\mathrm{C}$，$\mathrm{D}$ から等距離なので、(1) と同様に $\mathrm{O}$ から平面 $\mathrm{BCD}$ への垂線の足は $\mathrm{H}$ で、$\mathrm{O}$ は直線 $\mathrm{AH}$ 上にある。$\mathrm{OA}=\mathrm{OB}=R$，$\mathrm{OH}=2\sqrt6-R$ だから、$\triangle\mathrm{OBH}$ で<br>"
         r"　$R^2=(2\sqrt6-R)^2+(2\sqrt3)^2$　　$4\sqrt6R=36$　　$R=\dfrac{9}{\sqrt6}=\boldsymbol{\dfrac{3\sqrt6}{2}}$",
  "note": r"$r=\dfrac14\mathrm{AH}$，$R=\dfrac34\mathrm{AH}$ で $r+R=\mathrm{AH}$。内接球と外接球の中心は一致する（正四面体の重心）。1辺 $a$ なら $r=\dfrac{\sqrt6}{12}a$，$R=\dfrac{\sqrt6}{4}a$。",
  "ex": r"1辺の長さが $4$ の正四面体について、高さ、体積、内接球の半径、外接球の半径を求めよ。",
  "exa": r"高さ $\dfrac{4\sqrt6}{3}$，体積 $\dfrac{16\sqrt2}{3}$，内接球の半径 $\dfrac{\sqrt6}{3}$，外接球の半径 $\sqrt6$"},
 {"lv": 3, "title": "円錐の側面上の最短経路（展開図）",
  "q": r"底面の半径が $2$、母線の長さが $6$ の直円錐がある。頂点を $\mathrm{O}$、底面の円周上の点を $\mathrm{A}$、母線 $\mathrm{OA}$ の中点を $\mathrm{M}$ とする。$\mathrm{A}$ から側面上を通って円錐のまわりを1周し、$\mathrm{M}$ に至る経路の長さの最小値を求めよ。",
  "hint": r"側面を母線 $\mathrm{OA}$ で切り開いた展開図（おうぎ形）では、最短経路は線分になる。中心角は「弧の長さ＝底面の円周」から求め、線分の長さは余弦定理で計算する。",
  "sol": _fig_sector() + r"側面の展開図は半径 $6$ のおうぎ形で、中心角を $x^\circ$ とすると、弧の長さが底面の円周に等しいから<br>"
         r"　$2\pi\cdot6\cdot\dfrac{x}{360}=2\pi\cdot2$　　$x=120$<br>"
         r"母線 $\mathrm{OA}$ で切り開いたとき、$\mathrm{A}$ の移る点を $\mathrm{A}$，$\mathrm{A'}$ とする。1周して $\mathrm{M}$ に至る経路は、展開図で $\mathrm{A}$ から線分 $\mathrm{OA'}$ 上の点 $\mathrm{M}$（$\mathrm{OM}=3$）に至る曲線になる。中心角 $120^\circ<180^\circ$ なので、線分 $\mathrm{AM}$ はおうぎ形の内部にあり、これが最短である。<br>"
         r"$\triangle\mathrm{OAM}$ で余弦定理より　$\mathrm{AM}^2=6^2+3^2-2\cdot6\cdot3\cos120^\circ=36+9+18=63$<br>"
         r"よって、最小値は　$\boldsymbol{3\sqrt7}$",
  "note": r"おうぎ形の中心角は $\dfrac{x}{360}=\dfrac{r}{l}$（$r$：底面の半径，$l$：母線の長さ）で求まる。中心角が $180^\circ$ より大きいときは、2点を結ぶ線分がおうぎ形の外を通ることがあり、そのまま線分の長さを答えにはできない。",
  "ex": r"底面の半径が $1$、母線の長さが $4$ の直円錐で、頂点を $\mathrm{O}$、底面の円周上の点を $\mathrm{A}$ とし、母線 $\mathrm{OA}$ 上に $\mathrm{OB}=3$ となる点 $\mathrm{B}$ をとる。$\mathrm{A}$ から側面を1周して $\mathrm{B}$ に至る経路の長さの最小値を求めよ。",
  "exa": r"$5$"},
 {"lv": 4, "title": "正四角錐の内接球と隣り合う側面のなす角",
  "q": _fig_pyr() + r"正四角錐 $\mathrm{O}$-$\mathrm{ABCD}$ において、底面の正方形の1辺は $6$、高さは $4$ である。<br>(1) 側面 $\triangle\mathrm{OAB}$ の面積を求めよ。<br>(2) 内接球（5つの面すべてに接する球）の半径 $r$ を求めよ。<br>(3) 側面 $\mathrm{OAB}$ と側面 $\mathrm{OBC}$ のなす角を $\theta$ とするとき、$\cos\theta$ の値を求めよ。",
  "hint": r"(2) は体積を、内接球の中心を頂点とする5つの角錐に分けて表す。(3) 2平面のなす角は、交線 $\mathrm{OB}$ に垂直な2直線のなす角。$\mathrm{A}$ から $\mathrm{OB}$ に垂線 $\mathrm{AE}$ を引くと、対称性から $\mathrm{CE}\perp\mathrm{OB}$ で、$\theta=\angle\mathrm{AEC}$ となる。",
  "sol": r"底面の正方形の中心を $\mathrm{H}$、辺 $\mathrm{AB}$ の中点を $\mathrm{M}$ とする。<br>"
         r"(1) $\mathrm{HM}=3$，$\mathrm{OH}=4$ より $\mathrm{OM}=5$。$\mathrm{OA}=\mathrm{OB}$ より $\mathrm{OM}\perp\mathrm{AB}$ だから　$\triangle\mathrm{OAB}=\dfrac12\cdot6\cdot5=\boldsymbol{15}$<br>"
         r"(2) 体積は $V=\dfrac13\cdot6^2\cdot4=48$。内接球の中心から5つの面までの距離はすべて $r$ なので<br>"
         r"　$V=\dfrac13r(36+4\cdot15)=32r$　　よって　$r=\boldsymbol{\dfrac32}$<br>"
         r"(3) $\mathrm{BH}=3\sqrt2$ より $\mathrm{OB}=\sqrt{4^2+(3\sqrt2)^2}=\sqrt{34}$。$\mathrm{A}$ から $\mathrm{OB}$ に垂線 $\mathrm{AE}$ を下ろすと　$\mathrm{AE}=\dfrac{2\triangle\mathrm{OAB}}{\mathrm{OB}}=\dfrac{30}{\sqrt{34}}$<br>"
         r"$\triangle\mathrm{OBA}\equiv\triangle\mathrm{OBC}$（3辺相等）だから、$\mathrm{C}$ から $\mathrm{OB}$ に下ろした垂線の足も $\mathrm{E}$ で $\mathrm{CE}=\mathrm{AE}$。よって $\theta=\angle\mathrm{AEC}$。$\mathrm{AC}=6\sqrt2$ だから<br>"
         r"　$\cos\theta=\dfrac{\mathrm{AE}^2+\mathrm{CE}^2-\mathrm{AC}^2}{2\mathrm{AE}\cdot\mathrm{CE}}=1-\dfrac{\mathrm{AC}^2}{2\mathrm{AE}^2}=1-\dfrac{72\cdot34}{2\cdot900}=1-\dfrac{34}{25}=\boldsymbol{-\dfrac{9}{25}}$",
  "note": r"(2) は、$\mathrm{O}$ と対辺の中点 $\mathrm{M}$，$\mathrm{N}$ を通る断面（3辺 $5,\ 5,\ 6$ の二等辺三角形）の内接円の半径 $\dfrac{12}{8}=\dfrac32$ としても求まる。(3) で $\cos\theta<0$ となり、隣り合う側面は鈍角で交わる。",
  "ex": r"正四角錐 $\mathrm{O}$-$\mathrm{ABCD}$ において、底面の正方形の1辺は $2$、側辺 $\mathrm{OA}$ の長さは $\sqrt3$ である。高さ、内接球の半径、隣り合う側面 $\mathrm{OAB}$，$\mathrm{OBC}$ のなす角 $\theta$ を求めよ。",
  "exa": r"高さ $1$，内接球の半径 $\sqrt2-1$，$\theta=120^\circ$"},
 {"lv": 4, "title": "3辺が互いに垂直な四面体の面積と高さ",
  "q": r"四面体 $\mathrm{OABC}$ において $\angle\mathrm{AOB}=\angle\mathrm{BOC}=\angle\mathrm{COA}=90^\circ$，$\mathrm{OA}=a$，$\mathrm{OB}=b$，$\mathrm{OC}=c$ とする。<br>(1) $\triangle\mathrm{ABC}$ の面積を $S$ とするとき、$S^2=(\triangle\mathrm{OAB})^2+(\triangle\mathrm{OBC})^2+(\triangle\mathrm{OCA})^2$ が成り立つことを証明せよ。<br>(2) $\mathrm{O}$ から平面 $\mathrm{ABC}$ に下ろした垂線の長さを $h$ とするとき、$\dfrac{1}{h^2}=\dfrac{1}{a^2}+\dfrac{1}{b^2}+\dfrac{1}{c^2}$ が成り立つことを証明せよ。",
  "hint": r"(1) $\triangle\mathrm{ABC}$ の3辺は三平方の定理で $a,\ b,\ c$ で表せる。余弦定理で $\cos\angle\mathrm{BAC}$、さらに $\sin^2\angle\mathrm{BAC}$ を求め、$S^2=\dfrac14\mathrm{AB}^2\mathrm{AC}^2\sin^2\angle\mathrm{BAC}$ を計算する。(2) は体積を2通りに表す。",
  "sol": r"(1) $\mathrm{AB}^2=a^2+b^2$，$\mathrm{AC}^2=a^2+c^2$，$\mathrm{BC}^2=b^2+c^2$。$\angle\mathrm{BAC}=\alpha$ とすると、余弦定理より<br>"
         r"　$\cos\alpha=\dfrac{\mathrm{AB}^2+\mathrm{AC}^2-\mathrm{BC}^2}{2\mathrm{AB}\cdot\mathrm{AC}}=\dfrac{a^2}{\mathrm{AB}\cdot\mathrm{AC}}$<br>"
         r"　$\sin^2\alpha=1-\dfrac{a^4}{\mathrm{AB}^2\mathrm{AC}^2}=\dfrac{(a^2+b^2)(a^2+c^2)-a^4}{\mathrm{AB}^2\mathrm{AC}^2}=\dfrac{a^2b^2+b^2c^2+c^2a^2}{\mathrm{AB}^2\mathrm{AC}^2}$<br>"
         r"よって　$S^2=\dfrac14\mathrm{AB}^2\mathrm{AC}^2\sin^2\alpha=\dfrac{a^2b^2+b^2c^2+c^2a^2}{4}=\left(\dfrac{ab}{2}\right)^2+\left(\dfrac{bc}{2}\right)^2+\left(\dfrac{ca}{2}\right)^2$<br>"
         r"これは $(\triangle\mathrm{OAB})^2+(\triangle\mathrm{OBC})^2+(\triangle\mathrm{OCA})^2$ に等しい。（証明終）<br>"
         r"(2) 四面体の体積は、底面 $\triangle\mathrm{OAB}$、高さ $c$ とみて $V=\dfrac16abc$。底面 $\triangle\mathrm{ABC}$ とみて $V=\dfrac13Sh$。よって $h=\dfrac{abc}{2S}$ で<br>"
         r"　$\dfrac{1}{h^2}=\dfrac{4S^2}{a^2b^2c^2}=\dfrac{a^2b^2+b^2c^2+c^2a^2}{a^2b^2c^2}=\dfrac{1}{c^2}+\dfrac{1}{a^2}+\dfrac{1}{b^2}$　（証明終）",
  "note": r"(1) は三平方の定理の空間版（ド・グアの定理）とよばれる。前の直方体の例題（$a=1,\ b=c=2$）では $S^2=1+4+1=6$，$\dfrac1{h^2}=1+\dfrac14+\dfrac14=\dfrac32$ で、結果と一致する。",
  "ex": r"$\angle\mathrm{AOB}=\angle\mathrm{BOC}=\angle\mathrm{COA}=90^\circ$，$\mathrm{OA}=2$，$\mathrm{OB}=3$，$\mathrm{OC}=6$ の四面体 $\mathrm{OABC}$ で、$\triangle\mathrm{ABC}$ の面積と、$\mathrm{O}$ から平面 $\mathrm{ABC}$ に下ろした垂線の長さを求めよ。",
  "exa": r"面積 $3\sqrt{14}$，垂線の長さ $\dfrac{3\sqrt{14}}{7}$"},
 {"lv": 5, "title": "4つの面が合同な四面体（直方体への埋め込み）",
  "q": r"四面体 $\mathrm{ABCD}$ において、$\mathrm{AB}=\mathrm{CD}=5$，$\mathrm{AC}=\mathrm{BD}=6$，$\mathrm{AD}=\mathrm{BC}=7$ である。この四面体の体積 $V$ と、外接球の半径 $R$ を求めよ。",
  "hint": r"向かい合う辺の長さが等しく、4つの面はすべて3辺が $5,\ 6,\ 7$ の合同な三角形。このような四面体は、<b>直方体の面の対角線を辺とする四面体</b>として直方体に埋め込める。直方体の3辺を $p,\ q,\ r$ とおいて連立方程式を解く。",
  "sol": _fig_boxtet() + r"3辺の長さが $p,\ q,\ r$ の直方体で<br>"
         r"　$p^2+q^2=25$，$q^2+r^2=36$，$r^2+p^2=49$　…①<br>"
         r"となるものを考える。辺々加えて $p^2+q^2+r^2=55$ だから $p^2=19$，$q^2=6$，$r^2=30$ で、いずれも正なのでこの直方体は存在する。<br>"
         r"直方体の頂点を図のように1つおきに4つとって $\mathrm{A}$，$\mathrm{B}$，$\mathrm{C}$，$\mathrm{D}$ とすると、6辺はすべて面の対角線で、向かい合う辺は向かい合う面の対角線だから、①より $\mathrm{AB}=\mathrm{CD}=5$，$\mathrm{AC}=\mathrm{BD}=6$，$\mathrm{AD}=\mathrm{BC}=7$ となる。<br>"
         r"四面体は6辺の長さで決まる（$\triangle\mathrm{ABC}$ が決まり、$\mathrm{D}$ は $\mathrm{A}$，$\mathrm{B}$，$\mathrm{C}$ からの距離で平面 $\mathrm{ABC}$ に関して対称な2点のどちらかに決まる）ので、与えられた四面体はこの四面体と合同である。<br>"
         r"直方体から、4すみの三角錐（体積はどれも $\dfrac13\cdot\dfrac12pq\cdot r=\dfrac16pqr$）を除いたものが四面体だから<br>"
         r"　$V=pqr-4\cdot\dfrac16pqr=\dfrac13pqr=\dfrac13\sqrt{19\cdot6\cdot30}=\dfrac{6\sqrt{95}}{3}=\boldsymbol{2\sqrt{95}}$<br>"
         r"また、直方体の8頂点は直方体の中心から等距離 $\dfrac12\sqrt{p^2+q^2+r^2}$ にあるので、その球が $\mathrm{A}$，$\mathrm{B}$，$\mathrm{C}$，$\mathrm{D}$ を通る。同じ平面上にない4点を通る球はただ1つだから<br>"
         r"　$R=\dfrac12\sqrt{55}=\boldsymbol{\dfrac{\sqrt{55}}{2}}$",
  "note": r"一般に、向かい合う辺が $a,\ b,\ c$ の等面四面体の体積は $V=\sqrt{\dfrac{(a^2+b^2-c^2)(b^2+c^2-a^2)(c^2+a^2-b^2)}{72}}$。①で $p^2,\ q^2,\ r^2>0$ となるのは、面の三角形が鋭角三角形のときに限る（$5^2+6^2>7^2$）。",
  "ex": r"四面体 $\mathrm{ABCD}$ において、$\mathrm{AB}=\mathrm{CD}=4$，$\mathrm{AC}=\mathrm{BD}=5$，$\mathrm{AD}=\mathrm{BC}=6$ である。この四面体の体積と外接球の半径を求めよ。",
  "exa": r"体積 $\dfrac{15\sqrt6}{4}$，外接球の半径 $\dfrac{\sqrt{154}}{4}$"},
]})

# ---------------------------------------------------------------- 図：節8
def _fig_fermat():  # 回転による折れ線の一直線化
    s, ox, oy = 64, 22, 80
    r3 = math.sqrt(3)
    T = lambda x, y: (ox + s * x, oy - s * y)
    B, A, C, C2 = T(0, 0), T(0, 1), T(r3, 0), T(r3 / 2, -1.5)
    Pp, P2 = T(r3 / 7, 2 / 7), T(3 * r3 / 14, -1 / 14)
    f = _Fig(150, 188)
    f.PL([A, B, C], sw=1.3)
    f.PL([B, C, C2], dash=True, sw=0.9)
    f.L(A, C2, sw=1.0, col="#c0392b")
    f.L(Pp, B, sw=0.9); f.L(Pp, C, sw=0.9); f.L(P2, B, sw=0.8, dash=True)
    f.right(B, A, C, s=6)
    for q, t, dx, dy in ((A, "A", -8, -2), (B, "B", -8, 3), (C, "C", 7, -4), (C2, "C′", 7, 5), (Pp, "P", 2, -9), (P2, "P′", 10, 2)):
        f.dot(q, r=1.6); f.T(q, t, dx, dy, size=10)
    return f.svg()


def _fig_hex():  # 立方体を対角線に垂直な平面で切る（中央の正六角形）
    P, view = _proj(18, 116, 80, k=0.5, ang=35)
    V = {"A": (0, 0, 0), "B": (1, 0, 0), "C": (1, 1, 0), "D": (0, 1, 0), "E": (0, 0, 1), "F": (1, 0, 1), "G": (1, 1, 1), "H": (0, 1, 1)}
    hx = [(1, .5, 0), (1, 0, .5), (.5, 0, 1), (0, .5, 1), (0, 1, .5), (.5, 1, 0)]
    f = _Fig(150, 134)
    f.PL([P(*q) for q in hx], fill="#dfe8f7", sw=1.3)
    _solid(f, P, view, V, ["ABCD", "EFGH", "ABFE", "BCGF", "CDHG", "DAEH"], sw=1.0)
    f.L(P(*V["A"]), P(*V["G"]), dash=True, sw=0.8, col="#c0392b")
    f.dot(P(.5, .5, .5), r=1.6); f.T(P(.5, .5, .5), "P", 7, 5, size=10)
    _vlabels(f, P, V, "ABCDEFGH", d=8, size=10)
    return f.svg()


# ---------------------------------------------------------------- 節8
SEC.append({"title": "図形の最大・最小",
"base": r"""・辺や角を1つの文字で表し、2次関数の最大・最小に帰着させる。<b>文字の変域</b>（三角形の成立条件、点が辺上にある条件）を必ず確かめる。<br>
・$(b-c)^2\geqq0$ から $b^2+c^2\geqq2bc$，$(b+c)^2\geqq4bc$。実数 $b,\ c$ が存在する条件（判別式）も範囲を絞る道具になる。最後に等号が成り立つ例を示す。<br>
・空間の最短経路は展開図で、折れ線の長さの和は回転移動で一直線に並べて評価する。""",
"items": [
 {"lv": 3, "title": "2辺の和が一定の三角形の対辺の最小",
  "q": r"$\triangle\mathrm{ABC}$ において $A=60^\circ$，$b+c=6$ のとき、$a$ の最小値と、そのときの $\triangle\mathrm{ABC}$ の面積を求めよ。",
  "hint": r"$c=6-b$ として余弦定理で $a^2$ を $b$ の2次関数で表す。$b,\ c>0$ から変域は $0<b<6$。",
  "sol": r"$c=6-b$（$0<b<6$）とおく。余弦定理より<br>"
         r"　$a^2=b^2+c^2-2bc\cos60^\circ=(b+c)^2-3bc=36-3b(6-b)=3b^2-18b+36=3(b-3)^2+9$<br>"
         r"$0<b<6$ において $a^2$ は $b=3$ のとき最小値 $9$ をとる。$a>0$ だから、$a$ の最小値は $\boldsymbol{3}$（$b=c=3$）。<br>"
         r"このとき面積は　$\dfrac12\cdot3\cdot3\sin60^\circ=\boldsymbol{\dfrac{9\sqrt3}{4}}$",
  "note": r"最小となるのは $b=c=3$，$a=3$ の正三角形。$b+c$ が一定のとき、$a^2=(b+c)^2-3bc$ を最小にするには積 $bc$ を最大にすればよく、$bc\leqq\left(\dfrac{b+c}{2}\right)^2$ からも分かる。",
  "ex": r"$\triangle\mathrm{ABC}$ において $A=120^\circ$，$b+c=4$ のとき、$a$ の最小値と、そのときの面積を求めよ。",
  "exa": r"$a$ の最小値 $2\sqrt3$，面積 $\sqrt3$"},
 {"lv": 4, "title": "正四面体の辺上を動く点と三角形の面積・角の最大最小",
  "q": r"1辺の長さが $6$ の正四面体 $\mathrm{ABCD}$ の辺 $\mathrm{AB}$ 上に点 $\mathrm{P}$ をとり、$\mathrm{AP}=t$（$0\leqq t\leqq6$）とする。<br>(1) $\mathrm{PC}^2$ を $t$ で表せ。<br>(2) $\triangle\mathrm{PCD}$ の面積 $S$ の最小値を求めよ。<br>(3) $\angle\mathrm{CPD}$ の最大値を $\theta$ とするとき、$\cos\theta$ の値を求めよ。",
  "hint": r"$\triangle\mathrm{APC}$ で余弦定理。対称性から $\mathrm{PC}=\mathrm{PD}$ なので、$\mathrm{CD}$ の中点 $\mathrm{M}$ をとると $\mathrm{PM}\perp\mathrm{CD}$ で、$S=\dfrac12\cdot\mathrm{CD}\cdot\mathrm{PM}$。(3) は $\cos\angle\mathrm{CPD}$ を $\mathrm{PC}^2$ で表し、その増減を見る。",
  "sol": r"(1) $\triangle\mathrm{APC}$ で $\mathrm{AC}=6$，$\angle\mathrm{PAC}=60^\circ$ だから　$\mathrm{PC}^2=t^2+36-2\cdot6t\cos60^\circ=\boldsymbol{t^2-6t+36}$<br>"
         r"(2) 同様に $\triangle\mathrm{APD}$ で $\mathrm{PD}^2=t^2-6t+36$ なので $\mathrm{PC}=\mathrm{PD}$。$\mathrm{CD}$ の中点を $\mathrm{M}$ とすると $\mathrm{PM}\perp\mathrm{CD}$ で<br>"
         r"　$\mathrm{PM}^2=\mathrm{PC}^2-3^2=t^2-6t+27=(t-3)^2+18$<br>"
         r"$0\leqq t\leqq6$ で $\mathrm{PM}^2$ は $t=3$ のとき最小値 $18$。よって $S=\dfrac12\cdot6\cdot\mathrm{PM}$ の最小値は　$3\cdot3\sqrt2=\boldsymbol{9\sqrt2}$<br>"
         r"(3) $\triangle\mathrm{PCD}$ で余弦定理より　$\cos\angle\mathrm{CPD}=\dfrac{\mathrm{PC}^2+\mathrm{PD}^2-36}{2\mathrm{PC}\cdot\mathrm{PD}}=\dfrac{2\mathrm{PC}^2-36}{2\mathrm{PC}^2}=1-\dfrac{18}{\mathrm{PC}^2}$<br>"
         r"$\mathrm{PC}^2=(t-3)^2+27\geqq27$ だから　$\cos\angle\mathrm{CPD}\geqq1-\dfrac{18}{27}=\dfrac13$（等号は $t=3$）<br>"
         r"$0^\circ<\angle\mathrm{CPD}<180^\circ$ では、$\cos$ の値が小さいほど角は大きいので、$\angle\mathrm{CPD}$ は $t=3$ で最大となり　$\cos\theta=\boldsymbol{\dfrac13}$",
  "note": r"$t=3$（$\mathrm{P}$ が $\mathrm{AB}$ の中点）のとき、$\mathrm{PM}$ は $\mathrm{AB}$ と $\mathrm{CD}$ の両方に垂直になり、$\mathrm{PM}=3\sqrt2$ はねじれの位置にある2辺 $\mathrm{AB}$，$\mathrm{CD}$ の距離である。",
  "ex": r"1辺の長さが $6$ の正四面体 $\mathrm{ABCD}$ の辺 $\mathrm{AB}$ 上の点 $\mathrm{P}$ と、辺 $\mathrm{CD}$ 上の点 $\mathrm{Q}$ を考える。線分 $\mathrm{PQ}$ の長さの最小値を求めよ。",
  "exa": r"$3\sqrt2$（$\mathrm{P}$，$\mathrm{Q}$ がそれぞれ $\mathrm{AB}$，$\mathrm{CD}$ の中点のとき）"},
 {"lv": 4, "title": "外接円の半径が一定の三角形の内接円の半径の最大",
  "q": r"半径 $1$ の円に内接する $\triangle\mathrm{ABC}$ において $A=60^\circ$ とする。<br>(1) $a$ を求めよ。　(2) $b+c$ のとり得る値の範囲を求めよ。　(3) 内接円の半径 $r$ の最大値を求めよ。",
  "hint": r"(2) $b+c=t$ とおくと、余弦定理から $bc$ が $t$ で表せる。$b,\ c$ は「和 $t$、積 $bc$」の2次方程式の<b>正の実数解</b>なので、判別式と積の符号から $t$ の範囲が決まる。(3) $r=\dfrac{2S}{a+b+c}$ を $t$ で表す。",
  "sol": r"(1) 正弦定理より　$a=2\cdot1\cdot\sin60^\circ=\boldsymbol{\sqrt3}$<br>"
         r"(2) $b+c=t$ とおく。余弦定理より $3=b^2+c^2-bc=t^2-3bc$ だから　$bc=\dfrac{t^2-3}{3}$<br>"
         r"$b,\ c$ は $x^2-tx+\dfrac{t^2-3}{3}=0$ の2つの正の解（重解を含む）である。その条件は<br>"
         r"　判別式 $t^2-\dfrac{4(t^2-3)}{3}=\dfrac{12-t^2}{3}\geqq0$，和 $t>0$，積 $\dfrac{t^2-3}{3}>0$<br>"
         r"これより $\sqrt3<t\leqq2\sqrt3$。逆にこのとき、正の数 $b,\ c$ で $b^2+c^2-bc=3$ となるものがあり、$A=60^\circ$，$a=\sqrt3$ の三角形ができて外接円の半径は $\dfrac{a}{2\sin A}=1$ となる。<br>"
         r"よって　$\boldsymbol{\sqrt3<b+c\leqq2\sqrt3}$<br>"
         r"(3) $S=\dfrac12bc\sin60^\circ=\dfrac{\sqrt3(t^2-3)}{12}$ だから<br>"
         r"　$r=\dfrac{2S}{a+b+c}=\dfrac{\sqrt3(t^2-3)}{6(t+\sqrt3)}=\dfrac{\sqrt3(t-\sqrt3)}{6}$<br>"
         r"これは $t$ について増加するので、$t=2\sqrt3$（$b=c=\sqrt3$）のとき最大で、最大値は　$\dfrac{\sqrt3\cdot\sqrt3}{6}=\boldsymbol{\dfrac12}$",
  "note": r"最大となるのは正三角形のときで、$r=\dfrac R2$。一般に $r\leqq\dfrac R2$ が成り立つ（オイラーの不等式）。和と積で表したら、<b>実数条件</b>を忘れずに変域を出すのが要点。",
  "ex": r"半径 $1$ の円に内接する $\triangle\mathrm{ABC}$ において $A=120^\circ$ とする。$b+c$ のとり得る値の範囲と、内接円の半径 $r$ の最大値を求めよ。",
  "exa": r"$\sqrt3<b+c\leqq2$，$r$ の最大値 $\dfrac{2\sqrt3-3}{2}$"},
 {"lv": 5, "title": "3頂点からの距離の和の最小（回転移動）",
  "q": r"$\angle\mathrm{B}=90^\circ$，$\mathrm{AB}=1$，$\mathrm{BC}=\sqrt3$ の直角三角形 $\mathrm{ABC}$ がある。平面上の点 $\mathrm{P}$ について、$\mathrm{PA}+\mathrm{PB}+\mathrm{PC}$ の最小値を求めよ。",
  "hint": r"$\triangle\mathrm{PBC}$ を $\mathrm{B}$ を中心に $60^\circ$ 回転して $\triangle\mathrm{P'BC'}$ をつくると、$\mathrm{PB}=\mathrm{PP'}$（$\triangle\mathrm{BPP'}$ は正三角形）、$\mathrm{PC}=\mathrm{P'C'}$。3つの線分が折れ線 $\mathrm{A}\to\mathrm{P}\to\mathrm{P'}\to\mathrm{C'}$ に並ぶので、その長さは線分 $\mathrm{AC'}$ 以上。<b>等号が成り立つ P を実際に示す</b>ことも必要。",
  "sol": _fig_fermat() + r"$\mathrm{B}$ を中心として $\mathrm{C}$ を $\mathrm{A}$ と反対の側へ $60^\circ$ 回転した点を $\mathrm{C'}$ とする（$\triangle\mathrm{BCC'}$ は正三角形）。点 $\mathrm{P}$ がこの回転で移る点を $\mathrm{P'}$ とすると、$\mathrm{BP}=\mathrm{BP'}$，$\angle\mathrm{PBP'}=60^\circ$ より $\triangle\mathrm{BPP'}$ は正三角形で $\mathrm{PB}=\mathrm{PP'}$。また、線分 $\mathrm{PC}$ は線分 $\mathrm{P'C'}$ に移るので $\mathrm{PC}=\mathrm{P'C'}$。よって<br>"
         r"　$\mathrm{PA}+\mathrm{PB}+\mathrm{PC}=\mathrm{AP}+\mathrm{PP'}+\mathrm{P'C'}\geqq\mathrm{AC'}$　…①<br>"
         r"$\angle\mathrm{ABC'}=90^\circ+60^\circ=150^\circ$，$\mathrm{BC'}=\sqrt3$ だから、余弦定理より<br>"
         r"　$\mathrm{AC'}^2=1+3-2\cdot1\cdot\sqrt3\cos150^\circ=7$　　$\mathrm{AC'}=\sqrt7$<br>"
         r"<b>等号が成り立つ P の存在</b>：$\triangle\mathrm{ABC'}$ で $\cos\angle\mathrm{BAC'}=\dfrac{1+7-3}{2\sqrt7}=\dfrac{5}{2\sqrt7}$，$\sin\angle\mathrm{BAC'}=\dfrac{\sqrt3}{2\sqrt7}$。$\mathrm{B}$ から直線 $\mathrm{AC'}$ に下ろした垂線の足を $\mathrm{H}$ とすると　$\mathrm{BH}=\dfrac{\sqrt3}{2\sqrt7}$，$\mathrm{AH}=\dfrac{5}{2\sqrt7}$<br>"
         r"線分 $\mathrm{AC'}$ 上に、$\mathrm{AP}=\mathrm{AH}-\dfrac{\mathrm{BH}}{\sqrt3}=\dfrac{2}{\sqrt7}$，$\mathrm{AQ}=\mathrm{AH}+\dfrac{\mathrm{BH}}{\sqrt3}=\dfrac{3}{\sqrt7}$ となる点 $\mathrm{P}$，$\mathrm{Q}$ をとる（$\mathrm{AQ}<\mathrm{AC'}$）。$\mathrm{PH}=\mathrm{QH}=\dfrac{\mathrm{BH}}{\sqrt3}$ より<br>"
         r"　$\mathrm{BP}=\mathrm{BQ}=\sqrt{\mathrm{BH}^2+\dfrac{\mathrm{BH}^2}{3}}=\dfrac{2\mathrm{BH}}{\sqrt3}=\dfrac{1}{\sqrt7}$，$\mathrm{PQ}=\dfrac{2\mathrm{BH}}{\sqrt3}=\dfrac{1}{\sqrt7}$<br>"
         r"だから $\triangle\mathrm{BPQ}$ は正三角形。$\mathrm{P}$ より $\mathrm{Q}$ のほうが $\mathrm{C'}$ に近いので、$\mathrm{Q}$ は $\mathrm{P}$ を $\mathrm{C}$ から $\mathrm{C'}$ へ回す向きに $60^\circ$ 回転した点、すなわち $\mathrm{Q}=\mathrm{P'}$ である。このとき4点 $\mathrm{A}$，$\mathrm{P}$，$\mathrm{P'}$，$\mathrm{C'}$ はこの順に一直線上にあり、①で等号が成り立つ。<br>"
         r"よって、最小値は　$\boldsymbol{\sqrt7}$",
  "note": r"等号が成り立つ点では $\mathrm{PA}=\dfrac2{\sqrt7}$，$\mathrm{PB}=\dfrac1{\sqrt7}$，$\mathrm{PC}=\mathrm{AC'}-\mathrm{AP'}=\dfrac4{\sqrt7}$ で、$\angle\mathrm{APB}=\angle\mathrm{BPC}=\angle\mathrm{CPA}=120^\circ$ となる（フェルマー点）。内角がすべて $120^\circ$ 未満の三角形なら、同じ方法で最小値が求まる。",
  "ex": r"$\mathrm{AB}=2$，$\mathrm{BC}=3$，$\angle\mathrm{B}=60^\circ$ の $\triangle\mathrm{ABC}$ がある。平面上の点 $\mathrm{P}$ について、$\mathrm{PA}+\mathrm{PB}+\mathrm{PC}$ の最小値を求めよ。",
  "exa": r"$\sqrt{19}$"},
 {"lv": 5, "title": "立方体を対角線に垂直な平面で切った切り口の面積の最大",
  "q": _fig_hex() + r"1辺の長さが $1$ の立方体 $\mathrm{ABCD}$-$\mathrm{EFGH}$ がある。対角線 $\mathrm{AG}$ 上に点 $\mathrm{P}$ をとり、$\mathrm{P}$ を通り $\mathrm{AG}$ に垂直な平面 $\alpha$ で立方体を切る。$\mathrm{AP}=x$（$0<x<\sqrt3$）とし、切り口の面積を $S$ とする。<br>(1) 切り口が六角形になるような $x$ の値の範囲を求めよ。<br>(2) $S$ の最大値と、そのときの $x$ の値を求めよ。",
  "hint": r"$\alpha$ は対称性から直線 $\mathrm{AB}$，$\mathrm{AD}$，$\mathrm{AE}$ と、$\mathrm{A}$ から等しい距離 $t$ の点で交わる。$t$ と $x$ の関係を $\cos\angle\mathrm{BAG}$ で求める。六角形のときは、1辺 $\sqrt2t$ の大きな正三角形から、立方体の外にはみ出した3つの小さな正三角形を除いたものとみる。",
  "sol": r"$\mathrm{AG}=\sqrt3$，$\triangle\mathrm{ABG}$ は $\angle\mathrm{ABG}=90^\circ$ の直角三角形だから $\cos\angle\mathrm{BAG}=\dfrac{1}{\sqrt3}$。$\alpha$ と直線 $\mathrm{AB}$ の交点を $\mathrm{Q}$ とすると $\mathrm{PQ}\perp\mathrm{AP}$ だから $\mathrm{AQ}=\dfrac{\mathrm{AP}}{\cos\angle\mathrm{BAG}}=\sqrt3x$。直線 $\mathrm{AD}$，$\mathrm{AE}$ との交点 $\mathrm{R}$，$\mathrm{T}$ も同様で、$\mathrm{AQ}=\mathrm{AR}=\mathrm{AT}=t$（$t=\sqrt3x$，$0<t<3$）。$\triangle\mathrm{QRT}$ は1辺 $\sqrt2t$ の正三角形である。<br>"
         r"(i) $0<t\leqq1$ のとき、$\mathrm{Q}$，$\mathrm{R}$，$\mathrm{T}$ は辺上にあり、切り口は $\triangle\mathrm{QRT}$：$S=\dfrac{\sqrt3}{4}(\sqrt2t)^2=\dfrac{\sqrt3}{2}t^2$<br>"
         r"(ii) $1<t<2$ のとき、$\mathrm{Q}$ は辺 $\mathrm{AB}$ の延長上にある。平面 $\mathrm{ABCD}$ 上で直線 $\mathrm{QR}$ は $\angle\mathrm{AQR}=45^\circ$ だから、辺 $\mathrm{BC}$ と $\mathrm{B}$ から $t-1$ の点で交わる。同様に直線 $\mathrm{QT}$ は辺 $\mathrm{BF}$ と $\mathrm{B}$ から $t-1$ の点で交わる。よって $\mathrm{Q}$ の付近で立方体からはみ出す部分は1辺 $\sqrt2(t-1)$ の正三角形で、$\mathrm{R}$，$\mathrm{T}$ の付近も同様。$t<2$ よりこれら3つは重ならないから、切り口は六角形で<br>"
         r"　$S=\dfrac{\sqrt3}{2}\{t^2-3(t-1)^2\}=\dfrac{\sqrt3}{2}(-2t^2+6t-3)$<br>"
         r"(iii) $2\leqq t<3$ のとき、立方体の中心に関する対称性（$\mathrm{A}$ と $\mathrm{G}$ を入れかえる）により、$\mathrm{G}$ の側から (i) と同じ形になり、切り口は三角形：$S=\dfrac{\sqrt3}{2}(3-t)^2$<br>"
         r"(1) 六角形になるのは $1<t<2$，すなわち $\boldsymbol{\dfrac{\sqrt3}{3}<x<\dfrac{2\sqrt3}{3}}$<br>"
         r"(2) (i) では $S\leqq\dfrac{\sqrt3}{2}$，(iii) でも $S\leqq\dfrac{\sqrt3}{2}$。(ii) では $-2t^2+6t-3=-2\left(t-\dfrac32\right)^2+\dfrac32\leqq\dfrac32$ で、$S\leqq\dfrac{3\sqrt3}{4}$（等号は $t=\dfrac32$）。$\dfrac{3\sqrt3}{4}>\dfrac{\sqrt3}{2}$ だから<br>"
         r"　$S$ の最大値は $\boldsymbol{\dfrac{3\sqrt3}{4}}$，そのとき $x=\dfrac{t}{\sqrt3}=\boldsymbol{\dfrac{\sqrt3}{2}}$（$\mathrm{P}$ は $\mathrm{AG}$ の中点）",
  "note": r"最大のときの切り口は、各辺の中点を結ぶ1辺 $\dfrac{\sqrt2}{2}$ の正六角形（図）。$S$ を $t$ の式で表すと $t=1,\ 2$ でつながった1つの山形のグラフになる。「大きな図形から余分を引く」発想が、場合分けの多い切り口の面積を簡潔にする。",
  "ex": r"例題と同じ設定で、切り口の周の長さを $L$ とする。$L$ の最大値と、$L$ が最大となる $x$ の値の範囲を求めよ。",
  "exa": r"最大値 $3\sqrt2$（$\dfrac{\sqrt3}{3}\leqq x\leqq\dfrac{2\sqrt3}{3}$ のとき）"},
 {"lv": 5, "title": "辺の長さが変化する四面体の体積の最大",
  "q": r"四面体 $\mathrm{ABCD}$ において、$\mathrm{AC}=\mathrm{AD}=\mathrm{BC}=\mathrm{BD}=1$，$\mathrm{AB}=\mathrm{CD}=x$ とする。<br>(1) $x$ のとり得る値の範囲を求めよ。　(2) 体積 $V$ を $x$ で表せ。　(3) $V$ の最大値と、そのときの $x$ の値を求めよ。",
  "hint": r"$\mathrm{AB}$ の中点 $\mathrm{M}$，$\mathrm{CD}$ の中点 $\mathrm{N}$ をとると、二等辺三角形の性質から $\mathrm{AB}\perp$ 平面 $\mathrm{MCD}$，$\mathrm{MN}\perp\mathrm{CD}$。体積は平面 $\mathrm{MCD}$ で2つに分けて求める。(3) は $u=x^2$ の3次式の最大で、<b>微分を使わずに</b>、最大となる値 $u=\dfrac43$ との差を $(u-\alpha)^2(\cdots)$ の形に因数分解して評価する。",
  "sol": r"(1)(2) $\mathrm{AB}$ の中点を $\mathrm{M}$，$\mathrm{CD}$ の中点を $\mathrm{N}$ とする。$\triangle\mathrm{CAB}$ は $\mathrm{CA}=\mathrm{CB}=1$ の二等辺三角形だから　$\mathrm{CM}\perp\mathrm{AB}$，$\mathrm{CM}^2=1-\dfrac{x^2}{4}$<br>"
         r"同様に $\mathrm{DM}\perp\mathrm{AB}$，$\mathrm{DM}=\mathrm{CM}$。よって $\mathrm{AB}$ は平面 $\mathrm{MCD}$ 上の交わる2直線に垂直で、$\mathrm{AB}\perp$ 平面 $\mathrm{MCD}$。<br>"
         r"$\triangle\mathrm{MCD}$ は $\mathrm{MC}=\mathrm{MD}$ の二等辺三角形だから　$\mathrm{MN}\perp\mathrm{CD}$，$\mathrm{MN}^2=\mathrm{MC}^2-\dfrac{x^2}{4}=1-\dfrac{x^2}{2}$<br>"
         r"四面体ができるためには $\triangle\mathrm{MCD}$ がつぶれないこと、すなわち $\mathrm{MN}>0$ が必要で、$0<x<\sqrt2$。逆に $0<x<\sqrt2$ なら、長さ $x$ の線分 $\mathrm{AB}$ の中点 $\mathrm{M}$ を通り $\mathrm{AB}$ に垂直な平面上に、$\mathrm{MC}=\mathrm{MD}=\sqrt{1-\dfrac{x^2}{4}}$，$\mathrm{CD}=x$ となる2点がとれ（$x<2\sqrt{1-\dfrac{x^2}{4}}\iff x^2<2$）、条件を満たす四面体ができる。よって　$\boldsymbol{0<x<\sqrt2}$<br>"
         r"四面体を平面 $\mathrm{MCD}$ で、$\triangle\mathrm{MCD}$ を底面とし高さ $\mathrm{AM}$，$\mathrm{BM}$ の2つの三角錐に分けると<br>"
         r"　$V=\dfrac13\triangle\mathrm{MCD}\cdot(\mathrm{AM}+\mathrm{BM})=\dfrac13\cdot\dfrac12x\sqrt{1-\dfrac{x^2}{2}}\cdot x=\boldsymbol{\dfrac{x^2}{6}\sqrt{1-\dfrac{x^2}{2}}}$<br>"
         r"(3) $u=x^2$（$0<u<2$）とおくと　$V^2=\dfrac{u^2}{36}\left(1-\dfrac u2\right)=\dfrac{u^2(2-u)}{72}$<br>"
         r"ここで　$\dfrac{32}{27}-u^2(2-u)=u^3-2u^2+\dfrac{32}{27}=\left(u-\dfrac43\right)^2\left(u+\dfrac23\right)\geqq0$<br>"
         r"よって $u^2(2-u)\leqq\dfrac{32}{27}$（等号は $u=\dfrac43$）で、$V^2\leqq\dfrac{32}{27\cdot72}=\dfrac{4}{243}$，$V\leqq\dfrac{2}{9\sqrt3}=\dfrac{2\sqrt3}{27}$<br>"
         r"$u=\dfrac43$，すなわち $x=\dfrac{2}{\sqrt3}$ は範囲内だから、最大値は $\boldsymbol{\dfrac{2\sqrt3}{27}}$，そのとき $\boldsymbol{x=\dfrac{2\sqrt3}{3}}$",
  "note": r"$\dfrac43$ は、$u^3-2u^2+k=0$ が重解 $\alpha$ をもつような $k$ を探して見つける：$u^3-2u^2+k=(u-\alpha)^2(u-\beta)$ とおき係数を比べると $2\alpha+\beta=2$，$\alpha^2+2\alpha\beta=0$ から $\beta=-\dfrac\alpha2$，$\alpha=\dfrac43$。数学IIの微分法を使えば機械的に求まるが、因数分解による評価は等号成立条件まで一度に示せる。",
  "ex": r"四面体 $\mathrm{OABC}$ において $\mathrm{OA}=\mathrm{OB}=\mathrm{OC}=1$，$\angle\mathrm{AOB}=\angle\mathrm{BOC}=\angle\mathrm{COA}=\theta$（$0^\circ<\theta<120^\circ$）とする。体積 $V$ を $\cos\theta$ で表し、$V$ の最大値を求めよ。",
  "exa": r"$V=\dfrac16(1-\cos\theta)\sqrt{1+2\cos\theta}$，最大値 $\dfrac16$（$\theta=90^\circ$）"},
]})

CH = {"no": 3, "sections": SEC}


# ================================================================ 検算
def verify():
    import random
    import sympy as sp
    from sympy import sqrt, Rational as R, pi, sin, cos, tan, acos, atan, Symbol
    rnd = random.Random(3)

    def eq(a, b):
        a, b = sp.sympify(a), sp.sympify(b)
        if sp.simplify(sp.radsimp(a - b)) == 0:
            return
        assert abs(sp.N(a - b, 80)) < sp.Float(10) ** -60, (a, b)

    dg = lambda x: pi * sp.sympify(x) / 180

    # ---- 節1
    AC = sqrt(4**2 - 3**2); eq(AC, sqrt(7))
    eq(R(3, 4), 3 / R(4)); eq(AC / 4, sqrt(7) / 4); eq(3 / AC, 3 * sqrt(7) / 7)
    eq(R(3, 4)**2 + (sqrt(7) / 4)**2, 1)
    AC2 = sqrt(2**2 + 5); eq(AC2, 3)
    eq(2 / AC2, R(2, 3)); eq(sqrt(5) / AC2, sqrt(5) / 3); eq(2 / sqrt(5), 2 * sqrt(5) / 5)
    t = acos(R(2, 5)); eq(sin(t), sqrt(21) / 5); eq(tan(t), sqrt(21) / 2)
    t = atan(3); eq(cos(t), sqrt(10) / 10); eq(sin(t), 3 * sqrt(10) / 10)
    t = sp.asin(R(2, 3)); eq(cos(t), sqrt(5) / 3); eq(tan(t), 2 * sqrt(5) / 5)
    t = atan(R(1, 2)); eq(cos(t), 2 * sqrt(5) / 5); eq(sin(t), sqrt(5) / 5)
    eq(sin(dg(25)) * cos(dg(65)) + cos(dg(25)) * sin(dg(65)), 1)
    eq(tan(dg(10)) * tan(dg(20)) * tan(dg(70)) * tan(dg(80)), 1)
    for _ in range(50):
        A_, B_ = rnd.uniform(1, 100), rnd.uniform(1, 70)
        C_ = 180 - A_ - B_
        assert abs(math.sin(math.radians((A_ + B_) / 2)) - math.cos(math.radians(C_ / 2))) < 1e-12
    eq(sum(cos(dg(a))**2 for a in (15, 35, 55, 75)), 2)
    eq(sin(dg(40)) / cos(dg(50)) - tan(dg(40)) * tan(dg(50)), 0)
    h = Symbol("h")
    hs = sp.solve(sp.Eq(h / tan(dg(30)) - h / tan(dg(45)), 20), h)[0]; eq(hs, 10 * (sqrt(3) + 1))
    assert abs(float(hs) - 27.3) < 0.05
    hs = sp.solve(sp.Eq(h / tan(dg(30)) - h / tan(dg(60)), 30), h)[0]; eq(hs, 15 * sqrt(3))
    # 15°：C=(0,0), A=(0,1), B=(-√3,0), D=(-√3-2,0)
    A, B, D = sp.Matrix([0, 1]), sp.Matrix([-sqrt(3), 0]), sp.Matrix([-sqrt(3) - 2, 0])
    eq((A - B).norm(), 2); eq((B - D).norm(), 2); eq((A - D).norm(), sqrt(6) + sqrt(2))
    eq(1 / (2 + sqrt(3)), tan(pi / 12)); eq(tan(pi / 12), 2 - sqrt(3))
    eq(1 / (sqrt(6) + sqrt(2)), sin(pi / 12)); eq(sin(pi / 12), (sqrt(6) - sqrt(2)) / 4)
    eq((2 + sqrt(3)) / (sqrt(6) + sqrt(2)), (sqrt(6) + sqrt(2)) / 4); eq(cos(pi / 12), (sqrt(6) + sqrt(2)) / 4)
    eq(sqrt(8 + 2 * sqrt(12)), sqrt(6) + sqrt(2))
    # 練習：22.5°  C=(0,0), A=(0,1), B=(-1,0), D=(-1-√2,0)
    eq(1 / (1 + sqrt(2)), tan(pi / 8)); eq(tan(pi / 8), sqrt(2) - 1)
    eq((1 + sqrt(2)) / sqrt(1 + (1 + sqrt(2))**2), cos(pi / 8)); eq(cos(pi / 8), sqrt(2 + sqrt(2)) / 2)

    # ---- 節2
    def roots(fn, lo=0.0, hi=180.0, n=180000):
        """[lo,hi] 上の fn(θ°)=0 の解（符号変化と格子上の零点）。"""
        out, prev = [], None
        for k in range(n + 1):
            th = lo + (hi - lo) * k / n
            v = fn(th)
            if abs(v) < 1e-10:
                out.append(th)
            elif prev is not None and prev[1] * v < 0 and abs(prev[1]) >= 1e-10:
                out.append((prev[0] + th) / 2)
            prev = (th, v)
        res = []
        for r in out:
            if not res or r - res[-1] > 0.01:
                res.append(r)
        return res

    def same(a, b):
        return len(a) == len(b) and all(abs(x - y) < 0.01 for x, y in zip(a, b))

    S, Cs, Tn = (lambda d: math.sin(math.radians(d))), (lambda d: math.cos(math.radians(d))), (lambda d: math.tan(math.radians(d)))
    eq(sin(dg(135)), sqrt(2) / 2); eq(cos(dg(120)), -R(1, 2)); eq(tan(dg(150)), -sqrt(3) / 3)
    eq(sin(dg(100))**2 + sin(dg(170))**2, 1); eq(tan(dg(25)) * tan(dg(115)), -1)
    eq(sin(dg(150)), R(1, 2)); eq(cos(dg(135)), -sqrt(2) / 2); eq(tan(dg(120)), -sqrt(3))
    eq(cos(dg(100))**2 + cos(dg(170))**2, 1); eq(tan(dg(40)) * tan(dg(130)), -1)
    assert same(roots(lambda d: 2 * S(d) - 3**0.5), [60, 120])
    assert same(roots(lambda d: 2**0.5 * Cs(d) + 1), [135])
    assert same(roots(lambda d: 3**0.5 * S(d) + Cs(d)), [150])          # √3 tanθ+1=0 ⇔ √3 sinθ+cosθ=0 (cosθ≠0)
    assert same(roots(lambda d: 2 * S(d) - 1), [30, 150])
    assert same(roots(lambda d: 2 * Cs(d) + 3**0.5), [150])
    assert same(roots(lambda d: S(d) + 3**0.5 * Cs(d)), [120])
    for th in (sp.asin(R(1, 3)), pi - sp.asin(R(1, 3))):
        sg = 1 if th == sp.asin(R(1, 3)) else -1
        eq(cos(th), sg * 2 * sqrt(2) / 3); eq(tan(th), sg * sqrt(2) / 4)
    th = pi - atan(2); eq(tan(th), -2); eq(cos(th), -sqrt(5) / 5); eq(sin(th), 2 * sqrt(5) / 5)
    for th in (sp.asin(R(3, 4)), pi - sp.asin(R(3, 4))):
        sg = 1 if th == sp.asin(R(3, 4)) else -1
        eq(cos(th), sg * sqrt(7) / 4); eq(tan(th), sg * 3 * sqrt(7) / 7)
    th = pi - atan(R(1, 3)); eq(cos(th), -3 * sqrt(10) / 10); eq(sin(th), sqrt(10) / 10)

    def ineq(pred, ans, exact_pts=()):
        for k in range(18001):
            d = 0.0013 + 179.9974 * k / 18000
            if abs(d - 90) < 1e-6:
                continue
            assert pred(d) == ans(d), d
        for d, val in exact_pts:   # 端点は厳密に
            assert bool(val) == ans(d), d
    ineq(lambda d: 2 * S(d) > 1, lambda d: 30 < d < 150, [(30, 2 * sin(dg(30)) > 1), (150, 2 * sin(dg(150)) > 1)])
    ineq(lambda d: Tn(d) >= -1, lambda d: d < 90 or 135 <= d, [(0, True), (135, sp.simplify(tan(dg(135)) + 1) >= 0), (180, True)])
    ineq(lambda d: 2 * S(d)**2 + Cs(d) - 1 > 0, lambda d: 0 < d < 120,
         [(0, sp.simplify(2 * sin(0)**2 + cos(0) - 1) > 0), (120, sp.simplify(2 * sin(dg(120))**2 + cos(dg(120)) - 1) > 0)])
    ineq(lambda d: 2**0.5 * Cs(d) <= 1, lambda d: 45 <= d, [(45, True)])
    ineq(lambda d: Tn(d) < 3**0.5, lambda d: d < 60 or d > 90, [(60, False)])
    ineq(lambda d: 2 * Cs(d)**2 - S(d) - 1 < 0, lambda d: 30 < d < 150,
         [(30, sp.simplify(2 * cos(dg(30))**2 - sin(dg(30)) - 1) < 0), (150, sp.simplify(2 * cos(dg(150))**2 - sin(dg(150)) - 1) < 0)])
    s_, c_ = (1 + sqrt(17)) / 6, (1 - sqrt(17)) / 6
    eq(s_ + c_, R(1, 3)); eq(s_**2 + c_**2, 1); assert s_ > 0
    eq(s_ * c_, -R(4, 9)); eq(s_**3 + c_**3, R(13, 27)); eq(s_ - c_, sqrt(17) / 3); eq(s_ / c_, -(9 + sqrt(17)) / 8)
    s_, c_ = (sqrt(7) + 1) / 4, (sqrt(7) - 1) / 4
    eq(s_ - c_, R(1, 2)); eq(s_**2 + c_**2, 1); assert s_ > 0 and c_ > 0
    eq(s_ * c_, R(3, 8)); eq(s_**3 - c_**3, R(11, 16)); eq(s_ + c_, sqrt(7) / 2)

    def extrema(fn):
        vals = [(fn(180 * k / 36000), 180 * k / 36000) for k in range(36001)]
        return max(vals), min(vals)
    (mx, tx), (mn, tn_) = extrema(lambda d: S(d)**2 + Cs(d))
    assert abs(mx - 1.25) < 1e-9 and abs(tx - 60) < 0.01 and abs(mn + 1) < 1e-9 and abs(tn_ - 180) < 0.01
    eq(sin(dg(60))**2 + cos(dg(60)), R(5, 4))
    (mx, tx), (mn, tn_) = extrema(lambda d: S(d)**2 - 3**0.5 * Cs(d))
    assert abs(mx - 1.75) < 1e-9 and abs(tx - 150) < 0.01 and abs(mn + 3**0.5) < 1e-9 and abs(tn_) < 0.01
    eq(sin(dg(150))**2 - sqrt(3) * cos(dg(150)), R(7, 4))

    def ncount(poly_t, a):
        """sinθ=t の多項式方程式 poly_t(t)=a の、0°≦θ≦180° での異なる解の個数"""
        t = Symbol("t")
        ths = set()
        for r in sp.solve(sp.Eq(poly_t(t), a), t):
            if r.is_real and 0 <= r <= 1:
                th = float(sp.asin(r) * 180 / pi)
                ths.add(round(th, 9)); ths.add(round(180 - th, 9))
        return len(ths)
    for a in [R(k, 40) for k in range(20, 70)]:
        n = ncount(lambda t: 1 - t**2 + t, a)
        want = 0 if (a < 1 or a > R(5, 4)) else 3 if a == 1 else 4 if a < R(5, 4) else 2
        assert n == want, (a, n)
        n = ncount(lambda t: 2 * (1 - t**2) + 3 * t, a * 2)
        b = a * 2
        want = 0 if (b < 2 or b > R(25, 8)) else 2 if b < 3 else 3 if b == 3 else 4 if b < R(25, 8) else 2
        assert n == want, (b, n)
    assert ncount(lambda t: 2 * (1 - t**2) + 3 * t, R(25, 8)) == 2 and ncount(lambda t: 1 - t**2 + t, R(5, 4)) == 2

    # ---- 節3
    def side(b, c, A):            # 余弦定理：2辺と間の角（度）→ 対辺
        b, c = sp.sympify(b), sp.sympify(c)
        return sp.sqrt(sp.expand(b**2 + c**2 - 2 * b * c * cos(dg(A))))

    def cosang(a, b, c):          # 対辺 a の角の cos
        a, b, c = sp.sympify(a), sp.sympify(b), sp.sympify(c)
        return sp.radsimp((b**2 + c**2 - a**2) / (2 * b * c))
    R2 = 6 / sin(dg(45)); eq(R2 / 2, 3 * sqrt(2)); eq(R2 * sin(dg(60)), 3 * sqrt(6)); eq(R2 * sin(dg(75)), 3 + 3 * sqrt(3))
    R2 = 4 / sin(dg(30)); eq(R2 / 2, 4); eq(R2 * sin(dg(135)), 4 * sqrt(2))
    eq(side(3, 5, 120), 7); eq(side(4, 3 * sqrt(2), 45), sqrt(10))
    eq(cosang(7, 5, 8), R(1, 2)); eq(cosang(sqrt(5), 1, sqrt(2)), -sqrt(2) / 2)
    eq(cosang(7, 3, 5), -R(1, 2)); eq(cosang(3, 5, 7), R(13, 14))
    a_, b_, c_ = sp.symbols("a b c")
    so = sp.solve([b_ + c_ - 4, c_ + a_ - 5, a_ + b_ - 6], [a_, b_, c_])
    assert (so[a_], so[b_], so[c_]) == (R(7, 2), R(5, 2), R(3, 2))
    eq(cosang(so[a_], so[b_], so[c_]), -R(1, 2))

    # ---- 節4
    a = side(2, sqrt(3) + 1, 60); eq(a, sqrt(6))
    eq(cosang(2, sqrt(3) + 1, a), sqrt(2) / 2)          # cos B（B の対辺 b=2）
    c = side(sqrt(6) - sqrt(2), 2, 135); eq(c, 2 * sqrt(2))
    eq(cosang(2, sqrt(6) - sqrt(2), c), cos(dg(30)))   # B=30°
    eq(cosang(sqrt(6) - sqrt(2), 2, c), cos(dg(15)))   # A=15°
    cc = Symbol("c", positive=True)
    sols = sp.solve(sp.Eq(2**2, 6 + cc**2 - 2 * sqrt(6) * cc * cos(dg(45))), cc)
    assert len(sols) == 2
    for cv in sols:
        cb = cosang(sqrt(6), cv, 2)
        if sp.simplify(cv - (sqrt(3) + 1)) == 0:
            eq(cb, R(1, 2)); eq(cosang(cv, 2, sqrt(6)), cos(dg(75)))
        else:
            eq(cv, sqrt(3) - 1); eq(cb, -R(1, 2)); eq(cosang(cv, 2, sqrt(6)), cos(dg(15)))
    sols = sp.solve(sp.Eq(1, 3 + cc**2 - 2 * sqrt(3) * cc * cos(dg(30))), cc)
    assert sorted(sols) == [1, 2]
    eq(cosang(sqrt(3), 2, 1), cos(dg(60))); eq(cosang(2, 1, sqrt(3)), 0)
    eq(cosang(sqrt(3), 1, 1), cos(dg(120))); eq(cosang(1, 1, sqrt(3)), cos(dg(30)))
    a_, b_, c_ = sp.symbols("a b c", positive=True)
    lhs = a_**2 * (b_**2 + c_**2 - a_**2) - b_**2 * (c_**2 + a_**2 - b_**2)
    assert sp.expand(lhs - (a_**2 - b_**2) * (c_**2 - a_**2 - b_**2)) == 0
    assert sp.expand(lhs - (a_**2 * c_**2 - b_**2 * c_**2 - a_**4 + b_**4)) == 0
    # sinA = 2 sinB cosC ⇔ a = 2b(a^2+b^2-c^2)/(2ab) ⇔ b^2 = c^2
    assert sp.simplify(a_ - 2 * b_ * (a_**2 + b_**2 - c_**2) / (2 * a_ * b_) - (c_**2 - b_**2) / a_) == 0

    def obtuse(p, q, r):
        m = max(p, q, r)
        return 2 * m < p + q + r and m * m > (p * p + q * q + r * r - m * m)

    def acute(p, q, r):
        m = max(p, q, r)
        return 2 * m < p + q + r and m * m < (p * p + q * q + r * r - m * m)
    for k in range(1, 8000):
        x = k / 1000 + 0.00037
        assert obtuse(3, 4, x) == (1 < x < 7**0.5 or 5 < x < 7), x
        assert acute(2, 3, x) == (5**0.5 < x < 13**0.5), x
    eq(sp.Integer(3)**2 + 4**2, 5**2)                       # x=5 は直角
    for _ in range(200):
        Bd = rnd.uniform(1, 59)
        sa, sb, sc = (math.sin(math.radians(v)) for v in (2 * Bd, Bd, 180 - 3 * Bd))
        assert abs(sa * sa - sb * (sb + sc)) < 1e-12
    a = sqrt(4 * (4 + 5)); eq(a, 6); eq(cosang(4, 5, 6), R(3, 4))
    assert abs(math.acos(float(cosang(6, 4, 5))) - 2 * math.acos(0.75)) < 1e-12
    a = sqrt(9 * (9 + 7)); eq(a, 12); eq(cosang(9, 7, 12), R(2, 3))
    assert abs(math.acos(float(cosang(12, 9, 7))) - 2 * math.acos(2 / 3)) < 1e-12

    # ---- 節5
    area = lambda p, q, A: sp.Rational(1, 2) * p * q * sin(dg(A))
    eq(area(4, 5, 120), 5 * sqrt(3)); eq(2 * area(4, 6, 135), 12 * sqrt(2))
    eq(area(6, 2 * sqrt(3), 150), 3 * sqrt(3)); eq(2 * area(5, 4, 60), 10 * sqrt(3)); eq(2 * area(5, 4, 120), 10 * sqrt(3))

    def tri(a, b, c):  # (cos C, S, r, R)  C は辺 c の対角
        a, b, c = map(sp.sympify, (a, b, c))
        cC = (a**2 + b**2 - c**2) / (2 * a * b)
        sC = sqrt(1 - cC**2)
        S_ = a * b * sC / 2
        hs = (a + b + c) / 2
        eq(S_, sqrt(hs * (hs - a) * (hs - b) * (hs - c)))      # ヘロン
        return cC, S_, 2 * S_ / (a + b + c), c / (2 * sC)
    cC, S_, r_, R_ = tri(5, 6, 7)
    eq(cC, R(1, 5)); eq(S_, 6 * sqrt(6)); eq(r_, 2 * sqrt(6) / 3); eq(R_, 35 * sqrt(6) / 24); eq(5 * 6 * 7 / (4 * R_), S_)
    cB = cosang(6, 5, 7); eq(cB, R(19, 35)); eq(sqrt(49 + R(25, 4) - 2 * 7 * R(5, 2) * cB), sqrt(145) / 2)
    eq(sqrt(R(36 + 49, 2) - R(25, 4)), sqrt(145) / 2)                         # 中線定理と一致
    cA, S_, r_, R_ = tri(5, 6, 4)
    eq(cA, R(3, 4)); eq(S_, 15 * sqrt(7) / 4); eq(r_, sqrt(7) / 2); eq(R_, 8 * sqrt(7) / 7)
    xx = Symbol("x")
    for (p, q, A, ad, bd) in ((3, 6, 120, 2, sqrt(7)), (3, 6, 60, 2 * sqrt(3), sqrt(3))):
        adv = sp.solve(sp.Eq(area(p, xx, R(A, 2)) + area(q, xx, R(A, 2)), area(p, q, A)), xx)[0]
        eq(adv, ad)
        bc = side(p, q, A)
        eq(bc * p / (p + q), bd)
        # 座標でも確認：A=(0,0), B=(p,0), C=q(cosA, sinA)
        Bp, Cp = sp.Matrix([p, 0]), q * sp.Matrix([cos(dg(A)), sin(dg(A))])
        Dp = (q * Bp + p * Cp) / (p + q)
        eq(Dp.norm(), ad); eq((Dp - Bp).norm(), bd)
        eq(sp.atan2(Dp[1], Dp[0]), dg(R(A, 2)))
    eq(R(1, 3) + R(1, 6), R(1, 2))
    bb = Symbol("b")
    for (A, a, S0, bv, cv, rv) in ((60, 7, 10 * sqrt(3), 8, 5, sqrt(3)), (120, 7, 15 * sqrt(3) / 4, 5, 3, sqrt(3) / 2)):
        eq(area(bv, cv, A), S0); eq(side(bv, cv, A), a); eq(2 * S0 / (a + bv + cv), rv)
        # 解の一意性：bc と b^2+c^2 から b>c の解はこれだけ
        prod = sp.solve(sp.Eq(area(1, bb, A), S0), bb)[0]
        sols = [v for v in sp.solve(sp.Eq(bb**2 + (prod / bb)**2 - 2 * prod * cos(dg(A)), a**2), bb) if v.is_real and v > 0]
        assert sorted(sols) == sorted([bv, cv])

    # ---- 節6
    x1, x2, y1, y2, th_ = sp.symbols("x1 x2 y1 y2 theta", positive=True)
    tot = (x1 * y1 + y1 * x2 + x2 * y2 + y2 * x1) * sin(th_) / 2
    assert sp.expand(tot - (x1 + x2) * (y1 + y2) * sin(th_) / 2) == 0
    for _ in range(100):   # ランダムな凸四角形で靴ひも公式と比較
        a1, a2, b1, b2, t0 = rnd.uniform(.1, 3), rnd.uniform(.1, 3), rnd.uniform(.1, 3), rnd.uniform(.1, 3), rnd.uniform(.1, 3.0)
        P4 = [(a1, 0), (b1 * math.cos(t0), b1 * math.sin(t0)), (-a2, 0), (-b2 * math.cos(t0), -b2 * math.sin(t0))]
        sh = abs(sum(P4[i][0] * P4[(i + 1) % 4][1] - P4[(i + 1) % 4][0] * P4[i][1] for i in range(4))) / 2
        assert abs(sh - (a1 + a2) * (b1 + b2) * math.sin(t0) / 2) < 1e-9
    eq(R(1, 2) * 6 * 8, 24); eq(R(1, 2) * 5 * 7 * sin(dg(30)), R(35, 4))
    assert abs(max(p * (10 - p) / 2 for p in [k / 1000 for k in range(1, 10000)]) - 12.5) < 1e-9

    def cyc(a, b, c, d):
        """円に内接する四角形：cos B, AC, 面積, 外接円の半径, cos A, BD"""
        a, b, c, d = map(sp.sympify, (a, b, c, d))
        cB = (a**2 + b**2 - c**2 - d**2) / (2 * (a * b + c * d))
        AC = sqrt(a**2 + b**2 - 2 * a * b * cB)
        eq(AC**2, c**2 + d**2 + 2 * c * d * cB)
        sB = sqrt(1 - cB**2)
        S_ = (a * b + c * d) * sB / 2
        cA = (a**2 + d**2 - b**2 - c**2) / (2 * (a * d + b * c))
        BD = sqrt(a**2 + d**2 - 2 * a * d * cA)
        eq(AC * BD, a * c + b * d)                           # トレミー
        hs = (a + b + c + d) / 2
        eq(S_, sqrt((hs - a) * (hs - b) * (hs - c) * (hs - d)))
        return cB, AC, S_, AC / (2 * sB), cA, BD
    cB, AC, S_, R_, _, _ = cyc(2, 3, 5, 3)
    eq(cB, -R(1, 2)); eq(AC, sqrt(19)); eq(S_, 21 * sqrt(3) / 4); eq(R_, sqrt(57) / 3)
    cB, AC, S_, R_, _, _ = cyc(1, 3, 4, 3)
    eq(cB, -R(1, 2)); eq(AC, sqrt(13)); eq(S_, 15 * sqrt(3) / 4); eq(R_, sqrt(39) / 3)

    def cyc_xy(sides, Rr):   # 円周上に実際に配置して対角線の交点の比を測る
        ang = _cyc(sides, Rr)
        th, pts = 0.0, []
        for k in range(4):
            pts.append((Rr * math.cos(math.radians(th)), Rr * math.sin(math.radians(th)))); th -= ang[k]
        for k in range(4):
            assert abs(math.dist(pts[k], pts[(k + 1) % 4]) - sides[k]) < 1e-9
        (x1_, y1_), (x2_, y2_), (x3_, y3_), (x4_, y4_) = pts
        den = (x1_ - x3_) * (y2_ - y4_) - (y1_ - y3_) * (x2_ - x4_)
        t = ((x1_ - x2_) * (y2_ - y4_) - (y1_ - y2_) * (x2_ - x4_)) / den
        u = -((x1_ - x3_) * (y1_ - y2_) - (y1_ - y3_) * (x1_ - x2_)) / den
        return t / (1 - t), u / (1 - u), math.dist(pts[0], pts[2]), math.dist(pts[1], pts[3])
    cB, AC, S_, R_, cA, BD = cyc(5, 3, 3, 8)
    eq(cB, -R(1, 2)); eq(AC, 7); eq(cA, R(71, 98)); eq(BD, R(39, 7))
    ap, bp, ac_, bd_ = cyc_xy([5, 3, 3, 8], float(R_))
    assert abs(ap - 40 / 9) < 1e-9 and abs(bp - 5 / 8) < 1e-9 and abs(ac_ - 7) < 1e-9 and abs(bd_ - 39 / 7) < 1e-9
    cB, AC, S_, R_, cA, BD = cyc(3, 5, 5, 8)
    eq(AC, 7); eq(BD, R(55, 7))
    ap, bp, _, _ = cyc_xy([3, 5, 5, 8], float(R_))
    assert abs(ap - 24 / 25) < 1e-9 and abs(bp - 3 / 8) < 1e-9
    _ = cyc_xy([2, 3, 5, 3], math.sqrt(57) / 3); _ = cyc_xy([1, 3, 4, 3], math.sqrt(39) / 3)
    # ブラーマグプタ：恒等式
    a_, b_, c_, d_ = sp.symbols("a b c d", positive=True)
    hs = (a_ + b_ + c_ + d_) / 2
    lhs = 4 * (a_ * b_ + c_ * d_)**2 - (a_**2 + b_**2 - c_**2 - d_**2)**2
    assert sp.expand(lhs - 16 * (hs - a_) * (hs - b_) * (hs - c_) * (hs - d_)) == 0
    assert sp.expand(lhs - ((a_ + b_)**2 - (c_ - d_)**2) * ((c_ + d_)**2 - (a_ - b_)**2)) == 0
    bt, dt = sp.symbols("beta delta")
    assert sp.simplify((cos(bt) + cos(dt))**2 + (sin(bt) - sin(dt))**2 - (2 + 2 * (cos(bt) * cos(dt) - sin(bt) * sin(dt)))) == 0

    def qmax(a, b, c, d, n=200000):   # 凸四角形（B,D が AC の反対側）で面積を数値的に最大化
        best = (0, None)
        for k in range(1, n):
            be = math.pi * k / n
            ac2 = a * a + b * b - 2 * a * b * math.cos(be)
            cd_ = (c * c + d * d - ac2) / (2 * c * d)
            if abs(cd_) >= 1:
                continue
            S0 = (a * b * math.sin(be) + c * d * math.sin(math.acos(cd_))) / 2
            best = max(best, (S0, be))
        return best
    S0, be = qmax(2, 3, 4, 5)
    assert abs(S0 - 2 * 30**0.5) < 1e-8 and abs(math.cos(be) + 7 / 13) < 1e-4
    eq(cyc(2, 3, 4, 5)[2], 2 * sqrt(30)); eq(cyc(2, 3, 4, 5)[0], -R(7, 13))
    assert sp.simplify(sp.expand((6 * cos(bt) - 20 * cos(dt))**2 + (6 * sin(bt) + 20 * sin(dt))**2) - (436 - 240 * (cos(bt) * cos(dt) - sin(bt) * sin(dt)))) == 0
    S0, be = qmax(1, 2, 3, 4)
    assert abs(S0 - 2 * 6**0.5) < 1e-8 and abs(math.cos(be) + 5 / 7) < 1e-4
    eq(cyc(1, 2, 3, 4)[2], 2 * sqrt(6)); eq(cyc(1, 2, 3, 4)[0], -R(5, 7))

    # ---- 節7
    M3 = lambda *v: sp.Matrix(v)
    eq(60 * sin(dg(45)) / sin(dg(60)) * tan(dg(30)), 20 * sqrt(2))
    eq(100 * sin(dg(60)) / sin(dg(45)) * tan(dg(45)), 50 * sqrt(6))

    def tri_area(p, q, r):
        return (q - p).cross(r - p).norm() / 2

    def plane_dist(o, p, q, r):
        n = (q - p).cross(r - p)
        return sp.Abs(n.dot(o - p)) / n.norm()

    def tet_vol(p, q, r, s):
        return sp.Abs(sp.Matrix.hstack(q - p, r - p, s - p).det()) / 6
    for (ab, ad, ae, ang_at, cosv, Sv, hv) in ((1, 2, 2, "B", R(1, 5), sqrt(6), sqrt(6) / 3), (1, 1, 2, "E", R(4, 5), R(3, 2), R(2, 3))):
        A0, B0, D0, E0 = M3(0, 0, 0), M3(ab, 0, 0), M3(0, ad, 0), M3(0, 0, ae)
        X = {"B": B0, "E": E0}[ang_at]
        Y, Z = [v for v in (B0, D0, E0) if v != X]
        eq((Y - X).dot(Z - X) / ((Y - X).norm() * (Z - X).norm()), cosv)
        eq(tri_area(B0, D0, E0), Sv); eq(plane_dist(A0, B0, D0, E0), hv)
        eq(tet_vol(A0, B0, D0, E0), R(ab * ad * ae, 6))
    for a6, hv, Vv, rv, Rv in ((6, 2 * sqrt(6), 18 * sqrt(2), sqrt(6) / 2, 3 * sqrt(6) / 2), (4, 4 * sqrt(6) / 3, 16 * sqrt(2) / 3, sqrt(6) / 3, sqrt(6))):
        B0, C0, D0 = M3(0, 0, 0), M3(a6, 0, 0), M3(R(a6, 2), a6 * sqrt(3) / 2, 0)
        H0 = (B0 + C0 + D0) / 3
        A0 = H0 + M3(0, 0, hv)
        for p_, q_ in ((A0, B0), (A0, C0), (A0, D0), (B0, C0), (B0, D0), (C0, D0)):
            eq((p_ - q_).norm(), a6)
        Vt = tet_vol(A0, B0, C0, D0); eq(Vt, Vv)
        eq(3 * Vt / (4 * tri_area(B0, C0, D0)), rv)
        O0 = H0 + M3(0, 0, hv - Rv)
        eq((O0 - A0).norm(), Rv); eq((O0 - B0).norm(), Rv)
        eq(plane_dist(H0 + M3(0, 0, rv), A0, B0, C0), rv); eq(plane_dist(H0 + M3(0, 0, rv), B0, C0, D0), rv)
    eq(R(360) * 2 / 6, 120); eq(sqrt(36 + 9 - 2 * 6 * 3 * cos(dg(120))), 3 * sqrt(7))
    eq(R(360) * 1 / 4, 90); eq(sqrt(16 + 9 - 2 * 4 * 3 * cos(dg(90))), 5)
    # 円錐の最短経路：展開図の中心角が 180°未満なので線分で最短。円錐上の曲線を数値的に最適化して確認
    def cone_path(rb, l, om):
        phi = 360 * rb / l                         # 展開図の中心角（度）
        assert phi < 180                           # 線分がおうぎ形の内部を通る
        return math.sqrt(l * l + om * om - 2 * l * om * math.cos(math.radians(phi)))
    assert abs(cone_path(2, 6, 3) - 3 * 7**0.5) < 1e-12 and abs(cone_path(1, 4, 3) - 5) < 1e-12
    for (half, hgt, edge, area_s, rv, cth) in ((3, 4, None, 15, R(3, 2), -R(9, 25)), (1, None, sqrt(3), sqrt(2), sqrt(2) - 1, -R(1, 2))):
        if hgt is None:
            hgt = sqrt(edge**2 - 2 * half**2); eq(hgt, 1)
        Ap, Bp, Cp, Dp, Op = M3(-half, -half, 0), M3(half, -half, 0), M3(half, half, 0), M3(-half, half, 0), M3(0, 0, hgt)
        eq(tri_area(Op, Ap, Bp), area_s)
        Vp = R(1, 3) * (2 * half)**2 * hgt
        eq(3 * Vp / ((2 * half)**2 + 4 * tri_area(Op, Ap, Bp)), rv)
        I0 = M3(0, 0, rv)
        for fc in ((Op, Ap, Bp), (Op, Bp, Cp), (Op, Cp, Dp), (Op, Dp, Ap), (Ap, Bp, Cp)):
            eq(plane_dist(I0, *fc), rv)
        u = (Op - Bp) / (Op - Bp).norm()
        E0 = Bp + u * (Ap - Bp).dot(u)
        eq((Cp - Bp).dot(u), (Ap - Bp).dot(u))           # C から OB への垂線の足も E
        eq((Ap - E0).dot(Cp - E0) / ((Ap - E0).norm() * (Cp - E0).norm()), cth)
        if half == 3:
            eq((Ap - Bp).dot(u) / (Op - Bp).norm(), R(9, 17))   # 図の E の位置
            eq((Ap - E0).norm(), 30 / sqrt(34))
    a_, b_, c_ = sp.symbols("a b c", positive=True)
    AB2, AC2, BC2 = a_**2 + b_**2, a_**2 + c_**2, b_**2 + c_**2
    sin2 = 1 - (a_**2)**2 / (AB2 * AC2)
    assert sp.simplify(AB2 * AC2 * sin2 / 4 - (a_**2 * b_**2 + b_**2 * c_**2 + c_**2 * a_**2) / 4) == 0
    S2 = (a_**2 * b_**2 + b_**2 * c_**2 + c_**2 * a_**2) / 4
    hh = a_ * b_ * c_ / (2 * sp.sqrt(S2))
    assert sp.simplify(1 / hh**2 - (1 / a_**2 + 1 / b_**2 + 1 / c_**2)) == 0
    O0, A0, B0, C0 = M3(0, 0, 0), M3(2, 0, 0), M3(0, 3, 0), M3(0, 0, 6)
    eq(tri_area(A0, B0, C0), 3 * sqrt(14)); eq(plane_dist(O0, A0, B0, C0), 3 * sqrt(14) / 7)
    for (e1, e2, e3, Vv, Rv) in ((5, 6, 7, 2 * sqrt(95), sqrt(55) / 2), (4, 5, 6, 15 * sqrt(6) / 4, sqrt(154) / 4)):
        P2, Q2, R2_ = sp.symbols("P2 Q2 R2")
        so = sp.solve([P2 + Q2 - e1**2, Q2 + R2_ - e2**2, R2_ + P2 - e3**2], [P2, Q2, R2_])
        p_, q_, r_ = sqrt(so[P2]), sqrt(so[Q2]), sqrt(so[R2_])
        assert so[P2] > 0 and so[Q2] > 0 and so[R2_] > 0
        A0, B0, C0, D0 = M3(0, 0, 0), M3(p_, q_, 0), M3(0, q_, r_), M3(p_, 0, r_)
        for (x_, y_, L_) in ((A0, B0, e1), (C0, D0, e1), (A0, C0, e2), (B0, D0, e2), (A0, D0, e3), (B0, C0, e3)):
            eq((x_ - y_).norm(), L_)
        eq(tet_vol(A0, B0, C0, D0), Vv); eq(p_ * q_ * r_ / 3, Vv)
        eq(sqrt(R((e1**2 + e2**2 - e3**2) * (e2**2 + e3**2 - e1**2) * (e3**2 + e1**2 - e2**2), 72)), Vv)
        cen = M3(p_ / 2, q_ / 2, r_ / 2)
        for v in (A0, B0, C0, D0):
            eq((v - cen).norm(), Rv)
    eq(sqrt(19 * 6 * 30), 6 * sqrt(95))

    # ---- 節8
    bs = [6 * k / 60000 for k in range(1, 60000)]
    av = [(math.sqrt(b * b + (6 - b)**2 - b * (6 - b)), b) for b in bs]
    mn = min(av); assert abs(mn[0] - 3) < 1e-9 and abs(mn[1] - 3) < 1e-3
    eq(area(3, 3, 60), 9 * sqrt(3) / 4)
    bs = [4 * k / 40000 for k in range(1, 40000)]
    mn = min((math.sqrt(b * b + (4 - b)**2 + b * (4 - b)), b) for b in bs)
    assert abs(mn[0] - 2 * 3**0.5) < 1e-9 and abs(mn[1] - 2) < 1e-3
    eq(side(2, 2, 120), 2 * sqrt(3)); eq(area(2, 2, 120), sqrt(3))
    tt = Symbol("t")
    A0, B0, C0, D0 = M3(0, 0, 0), M3(6, 0, 0), M3(3, 3 * sqrt(3), 0), M3(3, sqrt(3), 2 * sqrt(6))
    for p_, q_ in ((A0, B0), (A0, C0), (A0, D0), (B0, C0), (B0, D0), (C0, D0)):
        eq((p_ - q_).norm(), 6)
    Pt = A0 + (B0 - A0) * tt / 6
    assert sp.expand((Pt - C0).dot(Pt - C0) - (tt**2 - 6 * tt + 36)) == 0
    assert sp.expand((Pt - D0).dot(Pt - D0) - (tt**2 - 6 * tt + 36)) == 0
    Sf = sp.lambdify(tt, tri_area(Pt, C0, D0)); cf = sp.lambdify(tt, (C0 - Pt).dot(D0 - Pt) / ((C0 - Pt).norm() * (D0 - Pt).norm()))
    vals = [(float(Sf(6 * k / 6000)), float(cf(6 * k / 6000)), 6 * k / 6000) for k in range(6001)]
    assert abs(min(v[0] for v in vals) - 9 * 2**0.5) < 1e-9 and abs(min(v[1] for v in vals) - 1 / 3) < 1e-9
    P3 = Pt.subs(tt, 3)
    eq(tri_area(P3, C0, D0), 9 * sqrt(2)); eq((C0 - P3).dot(D0 - P3) / ((C0 - P3).norm() * (D0 - P3).norm()), R(1, 3))
    uu = Symbol("u")
    Qt = C0 + (D0 - C0) * uu / 6
    dist2 = sp.lambdify((tt, uu), (Pt - Qt).dot(Pt - Qt))
    best = min((dist2(6 * i / 300, 6 * j / 300), i, j) for i in range(301) for j in range(301))
    assert abs(best[0] - 18) < 1e-9 and best[1] == 150 and best[2] == 150
    eq((Pt - Qt).dot(Pt - Qt).subs({tt: 3, uu: 3}), 18)
    # 外接円の半径 1・A=60°/120°：B を動かして b+c の範囲と r の最大
    for Adeg, tmax, rmax in ((60, 2 * 3**0.5, 0.5), (120, 2.0, (2 * 3**0.5 - 3) / 2)):
        a0 = 2 * math.sin(math.radians(Adeg))
        ts, rs = [], []
        for k in range(1, 20000):
            Bd = (180 - Adeg) * k / 20000; Cd = 180 - Adeg - Bd
            b0, c0 = 2 * math.sin(math.radians(Bd)), 2 * math.sin(math.radians(Cd))
            S0 = b0 * c0 * math.sin(math.radians(Adeg)) / 2
            r0 = 2 * S0 / (a0 + b0 + c0)
            t0 = b0 + c0
            ts.append(t0); rs.append(r0)
            if Adeg == 60:
                assert abs(r0 - 3**0.5 * (t0 - 3**0.5) / 6) < 1e-12 and abs(b0 * c0 - (t0 * t0 - 3) / 3) < 1e-12
            else:
                assert abs(r0 - 3**0.5 / 2 * (t0 - 3**0.5)) < 1e-12 and abs(b0 * c0 - (t0 * t0 - 3)) < 1e-12
        assert abs(max(ts) - tmax) < 1e-8 and min(ts) > 3**0.5 - 1e-9 and min(ts) < 3**0.5 + 1e-3
        assert abs(max(rs) - rmax) < 1e-8
    eq(sqrt(3) * (2 * sqrt(3) - sqrt(3)) / 6, R(1, 2)); eq(sqrt(3) / 2 * (2 - sqrt(3)), (2 * sqrt(3) - 3) / 2)
    # フェルマー：数値最小化と、構成した P の厳密な確認
    def fsum(pts, x, y):
        return sum(math.hypot(x - px, y - py) for px, py in pts)

    def fmin(pts):
        best = min((fsum(pts, -2 + 6 * i / 300, -2 + 6 * j / 300), -2 + 6 * i / 300, -2 + 6 * j / 300) for i in range(301) for j in range(301))
        v, x, y = best; h_ = 0.02
        for _ in range(60):
            cand = min((fsum(pts, x + dx * h_, y + dy * h_), x + dx * h_, y + dy * h_) for dx in (-1, 0, 1) for dy in (-1, 0, 1))
            if cand[0] >= v - 1e-15:
                h_ /= 2
            v, x, y = min((v, x, y), cand)
        return v
    assert abs(fmin([(0, 1), (0, 0), (3**0.5, 0)]) - 7**0.5) < 1e-9
    Ap, Bp, Cp = M3(0, 1), M3(0, 0), M3(sqrt(3), 0)
    rot = sp.Matrix([[cos(-pi / 3), -sin(-pi / 3)], [sin(-pi / 3), cos(-pi / 3)]])
    C2 = rot * Cp; eq(C2[0], sqrt(3) / 2); eq(C2[1], -R(3, 2))
    eq((Ap - C2).norm(), sqrt(7))
    u_ = (C2 - Ap) / sqrt(7)
    Pp, P2 = Ap + u_ * 2 / sqrt(7), Ap + u_ * 3 / sqrt(7)
    eq((rot * Pp - P2).norm(), 0)                                   # P' は P の回転像
    eq(Pp.norm(), 1 / sqrt(7)); eq((Pp - P2).norm(), 1 / sqrt(7))
    eq((Pp - Ap).norm() + Pp.norm() + (Pp - Cp).norm(), sqrt(7)); eq((Pp - Cp).norm(), 4 / sqrt(7))
    eq(cosang(1, 2 / sqrt(7), 1 / sqrt(7)), -R(1, 2))               # ∠APB=120°
    eq(R(5, 2) / sqrt(7), (1 + 7 - 3) / (2 * sqrt(7)))
    assert abs(fmin([(2 * math.cos(math.radians(60)), 2 * math.sin(math.radians(60))), (0, 0), (3, 0)]) - 19**0.5) < 1e-9
    eq(side(2, 3, 120), sqrt(19))
    # 立方体の切り口：平面 x+y+z=t の切り口を直接計算
    cube_edges = [((0, 0, 0), (1, 0, 0)), ((0, 0, 0), (0, 1, 0)), ((0, 0, 0), (0, 0, 1)), ((1, 0, 0), (1, 1, 0)), ((1, 0, 0), (1, 0, 1)),
                  ((0, 1, 0), (1, 1, 0)), ((0, 1, 0), (0, 1, 1)), ((0, 0, 1), (1, 0, 1)), ((0, 0, 1), (0, 1, 1)), ((1, 1, 0), (1, 1, 1)),
                  ((1, 0, 1), (1, 1, 1)), ((0, 1, 1), (1, 1, 1))]

    def section(t):
        pts = []
        for p0, p1 in cube_edges:
            s0, s1 = sum(p0), sum(p1)
            if (s0 - t) * (s1 - t) < 0:
                lam = (t - s0) / (s1 - s0)
                pts.append(tuple(p0[i] + lam * (p1[i] - p0[i]) for i in range(3)))
        c = tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))
        e1 = _unit((0, 0), (1, -1)); e1 = (e1[0], e1[1], 0.0)
        e2 = (1 / 6**0.5, 1 / 6**0.5, -2 / 6**0.5)
        pts.sort(key=lambda p: math.atan2(_dot(_sub(p, c), e2), _dot(_sub(p, c), e1)))
        q2 = [(_dot(_sub(p, c), e1), _dot(_sub(p, c), e2)) for p in pts]
        ar = abs(sum(q2[i][0] * q2[(i + 1) % len(q2)][1] - q2[(i + 1) % len(q2)][0] * q2[i][1] for i in range(len(q2)))) / 2
        per = sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))
        return len(pts), ar, per

    def Sform(t):
        if t <= 1:
            return 3**0.5 / 2 * t * t
        if t < 2:
            return 3**0.5 / 2 * (t * t - 3 * (t - 1)**2)
        return 3**0.5 / 2 * (3 - t)**2
    best = (0, 0)
    for k in range(1, 3000):
        t = 3 * k / 3000 + 1e-7
        n_, ar, per = section(t)
        assert abs(ar - Sform(t)) < 1e-9, t
        assert (n_ == 6) == (1 < t < 2), t
        if 1 <= t <= 2:
            assert abs(per - 3 * 2**0.5) < 1e-9
        else:
            assert per < 3 * 2**0.5 - 1e-9
        best = max(best, (ar, t))
    assert abs(best[0] - 3 * 3**0.5 / 4) < 1e-6 and abs(best[1] - 1.5) < 2e-3
    assert abs(section(1.5)[1] - 3 * 3**0.5 / 4) < 1e-12
    eq(R(3, 2) / sqrt(3), sqrt(3) / 2); eq(1 / sqrt(3), sqrt(3) / 3)
    # 四面体 AB=CD=x：座標で体積を確かめる
    xs = Symbol("x", positive=True)
    hN = sqrt(1 - xs**2 / 2)
    A0, B0, C0, D0 = M3(-xs / 2, 0, 0), M3(xs / 2, 0, 0), M3(0, -xs / 2, hN), M3(0, xs / 2, hN)
    for p_, q_, L_ in ((A0, C0, 1), (A0, D0, 1), (B0, C0, 1), (B0, D0, 1), (A0, B0, xs), (C0, D0, xs)):
        assert sp.simplify((p_ - q_).dot(p_ - q_) - L_**2) == 0
    Vx = sp.Matrix.hstack(B0 - A0, C0 - A0, D0 - A0).det() / 6
    assert sp.simplify(Vx + xs**2 / 6 * hN) == 0          # 行列式 = -x^2 h，体積はその絶対値 x^2 h/6
    assert sp.expand(R(32, 27) - uu**2 * (2 - uu) - (uu - R(4, 3))**2 * (uu + R(2, 3))) == 0
    Vf = lambda x: x * x / 6 * math.sqrt(max(0.0, 1 - x * x / 2))
    best = max((Vf(2**0.5 * k / 100000), 2**0.5 * k / 100000) for k in range(1, 100000))
    assert abs(best[0] - 2 * 3**0.5 / 27) < 1e-9 and abs(best[1] - 2 / 3**0.5) < 1e-4
    eq((xs**2 / 6 * hN).subs(xs, 2 / sqrt(3)), 2 * sqrt(3) / 27); eq(sqrt(R(4, 243)), 2 * sqrt(3) / 27)
    # 練習：OA=OB=OC=1，等しい角 θ（グラム行列式と比較）
    cth = Symbol("c")
    G = sp.Matrix([[1, cth, cth], [cth, 1, cth], [cth, cth, 1]])
    assert sp.expand(G.det() - (1 - cth)**2 * (1 + 2 * cth)) == 0
    assert sp.expand(1 - G.det() - cth**2 * (3 - 2 * cth)) == 0
    s2 = 2 - 2 * cth; hO2 = 1 - s2 / 3
    assert sp.simplify((R(1, 3) * sqrt(3) / 4 * s2)**2 * hO2 - ((1 - cth) * sqrt(1 + 2 * cth) / 6)**2) == 0
    best = max(((1 - c) * math.sqrt(1 + 2 * c) / 6, c) for c in [-0.5 + 1.5 * k / 30000 for k in range(1, 30000)])
    assert abs(best[0] - 1 / 6) < 1e-12 and abs(best[1]) < 1e-4

    # ---- 検討の数値
    eq(7 * R(40, 49), R(40, 7)); eq(R(39, 7) * R(5, 13), R(15, 7))          # 28：AP, BP
    eq(2 * area(5, 5, sp.acos(R(7, 25)) * 180 / pi) / (5 + 5 + 6), R(3, 2))  # 34：断面 5,5,6 の内接円の半径
    eq(side(5, 5, sp.acos(R(7, 25)) * 180 / pi), 6)
    Pp2 = Ap + (C2 - Ap) * R(2, 7)
    eq(cosang(sqrt(3), (Pp2 - Bp).norm(), (Pp2 - Cp).norm()), -R(1, 2))       # 40：∠BPC=120°
    eq(cosang(2, (Pp2 - Cp).norm(), (Pp2 - Ap).norm()), -R(1, 2))             # 40：∠CPA=120°
    hexp = [M3(1, R(1, 2), 0), M3(1, 0, R(1, 2)), M3(R(1, 2), 0, 1), M3(0, R(1, 2), 1), M3(0, 1, R(1, 2)), M3(R(1, 2), 1, 0)]
    for i in range(6):
        eq((hexp[i] - hexp[(i + 1) % 6]).norm(), sqrt(2) / 2); eq(sum(hexp[i]), R(3, 2))  # 41：正六角形の1辺
    al, be_, kk = sp.symbols("alpha beta k")
    so = sp.solve([2 * al + be_ - 2, al**2 + 2 * al * be_], [al, be_], dict=True)
    assert any(d[al] == R(4, 3) and d[be_] == -R(2, 3) for d in so)            # 42：重解の位置
    assert sp.expand((uu - R(4, 3))**2 * (uu + R(2, 3)) - (uu**3 - 2 * uu**2 + R(32, 27))) == 0

    # ---- 配分
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert 37 <= len(items) <= 43, len(items)
    assert 4 <= len(SEC) <= 9
    assert cnt[5] >= 5 and cnt[1] >= 6 and cnt[2] >= 8 and cnt[3] >= 8 and cnt[4] >= 6, cnt
    for sct in SEC:   # 節の中は易しい順
        lv = [it["lv"] for it in sct["items"]]
        assert lv == sorted(lv), sct["title"]
        for it in sct["items"]:
            for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
                assert it.get(k), (it.get("title"), k)
            for k in ("q", "hint", "sol", "note", "ex", "exa"):
                txt = str(it.get(k, ""))
                assert "$$" not in txt and "\\text" not in txt, (it["title"], k)
                assert txt.count("$") % 2 == 0, (it["title"], k)
    return cnt
