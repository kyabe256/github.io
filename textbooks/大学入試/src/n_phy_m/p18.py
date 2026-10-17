"""問題集 第18章 電子と光・原子の構造。CH に問題、verify() で答えを sympy で検算する。"""
from sympy import *

CONST = r"必要なら、プランク定数 $h=6.63\times10^{-34}\,\mathrm{J\cdot s}$、真空中の光の速さ $c=3.00\times10^8\,\mathrm{m/s}$、電気素量 $e=1.60\times10^{-19}\,\mathrm C$、電子の質量 $m=9.1\times10^{-31}\,\mathrm{kg}$ を用いよ。"

CH = {18: {
"goal": r"光の粒子性（光子・光電効果・X 線・コンプトン効果）と電子の波動性（物質波）を、エネルギー保存と運動量保存の式で扱う。ボーアの量子条件から水素原子のエネルギー準位とスペクトルを導けるようにする。<br>" + CONST,
"items": [
 {"lv": "A", "tag": "光子", "q": r"波長 $500\,\mathrm{nm}$ の光について答えよ。<br>(1) 光子 1 個のエネルギーを、J と eV の単位で求めよ。<br>(2) 光子 1 個の運動量の大きさを求めよ。<br>(3) この光を出力 $1.0\,\mathrm{mW}$ で出すレーザーは、1 s あたり何個の光子を出しているか。",
  "a": r"(1) $3.98\times10^{-19}\,\mathrm J$、$2.49\,\mathrm{eV}$　(2) $1.33\times10^{-27}\,\mathrm{kg\cdot m/s}$　(3) $2.5\times10^{15}$ 個",
  "s": r"(1) $E=\dfrac{hc}\lambda=\dfrac{6.63\times10^{-34}\times3.00\times10^8}{500\times10^{-9}}\fallingdotseq3.98\times10^{-19}\,\mathrm J$。$1\,\mathrm{eV}=1.60\times10^{-19}\,\mathrm J$ なので $\fallingdotseq2.49\,\mathrm{eV}$。<br>(2) $p=\dfrac h\lambda=\dfrac{6.63\times10^{-34}}{500\times10^{-9}}\fallingdotseq1.33\times10^{-27}\,\mathrm{kg\cdot m/s}$。<br>(3) $\dfrac{1.0\times10^{-3}}{3.98\times10^{-19}}\fallingdotseq2.5\times10^{15}$ 個。<br><b>ポイント</b>：光子 1 個のエネルギー $E=h\nu=\dfrac{hc}\lambda$、運動量 $p=\dfrac h\lambda=\dfrac Ec$。eV と J の換算は電気素量を掛け割りするだけ。"},
 {"lv": "A", "tag": "光電効果", "q": r"仕事関数が $2.0\,\mathrm{eV}$ の金属の表面に、波長 $400\,\mathrm{nm}$ の光を当てる。<br>(1) 飛び出す光電子の運動エネルギーの最大値を eV の単位で求めよ。<br>(2) 阻止電圧を求めよ。<br>(3) 光電子が飛び出す光の波長の上限（限界波長）を求めよ。<br>(4) 光の波長を変えずに強さを 2 倍にすると、(1) の値と、1 s あたりに飛び出す光電子の数はそれぞれどうなるか。",
  "a": r"(1) $1.1\,\mathrm{eV}$　(2) $1.1\,\mathrm V$　(3) $6.2\times10^2\,\mathrm{nm}$　(4) 最大の運動エネルギーは変わらない、光電子の数は 2 倍",
  "s": r"(1) 光子のエネルギーは $\dfrac{hc}\lambda=\dfrac{1.989\times10^{-25}}{4.00\times10^{-7}}\fallingdotseq4.97\times10^{-19}\,\mathrm J\fallingdotseq3.11\,\mathrm{eV}$。$K_\mathrm{max}=h\nu-W=3.11-2.0\fallingdotseq1.1\,\mathrm{eV}$。<br>(2) $eV_0=K_\mathrm{max}$ より $V_0\fallingdotseq1.1\,\mathrm V$。<br>(3) $\dfrac{hc}{\lambda_0}=W$ より $\lambda_0=\dfrac{1.989\times10^{-25}}{2.0\times1.60\times10^{-19}}\fallingdotseq6.2\times10^{-7}\,\mathrm m$。<br>(4) 光子 1 個のエネルギーは波長で決まるので $K_\mathrm{max}$ は変わらない。光が強いと光子の数が多く、光電子の数が 2 倍になる。<br><b>ポイント</b>：$K_\mathrm{max}=h\nu-W$。光の強さは「光子の数」、振動数は「光子 1 個のエネルギー」を決める。"},
 {"lv": "A", "tag": "物質波", "q": r"(1) 静止していた電子を $100\,\mathrm V$ の電圧で加速した。電子の速さと、ド・ブロイ波長を求めよ。<br>(2) 質量 $0.15\,\mathrm{kg}$ のボールが速さ $40\,\mathrm{m/s}$ で飛んでいるときのド・ブロイ波長を求めよ。ボールの波としての性質がふつう観測されないのはなぜか。",
  "a": r"(1) $5.9\times10^6\,\mathrm{m/s}$、$1.2\times10^{-10}\,\mathrm m$　(2) $1.1\times10^{-34}\,\mathrm m$。波長が原子の大きさよりはるかに小さく、回折や干渉が現れないから",
  "s": r"(1) $\dfrac12mv^2=eV$ より $v=\sqrt{\dfrac{2eV}m}=\sqrt{\dfrac{2\times1.60\times10^{-19}\times100}{9.1\times10^{-31}}}\fallingdotseq5.9\times10^6\,\mathrm{m/s}$。$\lambda=\dfrac h{mv}=\dfrac h{\sqrt{2meV}}\fallingdotseq1.2\times10^{-10}\,\mathrm m$（X 線と同程度で、結晶で回折する）。<br>(2) $\lambda=\dfrac{6.63\times10^{-34}}{0.15\times40}\fallingdotseq1.1\times10^{-34}\,\mathrm m$。回折が目立つのは、波長と同程度の大きさのすき間や障害物があるときだけである。<br><b>ポイント</b>：物質波の波長 $\lambda=\dfrac hp$。電圧 $V$ で加速した電子なら $p=\sqrt{2meV}$。"},
 {"lv": "A", "tag": "水素原子のエネルギー準位", "q": r"水素原子のエネルギー準位は $E_n=-\dfrac{13.6}{n^2}\,\mathrm{eV}$（$n=1,2,3,\cdots$）で表される。<br>(1) $n=3$ から $n=2$ の状態へ移るときに放出される光子のエネルギーと、光の波長を求めよ。<br>(2) 基底状態の水素原子を電離するのに必要な最小のエネルギーを求めよ。<br>(3) $n=2$ から $n=1$ へ移るときに放出される光の波長を求め、どの電磁波の領域にあるか答えよ。",
  "a": r"(1) $1.89\,\mathrm{eV}$、$6.58\times10^{-7}\,\mathrm m$　(2) $13.6\,\mathrm{eV}$　(3) $1.22\times10^{-7}\,\mathrm m$、紫外線",
  "s": r"(1) $E_3-E_2=13.6\left(\dfrac14-\dfrac19\right)\fallingdotseq1.89\,\mathrm{eV}$。$\lambda=\dfrac{hc}{\Delta E}=\dfrac{1.989\times10^{-25}}{1.89\times1.60\times10^{-19}}\fallingdotseq6.58\times10^{-7}\,\mathrm m$（赤い可視光）。<br>(2) $n=1$ から $n\to\infty$（$E=0$）まで上げればよいので $13.6\,\mathrm{eV}$。<br>(3) $\Delta E=13.6\times\dfrac34=10.2\,\mathrm{eV}$、$\lambda=\dfrac{1.989\times10^{-25}}{10.2\times1.60\times10^{-19}}\fallingdotseq1.22\times10^{-7}\,\mathrm m$。可視光（約 $3.8\times10^{-7}$〜$7.7\times10^{-7}\,\mathrm m$）より短く、紫外線。<br><b>ポイント</b>：振動数条件 $h\nu=E_n-E_{n'}$。エネルギーを eV で計算し、最後に $\lambda=\dfrac{hc}{\Delta E}$ で波長に直す。"},
 {"lv": "B", "tag": "電気素量の測定", "q": r"ミリカンの実験のように、小さな油滴の運動を観察する。質量 $M$ の油滴が速さ $v$ で動くとき、空気から大きさ $kv$（$k$ は定数）の抵抗力を受ける。重力加速度の大きさを $g$ とする。<br>(1) 電場がないとき、油滴は一定の速さ $v_1$ で落下した。$M$ を $k,\ v_1,\ g$ で表せ。<br>(2) 鉛直上向きに強さ $E$ の電場をかけると、この油滴（電気量 $q\gt0$）は一定の速さ $v_2$ で上昇した。$q$ を $k,\ v_1,\ v_2,\ E$ で表せ。<br>(3) いくつかの油滴で $q$ を測定すると、$3.21,\ 4.80,\ 8.02,\ 6.39$（単位 $10^{-19}\,\mathrm C$）であった。電気素量を有効数字 3 桁で推定せよ。",
  "a": r"(1) $M=\dfrac{kv_1}g$　(2) $q=\dfrac{k(v_1+v_2)}E$　(3) $1.60\times10^{-19}\,\mathrm C$",
  "s": r"(1) 一定の速さなので力がつりあう：$Mg=kv_1$、$M=\dfrac{kv_1}g$。<br>(2) 上昇中は抵抗力が下向き：$qE=Mg+kv_2=k(v_1+v_2)$、$q=\dfrac{k(v_1+v_2)}E$。$M$ を直接測らなくてよいのがこの方法の利点。<br>(3) 差をとると $4.80-3.21=1.59$、$6.39-4.80=1.59$、$8.02-6.39=1.63$ で、どれも約 $1.6$ の整数倍。各値は $1.6$ のおよそ $2,\ 3,\ 5,\ 4$ 倍なので、$e=\dfrac{3.21+4.80+8.02+6.39}{2+3+5+4}=\dfrac{22.42}{14}\fallingdotseq1.60\times10^{-19}\,\mathrm C$。<br><b>ポイント</b>：終端速度では「重力・電気力・抵抗力」がつりあう。測定値がある値の整数倍になっていることから電荷の最小単位（電気素量）を決める。"},
 {"lv": "B", "tag": "光電効果の実験", "q": r"ある金属に振動数 $\nu$ の光を当てて阻止電圧 $V_0$ を測ると、$\nu=6.0\times10^{14}\,\mathrm{Hz}$ のとき $V_0=0.50\,\mathrm V$、$\nu=8.0\times10^{14}\,\mathrm{Hz}$ のとき $V_0=1.33\,\mathrm V$ であった。<br>(1) $eV_0$ と $\nu$ の関係が直線になることを用いて、プランク定数を求めよ。<br>(2) この金属の仕事関数を eV の単位で求めよ。<br>(3) 限界振動数を求めよ。<br>(4) 仕事関数がより大きい金属で同じ実験をすると、$eV_0$-$\nu$ グラフの直線はどう変わるか。",
  "a": r"(1) $6.64\times10^{-34}\,\mathrm{J\cdot s}$　(2) $1.99\,\mathrm{eV}$　(3) $4.8\times10^{14}\,\mathrm{Hz}$　(4) 傾きは同じで、右（振動数の大きい側）へ平行に移る",
  "s": r"(1) $eV_0=h\nu-W$ なので、直線の傾きが $h$。$h=\dfrac{e(1.33-0.50)}{(8.0-6.0)\times10^{14}}=\dfrac{1.60\times10^{-19}\times0.83}{2.0\times10^{14}}=6.64\times10^{-34}\,\mathrm{J\cdot s}$。<br>(2) $W=h\nu-eV_0=6.64\times10^{-34}\times6.0\times10^{14}-1.60\times10^{-19}\times0.50\fallingdotseq3.18\times10^{-19}\,\mathrm J\fallingdotseq1.99\,\mathrm{eV}$。<br>(3) $\nu_0=\dfrac Wh=\dfrac{3.18\times10^{-19}}{6.64\times10^{-34}}\fallingdotseq4.8\times10^{14}\,\mathrm{Hz}$（直線と $\nu$ 軸の交点）。<br>(4) 傾き $h$ は金属によらない。$W$ が大きいと縦軸の切片 $-W$ が下がり、直線は右へ平行移動する（限界振動数が大きくなる）。<br><b>ポイント</b>：$eV_0$-$\nu$ グラフは「傾き $=h$、$\nu$ 切片 $=\nu_0$、縦軸切片 $=-W$」。"},
 {"lv": "B", "tag": "X 線", "q": r"(1) X 線管に $40\,\mathrm{kV}$ の電圧をかけて電子を加速し、陽極に当てた。発生する X 線の最短波長を求めよ。<br>(2) 加速電圧を 2 倍にすると、最短波長と、陽極の金属に特有の固有 X 線（特性 X 線）の波長はそれぞれどうなるか。<br>(3) 波長 $1.0\times10^{-10}\,\mathrm m$ の X 線を、格子面の間隔 $d=2.0\times10^{-10}\,\mathrm m$ の結晶に当てる。X 線と格子面のなす角を $\theta$ とすると、反射 X 線が強め合う条件は $2d\sin\theta=n\lambda$（$n=1,2,\cdots$）である。$n=1$ のときの $\sin\theta$ を求めよ。また、強め合う反射が起こる $n$ は何通りあるか。",
  "a": r"(1) $3.1\times10^{-11}\,\mathrm m$　(2) 最短波長は $\dfrac12$ 倍、固有 X 線の波長は変わらない　(3) $\sin\theta=0.25$、3 通り（$n=1,2,3$）",
  "s": r"(1) 電子の運動エネルギー $eV$ がすべて 1 個の光子になるとき波長が最短：$eV=\dfrac{hc}{\lambda_\mathrm{min}}$。$\lambda_\mathrm{min}=\dfrac{1.989\times10^{-25}}{1.60\times10^{-19}\times4.0\times10^4}\fallingdotseq3.1\times10^{-11}\,\mathrm m$。<br>(2) $\lambda_\mathrm{min}\propto\dfrac1V$ なので $\dfrac12$ 倍。固有 X 線は陽極の原子の電子のエネルギー準位の差で決まるので、電圧によらない。<br>(3) $\sin\theta=\dfrac{n\lambda}{2d}=0.25n$。$\sin\theta\lt1$ より $n=1,2,3$ の 3 通り（$n=4$ は $\theta=90^\circ$ で、反射とはいえない）。<br><b>ポイント</b>：連続 X 線の最短波長は電圧だけで決まり、固有 X 線の波長は陽極の物質だけで決まる。ブラッグの条件の $\theta$ は「格子面となす角」。"},
 {"lv": "B", "tag": "コンプトン効果", "q": r"静止している電子に波長 $\lambda=5.00\times10^{-11}\,\mathrm m$ の X 線光子が当たり、入射方向と角 $\phi$ をなす向きに波長 $\lambda'$ の光子が散乱され、電子は入射方向と角 $\alpha$ をなす向きに速さ $v$ ではね飛ばされた。<br>(1) エネルギー保存の式と、入射方向・それに垂直な方向の運動量保存の式を書け。<br>(2) これらから $\lambda'-\lambda=\dfrac h{mc}(1-\cos\phi)$ が導かれる。$\dfrac h{mc}$ の値を求め、$\phi=90^\circ$ のときの $\lambda'$ を求めよ。<br>(3) (2) のとき、はね飛ばされた電子の運動エネルギーを求めよ。<br>(4) 波長の変化が最大になる散乱の向きと、そのときの波長の変化を求めよ。",
  "a": r"(1) 解説参照　(2) $2.43\times10^{-12}\,\mathrm m$、$5.24\times10^{-11}\,\mathrm m$　(3) $1.8\times10^{-16}\,\mathrm J$　(4) 真後ろ（$\phi=180^\circ$）、$4.86\times10^{-12}\,\mathrm m$",
  "s": r"(1) エネルギー：$\dfrac{hc}\lambda=\dfrac{hc}{\lambda'}+\dfrac12mv^2$。<br>入射方向：$\dfrac h\lambda=\dfrac h{\lambda'}\cos\phi+mv\cos\alpha$。垂直方向：$0=\dfrac h{\lambda'}\sin\phi-mv\sin\alpha$。<br>(2) $\dfrac h{mc}=\dfrac{6.63\times10^{-34}}{9.1\times10^{-31}\times3.00\times10^8}\fallingdotseq2.43\times10^{-12}\,\mathrm m$。$\phi=90^\circ$ で $\lambda'=5.00\times10^{-11}+0.243\times10^{-11}\fallingdotseq5.24\times10^{-11}\,\mathrm m$。<br>(3) $\dfrac12mv^2=hc\left(\dfrac1\lambda-\dfrac1{\lambda'}\right)=1.989\times10^{-25}\times\left(\dfrac1{5.00\times10^{-11}}-\dfrac1{5.243\times10^{-11}}\right)\fallingdotseq1.8\times10^{-16}\,\mathrm J$。<br>(4) $1-\cos\phi$ が最大の $\phi=180^\circ$ で $2\times2.43\times10^{-12}=4.86\times10^{-12}\,\mathrm m$。<br><b>ポイント</b>：コンプトン効果は「光子と電子の弾性衝突」。光子がエネルギーを失うと波長が長くなる。光子の運動量 $\dfrac h\lambda$ を使って運動量保存を立てることが、光の粒子性の証拠になった。"},
 {"lv": "B", "tag": "ボーアの原子模型", "q": r"水素原子で、電子（質量 $m$、電気量 $-e$）が陽子（電気量 $+e$）を中心に半径 $r$、速さ $v$ の等速円運動をしているとする。クーロンの法則の比例定数を $k$、プランク定数を $h$ とする。<br>(1) 電子の円運動の運動方程式を書け。<br>(2) ボーアの量子条件は「円周の長さが電子の物質波の波長の整数倍」である。これを式で書け。<br>(3) (1)(2) から、量子数 $n$ の軌道半径 $r_n$ を求めよ。<br>(4) 電子のエネルギー（運動エネルギーと静電気力の位置エネルギーの和）$E_n$ を求めよ。<br>(5) $k=9.0\times10^9\,\mathrm{N\cdot m^2/C^2}$ として、$r_1$ と $E_1$（eV の単位）の値を求めよ。",
  "a": r"(1) $m\dfrac{v^2}r=\dfrac{ke^2}{r^2}$　(2) $2\pi r=n\dfrac h{mv}$　(3) $r_n=\dfrac{h^2}{4\pi^2kme^2}n^2$　(4) $E_n=-\dfrac{2\pi^2k^2me^4}{h^2}\cdot\dfrac1{n^2}$　(5) $r_1=5.3\times10^{-11}\,\mathrm m$、$E_1=-13.6\,\mathrm{eV}$",
  "s": r"(1) 向心力はクーロン力：$m\dfrac{v^2}r=\dfrac{ke^2}{r^2}$。<br>(2) 物質波の波長は $\dfrac h{mv}$ なので $2\pi r=n\dfrac h{mv}$。<br>(3) (2) より $v=\dfrac{nh}{2\pi mr}$。(1) の $mv^2=\dfrac{ke^2}r$ に代入して $\dfrac{n^2h^2}{4\pi^2mr^2}=\dfrac{ke^2}r$、$r_n=\dfrac{h^2}{4\pi^2kme^2}n^2$。<br>(4) $\dfrac12mv^2=\dfrac{ke^2}{2r}$、位置エネルギー $-\dfrac{ke^2}r$ より $E=-\dfrac{ke^2}{2r}$。$r_n$ を代入して $E_n=-\dfrac{2\pi^2k^2me^4}{h^2n^2}$。<br>(5) $r_1=\dfrac{(6.63\times10^{-34})^2}{4\pi^2\times9.0\times10^9\times9.1\times10^{-31}\times(1.60\times10^{-19})^2}\fallingdotseq5.3\times10^{-11}\,\mathrm m$。$E_1=-\dfrac{ke^2}{2r_1}\fallingdotseq-2.17\times10^{-18}\,\mathrm J\fallingdotseq-13.6\,\mathrm{eV}$。<br><b>ポイント</b>：ボーア模型は「運動方程式」と「量子条件」の連立。エネルギーは $E=-\dfrac{ke^2}{2r}$（運動エネルギーは位置エネルギーの絶対値の半分）とまとめておくと計算が速い。"},
 {"lv": "C", "tag": "総合・水素のスペクトル", "q": r"水素原子のエネルギー準位を $E_n=-\dfrac{13.6}{n^2}\,\mathrm{eV}$ とする。<br>(1) $n$ の準位から $n'\ (\lt n)$ の準位へ移るときに出る光の波長 $\lambda$ が $\dfrac1\lambda=R\left(\dfrac1{n'^2}-\dfrac1{n^2}\right)$ と表されることを示し、$R$ の値を求めよ。<br>(2) バルマー系列（$n'=2$）の光のうち、最も長い波長と最も短い波長を求めよ。<br>(3) 基底状態の水素原子に、運動エネルギー $12.5\,\mathrm{eV}$ の電子を衝突させる。水素原子が励起されうる準位をすべて答えよ。また、その後に水素原子が出しうる光は何種類あるか。そのうち可視光はどれか。<br>(4) 静止していた水素原子（質量 $1.67\times10^{-27}\,\mathrm{kg}$）が $n=2$ から $n=1$ へ移って光子を出すとき、原子が受ける反跳の速さを求めよ。反跳の運動エネルギーは、光子のエネルギーに比べて無視できることを確かめよ。",
  "a": r"(1) $R=\dfrac{13.6\,\mathrm{eV}}{hc}\fallingdotseq1.09\times10^7\,\mathrm{m^{-1}}$　(2) 最長 $6.58\times10^{-7}\,\mathrm m$、最短 $3.66\times10^{-7}\,\mathrm m$　(3) $n=2,\ 3$。3 種類で、可視光は $n=3\to2$ の光　(4) $3.3\,\mathrm{m/s}$（反跳の運動エネルギーは約 $5.5\times10^{-8}\,\mathrm{eV}$）",
  "s": r"(1) $\dfrac{hc}\lambda=E_n-E_{n'}=13.6\left(\dfrac1{n'^2}-\dfrac1{n^2}\right)\,\mathrm{eV}$ より $R=\dfrac{13.6\times1.60\times10^{-19}}{6.63\times10^{-34}\times3.00\times10^8}\fallingdotseq1.09\times10^7\,\mathrm{m^{-1}}$（リュードベリ定数）。<br>(2) 最長は $n=3\to2$：$\lambda=\dfrac{36}{5R}\fallingdotseq6.58\times10^{-7}\,\mathrm m$。最短は $n\to\infty$：$\lambda=\dfrac4R\fallingdotseq3.66\times10^{-7}\,\mathrm m$。<br>(3) 励起エネルギーは $n=2$ が $10.2\,\mathrm{eV}$、$n=3$ が $13.6\times\dfrac89\fallingdotseq12.1\,\mathrm{eV}$、$n=4$ が $12.75\,\mathrm{eV}$。$12.5\,\mathrm{eV}$ で届くのは $n=2,\ 3$。その後に出る光は $3\to2$、$3\to1$、$2\to1$ の 3 種類で、可視光は $3\to2$（$6.58\times10^{-7}\,\mathrm m$）だけ（他は紫外線）。<br>(4) 光子のエネルギーは $10.2\,\mathrm{eV}=1.632\times10^{-18}\,\mathrm J$、運動量 $p=\dfrac Ec=5.44\times10^{-27}\,\mathrm{kg\cdot m/s}$。運動量保存より原子は逆向きに $p$ をもつので $v=\dfrac p{M}\fallingdotseq3.3\,\mathrm{m/s}$。運動エネルギーは $\dfrac{p^2}{2M}\fallingdotseq8.9\times10^{-27}\,\mathrm J\fallingdotseq5.5\times10^{-8}\,\mathrm{eV}$ で、$10.2\,\mathrm{eV}$ に比べて無視できる。<br><b>ポイント</b>：系列の最長波長は隣の準位から、最短波長は $n\to\infty$ から。電子の衝突による励起では、電子の運動エネルギーの一部だけを受け取れる（光子の吸収と違い、ぴったりの値でなくてよい）。"},
 {"lv": "C", "tag": "総合・電子線回折", "q": r"静止していた電子を電圧 $V$ で加速し、結晶に当てて回折させる。<br>(1) 電子のド・ブロイ波長 $\lambda$ を、$h,\ m,\ e,\ V$ で表せ。<br>(2) 格子面の間隔 $d=2.0\times10^{-10}\,\mathrm m$ の結晶で、電子線と格子面のなす角が $30^\circ$ のときに 1 次の強い反射（$2d\sin\theta=\lambda$）が起こった。電子の波長と加速電圧 $V$ を求めよ。<br>(3) (2) と同じ波長の X 線の光子のエネルギーを eV の単位で求め、(2) の電子の運動エネルギーと比べよ。<br>(4) 加速電圧を (2) の 4 倍にすると、1 次の反射が起こる角の $\sin\theta$ はいくらになるか。また、角 $30^\circ$ で起こる反射は何次の反射になるか。",
  "a": r"(1) $\lambda=\dfrac h{\sqrt{2meV}}$　(2) $2.0\times10^{-10}\,\mathrm m$、$38\,\mathrm V$　(3) $6.2\times10^3\,\mathrm{eV}$。電子の運動エネルギー（約 $38\,\mathrm{eV}$）の約 160 倍　(4) $\sin\theta=0.25$、2 次の反射",
  "s": r"(1) $eV=\dfrac{p^2}{2m}$ より $p=\sqrt{2meV}$、$\lambda=\dfrac hp=\dfrac h{\sqrt{2meV}}$。<br>(2) $\lambda=2d\sin30^\circ=d=2.0\times10^{-10}\,\mathrm m$。$V=\dfrac{h^2}{2me\lambda^2}=\dfrac{(6.63\times10^{-34})^2}{2\times9.1\times10^{-31}\times1.60\times10^{-19}\times(2.0\times10^{-10})^2}\fallingdotseq38\,\mathrm V$。<br>(3) $E=\dfrac{hc}\lambda=\dfrac{1.989\times10^{-25}}{2.0\times10^{-10}}\fallingdotseq9.9\times10^{-16}\,\mathrm J\fallingdotseq6.2\times10^3\,\mathrm{eV}$。同じ波長でも、電子の運動エネルギー（約 $38\,\mathrm{eV}$）はその $\dfrac1{160}$ 程度にすぎない。<br>(4) $\lambda\propto\dfrac1{\sqrt V}$ なので波長は $\dfrac12$ の $1.0\times10^{-10}\,\mathrm m$。$\sin\theta=\dfrac{\lambda}{2d}=0.25$。角 $30^\circ$ では $2d\sin30^\circ=2.0\times10^{-10}\,\mathrm m=2\lambda$ なので 2 次の反射。<br><b>ポイント</b>：電子線回折は物質波の直接の証拠。光子は $E=\dfrac{hc}\lambda$、電子は $E=\dfrac{h^2}{2m\lambda^2}$ と、波長とエネルギーの関係が異なる。"},
]}}


