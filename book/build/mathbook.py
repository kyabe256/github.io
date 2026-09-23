"""数学書のための前処理——数式のSVG化と、定理番号の二パス解決。

WeasyPrint は MathML を組めない。そこで数式は MathJax であらかじめ SVG に変換し、
インラインSVGとして本文に埋め込む。図版がすでに同じ経路で確実に組めているため、
組版の信頼性を保ったまま数式を入れられる。

本文の書き方:
    行中      <m>x \\in X</m>
    別行立て  <M>\\int_X f \\, d\\mu</M>

定理環境の書き方:
    <div class="teiri" data-kind="定理" id="thm-compact-prod"><h4>…</h4>…</div>
    参照      <ref t="thm-compact-prod"/>  →  「定理 20.3」＋リンク

番号は手で書かない。第一パスで id → 番号の対応表を作り、第二パスで参照を解決する。
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[2] / "tools" / "mathrender"

# 番号づけの対象。同じ章のなかで一つの番号列を共有する（定理2.1の次が定義2.2）。
# Engelking 流に、定義も定理も反例も同じ列に並べると相互参照が追いやすい。
NUMBERED = {"teigi": "定義", "teiri": "定理", "rei": "例", "hanrei": "反例"}

MATH_RE = re.compile(r"<(m|M)>(.*?)</\1>", re.S)
# 箱の開きタグと、直後の <h4>…</h4> までを一度に捕まえる。
# ラベルは h4 の中へ直接書き込む。CSS の attr() は祖先の属性を読めないためであり、
# 同時に、番号が抽出テキストに乗って検証と索引から参照できるようになる。
BOX_RE = re.compile(
    r'<div class="(teigi|teiri|rei|hanrei)"([^>]*)>\s*<h4>(.*?)</h4>', re.S)
REF_RE = re.compile(r'<ref\s+t="([^"]+)"\s*/?>')
ID_RE = re.compile(r'id="([^"]+)"')
KIND_RE = re.compile(r'data-kind="([^"]+)"')


# ---------------------------------------------------------------- 数式

def _cache_dir(book: Path) -> Path:
    d = book / "build" / "mathcache"
    d.mkdir(parents=True, exist_ok=True)
    return d


def render_math(html: str, book: Path) -> tuple[str, dict]:
    """<m>/<M> を SVG に置き換える。TeX の SHA256 をキーにキャッシュする。"""
    found: list[tuple[str, str, bool]] = []   # (key, tex, display)
    seen: set[str] = set()

    for mo in MATH_RE.finditer(html):
        display = mo.group(1) == "M"
        tex = mo.group(2).strip()
        key = hashlib.sha256(f"{int(display)}\0{tex}".encode()).hexdigest()[:32]
        if key not in seen:
            seen.add(key)
            found.append((key, tex, display))

    cache = _cache_dir(book)
    todo = [{"id": k, "tex": t, "display": d}
            for k, t, d in found if not (cache / f"{k}.svg").exists()]

    stats = {"total": len(found), "rendered": len(todo), "errors": []}

    if todo:
        proc = subprocess.run(
            ["node", str(TOOLS / "render.js")],
            input=json.dumps(todo), capture_output=True, text=True, check=True,
        )
        for item in json.loads(proc.stdout):
            if "error" in item:
                stats["errors"].append((item["id"], item["error"]))
                continue
            (cache / f"{item['id']}.svg").write_text(item["svg"], encoding="utf-8")

    def sub(mo: re.Match) -> str:
        display = mo.group(1) == "M"
        tex = mo.group(2).strip()
        key = hashlib.sha256(f"{int(display)}\0{tex}".encode()).hexdigest()[:32]
        f = cache / f"{key}.svg"
        if not f.exists():
            return f'<span class="math-error">［式のレンダリングに失敗］</span>'
        svg = f.read_text(encoding="utf-8")
        cls = "mathdisp" if display else "mathinl"
        return f'<span class="{cls}">{svg}</span>'

    return MATH_RE.sub(sub, html), stats


# ---------------------------------------------------------------- 定理番号

def number_boxes(html: str, ch_num: int, registry: dict) -> str:
    """定義・定理・例・反例に章内の通し番号を振り、id → 表示名を registry に記録する。"""
    counter = {"n": 0}

    def sub(mo: re.Match) -> str:
        cls, attrs, title = mo.group(1), mo.group(2), mo.group(3).strip()
        counter["n"] += 1
        num = f"{ch_num}.{counter['n']}"

        kind_mo = KIND_RE.search(attrs)
        kind = kind_mo.group(1) if kind_mo else NUMBERED[cls]
        label = f"{kind}{num}"

        id_mo = ID_RE.search(attrs)
        if id_mo:
            registry[id_mo.group(1)] = {"label": label, "num": num, "kind": kind}

        # 見出しは「定義1.1」だけ、あるいは「定理20.3（Tychonoff）」のようになる。
        head = f'<span class="box-label">{label}</span>'
        if title:
            head += f'<span class="box-title">{title}</span>'

        return f'<div class="{cls}"{attrs} data-num="{num}">\n<h4>{head}</h4>'

    return BOX_RE.sub(sub, html)


def resolve_refs(html: str, registry: dict) -> tuple[str, list]:
    """<ref t="..."/> を「定理20.3」＋リンクに置き換える。未解決は残して報告する。"""
    missing: list[str] = []

    def sub(mo: re.Match) -> str:
        target = mo.group(1)
        info = registry.get(target)
        if info is None:
            missing.append(target)
            return f'<span class="ref-error">［{target}］</span>'
        return f'<a class="xref-thm" href="#{target}">{info["label"]}</a>'

    return REF_RE.sub(sub, html), missing


def leftovers(html: str) -> dict:
    """置き換え残しの検出。ビルドの最後に呼んで、0 でなければ警告する。"""
    return {
        "math": len(MATH_RE.findall(html)),
        "ref": len(REF_RE.findall(html)),
        "math_error": html.count('class="math-error"'),
        "ref_error": html.count('class="ref-error"'),
    }
