"""問題集 第3章 仕事と力学的エネルギー。CH に問題、verify() で答えを sympy で検算する。"""
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


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _spring(x1, x2, y, n=8, amp=5):
    pts = [(x1, y), (x1 + 4, y)]
    w = (x2 - x1 - 8) / n
    for i in range(n):
        pts.append((x1 + 4 + w * (i + 0.5), y + (amp if i % 2 == 0 else -amp)))
    pts += [(x2 - 4, y), (x2, y)]
    return f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="#333" stroke-width="1.1"/>'


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


def _fig_track():
    fy, sx, sy, bx, cx, wx = 120, 24, 40, 96, 186, 266   # 斜面の上端 (sx,sy)、下端 B=(bx,fy)
    ux, uy = (bx - sx), (fy - sy)
    ul = math.hypot(ux, uy)
    ux, uy = ux / ul, uy / ul
    nx, ny = uy, -ux                       # 斜面の外向き法線（右上向き）
    t = 8                                   # 点 A は上端から斜面に沿って 8px
    ax, ay = sx + ux * t, sy + uy * t
    s = [f'<polygon points="{sx},{sy} {sx},{fy} {bx},{fy}" fill="#f2f2f2" stroke="none"/>',
         _ln(sx, sy, bx, fy, "#333", 1.4), _ln(bx, fy, wx, fy, "#333", 1.4),
         f'<rect x="{bx}" y="{fy}" width="{cx - bx}" height="5" fill="#b9b9b9"/>',
         _ln(wx, fy - 30, wx, fy, "#333", 1.6)]
    for yy in range(fy - 28, fy + 1, 7):
        s.append(_ln(wx, yy, wx + 6, yy - 6, "#777", 0.8))
    s += [_spring(218, wx, fy - 8), f'<circle cx="{ax + nx * 6:.1f}" cy="{ay + ny * 6:.1f}" r="6" fill="#1d4e89"/>',
          _ln(8, ay, ax, ay, "#999", 1, "2,2"), _ln(10, ay, 10, fy, "#555", 1),
          _ln(6, ay, 14, ay, "#555", 1), _ln(6, fy, 14, fy, "#555", 1),
          _tx(14, 96, "0.80 m", 10), _tx(ax + nx * 6 + 10, ay + ny * 6 - 4, "A", 11),
          _tx(bx, fy + 17, "B", 11, anchor="middle"), _tx(cx, fy + 17, "C", 11, anchor="middle"),
          _tx((bx + cx) / 2, fy - 6, "あらい 0.60 m", 10, anchor="middle")]
    return _svg(280, 142, s)


