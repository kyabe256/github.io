# python3 voices.py [show] : VOICEVOX voices for every spoken line (engine on 127.0.0.1:50021)
# writes dist/v/<pack>.mp3 and src/vidx.json { key: [pack, offset, length] }; key = fnv(who + '|' + text)
import os, sys, json, re, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'src') if os.path.isdir(os.path.join(H, 'src')) else H
for d in [os.environ.get('VV_HELPER', ''), os.path.join(H, '..', 'game', 'v2'), os.path.join(H, '..', 'cyber-game', 'src'), os.path.join(H, '..', '..', 'cyber-game', 'src'), os.path.join(H, '..', '..', '..', 'cyber-game', 'src')]:
    if d and os.path.exists(os.path.join(d, 'voices_vv.py')): sys.path.insert(0, d); break
import voices_vv as vv
vv.V = {  # who -> (speaker, style id, pitch, speed, intonation, {emotion: style id}); the same person keeps one voice across the eras
 'saku': ('玄野武宏', 11, -0.03, 1.0, 1.0, {'a': 40, 'd': 41, 'c': 41}), 'akari': ('WhiteCUL', 23, 0.0, 1.02, 0.95, {'d': 25, 't': 25}), 'rei': ('九州そら', 16, -0.02, 1.02, 0.9, {}),
 'seiji76': ('麒ヶ島宗麟', 53, -0.06, 0.88, 0.9, {}), 'seiji43': ('麒ヶ島宗麟', 53, 0.0, 0.99, 1.0, {}), 'seiji10': ('白上虎太郎', 12, 0.07, 1.05, 1.1, {}),
 'sayo58': ('東北イタコ', 109, -0.03, 0.94, 0.9, {}), 'sayo25': ('東北イタコ', 109, 0.03, 1.03, 1.05, {}), 'osamu71': ('栗田まろん', 67, -0.05, 0.9, 0.95, {}), 'osamu38': ('栗田まろん', 67, 0.0, 1.0, 1.0, {}),
 'ren': ('離途', 99, 0.02, 1.03, 1.0, {}), 'tadashi60': ('離途', 99, -0.05, 0.9, 0.85, {}), 'iwao': ('剣崎雌雄', 21, -0.03, 1.0, 1.0, {}), 'kiichi': ('雀松朱司', 52, -0.04, 0.97, 1.0, {}),
 'toki': ('九州そら', 16, -0.07, 0.88, 0.85, {}), 'rei8': ('九州そら', 16, 0.12, 1.06, 1.15, {}), 'nozomu': ('雨晴はう', 10, 0.12, 0.96, 1.05, {}),
 'haru': ('波音リツ', 9, -0.03, 0.94, 0.9, {}), 'soichiro': ('青山龍星', 13, -0.02, 1.0, 0.9, {}), 'tae': ('春日部つむぎ', 8, 0.0, 1.02, 1.0, {}), 'kid': ('雨晴はう', 10, 0.1, 1.0, 1.1, {}),
}
vv.EMO['c'] = (0.94, 0.85, -0.01, 0.95); vv.EMO['p'] = vv.EMO['t']; vv.EMO['o'] = vv.EMO['u']; vv.EMO['g'] = vv.EMO['k']
EXTRA = [('知らん名', 'シランナ'), ('鳴る年は', 'ナルトシワ'), ('上手な', 'ジョーズナ'), ('下手', 'ヘタ'), ('1着', 'イッチャク'), ('2組', 'フタクミ'), ('3年生', 'サンネンセー'), ('4年生', 'ヨネンセー'), ('若女将', 'ワカオカミ'), ('女手', 'オンナデ'), ('舶来', 'ハクライ'), ('1ぺん', 'イッペン'), ('昭和2年', 'ショーワニネン'), ('遠うございましょう', 'トオーゴザイマショー'), ('荒うございます', 'アローゴザイマス'), ('離れを', 'ハナレヲ'), ('家内', 'カナイ'), ('好物', 'コーブツ'), ('形見', 'カタミ'), ('細工', 'サイク'), ('亭主', 'テーシュ'), ('当直', 'トーチョク'), ('奉公', 'ホーコー'), ('利発', 'リハツ'), ('気丈', 'キジョー'), ('親方', 'オヤカタ'), ('女房', 'ニョーボー'), ('一生', 'イッショー'), ('身もと', 'ミモト'), ('坊や', 'ボーヤ'), ('坊ちゃん', 'ボッチャン'), ('お得意さま', 'オトクイサマ'), ('所員', 'ショイン'), ('径22ミリ', 'ケーニジューニミリ'), ('2号機', 'ニゴーキ'), ('1まい', 'イチマイ'), ('産院', 'サンイン'), ('名だ', 'ナダ'), ('その名は', 'ソノナワ'), ('この名に', 'コノナニ'), ('の名です', 'ノナデス'), ('の名でございます', 'ノナデゴザイマス'), ('10の時', 'ジューノトキ'), ('気立て', 'キダテ'), ('霧渕', 'キリブチ'), ('雨穴', 'アマアナ'), ('黒檜', 'クロベ'), ('朽木屋', 'クチキヤ'), ('朽木', 'クチキ'), ('匡', 'タダシ'), ('汐見修', 'シオミオサム'), ('汐見', 'シオミ'), ('蓮', 'レン'), ('鷹取組', 'タカトリグミ'), ('鷹取', 'タカトリ'), ('征二', 'セイジ'), ('玲', 'レイ'), ('三雲', 'ミクモ'), ('朔', 'サク'), ('巌', 'イワオ'), ('喜一', 'キイチ'), ('灯り', 'アカリ'), ('灯', 'アカリ'), ('小夜', 'サヨ'), ('多恵', 'タエ'), ('宗一郎', 'ソーイチロー'),
 ('排水坑', 'ハイスイコー'), ('試掘坑', 'シクツコー'), ('発破', 'ハッパ'), ('無縁仏', 'ムエンボトケ'), ('宿帳', 'ヤドチョー'), ('検分', 'ケンブン'), ('廃炉', 'ハイロ'), ('入退構', 'ニュータイコー'), ('閉塞', 'ヘイソク'), ('飯場', 'ハンバ'), ('人夫', 'ニンプ'), ('倅', 'セガレ'), ('産婆', 'サンバ'), ('帳場', 'チョーバ'), ('薪割り', 'マキワリ'), ('鉤', 'カギ'), ('真鍮', 'シンチュー'), ('大腿骨', 'ダイタイコツ'), ('起工式', 'キコーシキ'), ('落盤', 'ラクバン'), ('板垣退助', 'イタガキタイスケ'), ('当主', 'トーシュ'), ('原本', 'ゲンポン'),
 ('KT-2021-0387', 'ケーティー、ニーゼロニーイチ、ゼロサンハチナナ'), ('№', 'ナンバー'), ('一輪', 'イチリン'), ('女将', 'オカミ'), ('今も', 'イマモ'), ('駐在', 'チューザイ'), ('天幕', 'テンマク'), ('支給品', 'シキューヒン'), ('台帳', 'ダイチョー'), ('金具', 'カナグ'), ('切らん', 'キラン'), ('止まらん', 'トマラン'), ('論破', 'ロンパ'), ('20人', 'ニジューニン'), ('1度', 'イチド'), ('2度', 'ニド'), ('3針', 'サンハリ'), ('1通', 'イッツー'), ('1字', 'イチジ'), ('千人', 'センニン'), ('何時', 'ナンジ'), ('森へ', 'モリエ'), ('下りの道', 'クダリノミチ'), ('上り', 'ノボリ'), ('一晩', 'ヒトバン'), ('ひと晩', 'ヒトバン'), ('空だ', 'カラダ'), ('空けた', 'アケタ'), ('空いて', 'アイテ'), ('望', 'ノゾム'), ('所長章', 'ショチョーショー'), ('針箱', 'ハリバコ'), ('双子', 'フタゴ'), ('拾われ子', 'ヒロワレゴ'), ('拾い物', 'ヒロイモノ'), ('老医師', 'ローイシ'), ('一卵性', 'イチランセー'), ('改葬', 'カイソー'), ('生地', 'セーチ'), ('仕う', 'ツカウ'), ('享年', 'キョーネン'), ('石灰', 'セッカイ'), ('無縁', 'ムエン'), ('休診', 'キューシン'), ('処方箋', 'ショホーセン'), ('戸籍', 'コセキ'), ('5つ', 'イツツ'), ('8つ', 'ヤッツ'), ('2つ', 'フタツ'), ('3つ', 'ミッツ'), ('1つ', 'ヒトツ'), ('3針', 'サンハリ'), ('着のみ着のまま', 'キノミキノママ'), ('先代', 'センダイ'), ('旦那さま', 'ダンナサマ'), ('お嬢さま', 'オジョーサマ'), ('達者', 'タッシャ'), ('手配', 'テハイ'), ('最期', 'サイゴ')]
