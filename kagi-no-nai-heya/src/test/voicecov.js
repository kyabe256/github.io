// node test3/voicecov.js : every spoken line of every built case must have a voice entry, and entries must fit inside the mp3
const fs = require('fs'), path = require('path');
const vm = require('vm'), H = path.join(__dirname, '..', 'v3'), V2 = path.join(__dirname, '..', 'v2');
const ctx = { console }; vm.createContext(ctx);
vm.runInContext([path.join(V2, 'chars.js'), path.join(V2, 'parse.js'), path.join(H, 'std.js')].map(f => fs.readFileSync(f, 'utf8').replace(/if \(typeof module[^\n]*\n?/g, '')).join('\n') + '\nthis.X = { parseStd };', ctx);
const { parseStd } = ctx.X;
const fnv = s => { let h = 0x811c9dc5; for (const x of Buffer.from(s, 'utf8')){ h ^= x; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, '0'); };
const dir = path.join(__dirname, '..', 'dist3'); let cases = 0, lines = 0, miss = 0, over = 0;
for (const f of fs.readdirSync(path.join(dir, 'c')).sort()){
  const id = f.slice(0, 3), D = parseStd(fs.readFileSync(path.join(dir, 'c', f), 'utf8')); cases++;
  if (!D.vidx){ console.log(id, 'no index'); miss++; continue; }
  const size = fs.statSync(path.join(dir, 'v', id + '.mp3')).size; let m = 0;
  for (const b in D.story) for (const ln of D.story[b]){ if (!ln.t || !ln.who || ln.who === '*' || /^[…。、！？\s]*$/.test(ln.t)) continue; lines++; const e = D.vidx[fnv(ln.who + '|' + ln.t)]; if (!e){ m++; if (m <= 2) console.log(id, 'no voice:', ln.who, ln.t.slice(0, 30)); } else { const a = Array.isArray(e) ? e : [e.o, e.n]; if (a[0] + a[1] > size) over++; } }
  miss += m;
}
console.log('cases', cases, 'spoken lines', lines, 'without voice', miss, 'outside file', over);
