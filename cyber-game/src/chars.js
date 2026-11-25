/* ---------- characters: parametric SVG busts (240 x 340) ---------- */
const CHARS = {
  tsubasa:  {name:'翼', role:'日米統合サイバー捜査総監', sex:'m', skin:'#fbdcc4', hair:'#27324f', hs:'fresh', eye:'#2f7fd6', es:'round', blush:1, brow:2.6, fit:{t:'suit', c:'#22335c', shirt:'#f4f7fb', lan:2}},
  kohei:    {name:'耕平', role:'父。食堂「こうへい」の店主', sex:'m', skin:'#eec4a0', hair:'#9a9da2', hs:'kohei', eye:'#6a4a34', es:'soft', sm:1, brow:3.2, wr:1, fit:{t:'chef', c:'#f3f0e8'}, wide:1},
  takano:   {name:'鷹野', role:'警視庁警護課のSP', sex:'m', skin:'#efc9a8', hair:'#23262e', hs:'buzz', eye:'#4a6a5a', es:'soft', brow:3, fit:{t:'suit', c:'#16181d', shirt:'#f4f7fb', tie:'#2a2d36', ear:1}, wide:1},
  yuki:     {name:'結城', role:'警察庁の秘書官', sex:'f', skin:'#f9dcc6', hair:'#3a2a4a', hs:'bob', eye:'#b8527a', es:'round', sm:1, brow:1.8, blush:1, fit:{t:'suit', c:'#2d3350', shirt:'#fdfdfd', bow:'#b23a48'}},
  oconnor:  {name:'オコナー', role:'FBI副長官', sex:'f', skin:'#f3d3c0', hair:'#b9b4ad', hs:'shortf', eye:'#3f8fc2', es:'soft', brow:1.8, wr:1, fit:{t:'suit', c:'#3a3f4a', shirt:'#e9edf2', pin:1}, remote:1},
  kane:     {name:'ケイン', role:'CIA副長官', sex:'f', skin:'#f4d6c4', hair:'#d8d4cc', hs:'shortf', eye:'#5aa07a', es:'soft', sm:1, brow:1.6, wr:1, fit:{t:'suit', c:'#5b4a5e', shirt:'#f6efe6', pin:1}, remote:1},
  chihaya:  {name:'千早', role:'警察庁の技官。元は高校生ハッカー', sex:'f', skin:'#fbe0cc', hair:'#c2622e', hs:'pony', eye:'#e08a1e', es:'round', sm:1, brow:1.8, blush:1, fit:{t:'hoodie', c:'#2f8f8a', lan:1}},
  hayase:   {name:'早瀬', role:'警視庁サイバー犯罪対策課長', sex:'m', skin:'#f1ccae', hair:'#2b3442', hs:'neat', eye:'#4a6a8a', es:'soft', brow:2.2, gl:'rect', fit:{t:'suit', c:'#55606e', shirt:'#f4f7fb', tie:'#31558a'}},
  onodera:  {name:'小野寺', role:'警察庁の捜査官。元は捜査一課の刑事', sex:'m', skin:'#e8bd98', hair:'#5a5550', hs:'neat', eye:'#7a5a3a', es:'soft', sm:1, brow:2.8, wr:1, beard:'stubble', fit:{t:'coat', c:'#b59a72', shirt:'#e9e4d8', tie:'#6b3b34'}},
  onizuka:  {name:'鬼塚', role:'警視庁捜査一課長', sex:'m', skin:'#e2b48e', hair:'#2a2424', hs:'buzz', eye:'#c26a2a', es:'sharp', brow:3, wr:1, fit:{t:'suit', c:'#3b3029', shirt:'#ece7dd', tie:'#7a2a2a', loose:1}, wide:1, jaw:2},
  kanri:    {name:'システム管理者', role:'東都医科大学病院の情報システム部', sex:'m', skin:'#f6d5bc', hair:'#3d4a44', hs:'messy', eye:'#5a8a6a', es:'round', brow:2, gl:'round', fit:{t:'shirt', c:'#dfe7ee', lan:1}},
  furukawa: {name:'古川', role:'科捜研の物理の研究員（錠前、機械）', sex:'m', skin:'#e9c09c', hair:'#4a4d55', hs:'buzz', eye:'#5a6a7a', es:'soft', brow:3, wr:1, fit:{t:'work', c:'#2c5c94', patch:'科捜研'}},
  shiraishi:{name:'白石', role:'警視庁科捜研の所長', sex:'m', skin:'#f0cfb4', hair:'#c9c9c9', hs:'thin', eye:'#6a7a8a', es:'soft', sm:1, brow:2.4, browc:'#b5b5b5', wr:1, gl:'round', fit:{t:'lab', c:'#fbfbf8', shirt:'#c7d6e6', tie:'#5a6b7d'}},
  kiryu:    {name:'桐生', role:'科捜研の法医の研究員（DNA、血液）', sex:'f', skin:'#f8dac4', hair:'#2a2a52', hs:'long', eye:'#7a5ac2', es:'soft', brow:1.8, fit:{t:'lab', c:'#fbfbf8', shirt:'#d7c9e6'}},
  miyashita:{name:'宮下', role:'科捜研の化学の研究員（薬物、毒物）', sex:'m', skin:'#f2cdb0', hair:'#4a3a30', hs:'neat', eye:'#7a6a3a', es:'soft', sm:1, brow:2.4, fit:{t:'lab', c:'#fbfbf8', shirt:'#cfe3d2'}, wide:1},
  sawaguchi:{name:'沢口', role:'警視庁の捜査官。ログの人', sex:'m', skin:'#f4d2b8', hair:'#2a4a52', hs:'messy', eye:'#3a9a9a', es:'soft', brow:2.2, gl:'rect', fit:{t:'shirt', c:'#3f4a5c', lan:1}},
  mendes:   {name:'メンデス', role:'FBIのサイバー捜査官。班の取りまとめ', sex:'m', skin:'#cf9f76', hair:'#2a221e', hs:'slick', eye:'#8a5a2a', es:'soft', sm:1, brow:3, beard:'goatee', fit:{t:'work', c:'#1d2b4a', patch:'FBI', patchc:'#f2c230'}, wide:1},
  rosen:    {name:'ローゼン', role:'FBIの会計担当の捜査官', sex:'f', skin:'#f2d0bb', hair:'#a8683a', hs:'wavy', eye:'#4a9a5a', es:'soft', brow:1.8, gl:'round', fit:{t:'suit', c:'#3d4a44', shirt:'#f3efe8'}, remote:1},
  hori:     {name:'堀', role:'メディコア・ジャパンの保守担当', sex:'m', skin:'#efc8a8', hair:'#4a3a32', hs:'messy', eye:'#7a6a5a', es:'soft', brow:2.4, fit:{t:'work', c:'#6f8596', patch:'MEDICORE', hands:1}},
  kacho:    {name:'保守部の課長', role:'メディコア・ジャパン', sex:'m', skin:'#ebc3a2', hair:'#7f7f84', hs:'thin', eye:'#6a5a4a', es:'soft', brow:2.6, browc:'#77777a', wr:1, fit:{t:'work', c:'#6f8596', patch:'MEDICORE'}, wide:1},
  news:     {name:'テレビ', noart:1}
};
function shade(hex, f){ const n=parseInt(hex.slice(1),16); let r=n>>16,g=(n>>8)&255,b=n&255; const m=v=>Math.max(0,Math.min(255,Math.round(f<1?v*f:v+(255-v)*(f-1)))); return '#'+[m(r),m(g),m(b)].map(v=>v.toString(16).padStart(2,'0')).join(''); }
const HAIR = {
  fresh:{f:'M76 102 C66 60 94 36 124 36 C156 36 174 62 164 102 C161 92 157 84 152 79 C151 87 147 93 142 97 C142 89 138 81 132 76 C126 87 116 95 104 97 C108 91 110 85 108 79 C100 85 92 93 86 97 C86 91 86 85 88 81 C82 87 78 93 76 102 Z', hl:'M92 56 C104 46 128 44 144 52'},
  neat:{f:'M77 100 C68 60 96 38 124 38 C154 38 172 60 163 100 C160 87 154 78 146 73 C130 70 112 73 100 80 C92 85 84 91 77 100 Z', hl:'M96 54 C108 46 132 44 148 54'},
  buzz:{f:'M79 94 C74 60 98 44 122 44 C146 44 166 60 161 94 C158 81 150 72 140 70 L100 70 C90 72 82 81 79 94 Z', hl:'M98 54 C110 48 134 48 144 54'},
  slick:{f:'M79 92 C72 56 98 40 122 40 C148 40 168 56 161 92 C158 76 146 65 122 65 C98 65 82 76 79 92 Z', hl:'M96 52 C112 44 134 44 148 52'},
  messy:{f:'M73 104 C64 62 92 36 122 36 C154 36 176 64 167 104 C163 95 160 89 156 85 C154 91 150 95 146 97 C146 91 144 85 140 81 C134 89 126 93 118 95 C120 89 120 85 118 81 C110 87 100 93 92 95 C92 89 94 85 96 81 C88 85 80 93 73 104 Z', hl:'M90 56 C104 44 132 44 148 54'},
  thin:{f:'M78 106 C70 84 78 64 94 58 C88 72 84 88 84 102 Z M162 106 C170 84 162 64 146 58 C152 72 156 88 156 102 Z M94 58 C106 48 134 48 146 58 C134 54 106 54 94 58 Z', hl:''},
  bob:{b:'M70 136 C58 70 88 36 122 36 C156 36 184 70 170 136 C170 146 160 150 154 142 L156 96 L84 96 L86 142 C80 150 70 146 70 136 Z', f:'M80 100 C76 64 98 44 122 44 C146 44 166 64 160 100 C150 91 140 87 128 87 C112 87 96 89 80 100 Z', hl:'M94 60 C108 50 134 50 148 60'},
  pony:{b:'M158 66 C190 54 204 92 194 134 C190 154 178 164 172 152 C182 130 180 100 162 86 Z M79 96 C74 114 76 134 82 146 C87 132 87 114 87 98 Z M161 96 C166 114 164 134 158 146 C153 132 153 114 153 98 Z', f:'M76 102 C66 60 94 38 124 38 C156 38 174 62 164 102 C161 92 157 84 152 79 C150 88 144 94 138 97 C138 89 134 82 128 78 C120 88 110 95 98 97 C102 91 103 85 102 80 C94 86 86 93 76 102 Z M118 40 C114 26 126 18 136 24 C128 26 124 32 125 40 Z', hl:'M92 56 C104 46 128 44 144 52', tie:[166,74]},
  long:{b:'M70 140 C56 70 88 36 122 36 C156 36 186 70 172 140 L166 204 C150 212 92 212 76 204 Z', f:'M80 102 C76 64 100 44 121 44 C142 44 166 62 160 102 C156 85 144 70 124 61 C104 70 86 85 80 102 Z', hl:'M94 60 C106 50 132 50 148 60'},
  wavy:{b:'M68 150 C54 72 88 36 122 36 C158 36 190 72 174 150 C182 170 172 190 160 186 C164 174 160 164 154 160 L156 96 L84 96 L86 160 C80 164 76 174 80 186 C68 190 58 170 68 150 Z', f:'M80 104 C74 64 98 44 122 44 C146 44 168 62 160 104 C154 88 142 76 130 72 C118 84 98 90 80 104 Z', hl:'M94 60 C108 50 134 50 148 60'},
  shortf:{b:'M72 120 C62 64 92 36 122 36 C154 36 182 64 170 120 C168 128 160 130 156 124 L156 96 L84 96 L84 124 C80 130 72 128 72 120 Z', f:'M78 104 C70 62 96 42 122 42 C150 42 172 62 162 104 C160 94 156 88 152 84 C144 78 136 70 130 62 C120 74 100 82 86 84 C82 90 79 96 78 104 Z', hl:'M94 58 C108 48 134 48 148 58'},
  kohei:{f:'M79 100 C77 90 78 82 82 76 L86 88 C84 92 82 96 79 100 Z M161 100 C163 90 162 82 158 76 L154 88 C156 92 158 96 161 100 Z', cap:1, hl:''}
};
function eyeSVG(id, side, x, c){
  // big anime eyes: tall glossy iris, large highlights, thick upper lash
  const st = {round:[15,-18,11.5], soft:[14.5,-15,10.5], sharp:[14.5,-12.5,9.5], narrow:[13.5,-10,8.5]}[c.es];
  const [w,up,dn] = st, cid = 'cl-'+id+'-'+side, gid = 'ig-'+id+'-'+side, o = side==='l' ? -1 : 1, F = c.sex==='f';
  const shape = `M${-w} 2 C${-w*0.75} ${up} ${w*0.65} ${up} ${w} 0 C${w*0.75} ${dn} ${-w*0.65} ${dn} ${-w} 2Z`;
  const irx = w*0.68, iry = (dn-up)*0.56, icy = up+iry*0.98, ec = c.eye, el = shade(ec, 1.75), ed = shade(ec, .45);
  const wing = F ? `M${o*(w-1)} ${up*0.3} L${o*(w+5)} ${up*0.72} M${o*(w-4)} ${up*0.62} L${o*(w+1.5)} ${up*1.02}` : '';
  return `<g class="eye" transform="translate(${x} 124)"><clipPath id="${cid}"><path d="${shape}"/></clipPath>
   <linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${ed}"/><stop offset=".55" stop-color="${ec}"/><stop offset="1" stop-color="${el}"/></linearGradient>
   <g class="eye-open"><path d="${shape}" fill="#fff"/><g clip-path="url(#${cid})"><g class="iris"><ellipse cy="${icy}" rx="${irx}" ry="${iry}" fill="url(#${gid})" stroke="${ed}" stroke-width="1.2"/><ellipse cy="${icy-iry*0.1}" rx="${irx*0.46}" ry="${iry*0.52}" fill="${shade(ec,.25)}"/><ellipse cy="${icy+iry*0.62}" rx="${irx*0.62}" ry="${iry*0.22}" fill="#fff" opacity=".35"/><ellipse cx="${-irx*0.42}" cy="${icy-iry*0.48}" rx="${irx*0.4}" ry="${iry*0.3}" fill="#fff"/><circle cx="${irx*0.46}" cy="${icy+iry*0.38}" r="${irx*0.2}" fill="#fff"/><circle cx="${irx*0.1}" cy="${icy+iry*0.62}" r="${irx*0.1}" fill="#fff" opacity=".9"/></g><rect x="${-w}" y="${up-1}" width="${2*w}" height="${-up*0.2}" fill="#4a2f5a" opacity=".14"/></g>
   <path d="M${-w-0.8} 2.6 C${-w*0.75} ${up-0.6} ${w*0.65} ${up-0.6} ${w+0.8} 0.4 ${wing}" fill="none" stroke="#3a2630" stroke-width="${F?3.6:3.2}" stroke-linecap="round" stroke-linejoin="round"/></g>
   <path class="eye-shut" d="M${-w} 2 Q0 ${dn*0.8} ${w} 2" fill="none" stroke="#3a2630" stroke-width="3.2" stroke-linecap="round"/>
   <path class="eye-smile" d="M${-w} 4 Q0 ${up*0.72} ${w} 4" fill="none" stroke="#3a2630" stroke-width="3.4" stroke-linecap="round"/></g>`;
}
function outfitSVG(id, c){
  const f = c.fit, col = f.c, dk = shade(col, .78), lt = shade(col, 1.18), W = c.wide ? 1 : 0, F = c.sex==='f';
  const body = F ? 'M48 340 L54 242 C56 218 80 206 101 194 L120 202 L139 194 C160 206 184 218 186 242 L192 340 Z'
                 : W ? 'M26 340 L34 238 C36 210 68 198 98 188 L120 198 L142 188 C172 198 204 210 206 238 L214 340 Z'
                     : 'M36 340 L42 238 C44 212 72 200 99 190 L120 198 L141 190 C168 200 196 212 198 238 L204 340 Z';
  let s = '';
  const lany = n => { let o=''; for(let i=0;i<n;i++){ const dx=i*16; o += `<path d="M${106-i*3} 192 L${112+dx} 276 M${134+i*3} 192 L${128+dx} 276" stroke="${i?'#2a6fb0':'#b8322f'}" stroke-width="3" fill="none"/><rect x="${109+dx}" y="274" width="22" height="30" rx="3" fill="#f7f7f2" stroke="#555" stroke-width="1"/><rect x="${113+dx}" y="279" width="9" height="10" fill="${i?'#2a6fb0':'#3a4a66'}"/><path d="M${113+dx} 294 h14 M${113+dx} 298 h10" stroke="#888" stroke-width="1.4"/>`; } return o; };
  if (f.t==='suit' || f.t==='coat' || f.t==='lab'){
    s += `<path d="${body}" fill="${col}"/>`;
    s += `<path d="M99 190 L120 246 L141 190 L132 183 L120 198 L108 183 Z" fill="${f.shirt}"/>`;
    s += `<path d="M107 183 L120 201 L103 206 Z M133 183 L120 201 L137 206 Z" fill="${shade(f.shirt,.93)}" stroke="${shade(f.shirt,.8)}" stroke-width=".8"/>`;
    if (f.tie) s += `<path d="M115 ${f.loose?206:200} L125 ${f.loose?206:200} L123 ${f.loose?214:208} L128 256 L120 266 L112 256 L117 ${f.loose?214:208} Z" fill="${f.tie}"/><path d="M115 ${f.loose?206:200} L125 ${f.loose?206:200} L123 ${f.loose?214:208} L117 ${f.loose?214:208} Z" fill="${shade(f.tie,.75)}"/>`;
    if (f.bow) s += `<path d="M120 204 L106 196 L106 214 Z M120 204 L134 196 L134 214 Z" fill="${f.bow}"/><circle cx="120" cy="204" r="3.4" fill="${shade(f.bow,.8)}"/>`;
    s += `<path d="M99 190 L82 204 L112 268 L120 246 Z" fill="${lt}"/><path d="M141 190 L158 204 L128 268 L120 246 Z" fill="${lt}"/>`;
    s += `<path d="M99 190 L82 204 L112 268 M141 190 L158 204 L128 268 M120 262 L120 340" stroke="${dk}" stroke-width="1.6" fill="none"/>`;
    s += `<circle cx="120" cy="296" r="2.6" fill="${dk}"/><circle cx="120" cy="322" r="2.6" fill="${dk}"/>`;
    if (f.t==='lab') s += `<path d="M150 276 h26 v30 h-26 Z" fill="none" stroke="#c9c9c2" stroke-width="1.6"/><path d="M156 276 v-9 M162 276 v-11" stroke="#3a62a8" stroke-width="2.4"/><path d="M168 276 v-8" stroke="#b33" stroke-width="2.4"/>`;
    if (f.t==='coat') s += `<path d="M62 232 L80 222 M178 232 L160 222" stroke="${dk}" stroke-width="2"/>`;
    if (f.pin) s += `<circle cx="90" cy="224" r="3.4" fill="#d9b24a"/>`;
    if (f.ear) s += `<path d="M162 118 C170 124 168 140 160 150 C158 160 158 176 150 190" stroke="#ddd" stroke-width="1.6" fill="none" stroke-dasharray="2 2"/>`;
  } else if (f.t==='chef'){
    s += `<path d="${body}" fill="${col}"/><path d="M99 190 L128 250 L120 262 L92 204 Z" fill="${shade(col,.9)}"/><path d="M141 190 L112 250" stroke="${shade(col,.75)}" stroke-width="2"/><path d="M99 190 L128 250" stroke="${shade(col,.75)}" stroke-width="2"/>`;
    s += `<path d="M60 262 L180 262 L190 340 L50 340 Z" fill="#27344f"/><path d="M60 262 L180 262" stroke="#1a2438" stroke-width="3"/><path d="M104 190 L120 208 L136 190" fill="none" stroke="#d8d2c4" stroke-width="5"/>`;
  } else if (f.t==='hoodie'){
    s += `<path d="M74 196 C80 170 160 170 166 196 C160 214 80 214 74 196 Z" fill="${dk}"/><path d="${body}" fill="${col}"/>`;
    s += `<path d="M100 192 L120 222 L140 192 L132 186 L120 198 L108 186 Z" fill="#f7f4ee"/><path d="M100 192 L120 224 L140 192" fill="none" stroke="${dk}" stroke-width="5"/>`;
    s += `<path d="M112 222 L110 262 M128 222 L130 262" stroke="#f3efe6" stroke-width="2.4"/><circle cx="110" cy="264" r="2.6" fill="#f3efe6"/><circle cx="130" cy="264" r="2.6" fill="#f3efe6"/><path d="M84 300 Q120 316 156 300" stroke="${dk}" stroke-width="2" fill="none"/>`;
  } else if (f.t==='shirt'){
    s += `<path d="${body}" fill="${col}"/><path d="M107 184 L120 202 L101 210 Z M133 184 L120 202 L139 210 Z" fill="${lt}" stroke="${dk}" stroke-width="1"/><path d="M120 202 L120 340" stroke="${dk}" stroke-width="1.6"/><circle cx="120" cy="230" r="2" fill="${dk}"/><circle cx="120" cy="262" r="2" fill="${dk}"/><circle cx="120" cy="294" r="2" fill="${dk}"/>`;
  } else if (f.t==='work'){
    s += `<path d="${body}" fill="${col}"/><path d="M100 190 L120 214 L140 190 L132 184 L120 198 L108 184 Z" fill="#e9e6df"/><path d="M106 184 L120 206 L94 214 L92 198 Z M134 184 L120 206 L146 214 L148 198 Z" fill="${lt}" stroke="${dk}" stroke-width="1"/><path d="M120 206 L120 340" stroke="${dk}" stroke-width="2.4"/><rect x="117" y="212" width="6" height="9" rx="1.5" fill="#c9c9c9"/>`;
    s += `<rect x="138" y="234" width="${f.patch.length>4?46:34}" height="15" rx="2" fill="${f.patchc? '#14203a':'#f4f4ee'}" stroke="${dk}" stroke-width="1"/><text x="${138+(f.patch.length>4?23:17)}" y="245.5" font-size="${f.patch.length>4?8:10}" text-anchor="middle" font-weight="700" fill="${f.patchc||'#2a3a4a'}" font-family="sans-serif">${f.patch}</text>`;
  }
  if (f.lan) s += lany(f.lan);
  if (f.hands){
    const sk = c.skin, sd = shade(sk,.85);
    s += `<g class="hands" transform="translate(0 -40)"><path d="M150 300 C140 300 130 306 126 314 L132 330 C140 326 152 322 158 318 Z" fill="${sk}" stroke="${sd}" stroke-width="1"/><rect class="watch" x="140" y="296" width="20" height="9" rx="3" fill="#d9b24a" stroke="#8a6a1a" stroke-width="1"/><circle cx="150" cy="300.5" r="3.2" fill="#fdf6dc" stroke="#8a6a1a" stroke-width=".8"/>
      <g class="hand-r"><path d="M90 300 C100 300 112 306 118 314 L112 330 C104 326 92 322 84 318 Z" fill="${sk}" stroke="${sd}" stroke-width="1"/><path d="M96 312 L112 318 M94 317 L109 323" stroke="${sd}" stroke-width="1"/></g></g>`;
  }
  return s;
}
function charSVG(id){
  const c = CHARS[id]; if (!c || c.noart) return '';
  const sk = c.skin, sd = shade(sk, .88), ol = '#7a4a3c', hc = c.hair, hd = shade(hc, .74), ho = shade(hc, .45), hl = shade(hc, 1.7), H = HAIR[c.hs], F = c.sex==='f', bc = c.browc || shade(hc, .8);
  const face = c.jaw===2 ? 'M72 104 C72 50 168 50 168 104 C168 130 160 150 140 160 C132 164 126 166 120 166 C114 166 108 164 100 160 C80 150 72 130 72 104 Z'
     : 'M73 104 C73 51 167 51 167 104 C167 128 157 146 139 157 C131 162 126 164 120 164 C114 164 109 162 101 157 C83 146 73 128 73 104 Z';
  const HT = 'transform="translate(120 92) scale(1.2 1.22) translate(-120 -92)"';
  let s = `<g transform="translate(0 20)"><g class="ch-body">`;
  if (H.b) s += `<g class="ch-hairb" transform="translate(120 172) scale(1.24) translate(-120 -172)"><path ${HT} d="${H.b}" fill="${hd}" stroke="${ho}" stroke-width="1.4" stroke-linejoin="round"/></g>`;
  s += `<path d="M110 160 L108 196 Q120 204 132 196 L130 160 Z" fill="${sd}"/>`;
  s += `<g transform="translate(120 340) scale(.94 1) translate(-120 -340)">` + outfitSVG(id, c) + `</g>`;
  s += `<g class="ch-head"><g transform="translate(120 172) scale(1.24) translate(-120 -172)">`;
  s += `<ellipse cx="72" cy="123" rx="6" ry="10" fill="${sk}" stroke="${ol}" stroke-width="1.3"/><ellipse cx="168" cy="123" rx="6" ry="10" fill="${sk}" stroke="${ol}" stroke-width="1.3"/>`;
  s += `<path d="${face}" fill="${sk}" stroke="${ol}" stroke-width="1.5" stroke-linejoin="round"/>`;
  s += `<ellipse cx="88" cy="142" rx="10" ry="5.5" fill="#ff8f86" opacity="${c.blush?.5:.26}"/><ellipse cx="152" cy="142" rx="10" ry="5.5" fill="#ff8f86" opacity="${c.blush?.5:.26}"/>`;
  if (c.blush) s += `<path d="M82 140 l3 5 M87 139 l3 5 M146 139 l3 5 M151 140 l3 5" stroke="#f0625a" stroke-width="1.1" stroke-linecap="round" opacity=".6"/>`;
  if (c.beard==='stubble') s += `<path d="M90 148 C96 158 108 163 120 164 C132 163 144 158 150 148 C144 155 134 158 120 158 C106 158 96 155 90 148 Z" fill="${shade(sk,.74)}" opacity=".4"/>`;
  if (c.beard==='goatee') s += `<path d="M111 156 C115 153 125 153 129 156 C129 162 125 165 120 165 C115 165 111 162 111 156 Z" fill="${hc}" opacity=".9"/>`;
  s += eyeSVG(id, 'l', 96, c) + eyeSVG(id, 'r', 144, c);
  const by = {round:100, soft:103, sharp:105.5, narrow:108}[c.es];
  s += `<path class="brow brow-l" d="M82 ${by+2} Q94 ${by-4} 109 ${by+0.5}" stroke="${bc}" stroke-width="${Math.min(c.brow,3)}" stroke-linecap="round" fill="none"/><path class="brow brow-r" d="M158 ${by+2} Q146 ${by-4} 131 ${by+0.5}" stroke="${bc}" stroke-width="${Math.min(c.brow,3)}" stroke-linecap="round" fill="none"/>`;
  s += `<path d="M120.6 139 l-1.2 2.6" stroke="${shade(sk,.66)}" stroke-width="1.7" fill="none" stroke-linecap="round"/>`;
  s += `<g class="mouth" transform="translate(120 151)"><path class="m-shape" d="M-4.5 0 Q0 3.5 4.5 0" stroke="#9a4a44" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/><g class="m-open"><path d="M-6 -2 Q0 -3.6 6 -2 Q5.4 6.4 0 7 Q-5.4 6.4 -6 -2Z" fill="#8a2f34" stroke="#6a2428" stroke-width=".8"/><ellipse cy="4.4" rx="3.2" ry="1.9" fill="#ff9a94"/></g></g>`;
  if (c.gl==='rect') s += `<g fill="rgba(215,238,255,.22)" stroke="#39404e" stroke-width="2.2"><rect x="78" y="108" width="36" height="27" rx="7"/><rect x="126" y="108" width="36" height="27" rx="7"/><path d="M114 119 h12 M78 118 L72 116 M162 118 L168 116" fill="none"/></g><path d="M83 113 l9 -1 M131 113 l9 -1" stroke="#fff" stroke-width="2.4" opacity=".8" stroke-linecap="round"/>`;
  if (c.gl==='round') s += `<g fill="rgba(215,238,255,.2)" stroke="#7a6652" stroke-width="2"><circle cx="96" cy="122" r="18"/><circle cx="144" cy="122" r="18"/><path d="M114 120 h12 M78 120 L72 118 M162 120 L168 118" fill="none"/></g><path d="M85 111 l7 -3 M133 111 l7 -3" stroke="#fff" stroke-width="2.4" opacity=".8" stroke-linecap="round"/>`;
  if (H.f) s += `<g ${HT}><path d="${H.f}" fill="${hc}" stroke="${ho}" stroke-width="1.4" stroke-linejoin="round"/>${H.hl ? `<path d="${H.hl}" stroke="${hl}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".7"/><path d="${H.hl}" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" opacity=".5" transform="translate(0 -1)"/>` : ''}${H.tie ? `<circle cx="${H.tie[0]}" cy="${H.tie[1]}" r="6" fill="#ffcf3a" stroke="#c9962a" stroke-width="1.2"/>` : ''}</g>`;
  if (H.cap) s += `<g ${HT}><path d="M78 80 C76 48 98 36 121 36 C144 36 166 48 164 80 C150 72 92 72 78 80 Z" fill="#fffdf8" stroke="#b8b2a0" stroke-width="1.4"/><path d="M78 80 C92 72 150 72 164 80 L164 70 C150 62 92 62 78 70 Z" fill="#ece7da"/></g>`;
  s += `<g class="fx-sweat"><path d="M178 84 C184 96 186 103 180 107 C174 103 173 96 178 84 Z" fill="#b8e6fc" stroke="#5aa3cc" stroke-width="1.3"/></g>`;
  s += `<g class="fx-anger" transform="translate(172 66)"><path d="M-8 -2.5 L-2.5 -2.5 L-2.5 -8 M2.5 -8 L2.5 -2.5 L8 -2.5 M8 2.5 L2.5 2.5 L2.5 8 M-2.5 8 L-2.5 2.5 L-8 2.5" stroke="#e8382f" stroke-width="3" fill="none" stroke-linecap="round"/></g>`;
  s += `</g></g></g></g>`;
  return s;
}
const MOUTHS = { n:'M-4.5 0 Q0 3.5 4.5 0', s:'M-7 -2 Q0 8 7 -2 Z', a:'M-5.5 2 Q0 -2.5 5.5 2', t:'M-6 1 Q-3 -2 0 1 Q3 4 6 1', u:'M-3 -3 Q0 -5 3 -3 Q4.4 1 3 4 Q0 6 -3 4 Q-4.4 1 -3 -3Z', k:'M-4.5 1 Q0 2 4.5 1', d:'M-5 2 Q0 -1.5 5 2' };
const BROWS = { n:[0,0], s:[-4,-2], a:[14,2.5], t:[-12,-1], u:[-5,-6], k:[8,2], d:[-14,0] };
function applyExpr(g, e){
  if (!g) return; e = MOUTHS[e] ? e : 'n'; g.dataset.e = e;
  const m = g.querySelector('.m-shape'); if (m){ m.setAttribute('d', MOUTHS[e]); m.setAttribute('fill', e==='u' ? '#8a2f34' : e==='s' ? '#c9524e' : 'none'); }
  const c = CHARS[g.dataset.id] || {}; g.classList.toggle('eyes-smile', e==='s' && !!c.sm);
  const [rot, dy] = BROWS[e], bl = g.querySelector('.brow-l'), br = g.querySelector('.brow-r');
  if (bl){ bl.style.transform = `translate(0px,${dy}px) rotate(${rot}deg)`; br.style.transform = `translate(0px,${dy}px) rotate(${-rot}deg)`; }
}
if (typeof module !== 'undefined') module.exports = { CHARS };
