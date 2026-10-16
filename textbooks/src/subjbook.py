"""教科別「一気読み教科書」の共通ビルダー。

使い方:  python3 -I subjbook.py <教科フォルダ>   （例: books/eng）
フォルダの中身:
  meta.json      … タイトル・色・部と章の構成・使い方ページ
  part*.html     … 章の本文。<!--CH n--> で区切る（h2 見出しはビルダーが付ける）
  drills.json    … {章番号: {"title":..., "items": [[問題HTML, 答えHTML], ...]}}
  glossary.json  … [[用語, よみ, 説明, 章], ...]
  sougou.html    … 総合演習（任意）
出力:  <フォルダ>/book.html
"""
import json, re, sys, os, glob

d = sys.argv[1]
meta = json.load(open(os.path.join(d, "meta.json"), encoding="utf-8"))
MATH = meta.get("math", False)

# ---- 章本文 ----
chap = {}
for fn in sorted(glob.glob(os.path.join(d, "part*.html"))):
    parts = re.split(r"<!--CH (\d+)-->", open(fn, encoding="utf-8").read())
    for i in range(1, len(parts), 2):
        chap[int(parts[i])] = parts[i + 1]
drills = json.load(open(os.path.join(d, "drills.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "drills.json")) else {}
gloss = json.load(open(os.path.join(d, "glossary.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "glossary.json")) else []
sougou = open(os.path.join(d, "sougou.html"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "sougou.html")) else ""

all_ch = [c for p in meta["parts"] for c in p["chapters"]]
missing = [c["no"] for c in all_ch if c["no"] not in chap]
assert not missing, f"本文がない章: {missing}"

def esc_math(s):
    if not MATH:
        return s
    return re.sub(r"\$([^$]*)\$", lambda m: "$" + m.group(1).replace("<", r"\lt ").replace(">", r"\gt ") + "$", s)

def drill_html(no):
    dd = drills.get(str(no))
    if not dd:
        return ""
    lis = "\n".join(f"<li>{q}</li>" for q, _ in dd["items"])
    cls = "dl one" if dd.get("one") else "dl"
    return (f'<div class="drill"><h3 class="drillh">🧮 {meta.get("drill_name","一問一答ドリル")}：{dd["title"]}（{len(dd["items"])}問）'
            f'<small>答えは巻末</small></h3>\n<ol class="{cls}">{lis}</ol></div>')

# ---- 表紙・使い方・目次 ----
toc = []
for p in meta["parts"]:
    toc.append(f'<div><b>{p["title"]}</b></div>')
    toc += [f'<div>{c["no"]}. {c["title"]}</div>' for c in p["chapters"]]
toc.append("<div><b>巻末</b></div>")
if sougou:
    toc.append("<div>総合演習</div>")
toc += ["<div>ドリル解答</div>", "<div>用語集（五十音順）</div>"]
n_drill = sum(len(v["items"]) for v in drills.values())

body = [f'''<div class="cover"><p style="font-size:15pt;letter-spacing:.3em">ざーッと一気に</p>
<h1>{meta["cover_title"]}</h1><p>{meta["cover_sub"]}<br>じっくり解説・入試チャレンジ・{meta.get("drill_name","一問一答ドリル")}{n_drill}問 収録</p></div>
<h2 class="np">この本の使い方</h2>
<ul>
<li><b>各章は2段構え。</b>前半（★〜🔁）で要点を一気に、後半「▼もっと詳しく」で理由・背景・応用までじっくり。</li>
<li>後半には <b>📘じっくり解説</b>、追加の例題、<b>🏆入試チャレンジ</b>、<b>🧮{meta.get("drill_name","一問一答ドリル")}</b>（答えは巻末）があります。</li>
<li><b>一周目は前半だけ</b>読んで全体をつかみ、二周目で後半に取り組むのがおすすめ。</li>
<li>わからない章があったら、<b>前の章に戻る</b>のが一番の近道です。</li>
</ul>
{meta.get("intro_html","")}
<h3>目次</h3><div class="toc">{"".join(toc)}</div>''']

for p in meta["parts"]:
    body.append(f'<h1 class="part">{p["title"]}<small>{p.get("sub","")}</small></h1>{p.get("intro","")}')
    for c in p["chapters"]:
        tag = f' <span class="tag">{c["tag"]}</span>' if c.get("tag") else ""
        body.append(f'<!-- ch{c["no"]} --><h2><span class="no">{c["no"]}</span>{c["title"]}{tag}</h2>')
        body.append(esc_math(chap[c["no"]]))
        body.append(esc_math(drill_html(c["no"])))

if sougou:
    body.append(esc_math(sougou))

# ---- 巻末：ドリル解答 ----
ans = ['<h2>巻末　ドリル解答</h2>']
for c in all_ch:
    dd = drills.get(str(c["no"]))
    if not dd:
        continue
    items = " ".join(f'<span class="ai"><b>({i})</b> {a}</span>' for i, (_, a) in enumerate(dd["items"], 1))
    ans.append(f'<div class="dans"><div class="dt">第{c["no"]}章　{dd["title"]}</div>{items}</div>')
body.append(esc_math("\n".join(ans)))

# ---- 巻末：用語集 ----
groups = [("あ", "あいうえお"), ("か", "かきくけこがぎぐげご"), ("さ", "さしすせそざじずぜぞ"), ("た", "たちつてとだぢづでど"),
          ("な", "なにぬねの"), ("は", "はひふへほばびぶべぼぱぴぷぺぽ"), ("ま", "まみむめも"), ("や", "やゆよ"), ("ら", "らりるれろ"), ("わ", "わをん")]
def grp(r):
    for g, cs in groups:
        if r[0] in cs:
            return g
    return "英数"
if gloss:
    gloss = sorted(gloss, key=lambda t: t[1])
    rows, cur = [], None
    for t in gloss:
        g = grp(t[1])
        if g != cur:
            cur = g
            rows.append(f'<tr class="gh"><td colspan="3">{g}</td></tr>')
        rows.append(f'<tr><td class="gt"><b>{t[0]}</b><br><small>{t[1]}</small></td><td>{t[2]}</td><td class="gc">{t[3]}</td></tr>')
    body.append(esc_math(f'<h2>巻末　用語集（五十音順）</h2><p>主な用語をまとめました。右端の数字は詳しく扱っている章です。</p><table class="gloss">{"".join(rows)}</table>'))

C = meta.get("color", "#1f5fa8")
katex = ('<link rel="stylesheet" href="../../node_modules/katex/dist/katex.min.css"><script src="../../node_modules/katex/dist/katex.min.js"></script>'
         '<script src="../../node_modules/katex/dist/contrib/auto-render.min.js"></script>') if MATH else ""
render = ('renderMathInElement(document.body,{delimiters:[{left:"$",right:"$",display:false}],throwOnError:false});' if MATH else "")
html = f"""<!doctype html><html lang="ja"><head><meta charset="utf-8"><title>{meta["title"]}</title>{katex}
<style>
@page {{ size: A4; margin: 16mm 15mm 18mm 15mm; }}
:root {{ --main:{C}; --sub:{meta.get("subcolor","#e8f0fb")}; --acc:#e0702a; --accbg:#fff3ea; --ok:#2e8b57; --okbg:#ecf8f1; --ink:#222; }}
body {{ font-family:"IPAPGothic","IPAGothic",sans-serif; color:var(--ink); font-size:10.5pt; line-height:1.75; background:#fff; margin:0; }}
.en, .en * {{ font-family:"Liberation Serif","DejaVu Serif",serif; }}
.en {{ font-size:11.5pt; }}
h1.part {{ page-break-before: always; background:var(--main); color:#fff; padding:28mm 10mm; font-size:28pt; margin:0 0 6mm; border-radius:6px; }}
h1.part small {{ display:block; font-size:12pt; opacity:.85; margin-top:4mm; font-weight:normal; }}
h2 {{ page-break-before: always; font-size:17pt; color:var(--main); border-bottom:3px solid var(--main); padding-bottom:2mm; margin:0 0 4mm; }}
h2 .no {{ display:inline-block; background:var(--main); color:#fff; border-radius:4px; padding:0 8px; margin-right:8px; font-size:13pt; }}
h2.cont {{ page-break-before:auto; margin-top:8mm; }}
h3 {{ font-size:12.5pt; color:var(--main); margin:5mm 0 2mm; border-left:6px solid var(--main); padding-left:3mm; page-break-after:avoid; }}
h3.deep {{ color:#7a3db8; border-left-color:#7a3db8; }}
.box {{ border-radius:6px; padding:3mm 4mm; margin:3mm 0; page-break-inside: avoid; }}
.point {{ background:var(--sub); border:2px solid var(--main); }}
.point::before {{ content:"★ ここだけ覚える"; display:block; font-weight:bold; color:var(--main); margin-bottom:1mm; }}
.image {{ background:var(--accbg); border-left:6px solid var(--acc); }}
.image::before {{ content:"💡 イメージで言うと"; display:block; font-weight:bold; color:var(--acc); margin-bottom:1mm; }}
.ex {{ border:1.5px dashed #888; }}
.ex::before {{ content:"✏ 例題"; display:block; font-weight:bold; margin-bottom:1mm; }}
.ans {{ background:var(--okbg); border-left:6px solid var(--ok); }}
.ans::before {{ content:"✔ 練習の答え"; display:block; font-weight:bold; color:var(--ok); margin-bottom:1mm; }}
.prac {{ border:1.5px solid var(--ok); }}
.prac::before {{ content:"🔁 練習問題"; display:block; font-weight:bold; color:var(--ok); margin-bottom:1mm; }}
.warn {{ background:#fdecec; border-left:6px solid #c0392b; }}
.warn::before {{ content:"⚠ よくあるミス"; display:block; font-weight:bold; color:#c0392b; margin-bottom:1mm; }}
.challenge {{ border:2px solid #7a3db8; background:#faf6ff; }}
.challenge::before {{ content:"🏆 入試チャレンジ"; display:block; font-weight:bold; color:#7a3db8; margin-bottom:1mm; }}
.q {{ border:1.5px solid var(--main); }}
.q::before {{ content:"📝 問題"; display:block; font-weight:bold; color:var(--main); margin-bottom:1mm; }}
.hint {{ background:var(--accbg); border-left:6px solid var(--acc); }}
.hint::before {{ content:"💡 方針"; display:block; font-weight:bold; color:var(--acc); margin-bottom:1mm; }}
.sol {{ background:var(--okbg); border-left:6px solid var(--ok); }}
.sol::before {{ content:"✔ 解答"; display:block; font-weight:bold; color:var(--ok); margin-bottom:1mm; }}
.moreh {{ margin:7mm 0 2mm; padding:1.5mm 4mm; background:#f3ecfb; color:#7a3db8; font-weight:bold; border-radius:4px; page-break-after: avoid; }}
.tag {{ display:inline-block; font-size:8.5pt; background:#666; color:#fff; border-radius:3px; padding:0 6px; margin-left:6px; vertical-align:middle; }}
table {{ border-collapse:collapse; margin:2mm 0; page-break-inside: avoid; }}
td, th {{ border:1px solid #999; padding:1mm 3mm; text-align:center; }}
th {{ background:var(--sub); }}
table.l td, table.l th {{ text-align:left; }}
table.w {{ width:100%; }}
.fig {{ text-align:center; margin:2mm 0; page-break-inside: avoid; }}
.fig svg {{ max-width:100%; }}
.two {{ display:flex; gap:5mm; align-items:flex-start; }} .two > div {{ flex:1; }}
.cover {{ height:255mm; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; background:linear-gradient(160deg,{C},{meta.get("color2","#3a8be0")}); color:#fff; border-radius:8px; }}
.cover h1 {{ font-size:32pt; margin:0; line-height:1.3; }}
.cover p {{ font-size:13pt; opacity:.92; }}
.np {{ page-break-before:always; }}
.toc {{ columns:2; font-size:10pt; }} .toc div {{ break-inside: avoid; }}
ol li, ul li {{ margin:0.5mm 0; }}
.drill {{ margin-top:6mm; border-top:3px double #2e8b57; padding-top:2mm; }}
h3.drillh {{ color:#2e8b57; border-left-color:#2e8b57; }}
h3.drillh small {{ font-weight:normal; font-size:8.5pt; color:#666; margin-left:3mm; }}
ol.dl {{ columns:2; column-gap:8mm; padding-left:7mm; margin:1mm 0; font-size:10pt; }}
ol.dl.one {{ columns:1; }}
ol.dl li {{ break-inside: avoid; margin:0 0 2mm; padding-left:1mm; }}
.dans {{ font-size:9pt; line-height:1.7; margin:0 0 3mm; }}
.dans .dt {{ font-weight:bold; color:#2e8b57; border-bottom:1px solid #2e8b57; margin-bottom:1mm; }}
.dans .ai {{ display:inline-block; margin-right:5mm; }}
table.gloss {{ width:100%; font-size:9.5pt; page-break-inside:auto; }}
table.gloss td {{ text-align:left; vertical-align:top; padding:1mm 2mm; }} table.gloss tr {{ page-break-inside:avoid; }}
table.gloss td.gt {{ width:28%; }} table.gloss td.gc {{ width:6%; text-align:center; color:#666; }}
table.gloss tr.gh td {{ background:var(--main); color:#fff; font-weight:bold; }}
.kb {{ display:inline-block; border:1px solid #999; border-radius:3px; padding:0 4px; font-size:9pt; }}
.big {{ font-size:13pt; }}
u.w {{ text-decoration:none; border-bottom:2px solid var(--acc); }}
.kt {{ font-size:13pt; letter-spacing:.05em; }}
.kt sub {{ font-size:7pt; vertical-align:-0.3em; color:#c0392b; }}
{meta.get("extra_css","")}
</style></head><body>
{"".join(body)}
<script>{render}document.body.setAttribute('data-done','1');</script>
</body></html>"""
open(os.path.join(d, "book.html"), "w", encoding="utf-8").write(html)
print("ok", len(html), "drills:", n_drill, "glossary:", len(gloss))