CH = {3: {
"goal": r"仕事 $W=Fx\cos\theta$ と「運動エネルギーの変化＝された仕事」を軸に、力学的エネルギー保存と、摩擦などの非保存力がする仕事を使い分ける。<br>（数値は有効数字2桁、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$ とする。）",
"items": [
 {"lv": "A", "tag": "仕事と仕事率",
  "q": r"(1) 質量 $5.0\,\mathrm{kg}$ の荷物を、一定の速さでゆっくり $4.0\,\mathrm{m}$ 持ち上げた。人が荷物にした仕事を求めよ。<br>(2) (1) の仕事を $10\,\mathrm{s}$ で行ったときの、平均の仕事率を求めよ。<br>(3) 水平な床の上の物体を、水平から $60^\circ$ 上向きの大きさ $10\,\mathrm{N}$ の力で引き、床に沿って $3.0\,\mathrm{m}$ 動かした。この力がした仕事を求めよ。<br>(4) (3) の間に、物体にはたらく重力と垂直抗力がした仕事をそれぞれ求めよ。",
  "a": r"(1) $2.0\times10^2\,\mathrm{J}$　(2) $20\,\mathrm{W}$　(3) $15\,\mathrm{J}$　(4) どちらも $0$",
  "s": r"(1) 一定の速さなので、人が加える力は重力とつりあい $5.0\times9.8=49\,\mathrm{N}$。$W=49\times4.0=196\fallingdotseq2.0\times10^2\,\mathrm{J}$。<br>(2) $P=\frac{W}{t}=\frac{196}{10}\fallingdotseq20\,\mathrm{W}$。<br>(3) $W=Fx\cos60^\circ=10\times3.0\times\frac12=15\,\mathrm{J}$。<br>(4) 重力も垂直抗力も移動の向きに垂直なので、仕事は $0$。<br><b>ポイント</b>：仕事は「力の移動方向の成分×移動距離」。力が移動方向に垂直なら仕事は $0$。"},
 {"lv": "A", "tag": "運動エネルギーと仕事",
  "q": r"なめらかな水平面上を速さ $3.0\,\mathrm{m/s}$ で進む質量 $2.0\,\mathrm{kg}$ の物体に、進行方向に大きさ $8.0\,\mathrm{N}$ の一定の力を加え続けて $4.0\,\mathrm{m}$ 進ませた。<br>(1) この力がした仕事を求めよ。<br>(2) 力を加え終えたときの物体の速さを求めよ。<br>(3) 続いて、進行方向と逆向きに一定の力を加えて、さらに $6.0\,\mathrm{m}$ 進んだところで物体を止めたい。必要な力の大きさを求めよ。",
  "a": r"(1) $32\,\mathrm{J}$　(2) $6.4\,\mathrm{m/s}$　(3) $6.8\,\mathrm{N}$",
  "s": r"(1) $W=8.0\times4.0=32\,\mathrm{J}$。<br>(2) 初めの運動エネルギーは $\frac12\times2.0\times3.0^2=9.0\,\mathrm{J}$。運動エネルギーの変化＝された仕事より $\frac12\times2.0\,v^2=9.0+32=41$、$v=\sqrt{41}\fallingdotseq6.4\,\mathrm{m/s}$。<br>(3) 運動エネルギー $41\,\mathrm{J}$ を $0$ にするので、力 $F$ がする仕事は $-F\times6.0=-41$。$F=\frac{41}{6.0}\fallingdotseq6.8\,\mathrm{N}$。<br><b>ポイント</b>：力が一定でなくても使える関係「$\frac12mv^2-\frac12mv_0^2=W$」。時間を聞かれていなければ、運動方程式よりも速い。"},
 {"lv": "A", "tag": "弾性力による位置エネルギー",
  "q": r"なめらかな水平面上で、ばね定数 $50\,\mathrm{N/m}$ の軽いばねの一端を壁に固定し、他端に質量 $0.50\,\mathrm{kg}$ の物体をつける。ばねを自然長から $0.20\,\mathrm{m}$ 縮めて静かに放した。<br>(1) 放す前の、弾性力による位置エネルギーを求めよ。<br>(2) ばねが自然長にもどったときの物体の速さを求めよ。<br>(3) ばねの縮みが $0.10\,\mathrm{m}$ のときの物体の速さを求めよ。",
  "a": r"(1) $1.0\,\mathrm{J}$　(2) $2.0\,\mathrm{m/s}$　(3) $1.7\,\mathrm{m/s}$",
  "s": r"(1) $U=\frac12kx^2=\frac12\times50\times0.20^2=1.0\,\mathrm{J}$。<br>(2) 力学的エネルギー保存：$1.0=\frac12\times0.50\,v^2$ より $v=2.0\,\mathrm{m/s}$。<br>(3) $\frac12\times50\times0.20^2=\frac12\times0.50\,v^2+\frac12\times50\times0.10^2$ より $0.25v^2=0.75$、$v=\sqrt3\fallingdotseq1.7\,\mathrm{m/s}$。<br><b>ポイント</b>：弾性エネルギーは $x^2$ に比例するので、縮みが半分になると $\frac14$ になる（残り $\frac34$ が運動エネルギー）。"},
 {"lv": "A", "tag": "力学的エネルギー保存",
  "q": r"なめらかな曲面上の、最下点からの高さ $2.5\,\mathrm{m}$ の点 A から小球を静かに放した。<br>(1) 最下点 B を通過するときの速さを求めよ。<br>(2) 曲面を上って、最下点からの高さ $1.6\,\mathrm{m}$ の点 C を通過するときの速さを求めよ。<br>(3) 曲面が十分高くまで続いているとき、小球が達する最高点の、最下点からの高さを求めよ。",
  "a": r"(1) $7.0\,\mathrm{m/s}$　(2) $4.2\,\mathrm{m/s}$　(3) $2.5\,\mathrm{m}$",
  "s": r"垂直抗力は運動の向きに垂直なので仕事をしない。重力だけが仕事をするので、力学的エネルギーが保存される。<br>(1) $mg\times2.5=\frac12mv_B^2$ より $v_B=\sqrt{2\times9.8\times2.5}=7.0\,\mathrm{m/s}$。<br>(2) $mg\times2.5=\frac12mv_C^2+mg\times1.6$ より $v_C=\sqrt{2\times9.8\times0.90}=4.2\,\mathrm{m/s}$。<br>(3) 最高点で速さ $0$ なので、高さは初めと同じ $2.5\,\mathrm{m}$。<br><b>ポイント</b>：曲面の形によらず、速さは「どれだけ下がったか（高さの差）」だけで決まる。"},
 {"lv": "B", "tag": "摩擦のある面とばね",
  "q": r"図のように、なめらかな斜面と水平面が点 B でなめらかにつながっている。水平面の BC 間（長さ $0.60\,\mathrm{m}$）だけがあらく、C より右はなめらかで、右端にはばね定数 $98\,\mathrm{N/m}$ の軽いばねが壁に固定されている。質量 $0.50\,\mathrm{kg}$ の小物体を、水平面からの高さ $0.80\,\mathrm{m}$ の斜面上の点 A から静かに放す。BC 間の動摩擦係数は $0.40$ とする。<br>" + _fig_track() +
       r"(1) B を初めて通過するときの速さを求めよ。<br>(2) BC 間を1回通過する間に、動摩擦力がする仕事を求めよ。<br>(3) ばねの縮みの最大値を求めよ。<br>(4) 小物体は最終的にどこで静止するか。",
  "a": r"(1) $4.0\,\mathrm{m/s}$　(2) $-1.2\,\mathrm{J}$（$-1.176\,\mathrm{J}$）　(3) $0.24\,\mathrm{m}$　(4) C から B の向きに $0.20\,\mathrm{m}$ の点（B から $0.40\,\mathrm{m}$）",
  "s": r"$mgh=0.50\times9.8\times0.80=3.92\,\mathrm{J}$。<br>(1) $\frac12mv^2=mgh$ より $v=\sqrt{2\times9.8\times0.80}\fallingdotseq4.0\,\mathrm{m/s}$。<br>(2) 動摩擦力の大きさは $0.40\times0.50\times9.8=1.96\,\mathrm{N}$、向きは運動と逆なので $W=-1.96\times0.60=-1.176\,\mathrm{J}$。<br>(3) 力学的エネルギーの変化＝非保存力の仕事：$\frac12\times98\,x^2=3.92-1.176=2.744$ より $x^2=0.056$、$x\fallingdotseq0.24\,\mathrm{m}$。<br>(4) 力学的エネルギーが減るのはあらい面を通るときだけ。静止するまでにあらい面上をすべる道のりの合計を $s$ とすると $1.96\,s=3.92$ より $s=2.0\,\mathrm{m}$。$2.0=0.60\times3+0.20$ なので、B→C、C→B、B→C と3回通過したのち、ばねではね返されて C から B の向きに $0.20\,\mathrm{m}$ 進んだ点で静止する。<br><b>ポイント</b>：摩擦がする仕事は「動摩擦力×道のり（往復も足す）」。エネルギーで考えると、往復の回数は道のりの合計から決まる。"},
 {"lv": "B", "tag": "あらい斜面の往復",
  "q": r"傾斜角 $30^\circ$ のあらい斜面の下端から、質量 $m$ の物体を斜面に沿って上向きに初速 $6.0\,\mathrm{m/s}$ ですべらせたところ、物体は斜面上のある点で一瞬止まった後、すべり下りてきた。物体と斜面の間の動摩擦係数を $\frac{\sqrt3}{6}$ とし、重力加速度の大きさを $g$ とする。<br>(1) 物体がすべっている間の動摩擦力の大きさを $mg$ で表せ。<br>(2) 物体が斜面上を上る距離を求めよ。<br>(3) 物体が下端にもどったときの速さを求めよ。<br>(4) 往復の間に動摩擦力がした仕事の合計を、$m$ [kg] を用いて表せ。",
  "a": r"(1) $\frac14mg$　(2) $2.4\,\mathrm{m}$　(3) $3.5\,\mathrm{m/s}$　(4) $-12m\,[\mathrm{J}]$",
  "s": r"(1) 垂直抗力は $mg\cos30^\circ$。動摩擦力は $\frac{\sqrt3}{6}\times\frac{\sqrt3}{2}mg=\frac14mg$。<br>(2) 上る距離を $L$ とする。上りでは重力の斜面成分 $\frac12mg$ も摩擦力 $\frac14mg$ も運動を妨げる。$0-\frac12mv_0^2=-\left(\frac12+\frac14\right)mgL$ より $L=\frac{2v_0^2}{3g}=\frac{2\times36}{3\times9.8}\fallingdotseq2.4\,\mathrm{m}$。<br>(3) 下りでは重力の斜面成分が正の仕事、摩擦力が負の仕事をする。$\frac12mv^2=\left(\frac12-\frac14\right)mgL=\frac14mg\cdot\frac{2v_0^2}{3g}=\frac16mv_0^2$ より $v=\frac{v_0}{\sqrt3}=\frac{6.0}{\sqrt3}\fallingdotseq3.5\,\mathrm{m/s}$。<br>(4) $-\frac14mg\times2L=-\frac13mv_0^2=-12m\,[\mathrm{J}]$。これは運動エネルギーの変化 $\frac12m\left(\frac{v_0^2}{3}-v_0^2\right)=-12m$ に一致する（重力の仕事は往復で $0$）。<br><b>ポイント</b>：摩擦力は上りでも下りでも運動と逆向き。重力のする仕事は往復で打ち消しあうが、摩擦力の仕事は打ち消しあわない。"},
 {"lv": "B", "tag": "鉛直ばね振り子のエネルギー",
  "q": r"ばね定数 $k=19.6\,\mathrm{N/m}$ の軽いばねの上端を天井に固定し、下端に質量 $m=0.20\,\mathrm{kg}$ のおもりをつける。ばねが自然長となる位置でおもりを手で支え、静かに手をはなした。<br>(1) おもりにはたらく力がつりあう位置での、ばねの伸びを求めよ。<br>(2) おもりが最も下がったときの、ばねの伸びを求めよ。<br>(3) おもりの速さの最大値を求めよ。<br>(4) 手をはなすかわりに、手で支えながらゆっくりおもりを下げて (1) の位置で静止させた。このとき、手がおもりにした仕事を求めよ。",
  "a": r"(1) $0.10\,\mathrm{m}$　(2) $0.20\,\mathrm{m}$　(3) $0.99\,\mathrm{m/s}$　(4) $-9.8\times10^{-2}\,\mathrm{J}$",
  "s": r"(1) $kx_0=mg$ より $x_0=\frac{0.20\times9.8}{19.6}=0.10\,\mathrm{m}$。<br>(2) 最下点では速さ $0$。自然長の位置を重力による位置エネルギーの基準とすると、$0=-mgx+\frac12kx^2$ より $x=\frac{2mg}{k}=0.20\,\mathrm{m}$（つりあいの位置の2倍）。<br>(3) 速さが最大になるのは、合力が $0$ になるつりあいの位置。$0=\frac12mv^2-mgx_0+\frac12kx_0^2$ に $kx_0=mg$ を使うと $\frac12mv^2=\frac12mgx_0$、$v=\sqrt{gx_0}=\sqrt{0.98}\fallingdotseq0.99\,\mathrm{m/s}$。<br>(4) 運動エネルギーは $0$ のまま。手の仕事を $W$ とすると $W=\left(-mgx_0+\frac12kx_0^2\right)-0=-\frac12mgx_0=-0.098\,\mathrm{J}$。<br><b>ポイント</b>：「静かにはなす」と「ゆっくり下ろす」はちがう。ゆっくり下ろすときは手が負の仕事をして、力学的エネルギーが減っている。"},
 {"lv": "B", "tag": "仕事率と速さ",
  "q": r"質量 $1.0\times10^3\,\mathrm{kg}$ の自動車が、一定の仕事率 $2.0\times10^4\,\mathrm{W}$ でエンジンを動かして走る。走行中は、運動を妨げる向きに大きさ $5.0\times10^2\,\mathrm{N}$ の一定の抵抗力を受ける。<br>(1) 水平な道路で、速さが $10\,\mathrm{m/s}$ のときの加速度の大きさを求めよ。<br>(2) 水平な道路での最大の速さを求めよ。<br>(3) 同じ仕事率で、水平と角 $\alpha$（$\sin\alpha=0.050$）をなす上り坂を走るときの最大の速さを求めよ。",
  "a": r"(1) $1.5\,\mathrm{m/s^2}$　(2) $40\,\mathrm{m/s}$　(3) $20\,\mathrm{m/s}$",
  "s": r"エンジンが自動車を進める力を $F$ とすると、仕事率は $P=Fv$。<br>(1) $F=\frac{P}{v}=\frac{2.0\times10^4}{10}=2.0\times10^3\,\mathrm{N}$。$1.0\times10^3\,a=2.0\times10^3-5.0\times10^2$ より $a=1.5\,\mathrm{m/s^2}$。<br>(2) 速さが最大のとき加速度は $0$ なので、$\frac Pv=5.0\times10^2$ より $v=40\,\mathrm{m/s}$。<br>(3) 坂では重力の斜面成分 $mg\sin\alpha=1.0\times10^3\times9.8\times0.050=490\,\mathrm{N}$ も妨げる。$\frac Pv=500+490$ より $v=\frac{2.0\times10^4}{990}\fallingdotseq20\,\mathrm{m/s}$。<br><b>ポイント</b>：仕事率一定なら、速いほど進める力 $F=\frac Pv$ は小さくなる。最大の速さは $F$ が抵抗とつりあうとき。"},
 {"lv": "B", "tag": "連結物体のエネルギー",
  "q": r"水平な机の上に質量 $M=3.0\,\mathrm{kg}$ の物体 A を置き、軽い糸で机の端の滑車を通して質量 $m=1.0\,\mathrm{kg}$ のおもり B とつなぐ。初め A, B を静止させておき、静かに放す。<br>(1) 机がなめらかなとき、B が $0.50\,\mathrm{m}$ 下降したときの B の速さを求めよ。<br>(2) (1) の間に、糸の張力が A にした仕事と B にした仕事を求めよ。<br>(3) A と机の間の動摩擦係数が $0.10$ のとき、B が $0.50\,\mathrm{m}$ 下降したときの B の速さを求めよ。",
  "a": r"(1) $1.6\,\mathrm{m/s}$　(2) A に $3.7\,\mathrm{J}$、B に $-3.7\,\mathrm{J}$　(3) $1.3\,\mathrm{m/s}$",
  "s": r"A と B は同じ速さで動く。2物体をまとめて考えると、張力の仕事は A への正の仕事と B への負の仕事が打ち消しあう。<br>(1) $\frac12(M+m)v^2=mgh$ より $v^2=\frac{2\times1.0\times9.8\times0.50}{4.0}=2.45$、$v\fallingdotseq1.6\,\mathrm{m/s}$。<br>(2) A について運動エネルギーの変化＝された仕事より、張力が A にした仕事は $\frac12\times3.0\times2.45\fallingdotseq3.7\,\mathrm{J}$。B には同じ大きさの張力が運動と逆向きにはたらくので $-3.7\,\mathrm{J}$。<br>(3) 摩擦力の仕事 $-0.10\times3.0\times9.8\times0.50=-1.47\,\mathrm{J}$ を加えて、$\frac12\times4.0\,v^2=4.9-1.47=3.43$、$v^2=1.715$、$v\fallingdotseq1.3\,\mathrm{m/s}$。<br><b>ポイント</b>：糸でつながれた物体系では、張力は内力どうしで仕事の和が $0$。系全体のエネルギーの式を1本立てればよい。"},
 {"lv": "C", "tag": "ばねへの落下",
  "q": r"ばね定数 $k=49\,\mathrm{N/m}$ の軽いばねを鉛直に立てて下端を床に固定する。ばねの上端から高さ $h=0.40\,\mathrm{m}$ の位置から、質量 $m=0.50\,\mathrm{kg}$ の小球を静かに放した。小球はばねの上端に当たった後、ばねと離れずに運動するものとする。<br>(1) 小球がばねに触れる直前の速さを求めよ。<br>(2) ばねの縮みの最大値 $d$ を $m,\ g,\ h,\ k$ で表し、数値を求めよ。<br>(3) 小球の速さが最大になるときのばねの縮みと、そのときの速さを求めよ。<br>(4) ばねが床を押す力の最大値は、小球の重さの何倍か。",
  "a": r"(1) $2.8\,\mathrm{m/s}$　(2) $d=\frac{mg+\sqrt{m^2g^2+2mghk}}{k}$、$0.40\,\mathrm{m}$　(3) $0.10\,\mathrm{m}$、$3.0\,\mathrm{m/s}$　(4) 4倍",
  "s": r"(1) $v=\sqrt{2gh}=\sqrt{2\times9.8\times0.40}=2.8\,\mathrm{m/s}$。<br>(2) 最下点で速さ $0$。放した点から最下点まで小球は $h+d$ 下がるので、$mg(h+d)=\frac12kd^2$。$kd^2-2mgd-2mgh=0$ を解いて、$d>0$ より $d=\frac{mg+\sqrt{m^2g^2+2mghk}}{k}$。数値は $mg=4.9$、$m^2g^2=24.01$、$2mghk=192.08$ より $\sqrt{216.09}=14.7$、$d=\frac{4.9+14.7}{49}=0.40\,\mathrm{m}$。<br>(3) 速さが最大になるのは合力が $0$ のとき：$kx_0=mg$、$x_0=\frac{4.9}{49}=0.10\,\mathrm{m}$。$\frac12mv^2=mg(h+x_0)-\frac12kx_0^2$ より $v^2=2gh+\frac{mg^2}{k}=7.84+0.98=8.82$、$v\fallingdotseq3.0\,\mathrm{m/s}$。<br>(4) ばねの力の最大値は $kd=49\times0.40=19.6\,\mathrm{N}$。ばねは軽いので、床を押す力もこれに等しい。小球の重さ $4.9\,\mathrm{N}$ の4倍。<br><b>ポイント</b>：速さが最大になるのはばねに触れた瞬間ではなく、重力と弾性力がつりあう位置。最下点ではばねの力が重さよりずっと大きくなる。"},
 {"lv": "C", "tag": "あらい面上のばね",
  "q": r"あらい水平面上で、ばね定数 $k=9.8\,\mathrm{N/m}$ の軽いばねの一端を壁に固定し、他端に質量 $m=1.0\,\mathrm{kg}$ の物体をつける。ばねが自然長のときの物体の位置を原点 O とし、ばねが伸びる向きに $x$ 軸をとる。物体と面の間の静止摩擦係数を $0.20$、動摩擦係数を $0.10$ とする。物体を $x=0.45\,\mathrm{m}$ まで引いて静かに放した。<br>(1) 放した直後に物体が動き出すことを確かめよ。<br>(2) 物体が最初に一瞬止まる位置 $x_1$ を求めよ。<br>(3) 物体はその後も動き出すか。動く場合は、次に一瞬止まる位置 $x_2$ を求めよ。<br>(4) 物体が最終的に静止する位置と、放してからそれまでに動摩擦力がした仕事を求めよ。",
  "a": r"(1) 解説参照　(2) $x_1=-0.25\,\mathrm{m}$　(3) 動き出す、$x_2=0.050\,\mathrm{m}$　(4) $x=0.050\,\mathrm{m}$、$-0.98\,\mathrm{J}$",
  "s": r"動摩擦力の大きさは $\mu'mg=0.10\times1.0\times9.8=0.98\,\mathrm{N}$、最大摩擦力は $\mu mg=1.96\,\mathrm{N}$。<br>(1) $x=0.45\,\mathrm{m}$ での弾性力 $9.8\times0.45=4.41\,\mathrm{N}$ が最大摩擦力 $1.96\,\mathrm{N}$ より大きいので動き出す。<br>(2) $x_0=0.45$ から $x_1\ (<0)$ まで動く間の道のりは $x_0-x_1$。力学的エネルギーの変化＝動摩擦力の仕事より $\frac12kx_1^2-\frac12kx_0^2=-\mu'mg(x_0-x_1)$。両辺を $x_0-x_1$ で割ると $\frac12k(x_0+x_1)=\mu'mg$、$x_1=\frac{2\mu'mg}{k}-x_0=0.20-0.45=-0.25\,\mathrm{m}$。<br>(3) $x_1$ での弾性力 $9.8\times0.25=2.45\,\mathrm{N}>1.96\,\mathrm{N}$ なので再び動き出す。同様に $\frac12k(x_2^2-x_1^2)=-\mu'mg(x_2-x_1)$ より $x_2=-x_1-\frac{2\mu'mg}{k}=0.25-0.20=0.050\,\mathrm{m}$。<br>(4) $x_2$ での弾性力 $9.8\times0.050=0.49\,\mathrm{N}<1.96\,\mathrm{N}$ なので、そのまま静止する。道のりは $0.70+0.30=1.00\,\mathrm{m}$ で、動摩擦力の仕事は $-0.98\times1.00=-0.98\,\mathrm{J}$。（弾性エネルギーの減少 $\frac12\times9.8\times(0.45^2-0.050^2)=0.98\,\mathrm{J}$ と一致する。）<br><b>ポイント</b>：止まる位置は1回ごとに $\frac{2\mu'mg}{k}$ ずつ原点に近づく。止まった位置で「弾性力 ≦ 最大摩擦力」なら、そこで静止する。"},
]}}


