"""将棋の局面表現・合法手生成・詰将棋探索。

盤面座標:
    r = 0..8  (一段目 .. 九段目)
    c = 0..8  (９筋 .. １筋)
    筋 f (1..9) -> c = 9 - f
先手は r が減る方向へ進む。
"""

from __future__ import annotations

# ---------------------------------------------------------------- 駒の定義

FU, KY, KE, GI, KI, KA, HI, OU = range(8)
TO, NY, NK, NG, _X, UM, RY = range(8, 15)

PROMOTE = {FU: TO, KY: NY, KE: NK, GI: NG, KA: UM, HI: RY}
UNPROMOTE = {v: k for k, v in PROMOTE.items()}

BLACK, WHITE = 0, 1

NAME = {
    FU: "歩", KY: "香", KE: "桂", GI: "銀", KI: "金", KA: "角", HI: "飛", OU: "玉",
    TO: "と", NY: "成香", NK: "成桂", NG: "成銀", UM: "馬", RY: "龍",
}
SFEN_CH = {FU: "P", KY: "L", KE: "N", GI: "S", KI: "G", KA: "B", HI: "R", OU: "K"}
CH_SFEN = {v: k for k, v in SFEN_CH.items()}

HAND_ORDER = [HI, KA, KI, GI, KE, KY, FU]

KANSUJI = "一二三四五六七八九"
ZENSUJI = "１２３４５６７８９"

GOLD_LIKE = (KI, TO, NY, NK, NG)

# (dr, dc) は先手視点。後手は符号反転。
STEPS = {
    FU: [(-1, 0)],
    KE: [(-2, -1), (-2, 1)],
    GI: [(-1, -1), (-1, 0), (-1, 1), (1, -1), (1, 1)],
    KI: [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0)],
    OU: [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
    UM: [(-1, 0), (0, -1), (0, 1), (1, 0)],
    RY: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
}
for _p in GOLD_LIKE:
    STEPS[_p] = STEPS[KI]

SLIDES = {
    KY: [(-1, 0)],
    KA: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    HI: [(-1, 0), (0, -1), (0, 1), (1, 0)],
    UM: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    RY: [(-1, 0), (0, -1), (0, 1), (1, 0)],
}


def piece(color: int, ptype: int) -> int:
    return color * 16 + ptype


def pcolor(p: int) -> int:
    return p >> 4


def ptype(p: int) -> int:
    return p & 15


# ---------------------------------------------------------------- 局面

