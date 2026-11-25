// validate case files against the engine's data: node check.js
const fs = require('fs'), path = require('path'), vm = require('vm');
const H = __dirname, R = p => fs.readFileSync(path.join(H, p), 'utf8');
const ctx = { console, module: {} }; vm.createContext(ctx);
vm.runInContext(R('chars.js') + '\n' + R('scenes.js') + '\n' + R('parse.js') + '\nthis.CHARS = CHARS; this.SCENES = SCENES; this.parseCase = parseCase;', ctx);
const cast = ctx.parseCase(R('cast.txt')); Object.assign(ctx.CHARS, cast.chars); let errs = 0; const E = (id, m) => { errs++; console.log('  ! ' + id + ': ' + m); };
for (const f of fs.readdirSync(path.join(H, 'cases')).filter(x => x.endsWith('.txt')).sort()){
  const C = ctx.parseCase(R('cases/' + f)), id = C.id, chars = Object.assign({}, ctx.CHARS, C.chars), views = Object.keys(C.views).length ? C.views : cast.views, B = b => { if (!C.story[b]) E(id, 'no block ' + b); };
  for (const t of C.targets) for (const p of t.trim().split(/\s+/)) B(p.replace(/^\[!?[\w:]+\]/, ''));
  let voiced = 0; const gets = new Set(), flagsSet = new Set();
  for (const [bid, blk] of Object.entries(C.story)) for (const it of blk){
    if (it.who && it.who !== '*'){ voiced++; if (!chars[it.who]) E(id, bid + ' unknown speaker ' + it.who); }
    if (it.cmd === 'get'){ gets.add(it.a[0]); if (!C.evid[it.a[0]]) E(id, bid + ' unknown evidence ' + it.a[0]); }
    if (it.cmd === 'flag') flagsSet.add(it.a[0]);
    if (it.cmd === 'bg' && !ctx.SCENES[it.a[0]]) E(id, bid + ' unknown scene ' + it.a[0]);
    if ((it.cmd === 'show') && !chars[it.a[0]]) E(id, bid + ' show unknown ' + it.a[0]);
    if (it.cmd && !['bg', 'bgm', 'sfx', 'card', 'show', 'hide', 'tel', 'get', 'flag', 'wait', 'obj'].includes(it.cmd)) E(id, bid + ' unknown command ' + it.cmd);
  }
  for (const h of (C.meta.have || '').split(',').filter(Boolean)) gets.add(h);
  for (const [pk, P] of Object.entries(C.places)){ if (!P.locs[P.start]) E(id, pk + ' bad start'); for (const [lk, L] of Object.entries(P.locs)){ if (!ctx.SCENES[L.bg]) E(id, lk + ' unknown scene ' + L.bg); for (const p of L.people) if (!chars[p]) E(id, lk + ' unknown person ' + p);
      for (const h of L.hs){ if (h.v !== 'any' && !views[h.v]) E(id, lk + ' bad view ' + h.v); if (h.f) flagsSet.add(h.f); if (h.r.length !== 4 || h.r.some(isNaN)) E(id, lk + ' bad rect ' + h.id); }
      for (const T of L.talk){ if (!chars[T.who]) E(id, lk + ' unknown talker ' + T.who); if (T.v !== 'any' && !views[T.v]) E(id, lk + ' bad view ' + T.v); for (const t of T.tp) if (t.f) flagsSet.add(t.f); }
      if (L.enter){ flagsSet.add(L.enter[0]); if (!C.flows[L.enter[1]]) E(id, lk + ' no flow ' + L.enter[1]); } }
    for (const n of P.need){ if (n.startsWith('f:')){ if (!flagsSet.has(n.slice(2))) E(id, pk + ' need flag never set: ' + n); } else if (!gets.has(n)) E(id, pk + ' need never given: ' + n); } }
  for (const [bk, Bt] of Object.entries(C.battles)){ if (!chars[Bt.foe]) E(id, bk + ' unknown foe'); if (!ctx.SCENES[Bt.bg]) E(id, bk + ' unknown scene ' + Bt.bg); Bt.miss.forEach(B); B(Bt.end);
    for (const ph of Bt.ph){ B(ph.c); B(ph.ok); if (!ph.h) E(id, bk + ' no hint'); if (ph.t === 'ev' && !gets.has(ph.a)) E(id, bk + ' evidence never given ' + ph.a); if (ph.t === 'view' && !views[ph.a]) E(id, bk + ' bad view ' + ph.a); if (ph.t === 'ded' && !(ph.a >= 0 && ph.a < ph.o.length)) E(id, bk + ' bad ded'); if (ph.t === 'obs' && !ph.z.some(z => z.id === ph.a)) E(id, bk + ' bad obs');
      const cl = (C.story[ph.c] || []).filter(x => x.who && x.who !== '*'); if (!cl.length) E(id, bk + ' claim has no line ' + ph.c); } }
  for (const [fk, F] of Object.entries(C.flows)) for (const s of F){ if (s.op === 'play') B(s.a); else if (s.op === 'inv'){ if (!C.places[s.a]) E(id, 'no place ' + s.a); } else if (s.op === 'battle'){ if (!C.battles[s.a]) E(id, 'no battle ' + s.a); } else if (s.op === 'bg'){ if (!ctx.SCENES[s.a]) E(id, 'flow unknown scene ' + s.a); } else if (s.op === 'timeline'){ if (!C.timelines[s.a]) E(id, 'no timeline ' + s.a); else B(C.timelines[s.a].wrong); } else if (s.op === 'ask'){ for (const o of s.opts) if (o.b) B(o.b); } else if (s.op === 'flowx'){ if (!C.flows[s.a]) E(id, 'no flow ' + s.a); } else if (!['cp', 'banner'].includes(s.op)) E(id, 'bad flow op ' + s.op); }
  if (!C.flows.main) E(id, 'no main flow');
  const used = new Set(); const walk = b => { if (typeof b === 'string') used.add(b); }; for (const t of C.targets) for (const p of t.trim().split(/\s+/)) used.add(p.replace(/^\[!?[\w:]+\]/, ''));
  for (const F of Object.values(C.flows)) for (const s of F){ if (s.op === 'play') used.add(s.a); if (s.op === 'ask') s.opts.forEach(o => used.add(o.b)); }
  for (const Bt of Object.values(C.battles)){ Bt.miss.forEach(x => used.add(x)); used.add(Bt.end); Bt.ph.forEach(p => { used.add(p.c); used.add(p.ok); }); } for (const T of Object.values(C.timelines)) used.add(T.wrong);
  const unused = Object.keys(C.story).filter(b => !used.has(b)); if (unused.length) E(id, 'unused blocks ' + unused.join(','));
  console.log('FILE ' + id + ' ' + C.title + ': blocks ' + Object.keys(C.story).length + ', voiced lines ' + voiced + ', evidence ' + Object.keys(C.evid).length);
}
console.log(errs ? 'ERRORS ' + errs : 'all ok'); process.exit(errs ? 1 : 0);
