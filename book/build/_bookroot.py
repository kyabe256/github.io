"""複数の本を同じパイプラインで組むための、本の根の解決。

各スクリプトは、自分の置かれた場所（`book/build/`）の親を既定の本として扱う。
`--book DIR` を渡すと、そのディレクトリを本の根とする。

    .venv/bin/python book/build/build_pdf.py                  # 既定＝book/
    .venv/bin/python book/build/build_pdf.py --book nihonseiji

解決した `--book` は `sys.argv` から取り除く。各スクリプトの argparse や
`sys.argv[1]` の扱いを変えずに済ませるためである。
"""
from __future__ import annotations

import sys
from pathlib import Path


def book_root(script: str) -> Path:
    """`--book` を見て本の根を返し、その引数を sys.argv から取り除く。"""
    given: str | None = None
    argv = sys.argv
    i = 1
    while i < len(argv):
        if argv[i] == "--book" and i + 1 < len(argv):
            given = argv[i + 1]
            del argv[i:i + 2]
            continue
        if argv[i].startswith("--book="):
            given = argv[i].split("=", 1)[1]
            del argv[i]
            continue
        i += 1

    if given is None:
        return Path(script).resolve().parent.parent

    root = Path(given).resolve()
    if not (root / "manifest.json").exists():
        raise SystemExit(f"--book {given} に manifest.json がありません")
    return root


def slug_of(manifest: dict) -> str:
    """出力するPDFの名前。manifest に無ければディレクトリ名で代用する。"""
    return manifest.get("slug", "book")
