// node check3.js [ids...] : checks every standard case file: references, obtainability, and that the case can be solved
const fs = require('fs'), path = require('path'), vm = require('vm');
const H = __dirname, V2 = [path.join(H, '..', 'v2'), path.join(H, '..', '..', 'cyber-game', 'src')].find(d => fs.existsSync(path.join(d, 'chars.js')));
const ctx = { console }; vm.createContext(ctx);
const src = [path.join(V2, 'chars.js'), path.join(V2, 'parse.js'), path.join(H, 'scenes3.js'), path.join(H, 'scenes4.js'), path.join(H, 'std.js')].map(f => fs.readFileSync(f, 'utf8').replace(/if \(typeof module[^\n]*\n?/g, '')).join('\n');
vm.runInContext(src + '\nfor (const k in SC3) SC3[k]();\nthis.X = { CHARS, parseCase, parseStd, autoLook, SC3, ANCH };', ctx);
const { CHARS, parseCase, parseStd, autoLook, SC3, ANCH } = ctx.X;
const cast = fs.readFileSync(path.join(H, 'cast3.txt'), 'utf8');
Object.assign(CHARS, parseCase(cast.split('\n').filter(l => l.startsWith('@char')).join('\n')).chars);
for (const l of cast.split('\n')) if (l.startsWith('@who ')){ const p = l.slice(5).trim().split(/\s+/); CHARS[p[0]] = autoLook(p[0], p[1], p[2], p[3], {}); }
const ids = process.argv.slice(2).length ? process.argv.slice(2) : fs.readdirSync(path.join(H, 'cases')).filter(f => /^\d{3}\.txt$/.test(f)).map(f => f.slice(0, 3));
let total = 0, lines = 0;
for (const id of ids){
  let bad = 0; const err = m => { bad++; total++; console.log(`  ${id} ERR ${m}`); };
  let D; try { D = parseStd(fs.readFileSync(path.join(H, 'cases', id + '.txt'), 'utf8')); } catch (e) { console.log(`${id} PARSE ${e.message}`); total++; continue; }
  if (D.id !== id) err('id in file is ' + D.id);
  const who = Object.assign({}, CHARS, D.chars), used = new Set(), S = D.story, own = x => D.EV[x] || D.FACTS[x] || D.HYPS[x];
  const blk = b => { used.add(b); if (!S[b]) err('no block ' + b); };
  ['op', 'end', 'fin', 'bad'].forEach(blk);
  for (const b in S) for (const ln of S[b]){ if (ln.cmd){ const a = ln.a; if (ln.cmd === 'bg' && !SC3[a[0]]) err(`${b}: bg ${a[0]}`); if (ln.cmd === 'get' && !D.EV[a[0]]) err(`${b}: get ${a[0]}`); if (ln.cmd === 'fact' && !D.FACTS[a[0]]) err(`${b}: fact ${a[0]}`); if ((ln.cmd === 'show' || ln.cmd === 'tel') && a[0] !== 'off' && !who[a[0]]) err(`${b}: char ${a[0]}`); if (!['bg', 'bgm', 'sfx', 'card', 'show', 'hide', 'tel', 'get', 'fact', 'flag', 'wait'].includes(ln.cmd)) err(`${b}: cmd ${ln.cmd}`); } else { if (ln.who !== '*'){ lines++; if (!who[ln.who]) err(`${b}: speaker ${ln.who}`); } if (ln.t.length > 96) err(`${b}: line too long (${ln.t.length})`); } }
  for (const l in D.LOCS){ const L = D.LOCS[l]; if (!SC3[L.bg]) { err(`loc ${l} bg ${L.bg}`); continue; } for (const h of L.hs){ if (!(ANCH[L.bg] || {})[h.a]) err(`anchor ${L.bg}.${h.a}`); blk(h.id); } for (const p of L.people){ if (!who[p.id]) err('person ' + p.id); for (const t of p.tp){ if (t.b) blk(t.b); if (t.need && !own(t.need)) err(`topic need ${t.need}`); } } }
  for (const h in D.HYPS){ used.add(h); for (const alt of D.HYPS[h].need) for (const x of alt) if (!D.FACTS[x] && !D.HYPS[x]) err(`hyp ${h} needs ${x}`); }
  const I = D.INTR.A; if (!I) err('no interrogation'); else { if (!D.LOCS[I.at]) err('intr at ' + I.at); if (!who[I.foe]) err('foe ' + I.foe); if (I.miss.length !== 2) err('need 2 @miss'); if (S.intr) used.add('intr'); I.miss.forEach(m => used.add(m)); if (!I.need.length) err('no contradictions');
    for (const s in I.st){ const st = I.st[s]; used.add(s); used.add(st.p); if (!S[st.p].length) err(`${s}: no press line`); if (st.ok){ used.add(st.o); if (!S[st.o].length) err(`${s}: no objection lines`); if (!st.hint) err(`${s}: no hint`); for (const x of st.ok) if (!own(x)) err(`${s} ok ${x}`); for (const n of st.ans) if (!(n >= 0 && n < st.ph.length)) err(`${s} ans ${n}`); for (const x in st.near || {}){ used.add(st.near[x]); if (!own(x)) err(`${s} near ${x}`); } } } }
  if (D.REPORT.length < 2) err('report needs 2+ fields'); for (const R of D.REPORT){ if (R.a === 'o-1') err('report field without *: ' + R.q); if (!R.sup.length) err('report field without support: ' + R.q); for (const x of R.sup) if (!own(x)) err(`report sup ${x}`); }
  for (const e of D.REL){ if (!who[e.a] || !who[e.b]) err(`rel ${e.a} ${e.b}`); if (e.need && !own(e.need)) err('rel need ' + e.need); }
  for (const b in S) if (!used.has(b) && !['x_near', 'x_break'].includes(b)) err('unused block ' + b);
  // solve it: what can a player reach?
  const have = new Set(), evFacts = {}; for (const e in D.EV){ const html = D.EV[e].faces.map(f => f()).join(''); evFacts[e] = [...html.matchAll(/data-f="(\w+)"/g)].map(m => m[1]); for (const f of evFacts[e]) if (!D.FACTS[f]) err(`ev ${e} marks unknown fact ${f}`); }
  const run = b => { for (const ln of S[b] || []) if (ln.cmd === 'get' || ln.cmd === 'fact') have.add(ln.a[0]); }; run('op');
  let grow = true; while (grow){ const n = have.size;
    for (const l in D.LOCS){ for (const h of D.LOCS[l].hs) run(h.id); for (const p of D.LOCS[l].people) for (const t of p.tp) if (t.b && (!t.need || have.has(t.need))) run(t.b); }
    for (const e in D.EV) if (have.has(e)) for (const f of evFacts[e]) have.add(f);
    for (const h in D.HYPS) if (D.HYPS[h].need.some(a => a.every(x => have.has(x)))) have.add(h);
    grow = have.size > n; }
  for (const e in D.EV) if (!have.has(e)) err('evidence cannot be obtained: ' + e);
  for (const f in D.FACTS) if (!have.has(f)) err('fact cannot be obtained: ' + f);
  for (const h in D.HYPS) if (!have.has(h)) err('hypothesis cannot be formed: ' + h);
  if (I){ const open = new Set(I.open), done = new Set(); let g2 = true; while (g2){ g2 = false; for (const s of [...open]){ const st = I.st[s]; if (!st.ok || done.has(s)) continue; if (st.ok.some(x => have.has(x))){ done.add(s); run(st.o); (st.opens || []).forEach(o => open.add(o)); g2 = true; for (const e in D.EV) if (have.has(e)) for (const f of evFacts[e]) have.add(f); for (const h in D.HYPS) if (D.HYPS[h].need.some(a => a.every(x => have.has(x)))) have.add(h); } } }
    for (const s of I.need) if (!done.has(s)) err('interrogation stuck at ' + s); for (const s in I.st) if (!open.has(s)) err('statement never opens: ' + s); }
  for (const R of D.REPORT) if (!R.sup.some(x => have.has(x))) err('no obtainable support for ' + R.q);
  console.log(`${id} ${bad ? bad + ' problems' : 'OK'} | ${D.title} | ev ${Object.keys(D.EV).length} facts ${Object.keys(D.FACTS).length} hyps ${Object.keys(D.HYPS).length} st ${I ? Object.keys(I.st).length : 0} rep ${D.REPORT.length}`);
}
console.log(total ? `${total} problems` : 'ALL OK', '| cases', ids.length, '| voiced lines', lines); process.exit(total ? 1 : 0);
