"""必至問題の自動生成と検証。

一手必至とは、指した後に玉方がどう応じても詰みが避けられない状態をいう。
ここでは「その手を指した後、玉方の全ての合法手に対して n 手以内の詰みが
存在する」ことを完全探索で確認する。さらに、
  * 初手が一意であること
  * 出題図の時点では詰まないこと（詰将棋ではないこと）
も確認する。
"""

from __future__ import annotations

import json
import random
import sys
import time

from shogi import BLACK, WHITE, Position, mate_in, move_str, line_str, principal_variation
import gen_tsume


def is_hisshi(pos: Position, mv, depth=3):
    """mv を指した後、玉方の応手すべてに対し depth 手以内の詰みがあるか。"""
    nx = pos.do(mv)
    moves = nx.legal_moves()
    if not moves:
        return False           # 詰みは必至と呼ばない
    for d in moves:
        if mate_in(nx.do(d), depth) is None:
            return False
    return True


def find(pos, depth=3):
    out = []
    for mv in pos.legal_moves():
        if is_hisshi(pos, mv, depth):
            out.append(mv)
    return out


def main():
    want = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 600.0
    rng = random.Random(4649)
    zones = [((0, 1, 2), (5, 6, 7, 8)), ((0, 1, 2), (0, 1, 2, 3)), ((0, 1, 2), (3, 4, 5))]
    found, seen = [], set()
    t0 = time.time()
    while len(found) < want and time.time() - t0 < budget:
        pos = gen_tsume.random_position(rng, rng.choice([2, 2, 3]), rng.choice([0, 1, 1, 2]),
                                        rng.choice([1, 1, 2]), rng.choice([0, 0, 1]),
                                        rng.choice(zones))
        sfen = pos.to_sfen()
        if sfen in seen:
            continue
        seen.add(sfen)
        if pos.in_check(WHITE) or pos.king_square(BLACK) is not None:
            continue
        if mate_in(pos, 5) is not None:
            continue                      # 詰将棋になってしまう図は除く
        mvs = find(pos, 3)
        if len(mvs) != 1:
            continue
        mv = mvs[0]
        nx = pos.do(mv)
        # 代表的な受けと、それに対する詰み手順を記録する
        lines = []
        defs = nx.legal_moves()
        for d in defs:
            nn = nx.do(d)
            n = mate_in(nn, 3)
            if n is None:
                lines = []
                break
            pv = principal_variation(nn, n)
            lines.append((move_str(nx, d), line_str(pv)))
        if not lines:
            continue
        lines.sort(key=lambda x: -len(x[1]))
        found.append({"sfen": sfen, "move": move_str(pos, mv),
                      "defences": lines[:3], "n_def": len(defs)})
        print("[%5.1fs] %s  %s (受け %d 通り)" % (time.time() - t0, sfen, move_str(pos, mv), len(lines)),
              file=sys.stderr)
    with open("hisshi.json", "w", encoding="utf-8") as f:
        json.dump(found, f, ensure_ascii=False, indent=1)
    print("saved %d" % len(found), file=sys.stderr)


if __name__ == "__main__":
    main()
