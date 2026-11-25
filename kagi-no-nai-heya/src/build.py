# python3 build.py -> index.html (and game.html, the fragment for the hosted copy), c/NNN.txt
import os, json, glob, shutil
H = os.path.dirname(os.path.abspath(__file__))
V2 = next(d for d in [os.path.join(H, '..', 'v2'), os.path.join(H, '..', '..', 'cyber-game', 'src')] if os.path.exists(os.path.join(d, 'chars.js')))  # shared character art and block parser
SCRATCH = os.path.basename(H) == 'v3'
OUT = os.path.join(H, '..', 'dist3') if SCRATCH else os.path.join(H, '..')
os.makedirs(os.path.join(OUT, 'c'), exist_ok=True)
rd = lambda p: open(p, encoding='utf-8').read()
vi = os.path.join(H, 'vi.json'); idx = rd(vi) if os.path.exists(vi) else '{}'
credit = rd(os.path.join(H, 'credit.txt')).strip() if os.path.exists(os.path.join(H, 'credit.txt')) else 'VOICEVOX'
# standard cases: copy each text with its voice index appended; a case is listed only when its text exists
avail = ['011']
for f in sorted(glob.glob(os.path.join(H, 'cases', '[0-9][0-9][0-9].txt'))):
    cid = os.path.basename(f)[:3]; txt = rd(f).rstrip('\n') + '\n'
    vj = os.path.join(H, 'cases', 'vi', cid + '.json')
    if os.path.exists(vj): txt += '@vidx ' + rd(vj).strip() + '\n'
    open(os.path.join(OUT, 'c', cid + '.txt'), 'w', encoding='utf-8').write(txt); avail.append(cid)
cl = json.loads(rd(os.path.join(H, 'caselist.json')))
data = rd(os.path.join(H, 'data.js')); data = data[:data.index("if (typeof module !== 'undefined')")]
case011 = 'function case011(){\n' + data + '\nreturn { FACTS, HYPS, EV, LOCS, INTR, REPORT, REL, LANES, MAPPOS, DAYS };\n}'
js = '\n'.join([rd(os.path.join(V2, 'chars.js')), rd(os.path.join(V2, 'parse.js')), rd(os.path.join(H, 'audio3.js')), rd(os.path.join(H, 'scenes3.js')), rd(os.path.join(H, 'scenes4.js')), rd(os.path.join(H, 'std.js')), case011,
  'const STORY_TXT = ' + json.dumps(rd(os.path.join(H, 'story.txt')), ensure_ascii=False) + ';', 'const CAST_TXT = ' + json.dumps(rd(os.path.join(H, 'cast3.txt')), ensure_ascii=False) + ';',
  'const VIDX = ' + idx + ';', 'const CREDIT = ' + json.dumps(credit, ensure_ascii=False) + ';',
  'const CHAPS = ' + json.dumps(cl['chaps'], ensure_ascii=False) + ', CASELIST = ' + json.dumps(cl['list'], ensure_ascii=False) + ', AVAIL = ' + json.dumps(sorted(avail)) + ';', rd(os.path.join(H, 'engine.js'))])
js = js.replace('</script>', '<\\/script>')
page = rd(os.path.join(H, 'page.html')).replace('/*CSS*/', rd(os.path.join(H, 'style.css'))).replace('/*JS*/', js)
if SCRATCH: open(os.path.join(OUT, 'game.html'), 'w', encoding='utf-8').write(page)  # fragment for the hosted copy
full = '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>html,body{margin:0}[hidden]{display:none!important}</style></head><body>' + page + '</body></html>'
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(full)
print('built', len(page), 'cases', len(avail))
