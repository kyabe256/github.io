# VOICEVOX voices: python voices_vv.py build [ids...]   (engine must be running on 127.0.0.1:50021)
import re, sys, os, json, subprocess, glob, urllib.request, urllib.parse, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OP = urllib.request.build_opener(urllib.request.ProxyHandler({}))
URL = 'http://127.0.0.1:50021'
def fnv(s):
    h = 0x811c9dc5
    for b in s.encode('utf-8'):
        h ^= b; h = (h * 0x01000193) & 0xffffffff
    return '%08x' % h
REP = [l.rstrip('\n').split('\t') for l in open(os.path.join(HERE, 'readings.tsv'), encoding='utf-8') if '\t' in l]
REP.sort(key=lambda p: -len(p[0]))
def norm(t):
    t = t.replace('……', '、').replace('…', '、').replace('「', '').replace('」', '').replace('　', '、')
    t = re.sub(r'(?<![0-9])0時', 'レイジ', t)
    for a, b in REP: t = t.replace(a, b)
    t = re.sub(r'(?<![一-龠ぁ-んァ-ヶ])金(?=[がのをはにでとじも、。])', 'カネ', t)
    t = re.sub(r'^[、。]+', '', t); t = re.sub(r'、+', '、', t); t = t.replace('、。', '。').replace('。、', '。')
    return t
# character -> (speaker name, base style id, pitch, speed, intonation, {emotion: style id})
N = 'ノーマル'
V = {
 'tsubasa': ('玄野武宏', 11, 0.0, 1.03, 1.05, {'a': 40, 's': 39, 'd': 41}),
 'kohei': ('麒ヶ島宗麟', 53, 0.0, 0.95, 0.95, {}), 'takano': ('青山龍星', 13, 0.0, 1.05, 0.7, {}),
 'yuki': ('No.7', 29, 0.0, 1.15, 1.0, {}), 'news': ('No.7', 30, 0.0, 1.05, 1.0, {}),
 'oconnor': ('波音リツ', 9, -0.03, 0.97, 0.9, {}), 'kane': ('後鬼', 27, 0.0, 0.92, 1.05, {}),
 'chihaya': ('春日部つむぎ', 8, 0.0, 1.12, 1.15, {}), 'hayase': ('剣崎雌雄', 21, 0.0, 1.15, 1.0, {}),
 'onodera': ('雀松朱司', 52, 0.0, 0.97, 1.05, {}), 'onizuka': ('青山龍星', 13, -0.04, 1.0, 1.1, {'a': 81, 'd': 85, 's': 83}),
 'kanri': ('白上虎太郎', 33, 0.0, 1.0, 1.0, {}), 'furukawa': ('†聖騎士 紅桜†', 51, -0.05, 0.92, 0.85, {}),
 'shiraishi': ('ちび式じい', 42, 0.0, 0.9, 1.0, {}), 'kiryu': ('冥鳴ひまり', 14, 0.0, 1.1, 0.9, {}),
 'miyashita': ('栗田まろん', 67, 0.0, 0.9, 0.95, {}), 'sawaguchi': ('黒沢冴白', 100, 0.0, 1.05, 0.9, {}),
 'mendes': ('離途', 99, 0.0, 0.98, 1.0, {}), 'rosen': ('九州そら', 16, 0.0, 1.02, 0.95, {}),
 'hori': ('玄野武宏', 41, -0.05, 0.98, 1.0, {'u': 11, 'n': 11}), 'kacho': ('麒ヶ島宗麟', 53, 0.03, 1.05, 1.0, {}),
 'margaret': ('東北イタコ', 109, 0.0, 0.98, 1.1, {}), 'reed': ('WhiteCUL', 23, -0.03, 0.97, 0.9, {}),
 'hamilton': ('黒沢冴白', 100, -0.04, 1.08, 0.8, {}), 'shapiro': ('白上虎太郎', 12, -0.06, 1.1, 1.0, {'s': 32}),
 'weiss': ('ちび式じい', 42, -0.04, 0.95, 0.85, {}), 'nair': ('中部つるぎ', 94, 0.0, 1.12, 0.95, {}),
 'park': ('琴詠ニア', 74, 0.0, 1.03, 0.8, {}), 'okafor': ('離途', 101, 0.0, 0.95, 0.9, {}),
 'maki': ('剣崎雌雄', 21, -0.06, 1.02, 1.0, {}), 'nonomura': ('四国めたん', 2, 0.0, 1.1, 1.05, {}),
 'beaumont': ('青山龍星', 84, 0.0, 0.97, 0.8, {}), 'ortega': ('青山龍星', 13, 0.04, 1.15, 0.8, {}),
 'grant': ('玄野武宏', 11, -0.04, 1.03, 0.85, {'d': 41}), 'cruz': ('雨晴はう', 10, 0.0, 1.0, 0.9, {}),
 'bates': ('栗田まろん', 67, 0.02, 1.02, 0.95, {}), 'blair': ('†聖騎士 紅桜†', 51, 0.02, 1.1, 1.15, {}),
 'uno': ('雀松朱司', 52, 0.04, 0.95, 0.8, {}), 'unowife': ('東北ずん子', 107, 0.0, 1.0, 0.95, {}),
 'kuga': ('玄野武宏', 11, -0.08, 0.95, 0.9, {'d': 41}), 'bengoshi': ('波音リツ', 9, 0.0, 1.06, 0.85, {}),
 'shonen': ('白上虎太郎', 12, 0.03, 1.05, 1.1, {'a': 34, 'd': 35, 't': 33, 'u': 33}), 'mikhailov': ('麒ヶ島宗麟', 53, -0.05, 0.9, 0.7, {}),
 'ross': ('No.7', 29, -0.02, 1.08, 0.9, {}), 'hanji': ('後鬼', 27, -0.05, 0.9, 0.8, {}),
 'hirose': ('満別花丸', 73, -0.02, 0.96, 0.8, {}), 'keiji': ('雀松朱司', 52, -0.05, 1.0, 1.1, {}),
 'kale': ('黒沢冴白', 100, 0.03, 0.98, 0.85, {}), 'emily': ('雨晴はう', 10, -0.02, 1.0, 0.9, {}),
 'dragan': ('青山龍星', 84, -0.03, 0.92, 0.75, {}), 'shocho': ('栗田まろん', 67, -0.04, 0.97, 1.1, {}),
}
EMO = {'a': (1.06, 1.25, 0.0, 1.1), 'd': (0.93, 0.8, -0.01, 0.95), 'u': (1.04, 1.2, 0.02, 1.05), 's': (1.0, 1.15, 0.01, 1.0), 't': (0.98, 0.95, 0.0, 0.97), 'k': (0.98, 1.0, -0.005, 1.0), 'n': (1.0, 1.0, 0.0, 1.0)}
def lines(fp):
    out = []; inb = False
    for ln in open(fp, encoding='utf-8'):
        if ln.startswith('## '): inb = True; continue
        if not inb: continue
        m = re.match(r'^([a-z0-9_]+)(?:\.([a-z]))?: (.+)$', ln.rstrip('\n'))
        if m: out.append((m.group(1), m.group(2) or 'n', m.group(3)))
    return out
