"""問題集 第2章 物質量と化学反応式。CH に問題、verify() で数値・反応式の係数・形式を検算する。"""
import re
from math import log10, floor
from collections import Counter
from fractions import Fraction as Fr

CH = {2: {
"goal": "質量・粒子数・気体の体積・濃度を物質量（mol）を軸に自在に換算する。反応式の係数比から量的関係を立て、過不足・混合物の問題を確実に解く。",
"items": [
 {"lv": "A", "tag": "物質量",
  "q": r"二酸化炭素 $\mathrm{CO_2}$ 11 g について、次の値を求めよ。$\mathrm{C}=12$、$\mathrm{O}=16$、アボガドロ定数 $6.0\times10^{23}\ /\mathrm{mol}$、標準状態（0 ℃、$1.013\times10^5\ \mathrm{Pa}$）での気体のモル体積を $22.4\ \mathrm{L/mol}$ とする。<br>(1) 物質量　(2) 分子の数　(3) 含まれる酸素原子の数　(4) 標準状態での体積　(5) これと同じ数の分子を含む酸素 $\mathrm{O_2}$ の質量",
  "a": r"(1) 0.25 mol　(2) $1.5\times10^{23}$ 個　(3) $3.0\times10^{23}$ 個　(4) 5.6 L　(5) 8.0 g",
  "s": r"$\mathrm{CO_2}=44$ より (1) $\frac{11}{44}=0.25\ \mathrm{mol}$。(2) $0.25\times6.0\times10^{23}=1.5\times10^{23}$。(3) 1分子に O 原子が2個なので $3.0\times10^{23}$。(4) $0.25\times22.4=5.6\ \mathrm{L}$。(5) 分子の数が同じ＝物質量が同じなので $0.25\times32=8.0\ \mathrm{g}$。<br><b>ポイント</b>：質量・粒子数・気体の体積は、いったん物質量に直してから換算する。"},
 {"lv": "A", "tag": "濃度",
  "q": r"$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、$\mathrm{Na}=23$、$\mathrm{S}=32$ とする。<br>(1) 水酸化ナトリウム 2.0 g を水に溶かして 250 mL にした水溶液のモル濃度を求めよ。<br>(2) 質量パーセント濃度 98%、密度 $1.8\ \mathrm{g/cm^3}$ の濃硫酸のモル濃度を求めよ。<br>(3) グルコース $\mathrm{C_6H_{12}O_6}$ 9.0 g を水 250 g に溶かした水溶液の質量モル濃度を求めよ。",
  "a": r"(1) $0.20\ \mathrm{mol/L}$　(2) $18\ \mathrm{mol/L}$　(3) $0.20\ \mathrm{mol/kg}$",
  "s": r"(1) $\mathrm{NaOH}=40$ より $\frac{2.0}{40}=0.050\ \mathrm{mol}$。$0.050\div0.250\ \mathrm{L}=0.20\ \mathrm{mol/L}$。(2) 溶液 1 L（$1000\ \mathrm{cm^3}$）で考える。溶液の質量 $1000\times1.8=1800\ \mathrm{g}$、そのうち $\mathrm{H_2SO_4}$ は $1800\times0.98=1764\ \mathrm{g}$、$\frac{1764}{98}=18\ \mathrm{mol}$。(3) $\mathrm{C_6H_{12}O_6}=180$ より $0.050\ \mathrm{mol}$。溶媒 0.250 kg あたりなので $0.20\ \mathrm{mol/kg}$。<br><b>ポイント</b>：モル濃度は「溶液 1 L あたり」、質量モル濃度は「溶媒 1 kg あたり」。濃度の換算は溶液 1 L（または 100 g）を仮定して始める。"},
 {"lv": "A", "tag": "化学反応式",
  "q": r"次の化学反応式の係数を決め、反応式を完成させよ。<br>(1) $\mathrm{C_3H_8+O_2\to CO_2+H_2O}$<br>(2) $\mathrm{Al+HCl\to AlCl_3+H_2}$<br>(3) $\mathrm{NH_3+O_2\to NO+H_2O}$<br>(4) $\mathrm{Cu+HNO_3\to Cu(NO_3)_2+NO+H_2O}$",
  "a": r"(1) $\mathrm{C_3H_8+5O_2\to3CO_2+4H_2O}$　(2) $\mathrm{2Al+6HCl\to2AlCl_3+3H_2}$　(3) $\mathrm{4NH_3+5O_2\to4NO+6H_2O}$　(4) $\mathrm{3Cu+8HNO_3\to3Cu(NO_3)_2+2NO+4H_2O}$",
  "s": r"(1)〜(3) は、登場回数の少ない原子から合わせる（目算法）。(3) N を合わせて $\mathrm{NH_3}$ と $\mathrm{NO}$ を同数、H を合わせると $\mathrm{2NH_3}$ に $\mathrm{3H_2O}$。O は $2+3=5$ 個で $\frac52\mathrm{O_2}$ となるので全体を2倍。(4) は未定係数法：$a\mathrm{Cu}+b\mathrm{HNO_3}\to c\mathrm{Cu(NO_3)_2}+d\mathrm{NO}+e\mathrm{H_2O}$ とおくと、Cu：$a=c$、H：$b=2e$、N：$b=2c+d$、O：$3b=6c+d+e$。$a=1$ とすると $c=1$、$b=\frac83$、$d=\frac23$、$e=\frac43$ となり、3倍して $3,8,3,2,4$。<br><b>ポイント</b>：目算で合わないときは未定係数法。最後に各原子の数が両辺で等しいか必ず数え直す。"},
 {"lv": "A", "tag": "量的関係",
  "q": r"プロパン $\mathrm{C_3H_8}$ 4.4 g を完全燃焼させた。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、標準状態のモル体積 $22.4\ \mathrm{L/mol}$ とする。<br>(1) 必要な酸素の物質量　(2) その酸素の標準状態での体積　(3) 生じる二酸化炭素の質量　(4) 生じる水の質量",
  "a": r"(1) 0.50 mol　(2) 11 L　(3) 13 g　(4) 7.2 g",
  "s": r"$\mathrm{C_3H_8+5O_2\to3CO_2+4H_2O}$。$\mathrm{C_3H_8}=44$ より 0.10 mol。係数比 $1:5:3:4$ から、(1) $\mathrm{O_2}$ 0.50 mol、(2) $0.50\times22.4=11.2\fallingdotseq11\ \mathrm{L}$、(3) $\mathrm{CO_2}$ 0.30 mol、$0.30\times44=13.2\fallingdotseq13\ \mathrm{g}$、(4) $\mathrm{H_2O}$ 0.40 mol、$0.40\times18=7.2\ \mathrm{g}$。<br><b>ポイント</b>：係数の比＝物質量の比。質量の比ではないことに注意。"},
 {"lv": "B", "tag": "過不足",
  "q": r"マグネシウム 0.60 g に 0.50 mol/L の塩酸 60 mL を加えて反応させた。$\mathrm{Mg}=24$、標準状態のモル体積 $22.4\ \mathrm{L/mol}$ とする。<br>(1) 反応の化学反応式を書け。<br>(2) 反応後、どちらの物質が何 mol 残るか。<br>(3) 発生した水素の標準状態での体積を求めよ。<br>(4) 残った物質の質量を求めよ。<br>(5) マグネシウムをすべて反応させるには、同じ塩酸を少なくともあと何 mL 加えればよいか。",
  "a": r"(1) $\mathrm{Mg+2HCl\to MgCl_2+H_2}$　(2) $\mathrm{Mg}$ が 0.010 mol 残る　(3) 0.34 L　(4) 0.24 g　(5) 40 mL",
  "s": r"$\mathrm{Mg}$ は $\frac{0.60}{24}=0.025\ \mathrm{mol}$、$\mathrm{HCl}$ は $0.50\times0.060=0.030\ \mathrm{mol}$。Mg 0.025 mol をすべて反応させるには HCl が 0.050 mol 必要だが 0.030 mol しかないので、HCl がすべて反応する。反応する Mg は $0.030\times\frac12=0.015\ \mathrm{mol}$ で、(2) Mg が $0.025-0.015=0.010\ \mathrm{mol}$ 残る。(3) $\mathrm{H_2}$ は 0.015 mol、$0.015\times22.4=0.336\fallingdotseq0.34\ \mathrm{L}$。(4) $0.010\times24=0.24\ \mathrm{g}$。(5) 不足する HCl は $0.050-0.030=0.020\ \mathrm{mol}$、$0.020\div0.50=0.040\ \mathrm{L}$。<br><b>ポイント</b>：過不足の問題は、まず両方の物質量を出し、係数比で「どちらが足りないか」を決める。生成物の量は足りない方（すべて反応する方）で決まる。"},
 {"lv": "B", "tag": "混合物",
  "q": r"メタン $\mathrm{CH_4}$ とプロパン $\mathrm{C_3H_8}$ の混合気体を完全燃焼させたところ、二酸化炭素 11 g と水 7.2 g が生じた。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$、標準状態のモル体積 $22.4\ \mathrm{L/mol}$ とする。<br>(1) 混合気体中のメタンとプロパンの物質量を求めよ。<br>(2) 混合気体中のメタンの体積百分率を整数で求めよ。<br>(3) 燃焼に使われた酸素の標準状態での体積を求めよ。",
  "a": r"(1) メタン 0.10 mol、プロパン 0.050 mol　(2) 67%　(3) 10 L",
  "s": r"$\mathrm{CH_4+2O_2\to CO_2+2H_2O}$、$\mathrm{C_3H_8+5O_2\to3CO_2+4H_2O}$。メタン $x$ mol、プロパン $y$ mol とすると、$\mathrm{CO_2}$：$x+3y=\frac{11}{44}=0.25$、$\mathrm{H_2O}$：$2x+4y=\frac{7.2}{18}=0.40$。解いて $x=0.10$、$y=0.050$。(2) 同温・同圧では体積比＝物質量比なので $\frac{0.10}{0.15}\times100\fallingdotseq67\%$。(3) $\mathrm{O_2}$ は $2x+5y=0.20+0.25=0.45\ \mathrm{mol}$、$0.45\times22.4=10.08\fallingdotseq10\ \mathrm{L}$。<br><b>ポイント</b>：混合物は成分ごとに未知数をおき、C・H など原子ごとの保存で連立方程式を立てる。"},
 {"lv": "B", "tag": "濃度の換算",
  "q": r"質量パーセント濃度 36.5%、密度 $1.18\ \mathrm{g/cm^3}$ の濃塩酸がある。$\mathrm{H}=1.0$、$\mathrm{Cl}=35.5$ とする。<br>(1) この濃塩酸のモル濃度を有効数字3桁で求めよ。<br>(2) この濃塩酸を水で薄めて、0.100 mol/L の塩酸 500 mL をつくりたい。必要な濃塩酸の体積〔mL〕を有効数字3桁で求めよ。<br>(3) この濃塩酸の質量モル濃度を有効数字3桁で求めよ。",
  "a": r"(1) $11.8\ \mathrm{mol/L}$　(2) 4.24 mL　(3) $15.7\ \mathrm{mol/kg}$",
  "s": r"(1) 溶液 1 L は $1000\times1.18=1180\ \mathrm{g}$、HCl は $1180\times0.365=430.7\ \mathrm{g}$、$\frac{430.7}{36.5}=11.8\ \mathrm{mol}$。(2) 必要な HCl は $0.100\times0.500=0.0500\ \mathrm{mol}$。薄めても溶質の物質量は変わらないので、$\frac{0.0500}{11.8}\ \mathrm{L}=4.24\times10^{-3}\ \mathrm{L}$。(3) 溶液 100 g で考えると、HCl 36.5 g（1.00 mol）、水 63.5 g。$\frac{1.00}{0.0635}\fallingdotseq15.7\ \mathrm{mol/kg}$。<br><b>ポイント</b>：モル濃度は「溶液 1 L」、質量モル濃度は「溶液 100 g（溶質と溶媒に分ける）」を仮定すると計算しやすい。希釈では溶質の物質量が保存される。"},
 {"lv": "B", "tag": "結晶水",
  "q": r"硫酸銅(II)五水和物 $\mathrm{CuSO_4\cdot5H_2O}$ について、次の問いに答えよ。$\mathrm{H}=1.0$、$\mathrm{O}=16$、$\mathrm{S}=32$、$\mathrm{Cu}=64$ とする。<br>(1) 0.10 mol/L の硫酸銅(II)水溶液 200 mL をつくるのに必要な五水和物の質量を求めよ。<br>(2) 五水和物 25 g を水 75 g に溶かした水溶液の、$\mathrm{CuSO_4}$ の質量パーセント濃度を求めよ。<br>(3) 五水和物 2.50 g を少しずつ加熱したところ、ある温度で質量が 1.78 g となり、しばらく一定になった。このときの固体の組成式を $\mathrm{CuSO_4\cdot}x\mathrm{H_2O}$ の形で答えよ。",
  "a": r"(1) 5.0 g　(2) 16%　(3) $\mathrm{CuSO_4\cdot H_2O}$",
  "s": r"$\mathrm{CuSO_4}=160$、$\mathrm{CuSO_4\cdot5H_2O}=250$。(1) $\mathrm{CuSO_4}$ は $0.10\times0.200=0.020\ \mathrm{mol}$。五水和物 1 mol から $\mathrm{CuSO_4}$ 1 mol が得られるので $0.020\times250=5.0\ \mathrm{g}$。(2) 25 g 中の $\mathrm{CuSO_4}$ は $25\times\frac{160}{250}=16\ \mathrm{g}$。溶液は $25+75=100\ \mathrm{g}$（結晶水は溶媒の水になる）なので 16%。(3) 五水和物は $\frac{2.50}{250}=0.0100\ \mathrm{mol}$。失われた水は $2.50-1.78=0.72\ \mathrm{g}$ で $0.040\ \mathrm{mol}$。残る水は $0.050-0.040=0.010\ \mathrm{mol}$ で、$\mathrm{CuSO_4}$ 0.0100 mol あたり 1 mol。<br><b>ポイント</b>：水和物を溶かすと、結晶水は溶媒に加わる。溶質の質量は式量の比で取り出す。"},
 {"lv": "B", "tag": "実験・考察",
  "q": r"<div class=" + '"bun"' + r">ステアリン酸 $\mathrm{C_{17}H_{35}COOH}$（分子量 284）0.0284 g をヘキサンに溶かして 100 mL とした。この溶液 0.10 mL を水面に静かに滴下すると、ヘキサンが蒸発したあと、ステアリン酸の分子がすき間なく1層に並んだ膜（単分子膜）ができ、その面積は $120\ \mathrm{cm^2}$ であった。ステアリン酸1分子が水面上で占める面積は $2.0\times10^{-15}\ \mathrm{cm^2}$ とする。</div>(1) 滴下した溶液に含まれるステアリン酸の物質量を求めよ。<br>(2) 膜をつくっている分子の数を求めよ。<br>(3) この実験から、アボガドロ定数を求めよ。<br>(4) ステアリン酸の分子は、水面に対してどのような向きに並ぶか。分子の構造に着目して説明せよ。",
  "a": r"(1) $1.0\times10^{-7}\ \mathrm{mol}$　(2) $6.0\times10^{16}$ 個　(3) $6.0\times10^{23}\ /\mathrm{mol}$　(4) 親水性のカルボキシ基 $\mathrm{-COOH}$ を水側に、疎水性の炭化水素基を空気側に向けて並ぶ。",
  "s": r"(1) 0.0284 g は $\frac{0.0284}{284}=1.00\times10^{-4}\ \mathrm{mol}$。これが 100 mL 中にあるので、0.10 mL 中には $1.00\times10^{-4}\times\frac{0.10}{100}=1.0\times10^{-7}\ \mathrm{mol}$。(2) $\frac{120}{2.0\times10^{-15}}=6.0\times10^{16}$。(3) 1 mol あたりの粒子数なので $\frac{6.0\times10^{16}}{1.0\times10^{-7}}=6.0\times10^{23}\ /\mathrm{mol}$。(4) $\mathrm{-COOH}$ は水と水素結合しやすく、長い炭化水素鎖 $\mathrm{C_{17}H_{35}-}$ は水になじまない。<br><b>ポイント</b>：アボガドロ定数＝「粒子の数 ÷ 物質量」。実験では、数えにくい粒子数を「面積 ÷ 1個の面積」のように別の量から求める。"},
 {"lv": "C", "tag": "総合",
  "q": r"マグネシウムとアルミニウムの混合物 1.02 g に十分な量の塩酸を加えると、水素が標準状態で 1.12 L 発生した。$\mathrm{Mg}=24$、$\mathrm{Al}=27$、標準状態のモル体積 $22.4\ \mathrm{L/mol}$ とする。<br>(1) マグネシウム・アルミニウムと塩酸の反応をそれぞれ化学反応式で書け。<br>(2) 混合物中のマグネシウムとアルミニウムの物質量を求めよ。<br>(3) 同じ質量の混合物に十分な量の水酸化ナトリウム水溶液を加えると、何 L（標準状態）の水素が発生するか。反応式も示せ。<br>(4) 同じ質量の混合物に、0.50 mol/L の塩酸を 100 mL だけ加えたとき、発生する水素は標準状態で何 L か。",
  "a": r"(1) $\mathrm{Mg+2HCl\to MgCl_2+H_2}$、$\mathrm{2Al+6HCl\to2AlCl_3+3H_2}$　(2) Mg 0.0200 mol、Al 0.0200 mol　(3) $\mathrm{2Al+2NaOH+6H_2O\to2Na[Al(OH)_4]+3H_2}$、0.672 L　(4) 0.56 L",
  "s": r"(2) Mg $x$ mol、Al $y$ mol とすると、質量：$24x+27y=1.02$、水素：$x+\frac32y=\frac{1.12}{22.4}=0.0500$。解いて $x=0.0200$、$y=0.0200$。(3) 水酸化ナトリウム水溶液と反応するのは両性金属の Al だけ。$\mathrm{H_2}$ は $0.0200\times\frac32=0.0300\ \mathrm{mol}$、$0.0300\times22.4=0.672\ \mathrm{L}$。(4) 金属をすべて溶かすのに必要な HCl は $2\times0.0200+3\times0.0200=0.100\ \mathrm{mol}$ だが、加えたのは $0.50\times0.100=0.050\ \mathrm{mol}$ なので HCl が不足する。どちらの金属が先に反応しても、$\mathrm{H^+}$ 2 mol から $\mathrm{H_2}$ 1 mol が生じる関係は同じなので、$\mathrm{H_2}=\frac{0.050}{2}=0.025\ \mathrm{mol}$、$0.025\times22.4=0.56\ \mathrm{L}$。<br><b>ポイント</b>：酸が不足するときは、生じる $\mathrm{H_2}$ が酸の量だけで決まる（$\mathrm{2H^+\to H_2}$）。どの金属が反応したかを考えなくても答えが出る。"},
 {"lv": "C", "tag": "総合",
  "q": r"水素・一酸化炭素・メタンからなる混合気体 60 mL に酸素 150 mL を加えて点火し、完全燃焼させた。もとの温度・圧力にもどすと、気体の体積は 120 mL になった。さらにこの気体を水酸化カリウム水溶液に通して二酸化炭素を完全に吸収させると、体積は 90 mL になった。生じた水はすべて液体で、その体積や水への気体の溶解は無視できる。体積はすべて同温・同圧で測ったものとする。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$。<br>(1) 3種類の気体の燃焼をそれぞれ化学反応式で書け。<br>(2) 最初の混合気体中の水素・一酸化炭素・メタンの体積を求めよ。<br>(3) 最初の混合気体の平均分子量を求めよ。",
  "a": r"(1) $\mathrm{2H_2+O_2\to2H_2O}$、$\mathrm{2CO+O_2\to2CO_2}$、$\mathrm{CH_4+2O_2\to CO_2+2H_2O}$　(2) 水素 30 mL、一酸化炭素 10 mL、メタン 20 mL　(3) 11",
  "s": r"$\mathrm{H_2}$ $a$ mL、$\mathrm{CO}$ $b$ mL、$\mathrm{CH_4}$ $c$ mL とする。同温・同圧では体積比＝物質量比なので、体積で係数比を使える。燃焼後の 120 mL は残った $\mathrm{O_2}$ と生じた $\mathrm{CO_2}$、KOH 水溶液に通したあとの 90 mL は残った $\mathrm{O_2}$。よって $\mathrm{CO_2}$：$b+c=120-90=30$、消費された $\mathrm{O_2}$：$\frac a2+\frac b2+2c=150-90=60$、全体：$a+b+c=60$。第1式と第3式から $a=30$。第2式に代入して $\frac b2+2c=45$、これと $b+c=30$ から $c=20$、$b=10$。(3) $\frac{30\times2.0+10\times28+20\times16}{60}=\frac{660}{60}=11$。<br><b>ポイント</b>：気体反応の体積の問題は「何が残り、何が吸収されたか」を整理し、成分ごとに体積の式を立てる。水が液体になる条件では、水の体積は数えない。"},
]}}


