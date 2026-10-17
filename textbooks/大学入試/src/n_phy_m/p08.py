"""問題集 第8章 剛体のつりあい。CH に問題、verify() で答えを sympy で検算する。"""
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


def _ar(x1, y1, x2, y2, c="#333", w=1.2, hs=6):
    a = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - hs * math.cos(a - 0.4), y2 - hs * math.sin(a - 0.4))
    p2 = (x2 - hs * math.cos(a + 0.4), y2 - hs * math.sin(a + 0.4))
    return (_ln(x1, y1, x2, y2, c, w) +
            f'<polygon points="{x2:.1f},{y2:.1f} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}" fill="{c}"/>')


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _arc(cx, cy, r, a1, a2, c="#555"):
    """角 a1→a2（度、反時計回り、y 軸は上向きとして）の円弧"""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    return f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 0 {x2:.1f},{y2:.1f}" fill="none" stroke="{c}" stroke-width="1"/>'


def _hatch_h(x1, x2, y, down=True):
    s = [_ln(x1, y, x2, y, "#333", 1.6)]
    x = x1
    while x < x2 - 1:
        s.append(_ln(x, y + (6 if down else -6), x + 6, y, "#777", 0.8))
        x += 8
    return "".join(s)


def _hatch_v(x, y1, y2):
    s = [_ln(x, y1, x, y2, "#333", 1.6)]
    y = y1
    while y < y2 - 1:
        s.append(_ln(x, y + 6, x + 6, y, "#777", 0.8))
        y += 8
    return "".join(s)


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _fig_rod2():
    u, x0, y = 100, 30, 70          # 1 m = 100px
    xa, xc, xb = x0, x0 + 1.5 * u, x0 + 2.0 * u
    s = [_hatch_h(x0 - 15, xb + 15, 15, down=False), _ln(xa, 15, xa, y - 3, "#1d4e89", 1.3), _ln(xc, 15, xc, y - 3, "#1d4e89", 1.3),
         f'<rect x="{xa}" y="{y - 3}" width="{xb - xa}" height="6" fill="#d9d9d9" stroke="#333" stroke-width="1"/>',
         _tx(xa, y + 18, "A", 11, anchor="middle"), _tx(xc, y + 18, "C", 11, anchor="middle"), _tx(xb, y + 18, "B", 11, anchor="middle"),
         _ln(xa, y + 26, xc, y + 26, "#777", 0.8), _tx((xa + xc) / 2, y + 38, "1.5 m", 10, anchor="middle"),
         _ln(xa, y + 44, xb, y + 44, "#777", 0.8), _tx((xa + xb) / 2, y + 56, "2.0 m", 10, anchor="middle")]
    return _svg(260, 132, s)


def _fig_ladder():
    wx, fy, L, th = 200, 150, 150, math.radians(60)
    bx, ty = wx - L * math.cos(th), fy - L * math.sin(th)
    s = [_hatch_h(40, wx, fy), _hatch_v(wx, 10, fy),
         _ln(bx, fy, wx, ty, "#1d4e89", 4), _arc(bx, fy, 22, 0, 60), _tx(bx + 26, fy - 8, "θ", 11, True),
         _tx(bx - 4, fy + 14, "床（あらい）", 10, anchor="middle"), _tx(wx - 6, 26, "壁（なめらか）", 10, anchor="end")]
    return _svg(240, 168, s)


