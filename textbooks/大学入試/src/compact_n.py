"""入試シリーズの圧縮版ビルド用ディレクトリをつくる: python3 -I compact_n.py n_phy_m → n_phy_m_c/
中身（問題・解説）はそのまま。章ごとの改ページと部の扉をやめ、文字・余白・図を詰める。"""
import json, os, sys, glob, shutil
src = sys.argv[1].rstrip("/"); dst = src + "_c"
os.makedirs(dst, exist_ok=True)
for f in glob.glob(os.path.join(src, "*")):
    b = os.path.basename(f)
    if b == "meta.json" or b.startswith("book") or f.endswith(".pdf") or os.path.isdir(f):
        continue
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
svg.fig { zoom:0.82; margin:1mm auto; }
table { margin:1.2mm 0; } td, th { padding:0.4mm 2mm; }
p { margin:1mm 0; }
.toc { font-size:8.8pt; line-height:1.4; }
.prob { display:flow-root; } .pq svg.fig { float:right; margin:0.5mm 0 1mm 4mm; }
"""
m["extra_css"] = m.get("extra_css", "") + CSS
json.dump(m, open(os.path.join(dst, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", dst)