AW = {"H": 1.0, "C": 12, "N": 14, "O": 16, "Na": 23, "Mg": 24, "Al": 27, "S": 32, "Cl": 35.5, "Cu": 64}


def _parse(s):
    st, i = [Counter()], 0
    while i < len(s):
        if s[i] in "([":
            st.append(Counter()); i += 1
        elif s[i] in ")]":
            m = re.match(r"\d*", s[i + 1:]); k = int(m.group() or 1); i += 1 + len(m.group())
            top = st.pop()
            for e, c in top.items():
                st[-1][e] += k * c
        else:
            m = re.match(r"([A-Z][a-z]?)(\d*)", s[i:])
            st[-1][m.group(1)] += int(m.group(2) or 1); i += len(m.group())
    return st[0]


def atoms(f):
    tot = Counter()
    for part in f.split("·"):
        m = re.match(r"(\d*)(.+)", part)
        for e, c in _parse(m.group(2)).items():
            tot[e] += int(m.group(1) or 1) * c
    return tot


def Mr(f):
    return sum(AW[e] * c for e, c in atoms(f).items())


def balanced(lhs, rhs):
    def tot(side):
        t = Counter()
        for k, f in side:
            for e, c in atoms(f).items():
                t[e] += k * c
        return +t
    assert tot(lhs) == tot(rhs), (lhs, rhs)


