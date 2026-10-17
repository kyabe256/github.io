"""数学 網羅系問題集（例題 約1000題）のビルダー。

使い方:  python3 -I mou.py <フォルダ> <巻>        → <フォルダ>/vol<巻>.html
  例: python3 -I mou.py mou_math 1
  試し刷り: ONLY=5-5 OUT=book_X.html python3 -I mou.py mou_math 1   （その巻のうち、指定の章だけ）
フォルダ/meta.json   … 巻と章の構成（変更しない）
フォルダ/cNN.py      … 1章1ファイル（NN は2桁の章番号）。次の2つを定義する:
  CH = {"no": 章番号, "sections": [
          {"title": "節の題", "base": r"基本事項（要点のHTML、任意）",
           "items": [ {"lv": 1〜5, "title": "例題の題", "q": r"問題", "hint": r"指針", "sol": r"解答",
                       "note": r"検討（任意）", "ex": r"練習（類題）", "exa": r"練習の答え"} , ...]} , ...]}
  def verify(): …  数値・式の答えを assert で検算する
例題・練習の番号はビルダーが巻ごとの通し番号でつける（本文中で番号を参照しない）。
"""
import json, re, sys, os, runpy

d, VOL = sys.argv[1], int(sys.argv[2])
meta = json.load(open(os.path.join(d, "meta.json"), encoding="utf-8"))
vol = [v for v in meta["volumes"] if v["no"] == VOL][0]
chs = vol["chapters"]
if os.environ.get("ONLY"):
    a, b = map(int, os.environ["ONLY"].split("-"))
    chs = [c for c in chs if a <= c <= b]
C, C2, SUB = meta["color"], meta["color2"], meta["subcolor"]

def esc_math(s):
    return re.sub(r"\$([^$]*)\$", lambda m: "$" + m.group(1).replace("<", r"\lt ").replace(">", r"\gt ") + "$", s)

LV = {1: "基礎", 2: "基本", 3: "標準", 4: "発展", 5: "最難関"}
def stars(lv):
    return f'<span class="st st{lv}">{"★" * lv}<span class="off">{"★" * (5 - lv)}</span></span><span class="lvn lv{lv}">{LV[lv]}</span>'

data = {}
for no in chs:
    g = runpy.run_path(os.path.join(d, f"c{no:02d}.py"))
    if "verify" in g:
        g["verify"]()
    ch = g["CH"]
    assert ch["no"] == no, f"c{no:02d}.py の no が違う"
    for s in ch["sections"]:
        assert s["title"] and s["items"], f"第{no}章 空の節"
        for it in s["items"]:
            for k in ("lv", "title", "q", "hint", "sol", "ex", "exa"):
                assert it.get(k) not in (None, ""), f"第{no}章「{it.get('title')}」の {k} が空"
            assert it["lv"] in LV
    data[no] = ch

n = 0
body, toc, answers = [], [], []
cnt = {k: 0 for k in LV}
for no in chs:
    info = meta["chapters"][str(no)]
    body.append(f'<h2><span class="no">{no}</span>{info["title"]}<span class="tag">{info.get("tag","")}</span></h2>')
    toc.append(f'<div class="tc"><b>{no}　{info["title"]}</b></div>')
    answers.append(f'<div class="ah">{no}　{info["title"]}</div>')
    for si, s in enumerate(data[no]["sections"], 1):
        first = n + 1
        body.append(f'<h3><span class="sn">{no}.{si}</span>{s["title"]}</h3>')
        if s.get("base"):
            body.append(f'<div class="base">{s["base"]}</div>')
        for it in s["items"]:
            n += 1
            cnt[it["lv"]] += 1
            note = f'<div class="note"><span class="lb">検討</span>{it["note"]}</div>' if it.get("note") else ""
            body.append(
                f'<div class="rei lv{it["lv"]}"><div class="rhq"><div class="rh"><span class="rno">例題 {n}</span>{stars(it["lv"])}<span class="rt">{it["title"]}</span></div>'
                f'<div class="rq">{it["q"]}</div></div>'
                f'<div class="hint"><span class="lb">指針</span>{it["hint"]}</div>'
                f'<div class="rsol"><span class="lb">解答</span>{it["sol"]}</div>{note}'
                f'<div class="ren"><span class="lb">練習 {n}</span>{it["ex"]}</div></div>')
            answers.append(f'<div class="ai"><b>練習 {n}</b>　{it["exa"]}</div>')
        toc.append(f'<div class="ts">{no}.{si}　{s["title"]}<span class="tr">例題 {first}〜{n}</span></div>')

