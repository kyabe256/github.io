"""問題集 第3章 酸と塩基・中和。CH に問題、verify() で数値・反応式・滴定曲線・形式を検算する。"""
import re
from math import log10, floor, sqrt
from collections import Counter

KW, KA = 1.0e-14, 2.7e-5   # 図の作成用（酢酸の電離定数）


def ph_strong(v):
    """0.10 mol/L HCl 10 mL に 0.10 mol/L NaOH を v mL 加えたときの pH"""
    ca, cb = 0.10 * 10 / (10 + v), 0.10 * v / (10 + v)
    d = ca - cb
    h = (d + sqrt(d * d + 4 * KW)) / 2
    return -log10(h)


def ph_weak(v):
    """0.10 mol/L CH3COOH 10 mL に 0.10 mol/L NaOH を v mL 加えたときの pH（電荷のつり合いを二分法で解く）"""
    ca, cb = 0.10 * 10 / (10 + v), 0.10 * v / (10 + v)
    f = lambda h: h + cb - KW / h - ca * KA / (KA + h)
    lo, hi = -14.0, 0.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(10 ** mid) > 0:
            hi = mid
        else:
            lo = mid
    return -(lo + hi) / 2


def fig_titration():
    W, H, x0, x1, y0, y1 = 400, 250, 40, 300, 10, 220
    X = lambda v: x0 + v / 20 * (x1 - x0)
    Y = lambda p: y1 - p / 14 * (y1 - y0)
    o = [f'<svg class="fig" width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-size="10">']
    for lo, hi, name in [(3.1, 4.4, "メチルオレンジ"), (8.0, 9.8, "フェノールフタレイン")]:
        o.append(f'<rect x="{x0}" y="{Y(hi):.1f}" width="{x1-x0}" height="{Y(lo)-Y(hi):.1f}" fill="#e3e3e3"/>'
                 f'<text x="{x1+5}" y="{(Y(lo)+Y(hi))/2+3:.1f}">{name}</text>')
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="#000"/>')
    for p in range(0, 15, 2):
        o.append(f'<text x="{x0-4}" y="{Y(p)+3:.1f}" text-anchor="end">{p}</text>'
                 f'<line x1="{x0}" y1="{Y(p):.1f}" x2="{x0+4}" y2="{Y(p):.1f}" stroke="#000"/>')
    o.append(f'<line x1="{x0}" y1="{Y(7):.1f}" x2="{x1}" y2="{Y(7):.1f}" stroke="#999" stroke-dasharray="3,3"/>')
    for v in range(0, 21, 5):
        o.append(f'<text x="{X(v):.1f}" y="{y1+13}" text-anchor="middle">{v}</text>'
                 f'<line x1="{X(v):.1f}" y1="{y1}" x2="{X(v):.1f}" y2="{y1-4}" stroke="#000"/>')
    o.append(f'<text x="{(x0+x1)/2}" y="{H-4}" text-anchor="middle">加えた NaOH 水溶液の体積〔mL〕</text>')
    o.append(f'<text x="12" y="{(y0+y1)/2}" transform="rotate(-90 12 {(y0+y1)/2})" text-anchor="middle">pH</text>')
    vs = [i / 20 for i in range(0, 401)]
    for fn, lab, dash, lv in [(ph_strong, "a", "", 2.0), (ph_weak, "b", ' stroke-dasharray="6,3"', 6.0)]:
        o.append(f'<polyline fill="none" stroke="#000" stroke-width="1.4"{dash} points="' +
                 " ".join(f"{X(v):.1f},{Y(fn(v)):.1f}" for v in vs) + '"/>')
        o.append(f'<text x="{X(lv)+3:.1f}" y="{Y(fn(lv))-5:.1f}" font-size="12">{lab}</text>')
    o.append("</svg>")
    return "".join(o)


B = '<div class="bun">'

