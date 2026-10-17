"""問題集 第4章 運動量と力積。CH に問題、verify() で答えを sympy で検算する。"""
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


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _fig_curved():
    fy, cx, r, right = 112, 130, 76, 226
    # 曲面：中心 (cx, fy-r)、半径 r の円の 1/4（最下点 (cx,fy) から (cx+r, fy-r) まで）
    s = [_ln(10, fy, 262, fy, "#333", 1.2),
         f'<path d="M{cx},{fy} A{r},{r} 0 0 0 {cx + r},{fy - r} L{right},{fy - r} L{right},{fy} Z" fill="#f2f2f2" stroke="#333" stroke-width="1.2"/>',
         f'<rect x="52" y="{fy - 16}" width="16" height="16" fill="#e8eef8" stroke="#333" stroke-width="1.2"/>',
         _tx(60, fy - 20, "m", 11, True, anchor="middle"), _ar(72, fy - 8, 104, fy - 8, "#c0392b", 1.5),
         _tx(88, fy - 13, "v₀", 11, True, anchor="middle", c="#c0392b"), _tx(right - 14, fy - 10, "M", 12, True, anchor="middle")]
    return _svg(270, 122, s)


CH = {4: {
"goal": r"「運動量の変化＝力積」と、内力だけがはたらくときの運動量保存。衝突は「運動量保存＋反発係数の式」の2式を連立し、失われるエネルギーは運動エネルギーの差で求める。<br>（数値は有効数字2桁、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$ とする。）",
"items": [
 {"lv": "A", "tag": "力積と運動量",
  "q": r"質量 $0.14\,\mathrm{kg}$ のボールが水平に速さ $30\,\mathrm{m/s}$ で飛んできて、バットで逆向きに速さ $40\,\mathrm{m/s}$ で打ち返された。<br>(1) ボールが受けた力積の大きさと向きを求めよ。<br>(2) バットとボールの接触時間が $1.0\times10^{-2}\,\mathrm{s}$ のとき、ボールが受けた平均の力の大きさを求めよ。",
  "a": r"(1) $9.8\,\mathrm{N\cdot s}$、打ち返された向き　(2) $9.8\times10^2\,\mathrm{N}$",
  "s": r"(1) 打ち返された向きを正とする。力積＝運動量の変化 $=0.14\times40-0.14\times(-30)=9.8\,\mathrm{N\cdot s}$。正なので打ち返された向き。<br>(2) $\bar F\Delta t=9.8$ より $\bar F=\frac{9.8}{1.0\times10^{-2}}=9.8\times10^2\,\mathrm{N}$。<br><b>ポイント</b>：速度の向きが逆になるときは、符号をつけて差をとる（$40-30$ ではなく $40-(-30)$）。"},
 {"lv": "A", "tag": "完全非弾性衝突",
  "q": r"なめらかな水平面上を速さ $3.0\,\mathrm{m/s}$ で進む質量 $2.0\,\mathrm{kg}$ の物体 A が、静止している質量 $1.0\,\mathrm{kg}$ の物体 B に衝突し、一体となって進んだ。<br>(1) 衝突後の速さを求めよ。<br>(2) 衝突によって失われた運動エネルギーを求めよ。<br>(3) この衝突の反発係数を答えよ。",
  "a": r"(1) $2.0\,\mathrm{m/s}$　(2) $3.0\,\mathrm{J}$　(3) $0$",
  "s": r"(1) 運動量保存：$2.0\times3.0=(2.0+1.0)V$ より $V=2.0\,\mathrm{m/s}$。<br>(2) 衝突前 $\frac12\times2.0\times3.0^2=9.0\,\mathrm{J}$、衝突後 $\frac12\times3.0\times2.0^2=6.0\,\mathrm{J}$。失われたのは $3.0\,\mathrm{J}$。<br>(3) 衝突後の相対速度が $0$ なので $e=0$（完全非弾性衝突）。<br><b>ポイント</b>：衝突では運動量は保存されるが、運動エネルギーは一般に保存されない（$e=1$ のときだけ保存）。"},
 {"lv": "A", "tag": "床との衝突",
  "q": r"高さ $2.5\,\mathrm{m}$ の位置から小球を静かに落としたところ、水平な床ではね返って、高さ $1.6\,\mathrm{m}$ まで上がった。<br>(1) 1回目の衝突の直前と直後の小球の速さを求めよ。<br>(2) 床と小球の間の反発係数を求めよ。<br>(3) 2回目にはね返った後に上がる高さを求めよ。",
  "a": r"(1) 直前 $7.0\,\mathrm{m/s}$、直後 $5.6\,\mathrm{m/s}$　(2) $0.80$　(3) $1.0\,\mathrm{m}$",
  "s": r"(1) 直前 $\sqrt{2\times9.8\times2.5}=7.0\,\mathrm{m/s}$、直後 $\sqrt{2\times9.8\times1.6}=5.6\,\mathrm{m/s}$。<br>(2) $e=\frac{5.6}{7.0}=0.80$（$e=\sqrt{\frac{1.6}{2.5}}$ としても同じ）。<br>(3) はね返る高さは速さの2乗に比例するので、1回ごとに $e^2=0.64$ 倍。$1.6\times0.64=1.024\fallingdotseq1.0\,\mathrm{m}$。<br><b>ポイント</b>：床（静止した面）との衝突では $e=\frac{\text{はね返る速さ}}{\text{当たる速さ}}$、高さの比は $e^2$。"},
 {"lv": "A", "tag": "分裂と重心",
  "q": r"なめらかな水平面上に静止していた質量 $3.0\,\mathrm{kg}$ の物体が、内部の爆発によって質量 $2.0\,\mathrm{kg}$ の A と質量 $1.0\,\mathrm{kg}$ の B に分裂し、A は右向きに速さ $4.0\,\mathrm{m/s}$ で動き出した。<br>(1) B の速度を求めよ。<br>(2) 分裂によって生じた運動エネルギーの和を求めよ。<br>(3) 分裂した位置を原点、右向きを正として、分裂の $2.0\,\mathrm{s}$ 後の A と B の重心の位置を求めよ。",
  "a": r"(1) 左向きに $8.0\,\mathrm{m/s}$　(2) $48\,\mathrm{J}$　(3) 原点（$x=0$）",
  "s": r"(1) 運動量保存：$0=2.0\times4.0+1.0\times v_B$ より $v_B=-8.0\,\mathrm{m/s}$。<br>(2) $\frac12\times2.0\times4.0^2+\frac12\times1.0\times8.0^2=16+32=48\,\mathrm{J}$。<br>(3) A は $x_A=8.0\,\mathrm{m}$、B は $x_B=-16\,\mathrm{m}$。重心 $x_G=\frac{2.0\times8.0+1.0\times(-16)}{3.0}=0$。<br><b>ポイント</b>：外力がなければ全運動量は一定で、重心の速度も一定。初め静止していたなら重心は動かない。"},
 {"lv": "B", "tag": "一直線上の衝突",
  "q": r"なめらかな水平面上で、速さ $v_0$ で進む質量 $m$ の小球 A が、静止している質量 $M$ の小球 B に正面衝突した。反発係数を $e$ とし、A の初めの進む向きを正とする。<br>(1) 衝突後の A, B の速度 $v_A,\ v_B$ を求めよ。<br>(2) $e=1$、$M=m$ のとき、衝突後の運動はどうなるか。<br>(3) $M=2m$、$e=\frac12$ のとき、$v_A,\ v_B$ を求めよ。また、衝突で失われる運動エネルギーは、初めの運動エネルギーの何倍か。",
  "a": r"(1) $v_A=\frac{m-eM}{m+M}v_0$、$v_B=\frac{(1+e)m}{m+M}v_0$　(2) A は静止し、B が速さ $v_0$ で進む（速度の交換）　(3) $v_A=0$、$v_B=\frac{v_0}{2}$、$\frac12$ 倍",
  "s": r"(1) 運動量保存：$mv_0=mv_A+Mv_B$。反発係数の式：$v_B-v_A=ev_0$。<br>第2式より $v_B=v_A+ev_0$ を第1式に代入して $(m+M)v_A=(m-eM)v_0$。よって $v_A=\frac{m-eM}{m+M}v_0$、$v_B=\frac{(1+e)m}{m+M}v_0$。<br>(2) $v_A=0$、$v_B=v_0$。同じ質量の弾性衝突では速度が入れかわる。<br>(3) $v_A=\frac{m-m}{3m}v_0=0$、$v_B=\frac{\frac32m}{3m}v_0=\frac{v_0}{2}$。衝突後の運動エネルギーは $\frac12(2m)\left(\frac{v_0}{2}\right)^2=\frac14mv_0^2$ で、初めの $\frac12mv_0^2$ の半分。失われたのも $\frac12$ 倍。<br><b>ポイント</b>：反発係数の式は「（遠ざかる速さ）$=e\times$（近づく速さ）」。符号は向きを正にそろえて $v_B-v_A=-e(0-v_0)$ と書くと間違えない。"},
 {"lv": "B", "tag": "平面内の衝突",
  "q": r"なめらかな水平面上で、速さ $v_0$ で進む小球 A が、静止している同じ質量の小球 B に衝突した。衝突後、A は初めの進行方向から $30^\circ$ の向きに、B は反対側に $60^\circ$ の向きに進んだ。<br>(1) 衝突後の A, B の速さを $v_0$ で表せ。<br>(2) この衝突で運動エネルギーは保存されているか。<br>(3) 一般に、静止している同じ質量の小球に弾性衝突（運動エネルギーが保存される衝突）して2球が別々の向きに進むとき、衝突後の2球の進む向きのなす角は $90^\circ$ であることを示せ。",
  "a": r"(1) A：$\frac{\sqrt3}{2}v_0$、B：$\frac12v_0$　(2) 保存されている　(3) 解説参照",
  "s": r"(1) 初めの進行方向を $x$ 軸、それに垂直に $y$ 軸をとる。質量を $m$ とする。<br>$x$ 成分：$mv_0=mv_A\cos30^\circ+mv_B\cos60^\circ$、$y$ 成分：$0=mv_A\sin30^\circ-mv_B\sin60^\circ$。<br>第2式より $v_A=\sqrt3\,v_B$。第1式に代入すると $v_0=\frac32v_B+\frac12v_B=2v_B$。よって $v_B=\frac12v_0$、$v_A=\frac{\sqrt3}{2}v_0$。<br>(2) $\frac12m\left(\frac34v_0^2+\frac14v_0^2\right)=\frac12mv_0^2$ で、保存されている。<br>(3) 運動量保存 $\vec v_0=\vec v_A+\vec v_B$ の両辺を2乗すると $v_0^2=v_A^2+v_B^2+2\vec v_A\cdot\vec v_B$。エネルギー保存 $v_0^2=v_A^2+v_B^2$ と比べて $\vec v_A\cdot\vec v_B=0$。よって2つの速度は直交する。<br><b>ポイント</b>：平面内の衝突は、運動量保存を2つの成分に分けて書く。運動量はベクトルとして保存される。"},
 {"lv": "B", "tag": "斜め衝突",
  "q": r"なめらかで固定された平らな壁に、質量 $m$ の小球が速さ $v$ で、壁の法線（壁に垂直な直線）と $30^\circ$ をなす向きから衝突した。壁と小球の間の反発係数を $\frac13$ とする。重力の影響は考えない。<br>(1) はね返った直後の小球の速さを求めよ。<br>(2) はね返った向きと壁の法線のなす角を求めよ。<br>(3) 小球が壁から受けた力積の大きさと向きを求めよ。",
  "a": r"(1) $\frac{v}{\sqrt3}$　(2) $60^\circ$　(3) $\frac{2\sqrt3}{3}mv$、壁に垂直で壁から離れる向き",
  "s": r"壁がなめらかなので、壁に平行な方向には力を受けず、平行な速度成分は変わらない。壁に垂直な成分だけが $e$ 倍になって向きが逆になる。<br>(1) 平行成分 $v\sin30^\circ=\frac v2$、垂直成分 $\frac13\times v\cos30^\circ=\frac{\sqrt3}{6}v$。速さ $\sqrt{\frac{v^2}{4}+\frac{v^2}{12}}=\frac{v}{\sqrt3}$。<br>(2) 法線となす角 $\phi$ は $\tan\phi=\frac{v/2}{\sqrt3v/6}=\sqrt3$ より $\phi=60^\circ$。<br>(3) 力積は壁に垂直な成分だけ：$m\cdot\frac{\sqrt3}{6}v-\left(-m\cdot\frac{\sqrt3}{2}v\right)=\frac{2\sqrt3}{3}mv$。<br><b>ポイント</b>：なめらかな面との衝突は「平行成分はそのまま、垂直成分は $e$ 倍で逆向き」。$e<1$ なら面に近い向きにはね返る。"},
 {"lv": "B", "tag": "ばねを介した衝突",
  "q": r"なめらかな水平面上に、ばね定数 $k$ の軽いばねを左端につけた質量 $2m$ の物体 B が静止している。左から質量 $m$ の物体 A が速さ $v_0$ で近づき、ばねを押し縮めた。右向きを正とする。<br>(1) ばねが最も縮んだときの A, B の速度を求めよ。<br>(2) ばねの縮みの最大値を求めよ。<br>(3) A がばねから離れた後の A, B の速度を求めよ。",
  "a": r"(1) どちらも $\frac{v_0}{3}$　(2) $v_0\sqrt{\frac{2m}{3k}}$　(3) A：$-\frac{v_0}{3}$（左向き）、B：$\frac{2v_0}{3}$",
  "s": r"(1) ばねが最も縮むのは、A と B の速度が等しくなった瞬間（それまでは A が速く、近づき続ける）。運動量保存 $mv_0=3mV$ より $V=\frac{v_0}{3}$。<br>(2) 力学的エネルギー保存：$\frac12mv_0^2=\frac12(3m)V^2+\frac12kx^2$ より $\frac12kx^2=\frac12mv_0^2-\frac16mv_0^2=\frac13mv_0^2$、$x=v_0\sqrt{\frac{2m}{3k}}$。<br>(3) ばねが自然長にもどると弾性エネルギーは $0$ なので、運動エネルギーの和が保存される（$e=1$ の衝突と同じ）。$mv_0=mv_A+2mv_B$、$v_B-v_A=v_0$ より $v_A=-\frac{v_0}{3}$、$v_B=\frac{2v_0}{3}$。<br><b>ポイント</b>：「最も縮む」「最も高く上がる」は相対速度 $0$（速度が等しい）の瞬間。運動量保存で共通の速度を出し、エネルギーの式につなぐ。"},
 {"lv": "B", "tag": "台の上をすべる物体",
  "q": r"なめらかな水平面上に、質量 $M=3.0\,\mathrm{kg}$ の長い台が静止している。台の上面はあらく、その左端に質量 $m=1.0\,\mathrm{kg}$ の小物体を置いて、右向きに初速 $4.0\,\mathrm{m/s}$ を与えた。小物体と台の間の動摩擦係数は $0.20$ である。小物体はやがて台に対して静止した。<br>(1) そのときの台の速さを求めよ。<br>(2) 小物体が台の上をすべっていた時間を求めよ。<br>(3) 小物体が台の上をすべった距離（台に対する距離）を求めよ。<br>(4) 摩擦によって失われた力学的エネルギーを求めよ。",
  "a": r"(1) $1.0\,\mathrm{m/s}$　(2) $1.5\,\mathrm{s}$　(3) $3.1\,\mathrm{m}$　(4) $6.0\,\mathrm{J}$",
  "s": r"(1) 水平方向の外力はないので、小物体と台の運動量の和は保存される。$1.0\times4.0=(1.0+3.0)V$ より $V=1.0\,\mathrm{m/s}$。<br>(2) 小物体は動摩擦力 $0.20\times1.0\times9.8=1.96\,\mathrm{N}$ を後ろ向きに受け、加速度の大きさは $1.96\,\mathrm{m/s^2}$。$4.0$ から $1.0\,\mathrm{m/s}$ まで減速するのに $t=\frac{3.0}{1.96}\fallingdotseq1.5\,\mathrm{s}$。<br>(3) 失われたエネルギー（(4)）は「動摩擦力×台に対してすべった距離」に等しい。$1.96\,d=6.0$ より $d\fallingdotseq3.1\,\mathrm{m}$。<br>（別解：台に対する小物体の相対加速度は $-1.96-\frac{1.96}{3.0}$、相対初速 $4.0$ から $d=\frac{4.0^2}{2\times2.613}\fallingdotseq3.1\,\mathrm{m}$。）<br>(4) $\frac12\times1.0\times4.0^2-\frac12\times4.0\times1.0^2=8.0-2.0=6.0\,\mathrm{J}$。<br><b>ポイント</b>：摩擦で失われる力学的エネルギーは「動摩擦力×相対的にすべった距離」。床に対する距離ではない。"},
 {"lv": "C", "tag": "曲面をもつ台",
  "q": r"なめらかな水平面上に、なめらかな曲面をもつ質量 $M$ の台が静止している。曲面の下端は水平面になめらかにつながっている。質量 $m$ の小物体が水平面上を速さ $v_0$ で進んで、曲面を上り始めた。小物体は台の上端をこえないものとし、重力加速度の大きさを $g$ とする。右向きを正とする。<br>" + _fig_curved() +
       r"(1) 小物体が曲面上で最も高い点に達したとき、小物体と台の速度にはどのような関係があるか。そのときの台の速さを求めよ。<br>(2) 小物体が達する最高点の高さ $h$ を求めよ。<br>(3) 小物体が曲面をすべり下りて台から離れた後の、小物体と台の速度 $v,\ V$ を求めよ。<br>(4) $m=1.0\,\mathrm{kg}$、$M=3.0\,\mathrm{kg}$、$v_0=4.0\,\mathrm{m/s}$ のとき、$h,\ v,\ V$ の値を求めよ（$g=9.8\,\mathrm{m/s^2}$）。",
  "a": r"(1) 小物体の速度は水平で台の速度と等しい、$\frac{m}{M+m}v_0$　(2) $h=\frac{Mv_0^2}{2g(M+m)}$　(3) $v=\frac{m-M}{m+M}v_0$、$V=\frac{2m}{m+M}v_0$　(4) $h\fallingdotseq0.61\,\mathrm{m}$、$v=-2.0\,\mathrm{m/s}$（左向き $2.0\,\mathrm{m/s}$）、$V=2.0\,\mathrm{m/s}$",
  "s": r"小物体と台の間の垂直抗力は内力。床からの垂直抗力と重力は鉛直方向なので、<b>水平方向の運動量だけ</b>が保存される。また、なめらかなので力学的エネルギーも保存される。<br>(1) 最高点では、小物体の台に対する速度が $0$（それより上にも下にも動いていない）。よって小物体と台は同じ水平速度 $V_1$ をもつ。$mv_0=(m+M)V_1$ より $V_1=\frac{m}{M+m}v_0$。<br>(2) $\frac12mv_0^2=\frac12(m+M)V_1^2+mgh$ より $mgh=\frac12mv_0^2\cdot\frac{M}{M+m}$、$h=\frac{Mv_0^2}{2g(M+m)}$。<br>(3) 離れた後は高さが元にもどるので、運動エネルギーの和が保存される。$mv_0=mv+MV$、$\frac12mv_0^2=\frac12mv^2+\frac12MV^2$。これは $e=1$ の衝突と同じ式で、$v\neq v_0$ の解は $v=\frac{m-M}{m+M}v_0$、$V=\frac{2m}{m+M}v_0$。<br>(4) $h=\frac{3.0\times16}{2\times9.8\times4.0}\fallingdotseq0.61\,\mathrm{m}$、$v=\frac{-2.0}{4.0}\times4.0=-2.0\,\mathrm{m/s}$、$V=\frac{2.0}{4.0}\times4.0=2.0\,\mathrm{m/s}$。<br><b>ポイント</b>：台が動く問題では、台を固定したときの $h=\frac{v_0^2}{2g}$ より低くなる（運動エネルギーの一部が全体の運動に残るため）。保存されるのは水平方向の運動量だけ。"},
 {"lv": "C", "tag": "台車からの飛び降り",
  "q": r"なめらかな水平面上に、質量 $M$ の台車が静止しており、その上に質量 $m$ の人が2人乗っている。人は、台車に対する相対速度が後ろ向きに大きさ $u$ となるように、水平に台車から飛び降りる（相対速度は飛び降りた直後の台車に対するものとする）。台車の進む向き（前向き）を正とする。<br>(1) 2人が同時に飛び降りるとき、台車の速さ $V_1$ を求めよ。<br>(2) 1人ずつ順に飛び降りるとき、1人目が飛び降りた直後の台車の速さ $V'$ と、2人目が飛び降りた直後の台車の速さ $V_2$ を求めよ。<br>(3) $M=80\,\mathrm{kg}$、$m=60\,\mathrm{kg}$、$u=4.0\,\mathrm{m/s}$ として、$V_1$ と $V_2$ の値を求めて比べよ。<br>(4) 一般に $V_1$ と $V_2$ ではどちらが大きいか。理由を簡潔に述べよ。",
  "a": r"(1) $\frac{2mu}{M+2m}$　(2) $V'=\frac{mu}{M+2m}$、$V_2=\frac{mu}{M+2m}+\frac{mu}{M+m}$　(3) $V_1=2.4\,\mathrm{m/s}$、$V_2\fallingdotseq2.9\,\mathrm{m/s}$　(4) $V_2$ の方が大きい（解説参照）",
  "s": r"飛び降りた人の地面に対する速度は（台車の速度）$-u$。水平方向の外力はないので運動量の和は保存される。<br>(1) $0=MV_1+2m(V_1-u)$ より $V_1=\frac{2mu}{M+2m}$。<br>(2) 1人目：$0=(M+m)V'+m(V'-u)$ より $V'=\frac{mu}{M+2m}$。<br>2人目：飛び降りる前の運動量 $(M+m)V'$ が保存されて、$(M+m)V'=MV_2+m(V_2-u)$ より $V_2=V'+\frac{mu}{M+m}=\frac{mu}{M+2m}+\frac{mu}{M+m}$。<br>(3) $V_1=\frac{2\times60\times4.0}{200}=2.4\,\mathrm{m/s}$、$V_2=\frac{240}{200}+\frac{240}{140}=1.2+1.71\fallingdotseq2.9\,\mathrm{m/s}$。<br>(4) $V_1=\frac{mu}{M+2m}+\frac{mu}{M+2m}$ と書けるので、$V_2-V_1=\frac{mu}{M+m}-\frac{mu}{M+2m}>0$。2人目がけり出すとき、相手（台車）はすでに1人分軽くなっているので、同じ相対速度 $u$ で飛び出したときに台車が得る速度の増加が大きくなる。<br><b>ポイント</b>：相対速度で与えられたときは「どの時点の何に対する速度か」を確かめて、地面に対する速度に直してから運動量保存を書く。多段ロケットが有利な理由も同じ考え方で説明できる。"},
]}}


