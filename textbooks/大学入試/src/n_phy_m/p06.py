"""問題集 第6章 単振動。CH に問題、verify() で答えを sympy で検算する。"""
import math
from sympy import *


def _near(x, shown, n=2):
    """x を有効数字 n 桁に丸めると shown になることを確かめる"""
    x = float(x)
    e = math.floor(math.log10(abs(shown))) - n + 1
    assert abs(x - shown) < 0.5 * 10 ** e * (1 - 1e-9), (x, shown, n)


def _eq(a, b):
    assert simplify(a - b) == 0, (a, b)


CH = {6: {
"goal": r"単振動は $x=A\sin(\omega t+\phi_0)$、$v_{\max}=A\omega$、$a=-\omega^2x$。物体にはたらく力が $F=-Kx$（$x$ は振動の中心からの変位）の形になることを示せば、周期 $T=2\pi\sqrt{\frac mK}$ が決まる。振動の中心（つりあいの位置）を正しく見つけることが第一歩。<br>（数値は有効数字2桁、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$ とする。）",
"items": [
 {"lv": "A", "tag": "単振動の式",
  "q": r"$x$ 軸上で、原点を中心に $x=0.10\sin\pi t$（$x$ の単位は $\mathrm m$、$t$ の単位は $\mathrm s$）で表される単振動をする物体がある。$\pi=3.14$ とする。<br>(1) 振幅、周期、振動数を求めよ。<br>(2) 速さの最大値と、それが生じる位置を求めよ。<br>(3) 加速度の大きさの最大値と、それが生じる位置を求めよ。<br>(4) $t=\frac16\,\mathrm{s}$ での位置を求めよ。",
  "a": r"(1) $0.10\,\mathrm{m}$、$2.0\,\mathrm{s}$、$0.50\,\mathrm{Hz}$　(2) $0.31\,\mathrm{m/s}$、$x=0$　(3) $0.99\,\mathrm{m/s^2}$、$x=\pm0.10\,\mathrm{m}$　(4) $x=0.050\,\mathrm{m}$",
  "s": r"$x=A\sin\omega t$ と比べて $A=0.10\,\mathrm{m}$、$\omega=\pi\,\mathrm{rad/s}$。<br>(1) $T=\frac{2\pi}{\omega}=2.0\,\mathrm{s}$、$f=\frac1T=0.50\,\mathrm{Hz}$。<br>(2) $v_{\max}=A\omega=0.10\times3.14\fallingdotseq0.31\,\mathrm{m/s}$。振動の中心 $x=0$ で最大。<br>(3) $a=-\omega^2x$ より、$|a|$ は両端 $x=\pm A$ で最大 $A\omega^2=0.10\times3.14^2\fallingdotseq0.99\,\mathrm{m/s^2}$。<br>(4) $x=0.10\sin\frac{\pi}{6}=0.050\,\mathrm{m}$。<br><b>ポイント</b>：速さは中心で最大・両端で $0$、加速度の大きさは中心で $0$・両端で最大。"},
 {"lv": "A", "tag": "ばね振り子の周期",
  "q": r"ばね定数 $10\,\mathrm{N/m}$ の軽いばねに質量 $0.40\,\mathrm{kg}$ のおもりをつけ、なめらかな水平面上で単振動させる。$\pi=3.14$ とする。<br>(1) 周期を求めよ。<br>(2) おもりの質量を4倍にすると、周期は何倍になるか。<br>(3) 同じばねとおもりを天井からつるして鉛直方向に単振動させると、周期はどうなるか。",
  "a": r"(1) $1.3\,\mathrm{s}$　(2) 2倍　(3) 変わらない（$1.3\,\mathrm{s}$）",
  "s": r"(1) $T=2\pi\sqrt{\frac mk}=2\times3.14\times\sqrt{\frac{0.40}{10}}=6.28\times0.20\fallingdotseq1.3\,\mathrm{s}$。<br>(2) $T\propto\sqrt m$ なので $\sqrt4=2$ 倍。<br>(3) 鉛直につるすと振動の中心がつりあいの位置にずれるだけで、復元力は $-kx$（$x$ はつりあいの位置からの変位）のまま。周期は同じ。<br><b>ポイント</b>：ばね振り子の周期は $m$ と $k$ だけで決まり、振幅や重力によらない。"},
 {"lv": "A", "tag": "単振り子",
  "q": r"$\pi=3.14$ とする。<br>(1) 周期が $2.0\,\mathrm{s}$ の単振り子の長さを求めよ。<br>(2) 糸の長さを4倍にすると、周期は何倍になるか。<br>(3) 重力加速度の大きさが地球の $\frac16$ である月面で、(1) の振り子の周期を求めよ。<br>(4) 単振り子の周期の式 $T=2\pi\sqrt{\frac lg}$ が成り立つのは、どのようなときか。",
  "a": r"(1) $0.99\,\mathrm{m}$　(2) 2倍　(3) $4.9\,\mathrm{s}$　(4) 振れの角が十分小さいとき",
  "s": r"(1) $l=\frac{gT^2}{4\pi^2}=\frac{9.8\times2.0^2}{4\times3.14^2}\fallingdotseq0.99\,\mathrm{m}$。<br>(2) $T\propto\sqrt l$ なので2倍。<br>(3) $T\propto\frac{1}{\sqrt g}$ なので $\sqrt6$ 倍：$2.0\times\sqrt6\fallingdotseq4.9\,\mathrm{s}$。<br>(4) 振れの角 $\theta$ が小さく、$\sin\theta\fallingdotseq\theta$ とみなせて、復元力が変位に比例するとき。<br><b>ポイント</b>：単振り子の周期はおもりの質量にも振幅にもよらない（振れが小さいとき）。"},
 {"lv": "A", "tag": "単振動のエネルギー",
  "q": r"なめらかな水平面上で、ばね定数 $50\,\mathrm{N/m}$ のばねにつけた質量 $0.50\,\mathrm{kg}$ の物体が、振幅 $0.10\,\mathrm{m}$ で単振動している。<br>(1) 振動のエネルギー（力学的エネルギー）を求めよ。<br>(2) 速さの最大値を求めよ。<br>(3) 変位が $0.050\,\mathrm{m}$ のときの速さを求めよ。<br>(4) 運動エネルギーと弾性エネルギーが等しくなる変位を求めよ。",
  "a": r"(1) $0.25\,\mathrm{J}$　(2) $1.0\,\mathrm{m/s}$　(3) $0.87\,\mathrm{m/s}$　(4) $\pm7.1\times10^{-2}\,\mathrm{m}$",
  "s": r"(1) 端（速さ $0$）で考えて $E=\frac12kA^2=\frac12\times50\times0.10^2=0.25\,\mathrm{J}$。<br>(2) 中心で $\frac12mv^2=E$ となるので $v=\sqrt{\frac{2\times0.25}{0.50}}=1.0\,\mathrm{m/s}$。<br>(3) $\frac12mv^2=\frac12k(A^2-x^2)$ より $v=\sqrt{\frac{50}{0.50}\times(0.010-0.0025)}=\sqrt{0.75}\fallingdotseq0.87\,\mathrm{m/s}$。<br>(4) $\frac12kx^2=\frac12E$ より $x^2=\frac{A^2}{2}$、$x=\pm\frac{A}{\sqrt2}\fallingdotseq\pm0.071\,\mathrm{m}$。<br><b>ポイント</b>：単振動では $\frac12mv^2+\frac12kx^2=\frac12kA^2$ が一定。"},
 {"lv": "B", "tag": "鉛直ばね振り子",
  "q": r"ばね定数 $20\,\mathrm{N/m}$ の軽いばねの上端を天井に固定し、下端に質量 $0.20\,\mathrm{kg}$ のおもりをつけた。ばねが自然長になる位置でおもりを支え、静かに放した。$\pi=3.14$ とする。<br>(1) つりあいの位置でのばねの伸びを求めよ。<br>(2) おもりの振動の中心と振幅を答えよ。<br>(3) 周期を求めよ。<br>(4) 速さの最大値を求めよ。<br>(5) 最下点での加速度の大きさと向きを求めよ。",
  "a": r"(1) $9.8\times10^{-2}\,\mathrm{m}$　(2) 中心はつりあいの位置、振幅 $9.8\times10^{-2}\,\mathrm{m}$　(3) $0.63\,\mathrm{s}$　(4) $0.98\,\mathrm{m/s}$　(5) $9.8\,\mathrm{m/s^2}$、上向き",
  "s": r"(1) $kx_0=mg$ より $x_0=\frac{0.20\times9.8}{20}=0.098\,\mathrm{m}$。<br>(2) つりあいの位置から下向きに $x$ ずれると、合力は $mg-k(x_0+x)=-kx$。よってつりあいの位置を中心とする単振動。自然長の位置（速さ $0$）は振動の端なので、振幅は $x_0=0.098\,\mathrm{m}$。<br>(3) $T=2\pi\sqrt{\frac{0.20}{20}}=6.28\times0.10\fallingdotseq0.63\,\mathrm{s}$。<br>(4) $\omega=\sqrt{\frac km}=10\,\mathrm{rad/s}$、$v_{\max}=A\omega=0.098\times10=0.98\,\mathrm{m/s}$。<br>(5) 端での加速度の大きさは $A\omega^2=0.098\times100=9.8\,\mathrm{m/s^2}$、向きは中心向き（上向き）。最上点（自然長）で下向きに $g$ なので、対称性からも最下点で上向きに $g$。<br><b>ポイント</b>：鉛直のばね振り子は、つりあいの位置を原点にとれば水平の場合と同じ式になる。"},
 {"lv": "B", "tag": "2本のばね",
  "q": r"なめらかな水平面上で、質量 $m$ の物体の左右に、ばね定数 $k_1,\ k_2$ の軽いばねをつなぎ、それぞれの他端を壁に固定した。物体がつりあいの位置にあるとき、2本のばねはどちらも自然長であった。<br>(1) 物体がつりあいの位置から右に $x$ だけずれたとき、物体にはたらく合力を求めよ（右向きを正）。<br>(2) 物体の単振動の周期を求めよ。<br>(3) 同じ2本のばねを直列につないで1本のばねとし、一端を壁に固定して他端に同じ物体をつけて振動させるときの周期を求めよ。<br>(4) $k_1=k_2=k$ のとき、(2) と (3) の周期の比を求めよ。",
  "a": r"(1) $-(k_1+k_2)x$　(2) $2\pi\sqrt{\frac{m}{k_1+k_2}}$　(3) $2\pi\sqrt{\frac{m(k_1+k_2)}{k_1k_2}}$　(4) $1:2$",
  "s": r"(1) 左のばねは $x$ 伸びて左向きに $k_1x$、右のばねは $x$ 縮んで左向きに $k_2x$ で押す。合力 $-(k_1+k_2)x$。<br>(2) $K=k_1+k_2$ として $T=2\pi\sqrt{\frac{m}{k_1+k_2}}$。<br>(3) 直列では2本に同じ大きさの力 $F$ がかかり、伸びの和は $\frac F{k_1}+\frac F{k_2}$。合成ばね定数は $K'=\frac{k_1k_2}{k_1+k_2}$。$T'=2\pi\sqrt{\frac{m(k_1+k_2)}{k_1k_2}}$。<br>(4) $T=2\pi\sqrt{\frac m{2k}}$、$T'=2\pi\sqrt{\frac{2m}{k}}$ より $T:T'=1:2$。<br><b>ポイント</b>：両側からばねで挟むと（並列と同じく）ばね定数は和、直列では逆数の和の逆数。"},
 {"lv": "B", "tag": "位相と時刻",
  "q": r"単振動 $x=A\sin(\omega t+\phi_0)$（$A>0$、$0\leqq\phi_0<2\pi$）をする物体が、時刻 $t=0$ に $x=\frac A2$ の位置を負の向きに運動していた。周期を $T$ とする。<br>(1) $\phi_0$ を求めよ。<br>(2) $t=0$ の後、初めて $x=-A$ となる時刻を求めよ。<br>(3) $t=0$ の後、初めて速度が正の向きに最大となる時刻を求めよ。<br>(4) $t=0$ から初めて $x=-A$ となるまでに物体が動いた道のりを求めよ。",
  "a": r"(1) $\frac56\pi$　(2) $\frac T3$　(3) $\frac{7}{12}T$　(4) $\frac32A$",
  "s": r"速度は $v=A\omega\cos(\omega t+\phi_0)$。<br>(1) $\sin\phi_0=\frac12$ より $\phi_0=\frac\pi6$ または $\frac56\pi$。$v<0$ すなわち $\cos\phi_0<0$ なので $\phi_0=\frac56\pi$。<br>(2) $x=-A$ となるのは位相が $\frac32\pi$ のとき。位相の増加は $\frac32\pi-\frac56\pi=\frac23\pi$ で、$t=\frac{2\pi/3}{2\pi}T=\frac T3$。<br>(3) 速度が正で最大になるのは位相が $2\pi$ のとき（中心を正の向きに通過）。増加は $\frac76\pi$ で $t=\frac7{12}T$。<br>(4) $x=\frac A2$ から負の向きに $x=-A$ まで動くので、道のりは $\frac A2+A=\frac32A$。<br><b>ポイント</b>：等速円運動の正射影として考えると、位相＝円周上の角。位相の差を $2\pi$ で割って $T$ をかければ時間になる。"},
 {"lv": "B", "tag": "加速度系の単振り子",
  "q": r"長さ $l$ の単振り子を乗り物の天井からつるし、乗り物に対して小さく振動させる。重力加速度の大きさを $g$ とする。<br>(1) 鉛直上向きに一定の加速度 $a$ で上昇するエレベーター内での周期を求めよ。<br>(2) 水平方向に一定の加速度 $a$ で走る電車内での周期を求めよ。また、振動の中心で糸が鉛直となす角を $\alpha$ として $\tan\alpha$ を求めよ。<br>(3) $l=1.0\,\mathrm{m}$、$a=\frac34g$ のとき、(2) の周期を求めよ（$g=9.8\,\mathrm{m/s^2}$、$\pi=3.14$）。",
  "a": r"(1) $2\pi\sqrt{\frac{l}{g+a}}$　(2) $2\pi\sqrt{\frac{l}{\sqrt{g^2+a^2}}}$、$\tan\alpha=\frac ag$　(3) $1.8\,\mathrm{s}$",
  "s": r"乗り物の中では、重力と慣性力の合力を「見かけの重力」$mg'$ とみなすと、$g$ を $g'$ におきかえた単振り子になる。<br>(1) 慣性力は下向き $ma$ なので $g'=g+a$。$T=2\pi\sqrt{\frac{l}{g+a}}$。<br>(2) 慣性力は水平に $ma$（加速度と逆向き）。$g'=\sqrt{g^2+a^2}$、見かけの重力の向きは鉛直から $\tan\alpha=\frac ag$ だけ傾いていて、振動の中心はこの向き。$T=2\pi\sqrt{\frac{l}{\sqrt{g^2+a^2}}}$。<br>(3) $g'=\frac54g=12.25\,\mathrm{m/s^2}$。$T=6.28\times\sqrt{\frac{1.0}{12.25}}=\frac{6.28}{3.5}\fallingdotseq1.8\,\mathrm{s}$。<br><b>ポイント</b>：加速する乗り物の中では「見かけの重力加速度」$\vec g'=\vec g-\vec a$ を使う。"},
 {"lv": "B", "tag": "衝突後の単振動",
  "q": r"なめらかな水平面上で、ばね定数 $k$ の軽いばねの一端を壁に固定し、他端に質量 $m$ の物体 A をつけて静止させておく。ばねの向きに沿って質量 $m$ の物体 B が速さ $v_0$ で A に衝突し、A と一体となった。<br>(1) 衝突直後の速さを求めよ。<br>(2) その後の単振動の周期と振幅を求めよ。<br>(3) 衝突してから、ばねが初めて最も縮むまでの時間を求めよ。<br>(4) 衝突で失われた運動エネルギーを求めよ。",
  "a": r"(1) $\frac{v_0}{2}$　(2) 周期 $2\pi\sqrt{\frac{2m}{k}}$、振幅 $v_0\sqrt{\frac{m}{2k}}$　(3) $\frac\pi2\sqrt{\frac{2m}{k}}$　(4) $\frac14mv_0^2$",
  "s": r"(1) 衝突は一瞬なので、その間のばねの力積は無視できる。運動量保存 $mv_0=2mV$ より $V=\frac{v_0}{2}$。<br>(2) 質量 $2m$ のばね振り子：$T=2\pi\sqrt{\frac{2m}{k}}$。衝突した位置（自然長の位置）が振動の中心で、そこでの速さ $V$ が最大の速さ。$V=A\omega$、$\omega=\sqrt{\frac{k}{2m}}$ より $A=\frac{v_0}{2}\sqrt{\frac{2m}{k}}=v_0\sqrt{\frac{m}{2k}}$。<br>(3) 中心から端まで $\frac T4=\frac\pi2\sqrt{\frac{2m}{k}}$。<br>(4) $\frac12mv_0^2-\frac12(2m)\left(\frac{v_0}{2}\right)^2=\frac14mv_0^2$。<br><b>ポイント</b>：「衝突（運動量保存）」と「その後の単振動（エネルギー保存）」は段階を分けて考える。衝突の瞬間をまたいでエネルギー保存は使えない。"},
 {"lv": "C", "tag": "板から離れる条件",
  "q": r"鉛直に立てたばね定数 $k$ の軽いばねの下端を床に固定し、上端に質量 $M$ の板を取りつける。板の上に質量 $m$ の小物体をのせ、つりあいの位置から距離 $d$ だけ押し下げて静かに放した。重力加速度の大きさを $g$ とする。<br>(1) 小物体が板から離れずに運動するとき、振動の周期を求めよ。<br>(2) つりあいの位置からの変位を $y$（上向きを正）とするとき、小物体が板から受ける垂直抗力の大きさ $N$ を $y$ の式で表せ。<br>(3) 小物体が板から離れないための $d$ の条件を求めよ。<br>(4) $d=\frac{2(M+m)g}{k}$ のとき、小物体が板から離れる位置（ばねの状態）と、その瞬間の速さを求めよ。また、離れた後、小物体はその位置から最大でどれだけ上昇するか。",
  "a": r"(1) $2\pi\sqrt{\frac{M+m}{k}}$　(2) $N=m\left(g-\frac{k}{M+m}y\right)$　(3) $d\leqq\frac{(M+m)g}{k}$　(4) ばねが自然長の位置、速さ $g\sqrt{\frac{3(M+m)}{k}}$、上昇 $\frac{3(M+m)g}{2k}$",
  "s": r"(1) 板と小物体を一体とみると質量 $M+m$ のばね振り子で、つりあいの位置を中心とする単振動。$T=2\pi\sqrt{\frac{M+m}{k}}$。<br>(2) 加速度は $a=-\omega^2y=-\frac{k}{M+m}y$。小物体の運動方程式 $ma=N-mg$ より $N=m\left(g-\frac{k}{M+m}y\right)$。<br>(3) $N$ は最高点 $y=d$ で最小。$N\geqq0$ より $d\leqq\frac{(M+m)g}{k}$。<br>(4) $N=0$ となるのは $y=\frac{(M+m)g}{k}$ のとき。つりあいの位置ではばねは $\frac{(M+m)g}{k}$ 縮んでいるので、この位置はばねが自然長の位置。速さは $v^2=\omega^2(d^2-y^2)=\frac{k}{M+m}\left(4-1\right)\left(\frac{(M+m)g}{k}\right)^2=\frac{3(M+m)g^2}{k}$。離れた後は鉛直投げ上げで、上昇する高さは $\frac{v^2}{2g}=\frac{3(M+m)g}{2k}$。<br><b>ポイント</b>：離れる瞬間は小物体の加速度が $-g$（板の上にのっているだけでは、下向き $g$ より大きな加速度は出せない）。それはばねが自然長のときで、質量によらない。"},
 {"lv": "C", "tag": "2物体の振動と重心",
  "q": r"なめらかな水平面上で、質量 $m_1$ の物体 A と質量 $m_2$ の物体 B を、ばね定数 $k$ の軽いばねでつなぐ。ばねを自然長から $d$ だけ縮めた状態で、A と B を同時に静かに放した。<br>(1) A と B の重心は動かないことを説明せよ。<br>(2) ばねのうち、A から重心までの部分の長さは、つねにばね全体の長さの何倍か。また、この部分を1本のばねとみなしたときのばね定数を求めよ（ばねは一様とする）。<br>(3) A の振動の周期を求め、B の周期も同じになることを確かめよ。<br>(4) A と B の振幅をそれぞれ求めよ。<br>(5) $m_1=1.0\,\mathrm{kg}$、$m_2=3.0\,\mathrm{kg}$、$k=12\,\mathrm{N/m}$ のとき、周期を求めよ（$\pi=3.14$）。",
  "a": r"(1) 解説参照　(2) $\frac{m_2}{m_1+m_2}$ 倍、$\frac{(m_1+m_2)k}{m_2}$　(3) $2\pi\sqrt{\frac{m_1m_2}{(m_1+m_2)k}}$　(4) A：$\frac{m_2}{m_1+m_2}d$、B：$\frac{m_1}{m_1+m_2}d$　(5) $1.6\,\mathrm{s}$",
  "s": r"(1) 水平方向の外力がないので、A, B の運動量の和は一定で、初めは $0$。重心の速度は $\frac{m_1v_1+m_2v_2}{m_1+m_2}=0$ のままなので、重心は静止している。<br>(2) A, B の位置を $x_1,\ x_2$ とすると、重心は $x_G=\frac{m_1x_1+m_2x_2}{m_1+m_2}=x_1+\frac{m_2}{m_1+m_2}(x_2-x_1)$。ばねの伸び縮みは一様なので、A から全長の $\frac{m_2}{m_1+m_2}$ の点がつねに重心と一致する。ばねの長さを $\frac{m_2}{m_1+m_2}$ 倍に切ると、同じ力での伸びもその倍になるので、ばね定数は $k_1=\frac{(m_1+m_2)k}{m_2}$。<br>(3) A は、固定点（重心）につながれたばね定数 $k_1$ のばね振り子として運動する。$T=2\pi\sqrt{\frac{m_1}{k_1}}=2\pi\sqrt{\frac{m_1m_2}{(m_1+m_2)k}}$。B も同様に $k_2=\frac{(m_1+m_2)k}{m_1}$ として $2\pi\sqrt{\frac{m_2}{k_2}}$ で同じ値。<br>(4) 初めの縮み $d$ のうち、A 側の部分は $\frac{m_2}{m_1+m_2}d$ 縮んでいる。A は静かに放されたので、これが A の振幅。B は $\frac{m_1}{m_1+m_2}d$。<br>(5) $\frac{m_1m_2}{m_1+m_2}=0.75\,\mathrm{kg}$。$T=6.28\times\sqrt{\frac{0.75}{12}}=6.28\times0.25\fallingdotseq1.6\,\mathrm{s}$。<br><b>ポイント</b>：外力のない2物体系は「重心は等速（ここでは静止）＋重心に対する振動」に分けられる。$\mu=\frac{m_1m_2}{m_1+m_2}$ を換算質量という。"},
]}}


