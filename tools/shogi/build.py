"""教科書 PDF をビルドする。

1 パス目: 不可視マーカー入りで印刷し、pypdf でマーカーの載った頁を読み取る。
2 パス目: 目次・索引・相互参照に実頁番号を流し込んで再印刷する。
3 パス目: 頁割りが動いていないことを確認する (動いていれば採用し直す)。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time

import bookgen

HERE = os.path.dirname(os.path.abspath(__file__))
SCRATCH = os.environ.get("SHOGI_SCRATCH",
                         "/tmp/claude-0/-home-user-github-io/1689cc2f-543b-5aee-9b94-83d44b602013/scratchpad")
FONTDIR = os.path.join(SCRATCH, "fonts")

ORDER = [
    "00_front.txt",
    "01_part1.txt",
    "02_part2.txt",
    "03_part3.txt",
    "04_part4.txt",
    "05_part5.txt",
    "06_part6.txt",
    "07_appendix.txt",
]

MARK_RE = re.compile(r"%%m(\d+)%%")


def extract_pagemap(pdf_path):
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    pm = {}
    for i, page in enumerate(reader.pages, start=1):
        try:
            txt = page.extract_text() or ""
        except Exception:
            continue
        txt = re.sub(r"\s+", "", txt)
        for mid in MARK_RE.findall(txt):
            pm.setdefault(mid, i)
    return pm, len(reader.pages)


def render(html_path, pdf_path):
    env = dict(os.environ)
    if "NODE_PATH" not in env:
        root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
        if root:
            env["NODE_PATH"] = root
    subprocess.run(["node", os.path.join(HERE, "render.js"), html_path, pdf_path],
                   check=True, cwd=HERE, env=env)


def main():
    def load(name):
        fp = os.path.join(HERE, name)
        if os.path.exists(fp):
            with open(fp, encoding="utf-8") as f:
                return json.load(f)
        return []
    tsume, hisshi = load("tsume.json"), load("hisshi.json")
    out_pdf = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "..", "shogi-genron.pdf")
    out_pdf = os.path.abspath(out_pdf)
    work_html = os.path.join(SCRATCH, "book.html")
    work_pdf = os.path.join(SCRATCH, "book-pass.pdf")
    os.makedirs(SCRATCH, exist_ok=True)

    pagemap = {}
    pages = 0
    for p in range(3):
        t0 = time.time()
        doc, book = bookgen.build_html(ORDER, pagemap=pagemap, tsume=tsume, hisshi=hisshi,
                                       fontdir="file://" + FONTDIR)
        with open(work_html, "w", encoding="utf-8") as f:
            f.write(doc)
        render(work_html, work_pdf)
        newmap, pages = extract_pagemap(work_pdf)
        same = newmap == pagemap
        print("pass %d: %d pages, %d markers, %d figures, %d problems, stable=%s (%.1fs)"
              % (p + 1, pages, len(newmap), book.fig_no, book.problem_no, same, time.time() - t0))
        pagemap = newmap
        if same and p > 0:
            break
    # 最終稿
    doc, book = bookgen.build_html(ORDER, pagemap=pagemap, tsume=tsume, hisshi=hisshi,
                                   fontdir="file://" + FONTDIR)
    with open(work_html, "w", encoding="utf-8") as f:
        f.write(doc)
    render(work_html, out_pdf)
    size = os.path.getsize(out_pdf)
    print("wrote %s (%d pages, %.1f MB)" % (out_pdf, pages, size / 1e6))


if __name__ == "__main__":
    main()