CH = {3: {
"goal": "酸・塩基の定義と強弱を区別し、pH を正確に計算する。中和の量的関係・滴定の器具と指示薬・滴定曲線を一体として理解し、二段滴定や逆滴定まで解けるようにする。",
"items": [
 {"lv": "A", "tag": "酸・塩基の定義",
  "q": r"(1)〜(4) の反応で下線を引いた物質（イオン）は、ブレンステッド・ローリーの定義で酸・塩基のどちらとしてはたらいているか。<br>(1) $\mathrm{NH_3+\underline{H_2O}\rightleftarrows NH_4^++OH^-}$<br>(2) $\mathrm{HCl+\underline{NH_3}\to NH_4^++Cl^-}$<br>(3) $\mathrm{HSO_4^-+\underline{H_2O}\rightleftarrows SO_4^{2-}+H_3O^+}$<br>(4) $\mathrm{\underline{CO_3^{2-}}+H_2O\rightleftarrows HCO_3^-+OH^-}$<br>(5) 次の酸・塩基の価数と強弱を答えよ。$\mathrm{H_2SO_4}$、$\mathrm{CH_3COOH}$、$\mathrm{NH_3}$、$\mathrm{Ca(OH)_2}$",
  "a": r"(1) 酸　(2) 塩基　(3) 塩基　(4) 塩基　(5) $\mathrm{H_2SO_4}$ 2価の強酸、$\mathrm{CH_3COOH}$ 1価の弱酸、$\mathrm{NH_3}$ 1価の弱塩基、$\mathrm{Ca(OH)_2}$ 2価の強塩基",
  "s": r"ブレンステッド・ローリーの定義では、$\mathrm{H^+}$ を与える物質が酸、受け取る物質が塩基。(1) $\mathrm{H_2O}$ は $\mathrm{NH_3}$ に $\mathrm{H^+}$ を与えて $\mathrm{OH^-}$ になる → 酸。(2) $\mathrm{NH_3}$ は $\mathrm{H^+}$ を受け取る → 塩基。(3) $\mathrm{H_2O}$ は $\mathrm{H^+}$ を受け取って $\mathrm{H_3O^+}$ になる → 塩基。水は相手によって酸にも塩基にもなる。(4) $\mathrm{CO_3^{2-}}$ は $\mathrm{H^+}$ を受け取る → 塩基。(5) $\mathrm{NH_3}$ は $\mathrm{NH_3+H_2O\rightleftarrows NH_4^++OH^-}$ で $\mathrm{OH^-}$ を1個生じるので1価。<br><b>ポイント</b>：「$\mathrm{H^+}$ のやりとり」で判断する。同じ物質（$\mathrm{H_2O}$ など）でも、反応によって酸にも塩基にもなる。"},
 {"lv": "A", "tag": "pH の計算",
  "q": r"次の水溶液の pH を求めよ。強酸・強塩基は完全に電離するものとし、水のイオン積 $K_\mathrm{w}=1.0\times10^{-14}\ (\mathrm{mol/L})^2$ とする。<br>(1) 0.010 mol/L の塩酸<br>(2) 0.0050 mol/L の硫酸<br>(3) 0.10 mol/L の酢酸水溶液（電離度 0.010）<br>(4) 0.050 mol/L の水酸化バリウム水溶液<br>(5) 0.10 mol/L の水酸化ナトリウム水溶液を、水で 1000 倍に薄めた水溶液",
  "a": r"(1) 2　(2) 2　(3) 3　(4) 13　(5) 10",
  "s": r"(1) $[\mathrm{H^+}]=1.0\times10^{-2}$。(2) 2価なので $[\mathrm{H^+}]=2\times0.0050=1.0\times10^{-2}$。(3) $[\mathrm{H^+}]=c\alpha=0.10\times0.010=1.0\times10^{-3}$。(4) $\mathrm{Ba(OH)_2}$ は2価なので $[\mathrm{OH^-}]=0.10$、$[\mathrm{H^+}]=\frac{K_\mathrm{w}}{[\mathrm{OH^-}]}=1.0\times10^{-13}$。(5) $[\mathrm{OH^-}]=1.0\times10^{-4}$、$[\mathrm{H^+}]=1.0\times10^{-10}$。<br><b>ポイント</b>：$[\mathrm{H^+}]$＝価数 × 濃度 × 電離度。塩基は $[\mathrm{OH^-}]$ を出してから $K_\mathrm{w}$ で $[\mathrm{H^+}]$ に直す（または $\mathrm{pH}=14-\mathrm{pOH}$）。"},
 {"lv": "A", "tag": "塩の性質",
  "q": r"次の塩 (ア)〜(キ) について、下の問いに答えよ。<br>(ア) $\mathrm{NaCl}$　(イ) $\mathrm{CH_3COONa}$　(ウ) $\mathrm{NH_4Cl}$　(エ) $\mathrm{Na_2CO_3}$　(オ) $\mathrm{NaHSO_4}$　(カ) $\mathrm{NaHCO_3}$　(キ) $\mathrm{KNO_3}$<br>(1) 酸性塩をすべて選べ。<br>(2) 水溶液が酸性を示すものをすべて選べ。<br>(3) 水溶液が塩基性を示すものをすべて選べ。",
  "a": r"(1) (オ)、(カ)　(2) (ウ)、(オ)　(3) (イ)、(エ)、(カ)",
  "s": r"正塩・酸性塩・塩基性塩は「酸の H や塩基の OH が残っているか」という組成による分類で、水溶液の性質とは別である。強酸と強塩基からなる正塩（$\mathrm{NaCl}$、$\mathrm{KNO_3}$）は中性。弱酸と強塩基の塩（$\mathrm{CH_3COONa}$、$\mathrm{Na_2CO_3}$）は加水分解で塩基性、強酸と弱塩基の塩（$\mathrm{NH_4Cl}$）は酸性。$\mathrm{NaHSO_4}$ は $\mathrm{HSO_4^-}$ がさらに電離して $\mathrm{H^+}$ を出すので酸性。$\mathrm{NaHCO_3}$ は酸性塩だが、$\mathrm{HCO_3^-+H_2O\rightleftarrows H_2CO_3+OH^-}$ により弱い塩基性を示す。<br><b>ポイント</b>：塩の水溶液の性質は「もとの酸と塩基の強弱」で決まる（強い方の性質が出る）。「酸性塩＝酸性」ではない。"},
 {"lv": "A", "tag": "中和の量的関係",
  "q": r"(1) 0.10 mol/L の硫酸 15 mL を中和するのに必要な、0.12 mol/L の水酸化ナトリウム水溶液の体積を求めよ。<br>(2) 0.050 mol/L の水酸化カルシウム水溶液 20 mL を中和するのに必要な、0.10 mol/L の塩酸の体積を求めよ。<br>(3) 0.20 mol/L の酢酸水溶液 10 mL と、0.20 mol/L の塩酸 10 mL を、それぞれ 0.10 mol/L の水酸化ナトリウム水溶液で中和するとき、必要な体積はそれぞれ何 mL か。",
  "a": r"(1) 25 mL　(2) 20 mL　(3) どちらも 20 mL",
  "s": r"中和の条件は（酸の価数）×（酸の物質量）＝（塩基の価数）×（塩基の物質量）。(1) $2\times0.10\times15=1\times0.12\times V$ より $V=25\ \mathrm{mL}$。(2) $1\times0.10\times V=2\times0.050\times20$ より $V=20\ \mathrm{mL}$。(3) 酢酸は弱酸で電離度は小さいが、中和が進むと電離平衡が移動して残りも次々に電離するので、最終的に放出できる $\mathrm{H^+}$ の量は塩酸と同じ。どちらも $1\times0.20\times10=1\times0.10\times V$ より $V=20\ \mathrm{mL}$。<br><b>ポイント</b>：中和に必要な量は、酸・塩基の強弱（電離度）には関係しない。価数と物質量だけで決まる。"},
 {"lv": "B", "tag": "中和滴定の実験",
  "q": r"食酢中の酢酸の濃度を求めるため、次の実験を行った。" + B + r"食酢 10.0 mL を器具 (a) で正確にはかりとり、器具 (b) に入れて純水を加え、100 mL とした。この水溶液 10.0 mL を (a) でコニカルビーカーにとり、指示薬を加えて、器具 (c) から 0.100 mol/L の水酸化ナトリウム水溶液を滴下したところ、7.20 mL で終点に達した。</div>(1) 器具 (a)〜(c) の名称を答えよ。<br>(2) (a)〜(c) とコニカルビーカーのうち、内部が純水でぬれたまま使ってよいものをすべて選べ。<br>(3) 指示薬として適切なものを答え、終点での色の変化を述べよ。<br>(4) 食酢中の酢酸のモル濃度を求めよ。<br>(5) 食酢の密度を $1.0\ \mathrm{g/cm^3}$ とし、食酢に含まれる酸はすべて酢酸として、酢酸の質量パーセント濃度を求めよ。$\mathrm{H}=1.0$、$\mathrm{C}=12$、$\mathrm{O}=16$。",
  "a": r"(1) (a) ホールピペット　(b) メスフラスコ　(c) ビュレット　(2) (b)、コニカルビーカー　(3) フェノールフタレイン、無色から淡赤色に変わる　(4) $0.720\ \mathrm{mol/L}$　(5) 4.3%",
  "s": r"(2) ホールピペットとビュレットは、中に入れる溶液の濃度が変わってはいけないので、その溶液で数回すすいで（共洗い）から使う。メスフラスコはあとで純水を加えるので、コニカルビーカーは中の溶質の物質量が変わらないので、ぬれたままでよい。(3) 中和点の水溶液は酢酸ナトリウムの加水分解で弱塩基性になるので、塩基性側に変色域をもつフェノールフタレインを使う。(4) 薄めた水溶液の濃度を $c$ とすると $1\times c\times10.0=1\times0.100\times7.20$ より $c=0.0720\ \mathrm{mol/L}$。10 倍に薄めたので食酢は $0.720\ \mathrm{mol/L}$。(5) 食酢 1 L（1000 g）に酢酸 $0.720\times60=43.2\ \mathrm{g}$、$\frac{43.2}{1000}\times100\fallingdotseq4.3\%$。<br><b>ポイント</b>：共洗いが必要なのは「中の溶液の濃度がそのまま結果に効く器具」（ホールピペット・ビュレット）。希釈した場合は、最後に倍率をかけてもとの濃度にもどす。"},
 {"lv": "B", "tag": "滴定曲線",
  "q": r"図は、0.10 mol/L の塩酸 10 mL（曲線 a）と、0.10 mol/L の酢酸水溶液 10 mL（曲線 b）を、それぞれ 0.10 mol/L の水酸化ナトリウム水溶液で滴定したときの滴定曲線である。灰色の帯は2種類の指示薬の変色域を示す。" + fig_titration() +
       r"(1) 中和点までに加えた水酸化ナトリウム水溶液の体積は、a・b それぞれ何 mL か。<br>(2) b の滴定で、メチルオレンジが指示薬として適さない理由を述べよ。<br>(3) b の中和点の pH が 7 より大きくなる理由を、イオン反応式を用いて説明せよ。<br>(4) 滴定を始める前の pH が、a より b の方が大きい理由を述べよ。<br>(5) 0.10 mol/L のアンモニア水 10 mL を 0.10 mol/L の塩酸で滴定するとき、指示薬として適切なのは図の2種類のうちどちらか。",
  "a": r"(1) どちらも 10 mL　(2) メチルオレンジの変色域は、中和点よりずっと前の pH がゆるやかに変化する範囲にあり、中和点で変色しないから。(3) $\mathrm{CH_3COO^-+H_2O\rightleftarrows CH_3COOH+OH^-}$ の加水分解で $\mathrm{OH^-}$ が生じるから。(4) 酢酸は弱酸で電離度が小さく、同じ濃度でも $[\mathrm{H^+}]$ が小さいから。(5) メチルオレンジ",
  "s": r"(1) 中和点は酸と塩基の物質量の関係だけで決まり、強弱には関係しない。$0.10\times10=0.10\times V$ より $V=10\ \mathrm{mL}$。(2) 曲線 b は pH 約 4.4 を中和点よりかなり手前で通過し、そこではゆるやかに変化している。メチルオレンジでは終点が早く見えてしまう。中和点付近の急な変化（pH 約 7〜11）の範囲に変色域があるのはフェノールフタレイン。(3) 中和点の水溶液は $\mathrm{CH_3COONa}$ 水溶液で、弱酸のイオン $\mathrm{CH_3COO^-}$ が加水分解する。(4) 塩酸は完全電離で pH 1.0、酢酸は一部しか電離しないので pH は約 2.8。(5) 弱塩基と強酸の滴定では中和点が酸性側（$\mathrm{NH_4^+}$ の加水分解）になり、急な変化も酸性側にかたよるので、メチルオレンジを使う。<br><b>ポイント</b>：指示薬は「中和点付近の pH の急変部分に変色域があるもの」を選ぶ。強酸＋強塩基はどちらも可、弱酸＋強塩基はフェノールフタレイン、強酸＋弱塩基はメチルオレンジ。"},
 {"lv": "B", "tag": "混合溶液の pH",
  "q": r"次の水溶液の pH を、小数第1位まで求めよ。強酸・強塩基は完全に電離し、混合後の体積は混合前の体積の和とする。$K_\mathrm{w}=1.0\times10^{-14}\ (\mathrm{mol/L})^2$、$\log_{10}2=0.30$ とする。<br>(1) 0.10 mol/L の塩酸 11 mL と 0.10 mol/L の水酸化ナトリウム水溶液 9.0 mL を混合した水溶液<br>(2) 0.20 mol/L の塩酸 10 mL と 0.10 mol/L の水酸化ナトリウム水溶液 30 mL を混合した水溶液<br>(3) pH 3.0 の塩酸を、水で 100 倍に薄めた水溶液<br>(4) pH 5.0 の塩酸を水で 1000 倍に薄めても、pH は 8.0 にはならない。およその pH を答え、その理由を述べよ。",
  "a": r"(1) 2.0　(2) 12.4　(3) 5.0　(4) およそ 7（7 よりわずかに小さい）。酸を薄めても塩基性にはならず、水自身の電離による $[\mathrm{H^+}]=1.0\times10^{-7}\ \mathrm{mol/L}$ が無視できなくなるから。",
  "s": r"(1) $\mathrm{H^+}$：$0.10\times\frac{11}{1000}=1.1\times10^{-3}\ \mathrm{mol}$、$\mathrm{OH^-}$：$0.90\times10^{-3}\ \mathrm{mol}$。残る $\mathrm{H^+}$ は $2.0\times10^{-4}\ \mathrm{mol}$、体積 20 mL なので $[\mathrm{H^+}]=1.0\times10^{-2}$、pH 2.0。(2) $\mathrm{H^+}$ $2.0\times10^{-3}\ \mathrm{mol}$、$\mathrm{OH^-}$ $3.0\times10^{-3}\ \mathrm{mol}$。残る $\mathrm{OH^-}$ $1.0\times10^{-3}\ \mathrm{mol}$ が 40 mL 中にあり $[\mathrm{OH^-}]=2.5\times10^{-2}$。$\log_{10}2.5=\log_{10}\frac{10}{4}=1-0.60=0.40$ なので $\mathrm{pOH}=2-0.40=1.60$、$\mathrm{pH}=14-1.60=12.4$。(3) $[\mathrm{H^+}]=1.0\times10^{-5}$。(4) 酸由来の $[\mathrm{H^+}]$ は $1.0\times10^{-8}$ で、水の電離による $10^{-7}$ 程度より小さい。正確に解くと $[\mathrm{H^+}]\fallingdotseq1.05\times10^{-7}$、pH 約 6.98。<br><b>ポイント</b>：混合では「残った方の $\mathrm{H^+}$ か $\mathrm{OH^-}$」を全体積で割る。極端に薄い酸・塩基では水の電離を無視できない。"},
 {"lv": "B", "tag": "正誤",
  "q": r"酸・塩基と pH に関する次の記述 ①〜⑤ のうち、誤りを含むものを2つ選べ。<br>① 酢酸は弱酸なので、同じ濃度・同じ体積の塩酸に比べて、中和に必要な水酸化ナトリウムの量は少ない。<br>② pH 2 の塩酸と pH 2 の酢酸水溶液を同じ体積ずつとると、中和に必要な水酸化ナトリウムの量は酢酸水溶液の方が多い。<br>③ 0.1 mol/L の硫酸の pH は、0.1 mol/L の塩酸の pH より小さい。<br>④ 温度を上げると水のイオン積は大きくなるので、純水の pH は 7 より小さくなるが、純水は中性のままである。<br>⑤ 濃度 $1.0\times10^{-8}\ \mathrm{mol/L}$ の塩酸の pH は 8 である。",
  "a": r"①、⑤",
  "s": r"① 誤り。A-4 (3) と同じく、中和に必要な量は価数と物質量だけで決まり、同じになる。② 正しい。pH が同じなら $[\mathrm{H^+}]$ は同じだが、酢酸はごく一部しか電離していないので、酢酸の濃度は塩酸よりはるかに大きい。③ 正しい。硫酸は2価の酸で、$[\mathrm{H^+}]$ は塩酸より大きくなる。④ 正しい。水の電離は吸熱変化で、温度を上げると $[\mathrm{H^+}]=[\mathrm{OH^-}]$ のまま両方大きくなる。中性とは $[\mathrm{H^+}]=[\mathrm{OH^-}]$ のことで、pH 7 とは限らない。⑤ 誤り。酸の水溶液が塩基性になることはない。水の電離を考えると pH は約 6.98。<br><b>ポイント</b>：「濃度」「$[\mathrm{H^+}]$」「中和に必要な量」を区別する。中性の定義は $[\mathrm{H^+}]=[\mathrm{OH^-}]$。"},
 {"lv": "B", "tag": "混合物の中和",
  "q": r"水酸化ナトリウムと水酸化カリウムの混合物 1.52 g を水に溶かし、1.00 mol/L の塩酸で中和すると 30.0 mL を要した。$\mathrm{H}=1.0$、$\mathrm{O}=16$、$\mathrm{Na}=23$、$\mathrm{K}=39$、$\log_{10}3=0.48$ とする。<br>(1) 混合物中の水酸化ナトリウムと水酸化カリウムの質量を、それぞれ有効数字3桁で求めよ。<br>(2) この混合物を水に溶かして 100 mL にした水溶液の pH を小数第1位まで求めよ。",
  "a": r"(1) 水酸化ナトリウム 0.400 g、水酸化カリウム 1.12 g　(2) 13.5",
  "s": r"(1) NaOH $x$ mol、KOH $y$ mol とすると、質量：$40x+56y=1.52$、中和：$x+y=1.00\times0.0300=0.0300$。$y=0.0300-x$ を代入して $40x+1.68-56x=1.52$、$x=0.0100$、$y=0.0200$。質量は $0.0100\times40=0.400\ \mathrm{g}$、$0.0200\times56=1.12\ \mathrm{g}$。(2) $[\mathrm{OH^-}]=\frac{0.0300}{0.100}=0.300=3.0\times10^{-1}$。$\mathrm{pOH}=1-0.48=0.52$、$\mathrm{pH}=14-0.52\fallingdotseq13.5$。<br><b>ポイント</b>：1価の塩基どうしの混合物では、「質量の式」と「$\mathrm{OH^-}$ の物質量の式」の2本で連立する。"},
 {"lv": "C", "tag": "二段滴定",
  "q": B + r"水酸化ナトリウム水溶液を空気中に放置したところ、二酸化炭素の一部を吸収した。この水溶液 20.0 mL にフェノールフタレインを加え、0.100 mol/L の塩酸で滴定すると、15.0 mL 加えたところで赤色が消えた（第1中和点）。続いてメチルオレンジを加えて滴定を続けると、さらに 5.00 mL 加えたところで黄色から赤色に変わった（第2中和点）。</div>(1) 水酸化ナトリウムが二酸化炭素を吸収する反応の化学反応式を書け。<br>(2) 第1中和点までに起こる2つの反応と、第1中和点から第2中和点までに起こる反応を、化学反応式で書け。<br>(3) 滴定前の水溶液中の水酸化ナトリウムと炭酸ナトリウムのモル濃度を求めよ。<br>(4) 二酸化炭素を吸収する前の水酸化ナトリウム水溶液のモル濃度と、この 20.0 mL が吸収した二酸化炭素の物質量を求めよ。ただし、吸収による水溶液の体積変化はないものとする。",
  "a": r"(1) $\mathrm{2NaOH+CO_2\to Na_2CO_3+H_2O}$　(2) 第1：$\mathrm{NaOH+HCl\to NaCl+H_2O}$、$\mathrm{Na_2CO_3+HCl\to NaHCO_3+NaCl}$　第2：$\mathrm{NaHCO_3+HCl\to NaCl+H_2O+CO_2}$　(3) $\mathrm{NaOH}$ $0.0500\ \mathrm{mol/L}$、$\mathrm{Na_2CO_3}$ $0.0250\ \mathrm{mol/L}$　(4) $0.100\ \mathrm{mol/L}$、$5.00\times10^{-4}\ \mathrm{mol}$",
  "s": r"第1中和点（pH 約 8.3）では、$\mathrm{NaOH}$ の中和と $\mathrm{CO_3^{2-}\to HCO_3^-}$ が終わっている。第2中和点（pH 約 4）では $\mathrm{HCO_3^-\to CO_2+H_2O}$ が終わる。NaOH を $x$ mol、$\mathrm{Na_2CO_3}$ を $y$ mol とすると、第2段階の HCl は $\mathrm{NaHCO_3}$（$y$ mol）と反応するので $y=0.100\times\frac{5.00}{1000}=5.00\times10^{-4}\ \mathrm{mol}$。第1段階：$x+y=0.100\times\frac{15.0}{1000}=1.50\times10^{-3}$ より $x=1.00\times10^{-3}\ \mathrm{mol}$。(3) 20.0 mL 中なので、$\mathrm{NaOH}$ $\frac{1.00\times10^{-3}}{0.0200}=0.0500\ \mathrm{mol/L}$、$\mathrm{Na_2CO_3}$ $0.0250\ \mathrm{mol/L}$。(4) $\mathrm{Na_2CO_3}$ 1 mol は NaOH 2 mol からできたので、もとの NaOH は $x+2y=2.00\times10^{-3}\ \mathrm{mol}$、濃度 $0.100\ \mathrm{mol/L}$。吸収した $\mathrm{CO_2}$ は $y=5.00\times10^{-4}\ \mathrm{mol}$。<br><b>ポイント</b>：炭酸塩の滴定は2段階（$\mathrm{CO_3^{2-}\to HCO_3^-\to H_2CO_3}$）。第2段階の滴下量から $\mathrm{CO_3^{2-}}$ の量が決まり、第1段階から NaOH の量を引き算で出す。"},
 {"lv": "C", "tag": "逆滴定",
  "q": B + r"硫酸アンモニウムを含む肥料 1.00 g に濃い水酸化ナトリウム水溶液を加えて加熱し、発生したアンモニアをすべて 0.250 mol/L の硫酸 40.0 mL に吸収させた。この水溶液に指示薬を加え、残った硫酸を 0.500 mol/L の水酸化ナトリウム水溶液で滴定すると、20.0 mL を要した。</div>$\mathrm{H}=1.0$、$\mathrm{N}=14$、$\mathrm{O}=16$、$\mathrm{S}=32$ とする。<br>(1) アンモニアが発生する反応の化学反応式を書け。<br>(2) 発生したアンモニアの物質量を求めよ。<br>(3) 肥料中の硫酸アンモニウムの質量パーセントを求めよ。<br>(4) 肥料中の窒素の質量パーセントを求めよ。ただし、肥料中の窒素はすべて硫酸アンモニウムとして含まれるものとする。<br>(5) この滴定の指示薬として、メチルオレンジとフェノールフタレインのどちらが適切か。理由とともに答えよ。",
  "a": r"(1) $\mathrm{(NH_4)_2SO_4+2NaOH\to Na_2SO_4+2NH_3+2H_2O}$　(2) $1.00\times10^{-2}\ \mathrm{mol}$　(3) 66.0%　(4) 14.0%　(5) メチルオレンジ。終点の水溶液には $\mathrm{NH_4^+}$ が含まれて弱酸性になるので、酸性側に変色域をもつ指示薬が必要だから（フェノールフタレインでは $\mathrm{NH_4^+}$ も NaOH と反応してしまう）。",
  "s": r"(2) 硫酸が出しうる $\mathrm{H^+}$ は $2\times0.250\times0.0400=0.0200\ \mathrm{mol}$。これを、アンモニア（1価）と滴定の NaOH（$0.500\times0.0200=0.0100\ \mathrm{mol}$）で中和したので、$\mathrm{NH_3}=0.0200-0.0100=0.0100\ \mathrm{mol}$。(3) $\mathrm{(NH_4)_2SO_4}=132$。1 mol から $\mathrm{NH_3}$ 2 mol が出るので $0.00500\ \mathrm{mol}$、$0.00500\times132=0.660\ \mathrm{g}$、66.0%。(4) N は $0.0100\times14=0.140\ \mathrm{g}$、14.0%。<br><b>ポイント</b>：逆滴定は「酸の $\mathrm{H^+}$ の総量＝（求めたい塩基）＋（滴定に使った塩基）」の式を立てる。気体のアンモニアを直接滴定しにくいので、一度過剰の酸に吸収させる。"},
]}}