def _fig_hinge():
    ax, y, L = 30, 112, 170
    cy = y - L * math.tan(math.radians(30))
    bx = ax + L
    s = [_hatch_v(ax - 6, 5, y + 25),
         f'<rect x="{ax}" y="{y - 3}" width="{L}" height="6" fill="#d9d9d9" stroke="#333" stroke-width="1"/>',
         f'<circle cx="{ax + 3}" cy="{y}" r="4" fill="#fff" stroke="#333" stroke-width="1.2"/>',
         _ln(bx, y - 3, ax, cy, "#1d4e89", 1.3), _ln(bx - 3, y + 3, bx - 3, y + 18, "#333", 1.2),
         f'<rect x="{bx - 15}" y="{y + 18}" width="24" height="18" fill="#e8eef8" stroke="#333" stroke-width="1"/>',
         _arc(bx, y, 26, 150, 180), _tx(bx - 34, y - 8, "30°", 10, anchor="end"),
         _tx(ax + 8, y + 18, "A", 11), _tx(bx + 6, y + 4, "B", 11), _tx(ax + 6, cy + 4, "C", 11)]
    return _svg(240, 156, s)


def _fig_step():
    fy, r, h = 130, 50, 25
    ox, oy = 100, fy - r
    d = math.sqrt(r * r - (r - h) ** 2)
    px, py = ox + d, fy - h
    s = [_hatch_h(20, px, fy),
         f'<polygon points="{px:.1f},{py} 240,{py} 240,{fy} {px:.1f},{fy}" fill="#e6e6e6" stroke="#333" stroke-width="1.2"/>',
         f'<circle cx="{ox}" cy="{oy}" r="{r}" fill="#f4f7fb" stroke="#333" stroke-width="1.4"/>',
         f'<circle cx="{ox}" cy="{oy}" r="2" fill="#333"/>', _ar(ox, oy, ox + 40, oy, "#c0392b", 1.6),
         _tx(ox + 22, oy - 6, "F", 11, True, c="#c0392b", anchor="middle"), _tx(ox - 6, oy + 4, "O", 11, anchor="end"),
         _tx(px + 6, py - 6, "P", 11), _ln(248, py, 248, fy, "#555", 1), _ln(244, py, 252, py, "#555", 1),
         _ln(244, fy, 252, fy, "#555", 1), _tx(254, (py + fy) / 2 + 4, "h", 11, True)]
    return _svg(268, 142, s)