def verify():
    g = Rational(98, 10)
    PI = Rational(314, 100)
    t = symbols("t")
    # 6-1
    x = Rational(1, 10) * sin(pi * t)
    assert 2 * pi / pi == 2
    _near(Rational(1, 10) * PI, 0.31); _near(Rational(1, 10) * PI ** 2, 0.99)
    assert x.subs(t, Rational(1, 6)) == Rational(1, 20)
    _eq(diff(x, t, 2), -pi ** 2 * x)
    # 6-2
    _near(2 * PI * sqrt(Rational(4, 10) / 10), 1.3)
    # 6-3
    _near(g * 4 / (4 * PI ** 2), 0.99); _near(2 * sqrt(6), 4.9)
    # 6-4
    k, m, A = 50, Rational(1, 2), Rational(1, 10)
    E = Rational(1, 2) * k * A ** 2
    assert E == Rational(1, 4) and sqrt(2 * E / m) == 1
    _near(sqrt(Rational(k) / m * (A ** 2 - Rational(1, 20) ** 2)), 0.87)
    _near(A / sqrt(2), 7.1e-2)
    # 6-5
    k, m = 20, Rational(2, 10)
    x0 = m * g / k; _near(x0, 9.8e-2)
    w = sqrt(k / m); assert w == 10
    _near(2 * PI / w, 0.63); _near(x0 * w, 0.98); _near(x0 * w ** 2, 9.8)
    # 6-6
    k1, k2, mm = symbols("k1 k2 m", positive=True)
    Ks = k1 * k2 / (k1 + k2)
    _eq(1 / Ks, 1 / k1 + 1 / k2)
    kk = symbols("k", positive=True)
    T1 = 2 * pi * sqrt(mm / (k1 + k2)); T2 = 2 * pi * sqrt(mm / Ks)
    _eq((T1 / T2).subs({k1: kk, k2: kk}), Rational(1, 2))
    # 6-7
    phis = solve(Eq(sin(symbols("p")), Rational(1, 2)), symbols("p"))
    p0 = [p for p in phis if cos(p) < 0][0]
    assert p0 == 5 * pi / 6
    assert (3 * pi / 2 - p0) / (2 * pi) == Rational(1, 3)
    assert (2 * pi - p0) / (2 * pi) == Rational(7, 12)
    # 6-8
    l, a, gg = symbols("l a g", positive=True)
    ge = sqrt(gg ** 2 + (3 * gg / 4) ** 2)
    _eq(ge, 5 * gg / 4)
    _near(2 * PI * sqrt(1 / (Rational(5, 4) * g)), 1.8)
    # 6-9
    v0 = symbols("v0", positive=True)
    V = mm * v0 / (2 * mm)
    Amp = V / sqrt(kk / (2 * mm))
    _eq(Amp, v0 * sqrt(mm / (2 * kk)))
    _eq(Rational(1, 2) * mm * v0 ** 2 - Rational(1, 2) * 2 * mm * V ** 2, mm * v0 ** 2 / 4)
    # 6-10
    M, y, N = symbols("M y N")
    om2 = kk / (M + mm)
    Nn = solve(Eq(mm * (-om2 * y), N - mm * gg), N)[0]
    _eq(Nn, mm * (gg - kk * y / (M + mm)))
    ysep = solve(Nn, y)[0]
    _eq(ysep, (M + mm) * gg / kk)
    d = 2 * (M + mm) * gg / kk
    v2 = om2 * (d ** 2 - ysep ** 2)
    _eq(v2, 3 * (M + mm) * gg ** 2 / kk)
    _eq(v2 / (2 * gg), 3 * (M + mm) * gg / (2 * kk))
    # 6-11 2物体の振動：運動方程式から相対座標の角振動数を確認
    m1, m2 = symbols("m1 m2", positive=True)
    kA = (m1 + m2) * kk / m2
    TA = 2 * pi * sqrt(m1 / kA); TB = 2 * pi * sqrt(m2 / ((m1 + m2) * kk / m1))
    _eq(TA, TB); _eq(TA, 2 * pi * sqrt(m1 * m2 / ((m1 + m2) * kk)))
    # 相対変位 s=x2-x1-L の方程式 s'' = -k(1/m1+1/m2) s と一致
    _eq((2 * pi / TA) ** 2, kk * (1 / m1 + 1 / m2))
    _near(2 * PI * sqrt(Rational(3, 4) / 12), 1.6)
