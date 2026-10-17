"""問題集 第5章 円運動と慣性力。CH に問題、verify() で答えを sympy で検算する。"""
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


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _fig_ring():
    cx, cy, R = 110, 88, 56
    th = math.radians(60)
    bx, by = cx + R * math.sin(th), cy + R * math.cos(th)
    s = [_ln(cx, 12, cx, 160, "#999", 1, "4,3"), f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#333" stroke-width="1.6"/>',
         _ln(cx, cy, bx, by, "#555", 1, "3,2"), _ln(cx, cy, cx, cy + R, "#555", 1, "3,2"),
         f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="5" fill="#1d4e89"/>', _arc(cx, cy, 18, 270, 270 + 60),
         _tx(cx + 6, cy + 30, "θ", 11, True), _tx(cx - 6, cy - 4, "O", 11, anchor="end"),
         _tx((cx + bx) / 2 + 8, (cy + by) / 2 - 4, "R", 11, True),
         f'<path d="M{cx - 22},{20} A22,6 0 0 0 {cx + 22},{20}" fill="none" stroke="#c0392b" stroke-width="1.2"/>',
         _ar(cx + 14, 25.2, cx + 22, 20.5, "#c0392b", 1.2, 5), _tx(cx + 28, 22, "ω", 12, True, c="#c0392b")]
    return _svg(220, 165, s)


def _fig_halfpipe():
    fy, cx, r = 132, 170, 56
    cy = fy - r
    s = [_ln(10, fy, cx, fy, "#333", 1.4),
         f'<path d="M{cx},{fy} A{r},{r} 0 0 0 {cx},{fy - 2 * r}" fill="none" stroke="#333" stroke-width="1.6"/>',
         _ln(cx, cy, cx + r, cy, "#777", 1, "3,2"), f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="#333"/>',
         _tx(cx - 4, cy + 4, "O", 11, anchor="end"), _tx(cx + r / 2, cy - 4, "r", 11, True, anchor="middle"),
         _tx(cx, fy + 15, "B", 11, anchor="middle"), _tx(cx - 4, fy - 2 * r + 4, "C", 11, anchor="end"),
         f'<circle cx="60" cy="{fy - 6}" r="6" fill="#1d4e89"/>', _ar(72, fy - 6, 104, fy - 6, "#c0392b", 1.5),
         _tx(88, fy - 12, "v₀", 11, True, anchor="middle", c="#c0392b"), _tx(20, fy - 6, "A", 11)]
    return _svg(250, 148, s)


