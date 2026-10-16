"""問題集 第20章 複素数平面。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CH = {20: {
"goal": r"極形式とド・モアブルの定理で積・累乗・$n$ 乗根を処理する。回転は「かける」、図形の条件は $|z-\alpha|$ と $\arg\frac{\gamma-\alpha}{\beta-\alpha}$ で読む。",
"items": [
 {"lv": "A", "q": r"$z=1+\sqrt3i,\ w=1-i$ とする。(1) $z,\ w$ を極形式で表せ（偏角 $\theta$ は $0^\circ\leqq\theta\lt360^\circ$）。(2) $zw$ を極形式で表せ。(3) $z^6$ を求めよ。",
  "a": r"(1) $z=2(\cos60^\circ+i\sin60^\circ)$、$w=\sqrt2(\cos315^\circ+i\sin315^\circ)$　(2) $2\sqrt2(\cos15^\circ+i\sin15^\circ)$　(3) $64$",
  "s": r"(1) $|z|=2$、$z=2\left(\frac12+\frac{\sqrt3}{2}i\right)$。$|w|=\sqrt2$、$w=\sqrt2\left(\frac{1}{\sqrt2}-\frac{1}{\sqrt2}i\right)$。<br>(2) 積は「絶対値はかけ、偏角は足す」：$|zw|=2\sqrt2$、偏角 $60^\circ+315^\circ=375^\circ$、すなわち $15^\circ$。<br>(3) ド・モアブルの定理より $z^6=2^6(\cos360^\circ+i\sin360^\circ)=64$。<br><b>ポイント</b>：偏角は $360^\circ$ の整数倍の違いを除いて決まる。指定の範囲に直して答える。"},
 {"lv": "A", "q": r"次の等式を満たす点 $z$ 全体はどのような図形か。(1) $|z-2i|=|z+4|$　(2) $|z-1|=2|z+2|$",
  "a": r"(1) 直線 $2x+y+3=0$（2点 $2i,\ -4$ を結ぶ線分の垂直二等分線）　(2) 点 $-3$ を中心とする半径 $2$ の円",
  "s": r"$z=x+yi$ とおく。<br>(1) 2点 $2i$、$-4$ から等距離の点の集合なので垂直二等分線。式では $x^2+(y-2)^2=(x+4)^2+y^2$ より $-4y+4=8x+16$、$2x+y+3=0$。<br>(2) $|z-1|^2=4|z+2|^2$ より $(x-1)^2+y^2=4\{(x+2)^2+y^2\}$、$3x^2+18x+3y^2+15=0$、$(x+3)^2+y^2=4$。<br><b>ポイント</b>：$|z-\alpha|=|z-\beta|$ は垂直二等分線、$|z-\alpha|=k|z-\beta|\ (k\neq1)$ は円（アポロニウスの円）。2乗して $|w|^2=w\overline{w}$ または $x,y$ で計算する。"},
 {"lv": "A", "q": r"(1) 点 $\mathrm{A}(3+i)$ を原点のまわりに $90^\circ$ 回転した点を求めよ。(2) 点 A を点 $\mathrm{B}(1+2i)$ のまわりに $60^\circ$ 回転した点を求めよ。",
  "a": r"(1) $-1+3i$　(2) $\left(2+\frac{\sqrt3}{2}\right)+\left(\frac32+\sqrt3\right)i$",
  "s": r"(1) $i(3+i)=-1+3i$。<br>(2) 求める点を $w$ とすると $w-(1+2i)=\{(3+i)-(1+2i)\}(\cos60^\circ+i\sin60^\circ)=(2-i)\left(\frac12+\frac{\sqrt3}{2}i\right)$。<br>右辺 $=1+\sqrt3i-\frac12i+\frac{\sqrt3}{2}=\left(1+\frac{\sqrt3}{2}\right)+\left(\sqrt3-\frac12\right)i$。よって $w=\left(2+\frac{\sqrt3}{2}\right)+\left(\frac32+\sqrt3\right)i$。<br><b>ポイント</b>：点 $\beta$ のまわりの $\theta$ 回転は、$\beta$ を原点に移して回してから戻す：$w-\beta=(z-\beta)(\cos\theta+i\sin\theta)$。"},
 {"lv": "A", "q": r"方程式 $z^3=8i$ を解け。",
  "a": r"$z=\sqrt3+i,\ -\sqrt3+i,\ -2i$",
  "s": r"$z=r(\cos\theta+i\sin\theta)\ (r\gt0)$ とおくと $z^3=r^3(\cos3\theta+i\sin3\theta)$、$8i=8(\cos90^\circ+i\sin90^\circ)$。<br>$r^3=8$ より $r=2$。$3\theta=90^\circ+360^\circ k$ より $\theta=30^\circ+120^\circ k$。$0^\circ\leqq\theta\lt360^\circ$ で $\theta=30^\circ,150^\circ,270^\circ$。<br>$z=2(\cos30^\circ+i\sin30^\circ)=\sqrt3+i$、$2(\cos150^\circ+i\sin150^\circ)=-\sqrt3+i$、$2(\cos270^\circ+i\sin270^\circ)=-2i$。<br><b>ポイント</b>：$n$ 乗根は、絶対値と偏角を別々に比べ、偏角に $360^\circ k$ をつけて $n$ 個とる。解は原点中心の正 $n$ 角形の頂点。"},
 {"lv": "B", "tag": "典型", "q": r"$z$ は $0$ でない複素数とする。$z+\dfrac1z$ が実数となるような点 $z$ 全体の図形を求めよ。",
  "a": r"実軸（原点を除く）と、原点を中心とする半径1の円",
  "s": r"$z+\frac1z$ が実数 ⇔ $z+\frac1z=\overline{z}+\frac{1}{\overline{z}}$。<br>変形すると $(z-\overline z)+\frac{\overline z-z}{z\overline z}=0$、すなわち $(z-\overline z)\left(1-\frac{1}{|z|^2}\right)=0$。<br>よって $z=\overline z$（$z$ は実数）または $|z|=1$。$z\neq0$ なので、求める図形は「原点を除く実軸」と「単位円 $|z|=1$」を合わせたもの。<br><b>ポイント</b>：$w$ が実数 ⇔ $\overline w=w$、純虚数 ⇔ $\overline w=-w$ かつ $w\neq0$。共役をとって式を整理し、因数分解する。"},
 {"lv": "B", "tag": "三角形の形状", "q": r"複素数平面上の3点 $\mathrm{O}(0),\ \mathrm{A}(\alpha),\ \mathrm{B}(\beta)$（$\alpha\neq0,\ \beta\neq0$）が $\alpha^2-2\alpha\beta+4\beta^2=0$ を満たすとき、$\triangle\mathrm{OAB}$ の3つの角の大きさを求めよ。",
  "a": r"$\angle\mathrm{O}=60^\circ,\ \angle\mathrm{B}=90^\circ,\ \angle\mathrm{A}=30^\circ$",
  "s": r"$\beta^2$ で割ると $\left(\frac\alpha\beta\right)^2-2\cdot\frac\alpha\beta+4=0$、$\frac\alpha\beta=1\pm\sqrt3i=2\{\cos(\pm60^\circ)+i\sin(\pm60^\circ)\}$。<br>よって $|\alpha|=2|\beta|$、すなわち $\mathrm{OA}=2\mathrm{OB}$、$\angle\mathrm{AOB}=60^\circ$。<br>$\mathrm{OB}=1,\ \mathrm{OA}=2$ とすると余弦定理で $\mathrm{AB}^2=1+4-2\cdot2\cdot1\cdot\frac12=3$。$\mathrm{OB}^2+\mathrm{AB}^2=1+3=4=\mathrm{OA}^2$ なので $\angle\mathrm{B}=90^\circ$、残りの $\angle\mathrm{A}=30^\circ$。<br><b>ポイント</b>：2つの複素数の比 $\frac\alpha\beta$ を求めると、絶対値が「長さの比」、偏角が「なす角」を表す。"},
 {"lv": "B", "tag": "回転", "q": r"2点 $\mathrm{A}(1+i),\ \mathrm{B}(3+2i)$ に対して、$\triangle\mathrm{ABC}$ が正三角形となるような点 C を表す複素数を求めよ。",
  "a": r"$\left(2-\frac{\sqrt3}{2}\right)+\left(\frac32+\sqrt3\right)i$、$\left(2+\frac{\sqrt3}{2}\right)+\left(\frac32-\sqrt3\right)i$",
  "s": r"C は B を A のまわりに $\pm60^\circ$ 回転した点。$\gamma-(1+i)=(2+i)\left(\frac12\pm\frac{\sqrt3}{2}i\right)$。<br>$+$：$(2+i)\left(\frac12+\frac{\sqrt3}{2}i\right)=\left(1-\frac{\sqrt3}{2}\right)+\left(\sqrt3+\frac12\right)i$ より $\gamma=\left(2-\frac{\sqrt3}{2}\right)+\left(\frac32+\sqrt3\right)i$。<br>$-$：$(2+i)\left(\frac12-\frac{\sqrt3}{2}i\right)=\left(1+\frac{\sqrt3}{2}\right)+\left(\frac12-\sqrt3\right)i$ より $\gamma=\left(2+\frac{\sqrt3}{2}\right)+\left(\frac32-\sqrt3\right)i$。<br><b>ポイント</b>：正三角形の第3の頂点は、回転の向きで2通りある。「$\triangle\mathrm{ABC}$ の向き」の指定がなければ両方答える。"},
 {"lv": "B", "tag": "変換と軌跡", "q": r"点 $z$ が直線 $\mathrm{Re}\,z=1$（実部が1の点全体）の上を動くとき、$w=\dfrac1z$ で表される点 $w$ はどのような図形を描くか。",
  "a": r"点 $\frac12$ を中心とする半径 $\frac12$ の円（ただし原点を除く）",
  "s": r"$z=\frac1w$（$w\neq0$）。$\mathrm{Re}\,z=1$ は $\frac{z+\overline z}{2}=1$ なので $\frac1w+\frac{1}{\overline w}=2$。両辺に $w\overline w$ をかけて $\overline w+w=2w\overline w$。<br>$w\overline w-\frac12w-\frac12\overline w=0$ より $\left(w-\frac12\right)\left(\overline w-\frac12\right)=\frac14$、すなわち $\left|w-\frac12\right|=\frac12$。<br>$w=0$ に対応する $z$ はないので、原点を除く。<br><b>ポイント</b>：$w=f(z)$ の軌跡は「$z$ を $w$ で表して、$z$ の条件に代入」。$w=\frac1z$ は原点を通らない直線を原点を通る円にうつす。除外点を確認すること。"},
 {"lv": "B", "tag": "ド・モアブル", "q": r"$\left(\dfrac{1+\sqrt3i}{1+i}\right)^n$ が実数となる最小の自然数 $n$ と、そのときの値を求めよ。",
  "a": r"$n=12$、値は $-64$",
  "s": r"$1+\sqrt3i=2(\cos60^\circ+i\sin60^\circ)$、$1+i=\sqrt2(\cos45^\circ+i\sin45^\circ)$ より $\frac{1+\sqrt3i}{1+i}=\sqrt2(\cos15^\circ+i\sin15^\circ)$。<br>$n$ 乗は $(\sqrt2)^n(\cos15n^\circ+i\sin15n^\circ)$。実数 ⇔ $\sin15n^\circ=0$ ⇔ $15n$ が $180$ の倍数 ⇔ $n$ が $12$ の倍数。最小は $n=12$ で、値は $(\sqrt2)^{12}\cos180^\circ=64\cdot(-1)=-64$。<br><b>ポイント</b>：商は「絶対値は割り、偏角は引く」。実数・純虚数の条件は偏角の条件に直す。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"$\alpha=\cos72^\circ+i\sin72^\circ$ とする。<br>(1) $\alpha^4+\alpha^3+\alpha^2+\alpha+1=0$ を示せ。<br>(2) $t=\alpha+\dfrac1\alpha$ とおくとき、$t^2+t-1=0$ を示せ。<br>(3) $\cos72^\circ$ の値を求めよ。",
  "a": r"(3) $\cos72^\circ=\frac{\sqrt5-1}{4}$",
  "s": r"(1) ド・モアブルの定理より $\alpha^5=\cos360^\circ+i\sin360^\circ=1$。$\alpha^5-1=(\alpha-1)(\alpha^4+\alpha^3+\alpha^2+\alpha+1)=0$ で、$\alpha\neq1$ なので示された。■<br>(2) (1) の両辺を $\alpha^2\ (\neq0)$ で割ると $\alpha^2+\alpha+1+\frac1\alpha+\frac{1}{\alpha^2}=0$。$\alpha^2+\frac{1}{\alpha^2}=t^2-2$ なので $t^2-2+t+1=0$、すなわち $t^2+t-1=0$。■<br>(3) $|\alpha|=1$ より $\frac1\alpha=\overline\alpha=\cos72^\circ-i\sin72^\circ$、$t=2\cos72^\circ$。$t^2+t-1=0$ より $t=\frac{-1\pm\sqrt5}{2}$。$\cos72^\circ\gt0$ なので $t=\frac{-1+\sqrt5}{2}$、$\cos72^\circ=\frac{\sqrt5-1}{4}$。<br><b>ポイント</b>：相反方程式（係数が左右対称）は $\alpha^2$ で割って $t=\alpha+\frac1\alpha$ とおくと次数が半分になる。$|\alpha|=1$ のとき $\alpha+\frac1\alpha=2\cos\theta$。"},
 {"lv": "C", "tag": "二次試験レベル", "q": r"複素数の列 $\{z_n\}$ を $z_1=0,\ z_{n+1}=\dfrac{1+i}{2}z_n+1$ で定める。<br>(1) $z_n$ を $n$ の式で表せ。<br>(2) 点 $z_n$ が直線 $y=x$（$z=x+yi$）上にあるような $n$ をすべて求めよ。<br>(3) $|z_n-(1+i)|\lt\dfrac{1}{100}$ となる最小の $n$ を求めよ。",
  "a": r"(1) $z_n=(1+i)-\dfrac{(1+i)^n}{2^{n-1}}$　(2) $n=4k+1$（$k=0,1,2,\cdots$）　(3) $n=16$",
  "s": r"(1) $\alpha=\frac{1+i}{2}\alpha+1$ を解くと $\alpha\cdot\frac{1-i}{2}=1$、$\alpha=\frac{2}{1-i}=1+i$。$z_{n+1}-\alpha=\frac{1+i}{2}(z_n-\alpha)$ より $z_n-\alpha=\left(\frac{1+i}{2}\right)^{n-1}(0-\alpha)=-\frac{(1+i)^n}{2^{n-1}}$。<br>(2) $\alpha=1+i$ は直線 $y=x$ 上にあるので、$z_n$ が $y=x$ 上 ⇔ $z_n-\alpha$ が $0$ または偏角 $45^\circ+180^\circ k$。$(1+i)^n$ の偏角は $45n^\circ$ で、$z_n-\alpha=-\frac{(1+i)^n}{2^{n-1}}$ の偏角は $45n^\circ+180^\circ$。$45n\equiv45\pmod{180}$ ⇔ $n\equiv1\pmod4$。よって $n=1,5,9,\cdots$（$n=4k+1$）。<br>(3) $|z_n-\alpha|=\frac{(\sqrt2)^n}{2^{n-1}}=2^{1-\frac n2}$。$2^{1-\frac n2}\lt\frac1{100}$ ⇔ $2^{\frac n2-1}\gt100$。$2^6=64\lt100\lt128=2^7$ なので $\frac n2-1\gt6.64\cdots$ が必要で、$n=15$ では $2^{6.5}=64\sqrt2\fallingdotseq90.5\lt100$、$n=16$ では $2^7=128\gt100$。よって $n=16$。<br><b>ポイント</b>：$z_{n+1}=\beta z_n+\gamma$ は不動点 $\alpha$ を中心とする「回転＋拡大縮小」のくり返し。点 $z_n$ は $1+i$ に向かって $45^\circ$ ずつ回りながら $\frac{1}{\sqrt2}$ 倍で近づく渦巻き。"},
]}}

def verify():
    z = 1+sqrt(3)*I; w = 1-I
    assert Abs(z) == 2 and arg(z) == pi/3 and Abs(w) == sqrt(2) and arg(w) == -pi/4
    assert simplify(expand(z*w) - 2*sqrt(2)*(cos(pi/12)+I*sin(pi/12))) == 0
    assert expand(z**6) == 64
    # A2
    x, y = symbols("x y", real=True)
    Z = x+I*y
    e1 = expand(Abs(Z-2*I)**2 - Abs(Z+4)**2)
    assert simplify(e1 - (-8*x-4*y-12)) == 0
    e2 = expand(Abs(Z-1)**2 - 4*Abs(Z+2)**2)
    assert simplify(e2 + 3*((x+3)**2+y**2-4)) == 0
    # A3
    assert expand(I*(3+I)) == -1+3*I
    w2 = expand(1+2*I + (2-I)*(Rational(1, 2)+sqrt(3)/2*I))
    assert simplify(w2 - ((2+sqrt(3)/2)+(Rational(3, 2)+sqrt(3))*I)) == 0
    # A4
    for r in [sqrt(3)+I, -sqrt(3)+I, -2*I]:
        assert expand(r**3) == 8*I
    # B1：数値確認
    for zz in [Rational(3, 2), -2, (3+4*I)/5, I]:
        assert simplify(im(zz+1/zz)) == 0
    for zz in [1+I, 2*I]:
        assert simplify(im(zz+1/zz)) != 0
    a_, b_ = symbols("a_ b_", real=True)
    q = a_+I*b_
    imv = simplify(im(expand(q+1/q)))
    assert simplify(imv - b_*(1-1/(a_**2+b_**2))) == 0
    # B2
    t = symbols("t")
    rr = solve(t**2-2*t+4, t)
    assert set(rr) == {1+sqrt(3)*I, 1-sqrt(3)*I}
    beta = Integer(1); alpha = 1+sqrt(3)*I
    assert expand(alpha**2-2*alpha*beta+4*beta**2) == 0
    OA, OB, AB = Abs(alpha), Abs(beta), Abs(alpha-beta)
    assert OA == 2 and OB == 1 and simplify(AB**2-3) == 0 and simplify(OB**2+AB**2-OA**2) == 0
    # B3
    A, B = 1+I, 3+2*I
    for sg in [1, -1]:
        C = expand(A+(B-A)*(Rational(1, 2)+sg*sqrt(3)/2*I))
        assert simplify(Abs(C-A)-Abs(B-A)) == 0 and simplify(Abs(C-B)-Abs(B-A)) == 0
    assert simplify(expand(A+(B-A)*(Rational(1, 2)+sqrt(3)/2*I)) - ((2-sqrt(3)/2)+(Rational(3, 2)+sqrt(3))*I)) == 0
    assert simplify(expand(A+(B-A)*(Rational(1, 2)-sqrt(3)/2*I)) - ((2+sqrt(3)/2)+(Rational(3, 2)-sqrt(3))*I)) == 0
    # B4
    for yy in [-3, -1, 0, Rational(1, 2), 2, 10]:
        ww = 1/(1+I*yy)
        assert simplify(Abs(ww-Rational(1, 2)) - Rational(1, 2)) == 0
    # B5
    q = (1+sqrt(3)*I)/(1+I)
    for n in range(1, 12):
        assert simplify(im(expand(q**n))) != 0
    assert simplify(expand(q**12)) == -64
    # C1
    al = cos(2*pi/5)+I*sin(2*pi/5)
    assert simplify(expand(al**4+al**3+al**2+al+1)) == 0
    tt = al+1/al
    assert simplify(expand(tt**2+tt-1)) == 0
    assert simplify(cos(2*pi/5) - (sqrt(5)-1)/4) == 0
    # C2
    zs = [Integer(0)]
    for _ in range(20):
        zs.append(expand((1+I)/2*zs[-1]+1))
    for n in range(1, 21):
        assert simplify(zs[n-1] - ((1+I) - (1+I)**n/2**(n-1))) == 0
        on_line = simplify(re(zs[n-1]) - im(zs[n-1])) == 0
        assert on_line == (n % 4 == 1), n
    dist = lambda n: 2**(1-Rational(n, 2))
    assert simplify(Abs(zs[15]-(1+I)) - dist(16)) == 0
    assert dist(16) < Rational(1, 100) < dist(15)
