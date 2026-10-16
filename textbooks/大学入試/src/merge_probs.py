"""問題集フォルダの p*.py を検算しながら problems.json にまとめる: python3 merge_probs.py <フォルダ>"""
import json, sys, glob, os, runpy
d = sys.argv[1]
pat = sys.argv[2] if len(sys.argv) > 2 else "p[0-9]*.py"   # 例: "p0[2-9].py"
outs = sys.argv[3] if len(sys.argv) > 3 else "problems.json"
out = {}
if pat[:1].isdigit():   # 章の範囲 例: "2-13"
    a, b = map(int, pat.split("-"))
    files = [os.path.join(d, f"p{n:02d}.py") for n in range(a, b + 1)]
else:
    files = sorted(glob.glob(os.path.join(d, pat)))
for f in files:
    g = runpy.run_path(f)
    if "verify" in g:
        g["verify"]()
    for k, v in g["CH"].items():
        assert str(k) not in out, f"章が重複: {k}"
        out[str(k)] = v
json.dump(out, open(os.path.join(d, outs), "w", encoding="utf-8"), ensure_ascii=False)
print("ok", {k: len(v["items"]) for k, v in sorted(out.items(), key=lambda t: int(t[0]))}, sum(len(v["items"]) for v in out.values()))
