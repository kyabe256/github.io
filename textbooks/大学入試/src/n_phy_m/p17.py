"""問題集 第17章 交流と電磁波。CH に問題、verify() で答えを sympy で検算する。図は座標を計算して SVG で描く。"""
from math import sin as _sin, cos as _cos, atan2 as _atan2, sqrt as _sqrt
from sympy import *


# ---------------- 図 ----------------
def _svg(w, h, body):
    return f'<svg class="fig" width="{w}" height="{h}" viewBox="0 0 {w} {h}">' + "".join(body) + "</svg>"

def _t(x, y, s, size=11, anchor="middle"):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}">{s}</text>'

def _ln(x1, y1, x2, y2, w=1.0, dash="", col="#222"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}"{d}/>'

def _dot(x, y, r=2.6, col="#222"):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{col}"/>'

I = lambda s: f'<tspan font-family="Liberation Serif,serif" font-style="italic" font-size="12.5">{s}</tspan>'
SUB = lambda s: f'<tspan dy="3" font-size="8">{s}</tspan>'

def _wire(pts, w=1.2):
    return '<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + f'" fill="none" stroke="#222" stroke-width="{w}"/>'

def _C(cx, cy):
    """縦の導線上のコンデンサー（極板は水平）"""
    return (f'<rect x="{cx-12}" y="{cy-4}" width="24" height="8" fill="#fff"/>' +
            _ln(cx - 11, cy - 4, cx + 11, cy - 4, 2.2) + _ln(cx - 11, cy + 4, cx + 11, cy + 4, 2.2))

def _Lcoil(cx, cy, n=4, w=10):
    """横の導線上のコイル"""
    x0 = cx - n * w / 2
    d = f"M {x0} {cy} " + " ".join(f"a {w/2} {w/2} 0 0 1 {w} 0" for _ in range(n))
    return (f'<rect x="{x0-1}" y="{cy-3}" width="{n*w+2}" height="6" fill="#fff"/>' +
            f'<path d="{d}" fill="none" stroke="#222" stroke-width="1.4"/>')

def _S(x1, y, x2):
    a = -0.45
    L = x2 - x1
    return (f'<rect x="{x1+1}" y="{y-3}" width="{L}" height="6" fill="#fff"/>' +
            _ln(x1, y, x1 + L * 0.95 * _cos(a), y + L * 0.95 * _sin(a), 1.3) +
            f'<circle cx="{x1}" cy="{y}" r="2.4" fill="#fff" stroke="#222"/><circle cx="{x2}" cy="{y}" r="2.4" fill="#fff" stroke="#222"/>')


def _fig_lc2():
    yt, yb, xl, xr = 30, 140, 60, 270
    ym = (yt + yb) / 2
    b = [_wire([(xl, ym), (xl, yt), (xr, yt), (xr, yb), (xl, yb), (xl, ym)]),
         _C(xl, ym), _C(xr, ym), _S(100, yt, 130), _Lcoil(200, yt),
         _t(xl - 16, ym + 4, "C" + SUB("1"), 11, "end"), _t(xr + 16, ym + 4, "C" + SUB("2"), 11, "start"),
         _t(xl + 16, ym - 8, "a", 11, "start"), _t(xr - 16, ym - 8, "b", 11, "end"),
         _t(115, yt - 10, "S"), _t(200, yt - 12, I("L"), 12)]
    return _svg(330, 156, b)


FIG_C2 = _fig_lc2()