have = {a for a, b in vv.REP}; vv.REP += [list(x) for x in EXTRA if x[0] not in have]; vv.REP = [r for r in vv.REP if r[0] != '長']; vv.REP.sort(key=lambda p: -len(p[0]))
PACK = [('e', r'^q_(akari|osamu71|sayo58|rei|seiji76)_'), ('f', r'^q_(iwao|sayo25|ren|ren2|osamu38|seiji43|toki|rei8)_'), ('g', r'^q_(nozomu|kiichi|haru|tae|soichiro|seiji10)_'), ('d', r'^(final_intro|end_|epilogue|bf_|b8_|b4_|b5_|osamu26_after|sayo26_after)'), ('b', r'^(arrive93|iwao93|p93|sayo93|i93|ren93|osamu93|pl93|seiji93|f93|t93|b2_|b6_|toki93|rei8|m93|g93)'), ('c', r'^(arrive60|kiichi60|p60|haru60|i60|tae60|soichiro60|pl60|boy60|f60|t60|b3_|st60|c60|b7_|nozomu60|g60)'), ('a', r'')]
def lines():
    blocks = {}; blk = None  # a block in story2.txt replaces the block of the same name in story.txt
    for fn in ['story.txt', 'story2.txt', 'story3.txt']:
        blk = None
        for ln in open(os.path.join(S, fn), encoding='utf-8'):
            ln = ln.rstrip('\n')
            if ln.startswith('## '): blk = ln[3:].strip(); blocks[blk] = []; continue
            m = re.match(r'^([a-z0-9_]+)(?:\.([a-z]))?: (.+)$', ln)
            if blk and m: blocks[blk].append((m.group(1), m.group(2) or 'n', m.group(3)))
    out = [(next(p for p, rx in PACK if re.search(rx, b)), w, e, t) for b, L in blocks.items() for w, e, t in L]
    for m in re.finditer(r"say: '([^']+)'", open(os.path.join(S, 'data.js'), encoding='utf-8').read()): out.append(('a', 'saku', 'k', m.group(1)))
    return out
