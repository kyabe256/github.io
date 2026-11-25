/* ---------- standard case format: one text file per case (see cases/FORMAT.md) ---------- */
function hsh(s){ let h = 2166136261; for (const c of s){ h ^= c.codePointAt(0); h = Math.imul(h, 16777619) >>> 0; } return h; }
function autoLook(id, name, role, sa, o){
  const sex = sa[0] === 'f' ? 'f' : 'm', age = +sa.slice(1) || 35, h = hsh(id + name), pk = (a, k) => a[(h >>> k) % a.length], F = sex === 'f';
  const skin = o.skin || pk(o.x ? ['#f2d2ba', '#f6d6bc', '#d9a882', '#c68e68', '#8d5a3c', '#eec8a6'] : ['#f6d6bc', '#eec8a6', '#f2d2ba', '#e8c0a0', '#f9dcc6'], 3);
  const hair = o.hair || (age >= 62 ? pk(['#c4c4c4', '#9a9da2', '#e2e2e2'], 5) : age >= 52 ? pk(['#5a5a60', '#3a3a40', '#6a6a70', '#2a2a30'], 5) : pk(o.x ? ['#b89a5a', '#8a5a2a', '#2a1e1a', '#a8442a', '#4a3a30', '#d9c08a'] : ['#23262e', '#2a1e1a', '#3a2a22', '#4a3a30', '#27324f'], 5));
  const hs = o.hs || (F ? pk(age >= 50 ? ['bob', 'shortf', 'wavy'] : ['bob', 'pony', 'long', 'wavy', 'shortf'], 7) : age >= 60 ? pk(['thin', 'slick', 'neat'], 7) : pk(['fresh', 'neat', 'buzz', 'slick', 'messy', 'neat'], 7));
  const ft = o.fit || 'suit', cols = { suit: ['#3a4458', '#2a3350', '#3a3d44', '#55606e', '#26282e', '#4a3a44', '#5a6a7a'], coat: ['#b89a6a', '#6a7a9a', '#5a5a66', '#8a6a5a'], lab: ['#f4f7fb'], chef: ['#f3f0e8'], hoodie: ['#2f8f8a', '#5a5a8a', '#8a4a4a', '#4a6a4a', '#3a3f4c'], shirt: ['#dfe8f4', '#f4e6d8', '#d8ecd8', '#e8d8ec'], work: ['#5a7a5a', '#3a5a8a', '#8a6a3a', '#5a6470'] }[ft] || ['#3a4458'];
  const c = { name, role, sex, age, skin, hair, hs, eye: o.eye || pk(['#5a6a5a', '#7a5a3a', '#4a6a8a', '#6a4a34', '#5a5a66', '#8a5a2a'].concat(o.x ? ['#4a8ac2', '#3a8a6a'] : []), 9), es: o.es || pk(F ? ['round', 'soft', 'soft', 'cool'] : ['soft', 'cool', 'narrow', 'half', 'cool'], 11),
    tilt: ((h >>> 13) % 11) - 5, jaw: F ? 0 : (h >>> 15) % 3, brow: F ? 1.8 + ((h >>> 17) % 4) / 10 : 2.3 + ((h >>> 17) % 8) / 10, pose: o.pose || pk(['stand', 'cross', 'pocket', 'chin', 'hands', 'stand'], 19),
    fit: { t: ft, c: o.fc || pk(cols, 21), shirt: '#f4f7fb' } };
  if (ft === 'work') c.fit.patch = o.patch || name.slice(0, 2); else if (ft === 'suit' && !F) c.fit.tie = pk(['#7a2a3a', '#3a4a5a', '#3a7a8a', '#4a2a2a', '#2a3a6a', '#6a5a2a'], 23); else if (ft === 'suit') c.fit.bow = (h >>> 23) % 3 ? undefined : '#b23a48';
  const gl = o.gl || ((h >>> 25) % 5 === 0 ? pk(['rect', 'round'], 27) : ''); if (gl && gl !== '0') c.gl = gl;
  if (age >= 55) c.wr = 1; if (F && age < 35) c.blush = 1; if (!F && age >= 30 && (h >>> 29) % 6 === 0) c.beard = 'stubble'; if (age >= 62) c.browc = '#aaaaaa';
  return c;
}
const esc3 = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function docHTML(d){ // d = { kind, head: [...], rows: [{ c: [cells], f, z, note, fine }] }
  const hot = (r, inner, tag = 'b') => r.f ? `<${tag} class="h" data-f="${r.f}"${r.z ? ` data-z="${r.z}"` : ''}>${inner}</${tag}>` : r.note ? `<${tag} class="h" data-t="${esc3(r.note)}">${inner}</${tag}>` : inner;
  const fine = d.rows.filter(r => r.fine).map(r => `<p class="fine${r.z ? ' tiny' : ''}">${hot(r, esc3(r.c[0]))}</p>`).join(''), rows = d.rows.filter(r => !r.fine);
  const h3 = d.head[0] ? `<h3>${esc3(d.head[0])}</h3>` : '', sub = d.head[1] ? `<p class="sub">${esc3(d.head[1])}</p>` : '';
  if (d.kind === 'table'){ const cols = (d.head[2] || '').split(',').filter(Boolean); return `<div class="paper typed">${h3}${sub}<table class="t"><thead><tr>${cols.map(c => `<th>${esc3(c)}</th>`).join('')}</tr></thead><tbody>${rows.map(r => `<tr${r.f ? ` class="h" data-f="${r.f}"${r.z ? ` data-z="${r.z}"` : ''}` : r.note ? ` class="h" data-t="${esc3(r.note)}"` : ''}>${r.c.map(c => `<td>${esc3(c)}</td>`).join('')}</tr>`).join('')}</tbody></table>${fine}</div>`; }
  if (d.kind === 'form') return `<div class="paper">${h3}${sub}<table class="f">${rows.map(r => `<tr><th>${esc3(r.c[0])}</th><td>${hot(r, esc3(r.c.slice(1).join('｜')))}</td></tr>`).join('')}</table>${fine}</div>`;
  if (d.kind === 'memo') return `<div class="paper hand">${rows.map(r => `<p>${hot(r, esc3(r.c.join('　')))}</p>`).join('')}${fine}</div>`;
  if (d.kind === 'text') return `<div class="paper">${h3}${sub}${rows.map(r => `<p>${hot(r, esc3(r.c.join('　')))}</p>`).join('')}${fine}</div>`;
  if (d.kind === 'news') return `<div class="paper news">${h3}${sub}${rows.map(r => `<p>${hot(r, esc3(r.c.join('　')))}</p>`).join('')}</div>`;
  if (d.kind === 'chat') return `<div class="phone"><div class="ph-top"><span>${esc3(d.head[1] || '')}</span><span>圏内</span></div><div class="ph-h">メッセージ　${esc3(d.head[0] || '')}</div>${rows.map(r => r.c[0] === '-' ? `<div class="ph-day">${esc3(r.c[1] || '')}</div>` : `<div class="bub ${r.c[0] === '>' ? 'me' : 'you'}">${hot(r, esc3(r.c[1] || ''))}<i>${esc3(r.c[2] || '')}</i></div>`).join('')}${fine}</div>`;
  if (d.kind === 'graph'){ const vals = rows.map(r => +r.c[1] || 0), mx = Math.max(...vals, 1), n = rows.length, bw = Math.min(70, 620 / n - 8); let b = '';
    rows.forEach((r, i) => { const x = 80 + i * (640 / n), hh = vals[i] / mx * 230, attr = r.f ? ` class="h" data-f="${r.f}"${r.z ? ` data-z="${r.z}"` : ''}` : r.note ? ` class="h" data-t="${esc3(r.note)}"` : ''; b += `<g${attr}><rect x="${x}" y="${330 - hh}" width="${bw}" height="${hh}" fill="${r.c[2] === '!' ? '#c8382f' : '#2456c8'}"/><rect x="${x}" y="90" width="${bw}" height="260" fill="transparent"/><text x="${x + bw / 2}" y="${322 - hh}" font-size="${r.z ? 5 : 11}" text-anchor="middle" fill="#23202a" font-family="monospace">${esc3(r.c[1])}</text></g><text x="${x + bw / 2}" y="350" font-size="11" text-anchor="middle" fill="#23202a" font-family="monospace">${esc3(r.c[0])}</text>`; });
    return `<svg viewBox="0 0 760 420" width="760" height="420"><rect width="760" height="420" fill="#f4efe2"/><text x="40" y="40" font-size="20" font-weight="800" fill="#23202a">${esc3(d.head[0] || '')}</text><text x="40" y="62" font-size="12" fill="#55525e">${esc3(d.head[1] || '')}</text><path d="M70 330 H730 M70 90 V330" stroke="#23202a" stroke-opacity=".4"/>${b}${d.rows.filter(r => r.fine).map((r, i) => `<text x="40" y="${384 + i * 16}" font-size="11" fill="#55525e">${esc3(r.c[0])}</text>`).join('')}</svg>`; }
  if (d.kind === 'cctv'){ const n = Math.max(0, Math.min(3, +(d.head[2] || 1))), man = (x, s) => `<g transform="translate(${x} 150) scale(${s})"><path d="M-70 250 q0 -120 70 -130 q70 10 70 130Z" fill="#30333c" stroke="#111" stroke-width="3"/><circle cx="0" cy="70" r="46" fill="#c9b09a" stroke="#111" stroke-width="3"/><path d="M-48 60 q48 -70 96 0 l14 4 q-62 -30 -124 0Z" fill="#1c1e26" stroke="#111" stroke-width="3"/></g>`;
    const r0 = rows[0] || { c: [''] }, fig = [...Array(n)].map((_, i) => man(380 + (i - (n - 1) / 2) * 190, 1 + i * .04)).join('');
    return `<svg viewBox="0 0 760 480" width="760" height="480"><rect width="760" height="480" fill="#23262c"/><polygon points="120,40 640,40 720,460 40,460" fill="#3a3e46"/><polygon points="200,40 560,40 600,300 160,300" fill="#4a4f58"/>${hot(r0, `<rect x="200" y="150" width="360" height="270" fill="transparent"/>${fig}`, 'g')}${[...Array(40)].map((_, i) => `<path d="M0 ${i * 12} H760" stroke="#000" stroke-opacity=".18"/>`).join('')}<text x="24" y="34" font-size="18" fill="#e9f3ff" font-family="monospace">${esc3(d.head[0] || 'CAM')}　${esc3(d.head[1] || '')}</text>${rows.slice(n ? 1 : 0).map((r, i) => `<text x="24" y="${448 - i * 22}" font-size="15" fill="#e9f3ff" font-family="monospace">${hot(r, esc3(r.c.join(' ')), 'tspan')}</text>`).join('')}</svg>`; }
  return `<div class="paper">${rows.map(r => `<p>${esc3(r.c.join(' '))}</p>`).join('')}</div>`;
}
function parseStd(txt){
  const D = { id: '', title: '', when: '', where: '', lead: '', chars: {}, vox: {}, FACTS: {}, HYPS: {}, EV: {}, LOCS: {}, INTR: {}, REPORT: [], REL: [], story: {}, vidx: null, start: null };
  const lines = txt.split('\n'), kvs = a => { const o = {}; for (const t of a){ const i = t.indexOf('='); if (i > 0) o[t.slice(0, i)] = t.slice(i + 1); } return o; };
  const sp = s => s.split('|').map(x => x.trim()), say = s => { const m = s.match(/^([a-z0-9_]+)(?:\.([a-z]))?: (.+)$/); if (!m) throw new Error('bad line: ' + s); return { who: m[1], e: m[2] || 'n', t: m[3] }; };
  let i = 0, ev = null, doc = null, loc = null, I = null, st = null, miss = 0;
  const endDoc = () => { doc = null; };
  for (; i < lines.length; i++){ const raw = lines[i].replace(/\s+$/, ''); if (!raw.trim() || raw.startsWith('//')) continue; if (raw.startsWith('## ')) break;
    let m; const ln = raw.trim();
    if ((m = raw.match(/^# (\d+)\s+(.+)$/))){ D.id = m[1]; D.title = m[2]; continue; }
    if (raw[0] === '@'){ const s1 = raw.indexOf(' '), cmd = s1 < 0 ? raw : raw.slice(0, s1), rest = s1 < 0 ? '' : raw.slice(s1 + 1).trim(); st = cmd === '@st' ? st : null; if (cmd !== '@ev') { ev = null; doc = null; }
      if (cmd === '@when') D.when = rest; else if (cmd === '@where') D.where = rest; else if (cmd === '@lead') D.lead = rest;
      else if (cmd === '@who'){ const p = rest.split(/\s+/); D.chars[p[0]] = autoLook(p[0], p[1], (p[2] || '').replace(/_/g, ' '), p[3] || 'm40', kvs(p.slice(4))); }
      else if (cmd === '@loc'){ const p = rest.split(/\s+/), o = kvs(p.slice(2)); loc = D.LOCS[p[0]] = { n: p[1].replace(/_/g, '　'), g: '', bg: o.bg, bgm: o.bgm || 'invest', people: [], hs: [] }; if (!D.start) D.start = p[0]; }
      else if (cmd === '@p'){ const [l, r] = rest.split('->').map(x => x.trim()), p = l.split(/\s+/), rr = r.split(/\s+/), o = kvs(rr.slice(1)); let P = loc.people.find(x => x.id === p[0]); if (!P) loc.people.push(P = { id: p[0], tp: [] }); P.tp.push({ l: p.slice(1).join(' '), b: rr[0], need: o.if || null }); }
      else if (cmd === '@h'){ const [l, r] = rest.split('->').map(x => x.trim()); loc.hs.push({ id: r.split(/\s+/)[0], a: l }); }
      else if (cmd === '@ev'){ const p = sp(rest), h = p[0].split(/\s+/); ev = D.EV[h[0]] = { n: h.slice(1).join(' '), k: p[1] || '紙', d: p[2] || '', docs: [], faces: [] }; doc = null; }
      else if (cmd === '@fact'){ const p = sp(rest), h = p[0].split(/\s+/), F = D.FACTS[h[0]] = { t: h.slice(1).join(' '), d: p[1] || '', c: p[2] || '事実' }; if (p[3]){ const tm = p[3].split('-').map(x => { const q = x.split(':'); return +q[0] * 60 + +q[1]; }); F.tm = [tm[0], tm[1] || tm[0]]; } }
      else if (cmd === '@hyp'){ const p = sp(rest), h = p[0].split(/\s+/); D.HYPS[h[0]] = { t: h.slice(1).join(' '), d: p[1] || '', need: p[2].split(',').map(a => a.trim().split('+')), hint: p[3] || '' }; D.story[h[0]] = [{ who: 'tsubasa', e: 'k', t: p[4] || p[1] }]; }
      else if (cmd === '@rel'){ const p = rest.split(/\s+/), o = kvs(p.slice(3)); D.REL.push({ a: p[0], b: p[1], l: p[2].replace(/_/g, ' '), need: o.if || null }); }
      else if (cmd === '@intr'){ const p = rest.split(/\s+/), o = kvs(p.slice(1)); I = D.INTR.A = { foe: p[0], at: o.at, bg: o.bg || null, title: (o.title || '').replace(/_/g, '　'), intro: null, end: 'end', miss: [], open: [], need: [], st: {} }; }
      else if (cmd === '@st'){ const p = rest.split(/\s+/), id = p[0]; let k = 1, after = null; if (p[1] && p[1].startsWith('after=')){ after = p[1].slice(6); k = 2; } const ph = p.slice(k).join(' ').split('/').map(x => x.trim()); st = I.st[id] = { p: id + '_p', ph }; D.story[id] = [{ who: I.foe, e: 'n', t: ph.join('') }]; D.story[id + '_p'] = [];
        if (after){ const a = I.st[after]; (a.opens || (a.opens = [])).push(id); } else I.open.push(id); }
      else if (cmd === '@miss'){ const id = 'miss' + (++miss); D.story[id] = [say(rest)]; I.miss.push(id); }
      else if (cmd === '@rep'){ const [l, sup] = rest.split('^').map(x => x.trim()), p = sp(l), opts = p.slice(2).map((x, n) => ['o' + n, x.replace(/^\*/, '')]); D.REPORT.push({ k: 'r' + D.REPORT.length, q: p[0], sub: p[1] || '', opts, a: 'o' + p.slice(2).findIndex(x => x.startsWith('*')), sup: sup ? sup.split(',').map(x => x.trim()) : [] }); }
      else if (cmd === '@vidx') D.vidx = JSON.parse(rest);
      else throw new Error('bad directive: ' + raw);
      continue; }
    if (st){ const s1 = ln.indexOf(' '), k = ln.slice(0, s1), rest = ln.slice(s1 + 1).trim();
      if (k === 'p') D.story[st.p].push(say(rest));
      else if (k === 'a'){ const p = rest.split(/\s+/); st.ans = p[0].split(',').map(Number); st.ok = p[1].split(','); st.o = Object.keys(I.st).find(x => I.st[x] === st) + '_o'; D.story[st.o] = []; I.need.push(st.o.slice(0, -2)); }
      else if (k === 'n'){ const s2 = rest.indexOf(' '), id = st.p.slice(0, -2) + '_n'; st.near = Object.fromEntries(rest.slice(0, s2).split(',').map(x => [x, id])); D.story[id] = [say(rest.slice(s2 + 1).trim())]; }
      else if (k === 'o') D.story[st.o].push(say(rest));
      else if (k === 'h') st.hint = rest;
      else throw new Error('bad statement line: ' + raw);
      continue; }
    if (ev){ if (ln[0] === '%'){ const s1 = ln.indexOf(' '), kind = (s1 < 0 ? ln : ln.slice(0, s1)).slice(1), rest = s1 < 0 ? '' : ln.slice(s1 + 1); if (kind === 'back'){ ev.fl = rest ? rest.split(',') : ['表', '裏']; doc = null; continue; } doc = { kind, head: sp(rest), rows: [] }; ev.docs.push(doc); continue; }
      if (!doc) throw new Error('row before a % template: ' + raw);
      let r = { c: null }, s = ln; if ((m = s.match(/^\*(\w+)(?:@([\d.]+))?\s+(.*)$/))){ r.f = m[1]; if (m[2]) r.z = +m[2]; s = m[3]; } else if ((m = s.match(/^~(\w*)(?:@([\d.]+))?\s+(.*)$/))){ r.fine = 1; if (m[1]){ r.f = m[1]; r.z = +(m[2] || 1.8); } s = m[3]; } else if ((m = s.match(/^\?(.+?) :: (.*)$/))){ r.note = m[1]; s = m[2]; }
      if (doc.kind === 'chat' && !r.fine){ const mm = s.match(/^([<>-])\s*(.*)$/); if (!mm) throw new Error('chat row: ' + raw); r.c = [mm[1], ...sp(mm[2])]; } else r.c = r.fine ? [s] : sp(s); doc.rows.push(r); continue; }
    throw new Error('stray line: ' + raw);
  }
  for (const e in D.EV){ const E = D.EV[e]; E.faces = E.docs.map(d => () => docHTML(d)); if (E.faces.length > 1 && !E.fl) E.fl = ['1枚目', '2枚目']; }
  const P = parseCase(lines.slice(i).filter(l => !l.startsWith('@vidx ')).join('\n')); Object.assign(D.story, P.story);
  const vx = lines.find(l => l.startsWith('@vidx ')); if (vx) D.vidx = JSON.parse(vx.slice(6));
  if (D.INTR.A){ const I2 = D.INTR.A; if (D.story.intr) I2.intro = 'intr'; if (!I2.bg) I2.bg = D.LOCS[I2.at].bg; const L = D.LOCS[I2.at]; let Pp = L.people.find(x => x.id === I2.foe); if (!Pp) L.people.push(Pp = { id: I2.foe, tp: [] }); Pp.tp.push({ l: '尋問する', intr: 'A' }); }
  return D;
}
if (typeof module !== 'undefined') module.exports = { parseStd, autoLook, docHTML, hsh };