class Position:
    __slots__ = ("board", "hands", "turn")

    def __init__(self, board=None, hands=None, turn=BLACK):
        self.board = board if board is not None else [None] * 81
        self.hands = hands if hands is not None else [dict(), dict()]
        self.turn = turn

    def copy(self) -> "Position":
        return Position(list(self.board), [dict(self.hands[0]), dict(self.hands[1])], self.turn)

    def get(self, r, c):
        return self.board[r * 9 + c]

    def set(self, r, c, p):
        self.board[r * 9 + c] = p

    # ---- SFEN -------------------------------------------------------

    @staticmethod
    def from_sfen(sfen: str) -> "Position":
        parts = sfen.split()
        boardpart = parts[0]
        turn = BLACK if len(parts) < 2 or parts[1] == "b" else WHITE
        handpart = parts[2] if len(parts) > 2 else "-"
        pos = Position(turn=turn)
        r = c = 0
        promoted = False
        for ch in boardpart:
            if ch == "/":
                r += 1
                c = 0
            elif ch.isdigit():
                c += int(ch)
            elif ch == "+":
                promoted = True
            else:
                t = CH_SFEN[ch.upper()]
                if promoted:
                    t = PROMOTE[t]
                    promoted = False
                pos.set(r, c, piece(BLACK if ch.isupper() else WHITE, t))
                c += 1
        if handpart != "-":
            n = 0
            for ch in handpart:
                if ch.isdigit():
                    n = n * 10 + int(ch)
                else:
                    t = CH_SFEN[ch.upper()]
                    col = BLACK if ch.isupper() else WHITE
                    pos.hands[col][t] = pos.hands[col].get(t, 0) + (n or 1)
                    n = 0
        return pos

    def to_sfen(self) -> str:
        rows = []
        for r in range(9):
            row, blank = "", 0
            for c in range(9):
                p = self.get(r, c)
                if p is None:
                    blank += 1
                    continue
                if blank:
                    row += str(blank)
                    blank = 0
                t = ptype(p)
                base = UNPROMOTE.get(t, t)
                ch = SFEN_CH[base]
                if t in UNPROMOTE:
                    ch = "+" + ch
                row += ch if pcolor(p) == BLACK else ch.lower()
            if blank:
                row += str(blank)
            rows.append(row)
        hs = ""
        for col in (BLACK, WHITE):
            for t in HAND_ORDER:
                n = self.hands[col].get(t, 0)
                if n:
                    ch = SFEN_CH[t]
                    hs += (str(n) if n > 1 else "") + (ch if col == BLACK else ch.lower())
        return "%s %s %s 1" % ("/".join(rows), "b" if self.turn == BLACK else "w", hs or "-")

    # ---- 手 ---------------------------------------------------------
    # move = ("m", fr, fc, tr, tc, promote) / ("d", ptype, tr, tc)

    def king_square(self, color):
        want = piece(color, OU)
        for i, p in enumerate(self.board):
            if p == want:
                return divmod(i, 9)
        return None

    def attacks_square(self, color, r, c) -> bool:
        """color 側の駒が (r, c) に利いているか。"""
        sign = 1 if color == BLACK else -1
        for i, p in enumerate(self.board):
            if p is None or pcolor(p) != color:
                continue
            t = ptype(p)
            pr, pc = divmod(i, 9)
            for dr, dc in STEPS.get(t, ()):  # 近接の利き
                if pr + dr * sign == r and pc + dc * sign == c:
                    return True
            for dr, dc in SLIDES.get(t, ()):  # 走りの利き
                sr, sc = dr * sign, dc * sign
                nr, nc = pr + sr, pc + sc
                while 0 <= nr < 9 and 0 <= nc < 9:
                    if nr == r and nc == c:
                        return True
                    if self.get(nr, nc) is not None:
                        break
                    nr += sr
                    nc += sc
        return False

    def in_check(self, color=None) -> bool:
        color = self.turn if color is None else color
        ks = self.king_square(color)
        if ks is None:
            return False
        return self.attacks_square(1 - color, ks[0], ks[1])

    def piece_dests(self, r, c):
        """(r, c) の駒が動ける升 (自駒のある升を除く) を返す。"""
        p = self.get(r, c)
        color = pcolor(p)
        t = ptype(p)
        sign = 1 if color == BLACK else -1
        dests = []
        for dr, dc in STEPS.get(t, ()):
            nr, nc = r + dr * sign, c + dc * sign
            if 0 <= nr < 9 and 0 <= nc < 9:
                q = self.get(nr, nc)
                if q is None or pcolor(q) != color:
                    dests.append((nr, nc))
        for dr, dc in SLIDES.get(t, ()):
            nr, nc = r + dr * sign, c + dc * sign
            while 0 <= nr < 9 and 0 <= nc < 9:
                q = self.get(nr, nc)
                if q is not None and pcolor(q) == color:
                    break
                dests.append((nr, nc))
                if q is not None:
                    break
                nr += dr * sign
                nc += dc * sign
        return dests

    def _expand(self, r, c, nr, nc, out):
        """成・不成を展開して out に積む。"""
        p = self.get(r, c)
        color, t = pcolor(p), ptype(p)
        zone = (0, 1, 2) if color == BLACK else (6, 7, 8)
        must = False
        if t in (FU, KY):
            must = (nr == 0) if color == BLACK else (nr == 8)
        elif t == KE:
            must = (nr <= 1) if color == BLACK else (nr >= 7)
        if not must:
            out.append(("m", r, c, nr, nc, False))
        if t in PROMOTE and (r in zone or nr in zone):
            out.append(("m", r, c, nr, nc, True))

    def drop_squares(self, t):
        color = self.turn
        bad_files = set()
        if t == FU:
            for i, p in enumerate(self.board):
                if p is not None and pcolor(p) == color and ptype(p) == FU:
                    bad_files.add(i % 9)
        out = []
        for i, p in enumerate(self.board):
            if p is not None:
                continue
            r, c = divmod(i, 9)
            if t == FU and c in bad_files:
                continue
            if t in (FU, KY) and ((r == 0) if color == BLACK else (r == 8)):
                continue
            if t == KE and ((r <= 1) if color == BLACK else (r >= 7)):
                continue
            out.append((r, c))
        return out

    def pseudo_moves(self):
        color = self.turn
        out = []
        for i, p in enumerate(self.board):
            if p is None or pcolor(p) != color:
                continue
            r, c = divmod(i, 9)
            for nr, nc in self.piece_dests(r, c):
                self._expand(r, c, nr, nc, out)
        for t, n in self.hands[color].items():
            if n:
                for r, c in self.drop_squares(t):
                    out.append(("d", t, r, c))
        return out

    # ---- 王手・王手回避 ----------------------------------------------

    def checkers(self, color):
        """color の玉に王手をかけている相手駒の位置を列挙。"""
        ks = self.king_square(color)
        if ks is None:
            return []
        out = []
        for i, p in enumerate(self.board):
            if p is None or pcolor(p) == color:
                continue
            r, c = divmod(i, 9)
            if ks in self.piece_dests(r, c):
                out.append((r, c))
        return out

    def evasions(self):
        """王手を受けている側の合法手 (玉の移動・王手駒の駒取り・合駒)。"""
        color = self.turn
        ks = self.king_square(color)
        chk = self.checkers(color)
        cand = []
        kr, kc = ks
        for nr, nc in self.piece_dests(kr, kc):
            cand.append(("m", kr, kc, nr, nc, False))
        if len(chk) == 1:
            cr, cc = chk[0]
            targets = {(cr, cc)}
            cp = self.get(cr, cc)
            if ptype(cp) in SLIDES:
                dr = (kr > cr) - (kr < cr)
                dc = (kc > cc) - (kc < cc)
                nr, nc = cr + dr, cc + dc
                while (nr, nc) != (kr, kc):
                    if self.get(nr, nc) is None:
                        targets.add((nr, nc))
                    nr += dr
                    nc += dc
            for i, p in enumerate(self.board):
                if p is None or pcolor(p) != color or ptype(p) == OU:
                    continue
                r, c = divmod(i, 9)
                for nr, nc in self.piece_dests(r, c):
                    if (nr, nc) in targets:
                        self._expand(r, c, nr, nc, cand)
            for t, n in self.hands[color].items():
                if not n:
                    continue
                for r, c in self.drop_squares(t):
                    if (r, c) in targets and (r, c) != (cr, cc):
                        cand.append(("d", t, r, c))
        res = []
        for mv in cand:
            nx = self.do(mv)
            if not nx.in_check(color):
                res.append(mv)
        return res

    def checking_moves(self):
        """手番側の王手 (合法手のみ)。打ち歩詰めは除外する。"""
        color = self.turn
        ek = self.king_square(1 - color)
        if ek is None:
            return []
        out = []
        for i, p in enumerate(self.board):
            if p is None or pcolor(p) != color:
                continue
            r, c = divmod(i, 9)
            buf = []
            for nr, nc in self.piece_dests(r, c):
                self._expand(r, c, nr, nc, buf)
            for mv in buf:
                nx = self.do(mv)
                if nx.in_check(1 - color) and not nx.in_check(color):
                    out.append(mv)
        for t, n in self.hands[color].items():
            if not n:
                continue
            for r, c in self.drop_squares(t):
                nx = self.do(("d", t, r, c))
                if not nx.in_check(1 - color):
                    continue
                if t == FU and not nx.evasions():
                    continue  # 打ち歩詰め
                out.append(("d", t, r, c))
        return out

    def do(self, mv) -> "Position":
        nx = self.copy()
        color = self.turn
        if mv[0] == "m":
            _, r, c, nr, nc, pro = mv
            p = nx.get(r, c)
            cap = nx.get(nr, nc)
            if cap is not None:
                t = ptype(cap)
                t = UNPROMOTE.get(t, t)
                nx.hands[color][t] = nx.hands[color].get(t, 0) + 1
            nx.set(r, c, None)
            nx.set(nr, nc, piece(color, PROMOTE[ptype(p)]) if pro else p)
        else:
            _, t, r, c = mv
            nx.hands[color][t] -= 1
            if nx.hands[color][t] == 0:
                del nx.hands[color][t]
            nx.set(r, c, piece(color, t))
        nx.turn = 1 - color
        return nx

    def legal_moves(self):
        if self.in_check():
            return self.evasions()
        res = []
        for mv in self.pseudo_moves():
            nx = self.do(mv)
            if nx.in_check(self.turn):
                continue
            if mv[0] == "d" and mv[1] == FU and nx.in_check(nx.turn) and not nx.evasions():
                continue  # 打ち歩詰め
            res.append(mv)
        return res

    def gives_check(self, mv) -> bool:
        return self.do(mv).in_check(1 - self.turn)


