"""詰将棋の自動生成と検証。

ランダムに小さな局面を作り、完全探索で
  * ちょうど N 手詰であること
  * N-2 手以下では詰まないこと
  * 初手が一通りしかないこと (余詰なし)
を確認したものだけを採用する。玉方の持駒は図に明記する方式とし、
無駄合による手数の水増しを避ける。
"""

from __future__ import annotations

import json
import random
import sys
import time

from shogi import (BLACK, WHITE, FU, KY, KE, GI, KI, KA, HI, OU, TO, NY, NK, NG, UM, RY,
                   Position, piece, ptype, pcolor, mate_in, mating_moves,
                   principal_variation, line_str, move_str, UNPROMOTE)

ATTACK_TYPES = [FU, KY, KE, GI, KI, KA, HI, TO, NG, UM, RY]
ATTACK_W = [6, 3, 3, 6, 6, 4, 4, 5, 3, 3, 3]
DEFEND_TYPES = [FU, KY, KE, GI, KI]
DEFEND_W = [8, 2, 2, 4, 4]
HAND_TYPES = [FU, KY, KE, GI, KI, KA, HI]
HAND_W = [5, 2, 3, 5, 6, 3, 3]

MAX_PIECES = {FU: 18, KY: 4, KE: 4, GI: 4, KI: 4, KA: 2, HI: 2}


def legal_square(color, t, r):
    base = UNPROMOTE.get(t, t)
    if base in (FU, KY):
        return r > 0 if color == BLACK else r < 8
    if base == KE:
        return r > 1 if color == BLACK else r < 7
    return True


def count_used(pos):
    used = {}
    for p in pos.board:
        if p is None:
            continue
        t = UNPROMOTE.get(ptype(p), ptype(p))
        used[t] = used.get(t, 0) + 1
    for col in (BLACK, WHITE):
        for t, n in pos.hands[col].items():
            used[t] = used.get(t, 0) + n
    return used


def random_position(rng, n_att, n_def, n_hand, n_dhand, king_zone):
    pos = Position(turn=BLACK)
    kr = rng.choice(king_zone[0])
    kc = rng.choice(king_zone[1])
    pos.set(kr, kc, piece(WHITE, OU))
    box = [(r, c) for r in range(max(0, kr - 2), min(9, kr + 3))
           for c in range(max(0, kc - 2), min(9, kc + 3)) if (r, c) != (kr, kc)]
    rng.shuffle(box)
    used = {}

    def take(t):
        if used.get(t, 0) >= MAX_PIECES[t]:
            return False
        used[t] = used.get(t, 0) + 1
        return True

    for _ in range(n_att):
        if not box:
            break
        r, c = box.pop()
        t = rng.choices(ATTACK_TYPES, ATTACK_W)[0]
        if not legal_square(BLACK, t, r):
            continue
        if not take(UNPROMOTE.get(t, t)):
            continue
        if UNPROMOTE.get(t, t) == FU and any(
                pos.get(rr, c) is not None and pos.get(rr, c) == piece(BLACK, FU) for rr in range(9)):
            continue
        pos.set(r, c, piece(BLACK, t))
    for _ in range(n_def):
        if not box:
            break
        r, c = box.pop()
        t = rng.choices(DEFEND_TYPES, DEFEND_W)[0]
        if not legal_square(WHITE, t, r):
            continue
        if not take(t):
            continue
        if t == FU and any(pos.get(rr, c) == piece(WHITE, FU) for rr in range(9)):
            continue
        pos.set(r, c, piece(WHITE, t))
    for _ in range(n_hand):
        t = rng.choices(HAND_TYPES, HAND_W)[0]
        if take(t):
            pos.hands[BLACK][t] = pos.hands[BLACK].get(t, 0) + 1
    for _ in range(n_dhand):
        t = rng.choices(HAND_TYPES, HAND_W)[0]
        if take(t):
            pos.hands[WHITE][t] = pos.hands[WHITE].get(t, 0) + 1
    return pos


def evaluate(pos, n):
    """ちょうど n 手詰かつ初手一意なら (pv文字列, 手順) を返す。"""
    if pos.in_check(WHITE) or pos.in_check(BLACK):
        return None
    if pos.king_square(BLACK) is not None:
        return None
    if n > 1 and mate_in(pos, n - 2) is not None:
        return None
    cands = mating_moves(pos, n)
    exact = [(m, d) for m, d in cands if d == n]
    if len(exact) != 1 or len(cands) != 1:
        return None
    pv = principal_variation(pos, n)
    if len(pv) != n:
        return None
    return pv


def generate(count_by_len, seed=20260916, time_budget=None):
    rng = random.Random(seed)
    found = {n: [] for n in count_by_len}
    seen = set()
    start = time.time()
    tries = 0
    zones = [((0, 1, 2), (5, 6, 7, 8)), ((0, 1, 2), (0, 1, 2, 3)), ((0, 1, 2), (3, 4, 5))]
    while any(len(found[n]) < count_by_len[n] for n in count_by_len):
        tries += 1
        if time_budget and time.time() - start > time_budget:
            break
        n = rng.choice([k for k in count_by_len if len(found[k]) < count_by_len[k]])
        n_att = rng.choice([1, 2, 2, 3, 3, 4]) if n > 1 else rng.choice([1, 2])
        n_def = rng.choice([0, 0, 1, 1, 2])
        n_hand = rng.choice([1, 1, 2]) if n > 1 else 1
        n_dhand = rng.choice([0, 0, 0, 1])
        pos = random_position(rng, n_att, n_def, n_hand, n_dhand, rng.choice(zones))
        sfen = pos.to_sfen()
        if sfen in seen:
            continue
        seen.add(sfen)
        try:
            pv = evaluate(pos, n)
        except Exception:
            continue
        if pv is None:
            continue
        found[n].append({"sfen": sfen, "moves": n, "pv": line_str(pv)})
        print("[%5.1fs] %d手詰 (%d/%d) %s  %s" % (
            time.time() - start, n, len(found[n]), count_by_len[n], sfen, line_str(pv)),
            file=sys.stderr)
    return found


if __name__ == "__main__":
    want = {1: 8, 3: 14, 5: 12, 7: 6}
    if len(sys.argv) > 1:
        want = {int(k): v for k, v in json.loads(sys.argv[1]).items()}
    budget = float(sys.argv[2]) if len(sys.argv) > 2 else 900.0
    res = generate(want, time_budget=budget)
    out = []
    for n in sorted(res):
        out.extend(res[n])
    with open("tsume.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("saved %d problems" % len(out), file=sys.stderr)
