"""第18章 平面ベクトル（数学C）　担当 M18
節ごとに SEC.append(...)。本文中の \\VV{AB} は最後に \\overrightarrow{\\mathrm{AB}} に置き換える。"""
import math, random, re
from fractions import Fraction as Fr
from sympy import (symbols, sqrt, Rational, simplify, expand, Matrix, solve, nsimplify,
                   cos, sin, pi, Eq, factor, zeros)

# ---------------------------------------------------------------- 図の小道具（座標は Python で計算）
def _n(v):
    return f"{v:.1f}"

def _svg(w, h, body):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{body}</svg>'

def _ln(p, q, c="#333", w=1.1, d=""):
    da = f' stroke-dasharray="{d}"' if d else ""
    return f'<line x1="{_n(p[0])}" y1="{_n(p[1])}" x2="{_n(q[0])}" y2="{_n(q[1])}" stroke="{c}" stroke-width="{w}"{da}/>'

def _ar(p, q, c="#1f4fbf", w=1.5, hl=7.0):
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    bx, by = q[0] - ux * hl, q[1] - uy * hl
    h = hl * 0.42
    return (_ln(p, (bx, by), c, w) +
            f'<polygon points="{_n(q[0])},{_n(q[1])} {_n(bx - uy*h)},{_n(by + ux*h)} {_n(bx + uy*h)},{_n(by - ux*h)}" fill="{c}"/>')

def _pg(pts, fill="none", c="#333", w=1.1, op=1.0, d=""):
    da = f' stroke-dasharray="{d}"' if d else ""
    s = " ".join(f"{_n(x)},{_n(y)}" for x, y in pts)
    return f'<polygon points="{s}" fill="{fill}" fill-opacity="{op}" stroke="{c}" stroke-width="{w}"{da}/>'

