"""問題集 第3章 図形と計量。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {3: {
"goal": "三角比の相互関係・正弦定理・余弦定理・面積公式を、どの量が分かっていてどれを求めるかで使い分ける。空間図形では切り口の三角形を取り出す。",
"items": [
 {"lv": "A", "q": r"$90^\circ<\theta<180^\circ$ で $\sin\theta=\dfrac23$ のとき、$\cos\theta,\ \tan\theta$ の値を求めよ。",
  "a": r"$\cos\theta=-\frac{\sqrt5}{3}$、$\tan\theta=-\frac{2\sqrt5}{5}$",
  "s": r"$\cos^2\theta=1-\frac49=\frac59$。$\theta$ は鈍角なので $\cos\theta<0$、$\cos\theta=-\frac{\sqrt5}3$。$\tan\theta=\frac{\sin\theta}{\cos\theta}=\frac{2/3}{-\sqrt5/3}=-\frac{2}{\sqrt5}=-\frac{2\sqrt5}5$。<br><b>ポイント</b>：平方根をとるときは、角の範囲から符号を決める。"},
 {"lv": "A", "q": r"$\triangle\mathrm{ABC}$ において $b=3,\ c=5,\ A=120^\circ$ のとき、$a$、面積 $S$、外接円の半径 $R$ を求めよ。",
  "a": r"$a=7$、$S=\frac{15\sqrt3}{4}$、$R=\frac{7\sqrt3}{3}$",
  "s": r"余弦定理 $a^2=9+25-2\cdot3\cdot5\cos120^\circ=34+15=49$ より $a=7$。$S=\frac12bc\sin A=\frac12\cdot3\cdot5\cdot\frac{\sqrt3}2=\frac{15\sqrt3}4$。正弦定理 $2R=\frac{a}{\sin A}=\frac{7}{\sqrt3/2}$ より $R=\frac7{\sqrt3}=\frac{7\sqrt3}3$。"},
 {"lv": "A", "q": r"$0^\circ\leqq\theta\leqq180^\circ$ のとき、方程式 $2\sin^2\theta-\cos\theta-1=0$ を解け。",
  "a": r"$\theta=60^\circ,\ 180^\circ$",
  "s": r"$\sin^2\theta=1-\cos^2\theta$ を代入して $2-2\cos^2\theta-\cos\theta-1=0$、すなわち $2\cos^2\theta+\cos\theta-1=0$。$(2\cos\theta-1)(\cos\theta+1)=0$ より $\cos\theta=\frac12,\ -1$。よって $\theta=60^\circ,\ 180^\circ$。<br><b>ポイント</b>：$\sin$ と $\cos$ が混在したら、2乗の側を $\sin^2+\cos^2=1$ で1種類にそろえる。"},
 {"lv": "A", "q": r"$0^\circ\leqq\theta\leqq180^\circ$ で $\sin\theta+\cos\theta=\dfrac13$ のとき、次の値を求めよ。<br>(1) $\sin\theta\cos\theta$　(2) $\sin\theta-\cos\theta$　(3) $\sin^3\theta+\cos^3\theta$",
  "a": r"(1) $-\frac49$　(2) $\frac{\sqrt{17}}{3}$　(3) $\frac{13}{27}$",
  "s": r"(1) 両辺を2乗して $1+2\sin\theta\cos\theta=\frac19$ より $\sin\theta\cos\theta=-\frac49$。(2) $(\sin\theta-\cos\theta)^2=1-2\sin\theta\cos\theta=\frac{17}9$。$\sin\theta\geqq0$ と $\sin\theta\cos\theta<0$ から $\cos\theta<0<\sin\theta$ なので $\sin\theta-\cos\theta>0$、よって $\frac{\sqrt{17}}3$。(3) $(\sin\theta+\cos\theta)(1-\sin\theta\cos\theta)=\frac13\cdot\frac{13}9=\frac{13}{27}$。<br><b>ポイント</b>：和と積は対称式。差は符号を角の範囲から判断する。"},
 {"lv": "B", "tag": "頻出", "q": r"$\triangle\mathrm{ABC}$ において $a=5,\ b=6,\ c=7$ とする。<br>(1) $\cos C,\ \sin C$ を求めよ。　(2) 面積 $S$ を求めよ。<br>(3) 内接円の半径 $r$、外接円の半径 $R$ を求めよ。",
  "a": r"(1) $\cos C=\frac15,\ \sin C=\frac{2\sqrt6}5$　(2) $6\sqrt6$　(3) $r=\frac{2\sqrt6}{3},\ R=\frac{35\sqrt6}{24}$",
  "s": r"(1) $\cos C=\frac{25+36-49}{2\cdot5\cdot6}=\frac{12}{60}=\frac15$、$\sin C=\sqrt{1-\frac1{25}}=\frac{2\sqrt6}5$。(2) $S=\frac12\cdot5\cdot6\cdot\frac{2\sqrt6}5=6\sqrt6$。(3) $S=\frac12r(a+b+c)$ より $6\sqrt6=9r$、$r=\frac{2\sqrt6}3$。$2R=\frac{c}{\sin C}=\frac{7}{2\sqrt6/5}=\frac{35}{2\sqrt6}$ より $R=\frac{35}{4\sqrt6}=\frac{35\sqrt6}{24}$。<br><b>ポイント</b>：3辺が分かれば「余弦定理で cos → sin → 面積 → $r,\ R$」の流れが定番。"},
 {"lv": "B", "q": r"$\triangle\mathrm{ABC}$ において $\mathrm{AB}=6,\ \mathrm{AC}=4,\ \angle\mathrm{A}=60^\circ$ とする。$\angle\mathrm{A}$ の二等分線と辺 $\mathrm{BC}$ の交点を $\mathrm D$ とするとき、$\mathrm{BC},\ \mathrm{AD},\ \mathrm{BD}$ の長さを求めよ。",
  "a": r"$\mathrm{BC}=2\sqrt7$、$\mathrm{AD}=\frac{12\sqrt3}{5}$、$\mathrm{BD}=\frac{6\sqrt7}{5}$",
  "s": r"$\mathrm{BC}^2=36+16-2\cdot6\cdot4\cdot\frac12=28$ より $\mathrm{BC}=2\sqrt7$。$\mathrm{AD}=x$ として面積を2通りに表す：$\triangle\mathrm{ABC}=\triangle\mathrm{ABD}+\triangle\mathrm{ADC}$ より<br>$\frac12\cdot6\cdot4\sin60^\circ=\frac12\cdot6x\sin30^\circ+\frac12\cdot4x\sin30^\circ$、$6\sqrt3=\frac52x$、$x=\frac{12\sqrt3}5$。<br>二等分線の性質 $\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}=3:2$ より $\mathrm{BD}=\frac35\cdot2\sqrt7=\frac{6\sqrt7}5$。<br><b>ポイント</b>：角の二等分線の長さは「面積を分割して2通りに表す」が最速。"},
 {"lv": "B", "tag": "頻出", "q": r"円に内接する四角形 $\mathrm{ABCD}$ において、$\mathrm{AB}=5,\ \mathrm{BC}=3,\ \mathrm{CD}=3,\ \mathrm{DA}=8$ である。<br>(1) $\cos B$ の値と $\angle B$ を求めよ。　(2) 対角線 $\mathrm{AC}$ の長さを求めよ。<br>(3) 四角形 $\mathrm{ABCD}$ の面積と、円の半径を求めよ。",
  "a": r"(1) $\cos B=-\frac12,\ B=120^\circ$　(2) $7$　(3) 面積 $\frac{39\sqrt3}{4}$、半径 $\frac{7\sqrt3}{3}$",
  "s": r"(1) 円に内接するので $D=180^\circ-B$、$\cos D=-\cos B$。$\triangle\mathrm{ABC}$ と $\triangle\mathrm{ACD}$ で $\mathrm{AC}^2$ を2通りに表す：<br>$25+9-30\cos B=9+64+48\cos B$ より $78\cos B=-39$、$\cos B=-\frac12$、$B=120^\circ$。<br>(2) $\mathrm{AC}^2=34-30\cdot(-\frac12)=49$ より $\mathrm{AC}=7$。<br>(3) $D=60^\circ$。面積は $\frac12\cdot5\cdot3\sin120^\circ+\frac12\cdot3\cdot8\sin60^\circ=\frac{15\sqrt3}4+6\sqrt3=\frac{39\sqrt3}4$。半径は $\triangle\mathrm{ABC}$ の外接円の半径なので $\frac{7}{2\sin120^\circ}=\frac7{\sqrt3}=\frac{7\sqrt3}3$。<br><b>ポイント</b>：内接四角形は「向かい合う角の和が $180^\circ$」で、対角線を共有する2つの三角形に余弦定理。"},
 {"lv": "B", "tag": "空間図形", "q": r"四面体 $\mathrm{OABC}$ において、$\mathrm{OA}=1,\ \mathrm{OB}=\mathrm{OC}=2$ で、$\angle\mathrm{AOB}=\angle\mathrm{BOC}=\angle\mathrm{COA}=90^\circ$ である。<br>(1) $\cos\angle\mathrm{BAC}$ と $\triangle\mathrm{ABC}$ の面積を求めよ。<br>(2) 点 $\mathrm O$ から平面 $\mathrm{ABC}$ に下ろした垂線の長さ $h$ を求めよ。",
  "a": r"(1) $\cos\angle\mathrm{BAC}=\frac15$、面積 $\sqrt6$　(2) $h=\frac{\sqrt6}{3}$",
  "s": r"(1) 三平方の定理で $\mathrm{AB}=\mathrm{AC}=\sqrt5,\ \mathrm{BC}=2\sqrt2$。$\cos\angle\mathrm{BAC}=\frac{5+5-8}{2\cdot5}=\frac15$、$\sin\angle\mathrm{BAC}=\frac{2\sqrt6}5$。面積 $=\frac12\cdot\sqrt5\cdot\sqrt5\cdot\frac{2\sqrt6}5=\sqrt6$。<br>(2) 底面を $\triangle\mathrm{OBC}$ とみると体積 $V=\frac13\cdot\frac12\cdot2\cdot2\cdot1=\frac23$。底面を $\triangle\mathrm{ABC}$ とみると $V=\frac13\cdot\sqrt6\cdot h$。よって $h=\frac{2}{\sqrt6}=\frac{\sqrt6}3$。<br><b>ポイント</b>：点と平面の距離は「体積を2通りに表す」。"},
 {"lv": "B", "q": r"$\triangle\mathrm{ABC}$ について次の問いに答えよ。<br>(1) $\sin A:\sin B:\sin C=3:5:7$ のとき、最も大きい角の大きさを求めよ。<br>(2) $a\cos A=b\cos B$ が成り立つとき、$\triangle\mathrm{ABC}$ はどのような形の三角形か。",
  "a": r"(1) $120^\circ$　(2) $a=b$ の二等辺三角形、または $C=90^\circ$ の直角三角形",
  "s": r"(1) 正弦定理より $a:b:c=3:5:7$。$a=3k,\ b=5k,\ c=7k$ とおくと最大角は $C$ で、$\cos C=\frac{9+25-49}{2\cdot3\cdot5}=-\frac12$、$C=120^\circ$。<br>(2) 余弦定理で辺だけの式にする：$a\cdot\frac{b^2+c^2-a^2}{2bc}=b\cdot\frac{c^2+a^2-b^2}{2ca}$。両辺に $2abc$ を掛けて $a^2(b^2+c^2-a^2)=b^2(c^2+a^2-b^2)$。整理すると $c^2(a^2-b^2)-(a^4-b^4)=0$、すなわち $(a^2-b^2)(c^2-a^2-b^2)=0$。よって $a=b$ または $c^2=a^2+b^2$。<br><b>ポイント</b>：形状決定は「辺だけ」の式に直して因数分解。答えの「または」を落とさない。"},
 {"lv": "C", "tag": "最大・最小", "q": r"半径 $1$ の円に内接する $\triangle\mathrm{ABC}$ において $A=60^\circ$ とする。<br>(1) 辺 $\mathrm{BC}$ の長さ $a$ を求めよ。<br>(2) $b+c$ の最大値を求めよ。　(3) $\triangle\mathrm{ABC}$ の面積の最大値を求めよ。",
  "a": r"(1) $\sqrt3$　(2) $2\sqrt3$　(3) $\frac{3\sqrt3}{4}$（いずれも正三角形のとき）",
  "s": r"(1) 正弦定理 $a=2R\sin A=2\sin60^\circ=\sqrt3$。<br>(2) 余弦定理 $3=b^2+c^2-bc=(b+c)^2-3bc$。相加・相乗平均の関係より $bc\leqq\left(\frac{b+c}2\right)^2$ なので $3\geqq(b+c)^2-\frac34(b+c)^2=\frac14(b+c)^2$。よって $b+c\leqq2\sqrt3$。等号は $b=c=\sqrt3$（正三角形）のときで、実際にこの三角形は存在する。<br>(3) $3=b^2+c^2-bc\geqq2bc-bc=bc$ より $bc\leqq3$。面積 $=\frac12bc\sin60^\circ\leqq\frac{3\sqrt3}4$。等号は $b=c$（正三角形）のとき。<br><b>ポイント</b>：1つの辺と対角が固定された三角形は、余弦定理を「和と積」の関係として読み、相加・相乗平均で評価する。等号成立の確認を忘れない。"},
 {"lv": "C", "tag": "空間図形", "q": r"四面体 $\mathrm{ABCD}$ において、$\mathrm{AB}=\mathrm{CD}=\sqrt5,\ \mathrm{AC}=\mathrm{BD}=\sqrt{10},\ \mathrm{AD}=\mathrm{BC}=\sqrt{13}$ である。<br>(1) 3辺の長さが $p,\ q,\ r\ (p<q<r)$ の直方体の4つの頂点をうまく選ぶと、この四面体の頂点になる。$p,\ q,\ r$ を求めよ。<br>(2) 四面体 $\mathrm{ABCD}$ の体積 $V$ を求めよ。<br>(3) 四面体 $\mathrm{ABCD}$ の外接球の半径と内接球の半径を求めよ。",
  "a": r"(1) $p=1,\ q=2,\ r=3$　(2) $V=2$　(3) 外接球 $\frac{\sqrt{14}}{2}$、内接球 $\frac37$",
  "s": r"(1) 直方体の向かい合う2面の、ねじれの位置にある対角線を対辺とする四面体を考える。各辺は面の対角線なので $p^2+q^2=5,\ p^2+r^2=10,\ q^2+r^2=13$。辺々加えて $p^2+q^2+r^2=14$、よって $r^2=9,\ q^2=4,\ p^2=1$。$p=1,\ q=2,\ r=3$。<br>(2) 直方体から、四面体に含まれない4隅の三角錐（それぞれ体積 $\frac13\cdot\frac12pq\cdot r=\frac16pqr$）を除く。$V=pqr-4\cdot\frac16pqr=\frac13pqr=2$。<br>(3) 外接球は直方体の外接球と同じで、半径は対角線の半分 $\frac{\sqrt{p^2+q^2+r^2}}2=\frac{\sqrt{14}}2$。<br>4つの面はすべて3辺が $\sqrt5,\ \sqrt{10},\ \sqrt{13}$ の合同な三角形。長さ $\sqrt{13}$ の辺の対角を $\theta$ とすると $\cos\theta=\frac{5+10-13}{2\sqrt{50}}=\frac{1}{5\sqrt2}$、$\sin\theta=\sqrt{1-\frac1{50}}=\frac{7}{5\sqrt2}$。1面の面積は $\frac12\sqrt5\sqrt{10}\cdot\frac7{5\sqrt2}=\frac72$、表面積は $14$。内接球の半径を $\rho$ とすると $V=\frac13\cdot14\rho$ より $\rho=\frac{3V}{14}=\frac37$。<br><b>ポイント</b>：対辺の長さが等しい四面体（等面四面体）は直方体に埋め込む。内接球の半径は「体積 $=\frac13\times$表面積$\times$半径」。"},
]}}


def verify():
    t = symbols("t")
    # A1
    s1 = Rational(2, 3); c1 = -sqrt(1-s1**2)
    assert simplify(c1+sqrt(5)/3) == 0 and simplify(s1/c1 + 2*sqrt(5)/5) == 0
    # A2
    a2 = sqrt(9+25-2*3*5*cos(rad(120)))
    assert simplify(a2-7) == 0
    assert simplify(Rational(1, 2)*3*5*sin(rad(120)) - 15*sqrt(3)/4) == 0
    assert simplify(7/(2*sin(rad(120))) - 7*sqrt(3)/3) == 0
    # A3: 0..180 度で数値的に解を探す
    sols = [d for d in range(0, 181) if abs(N(2*sin(rad(d))**2-cos(rad(d))-1)) < 1e-12]
    assert sols == [60, 180]
    # A4
    th = nsolve(sin(t)+cos(t)-Rational(1, 3), t, 2.0)
    assert 0 < th < pi
    assert abs(N(sin(th)*cos(th)+Rational(4, 9))) < 1e-12
    assert abs(N(sin(th)-cos(th)-sqrt(17)/3)) < 1e-12
    assert abs(N(sin(th)**3+cos(th)**3-Rational(13, 27))) < 1e-12
    # B1
    a, b, c = 5, 6, 7
    cC = Rational(a*a+b*b-c*c, 2*a*b); sC = sqrt(1-cC**2)
    assert cC == Rational(1, 5) and simplify(sC-2*sqrt(6)/5) == 0
    S = Rational(1, 2)*a*b*sC
    assert simplify(S-6*sqrt(6)) == 0
    assert simplify(2*S/(a+b+c) - 2*sqrt(6)/3) == 0
    assert simplify(c/(2*sC) - 35*sqrt(6)/24) == 0
    # B2: 座標で確認
    A = Matrix([0, 0]); B = Matrix([6, 0]); C = Matrix([4*cos(rad(60)), 4*sin(rad(60))])
    assert simplify((B-C).norm()-2*sqrt(7)) == 0
    D = B + Rational(3, 5)*(C-B)
    assert simplify(D.norm()-12*sqrt(3)/5) == 0 and simplify((D-B).norm()-6*sqrt(7)/5) == 0
    # 角の二等分線上にあることの確認
    assert simplify(atan2(D[1], D[0]) - pi/6) == 0
    # B3
    cB = symbols("cB")
    sol = solve(25+9-30*cB-(9+64+48*cB), cB)
    assert sol == [Rational(-1, 2)]
    assert 34-30*Rational(-1, 2) == 49
    area = Rational(1, 2)*15*sin(rad(120))+Rational(1, 2)*24*sin(rad(60))
    assert simplify(area-39*sqrt(3)/4) == 0
    # BD をトレミーなしで（cos A を2通り）確認し、円に内接することを数値で確認
    cA = symbols("cA")
    cAv = solve(25+64-80*cA-(9+9+18*cA), cA)[0]
    BD = sqrt(18+18*cAv)
    assert simplify(BD-Rational(39, 7)) == 0
    assert simplify(7*BD - (5*3+3*8)) == 0
    # B4
    O = Matrix([0, 0, 0]); A3 = Matrix([1, 0, 0]); B3 = Matrix([0, 2, 0]); C3 = Matrix([0, 0, 2])
    ab, ac = B3-A3, C3-A3
    assert ab.dot(ac)/(ab.norm()*ac.norm()) == Rational(1, 5)
    ar = ab.cross(ac).norm()/2
    assert simplify(ar-sqrt(6)) == 0
    nrm = ab.cross(ac)
    h = Abs(nrm.dot(O-A3))/nrm.norm()
    assert simplify(h-sqrt(6)/3) == 0
    # B5
    assert Rational(9+25-49, 30) == Rational(-1, 2)
    a_, b_, c_ = symbols("a b c", positive=True)
    lhs = a_**2*(b_**2+c_**2-a_**2) - b_**2*(c_**2+a_**2-b_**2)
    assert expand(lhs - (a_**2-b_**2)*(c_**2-a_**2-b_**2)) == 0
    # C1: 数値で最大を探索（B を動かす）
    import math
    best_sum = best_area = 0
    for k in range(1, 1200):
        Bang = math.pi*2/3*k/1200
        Cang = math.pi*2/3-Bang
        bb, cc = 2*math.sin(Bang), 2*math.sin(Cang)
        best_sum = max(best_sum, bb+cc); best_area = max(best_area, bb*cc*math.sin(math.pi/3)/2)
    assert abs(best_sum-N(2*sqrt(3))) < 1e-5 and abs(best_area-N(3*sqrt(3)/4)) < 1e-5
    assert simplify(2*sin(pi/3)-sqrt(3)) == 0
    # C2
    p2, q2, r2 = symbols("p2 q2 r2")
    assert solve([p2+q2-5, p2+r2-10, q2+r2-13], [p2, q2, r2]) == {p2: 1, q2: 4, r2: 9}
    PA = Matrix([0, 0, 0]); PB = Matrix([1, 2, 0]); PC = Matrix([1, 0, 3]); PD = Matrix([0, 2, 3])
    d = lambda u, v: (u-v).norm()
    assert d(PA, PB) == sqrt(5) == d(PC, PD) and d(PA, PC) == sqrt(10) == d(PB, PD) and d(PA, PD) == sqrt(13) == d(PB, PC)
    V = Abs(Matrix.hstack(PB-PA, PC-PA, PD-PA).det())/6
    assert V == 2
    cen = Matrix([Rational(1, 2), 1, Rational(3, 2)])
    assert all(simplify(d(cen, P)-sqrt(14)/2) == 0 for P in [PA, PB, PC, PD])
    faces = [(PA, PB, PC), (PA, PB, PD), (PA, PC, PD), (PB, PC, PD)]
    Sface = [simplify((Q-P).cross(R-P).norm()/2) for P, Q, R in faces]
    assert all(f == Rational(7, 2) for f in Sface)
    assert 3*V/sum(Sface) == Rational(3, 7)
