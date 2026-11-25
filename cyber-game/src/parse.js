/* ---------- case file parser (shared by the game and the build tools) ---------- */
function kv(tokens){ const o = {}; for (const t of tokens){ const i = t.indexOf('='); if (i > 0) o[t.slice(0, i)] = t.slice(i + 1); } return o; }
function parseTarget(s){ // "[!nidan]a [x]b c" -> function of has(); plain "a" -> string
  s = s.trim(); if (!s.includes('[')) return s;
  const parts = s.split(/\s+/).map(p => { const m = p.match(/^\[(!?)([\w:]+)\](\w+)$/); return m ? { neg: !!m[1], c: m[2], b: m[3] } : { b: p }; });
  return has => { for (const p of parts){ if (!p.c) return p.b; const v = has(p.c); if (p.neg ? !v : v) return p.b; } return parts[parts.length - 1].b; };
}
function parseCase(txt){
  const C = { id: '', title: '', meta: {}, end: {}, chars: {}, voices: {}, views: {}, evid: {}, places: {}, battles: {}, flows: {}, timelines: {}, story: {}, targets: [] };
  let blk = null, place = null, loc = null, battle = null, flow = null, tl = null;
  const tgt = s => { const t = parseTarget(s); C.targets.push(s); return t; };
  for (const raw of txt.split('\n')){
    const ln = raw.replace(/\s+$/, ''); if (!ln.trim() || ln.startsWith('//')) continue;
    let m;
    if ((m = ln.match(/^# FILE (\d+)\s+(.+)$/))){ C.id = m[1]; C.title = m[2]; continue; }
    if ((m = ln.match(/^## (\w+)/))){ blk = C.story[m[1]] = []; flow = tl = null; continue; }
    if (blk){
      if (ln[0] === '@'){ const p = ln.slice(1).split(' '); blk.push({ cmd: p[0], a: p.slice(1) }); continue; }
      if ((m = ln.match(/^\*: (.+)$/))){ blk.push({ who: '*', t: m[1] }); continue; }
      if ((m = ln.match(/^([a-z0-9_]+)(?:\.([a-z]))?: (.+)$/))){ blk.push({ who: m[1], e: m[2] || 'n', t: m[3] }); continue; }
      throw new Error('bad story line: ' + ln);
    }
    if (flow && /^\s/.test(raw)){ const s = ln.trim(), sp = s.indexOf(' '), op = sp < 0 ? s : s.slice(0, sp), rest = sp < 0 ? '' : s.slice(sp + 1);
      if (op === 'ask'){ const ps = rest.split('|').map(x => x.trim()); flow.push({ op, msg: ps[0], opts: ps.slice(1).map(x => { const [l, b] = x.split('->').map(y => y.trim()); return { l, b, angry: l.startsWith('!') }; }).map(o => ({ l: o.l.replace(/^!/, ''), b: o.b, angry: o.angry })) }); }
      else if (op === 'banner'){ const ps = rest.split('|').map(x => x.trim()); flow.push({ op, a: ps[0], b: ps[1] }); }
      else flow.push({ op, a: rest.trim() });
      continue; }
    if (tl && /^\s/.test(raw)){ const s = ln.trim(), ps = s.slice(s.indexOf(' ') + 1).split('|').map(x => x.trim());
      if (s.startsWith('ev ')) tl.events.push(ps); else if (s.startsWith('q ')) tl.qs.push({ m: ps[0], o: ps.slice(1).map(x => x.replace(/^\*/, '')), a: ps.slice(1).findIndex(x => x.startsWith('*')) }); else if (s.startsWith('hit ')) tl.hit = ps; continue; }
    flow = tl = null;
    const sp = ln.indexOf(' '), cmd = sp < 0 ? ln : ln.slice(0, sp), rest = sp < 0 ? '' : ln.slice(sp + 1);
    if (cmd === '@meta'){ Object.assign(C.meta, kv(rest.split(' '))); }
    else if (cmd === '@intro'){ C.meta.intro = rest; }
    else if (cmd === '@next'){ C.meta.next = rest; }
    else if (cmd === '@end'){ C.end[rest[0]] = rest.slice(2); }
    else if (cmd === '@char'){ const ps = rest.split(' '), o = kv(ps.slice(1)), c = { name: o.name, role: (o.role || '').replace(/_/g, ' '), sex: o.sex || 'm', skin: o.skin || '#f4d2b8', hair: o.hair || '#2a2a30', hs: o.hs || 'neat', eye: o.eye || '#5a6a7a', es: o.es || 'soft', tilt: +(o.tilt || 0), jaw: +(o.jaw || 1), brow: +(o.brow || 2.4), pose: o.pose || 'stand' };
      for (const k of ['gl', 'beard', 'browc']) if (o[k]) c[k] = o[k]; for (const k of ['wr', 'wide', 'blush', 'sm', 'remote', 'noart']) if (o[k]) c[k] = 1;
      if (o.hsz) c.hsz = o.hsz.split(',').map(Number);
      const ft = (o.fit || 'suit:#3a4458:#f4f7fb').split(':'); c.fit = { t: ft[0], c: ft[1], shirt: ft[2] || '#f4f7fb' }; if (ft[3]) c.fit[ft[0] === 'work' ? 'patch' : 'tie'] = ft[3]; if (o.lan) c.fit.lan = +o.lan; if (o.bow) c.fit.bow = o.bow; if (o.patchc) c.fit.patchc = o.patchc; if (o.pin) c.fit.pin = 1;
      C.chars[ps[0]] = c; if (o.v) C.voices[ps[0]] = o.v; }
    else if (cmd === '@voice'){ const ps = rest.split(' '); C.voices[ps[0]] = ps[1]; }
    else if (cmd === '@view'){ const ps = rest.split(' '); const [n, d] = ps.slice(1).join(' ').split('|').map(x => x.trim()); C.views[ps[0]] = { n, d }; }
    else if (cmd === '@ev'){ const ps = rest.split(' '); const [n, k, d] = ps.slice(1).join(' ').split('|').map(x => x.trim()); C.evid[ps[0]] = { n, k, d }; }
    else if (cmd === '@place'){ const ps = rest.split(' '), o = kv(ps.slice(1)); place = C.places[ps[0]] = { start: o.start, need: (o.need || '').split(',').filter(Boolean), simple: !!o.simple, locs: {} }; }
    else if (cmd === '@loc'){ const ps = rest.split(' '), o = kv(ps.slice(2)); loc = place.locs[ps[0]] = { n: ps[1].replace(/_/g, '　'), bg: o.bg, people: (o.people || '').split(',').filter(Boolean), hs: [], talk: [], objs: {}, cond: o.cond || null, enter: o.enter ? o.enter.split(':') : null }; if (o.objs) for (const x of o.objs.split(',')){ const [a, b] = x.split(':'); loc.objs[a] = b; } }
    else if (cmd === '@hs'){ const [l, r] = rest.split('->'), ps = l.trim().split(' '), rr = r.trim().split(' | '), o = kv((rr[1] || '').split(' ')); loc.hs.push({ id: ps[0], v: ps[1], r: ps[2].split(',').map(Number), l: ps.slice(3).join(' '), b: tgt(rr[0]), f: o.f || null, done: o.done || null }); }
    else if (cmd === '@talk'){ const [l, r] = rest.split('->'), ps = l.trim().split(' '), rr = r.trim().split(' | '), o = kv((rr[1] || '').split(' ')); let T = loc.talk.find(t => t.who === ps[0] && t.v === ps[1]); if (!T) loc.talk.push(T = { who: ps[0], v: ps[1], tp: [] }); T.tp.push({ l: ps.slice(2).join(' '), b: tgt(rr[0]), f: o.f || null, cond: o.cond || null, rep: o.rep ? 1 : 0 }); }
    else if (cmd === '@battle'){ const ps = rest.split(' '), o = kv(ps.slice(1)); battle = C.battles[ps[0]] = { foe: o.foe, title: (o.title || '').replace(/_/g, ' '), bg: o.bg, miss: (o.miss || '').split(','), end: o.end, pos: o.pos || 'center', ph: [] }; }
    else if (cmd === '@ph'){ const ps = rest.split('|').map(x => x.trim()), h = ps[0].split(' '), ph = { c: h[0], t: h[1], a: h[2], ok: h[3], h: ps[1] };
      if (ph.t === 'ded'){ ph.a = +ph.a; ph.o = ps.slice(2); } if (ph.t === 'obs') ph.z = ps.slice(2).map(z => { const [id, l, r] = z.split(':'); return { id, l, r: r.split(',').map(Number) }; }); battle.ph.push(ph); }
    else if (cmd === '@flow'){ flow = C.flows[rest.trim()] = []; }
    else if (cmd === '@timeline'){ const ps = rest.split(' '), o = kv(ps.slice(1)); tl = C.timelines[ps[0]] = { events: [], qs: [], wrong: o.wrong, title: (o.title || 'あの夜の時刻表').replace(/_/g, ' ') }; }
    else throw new Error('bad line: ' + ln);
  }
  return C;
}
if (typeof module !== 'undefined') module.exports = { parseCase, parseTarget };