def _pl(pts, c="#333", w=1.1, d=""):
    da = f' stroke-dasharray="{d}"' if d else ""
    s = " ".join(f"{_n(x)},{_n(y)}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" stroke="{c}" stroke-width="{w}"{da}/>'

def _dot(p, r=2.0, c="#222"):
    return f'<circle cx="{_n(p[0])}" cy="{_n(p[1])}" r="{r}" fill="{c}"/>'

def _cir(p, r, c="#333", w=1.1, fill="none", d=""):
    da = f' stroke-dasharray="{d}"' if d else ""
    return f'<circle cx="{_n(p[0])}" cy="{_n(p[1])}" r="{_n(r)}" fill="{fill}" stroke="{c}" stroke-width="{w}"{da}/>'

def _tx(p, s, size=11, c="#222", it=False):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{_n(p[0])}" y="{_n(p[1] + size * 0.36)}" font-size="{size}" text-anchor="middle" fill="{c}"{st}>{s}</text>'

def _lab(p, s, ang, dist=9, size=11, c="#222"):
    """点 p（画面座標）から角 ang 度（右=0，上=90）の向きに dist 離して文字を置く"""
    a = math.radians(ang)
    return _tx((p[0] + dist * math.cos(a), p[1] - dist * math.sin(a)), s, size, c)

def _vlab(p, s, c="#1f4fbf"):
    """ベクトルの文字（斜体＋上に小さな矢印）"""
    return _tx(p, s, 11, c, True) + _ar((p[0] - 4, p[1] - 8), (p[0] + 5, p[1] - 8), c, 0.8, 3)

def _tr(ox, oy, s):
    return lambda P: (ox + s * P[0], oy - s * P[1])

def _away(P, O):
    """点 P が中心 O から離れる向きの角（画面座標で）"""
    return math.degrees(math.atan2(-(P[1] - O[1]), P[0] - O[0]))

BL, RD, GR = "#1f4fbf", "#c0392b", "#2e8b57"
FILL = "#cfe0f7"

SEC = []

# ================================================================ 節1
def _fig_hex():
    s = 62
    T = _tr(51, 125, s)
    r3 = math.sqrt(3)
    P = {"A": (0, 0), "B": (1, 0), "C": (1.5, r3 / 2), "D": (1, r3), "E": (0, r3), "F": (-0.5, r3 / 2)}
    O = (0.5, r3 / 2)
    Q = {k: T(v) for k, v in P.items()}
    Ot = T(O)
    b = _pg([Q[k] for k in "ABCDEF"])
    for k in "CDE":
        b += _ln(Q["A"], Q[k], "#888", 0.9, "3,2")
    b += _ar(Q["A"], Q["B"], BL) + _ar(Q["A"], Q["F"], RD)
    b += _dot(Ot) + _lab(Ot, "O", -60, 9, 10)
    for k, v in Q.items():
        b += _lab(v, k, _away(v, Ot), 10)
    b += _vlab((Q["A"][0] + s / 2, Q["A"][1] + 12), "a", BL)
    b += _vlab((Q["A"][0] - 22, Q["A"][1] - s * 0.43), "b", RD)
    return _svg(164, 145, b)

def _fig_pent():
    R = 1 / (2 * math.sin(math.radians(36)))
    s = 80
    T = _tr(85, 90, s)
    angs = {"A": 90, "B": 162, "C": 234, "D": 306, "E": 18}
    P = {k: T((R * math.cos(math.radians(a)), R * math.sin(math.radians(a)))) for k, a in angs.items()}
    Ot = T((0, 0))
    b = _pg([P[k] for k in "ABCDE"])
    for u, v in (("A", "C"), ("A", "D"), ("B", "E")):
        b += _ln(P[u], P[v], "#888", 0.9, "3,2")
    b += _ar(P["A"], P["B"], BL) + _ar(P["A"], P["E"], RD)
    for k, v in P.items():
        b += _lab(v, k, _away(v, Ot), 10)
    b += _vlab(((P["A"][0] + P["B"][0]) / 2 - 10, (P["A"][1] + P["B"][1]) / 2 - 6), "a", BL)
    b += _vlab(((P["A"][0] + P["E"][0]) / 2 + 10, (P["A"][1] + P["E"][1]) / 2 - 6), "b", RD)
    return _svg(170, 166, b)

SEC.append({"title": "ベクトルの演算と1次独立",
"base": r"""・和・差・実数倍は文字式と同じ規則で計算できる。$\VV{AB}+\VV{BC}=\VV{AC}$（つなぐ），$\VV{AB}=\VV{OB}-\VV{OA}$（始点をそろえる）<br>
・平行条件：$\vec a\neq\vec 0,\ \vec b\neq\vec 0$ のとき　$\vec a\parallel\vec b\iff\vec b=k\vec a$ となる実数 $k$ がある<br>
・1次独立：$\vec a\neq\vec 0,\ \vec b\neq\vec 0,\ \vec a\nparallel\vec b$ のとき，平面上のどんな $\vec p$ も $\vec p=s\vec a+t\vec b$ とただ1通りに表せる。特に　$s\vec a+t\vec b=s'\vec a+t'\vec b\iff s=s',\ t=t'$（係数比較）""",
"items": [
 {"lv": 1, "title": "ベクトルを未知数とする方程式",
  "q": r"(1) $3(\vec x-2\vec a)+2\vec b=\vec x+4\vec b$ を満たす $\vec x$ を $\vec a,\ \vec b$ で表せ。<br>(2) $\vec x+2\vec y=\vec a$，$2\vec x-\vec y=\vec b$ を満たす $\vec x,\ \vec y$ を $\vec a,\ \vec b$ で表せ。",
  "hint": r"ベクトルの和・差・実数倍は文字式と同じ規則に従うので，数の1次方程式・連立方程式と同じように移項や加減法で解ける。",
  "sol": r"(1) 左辺を展開して　$3\vec x-6\vec a+2\vec b=\vec x+4\vec b$<br>よって $2\vec x=6\vec a+2\vec b$ より　$\boldsymbol{\vec x=3\vec a+\vec b}$<br>"
         r"(2) 第1式 $+$ 第2式 $\times2$ より　$5\vec x=\vec a+2\vec b$<br>第1式 $\times2-$ 第2式 より　$5\vec y=2\vec a-\vec b$<br>"
         r"よって　$\boldsymbol{\vec x=\dfrac{\vec a+2\vec b}{5},\ \ \vec y=\dfrac{2\vec a-\vec b}{5}}$",
  "note": r"答えをもとの式に代入して確かめる習慣をつけよう。(2) なら $\vec x+2\vec y=\dfrac{\vec a+2\vec b+4\vec a-2\vec b}{5}=\vec a$ となる。",
  "ex": r"(1) $2(\vec x+\vec a)-3(\vec b-\vec x)=\vec 0$ を満たす $\vec x$ を $\vec a,\ \vec b$ で表せ。<br>(2) $3\vec x-\vec y=\vec a$，$\vec x+2\vec y=\vec b$ を満たす $\vec x,\ \vec y$ を $\vec a,\ \vec b$ で表せ。",
  "exa": r"(1) $\vec x=\dfrac{-2\vec a+3\vec b}{5}$　(2) $\vec x=\dfrac{2\vec a+\vec b}{7},\ \vec y=\dfrac{-\vec a+3\vec b}{7}$"},
 {"lv": 1, "title": "正六角形とベクトルの表示",
  "q": _fig_hex() + r"正六角形 ABCDEF において，$\VV{AB}=\vec a$，$\VV{AF}=\vec b$ とする。次のベクトルを $\vec a,\ \vec b$ で表せ。<br>(1) $\VV{AD}$　(2) $\VV{AC}$　(3) $\VV{AE}$　(4) $\VV{CE}$",
  "hint": r"正六角形の中心 O をとると，正六角形は6つの正三角形に分かれ，ABOF などはひし形になる。平行で長さの等しい辺を見つけ，「つなぐ」「始点をそろえる」で表す。",
  "sol": r"正六角形の中心を O とする。四角形 ABOF はひし形なので　$\VV{AO}=\VV{AB}+\VV{AF}=\vec a+\vec b$<br>"
         r"(1) $\VV{AD}=2\VV{AO}=\boldsymbol{2\vec a+2\vec b}$<br>"
         r"(2) 四角形 ABCO もひし形なので $\VV{BC}=\VV{AO}$。よって　$\VV{AC}=\VV{AB}+\VV{BC}=\vec a+(\vec a+\vec b)=\boldsymbol{2\vec a+\vec b}$<br>"
         r"(3) 同様に $\VV{FE}=\VV{AO}$ より　$\VV{AE}=\VV{AF}+\VV{FE}=\boldsymbol{\vec a+2\vec b}$<br>"
         r"(4) $\VV{CE}=\VV{AE}-\VV{AC}=\boldsymbol{-\vec a+\vec b}$",
  "note": r"(4) は $\VV{CD}=\VV{AF}=\vec b$，$\VV{DE}=-\VV{AB}=-\vec a$ を使って $\VV{CE}=\VV{CD}+\VV{DE}$ としてもよい。",
  "ex": r"正六角形 ABCDEF において，$\VV{AB}=\vec a$，$\VV{AC}=\vec b$ とするとき，$\VV{AF}$，$\VV{AD}$ を $\vec a,\ \vec b$ で表せ。",
  "exa": r"$\VV{AF}=-2\vec a+\vec b$，$\VV{AD}=-2\vec a+2\vec b$"},
 {"lv": 2, "title": "1次独立なベクトルの係数比較と平行条件",
  "q": r"$\vec a,\ \vec b$ は $\vec 0$ でなく，平行でないとする。<br>(1) $(s+t-3)\vec a+(2s-t)\vec b=\vec 0$ を満たす実数 $s,\ t$ を求めよ。<br>(2) $\vec p=k\vec a+2\vec b$，$\vec q=3\vec a+(k+5)\vec b$ が平行になるような実数 $k$ の値を求めよ。",
  "hint": r"$\vec a,\ \vec b$ が1次独立なので「$s\vec a+t\vec b=\vec 0\iff s=t=0$」として係数を比較できる。(2) は $\vec q=m\vec p$ とおいて係数を比較する。",
  "sol": r"(1) $\vec a,\ \vec b$ は1次独立だから　$s+t-3=0,\ 2s-t=0$<br>これを解いて　$\boldsymbol{s=1,\ t=2}$<br>"
         r"(2) $\vec p$ の $\vec b$ の係数は $2\neq0$，$\vec q$ の $\vec a$ の係数は $3\neq0$ なので $\vec p\neq\vec 0$，$\vec q\neq\vec 0$。よって $\vec p\parallel\vec q\iff\vec q=m\vec p$ となる実数 $m$ がある。<br>"
         r"$3\vec a+(k+5)\vec b=mk\vec a+2m\vec b$ の係数を比較して　$3=mk,\ k+5=2m$<br>"
         r"$m=\dfrac{k+5}{2}$ を代入して $k(k+5)=6$，$k^2+5k-6=0$，$(k-1)(k+6)=0$<br>"
         r"よって　$\boldsymbol{k=1,\ -6}$　（$k=1$ のとき $\vec q=3\vec p$，$k=-6$ のとき $\vec q=-\dfrac12\vec p$）",
  "note": r"係数比較ができるのは $\vec a,\ \vec b$ が1次独立だからである。例えば $\vec b=2\vec a$ だと (1) の式は $(5s-t-3)\vec a=\vec 0$ となり，$s,\ t$ は1組に決まらない。(2) は「係数の比が等しい」$k:2=3:(k+5)$ と同じ式になる。",
  "ex": r"$\vec a,\ \vec b$ は1次独立とする。(1) $(2s+t-1)\vec a+(s-t+4)\vec b=\vec 0$ を満たす $s,\ t$ を求めよ。(2) $\vec p=(k+1)\vec a+3\vec b$，$\vec q=2\vec a+k\vec b$ が平行になる $k$ を求めよ。",
  "exa": r"(1) $s=-1,\ t=3$　(2) $k=2,\ -3$"},
 {"lv": 3, "title": "正五角形の対角線のベクトル",
  "q": _fig_pent() + r"1辺の長さが1の正五角形 ABCDE において，$\VV{AB}=\vec a$，$\VV{AE}=\vec b$ とし，対角線の長さを $t$ とする。<br>(1) $t$ の値を求めよ。<br>(2) $\VV{AC}$，$\VV{AD}$ を $\vec a,\ \vec b$ で表せ。",
  "hint": r"正五角形では，各辺はそれと向かい合う対角線に平行（BC∥AD，ED∥AC，CD∥BE）で，長さの比は $1:t$。よって $\VV{BC}=\dfrac1t\VV{AD}$ などと書け，$\VV{AC},\ \VV{AD}$ についての連立方程式ができる。",
  "sol": r"正五角形の5頂点は1つの円周上にあり，各辺に対する円周角はすべて $36^\circ$ である。よって $\angle\mathrm{DAC}=\angle\mathrm{ACB}=36^\circ$（錯角が等しい）から AD∥BC。同様に AC∥ED，BE∥CD。向きも考えて<br>"
         r"$\VV{BC}=\dfrac1t\VV{AD}$，$\VV{ED}=\dfrac1t\VV{AC}$，$\VV{CD}=\dfrac1t\VV{BE}=\dfrac1t(\vec b-\vec a)$ ……①<br>"
         r"$\VV{AC}=\vec c$，$\VV{AD}=\vec d$ とおくと<br>"
         r"$\vec c=\vec a+\VV{BC}=\vec a+\dfrac1t\vec d$ ……②，　$\vec d=\vec b+\VV{ED}=\vec b+\dfrac1t\vec c$ ……③<br>"
         r"(1) ③$-$② より $\vec d-\vec c=(\vec b-\vec a)-\dfrac1t(\vec d-\vec c)$，すなわち $\left(1+\dfrac1t\right)(\vec d-\vec c)=\vec b-\vec a$ で　$\vec d-\vec c=\dfrac{t}{t+1}(\vec b-\vec a)$<br>"
         r"一方 ① より $\vec d-\vec c=\VV{CD}=\dfrac1t(\vec b-\vec a)$。$\vec b-\vec a\neq\vec 0$ だから $\dfrac{t}{t+1}=\dfrac1t$，$t^2-t-1=0$。$t>0$ より　$\boldsymbol{t=\dfrac{1+\sqrt5}{2}}$<br>"
         r"(2) ③を②に代入して $\vec c=\vec a+\dfrac1t\vec b+\dfrac1{t^2}\vec c$，$\left(1-\dfrac1{t^2}\right)\vec c=\vec a+\dfrac1t\vec b$。<br>"
         r"$t^2=t+1$ より $1-\dfrac1{t^2}=\dfrac{t^2-1}{t^2}=\dfrac{t}{t^2}=\dfrac1t$ なので $\vec c=t\vec a+\vec b$，すなわち　$\boldsymbol{\VV{AC}=\dfrac{1+\sqrt5}{2}\vec a+\vec b}$<br>"
         r"③に代入して $\vec d=\vec b+\dfrac1t(t\vec a+\vec b)=\vec a+\left(1+\dfrac1t\right)\vec b$。$1+\dfrac1t=\dfrac{t+1}{t}=\dfrac{t^2}{t}=t$ より　$\boldsymbol{\VV{AD}=\vec a+\dfrac{1+\sqrt5}{2}\vec b}$",
  "note": r"$t=\dfrac{1+\sqrt5}{2}$ は黄金比。△ABC（AB＝BC＝1，∠B＝108°）で AC＝$2\cos36^\circ$ だから $\cos36^\circ=\dfrac{1+\sqrt5}{4}$ も得られる。$\VV{AD}$ は，正五角形が A と辺 CD の中点を通る直線に関して対称なことから，$\VV{AC}$ の $\vec a$ と $\vec b$ を入れかえたものと見てもよい。",
  "ex": r"1辺の長さが1の正五角形 ABCDE において，$\VV{AB}=\vec a$，$\VV{AE}=\vec b$ とし，対角線 AC と BE の交点を P とする。$\VV{AP}$ を $\vec a,\ \vec b$ で表せ。",
  "exa": r"$\VV{AP}=\dfrac{\sqrt5-1}{2}\vec a+\dfrac{3-\sqrt5}{2}\vec b$"},
]})

# ================================================================ 節2
SEC.append({"title": "ベクトルの成分",
"base": r"""・$\vec a=(a_1,a_2)$，$\vec b=(b_1,b_2)$ のとき　$s\vec a+t\vec b=(sa_1+tb_1,\ sa_2+tb_2)$，$|\vec a|=\sqrt{a_1^2+a_2^2}$<br>
・A$(a_1,a_2)$，B$(b_1,b_2)$ のとき　$\VV{AB}=(b_1-a_1,\ b_2-a_2)$<br>
・平行条件：$\vec a\neq\vec 0,\ \vec b\neq\vec 0$ のとき　$\vec a\parallel\vec b\iff a_1b_2-a_2b_1=0$<br>
・$\vec a$ と同じ向きの単位ベクトルは $\dfrac{\vec a}{|\vec a|}$，平行な単位ベクトルは $\pm\dfrac{\vec a}{|\vec a|}$""",
"items": [
 {"lv": 1, "title": "成分による演算・大きさ・ベクトルの分解",
  "q": r"$\vec a=(2,-1)$，$\vec b=(-3,4)$ とする。<br>(1) $3\vec a+2\vec b$，$\vec a-\vec b$ の成分と大きさをそれぞれ求めよ。<br>(2) $\vec c=(7,-6)$ を $s\vec a+t\vec b$（$s,\ t$ は実数）の形で表せ。<br>(3) $\vec a$ と同じ向きの単位ベクトルを求めよ。",
  "hint": r"(2) 成分を比較して $s,\ t$ の連立方程式を解く。$\vec a,\ \vec b$ は平行でないので，ただ1通りに表せる。(3) $\vec a$ をその大きさ $|\vec a|$ で割る。",
  "sol": r"(1) $3\vec a+2\vec b=(6-6,\ -3+8)=\boldsymbol{(0,\ 5)}$，大きさ $\boldsymbol{5}$<br>"
         r"$\vec a-\vec b=(2+3,\ -1-4)=\boldsymbol{(5,\ -5)}$，大きさ $\sqrt{25+25}=\boldsymbol{5\sqrt2}$<br>"
         r"(2) $s\vec a+t\vec b=(2s-3t,\ -s+4t)=(7,\ -6)$ より　$2s-3t=7,\ -s+4t=-6$<br>"
         r"これを解いて $s=2,\ t=-1$。よって　$\boldsymbol{\vec c=2\vec a-\vec b}$<br>"
         r"(3) $|\vec a|=\sqrt{4+1}=\sqrt5$ より　$\dfrac{\vec a}{|\vec a|}=\boldsymbol{\left(\dfrac{2\sqrt5}{5},\ -\dfrac{\sqrt5}{5}\right)}$",
  "note": r"(2) で $\vec a,\ \vec b$ が平行だと，表せないか表し方が無数にある。ここでは $2\cdot4-(-1)\cdot(-3)=5\neq0$ なので平行でない。",
  "ex": r"$\vec a=(3,1)$，$\vec b=(-1,2)$ のとき，(1) $2\vec a+\vec b$ の成分と大きさ (2) $\vec c=(1,5)$ を $s\vec a+t\vec b$ の形に表せ (3) $\vec b$ と同じ向きの単位ベクトル を求めよ。",
  "exa": r"(1) $(5,\ 4)$，$\sqrt{41}$　(2) $\vec c=\vec a+2\vec b$　(3) $\left(-\dfrac{\sqrt5}{5},\ \dfrac{2\sqrt5}{5}\right)$"},
 {"lv": 1, "title": "平行条件（成分）と平行な単位ベクトル",
  "q": r"(1) $\vec a=(1,\ x)$，$\vec b=(x+1,\ 6)$ が平行になるような $x$ の値を求めよ。<br>(2) $\vec c=(3,-4)$ に平行な単位ベクトルを求めよ。<br>(3) $\vec d=(2,1)$，$\vec e=(-1,3)$ とする。$\vec d+t\vec e$ が $\vec c$ と平行になるような実数 $t$ の値を求めよ。",
  "hint": r"$\vec a=(a_1,a_2)$，$\vec b=(b_1,b_2)$（ともに $\vec 0$ でない）について　$\vec a\parallel\vec b\iff\vec b=k\vec a\iff a_1b_2-a_2b_1=0$。平行な単位ベクトルは向きが2通りある。",
  "sol": r"(1) $\vec a,\ \vec b$ はともに $\vec 0$ でない。平行条件 $1\cdot6-x(x+1)=0$ より $x^2+x-6=0$，$(x-2)(x+3)=0$　∴ $\boldsymbol{x=2,\ -3}$<br>"
         r"(2) $|\vec c|=\sqrt{9+16}=5$ より　$\pm\dfrac{\vec c}{5}=\boldsymbol{\left(\dfrac35,\ -\dfrac45\right),\ \left(-\dfrac35,\ \dfrac45\right)}$<br>"
         r"(3) $\vec d+t\vec e=(2-t,\ 1+3t)$ は $\vec 0$ にならない（$2-t=0$ と $1+3t=0$ は同時に成り立たない）。よって $\vec c$ と平行になる条件は<br>"
         r"$(2-t)\cdot(-4)-(1+3t)\cdot3=0$，$-11-5t=0$　∴ $\boldsymbol{t=-\dfrac{11}{5}}$　（このとき $\vec d+t\vec e=\left(\dfrac{21}{5},\ -\dfrac{28}{5}\right)=\dfrac75\vec c$）",
  "note": r"(1) で $x=2$ のとき $\vec b=3\vec a$，$x=-3$ のとき $\vec b=-2\vec a$ となる。「$\vec b=k\vec a$ とおいて成分を比較」しても同じ式になる。",
  "ex": r"(1) $\vec a=(x,\ 3)$，$\vec b=(4,\ x+4)$ が平行になる $x$ を求めよ。(2) $\vec c=(-5,12)$ に平行な単位ベクトルを求めよ。(3) $\vec d=(1,2)$，$\vec e=(3,-1)$ のとき，$\vec d+t\vec e$ が $(1,\ 1)$ と平行になる $t$ を求めよ。",
  "exa": r"(1) $x=2,\ -6$　(2) $\pm\left(-\dfrac5{13},\ \dfrac{12}{13}\right)$　(3) $t=\dfrac14$"},
 {"lv": 2, "title": "平行四辺形の頂点（3通りの場合分け）",
  "q": r"3点 A(1, 2)，B(4, 1)，C(5, 5) と点 D を4つの頂点とする平行四辺形がある。点 D の座標を求めよ。",
  "hint": r"「平行四辺形 ABCD」とは書かれていないので，どの2点が向かい合う頂点になるかで3通りに分かれる。四角形 PQRS（この順に頂点）が平行四辺形 $\iff\VV{PQ}=\VV{SR}$。",
  "sol": r"D$(x,\ y)$ とする。$\VV{AB}=(3,-1)$，$\VV{AC}=(4,3)$ は平行でないので A，B，C は一直線上にない。<br>"
         r"(i) 平行四辺形 ABCD のとき：$\VV{AD}=\VV{BC}$ より $(x-1,\ y-2)=(1,\ 4)$　∴ D$(2,\ 6)$<br>"
         r"(ii) 平行四辺形 ABDC のとき：$\VV{BD}=\VV{AC}$ より $(x-4,\ y-1)=(4,\ 3)$　∴ D$(8,\ 4)$<br>"
         r"(iii) 平行四辺形 ADBC のとき：$\VV{AD}=\VV{CB}$ より $(x-1,\ y-2)=(-1,\ -4)$　∴ D$(0,\ -2)$<br>"
         r"以上より　$\boldsymbol{\mathrm{D}(2,\ 6),\ (8,\ 4),\ (0,\ -2)}$",
  "note": r"対角線の中点が一致することから，D の位置ベクトルを $\vec a+\vec c-\vec b$，$\vec b+\vec c-\vec a$，$\vec a+\vec b-\vec c$ と求めてもよい。3つの D は △ABC の各辺に関して「反対側」にでき，△ABC はこの3点を結ぶ三角形の中点三角形になっている。",
  "ex": r"3点 A(−1, 0)，B(3, 2)，C(1, 4) と点 D を4つの頂点とする平行四辺形がある。点 D の座標を求めよ。",
  "exa": r"$(-3,\ 2),\ (5,\ 6),\ (1,\ -2)$"},
 {"lv": 2, "title": r"$|\vec a+t\vec b|$ の最小値（成分）",
  "q": r"$\vec a=(3,1)$，$\vec b=(1,-2)$ とする。実数 $t$ が変化するとき，$|\vec a+t\vec b|$ の最小値と，そのときの $t$ の値を求めよ。",
  "hint": r"大きさは根号を含むので，2乗した $|\vec a+t\vec b|^2$（$t$ の2次関数）の最小を考える。$|\vec a+t\vec b|\geqq0$ なので，2乗が最小になる $t$ でもとの式も最小になる。",
  "sol": r"$\vec a+t\vec b=(3+t,\ 1-2t)$ より<br>"
         r"$|\vec a+t\vec b|^2=(3+t)^2+(1-2t)^2=5t^2+2t+10=5\left(t+\dfrac15\right)^2+\dfrac{49}{5}$<br>"
         r"よって $\boldsymbol{t=-\dfrac15}$ のとき最小で，最小値は　$\sqrt{\dfrac{49}{5}}=\boldsymbol{\dfrac{7\sqrt5}{5}}$",
  "note": r"$\vec a+t\vec b$ を原点 O を始点とするベクトルと見ると，その終点 P は「点 A(3, 1) を通り $\vec b$ に平行な直線」上を動く。最小になるのは OP がこの直線に垂直なときで，実際 $t=-\dfrac15$ のとき $\vec a+t\vec b=\left(\dfrac{14}5,\ \dfrac75\right)$ と $\vec b$ の内積は $\dfrac{14}{5}-\dfrac{14}{5}=0$。最小値は原点とこの直線の距離である。",
  "ex": r"$\vec a=(-1,4)$，$\vec b=(2,1)$ のとき，$|\vec a+t\vec b|$ の最小値とそのときの $t$ の値を求めよ。",
  "exa": r"$t=-\dfrac25$ のとき最小値 $\dfrac{9\sqrt5}{5}$"},
]})

# ================================================================ 節3
SEC.append({"title": "内積・なす角・垂直",
"base": r"""・内積：$\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta$（$\theta$ は $\vec a,\ \vec b$ のなす角，$0^\circ\leqq\theta\leqq180^\circ$，始点をそろえて測る）。成分では $\vec a\cdot\vec b=a_1b_1+a_2b_2$<br>
・$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}$，垂直条件：$\vec a\neq\vec 0,\ \vec b\neq\vec 0$ のとき　$\vec a\perp\vec b\iff\vec a\cdot\vec b=0$<br>
・$|\vec a|^2=\vec a\cdot\vec a$，$|\vec a+\vec b|^2=|\vec a|^2+2\vec a\cdot\vec b+|\vec b|^2$（大きさは2乗して内積の計算にする）""",
"items": [
 {"lv": 1, "title": "内積の計算となす角",
  "q": r"(1) $\vec a=(2,1)$，$\vec b=(1,3)$ の内積と，なす角 $\theta$ を求めよ。<br>(2) 1辺の長さが2の正三角形 ABC において，内積 $\VV{AB}\cdot\VV{AC}$，$\VV{AB}\cdot\VV{BC}$ を求めよ。",
  "hint": r"(1) 成分で内積を計算し，$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}$。(2) なす角は2つのベクトルの<b>始点をそろえて</b>測る。",
  "sol": r"(1) $\vec a\cdot\vec b=2\cdot1+1\cdot3=\boldsymbol{5}$。$|\vec a|=\sqrt5$，$|\vec b|=\sqrt{10}$ より $\cos\theta=\dfrac{5}{\sqrt5\sqrt{10}}=\dfrac{1}{\sqrt2}$。$0^\circ\leqq\theta\leqq180^\circ$ より　$\boldsymbol{\theta=45^\circ}$<br>"
         r"(2) $\VV{AB}$ と $\VV{AC}$ のなす角は $60^\circ$ なので　$\VV{AB}\cdot\VV{AC}=2\cdot2\cos60^\circ=\boldsymbol{2}$<br>"
         r"$\VV{BC}$ を平行移動して始点を A にそろえると，$\VV{AB}$ とのなす角は $180^\circ-60^\circ=120^\circ$。よって　$\VV{AB}\cdot\VV{BC}=2\cdot2\cos120^\circ=\boldsymbol{-2}$",
  "note": r"(2) で $\angle\mathrm{B}=60^\circ$ をそのまま使って $2$ とするのは典型的な誤り。$\VV{AB}\cdot\VV{BC}=-\VV{BA}\cdot\VV{BC}$ と書き直せば始点が B にそろい，$-2\cdot2\cos60^\circ=-2$ と計算できる。",
  "ex": r"(1) $\vec a=(3,1)$，$\vec b=(-2,1)$ の内積となす角を求めよ。(2) 1辺の長さが1の正六角形 ABCDEF において，$\VV{AB}\cdot\VV{AC}$，$\VV{AB}\cdot\VV{CD}$ を求めよ。",
  "exa": r"(1) $\vec a\cdot\vec b=-5$，$\theta=135^\circ$　(2) $\dfrac32,\ -\dfrac12$"},
 {"lv": 1, "title": "垂直条件と垂直な単位ベクトル",
  "q": r"(1) $\vec a=(x,\ 2)$，$\vec b=(x-3,\ x)$ が垂直になるような $x$ の値を求めよ。<br>(2) $\vec c=(3,-4)$ に垂直な単位ベクトルを求めよ。",
  "hint": r"$\vec 0$ でない2つのベクトルが垂直 $\iff$ 内積が 0。(2) 求めるベクトルを $(p,\ q)$ とおき，「内積 0」「大きさ 1」の連立方程式を解く。",
  "sol": r"(1) $\vec a$ は $y$ 成分が 2 なので $\vec 0$ でなく，$\vec b=\vec 0$ となるのは $x=3$ かつ $x=0$ のときで起こらない。よって<br>"
         r"$\vec a\perp\vec b\iff\vec a\cdot\vec b=x(x-3)+2x=x^2-x=0$　∴ $\boldsymbol{x=0,\ 1}$<br>"
         r"(2) 求めるベクトルを $(p,\ q)$ とすると　$3p-4q=0$，$p^2+q^2=1$<br>"
         r"$q=\dfrac34p$ を代入して $\dfrac{25}{16}p^2=1$，$p=\pm\dfrac45$。∴ $\boldsymbol{\left(\dfrac45,\ \dfrac35\right),\ \left(-\dfrac45,\ -\dfrac35\right)}$",
  "note": r"$(a_1,\ a_2)$ に垂直なベクトルの1つは $(a_2,\ -a_1)$（内積が $a_1a_2-a_2a_1=0$）。(2) なら $(-4,\ -3)$ を大きさ 5 で割って $\pm\left(\dfrac45,\ \dfrac35\right)$ とすぐ求まる。",
  "ex": r"(1) $\vec a=(x,\ -1)$，$\vec b=(x+1,\ 6)$ が垂直になる $x$ を求めよ。(2) $\vec c=(5,\ 12)$ に垂直な単位ベクトルを求めよ。",
  "exa": r"(1) $x=2,\ -3$　(2) $\pm\left(\dfrac{12}{13},\ -\dfrac5{13}\right)$"},
 {"lv": 2, "title": "大きさの条件から内積・なす角を求める",
  "q": r"$|\vec a|=2$，$|\vec b|=3$，$|\vec a-\vec b|=\sqrt7$ のとき，次のものを求めよ。<br>(1) $\vec a\cdot\vec b$ と，$\vec a,\ \vec b$ のなす角 $\theta$　(2) $|2\vec a+\vec b|$<br>(3) $\vec a+t\vec b$ と $\vec a-\vec b$ が垂直になるような実数 $t$",
  "hint": r"大きさの条件は2乗して内積の式にする：$|\vec a-\vec b|^2=|\vec a|^2-2\vec a\cdot\vec b+|\vec b|^2$。$|\vec a|,\ |\vec b|,\ \vec a\cdot\vec b$ の3つがわかれば，どんな $|s\vec a+t\vec b|$ や内積も計算できる。",
  "sol": r"(1) $|\vec a-\vec b|^2=7$ より $4-2\vec a\cdot\vec b+9=7$　∴ $\boldsymbol{\vec a\cdot\vec b=3}$<br>"
         r"$\cos\theta=\dfrac{3}{2\cdot3}=\dfrac12$ より　$\boldsymbol{\theta=60^\circ}$<br>"
         r"(2) $|2\vec a+\vec b|^2=4|\vec a|^2+4\vec a\cdot\vec b+|\vec b|^2=16+12+9=37$　∴ $|2\vec a+\vec b|=\boldsymbol{\sqrt{37}}$<br>"
         r"(3) $(\vec a+t\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-\vec a\cdot\vec b+t\vec a\cdot\vec b-t|\vec b|^2=4-3+3t-9t=1-6t$<br>"
         r"$\vec a,\ \vec b$ は平行でないから $\vec a+t\vec b\neq\vec 0$，$\vec a-\vec b\neq\vec 0$。よって垂直 $\iff1-6t=0$　∴ $\boldsymbol{t=\dfrac16}$",
  "note": r"(1) は △OAB（OA＝2，OB＝3，AB＝$\sqrt7$）に余弦定理を使うのと同じ計算である。垂直条件を使うときは，両方のベクトルが $\vec 0$ でないことを確認しておく。",
  "ex": r"$|\vec a|=3$，$|\vec b|=1$，$|\vec a+\vec b|=\sqrt7$ のとき，(1) $\vec a\cdot\vec b$ となす角 (2) $|\vec a-2\vec b|$ (3) $\vec a+t\vec b$ と $\vec b$ が垂直になる $t$ を求めよ。",
  "exa": r"(1) $\vec a\cdot\vec b=-\dfrac32$，$120^\circ$　(2) $\sqrt{19}$　(3) $t=\dfrac32$"},
 {"lv": 3, "title": r"$\vec a+\vec b+\vec c=\vec 0$ の条件と内積",
  "q": r"$\vec a+\vec b+\vec c=\vec 0$，$|\vec a|=3$，$|\vec b|=5$，$|\vec c|=7$ のとき，次のものを求めよ。<br>(1) $\vec a,\ \vec b$ のなす角　(2) $\vec a\cdot\vec b+\vec b\cdot\vec c+\vec c\cdot\vec a$<br>(3) $\vec a,\ \vec c$ のなす角を $\theta$ とするときの $\cos\theta$",
  "hint": r"1つのベクトルを消去して $\vec c=-(\vec a+\vec b)$ とし，両辺の大きさを2乗すれば $\vec a\cdot\vec b$ が出る。(2) は $|\vec a+\vec b+\vec c|^2=0$ を展開する。",
  "sol": r"(1) $\vec c=-(\vec a+\vec b)$ の両辺の大きさを2乗して $|\vec c|^2=|\vec a|^2+2\vec a\cdot\vec b+|\vec b|^2$<br>"
         r"$49=9+2\vec a\cdot\vec b+25$　∴ $\vec a\cdot\vec b=\dfrac{15}{2}$。$\cos=\dfrac{15}{2}\div(3\cdot5)=\dfrac12$ より，なす角は $\boldsymbol{60^\circ}$<br>"
         r"(2) $|\vec a+\vec b+\vec c|^2=0$ を展開して $|\vec a|^2+|\vec b|^2+|\vec c|^2+2(\vec a\cdot\vec b+\vec b\cdot\vec c+\vec c\cdot\vec a)=0$<br>"
         r"∴ $\vec a\cdot\vec b+\vec b\cdot\vec c+\vec c\cdot\vec a=-\dfrac{9+25+49}{2}=\boldsymbol{-\dfrac{83}{2}}$<br>"
         r"(3) $\vec b=-(\vec a+\vec c)$ より $25=9+2\vec a\cdot\vec c+49$，$\vec a\cdot\vec c=-\dfrac{33}{2}$<br>"
         r"∴ $\cos\theta=-\dfrac{33}{2}\div(3\cdot7)=\boldsymbol{-\dfrac{11}{14}}$",
  "note": r"和が $\vec 0$ なので，$\vec a,\ \vec b,\ \vec c$ を順につなぐと3辺が 3，5，7 の三角形ができる。(1) の $60^\circ$ は，長さ 7 の辺の対角 $120^\circ$ の外角である（なす角は始点をそろえて測るので，三角形の内角とは限らない）。",
  "ex": r"$\vec a+\vec b+\vec c=\vec 0$，$|\vec a|=2$，$|\vec b|=3$，$|\vec c|=4$ のとき，(1) $\vec a,\ \vec b$ のなす角を $\theta$ として $\cos\theta$ (2) $\vec a\cdot\vec b+\vec b\cdot\vec c+\vec c\cdot\vec a$ を求めよ。",
  "exa": r"(1) $\cos\theta=\dfrac14$　(2) $-\dfrac{29}{2}$"},
 {"lv": 3, "title": "内積の等式と三角形の形状（証明）",
  "q": r"△ABC において $\VV{AB}\cdot\VV{BC}=\VV{BC}\cdot\VV{CA}=\VV{CA}\cdot\VV{AB}$ が成り立つとき，△ABC は正三角形であることを示せ。",
  "hint": r"$\vec x=\VV{AB}$，$\vec y=\VV{BC}$，$\vec z=\VV{CA}$ とおくと $\vec x+\vec y+\vec z=\vec 0$。$|\vec x|^2=\vec x\cdot\vec x$ の一方の $\vec x$ を $-\vec y-\vec z$ に置きかえると，与えられた内積だけで表せる。",
  "sol": r"$\vec x=\VV{AB}$，$\vec y=\VV{BC}$，$\vec z=\VV{CA}$ とおくと $\vec x+\vec y+\vec z=\VV{AA}=\vec 0$。条件の共通の値を $k$ とすると $\vec x\cdot\vec y=\vec y\cdot\vec z=\vec z\cdot\vec x=k$。<br>"
         r"$|\vec x|^2=\vec x\cdot\vec x=\vec x\cdot(-\vec y-\vec z)=-\vec x\cdot\vec y-\vec z\cdot\vec x=-2k$<br>"
         r"$|\vec y|^2=\vec y\cdot(-\vec x-\vec z)=-\vec x\cdot\vec y-\vec y\cdot\vec z=-2k$<br>"
         r"$|\vec z|^2=\vec z\cdot(-\vec x-\vec y)=-\vec z\cdot\vec x-\vec y\cdot\vec z=-2k$<br>"
         r"よって $|\vec x|=|\vec y|=|\vec z|$，すなわち AB＝BC＝CA で，△ABC は正三角形である。■",
  "note": r"逆に1辺 $l$ の正三角形なら3つの内積はすべて $l^2\cos120^\circ=-\dfrac{l^2}{2}$ で等しい（上の式で $k=-\dfrac{l^2}{2}$）。辺をベクトルで表し，「和が $\vec 0$」を使って内積の関係を辺の長さに直すのが定石。",
  "ex": r"△ABC において $\VV{AB}\cdot\VV{AC}=\VV{BA}\cdot\VV{BC}$ ならば，△ABC は CA＝CB の二等辺三角形であることを示せ。",
  "exa": r"移項すると $\VV{AB}\cdot(\VV{AC}+\VV{BC})=0$。辺 AB の中点を M とすると $\VV{AC}+\VV{BC}=2\VV{MC}$ なので MC⊥AB，よって C は AB の垂直二等分線上にあり CA＝CB。"},
]})

# ================================================================ 節4
def _fig_circ_dot():
    s = 32
    T = _tr(61, 91, s)
    b = _ar(T((-1.6, 0)), T((4.6, 0)), "#999", 0.8, 5) + _ar(T((0, -1.4)), T((0, 2.6)), "#999", 0.8, 5)
    b += _lab(T((4.6, 0)), "x", -90, 8, 10, "#666") + _lab(T((0, 2.6)), "y", 0, 8, 10, "#666")
    b += _cir(T((0, 0)), s)
    A, B, M = (4, 0), (0, 2), (2, 1)
    th = math.radians(140)
    P = (math.cos(th), math.sin(th))
    b += _ln(T(A), T(B), "#333", 1.0)
    b += _ln(T(P), T(A), BL, 1.1) + _ln(T(P), T(B), BL, 1.1) + _ln(T(P), T(M), RD, 1.1, "3,2")
    r5 = math.sqrt(5)
    b += _ln(T((-2/r5, -1/r5)), T(M), "#888", 0.8, "2,2")
    for Q, nm, an in ((A, "A", -60), (B, "B", 180), (M, "M", 60), (P, "P", 150), ((0, 0), "O", -135)):
        b += _dot(T(Q)) + _lab(T(Q), nm, an, 9, 10)
    return _svg(218, 144, b)

def _fig_inscribed():
    s = 58
    T = _tr(72, 76, s)
    pt = {k: (math.cos(math.radians(g)), math.sin(math.radians(g))) for k, g in (("A", 100), ("B", 205), ("C", 330))}
    M = ((pt["B"][0] + pt["C"][0]) / 2, (pt["B"][1] + pt["C"][1]) / 2)
    b = _cir(T((0, 0)), s, "#666", 0.9)
    b += _pg([T(pt[k]) for k in "ABC"], "none", "#333", 1.1)
    b += _ln(T((0, 0)), T(M), RD, 1.0, "3,2") + _ln(T(pt["A"]), T(M), BL, 1.0, "3,2")
    for k, v in pt.items():
        b += _dot(T(v)) + _lab(T(v), k, _away(T(v), T((0, 0))), 9, 10)
    b += _dot(T((0, 0))) + _lab(T((0, 0)), "O", 160, 9, 10) + _dot(T(M)) + _lab(T(M), "M", -80, 9, 10)
    return _svg(146, 148, b)

SEC.append({"title": "三角形の面積と内積の最大・最小",
"base": r"""・△OAB の面積：$S=\dfrac12\sqrt{|\vec a|^2|\vec b|^2-(\vec a\cdot\vec b)^2}$（$\vec a=\VV{OA},\ \vec b=\VV{OB}$）。成分で $\vec a=(a_1,a_2)$，$\vec b=(b_1,b_2)$ なら　$S=\dfrac12|a_1b_2-a_2b_1|$<br>
・$-|\vec a||\vec b|\leqq\vec a\cdot\vec b\leqq|\vec a||\vec b|$（等号は $\vec a,\ \vec b$ が同じ向き・逆向きのとき，または一方が $\vec 0$ のとき）<br>
・中点の利用：M が線分 AB の中点なら　$\VV{PA}\cdot\VV{PB}=|\VV{PM}|^2-|\VV{MA}|^2$<br>
・動点を含む内積は，動点を1つの文字で表して関数の最大・最小にするか，上の変形で「距離」の問題にする""",
"items": [
 {"lv": 1, "title": "ベクトルによる三角形の面積",
  "q": r"(1) 3点 A(1, 1)，B(4, 2)，C(2, 5) を頂点とする △ABC の面積を求めよ。<br>(2) $|\vec a|=3$，$|\vec b|=4$，$\vec a\cdot\vec b=6$ のとき，$\VV{OA}=\vec a$，$\VV{OB}=\vec b$ である △OAB の面積を求めよ。",
  "hint": r"面積公式 $S=\dfrac12\sqrt{|\vec a|^2|\vec b|^2-(\vec a\cdot\vec b)^2}$ は，$S=\dfrac12|\vec a||\vec b|\sin\theta$ に $\sin\theta=\sqrt{1-\cos^2\theta}$，$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}$ を代入したもの。成分なら $\dfrac12|a_1b_2-a_2b_1|$ が速い。",
  "sol": r"(1) $\VV{AB}=(3,\ 1)$，$\VV{AC}=(1,\ 4)$ より　$\triangle\mathrm{ABC}=\dfrac12|3\cdot4-1\cdot1|=\boldsymbol{\dfrac{11}{2}}$<br>"
         r"(2) $\triangle\mathrm{OAB}=\dfrac12\sqrt{3^2\cdot4^2-6^2}=\dfrac12\sqrt{108}=\boldsymbol{3\sqrt3}$",
  "note": r"成分の公式は $|\vec a|^2|\vec b|^2-(\vec a\cdot\vec b)^2=(a_1^2+a_2^2)(b_1^2+b_2^2)-(a_1b_1+a_2b_2)^2=(a_1b_2-a_2b_1)^2$ から導かれる。(2) では $\cos\theta=\dfrac{6}{12}=\dfrac12$ より $\theta=60^\circ$，$S=\dfrac12\cdot3\cdot4\sin60^\circ$ としても同じ。",
  "ex": r"(1) A(−1, 2)，B(3, −1)，C(2, 4) を頂点とする △ABC の面積を求めよ。(2) $|\vec a|=2$，$|\vec b|=5$，$\vec a\cdot\vec b=-6$ のとき △OAB の面積を求めよ。",
  "exa": r"(1) $\dfrac{17}{2}$　(2) $4$"},
 {"lv": 2, "title": "線分上を動く点と内積の最大・最小",
  "q": r"1辺の長さが2の正三角形 ABC の辺 BC 上（両端を含む）を点 P が動くとき，内積 $\VV{PA}\cdot\VV{PB}$ の最大値と最小値を求めよ。",
  "hint": r"動点 P を1つの文字で表す：$\VV{BP}=k\VV{BC}$（$0\leqq k\leqq1$）。始点を B にそろえると，内積は $k$ の2次関数になるので，定義域 $0\leqq k\leqq1$ での最大・最小を調べる。",
  "sol": r"$\VV{BP}=k\VV{BC}$（$0\leqq k\leqq1$）とおく。$\vec u=\VV{BA}$，$\vec v=\VV{BC}$ とすると $|\vec u|=|\vec v|=2$，$\vec u\cdot\vec v=2\cdot2\cos60^\circ=2$。<br>"
         r"$\VV{PA}=\vec u-k\vec v$，$\VV{PB}=-k\vec v$ より<br>"
         r"$\VV{PA}\cdot\VV{PB}=-k\vec u\cdot\vec v+k^2|\vec v|^2=4k^2-2k=4\left(k-\dfrac14\right)^2-\dfrac14$<br>"
         r"$0\leqq k\leqq1$ において，$k=1$ で最大，$k=\dfrac14$ で最小となる。<br>"
         r"よって　最大値 $\boldsymbol{2}$（P が C に一致するとき），最小値 $\boldsymbol{-\dfrac14}$（BP$=\dfrac12$ のとき）",
  "note": r"中点を使う別解：辺 AB の中点を M とすると $\VV{PA}\cdot\VV{PB}=\mathrm{PM}^2-\mathrm{MA}^2=\mathrm{PM}^2-1$。PM が最小になるのは P が M から BC に下ろした垂線の足のとき（PM$=\dfrac{\sqrt3}{2}$），最大は P＝C のとき（PM$=\sqrt3$）で，$\dfrac34-1=-\dfrac14$，$3-1=2$ と同じ結果になる。",
  "ex": r"1辺の長さが2の正方形 ABCD の辺 CD 上（両端を含む）を点 P が動くとき，$\VV{PA}\cdot\VV{PC}$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $0$（P が C または D のとき），最小値 $-1$（P が辺 CD の中点のとき）"},
 {"lv": 3, "title": "円周上を動く点と内積（中点の利用）",
  "q": _fig_circ_dot() + r"座標平面上に2点 A(4, 0)，B(0, 2) がある。点 P が円 $x^2+y^2=1$ 上を動くとき，内積 $\VV{PA}\cdot\VV{PB}$ の最大値と最小値を求めよ。",
  "hint": r"2つのベクトルの始点 P が共通で，終点 A，B が定点。AB の中点 M を使うと $\VV{PA}\cdot\VV{PB}=\mathrm{PM}^2-\mathrm{MA}^2$ となり，「円周上の点と定点 M の距離」の問題になる。",
  "sol": r"線分 AB の中点を M(2, 1) とする。$\VV{PA}=\VV{PM}+\VV{MA}$，$\VV{PB}=\VV{PM}+\VV{MB}=\VV{PM}-\VV{MA}$ より<br>"
         r"$\VV{PA}\cdot\VV{PB}=|\VV{PM}|^2-|\VV{MA}|^2=\mathrm{PM}^2-5$<br>"
         r"OM$=\sqrt5>1$ なので M は円の外部にあり，円周上の点 P について $\mathrm{OM}-1\leqq\mathrm{PM}\leqq\mathrm{OM}+1$。左の等号は P が線分 OM と円の交点のとき，右の等号は P が直線 OM と円の交点のうち M と反対側の点のときに成り立つ。<br>"
         r"よって $\sqrt5-1\leqq\mathrm{PM}\leqq\sqrt5+1$ で<br>"
         r"最大値 $(\sqrt5+1)^2-5=\boldsymbol{1+2\sqrt5}$　$\left(\mathrm{P}\left(-\dfrac{2}{\sqrt5},\ -\dfrac{1}{\sqrt5}\right)\right)$<br>"
         r"最小値 $(\sqrt5-1)^2-5=\boldsymbol{1-2\sqrt5}$　$\left(\mathrm{P}\left(\dfrac{2}{\sqrt5},\ \dfrac{1}{\sqrt5}\right)\right)$",
  "note": r"別解：P$(\cos\theta,\ \sin\theta)$ とおくと $\VV{PA}\cdot\VV{PB}=(4-\cos\theta)(-\cos\theta)+(-\sin\theta)(2-\sin\theta)=1-4\cos\theta-2\sin\theta$。三角関数の合成で $-2\sqrt5\leqq-4\cos\theta-2\sin\theta\leqq2\sqrt5$ となり同じ結果。中点を使う方法は，P が線分や多角形の周を動くときにもそのまま使える。",
  "ex": r"2点 A(3, 0)，B(1, 4) と，円 $x^2+y^2=2$ 上を動く点 P について，$\VV{PA}\cdot\VV{PB}$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $13$，最小値 $-3$"},
 {"lv": 3, "title": "内積を利用した不等式と最大・最小",
  "q": r"(1) 実数 $a,\ b,\ x,\ y$ に対して，不等式 $(ax+by)^2\leqq(a^2+b^2)(x^2+y^2)$ が成り立つことを，ベクトルの内積を用いて示せ。また，等号が成り立つ条件を求めよ。<br>(2) 実数 $x,\ y$ が $x^2+2y^2=6$ を満たすとき，$x+2y$ の最大値と最小値を求めよ。",
  "hint": r"(1) $\vec u=(a,\ b)$，$\vec v=(x,\ y)$ とおくと，左辺は $(\vec u\cdot\vec v)^2$，右辺は $|\vec u|^2|\vec v|^2$。(2) $x+2y$ を内積とみる。条件の左辺が $|\vec u|^2$ になるように $\vec u=(x,\ \sqrt2y)$ と選ぶのがポイント。",
  "sol": r"(1) $\vec u=(a,\ b)$，$\vec v=(x,\ y)$ とおく。一方が $\vec 0$ なら両辺とも 0 で成り立つ。どちらも $\vec 0$ でないとき，なす角を $\theta$ とすると<br>"
         r"$(\vec u\cdot\vec v)^2=|\vec u|^2|\vec v|^2\cos^2\theta\leqq|\vec u|^2|\vec v|^2$<br>"
         r"すなわち $(ax+by)^2\leqq(a^2+b^2)(x^2+y^2)$。等号は $\cos\theta=\pm1$（$\vec u\parallel\vec v$）のときで，一方が $\vec 0$ の場合も含めて，等号成立条件は　$\boldsymbol{ay=bx}$<br>"
         r"(2) $\vec u=(x,\ \sqrt2y)$，$\vec v=(1,\ \sqrt2)$ とおくと $\vec u\cdot\vec v=x+2y$，$|\vec u|^2=x^2+2y^2=6$，$|\vec v|^2=3$。<br>"
         r"(1) より $(x+2y)^2\leqq6\cdot3=18$，よって $-3\sqrt2\leqq x+2y\leqq3\sqrt2$。<br>"
         r"等号は $\vec u=k\vec v$，すなわち $x=k,\ y=k$ のときで，$x^2+2y^2=3k^2=6$ より $k=\pm\sqrt2$。<br>"
         r"よって　$x=y=\sqrt2$ のとき最大値 $\boldsymbol{3\sqrt2}$，$x=y=-\sqrt2$ のとき最小値 $\boldsymbol{-3\sqrt2}$",
  "note": r"(1) はコーシー・シュワルツの不等式。(2) の別解（判別式）：$x+2y=k$ とおき $x=k-2y$ を代入すると $6y^2-4ky+k^2-6=0$。$y$ が実数である条件 $\dfrac{D}{4}=4k^2-6(k^2-6)=36-2k^2\geqq0$ より $k^2\leqq18$。最大・最小をとる $x,\ y$ を必ず確認すること。",
  "ex": r"実数 $x,\ y$ が $x^2+3y^2=4$ を満たすとき，$x+y$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $\dfrac{4\sqrt3}{3}$（$x=\sqrt3,\ y=\dfrac{\sqrt3}{3}$），最小値 $-\dfrac{4\sqrt3}{3}$（$x=-\sqrt3,\ y=-\dfrac{\sqrt3}{3}$）"},
 {"lv": 4, "title": "大きさの条件から内積のとり得る範囲を求める",
  "q": r"平面上のベクトル $\vec a,\ \vec b$ が $|\vec a+2\vec b|=2$，$|2\vec a-\vec b|=1$ を満たしながら動くとき，内積 $\vec a\cdot\vec b$ の最大値と最小値を求めよ。",
  "hint": r"条件に現れるベクトル $\vec u=\vec a+2\vec b$，$\vec v=2\vec a-\vec b$ を新しい変数にすると，条件は「$|\vec u|=2,\ |\vec v|=1$」で，$\vec u,\ \vec v$ の向きは互いに無関係に選べる。$\vec a,\ \vec b$ を $\vec u,\ \vec v$ で表し，$\vec a\cdot\vec b$ を $\vec u\cdot\vec v$ だけの式にする。",
  "sol": r"$\vec u=\vec a+2\vec b$，$\vec v=2\vec a-\vec b$ とおくと，$\vec u+2\vec v=5\vec a$，$2\vec u-\vec v=5\vec b$ より<br>"
         r"$\vec a=\dfrac{\vec u+2\vec v}{5}$，$\vec b=\dfrac{2\vec u-\vec v}{5}$<br>"
         r"逆に，$|\vec u|=2$，$|\vec v|=1$ を満たす任意の $\vec u,\ \vec v$ に対し，こう定めた $\vec a,\ \vec b$ は条件を満たす。よって $\vec u,\ \vec v$ は「$|\vec u|=2,\ |\vec v|=1$」の範囲を自由に動く。<br>"
         r"$\vec a\cdot\vec b=\dfrac{(\vec u+2\vec v)\cdot(2\vec u-\vec v)}{25}=\dfrac{2|\vec u|^2+3\vec u\cdot\vec v-2|\vec v|^2}{25}=\dfrac{6+3\vec u\cdot\vec v}{25}$<br>"
         r"$\vec u,\ \vec v$ のなす角を $\theta$ とすると $\vec u\cdot\vec v=2\cos\theta$ は $-2$ 以上 $2$ 以下のすべての値をとる。<br>"
         r"よって，$\vec u\cdot\vec v=2$（$\vec u,\ \vec v$ が同じ向き）のとき最大値 $\boldsymbol{\dfrac{12}{25}}$，$\vec u\cdot\vec v=-2$（逆向き）のとき最小値 $\boldsymbol{0}$",
  "note": r"「$\vec a,\ \vec b$ のなす角」を直接の変数にすると $|\vec a|,\ |\vec b|$ も同時に変わるので扱いにくい。条件式のベクトルを「独立に動ける変数」に取りかえるのがコツ。例えば最大のときは $\vec u=(2,0)$，$\vec v=(1,0)$ で $\vec a=\left(\dfrac45,\ 0\right)$，$\vec b=\left(\dfrac35,\ 0\right)$，最小のときは $\vec v=(-1,0)$ で $\vec a=\vec 0$，$\vec b=(1,\ 0)$ となる。",
  "ex": r"$|\vec a+\vec b|=2$，$|\vec a-2\vec b|=1$ を満たすベクトル $\vec a,\ \vec b$ について，$\vec a\cdot\vec b$ の最大値と最小値を求めよ。",
  "exa": r"最大値 $1$，最小値 $\dfrac59$"},
 {"lv": 5, "title": "円に内接する三角形の内積のとり得る値の範囲",
  "q": _fig_inscribed() + r"半径1の円に内接する三角形 ABC について，内積 $\VV{AB}\cdot\VV{AC}$ のとり得る値の範囲を求めよ。",
  "hint": r"円の中心 O を始点にとり，辺 BC の中点 M を使って $\VV{AB}\cdot\VV{AC}=\mathrm{AM}^2-\mathrm{MB}^2$ と変形する。まず B，C を固定して（$m=\mathrm{OM}$ を固定して）A を動かし，次に $m$ を動かす「2段階の評価」。最後に，範囲の端が実際にとれるか，間の値がすべてとれるかを確かめる。",
  "sol": r"円の中心を O とし，$\vec a=\VV{OA}$，$\vec b=\VV{OB}$，$\vec c=\VV{OC}$（$|\vec a|=|\vec b|=|\vec c|=1$）とする。辺 BC の中点を M，$\vec m=\VV{OM}=\dfrac{\vec b+\vec c}{2}$，$m=|\vec m|$ とおく。<br>"
         r"<b>[1] 内積の変形</b>　$\vec b-\vec m=\dfrac{\vec b-\vec c}{2}=-(\vec c-\vec m)$ だから<br>"
         r"$\VV{AB}\cdot\VV{AC}=\{(\vec m-\vec a)+(\vec b-\vec m)\}\cdot\{(\vec m-\vec a)-(\vec b-\vec m)\}=|\vec m-\vec a|^2-|\vec b-\vec m|^2$<br>"
         r"また $|\vec b-\vec m|^2=\dfrac{2-2\vec b\cdot\vec c}{4}$，$m^2=\dfrac{2+2\vec b\cdot\vec c}{4}$ より $|\vec b-\vec m|^2=1-m^2$。よって<br>"
         r"$\VV{AB}\cdot\VV{AC}=\mathrm{AM}^2-1+m^2$ ……①<br>"
         r"B≠C より $\vec b\cdot\vec c<1$ なので　$0\leqq m<1$<br>"
         r"<b>[2] 評価</b>　$|\vec a|=1$ より $1-m\leqq\mathrm{AM}\leqq1+m$ なので，①から　$2m^2-2m\leqq\VV{AB}\cdot\VV{AC}\leqq2m^2+2m$<br>"
         r"ここで $2m^2-2m=2\left(m-\dfrac12\right)^2-\dfrac12\geqq-\dfrac12$，$2m^2+2m<2+2=4$（$m<1$）。ゆえに<br>"
         r"$-\dfrac12\leqq\VV{AB}\cdot\VV{AC}<4$ ……②<br>"
         r"<b>[3] すべての値をとること</b>　O を原点とする座標で A(0, 1)，B$(-\sin\varphi,\ \cos\varphi)$，C$(\sin\varphi,\ \cos\varphi)$（$0<\varphi<\pi$）とすると，三角形 ABC は円に内接し<br>"
         r"$\VV{AB}\cdot\VV{AC}=-\sin^2\varphi+(\cos\varphi-1)^2=2\cos^2\varphi-2\cos\varphi$<br>"
         r"$x=\cos\varphi$ は $-1<x<1$ のすべての値をとり，$f(x)=2x^2-2x$ は $-1<x\leqq\dfrac12$ で連続かつ減少，$f\left(\dfrac12\right)=-\dfrac12$，$x\to-1$ のとき $f(x)\to4$。よって②の範囲のすべての値をとる。<br>"
         r"以上より　$\boldsymbol{-\dfrac12\leqq\VV{AB}\cdot\VV{AC}<4}$",
  "note": r"最小になるのは $m=\dfrac12$ で A が M の側（短い方の弧 BC の中点）にあるときで，AB＝AC＝1，∠A＝120° の二等辺三角形（$1\cdot1\cos120^\circ=-\dfrac12$）。上限の 4 は B，C が1点に近づき A がその反対側に近づく極限で，三角形にならないので達しない。正弦定理から $\VV{AB}\cdot\VV{AC}=4\sin B\sin C\cos A$ と書いて考えることもできる。「固定して動かす」評価と，「範囲の端が実際にとれるか」の確認が，最難関の答案で差がつくところ。",
  "ex": r"半径1の円に内接する三角形 ABC について，$\VV{AB}\cdot\VV{AC}+\VV{BC}\cdot\VV{BA}+\VV{CA}\cdot\VV{CB}$ のとり得る値の範囲を求めよ。",
  "exa": r"$0$ より大きく $\dfrac92$ 以下（O を始点として，与式 $=\dfrac{\mathrm{AB}^2+\mathrm{BC}^2+\mathrm{CA}^2}{2}=\dfrac{9-|\vec a+\vec b+\vec c|^2}{2}$。最大は正三角形のとき）"},
]})

# ================================================================ 節5
def _mix(P, Q, k):
    """P から Q へ k の位置（P + k(Q-P)）"""
    return (P[0] + k*(Q[0] - P[0]), P[1] + k*(Q[1] - P[1]))

def _meet(P1, P2, Q1, Q2):
    """直線 P1P2 と Q1Q2 の交点"""
    d1 = (P2[0] - P1[0], P2[1] - P1[1]); d2 = (Q2[0] - Q1[0], Q2[1] - Q1[1])
    det = d1[0]*(-d2[1]) - d1[1]*(-d2[0])
    rx, ry = Q1[0] - P1[0], Q1[1] - P1[1]
    lam = (rx*(-d2[1]) - ry*(-d2[0])) / det
    return (P1[0] + lam*d1[0], P1[1] + lam*d1[1])

def _fig_menelaus():
    T = _tr(12, 117, 44)
    A, B, C = (0.8, 2.2), (0, 0), (2.4, 0)
    F = (4.8, 0); D = _mix(A, B, 1/3); E = _mix(A, C, 0.5)
    b = _pg([T(A), T(B), T(C)]) + _ln(T(C), T(F), "#333", 1.0, "3,2")
    b += _ln(T(D), T(F), RD, 1.2)
    for P, nm, an in ((A, "A", 90), (B, "B", 225), (C, "C", -90), (D, "D", 160), (E, "E", 45), (F, "F", -90)):
        b += _dot(T(P)) + _lab(T(P), nm, an, 9, 10)
    return _svg(235, 130, b)

def _fig_cross():
    T = _tr(14, 136, 48)
    O, A, B = (0, 0), (3.2, 0), (1.0, 2.4)
    C = _mix(O, A, 2/3); D = _mix(O, B, 3/5)
    P = (4/9*A[0] + 1/3*B[0], 4/9*A[1] + 1/3*B[1]); Q = (4/7*A[0] + 3/7*B[0], 4/7*A[1] + 3/7*B[1])
    b = _pg([T(O), T(A), T(B)]) + _ln(T(A), T(D), BL, 1.1) + _ln(T(B), T(C), BL, 1.1)
    b += _ln(T(O), T(Q), RD, 1.0, "3,2")
    for X, nm, an in ((O, "O", 200), (A, "A", -30), (B, "B", 90), (C, "C", -90), (D, "D", 150), (P, "P", -100), (Q, "Q", 30)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(184, 150, b)

def _fig_lmn():
    T = _tr(14, 134, 44)
    A, B, C = (1.0, 2.6), (0, 0), (3.2, 0)
    D = _mix(B, C, 4/7); P = _mix(A, D, 7/9)
    b = _pg([T(A), T(B), T(C)], FILL, "#333", 1.1, 0.35)
    b += _ln(T(A), T(D), "#555", 1.0, "3,2") + _ln(T(P), T(B), BL, 1.1) + _ln(T(P), T(C), BL, 1.1)
    for X, nm, an in ((A, "A", 90), (B, "B", 225), (C, "C", -45), (D, "D", -90), (P, "P", 15)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(170, 148, b)

def _fig_para():
    T = _tr(12, 94, 40)
    A, B, C, D = (0, 0), (3, 0), (4, 2), (1, 2)
    M, N = (3.5, 1), (2, 2)
    P, Q = (7/3, 2/3), (1.5, 1.5)
    b = _pg([T(A), T(B), T(C), T(D)]) + _ln(T(B), T(D), "#333", 1.0)
    b += _ln(T(A), T(M), BL, 1.1) + _ln(T(A), T(N), RD, 1.1)
    for X, nm, an in ((A, "A", 225), (B, "B", -45), (C, "C", 45), (D, "D", 135), (M, "M", 0), (N, "N", 90), (P, "P", -80), (Q, "Q", 160)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(186, 108, b)

def _fig_routh():
    T = _tr(14, 130, 46)
    A, B, C = (0.9, 2.4), (0, 0), (3.0, 0)
    t = (5 - math.sqrt(5)) / 10
    D = _mix(B, C, t); E = _mix(C, A, t); F = _mix(A, B, t)
    R = _meet(A, D, B, E); P = _meet(B, E, C, F); Q = _meet(C, F, A, D)
    b = _pg([T(A), T(B), T(C)]) + _pg([T(P), T(Q), T(R)], FILL, "#333", 0.8, 0.9)
    b += _ln(T(A), T(D), BL, 1.0) + _ln(T(B), T(E), BL, 1.0) + _ln(T(C), T(F), BL, 1.0)
    for X, nm, an in ((A, "A", 90), (B, "B", 225), (C, "C", -45), (D, "D", -90), (E, "E", 45), (F, "F", 150)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(166, 144, b)

SEC.append({"title": "位置ベクトル・分点と交点",
"base": r"""・2点 A$(\vec a)$，B$(\vec b)$ を $m:n$ に内分する点：$\dfrac{n\vec a+m\vec b}{m+n}$，外分する点：$\dfrac{-n\vec a+m\vec b}{m-n}$。△ABC の重心：$\dfrac{\vec a+\vec b+\vec c}{3}$<br>
・3点 A，B，C が一直線上にある $\iff\VV{AC}=k\VV{AB}$ となる実数 $k$ がある<br>
・$\VV{OP}=s\VV{OA}+t\VV{OB}$ のとき，P が直線 AB 上にある $\iff s+t=1$（係数の和が1）<br>
・交点の位置ベクトルは「2通りに表して係数比較」（$\VV{OA},\ \VV{OB}$ の1次独立性を使う）""",
"items": [
 {"lv": 1, "title": "内分点・外分点・重心の位置ベクトル",
  "q": r"△ABC において，A$(\vec a)$，B$(\vec b)$，C$(\vec c)$ とする。辺 BC を 2:1 に内分する点を D，辺 AB を 1:3 に外分する点を E とするとき，次のものを $\vec a,\ \vec b,\ \vec c$ で表せ。<br>(1) D，E の位置ベクトル $\vec d,\ \vec e$　(2) $\VV{DE}$　(3) △ADE の重心 G の位置ベクトル $\vec g$",
  "hint": r"$m:n$ に内分する点は $\dfrac{n\vec a+m\vec b}{m+n}$。外分は「$m:(-n)$ に内分」と考えれば同じ公式が使える（1:3 の外分 → $\dfrac{-3\vec a+\vec b}{1-3}$）。",
  "sol": r"(1) $\vec d=\dfrac{1\cdot\vec b+2\vec c}{2+1}=\boldsymbol{\dfrac{\vec b+2\vec c}{3}}$，　$\vec e=\dfrac{-3\vec a+1\cdot\vec b}{1-3}=\boldsymbol{\dfrac{3\vec a-\vec b}{2}}$<br>"
         r"(2) $\VV{DE}=\vec e-\vec d=\dfrac{3(3\vec a-\vec b)-2(\vec b+2\vec c)}{6}=\boldsymbol{\dfrac{9\vec a-5\vec b-4\vec c}{6}}$<br>"
         r"(3) $\vec g=\dfrac{\vec a+\vec d+\vec e}{3}=\dfrac13\cdot\dfrac{6\vec a+2(\vec b+2\vec c)+3(3\vec a-\vec b)}{6}=\boldsymbol{\dfrac{15\vec a-\vec b+4\vec c}{18}}$",
  "note": r"重心 G については $\VV{GA}+\VV{GB}+\VV{GC}=\vec 0$ もよく使う。また，2つの三角形 ABC，PQR の重心が一致する $\iff\vec a+\vec b+\vec c=\vec p+\vec q+\vec r$。例えば △ABC の辺 BC，CA，AB を同じ比 $m:n$ に内分する点を P，Q，R とすると $\vec p+\vec q+\vec r=\vec a+\vec b+\vec c$ となり，△PQR と △ABC の重心は一致する。",
  "ex": r"△ABC において，辺 AB を 3:2 に内分する点を P，辺 AC を 3:1 に外分する点を Q とするとき，$\vec p,\ \vec q$ および $\VV{PQ}$ を $\vec a,\ \vec b,\ \vec c$ で表せ。",
  "exa": r"$\vec p=\dfrac{2\vec a+3\vec b}{5}$，$\vec q=\dfrac{-\vec a+3\vec c}{2}$，$\VV{PQ}=\dfrac{-9\vec a-6\vec b+15\vec c}{10}$"},
 {"lv": 2, "title": "3点が一直線上にあることの証明",
  "q": _fig_menelaus() + r"△ABC において，辺 AB を 1:2 に内分する点を D，辺 AC の中点を E，辺 BC を 2:1 に外分する点を F とする。3点 D，E，F は一直線上にあることを示し，DE:EF を求めよ。",
  "hint": r"始点を A にそろえ，$\VV{DE}$ と $\VV{DF}$ を $\vec b=\VV{AB}$，$\vec c=\VV{AC}$ で表す。$\VV{DF}=k\VV{DE}$ となる実数 $k$ が見つかれば一直線上にある。",
  "sol": r"$\VV{AB}=\vec b$，$\VV{AC}=\vec c$ とすると<br>"
         r"$\VV{AD}=\dfrac13\vec b$，$\VV{AE}=\dfrac12\vec c$，$\VV{AF}=\dfrac{-1\cdot\vec b+2\vec c}{2-1}=-\vec b+2\vec c$<br>"
         r"$\VV{DE}=\dfrac12\vec c-\dfrac13\vec b=\dfrac{-2\vec b+3\vec c}{6}$，　$\VV{DF}=-\vec b+2\vec c-\dfrac13\vec b=\dfrac{-8\vec b+12\vec c}{6}=4\VV{DE}$<br>"
         r"よって3点 D，E，F は一直線上にある。■<br>"
         r"また $\VV{DF}=4\VV{DE}$ より DE:DF＝1:4 で，E は D と F の間にあるから　$\boldsymbol{\mathrm{DE}:\mathrm{EF}=1:3}$",
  "note": r"メネラウスの定理の逆からも示せる：$\dfrac{\mathrm{AD}}{\mathrm{DB}}\cdot\dfrac{\mathrm{BF}}{\mathrm{FC}}\cdot\dfrac{\mathrm{CE}}{\mathrm{EA}}=\dfrac12\cdot\dfrac21\cdot\dfrac11=1$。ベクトルなら比 DE:EF まで同時に求まる。",
  "ex": r"△ABC において，辺 AB を 2:1 に内分する点を P，辺 AC を 2:3 に内分する点を Q，辺 BC を 1:3 に外分する点を R とする。3点 P，Q，R が一直線上にあることを示し，PQ:PR を求めよ。",
  "exa": r"$\VV{PR}=-\dfrac54\VV{PQ}$ より一直線上（P は Q と R の間）。PQ:PR＝4:5"},
 {"lv": 2, "title": "2直線の交点の位置ベクトル",
  "q": _fig_cross() + r"△OAB において，辺 OA を 2:1 に内分する点を C，辺 OB を 3:2 に内分する点を D とし，線分 AD と線分 BC の交点を P とする。$\VV{OA}=\vec a$，$\VV{OB}=\vec b$ とする。<br>(1) $\VV{OP}$ を $\vec a,\ \vec b$ で表せ。<br>(2) 直線 OP と辺 AB の交点を Q とするとき，AQ:QB，OP:PQ を求めよ。",
  "hint": r"P を「AD 上の点」「BC 上の点」として2通りに表し，$\vec a,\ \vec b$ が1次独立であることから係数を比較する。(2) Q は直線 OP 上にあるので $\VV{OQ}=k\VV{OP}$，直線 AB 上にあるので係数の和が1。",
  "sol": r"(1) AP:PD＝$s:(1-s)$ とすると　$\VV{OP}=(1-s)\vec a+s\cdot\dfrac35\vec b$<br>"
         r"BP:PC＝$t:(1-t)$ とすると　$\VV{OP}=t\cdot\dfrac23\vec a+(1-t)\vec b$<br>"
         r"$\vec a,\ \vec b$ は1次独立なので　$1-s=\dfrac23t$，$\dfrac35s=1-t$<br>"
         r"これを解いて $s=\dfrac59$，$t=\dfrac23$。よって　$\boldsymbol{\VV{OP}=\dfrac49\vec a+\dfrac13\vec b}$<br>"
         r"(2) Q は直線 OP 上にあるから $\VV{OQ}=k\VV{OP}=\dfrac{4k}{9}\vec a+\dfrac{3k}{9}\vec b$。Q は直線 AB 上にあるから $\dfrac{4k}{9}+\dfrac{3k}{9}=1$，$k=\dfrac97$<br>"
         r"$\VV{OQ}=\dfrac{4\vec a+3\vec b}{7}$ より　$\boldsymbol{\mathrm{AQ}:\mathrm{QB}=3:4}$。また $\VV{OQ}=\dfrac97\VV{OP}$ より　$\boldsymbol{\mathrm{OP}:\mathrm{PQ}=7:2}$",
  "note": r"メネラウスの定理（△OAD と直線 BC）を使うと $\dfrac{\mathrm{OC}}{\mathrm{CA}}\cdot\dfrac{\mathrm{AP}}{\mathrm{PD}}\cdot\dfrac{\mathrm{DB}}{\mathrm{BO}}=1$，すなわち $2\cdot\dfrac{\mathrm{AP}}{\mathrm{PD}}\cdot\dfrac25=1$ から AP:PD＝5:4（$s=\dfrac59$ と一致）。AQ:QB はチェバの定理 $\dfrac{\mathrm{OC}}{\mathrm{CA}}\cdot\dfrac{\mathrm{AQ}}{\mathrm{QB}}\cdot\dfrac{\mathrm{BD}}{\mathrm{DO}}=1$ でも確かめられる。",
  "ex": r"△OAB において，辺 OA の中点を C，辺 OB を 2:1 に内分する点を D，線分 AD と BC の交点を P，直線 OP と辺 AB の交点を Q とする。$\VV{OP}$ を $\vec a=\VV{OA}$，$\vec b=\VV{OB}$ で表し，AQ:QB，OP:PQ を求めよ。",
  "exa": r"$\VV{OP}=\dfrac14\vec a+\dfrac12\vec b$，AQ:QB＝2:1，OP:PQ＝3:1"},
 {"lv": 3, "title": r"$l\VV{PA}+m\VV{PB}+n\VV{PC}=\vec 0$ を満たす点と面積比",
  "q": _fig_lmn() + r"△ABC と点 P が $2\VV{PA}+3\VV{PB}+4\VV{PC}=\vec 0$ を満たしている。<br>(1) 点 P はどのような位置にあるか。<br>(2) △PBC：△PCA：△PAB を求めよ。",
  "hint": r"始点を A にそろえて $\VV{AP}$ を求め，$\VV{AP}=k\cdot\dfrac{m\vec b+n\vec c}{m+n}$ の形（「辺 BC 上の点」の実数倍）に変形する。面積比は「高さが共通なら底辺の比」を2回使う。",
  "sol": r"A を始点とし，$\VV{AB}=\vec b$，$\VV{AC}=\vec c$，$\VV{AP}=\vec p$ とする。与式は<br>"
         r"$2(-\vec p)+3(\vec b-\vec p)+4(\vec c-\vec p)=\vec 0$ より $9\vec p=3\vec b+4\vec c$，$\vec p=\dfrac79\cdot\dfrac{3\vec b+4\vec c}{7}$<br>"
         r"(1) $\VV{AD}=\dfrac{3\vec b+4\vec c}{7}$ とおくと D は辺 BC を 4:3 に内分する点で，$\VV{AP}=\dfrac79\VV{AD}$。<br>"
         r"よって　<b>辺 BC を 4:3 に内分する点を D とすると，P は線分 AD を 7:2 に内分する点</b><br>"
         r"(2) △ABC の面積を $S$ とする。△ABD＝$\dfrac47S$，△ACD＝$\dfrac37S$ であり<br>"
         r"△PBC＝$\dfrac{\mathrm{PD}}{\mathrm{AD}}S=\dfrac29S$，△PCA＝$\dfrac{\mathrm{AP}}{\mathrm{AD}}$△ACD＝$\dfrac79\cdot\dfrac37S=\dfrac39S$，△PAB＝$\dfrac79$△ABD＝$\dfrac79\cdot\dfrac47S=\dfrac49S$<br>"
         r"よって　$\boldsymbol{\triangle\mathrm{PBC}:\triangle\mathrm{PCA}:\triangle\mathrm{PAB}=2:3:4}$",
  "note": r"一般に $l,\ m,\ n>0$ で $l\VV{PA}+m\VV{PB}+n\VV{PC}=\vec 0$ なら，P は △ABC の内部にあり △PBC:△PCA:△PAB＝$l:m:n$（重心は $l=m=n$ の場合）。なお，P が △ABC の内部にある条件は「$\VV{AP}=s\VV{AB}+t\VV{AC}$，$s>0,\ t>0,\ s+t<1$」である。",
  "ex": r"△ABC と点 P が $3\VV{PA}+\VV{PB}+2\VV{PC}=\vec 0$ を満たす。点 P の位置をいい，△PBC:△PCA:△PAB を求めよ。",
  "exa": r"辺 BC を 2:1 に内分する点を D とすると，P は線分 AD の中点。面積比は 3:1:2"},
 {"lv": 3, "title": "平行四辺形の対角線上の交点と比",
  "q": _fig_para() + r"平行四辺形 ABCD において，辺 BC の中点を M，辺 CD を 2:1 に内分する点を N とし，線分 AM，AN と対角線 BD の交点をそれぞれ P，Q とする。BP:PQ:QD を求めよ。",
  "hint": r"$\vec b=\VV{AB}$，$\vec d=\VV{AD}$ を基準にする。対角線 BD 上の点は $(1-u)\vec b+u\vec d$（係数の和が1）と表せる。AM 上の点 $k\VV{AM}$ が BD 上にある条件から $k$ を決める。",
  "sol": r"$\VV{AB}=\vec b$，$\VV{AD}=\vec d$ とする。直線 BD 上の点 X は $\VV{AX}=(1-u)\vec b+u\vec d$ と表せ，BX:BD＝$u:1$ である。<br>"
         r"$\VV{AM}=\vec b+\dfrac12\vec d$。P は直線 AM 上にあるから $\VV{AP}=k\VV{AM}=k\vec b+\dfrac k2\vec d$。P は直線 BD 上にあるから $k+\dfrac k2=1$，$k=\dfrac23$。<br>"
         r"よって $\VV{AP}=\dfrac23\vec b+\dfrac13\vec d$ で，BP＝$\dfrac13$BD。<br>"
         r"$\VV{AN}=\dfrac{\VV{AC}+2\VV{AD}}{3}=\dfrac{(\vec b+\vec d)+2\vec d}{3}=\dfrac13\vec b+\vec d$。$\VV{AQ}=l\VV{AN}$ とおくと $\dfrac l3+l=1$，$l=\dfrac34$。<br>"
         r"よって $\VV{AQ}=\dfrac14\vec b+\dfrac34\vec d$ で，BQ＝$\dfrac34$BD。<br>"
         r"したがって BP:PQ:QD＝$\dfrac13:\left(\dfrac34-\dfrac13\right):\dfrac14=\dfrac4{12}:\dfrac5{12}:\dfrac3{12}$ より　$\boldsymbol{4:5:3}$",
  "note": r"相似を使う別解：AD∥BM より △PBM∽△PDA で BP:PD＝BM:DA＝1:2。AB∥ND より △QBA∽△QDN で BQ:QD＝AB:ND＝3:1。ベクトルの方法は，平行線が見つけにくい図形でもそのまま使える。",
  "ex": r"平行四辺形 ABCD において，辺 CD の中点を M，辺 BC を 1:2 に内分する点を N とし，線分 AM，AN と対角線 BD の交点をそれぞれ P，Q とする。BQ:QP:PD を求めよ。",
  "exa": r"3:5:4"},
 {"lv": 4, "title": "重心を通る直線と三角形の面積の範囲",
  "q": r"△OAB の重心を G とする。辺 OA 上の点 P，辺 OB 上の点 Q を，直線 PQ が G を通るように動かす。$\VV{OP}=s\VV{OA}$，$\VV{OQ}=t\VV{OB}$ とするとき，<br>(1) $\dfrac1s+\dfrac1t$ の値を求めよ。<br>(2) △OPQ の面積は △OAB の面積の何倍か。そのとり得る値の範囲を求めよ。",
  "hint": r"(1) $\VV{OG}$ を $\VV{OP}$，$\VV{OQ}$ で表すと，G が直線 PQ 上にある条件は「係数の和が1」。(2) 面積比は $st$。条件 $s+t=3st$ の下で，$s,\ t$ の動く範囲 $0<s\leqq1$，$0<t\leqq1$ に注意して $st$ の範囲を求める（下からは相加・相乗平均，上からは $(1-s)(1-t)\geqq0$）。",
  "sol": r"$\VV{OA}=\vec a$，$\VV{OB}=\vec b$ とする。P＝O だと直線 PQ は直線 OB になり G を通らないので P≠O，同様に Q≠O。よって $0<s\leqq1$，$0<t\leqq1$。<br>"
         r"(1) $\VV{OG}=\dfrac{\vec a+\vec b}{3}=\dfrac1{3s}\VV{OP}+\dfrac1{3t}\VV{OQ}$。G は直線 PQ 上にあるから $\dfrac1{3s}+\dfrac1{3t}=1$　∴ $\boldsymbol{\dfrac1s+\dfrac1t=3}$<br>"
         r"(2) △OPQ＝$st\cdot$△OAB（2辺の比）なので，$st$ の範囲を求める。(1) より　$s+t=3st$ ……①<br>"
         r"［下からの評価］相加平均・相乗平均の関係から $3st=s+t\geqq2\sqrt{st}$，$\sqrt{st}\geqq\dfrac23$，$st\geqq\dfrac49$。等号は $s=t=\dfrac23$ のとき（①を満たす）。<br>"
         r"［上からの評価］$s\leqq1,\ t\leqq1$ より $(1-s)(1-t)\geqq0$，$1-(s+t)+st\geqq0$。①を代入して $1-2st\geqq0$，$st\leqq\dfrac12$。等号は $s=1$，$t=\dfrac12$（P＝A，Q は OB の中点）などのとき。<br>"
         r"［間の値］(1) より $t=\dfrac{s}{3s-1}$ で，$s$ を $\dfrac12\leqq s\leqq1$ で動かすと $t$ は $1$ から $\dfrac12$ まで連続的に減少し，$0<t\leqq1$ を満たす。$st$ は連続的に変わるので，$\dfrac49$ と $\dfrac12$ の間の値はすべてとる。<br>"
         r"よって　$\boldsymbol{\dfrac49}$ 倍以上 $\boldsymbol{\dfrac12}$ 倍以下",
  "note": r"置き換え $3s-1=x$（$\dfrac12\leqq x\leqq2$）を使うと $st=\dfrac{s^2}{3s-1}=\dfrac19\left(x+\dfrac1x+2\right)$ となり，$x=1$ で最小 $\dfrac49$，$x=\dfrac12,\ 2$ で最大 $\dfrac12$ と確かめられる。「重心を通る直線で切り取られる三角形の面積は，もとの $\dfrac49$ 倍以上 $\dfrac12$ 倍以下」という有名な事実である。",
  "ex": r"△OAB の辺 AB の中点を M，線分 OM の中点を N とする。辺 OA 上の点 P，辺 OB 上の点 Q を，直線 PQ が N を通るように動かす。$\VV{OP}=s\VV{OA}$，$\VV{OQ}=t\VV{OB}$ とするとき，$\dfrac1s+\dfrac1t$ の値と，△OPQ の面積が △OAB の面積の何倍か（その範囲）を求めよ。",
  "exa": r"$\dfrac1s+\dfrac1t=4$，$\dfrac14$ 倍以上 $\dfrac13$ 倍以下"},
 {"lv": 4, "title": "3本の線分で囲まれる三角形の面積（文字を含む分点）",
  "q": _fig_routh() + r"△ABC の辺 BC，CA，AB を，それぞれ $t:(1-t)$ に内分する点を D，E，F とする（$0<t<1$，$t\neq\dfrac12$）。すなわち BD:DC＝CE:EA＝AF:FB＝$t:(1-t)$ である。線分 AD，BE，CF で囲まれる三角形の面積が △ABC の面積の $\dfrac14$ となるような $t$ の値を求めよ。",
  "hint": r"まず AD と BE の交点 R の位置（AR:AD）を，「AD 上」「BE 上」の2通りに表して $t$ で求める。周りの3つの三角形 ABR，BCP，CAQ は，文字を入れかえても同じ形なので面積が等しく，中央の三角形はその残り。",
  "sol": r"△ABC の面積を $S$，$\VV{AB}=\vec b$，$\VV{AC}=\vec c$ とすると<br>"
         r"$\VV{AD}=(1-t)\vec b+t\vec c$，$\VV{AE}=(1-t)\vec c$，$\VV{AF}=t\vec b$<br>"
         r"AD と BE の交点を R とし，$\VV{AR}=k\VV{AD}=k(1-t)\vec b+kt\vec c$ とおく。R は直線 BE 上にあるから $\VV{AR}=(1-m)\vec b+m\VV{AE}=(1-m)\vec b+m(1-t)\vec c$ と表せる。係数を比較して<br>"
         r"$k(1-t)=1-m$，$kt=m(1-t)$。第2式の $m=\dfrac{kt}{1-t}$ を第1式に代入して $k\left\{(1-t)+\dfrac{t}{1-t}\right\}=1$<br>"
         r"∴ $k=\dfrac{1-t}{(1-t)^2+t}=\dfrac{1-t}{t^2-t+1}$<br>"
         r"△ABD＝$\dfrac{\mathrm{BD}}{\mathrm{BC}}S=tS$ なので　△ABR＝$\dfrac{\mathrm{AR}}{\mathrm{AD}}$△ABD＝$ktS=\dfrac{t(1-t)}{t^2-t+1}S$<br>"
         r"条件は A→B→C→A，D→E→F→D と文字を入れかえても同じ形なので，BE と CF の交点 P，CF と AD の交点 Q についても △BCP＝△CAQ＝$\dfrac{t(1-t)}{t^2-t+1}S$。<br>"
         r"△ABC は △ABR，△BCP，△CAQ と，3本の線分で囲まれる △PQR に分けられるから<br>"
         r"△PQR＝$S-\dfrac{3t(1-t)}{t^2-t+1}S=\dfrac{t^2-t+1-3t+3t^2}{t^2-t+1}S=\dfrac{(2t-1)^2}{t^2-t+1}S$<br>"
         r"これが $\dfrac14S$ となる条件は $4(2t-1)^2=t^2-t+1$，$15t^2-15t+3=0$，$5t^2-5t+1=0$<br>"
         r"∴ $\boldsymbol{t=\dfrac{5\pm\sqrt5}{10}}$（ともに $0<t<1$ を満たす）",
  "note": r"これはラウスの定理の特別な場合。$t=\dfrac12$ のときは3本が重心で交わって面積 0，$t=\dfrac13$（各辺を 1:2）のときは $\dfrac17$ になる。2つの解は $t$ と $1-t$ の関係にあり，図を裏返した配置に対応する。",
  "ex": r"△ABC の辺 BC，CA，AB を，それぞれ 1:3 に内分する点を D，E，F とする（BD:DC＝CE:EA＝AF:FB＝1:3）。線分 AD，BE，CF で囲まれる三角形の面積は △ABC の面積の何倍か。",
  "exa": r"$\dfrac{4}{13}$ 倍"},
]})

# ================================================================ 節6
def _fig_euler():
    T = _tr(10, 128, 44)
    A, B, C = (1.0, 2.5), (0, 0), (3.4, 0)
    ox = 1.7
    oy = (A[0]**2 + A[1]**2 - 2*ox*A[0]) / (2*A[1])     # |O-A| = |O-B|, O=(1.7, oy)
    O = (ox, oy)
    H = (A[0] + B[0] + C[0] - 2*O[0], A[1] + B[1] + C[1] - 2*O[1])
    G = ((A[0] + B[0] + C[0])/3, (A[1] + B[1] + C[1])/3)
    b = _pg([T(A), T(B), T(C)])
    b += _ln(T(A), T((A[0], 0)), "#888", 0.8, "2,2") + _ln(T(O), T((ox, 0)), "#888", 0.8, "2,2")
    b += _ln(T(O), T(H), RD, 1.2)
    for X, nm, an in ((A, "A", 90), (B, "B", 225), (C, "C", -45), (O, "O", 0), (H, "H", 160), (G, "G", -70)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(170, 144, b)

SEC.append({"title": "三角形の五心とベクトル",
"base": r"""・垂線の足：点 B から直線 OA に下ろした垂線の足 H は $\VV{OH}=\dfrac{\vec a\cdot\vec b}{|\vec a|^2}\vec a$（$\vec b$ の $\vec a$ 方向への正射影）<br>
・外心 O：各辺の垂直二等分線の交点。$\VV{AO}\cdot\VV{AB}=\dfrac12\mathrm{AB}^2$，$\VV{AO}\cdot\VV{AC}=\dfrac12\mathrm{AC}^2$<br>
・内心 I：$\VV{AI}=\dfrac{b\VV{AB}+c\VV{AC}}{a+b+c}$（$a=\mathrm{BC},\ b=\mathrm{CA},\ c=\mathrm{AB}$）。垂心 H：$\VV{AH}\cdot\VV{BC}=0$，$\VV{BH}\cdot\VV{CA}=0$<br>
・外心 O を始点とすると　垂心 $\VV{OH}=\VV{OA}+\VV{OB}+\VV{OC}$，重心 $\VV{OG}=\dfrac13\VV{OH}$（オイラー線）""",
"items": [
 {"lv": 2, "title": "垂線の足と対称な点",
  "q": r"△OAB において，$\vec a=\VV{OA}$，$\vec b=\VV{OB}$ とし，$|\vec a|=2$，$|\vec b|=3$，$\vec a\cdot\vec b=2$ とする。<br>(1) 点 B から直線 OA に下ろした垂線の足を H とするとき，$\VV{OH}$ を $\vec a$ で表せ。<br>(2) 直線 OA に関して点 B と対称な点 B' について，$\VV{OB'}$ を $\vec a,\ \vec b$ で表せ。<br>(3) 点 B と直線 OA の距離を求めよ。",
  "hint": r"H は直線 OA 上にあるので $\VV{OH}=k\vec a$ とおき，$\VV{BH}\perp\vec a$（内積 0）から $k$ を決める。対称な点は「H が線分 BB' の中点」を使う。",
  "sol": r"(1) $\VV{OH}=k\vec a$ とおく。$\VV{BH}\perp\vec a$ より $(k\vec a-\vec b)\cdot\vec a=0$，$k|\vec a|^2-\vec a\cdot\vec b=0$，$4k-2=0$　∴ $k=\dfrac12$<br>"
         r"よって　$\boldsymbol{\VV{OH}=\dfrac12\vec a}$<br>"
         r"(2) H は線分 BB' の中点だから $\VV{OH}=\dfrac{\vec b+\VV{OB'}}{2}$。∴ $\VV{OB'}=2\VV{OH}-\vec b=\boldsymbol{\vec a-\vec b}$<br>"
         r"(3) $|\VV{BH}|^2=\left|\dfrac12\vec a-\vec b\right|^2=\dfrac14|\vec a|^2-\vec a\cdot\vec b+|\vec b|^2=1-2+9=8$　∴ 距離は $\boldsymbol{2\sqrt2}$",
  "note": r"一般に $\VV{OH}=\dfrac{\vec a\cdot\vec b}{|\vec a|^2}\vec a$（正射影ベクトル）。(3) は面積を使って $\triangle\mathrm{OAB}=\dfrac12\sqrt{4\cdot9-2^2}=2\sqrt2$ と $\triangle\mathrm{OAB}=\dfrac12\cdot\mathrm{OA}\cdot\mathrm{BH}=\mathrm{BH}$ からも得られる。",
  "ex": r"$|\vec a|=3$，$|\vec b|=2$，$\vec a\cdot\vec b=-3$ のとき，(1) 点 A から直線 OB に下ろした垂線の足 H について $\VV{OH}$ (2) 直線 OB に関して A と対称な点 A' について $\VV{OA'}$ (3) 線分 AH の長さ を求めよ。",
  "exa": r"(1) $\VV{OH}=-\dfrac34\vec b$　(2) $\VV{OA'}=-\vec a-\dfrac32\vec b$　(3) $\dfrac{3\sqrt3}{2}$"},
 {"lv": 3, "title": "外心の位置ベクトル",
  "q": r"△ABC において AB＝2，AC＝3，∠BAC＝60° とする。外心を O とするとき，$\VV{AO}$ を $\vec b=\VV{AB}$，$\vec c=\VV{AC}$ で表せ。",
  "hint": r"外心から辺に下ろした垂線の足は辺の中点。よって内積 $\VV{AO}\cdot\VV{AB}$ は「$\VV{AO}$ の AB 方向の成分 × AB」$=\dfrac12\mathrm{AB}^2$。$\VV{AO}=s\vec b+t\vec c$ とおき，2つの内積の条件から $s,\ t$ を求める。",
  "sol": r"$|\vec b|=2$，$|\vec c|=3$，$\vec b\cdot\vec c=2\cdot3\cos60^\circ=3$。$\VV{AO}=s\vec b+t\vec c$ とおく。<br>"
         r"辺 AB の中点を M とすると OM⊥AB なので　$\VV{AO}\cdot\vec b=(\VV{AM}+\VV{MO})\cdot\vec b=\VV{AM}\cdot\vec b=\dfrac12|\vec b|^2=2$<br>"
         r"同様に $\VV{AO}\cdot\vec c=\dfrac12|\vec c|^2=\dfrac92$。よって<br>"
         r"$4s+3t=2$，$3s+9t=\dfrac92$。これを解いて $s=\dfrac16$，$t=\dfrac49$<br>"
         r"∴ $\boldsymbol{\VV{AO}=\dfrac16\vec b+\dfrac49\vec c}$",
  "note": r"検算：$|\VV{AO}|^2=\dfrac{4}{36}+2\cdot\dfrac16\cdot\dfrac49\cdot3+\dfrac{16}{81}\cdot9=\dfrac73$。一方，余弦定理より BC$=\sqrt7$，正弦定理より $R=\dfrac{\sqrt7}{2\sin60^\circ}=\sqrt{\dfrac73}$ で一致する。∠A が鈍角だと係数の和 $s+t$ が 1 より大きくなり，O は直線 BC に関して A と反対側に出る（練習）。",
  "ex": r"AB＝3，AC＝4，∠BAC＝120° の △ABC の外心を O とする。$\VV{AO}$ を $\vec b=\VV{AB}$，$\vec c=\VV{AC}$ で表せ。",
  "exa": r"$\VV{AO}=\dfrac{10}{9}\vec b+\dfrac{11}{12}\vec c$"},
 {"lv": 3, "title": "内心の位置ベクトル",
  "q": r"AB＝4，BC＝6，CA＝5 の △ABC の内心を I とする。$\VV{AI}$ を $\VV{AB}$，$\VV{AC}$ で表せ。",
  "hint": r"内心は角の二等分線の交点。角の二等分線の定理を2回使う：∠A の二等分線と BC の交点 D で BD:DC を出し，次に △ABD で ∠B の二等分線が AD を分ける比 AI:ID を出す。",
  "sol": r"∠A の二等分線と辺 BC の交点を D とすると BD:DC＝AB:AC＝4:5 なので<br>"
         r"$\VV{AD}=\dfrac{5\VV{AB}+4\VV{AC}}{9}$，　BD$=6\cdot\dfrac49=\dfrac83$<br>"
         r"△ABD で BI は ∠B の二等分線なので　AI:ID＝BA:BD＝$4:\dfrac83=3:2$<br>"
         r"よって $\VV{AI}=\dfrac35\VV{AD}=\dfrac{5\VV{AB}+4\VV{AC}}{15}$，すなわち　$\boldsymbol{\VV{AI}=\dfrac13\VV{AB}+\dfrac4{15}\VV{AC}}$",
  "note": r"一般に $a=\mathrm{BC},\ b=\mathrm{CA},\ c=\mathrm{AB}$ とすると $\VV{AI}=\dfrac{b\VV{AB}+c\VV{AC}}{a+b+c}$（この問題では $\dfrac{5\VV{AB}+4\VV{AC}}{15}$）。これは $a\VV{IA}+b\VV{IB}+c\VV{IC}=\vec 0$ と同値で，△IBC:△ICA:△IAB＝$a:b:c$（高さがすべて内接円の半径 $r$）とも合う。",
  "ex": r"AB＝5，BC＝7，CA＝3 の △ABC の内心を I とする。$\VV{AI}$ を $\VV{AB}$，$\VV{AC}$ で表せ。",
  "exa": r"$\VV{AI}=\dfrac15\VV{AB}+\dfrac13\VV{AC}$"},
 {"lv": 4, "title": "垂心の位置ベクトルとオイラー線",
  "q": _fig_euler() + r"△ABC の外心を O とし，$\VV{OH}=\VV{OA}+\VV{OB}+\VV{OC}$ で点 H を定める。<br>(1) H は △ABC の垂心であることを示せ。また，重心 G について，O，G，H の位置関係を述べよ。<br>(2) AB＝2，AC＝3，∠BAC＝60° のとき，$\VV{AH}$ を $\vec b=\VV{AB}$，$\vec c=\VV{AC}$ で表せ。",
  "hint": r"(1) 外心を始点にすると $|\VV{OA}|=|\VV{OB}|=|\VV{OC}|$ なので，「和と差の内積」$(\vec y+\vec z)\cdot(\vec z-\vec y)=|\vec z|^2-|\vec y|^2$ が 0 になる。(2) は (1) から $\VV{AH}=\vec b+\vec c-2\VV{AO}$ となり，外心を求める問題に帰着する。",
  "sol": r"(1) $\vec x=\VV{OA}$，$\vec y=\VV{OB}$，$\vec z=\VV{OC}$ とおくと $|\vec x|=|\vec y|=|\vec z|$（外接円の半径）で，$\VV{AH}=\vec y+\vec z$，$\VV{BH}=\vec x+\vec z$。<br>"
         r"$\VV{AH}\cdot\VV{BC}=(\vec y+\vec z)\cdot(\vec z-\vec y)=|\vec z|^2-|\vec y|^2=0$<br>"
         r"$\VV{BH}\cdot\VV{CA}=(\vec x+\vec z)\cdot(\vec x-\vec z)=|\vec x|^2-|\vec z|^2=0$<br>"
         r"よって H＝A または AH⊥BC だから，H は A から直線 BC に下ろした垂線上にある。同様に H は B から直線 CA に下ろした垂線上にもある。この2本の垂線の交点が垂心だから，H は △ABC の垂心である。■<br>"
         r"また $\VV{OG}=\dfrac{\vec x+\vec y+\vec z}{3}=\dfrac13\VV{OH}$ より　<b>O，G，H は一直線上にあり，OG:GH＝1:2</b>（正三角形のときは3点が一致する）。<br>"
         r"(2) $|\vec b|=2$，$|\vec c|=3$，$\vec b\cdot\vec c=3$。外心について $\VV{AO}\cdot\vec b=\dfrac12|\vec b|^2$，$\VV{AO}\cdot\vec c=\dfrac12|\vec c|^2$ だから，$\VV{AO}=s\vec b+t\vec c$ とおくと $4s+3t=2$，$3s+9t=\dfrac92$ より $\VV{AO}=\dfrac16\vec b+\dfrac49\vec c$。<br>"
         r"$\VV{AH}=\VV{OH}-\VV{OA}=\VV{OB}+\VV{OC}=(\vec b-\VV{AO})+(\vec c-\VV{AO})=\vec b+\vec c-2\VV{AO}$<br>"
         r"∴ $\boldsymbol{\VV{AH}=\dfrac23\vec b+\dfrac19\vec c}$",
  "note": r"検算：$\VV{AH}\cdot\VV{BC}=\left(\dfrac23\vec b+\dfrac19\vec c\right)\cdot(\vec c-\vec b)=\dfrac23\cdot3+\dfrac19\cdot9-\dfrac23\cdot4-\dfrac19\cdot3=0$。$\VV{AH}\cdot\VV{BC}=0$，$\VV{BH}\cdot\VV{CA}=0$ から直接連立方程式を立ててもよい。直線 OGH をオイラー線という。",
  "ex": r"AB＝4，AC＝3，∠BAC＝60° の △ABC の外心を O，垂心を H とする。$\VV{AO}$，$\VV{AH}$ を $\vec b=\VV{AB}$，$\vec c=\VV{AC}$ で表せ。",
  "exa": r"$\VV{AO}=\dfrac5{12}\vec b+\dfrac29\vec c$，$\VV{AH}=\dfrac16\vec b+\dfrac59\vec c$"},
 {"lv": 4, "title": "外心についてのベクトルの等式と三角形の決定",
  "q": r"外接円の半径が1である △ABC の外心 O が $3\VV{OA}+4\VV{OB}+5\VV{OC}=\vec 0$ を満たしている。<br>(1) 内積 $\VV{OA}\cdot\VV{OB}$，$\VV{OB}\cdot\VV{OC}$，$\VV{OC}\cdot\VV{OA}$ を求めよ。<br>(2) ∠ACB の大きさと △ABC の面積を求めよ。",
  "hint": r"1つのベクトルを残りの2つで表して大きさを2乗すれば，$|\VV{OA}|=|\VV{OB}|=|\VV{OC}|=1$ から内積が出る。角は円周角の定理（中心角の半分）で求めるが，C と O が直線 AB の同じ側にあるか（O が三角形の内部にあるか）を確かめる必要がある。",
  "sol": r"$\vec a=\VV{OA}$，$\vec b=\VV{OB}$，$\vec c=\VV{OC}$，$|\vec a|=|\vec b|=|\vec c|=1$ とする。<br>"
         r"(1) $5\vec c=-(3\vec a+4\vec b)$ の大きさを2乗して $25=9+24\vec a\cdot\vec b+16$　∴ $\vec a\cdot\vec b=\boldsymbol{0}$<br>"
         r"$4\vec b=-(3\vec a+5\vec c)$ より $16=9+30\vec c\cdot\vec a+25$　∴ $\vec c\cdot\vec a=\boldsymbol{-\dfrac35}$<br>"
         r"$3\vec a=-(4\vec b+5\vec c)$ より $9=16+40\vec b\cdot\vec c+25$　∴ $\vec b\cdot\vec c=\boldsymbol{-\dfrac45}$<br>"
         r"(2) 与式を A を始点として書きかえると $-3\VV{AO}+4(\VV{AB}-\VV{AO})+5(\VV{AC}-\VV{AO})=\vec 0$，$\VV{AO}=\dfrac13\VV{AB}+\dfrac5{12}\VV{AC}$。係数が正で和が $\dfrac34<1$ なので，O は △ABC の内部にある。<br>"
         r"$\vec a\cdot\vec b=0$ より ∠AOB＝90°。O が内部にあるので C は直線 AB に関して O と同じ側にあり，円周角の定理より　$\angle\mathrm{ACB}=\dfrac12\angle\mathrm{AOB}=\boldsymbol{45^\circ}$<br>"
         r"また $\cos\angle\mathrm{BOC}=-\dfrac45$，$\cos\angle\mathrm{COA}=-\dfrac35$ より $\sin\angle\mathrm{BOC}=\dfrac35$，$\sin\angle\mathrm{COA}=\dfrac45$。O は内部にあるから<br>"
         r"△ABC＝△OAB＋△OBC＋△OCA＝$\dfrac12\left(1+\dfrac35+\dfrac45\right)=\boldsymbol{\dfrac65}$",
  "note": r"△OBC:△OCA:△OAB＝$\dfrac35:\dfrac45:1=3:4:5$ で，与式の係数の比と一致する（$l\VV{PA}+m\VV{PB}+n\VV{PC}=\vec 0$ のときの面積比の性質）。O が内部にあることを確認しないと，∠ACB＝135° の可能性を排除できない。",
  "ex": r"外接円の半径が1である △ABC の外心 O が $5\VV{OA}+12\VV{OB}+13\VV{OC}=\vec 0$ を満たすとき，∠ACB の大きさと △ABC の面積を求めよ。",
  "exa": r"∠ACB$=45^\circ$，面積 $\dfrac{15}{13}$"},
 {"lv": 5, "title": "外心と内心の距離（オイラーの定理）",
  "q": r"△ABC の外接円の中心を O，半径を $R$，内心を I，内接円の半径を $r$ とし，BC$=a$，CA$=b$，AB$=c$ とする。<br>(1) $\mathrm{OI}^2=R^2-\dfrac{abc}{a+b+c}$ を示せ。<br>(2) $\mathrm{OI}^2=R^2-2Rr$ を示し，$R\geqq2r$ が成り立つこと，および等号が成り立つのは △ABC が正三角形のときに限ることを示せ。",
  "hint": r"外心を始点にとると $|\VV{OA}|=|\VV{OB}|=|\VV{OC}|=R$ で，$\VV{OA}\cdot\VV{OB}=R^2-\dfrac{c^2}{2}$ のように内積が辺の長さで表せる。内心の位置ベクトルを O 始点に書き直して大きさを2乗する。(2) は面積を2通り（$\dfrac12r(a+b+c)$ と $\dfrac{abc}{4R}$）に表して $abc$ を $R,\ r$ で書く。",
  "sol": r"(1) $\vec x=\VV{OA}$，$\vec y=\VV{OB}$，$\vec z=\VV{OC}$（$|\vec x|=|\vec y|=|\vec z|=R$）とする。内心の位置ベクトル $\VV{AI}=\dfrac{b\VV{AB}+c\VV{AC}}{a+b+c}$ を O 始点に書き直すと<br>"
         r"$\VV{OI}=\vec x+\dfrac{b(\vec y-\vec x)+c(\vec z-\vec x)}{a+b+c}=\dfrac{a\vec x+b\vec y+c\vec z}{a+b+c}$<br>"
         r"$c^2=|\vec y-\vec x|^2=2R^2-2\vec x\cdot\vec y$ より $\vec x\cdot\vec y=R^2-\dfrac{c^2}{2}$。同様に $\vec y\cdot\vec z=R^2-\dfrac{a^2}{2}$，$\vec z\cdot\vec x=R^2-\dfrac{b^2}{2}$。よって<br>"
         r"$|a\vec x+b\vec y+c\vec z|^2=(a^2+b^2+c^2)R^2+2ab\,\vec x\cdot\vec y+2bc\,\vec y\cdot\vec z+2ca\,\vec z\cdot\vec x$<br>"
         r"$=(a^2+b^2+c^2+2ab+2bc+2ca)R^2-(abc^2+bca^2+cab^2)=(a+b+c)^2R^2-abc(a+b+c)$<br>"
         r"両辺を $(a+b+c)^2$ で割って　$\mathrm{OI}^2=R^2-\dfrac{abc}{a+b+c}$ ■<br>"
         r"(2) △ABC の面積を $S$ とすると $S=\dfrac12r(a+b+c)$。また正弦定理 $\sin A=\dfrac{a}{2R}$ より $S=\dfrac12bc\sin A=\dfrac{abc}{4R}$。<br>"
         r"よって $abc=4RS=2Rr(a+b+c)$，$\dfrac{abc}{a+b+c}=2Rr$ で，(1) から　$\mathrm{OI}^2=R^2-2Rr$ ■<br>"
         r"$\mathrm{OI}^2\geqq0$ より $R(R-2r)\geqq0$，$R>0$ だから　$R\geqq2r$<br>"
         r"等号が成り立つ $\iff$ O＝I。O＝I なら，I から辺 BC に下ろした垂線の足（内接円と BC の接点）は BC の中点になる。接点と B，C の距離はそれぞれ $\dfrac{a+c-b}{2}$，$\dfrac{a+b-c}{2}$ なので $b=c$。同様に $c=a$ となり正三角形。逆に正三角形なら O＝I で等号が成り立つ。■",
  "note": r"(2) の等式をオイラーの定理という。例えば3辺が 3，4，5 の直角三角形では $R=\dfrac52$，$r=1$ で $\mathrm{OI}^2=\dfrac{25}{4}-5=\dfrac54$（座標で確かめられる）。「外接円の半径は内接円の半径の2倍以上」という不等式が，ベクトルの等式から一気に導ける。",
  "ex": r"同じ記号で，△ABC の垂心を H とする。$\VV{OH}=\VV{OA}+\VV{OB}+\VV{OC}$ を用いて，$\mathrm{OH}^2=9R^2-(a^2+b^2+c^2)$ を示せ。",
  "exa": r"$\mathrm{OH}^2=|\vec x+\vec y+\vec z|^2=3R^2+2\left(3R^2-\dfrac{a^2+b^2+c^2}{2}\right)=9R^2-(a^2+b^2+c^2)$"},
 {"lv": 5, "title": "オイラー線が辺と平行になる条件",
  "q": r"正三角形でない鋭角三角形 ABC の外心を O，垂心を H とする。直線 OH が辺 BC と平行になるための必要十分条件は $\tan B\tan C=3$ であることを示せ。",
  "hint": r"外心 O を始点にとると $\VV{OH}=\VV{OA}+\VV{OB}+\VV{OC}$。BC の中点 M について OM⊥BC なので，「OH∥BC」は「$\VV{OH}\cdot\VV{OM}=0$」と言いかえられる。内積は中心角 $2A,\ 2B,\ 2C$ の余弦で表し，三角関数の公式で整理する。",
  "sol": r"外接円の半径を $R$，$\vec x=\VV{OA}$，$\vec y=\VV{OB}$，$\vec z=\VV{OC}$ とすると $\VV{OH}=\vec x+\vec y+\vec z$。<br>"
         r"H＝O とすると $\VV{OG}=\dfrac13\VV{OH}=\vec 0$ で重心と外心が一致し，各中線が辺の垂直二等分線になって正三角形となるから，H≠O である。<br>"
         r"辺 BC の中点を M とすると $\VV{OM}=\dfrac{\vec y+\vec z}{2}$。鋭角三角形なので O は三角形の内部にあり $\VV{OM}\neq\vec 0$，OM⊥BC。よって<br>"
         r"OH∥BC $\iff\VV{OH}\perp\VV{OM}\iff(\vec x+\vec y+\vec z)\cdot(\vec y+\vec z)=0$ ……①<br>"
         r"鋭角三角形なので，円周角の定理より ∠BOC$=2A$，∠COA$=2B$，∠AOB$=2C$。よって<br>"
         r"$\vec y\cdot\vec z=R^2\cos2A$，$\vec z\cdot\vec x=R^2\cos2B$，$\vec x\cdot\vec y=R^2\cos2C$<br>"
         r"①の左辺 $=\vec x\cdot\vec y+\vec x\cdot\vec z+|\vec y+\vec z|^2=R^2(\cos2B+\cos2C+2+2\cos2A)$<br>"
         r"ここで $2+2\cos2A=4\cos^2A$，$\cos2B+\cos2C=2\cos(B+C)\cos(B-C)=-2\cos A\cos(B-C)$ なので<br>"
         r"①の左辺 $=2R^2\cos A\{2\cos A-\cos(B-C)\}$<br>"
         r"$\cos A>0$ だから　①$\iff2\cos A=\cos(B-C)$<br>"
         r"$\cos A=-\cos(B+C)$ を代入すると $-2\cos B\cos C+2\sin B\sin C=\cos B\cos C+\sin B\sin C$，すなわち $\sin B\sin C=3\cos B\cos C$。<br>"
         r"$\cos B\cos C>0$ で割って　$\tan B\tan C=3$。以上の変形はすべて同値変形なので，求める必要十分条件は $\tan B\tan C=3$ である。■",
  "note": r"例えば $B=45^\circ$ なら $\tan C=3$ で，$\tan A=-\tan(B+C)=-\dfrac{1+3}{1-3}=2>0$ なので確かに鋭角三角形になる。重心 G は線分 OH 上にあるので，この条件は「OG∥BC」とも同値。正三角形を除いたのは H＝O となって直線 OH が定まらないから（正三角形でも $\tan B\tan C=3$ は成り立つ）。",
  "ex": r"鋭角三角形 ABC の外心を O，垂心を H，外接円の半径を $R$ とする。AH$=2R\cos A$ を示し，AH＝AO となるのは ∠A＝60° のときに限ることを示せ。",
  "exa": r"$\VV{AH}=\VV{OB}+\VV{OC}$ より $\mathrm{AH}^2=2R^2+2R^2\cos2A=4R^2\cos^2A$，$\cos A>0$ なので AH$=2R\cos A$。AH$=R\iff\cos A=\dfrac12\iff A=60^\circ$"},
]})

# ================================================================ 節7
SEC.append({"title": "ベクトル方程式（直線・円）",
"base": r"""・点 A$(\vec a)$ を通り $\vec d$ に平行な直線：$\vec p=\vec a+t\vec d$（$\vec d$ は方向ベクトル）。2点 A，B を通る直線：$\vec p=(1-t)\vec a+t\vec b$<br>
・点 A$(\vec a)$ を通り $\vec n$ に垂直な直線：$\vec n\cdot(\vec p-\vec a)=0$。$\vec n=(a,\ b)$ なら $ax+by+c=0$ の形（$\vec n$ は法線ベクトル）<br>
・中心 C$(\vec c)$，半径 $r$ の円：$|\vec p-\vec c|=r$。2点 A，B を直径の両端とする円：$(\vec p-\vec a)\cdot(\vec p-\vec b)=0$<br>
・円 $|\vec p-\vec c|=r$ 上の点 $\mathrm{P_0}(\vec{p_0})$ における接線：$(\vec{p_0}-\vec c)\cdot(\vec p-\vec{p_0})=0$，すなわち $(\vec{p_0}-\vec c)\cdot(\vec p-\vec c)=r^2$""",
"items": [
 {"lv": 1, "title": "直線のベクトル方程式（方向ベクトル・法線ベクトル）",
  "q": r"(1) 点 A(1, 2) を通り，$\vec d=(3,-1)$ に平行な直線を，媒介変数 $t$ を用いて表せ。また，$t$ を消去した方程式を求めよ。<br>(2) 点 A(1, 2) を通り，$\vec n=(2,3)$ に垂直な直線の方程式を求めよ。<br>(3) 2直線 $x-3y+1=0$，$2x-y-4=0$ のなす角 $\theta$（$0^\circ\leqq\theta\leqq90^\circ$）を求めよ。",
  "hint": r"(1) $(x,\ y)=(1,\ 2)+t(3,\ -1)$。(2) 直線上の点 P について $\vec n\cdot\VV{AP}=0$。(3) $ax+by+c=0$ の法線ベクトルは $(a,\ b)$。2直線のなす角は法線ベクトルのなす角（またはその補角）なので，$\cos\theta=\dfrac{|\vec{n_1}\cdot\vec{n_2}|}{|\vec{n_1}||\vec{n_2}|}$。",
  "sol": r"(1) $(x,\ y)=(1,\ 2)+t(3,\ -1)$ より　$\boldsymbol{x=1+3t,\ \ y=2-t}$<br>"
         r"第2式から $t=2-y$ を第1式に代入して $x=7-3y$，すなわち　$\boldsymbol{x+3y-7=0}$<br>"
         r"(2) 直線上の点を P$(x,\ y)$ とすると $\vec n\cdot\VV{AP}=0$ より $2(x-1)+3(y-2)=0$　∴ $\boldsymbol{2x+3y-8=0}$<br>"
         r"(3) 法線ベクトルは $\vec{n_1}=(1,\ -3)$，$\vec{n_2}=(2,\ -1)$。$\vec{n_1}\cdot\vec{n_2}=2+3=5$，$|\vec{n_1}||\vec{n_2}|=\sqrt{10}\sqrt5=5\sqrt2$ より<br>"
         r"$\cos\theta=\dfrac{5}{5\sqrt2}=\dfrac{1}{\sqrt2}$　∴ $\boldsymbol{\theta=45^\circ}$",
  "note": r"(3) で内積が負になるときは，法線ベクトルのなす角は鈍角なので，その補角が2直線のなす角になる（絶対値をつける理由）。方向ベクトル $(3,\ 1)$，$(1,\ 2)$ のなす角で考えてもよい。",
  "ex": r"(1) 点 A(−2, 1) を通り $\vec d=(2,5)$ に平行な直線を媒介変数表示し，$t$ を消去した方程式を求めよ。(2) 点 A(−2, 1) を通り $\vec n=(4,-1)$ に垂直な直線の方程式を求めよ。(3) 2直線 $x+\sqrt3y=1$，$x-\sqrt3y=2$ のなす角（$0^\circ$ 以上 $90^\circ$ 以下）を求めよ。",
  "exa": r"(1) $x=-2+2t,\ y=1+5t$；$5x-2y+12=0$　(2) $4x-y+9=0$　(3) $60^\circ$"},
 {"lv": 2, "title": "円のベクトル方程式と接線",
  "q": r"O を原点とし，一直線上にない3点 O，A$(\vec a)$，B$(\vec b)$ がある。<br>(1) 次のベクトル方程式を満たす点 P$(\vec p)$ 全体はどのような図形か。<br>　(ア) $|3\vec p-\vec a-2\vec b|=6$　(イ) $(\vec p-\vec a)\cdot(2\vec p-\vec b)=0$<br>(2) 円 $(x-1)^2+(y-2)^2=10$ 上の点 (2, 5) における接線の方程式を，ベクトルを用いて求めよ。",
  "hint": r"(ア) $\vec p$ の係数 3 でくくって $|\vec p-\vec c|=r$ の形にする。(イ) $2\vec p-\vec b=2\left(\vec p-\dfrac{\vec b}{2}\right)$ と変形すると，$(\vec p-\vec a)\cdot(\vec p-\vec m)=0$ の形（直径の両端が A と M）。(2) 接線は接点を通る半径に垂直。",
  "sol": r"(1)(ア) $\left|3\left(\vec p-\dfrac{\vec a+2\vec b}{3}\right)\right|=6$ より $\left|\vec p-\dfrac{\vec a+2\vec b}{3}\right|=2$。<br>"
         r"$\dfrac{\vec a+2\vec b}{3}$ は線分 AB を 2:1 に内分する点の位置ベクトルなので　<b>線分 AB を 2:1 に内分する点を中心とする半径 2 の円</b><br>"
         r"(イ) $2(\vec p-\vec a)\cdot\left(\vec p-\dfrac{\vec b}{2}\right)=0$。線分 OB の中点を M$\left(\dfrac{\vec b}{2}\right)$ とすると $\VV{AP}\cdot\VV{MP}=0$ で，これは P＝A，P＝M または ∠APM＝90° を表す。<br>"
         r"よって　<b>2点 A，M（M は線分 OB の中点）を直径の両端とする円</b><br>"
         r"(2) 中心を C(1, 2)，接点を $\mathrm{P_0}$(2, 5) とすると $\VV{CP_0}=(1,\ 3)$。接線上の点 P$(x,\ y)$ について $\VV{CP_0}\cdot\VV{P_0P}=0$ より<br>"
         r"$1\cdot(x-2)+3(y-5)=0$　∴ $\boldsymbol{x+3y-17=0}$",
  "note": r"(イ) は展開して平方完成しても，$\left|\vec p-\dfrac{\vec a+\vec m}{2}\right|^2=\dfrac{|\vec a-\vec m|^2}{4}$（中心は AM の中点，半径は $\dfrac12$AM）となり同じ結論。(2) の接線は $(\vec{p_0}-\vec c)\cdot(\vec p-\vec c)=r^2$ の形にすると $(x-1)+3(y-2)=10$ で，やはり $x+3y-17=0$。",
  "ex": r"(1) $|2\vec p+\vec a-3\vec b|=4$ を満たす点 P$(\vec p)$ 全体はどのような図形か。(2) 円 $x^2+y^2-4x+2y=0$ 上の点 (3, 1) における接線の方程式を求めよ。",
  "exa": r"(1) 線分 AB を 3:1 に外分する点を中心とする半径 2 の円　(2) $x+2y-5=0$"},
 {"lv": 3, "title": "点と直線の距離（法線ベクトルによる導出）",
  "q": r"(1) 点 P$(x_0,\ y_0)$ と直線 $\ell:\ ax+by+c=0$ の距離 $d$ が $d=\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}$ であることを，法線ベクトルを用いて示せ。<br>(2) 点 (3, 1) から直線 $3x+4y-3=0$ に下ろした垂線の足 H の座標と，点と直線の距離を求めよ。",
  "hint": r"$\vec n=(a,\ b)$ は $\ell$ の法線ベクトル。垂線の足 H について $\VV{PH}\parallel\vec n$ だから $\VV{PH}=k\vec n$ とおき，H が $\ell$ 上にある条件から $k$ を求める。距離は $|\VV{PH}|=|k||\vec n|$。",
  "sol": r"(1) $\vec n=(a,\ b)$ は $\ell$ の法線ベクトル（$\vec n\neq\vec 0$）。P から $\ell$ に下ろした垂線の足を H とすると $\VV{PH}\parallel\vec n$ なので $\VV{PH}=k\vec n$ とおけ，H$(x_0+ka,\ y_0+kb)$。<br>"
         r"H は $\ell$ 上にあるから $a(x_0+ka)+b(y_0+kb)+c=0$，$k=-\dfrac{ax_0+by_0+c}{a^2+b^2}$<br>"
         r"よって　$d=|\VV{PH}|=|k||\vec n|=\dfrac{|ax_0+by_0+c|}{a^2+b^2}\cdot\sqrt{a^2+b^2}=\dfrac{|ax_0+by_0+c|}{\sqrt{a^2+b^2}}$ ■<br>"
         r"(2) $\vec n=(3,\ 4)$，$k=-\dfrac{9+4-3}{25}=-\dfrac25$ より H$\left(3-\dfrac65,\ 1-\dfrac85\right)$，すなわち　$\boldsymbol{\mathrm{H}\left(\dfrac95,\ -\dfrac35\right)}$<br>"
         r"距離は　$|k||\vec n|=\dfrac25\cdot5=\boldsymbol{2}$",
  "note": r"別解：$\ell$ 上の1点 Q をとると，$d$ は $\VV{QP}$ の $\vec n$ 方向への正射影の長さで $d=\dfrac{|\VV{QP}\cdot\vec n|}{|\vec n|}$。Q$(x_1,\ y_1)$ なら $\VV{QP}\cdot\vec n=a(x_0-x_1)+b(y_0-y_1)=ax_0+by_0+c$（$ax_1+by_1=-c$）となり同じ式を得る。",
  "ex": r"点 (−1, 4) から直線 $x-2y+4=0$ に下ろした垂線の足の座標と，点と直線の距離を求めよ。",
  "exa": r"垂線の足 (0, 2)，距離 $\sqrt5$"},
 {"lv": 4, "title": "内積の条件を満たす点の軌跡（重心が中心の円）",
  "q": r"OA＝3，OB＝2，∠AOB＝60° の △OAB がある。点 P が<br>$\VV{PO}\cdot\VV{PA}+\VV{PA}\cdot\VV{PB}+\VV{PB}\cdot\VV{PO}=0$<br>を満たしながら動くとき，点 P の軌跡を求めよ。",
  "hint": r"始点を O にそろえて $\vec p=\VV{OP}$ で展開すると，$|\vec p|^2$ の項と $\vec p$ の1次の項が現れる。$|\vec p|^2$ の係数でくくって平方完成し，$|\vec p-\vec c|=r$ の形にする。",
  "sol": r"$\vec a=\VV{OA}$，$\vec b=\VV{OB}$，$\vec p=\VV{OP}$ とすると $|\vec a|=3$，$|\vec b|=2$，$\vec a\cdot\vec b=3\cdot2\cos60^\circ=3$。<br>"
         r"$\VV{PO}=-\vec p$，$\VV{PA}=\vec a-\vec p$，$\VV{PB}=\vec b-\vec p$ を代入して<br>"
         r"$-\vec p\cdot(\vec a-\vec p)+(\vec a-\vec p)\cdot(\vec b-\vec p)+(\vec b-\vec p)\cdot(-\vec p)=0$<br>"
         r"$3|\vec p|^2-2(\vec a+\vec b)\cdot\vec p+\vec a\cdot\vec b=0$<br>"
         r"$\left|\vec p-\dfrac{\vec a+\vec b}{3}\right|^2=\dfrac{|\vec a+\vec b|^2}{9}-\dfrac{\vec a\cdot\vec b}{3}=\dfrac{|\vec a|^2-\vec a\cdot\vec b+|\vec b|^2}{9}=\dfrac{9-3+4}{9}=\dfrac{10}{9}$<br>"
         r"$\dfrac{\vec a+\vec b}{3}$ は △OAB の重心 G の位置ベクトル（$\vec 0$ は O）だから，<br>"
         r"P の軌跡は　<b>△OAB の重心を中心とする半径 $\boldsymbol{\dfrac{\sqrt{10}}{3}}$ の円</b>",
  "note": r"$|\vec a|^2-\vec a\cdot\vec b+|\vec b|^2=\dfrac{\mathrm{OA}^2+\mathrm{OB}^2+\mathrm{AB}^2}{2}$ なので，半径の2乗は $\dfrac{\mathrm{OA}^2+\mathrm{OB}^2+\mathrm{AB}^2}{18}$ と対称な形に書ける（ここでは AB$^2=7$ で $\dfrac{20}{18}=\dfrac{10}{9}$）。3つの頂点に対して対称な条件なので，中心が重心になるのは自然である。",
  "ex": r"1辺の長さが3の正三角形 ABC がある。点 P が $\VV{PA}\cdot\VV{PB}+\VV{PB}\cdot\VV{PC}+\VV{PC}\cdot\VV{PA}=3$ を満たしながら動くとき，点 P の軌跡を求めよ。",
  "exa": r"△ABC の重心を中心とする半径 $\dfrac{\sqrt{10}}{2}$ の円"},
]})

# ================================================================ 節8
def _fig_region1():
    T = _tr(22, 112, 44)
    O, A, B = (0, 0), (1.6, 0), (0.5, 1.0)
    A2, B2, M = (3.2, 0), (1.0, 2.0), (0.25, 0.5)
    b = _pg([T(O), T(A2), T(B2)], FILL, "none", 0, 0.8)
    b += _ln(T(_mix(A2, B2, -0.12)), T(_mix(A2, B2, 1.12)), RD, 1.3)
    b += _ln(T(O), T(A2), "#333", 1.0) + _ln(T(O), T(B2), "#333", 1.0) + _ln(T(A), T(B), "#333", 1.0)
    b += _ln(T(A), T(M), GR, 1.8)
    for X, nm, an in ((O, "O", 200), (A, "A", -90), (B, "B", 160), (A2, "A'", -90), (B2, "B'", 160), (M, "M", 160)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(196, 130, b)

def _fig_region2():
    T = _tr(14, 122, 40)
    O, A = (0, 0), (2, 0)
    B = (1.5, 1.5*math.sqrt(3))
    A1, B1, A3, B3 = (1, 0), (B[0]/3, B[1]/3), (3, 0), B
    b = _pg([T(A1), T(A3), T(B3), T(B1)], FILL, "#333", 1.1, 0.9)
    b += _ln(T(O), T(A3), "#333", 1.0) + _ln(T(O), T(B3), "#333", 1.0) + _ln(T(A), T(B), "#888", 0.9, "3,2")
    for X, nm, an in ((O, "O", 200), (A, "A", -90), (B, 'B=B<tspan font-size="8" dy="2">3</tspan>', 160), (A1, 'A<tspan font-size="8" dy="2">1</tspan>', -90), (B1, 'B<tspan font-size="8" dy="2">1</tspan>', 160), (A3, 'A<tspan font-size="8" dy="2">3</tspan>', -90)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 10, 10)
    return _svg(150, 136, b)

def _fig_region3():
    T = _tr(16, 94, 50)
    O, A, B = (0, 0), (2.0, 0.4), (0.6, 1.2)
    C, D = (2.6, 1.6), (1.4, -0.8)
    b = _pg([T(O), T(C), T(D)], FILL, "#333", 1.1, 0.9)
    b += _ar(T(O), T(A), BL, 1.3) + _ar(T(O), T(B), RD, 1.3)
    b += _ln(T(A), T(C), "#888", 0.8, "3,2") + _ln(T(B), T(C), "#888", 0.8, "3,2")
    for X, nm, an in ((O, "O", 180), (A, "A", -30), (B, "B", 120), (C, "C", 30), (D, "D", -30)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(160, 150, b)

def _fig_hexregion():
    T = _tr(14, 132, 48)
    A, B, C = (0.9, 2.4), (0, 0), (3.0, 0)
    pts = [_mix(A, B, 1/3), _mix(A, B, 2/3), _mix(B, C, 1/3), _mix(B, C, 2/3), _mix(C, A, 1/3), _mix(C, A, 2/3)]
    b = _pg([T(A), T(B), T(C)]) + _pg([T(p) for p in pts], FILL, BL, 1.1, 0.9)
    for p in pts:
        b += _dot(T(p), 1.8, BL)
    G = ((A[0] + B[0] + C[0])/3, (A[1] + B[1] + C[1])/3)
    b += _dot(T(G)) + _lab(T(G), 'G<tspan font-size="8" dy="2">0</tspan>', -90, 9, 10)
    for X, nm, an in ((A, "A", 90), (B, "B", 225), (C, "C", -45)):
        b += _lab(T(X), nm, an, 9, 10)
    return _svg(176, 148, b)

def _fig_stadium():
    T = _tr(90, 64, 26)
    outer = [(-1, 2), (1, 2)] + [(1 + 2*math.cos(math.radians(g)), 2*math.sin(math.radians(g))) for g in range(90, -91, -6)]
    outer += [(-1, -2)] + [(-1 + 2*math.cos(math.radians(g)), 2*math.sin(math.radians(g))) for g in range(270, 89, -6)]
    lens = [(-1 + 2*math.cos(math.radians(g)), 2*math.sin(math.radians(g))) for g in range(60, -61, -5)]
    lens += [(1 + 2*math.cos(math.radians(g)), 2*math.sin(math.radians(g))) for g in range(240, 119, -5)]
    def path(ps):
        q = [T(p) for p in ps]
        return "M" + " L".join(f"{_n(x)},{_n(y)}" for x, y in q) + " Z"
    b = f'<path d="{path(outer)} {path(lens)}" fill="{FILL}" fill-rule="evenodd" stroke="{BL}" stroke-width="1.1"/>'
    b += _ln(T((-3.3, 0)), T((3.3, 0)), "#999", 0.7) + _ln(T((0, -2.3)), T((0, 2.3)), "#999", 0.7)
    b += _ln(T((-1, 0)), T((1, 0)), RD, 2.2)
    b += _cir(T((0.4, 0)), 52, "#888", 0.8, "none", "3,2")
    for X, nm, an in (((-1, 0), "A", -120), ((1, 0), "B", -60), ((0, 0), "O", 120)):
        b += _dot(T(X)) + _lab(T(X), nm, an, 9, 10)
    return _svg(180, 128, b)

SEC.append({"title": "点の存在範囲",
"base": r"""$\VV{OP}=s\VV{OA}+t\VV{OB}$（$\VV{OA},\ \VV{OB}$ は1次独立）のとき<br>
・$s+t=1$ $\iff$ P は直線 AB 上。さらに $s\geqq0,\ t\geqq0$ $\iff$ 線分 AB 上<br>
・$s+t\leqq1,\ s\geqq0,\ t\geqq0$ $\iff$ △OAB の周および内部　・$0\leqq s\leqq1,\ 0\leqq t\leqq1$ $\iff$ OA，OB を2辺とする平行四辺形の周および内部<br>
・$ps+qt=k$ の形は，$\VV{OP}=\dfrac{ps}{k}\left(\dfrac kp\VV{OA}\right)+\dfrac{qt}{k}\left(\dfrac kq\VV{OB}\right)$ と変形して「係数の和を1」にする<br>
・$(s,\ t)$ を斜交座標と見ると，P の範囲の面積は $(s,\ t)$ 平面での面積の $2\triangle\mathrm{OAB}$ 倍""",
"items": [
 {"lv": 2, "title": "点の存在範囲の基本（係数の和を1にする）",
  "q": _fig_region1() + r"△OAB において $\VV{OP}=s\VV{OA}+t\VV{OB}$ とする。実数 $s,\ t$ が次の条件を満たして動くとき，点 P の存在範囲を求めよ。<br>(1) $s+t=2$　(2) $s+t\leqq2,\ s\geqq0,\ t\geqq0$　(3) $s+2t=1,\ s\geqq0,\ t\geqq0$",
  "hint": r"「係数の和が1」の形にすれば直線（係数がともに 0 以上なら線分）になる。条件の数をベクトルの側に移す：$s+t=2$ なら $\VV{OP}=\dfrac s2(2\VV{OA})+\dfrac t2(2\VV{OB})$。不等式のときは $s+t=k$ と固定してから $k$ を動かす。",
  "sol": r"$\VV{OA'}=2\VV{OA}$，$\VV{OB'}=2\VV{OB}$ となる点 A'，B' をとる。<br>"
         r"(1) $\VV{OP}=\dfrac s2\VV{OA'}+\dfrac t2\VV{OB'}$，$\dfrac s2+\dfrac t2=1$ で，$s$ はすべての実数をとるから　<b>直線 A'B'</b>（図の赤線）<br>"
         r"(2) $s+t=k$ とおくと $0\leqq k\leqq2$。$k=0$ のとき P＝O。$0<k\leqq2$ のとき $\VV{OP}=\dfrac sk(k\VV{OA})+\dfrac tk(k\VV{OB})$ で，係数は 0 以上で和が1だから，P は $k\VV{OA}$，$k\VV{OB}$ を結ぶ線分（AB に平行）上を動く。$k$ を 0 から 2 まで動かすと，この線分は O から A'B' まで平行に動く。<br>"
         r"よって　<b>△OA'B' の周および内部</b>（図の網かけ部分）<br>"
         r"(3) 辺 OB の中点を M とすると $\VV{OP}=s\VV{OA}+2t\VV{OM}$，$s+2t=1$，$s\geqq0$，$2t\geqq0$ だから　<b>線分 AM</b>（図の緑の線分）",
  "note": r"「係数の和が1」かつ「係数がともに 0 以上」⟺ 線分上，が基本。$ps+qt=1$ の形は，係数 $p,\ q$ をベクトルの側に押しつけて $\VV{OP}=(ps)\left(\dfrac1p\VV{OA}\right)+(qt)\left(\dfrac1q\VV{OB}\right)$ とする。",
  "ex": r"△OAB において $\VV{OP}=s\VV{OA}+t\VV{OB}$ とする。次の条件のとき，点 P の存在範囲を求めよ。(1) $s+t=\dfrac12$　(2) $2s+3t\leqq6,\ s\geqq0,\ t\geqq0$",
  "exa": r"(1) 辺 OA，OB の中点を通る直線　(2) $\VV{OA'}=3\VV{OA}$，$\VV{OB'}=2\VV{OB}$ となる点 A'，B' をとった △OA'B' の周および内部"},
 {"lv": 3, "title": "存在範囲の面積（係数の1次式が範囲をもつ場合）",
  "q": _fig_region2() + r"OA＝2，OB＝3，∠AOB＝60° の △OAB がある。$\VV{OP}=s\VV{OA}+t\VV{OB}$ で，実数 $s,\ t$ が $1\leqq2s+3t\leqq3,\ s\geqq0,\ t\geqq0$ を満たして動くとき，点 P の存在範囲の面積を求めよ。",
  "hint": r"$2s+3t=k$ と固定すると，P は AB に平行な線分上を動く。$k$ を 1 から 3 まで動かすと，その線分が平行移動しながら台形を描く。",
  "sol": r"$2s+3t=k$（$1\leqq k\leqq3$）とおき，$k$ を固定すると<br>"
         r"$\VV{OP}=\dfrac{2s}{k}\left(\dfrac k2\VV{OA}\right)+\dfrac{3t}{k}\left(\dfrac k3\VV{OB}\right)$，$\dfrac{2s}{k}+\dfrac{3t}{k}=1$，$\dfrac{2s}{k}\geqq0$，$\dfrac{3t}{k}\geqq0$<br>"
         r"よって P は，$\dfrac k2\VV{OA}$ と $\dfrac k3\VV{OB}$ の終点を結ぶ線分上を動く。この線分は $k$ によらず一定の向きで，$k$ が 1 から 3 まで動くと平行移動する。<br>"
         r"$\VV{OA_1}=\dfrac12\VV{OA}$，$\VV{OB_1}=\dfrac13\VV{OB}$，$\VV{OA_3}=\dfrac32\VV{OA}$，$\VV{OB_3}=\VV{OB}$ とすると，存在範囲は台形 $\mathrm{A_1A_3B_3B_1}$ の周および内部。<br>"
         r"$\triangle\mathrm{OAB}=\dfrac12\cdot2\cdot3\sin60^\circ=\dfrac{3\sqrt3}{2}$ で<br>"
         r"$\triangle\mathrm{OA_3B_3}=\dfrac32\cdot1\cdot\triangle\mathrm{OAB}=\dfrac{9\sqrt3}{4}$，$\triangle\mathrm{OA_1B_1}=\dfrac12\cdot\dfrac13\cdot\triangle\mathrm{OAB}=\dfrac{\sqrt3}{4}$<br>"
         r"求める面積は　$\dfrac{9\sqrt3}{4}-\dfrac{\sqrt3}{4}=\boldsymbol{2\sqrt3}$",
  "note": r"斜交座標の考え：$(s,\ t)$ 平面で条件の表す領域の面積は $\dfrac12\cdot\dfrac32\cdot1-\dfrac12\cdot\dfrac12\cdot\dfrac13=\dfrac23$。P の世界では面積が「OA，OB を2辺とする平行四辺形の面積 $2\triangle\mathrm{OAB}=3\sqrt3$」倍になるので $\dfrac23\cdot3\sqrt3=2\sqrt3$ と求めてもよい。",
  "ex": r"OA＝4，OB＝3，∠AOB＝90° の △OAB がある。$\VV{OP}=s\VV{OA}+t\VV{OB}$ で，実数 $s,\ t$ が $2\leqq s+2t\leqq4,\ s\geqq0,\ t\geqq0$ を満たして動くとき，点 P の存在範囲の面積を求めよ。",
  "exa": r"$36$"},
 {"lv": 4, "title": "係数の置きかえによる存在範囲",
  "q": _fig_region3() + r"△OAB の面積を $S$ とする。実数 $s,\ t$ が $s\geqq0,\ t\geqq0,\ s+t\leqq1$ を満たして動くとき，<br>$\VV{OP}=(s+t)\VV{OA}+(s-t)\VV{OB}$<br>で定まる点 P の存在範囲を求め，その面積を $S$ で表せ。",
  "hint": r"$\VV{OA},\ \VV{OB}$ の係数 $u=s+t$，$v=s-t$ を新しい変数とし，$s,\ t$ についての条件を $u,\ v$ の条件に書き直す（$s,\ t$ を $u,\ v$ で表して代入）。逆に，その条件を満たす $(u,\ v)$ にはもとの $(s,\ t)$ が対応することも確認する。",
  "sol": r"$u=s+t$，$v=s-t$ とおくと $s=\dfrac{u+v}{2}$，$t=\dfrac{u-v}{2}$ で，$(s,\ t)$ と $(u,\ v)$ は1対1に対応する。条件は<br>"
         r"$s\geqq0\iff v\geqq-u$，$t\geqq0\iff v\leqq u$，$s+t\leqq1\iff u\leqq1$<br>"
         r"よって，$\VV{OP}=u\VV{OA}+v\VV{OB}$ で $(u,\ v)$ が「$-u\leqq v\leqq u\leqq1$」を満たして動くときの P の範囲を求めればよい。<br>"
         r"$u$ を固定すると（$0\leqq u\leqq1$），$v$ は $-u$ から $u$ まで動き，P は $u(\VV{OA}-\VV{OB})$ と $u(\VV{OA}+\VV{OB})$ の終点を結ぶ線分上を動く。<br>"
         r"$\VV{OC}=\VV{OA}+\VV{OB}$，$\VV{OD}=\VV{OA}-\VV{OB}$ とすると，この線分は CD に平行で，$u$ が 0 から 1 まで動くと O から CD まで動く。<br>"
         r"ゆえに存在範囲は　<b>△OCD の周および内部</b><br>"
         r"A は線分 CD の中点（$\dfrac{\VV{OC}+\VV{OD}}{2}=\VV{OA}$）だから △OCD＝2△OAC。四角形 OACB は平行四辺形なので △OAC＝△OAB＝$S$。<br>"
         r"よって面積は　$\boldsymbol{2S}$",
  "note": r"斜交座標で見ると，$(u,\ v)$ 平面での領域 $-u\leqq v\leqq u\leqq1$ は面積 1 の三角形で，P の世界ではその $2S$ 倍になる。もとの $(s,\ t)$ 平面の三角形（面積 $\dfrac12$）が，置きかえで面積 2 倍の三角形に移ったと見ることもできる。",
  "ex": r"△OAB の面積を $S$ とする。実数 $s,\ t$ が $s\geqq0,\ t\geqq0,\ s+t\leqq1$ を満たして動くとき，$\VV{OP}=(2s+t)\VV{OA}+(s+t)\VV{OB}$ で定まる点 P の存在範囲を求め，その面積を $S$ で表せ。",
  "exa": r"$\VV{OC}=\VV{OA}+\VV{OB}$，$\VV{OE}=2\VV{OA}+\VV{OB}$ とした △OCE の周および内部，面積 $S$"},
 {"lv": 5, "title": "3つの動点の重心の存在範囲",
  "q": _fig_hexregion() + r"面積が1の △ABC の辺 BC，CA，AB 上（端点を含む）を，それぞれ点 P，Q，R が互いに無関係に動く。$\VV{AG}=\dfrac13(\VV{AP}+\VV{AQ}+\VV{AR})$ で定まる点 G（△PQR の重心）の存在範囲を求め，その面積を求めよ。",
  "hint": r"3つの動点を媒介変数 $u,\ v,\ w$ で表すと，$\VV{AG}=X\VV{AB}+Y\VV{AC}$ の $X,\ Y$ が $u,\ v,\ w$ の1次式になる。まず $u$ を固定して $v,\ w$ を動かし（「1文字を固定して残りを動かす」），次に $u$ を動かす。斜交座標 $(X,\ Y)$ で領域を求めてから図形に戻す。",
  "sol": r"$\VV{AB}=\vec b$，$\VV{AC}=\vec c$ とする。$0\leqq u,\ v,\ w\leqq1$ を用いて<br>"
         r"$\VV{AP}=(1-u)\vec b+u\vec c$，$\VV{AQ}=(1-v)\vec c$，$\VV{AR}=w\vec b$<br>"
         r"と表せ，$u,\ v,\ w$ は互いに無関係に $0$ から $1$ まで動く。よって<br>"
         r"$\VV{AG}=X\vec b+Y\vec c$，　$X=\dfrac{1-u+w}{3}$，$Y=\dfrac{1+u-v}{3}$<br>"
         r"<b>[1] $u$ を固定する。</b> $w,\ v$ が独立に $0$ から $1$ まで動くので，$(X,\ Y)$ は<br>"
         r"$\dfrac{1-u}{3}\leqq X\leqq\dfrac{2-u}{3}$，$\dfrac u3\leqq Y\leqq\dfrac{1+u}{3}$ ……①<br>"
         r"の範囲（斜交座標での1辺 $\dfrac13$ の正方形）をすべて動く。<br>"
         r"<b>[2] $u$ を動かす。</b> 点 $(X,\ Y)$ が存在範囲に入る $\iff$ ①を満たす $u$（$0\leqq u\leqq1$）がある $\iff$<br>"
         r"$1-3X\leqq u\leqq2-3X$，$3Y-1\leqq u\leqq3Y$，$0\leqq u\leqq1$ を同時に満たす $u$ がある。<br>"
         r"これは「3つの下限 $1-3X,\ 3Y-1,\ 0$ のどれもが3つの上限 $2-3X,\ 3Y,\ 1$ のどれ以下でもある」ことと同値で，整理すると<br>"
         r"$0\leqq X\leqq\dfrac23$，$0\leqq Y\leqq\dfrac23$，$\dfrac13\leqq X+Y\leqq1$ ……②<br>"
         r"<b>[3] 図形に戻す。</b> ②は $(X,\ Y)$ で6点 $\left(\dfrac13,0\right)$，$\left(\dfrac23,0\right)$，$\left(\dfrac23,\dfrac13\right)$，$\left(\dfrac13,\dfrac23\right)$，$\left(0,\dfrac23\right)$，$\left(0,\dfrac13\right)$ を頂点とする六角形を表す。これらは順に，辺 AB，BC，CA を3等分する6個の点である（例えば $\dfrac23\vec b+\dfrac13\vec c$ は辺 BC を 1:2 に内分する点）。<br>"
         r"よって G の存在範囲は　<b>各辺を3等分する6個の点を頂点とする六角形の周および内部</b><br>"
         r"その面積は，△ABC から各頂点のところの3つの三角形（どれも △ABC と相似比 $\dfrac13$ で面積 $\dfrac19$）を除いて　$1-3\cdot\dfrac19=\boldsymbol{\dfrac23}$",
  "note": r"六角形は △ABC の重心 $\mathrm{G_0}$ に関して点対称で，「3つの線分 $\dfrac13\mathrm{BC}$，$\dfrac13\mathrm{CA}$，$\dfrac13\mathrm{AB}$ を“足し合わせた”図形」になっている。[2] の「固定した $u$ ごとの正方形が，$u$ とともに斜めに平行移動して掃く範囲」と図形的に見てもよい。2点だけが動く場合は平行四辺形になる（練習）。",
  "ex": r"面積が1の △ABC の辺 BC 上を点 P，辺 CA 上を点 Q が（端点を含めて）互いに無関係に動くとき，線分 PQ を 1:2 に内分する点 X の存在範囲の面積を求めよ。",
  "exa": r"$\dfrac49$（辺 AB の B 寄りの3等分点，辺 BC の B 寄りの3等分点，C，辺 CA の C 寄りの3等分点を頂点とする平行四辺形）"},
 {"lv": 5, "title": "ベクトルの和で定まる点の存在範囲（円が掃く範囲）",
  "q": _fig_stadium() + r"座標平面上に2点 A(−1, 0)，B(1, 0) があり，O を原点とする。点 P が線分 AB 上を，点 Q が円 $x^2+y^2=4$ 上を，それぞれ互いに無関係に動くとき，$\VV{OR}=\VV{OP}+\VV{OQ}$ で定まる点 R の存在範囲を求め，その面積を求めよ。",
  "hint": r"$\VV{PR}=\VV{OQ}$ だから，R は「P を中心とする半径 2 の円」の周上にある。P を動かしたときの円の通過範囲を，「R を固定して，PR＝2 となる P が線分 AB 上にあるか」と言いかえる。距離 PR は P とともに連続的に変わるので，最小値と最大値の間の値はすべてとる。",
  "sol": r"$\VV{PR}=\VV{OR}-\VV{OP}=\VV{OQ}$ より PR＝2。逆に PR＝2 なら $\VV{OQ}=\VV{PR}$ で Q を定めればよい。よって<br>"
         r"R が存在範囲に入る $\iff$ 線分 AB 上に PR＝2 となる点 P がある<br>"
         r"R を固定し，P を線分 AB 上で A から B まで動かすと，距離 PR は連続的に変化する。その最小値を $d_1$（R と線分 AB の距離），最大値を $d_2$ とすると，PR は $d_1$ 以上 $d_2$ 以下のすべての値をとる。R から直線 AB に下ろした垂線の足を K とすると PR$^2$＝RK$^2$＋KP$^2$ で，KP は P が線分の端にあるとき最大になるから $d_2=\max\{\mathrm{RA},\ \mathrm{RB}\}$。したがって<br>"
         r"R が存在範囲に入る $\iff d_1\leqq2\leqq d_2\iff$「R と線分 AB の距離が 2 以下」かつ「RA$\geqq2$ または RB$\geqq2$」<br>"
         r"前者を満たす点全体を $D$ とすると，$D$ は長方形 $-1\leqq x\leqq1,\ -2\leqq y\leqq2$ と，A，B を中心とする半径 2 の円の周および内部をあわせた図形である。<br>"
         r"後者の否定「RA＜2 かつ RB＜2」を満たす点全体を $L$ とすると，$L$ は2つの円の内部の共通部分（レンズ形）である。<br>"
         r"よって存在範囲は　<b>$D$ から $L$ を除いた部分</b>（図の網かけ部分）<br>"
         r"［面積］$D=2\cdot4+\pi\cdot2^2=8+4\pi$（長方形と左右の半円2つ）。<br>"
         r"2円は中心間の距離が 2，半径が 2 で，交点は $(0,\ \pm\sqrt3)$。$L$ は中心角 $120^\circ$ の弓形2つ分なので<br>"
         r"$L=2\left(\dfrac12\cdot2^2\cdot\dfrac{2\pi}{3}-\dfrac12\cdot2^2\sin120^\circ\right)=\dfrac{8\pi}{3}-2\sqrt3$<br>"
         r"求める面積は　$8+4\pi-\left(\dfrac{8\pi}{3}-2\sqrt3\right)=\boldsymbol{8+\dfrac{4\pi}{3}+2\sqrt3}$",
  "note": r"Q が円の周<b>および内部</b>を動くなら，答えは $D$ そのもので面積は $8+4\pi$。周だけを動くときは，P がどこにあっても PR＜2 となってしまう中央のレンズ形の部分に「穴」があく。この穴を見落とすのが典型的な誤り。「動くものを固定して，条件を満たすものが存在するか」と逆に考えるのが，存在範囲・通過範囲の基本である。",
  "ex": r"2点 A(−1, 0)，B(1, 0) について，点 P が線分 AB 上を，点 Q が円 $x^2+y^2=2$ 上を互いに無関係に動くとき，$\VV{OR}=\VV{OP}+\VV{OQ}$ で定まる点 R の存在範囲の面積を求めよ。",
  "exa": r"$4\sqrt2+\pi+2$"},
]})

# ==== 節の終わり ====

def _fix(s):
    return re.sub(r"\\VV\{([^{}]*)\}", lambda m: r"\overrightarrow{\mathrm{" + m.group(1) + "}}", s)

for _s in SEC:
    _s["base"] = _fix(_s["base"])
    for _it in _s["items"]:
        for _k in list(_it):
            if isinstance(_it[_k], str):
                _it[_k] = _fix(_it[_k])

CH = {"no": 18, "sections": SEC}


# ================================================================ 検算
def _z(M):
    return all(simplify(e) == 0 for e in M)

def _close(x, y, eps=1e-9):
    return abs(x - y) < eps

def _v1():
    a1, a2, b1, b2 = symbols("a1 a2 b1 b2")
    a, b = Matrix([a1, a2]), Matrix([b1, b2])
    x = 3*a + b
    assert _z(3*(x - 2*a) + 2*b - (x + 4*b))
    x, y = (a + 2*b)/5, (2*a - b)/5
    assert _z(x + 2*y - a) and _z(2*x - y - b)
    x = (-2*a + 3*b)/5
    assert _z(2*(x + a) - 3*(b - x))
    x, y = (2*a + b)/7, (-a + 3*b)/7
    assert _z(3*x - y - a) and _z(x + 2*y - b)
    # 正六角形
    r3 = sqrt(3)
    P = {"A": (0, 0), "B": (1, 0), "C": (Rational(3, 2), r3/2), "D": (1, r3), "E": (0, r3), "F": (-Rational(1, 2), r3/2)}
    V = lambda X, Y: Matrix(P[Y]) - Matrix(P[X])
    a, b = V("A", "B"), V("A", "F")
    assert _z(V("A", "D") - (2*a + 2*b)) and _z(V("A", "C") - (2*a + b))
    assert _z(V("A", "E") - (a + 2*b)) and _z(V("C", "E") - (-a + b))
    a, b = V("A", "B"), V("A", "C")
    assert _z(V("A", "F") - (-2*a + b)) and _z(V("A", "D") - (-2*a + 2*b))
    # 係数比較・平行
    s, t, k = symbols("s t k")
    assert solve([s + t - 3, 2*s - t], [s, t]) == {s: 1, t: 2}
    assert sorted(solve(k*(k + 5) - 6, k)) == [-6, 1]
    for kk in (1, -6):   # p=(k,2), q=(3,k+5) の行列式
        assert kk*(kk + 5) - 2*3 == 0
    assert solve([2*s + t - 1, s - t + 4], [s, t]) == {s: -1, t: 3}
    assert sorted(solve((k + 1)*k - 6, k)) == [-3, 2]
    # 正五角形（数値）
    R = 1 / (2*math.sin(math.radians(36)))
    pt = {c: (R*math.cos(math.radians(g)), R*math.sin(math.radians(g)))
          for c, g in zip("ABCDE", (90, 162, 234, 306, 18))}
    v = lambda X, Y: (pt[Y][0] - pt[X][0], pt[Y][1] - pt[X][1])
    a, b = v("A", "B"), v("A", "E")
    assert _close(math.hypot(*a), 1)
    tt = (1 + math.sqrt(5)) / 2
    assert _close(math.hypot(*v("A", "C")), tt)
    for X, Y, ca, cb in (("A", "C", tt, 1), ("A", "D", 1, tt)):
        w = v(X, Y)
        assert _close(w[0], ca*a[0] + cb*b[0]) and _close(w[1], ca*a[1] + cb*b[1])
    # BC = AD/t, ED = AC/t, CD = BE/t（向きも）
    for (X, Y), (U, W) in ((("B", "C"), ("A", "D")), (("E", "D"), ("A", "C")), (("C", "D"), ("B", "E"))):
        p_, q_ = v(X, Y), v(U, W)
        assert _close(p_[0], q_[0]/tt) and _close(p_[1], q_[1]/tt)
    # 練習：AC と BE の交点
    A_, C_, B_, E_ = pt["A"], pt["C"], pt["B"], pt["E"]
    d1 = (C_[0] - A_[0], C_[1] - A_[1]); d2 = (E_[0] - B_[0], E_[1] - B_[1])
    det = d1[0]*(-d2[1]) - d1[1]*(-d2[0])
    rx, ry = B_[0] - A_[0], B_[1] - A_[1]
    lam = (rx*(-d2[1]) - ry*(-d2[0])) / det
    AP = (lam*d1[0], lam*d1[1])
    ca, cb = (math.sqrt(5) - 1)/2, (3 - math.sqrt(5))/2
    assert _close(AP[0], ca*a[0] + cb*b[0]) and _close(AP[1], ca*a[1] + cb*b[1])


def _v2():
    s, t, x = symbols("s t x")
    a, b = Matrix([2, -1]), Matrix([-3, 4])
    assert list(3*a + 2*b) == [0, 5] and list(a - b) == [5, -5]
    assert sqrt((a - b).dot(a - b)) == 5*sqrt(2)
    assert solve(list(s*a + t*b - Matrix([7, -6])), [s, t]) == {s: 2, t: -1}
    u = a / sqrt(a.dot(a))
    assert simplify(u[0] - 2*sqrt(5)/5) == 0 and simplify(u[1] + sqrt(5)/5) == 0
    a, b = Matrix([3, 1]), Matrix([-1, 2])
    assert list(2*a + b) == [5, 4]
    assert solve(list(s*a + t*b - Matrix([1, 5])), [s, t]) == {s: 1, t: 2}
    # 平行条件
    assert sorted(solve(1*6 - x*(x + 1), x)) == [-3, 2]
    sol_t = solve((2 - t)*(-4) - (1 + 3*t)*3, t)
    assert sol_t == [Rational(-11, 5)]
    w = Matrix([2, 1]) + sol_t[0]*Matrix([-1, 3])
    assert w == Rational(7, 5)*Matrix([3, -4])
    assert sorted(solve(x*(x + 4) - 12, x)) == [-6, 2]
    assert solve((1 + 3*t) - (2 - t), t) == [Rational(1, 4)]
    # 平行四辺形
    A, B, C = Matrix([1, 2]), Matrix([4, 1]), Matrix([5, 5])
    Ds = [A + C - B, B + C - A, A + B - C]
    assert [list(D) for D in Ds] == [[2, 6], [8, 4], [0, -2]]
    A, B, C = Matrix([-1, 0]), Matrix([3, 2]), Matrix([1, 4])
    assert [list(D) for D in (A + C - B, B + C - A, A + B - C)] == [[-3, 2], [5, 6], [1, -2]]
    # 最小値
    for a, b, t0, m in ((Matrix([3, 1]), Matrix([1, -2]), Rational(-1, 5), 7*sqrt(5)/5),
                        (Matrix([-1, 4]), Matrix([2, 1]), Rational(-2, 5), 9*sqrt(5)/5)):
        f = expand((a + t*b).dot(a + t*b))
        tc = solve(f.diff(t), t)[0]
        assert tc == t0 and simplify(sqrt(f.subs(t, tc)) - m) == 0
        assert (a + t0*b).dot(b) == 0


def _ang(u, v):
    return math.degrees(math.acos((u[0]*v[0] + u[1]*v[1]) / (math.hypot(*u) * math.hypot(*v))))

def _v3():
    x, t = symbols("x t")
    assert _close(_ang((2, 1), (1, 3)), 45) and 2*1 + 1*3 == 5
    assert _close(_ang((3, 1), (-2, 1)), 135) and 3*(-2) + 1*1 == -5
    r3 = math.sqrt(3)
    A, B, C = (0, 0), (2, 0), (1, r3)
    dot = lambda u, v: u[0]*v[0] + u[1]*v[1]
    sub = lambda P, Q: (Q[0] - P[0], Q[1] - P[1])
    assert _close(dot(sub(A, B), sub(A, C)), 2) and _close(dot(sub(A, B), sub(B, C)), -2)
    H = [(0, 0), (1, 0), (1.5, r3/2), (1, r3), (0, r3), (-0.5, r3/2)]
    assert _close(dot(sub(H[0], H[1]), sub(H[0], H[2])), 1.5) and _close(dot(sub(H[0], H[1]), sub(H[2], H[3])), -0.5)
    # 垂直
    assert sorted(solve(x*(x - 3) + 2*x, x)) == [0, 1]
    assert sorted(solve(x*(x + 1) - 6, x)) == [-3, 2]
    for c, u in (((3, -4), (Fr(4, 5), Fr(3, 5))), ((5, 12), (Fr(12, 13), Fr(-5, 13)))):
        assert c[0]*u[0] + c[1]*u[1] == 0 and u[0]**2 + u[1]**2 == 1
    # 大きさの条件（具体的なベクトルで）
    a = Matrix([2, 0]); b = 3*Matrix([cos(pi/3), sin(pi/3)])
    assert simplify((a - b).dot(a - b) - 7) == 0 and simplify(a.dot(b) - 3) == 0
    assert simplify((2*a + b).dot(2*a + b) - 37) == 0
    assert solve(simplify((a + t*b).dot(a - b)), t) == [Rational(1, 6)]
    a = Matrix([3, 0]); b = Matrix([cos(2*pi/3), sin(2*pi/3)])
    assert simplify((a + b).dot(a + b) - 7) == 0 and simplify(a.dot(b) + Rational(3, 2)) == 0
    assert simplify((a - 2*b).dot(a - 2*b) - 19) == 0
    assert solve(simplify((a + t*b).dot(b)), t) == [Rational(3, 2)]
    # a+b+c=0
    for (la, lb, lc), cab, S in (((3, 5, 7), Rational(1, 2), Rational(-83, 2)), ((2, 3, 4), Rational(1, 4), Rational(-29, 2))):
        ab = Rational(lc**2 - la**2 - lb**2, 2)
        assert ab / (la*lb) == cab
        import sympy
        th = sympy.acos(cab)
        a = la*Matrix([1, 0]); b = lb*Matrix([cos(th), sin(th)]); c = -(a + b)
        assert simplify(c.dot(c) - lc**2) == 0
        assert simplify(a.dot(b) + b.dot(c) + c.dot(a) - S) == 0
        if la == 3:
            assert simplify(a.dot(c) / (la*lc) + Rational(11, 14)) == 0
    # 証明：恒等式 |x|^2 = -(x.y) - (z.x)（x+y+z=0）
    p, q, r, s_ = symbols("p q r s")
    X = Matrix([p, q]); Y = Matrix([r, s_]); Z = -X - Y
    assert expand(X.dot(X) + X.dot(Y) + Z.dot(X)) == 0
    # 練習：AB.AC - BA.BC = CA^2 - CB^2
    b = Matrix([p, q]); c = Matrix([r, s_])
    assert expand(b.dot(c) - (-b).dot(c - b) - (c.dot(c) - (c - b).dot(c - b))) == 0
    for _ in range(200):   # 正三角形でない三角形では3つの内積は等しくならない
        P = [(random.uniform(-3, 3), random.uniform(-3, 3)) for _ in range(3)]
        xv, yv, zv = sub(P[0], P[1]), sub(P[1], P[2]), sub(P[2], P[0])
        ls = sorted([math.hypot(*xv), math.hypot(*yv), math.hypot(*zv)])
        if ls[2] - ls[0] > 0.1:
            k = [dot(xv, yv), dot(yv, zv), dot(zv, xv)]
            assert max(k) - min(k) > 1e-6


def _area(P):
    return abs(sum(P[i][0]*P[(i+1) % len(P)][1] - P[(i+1) % len(P)][0]*P[i][1] for i in range(len(P)))) / 2

def _v4():
    assert _area([(1, 1), (4, 2), (2, 5)]) == 5.5 and _area([(-1, 2), (3, -1), (2, 4)]) == 8.5
    assert sqrt(9*16 - 36)/2 == 3*sqrt(3) and sqrt(4*25 - 36)/2 == 4
    # 正三角形の辺 BC 上：B(0,0) C(2,0) A(1,√3)
    r3 = math.sqrt(3)
    vals = []
    for i in range(2001):
        x = 2*i/2000
        vals.append((1 - x)*(-x) + r3*0)
    assert _close(max(vals), 2) and _close(min(vals), -0.25, 1e-6)
    vals = [(-x)*(2 - x) + (-2)*0 for x in [2*i/2000 for i in range(2001)]]   # 正方形 P(x,2), A(0,0), C(2,2)
    assert _close(max(vals), 0) and _close(min(vals), -1, 1e-6)
    # 円周上の点
    for A, B, r, mx, mn in (((4, 0), (0, 2), 1, 1 + 2*math.sqrt(5), 1 - 2*math.sqrt(5)), ((3, 0), (1, 4), math.sqrt(2), 13, -3)):
        vals = []
        for i in range(40000):
            th = 2*math.pi*i/40000
            P = (r*math.cos(th), r*math.sin(th))
            vals.append((A[0] - P[0])*(B[0] - P[0]) + (A[1] - P[1])*(B[1] - P[1]))
        assert abs(max(vals) - mx) < 1e-6 and abs(min(vals) - mn) < 1e-6
    r5 = math.sqrt(5)
    P = (2/r5, 1/r5)
    assert _close((4 - P[0])*(-P[0]) + (-P[1])*(2 - P[1]), 1 - 2*r5)
    # コーシー・シュワルツ
    for c1, c2, mx, f in ((6, 3, 3*math.sqrt(2), lambda X, Y: X + 2*Y), (4, 4/3, 4/math.sqrt(3), lambda X, Y: X + Y)):
        vals = [f(math.sqrt(c1)*math.cos(t), math.sqrt(c2)*math.sin(t)) for t in [2*math.pi*i/40000 for i in range(40000)]]
        assert abs(max(vals) - mx) < 1e-6 and abs(min(vals) + mx) < 1e-6
    assert _close(math.sqrt(2) + 2*math.sqrt(2), 3*math.sqrt(2)) and _close(2*2 + 2*2, 8)  # x=y=√2 で x^2+2y^2=6
    assert _close(3 + 3*(1/3), 4) and _close(math.sqrt(3) + math.sqrt(3)/3, 4/math.sqrt(3))
    # 大きさの条件 → 内積の範囲
    u1, u2, v1, v2 = symbols("u1 u2 v1 v2")
    U, W = Matrix([u1, u2]), Matrix([v1, v2])
    a, b = (U + 2*W)/5, (2*U - W)/5
    assert _z(a + 2*b - U) and _z(2*a - b - W)
    assert expand(a.dot(b) - (2*U.dot(U) + 3*U.dot(W) - 2*W.dot(W))/25) == 0
    a2, b2 = (2*U + W)/3, (U - W)/3
    assert _z(a2 + b2 - U) and _z(a2 - 2*b2 - W)
    assert expand(a2.dot(b2) - (2*U.dot(U) - U.dot(W) - W.dot(W))/9) == 0
    for coef, lo, hi in (((6, 3, 25), 0, 12/25), ((7, -1, 9), 5/9, 1)):
        vals = []
        for i in range(2000):
            for j in (0, 1):
                th, ph = random.uniform(0, 2*math.pi), random.uniform(0, 2*math.pi)
                uu = (2*math.cos(th), 2*math.sin(th)); vv = (math.cos(ph), math.sin(ph))
                if coef[0] == 6:
                    A_ = ((uu[0] + 2*vv[0])/5, (uu[1] + 2*vv[1])/5); B_ = ((2*uu[0] - vv[0])/5, (2*uu[1] - vv[1])/5)
                    assert _close(math.hypot(A_[0] + 2*B_[0], A_[1] + 2*B_[1]), 2) and _close(math.hypot(2*A_[0] - B_[0], 2*A_[1] - B_[1]), 1)
                else:
                    A_ = ((2*uu[0] + vv[0])/3, (2*uu[1] + vv[1])/3); B_ = ((uu[0] - vv[0])/3, (uu[1] - vv[1])/3)
                    assert _close(math.hypot(A_[0] + B_[0], A_[1] + B_[1]), 2) and _close(math.hypot(A_[0] - 2*B_[0], A_[1] - 2*B_[1]), 1)
                vals.append(A_[0]*B_[0] + A_[1]*B_[1])
        assert min(vals) >= lo - 1e-12 and max(vals) <= hi + 1e-12
        assert min(vals) < lo + 0.01 and max(vals) > hi - 0.01
    # 円に内接する三角形
    def dd(A, B, C):
        return (B[0] - A[0])*(C[0] - A[0]) + (B[1] - A[1])*(C[1] - A[1])
    lo, hi = 10, -10
    for _ in range(100000):
        A, B, C = [(math.cos(g), math.sin(g)) for g in (random.uniform(0, 2*math.pi) for _ in range(3))]
        v = dd(A, B, C)
        M = ((B[0] + C[0])/2, (B[1] + C[1])/2)
        assert _close(v, (A[0] - M[0])**2 + (A[1] - M[1])**2 - 1 + M[0]**2 + M[1]**2, 1e-9)
        lo, hi = min(lo, v), max(hi, v)
    assert lo >= -0.5 - 1e-12 and hi < 4
    r3 = math.sqrt(3)
    assert _close(dd((0, 1), (-r3/2, 0.5), (r3/2, 0.5)), -0.5)
    ph = math.pi - 1e-4
    assert dd((0, 1), (-math.sin(ph), math.cos(ph)), (math.sin(ph), math.cos(ph))) > 3.999
    for ph in [0.01*k for k in range(1, 314)]:
        x = math.cos(ph)
        assert _close(dd((0, 1), (-math.sin(ph), x), (math.sin(ph), x)), 2*x*x - 2*x)
    # 練習：和 = (9-|a+b+c|^2)/2 ∈ (0, 9/2]
    hi = 0
    for _ in range(50000):
        P = [(math.cos(g), math.sin(g)) for g in (random.uniform(0, 2*math.pi) for _ in range(3))]
        A, B, C = P
        sm = dd(A, B, C) + dd(B, C, A) + dd(C, A, B)
        h = (A[0] + B[0] + C[0], A[1] + B[1] + C[1])
        assert _close(sm, (9 - h[0]**2 - h[1]**2)/2, 1e-9) and sm > 0
        hi = max(hi, sm)
    assert hi <= 4.5 + 1e-12
    E = [(math.cos(g), math.sin(g)) for g in (0, 2*math.pi/3, 4*math.pi/3)]
    assert _close(dd(E[0], E[1], E[2]) + dd(E[1], E[2], E[0]) + dd(E[2], E[0], E[1]), 4.5)


def _v5():
    a1, a2, b1, b2, c1, c2 = symbols("a1 a2 b1 b2 c1 c2")
    a, b, c = Matrix([a1, a2]), Matrix([b1, b2]), Matrix([c1, c2])
    d = b + Rational(2, 3)*(c - b)                 # BC を 2:1 に内分
    e = (-3*a + b) / (1 - 3)                        # AB を 1:3 に外分
    assert _z(d - (b + 2*c)/3) and _z(e - (3*a - b)/2)
    assert _z(e - d - (9*a - 5*b - 4*c)/6) and _z((a + d + e)/3 - (15*a - b + 4*c)/18)
    # E は AB を 1:3 に外分：AE:EB = 1:3 で外側
    assert _z((e - a) + Rational(1, 2)*(b - a))
    p = a + Rational(3, 5)*(b - a); q = (-1*a + 3*c)/(3 - 1)
    assert _z(p - (2*a + 3*b)/5) and _z(q - (-a + 3*c)/2) and _z(q - p - (-9*a - 6*b + 15*c)/10)
    # 一直線上（A を原点）
    a = zeros(2, 1)
    D, E, F = b/3, c/2, (-b + 2*c)
    assert _z((F - D) - 4*(E - D))
    P, Q, R = 2*b/3, 2*c/5, (-3*b + c)/(1 - 3)
    assert _z((R - P) + Rational(5, 4)*(Q - P))
    # 交点（O を原点，a=(1,0), b=(0,1) で十分：アフィン不変）
    s, t, k = symbols("s t k")
    A, B = Matrix([1, 0]), Matrix([0, 1])
    for rc, rd, OP, OQ, r1, r2 in ((Rational(2, 3), Rational(3, 5), (Rational(4, 9), Rational(1, 3)), (Rational(4, 7), Rational(3, 7)), (3, 4), (7, 2)),
                                   (Rational(1, 2), Rational(2, 3), (Rational(1, 4), Rational(1, 2)), (Rational(1, 3), Rational(2, 3)), (2, 1), (3, 1))):
        C, D = rc*A, rd*B
        sl = solve(list((A + s*(D - A)) - (B + t*(C - B))), [s, t])
        Pp = A + sl[s]*(D - A)
        assert list(Pp) == list(OP)
        kk = 1 / (Pp[0] + Pp[1])
        Qq = kk*Pp
        assert list(Qq) == list(OQ)
        assert Qq[1] / Qq[0] == Rational(r1[0], r1[1])     # AQ:QB = (Bの係数):(Aの係数)
        assert 1 / (kk - 1) == Rational(r2[0], r2[1])
    # l,m,n の点（ランダムな三角形で面積比）
    for (l, m, n), ratio in (((2, 3, 4), (2, 3, 4)), ((3, 1, 2), (3, 1, 2))):
        for _ in range(20):
            A, B, C = [(random.uniform(-5, 5), random.uniform(-5, 5)) for _ in range(3)]
            S = _area([A, B, C])
            if S < 0.5:
                continue
            P = ((l*A[0] + m*B[0] + n*C[0])/(l + m + n), (l*A[1] + m*B[1] + n*C[1])/(l + m + n))
            ar = [_area([P, B, C]), _area([P, C, A]), _area([P, A, B])]
            assert all(_close(ar[i]/ar[0], ratio[i]/ratio[0], 1e-9) for i in range(3))
            D = _meet(A, P, B, C)
            if l == 2:
                assert _close(math.dist(B, D)/math.dist(D, C), 4/3, 1e-9) and _close(math.dist(A, P)/math.dist(P, D), 7/2, 1e-9)
            else:
                assert _close(math.dist(B, D)/math.dist(D, C), 2, 1e-9) and _close(math.dist(A, P), math.dist(P, D), 1e-9)
    # 平行四辺形
    A, B, D = (0, 0), (3, 0), (1, 2); C = (4, 2)
    M = _mix(B, C, 0.5); N = _mix(C, D, 2/3)
    P = _meet(A, M, B, D); Q = _meet(A, N, B, D)
    L = math.dist(B, D)
    assert _close(math.dist(B, P)/L, 1/3) and _close(math.dist(B, Q)/L, 3/4)
    M = _mix(C, D, 0.5); N = _mix(B, C, 1/3)
    P = _meet(A, M, B, D); Q = _meet(A, N, B, D)
    assert _close(math.dist(B, Q)/L, 1/4) and _close(math.dist(B, P)/L, 2/3)
    # 重心を通る直線
    for K, lo, hi, s0 in ((3, 4/9, 1/2, 1/2), (4, 1/4, 1/3, 1/3)):
        vals = []
        for i in range(20001):
            ss = s0 + (1 - s0)*i/20000
            tt = ss / (K*ss - 1)
            assert 0 < tt <= 1 + 1e-12 and _close(1/ss + 1/tt, K)
            vals.append(ss*tt)
        assert _close(min(vals), lo, 1e-8) and _close(max(vals), hi, 1e-12)
    O, A, B = (0, 0), (3, 0.5), (1, 2)
    G = ((A[0] + B[0])/3, (A[1] + B[1])/3)
    ss = 0.8; tt = ss/(3*ss - 1)
    P, Q = (ss*A[0], ss*A[1]), (tt*B[0], tt*B[1])
    assert abs((Q[0] - P[0])*(G[1] - P[1]) - (Q[1] - P[1])*(G[0] - P[0])) < 1e-12
    # ラウス型
    tt = symbols("tt")
    assert sorted(solve(4*(2*tt - 1)**2 - (tt**2 - tt + 1), tt), key=lambda z: float(z)) == [(5 - sqrt(5))/10, (5 + sqrt(5))/10]
    def inner(tv, A, B, C):
        D = _mix(B, C, tv); E = _mix(C, A, tv); F = _mix(A, B, tv)
        R = _meet(A, D, B, E); P = _meet(B, E, C, F); Q = _meet(C, F, A, D)
        return _area([P, Q, R]) / _area([A, B, C]), R, A, D
    for tv in (0.1, 0.25, 1/3, 0.6, 0.9, (5 - math.sqrt(5))/10, (5 + math.sqrt(5))/10):
        A, B, C = (0.3, 2.2), (-1, 0.1), (2.7, -0.4)
        ratio, R, A_, D = inner(tv, A, B, C)
        assert _close(ratio, (2*tv - 1)**2/(tv*tv - tv + 1), 1e-9)
        assert _close(math.dist(A_, R)/math.dist(A_, D), (1 - tv)/(tv*tv - tv + 1), 1e-9)
    assert _close(inner((5 - math.sqrt(5))/10, (0, 0), (1, 0), (0, 1))[0], 0.25) and _close(inner(0.25, (0, 0), (1, 0), (0, 1))[0], 4/13)
    assert _close(inner(1/3, (0, 0), (1, 0), (0, 1))[0], 1/7)


def _circum(A, B, C):
    ax, ay = A; bx, by = B; cx, cy = C
    d = 2*(ax*(by - cy) + bx*(cy - ay) + cx*(ay - by))
    ux = ((ax*ax + ay*ay)*(by - cy) + (bx*bx + by*by)*(cy - ay) + (cx*cx + cy*cy)*(ay - by)) / d
    uy = ((ax*ax + ay*ay)*(cx - bx) + (bx*bx + by*by)*(ax - cx) + (cx*cx + cy*cy)*(bx - ax)) / d
    return (ux, uy)

def _coef(v, b, c):
    """v = s b + t c となる (s, t)"""
    det = b[0]*c[1] - b[1]*c[0]
    return ((v[0]*c[1] - v[1]*c[0]) / det, (b[0]*v[1] - b[1]*v[0]) / det)

def _tri(AB, AC, deg):
    """A=(0,0), AB 上に B，∠A=deg の三角形"""
    g = math.radians(deg)
    return (0.0, 0.0), (AB, 0.0), (AC*math.cos(g), AC*math.sin(g))

def _v6():
    # 垂線の足
    a = Matrix([2, 0]); b = Matrix([1, 2*sqrt(2)])
    assert a.dot(a) == 4 and b.dot(b) == 9 and a.dot(b) == 2
    H = (a.dot(b)/a.dot(a))*a
    assert H == a/2 and (H - b).dot(a) == 0
    B2 = 2*H - b
    assert B2 == a - b and (B2 - H).dot(B2 - H) == (b - H).dot(b - H)
    assert simplify(sqrt((b - H).dot(b - H)) - 2*sqrt(2)) == 0
    a = Matrix([-Rational(3, 2), 3*sqrt(3)/2]); b = Matrix([2, 0])
    assert simplify(a.dot(a) - 9) == 0 and a.dot(b) == -3
    H = (a.dot(b)/b.dot(b))*b
    assert H == -Rational(3, 4)*b
    assert _z(2*H - a - (-a - Rational(3, 2)*b)) and simplify(sqrt((a - H).dot(a - H)) - 3*sqrt(3)/2) == 0
    # 外心
    for (p, q, g), (s0, t0) in (((2, 3, 60), (1/6, 4/9)), ((3, 4, 120), (10/9, 11/12)), ((4, 3, 60), (5/12, 2/9))):
        A, B, C = _tri(p, q, g)
        O = _circum(A, B, C)
        s_, t_ = _coef(O, B, C)
        assert _close(s_, s0) and _close(t_, t0)
    # 内心：3辺から座標をつくり，3辺への距離が等しい点として確認
    for (c_, a_, b_), (s0, t0) in (((4, 6, 5), (1/3, 4/15)), ((5, 7, 3), (1/5, 1/3))):
        A, B = (0.0, 0.0), (float(c_), 0.0)
        cx = (c_**2 + b_**2 - a_**2) / (2*c_)
        C = (cx, math.sqrt(b_**2 - cx**2))
        assert _close(math.dist(B, C), a_)
        s_, t_ = s0, t0
        I = (s_*B[0] + t_*C[0], s_*B[1] + t_*C[1])
        def dl(P, Q, X):
            return abs((Q[0] - P[0])*(X[1] - P[1]) - (Q[1] - P[1])*(X[0] - P[0])) / math.dist(P, Q)
        r1, r2, r3_ = dl(A, B, I), dl(B, C, I), dl(C, A, I)
        assert _close(r1, r2) and _close(r2, r3_) and s_ > 0 and t_ > 0 and s_ + t_ < 1
    # 垂心：OH = OA+OB+OC（ランダム）
    for _ in range(200):
        A, B, C = [(random.uniform(-4, 4), random.uniform(-4, 4)) for _ in range(3)]
        if _area([A, B, C]) < 0.3:
            continue
        O = _circum(A, B, C)
        H = (A[0] + B[0] + C[0] - 2*O[0], A[1] + B[1] + C[1] - 2*O[1])
        assert abs((H[0] - A[0])*(C[0] - B[0]) + (H[1] - A[1])*(C[1] - B[1])) < 1e-7
        assert abs((H[0] - B[0])*(A[0] - C[0]) + (H[1] - B[1])*(A[1] - C[1])) < 1e-7
    for (p, q, g), (s0, t0) in (((2, 3, 60), (2/3, 1/9)), ((4, 3, 60), (1/6, 5/9))):
        A, B, C = _tri(p, q, g)
        O = _circum(A, B, C)
        H = (A[0] + B[0] + C[0] - 2*O[0], A[1] + B[1] + C[1] - 2*O[1])
        s_, t_ = _coef(H, B, C)
        assert _close(s_, s0) and _close(t_, t0)
    # 3OA+4OB+5OC = 0
    for (l, m, n), area in (((3, 4, 5), 6/5), ((5, 12, 13), 15/13)):
        a, b = (1.0, 0.0), (0.0, 1.0)
        c = (-(l*a[0] + m*b[0])/n, -(l*a[1] + m*b[1])/n)
        assert _close(math.hypot(*c), 1)
        assert _close(l*a[0] + m*b[0] + n*c[0], 0) and _close(l*a[1] + m*b[1] + n*c[1], 0)
        assert _close(_ang((a[0] - c[0], a[1] - c[1]), (b[0] - c[0], b[1] - c[1])), 45)
        assert _close(_area([a, b, c]), area)
        if l == 3:
            assert _close(b[0]*c[0] + b[1]*c[1], -0.8) and _close(c[0]*a[0] + c[1]*a[1], -0.6)
    # オイラーの定理 OI^2 = R^2 - 2Rr，OH^2 = 9R^2 - (a^2+b^2+c^2)
    R_, aa, bb, cc = symbols("R aa bb cc", positive=True)
    xy, yz, zx = R_**2 - cc**2/2, R_**2 - aa**2/2, R_**2 - bb**2/2
    lhs = (aa**2 + bb**2 + cc**2)*R_**2 + 2*aa*bb*xy + 2*bb*cc*yz + 2*cc*aa*zx
    assert expand(lhs - ((aa + bb + cc)**2*R_**2 - aa*bb*cc*(aa + bb + cc))) == 0
    assert expand(3*R_**2 + 2*(xy + yz + zx) - (9*R_**2 - (aa**2 + bb**2 + cc**2))) == 0
    for _ in range(300):
        A, B, C = [(random.uniform(-4, 4), random.uniform(-4, 4)) for _ in range(3)]
        S = _area([A, B, C])
        if S < 0.3:
            continue
        a_, b_, c_ = math.dist(B, C), math.dist(C, A), math.dist(A, B)
        O = _circum(A, B, C); R = math.dist(O, A)
        I = ((a_*A[0] + b_*B[0] + c_*C[0])/(a_ + b_ + c_), (a_*A[1] + b_*B[1] + c_*C[1])/(a_ + b_ + c_))
        r = 2*S/(a_ + b_ + c_)
        assert _close(math.dist(O, I)**2, R*R - 2*R*r, 1e-7) and R >= 2*r - 1e-12
        H = (A[0] + B[0] + C[0] - 2*O[0], A[1] + B[1] + C[1] - 2*O[1])
        assert _close(math.dist(O, H)**2, 9*R*R - (a_*a_ + b_*b_ + c_*c_), 1e-6)
    A, B, C = (4.0, 0.0), (0.0, 3.0), (0.0, 0.0)
    O = _circum(A, B, C)
    assert _close(math.dist(O, (1, 1))**2, 1.25)
    # OH ∥ BC ⇔ tanB tanC = 3（鋭角三角形）
    cnt = 0
    while cnt < 300:
        Ad, Bd = random.uniform(1, 89), random.uniform(1, 89)
        Cd = 180 - Ad - Bd
        if not (1 < Cd < 89):
            continue
        cnt += 1
        A_, B_, C_ = (math.radians(z) for z in (Ad, Bd, Cd))
        # 外接円半径1：A を偏角 0，B を 2C，C を 2C+2A に置く（∠AOB=2C，∠BOC=2A，∠COA=2B）
        A = (1.0, 0.0); B = (math.cos(2*C_), math.sin(2*C_)); C = (math.cos(2*C_ + 2*A_), math.sin(2*C_ + 2*A_))
        assert _close(_ang((B[0] - A[0], B[1] - A[1]), (C[0] - A[0], C[1] - A[1])), Ad, 1e-7)
        assert _close(_ang((A[0] - B[0], A[1] - B[1]), (C[0] - B[0], C[1] - B[1])), Bd, 1e-7)
        h = (A[0] + B[0] + C[0], A[1] + B[1] + C[1]); m = ((B[0] + C[0])/2, (B[1] + C[1])/2)
        lhs = (h[0]*m[0] + h[1]*m[1]) * 2
        assert _close(lhs, 2*math.cos(A_)*(2*math.cos(A_) - math.cos(B_ - C_)), 1e-9)
        # AH = 2R cos A
        assert _close(math.hypot(h[0] - A[0], h[1] - A[1]), 2*math.cos(A_), 1e-9)
    Bd = 45; Cd = math.degrees(math.atan(3)); Ad = 180 - Bd - Cd
    assert Ad < 90 and _close(math.tan(math.radians(Ad)), 2, 1e-9)
    A_, B_, C_ = (math.radians(z) for z in (Ad, Bd, Cd))
    A = (1.0, 0.0); B = (math.cos(2*C_), math.sin(2*C_)); C = (math.cos(2*C_ + 2*A_), math.sin(2*C_ + 2*A_))
    h = (A[0] + B[0] + C[0], A[1] + B[1] + C[1])
    assert abs(h[0]*(C[1] - B[1]) - h[1]*(C[0] - B[0])) < 1e-9 and math.hypot(*h) > 0.1


def _v7():
    x, y, t = symbols("x y t")
    # (1) 媒介変数表示と消去
    for A, d, eq in (((1, 2), (3, -1), x + 3*y - 7), ((-2, 1), (2, 5), 5*x - 2*y + 12)):
        assert expand(eq.subs({x: A[0] + d[0]*t, y: A[1] + d[1]*t})) == 0
    for A, n, eq in (((1, 2), (2, 3), 2*x + 3*y - 8), ((-2, 1), (4, -1), 4*x - y + 9)):
        assert eq.subs({x: A[0], y: A[1]}) == 0 and eq.coeff(x) == n[0] and eq.coeff(y) == n[1]
    def la(n1, n2):
        c = abs(n1[0]*n2[0] + n1[1]*n2[1]) / (math.hypot(*n1)*math.hypot(*n2))
        return math.degrees(math.acos(c))
    assert _close(la((1, -3), (2, -1)), 45) and _close(la((1, math.sqrt(3)), (1, -math.sqrt(3))), 60)
    # 円のベクトル方程式（ランダムな a, b と円上の点で確認）
    for _ in range(50):
        a = (random.uniform(-3, 3), random.uniform(-3, 3)); b = (random.uniform(-3, 3), random.uniform(-3, 3))
        th = random.uniform(0, 2*math.pi)
        c = ((a[0] + 2*b[0])/3, (a[1] + 2*b[1])/3)
        p = (c[0] + 2*math.cos(th), c[1] + 2*math.sin(th))
        assert _close(math.hypot(3*p[0] - a[0] - 2*b[0], 3*p[1] - a[1] - 2*b[1]), 6)
        m = (b[0]/2, b[1]/2); cc = ((a[0] + m[0])/2, (a[1] + m[1])/2); r = math.dist(a, m)/2
        p = (cc[0] + r*math.cos(th), cc[1] + r*math.sin(th))
        assert abs((p[0] - a[0])*(2*p[0] - b[0]) + (p[1] - a[1])*(2*p[1] - b[1])) < 1e-9
        c = ((-a[0] + 3*b[0])/2, (-a[1] + 3*b[1])/2)          # 3:1 外分
        p = (c[0] + 2*math.cos(th), c[1] + 2*math.sin(th))
        assert _close(math.hypot(2*p[0] + a[0] - 3*b[0], 2*p[1] + a[1] - 3*b[1]), 4)
    # 接線
    for C, r2, P0, eq in (((1, 2), 10, (2, 5), x + 3*y - 17), ((2, -1), 5, (3, 1), x + 2*y - 5)):
        assert (P0[0] - C[0])**2 + (P0[1] - C[1])**2 == r2 and eq.subs({x: P0[0], y: P0[1]}) == 0
        a_, b_ = eq.coeff(x), eq.coeff(y)
        assert a_*(P0[1] - C[1]) - b_*(P0[0] - C[0]) == 0           # 法線が半径方向
    assert expand(x**2 + y**2 - 4*x + 2*y - ((x - 2)**2 + (y + 1)**2 - 5)) == 0
    # 点と直線の距離
    for P, (a_, b_, c_), H, dist in (((3, 1), (3, 4, -3), (Fr(9, 5), Fr(-3, 5)), 2), ((-1, 4), (1, -2, 4), (0, 2), math.sqrt(5))):
        k = Fr(-(a_*P[0] + b_*P[1] + c_), a_*a_ + b_*b_)
        Hc = (P[0] + k*a_, P[1] + k*b_)
        assert Hc == tuple(Fr(z) for z in H) and a_*Hc[0] + b_*Hc[1] + c_ == 0
        assert _close(abs(a_*P[0] + b_*P[1] + c_)/math.hypot(a_, b_), dist)
    # 軌跡（重心中心の円）
    a = (3.0, 0.0); b = (1.0, math.sqrt(3))
    G = ((a[0] + b[0])/3, (a[1] + b[1])/3); r = math.sqrt(10)/3
    dd = lambda P, Q, R: (Q[0] - P[0])*(R[0] - P[0]) + (Q[1] - P[1])*(R[1] - P[1])
    for i in range(100):
        th = 2*math.pi*i/100
        P = (G[0] + r*math.cos(th), G[1] + r*math.sin(th))
        assert abs(dd(P, (0, 0), a) + dd(P, a, b) + dd(P, b, (0, 0))) < 1e-9
    assert _close(math.dist(a, b)**2, 7)
    A, B, C = (0.0, 0.0), (3.0, 0.0), (1.5, 1.5*math.sqrt(3))
    G = (1.5, 0.5*math.sqrt(3)); r = math.sqrt(10)/2
    for i in range(100):
        th = 2*math.pi*i/100
        P = (G[0] + r*math.cos(th), G[1] + r*math.sin(th))
        assert _close(dd(P, A, B) + dd(P, B, C) + dd(P, C, A), 3)


def _inside(P, poly):
    """凸多角形（反時計回りでも時計回りでも）の周および内部にあるか"""
    sg = []
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        sg.append((b[0] - a[0])*(P[1] - a[1]) - (b[1] - a[1])*(P[0] - a[0]))
    return all(z >= -1e-9 for z in sg) or all(z <= 1e-9 for z in sg)

def _v8():
    # (1) 基本：s+t=2 の点は直線 A'B' 上，(3) は線分 AM 上
    A, B = (1.6, 0.0), (0.5, 1.0)
    for _ in range(100):
        s = random.uniform(-3, 3); t = 2 - s
        P = (s*A[0] + t*B[0], s*A[1] + t*B[1])
        A2, B2 = (2*A[0], 2*A[1]), (2*B[0], 2*B[1])
        assert abs((B2[0] - A2[0])*(P[1] - A2[1]) - (B2[1] - A2[1])*(P[0] - A2[0])) < 1e-9
        s = random.uniform(0, 1); t = (1 - s)/2
        P = (s*A[0] + t*B[0], s*A[1] + t*B[1]); M = (B[0]/2, B[1]/2)
        assert _close(math.dist(A, P) + math.dist(P, M), math.dist(A, M))
        s, t = random.uniform(0, 3), random.uniform(0, 2)
        P = (s*A[0] + t*B[0], s*A[1] + t*B[1])
        assert _inside(P, [(0, 0), (3*A[0], 3*A[1]), (2*B[0], 2*B[1])]) == (2*s + 3*t <= 6)
    # (2) 台形の面積
    O, A, B = (0.0, 0.0), (2.0, 0.0), (1.5, 1.5*math.sqrt(3))
    quad = [(1.0, 0.0), (3.0, 0.0), B, (B[0]/3, B[1]/3)]
    assert _close(_area(quad), 2*math.sqrt(3))
    assert _close(Fr(1, 2)*Fr(3, 2) - Fr(1, 2)*Fr(1, 2)*Fr(1, 3), Fr(2, 3)) and _close(2/3*2*_area([O, A, B]), 2*math.sqrt(3))
    A, B = (4.0, 0.0), (0.0, 3.0)
    assert _close(_area([(8.0, 0.0), (16.0, 0.0), (0.0, 6.0), (0.0, 3.0)]), 36)
    assert (Fr(1, 2)*4*2 - Fr(1, 2)*2*1) * 12 == 36
    # (3) 置きかえ：△OCD，面積 2S
    A, B = (2.0, 0.4), (0.6, 1.2)
    S = _area([(0, 0), A, B])
    C, D = (A[0] + B[0], A[1] + B[1]), (A[0] - B[0], A[1] - B[1])
    E = (2*A[0] + B[0], 2*A[1] + B[1])
    assert _close(_area([(0, 0), C, D]), 2*S) and _close(_area([(0, 0), C, E]), S)
    for _ in range(3000):
        s, t = random.random(), random.random()
        if s + t > 1:
            continue
        P = ((s + t)*A[0] + (s - t)*B[0], (s + t)*A[1] + (s - t)*B[1])
        assert _inside(P, [(0, 0), C, D])
        P = ((2*s + t)*A[0] + (s + t)*B[0], (2*s + t)*A[1] + (s + t)*B[1])
        assert _inside(P, [(0, 0), C, E])
    for _ in range(3000):    # 逆：三角形内の点はもとの (s,t) をもつ
        x, y = random.uniform(-1, 3), random.uniform(-1, 2)
        if _inside((x, y), [(0, 0), C, D]):
            u, v = _coef((x, y), A, B); s, t = (u + v)/2, (u - v)/2
            assert s >= -1e-9 and t >= -1e-9 and s + t <= 1 + 1e-9
        if _inside((x, y), [(0, 0), C, E]):
            u, v = _coef((x, y), A, B); s, t = u - v, 2*v - u
            assert s >= -1e-9 and t >= -1e-9 and s + t <= 1 + 1e-9
    # (4) 3点の重心：六角形，面積 2/3
    hexa = [(Fr(1, 3), 0), (Fr(2, 3), 0), (Fr(2, 3), Fr(1, 3)), (Fr(1, 3), Fr(2, 3)), (0, Fr(2, 3)), (0, Fr(1, 3))]
    assert _area(hexa) * 2 == Fr(2, 3)
    def inH(X, Y):
        return -1e-12 <= X <= 2/3 + 1e-12 and -1e-12 <= Y <= 2/3 + 1e-12 and 1/3 - 1e-12 <= X + Y <= 1 + 1e-12
    for _ in range(20000):
        u, v, w = random.random(), random.random(), random.random()
        X, Y = (1 - u + w)/3, (1 + u - v)/3
        assert inH(X, Y)
    for _ in range(20000):
        X, Y = random.uniform(-0.1, 0.8), random.uniform(-0.1, 0.8)
        lo = max(1 - 3*X, 3*Y - 1, 0); hi = min(2 - 3*X, 3*Y, 1)
        if inH(X, Y):
            assert lo <= hi + 1e-12
            u = min(max(lo, 0), 1); w = 3*X - 1 + u; v = 1 + u - 3*Y
            assert -1e-9 <= w <= 1 + 1e-9 and -1e-9 <= v <= 1 + 1e-9
        elif min(abs(X), abs(Y), abs(X - 2/3), abs(Y - 2/3), abs(X + Y - 1/3), abs(X + Y - 1)) > 1e-6:
            assert lo > hi
    A, B, C = (0.9, 2.4), (0.0, 0.0), (3.0, 0.0)
    pts = [_mix(A, B, 1/3), _mix(A, B, 2/3), _mix(B, C, 1/3), _mix(B, C, 2/3), _mix(C, A, 1/3), _mix(C, A, 2/3)]
    assert _close(_area(pts), 2/3*_area([A, B, C]))
    # 練習：PQ を 1:2 に内分する点 → 平行四辺形 4/9
    par = [(Fr(2, 3), 0), (Fr(2, 3), Fr(1, 3)), (0, 1), (0, Fr(2, 3))]
    assert _area(par) * 2 == Fr(4, 9)
    for _ in range(5000):
        u, v = random.random(), random.random()
        X, Y = 2*(1 - u)/3, (2*u + 1 - v)/3
        assert _inside((X, Y), [(2/3, 0), (2/3, 1/3), (0, 1), (0, 2/3)])
    # (5) 円が掃く範囲：格子で面積を数える
    def region(x, y, r):
        d1 = abs(y) if abs(x) <= 1 else math.hypot(abs(x) - 1, y)
        d2 = math.hypot(abs(x) + 1, y)
        return d1 <= r <= d2
    for r, ans in ((2.0, 8 + 4*math.pi/3 + 2*math.sqrt(3)), (math.sqrt(2), 4*math.sqrt(2) + math.pi + 2)):
        h = 0.005
        nx, ny = int(2*(1 + r)/h) + 2, int(2*r/h) + 2
        cnt = 0
        for i in range(nx):
            x = -(1 + r) - h + (i + 0.5)*h
            for j in range(ny):
                y = -r - h + (j + 0.5)*h
                if region(x, y, r):
                    cnt += 1
        assert abs(cnt*h*h - ans) < 0.01, (cnt*h*h, ans)
    # 存在範囲の特徴づけ（P を細かく動かして直接確かめる）
    for _ in range(400):
        x, y = random.uniform(-3.2, 3.2), random.uniform(-2.2, 2.2)
        ds = [math.hypot(x - (-1 + 2*k/400), y) for k in range(401)]
        exist = min(ds) <= 2 <= max(ds)
        if abs(min(ds) - 2) > 0.02 and abs(max(ds) - 2) > 0.02:
            assert exist == region(x, y, 2.0)


def verify():
    _v1()
    _v2()
    _v3()
    _v4()
    _v5()
    _v6()
    _v7()
    _v8()
    # 例題数と難易度の配分
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert 37 <= len(items) <= 43, len(items)
    assert cnt[5] >= 5 and 4 <= len(SEC) <= 9, cnt
    # 文字列に制御文字（"\v" などの書き損じ）がないこと，$ の対応
    for s in SEC:
        for it in s["items"] + [{"base": s["base"]}]:
            for k, v in it.items():
                if isinstance(v, str):
                    assert not re.search(r"[\x00-\x08\x0b-\x1f]", v), (k, v[:40])
                    assert v.count("$") % 2 == 0, (k, v[:60])
                    assert "\\VV" not in v