def synth(who, emo, text):
    name, base, pitch, speed, inton, styles = V[who]; sid = styles.get(emo, base); e = EMO[emo]
    t = norm(text)
    if not re.search(r'[ぁ-んァ-ヶ一-龠0-9A-Za-z]', t): return b''
    q = json.load(OP.open(urllib.request.Request(URL + '/audio_query?' + urllib.parse.urlencode({'text': t, 'speaker': sid}), method='POST')))
    q['speedScale'] = speed * e[0]; q['intonationScale'] = inton * e[1]; q['pitchScale'] = pitch + e[2]; q['volumeScale'] = e[3]; q['prePhonemeLength'] = 0.06; q['postPhonemeLength'] = 0.12
    w = OP.open(urllib.request.Request(URL + '/synthesis?speaker=%d' % sid, data=json.dumps(q).encode(), headers={'Content-Type': 'application/json'}, method='POST')).read()
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', '-', '-af', 'loudnorm=I=-17:TP=-1.5:LRA=11', '-ar', '24000', '-ac', '1', '-c:a', 'libmp3lame', '-b:a', '40k', '-write_xing', '0', '-id3v2_version', '0', '-f', 'mp3', '-'], input=w, stdout=subprocess.PIPE, check=True)
    return p.stdout
if __name__ == '__main__':
    mode = sys.argv[1]; ids = sys.argv[2:] or [os.path.basename(f)[:-4] for f in sorted(glob.glob(os.path.join(HERE, 'cases', '*.txt')))]
    cache = os.path.join(HERE, '..', 'vcache_vv'); os.makedirs(cache, exist_ok=True)
    for cid in ids:
        L = lines(os.path.join(HERE, 'cases', cid + '.txt'))
        bad = sorted({w for w, e, t in L if w not in V}); assert not bad, ('no voice for', bad)
        todo = {}
        for who, emo, text in L:
            k = fnv(who + '|' + text)
            if k not in todo: todo[k] = (who, emo, text, os.path.join(cache, fnv(who + '|' + emo + '|' + norm(text) + '|' + repr(V[who])) + '.mp3'))
        def work(item):
            who, emo, text, fp = item
            if not os.path.exists(fp):
                b = synth(who, emo, text); open(fp + '.tmp', 'wb').write(b); os.replace(fp + '.tmp', fp)
            return fp
        with cf.ThreadPoolExecutor(3) as ex: list(ex.map(work, todo.values()))
        index = {}; blob = b''
        for k, (who, emo, text, fp) in todo.items():
            b = open(fp, 'rb').read()
            if b: index[k] = [len(blob), len(b)]; blob += b
        out = os.path.join(HERE, '..', 'dist2'); os.makedirs(os.path.join(HERE, 'vi'), exist_ok=True)
        open(os.path.join(out, 'voice-%s.mp3' % cid), 'wb').write(blob)
        json.dump(index, open(os.path.join(HERE, 'vi', cid + '.json'), 'w'))
        print('voice', cid, 'lines', len(index), 'bytes', len(blob), flush=True)
    used = sorted({V[w][0] for cid in ids for w, e, t in lines(os.path.join(HERE, 'cases', cid + '.txt'))})
    print('speakers used:', '、'.join(used), flush=True)
