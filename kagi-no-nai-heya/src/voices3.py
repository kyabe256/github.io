# python3 v3/voices3.py : VOICEVOX voices for the v3 case (engine on 127.0.0.1:50021)
import os, sys, json, re, concurrent.futures as cf
H = os.path.dirname(os.path.abspath(__file__))
for d in [os.path.join(H, '..', 'v2'), os.path.join(H, '..', '..', 'cyber-game', 'src')]:
    if os.path.exists(os.path.join(d, 'voices_vv.py')): sys.path.insert(0, d); break
import voices_vv as vv
vv.V.update({
 'cole': ('離途', 101, -0.02, 0.98, 0.9, {'d': 99, 'u': 99}), 'saegusa': ('雀松朱司', 52, -0.03, 1.03, 0.85, {}), 'mashiba': ('栗田まろん', 67, 0.0, 1.0, 1.05, {}),
 'kujo': ('麒ヶ島宗麟', 53, -0.04, 0.92, 0.85, {}), 'laila': ('WhiteCUL', 23, 0.0, 1.0, 0.95, {'d': 25, 't': 25}), 'kanrinin': ('ちび式じい', 42, -0.02, 0.95, 1.0, {}),
})
EXTRA = [('協定世界時', 'キョーテーセカイジ'), ('外事課', 'ガイジカ'), ('合鍵', 'アイカギ'), ('内通者', 'ナイツーシャ'), ('大使館', 'タイシカン'), ('1204号室', 'センニヒャクヨンゴーシツ'), ('1204', 'センニヒャクヨン'), ('N.C.', 'エヌシー'), ('12階', 'ジューニカイ'), ('入出庫', 'ニューシュッコ'), ('品川330 す 41-07', 'シナガワ、サンサンマル、ス、ヨンイチ、ゼロナナ'), ('足立500 は 12-88', 'アダチ、ゴーマルマル、ハ、イチニー、ハチハチ'), ('203.0.113.77', 'ニーマルサン、ゼロ、イチイチサン、ナナナナ'),
  ('駐在官', 'チューザイカン'), ('連絡調整官', 'レンラクチョーセーカン'), ('連絡調整室', 'レンラクチョーセーシツ'), ('警備局', 'ケービキョク'), ('一課', 'イッカ'), ('浴槽', 'ヨクソー'), ('当直', 'トーチョク'), ('庁舎', 'チョーシャ'), ('無届け', 'ムトドケ'), ('席次', 'セキジ'), ('湾岸', 'ワンガン'), ('菓子折り', 'カシオリ'), ('公安', 'コーアン'), ('所管', 'ショカン'), ('秘匿', 'ヒトク'), ('亡命', 'ボーメー'), ('角が立たない', 'カドガタタナイ'), ('216', 'ニヒャクジューロク'), ('214', 'ニヒャクジューヨン'), ('212', 'ニヒャクジューニ'), ('1000万戸', 'イッセンマンコ'), ('3割', 'サンワリ'), ('辺', 'ヘン'), ('録画機', 'ロクガキ'), ('官の机', 'カンノツクエ'), ('外の空気', 'ソトノクーキ'), ('「外」', 'ガイ'), ('一晩中', 'ヒトバンジュー'), ('方角', 'ホーガク'), ('1人', 'ヒトリ'), ('2人', 'フタリ'), ('1つ', 'ヒトツ'), ('2つ', 'フタツ'), ('3つ', 'ミッツ'), ('1台', 'イチダイ'), ('1度', 'イチド'), ('2度', 'ニド'), ('何です', 'ナンデス'), ('長', 'チョー')]
# only add a reading when v2 has no rule for the same key; the bare 長 rule is too broad, so drop it
have = {a for a, b in vv.REP}; vv.REP += [list(x) for x in EXTRA if x[0] not in have and x[0] != '長']; vv.REP.sort(key=lambda p: -len(p[0]))
_norm = vv.norm
def norm(t):
    t = t.replace('FBIの長', 'エフビーアイのチョー').replace('「外」', 'ガイ')
    t = re.sub(r'([1-5])1分', lambda m: {'1': 'ジュー', '2': 'ニジュー', '3': 'サンジュー', '4': 'ヨンジュー', '5': 'ゴジュー'}[m.group(1)] + 'イップン', t)
    return _norm(t)
vv.norm = norm
if __name__ == '__main__':
    L = vv.lines(os.path.join(H, 'story.txt')); bad = sorted({w for w, e, t in L if w not in vv.V}); assert not bad, bad
    if len(sys.argv) > 1 and sys.argv[1] == 'show':
        for w, e, t in L: print(w, e, norm(t))
        sys.exit()
    cache = os.path.join(H, '..', 'vcache_vv'); os.makedirs(cache, exist_ok=True); todo = {}
    for who, emo, text in L:
        k = vv.fnv(who + '|' + text)
        if k not in todo: todo[k] = (who, emo, text, os.path.join(cache, vv.fnv(who + '|' + emo + '|' + norm(text) + '|' + repr(vv.V[who])) + '.mp3'))
    def work(item):
        who, emo, text, fp = item
        if not os.path.exists(fp):
            b = vv.synth(who, emo, text); open(fp + '.tmp', 'wb').write(b); os.replace(fp + '.tmp', fp)
        return fp
    with cf.ThreadPoolExecutor(3) as ex: list(ex.map(work, todo.values()))
    index = {}; blob = b''
    for k, (who, emo, text, fp) in todo.items():
        b = open(fp, 'rb').read()
        if b: index[k] = [len(blob), len(b)]; blob += b
    out = os.path.join(H, '..', 'dist3') if os.path.basename(H) == 'v3' else os.path.join(H, '..'); open(os.path.join(out, 'voice-011.mp3'), 'wb').write(blob); json.dump(index, open(os.path.join(H, 'vi.json'), 'w'))
    used = sorted({vv.V[w][0] for w, e, t in L}); open(os.path.join(H, 'credit.txt'), 'w', encoding='utf-8').write('　'.join('VOICEVOX:' + u for u in used))
    print('lines', len(index), 'bytes', len(blob), 'speakers', '、'.join(used))
