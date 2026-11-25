# python3 voices4.py [ids...] : VOICEVOX voices for the standard cases (engine on 127.0.0.1:50021)
# each case gets <out>/v/NNN.mp3 and cases/vi/NNN.json; a character keeps the same voice in every case
import os, sys, json, subprocess, glob, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
import voices3 as v3  # adds the v2 path, the extra readings and the fixed voices
vv = v3.vv; norm = v3.norm
SCRATCH = os.path.basename(H) == 'v3'
OUT = os.path.join(H, '..', 'dist3') if SCRATCH else os.path.join(H, '..')
CACHE = os.path.join(H, '..', 'vcache_vv') if SCRATCH else os.path.join(H, '.vcache'); os.makedirs(CACHE, exist_ok=True); os.makedirs(os.path.join(OUT, 'v'), exist_ok=True); os.makedirs(os.path.join(H, 'cases', 'vi'), exist_ok=True)
vv.V.update({  # recurring people who had no voice yet
 'amano': ('春日部つむぎ', 8, -0.02, 1.02, 0.9, {}), 'hinata': ('白上虎太郎', 12, -0.04, 0.9, 0.8, {}), 'oki': ('ちび式じい', 42, 0.02, 0.95, 0.9, {}), 'soma': ('剣崎雌雄', 21, -0.02, 0.97, 0.95, {}), 'kenmochi': ('青山龍星', 84, -0.02, 0.95, 0.8, {}),
 'takamine': ('雀松朱司', 52, -0.05, 0.95, 0.85, {}), 'makabe': ('黒沢冴白', 100, -0.04, 0.95, 0.85, {}), 'okochi': ('麒ヶ島宗麟', 53, 0.03, 1.0, 1.05, {}), 'himuro': ('離途', 101, 0.0, 1.05, 0.75, {}), 'todo': ('麒ヶ島宗麟', 53, 0.0, 0.92, 1.0, {}),
 'mochizuki': ('栗田まろん', 67, -0.05, 0.95, 0.85, {}), 'omiya': ('ちび式じい', 42, -0.03, 0.92, 0.9, {}), 'katsuragi': ('麒ヶ島宗麟', 53, -0.02, 0.88, 0.9, {}), 'brooks': ('玄野武宏', 11, -0.06, 1.0, 0.8, {}), 'drake': ('青山龍星', 13, -0.02, 1.0, 0.9, {}),
 'hart': ('東北イタコ', 109, -0.03, 0.95, 0.95, {}), 'bell': ('栗田まろん', 67, 0.0, 1.05, 0.9, {}), 'chen': ('九州そら', 16, -0.02, 1.05, 0.9, {}), 'lowe': ('青山龍星', 84, -0.05, 0.9, 0.7, {}), 'blake': ('麒ヶ島宗麟', 53, 0.02, 0.95, 1.1, {}),
 'foster': ('波音リツ', 9, 0.0, 1.05, 0.85, {}), 'whitaker': ('ちび式じい', 42, -0.05, 0.88, 1.0, {}), 'pembroke': ('麒ヶ島宗麟', 53, 0.04, 1.0, 1.2, {}), 'fisher': ('冥鳴ひまり', 14, 0.0, 1.08, 1.0, {}), 'kessler': ('離途', 99, -0.03, 0.92, 0.75, {}),
 'marsh': ('雀松朱司', 52, -0.06, 0.9, 0.9, {}), 'stone': ('白上虎太郎', 12, 0.0, 1.1, 1.15, {'s': 32}),
})
POOL = {
 'my': [('白上虎太郎', 12), ('満別花丸', 73), ('玄野武宏', 11), ('離途', 99)],
 'mm': [('剣崎雌雄', 21), ('雀松朱司', 52), ('栗田まろん', 67), ('離途', 99), ('黒沢冴白', 100), ('青山龍星', 13), ('†聖騎士 紅桜†', 51), ('離途', 101), ('玄野武宏', 11), ('青山龍星', 84)],
 'mo': [('麒ヶ島宗麟', 53), ('ちび式じい', 42), ('青山龍星', 84), ('雀松朱司', 52), ('栗田まろん', 67)],
 'fy': [('春日部つむぎ', 8), ('雨晴はう', 10), ('四国めたん', 2), ('WhiteCUL', 23), ('中部つるぎ', 94), ('琴詠ニア', 74), ('東北ずん子', 107), ('冥鳴ひまり', 14)],
 'fm': [('九州そら', 16), ('冥鳴ひまり', 14), ('東北イタコ', 109), ('波音リツ', 9), ('琴詠ニア', 74), ('WhiteCUL', 23)],
 'fo': [('東北イタコ', 109), ('波音リツ', 9), ('九州そら', 16)],
}
def hsh(s):
    h = 2166136261
    for c in s:
        h ^= ord(c); h = (h * 16777619) & 0xffffffff
    return h
