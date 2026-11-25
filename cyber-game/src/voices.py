import re, sys, os, json, subprocess, glob
import numpy as np
import pyopenjtalk, pyworld as pw
HERE = os.path.dirname(os.path.abspath(__file__))
MEI = os.path.join(HERE, '..', 'dl', 'voices', 'package', 'voice', 'mei')
M001 = os.path.join(HERE, '..', 'apt', 'ext', 'usr', 'share', 'hts-voice', 'nitech-jp-atr503-m001', 'nitech_jp_atr503_m001.htsvoice')
def fnv(s):
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b; h = (h * 0x01000193) & 0xffffffff
    return '%08x' % h
EMO = {'n': 'normal', 'k': 'normal', 'u': 'normal', 's': 'happy', 'a': 'angry', 't': 'sad', 'd': 'sad'}
REP = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'readings.tsv'), encoding='utf-8') if '\t' in l]
REP.sort(key=lambda p: -len(p[0]))
def norm(t):
    t = t.replace('……', '、').replace('…', '、').replace('「', '').replace('」', '').replace('！', '。').replace('　', '、').replace('？', '？')
    t = re.sub(r'(?<![0-9])0時', 'レイジ', t)
    for a, b in REP: t = t.replace(a, b)
    t = re.sub(r'(?<![一-龠ぁ-んァ-ヶ])金(?=[がのをはにでとじも、。])', 'カネ', t)
    t = re.sub(r'^[、。]+', '', t); t = re.sub(r'、+', '、', t); t = t.replace('、。', '。').replace('。、', '。')
    return t
def voices():
    V = {}
    for fp in [os.path.join(HERE, 'cast.txt')] + sorted(glob.glob(os.path.join(HERE, 'cases', '*.txt'))):
        for ln in open(fp, encoding='utf-8'):
            m = re.match(r'^@voice (\w+) (\S+)', ln)
            if m: V[m.group(1)] = m.group(2)
            m = re.match(r'^@char (\w+) .*\bv=(\S+)', ln)
            if m: V[m.group(1)] = m.group(2)
    return {k: (v.split(',')[0], *[float(x) for x in v.split(',')[1:]]) for k, v in V.items()}
def lines(fp):
    out = []; inb = False
    for ln in open(fp, encoding='utf-8'):
        if ln.startswith('## '): inb = True; continue
        if not inb: continue
        m = re.match(r'^([a-z0-9_]+)(?:\.([a-z]))?: (.+)$', ln.rstrip('\n'))
        if m: out.append((m.group(1), m.group(2) or 'n', m.group(3)))
    return out
ENG = {}
def engine(path):
    if path not in ENG: ENG[path] = pyopenjtalk.HTSEngine(path.encode('utf-8'))
    return ENG[path]
def synth(par, who, emo, text):
    base, f0r, fmt, speed, dyn = par
    if base == 'F':
        e = engine(os.path.join(MEI, 'mei_%s.htsvoice' % ('bashful' if (who == 'chihaya' and emo == 't') else EMO[emo])))
        f0e = 1.0
    else:
        e = engine(M001); f0e = {'a': 1.07, 's': 1.06, 'd': 0.95, 't': 1.02, 'u': 1.10}.get(emo, 1.0); dyn *= {'a': 1.35, 's': 1.2, 'd': 0.7, 'u': 1.3}.get(emo, 1.0)
    e.set_speed(speed * {'a': 1.08, 'd': 0.93, 'u': 1.05}.get(emo, 1.0))
    t = norm(text)
    if not pyopenjtalk.g2p(t).replace('pau', '').strip(): return None, 48000
    x = np.asarray(e.synthesize(pyopenjtalk.make_label(pyopenjtalk.run_frontend(t))), dtype=np.float64) / 32768.0; fs = 48000
    f0, tt = pw.harvest(x, fs, f0_floor=60, f0_ceil=600); sp = pw.cheaptrick(x, f0, tt, fs); ap = pw.d4c(x, f0, tt, fs)
    v = f0 > 0
    if v.any():
        lf = np.log(f0[v]); m = lf.mean(); f0 = f0.copy(); f0[v] = np.exp(m + np.log(f0r * f0e) + dyn * (lf - m))
    n = sp.shape[1]; idx = np.clip(np.arange(n) / fmt, 0, n - 1); lo = np.floor(idx).astype(int); hi = np.minimum(lo + 1, n - 1); w = idx - lo
    y = pw.synthesize(f0, np.ascontiguousarray(sp[:, lo] * (1 - w) + sp[:, hi] * w), np.ascontiguousarray(ap[:, lo] * (1 - w) + ap[:, hi] * w), fs)
    return y / (np.abs(y).max() + 1e-9) * 0.89, fs
def mp3(y, fs):
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 's16le', '-ar', str(fs), '-ac', '1', '-i', '-', '-af', 'highpass=f=70,apad=pad_dur=0.12',
        '-ar', '24000', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '32k', '-write_xing', '0', '-id3v2_version', '0', '-f', 'mp3', '-'],
        input=(y * 32767).astype('<i2').tobytes(), stdout=subprocess.PIPE, check=True)
    return p.stdout
if __name__ == '__main__':
    mode = sys.argv[1]; ids = sys.argv[2:] or [os.path.basename(f)[:-4] for f in sorted(glob.glob(os.path.join(HERE, 'cases', '*.txt')))]
    V = voices()
    for cid in ids:
        L = lines(os.path.join(HERE, 'cases', cid + '.txt'))
        bad = sorted({w for w, e, t in L if w not in V}); assert not bad, ('no voice for', bad)
        if mode == 'kana':
            for who, emo, text in L: print(pyopenjtalk.g2p(norm(text), kana=True), ' <- ', who, text)
            continue
        cache = os.path.join(HERE, '..', 'vcache2'); os.makedirs(cache, exist_ok=True)
        index = {}; blob = b''; seen = set()
        for i, (who, emo, text) in enumerate(L):
            k = fnv(who + '|' + text)
            if k in seen: continue
            seen.add(k)
            fp = os.path.join(cache, fnv(who + '|' + emo + '|' + norm(text) + '|' + repr(V[who])) + '.mp3')
            if not os.path.exists(fp):
                y, fs = synth(V[who], who, emo, text)
                open(fp, 'wb').write(mp3(y, fs) if y is not None else b'')
            b = open(fp, 'rb').read()
            if b: index[k] = [len(blob), len(b)]; blob += b
        out = os.path.join(HERE, '..', 'dist2'); os.makedirs(out, exist_ok=True); os.makedirs(os.path.join(HERE, 'vi'), exist_ok=True)
        open(os.path.join(out, 'voice-%s.mp3' % cid), 'wb').write(blob)
        json.dump(index, open(os.path.join(HERE, 'vi', cid + '.json'), 'w'))
        print('voice', cid, 'lines', len(index), 'bytes', len(blob), flush=True)
