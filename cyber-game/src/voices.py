import re, sys, os, json, subprocess, struct
import numpy as np
import pyopenjtalk, pyworld as pw
HERE = os.path.dirname(os.path.abspath(__file__))
VD = os.path.join(HERE, '..', 'dl', 'voices', 'package', 'voice', 'mei')
def fnv(s):
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b; h = (h * 0x01000193) & 0xffffffff
    return '%08x' % h
# speaker: (f0 ratio, formant ratio, speed, intonation, gain)
V = {
 'tsubasa': (0.60, 0.880, 1.03, 1.05), 'kohei': (0.46, 0.800, 0.90, 0.85), 'takano': (0.52, 0.835, 1.02, 0.60),
 'yuki': (0.94, 0.985, 1.16, 1.00), 'oconnor': (0.76, 0.930, 0.96, 0.90), 'kane': (0.80, 0.950, 0.88, 1.10),
 'chihaya': (1.10, 1.035, 1.20, 1.25), 'hayase': (0.57, 0.860, 1.18, 0.95), 'onodera': (0.50, 0.815, 0.94, 1.00),
 'onizuka': (0.43, 0.780, 1.00, 1.10), 'kanri': (0.64, 0.900, 0.98, 0.90), 'furukawa': (0.49, 0.825, 0.90, 0.80),
 'shiraishi': (0.47, 0.840, 0.86, 1.00), 'kiryu': (0.88, 0.965, 1.14, 0.85), 'miyashita': (0.53, 0.850, 0.84, 0.90),
 'sawaguchi': (0.61, 0.875, 1.06, 0.85), 'mendes': (0.50, 0.845, 0.96, 1.00), 'rosen': (0.83, 0.945, 1.02, 0.90),
 'hori': (0.56, 0.865, 1.00, 1.05), 'kacho': (0.48, 0.830, 0.95, 0.95), 'news': (1.00, 1.000, 1.06, 0.90),
}
EMO = {'n': 'normal', 'k': 'normal', 'u': 'normal', 's': 'happy', 'a': 'angry', 't': 'sad', 'd': 'sad'}
REP = [('FBI', 'エフビーアイ'), ('CIA', 'シーアイエー'), ('DNA', 'ディーエヌエー'), ('50BTC', '50ビットコイン'),
 ('科捜研', 'カソウケン'), ('一課', 'イッカ'), ('鬼塚', 'オニヅカ'), ('千早', 'チハヤ'), ('堀健吾', 'ホリケンゴ'), ('堀', 'ホリ'),
 ('翼氏', 'ツバサシ'), ('翼', 'ツバサ'), ('総監', 'ソウカン'), ('三浦', 'ミウラ'), ('入退室', 'ニュウタイシツ'), ('回数計', 'カイスウケイ'),
 ('錠前', 'ジョウマエ'), ('電子錠', 'デンシジョウ'), ('錠', 'ジョウ'), ('地下2階', 'チカニカイ'), ('20階', 'ニジッカイ'), ('0時ちょうど', 'レイジチョウド'),
 ('0時', 'レイジ'), ('兄貴', 'アニキ'), ('伯父', 'オジ'), ('上着', 'ウワギ'), ('飲み口', 'ノミクチ'), ('晩めし', 'バンメシ'),
 ('1人', 'ヒトリ'), ('4つ上', 'ヨッツウエ'), ('3つ', 'ミッツ'), ('1つ', 'ヒトツ'), ('2回', 'ニカイ'), ('1本', 'イッポン'), ('1杯', 'イッパイ'),
 ('1度', 'イチド'), ('1錠', 'イチジョウ'), ('20歩', 'ニジッポ'), ('1分', 'イップン'), ('25分', 'ニジュウゴフン'), ('1件', 'イッケン'),
 ('病棟', 'ビョウトウ'), ('挙げ', 'あげ'), ('止血', 'シケツ'), ('20歳', 'ハタチ'), ('24です', 'にじゅうよんです'), ('登庁', 'トウチョウ'),
 ('身代金', 'ミノシロキン'), ('内線', 'ナイセン'), ('外傷', 'ガイショウ'), ('保守', 'ホシュ'), ('出金', 'シュッキン'), ('名義', 'メイギ'),
 ('技官', 'ギカン'), ('警護課', 'ケイゴカ'), ('夜中', 'ヨナカ'), ('手錠', 'テジョウ'), ('甘い物', 'あまいもの'), ('物', 'モノ'), ('殺し', 'コロシ'),
 ('残業代', 'ザンギョウダイ'), ('法廷', 'ホウテイ'), ('急変', 'キュウヘン'), ('点滴', 'テンテキ'), ('私物', 'シブツ'), ('長を', 'ちょうを'),
 ('写し', 'ウツシ'), ('1100人', 'センヒャクニン'), ('0.3', 'レイテンサン'), ('13時間', 'ジュウサンジカン'), ('入口', 'イリグチ'), ('行き先', 'ユキサキ'),
 ('7億円', 'ナナオクエン'), ('課長', 'カチョウ'), ('部長', 'ブチョウ'), ('手で', 'てで'), ('線で', 'せんで'), ('空いて', 'あいて'), ('30年', 'サンジュウネン'),
 ('ドーン', 'ドーン'), ('止め', 'とめ'), ('止ま', 'とま'), ('開か', 'あか'), ('開き', 'あき'), ('開い', 'あい'), ('開け', 'あけ'), ('閉じ', 'とじ'), ('閉ま', 'しま'),
 ('外し', 'はずし'), ('外さ', 'はずさ'), ('外す', 'はずす'), ('伺い', 'うかがい'), ('前もって', 'まえもって'), ('合い', 'あい'), ('筋', 'スジ'), ('目で', 'めで'),
 ('今夜', 'こんや'), ('けさ', 'けさ'), ('表に', 'おもてに'), ('席', 'セキ'), ('癖', 'クセ'), ('隅', 'スミ'), ('最初', 'サイショ'), ('私', 'ワタシ'),
 ('金には', 'カネには'), ('「金」', 'カネ'), ('何回', 'ナンカイ'), ('はいっ', 'ハイ'), ('1つ開く', 'ヒトツあく'),
]
REP.sort(key=lambda p: -len(p[0]))
def norm(t):
    t = t.replace('……', '、').replace('…', '、').replace('「', '').replace('」', '').replace('！', '。').replace('　', '、')
    for a, b in REP: t = t.replace(a, b)
    t = re.sub(r'^[、。]+', '', t); t = re.sub(r'、+', '、', t); t = t.replace('、。', '。').replace('。、', '。')
    return t
