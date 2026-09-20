#!/usr/bin/env python3
"""Google Fonts から本文用の日本語フォント（Noto Serif JP / Noto Sans JP）を取得する。

このコンテナには日本語明朝が同梱されていないため、ビルド時にダウンロードする。
フォント本体はリポジトリに入れず（.gitignore 済み）、ビルドのたびにここで用意する。

ライセンス: SIL Open Font License 1.1（book/assets/fonts/OFL.txt に併置）
"""
from __future__ import annotations

import re
import sys
import urllib.request
from pathlib import Path

from _bookroot import book_root

FONT_DIR = book_root(__file__) / "assets" / "fonts"

# css2 API は User-Agent で返す形式を変える。UA を付けないと truetype(ttf) が返り、
# WeasyPrint が追加依存なしで扱えるのでこれを使う。
CSS_API = "https://fonts.googleapis.com/css2?family={family}:wght@{weights}&display=swap"

FAMILIES = [
    ("Noto Serif JP", "400;700", "NotoSerifJP"),
    ("Noto Sans JP", "400;700", "NotoSansJP"),
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def main() -> int:
    FONT_DIR.mkdir(parents=True, exist_ok=True)
    downloaded = []

    for family, weights, slug in FAMILIES:
        css_url = CSS_API.format(family=family.replace(" ", "+"), weights=weights)
        css = fetch(css_url).decode("utf-8")

        # @font-face ブロックごとに weight と src URL を取り出す
        blocks = css.split("@font-face")
        for block in blocks:
            m_weight = re.search(r"font-weight:\s*(\d+)", block)
            m_src = re.search(r"src:\s*url\(([^)]+)\)", block)
            if not (m_weight and m_src):
                continue
            weight = m_weight.group(1)
            src = m_src.group(1)
            ext = "ttf" if "truetype" in block or src.endswith(".ttf") else "woff2"
            out = FONT_DIR / f"{slug}-{weight}.{ext}"
            if out.exists() and out.stat().st_size > 100_000:
                print(f"skip (exists): {out.name} ({out.stat().st_size:,} bytes)")
                downloaded.append(out)
                continue
            data = fetch(src)
            out.write_bytes(data)
            print(f"downloaded: {out.name} ({len(data):,} bytes)")
            downloaded.append(out)

    if not downloaded:
        print("ERROR: フォントを1つも取得できませんでした", file=sys.stderr)
        return 1

    # OFL の告知を置く（フォント自体は再配布しないが、由来を明示する）
    (FONT_DIR / "README.md").write_text(
        "# フォントについて\n\n"
        "本書の組版には Google の Noto Serif JP / Noto Sans JP を使用しています。\n"
        "これらは SIL Open Font License 1.1 で提供されています。\n"
        "https://openfontlicense.org/\n\n"
        "フォントファイル自体はリポジトリに含めず、`book/build/fetch_fonts.py` が\n"
        "ビルド時に Google Fonts から取得します。\n",
        encoding="utf-8",
    )

    print(f"\n{len(downloaded)} 個のフォントを {FONT_DIR} に用意しました。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