def verify():
    g = Rational(98, 10)
    # 3-1
    W = 5 * g * 4
    _near(W, 2.0e2); _near(W / 10, 20); assert 10 * 3 * cos(pi / 3) == 15
    # 3-2
    v2 = (Rational(1, 2) * 2 * 9 + 32) * 2 / 2
    assert v2 == 41; _near(sqrt(41), 6.4); _near(Rational(41, 6), 6.8)
    # 3-3
    assert Rational(1, 2) * 50 * Rational(4, 100) == 1
    assert sqrt(2 * 1 / Rational(1, 2)) == 2
    v = sqrt((1 - Rational(1, 2) * 50 * Rational(1, 100)) * 2 / Rational(1, 2))
    _eq(v, sqrt(3)); _near(v, 1.7)
    # 3-4
    assert sqrt(2 * g * Rational(5, 2)) == 7 and sqrt(2 * g * Rational(9, 10)) == Rational(42, 10)
    # 3-5
    m, k, h, L, mu = Rational(1, 2), 98, Rational(8, 10), Rational(6, 10), Rational(4, 10)
    _near(sqrt(2 * g * h), 4.0)
    Wf = -mu * m * g * L
    _near(Wf, -1.2); assert Wf == Rational(-1176, 1000)
    x = sqrt(2 * (m * g * h + Wf) / k); _near(x, 0.24)
    s = m * g * h / (mu * m * g)
    assert s == 2 and s - 3 * L == Rational(1, 5)
    # 3-6
    mm, gg, v0 = symbols("m g v0", positive=True)
    f = sqrt(3) / 6 * mm * gg * cos(pi / 6)
    _eq(f, mm * gg / 4)
    Ls = solve(Eq(Rational(1, 2) * mm * v0 ** 2, (mm * gg * sin(pi / 6) + f) * symbols("L")), symbols("L"))[0]
    _eq(Ls, 2 * v0 ** 2 / (3 * gg))
    _near(Ls.subs({v0: 6, gg: g}), 2.4)
    vb = sqrt(2 * (mm * gg * sin(pi / 6) - f) * Ls / mm)
    _eq(vb, v0 / sqrt(3)); _near(vb.subs(v0, 6), 3.5)
    _eq(-f * 2 * Ls, -mm * v0 ** 2 / 3); assert (-mm * v0 ** 2 / 3).subs({v0: 6}) == -12 * mm
    # 3-7
    k, m = Rational(196, 10), Rational(2, 10)
    x0 = m * g / k
    assert x0 == Rational(1, 10)
    xs = solve(-m * g * symbols("x") + Rational(1, 2) * k * symbols("x") ** 2, symbols("x"))
    assert max(xs) == Rational(1, 5)
    v = sqrt(2 * (m * g * x0 - Rational(1, 2) * k * x0 ** 2) / m); _near(v, 0.99)
    Wh = -m * g * x0 + Rational(1, 2) * k * x0 ** 2
    _near(Wh, -9.8e-2)
    # 3-8
    P, f, M = 2 * 10 ** 4, 500, 1000
    assert Rational(P, 10) == 2000 and Rational(2000 - 500, 1000) == Rational(3, 2) and Rational(P, f) == 40
    _near(Rational(P) / (f + M * g * Rational(5, 100)), 20)
    # 3-9
    v2 = 2 * 1 * g * Rational(1, 2) / 4
    assert v2 == Rational(245, 100); _near(sqrt(v2), 1.6); _near(Rational(1, 2) * 3 * v2, 3.7)
    v2b = (g * Rational(1, 2) - Rational(1, 10) * 3 * g * Rational(1, 2)) * 2 / 4
    _near(sqrt(v2b), 1.3)
    # 3-10
    k, m, h = 49, Rational(1, 2), Rational(4, 10)
    _near(sqrt(2 * g * h), 2.8); assert sqrt(2 * g * h) == Rational(28, 10)
    d = symbols("d", positive=True)
    ds = solve(Eq(m * g * (h + d), Rational(1, 2) * k * d ** 2), d)
    assert ds == [Rational(2, 5)]
    K, Mg, Hh = symbols("k mg h", positive=True)
    dd = solve(Eq(Mg * (Hh + symbols("dd")), K * symbols("dd") ** 2 / 2), symbols("dd"))
    dpos = [r for r in dd if r.subs({Mg: 4.9, Hh: 0.4, K: 49}) > 0]
    assert len(dpos) == 1
    _eq(dpos[0], (Mg + sqrt(Mg ** 2 + 2 * Mg * Hh * K)) / K)
    x0 = m * g / k
    assert x0 == Rational(1, 10)
    v2 = 2 * g * h + m * g ** 2 / k
    _eq(v2, (m * g * (h + x0) - Rational(1, 2) * k * x0 ** 2) * 2 / m); _near(sqrt(v2), 3.0)
    assert k * Rational(2, 5) / (m * g) == 4
    # 3-11
    k, m, mus, muk = Rational(98, 10), 1, Rational(2, 10), Rational(1, 10)
    x = symbols("x")
    assert k * Rational(45, 100) > mus * m * g
    x1 = [r for r in solve(Eq(k * x ** 2 / 2 - k * Rational(45, 100) ** 2 / 2, -muk * m * g * (Rational(45, 100) - x)), x) if r < 0][0]
    assert x1 == Rational(-1, 4) and k * Rational(1, 4) > mus * m * g
    x2 = [r for r in solve(Eq(k * x ** 2 / 2 - k * x1 ** 2 / 2, -muk * m * g * (x - x1)), x) if r > x1][0]
    assert x2 == Rational(1, 20) and k * x2 < mus * m * g
    W = -muk * m * g * ((Rational(45, 100) - x1) + (x2 - x1))
    _near(W, -0.98); _eq(W, Rational(1, 2) * k * (x2 ** 2 - Rational(45, 100) ** 2))