def lines():
    out = []
    for ln in open(os.path.join(HERE, 'story.txt'), encoding='utf-8'):
        m = re.match(r'^([a-z]+)(?:\.([a-z]))?: (.+)$', ln.rstrip('\n'))
        if m: out.append((m.group(1), m.group(2) or 'n', m.group(3)))
    return out
ENG = {}
def engine(name):
    if name not in ENG: ENG[name] = pyopenjtalk.HTSEngine(os.path.join(VD, 'mei_%s.htsvoice' % name).encode('utf-8'))
    return ENG[name]
def synth(who, emo, text):
    f0r, fmt, speed, dyn = V[who]
    e = engine('bashful' if (who == 'chihaya' and emo == 't') else EMO[emo]); e.set_speed(speed * (1.08 if emo == 'a' else 0.95 if emo == 'd' else 1.0))
    labels = pyopenjtalk.make_label(pyopenjtalk.run_frontend(norm(text)))
    if not pyopenjtalk.g2p(norm(text)).replace('pau', '').strip(): return None, 48000
    x = np.asarray(e.synthesize(labels), dtype=np.float64); fs = 48000
    x = x / 32768.0
    if emo == 'a': dyn *= 1.2
    f0, t = pw.harvest(x, fs, f0_floor=90, f0_ceil=600); sp = pw.cheaptrick(x, f0, t, fs); ap = pw.d4c(x, f0, t, fs)
    v = f0 > 0
    if v.any():
        lf = np.log(f0[v]); m = lf.mean(); f0 = f0.copy(); f0[v] = np.exp(m + np.log(f0r) + dyn * (lf - m))
    n = sp.shape[1]; idx = np.arange(n) / fmt; idx = np.clip(idx, 0, n - 1)
    lo = np.floor(idx).astype(int); hi = np.minimum(lo + 1, n - 1); w = idx - lo
    sp2 = sp[:, lo] * (1 - w) + sp[:, hi] * w
    ap2 = ap[:, lo] * (1 - w) + ap[:, hi] * w
    y = pw.synthesize(f0, np.ascontiguousarray(sp2), np.ascontiguousarray(ap2), fs)
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    return y, fs
def mp3(y, fs):
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 's16le', '-ar', str(fs), '-ac', '1', '-i', '-', '-af', 'highpass=f=70,apad=pad_dur=0.12',
        '-ar', '24000', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '32k', '-write_xing', '0', '-id3v2_version', '0', '-f', 'mp3', '-'],
        input=(y * 32767).astype('<i2').tobytes(), stdout=subprocess.PIPE, check=True)
    return p.stdout
if __name__ == '__main__':
    L = lines(); mode = sys.argv[1]
    if mode == 'kana':
        for who, emo, text in L: print(who, '|', text, '\n   ', pyopenjtalk.g2p(norm(text), kana=True))
    elif mode == 'test':
        for who, emo, text in L[:int(sys.argv[2])]:
            y, fs = synth(who, emo, text); print(who, None if y is None else len(y) / fs)
    else:
        cache = os.path.join(HERE, '..', 'vcache'); os.makedirs(cache, exist_ok=True)
        index = {}; blob = b''; seen = set()
        for i, (who, emo, text) in enumerate(L):
            k = fnv(who + '|' + text)
            if k in seen: continue
            seen.add(k)
            ck = fnv(who + '|' + emo + '|' + norm(text) + '|' + repr(V[who]))
            fp = os.path.join(cache, ck + '.mp3')
            if not os.path.exists(fp):
                y, fs = synth(who, emo, text)
                if y is None: continue
                open(fp, 'wb').write(mp3(y, fs))
            b = open(fp, 'rb').read(); index[k] = [len(blob), len(b)]; blob += b
            if i % 20 == 0: print(i, len(L), len(blob), flush=True)
        out = os.path.join(HERE, '..', 'dist'); os.makedirs(out, exist_ok=True)
        open(os.path.join(out, 'voice.mp3'), 'wb').write(blob)
        json.dump(index, open(os.path.join(HERE, 'voice-index.json'), 'w'))
        print('done', len(index), len(blob))
