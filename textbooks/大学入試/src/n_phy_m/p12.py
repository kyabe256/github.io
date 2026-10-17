"""問題集 第12章 音波。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
from math import sin as _sin, cos as _cos, atan2 as _atan2
from sympy import *


# ---------------- 図 ----------------
def _svg(w, h, body):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(body) + "</svg>"

def _t(x, y, s, size=11, anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}">{s}</text>'

def _ln(x1, y1, x2, y2, w=1.0, dash="", col="#222"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'

def _arrow(x1, y1, x2, y2, w=1.1, col="#222", hs=6.0):
    a = _atan2(y2 - y1, x2 - x1)
    bx, by = x2 - hs * _cos(a), y2 - hs * _sin(a)
    px, py = 0.42 * hs * _sin(a), -0.42 * hs * _cos(a)
    return (_ln(x1, y1, bx, by, w, col=col) +
            f'<polygon points="{x2:.1f},{y2:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{col}"/>')

def _curve(pts, w=1.6, col="#1d4e89"):
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="{col}" stroke-width="{w}"/>'

def _dot(x, y, r=2.6, col="#222"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'

I = lambda s: f'<tspan font-family="Liberation Serif,serif" font-style="italic" font-size="12.5">{s}</tspan>'


def _fig_tube():
    """気柱共鳴の実験。水面が 2 回目の共鳴位置（50.5 cm）にある状態。1 回目の位置（16.5 cm）を破線で示す。縮尺 2.4 px/cm。"""
    k, x1, x2, top = 2.4, 70, 100, 30
    Y = lambda cm: top + k * cm
    b = [f'<rect x="{x1}" y="{Y(50.5):.1f}" width="{x2-x1}" height="{Y(70)-Y(50.5):.1f}" fill="#cfe0f3"/>',
         _ln(x1, Y(50.5), x2, Y(50.5), 1.0, "", "#1d4e89"),
         _ln(x1, top, x1, Y(70), 1.3), _ln(x2, top, x2, Y(70), 1.3), _ln(x1, Y(70), x2, Y(70), 1.3),
         _t((x1 + x2) / 2, Y(61) + 4, "水", 10),
         _ln(x1 - 4, Y(16.5), x2 + 4, Y(16.5), 1.0, "4,2", "#1d4e89"),
         _t(x1 - 6, Y(16.5) + 4, "1回目の水面", 10, "end"), _t(x1 - 6, Y(50.5) + 4, "2回目の水面", 10, "end")]
    fx = (x1 + x2) / 2
    b += [_ln(fx - 6, 4, fx - 6, 18, 2), _ln(fx + 6, 4, fx + 6, 18, 2), _ln(fx - 6, 18, fx + 6, 18, 2), _ln(fx, 18, fx, 24, 2),
          _t(fx + 14, 14, "おんさ（500 Hz）", 10, "start")]
    for cm, xa in [(16.5, x2 + 16), (50.5, x2 + 62)]:
        b.append(_arrow(xa, Y(cm), xa, top, 0.9, hs=5) + _arrow(xa, top, xa, Y(cm), 0.9, hs=5))
        b.append(_t(xa + 4, (top + Y(cm)) / 2 + 4, f"{cm} cm", 10, "start"))
    b.append(_ln(x2, top, x2 + 70, top, 0.6, "2,2", "#666"))
    b.append(_t(x1 - 6, top + 4, "管口", 10, "end"))
    return _svg(250, Y(70) + 6, b)


def _fig_doppler():
    """直線 ℓ 上を進む音源 S と、ℓ から d 離れた観測者 O。"""
    yl, sx, hx, oy = 34, 70, 210, 134
    b = [_ln(14, yl, 320, yl, 1.1), _t(316, yl - 6, "ℓ", 12),
         _ln(hx, yl, hx, oy, 0.9, "4,3", "#666"), _ln(sx, yl, hx, oy, 1.0, "", "#1d4e89"),
         _dot(sx, yl, 4.0, "#c0392b"), _dot(hx, yl, 2.4), _dot(hx, oy, 4.0, "#1d4e89"),
         _t(sx, yl - 9, "S"), _t(hx + 9, yl - 6, "H"), _t(hx + 12, oy + 4, "O"),
         _arrow(sx + 2, yl - 18, sx + 50, yl - 18, 1.3), _t(sx + 58, yl - 14, I("u"), 11, "start"),
         _t(hx + 8, (yl + oy) / 2 + 4, I("d"), 11, "start")]
    ang = _atan2(oy - yl, hx - sx)
    r = 26
    arc = [(sx + r * _cos(ang * k / 20), yl + r * _sin(ang * k / 20)) for k in range(21)]
    b.append(_curve(arc, 0.9, "#222"))
    b.append(_t(sx + 36 * _cos(ang / 2), yl + 36 * _sin(ang / 2) + 5, I("θ")))
    b.append(_ln(hx, yl + 10, hx + 10, yl + 10, 0.8) + _ln(hx + 10, yl, hx + 10, yl + 10, 0.8))
    return _svg(330, 150, b)


FIG_B1 = _fig_tube()
FIG_C1 = _fig_doppler()

CH = {12: {
"goal": r"音速・波長・振動数の関係と、弦・気柱の固有振動、うなり、ドップラー効果を、図と式の両方で処理できるようにする。",
"items": [
 {"lv": "A", "tag": "基本計算", "q": r"気温 $t\,[^\circ\mathrm C]$ における空気中の音速を $V=331.5+0.6t\,[\mathrm{m/s}]$ とする。<br>(1) 気温 $20^\circ\mathrm C$ での音速を求めよ。<br>(2) このとき、崖に向かって声を出したところ、$1.20\,\mathrm s$ 後にこだまが聞こえた。崖までの距離を求めよ。<br>(3) このとき、振動数 $440\,\mathrm{Hz}$ の音の波長を求めよ。",
  "a": r"(1) $343.5\,\mathrm{m/s}$　(2) $206\,\mathrm m$　(3) $0.781\,\mathrm m$",
  "s": r"(1) $V=331.5+0.6\times20=343.5\,\mathrm{m/s}$。<br>(2) 音は崖まで往復するので、距離は $\dfrac{343.5\times1.20}{2}\fallingdotseq206\,\mathrm m$。<br>(3) $\lambda=\dfrac Vf=\dfrac{343.5}{440}\fallingdotseq0.781\,\mathrm m$。<br><b>ポイント</b>：こだまの問題は「往復」に注意。音速は温度で変わるが、振動数は音源で決まる。"},
 {"lv": "A", "tag": "うなり", "q": r"振動数 $440\,\mathrm{Hz}$ のおんさ A と、振動数のわからないおんさ B を同時に鳴らすと、毎秒 3 回のうなりが聞こえた。B の脚に小さなおもりをつけて振動数をわずかに下げてから同時に鳴らすと、うなりは増えて毎秒 5 回になった。<br>(1) おもりをつける前の B の振動数を求めよ。<br>(2) おもりをつけた後の B の振動数を求めよ。",
  "a": r"(1) $437\,\mathrm{Hz}$　(2) $435\,\mathrm{Hz}$",
  "s": r"(1) うなりの回数は振動数の差なので、B は $440\pm3$、すなわち $443\,\mathrm{Hz}$ か $437\,\mathrm{Hz}$。$443\,\mathrm{Hz}$ をわずかに下げると $440\,\mathrm{Hz}$ に近づき、うなりは減るはず。うなりが増えたので B は $437\,\mathrm{Hz}$。<br>(2) $440-f'=5$ より $f'=435\,\mathrm{Hz}$。<br><b>ポイント</b>：うなりの回数 $|f_1-f_2|$ からは差しかわからない。どちらが高いかは「振動数を変えたときにうなりが増えるか減るか」で決める。"},
 {"lv": "A", "tag": "弦の振動", "q": r"長さ $0.60\,\mathrm m$ の弦の両端を固定し、基本振動の振動数が $200\,\mathrm{Hz}$ になるように張った。弦を伝わる波の速さは $v=\sqrt{\dfrac S\rho}$（$S$：張力、$\rho$：線密度）で表される。<br>(1) 基本振動の波長と、弦を伝わる波の速さを求めよ。<br>(2) 3 倍振動の振動数と、そのときの腹の数を答えよ。<br>(3) 弦の張力を 4 倍にすると、基本振動数はいくらになるか。",
  "a": r"(1) $1.2\,\mathrm m$、$240\,\mathrm{m/s}$　(2) $600\,\mathrm{Hz}$、腹 3 個　(3) $400\,\mathrm{Hz}$",
  "s": r"(1) 基本振動は両端が節で腹が 1 つ。弦の長さが半波長なので $\lambda=2\times0.60=1.2\,\mathrm m$。$v=f\lambda=200\times1.2=240\,\mathrm{m/s}$。<br>(2) $m$ 倍振動では $L=m\cdot\dfrac{\lambda}2$、$f_m=\dfrac{mv}{2L}=mf_1$。3 倍振動は $600\,\mathrm{Hz}$ で腹は 3 個。<br>(3) 張力 4 倍で $v$ は $\sqrt4=2$ 倍。波長は弦の長さで決まり変わらないので、$f$ も 2 倍の $400\,\mathrm{Hz}$。<br><b>ポイント</b>：弦では「波長は長さで決まる、速さは張力と線密度で決まる」。振動数は $f=\dfrac v\lambda$ で結ぶ。"},
 {"lv": "A", "tag": "気柱", "q": r"長さ $0.50\,\mathrm m$ の管がある。音速を $340\,\mathrm{m/s}$ とし、開口端補正は無視する。<br>(1) 一端を閉じた閉管にしたとき、基本振動数と、その次に高い固有振動数を求めよ。<br>(2) 両端を開いた開管にしたとき、基本振動数と 2 倍振動の振動数を求めよ。",
  "a": r"(1) $170\,\mathrm{Hz}$、$510\,\mathrm{Hz}$　(2) $340\,\mathrm{Hz}$、$680\,\mathrm{Hz}$",
  "s": r"(1) 閉管では閉端が節、開口端が腹。$L=(2m-1)\dfrac\lambda4$ より $f=\dfrac{(2m-1)V}{4L}$。基本振動は $\dfrac{340}{4\times0.50}=170\,\mathrm{Hz}$、次は 3 倍振動の $510\,\mathrm{Hz}$（閉管に偶数倍振動はない）。<br>(2) 開管では両端が腹。$L=m\dfrac\lambda2$ より $f=\dfrac{mV}{2L}$。基本振動 $340\,\mathrm{Hz}$、2 倍振動 $680\,\mathrm{Hz}$。<br><b>ポイント</b>：閉管は奇数倍振動だけ、開管はすべての整数倍振動がある。図に「節と腹」を描いてから $\lambda$ を決めると間違えない。"},
 {"lv": "B", "tag": "実験・気柱の共鳴", "q": r"図のように、水を入れたガラス管の管口付近で振動数 $500\,\mathrm{Hz}$ のおんさを鳴らしながら、水面を管口から下げていった。管口から水面までの距離が $16.5\,\mathrm{cm}$ のときに 1 回目、$50.5\,\mathrm{cm}$ のときに 2 回目の共鳴が起こった。" + FIG_B1 + r"(1) 音の波長と音速を求めよ。<br>(2) 開口端補正を求めよ。<br>(3) さらに水面を下げていくと、次に共鳴が起こるのは管口から何 cm のところか。<br>(4) 2 回目の共鳴のとき、管内で空気の密度の変化が最も大きい位置を、管口からの距離ですべて答えよ。",
  "a": r"(1) $0.680\,\mathrm m$、$340\,\mathrm{m/s}$　(2) $0.5\,\mathrm{cm}$　(3) $84.5\,\mathrm{cm}$　(4) $16.5\,\mathrm{cm}$ と $50.5\,\mathrm{cm}$",
  "s": r"(1) 隣り合う共鳴位置の差は半波長。$\dfrac\lambda2=50.5-16.5=34.0\,\mathrm{cm}$ より $\lambda=68.0\,\mathrm{cm}=0.680\,\mathrm m$。$V=f\lambda=500\times0.680=340\,\mathrm{m/s}$。<br>(2) 1 回目の共鳴では、水面（節）から管口の少し外側の腹までが $\dfrac\lambda4=17.0\,\mathrm{cm}$。開口端補正は $17.0-16.5=0.5\,\mathrm{cm}$。<br>(3) さらに半波長下の $50.5+34.0=84.5\,\mathrm{cm}$。<br>(4) 密度の変化が最も大きいのは変位の節。2 回目の共鳴では、水面（$50.5\,\mathrm{cm}$）とそこから半波長上の $16.5\,\mathrm{cm}$ の位置が節。<br><b>ポイント</b>：開口端補正は差をとれば消える。「差 $=\dfrac\lambda2$」で波長を出し、補正は最後に求める。密度（圧力）変化が大きいのは変位の節である。"},
 {"lv": "B", "tag": "ドップラー効果", "q": r"振動数 $576\,\mathrm{Hz}$ の音を出す救急車が、静止している観測者に向かって一直線上を速さ $20\,\mathrm{m/s}$ で近づき、通り過ぎて遠ざかっていく。音速は $340\,\mathrm{m/s}$、風はないものとする。<br>(1) 救急車の前方での音の波長を求めよ。<br>(2) 近づいてくるときに観測者が聞く音の振動数を求めよ。<br>(3) 救急車の後方での音の波長と、遠ざかるときに観測者が聞く音の振動数を求めよ。",
  "a": r"(1) $0.556\,\mathrm m$　(2) $612\,\mathrm{Hz}$　(3) $0.625\,\mathrm m$、$544\,\mathrm{Hz}$",
  "s": r"(1) 1 s の間に音源は $576$ 個の波を出し、前方ではそれが $(340-20)\,\mathrm m$ の中に並ぶ。$\lambda=\dfrac{340-20}{576}\fallingdotseq0.556\,\mathrm m$。<br>(2) $f=\dfrac{V}{\lambda}=\dfrac{340}{340-20}\times576=612\,\mathrm{Hz}$。<br>(3) 後方では $\lambda'=\dfrac{340+20}{576}=0.625\,\mathrm m$、$f'=\dfrac{340}{0.625}=544\,\mathrm{Hz}$。<br><b>ポイント</b>：音源が動くと<b>波長</b>が変わる。$f=\dfrac{V-v_{\text{観測者}}}{V-v_{\text{音源}}}f_0$（音源から観測者への向きを正）にあてはめる前に、「1 s 間に出た波が何 m に並ぶか」を考えると符号を間違えない。"},
 {"lv": "B", "tag": "ドップラー効果・反射", "q": r"静止した音源から振動数 $840\,\mathrm{Hz}$ の音を出し、音源に向かって速さ $4.0\,\mathrm{m/s}$ で近づいてくる大きな壁に当てる。音源の位置で、音源からの直接音と壁からの反射音を同時に聞く。音速は $340\,\mathrm{m/s}$ とする。<br>(1) 壁が受ける音の振動数を求めよ（有効数字 3 桁）。<br>(2) 音源の位置で聞く反射音の振動数を求めよ。<br>(3) 1 s あたりのうなりの回数を求めよ。<br>(4) うなりが毎秒 10 回になるのは、壁の速さがいくらのときか。",
  "a": r"(1) $850\,\mathrm{Hz}$　(2) $860\,\mathrm{Hz}$　(3) $20$ 回　(4) $2.0\,\mathrm{m/s}$",
  "s": r"(1) 壁は「近づく観測者」：$f_1=\dfrac{340+4.0}{340}\times840\fallingdotseq850\,\mathrm{Hz}$。<br>(2) 壁は受けた音を、そのまま「近づく音源」として出す：$f_2=\dfrac{340}{340-4.0}f_1=\dfrac{344}{336}\times840=860\,\mathrm{Hz}$。<br>(3) $860-840=20$ 回。<br>(4) 壁の速さを $v$ とすると $\dfrac{340+v}{340-v}\times840-840=\dfrac{2v}{340-v}\times840=10$。$1690v=3400$ より $v\fallingdotseq2.0\,\mathrm{m/s}$。<br><b>ポイント</b>：反射は「観測者として受け、音源として出す」の 2 段階。$v\ll V$ ならうなりは $\fallingdotseq\dfrac{2v}{V}f_0$ で、反射体の速さの測定（スピードガン）の原理になる。"},
 {"lv": "B", "tag": "実験・弦の共振", "q": r"弦の一端を、弦に垂直な向きに振動数 $50\,\mathrm{Hz}$ で振動する振動子に結び、他端は $0.90\,\mathrm m$ 離れた滑車にかけて質量 $M$ のおもりをつるした。振動子の位置は節とみなせる。弦の線密度は $4.9\times10^{-4}\,\mathrm{kg/m}$、重力加速度の大きさは $9.8\,\mathrm{m/s^2}$、弦を伝わる波の速さは $v=\sqrt{\dfrac S\rho}$（$S$：張力、$\rho$：線密度）とする。<br>振動子と滑車の間に腹が 3 つの定常波ができた。<br>(1) 定常波の波長と、弦を伝わる波の速さを求めよ。<br>(2) 弦の張力とおもりの質量 $M$ を求めよ。<br>(3) おもりだけを取りかえて腹が 1 つの定常波をつくるには、何 kg のおもりにすればよいか。<br>(4) おもりを $M$ のままにして、振動子の振動数だけを変えて腹が 2 つの定常波をつくるには、振動数をいくらにすればよいか。",
  "a": r"(1) $0.60\,\mathrm m$、$30\,\mathrm{m/s}$　(2) $0.44\,\mathrm N$、$4.5\times10^{-2}\,\mathrm{kg}$　(3) $0.41\,\mathrm{kg}$　(4) $33\,\mathrm{Hz}$",
  "s": r"(1) 腹が 3 つなので $0.90=3\times\dfrac\lambda2$、$\lambda=0.60\,\mathrm m$。$v=f\lambda=50\times0.60=30\,\mathrm{m/s}$。<br>(2) $S=\rho v^2=4.9\times10^{-4}\times30^2\fallingdotseq0.44\,\mathrm N$。$Mg=S$ より $M=\dfrac{0.441}{9.8}=4.5\times10^{-2}\,\mathrm{kg}$。<br>(3) 振動数は振動子で決まり $50\,\mathrm{Hz}$ のまま。腹 1 つでは $\lambda=1.8\,\mathrm m$、$v=90\,\mathrm{m/s}$ で、$v$ が 3 倍なので張力は 9 倍。$9M=0.405\fallingdotseq0.41\,\mathrm{kg}$。<br>(4) $v=30\,\mathrm{m/s}$ のまま、腹 2 つでは $\lambda=0.90\,\mathrm m$。$f=\dfrac{30}{0.90}\fallingdotseq33\,\mathrm{Hz}$。<br><b>ポイント</b>：何が一定かを最初に決める。おもりを変えるとき一定なのは振動数、振動数を変えるとき一定なのは速さ（張力）。腹の数 $n$ のとき $L=n\dfrac\lambda2$。"},
 {"lv": "B", "tag": "ドップラー効果・観測者", "q": r"同じ振動数 $680\,\mathrm{Hz}$ の音を同位相で出す 2 つのスピーカー A、B が、一直線上で向かい合って静止している。AB 間を、観測者が A から B に向かって速さ $2.0\,\mathrm{m/s}$ で動く。音速は $340\,\mathrm{m/s}$ とする。<br>(1) 観測者が聞く A からの音と B からの音の振動数を、それぞれ求めよ。<br>(2) 観測者が聞くうなりは毎秒何回か。<br>(3) AB 間には、A と B の音による定常波ができている。観測者が 1 s 間に通過する節の数を求め、(2) の結果と比べよ。",
  "a": r"(1) A：$676\,\mathrm{Hz}$、B：$684\,\mathrm{Hz}$　(2) $8$ 回　(3) $8$ 個で、うなりの回数と一致する",
  "s": r"(1) A からの音に対しては遠ざかる観測者：$\dfrac{340-2.0}{340}\times680=676\,\mathrm{Hz}$。B からの音には近づく観測者：$\dfrac{340+2.0}{340}\times680=684\,\mathrm{Hz}$。<br>(2) $684-676=8$ 回。<br>(3) 波長 $\lambda=\dfrac{340}{680}=0.50\,\mathrm m$。定常波の節の間隔は $\dfrac\lambda2=0.25\,\mathrm m$ で、1 s 間に $\dfrac{2.0}{0.25}=8$ 個の節を通過する。節を通るたびに音が弱くなるので、これが毎秒 8 回のうなりとして聞こえる。<br><b>ポイント</b>：観測者が動くと、波長は変わらず「観測者に対する音の速さ」が $V\pm v$ になる。同じ現象を「振動数の差」と「定常波の節の通過」の 2 通りで説明できる。"},
 {"lv": "C", "tag": "総合・斜めのドップラー効果", "q": r"図のように、振動数 $f_0=900\,\mathrm{Hz}$ の音を出す音源 S が、直線 ℓ 上を一定の速さ $u=34\,\mathrm{m/s}$ で右向きに進む。観測者 O は ℓ から距離 $d=170\,\mathrm m$ 離れた位置に静止しており、O から ℓ に下ろした垂線の足を H とする。音速は $V=340\,\mathrm{m/s}$、風はない。" + FIG_C1 + r"(1) S が H の左方の十分遠くにあるときに出した音を、O は何 Hz で聞くか。<br>(2) S の速度の向きと、S から O へ向かう向きとのなす角が $\theta$ のときに S が出した音を、O は $f=\dfrac{V}{V-u\cos\theta}f_0$ の振動数で聞く。その理由を説明し、$\theta=60^\circ$ のときの $f$ を求めよ。<br>(3) O がちょうど振動数 $900\,\mathrm{Hz}$ の音を聞く瞬間、S は H からどちら側に何 m 離れた位置にあるか。<br>(4) S が H の右方の十分遠くにあるときに出した音を、O は何 Hz で聞くか。",
  "a": r"(1) $1000\,\mathrm{Hz}$　(2) 理由は解説、$947\,\mathrm{Hz}$　(3) H の右側（通過した後の側）に $17\,\mathrm m$　(4) $818\,\mathrm{Hz}$",
  "s": r"(1) S は O の方へまっすぐ近づくとみなせる（$\theta\to0$）。$f=\dfrac{340}{340-34}\times900=1000\,\mathrm{Hz}$。<br>(2) 振動数を決めるのは、S から O へ向かう向きに並ぶ波の間隔である。S が 1 つの波を出してから次の波を出すまでの短い時間 $\dfrac1{f_0}$ に、S は O へ向かう向きに $u\cos\theta\cdot\dfrac1{f_0}$ だけ近づく（速度の SO 方向の成分が $u\cos\theta$）。よって O へ向かう音の波長は $\lambda=\dfrac{V-u\cos\theta}{f_0}$、$f=\dfrac V\lambda=\dfrac{V}{V-u\cos\theta}f_0$。<br>$\theta=60^\circ$ のとき $f=\dfrac{340}{340-17}\times900\fallingdotseq947\,\mathrm{Hz}$。<br>(3) $f=f_0$ となるのは $\cos\theta=0$、すなわち S が H にあるときに出した音。その音が O に届くまでの時間は $\dfrac dV=\dfrac{170}{340}=0.50\,\mathrm s$ で、その間に S は $34\times0.50=17\,\mathrm m$ 進む。よって O が $900\,\mathrm{Hz}$ を聞く瞬間、S は H を通り過ぎて右側に $17\,\mathrm m$ の位置にある。<br>(4) $\theta\to180^\circ$ で $f=\dfrac{340}{340+34}\times900\fallingdotseq818\,\mathrm{Hz}$。<br><b>ポイント</b>：斜めのドップラー効果では、速度の「音源→観測者方向の成分」だけが効く。どの瞬間に<b>出した</b>音を、いつ<b>聞く</b>のかを区別する。"},
 {"lv": "C", "tag": "総合・風とドップラー効果", "q": r"$x$ 軸上の原点に、振動数 $f_0=700\,\mathrm{Hz}$ の音源 S があり、$x\gt0$ の位置に観測者 O がいる。空気に対する音速は $V=340\,\mathrm{m/s}$ で、$x$ 軸の正の向き（S から O の向き）に一様な風が速さ $w=10\,\mathrm{m/s}$ で吹いている。速さはすべて地面に対する値で与えてある。<br>(1) S、O がともに静止しているとき、地面に対する $x$ 軸正の向きの音速、音の波長、O が聞く振動数を求めよ。<br>(2) S が $x$ 軸の正の向きに速さ $u=20\,\mathrm{m/s}$ で動き、O が静止しているとき、S の前方の波長と、O が聞く振動数を求めよ（有効数字 3 桁）。<br>(3) (2) の状態で、さらに O が S に向かって速さ $15\,\mathrm{m/s}$ で動くとき、O が聞く振動数を求めよ。<br>(4) 空気とともに動く立場（風のない立場）で考えると、S と O の速さはそれぞれいくらに見えるか。それを用いて (3) の結果を確かめよ。",
  "a": r"(1) $350\,\mathrm{m/s}$、$0.500\,\mathrm m$、$700\,\mathrm{Hz}$　(2) $0.471\,\mathrm m$、$742\,\mathrm{Hz}$　(3) $774\,\mathrm{Hz}$　(4) S は O に向かって $10\,\mathrm{m/s}$、O は S に向かって $25\,\mathrm{m/s}$。$\dfrac{340+25}{340-10}\times700\fallingdotseq774\,\mathrm{Hz}$ で一致",
  "s": r"(1) 音は空気に対して $V$ で進み、空気が地面に対して $w$ で動くので、地面に対しては $V+w=350\,\mathrm{m/s}$。$\lambda=\dfrac{350}{700}=0.500\,\mathrm m$。S も O も静止していれば、O には 1 s 間に 700 個の波が届くので $700\,\mathrm{Hz}$（風だけでは振動数は変わらない）。<br>(2) 1 s 間に出た 700 個の波は、前方では $(350-20)\,\mathrm m$ の中に並ぶ。$\lambda=\dfrac{330}{700}\fallingdotseq0.471\,\mathrm m$。O に対する音の速さは $350\,\mathrm{m/s}$ なので $f=\dfrac{350}{\lambda}=\dfrac{350}{330}\times700\fallingdotseq742\,\mathrm{Hz}$。<br>(3) O に対する音の速さは $350+15=365\,\mathrm{m/s}$。$f=\dfrac{365}{330}\times700\fallingdotseq774\,\mathrm{Hz}$。<br>(4) 空気に対して、S は $20-10=10\,\mathrm{m/s}$ で O に近づき、O は $15+10=25\,\mathrm{m/s}$ で S に近づく。風のないときの公式で $\dfrac{V+25}{V-10}f_0=\dfrac{365}{330}\times700$ となり一致する。<br><b>ポイント</b>：風があるときは「音速は空気に対して $V$」を出発点にする。地面から見て $V\pm w$ を使うか、空気の立場に移って速さを読みかえるかのどちらかで統一する。"},
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
    R = Rational
    # A1
    V = R(3315, 10) + R(6, 10) * 20
    assert V == R(3435, 10)
    _sf(V * R(120, 100) / 2, 206, 3); _sf(V / 440, 0.781, 3)
    # A2
    cand = [440 + 3, 440 - 3]
    ok = [fb for fb in cand if abs(440 - (fb - R(1, 2))) > abs(440 - fb)]   # わずかに下げるとうなりが増える
    assert ok == [437] and 440 - 5 == 435
    # A3
    lam = 2 * R(6, 10); v = 200 * lam
    assert lam == R(6, 5) and v == 240 and 3 * 200 == 600 and sqrt(4) * 200 == 400
    # A4
    V, L = 340, R(1, 2)
    assert V / (4 * L) == 170 and 3 * V / (4 * L) == 510 and V / (2 * L) == 340 and 2 * V / (2 * L) == 680
    # B1
    half = R(505 - 165, 10)  # cm
    lam = 2 * half / 100
    assert lam == R(68, 100) and 500 * lam == 340
    assert lam * 100 / 4 - R(165, 10) == R(1, 2)
    assert R(505, 10) + half == R(845, 10) and R(505, 10) - half == R(165, 10)
    # B2
    f0, u, V = 576, 20, 340
    _sf(R(V - u, f0), 0.556, 3)
    assert R(V, V - u) * f0 == 612 and R(V + u, f0) == R(5, 8) and R(V, V + u) * f0 == 544
    # B3
    f0, v, V = 840, R(4), 340
    f1 = (V + v) / V * f0; f2 = V / (V - v) * f1
    _sf(f1, 850, 3)
    assert f2 == 860 and f2 - f0 == 20
    vs = symbols("v", positive=True)
    sol = solve(Eq((V + vs) / (V - vs) * f0 - f0, 10), vs)[0]
    assert sol == R(3400, 1690)
    _sf(sol, 2.0, 2)
    # B4
    f, L, rho, g = 50, R(9, 10), R(49, 100000), R(98, 10)
    lam = 2 * L / 3; v = f * lam; S = rho * v ** 2; M = S / g
    assert lam == R(3, 5) and v == 30 and S == R(441, 1000) and M == R(45, 1000)
    _sf(S, 0.44, 2)
    v1 = f * 2 * L; M1 = rho * v1 ** 2 / g
    assert M1 == 9 * M and M1 == R(405, 1000)
    _sf(M1, 0.41, 2)
    _sf(v / L, 33, 2)
    # B5
    f0, u, V = 680, 2, 340
    fa, fb = R(V - u, V) * f0, R(V + u, V) * f0
    assert fa == 676 and fb == 684 and fb - fa == 8
    assert R(2) / (R(V, f0) / 2) == 8
    # C1
    f0, u, V, d = 900, 34, 340, 170
    th = symbols("theta")
    fth = V / (V - u * cos(th)) * f0
    assert fth.subs(th, 0) == 1000
    _sf(fth.subs(th, pi / 3), 947, 3); _sf(fth.subs(th, pi), 818, 3)
    assert fth.subs(th, pi / 2) == f0 and u * R(d, V) == 17
    # C2
    V, w, f0, u, vo = 340, 10, 700, 20, 15
    assert V + w == 350 and R(V + w, f0) == R(1, 2)
    lam = R(V + w - u, f0)
    _sf(lam, 0.471, 3); _sf((V + w) / lam, 742, 3); _sf((V + w + vo) / lam, 774, 3)
    us, vo_air = u - w, vo + w
    assert R(V + vo_air, V - us) * f0 == (V + w + vo) / lam
