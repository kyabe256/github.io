"""大学入試シリーズ（教科書・参考書・問題集）の共通ビルダー。

使い方:  python3 -I nyushi.py <フォルダ>     → <フォルダ>/book.html
meta.json
  kind        … "教科書" | "参考書" | "問題集"
  subject     … 教科名（表紙の帯）
  title, cover_title, cover_sub, color, color2, subcolor, math(bool), intro_html, extra_css
  parts       … [{title, sub, intro, chapters:[{no, title, tag}]}]
教科書・参考書: part*.html を <!--CH n--> で区切る（h2 はビルダーが付ける）
  参考書の解法カードは <div class="pat"><h4>題名</h4> … </div>。番号と巻末索引はビルダーが付ける
問題集: problems.json = {"章番号": {"goal": html, "items": [{"lv":"A|B|C", "tag":"出典の型など", "q":html, "a":答えの要約, "s":解説html}]}}
共通（任意）: appendix*.html … 巻末付録（公式集など）。ファイル名順に入る
"""
import json, re, sys, os, glob

d = sys.argv[1]
meta = json.load(open(os.path.join(d, "meta.json"), encoding="utf-8"))
KIND = meta["kind"]
MATH = meta.get("math", False)
C = meta.get("color", "#1f3f8f")

def esc_math(s):
    if not MATH:
        return s
    return re.sub(r"\$([^$]*)\$", lambda m: "$" + m.group(1).replace("<", r"\lt ").replace(">", r"\gt ") + "$", s)

all_ch = [c for p in meta["parts"] for c in p["chapters"]]
chap = {}
for fn in sorted(glob.glob(os.path.join(d, "part*.html"))):
    ps = re.split(r"<!--CH (\d+)-->", open(fn, encoding="utf-8").read())
    for i in range(1, len(ps), 2):
        chap[int(ps[i])] = ps[i + 1]
probs = json.load(open(os.path.join(d, os.environ.get("PROBS", "problems.json")), encoding="utf-8")) if KIND == "問題集" else {}
apps = [open(f, encoding="utf-8").read() for f in sorted(glob.glob(os.path.join(d, "appendix*.html")))]

if os.environ.get("ONLY"):  # 例: ONLY=2-8 … その章だけで試し刷り（他の章のファイルは読まない）
    a, b = map(int, os.environ["ONLY"].split("-"))
    keep = set(range(a, b + 1))
    chap = {k: v for k, v in chap.items() if k in keep}
    probs = {k: v for k, v in probs.items() if int(k) in keep}
    os.environ["PARTIAL"] = "1"
if os.environ.get("PARTIAL"):  # 書きかけの章を飛ばして試し刷り
    have = set(int(k) for k in probs) if KIND == "問題集" else set(chap)
    for p in meta["parts"]:
        p["chapters"] = [c for c in p["chapters"] if c["no"] in have]
    meta["parts"] = [p for p in meta["parts"] if p["chapters"]]
    all_ch = [c for p in meta["parts"] for c in p["chapters"]]
if KIND == "問題集":
    missing = [c["no"] for c in all_ch if str(c["no"]) not in probs]
else:
    missing = [c["no"] for c in all_ch if c["no"] not in chap]
assert not missing, f"中身がない章: {missing}"

# ---- 参考書：解法カードに通し番号をつけ、索引を集める ----
pat_index = []
def number_patterns(no, html):
    def rep(m):
        n = len(pat_index) + 1
        pat_index.append((n, re.sub(r"<[^>]+>", "", m.group(1)), no))
        return f'<div class="pat" id="pat{n}"><h4><span class="pn">解法 {n:03d}</span>{m.group(1)}</h4>'
    return re.sub(r'<div class="pat">\s*<h4>(.*?)</h4>', rep, html, flags=re.S)

# ---- 問題集 ----
LV = {"A": ("A", "基本", "#2e8b57"), "B": ("B", "標準", "#d27a00"), "C": ("C", "発展", "#c0392b")}
n_prob = sum(len(v["items"]) for v in probs.values())
def prob_html(no):
    pd = probs[str(no)]
    out = [f'<div class="goal">{pd["goal"]}</div>'] if pd.get("goal") else []
    for i, it in enumerate(pd["items"], 1):
        lv, lvn, _ = LV[it["lv"]]
        tag = f'<span class="ptag">{it["tag"]}</span>' if it.get("tag") else ""
        out.append(f'<div class="prob lv{lv}"><div class="ph"><span class="pno">{no}-{i}</span><span class="lv">{lv} {lvn}</span>{tag}'
                   f'<span class="tick">□□□</span></div><div class="pq">{it["q"]}</div></div>')
    return "\n".join(out)