CH = {8: {
"goal": r"剛体が静止する条件は「力のつりあい（並進しない）」と「力のモーメントのつりあい（回転しない）」の2つ。未知の力がたくさん集まる点のまわりのモーメントを考えると、式が簡単になる。<br>（数値は有効数字2桁、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$ とする。）",
"items": [
 {"lv": "A", "tag": "力のモーメント",
  "q": r"長さ $1.2\,\mathrm{m}$ の軽い棒を、左端から $0.40\,\mathrm{m}$ の点 O で支え、棒の左端に重さ $30\,\mathrm{N}$ のおもりをつるした。<br>(1) 重さ $20\,\mathrm{N}$ のおもりを、O から右に何 $\mathrm m$ の点につるせば、棒は水平につりあうか。<br>(2) そのとき、支点が棒を支える力の大きさを求めよ。<br>(3) (1) のおもりのかわりに、棒の右端を鉛直下向きに引いて水平につりあわせるには、何 $\mathrm N$ の力が必要か。",
  "a": r"(1) $0.60\,\mathrm{m}$　(2) $50\,\mathrm{N}$　(3) $15\,\mathrm{N}$",
  "s": r"O のまわりの力のモーメントのつりあいを考える（支点の力は O を通るのでモーメントが $0$）。<br>(1) $30\times0.40=20\times x$ より $x=0.60\,\mathrm{m}$。<br>(2) 鉛直方向のつりあい：$30+20=50\,\mathrm{N}$。<br>(3) 右端は O から $0.80\,\mathrm{m}$。$30\times0.40=F\times0.80$ より $F=15\,\mathrm{N}$。<br><b>ポイント</b>：力のモーメント＝力の大きさ×うでの長さ（回転軸から作用線までの距離）。支点のまわりで考えると支点の力が消える。"},
 {"lv": "A", "tag": "重心",
  "q": r"長さ $0.90\,\mathrm{m}$、質量 $2.0\,\mathrm{kg}$ の一様な棒の左端に質量 $1.0\,\mathrm{kg}$ の小球 P を、右端に質量 $2.0\,\mathrm{kg}$ の小球 Q を取りつけた。<br>(1) 全体の重心の位置を、棒の左端からの距離で答えよ。<br>(2) この物体を1本の糸でつるして棒を水平に保つには、糸をどこに結べばよいか。<br>(3) そのときの糸の張力の大きさを求めよ。",
  "a": r"(1) $0.54\,\mathrm{m}$　(2) 左端から $0.54\,\mathrm{m}$ の点（重心）　(3) $49\,\mathrm{N}$",
  "s": r"(1) 一様な棒の重心は中点（左端から $0.45\,\mathrm{m}$）。$x_G=\frac{1.0\times0+2.0\times0.45+2.0\times0.90}{1.0+2.0+2.0}=\frac{2.7}{5.0}=0.54\,\mathrm{m}$。<br>(2) 重心の真上でつるせば、重力のモーメントが $0$ になって水平に保たれる。<br>(3) $5.0\times9.8=49\,\mathrm{N}$。<br><b>ポイント</b>：重心の座標は「質量で重みをつけた平均」。剛体は重心に全重力がはたらくとして扱える。"},
 {"lv": "A", "tag": "偶力",
  "q": r"(1) 偶力とは何か。また、偶力の合力と、偶力のモーメントの性質を述べよ。<br>(2) 半径 $0.15\,\mathrm{m}$ の円形のハンドルの直径の両端に、ハンドルの面内で直径に垂直に、互いに逆向きで大きさ $20\,\mathrm{N}$ の力を加えた。偶力のモーメントの大きさを求めよ。",
  "a": r"(1) 解説参照　(2) $6.0\,\mathrm{N\cdot m}$",
  "s": r"(1) 大きさが等しく、向きが逆で、作用線が平行にずれている2力の組を偶力という。合力は $0$ なので物体を並進させないが、回転させるはたらきがある。偶力のモーメントは $Fd$（$d$ は2つの作用線の間の距離）で、どの点のまわりで計算しても同じ値になる。<br>(2) 作用線の間の距離は直径 $0.30\,\mathrm{m}$。$20\times0.30=6.0\,\mathrm{N\cdot m}$。<br><b>ポイント</b>：偶力は1つの力でおきかえることはできない（合力が $0$ なのに回転させる）。"},
 {"lv": "A", "tag": "棒のつりあい",
  "q": r"長さ $2.0\,\mathrm{m}$、質量 $6.0\,\mathrm{kg}$ の一様な棒 AB を、端 A と、A から $1.5\,\mathrm{m}$ の点 C で、鉛直な2本の糸でつるして水平に保った。<br>" + _fig_rod2() +
       r"(1) 点 C の糸の張力の大きさを求めよ。<br>(2) 点 A の糸の張力の大きさを求めよ。<br>(3) 棒の端 B に質量 $m$ のおもりをつるす。棒が水平のまま（A の糸がたるまない）であるための $m$ の最大値を求めよ。",
  "a": r"(1) $39\,\mathrm{N}$　(2) $20\,\mathrm{N}$（$19.6\,\mathrm{N}$）　(3) $6.0\,\mathrm{kg}$",
  "s": r"重力 $6.0\times9.8=58.8\,\mathrm{N}$ は中点（A から $1.0\,\mathrm{m}$）にはたらく。<br>(1) A のまわりのモーメント：$T_C\times1.5=58.8\times1.0$ より $T_C=39.2\fallingdotseq39\,\mathrm{N}$。<br>(2) 鉛直方向のつりあい：$T_A=58.8-39.2=19.6\fallingdotseq20\,\mathrm{N}$。<br>(3) A の糸がたるむ直前は $T_A=0$。C のまわりのモーメント：棒の重心は C の左 $0.50\,\mathrm{m}$、B は C の右 $0.50\,\mathrm{m}$ なので $58.8\times0.50=m\times9.8\times0.50$、$m=6.0\,\mathrm{kg}$。<br><b>ポイント</b>：「糸がたるむ（離れる）直前」は、その張力（垂直抗力）を $0$ とおいてモーメントのつりあいを考える。"},
 {"lv": "B", "tag": "立てかけたはしご",
  "q": r"長さ $l$、質量 $m$ の一様なはしごを、なめらかな鉛直の壁とあらい水平な床の間に、床となす角 $\theta$ で立てかけた。床とはしごの間の静止摩擦係数を $\mu$、重力加速度の大きさを $g$ とする。<br>" + _fig_ladder() +
       r"(1) はしごが静止しているとき、壁がはしごを押す力 $N_1$、床からの垂直抗力 $N_2$、床からの静止摩擦力 $f$ の大きさを求めよ。<br>(2) はしごがすべらないための $\tan\theta$ の条件を求めよ。<br>(3) $\theta=60^\circ$、$\mu=0.40$ のとき、質量 $2m$ の人がはしごを登る。はしごがすべらずに、人がはしごの下端から距離 $x$ の位置まで登れるとき、$\frac xl$ の最大値を求めよ。人は質点とみなす。",
  "a": r"(1) $N_1=f=\frac{mg}{2\tan\theta}$、$N_2=mg$　(2) $\tan\theta\geqq\frac{1}{2\mu}$　(3) $0.79$",
  "s": r"(1) 鉛直：$N_2=mg$。水平：$f=N_1$。下端のまわりのモーメント（$N_2,\ f$ が消える）：$N_1\cdot l\sin\theta=mg\cdot\frac l2\cos\theta$ より $N_1=\frac{mg}{2\tan\theta}$。<br>(2) $f\leqq\mu N_2$ より $\frac{mg}{2\tan\theta}\leqq\mu mg$、$\tan\theta\geqq\frac{1}{2\mu}$。<br>(3) 下端のまわりのモーメント：$N_1l\sin\theta=mg\frac l2\cos\theta+2mg\,x\cos\theta$ より $N_1=\frac{mg}{\tan\theta}\left(\frac12+\frac{2x}{l}\right)$。床の垂直抗力は $N_2=3mg$。すべらない条件 $N_1\leqq\mu N_2$ より $\frac12+\frac{2x}{l}\leqq3\mu\tan\theta=1.2\sqrt3\fallingdotseq2.078$。$\frac xl\leqq0.789\fallingdotseq0.79$。<br><b>ポイント</b>：モーメントの軸は、未知の力が2つ集まる下端にとると楽。人が高く登るほど壁からの力（＝必要な摩擦力）が大きくなる。"},
 {"lv": "B", "tag": "すべるか倒れるか",
  "q": r"あらい水平な床の上に、幅 $a=0.40\,\mathrm{m}$、高さ $b=1.0\,\mathrm{m}$、質量 $m$ の一様な直方体を置く。直方体の右側面の、床からの高さ $h$ の点に、水平右向きの力 $F$ を加え、$F$ を $0$ からゆっくり大きくする。床との静止摩擦係数を $\mu$ とする。<br>(1) 直方体が静止している間、$F$ を大きくすると、床からの垂直抗力の作用点はどちらへ移るか。<br>(2) すべらないとして、直方体が傾き始めるときの $F$ を $m,\ g,\ a,\ h$ で表せ。<br>(3) $h=b$ のとき、直方体が傾く前にすべり出すための $\mu$ の条件を求めよ。",
  "a": r"(1) 右へ（右下の辺に近づく）　(2) $F=\frac{mga}{2h}$　(3) $\mu<0.20$",
  "s": r"(1) $F$ は直方体を右下の辺のまわりに回そうとする。これを打ち消すため、垂直抗力の作用点は右へ移っていく。<br>(2) 傾き始めるのは、垂直抗力の作用点が右下の辺に達したとき。その辺のまわりのモーメント：$Fh=mg\cdot\frac a2$ より $F=\frac{mga}{2h}$。<br>(3) すべり出すときの力は $\mu mg$。これが (2) の値より小さければ先にすべる：$\mu mg<\frac{mga}{2b}$、$\mu<\frac{a}{2b}=0.20$。<br><b>ポイント</b>：「すべる条件（$F>\mu mg$）」と「倒れる条件（作用点が端に来る）」をそれぞれ求めて、小さい力で起こる方が先に起こる。"},
 {"lv": "B", "tag": "斜面上の直方体",
  "q": r"傾斜角 $\theta$ を変えられるあらい板の上に、斜面方向の底面の長さ $a=0.30\,\mathrm{m}$、高さ $b=0.60\,\mathrm{m}$ の一様な直方体を置き、$\theta$ を $0$ から少しずつ大きくする。直方体と板の間の静止摩擦係数は $\mu=0.60$ である。<br>(1) 倒れないとして、直方体がすべり出すときの $\tan\theta$ を求めよ。<br>(2) すべらないとして、直方体が倒れ始めるときの $\tan\theta$ を求めよ。<br>(3) すべりと転倒のどちらが先に起こるか。",
  "a": r"(1) $0.60$　(2) $0.50$　(3) 転倒が先",
  "s": r"(1) $mg\sin\theta=\mu mg\cos\theta$ より $\tan\theta=\mu=0.60$。<br>(2) 倒れ始めるのは、重心を通る鉛直線が、底面の下側の辺を通るとき。重心は底面から $\frac b2$、下側の辺から斜面方向に $\frac a2$ の位置なので、$\tan\theta=\frac{a/2}{b/2}=\frac ab=0.50$。<br>(3) $\tan\theta$ が $0.50$ に達した時点でまだすべっていない（$0.50<0.60$）ので、先に倒れる。<br><b>ポイント</b>：直方体が倒れる条件は「重心の真下が底面からはみ出す」こと。背の高い物体ほど倒れやすい。"},
 {"lv": "B", "tag": "ちょうつがいと糸",
  "q": r"長さ $l$、質量 $4.0\,\mathrm{kg}$ の一様な棒 AB の端 A を、鉛直な壁にちょうつがいで取りつけ、端 B に質量 $2.0\,\mathrm{kg}$ のおもりをつるす。B と、A の真上の壁の点 C を軽い糸で結んだところ、棒は水平になって静止した。糸と棒のなす角は $30^\circ$ である。<br>" + _fig_hinge() +
       r"(1) 糸の張力の大きさを求めよ。<br>(2) ちょうつがいが棒に及ぼす力の、水平成分と鉛直成分の大きさと向きを求めよ。<br>(3) ちょうつがいが棒に及ぼす力の大きさを求めよ。",
  "a": r"(1) $78\,\mathrm{N}$　(2) 水平成分 $68\,\mathrm{N}$（壁から離れる向き）、鉛直成分 $20\,\mathrm{N}$（上向き）　(3) $71\,\mathrm{N}$",
  "s": r"(1) A のまわりのモーメント（ちょうつがいの力が消える）：張力の棒に垂直な成分 $T\sin30^\circ$ のうでは $l$。$T\sin30^\circ\cdot l=4.0\times9.8\times\frac l2+2.0\times9.8\times l$ より $\frac T2=19.6+19.6$、$T=78.4\fallingdotseq78\,\mathrm{N}$。<br>(2) 水平：張力の水平成分 $T\cos30^\circ\fallingdotseq67.9\,\mathrm{N}$ は壁に向かう向きなので、ちょうつがいの力の水平成分は壁から離れる向きに $68\,\mathrm{N}$。鉛直：$6.0\times9.8=58.8\,\mathrm{N}$ のうち $T\sin30^\circ=39.2\,\mathrm{N}$ を糸が支えるので、残り $19.6\fallingdotseq20\,\mathrm{N}$ を上向きに支える。<br>(3) $\sqrt{67.9^2+19.6^2}\fallingdotseq71\,\mathrm{N}$。<br><b>ポイント</b>：ちょうつがいの力は向きがわからないので、水平・鉛直の2成分を未知数にする。その点のまわりのモーメントを考えれば、まず張力が求まる。"},
 {"lv": "B", "tag": "穴をあけた円板の重心",
  "q": r"半径 $R$ の一様な薄い円板（中心 O）から、OA を直径とする円（半径 $\frac R2$、A は円板の縁の点）の部分をくりぬいた。<br>(1) 残りの板の重心の位置を求めよ。<br>(2) 残りの板を、縁の点 P（$\mathrm{OP}\perp\mathrm{OA}$）で糸につるして静止させた。OP と鉛直線のなす角を $\alpha$ とするとき、$\tan\alpha$ を求めよ。",
  "a": r"(1) 直線 OA 上で、O から A と反対側へ $\frac R6$ の点　(2) $\frac16$",
  "s": r"(1) 質量は面積に比例する。もとの円板（面積 $\pi R^2$、重心 O）＝ 残りの板（面積 $\frac34\pi R^2$、重心 $x_G$）＋ くりぬいた円（面積 $\frac14\pi R^2$、重心は O から A の向きに $\frac R2$）。O を原点、A の向きを正とすると $0=\frac34x_G+\frac14\cdot\frac R2$ より $x_G=-\frac R6$。<br>(2) つるしたとき、重心 G は P の真下にくる。三角形 OPG は O で直角で、$\mathrm{OP}=R$、$\mathrm{OG}=\frac R6$。PG が鉛直なので $\tan\alpha=\frac{\mathrm{OG}}{\mathrm{OP}}=\frac16$。<br><b>ポイント</b>：穴のあいた物体の重心は「全体 ＝ 残り ＋ 穴」として、穴を負の質量のように扱うと求めやすい。"},
 {"lv": "C", "tag": "壁も床もあらいはしご",
  "q": r"長さ $l$、質量 $m$ の一様な棒を、あらい鉛直の壁とあらい水平な床の間に、床となす角 $\theta$ で立てかける。棒と床の間の静止摩擦係数を $\mu_1$、棒と壁の間の静止摩擦係数を $\mu_2$ とし、重力加速度の大きさを $g$ とする。$\theta$ を小さくしていくと、ある角で棒はすべり出した。<br>(1) すべり出す直前に、床と壁から棒が受ける摩擦力の向きを答えよ。<br>(2) すべり出す直前の $\tan\theta$ を $\mu_1,\ \mu_2$ で表せ。<br>(3) $\mu_1=\mu_2=0.50$ のとき、すべらずに立てかけられる角の最小値について、$\tan\theta$ の値を求め、壁がなめらかな場合（$\mu_2=0$）の値と比べよ。",
  "a": r"(1) 床：水平で壁に向かう向き、壁：鉛直上向き　(2) $\tan\theta=\frac{1-\mu_1\mu_2}{2\mu_1}$　(3) $0.75$（なめらかな壁では $1.0$ で、壁の摩擦があると小さい角まで立てかけられる）",
  "s": r"(1) 棒は、下端が壁から離れる向きに、上端が壁に沿って下向きにすべろうとする。摩擦力はその逆向きなので、床からは壁に向かう水平な向き、壁からは鉛直上向き。<br>(2) 床の垂直抗力 $N_1$、摩擦力 $f_1=\mu_1N_1$、壁の垂直抗力 $N_2$、摩擦力 $f_2=\mu_2N_2$（すべり出す直前は両方とも最大摩擦力）。<br>水平：$f_1=N_2$ より $N_2=\mu_1N_1$。鉛直：$N_1+f_2=mg$ より $N_1(1+\mu_1\mu_2)=mg$。<br>下端のまわりのモーメント：$N_2\,l\sin\theta+f_2\,l\cos\theta=mg\frac l2\cos\theta$。<br>両辺を $N_1l\cos\theta$ で割ると $\mu_1\tan\theta+\mu_1\mu_2=\frac{1+\mu_1\mu_2}{2}$、$\tan\theta=\frac{1-\mu_1\mu_2}{2\mu_1}$。<br>(3) $\tan\theta=\frac{1-0.25}{1.0}=0.75$。$\mu_2=0$ なら $\tan\theta=\frac{1}{2\mu_1}=1.0$。壁の摩擦が棒の一部を支えるので、より小さい角（寝かせた状態）まですべらない。<br><b>ポイント</b>：はしごがすべり出すとき、上端と下端は同時にすべるので、両方の摩擦力が最大摩擦力に達している。"},
 {"lv": "C", "tag": "段差に乗り上げる円柱",
  "q": r"半径 $r$、質量 $m$ の一様な円柱が水平な床の上にあり、高さ $h=\frac r2$ の段差の角 P に接している（円柱の軸は段差の辺に平行）。この円柱を段差の上に引き上げたい。円柱は P ですべらないものとし、重力加速度の大きさを $g$ とする。<br>" + _fig_step() +
       r"(1) 円柱の中心 O に水平な力 $F$ を加える。円柱が床から浮き上がり始めるための $F$ の最小値を求めよ。<br>(2) 中心 O に加える力の向きを自由に選べるとき、浮き上がらせるのに必要な力の最小値と、その向きを求めよ。<br>(3) 円柱の表面のどこに力を加えてもよいとき、必要な力の最小値を求めよ。",
  "a": r"(1) $\sqrt3\,mg$　(2) $\frac{\sqrt3}{2}mg$、OP に垂直で、水平から $60^\circ$ 上向き（段差側）　(3) $\frac{\sqrt3}{4}mg$",
  "s": r"浮き上がり始めるとき床からの垂直抗力は $0$ になり、円柱には重力・加える力・P からの力だけがはたらく。P のまわりのモーメントで考えると、P からの力が消える。<br>P は O より $r-h=\frac r2$ 低く、水平距離は $\sqrt{r^2-\left(\frac r2\right)^2}=\frac{\sqrt3}{2}r$。重力のモーメントは $mg\cdot\frac{\sqrt3}{2}r$。<br>(1) 水平な力のうでは $\frac r2$。$F\cdot\frac r2\geqq mg\cdot\frac{\sqrt3}{2}r$ より $F\geqq\sqrt3\,mg$。<br>(2) O に加える力のうでは最大で $\mathrm{OP}=r$（力を OP に垂直に加えるとき）。$F\cdot r=mg\cdot\frac{\sqrt3}{2}r$ より $F=\frac{\sqrt3}{2}mg$。OP は水平と $30^\circ$ をなすので、力の向きは水平から $60^\circ$ 上向き（段差側）。<br>(3) うでの最大値は、P から最も遠い点（P と直径の反対側の点 Q）に PQ に垂直な力を加えるときの $2r$。$F\cdot2r=mg\cdot\frac{\sqrt3}{2}r$ より $F=\frac{\sqrt3}{4}mg$。<br><b>ポイント</b>：同じモーメントを得るには、うでが長いほど小さな力ですむ。回転軸（P）から力の作用点までの距離が最大になる点を探す。"},
]}}


