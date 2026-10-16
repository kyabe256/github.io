#!/bin/sh
# 圧縮版をビルド: sh build_c.sh soc 社会
set -e
cd "$(dirname "$0")"
python3 -I compact.py "$1" >/dev/null
python3 -I subjbook.py "$1_c" >/dev/null
sed -i 's|<h2>巻末　|<h2 class="np">巻末　|g; s|<h1 class="part">総合演習|<h1 class="part">総合演習|' "$1_c/book.html"
cd ..
node render_c.js "books/$1_c/$2_圧縮版.pdf" "books/$1_c/book.html"
pdfinfo "books/$1_c/$2_圧縮版.pdf" | grep Pages
ls -la "books/$1_c/$2_圧縮版.pdf"