def sol_html():
    out = ['<h1 class="part">解答・解説編<small>答え合わせのあと、解説の「ポイント」を必ず読もう</small></h1>']
    for c in all_ch:
        pd = probs[str(c["no"])]
        out.append(f'<h2 class="solh"><span class="no">{c["no"]}</span>{c["title"]}</h2>')
        for i, it in enumerate(pd["items"], 1):
            lv = it["lv"]
            out.append(f'<div class="sol"><div class="sh"><span class="pno">{c["no"]}-{i}</span><span class="lv lv{lv}">{lv}</span>'
                       f'<span class="sa">答　{it["a"]}</span></div><div class="ss">{it["s"]}</div></div>')
    return "\n".join(out)

# ---- 表紙・使い方・目次 ----
USAGE = {
 "教科書": ["各章は <b>★要点 → 📘講義 → ✏例題 → 🔁確認問題 → 🎯入試の着眼点</b> の順。",
            "講義は「なぜそうなるか」を重視。公式は導き方とセットで覚えると、初見の入試問題にも対応できます。",
            "例題は入試の典型。まず自分で解き、解答と見比べて<b>書き方</b>まで真似しましょう。",
            "確認問題の答えは各章の最後にあります。"],
 "参考書": ["入試に出る考え方を <b>解法カード</b> にまとめました。各カードは <b>「こう出たら」→「こう解く」→ 例題</b> の順。",
            "巻末の <b>解法索引</b> から逆引きできます。問題を見て「どのカードを使うか」がすぐ浮かぶようにするのが目標。",
            "⚠のついた所は、入試で失点が多いポイントです。"],
 "問題集": ["問題は <b>A 基本</b>（教科書・共通テストの基礎）、<b>B 標準</b>（入試の典型）、<b>C 発展</b>（難関大レベル）の3段階。",
            "□□□ は解いた回数のチェック欄。<b>間違えた問題に印</b>をつけ、2周目・3周目で解き直しましょう。",
            "答えと解説は後半の <b>解答・解説編</b> にまとめました。答えだけでなく、解説の流れを自分で再現できるかを確認。",
            "A → B → C の順に。B が7割解ければ一般的な入試の合格ライン、C に挑戦するのは難関大志望者向けです。"],
}[KIND]
toc = []
for p in meta["parts"]:
    toc.append(f'<div><b>{p["title"]}</b></div>')
    toc += [f'<div>{c["no"]}. {c["title"]}</div>' for c in p["chapters"]]
toc.append("<div><b>巻末</b></div>")
if KIND == "問題集":
    toc.append("<div>解答・解説編</div>")
toc += [f'<div>{re.search(r"<h2[^>]*>(.*?)</h2>", a).group(1)}</div>' for a in apps if re.search(r"<h2[^>]*>(.*?)</h2>", a)]
if KIND == "参考書":
    toc.append("<div>解法索引</div>")

body_ch = []
for p in meta["parts"]:
    body_ch.append(f'<h1 class="part">{p["title"]}<small>{p.get("sub","")}</small></h1>{p.get("intro","")}')
    for c in p["chapters"]:
        tag = f' <span class="tag">{c["tag"]}</span>' if c.get("tag") else ""
        body_ch.append(f'<h2><span class="no">{c["no"]}</span>{c["title"]}{tag}</h2>')
        if KIND == "問題集":
            body_ch.append(esc_math(prob_html(c["no"])))
        else:
            h = chap[c["no"]]
            if KIND == "参考書":
                h = number_patterns(c["no"], h)
            body_ch.append(esc_math(h))

count = {"教科書": f'{len(all_ch)}章', "参考書": f'解法カード {len(pat_index)} 枚', "問題集": f'{n_prob} 問'}[KIND]
body = [f'''<div class="cover"><div class="series">大学入試シリーズ　{meta.get("subject","")}</div>
<div class="kind">{KIND}<small>{ {"教科書":"講義編","参考書":"解法・知識の整理編","問題集":"演習編"}[KIND] }</small></div>
<h1>{meta["cover_title"]}</h1><p>{meta["cover_sub"]}</p><p class="cnt">{count}</p></div>
<h2 class="np">この本の使い方</h2><ul>{"".join(f"<li>{u}</li>" for u in USAGE)}</ul>
{meta.get("intro_html","")}
<h3>目次</h3><div class="toc">{"".join(toc)}</div>''']
body += body_ch
if KIND == "問題集":
    body.append(esc_math(sol_html()))
for a in apps:
    body.append(esc_math(a))