# ---------------------------------------------------------------- 詰将棋探索

def _key(pos):
    return (tuple(pos.board), tuple(sorted(pos.hands[0].items())),
            tuple(sorted(pos.hands[1].items())), pos.turn)


def mate_in(pos: Position, depth: int, _memo=None):
    """手番側が depth 手以内で詰ませられるか。詰む最短手数を返す (無ければ None)。"""
    if _memo is None:
        _memo = {}
    k = (_key(pos), depth)
    if k in _memo:
        return _memo[k]
    best = None
    if depth >= 1:
        for mv in pos.checking_moves():
            nx = pos.do(mv)
            d = _defend(nx, depth - 1, _memo)
            if d is not None and (best is None or d + 1 < best):
                best = d + 1
    _memo[k] = best
    return best


def _defend(pos: Position, depth: int, memo):
    """王手を受けている側の手番。depth 手以内に必ず詰むなら最長手数を返す。"""
    k = ("d", _key(pos), depth)
    if k in memo:
        return memo[k]
    moves = pos.evasions()
    if not moves:
        memo[k] = 0
        return 0
    if depth <= 0:
        memo[k] = None
        return None
    worst = 0
    for mv in moves:
        nx = pos.do(mv)
        d = mate_in(nx, depth - 1, memo)
        if d is None:
            memo[k] = None
            return None
        worst = max(worst, d + 1)
    memo[k] = worst
    return worst


