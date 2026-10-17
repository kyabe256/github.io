"""問題集 第7章 万有引力。CH に問題、verify() で答えを sympy で検算する。"""
import math
from sympy import *


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) < 0.5 * 10 ** e * (1 - 1e-9), (x, shown, n)


def _eq(a, b):
    assert simplify(a - b) == 0, (a, b)


def _tx(x, y, s, size=11, it=False, anchor="start", c="#222"):
    st = ' font-style="italic"' if it else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{st}>{s}</text>'


def _fig_transfer():
    """円軌道（半径 r）と、近地点 P（距離 r）・遠地点 Q（距離 3r）の楕円。焦点は地球の中心 O"""
    u, ox, oy = 24, 72, 66
    a, c = 2 * u, u                   # 半長軸 2r、中心と焦点の距離 r
    b = math.sqrt(a * a - c * c)
    ecx = ox + c                      # 楕円の中心（O から Q の向きに r）
    px, qx = ox - u, ox + 3 * u
    s = [f'<svg class="fig" width="200" height="132" viewBox="0 0 200 132">',
         f'<circle cx="{ox}" cy="{oy}" r="{u}" fill="none" stroke="#777" stroke-width="1.1" stroke-dasharray="4,3"/>',
         f'<ellipse cx="{ecx}" cy="{oy}" rx="{a}" ry="{b:.1f}" fill="none" stroke="#1d4e89" stroke-width="1.6"/>',
         f'<circle cx="{ox}" cy="{oy}" r="9" fill="#cfe0f5" stroke="#333" stroke-width="1"/>',
         f'<circle cx="{px}" cy="{oy}" r="3" fill="#c0392b"/><circle cx="{qx}" cy="{oy}" r="3" fill="#c0392b"/>',
         f'<line x1="{ox}" y1="{oy}" x2="{qx}" y2="{oy}" stroke="#999" stroke-width="0.8" stroke-dasharray="2,2"/>',
         _tx(ox, oy + 22, "O", 11, anchor="middle"), _tx(px - 5, oy + 4, "P", 11, anchor="end"),
         _tx(qx + 5, oy + 4, "Q", 11), _tx((ox + qx) / 2 + 12, oy - 4, "3r", 11, True, anchor="middle"),
         '</svg>']
    return "".join(s)


