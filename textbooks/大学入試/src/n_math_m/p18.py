"""問題集 第18章 平面ベクトル。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {18: {
"goal": r"成分・内積の計算を確実に。交点の位置ベクトルは「2通りに表して係数比較」、点の存在範囲は「係数の和を1にする」。内積で長さ・角・垂直を処理する。",
"items": [
 {"lv": "A", "q": r"$\vec a=(2,\ 1),\ \vec b=(1,\ 3)$ のとき、(1) $|\vec a+2\vec b|$ を求めよ。(2) $\vec a$ と $\vec b$ のなす角 $\theta$ を求めよ。(3) $\vec a+t\vec b$ と $\vec a$ が垂直になる実数 $t$ を求めよ。",
  "a": r"(1) $\sqrt{65}$　(2) $\theta=45^\circ$　(3) $t=-1$",
  "s": r"(1) $\vec a+2\vec b=(4,\ 7)$ より $\sqrt{16+49}=\sqrt{65}$。<br>(2) $\vec a\cdot\vec b=2+3=5$、$|\vec a|=\sqrt5,\ |\vec b|=\sqrt{10}$。$\cos\theta=\frac{5}{\sqrt{50}}=\frac{1}{\sqrt2}$、$0^\circ\leqq\theta\leqq180^\circ$ より $\theta=45^\circ$。<br>(3) $(\vec a+t\vec b)\cdot\vec a=|\vec a|^2+t\,\vec a\cdot\vec b=5+5t=0$ より $t=-1$。<br><b>ポイント</b>：垂直 ⇔ 内積 $=0$（どちらも $\vec 0$ でないとき）。"},
 {"lv": "A", "q": r"$|\vec a|=2,\ |\vec b|=3,\ \vec a\cdot\vec b=-3$ のとき、$|2\vec a-\vec b|$ の値と、$\vec a,\ \vec b$ のなす角を求めよ。",
  "a": r"$|2\vec a-\vec b|=\sqrt{37}$、なす角 $120^\circ$",
  "s": r"$|2\vec a-\vec b|^2=4|\vec a|^2-4\vec a\cdot\vec b+|\vec b|^2=16+12+9=37$ より $\sqrt{37}$。$\cos\theta=\frac{-3}{2\cdot3}=-\frac12$ より $\theta=120^\circ$。<br><b>ポイント</b>：大きさは2乗して内積で展開する。$|\vec a|^2=\vec a\cdot\vec a$。"},
 {"lv": "A", "q": r"3点 $\mathrm{A}(1,\ 2),\ \mathrm{B}(4,\ 3),\ \mathrm{C}(x,\ 7)$ が一直線上にあるように $x$ の値を定めよ。",
  "a": r"$x=16$",
  "s": r"$\overrightarrow{\mathrm{AC}}=k\overrightarrow{\mathrm{AB}}$ となる実数 $k$ がある。$\overrightarrow{\mathrm{AB}}=(3,\ 1)$、$\overrightarrow{\mathrm{AC}}=(x-1,\ 5)$ より $k=5$、$x-1=15$、$x=16$。<br><b>ポイント</b>：一直線上 ⇔ $\overrightarrow{\mathrm{AC}}=k\overrightarrow{\mathrm{AB}}$。成分では $(a_1,a_2)\parallel(b_1,b_2) \iff a_1b_2-a_2b_1=0$ も使える。"},
 {"lv": "A", "q": r"$\overrightarrow{\mathrm{OA}}=(3,\ 1),\ \overrightarrow{\mathrm{OB}}=(1,\ 4)$ のとき、$\triangle\mathrm{OAB}$ の面積を2通りの方法で求めよ。",
  "a": r"$\frac{11}{2}$",
  "s": r"方法1：$S=\frac12|a_1b_2-a_2b_1|=\frac12|3\cdot4-1\cdot1|=\frac{11}{2}$。<br>方法2：$S=\frac12\sqrt{|\vec a|^2|\vec b|^2-(\vec a\cdot\vec b)^2}=\frac12\sqrt{10\cdot17-7^2}=\frac12\sqrt{121}=\frac{11}{2}$。<br><b>ポイント</b>：2つの公式はどちらも $S=\frac12|\vec a||\vec b|\sin\theta$ から導かれる。成分があれば方法1、大きさと内積だけなら方法2。"},
 {"lv": "B", "tag": "典型", "q": r"$\triangle\mathrm{OAB}$ において、$\overrightarrow{\mathrm{OA}}=\vec a,\ \overrightarrow{\mathrm{OB}}=\vec b$ とする。辺 OA を $2:1$ に内分する点を C、辺 OB を $3:1$ に内分する点を D とし、線分 AD と BC の交点を P とする。(1) $\overrightarrow{\mathrm{OP}}$ を $\vec a,\ \vec b$ で表せ。(2) 直線 OP と辺 AB の交点を Q とするとき、$\mathrm{AQ}:\mathrm{QB}$ を求めよ。",
  "a": r"(1) $\overrightarrow{\mathrm{OP}}=\frac13\vec a+\frac12\vec b$　(2) $\mathrm{AQ}:\mathrm{QB}=3:2$",
  "s": r"(1) P は AD 上にあるので $\mathrm{AP}:\mathrm{PD}=s:(1-s)$ として $\overrightarrow{\mathrm{OP}}=(1-s)\vec a+\frac34s\,\vec b$。P は BC 上にもあるので $\mathrm{BP}:\mathrm{PC}=t:(1-t)$ として $\overrightarrow{\mathrm{OP}}=\frac23t\,\vec a+(1-t)\vec b$。<br>$\vec a,\ \vec b$ は1次独立（$\vec 0$ でなく平行でない）なので係数を比べて $1-s=\frac23t,\ \frac34s=1-t$。これを解いて $s=\frac23,\ t=\frac12$。よって $\overrightarrow{\mathrm{OP}}=\frac13\vec a+\frac12\vec b$。<br>(2) $\overrightarrow{\mathrm{OQ}}=k\overrightarrow{\mathrm{OP}}=\frac k3\vec a+\frac k2\vec b$ で、Q が AB 上にあるので係数の和が1：$\frac k3+\frac k2=1$、$k=\frac65$。$\overrightarrow{\mathrm{OQ}}=\frac25\vec a+\frac35\vec b$ より $\mathrm{AQ}:\mathrm{QB}=3:2$。<br><b>ポイント</b>：係数比較をするときは「$\vec a,\vec b$ が1次独立」と明記する。直線 AB 上の点は「係数の和が1」。"},
 {"lv": "B", "tag": "外心・垂心", "q": r"$\triangle\mathrm{OAB}$ において $\overrightarrow{\mathrm{OA}}=\vec a,\ \overrightarrow{\mathrm{OB}}=\vec b$、$|\vec a|=2,\ |\vec b|=3,\ \vec a\cdot\vec b=3$ とする。(1) 外心を P とするとき、$\overrightarrow{\mathrm{OP}}$ を $\vec a,\ \vec b$ で表せ。(2) 垂心を H とするとき、$\overrightarrow{\mathrm{OH}}$ を $\vec a,\ \vec b$ で表せ。",
  "a": r"(1) $\overrightarrow{\mathrm{OP}}=\frac16\vec a+\frac49\vec b$　(2) $\overrightarrow{\mathrm{OH}}=\frac23\vec a+\frac19\vec b$",
  "s": r"(1) $\overrightarrow{\mathrm{OP}}=s\vec a+t\vec b$ とおく。外心は辺 OA の垂直二等分線上にあるので、OA の中点 M について $\overrightarrow{\mathrm{MP}}\cdot\vec a=0$、すなわち $\overrightarrow{\mathrm{OP}}\cdot\vec a=\frac12|\vec a|^2$。同様に $\overrightarrow{\mathrm{OP}}\cdot\vec b=\frac12|\vec b|^2$。<br>$4s+3t=2$、$3s+9t=\frac92$。解いて $s=\frac16,\ t=\frac49$。<br>(2) $\overrightarrow{\mathrm{OH}}=x\vec a+y\vec b$ とおく。$\overrightarrow{\mathrm{AH}}\perp\vec b$：$(\overrightarrow{\mathrm{OH}}-\vec a)\cdot\vec b=3x+9y-3=0$。$\overrightarrow{\mathrm{BH}}\perp\vec a$：$(\overrightarrow{\mathrm{OH}}-\vec b)\cdot\vec a=4x+3y-3=0$。解いて $x=\frac23,\ y=\frac19$。<br>（検算）外心 P を基準にすると $\overrightarrow{\mathrm{PH}}=\overrightarrow{\mathrm{PO}}+\overrightarrow{\mathrm{PA}}+\overrightarrow{\mathrm{PB}}$ が成り立つ（18-10 参照）。これを O 基準に直すと $\overrightarrow{\mathrm{OH}}=\vec a+\vec b-2\overrightarrow{\mathrm{OP}}=\frac23\vec a+\frac19\vec b$ で一致する。<br><b>ポイント</b>：外心は「$\overrightarrow{\mathrm{OP}}\cdot\vec a=\frac12|\vec a|^2$」、垂心は「頂点から引いたベクトルと対辺の内積 $=0$」の2本の式で決まる。"},
 {"lv": "B", "tag": "存在範囲", "q": r"$\mathrm{O}(0,\ 0),\ \mathrm{A}(2,\ 1),\ \mathrm{B}(1,\ 3)$ とする。$\overrightarrow{\mathrm{OP}}=s\overrightarrow{\mathrm{OA}}+t\overrightarrow{\mathrm{OB}}$、$s\geqq0,\ t\geqq0,\ s+2t\leqq2$ を満たす点 P の存在範囲を図示し、その面積を求めよ。",
  "a": r"$\overrightarrow{\mathrm{OA'}}=2\overrightarrow{\mathrm{OA}}$ となる点 $\mathrm{A'}(4,2)$ をとって、$\triangle\mathrm{OA'B}$ の周および内部。面積 $5$",
  "s": r"$s+2t\leqq2$ を $\frac s2+t\leqq1$ と変形し、$s'=\frac s2$ とおくと $\overrightarrow{\mathrm{OP}}=s'(2\overrightarrow{\mathrm{OA}})+t\overrightarrow{\mathrm{OB}}$、$s'\geqq0,\ t\geqq0,\ s'+t\leqq1$。<br>よって $\overrightarrow{\mathrm{OA'}}=2\overrightarrow{\mathrm{OA}}$、すなわち $\mathrm{A'}(4,\ 2)$ とすると、P の存在範囲は $\triangle\mathrm{OA'B}$ の周および内部。面積は $\frac12|4\cdot3-2\cdot1|=5$（$\triangle\mathrm{OAB}=\frac52$ の2倍）。<svg class='fig' width='210' height='160' viewBox='0 0 210 160'><polygon points='30,135 182,59 68,21' fill='#cfe0ff' stroke='#1f3f8f' stroke-width='1.3'/><line x1='4' y1='135' x2='206' y2='135' stroke='#555'/><line x1='30' y1='156' x2='30' y2='4' stroke='#555'/><text x='198' y='148' font-size='11'>x</text><text x='35' y='13' font-size='11'>y</text><circle cx='30' cy='135' r='2.2' fill='#1e1e1e'/><text x='18' y='148' font-size='11' fill='#1e1e1e' text-anchor='start'>O</text><circle cx='106' cy='97' r='2.2' fill='#1e1e1e'/><text x='108' y='111' font-size='11' fill='#1e1e1e' text-anchor='start'>A</text><circle cx='182' cy='59' r='2.2' fill='#1e1e1e'/><text x='174' y='73' font-size='11' fill='#1e1e1e' text-anchor='start'>A′</text><circle cx='68' cy='21' r='2.2' fill='#1e1e1e'/><text x='64' y='15' font-size='11' fill='#1e1e1e' text-anchor='start'>B</text></svg><b>ポイント</b>：「$s+t\leqq1,\ s\geqq0,\ t\geqq0$」なら $\triangle\mathrm{OAB}$。係数の和が1になるように、ベクトルの側を伸び縮みさせて読みかえる。"},
 {"lv": "B", "tag": "頻出", "q": r"$\triangle\mathrm{ABC}$ と点 P が $3\overrightarrow{\mathrm{PA}}+4\overrightarrow{\mathrm{PB}}+5\overrightarrow{\mathrm{PC}}=\vec 0$ を満たす。(1) 点 P はどのような位置にあるか。(2) $\triangle\mathrm{PBC}:\triangle\mathrm{PCA}:\triangle\mathrm{PAB}$ を求めよ。",
  "a": r"(1) 辺 BC を $5:4$ に内分する点を D とすると、線分 AD を $3:1$ に内分する点　(2) $3:4:5$",
  "s": r"(1) A を始点にすると $-3\overrightarrow{\mathrm{AP}}+4(\overrightarrow{\mathrm{AB}}-\overrightarrow{\mathrm{AP}})+5(\overrightarrow{\mathrm{AC}}-\overrightarrow{\mathrm{AP}})=\vec0$ より $\overrightarrow{\mathrm{AP}}=\frac{4\overrightarrow{\mathrm{AB}}+5\overrightarrow{\mathrm{AC}}}{12}=\frac{9}{12}\cdot\frac{4\overrightarrow{\mathrm{AB}}+5\overrightarrow{\mathrm{AC}}}{9}$。<br>$\overrightarrow{\mathrm{AD}}=\frac{4\overrightarrow{\mathrm{AB}}+5\overrightarrow{\mathrm{AC}}}{9}$ は BC を $5:4$ に内分する点 D を表し、$\overrightarrow{\mathrm{AP}}=\frac34\overrightarrow{\mathrm{AD}}$ なので P は AD を $3:1$ に内分する点。<br>(2) $\triangle\mathrm{ABC}$ の面積を $S$ とする。$\mathrm{PD}=\frac14\mathrm{AD}$ より $\triangle\mathrm{PBC}=\frac14S$。$\triangle\mathrm{ABD}=\frac59S$ で $\triangle\mathrm{PAB}=\frac34\cdot\frac59S=\frac{5}{12}S$。同様に $\triangle\mathrm{PCA}=\frac34\cdot\frac49S=\frac{4}{12}S$。よって $\frac{3}{12}:\frac{4}{12}:\frac{5}{12}=3:4:5$。<br><b>ポイント</b>：$a\overrightarrow{\mathrm{PA}}+b\overrightarrow{\mathrm{PB}}+c\overrightarrow{\mathrm{PC}}=\vec0$（$a,b,c\gt0$）なら、面積比は $\triangle\mathrm{PBC}:\triangle\mathrm{PCA}:\triangle\mathrm{PAB}=a:b:c$。"},
 {"lv": "B", "tag": "内積の最大最小", "q": r"$\mathrm{A}(3,\ 0),\ \mathrm{B}(0,\ 4)$ とし、点 P は原点 O を中心とする半径1の円周上を動く。内積 $\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}$ の最大値と最小値、およびそのときの P の座標を求めよ。",
  "a": r"最大値 $6$（$\mathrm{P}\left(-\frac35,\ -\frac45\right)$）、最小値 $-4$（$\mathrm{P}\left(\frac35,\ \frac45\right)$）",
  "s": r"$\vec p=\overrightarrow{\mathrm{OP}}$ とすると $\overrightarrow{\mathrm{PA}}\cdot\overrightarrow{\mathrm{PB}}=(\vec a-\vec p)\cdot(\vec b-\vec p)=\vec a\cdot\vec b-(\vec a+\vec b)\cdot\vec p+|\vec p|^2=0-(\vec a+\vec b)\cdot\vec p+1$。<br>$\vec a+\vec b=(3,\ 4)$、$|\vec a+\vec b|=5$。$\vec a+\vec b$ と $\vec p$ のなす角を $\theta$ とすると $(\vec a+\vec b)\cdot\vec p=5\cos\theta$ で、$-5\leqq5\cos\theta\leqq5$。<br>よって最大値 $1+5=6$（$\vec p$ が $\vec a+\vec b$ と逆向き：$\mathrm{P}\left(-\frac35,-\frac45\right)$）、最小値 $1-5=-4$（同じ向き：$\mathrm{P}\left(\frac35,\frac45\right)$）。<br><b>ポイント</b>：動く点 $\vec p$ について整理すると、「定ベクトルとの内積」の最大最小になる。なす角で考えるのが速い。"},
 {"lv": "C", "tag": "論証", "q": r"$\triangle\mathrm{ABC}$ の外心を O、重心を G とし、$\overrightarrow{\mathrm{OH}}=\overrightarrow{\mathrm{OA}}+\overrightarrow{\mathrm{OB}}+\overrightarrow{\mathrm{OC}}$ で点 H を定める。<br>(1) H は $\triangle\mathrm{ABC}$ の垂心であることを示せ。<br>(2) $\triangle\mathrm{ABC}$ が正三角形でないとき、3点 O、G、H は一直線上にあり、$\mathrm{OG}:\mathrm{GH}=1:2$ であることを示せ。",
  "a": r"証明（解説参照）",
  "s": r"$\vec a=\overrightarrow{\mathrm{OA}}$ などとおく。O は外心なので $|\vec a|=|\vec b|=|\vec c|$（外接円の半径）。<br>(1) $\overrightarrow{\mathrm{AH}}=\vec b+\vec c$、$\overrightarrow{\mathrm{BC}}=\vec c-\vec b$ より $\overrightarrow{\mathrm{AH}}\cdot\overrightarrow{\mathrm{BC}}=|\vec c|^2-|\vec b|^2=0$。よって $\mathrm{AH}\perp\mathrm{BC}$ または $\mathrm{H}=\mathrm{A}$。同様に $\overrightarrow{\mathrm{BH}}\cdot\overrightarrow{\mathrm{CA}}=(\vec c+\vec a)\cdot(\vec a-\vec c)=0$。<br>H が A, B のいずれとも異なれば、H は A から BC への垂線と B から CA への垂線の上にあり、垂心である。H$=$A のときは $\vec b+\vec c=\vec 0$、すなわち BC が外接円の直径で $\angle\mathrm{A}=90^\circ$ となり、直角三角形の垂心は直角の頂点 A なので、やはり H は垂心。H$=$B のときも同様。■<br>(2) $\overrightarrow{\mathrm{OG}}=\frac{\vec a+\vec b+\vec c}{3}=\frac13\overrightarrow{\mathrm{OH}}$。正三角形でなければ外心と重心は一致しない（一致すると各中線が垂直二等分線となり、3辺が等しくなる）ので $\overrightarrow{\mathrm{OG}}\neq\vec0$。よって O、G、H は一直線上にあり、$\mathrm{OG}:\mathrm{OH}=1:3$、すなわち $\mathrm{OG}:\mathrm{GH}=1:2$。■<br><b>ポイント</b>：この直線をオイラー線という。「外心を始点にとる」と $|\vec a|=|\vec b|=|\vec c|$ が使え、垂直の証明が内積1行で済む。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$\mathrm{A}(1,\ 1),\ \mathrm{B}(5,\ 2),\ \mathrm{C}(3,\ 6)$ とし、$\triangle\mathrm{ABC}$ の重心を G とする。<br>(1) 任意の点 P について $\mathrm{PA}^2+\mathrm{PB}^2+\mathrm{PC}^2=3\mathrm{PG}^2+\mathrm{GA}^2+\mathrm{GB}^2+\mathrm{GC}^2$ が成り立つことを示せ。<br>(2) 点 P が直線 $y=x+2$ 上を動くとき、$\mathrm{PA}^2+\mathrm{PB}^2+\mathrm{PC}^2$ の最小値と、そのときの P の座標を求めよ。",
  "a": r"(2) 最小値 $28$、$\mathrm{P}(2,\ 4)$",
  "s": r"(1) G を始点とし、$\vec a=\overrightarrow{\mathrm{GA}}$ などとおくと $\vec a+\vec b+\vec c=\vec0$。$\vec p=\overrightarrow{\mathrm{GP}}$ として<br>$\sum|\vec a-\vec p|^2=|\vec a|^2+|\vec b|^2+|\vec c|^2-2(\vec a+\vec b+\vec c)\cdot\vec p+3|\vec p|^2=3\mathrm{PG}^2+\mathrm{GA}^2+\mathrm{GB}^2+\mathrm{GC}^2$。■<br>(2) $\mathrm{G}(3,\ 3)$。$\mathrm{GA}^2=4+4=8$、$\mathrm{GB}^2=4+1=5$、$\mathrm{GC}^2=0+9=9$ で和は $22$。(1) より、$\mathrm{PG}$ が最小のとき、すなわち P が G から直線 $x-y+2=0$ に下ろした垂線の足のとき最小。<br>G と直線の距離は $\frac{|3-3+2|}{\sqrt2}=\sqrt2$ なので、最小値は $3\cdot2+22=28$。垂線の足は、G を通り直線の法線ベクトル $(1,\ -1)$ に平行な直線上の点 $(3-u,\ 3+u)$ とおいて直線の式に代入：$3+u=3-u+2$、$u=1$ で $\mathrm{P}(2,\ 4)$。<br>（検算）$\mathrm{PA}^2+\mathrm{PB}^2+\mathrm{PC}^2=(1+9)+(9+4)+(1+4)=28$。<br><b>ポイント</b>：重心を始点にすると $\vec a+\vec b+\vec c=\vec0$ で1次の項が消え、「重心からの距離」だけの式になる。"},
]}}

def verify():
    a = Matrix([2, 1]); b = Matrix([1, 3])
    assert (a+2*b).norm() == sqrt(65) and a.dot(b) == 5
    assert acos(a.dot(b)/(a.norm()*b.norm())) == pi/4
    t = symbols("t")
    assert solve((a+t*b).dot(a), t) == [-1]
    # A2
    assert 4*4-4*(-3)+9 == 37 and Rational(-3, 6) == Rational(-1, 2)
    # A3
    x = symbols("x")
    assert solve(3*5-1*(x-1), x) == [16]
    # A4
    A = Matrix([3, 1]); B = Matrix([1, 4])
    assert Rational(1, 2)*abs(A[0]*B[1]-A[1]*B[0]) == Rational(11, 2)
    assert Rational(1, 2)*sqrt(A.dot(A)*B.dot(B)-A.dot(B)**2) == Rational(11, 2)
    # B1：一般の a, b で係数比較
    s, tt = symbols("s tt")
    sol = solve([1-s-Rational(2, 3)*tt, Rational(3, 4)*s-(1-tt)], [s, tt])
    assert sol == {s: Rational(2, 3), tt: Rational(1, 2)}
    assert 1-sol[s] == Rational(1, 3) and Rational(3, 4)*sol[s] == Rational(1, 2)
    k = solve(x/3+x/2-1, x)[0]
    assert k == Rational(6, 5) and k/3 == Rational(2, 5) and k/2 == Rational(3, 5)
    # 数値例で交点を直接確認
    a0, b0 = Matrix([4, 1]), Matrix([1, 5])
    C0, D0 = a0*Rational(2, 3), b0*Rational(3, 4)
    u, v = symbols("u v")
    sl = solve(list(a0+u*(D0-a0) - (b0+v*(C0-b0))), [u, v])
    Pp = a0+sl[u]*(D0-a0)
    assert Pp == a0/3+b0/2
    # B2
    sol = solve([4*s+3*tt-2, 3*s+9*tt-Rational(9, 2)], [s, tt])
    assert sol == {s: Rational(1, 6), tt: Rational(4, 9)}
    sol2 = solve([3*s+9*tt-3, 4*s+3*tt-3], [s, tt])
    assert sol2 == {s: Rational(2, 3), tt: Rational(1, 9)}
    assert 1-2*Rational(1, 6) == Rational(2, 3) and 1-2*Rational(4, 9) == Rational(1, 9)
    # 具体的な座標で：|a|=2, |b|=3, a.b=3 → a=(2,0), b=(3/2, 3√3/2)
    aa = Matrix([2, 0]); bb = Matrix([Rational(3, 2), 3*sqrt(3)/2])
    assert aa.dot(bb) == 3 and simplify(bb.norm()-3) == 0
    Pc = aa/6+bb*Rational(4, 9)
    assert simplify(Pc.norm()-(Pc-aa).norm()) == 0 and simplify(Pc.norm()-(Pc-bb).norm()) == 0
    Hc = aa*Rational(2, 3)+bb/9
    assert simplify((Hc-aa).dot(bb)) == 0 and simplify((Hc-bb).dot(aa)) == 0
    # B3
    assert Rational(1, 2)*abs(4*3-2*1) == 5 and Rational(1, 2)*abs(2*3-1*1) == Rational(5, 2)
    # B4：数値例
    Aq, Bq, Cq = Matrix([0, 0]), Matrix([7, 1]), Matrix([2, 5])
    Pq = (3*Aq+4*Bq+5*Cq)/12
    Dq = (4*Bq+5*Cq)/9
    assert Pq == Aq+Rational(3, 4)*(Dq-Aq)
    assert (Dq-Bq) == Rational(5, 9)*(Cq-Bq)
    area = lambda X, Y, Z: abs((Y-X)[0]*(Z-X)[1]-(Y-X)[1]*(Z-X)[0])/2
    S = area(Aq, Bq, Cq)
    assert [area(Pq, Bq, Cq)/S, area(Pq, Cq, Aq)/S, area(Pq, Aq, Bq)/S] == [Rational(3, 12), Rational(4, 12), Rational(5, 12)]
    # B5
    th = symbols("th", real=True)
    p = Matrix([cos(th), sin(th)])
    Av, Bv = Matrix([3, 0]), Matrix([0, 4])
    f = expand((Av-p).dot(Bv-p))
    assert simplify(f - (1-3*cos(th)-4*sin(th))) == 0
    for P0, val in [((-Rational(3, 5), -Rational(4, 5)), 6), ((Rational(3, 5), Rational(4, 5)), -4)]:
        q = Matrix(P0)
        assert (Av-q).dot(Bv-q) == val and q.dot(q) == 1
    # C1：数値例（外心を原点にとる）
    r = 5
    Ap, Bp, Cp = Matrix([5, 0]), Matrix([3, 4]), Matrix([-4, -3])
    assert all(v.dot(v) == r**2 for v in (Ap, Bp, Cp))
    H = Ap+Bp+Cp
    assert (H-Ap).dot(Cp-Bp) == 0 and (H-Bp).dot(Ap-Cp) == 0 and (H-Cp).dot(Bp-Ap) == 0
    G = (Ap+Bp+Cp)/3
    assert G*3 == H
    # C2
    A2, B2, C2 = Matrix([1, 1]), Matrix([5, 2]), Matrix([3, 6])
    G = (A2+B2+C2)/3
    assert G == Matrix([3, 3])
    X, Y = symbols("X Y", real=True)
    P2 = Matrix([X, Y])
    lhs = sum(((P2-V).dot(P2-V) for V in (A2, B2, C2)), 0)
    rhs = 3*(P2-G).dot(P2-G)+sum(((V-G).dot(V-G) for V in (A2, B2, C2)), 0)
    assert expand(lhs-rhs) == 0 and sum(((V-G).dot(V-G) for V in (A2, B2, C2)), 0) == 22
    g = expand(lhs.subs(Y, X+2))
    xm = solve(diff(g, X), X)[0]
    assert xm == 2 and g.subs(X, 2) == 28
