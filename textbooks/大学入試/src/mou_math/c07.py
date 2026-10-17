r"""第7章 図形の性質（数学A）。担当 M07。
図はすべてこのファイル内で座標を計算して SVG にしている（問題の条件を満たす図）。
数式中の大文字の連続（点の名前）は最後に _fix で \mathrm{} に直す。斜体のままにしたい大文字は !S のように書く。"""
import math, re, random
from fractions import Fraction as Fr

# ================================================================ 幾何の補助（図と検算で共用）
def add(p, q): return (p[0] + q[0], p[1] + q[1])
def sub(p, q): return (p[0] - q[0], p[1] - q[1])
def mul(p, k): return (p[0] * k, p[1] * k)
def dot(p, q): return p[0] * q[0] + p[1] * q[1]
def crs(p, q): return p[0] * q[1] - p[1] * q[0]
def dist(p, q): return math.hypot(p[0] - q[0], p[1] - q[1])
def lerp(p, q, t): return (p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t)
def inter(a, b, c, d):
    """直線 AB と直線 CD の交点"""
    r, s = sub(b, a), sub(d, c)
    return add(a, mul(r, crs(sub(c, a), s) / crs(r, s)))
def foot(p, a, b):
    d = sub(b, a)
    return add(a, mul(d, dot(sub(p, a), d) / dot(d, d)))
def refl(p, a, b):
    f = foot(p, a, b)
    return (2 * f[0] - p[0], 2 * f[1] - p[1])
def rot(p, o, deg):
    t = math.radians(deg); v = sub(p, o)
    return (o[0] + v[0] * math.cos(t) - v[1] * math.sin(t), o[1] + v[0] * math.sin(t) + v[1] * math.cos(t))
def onc(o, r, deg):
    return (o[0] + r * math.cos(math.radians(deg)), o[1] + r * math.sin(math.radians(deg)))
def tri(a, b, c):
    """BC=a, CA=b, AB=c の三角形の頂点 A, B, C（B が原点、C が x 軸上、A が上側）"""
    B = (0.0, 0.0); C = (float(a), 0.0)
    x = (c * c - b * b + a * a) / (2 * a)
    return (x, math.sqrt(c * c - x * x)), B, C
def circum(A, B, C):
    ax, ay = A; bx, by = B; cx, cy = C
    d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax*ax + ay*ay) * (by - cy) + (bx*bx + by*by) * (cy - ay) + (cx*cx + cy*cy) * (ay - by)) / d
    uy = ((ax*ax + ay*ay) * (cx - bx) + (bx*bx + by*by) * (ax - cx) + (cx*cx + cy*cy) * (bx - ax)) / d
    return (ux, uy)
def incen(A, B, C):
    a, b, c = dist(B, C), dist(C, A), dist(A, B); s = a + b + c
    return ((a * A[0] + b * B[0] + c * C[0]) / s, (a * A[1] + b * B[1] + c * C[1]) / s)
def excen(A, B, C):
    """∠A 内の傍心"""
    a, b, c = dist(B, C), dist(C, A), dist(A, B); s = -a + b + c
    return ((-a * A[0] + b * B[0] + c * C[0]) / s, (-a * A[1] + b * B[1] + c * C[1]) / s)
def cent(A, B, C): return ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
def orth(A, B, C): return inter(A, foot(A, B, C), B, foot(B, C, A))
def ang(a, o, b):
    u, v = sub(a, o), sub(b, o)
    return math.degrees(math.acos(max(-1.0, min(1.0, dot(u, v) / math.hypot(*u) / math.hypot(*v)))))
def area(a, b, c): return abs(crs(sub(b, a), sub(c, a))) / 2
def line_circ(p, q, o, r):
    """直線 PQ と円（中心 o、半径 r）の交点 2つ（P からの向き t の小さい順）"""
    d = sub(q, p); f = sub(p, o)
    A_, B_, C_ = dot(d, d), 2 * dot(f, d), dot(f, f) - r * r
    D_ = math.sqrt(B_ * B_ - 4 * A_ * C_)
    return [add(p, mul(d, (-B_ - D_) / (2 * A_))), add(p, mul(d, (-B_ + D_) / (2 * A_)))]
def close(x, y, e=1e-9): return abs(x - y) < e


