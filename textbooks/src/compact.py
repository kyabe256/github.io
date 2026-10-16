"""圧縮版のビルド用ディレクトリをつくる: python3 compact.py soc → soc_c/"""
import json, os, sys, glob, shutil
src = sys.argv[1]; dst = src + "_c"
os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(src, "*")):
    if os.path.basename(f) in ("meta.json", "book.html") or f.endswith(".pdf") or os.path.isdir(f): continue
    shutil.copy(f, dst)
m = json.load(open(os.path.join(src, "meta.json"), encoding="utf-8"))
m["cover_sub"] = m["cover_sub"] + "<br><small>（圧縮版：内容はそのまま、ページを詰めて軽くした版）</small>"
CSS = """
* { font-synthesis: none; }
b, strong, h1, h2, h3, th, .box::before, .dans .dt, .gh td, .toc b { text-shadow: 0.3px 0 0 currentColor; }
body { font-size:9.8pt; line-height:1.58; }
.en { font-size:10.6pt; }
h2 { page-break-before:auto; margin:7mm 0 3mm; font-size:15pt; padding-bottom:1.2mm; }
h2.np { page-break-before:always; } h2 { page-break-after:avoid; }
h1.part { padding:16mm 10mm; font-size:24pt; margin-bottom:4mm; }
h3 { font-size:11.3pt; margin:3.5mm 0 1.5mm; }
.box { padding:2mm 3.2mm; margin:2mm 0; }
.box::before { margin-bottom:0.5mm; }
p { margin:1.5mm 0; }
td, th { padding:0.6mm 2.2mm; }
table { margin:1.5mm 0; }
.moreh { margin:4mm 0 1.5mm; padding:1mm 3mm; }
.drill { margin-top:4mm; }
ol.dl { font-size:9.2pt; } ol.dl li { margin-bottom:1.2mm; }
.dans { font-size:8.6pt; line-height:1.55; margin-bottom:2mm; }
table.gloss { font-size:8.6pt; } table.gloss td.gt br { display:none; } table.gloss td.gt small { margin-left:1.5mm; color:#666; } table.gloss td.gt { width:34%; } table.gloss td { padding:0.5mm 1.8mm; }
.toc { font-size:9pt; line-height:1.5; }
"""
m["extra_css"] = m.get("extra_css", "") + CSS
json.dump(m, open(os.path.join(dst, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", dst)
