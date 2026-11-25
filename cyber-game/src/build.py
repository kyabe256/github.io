import json, os, re, shutil
H = os.path.dirname(os.path.abspath(__file__)); R = lambda p: open(os.path.join(H, p), encoding='utf-8').read()
story = R('story.txt'); idx = R('voice-index.json')
js = 'const STORY_TXT = ' + json.dumps(story, ensure_ascii=False) + ';\nconst VOICE_INDEX = ' + idx + ';\n' + '\n'.join(R(f) for f in ['chars.js', 'scenes.js', 'data.js', 'audio.js', 'engine.js'])
js = js.replace("if (typeof module !== 'undefined') module.exports = { CHARS };", '').replace("if (typeof module !== 'undefined') module.exports = { SCENES };", '').replace("if (typeof module !== 'undefined') module.exports = { EVID, PLACES, BATTLES };", '')
assert '</script' not in js
page = R('page.html').replace('/*CSS*/', R('style.css')).replace('/*JS*/', js)
out = os.path.join(H, '..', 'dist'); os.makedirs(out, exist_ok=True)
open(os.path.join(out, 'game.html'), 'w', encoding='utf-8').write(page)
full = '<!doctype html>\n<html lang="ja">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n' + page + '\n</body>\n</html>\n'
open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(full)
# checks: every block referenced exists, every voiced line has audio
blocks = set(re.findall(r'^## (\w+)', story, re.M)); refs = set(re.findall(r"'((?:pro|c1|c2|c3|b1|b2|b3|ep)_\w+)'", R('data.js') + R('engine.js')))
refs |= {'c2_miss_a', 'c2_miss_b', 'c2_miss_c'}; refs.discard('c2_miss_')
print('missing blocks', sorted(refs - blocks)); print('unused blocks', sorted(blocks - refs))
print('page bytes', len(page.encode()), 'voice bytes', os.path.getsize(os.path.join(out, 'voice.mp3')), 'voices', len(json.loads(idx)))
