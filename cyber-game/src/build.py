import json, os, glob
H = os.path.dirname(os.path.abspath(__file__)); R = lambda p: open(os.path.join(H, p), encoding='utf-8').read()
cases = {os.path.basename(f)[:-4]: open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(H, 'cases', '*.txt')))}
vi = {k: (json.load(open(os.path.join(H, 'vi', k + '.json'))) if os.path.exists(os.path.join(H, 'vi', k + '.json')) else {}) for k in cases}
js = 'const CAST_TXT = ' + json.dumps(R('cast.txt'), ensure_ascii=False) + ';\nconst CASE_TXT = ' + json.dumps(cases, ensure_ascii=False) + ';\nconst VOICE_INDEX = ' + json.dumps(vi) + ';\n' + '\n'.join(R(f) for f in ['chars.js', 'scenes.js', 'parse.js', 'audio.js', 'engine.js'])
js = js.replace("if (typeof module !== 'undefined') module.exports = { parseCase, parseTarget };", '')
assert '</script' not in js
page = R('page.html').replace('/*CSS*/', R('style.css')).replace('/*JS*/', js)
out = os.path.join(H, '..', 'dist2'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'game.html'), 'w', encoding='utf-8').write(page)
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write('<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n' + page + '\n</body>\n</html>\n')
print('cases', list(cases), 'page bytes', len(page.encode()), 'voices', {k: len(v) for k, v in vi.items()})
