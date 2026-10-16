"""問題集 第19章 空間ベクトル。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {19: {
"goal": r"空間でも平面と同じ道具（成分・内積・1次独立）が使える。同一平面上の条件「係数の和が1」と、垂線の足は「2方向との内積 $=0$」を自在に使う。",
"items": [
 {"lv": "A", "q": r"$\vec a=(1,\ -1,\ 2),\ \vec b=(2,\ 1,\ 1)$ について、(1) $\vec a$ と $\vec b$ のなす角を求めよ。(2) $\vec a,\ \vec b$ のどちらにも垂直な単位ベクトルを求めよ。",
  "a": r"(1) $60^\circ$　(2) $\pm\frac{1}{\sqrt3}(-1,\ 1,\ 1)$",
  "s": r"(1) $\vec a\cdot\vec b=2-1+2=3$、$|\vec a|=|\vec b|=\sqrt6$。$\cos\theta=\frac36=\frac12$ より $60^\circ$。<br>(2) 求めるベクトルを $(x,y,z)$ とすると $x-y+2z=0,\ 2x+y+z=0,\ x^2+y^2+z^2=1$。初めの2式を足して $3x+3z=0$ より $z=-x$、さらに $y=x+2z=-x$。$3x^2=1$ より $x=\pm\frac{1}{\sqrt3}$。よって $\pm\frac{1}{\sqrt3}(1,\ -1,\ -1)$、すなわち $\pm\frac{1}{\sqrt3}(-1,\ 1,\ 1)$。<br><b>ポイント</b>：2つのベクトルに垂直なベクトルは、内積 $=0$ を2本立てて1文字で表す。符号 $\pm$ を忘れない。"},
 {"lv": "A", "q": r"2点 $\mathrm{A}(1,\ 2,\ 3),\ \mathrm{B}(4,\ -1,\ 0)$ について、線分 AB を $2:1$ に内分する点、外分する点の座標と、線分 AB の長さを求めよ。",
  "a": r"内分点 $(3,\ 0,\ 1)$、外分点 $(7,\ -4,\ -3)$、$\mathrm{AB}=3\sqrt3$",
  "s": r"内分点 $\frac{1\cdot\mathrm{A}+2\cdot\mathrm{B}}{3}=\left(\frac{1+8}{3},\ \frac{2-2}{3},\ \frac{3+0}{3}\right)=(3,\ 0,\ 1)$。外分点 $\frac{-1\cdot\mathrm{A}+2\cdot\mathrm{B}}{2-1}=(7,\ -4,\ -3)$。$\mathrm{AB}=\sqrt{3^2+3^2+3^2}=3\sqrt3$。<br><b>ポイント</b>：$m:n$ の外分は内分の公式で $n$ を $-n$ に置きかえる。"},
 {"lv": "A", "q": r"4点 $\mathrm{A}(1,\ 0,\ 0),\ \mathrm{B}(0,\ 2,\ 0),\ \mathrm{C}(0,\ 0,\ 3),\ \mathrm{D}(x,\ 1,\ 1)$ が同一平面上にあるように $x$ の値を定めよ。",
  "a": r"$x=\frac16$",
  "s": r"$\overrightarrow{\mathrm{AD}}=s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$ となる実数 $s,t$ がある。$(x-1,\ 1,\ 1)=s(-1,\ 2,\ 0)+t(-1,\ 0,\ 3)$ より $y$ 成分 $2s=1$、$z$ 成分 $3t=1$。$s=\frac12,\ t=\frac13$、$x-1=-\frac12-\frac13=-\frac56$、$x=\frac16$。<br><b>ポイント</b>：D が平面 ABC 上 ⇔ $\overrightarrow{\mathrm{AD}}=s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}$ ⇔ $\overrightarrow{\mathrm{OD}}=(1-s-t)\overrightarrow{\mathrm{OA}}+s\overrightarrow{\mathrm{OB}}+t\overrightarrow{\mathrm{OC}}$（係数の和が1）。"},
 {"lv": "A", "q": r"中心が $(1,\ -2,\ 3)$ で点 $(3,\ 0,\ 2)$ を通る球面の方程式を求めよ。また、この球面と $yz$ 平面が交わってできる円の中心と半径を求めよ。",
  "a": r"$(x-1)^2+(y+2)^2+(z-3)^2=9$；円の中心 $(0,\ -2,\ 3)$、半径 $2\sqrt2$",
  "s": r"半径の2乗は $2^2+2^2+(-1)^2=9$。$yz$ 平面は $x=0$ なので代入して $(y+2)^2+(z-3)^2=8$。$yz$ 平面上の中心 $(0,\ -2,\ 3)$、半径 $2\sqrt2$ の円。<br><b>ポイント</b>：球の中心から平面までの距離 $d$（ここでは $1$）と半径 $r$ で、切り口の円の半径は $\sqrt{r^2-d^2}=\sqrt{9-1}$ とも求められる。"},
 {"lv": "B", "tag": "典型", "q": r"四面体 OABC において $\overrightarrow{\mathrm{OA}}=\vec a,\ \overrightarrow{\mathrm{OB}}=\vec b,\ \overrightarrow{\mathrm{OC}}=\vec c$ とする。辺 OA の中点を P、辺 OB を $2:1$ に内分する点を Q、辺 OC を $1:3$ に内分する点を R とし、$\triangle\mathrm{ABC}$ の重心を G とする。直線 OG と平面 PQR の交点を X とするとき、$\overrightarrow{\mathrm{OX}}$ を $\vec a,\ \vec b,\ \vec c$ で表し、$\mathrm{OX}:\mathrm{XG}$ を求めよ。",
  "a": r"$\overrightarrow{\mathrm{OX}}=\frac{2}{15}(\vec a+\vec b+\vec c)$、$\mathrm{OX}:\mathrm{XG}=2:3$",
  "s": r"$\overrightarrow{\mathrm{OG}}=\frac{\vec a+\vec b+\vec c}{3}$。X は直線 OG 上にあるので $\overrightarrow{\mathrm{OX}}=k\overrightarrow{\mathrm{OG}}=\frac k3(\vec a+\vec b+\vec c)$。<br>$\vec a=2\overrightarrow{\mathrm{OP}},\ \vec b=\frac32\overrightarrow{\mathrm{OQ}},\ \vec c=4\overrightarrow{\mathrm{OR}}$ を代入すると $\overrightarrow{\mathrm{OX}}=\frac k3\left(2\overrightarrow{\mathrm{OP}}+\frac32\overrightarrow{\mathrm{OQ}}+4\overrightarrow{\mathrm{OR}}\right)$。<br>X が平面 PQR 上にある条件は係数の和が1（$\overrightarrow{\mathrm{OP}},\overrightarrow{\mathrm{OQ}},\overrightarrow{\mathrm{OR}}$ は1次独立）：$\frac k3\cdot\frac{15}{2}=1$、$k=\frac25$。<br>よって $\overrightarrow{\mathrm{OX}}=\frac{2}{15}(\vec a+\vec b+\vec c)$、$\mathrm{OX}:\mathrm{OG}=2:5$ より $\mathrm{OX}:\mathrm{XG}=2:3$。<br><b>ポイント</b>：平面 PQR との交点は「$\overrightarrow{\mathrm{OP}},\overrightarrow{\mathrm{OQ}},\overrightarrow{\mathrm{OR}}$ で表して係数の和 $=1$」。"},
 {"lv": "B", "tag": "垂線の足", "q": r"$\mathrm{A}(2,\ 0,\ 0),\ \mathrm{B}(0,\ 4,\ 0),\ \mathrm{C}(0,\ 0,\ 4)$ とし、原点 O から平面 ABC に下ろした垂線の足を H とする。(1) H の座標と線分 OH の長さを求めよ。(2) $\triangle\mathrm{ABC}$ の面積を求めよ。",
  "a": r"(1) $\mathrm{H}\left(\frac43,\ \frac23,\ \frac23\right)$、$\mathrm{OH}=\frac{2\sqrt6}{3}$　(2) $4\sqrt6$",
  "s": r"(1) H は平面 ABC 上にあるので $\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OA}}+s\overrightarrow{\mathrm{AB}}+t\overrightarrow{\mathrm{AC}}=(2-2s-2t,\ 4s,\ 4t)$。<br>$\overrightarrow{\mathrm{OH}}\perp\overrightarrow{\mathrm{AB}}$：$(2-2s-2t)(-2)+16s=0$ より $20s+4t=4$。$\overrightarrow{\mathrm{OH}}\perp\overrightarrow{\mathrm{AC}}$：同様に $4s+20t=4$。解いて $s=t=\frac16$。$\mathrm{H}\left(\frac43,\ \frac23,\ \frac23\right)$、$\mathrm{OH}=\sqrt{\frac{16+4+4}{9}}=\frac{2\sqrt6}{3}$。<br>(2) 四面体 OABC の体積は $\frac13\cdot\frac12\cdot2\cdot4\cdot4=\frac{16}{3}$。これは $\frac13\triangle\mathrm{ABC}\cdot\mathrm{OH}$ に等しいので $\triangle\mathrm{ABC}=\frac{16}{\mathrm{OH}}=\frac{16\cdot3}{2\sqrt6}=4\sqrt6$。<br>（別解）$|\overrightarrow{\mathrm{AB}}|^2=20,\ |\overrightarrow{\mathrm{AC}}|^2=20,\ \overrightarrow{\mathrm{AB}}\cdot\overrightarrow{\mathrm{AC}}=4$ より $\frac12\sqrt{400-16}=\frac12\sqrt{384}=4\sqrt6$。<br><b>ポイント</b>：垂線の足は「平面上にある」（2文字で表す）＋「平面内の2方向と垂直」で決まる。体積を2通りに表すと面積や距離が出る。"},
 {"lv": "B", "tag": "2直線の距離", "q": r"直線 $\ell$：点 $(1,\ 0,\ 0)$ を通り方向ベクトル $\vec u=(1,\ 1,\ 0)$、直線 $m$：点 $(0,\ 0,\ 2)$ を通り方向ベクトル $\vec v=(0,\ 1,\ 1)$ とする。$\ell$ 上の点 P と $m$ 上の点 Q の距離 PQ の最小値と、そのときの P、Q の座標を求めよ。",
  "a": r"最小値 $\frac{\sqrt3}{3}$、$\mathrm{P}\left(-\frac13,\ -\frac43,\ 0\right),\ \mathrm{Q}\left(0,\ -\frac53,\ \frac13\right)$",
  "s": r"$\mathrm{P}(1+s,\ s,\ 0),\ \mathrm{Q}(0,\ t,\ 2+t)$ とおくと $\overrightarrow{\mathrm{PQ}}=(-1-s,\ t-s,\ 2+t)$。<br>PQ が最小になるのは $\overrightarrow{\mathrm{PQ}}\perp\vec u$ かつ $\overrightarrow{\mathrm{PQ}}\perp\vec v$ のとき（共通垂線）。<br>$\overrightarrow{\mathrm{PQ}}\cdot\vec u=-1-2s+t=0$、$\overrightarrow{\mathrm{PQ}}\cdot\vec v=-s+2t+2=0$。解いて $s=-\frac43,\ t=-\frac53$。<br>$\overrightarrow{\mathrm{PQ}}=\left(\frac13,\ -\frac13,\ \frac13\right)$、$\mathrm{PQ}=\frac{1}{\sqrt3}=\frac{\sqrt3}{3}$。<br>（別解）$\mathrm{PQ}^2=(1+s)^2+(t-s)^2+(2+t)^2=2s^2-2st+2t^2+2s+4t+5$ を平方完成すると $2\left(s-\frac{t-1}{2}\right)^2+\frac32\left(t+\frac53\right)^2+\frac13$。$t=-\frac53,\ s=\frac{t-1}{2}=-\frac43$ で最小値 $\frac13$ をとり、同じ結果になる。<br><b>ポイント</b>：ねじれの位置にある2直線の距離は、両方に垂直な線分（共通垂線）の長さ。"},
 {"lv": "B", "tag": "頻出", "q": r"1辺の長さが1の正四面体 OABC において、辺 OA の中点を M、辺 BC の中点を N とする。(1) $|\overrightarrow{\mathrm{MN}}|$ を求めよ。(2) $\overrightarrow{\mathrm{MN}}$ と $\overrightarrow{\mathrm{OA}}$、$\overrightarrow{\mathrm{MN}}$ と $\overrightarrow{\mathrm{BC}}$ がそれぞれ垂直であることを示せ。",
  "a": r"(1) $\frac{\sqrt2}{2}$",
  "s": r"$\vec a=\overrightarrow{\mathrm{OA}}$ などとおくと、$|\vec a|=|\vec b|=|\vec c|=1$、$\vec a\cdot\vec b=\vec b\cdot\vec c=\vec c\cdot\vec a=1\cdot1\cdot\cos60^\circ=\frac12$。<br>(1) $\overrightarrow{\mathrm{MN}}=\frac{\vec b+\vec c}{2}-\frac{\vec a}{2}=\frac12(-\vec a+\vec b+\vec c)$。<br>$|-\vec a+\vec b+\vec c|^2=3+2\vec b\cdot\vec c-2\vec a\cdot\vec b-2\vec a\cdot\vec c=3+1-1-1=2$ より $|\overrightarrow{\mathrm{MN}}|=\frac{\sqrt2}{2}$。<br>(2) $\overrightarrow{\mathrm{MN}}\cdot\vec a=\frac12\left(-1+\frac12+\frac12\right)=0$。$\overrightarrow{\mathrm{MN}}\cdot(\vec c-\vec b)=\frac12\left(-\vec a\cdot\vec c+\vec a\cdot\vec b+|\vec c|^2-|\vec b|^2\right)=0$。■<br><b>ポイント</b>：MN は OA と BC の共通垂線で、その長さ $\frac{\sqrt2}{2}$ が2辺 OA、BC の距離。正四面体は「長さ1・内積 $\frac12$」で計算できる。"},
 {"lv": "B", "tag": "球と直線", "q": r"球面 $S:\ (x-1)^2+(y-2)^2+(z+1)^2=9$ と、原点を通り方向ベクトル $(1,\ 1,\ 1)$ の直線 $\ell$ が交わる2点を P、Q とする。線分 PQ の長さを求めよ。",
  "a": r"$\frac{2\sqrt{39}}{3}$",
  "s": r"$\ell$ 上の点は $(t,\ t,\ t)$。$S$ に代入して $(t-1)^2+(t-2)^2+(t+1)^2=9$、$3t^2-4t-3=0$。2解を $t_1,t_2$ とすると $t_1+t_2=\frac43,\ t_1t_2=-1$、$(t_1-t_2)^2=\frac{16}{9}+4=\frac{52}{9}$。<br>$\mathrm{PQ}=|t_1-t_2|\cdot|(1,1,1)|=\frac{2\sqrt{13}}{3}\cdot\sqrt3=\frac{2\sqrt{39}}{3}$。<br>（別解）中心 $\mathrm{C}(1,2,-1)$ から $\ell$ までの距離 $d$ は、$\vec e=\frac{1}{\sqrt3}(1,1,1)$ として $d^2=|\overrightarrow{\mathrm{OC}}|^2-(\overrightarrow{\mathrm{OC}}\cdot\vec e)^2=6-\frac43=\frac{14}{3}$。$\mathrm{PQ}=2\sqrt{9-\frac{14}{3}}=2\sqrt{\frac{13}{3}}=\frac{2\sqrt{39}}{3}$。<br><b>ポイント</b>：弦の長さは「パラメータの差 × 方向ベクトルの大きさ」。解と係数の関係で差を出すと計算が軽い。"},
 {"lv": "C", "tag": "論証", "q": r"四面体 OABC において、$\mathrm{OA}\perp\mathrm{BC}$ かつ $\mathrm{OB}\perp\mathrm{CA}$ であるとする。<br>(1) $\mathrm{OC}\perp\mathrm{AB}$ であることを示せ。<br>(2) O から平面 ABC に下ろした垂線の足を H とする。H は $\triangle\mathrm{ABC}$ の垂心であることを示せ。",
  "a": r"証明（解説参照）",
  "s": r"$\vec a=\overrightarrow{\mathrm{OA}}$ などとおく。仮定は $\vec a\cdot(\vec c-\vec b)=0$ …①、$\vec b\cdot(\vec a-\vec c)=0$ …②。<br>(1) ①＋② より $\vec a\cdot\vec c-\vec a\cdot\vec b+\vec a\cdot\vec b-\vec b\cdot\vec c=0$、すなわち $\vec c\cdot(\vec a-\vec b)=0$。よって $\overrightarrow{\mathrm{OC}}\perp\overrightarrow{\mathrm{BA}}$。■<br>(2) $\overrightarrow{\mathrm{OH}}$ は平面 ABC に垂直なので、平面内のベクトル $\overrightarrow{\mathrm{BC}},\ \overrightarrow{\mathrm{CA}}$ と垂直。<br>$\overrightarrow{\mathrm{AH}}\cdot\overrightarrow{\mathrm{BC}}=(\overrightarrow{\mathrm{OH}}-\vec a)\cdot\overrightarrow{\mathrm{BC}}=0-\vec a\cdot(\vec c-\vec b)=0$（①）。<br>$\overrightarrow{\mathrm{BH}}\cdot\overrightarrow{\mathrm{CA}}=(\overrightarrow{\mathrm{OH}}-\vec b)\cdot\overrightarrow{\mathrm{CA}}=0-\vec b\cdot(\vec a-\vec c)=0$（②）。<br>よって H は A から BC への垂線上と、B から CA への垂線上にある（H が頂点 A や B と一致する場合も、その頂点で直角となり、直角三角形の垂心は直角の頂点なので結論は同じ）。2本の垂線の交点は垂心なので、H は $\triangle\mathrm{ABC}$ の垂心。■<br><b>ポイント</b>：空間の論証でも、「垂直」を内積 $=0$ の式に直して足し引きするだけで証明できることが多い。(1)は、(2)の垂心の3本目の垂線 $\mathrm{CH}\perp\mathrm{AB}$ にも対応している。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$\mathrm{A}(2,\ 0,\ 0),\ \mathrm{B}(0,\ 2,\ 0),\ \mathrm{C}(0,\ 0,\ 2)$ とし、点 P は原点 O を中心とする半径1の球面上を動く。<br>(1) O から平面 ABC に下ろした垂線の足 H と、$\triangle\mathrm{ABC}$ の面積を求めよ。<br>(2) 四面体 PABC の体積の最大値と、そのときの P の座標を求めよ。",
  "a": r"(1) $\mathrm{H}\left(\frac23,\ \frac23,\ \frac23\right)$、面積 $2\sqrt3$　(2) 最大値 $\frac{4+2\sqrt3}{3}$、$\mathrm{P}\left(-\frac{1}{\sqrt3},\ -\frac{1}{\sqrt3},\ -\frac{1}{\sqrt3}\right)$",
  "s": r"(1) 対称性から $\mathrm{H}(h,h,h)$ とおける（19-6 と同様に $\overrightarrow{\mathrm{OH}}\perp\overrightarrow{\mathrm{AB}},\ \overrightarrow{\mathrm{AC}}$ から導いても同じ）。H は平面 ABC 上：$\overrightarrow{\mathrm{AH}}=(h-2,\ h,\ h)=s(-2,2,0)+t(-2,0,2)$ より $s=t=\frac h2$、$h-2=-2h$、$h=\frac23$。$\mathrm{OH}=\frac{2}{\sqrt3}$。<br>$\triangle\mathrm{ABC}$ は1辺 $2\sqrt2$ の正三角形なので面積 $\frac{\sqrt3}{4}\cdot8=2\sqrt3$。<br>(2) 体積は $\frac13\cdot2\sqrt3\cdot(\text{P と平面 ABC の距離})$。$\vec n=\frac{1}{\sqrt3}(1,1,1)$（平面 ABC の単位法線ベクトル、$\overrightarrow{\mathrm{OH}}$ と同じ向き）とすると、P と平面の距離は $|\overrightarrow{\mathrm{HP}}\cdot\vec n|=|\overrightarrow{\mathrm{OP}}\cdot\vec n-\mathrm{OH}|=\left|\overrightarrow{\mathrm{OP}}\cdot\vec n-\frac{2}{\sqrt3}\right|$。<br>$|\overrightarrow{\mathrm{OP}}|=1$ より $-1\leqq\overrightarrow{\mathrm{OP}}\cdot\vec n\leqq1$ なので、距離の最大値は $1+\frac{2}{\sqrt3}$（$\overrightarrow{\mathrm{OP}}=-\vec n$ のとき）。<br>体積の最大値は $\frac{2\sqrt3}{3}\left(1+\frac{2}{\sqrt3}\right)=\frac{2\sqrt3+4}{3}$、$\mathrm{P}=-\vec n=\left(-\frac{1}{\sqrt3},-\frac{1}{\sqrt3},-\frac{1}{\sqrt3}\right)$。<br><b>ポイント</b>：底面を固定すると、体積の最大は「高さの最大」。球面上の点と平面の距離は、中心と平面の距離 $\pm$ 半径の範囲を動く。"},
]}}

def verify():
    a = Matrix([1, -1, 2]); b = Matrix([2, 1, 1])
    assert a.dot(b) == 3 and a.norm() == b.norm() == sqrt(6)
    assert acos(a.dot(b)/(a.norm()*b.norm())) == pi/3
    n = Matrix([-1, 1, 1])/sqrt(3)
    assert n.dot(a) == 0 and n.dot(b) == 0 and simplify(n.norm()-1) == 0
    assert a.cross(b) == Matrix([-3, 3, 3])
    # A2
    A, B = Matrix([1, 2, 3]), Matrix([4, -1, 0])
    assert (A+2*B)/3 == Matrix([3, 0, 1]) and -A+2*B == Matrix([7, -4, -3]) and (B-A).norm() == 3*sqrt(3)
    # A3
    x, s, t = symbols("x s t")
    sol = solve(list(Matrix([x-1, 1, 1]) - s*Matrix([-1, 2, 0]) - t*Matrix([-1, 0, 3])), [x, s, t])
    assert sol == {x: Rational(1, 6), s: Rational(1, 2), t: Rational(1, 3)}
    assert Rational(1, 6) + Rational(1, 2) + Rational(1, 3) == 1   # x/1+y/2+z/3=1
    # A4
    assert 2**2+2**2+1 == 9 and 9-1 == 8
    # B1
    k = symbols("k")
    kv = solve(k/3*(2+Rational(3, 2)+4)-1, k)[0]
    assert kv == Rational(2, 5) and kv/3 == Rational(2, 15)
    # 数値で確認：一般の四面体
    Ov = Matrix([0, 0, 0]); av, bv, cv = Matrix([3, 0, 1]), Matrix([1, 4, 0]), Matrix([0, 1, 5])
    P, Q, R = av/2, bv*Rational(2, 3), cv/4
    X = (av+bv+cv)*Rational(2, 15)
    u, v = symbols("u v")
    sl = solve(list(P+u*(Q-P)+v*(R-P)-X), [u, v])
    assert len(sl) == 2   # X は平面 PQR 上
    # B2
    sol = solve([20*s+4*t-4, 4*s+20*t-4], [s, t])
    assert sol == {s: Rational(1, 6), t: Rational(1, 6)}
    H = Matrix([2-2*s-2*t, 4*s, 4*t]).subs(sol)
    assert H == Matrix([Rational(4, 3), Rational(2, 3), Rational(2, 3)])
    AB, AC = Matrix([-2, 4, 0]), Matrix([-2, 0, 4])
    assert H.dot(AB) == 0 and H.dot(AC) == 0 and simplify(H.norm()-2*sqrt(6)/3) == 0
    assert simplify(AB.cross(AC).norm()/2 - 4*sqrt(6)) == 0
    assert simplify(Rational(16, 3) - Rational(1, 3)*4*sqrt(6)*H.norm()) == 0
    # B3
    Pp = Matrix([1+s, s, 0]); Qp = Matrix([0, t, 2+t])
    d = Qp-Pp
    sol = solve([d.dot(Matrix([1, 1, 0])), d.dot(Matrix([0, 1, 1]))], [s, t])
    assert sol == {s: Rational(-4, 3), t: Rational(-5, 3)}
    assert d.subs(sol) == Matrix([1, -1, 1])/3 and simplify(d.subs(sol).norm() - sqrt(3)/3) == 0
    f = expand(d.dot(d))
    assert expand(f - (2*s**2-2*s*t+2*t**2+2*s+4*t+5)) == 0
    assert expand(f - (2*(s-(t-1)/2)**2+Rational(3, 2)*(t+Rational(5, 3))**2+Rational(1, 3))) == 0
    # B4
    O3 = Matrix([0, 0, 0]); a4 = Matrix([1, 0, 0]); b4 = Matrix([Rational(1, 2), sqrt(3)/2, 0])
    c4 = Matrix([Rational(1, 2), sqrt(3)/6, sqrt(Rational(2, 3))])
    for p_, q_ in [(a4, b4), (b4, c4), (c4, a4)]:
        assert simplify((p_-q_).norm()-1) == 0
    MN = (b4+c4)/2 - a4/2
    assert simplify(MN.norm()-sqrt(2)/2) == 0 and simplify(MN.dot(a4)) == 0 and simplify(MN.dot(c4-b4)) == 0
    # B5
    assert expand((t-1)**2+(t-2)**2+(t+1)**2-9 - (3*t**2-4*t-3)) == 0
    r = solve(3*t**2-4*t-3, t)
    assert simplify(abs(r[0]-r[1])*sqrt(3) - 2*sqrt(39)/3) == 0
    assert Rational(16, 9)+4 == Rational(52, 9) and 6-Rational(4, 3) == Rational(14, 3)
    # C1：数値例（OA⊥BC, OB⊥CA を満たす四面体）
    a5, b5 = Matrix([1, 0, 0]), Matrix([0, 1, 0])
    c5 = Matrix([0, 0, 1])   # 直角四面体はこの条件を満たす
    assert a5.dot(c5-b5) == 0 and b5.dot(a5-c5) == 0 and c5.dot(a5-b5) == 0
    a5, b5, c5 = Matrix([2, 1, 0]), Matrix([1, 3, 0]), None
    X3, Y3, Z3 = symbols("X3 Y3 Z3")
    cc = Matrix([X3, Y3, 1])
    sl = solve([a5.dot(cc-b5), b5.dot(a5-cc)], [X3, Y3])
    cc = cc.subs(sl)
    assert simplify(cc.dot(a5-b5)) == 0
    nrm = (b5-a5).cross(cc-a5)
    lam = symbols("lam")
    Hh = nrm*solve((nrm*lam-a5).dot(nrm), lam)[0]
    assert simplify((Hh-a5).dot(cc-b5)) == 0 and simplify((Hh-b5).dot(a5-cc)) == 0 and simplify((Hh-cc).dot(b5-a5)) == 0
    # C2
    A6, B6, C6 = Matrix([2, 0, 0]), Matrix([0, 2, 0]), Matrix([0, 0, 2])
    H6 = Matrix([1, 1, 1])*Rational(2, 3)
    assert H6.dot(B6-A6) == 0 and H6.dot(C6-A6) == 0 and sum(H6) == 2   # 平面 x+y+z=2 上
    area = (B6-A6).cross(C6-A6).norm()/2
    assert simplify(area - 2*sqrt(3)) == 0
    nn = Matrix([1, 1, 1])/sqrt(3)
    Pm = -nn
    dist = abs((Pm-H6).dot(nn))
    assert simplify(dist - (1+2/sqrt(3))) == 0
    V = simplify(area*dist/3)
    assert simplify(V - (4+2*sqrt(3))/3) == 0
    # 体積の直接計算（スカラー三重積）とも一致
    assert simplify(abs((A6-Pm).dot((B6-Pm).cross(C6-Pm)))/6 - V) == 0