CH = {17: {
"goal": r"交流の実効値・リアクタンス・位相のずれを使いこなし、RLC 回路のインピーダンスと消費電力、電気振動、変圧器と送電、電磁波の性質を整理する。",
"items": [
 {"lv": "A", "tag": "交流の発生", "q": r"巻数 100、面積 $0.020\,\mathrm{m^2}$ の長方形コイルを、磁束密度 $0.50\,\mathrm T$ の一様な磁場中で、磁場に垂直な軸のまわりに毎秒 50 回転の割合で回転させる。<br>(1) コイルの面が磁場に垂直になった時刻を $t=0$ として、コイルを貫く磁束 $\Phi$ を $t$ の式で表し、誘導起電力が $V=V_0\sin\omega t$ の形になることを示せ。<br>(2) 誘導起電力の最大値 $V_0$ と実効値を求めよ。<br>(3) 回転の速さを 2 倍にすると、最大値と周波数はそれぞれ何倍になるか。",
  "a": r"(1) $\Phi=BS\cos\omega t$、$V=NBS\omega\sin\omega t$　(2) $V_0=100\pi\fallingdotseq314\,\mathrm V$、実効値 $222\,\mathrm V$　(3) どちらも 2 倍",
  "s": r"(1) 面の法線と磁場のなす角が $\omega t$ なので $\Phi=BS\cos\omega t$。$V=-N\dfrac{\Delta\Phi}{\Delta t}$ の $\Delta t\to0$ の極限をとると $V=NBS\omega\sin\omega t$。<br>(2) $\omega=2\pi\times50=100\pi\,\mathrm{rad/s}$。$V_0=100\times0.50\times0.020\times100\pi=100\pi\fallingdotseq314\,\mathrm V$、実効値 $\dfrac{V_0}{\sqrt2}\fallingdotseq222\,\mathrm V$。<br>(3) $V_0\propto\omega$ なので 2 倍、周波数も 2 倍。<br><b>ポイント</b>：発電機の起電力の最大値は $NBS\omega$。実効値は最大値の $\dfrac1{\sqrt2}$。"},
 {"lv": "A", "tag": "実効値と電力", "q": r"実効値 $100\,\mathrm V$ の交流電源に $50\,\Omega$ の抵抗をつなぐ。<br>(1) 電流の実効値と最大値を求めよ。<br>(2) 電圧の最大値を求めよ。<br>(3) 平均の消費電力と、瞬間の消費電力の最大値を求めよ。",
  "a": r"(1) $2.0\,\mathrm A$、$2.8\,\mathrm A$　(2) $141\,\mathrm V$　(3) $200\,\mathrm W$、$400\,\mathrm W$",
  "s": r"(1) $I_e=\dfrac{V_e}R=2.0\,\mathrm A$、$I_0=\sqrt2I_e\fallingdotseq2.8\,\mathrm A$。<br>(2) $V_0=\sqrt2\times100\fallingdotseq141\,\mathrm V$。<br>(3) 瞬間の電力 $P=V_0I_0\sin^2\omega t$ の平均は $\dfrac12V_0I_0=V_eI_e=200\,\mathrm W$。最大値は $V_0I_0=400\,\mathrm W$。<br><b>ポイント</b>：実効値は「同じ抵抗で同じ平均電力を生む直流の値」。抵抗だけの回路では、実効値でオームの法則・電力の式がそのまま使える。"},
 {"lv": "A", "tag": "リアクタンス", "q": r"周波数 $50\,\mathrm{Hz}$、実効値 $100\,\mathrm V$ の交流電源がある。<br>(1) 自己インダクタンス $0.20\,\mathrm H$ のコイル（抵抗は無視）だけをつないだとき、リアクタンスと電流の実効値を求めよ。電流の位相は電圧に対して進むか遅れるか。<br>(2) 電気容量 $50\,\mu\mathrm F$ のコンデンサーだけをつないだとき、リアクタンスと電流の実効値を求めよ。電流の位相は電圧に対して進むか遅れるか。<br>(3) 周波数を $100\,\mathrm{Hz}$ にすると、(1)、(2) のリアクタンスはそれぞれいくらになるか。",
  "a": r"(1) $63\,\Omega$、$1.6\,\mathrm A$、$\dfrac\pi2$ 遅れる　(2) $64\,\Omega$、$1.6\,\mathrm A$、$\dfrac\pi2$ 進む　(3) コイル $1.3\times10^2\,\Omega$、コンデンサー $32\,\Omega$",
  "s": r"(1) $X_L=\omega L=2\pi\times50\times0.20=20\pi\fallingdotseq63\,\Omega$、$I_e=\dfrac{100}{20\pi}\fallingdotseq1.6\,\mathrm A$。コイルは電流の変化を妨げるので、電流は電圧より $\dfrac\pi2$（$\dfrac14$ 周期）遅れる。<br>(2) $X_C=\dfrac1{\omega C}=\dfrac1{2\pi\times50\times50\times10^{-6}}\fallingdotseq64\,\Omega$、$I_e\fallingdotseq1.6\,\mathrm A$。コンデンサーは電荷がたまってから電圧が上がるので、電流は電圧より $\dfrac\pi2$ 進む。<br>(3) $X_L\propto f$ で $40\pi\fallingdotseq1.3\times10^2\,\Omega$、$X_C\propto\dfrac1f$ で $\fallingdotseq32\,\Omega$。<br><b>ポイント</b>：$X_L=\omega L$（高周波ほど通しにくい）、$X_C=\dfrac1{\omega C}$（高周波ほど通しやすい）。コイル・コンデンサーの平均消費電力は 0。"},
 {"lv": "A", "tag": "変圧器・電磁波", "q": r"(1) 1 次コイルの巻数 1000、2 次コイルの巻数 50 の理想的な変圧器の 1 次側に、実効値 $100\,\mathrm V$ の交流電圧をかけた。2 次側の電圧の実効値を求めよ。<br>(2) (1) の 2 次側に $10\,\Omega$ の抵抗をつないだ。2 次側の電流、消費電力、1 次側の電流（いずれも実効値）を求めよ。<br>(3) 振動数 $80\,\mathrm{MHz}$ の電波の波長を求めよ。真空中の光の速さを $3.0\times10^8\,\mathrm{m/s}$ とする。",
  "a": r"(1) $5.0\,\mathrm V$　(2) $0.50\,\mathrm A$、$2.5\,\mathrm W$、$2.5\times10^{-2}\,\mathrm A$　(3) $3.75\,\mathrm m$",
  "s": r"(1) $\dfrac{V_2}{V_1}=\dfrac{N_2}{N_1}$ より $V_2=100\times\dfrac{50}{1000}=5.0\,\mathrm V$。<br>(2) $I_2=\dfrac{5.0}{10}=0.50\,\mathrm A$、$P=5.0\times0.50=2.5\,\mathrm W$。理想的な変圧器では電力が等しいので $I_1=\dfrac{2.5}{100}=2.5\times10^{-2}\,\mathrm A$。<br>(3) $\lambda=\dfrac cf=\dfrac{3.0\times10^8}{80\times10^6}=3.75\,\mathrm m$。<br><b>ポイント</b>：変圧器は「電圧は巻数に比例、電流は巻数に反比例、電力は等しい」。変圧器は直流には使えない（磁束が変化しないため）。"},
 {"lv": "B", "tag": "RLC 直列回路", "q": r"抵抗 $R=30\,\Omega$、コイル、コンデンサーを直列にし、周波数 $50\,\mathrm{Hz}$、実効値 $100\,\mathrm V$ の交流電源につないだ。この周波数でのコイルのリアクタンスは $80\,\Omega$、コンデンサーのリアクタンスは $40\,\Omega$ である。<br>(1) 回路のインピーダンスと、電流の実効値を求めよ。<br>(2) 抵抗・コイル・コンデンサーそれぞれの両端の電圧の実効値を求めよ。コイルの電圧が電源の電圧より大きくなる理由を簡潔に述べよ。<br>(3) 回路の消費電力と力率を求めよ。電流の位相は電源電圧に対して進むか遅れるか。<br>(4) 電源の周波数だけを変えて共振させるには、周波数を何 Hz にすればよいか。",
  "a": r"(1) $50\,\Omega$、$2.0\,\mathrm A$　(2) 抵抗 $60\,\mathrm V$、コイル $160\,\mathrm V$、コンデンサー $80\,\mathrm V$。理由は解説　(3) $120\,\mathrm W$、$0.60$、遅れる　(4) $35\,\mathrm{Hz}$",
  "s": r"(1) $Z=\sqrt{R^2+(X_L-X_C)^2}=\sqrt{30^2+40^2}=50\,\Omega$、$I_e=\dfrac{100}{50}=2.0\,\mathrm A$。<br>(2) $V_R=60\,\mathrm V$、$V_L=160\,\mathrm V$、$V_C=80\,\mathrm V$。コイルとコンデンサーの電圧は位相が $\pi$ ずれていて（互いに逆向き）、瞬間瞬間では打ち消しあう。電源の電圧はベクトル的な和 $\sqrt{60^2+(160-80)^2}=100\,\mathrm V$ なので、一つの素子の電圧が電源電圧を超えてもよい。<br>(3) 電力を消費するのは抵抗だけで $P=I_e^2R=120\,\mathrm W$。力率 $\cos\phi=\dfrac RZ=0.60$（$P=V_eI_e\cos\phi$ と一致）。$X_L\gt X_C$ なのでコイルの性質が勝ち、電流は遅れる。<br>(4) 共振は $X_L=X_C$ のとき。周波数を $k$ 倍すると $X_L=80k$、$X_C=\dfrac{40}k$。$80k=\dfrac{40}k$ より $k=\dfrac1{\sqrt2}$、$f=\dfrac{50}{\sqrt2}\fallingdotseq35\,\mathrm{Hz}$。<br><b>ポイント</b>：直列回路の電圧は単純に足さず、位相を考えて合成する（$Z=\sqrt{R^2+(X_L-X_C)^2}$）。共振周波数は $f_0=\dfrac1{2\pi\sqrt{LC}}$。"},
 {"lv": "B", "tag": "電気振動", "q": r"電気容量 $2.0\,\mu\mathrm F$ のコンデンサーを $10\,\mathrm V$ に充電し、自己インダクタンス $0.50\,\mathrm{mH}$ のコイルとスイッチでつないだ回路をつくる。時刻 $t=0$ にスイッチを閉じた。回路の抵抗は無視する。<br>(1) 電気振動の周期を求めよ。<br>(2) 回路を流れる電流の最大値を求めよ。<br>(3) はじめて電流が最大になる時刻と、そのときのコンデンサーの電気量を求めよ。<br>(4) コンデンサーの電圧が $5.0\,\mathrm V$ のときの電流の大きさを求めよ。",
  "a": r"(1) $2.0\times10^{-4}\,\mathrm s$　(2) $0.63\,\mathrm A$　(3) $5.0\times10^{-5}\,\mathrm s$、$0$　(4) $0.55\,\mathrm A$",
  "s": r"(1) $T=2\pi\sqrt{LC}=2\pi\sqrt{0.50\times10^{-3}\times2.0\times10^{-6}}=2\pi\times10^{-4.5}\fallingdotseq2.0\times10^{-4}\,\mathrm s$。<br>(2) エネルギー保存 $\dfrac12CV_0^2=\dfrac12LI_0^2$ より $I_0=V_0\sqrt{\dfrac CL}=10\times\sqrt{4.0\times10^{-3}}\fallingdotseq0.63\,\mathrm A$。<br>(3) 電流が最大になるのは、コンデンサーの電荷が 0 になって、エネルギーがすべてコイルに移ったとき。それは $\dfrac T4\fallingdotseq5.0\times10^{-5}\,\mathrm s$。<br>(4) $\dfrac12CV_0^2=\dfrac12CV^2+\dfrac12LI^2$ より $I=\sqrt{\dfrac CL(V_0^2-V^2)}=\sqrt{4.0\times10^{-3}\times75}=\sqrt{0.30}\fallingdotseq0.55\,\mathrm A$。<br><b>ポイント</b>：電気振動はばね振り子と同じ形。電気量 ↔ 変位、電流 ↔ 速度、$\dfrac{Q^2}{2C}$ ↔ 弾性エネルギー、$\dfrac12LI^2$ ↔ 運動エネルギー。"},
 {"lv": "B", "tag": "送電と変圧器", "q": r"発電所から $100\,\mathrm{kW}$ の電力を、抵抗が合計 $1.0\,\Omega$ の送電線で送る。電圧・電流は実効値で考え、力率は 1 とする。<br>(1) 送電電圧が $1.0\,\mathrm{kV}$ のとき、送電線を流れる電流と、送電線で失われる電力を求めよ。それは送る電力の何 % か。<br>(2) 変圧器で送電電圧を $10\,\mathrm{kV}$ に上げると、失われる電力はいくらになるか。<br>(3) (2) の変圧器の 1 次コイルと 2 次コイルの巻数の比を求めよ。<br>(4) 送る電力が同じとき、送電線で失われる電力は送電電圧とどのような関係にあるか。",
  "a": r"(1) $100\,\mathrm A$、$10\,\mathrm{kW}$、$10\,\%$　(2) $100\,\mathrm W$（$0.1\,\%$）　(3) $1:10$　(4) 送電電圧の 2 乗に反比例する",
  "s": r"(1) $I=\dfrac PV=\dfrac{100\times10^3}{1.0\times10^3}=100\,\mathrm A$。損失 $I^2r=100^2\times1.0=1.0\times10^4\,\mathrm W$ で $10\,\%$。<br>(2) $I=10\,\mathrm A$、損失 $10^2\times1.0=100\,\mathrm W$（$0.1\,\%$）。<br>(3) 電圧を 10 倍にするので $N_1:N_2=1:10$。<br>(4) $I=\dfrac PV$ より損失 $\left(\dfrac PV\right)^2r\propto\dfrac1{V^2}$。<br><b>ポイント</b>：送電の損失は「電流の 2 乗」で決まる。高電圧にして電流を小さくするのが損失を減らす方法で、電圧を簡単に変えられることが交流送電の利点。"},
 {"lv": "B", "tag": "同調回路・電磁波", "q": r"(1) 自己インダクタンス $0.25\,\mathrm{mH}$ のコイルとコンデンサーで、周波数 $1.0\,\mathrm{MHz}$ の電波に共振（同調）させたい。コンデンサーの電気容量をいくらにすればよいか。$\pi^2=9.87$ とする。<br>(2) この電波の波長を求めよ。真空中の光の速さを $3.0\times10^8\,\mathrm{m/s}$ とする。<br>(3) 同じコイルで $0.50\,\mathrm{MHz}$ の電波に同調させるには、電気容量を何倍にすればよいか。<br>(4) 次の電磁波を、波長の長いものから順に並べよ。<br>X 線、可視光線、電波、紫外線、$\gamma$ 線、赤外線",
  "a": r"(1) $1.0\times10^{-10}\,\mathrm F$　(2) $3.0\times10^2\,\mathrm m$　(3) 4 倍　(4) 電波、赤外線、可視光線、紫外線、X 線、$\gamma$ 線",
  "s": r"(1) $f=\dfrac1{2\pi\sqrt{LC}}$ より $C=\dfrac1{4\pi^2f^2L}=\dfrac1{4\times9.87\times(1.0\times10^6)^2\times0.25\times10^{-3}}\fallingdotseq1.0\times10^{-10}\,\mathrm F$（$100\,\mathrm{pF}$）。<br>(2) $\lambda=\dfrac cf=3.0\times10^2\,\mathrm m$。<br>(3) $C\propto\dfrac1{f^2}$ なので 4 倍。<br>(4) 波長の長い順に、電波、赤外線、可視光線、紫外線、X 線、$\gamma$ 線。どれも真空中を同じ速さ $c$ で進む横波である。<br><b>ポイント</b>：LC 回路の固有周波数 $\dfrac1{2\pi\sqrt{LC}}$ は、ラジオの同調にも電気振動にも共通。電磁波は振動数（波長）で呼び名が変わるだけで、同じ性質の波。"},
 {"lv": "B", "tag": "並列共振", "q": r"自己インダクタンス $10\,\mathrm{mH}$ のコイル（抵抗は無視）と電気容量 $10\,\mu\mathrm F$ のコンデンサーを並列にし、実効値 $10\,\mathrm V$、角周波数 $\omega$ を変えられる交流電源につなぐ。<br>(1) $\omega=2.0\times10^3\,\mathrm{rad/s}$ のとき、コイルとコンデンサーを流れる電流の実効値と、電源を流れる電流の実効値を求めよ。<br>(2) 電源を流れる電流が 0 になる角周波数を求めよ。<br>(3) $\omega=2.0\times10^3\,\mathrm{rad/s}$ 以外で、電源を流れる電流の実効値が (1) と同じになる角周波数を求めよ。",
  "a": r"(1) コイル $0.50\,\mathrm A$、コンデンサー $0.20\,\mathrm A$、電源 $0.30\,\mathrm A$　(2) $3.2\times10^3\,\mathrm{rad/s}$　(3) $5.0\times10^3\,\mathrm{rad/s}$",
  "s": r"(1) 並列なので電圧が共通。$I_L=\dfrac{10}{\omega L}=\dfrac{10}{20}=0.50\,\mathrm A$、$I_C=\omega CV=2.0\times10^3\times10\times10^{-6}\times10=0.20\,\mathrm A$。$I_L$ は電圧より $\dfrac\pi2$ 遅れ、$I_C$ は $\dfrac\pi2$ 進むので、2 つは逆位相。電源の電流は差の $0.30\,\mathrm A$。<br>(2) $I_L=I_C$、すなわち $\dfrac1{\omega L}=\omega C$ のとき 0。$\omega=\dfrac1{\sqrt{LC}}=\dfrac1{\sqrt{10^{-7}}}\fallingdotseq3.2\times10^3\,\mathrm{rad/s}$。コイルとコンデンサーの間を電流が行き来し、電源からは電流が流れない。<br>(3) $I_C-I_L=0.30$ となる場合：$10^{-4}\omega-\dfrac{10^3}\omega=0.30$。$10^{-4}\omega^2-0.30\omega-10^3=0$ より $\omega=\dfrac{0.30+\sqrt{0.09+0.40}}{2\times10^{-4}}=5.0\times10^3\,\mathrm{rad/s}$（$\omega_1\omega_2=\dfrac1{LC}$ を満たす）。<br><b>ポイント</b>：並列回路は「電圧共通」で枝ごとの電流を出し、位相を考えて合成する。並列共振では電源の電流が最小（理想的には 0）になる。"},
 {"lv": "C", "tag": "総合・共振と Q 値", "q": r"抵抗 $R=10\,\Omega$、自己インダクタンス $L=0.10\,\mathrm H$ のコイル、電気容量 $C=10\,\mu\mathrm F$ のコンデンサーを直列にし、実効値 $V=10\,\mathrm V$、角周波数 $\omega$ を変えられる交流電源につなぐ。<br>(1) 回路のインピーダンス $Z$ を $\omega$ の式で表せ。<br>(2) 電流が最大になる角周波数 $\omega_0$ と、そのときの電流の実効値、コイルの両端の電圧の実効値を求めよ。<br>(3) 消費電力が (2) のときの半分になる角周波数 $\omega_1,\ \omega_2\ (\omega_1\lt\omega_2)$ を求めよ。$\sqrt{401}=20.025$ とする。<br>(4) $\omega_1\omega_2=\omega_0^2$、$\omega_2-\omega_1=\dfrac RL$ が成り立つことを示せ。また、$\dfrac{\omega_0}{\omega_2-\omega_1}$ の値を求め、(2) の結果と比べよ。",
  "a": r"(1) $Z=\sqrt{R^2+\left(\omega L-\dfrac1{\omega C}\right)^2}$　(2) $\omega_0=1.0\times10^3\,\mathrm{rad/s}$、$1.0\,\mathrm A$、$1.0\times10^2\,\mathrm V$　(3) $\omega_1\fallingdotseq951\,\mathrm{rad/s}$、$\omega_2\fallingdotseq1051\,\mathrm{rad/s}$　(4) $10$。コイルの電圧が電源電圧の 10 倍であることと一致",
  "s": r"(1) $Z=\sqrt{R^2+\left(\omega L-\dfrac1{\omega C}\right)^2}$。<br>(2) $\omega L=\dfrac1{\omega C}$ で $Z=R$ が最小。$\omega_0=\dfrac1{\sqrt{LC}}=\dfrac1{\sqrt{10^{-6}}}=1.0\times10^3\,\mathrm{rad/s}$。$I=\dfrac VR=1.0\,\mathrm A$、$V_L=\omega_0LI=1.0\times10^3\times0.10\times1.0=1.0\times10^2\,\mathrm V$（コンデンサーも同じ大きさで逆位相）。<br>(3) 電力 $I^2R=\dfrac{V^2R}{Z^2}$ が半分になるのは $Z^2=2R^2$、すなわち $\left|\omega L-\dfrac1{\omega C}\right|=R$。$\omega$ を掛けて整理すると $L\omega^2\mp R\omega-\dfrac1C=0$。正の解は $\omega=\dfrac{\pm R+\sqrt{R^2+4L/C}}{2L}=\dfrac{\pm10+\sqrt{100+40000}}{0.20}$。$\sqrt{40100}=10\sqrt{401}=200.25$ なので $\omega_1=\dfrac{190.25}{0.20}\fallingdotseq951\,\mathrm{rad/s}$、$\omega_2=\dfrac{210.25}{0.20}\fallingdotseq1051\,\mathrm{rad/s}$。<br>(4) $\omega_1$ は $L\omega^2+R\omega-\dfrac1C=0$、$\omega_2$ は $L\omega^2-R\omega-\dfrac1C=0$ の正の解。$\omega_2-\omega_1=\dfrac{2R}{2L}=\dfrac RL$、$\omega_1\omega_2=\dfrac{(R^2+4L/C)-R^2}{4L^2}=\dfrac1{LC}=\omega_0^2$。$\dfrac{\omega_0}{\omega_2-\omega_1}=\dfrac{\omega_0L}R=\dfrac{1.0\times10^3\times0.10}{10}=10$ で、(2) の $\dfrac{V_L}V=\dfrac{100}{10}=10$ と同じ値になる。<br><b>ポイント</b>：共振の鋭さ $Q=\dfrac{\omega_0L}R$ は、共振曲線の幅の逆数であり、共振時にコイルの電圧が電源の何倍になるかも表す。"},
 {"lv": "C", "tag": "総合・2 つのコンデンサーの電気振動", "q": r"図のように、電気容量 $C$ の 2 つのコンデンサー $\mathrm{C_1}$、$\mathrm{C_2}$、自己インダクタンス $L$ のコイル、スイッチ S をつないだ。はじめ $\mathrm{C_1}$ は極板 a 側が正になるように電圧 $V_0$ に充電され、$\mathrm{C_2}$ は電荷をもたない。時刻 $t=0$ に S を閉じる。回路の抵抗と電磁波の放射は無視する。$\mathrm{C_1}$ の極板 a の電気量を $q_1$、$\mathrm{C_2}$ の極板 b の電気量を $q_2$、コイルを a 側から b 側へ流れる電流を $i$ とする。" + FIG_C2 + r"(1) $q_1$ と $q_2$ の間に成り立つ関係と、コイルの自己誘導を含めた回路の式（$L\dfrac{\Delta i}{\Delta t}$ を $q_1,\ q_2,\ C$ で表す式）を書け。<br>(2) 電流が最大になるときの $q_1,\ q_2$ と、電流の最大値を求めよ。<br>(3) $u=q_2-\dfrac{CV_0}2$ とおくと、$u$ は単振動をする。その周期 $T$ を求めよ。<br>(4) $q_2$ がはじめて最大になる時刻と、その最大値を求めよ。そのとき、エネルギーはどこに蓄えられているか。",
  "a": r"(1) $q_1+q_2=CV_0$、$L\dfrac{\Delta i}{\Delta t}=\dfrac{q_1-q_2}C$　(2) $q_1=q_2=\dfrac{CV_0}2$、$V_0\sqrt{\dfrac C{2L}}$　(3) $T=\pi\sqrt{2LC}$　(4) $t=\pi\sqrt{\dfrac{LC}2}$、$CV_0$。すべて $\mathrm{C_2}$ に静電エネルギー $\dfrac12CV_0^2$ として蓄えられている",
  "s": r"(1) a から出た電荷は b に移るだけなので $q_1+q_2=CV_0$。回路を 1 周すると、$\mathrm{C_1}$ の電圧 $\dfrac{q_1}C$ がコイルの起電力と $\mathrm{C_2}$ の電圧の和につりあい、$\dfrac{q_1}C=L\dfrac{\Delta i}{\Delta t}+\dfrac{q_2}C$、すなわち $L\dfrac{\Delta i}{\Delta t}=\dfrac{q_1-q_2}C$。<br>(2) 電流が最大の瞬間は $\dfrac{\Delta i}{\Delta t}=0$ なので $q_1=q_2=\dfrac{CV_0}2$。エネルギー保存 $\dfrac12CV_0^2=2\times\dfrac{(CV_0/2)^2}{2C}+\dfrac12Li^2$ より $\dfrac12Li^2=\dfrac14CV_0^2$、$i=V_0\sqrt{\dfrac C{2L}}$。<br>(3) $i=\dfrac{\Delta q_2}{\Delta t}=\dfrac{\Delta u}{\Delta t}$、$q_1-q_2=CV_0-2q_2=-2u$。(1) の式は $L\dfrac{\Delta i}{\Delta t}=-\dfrac{2}{C}u$ となり、ばね定数 $\dfrac2C$、質量 $L$ の単振動と同じ形。角振動数 $\omega=\sqrt{\dfrac2{LC}}$、$T=\dfrac{2\pi}\omega=\pi\sqrt{2LC}$。<br>(4) $t=0$ で $u=-\dfrac{CV_0}2$、$i=0$ なので $u=-\dfrac{CV_0}2\cos\omega t$、$q_2=\dfrac{CV_0}2(1-\cos\omega t)$。はじめて最大になるのは $\omega t=\pi$、$t=\dfrac T2=\pi\sqrt{\dfrac{LC}2}$ で、$q_2=CV_0$（このとき $q_1=0$、$i=0$）。エネルギー $\dfrac{(CV_0)^2}{2C}=\dfrac12CV_0^2$ はすべて $\mathrm{C_2}$ にある。<br><b>ポイント</b>：電気振動も「つりあいの位置（電流最大の点）のまわりの単振動」として扱える。2 つのコンデンサーの直列の容量 $\dfrac C2$ を使うと $T=2\pi\sqrt{L\cdot\dfrac C2}$ と同じ結果になる。"},
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
    t, w = symbols("t omega", positive=True)
    # A1
    N, S, B = 100, R(2, 100), R(1, 2)
    Phi = B * S * cos(w * t)
    assert simplify(-N * diff(Phi, t) - N * B * S * w * sin(w * t)) == 0
    V0 = N * B * S * 2 * pi * 50
    assert simplify(V0 - 100 * pi) == 0
    _sf(V0, 314, 3); _sf(V0 / sqrt(2), 222, 3)
    # A2
    assert R(100, 50) == 2
    _sf(2 * sqrt(2), 2.8, 2); _sf(100 * sqrt(2), 141, 3)
    assert 100 * 2 == 200 and (100 * sqrt(2)) * (2 * sqrt(2)) == 400
    # A3
    XL = 2 * pi * 50 * R(1, 5); XC = 1 / (2 * pi * 50 * R(50, 10 ** 6))
    _sf(XL, 63, 2); _sf(100 / XL, 1.6, 2); _sf(XC, 64, 2); _sf(100 / XC, 1.6, 2)
    _sf(2 * XL, 130, 2); _sf(XC / 2, 32, 2)
    # A4
    assert 100 * R(50, 1000) == 5 and R(5, 10) == R(1, 2) and 5 * R(1, 2) == R(5, 2) and R(5, 2) / 100 == R(25, 1000)
    assert R(3, 1) * 10 ** 8 / (80 * 10 ** 6) == R(375, 100)
    # B1
    Rr, xl, xc, V = 30, 80, 40, 100
    Z = sqrt(Rr ** 2 + (xl - xc) ** 2)
    Ie = V / Z
    assert Z == 50 and Ie == 2 and Ie * Rr == 60 and Ie * xl == 160 and Ie * xc == 80
    assert sqrt(60 ** 2 + (160 - 80) ** 2) == 100 and Ie ** 2 * Rr == 120 and R(Rr, Z) == R(3, 5)
    k = symbols("k", positive=True)
    kk = solve(Eq(80 * k, 40 / k), k)[0]
    assert kk == 1 / sqrt(2)
    _sf(50 * kk, 35, 2)
    # B2
    C, L, V0 = R(2, 10 ** 6), R(5, 10 ** 4), 10
    T = 2 * pi * sqrt(L * C)
    _sf(T, 2.0e-4, 2); _sf(T / 4, 5.0e-5, 2)
    I0 = V0 * sqrt(C / L)
    _sf(I0, 0.63, 2)
    assert simplify(C * V0 ** 2 / 2 - L * I0 ** 2 / 2) == 0
    I5 = sqrt(C / L * (V0 ** 2 - 25))
    assert I5 == sqrt(R(3, 10))
    _sf(I5, 0.55, 2)
    q = symbols("q", cls=Function)
    sol = dsolve(Eq(L * q(t).diff(t, 2), -q(t) / C), q(t), ics={q(0): C * V0, q(t).diff(t).subs(t, 0): 0})
    qt = sol.rhs
    assert simplify(qt.subs(t, T / 4)) == 0
    assert simplify(Abs(diff(qt, t).subs(t, T / 4)) - I0) == 0
    # B3
    P, r = 100 * 10 ** 3, 1
    I1 = R(P, 1000); I2 = R(P, 10000)
    assert I1 == 100 and I1 ** 2 * r == 10 ** 4 and R(10 ** 4, P) == R(1, 10) and I2 ** 2 * r == 100
    # B4
    pi2 = R(987, 100)
    Cc = 1 / (4 * pi2 * (10 ** 6) ** 2 * R(25, 10 ** 5))
    _sf(Cc, 1.0e-10, 2)
    _sf(1 / (4 * pi ** 2 * (10 ** 6) ** 2 * R(25, 10 ** 5)), 1.0e-10, 2)
    assert R(3, 1) * 10 ** 8 / 10 ** 6 == 300
    assert (1 / (4 * pi2 * (R(1, 2) * 10 ** 6) ** 2 * R(25, 10 ** 5))) / Cc == 4
    # B5
    L, C, V = R(1, 100), R(1, 10 ** 5), 10
    IL = lambda om: V / (om * L); IC = lambda om: om * C * V
    assert IL(2000) == R(1, 2) and IC(2000) == R(1, 5) and IL(2000) - IC(2000) == R(3, 10)
    w0 = 1 / sqrt(L * C)
    _sf(w0, 3.2e3, 2)
    sols = solve(Eq(IC(w) - IL(w), R(3, 10)), w)
    assert sols == [5000] and 2000 * 5000 == 1 / (L * C)
    # C1
    Rr, L, C, V = 10, R(1, 10), R(1, 10 ** 5), 10
    w0 = 1 / sqrt(L * C)
    assert w0 == 1000 and R(V, Rr) == 1 and w0 * L * 1 == 100
    Zw = sqrt(Rr ** 2 + (w * L - 1 / (w * C)) ** 2)
    half = solve(Eq(Zw ** 2, 2 * Rr ** 2), w)
    half = sorted(half, key=lambda e: float(e))
    w1, w2 = half
    _sf(w1, 951, 3); _sf(w2, 1051, 4)
    assert simplify(w1 * w2 - w0 ** 2) == 0 and simplify(w2 - w1 - R(Rr, 1) / L) == 0
    assert simplify(w0 / (w2 - w1)) == 10
    _sf((-10 + 10 * 20.025) / 0.20, 951, 3); _sf((10 + 10 * 20.025) / 0.20, 1051, 4)
    # C2
    Ls, Cs, V0s = symbols("L C V_0", positive=True)
    q2 = Function("q2")
    ode = Eq(Ls * q2(t).diff(t, 2), ((Cs * V0s - q2(t)) - q2(t)) / Cs)
    s2 = dsolve(ode, q2(t), ics={q2(0): 0, q2(t).diff(t).subs(t, 0): 0}).rhs
    om = sqrt(2 / (Ls * Cs))
    assert simplify(s2 - Cs * V0s / 2 * (1 - cos(om * t))) == 0
    tmax = pi / om
    assert simplify(tmax - pi * sqrt(Ls * Cs / 2)) == 0 and simplify(s2.subs(t, tmax) - Cs * V0s) == 0
    imax = diff(s2, t).subs(t, pi / (2 * om))
    assert simplify(imax - V0s * sqrt(Cs / (2 * Ls))) == 0
    assert simplify(2 * pi / om - pi * sqrt(2 * Ls * Cs)) == 0
