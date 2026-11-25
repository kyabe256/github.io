/* ---------- characters v2: three-quarter view, ink lines, cel shadows, poses (box 240 x 360) ---------- */
const INK = '#2b1b2e';
function shade(hex, f){ const n = parseInt(hex.slice(1), 16); const m = v => Math.max(0, Math.min(255, Math.round(f < 1 ? v * f : v + (255 - v) * (f - 1)))); return '#' + [n >> 16, (n >> 8) & 255, n & 255].map(v => m(v).toString(16).padStart(2, '0')).join(''); }
const CHARS = {
  tsubasa:  {name:'翼', role:'日米統合サイバー捜査総監', sex:'m', skin:'#fbdcc4', hair:'#27324f', hs:'fresh', eye:'#2f7fd6', blush:1, brow:2.6, fit:{t:'suit', c:'#22335c', shirt:'#f4f7fb', lan:2}, es:'round', tilt:-3, jaw:0, pose:'stand'},
  kohei:    {name:'耕平', role:'父。食堂「こうへい」の店主', sex:'m', skin:'#eec4a0', hair:'#9a9da2', hs:'kohei', eye:'#6a4a34', sm:1, brow:3.2, wr:1, fit:{t:'chef', c:'#f3f0e8'}, wide:1, es:'soft', tilt:4, jaw:2, hsz:[1.04,0.98], pose:'cross'},
  takano:   {name:'鷹野', role:'警視庁警護課のSP', sex:'m', skin:'#efc9a8', hair:'#23262e', hs:'buzz', eye:'#4a6a5a', brow:3, fit:{t:'suit', c:'#16181d', shirt:'#f4f7fb', tie:'#2a2d36', ear:1}, wide:1, es:'cool', tilt:-6, jaw:1, hsz:[0.98,1.03], pose:'stand'},
  yuki:     {name:'結城', role:'警察庁の秘書官', sex:'f', skin:'#f9dcc6', hair:'#3a2a4a', hs:'bob', eye:'#b8527a', sm:1, brow:1.8, blush:1, fit:{t:'suit', c:'#2d3350', shirt:'#fdfdfd', bow:'#b23a48'}, es:'round', tilt:-2, jaw:0, pose:'tablet'},
  oconnor:  {name:'オコナー', role:'FBI副長官', sex:'f', skin:'#f3d3c0', hair:'#b9b4ad', hs:'shortf', eye:'#3f8fc2', brow:1.8, wr:1, fit:{t:'suit', c:'#3a3f4a', shirt:'#e9edf2', pin:1}, remote:1, es:'cool', tilt:-4, jaw:1},
  kane:     {name:'ケイン', role:'CIA副長官', sex:'f', skin:'#f4d6c4', hair:'#d8d4cc', hs:'shortf', eye:'#5aa07a', sm:1, brow:1.6, wr:1, fit:{t:'suit', c:'#5b4a5e', shirt:'#f6efe6', pin:1}, remote:1, es:'soft', tilt:5, jaw:0},
  chihaya:  {name:'千早', role:'警察庁の技官。元は高校生ハッカー', sex:'f', skin:'#fbe0cc', hair:'#c2622e', hs:'pony', eye:'#e08a1e', sm:1, brow:1.8, blush:1, fit:{t:'hoodie', c:'#2f8f8a', lan:1}, es:'round', tilt:2, jaw:0, hsz:[1.03,1.0], pose:'pocket'},
  hayase:   {name:'早瀬', role:'警視庁サイバー犯罪対策課長', sex:'m', skin:'#f1ccae', hair:'#2b3442', hs:'neat', eye:'#4a6a8a', brow:2.2, gl:'rect', fit:{t:'suit', c:'#55606e', shirt:'#f4f7fb', tie:'#31558a'}, es:'cool', tilt:-3, jaw:1, hsz:[0.97,1.04], pose:'chin'},
  onodera:  {name:'小野寺', role:'警察庁の捜査官。元は捜査一課の刑事', sex:'m', skin:'#e8bd98', hair:'#5a5550', hs:'neat', eye:'#7a5a3a', sm:1, brow:2.8, wr:1, beard:'stubble', fit:{t:'coat', c:'#b59a72', shirt:'#e9e4d8', tie:'#6b3b34'}, es:'half', tilt:6, jaw:1, hsz:[1.02,1.0], pose:'stand'},
  onizuka:  {name:'鬼塚', role:'警視庁捜査一課長', sex:'m', skin:'#e2b48e', hair:'#2a2424', hs:'buzz', eye:'#c26a2a', brow:3, wr:1, fit:{t:'suit', c:'#3b3029', shirt:'#ece7dd', tie:'#7a2a2a', loose:1}, wide:1, jaw:2, es:'cool', tilt:-9, jaw:2, hsz:[1.06,1.0], pose:'cross'},
  kanri:    {name:'システム管理者', role:'東都医科大学病院の情報システム部', sex:'m', skin:'#f6d5bc', hair:'#3d4a44', hs:'messy', eye:'#5a8a6a', brow:2, gl:'round', fit:{t:'shirt', c:'#dfe7ee', lan:1}, es:'round', tilt:6, jaw:0, hsz:[0.98,1.0]},
  furukawa: {name:'古川', role:'科捜研の物理の研究員（錠前、機械）', sex:'m', skin:'#e9c09c', hair:'#4a4d55', hs:'buzz', eye:'#5a6a7a', brow:3, wr:1, fit:{t:'work', c:'#2c5c94', patch:'科捜研'}, es:'narrow', tilt:0, jaw:2, pose:'cross'},
  shiraishi:{name:'白石', role:'警視庁科捜研の所長', sex:'m', skin:'#f0cfb4', hair:'#c9c9c9', hs:'thin', eye:'#6a7a8a', sm:1, brow:2.4, browc:'#b5b5b5', wr:1, gl:'round', fit:{t:'lab', c:'#fbfbf8', shirt:'#c7d6e6', tie:'#5a6b7d'}, es:'soft', tilt:6, jaw:0, hsz:[1.0,0.98], pose:'chin'},
  kiryu:    {name:'桐生', role:'科捜研の法医の研究員（DNA、血液）', sex:'f', skin:'#f8dac4', hair:'#2a2a52', hs:'long', eye:'#7a5ac2', brow:1.8, fit:{t:'lab', c:'#fbfbf8', shirt:'#d7c9e6'}, es:'cool', tilt:-5, jaw:0, pose:'tablet'},
  miyashita:{name:'宮下', role:'科捜研の化学の研究員（薬物、毒物）', sex:'m', skin:'#f2cdb0', hair:'#4a3a30', hs:'neat', eye:'#7a6a3a', sm:1, brow:2.4, fit:{t:'lab', c:'#fbfbf8', shirt:'#cfe3d2'}, wide:1, es:'half', tilt:5, jaw:2, hsz:[1.07,0.98]},
  sawaguchi:{name:'沢口', role:'警視庁の捜査官。ログの人', sex:'m', skin:'#f4d2b8', hair:'#2a4a52', hs:'messy', eye:'#3a9a9a', brow:2.2, gl:'rect', fit:{t:'shirt', c:'#3f4a5c', lan:1}, es:'half', tilt:0, jaw:1, pose:'stand'},
  mendes:   {name:'メンデス', role:'FBIのサイバー捜査官。班の取りまとめ', sex:'m', skin:'#cf9f76', hair:'#2a221e', hs:'slick', eye:'#8a5a2a', sm:1, brow:3, beard:'goatee', fit:{t:'work', c:'#1d2b4a', patch:'FBI', patchc:'#f2c230'}, wide:1, es:'soft', tilt:-2, jaw:2, hsz:[1.04,1.0], pose:'cross'},
  rosen:    {name:'ローゼン', role:'FBIの会計担当の捜査官', sex:'f', skin:'#f2d0bb', hair:'#a8683a', hs:'wavy', eye:'#4a9a5a', brow:1.8, gl:'round', fit:{t:'suit', c:'#3d4a44', shirt:'#f3efe8'}, remote:1, es:'soft', tilt:-3, jaw:0},
  hori:     {name:'堀', role:'メディコア・ジャパンの保守担当', sex:'m', skin:'#efc8a8', hair:'#4a3a32', hs:'messy', eye:'#7a6a5a', brow:2.4, fit:{t:'work', c:'#6f8596', patch:'MEDICORE'}, es:'soft', tilt:7, jaw:1, pose:'hands'},
  kacho:    {name:'保守部の課長', role:'メディコア・ジャパン', sex:'m', skin:'#ebc3a2', hair:'#7f7f84', hs:'thin', eye:'#6a5a4a', brow:2.6, browc:'#77777a', wr:1, fit:{t:'work', c:'#6f8596', patch:'MEDICORE'}, wide:1, es:'narrow', tilt:4, jaw:2, hsz:[1.05,0.98]},
  news:     {name:'テレビ', noart:1}
};