CH = {5: {
"goal": r"等速円運動では「中心向きの合力 $=mr\omega^2=m\frac{v^2}{r}$」。加速する観測者から見るときは慣性力 $-m\vec a$ を加えてつりあいで考える。鉛直面内の円運動は「力学的エネルギー保存＋中心方向の運動方程式」で解く。<br>（数値は有効数字2桁、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$ とする。）",
"items": [
 {"lv": "A", "tag": "等速円運動",
  "q": r"質量 $0.20\,\mathrm{kg}$ の小球が、半径 $0.50\,\mathrm{m}$ の円周上を周期 $2.0\,\mathrm{s}$ で等速円運動している。$\pi=3.14$ とする。<br>(1) 角速度を求めよ。　(2) 速さを求めよ。<br>(3) 加速度の大きさと向きを求めよ。　(4) 小球にはたらく合力（向心力）の大きさを求めよ。",
  "a": r"(1) $3.1\,\mathrm{rad/s}$　(2) $1.6\,\mathrm{m/s}$　(3) $4.9\,\mathrm{m/s^2}$、円の中心向き　(4) $0.99\,\mathrm{N}$",
  "s": r"(1) $\omega=\frac{2\pi}{T}=\frac{2\times3.14}{2.0}=3.14\fallingdotseq3.1\,\mathrm{rad/s}$。<br>(2) $v=r\omega=0.50\times3.14\fallingdotseq1.6\,\mathrm{m/s}$。<br>(3) $a=r\omega^2=0.50\times3.14^2\fallingdotseq4.9\,\mathrm{m/s^2}$。向きは常に円の中心向き。<br>(4) $F=ma=0.20\times4.93\fallingdotseq0.99\,\mathrm{N}$。<br><b>ポイント</b>：等速円運動は速さが一定でも速度の向きが変わるので、加速度（中心向き）がある。"},
 {"lv": "A", "tag": "円錐振り子",
  "q": r"長さ $0.50\,\mathrm{m}$ の軽い糸の一端を天井に固定し、他端に質量 $m$ のおもりをつけ、糸が鉛直と $60^\circ$ をなすようにして、おもりを水平面内で等速円運動させた。重力加速度の大きさを $g$ とし、$\pi=3.14$ とする。<br>(1) 糸の張力の大きさを $mg$ で表せ。<br>(2) 角速度を求めよ。<br>(3) 周期を求めよ。",
  "a": r"(1) $2mg$　(2) $6.3\,\mathrm{rad/s}$　(3) $1.0\,\mathrm{s}$",
  "s": r"円の半径は $r=0.50\sin60^\circ$。<br>(1) 鉛直方向のつりあい：$T\cos60^\circ=mg$ より $T=2mg$。<br>(2) 水平方向（中心向き）の運動方程式：$T\sin60^\circ=m(0.50\sin60^\circ)\omega^2$ より $\omega^2=\frac{T}{0.50m}=\frac{2g}{0.50}=39.2$、$\omega\fallingdotseq6.3\,\mathrm{rad/s}$。<br>(3) $T_{\text{周期}}=\frac{2\pi}{\omega}=\frac{6.28}{6.26}\fallingdotseq1.0\,\mathrm{s}$。<br><b>ポイント</b>：円錐振り子は「鉛直はつりあい、水平は円運動の方程式」。一般に $\omega=\sqrt{\frac{g}{l\cos\theta}}$ となる。"},
 {"lv": "A", "tag": "エレベーターと慣性力",
  "q": r"エレベーターの床に体重計を置き、質量 $50\,\mathrm{kg}$ の人が乗った。次の各場合に、体重計が人から受ける力（体重計の示す力）の大きさを求めよ。<br>(1) エレベーターが一定の速さで上昇しているとき<br>(2) 上向きに大きさ $1.4\,\mathrm{m/s^2}$ の加速度で動いているとき<br>(3) 下向きに大きさ $1.4\,\mathrm{m/s^2}$ の加速度で動いているとき<br>(4) エレベーターをつるすケーブルが切れて、自由落下しているとき",
  "a": r"(1) $4.9\times10^2\,\mathrm{N}$　(2) $5.6\times10^2\,\mathrm{N}$　(3) $4.2\times10^2\,\mathrm{N}$　(4) $0$",
  "s": r"エレベーター内で見ると、人には重力 $mg$、体重計からの垂直抗力 $N$、慣性力（加速度と逆向きに $ma$）がはたらき、つりあっている。体重計が受ける力は作用・反作用で $N$ に等しい。<br>(1) 加速度は $0$ なので $N=mg=490\fallingdotseq4.9\times10^2\,\mathrm{N}$。<br>(2) 慣性力は下向き：$N=m(g+a)=50\times11.2=5.6\times10^2\,\mathrm{N}$。<br>(3) 慣性力は上向き：$N=m(g-a)=50\times8.4=4.2\times10^2\,\mathrm{N}$。<br>(4) $a=g$（下向き）なので $N=m(g-g)=0$（無重量状態）。<br><b>ポイント</b>：慣性力は「観測者の加速度と逆向きに $ma$」。速度の向きではなく加速度の向きで決まる。"},
 {"lv": "A", "tag": "加速する車内の振り子",
  "q": r"水平な直線道路を一定の加速度 $a$ で加速している自動車の天井から、質量 $0.10\,\mathrm{kg}$ のおもりを糸でつるしたところ、糸は鉛直から角 $\theta$ だけ傾いて、車内で静止して見えた。重力加速度の大きさを $g$ とする。<br>(1) 車内の人から見て、おもりにはたらく慣性力の向きと大きさを答えよ。<br>(2) $\tan\theta$ を $a,\ g$ で表せ。<br>(3) $a=4.9\,\mathrm{m/s^2}$ のとき、$\tan\theta$ の値と糸の張力の大きさを求めよ。また、糸は進行方向の前方・後方のどちらに傾くか。",
  "a": r"(1) 進行方向と逆向き、大きさ $0.10a$（$ma$）　(2) $\tan\theta=\frac ag$　(3) $0.50$、$1.1\,\mathrm{N}$、後方",
  "s": r"(1) 自動車の加速度は進行方向なので、慣性力は進行方向と逆向きに $ma$。<br>(2) 車内では、重力 $mg$（下向き）、慣性力 $ma$（後ろ向き）、張力 $T$ がつりあう。張力の鉛直成分 $T\cos\theta=mg$、水平成分 $T\sin\theta=ma$ より $\tan\theta=\frac ag$。<br>(3) $\tan\theta=\frac{4.9}{9.8}=0.50$。$T=m\sqrt{g^2+a^2}=0.10\times\sqrt{9.8^2+4.9^2}\fallingdotseq1.1\,\mathrm{N}$。慣性力が後ろ向きなので、おもりは後方に傾く。<br><b>ポイント</b>：車内では「重力＋慣性力」が見かけの重力になる。糸はその向き（鉛直から後方へ $\theta$）に張る。"},
 {"lv": "B", "tag": "鉛直面内の円運動（糸）",
  "q": r"長さ $l$ の軽い糸の一端を点 O に固定し、他端に質量 $m$ の小球をつけ、最下点で水平に速さ $v_0$ を与えて、鉛直面内で円運動させる。糸が鉛直下向きと角 $\theta$ をなす位置での小球の速さを $v$、糸の張力の大きさを $T$ とする。重力加速度の大きさを $g$ とする。<br>(1) $v^2$ を $v_0,\ g,\ l,\ \theta$ で表せ。<br>(2) $T$ を $m,\ v_0,\ g,\ l,\ \theta$ で表せ。<br>(3) 小球が糸をたるませずに円軌道を1周するための $v_0$ の条件を求めよ。<br>(4) (3) の条件を満たすとき、最下点と最高点での張力の差は $v_0$ によらず一定であることを示し、その値を求めよ。",
  "a": r"(1) $v^2=v_0^2-2gl(1-\cos\theta)$　(2) $T=\frac{mv_0^2}{l}-mg(2-3\cos\theta)$　(3) $v_0\geqq\sqrt{5gl}$　(4) $6mg$",
  "s": r"(1) 最下点からの高さは $l(1-\cos\theta)$。力学的エネルギー保存より $\frac12mv_0^2=\frac12mv^2+mgl(1-\cos\theta)$。<br>(2) 中心方向の運動方程式：$m\frac{v^2}{l}=T-mg\cos\theta$。(1) を代入して $T=\frac{mv_0^2}{l}-2mg(1-\cos\theta)+mg\cos\theta=\frac{mv_0^2}{l}-mg(2-3\cos\theta)$。<br>(3) $T$ は $\theta=180^\circ$（最高点）で最小になる。そこで $T\geqq0$ となればよい。$\frac{mv_0^2}{l}-5mg\geqq0$ より $v_0\geqq\sqrt{5gl}$。<br>(4) 最下点 $\theta=0$ で $T_1=\frac{mv_0^2}{l}+mg$、最高点で $T_2=\frac{mv_0^2}{l}-5mg$。$T_1-T_2=6mg$ で $v_0$ によらない。<br><b>ポイント</b>：糸の円運動は「最高点で $T\geqq0$」が1周の条件。最高点で速さが $0$ でなくても糸はたるみうる。"},
 {"lv": "B", "tag": "回転円板と遠心力",
  "q": r"水平な円板が、鉛直な中心軸のまわりに一定の角速度 $\omega$ で回転している。中心から $0.20\,\mathrm{m}$ の位置に質量 $m$ の小物体を置いたところ、小物体は円板に対して静止したまま回った。小物体と円板の間の静止摩擦係数は $0.40$ である。<br>(1) 小物体にはたらく静止摩擦力の向きと大きさを、$m,\ \omega$ を用いて表せ。<br>(2) 小物体がすべり出さないための $\omega$ の最大値を求めよ。<br>(3) 円板とともに回転する観測者から見たとき、小物体が静止している理由を説明せよ。<br>(4) 中心からの距離を2倍にすると、(2) の最大値は何倍になるか。",
  "a": r"(1) 円の中心向き、$0.20m\omega^2$　(2) $4.4\,\mathrm{rad/s}$　(3) 解説参照　(4) $\frac{1}{\sqrt2}$ 倍",
  "s": r"(1) 等速円運動の向心力は静止摩擦力だけがになう。中心向きに $f=mr\omega^2=0.20m\omega^2$。<br>(2) $f\leqq\mu mg$ より $0.20\omega^2\leqq0.40\times9.8$、$\omega\leqq\sqrt{19.6}\fallingdotseq4.4\,\mathrm{rad/s}$。<br>(3) 回転する観測者から見ると、小物体には中心から遠ざかる向きに遠心力 $mr\omega^2$ がはたらき、これと中心向きの静止摩擦力がつりあっている。<br>(4) $\omega_{\max}=\sqrt{\frac{\mu g}{r}}$ なので、$r$ を2倍にすると $\frac{1}{\sqrt2}$ 倍。<br><b>ポイント</b>：地上から見れば「摩擦力＝向心力」、回転系から見れば「摩擦力と遠心力のつりあい」。どちらか一方の立場で式を立て、両方を混ぜない。"},
 {"lv": "B", "tag": "球面から離れる条件",
  "q": r"半径 $R$ のなめらかな半球が水平面上に固定されている。その頂上に置いた質量 $m$ の小物体にごくわずかな速さを与えたところ、小物体は球面上をすべり下り、やがて球面から離れた。半球の中心 O から小物体への向きが鉛直となす角を $\theta$ とし、重力加速度の大きさを $g$ とする。<br>(1) 角 $\theta$ の位置での小物体の速さ $v$ を求めよ（初めの速さは $0$ とみなす）。<br>(2) その位置で小物体が球面から受ける垂直抗力の大きさ $N$ を求めよ。<br>(3) 小物体が球面から離れる位置の $\cos\theta$ と、そのときの速さを求めよ。<br>(4) 離れる位置の、水平面からの高さを求めよ。",
  "a": r"(1) $v=\sqrt{2gR(1-\cos\theta)}$　(2) $N=mg(3\cos\theta-2)$　(3) $\cos\theta=\frac23$、$\sqrt{\frac{2gR}{3}}$　(4) $\frac23R$",
  "s": r"(1) 頂上からの下がった高さは $R(1-\cos\theta)$。$\frac12mv^2=mgR(1-\cos\theta)$。<br>(2) 中心方向の運動方程式：$m\frac{v^2}{R}=mg\cos\theta-N$。$N=mg\cos\theta-2mg(1-\cos\theta)=mg(3\cos\theta-2)$。<br>(3) 離れるのは $N=0$ のとき：$\cos\theta=\frac23$。$v^2=2gR\left(1-\frac23\right)=\frac{2gR}{3}$。<br>(4) $R\cos\theta=\frac23R$。<br><b>ポイント</b>：「面から離れる」条件は垂直抗力 $N=0$。$N$ を角度の関数として求め、$0$ になる角を探す。"},
 {"lv": "B", "tag": "傾いたカーブ",
  "q": r"半径 $50\,\mathrm{m}$ の水平なカーブで、路面がカーブの内側に向かって角 $\theta$（$\tan\theta=0.20$）だけ低くなるように傾けてある。<br>(1) 路面との摩擦力がはたらかなくても、自動車がこのカーブを等速円運動で曲がれる速さを求めよ。<br>(2) 路面が傾いていない（水平な）カーブで、同じ速さで曲がるのに必要な、タイヤと路面の静止摩擦係数の最小値を求めよ。<br>(3) 傾いたカーブを (1) の速さより速く走るとき、自動車がすべらないために摩擦力は路面に沿ってどちら向きに必要か。",
  "a": r"(1) $9.9\,\mathrm{m/s}$　(2) $0.20$　(3) 路面に沿ってカーブの内側（下向き）",
  "s": r"(1) 自動車にはたらく力は重力 $mg$ と垂直抗力 $N$。鉛直：$N\cos\theta=mg$、水平（中心向き）：$N\sin\theta=m\frac{v^2}{r}$。よって $v=\sqrt{gr\tan\theta}=\sqrt{9.8\times50\times0.20}=\sqrt{98}\fallingdotseq9.9\,\mathrm{m/s}$。<br>(2) 水平なカーブでは静止摩擦力 $f=m\frac{v^2}{r}\leqq\mu mg$ が必要。$\mu\geqq\frac{v^2}{gr}=\tan\theta=0.20$。<br>(3) 速いと必要な向心力が $N\sin\theta$ だけでは足りず、外側へすべり出そうとする。それを防ぐ摩擦力は路面に沿って内側（下向き）で、その水平成分が向心力を補う。<br><b>ポイント</b>：バンクのついたカーブでは、垂直抗力の水平成分が向心力になる。"},
 {"lv": "B", "tag": "加速する系での落下",
  "q": r"上向きに一定の加速度 $a=2.2\,\mathrm{m/s^2}$ で上昇しているエレベーターの中で、床から高さ $1.5\,\mathrm{m}$ の位置で、小球をエレベーターに対して静かに放した。<br>(1) エレベーター内の人から見た、小球の加速度の大きさと向きを求めよ。<br>(2) 小球が床に達するまでの時間を求めよ。<br>(3) 床に達する直前の、エレベーターに対する小球の速さを求めよ。<br>(4) 地上の人から見ると、放した瞬間の小球の速度は $0$ ではない。それでも (2) の答えが正しいことを、地上から見た運動で説明せよ。",
  "a": r"(1) 下向きに $12\,\mathrm{m/s^2}$　(2) $0.50\,\mathrm{s}$　(3) $6.0\,\mathrm{m/s}$　(4) 解説参照",
  "s": r"(1) エレベーター内では、重力 $mg$ に加えて下向きの慣性力 $ma$ がはたらくので、見かけの重力加速度は $g+a=9.8+2.2=12\,\mathrm{m/s^2}$（下向き）。<br>(2) $1.5=\frac12\times12\,t^2$ より $t=0.50\,\mathrm{s}$。<br>(3) $12\times0.50=6.0\,\mathrm{m/s}$。<br>(4) 放した瞬間のエレベーターの速度を $u$（上向き）とする。地上から見ると、小球は初速度 $u$、加速度 $-g$ で運動し、床は初速度 $u$、加速度 $+a$ で運動する。床から見た小球の相対変位は $(ut-\frac12gt^2)-(ut+\frac12at^2)=-\frac12(g+a)t^2$ で、$u$ によらない。これが $-1.5\,\mathrm{m}$ になる時刻は (2) と同じ。<br><b>ポイント</b>：慣性力を使う解き方と、地上から見て相対運動を考える解き方は同じ結果になる。"},
 {"lv": "C", "tag": "回転する円形の針金",
  "q": r"半径 $R$ のなめらかな円形の細い針金が、鉛直な直径を軸として一定の角速度 $\omega$ で回転している。針金には質量 $m$ の小さなビーズが通されていて、針金に沿ってなめらかに動ける。ビーズが針金に対して静止している位置を、円の中心 O から見て鉛直下向きとなす角 $\theta$（$0<\theta<90^\circ$）で表す。重力加速度の大きさを $g$ とする。<br>" + _fig_ring() +
       r"(1) 針金とともに回転する観測者から見て、ビーズにはたらく力をすべてあげよ。また、遠心力の大きさを $m,\ R,\ \omega,\ \theta$ で表せ。<br>(2) 針金に沿った方向の力のつりあいから、$\cos\theta$ を求めよ。また、$0<\theta<90^\circ$ の位置で静止できるための $\omega$ の条件を求めよ。<br>(3) ビーズが針金から受ける力の大きさを $m,\ R,\ \omega$ で表せ。<br>(4) $\omega^2=\frac{2g}{R}$ のとき、$\theta$ と、ビーズが針金から受ける力の大きさ（$mg$ の何倍か）を求めよ。",
  "a": r"(1) 重力、針金からの垂直抗力、遠心力 $mR\omega^2\sin\theta$　(2) $\cos\theta=\frac{g}{R\omega^2}$、$\omega>\sqrt{\frac gR}$　(3) $mR\omega^2$　(4) $\theta=60^\circ$、$2$ 倍",
  "s": r"(1) 重力 $mg$（鉛直下向き）、針金からの垂直抗力 $N$（針金はなめらかなので針金に垂直、ここでは中心 O の向きにとる）、遠心力（回転軸から遠ざかる水平の向き）。ビーズの回転半径は $R\sin\theta$ なので、遠心力の大きさは $mR\omega^2\sin\theta$。<br>(2) 針金に沿った方向（円の接線方向）：重力の成分 $mg\sin\theta$（最下点へ向かう向き）と、遠心力の成分 $mR\omega^2\sin\theta\cos\theta$（上へ向かう向き）がつりあう。$\sin\theta\neq0$ より $\cos\theta=\frac{g}{R\omega^2}$。$0<\theta<90^\circ$ となるには $0<\frac{g}{R\omega^2}<1$、すなわち $\omega>\sqrt{\frac gR}$。<br>(3) 半径方向（O 向き）：$N=mg\cos\theta+mR\omega^2\sin\theta\cdot\sin\theta$。$\cos\theta=\frac{g}{R\omega^2}$ を使うと $mg\cos\theta=mR\omega^2\cos^2\theta$ なので $N=mR\omega^2(\cos^2\theta+\sin^2\theta)=mR\omega^2$。<br>(4) $\cos\theta=\frac{g}{2g}=\frac12$ より $\theta=60^\circ$。$N=mR\cdot\frac{2g}{R}=2mg$。<br><b>ポイント</b>：回転系では遠心力を加えて「つりあい」で考える。なめらかな針金からの力は針金に垂直なので、針金に沿った方向の式には入らない。"},
 {"lv": "C", "tag": "円筒面と放物運動",
  "q": r"図のように、なめらかな水平面 AB が、点 B で半径 $r$ のなめらかな半円筒の内面（中心 O、最下点 B、最高点 C を含む鉛直面内）になめらかにつながっている。質量 $m$ の小球が水平面上を速さ $v_0$ で進み、B から円筒面に入った。重力加速度の大きさを $g$ とする。<br>" + _fig_halfpipe() +
       r"(1) 小球が円筒面から離れずに C に達するための $v_0$ の条件を求めよ。<br>(2) $v_0=\sqrt{6gr}$ のとき、C から飛び出した小球が水平面に落ちる点と B との距離を求めよ。<br>(3) $v_0=\sqrt{\frac72gr}$ のとき、小球は C に達する前に円筒面から離れる。離れる位置を、O から見て最下点 B の向きとなす角 $\theta$ で表し、離れるときの速さを求めよ。<br>(4) (3) の場合、面から離れた後の小球の最高点の、水平面からの高さを求めよ。",
  "a": r"(1) $v_0\geqq\sqrt{5gr}$　(2) $2\sqrt2\,r$　(3) $\theta=120^\circ$、$\sqrt{\frac{gr}{2}}$　(4) $\frac{27}{16}r$",
  "s": r"角 $\theta$ の位置で、高さは $r(1-\cos\theta)$、速さを $v$、垂直抗力を $N$ とすると<br>エネルギー：$v^2=v_0^2-2gr(1-\cos\theta)$、中心方向：$m\frac{v^2}{r}=N-mg\cos\theta$<br>より $N=\frac{mv_0^2}{r}-mg(2-3\cos\theta)$。<br>(1) C（$\theta=180^\circ$）で $N\geqq0$ となればよい。$v_0^2\geqq5gr$。<br>(2) C での速さは $v_C^2=6gr-4gr=2gr$。C から水平に飛び出し、高さ $2r$ を落ちる時間は $\sqrt{\frac{4r}{g}}$。C は B の真上なので、距離は $\sqrt{2gr}\times2\sqrt{\frac rg}=2\sqrt2\,r$。<br>(3) $N=mg\left(\frac72-2+3\cos\theta\right)=mg\left(\frac32+3\cos\theta\right)=0$ より $\cos\theta=-\frac12$、$\theta=120^\circ$。このとき $v^2=\frac72gr-2gr\times\frac32=\frac12gr$、$v=\sqrt{\frac{gr}{2}}$。<br>(4) 離れる点の高さは $r(1-\cos120^\circ)=\frac32r$。速度は円の接線方向で、水平と $60^\circ$ をなす斜め上向き。鉛直成分は $v\sin60^\circ$、その2乗は $\frac{gr}{2}\times\frac34=\frac38gr$。さらに上がる高さは $\frac{3gr/8}{2g}=\frac{3}{16}r$。最高点の高さは $\frac32r+\frac3{16}r=\frac{27}{16}r$。<br><b>ポイント</b>：面から離れた後は放物運動。離れる瞬間の速度の向き（接線方向）を、角 $\theta$ から正しく求める。"},
]}}


