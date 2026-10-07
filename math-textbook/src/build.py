"""book.html（本体）に ext*.html（加筆）と drills.json（ドリル）を差し込み book_full.html を作る。"""
import json, re

base = open("book.html", encoding="utf-8").read()
drills = json.load(open("drills.json", encoding="utf-8"))

def esc_math(s):
    # $...$ の中の < > を KaTeX 用に \lt \gt に（HTML タグと誤認されないように）
    return re.sub(r"\$([^$]*)\$", lambda m: "$" + m.group(1).replace("<", r"\lt ").replace(">", r"\gt ") + "$", s)

JP = re.compile(r"([　-ヿ一-鿿＀-￯]+)")

def as_math(s):
    """ドリル1項目を HTML に。$ を含めば地の文、含まなければ全体を数式とみなす。"""
    if "$" in s:
        return esc_math(s)
    s = JP.sub(lambda m: r"\text{" + m.group(1) + "}", s)
    return esc_math("$" + s + "$")

# ---- 加筆原稿を章ごとに分解 ----
ext = {}
for fn in ["ext1.html", "ext2.html", "ext3.html", "ext4.html"]:
    txt = open(fn, encoding="utf-8").read()
    parts = re.split(r"<!--EXT (\d+)-->", txt)
    for i in range(1, len(parts), 2):
        ext[int(parts[i])] = esc_math(parts[i + 1])
assert sorted(ext) == list(range(1, 35)), sorted(ext)

def drill_html(ch):
    d = drills[str(ch)]
    lis = "\n".join(f"<li>{as_math(q)}</li>" for q, _ in d["items"])
    return (f'<div class="drill"><h3 class="drillh">🧮 計算ドリル：{d["title"]}（{len(d["items"])}問）'
            f'<small>答えは巻末「ドリル解答」</small></h3>\n<ol class="dl">{lis}</ol></div>')

# ---- 各章の「練習の答え」ボックスの直後に差し込む ----
out = base
for ch in range(1, 35):
    m = re.search(rf'<h2><span class="no">{ch}</span>', out)
    assert m, ch
    a = out.index('<div class="box ans">', m.end())
    end = out.index("</div>", a) + len("</div>")
    block = ('\n<div class="moreh">▼ ここから「もっと詳しく」</div>\n' + ext[ch] + "\n" + drill_html(ch) + "\n")
    out = out[:end] + block + out[end:]

# ---- 巻末ドリル解答 ----
ans = ['<h2>巻末　計算ドリル解答</h2>',
       '<p>すべての答えはコンピュータ代数（sympy）で計算・検算しています。分数は既約、根号は簡単にした形です。答えの形が違っても同値なら正解です。</p>']
for ch in range(1, 35):
    d = drills[str(ch)]
    items = " ".join(f'<span class="ai"><b>({i})</b> {as_math(a)}</span>' for i, (_, a) in enumerate(d["items"], 1))
    ans.append(f'<div class="dans"><div class="dt">第{ch}章　{d["title"]}</div>{items}</div>')
ans_html = "\n".join(ans)
sougou = esc_math(open("sougou.html", encoding="utf-8").read())
gloss = esc_math(open("glossary.html", encoding="utf-8").read())
owari = '<h2 class="cont" style="page-break-before:always">おわりに'
assert owari in out
out = out.replace(owari, sougou + "\n" + owari)
tail = "\n<script>\nrenderMath"
assert tail in out
out = out.replace(tail, "\n" + ans_html + "\n" + gloss + tail)

# ---- 追加 CSS ----
css = """
h3.deep { color:#7a3db8; border-left-color:#7a3db8; }
.moreh { margin:7mm 0 2mm; padding:1.5mm 4mm; background:#f3ecfb; color:#7a3db8; font-weight:bold; border-radius:4px; page-break-after: avoid; }
.challenge { border:2px solid #7a3db8; background:#faf6ff; }
.challenge::before { content:"🏆 入試チャレンジ"; display:block; font-weight:bold; color:#7a3db8; margin-bottom:1mm; }
.drill { margin-top:6mm; border-top:3px double #2e8b57; padding-top:2mm; }
h3.drillh { color:#2e8b57; border-left-color:#2e8b57; page-break-after: avoid; }
h3.drillh small { font-weight:normal; font-size:8.5pt; color:#666; margin-left:3mm; }
ol.dl { columns:2; column-gap:8mm; padding-left:7mm; margin:1mm 0; font-size:10pt; }
ol.dl li { break-inside: avoid; margin:0 0 2.2mm; padding-left:1mm; }
.dans { font-size:9pt; line-height:1.7; margin:0 0 3mm; page-break-inside:auto; }
.dans .dt { font-weight:bold; color:#2e8b57; border-bottom:1px solid #2e8b57; margin-bottom:1mm; }
.dans .ai { display:inline-block; margin-right:5mm; }
.q { border:1.5px solid #1f5fa8; background:#fff; }
.q::before { content:"📝 問題"; display:block; font-weight:bold; color:#1f5fa8; margin-bottom:1mm; }
.hint { background:var(--accbg); border-left:6px solid var(--acc); }
.hint::before { content:"💡 方針"; display:block; font-weight:bold; color:var(--acc); margin-bottom:1mm; }
.sol { background:var(--okbg); border-left:6px solid var(--ok); }
.sol::before { content:"✔ 解答"; display:block; font-weight:bold; color:var(--ok); margin-bottom:1mm; }
table.gloss { width:100%; font-size:9.5pt; }
table.gloss td { text-align:left; vertical-align:top; padding:1mm 2mm; }
table.gloss td.gt { width:28%; } table.gloss td.gc { width:6%; text-align:center; color:#666; }
table.gloss tr.gh td { background:#1f5fa8; color:#fff; font-weight:bold; }
table.gloss { page-break-inside:auto; } table.gloss tr { page-break-inside:avoid; }
"""
out = out.replace("</style>", css + "</style>", 1)

# ---- 表紙・使い方の更新 ----
out = out.replace("「なぜそうなるか」をイメージでつかむ全34章",
                  "「なぜそうなるか」をイメージでつかむ全34章<br>じっくり解説・入試チャレンジ・計算ドリル1500問以上・総合演習31題・用語集 収録")
out = out.replace("<li><b>1章 = 2〜3ページ。</b> 細かい例外より「つまり何をしているのか」を優先しています。</li>",
                  "<li><b>各章は2段構え。</b>前半（★〜🔁）で要点を一気に、後半「▼もっと詳しく」で理由・証明・応用までじっくり。</li>\n"
                  "  <li>後半には <b>📘じっくり解説</b>、追加の ✏例題、<b>🏆入試チャレンジ</b>、<b>🧮計算ドリル</b>（答えは巻末）があります。</li>\n"
                  "  <li><b>一周目は前半だけ</b>読んで全体をつかみ、二周目で後半に取り組むのがおすすめ。</li>")

out = out.replace("<div><b>付録</b> 公式まとめ</div>", "<div><b>巻末</b></div><div>総合演習（入試レベル31題）</div><div>公式まとめ</div><div>計算ドリル解答</div><div>用語集（五十音順）</div>")
open("book_full.html", "w", encoding="utf-8").write(out)
print("ok", len(out))