/* hair: f = front (over the face), b = back (behind head and neck), x = extra strands drawn last, hl = highlight arc */
const HAIR = {
  fresh: { b: 'M62 104 C56 128 62 146 78 154 C76 138 78 122 84 110 Z',
    f: 'M60 114 C50 66 76 28 122 26 C162 26 178 56 171 98 C169 106 167 110 164 112 C165 98 161 86 155 77 C153 88 149 96 142 102 C143 91 139 81 132 74 C126 89 114 101 99 105 C104 97 106 88 104 80 C96 91 86 99 79 103 C79 112 77 120 74 128 C69 126 63 121 60 114 Z',
    x: 'M118 28 C112 16 122 8 132 12 C126 16 124 22 126 28 Z', hl: 'M82 56 C98 40 130 36 152 48' },
  neat: { b: 'M62 104 C58 124 64 140 76 148 C74 134 76 120 82 110 Z',
    f: 'M62 112 C52 66 78 30 122 28 C160 28 176 56 169 100 C167 88 161 79 151 74 C132 70 111 76 96 87 C88 93 82 101 79 111 C77 119 75 125 73 130 C67 126 63 120 62 112 Z', hl: 'M84 54 C100 40 132 38 152 50' },
  buzz: { f: 'M66 106 C58 66 84 36 122 34 C156 34 172 58 167 94 C163 81 154 73 142 71 L104 73 C92 77 84 87 81 99 C79 107 77 113 75 120 C70 116 66 111 66 106 Z', hl: 'M88 54 C104 44 134 44 150 54' },
  slick: { b: 'M64 100 C60 118 64 134 74 142 C72 128 74 116 80 106 Z',
    f: 'M64 108 C54 62 84 32 122 30 C158 30 174 56 167 92 C161 73 145 62 121 64 C101 66 87 80 81 98 C79 108 77 115 75 122 C69 118 65 113 64 108 Z', hl: 'M86 52 C104 42 134 42 150 52', x: 'M96 68 C108 56 132 52 150 60 M90 78 C104 64 130 58 154 68' },
  messy: { b: 'M60 104 C52 130 60 150 78 158 C74 142 76 124 84 110 Z',
    f: 'M58 116 C46 64 76 24 122 24 C164 24 182 58 173 102 C171 97 169 93 165 89 C165 97 161 105 154 109 C155 99 151 89 144 82 C140 93 132 101 122 105 C124 97 124 89 120 82 C112 93 102 101 90 105 C92 99 92 93 90 87 C84 95 80 103 79 113 C77 121 75 127 73 132 C65 128 60 122 58 116 Z',
    x: 'M104 26 C96 14 104 6 114 10 C110 14 110 20 112 26 Z M138 26 C142 14 152 12 158 18 C152 20 148 24 148 30 Z', hl: 'M80 56 C96 38 132 34 154 48' },
  thin: { f: 'M66 112 C58 90 64 64 82 54 C78 72 76 92 79 110 C77 118 75 124 73 128 C69 124 66 118 66 112 Z M82 54 C100 38 146 36 162 58 C144 50 104 50 82 54 Z M160 60 C168 72 170 86 167 98 C165 86 162 72 158 64 Z', hl: '' },
  bob: { b: 'M54 152 C42 80 72 26 122 26 C168 26 188 70 176 140 C174 152 166 156 161 148 L161 100 L80 104 L84 152 C76 163 58 162 54 152 Z',
    f: 'M60 114 C52 68 80 32 122 32 C160 32 176 60 169 102 C159 93 147 89 132 89 C110 89 92 95 79 107 C77 121 77 136 79 148 C68 144 62 132 60 114 Z', hl: 'M82 58 C98 44 134 42 154 54' },
  pony: { b: 'M72 56 C40 46 20 84 28 132 C32 154 46 166 53 152 C44 128 48 100 72 84 Z M74 104 C69 126 71 146 78 158 C83 144 83 122 83 106 Z',
    f: 'M60 114 C50 66 76 28 122 26 C162 26 178 56 171 98 C169 106 167 110 164 112 C165 98 161 86 155 77 C152 89 146 97 138 101 C139 91 135 82 128 76 C120 89 110 99 97 103 C101 96 102 88 101 81 C93 90 85 98 79 103 C79 112 77 120 74 128 C69 126 63 121 60 114 Z',
    x: 'M116 28 C108 12 122 2 134 10 C126 13 122 20 124 28 Z', hl: 'M82 56 C98 40 130 36 152 48', tie: [66, 70] },
  long: { b: 'M52 152 C40 76 72 26 122 26 C168 26 190 72 178 150 L172 236 C150 246 78 246 60 236 Z',
    f: 'M60 116 C52 68 82 32 122 32 C158 32 176 60 169 106 C165 89 153 73 135 64 C116 75 94 91 80 107 C78 124 78 142 81 156 C68 150 62 136 60 116 Z', hl: 'M82 58 C98 44 132 42 154 54' },
  wavy: { b: 'M50 162 C38 80 70 26 122 26 C170 26 192 74 180 150 C188 172 180 194 165 192 C169 178 165 167 161 161 L161 100 L80 104 L84 168 C78 174 76 186 82 196 C66 200 52 182 50 162 Z',
    f: 'M60 116 C52 66 82 32 122 32 C158 32 176 60 169 106 C161 91 149 81 135 77 C118 91 98 99 80 109 C78 125 78 140 81 152 C68 148 62 134 60 116 Z', hl: 'M82 58 C98 44 134 42 154 54' },
  shortf: { b: 'M56 134 C46 70 76 26 122 26 C166 26 186 66 176 124 C174 132 166 134 161 128 L161 100 L80 104 L82 136 C76 143 60 142 56 134 Z',
    f: 'M60 114 C52 66 82 32 122 32 C158 32 176 60 169 106 C167 97 163 91 159 87 C149 81 141 73 135 64 C122 79 100 89 85 91 C81 101 79 111 77 124 C68 124 62 120 60 114 Z', hl: 'M82 58 C98 44 134 42 154 54' },
  kohei: { f: 'M66 112 C62 98 64 86 70 78 L80 92 C78 100 78 108 76 124 C70 122 67 118 66 112 Z M160 74 C166 82 168 92 166 100 L158 88 Z', cap: 1, hl: '' }
};
/* eyes: [half width, up, down] for the near eye; tilt rotates the outer corner up (-) or down (+) */
const EYES = { round: [14, -17, 11], soft: [14, -14, 10], cool: [14.5, -11, 8.5], narrow: [13.5, -8.5, 7], half: [14, -9, 9.5] };
function eyeSVG(id, near, c){
  const st = EYES[c.es] || EYES.soft, k = near ? 1 : 0.7, w = st[0] * k, up = st[1], dn = st[2], F = c.sex === 'f';
  const cx = near ? 105 : 147, cy = near ? 121 : 120, cid = 'cl-' + id + (near ? 'n' : 'f'), gid = 'ig-' + id + (near ? 'n' : 'f'), tilt = (c.tilt || 0) * (near ? -1 : 1), o = near ? -1 : 1;
  const shape = `M${-w} 2 C${-w * 0.75} ${up} ${w * 0.65} ${up} ${w} 0 C${w * 0.75} ${dn} ${-w * 0.65} ${dn} ${-w} 2Z`;
  const irx = w * 0.66, iry = (dn - up) * 0.55, icy = up + iry * 0.96 + (c.es === 'half' ? 2 : 0), ec = c.eye, el = shade(ec, 1.8), ed = shade(ec, .42), ix = near ? 0.5 : 1;
  const lash = `M${-w - 1.5} 3 C${-w * 0.75} ${up - 1.2} ${w * 0.65} ${up - 1.2} ${w + 1.2} 0.2 L${w + o * 0 + (o > 0 ? 4 : 1)} ${o > 0 ? -3.5 : 0} C${w * 0.6} ${up - (F ? 5 : 4)} ${-w * 0.7} ${up - (F ? 4.6 : 3.6)} ${-w - (o < 0 ? 4.5 : 1.5)} ${o < 0 ? -1.5 : 3} Z`;
  return `<g class="eye" transform="translate(${cx} ${cy}) rotate(${tilt})"><clipPath id="${cid}"><path d="${shape}"/></clipPath>
   <linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${ed}"/><stop offset=".5" stop-color="${ec}"/><stop offset="1" stop-color="${el}"/></linearGradient>
   <g class="eye-open"><path d="${shape}" fill="#fff"/><g clip-path="url(#${cid})"><g class="iris" transform="translate(${ix} 0)"><ellipse cy="${icy}" rx="${irx}" ry="${iry}" fill="url(#${gid})" stroke="${ed}" stroke-width="1.3"/><ellipse cy="${icy - iry * 0.08}" rx="${irx * 0.44}" ry="${iry * 0.5}" fill="${shade(ec, .2)}"/><path d="M${-irx} ${icy + iry * 0.35} Q0 ${icy + iry * 1.1} ${irx} ${icy + iry * 0.35} L${irx} ${icy + iry} L${-irx} ${icy + iry}Z" fill="#fff" opacity=".28"/><ellipse cx="${-irx * 0.42}" cy="${icy - iry * 0.46}" rx="${irx * 0.4}" ry="${iry * 0.3}" fill="#fff"/><circle cx="${irx * 0.44}" cy="${icy + iry * 0.4}" r="${irx * 0.19}" fill="#fff"/></g><path d="M${-w} ${up - 1} h${2 * w} v${-up * 0.28} Q0 ${up * 0.42} ${-w} ${up * 0.72}Z" fill="#3b2550" opacity=".2"/></g>
   <path d="${lash}" fill="${INK}"/>${F ? `<path d="M${o * (w - 2)} ${up * 0.5} l${o * 5} -4 M${o * (w - 6)} ${up * 0.82} l${o * 4} -5" stroke="${INK}" stroke-width="1.6" stroke-linecap="round"/>` : ''}<path d="M${-w * 0.7} ${up - 4.5} Q0 ${up - 8} ${w * 0.75} ${up - 4}" fill="none" stroke="${shade(c.skin, .62)}" stroke-width="1.1" stroke-linecap="round"/><path d="M${o * w * 0.25} ${dn - 0.2} Q${o * w * 0.65} ${dn} ${o * w * 0.95} ${dn * 0.5}" fill="none" stroke="${shade(c.skin, .55)}" stroke-width="1.2" stroke-linecap="round"/></g>
   <path class="eye-shut" d="M${-w} 2 Q0 ${dn * 0.85} ${w} 1" fill="none" stroke="${INK}" stroke-width="3" stroke-linecap="round"/>
   <path class="eye-smile" d="M${-w} 4 Q0 ${up * 0.7} ${w} 3" fill="none" stroke="${INK}" stroke-width="3.2" stroke-linecap="round"/></g>`;
}
function armSVG(c, col, dk){
  const sk = c.skin, sd = shade(sk, .84), st = `stroke="${INK}" stroke-width="1.6" stroke-linejoin="round"`, p = c.pose || 'stand';
  const hand = (x, y, r = 0) => `<g transform="translate(${x} ${y}) rotate(${r})"><path d="M-9 -7 C-2 -11 8 -9 12 -3 C14 2 12 8 6 10 C-2 12 -9 8 -11 2 Z" fill="${sk}" ${st}/><path d="M-3 -1 L7 1 M-4 4 L6 6" stroke="${sd}" stroke-width="1.2" fill="none" stroke-linecap="round"/></g>`;
  if (p === 'cross') return `<g class="arms"><path d="M46 262 C70 252 120 262 168 276 L172 304 C128 300 86 302 52 310 Z" fill="${col}" ${st}/><path d="M192 252 C168 250 120 268 70 290 L62 316 C108 312 158 300 196 290 Z" fill="${shade(col, 1.08)}" ${st}/><path d="M70 290 L62 316" stroke="${dk}" stroke-width="5"/>${hand(58, 300, -20)}${hand(176, 290, 160)}</g>`;
  if (p === 'tablet') return `<g class="arms"><g transform="rotate(-7 128 290)"><rect x="92" y="246" width="76" height="98" rx="7" fill="#20242e" ${st}/><rect x="98" y="253" width="64" height="82" rx="3" fill="#bfe6ff"/><path d="M104 266 h40 M104 278 h52 M104 290 h30 M104 302 h46" stroke="#4a7fb0" stroke-width="3" stroke-linecap="round"/></g>${hand(92, 306, 60)}${hand(170, 292, 120)}</g>`;
  if (p === 'pocket') return `<g class="arms"><path d="M70 296 C92 284 148 284 170 296 L164 336 C138 344 100 344 76 336 Z" fill="${shade(col, 1.1)}" ${st}/><path d="M84 300 C96 312 96 326 86 336 M156 300 C144 312 144 326 154 336" stroke="${dk}" stroke-width="2" fill="none"/></g>`;
  if (p === 'chin') return `<g class="arms"><path d="M196 360 C198 320 186 268 158 214 L138 222 C152 270 160 320 160 360 Z" fill="${shade(col, 1.06)}" ${st}/><path d="M160 214 L138 222 L136 212 L156 204 Z" fill="#f4f4f4" ${st}/>${hand(142, 196, -70)}</g>`;
  if (p === 'hands') return `<g class="arms hands"><path d="M152 296 C142 296 132 302 128 310 L134 326 C142 322 154 318 160 314 Z" fill="${sk}" ${st}/><rect class="watch" x="142" y="291" width="21" height="10" rx="3.5" fill="#e0b84a" stroke="#7a5a14" stroke-width="1.2"/><circle cx="152.5" cy="296" r="3.4" fill="#fff8de" stroke="#7a5a14" stroke-width=".8"/><g class="hand-r"><path d="M92 296 C102 296 114 302 120 310 L114 326 C106 322 94 318 86 314 Z" fill="${sk}" ${st}/><path d="M98 308 L114 314 M96 313 L111 319" stroke="${sd}" stroke-width="1.1"/></g></g>`;
  return '';
}
function outfitSVG(id, c, flip){
  const f = c.fit, col = f.c, dk = shade(col, .72), lt = shade(col, 1.16), F = c.sex === 'f', W = c.wide ? 1 : 0, st = `stroke="${INK}" stroke-width="1.8" stroke-linejoin="round"`;
  const body = F ? 'M50 360 L56 254 C58 232 80 220 100 208 L114 214 L134 206 C156 214 178 224 182 250 L190 360 Z'
             : W ? 'M22 360 L30 250 C32 222 64 208 96 198 L114 208 L136 196 C168 204 202 216 206 246 L216 360 Z'
                 : 'M32 360 L40 252 C42 226 70 212 98 202 L114 210 L134 200 C162 208 192 220 196 248 L204 360 Z';
  const cx = 118; let s = '';
  const txt = (x, y, t, size, fill) => `<text x="${x}" y="${y}" font-size="${size}" text-anchor="middle" font-weight="900" fill="${fill}" font-family="sans-serif"${flip ? ` transform="translate(${2 * x} 0) scale(-1 1)"` : ''}>${t}</text>`;
  const lany = n => { let o = ''; for (let i = 0; i < n; i++){ const dx = i * 17; o += `<path d="M${104 - i * 3} 208 L${110 + dx} 290 M${134 + i * 3} 204 L${126 + dx} 290" stroke="${i ? '#2a7fd6' : '#d6382f'}" stroke-width="3.2" fill="none"/><rect x="${107 + dx}" y="288" width="23" height="31" rx="3" fill="#fbfbf6" stroke="${INK}" stroke-width="1.3"/><rect x="${111 + dx}" y="293" width="9" height="10" fill="${i ? '#2a7fd6' : '#4a5a7a'}"/><path d="M${111 + dx} 308 h15 M${111 + dx} 312 h10" stroke="#8a8a8a" stroke-width="1.4"/>`; } return o; };
  if (f.t === 'suit' || f.t === 'coat' || f.t === 'lab'){
    s += `<path d="${body}" fill="${col}" ${st}/>`;
    s += `<path d="M98 202 L${cx + 2} 262 L136 200 L128 192 L${cx} 210 L106 194 Z" fill="${f.shirt}" stroke="${INK}" stroke-width="1.2"/>`;
    if (f.tie) s += `<path d="M${cx - 5} ${f.loose ? 220 : 212} L${cx + 5} ${f.loose ? 219 : 211} L${cx + 4} ${f.loose ? 228 : 220} L${cx + 9} 268 L${cx + 2} 280 L${cx - 5} 268 L${cx - 3} ${f.loose ? 228 : 220} Z" fill="${f.tie}" stroke="${INK}" stroke-width="1.2" stroke-linejoin="round"/>`;
    if (f.bow) s += `<path d="M${cx} 216 L${cx - 15} 207 L${cx - 14} 227 Z M${cx} 216 L${cx + 15} 206 L${cx + 15} 226 Z" fill="${f.bow}" stroke="${INK}" stroke-width="1.2" stroke-linejoin="round"/><circle cx="${cx}" cy="216" r="3.8" fill="${shade(f.bow, .78)}" stroke="${INK}" stroke-width="1"/>`;
    s += `<path d="M105 193 L${cx} 212 L99 218 Z M129 191 L${cx} 212 L137 216 Z" fill="${shade(f.shirt, .95)}" stroke="${INK}" stroke-width="1.2" stroke-linejoin="round"/>`;
    s += `<path d="M98 202 L80 218 L${cx - 6} 288 L${cx + 2} 262 Z" fill="${lt}" ${st}/><path d="M136 200 L156 214 L${cx + 10} 286 L${cx + 2} 262 Z" fill="${lt}" ${st}/>`;
    s += `<path d="M${cx + 2} 282 L${cx + 4} 360" stroke="${INK}" stroke-width="1.6"/><circle cx="${cx + 3}" cy="312" r="3" fill="${dk}" stroke="${INK}" stroke-width="1"/><circle cx="${cx + 4}" cy="340" r="3" fill="${dk}" stroke="${INK}" stroke-width="1"/>`;
    if (f.t === 'lab') s += `<path d="M152 292 h26 v32 h-26 Z" fill="${shade(col, .96)}" stroke="${INK}" stroke-width="1.2"/><path d="M158 292 v-10 M164 292 v-12" stroke="#3a62c8" stroke-width="2.6" stroke-linecap="round"/><path d="M170 292 v-9" stroke="#d33" stroke-width="2.6" stroke-linecap="round"/>`;
    if (f.t === 'coat') s += `<path d="M58 244 L78 234 M182 240 L162 232" stroke="${INK}" stroke-width="1.6"/><rect x="60" y="300" width="26" height="8" rx="2" fill="${dk}" stroke="${INK}" stroke-width="1"/>`;
    if (f.pin) s += `<circle cx="88" cy="240" r="4" fill="#f0c44a" stroke="${INK}" stroke-width="1"/>`;
    if (f.ear) s += `<path d="M82 132 C74 142 78 160 86 170 C88 182 88 196 96 206" stroke="#e8e8e8" stroke-width="1.8" fill="none" stroke-dasharray="2.5 2.5"/>`;
  } else if (f.t === 'chef'){
    s += `<path d="${body}" fill="${col}" ${st}/><path d="M98 202 L130 268 L120 282 L90 220 Z" fill="${shade(col, .92)}" stroke="${INK}" stroke-width="1.3" stroke-linejoin="round"/><path d="M136 200 L108 262" stroke="${INK}" stroke-width="1.4"/>`;
    s += `<path d="M58 280 L182 276 L192 360 L48 360 Z" fill="#2a3a5c" ${st}/><path d="M104 204 L${cx} 222 L134 202" fill="none" stroke="#d6cfbe" stroke-width="6" stroke-linecap="round"/>`;
  } else if (f.t === 'hoodie'){
    s += `<path d="M70 214 C76 184 162 180 168 210 C162 232 78 236 70 214 Z" fill="${dk}" ${st}/><path d="${body}" fill="${col}" ${st}/>`;
    s += `<path d="M100 206 L${cx} 240 L138 204 L130 196 L${cx} 212 L106 198 Z" fill="#fbf8f0" stroke="${INK}" stroke-width="1.2"/><path d="M100 206 L${cx} 242 L138 204" fill="none" stroke="${dk}" stroke-width="6" stroke-linejoin="round"/>`;
    s += `<path d="M110 238 L108 280 M126 238 L128 280" stroke="#fbf8f0" stroke-width="2.6" stroke-linecap="round"/><circle cx="108" cy="282" r="3" fill="#fbf8f0" stroke="${INK}" stroke-width="1"/><circle cx="128" cy="282" r="3" fill="#fbf8f0" stroke="${INK}" stroke-width="1"/>`;
  } else if (f.t === 'shirt'){
    s += `<path d="${body}" fill="${col}" ${st}/><path d="M105 196 L${cx} 216 L98 226 Z M129 194 L${cx} 216 L139 222 Z" fill="${lt}" stroke="${INK}" stroke-width="1.3" stroke-linejoin="round"/><path d="M${cx} 216 L${cx + 4} 360" stroke="${INK}" stroke-width="1.4"/><circle cx="${cx + 1}" cy="246" r="2.2" fill="${dk}"/><circle cx="${cx + 2}" cy="280" r="2.2" fill="${dk}"/><circle cx="${cx + 3}" cy="314" r="2.2" fill="${dk}"/>`;
  } else if (f.t === 'work'){
    s += `<path d="${body}" fill="${col}" ${st}/><path d="M100 204 L${cx} 230 L138 202 L130 194 L${cx} 212 L106 196 Z" fill="#eeeae2" stroke="${INK}" stroke-width="1.2"/><path d="M104 196 L${cx} 222 L90 232 L88 212 Z M130 194 L${cx} 222 L148 228 L150 210 Z" fill="${lt}" stroke="${INK}" stroke-width="1.4" stroke-linejoin="round"/><path d="M${cx} 222 L${cx + 4} 360" stroke="${INK}" stroke-width="2.4"/><rect x="${cx - 3}" y="228" width="7" height="10" rx="1.5" fill="#d4d4d4" stroke="${INK}" stroke-width="1"/>`;
    const pw = f.patch.length > 4 ? 48 : 36; s += `<rect x="140" y="250" width="${pw}" height="16" rx="2.5" fill="${f.patchc ? '#14203a' : '#fafaf4'}" stroke="${INK}" stroke-width="1.2"/>` + txt(140 + pw / 2, 262, f.patch, f.patch.length > 4 ? 8 : 10.5, f.patchc || '#2a3a4a');
  }
  /* cel shadow on the far side and under the collar */
  s += `<path d="${body}" fill="#2d1b4e" opacity=".14" clip-path="inset(0 0 0 62%)"/><path d="M96 200 C104 214 128 214 138 198 L150 212 C132 232 104 232 84 216 Z" fill="#2d1b4e" opacity=".13"/>`;
  if (f.lan) s += lany(f.lan);
  s += armSVG(c, col, dk);
  return s;
}
function charSVG(id, flip){
  const c = CHARS[id]; if (!c || c.noart) return '';
  const sk = c.skin, sd = shade(sk, .86), hc = c.hair, hd = shade(hc, .7), hl = shade(hc, 1.75), H = HAIR[c.hs], F = c.sex === 'f', bc = c.browc || shade(hc, .78), sh = c.hsz || [1, 1];
  const jaw = c.jaw === 2 ? 'C74 136 84 156 102 165 C114 171 128 172 138 168 C152 161 161 148 164 132'   /* square */
            : c.jaw === 1 ? 'C74 134 86 152 104 162 C114 168 126 169 134 165 C148 158 158 146 162 130'   /* standard */
                          : 'C74 132 88 150 106 161 C116 167 126 168 133 164 C146 157 157 145 161 129';  /* soft, small chin */
  const face = `M76 108 ${jaw} C164 122 163 116 160 110 C162 100 162 86 156 72 C146 52 100 48 82 72 C78 82 76 94 76 108 Z`;
  const st = `stroke="${INK}" stroke-width="1.8" stroke-linejoin="round"`;
  let s = `<g class="ch-root"${flip ? ' transform="translate(240 0) scale(-1 1)"' : ''}><g class="ch-body">`;
  if (H.b) s += `<g class="ch-hairb"><g transform="translate(118 170) scale(${1.2 * sh[0]} ${1.2 * sh[1]}) translate(-118 -170)"><path d="${H.b}" fill="${hd}" ${st}/></g></g>`;
  s += `<path d="M100 168 L96 212 Q114 222 134 210 L132 172 Z" fill="${sd}" ${st}/><path d="M100 174 C112 186 126 184 132 176 L132 190 C120 198 108 196 99 186 Z" fill="#2d1b4e" opacity=".22"/>`;
  s += outfitSVG(id, c, flip);
  s += `<g class="ch-head"><g transform="translate(118 170) scale(${1.2 * sh[0]} ${1.2 * sh[1]}) translate(-118 -170)">`;
  s += `<path d="M79 106 C67 102 62 118 67 129 C70 137 78 138 81 131 Z" fill="${sk}" ${st}/><path d="M74 112 C70 116 70 124 74 128" fill="none" stroke="${shade(sk, .66)}" stroke-width="1.4" stroke-linecap="round"/>`;
  s += `<path d="${face}" fill="${sk}" ${st}/>`;
  s += `<path d="M82 72 C100 48 146 52 156 72 C160 82 161 92 160 100 C150 88 138 84 124 86 C106 88 90 96 78 106 C78 94 79 82 82 72 Z" fill="#2d1b4e" opacity=".07"/>`;
  s += `<ellipse cx="92" cy="141" rx="10" ry="5.5" fill="#ff8a80" opacity="${c.blush ? .5 : .22}"/><ellipse cx="153" cy="139" rx="6" ry="5" fill="#ff8a80" opacity="${c.blush ? .5 : .22}"/>`;
  if (c.blush) s += `<path d="M86 139 l3 5 M91 138 l3 5 M96 139 l3 5" stroke="#f0625a" stroke-width="1.1" stroke-linecap="round" opacity=".65"/>`;
  if (c.wr) s += `<path d="M86 127 l-5 2 M86 130 l-4 4 M159 126 l4 2" stroke="${shade(sk, .66)}" stroke-width="1.1" fill="none" stroke-linecap="round"/>`;
  if (c.beard === 'stubble') s += `<path d="M92 146 C100 160 114 167 128 167 C142 165 154 154 160 140 C152 154 142 160 128 161 C112 161 100 156 92 146 Z" fill="${shade(sk, .7)}" opacity=".45"/>`;
  if (c.beard === 'goatee') s += `<path d="M120 158 C124 155 136 155 140 158 C140 165 136 169 130 169 C124 169 120 165 120 158 Z" fill="${hc}" stroke="${INK}" stroke-width="1"/>`;
  s += eyeSVG(id, true, c) + eyeSVG(id, false, c);
  const by = { round: 99, soft: 102, cool: 105, narrow: 108, half: 104 }[c.es] || 102, bw = Math.min(c.brow, 3.4);
  s += `<path class="brow brow-l" d="M88 ${by + 3} Q102 ${by - 4} 119 ${by + 1}" stroke="${bc}" stroke-width="${bw}" stroke-linecap="round" fill="none"/><path class="brow brow-r" d="M157 ${by + 1} Q148 ${by - 3} 137 ${by}" stroke="${bc}" stroke-width="${bw}" stroke-linecap="round" fill="none"/>`;
  s += `<path d="M137 128 L141 138 L135.5 140" stroke="${shade(sk, .56)}" stroke-width="1.7" fill="none" stroke-linecap="round" stroke-linejoin="round"/><path d="M141 138 L136 141 L138 136Z" fill="#2d1b4e" opacity=".14"/>`;
  s += `<g class="mouth" transform="translate(131 152)"><path class="m-shape" d="M-5 0 Q0 3.5 4 0" stroke="#8a3f44" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><g class="m-open"><path d="M-6.5 -2 Q0 -3.6 5.5 -2 Q5 6.6 -0.5 7 Q-5.6 6.4 -6.5 -2Z" fill="#8a2f38" stroke="${INK}" stroke-width="1.2"/><path d="M-5 -1.8 Q0 -3 4.4 -1.8 L4 -0.2 Q0 -1 -4.6 -0.2Z" fill="#fff"/><ellipse cx="-0.4" cy="4.4" rx="3.2" ry="1.9" fill="#ff9a94"/></g></g>`;
  if (c.gl === 'rect') s += `<g fill="rgba(214,238,255,.26)" stroke="${INK}" stroke-width="2.2"><rect x="87" y="108" width="36" height="26" rx="7"/><rect x="134" y="108" width="27" height="25" rx="6"/><path d="M123 119 h11 M87 118 L76 114" fill="none"/></g><path d="M92 113 l9 -1 M139 113 l6 -1" stroke="#fff" stroke-width="2.4" opacity=".85" stroke-linecap="round"/>`;
  if (c.gl === 'round') s += `<g fill="rgba(214,238,255,.24)" stroke="#6a5444" stroke-width="2"><circle cx="105" cy="122" r="18"/><ellipse cx="148" cy="121" rx="13.5" ry="17"/><path d="M123 120 h11.5 M87 120 L76 116" fill="none"/></g><path d="M94 111 l7 -3 M141 110 l5 -2" stroke="#fff" stroke-width="2.4" opacity=".85" stroke-linecap="round"/>`;
  if (H.f) s += `<path d="${H.f}" fill="${hc}" ${st}/>`;
  if (H.x) s += `<path d="${H.x}" fill="${H.x.includes('Z') ? hc : 'none'}" stroke="${H.x.includes('Z') ? INK : shade(hc, .55)}" stroke-width="${H.x.includes('Z') ? 1.8 : 1.4}" stroke-linejoin="round" stroke-linecap="round"/>`;
  if (H.hl) s += `<path d="${H.hl}" stroke="${hl}" stroke-width="6.5" fill="none" stroke-linecap="round" opacity=".75"/><path d="${H.hl}" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" opacity=".55" transform="translate(0 -1.5)"/>`;
  if (H.tie) s += `<circle cx="${H.tie[0]}" cy="${H.tie[1]}" r="6.5" fill="#ffcf3a" stroke="${INK}" stroke-width="1.5"/>`;
  if (H.cap) s += `<path d="M66 82 C60 44 88 26 122 26 C154 26 176 44 170 80 C150 70 88 72 66 82 Z" fill="#fffdf8" ${st}/><path d="M66 82 C88 72 150 70 170 80 L170 68 C150 58 88 60 66 70 Z" fill="#e9e3d4" stroke="${INK}" stroke-width="1.4"/>`;
  s += `<g class="fx-sweat"><path d="M176 82 C182 94 184 101 178 105 C172 101 171 94 176 82 Z" fill="#bfe8fc" stroke="${INK}" stroke-width="1.3"/></g>`;
  s += `<g class="fx-anger" transform="translate(66 60)"><path d="M-8 -2.5 L-2.5 -2.5 L-2.5 -8 M2.5 -8 L2.5 -2.5 L8 -2.5 M8 2.5 L2.5 2.5 L2.5 8 M-2.5 8 L-2.5 2.5 L-8 2.5" stroke="#e8382f" stroke-width="3.2" fill="none" stroke-linecap="round"/></g>`;
  s += `</g></g></g></g>`;
  return s;
}
const MOUTHS = { n: 'M-5 0 Q0 3.5 4 0', s: 'M-7.5 -2 Q-1 8.5 6 -2 Z', a: 'M-6 2.5 Q-1 -2.5 5 2', t: 'M-6 1 Q-3 -2 0 1 Q3 4 5.5 1', u: 'M-3.2 -3 Q0 -5 3 -3 Q4.4 1 3 4 Q0 6 -3.2 4 Q-4.6 1 -3.2 -3Z', k: 'M-5 1 Q0 2 4 0.6', d: 'M-5 2.2 Q0 -1.5 4.4 2' };
const BROWS = { n: [0, 0], s: [-4, -2], a: [14, 3], t: [-12, -1], u: [-5, -6], k: [8, 2], d: [-14, 0] };
function applyExpr(g, e){
  if (!g) return; e = MOUTHS[e] ? e : 'n'; g.dataset.e = e;
  const m = g.querySelector('.m-shape'); if (m){ m.setAttribute('d', MOUTHS[e]); m.setAttribute('fill', e === 'u' ? '#8a2f38' : e === 's' ? '#c9524e' : 'none'); }
  const c = CHARS[g.dataset.id] || {}; g.classList.toggle('eyes-smile', e === 's' && !!c.sm);
  const [rot, dy] = BROWS[e], bl = g.querySelector('.brow-l'), br = g.querySelector('.brow-r');
  if (bl){ bl.style.transform = `translate(0px,${dy}px) rotate(${rot}deg)`; br.style.transform = `translate(0px,${dy}px) rotate(${-rot}deg)`; }
}