def auto_voice(cid, who, name, sex, age, taken):
    pool = POOL[('f' if sex == 'f' else 'm') + ('y' if age < 32 else 'm' if age < 55 else 'o')]; h = hsh(who + name); k = h % len(pool)
    for step in range(len(pool)):
        sp = pool[(k + step) % len(pool)]
        if sp[0] not in taken: break
    else: sp = pool[k]
    taken.add(sp[0]); low = -0.03 if age >= 55 else 0.0
    return (sp[0], sp[1], low + ((h >> 8) % 7 - 3) * 0.012, 0.95 + ((h >> 12) % 6) * 0.025, 0.85 + ((h >> 16) % 6) * 0.05, {})
def dump(cid):
    js = "const fs=require('fs'),path=require('path'),vm=require('vm');const H=process.argv[1],V2=process.argv[2];const c={console};vm.createContext(c);vm.runInContext([path.join(V2,'chars.js'),path.join(V2,'parse.js'),path.join(H,'std.js')].map(f=>fs.readFileSync(f,'utf8').replace(/if \\(typeof module[^\\n]*\\n?/g,'')).join('\\n')+'\\nthis.X={parseStd};',c);const D=c.X.parseStd(fs.readFileSync(path.join(H,'cases',process.argv[3]+'.txt'),'utf8'));const L=[];for(const b in D.story)for(const l of D.story[b])if(!l.cmd&&l.who!=='*')L.push([l.who,l.e,l.t]);console.log(JSON.stringify({L,chars:Object.fromEntries(Object.keys(D.chars).map(k=>[k,[D.chars[k].name,D.chars[k].sex,D.chars[k].age]]))}));"
    return json.loads(subprocess.run(['node', '-e', js, H, vv.HERE, cid], capture_output=True, text=True, check=True).stdout)
if __name__ == '__main__':
    ids = sys.argv[1:] or [os.path.basename(f)[:3] for f in sorted(glob.glob(os.path.join(H, 'cases', '[0-9][0-9][0-9].txt')))]
    used = set(open(os.path.join(H, 'credit.txt'), encoding='utf-8').read().replace('VOICEVOX:', '').split('　')) if os.path.exists(os.path.join(H, 'credit.txt')) else set()
    for cid in ids:
        d = dump(cid); L = d['L']; V = dict(vv.V); taken = {V[w][0] for w, e, t in L if w in V}
        for w, (name, sex, age) in sorted(d['chars'].items()):
            if w not in V: V[w] = auto_voice(cid, w, name, sex, age, taken)
        bad = sorted({w for w, e, t in L if w not in V}); assert not bad, ('no voice for', cid, bad)
        todo = {}
        for who, emo, text in L:
            k = vv.fnv(who + '|' + text)
            if k not in todo: todo[k] = (who, emo, text, os.path.join(CACHE, vv.fnv(who + '|' + emo + '|' + norm(text) + '|' + repr(V[who])) + '.mp3'))
        def work(item):
            who, emo, text, fp = item
            if not os.path.exists(fp):
                vv.V[who] = V[who]; b = vv.synth(who, emo, text); open(fp + '.tmp', 'wb').write(b); os.replace(fp + '.tmp', fp)
            return fp
        with cf.ThreadPoolExecutor(3) as ex: list(ex.map(work, todo.values()))
        index = {}; blob = b''
        for k, (who, emo, text, fp) in todo.items():
            b = open(fp, 'rb').read()
            if b: index[k] = [len(blob), len(b)]; blob += b
        open(os.path.join(OUT, 'v', cid + '.mp3'), 'wb').write(blob); json.dump(index, open(os.path.join(H, 'cases', 'vi', cid + '.json'), 'w'))
        used |= {V[w][0] for w, e, t in L}
        open(os.path.join(H, 'credit.txt'), 'w', encoding='utf-8').write('　'.join('VOICEVOX:' + u for u in sorted(x for x in used if x)))
        print(cid, 'lines', len(index), 'bytes', len(blob), flush=True)
