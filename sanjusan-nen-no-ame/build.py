# python3 build.py : put the page, styles, scripts, story and voice index into dist/index.html (to open) and dist/game.html (to publish)
import os, re, json
H = os.path.dirname(os.path.abspath(__file__)); S = os.path.join(H, 'src') if os.path.isdir(os.path.join(H, 'src')) else H; DIST = os.path.isdir(os.path.join(H, 'dist')); OUT = os.path.join(H, 'dist') if DIST else H
rd = lambda f: open(os.path.join(S, f), encoding='utf-8').read()
js = ''
for f in ['chars.js', 'cast.js', 'scenes_a.js', 'scenes_b.js', 'scenes_c.js', 'art2.js', 'art3.js', 'drive.js', 'data.js', 'audio.js']:
    js += re.sub(r'\nif \(typeof module[^\n]*', '', rd(f)) + '\n'
js += 'const STORY_TXT = ' + json.dumps(rd('story.txt') + '\n' + rd('story2.txt'), ensure_ascii=False) + ';\n'
vi = os.path.join(S, 'vidx.json'); js += 'const VIDX = ' + (open(vi).read() if os.path.exists(vi) else 'null') + ';\n'
js += rd('engine.js')
page = rd('page.html').replace('/*CSS*/', rd('style.css')).replace('/*JS*/', js.replace('</script', '<\\/script'))
os.makedirs(OUT, exist_ok=True)
if DIST: open(os.path.join(OUT, 'game.html'), 'w', encoding='utf-8').write(page)
open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write('<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>*{box-sizing:border-box}body{margin:0}[hidden]{display:none!important}</style></head><body>' + page + '</body></html>')
print('built', len(page))
