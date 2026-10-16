"""問題集 第7章 図形の性質。CH に問題、verify() で答えを座標計算・構成で検算する。"""
from sympy import *
from itertools import combinations


def _fig_orth():
    """B(-2,0), C(3,0), A(0,6), 垂心 H(0,1), D(0,-1), 外接円 中心(1/2,5/2)"""
    u, ox, oy = 23, 84, 148
    X = lambda x: ox + u * x
    Y = lambda y: oy - u * y
    P = {"A": (0, 6), "B": (-2, 0), "C": (3, 0), "H": (0, 1), "D": (0, -1), "E": (0, 0)}
    s = ['<svg class="fig" width="200" height="184" viewBox="0 0 200 184">']
    s.append(f'<circle cx="{X(0.5)}" cy="{Y(2.5)}" r="{u * float(sqrt(Rational(25, 2))):.1f}" fill="none" stroke="#999"/>')
    s.append(f'<polygon points="{X(0)},{Y(6)} {X(-2)},{Y(0)} {X(3)},{Y(0)}" fill="none" stroke="#1f3f8f" stroke-width="1.5"/>')
    s.append(f'<line x1="{X(0)}" y1="{Y(6)}" x2="{X(0)}" y2="{Y(-1)}" stroke="#c0392b" stroke-dasharray="4,2"/>')
    s.append(f'<line x1="{X(-2)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(-1)}" stroke="#d27a00"/>')
    s.append(f'<line x1="{X(-2)}" y1="{Y(0)}" x2="{X(0)}" y2="{Y(1)}" stroke="#d27a00"/>')
    lab = {"A": (4, 0), "B": (-12, 4), "C": (5, 4), "H": (4, -2), "D": (4, 10), "E": (4, 12)}
    for k, (x, y) in P.items():
        s.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="2.2" fill="#333"/>')
        s.append(f'<text x="{X(x) + lab[k][0]}" y="{Y(y) + lab[k][1]}" font-size="11">{k}</text>')
    s.append('</svg>')
    return "".join(s)