AW = {"H": 1.0, "C": 12, "N": 14, "O": 16, "Na": 23, "S": 32, "Cl": 35.5, "K": 39}


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


def Mr(f):
    return sum(AW[e] * c for e, c in _parse(f).items())


def balanced(lhs, rhs):
    def tot(side):
        t = Counter()
        for k, f in side:
            for e, c in _parse(f).items():
                t[e] += k * c
        return +t
    assert tot(lhs) == tot(rhs), (lhs, rhs)


def verify():
    items = CH[3]["items"]
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

    pH = lambda h: -log10(h)
    # A2
    eq(pH(0.010), 2); eq(pH(2 * 0.0050), 2); eq(pH(0.10 * 0.010), 3)
    eq(pH(KW / (2 * 0.050)), 13); eq(pH(KW / (0.10 / 1000)), 10)
    # A4
    eq(2 * 0.10 * 15 / 0.12, 25); eq(2 * 0.050 * 20 / 0.10, 20); eq(0.20 * 10 / 0.10, 20)
    # B1 食酢
    c = 0.100 * 7.20 / 10.0; eq(c * 10, 0.720, 3); eq(c * 10 * Mr("CH3COOH") / 1000 * 100, 4.3)
    # B2 滴定曲線の性質
    assert abs(ph_strong(0) - 1.0) < 1e-6 and 2.7 < ph_weak(0) < 3.0
    assert abs(ph_strong(10) - 7.0) < 1e-6 and 8.0 < ph_weak(10) < 9.5
    v44 = next(v / 100 for v in range(0, 2001) if ph_weak(v / 100) >= 4.4)
    assert v44 < 7      # メチルオレンジの変色域の上端を中和点よりかなり前に通過
    assert ph_weak(9.9) < 8.0 < ph_weak(10.1)   # フェノールフタレインは中和点の急変部で変色
    assert ph_strong(9.9) < 4.4 and ph_strong(10.1) > 9.8
    # B3 混合溶液
    h = (0.10 * 11 - 0.10 * 9.0) / 1000 / 0.020; eq(pH(h), 2.0)
    oh = (0.10 * 30 - 0.20 * 10) / 1000 / 0.040; assert abs(oh - 0.025) < 1e-12
    assert abs((14 - (2 - (1 - 2 * 0.30))) - 12.4) < 1e-9 and round(14 + log10(oh), 1) == 12.4
    eq(pH(1e-3 / 100), 5.0)
    c = 1.0e-8; h = (c + sqrt(c * c + 4 * KW)) / 2
    assert abs(h - 1.05e-7) < 0.005e-7 and round(pH(h), 2) == 6.98
    # B5 NaOH/KOH
    x = (1.52 - 56 * 0.0300) / (40 - 56); y = 0.0300 - x
    eq(x * Mr("NaOH"), 0.400, 3); eq(y * Mr("KOH"), 1.12, 3)
    assert abs((14 - (1 - 0.48)) - 13.48) < 1e-9 and round(14 + log10(0.300), 1) == 13.5
    # C1 二段滴定
    y = 0.100 * 5.00e-3; x = 0.100 * 15.0e-3 - y
    eq(x / 0.0200, 0.0500, 3); eq(y / 0.0200, 0.0250, 3); eq((x + 2 * y) / 0.0200, 0.100, 3); eq(y, 5.00e-4, 3)
    balanced([(2, "NaOH"), (1, "CO2")], [(1, "Na2CO3"), (1, "H2O")])
    balanced([(1, "Na2CO3"), (1, "HCl")], [(1, "NaHCO3"), (1, "NaCl")])
    balanced([(1, "NaHCO3"), (1, "HCl")], [(1, "NaCl"), (1, "H2O"), (1, "CO2")])
    # C2 逆滴定
    nh3 = 2 * 0.250 * 0.0400 - 0.500 * 0.0200; eq(nh3, 1.00e-2, 3)
    assert Mr("(NH4)2SO4") == 132
    eq(nh3 / 2 * 132 / 1.00 * 100, 66.0, 3); eq(nh3 * 14 / 1.00 * 100, 14.0, 3)
    balanced([(1, "(NH4)2SO4"), (2, "NaOH")], [(1, "Na2SO4"), (2, "NH3"), (2, "H2O")])