def verify():
    g = Rational(98, 10)
    # 8-1
    assert Rational(30 * 4, 10) / 20 == Rational(6, 10) and 30 * Rational(4, 10) / Rational(8, 10) == 15
    # 8-2
    xg = (1 * 0 + 2 * Rational(45, 100) + 2 * Rational(9, 10)) / 5
    assert xg == Rational(54, 100) and 5 * g == 49
    # 8-3
    assert 20 * Rational(30, 100) == 6
    # 8-4
    W = 6 * g
    TC = W * 1 / Rational(3, 2); _near(TC, 39); _near(W - TC, 20)
    m = symbols("m")
    assert solve(Eq(W * Rational(1, 2), m * g * Rational(1, 2)), m) == [6]
    # 8-5
    mm, gg, l, th, mu, x = symbols("m g l theta mu x", positive=True)
    N1 = solve(Eq(symbols("N1") * l * sin(th), mm * gg * l / 2 * cos(th)), symbols("N1"))[0]
    _eq(N1, mm * gg / (2 * tan(th)))
    N1p = solve(Eq(symbols("N1") * l * sin(th), mm * gg * l / 2 * cos(th) + 2 * mm * gg * x * cos(th)), symbols("N1"))[0]
    xs = solve(Eq(N1p.subs({th: pi / 3}), Rational(4, 10) * 3 * mm * gg), x)[0]
    _near(xs / l, 0.79)
    assert 1 / (2 * Rational(4, 10)) < sqrt(3)       # 人がいなければすべらない
    # 8-6
    a, b = Rational(4, 10), 1
    assert a / (2 * b) == Rational(1, 5)
    # 8-7
    assert Rational(3, 10) / Rational(6, 10) == Rational(1, 2) < Rational(6, 10)
    # 8-8
    T = solve(Eq(symbols("T") * sin(pi / 6), 4 * g / 2 + 2 * g), symbols("T"))[0]
    _near(T, 78)
    H = T * cos(pi / 6); V = 6 * g - T * sin(pi / 6)
    _near(H, 68); _near(V, 20); _near(sqrt(H ** 2 + V ** 2), 71)
    # 8-9
    xG = solve(Eq(0, Rational(3, 4) * symbols("xG") + Rational(1, 4) * Rational(1, 2)), symbols("xG"))[0]
    assert xG == Rational(-1, 6)    # R を単位として
    # 8-10
    m1, m2, N1s, N2s = symbols("mu1 mu2 N1 N2", positive=True)
    t = symbols("t", positive=True)    # tanθ
    s = solve([m1 * N1s - N2s, N1s + m2 * N2s - mm * gg], [N1s, N2s], dict=True)[0]
    # モーメント式を cosθ で割った形: N2 tanθ + μ2 N2 = mg/2
    tt = solve(Eq(s[N2s] * t + m2 * s[N2s], mm * gg / 2), t)[0]
    _eq(tt, (1 - m1 * m2) / (2 * m1))
    assert tt.subs({m1: Rational(1, 2), m2: Rational(1, 2)}) == Rational(3, 4)
    assert ((1 - m1 * 0) / (2 * m1)).subs(m1, Rational(1, 2)) == 1
    # 8-11 段差：P を原点とした座標で数値的にも確認
    r = symbols("r", positive=True)
    h = r / 2
    dx = sqrt(r ** 2 - (r - h) ** 2)
    _eq(dx, sqrt(3) * r / 2)
    F1 = mm * gg * dx / (r - h); _eq(F1, sqrt(3) * mm * gg)
    F2 = mm * gg * dx / r; _eq(F2, sqrt(3) * mm * gg / 2)
    F3 = mm * gg * dx / (2 * r); _eq(F3, sqrt(3) * mm * gg / 4)
    # (2) の向き：OP に垂直な単位ベクトルのうち、P のまわりで重力と逆向きのモーメントをもつもの
    PO = Matrix([-dx, r - h])       # P から O へ
    e = Matrix([Rational(1, 2), sqrt(3) / 2])
    assert simplify(PO.dot(e)) == 0
    torque = lambda rv, fv: rv[0] * fv[1] - rv[1] * fv[0]
    assert simplify(torque(PO, e)) < 0 and simplify(torque(PO, Matrix([0, -1]))) > 0
    assert math.isclose(math.degrees(math.atan2(math.sqrt(3) / 2, 0.5)), 60)
