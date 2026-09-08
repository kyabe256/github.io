# ビルド手順

組版環境: LuaLaTeX + luatexja（Ubuntu 24.04 / TeX Live 2023）

## 必要パッケージ

    sudo apt-get install -y --no-install-recommends \
      texlive-luatex texlive-lang-japanese texlive-latex-recommended \
      fonts-ipafont-mincho fonts-ipafont-gothic

## コンパイル

    cd src && make

目次とページ参照を確定させるため lualatex を2回実行する。

## 動作確認済みのプリアンブル

`src/report.tex` 冒頭のとおり。本文書体は IPA明朝、見出し等の和文ゴシックは
IPAゴシックを使用する。`\ltjsetmainjfont` は当環境では未定義のため、
`\setmainjfont` / `\setsansjfont`（luatexja-fontspec）を用いること。
