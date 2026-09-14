#!/usr/bin/env python3
"""生成された『世界史大全』のPDFを検証する。

  python book/build/verify_pdf.py [PDFのパス]

ビルドのたびに走らせ、次を自動で確認する。
  1. ページ数が目標範囲に入っているか
  2. PDFのしおりが部→章→節の3階層になっているか
  3. 豆腐（フォント未収録の欠字）が混入していないか
  4. 想定外の文字体系（ハングル・キリル文字など）が紛れ込んでいないか
  5. 目次のページ番号が、実際にその章が現れるページと一致するか
  6. 章のHTML断片に書かれた内部リンクの参照先が存在するか
  7. 日本語が正しく埋め込まれ、テキストとして抽出できるか
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader

BOOK = Path(__file__).resolve().parent.parent
MANIFEST = json.loads((BOOK / "manifest.json").read_text(encoding="utf-8"))
CONTENT = BOOK / "content"

OK, NG, WARN = "\033[32m✓\033[0m", "\033[31m✗\033[0m", "\033[33m!\033[0m"

# 本書で使ってよい文字体系。これ以外が現れたら誤入力を疑う。
ALLOWED = re.compile(
    r"[　-〿"      # 和文の約物
    r"぀-ヿ"       # ひらがな・カタカナ
    r"㐀-䶿"       # 漢字拡張A
    r"一-鿿"       # 漢字
    r"豈-﫿"       # 互換漢字
    r"＀-￯"       # 全角英数・半角カナ
    r" -~"       # ASCII
    r" -ɏ"       # ラテン拡張（欧語の綴り）
    r"Ͱ-Ͽ"       # ギリシア文字
    r"‐-⁞"       # ダッシュ・引用符など
    r"←-⇿∀-⋿■-⛿✀-➿"  # 記号・★など
    r"①-⓿"       # 丸数字（図版の番号づけ）
    r"\s]"
)


class Report:
    def __init__(self) -> None:
        self.failed = 0

    def check(self, ok: bool, label: str, detail: str = "") -> None:
        mark = OK if ok else NG
        if not ok:
            self.failed += 1
        print(f"  {mark} {label}" + (f"  — {detail}" if detail else ""))

    def note(self, label: str, detail: str = "") -> None:
        print(f"  {WARN} {label}" + (f"  — {detail}" if detail else ""))


def walk_outline(items, depth=0, acc=None):
    acc = acc if acc is not None else []
    for it in items:
        if isinstance(it, list):
            walk_outline(it, depth + 1, acc)
        else:
            acc.append((depth, str(it.title)))
    return acc


def main() -> int:
    pdf_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BOOK / "out" / "sekaishi-taizen.pdf"
    if not pdf_path.exists():
        print(f"{NG} PDFが見つかりません: {pdf_path}")
        return 1

    r = Report()
    reader = PdfReader(str(pdf_path))
    n_pages = len(reader.pages)
    pages_text = [p.extract_text() or "" for p in reader.pages]
    full_text = "\n".join(pages_text)

    print(f"\n『{MANIFEST['title']}』 検証: {pdf_path.name}"
          f"  ({pdf_path.stat().st_size/1024/1024:.1f} MB)\n")

    # 執筆の進捗（未完成のうちはページ数を判定基準にしない）
    written = [(p, ch) for p in MANIFEST["parts"] for ch in p["chapters"]
               if (CONTENT / p["dir"] / ch["file"]).exists()]
    all_ch = sum(len(p["chapters"]) for p in MANIFEST["parts"])
    n_ap = sum(1 for a in MANIFEST["appendix"] if (CONTENT / "zz-appendix" / a["file"]).exists())
    complete = len(written) == all_ch and n_ap == len(MANIFEST["appendix"])

    # 1. ページ数
    lo, hi = MANIFEST["page_target"]
    print("1. ページ数")
    if complete:
        r.check(lo <= n_pages <= hi, f"{n_pages} ページ", f"目標 {lo}〜{hi}")
    else:
        # 完成時のページ数を見積もる。
        # 未執筆章はスタブとして1ページを占めているので、その分を差し引いてから
        # 執筆済み章の平均ページ数で置き換える。
        n_stub = all_ch - len(written)
        overhead = 40   # 表紙・凡例・目次・部扉・白ページの合計（実測値）
        per_ch = max((n_pages - n_stub - overhead) / max(len(written), 1), 1)
        ap_est = 60     # 巻末資料7点の見込み
        est = int(len(written) * per_ch + n_stub * per_ch + overhead + ap_est)
        r.note(f"{n_pages} ページ（執筆途中のため判定を保留）",
               f"実測 {per_ch:.1f} ページ/章 → 完成時 約{est}ページ／目標 {lo}〜{hi}")

    # 2. しおりの階層
    print("\n2. PDFしおり")
    outline = walk_outline(reader.outline)
    depths = {d for d, _ in outline}
    n_parts = sum(1 for d, _ in outline if d == 0)
    n_chaps = sum(1 for d, _ in outline if d == 1)
    r.check(len(outline) > 0, f"しおり {len(outline)} 項目")
    r.check(max(depths, default=-1) >= 2, f"階層の深さ {max(depths, default=-1)+1}", "部→章→節の3階層を期待")
    r.check(n_chaps > 0, f"部レベル {n_parts} 項目 / 章レベル {n_chaps} 項目")

    # 3. 豆腐・欠字
    print("\n3. 欠字（豆腐）")
    tofu = re.findall(r"[�□■]", full_text)
    r.check(not tofu, f"欠字 {len(tofu)} 個", "本文に □ や U+FFFD が無いこと")

    # 4. 想定外の文字体系
    print("\n4. 文字体系")
    stray = sorted({c for c in full_text if not ALLOWED.match(c)})
    r.check(not stray, f"想定外の文字 {len(stray)} 種",
            "".join(f"{c}(U+{ord(c):04X}) " for c in stray[:12]) or "なし")

    # 5. 目次のページ番号照合
    print("\n5. 目次のページ番号")
    toc_entries = re.findall(r"第(\d+)章\s*(.+?)\s*[.… ]{3,}\s*(\d+)", full_text[:40000])
    mismatches = []
    titles = {ch["n"]: ch["title"] for p in MANIFEST["parts"] for ch in p["chapters"]}
    for num_s, _title, page_s in toc_entries:
        n, claimed = int(num_s), int(page_s)
        if n not in titles or not (1 <= claimed <= n_pages):
            continue
        # 目次が示すページに、その章の見出しが実在するか
        # 字間調整で入る半角・全角スペースと改行を落としてから照合する
        squeeze = lambda s: re.sub(r"\s|　", "", s)
        target = squeeze(pages_text[claimed - 1])
        head = squeeze(f"第{n}章" + titles[n])
        if head[:14] not in target:
            mismatches.append((n, claimed))
    r.check(bool(toc_entries), f"目次項目 {len(toc_entries)} 件を検出")
    r.check(not mismatches, f"不一致 {len(mismatches)} 件",
            ", ".join(f"第{n}章→{p}p" for n, p in mismatches[:6]) or "全て一致")

    # 6. 内部リンクの参照先
    print("\n6. 内部リンク")
    ids: set[str] = set()
    hrefs: list[tuple[str, str]] = []
    for part in MANIFEST["parts"]:
        ids.add(part["id"])
        for ch in part["chapters"]:
            ids.add(f'ch{ch["n"]:02d}')
            f = CONTENT / part["dir"] / ch["file"]
            if not f.exists():
                continue
            html = f.read_text(encoding="utf-8")
            ids.update(re.findall(r'id="([^"]+)"', html))
            hrefs += [(f.name, h) for h in re.findall(r'href="#([^"]+)"', html)]
            # <figure> の id はビルド時に付与される（build_pdf.number_captions）。
            # 図版索引（付録D）が参照するため、ここで同じ規則を再現しておく。
            n_fig = len(re.findall(r"<figure(?![^>]*\sid=)", html))
            ids.update(f'fig{ch["n"]}-{i}' for i in range(1, n_fig + 1))
    for ap in MANIFEST["appendix"]:
        ids.add(ap["id"])
        f = CONTENT / "zz-appendix" / ap["file"]
        if f.exists():
            html = f.read_text(encoding="utf-8")
            ids.update(re.findall(r'id="([^"]+)"', html))
            hrefs += [(f.name, h) for h in re.findall(r'href="#([^"]+)"', html)]
    broken = [(fn, h) for fn, h in hrefs if h not in ids]
    r.check(not broken, f"断片内リンク {len(hrefs)} 件 / 切れ {len(broken)} 件",
            ", ".join(f"{fn}#{h}" for fn, h in broken[:5]) or "切れなし")

    # 7. 日本語の埋め込み確認
    print("\n7. 日本語の埋め込み")
    flat = full_text.replace(" ", "").replace("\n", "")
    missing = [ch["n"] for _p, ch in written if ch["title"].replace(" ", "")[:8] not in flat]
    r.check(not missing, f"執筆済み {len(written)} 章の見出しを抽出テキストで確認",
            f"見つからない章: {missing[:6]}" if missing else "全て抽出可能")

    # 8. 和文に紛れた欧文語
    # 「イベリア半島から north 上してきた」のような書き間違いを捕まえる。
    # 原語の併記は括弧や .orig / .dates の内側に書く方針なので、
    # 和文と欧文が素の空白で直接隣り合う形は誤りとみなす。
    print("\n8. 和文への欧文混入")
    JA = r"[ぁ-んァ-ヶ一-鿿]"
    stray_latin: list[tuple[str, str]] = []
    for part in MANIFEST["parts"]:
        for ch in part["chapters"]:
            f = CONTENT / part["dir"] / ch["file"]
            if not f.exists():
                continue
            src = f.read_text(encoding="utf-8")
            # 原語の併記は .orig / .dates の内側に書く方針なので、その中身は除外する
            src = re.sub(r'<span class="(?:orig|dates)">.*?</span>', "", src, flags=re.S)
            plain = re.sub(r"<[^>]+>", "", src, flags=re.S)
            for m in re.finditer(rf"{JA} [A-Za-z]+ {JA}", plain):
                stray_latin.append((f.name, m.group(0)))
    r.check(not stray_latin, f"混入 {len(stray_latin)} 件",
            ", ".join(f"{fn}「{s}」" for fn, s in stray_latin[:5]) or "なし")

    # 参考情報
    body_chars = sum(len(t) for t in pages_text)
    print(f"\n  参考: 抽出テキスト {body_chars:,} 字 / {n_pages} ページ"
          f" = {body_chars//max(n_pages,1):,} 字/ページ")
    print(f"  進捗: 本文 {len(written)}/{all_ch} 章"
          f" ({len(written)*100//all_ch}%)、巻末 {n_ap}/{len(MANIFEST['appendix'])} 点")

    print(f"\n{'—'*54}")
    if r.failed:
        print(f"{NG} {r.failed} 件の検証に失敗しました\n")
        return 1
    print(f"{OK} すべての検証を通過しました\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