if KIND == "参考書":
    rows = []
    for c in all_ch:
        items = [f'<div class="ix"><span class="pn">{n:03d}</span>{t}</div>' for n, t, no in pat_index if no == c["no"]]
        if items:
            rows.append(f'<div class="ixc"><div class="ixh">{c["no"]}. {c["title"]}</div>{"".join(items)}</div>')
    body.append(f'<h2 class="np">解法索引</h2><div class="ixw">{"".join(rows)}</div>')

katex = ('<link rel="stylesheet" href="../../node_modules/katex/dist/katex.min.css"><script src="../../node_modules/katex/dist/katex.min.js"></script>'
         '<script src="../../node_modules/katex/dist/contrib/auto-render.min.js"></script>') if MATH else ""
render = ('renderMathInElement(document.body,{delimiters:[{left:"$$",right:"$$",display:true},{left:"$",right:"$",display:false}],throwOnError:false});' if MATH else "")
html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>{meta["title"]}</title>{katex}
<style>
@page {{ size:A4; }}
:root {{ --main:{C}; --sub:{meta.get("subcolor","#e8eefb")}; --acc:#d9701e; --accbg:#fff4ea; --ok:#2e8b57; --okbg:#edf8f1; --ink:#1e1e1e; --deep:#6b3fa0; }}
* {{ font-synthesis:none; }}
b, strong, h1, h2, h3, h4, th, .box::before, .ph .lv, .pno, .sa, .kind, .series, .ixh, .goal::before {{ text-shadow:0.3px 0 0 currentColor; }}
body {{ font-family:"IPAPGothic","IPAGothic",sans-serif; color:var(--ink); font-size:10pt; line-height:1.68; background:#fff; margin:0; }}
.en, .en * {{ font-family:"Liberation Serif","DejaVu Serif",serif; }} .en {{ font-size:10.8pt; }}
h1.part {{ page-break-before:always; background:var(--main); color:#fff; padding:18mm 10mm; font-size:24pt; margin:0 0 5mm; border-radius:6px; }}
h1.part small {{ display:block; font-size:11pt; opacity:.88; margin-top:3mm; }}
h2 {{ page-break-before:always; font-size:16pt; color:var(--main); border-bottom:3px solid var(--main); padding-bottom:1.5mm; margin:0 0 3mm; page-break-after:avoid; }}
h2 .no {{ display:inline-block; background:var(--main); color:#fff; border-radius:4px; padding:0 8px; margin-right:8px; font-size:12.5pt; }}
h2.cont {{ page-break-before:auto; margin-top:6mm; }}
h2.solh {{ page-break-before:auto; margin-top:6mm; font-size:13pt; }}
h3 {{ font-size:11.8pt; color:var(--main); margin:4mm 0 1.5mm; border-left:6px solid var(--main); padding-left:3mm; page-break-after:avoid; }}
h3.deep {{ color:var(--deep); border-left-color:var(--deep); }}
p {{ margin:1.5mm 0; }}
.box {{ border-radius:6px; padding:2.4mm 3.6mm; margin:2.5mm 0; page-break-inside:avoid; }}
.box::before {{ display:block; font-weight:bold; margin-bottom:0.8mm; }}
.point {{ background:var(--sub); border:2px solid var(--main); }} .point::before {{ content:"★ この章の要点"; color:var(--main); }}
.lect {{ border-left:5px solid var(--main); background:#fafbfd; }} .lect::before {{ content:"📘 講義"; color:var(--main); }}
.ex {{ border:1.5px solid #b9b9b9; }} .ex::before {{ content:"✏ 例題"; }}
.ex .solx {{ margin-top:1.5mm; padding-top:1.5mm; border-top:1px solid #dcdcdc; }}
.chk {{ border:1.5px solid var(--ok); }} .box.chk::before {{ content:"🔁 確認問題"; color:var(--ok); }}
.ans {{ background:var(--okbg); border-left:5px solid var(--ok); }} .ans::before {{ content:"✔ 確認問題の答え"; color:var(--ok); }}
.aim {{ background:var(--accbg); border-left:5px solid var(--acc); }} .aim::before {{ content:"🎯 入試の着眼点"; color:var(--acc); }}
.warn {{ background:#fdecec; border-left:5px solid #c0392b; }} .warn::before {{ content:"⚠ よくあるミス"; color:#c0392b; }}
.memo {{ background:#f4f4f4; }} .memo::before {{ content:"📝 まとめ"; }}
.pat {{ border:2px solid var(--main); border-radius:7px; margin:3mm 0; page-break-inside:avoid; overflow:hidden; }}
.pat h4 {{ margin:0; background:var(--main); color:#fff; padding:1.5mm 3.5mm; font-size:11pt; }}
.pat .pn {{ display:inline-block; background:#fff; color:var(--main); border-radius:3px; padding:0 6px; margin-right:8px; font-size:9pt; }}
.pat .when, .pat .how, .pat .pex, .pat .pnote {{ padding:1.6mm 3.6mm; }}
.pat .when::before {{ content:"こう出たら"; font-weight:bold; color:var(--acc); margin-right:3mm; }}
.pat .how {{ background:var(--sub); }} .pat .how::before {{ content:"こう解く"; display:block; font-weight:bold; color:var(--main); }}
.pat .pex {{ border-top:1px solid #d5d5d5; }} .pat .pex::before {{ content:"例題"; font-weight:bold; margin-right:3mm; }}
.pat .pnote {{ background:#fdecec; font-size:9.4pt; }} .pat .pnote::before {{ content:"⚠ "; }}
.goal {{ background:var(--sub); border-radius:6px; padding:2mm 3.5mm; margin:0 0 3mm; }} .goal::before {{ content:"この章の目標　"; font-weight:bold; color:var(--main); }}
.prob {{ margin:0 0 3mm; page-break-inside:avoid; }}
.prob .ph {{ border-bottom:1.5px solid #bbb; padding-bottom:0.6mm; margin-bottom:1mm; }}
.pno {{ display:inline-block; min-width:12mm; font-weight:bold; color:var(--main); font-size:11pt; }}
.lv {{ display:inline-block; font-size:8.5pt; color:#fff; border-radius:3px; padding:0 5px; margin-right:6px; }}
.lvA .lv, .lv.lvA {{ background:#2e8b57; }} .lvB .lv, .lv.lvB {{ background:#d27a00; }} .lvC .lv, .lv.lvC {{ background:#c0392b; }}
.ptag {{ font-size:8.5pt; color:#666; border:1px solid #bbb; border-radius:3px; padding:0 4px; }}
.ph .tick {{ float:right; letter-spacing:2px; color:#999; }}
.pq {{ padding-left:2mm; }}
.sol {{ margin:0 0 2.6mm; padding:1.6mm 3mm; border-left:4px solid #bbb; page-break-inside:avoid; }}
.sol .sh {{ margin-bottom:0.8mm; }} .sa {{ color:var(--ok); margin-left:2mm; }}
.ss {{ font-size:9.6pt; }}
.tag {{ display:inline-block; font-size:8.5pt; background:#666; color:#fff; border-radius:3px; padding:0 6px; margin-left:6px; vertical-align:middle; }}
table {{ border-collapse:collapse; margin:1.8mm 0; page-break-inside:avoid; }}
td, th {{ border:1px solid #999; padding:0.7mm 2.5mm; text-align:center; }} th {{ background:var(--sub); }}
table.l td, table.l th {{ text-align:left; }} table.w {{ width:100%; }}
svg.fig {{ display:block; margin:2mm auto; page-break-inside:avoid; }}
.two {{ display:flex; gap:5mm; }} .two > div {{ flex:1; }}
.cover {{ height:255mm; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; background:linear-gradient(160deg,{C},{meta.get("color2","#4a6fd0")}); color:#fff; border-radius:8px; }}
.cover .series {{ font-size:14pt; letter-spacing:.25em; border:1.5px solid #fff; padding:1mm 6mm; border-radius:20px; }}
.cover .kind {{ font-size:40pt; margin:8mm 0 2mm; }} .cover .kind small {{ display:block; font-size:14pt; opacity:.9; }}
.cover h1 {{ font-size:22pt; margin:6mm 0 0; line-height:1.4; }} .cover p {{ font-size:12pt; opacity:.93; }} .cover .cnt {{ font-size:13pt; margin-top:6mm; }}
.np {{ page-break-before:always; }}
.toc {{ columns:2; font-size:9.3pt; line-height:1.5; }} .toc div {{ break-inside:avoid; }}
ol li, ul li {{ margin:0.4mm 0; }}
.ixw {{ columns:2; column-gap:8mm; font-size:9pt; }} .ixc {{ break-inside:avoid; margin-bottom:2mm; }}
.ixh {{ font-weight:bold; color:var(--main); border-bottom:1px solid var(--main); margin-bottom:0.6mm; }}
.ix .pn {{ display:inline-block; width:9mm; color:#888; }}
.katex {{ font-size:1.05em; }}
{meta.get("extra_css","")}
</style></head><body>
{"".join(body)}
<script>{render}document.body.setAttribute("data-done","1");</script>
</body></html>"""
open(os.path.join(d, os.environ.get("OUT", "book.html")), "w", encoding="utf-8").write(html)
print("ok", KIND, len(html), count)