if __name__ == '__main__':
    L = lines(); bad = sorted({w for p, w, e, t in L if w not in vv.V}); assert not bad, bad
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        for p, w, e, t in L: print(p, w, e, vv.norm(t))
        sys.exit()
    OUT = os.path.join(H, 'dist', 'v') if os.path.isdir(os.path.join(H, 'dist')) else os.path.join(H, 'v'); cache = os.path.join(H, 'vcache'); os.makedirs(OUT, exist_ok=True); os.makedirs(cache, exist_ok=True); todo = {}
    for p, who, emo, text in L:
        k = vv.fnv(who + '|' + text)
        if k not in todo: todo[k] = (p, who, emo, text, os.path.join(cache, vv.fnv(who + '|' + emo + '|' + vv.norm(text) + '|' + repr(vv.V[who])) + '.mp3'))
    def work(item):
        p, who, emo, text, fp = item
        if not os.path.exists(fp):
            b = vv.synth(who, emo, text); open(fp + '.tmp', 'wb').write(b); os.replace(fp + '.tmp', fp)
        return fp
    done = 0
    with cf.ThreadPoolExecutor(3) as ex:
        for _ in ex.map(work, todo.values()):
            done += 1
            if done % 50 == 0: print('made', done, '/', len(todo), flush=True)
    blobs = {}; index = {}
    for k, (p, who, emo, text, fp) in todo.items():
        b = open(fp, 'rb').read()
        if b: index[k] = [p, len(blobs.get(p, b'')), len(b)]; blobs[p] = blobs.get(p, b'') + b
    for p, b in blobs.items(): open(os.path.join(OUT, p + '.mp3'), 'wb').write(b)
    json.dump(index, open(os.path.join(S, 'vidx.json'), 'w'))
    used = sorted({vv.V[w][0] for p, w, e, t in L}); open(os.path.join(S, 'credit.txt'), 'w', encoding='utf-8').write('　'.join('VOICEVOX:' + u for u in used))
    print('lines', len(index), 'packs', {p: len(b) for p, b in blobs.items()}, 'speakers', '、'.join(used), flush=True)