def _form():
    for no, ch in CH.items():
        lv = [it["lv"] for it in ch["items"]]
        assert lv.count("A") == 4 and lv.count("B") in (4, 5) and lv.count("C") == 2, lv
        for it in ch["items"]:
            for k in ("q", "a", "s", "tag"):
                assert it[k].strip(), (no, k)
            assert it["q"].count("$") % 2 == 0 and it["a"].count("$") % 2 == 0 and it["s"].count("$") % 2 == 0
            assert "<b>ポイント</b>" in it["s"]


def _sf(x, v, n):
    """x を有効数字 n 桁に丸めると v になることを確かめる"""
    assert float(f"{float(x):.{n}g}") == v, (float(x), v)


def verify():
    _form()
    h, c, e, m = 6.63e-34, 3.00e8, 1.60e-19, 9.1e-31
    hc = h * c
    _sf(hc, 1.989e-25, 4)
    # A1
    E = hc / 500e-9
    _sf(E, 3.98e-19, 3); _sf(E / e, 2.49, 3); _sf(h / 500e-9, 1.33e-27, 3); _sf(1.0e-3 / E, 2.5e15, 2)
    # A2
    Ep = hc / 400e-9 / e
    _sf(Ep, 3.11, 3); _sf(Ep - 2.0, 1.1, 2); _sf(hc / (2.0 * e), 6.2e-7, 2)
    # A3
    v = (2 * e * 100 / m) ** 0.5
    _sf(v, 5.9e6, 2); _sf(h / (2 * m * e * 100) ** 0.5, 1.2e-10, 2); _sf(h / (0.15 * 40), 1.1e-34, 2)
    # A4
    En = lambda n: -13.6 / n ** 2
    d32 = En(3) - En(2)
    _sf(d32, 1.89, 3); _sf(hc / (d32 * e), 6.58e-7, 3)
    d21 = En(2) - En(1)
    _sf(d21, 10.2, 3); _sf(hc / (d21 * e), 1.22e-7, 3)
    assert hc / (d21 * e) < 3.8e-7
    # B1
    k, v1, v2, g, E_, q = symbols("k v1 v2 g E q", positive=True)
    M = k * v1 / g
    qs = solve(Eq(q * E_, M * g + k * v2), q)[0]
    assert simplify(qs - k * (v1 + v2) / E_) == 0
    data = [3.21, 4.80, 8.02, 6.39]
    ns = [round(x / 1.6) for x in data]
    assert ns == [2, 3, 5, 4]
    _sf(sum(data) / sum(ns), 1.60, 3)
    # B2
    hh = e * (1.33 - 0.50) / (2.0e14)
    _sf(hh, 6.64e-34, 3)
    W = hh * 6.0e14 - e * 0.50
    _sf(W, 3.18e-19, 3); _sf(W / e, 1.99, 3); _sf(W / hh, 4.8e14, 2)
    # B3
    _sf(hc / (e * 4.0e4), 3.1e-11, 2)
    lam, d = 1.0e-10, 2.0e-10
    assert abs(lam / (2 * d) - 0.25) < 1e-12
    assert [n for n in range(1, 10) if n * lam / (2 * d) < 1] == [1, 2, 3]
    # B4
    lc = h / (m * c)
    _sf(lc, 2.43e-12, 3)
    lp = 5.00e-11 + lc
    _sf(lp, 5.24e-11, 3); _sf(hc * (1 / 5.00e-11 - 1 / lp), 1.8e-16, 2); _sf(2 * lc, 4.86e-12, 3)
    # コンプトンの式の導出（相対論的に厳密な形）を sympy で確かめる：E'=E/(1+E(1-cosφ)/mc^2) ⇔ λ'-λ=(h/mc)(1-cosφ)
    hs, cs, ms, ls, ph = symbols("h c m lambda phi", positive=True)
    lps = ls + hs / (ms * cs) * (1 - cos(ph))
    Eph, Eph2 = hs * cs / ls, hs * cs / lps
    assert simplify(Eph2 - Eph / (1 + Eph * (1 - cos(ph)) / (ms * cs ** 2))) == 0
    # B5
    ks, es = symbols("k e", positive=True)
    n = symbols("n", positive=True, integer=True)
    r, vv = symbols("r v", positive=True)
    sol = solve([Eq(ms * vv ** 2 / r, ks * es ** 2 / r ** 2), Eq(2 * pi * r, n * hs / (ms * vv))], [r, vv], dict=True)[0]
    rn = sol[r]
    assert simplify(rn - hs ** 2 * n ** 2 / (4 * pi ** 2 * ks * ms * es ** 2)) == 0
    Etot = ms * sol[vv] ** 2 / 2 - ks * es ** 2 / rn
    assert simplify(Etot + 2 * pi ** 2 * ks ** 2 * ms * es ** 4 / (hs ** 2 * n ** 2)) == 0
    kk = 9.0e9
    r1 = h ** 2 / (4 * 3.141592653589793 ** 2 * kk * m * e ** 2)
    _sf(r1, 5.3e-11, 2)
    E1 = -kk * e ** 2 / (2 * r1)
    _sf(E1, -2.17e-18, 3); _sf(E1 / e, -13.6, 3)
    # C1
    Ry = 13.6 * e / hc
    _sf(Ry, 1.09e7, 3); _sf(36 / (5 * Ry), 6.58e-7, 3); _sf(4 / Ry, 3.66e-7, 3)
    exc = [nn for nn in range(2, 10) if En(nn) - En(1) <= 12.5]
    assert exc == [2, 3]
    lines = {(a, b) for a in (2, 3) for b in (1, 2) if b < a}
    assert len(lines) == 3
    vis = [(a, b) for a, b in lines if 3.8e-7 <= hc / ((En(a) - En(b)) * e) <= 7.7e-7]
    assert vis == [(3, 2)]
    Mh = 1.67e-27
    p = d21 * e / c
    _sf(p, 5.44e-27, 3); _sf(p / Mh, 3.3, 2); _sf(p ** 2 / (2 * Mh), 8.9e-27, 2); _sf(p ** 2 / (2 * Mh) / e, 5.5e-8, 2)
    # C2
    lam = 2 * 2.0e-10 * 0.5
    V = h ** 2 / (2 * m * e * lam ** 2)
    _sf(lam, 2.0e-10, 2); _sf(V, 38, 2)
    Ex = hc / lam
    _sf(Ex, 9.9e-16, 2); _sf(Ex / e, 6.2e3, 2); _sf(Ex / e / V, 160, 2)
    lam4 = h / (2 * m * e * 4 * V) ** 0.5
    _sf(lam4 / (2 * 2.0e-10), 0.25, 2)
    assert abs(2 * 2.0e-10 * 0.5 / lam4 - 2) < 1e-9