def mating_moves(pos: Position, depth: int):
    """詰みに至る初手をすべて列挙する (余詰検出用)。"""
    out = []
    memo = {}
    for mv in pos.checking_moves():
        nx = pos.do(mv)
        d = _defend(nx, depth - 1, memo)
        if d is not None:
            out.append((mv, d + 1))
    return out


def principal_variation(pos: Position, depth: int):
    """最善応酬 (玉方は最長、複数あれば最初の手) を返す。"""
    line = []
    cur = pos
    d = depth
    while d > 0:
        cands = mating_moves(cur, d)
        if not cands:
            break
        mv, n = min(cands, key=lambda x: x[1])
        line.append((cur, mv))
        cur = cur.do(mv)
        d = n - 1
        if d <= 0:
            break
        moves = cur.legal_moves()
        best, bestlen = None, -1
        memo = {}
        for m2 in moves:
            nx = cur.do(m2)
            r = mate_in(nx, d - 1, memo)
            if r is not None and r > bestlen:
                best, bestlen = m2, r
        if best is None:
            break
        line.append((cur, best))
        cur = cur.do(best)
        d -= 1
    return line


def fill_defender_hand(pos: Position, defender: int) -> Position:
    """詰将棋のルールどおり、残りの駒をすべて玉方の持駒にする。"""
    total = {FU: 18, KY: 4, KE: 4, GI: 4, KI: 4, KA: 2, HI: 2, OU: 2}
    used = dict()
    for p in pos.board:
        if p is None:
            continue
        t = ptype(p)
        t = UNPROMOTE.get(t, t)
        used[t] = used.get(t, 0) + 1
    for col in (BLACK, WHITE):
        for t, n in pos.hands[col].items():
            used[t] = used.get(t, 0) + n
    nx = pos.copy()
    for t, n in total.items():
        if t == OU:
            continue
        rest = n - used.get(t, 0)
        if rest > 0:
            nx.hands[defender][t] = nx.hands[defender].get(t, 0) + rest
    return nx


# ---------------------------------------------------------------- 棋譜表記

def square_str(r, c) -> str:
    return "%s%s" % (ZENSUJI[8 - c], KANSUJI[r])


def move_str(pos: Position, mv, prev_dest=None) -> str:
    """KIF 形式に準じた日本語表記。紛らわしい手は移動元を括弧で補う。"""
    mark = "▲" if pos.turn == BLACK else "△"
    color = pos.turn
    if mv[0] == "d":
        _, t, r, c = mv
        # 盤上の同種駒も同じ升へ動けるときだけ「打」を付す
        ambiguous = False
        for i, p in enumerate(pos.board):
            if p is not None and pcolor(p) == color and ptype(p) == t:
                pr, pc = divmod(i, 9)
                if (r, c) in pos.piece_dests(pr, pc):
                    ambiguous = True
                    break
        return "%s%s%s%s" % (mark, square_str(r, c), NAME[t], "打" if ambiguous else "")
    _, r, c, nr, nc, pro = mv
    t = ptype(pos.get(r, c))
    dest = "同" if prev_dest == (nr, nc) else square_str(nr, nc)
    suffix = "成" if pro else ""
    if not pro and t in PROMOTE:
        zone = (0, 1, 2) if color == BLACK else (6, 7, 8)
        if r in zone or nr in zone:
            suffix = "不成"
    origin = ""
    for i, p in enumerate(pos.board):
        if p is not None and pcolor(p) == color and ptype(p) == t and (i // 9, i % 9) != (r, c):
            if (nr, nc) in pos.piece_dests(i // 9, i % 9):
                origin = "(%d%d)" % (9 - c, r + 1)
                break
    return "%s%s%s%s%s" % (mark, dest, NAME[t], suffix, origin)


def line_str(line, sep="") -> str:
    out, prev_dest = [], None
    for p, mv in line:
        out.append(move_str(p, mv, prev_dest))
        prev_dest = (mv[2], mv[3]) if mv[0] == "d" else (mv[3], mv[4])
    return sep.join(out)