CH = {7: {
"goal": "角の二等分線の定理・メネラウス・チェバ・方べきの定理・接弦定理を、辺の比や長さの計算に自在に使う。図形の論証では「どの定理の仮定が満たされているか」を明示する。",
"items": [
 {"lv": "A", "q": r"$\triangle\mathrm{ABC}$ において $\mathrm{AB}=6,\ \mathrm{BC}=5,\ \mathrm{CA}=4$ である。$\angle\mathrm{A}$ の二等分線と辺 $\mathrm{BC}$ の交点を $\mathrm D$、$\angle\mathrm{A}$ の外角の二等分線と直線 $\mathrm{BC}$ の交点を $\mathrm E$ とする。$\mathrm{BD},\ \mathrm{CE},\ \mathrm{DE}$ の長さを求めよ。",
  "a": r"$\mathrm{BD}=3,\ \mathrm{CE}=10,\ \mathrm{DE}=12$",
  "s": r"$\mathrm{BD}:\mathrm{DC}=\mathrm{AB}:\mathrm{AC}=3:2$ より $\mathrm{BD}=5\cdot\frac35=3$、$\mathrm{DC}=2$。外角の二等分線は $\mathrm{BC}$ を $\mathrm{BE}:\mathrm{EC}=3:2$ に外分する。$\mathrm{AB}>\mathrm{AC}$ なので $\mathrm E$ は $\mathrm C$ の側の延長上にあり、$\mathrm{CE}=x$ とおくと $(5+x):x=3:2$、$x=10$。$\mathrm{DE}=2+10=12$。<br><b>ポイント</b>：内角・外角の二等分線は、対辺を同じ比 $\mathrm{AB}:\mathrm{AC}$ に内分・外分する。"},
 {"lv": "A", "q": r"$\triangle\mathrm{ABC}$ において $\angle\mathrm A=50^\circ,\ \angle\mathrm B=60^\circ,\ \angle\mathrm C=70^\circ$ とする。内心を $\mathrm I$、外心を $\mathrm O$、垂心を $\mathrm H$ とするとき、$\angle\mathrm{BIC},\ \angle\mathrm{BOC},\ \angle\mathrm{BHC}$ を求めよ。",
  "a": r"$\angle\mathrm{BIC}=115^\circ,\ \angle\mathrm{BOC}=100^\circ,\ \angle\mathrm{BHC}=130^\circ$",
  "s": r"内心：$\angle\mathrm{IBC}+\angle\mathrm{ICB}=\frac12(60^\circ+70^\circ)=65^\circ$ より $\angle\mathrm{BIC}=115^\circ$（一般に $90^\circ+\frac A2$）。<br>外心：$\mathrm O$ は外接円の中心で、$\angle\mathrm A$ は鋭角だから中心角 $\angle\mathrm{BOC}=2\angle\mathrm A=100^\circ$。<br>垂心：$\mathrm B,\ \mathrm C$ から対辺に下ろした垂線の足をそれぞれ $\mathrm E,\ \mathrm F$ とすると、四角形 $\mathrm{AFHE}$ は $\mathrm E,\ \mathrm F$ の角が直角なので $\angle\mathrm{EHF}=360^\circ-90^\circ-90^\circ-50^\circ=130^\circ$。$\angle\mathrm{BHC}$ はその対頂角で $130^\circ$（一般に鋭角三角形で $180^\circ-A$）。<br><b>ポイント</b>：内心は角の二等分線、外心は円周角と中心角、垂心は直角2つを含む四角形で処理する。"},
 {"lv": "A", "tag": "方べきの定理", "q": r"円の外部の点 $\mathrm P$ を通る2直線が円とそれぞれ2点 $\mathrm A,\ \mathrm B$ および $\mathrm C,\ \mathrm D$ で交わる（$\mathrm A$ は $\mathrm P$ と $\mathrm B$ の間、$\mathrm C$ は $\mathrm P$ と $\mathrm D$ の間）。$\mathrm{PA}=3,\ \mathrm{AB}=5,\ \mathrm{PC}=4$ のとき、$\mathrm{CD}$ の長さを求めよ。また、$\mathrm P$ から円に引いた接線の接点を $\mathrm T$ とするとき、$\mathrm{PT}$ の長さを求めよ。",
  "a": r"$\mathrm{CD}=2,\ \mathrm{PT}=2\sqrt6$",
  "s": r"方べきの定理 $\mathrm{PA}\cdot\mathrm{PB}=\mathrm{PC}\cdot\mathrm{PD}$ より $3\cdot8=4\cdot\mathrm{PD}$、$\mathrm{PD}=6$、$\mathrm{CD}=6-4=2$。接線については $\mathrm{PT}^2=\mathrm{PA}\cdot\mathrm{PB}=24$ より $\mathrm{PT}=2\sqrt6$。<br><b>ポイント</b>：$\mathrm{PB}=\mathrm{PA}+\mathrm{AB}$ と、点 $\mathrm P$ からの長さに直してから使う。"},
 {"lv": "A", "tag": "メネラウス・チェバ", "q": r"$\triangle\mathrm{ABC}$ の辺 $\mathrm{AB}$ を $2:1$ に内分する点を $\mathrm R$、辺 $\mathrm{AC}$ を $3:2$ に内分する点を $\mathrm Q$ とし、線分 $\mathrm{BQ}$ と $\mathrm{CR}$ の交点を $\mathrm O$、直線 $\mathrm{AO}$ と辺 $\mathrm{BC}$ の交点を $\mathrm P$ とする。$\mathrm{BP}:\mathrm{PC}$ と $\mathrm{BO}:\mathrm{OQ}$ を求めよ。",
  "a": r"$\mathrm{BP}:\mathrm{PC}=3:4$、$\mathrm{BO}:\mathrm{OQ}=5:4$",
  "s": r"チェバの定理 $\frac{\mathrm{AR}}{\mathrm{RB}}\cdot\frac{\mathrm{BP}}{\mathrm{PC}}\cdot\frac{\mathrm{CQ}}{\mathrm{QA}}=1$ より $2\cdot\frac{\mathrm{BP}}{\mathrm{PC}}\cdot\frac23=1$、$\frac{\mathrm{BP}}{\mathrm{PC}}=\frac34$。<br>$\triangle\mathrm{ABQ}$ と直線 $\mathrm{RC}$ にメネラウスの定理：$\frac{\mathrm{AR}}{\mathrm{RB}}\cdot\frac{\mathrm{BO}}{\mathrm{OQ}}\cdot\frac{\mathrm{QC}}{\mathrm{CA}}=1$ より $2\cdot\frac{\mathrm{BO}}{\mathrm{OQ}}\cdot\frac25=1$、$\frac{\mathrm{BO}}{\mathrm{OQ}}=\frac54$。<br><b>ポイント</b>：メネラウスは「三角形の頂点 → 分点 → 頂点 …」と一筆書きで比をつなぐ。どの三角形とどの直線を使うかを最初に決める。"},
 {"lv": "B", "tag": "接弦定理", "q": r"$\mathrm{AB}=2,\ \mathrm{BC}=4,\ \mathrm{CA}=3$ の $\triangle\mathrm{ABC}$ の外接円について、点 $\mathrm A$ における接線と直線 $\mathrm{BC}$ の交点を $\mathrm T$ とする。<br>(1) $\triangle\mathrm{TAB}\backsim\triangle\mathrm{TCA}$ であることを示せ。　(2) $\mathrm{TB},\ \mathrm{TA}$ の長さを求めよ。",
  "a": r"(1) 略　(2) $\mathrm{TB}=\frac{16}{5},\ \mathrm{TA}=\frac{24}{5}$",
  "s": r"(1) $\mathrm{AB}<\mathrm{AC}$ より $\angle\mathrm C<\angle\mathrm B$ なので、$\mathrm T$ は辺 $\mathrm{BC}$ の $\mathrm B$ 側の延長上にある（$\mathrm C$ 側にあるとすると、接弦定理から $\triangle\mathrm{TAC}$ の内角 $\angle\mathrm{ATC}=\angle\mathrm C-\angle\mathrm B$ が負になってしまう）。接弦定理より $\angle\mathrm{TAB}=\angle\mathrm{ACB}=\angle\mathrm{TCA}$。$\angle\mathrm{ATB}$ は共通。2組の角がそれぞれ等しいので $\triangle\mathrm{TAB}\backsim\triangle\mathrm{TCA}$。■<br>(2) 相似比は $\mathrm{AB}:\mathrm{CA}=2:3$ なので $\mathrm{TB}=\frac23\mathrm{TA},\ \mathrm{TA}=\frac23\mathrm{TC}$。よって $\mathrm{TB}=\frac49\mathrm{TC}$。$\mathrm{TC}-\mathrm{TB}=\mathrm{BC}=4$ より $\frac59\mathrm{TC}=4$、$\mathrm{TC}=\frac{36}5$。$\mathrm{TB}=\frac{16}5,\ \mathrm{TA}=\frac23\cdot\frac{36}5=\frac{24}5$。（方べきの定理 $\mathrm{TA}^2=\mathrm{TB}\cdot\mathrm{TC}=\frac{576}{25}$ とも一致する。）<br><b>ポイント</b>：接線と弦があれば接弦定理で相似な三角形を作る。$\mathrm{TA}^2=\mathrm{TB}\cdot\mathrm{TC}$ は方べきの定理そのもの。"},
 {"lv": "B", "q": r"$\mathrm{AB}=7,\ \mathrm{BC}=8,\ \mathrm{CA}=9$ の $\triangle\mathrm{ABC}$ の内心を $\mathrm I$ とし、内接円と辺 $\mathrm{BC}$ の接点を $\mathrm D$、直線 $\mathrm{AI}$ と辺 $\mathrm{BC}$ の交点を $\mathrm E$ とする。<br>(1) $\mathrm{BD}$ の長さを求めよ。　(2) 内接円の半径 $r$ を求めよ。　(3) $\mathrm{AI}:\mathrm{IE}$ を求めよ。",
  "a": r"(1) $3$　(2) $\sqrt5$　(3) $2:1$",
  "s": r"(1) 接点を $\mathrm{BC}$ 上 $\mathrm D$、$\mathrm{CA}$ 上 $\mathrm F$、$\mathrm{AB}$ 上 $\mathrm G$ とすると、1点から引いた接線の長さは等しいので $\mathrm{BD}=\mathrm{BG}=x$、$\mathrm{CD}=\mathrm{CF}=8-x$、$\mathrm{AG}=\mathrm{AF}=7-x$。$\mathrm{AF}+\mathrm{FC}=9$ より $(7-x)+(8-x)=9$、$x=3$。<br>(2) $s=\frac{7+8+9}2=12$。ヘロンの公式で面積 $S=\sqrt{12\cdot5\cdot4\cdot3}=12\sqrt5$。$S=rs$ より $r=\sqrt5$。<br>(3) $\mathrm{BE}:\mathrm{EC}=7:9$ より $\mathrm{BE}=8\cdot\frac7{16}=\frac72$。$\triangle\mathrm{ABE}$ で $\mathrm{BI}$ は $\angle\mathrm B$ の二等分線なので $\mathrm{AI}:\mathrm{IE}=\mathrm{AB}:\mathrm{BE}=7:\frac72=2:1$。<br><b>ポイント</b>：接線の長さは $\mathrm{BD}=\frac{\mathrm{AB}+\mathrm{BC}-\mathrm{CA}}2$ の形で覚えておくと速い。"},
 {"lv": "B", "q": r"半径 $5$ の円 $\mathrm{O}$ と半径 $2$ の円 $\mathrm{O'}$ があり、中心間の距離は $9$ である。<br>(1) 2円の位置関係を答え、共通接線は何本あるか答えよ。<br>(2) 共通外接線について、2つの接点の間の距離を求めよ。<br>(3) 共通内接線について、2つの接点の間の距離を求めよ。",
  "a": r"(1) 互いに外部にある、4本　(2) $6\sqrt2$　(3) $4\sqrt2$",
  "s": r"(1) $9>5+2$ なので互いに外部にあり、共通接線は外接線2本・内接線2本の計4本。<br>(2) 接点を $\mathrm{P},\ \mathrm{Q}$ とし、$\mathrm{O'}$ から $\mathrm{OP}$ に垂線 $\mathrm{O'H}$ を下ろすと、$\mathrm{PQO'H}$ は長方形で $\mathrm{OH}=5-2=3$。$\mathrm{PQ}=\mathrm{O'H}=\sqrt{9^2-3^2}=\sqrt{72}=6\sqrt2$。<br>(3) 同様に $\mathrm{OP}$ の延長上に $\mathrm H$ をとると $\mathrm{OH}=5+2=7$、$\mathrm{PQ}=\sqrt{81-49}=\sqrt{32}=4\sqrt2$。<br><b>ポイント</b>：共通接線の長さは、中心どうしを結ぶ線分を斜辺とする直角三角形を作る。他方の半径を「引く」か「足す」かが外接線と内接線の違い。"},
 {"lv": "B", "tag": "空間図形", "q": r"正五角形の面12枚と正六角形の面20枚で囲まれ、どの頂点にも3つの面が集まっている凸多面体（サッカーボールの形）について答えよ。<br>(1) 辺の数 $e$ と頂点の数 $v$ を求め、オイラーの多面体定理が成り立つことを確かめよ。<br>(2) 同じ面上にない2頂点を結ぶ線分（空間対角線）は何本あるか。",
  "a": r"(1) $e=90,\ v=60$、$60-90+32=2$　(2) $1440$ 本",
  "s": r"(1) 面の辺の総数 $12\cdot5+20\cdot6=180$ は各辺を2回ずつ数えているので $e=90$。頂点の総数は各頂点を3回ずつ数えているので $v=\frac{180}{3}=60$。$v-e+f=60-90+32=2$ で成り立つ。<br>(2) 2頂点の選び方 ${}_{60}\mathrm{C}_2=1770$ から、辺 $90$ 本と面の対角線を除く。正五角形の対角線は $5$ 本、正六角形は $9$ 本なので、面の対角線は $12\cdot5+20\cdot9=240$ 本。$1770-90-240=1440$ 本。<br><b>ポイント</b>：多面体の辺・頂点は「面ごとに数えて重複度で割る」。凸多面体では、隣り合わない2頂点が2つの面に同時に含まれることはないので、面の対角線は重複しない。"},
 {"lv": "B", "q": r"$\triangle\mathrm{ABC}$ の辺 $\mathrm{AB}$ を $1:2$ に内分する点を $\mathrm D$、辺 $\mathrm{BC}$ を $3:1$ に内分する点を $\mathrm E$ とし、線分 $\mathrm{AE}$ と $\mathrm{CD}$ の交点を $\mathrm P$ とする。<br>(1) $\mathrm{AP}:\mathrm{PE}$ と $\mathrm{CP}:\mathrm{PD}$ を求めよ。<br>(2) $\triangle\mathrm{PBC}$ の面積は $\triangle\mathrm{ABC}$ の面積の何倍か。",
  "a": r"(1) $\mathrm{AP}:\mathrm{PE}=2:1$、$\mathrm{CP}:\mathrm{PD}=1:1$　(2) $\frac13$ 倍",
  "s": r"(1) $\triangle\mathrm{ABE}$ と直線 $\mathrm{DC}$ にメネラウスの定理：$\frac{\mathrm{AD}}{\mathrm{DB}}\cdot\frac{\mathrm{BC}}{\mathrm{CE}}\cdot\frac{\mathrm{EP}}{\mathrm{PA}}=1$ より $\frac12\cdot\frac41\cdot\frac{\mathrm{EP}}{\mathrm{PA}}=1$、$\mathrm{AP}:\mathrm{PE}=2:1$。<br>$\triangle\mathrm{BCD}$ と直線 $\mathrm{AE}$ に：$\frac{\mathrm{BE}}{\mathrm{EC}}\cdot\frac{\mathrm{CP}}{\mathrm{PD}}\cdot\frac{\mathrm{DA}}{\mathrm{AB}}=1$ より $3\cdot\frac{\mathrm{CP}}{\mathrm{PD}}\cdot\frac13=1$、$\mathrm{CP}:\mathrm{PD}=1:1$。<br>(2) $\triangle\mathrm{PBC}$ と $\triangle\mathrm{ABC}$ は底辺 $\mathrm{BC}$ が共通で、高さの比は $\mathrm{PE}:\mathrm{AE}=1:3$。よって $\frac13$ 倍。<br><b>ポイント</b>：面積比は「共通な底辺」を探して高さの比に、高さの比は線分の比に直す。"},
 {"lv": "C", "tag": "証明", "q": r"$\triangle\mathrm{ABC}$ の内接円が辺 $\mathrm{BC},\ \mathrm{CA},\ \mathrm{AB}$ とそれぞれ点 $\mathrm D,\ \mathrm E,\ \mathrm F$ で接している。<br>(1) 3直線 $\mathrm{AD},\ \mathrm{BE},\ \mathrm{CF}$ は1点で交わることを証明せよ。<br>(2) $\mathrm{AB}=7,\ \mathrm{BC}=8,\ \mathrm{CA}=9$ のとき、(1) の交点を $\mathrm G$ として $\mathrm{AG}:\mathrm{GD}$ を求めよ。",
  "a": r"(1) 略（チェバの定理の逆）　(2) $32:15$",
  "s": r"(1) 1点から円に引いた2本の接線の長さは等しいので $\mathrm{AF}=\mathrm{AE},\ \mathrm{BD}=\mathrm{BF},\ \mathrm{CE}=\mathrm{CD}$。よって $\frac{\mathrm{AF}}{\mathrm{FB}}\cdot\frac{\mathrm{BD}}{\mathrm{DC}}\cdot\frac{\mathrm{CE}}{\mathrm{EA}}=\frac{\mathrm{AF}}{\mathrm{BD}}\cdot\frac{\mathrm{BD}}{\mathrm{CE}}\cdot\frac{\mathrm{CE}}{\mathrm{AF}}=1$。$\mathrm D,\mathrm E,\mathrm F$ はいずれも辺上（内分点）にあるので、チェバの定理の逆により3直線は1点で交わる。■<br>(2) 接線の長さから $\mathrm{BD}=\mathrm{BF}=3,\ \mathrm{CD}=\mathrm{CE}=5,\ \mathrm{AE}=\mathrm{AF}=4$。$\triangle\mathrm{ABD}$ と直線 $\mathrm{FC}$（$\mathrm G$ を通る）にメネラウスの定理：$\frac{\mathrm{AF}}{\mathrm{FB}}\cdot\frac{\mathrm{BC}}{\mathrm{CD}}\cdot\frac{\mathrm{DG}}{\mathrm{GA}}=1$ より $\frac43\cdot\frac85\cdot\frac{\mathrm{DG}}{\mathrm{GA}}=1$、$\frac{\mathrm{DG}}{\mathrm{GA}}=\frac{15}{32}$。よって $\mathrm{AG}:\mathrm{GD}=32:15$。<br><b>ポイント</b>：3直線が1点で交わることの証明は「チェバの定理の逆」。比の積が $1$ になることに加えて、分点がどこにあるか（内分か外分か）にも触れる。"},
 {"lv": "C", "tag": "証明", "q": r"鋭角三角形 $\mathrm{ABC}$ の垂心を $\mathrm H$ とし、頂点 $\mathrm A$ から辺 $\mathrm{BC}$ に下ろした垂線と $\mathrm{BC}$ の交点を $\mathrm E$、直線 $\mathrm{AE}$ と外接円の $\mathrm A$ 以外の交点を $\mathrm D$ とする。<br>(1) $\mathrm{HE}=\mathrm{ED}$ であることを証明せよ。<br>(2) $\mathrm{BE}=2,\ \mathrm{EC}=3,\ \mathrm{AE}=6$ のとき、$\mathrm{AH}$ の長さを求めよ。",
  "a": r"(1) 略　(2) $\mathrm{AH}=5$",
  "s": r"(1) $\mathrm{BH}$ の延長は $\mathrm{CA}$ に垂直なので、直角三角形を考えて $\angle\mathrm{HBC}=90^\circ-\angle\mathrm C$。一方 $\angle\mathrm{DBC}=\angle\mathrm{DAC}$（弧 $\mathrm{DC}$ に対する円周角）で、直角三角形 $\mathrm{AEC}$ より $\angle\mathrm{DAC}=90^\circ-\angle\mathrm C$。よって $\angle\mathrm{HBE}=\angle\mathrm{DBE}$。<br>$\triangle\mathrm{HBE}$ と $\triangle\mathrm{DBE}$ は、$\mathrm{BE}$ 共通、$\angle\mathrm{BEH}=\angle\mathrm{BED}=90^\circ$、$\angle\mathrm{HBE}=\angle\mathrm{DBE}$ なので合同（1辺とその両端の角）。ゆえに $\mathrm{HE}=\mathrm{ED}$。■" + _fig_orth() + r"(2) 方べきの定理（弦 $\mathrm{AD}$ と $\mathrm{BC}$ が $\mathrm E$ で交わる）より $\mathrm{AE}\cdot\mathrm{ED}=\mathrm{BE}\cdot\mathrm{EC}$、$6\cdot\mathrm{ED}=6$、$\mathrm{ED}=1$。(1) より $\mathrm{HE}=1$、$\mathrm{AH}=6-1=5$。<br>（確認：$\mathrm E$ を原点、$\mathrm B(-2,0),\ \mathrm C(3,0),\ \mathrm A(0,6)$ とすると、$\mathrm B$ を通り $\mathrm{AC}$ に垂直な直線は $y=\frac12(x+2)$ で、$x=0$ のとき $y=1$。$\mathrm H(0,1)$ となり一致する。）<br><b>ポイント</b>：「垂心の $\mathrm{BC}$ に関する対称点は外接円上にある」は頻出の性質。円周角と直角三角形の角で $90^\circ-C$ を2か所に作る。"},
]}}