# ================================================================ SVG の図
class Fig:
    """世界座標（y 上向き）の点から、幅 w・高さ h 以内に収まる SVG をつくる"""
    def __init__(s, pts, w=200, h=150, pad=15):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        s.x0, s.x1, s.y0, s.y1 = min(xs), max(xs), min(ys), max(ys)
        s.k = min((w - 2 * pad) / ((s.x1 - s.x0) or 1), (h - 2 * pad) / ((s.y1 - s.y0) or 1))
        s.w = round((s.x1 - s.x0) * s.k + 2 * pad); s.h = round((s.y1 - s.y0) * s.k + 2 * pad)
        s.pad = pad; s.el = []
    def T(s, p): return (s.pad + (p[0] - s.x0) * s.k, s.pad + (s.y1 - p[1]) * s.k)
    def seg(s, p, q, dash=False, wd=1.1, col="#222"):
        (x1, y1), (x2, y2) = s.T(p), s.T(q)
        s.el.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{wd}"'
                    + (' stroke-dasharray="3,2"' if dash else '') + '/>')
    def poly(s, ps, fill="none", wd=1.1, col="#222", dash=False):
        pt = " ".join(f"{x:.1f},{y:.1f}" for x, y in map(s.T, ps))
        s.el.append(f'<polygon points="{pt}" fill="{fill}" stroke="{col}" stroke-width="{wd}"'
                    + (' stroke-dasharray="3,2"' if dash else '') + '/>')
    def circ(s, o, r, fill="none", wd=1.0, col="#222", dash=False):
        x, y = s.T(o)
        s.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * s.k:.1f}" fill="{fill}" stroke="{col}" stroke-width="{wd}"'
                    + (' stroke-dasharray="3,2"' if dash else '') + '/>')
    def dot(s, p, r=1.7, col="#222"):
        x, y = s.T(p)
        s.el.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>')
    def lab(s, p, t, dx=0, dy=0, size=11, col="#222"):
        x, y = s.T(p)
        s.el.append(f'<text x="{x + dx:.1f}" y="{y + dy + size * 0.36:.1f}" font-size="{size}" font-family="serif" '
                    f'text-anchor="middle" fill="{col}">{t}</text>')
    def labs(s, d, c, r=8):
        """d: {名前: 点}。中心 c から外向きに r px 離して名前を置く"""
        cx, cy = s.T(c)
        for t, p in d.items():
            x, y = s.T(p); vx, vy = x - cx, y - cy; n = math.hypot(vx, vy) or 1
            s.lab(p, t, r * vx / n, r * vy / n)
    def ra(s, v, a, b, size=5):
        """頂点 v の直角の印（a, b は2辺の方向の点）"""
        X, Y = s.T(v); A_, B_ = s.T(a), s.T(b)
        ua = ((A_[0] - X), (A_[1] - Y)); na = math.hypot(*ua); ua = (ua[0] / na * size, ua[1] / na * size)
        ub = ((B_[0] - X), (B_[1] - Y)); nb = math.hypot(*ub); ub = (ub[0] / nb * size, ub[1] / nb * size)
        s.el.append(f'<polyline points="{X + ua[0]:.1f},{Y + ua[1]:.1f} {X + ua[0] + ub[0]:.1f},{Y + ua[1] + ub[1]:.1f} '
                    f'{X + ub[0]:.1f},{Y + ub[1]:.1f}" fill="none" stroke="#222" stroke-width="0.8"/>')
    def arc(s, o, r, t1, t2, wd=1.0, col="#222", dash=False):
        """中心 o・半径 r の円の、角 t1 から t2 まで（反時計回り）の弧"""
        (x1, y1), (x2, y2) = s.T(onc(o, r, t1)), s.T(onc(o, r, t2)); big = 1 if (t2 - t1) % 360 > 180 else 0
        s.el.append(f'<path d="M{x1:.1f},{y1:.1f} A{r * s.k:.1f},{r * s.k:.1f} 0 {big} 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{col}" stroke-width="{wd}"'
                    + (' stroke-dasharray="3,2"' if dash else '') + '/>')
    def txt(s, x, y, t, size=10):
        """SVG 座標で直接文字を置く"""
        s.el.append(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-family="serif" text-anchor="middle" fill="#222">{t}</text>')
    def svg(s):
        return (f'<svg class="fig" width="{s.w}" height="{s.h}" viewBox="0 0 {s.w} {s.h}">' + "".join(s.el) + '</svg>')

def hcat(figs, gap=8, tags=None):
    """いくつかの Fig を横に並べて1つの SVG にする（tags は左上に置く (1) などの文字）"""
    W = sum(f.w for f in figs) + gap * (len(figs) - 1); H = max(f.h for f in figs); x = 0; out = []
    for i, f in enumerate(figs):
        out.append(f'<g transform="translate({x},{(H - f.h) / 2:.1f})">' + "".join(f.el) + '</g>')
        if tags: out.append(f'<text x="{x + 9}" y="11" font-size="10" font-family="serif" text-anchor="middle" fill="#222">{tags[i]}</text>')
        x += f.w + gap
    return f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(out) + '</svg>'

SH = "#dfe8f7"   # 塗りの色

SEC = []

# ================================================================ 節1 図
def _f11():
    A, B, C = tri(5, 4, 6); D = lerp(B, C, 3 / 5); E = (15.0, 0.0); I = incen(A, B, C)
    F = Fig([A, B, C, E], w=250, h=100)
    F.seg(C, E, dash=True); F.poly([A, B, C]); F.seg(A, D); F.seg(A, E); F.dot(I)
    F.lab(A, "A", 0, -8); F.lab(B, "B", -6, 7); F.lab(C, "C", 2, 8); F.lab(D, "D", -1, 8); F.lab(E, "E", 0, 8); F.lab(I, "I", -7, 0, 10)
    return F.svg()
def _f12():
    A, B, C, Pp = (1.3, 3.3), (0.0, 0.0), (4.2, 0.0), (1.9, 1.15); Q = inter(B, Pp, A, C)
    F = Fig([A, B, C], w=150, h=120)
    F.poly([A, B, C]); F.seg(B, Q); F.seg(Pp, C); F.dot(Pp)
    F.labs({"A": A, "B": B, "C": C, "Q": Q}, cent(A, B, C)); F.lab(Pp, "P", -2, 9)
    return F.svg()
def _f14():
    A, B, C = tri(5, 4, 6); D = lerp(B, C, 3 / 5)
    F = Fig([A, B, C], w=150, h=110)
    F.poly([A, B, C]); F.seg(A, D)
    F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(D, "D", 0, 8)
    F.lab(lerp(A, B, .5), "c", -7, -2, 11); F.lab(lerp(A, C, .5), "b", 7, -2, 11)
    F.lab(lerp(B, D, .5), "m", 0, 8, 10); F.lab(lerp(D, C, .5), "n", 0, 8, 10)
    return F.svg()
def _f15():
    A, B, C = tri(6, 5, 4); D = lerp(A, C, 4 / 10); E = lerp(A, B, 5 / 11)
    F = Fig([A, B, C], w=160, h=120)
    F.poly([A, B, C]); F.seg(B, D); F.seg(C, E)
    F.labs({"A": A, "B": B, "C": C, "D": D, "E": E}, cent(A, B, C))
    return F.svg()

# ---------------------------------------------------------------- 節1
SEC.append({"title": "三角形の辺と角・角の二等分線",
"base": r"""・三角形の成立条件：3辺 $a,\ b,\ c$ について $|b-c|<a<b+c$。辺の大小と向かい合う角の大小は一致する（$a>b\iff A>B$）<br>
・角の二等分線と比：$\angle A$ の二等分線と辺 $BC$ の交点 $D$ について $BD:DC=AB:AC$。外角の二等分線と直線 $BC$ の交点 $E$ について $BE:EC=AB:AC$（$AB\neq AC$ のとき）<br>
・中線定理：辺 $BC$ の中点 $M$ について $AB^2+AC^2=2(AM^2+BM^2)$""",
"items": [
 {"lv": 1, "title": "内角・外角の二等分線と線分の比",
  "q": r"$\triangle ABC$ において $AB=6,\ BC=5,\ CA=4$ とする。$\angle A$ の二等分線と辺 $BC$ の交点を $D$，$\angle A$ の外角の二等分線と直線 $BC$ の交点を $E$ とし，$\triangle ABC$ の内心を $I$ とする。<br>(1) 線分 $BD,\ BE,\ DE$ の長さを求めよ。<br>(2) $AI:ID$ を求めよ。" + _f11(),
  "hint": r"内角の二等分線は対辺を $AB:AC$ に<b>内分</b>し，外角の二等分線は $AB:AC$ に<b>外分</b>する。内心 $I$ は $\angle B$ の二等分線上にもあるので，$\triangle ABD$ において $BI$ が $\angle ABD$ を二等分することを使う。",
  "sol": r"(1) $BD:DC=AB:AC=6:4=3:2$ より　$BD=\dfrac35BC=\boldsymbol{3}$<br>"
         r"$E$ は辺 $BC$ を $3:2$ に外分する点で，$AB>AC$ より辺 $BC$ の $C$ の側の延長上にある。$EC=\dfrac23BE$ を $BE-EC=BC=5$ に代入して $\dfrac13BE=5$，よって $BE=\boldsymbol{15}$<br>"
         r"$DE=BE-BD=\boldsymbol{12}$<br>"
         r"(2) $BI$ は $\angle ABD$ の二等分線であるから，$\triangle ABD$ において　$AI:ID=BA:BD=6:3=\boldsymbol{2:1}$",
  "note": r"$\angle DAE=\dfrac12\cdot180^\circ=90^\circ$ だから，$A$ は $DE$ を直径とする円周上にある。この円は $PB:PC=3:2$ を満たす点 $P$ 全体（アポロニウスの円）である。また (2) は一般に $AI:ID=(b+c):a$ となる。",
  "ex": r"$\triangle ABC$ において $AB=7,\ BC=6,\ CA=3$ とする。$\angle A$ の二等分線，$\angle A$ の外角の二等分線と直線 $BC$ の交点をそれぞれ $D,\ E$，内心を $I$ とするとき，$BD,\ BE,\ DE$ の長さと $AI:ID$ を求めよ。",
  "exa": r"$BD=\dfrac{21}5,\ BE=\dfrac{21}2,\ DE=\dfrac{63}{10}$，$AI:ID=5:3$"},
 {"lv": 2, "title": "三角形の辺の大小関係（内部の点と不等式）",
  "q": r"$\triangle ABC$ の内部の点 $P$ に対して，$PB+PC<AB+AC$ が成り立つことを証明せよ。",
  "hint": r"「2辺の和は他の1辺より大きい」を，うまく選んだ三角形に使う。直線 $BP$ と辺 $AC$ の交点 $Q$ をとり，$\triangle ABQ$ と $\triangle PQC$ に着目する。",
  "sol": _f12() + r"直線 $BP$ と辺 $AC$ の交点を $Q$ とする。$P$ は三角形の内部にあるから，$Q$ は辺 $AC$ 上（端点を除く）にあり，$P$ は線分 $BQ$ 上にある。<br>"
         r"$\triangle ABQ$ において　$AB+AQ>BQ=BP+PQ$　…①<br>"
         r"$\triangle PQC$ において　$PQ+QC>PC$　…②<br>"
         r"①，② の辺々を加えると　$AB+AQ+PQ+QC>BP+PQ+PC$<br>"
         r"$AQ+QC=AC$ であるから　$\boldsymbol{PB+PC<AB+AC}$　（終）",
  "note": r"同じ図で三角形の外角の性質を2回使うと，$\angle BPC=\angle PQC+\angle PCQ>\angle PQC=\angle BAQ+\angle ABQ>\angle BAC$ も示せる。辺の和の評価でも角の大小でも，補助点 $Q$ が鍵になる。",
  "ex": r"$\triangle ABC$ の内部の点 $P$ に対して，次の不等式を証明せよ。<br>$\dfrac12(AB+BC+CA)<PA+PB+PC<AB+BC+CA$",
  "exa": r"左：$PA+PB>AB$ など3式を加えて2で割る。右：例題の不等式と，同様に示せる $PC+PA<BC+BA$，$PA+PB<CA+CB$ を加えて2で割る。"},
 {"lv": 2, "title": "中線定理",
  "q": r"$\triangle ABC$ の辺 $BC$ の中点を $M$ とする。<br>(1) $AB^2+AC^2=2(AM^2+BM^2)$ が成り立つことを証明せよ。<br>(2) $AB=7,\ BC=8,\ CA=5$ のとき，中線 $AM$ の長さを求めよ。",
  "hint": r"$\angle AMB+\angle AMC=180^\circ$ だから $\cos\angle AMC=-\cos\angle AMB$。$\triangle ABM,\ \triangle ACM$ で余弦定理を立てて加えると，$\cos$ を含む項が消える。",
  "sol": r"(1) $\angle AMB=\theta$ とおくと $\angle AMC=180^\circ-\theta$ で，$\cos(180^\circ-\theta)=-\cos\theta$。$CM=BM$ に注意して余弦定理を用いると<br>"
         r"$AB^2=AM^2+BM^2-2AM\cdot BM\cos\theta$<br>"
         r"$AC^2=AM^2+BM^2+2AM\cdot BM\cos\theta$<br>"
         r"辺々を加えて　$AB^2+AC^2=2(AM^2+BM^2)$　（終）<br>"
         r"(2) $BM=4$ であるから $7^2+5^2=2(AM^2+4^2)$，$AM^2=21$。よって　$AM=\boldsymbol{\sqrt{21}}$",
  "note": r"$A$ から $BC$ に垂線を下ろし三平方の定理を使っても証明できる（垂線の足の位置で場合分けが要る）。平行四辺形 $ABCD$ では対角線が互いに他を二等分するので，$\triangle ABD$ に中線定理を使うと $AC^2+BD^2=2(AB^2+AD^2)$ が得られる。",
  "ex": r"平行四辺形 $ABCD$ において $AB=5,\ AD=7,\ AC=10$ のとき，対角線 $BD$ の長さを求めよ。",
  "exa": r"$BD=4\sqrt3$"},
 {"lv": 3, "title": "角の二等分線の長さ（スチュワートの定理）",
  "q": r"$\triangle ABC$ の $\angle A$ の二等分線と辺 $BC$ の交点を $D$ とし，$AB=c,\ AC=b,\ BD=m,\ DC=n$ とする。<br>(1) $AD^2=bc-mn$ を証明せよ。<br>(2) $AB=6,\ BC=5,\ CA=4$ のとき，$AD$ の長さを求めよ。" + _f14(),
  "hint": r"$\angle ADB$ と $\angle ADC$ は補角なので，$\triangle ABD,\ \triangle ADC$ で余弦定理を立てて $\cos$ を消去する（中線定理と同じ発想）。最後に二等分線の性質 $c:b=m:n$ を使う。",
  "sol": r"(1) $AD=d,\ \angle ADB=\theta$ とおくと $\angle ADC=180^\circ-\theta$。余弦定理より<br>"
         r"$c^2=d^2+m^2-2dm\cos\theta$　…①，　$b^2=d^2+n^2+2dn\cos\theta$　…②<br>"
         r"①$\times n+$②$\times m$ より　$nc^2+mb^2=(m+n)d^2+mn(m+n)$　…③<br>"
         r"一方，$c:b=m:n$ より $cn=bm$ であるから　$nc^2+mb^2=c\cdot cn+b\cdot bm=c\cdot bm+b\cdot cn=bc(m+n)$<br>"
         r"これを ③ に代入して $m+n$ で割ると $bc=d^2+mn$，すなわち　$AD^2=bc-mn$　（終）<br>"
         r"(2) $BD:DC=6:4$ より $m=3,\ n=2$。$AD^2=6\cdot4-3\cdot2=18$ より　$AD=\boldsymbol{3\sqrt2}$",
  "note": r"③ は辺 $BC$ 上の任意の点 $D$ で成り立つ（スチュワートの定理）。別証：直線 $AD$ と外接円の交点を $E$ とすると $\triangle ABD\backsim\triangle AEC$ より $AB\cdot AC=AD\cdot AE=AD^2+AD\cdot DE$ で，方べきの定理より $AD\cdot DE=BD\cdot DC$。",
  "ex": r"$AB=8,\ BC=7,\ CA=6$ の $\triangle ABC$ において，$\angle A$ の二等分線と辺 $BC$ の交点を $D$ とするとき，$AD$ の長さを求めよ。",
  "exa": r"$AD=6$"},
 {"lv": 5, "title": "2本の二等分線が等しい三角形（シュタイナー・レームスの定理）",
  "q": r"$\triangle ABC$ において，$\angle B$ の二等分線と辺 $CA$ の交点を $D$，$\angle C$ の二等分線と辺 $AB$ の交点を $E$ とする。$BD=CE$ ならば $AB=AC$ であることを証明せよ。" + _f15(),
  "hint": r"「$AB=AC$ ならば $BD=CE$」は易しいが，逆を図形的に示すのは難しい。前の例題の公式で $BD^2,\ CE^2$ を3辺 $a,\ b,\ c$ で表し，$BD^2-CE^2$ が $(c-b)\times$（正の式）と因数分解できることを示す。",
  "sol": r"$BC=a,\ CA=b,\ AB=c$ とする。$BD$ は $\angle B$ の二等分線なので $AD:DC=c:a$，$AD=\dfrac{bc}{a+c},\ DC=\dfrac{ab}{a+c}$。前の例題の公式より<br>"
         r"$BD^2=ac-\dfrac{ab^2c}{(a+c)^2}=\dfrac{ac\{(a+c)^2-b^2\}}{(a+c)^2}=\dfrac{ac(a+b+c)(a-b+c)}{(a+c)^2}$<br>"
         r"同様に（$b$ と $c$ を入れかえて）　$CE^2=\dfrac{ab(a+b+c)(a+b-c)}{(a+b)^2}$<br>"
         r"よって　$BD^2-CE^2=\dfrac{a(a+b+c)}{(a+b)^2(a+c)^2}!F$，　$!F=c(a-b+c)(a+b)^2-b(a+b-c)(a+c)^2$<br>"
         r"ここで $c(a-b+c)(a+b)^2=a^3c+a^2bc-ab^2c-b^3c+a^2c^2+2abc^2+b^2c^2$ で，$!F$ の後ろの項はこれの $b$ と $c$ を入れかえたものだから<br>"
         r"$!F=a^3(c-b)+3abc(c-b)+bc(c^2-b^2)+a^2(c^2-b^2)=(c-b)\{a^3+a^2(b+c)+3abc+bc(b+c)\}$<br>"
         r"$\{\ \}$ の中は正であり，$\dfrac{a(a+b+c)}{(a+b)^2(a+c)^2}>0$ である。<br>"
         r"$BD=CE$ のとき $BD^2-CE^2=0$ であるから $c-b=0$，すなわち $\boldsymbol{AB=AC}$　（終）",
  "note": r"背理法による初等幾何の証明も知られているが，長さを3辺で表して因数分解する方法が確実である。なお，内心 $I$ について $ID=IE$ からは $AB=AC$ は導けない。$\angle A=60^\circ$ のとき $\angle EID=\angle BIC=120^\circ$ より $A,\ E,\ I,\ D$ は同一円周上にあり，$AI$ が $\angle EAD$ を二等分するので，常に $ID=IE$ となる。",
  "ex": r"例題と同じ記号で，$AB>AC$ ならば $BD>CE$ であることを証明せよ。また，頂点 $B,\ C$ から引いた中線の長さの大小も調べよ。",
  "exa": r"例題の計算で $c>b$ より $BD^2-CE^2>0$。中線は中線定理より（$B$ からの中線）$^2-$（$C$ からの中線）$^2=\dfrac34(c^2-b^2)>0$ で，$B$ から引いた中線の方が長い。"},
]})

# ================================================================ 節2 図
def _f21():
    k = 4.0
    A, B, C = tri(k * math.sin(math.radians(70)), k * math.sin(math.radians(60)), k * math.sin(math.radians(50)))
    O = circum(A, B, C)
    F = Fig([A, B, C], w=140, h=110)
    F.poly([A, B, C]); F.seg(O, A); F.seg(O, B); F.seg(O, C); F.dot(O)
    F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(O, "O", 0, 9)
    return F.svg()
def _f22():
    A, B, C = tri(8, 5, 7); I = incen(A, B, C); J = excen(A, B, C); r = math.sqrt(3); rr = 5 * math.sqrt(3)
    u = mul(sub(B, A), 1 / 7); v = mul(sub(C, A), 1 / 5); Pp = add(A, mul(u, 10)); Q = add(A, mul(v, 10))
    D = (5.0, 0.0); E = (3.0, 0.0)
    F = Fig([A, Pp, Q, onc(J, rr, 150), onc(J, rr, 12)], w=190, h=130)
    F.poly([A, B, C]); F.seg(B, Pp); F.seg(C, Q); F.circ(I, r); F.arc(J, rr, 12, 150, dash=True)
    for p in (D, E, Pp, Q): F.dot(p, 1.4)
    F.lab(A, "A", 0, -8); F.lab(B, "B", -8, -3); F.lab(C, "C", 8, -3); F.lab(D, "D", 3, -7, 10); F.lab(E, "E", -2, -7, 10)
    F.lab(Pp, "P", -8, -3); F.lab(Q, "Q", 8, -2)
    return F.svg()
def _f23():
    A, B, C = (1.5, 3.4), (0.0, 0.0), (4.2, 0.0); O = circum(A, B, C); R = dist(O, A); H = orth(A, B, C)
    D = foot(A, B, C); E = foot(B, C, A); Fp = foot(C, A, B); Pp = line_circ(A, D, O, R)[1]
    F = Fig([(O[0] - R, O[1] - R), (O[0] + R, O[1] + R)], w=150, h=150)
    F.circ(O, R); F.poly([A, B, C]); F.seg(A, Pp); F.seg(B, E); F.seg(C, Fp); F.seg(B, Pp, dash=True); F.seg(C, Pp, dash=True)
    F.dot(H); F.ra(D, C, A, 4)
    F.labs({"A": A, "B": B, "C": C, "P": Pp, "E": E, "F": Fp}, O); F.lab(H, "H", 7, -2); F.lab(D, "D", 6, 7, 10)
    return F.svg()
def _f24():
    A, B, C = (0.6, 3.0), (0.0, 0.0), (4.4, 0.0); O = circum(A, B, C); R = dist(O, A); H = orth(A, B, C); G = cent(A, B, C)
    M = lerp(B, C, .5); D = sub(mul(O, 2), B)
    F = Fig([(O[0] - R, O[1] - R), (O[0] + R, O[1] + R)], w=150, h=150)
    F.circ(O, R); F.poly([A, B, C]); F.seg(B, D); F.seg(A, D, wd=.8); F.seg(D, C, wd=.8); F.seg(A, H); F.seg(C, H); F.seg(O, M)
    F.seg(A, M, wd=.7, dash=True); F.seg(lerp(O, H, -0.6), lerp(O, H, 1.5), col="#2a55b0", dash=True)
    for p in (O, G, H): F.dot(p)
    F.labs({"A": A, "B": B, "C": C, "D": D}, O); F.lab(M, "M", 0, 8); F.lab(O, "O", 4, -7); F.lab(G, "G", 1, 8); F.lab(H, "H", -7, 3)
    return F.svg()
def _c25():
    A, B, C = (1.6, 2.6), (0.0, 0.0), (5.0, 0.0); I = incen(A, B, C); W = inter(A, I, B, C)
    K = (0.9, 0.0); P2 = lerp(A, K, 0.6); Pp = refl(P2, A, W)
    return A, B, C, W, Pp, P2, K
def _f25():
    A, B, C, W, Pp, P2, K = _c25()
    X, Y, Z = foot(Pp, B, C), foot(Pp, C, A), foot(Pp, A, B)
    F = Fig([A, B, C], w=160, h=110)
    F.poly([A, B, C]); F.seg(Pp, A, wd=.8); F.seg(Pp, B, wd=.8); F.seg(Pp, C, wd=.8)
    for q, t, dx, dy in ((X, "x", 5, 0), (Y, "y", 4, -6), (Z, "z", 0, -7)):
        F.seg(Pp, q, dash=True); F.lab(lerp(Pp, q, .5), t, dx, dy, 10)
    F.dot(Pp); F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(Pp, "P", 7, 5)
    return F.svg()
def _f25b():
    A, B, C, W, Pp, P2, K = _c25()
    fb, fc = foot(B, A, K), foot(C, A, K)
    F = Fig([A, B, C, fb], w=160, h=115)
    F.poly([A, B, C]); F.seg(A, W, dash=True, col="#2a55b0"); F.seg(A, K); F.seg(lerp(A, K, 1), fb, wd=.7); F.seg(B, fb, dash=True); F.seg(C, fc, dash=True)
    F.ra(fb, B, A, 4); F.ra(fc, C, A, 4); F.dot(Pp); F.dot(P2)
    F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(K, "K", 6, 7); F.lab(Pp, "P", 7, 3); F.lab(P2, "P\u2032", -9, 1)
    F.lab(lerp(B, fb, .5), "d", -5, 4, 10); F.lab(lerp(B, fb, .5), "B", 0, 7, 7)
    F.lab(lerp(C, fc, .5), "d", 2, -7, 10); F.lab(lerp(C, fc, .5), "C", 7, -4, 7)
    return F.svg()

# ---------------------------------------------------------------- 節2
SEC.append({"title": "三角形の五心",
"base": r"""・外心 $O$：3辺の垂直二等分線の交点で，$OA=OB=OC$（外接円の中心）<br>
・内心 $I$：3つの内角の二等分線の交点（内接円の中心）。$\angle BIC=90^\circ+\dfrac12\angle A$。傍心：1つの内角と他の2つの外角の二等分線の交点<br>
・重心 $G$：3本の中線の交点。各中線を頂点の側から $2:1$ に内分する<br>
・垂心 $H$：3頂点から対辺（またはその延長）に下ろした垂線の交点<br>
・円外の点から引いた2本の接線の長さは等しい。内接円と辺 $BC$ の接点 $D$ について $BD=s-b$（$s=\dfrac{a+b+c}2$）""",
"items": [
 {"lv": 1, "title": "外心・内心・重心の基本性質",
  "q": _f21() + r"(1) $\triangle ABC$ の外心を $O$ とする。$\angle OBC=20^\circ,\ \angle OCA=30^\circ$ のとき，$\angle OAB$ と $\angle BAC$ を求めよ。<br>"
       r"(2) $\triangle ABC$ の内心を $I$ とする。$\angle BAC=70^\circ$ のとき，$\angle BIC$ を求めよ。<br>"
       r"(3) $\triangle ABC$ の重心を $G$，辺 $BC,\ CA$ の中点を $M,\ N$ とする。$\triangle ABC$ の面積を $!S$ とするとき，四角形 $GMCN$ の面積を $!S$ で表せ。",
  "hint": r"(1) $OA=OB=OC$ より $\triangle OAB,\ \triangle OBC,\ \triangle OCA$ はすべて二等辺三角形。(2) $\angle IBC+\angle ICB=\dfrac12(\angle B+\angle C)$。(3) $G$ は中線 $AM$ を $2:1$ に内分するので，高さの比から面積比がわかる。",
  "sol": r"(1) $OA=OB=OC$ より　$\angle OCB=\angle OBC=20^\circ$，$\angle OAC=\angle OCA=30^\circ$，$\angle OBA=\angle OAB$<br>"
         r"$\triangle ABC$ の内角の和より $2(\angle OAB+20^\circ+30^\circ)=180^\circ$。よって　$\angle OAB=\boldsymbol{40^\circ}$，$\angle BAC=40^\circ+30^\circ=\boldsymbol{70^\circ}$<br>"
         r"(2) $\angle IBC+\angle ICB=\dfrac12(\angle B+\angle C)=\dfrac12(180^\circ-70^\circ)=55^\circ$ より　$\angle BIC=180^\circ-55^\circ=\boldsymbol{125^\circ}$<br>"
         r"(3) $GM=\dfrac13AM$ より $\triangle GBC=\dfrac13\triangle ABC=\dfrac13!S$。$M$ は $BC$ の中点なので $\triangle GMC=\dfrac12\triangle GBC=\dfrac16!S$。"
         r"同様に $\triangle GCA=\dfrac13!S$，$\triangle GCN=\dfrac12\triangle GCA=\dfrac16!S$。よって　四角形 $GMCN=\boldsymbol{\dfrac13!S}$",
  "note": r"(1) は $O$ が三角形の内部にある図で計算した。得られた $\angle A=70^\circ,\ \angle B=60^\circ,\ \angle C=50^\circ$ は確かに鋭角三角形で，図と矛盾しない。(3) から，3本の中線は $\triangle ABC$ を面積の等しい6つの三角形に分けることがわかる。",
  "ex": r"(1) $\triangle ABC$ の外心を $O$ とする。$\angle OAB=25^\circ,\ \angle OBC=35^\circ$ のとき，$\angle OCA$ と $\angle ABC$ を求めよ。<br>"
        r"(2) $\triangle ABC$ の内心を $I$ とする。$\angle BIC=118^\circ$ のとき，$\angle BAC$ を求めよ。<br>"
        r"(3) $\triangle ABC$（面積 $!S$）の重心 $G$ を通り辺 $BC$ に平行な直線と辺 $AB,\ AC$ の交点を $P,\ Q$ とする。$\triangle APQ$ の面積を $!S$ で表せ。",
  "exa": r"(1) $\angle OCA=30^\circ,\ \angle ABC=60^\circ$　(2) $56^\circ$　(3) $\dfrac49!S$"},
 {"lv": 2, "title": "内接円・傍接円と接線の長さ",
  "q": r"$AB=7,\ BC=8,\ CA=5$ の $\triangle ABC$ の内接円が辺 $BC$ に接する点を $D$ とする。また，辺 $BC$ および辺 $AB,\ AC$ の延長に接する円（$\angle A$ 内の傍接円）が辺 $BC$ に接する点を $E$ とする。<br>"
       r"(1) $BD,\ BE$ を求めよ。<br>(2) 内接円の半径 $r$ と，$\angle A$ 内の傍接円の半径 $r'$ を求めよ。",
  "hint": r"円外の点から引いた2本の接線の長さは等しい。各頂点からの接線の長さを文字でおいて連立する。半径は面積を2通りに表して求める：内接円では $!S=\dfrac12r(a+b+c)$，傍接円では $!S=\dfrac12r'(b+c-a)$。",
  "sol": _f22() + r"(1) 内接円と辺 $CA,\ AB$ の接点を $F,\ G$ とし，$AF=AG=x,\ BG=BD=y,\ CD=CF=z$ とおくと<br>"
         r"$y+z=8,\ z+x=5,\ x+y=7$　これより $x+y+z=10$，$x=2,\ y=5,\ z=3$。よって　$BD=\boldsymbol{5}$<br>"
         r"傍接円と直線 $AB,\ AC$ の接点を $P,\ Q$ とすると，$AP=AQ,\ BP=BE,\ CQ=CE$ であるから<br>"
         r"$AP+AQ=(AB+BE)+(AC+CE)=AB+AC+BC=20$，$AP=10$。よって　$BE=BP=AP-AB=\boldsymbol{3}$<br>"
         r"(2) 余弦定理より $\cos C=\dfrac{8^2+5^2-7^2}{2\cdot8\cdot5}=\dfrac12$，$C=60^\circ$ だから　$\triangle ABC=\dfrac12\cdot8\cdot5\sin60^\circ=10\sqrt3$<br>"
         r"内心を $I$ とすると $\triangle ABC=\triangle IBC+\triangle ICA+\triangle IAB=\dfrac12r(8+5+7)=10r$ より　$r=\boldsymbol{\sqrt3}$<br>"
         r"傍接円の中心を $J$ とすると $\triangle ABC=\triangle JAB+\triangle JAC-\triangle JBC=\dfrac12r'(7+5-8)=2r'$ より　$r'=\boldsymbol{5\sqrt3}$",
  "note": r"一般に $BD=s-b,\ BE=s-c$（$s=\dfrac{a+b+c}2$）で，$CE=s-b=BD$ となる。つまり $D$ と $E$ は辺 $BC$ の中点に関して対称である。また $!S=rs=r'(s-a)$。",
  "ex": r"$AB=13,\ BC=14,\ CA=15$ の $\triangle ABC$ について，例題と同様に $D,\ E$ を定めるとき，$BD,\ BE$ と，内接円の半径 $r$，$\angle A$ 内の傍接円の半径 $r'$ を求めよ。",
  "exa": r"$BD=6,\ BE=8,\ r=4,\ r'=12$"},
 {"lv": 3, "title": "垂心の性質（垂心の対称点は外接円上）",
  "q": r"鋭角三角形 $ABC$ の垂心を $H$ とし，直線 $AH$ と辺 $BC$ の交点を $D$，直線 $AH$ と $\triangle ABC$ の外接円の $A$ 以外の交点を $P$ とする。<br>"
       r"(1) $\angle BHC=180^\circ-\angle A$ を証明せよ。<br>(2) $HD=DP$ を証明せよ。" + _f23(),
  "hint": r"$B,\ C$ から対辺に下ろした垂線の足 $E,\ F$ をとる。(2) は $\triangle BHD\equiv\triangle BPD$ を示す。円周角の定理で $\angle PBC=\angle PAC$ とし，2つの直角三角形の角 $90^\circ-\angle C$ に結びつける。",
  "sol": r"$B,\ C$ から辺 $CA,\ AB$ に下ろした垂線の足を $E,\ F$ とする（鋭角三角形なので $H$ は内部にある）。<br>"
         r"(1) 四角形 $AFHE$ の内角の和は $360^\circ$ で，$\angle AFH=\angle AEH=90^\circ$ だから $\angle FHE=180^\circ-\angle A$。対頂角は等しいので　$\angle BHC=\angle FHE=180^\circ-\angle A$　（終）<br>"
         r"(2) 弧 $PC$ に対する円周角より　$\angle PBC=\angle PAC=\angle DAC=90^\circ-\angle C$（直角三角形 $ADC$）<br>"
         r"直角三角形 $BEC$ において　$\angle HBC=\angle EBC=90^\circ-\angle C$<br>"
         r"よって $\angle HBD=\angle PBD$。$\triangle BHD$ と $\triangle BPD$ において，$BD$ は共通，$\angle BDH=\angle BDP=90^\circ$，$\angle HBD=\angle PBD$ であるから，1辺とその両端の角がそれぞれ等しく $\triangle BHD\equiv\triangle BPD$。<br>"
         r"したがって　$HD=PD$　（終）",
  "note": r"(2) は「垂心 $H$ の辺 $BC$ に関する対称点は外接円上にある」ということで，辺 $CA,\ AB$ についても同様である。(1) と合わせると，$\triangle HBC$ の外接円は $\triangle ABC$ の外接円を $BC$ で折り返した円であり，半径が等しい。",
  "ex": r"鋭角三角形 $ABC$ の垂心を $H$，辺 $BC$ の中点を $M$ とし，$M$ に関して $H$ と対称な点を $Q$ とする。$Q$ は $\triangle ABC$ の外接円上にあり，$AQ$ はその直径であることを証明せよ。",
  "exa": r"四角形 $BHCQ$ は平行四辺形なので $QB\parallel CH$，$CH\perp AB$ より $\angle ABQ=90^\circ$。同様に $\angle ACQ=90^\circ$。よって $B,\ C$ は $AQ$ を直径とする円周上にあり，その円が外接円である。"},
 {"lv": 4, "title": "オイラー線（外心・重心・垂心は一直線上）",
  "q": r"鋭角三角形 $ABC$（$AB\neq AC$）の外心を $O$，重心を $G$，垂心を $H$，辺 $BC$ の中点を $M$ とする。<br>"
       r"(1) $AH=2OM$ を証明せよ。<br>(2) 3点 $O,\ G,\ H$ は一直線上にあり，$GH=2OG$ であることを証明せよ。" + _f24(),
  "hint": r"(1) 外接円の直径 $BD$ をとると，四角形 $AHCD$ は平行四辺形になる。$OM$ は $\triangle BCD$ の2辺の中点を結ぶ線分。(2) $AH\parallel OM$ と $AG:GM=2:1$ から $\triangle AGH\backsim\triangle MGO$ を示す。",
  "sol": r"(1) 外接円の直径 $BD$ をとると，$\angle BAD=\angle BCD=90^\circ$。<br>"
         r"$DA\perp AB,\ CH\perp AB$ より $DA\parallel CH$。$DC\perp BC,\ AH\perp BC$ より $DC\parallel AH$。<br>"
         r"よって四角形 $AHCD$ は平行四辺形で $AH=DC$。$\triangle BCD$ で $O,\ M$ はそれぞれ $BD,\ BC$ の中点なので，中点連結定理より $DC=2OM$。ゆえに　$AH=2OM$　（終）<br>"
         r"(2) $AB\neq AC$ より $O$ は直線 $AM$ 上にない。平行四辺形 $AHCD$ において $A\to H$ と $D\to C$ は同じ向きで，中点連結定理より $O\to M$ も $D\to C$ と同じ向きに平行である。"
         r"よって線分 $AH$ と $MO$ は平行で向きが逆であり，$H$ と $O$ は直線 $AM$ に関して反対側にあって，$\angle HAG=\angle OMG$（錯角）。<br>"
         r"さらに $AG:MG=2:1=AH:MO$ であるから，2辺の比とその間の角が等しく　$\triangle AGH\backsim\triangle MGO$<br>"
         r"ゆえに $\angle AGH=\angle MGO$。$A,\ G,\ M$ は一直線上にあり $H,\ O$ はその反対側にあるから，この2角は対頂角の位置にあり，$H,\ G,\ O$ は一直線上にある。相似比より $GH:GO=2:1$，すなわち　$GH=2OG$　（終）",
  "note": r"直線 $OGH$ をオイラー線という（正三角形では3点が一致する）。$\angle BOM=\angle A$ より $OM=!R\cos A$ なので，(1) は $AH=2!R\cos A$（$!R$ は外接円の半径）とも書ける。ベクトルでは $\overrightarrow{OH}=\overrightarrow{OA}+\overrightarrow{OB}+\overrightarrow{OC}$ と表される（数学C）。",
  "ex": r"鋭角三角形 $ABC$ において $\angle A=60^\circ$ のとき，外心 $O$，垂心 $H$ について $AH=AO$ であることを証明せよ。",
  "exa": r"$\angle BOC=2\angle A=120^\circ$ で $OM$ は $\angle BOC$ を二等分するから $\angle BOM=60^\circ$，$OM=OB\cos60^\circ=\dfrac12OB$。(1) より $AH=2OM=OB=AO$。"},
 {"lv": 5, "title": "3頂点への距離と3辺への距離（エルデシュ・モーデルの不等式）",
  "q": r"$\triangle ABC$ の内部の点 $P$ から辺 $BC,\ CA,\ AB$ に下ろした垂線の長さをそれぞれ $x,\ y,\ z$ とする。<br>"
       r"$PA+PB+PC\geqq2(x+y+z)$<br>が成り立つことを証明せよ。また，等号が成り立つのはどのようなときか。" + _f25(),
  "hint": r"$BC=a,\ CA=b,\ AB=c$ とする。$P$ を $\angle A$ の二等分線に関して折り返した点 $P'$ をとると，$P'$ から $AB,\ AC$ への距離は $y,\ z$ に入れかわる。面積を考えて $a\cdot PA\geqq cy+bz$ を導き，3つを加えて $\dfrac bc+\dfrac cb\geqq2$ を使う。",
  "sol": _f25b() + r"$BC=a,\ CA=b,\ AB=c$ とする。<br>"
         r"【$a\cdot PA\geqq cy+bz$ の証明】$P$ を $\angle A$ の二等分線に関して対称移動した点を $P'$ とする。$AP'=AP$ で，$P'$ から直線 $AB,\ AC$ までの距離はそれぞれ $y,\ z$ である。"
         r"$P$ は $\angle BAC$ の内部にあるので $P'$ も $\angle BAC$ の内部にあり，直線 $AP'$ は辺 $BC$ と点 $K$ で交わる。$B,\ C$ から直線 $AP'$ までの距離を $d_B,\ d_C$ とすると，$d_B\leqq BK,\ d_C\leqq CK$ より $d_B+d_C\leqq a$。よって<br>"
         r"$\dfrac12cy+\dfrac12bz=\triangle ABP'+\triangle ACP'=\dfrac12AP'(d_B+d_C)\leqq\dfrac12a\cdot AP$<br>"
         r"ゆえに $a\cdot PA\geqq cy+bz$，すなわち $PA\geqq\dfrac cay+\dfrac baz$。<br>"
         r"【結論】同様に $PB\geqq\dfrac abz+\dfrac cbx$，$PC\geqq\dfrac bcx+\dfrac acy$。3式を加えると<br>"
         r"$PA+PB+PC\geqq\left(\dfrac bc+\dfrac cb\right)x+\left(\dfrac ca+\dfrac ac\right)y+\left(\dfrac ab+\dfrac ba\right)z$<br>"
         r"ここで $\dfrac bc+\dfrac cb-2=\dfrac{(b-c)^2}{bc}\geqq0$ などより，右辺 $\geqq2x+2y+2z$。よって　$\boldsymbol{PA+PB+PC\geqq2(x+y+z)}$<br>"
         r"【等号】等号が成り立つには $a=b=c$ であり，かつ各頂点で $d_B+d_C=a$，すなわち $AP'\perp BC$ などが成り立つことが必要である。正三角形では $\angle A$ の二等分線が $BC$ に垂直なので，$AP'\perp BC$ は $P'$ が，したがって $P$ がこの二等分線上にあることを意味する。"
         r"3頂点について合わせると $P$ は正三角形の中心である。逆に，正三角形の中心では $PA=PB=PC=2x=2y=2z$ となり等号が成り立つ。<br>"
         r"よって等号が成り立つのは，$\boldsymbol{\triangle ABC}$ <b>が正三角形で $\boldsymbol{P}$ がその中心のとき</b> に限る。",
  "note": r"折り返さずに直線 $AP$ のまま評価すると $a\cdot PA\geqq by+cz$ となり，加えたときの $x$ の係数が $\dfrac ab+\dfrac ac$ となってうまくいかない。「$\angle A$ の二等分線で折り返して $y,\ z$ を入れかえる」のが急所である。$P$ が内心 $I$ のときは $IA+IB+IC\geqq6r$ が得られる。",
  "ex": r"例題と同じ記号で，$PA\cdot PB\cdot PC\geqq8xyz$ を証明せよ。",
  "exa": r"例題の $a\cdot PA\geqq cy+bz\geqq2\sqrt{bc\,yz}$（$(\sqrt{cy}-\sqrt{bz})^2\geqq0$ による）と同様の2式を掛け合わせると $abc\cdot PA\cdot PB\cdot PC\geqq8abc\,xyz$。"},
]})


# ================================================================ 節3 図
_T3 = ((1.3, 3.2), (0.0, 0.0), (4.4, 0.0))
def _f31():
    A, B, C = _T3; R = lerp(A, B, 1 / 3); Pp = lerp(B, C, 3 / 7); O = inter(A, Pp, C, R); Q = inter(B, O, C, A)
    F = Fig([A, B, C], w=150, h=115)
    F.poly([A, B, C]); F.seg(A, Pp); F.seg(C, R); F.seg(B, Q); F.dot(O)
    F.labs({"A": A, "B": B, "C": C, "R": R, "P": Pp, "Q": Q}, cent(A, B, C)); F.lab(O, "O", 3, -8)
    return F.svg()
def _f32():
    A, B, C = _T3; E = lerp(A, C, 1 / 3); D = lerp(B, C, 3 / 4); Pp = inter(A, D, B, E)
    F = Fig([A, B, C], w=150, h=115)
    F.poly([Pp, A, B], fill=SH, wd=0); F.poly([A, B, C]); F.seg(A, D); F.seg(B, E)
    F.labs({"A": A, "B": B, "C": C, "D": D, "E": E}, cent(A, B, C)); F.lab(Pp, "P", 1, 9)
    return F.svg()
def _f33():
    A, B, C = (1.6, 3.3), (0.0, 0.0), (4.4, 0.0); I = incen(A, B, C); r = dist(I, foot(I, B, C))
    D, E, Fp = foot(I, B, C), foot(I, C, A), foot(I, A, B); G = inter(A, D, B, E)
    F = Fig([A, B, C], w=150, h=115)
    F.poly([A, B, C]); F.circ(I, r, col="#2a55b0"); F.seg(A, D); F.seg(B, E); F.seg(C, Fp); F.dot(G)
    F.labs({"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp}, cent(A, B, C))
    return F.svg()
def _f34():
    A, B, C = tri(5, 3, 6); D = (10.0, 0.0); E = lerp(C, A, 5 / 11); Fp = lerp(A, B, 3 / 8)
    F = Fig([A, B, C, D], w=250, h=100)
    F.poly([A, B, C]); F.seg(C, D, dash=True); F.seg(A, D, wd=.8); F.seg(B, E, wd=.8); F.seg(C, Fp, wd=.8)
    F.seg(Fp, D, col="#c0392b", wd=1.3)
    F.lab(A, "A", 0, -8); F.lab(B, "B", -7, 4); F.lab(C, "C", 0, 9); F.lab(D, "D", 0, 9); F.lab(E, "E", 4, -8); F.lab(Fp, "F", -8, -2)
    return F.svg()
def _f35():
    A, B, C = _T3; D, E, Fp = lerp(B, C, 1 / 3), lerp(C, A, 1 / 3), lerp(A, B, 1 / 3)
    Pp, Q, R = inter(A, D, B, E), inter(B, E, C, Fp), inter(C, Fp, A, D)
    F = Fig([A, B, C], w=180, h=135)
    F.poly([Pp, Q, R], fill=SH, wd=0); F.poly([A, B, C]); F.seg(A, D); F.seg(B, E); F.seg(C, Fp)
    F.labs({"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp}, cent(A, B, C))
    F.lab(Pp, "P", 0, 9, 10); F.lab(Q, "Q", 6, -6, 10); F.lab(R, "R", -7, -4, 10)
    return F.svg()
def _f36():
    A, B, C = _T3; al, be, ga = 1.0, 2.0, 1.5
    D = lerp(B, C, ga / (be + ga)); E = lerp(C, A, al / (al + ga)); Fp = lerp(A, B, be / (al + be)); O = inter(A, D, B, E)
    F = Fig([A, B, C], w=150, h=115)
    F.poly([D, E, Fp], fill=SH); F.poly([A, B, C]); F.seg(A, D, wd=.7); F.seg(B, E, wd=.7); F.seg(C, Fp, wd=.7); F.dot(O)
    F.labs({"A": A, "B": B, "C": C, "D": D, "E": E, "F": Fp}, cent(A, B, C))
    return F.svg()

# ---------------------------------------------------------------- 節3
SEC.append({"title": "チェバの定理・メネラウスの定理",
"base": r"""・チェバの定理：$\triangle ABC$ の辺 $BC,\ CA,\ AB$ 上の点 $P,\ Q,\ R$ について，$AP,\ BQ,\ CR$ が1点で交わるならば<br>　　$\dfrac{BP}{PC}\cdot\dfrac{CQ}{QA}\cdot\dfrac{AR}{RB}=1$<br>
・メネラウスの定理：直線 $\ell$ が $\triangle ABC$ の辺 $BC,\ CA,\ AB$ またはその延長と，それぞれ $P,\ Q,\ R$ で交わるならば<br>　　$\dfrac{BP}{PC}\cdot\dfrac{CQ}{QA}\cdot\dfrac{AR}{RB}=1$<br>
・どちらも逆が成り立つ（メネラウスの定理の逆では，3点のうち辺の延長上にあるものが1個または3個）<br>
・面積比：高さが共通なら底辺の比。$P,\ Q$ が辺 $AB,\ AC$ 上にあるとき $\triangle APQ=\dfrac{AP}{AB}\cdot\dfrac{AQ}{AC}\triangle ABC$""",
"items": [
 {"lv": 1, "title": "チェバの定理・メネラウスの定理の基本",
  "q": r"$\triangle ABC$ の辺 $AB$ を $1:2$ に内分する点を $R$，辺 $BC$ を $3:4$ に内分する点を $P$ とし，$AP$ と $CR$ の交点を $O$，直線 $BO$ と辺 $CA$ の交点を $Q$ とする。<br>(1) $CQ:QA$ を求めよ。　(2) $AO:OP$ を求めよ。" + _f31(),
  "hint": r"(1) 3本の線分が1点で交わるのでチェバの定理。(2) $\triangle ABP$ と直線 $RC$（$O$ を通る）にメネラウスの定理を使う。頂点 → 分点 → 頂点 → … と三角形を一周するように比を並べる。",
  "sol": r"(1) チェバの定理より　$\dfrac{BP}{PC}\cdot\dfrac{CQ}{QA}\cdot\dfrac{AR}{RB}=\dfrac34\cdot\dfrac{CQ}{QA}\cdot\dfrac12=1$　よって $\dfrac{CQ}{QA}=\dfrac83$，$CQ:QA=\boldsymbol{8:3}$<br>"
         r"(2) $\triangle ABP$ と直線 $RC$ にメネラウスの定理を用いると　$\dfrac{AR}{RB}\cdot\dfrac{BC}{CP}\cdot\dfrac{PO}{OA}=1$<br>"
         r"$\dfrac12\cdot\dfrac74\cdot\dfrac{PO}{OA}=1$ より $\dfrac{PO}{OA}=\dfrac87$。よって　$AO:OP=\boldsymbol{7:8}$",
  "note": r"(2) は $\dfrac{AO}{OP}=\dfrac{AR}{RB}+\dfrac{AQ}{QC}=\dfrac12+\dfrac38=\dfrac78$ でも検算できる（ファン・オーベルの定理）。メネラウスの定理を使うときは，どの三角形とどの直線を考えるかを最初に明示すること。",
  "ex": r"$\triangle ABC$ の辺 $AB$ を $2:3$ に内分する点を $R$，辺 $BC$ を $1:2$ に内分する点を $P$ とし，$AP$ と $CR$ の交点を $O$，直線 $BO$ と辺 $CA$ の交点を $Q$ とする。$CQ:QA$ と $AO:OP$ を求めよ。",
  "exa": r"$CQ:QA=3:1$，$AO:OP=1:1$"},
 {"lv": 2, "title": "線分の比と面積比",
  "q": r"$\triangle ABC$ の辺 $AC$ を $1:2$ に内分する点を $E$，辺 $BC$ を $3:1$ に内分する点を $D$ とし，$AD$ と $BE$ の交点を $P$ とする。<br>"
       r"(1) $AP:PD$，$BP:PE$ を求めよ。<br>(2) $\triangle ABC$ の面積を $!S$ とするとき，$\triangle PAB$ と四角形 $PDCE$ の面積を $!S$ で表せ。" + _f32(),
  "hint": r"(1) $AP:PD$ は $\triangle ADC$ と直線 $BE$，$BP:PE$ は $\triangle BCE$ と直線 $AD$ にメネラウスの定理。(2) 高さが共通な三角形の面積比は底辺の比。$\triangle ABC\to\triangle ABD\to\triangle PAB$ と順に比をかける。",
  "sol": r"(1) $\triangle ADC$ と直線 $BE$ にメネラウスの定理を用いて　$\dfrac{AP}{PD}\cdot\dfrac{DB}{BC}\cdot\dfrac{CE}{EA}=\dfrac{AP}{PD}\cdot\dfrac34\cdot\dfrac21=1$　よって $AP:PD=\boldsymbol{2:3}$<br>"
         r"$\triangle BCE$ と直線 $AD$ にメネラウスの定理を用いて　$\dfrac{BD}{DC}\cdot\dfrac{CA}{AE}\cdot\dfrac{EP}{PB}=\dfrac31\cdot\dfrac31\cdot\dfrac{EP}{PB}=1$　よって $BP:PE=\boldsymbol{9:1}$<br>"
         r"(2) $\triangle ABD=\dfrac34!S$ より　$\triangle PAB=\dfrac{AP}{AD}\triangle ABD=\dfrac25\cdot\dfrac34!S=\boldsymbol{\dfrac3{10}!S}$<br>"
         r"また $\triangle BCE=\dfrac23!S$，$\triangle PBD=\dfrac{PD}{AD}\triangle ABD=\dfrac35\cdot\dfrac34!S=\dfrac9{20}!S$ より<br>"
         r"四角形 $PDCE=\triangle BCE-\triangle PBD=\dfrac23!S-\dfrac9{20}!S=\boldsymbol{\dfrac{13}{60}!S}$",
  "note": r"メネラウスの定理を使う三角形は，<b>求めたい比の線分を1辺に含み，他の2辺上の分点の比がわかっている三角形</b>を選ぶ。(1) では $AP:PD$ に $\triangle ADC$，$BP:PE$ に $\triangle BCE$ を選んだ。",
  "ex": r"$\triangle ABC$ の辺 $AC$ を $2:1$ に内分する点を $E$，辺 $BC$ を $1:2$ に内分する点を $D$ とし，$AD$ と $BE$ の交点を $P$ とする。$AP:PD$，$BP:PE$ と，$\triangle PAB$ の面積は $\triangle ABC$ の面積の何倍かを求めよ。",
  "exa": r"$AP:PD=6:1$，$BP:PE=3:4$，$\dfrac27$ 倍"},
 {"lv": 3, "title": "チェバの定理の逆（3直線が1点で交わる）",
  "q": r"$\triangle ABC$ の内接円が辺 $BC,\ CA,\ AB$ に接する点をそれぞれ $D,\ E,\ F$ とする。3直線 $AD,\ BE,\ CF$ は1点で交わることを証明せよ。" + _f33(),
  "hint": r"接線の長さが等しいことから $\dfrac{BD}{DC}\cdot\dfrac{CE}{EA}\cdot\dfrac{AF}{FB}=1$ がわかる。あとはチェバの定理の逆。答案では「2直線の交点を通る第3の直線をひき，それが $F$ を通ることを示す」という流れを書く。",
  "sol": r"円外の点から引いた2本の接線の長さは等しいので　$AE=AF,\ BF=BD,\ CD=CE$<br>"
         r"よって　$\dfrac{BD}{DC}\cdot\dfrac{CE}{EA}\cdot\dfrac{AF}{FB}=\dfrac{BD\cdot CE\cdot AF}{DC\cdot EA\cdot FB}=\dfrac{BF\cdot CD\cdot AE}{CD\cdot AE\cdot BF}=1$　…①<br>"
         r"$D,\ E$ はそれぞれ辺 $BC,\ CA$ 上（端点を除く）にあるから，線分 $AD$ と $BE$ は三角形の内部の点 $O$ で交わる。直線 $CO$ と辺 $AB$ の交点を $F'$ とすると，チェバの定理より<br>"
         r"$\dfrac{BD}{DC}\cdot\dfrac{CE}{EA}\cdot\dfrac{AF'}{F'B}=1$　…②<br>"
         r"①，② より $\dfrac{AF'}{F'B}=\dfrac{AF}{FB}$。$F,\ F'$ はともに辺 $AB$ を同じ比に内分する点だから $F'=F$。<br>"
         r"したがって，3直線 $AD,\ BE,\ CF$ は1点 $O$ で交わる。　（終）",
  "note": r"この点をジェルゴンヌ点という。3本の内角の二等分線が1点（内心）で交わることも，$\dfrac{BD}{DC}\cdot\dfrac{CE}{EA}\cdot\dfrac{AF}{FB}=\dfrac cb\cdot\dfrac ac\cdot\dfrac ba=1$ とチェバの定理の逆から示せる（$a,\ b,\ c$ は3辺の長さ）。",
  "ex": r"$\triangle ABC$ の $\angle A$ 内の傍接円が辺 $BC$ に接する点を $D$，$\angle B$ 内の傍接円が辺 $CA$ に接する点を $E$，$\angle C$ 内の傍接円が辺 $AB$ に接する点を $F$ とする。$AD,\ BE,\ CF$ は1点で交わることを証明せよ。",
  "exa": r"$s=\dfrac{a+b+c}2$ とすると $BD=s-c,\ DC=s-b,\ CE=s-a,\ EA=s-c,\ AF=s-b,\ FB=s-a$（前節の例題と同様）で，比の積が $1$。チェバの定理の逆による（ナーゲル点）。"},
 {"lv": 3, "title": "メネラウスの定理の逆（3点が一直線上）",
  "q": r"$AB\neq AC$ である $\triangle ABC$ において，$\angle A$ の外角の二等分線と直線 $BC$ の交点を $D$，$\angle B$ の二等分線と辺 $CA$ の交点を $E$，$\angle C$ の二等分線と辺 $AB$ の交点を $F$ とする。3点 $D,\ E,\ F$ は一直線上にあることを証明せよ。" + _f34(),
  "hint": r"角の二等分線の性質で3つの比を辺の長さで表すと，積が $1$ になる。メネラウスの定理の逆を使うには，直線 $EF$ と直線 $BC$ の交点 $D'$ をとって $D'=D$ を示す。$EF\parallel BC$ とならないことの確認も必要。",
  "sol": r"$BC=a,\ CA=b,\ AB=c$ とする。角の二等分線の性質より<br>"
         r"$\dfrac{BD}{DC}=\dfrac{AB}{AC}=\dfrac cb$（$D$ は辺 $BC$ の延長上），$\dfrac{CE}{EA}=\dfrac{BC}{BA}=\dfrac ac$，$\dfrac{AF}{FB}=\dfrac{CA}{CB}=\dfrac ba$<br>"
         r"よって　$\dfrac{BD}{DC}\cdot\dfrac{CE}{EA}\cdot\dfrac{AF}{FB}=\dfrac cb\cdot\dfrac ac\cdot\dfrac ba=1$　…①<br>"
         r"もし $EF\parallel BC$ ならば $\dfrac{AF}{FB}=\dfrac{AE}{EC}$，すなわち $\dfrac ba=\dfrac ca$ となり $b\neq c$ に反する。よって直線 $EF$ は直線 $BC$ と1点 $D'$ で交わる。"
         r"直線 $EF$ は辺 $CA,\ AB$ と端点以外で交わり，1本の直線が三角形の3辺すべてと（端点以外で）交わることはないから，$D'$ は辺 $BC$ の延長上にある。$\triangle ABC$ と直線 $EF$ にメネラウスの定理を用いると<br>"
         r"$\dfrac{BD'}{D'C}\cdot\dfrac{CE}{EA}\cdot\dfrac{AF}{FB}=1$　…②<br>"
         r"①，② より $\dfrac{BD'}{D'C}=\dfrac{BD}{DC}=\dfrac cb$。$D,\ D'$ はともに辺 $BC$ を $c:b$ に外分する点であり，そのような点はただ1つだから $D'=D$。<br>"
         r"よって，$D,\ E,\ F$ は一直線上にある。　（終）",
  "note": r"「比の積が $1$」だけでは一直線上とはいえない（内分点3つでは積が $1$ でも一直線上にない）。逆を使うときは，延長上にある点が1個または3個であることを必ず確かめる。",
  "ex": r"3辺の長さがすべて異なる $\triangle ABC$ において，$\angle A,\ \angle B,\ \angle C$ の外角の二等分線と直線 $BC,\ CA,\ AB$ の交点をそれぞれ $D,\ E,\ F$ とする。$D,\ E,\ F$ は一直線上にあることを証明せよ。",
  "exa": r"$\dfrac{BD}{DC}=\dfrac cb,\ \dfrac{CE}{EA}=\dfrac ac,\ \dfrac{AF}{FB}=\dfrac ba$ で積は $1$。3点とも辺の延長上にあるので，例題と同様にメネラウスの定理の逆が使える。"},
 {"lv": 3, "title": "3本の線分で囲まれた三角形の面積",
  "q": r"$\triangle ABC$ の辺 $BC,\ CA,\ AB$ を $1:2$ に内分する点をそれぞれ $D,\ E,\ F$ とし，$AD$ と $BE$，$BE$ と $CF$，$CF$ と $AD$ の交点をそれぞれ $P,\ Q,\ R$ とする。$\triangle PQR$ の面積は $\triangle ABC$ の面積の何倍か。" + _f35(),
  "hint": r"$\triangle PQR$ を直接求めず，$\triangle ABC$ から周りの3つの三角形 $\triangle ABP,\ \triangle BCQ,\ \triangle CAR$ を引く。$\triangle ABP$ は $AP:PD$ がわかれば求まり，残りの2つも同じ配置である。",
  "sol": r"$\triangle ABC$ の面積を $!S$ とする。$\triangle ADC$ と直線 $BE$ にメネラウスの定理を用いると<br>"
         r"$\dfrac{AP}{PD}\cdot\dfrac{DB}{BC}\cdot\dfrac{CE}{EA}=\dfrac{AP}{PD}\cdot\dfrac13\cdot\dfrac12=1$　よって $AP:PD=6:1$<br>"
         r"$\triangle ABD=\dfrac13!S$ であるから　$\triangle ABP=\dfrac67\triangle ABD=\dfrac27!S$<br>"
         r"辺の分け方は $A\to B\to C$ の順に同じ規則（$BD:DC=CE:EA=AF:FB=1:2$）なので，同様に $\triangle BCQ=\triangle CAR=\dfrac27!S$。<br>"
         r"$\triangle ABC$ は $\triangle ABP,\ \triangle BCQ,\ \triangle CAR,\ \triangle PQR$ に分けられるから<br>"
         r"$\triangle PQR=!S-3\cdot\dfrac27!S=\dfrac17!S$　　答　$\boldsymbol{\dfrac17}$ <b>倍</b>",
  "note": r"一般に $BD:DC=CE:EA=AF:FB=1:k$ のとき，同様の計算で $\triangle PQR=\dfrac{(k-1)^2}{k^2+k+1}!S$ となる（ラウスの定理の特別な場合）。$k=1$（中線）なら $0$ で，3本は1点（重心）で交わる。",
  "ex": r"$\triangle ABC$ の辺 $BC,\ CA,\ AB$ を $1:3$ に内分する点をそれぞれ $D,\ E,\ F$ とし，例題と同様に $P,\ Q,\ R$ を定める。$\triangle PQR$ の面積は $\triangle ABC$ の面積の何倍か。",
  "exa": r"$\dfrac4{13}$ 倍"},
 {"lv": 4, "title": "チェバの定理と面積の最大",
  "q": r"$\triangle ABC$ の辺 $BC,\ CA,\ AB$ 上（端点を除く）にそれぞれ点 $D,\ E,\ F$ があり，$AD,\ BE,\ CF$ は1点で交わっている。$\triangle ABC$ の面積を $!S$ とするとき，$\triangle DEF$ の面積は $\dfrac14!S$ 以下であることを証明せよ。また，等号が成り立つのはどのようなときか。" + _f36(),
  "hint": r"チェバの定理より，正の数 $\alpha,\ \beta,\ \gamma$ を用いて $BD:DC=\gamma:\beta,\ CE:EA=\alpha:\gamma,\ AF:FB=\beta:\alpha$ と表せる。$\triangle DEF$ は $!S$ から隅の3つの三角形を引いたもの。最後は $(\alpha+\beta)^2\geqq4\alpha\beta$ を使う。",
  "sol": r"$\dfrac{BD}{DC}=u,\ \dfrac{CE}{EA}=v,\ \dfrac{AF}{FB}=w$ とおくと，チェバの定理より $uvw=1$。$\alpha=1,\ \beta=w,\ \gamma=\dfrac1v$ とおくと $\dfrac\beta\alpha=w,\ \dfrac\alpha\gamma=v,\ \dfrac\gamma\beta=\dfrac1{vw}=u$ であるから<br>"
         r"$BD:DC=\gamma:\beta,\ CE:EA=\alpha:\gamma,\ AF:FB=\beta:\alpha$　（$\alpha,\ \beta,\ \gamma>0$）<br>"
         r"と表せる。このとき　$\triangle AFE=\dfrac{AF}{AB}\cdot\dfrac{AE}{AC}!S=\dfrac{\beta\gamma}{(\alpha+\beta)(\gamma+\alpha)}!S$<br>"
         r"同様に　$\triangle BDF=\dfrac{\gamma\alpha}{(\beta+\gamma)(\alpha+\beta)}!S$，$\triangle CED=\dfrac{\alpha\beta}{(\gamma+\alpha)(\beta+\gamma)}!S$<br>"
         r"$\Pi=(\alpha+\beta)(\beta+\gamma)(\gamma+\alpha)$ とおくと，展開して $\Pi=\beta\gamma(\beta+\gamma)+\gamma\alpha(\gamma+\alpha)+\alpha\beta(\alpha+\beta)+2\alpha\beta\gamma$ であるから<br>"
         r"$\triangle DEF=!S-(\triangle AFE+\triangle BDF+\triangle CED)=\dfrac{\Pi-\{\beta\gamma(\beta+\gamma)+\gamma\alpha(\gamma+\alpha)+\alpha\beta(\alpha+\beta)\}}{\Pi}!S=\dfrac{2\alpha\beta\gamma}{\Pi}!S$<br>"
         r"$(\alpha+\beta)^2-4\alpha\beta=(\alpha-\beta)^2\geqq0$ などから $(\alpha+\beta)^2(\beta+\gamma)^2(\gamma+\alpha)^2\geqq64\alpha^2\beta^2\gamma^2$，すなわち $\Pi\geqq8\alpha\beta\gamma$。<br>"
         r"よって　$\triangle DEF\leqq\dfrac{2\alpha\beta\gamma}{8\alpha\beta\gamma}!S=\boldsymbol{\dfrac14!S}$<br>"
         r"等号は $\alpha=\beta=\gamma$，すなわち $\boldsymbol{D,\ E,\ F}$ <b>がそれぞれ辺の中点のとき</b>（3直線の交点が重心のとき）に限り成り立つ。",
  "note": r"3直線が1点で交わるという条件がないと，$D,\ E,\ F$ をそれぞれ $C,\ A,\ B$ の近くにとれば $\triangle DEF$ は $!S$ にいくらでも近づく。また $\alpha:\beta:\gamma$ は，3直線の交点 $O$ について $\triangle OBC:\triangle OCA:\triangle OAB$ に等しい。",
  "ex": r"例題と同じ設定で $BD:DC=1:2,\ CE:EA=1:1$ のとき，$AF:FB$ を求め，$\triangle DEF$ の面積を $!S$ で表せ。",
  "exa": r"$AF:FB=2:1$，$\triangle DEF=\dfrac29!S$"},
]})


# ================================================================ 節4 図
def _c41():
    O1, O2 = (0.0, 0.0), (2.75, 0.0)
    A, B, C, D = (onc(O1, 1, t) for t in (200, 300, 20, 70))
    B2, C2, D2, A2 = (onc(O2, 1, t) for t in (220, 350, 60, 140))
    T = add(C2, mul((math.cos(math.radians(80)), math.sin(math.radians(80))), 0.85))
    T0 = add(C2, mul((math.cos(math.radians(80)), math.sin(math.radians(80))), -0.45))
    return O1, A, B, C, D, O2, A2, B2, C2, D2, T, T0
def _f41():
    O1, A, B, C, D, O2, A2, B2, C2, D2, T, T0 = _c41(); E = inter(A, C, B, D)
    F = Fig([(-1, -1), (1, 1), (O2[0] + 1, 1), (O2[0] + 1, -1), T], w=250, h=112, pad=14)
    F.circ(O1, 1); F.poly([A, B, C, D]); F.seg(A, C); F.seg(B, D); F.seg(O1, A, wd=.8); F.seg(O1, B, wd=.8); F.dot(O1)
    F.labs({"A": A, "B": B, "C": C, "D": D}, O1); F.lab(O1, "O", -8, 2); F.lab(E, "E", 0, -8)
    F.circ(O2, 1); F.poly([A2, B2, C2, D2]); F.seg(B2, D2); F.seg(T0, T)
    F.labs({"A": A2, "B": B2, "C": C2, "D": D2}, O2); F.lab(T, "T", 7, 0)
    F.txt(10, 12, "(1)"); F.txt(F.T(O2)[0] - F.k * 1.15, 12, "(2)")
    return F.svg()
def _f42():
    A, B, C = tri(8, 5, 7); E, Fp = foot(B, C, A), foot(C, A, B); M = lerp(B, C, .5)
    F = Fig([A, B, C, (0, 4), (8, 4)], w=170, h=120)
    F.arc(M, 4, 0, 180, dash=True, col="#2a55b0"); F.poly([A, B, C]); F.seg(B, E); F.seg(C, Fp); F.seg(E, Fp, col="#c0392b", wd=1.3)
    F.ra(E, A, B, 4); F.ra(Fp, A, C, 4)
    F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(E, "E", 7, -2); F.lab(Fp, "F", -7, -2)
    return F.svg()
def _f43():
    A, B, C = (0.9, 3.3), (0.0, 0.0), (4.2, 0.0); O = circum(A, B, C); R = dist(O, A); I = incen(A, B, C)
    M = line_circ(A, I, O, R)[1]
    F = Fig([(O[0] - R, O[1] - R), (O[0] + R, O[1] + R)], w=150, h=150)
    F.circ(O, R); F.poly([A, B, C]); F.seg(A, M); F.seg(B, M); F.seg(C, M); F.seg(B, I, wd=.8); F.seg(C, I, wd=.8); F.dot(I)
    F.labs({"A": A, "B": B, "C": C, "M": M}, O); F.lab(I, "I", 8, -1)
    return F.svg()
def _f44():
    O = (0.0, 0.0); A, B, C, D = (onc(O, 1, t) for t in (150, 215, 300, 40))
    t = ang(D, B, C); u = sub(A, B); E = inter(B, add(B, rot(u, (0, 0), -t)), A, C)
    if dist(E, A) + dist(E, C) > dist(A, C) + 1e-9: E = inter(B, add(B, rot(u, (0, 0), t)), A, C)
    F = Fig([(-1, -1), (1, 1)], w=140, h=140)
    F.circ(O, 1); F.poly([A, B, C, D]); F.seg(A, C); F.seg(B, D); F.seg(B, E, col="#c0392b"); F.dot(E)
    F.labs({"A": A, "B": B, "C": C, "D": D}, O); F.lab(E, "E", 2, -8)
    return F.svg()
def _f45():
    A, B, C = tri(14, 15, 13); D, E, Fp = foot(A, B, C), foot(B, C, A), foot(C, A, B)
    D1, D2 = refl(D, A, B), refl(D, A, C)
    F = Fig([A, B, C, D1, D2], w=170, h=130)
    F.poly([A, B, C]); F.seg(D1, D2, dash=True, col="#c0392b"); F.poly([D, E, Fp], col="#c0392b", wd=1.3)
    F.seg(D, D1, dash=True, wd=.7); F.seg(D, D2, dash=True, wd=.7); F.seg(A, D, wd=.7)
    F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(D, "D", 0, 9); F.lab(E, "E", 8, 2); F.lab(Fp, "F", -7, 3)
    F.lab(D1, "D₁", -8, 2); F.lab(D2, "D₂", 9, 2)
    return F.svg()

# ---------------------------------------------------------------- 節4
SEC.append({"title": "円周角・円に内接する四角形・接弦定理",
"base": r"""・円周角の定理：1つの弧に対する円周角は一定で，その弧に対する中心角の半分。逆：2点 $P,\ Q$ が直線 $AB$ に関して同じ側にあり $\angle APB=\angle AQB$ ならば，$A,\ B,\ P,\ Q$ は同一円周上にある<br>
・円に内接する四角形：対角の和は $180^\circ$，外角はその内対角に等しい。逆に，これらのどちらかが成り立つ四角形は円に内接する<br>
・接弦定理：円の接線と，接点を通る弦のつくる角は，その角の内部にある弧に対する円周角に等しい""",
"items": [
 {"lv": 1, "title": "円周角・内接四角形・接弦定理と角の大きさ",
  "q": r"(1) 図のように，円 $O$ の周上に4点 $A,\ B,\ C,\ D$ があり，$\angle AOB=100^\circ,\ \angle CAD=25^\circ$ である。弦 $AC$ と $BD$ の交点を $E$ とするとき，$\angle ACB$ と $\angle AEB$ を求めよ。<br>"
       r"(2) 図のように，四角形 $ABCD$ は円に内接し，$\angle BAD=100^\circ$ である。直線 $CT$ は点 $C$ で円に接し，$\angle DCT=35^\circ$ である。$\angle BCD,\ \angle CBD,\ \angle BDC$ を求めよ。" + _f41(),
  "hint": r"(1) 円周角は中心角の半分。$\angle AEB$ は $\triangle EBC$ の外角とみる。(2) 内接四角形の対角の和は $180^\circ$。接線 $CT$ と弦 $CD$ のつくる角は，弧 $CD$ に対する円周角 $\angle CBD$ に等しい（接弦定理）。",
  "sol": r"(1) 弧 $AB$ に対する円周角と中心角の関係から　$\angle ACB=\dfrac12\angle AOB=\boldsymbol{50^\circ}$<br>"
         r"弧 $CD$ に対する円周角より $\angle DBC=\angle DAC=25^\circ$。$\angle AEB$ は $\triangle EBC$ の外角だから<br>"
         r"$\angle AEB=\angle ECB+\angle EBC=50^\circ+25^\circ=\boldsymbol{75^\circ}$<br>"
         r"(2) 対角の和は $180^\circ$ であるから　$\angle BCD=180^\circ-100^\circ=\boldsymbol{80^\circ}$<br>"
         r"接弦定理より　$\angle CBD=\angle DCT=\boldsymbol{35^\circ}$<br>"
         r"$\triangle BCD$ の内角の和より　$\angle BDC=180^\circ-80^\circ-35^\circ=\boldsymbol{65^\circ}$",
  "note": r"(1) の結果は「2弦の交角は，その角とその対頂角がはさむ2つの弧に対する円周角の和」$\angle AEB=\angle ACB+\angle CAD$ と覚えてもよい。接弦定理は，接点を通る直径をひいて直角をつくれば証明できる。",
  "ex": r"(1) 例題 (1) と同じ図で $\angle AOB=80^\circ,\ \angle CAD=30^\circ$ のとき，$\angle ACB$ と $\angle AEB$ を求めよ。<br>"
        r"(2) 例題 (2) と同じ図で $\angle BAD=110^\circ,\ \angle DCT=40^\circ$ のとき，$\angle BCD,\ \angle CBD,\ \angle BDC$ を求めよ。",
  "exa": r"(1) $\angle ACB=40^\circ,\ \angle AEB=70^\circ$　(2) $\angle BCD=70^\circ,\ \angle CBD=40^\circ,\ \angle BDC=70^\circ$"},
 {"lv": 2, "title": "4点が同一円周上にあることの証明",
  "q": r"鋭角三角形 $ABC$ の頂点 $B,\ C$ から対辺に下ろした垂線を $BE,\ CF$ とする。<br>"
       r"(1) 4点 $B,\ C,\ E,\ F$ は同一円周上にあることを示し，$\angle AEF=\angle ABC$ を証明せよ。<br>"
       r"(2) $AB=7,\ BC=8,\ CA=5$ のとき，線分 $EF$ の長さを求めよ。" + _f42(),
  "hint": r"(1) $\angle BEC=\angle BFC=90^\circ$ なので，$E,\ F$ は $BC$ を直径とする円周上にある（円周角の定理の逆）。内接四角形の外角は内対角に等しい。(2) (1) から $\triangle AEF\backsim\triangle ABC$ で，相似比は $\dfrac{AE}{AB}=\cos A$。",
  "sol": r"(1) $\angle BEC=\angle BFC=90^\circ$ であり，$E,\ F$ は直線 $BC$ に関して同じ側にあるから，円周角の定理の逆により $E,\ F$ は $BC$ を直径とする円周上にある。よって $B,\ C,\ E,\ F$ は同一円周上にある。<br>"
         r"四角形 $BCEF$ は円に内接するので，その外角 $\angle AEF$ は内対角 $\angle FBC$ に等しい。すなわち　$\angle AEF=\angle ABC$　（終）<br>"
         r"(2) $\triangle AEF$ と $\triangle ABC$ は $\angle A$ が共通で $\angle AEF=\angle ABC$ だから相似であり，相似比は $AE:AB$。直角三角形 $ABE$ で $AE=AB\cos A$ であるから　$EF=BC\cos A$<br>"
         r"$\cos A=\dfrac{7^2+5^2-8^2}{2\cdot7\cdot5}=\dfrac17$ より　$EF=8\cdot\dfrac17=\boldsymbol{\dfrac87}$",
  "note": r"4点が同一円周上にあることを示すには，① 円周角の定理の逆，② 対角の和が $180^\circ$，③ 外角が内対角に等しい，④ 方べきの定理の逆，のいずれかを使う。垂心 $H$ について，$A,\ F,\ H,\ E$ も $AH$ を直径とする円周上にある。",
  "ex": r"$AB=5,\ BC=7,\ CA=6$ の鋭角三角形 $ABC$ の頂点 $B,\ C$ から対辺に下ろした垂線の足を $E,\ F$ とするとき，$EF$ の長さを求めよ。",
  "exa": r"$EF=\dfrac75$"},
 {"lv": 3, "title": "内心と外接円（MB＝MI＝MC）",
  "q": r"$\triangle ABC$ の内心を $I$ とし，直線 $AI$ と $\triangle ABC$ の外接円の $A$ 以外の交点を $M$ とする。$MB=MC=MI$ であることを証明せよ。" + _f43(),
  "hint": r"$AM$ は $\angle A$ を二等分するので，弦 $MB$ と $MC$ に対する円周角が等しい。$MB=MI$ は $\triangle MBI$ が二等辺三角形であること，すなわち $\angle MBI=\angle MIB$ を示せばよい。どちらも $\dfrac12(\angle A+\angle B)$ になる。",
  "sol": r"$\angle A=2\alpha,\ \angle B=2\beta$ とおく。$\angle BAM=\angle CAM=\alpha$ であり，等しい円周角に対する弦は等しいから　$MB=MC$<br>"
         r"$M$ は $A$ を含まない弧 $BC$ 上にあるので，弧 $MC$ に対する円周角より $\angle MBC=\angle MAC=\alpha$。よって<br>"
         r"$\angle MBI=\angle MBC+\angle CBI=\alpha+\beta$<br>"
         r"一方，$\angle MIB$ は $\triangle ABI$ の外角であるから　$\angle MIB=\angle IAB+\angle IBA=\alpha+\beta$<br>"
         r"よって $\angle MBI=\angle MIB$ となり，$\triangle MBI$ は $MB=MI$ の二等辺三角形である。以上より　$MB=MC=MI$　（終）",
  "note": r"$M$ は $\triangle IBC$ の外接円の中心である。この性質は内心と外接円が絡む問題で頻出で，後の節の $OI^2=!R^2-2!Rr$ の証明にも使う。$\angle A$ 内の傍心もこの円の上にある（練習）。",
  "ex": r"例題と同じ設定で，$\angle A$ 内の傍心を $J$ とする。$MJ=MB$ を証明せよ（したがって $M$ は線分 $IJ$ の中点である）。",
  "exa": r"$BI,\ BJ$ は $\angle B$ の内角・外角の二等分線なので $\angle IBJ=90^\circ$。$\angle MBJ=90^\circ-\angle MBI=90^\circ-\angle MIB=\angle MJB$ より $MB=MJ$。"},
 {"lv": 4, "title": "トレミーの定理",
  "q": r"(1) 円に内接する四角形 $ABCD$ において，$AB\cdot CD+AD\cdot BC=AC\cdot BD$ が成り立つことを証明せよ。<br>(2) 1辺の長さが $1$ の正五角形の対角線の長さを求めよ。" + _f44(),
  "hint": r"対角線 $AC$ 上に $\angle ABE=\angle DBC$ となる点 $E$ をとると，相似な三角形が2組できる。$AB\cdot CD=AE\cdot BD$，$AD\cdot BC=EC\cdot BD$ を示して加える。(2) は正五角形の4頂点でできる四角形に (1) を使う。",
  "sol": r"(1) $\angle DBC<\angle ABC$ だから，対角線 $AC$ 上に $\angle ABE=\angle DBC$ となる点 $E$ がとれる。<br>"
         r"$\triangle ABE$ と $\triangle DBC$ において，$\angle ABE=\angle DBC$，弧 $BC$ に対する円周角より $\angle BAE=\angle BAC=\angle BDC$。よって $\triangle ABE\backsim\triangle DBC$ で $\dfrac{AB}{DB}=\dfrac{AE}{DC}$，すなわち　$AB\cdot CD=AE\cdot BD$　…①<br>"
         r"$\triangle EBC$ と $\triangle ABD$ において，$\angle EBC=\angle ABC-\angle ABE=\angle ABC-\angle DBC=\angle ABD$，弧 $AB$ に対する円周角より $\angle ECB=\angle ACB=\angle ADB$。よって $\triangle EBC\backsim\triangle ABD$ で $\dfrac{BC}{BD}=\dfrac{EC}{AD}$，すなわち　$AD\cdot BC=EC\cdot BD$　…②<br>"
         r"①＋② より　$AB\cdot CD+AD\cdot BC=(AE+EC)BD=AC\cdot BD$　（終）<br>"
         r"(2) 正五角形を $PQRST$，対角線の長さを $x$ とする。四角形 $PQRS$ は円に内接し，$PQ=QR=RS=1,\ PR=QS=PS=x$。(1) より $1\cdot1+x\cdot1=x\cdot x$，$x^2-x-1=0$。$x>0$ より　$x=\boldsymbol{\dfrac{1+\sqrt5}2}$",
  "note": r"一般の四角形では $AB\cdot CD+AD\cdot BC\geqq AC\cdot BD$（トレミーの不等式）で，等号は円に内接するときに限る。(2) の値は黄金比で，頂角 $36^\circ$ の二等辺三角形 $PRS$ などから $\cos36^\circ=\dfrac{1+\sqrt5}4$ も得られる。",
  "ex": r"正七角形 $ABCDEFG$ において，$\dfrac1{AB}=\dfrac1{AC}+\dfrac1{AD}$ が成り立つことを証明せよ。",
  "exa": r"$AB=a,\ AC=b,\ AD=c$ とすると，円に内接する四角形 $ACDE$ で $AC=CE=b,\ CD=DE=a,\ AD=AE=c$。トレミーの定理より $ba+ac=cb$，両辺を $abc$ で割る。"},
 {"lv": 5, "title": "周の長さが最小の内接三角形（垂足三角形）",
  "q": r"鋭角三角形 $ABC$ の辺 $BC,\ CA,\ AB$ 上（端点を除く）にそれぞれ点 $P,\ Q,\ R$ をとる。<br>"
       r"(1) $PQ+QR+RP\geqq2AP\sin A$ であることを示せ。<br>"
       r"(2) $A,\ B,\ C$ から対辺に下ろした垂線の足を $D,\ E,\ F$ とする。$\triangle DEF$ の周の長さは $2AD\sin A$ に等しいことを示せ。<br>"
       r"(3) $AB=13,\ BC=14,\ CA=15$ のとき，$PQ+QR+RP$ の最小値を求めよ。",
  "hint": r"(1) $P$ を $AB,\ AC$ に関して折り返した点 $P_1,\ P_2$ をとると，周の長さは折れ線 $P_1RQP_2$ の長さになる。$\triangle AP_1P_2$ は頂角 $2A$ の二等辺三角形。(2) この節の「4点が同一円周上にあることの証明」の例題と同様にして $\angle AFE=\angle BFD=\angle C$ を導き，$D$ を折り返した点と $F,\ E$ が一直線上にあることを示す。",
  "sol": _f45() + r"(1) $P$ を直線 $AB,\ AC$ に関して対称移動した点を $P_1,\ P_2$ とすると，$RP=RP_1,\ QP=QP_2$ であるから<br>"
         r"$PQ+QR+RP=P_1R+RQ+QP_2\geqq P_1P_2$（折れ線の長さは両端を結ぶ線分の長さ以上）<br>"
         r"$AP_1=AP_2=AP$，$\angle P_1AP_2=2\angle BAP+2\angle PAC=2A\ (<180^\circ)$ であるから，二等辺三角形 $AP_1P_2$ の頂点 $A$ から底辺に垂線を下ろして考えると $P_1P_2=2AP\sin A$。<br>"
         r"よって　$PQ+QR+RP\geqq2AP\sin A$　（終）<br>"
         r"(2) $\angle BEC=\angle BFC=90^\circ$ より $B,\ C,\ E,\ F$ は $BC$ を直径とする円周上にあり，内接四角形 $BCEF$ の外角として $\angle AFE=\angle C$。同様に $A,\ C,\ D,\ F$ は $AC$ を直径とする円周上にあり，$\angle BFD=\angle C$。<br>"
         r"$D$ を直線 $AB,\ AC$ に関して対称移動した点を $D_1,\ D_2$ とすると $\angle BFD_1=\angle BFD=\angle C=\angle AFE$。$D_1$ と $E$ は直線 $AB$ に関して反対側にあるから，$\angle BFD_1$ と $\angle AFE$ は対頂角の位置にあり，$D_1,\ F,\ E$ はこの順に一直線上にある。同様に $F,\ E,\ D_2$ もこの順に一直線上にある。<br>"
         r"よって　$DF+FE+ED=D_1F+FE+ED_2=D_1D_2=2AD\sin A$　（終）<br>"
         r"(3) (1) と $AP\geqq AD$ より，どのような $P,\ Q,\ R$ に対しても $PQ+QR+RP\geqq2AP\sin A\geqq2AD\sin A$ であり，(2) より $P,\ Q,\ R$ を $D,\ E,\ F$ にとると等号が成り立つ。よって最小値は $2AD\sin A$ である。<br>"
         r"$\cos B=\dfrac{13^2+14^2-15^2}{2\cdot13\cdot14}=\dfrac5{13}$，$\sin B=\dfrac{12}{13}$ より $AD=AB\sin B=12$，$\triangle ABC=\dfrac12\cdot14\cdot12=84$。<br>"
         r"$84=\dfrac12\cdot13\cdot15\sin A$ より $\sin A=\dfrac{56}{65}$。よって最小値は　$2\cdot12\cdot\dfrac{56}{65}=\boldsymbol{\dfrac{1344}{65}}$",
  "note": r"最小値は $2AD\sin A=\dfrac{2\triangle ABC}{!R}$（$!R$ は外接円の半径）とも表せる。垂足三角形 $DEF$ では各頂点で「入射角＝反射角」（$\angle AFE=\angle BFD$ など）が成り立っており，光の反射の経路として最短になっている（ファニャノの問題）。「$P$ を固定して $Q,\ R$ を最適化 → $P$ を最適化」という2段階の最小化が考え方の骨格である。",
  "ex": r"$AB=AC=5,\ BC=6$ の三角形 $ABC$ の辺 $BC,\ CA,\ AB$ 上（端点を除く）にそれぞれ点 $P,\ Q,\ R$ をとるとき，$PQ+QR+RP$ の最小値を求めよ。",
  "exa": r"$\dfrac{192}{25}$"},
]})


# ================================================================ 節5 図
def _c51():
    """方べきの3つの図の点。P は x 軸上、円の中心は原点"""
    def u(px, pu, sg):
        c = pu / px; return (c, sg * math.sqrt(1 - c * c))
    def at(P, v, t): return add(P, mul(v, t))
    P1 = (2 * math.sqrt(3), 0.0); a, c = u(P1[0], -1, 1), u(P1[0], -2.5, -1)
    g1 = dict(R=6, P=P1, A=at(P1, a, -4), B=at(P1, a, 6), C=at(P1, c, -3), D=at(P1, c, 8))
    P2 = (-math.sqrt(33), 0.0); a, c = u(P2[0], -5.5, 1), u(P2[0], -5, -1)
    g2 = dict(R=3, P=P2, A=at(P2, a, 3), B=at(P2, a, 8), C=at(P2, c, 4), D=at(P2, c, 6))
    P3 = (-math.sqrt(45), 0.0); a = u(P3[0], -6.5, 1)
    g3 = dict(R=3, P=P3, A=at(P3, a, 4), B=at(P3, a, 9), T=(-9 / math.sqrt(45), -18 / math.sqrt(45)))
    return g1, g2, g3
def _f51():
    g1, g2, g3 = _c51(); O = (0.0, 0.0); figs = []
    for g in (g1, g2, g3):
        R = g["R"]; F = Fig([(-R, -R), (R, R), g["P"]], w=86, h=82, pad=13)
        F.circ(O, R)
        if "C" in g:
            if g is g1: F.seg(g["A"], g["B"]); F.seg(g["C"], g["D"])
            else: F.seg(g["P"], g["B"]); F.seg(g["P"], g["D"])
        else:
            F.seg(g["P"], g["B"]); F.seg(g["P"], g["T"])
        F.dot(g["P"]); c = O if g is g1 else lerp(O, g["P"], .35)
        F.labs({k: v for k, v in g.items() if k not in ("R", "P")}, c)
        F.lab(g["P"], "P", -8 if g is g1 else -7, 2 if g is g1 else 0)
        figs.append(F)
    return hcat(figs, 6, ["(1)", "(2)", "(3)"])
def _f52():
    O, O2 = (0.0, 0.0), (7.0, 0.0); n = (-2 / 7, math.sqrt(45) / 7); m = (6 / 7, -math.sqrt(13) / 7)
    S, S2 = mul(n, 2), add(O2, mul(n, 4)); T, T2 = mul(m, 2), sub(O2, mul(m, 4)); H = add(O2, mul(n, 2))
    F = Fig([(-2, -2), (11, 4), (11, -4), lerp(S, S2, -.15), lerp(S, S2, 1.15)], w=180, h=110)
    F.circ(O, 2); F.circ(O2, 4); F.seg(lerp(S, S2, -.15), lerp(S, S2, 1.15)); F.seg(lerp(T, T2, -.2), lerp(T, T2, 1.25))
    F.seg(O, S, wd=.8); F.seg(O2, S2, wd=.8); F.seg(O, H, dash=True); F.seg(O, O2, wd=.7, dash=True)
    for p in (O, O2, S, S2, T, T2): F.dot(p, 1.5)
    F.lab(O, "O", -2, 8); F.lab(O2, "O′", 0, 9); F.lab(S, "S", -5, -7); F.lab(S2, "S′", -2, -8); F.lab(H, "H", 8, 3)
    F.lab(T, "T", 3, 9); F.lab(T2, "T′", -9, -4)
    return F.svg()
def _f53():
    A, B, C = tri(5, 4, 6); O = circum(A, B, C); R = dist(O, A); Pp = (9.0, 0.0)
    F = Fig([(O[0] - R, O[1] - R), (O[0] + R, O[1] + R), Pp], w=200, h=110)
    F.circ(O, R); F.poly([A, B, C]); F.seg(C, Pp); F.seg(lerp(Pp, A, 1.18), Pp)
    F.labs({"A": A, "B": B, "C": C}, O); F.lab(Pp, "P", 3, 8)
    return F.svg()
def _c54():
    M, A, B = (0.0, 0.0), (0.0, 4.0), (0.0, 9.0); th = math.radians(10); e = (math.cos(th), math.sin(th)); n = (-math.sin(th), math.cos(th))
    S, T = mul(e, -6), mul(e, 6); cs = []
    for X in (S, T):
        k = -dot(sub(X, A), sub(X, A)) / (2 * dot(n, sub(X, A))); cs.append((add(X, mul(n, k)), k))
    return M, A, B, S, T, cs
def _f54():
    M, A, B, S, T, cs = _c54()
    pts = [lerp(S, T, -.2), lerp(S, T, 1.2)] + [(z[0] + sg * k, z[1] + sg * k) for z, k in cs for sg in (1, -1)]
    F = Fig(pts, w=200, h=160)
    for z, k in cs: F.circ(z, k)
    F.seg(lerp(S, T, -.2), lerp(S, T, 1.2)); F.seg((0, -1.2), (0, 10.5), dash=True)
    for p in (M, A, B, S, T): F.dot(p, 1.5)
    F.lab(M, "M", 6, 8); F.lab(A, "A", 7, 4); F.lab(B, "B", 7, -5); F.lab(S, "S", -2, 9); F.lab(T, "T", 2, 9)
    F.lab(onc(cs[0][0], cs[0][1], 140), "K", -7, -6); F.lab(onc(cs[1][0], cs[1][1], 40), "L", 7, -6)
    return F.svg()
def _f55():
    A, B, C = tri(14, 15, 13); O = circum(A, B, C); R = dist(O, A); I = incen(A, B, C); r = dist(I, foot(I, B, C))
    M = line_circ(A, I, O, R)[1]; X, Y = line_circ(I, O, O, R)
    F = Fig([(O[0] - R, O[1] - R), (O[0] + R, O[1] + R)], w=150, h=150)
    F.circ(O, R); F.poly([A, B, C]); F.circ(I, r, wd=.7); F.seg(A, M); F.seg(M, B); F.seg(X, Y, dash=True)
    F.dot(O); F.dot(I)
    F.labs({"A": A, "B": B, "C": C, "M": M, "X": X, "Y": Y}, O); F.lab(O, "O", 4, -7); F.lab(I, "I", -7, -3)
    return F.svg()
def _c56():
    Z, R = (0.0, 0.8), 2.0; h = math.sqrt(R * R - 0.64); P, Q, M = (-h, 0.0), (h, 0.0), (0.0, 0.0)
    a = line_circ(M, onc(M, 1, 115), Z, R); c = line_circ(M, onc(M, 1, 60), Z, R)
    A, B = (a[1], a[0]) if a[1][1] > 0 else (a[0], a[1]); C, D = (c[1], c[0]) if c[1][1] > 0 else (c[0], c[1])
    return Z, R, P, Q, M, A, B, C, D, inter(A, D, P, Q), inter(C, B, P, Q)
def _f56():
    Z, R, P, Q, M, A, B, C, D, X, Y = _c56()
    F = Fig([(Z[0] - R, Z[1] - R), (Z[0] + R, Z[1] + R)], w=165, h=165)
    F.circ(Z, R); F.seg(P, Q, wd=1.3); F.seg(A, B); F.seg(C, D); F.seg(A, D, col="#c0392b"); F.seg(C, B, col="#c0392b")
    for p in (M, X, Y): F.dot(p, 1.6)
    F.labs({"A": A, "B": B, "C": C, "D": D, "P": P, "Q": Q}, Z); F.lab(M, "M", 0, 9); F.lab(X, "X", -6, -7); F.lab(Y, "Y", 6, -7)
    return F.svg()

# ---------------------------------------------------------------- 節5
SEC.append({"title": "方べきの定理・2円の位置関係・共通接線",
"base": r"""・方べきの定理：点 $P$ を通る2直線が円とそれぞれ $A,\ B$ および $C,\ D$ で交わるとき $PA\cdot PB=PC\cdot PD$。直線 $PT$ が点 $T$ で円に接するときは $PA\cdot PB=PT^2$<br>
・方べきの定理の逆：2線分 $AB,\ CD$（またはその延長）が点 $P$ で交わり $PA\cdot PB=PC\cdot PD$ ならば，$A,\ B,\ C,\ D$ は同一円周上にある<br>
・2円（半径 $r>r'$，中心間の距離 $d$）：$d>r+r'$（離れている，共通接線4本），$d=r+r'$（外接，3本），$r-r'<d<r+r'$（2点で交わる，2本），$d=r-r'$（内接，1本），$d<r-r'$（内部にある，0本）<br>
・共通接線の2接点間の距離：共通外接線 $\sqrt{d^2-(r-r')^2}$，共通内接線 $\sqrt{d^2-(r+r')^2}$""",
"items": [
 {"lv": 1, "title": "方べきの定理",
  "q": r"次の各場合に $x$ を求めよ。(1)〜(3) はそれぞれ図の (1)〜(3) に対応する。<br>"
       r"(1) 2つの弦 $AB,\ CD$ が円の内部の点 $P$ で交わり，$PA=4,\ PB=6,\ PC=3,\ PD=x$<br>"
       r"(2) 円の外部の点 $P$ を通る2直線が円と $A,\ B$ および $C,\ D$ で交わり，$PA=3,\ AB=5,\ PC=4,\ CD=x$<br>"
       r"(3) 円の外部の点 $P$ から引いた接線の接点を $T$ とし，$P$ を通る直線が円と $A,\ B$ で交わり，$PA=4,\ AB=5,\ PT=x$" + _f51(),
  "hint": r"どの場合も「点 $P$ から円との2交点までの長さの積」が一定。(2) では $PB=PA+AB$，$PD=PC+CD$ のように，$P$ からの長さに直してから使う。",
  "sol": r"(1) $PA\cdot PB=PC\cdot PD$ より $4\cdot6=3x$　よって　$x=\boldsymbol{8}$<br>"
         r"(2) $PB=3+5=8,\ PD=4+x$ で，$PA\cdot PB=PC\cdot PD$ より $3\cdot8=4(4+x)$　よって　$x=\boldsymbol{2}$<br>"
         r"(3) $PB=4+5=9$ で，$PT^2=PA\cdot PB$ より $x^2=36$。$x>0$ より　$x=\boldsymbol{6}$",
  "note": r"(1)〜(3) はどれも「$P$ を通る直線と円の2交点を $X,\ Y$ とすると $PX\cdot PY$ は直線によらず一定」という1つの事実で，その値は円の中心を $O$，半径を $r$ として $|OP^2-r^2|$ である。証明は相似な三角形による（例えば (1) では $\triangle PAC\backsim\triangle PDB$）。",
  "ex": r"(1) 2つの弦 $AB,\ CD$ が円の内部の点 $P$ で交わり，$PA=5,\ PB=4,\ PC=2$ のとき，$PD$ を求めよ。<br>"
        r"(2) 円の外部の点 $P$ を通る2直線が円と $A,\ B$ および $C,\ D$ で交わり，$PA=2,\ AB=10,\ PC=3$ のとき，$CD$ を求めよ。<br>"
        r"(3) 円の外部の点 $P$ から引いた接線の接点を $T$，$P$ を通る直線と円の交点を $A,\ B$ とする。$PA=2,\ AB=6$ のとき，$PT$ を求めよ。",
  "exa": r"(1) $PD=10$　(2) $CD=5$　(3) $PT=4$"},
 {"lv": 2, "title": "2円の位置関係と共通接線の長さ",
  "q": r"半径 $r$ の円 $O$ と半径 $4$ の円 $O'$ があり，中心間の距離は $OO'=7$ である。<br>"
       r"(1) 2円が異なる2点で交わるような $r$ の値の範囲を求めよ。<br>"
       r"(2) 2円の共通接線がちょうど3本となる $r$，ちょうど1本となる $r$ をそれぞれ求めよ。<br>"
       r"(3) $r=2$ のとき，共通外接線（2円が接線に関して同じ側にあるもの）の2接点間の距離と，共通内接線の2接点間の距離を求めよ。",
  "hint": r"中心間の距離 $d$ と，半径の和・差を比べる。(2) 共通接線が3本なら外接，1本なら内接。(3) 接点を $S,\ S'$ とし，$O$ から $O'S'$ に垂線を下ろすと，斜辺が $OO'$ の直角三角形ができる（$OS\perp SS',\ O'S'\perp SS'$）。",
  "sol": r"(1) 条件は $|r-4|<7<r+4$。$7<r+4$ より $r>3$，$|r-4|<7$ より $-3<r<11$。よって　$\boldsymbol{3<r<11}$<br>"
         r"(2) 共通接線が3本となるのは外接するときで，$r+4=7$ より $\boldsymbol{r=3}$。1本となるのは内接するときで，$|r-4|=7,\ r>0$ より $\boldsymbol{r=11}$<br>"
         + _f52() + r"(3) $r=2$ のとき $2+4<7$ で，2円は互いに外部にある。共通外接線が2円に接する点を $S,\ S'$ とする。$OS\perp SS',\ O'S'\perp SS'$ だから，$O$ から $O'S'$ に下ろした垂線の足を $H$ とすると，四角形 $OSS'H$ は長方形で $OH=SS'$，$O'H=4-2=2$。直角三角形 $OHO'$ より<br>"
         r"$SS'=\sqrt{7^2-2^2}=\boldsymbol{3\sqrt5}$<br>"
         r"共通内接線が2円に接する点を $T,\ T'$ とすると，同様に $O$ から直線 $O'T'$ に下ろした垂線の足 $K$ について $O'K=4+2=6$ となるから　$TT'=\sqrt{7^2-6^2}=\boldsymbol{\sqrt{13}}$",
  "note": r"2円の位置関係は「$d$ と $r+r'$，$|r-r'|$ の大小」だけで決まる。共通接線の長さは，接点への半径が接線に垂直であることから直角三角形をつくって求めるのが定石。",
  "ex": r"(1) 半径 $2$ と $6$ の2円の中心間の距離が $10$ のとき，共通外接線，共通内接線の2接点間の距離をそれぞれ求めよ。<br>"
        r"(2) 半径 $4$ と $9$ の2円が外接し，ともに直線 $\ell$ に接している。$\ell$ 上の2つの接点間の距離を求めよ。",
  "exa": r"(1) $2\sqrt{21},\ 6$　(2) $12$"},
 {"lv": 3, "title": "接線と相似（接弦定理と方べき）",
  "q": r"$AB=6,\ BC=5,\ CA=4$ の $\triangle ABC$ の外接円の，点 $A$ における接線と直線 $BC$ の交点を $P$ とする。線分 $PA,\ PB,\ PC$ の長さを求めよ。" + _f53(),
  "hint": r"接弦定理より $\angle PAC=\angle PBA$ となり，$\triangle PAC\backsim\triangle PBA$。相似比 $CA:AB$ を使って $PA,\ PB$ を $PC$ で表し，$PB-PC=BC$ から決定する（方べきの定理 $PA^2=PB\cdot PC$ と同じ内容）。",
  "sol": r"接線上の点 $T$ を直線 $AC$ に関して $B$ と反対側にとると，接弦定理より $\angle TAC=\angle B$。$AB>AC$ より $\angle C>\angle B$ で，$\angle B+(180^\circ-\angle C)<180^\circ$ であるから，半直線 $AT$ は辺 $BC$ の $C$ の側の延長と交わる。この交点が $P$ であり　$\angle PAC=\angle ABC=\angle PBA$<br>"
         r"また $\angle APC=\angle BPA$（共通）。よって　$\triangle PAC\backsim\triangle PBA$<br>"
         r"相似比は $AC:BA=4:6=2:3$ であるから　$\dfrac{PC}{PA}=\dfrac{PA}{PB}=\dfrac23$<br>"
         r"$PC=x$ とおくと $PA=\dfrac32x,\ PB=\dfrac32PA=\dfrac94x$。$PB-PC=BC=5$ より $\dfrac54x=5$，$x=4$。<br>"
         r"よって　$\boldsymbol{PA=6,\ PB=9,\ PC=4}$",
  "note": r"結果は方べきの定理 $PA^2=PB\cdot PC$（$36=9\cdot4$）と一致する。一般に $\dfrac{PB}{PC}=\left(\dfrac{AB}{AC}\right)^2$ となり，$P$ は辺 $BC$ を $AB^2:AC^2$ に外分する点である。",
  "ex": r"$AB=5,\ BC=4,\ CA=3$ の $\triangle ABC$ の外接円の，点 $A$ における接線と直線 $BC$ の交点を $P$ とするとき，$PA,\ PB,\ PC$ を求めよ。",
  "exa": r"$PA=\dfrac{15}4,\ PB=\dfrac{25}4,\ PC=\dfrac94$"},
 {"lv": 3, "title": "2円の共通弦と共通接線（方べきの利用）",
  "q": r"2つの円 $K,\ L$ が2点 $A,\ B$ で交わっている。2円の共通接線の1つが $K,\ L$ とそれぞれ点 $S,\ T$ で接し，直線 $AB$ と直線 $ST$ の交点を $M$ とする。<br>"
       r"(1) $MS=MT$ を証明せよ。<br>(2) $M,\ A,\ B$ がこの順に並び，$MA=4,\ AB=5$ のとき，$ST$ の長さを求めよ。" + _f54(),
  "hint": r"$M$ は直線 $AB$ 上の点なので，2円のどちらに対しても同じ積 $MA\cdot MB$ が現れる。接線の長さの2乗は方べきに等しい。",
  "sol": r"(1) $M$ は接線 $ST$ 上の点で $S,\ T$ と異なるから，円 $K,\ L$ の外部にある。<br>"
         r"円 $K$ について方べきの定理より $MS^2=MA\cdot MB$，円 $L$ について $MT^2=MA\cdot MB$。<br>"
         r"よって $MS^2=MT^2$，$MS=MT$　（終）<br>"
         r"(2) $MB=4+5=9$ より $MS^2=4\cdot9=36$，$MS=6$。(1) より $M$ は線分 $ST$ の中点だから　$ST=2MS=\boldsymbol{12}$",
  "note": r"2円の共通弦を含む直線上（共通弦の外側）の点からは，2円に引いた接線の長さが等しい。この直線を2円の根軸という。3つの円がどの2つも2点で交わるとき，3本の共通弦を含む直線は1点で交わる（または互いに平行）。",
  "ex": r"3つの円 $K_1,\ K_2,\ K_3$ があり，どの2つも2点で交わる。$K_1$ と $K_2$，$K_1$ と $K_3$ の共通弦の延長が，3つの円のいずれの外部にもある点 $P$ で交わるとき，$K_2$ と $K_3$ の共通弦の延長も $P$ を通ることを証明せよ。",
  "exa": r"$P$ から3円に引いた接線の長さは例題 (1) と同様にすべて等しく，これを $t$ とする。$K_2,\ K_3$ の共有点の1つを $C$ とし，直線 $PC$ と $K_2,\ K_3$ の $C$ 以外の交点を $D,\ D'$ とすると $PC\cdot PD=t^2=PC\cdot PD'$ より $D=D'$。これは $K_2,\ K_3$ のもう1つの共有点であり，$P$ は直線 $CD$ 上にある。"},
 {"lv": 4, "title": "外心と内心の距離（オイラーの定理）",
  "q": r"$\triangle ABC$ の外接円の中心を $O$，半径を $!R$，内接円の中心を $I$，半径を $r$ とする。<br>"
       r"(1) $OI^2=!R^2-2!Rr$ を証明せよ。<br>(2) $AB=13,\ BC=14,\ CA=15$ のとき，$OI$ の長さを求めよ。" + _f55(),
  "hint": r"直線 $AI$ と外接円の交点 $M$ をとる。点 $I$ を通る直径 $XY$ を考えると，方べきの定理より $AI\cdot IM=XI\cdot IY=!R^2-OI^2$。一方 $AI=\dfrac r{\sin\frac A2}$ であり，前の節の例題より $IM=MB=2!R\sin\dfrac A2$。",
  "sol": r"直線 $AI$ と外接円の $A$ 以外の交点を $M$ とする。<br>"
         r"【方べき】$I\neq O$ のとき，直線 $OI$ と外接円の交点を $X,\ Y$（$X$ は $I$ の側）とする。$I$ は円の内部にあるから，方べきの定理より<br>"
         r"$AI\cdot IM=XI\cdot IY=(!R-OI)(!R+OI)=!R^2-OI^2$<br>"
         r"（$I=O$ のときも，任意の直径 $XY$ について同じ式が成り立つ。）<br>"
         r"【$AI\cdot IM$ の計算】$I$ から辺 $AB$ に下ろした垂線の足を $F$ とすると，$IF=r,\ \angle IAF=\dfrac A2$ より　$AI=\dfrac r{\sin\frac A2}$<br>"
         r"$\triangle ABM$ に正弦定理を用いると $\dfrac{MB}{\sin\angle BAM}=2!R$ より $MB=2!R\sin\dfrac A2$。前の節の例題より $IM=MB$ であるから<br>"
         r"$AI\cdot IM=\dfrac r{\sin\frac A2}\cdot2!R\sin\dfrac A2=2!Rr$<br>"
         r"以上より $!R^2-OI^2=2!Rr$，すなわち　$OI^2=!R^2-2!Rr$　（終）<br>"
         r"(2) $\cos B=\dfrac{13^2+14^2-15^2}{2\cdot13\cdot14}=\dfrac5{13}$ より $\sin B=\dfrac{12}{13}$，$\triangle ABC=\dfrac12\cdot13\cdot14\cdot\dfrac{12}{13}=84$。<br>"
         r"$r=\dfrac{2\cdot84}{13+14+15}=4$，正弦定理より $!R=\dfrac{CA}{2\sin B}=\dfrac{15}{2}\cdot\dfrac{13}{12}=\dfrac{65}8$<br>"
         r"$OI^2=\left(\dfrac{65}8\right)^2-2\cdot\dfrac{65}8\cdot4=\dfrac{4225-4160}{64}=\dfrac{65}{64}$　よって　$OI=\boldsymbol{\dfrac{\sqrt{65}}8}$",
  "note": r"$OI^2\geqq0$ より $!R\geqq2r$（オイラーの不等式）で，等号は $O=I$，すなわち正三角形のときに限る。$\angle A$ 内の傍心 $J$ と傍接円の半径 $r'$ についても，同様にして $OJ^2=!R^2+2!Rr'$ が成り立つ。",
  "ex": r"$AB=AC=5,\ BC=6$ の $\triangle ABC$ の外心を $O$，内心を $I$ とするとき，$OI$ の長さを求めよ。",
  "exa": r"$OI=\dfrac58$（$!R=\dfrac{25}8,\ r=\dfrac32$）"},
 {"lv": 5, "title": "バタフライ定理（面積比と方べき）",
  "q": r"円の弦 $PQ$ の中点を $M$ とし，$M$ を通る2本の弦 $AB,\ CD$ を，$A,\ C$ が直線 $PQ$ に関して同じ側にあるようにひく。弦 $AD,\ CB$ と弦 $PQ$ の交点をそれぞれ $X,\ Y$ とするとき，$MX=MY$ であることを証明せよ。" + _f56(),
  "hint": r"$MX=x,\ MY=y$ とおき，面積の比 $\dfrac{\triangle AMX\cdot\triangle DMX}{\triangle CMY\cdot\triangle BMY}$ を「$M$ の角を使う」「$A,\ D,\ C,\ B$ の角を使う」の2通りに表す（三角形の面積 $=\dfrac12\times$2辺$\times\sin$ 間の角）。すると $\dfrac{x^2}{y^2}=\dfrac{AX\cdot XD}{CY\cdot YB}$ となり，右辺は方べきの定理で $x,\ y$ と $PM$ だけで表せる。",
  "sol": r"$PM=MQ=m,\ MX=x,\ MY=y$ とする。$X,\ Y$ は弦 $PQ$ 上で，$M$ に関して互いに反対側にある（図）。<br>"
         r"【角の関係】対頂角より $\angle AMX=\angle BMY,\ \angle DMX=\angle CMY$。円周角の定理より<br>"
         r"$\angle MAX=\angle BAD=\angle BCD=\angle MCY$，　$\angle MDX=\angle CDA=\angle CBA=\angle MBY$<br>"
         r"【面積比を2通りに表す】$k=\dfrac{\triangle AMX\cdot\triangle DMX}{\triangle CMY\cdot\triangle BMY}$ とおく。$M$ における角を使うと<br>"
         r"$k=\dfrac{\frac12MA\cdot x\sin\angle AMX\cdot\frac12MD\cdot x\sin\angle DMX}{\frac12MC\cdot y\sin\angle CMY\cdot\frac12MB\cdot y\sin\angle BMY}=\dfrac{MA\cdot MD\cdot x^2}{MC\cdot MB\cdot y^2}$<br>"
         r"$A,\ D,\ C,\ B$ における角を使うと<br>"
         r"$k=\dfrac{\frac12AM\cdot AX\sin\angle MAX\cdot\frac12DM\cdot DX\sin\angle MDX}{\frac12CM\cdot CY\sin\angle MCY\cdot\frac12BM\cdot BY\sin\angle MBY}=\dfrac{AM\cdot AX\cdot DM\cdot DX}{CM\cdot CY\cdot BM\cdot BY}$<br>"
         r"2式を比べて　$\dfrac{x^2}{y^2}=\dfrac{AX\cdot XD}{CY\cdot YB}$　…①<br>"
         r"【方べき】弦 $AD$ と $PQ$ は $X$ で交わるので $AX\cdot XD=PX\cdot XQ=(m-x)(m+x)=m^2-x^2$。同様に $CY\cdot YB=m^2-y^2$。<br>"
         r"① に代入すると $x^2(m^2-y^2)=y^2(m^2-x^2)$，すなわち $m^2x^2=m^2y^2$。$x,\ y>0$ より $x=y$。よって　$MX=MY$　（終）",
  "note": r"「面積比を2通りに表して比をつくる」のは，線分の比が絡む証明で強力な手法である。$M$ が弦 $PQ$ の中点でない場合にも，同様の計算で $MX,\ MY$ の関係式が得られる（練習）。",
  "ex": r"例題で，$M$ が弦 $PQ$ の中点とは限らず $PM=p,\ MQ=q$ であるとする。$X$ が線分 $PM$ 上，$Y$ が線分 $MQ$ 上にあるとき，$\dfrac1{MX}-\dfrac1{MY}=\dfrac1p-\dfrac1q$ を証明せよ。",
  "exa": r"例題と同様に $\dfrac{x^2}{y^2}=\dfrac{PX\cdot XQ}{PY\cdot YQ}=\dfrac{(p-x)(q+x)}{(p+y)(q-y)}$。整理すると $(x+y)\{pq(x-y)-(p-q)xy\}=0$ で，$pq(x-y)=(p-q)xy$ の両辺を $pqxy$ で割る。"},
]})


# ================================================================ 節6 図
def _c61(m=2, n=3):
    A, B = (0.0, 0.0), (5.0, 0.0); v = onc((0, 0), 1, 65)
    C = mul(v, m); D = add(B, mul(v, n)); D2 = sub(B, mul(v, n))
    return A, B, C, D, D2, inter(C, D2, A, B), inter(C, D, A, B)
def _f61():
    A, B, C, D, D2, Pp, Q = _c61()
    F = Fig([Q, B, D, D2, lerp(A, C, 1.6)], w=250, h=95)
    F.seg(lerp(Q, B, -.03), lerp(Q, B, 1.05)); F.seg(lerp(A, C, -1.2), lerp(A, C, 1.6), wd=.8); F.seg(lerp(B, D, -1.15), lerp(B, D, 1.15), wd=.8)
    F.seg(C, D2, col="#c0392b"); F.seg(Q, D, col="#c0392b")
    for p in (A, B, C, D, D2, Pp, Q): F.dot(p, 1.5)
    F.lab(A, "A", -3, 8); F.lab(B, "B", 7, 7); F.lab(C, "C", -8, -2); F.lab(D, "D", 8, 0); F.lab(D2, "D′", 9, 0); F.lab(Pp, "P", 3, -8); F.lab(Q, "Q", 0, 8)
    F.lab(lerp(A, C, 1.6), "ℓ", -7, 2, 11); F.lab(lerp(B, D, 1.15), "m", -12, 4, 11)
    return F.svg()
def _f62():
    O = (0.0, 0.0); a, b = 2.0, 1.5; u, w = (1.0, 0.0), onc(O, 1, 38)
    E, A = mul(u, 1), mul(u, a); B = mul(w, b); C = inter(A, add(A, sub(B, E)), O, w)
    F1 = Fig([O, mul(u, 3.6), mul(w, 3.4)], w=120, h=95, pad=15)
    F1.seg(O, mul(u, 3.6)); F1.seg(O, mul(w, 3.4)); F1.seg(E, B, wd=.9); F1.seg(A, C, col="#c0392b")
    for p in (E, A, B, C): F1.dot(p, 1.5)
    F1.lab(O, "O", -6, 6); F1.lab(E, "E", 0, 9); F1.lab(A, "A", 0, 9); F1.lab(B, "B", -7, -4); F1.lab(C, "C", -7, -4)
    a = 3.0; A2, B2, C2 = (0.0, 0.0), (a, 0.0), (a + 1, 0.0); Oc = ((a + 1) / 2, 0.0); D = (a, math.sqrt(a))
    F2 = Fig([A2, C2, (Oc[0], Oc[1] + (a + 1) / 2)], w=120, h=95, pad=15)
    F2.arc(Oc, (a + 1) / 2, 0, 180); F2.seg(A2, C2); F2.seg(B2, D, col="#c0392b"); F2.seg(A2, D, wd=.8); F2.seg(D, C2, wd=.8); F2.ra(B2, C2, D, 4)
    F2.lab(A2, "A", -2, 9); F2.lab(B2, "B", 0, 9); F2.lab(C2, "C", 2, 9); F2.lab(D, "D", 0, -8)
    F2.lab(lerp(A2, B2, .5), "a", 0, 8, 10); F2.lab(lerp(B2, C2, .5), "1", 0, 8, 10)
    return hcat([F1, F2], 10, ["(1)", "(2)"])
def _c63():
    A, B, C = (1.3, 3.0), (0.0, 0.0), (4.4, 0.0)
    S1 = lerp(B, A, 0.32); P1 = foot(S1, B, C); s1 = S1[1]; Q1 = add(P1, (s1, 0)); R1 = add(Q1, (0, s1))
    R = inter(B, R1, A, C); S = inter(R, add(R, (1, 0)), A, B); Pp, Q = foot(S, B, C), foot(R, B, C)
    return A, B, C, P1, Q1, R1, S1, Pp, Q, R, S
def _f63():
    A, B, C, P1, Q1, R1, S1, Pp, Q, R, S = _c63()
    F = Fig([A, B, C], w=160, h=115)
    F.poly([Pp, Q, R, S], fill=SH, col="#c0392b", wd=1.2); F.poly([A, B, C]); F.poly([P1, Q1, R1, S1], dash=True); F.seg(B, R, wd=.8, dash=True)
    F.labs({"A": A, "B": B, "C": C}, cent(A, B, C)); F.lab(Pp, "P", 0, 9); F.lab(Q, "Q", 0, 9); F.lab(R, "R", 7, -2); F.lab(S, "S", -7, -2)
    F.lab(R1, "R′", 2, -8, 10); F.lab(S1, "S′", -9, 0, 10)
    return F.svg()
def _c64(c=5.0, a=8.0, Bdeg=60.0):
    B, C = (0.0, 0.0), (a, 0.0); A = onc(B, c, Bdeg); D = rot(C, B, -60)
    G = cent(B, C, D); R = dist(G, B); Pp = line_circ(A, D, G, R)[0]
    return A, B, C, D, G, R, Pp
def _f64():
    A, B, C, D, G, R, Pp = _c64()
    F = Fig([A, B, C, D, (G[0] - R, G[1]), (G[0] + R, G[1])], w=140, h=170)
    F.circ(G, R, wd=.7, col="#2a55b0"); F.poly([A, B, C]); F.poly([B, C, D], dash=True); F.seg(A, D)
    F.seg(Pp, B, col="#c0392b"); F.seg(Pp, C, col="#c0392b"); F.dot(Pp)
    F.lab(A, "A", 0, -8); F.lab(B, "B", -7, -4); F.lab(C, "C", 7, -4); F.lab(D, "D", 0, 9); F.lab(Pp, "P", -8, -3)
    F.lab(onc(G, R, 200), "Γ", -8, 0, 12)
    return F.svg()

# ---------------------------------------------------------------- 節6
SEC.append({"title": "作図",
"base": r"""・作図：定規（2点を通る直線をひく）とコンパス（円をかく）だけを有限回用いて図形をかくこと<br>
・基本の作図：線分の垂直二等分線，角の二等分線，垂線，平行線，与えられた角に等しい角<br>
・長さ $1,\ a,\ b$ が与えられると，$a+b,\ a-b,\ ab,\ \dfrac ab,\ \sqrt a$ の長さが作図できる（平行線と線分の比，直角三角形の相似）<br>
・作図問題の答案は【作図】（手順）と【証明】（その図形が条件を満たす理由）の2つを書く""",
"items": [
 {"lv": 1, "title": "線分の内分点・外分点の作図",
  "q": r"線分 $AB$ を $2:3$ に内分する点 $P$ と，$2:3$ に外分する点 $Q$ を作図せよ。また，その作図が正しいことを証明せよ。",
  "hint": r"平行線と線分の比を利用する。$A,\ B$ を通る平行な2直線をひき，その上に長さの比が $2:3$ となる点をとる。2点を直線 $AB$ に関して同じ側にとれば外分点，反対側にとれば内分点が得られる（三角形の相似）。",
  "sol": r"【作図】① 点 $A$ を通る直線 $\ell$（直線 $AB$ と異なる）をひき，点 $B$ を通り $\ell$ に平行な直線 $m$ をひく。<br>"
         r"② 適当な長さ $e$ をとり，$\ell$ 上に $AC=2e$ となる点 $C$ をとる。$m$ 上に，直線 $AB$ に関して $C$ と同じ側に $BD=3e$，反対側に $BD'=3e$ となる点 $D,\ D'$ をコンパスでとる。<br>"
         r"③ 直線 $CD'$ と線分 $AB$ の交点が $P$，直線 $CD$ と直線 $AB$ の交点が $Q$ である（$AC\neq BD$ なので $CD$ は $AB$ と平行でない）。<br>" + _f61() +
         r"【証明】$AC\parallel BD'$ より $\triangle PAC\backsim\triangle PBD'$ であるから　$AP:PB=AC:BD'=2:3$<br>"
         r"$P$ は線分 $AB$ 上にあるので，$P$ は $AB$ を $2:3$ に内分する。<br>"
         r"同様に $AC\parallel BD$ より $\triangle QAC\backsim\triangle QBD$ で　$QA:QB=AC:BD=2:3$<br>"
         r"$Q$ は線分 $AB$ の外（$A$ の側の延長上）にあるので，$Q$ は $AB$ を $2:3$ に外分する。　（終）",
  "note": r"平行線は「同位角が等しい角をつくる」作図などでひける。$A$ から半直線をひいて等間隔に5点 $A_1,\ \cdots,\ A_5$ をとり，$A_5B$ に平行な直線を $A_2$ を通してひいても内分点が得られる。",
  "ex": r"線分 $AB$ を $3:1$ に内分する点と，$3:1$ に外分する点を作図する方法を述べよ。",
  "exa": r"例題と同様に $AC=3e,\ BD=BD'=e$ をとる（$D$ は $C$ と同じ側，$D'$ は反対側）。$CD'$ と $AB$ の交点が内分点，直線 $CD$ と直線 $AB$ の交点（$B$ の側の延長上）が外分点。"},
 {"lv": 2, "title": r"長さ $ab$，$\sqrt a$ の線分の作図",
  "q": r"長さ $1$ の線分と，長さ $a,\ b$ の線分が与えられている。<br>(1) 長さ $ab$ の線分を作図せよ。<br>(2) 長さ $\sqrt a$ の線分を作図せよ。<br>いずれも作図の方法を述べ，それが正しいことを証明せよ。",
  "hint": r"(1) 平行線と線分の比で「$1:a=b:x$」をつくる。(2) 直径の両端と円周上の点を結ぶと直角三角形ができ，直角の頂点から斜辺に下ろした垂線の長さ $h$ について $h^2=$（斜辺を分けた2つの長さの積）。",
  "sol": _f62() + r"(1) 【作図】点 $O$ から2本の半直線 $\ell_1,\ \ell_2$ をひく。$\ell_1$ 上に $OE=1,\ OA=a$，$\ell_2$ 上に $OB=b$ となる点をとる。$A$ を通り直線 $EB$ に平行な直線と $\ell_2$ の交点を $C$ とすると，$OC$ が求める線分である。<br>"
         r"【証明】$EB\parallel AC$ より $OE:OA=OB:OC$，すなわち $1:a=b:OC$。よって $OC=ab$。<br>"
         r"(2) 【作図】直線上に $AB=a,\ BC=1$ となるように点 $A,\ B,\ C$ をこの順にとり，$AC$ を直径とする円をかく。$B$ を通り $AC$ に垂直な直線と円の交点の1つを $D$ とすると，$BD$ が求める線分である。<br>"
         r"【証明】$AC$ は直径だから $\angle ADC=90^\circ$。$\triangle ABD$ と $\triangle DBC$ において，$\angle ABD=\angle DBC=90^\circ$，$\angle BAD=90^\circ-\angle ADB=\angle BDC$ より $\triangle ABD\backsim\triangle DBC$。<br>"
         r"よって $AB:BD=DB:BC$，$BD^2=AB\cdot BC=a$。ゆえに $BD=\sqrt a$。",
  "note": r"(2) は方べきの定理（$D$ と反対側の交点 $D'$ について $BD\cdot BD'=AB\cdot BC$）からもわかる。和・差・積・商・平方根が作図できるので，整数から出発して四則と平方根を有限回用いて表される長さはすべて作図できる。",
  "ex": r"長さ $1,\ a,\ b$ の線分が与えられたとき，長さ $\dfrac ab$ と $\sqrt{ab}$ の線分を作図する方法を述べよ。",
  "exa": r"$\dfrac ab$：$\ell_1$ 上に $OE=1,\ OB=b$，$\ell_2$ 上に $OA=a$ をとり，$E$ を通り $BA$ に平行な直線と $\ell_2$ の交点を $C$ とすると $OC=\dfrac ab$。$\sqrt{ab}$：例題 (2) で $AB=a,\ BC=b$ とする。"},
 {"lv": 3, "title": "三角形に内接する正方形の作図（相似の利用）",
  "q": r"$\angle B,\ \angle C$ がともに鋭角である $\triangle ABC$ がある。辺 $BC$ 上に2頂点 $P,\ Q$ をもち，辺 $AB,\ AC$ 上にそれぞれ頂点 $S,\ R$ をもつ正方形 $PQRS$ を作図せよ。また，$BC=a$，頂点 $A$ と直線 $BC$ の距離を $h$ とするとき，正方形の1辺の長さを求めよ。",
  "hint": r"条件の一部（$S$ が $AB$ 上，$P,\ Q$ が $BC$ 上）だけを満たす小さな正方形をまずかき，$B$ を中心に拡大して残りの条件（$R$ が $AC$ 上）を満たすようにする（相似の利用）。",
  "sol": _f63() + r"【作図】① 辺 $AB$ 上に適当な点 $S'$ をとり，$S'$ から $BC$ に垂線 $S'P'$ を下ろす。<br>"
         r"② $P'S'$ を1辺とする正方形 $P'Q'R'S'$ を，$Q'$ が直線 $BC$ 上で $P'$ より $C$ の側になるようにかく。<br>"
         r"③ 直線 $BR'$ と辺 $AC$ の交点を $R$ とし，$R$ を通り $BC$ に平行な直線と辺 $AB$ の交点を $S$ とする。$R,\ S$ から $BC$ に下ろした垂線の足を $Q,\ P$ とすると，$PQRS$ が求める正方形である。<br>"
         r"【証明】$SR\parallel S'R'$ より $\triangle BSR\backsim\triangle BS'R'$，$RQ\parallel R'Q'$ より $\triangle BRQ\backsim\triangle BR'Q'$ であるから　$\dfrac{SR}{S'R'}=\dfrac{BR}{BR'}=\dfrac{RQ}{R'Q'}$<br>"
         r"$S'R'=R'Q'$ より $SR=RQ$。四角形 $PQRS$ は $SP\perp BC,\ RQ\perp BC,\ SR\parallel BC$ より長方形で，$SR=RQ$ だから正方形である。また $\angle B,\ \angle C$ が鋭角なので，$P,\ Q$ は辺 $BC$ 上にある。<br>"
         r"【1辺の長さ】1辺を $x$ とする。$SR\parallel BC$ より $\triangle ASR\backsim\triangle ABC$ で，相似比は高さの比 $(h-x):h$。よって $\dfrac xa=\dfrac{h-x}h$，$x(a+h)=ah$。ゆえに　$x=\boldsymbol{\dfrac{ah}{a+h}}$",
  "note": r"「条件の一部を満たす図形をかき，相似の中心から拡大・縮小して残りの条件を満たす」方法を相似法という。$x=\dfrac{ah}{a+h}$ は $\dfrac1x=\dfrac1a+\dfrac1h$ とも書ける。",
  "ex": r"$\angle A=90^\circ,\ AB=3,\ AC=4$ の直角三角形 $ABC$ において，斜辺 $BC$ 上に2頂点をもち，残りの2頂点がそれぞれ辺 $AB,\ AC$ 上にある正方形の1辺の長さを求めよ。",
  "exa": r"$\dfrac{60}{37}$"},
 {"lv": 5, "title": "3頂点への距離の和の最小（フェルマー点）",
  "q": r"鋭角三角形 $ABC$ の内部の点 $P$ に対して $!L=PA+PB+PC$ とおく。辺 $BC$ を1辺とする正三角形 $BCD$ を $\triangle ABC$ の外側にかく。<br>"
       r"(1) $!L\geqq AD$ であることを証明せよ。<br>"
       r"(2) $!L=AD$ となる点 $P$ が $\triangle ABC$ の内部に存在することを示し，その点の作図の方法を述べよ。<br>"
       r"(3) $AB=5,\ BC=8,\ CA=7$ のとき，$!L$ の最小値を求めよ。",
  "hint": r"(1) $B$ を中心に $\triangle BPC$ を $60^\circ$ 回転して $\triangle BP'D$ に重ねると，$PB=PP'$，$PC=P'D$ となり，$!L$ は折れ線 $APP'D$ の長さになる。(2) 正三角形 $BCD$ の外接円と線分 $AD$ の交点をとり，トレミーの定理で $PB+PC=PD$ を示す。",
  "sol": _f64() + r"(1) $C$ が $D$ に移る向きに $B$ を中心として $60^\circ$ 回転する移動で，$P$ が移る点を $P'$ とする。$\triangle BPC$ は $\triangle BP'D$ に移るから $P'D=PC$。また $BP=BP',\ \angle PBP'=60^\circ$ より $\triangle BPP'$ は正三角形で $PP'=PB$。よって<br>"
         r"$!L=AP+PP'+P'D\geqq AD$（折れ線 $APP'D$ の長さは線分 $AD$ の長さ以上）　（終）<br>"
         r"(2) $\angle ABD=\angle B+60^\circ<180^\circ$，$\angle ACD=\angle C+60^\circ<180^\circ$ であるから四角形 $ABDC$ は凸であり，対角線 $AD$ は辺 $BC$ と点 $K$（$B,\ C$ と異なる）で交わる。<br>"
         r"$\triangle BCD$ の外接円を $\Gamma$ とする。$\Gamma$ の弧 $BC$ のうち $D$ を含まない側の点 $X$ では $\angle BXC=180^\circ-60^\circ=120^\circ$ であり，直線 $BC$ に関して $A$ と同じ側で $\Gamma$ の内部にある点 $Y$ では $\angle BYC>120^\circ$ である。"
         r"$\angle BAC<90^\circ$ だから $A$ は $\Gamma$ の外部にあり，$K$ は弦 $BC$ 上の点だから $\Gamma$ の内部にある。よって線分 $AK$ は $A$ と $K$ の間の点 $P$ で $\Gamma$ と交わり，$P$ は $\triangle ABC$ の内部にある。<br>"
         r"四角形 $PBDC$ は $\Gamma$ に内接するから，トレミーの定理より $PD\cdot BC=PB\cdot CD+PC\cdot BD$。$BC=CD=BD$ より $PD=PB+PC$。$P$ は線分 $AD$ 上にあるから<br>"
         r"$!L=PA+PB+PC=PA+PD=AD$<br>"
         r"【作図】$B,\ C$ を中心とする半径 $BC$ の円の交点（$A$ と反対側）を $D$ として正三角形 $BCD$ をかき，その外接円（中心は $\triangle BCD$ の重心）と線分 $AD$ の交点を $P$ とする。<br>"
         r"(3) (1)，(2) より $!L$ の最小値は $AD$ である。$\cos B=\dfrac{5^2+8^2-7^2}{2\cdot5\cdot8}=\dfrac12$ より $\angle B=60^\circ$，$\angle ABD=60^\circ+60^\circ=120^\circ$。$\triangle ABD$ に余弦定理を用いて<br>"
         r"$AD^2=5^2+8^2-2\cdot5\cdot8\cos120^\circ=25+64+40=129$　よって最小値は　$\boldsymbol{\sqrt{129}}$",
  "note": r"この $P$ は $\angle APB=\angle BPC=\angle CPA=120^\circ$ を満たす点で，フェルマー点とよばれる。他の2辺の外側にも正三角形 $CAE,\ ABF$ をかくと $AD=BE=CF$ で，3直線 $AD,\ BE,\ CF$ は $P$ で交わる。一般に最小値の2乗は $\dfrac{a^2+b^2+c^2}2+2\sqrt3\,!S$（$!S$ は面積）で，(3) では $69+60=129$。1つの角が $120^\circ$ 以上なら，最小となるのはその頂点である。",
  "ex": r"$AB=7,\ BC=8,\ \angle ABC=60^\circ$ の三角形 $ABC$ の内部の点 $P$ について，$PA+PB+PC$ の最小値を求めよ。",
  "exa": r"$13$（$\triangle ABC$ は鋭角三角形で，最小値は $\sqrt{7^2+8^2+7\cdot8}=13$）"},
]})


# ================================================================ 節7 図（空間図形は斜投影：x 右、y 奥、z 上）
def pj(p): return (p[0] + 0.42 * p[1], p[2] + 0.28 * p[1])
def _cube(a=1.0):
    n = dict(A=(0, 0, 0), B=(1, 0, 0), C=(1, 1, 0), D=(0, 1, 0), E=(0, 0, 1), F=(1, 0, 1), G=(1, 1, 1), H=(0, 1, 1))
    return {k: (v[0] * a, v[1] * a, v[2] * a) for k, v in n.items()}
_CE = ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"]
def _drawcube(F, V, col="#555", wd=.9):
    for e in _CE:
        F.seg(pj(V[e[0]]), pj(V[e[1]]), dash="D" in e, col=col, wd=wd)
_CL = dict(A=(-6, 7), B=(6, 7), C=(7, 2), D=(-7, -3), E=(-7, -2), F=(7, 5), G=(6, -6), H=(-6, -6))
def _f73():
    O, A, B, C = (0, 0, 0), (0, -2, 0), (2, 0, 0), (0, 0, 1)
    n = _cr3(_sb3(B, A), _sb3(C, A)); t = _dt3(_sb3(O, A), n) / _dt3(n, n)
    H = (O[0] - n[0] * t, O[1] - n[1] * t, O[2] - n[2] * t)
    F = Fig([pj(p) for p in (O, A, B, C)], w=175, h=125)
    F.seg(pj(O), pj(A), dash=True); F.seg(pj(O), pj(B), dash=True); F.seg(pj(O), pj(C), dash=True)
    F.poly([pj(A), pj(B), pj(C)]); F.seg(pj(O), pj(H), dash=True, col="#c0392b"); F.dot(pj(H), 1.5)
    F.lab(pj(O), "O", 4, -8); F.lab(pj(A), "A", -7, 4); F.lab(pj(B), "B", 7, 3); F.lab(pj(C), "C", 0, -8); F.lab(pj(H), "H", 8, 2)
    return F.svg()
def _f74():
    V = _cube(); c = (.5, .5, .5)
    fc = [(.5, .5, 0), (.5, .5, 1), (0, .5, .5), (1, .5, .5), (.5, 0, .5), (.5, 1, .5)]
    F = Fig([pj(v) for v in V.values()], w=140, h=125)
    _drawcube(F, V)
    eq = [fc[4], fc[3], fc[5], fc[2]]
    for i in range(4):
        hid = eq[i] == fc[5] or eq[(i + 1) % 4] == fc[5]     # 奥の面の中心を含む辺は見えない
        F.seg(pj(eq[i]), pj(eq[(i + 1) % 4]), col="#c0392b", wd=1.1, dash=hid)
        F.seg(pj(eq[i]), pj(fc[0]), col="#c0392b", wd=1.1, dash=eq[i] == fc[5]); F.seg(pj(eq[i]), pj(fc[1]), col="#c0392b", wd=1.1, dash=eq[i] == fc[5])
    for k, v in V.items(): F.lab(pj(v), k, *_CL[k])
    return F.svg()
def _c75(p2=33, q2=16, r2=48):
    p, q, r = math.sqrt(p2), math.sqrt(q2), math.sqrt(r2)
    return p, q, r, (0, 0, 0), (p, q, 0), (0, q, r), (p, 0, r)
def _f75():
    p, q, r, O, X, Y, Z = _c75()
    V = {k: (v[0] * p, v[1] * q, v[2] * r) for k, v in _cube().items()}
    F = Fig([pj(v) for v in V.values()], w=150, h=150)
    _drawcube(F, V, col="#888", wd=.8)
    for s_, t_ in ((O, X), (O, Y), (O, Z), (X, Y), (Y, Z), (Z, X)):
        F.seg(pj(s_), pj(t_), col="#c0392b", wd=1.3, dash=(s_, t_) in ((O, X), (O, Y), (X, Y)))
    F.lab(pj(O), "O", -6, 7); F.lab(pj(X), "X", 7, 3); F.lab(pj(Y), "Y", -6, -6); F.lab(pj(Z), "Z", 6, -6)
    F.lab(pj((p / 2, 0, 0)), "p", 0, 8, 10); F.lab(pj((p, q / 2, 0)), "q", 7, 4, 10); F.lab(pj((p, 0, r / 2)), "r", 7, 0, 10)
    return F.svg()
def _f76():
    V = _cube(); hx = [(1, .5, 0), (1, 0, .5), (.5, 0, 1), (0, .5, 1), (0, 1, .5), (.5, 1, 0)]
    F = Fig([pj(v) for v in V.values()], w=140, h=125)
    F.poly([pj(p) for p in hx], fill=SH, col="#c0392b", wd=1.1)
    _drawcube(F, V); F.seg(pj(V["A"]), pj(V["G"]), dash=True, col="#2a55b0")
    for k, v in V.items(): F.lab(pj(v), k, *_CL[k])
    return F.svg()
def _sb3(p, q): return (p[0] - q[0], p[1] - q[1], p[2] - q[2])
def _dt3(p, q): return p[0] * q[0] + p[1] * q[1] + p[2] * q[2]
def _cr3(p, q): return (p[1] * q[2] - p[2] * q[1], p[2] * q[0] - p[0] * q[2], p[0] * q[1] - p[1] * q[0])
def _d3(p, q): return math.sqrt(_dt3(_sb3(p, q), _sb3(p, q)))
def _vol(a, b, c, d): return abs(_dt3(_sb3(b, a), _cr3(_sb3(c, a), _sb3(d, a)))) / 6

_T72 = (r"<table><tr><th>正多面体</th><th>面の形</th><th>$m$</th><th>$v$</th><th>$e$</th><th>$f$</th></tr>"
        r"<tr><td>正四面体</td><td>正三角形</td><td>3</td><td>4</td><td>6</td><td>4</td></tr>"
        r"<tr><td>正六面体</td><td>正方形</td><td>3</td><td>8</td><td>12</td><td>6</td></tr>"
        r"<tr><td>正八面体</td><td>正三角形</td><td>4</td><td>6</td><td>12</td><td>8</td></tr>"
        r"<tr><td>正十二面体</td><td>正五角形</td><td>3</td><td>20</td><td>30</td><td>12</td></tr>"
        r"<tr><td>正二十面体</td><td>正三角形</td><td>5</td><td>12</td><td>30</td><td>20</td></tr></table>")

# ---------------------------------------------------------------- 節7
SEC.append({"title": "空間図形と多面体",
"base": r"""・直線と平面の垂直：直線 $\ell$ が平面 $\alpha$ 上の交わる2直線に垂直ならば $\ell\perp\alpha$ で，$\ell$ は $\alpha$ 上のすべての直線に垂直<br>
・三垂線の定理：平面 $\alpha$ 上にない点 $P$ から $\alpha$ に下ろした垂線の足を $H$，$\alpha$ 上の直線 $m$ 上の点を $Q$ とするとき，$HQ\perp m$ ならば $PQ\perp m$<br>
・オイラーの多面体定理：凸多面体の頂点の数 $v$，辺の数 $e$，面の数 $f$ について $v-e+f=2$<br>
・数え上げ：（各面の辺の数の和）$=2e$，（各頂点に集まる辺の数の和）$=2e$<br>
・正多面体：すべての面が合同な正多角形で，各頂点に集まる面の数が等しい凸多面体""",
"items": [
 {"lv": 1, "title": "オイラーの多面体定理と頂点・辺・対角線の数",
  "q": r"正五角形の面 $12$ 個と正六角形の面 $20$ 個からなり，各頂点に $3$ つの面が集まる凸多面体（サッカーボール型の多面体）がある。<br>"
       r"(1) 頂点の数 $v$，辺の数 $e$，面の数 $f$ を求め，$v-e+f=2$ が成り立つことを確かめよ。<br>"
       r"(2) 同じ面上にない2頂点を結ぶ線分（対角線）は何本あるか。",
  "hint": r"各面の辺を数え上げると，1本の辺は2つの面に共有されるので2回ずつ数えられる。頂点は3つの面に共有されるので3回ずつ数えられる。(2) は「2頂点の選び方」から「辺」と「面の対角線」を引く。",
  "sol": r"(1) $f=12+20=\boldsymbol{32}$。各面の辺の数の和は $5\cdot12+6\cdot20=180$ で，各辺は2つの面に共有されるから $e=\dfrac{180}2=\boldsymbol{90}$。"
         r"各面の頂点の数の和も $180$ で，各頂点は3つの面に共有されるから $v=\dfrac{180}3=\boldsymbol{60}$。<br>"
         r"$v-e+f=60-90+32=2$ となり，確かに成り立つ。<br>"
         r"(2) 2頂点の選び方は ${}_{60}\mathrm{C}_2=1770$ 通り。このうち辺は $90$ 本。同じ面上にあって辺でないもの（面の対角線）は，正五角形1つに $5$ 本，正六角形1つに ${}_6\mathrm{C}_2-6=9$ 本あるから $5\cdot12+9\cdot20=240$ 本。<br>"
         r"よって対角線は　$1770-90-240=\boldsymbol{1440}$ <b>本</b>",
  "note": r"凸多面体の異なる2つの面が共有するのは高々1本の辺だから，面の対角線は重複して数えていない。この多面体は正二十面体の各頂点を切り落としたもの（切頂二十面体）で，炭素原子 $60$ 個からなる分子の形としても知られる。",
  "ex": r"正方形の面 $6$ 個と正六角形の面 $8$ 個からなり，各頂点に $3$ つの面が集まる凸多面体について，頂点・辺・面の数と対角線の本数を求めよ。",
  "exa": r"$v=24,\ e=36,\ f=14$，対角線は $276-36-84=156$ 本"},
 {"lv": 2, "title": "正多面体は5種類しかない",
  "q": r"正多面体は5種類しかないことを，次の方針で証明せよ。また，それぞれの頂点・辺・面の数を求めよ。<br>"
       r"方針：各面を正 $n$ 角形，各頂点に集まる面の数を $m$ とすると，1つの頂点に集まる角の和は $360^\circ$ より小さい。",
  "hint": r"正 $n$ 角形の1つの内角は $\dfrac{180^\circ(n-2)}n$。条件 $m\cdot\dfrac{180^\circ(n-2)}n<360^\circ$ を $(m-2)(n-2)<4$ と変形すると，整数の組が絞れる。頂点・辺・面の数は $nf=2e,\ mv=2e$ とオイラーの多面体定理から求める。",
  "sol": r"各頂点には3つ以上の面が集まるから $m\geqq3$，また $n\geqq3$。1つの頂点に集まる角の和は $360^\circ$ より小さいから<br>"
         r"$m\cdot\dfrac{180^\circ(n-2)}n<360^\circ$　すなわち　$m(n-2)<2n$，$mn-2m-2n+4<4$，$(m-2)(n-2)<4$<br>"
         r"$m-2\geqq1,\ n-2\geqq1$ の整数で積が $4$ 未満となるのは $(m-2,\ n-2)=(1,\ 1),\ (1,\ 2),\ (2,\ 1),\ (1,\ 3),\ (3,\ 1)$<br>"
         r"すなわち $(n,\ m)=(3,\ 3),\ (4,\ 3),\ (3,\ 4),\ (5,\ 3),\ (3,\ 5)$ の5通りしかない。それぞれ正四面体，正六面体，正八面体，正十二面体，正二十面体として実際に存在するから，正多面体は<b>5種類</b>である。<br>"
         r"頂点・辺・面の数を $v,\ e,\ f$ とすると，$nf=2e,\ mv=2e$ と $v-e+f=2$ より $\dfrac{2e}m-e+\dfrac{2e}n=2$，$e=\dfrac{2mn}{2m+2n-mn}$。これから次の表を得る。" + _T72,
  "note": r"角の和が $360^\circ$ 未満であることは，頂点のまわりの面を切り開いて平面に広げると隙間ができることからわかる（ちょうど $360^\circ$ なら平らになってしまう）。条件 $(m-2)(n-2)<4$ は $\dfrac1m+\dfrac1n>\dfrac12$ と同値で，オイラーの多面体定理から $e>0$ として導くこともできる。",
  "ex": r"各頂点に正三角形2個と正方形2個が（交互に）集まる凸多面体がある。頂点・辺・面の数を求めよ。",
  "exa": r"$v=12,\ e=24,\ f=14$（正三角形 $8$ 個，正方形 $6$ 個）"},
 {"lv": 2, "title": "直線と平面の垂直（三垂線の定理）",
  "q": r"四面体 $OABC$ において，$OA,\ OB,\ OC$ はどの2つも互いに垂直である。$O$ から平面 $ABC$ に下ろした垂線を $OH$ とする。<br>"
       r"(1) $H$ は $\triangle ABC$ の垂心であることを証明せよ。<br>(2) $OA=OB=2,\ OC=1$ のとき，$OH$ の長さを求めよ。" + _f73(),
  "hint": r"(1) $OA$ は平面 $OBC$ 上の交わる2直線 $OB,\ OC$ に垂直なので $OA\perp BC$。$OH\perp BC$ と合わせて $BC\perp$ 平面 $OAH$。(2) 四面体の体積を2通り（底面 $\triangle OAB$ と底面 $\triangle ABC$）に表す。",
  "sol": r"(1) $OA\perp OB,\ OA\perp OC$ より，$OA$ は平面 $OBC$ に垂直で $OA\perp BC$。また $OH\perp$ 平面 $ABC$ より $OH\perp BC$。<br>"
         r"$OA$ と $OH$ は点 $O$ で交わる2直線だから，$BC$ は平面 $OAH$ に垂直であり，その平面上の直線 $AH$ について $AH\perp BC$。<br>"
         r"同様に $BH\perp CA$。よって $H$ は $\triangle ABC$ の2本の垂線の交点，すなわち垂心である。　（終）<br>"
         r"(2) 四面体の体積は　$!V=\dfrac13\cdot\triangle OAB\cdot OC=\dfrac13\cdot\dfrac12\cdot2\cdot2\cdot1=\dfrac23$<br>"
         r"$AB=2\sqrt2,\ CA=CB=\sqrt5$ で，$AB$ の中点 $M$ について $CM=\sqrt{5-2}=\sqrt3$ だから　$\triangle ABC=\dfrac12\cdot2\sqrt2\cdot\sqrt3=\sqrt6$<br>"
         r"$!V=\dfrac13\cdot\triangle ABC\cdot OH$ より　$OH=\dfrac{3!V}{\sqrt6}=\dfrac2{\sqrt6}=\boldsymbol{\dfrac{\sqrt6}3}$",
  "note": r"(1) の後半の議論は三垂線の定理そのものである。(2) は一般に $\dfrac1{OH^2}=\dfrac1{OA^2}+\dfrac1{OB^2}+\dfrac1{OC^2}$ が成り立つ（$\dfrac14+\dfrac14+1=\dfrac32$）。直角三角形の斜辺に下ろした垂線 $h$ についての $\dfrac1{h^2}=\dfrac1{a^2}+\dfrac1{b^2}$ の空間版である。",
  "ex": r"(1) 正四面体 $ABCD$ において $AB\perp CD$ であることを証明せよ。<br>"
        r"(2) 四面体 $OABC$ で $OA,\ OB,\ OC$ がどの2つも垂直で $OA=OB=OC=3$ のとき，$O$ から平面 $ABC$ に下ろした垂線の長さを求めよ。",
  "exa": r"(1) $CD$ の中点 $M$ について $AM\perp CD,\ BM\perp CD$ より $CD\perp$ 平面 $ABM$，よって $AB\perp CD$。(2) $\sqrt3$"},
 {"lv": 3, "title": "立方体の中の正多面体と頂点の切り落とし",
  "q": r"1辺の長さが $a$ の立方体 $ABCD$-$EFGH$ について，次の問いに答えよ。<br>"
       r"(1) 6つの面の中心（対角線の交点）を頂点とする正八面体の，1辺の長さと体積を求めよ。<br>"
       r"(2) 4点 $A,\ C,\ F,\ H$ を頂点とする正四面体の体積を求めよ。<br>"
       r"(3) 立方体の各頂点を，その頂点に集まる3辺の中点を通る平面で切り落としてできる多面体の，頂点・辺・面の数と体積を求めよ。" + _f74(),
  "hint": r"(1) 正八面体は，立方体の中心を通る正方形を共通の底面とする2つの正四角錐に分けられる。(2)(3) 立方体から，隅の三角錐（直角をはさむ3辺が等しい）を切り取ったものとみる。三角錐の体積は $\dfrac13\times$（底面積）$\times$（高さ）。",
  "sol": r"(1) 隣り合う2面の中心を結ぶ線分は，直角をはさむ2辺が $\dfrac a2$ の直角二等辺三角形の斜辺だから，1辺の長さは　$\boldsymbol{\dfrac{\sqrt2}2a}$<br>"
         r"側面の4つの中心は，立方体の中心を通り底面に平行な平面上で，対角線の長さが $a$ の正方形（面積 $\dfrac{a^2}2$）をつくる。上下の面の中心はこの平面から $\dfrac a2$ 離れているから，体積は　$2\cdot\dfrac13\cdot\dfrac{a^2}2\cdot\dfrac a2=\boldsymbol{\dfrac{a^3}6}$<br>"
         r"(2) 正四面体 $ACFH$ は，立方体から4つの三角錐 $B$-$ACF$，$D$-$ACH$，$E$-$AFH$，$G$-$CFH$ を除いたもの。各三角錐は直角をはさむ3辺が $a$ で体積 $\dfrac13\cdot\dfrac{a^2}2\cdot a=\dfrac{a^3}6$ だから　$a^3-4\cdot\dfrac{a^3}6=\boldsymbol{\dfrac{a^3}3}$<br>"
         r"(3) 切り落とした後の頂点は，立方体の12本の辺の中点で $v=\boldsymbol{12}$。面は，もとの6つの面から残る正方形6個と，切り口の正三角形8個で $f=\boldsymbol{14}$。各頂点に4本の辺が集まるので $e=\dfrac{12\cdot4}2=\boldsymbol{24}$（$v-e+f=2$ も成り立つ）。<br>"
         r"切り落とす三角錐は直角をはさむ3辺が $\dfrac a2$ で，体積は $\dfrac13\cdot\dfrac12\left(\dfrac a2\right)^2\cdot\dfrac a2=\dfrac{a^3}{48}$。これを8個切り落とすから，体積は　$a^3-8\cdot\dfrac{a^3}{48}=\boldsymbol{\dfrac56a^3}$",
  "note": r"(1) の正八面体と立方体のように，一方の面の中心を結ぶと他方ができる2つの多面体を互いに双対という（正十二面体と正二十面体も双対）。(3) の多面体は立方八面体とよばれ，前の正多面体の例題の練習で扱った多面体である。",
  "ex": r"1辺の長さが $3$ の正四面体の各頂点を，その頂点から長さ $1$ の位置で3辺を切る平面で切り落とす。できる多面体の頂点・辺・面の数を求めよ。また，その体積はもとの正四面体の体積の何倍か。",
  "exa": r"$v=12,\ e=18,\ f=8$，$\dfrac{23}{27}$ 倍"},
 {"lv": 4, "title": "等面四面体の体積（直方体への埋め込み）",
  "q": r"4つの面がすべて，3辺の長さが $7,\ 8,\ 9$ の合同な三角形である四面体の体積を求めよ。",
  "hint": r"直方体の4つの頂点を，各面の対角線が辺になるように選ぶと，向かい合う辺の長さが等しい四面体ができる。3辺 $p,\ q,\ r$ の直方体で $p^2+q^2=49,\ q^2+r^2=64,\ r^2+p^2=81$ となるものを探す。",
  "sol": _f75() + r"【向かい合う辺は等しい】各面は長さ $7,\ 8,\ 9$ の辺を1本ずつもつ。4つの面の辺をのべで数えると長さ $7$ の辺は $4$ 回現れ，各辺は2つの面に共有されるので，長さ $7$ の辺は $2$ 本ある。"
         r"この2本が頂点を共有すると，その2本を含む面に長さ $7$ の辺が2本あることになり矛盾する。よって長さ $7$ の2辺は向かい合う（ねじれの位置にある）。$8,\ 9$ についても同様である。<br>"
         r"【直方体への埋め込み】$p^2+q^2=49,\ q^2+r^2=64,\ r^2+p^2=81$ を満たす正の数 $p,\ q,\ r$ を求めると，3式の和より $p^2+q^2+r^2=97$ で<br>"
         r"$p^2=33,\ q^2=16,\ r^2=48$，すなわち　$p=\sqrt{33},\ q=4,\ r=4\sqrt3$<br>"
         r"3辺が $p,\ q,\ r$ の直方体の1つの頂点 $O$ と，$O$ を含む3つの面それぞれで $O$ と対角線で結ばれる頂点 $X,\ Y,\ Z$ をとると，四面体 $OXYZ$ の6辺はすべて直方体の面の対角線で，向かい合う辺の長さが $7,\ 8,\ 9$ ずつ等しい。"
         r"四面体は6辺の長さで形が決まるから，求める四面体はこれと合同である。<br>"
         r"【体積】四面体 $OXYZ$ は，直方体から，直角をはさむ3辺が $p,\ q,\ r$ の三角錐（体積 $\dfrac16pqr$）を4つ切り取ったものだから<br>"
         r"$!V=pqr-4\cdot\dfrac16pqr=\dfrac13pqr=\dfrac13\cdot\sqrt{33}\cdot4\cdot4\sqrt3=\dfrac{48\sqrt{11}}3=\boldsymbol{16\sqrt{11}}$",
  "note": r"一般に，3辺が $a,\ b,\ c$ の三角形4つでできる四面体（等面四面体）の体積は $\sqrt{\dfrac{(a^2+b^2-c^2)(b^2+c^2-a^2)(c^2+a^2-b^2)}{72}}$。$p^2,\ q^2,\ r^2>0$ となる条件は面が鋭角三角形であることで，このときに限り等面四面体ができる。",
  "ex": r"4つの面がすべて，3辺の長さが $5,\ 6,\ 7$ の合同な三角形である四面体の体積を求めよ。",
  "exa": r"$2\sqrt{95}$"},
 {"lv": 4, "title": "立方体の断面積の最大",
  "q": r"1辺の長さが $1$ の立方体 $ABCD$-$EFGH$ を，対角線 $AG$ に垂直な平面 $\alpha$ で切る。断面積の最大値を求めよ。また，そのとき断面はどのような図形か。",
  "hint": r"$AG\perp$ 平面 $BDE$ であり，$\alpha$ は平面 $BDE$ に平行。$\alpha$ と直線 $AB,\ AD,\ AE$ の交点は $A$ から等距離 $t$ にある。$t\leqq1$ なら断面は正三角形，$1\leqq t\leqq\dfrac32$ なら正三角形から3つの隅の正三角形を除いた六角形になる。",
  "sol": _f76() + r"【$AG\perp$ 平面 $BDE$】$BD\perp AC,\ BD\perp CG$ より $BD\perp$ 平面 $ACGE$ で $BD\perp AG$。同様に $BE\perp AF,\ BE\perp FG$ より $BE\perp$ 平面 $AFGD$ で $BE\perp AG$。よって $AG\perp$ 平面 $BDE$ であり，$\alpha$ は平面 $BDE$ に平行である。<br>"
         r"【断面】$\alpha$ と直線 $AB,\ AD,\ AE$ の交点を $P,\ Q,\ R$ とすると，$\alpha\parallel$ 平面 $BDE$ より $AP=AQ=AR$ で，これを $t$ とおく（$0<t<3$）。立方体は中心に関して対称で，$\alpha$ を中心に関して対称移動しても $AG$ に垂直な平面になるから，$0<t\leqq\dfrac32$ で考えればよい。<br>"
         r"(i) $0<t\leqq1$ のとき　断面は1辺 $\sqrt2t$ の正三角形 $PQR$ で，面積は $\dfrac{\sqrt3}4(\sqrt2t)^2=\dfrac{\sqrt3}2t^2\leqq\dfrac{\sqrt3}2$<br>"
         r"(ii) $1\leqq t\leqq\dfrac32$ のとき　$P$ は辺 $AB$ の $B$ の側の延長上にある。面 $ABCD$ を含む平面で，$\angle BPQ=45^\circ$ より直線 $PQ$ は辺 $BC$ と $BS=BP=t-1$ となる点 $S$ で交わる。同様に $PR$ は辺 $BF$ と $BT=t-1$ となる点 $T$ で交わり，$PS=PT=ST=\sqrt2(t-1)$。"
         r"$\triangle PQR$ のうち立方体の外にあるのは，このような隅の正三角形 $\triangle PST$ と，$Q,\ R$ の側の同じ形の三角形の3つである（$t\leqq\dfrac32$ なので互いに重ならない）。よって断面積は<br>"
         r"$\dfrac{\sqrt3}2\{t^2-3(t-1)^2\}=\dfrac{\sqrt3}2(-2t^2+6t-3)=\dfrac{\sqrt3}2\left\{-2\left(t-\dfrac32\right)^2+\dfrac32\right\}$<br>"
         r"これは $t=\dfrac32$ で最大値 $\dfrac{3\sqrt3}4$ をとる。$\dfrac{3\sqrt3}4>\dfrac{\sqrt3}2$ であるから，求める最大値は　$\boldsymbol{\dfrac{3\sqrt3}4}$<br>"
         r"このとき $\alpha$ は $AG$ の中点（立方体の中心）を通り，$BS=BT=\dfrac12$ だから，断面は6本の辺 $BC,\ BF,\ FE,\ EH,\ HD,\ DC$ の中点を頂点とする<b>1辺 $\boldsymbol{\dfrac{\sqrt2}2}$ の正六角形</b>である。",
  "note": r"断面の形は，$t$ が $0$ から増えるにつれて 正三角形 → 六角形 → 正六角形（$t=\dfrac32$）→ 六角形 → 正三角形 と変化する。立方体の切断では，断面が通る辺の位置を，対称性を利用して1つの文字で表すのが基本である。",
  "ex": r"例題と同じ立方体を $AG$ に垂直な平面で切るとき，断面の周の長さの最大値を求めよ。",
  "exa": r"$3\sqrt2$（$1\leqq t\leqq2$ のとき周の長さは $3\sqrt2(2-t)+3\sqrt2(t-1)=3\sqrt2$ で一定，$t\leqq1$ では $3\sqrt2t\leqq3\sqrt2$）"},
]})


# ================================================================ 仕上げ（点の名前を立体に）
def _fix(s):
    def f(m):
        b = re.sub(r"(?<![\\A-Za-z!])([A-Z]+)", r"{\\mathrm{\1}}", m.group(1))
        return "$" + re.sub(r"!([A-Z])", r"\1", b) + "$"
    return re.sub(r"\$([^$]*)\$", f, s)
for _s in SEC:
    _s["base"] = _fix(_s["base"])
    for _it in _s["items"]:
        for _k in ("q", "hint", "sol", "note", "ex", "exa"):
            if _it.get(_k):
                _it[_k] = _fix(_it[_k])

CH = {"no": 7, "sections": SEC}


# ================================================================ 検算
def _rand_tri(rng):
    while True:
        A = (rng.uniform(-3, 3), rng.uniform(1, 5)); B = (rng.uniform(-4, -0.5), rng.uniform(-1, 0.5)); C = (rng.uniform(0.5, 4), rng.uniform(-1, 0.5))
        if area(A, B, C) > 1 and min(ang(B, A, C), ang(A, B, C), ang(A, C, B)) > 8:
            return A, B, C
def _in_tri(rng, A, B, C):
    u, v = rng.random(), rng.random()
    if u + v > 1: u, v = 1 - u, 1 - v
    return add(A, add(mul(sub(B, A), u), mul(sub(C, A), v)))

def v1():
    import sympy as sp
    rng = random.Random(1)
    # 1.1
    def bis(a, b, c):
        A, B, C = tri(a, b, c); D = lerp(B, C, c / (b + c)); I = incen(A, B, C)
        assert close(ang(B, A, D), ang(D, A, C))
        E = (a * c / (c - b), 0.0)                      # 外分点
        assert close(ang(D, A, E), 90) and close(dist(E, B) / dist(E, C), c / b)
        return dist(B, D), dist(B, E), dist(D, E), dist(A, I) / dist(I, D)
    r = bis(5, 4, 6); assert close(r[0], 3) and close(r[1], 15) and close(r[2], 12) and close(r[3], 2)
    r = bis(6, 3, 7); assert close(r[0], 21/5) and close(r[1], 21/2) and close(r[2], 63/10) and close(r[3], 5/3)
    # 1.2 内部の点の不等式
    for _ in range(3000):
        A, B, C = _rand_tri(rng); Pp = _in_tri(rng, A, B, C)
        assert dist(Pp, B) + dist(Pp, C) < dist(A, B) + dist(A, C)
        L = dist(Pp, A) + dist(Pp, B) + dist(Pp, C); per = dist(A, B) + dist(B, C) + dist(C, A)
        assert per / 2 < L < per and ang(B, Pp, C) > ang(B, A, C)
    # 1.3 中線定理
    A, B, C = tri(8, 5, 7); M = lerp(B, C, .5); assert close(dist(A, M) ** 2, 21)
    t = math.acos(26 / 70); Aq, Bq, Dq = (0, 0), (5, 0), (7 * math.cos(t), 7 * math.sin(t)); Cq = add(Bq, Dq)
    assert close(dist(Aq, Cq), 10) and close(dist(Bq, Dq), 4 * math.sqrt(3))
    # 1.4 二等分線の長さ
    for _ in range(500):
        A, B, C = _rand_tri(rng); a, b, c = dist(B, C), dist(C, A), dist(A, B)
        D = lerp(B, C, c / (b + c)); assert close(dist(A, D) ** 2, b * c - dist(B, D) * dist(D, C), 1e-7)
        X = lerp(B, C, rng.random()); m, n = dist(B, X), dist(X, C)   # スチュワート
        assert close(n * c * c + m * b * b, (m + n) * (dist(A, X) ** 2 + m * n), 1e-7)
    A, B, C = tri(5, 4, 6); assert close(dist(A, lerp(B, C, .6)) ** 2, 18)
    A, B, C = tri(7, 6, 8); assert close(dist(A, lerp(B, C, 8 / 14)), 6)
    # 1.5 シュタイナー・レームス
    a, b, c = sp.symbols("a b c", positive=True)
    BD2 = a*c*((a + c)**2 - b**2) / (a + c)**2; CE2 = a*b*((a + b)**2 - c**2) / (a + b)**2
    F = c*(a - b + c)*(a + b)**2 - b*(a + b - c)*(a + c)**2
    G = a**3 + a**2*(b + c) + 3*a*b*c + b*c*(b + c)
    assert sp.expand(c*(a - b + c)*(a + b)**2 - (a**3*c + a**2*b*c - a*b**2*c - b**3*c + a**2*c**2 + 2*a*b*c**2 + b**2*c**2)) == 0
    assert sp.expand(F - (a**3*(c - b) + 3*a*b*c*(c - b) + b*c*(c**2 - b**2) + a**2*(c**2 - b**2))) == 0
    assert sp.expand(F - (c - b) * G) == 0
    assert sp.simplify(BD2 - CE2 - a*(a + b + c)*F / ((a + b)**2 * (a + c)**2)) == 0
    for _ in range(500):
        A, B, C = _rand_tri(rng); a_, b_, c_ = dist(B, C), dist(C, A), dist(A, B)
        D = lerp(A, C, c_ / (a_ + c_)); E = lerp(A, B, b_ / (a_ + b_))
        assert close(ang(A, B, D), ang(D, B, C)) and close(ang(A, C, E), ang(E, C, B))
        assert close(dist(B, D) ** 2, a_ * c_ * ((a_ + c_) ** 2 - b_ ** 2) / (a_ + c_) ** 2, 1e-7)
        if abs(b_ - c_) > 1e-3:
            assert (dist(B, D) - dist(C, E)) * (c_ - b_) > 0          # AB>AC ⇔ BD>CE
            mb = dist(B, lerp(C, A, .5)); mc = dist(C, lerp(A, B, .5))
            assert (mb - mc) * (c_ - b_) > 0 and close(mb**2 - mc**2, 0.75 * (c_**2 - b_**2), 1e-7)
    for _ in range(200):   # ∠A=60° なら ID=IE
        t1 = rng.uniform(10, 110); A = (0.0, 0.0); B = (rng.uniform(1, 5), 0.0); C = onc(A, rng.uniform(1, 5), 60)
        a_, b_, c_ = dist(B, C), dist(C, A), dist(A, B); I = incen(A, B, C)
        D = lerp(A, C, c_ / (a_ + c_)); E = lerp(A, B, b_ / (a_ + b_)); assert close(dist(I, D), dist(I, E), 1e-7)


def v2():
    rng = random.Random(2)
    # 2.1
    def bytri(A_, B_, C_):
        k = 3.0
        return tri(k * math.sin(math.radians(A_)), k * math.sin(math.radians(B_)), k * math.sin(math.radians(C_)))
    A, B, C = bytri(70, 60, 50); O = circum(A, B, C)
    assert close(ang(O, B, C), 20) and close(ang(O, C, A), 30) and close(ang(O, A, B), 40) and close(ang(B, A, C), 70)
    I = incen(A, B, C); assert close(ang(B, I, C), 125)
    A, B, C = bytri(55, 60, 65); O = circum(A, B, C)
    assert close(ang(O, A, B), 25) and close(ang(O, B, C), 35) and close(ang(O, C, A), 30) and close(ang(A, B, C), 60)
    A, B, C = bytri(56, 70, 54); assert close(ang(B, incen(A, B, C), C), 118)
    for _ in range(200):
        A, B, C = _rand_tri(rng); S = area(A, B, C); G = cent(A, B, C); M = lerp(B, C, .5); N = lerp(C, A, .5)
        assert close(area(G, M, C) + area(G, C, N), S / 3, 1e-9)
        Pp, Q = lerp(A, B, 2 / 3), lerp(A, C, 2 / 3); assert close(crs(sub(Q, Pp), sub(G, Pp)), 0, 1e-9)
        assert close(area(A, Pp, Q), 4 * S / 9, 1e-9)
    # 2.2
    def tang(a, b, c):
        A, B, C = tri(a, b, c); I = incen(A, B, C); J = excen(A, B, C)
        D, E = foot(I, B, C), foot(J, B, C)
        return dist(B, D), dist(B, E), dist(I, D), dist(J, E), dist(J, foot(J, A, B))
    t = tang(8, 5, 7); assert close(t[0], 5) and close(t[1], 3) and close(t[2], math.sqrt(3)) and close(t[3], 5 * math.sqrt(3)) and close(t[4], t[3])
    A, B, C = tri(8, 5, 7); assert close(ang(A, C, B), 60) and close(area(A, B, C), 10 * math.sqrt(3))
    J = excen(A, B, C); Pp = foot(J, A, B); assert close(dist(A, Pp), 10) and dist(A, Pp) > dist(A, B)
    t = tang(14, 15, 13); assert close(t[0], 6) and close(t[1], 8) and close(t[2], 4) and close(t[3], 12)
    # 2.3 / 2.4 鋭角三角形
    n = 0
    while n < 300:
        A, B, C = _rand_tri(rng)
        if max(ang(B, A, C), ang(A, B, C), ang(A, C, B)) >= 89 or abs(dist(A, B) - dist(A, C)) < 1e-3: continue
        n += 1
        O = circum(A, B, C); R = dist(O, A); H = orth(A, B, C); G = cent(A, B, C); M = lerp(B, C, .5)
        assert close(ang(B, H, C), 180 - ang(B, A, C), 1e-7)
        D = foot(A, B, C); Pp = line_circ(A, D, O, R)[1]
        assert close(dist(H, D), dist(D, Pp), 1e-7) and close(dist(refl(H, B, C), O), R, 1e-7)
        Q = sub(mul(M, 2), H); assert close(dist(O, Q), R, 1e-7) and close(dist(Q, sub(mul(O, 2), A)), 0, 1e-7)
        assert close(dist(A, H), 2 * dist(O, M), 1e-7)
        assert close(dist(G, H), 2 * dist(O, G), 1e-7) and close(crs(sub(G, O), sub(H, O)), 0, 1e-7)
        Dd = sub(mul(O, 2), B); assert close(dist(A, H), dist(Dd, C), 1e-7)
    for _ in range(100):  # ∠A=60° → AH=AO
        A = (0.0, 0.0); B = (rng.uniform(2, 4), 0.0); C = onc(A, rng.uniform(2, 4), 60)
        if max(ang(A, B, C), ang(A, C, B)) >= 89: continue
        assert close(dist(A, orth(A, B, C)), dist(A, circum(A, B, C)), 1e-7)
    # 2.5 エルデシュ・モーデル
    for _ in range(4000):
        A, B, C = _rand_tri(rng); Pp = _in_tri(rng, A, B, C)
        a, b, c = dist(B, C), dist(C, A), dist(A, B)
        x, y, z = dist(Pp, foot(Pp, B, C)), dist(Pp, foot(Pp, C, A)), dist(Pp, foot(Pp, A, B))
        PA, PB, PC = dist(Pp, A), dist(Pp, B), dist(Pp, C)
        assert a * PA >= c * y + b * z - 1e-9 and b * PB >= a * z + c * x - 1e-9 and c * PC >= b * x + a * y - 1e-9
        assert PA + PB + PC >= 2 * (x + y + z) - 1e-9 and PA * PB * PC >= 8 * x * y * z - 1e-9
    A, B, C = (0.0, 0.0), (1.0, 0.0), (0.5, math.sqrt(3) / 2); O = cent(A, B, C); x = dist(O, foot(O, A, B))
    assert close(3 * dist(O, A), 6 * x) and close(dist(O, A) ** 3, 8 * x ** 3)


def v3():
    import sympy as sp
    rng = random.Random(3)
    A, B, C = _rand_tri(rng)
    def rat(p, q, r): return dist(p, q) / dist(q, r)
    # 3.1
    def cm(ar, bp):
        R = lerp(A, B, ar); Pp = lerp(B, C, bp); O = inter(A, Pp, C, R); Q = inter(B, O, C, A)
        return rat(C, Q, A), rat(A, O, Pp)
    t = cm(1 / 3, 3 / 7); assert close(t[0], 8 / 3) and close(t[1], 7 / 8)
    t = cm(2 / 5, 1 / 3); assert close(t[0], 3) and close(t[1], 1)
    # 3.2
    def ar2(ae, bd):
        E = lerp(A, C, ae); D = lerp(B, C, bd); Pp = inter(A, D, B, E); S = area(A, B, C)
        return rat(A, Pp, D), rat(B, Pp, E), area(Pp, A, B) / S, (area(B, C, E) - area(Pp, B, D)) / S
    t = ar2(1 / 3, 3 / 4); assert close(t[0], 2 / 3) and close(t[1], 9) and close(t[2], 3 / 10) and close(t[3], 13 / 60)
    t = ar2(2 / 3, 1 / 3); assert close(t[0], 6) and close(t[1], 3 / 4) and close(t[2], 2 / 7)
    # 3.3 ジェルゴンヌ点・ナーゲル点、3.4 共線
    for _ in range(300):
        A, B, C = _rand_tri(rng); I = incen(A, B, C)
        D, E, F = foot(I, B, C), foot(I, C, A), foot(I, A, B); O = inter(A, D, B, E)
        assert close(crs(sub(F, C), sub(O, C)), 0, 1e-7)
        Ja = excen(A, B, C); Jb = excen(B, C, A); Jc = excen(C, A, B)
        D, E, F = foot(Ja, B, C), foot(Jb, C, A), foot(Jc, A, B); O = inter(A, D, B, E)
        assert close(crs(sub(F, C), sub(O, C)), 0, 1e-7)
        a, b, c = dist(B, C), dist(C, A), dist(A, B)
        if min(abs(a - b), abs(b - c), abs(c - a)) < 0.05: continue
        D = inter(Jb, Jc, B, C)                  # ∠A の外角の二等分線は傍心 Jb, Jc を通る
        assert close(ang(D, A, I), 90, 1e-6) and close(rat(B, D, C), c / b, 1e-7)
        E = inter(B, I, C, A); F = inter(C, I, A, B)
        assert close(crs(sub(E, D), sub(F, D)), 0, 1e-6)
        E2 = inter(Jc, Ja, C, A); F2 = inter(Ja, Jb, A, B)
        assert close(crs(sub(E2, D), sub(F2, D)), 0, 1e-5)
    # 3.5 ラウス型
    for k, ans in ((2, 1 / 7), (3, 4 / 13)):
        D, E, F = lerp(B, C, 1 / (k + 1)), lerp(C, A, 1 / (k + 1)), lerp(A, B, 1 / (k + 1))
        Pp, Q, R = inter(A, D, B, E), inter(B, E, C, F), inter(C, F, A, D)
        assert close(area(Pp, Q, R) / area(A, B, C), ans) and close(ans, (k - 1) ** 2 / (k * k + k + 1))
        assert close(area(A, B, Pp) + area(B, C, Q) + area(C, A, R) + area(Pp, Q, R), area(A, B, C))
        assert close(rat(A, Pp, D), k * (k + 1))
    # 3.6 チェバ三角形の面積
    al, be, ga = sp.symbols("alpha beta gamma", positive=True)
    Pi = (al + be) * (be + ga) * (ga + al)
    assert sp.expand(Pi - (be*ga*(be + ga) + ga*al*(ga + al) + al*be*(al + be) + 2*al*be*ga)) == 0
    mx = 0
    for _ in range(3000):
        A, B, C = _rand_tri(rng); O = _in_tri(rng, A, B, C)
        D, E, F = inter(A, O, B, C), inter(B, O, C, A), inter(C, O, A, B); S = area(A, B, C)
        r = area(D, E, F) / S; mx = max(mx, r); assert r <= 0.25 + 1e-12
        a_, b_, g_ = area(O, B, C), area(O, C, A), area(O, A, B)
        assert close(rat(B, D, C), g_ / b_, 1e-7) and close(r, 2 * a_ * b_ * g_ / ((a_ + b_) * (b_ + g_) * (g_ + a_)), 1e-7)
    assert mx > 0.249
    G = cent(A, B, C); assert close(area(lerp(B, C, .5), lerp(C, A, .5), lerp(A, B, .5)) / area(A, B, C), .25)
    D = lerp(B, C, 1 / 3); E = lerp(C, A, 1 / 2); O = inter(A, D, B, E); F = inter(C, O, A, B)
    assert close(rat(A, F, B), 2) and close(area(D, E, F) / area(A, B, C), 2 / 9)


def v4():
    rng = random.Random(4)
    # 4.1
    O1, A, B, C, D, O2, A2, B2, C2, D2, T, T0 = _c41(); E = inter(A, C, B, D)
    assert close(ang(A, O1, B), 100) and close(ang(C, A, D), 25) and close(ang(A, C, B), 50) and close(ang(A, E, B), 75)
    assert close(ang(B2, A2, D2), 100) and close(ang(D2, C2, T), 35) and close(dot(sub(T, C2), sub(C2, O2)), 0)
    assert crs(sub(D2, C2), sub(T, C2)) * crs(sub(D2, C2), sub(B2, C2)) < 0          # T は直線 CD に関して B と反対側
    assert close(ang(B2, C2, D2), 80) and close(ang(C2, B2, D2), 35) and close(ang(B2, D2, C2), 65)
    O = (0.0, 0.0); A, B, C, D = (onc(O, 1, t) for t in (0, 80, 180, 240)); E = inter(A, C, B, D)
    assert close(ang(A, O, B), 80) and close(ang(C, A, D), 30) and close(ang(A, C, B), 40) and close(ang(A, E, B), 70)
    B, C, D, A = (onc(O, 1, t) for t in (0, 140, 220, 290)); T = add(C, rot(sub(C, O), (0, 0), 90))
    assert close(ang(B, A, D), 110) and close(ang(D, C, T), 40) and close(ang(B, C, D), 70) and close(ang(C, B, D), 40) and close(ang(B, D, C), 70)
    # 4.2
    A, B, C = tri(8, 5, 7); E, F = foot(B, C, A), foot(C, A, B); assert close(dist(E, F), 8 / 7)
    A, B, C = tri(7, 6, 5); E, F = foot(B, C, A), foot(C, A, B); assert close(dist(E, F), 7 / 5)
    for _ in range(300):
        A, B, C = _rand_tri(rng)
        if max(ang(B, A, C), ang(A, B, C), ang(A, C, B)) >= 89: continue
        E, F = foot(B, C, A), foot(C, A, B); M = lerp(B, C, .5)
        assert close(dist(M, E), dist(M, B), 1e-7) and close(dist(M, F), dist(M, B), 1e-7)
        assert close(ang(A, E, F), ang(A, B, C), 1e-6) and close(dist(E, F), dist(B, C) * math.cos(math.radians(ang(B, A, C))), 1e-7)
    # 4.3
    for _ in range(300):
        A, B, C = _rand_tri(rng); O = circum(A, B, C); R = dist(O, A); I = incen(A, B, C); J = excen(A, B, C)
        M = line_circ(A, I, O, R)[1]
        assert close(dist(M, B), dist(M, C), 1e-7) and close(dist(M, B), dist(M, I), 1e-7) and close(dist(M, J), dist(M, B), 1e-7)
    # 4.4 トレミー
    for _ in range(300):
        ts = sorted(rng.uniform(0, 360) for _ in range(4))
        if min(b - a for a, b in zip(ts, ts[1:] + [ts[0] + 360])) < 5: continue
        A, B, C, D = (onc((0, 0), 1, t) for t in ts)
        assert close(dist(A, B) * dist(C, D) + dist(A, D) * dist(B, C), dist(A, C) * dist(B, D), 1e-9)
        t = ang(D, B, C); u = sub(A, B)
        for sg in (1, -1):
            E = inter(B, add(B, rot(u, (0, 0), sg * t)), A, C)
            if close(ang(A, B, E), t, 1e-6) and close(dist(A, E) + dist(E, C), dist(A, C), 1e-9): break
        assert close(dist(A, B) * dist(C, D), dist(A, E) * dist(B, D), 1e-9) and close(dist(A, D) * dist(B, C), dist(E, C) * dist(B, D), 1e-9)
    pent = [onc((0, 0), 1, 72 * k) for k in range(5)]; s1 = dist(pent[0], pent[1])
    assert close(dist(pent[0], pent[2]) / s1, (1 + math.sqrt(5)) / 2) and close(math.cos(math.radians(36)), (1 + math.sqrt(5)) / 4)
    hp = [onc((0, 0), 1, 360 / 7 * k) for k in range(7)]
    assert close(1 / dist(hp[0], hp[1]), 1 / dist(hp[0], hp[2]) + 1 / dist(hp[0], hp[3]))
    # 4.5 ファニャノ
    def per(A, B, C, u, v, w):
        Pp, Q, R = lerp(B, C, u), lerp(C, A, v), lerp(A, B, w)
        return dist(Pp, Q) + dist(Q, R) + dist(R, Pp)
    for (a, b, c), ans in (((14, 15, 13), 1344 / 65), ((6, 5, 5), 192 / 25)):
        A, B, C = tri(a, b, c); D, E, F = foot(A, B, C), foot(B, C, A), foot(C, A, B)
        orth_p = dist(D, E) + dist(E, F) + dist(F, D)
        sA = math.sin(math.radians(ang(B, A, C)))
        assert close(orth_p, ans) and close(orth_p, 2 * dist(A, D) * sA)
        D1, D2 = refl(D, A, B), refl(D, A, C); assert close(dist(D1, D2), orth_p) and close(crs(sub(F, D1), sub(E, D1)), 0, 1e-9)
        best = 1e9
        for _ in range(20000):
            best = min(best, per(A, B, C, rng.random(), rng.random(), rng.random()))
        assert best >= ans - 1e-9
        u, v, w = .5, .5, .5; h = .1   # 局所探索で最小値に近づくことを確認
        cur = per(A, B, C, u, v, w)
        while h > 1e-9:
            moved = False
            for du, dv, dw in ((h, 0, 0), (-h, 0, 0), (0, h, 0), (0, -h, 0), (0, 0, h), (0, 0, -h)):
                nu, nv, nw = u + du, v + dv, w + dw
                if 0 < nu < 1 and 0 < nv < 1 and 0 < nw < 1 and per(A, B, C, nu, nv, nw) < cur:
                    u, v, w, cur, moved = nu, nv, nw, per(A, B, C, nu, nv, nw), True
            if not moved: h /= 2
        assert close(cur, ans, 1e-6)
    A, B, C = tri(14, 15, 13); assert close(area(A, B, C), 84) and close(dist(A, foot(A, B, C)), 12)
    assert close(2 * 84 / (dist(A, B) * dist(B, C) * dist(C, A) / (4 * 84)), 1344 / 65)


def v5():
    import sympy as sp
    rng = random.Random(5)
    # 5.1 図の点が条件どおりか
    g1, g2, g3 = _c51(); O = (0.0, 0.0)
    for g in (g1, g2, g3):
        for k in "ABCDT":
            if k in g: assert close(dist(O, g[k]), g["R"])
    P = g1["P"]; assert [round(dist(P, g1[k]), 9) for k in "ABCD"] == [4, 6, 3, 8] and dist(P, O) < 6
    assert close(dist(g1["A"], g1["B"]), 10) and close(dist(g1["C"], g1["D"]), 11)
    P = g2["P"]; assert [round(dist(P, g2[k]), 9) for k in "ABCD"] == [3, 8, 4, 6]
    P = g3["P"]; assert [round(dist(P, g3[k]), 9) for k in "ABT"] == [4, 9, 6] and close(dot(g3["T"], sub(g3["T"], P)), 0)
    assert 5 * 4 == 2 * 10 and 2 * 12 == 3 * (3 + 5) and 2 * 8 == 4 ** 2
    # 5.2 位置関係
    def ncom(r1, r2, d):
        if d > r1 + r2 + 1e-12: return 4, 0
        if abs(d - (r1 + r2)) < 1e-12: return 3, 1
        if d > abs(r1 - r2) + 1e-12: return 2, 2
        if abs(d - abs(r1 - r2)) < 1e-12: return 1, 1
        return 0, 0
    for k in range(1, 1500):
        r = k / 100; nt, npnt = ncom(r, 4, 7)
        assert (npnt == 2) == (3 < r < 11)
    assert ncom(3, 4, 7)[0] == 3 and ncom(11, 4, 7)[0] == 1
    n = (-2 / 7, math.sqrt(45) / 7); m = (6 / 7, -math.sqrt(13) / 7); O2 = (7.0, 0.0)
    S, S2 = mul(n, 2), add(O2, mul(n, 4)); T, T2 = mul(m, 2), sub(O2, mul(m, 4))
    for X, Y in ((S, S2), (T, T2)):
        assert close(dist(O, foot(O, X, Y)), 2) and close(dist(O2, foot(O2, X, Y)), 4)
    assert close(dist(S, S2), 3 * math.sqrt(5)) and close(dist(T, T2), math.sqrt(13))
    assert close(math.sqrt(100 - 16), 2 * math.sqrt(21)) and close(math.sqrt(100 - 64), 6) and close(math.sqrt(13 ** 2 - 5 ** 2), 12)
    # 5.3
    for (a, b, c), ans in (((5, 4, 6), (6, 9, 4)), ((4, 3, 5), (15 / 4, 25 / 4, 9 / 4))):
        A, B, C = tri(a, b, c); Oc = circum(A, B, C); t = rot(sub(A, Oc), (0, 0), 90)
        Pp = inter(A, add(A, t), B, C); assert Pp[0] > C[0]
        assert close(dist(Pp, A), ans[0]) and close(dist(Pp, B), ans[1]) and close(dist(Pp, C), ans[2])
    # 5.4
    M, A, B, S, T, cs = _c54()
    for (z, k), X in zip(cs, (S, T)):
        assert close(dist(z, A), k) and close(dist(z, B), k) and close(dist(z, X), k) and close(dot(sub(X, z), sub(T, S)), 0)
    assert close(dist(M, S), 6) and close(dist(M, T), 6) and close(dist(S, T), 12)
    for _ in range(200):   # 3円の根軸は1点で交わる
        cs3 = [((rng.uniform(-3, 3), rng.uniform(-3, 3)), rng.uniform(2, 4)) for _ in range(3)]
        def ax(c1, c2):  # 根軸 a x + b y = c
            (x1, y1), r1 = c1; (x2, y2), r2 = c2
            return 2 * (x2 - x1), 2 * (y2 - y1), (x2*x2 + y2*y2 - r2*r2) - (x1*x1 + y1*y1 - r1*r1)
        L1, L2, L3 = ax(cs3[0], cs3[1]), ax(cs3[0], cs3[2]), ax(cs3[1], cs3[2])
        det = L1[0] * L2[1] - L1[1] * L2[0]
        if abs(det) < 1e-3: continue
        x = (L1[2] * L2[1] - L1[1] * L2[2]) / det; y = (L1[0] * L2[2] - L1[2] * L2[0]) / det
        assert close(L3[0] * x + L3[1] * y, L3[2], 1e-7)
    # 5.5 オイラーの定理
    for _ in range(500):
        A, B, C = _rand_tri(rng); Oc = circum(A, B, C); R = dist(Oc, A); I = incen(A, B, C); r = dist(I, foot(I, B, C))
        J = excen(A, B, C); ra = dist(J, foot(J, B, C)); M = line_circ(A, I, Oc, R)[1]
        assert close(dist(Oc, I) ** 2, R * R - 2 * R * r, 1e-7) and close(dist(Oc, J) ** 2, R * R + 2 * R * ra, 1e-6)
        assert close(dist(A, I) * dist(I, M), 2 * R * r, 1e-7) and close(dist(M, B), 2 * R * math.sin(math.radians(ang(B, A, C) / 2)), 1e-7)
    for (a, b, c), ans in (((14, 15, 13), math.sqrt(65) / 8), ((6, 5, 5), 5 / 8)):
        A, B, C = tri(a, b, c); assert close(dist(circum(A, B, C), incen(A, B, C)), ans)
    assert Fr(65, 8) ** 2 - 2 * Fr(65, 8) * 4 == Fr(65, 64) and Fr(25, 8) ** 2 - 2 * Fr(25, 8) * Fr(3, 2) == Fr(25, 64)
    # 5.6 バタフライ
    Z, R, P, Q, M, A, B, C, D, X, Y = _c56()
    assert X[0] < 0 < Y[0] and close(dist(M, X), dist(M, Y)) and close(dist(P, M), dist(M, Q))
    for _ in range(2000):
        Zc = (rng.uniform(-1, 1), rng.uniform(-1, 1)); R = rng.uniform(1, 3)
        M = add(Zc, (rng.uniform(-.8, .8) * R / 1.5, rng.uniform(-.8, .8) * R / 1.5))
        if dist(M, Zc) > 0.9 * R: continue
        t0 = rng.uniform(0, 180); Pq = line_circ(M, onc(M, 1, t0), Zc, R)
        t1, t2 = rng.uniform(t0 + 5, t0 + 175), rng.uniform(t0 + 5, t0 + 175)
        if abs(t1 - t2) < 3: continue
        a = line_circ(M, onc(M, 1, t1), Zc, R); c = line_circ(M, onc(M, 1, t2), Zc, R)
        A, B = a[1], a[0]; C, D = c[1], c[0]   # A, C は同じ側（t の正の向き）
        X, Y = inter(A, D, Pq[0], Pq[1]), inter(C, B, Pq[0], Pq[1])
        x, y = dist(M, X), dist(M, Y)
        assert close(dist(A, X) * dist(X, D), dist(Pq[0], X) * dist(X, Pq[1]), 1e-7)
        u = sub(onc(M, 1, t0), M); sx, sy = dot(sub(X, M), u), dot(sub(Y, M), u)
        assert sx * sy < 0 and dot(sub(Pq[0], M), u) < 0            # X, Y は M の反対側
        p_, q_ = (dist(M, Pq[0]), dist(M, Pq[1])) if sx < 0 else (dist(M, Pq[1]), dist(M, Pq[0]))
        assert close(1 / x - 1 / y, 1 / p_ - 1 / q_, 1e-6)
        if close(p_, q_, 1e-12): assert close(x, y, 1e-7)
    x, y, p, q = sp.symbols("x y p q")
    assert sp.expand(x**2*(p + y)*(q - y) - y**2*(p - x)*(q + x) - (x + y)*(p*q*(x - y) - (p - q)*x*y)) == 0


def v6():
    rng = random.Random(6)
    # 6.1
    for (m, n) in ((2, 3), (3, 1)):
        A, B, C, D, D2, Pp, Q = _c61(m, n)
        assert close(dist(A, Pp) / dist(Pp, B), m / n) and close(dist(A, Pp) + dist(Pp, B), dist(A, B))
        assert close(dist(Q, A) / dist(Q, B), m / n) and close(abs(dist(Q, A) - dist(Q, B)), dist(A, B))
        assert (Q[0] < 0) == (m < n) and (Q[0] > 5) == (m > n)
    # 6.2
    for _ in range(200):
        a, b = rng.uniform(.3, 4), rng.uniform(.3, 4); O = (0.0, 0.0); w = onc(O, 1, rng.uniform(10, 170))
        E, A, B = (1.0, 0.0), (a, 0.0), mul(w, b); C = inter(A, add(A, sub(B, E)), O, w); assert close(dist(O, C), a * b, 1e-7)
        Bq, Aq = (b, 0.0), mul(w, a); Cq = inter(E, add(E, sub(Aq, Bq)), O, w); assert close(dist(O, Cq), a / b, 1e-7)
        for s, t in ((a, 1.0), (a, b)):
            Oc = ((s + t) / 2, 0.0); D = (s, math.sqrt(((s + t) / 2) ** 2 - (s - (s + t) / 2) ** 2))
            assert close(D[1], math.sqrt(s * t), 1e-9) and close(ang((0, 0), D, (s + t, 0)), 90, 1e-7)
    # 6.3
    A, B, C, P1, Q1, R1, S1, Pp, Q, R, S = _c63()
    assert close(dist(Pp, Q), dist(Q, R)) and close(dist(Q, R), dist(R, S)) and close(ang(Pp, Q, R), 90) and close(ang(Q, R, S), 90)
    assert close(dist(A, S) + dist(S, B), dist(A, B)) and close(dist(A, R) + dist(R, C), dist(A, C)) and 0 < Pp[0] < Q[0] < C[0]
    a, h = dist(B, C), A[1]; assert close(dist(Pp, Q), a * h / (a + h))
    A, B, C = (0.0, 0.0), (3.0, 0.0), (0.0, 4.0); h = 2 * area(A, B, C) / dist(B, C); assert close(5 * h / (5 + h), 60 / 37)
    # 6.4 フェルマー点
    def Lmin(A, B, C):
        f = lambda p: dist(p, A) + dist(p, B) + dist(p, C)
        p = cent(A, B, C); cur = f(p); hstep = 1.0
        while hstep > 1e-10:
            moved = False
            for d in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)):
                q = add(p, mul(d, hstep))
                if f(q) < cur: p, cur, moved = q, f(q), True
            if not moved: hstep /= 2
        return cur, p
    for (c, a, Bd), ans in (((5.0, 8.0, 60.0), math.sqrt(129)), ((7.0, 8.0, 60.0), 13.0)):
        A, B, C, D, G, R, Pp = _c64(c, a, Bd)
        assert max(ang(B, A, C), ang(A, B, C), ang(A, C, B)) < 90
        assert close(dist(A, D), ans) and close(dist(Pp, B) + dist(Pp, C), dist(Pp, D), 1e-9)
        assert close(dist(Pp, A) + dist(Pp, B) + dist(Pp, C), ans, 1e-9)
        for X, Y in ((A, B), (B, C), (C, A)): assert close(ang(X, Pp, Y), 120, 1e-6)
        m, q = Lmin(A, B, C); assert close(m, ans, 1e-7) and dist(q, Pp) < 1e-5
        for _ in range(3000):
            X = _in_tri(rng, A, B, C); assert dist(X, A) + dist(X, B) + dist(X, C) >= ans - 1e-9
    A, B, C = tri(8, 7, 5); assert close(ang(A, B, C), 60)
    for _ in range(100):
        A, B, C = _rand_tri(rng)
        if max(ang(B, A, C), ang(A, B, C), ang(A, C, B)) >= 115: continue
        a, b, c = dist(B, C), dist(C, A), dist(A, B)
        assert close(Lmin(A, B, C)[0] ** 2, (a*a + b*b + c*c) / 2 + 2 * math.sqrt(3) * area(A, B, C), 1e-6)


def v7():
    import itertools
    phi = (1 + math.sqrt(5)) / 2
    # 7.1 切頂二十面体・切頂八面体
    base = [(0, 1, 3 * phi), (1, 2 + phi, 2 * phi), (phi, 2, 2 * phi + 1)]
    pts = set()
    for b in base:
        for sg in itertools.product((1, -1), repeat=3):
            v = tuple(b[i] * sg[i] for i in range(3))
            for k in range(3): pts.add(tuple(round(v[(i + k) % 3], 9) for i in range(3)))
    pts = list(pts); E = [(p, q) for p, q in itertools.combinations(pts, 2) if abs(_d3(p, q) - 2) < 1e-6]
    assert len(pts) == 60 and len(E) == 90 and all(sum(1 for e in E if p in e) == 3 for p in pts)
    assert 60 - 90 + 32 == 2 and math.comb(60, 2) - 90 - (5 * 12 + 9 * 20) == 1440
    pts = {tuple(s * x for s, x in zip(sg, pm)) for pm in itertools.permutations((0, 1, 2)) for sg in itertools.product((1, -1), repeat=3)}
    pts = list(pts); E = [1 for p, q in itertools.combinations(pts, 2) if abs(_d3(p, q) - math.sqrt(2)) < 1e-9]
    assert len(pts) == 24 and len(E) == 36 and 24 - 36 + 14 == 2 and math.comb(24, 2) - 36 - (6 * 2 + 8 * 9) == 156
    # 7.2 正多面体
    sols = []
    for n in range(3, 50):
        for m in range(3, 50):
            if m * Fr(180 * (n - 2), n) < 360:
                assert (m - 2) * (n - 2) < 4
                e = Fr(2 * m * n, 2 * m + 2 * n - m * n); f, v = 2 * e / n, 2 * e / m
                assert v - e + f == 2; sols.append((n, m, int(v), int(e), int(f)))
    assert sorted(sols) == sorted([(3, 3, 4, 6, 4), (4, 3, 8, 12, 6), (3, 4, 6, 12, 8), (5, 3, 20, 30, 12), (3, 5, 12, 30, 20)])
    pts = list({tuple(s * x for s, x in zip(sg, pm)) for pm in itertools.permutations((1, 1, 0)) for sg in itertools.product((1, -1), repeat=3)})
    E = [1 for p, q in itertools.combinations(pts, 2) if abs(_d3(p, q) - math.sqrt(2)) < 1e-9]
    assert len(pts) == 12 and len(E) == 24
    # 7.3
    def foot_plane(O, A, B, C):
        n = _cr3(_sb3(B, A), _sb3(C, A)); t = _dt3(_sb3(O, A), n) / _dt3(n, n)
        return (O[0] - n[0] * t, O[1] - n[1] * t, O[2] - n[2] * t)
    for a, b, c, ans in ((2, 2, 1, math.sqrt(6) / 3), (3, 3, 3, math.sqrt(3))):
        O, A, B, C = (0, 0, 0), (a, 0, 0), (0, b, 0), (0, 0, c); H = foot_plane(O, A, B, C)
        assert close(_d3(O, H), ans) and close(_dt3(_sb3(H, A), _sb3(C, B)), 0) and close(_dt3(_sb3(H, B), _sb3(A, C)), 0)
        assert close(1 / _d3(O, H) ** 2, 1 / a ** 2 + 1 / b ** 2 + 1 / c ** 2)
    T = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; assert close(_dt3(_sb3(T[1], T[0]), _sb3(T[3], T[2])), 0)
    # 7.4
    V = _cube(); assert close(_vol(V["A"], V["C"], V["F"], V["H"]), 1 / 3)
    assert all(close(_d3(V[x], V[y]), math.sqrt(2)) for x, y in itertools.combinations("ACFH", 2))
    for k, (p, q, r) in dict(B="ACF", D="ACH", E="AFH", G="CFH").items():
        assert all(close(_d3(V[k], V[z]), 1) for z in (p, q, r)) and close(_vol(V[k], V[p], V[q], V[r]), 1 / 6)
    fc = [(.5, .5, 0), (.5, .5, 1), (0, .5, .5), (1, .5, .5), (.5, 0, .5), (.5, 1, .5)]
    assert close(min(_d3(p, q) for p, q in itertools.combinations(fc, 2)), math.sqrt(2) / 2)
    c = (.5, .5, .5); N = 60; cnt = 0                  # 正八面体の体積を格子点で近似
    for i in range(N):
        for j in range(N):
            for k in range(N):
                x, y, z = (i + .5) / N, (j + .5) / N, (k + .5) / N
                cnt += abs(x - .5) + abs(y - .5) + abs(z - .5) <= .5
    assert abs(cnt / N ** 3 - 1 / 6) < 0.01
    mids = list({tuple((V[e[0]][i] + V[e[1]][i]) / 2 for i in range(3)) for e in _CE})
    E = [1 for p, q in itertools.combinations(mids, 2) if abs(_d3(p, q) - math.sqrt(2) / 2) < 1e-9]
    assert len(mids) == 12 and len(E) == 24 and close(_vol(V["A"], (.5, 0, 0), (0, .5, 0), (0, 0, .5)), 1 / 48) and close(1 - 8 / 48, 5 / 6)
    T = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]; s = _d3(T[0], T[1])
    tv = [tuple(T[i][k] + (T[j][k] - T[i][k]) / 3 for k in range(3)) for i in range(4) for j in range(4) if i != j]
    E = [1 for p, q in itertools.combinations(tv, 2) if abs(_d3(p, q) - s / 3) < 1e-9]
    assert len(tv) == 12 and len(E) == 18 and 12 - 18 + 8 == 2
    corner = _vol(T[0], tv[0], tv[1], tv[2]); assert close(1 - 4 * corner / _vol(*T), 23 / 27)
    # 7.5 等面四面体
    for (a, b, c), p2, ans in (((7, 8, 9), (33, 16, 48), 16 * math.sqrt(11)), ((5, 6, 7), (19, 6, 30), 2 * math.sqrt(95))):
        p, q, r, O, X, Y, Z = _c75(*p2)
        assert close(p * p + q * q, a * a) and close(q * q + r * r, b * b) and close(r * r + p * p, c * c)
        L = sorted(round(_d3(u, w), 9) for u, w in itertools.combinations((O, X, Y, Z), 2)); assert L == sorted([a, a, b, b, c, c])
        for face in itertools.combinations((O, X, Y, Z), 3):
            assert sorted(round(_d3(u, w), 9) for u, w in itertools.combinations(face, 2)) == [a, b, c]
        assert close(_vol(O, X, Y, Z), ans) and close(ans, math.sqrt((a*a + b*b - c*c) * (b*b + c*c - a*a) * (c*c + a*a - b*b) / 72))
    # 7.6 立方体の断面
    def section(t):
        P = []
        for e in _CE:
            u, w = V[e[0]], V[e[1]]; su, sw = sum(u), sum(w)
            if (su - t) * (sw - t) < 0: s_ = (t - su) / (sw - su); P.append(tuple(u[i] + (w[i] - u[i]) * s_ for i in range(3)))
        g = tuple(sum(p[i] for p in P) / len(P) for i in range(3)); e1 = _sb3(P[0], g); nrm = (1, 1, 1)
        e2 = _cr3(nrm, e1)
        P.sort(key=lambda p: math.atan2(_dt3(_sb3(p, g), e2), _dt3(_sb3(p, g), e1)))
        ar = sum(math.sqrt(_dt3(cr, cr)) for cr in (_cr3(_sb3(P[i], g), _sb3(P[(i + 1) % len(P)], g)) for i in range(len(P)))) / 2
        per = sum(_d3(P[i], P[(i + 1) % len(P)]) for i in range(len(P)))
        return ar, per, len(P)
    best = 0
    for k in range(3000):
        t = 3 * (k + 0.37) / 3000; ar, per, n = section(t)
        f = math.sqrt(3) / 2 * (t * t if t <= 1 else (t * t - 3 * (t - 1) ** 2 if t <= 2 else (3 - t) ** 2))
        assert close(ar, f, 1e-9) and per <= 3 * math.sqrt(2) + 1e-9 and n == (3 if (t < 1 or t > 2) else 6)
        if 1 <= t <= 2: assert close(per, 3 * math.sqrt(2), 1e-9)
        best = max(best, ar)
    ar, per, n = section(1.5); assert close(ar, 3 * math.sqrt(3) / 4) and n == 6 and close(best, ar, 1e-6)
    assert close(per / 6, math.sqrt(2) / 2)


def verify():
    v1()
    v2()
    v3()
    v4()
    v5()
    v6()
    v7()
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert len(SEC) == 7 and 32 <= len(items) <= 38, len(items)          # 目標 35±3
    assert cnt == {1: 7, 2: 9, 3: 10, 4: 6, 5: 5}, cnt                    # ★5 は3題以上
    for it in items:
        for k in ("q", "hint", "sol", "note", "ex", "exa"):
            s = it.get(k, "")
            assert s.count("$") % 2 == 0, (it["title"], k)
            assert "$$" not in s, (it["title"], k)
