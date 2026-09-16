"""実戦形（囲いを崩した局面）で詰みが成立する配置を探す。"""
import sys, time, itertools
from shogi import *

BASES = {
 "mino":    ("後手美濃囲い", "ln1g5/1ks1g4/ppp6/9/9/9/9/9/9"),
 "mino2":   ("後手美濃（金一枚）", "ln1g5/1ks6/ppp6/9/9/9/9/9/9"),
 "yagura":  ("後手矢倉", "7nl/6gk1/5gs1p/9/9/9/9/9/9"),
 "anaguma": ("後手穴熊", "6g1k/6gsl/6ppp/9/9/9/9/9/9"),
 "gin":     ("後手銀冠", "7nl/6gk1/6s1p/9/9/9/9/9/9"),
}
EXTRAS = {
 "": None, "龍八六": ("+R", 5, 1), "龍二六": ("+R", 5, 7), "龍一八": ("+R", 7, 8),
 "馬六四": ("+B", 3, 3), "馬四四": ("+B", 3, 5), "と金三三": ("+P", 2, 6),
 "と金七三": ("+P", 2, 2), "桂八五": ("N", 4, 1), "桂二五": ("N", 4, 7),
 "香一五": ("L", 4, 8), "香九五": ("L", 4, 0),
}
HANDS = ["GS", "G2S", "RG", "BG", "GSN", "2GS", "GSL", "GN", "GL", "SN", "RS", "2G"]

def main():
    want_depths = (3, 5, 7)
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else 900
    t0 = time.time()
    out = []
    for bk, (bname, b) in BASES.items():
        for ek, e in EXTRAS.items():
            for h in HANDS:
                if time.time() - t0 > budget:
                    break
                pos = Position.from_sfen(b + " b " + h + " 1")
                if e:
                    ch, r, c = e
                    if pos.get(r, c) is not None:
                        continue
                    t = CH_SFEN[ch[-1]]
                    if ch.startswith("+"):
                        t = PROMOTE[t]
                    pos.set(r, c, piece(BLACK, t))
                if pos.in_check(WHITE):
                    continue
                n = None
                for d in want_depths:
                    n = mate_in(pos, d)
                    if n:
                        break
                if n and n >= 3:
                    rec = (n, bname, ek, pos.to_sfen(), line_str(principal_variation(pos, n)))
                    out.append(rec)
                    print("%d手詰 %-12s %-8s %s\n    %s" % rec, flush=True)
    print("total", len(out), "%.0fs" % (time.time() - t0))

main()
