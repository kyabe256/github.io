"""問題集 第7章 遺伝の法則。問題はすべて書き下ろし。verify() は配偶子の列挙による分離比の検算・形式・論述の字数の点検。"""
import re, math
from fractions import Fraction as Fr

G, G2, OR, RD, BL, GR = "#2e6b30", "#56a05a", "#d9701e", "#c0392b", "#1f5f9f", "#555"


def B(s):
    return f'<div class="bun">{s}</div>'


def TB(head, rows, w=False):
    cls = ' class="w"' if w else ""
    h = "<tr>" + "".join(f"<th>{c}</th>" for c in head) + "</tr>"
    r = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table{cls}>{h}{r}</table>"


# ---- 図（座標は計算で出す） ----
def _f(x):
    return ("%.1f" % x).rstrip("0").rstrip(".")


def _t(x, y, s, size=10.5, anchor="start", c="#222", bold=False):
    b = ' font-weight="bold"' if bold else ""
    return f'<text x="{_f(x)}" y="{_f(y)}" font-size="{size}" text-anchor="{anchor}" fill="{c}"{b}>{s}</text>'


def _l(x1, y1, x2, y2, c=GR, w=1, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" stroke="{c}" stroke-width="{w}"{d}/>'


def _pl(pts, c=G, w=1.8, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<polyline points="{" ".join(_f(x) + "," + _f(y) for x, y in pts)}" fill="none" stroke="{c}" stroke-width="{w}"{d}/>'


def _ar(x1, y1, x2, y2, c=GR, w=1.1, hs=5):
    a = math.atan2(y2 - y1, x2 - x1)
    p = [(x2, y2), (x2 - hs * math.cos(a - 0.45), y2 - hs * math.sin(a - 0.45)),
         (x2 - hs * math.cos(a + 0.45), y2 - hs * math.sin(a + 0.45))]
    return (_l(x1, y1, x2 - 0.6 * hs * math.cos(a), y2 - 0.6 * hs * math.sin(a), c, w)
            + f'<polygon points="{" ".join(_f(u) + "," + _f(v) for u, v in p)}" fill="{c}"/>')


def _svg(w, h, parts):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(parts) + "</svg>"


class _Ax:
    """データ座標 → SVG 座標"""
    def __init__(s, x0, y0, w, h, xr, yr):
        s.x0, s.y0, s.w, s.h, s.xr, s.yr = x0, y0, w, h, xr, yr

    def X(s, x):
        return s.x0 + (x - s.xr[0]) / (s.xr[1] - s.xr[0]) * s.w

    def Y(s, y):
        return s.y0 - (y - s.yr[0]) / (s.yr[1] - s.yr[0]) * s.h

    def P(s, pts):
        return [(s.X(a), s.Y(b)) for a, b in pts]

    def frame(s, xl, yl, xt=(), yt=(), grid=True):
        o = []
        for v in xt:
            if grid and v != s.xr[0]:
                o.append(_l(s.X(v), s.y0, s.X(v), s.y0 - s.h, "#d4d4d4", 0.6))
            o.append(_t(s.X(v), s.y0 + 13, _f(v), 10, "middle"))
        for v in yt:
            if grid and v != s.yr[0]:
                o.append(_l(s.x0, s.Y(v), s.x0 + s.w, s.Y(v), "#d4d4d4", 0.6))
            o.append(_t(s.x0 - 4, s.Y(v) + 3.5, _f(v), 10, "end"))
        o += [_ar(s.x0, s.y0, s.x0 + s.w + 12, s.y0), _ar(s.x0, s.y0, s.x0, s.y0 - s.h - 12),
              _t(s.x0 + s.w + 12, s.y0 + 27, xl, 10.5, "end"), _t(s.x0 + 7, s.y0 - s.h - 6, yl, 10.5)]
        return o



from itertools import product
from collections import Counter


def _gam_link(cis, r):
    """2遺伝子 A,B の連鎖。cis=True なら AB/ab、False なら Ab/aB。r は組換え価（Fraction）"""
    par = ["AB", "ab"] if cis else ["Ab", "aB"]
    rec = ["Ab", "aB"] if cis else ["AB", "ab"]
    return {par[0]: (1 - r) / 2, par[1]: (1 - r) / 2, rec[0]: r / 2, rec[1]: r / 2}


def _pheno2(g1, g2):
    """2遺伝子の配偶子分布どうしの交配 → 表現型 [AB] [Ab] [aB] [ab] の割合"""
    out = Counter()
    for (x, p), (y, q) in product(g1.items(), g2.items()):
        ph = ("A" if "A" in x[0] + y[0] else "a") + ("B" if "B" in x[1] + y[1] else "b")
        out[ph] += p * q
    return out


def _fig_ped():
    p = []
    S = 22

    def male(x, y, fill=False, lab=""):
        return (f'<rect x="{x - S / 2}" y="{y - S / 2}" width="{S}" height="{S}" fill="{G if fill else "#fff"}" stroke="#222" stroke-width="1.3"/>'
                + _t(x, y + S / 2 + 13, lab, 10, "middle"))

    def female(x, y, fill=False, lab=""):
        return (f'<circle cx="{x}" cy="{y}" r="{S / 2}" fill="{G if fill else "#fff"}" stroke="#222" stroke-width="1.3"/>'
                + _t(x, y + S / 2 + 13, lab, 10, "middle"))
    y1, y2 = 26, 96
    p += [_l(111, y1, 169, y1, "#222", 1.3), _l(140, y1, 140, y2 - 30, "#222", 1.3), _l(80, y2 - 30, 200, y2 - 30, "#222", 1.3)]
    for x in (80, 140, 200):
        p.append(_l(x, y2 - 30, x, y2 - S / 2, "#222", 1.3))
    p += [male(100, y1, False, ""), female(180, y1, False, ""), _t(78, y1 + 4, "Ⅰ−1", 10, "end"), _t(202, y1 + 4, "Ⅰ−2", 10, "start"),
          female(80, y2, True, "Ⅱ−1"), male(140, y2, False, "Ⅱ−2"), female(200, y2, False, "Ⅱ−3"),
          male(250, 40, False, ""), _t(266, 44, "男性", 10), female(250, 70, False, ""), _t(266, 74, "女性", 10),
          f'<rect x="{250 - 6}" y="{100 - 6}" width="12" height="12" fill="{G}" stroke="#222"/>', _t(266, 104, "発症者", 10)]
    return _svg(320, 132, p)


# 7-10 三点交雑の検定交雑の結果（A−B 10%、B−C 20%、二重乗換え 0.1×0.2）
TP = {"ABC": 360, "abc": 360, "Abc": 40, "aBC": 40, "ABc": 90, "abC": 90, "AbC": 10, "aBc": 10}
TP_SHOW = ["ABc", "abc", "aBC", "AbC", "ABC", "abC", "aBc", "Abc"]   # 表に並べる順（並び順を見せないため）


def _recomb_tp(i, j):
    return Fr(sum(n for g, n in TP.items() if (g[i].isupper()) != (g[j].isupper())), sum(TP.values()))


CH = {7: {
"goal": "分離の法則・独立の法則から交配の結果を予測し、連鎖・組換え価・染色体地図・伴性遺伝・家系図の問題を、配偶子の種類と割合から確実に解けるようにする。",
"items": [
 {"lv": "A", "tag": "一遺伝子雑種",
  "q": "エンドウの種子の形は、丸（優性、遺伝子R）としわ（劣性、遺伝子r）の対立形質である。丸の純系としわの純系を交配してF<sub>1</sub>を得、F<sub>1</sub>を自家受精してF<sub>2</sub>を得た。<br>"
       "(1) F<sub>1</sub>の遺伝子型と表現型を答えよ。<br>(2) F<sub>2</sub>の遺伝子型の比と表現型の比を答えよ。F<sub>2</sub>が800個体のとき、しわの個体は約何個体か。<br>"
       "(3) F<sub>2</sub>の丸の個体のうち、遺伝子型がホモ接合体であるものの割合を求めよ。<br>"
       "(4) F<sub>2</sub>の丸の個体の遺伝子型を調べるために、しわの個体と交配した。このような交配を何というか。また、遺伝子型がRRの場合とRrの場合で、生じる子の表現型の比はそれぞれどうなるか。",
  "a": "(1) Rr、丸　(2) RR：Rr：rr＝1：2：1、丸：しわ＝3：1、約200個体　(3) 1/3　(4) 検定交雑。RRの場合：すべて丸、Rrの場合：丸：しわ＝1：1",
  "s": "(1) 対立遺伝子の一方が優性のとき、ヘテロ接合体Rrは優性の形質（丸）を示す。<br>"
       "(2) F<sub>1</sub>の配偶子はR：r＝1：1（分離の法則）。その組み合わせで RR：Rr：rr＝1：2：1。しわ（rr）は 800×1/4＝200。<br>"
       "(3) 丸（RR＋Rr）3のうちRRは1なので 1/3。<br>"
       "(4) 劣性ホモ（rr）の個体はrの配偶子しかつくらないので、子の表現型の比が、調べたい個体の配偶子の比をそのまま表す。<br>"
       "<b>ポイント</b>：検定交雑の結果＝調べる個体の配偶子の種類と比。連鎖や組換え価の問題でも同じ考え方を使う。"},
 {"lv": "A", "tag": "二遺伝子雑種",
  "q": "エンドウの種子の形（丸R＞しわr）と子葉の色（黄Y＞緑y）は、別々の染色体上にある遺伝子によって決まる。丸・黄の純系（RRYY）としわ・緑の純系（rryy）を交配してF<sub>1</sub>を得た。<br>"
       "(1) F<sub>1</sub>がつくる配偶子の遺伝子型とその比を答えよ。<br>"
       "(2) F<sub>1</sub>を自家受精して得たF<sub>2</sub>の表現型の比を答えよ。また、F<sub>2</sub>が1600個体のとき、しわ・黄の個体は約何個体か。<br>"
       "(3) F<sub>2</sub>のうち、遺伝子型がF<sub>1</sub>と同じ（RrYy）ものの割合を求めよ。<br>"
       "(4) F<sub>1</sub>をしわ・緑の個体と交配したとき、生じる子の表現型の比を答えよ。",
  "a": "(1) RY：Ry：rY：ry＝1：1：1：1　(2) 丸・黄：丸・緑：しわ・黄：しわ・緑＝9：3：3：1、約300個体　(3) 1/4　(4) 丸・黄：丸・緑：しわ・黄：しわ・緑＝1：1：1：1",
  "s": "(1) 2対の遺伝子が別々の染色体上にあると、減数分裂で互いに独立に配偶子に入る（独立の法則）。<br>"
       "(2) 形ごとに 丸：しわ＝3：1、色ごとに 黄：緑＝3：1 で、その積が (3：1)×(3：1)＝9：3：3：1。しわ・黄は 1600×3/16＝300。<br>"
       "(3) Rrになる確率1/2、Yyになる確率1/2で、1/2×1/2＝1/4。<br>"
       "<b>ポイント</b>：独立な2遺伝子は「1遺伝子ずつ分けて考え、確率をかける」。9：3：3：1を毎回書き出す必要はない。"},
 {"lv": "A", "tag": "不完全優性・複対立遺伝子",
  "q": "(1) マルバアサガオの花の色では、赤花の純系と白花の純系を交配すると、F<sub>1</sub>はすべて桃色の花になる。F<sub>2</sub>の表現型の比を答えよ。<br>"
       "(2) ヒトのABO式血液型は、3つの対立遺伝子A、B、Oによって決まり、AとBはOに対して優性、AとBの間には優劣がない。A型の父とB型の母からO型の子が生まれた。父と母の遺伝子型を答えよ。また、この両親から次に生まれる子がAB型である確率を求めよ。<br>"
       "(3) ハツカネズミの毛の色で、黄色の遺伝子Yは黒色の遺伝子yに対して優性であるが、Yをホモにもつ個体は胎児のうちに死ぬ。黄色の個体どうしを交配したとき、生まれてくる子の表現型の比を答えよ。",
  "a": "(1) 赤：桃：白＝1：2：1　(2) 父 AO、母 BO、1/4　(3) 黄色：黒色＝2：1",
  "s": "(1) 赤と白の間に優劣がない（不完全優性）ので、ヘテロ接合体は中間の桃色になり、遺伝子型の比がそのまま表現型の比になる。<br>"
       "(2) O型の子（OO）は両親からOを1つずつ受けつぐので、父はAO、母はBO。子は AB、AO、BO、OO が1/4ずつ。<br>"
       "(3) 黄色の個体はすべてYy。Yy×Yy → YY：Yy：yy＝1：2：1 だが、YYは生まれないので 黄色（Yy）：黒色（yy）＝2：1。<br>"
       "<b>ポイント</b>：3：1からずれた比（1：2：1、2：1）は、不完全優性や致死遺伝子のサイン。"},
 {"lv": "A", "tag": "減数分裂と遺伝子の組み合わせ",
  "q": "(1) 体細胞の染色体数が2n＝8の生物で、乗換えが起こらないとすると、1個体がつくる配偶子の染色体の組み合わせは何通りか。また、同じ両親から生じる受精卵の染色体の組み合わせは何通りか。<br>"
       "(2) ヒト（2n＝46）がつくる配偶子の染色体の組み合わせは何通りか。乗換えは考えず、有効数字2桁で答えよ。<br>"
       "(3) 減数分裂で、相同染色体どうしが分かれて別々の細胞に入るのは、第一分裂と第二分裂のどちらか。また、相同染色体が対合したものを何というか。<br>"
       "(4) (1)(2)で考えなかった乗換えは、減数分裂のどの時期に起こるか。また、乗換えは配偶子の遺伝子の組み合わせにどのような影響をあたえるか。",
  "a": "(1) 16通り、256通り　(2) 約8.4×10<sup>6</sup>通り　(3) 第一分裂、二価染色体　(4) 第一分裂前期。相同染色体の間で遺伝子の組み合わせが変わり、配偶子の遺伝的な多様性がさらに大きくなる。",
  "s": "(1) n＝4組の相同染色体のそれぞれで、父方・母方のどちらが入るか2通り。2<sup>4</sup>＝16。受精卵は 16×16＝256 通り。<br>"
       "(2) 2<sup>23</sup>＝8388608 ≒ 8.4×10<sup>6</sup>。<br>"
       "(4) 二価染色体をつくった相同染色体の間で、染色体の一部が交換される（このとき見られる交差部分をキアズマという）。<br>"
       "<b>ポイント</b>：配偶子の染色体の組み合わせは 2<sup>n</sup> 通り。減数分裂の第一分裂で相同染色体が分かれることが、分離の法則・独立の法則のしくみ。"},
 {"lv": "B", "tag": "計算（組換え価）",
  "q": "ある植物の花の色（紫A＞赤a）と花粉の形（長B＞丸b）について、紫・長の純系（AABB）と赤・丸の純系（aabb）を交配してF<sub>1</sub>を得た。F<sub>1</sub>を赤・丸の個体と交配すると、次の結果を得た。"
       + TB(["表現型", "紫・長", "紫・丸", "赤・長", "赤・丸", "計"], [["個体数", "400", "100", "100", "400", "1000"]])
       + "(1) 遺伝子A（a）とB（b）が同じ染色体上にある（連鎖している）と判断できる理由を答えよ。<br>"
       "(2) AとBの間の組換え価を求めよ。<br>"
       "(3) F<sub>1</sub>を自家受精して得られるF<sub>2</sub>の表現型の比を求めよ。ただし、卵と花粉をつくるときの組換え価はどちらも(2)の値とする。<br>"
       "(4) 紫・丸の純系（AAbb）と赤・長の純系（aaBB）を交配して得たF<sub>1</sub>を、赤・丸の個体と交配したとき、子の表現型の比を求めよ。",
  "a": "(1) 独立している場合の1：1：1：1から大きくずれ、親と同じ組み合わせ（紫・長、赤・丸）が多いから。　(2) 20%"
       "　(3) 紫・長：紫・丸：赤・長：赤・丸＝66：9：9：16　(4) 紫・長：紫・丸：赤・長：赤・丸＝1：4：4：1",
  "s": "(2) 検定交雑の結果は、F<sub>1</sub>の配偶子の比 AB：Ab：aB：ab＝4：1：1：4 を表す。組換えで生じたのはAbとaBなので、(100＋100)/1000×100＝20%。<br>"
       "(3) F<sub>1</sub>の配偶子は AB 0.4、Ab 0.1、aB 0.1、ab 0.4。赤・丸（aabb）は 0.4×0.4＝0.16。紫・丸（A_bb）は AbとAb：0.1×0.1、Abとab：2×0.1×0.4 で 0.01＋0.08＝0.09。赤・長も同様に0.09。紫・長は残りの 1−0.16−0.09−0.09＝0.66。<br>"
       "(4) このF<sub>1</sub>はAとb、aとBが連鎖している（Ab/aB）。組換えが起こらない配偶子が Ab と aB で各0.4、組換えで生じる AB と ab が各0.1。<br>"
       "<b>ポイント</b>：組換え価＝（組換えで生じた配偶子の数）÷（全配偶子の数）×100。どれが「組換え型」かは、F<sub>1</sub>がどの組み合わせで遺伝子を受けついだか（両親の遺伝子型）で決まる。"},
 {"lv": "B", "tag": "染色体地図",
  "q": "同じ染色体上にある4つの遺伝子A、B、C、Dについて、2つずつの組換え価を調べたところ、次の結果を得た。"
       + TB(["遺伝子の組", "A−B", "B−C", "A−C", "A−D", "C−D"], [["組換え価〔%〕", "12", "7", "5", "3", "8"]])
       + "(1) 4つの遺伝子の染色体上での並び順を答えよ。<br>"
       "(2) BとDの間の組換え価は約何%になると予想されるか。<br>"
       "(3) 実際にBとDの間の組換え価を測定すると、(2)の値よりやや小さかった。その理由を答えよ。",
  "a": "(1) D−A−C−B（またはB−C−A−D）　(2) 約15%　(3) BとDの距離が大きいと、その間で2回の乗換え（二重乗換え）が起こることがあり、そのときはBとDの組み合わせがもとにもどるので、組換えとして数えられないから。",
  "s": "(1) 組換え価は遺伝子間の距離にほぼ比例する。A−C（5）とC−B（7）の和がA−B（12）に等しいので、A−C−Bの順。Dは、A−D（3）、C−D（8）＝3＋5 より、Aをはさんで C と反対側にある。<br>"
       "(2) D−A（3）＋A−C（5）＋C−B（7）＝15。<br>"
       "(3) 二重乗換えの影響は、遺伝子の間の距離が大きいほど大きくなる。そのため、地図は近い遺伝子どうしの組換え価を積み上げてつくる。<br>"
       "<b>ポイント</b>：3つの組換え価のうち「最大のもの＝残り2つの和」となるように並べると、最大の組の両端の遺伝子が外側、残りが中央。"},
 {"lv": "B", "tag": "伴性遺伝",
  "q": "キイロショウジョウバエの眼の色は、X染色体上の遺伝子によって決まり、赤眼（W）は白眼（w）に対して優性である。<br>"
       "(1) 白眼の雌と赤眼の雄を交配した。F<sub>1</sub>の雌と雄の表現型を答えよ。また、F<sub>1</sub>どうしを交配して得たF<sub>2</sub>の、雌と雄それぞれの表現型の比を答えよ。<br>"
       "(2) 赤眼の雌（純系）と白眼の雄を交配した。F<sub>1</sub>の表現型と、F<sub>2</sub>の雌と雄それぞれの表現型の比を答えよ。<br>"
       "(3) (2)のF<sub>2</sub>の赤眼の雌から1匹を選び、白眼の雄と交配したとき、生まれる子が白眼である確率を求めよ。<br>"
       "(4) X染色体上の劣性の形質が、雌より雄に多く現れる理由を答えよ。",
  "a": "(1) F<sub>1</sub>：雌はすべて赤眼、雄はすべて白眼。F<sub>2</sub>：雌 赤眼：白眼＝1：1、雄 赤眼：白眼＝1：1"
       "　(2) F<sub>1</sub>：雌雄ともすべて赤眼。F<sub>2</sub>：雌はすべて赤眼、雄 赤眼：白眼＝1：1　(3) 1/4"
       "　(4) 雄はX染色体を1本しかもたないので、劣性の遺伝子を1つもつだけでその形質が現れるから。",
  "s": "(1) X<sup>w</sup>X<sup>w</sup>×X<sup>W</sup>Y → 雌 X<sup>W</sup>X<sup>w</sup>（赤）、雄 X<sup>w</sup>Y（白）。F<sub>2</sub>は X<sup>W</sup>X<sup>w</sup>、X<sup>w</sup>X<sup>w</sup>、X<sup>W</sup>Y、X<sup>w</sup>Y が1：1：1：1。<br>"
       "(2) X<sup>W</sup>X<sup>W</sup>×X<sup>w</sup>Y → X<sup>W</sup>X<sup>w</sup>、X<sup>W</sup>Y（すべて赤）。F<sub>2</sub>：雌 X<sup>W</sup>X<sup>W</sup>、X<sup>W</sup>X<sup>w</sup>（すべて赤）、雄 X<sup>W</sup>Y、X<sup>w</sup>Y（1：1）。<br>"
       "(3) F<sub>2</sub>の赤眼の雌は X<sup>W</sup>X<sup>W</sup> と X<sup>W</sup>X<sup>w</sup> が1：1。X<sup>W</sup>X<sup>w</sup> を選ぶ確率1/2、そのとき子が白眼（X<sup>w</sup>X<sup>w</sup> または X<sup>w</sup>Y）になる確率1/2。1/2×1/2＝1/4。<br>"
       "<b>ポイント</b>：伴性遺伝は正逆交雑で結果が変わる。雄は母親からX染色体を受けつぐので、「雄の表現型＝母親の配偶子のX」を読めばよい。"},
 {"lv": "B", "tag": "遺伝子の相互作用",
  "q": "スイートピーの白花の2つの純系P、Qを交配すると、F<sub>1</sub>はすべて紫花になった。F<sub>1</sub>を自家受精して得たF<sub>2</sub>800個体は、紫花451、白花349であった。<br>"
       "(1) F<sub>2</sub>の紫花と白花の比は、およそ何：何か。<br>"
       "(2) 花の色は2組の対立遺伝子C（c）とP（p）によって決まり、両者は独立に遺伝する。どのような遺伝子型のときに紫花になると考えられるか。また、純系P、Qの遺伝子型を答えよ。<br>"
       "(3) F<sub>2</sub>の白花のうち、遺伝子型がホモ接合体（2組とも）であるものの割合を求めよ。<br>"
       "(4) 紫色の色素が、前駆物質から2段階の酵素反応でつくられると考えると、この遺伝のしかたはどのように説明できるか。",
  "a": "(1) 9：7　(2) CとPの両方の優性遺伝子をもつとき（C_P_）。純系P、Qは CCpp と ccPP（順不同）　(3) 3/7"
       "　(4) 遺伝子Cが1段階目の酵素を、遺伝子Pが2段階目の酵素をつくり、両方の酵素がはたらいたときだけ紫の色素ができる。どちらかが劣性ホモだと反応が途中で止まり、白花になる。",
  "s": "(1) 451：349 ≒ 9：7（800×9/16＝450、800×7/16＝350）。<br>"
       "(2) F<sub>1</sub>がCcPpで、F<sub>2</sub>の C_P_ が9/16。残りの C_pp、ccP_、ccpp（3＋3＋1＝7）が白花。F<sub>1</sub>がCcPpとなるには、白花の純系どうしがCCppとccPPである必要がある。<br>"
       "(3) 白花7のうちホモ接合体は CCpp、ccPP、ccpp の各1で計3。3/7。<br>"
       "<b>ポイント</b>：9：7（補足遺伝子）、9：3：4（条件遺伝子）、13：3（抑制遺伝子）などは、どれも9：3：3：1の一部を合わせた比。16の分け方から遺伝子型を読む。"},
 {"lv": "B", "tag": "家系図",
  "q": "図は、ある遺伝病についての家系図である。この遺伝病は1組の対立遺伝子によって決まり、Ⅰ−1、Ⅰ−2、Ⅱ−2、Ⅱ−3は発症していない。"
       + _fig_ped()
       + "(1) この遺伝病の原因遺伝子は、優性と劣性のどちらか。理由とともに答えよ。<br>"
       "(2) この原因遺伝子は、常染色体とX染色体のどちらにあると考えられるか。理由とともに答えよ。<br>"
       "(3) Ⅱ−2が、原因遺伝子をヘテロにもつ（保因者である）確率を求めよ。<br>"
       "(4) Ⅱ−2が、保因者であることがわかっている女性との間に子をもつとき、その子が発症する確率を求めよ。",
  "a": "(1) 劣性。発症していない両親（Ⅰ−1、Ⅰ−2）から発症した子（Ⅱ−1）が生まれているから。"
       "　(2) 常染色体。X染色体上の劣性遺伝子なら、発症した娘（Ⅱ−1）の父（Ⅰ−1）も必ず発症するはずだが、Ⅰ−1は発症していないから。　(3) 2/3　(4) 1/6",
  "s": "(1) 正常な両親が劣性遺伝子をヘテロにもち（Aa）、子が劣性ホモ（aa）になったと考えられる。優性遺伝なら、発症した子の親の少なくとも一方は発症しているはず。<br>"
       "(2) 娘は父からX染色体を必ず1本受けつぐ。娘がX<sup>a</sup>X<sup>a</sup>なら父はX<sup>a</sup>Yで発症しているはず。<br>"
       "(3) Ⅰ−1、Ⅰ−2はともにAa。Ⅱ−2は発症していないので、AA：Aa＝1：2 のどちらか。保因者の確率は 2/3。<br>"
       "(4) Ⅱ−2がAaである確率2/3、Aa×Aa で aa が生まれる確率1/4。2/3×1/4＝1/6。<br>"
       "<b>ポイント</b>：家系図では「発症していない」という情報で可能性をしぼる（AA：Aa：aa＝1：2：1 から aa を除いて 1：2）。この条件つき確率の処理が差のつくところ。"},
 {"lv": "C", "tag": "三点交雑",
  "q": "ある植物の3組の対立遺伝子A（a）、B（b）、C（c）は同じ染色体上にあり、大文字が優性である。AABBCCとaabbccを交配して得たF<sub>1</sub>を、aabbccの個体と交配し、次の結果を得た。表の［ ］は表現型を表す（例：［Abc］はAの形質を示し、BとCについては劣性の形質を示す）。"
       + TB(["表現型"] + [f"［{g}］" for g in TP_SHOW[:4]], [["個体数"] + [str(TP[g]) for g in TP_SHOW[:4]]])
       + TB(["表現型"] + [f"［{g}］" for g in TP_SHOW[4:]], [["個体数"] + [str(TP[g]) for g in TP_SHOW[4:]]])
       + "(1) 3つの遺伝子の染色体上での並び順を答えよ。また、そう判断した理由を答えよ。<br>"
       "(2) A−B間、B−C間の組換え価をそれぞれ求めよ。<br>"
       "(3) この表のデータだけからA−C間の組換え価を求めると何%になるか。また、それが(2)の2つの値の和より小さくなる理由を60字以内で説明せよ。<br>"
       "(4) 2つの区間の乗換えが互いに無関係に起こるとすると、二重乗換えで生じる個体の数の期待値はいくらか。実際の結果と比べよ。",
  "a": "(1) A−B−C（Bが中央）。最も数の少ない［AbC］と［aBc］は二重乗換えで生じたもので、親の組み合わせ（ABC、abc）からBだけが入れかわっているから。"
       "　(2) A−B間 10%、B−C間 20%"
       "　(3) 26%。解答例：AとCの間で二重乗換えが起こるとAとCの組み合わせは親と同じにもどり、組換えとして数えられないから。（50字）"
       "　(4) 1000×0.10×0.20＝20個体で、実際の10＋10＝20個体と一致する。",
  "s": "(1) 個体数が最も多い［ABC］［abc］が親と同じ組み合わせ、最も少ない［AbC］［aBc］が二重乗換え型。二重乗換えでは中央の遺伝子だけが入れかわるので、Bが中央。<br>"
       "(2) A−B間の組換え：AとBの組み合わせが親と異なる［Abc］［aBC］［AbC］［aBc］で 40＋40＋10＋10＝100。100/1000＝10%。B−C間：［ABc］［abC］［AbC］［aBc］で 90＋90＋10＋10＝200。20%。<br>"
       "(3) AとCの組み合わせが親と異なるのは［Abc］［aBC］［ABc］［abC］で 40＋40＋90＋90＝260、26%。二重乗換え型20個体の分だけ、10＋20＝30%より小さい。<br>"
       "<b>ポイント</b>：三点交雑では「最多＝親型、最少＝二重乗換え型、中央の遺伝子＝二重乗換えで入れかわる遺伝子」。二重乗換え型は両方の区間の組換えに数える。"},
 {"lv": "C", "tag": "実験考察（連鎖と性）",
  "q": "キイロショウジョウバエの2組の対立遺伝子A（a）とB（b）は同じ常染色体上にあり、大文字が優性である。AABBの個体とaabbの個体を交配してF<sub>1</sub>を得た。<br>"
       "【実験1】F<sub>1</sub>の雌をaabbの雄と交配した。<br>【実験2】F<sub>1</sub>の雄をaabbの雌と交配した。"
       + TB(["子の表現型", "［AB］", "［Ab］", "［aB］", "［ab］"], [["実験1", "400", "100", "100", "400"], ["実験2", "500", "0", "0", "500"]])
       + "(1) 実験1から、F<sub>1</sub>の雌における組換え価を求めよ。<br>"
       "(2) 実験1と実験2の結果のちがいから、どのようなことが推論できるか。60字以内で説明せよ。<br>"
       "(3) F<sub>1</sub>の雌雄を交配したとき、子の表現型の比を求めよ。<br>"
       "(4) AAbbの個体とaaBBの個体を交配して得たF<sub>1</sub>の雌雄を交配したとき、子の表現型の比を求めよ。ただし、雌の組換え価は(1)と同じとする。",
  "a": "(1) 20%　(2) 解答例：この遺伝子の組では、雄では減数分裂のときに乗換えが起こらず、F<sub>1</sub>の雄は親と同じ組み合わせの配偶子しかつくらない。（56字）"
       "　(3) ［AB］：［Ab］：［aB］：［ab］＝14：1：1：4　(4) ［AB］：［Ab］：［aB］：［ab］＝2：1：1：0",
  "s": "(1) (100＋100)/1000＝20%。<br>"
       "(2) 実験2では組換え型（［Ab］［aB］）がまったく現れない。F<sub>1</sub>の雄の配偶子は AB：ab＝1：1 だけである。実際、キイロショウジョウバエの雄では減数分裂で乗換えが起こらないことが知られている。<br>"
       "(3) 雌の配偶子 AB 0.4、Ab 0.1、aB 0.1、ab 0.4。雄の配偶子 AB 0.5、ab 0.5。雄からABを受けた子（0.5）はすべて［AB］。雄からabを受けた子は雌の配偶子の表現型になり、［AB］0.2、［Ab］0.05、［aB］0.05、［ab］0.2。合計 ［AB］0.7、［Ab］0.05、［aB］0.05、［ab］0.2 → 14：1：1：4。<br>"
       "(4) F<sub>1</sub>はAb/aB。雌の配偶子 Ab 0.4、aB 0.4、AB 0.1、ab 0.1。雄の配偶子 Ab 0.5、aB 0.5。雄がAbを渡すと、雌がaBかABなら［AB］（0.5×0.5＝0.25）、AbかabならAb型（0.25）。雄がaBのときも同様に［AB］0.25、［aB］0.25。雄はabを渡さないので［ab］は生じない。<br>"
       "<b>ポイント</b>：雌雄で組換え価が異なるときは、雌雄の配偶子の表を別々につくってかけ合わせる。一方の配偶子が2種類しかないと計算が簡単になる。"},
]}}


def verify():
    _check(7)
    # 7-1
    f2 = Counter("".join(sorted(x)) for x in product("Rr", "Rr"))
    assert f2 == {"RR": 1, "Rr": 2, "rr": 1} and 800 * Fr(f2["rr"], 4) == 200 and Fr(f2["RR"], f2["RR"] + f2["Rr"]) == Fr(1, 3)
    # 7-2
    g = ["".join(x) for x in product("Rr", "Yy")]
    ph = Counter(("R" if "R" in a[0] + b[0] else "r") + ("Y" if "Y" in a[1] + b[1] else "y") for a, b in product(g, g))
    assert ph == {"RY": 9, "Ry": 3, "rY": 3, "ry": 1} and 1600 * Fr(ph["rY"], 16) == 300
    assert Fr(sum(1 for a, b in product(g, g) if {a[0], b[0]} == {"R", "r"} and {a[1], b[1]} == {"Y", "y"}), 16) == Fr(1, 4)
    # 7-3
    kids = Counter("".join(sorted(x)) for x in product("AO", "BO"))
    assert kids["AB"] == 1 and sum(kids.values()) == 4
    yy = Counter("".join(sorted(x)) for x in product("Yy", "Yy"))
    assert Fr(yy["Yy"], yy["yy"]) == 2
    # 7-4
    assert 2 ** 4 == 16 and 16 * 16 == 256 and round(2 ** 23 / 1e6, 1) == 8.4
    # 7-5
    r = Fr(200, 1000)
    assert r == Fr(1, 5)
    f2 = _pheno2(_gam_link(True, r), _gam_link(True, r))
    assert [f2[k] * 100 for k in ("AB", "Ab", "aB", "ab")] == [66, 9, 9, 16]
    tc = _pheno2(_gam_link(False, r), {"ab": Fr(1)})
    assert [tc[k] * 10 for k in ("AB", "Ab", "aB", "ab")] == [1, 4, 4, 1]
    # 7-6 地図：位置を D=0, A=3, C=8, B=15 として組換え価を再現
    pos = {"D": 0, "A": 3, "C": 8, "B": 15}
    data = {("A", "B"): 12, ("B", "C"): 7, ("A", "C"): 5, ("A", "D"): 3, ("C", "D"): 8}
    assert all(abs(pos[a] - pos[b]) == v for (a, b), v in data.items()) and pos["B"] - pos["D"] == 15
    # 7-7 伴性遺伝
    def cross(mom, dad):
        out = Counter()
        for x, y in product(mom, dad):
            sex = "雄" if y == "Y" else "雌"
            red = "W" in x + (y if y != "Y" else "")
            out[(sex, "赤" if red else "白")] += 1
        return out
    f1 = cross(["w", "w"], ["W", "Y"])
    assert f1 == {("雌", "赤"): 2, ("雄", "白"): 2}
    f2 = cross(["W", "w"], ["w", "Y"])        # F1 雌 XWXw × F1 雄 XwY
    assert f2 == {("雌", "赤"): 1, ("雌", "白"): 1, ("雄", "赤"): 1, ("雄", "白"): 1}
    f2b = cross(["W", "w"], ["W", "Y"])       # (2) F1 雌 XWXw × F1 雄 XWY
    assert f2b == {("雌", "赤"): 2, ("雄", "赤"): 1, ("雄", "白"): 1}
    p_white = Fr(1, 2) * Fr(cross(["W", "w"], ["w", "Y"])[("雌", "白")] + cross(["W", "w"], ["w", "Y"])[("雄", "白")], 4)
    assert p_white == Fr(1, 4)
    # 7-8 補足遺伝子
    g = ["".join(x) for x in product("Cc", "Pp")]
    col = Counter()
    homo_white = 0
    for a, b in product(g, g):
        purple = "C" in a[0] + b[0] and "P" in a[1] + b[1]
        col[purple] += 1
        if not purple and a == b:
            homo_white += 1
    assert col[True] == 9 and col[False] == 7 and Fr(homo_white, col[False]) == Fr(3, 7)
    assert 800 * 9 // 16 == 450
    # 7-9 家系図
    sib = Counter("".join(sorted(x)) for x in product("Aa", "Aa"))
    pc = Fr(sib["Aa"], sib["AA"] + sib["Aa"])
    assert pc == Fr(2, 3) and pc * Fr(1, 4) == Fr(1, 6)
    # 7-10 三点交雑
    assert sum(TP.values()) == 1000 and sorted(TP_SHOW) == sorted(TP)
    assert _recomb_tp(0, 1) == Fr(1, 10) and _recomb_tp(1, 2) == Fr(1, 5) and _recomb_tp(0, 2) == Fr(26, 100)
    assert min(TP, key=TP.get) in ("AbC", "aBc") and 1000 * Fr(1, 10) * Fr(1, 5) == TP["AbC"] + TP["aBc"]
    # 7-11 雄は組換えなし
    r = Fr(1, 5)
    f = _pheno2(_gam_link(True, r), _gam_link(True, Fr(0)))
    assert [f[k] * 20 for k in ("AB", "Ab", "aB", "ab")] == [14, 1, 1, 4]
    f = _pheno2(_gam_link(False, r), _gam_link(False, Fr(0)))
    assert [f[k] * 4 for k in ("AB", "Ab", "aB", "ab")] == [2, 1, 1, 0]


def _check(no):
    items = CH[no]["items"]
    lv = [it["lv"] for it in items]
    assert lv.count("A") == 4 and lv.count("B") in (4, 5) and lv.count("C") == 2 and lv == sorted(lv), lv
    for i, it in enumerate(items, 1):
        for k in ("lv", "tag", "q", "a", "s"):
            assert it.get(k, "").strip(), (no, i, k)
        assert "$" not in it["q"] + it["a"] + it["s"], (no, i)
        assert "<b>ポイント</b>：" in it["s"], (no, i)
        for k in ("q", "a", "s"):
            t = it[k]
            for tg in ("div", "table", "tr", "svg", "sub", "sup", "b"):
                assert len(re.findall(f"<{tg}[ >]", t)) == t.count(f"</{tg}>"), (no, i, k, tg)
        lims = [int(n) for n in re.findall(r"(\d+)字以内", it["q"])]
        bods = re.findall(r"解答例：(.*?)（(\d+)字）", it["a"])
        assert len(lims) == len(bods), (no, i, lims, len(bods))
        for lim, (b, n) in zip(lims, bods):
            m = len(re.sub(r"<[^>]+>", "", b))
            assert m == int(n) and lim * 0.55 <= m <= lim, (no, i, m, n, lim)