def verify():
    g = Rational(98, 10)
    # 4-1
    I = Rational(14, 100) * 40 - Rational(14, 100) * (-30)
    assert I == Rational(98, 10); assert I / Rational(1, 100) == 980
    # 4-2
    V = Rational(6, 3)
    assert V == 2 and Rational(1, 2) * 2 * 9 - Rational(1, 2) * 3 * 4 == 3
    # 4-3
    v1, v2 = sqrt(2 * g * Rational(5, 2)), sqrt(2 * g * Rational(16, 10))
    assert v1 == 7 and v2 == Rational(56, 10) and v2 / v1 == Rational(8, 10)
    _near(Rational(16, 10) * Rational(64, 100), 1.0)
    # 4-4
    vB = -2 * 4 / Rational(1)
    assert vB == -8 and Rational(1, 2) * 2 * 16 + Rational(1, 2) * 1 * 64 == 48
    assert 2 * 8 + 1 * (-16) == 0
    # 4-5
    m, M, e, v0, vA, vB = symbols("m M e v0 vA vB", positive=True)
    vA, vB = symbols("vA vB")
    s = solve([m * v0 - m * vA - M * vB, vB - vA - e * v0], [vA, vB])
    _eq(s[vA], (m - e * M) * v0 / (m + M)); _eq(s[vB], (1 + e) * m * v0 / (m + M))
    assert simplify(s[vA].subs({e: 1, M: m})) == 0 and simplify(s[vB].subs({e: 1, M: m}) - v0) == 0
    a3, b3 = s[vA].subs({M: 2 * m, e: Rational(1, 2)}), s[vB].subs({M: 2 * m, e: Rational(1, 2)})
    _eq(a3, 0); _eq(b3, v0 / 2)
    KE0 = m * v0 ** 2 / 2
    _eq((KE0 - (m * a3 ** 2 / 2 + 2 * m * b3 ** 2 / 2)) / KE0, Rational(1, 2))
    # 4-6
    s = solve([v0 - vA * cos(pi / 6) - vB * cos(pi / 3), vA * sin(pi / 6) - vB * sin(pi / 3)], [vA, vB])
    _eq(s[vA], sqrt(3) * v0 / 2); _eq(s[vB], v0 / 2)
    _eq(s[vA] ** 2 + s[vB] ** 2, v0 ** 2)
    # 4-7
    v = symbols("v", positive=True)
    par, perp = v * sin(pi / 6), Rational(1, 3) * v * cos(pi / 6)
    _eq(sqrt(par ** 2 + perp ** 2), v / sqrt(3)); _eq(par / perp, sqrt(3))
    _eq(m * perp + m * v * cos(pi / 6), 2 * sqrt(3) * m * v / 3)
    # 4-8
    k = symbols("k", positive=True)
    Vc = m * v0 / (3 * m)
    x = sqrt((m * v0 ** 2 / 2 - 3 * m * Vc ** 2 / 2) * 2 / k)
    _eq(x, v0 * sqrt(2 * m / (3 * k)))
    s = solve([m * v0 - m * vA - 2 * m * vB, m * v0 ** 2 - m * vA ** 2 - 2 * m * vB ** 2], [vA, vB], dict=True)
    s = [d for d in s if simplify(d[vB]) != 0]
    _eq(s[0][vA], -v0 / 3); _eq(s[0][vB], 2 * v0 / 3)
    # 4-9
    V = Rational(4, 4)
    assert V == 1
    a = Rational(2, 10) * g
    _near(3 / a, 1.5)
    loss = Rational(1, 2) * 16 - Rational(1, 2) * 4 * 1
    assert loss == 6
    d = loss / (Rational(2, 10) * 1 * g); _near(d, 3.1)
    arel = a + Rational(2, 10) * g / 3
    _eq(16 / (2 * arel), d)
    # 4-10
    gg = symbols("g", positive=True)
    V1 = m * v0 / (M + m)
    h = (m * v0 ** 2 / 2 - (m + M) * V1 ** 2 / 2) / (m * gg)
    _eq(h, M * v0 ** 2 / (2 * gg * (M + m)))
    s = solve([m * v0 - m * vA - M * vB, m * v0 ** 2 - m * vA ** 2 - M * vB ** 2], [vA, vB], dict=True)
    s = [d for d in s if simplify(d[vB]) != 0][0]
    _eq(s[vA], (m - M) * v0 / (m + M)); _eq(s[vB], 2 * m * v0 / (m + M))
    num = {m: 1, M: 3, v0: 4}
    _near(h.subs(num).subs(gg, g), 0.61); assert s[vA].subs(num) == -2 and s[vB].subs(num) == 2
    # 4-11
    u, V_ = symbols("u V")
    V1 = solve(M * V_ + 2 * m * (V_ - u), V_)[0]
    _eq(V1, 2 * m * u / (M + 2 * m))
    Vp = solve((M + m) * V_ + m * (V_ - u), V_)[0]
    _eq(Vp, m * u / (M + 2 * m))
    V2 = solve((M + m) * Vp - M * V_ - m * (V_ - u), V_)[0]
    _eq(V2, m * u / (M + 2 * m) + m * u / (M + m))
    num = {M: 80, m: 60, u: 4}
    assert V1.subs(num) == Rational(12, 5); _near(V2.subs(num), 2.9)
    assert simplify(V2 - V1 - (m * u / (M + m) - m * u / (M + 2 * m))) == 0
