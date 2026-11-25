# python3 v3/build.py  -> dist3/game.html (artifact fragment), dist3/index.html (full page)
import os, json
H = os.path.dirname(os.path.abspath(__file__))
V2 = next(d for d in [os.path.join(H, '..', 'v2'), os.path.join(H, '..', '..', 'cyber-game', 'src')] if os.path.exists(os.path.join(d, 'chars.js')))  # shared art, parser and audio
OUT = os.path.join(H, '..', 'dist3') if os.path.basename(H) == 'v3' else os.path.join(H, '..'); os.makedirs(OUT, exist_ok=True)
rd = lambda p: open(p, encoding='utf-8').read()
vi = os.path.join(H, 'vi.json'); idx = rd(vi) if os.path.exists(vi) else '{}'
cr = os.path.join(H, 'credit.txt'); credit = rd(cr).strip() if os.path.exists(cr) else 'VOICEVOX'
js = '\n'.join([rd(os.path.join(V2, 'chars.js')), rd(os.path.join(V2, 'parse.js')), rd(os.path.join(V2, 'audio.js')), rd(os.path.join(H, 'scenes3.js')), rd(os.path.join(H, 'data.js')),
  'const STORY_TXT = ' + json.dumps(rd(os.path.join(H, 'story.txt')), ensure_ascii=False) + ';', 'const VIDX = ' + idx + ';', 'const CREDIT = ' + json.dumps(credit, ensure_ascii=False) + ';', rd(os.path.join(H, 'engine.js'))])
js = js.replace('</script>', '<\\/script>')
page = rd(os.path.join(H, 'page.html')).replace('/*CSS*/', rd(os.path.join(H, 'style.css'))).replace('/*JS*/', js)
if os.path.basename(H) == 'v3': open(os.path.join(OUT, 'game.html'), 'w', encoding='utf-8').write(page)  # fragment for the hosted copy
full = '<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>html,body{margin:0}[hidden]{display:none!important}</style></head><body>' + page + '</body></html>'
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(full)
print('built', len(page))
