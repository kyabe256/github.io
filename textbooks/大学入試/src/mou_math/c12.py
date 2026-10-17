"""第12章 三角関数（数学II）"""
import math
import random
from fractions import Fraction as Fr

SEC = []
VS = []          # 各節の検算関数


def _v(f):
    VS.append(f)
    return f


class _Fig:
    """数学座標 → SVG 座標の簡易作図。"""

    def __init__(self, w, h, xr, yr, pad=(16, 10, 12, 14)):
        self.w, self.h = w, h
        self.x0, self.x1 = xr
        self.y0, self.y1 = yr
        self.pl, self.pt, self.pr, self.pb = pad
        self.e = []

    def X(self, x):
        return self.pl + (x - self.x0) / (self.x1 - self.x0) * (self.w - self.pl - self.pr)

    def Y(self, y):
        return self.h - self.pb - (y - self.y0) / (self.y1 - self.y0) * (self.h - self.pt - self.pb)

    def line(self, a, b, c, d, sw=1.0, col="#333", dash=None):
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.e.append(f'<line x1="{self.X(a):.1f}" y1="{self.Y(b):.1f}" x2="{self.X(c):.1f}" y2="{self.Y(d):.1f}" '
                      f'stroke="{col}" stroke-width="{sw}"{ds}/>')

    def poly(self, pts, sw=1.4, col="#16367a", close=False, fill="none", dash=None):
        p = " ".join(f"{self.X(x):.1f},{self.Y(y):.1f}" for x, y in pts)
        tag = "polygon" if close else "polyline"
        ds = f' stroke-dasharray="{dash}"' if dash else ""
        self.e.append(f'<{tag} points="{p}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{ds}/>')

    def fn(self, f, a, b, n=240, **kw):
        self.poly([(a + (b - a) * k / n, f(a + (b - a) * k / n)) for k in range(n + 1)], **kw)

    def arc(self, cx, cy, r, t0, t1, n=90, **kw):
        self.poly([(cx + r * math.cos(t0 + (t1 - t0) * k / n), cy + r * math.sin(t0 + (t1 - t0) * k / n))
                   for k in range(n + 1)], **kw)

    def text(self, x, y, s, size=10, anchor="middle", dx=0, dy=0, it=False):
        st = ' font-style="italic"' if it else ""
        self.e.append(f'<text x="{self.X(x) + dx:.1f}" y="{self.Y(y) + dy:.1f}" font-size="{size}" '
                      f'text-anchor="{anchor}" fill="#222"{st}>{s}</text>')

    def dot(self, x, y, r=2.0, col="#222"):
        self.e.append(f'<circle cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}" fill="{col}"/>')

    def axes(self, xl="x", yl="y", o=True):
        X0, X1, Y0, Y1 = self.X(self.x0), self.X(self.x1), self.Y(self.y0), self.Y(self.y1)
        ox, oy = self.X(0), self.Y(0)
        self.e.append(f'<line x1="{X0:.1f}" y1="{oy:.1f}" x2="{X1:.1f}" y2="{oy:.1f}" stroke="#555" stroke-width="0.8"/>')
        self.e.append(f'<line x1="{ox:.1f}" y1="{Y0:.1f}" x2="{ox:.1f}" y2="{Y1:.1f}" stroke="#555" stroke-width="0.8"/>')
        self.e.append(f'<polygon points="{X1:.1f},{oy:.1f} {X1 - 5:.1f},{oy - 2.5:.1f} {X1 - 5:.1f},{oy + 2.5:.1f}" fill="#555"/>')
        self.e.append(f'<polygon points="{ox:.1f},{Y1:.1f} {ox - 2.5:.1f},{Y1 + 5:.1f} {ox + 2.5:.1f},{Y1 + 5:.1f}" fill="#555"/>')
        self.e.append(f'<text x="{X1 - 2:.1f}" y="{oy + 12:.1f}" font-size="11" font-style="italic" text-anchor="end">{xl}</text>')
        self.e.append(f'<text x="{ox + 5:.1f}" y="{Y1 + 9:.1f}" font-size="11" font-style="italic">{yl}</text>')
        if o:
            self.e.append(f'<text x="{ox - 3:.1f}" y="{oy + 11:.1f}" font-size="10" text-anchor="end">O</text>')

    def svg(self):
        return (f'<svg class="fig" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'xmlns="http://www.w3.org/2000/svg">' + "".join(self.e) + "</svg>")


# ---------------------------------------------------------------- 節1
SEC.append({"title": "一般角と弧度法",
"base": r"""・動径 OP が始線 OX となす角の1つを $\alpha$ とすると，OP の表す一般角は $\alpha+360^\circ\times n$（$n$ は整数）<br>
・弧度法：$180^\circ=\pi$（ラジアン），$1^\circ=\dfrac{\pi}{180}$，$1$ ラジアン $=\dfrac{180^\circ}{\pi}$。一般角は $\alpha+2n\pi$ と表す<br>
・半径 $r$，中心角 $\theta$（弧度法）の扇形：弧の長さ $l=r\theta$，面積 $S=\dfrac12r^2\theta=\dfrac12rl$""",
"items": [
 {"lv": 1, "title": "一般角と動径・象限",
  "q": r"次の角の動径を $\alpha+360^\circ\times n$（$0^\circ\leqq\alpha<360^\circ$，$n$ は整数）の形で表し，第何象限の角かを答えよ。<br>(1) $840^\circ$　　(2) $-1000^\circ$　　(3) $1530^\circ$",
  "hint": r"$360^\circ$ 回転しても動径は変わらない。$360^\circ$ の整数倍を引いたり足したりして，$0^\circ$ 以上 $360^\circ$ 未満の角 $\alpha$ を見つける。負の角は $360^\circ$ の倍数を足して正にする。",
  "sol": r"(1) $840^\circ=120^\circ+360^\circ\times2$ より　$\boldsymbol{120^\circ+360^\circ\times2}$，<b>第2象限</b>の角<br>"
         r"(2) $-1000^\circ=80^\circ+360^\circ\times(-3)$ より　$\boldsymbol{80^\circ+360^\circ\times(-3)}$，<b>第1象限</b>の角<br>"
         r"(3) $1530^\circ=90^\circ+360^\circ\times4$ より　$\boldsymbol{90^\circ+360^\circ\times4}$。動径は $y$ 軸の正の部分に重なるので，<b>どの象限の角でもない</b>",
  "note": r"$-1000^\circ=-280^\circ+360^\circ\times(-2)$ と表しても同じ動径だが，$\alpha$ の範囲の指定に合わせて答える。動径が座標軸に重なる角（$90^\circ$ の整数倍）はどの象限にも属さない。",
  "ex": r"次の角の動径を同様の形で表し，第何象限の角かを答えよ。<br>(1) $1290^\circ$　　(2) $-640^\circ$",
  "exa": r"(1) $210^\circ+360^\circ\times3$，第3象限　(2) $80^\circ+360^\circ\times(-2)$，第1象限"},
 {"lv": 1, "title": "弧度法と扇形の弧の長さ・面積",
  "q": r"(1) $135^\circ$，$-210^\circ$ を弧度法で表せ。また，$\dfrac{7}{12}\pi$ を度数法で表せ。<br>(2) 半径 $4$，中心角 $\dfrac34\pi$ の扇形の弧の長さ $l$ と面積 $S$ を求めよ。",
  "hint": r"$180^\circ=\pi$ を比例で使う。扇形は，半径 $r$，中心角 $\theta$（弧度法）のとき $l=r\theta$，$S=\dfrac12r^2\theta$。",
  "sol": r"(1) $1^\circ=\dfrac{\pi}{180}$ より　$135^\circ=\dfrac{135}{180}\pi=\boldsymbol{\dfrac34\pi}$，$-210^\circ=-\dfrac{210}{180}\pi=\boldsymbol{-\dfrac76\pi}$<br>"
         r"また　$\dfrac{7}{12}\pi=\dfrac{7}{12}\times180^\circ=\boldsymbol{105^\circ}$<br>"
         r"(2) $l=4\cdot\dfrac34\pi=\boldsymbol{3\pi}$，$S=\dfrac12\cdot4^2\cdot\dfrac34\pi=\boldsymbol{6\pi}$",
  "note": r"$S=\dfrac12rl=\dfrac12\cdot4\cdot3\pi$ としてもよい。弧度法では「半径 $1$ の円の弧の長さ」が角の大きさなので，弧の長さや面積の公式が $\pi$ を含まない簡単な形になる。",
  "ex": r"(1) $150^\circ$ を弧度法で，$\dfrac85\pi$ を度数法で表せ。<br>(2) 半径 $6$，中心角 $\dfrac56\pi$ の扇形の弧の長さと面積を求めよ。",
  "exa": r"(1) $\dfrac56\pi$，$288^\circ$　(2) 弧の長さ $5\pi$，面積 $15\pi$"},
 {"lv": 2, "title": "周の長さが一定の扇形の面積の最大",
  "q": r"周の長さが $16$ である扇形のうち，面積が最大となるものの半径と中心角，およびそのときの面積を求めよ。",
  "hint": r"半径 $r$，中心角 $\theta$ とすると周の長さは $2r+r\theta$。$r\theta$ を消去して面積を $r$ の2次関数で表す。$0<\theta<2\pi$ から決まる $r$ の変域にも注意する。",
  "sol": r"半径を $r$，中心角を $\theta$（$0<\theta<2\pi$）とすると，$2r+r\theta=16$ より $r\theta=16-2r$。<br>"
         r"$r\theta>0$ より $r<8$。また $r\theta<2\pi r$ より $16-2r<2\pi r$，すなわち $r>\dfrac{8}{1+\pi}$。<br>"
         r"面積は　$S=\dfrac12r\cdot r\theta=\dfrac12r(16-2r)=-r^2+8r=-(r-4)^2+16$<br>"
         r"$r=4$ は $\dfrac{8}{1+\pi}<4<8$ を満たすから，$S$ は $r=4$ で最大となる。このとき $\theta=\dfrac{16-8}{4}=2$。<br>"
         r"よって　<b>半径 $\boldsymbol{4}$，中心角 $\boldsymbol{2}$（ラジアン）のとき，面積の最大値 $\boldsymbol{16}$</b>",
  "note": r"弧の長さ $l=r\theta$ を使うと $2r+l=16$，$S=\dfrac12rl=\dfrac14\cdot2r\cdot l$。相加平均と相乗平均の関係から $2r\cdot l\leqq\left(\dfrac{2r+l}{2}\right)^2=64$ なので $S\leqq16$（等号は $2r=l=8$）。周の長さが $L$ でも $r=\dfrac{L}{4}$ のとき最大で，中心角はいつも $2$ ラジアンになる。",
  "ex": r"周の長さが $12$ の扇形の面積の最大値と，そのときの半径・中心角を求めよ。",
  "exa": r"半径 $3$，中心角 $2$ のとき最大値 $9$"},
 {"lv": 2, "title": r"$\dfrac{\theta}{2}$，$\dfrac{\theta}{3}$ の動径の存在範囲",
  "q": r"$\theta$ が第2象限の角であるとき，$\dfrac{\theta}{2}$，$\dfrac{\theta}{3}$ はそれぞれ第何象限の角か。",
  "hint": r"「第2象限の角」を一般角で $\dfrac{\pi}{2}+2n\pi<\theta<\pi+2n\pi$（$n$ は整数）と表す。$3$ で割ると $\dfrac{2n\pi}{3}$ の項が出るので，$n$ を $3$ で割った余りで分類する。",
  "sol": r"$\dfrac{\pi}{2}+2n\pi<\theta<\pi+2n\pi$（$n$ は整数）と表せる。<br>"
         r"(i) $\dfrac{\pi}{4}+n\pi<\dfrac{\theta}{2}<\dfrac{\pi}{2}+n\pi$。$n$ が偶数のとき第1象限，奇数のとき第3象限の角。<br>"
         r"よって $\dfrac{\theta}{2}$ は　<b>第1象限または第3象限</b>の角<br>"
         r"(ii) $\dfrac{\pi}{6}+\dfrac{2n\pi}{3}<\dfrac{\theta}{3}<\dfrac{\pi}{3}+\dfrac{2n\pi}{3}$。$k$ を整数として<br>"
         r"$n=3k$ のとき　$\dfrac{\pi}{6}+2k\pi<\dfrac{\theta}{3}<\dfrac{\pi}{3}+2k\pi$（第1象限）<br>"
         r"$n=3k+1$ のとき　$\dfrac56\pi+2k\pi<\dfrac{\theta}{3}<\pi+2k\pi$（第2象限）<br>"
         r"$n=3k+2$ のとき　$\dfrac32\pi+2k\pi<\dfrac{\theta}{3}<\dfrac53\pi+2k\pi$（第4象限）<br>"
         r"よって $\dfrac{\theta}{3}$ は　<b>第1象限，第2象限，第4象限</b>のいずれかの角",
  "note": r"$\dfrac{\pi}{2}<\theta<\pi$ の範囲だけで考えて「$\dfrac{\pi}{6}<\dfrac{\theta}{3}<\dfrac{\pi}{3}$ だから第1象限」とするのは誤り。$\theta$ に $2\pi$ を加えても同じ象限の角だが，$\dfrac{\theta}{3}$ は $\dfrac23\pi$ ずれる。一般角で考えるのが要点。",
  "ex": r"$\theta$ が第3象限の角であるとき，$\dfrac{\theta}{2}$，$\dfrac{\theta}{3}$ はそれぞれ第何象限の角か。",
  "exa": r"$\dfrac{\theta}{2}$：第2象限または第4象限，$\dfrac{\theta}{3}$：第1，第3，第4象限のいずれか"},
]})


@_v
def _v1():
    assert (840 % 360, 840 // 360) == (120, 2)
    assert (-1000 % 360, -1000 // 360) == (80, -3)
    assert (1530 % 360, 1530 // 360) == (90, 4)
    assert (1290 % 360, 1290 // 360) == (210, 3) and (-640 % 360, -640 // 360) == (80, -2)
    assert Fr(135, 180) == Fr(3, 4) and Fr(-210, 180) == Fr(-7, 6) and Fr(7, 12) * 180 == 105
    assert Fr(150, 180) == Fr(5, 6) and Fr(8, 5) * 180 == 288
    assert 4 * Fr(3, 4) == 3 and Fr(1, 2) * 16 * Fr(3, 4) == 6          # ×π
    assert 6 * Fr(5, 6) == 5 and Fr(1, 2) * 36 * Fr(5, 6) == 15
    # 周の長さ一定の扇形
    for L, rr, S in [(16, 4, 16), (12, 3, 9)]:
        lo, hi = L / (2 + 2 * math.pi), L / 2
        best = max((r * (L - 2 * r) / 2, r) for r in [lo + (hi - lo) * k / 200000 for k in range(1, 200000)])
        assert abs(best[0] - S) < 1e-6 and abs(best[1] - rr) < 1e-3
        assert (L - 2 * rr) / rr == 2 and lo < rr < hi
    # θ/2, θ/3 の象限
    def quad(t):
        t = t % (2 * math.pi)
        return 1 + int(t // (math.pi / 2))
    rnd = random.Random(1)
    for lo, hi, a2, a3 in [(math.pi / 2, math.pi, {1, 3}, {1, 2, 4}), (math.pi, 1.5 * math.pi, {2, 4}, {1, 3, 4})]:
        s2, s3 = set(), set()
        for _ in range(20000):
            n = rnd.randint(-10, 10)
            th = rnd.uniform(lo + 1e-9, hi - 1e-9) + 2 * n * math.pi
            s2.add(quad(th / 2))
            s3.add(quad(th / 3))
        assert s2 == a2 and s3 == a3, (s2, s3)


# ---------------------------------------------------------------- 節2
SEC.append({"title": "三角関数の定義と相互関係",
"base": r"""・原点中心，半径 $1$ の円（単位円）と角 $\theta$ の動径の交点を $\mathrm{P}(x,\ y)$ とすると　$\sin\theta=y$，$\cos\theta=x$，$\tan\theta=\dfrac{y}{x}$<br>
・相互関係：$\sin^2\theta+\cos^2\theta=1$，$\tan\theta=\dfrac{\sin\theta}{\cos\theta}$，$1+\tan^2\theta=\dfrac{1}{\cos^2\theta}$<br>
・$\sin(-\theta)=-\sin\theta$，$\cos(-\theta)=\cos\theta$，$\sin(\pi-\theta)=\sin\theta$，$\cos(\pi-\theta)=-\cos\theta$，$\sin(\theta+\pi)=-\sin\theta$，$\cos(\theta+\pi)=-\cos\theta$，$\tan(\theta+\pi)=\tan\theta$<br>
・$\sin\left(\dfrac{\pi}{2}-\theta\right)=\cos\theta$，$\cos\left(\dfrac{\pi}{2}-\theta\right)=\sin\theta$，$\sin\left(\theta+\dfrac{\pi}{2}\right)=\cos\theta$，$\cos\left(\theta+\dfrac{\pi}{2}\right)=-\sin\theta$""",
"items": [
 {"lv": 1, "title": "三角関数の値と式の簡単化",
  "q": r"(1) 次の値を求めよ。　$\sin\dfrac76\pi$，$\cos\left(-\dfrac34\pi\right)$，$\tan\dfrac53\pi$，$\sin\dfrac{17}{4}\pi$<br>"
       r"(2) 次の式を簡単にせよ。　$\sin\left(\dfrac{\pi}{2}+\theta\right)\cos(\pi-\theta)+\sin(\pi+\theta)\cos\left(\dfrac{\pi}{2}-\theta\right)$",
  "hint": r"(1) 単位円周上で動径との交点の座標を読む。$2\pi$ の整数倍は除いてよい。(2) $\pi\pm\theta$，$\dfrac{\pi}{2}\pm\theta$ の公式で $\sin\theta,\ \cos\theta$ だけの式に直す。",
  "sol": r"(1) $\dfrac76\pi$ の動径と単位円の交点は $\left(-\dfrac{\sqrt3}{2},\ -\dfrac12\right)$ なので　$\sin\dfrac76\pi=\boldsymbol{-\dfrac12}$<br>"
         r"$-\dfrac34\pi$ の交点は $\left(-\dfrac{1}{\sqrt2},\ -\dfrac{1}{\sqrt2}\right)$ なので　$\cos\left(-\dfrac34\pi\right)=\boldsymbol{-\dfrac{\sqrt2}{2}}$<br>"
         r"$\dfrac53\pi$ の交点は $\left(\dfrac12,\ -\dfrac{\sqrt3}{2}\right)$ なので　$\tan\dfrac53\pi=\dfrac{-\frac{\sqrt3}{2}}{\frac12}=\boldsymbol{-\sqrt3}$<br>"
         r"$\sin\dfrac{17}{4}\pi=\sin\left(\dfrac{\pi}{4}+2\pi\times2\right)=\sin\dfrac{\pi}{4}=\boldsymbol{\dfrac{\sqrt2}{2}}$<br>"
         r"(2) $\sin\left(\dfrac{\pi}{2}+\theta\right)=\cos\theta$，$\cos(\pi-\theta)=-\cos\theta$，$\sin(\pi+\theta)=-\sin\theta$，$\cos\left(\dfrac{\pi}{2}-\theta\right)=\sin\theta$ より<br>"
         r"与式 $=\cos\theta\cdot(-\cos\theta)+(-\sin\theta)\cdot\sin\theta=-(\cos^2\theta+\sin^2\theta)=\boldsymbol{-1}$",
  "note": r"公式を丸暗記するより，単位円で $\theta$ と $\pi-\theta$，$\pi+\theta$，$\dfrac{\pi}{2}-\theta$ の動径の位置関係（対称・回転）を図で確認できるようにしておくと間違えない。",
  "ex": r"(1) $\cos\dfrac{11}{6}\pi$，$\sin\left(-\dfrac23\pi\right)$，$\tan\dfrac{13}{4}\pi$ の値を求めよ。<br>(2) $\sin(\pi-\theta)\cos\left(\dfrac{\pi}{2}-\theta\right)+\sin\left(\dfrac{\pi}{2}+\theta\right)\cos(-\theta)$ を簡単にせよ。",
  "exa": r"(1) $\dfrac{\sqrt3}{2}$，$-\dfrac{\sqrt3}{2}$，$1$　(2) $1$"},
 {"lv": 1, "title": "相互関係による値の決定",
  "q": r"(1) $\pi<\theta<\dfrac32\pi$，$\cos\theta=-\dfrac23$ のとき，$\sin\theta$，$\tan\theta$ の値を求めよ。<br>"
       r"(2) $\dfrac{\pi}{2}<\theta<\pi$，$\tan\theta=-2$ のとき，$\cos\theta$，$\sin\theta$ の値を求めよ。",
  "hint": r"$\sin^2\theta+\cos^2\theta=1$，$1+\tan^2\theta=\dfrac{1}{\cos^2\theta}$ で2乗の値が出る。符号は $\theta$ の象限で決める。",
  "sol": r"(1) $\sin^2\theta=1-\cos^2\theta=1-\dfrac49=\dfrac59$。$\pi<\theta<\dfrac32\pi$ より $\sin\theta<0$ なので　$\sin\theta=\boldsymbol{-\dfrac{\sqrt5}{3}}$<br>"
         r"$\tan\theta=\dfrac{\sin\theta}{\cos\theta}=\left(-\dfrac{\sqrt5}{3}\right)\div\left(-\dfrac23\right)=\boldsymbol{\dfrac{\sqrt5}{2}}$<br>"
         r"(2) $\dfrac{1}{\cos^2\theta}=1+\tan^2\theta=5$ より $\cos^2\theta=\dfrac15$。$\dfrac{\pi}{2}<\theta<\pi$ より $\cos\theta<0$ なので　$\cos\theta=\boldsymbol{-\dfrac{\sqrt5}{5}}$<br>"
         r"$\sin\theta=\tan\theta\cos\theta=(-2)\cdot\left(-\dfrac{\sqrt5}{5}\right)=\boldsymbol{\dfrac{2\sqrt5}{5}}$",
  "note": r"$\tan\theta$ の値だけから $\dfrac{\sin\theta+2\cos\theta}{\sin\theta-\cos\theta}$ のような式の値を求めるときは，分母・分子を $\cos\theta$ で割って $\tan\theta$ の式に直せばよい（例えば $\tan\theta=3$ なら $\dfrac{3+2}{3-1}=\dfrac52$）。",
  "ex": r"(1) $\dfrac32\pi<\theta<2\pi$，$\sin\theta=-\dfrac13$ のとき，$\cos\theta$，$\tan\theta$ の値を求めよ。<br>(2) $\pi<\theta<\dfrac32\pi$，$\tan\theta=3$ のとき，$\cos\theta$，$\sin\theta$ の値を求めよ。",
  "exa": r"(1) $\cos\theta=\dfrac{2\sqrt2}{3}$，$\tan\theta=-\dfrac{\sqrt2}{4}$　(2) $\cos\theta=-\dfrac{\sqrt{10}}{10}$，$\sin\theta=-\dfrac{3\sqrt{10}}{10}$"},
 {"lv": 2, "title": r"$\sin\theta+\cos\theta$ の値から式の値を求める",
  "q": r"$\sin\theta+\cos\theta=\dfrac12$（$0<\theta<\pi$）のとき，次の値を求めよ。<br>(1) $\sin\theta\cos\theta$　　(2) $\sin^3\theta+\cos^3\theta$　　(3) $\sin\theta-\cos\theta$　　(4) $\tan\theta+\dfrac{1}{\tan\theta}$",
  "hint": r"$\sin\theta,\ \cos\theta$ の対称式は，和 $\sin\theta+\cos\theta$ と積 $\sin\theta\cos\theta$ で表せる。積は和を2乗して $\sin^2\theta+\cos^2\theta=1$ を使う。(3) は2乗してから符号を決める。",
  "sol": r"(1) 両辺を2乗して $1+2\sin\theta\cos\theta=\dfrac14$。よって　$\sin\theta\cos\theta=\boldsymbol{-\dfrac38}$<br>"
         r"(2) $\sin^3\theta+\cos^3\theta=(\sin\theta+\cos\theta)(\sin^2\theta-\sin\theta\cos\theta+\cos^2\theta)=\dfrac12\left(1+\dfrac38\right)=\boldsymbol{\dfrac{11}{16}}$<br>"
         r"(3) $(\sin\theta-\cos\theta)^2=1-2\sin\theta\cos\theta=1+\dfrac34=\dfrac74$。<br>"
         r"$0<\theta<\pi$ より $\sin\theta>0$，さらに $\sin\theta\cos\theta<0$ より $\cos\theta<0$。よって $\sin\theta-\cos\theta>0$ で　$\sin\theta-\cos\theta=\boldsymbol{\dfrac{\sqrt7}{2}}$<br>"
         r"(4) $\tan\theta+\dfrac{1}{\tan\theta}=\dfrac{\sin\theta}{\cos\theta}+\dfrac{\cos\theta}{\sin\theta}=\dfrac{\sin^2\theta+\cos^2\theta}{\sin\theta\cos\theta}=\dfrac{1}{\sin\theta\cos\theta}=\boldsymbol{-\dfrac83}$",
  "note": r"(3) の符号の決定が要点。$\sin\theta,\ \cos\theta$ の符号は，$\sin\theta\cos\theta$ の符号と $\theta$ の範囲から決める。(1)(3) と和の条件から $\sin\theta=\dfrac{1+\sqrt7}{4}$，$\cos\theta=\dfrac{1-\sqrt7}{4}$ も求まる。",
  "ex": r"$\sin\theta-\cos\theta=\dfrac13$（$0<\theta<\pi$）のとき，$\sin\theta\cos\theta$，$\sin\theta+\cos\theta$，$\sin^3\theta-\cos^3\theta$ の値を求めよ。",
  "exa": r"$\sin\theta\cos\theta=\dfrac49$，$\sin\theta+\cos\theta=\dfrac{\sqrt{17}}{3}$，$\sin^3\theta-\cos^3\theta=\dfrac{13}{27}$"},
 {"lv": 3, "title": r"$\sin\theta,\ \cos\theta$ を解とする2次方程式",
  "q": r"$x$ の2次方程式 $5x^2-x+a=0$ の2つの解が $\sin\theta$，$\cos\theta$ であるとき，定数 $a$ の値と $\tan\theta$ の値を求めよ。",
  "hint": r"解と係数の関係で $\sin\theta+\cos\theta$ と $\sin\theta\cos\theta$ が分かる。この2つは $(\sin\theta+\cos\theta)^2=1+2\sin\theta\cos\theta$ で結ばれているので，これが $a$ を決める条件になる。",
  "sol": r"解と係数の関係より　$\sin\theta+\cos\theta=\dfrac15$ …①，$\sin\theta\cos\theta=\dfrac{a}{5}$ …②<br>"
         r"①の両辺を2乗すると $1+2\sin\theta\cos\theta=\dfrac{1}{25}$ より $\sin\theta\cos\theta=-\dfrac{12}{25}$。②より　$a=\boldsymbol{-\dfrac{12}{5}}$<br>"
         r"このとき方程式は $5x^2-x-\dfrac{12}{5}=0$，すなわち $25x^2-5x-12=0$，$(5x+3)(5x-4)=0$ で，解は $x=\dfrac45,\ -\dfrac35$。<br>"
         r"$\left(\dfrac45\right)^2+\left(-\dfrac35\right)^2=1$ なので，$(\sin\theta,\ \cos\theta)=\left(\dfrac45,\ -\dfrac35\right)$，$\left(-\dfrac35,\ \dfrac45\right)$ となる $\theta$ は確かに存在する。<br>"
         r"よって　$\tan\theta=\boldsymbol{-\dfrac43,\ -\dfrac34}$",
  "note": r"「$\sin\theta,\ \cos\theta$ が解」という条件は，$\sin^2\theta+\cos^2\theta=1$ を通して係数に制約を与える。$a$ を求めた後，実際に解が $\sin\theta,\ \cos\theta$ になれるか（2解の2乗の和が $1$ か）を確かめておくと安心。",
  "ex": r"$x$ の2次方程式 $2x^2-(\sqrt3+1)x+a=0$ の2つの解が $\sin\theta$，$\cos\theta$（$0\leqq\theta<2\pi$）であるとき，定数 $a$ の値と $\theta$ の値を求めよ。",
  "exa": r"$a=\dfrac{\sqrt3}{2}$，$\theta=\dfrac{\pi}{6},\ \dfrac{\pi}{3}$"},
]})


def _eq(a, b):
    import sympy as sp
    a, b = sp.sympify(a), sp.sympify(b)
    if sp.simplify(a - b) == 0:
        return
    assert abs(sp.N(a - b, 60)) < 1e-45, (a, b)


@_v
def _v2():
    import sympy as sp
    from sympy import sin, cos, tan, pi, sqrt, Rational as R, symbols
    t = symbols("t", real=True)
    _eq(sin(7 * pi / 6), -R(1, 2)); _eq(cos(-3 * pi / 4), -sqrt(2) / 2)
    _eq(tan(5 * pi / 3), -sqrt(3)); _eq(sin(17 * pi / 4), sqrt(2) / 2)
    _eq(cos(11 * pi / 6), sqrt(3) / 2); _eq(sin(-2 * pi / 3), -sqrt(3) / 2); _eq(tan(13 * pi / 4), 1)
    assert sp.simplify(sin(pi / 2 + t) * cos(pi - t) + sin(pi + t) * cos(pi / 2 - t) + 1) == 0
    assert sp.simplify(sin(pi - t) * cos(pi / 2 - t) + sin(pi / 2 + t) * cos(-t) - 1) == 0
    # 相互関係（数値で θ を作って確認）
    th = math.pi + math.acos(2 / 3)                     # π<θ<3π/2, cos=-2/3
    assert abs(math.cos(th) + 2 / 3) < 1e-12 and math.pi < th < 1.5 * math.pi
    assert abs(math.sin(th) + math.sqrt(5) / 3) < 1e-12 and abs(math.tan(th) - math.sqrt(5) / 2) < 1e-12
    th = math.pi - math.atan(2)                          # π/2<θ<π, tan=-2
    assert abs(math.tan(th) + 2) < 1e-12 and abs(math.cos(th) + math.sqrt(5) / 5) < 1e-12 and abs(math.sin(th) - 2 * math.sqrt(5) / 5) < 1e-12
    th = 2 * math.pi - math.asin(1 / 3)
    assert abs(math.cos(th) - 2 * math.sqrt(2) / 3) < 1e-12 and abs(math.tan(th) + math.sqrt(2) / 4) < 1e-12
    th = math.pi + math.atan(3)
    assert abs(math.cos(th) + math.sqrt(10) / 10) < 1e-12 and abs(math.sin(th) + 3 * math.sqrt(10) / 10) < 1e-12
    assert Fr(3 + 2, 3 - 1) == Fr(5, 2)
    # sinθ+cosθ=1/2 (0<θ<π)：θ を解いて確認
    th = math.pi - math.asin(0.5 / math.sqrt(2)) - math.pi / 4      # √2 sin(θ+π/4)=1/2，θ∈(0,π)
    assert 0 < th < math.pi and abs(math.sin(th) + math.cos(th) - 0.5) < 1e-12
    s, c = math.sin(th), math.cos(th)
    assert abs(s * c + 3 / 8) < 1e-12 and abs(s**3 + c**3 - 11 / 16) < 1e-12
    assert abs(s - c - math.sqrt(7) / 2) < 1e-12 and abs(s / c + c / s + 8 / 3) < 1e-12
    assert abs(s - (1 + math.sqrt(7)) / 4) < 1e-12 and abs(c - (1 - math.sqrt(7)) / 4) < 1e-12
    # 練習：sinθ-cosθ=1/3
    th = math.pi / 4 + math.asin(1 / (3 * math.sqrt(2)))
    s, c = math.sin(th), math.cos(th)
    assert 0 < th < math.pi and abs(s - c - 1 / 3) < 1e-12
    assert abs(s * c - 4 / 9) < 1e-12 and abs(s + c - math.sqrt(17) / 3) < 1e-12 and abs(s**3 - c**3 - 13 / 27) < 1e-12
    # 2次方程式
    x = symbols("x")
    a = -R(12, 5)
    assert R(1, 5)**2 == 1 + 2 * (a / 5)
    assert sp.expand((5 * x + 3) * (5 * x - 4)) == 25 * x**2 - 5 * x - 12
    assert set(sp.solve(5 * x**2 - x + a, x)) == {R(4, 5), -R(3, 5)}
    assert R(4, 5)**2 + R(3, 5)**2 == 1
    a2 = sqrt(3) / 2
    rts = sp.solve(2 * x**2 - (sqrt(3) + 1) * x + a2, x)
    assert {sp.nsimplify(r) for r in rts} == {R(1, 2), sqrt(3) / 2}
    _eq(((sqrt(3) + 1) / 2)**2, 1 + 2 * (a2 / 2))
    for tt in (math.pi / 6, math.pi / 3):
        assert abs(2 * math.sin(tt)**2 - (math.sqrt(3) + 1) * math.sin(tt) + math.sqrt(3) / 2) < 1e-12
        assert abs(2 * math.cos(tt)**2 - (math.sqrt(3) + 1) * math.cos(tt) + math.sqrt(3) / 2) < 1e-12


# ---------------------------------------------------------------- 節3
def _fig31():
    P = math.pi
    f = _Fig(236, 140, (-0.25, 3.95), (-2.95, 2.75), pad=(14, 8, 10, 6))
    f.axes("θ", "y")
    f.line(0, 2, 5 * P / 12, 2, sw=0.7, col="#888", dash="3,2")
    f.line(5 * P / 12, 0, 5 * P / 12, 2, sw=0.7, col="#888", dash="3,2")
    f.line(0, -2, 11 * P / 12, -2, sw=0.7, col="#888", dash="3,2")
    f.line(11 * P / 12, 0, 11 * P / 12, -2, sw=0.7, col="#888", dash="3,2")
    f.fn(lambda t: 2 * math.sin(2 * t - P / 3), 0, 3.85)
    f.text(0, 2, "2", size=10, anchor="end", dx=-3, dy=4)
    f.text(0, -2, "−2", size=10, anchor="end", dx=-3, dy=4)
    f.text(P / 6, 0, "π/6", size=9, dx=7, dy=11)
    f.text(5 * P / 12, 0, "5π/12", size=9, dy=11)
    f.text(2 * P / 3, 0, "2π/3", size=9, dx=10, dy=-4)
    f.text(11 * P / 12, -2, "11π/12", size=9, dy=11)
    f.text(7 * P / 6, 0, "7π/6", size=9, dx=-10, dy=-4)
    return f.svg()


def _fig32():
    P = math.pi
    f = _Fig(220, 128, (-0.3, 3.9), (-3.7, 4.0), pad=(14, 8, 10, 8))
    f.axes("θ", "y")
    f.line(0, 3, 3 * P / 8, 3, sw=0.7, col="#888", dash="3,2")
    f.line(0, -3, 7 * P / 8, -3, sw=0.7, col="#888", dash="3,2")
    f.fn(lambda t: 3 * math.sin(2 * t - P / 4), 0, 3.8)
    f.text(0, 3, "3", size=10, anchor="end", dx=-3, dy=4)
    f.text(0, -3, "−3", size=10, anchor="end", dx=-3, dy=4)
    f.dot(P / 8, 0, r=1.6)
    f.dot(5 * P / 8, 0, r=1.6)
    f.text(P / 8, 0, "π/8", size=9, dx=8, dy=11)
    f.text(5 * P / 8, 0, "5π/8", size=9, dx=11, dy=-4)
    return f.svg()


SEC.append({"title": "三角関数のグラフ",
"base": r"""・$y=\sin\theta$，$y=\cos\theta$ は周期 $2\pi$，値域は $-1\leqq y\leqq1$。$y=\tan\theta$ は周期 $\pi$，漸近線は直線 $\theta=\dfrac{\pi}{2}+n\pi$（$n$ は整数）<br>
・$y=a\sin k(\theta-p)$（$a>0$，$k>0$）のグラフ：$y=\sin\theta$ のグラフを $\theta$ 軸方向に $\dfrac1k$ 倍，$y$ 軸方向に $a$ 倍し，$\theta$ 軸方向に $p$ だけ平行移動したもの。周期は $\dfrac{2\pi}{k}$<br>
・すべての $\theta$ で $f(\theta+p)=f(\theta)$ となる正の数 $p$ を周期といい，その最小のもの（基本周期）を単に周期ということが多い""",
"items": [
 {"lv": 1, "title": r"$y=a\sin(k\theta-b)$ のグラフと周期",
  "q": r"関数 $y=2\sin\left(2\theta-\dfrac{\pi}{3}\right)$ のグラフをかけ。また，その周期を求めよ。",
  "hint": r"$2\theta-\dfrac{\pi}{3}=2\left(\theta-\dfrac{\pi}{6}\right)$ と $\theta$ の係数をくくり出すと，平行移動の量 $\dfrac{\pi}{6}$ が分かる。周期は $2\pi$ を $\theta$ の係数 $2$ で割ったもの。",
  "sol": _fig31() +
         r"$y=2\sin2\left(\theta-\dfrac{\pi}{6}\right)$ と変形できる。<br>"
         r"これは，$y=\sin\theta$ のグラフを $\theta$ 軸方向に $\dfrac12$ 倍，$y$ 軸方向に $2$ 倍に拡大した $y=2\sin2\theta$ のグラフを，$\theta$ 軸方向に $\dfrac{\pi}{6}$ だけ平行移動したもの。<br>"
         r"周期は　$\dfrac{2\pi}{2}=\boldsymbol{\pi}$<br>"
         r"$\theta=\dfrac{\pi}{6}$ で $y=0$（増加），$\theta=\dfrac{5}{12}\pi$ で最大値 $2$，$\theta=\dfrac23\pi$ で $y=0$，$\theta=\dfrac{11}{12}\pi$ で最小値 $-2$，$\theta=\dfrac76\pi$ で $y=0$ となり，以後これをくり返す。$\theta=0$ のとき $y=2\sin\left(-\dfrac{\pi}{3}\right)=-\sqrt3$。グラフは右の図。",
  "note": r"$2\theta-\dfrac{\pi}{3}$ を見て「$\dfrac{\pi}{3}$ だけ平行移動」とするのはよくある誤り。必ず $\theta$ の係数をくくり出して $2\left(\theta-\dfrac{\pi}{6}\right)$ とする。かくときは，$2\theta-\dfrac{\pi}{3}=0,\ \dfrac{\pi}{2},\ \pi,\ \dfrac32\pi,\ 2\pi$ となる $\theta$ を求めて5点をとるとよい。",
  "ex": r"関数 $y=\cos\left(\dfrac{\theta}{2}+\dfrac{\pi}{4}\right)$ の周期を求めよ。また，このグラフは $y=\cos\dfrac{\theta}{2}$ のグラフをどのように平行移動したものか。",
  "exa": r"周期 $4\pi$，$\theta$ 軸方向に $-\dfrac{\pi}{2}$ だけ平行移動したもの"},
 {"lv": 2, "title": "グラフから式を決定する",
  "q": _fig32() +
       r"右の図は，関数 $y=a\sin(b\theta-c)$ のグラフの一部である。ただし，$a>0$，$b>0$，$0<c<\pi$ とする。<br>$a,\ b,\ c$ の値を求めよ。",
  "hint": r"最大値から $a$，$\theta$ 軸との隣り合う交点の間隔（半周期）から $b$，「$y=0$ で増加している点」から $c$ を決める。",
  "sol": r"最大値が $3$ なので　$a=3$<br>"
         r"$\theta$ 軸との隣り合う交点 $\theta=\dfrac{\pi}{8},\ \dfrac58\pi$ の間隔が半周期だから，周期は $2\left(\dfrac58\pi-\dfrac{\pi}{8}\right)=\pi$。$\dfrac{2\pi}{b}=\pi$ より　$b=2$<br>"
         r"$\theta=\dfrac{\pi}{8}$ で $y=0$ となり増加しているから，$\sin$ の中身について $2\cdot\dfrac{\pi}{8}-c=2n\pi$（$n$ は整数）。よって $c=\dfrac{\pi}{4}-2n\pi$。$0<c<\pi$ より $c=\dfrac{\pi}{4}$。<br>"
         r"以上より　$\boldsymbol{a=3,\ b=2,\ c=\dfrac{\pi}{4}}$",
  "note": r"$y=\sin u$ が $0$ で増加するのは $u=2n\pi$，$0$ で減少するのは $u=\pi+2n\pi$ のとき。$c$ の範囲の条件がなければ $c=\dfrac{\pi}{4}+2n\pi$ のどれでも同じグラフになるので，問題文の範囲の指定で1つに決める。",
  "ex": r"関数 $y=a\sin(b\theta-c)$（$a>0$，$b>0$，$0<c<\pi$）の最大値は $2$，周期は $4\pi$ で，そのグラフは $\theta=\dfrac{\pi}{3}$ で $\theta$ 軸と交わり，そこで増加している。$a,\ b,\ c$ の値を求めよ。",
  "exa": r"$a=2,\ b=\dfrac12,\ c=\dfrac{\pi}{6}$"},
 {"lv": 2, "title": "三角関数の値の大小比較",
  "q": r"$\sin1$，$\sin2$，$\sin3$，$\cos1$ を小さい順に並べよ。ただし，角の単位はラジアンとする。",
  "hint": r"すべてを $0$ から $\dfrac{\pi}{2}$ までの角の $\sin$ に直せば，その範囲で $\sin$ が増加することから比べられる。$3<\pi<4$ を使って角の大小を決める。",
  "sol": r"$\sin2=\sin(\pi-2)$，$\sin3=\sin(\pi-3)$，$\cos1=\sin\left(\dfrac{\pi}{2}-1\right)$ である。<br>"
         r"$3<\pi<4$ より　$0<\pi-3<\dfrac{\pi}{2}-1<1<\pi-2<\dfrac{\pi}{2}$<br>"
         r"（$\pi-3<\dfrac{\pi}{2}-1\iff\pi<4$，$\dfrac{\pi}{2}-1<1\iff\pi<4$，$1<\pi-2\iff\pi>3$，$\pi-2<\dfrac{\pi}{2}\iff\pi<4$）<br>"
         r"$0\leqq\theta\leqq\dfrac{\pi}{2}$ で $\sin\theta$ は増加するから　$\sin(\pi-3)<\sin\left(\dfrac{\pi}{2}-1\right)<\sin1<\sin(\pi-2)$<br>"
         r"よって　$\boldsymbol{\sin3<\cos1<\sin1<\sin2}$",
  "note": r"数値（$\pi\fallingdotseq3.14$）で $\pi-3\fallingdotseq0.14$，$\dfrac{\pi}{2}-1\fallingdotseq0.57$，$\pi-2\fallingdotseq1.14$ と見当をつけてから，不等式で裏づけるとよい。$\cos$ どうしなら $0\leqq\theta\leqq\pi$ で減少することを使う。",
  "ex": r"$\cos1$，$\cos2$，$\cos3$，$\cos4$ を小さい順に並べよ。",
  "exa": r"$\cos3<\cos4<\cos2<\cos1$"},
 {"lv": 3, "title": "和で表された関数の基本周期",
  "q": r"関数 $f(x)=\sin2x+\cos3x$ の正の周期のうち最小のもの（基本周期）を求めよ。",
  "hint": r"$\sin2x$ の周期 $\pi$ と $\cos3x$ の周期 $\dfrac23\pi$ の公倍数 $2\pi$ が周期になることはすぐ分かる。それより小さい周期がないことは，$f(x+p)=f(x)$ に特別な $x$ を代入して $p$ を絞り込んで示す。",
  "sol": r"$f(x+2\pi)=\sin(2x+4\pi)+\cos(3x+6\pi)=f(x)$ なので，$2\pi$ は周期である。<br>"
         r"逆に，正の数 $p$ がすべての $x$ で $f(x+p)=f(x)$ を満たすとする。<br>"
         r"$x=0$ とすると $f(p)=f(0)$ より　$\sin2p+\cos3p=1$ …①<br>"
         r"$x=-p$ とすると $f(0)=f(-p)$ より　$1=-\sin2p+\cos3p$ …②<br>"
         r"①＋② より $\cos3p=1$，①－② より $\sin2p=0$。<br>"
         r"よって，正の整数 $k,\ m$ を用いて $3p=2k\pi$，$2p=m\pi$ と表せる。$p=\dfrac{2k\pi}{3}=\dfrac{m\pi}{2}$ より $4k=3m$。$4$ と $3$ は互いに素だから $k$ は $3$ の倍数で，$p=\dfrac{2k\pi}{3}$ は $2\pi$ の正の倍数。<br>"
         r"したがって $p\geqq2\pi$ であり，基本周期は　$\boldsymbol{2\pi}$",
  "note": r"周期の公倍数は周期になるが，最小とは限らない。例えば $\sin x$ と $\cos2x-\sin x$ はどちらも基本周期 $2\pi$ だが，和の $\cos2x$ の基本周期は $\pi$ である。最小性は特別な値の代入で必ず確かめる。",
  "ex": r"関数 $f(x)=\cos2x+\sin3x$ の基本周期を求めよ。",
  "exa": r"$2\pi$（$x=0,\ -p$ の代入で $p$ は $\pi$ の倍数，さらに $x=\dfrac{\pi}{6}$ の代入で $2\pi$ の倍数に絞られる）"},
]})


@_v
def _v3():
    P = math.pi
    g = lambda t: 2 * math.sin(2 * t - P / 3)
    for t, y in [(P / 6, 0), (5 * P / 12, 2), (2 * P / 3, 0), (11 * P / 12, -2), (7 * P / 6, 0), (0, -math.sqrt(3))]:
        assert abs(g(t) - y) < 1e-12
    assert g(P / 6 + 1e-4) > 0 and all(abs(g(t + P) - g(t)) < 1e-12 for t in [0.1 * k for k in range(60)])
    # 練習：cos(θ/2+π/4) = cos((θ+π/2)/2)
    assert all(abs(math.cos(t / 2 + P / 4) - math.cos((t + P / 2) / 2)) < 1e-12 for t in [0.3 * k for k in range(40)])
    # 式の決定
    h = lambda t: 3 * math.sin(2 * t - P / 4)
    assert abs(h(P / 8)) < 1e-12 and abs(h(5 * P / 8)) < 1e-12 and h(P / 8 + 1e-4) > 0
    assert abs(max(h(k * P / 4000) for k in range(4001)) - 3) < 1e-6
    assert all(abs(h(t)) > 1e-6 for t in [P / 8 + 0.001 * k for k in range(1, 1570)])   # 間に零点なし
    h2 = lambda t: 2 * math.sin(t / 2 - P / 6)
    assert abs(h2(P / 3)) < 1e-12 and h2(P / 3 + 1e-4) > 0 and all(abs(h2(t + 4 * P) - h2(t)) < 1e-12 for t in range(10))
    # 大小比較
    v = sorted([(math.sin(1), "s1"), (math.sin(2), "s2"), (math.sin(3), "s3"), (math.cos(1), "c1")])
    assert [n for _, n in v] == ["s3", "c1", "s1", "s2"]
    v = sorted([(math.cos(k), k) for k in (1, 2, 3, 4)])
    assert [k for _, k in v] == [3, 4, 2, 1]
    # 基本周期：(0,2π) に周期がないこと、2π が周期であること
    xs = [0.013 * k for k in range(500)]
    for F in (lambda x: math.sin(2 * x) + math.cos(3 * x), lambda x: math.cos(2 * x) + math.sin(3 * x)):
        assert all(abs(F(x + 2 * P) - F(x)) < 1e-12 for x in xs)
        for k in range(1, 4000):
            p = 2 * P * k / 4000
            assert max(abs(F(x + p) - F(x)) for x in xs) > 1e-4, p
    # 練習の絞り込み：p=kπ のとき x=π/6 で f(π/6+kπ)=1/2+(-1)^k
    F = lambda x: math.cos(2 * x) + math.sin(3 * x)
    assert abs(F(P / 6 + P) - (0.5 - 1)) < 1e-12 and abs(F(P / 6) - 1.5) < 1e-12
    # 検討の例：sin x + (cos2x - sin x) = cos 2x
    assert all(abs(math.cos(2 * x) - math.sin(x) - math.cos(2 * (x + 2 * P)) + math.sin(x + 2 * P)) < 1e-12 for x in xs)


# ---------------------------------------------------------------- 節4
def _roots(g, lo, hi, N=60000):
    """[lo,hi) における g の零点（符号変化＋接する零点）を近似で列挙。"""
    xs = [lo + (hi - lo) * k / N for k in range(N + 1)]
    ys = [g(x) for x in xs]
    out = []
    for i in range(N):
        a, b, fa, fb = xs[i], xs[i + 1], ys[i], ys[i + 1]
        if fa == 0:
            out.append(a)
        elif fa * fb < 0:
            for _ in range(60):
                m = (a + b) / 2
                if fa * g(m) <= 0:
                    b = m
                else:
                    a, fa = m, g(m)
            out.append((a + b) / 2)
    for i in range(1, N):                         # 接する零点（極小値が 0）
        if abs(ys[i]) <= abs(ys[i - 1]) and abs(ys[i]) <= abs(ys[i + 1]) and abs(ys[i]) < 1e-6:
            if ys[i - 1] * ys[i + 1] > 0:
                out.append(xs[i])
    out = sorted(x for x in out if lo - 1e-12 <= x < hi - 1e-9)
    ded = []
    for x in out:
        if not ded or x - ded[-1] > 1e-5:
            ded.append(x)
    return ded


def _same_roots(g, sols, lo=0.0, hi=2 * math.pi, N=60000):
    r = _roots(g, lo, hi, N)
    assert len(r) == len(sols) and all(abs(a - b) < 1e-4 for a, b in zip(r, sorted(sols))), (r, sorted(sols))
    assert all(abs(g(s)) < 1e-9 for s in sols)


def _same_set(pred, ints, lo=0.0, hi=2 * math.pi, N=20000):
    """開区間の和 ints（端点は別に確認）と pred の真偽が格子点で一致するか。"""
    for k in range(N):
        t = lo + (hi - lo) * (k + 0.37) / N
        if any(min(abs(t - a), abs(t - b)) < 1e-7 for a, b in ints):
            continue
        assert pred(t) == any(a < t < b for a, b in ints), t


SEC.append({"title": "三角関数を含む方程式・不等式",
"base": r"""・$\sin\theta=k$ は単位円と直線 $y=k$，$\cos\theta=k$ は直線 $x=k$，$\tan\theta=k$ は原点と点 $(1,\ k)$ を通る直線との交点から $\theta$ を読む。不等式は単位円の上下・左右で考える<br>
・一般解（$n$ は整数）：$\sin\theta=\sin\alpha\iff\theta=\alpha+2n\pi$ または $\theta=\pi-\alpha+2n\pi$；$\cos\theta=\cos\alpha\iff\theta=\pm\alpha+2n\pi$；$\tan\theta=\tan\alpha\iff\theta=\alpha+n\pi$<br>
・$2\theta+\alpha$ などの角を含むときは，その角の変域を先に求めてから解く。$\sin\theta$，$\cos\theta$ の2次式は一方にそろえて置き換え（変域 $-1\leqq t\leqq1$ に注意）""",
"items": [
 {"lv": 1, "title": "三角関数を含む基本的な方程式と一般解",
  "q": r"$0\leqq\theta<2\pi$ のとき，次の方程式を解け。また，(1) については一般解も求めよ。<br>(1) $2\sin\theta+\sqrt3=0$　　(2) $\sqrt3\tan\theta=1$　　(3) $2\cos\theta=\sqrt2$",
  "hint": r"$\sin\theta=k$ なら単位円と直線 $y=k$ の交点，$\cos\theta=k$ なら直線 $x=k$ との交点，$\tan\theta=k$ なら原点と点 $(1,\ k)$ を結ぶ直線との交点を考える。",
  "sol": r"(1) $\sin\theta=-\dfrac{\sqrt3}{2}$。単位円と直線 $y=-\dfrac{\sqrt3}{2}$ の交点を考えて　$\boldsymbol{\theta=\dfrac43\pi,\ \dfrac53\pi}$<br>"
         r"一般解は，$n$ を整数として　$\boldsymbol{\theta=\dfrac43\pi+2n\pi,\ \dfrac53\pi+2n\pi}$<br>"
         r"(2) $\tan\theta=\dfrac{1}{\sqrt3}$ より　$\boldsymbol{\theta=\dfrac{\pi}{6},\ \dfrac76\pi}$<br>"
         r"(3) $\cos\theta=\dfrac{\sqrt2}{2}$ より　$\boldsymbol{\theta=\dfrac{\pi}{4},\ \dfrac74\pi}$",
  "note": r"一般解は，$0\leqq\theta<2\pi$ の解に $2n\pi$ を加えたもの。$\tan$ は周期が $\pi$ なので，(2) の一般解は $\theta=\dfrac{\pi}{6}+n\pi$ と1つにまとまる。",
  "ex": r"$0\leqq\theta<2\pi$ のとき，次の方程式を解け。<br>(1) $2\cos\theta+\sqrt2=0$　　(2) $\tan\theta=-\sqrt3$",
  "exa": r"(1) $\theta=\dfrac34\pi,\ \dfrac54\pi$　(2) $\theta=\dfrac23\pi,\ \dfrac53\pi$"},
 {"lv": 1, "title": "三角関数を含む基本的な不等式",
  "q": r"$0\leqq\theta<2\pi$ のとき，次の不等式を解け。<br>(1) $2\cos\theta\leqq-1$　　(2) $\sqrt2\sin\theta>1$　　(3) $\tan\theta>1$",
  "hint": r"まず等号が成り立つ $\theta$ を求め，単位円周上で条件を満たす部分（$x$ 座標や $y$ 座標が大きい・小さい部分）を読み取る。$\tan\theta$ は定義されない角を除く。",
  "sol": r"(1) $\cos\theta\leqq-\dfrac12$。単位円周上で $x$ 座標が $-\dfrac12$ 以下の部分を考えて　$\boldsymbol{\dfrac23\pi\leqq\theta\leqq\dfrac43\pi}$<br>"
         r"(2) $\sin\theta>\dfrac{1}{\sqrt2}$。$y$ 座標が $\dfrac{1}{\sqrt2}$ より大きい部分を考えて　$\boldsymbol{\dfrac{\pi}{4}<\theta<\dfrac34\pi}$<br>"
         r"(3) $\theta\neq\dfrac{\pi}{2},\ \dfrac32\pi$ で考える。$\tan\theta=1$ となるのは $\theta=\dfrac{\pi}{4},\ \dfrac54\pi$。$\tan\theta$ は $0\leqq\theta<\dfrac{\pi}{2}$，$\dfrac{\pi}{2}<\theta<\dfrac32\pi$，$\dfrac32\pi<\theta<2\pi$ のそれぞれで増加するから<br>"
         r"$\boldsymbol{\dfrac{\pi}{4}<\theta<\dfrac{\pi}{2},\ \dfrac54\pi<\theta<\dfrac32\pi}$",
  "note": r"(3) は $y=\tan\theta$ のグラフと直線 $y=1$ の上下関係で考えてもよい。$\tan\theta$ の不等式では，$\theta=\dfrac{\pi}{2}+n\pi$ を除くことを忘れない。",
  "ex": r"$0\leqq\theta<2\pi$ のとき，次の不等式を解け。<br>(1) $2\sin\theta+1<0$　　(2) $\tan\theta\leqq\sqrt3$",
  "exa": r"(1) $\dfrac76\pi<\theta<\dfrac{11}{6}\pi$　(2) $0\leqq\theta\leqq\dfrac{\pi}{3},\ \dfrac{\pi}{2}<\theta\leqq\dfrac43\pi,\ \dfrac32\pi<\theta<2\pi$"},
 {"lv": 2, "title": r"$2\theta+\alpha$ の形の角を含む方程式・不等式",
  "q": r"$0\leqq\theta<\pi$ のとき，次の方程式・不等式を解け。<br>(1) $\sin\left(2\theta+\dfrac{\pi}{3}\right)=-\dfrac12$　　(2) $\cos\left(2\theta-\dfrac{\pi}{6}\right)>\dfrac12$",
  "hint": r"$t=2\theta+\dfrac{\pi}{3}$ のようにおき，まず $t$ の変域を求める。$\theta$ の範囲が $0\leqq\theta<\pi$ でも，$t$ は長さ $2\pi$ の範囲を動くので解は2つずつ出てくる。",
  "sol": r"(1) $t=2\theta+\dfrac{\pi}{3}$ とおくと，$0\leqq\theta<\pi$ より $\dfrac{\pi}{3}\leqq t<\dfrac73\pi$。<br>"
         r"この範囲で $\sin t=-\dfrac12$ となるのは $t=\dfrac76\pi,\ \dfrac{11}{6}\pi$。よって $2\theta=\dfrac56\pi,\ \dfrac32\pi$ で　$\boldsymbol{\theta=\dfrac{5}{12}\pi,\ \dfrac34\pi}$<br>"
         r"(2) $t=2\theta-\dfrac{\pi}{6}$ とおくと $-\dfrac{\pi}{6}\leqq t<\dfrac{11}{6}\pi$。<br>"
         r"この範囲で $\cos t>\dfrac12$ となるのは　$-\dfrac{\pi}{6}\leqq t<\dfrac{\pi}{3}$，$\dfrac53\pi<t<\dfrac{11}{6}\pi$<br>"
         r"よって $0\leqq2\theta<\dfrac{\pi}{2}$，$\dfrac{11}{6}\pi<2\theta<2\pi$ で　$\boldsymbol{0\leqq\theta<\dfrac{\pi}{4},\ \dfrac{11}{12}\pi<\theta<\pi}$",
  "note": r"(2) で $t$ の範囲を $0\leqq t<2\pi$ のつもりで解くと，$-\dfrac{\pi}{6}\leqq t<0$ の部分（$\theta$ が $0$ に近い部分）を落とす。変域の両端を正確に求めることが大切。",
  "ex": r"$0\leqq\theta<\pi$ のとき，次の方程式・不等式を解け。<br>(1) $\sin\left(2\theta-\dfrac{\pi}{4}\right)=\dfrac{\sqrt3}{2}$　　(2) $\cos\left(2\theta+\dfrac{\pi}{4}\right)\leqq-\dfrac{\sqrt2}{2}$",
  "exa": r"(1) $\theta=\dfrac{7}{24}\pi,\ \dfrac{11}{24}\pi$　(2) $\dfrac{\pi}{4}\leqq\theta\leqq\dfrac{\pi}{2}$"},
 {"lv": 2, "title": r"$\sin\theta,\ \cos\theta$ の2次方程式・2次不等式",
  "q": r"$0\leqq\theta<2\pi$ のとき，次の方程式・不等式を解け。<br>(1) $2\cos^2\theta+3\sin\theta-3=0$　　(2) $2\sin^2\theta+\cos\theta-1<0$",
  "hint": r"$\sin^2\theta+\cos^2\theta=1$ で一方の関数にそろえると，その関数の2次方程式・2次不等式になる。$-1\leqq\sin\theta\leqq1$，$-1\leqq\cos\theta\leqq1$ を忘れない。",
  "sol": r"(1) $\cos^2\theta=1-\sin^2\theta$ を代入して整理すると　$2\sin^2\theta-3\sin\theta+1=0$<br>"
         r"$(2\sin\theta-1)(\sin\theta-1)=0$ より $\sin\theta=\dfrac12,\ 1$。よって　$\boldsymbol{\theta=\dfrac{\pi}{6},\ \dfrac{\pi}{2},\ \dfrac56\pi}$<br>"
         r"(2) $\sin^2\theta=1-\cos^2\theta$ を代入して整理すると $-2\cos^2\theta+\cos\theta+1<0$，すなわち<br>"
         r"$2\cos^2\theta-\cos\theta-1>0$，$(2\cos\theta+1)(\cos\theta-1)>0$<br>"
         r"$\cos\theta-1\leqq0$ だから，成り立つのは $\cos\theta-1<0$ かつ $2\cos\theta+1<0$，すなわち $\cos\theta<-\dfrac12$ のとき。<br>"
         r"よって　$\boldsymbol{\dfrac23\pi<\theta<\dfrac43\pi}$",
  "note": r"(2) を「$\cos\theta<-\dfrac12$ または $\cos\theta>1$」としてから $\cos\theta>1$ を捨ててもよい。置き換えた文字の変域で不要な解を除く作業を必ず行う。",
  "ex": r"$0\leqq\theta<2\pi$ のとき，次の方程式・不等式を解け。<br>(1) $2\sin^2\theta-5\cos\theta+1=0$　　(2) $2\cos^2\theta-\sin\theta-1\geqq0$",
  "exa": r"(1) $\theta=\dfrac{\pi}{3},\ \dfrac53\pi$　(2) $0\leqq\theta\leqq\dfrac{\pi}{6},\ \dfrac56\pi\leqq\theta<2\pi$"},
 {"lv": 3, "title": r"$\sin A=\sin B$ の形に直して解く",
  "q": r"$0\leqq\theta<2\pi$ のとき，方程式 $\sin3\theta=\cos\theta$ を解け。",
  "hint": r"$\cos\theta=\sin\left(\dfrac{\pi}{2}-\theta\right)$ と直すと $\sin A=\sin B$ の形になる。一般解 $A=B+2n\pi$ または $A=\pi-B+2n\pi$ を使えば，$3\theta$ を展開せずに解ける。",
  "sol": r"$\cos\theta=\sin\left(\dfrac{\pi}{2}-\theta\right)$ より，方程式は $\sin3\theta=\sin\left(\dfrac{\pi}{2}-\theta\right)$。よって，$n$ を整数として<br>"
         r"$3\theta=\dfrac{\pi}{2}-\theta+2n\pi$ …①　または　$3\theta=\pi-\left(\dfrac{\pi}{2}-\theta\right)+2n\pi$ …②<br>"
         r"①より $\theta=\dfrac{\pi}{8}+\dfrac{n\pi}{2}$。$0\leqq\theta<2\pi$ となるのは $n=0,\ 1,\ 2,\ 3$ で　$\theta=\dfrac{\pi}{8},\ \dfrac58\pi,\ \dfrac98\pi,\ \dfrac{13}{8}\pi$<br>"
         r"②より $2\theta=\dfrac{\pi}{2}+2n\pi$，$\theta=\dfrac{\pi}{4}+n\pi$。$n=0,\ 1$ で　$\theta=\dfrac{\pi}{4},\ \dfrac54\pi$<br>"
         r"①と②の解に重なりはないから　$\boldsymbol{\theta=\dfrac{\pi}{8},\ \dfrac{\pi}{4},\ \dfrac58\pi,\ \dfrac98\pi,\ \dfrac54\pi,\ \dfrac{13}{8}\pi}$",
  "note": r"3倍角の公式（後の節）で $\sin3\theta=3\sin\theta-4\sin^3\theta$ と展開すると $\sin\theta$ と $\cos\theta$ が混ざって解きにくい。$\sin A=\sin B$ の一般解は，単位円で「$y$ 座標が等しい2つの動径」を考えれば導ける。",
  "ex": r"$0\leqq\theta<\pi$ のとき，方程式 $\cos3\theta=\sin\theta$ を解け。",
  "exa": r"$\theta=\dfrac{\pi}{8},\ \dfrac58\pi,\ \dfrac34\pi$"},
]})


@_v
def _v4():
    import sympy as sp
    from sympy import sin, cos, tan, pi, sqrt, Rational as R
    P = math.pi
    _same_roots(lambda t: 2 * math.sin(t) + math.sqrt(3), [4 * P / 3, 5 * P / 3])
    _same_roots(lambda t: math.sqrt(3) * math.sin(t) - math.cos(t), [P / 6, 7 * P / 6])        # √3 tanθ = 1
    _same_roots(lambda t: 2 * math.cos(t) - math.sqrt(2), [P / 4, 7 * P / 4])
    _same_roots(lambda t: 2 * math.cos(t) + math.sqrt(2), [3 * P / 4, 5 * P / 4])
    _same_roots(lambda t: math.sin(t) + math.sqrt(3) * math.cos(t), [2 * P / 3, 5 * P / 3])    # tanθ = -√3
    for n in range(-3, 4):
        _eq(2 * sin(R(4, 3) * pi + 2 * n * pi) + sqrt(3), 0); _eq(2 * sin(R(5, 3) * pi + 2 * n * pi) + sqrt(3), 0)
    # 不等式
    _same_set(lambda t: 2 * math.cos(t) <= -1, [(2 * P / 3, 4 * P / 3)])
    _eq(2 * cos(2 * pi / 3), -1); _eq(2 * cos(4 * pi / 3), -1)
    _same_set(lambda t: math.sqrt(2) * math.sin(t) > 1, [(P / 4, 3 * P / 4)])
    tanok = lambda t: abs(math.cos(t)) > 1e-9
    _same_set(lambda t: tanok(t) and math.tan(t) > 1, [(P / 4, P / 2), (5 * P / 4, 3 * P / 2)])
    _same_set(lambda t: 2 * math.sin(t) + 1 < 0, [(7 * P / 6, 11 * P / 6)])
    _same_set(lambda t: tanok(t) and math.tan(t) <= math.sqrt(3), [(0, P / 3), (P / 2, 4 * P / 3), (3 * P / 2, 2 * P)])
    _eq(tan(pi / 3), sqrt(3)); _eq(tan(4 * pi / 3), sqrt(3))
    # 2θ+α
    _same_roots(lambda t: math.sin(2 * t + P / 3) + 0.5, [5 * P / 12, 3 * P / 4], 0, P)
    _same_set(lambda t: math.cos(2 * t - P / 6) > 0.5, [(-1, P / 4), (11 * P / 12, P + 1)], 0, P)
    assert math.cos(-P / 6) > 0.5                       # θ=0 は解
    _same_roots(lambda t: math.sin(2 * t - P / 4) - math.sqrt(3) / 2, [7 * P / 24, 11 * P / 24], 0, P)
    _same_set(lambda t: math.cos(2 * t + P / 4) <= -math.sqrt(2) / 2, [(P / 4, P / 2)], 0, P)
    _eq(cos(2 * pi / 4 + pi / 4), -sqrt(2) / 2); _eq(cos(2 * pi / 2 + pi / 4), -sqrt(2) / 2)
    # 2次
    _same_roots(lambda t: 2 * math.cos(t)**2 + 3 * math.sin(t) - 3, [P / 6, P / 2, 5 * P / 6])
    _same_set(lambda t: 2 * math.sin(t)**2 + math.cos(t) - 1 < 0, [(2 * P / 3, 4 * P / 3)])
    _same_roots(lambda t: 2 * math.sin(t)**2 - 5 * math.cos(t) + 1, [P / 3, 5 * P / 3])
    _same_set(lambda t: 2 * math.cos(t)**2 - math.sin(t) - 1 >= 0, [(-1, P / 6), (5 * P / 6, 3 * P)])
    x = sp.symbols("x")
    assert sp.expand((2 * x - 1) * (x - 1)) == 2 * x**2 - 3 * x + 1
    assert sp.expand((2 * x + 1) * (x - 1)) == 2 * x**2 - x - 1
    # sin3θ = cosθ
    _same_roots(lambda t: math.sin(3 * t) - math.cos(t), [P / 8, P / 4, 5 * P / 8, 9 * P / 8, 5 * P / 4, 13 * P / 8])
    _same_roots(lambda t: math.cos(3 * t) - math.sin(t), [P / 8, 5 * P / 8, 3 * P / 4], 0, P)


# ---------------------------------------------------------------- 節5
SEC.append({"title": "加法定理",
"base": r"""・$\sin(\alpha\pm\beta)=\sin\alpha\cos\beta\pm\cos\alpha\sin\beta$，$\cos(\alpha\pm\beta)=\cos\alpha\cos\beta\mp\sin\alpha\sin\beta$（複号同順）<br>
・$\tan(\alpha\pm\beta)=\dfrac{\tan\alpha\pm\tan\beta}{1\mp\tan\alpha\tan\beta}$（複号同順）<br>
・2直線 $y=m_1x+n_1$，$y=m_2x+n_2$ のなす角 $\theta$（$0<\theta<\dfrac{\pi}{2}$）：$\tan\theta=\left|\dfrac{m_1-m_2}{1+m_1m_2}\right|$（$1+m_1m_2=0$ のときは垂直）""",
"items": [
 {"lv": 1, "title": "加法定理による値の計算",
  "q": r"(1) $\sin75^\circ$，$\cos15^\circ$，$\tan105^\circ$ の値を求めよ。<br>"
       r"(2) $\alpha$ は第2象限の角，$\beta$ は第4象限の角で，$\sin\alpha=\dfrac35$，$\cos\beta=\dfrac{5}{13}$ のとき，$\sin(\alpha+\beta)$，$\cos(\alpha-\beta)$ の値を求めよ。",
  "hint": r"(1) $75^\circ=45^\circ+30^\circ$ などと，値の分かる角の和・差に分ける。(2) 加法定理に必要な $\cos\alpha$，$\sin\beta$ を相互関係で先に求める（符号は象限で決める）。",
  "sol": r"(1) $\sin75^\circ=\sin(45^\circ+30^\circ)=\sin45^\circ\cos30^\circ+\cos45^\circ\sin30^\circ=\dfrac{\sqrt2}{2}\cdot\dfrac{\sqrt3}{2}+\dfrac{\sqrt2}{2}\cdot\dfrac12=\boldsymbol{\dfrac{\sqrt6+\sqrt2}{4}}$<br>"
         r"$\cos15^\circ=\cos(45^\circ-30^\circ)=\cos45^\circ\cos30^\circ+\sin45^\circ\sin30^\circ=\boldsymbol{\dfrac{\sqrt6+\sqrt2}{4}}$<br>"
         r"$\tan105^\circ=\tan(60^\circ+45^\circ)=\dfrac{\sqrt3+1}{1-\sqrt3\cdot1}=\dfrac{(\sqrt3+1)^2}{(1-\sqrt3)(1+\sqrt3)}=\dfrac{4+2\sqrt3}{-2}=\boldsymbol{-2-\sqrt3}$<br>"
         r"(2) $\alpha$ は第2象限の角だから $\cos\alpha<0$ で $\cos\alpha=-\sqrt{1-\dfrac{9}{25}}=-\dfrac45$。<br>"
         r"$\beta$ は第4象限の角だから $\sin\beta<0$ で $\sin\beta=-\sqrt{1-\dfrac{25}{169}}=-\dfrac{12}{13}$。<br>"
         r"$\sin(\alpha+\beta)=\sin\alpha\cos\beta+\cos\alpha\sin\beta=\dfrac35\cdot\dfrac{5}{13}+\left(-\dfrac45\right)\left(-\dfrac{12}{13}\right)=\boldsymbol{\dfrac{63}{65}}$<br>"
         r"$\cos(\alpha-\beta)=\cos\alpha\cos\beta+\sin\alpha\sin\beta=\left(-\dfrac45\right)\cdot\dfrac{5}{13}+\dfrac35\cdot\left(-\dfrac{12}{13}\right)=\boldsymbol{-\dfrac{56}{65}}$",
  "note": r"$\cos15^\circ=\sin75^\circ$ は $\cos(90^\circ-\theta)=\sin\theta$ からも分かる。$15^\circ$，$75^\circ$ の正弦・余弦の値 $\dfrac{\sqrt6\pm\sqrt2}{4}$ はよく使うので覚えておくとよい。",
  "ex": r"(1) $\cos75^\circ$，$\tan15^\circ$ の値を求めよ。<br>(2) $0<\alpha<\dfrac{\pi}{2}$，$\dfrac{\pi}{2}<\beta<\pi$，$\sin\alpha=\dfrac45$，$\cos\beta=-\dfrac{12}{13}$ のとき，$\cos(\alpha+\beta)$，$\sin(\alpha-\beta)$ の値を求めよ。",
  "exa": r"(1) $\dfrac{\sqrt6-\sqrt2}{4}$，$2-\sqrt3$　(2) $\cos(\alpha+\beta)=-\dfrac{56}{65}$，$\sin(\alpha-\beta)=-\dfrac{63}{65}$"},
 {"lv": 2, "title": "2直線のなす角",
  "q": r"(1) 2直線 $y=2x+1$，$y=-3x+2$ のなす角 $\theta$（$0<\theta<\dfrac{\pi}{2}$）を求めよ。<br>(2) 直線 $y=2x$ と $\dfrac{\pi}{4}$ の角をなす直線の傾きを求めよ。",
  "hint": r"直線が $x$ 軸の正の向きとなす角を $\alpha$ とすると，傾きは $\tan\alpha$。2直線のなす角は角の差に関係するので，$\tan$ の加法定理を使う。",
  "sol": r"(1) 2直線が $x$ 軸の正の向きとなす角をそれぞれ $\alpha,\ \beta$（$0\leqq\alpha<\pi$，$0\leqq\beta<\pi$）とすると，$\tan\alpha=2$，$\tan\beta=-3$ で $0<\alpha<\dfrac{\pi}{2}<\beta<\pi$。<br>"
         r"$\tan(\beta-\alpha)=\dfrac{\tan\beta-\tan\alpha}{1+\tan\beta\tan\alpha}=\dfrac{-3-2}{1+(-3)\cdot2}=1$<br>"
         r"$0<\beta-\alpha<\pi$ より $\beta-\alpha=\dfrac{\pi}{4}$。これは $\dfrac{\pi}{2}$ より小さいから　$\boldsymbol{\theta=\dfrac{\pi}{4}}$<br>"
         r"(2) 直線 $y=2x$ が $x$ 軸の正の向きとなす角を $\alpha$ とすると $\tan\alpha=2$。求める直線が $x$ 軸の正の向きとなす角は $\alpha\pm\dfrac{\pi}{4}$ だから，傾きは<br>"
         r"$\tan\left(\alpha+\dfrac{\pi}{4}\right)=\dfrac{2+1}{1-2\cdot1}=-3$，　$\tan\left(\alpha-\dfrac{\pi}{4}\right)=\dfrac{2-1}{1+2\cdot1}=\dfrac13$<br>"
         r"よって　$\boldsymbol{-3,\ \dfrac13}$",
  "note": r"角の差が $\dfrac{\pi}{2}$ より大きくなったときは，なす角はその補角 $\pi-(\beta-\alpha)$ である。公式 $\tan\theta=\left|\dfrac{m_1-m_2}{1+m_1m_2}\right|$ はこれをまとめたもの。(2) は「$\pm$」の2通りを忘れやすい。",
  "ex": r"(1) 2直線 $y=x$，$y=(2+\sqrt3)x$ のなす角 $\theta$（$0<\theta<\dfrac{\pi}{2}$）を求めよ。<br>(2) 直線 $y=3x$ と $\dfrac{\pi}{4}$ の角をなす直線の傾きを求めよ。",
  "exa": r"(1) $\dfrac{\pi}{6}$　(2) $-2,\ \dfrac12$"},
 {"lv": 3, "title": r"$\tan$ の値から角の和を求める",
  "q": r"$\alpha,\ \beta,\ \gamma$ は鋭角で，$\tan\alpha=\dfrac12$，$\tan\beta=\dfrac15$，$\tan\gamma=\dfrac18$ である。$\alpha+\beta+\gamma$ の値を求めよ。",
  "hint": r"まず $\tan(\alpha+\beta)$，次に $\tan\{(\alpha+\beta)+\gamma\}$ を求める。最後に $\alpha+\beta+\gamma$ のとり得る範囲を絞って，角を1つに決める。",
  "sol": r"$\tan(\alpha+\beta)=\dfrac{\frac12+\frac15}{1-\frac12\cdot\frac15}=\dfrac{\frac{7}{10}}{\frac{9}{10}}=\dfrac79$<br>"
         r"$\tan(\alpha+\beta+\gamma)=\dfrac{\frac79+\frac18}{1-\frac79\cdot\frac18}=\dfrac{\frac{65}{72}}{\frac{65}{72}}=1$<br>"
         r"ここで $0<\tan\alpha<1$，$0<\tan\beta<1$，$0<\tan\gamma<1$ より $0<\alpha,\ \beta,\ \gamma<\dfrac{\pi}{4}$ だから　$0<\alpha+\beta+\gamma<\dfrac34\pi$<br>"
         r"この範囲で $\tan$ の値が $1$ となる角は $\dfrac{\pi}{4}$ だけである。よって　$\boldsymbol{\alpha+\beta+\gamma=\dfrac{\pi}{4}}$",
  "note": r"範囲の絞り込みが甘いと（例えば鋭角だから $0<\alpha+\beta+\gamma<\dfrac32\pi$ とするだけでは），$\dfrac54\pi$ も候補に残ってしまう。$\tan\theta$ の値から角を決めるときは，角の範囲を長さ $\pi$ 未満に絞ることが必要。",
  "ex": r"鋭角 $\alpha,\ \beta,\ \gamma$ が $\tan\alpha=\dfrac13$，$\tan\beta=\dfrac14$，$\tan\gamma=\dfrac29$ を満たすとき，$\alpha+\beta+\gamma$ の値を求めよ。",
  "exa": r"$\dfrac{\pi}{4}$"},
 {"lv": 3, "title": r"$\sin\alpha+\sin\beta$，$\cos\alpha+\cos\beta$ の値から求める",
  "q": r"$\sin\alpha+\sin\beta=\dfrac12$，$\cos\alpha+\cos\beta=\dfrac13$ のとき，次の値を求めよ。<br>(1) $\cos(\alpha-\beta)$　　(2) $\cos(\alpha+\beta)$",
  "hint": r"(1) 2つの式をそれぞれ2乗して加えると，$\sin^2+\cos^2=1$ と加法定理により $\cos(\alpha-\beta)$ だけが残る。(2) 2乗して引くと $\cos^2\alpha-\sin^2\alpha=\cos(\alpha+\alpha)$ などが現れる。$2\alpha=(\alpha+\beta)+(\alpha-\beta)$，$2\beta=(\alpha+\beta)-(\alpha-\beta)$ と見る。",
  "sol": r"(1) 2式を2乗して加えると<br>"
         r"$(\sin^2\alpha+\cos^2\alpha)+(\sin^2\beta+\cos^2\beta)+2(\cos\alpha\cos\beta+\sin\alpha\sin\beta)=\dfrac14+\dfrac19$<br>"
         r"$2+2\cos(\alpha-\beta)=\dfrac{13}{36}$ より　$\cos(\alpha-\beta)=\boldsymbol{-\dfrac{59}{72}}$<br>"
         r"(2) 第2式の2乗から第1式の2乗を引くと<br>"
         r"$(\cos^2\alpha-\sin^2\alpha)+(\cos^2\beta-\sin^2\beta)+2(\cos\alpha\cos\beta-\sin\alpha\sin\beta)=\dfrac19-\dfrac14$<br>"
         r"加法定理より $\cos^2\alpha-\sin^2\alpha=\cos(\alpha+\alpha)=\cos2\alpha$ などとなるので　$\cos2\alpha+\cos2\beta+2\cos(\alpha+\beta)=-\dfrac{5}{36}$ …①<br>"
         r"$u=\alpha+\beta$，$v=\alpha-\beta$ とおくと $2\alpha=u+v$，$2\beta=u-v$ だから　$\cos2\alpha+\cos2\beta=\cos(u+v)+\cos(u-v)=2\cos u\cos v$<br>"
         r"よって①は $2\cos(\alpha+\beta)\{\cos(\alpha-\beta)+1\}=-\dfrac{5}{36}$。(1) より $\cos(\alpha-\beta)+1=\dfrac{13}{72}$ だから<br>"
         r"$\cos(\alpha+\beta)=-\dfrac{5}{36}\div\dfrac{13}{36}=\boldsymbol{-\dfrac{5}{13}}$",
  "note": r"和と積の公式（後の節）を使うと，$\sin\alpha+\sin\beta=2\sin\dfrac{\alpha+\beta}{2}\cos\dfrac{\alpha-\beta}{2}$，$\cos\alpha+\cos\beta=2\cos\dfrac{\alpha+\beta}{2}\cos\dfrac{\alpha-\beta}{2}$ の比から $\tan\dfrac{\alpha+\beta}{2}=\dfrac32$ が分かり，$\cos(\alpha+\beta)=\dfrac{1-\tan^2\frac{\alpha+\beta}{2}}{1+\tan^2\frac{\alpha+\beta}{2}}=-\dfrac{5}{13}$ と速く求まる。",
  "ex": r"$\sin\alpha-\sin\beta=\dfrac13$，$\cos\alpha-\cos\beta=\dfrac12$ のとき，$\cos(\alpha-\beta)$，$\cos(\alpha+\beta)$ の値を求めよ。",
  "exa": r"$\cos(\alpha-\beta)=\dfrac{59}{72}$，$\cos(\alpha+\beta)=-\dfrac{5}{13}$"},
 {"lv": 4, "title": r"$\tan A+\tan B+\tan C=\tan A\tan B\tan C$ と整数",
  "q": r"直角三角形でない三角形 ABC について，次の問いに答えよ。<br>"
       r"(1) $\tan A+\tan B+\tan C=\tan A\tan B\tan C$ が成り立つことを証明せよ。<br>"
       r"(2) $\tan A,\ \tan B,\ \tan C$ がすべて整数であるとき，それらの値を求めよ。",
  "hint": r"(1) $A+B=\pi-C$ の両辺の $\tan$ をとり，加法定理の分母を払う。(2) 鈍角は高々1つ。鈍角があると $\tan$ が正の整数の2角は $\dfrac{\pi}{4}$ 以上で矛盾。鋭角だけなら $x\leqq y\leqq z$ として $xyz=x+y+z\leqq3z$ から $xy\leqq3$ と絞る。",
  "sol": r"(1) 直角三角形でないから $A,\ B,\ C$ はいずれも $\dfrac{\pi}{2}$ でなく，$\tan A,\ \tan B,\ \tan C$ は定義される。また $A+B=\pi-C\neq\dfrac{\pi}{2}$ より $\cos(A+B)\neq0$。<br>"
         r"$\cos(A+B)=\cos A\cos B(1-\tan A\tan B)$ だから $1-\tan A\tan B\neq0$ で，$\tan(A+B)=\dfrac{\tan A+\tan B}{1-\tan A\tan B}$。<br>"
         r"一方 $\tan(A+B)=\tan(\pi-C)=-\tan C$ なので　$\tan A+\tan B=-\tan C(1-\tan A\tan B)=-\tan C+\tan A\tan B\tan C$<br>"
         r"よって $\tan A+\tan B+\tan C=\tan A\tan B\tan C$ が成り立つ。$\blacksquare$<br>"
         r"(2) $0<A,\ B,\ C<\pi$ で直角はないから，$\tan A,\ \tan B,\ \tan C$ は $0$ でない整数である。<br>"
         r"(i) 鈍角があるとき：鈍角は1つだけなので，それを $C$ とする。$\tan A,\ \tan B$ は正の整数だから $\tan A\geqq1$，$\tan B\geqq1$，すなわち $A\geqq\dfrac{\pi}{4}$，$B\geqq\dfrac{\pi}{4}$。すると $C=\pi-A-B\leqq\dfrac{\pi}{2}$ となり矛盾。<br>"
         r"(ii) すべて鋭角のとき：$\tan A,\ \tan B,\ \tan C$ を小さい順に $x\leqq y\leqq z$（正の整数）とすると，(1) より $xyz=x+y+z\leqq3z$。よって $xy\leqq3$。<br>"
         r"$(x,\ y)=(1,\ 1)$ のとき $z=2+z$ で不適。$(1,\ 2)$ のとき $2z=3+z$ より $z=3$。$(1,\ 3)$ のとき $3z=4+z$ より $z=2$ となり $y\leqq z$ に反する。<br>"
         r"逆に，$\tan\alpha=2$，$\tan\beta=3$ の鋭角 $\alpha,\ \beta$ について $\tan(\alpha+\beta)=\dfrac{2+3}{1-6}=-1$，$\dfrac{\pi}{2}<\alpha+\beta<\pi$ より $\alpha+\beta=\dfrac34\pi$ で，$\dfrac{\pi}{4}+\alpha+\beta=\pi$。よって $\tan$ の値が $1,\ 2,\ 3$ の三角形は存在する。<br>"
         r"答　$\tan A,\ \tan B,\ \tan C$ の値は $\boldsymbol{1,\ 2,\ 3}$（順序は問わない）",
  "note": r"(1) の恒等式は $A+B+C=\pi$ だけから導かれる。(2) のように，対称性を利用して大小を仮定し，不等式で範囲を絞るのは整数問題の定石。",
  "ex": r"$\alpha,\ \beta,\ \gamma$ は正の角で $\alpha+\beta+\gamma=\dfrac{\pi}{2}$ を満たす。$\tan\alpha\tan\beta+\tan\beta\tan\gamma+\tan\gamma\tan\alpha=1$ を証明せよ。また，$\dfrac{1}{\tan\alpha},\ \dfrac{1}{\tan\beta},\ \dfrac{1}{\tan\gamma}$ がすべて整数となるとき，その値を求めよ。",
  "exa": r"$\tan(\alpha+\beta)=\dfrac{1}{\tan\gamma}$ の分母を払えばよい。値は $1,\ 2,\ 3$（順序は問わない）"},
 {"lv": 5, "title": r"$\sin x+\sin y+\sin z=\cos x+\cos y+\cos z=0$ の条件",
  "q": r"実数 $x,\ y,\ z$ が $\sin x+\sin y+\sin z=0$，$\cos x+\cos y+\cos z=0$ を満たすとき，次の問いに答えよ。<br>"
       r"(1) $\cos(x-y)$ の値を求めよ。<br>(2) $\cos2x+\cos2y+\cos2z$ の値を求めよ。<br>(3) $\cos3x+\cos3y+\cos3z=3\cos(x+y+z)$ が成り立つことを証明せよ。",
  "hint": r"移項して $\sin x+\sin y=-\sin z$，$\cos x+\cos y=-\cos z$ とし，2乗して加えると $z$ が消える。同様に $x-y,\ y-z,\ z-x$ の余弦がすべて分かるので，$y,\ z$ を $x$ で表してしまうのが早い。",
  "sol": r"(1) $\sin x+\sin y=-\sin z$，$\cos x+\cos y=-\cos z$ の両辺を2乗して加えると<br>"
         r"$2+2(\cos x\cos y+\sin x\sin y)=\sin^2z+\cos^2z=1$。よって $2+2\cos(x-y)=1$ で　$\cos(x-y)=\boldsymbol{-\dfrac12}$<br>"
         r"(2) 同様に $\cos(y-z)=\cos(z-x)=-\dfrac12$ である。<br>"
         r"$\cos(y-x)=-\dfrac12$ より $y=x\pm\dfrac23\pi+2m\pi$（$m$ は整数），同様に $z=x\pm\dfrac23\pi+2l\pi$（$l$ は整数）。<br>"
         r"$y,\ z$ の複号が同じだと $y-z$ が $2\pi$ の整数倍となり，$\cos(y-z)=1$ で矛盾する。よって複号は異なる。$y$ と $z$ を入れかえても条件も求める式も変わらないから，<br>"
         r"$y=x+\dfrac23\pi+2m\pi$，$z=x-\dfrac23\pi+2l\pi$　としてよい。<br>"
         r"【補題】任意の $a$ に対して，加法定理より $\cos\left(a+\dfrac23\pi\right)+\cos\left(a-\dfrac23\pi\right)=2\cos a\cos\dfrac23\pi=-\cos a$。<br>"
         r"よって　$\cos a+\cos\left(a+\dfrac23\pi\right)+\cos\left(a-\dfrac23\pi\right)=0$<br>"
         r"$2y=2x+\dfrac43\pi+4m\pi$，$2z=2x-\dfrac43\pi+4l\pi$ より　$\cos2y=\cos\left(2x-\dfrac23\pi\right)$，$\cos2z=\cos\left(2x+\dfrac23\pi\right)$<br>"
         r"（$\dfrac43\pi=-\dfrac23\pi+2\pi$ を用いた）。補題で $a=2x$ として　$\cos2x+\cos2y+\cos2z=\boldsymbol{0}$<br>"
         r"(3) $3y=3x+2\pi+6m\pi$，$3z=3x-2\pi+6l\pi$ より $\cos3y=\cos3z=\cos3x$。よって 左辺 $=3\cos3x$。<br>"
         r"また $x+y+z=3x+2(m+l)\pi$ より 右辺 $=3\cos3x$。したがって等式は成り立つ。$\blacksquare$",
  "note": r"条件は「単位円周上の3点 $(\cos x,\ \sin x)$，$(\cos y,\ \sin y)$，$(\cos z,\ \sin z)$ の重心が原点」ということで，3点は正三角形の頂点になる。(2) は，$\cos(x+y)=\cos\{(x+y+z)-z\}$ を展開して $\cos(x+y)+\cos(y+z)+\cos(z+x)=0$ を示し，$(\cos x+\cos y+\cos z)^2-(\sin x+\sin y+\sin z)^2=0$ を展開する方法でも解ける。",
  "ex": r"実数 $x,\ y,\ z$ が例題と同じ条件を満たすとき，$\sin2x+\sin2y+\sin2z$ と $\cos(x+y)+\cos(y+z)+\cos(z+x)$ の値を求めよ。",
  "exa": r"どちらも $0$"},
]})


@_v
def _v5():
    import sympy as sp
    from sympy import sin, cos, tan, pi, sqrt, Rational as R, atan
    d = lambda x: pi * x / 180
    _eq(sin(d(75)), (sqrt(6) + sqrt(2)) / 4); _eq(cos(d(15)), (sqrt(6) + sqrt(2)) / 4); _eq(tan(d(105)), -2 - sqrt(3))
    _eq(cos(d(75)), (sqrt(6) - sqrt(2)) / 4); _eq(tan(d(15)), 2 - sqrt(3))
    _eq((sqrt(3) + 1)**2 / ((1 - sqrt(3)) * (1 + sqrt(3))), -2 - sqrt(3))
    a = math.pi - math.asin(3 / 5); b = -math.acos(5 / 13)
    assert abs(math.sin(a + b) - 63 / 65) < 1e-12 and abs(math.cos(a - b) + 56 / 65) < 1e-12
    a = math.asin(4 / 5); b = math.acos(-12 / 13)
    assert abs(math.cos(a + b) + 56 / 65) < 1e-12 and abs(math.sin(a - b) + 63 / 65) < 1e-12
    # なす角
    al, be = math.atan(2), math.pi + math.atan(-3)
    assert abs(be - al - math.pi / 4) < 1e-12
    assert abs(math.tan(al + math.pi / 4) + 3) < 1e-12 and abs(math.tan(al - math.pi / 4) - 1 / 3) < 1e-12
    assert abs(math.atan(2 + math.sqrt(3)) - math.pi / 4 - math.pi / 6) < 1e-12
    al = math.atan(3)
    assert abs(math.tan(al + math.pi / 4) + 2) < 1e-12 and abs(math.tan(al - math.pi / 4) - 0.5) < 1e-12
    # tan の和
    assert abs(math.atan(1 / 2) + math.atan(1 / 5) + math.atan(1 / 8) - math.pi / 4) < 1e-12
    assert abs(math.atan(1 / 3) + math.atan(1 / 4) + math.atan(2 / 9) - math.pi / 4) < 1e-12
    assert (Fr(7, 9) + Fr(1, 8)) / (1 - Fr(7, 72)) == 1 and (Fr(1, 2) + Fr(1, 5)) / (1 - Fr(1, 10)) == Fr(7, 9)
    # sin α + sin β = S, cos α + cos β = C から α, β を作る
    for S, C, sg, c1, c2 in [(0.5, 1 / 3, 1, -59 / 72, -5 / 13), (1 / 3, 0.5, -1, 59 / 72, -5 / 13)]:
        if sg == 1:      # 和：S=2 sin u cos v, C=2 cos u cos v
            u = math.atan2(S, C); v = math.acos(math.hypot(S, C) / 2)
            A, B = u + v, u - v
            assert abs(math.sin(A) + math.sin(B) - S) < 1e-12 and abs(math.cos(A) + math.cos(B) - C) < 1e-12
        else:            # 差：sinα-sinβ = 2cos u sin v = S，cosα-cosβ = -2 sin u sin v = C
            u = math.atan2(-C, S); v = math.asin(math.hypot(S, C) / 2)
            A, B = u + v, u - v
            assert abs(math.sin(A) - math.sin(B) - S) < 1e-12 and abs(math.cos(A) - math.cos(B) - C) < 1e-12
        assert abs(math.cos(A - B) - c1) < 1e-12 and abs(math.cos(A + B) - c2) < 1e-12
    # tanA+tanB+tanC 恒等式と整数解
    A_, B_ = sp.symbols("A B")
    C_ = pi - A_ - B_
    assert sp.simplify(sp.expand_trig(tan(A_) + tan(B_) + tan(C_) - tan(A_) * tan(B_) * tan(C_))) == 0
    ang = lambda t: math.atan(t) if t > 0 else math.pi + math.atan(t)
    found = set()
    for x in range(-40, 41):
        for y in range(x, 41):
            for z in range(y, 41):
                if 0 in (x, y, z):
                    continue
                if abs(ang(x) + ang(y) + ang(z) - math.pi) < 1e-9:
                    found.add((x, y, z))
    assert found == {(1, 2, 3)}, found
    found = set()
    for p in range(1, 60):
        for q in range(p, 60):
            for r in range(q, 60):
                if abs(math.atan(1 / p) + math.atan(1 / q) + math.atan(1 / r) - math.pi / 2) < 1e-9:
                    found.add((p, q, r))
    assert found == {(1, 2, 3)}
    rnd = random.Random(5)
    for _ in range(200):
        a_ = rnd.uniform(0.01, 1.5); b_ = rnd.uniform(0.01, 1.55 - a_); g_ = math.pi / 2 - a_ - b_
        ta, tb, tg = math.tan(a_), math.tan(b_), math.tan(g_)
        assert abs(ta * tb + tb * tg + tg * ta - 1) < 1e-8
    # sin x+sin y+sin z = cos x+cos y+cos z = 0
    for _ in range(300):
        x = rnd.uniform(-10, 10); m, l = rnd.randint(-3, 3), rnd.randint(-3, 3)
        y = x + 2 * math.pi / 3 + 2 * m * math.pi; z = x - 2 * math.pi / 3 + 2 * l * math.pi
        if rnd.random() < 0.5:
            y, z = z, y
        assert abs(math.sin(x) + math.sin(y) + math.sin(z)) < 1e-9 and abs(math.cos(x) + math.cos(y) + math.cos(z)) < 1e-9
        assert abs(math.cos(x - y) + 0.5) < 1e-9 and abs(math.cos(y - z) + 0.5) < 1e-9
        assert abs(math.cos(2 * x) + math.cos(2 * y) + math.cos(2 * z)) < 1e-9
        assert abs(math.cos(3 * x) + math.cos(3 * y) + math.cos(3 * z) - 3 * math.cos(x + y + z)) < 1e-8
        assert abs(math.sin(2 * x) + math.sin(2 * y) + math.sin(2 * z)) < 1e-9
        assert abs(math.cos(x + y) + math.cos(y + z) + math.cos(z + x)) < 1e-9
    t = sp.symbols("t")
    assert sp.simplify(cos(t + 2 * pi / 3) + cos(t - 2 * pi / 3) + cos(t)) == 0
    # 「2乗して加える」と z が消える
    for _ in range(100):
        x, y = rnd.uniform(-5, 5), rnd.uniform(-5, 5)
        assert abs((math.sin(x) + math.sin(y))**2 + (math.cos(x) + math.cos(y))**2 - 2 - 2 * math.cos(x - y)) < 1e-12


# ---------------------------------------------------------------- 節6
SEC.append({"title": "2倍角・半角・3倍角の公式",
"base": r"""・2倍角：$\sin2\alpha=2\sin\alpha\cos\alpha$，$\cos2\alpha=\cos^2\alpha-\sin^2\alpha=1-2\sin^2\alpha=2\cos^2\alpha-1$，$\tan2\alpha=\dfrac{2\tan\alpha}{1-\tan^2\alpha}$<br>
・半角：$\sin^2\dfrac{\alpha}{2}=\dfrac{1-\cos\alpha}{2}$，$\cos^2\dfrac{\alpha}{2}=\dfrac{1+\cos\alpha}{2}$，$\tan^2\dfrac{\alpha}{2}=\dfrac{1-\cos\alpha}{1+\cos\alpha}$<br>
・3倍角：$\sin3\alpha=3\sin\alpha-4\sin^3\alpha$，$\cos3\alpha=4\cos^3\alpha-3\cos\alpha$<br>
・次数下げ：$\sin^2\alpha=\dfrac{1-\cos2\alpha}{2}$，$\cos^2\alpha=\dfrac{1+\cos2\alpha}{2}$，$\sin\alpha\cos\alpha=\dfrac12\sin2\alpha$""",
"items": [
 {"lv": 1, "title": "2倍角・半角の公式による値の計算",
  "q": r"(1) $\dfrac{\pi}{2}<\alpha<\pi$，$\sin\alpha=\dfrac35$ のとき，$\sin2\alpha$，$\cos2\alpha$，$\sin\dfrac{\alpha}{2}$ の値を求めよ。<br>(2) $\cos\dfrac{\pi}{8}$ の値を求めよ。",
  "hint": r"2倍角の公式は加法定理で $\beta=\alpha$ としたもの。半角の公式は2乗の値を与えるので，$\dfrac{\alpha}{2}$ の範囲から符号を決める。",
  "sol": r"(1) $\dfrac{\pi}{2}<\alpha<\pi$ より $\cos\alpha<0$ で，$\cos\alpha=-\dfrac45$。<br>"
         r"$\sin2\alpha=2\sin\alpha\cos\alpha=2\cdot\dfrac35\cdot\left(-\dfrac45\right)=\boldsymbol{-\dfrac{24}{25}}$，$\cos2\alpha=1-2\sin^2\alpha=1-\dfrac{18}{25}=\boldsymbol{\dfrac{7}{25}}$<br>"
         r"$\sin^2\dfrac{\alpha}{2}=\dfrac{1-\cos\alpha}{2}=\dfrac{1+\frac45}{2}=\dfrac{9}{10}$。$\dfrac{\pi}{4}<\dfrac{\alpha}{2}<\dfrac{\pi}{2}$ より $\sin\dfrac{\alpha}{2}>0$ だから　$\sin\dfrac{\alpha}{2}=\dfrac{3}{\sqrt{10}}=\boldsymbol{\dfrac{3\sqrt{10}}{10}}$<br>"
         r"(2) $\cos^2\dfrac{\pi}{8}=\dfrac{1+\cos\frac{\pi}{4}}{2}=\dfrac{2+\sqrt2}{4}$。$\cos\dfrac{\pi}{8}>0$ より　$\cos\dfrac{\pi}{8}=\boldsymbol{\dfrac{\sqrt{2+\sqrt2}}{2}}$",
  "note": r"同様に $\sin\dfrac{\pi}{8}=\dfrac{\sqrt{2-\sqrt2}}{2}$。$\tan\dfrac{\alpha}{2}=\dfrac{\sin\alpha}{1+\cos\alpha}$（分母分子を $2\cos^2\dfrac{\alpha}{2}$ で表すと分かる）を使うと，$\tan\dfrac{\pi}{8}=\dfrac{\frac{\sqrt2}{2}}{1+\frac{\sqrt2}{2}}=\sqrt2-1$ と2重根号なしで求まる。",
  "ex": r"(1) $\pi<\alpha<\dfrac32\pi$，$\cos\alpha=-\dfrac13$ のとき，$\sin2\alpha$，$\cos2\alpha$，$\cos\dfrac{\alpha}{2}$ の値を求めよ。<br>(2) $\tan\dfrac{\pi}{12}$ の値を求めよ。",
  "exa": r"(1) $\sin2\alpha=\dfrac{4\sqrt2}{9}$，$\cos2\alpha=-\dfrac79$，$\cos\dfrac{\alpha}{2}=-\dfrac{\sqrt3}{3}$　(2) $2-\sqrt3$"},
 {"lv": 2, "title": "2倍角を含む方程式・不等式",
  "q": r"$0\leqq\theta<2\pi$ のとき，次の方程式・不等式を解け。<br>(1) $\sin2\theta=\sin\theta$　　(2) $\cos2\theta+3\cos\theta+2>0$",
  "hint": r"2倍角の公式で角を $\theta$ にそろえる。(1) は $\sin\theta$ でくくって積の形に，(2) は $\cos2\theta=2\cos^2\theta-1$ として $\cos\theta$ の2次不等式にする。",
  "sol": r"(1) $2\sin\theta\cos\theta-\sin\theta=0$ より $\sin\theta(2\cos\theta-1)=0$。<br>"
         r"$\sin\theta=0$ より $\theta=0,\ \pi$。$\cos\theta=\dfrac12$ より $\theta=\dfrac{\pi}{3},\ \dfrac53\pi$。よって　$\boldsymbol{\theta=0,\ \dfrac{\pi}{3},\ \pi,\ \dfrac53\pi}$<br>"
         r"(2) $2\cos^2\theta-1+3\cos\theta+2>0$ より $2\cos^2\theta+3\cos\theta+1>0$，$(2\cos\theta+1)(\cos\theta+1)>0$。<br>"
         r"$\cos\theta+1\geqq0$ だから，成り立つのは $\cos\theta+1>0$ かつ $2\cos\theta+1>0$，すなわち $\cos\theta>-\dfrac12$ のとき。<br>"
         r"よって　$\boldsymbol{0\leqq\theta<\dfrac23\pi,\ \dfrac43\pi<\theta<2\pi}$",
  "note": r"(1) で両辺を $\sin\theta$ で割ると $\sin\theta=0$ の解を落とす。割る代わりにくくり出して積の形にするのが原則。",
  "ex": r"$0\leqq\theta<2\pi$ のとき，次の方程式・不等式を解け。<br>(1) $\cos2\theta=\cos\theta$　　(2) $\cos2\theta<3\sin\theta+2$",
  "exa": r"(1) $\theta=0,\ \dfrac23\pi,\ \dfrac43\pi$　(2) $0\leqq\theta<\dfrac76\pi,\ \dfrac{11}{6}\pi<\theta<2\pi$"},
 {"lv": 3, "title": "3倍角の公式とその利用",
  "q": r"(1) 加法定理を用いて，$\cos3\theta=4\cos^3\theta-3\cos\theta$ を証明せよ。<br>(2) $0\leqq\theta<2\pi$ のとき，方程式 $\cos3\theta+\cos2\theta+\cos\theta+1=0$ を解け。",
  "hint": r"(1) $3\theta=2\theta+\theta$ として加法定理を使い，さらに2倍角の公式で $\cos\theta$ だけの式にする。(2) すべて $\cos\theta$ で表すと $\cos\theta$ の3次方程式になり，因数分解できる。",
  "sol": r"(1) $\cos3\theta=\cos(2\theta+\theta)=\cos2\theta\cos\theta-\sin2\theta\sin\theta$<br>"
         r"$=(2\cos^2\theta-1)\cos\theta-2\sin^2\theta\cos\theta=(2\cos^2\theta-1)\cos\theta-2(1-\cos^2\theta)\cos\theta=4\cos^3\theta-3\cos\theta$　$\blacksquare$<br>"
         r"(2) $c=\cos\theta$ とおくと　$(4c^3-3c)+(2c^2-1)+c+1=0$，すなわち $4c^3+2c^2-2c=0$<br>"
         r"$2c(2c^2+c-1)=0$，$2c(2c-1)(c+1)=0$ より　$c=0,\ \dfrac12,\ -1$<br>"
         r"$\cos\theta=0$ より $\theta=\dfrac{\pi}{2},\ \dfrac32\pi$，$\cos\theta=\dfrac12$ より $\theta=\dfrac{\pi}{3},\ \dfrac53\pi$，$\cos\theta=-1$ より $\theta=\pi$。<br>"
         r"よって　$\boldsymbol{\theta=\dfrac{\pi}{3},\ \dfrac{\pi}{2},\ \pi,\ \dfrac32\pi,\ \dfrac53\pi}$",
  "note": r"同様に $\sin3\theta=\sin(2\theta+\theta)=3\sin\theta-4\sin^3\theta$ が導ける。$\cos3\theta$ は $\cos\theta$ だけの，$\sin3\theta$ は $\sin\theta$ だけの3次式になる。",
  "ex": r"$0\leqq\theta<2\pi$ のとき，方程式 $\cos3\theta+\cos\theta=0$ を解け。",
  "exa": r"$\theta=\dfrac{\pi}{4},\ \dfrac{\pi}{2},\ \dfrac34\pi,\ \dfrac54\pi,\ \dfrac32\pi,\ \dfrac74\pi$"},
 {"lv": 3, "title": r"$\cos\dfrac{\pi}{5}$ の値",
  "q": r"$\cos\dfrac{\pi}{5}$ の値を求めよ。",
  "hint": r"$\theta=\dfrac{\pi}{5}$ とおくと $5\theta=\pi$，すなわち $3\theta=\pi-2\theta$ なので $\sin3\theta=\sin2\theta$。3倍角・2倍角の公式で展開し，$\cos\theta$ の2次方程式を導く。",
  "sol": r"$\theta=\dfrac{\pi}{5}$ とおくと $3\theta=\pi-2\theta$ だから　$\sin3\theta=\sin(\pi-2\theta)=\sin2\theta$<br>"
         r"$3\sin\theta-4\sin^3\theta=2\sin\theta\cos\theta$。$\sin\theta\neq0$ だから両辺を $\sin\theta$ で割って $3-4\sin^2\theta=2\cos\theta$<br>"
         r"$3-4(1-\cos^2\theta)=2\cos\theta$ より　$4\cos^2\theta-2\cos\theta-1=0$，$\cos\theta=\dfrac{1\pm\sqrt5}{4}$<br>"
         r"$\cos\theta>0$ だから　$\cos\dfrac{\pi}{5}=\boldsymbol{\dfrac{1+\sqrt5}{4}}$",
  "note": r"$\cos\dfrac25\pi=2\cos^2\dfrac{\pi}{5}-1=\dfrac{\sqrt5-1}{4}$ も得られる。正五角形の対角線と1辺の長さの比（黄金比）$\dfrac{1+\sqrt5}{2}$ は $2\cos\dfrac{\pi}{5}$ に等しい。",
  "ex": r"$\sin\dfrac{\pi}{10}$ の値を求めよ。",
  "exa": r"$\dfrac{\sqrt5-1}{4}$（$\theta=\dfrac{\pi}{10}$ とすると $2\theta=\dfrac{\pi}{2}-3\theta$ より $\sin2\theta=\cos3\theta$）"},
 {"lv": 4, "title": "3倍角の公式で3次方程式を解く",
  "q": r"(1) 3次方程式 $8x^3-6x-1=0$ の解は $x=\cos\dfrac{\pi}{9},\ \cos\dfrac59\pi,\ \cos\dfrac79\pi$ であることを示せ。<br>"
       r"(2) $\cos\dfrac{\pi}{9}\cos\dfrac29\pi\cos\dfrac49\pi$ の値，および $\cos\dfrac{\pi}{9}-\cos\dfrac29\pi-\cos\dfrac49\pi$ の値を求めよ。",
  "hint": r"$x=\cos\theta$ を代入すると $8x^3-6x=2(4\cos^3\theta-3\cos\theta)=2\cos3\theta$。3つの値が解であることと，それらが互いに異なることを示せば，3次方程式の解はそれで全部である。(2) は解と係数の関係。",
  "sol": r"(1) $x=\cos\theta$ とすると　$8x^3-6x-1=2(4\cos^3\theta-3\cos\theta)-1=2\cos3\theta-1$<br>"
         r"$\theta=\dfrac{\pi}{9},\ \dfrac59\pi,\ \dfrac79\pi$ のとき $3\theta=\dfrac{\pi}{3},\ \dfrac53\pi,\ \dfrac73\pi$ で，いずれも $\cos3\theta=\dfrac12$。よって $\cos\dfrac{\pi}{9},\ \cos\dfrac59\pi,\ \cos\dfrac79\pi$ はすべて解である。<br>"
         r"$0<\dfrac{\pi}{9}<\dfrac59\pi<\dfrac79\pi<\pi$ で，$\cos\theta$ は $0\leqq\theta\leqq\pi$ で減少するから，この3つの値は互いに異なる。3次方程式の解は高々3個なので，解はこの3つである。$\blacksquare$<br>"
         r"(2) 解と係数の関係より　$\cos\dfrac{\pi}{9}+\cos\dfrac59\pi+\cos\dfrac79\pi=0$，$\cos\dfrac{\pi}{9}\cos\dfrac59\pi\cos\dfrac79\pi=\dfrac18$<br>"
         r"$\cos\dfrac59\pi=\cos\left(\pi-\dfrac49\pi\right)=-\cos\dfrac49\pi$，$\cos\dfrac79\pi=-\cos\dfrac29\pi$ だから<br>"
         r"$\cos\dfrac{\pi}{9}\cos\dfrac29\pi\cos\dfrac49\pi=\boldsymbol{\dfrac18}$，$\cos\dfrac{\pi}{9}-\cos\dfrac29\pi-\cos\dfrac49\pi=\boldsymbol{0}$",
  "note": r"一般に $x=\cos\theta$ とおくと $4x^3-3x=\cos3\theta$ なので，$4x^3-3x=k$（$-1<k<1$）の形の3次方程式は三角関数で解ける。積の値は，$8\sin\dfrac{\pi}{9}$ を掛けて2倍角の公式を3回使い $\sin\dfrac89\pi=\sin\dfrac{\pi}{9}$ に帰着させても求まる。",
  "ex": r"3次方程式 $x^3-3x+1=0$ の3つの解を，三角関数を用いて表せ。",
  "exa": r"$2\cos\dfrac29\pi,\ 2\cos\dfrac49\pi,\ 2\cos\dfrac89\pi$"},
 {"lv": 4, "title": r"すべての $\theta$ で成り立つ不等式と係数の最大",
  "q": r"すべての実数 $\theta$ に対して $1+a\cos\theta+b\cos2\theta\geqq0$ が成り立つような実数の組 $(a,\ b)$ を考える。<br>(1) $a$ の最大値を求めよ。　(2) $a+b$ の最大値を求めよ。",
  "hint": r"$t=\cos\theta$ とおくと，条件は「$-1\leqq t\leqq1$ で $f(t)=2bt^2+at+1-b\geqq0$」。最大のときは $f(t)$ のグラフが区間内で $t$ 軸に接すると予想できる。うまい $t$ を代入した必要条件で上から抑え，等号が成り立つ例を示す。",
  "sol": r"$t=\cos\theta$ とおくと $\cos2\theta=2t^2-1$ で，$t$ は $-1\leqq t\leqq1$ のすべての値をとる。条件は<br>"
         r"$-1\leqq t\leqq1$ のすべての $t$ で　$f(t)=1+at+b(2t^2-1)\geqq0$ …(*)<br>"
         r"(1) (*) で $t=-\dfrac{1}{\sqrt2}$ とすると $2t^2-1=0$ だから $1-\dfrac{a}{\sqrt2}\geqq0$，すなわち $a\leqq\sqrt2$。<br>"
         r"逆に $a=\sqrt2$，$b=\dfrac12$ のとき $f(t)=t^2+\sqrt2t+\dfrac12=\left(t+\dfrac{1}{\sqrt2}\right)^2\geqq0$ で (*) が成り立つ。よって $a$ の最大値は　$\boldsymbol{\sqrt2}$<br>"
         r"(2) (*) で $t=-\dfrac12$ とすると $2t^2-1=-\dfrac12$ だから $1-\dfrac{a}{2}-\dfrac{b}{2}\geqq0$，すなわち $a+b\leqq2$。<br>"
         r"逆に $a=\dfrac43$，$b=\dfrac23$ のとき $f(t)=\dfrac43t^2+\dfrac43t+\dfrac13=\dfrac13(2t+1)^2\geqq0$ で (*) が成り立つ。よって $a+b$ の最大値は　$\boldsymbol{2}$",
  "note": r"代入する $t$ の見つけ方：$f(t)$ が $t=t_0$ で $t$ 軸に接するとき，$f(t_0)\geqq0$ すなわち $1+at_0+b(2t_0^2-1)\geqq0$ が $a,\ b$ の1次不等式になり，等号が成り立つ。これが目的の式（$a$ や $a+b$）の定数倍の形になるように $t_0$ を選ぶ（(1) は $2t_0^2-1=0$，(2) は $t_0=2t_0^2-1$ の負の解）。軸の位置で場合分けして点 $(a,\ b)$ の存在範囲を求める方法もあるが，計算量が多い。",
  "ex": r"例題と同じ条件のもとで，$3a+7b$ の最大値を求めよ。",
  "exa": r"$9$（$t=-\dfrac13$ を代入して $3a+7b\leqq9$。等号は $a=\dfrac{12}{11},\ b=\dfrac{9}{11}$ のとき）"},
 {"lv": 5, "title": r"$\sin1^\circ$ が無理数であることの証明",
  "q": r"$\sin1^\circ$ は無理数であることを証明せよ。",
  "hint": r"背理法。有理数どうしの和・差・積は有理数なので，$\sin1^\circ$ が有理数なら，2倍角・3倍角の公式で次々に有理数となる角が増える。値の分かっている無理数（$\cos36^\circ$ など）に到達させれば矛盾。",
  "sol": r"$\sin1^\circ$ が有理数であると仮定する。<br>"
         r"2倍角の公式より $\cos2^\circ=1-2\sin^21^\circ$ は有理数。<br>"
         r"3倍角の公式より $\cos6^\circ=4\cos^32^\circ-3\cos2^\circ$ は有理数，さらに $\cos18^\circ=4\cos^36^\circ-3\cos6^\circ$ も有理数。<br>"
         r"2倍角の公式より $\cos36^\circ=2\cos^218^\circ-1$ も有理数となる。<br>"
         r"一方，$\theta=36^\circ$ とすると $5\theta=180^\circ$ より $\sin3\theta=\sin(180^\circ-2\theta)=\sin2\theta$。<br>"
         r"$3\sin\theta-4\sin^3\theta=2\sin\theta\cos\theta$ で $\sin\theta\neq0$ だから $3-4(1-\cos^2\theta)=2\cos\theta$，すなわち $4\cos^2\theta-2\cos\theta-1=0$。$\cos\theta>0$ より $\cos36^\circ=\dfrac{1+\sqrt5}{4}$。<br>"
         r"ここで $\sqrt5$ は無理数である（$\sqrt5=\dfrac{m}{n}$（$m,\ n$ は互いに素な正の整数）とすると $m^2=5n^2$ より $m$ は $5$ の倍数，$m=5k$ とおくと $n^2=5k^2$ より $n$ も $5$ の倍数となり矛盾）。<br>"
         r"$\cos36^\circ=q$（有理数）とすると $\sqrt5=4q-1$ が有理数となり矛盾する。<br>"
         r"よって仮定は誤りで，$\sin1^\circ$ は無理数である。$\blacksquare$",
  "note": r"鍵は「どの角の三角関数なら値（無理数）が分かるか」を見定め，$1^\circ\to2^\circ\to6^\circ\to18^\circ\to36^\circ$ と，有理数であることを伝えていく経路を見つけること。$\cos(n+1)x=2\cos x\cos nx-\cos(n-1)x$（加法定理）をくり返して $\cos30^\circ=\dfrac{\sqrt3}{2}$ に到達させる方法もある。",
  "ex": r"$\sin5^\circ$ は無理数であることを証明せよ。",
  "exa": r"有理数と仮定すると $\cos10^\circ=1-2\sin^25^\circ$，$\cos30^\circ=4\cos^310^\circ-3\cos10^\circ$ が順に有理数となり，$\cos30^\circ=\dfrac{\sqrt3}{2}$ が無理数であることに矛盾する"},
]})


@_v
def _v6():
    import sympy as sp
    import numpy as np
    from sympy import sin, cos, tan, pi, sqrt, Rational as R
    P = math.pi
    a = P - math.asin(3 / 5)
    assert abs(math.sin(2 * a) + 24 / 25) < 1e-12 and abs(math.cos(2 * a) - 7 / 25) < 1e-12 and abs(math.sin(a / 2) - 3 * math.sqrt(10) / 10) < 1e-12
    _eq(cos(pi / 8), sqrt(2 + sqrt(2)) / 2); _eq(sin(pi / 8), sqrt(2 - sqrt(2)) / 2); _eq(tan(pi / 8), sqrt(2) - 1)
    _eq((sqrt(2) / 2) / (1 + sqrt(2) / 2), sqrt(2) - 1)
    a = P + math.acos(1 / 3)                                   # π<α<3π/2, cos α = -1/3
    assert abs(math.cos(a) + 1 / 3) < 1e-12 and P < a < 1.5 * P
    assert abs(math.sin(2 * a) - 4 * math.sqrt(2) / 9) < 1e-12 and abs(math.cos(2 * a) + 7 / 9) < 1e-12 and abs(math.cos(a / 2) + math.sqrt(3) / 3) < 1e-12
    _eq(tan(pi / 12), 2 - sqrt(3))
    _same_roots(lambda t: math.sin(2 * t) - math.sin(t), [0, P / 3, P, 5 * P / 3])
    _same_set(lambda t: math.cos(2 * t) + 3 * math.cos(t) + 2 > 0, [(-1, 2 * P / 3), (4 * P / 3, 3 * P)])
    _same_roots(lambda t: math.cos(2 * t) - math.cos(t), [0, 2 * P / 3, 4 * P / 3])
    _same_set(lambda t: math.cos(2 * t) < 3 * math.sin(t) + 2, [(-1, 7 * P / 6), (11 * P / 6, 3 * P)])
    th = sp.symbols("theta")
    assert sp.simplify(sp.expand_trig(cos(3 * th)) - (4 * cos(th)**3 - 3 * cos(th))) == 0
    assert sp.simplify(sp.expand_trig(sin(3 * th)) - (3 * sin(th) - 4 * sin(th)**3)) == 0
    c = sp.symbols("c")
    assert sp.expand(2 * c * (2 * c - 1) * (c + 1)) == sp.expand((4 * c**3 - 3 * c) + (2 * c**2 - 1) + c + 1)
    _same_roots(lambda t: math.cos(3 * t) + math.cos(2 * t) + math.cos(t) + 1, [P / 3, P / 2, P, 3 * P / 2, 5 * P / 3])
    _same_roots(lambda t: math.cos(3 * t) + math.cos(t), [P / 4, P / 2, 3 * P / 4, 5 * P / 4, 3 * P / 2, 7 * P / 4])
    _eq(cos(pi / 5), (1 + sqrt(5)) / 4); _eq(cos(2 * pi / 5), (sqrt(5) - 1) / 4); _eq(sin(pi / 10), (sqrt(5) - 1) / 4)
    assert sp.expand(4 * ((1 + sqrt(5)) / 4)**2 - 2 * (1 + sqrt(5)) / 4 - 1) == 0
    s = (sqrt(5) - 1) / 4
    assert sp.expand(2 * s - (4 * (1 - s**2) - 3)) == 0                 # sin2θ=cos3θ を cosθ で割った式
    # 3次方程式
    x = sp.symbols("x")
    for t in (pi / 9, 5 * pi / 9, 7 * pi / 9):
        _eq(8 * cos(t)**3 - 6 * cos(t) - 1, 0)
    _eq(cos(pi / 9) * cos(2 * pi / 9) * cos(4 * pi / 9), R(1, 8)); _eq(cos(pi / 9) - cos(2 * pi / 9) - cos(4 * pi / 9), 0)
    for t in (2 * pi / 9, 4 * pi / 9, 8 * pi / 9):
        _eq((2 * cos(t))**3 - 3 * 2 * cos(t) + 1, 0)
    assert len({round(math.cos(k * P / 9), 9) for k in (2, 4, 8)}) == 3
    # 1 + a cosθ + b cos2θ ≥ 0：t の格子で線形計画を近似
    T = np.linspace(-1, 1, 4001)
    def best(cx, cy):
        m = -1e9
        for b in np.linspace(-1.2, 1.2, 4801):
            g = 1 + b * (2 * T**2 - 1)
            pos, neg = T > 1e-12, T < -1e-12
            if np.any(g[np.abs(T) <= 1e-12] < 0):
                continue
            lo = np.max(-g[pos] / T[pos]); hi = np.min(g[neg] / (-T[neg]))
            if lo <= hi + 1e-12:
                m = max(m, cx * lo + cy * b, cx * hi + cy * b)
        return m
    assert abs(best(1, 0) - math.sqrt(2)) < 2e-3 and abs(best(1, 1) - 2) < 2e-3 and abs(best(3, 7) - 9) < 5e-3
    tt = sp.symbols("t")
    assert sp.expand(1 + sqrt(2) * tt + R(1, 2) * (2 * tt**2 - 1) - (tt + 1 / sqrt(2))**2) == 0
    assert sp.expand(1 + R(4, 3) * tt + R(2, 3) * (2 * tt**2 - 1) - R(1, 3) * (2 * tt + 1)**2) == 0
    assert sp.expand(1 + R(12, 11) * tt + R(9, 11) * (2 * tt**2 - 1) - R(2, 11) * (3 * tt + 1)**2) == 0
    assert 3 * R(12, 11) + 7 * R(9, 11) == 9
    aa, bb = sp.symbols("a b")
    assert sp.expand(9 * (1 + aa * R(-1, 3) + bb * (2 * R(1, 9) - 1))) == 9 - 3 * aa - 7 * bb      # t=-1/3 の代入
    assert sp.expand(2 * (1 + aa * R(-1, 2) + bb * (2 * R(1, 4) - 1))) == 2 - aa - bb              # t=-1/2 の代入
    # sin1° の経路
    d = lambda k: pi * k / 180
    _eq(cos(d(2)), 1 - 2 * sin(d(1))**2); _eq(cos(d(6)), 4 * cos(d(2))**3 - 3 * cos(d(2)))
    _eq(cos(d(18)), 4 * cos(d(6))**3 - 3 * cos(d(6))); _eq(cos(d(36)), 2 * cos(d(18))**2 - 1)
    _eq(cos(d(36)), (1 + sqrt(5)) / 4)
    _eq(cos(d(10)), 1 - 2 * sin(d(5))**2); _eq(cos(d(30)), 4 * cos(d(10))**3 - 3 * cos(d(10)))


# ---------------------------------------------------------------- 節7
SEC.append({"title": "三角関数の合成",
"base": r"""・$a\sin\theta+b\cos\theta=\sqrt{a^2+b^2}\sin(\theta+\alpha)$　ただし $\cos\alpha=\dfrac{a}{\sqrt{a^2+b^2}}$，$\sin\alpha=\dfrac{b}{\sqrt{a^2+b^2}}$（$\alpha$ は点 $(a,\ b)$ の動径の表す角）<br>
・$\theta$ に制限がなければ，最大値は $\sqrt{a^2+b^2}$，最小値は $-\sqrt{a^2+b^2}$。制限があるときは $\theta+\alpha$ の変域で考える<br>
・$\sin^2\theta$，$\sin\theta\cos\theta$，$\cos^2\theta$ の2次式は，次数下げの公式で $\sin2\theta,\ \cos2\theta$ の1次式にしてから合成する""",
"items": [
 {"lv": 1, "title": "三角関数の合成",
  "q": r"次の式を $r\sin(\theta+\alpha)$（$r>0$，$-\pi<\alpha\leqq\pi$）の形に表せ。ただし，(3) の $\alpha$ は $\cos\alpha,\ \sin\alpha$ の値で示せ。<br>"
       r"(1) $\sqrt3\sin\theta+\cos\theta$　　(2) $\sin\theta-\cos\theta$　　(3) $3\sin\theta+4\cos\theta$",
  "hint": r"$a\sin\theta+b\cos\theta$ の係数を座標とする点 $(a,\ b)$ をとり，原点からの距離 $r=\sqrt{a^2+b^2}$ と，動径の表す角 $\alpha$ を読む。",
  "sol": r"(1) 点 $(\sqrt3,\ 1)$ について $r=\sqrt{3+1}=2$，$\cos\alpha=\dfrac{\sqrt3}{2}$，$\sin\alpha=\dfrac12$ より $\alpha=\dfrac{\pi}{6}$。<br>"
         r"$\sqrt3\sin\theta+\cos\theta=2\left(\sin\theta\cos\dfrac{\pi}{6}+\cos\theta\sin\dfrac{\pi}{6}\right)=\boldsymbol{2\sin\left(\theta+\dfrac{\pi}{6}\right)}$<br>"
         r"(2) 点 $(1,\ -1)$ について $r=\sqrt2$，$\alpha=-\dfrac{\pi}{4}$。よって　$\boldsymbol{\sqrt2\sin\left(\theta-\dfrac{\pi}{4}\right)}$<br>"
         r"(3) 点 $(3,\ 4)$ について $r=\sqrt{9+16}=5$。よって　$\boldsymbol{5\sin(\theta+\alpha)}$　ただし $\boldsymbol{\cos\alpha=\dfrac35,\ \sin\alpha=\dfrac45}$",
  "note": r"$a\sin\theta+b\cos\theta=r(\sin\theta\cos\alpha+\cos\theta\sin\alpha)$ と，加法定理を逆向きに使っている。$\cos$ でまとめることもでき，$a\sin\theta+b\cos\theta=r\cos(\theta-\beta)$（$\cos\beta=\dfrac{b}{r}$，$\sin\beta=\dfrac{a}{r}$）となる。",
  "ex": r"次の式を $r\sin(\theta+\alpha)$（$r>0$，$-\pi<\alpha\leqq\pi$）の形に表せ。ただし，(3) の $\alpha$ は $\cos\alpha,\ \sin\alpha$ の値で示せ。<br>(1) $\sin\theta-\sqrt3\cos\theta$　　(2) $-\sin\theta+\cos\theta$　　(3) $5\sin\theta-12\cos\theta$",
  "exa": r"(1) $2\sin\left(\theta-\dfrac{\pi}{3}\right)$　(2) $\sqrt2\sin\left(\theta+\dfrac34\pi\right)$　(3) $13\sin(\theta+\alpha)$（$\cos\alpha=\dfrac{5}{13}$，$\sin\alpha=-\dfrac{12}{13}$）"},
 {"lv": 2, "title": "合成の利用（方程式・不等式・最大最小）",
  "q": r"(1) $0\leqq\theta<2\pi$ のとき，方程式 $\sin\theta+\sqrt3\cos\theta=1$ を解け。<br>"
       r"(2) $0\leqq\theta<2\pi$ のとき，不等式 $\sin\theta-\cos\theta\geqq1$ を解け。<br>"
       r"(3) 関数 $y=\sin\theta+\sqrt3\cos\theta$（$0\leqq\theta\leqq\pi$）の最大値と最小値を求めよ。",
  "hint": r"合成して $\sin$ 1つにまとめれば，$2\theta+\alpha$ の形の角を含む方程式と同じように，まず $\theta+\alpha$ の変域を求めて解ける。",
  "sol": r"(1) $2\sin\left(\theta+\dfrac{\pi}{3}\right)=1$ より $\sin\left(\theta+\dfrac{\pi}{3}\right)=\dfrac12$。$\dfrac{\pi}{3}\leqq\theta+\dfrac{\pi}{3}<\dfrac73\pi$ より $\theta+\dfrac{\pi}{3}=\dfrac56\pi,\ \dfrac{13}{6}\pi$。<br>"
         r"よって　$\boldsymbol{\theta=\dfrac{\pi}{2},\ \dfrac{11}{6}\pi}$<br>"
         r"(2) $\sqrt2\sin\left(\theta-\dfrac{\pi}{4}\right)\geqq1$ より $\sin\left(\theta-\dfrac{\pi}{4}\right)\geqq\dfrac{1}{\sqrt2}$。$-\dfrac{\pi}{4}\leqq\theta-\dfrac{\pi}{4}<\dfrac74\pi$ より $\dfrac{\pi}{4}\leqq\theta-\dfrac{\pi}{4}\leqq\dfrac34\pi$。<br>"
         r"よって　$\boldsymbol{\dfrac{\pi}{2}\leqq\theta\leqq\pi}$<br>"
         r"(3) $y=2\sin\left(\theta+\dfrac{\pi}{3}\right)$。$\dfrac{\pi}{3}\leqq\theta+\dfrac{\pi}{3}\leqq\dfrac43\pi$ より $-\dfrac{\sqrt3}{2}\leqq\sin\left(\theta+\dfrac{\pi}{3}\right)\leqq1$。<br>"
         r"よって　$\boldsymbol{\theta=\dfrac{\pi}{6}}$ のとき最大値 $\boldsymbol{2}$，$\boldsymbol{\theta=\pi}$ のとき最小値 $\boldsymbol{-\sqrt3}$",
  "note": r"(3) で $\theta$ に制限がなければ最小値は $-2$ だが，ここでは $\theta+\dfrac{\pi}{3}=\dfrac32\pi$ となる $\theta$ が変域にないので，端 $\theta=\pi$ で最小になる。",
  "ex": r"(1) $0\leqq\theta<2\pi$ のとき，方程式 $\sqrt3\sin\theta-\cos\theta=\sqrt2$ を解け。<br>(2) $0\leqq\theta<2\pi$ のとき，不等式 $\sin\theta+\cos\theta<1$ を解け。<br>(3) 関数 $y=\sqrt3\sin\theta-\cos\theta$（$0\leqq\theta\leqq\pi$）の最大値と最小値を求めよ。",
  "exa": r"(1) $\theta=\dfrac{5}{12}\pi,\ \dfrac{11}{12}\pi$　(2) $\dfrac{\pi}{2}<\theta<2\pi$　(3) $\theta=\dfrac23\pi$ で最大値 $2$，$\theta=0$ で最小値 $-1$"},
 {"lv": 3, "title": "合成した角が具体的に求まらない場合の最大・最小",
  "q": r"関数 $y=3\sin\theta+4\cos\theta$（$0\leqq\theta\leqq\dfrac{\pi}{2}$）の最大値と最小値を求めよ。",
  "hint": r"$5\sin(\theta+\alpha)$ と合成すると $\alpha$ は具体的な角にならない。$\alpha$ のおよその範囲（$0<\alpha<\dfrac{\pi}{2}$）を押さえ，$\theta+\alpha$ の変域の端での $\sin$ の値を $\sin\alpha,\ \cos\alpha$ で表して比べる。",
  "sol": r"$y=5\sin(\theta+\alpha)$　ただし $\cos\alpha=\dfrac35$，$\sin\alpha=\dfrac45$，$0<\alpha<\dfrac{\pi}{2}$。<br>"
         r"$0\leqq\theta\leqq\dfrac{\pi}{2}$ より $\alpha\leqq\theta+\alpha\leqq\alpha+\dfrac{\pi}{2}$ で，$\alpha<\dfrac{\pi}{2}<\alpha+\dfrac{\pi}{2}$ だからこの範囲は $\dfrac{\pi}{2}$ を含む。<br>"
         r"よって $\theta+\alpha=\dfrac{\pi}{2}$ のとき最大値 $5$ をとる。<br>"
         r"$\sin u$ は $\alpha\leqq u\leqq\dfrac{\pi}{2}$ で増加し，$\dfrac{\pi}{2}\leqq u\leqq\alpha+\dfrac{\pi}{2}$ で減少するから，最小値は端点でとる。<br>"
         r"$\sin\alpha=\dfrac45$，$\sin\left(\alpha+\dfrac{\pi}{2}\right)=\cos\alpha=\dfrac35$ だから，最小値は $5\cdot\dfrac35=3$（$\theta=\dfrac{\pi}{2}$ のとき）。<br>"
         r"答　<b>最大値 $\boldsymbol{5}$</b>（$\sin\theta=\dfrac35,\ \cos\theta=\dfrac45$ のとき），<b>最小値 $\boldsymbol{3}$</b>（$\theta=\dfrac{\pi}{2}$ のとき）",
  "note": r"最大値をとる $\theta=\dfrac{\pi}{2}-\alpha$ は具体的な角でないので，$\sin\theta=\cos\alpha=\dfrac35$，$\cos\theta=\sin\alpha=\dfrac45$ を満たす角として答える。最小値は，端点 $\theta=0,\ \dfrac{\pi}{2}$ での値 $4,\ 3$ を直接比べてもよい。",
  "ex": r"関数 $y=4\sin\theta-3\cos\theta$（$0\leqq\theta\leqq\pi$）の最大値と最小値を求めよ。",
  "exa": r"最大値 $5$（$\sin\theta=\dfrac45,\ \cos\theta=-\dfrac35$ のとき），最小値 $-3$（$\theta=0$ のとき）"},
 {"lv": 3, "title": r"$\sin\theta,\ \cos\theta$ の2次の同次式の最大・最小",
  "q": r"関数 $y=\sin^2\theta+2\sin\theta\cos\theta+3\cos^2\theta$（$0\leqq\theta\leqq\dfrac{\pi}{2}$）の最大値と最小値，およびそのときの $\theta$ の値を求めよ。",
  "hint": r"$\sin^2\theta=\dfrac{1-\cos2\theta}{2}$，$\cos^2\theta=\dfrac{1+\cos2\theta}{2}$，$\sin\theta\cos\theta=\dfrac12\sin2\theta$ で次数を下げると，$\sin2\theta$ と $\cos2\theta$ の1次式になり合成できる。",
  "sol": r"$y=\dfrac{1-\cos2\theta}{2}+\sin2\theta+\dfrac{3(1+\cos2\theta)}{2}=\sin2\theta+\cos2\theta+2=\sqrt2\sin\left(2\theta+\dfrac{\pi}{4}\right)+2$<br>"
         r"$0\leqq\theta\leqq\dfrac{\pi}{2}$ より $\dfrac{\pi}{4}\leqq2\theta+\dfrac{\pi}{4}\leqq\dfrac54\pi$ だから　$-\dfrac{1}{\sqrt2}\leqq\sin\left(2\theta+\dfrac{\pi}{4}\right)\leqq1$<br>"
         r"最大となるのは $2\theta+\dfrac{\pi}{4}=\dfrac{\pi}{2}$，最小となるのは $2\theta+\dfrac{\pi}{4}=\dfrac54\pi$ のとき。<br>"
         r"よって　$\boldsymbol{\theta=\dfrac{\pi}{8}}$ のとき最大値 $\boldsymbol{2+\sqrt2}$，$\boldsymbol{\theta=\dfrac{\pi}{2}}$ のとき最小値 $\boldsymbol{1}$",
  "note": r"$\sin\theta,\ \cos\theta$ の2次の同次式は，次数下げで必ず「$\sin2\theta,\ \cos2\theta$ の1次式＋定数」になる。角が $2\theta$ になるので，変域も2倍して考えることを忘れない。",
  "ex": r"関数 $y=3\sin^2\theta-2\sqrt3\sin\theta\cos\theta+\cos^2\theta$（$0\leqq\theta\leqq\pi$）の最大値と最小値，およびそのときの $\theta$ の値を求めよ。",
  "exa": r"$\theta=\dfrac23\pi$ のとき最大値 $4$，$\theta=\dfrac{\pi}{6}$ のとき最小値 $0$"},
 {"lv": 4, "title": "係数に文字を含む合成と最大・最小の場合分け",
  "q": r"$a$ を実数の定数とする。関数 $f(\theta)=\sin\theta+a\cos\theta$（$0\leqq\theta\leqq\dfrac{\pi}{3}$）の最大値 $M(a)$ と最小値 $m(a)$ を求めよ。",
  "hint": r"$f(\theta)=\sqrt{a^2+1}\sin(\theta+\alpha)$（$\tan\alpha=a$，$-\dfrac{\pi}{2}<\alpha<\dfrac{\pi}{2}$）と合成すると，$\alpha$ が $a$ とともに動く。変域 $\alpha\leqq\theta+\alpha\leqq\alpha+\dfrac{\pi}{3}$ に $\dfrac{\pi}{2}$ が入るかどうかで最大値を場合分けする。最小値は端点の値を比べる。",
  "sol": r"$r=\sqrt{a^2+1}$ とし，$\cos\alpha=\dfrac1r$，$\sin\alpha=\dfrac{a}{r}$ を満たす $\alpha$（$-\dfrac{\pi}{2}<\alpha<\dfrac{\pi}{2}$）をとると，$\tan\alpha=a$ で<br>"
         r"$f(\theta)=r\sin(\theta+\alpha)$，$u=\theta+\alpha$ の変域は $\alpha\leqq u\leqq\alpha+\dfrac{\pi}{3}$<br>"
         r"この区間は $-\dfrac{\pi}{2}<u<\dfrac56\pi$ に含まれる。$\sin u$ は $-\dfrac{\pi}{2}\leqq u\leqq\dfrac{\pi}{2}$ で増加，$\dfrac{\pi}{2}\leqq u\leqq\dfrac32\pi$ で減少する。<br>"
         r"【最大値】(i) $\alpha+\dfrac{\pi}{3}\geqq\dfrac{\pi}{2}$，すなわち $\alpha\geqq\dfrac{\pi}{6}$ のとき，区間は $u=\dfrac{\pi}{2}$ を含むから $M(a)=r$。<br>"
         r"(ii) $\alpha<\dfrac{\pi}{6}$ のとき，区間で $\sin u$ は増加するから $M(a)=f\left(\dfrac{\pi}{3}\right)=\dfrac{\sqrt3}{2}+\dfrac{a}{2}$。<br>"
         r"$\tan$ は $-\dfrac{\pi}{2}<\alpha<\dfrac{\pi}{2}$ で増加するので，$\alpha\geqq\dfrac{\pi}{6}\iff a\geqq\dfrac{1}{\sqrt3}$。<br>"
         r"【最小値】区間で $\sin u$ は「増加」または「増加してから減少」するから，最小値は端点でとる。<br>"
         r"$f(0)=a$，$f\left(\dfrac{\pi}{3}\right)=\dfrac{\sqrt3+a}{2}$ で，$\dfrac{\sqrt3+a}{2}-a=\dfrac{\sqrt3-a}{2}$ だから，$a\leqq\sqrt3$ なら $f(0)$ が小さい方。<br>"
         r"答　$a<\dfrac{1}{\sqrt3}$ のとき $\boldsymbol{M(a)=\dfrac{a+\sqrt3}{2}}$，$a\geqq\dfrac{1}{\sqrt3}$ のとき $\boldsymbol{M(a)=\sqrt{a^2+1}}$<br>"
         r"　　$a\leqq\sqrt3$ のとき $\boldsymbol{m(a)=a}$，$a>\sqrt3$ のとき $\boldsymbol{m(a)=\dfrac{a+\sqrt3}{2}}$",
  "note": r"合成した角 $\alpha$ が $a$ とともに動くので，「軸が動く2次関数の最大・最小」と同じく，頂点にあたる $\theta+\alpha=\dfrac{\pi}{2}$ が変域に入るかどうかで場合分けする。$a=\dfrac{1}{\sqrt3}$ では2つの式の値がともに $\dfrac{2}{\sqrt3}$ となり，$M(a)$ はつながっている。",
  "ex": r"$a>0$ とする。関数 $f(\theta)=a\sin\theta+\cos\theta$（$0\leqq\theta\leqq\dfrac{\pi}{2}$）の最大値と最小値を求めよ。",
  "exa": r"最大値 $\sqrt{a^2+1}$；最小値は $0<a\leqq1$ のとき $a$，$a\geqq1$ のとき $1$"},
]})


def _maxmin(g, lo, hi, N=200000):
    v = [g(lo + (hi - lo) * k / N) for k in range(N + 1)]
    return max(v), min(v)


@_v
def _v7():
    import sympy as sp
    from sympy import sin, cos, pi, sqrt
    P = math.pi
    t = sp.symbols("t", real=True)
    for lhs, rhs in [(sqrt(3) * sin(t) + cos(t), 2 * sin(t + pi / 6)), (sin(t) - cos(t), sqrt(2) * sin(t - pi / 4)),
                     (sin(t) - sqrt(3) * cos(t), 2 * sin(t - pi / 3)), (-sin(t) + cos(t), sqrt(2) * sin(t + 3 * pi / 4))]:
        assert sp.simplify(sp.expand_trig(lhs - rhs)) == 0
    al = math.atan2(4, 3); assert all(abs(3 * math.sin(x) + 4 * math.cos(x) - 5 * math.sin(x + al)) < 1e-12 for x in range(20))
    assert abs(math.cos(al) - 0.6) < 1e-12
    al = math.atan2(-12, 5); assert all(abs(5 * math.sin(x) - 12 * math.cos(x) - 13 * math.sin(x + al)) < 1e-12 for x in range(20))
    assert abs(math.cos(al) - 5 / 13) < 1e-12 and -P < al <= P
    _same_roots(lambda x: math.sin(x) + math.sqrt(3) * math.cos(x) - 1, [P / 2, 11 * P / 6])
    _same_set(lambda x: math.sin(x) - math.cos(x) >= 1, [(P / 2, P)])
    _eq(sin(pi / 2) - cos(pi / 2), 1); _eq(sin(pi) - cos(pi), 1)
    M, m = _maxmin(lambda x: math.sin(x) + math.sqrt(3) * math.cos(x), 0, P)
    assert abs(M - 2) < 1e-9 and abs(m + math.sqrt(3)) < 1e-9
    assert abs(math.sin(P / 6) + math.sqrt(3) * math.cos(P / 6) - 2) < 1e-12
    _same_roots(lambda x: math.sqrt(3) * math.sin(x) - math.cos(x) - math.sqrt(2), [5 * P / 12, 11 * P / 12])
    _same_set(lambda x: math.sin(x) + math.cos(x) < 1, [(P / 2, 2 * P)])
    assert not (math.sin(0) + math.cos(0) < 1)
    M, m = _maxmin(lambda x: math.sqrt(3) * math.sin(x) - math.cos(x), 0, P)
    assert abs(M - 2) < 1e-9 and abs(m + 1) < 1e-12
    assert abs(math.sqrt(3) * math.sin(2 * P / 3) - math.cos(2 * P / 3) - 2) < 1e-12
    # 3 sin + 4 cos
    M, m = _maxmin(lambda x: 3 * math.sin(x) + 4 * math.cos(x), 0, P / 2)
    assert abs(M - 5) < 1e-9 and abs(m - 3) < 1e-12
    x0 = math.asin(3 / 5); assert abs(3 * math.sin(x0) + 4 * math.cos(x0) - 5) < 1e-12
    M, m = _maxmin(lambda x: 4 * math.sin(x) - 3 * math.cos(x), 0, P)
    assert abs(M - 5) < 1e-9 and abs(m + 3) < 1e-12
    x0 = P - math.asin(4 / 5); assert abs(math.cos(x0) + 3 / 5) < 1e-12 and abs(4 * math.sin(x0) - 3 * math.cos(x0) - 5) < 1e-12
    # 同次式
    g = lambda x: math.sin(x)**2 + 2 * math.sin(x) * math.cos(x) + 3 * math.cos(x)**2
    assert all(abs(g(x) - (math.sqrt(2) * math.sin(2 * x + P / 4) + 2)) < 1e-12 for x in [0.1 * k for k in range(40)])
    M, m = _maxmin(g, 0, P / 2)
    assert abs(M - 2 - math.sqrt(2)) < 1e-9 and abs(m - 1) < 1e-12 and abs(g(P / 8) - 2 - math.sqrt(2)) < 1e-12 and abs(g(P / 2) - 1) < 1e-12
    g = lambda x: 3 * math.sin(x)**2 - 2 * math.sqrt(3) * math.sin(x) * math.cos(x) + math.cos(x)**2
    M, m = _maxmin(g, 0, P)
    assert abs(M - 4) < 1e-9 and abs(m) < 1e-9 and abs(g(2 * P / 3) - 4) < 1e-12 and abs(g(P / 6)) < 1e-12
    # M(a), m(a)
    for a in [-3, -1, -0.3, 0, 0.3, 1 / math.sqrt(3) - 1e-3, 1 / math.sqrt(3), 0.8, 1.5, math.sqrt(3), 2, 5]:
        M, m = _maxmin(lambda x: math.sin(x) + a * math.cos(x), 0, P / 3, 60000)
        Mf = (a + math.sqrt(3)) / 2 if a < 1 / math.sqrt(3) else math.sqrt(a * a + 1)
        mf = a if a <= math.sqrt(3) else (a + math.sqrt(3)) / 2
        assert abs(M - Mf) < 1e-8 and abs(m - mf) < 1e-12, a
    for a in [0.2, 0.7, 1, 1.4, 3]:
        M, m = _maxmin(lambda x: a * math.sin(x) + math.cos(x), 0, P / 2, 60000)
        assert abs(M - math.sqrt(a * a + 1)) < 1e-8 and abs(m - min(a, 1)) < 1e-12


# ---------------------------------------------------------------- 節8
SEC.append({"title": "和と積の公式",
"base": r"""・積→和：$\sin\alpha\cos\beta=\dfrac12\{\sin(\alpha+\beta)+\sin(\alpha-\beta)\}$，$\cos\alpha\cos\beta=\dfrac12\{\cos(\alpha+\beta)+\cos(\alpha-\beta)\}$，$\sin\alpha\sin\beta=-\dfrac12\{\cos(\alpha+\beta)-\cos(\alpha-\beta)\}$<br>
・和→積：$\sin A+\sin B=2\sin\dfrac{A+B}{2}\cos\dfrac{A-B}{2}$，$\sin A-\sin B=2\cos\dfrac{A+B}{2}\sin\dfrac{A-B}{2}$<br>
　　　　$\cos A+\cos B=2\cos\dfrac{A+B}{2}\cos\dfrac{A-B}{2}$，$\cos A-\cos B=-2\sin\dfrac{A+B}{2}\sin\dfrac{A-B}{2}$<br>
・三角形 ABC では $\dfrac{A+B}{2}=\dfrac{\pi}{2}-\dfrac{C}{2}$ より　$\sin\dfrac{A+B}{2}=\cos\dfrac{C}{2}$，$\cos\dfrac{A+B}{2}=\sin\dfrac{C}{2}$""",
"items": [
 {"lv": 2, "title": "和と積の公式による値の計算と方程式",
  "q": r"(1) $\sin75^\circ\cos15^\circ$，$\cos75^\circ+\cos15^\circ$ の値を求めよ。<br>(2) $0\leqq\theta<2\pi$ のとき，方程式 $\sin\theta+\sin2\theta+\sin3\theta=0$ を解け。",
  "hint": r"(1) 積→和，和→積の公式で，値の分かる角 $90^\circ,\ 60^\circ,\ 45^\circ,\ 30^\circ$ に直す。(2) 角の平均が $2\theta$ になる $\sin\theta$ と $\sin3\theta$ を組にして和→積の公式を使うと，$\sin2\theta$ が共通因数になる。",
  "sol": r"(1) $\sin75^\circ\cos15^\circ=\dfrac12(\sin90^\circ+\sin60^\circ)=\dfrac12\left(1+\dfrac{\sqrt3}{2}\right)=\boldsymbol{\dfrac{2+\sqrt3}{4}}$<br>"
         r"$\cos75^\circ+\cos15^\circ=2\cos45^\circ\cos30^\circ=2\cdot\dfrac{\sqrt2}{2}\cdot\dfrac{\sqrt3}{2}=\boldsymbol{\dfrac{\sqrt6}{2}}$<br>"
         r"(2) $\sin3\theta+\sin\theta=2\sin2\theta\cos\theta$ より，方程式は $2\sin2\theta\cos\theta+\sin2\theta=0$，すなわち $\sin2\theta(2\cos\theta+1)=0$。<br>"
         r"$\sin2\theta=0$ のとき，$0\leqq2\theta<4\pi$ より $2\theta=0,\ \pi,\ 2\pi,\ 3\pi$ で　$\theta=0,\ \dfrac{\pi}{2},\ \pi,\ \dfrac32\pi$<br>"
         r"$\cos\theta=-\dfrac12$ のとき　$\theta=\dfrac23\pi,\ \dfrac43\pi$<br>"
         r"よって　$\boldsymbol{\theta=0,\ \dfrac{\pi}{2},\ \dfrac23\pi,\ \pi,\ \dfrac43\pi,\ \dfrac32\pi}$",
  "note": r"(2) で $\sin\theta+\sin2\theta$ を組にすると $2\sin\dfrac32\theta\cos\dfrac{\theta}{2}$ となり，残りの $\sin3\theta$ と共通因数が出ない。和→積の公式は「角の和の半分がそろう組」を選んで使う。",
  "ex": r"(1) $\cos75^\circ\cos15^\circ$，$\sin105^\circ-\sin15^\circ$ の値を求めよ。<br>(2) $0\leqq\theta<2\pi$ のとき，方程式 $\cos\theta+\cos2\theta+\cos3\theta=0$ を解け。",
  "exa": r"(1) $\dfrac14$，$\dfrac{\sqrt2}{2}$　(2) $\theta=\dfrac{\pi}{4},\ \dfrac23\pi,\ \dfrac34\pi,\ \dfrac54\pi,\ \dfrac43\pi,\ \dfrac74\pi$"},
 {"lv": 3, "title": "三角形の角についての等式の証明",
  "q": r"三角形 ABC において，次の等式が成り立つことを証明せよ。<br>$\sin A+\sin B+\sin C=4\cos\dfrac{A}{2}\cos\dfrac{B}{2}\cos\dfrac{C}{2}$",
  "hint": r"$\sin A+\sin B$ を和→積の公式で積にし，$\sin C$ は2倍角の公式で $C$ の半角で表す。$\dfrac{A+B}{2}=\dfrac{\pi}{2}-\dfrac{C}{2}$ を使って，$C$ の半角の関数を $A,\ B$ の式に直すのがポイント。",
  "sol": r"$A+B+C=\pi$ より $\dfrac{A+B}{2}=\dfrac{\pi}{2}-\dfrac{C}{2}$ だから　$\sin\dfrac{A+B}{2}=\cos\dfrac{C}{2}$，$\cos\dfrac{A+B}{2}=\sin\dfrac{C}{2}$<br>"
         r"よって　$\sin A+\sin B=2\sin\dfrac{A+B}{2}\cos\dfrac{A-B}{2}=2\cos\dfrac{C}{2}\cos\dfrac{A-B}{2}$<br>"
         r"$\sin C=2\sin\dfrac{C}{2}\cos\dfrac{C}{2}=2\cos\dfrac{C}{2}\cos\dfrac{A+B}{2}$<br>"
         r"したがって　$\sin A+\sin B+\sin C=2\cos\dfrac{C}{2}\left(\cos\dfrac{A-B}{2}+\cos\dfrac{A+B}{2}\right)$<br>"
         r"ここで，和→積の公式より $\cos\dfrac{A-B}{2}+\cos\dfrac{A+B}{2}=2\cos\dfrac{A}{2}\cos\left(-\dfrac{B}{2}\right)=2\cos\dfrac{A}{2}\cos\dfrac{B}{2}$ だから<br>"
         r"$\sin A+\sin B+\sin C=4\cos\dfrac{A}{2}\cos\dfrac{B}{2}\cos\dfrac{C}{2}$　$\blacksquare$",
  "note": r"三角形の条件として使ったのは $A+B+C=\pi$ だけ。この種の等式は，2つの角を和→積でまとめ，残りの角を半角で表して共通因数を作るのが定石。",
  "ex": r"三角形 ABC において，$\cos A+\cos B+\cos C=1+4\sin\dfrac{A}{2}\sin\dfrac{B}{2}\sin\dfrac{C}{2}$ が成り立つことを証明せよ。",
  "exa": r"$\cos A+\cos B=2\sin\dfrac{C}{2}\cos\dfrac{A-B}{2}$，$\cos C=1-2\sin^2\dfrac{C}{2}$，$\sin\dfrac{C}{2}=\cos\dfrac{A+B}{2}$ と $\cos\dfrac{A-B}{2}-\cos\dfrac{A+B}{2}=2\sin\dfrac{A}{2}\sin\dfrac{B}{2}$ を用いる"},
 {"lv": 4, "title": r"三角形における $\cos A+\cos B+\cos C$ の最大値",
  "q": r"三角形 ABC において，$\cos A+\cos B+\cos C$ の最大値を求めよ。",
  "hint": r"まず $C$ を固定して $A,\ B$ を動かす。和→積の公式で $\cos A+\cos B=2\sin\dfrac{C}{2}\cos\dfrac{A-B}{2}\leqq2\sin\dfrac{C}{2}$。次に $\cos C=1-2\sin^2\dfrac{C}{2}$ として，$\sin\dfrac{C}{2}$ の2次関数を考える。",
  "sol": r"$A+B=\pi-C$ より $\cos\dfrac{A+B}{2}=\sin\dfrac{C}{2}$ だから　$\cos A+\cos B=2\cos\dfrac{A+B}{2}\cos\dfrac{A-B}{2}=2\sin\dfrac{C}{2}\cos\dfrac{A-B}{2}$<br>"
         r"$\sin\dfrac{C}{2}>0$，$\cos\dfrac{A-B}{2}\leqq1$ だから　$\cos A+\cos B\leqq2\sin\dfrac{C}{2}$<br>"
         r"（$-\dfrac{\pi}{2}<\dfrac{A-B}{2}<\dfrac{\pi}{2}$ なので，等号は $A=B$ のときに限る）<br>"
         r"$s=\sin\dfrac{C}{2}$ とおくと $0<s<1$ で，$\cos C=1-2s^2$ より<br>"
         r"$\cos A+\cos B+\cos C\leqq2s+1-2s^2=-2\left(s-\dfrac12\right)^2+\dfrac32\leqq\dfrac32$<br>"
         r"等号は $A=B$ かつ $s=\dfrac12$，すなわち $C=\dfrac{\pi}{3}$，$A=B=\dfrac{\pi}{3}$ のとき成り立つ。<br>"
         r"よって，最大値は　$\boldsymbol{\dfrac32}$（正三角形のとき）",
  "note": r"変数が2つ以上の最大・最小は「1つを固定して他を動かす」のが基本。前の例題の練習の等式を使うと，この結果は $\sin\dfrac{A}{2}\sin\dfrac{B}{2}\sin\dfrac{C}{2}\leqq\dfrac18$ と同じことである。",
  "ex": r"三角形 ABC において，$\cos A\cos B\cos C$ の最大値を求めよ。",
  "exa": r"$\dfrac18$（正三角形のとき）"},
 {"lv": 5, "title": "三角形の内角の正弦の和の最大（2つずつ平均に寄せる）",
  "q": r"三角形 ABC において，$\sin A+\sin B+\sin C\leqq\dfrac{3\sqrt3}{2}$ が成り立つことを証明せよ。また，等号が成り立つのはどのようなときか。",
  "hint": r"$0<x,\ y<\pi$ なら $\sin x+\sin y=2\sin\dfrac{x+y}{2}\cos\dfrac{x-y}{2}\leqq2\sin\dfrac{x+y}{2}$ で，2つの角を平均に寄せると和は増える。2つずつ2回くり返せば4つの角の平均に寄せられるので，3つの角に平均の角 $\dfrac{\pi}{3}$ を4つ目として補う。",
  "sol": r"【補題】$0<x<\pi$，$0<y<\pi$ のとき　$\sin x+\sin y\leqq2\sin\dfrac{x+y}{2}$（等号は $x=y$ のときに限る）<br>"
         r"（証明）$\sin x+\sin y=2\sin\dfrac{x+y}{2}\cos\dfrac{x-y}{2}$ で，$0<\dfrac{x+y}{2}<\pi$ より $\sin\dfrac{x+y}{2}>0$。また $-\dfrac{\pi}{2}<\dfrac{x-y}{2}<\dfrac{\pi}{2}$ より $\cos\dfrac{x-y}{2}\leqq1$ で，等号は $x=y$ のときに限る。<br>"
         r"補題を $A,\ B$ の組と $C,\ \dfrac{\pi}{3}$ の組に用いると<br>"
         r"$\sin A+\sin B+\sin C+\sin\dfrac{\pi}{3}\leqq2\sin\dfrac{A+B}{2}+2\sin\dfrac{C+\frac{\pi}{3}}{2}$ …①<br>"
         r"$\dfrac{A+B}{2}$，$\dfrac{C+\frac{\pi}{3}}{2}$ はともに $0$ と $\pi$ の間にあるから，再び補題より<br>"
         r"$2\sin\dfrac{A+B}{2}+2\sin\dfrac{C+\frac{\pi}{3}}{2}\leqq4\sin\dfrac{A+B+C+\frac{\pi}{3}}{4}=4\sin\dfrac{\pi}{3}$ …②<br>"
         r"（$A+B+C=\pi$ より $\dfrac{A+B+C+\frac{\pi}{3}}{4}=\dfrac{\pi}{3}$）。①，②より<br>"
         r"$\sin A+\sin B+\sin C\leqq3\sin\dfrac{\pi}{3}=\dfrac{3\sqrt3}{2}$<br>"
         r"等号は①，②でともに等号が成り立つとき，すなわち $A=B$，$C=\dfrac{\pi}{3}$，$\dfrac{A+B}{2}=\dfrac{C+\frac{\pi}{3}}{2}$ のときで，これは $A=B=C=\dfrac{\pi}{3}$ と同値。<br>"
         r"よって，等号が成り立つのは　<b>正三角形のとき</b>　$\blacksquare$",
  "note": r"これは「上に凸な関数では，値の平均は平均での値以下」（イェンセンの不等式）の特別な場合。2個ずつの平均を2回とると4個の平均が扱えるので，3個の場合は平均値 $\dfrac{\pi}{3}$ を4個目として補う，というのが核心のアイデア。外接円の半径を $R$ とすると，正弦定理より周の長さは $2R(\sin A+\sin B+\sin C)$ である。",
  "ex": r"半径 $1$ の円に内接する三角形の周の長さの最大値を求めよ。",
  "exa": r"$3\sqrt3$（正三角形のとき）"},
 {"lv": 5, "title": r"$\cos\dfrac{2}{7}\pi$ が満たす3次方程式と無理数であることの証明",
  "q": r"$\theta=\dfrac27\pi$ とする。<br>"
       r"(1) $\cos\theta+\cos2\theta+\cos3\theta=-\dfrac12$ を示せ。<br>"
       r"(2) $\cos\theta,\ \cos2\theta,\ \cos3\theta$ を3つの解とする，係数が整数の3次方程式を1つ求めよ。<br>"
       r"(3) $\cos\dfrac27\pi$ は無理数であることを示せ。",
  "hint": r"(1) $2\sin\dfrac{\theta}{2}$ を掛けると，積→和の公式で各項が「差」になり，次々に消える。(2) 解と係数の関係を逆に使う。積は $\cos3\theta=\cos4\theta$ に直して $\sin\theta$ を掛け，2倍角の公式をくり返す。(3) 有理数 $\dfrac{p}{q}$ が解なら $p,\ q$ の候補が絞れる。",
  "sol": r"$7\theta=2\pi$ に注意する。<br>"
         r"(1) $S=\cos\theta+\cos2\theta+\cos3\theta$ とおく。積→和の公式 $2\sin\dfrac{\theta}{2}\cos k\theta=\sin\left(k+\dfrac12\right)\theta-\sin\left(k-\dfrac12\right)\theta$ より<br>"
         r"$2\sin\dfrac{\theta}{2}\cdot S=\left(\sin\dfrac32\theta-\sin\dfrac12\theta\right)+\left(\sin\dfrac52\theta-\sin\dfrac32\theta\right)+\left(\sin\dfrac72\theta-\sin\dfrac52\theta\right)=\sin\dfrac72\theta-\sin\dfrac{\theta}{2}$<br>"
         r"$\dfrac72\theta=\pi$ より $\sin\dfrac72\theta=0$。$0<\dfrac{\theta}{2}<\pi$ より $\sin\dfrac{\theta}{2}\neq0$ だから　$S=-\dfrac12$　$\blacksquare$<br>"
         r"(2) $\cos5\theta=\cos(2\pi-2\theta)=\cos2\theta$，$\cos4\theta=\cos(2\pi-3\theta)=\cos3\theta$ に注意すると，積→和の公式より<br>"
         r"$\cos\theta\cos2\theta+\cos2\theta\cos3\theta+\cos3\theta\cos\theta=\dfrac{(\cos3\theta+\cos\theta)+(\cos5\theta+\cos\theta)+(\cos4\theta+\cos2\theta)}{2}$<br>"
         r"$=\dfrac{2\cos\theta+2\cos2\theta+2\cos3\theta}{2}=S=-\dfrac12$<br>"
         r"また $P=\cos\theta\cos2\theta\cos3\theta=\cos\theta\cos2\theta\cos4\theta$ で，<br>"
         r"$8\sin\theta\cdot P=4\sin2\theta\cos2\theta\cos4\theta=2\sin4\theta\cos4\theta=\sin8\theta=\sin(2\pi+\theta)=\sin\theta$<br>"
         r"$\sin\theta\neq0$ より $P=\dfrac18$。よって，解と係数の関係から，$\cos\theta,\ \cos2\theta,\ \cos3\theta$ を解とする3次方程式として<br>"
         r"$x^3+\dfrac12x^2-\dfrac12x-\dfrac18=0$，すなわち　$\boldsymbol{8x^3+4x^2-4x-1=0}$<br>"
         r"(3) $\cos\theta$ が有理数 $\dfrac{p}{q}$（$p,\ q$ は互いに素な整数，$q\geqq1$）であるとすると，(2) より $8p^3+4p^2q-4pq^2-q^3=0$。<br>"
         r"$q^3=p(8p^2+4pq-4q^2)$ より $q^3$ は $p$ の倍数で，$p,\ q$ は互いに素だから $p=\pm1$。<br>"
         r"$8p^3=q(-4p^2+4pq+q^2)$ より $8p^3$ は $q$ の倍数で，$q$ は $8$ の正の約数。よって $\cos\theta$ は $\pm1,\ \pm\dfrac12,\ \pm\dfrac14,\ \pm\dfrac18$ のいずれか。<br>"
         r"$f(x)=8x^3+4x^2-4x-1$ とすると　$f(1)=7$，$f(-1)=-1$，$f\left(\dfrac12\right)=-1$，$f\left(-\dfrac12\right)=1$，$f\left(\dfrac14\right)=-\dfrac{13}{8}$，$f\left(-\dfrac14\right)=\dfrac18$，$f\left(\dfrac18\right)=-\dfrac{91}{64}$，$f\left(-\dfrac18\right)=-\dfrac{29}{64}$<br>"
         r"いずれも $0$ でないので矛盾。したがって $\cos\dfrac27\pi$ は無理数である。$\blacksquare$",
  "note": r"(1) の「$2\sin\dfrac{\theta}{2}$ を掛けて積→和で差の形にし，次々に消す」のは，$\cos$ や $\sin$ の等差的な角の和を求める定石。(3) の論法から，$8x^3+4x^2-4x-1=0$ は有理数の解をもたない。正七角形が定規とコンパスで作図できないことは，この事実と深く関係している。",
  "ex": r"$\theta=\dfrac{\pi}{7}$ とする。$\cos\theta-\cos2\theta+\cos3\theta=\dfrac12$ を示し，$\cos\dfrac{\pi}{7}\cos\dfrac27\pi\cos\dfrac37\pi$ の値を求めよ。",
  "exa": r"$-\cos2\theta=\cos5\theta$ として $2\sin\theta$ を掛けると $\sin6\theta=\sin\theta$ に帰着する。値は $\dfrac18$"},
]})


@_v
def _v8():
    import sympy as sp
    from sympy import sin, cos, pi, sqrt, Rational as R
    P = math.pi
    d = lambda k: pi * k / 180
    _eq(sin(d(75)) * cos(d(15)), (2 + sqrt(3)) / 4); _eq(cos(d(75)) + cos(d(15)), sqrt(6) / 2)
    _eq(cos(d(75)) * cos(d(15)), R(1, 4)); _eq(sin(d(105)) - sin(d(15)), sqrt(2) / 2)
    _same_roots(lambda t: math.sin(t) + math.sin(2 * t) + math.sin(3 * t), [0, P / 2, 2 * P / 3, P, 4 * P / 3, 3 * P / 2])
    _same_roots(lambda t: math.cos(t) + math.cos(2 * t) + math.cos(3 * t), [P / 4, 2 * P / 3, 3 * P / 4, 5 * P / 4, 4 * P / 3, 7 * P / 4])
    rnd = random.Random(8)
    for _ in range(500):
        A = rnd.uniform(0.01, 3.1); B = rnd.uniform(0.01, P - A - 0.005); C = P - A - B
        s = math.sin(A) + math.sin(B) + math.sin(C)
        assert abs(s - 4 * math.cos(A / 2) * math.cos(B / 2) * math.cos(C / 2)) < 1e-12
        c = math.cos(A) + math.cos(B) + math.cos(C)
        assert abs(c - 1 - 4 * math.sin(A / 2) * math.sin(B / 2) * math.sin(C / 2)) < 1e-12
        assert c <= 1.5 + 1e-12 and s <= 3 * math.sqrt(3) / 2 + 1e-12
        assert math.cos(A) * math.cos(B) * math.cos(C) <= 1 / 8 + 1e-12
        x, y = rnd.uniform(0.001, P - 0.001), rnd.uniform(0.001, P - 0.001)
        assert math.sin(x) + math.sin(y) <= 2 * math.sin((x + y) / 2) + 1e-12
    best = [0, 0, -9]
    N = 600
    for i in range(1, N):
        for j in range(1, N - i):
            A, B = P * i / N, P * j / N
            C = P - A - B
            best[0] = max(best[0], math.cos(A) + math.cos(B) + math.cos(C))
            best[1] = max(best[1], math.sin(A) + math.sin(B) + math.sin(C))
            best[2] = max(best[2], math.cos(A) * math.cos(B) * math.cos(C))
    assert abs(best[0] - 1.5) < 1e-9 and abs(best[1] - 3 * math.sqrt(3) / 2) < 1e-9 and abs(best[2] - 1 / 8) < 1e-9
    s_ = math.sin(P / 3); assert abs(2 * (3 * s_) - 3 * math.sqrt(3)) < 1e-12        # 周の長さ 2R(sinA+sinB+sinC)
    # cos(2π/7)
    th = 2 * pi / 7
    S = cos(th) + cos(2 * th) + cos(3 * th)
    _eq(S, -R(1, 2))
    _eq(cos(th) * cos(2 * th) + cos(2 * th) * cos(3 * th) + cos(3 * th) * cos(th), -R(1, 2))
    _eq(cos(th) * cos(2 * th) * cos(3 * th), R(1, 8))
    xx = sp.symbols("x")
    cf = sp.Poly(sp.expand(8 * (xx - cos(th)) * (xx - cos(2 * th)) * (xx - cos(3 * th))), xx).all_coeffs()
    for c1, c2 in zip(cf, [8, 4, -4, -1]):
        _eq(c1, c2)
    f = lambda v: 8 * v**3 + 4 * v**2 - 4 * v - 1
    vals = {Fr(1): 7, Fr(-1): -1, Fr(1, 2): -1, Fr(-1, 2): 1, Fr(1, 4): Fr(-13, 8), Fr(-1, 4): Fr(1, 8), Fr(1, 8): Fr(-91, 64), Fr(-1, 8): Fr(-29, 64)}
    for v, fv in vals.items():
        assert f(v) == fv and fv != 0
    for kk in (1, 2, 3):
        assert abs(f(math.cos(2 * kk * P / 7))) < 1e-12
    # 練習：θ=π/7
    th = pi / 7
    _eq(cos(th) - cos(2 * th) + cos(3 * th), R(1, 2)); _eq(cos(th) * cos(2 * th) * cos(3 * th), R(1, 8))
    _eq(-cos(2 * th), cos(5 * th)); _eq(sin(6 * th), sin(th))


# ---------------------------------------------------------------- 節9
def _fig93():
    th = 0.42
    f = _Fig(170, 152, (-0.1, 1.15), (-0.12, 0.95), pad=(10, 10, 10, 14))
    f.arc(0, 0, 1, 0, math.pi / 3, col="#333", sw=1.1)
    f.line(0, 0, 1, 0, sw=1.1)
    f.line(0, 0, 0.5, math.sqrt(3) / 2, sw=1.1)
    P = (math.cos(th), math.sin(th)); Q = (P[0], 0); S = (P[1] / math.sqrt(3), P[1]); R = (S[0], 0)
    f.poly([P, Q, R, S], close=True, fill="#eaf0fb", sw=1.3)
    for (x, y), s, dx, dy in [((0, 0), "O", -4, 11), ((1, 0), "A", 3, 11), ((0.5, math.sqrt(3) / 2), "B", -2, -4),
                              (P, "P", 7, 2), (Q, "Q", 0, 11), (R, "R", 0, 11), (S, "S", -7, -1)]:
        f.text(x, y, s, size=11, dx=dx, dy=dy)
    for p in (P, Q, R, S):
        f.dot(*p, r=1.6)
    return f.svg()


def _fig95():
    th = 1.1
    f = _Fig(170, 107, (-1.15, 1.15), (-0.15, 1.12), pad=(10, 10, 10, 14))
    f.arc(0, 0, 1, 0, math.pi, col="#333", sw=1.1)
    f.line(-1, 0, 1, 0, sw=1.1)
    C = (math.cos(th), math.sin(th)); D = (-C[0], C[1])
    f.poly([(-1, 0), (1, 0), C, D], close=True, fill="#eaf0fb", sw=1.3)
    for (x, y), s, dx, dy in [((-1, 0), "A", -2, 11), ((1, 0), "B", 2, 11), (C, "C", 7, -2), (D, "D", -7, -2), ((0, 0), "O", 0, 11)]:
        f.text(x, y, s, size=11, dx=dx, dy=dy)
    f.dot(0, 0, r=1.4)
    return f.svg()


def _fig97():
    A, B, C = (1.3, 2.6), (0.0, 0.0), (4.0, 0.0)
    dist = lambda p, q: math.hypot(p[0] - q[0], p[1] - q[1])
    a, b, c = dist(B, C), dist(C, A), dist(A, B)
    I = ((a * A[0] + b * B[0] + c * C[0]) / (a + b + c), (a * A[1] + b * B[1] + c * C[1]) / (a + b + c))
    r = I[1]
    f = _Fig(196, 146, (-0.3, 4.3), (-0.35, 2.85), pad=(8, 6, 8, 12))
    f.poly([A, B, C], close=True, sw=1.2, col="#333")
    f.arc(I[0], I[1], r, 0, 2 * math.pi, n=120, col="#16367a", sw=1.1)
    f.line(B[0], B[1], I[0], I[1], sw=0.8, col="#666", dash="3,2")
    f.line(C[0], C[1], I[0], I[1], sw=0.8, col="#666", dash="3,2")
    f.line(I[0], I[1], I[0], 0, sw=1.0, col="#c0392b")
    f.dot(*I, r=1.6)
    f.dot(I[0], 0, r=1.6)
    for (x, y), s, dx, dy in [(A, "A", 0, -4), (B, "B", -6, 10), (C, "C", 6, 10), (I, "I", 7, -2), ((I[0], 0), "D", 0, 11)]:
        f.text(x, y, s, size=11, dx=dx, dy=dy)
    f.text(I[0], r / 2, "r", size=11, dx=-6, dy=4, it=True)
    f.text(0.55, 0.05, "B/2", size=9, dy=-1)
    f.text(3.45, 0.05, "C/2", size=9, dy=-1)
    return f.svg()


SEC.append({"title": "置き換え・解の個数と図形への応用",
"base": r"""・$\sin\theta,\ \cos\theta$ の一方だけの式は $t=\sin\theta$ などとおき，$t$ の変域（$-1\leqq t\leqq1$，または $\theta$ の範囲から決まる範囲）で考える<br>
・$\sin\theta\pm\cos\theta$ と $\sin\theta\cos\theta$ を含む式は $t=\sin\theta+\cos\theta=\sqrt2\sin\left(\theta+\dfrac{\pi}{4}\right)$ とおくと $\sin\theta\cos\theta=\dfrac{t^2-1}{2}$<br>
・方程式の解の個数は，定数を分離したグラフと直線の共有点で数える。置き換えたときは，$t$ の値1つに対応する $\theta$ の個数に注意<br>
・図形の量は，角を変数にとると三角関数で表せる（円周上の点 $(\cos\theta,\ \sin\theta)$，正弦定理 $a=2R\sin A$ など）""",
"items": [
 {"lv": 2, "title": "置き換えによる2次関数の最大・最小",
  "q": r"関数 $y=\cos2\theta+2\sin\theta$（$0\leqq\theta<2\pi$）の最大値と最小値，およびそのときの $\theta$ の値を求めよ。",
  "hint": r"$\cos2\theta=1-2\sin^2\theta$ で $\sin\theta$ だけの式にし，$t=\sin\theta$ とおく。$t$ の変域 $-1\leqq t\leqq1$ での2次関数の最大・最小を考える。",
  "sol": r"$y=1-2\sin^2\theta+2\sin\theta$。$t=\sin\theta$ とおくと，$0\leqq\theta<2\pi$ より $-1\leqq t\leqq1$ で<br>"
         r"$y=-2t^2+2t+1=-2\left(t-\dfrac12\right)^2+\dfrac32$<br>"
         r"$-1\leqq t\leqq1$ において，$y$ は $t=\dfrac12$ で最大値 $\dfrac32$，$t=-1$ で最小値 $-3$ をとる。<br>"
         r"$\sin\theta=\dfrac12$ より $\theta=\dfrac{\pi}{6},\ \dfrac56\pi$，$\sin\theta=-1$ より $\theta=\dfrac32\pi$。<br>"
         r"よって　$\boldsymbol{\theta=\dfrac{\pi}{6},\ \dfrac56\pi}$ のとき最大値 $\boldsymbol{\dfrac32}$，$\boldsymbol{\theta=\dfrac32\pi}$ のとき最小値 $\boldsymbol{-3}$",
  "note": r"置き換えたら，必ず新しい文字の変域を確認する。例えば $\theta$ の範囲が $0\leqq\theta\leqq\dfrac{\pi}{2}$ なら $0\leqq t\leqq1$ となり，最小値は $t=0,\ 1$ のときの $1$ に変わる。",
  "ex": r"関数 $y=\cos2\theta-4\cos\theta$（$0\leqq\theta<2\pi$）の最大値と最小値，およびそのときの $\theta$ の値を求めよ。",
  "exa": r"$\theta=\pi$ のとき最大値 $5$，$\theta=0$ のとき最小値 $-3$"},
 {"lv": 3, "title": r"$t=\sin\theta+\cos\theta$ の置き換え",
  "q": r"関数 $y=\sin\theta\cos\theta+\sin\theta+\cos\theta$（$0\leqq\theta\leqq\pi$）の最大値と最小値，およびそのときの $\theta$ の値を求めよ。",
  "hint": r"$t=\sin\theta+\cos\theta$ とおくと，$t^2=1+2\sin\theta\cos\theta$ より $\sin\theta\cos\theta=\dfrac{t^2-1}{2}$。$t$ の変域は合成 $t=\sqrt2\sin\left(\theta+\dfrac{\pi}{4}\right)$ から求める。",
  "sol": r"$t=\sin\theta+\cos\theta$ とおくと，$t^2=1+2\sin\theta\cos\theta$ より $\sin\theta\cos\theta=\dfrac{t^2-1}{2}$。<br>"
         r"また $t=\sqrt2\sin\left(\theta+\dfrac{\pi}{4}\right)$ で，$\dfrac{\pi}{4}\leqq\theta+\dfrac{\pi}{4}\leqq\dfrac54\pi$ より $-\dfrac{1}{\sqrt2}\leqq\sin\left(\theta+\dfrac{\pi}{4}\right)\leqq1$，すなわち $-1\leqq t\leqq\sqrt2$。<br>"
         r"$y=\dfrac{t^2-1}{2}+t=\dfrac12(t+1)^2-1$ は $-1\leqq t\leqq\sqrt2$ で増加するから，<br>"
         r"$t=\sqrt2$ のとき最大値 $\dfrac12(\sqrt2+1)^2-1=\dfrac12+\sqrt2$，$t=-1$ のとき最小値 $-1$。<br>"
         r"$t=\sqrt2$ となるのは $\theta+\dfrac{\pi}{4}=\dfrac{\pi}{2}$ より $\theta=\dfrac{\pi}{4}$，$t=-1$ となるのは $\theta+\dfrac{\pi}{4}=\dfrac54\pi$ より $\theta=\pi$。<br>"
         r"よって　$\boldsymbol{\theta=\dfrac{\pi}{4}}$ のとき最大値 $\boldsymbol{\dfrac12+\sqrt2}$，$\boldsymbol{\theta=\pi}$ のとき最小値 $\boldsymbol{-1}$",
  "note": r"$\sin\theta\pm\cos\theta$ と $\sin\theta\cos\theta$（または $\sin2\theta$）が混ざった式は，この置き換えが定石。$t$ の変域を合成で正しく求めることが最も大切で，$-\sqrt2\leqq t\leqq\sqrt2$ と決めつけると誤る。",
  "ex": r"関数 $y=\sin2\theta-2(\sin\theta+\cos\theta)$（$0\leqq\theta<2\pi$）の最大値と最小値，およびそのときの $\theta$ の値を求めよ。",
  "exa": r"$\theta=\dfrac54\pi$ のとき最大値 $1+2\sqrt2$，$\theta=0,\ \dfrac{\pi}{2}$ のとき最小値 $-2$"},
 {"lv": 3, "title": "扇形に内接する長方形の面積の最大",
  "q": _fig93() +
       r"半径 $1$，中心角 $\dfrac{\pi}{3}$ の扇形 OAB がある。右の図のように，弧 AB 上の点 P，半径 OA 上の2点 Q，R，半径 OB 上の点 S を頂点とする長方形 PQRS をつくる。<br>この長方形の面積の最大値を求めよ。",
  "hint": r"$\angle\mathrm{AOP}=\theta$ を変数にとり，辺の長さを $\theta$ で表す。面積は $\sin^2\theta$，$\sin\theta\cos\theta$ の式になるので，次数を下げて合成する。$\theta$ の変域も忘れない。",
  "sol": r"$\angle\mathrm{AOP}=\theta$ とおくと $0<\theta<\dfrac{\pi}{3}$。O を原点，A を $(1,\ 0)$ とする座標で $\mathrm{P}(\cos\theta,\ \sin\theta)$。<br>"
         r"PS は OA に平行で，S は直線 OB：$y=\sqrt3x$ 上にあるから $\mathrm{S}\left(\dfrac{\sin\theta}{\sqrt3},\ \sin\theta\right)$。<br>"
         r"よって $\mathrm{PQ}=\sin\theta$，$\mathrm{PS}=\cos\theta-\dfrac{\sin\theta}{\sqrt3}$（$0<\theta<\dfrac{\pi}{3}$ では $\tan\theta<\sqrt3$ より正）で，面積を $F$ とすると<br>"
         r"$F=\sin\theta\cos\theta-\dfrac{\sin^2\theta}{\sqrt3}=\dfrac12\sin2\theta-\dfrac{1}{\sqrt3}\cdot\dfrac{1-\cos2\theta}{2}$<br>"
         r"$=\dfrac{1}{2\sqrt3}(\sqrt3\sin2\theta+\cos2\theta-1)=\dfrac{1}{2\sqrt3}\left\{2\sin\left(2\theta+\dfrac{\pi}{6}\right)-1\right\}$<br>"
         r"$\dfrac{\pi}{6}<2\theta+\dfrac{\pi}{6}<\dfrac56\pi$ だから，$2\theta+\dfrac{\pi}{6}=\dfrac{\pi}{2}$，すなわち $\theta=\dfrac{\pi}{6}$ のとき $F$ は最大となる。<br>"
         r"最大値は　$\dfrac{1}{2\sqrt3}(2-1)=\boldsymbol{\dfrac{\sqrt3}{6}}$",
  "note": r"最大となる $\theta=\dfrac{\pi}{6}$ は，P が弧 AB の中点にくるとき。面積を「$\sin(2\theta+\alpha)$ 1つ＋定数」の形にまとめるのがポイントで，これは2次の同次式の最大・最小と同じ処理である。",
  "ex": r"半径 $1$，中心角 $\dfrac{\pi}{4}$ の扇形 OAB に，例題と同じように長方形 PQRS（P は弧 AB 上，Q，R は半径 OA 上，S は半径 OB 上）をつくる。この長方形の面積の最大値を求めよ。",
  "exa": r"$\dfrac{\sqrt2-1}{2}$（$\angle\mathrm{AOP}=\dfrac{\pi}{8}$ のとき）"},
 {"lv": 4, "title": "置き換えを含む方程式の解の個数",
  "q": r"$a$ を定数とする。$0\leqq x<2\pi$ のとき，$x$ の方程式 $\sin x\cos x+\sin x+\cos x=a$ の異なる実数解の個数を調べよ。",
  "hint": r"$t=\sin x+\cos x$ とおくと $t$ の2次方程式になる。$t$ の値1つに対応する $x$ の個数（$|t|<\sqrt2$ なら2個，$t=\pm\sqrt2$ なら1個）に注意して，$y=g(t)$ のグラフと直線 $y=a$ の共有点を数える。",
  "sol": r"$t=\sin x+\cos x=\sqrt2\sin\left(x+\dfrac{\pi}{4}\right)$ とおく。$0\leqq x<2\pi$ のとき $\dfrac{\pi}{4}\leqq x+\dfrac{\pi}{4}<\dfrac94\pi$ で，$t$ のとり得る値の範囲は $-\sqrt2\leqq t\leqq\sqrt2$。<br>"
         r"$t$ の値1つに対して，$x$ は　$-\sqrt2<t<\sqrt2$ のとき2個，$t=\pm\sqrt2$ のとき1個　ある。<br>"
         r"$\sin x\cos x=\dfrac{t^2-1}{2}$ より，方程式は　$g(t)=a$，ただし $g(t)=\dfrac{t^2-1}{2}+t=\dfrac12(t+1)^2-1$<br>"
         r"$g(-\sqrt2)=\dfrac12(1-\sqrt2)^2-1=\dfrac12-\sqrt2$，$g(-1)=-1$，$g(\sqrt2)=\dfrac12+\sqrt2$ で，$-1<\dfrac12-\sqrt2<\dfrac12+\sqrt2$。<br>"
         r"$y=g(t)$（$-\sqrt2\leqq t\leqq\sqrt2$）は $t=-1$ を軸とする放物線の一部で，左端 $t=-\sqrt2$ の方が右端 $t=\sqrt2$ より軸に近い。直線 $y=a$ との共有点を調べると<br>"
         r"・$a<-1$ のとき，$t$ はない → $0$ 個<br>"
         r"・$a=-1$ のとき，$t=-1$ → $2$ 個<br>"
         r"・$-1<a<\dfrac12-\sqrt2$ のとき，$t$ は $-\sqrt2<t<-1$，$-1<t<\sqrt2-2$ に1個ずつ → $x$ は $2+2=4$ 個<br>"
         r"・$a=\dfrac12-\sqrt2$ のとき，$(t+1)^2=(\sqrt2-1)^2$ より $t=-\sqrt2,\ \sqrt2-2$ → $1+2=3$ 個<br>"
         r"・$\dfrac12-\sqrt2<a<\dfrac12+\sqrt2$ のとき，$-\sqrt2\leqq t\leqq\sqrt2$ の範囲の $t$ は1個で $-\sqrt2<t<\sqrt2$ → $2$ 個<br>"
         r"・$a=\dfrac12+\sqrt2$ のとき，$t=\sqrt2$ → $1$ 個　　・$a>\dfrac12+\sqrt2$ のとき，$t$ はない → $0$ 個<br>"
         r"答　$a<-1,\ \dfrac12+\sqrt2<a$ のとき <b>0個</b>；$a=-1$ のとき <b>2個</b>；$-1<a<\dfrac12-\sqrt2$ のとき <b>4個</b>；$a=\dfrac12-\sqrt2$ のとき <b>3個</b>；$\dfrac12-\sqrt2<a<\dfrac12+\sqrt2$ のとき <b>2個</b>；$a=\dfrac12+\sqrt2$ のとき <b>1個</b>",
  "note": r"置き換えた文字 $t$ と元の変数 $x$ の対応が1対1でないときは，「$t$ の値1つに $x$ が何個対応するか」を必ず調べる。端の値 $t=\pm\sqrt2$ だけは対応する $x$ が1個になることが，答えに「3個」「1個」が現れる理由である。",
  "ex": r"$a$ を定数とする。$0\leqq x<2\pi$ のとき，$x$ の方程式 $\sin2x-2(\sin x+\cos x)=a$ の異なる実数解の個数を調べよ。",
  "exa": r"$a<-2,\ 1+2\sqrt2<a$ のとき 0個；$a=-2$ のとき 2個；$-2<a<1-2\sqrt2$ のとき 4個；$a=1-2\sqrt2$ のとき 3個；$1-2\sqrt2<a<1+2\sqrt2$ のとき 2個；$a=1+2\sqrt2$ のとき 1個"},
 {"lv": 4, "title": "半円に内接する台形の面積の最大",
  "q": _fig95() +
       r"半径 $1$ の半円がある。右の図のように，直径 AB を下底とし，上底 CD の両端が弧の上にある台形 ABCD をつくる。<br>台形 ABCD の面積の最大値を求めよ。",
  "hint": r"中心を O，$\angle\mathrm{BOC}=\theta$ とすると面積は $(1+\cos\theta)\sin\theta$ となるが，合成では処理できない。2乗して $c=\cos\theta$ の4次式にし，最大値を予想して（正六角形の半分，$c=\dfrac12$），差が $\left(c-\dfrac12\right)^2\times$（正の式）と因数分解できることを示す。",
  "sol": r"中心を O とし，$\angle\mathrm{BOC}=\theta$（$0<\theta<\dfrac{\pi}{2}$）とする。O を原点，B を $(1,\ 0)$ とすると $\mathrm{C}(\cos\theta,\ \sin\theta)$，$\mathrm{D}(-\cos\theta,\ \sin\theta)$ で，<br>"
         r"$\mathrm{AB}=2$，$\mathrm{CD}=2\cos\theta$，高さは $\sin\theta$ だから，面積は　$F=\dfrac12(2+2\cos\theta)\sin\theta=(1+\cos\theta)\sin\theta$<br>"
         r"$c=\cos\theta$ とおくと $0<c<1$，$F>0$ で　$F^2=(1+c)^2(1-c^2)=(1+c)^3(1-c)=1+2c-2c^3-c^4$<br>"
         r"ここで　$\dfrac{27}{16}-F^2=c^4+2c^3-2c+\dfrac{11}{16}=\left(c-\dfrac12\right)^2\left(c^2+3c+\dfrac{11}{4}\right)$<br>"
         r"$c^2+3c+\dfrac{11}{4}=\left(c+\dfrac32\right)^2+\dfrac12>0$ だから $F^2\leqq\dfrac{27}{16}$，すなわち $F\leqq\dfrac{3\sqrt3}{4}$。等号は $c=\dfrac12$，すなわち $\theta=\dfrac{\pi}{3}$ のとき成り立つ。<br>"
         r"よって，面積の最大値は　$\boldsymbol{\dfrac{3\sqrt3}{4}}$",
  "note": r"最大となるのは $\mathrm{BC}=\mathrm{CD}=\mathrm{DA}=1$，すなわち正六角形の半分のとき。4個の正の数の相加平均と相乗平均の関係 $\sqrt[4]{pqrs}\leqq\dfrac{p+q+r+s}{4}$ を $p=q=r=1+c$，$s=3-3c$ に用いて $3F^2=(1+c)^3(3-3c)\leqq\left(\dfrac64\right)^4$ としてもよい。微分法（第14章）を学べば，$F^2$ の増減からも求まる。",
  "ex": r"半径 $1$ の円に内接する二等辺三角形の面積の最大値を求めよ。",
  "exa": r"$\dfrac{3\sqrt3}{4}$（正三角形のとき）"},
 {"lv": 5, "title": r"$\sin(a\pi\cos x)=\cos(a\pi\sin x)$ の解の個数",
  "q": r"$a$ を正の定数とし，$0\leqq x<2\pi$ における $x$ の方程式<br>$\sin(a\pi\cos x)=\cos(a\pi\sin x)$ …(*)<br>を考える。(1) $a=1$ のとき，(*) の解の個数を求めよ。　(2) $a=2$ のとき，(*) の解の個数を求めよ。",
  "hint": r"$\cos\beta=\sin\left(\dfrac{\pi}{2}-\beta\right)$ とすれば「$\sin A=\sin B$」の形になり，一般解から $\sin x+\cos x$，$\cos x-\sin x$ の1次方程式の集まりに帰着する。$|\sin x\pm\cos x|\leqq\sqrt2$ で候補を絞り，最後に解の重なりを調べる。",
  "sol": r"(*) は $\sin(a\pi\cos x)=\sin\left(\dfrac{\pi}{2}-a\pi\sin x\right)$ と同値だから，$n$ を整数として<br>"
         r"$a\pi\cos x=\dfrac{\pi}{2}-a\pi\sin x+2n\pi$　または　$a\pi\cos x=\pi-\left(\dfrac{\pi}{2}-a\pi\sin x\right)+2n\pi$<br>"
         r"すなわち　$a(\sin x+\cos x)=\dfrac12+2n$ …①　または　$a(\cos x-\sin x)=\dfrac12+2n$ …②<br>"
         r"$\sin x+\cos x=\sqrt2\sin\left(x+\dfrac{\pi}{4}\right)$，$\cos x-\sin x=\sqrt2\cos\left(x+\dfrac{\pi}{4}\right)$ だから，定数 $v$ に対して $\sin x+\cos x=v$（$\cos x-\sin x=v$ も同様）を満たす $x$（$0\leqq x<2\pi$）は<br>"
         r"$|v|<\sqrt2$ のとき2個，$|v|=\sqrt2$ のとき1個，$|v|>\sqrt2$ のとき0個。<br>"
         r"また，$\sin x+\cos x=v_1$ と $\cos x-\sin x=v_2$ を同時に満たす $x$ があれば $\cos x=\dfrac{v_1+v_2}{2}$，$\sin x=\dfrac{v_1-v_2}{2}$ より $v_1^2+v_2^2=2$ である …③<br>"
         r"(1) $a=1$ のとき，$v=\dfrac12+2n$ で $|v|\leqq\sqrt2$ となるのは $n=0$ の $v=\dfrac12$ のみ（$n=-1$ では $|v|=\dfrac32>\sqrt2$）。<br>"
         r"①，②はそれぞれ2個の解をもち，$\left(\dfrac12\right)^2+\left(\dfrac12\right)^2\neq2$ だから③より重なりはない。よって　$\boldsymbol{4}$ 個<br>"
         r"(2) $a=2$ のとき，$v=\dfrac14+n$ で $|v|\leqq\sqrt2$ となるのは $v=-\dfrac34,\ \dfrac14,\ \dfrac54$（$\left(\dfrac54\right)^2=\dfrac{25}{16}<2$，$\left(\dfrac74\right)^2>2$）。いずれも $|v|<\sqrt2$。<br>"
         r"①で $v$ の値が異なれば解も異なるから，①の解は $2\times3=6$ 個，同様に②の解も6個。<br>"
         r"$v^2$ は $\dfrac{9}{16},\ \dfrac{1}{16},\ \dfrac{25}{16}$ のいずれかで，2つの和が $2=\dfrac{32}{16}$ となる組はない（$9,\ 1,\ 25$ から重複を許して2つ選んだ和は $32$ にならない）。③より①と②の解に重なりはない。<br>"
         r"よって　$\boldsymbol{12}$ 個",
  "note": r"$\sin A=\sin B$ を和→積の公式で $2\cos\dfrac{A+B}{2}\sin\dfrac{A-B}{2}=0$ としても同じ式が出る。重なりの確認を怠ると数え違える。実際，$a=\dfrac12$ のときは①が $\sin x+\cos x=1$，②が $\cos x-\sin x=1$ となり，$x=0$ が共通解となるので，解は $x=0,\ \dfrac{\pi}{2},\ \dfrac32\pi$ の3個である。",
  "ex": r"$0\leqq x<2\pi$ のとき，方程式 $\sin(\pi\cos x)=\sin(\pi\sin x)$ の解の個数を求めよ。",
  "exa": r"$6$ 個（$x=0,\ \dfrac{\pi}{4},\ \dfrac{\pi}{2},\ \pi,\ \dfrac54\pi,\ \dfrac32\pi$）"},
 {"lv": 5, "title": r"外接円と内接円の半径の関係（$R\geqq2r$）",
  "q": r"三角形 ABC の外接円の半径を $R$，内接円の半径を $r$ とする。<br>"
       r"(1) $r=4R\sin\dfrac{A}{2}\sin\dfrac{B}{2}\sin\dfrac{C}{2}$ が成り立つことを示せ。<br>"
       r"(2) $R\geqq2r$ が成り立つことを示せ。また，等号が成り立つのはどのようなときか。",
  "hint": r"(1) 辺 BC の長さを2通りに表す：内心 I から BC に下ろした垂線の足 D で BC を分けると，直角三角形 IBD，ICD から $\mathrm{BD}=\dfrac{r}{\tan\frac{B}{2}}$ など。もう1つは正弦定理。(2) $\cos A+\cos B+\cos C$ の最大値と同じく，まず $A$ を固定して $B,\ C$ を動かす。",
  "sol": _fig97() +
         r"(1) 内心を I，内接円と辺 BC の接点を D とすると，$\mathrm{ID}=r$，$\mathrm{ID}\perp\mathrm{BC}$，$\angle\mathrm{IBD}=\dfrac{B}{2}$，$\angle\mathrm{ICD}=\dfrac{C}{2}$ だから　$\mathrm{BD}=\dfrac{r}{\tan\frac{B}{2}}$，$\mathrm{DC}=\dfrac{r}{\tan\frac{C}{2}}$<br>"
         r"よって　$a=\mathrm{BD}+\mathrm{DC}=r\left(\dfrac{\cos\frac{B}{2}}{\sin\frac{B}{2}}+\dfrac{\cos\frac{C}{2}}{\sin\frac{C}{2}}\right)=\dfrac{r\sin\left(\frac{B}{2}+\frac{C}{2}\right)}{\sin\frac{B}{2}\sin\frac{C}{2}}=\dfrac{r\cos\frac{A}{2}}{\sin\frac{B}{2}\sin\frac{C}{2}}$<br>"
         r"（加法定理と $\dfrac{B+C}{2}=\dfrac{\pi}{2}-\dfrac{A}{2}$ を用いた）。一方，正弦定理より $a=2R\sin A=4R\sin\dfrac{A}{2}\cos\dfrac{A}{2}$。<br>"
         r"2式を比べて $\cos\dfrac{A}{2}>0$ で割ると　$r=4R\sin\dfrac{A}{2}\sin\dfrac{B}{2}\sin\dfrac{C}{2}$　$\blacksquare$<br>"
         r"(2) 積→和の公式と $\cos\dfrac{B+C}{2}=\sin\dfrac{A}{2}$ より<br>"
         r"$\sin\dfrac{B}{2}\sin\dfrac{C}{2}=\dfrac12\left(\cos\dfrac{B-C}{2}-\cos\dfrac{B+C}{2}\right)\leqq\dfrac12\left(1-\sin\dfrac{A}{2}\right)$（等号は $B=C$ のとき）<br>"
         r"$s=\sin\dfrac{A}{2}$ とおくと $0<s<1$ で，(1) より<br>"
         r"$\dfrac{r}{4R}=s\sin\dfrac{B}{2}\sin\dfrac{C}{2}\leqq\dfrac{s(1-s)}{2}=\dfrac12\left\{\dfrac14-\left(s-\dfrac12\right)^2\right\}\leqq\dfrac18$<br>"
         r"よって $r\leqq\dfrac{R}{2}$，すなわち $R\geqq2r$ である。$\blacksquare$<br>"
         r"等号は $B=C$ かつ $s=\dfrac12$（$A=\dfrac{\pi}{3}$）のとき，すなわち <b>正三角形のとき</b> に成り立つ。",
  "note": r"$R\geqq2r$ はオイラーの不等式とよばれ，外心と内心の距離 $d$ について成り立つ等式 $d^2=R^2-2Rr$（オイラーの定理）からも分かる。(1) の等式は，三角形の辺や半径を角の三角関数で表して比べる典型的な手法である。",
  "ex": r"三角形 ABC の外接円の半径を $R$，内接円の半径を $r$ とするとき，$\dfrac{r}{R}=\cos A+\cos B+\cos C-1$ が成り立つことを示せ。",
  "exa": r"(1) の等式と，和と積の公式の節の練習の等式 $\cos A+\cos B+\cos C=1+4\sin\dfrac{A}{2}\sin\dfrac{B}{2}\sin\dfrac{C}{2}$ から従う"},
]})


@_v
def _v9():
    import sympy as sp
    from sympy import sqrt, Rational as R
    P = math.pi
    M, m = _maxmin(lambda t: math.cos(2 * t) + 2 * math.sin(t), 0, 2 * P)
    assert abs(M - 1.5) < 1e-9 and abs(m + 3) < 1e-9
    _same_roots(lambda t: math.cos(2 * t) + 2 * math.sin(t) - 1.5, [P / 6, 5 * P / 6])
    assert abs(math.cos(3 * P) + 2 * math.sin(1.5 * P) + 3) < 1e-12
    M, m = _maxmin(lambda t: math.cos(2 * t) - 4 * math.cos(t), 0, 2 * P)
    assert abs(M - 5) < 1e-9 and abs(m + 3) < 1e-9 and abs(math.cos(2 * P) - 4 * math.cos(P) - 5) < 1e-12
    M, m = _maxmin(lambda t: math.sin(t) * math.cos(t) + math.sin(t) + math.cos(t), 0, P)
    assert abs(M - 0.5 - math.sqrt(2)) < 1e-9 and abs(m + 1) < 1e-12
    g = lambda t: math.sin(t) * math.cos(t) + math.sin(t) + math.cos(t)
    assert abs(g(P / 4) - 0.5 - math.sqrt(2)) < 1e-12 and abs(g(P) + 1) < 1e-12
    h = lambda t: math.sin(2 * t) - 2 * (math.sin(t) + math.cos(t))
    M, m = _maxmin(h, 0, 2 * P)
    assert abs(M - 1 - 2 * math.sqrt(2)) < 1e-9 and abs(m + 2) < 1e-9
    assert abs(h(5 * P / 4) - 1 - 2 * math.sqrt(2)) < 1e-12 and abs(h(0) + 2) < 1e-12 and abs(h(P / 2) + 2) < 1e-12
    _same_roots(lambda t: h(t) + 2, [0, P / 2])
    # 扇形の長方形（座標で長方形であることも確認）
    for ang, Fmax, thb in [(P / 3, math.sqrt(3) / 6, P / 6), (P / 4, (math.sqrt(2) - 1) / 2, P / 8)]:
        k = math.tan(ang)
        def F(t):
            Px, Py = math.cos(t), math.sin(t)
            Sx = Py / k
            return (Px - Sx) * Py
        M, _ = _maxmin(F, 1e-9, ang - 1e-9)
        assert abs(M - Fmax) < 1e-9 and abs(F(thb) - Fmax) < 1e-12
    t = 0.37
    assert abs((math.cos(t) - math.sin(t) / math.sqrt(3)) * math.sin(t) - (2 * math.sin(2 * t + P / 6) - 1) / (2 * math.sqrt(3))) < 1e-12
    # 解の個数
    def count(fun, a):
        return len(_roots(lambda x: fun(x) - a, 0, 2 * P, 40000))
    f1 = lambda x: math.sin(x) * math.cos(x) + math.sin(x) + math.cos(x)
    r2 = math.sqrt(2)
    assert -1 < 0.5 - r2 < 0.5 + r2
    for a, n in [(-1.3, 0), (-1, 2), (-0.96, 4), (-0.93, 4), (0.5 - r2, 3), (-0.9, 2), (0, 2), (1.5, 2), (1.9, 2), (0.5 + r2, 1), (2, 0)]:
        assert count(f1, a) == n, (a, count(f1, a))
    f2 = lambda x: math.sin(2 * x) - 2 * (math.sin(x) + math.cos(x))
    for a, n in [(-2.5, 0), (-2, 2), (-1.95, 4), (-1.85, 4), (1 - 2 * r2, 3), (-1.8, 2), (0, 2), (3.8, 2), (1 + 2 * r2, 1), (4, 0)]:
        assert count(f2, a) == n, (a, count(f2, a))
    for a in [-1 + 1e-9, -0.97, -0.93, 0.5 - r2 - 1e-12]:          # -1<a<1/2-√2 での2つの t の位置
        t1, t2 = -1 - math.sqrt(2 * (a + 1)), -1 + math.sqrt(2 * (a + 1))
        assert -r2 < t1 < -1 < t2 < r2 - 2
    x = sp.symbols("x")
    assert sp.expand((x + 1)**2 / 2 - 1 - ((x**2 - 1) / 2 + x)) == 0
    _eq(R(1, 2) * (1 - sqrt(2))**2 - 1, R(1, 2) - sqrt(2)); _eq(2 * (R(1, 2) - sqrt(2)) + 2, (sqrt(2) - 1)**2)
    # 半円の台形
    M, _ = _maxmin(lambda t: (1 + math.cos(t)) * math.sin(t), 0, P / 2)
    assert abs(M - 3 * math.sqrt(3) / 4) < 1e-9 and abs((1 + math.cos(P / 3)) * math.sin(P / 3) - 3 * math.sqrt(3) / 4) < 1e-12
    c = sp.symbols("c")
    assert sp.expand((1 + c)**3 * (1 - c) - (1 + 2 * c - 2 * c**3 - c**4)) == 0
    assert sp.expand(R(27, 16) - (1 + c)**3 * (1 - c) - (c - R(1, 2))**2 * (c**2 + 3 * c + R(11, 4))) == 0
    assert sp.expand((c + R(3, 2))**2 + R(1, 2) - (c**2 + 3 * c + R(11, 4))) == 0
    assert Fr(3, 2)**4 / 3 == Fr(27, 16)
    # 円に内接する二等辺三角形：頂点 (0,1)，底辺 y=-cos u，半幅 sin u
    M, _ = _maxmin(lambda u: math.sin(u) * (1 + math.cos(u)), 0, P)
    assert abs(M - 3 * math.sqrt(3) / 4) < 1e-9
    # sin(aπ cos x) = cos(aπ sin x)
    for a, n in [(1, 4), (2, 12), (0.5, 3)]:
        rr = _roots(lambda x: math.sin(a * P * math.cos(x)) - math.cos(a * P * math.sin(x)), 0, 2 * P, 80000)
        assert len(rr) == n, (a, rr)
    rr = _roots(lambda x: math.sin(P * math.cos(x)) - math.sin(P * math.sin(x)), 0, 2 * P, 80000)
    assert len(rr) == 6 and all(abs(u - v) < 1e-5 for u, v in zip(rr, [0, P / 4, P / 2, P, 5 * P / 4, 3 * P / 2]))
    sq = [Fr(9, 16), Fr(1, 16), Fr(25, 16)]
    assert all(u + v != 2 for u in sq for v in sq) and Fr(25, 16) < 2 < Fr(49, 16) and Fr(9, 4) > 2
    # R ≥ 2r と r = 4R sin(A/2) sin(B/2) sin(C/2)
    rnd = random.Random(9)
    for _ in range(500):
        pts = [(rnd.uniform(-3, 3), rnd.uniform(-3, 3)) for _ in range(3)]
        (x1, y1), (x2, y2), (x3, y3) = pts
        S2 = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        if S2 < 0.05:
            continue
        a_ = math.dist(pts[1], pts[2]); b_ = math.dist(pts[2], pts[0]); c_ = math.dist(pts[0], pts[1])
        A = math.acos((b_**2 + c_**2 - a_**2) / (2 * b_ * c_)); B = math.acos((c_**2 + a_**2 - b_**2) / (2 * c_ * a_)); C = P - A - B
        Rr = a_ * b_ * c_ / (2 * S2); rr_ = S2 / (a_ + b_ + c_)
        assert abs(rr_ - 4 * Rr * math.sin(A / 2) * math.sin(B / 2) * math.sin(C / 2)) < 1e-9
        assert Rr >= 2 * rr_ - 1e-12
        assert abs(rr_ / Rr - (math.cos(A) + math.cos(B) + math.cos(C) - 1)) < 1e-9
        assert abs(a_ - rr_ * (1 / math.tan(B / 2) + 1 / math.tan(C / 2))) < 1e-9


# ==== END SECTIONS
CH = {"no": 12, "sections": SEC}


def verify():
    for f in VS:
        f()
    items = [it for s in SEC for it in s["items"]]
    cnt = {k: sum(1 for it in items if it["lv"] == k) for k in range(1, 6)}
    assert len(SEC) == 9 and 42 <= len(items) <= 48, (len(SEC), len(items))
    assert cnt == {1: 10, 2: 12, 3: 12, 4: 7, 5: 6}, cnt          # 47題：★5 は6題
    for s in SEC:
        lv = [it["lv"] for it in s["items"]]
        assert lv == sorted(lv), s["title"]                       # 節の中は易しい順
        for it in s["items"]:
            for k in ("title", "q", "hint", "sol", "note", "ex", "exa"):
                txt = it.get(k, "")
                assert k == "note" or txt, (it["title"], k)
                assert not any(ord(ch) < 32 for ch in txt), (it["title"], k)   # \t などの混入なし
                body = txt.split("<svg")[0] + "".join(p.split("</svg>")[-1] for p in txt.split("<svg")[1:])
                assert body.count("$") % 2 == 0 and "$$" not in body, (it["title"], k)