def verify():
    items = CH[2]["items"]
    lv = [it["lv"] for it in items]
    assert lv == sorted(lv) and lv.count("A") == 4 and 4 <= lv.count("B") <= 5 and lv.count("C") == 2
    for it in items:
        for k in ("tag", "q", "a", "s"):
            assert it[k].strip(), k
        for k in ("q", "a", "s"):
            assert it[k].count("$") % 2 == 0 and "$$" not in it[k], it[k][:30]
        assert "<b>ポイント</b>" in it["s"]

    def sig(x, n=2):
        return round(x, n - 1 - int(floor(log10(abs(x)))))

    def eq(x, v, n=2):
        assert abs(sig(x, n) - v) <= 1e-9 * abs(v), (x, sig(x, n), v)

    # A1
    n = 11 / Mr("CO2"); eq(n, 0.25); eq(n * 6.0e23, 1.5e23); eq(2 * n * 6.0e23, 3.0e23); eq(n * 22.4, 5.6); eq(n * Mr("O2"), 8.0)
    # A2
    eq(2.0 / Mr("NaOH") / 0.250, 0.20); eq(1000 * 1.8 * 0.98 / Mr("H2SO4"), 18); eq(9.0 / Mr("C6H12O6") / 0.250, 0.20)
    # A3 係数
    balanced([(1, "C3H8"), (5, "O2")], [(3, "CO2"), (4, "H2O")])
    balanced([(2, "Al"), (6, "HCl")], [(2, "AlCl3"), (3, "H2")])
    balanced([(4, "NH3"), (5, "O2")], [(4, "NO"), (6, "H2O")])
    balanced([(3, "Cu"), (8, "HNO3")], [(3, "Cu(NO3)2"), (2, "NO"), (4, "H2O")])
    a, c = Fr(1), Fr(1); b = Fr(8, 3); d = b - 2 * c; e = b / 2
    assert 3 * b == 6 * c + d + e and (d, e) == (Fr(2, 3), Fr(4, 3))
    # A4
    n = 4.4 / Mr("C3H8"); assert abs(n - 0.10) < 1e-12
    eq(5 * n, 0.50); eq(5 * n * 22.4, 11); eq(3 * n * Mr("CO2"), 13); eq(4 * n * Mr("H2O"), 7.2)
    # B1 過不足
    mg, hcl = 0.60 / 24, 0.50 * 0.060
    assert hcl < 2 * mg
    eq(mg - hcl / 2, 0.010); eq(hcl / 2 * 22.4, 0.34); eq((mg - hcl / 2) * 24, 0.24); eq((2 * mg - hcl) / 0.50 * 1000, 40)
    # B2 混合気体
    co2, h2o = 11 / Mr("CO2"), 7.2 / Mr("H2O")
    y = (h2o - 2 * co2) / (4 - 6); x = co2 - 3 * y
    eq(x, 0.10); eq(y, 0.050); assert round(100 * x / (x + y)) == 67; eq((2 * x + 5 * y) * 22.4, 10)
    balanced([(1, "CH4"), (2, "O2")], [(1, "CO2"), (2, "H2O")])
    # B3 濃塩酸
    c = 1000 * 1.18 * 0.365 / Mr("HCl"); eq(c, 11.8, 3)
    eq(0.100 * 0.500 / c * 1000, 4.24, 3); eq(1.00 / 0.0635, 15.7, 3)
    assert abs(Mr("HCl") - 36.5) < 1e-9 and round(1180 * 0.365, 1) == 430.7
    # B4 結晶水
    assert Mr("CuSO4·5H2O") == 250 and Mr("CuSO4") == 160
    eq(0.10 * 0.200 * 250, 5.0); eq(25 * 160 / 250 / 100 * 100, 16)
    n = 2.50 / 250; lost = (2.50 - 1.78) / 18
    assert abs((5 * n - lost) / n - 1) < 1e-9 and abs(Mr("CuSO4·H2O") * n - 1.78) < 1e-9
    # B5 単分子膜
    assert Mr("C17H35COOH") == 284
    nmol = 0.0284 / 284 * 0.10 / 100; eq(nmol, 1.0e-7); eq(120 / 2.0e-15, 6.0e16); eq(120 / 2.0e-15 / nmol, 6.0e23)
    # C1 Mg/Al
    nh2 = 1.12 / 22.4
    det = 24 * 1.5 - 27 * 1
    x = (1.02 * 1.5 - 27 * nh2) / det; y = (24 * nh2 - 1.02) / det
    eq(x, 0.0200, 3); eq(y, 0.0200, 3)
    balanced([(1, "Mg"), (2, "HCl")], [(1, "MgCl2"), (1, "H2")])
    balanced([(2, "Al"), (2, "NaOH"), (6, "H2O")], [(2, "Na[Al(OH)4]"), (3, "H2")])
    eq(1.5 * y * 22.4, 0.672, 3)
    need = 2 * x + 3 * y; add = 0.50 * 0.100
    assert add < need
    eq(add / 2 * 22.4, 0.56)
    # C2 気体の燃焼（体積）
    from sympy import symbols, solve, Rational
    A, B, C_ = symbols("A B C")
    sol = solve([A + B + C_ - 60, B + C_ - 30, A / 2 + B / 2 + 2 * C_ - 60], [A, B, C_])
    assert (sol[A], sol[B], sol[C_]) == (30, 10, 20)
    o2_left = 150 - (30 / 2 + 10 / 2 + 2 * 20); assert o2_left == 90 and o2_left + 30 == 120
    eq((30 * 2.0 + 10 * Mr("CO") + 20 * Mr("CH4")) / 60, 11)
    balanced([(2, "H2"), (1, "O2")], [(2, "H2O")]); balanced([(2, "CO"), (1, "O2")], [(2, "CO2")])
