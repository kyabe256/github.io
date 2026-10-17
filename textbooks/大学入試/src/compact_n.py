"""入試シリーズの圧縮版ビルド用ディレクトリをつくる: python3 -I compact_n.py n_phy_m → n_phy_m_c/
中身（問題・解説）はそのまま。章ごとの改ページと部の扉をやめ、文字・余白・図を詰める。"""
import json, os, re, sys, glob, shutil
src = sys.argv[1].rstrip("/"); dst = src + "_c"
os.makedirs(dst, exist_ok=True)
SCALE = float(os.environ.get("SVGSCALE", "0.82"))  # 図の縮小率（width/height 属性を書き換える）。図中の文字が多い本では縮小で PDF が重くなることがあるので、そのときは SVGSCALE=1
def shrink_svg(m):
    tag = m.group(0)
    if "viewBox" not in tag:
        return tag
    return re.sub(r'\b(width|height)=(\\?")([\d.]+)(\\?")',
                  lambda a: f'{a.group(1)}={a.group(2)}{float(a.group(3)) * SCALE:.0f}{a.group(4)}', tag)
for f in glob.glob(os.path.join(src, "*")):
    b = os.path.basename(f)
    if b == "meta.json" or b.startswith("book") or f.endswith(".pdf") or os.path.isdir(f):
        continue
    if f.endswith((".html", ".json")):
        s = open(f, encoding="utf-8").read()
        s = re.sub(r'<svg\b[^>]*class=\\?"fig[^>]*>', shrink_svg, s)
        open(os.path.join(dst, b), "w", encoding="utf-8").write(s)
    else:
        shutil.copy(f, dst)
m = json.load(open(os.path.join(src, "meta.json"), encoding="utf-8"))
m["cover_sub"] = m["cover_sub"] + "<br><small>（圧縮版：内容はそのまま、ページを詰めて軽くした版）</small>"
CSS = """
body { font-size:9.3pt; line-height:1.5; }
h1.part { page-break-before:auto; padding:2.2mm 5mm; font-size:14pt; margin:5mm 0 2mm; border-radius:4px; page-break-after:avoid; }
h1.part small { display:inline; font-size:9pt; margin:0 0 0 4mm; }
body > h1.part:last-of-type { page-break-before:always; margin-top:0; }
h2 { page-break-before:auto; font-size:12.5pt; margin:4.5mm 0 2mm; padding-bottom:1mm; border-bottom-width:2px; }
h1.part + h2 { margin-top:2mm; }
h2 .no { font-size:10.5pt; padding:0 6px; }
h2.solh { margin-top:3.5mm; font-size:11.5pt; }
.goal { padding:1.2mm 3mm; margin:0 0 2mm; font-size:8.8pt; }
.prob { margin:0 0 1.9mm; }
.prob .ph { padding-bottom:0.3mm; margin-bottom:0.6mm; border-bottom-width:1px; }
.pno { font-size:10pt; min-width:11mm; }
.lv, .ptag { font-size:7.8pt; }
.pq { padding-left:1.5mm; }
.sol { margin:0 0 1.4mm; padding:0.9mm 2.4mm; border-left-width:3px; }
.sol .sh { margin-bottom:0.4mm; }
.ss { font-size:8.7pt; line-height:1.48; }
svg.fig { margin:1mm auto; }
table { margin:1.2mm 0; } td, th { padding:0.4mm 2mm; }
p { margin:1mm 0; }
.toc { font-size:8.8pt; line-height:1.4; }
.prob { display:flow-root; } .pq svg.fig { float:right; margin:0.5mm 0 1mm 4mm; }
h3 { font-size:10.8pt; margin:3mm 0 1.2mm; border-left-width:5px; padding-left:2.5mm; }
.box { padding:1.8mm 3mm; margin:1.8mm 0; }
.box::before { margin-bottom:0.4mm; }
.box.lect, .box.point, .box.aim, .box.warn, .box.ans, .box.chk, .box.memo { page-break-inside:auto; }
.box::before { display:inline; white-space:pre; }
.box.point::before { content:"★ この章の要点\\A"; } .box.lect::before { content:"📘 講義\\A"; } .box.ex::before { content:"✏ 例題\\A"; }
.box.chk::before { content:"🔁 確認問題\\A"; } .box.ans::before { content:"✔ 確認問題の答え\\A"; } .box.aim::before { content:"🎯 入試の着眼点\\A"; }
.box.warn::before { content:"⚠ よくあるミス\\A"; } .box.memo::before { content:"📝 まとめ\\A"; }
.box > :first-child { break-before:avoid; }
.ex .solx { margin-top:1mm; padding-top:1mm; }
.pat { margin:2mm 0; } .pat h4 { padding:1.1mm 3mm; font-size:10.2pt; }
.pat .when, .pat .how, .pat .pex, .pat .pnote { padding:1.1mm 3mm; }
"""
m["extra_css"] = m.get("extra_css", "") + CSS
json.dump(m, open(os.path.join(dst, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", dst)