def verify():
    # A1
    B = Matrix([0, 0]); C = Matrix([5, 0])
    xA = Rational(25+36-16, 10); A = Matrix([xA, sqrt(36-xA**2)])
    assert simplify((A-C).norm()-4) == 0
    D = B+Rational(3, 5)*(C-B)
    assert D[0] == 3
    # 外角の二等分線上の点 E：AB と AC の単位ベクトルの差の方向
    uB = (B-A)/6; uC = (C-A)/4
    dirv = uB-uC
    t = symbols("t")
    tE = solve((A+t*dirv)[1], t)[0]
    E = A+tE*dirv
    assert simplify(E[0]-15) == 0 and simplify(E[0]-C[0]-10) == 0 and simplify(E[0]-D[0]-12) == 0
    # A2: 角度から座標を作って確認
    Aang, Bang, Cang = rad(50), rad(60), rad(70)
    PB = Matrix([0, 0]); PC = Matrix([1, 0])
    c = sin(Cang)/sin(Aang)
    PA = Matrix([c*cos(Bang), c*sin(Bang)])
    a_, b_, c_ = (PB-PC).norm(), (PA-PC).norm(), (PA-PB).norm()
    I = (a_*PA+b_*PB+c_*PC)/(a_+b_+c_)
    ang = lambda P, Q, R: N(acos(((Q-P).dot(R-P))/((Q-P).norm()*(R-P).norm()))*180/pi)
    assert abs(ang(I, PB, PC)-115) < 1e-9
    x, y = symbols("x y")
    O = Matrix([Rational(1, 2), solve((Rational(1, 2)-PA[0])**2+(y-PA[1])**2-(Rational(1, 4)+y**2), y)[0]])
    assert abs(ang(O, PB, PC)-100) < 1e-9
    # 垂心：B から AC に垂直、C から AB に垂直
    H = Matrix([x, y])
    sH = solve([(H-PB).dot(PC-PA), (H-PC).dot(PB-PA)], [x, y])
    H = Matrix([sH[x], sH[y]])
    assert abs(ang(H, PB, PC)-130) < 1e-9
    # A3
    PD = Rational(3*8, 4)
    assert PD == 6 and PD-4 == 2 and sqrt(3*8) == 2*sqrt(6)
    # A4: 座標で
    A = Matrix([0, 0]); B = Matrix([6, 0]); C = Matrix([1, 5])
    R_ = A+Rational(2, 3)*(B-A); Q = A+Rational(3, 5)*(C-A)
    s, u = symbols("s u")
    so = solve(list(B+s*(Q-B)-(C+u*(R_-C))), [s, u])
    assert so[s]/(1-so[s]) == Rational(5, 4)
    O = B+so[s]*(Q-B)
    so2 = solve(list(s*O-(B+u*(C-B))), [s, u])
    assert so2[u]/(1-so2[u]) == Rational(3, 4)
    # B1: 外接円と接線を座標で
    B = Matrix([0, 0]); C = Matrix([4, 0])
    xA = Rational(16+4-9, 8); A = Matrix([xA, sqrt(4-xA**2)])
    assert simplify((A-C).norm()-3) == 0
    cy = symbols("cy")
    Oc = Matrix([2, solve((2-A[0])**2+(cy-A[1])**2-(4+cy**2), cy)[0]])
    # 接線：A を通り OA に垂直。y=0 との交点
    tt = solve((A+t*Matrix([-(A-Oc)[1], (A-Oc)[0]]))[1], t)[0]
    T = A+tt*Matrix([-(A-Oc)[1], (A-Oc)[0]])
    assert simplify(T[0]+Rational(16, 5)) == 0  # B の左側（B 側の延長上）
    assert simplify((T-A).norm()-Rational(24, 5)) == 0
    assert Rational(16, 5)*Rational(36, 5) == Rational(24, 5)**2
    # B2
    a, b, c = 8, 9, 7
    BD = Rational(c+a-b, 2)
    assert BD == 3
    S = sqrt(12*5*4*3)
    assert simplify(S-12*sqrt(5)) == 0 and simplify(S/12-sqrt(5)) == 0
    B = Matrix([0, 0]); C = Matrix([8, 0])
    xA = Rational(64+49-81, 16); A = Matrix([xA, sqrt(49-xA**2)])
    I = (a*A+b*B+c*C)/(a+b+c)
    assert simplify(I[1]-sqrt(5)) == 0 and simplify(I[0]-3) == 0
    E = Matrix([Rational(7, 2), 0])
    assert simplify((A-I).norm()-2*(I-E).norm()) == 0
    # E が AI 上にあること
    assert simplify((I-A)[0]*(E-A)[1]-(I-A)[1]*(E-A)[0]) == 0
    # B3
    assert sqrt(81-9) == 6*sqrt(2) and sqrt(81-49) == 4*sqrt(2) and 9 > 5+2
    # B4: 正二十面体から切頂二十面体を組み立てて数える
    import math
    ph = (1+math.sqrt(5))/2
    V = []
    for a1 in (1, -1):
        for b1 in (ph, -ph):
            V += [(0, a1, b1), (a1, b1, 0), (b1, 0, a1)]
    dist = lambda p, q: math.dist(p, q)
    E0 = [(i, j) for i, j in combinations(range(12), 2) if abs(dist(V[i], V[j])-2) < 1e-9]
    nb = {i: {j for e in E0 for j in e if i in e and j != i} for i in range(12)}
    F0 = [t3 for t3 in combinations(range(12), 3) if all(abs(dist(V[p], V[q])-2) < 1e-9 for p, q in combinations(t3, 2))]
    assert len(E0) == 30 and len(F0) == 20
    tv = [(i, j) for i in range(12) for j in nb[i]]  # 頂点 i の近くで辺 ij 上の点
    faces = [frozenset((i, j) for j in nb[i]) for i in range(12)]  # 五角形
    for p, q, r in F0:
        faces.append(frozenset([(p, q), (q, p), (q, r), (r, q), (r, p), (p, r)]))  # 六角形
    edges = set(frozenset([(i, j), (j, i)]) for i, j in E0)
    for i in range(12):
        for j, k in combinations(nb[i], 2):
            if k in nb[j]:
                edges.add(frozenset([(i, j), (i, k)]))
    nv, ne, nf = len(tv), len(edges), len(faces)
    assert (nv, ne, nf) == (60, 90, 32) and nv-ne+nf == 2
    assert sum(1 for f in faces if len(f) == 5) == 12 and sum(1 for f in faces if len(f) == 6) == 20
    space = sum(1 for p, q in combinations(tv, 2) if not any(p in f and q in f for f in faces))
    assert space == 1440 and math.comb(60, 2)-90-(12*5+20*9) == 1440
    # B5
    A = Matrix([0, 0]); B = Matrix([6, 0]); C = Matrix([1, 5])
    D = A+Rational(1, 3)*(B-A); E = B+Rational(3, 4)*(C-B)
    so = solve(list(A+s*(E-A)-(C+u*(D-C))), [s, u])
    assert so[s]/(1-so[s]) == 2 and so[u]/(1-so[u]) == 1
    P = A+so[s]*(E-A)
    ar = lambda p, q, r: Abs(Matrix.hstack(q-p, r-p).det())/2
    assert ar(P, B, C)/ar(A, B, C) == Rational(1, 3)
    # C1
    B = Matrix([0, 0]); C = Matrix([8, 0])
    xA = Rational(64+49-81, 16); A = Matrix([xA, sqrt(49-xA**2)])
    D = Matrix([3, 0]); Ee = C+Rational(5, 9)*(A-C); F = B+Rational(3, 7)*(A-B)
    I = (8*A+9*B+7*C)/24
    for Pt, P1, P2 in [(D, B, C), (Ee, C, A), (F, A, B)]:  # 接点は内心からの垂線の足
        assert simplify((I-Pt).dot(P2-P1)) == 0
    so = solve(list(A+s*(D-A)-(B+u*(Ee-B))), [s, u])
    G = A+so[s]*(D-A)
    assert simplify(so[s]/(1-so[s])-Rational(32, 15)) == 0
    # G が CF 上にもあること
    assert simplify((G-C)[0]*(F-C)[1]-(G-C)[1]*(F-C)[0]) == 0
    # C2
    A = Matrix([0, 6]); B = Matrix([-2, 0]); C = Matrix([3, 0])
    H = Matrix([x, y])
    sH = solve([(H-B).dot(C-A), (H-C).dot(B-A)], [x, y])
    assert (sH[x], sH[y]) == (0, 1)
    assert all((Q-A).dot(R-A) > 0 for Q, R in [(B, C)]) and (A-B).dot(C-B) > 0 and (A-C).dot(B-C) > 0
    Oc = Matrix([Rational(1, 2), Rational(5, 2)])
    assert (Oc-A).dot(Oc-A) == (Oc-B).dot(Oc-B) == (Oc-C).dot(Oc-C) == (Oc-Matrix([0, -1])).dot(Oc-Matrix([0, -1]))
    assert 6-1 == 5