def verify():
    g = Rational(98, 10)
    PI = Rational(314, 100)
    # 5-1
    w = 2 * PI / 2
    _near(w, 3.1); _near(Rational(1, 2) * w, 1.6); _near(Rational(1, 2) * w ** 2, 4.9); _near(Rational(2, 10) * Rational(1, 2) * w ** 2, 0.99)
    # 5-2
    m, gg = symbols("m g", positive=True)
    T = solve(Eq(symbols("T") * cos(pi / 3), m * gg), symbols("T"))[0]
    _eq(T, 2 * m * gg)
    w2 = solve(Eq(T * sin(pi / 3), m * Rational(1, 2) * sin(pi / 3) * symbols("w2")), symbols("w2"))[0]
    _eq(w2, 4 * gg)
    wv = sqrt(w2.subs(gg, g)); _near(wv, 6.3); _near(2 * PI / wv, 1.0)
    # 5-3
    _near(50 * g, 4.9e2); _near(50 * (g + Rational(14, 10)), 5.6e2); _near(50 * (g - Rational(14, 10)), 4.2e2)
    # 5-4
    a = Rational(49, 10)
    assert a / g == Rational(1, 2); _near(Rational(1, 10) * sqrt(g ** 2 + a ** 2), 1.1)
    # 5-5
    l, v0, th = symbols("l v0 theta", positive=True)
    v2 = v0 ** 2 - 2 * gg * l * (1 - cos(th))
    Tt = m * v2 / l + m * gg * cos(th)
    _eq(Tt, m * v0 ** 2 / l - m * gg * (2 - 3 * cos(th)))
    _eq(solve(Tt.subs(th, pi), v0)[0], sqrt(5 * gg * l))
    _eq(Tt.subs(th, 0) - Tt.subs(th, pi), 6 * m * gg)
    # 5-6
    wmax = sqrt(Rational(4, 10) * g / Rational(2, 10)); _near(wmax, 4.4)
    r = symbols("r", positive=True)
    _eq(sqrt(Rational(4, 10) * gg / (2 * r)) / sqrt(Rational(4, 10) * gg / r), 1 / sqrt(2))
    # 5-7
    R = symbols("R", positive=True)
    v2 = 2 * gg * R * (1 - cos(th))
    N = m * gg * cos(th) - m * v2 / R
    _eq(N, m * gg * (3 * cos(th) - 2))
    c = solve(N.subs(cos(th), symbols("c")), symbols("c"))[0]
    assert c == Rational(2, 3)
    _eq((2 * gg * R * (1 - symbols("c"))).subs(symbols("c"), c), 2 * gg * R / 3)
    # 5-8
    v = sqrt(g * 50 * Rational(2, 10)); _eq(v, sqrt(98)); _near(v, 9.9)
    assert v ** 2 / (g * 50) == Rational(2, 10)
    # 5-9
    ge = g + Rational(22, 10)
    assert ge == 12 and sqrt(2 * Rational(15, 10) / ge) == Rational(1, 2) and ge * Rational(1, 2) == 6
    u, t = symbols("u t")
    _eq((u * t - gg * t ** 2 / 2) - (u * t + symbols("a") * t ** 2 / 2), -(gg + symbols("a")) * t ** 2 / 2)
    # 5-10 リング：回転系で接線方向・法線方向のつりあい
    w = symbols("omega", positive=True)
    # ビーズの位置 (R sin, -R cos)、接線（θ増加向き）(cos, sin)、O 向き (-sin, cos)
    F = Matrix([m * R * sin(th) * w ** 2, -m * gg])      # 遠心力＋重力
    tang = Matrix([cos(th), sin(th)]); inward = Matrix([-sin(th), cos(th)])
    ft = simplify(F.dot(tang))
    _eq(ft, sin(th) * m * (R * w ** 2 * cos(th) - gg))
    cth = gg / (R * w ** 2)
    Nn = simplify(-F.dot(inward))       # 垂直抗力（O 向き）＝ −(他の力の O 向き成分)
    _eq(Nn, m * gg * cos(th) + m * R * w ** 2 * sin(th) ** 2)
    _eq(Nn.subs(th, acos(cth)), m * R * w ** 2)
    assert simplify(cth.subs(w, sqrt(2 * gg / R))) == Rational(1, 2)
    _eq((m * R * w ** 2).subs(w, sqrt(2 * gg / R)), 2 * m * gg)
    # 5-11 円筒面
    N = m * v0 ** 2 / r - m * gg * (2 - 3 * cos(th))
    _eq(solve(N.subs(th, pi), v0)[0], sqrt(5 * gg * r))
    vC = sqrt(6 * gg * r - 4 * gg * r)
    _eq(vC * sqrt(4 * r / gg), 2 * sqrt(2) * r)
    N3 = N.subs(v0, sqrt(Rational(7, 2) * gg * r))
    cs = solve(N3.subs(cos(th), symbols("c")), symbols("c"))[0]
    assert cs == Rational(-1, 2)
    v2 = Rational(7, 2) * gg * r - 2 * gg * r * (1 - cs)
    _eq(v2, gg * r / 2)
    # 接線方向 (cosθ, sinθ) at θ=120°
    vy2 = v2 * sin(2 * pi / 3) ** 2
    hmax = r * (1 - cs) + vy2 / (2 * gg)
    _eq(hmax, Rational(27, 16) * r)