CH = {7: {
"goal": r"万有引力 $F=G\frac{Mm}{r^2}$ と、地表での関係 $GM=gR^2$ のおきかえ。円軌道は「万有引力＝向心力」、楕円軌道は「面積速度一定＋力学的エネルギー保存（位置エネルギー $U=-G\frac{Mm}{r}$）」で解く。<br>（数値は有効数字2桁。万有引力定数 $G=6.7\times10^{-11}\,\mathrm{N\cdot m^2/kg^2}$、地球の半径 $R=6.4\times10^6\,\mathrm{m}$、地表の重力加速度の大きさ $g=9.8\,\mathrm{m/s^2}$、$\pi=3.14$ とする。地球の自転は、断りがなければ無視する。）",
"items": [
 {"lv": "A", "tag": "ケプラーの法則",
  "q": r"(1) ケプラーの3法則をそれぞれ簡潔に述べよ。<br>(2) 太陽のまわりを回る小惑星の楕円軌道の半長軸（長半径）が、地球の公転軌道の半径の $4.0$ 倍であるとき、この小惑星の公転周期は何年か。地球の軌道は円とみなす。<br>(3) ある惑星の近日点と遠日点の太陽からの距離が $r_1,\ r_2$ であるとき、近日点と遠日点での速さの比 $v_1:v_2$ を求めよ。",
  "a": r"(1) 解説参照　(2) $8.0$ 年　(3) $v_1:v_2=r_2:r_1$",
  "s": r"(1) 第1法則：惑星は太陽を1つの焦点とする楕円軌道を描く。第2法則：惑星と太陽を結ぶ線分が単位時間に描く面積（面積速度）は一定。第3法則：公転周期 $T$ の2乗は楕円の半長軸 $a$ の3乗に比例する（$\frac{T^2}{a^3}$ は惑星によらず一定）。<br>(2) $T^2\propto a^3$ より $T=1\times4.0^{\frac32}=8.0$ 年。<br>(3) 近日点・遠日点では速度が太陽との線分に垂直なので、面積速度は $\frac12r_1v_1=\frac12r_2v_2$。よって $v_1:v_2=r_2:r_1$。<br><b>ポイント</b>：面積速度一定は「太陽に近いほど速い」ことを表す。"},
 {"lv": "A", "tag": "万有引力の法則",
  "q": r"(1) 質量 $50\,\mathrm{kg}$ と $60\,\mathrm{kg}$ の2人が $1.0\,\mathrm{m}$ 離れているとき、互いにはたらく万有引力の大きさを求めよ（2人を質点とみなす）。<br>(2) 2人の距離を $2.0\,\mathrm{m}$ にすると、万有引力の大きさは何倍になるか。<br>(3) (1) の力は、質量 $50\,\mathrm{kg}$ の人にはたらく重力の大きさの約何倍か。",
  "a": r"(1) $2.0\times10^{-7}\,\mathrm{N}$　(2) $\frac14$ 倍　(3) 約 $4\times10^{-10}$ 倍",
  "s": r"(1) $F=G\frac{Mm}{r^2}=6.7\times10^{-11}\times\frac{50\times60}{1.0^2}\fallingdotseq2.0\times10^{-7}\,\mathrm{N}$。<br>(2) 距離の2乗に反比例するので $\frac14$ 倍。<br>(3) 重力は $50\times9.8=490\,\mathrm{N}$。$\frac{2.0\times10^{-7}}{490}\fallingdotseq4\times10^{-10}$。<br><b>ポイント</b>：身近な物体どうしの万有引力は非常に小さい。地球の重力が大きいのは地球の質量が巨大だから。"},
 {"lv": "A", "tag": "重力と万有引力",
  "q": r"地球を一様な球とする。<br>(1) 地表の物体にはたらく重力が地球からの万有引力に等しいとして、地球の質量 $M$ を $g,\ R,\ G$ で表し、数値を求めよ。<br>(2) 地表からの高さが $R$ の位置での重力加速度の大きさは、地表の何倍か。<br>(3) 地表からの高さ $h$ の位置での重力加速度の大きさを $g,\ R,\ h$ で表せ。",
  "a": r"(1) $M=\frac{gR^2}{G}$、$6.0\times10^{24}\,\mathrm{kg}$　(2) $\frac14$ 倍　(3) $\frac{gR^2}{(R+h)^2}$",
  "s": r"(1) $mg=G\frac{Mm}{R^2}$ より $M=\frac{gR^2}{G}=\frac{9.8\times(6.4\times10^6)^2}{6.7\times10^{-11}}\fallingdotseq6.0\times10^{24}\,\mathrm{kg}$。<br>(2) 中心からの距離が $2R$ なので $\frac{1}{2^2}=\frac14$ 倍。<br>(3) $g'=\frac{GM}{(R+h)^2}=\frac{gR^2}{(R+h)^2}$。<br><b>ポイント</b>：$G$ と $M$ が与えられていないときは $GM=gR^2$ とおきかえる。"},
 {"lv": "A", "tag": "第1宇宙速度",
  "q": r"地表すれすれを回る人工衛星（地球の中心を中心とする半径 $R$ の等速円運動）について答えよ。<br>(1) 衛星の速さ（第1宇宙速度）を $g,\ R$ で表し、数値を求めよ。<br>(2) 衛星の周期を求めよ。<br>(3) 衛星の中の物体が「無重量状態」になる理由を説明せよ。",
  "a": r"(1) $\sqrt{gR}$、$7.9\times10^3\,\mathrm{m/s}$　(2) $5.1\times10^3\,\mathrm{s}$（約85分）　(3) 解説参照",
  "s": r"(1) 万有引力（＝重力 $mg$）が向心力：$m\frac{v^2}{R}=mg$ より $v=\sqrt{gR}=\sqrt{9.8\times6.4\times10^6}\fallingdotseq7.9\times10^3\,\mathrm{m/s}$。<br>(2) $T=\frac{2\pi R}{v}=\frac{2\times3.14\times6.4\times10^6}{7.92\times10^3}\fallingdotseq5.1\times10^3\,\mathrm{s}$。<br>(3) 衛星も中の物体も、万有引力だけを受けて同じ加速度で運動しているので、物体は衛星の床を押さない。衛星とともに回る立場では、万有引力と遠心力がつりあっている。<br><b>ポイント</b>：無重量状態は「重力がない」のではなく、「重力だけで運動している（自由落下している）」状態。"},
 {"lv": "B", "tag": "静止衛星",
  "q": r"赤道上空を、地球の自転と同じ向きに、自転と同じ周期 $T=8.6\times10^4\,\mathrm{s}$ で円運動する静止衛星がある。<br>(1) 軌道半径 $r$ を $g,\ R,\ T$ で表せ。<br>(2) $r$ の値を求め、地球の半径の約何倍かを答えよ。<br>(3) 静止衛星の速さを求めよ。",
  "a": r"(1) $r=\sqrt[3]{\frac{gR^2T^2}{4\pi^2}}$　(2) $4.2\times10^7\,\mathrm{m}$、約 $6.6$ 倍　(3) $3.1\times10^3\,\mathrm{m/s}$",
  "s": r"(1) $mr\left(\frac{2\pi}{T}\right)^2=G\frac{Mm}{r^2}$、$GM=gR^2$ より $r^3=\frac{gR^2T^2}{4\pi^2}$。<br>(2) $r^3=\frac{9.8\times(6.4\times10^6)^2\times(8.6\times10^4)^2}{4\times3.14^2}\fallingdotseq7.5\times10^{22}$ より $r\fallingdotseq4.2\times10^7\,\mathrm{m}$。$\frac rR\fallingdotseq6.6$。<br>(3) $v=\frac{2\pi r}{T}=\frac{2\times3.14\times4.22\times10^7}{8.6\times10^4}\fallingdotseq3.1\times10^3\,\mathrm{m/s}$。<br><b>ポイント</b>：周期が決まれば軌道半径が1つに決まる（ケプラーの第3法則）。静止衛星は地表すれすれの衛星より遅い。"},
 {"lv": "B", "tag": "位置エネルギーと脱出速度",
  "q": r"地球の質量を $M$、万有引力定数を $G$ とする。<br>(1) 質量 $m$ の物体の、地球の中心から距離 $r$ の点での万有引力による位置エネルギーを、無限遠を基準として表せ。<br>(2) 地表から打ち上げた物体が、地球の引力を振り切って無限遠まで飛び去るための最小の速さ（第2宇宙速度）を $g,\ R$ で表し、数値を求めよ。<br>(3) 地表から鉛直上向きに速さ $\sqrt{gR}$ で打ち上げた物体が達する最高点の、地表からの高さを求めよ。空気抵抗は無視する。",
  "a": r"(1) $-G\frac{Mm}{r}$　(2) $\sqrt{2gR}$、$1.1\times10^4\,\mathrm{m/s}$　(3) $R$",
  "s": r"(1) $U=-G\frac{Mm}{r}$（無限遠で $0$、近づくほど小さい）。<br>(2) 無限遠で速さ $0$ になる場合が最小：$\frac12mv^2-G\frac{Mm}{R}=0$。$GM=gR^2$ より $v=\sqrt{2gR}=\sqrt{2\times9.8\times6.4\times10^6}\fallingdotseq1.1\times10^4\,\mathrm{m/s}$。<br>(3) 最高点の中心からの距離を $r$ とすると $\frac12m(gR)-\frac{mgR^2}{R}=-\frac{mgR^2}{r}$。$-\frac12gR=-\frac{gR^2}{r}$ より $r=2R$、高さは $R$。<br><b>ポイント</b>：高さが $R$ と比べて無視できないときは $mgh$ を使わず、$-G\frac{Mm}{r}$ で考える（$mgh$ で計算すると高さ $\frac R2$ となり誤り）。"},
 {"lv": "B", "tag": "楕円軌道への移行",
  "q": r"地球（質量 $M$）の中心 O から距離 $r$ の円軌道を速さ $v_0$ で回っている人工衛星が、点 P で進行方向に瞬間的に加速して、P を近地点、O からの距離が $3r$ の点 Q を遠地点とする楕円軌道に移った。万有引力定数を $G$ とする。<br>" + _fig_transfer() +
       r"(1) $v_0$ を $G,\ M,\ r$ で表せ。<br>(2) P で加速した直後の速さ $v_P$ と、Q での速さ $v_Q$ を $v_0$ で表せ。<br>(3) 楕円軌道の周期は、もとの円軌道の周期の何倍か。",
  "a": r"(1) $v_0=\sqrt{\frac{GM}{r}}$　(2) $v_P=\frac{\sqrt6}{2}v_0$、$v_Q=\frac{\sqrt6}{6}v_0$　(3) $2\sqrt2$ 倍",
  "s": r"(1) $m\frac{v_0^2}{r}=G\frac{Mm}{r^2}$ より $v_0=\sqrt{\frac{GM}{r}}$。<br>(2) 面積速度一定：$\frac12rv_P=\frac12(3r)v_Q$ より $v_Q=\frac{v_P}{3}$。<br>力学的エネルギー保存：$\frac12mv_P^2-G\frac{Mm}{r}=\frac12mv_Q^2-G\frac{Mm}{3r}$。<br>代入して $\frac12v_P^2\left(1-\frac19\right)=\frac{GM}{r}\cdot\frac23$、$v_P^2=\frac32\cdot\frac{GM}{r}=\frac32v_0^2$。$v_P=\frac{\sqrt6}{2}v_0$、$v_Q=\frac{\sqrt6}{6}v_0$。<br>(3) 楕円の半長軸は $\frac{r+3r}{2}=2r$。ケプラーの第3法則 $T^2\propto a^3$ より $2^{\frac32}=2\sqrt2$ 倍。<br><b>ポイント</b>：楕円軌道は「近地点・遠地点で面積速度一定（速度が半径に垂直）」と「力学的エネルギー保存」の連立で解く。"},
 {"lv": "B", "tag": "自転と重力",
  "q": r"地球の自転周期を $T=8.6\times10^4\,\mathrm{s}$ とし、地表で地球の万有引力だけによる加速度の大きさを $9.8\,\mathrm{m/s^2}$ とする。<br>(1) 赤道上で静止している質量 $1.0\,\mathrm{kg}$ の物体が受ける遠心力（地球とともに回る立場で考える）の大きさを求めよ。<br>(2) 赤道上の物体にはたらく重力（万有引力と遠心力の合力）の大きさは、北極での重力の大きさより約何％小さいか。<br>(3) 自転周期がいくらより短くなると、赤道上の物体は地表から浮き上がるか。",
  "a": r"(1) $3.4\times10^{-2}\,\mathrm{N}$　(2) 約 $0.35$ ％　(3) $5.1\times10^3\,\mathrm{s}$",
  "s": r"(1) $\omega=\frac{2\pi}{T}=\frac{6.28}{8.6\times10^4}\fallingdotseq7.30\times10^{-5}\,\mathrm{rad/s}$。遠心力 $mR\omega^2=1.0\times6.4\times10^6\times(7.30\times10^{-5})^2\fallingdotseq3.4\times10^{-2}\,\mathrm{N}$。<br>(2) 北極では遠心力が $0$（回転軸上）なので重力は $9.8\,\mathrm{N}$。赤道では遠心力が万有引力と逆向き（鉛直上向き）なので $9.8-0.034$。$\frac{0.034}{9.8}\times100\fallingdotseq0.35$ ％小さい。<br>(3) 遠心力が万有引力に等しくなる：$mR\omega^2=mg$ より $T=2\pi\sqrt{\frac Rg}=6.28\times\sqrt{\frac{6.4\times10^6}{9.8}}\fallingdotseq5.1\times10^3\,\mathrm{s}$（地表すれすれの衛星の周期と同じ）。<br><b>ポイント</b>：重力＝万有引力＋自転による遠心力。遠心力は回転軸からの距離に比例するので、赤道で最大、極で $0$。"},
 {"lv": "B", "tag": "人工衛星の比較",
  "q": r"地球のまわりを円軌道で回る2つの人工衛星 A, B の軌道半径はそれぞれ $r,\ 4r$ で、質量はどちらも $m$ である。地球の質量を $M$、万有引力定数を $G$ とする。<br>(1) A, B の速さの比 $v_A:v_B$ を求めよ。<br>(2) 周期の比 $T_A:T_B$ を求めよ。<br>(3) A の力学的エネルギー（無限遠を位置エネルギーの基準とする）を求めよ。また、A と B のどちらの力学的エネルギーが大きいか。<br>(4) A を B の軌道に移すには、少なくともどれだけのエネルギーを与える必要があるか。",
  "a": r"(1) $2:1$　(2) $1:8$　(3) $-\frac{GMm}{2r}$、B の方が大きい　(4) $\frac{3GMm}{8r}$",
  "s": r"半径 $r$ の円軌道では $m\frac{v^2}{r}=G\frac{Mm}{r^2}$ より $v=\sqrt{\frac{GM}{r}}$。<br>(1) $v\propto\frac{1}{\sqrt r}$ なので $v_A:v_B=2:1$。<br>(2) $T=\frac{2\pi r}{v}\propto r^{\frac32}$ なので $1:8$。<br>(3) $E=\frac12mv^2-\frac{GMm}{r}=\frac{GMm}{2r}-\frac{GMm}{r}=-\frac{GMm}{2r}$。B は $-\frac{GMm}{8r}$ で、B の方が大きい（$0$ に近い）。<br>(4) $E_B-E_A=-\frac{GMm}{8r}+\frac{GMm}{2r}=\frac{3GMm}{8r}$。<br><b>ポイント</b>：円軌道では運動エネルギー $=\frac{GMm}{2r}$、力学的エネルギー $=-\frac{GMm}{2r}$。外側の軌道ほど遅いが、エネルギーは大きい。"},
 {"lv": "C", "tag": "連星",
  "q": r"互いの万有引力だけを受けて、共通の重心 C のまわりを同じ周期で等速円運動している2つの星 A（質量 $M_1$）と B（質量 $M_2$）がある。AB 間の距離は $d$ で一定である。万有引力定数を $G$ とする。<br>(1) A, B の円軌道の半径 $r_1,\ r_2$ を求めよ。<br>(2) 周期 $T$ を求めよ。<br>(3) A と B の速さの比、運動エネルギーの比を求めよ。<br>(4) 観測によって $d$ と $T$ がわかると、何を求めることができるか。式で示せ。",
  "a": r"(1) $r_1=\frac{M_2}{M_1+M_2}d$、$r_2=\frac{M_1}{M_1+M_2}d$　(2) $T=2\pi\sqrt{\frac{d^3}{G(M_1+M_2)}}$　(3) 速さ $M_2:M_1$、運動エネルギー $M_2:M_1$　(4) 質量の和 $M_1+M_2=\frac{4\pi^2d^3}{GT^2}$",
  "s": r"(1) 重心は AB を $M_2:M_1$ に内分する点なので $r_1=\frac{M_2}{M_1+M_2}d$、$r_2=\frac{M_1}{M_1+M_2}d$。<br>(2) A の運動方程式（向心力＝万有引力）：$M_1r_1\omega^2=G\frac{M_1M_2}{d^2}$。$r_1$ を代入して $\omega^2=\frac{G(M_1+M_2)}{d^3}$、$T=\frac{2\pi}{\omega}=2\pi\sqrt{\frac{d^3}{G(M_1+M_2)}}$。（B の式からも同じ結果になる。）<br>(3) 角速度が等しいので $v_1:v_2=r_1:r_2=M_2:M_1$。運動エネルギーの比は $M_1v_1^2:M_2v_2^2=M_1M_2^2:M_2M_1^2=M_2:M_1$。<br>(4) (2) を変形して $M_1+M_2=\frac{4\pi^2d^3}{GT^2}$。<br><b>ポイント</b>：連星では「中心」は重い方の星ではなく共通重心。半径は $d$ ではなく $r_1$ だが、万有引力の距離は $d$ であることに注意。"},
 {"lv": "C", "tag": "地球を貫くトンネル",
  "q": r"地球を半径 $R$、密度が一様な球とし、自転と空気抵抗は無視する。一様な球の内部の、中心から距離 $r$ の点にある物体にはたらく万有引力は、半径 $r$ より内側の部分の質量がすべて中心に集まったときの万有引力に等しい（外側の部分からの引力は打ち消しあう）ことが知られている。地球の中心を通るまっすぐなトンネルを掘り、地表の入口から質量 $m$ の物体を静かに放した。地表の重力加速度の大きさを $g$ とする。<br>(1) 中心から距離 $r$（$r\leqq R$）の点で物体にはたらく力の大きさを、$m,\ g,\ R,\ r$ で表せ。<br>(2) 物体は単振動することを示し、その周期を求めよ。<br>(3) 物体が反対側の地表に達するまでの時間と、中心を通過するときの速さを数値で求めよ。<br>(4) 中心を通らないまっすぐなトンネル（中心からトンネルまでの距離 $b$）の場合、トンネルに沿った運動の周期はどうなるか。",
  "a": r"(1) $\frac{mgr}{R}$　(2) 周期 $2\pi\sqrt{\frac Rg}$　(3) $2.5\times10^3\,\mathrm{s}$（約42分）、$7.9\times10^3\,\mathrm{m/s}$　(4) $2\pi\sqrt{\frac Rg}$ で変わらない",
  "s": r"(1) 地球の質量を $M$ とすると、半径 $r$ の内側の質量は $M\frac{r^3}{R^3}$。力は $G\frac{mM}{r^2}\cdot\frac{r^3}{R^3}=\frac{GMm}{R^3}r=\frac{mg}{R}r$（$GM=gR^2$）。<br>(2) 中心を原点にトンネルに沿って $x$ 軸をとると、力は中心向きで $F=-\frac{mg}{R}x$。変位に比例する復元力なので単振動で、$T=2\pi\sqrt{\frac{m}{mg/R}}=2\pi\sqrt{\frac Rg}$。<br>(3) 反対側まで $\frac T2=\pi\sqrt{\frac Rg}=3.14\times\sqrt{\frac{6.4\times10^6}{9.8}}\fallingdotseq2.5\times10^3\,\mathrm{s}$。中心での速さは $A\omega=R\sqrt{\frac gR}=\sqrt{gR}\fallingdotseq7.9\times10^3\,\mathrm{m/s}$（第1宇宙速度と同じ）。<br>(4) トンネルの中点からトンネルに沿って $s$ の位置では、中心までの距離は $r=\sqrt{b^2+s^2}$。力 $\frac{mg}{R}r$ のトンネル方向の成分は $\frac{mg}{R}r\cdot\frac sr=\frac{mg}{R}s$（中点向き）。やはり単振動で、周期は $2\pi\sqrt{\frac Rg}$ と変わらない。<br><b>ポイント</b>：復元力が「変位に比例」することさえ示せれば、単振動の結果がすべて使える。この周期は地表すれすれの人工衛星の周期と等しい。"},
]}}