USAGE = [
    "各節は <b>基本事項 → 例題</b> の順。例題は <b>問題 → 指針（方針の立て方） → 解答 → 検討（別解・発展・注意）</b> で、最後に同じ考え方で解ける <b>練習</b> がつく。練習の答えは巻末にある。",
    "難易度は ★ の数で5段階：" + "、".join(f"{'★' * k}{LV[k]}" for k in LV) + "。",
    "目安：★1〜2 は教科書・共通テストの基礎、★3 は一般的な入試の典型、★4 は難関大の標準、★5 は東大・京大など最難関大で差がつくレベル。",
    "まず指針を隠して自分で方針を立て、解答と見比べる。解けなかった例題は練習で確かめ、日をおいてもう一度解こう。",
]
dist = "　".join(f"{'★' * k}：{cnt[k]}題" for k in LV)
title = f'{meta["series"]}　第{VOL}巻　{vol["title"]}'
cover = f'''<div class="cover"><div class="series">{meta["series"]}</div>
<div class="kind">第{VOL}巻<small>{vol["title"]}</small></div>
<h1>{meta["cover_title"]}</h1><p>{vol["sub"]}</p><p class="cnt">例題 {n} 題・練習 {n} 題</p></div>
<h2 class="np">この本の使い方</h2><ul>{"".join(f"<li>{u}</li>" for u in USAGE)}</ul>
<p class="dist">この巻の例題の難易度の内訳：{dist}</p>
<h3 class="tch">目次</h3><div class="toc">{"".join(toc)}<div class="tc"><b>巻末　練習の答え</b></div></div>'''
html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="../../node_modules/katex/dist/katex.min.css"><script src="../../node_modules/katex/dist/katex.min.js"></script>
<script src="../../node_modules/katex/dist/contrib/auto-render.min.js"></script>
<style>
@page {{ size:A4; }}
:root {{ --main:{C}; --sub:{SUB}; --ink:#1e1e1e; --acc:#d9701e; --ok:#2e8b57; }}
* {{ font-synthesis:none; }}
b, strong, h1, h2, h3, .rno, .lb, .kind, .series, .tc b, .ah, .ai b {{ text-shadow:0.3px 0 0 currentColor; }}
body {{ font-family:"IPAPGothic","IPAGothic",sans-serif; color:var(--ink); font-size:9.6pt; line-height:1.56; margin:0; background:#fff; }}
h2 {{ page-break-before:always; font-size:15pt; color:var(--main); border-bottom:3px solid var(--main); padding-bottom:1.2mm; margin:0 0 3mm; page-break-after:avoid; }}
h2 .no {{ display:inline-block; background:var(--main); color:#fff; border-radius:4px; padding:0 8px; margin-right:8px; font-size:12pt; }}
h2 .tag {{ font-size:9pt; color:#fff; background:#666; border-radius:3px; padding:0 6px; margin-left:8px; vertical-align:middle; }}
h3 {{ font-size:11.5pt; color:#fff; background:var(--main); padding:1mm 3mm; margin:4mm 0 2mm; border-radius:3px; page-break-after:avoid; }}
h3 .sn {{ margin-right:3mm; opacity:.85; }}
.base {{ background:var(--sub); border:1.5px solid var(--main); border-radius:5px; padding:1.8mm 3.2mm; margin:0 0 2.5mm; page-break-inside:avoid; }}
.base::before {{ content:"基本事項"; display:block; font-weight:bold; color:var(--main); text-shadow:0.3px 0 0 currentColor; }}
.rei {{ border:1.4px solid #9aa9cc; border-radius:5px; margin:0 0 3mm; padding:0; }}
.rhq {{ page-break-inside:avoid; }}
.rh {{ background:#eef2fa; border-bottom:1px solid #c5cfe6; padding:0.8mm 3mm; border-radius:5px 5px 0 0; }}
.rno {{ color:var(--main); font-size:10.5pt; margin-right:3mm; }}
.st {{ color:#d9a400; letter-spacing:-1px; margin-right:1.5mm; }} .st .off {{ color:#d6d6d6; }}
.lvn {{ display:inline-block; font-size:7.8pt; color:#fff; border-radius:3px; padding:0 4px; margin-right:3mm; vertical-align:1px; }}
.lv1 .lvn, .lvn.lv1 {{ background:#5a9e6f; }} .lvn.lv2 {{ background:#2e8b57; }} .lvn.lv3 {{ background:#d27a00; }} .lvn.lv4 {{ background:#c0392b; }} .lvn.lv5 {{ background:#6b1f7a; }}
.rt {{ font-weight:bold; text-shadow:0.3px 0 0 currentColor; }}
.rq {{ padding:1.4mm 3mm 1.2mm; }}
.hint {{ background:#fff7ea; border-top:1px solid #f0d9b5; padding:1.2mm 3mm; font-size:9.2pt; }}
.rsol {{ padding:1.4mm 3mm; border-top:1px solid #dde3ef; }}
.note {{ background:#f3f6f3; border-top:1px solid #d6e2d6; padding:1.2mm 3mm; font-size:9.1pt; }}
.ren {{ background:#f5f5f5; border-top:1px solid #ddd; padding:1.2mm 3mm; border-radius:0 0 5px 5px; page-break-inside:avoid; }}
.lb {{ display:inline-block; font-weight:bold; margin-right:2.5mm; }}
.hint .lb {{ color:var(--acc); }} .rsol .lb {{ color:var(--main); }} .note .lb {{ color:var(--ok); }} .ren .lb {{ color:#555; }}
.rei.lv5 {{ border-color:#8e5a99; }} .rei.lv5 .rh {{ background:#f4ecf6; }}
table {{ border-collapse:collapse; margin:1.5mm 0; page-break-inside:avoid; }} td, th {{ border:1px solid #999; padding:0.5mm 2.2mm; text-align:center; }} th {{ background:var(--sub); }}
svg.fig {{ display:block; margin:1.5mm auto; page-break-inside:avoid; }}
.rq svg.fig, .rsol svg.fig {{ float:right; margin:0.5mm 0 1mm 4mm; }} .rq, .rsol {{ display:flow-root; }}
.two {{ display:flex; gap:5mm; }} .two > div {{ flex:1; }}
.cover {{ height:255mm; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; background:linear-gradient(160deg,{C},{C2}); color:#fff; border-radius:8px; }}
.cover .series {{ font-size:14pt; letter-spacing:.2em; border:1.5px solid #fff; padding:1mm 6mm; border-radius:20px; }}
.cover .kind {{ font-size:38pt; margin:8mm 0 2mm; }} .cover .kind small {{ display:block; font-size:16pt; opacity:.92; margin-top:2mm; }}
.cover h1 {{ font-size:22pt; margin:6mm 0 0; line-height:1.4; }} .cover p {{ font-size:12pt; opacity:.93; }} .cover .cnt {{ font-size:13pt; margin-top:6mm; }}
.np {{ page-break-before:always; }}
.dist {{ font-size:9.2pt; }}
h3.tch {{ background:none; color:var(--main); padding:0; border-left:5px solid var(--main); padding-left:3mm; border-radius:0; }}
.toc {{ columns:2; column-gap:8mm; font-size:8.8pt; line-height:1.45; }} .toc .tc {{ margin-top:1.5mm; break-after:avoid; }} .toc .ts {{ display:flex; break-inside:avoid; }} .toc .tr {{ margin-left:auto; color:#777; padding-left:2mm; white-space:nowrap; }}
.ans {{ font-size:8.9pt; line-height:1.5; }} .ah {{ color:var(--main); border-bottom:1.5px solid var(--main); margin:3mm 0 1mm; break-after:avoid; }}
.ai {{ margin:0 0 0.8mm; break-inside:avoid; }} .ai b {{ color:var(--main); }}
ul li {{ margin:0.5mm 0; }}
.katex {{ font-size:1.04em; }}
</style></head><body>
{cover}
{esc_math("".join(body))}
<h2>練習の答え</h2><div class="ans">{esc_math("".join(answers))}</div>
<script>renderMathInElement(document.body,{{delimiters:[{{left:"$",right:"$",display:false}}],throwOnError:false}});document.body.setAttribute("data-done","1");</script>
</body></html>"""
out = os.environ.get("OUT", f"vol{VOL}.html")
open(os.path.join(d, out), "w", encoding="utf-8").write(html)
print("ok", title, f"例題 {n}", cnt)