def verify():
    g = Rational(98, 10)
    G = Rational(67, 10) * Rational(1, 10 ** 11)
    R = Rational(64, 10) * 10 ** 6
    PI = Rational(314, 100)
    # 7-1
    assert Rational(4) ** Rational(3, 2) == 8
    # 7-2
    F = G * 50 * 60
    _near(F, 2.0e-7); _near(F / (50 * g), 4e-10, 1)
    # 7-3
    _near(g * R ** 2 / G, 6.0e24)
    # 7-4
    v = sqrt(g * R); _near(v, 7.9e3); _near(2 * PI * R / v, 5.1e3)
    # 7-5
    T = Rational(86, 10) * 10 ** 4
    r = (g * R ** 2 * T ** 2 / (4 * PI ** 2)) ** Rational(1, 3)
    _near(r ** 3, 7.5e22); _near(r, 4.2e7); _near(r / R, 6.6); _near(2 * PI * r / T, 3.1e3)
    # 7-6
    M, m, Gs, rr, gg, Rs, vv = symbols("M m G r g R v", positive=True)
    _near(sqrt(2 * g * R), 1.1e4)
    rmax = solve(Eq(Rational(1, 2) * m * gg * Rs - m * gg * Rs, -m * gg * Rs ** 2 / rr), rr)[0]
    _eq(rmax, 2 * Rs)
    # 7-7
    vP, vQ = symbols("vP vQ", positive=True)
    s = solve([rr * vP - 3 * rr * vQ, vP ** 2 / 2 - Gs * M / rr - vQ ** 2 / 2 + Gs * M / (3 * rr)], [vP, vQ], dict=True)[0]
    v0 = sqrt(Gs * M / rr)
    _eq(s[vP], sqrt(6) / 2 * v0); _eq(s[vQ], sqrt(6) / 6 * v0)
    assert Rational(2) ** Rational(3, 2) == 2 * sqrt(2)
    # 7-8
    w = 2 * PI / T
    fc = R * w ** 2
    _near(fc, 3.4e-2); _near(fc / g * 100, 0.35)
    _near(2 * PI * sqrt(R / g), 5.1e3)
    # 7-9
    vr = lambda x: sqrt(Gs * M / x)
    _eq(vr(rr) / vr(4 * rr), 2)
    Tr = lambda x: 2 * pi * x / vr(x)
    _eq(Tr(rr) / Tr(4 * rr), Rational(1, 8))
    E = lambda x: m * vr(x) ** 2 / 2 - Gs * M * m / x
    _eq(E(rr), -Gs * M * m / (2 * rr)); _eq(E(4 * rr) - E(rr), 3 * Gs * M * m / (8 * rr))
    # 7-10
    M1, M2, d, w2 = symbols("M1 M2 d w2", positive=True)
    r1, r2 = M2 * d / (M1 + M2), M1 * d / (M1 + M2)
    _eq(M1 * r1 + 0, M2 * r2)
    om2 = solve(Eq(M1 * r1 * w2, Gs * M1 * M2 / d ** 2), w2)[0]
    _eq(om2, Gs * (M1 + M2) / d ** 3)
    _eq(solve(Eq(M2 * r2 * w2, Gs * M1 * M2 / d ** 2), w2)[0], om2)
    _eq((M1 * r1 ** 2) / (M2 * r2 ** 2), M2 / M1)
    # 7-11
    x = symbols("x", positive=True)
    Fin = Gs * m * M * x ** 3 / Rs ** 3 / x ** 2
    _eq(Fin.subs(Gs * M, gg * Rs ** 2), m * gg * x / Rs)
    _near(PI * sqrt(R / g), 2.5e3); _near(sqrt(g * R), 7.9e3)
    b, sx = symbols("b s", positive=True)
    rr2 = sqrt(b ** 2 + sx ** 2)
    _eq(m * gg / Rs * rr2 * sx / rr2, m * gg * sx / Rs)
