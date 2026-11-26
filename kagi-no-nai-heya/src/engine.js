/* ---------- engine: stage, dialogue, investigation, inspector, board, interrogation, report ---------- */
const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
const sleep = ms => new Promise(r => setTimeout(r, FAST ? Math.min(ms, 20) : ms));
const castChars = t => { const o = parseCase(t.split('\n').filter(l => l.startsWith('@char')).join('\n')).chars; for (const l of t.split('\n')) if (l.startsWith('@who ')){ const p = l.slice(5).trim().split(/\s+/), kv = {}; for (const x of p.slice(4)){ const i = x.indexOf('='); if (i > 0) kv[x.slice(0, i)] = x.slice(i + 1); } o[p[0]] = autoLook(p[0], p[1], (p[2] || '').replace(/_/g, ' '), p[3] || 'm40', kv); } return o; };
const BASECHARS = Object.assign({}, CHARS, castChars(CAST_TXT)); Object.assign(CHARS, BASECHARS);
let CASE = null, FACTS = {}, HYPS = {}, EV = {}, LOCS = {}, INTR = {}, REPORT = [], REL = null, LANES = [], MAPPOS = {}, DAYS = [''], META = null, CID = null, _fo = {};
const X011 = () => !!META && META.flow === 'x011';
const CATC0 = { '現場': '#c9824a', '錠': '#4f8dff', '通信': '#3fb7a6', '映像': '#9a7be0', 'コール': '#5aa0ff', '三枝': '#d5a53a', '真柴': '#d96a8a', '大使館': '#5fae6a', '人': '#aab2c2', '仮説': '#e3b54a', '物': '#c9824a', '記録': '#4f8dff', '金': '#d5a53a', '時刻': '#9a7be0', '話': '#3fb7a6' };
const PALC = ['#c9824a', '#4f8dff', '#3fb7a6', '#9a7be0', '#d5a53a', '#d96a8a', '#5fae6a', '#aab2c2'], catc = c => CATC0[c] || PALC[hsh(String(c)) % PALC.length];
const AFF = { tsubasa: '#e3b54a', yuki: '#e3b54a', onizuka: '#e3b54a', kujo: '#e3b54a', saegusa: '#e3b54a', mashiba: '#d96a8a', chihaya: '#e3b54a', furukawa: '#58c98a', kiryu: '#58c98a', sawaguchi: '#e3b54a', cole: '#5a9bff', laila: '#c9824a', kanrinin: '#97a0b4' };
const RIM = { soukan: ['#ffcf9a66', -5], genkan: ['#ffe6b855', 4], living: ['#fff0c866', -4], bath: ['#d8f6ff66', -4], hall: ['#e8ffe055', 4], kanri: ['#ffe6a855', 4], fbi: ['#9fc4ff77', 5], keibi: ['#e8eef666', -5], kasouken: ['#c8fff066', 4], cyber: ['#6ad0ff88', -5], renraku: ['#ffc89a66', -5] };
for (const k in SC3) SC3[k](); // fills ANCH
const OPT = 'kagi-no-nai-heya-opt', METAK = 'kagi-meta', saveKey = id => id === '011' ? 'kagi-no-nai-heya-1' : 'kagi-c-' + id;
const stage = $('#stage'), world = $('#world'), bg = $('#bg'), cast = $('#cast'), dlg = $('#dlg'), hud = $('#hud'), bar = $('#bar');
let G = null, mode = 'title', busy = false, FAST = false, talkId = null, typingNow = false, telWho = null, curBg = null, zone = null, LOG = [];
let O = { speed: 26, voice: 1, bgm: .4, se: .7, auto: 0, q: 'auto', hint: 0 }, lite = false;
try { Object.assign(O, JSON.parse(localStorage.getItem(OPT) || '{}')); } catch (e) {}
const saveOpt = () => { try { localStorage.setItem(OPT, JSON.stringify(O)); } catch (e) {} };
const newG = () => ({ v: 1, id: CID, day: 1, loc: META.start, ev: [], evNew: {}, facts: [], hyp: [], links: [], pos: {}, seen: {}, tk: {}, flags: {}, notes: {}, intr: Object.fromEntries(Object.keys(INTR).map(k => [k, { open: [], done: [], g: 5, clear: 0, n: 0 }])), miss: 0, brk: 0, hints: 0, wrongRep: 0, rep: {}, sup: {}, hintOn: O.hint | 0, phase: 'op', score: null });
/* saves: this browser (localStorage) and, when the page runs inside claude.ai for a signed-in viewer, that viewer's private store */
const LS = { get(k){ try { return JSON.parse(localStorage.getItem(k) || 'null'); } catch (e) { return null; } }, set(k, v){ try { localStorage.setItem(k, typeof v === 'string' ? v : JSON.stringify(v)); return true; } catch (e) { return false; } } };
const Cloud = (() => { let db = null, uid = null, st = 'wait'; const pend = {}, tm = {}, run = {};
  const ready = (async () => { try { if (!window.claude || !window.claude.use){ st = 'none'; return false; } const [d, u] = await Promise.all([window.claude.use('db'), window.claude.use('user')]); const id = d && u ? await u.id() : null; if (!id){ st = 'none'; return false; } db = d; uid = id; st = 'ok'; return true; } catch (e) { st = 'none'; return false; } })();
  const ref = k => db.doc('data/users/' + uid + '/' + k);
  async function get(k){ if (!(await ready)) return null; try { const s = await Promise.race([ref(k).get(), new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 7000))]); return s.exists ? s.data() : null; } catch (e) { return null; } }
  async function flush(k){ tm[k] = 0; if (run[k] || !(await ready)) return; const d = pend[k]; if (!d) return; pend[k] = null; run[k] = 1; try { await ref(k).set(d); st = 'ok'; } catch (e) { st = 'err'; } run[k] = 0; if (pend[k] && !tm[k]) tm[k] = setTimeout(() => flush(k), 4000); }
  function put(k, d, now){ pend[k] = d; if (now){ clearTimeout(tm[k]); tm[k] = 0; flush(k); } else if (!tm[k]) tm[k] = setTimeout(() => flush(k), 4000); }
  return { ready, get, put, get state(){ return st; } }; })();
let MET = LS.get(METAK) || { done: {}, saves: {}, last: null, ts: 0 }, lsOK = true, metaAt = 0, flashAt = 0;
const RANKV = { S: 4, A: 3, B: 2, C: 1 };
function mergeMeta(m){ if (!m) return; for (const k in m.done || {}) if (!MET.done[k] || (RANKV[m.done[k].rank] || 0) > (RANKV[MET.done[k].rank] || 0)) MET.done[k] = m.done[k]; for (const k in m.saves || {}) if (!MET.saves[k] || m.saves[k] > MET.saves[k]) MET.saves[k] = m.saves[k]; if ((m.ts || 0) > (MET.ts || 0)) MET.last = m.last || MET.last; }
function saveMeta(now){ MET.ts = Date.now(); metaAt = MET.ts; LS.set(METAK, MET); Cloud.put('meta', { s: JSON.stringify(MET), ts: MET.ts }, now); }
Cloud.ready.then(async ok => { if (!ok) return; const d = await Cloud.get('meta'); if (d && d.s){ try { mergeMeta(JSON.parse(d.s)); LS.set(METAK, MET); } catch (e) {} } if (mode === 'title') showTitle(true); });
function save(now){ if (!G || G.phase === 'op') return; G.ts = Date.now(); const s = JSON.stringify(G); lsOK = LS.set(saveKey(CID), s); Cloud.put('c' + CID, { s, ts: G.ts }, now);
  const fresh = !MET.saves[CID] || MET.last !== CID; MET.saves[CID] = G.ts; MET.last = CID; if (now || fresh || G.ts - metaAt > 60000) saveMeta(now);
  if (now || G.ts - flashAt > 15000){ flashAt = G.ts; const e = $('#saved'); if (e){ e.hidden = false; e.classList.remove('go'); void e.offsetWidth; e.classList.add('go'); } } }
async function loadSave(id){ const a = LS.get(saveKey(id)); let b = null; const d = await Cloud.get('c' + id); if (d && d.s){ try { b = JSON.parse(d.s); } catch (e) {} } const g = a && b ? ((b.ts || 0) > (a.ts || 0) ? b : a) : (a || b); return g && g.v === 1 ? g : null; }
const hasSave = id => !!MET.saves[id] || !!LS.get(saveKey(id));
function recordDone(kind, rank, pts){ const o = MET.done[CID]; if (!o || (RANKV[rank] || 0) >= (RANKV[o.rank] || 0)) MET.done[CID] = { kind, rank, pts }; saveMeta(true); }
const CTXT = {};
async function useCase(id){ let D;
  if (id === '011'){ D = case011(); const P = parseCase(STORY_TXT); D.story = P.story; D.chars = P.chars; D.meta = { id, name: '鍵のない部屋', flow: 'x011', start: 'genkan', intro: ['op_1', 'op_2', 'sc_arrive'], vurl: 'voice-011.mp3', vidx: VIDX, where: '' }; }
  else { if (!CTXT[id]){ const r = await fetch('c/' + id + '.txt'); if (!r.ok) throw new Error('fetch ' + id); CTXT[id] = await r.text(); } const S = parseStd(CTXT[id]); D = { FACTS: S.FACTS, HYPS: S.HYPS, EV: S.EV, LOCS: S.LOCS, INTR: S.INTR, REPORT: S.REPORT, REL: S.REL, LANES: [], MAPPOS: {}, DAYS: ['', S.when], story: S.story, chars: S.chars, meta: { id, name: S.title, flow: 'std', start: S.start, intro: ['op'], vurl: 'v/' + id + '.mp3', vidx: S.vidx || {}, where: S.where } }; if (!D.story.x_near) D.story.x_near = [{ who: '*', t: '物は合っている。だが、突く言葉がちがう。' }]; if (!D.story.x_break) D.story.x_break = [{ who: '*', t: '相手は、口を閉ざした。信頼を失った。……出直すしかない。' }]; }
  for (const k of Object.keys(CHARS)) if (!BASECHARS[k]) delete CHARS[k]; Object.assign(CHARS, D.chars);
  CASE = { story: D.story }; ({ FACTS, HYPS, EV, LOCS, INTR, REPORT, REL, LANES, MAPPOS, DAYS } = D); META = D.meta; CID = id; _fo = {}; }
const tpOK = t => (!t.cond || t.cond(G)) && (!t.need || has(t.need) || !!G.flags[t.need]) && (!t.intr || X011() || !G.intr[t.intr].clear);

const has = id => G.ev.includes(id) || G.facts.includes(id) || G.hyp.includes(id);

/* --- drawing load: 'lite' drops filters and most ambient motion; 'auto' picks it for touch or weak devices and switches to it when frames run slow --- */
function setLite(v){ lite = !!v; stage.classList.toggle('lite', lite); AudioSys.setLite(lite); }
function initQuality(){ const touch = (navigator.maxTouchPoints || 0) > 0 && matchMedia('(pointer:coarse)').matches, weak = (navigator.hardwareConcurrency || 8) <= 4 || (navigator.deviceMemory || 8) < 4, calm = matchMedia('(prefers-reduced-motion:reduce)').matches; setLite(O.q === 'lite' || (O.q !== 'high' && (touch || weak || calm))); }
/* --- fit the stage to the window --- */
function fit(){ const b = $('#fitbox'), s = Math.min(b.clientWidth / 1600, b.clientHeight / 900); stage.style.setProperty('--s', s); stage.style.transform = `translate(-50%,-50%) scale(${s})`; }
addEventListener('resize', fit); fit(); stage.addEventListener('scroll', () => { stage.scrollTop = 0; stage.scrollLeft = 0; });

/* --- characters --- */
function chSVG(id, flip, vb = '0 0 240 330'){ return `<svg viewBox="${vb}" preserveAspectRatio="xMidYMin slice"><g class="ch" data-id="${id}">${charSVG(id, flip)}</g></svg>`; }
function showChar(id, pos){ if (!CHARS[id] || CHARS[id].noart) return; let s = cast.querySelector(`.slot[data-id="${id}"]`);
  if (s){ if (pos && !s.classList.contains('p-' + pos)){ s.className = 'slot p-' + pos; } return s; }
  pos = pos || freePos(id); const old = cast.querySelector('.slot.p-' + pos); if (old) old.remove();
  s = el('div', 'slot p-' + pos, `<div class="slot-in">${chSVG(id, pos === 'right' || pos === 'foe')}</div>`); s.dataset.id = id; cast.appendChild(s);
  stage.classList.add('talk'); return s; }
function freePos(id){ const used = $$('.slot', cast).map(s => s.className.match(/p-(\w+)/)[1]); if (!used.length) return id === 'tsubasa' ? 'left' : 'center'; if (used.includes('foe')) return 'left';
  const order = id === 'tsubasa' ? ['left', 'right', 'center'] : ['right', 'left', 'center']; for (const p of order) if (!used.includes(p)) return p;
  const victim = $$('.slot', cast).find(s => s.dataset.id !== talkId); return victim ? victim.className.match(/p-(\w+)/)[1] : 'center'; }
function hideChar(id){ if (id === 'all'){ cast.innerHTML = ''; } else { const s = cast.querySelector(`.slot[data-id="${id}"]`); if (s) s.remove(); } if (!cast.children.length) stage.classList.remove('talk'); }
function setSpeaker(who, e){
  for (const s of $$('.slot', cast)){ s.classList.toggle('speaking', s.dataset.id === who); s.classList.toggle('dim', who !== '*' && s.dataset.id !== who); }
  if (who === '*') return;
  for (const g of $$(`.ch[data-id="${who}"]`)){ applyExpr(g, e); const si = g.closest('.slot-in'); const a = { u: 'jump', a: 'shake', d: 'droop', t: 'shiver', s: 'hop' }[e]; if (si && a){ si.classList.remove('jump', 'shake', 'droop', 'shiver', 'hop'); void si.offsetWidth; si.classList.add(a); } }
  if (e === 'a'){ stage.classList.remove('shake'); void stage.offsetWidth; stage.classList.add('shake'); }
}
let lastTs = 0, slow = 0, frames = 0, odd = 0;
function tick(ts){
  requestAnimationFrame(tick);
  const dt = ts - lastTs; lastTs = ts;
  if (O.q === 'auto' && !lite && dt < 1000 && mode !== 'title'){ frames++; if (dt > 42) slow++; if (frames >= 150){ if (slow > 45){ setLite(true); toast('<b>動き</b>重いので、軽い表示に切り替えた'); } frames = slow = 0; } }
  odd = (odd + 1) % 3; if (lite && odd) return; // about 20 updates a second in light mode
  const t = ts / 1000, lvl = AudioSys.level(), sp = AudioSys.speaking();
  for (const g of $$('.ch')){
    if (g.closest('[hidden]')) continue;
    const ph = g._ph ?? (g._ph = Math.random() * 6); if (!g._nb) g._nb = t + 1 + Math.random() * 3;
    if (t > g._nb){ g.classList.add('blink'); g._nb = t + 2 + Math.random() * 4; setTimeout(() => g.classList.remove('blink'), 130); }
    const talk = g.dataset.id === talkId; let open = 0;
    if (talk) open = (sp && AudioSys.hasPack) ? lvl : (typingNow || sp ? 0.45 + 0.4 * Math.sin(t * 21 + ph) : 0);
    g.classList.toggle('talk', open > 0.14);
    const mo = g.querySelector('.m-open'); if (mo) mo.style.transform = `scale(${(0.8 + open * 0.3).toFixed(2)},${(0.3 + open * 1.0).toFixed(2)})`;
    const body = g.querySelector('.ch-body'), head = g.querySelector('.ch-head'), hb = g.querySelector('.ch-hairb');
    if (body) body.style.transform = `translateY(${(Math.sin(t * 1.7 + ph) * 1.4).toFixed(2)}px)`;
    const hr = Math.sin(t * 0.8 + ph) * 1.4, hy = Math.sin(t * 1.7 + ph + 0.6) * 0.9 + (talk && open > 0.1 ? Math.sin(t * 10) * 0.9 : 0);
    if (head) head.style.transform = `translateY(${hy.toFixed(2)}px) rotate(${hr.toFixed(2)}deg)`;
    if (hb) hb.style.transform = `translateY(${hy.toFixed(2)}px) rotate(${(hr * 1.6).toFixed(2)}deg)`;
  }
}
requestAnimationFrame(tick);

/* --- camera (animated viewBox keeps the art sharp at any zoom) --- */
let camCur = [800, 450, 1], camRaf = 0, camHold = false;
function applyCam(){ const [x, y, z] = camCur, w = 1600 / z, h = 900 / z, vx = Math.max(0, Math.min(1600 - w, x - w / 2)), vy = Math.max(0, Math.min(900 - h, y - h / 2)); bg.setAttribute('viewBox', `${vx.toFixed(1)} ${vy.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)}`); }
function cam(x, y, z, ms = 700){ cancelAnimationFrame(camRaf); world.classList.toggle('drift', z === 1); if (lite) ms = Math.min(ms, 380); if (FAST || !ms){ camCur = [x, y, z]; applyCam(); return Promise.resolve(); }
  return new Promise(res => { const from = camCur.slice(), to = [x, y, z], t0 = performance.now(); const step = now => { const k = Math.min(1, (now - t0) / ms), e = k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; camCur = from.map((v, i) => v + (to[i] - v) * e); applyCam(); if (k < 1) camRaf = requestAnimationFrame(step); else res(); }; camRaf = requestAnimationFrame(step); }); }
let curFlag = null;
function flagMode(name){ if (name !== 'hearing' && name !== 'oval') return null; if (X011() || !G) return null; const L = (LOCS[G.loc] && LOCS[G.loc].bg === name) ? LOCS[G.loc] : Object.values(LOCS).find(l => l.bg === name); if (!L) return 'none'; if (L.flag) return L.flag;
  const t = L.n, us = /大統領|ホワイトハウス|上院|議会|議員|FBI|CIA|ラングレー|アメリカ|委員長/.test(t), jp = /総理|官邸|官房|警察庁|総監|国会|特捜|警備局/.test(t); if (us && jp) return 'both'; if (us) return 'us'; if (jp) return 'jp';
  if ((L.hs || []).some(h => h.a === 'flag')) return /東京|日本|千葉|霞が関/.test((META && META.where) || '') ? 'jp' : 'us'; return 'none'; }
const bgSame = name => curBg === name && curFlag === flagMode(name);
function setBg(name){ const fm = flagMode(name); if (curBg === name && curFlag === fm) return; curBg = name; curFlag = fm; bg.innerHTML = SC3[name]();
  if (fm){ const g = bg.querySelector('.o-flag'); if (g) g.innerHTML = name === 'hearing' ? (fm === 'none' ? '' : fm === 'both' ? flag3(250, 200, false, 400) + flag3(335, 212, true, 388) : flag3(290, 200, fm === 'jp', 400)) : (fm === 'none' ? '' : fm === 'both' ? flag3(1130, 200, false, 400) + flag3(1220, 220, true, 380) : flag3(1175, 210, fm === 'jp', 390)); } const r = RIM[name] || ['#fff5', -4]; stage.style.setProperty('--rim', r[0]); stage.style.setProperty('--rimx', r[1] + 'px'); camCur = [800, 450, 1]; applyCam(); }
async function fadeTo(fn){ const f = $('#fade'); f.classList.add('on'); await sleep(300); await fn(); await sleep(60); f.classList.remove('on'); await sleep(260); }

/* --- toast, card --- */
function toast(html, bad){ const box = $('#toasts'); while (box.children.length >= 3) box.firstChild.remove(); const t = el('div', 'toast' + (bad ? ' bad' : ''), html); box.appendChild(t); setTimeout(() => t.remove(), 2700); }
async function card(a, b){ const c = el('div', '', `<div><b>${b || a}</b>${b ? `<span>${a}</span>` : ''}<i></i></div>`); c.id = 'card'; stage.appendChild(c); stage.classList.add('cine'); AudioSys.sfx('card'); await sleep(2100); c.remove(); }

/* --- dialogue --- */
let advance = null;
function waitAdvance(){ return new Promise(res => { advance = () => { advance = null; res(); }; }); }
function onAdvance(){ if (advance) advance(); }
dlg.addEventListener('click', e => { if (e.target.closest('.dt')) return; onAdvance(); });
addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && !dlg.hidden && !e.target.closest('button,input')){ e.preventDefault(); onAdvance(); } if (e.key === 'Escape'){ const x = $$('.ov .x').pop(); if (x) x.click(); } });
function dlgTools(){ $('#b-auto').classList.toggle('on', !!O.auto); $('#b-fast').classList.toggle('on', FAST); }
$('#b-auto').onclick = () => { O.auto = O.auto ? 0 : 1; saveOpt(); dlgTools(); if (O.auto) onAdvance(); };
$('#b-fast').onclick = () => { FAST = !FAST; dlgTools(); if (FAST) onAdvance(); };
$('#b-log').onclick = () => openLog();
async function say(who, e, text){
  const nar = who === '*', c = CHARS[who];
  if (!nar && who !== telWho) showChar(who);
  talkId = nar ? null : who; setSpeaker(who, e);
  if (!camHold && !FAST && !lite){ const sl = nar ? null : cast.querySelector(`.slot[data-id="${who}"]`), off = !sl ? 0 : sl.classList.contains('p-left') ? -70 : sl.classList.contains('p-center') ? 0 : 70; cam(800 + off, 440, sl ? 1.06 : 1.02, 900); }
  dlg.hidden = false; dlg.classList.toggle('narr', nar); dlg.classList.remove('wait'); dlg.style.setProperty('--aff', AFF[who] || '#97a0b4');
  $('.nm b', dlg).textContent = nar ? '' : c.name; $('.nm span', dlg).textContent = nar ? '' : (c.role || '');
  const tx = $('.tx', dlg); tx.textContent = ''; LOG.push([nar ? '' : c.name, text]); if (LOG.length > 400) LOG.shift();
  let done = false, dur = 0; const vp = nar ? Promise.resolve(0) : AudioSys.speak(who, text); vp.then(d => { dur = d; });
  typingNow = true; const t0 = performance.now();
  if (FAST){ tx.textContent = text; } else { let i = 0; const skip = waitAdvance().then(() => { done = true; }); while (i < text.length && !done){ i++; tx.textContent = text.slice(0, i); if (i % 3 === 0) AudioSys.sfx('tick'); await Promise.race([sleep(/[、。…！？]/.test(text[i - 1]) ? O.speed * 3 : O.speed), skip]); } tx.textContent = text; advance = null; }
  typingNow = false; dlg.classList.add('wait');
  if (FAST){ await sleep(10); }
  else if (O.auto){ await vp; const left = Math.max(500, dur * 1000 - (performance.now() - t0) + 450, nar ? text.length * 60 : 0); await Promise.race([sleep(left), waitAdvance()]); advance = null; }
  else await waitAdvance();
  AudioSys.stopVoice(); talkId = null;
}
function endDlg(){ dlg.hidden = true; stage.classList.remove('cine'); if (!camHold && camCur[2] !== 1 && camCur[2] < 1.1) cam(800, 450, 1, 500); }
async function play(id){
  const blk = CASE.story[id]; if (!blk) throw new Error('no block ' + id);
  hud.hidden = true; bar.hidden = true;
  for (const ln of blk){
    if (ln.cmd){ const a = ln.a;
      if (ln.cmd === 'bg'){ if (!bgSame(a[0])) await fadeTo(() => { setBg(a[0]); hideChar('all'); }); }
      else if (ln.cmd === 'bgm') AudioSys.bgm(a[0]);
      else if (ln.cmd === 'sfx') AudioSys.sfx(a[0]);
      else if (ln.cmd === 'card'){ dlg.hidden = true; const [x, y] = a.join(' ').split('｜'); await card(x, y); }
      else if (ln.cmd === 'show') showChar(a[0], a[1]);
      else if (ln.cmd === 'hide') hideChar(a[0]);
      else if (ln.cmd === 'tel') setTel(a[0]);
      else if (ln.cmd === 'get') await getEv(a[0]);
      else if (ln.cmd === 'fact') addFact(a[0]);
      else if (ln.cmd === 'flag') G.flags[a[0]] = 1;
      else if (ln.cmd === 'wait') await sleep(+a[0]);
    } else await say(ln.who, ln.e, ln.t);
  }
  setTel('off');
}
function setTel(id){ const old = $('#tel'); if (old) old.remove(); telWho = null; if (id === 'off' || !id) return; telWho = id; AudioSys.sfx('phone');
  const t = el('div', '', chSVG(id, true, '0 0 240 330') + `<div class="tl"><span>${CHARS[id].name}　${CHARS[id].role || ''}</span><i>通話中</i></div>`); t.id = 'tel'; stage.appendChild(t); }
async function getEv(id){ if (G.ev.includes(id)) return; G.ev.push(id); G.evNew[id] = 1; AudioSys.sfx('get'); toast(`<b>証拠</b>${EV[id].n}`); refreshHud(); await sleep(500); }
function addFact(id, quiet){ if (G.facts.includes(id)) return false; G.facts.push(id); if (!quiet){ AudioSys.sfx('correct'); toast(`<b>事実カード</b>${FACTS[id].t}`); } G.flags.brdNew = 1; refreshHud(); return true; }
function choose(title, opts){ return new Promise(res => { const c = el('div', '', title ? `<h4>${title}</h4>` : ''); c.id = 'choice'; opts.forEach((o, i) => { const b = el('button', o.cls || '', o.l); b.style.animationDelay = i * 50 + 'ms'; b.onclick = () => { AudioSys.sfx('select'); c.remove(); res(i); }; c.appendChild(b); }); stage.appendChild(c); }); }

/* --- HUD --- */
function refreshHud(){ if (!G) return; const L = LOCS[G.loc]; $('#place b').textContent = L.n; $('#place span').textContent = (DAYS[G.day] || DAYS[1] || '') + '　' + (L.g || META.where || '');
  $('#t-ev i').textContent = G.ev.length; $('#t-ev').classList.toggle('new', Object.keys(G.evNew).length > 0); $('#t-brd i').textContent = G.facts.length + G.hyp.length; $('#t-brd').classList.toggle('new', !!G.flags.brdNew);
  $('#a-rep').hidden = X011() ? (!G.flags.mid || !!G.flags.repOK) : (!G.flags.rep || !!G.flags.done); $('#a-hint').hidden = !G.hintOn; }
function people(){ const L = LOCS[G.loc]; return (L.people || []).filter(p => (!p.cond || p.cond(G)) && p.tp.some(tpOK)); }
function renderFree(){ refreshHud(); hud.hidden = false; bar.hidden = false; endDlg(); hideChar('all'); $('#intr').hidden = true;
  const box = $('#people'); box.innerHTML = ''; for (const p of people()){ const b = el('button', 'chip', chSVG(p.id, false, '40 30 160 150') + CHARS[p.id].name + `<small>話を聞く</small>`); b.onclick = () => guard(() => talk(p)); box.appendChild(b); }
  $('#zoomout').hidden = !zone; mode = 'free'; }
async function guard(fn){ if (busy) return; busy = true; try { await fn(); } catch (e) { console.error(e); } finally { busy = false; } }
async function enterLoc(id, quick){ G.loc = id; zone = null; camHold = false; const L = LOCS[id]; const go = () => { setBg(L.bg); hideChar('all'); cam(800, 450, 1, 0); }; if (quick) go(); else { AudioSys.sfx('door'); await fadeTo(go); } AudioSys.bgm(L.bgm); renderFree(); save(); }

/* --- scene investigation --- */
function svgPt(e){ const p = bg.createSVGPoint(); p.x = e.clientX; p.y = e.clientY; return p.matrixTransform(bg.getScreenCTM().inverse()); }
const hsRect = (L, h) => h.r || ANCH[L.bg][h.a];
const hz = (h, r) => h.z || Math.max(1.5, Math.min(3.2, Math.min(1600 / (r[2] * 2.4), 900 / (r[3] * 2.4))));
function activeHs(){ const L = LOCS[G.loc]; return L.hs.filter(h => zone ? h.zone === zone : !h.zone); }
world.addEventListener('click', e => { if (mode !== 'free' || busy){ if (!dlg.hidden) onAdvance(); return; } const p = svgPt(e), L = LOCS[G.loc];
  const h = activeHs().find(h => { const r = hsRect(L, h); return p.x >= r[0] && p.x <= r[0] + r[2] && p.y >= r[1] && p.y <= r[1] + r[3]; });
  const sr = stage.getBoundingClientRect(), s = sr.width / 1600, rp = el('div', 'ripple'); rp.style.left = (e.clientX - sr.left) / s + 'px'; rp.style.top = (e.clientY - sr.top) / s + 'px'; stage.appendChild(rp); setTimeout(() => rp.remove(), 520);
  if (!h){ AudioSys.sfx('tick'); return; } guard(() => examine(h)); });
async function examine(h){ const L = LOCS[G.loc], r = hsRect(L, h), cx = r[0] + r[2] / 2, cy = r[1] + r[3] / 2; mode = 'dlg'; AudioSys.sfx('select');
  if (h.desk){ await deskMenu(); return; }
  if (h.enter){ zone = h.enter; hud.hidden = false; camHold = true; await cam(cx, cy, hz(h, r)); G.seen[h.id] = 1; renderFree(); return; }
  hud.hidden = true; bar.hidden = true; $('#zoomout').hidden = true; camHold = true; await cam(cx, cy, hz(h, r)); await play(h.id); camHold = false; G.seen[h.id] = 1; hideChar('all'); endDlg();
  if (zone){ const z = L.hs.find(x => x.enter === zone), zr = hsRect(L, z); await cam(zr[0] + zr[2] / 2, zr[1] + zr[3] / 2, z.z, 500); } else await cam(800, 450, 1, 600);
  await triggers(); renderFree(); save(); }
$('#zoomout').onclick = () => guard(async () => { zone = null; camHold = false; AudioSys.sfx('back'); await cam(800, 450, 1, 600); renderFree(); });
$('#a-hint').onclick = () => { if (mode !== 'free' || busy) return; const L = LOCS[G.loc], left = activeHs().filter(h => !G.seen[h.id] && !h.desk); if (!left.length){ toast('<b>気配</b>ここには、もう何もなさそうだ'); return; } G.hints++; AudioSys.sfx('select');
  for (const h of left){ const r = hsRect(L, h), pt = bg.createSVGPoint(); pt.x = r[0] + r[2] / 2; pt.y = r[1] + r[3] / 2; const q = pt.matrixTransform(bg.getScreenCTM()), sr = stage.getBoundingClientRect(), s = sr.width / 1600, d = Math.max(60, Math.min(r[2], r[3]) * camCur[2]); const g = el('div', 'hintring'); g.style.cssText = `left:${(q.x - sr.left) / s - d / 2}px;top:${(q.y - sr.top) / s - d / 2}px;width:${d}px;height:${d}px`; stage.appendChild(g); setTimeout(() => g.remove(), 2100); } save(); };
async function talk(p){ mode = 'dlg'; hud.hidden = true; bar.hidden = true; showChar(p.id, 'center');
  for (;;){ const tps = p.tp.filter(tpOK); const i = await choose(CHARS[p.id].name + 'に聞く', [...tps.map(t => ({ l: t.l, cls: (t.intr ? 'hot' : G.tk[t.b] ? 'seen' : '') })), { l: 'やめる', cls: 'sub' }]);
    if (i >= tps.length) break; const t = tps[i]; if (t.intr){ hideChar('all'); await interrogate(t.intr); return; } await play(t.b); G.tk[t.b] = 1; endDlg(); hideChar('all'); showChar(p.id, 'center'); save(); if (!people().some(x => x.id === p.id)) break; }
  hideChar('all'); await triggers(); renderFree(); save(); }
async function triggers(){ if (!X011()) return; if (G.intr.A.clear && G.intr.B.clear && !G.flags.mid){ await play('mid'); G.flags.mid = 1; G.day = 3; endDlg(); await enterLoc('soukan', true); } }
async function deskMenu(){ const o = [{ l: '推理ボードを開く' }, { l: '証拠を見直す' }]; if (G.flags.mid && !G.flags.repOK) o.push({ l: '推理レポートを書く', cls: 'hot' }); o.push({ l: 'やめる', cls: 'sub' });
  const i = await choose('総監の机', o); renderFree(); if (o[i].l.startsWith('推理ボード')) openBoard(); else if (o[i].l.startsWith('証拠')) openIns(); else if (o[i].l.startsWith('推理レポート')) openReport(); }

/* --- map --- */
function openMap(){ if (busy || mode !== 'free') return; AudioSys.sfx('select'); const ov = el('div', 'ov'), x11 = X011(); ov.id = 'map';
  ov.innerHTML = `<div class="ov-h"><h2>移動<small>${DAYS[G.day] || DAYS[1] || ''}</small></h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b"><svg class="m" viewBox="0 0 1600 800" preserveAspectRatio="none"><path d="M0 700 Q400 620 700 720 T1600 660 V800 H0Z" fill="#13203c"/>${[...Array(14)].map((_, i) => `<path d="M${i * 120 + 40} 0 V800" stroke="#1b2644" stroke-width="2"/>`).join('')}${[...Array(8)].map((_, i) => `<path d="M0 ${i * 100 + 30} H1600" stroke="#1b2644" stroke-width="2"/>`).join('')}${x11 ? '<path d="M60 300 H640 V660 H60Z" fill="#141c34" stroke="#2f3850" stroke-width="2"/><path d="M900 80 H1540 V480 H900Z" fill="#141c34" stroke="#2f3850" stroke-width="2"/><path d="M700 570 H960 V710 H700Z" fill="#141c34" stroke="#2f3850" stroke-width="2"/><path d="M640 480 Q760 420 900 400 M830 570 Q880 520 960 480" stroke="#e3b54a" stroke-width="3" stroke-dasharray="4 10" fill="none"/>' : '<path d="M200 400 H1400" stroke="#e3b54a" stroke-width="3" stroke-dasharray="4 10" fill="none"/>'}</svg>${x11 ? '<div class="area" style="left:80px;top:310px">港区　現場のマンション</div><div class="area" style="left:920px;top:96px">霞が関　警察庁</div><div class="area" style="left:716px;top:716px">赤坂</div>' : `<div class="area" style="left:80px;top:60px">${META.where || ''}</div>`}</div>`;
  const b = $('.ov-b', ov), ids = Object.keys(LOCS).filter(id => (LOCS[id].day || 1) <= G.day);
  ids.forEach((id, i) => { const L = LOCS[id], [x, y] = x11 ? MAPPOS[id] : [800 + (i - (ids.length - 1) / 2) * Math.min(340, 1200 / ids.length), 400 + (i % 2 ? 70 : -70) * (ids.length > 3 ? 1 : 0)], n = el('button', 'node' + (id === G.loc ? ' here' : ''), L.n.replace('1204号室　', '') + (id === G.loc ? '<small>いま、ここ</small>' : '')); n.style.left = x + 'px'; n.style.top = y + 'px'; n.dataset.loc = id; n.onclick = () => { ov.remove(); if (id !== G.loc) guard(() => enterLoc(id)); }; b.appendChild(n); });
  if (x11 && G.day === 1){ const n = el('button', 'node', '霞が関へ戻る<small>翌朝へ進む。現場には後で戻れる</small>'); n.style.left = '1220px'; n.style.top = '300px'; n.dataset.loc = 'next'; n.onclick = () => { ov.remove(); guard(nextDay); }; b.appendChild(n); }
  $('.x', ov).onclick = () => { AudioSys.sfx('back'); ov.remove(); }; stage.appendChild(ov); }
async function nextDay(){ mode = 'dlg'; await play('leave_d1'); await play('ev2'); G.day = 2; endDlg(); await enterLoc('soukan', true); }

/* --- evidence inspector --- */
let insCur = null;
function openIns(sel){ AudioSys.sfx('select'); const ov = el('div', 'ov'); ov.id = 'ins';
  ov.innerHTML = `<div class="ov-h"><h2>証拠<small>ホイールか＋で拡大。つかんで動かす。裏返す。気づいた所を押す。</small></h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b"><div class="list"></div><div class="view"><div class="sheet"></div><div class="ctl"><button data-z="-1" aria-label="縮小">−</button><button data-z="1" aria-label="拡大">＋</button><button data-z="0" class="w">戻す</button><button class="w" id="flip">裏返す</button></div><div class="zl"></div></div><div class="info"></div></div>`;
  stage.appendChild(ov); const list = $('.list', ov), view = $('.view', ov), sheet = $('.sheet', ov), info = $('.info', ov); let V = { z: 1, x: 0, y: 0, face: 0 }, vidTimer = 0;
  const apply = () => { const vw = view.offsetWidth, vh = view.offsetHeight, f = sheet.firstElementChild, w = (f ? f.offsetWidth : 760) * V.z, h = (f ? f.offsetHeight : 500) * V.z, m = 240;
    if (vw && vh){ const l = vw / 2 + V.x - 380 * V.z, t = 40 + V.y; V.x += Math.max(m - (l + w), 0) - Math.max(l - (vw - m), 0); V.y += Math.max(m - (t + h), 0) - Math.max(t - (vh - m), 0); }
    sheet.style.transform = `translate(${V.x - 380 * V.z}px,${V.y}px) scale(${V.z})`; $('.zl', ov).textContent = '倍率 ' + V.z.toFixed(1); };
  const zoomAt = (nz, px, py) => { nz = Math.max(.6, Math.min(lite ? 2.8 : 3.2, nz)); const r = view.getBoundingClientRect(), s = r.width / view.offsetWidth, cx = px == null ? view.offsetWidth / 2 : (px - r.left) / s, cy = py == null ? view.offsetHeight / 2 : (py - r.top) / s; const ox = cx - view.offsetWidth / 2 - V.x, oy = cy - 40 - V.y; V.x -= ox * (nz / V.z - 1); V.y -= oy * (nz / V.z - 1); V.z = nz; apply(); };
  const renderInfo = () => { const E = EV[insCur], fs = factsOf(insCur).filter(f => G.facts.includes(f)), nt = G.notes[insCur] || []; info.innerHTML = `<h3>${E.n}</h3><p>${E.d}</p><h4>ここから分かった事</h4>` + (fs.length ? fs.map(f => `<div class="fc" style="--c:${catc(FACTS[f].c)}">${FACTS[f].t}</div>`).join('') : '<p>まだ、何もない。</p>') + (nt.length ? '<h4>気づき</h4>' + nt.map(t => `<div class="nt">${t}</div>`).join('') : '') + (G.hintOn ? `<h4>ヒント</h4><p>この証拠に残る事実：あと${factsOf(insCur).filter(f => !G.facts.includes(f)).length}つ</p>` : ''); };
  const markGot = () => { for (const h of $$('.h', sheet)) if (h.dataset.f && G.facts.includes(h.dataset.f)) h.classList.add('got'); };
  const show = id => { insCur = id; delete G.evNew[id]; clearInterval(vidTimer); const E = EV[id]; V = { z: 1, x: 0, y: 0, face: 0 };
    for (const b of $$('.evi', list)){ b.classList.toggle('on', b.dataset.id === id); if (b.dataset.id === id) b.classList.remove('new'); }
    if (E.video){ sheet.innerHTML = videoHTML(); vidTimer = videoInit(sheet); $('#flip', ov).hidden = true; }
    else { sheet.innerHTML = `<div class="flipper"><div class="face">${E.faces[0]()}</div>${E.faces[1] ? `<div class="face back">${E.faces[1]()}</div>` : ''}</div>`; const f = $('#flip', ov); f.hidden = !E.faces[1]; f.textContent = E.fl ? `${E.fl[1]}を見る` : '裏返す'; }
    markGot(); apply(); renderInfo(); refreshHud(); };
  for (const id of G.ev){ const E = EV[id], b = el('button', 'evi' + (G.evNew[id] ? ' new' : ''), `<u>${E.k}</u><span>${E.n}</span>`); b.dataset.id = id; b.onclick = () => { AudioSys.sfx('tick'); show(id); }; list.appendChild(b); }
  $('#flip', ov).onclick = () => { const E = EV[insCur]; V.face = 1 - V.face; $('.flipper', sheet).classList.toggle('b', !!V.face); $('#flip', ov).textContent = E.fl ? `${E.fl[1 - V.face]}を見る` : '裏返す'; AudioSys.sfx('card'); };
  for (const b of $$('.ctl button[data-z]', ov)) b.onclick = () => { const d = +b.dataset.z; if (!d){ V = { z: 1, x: 0, y: 0, face: V.face }; apply(); } else zoomAt(V.z * (d > 0 ? 1.4 : 1 / 1.4)); };
  view.addEventListener('wheel', e => { e.preventDefault(); if (e.shiftKey){ V.y -= e.deltaY; V.x -= e.deltaX; apply(); } else zoomAt(V.z * (e.deltaY < 0 ? 1.12 : 1 / 1.12), e.clientX, e.clientY); }, { passive: false });
  const pts = new Map(); let moved = 0, pinch = 0;
  view.addEventListener('pointerdown', e => { if (e.target.closest('.ctl,input,button')) return; view.setPointerCapture(e.pointerId); pts.set(e.pointerId, [e.clientX, e.clientY]); moved = 0; view.classList.add('drag'); if (pts.size === 2){ const [a, b] = [...pts.values()]; pinch = Math.hypot(a[0] - b[0], a[1] - b[1]); } });
  view.addEventListener('pointermove', e => { const p = pts.get(e.pointerId); if (!p) return; const s = view.getBoundingClientRect().width / view.offsetWidth, dx = (e.clientX - p[0]) / s, dy = (e.clientY - p[1]) / s; pts.set(e.pointerId, [e.clientX, e.clientY]);
    if (pts.size === 2){ const [a, b] = [...pts.values()], d = Math.hypot(a[0] - b[0], a[1] - b[1]); if (pinch) zoomAt(V.z * d / pinch, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2); pinch = d; moved = 99; } else { V.x += dx; V.y += dy; moved += Math.abs(dx) + Math.abs(dy); apply(); } });
  const up = e => { if (!pts.has(e.pointerId)) return; pts.delete(e.pointerId); view.classList.remove('drag'); if (pts.size < 2) pinch = 0; if (moved > 8) return;
    let h = null; for (const t of document.elementsFromPoint(e.clientX, e.clientY)){ const c = t.closest && t.closest('.h'); if (c && sheet.contains(c) && (!c.dataset.cond || videoCond(c.dataset.cond, sheet))){ h = c; break; } } if (!h) return;
    const need = +(h.dataset.z || 0); if (V.z < need - .01){ AudioSys.sfx('back'); toast('字が細かい。拡大しないと読めない', 1); return; }
    if (h.dataset.f){ if (addFact(h.dataset.f)){ markGot(); renderInfo(); save(); } else toast('もう、カードにしてある'); }
    else if (h.dataset.t){ const n = G.notes[insCur] || (G.notes[insCur] = []); if (!n.includes(h.dataset.t)){ n.push(h.dataset.t); AudioSys.sfx('select'); } renderInfo(); toast(h.dataset.t.length > 30 ? h.dataset.t.slice(0, 30) + '…' : h.dataset.t); save(); } };
  view.addEventListener('pointerup', up); view.addEventListener('pointercancel', e => { pts.delete(e.pointerId); view.classList.remove('drag'); });
  $('.x', ov).onclick = () => { clearInterval(vidTimer); AudioSys.sfx('back'); ov.remove(); refreshHud(); save(); };
  window.__ins = { zoom: z => zoomAt(z), show, flip: () => $('#flip', ov).click(), V: () => V, center: h => { const r = h.getBoundingClientRect(), v = view.getBoundingClientRect(), k = v.width / view.offsetWidth; V.x += (v.left + v.width / 2 - (r.left + r.width / 2)) / k; V.y += (v.top + v.height / 2 - (r.top + r.height / 2)) / k; apply(); } };
  if (G.ev.length) show(sel && G.ev.includes(sel) ? sel : (insCur && G.ev.includes(insCur) ? insCur : G.ev[0])); else info.innerHTML = '<p>まだ、何も持っていない。</p>';
}
function factsOf(id){ if (_fo[id]) return _fo[id]; const E = EV[id]; const html = E.video ? videoHTML() : E.faces.map(f => f()).join(''); return _fo[id] = [...new Set([...html.matchAll(/data-f="(\w+)"/g)].map(m => m[1]))]; }
/* the corridor video: the real feed blinks with the failing exit lamp; 2:08-2:30 was swapped for an older clip */
function videoHTML(){ const la = ANCH.hall.lamp;
  const fig = `<g id="vfig" class="h" data-f="f_figure" data-cond="fig"><ellipse cx="1262" cy="852" rx="90" ry="16" fill="#000" opacity=".4"/><path d="M1196 850 q-10 -220 30 -300 q36 -40 76 0 q40 80 30 300Z" fill="#2a2d38" stroke="#111" stroke-width="4"/><circle cx="1264" cy="500" r="44" fill="#d9c0a6" stroke="#111" stroke-width="4"/><path d="M1222 492 q10 -56 60 -50 q36 6 28 50 q-40 -30 -88 0Z" fill="#a8884a" stroke="#111" stroke-width="3"/><path id="varm" d="M1310 640 q50 -30 70 -90" fill="none" stroke="#2a2d38" stroke-width="26" stroke-linecap="round"/></g>`;
  const ajar = `<g id="vajar" class="h" data-t="非常口の扉が、わずかに開いている。……階段から、誰かがのぞいている。" data-cond="ajar"><polygon points="492,360 506,354 506,640 492,650" fill="#05070c"/><circle cx="499" cy="430" r="5" fill="#cfd4e0" opacity=".7"/></g>`;
  return `<div class="vid real"><div class="scr"><div class="ts"></div><div class="cam"><span class="rec">●</span> 12F 廊下 CAM-2</div><svg class="vs" viewBox="0 0 1600 900">${SC3.hall()}${fig}${ajar}<rect class="h" data-cond="lamp" data-f="f_lamp" x="${la[0]}" y="${la[1]}" width="${la[2]}" height="${la[3]}" fill="transparent"/><rect class="h" data-cond="lampreal" data-t="非常口の灯りは、点滅している。現場で見たのと同じ、切れかけの灯りだ。" x="${la[0]}" y="${la[1]}" width="${la[2]}" height="${la[3]}" fill="transparent"/></svg></div><div class="ctr"><button id="vplay">再生</button><span>1:30</span><input id="vt" type="range" min="5400" max="12600" step="10" value="5400" aria-label="映像の時刻"><span>3:30</span></div><div class="marks"><span></span><span>2:00</span><span>2:30</span><span>3:00</span><span></span></div></div>`; }
const vidState = t => ({ loop: t >= 7680 && t < 9000, fig: t >= 10410 && t < 10960, lean: t >= 10500 && t < 10700, ajar: t >= 10480 && t < 10990 });
function videoCond(c, root){ const t = +$('#vt', root).value, s = vidState(t); return c === 'lamp' ? s.loop : c === 'lampreal' ? !s.loop : s[c]; }
function videoInit(root){ const sl = $('#vt', root), ts = $('.ts', root), vid = $('.vid', root), fig = $('#vfig', root), aj = $('#vajar', root), arm = $('#varm', root); let playing = false;
  const upd = () => { const t = +sl.value, s = vidState(t); ts.textContent = `2027/06/07 ${String(Math.floor(t / 3600)).padStart(2, '0')}:${String(Math.floor(t / 60) % 60).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`; vid.classList.toggle('loop', s.loop); vid.classList.toggle('real', !s.loop); fig.style.display = s.fig ? '' : 'none'; aj.style.display = s.ajar ? '' : 'none'; fig.setAttribute('transform', s.lean ? 'translate(60 0) rotate(8 1262 850)' : ''); arm.style.display = s.lean ? 'none' : ''; };
  sl.oninput = upd; $('#vplay', root).onclick = e => { playing = !playing; e.target.textContent = playing ? '停止' : '再生'; }; upd();
  return setInterval(() => { if (playing){ sl.value = Math.min(12600, +sl.value + 20); if (+sl.value >= 12600) playing = false; upd(); } }, 100); }

/* --- deduction board --- */
const cardOf = id => FACTS[id] || HYPS[id];
function openBoard(tab = 'board'){ AudioSys.sfx('select'); delete G.flags.brdNew; const ov = el('div', 'ov'); ov.id = 'brd';
  ov.innerHTML = `<div class="ov-h"><h2>推理ボード<small></small></h2><div class="r"><div class="tabs"><button data-t="board">糸でつなぐ</button><button data-t="tl">時系列</button><button data-t="rel">相関図</button></div><button class="x" id="b-tidy">並べ直す</button><button class="x" id="b-idea" ${G.hintOn ? '' : 'hidden'}>ひらめき</button><button class="x">閉じる</button></div></div><div class="ov-b"></div><div class="foot"><span class="say"></span><span class="cnt"></span></div>`;
  stage.appendChild(ov); const body = $('.ov-b', ov), sayEl = $('.say', ov), cnt = $('.cnt', ov); let sel = null;
  const setTab = t => { tab = t; for (const b of $$('.tabs button', ov)) b.classList.toggle('on', b.dataset.t === t); $('h2 small', ov).textContent = { board: 'カードを2枚押すと、糸が張られる。筋が通れば、仮説が生まれる。糸の●を押すと外れる。', tl: '時刻のわかった事実が、自動で並ぶ。', rel: '人と人のつながり。分かった分だけ、線が増える。' }[t]; body.innerHTML = ''; if (t === 'board') drawBoard(); else if (t === 'tl') body.appendChild(el('div', 'tl', X011() ? timelineSVG() : timelineStd())); else body.appendChild(el('div', 'rel', X011() ? relSVG() : relStd())); };
  const ids = () => [...G.facts, ...G.hyp];
  const posOf = id => { if (!G.pos[id]){ const used = Object.values(G.pos).map(p => p.join()); let i = 0; for (;; i++){ const p = [22 + (i % 7) * 219, 26 + Math.floor(i / 7) * 122]; if (!used.includes(p.join())){ G.pos[id] = p; break; } } } return G.pos[id]; };
  const okLinks = () => { const s = new Set(); for (const h of G.hyp) for (const alt of HYPS[h].need) if (connected(alt)) for (const [a, b] of G.links) if (alt.includes(a) && alt.includes(b)) s.add(a + '|' + b); return s; };
  const connected = alt => { if (!alt.every(x => ids().includes(x))) return false; const seen = new Set([alt[0]]), q = [alt[0]]; while (q.length){ const c = q.pop(); for (const [a, b] of G.links){ if (!alt.includes(a) || !alt.includes(b)) continue; const o = a === c ? b : b === c ? a : null; if (o && !seen.has(o)){ seen.add(o); q.push(o); } } } return seen.size === alt.length; };
  function drawBoard(){ const cv = el('div', 'canvas', '<div class="inner"><svg class="strings"></svg></div>'); body.appendChild(cv); const inner = $('.inner', cv), sv = $('svg', cv);
    const limY = () => Math.max(cv.clientHeight || 640, 26 + (Math.ceil(ids().length / 7) + 1) * 122) - 118, clampP = p => { p[0] = Math.max(0, Math.min(1354, p[0])); p[1] = Math.max(0, Math.min(limY(), p[1])); return p; };
    for (const id of ids()) clampP(posOf(id));
    const strings = () => { const ok = okLinks(); let s = ''; for (const [a, b] of G.links){ const p = posOf(a), q = posOf(b), x1 = p[0] + 103, y1 = p[1] + 4, x2 = q[0] + 103, y2 = q[1] + 4, mx = (x1 + x2) / 2, my = (y1 + y2) / 2 + 26; const good = ok.has(a + '|' + b); s += `<path class="${good ? 'ok' : ''}" d="M${x1} ${y1} Q${mx} ${my} ${x2} ${y2}"/>` + (good ? '' : `<circle cx="${mx}" cy="${my - 13}" r="13" data-a="${a}" data-b="${b}"/><text x="${mx}" y="${my - 8}">×</text>`); } sv.innerHTML = s; for (const c of $$('circle', sv)) c.onclick = () => { G.links = G.links.filter(l => !(l[0] === c.dataset.a && l[1] === c.dataset.b)); AudioSys.sfx('back'); strings(); count(); save(); }; let maxY = 0; for (const id of ids()) maxY = Math.max(maxY, posOf(id)[1]); inner.style.height = maxY + 170 + 'px'; };
    const count = () => { const loose = G.links.length - okLinks().size; cnt.textContent = `糸 ${loose}／8　　カード ${G.facts.length}　仮説 ${G.hyp.length}／${Object.keys(HYPS).length}`; };
    const mk = id => { const c = cardOf(id), hyp = !!HYPS[id], p = posOf(id), d = el('div', 'card' + (hyp ? ' hyp' : ''), `${c.t}<small>${hyp ? '仮説' : c.c}</small>`); d.style.cssText = `left:${p[0]}px;top:${p[1]}px;--c:${hyp ? catc('仮説') : catc(c.c)}`; d.dataset.id = id; d.tabIndex = 0; inner.appendChild(d);
      let st = null; d.addEventListener('pointerdown', e => { d.setPointerCapture(e.pointerId); const s = stage.getBoundingClientRect().width / 1600; st = { x: e.clientX, y: e.clientY, px: p[0], py: p[1], s, mv: 0 }; });
      d.addEventListener('pointermove', e => { if (!st) return; const dx = (e.clientX - st.x) / st.s, dy = (e.clientY - st.y) / st.s; st.mv = Math.max(st.mv, Math.abs(dx) + Math.abs(dy)); if (st.mv > 8){ p[0] = st.px + dx; p[1] = st.py + dy; clampP(p); d.style.left = p[0] + 'px'; d.style.top = p[1] + 'px'; strings(); } });
      d.addEventListener('pointerup', () => { const mv = st ? st.mv : 0; st = null; if (mv > 8){ save(); return; } pickCard(id, d); });
      d.addEventListener('keydown', e => { if (e.key === 'Enter') pickCard(id, d); });
      d.addEventListener('pointerenter', () => tip(c)); d.addEventListener('pointerleave', () => tip(null)); return d; };
    const tip = c => { const o = $('.tip', ov); if (o) o.remove(); if (c) ov.appendChild(el('div', 'tip', `<b>${c.t}</b>${c.d}`)); };
    const pickCard = (id, d) => { if (!sel){ sel = id; d.classList.add('sel'); AudioSys.sfx('tick'); return; } if (sel === id){ sel = null; d.classList.remove('sel'); return; }
      const a = sel, b = id; sel = null; for (const x of $$('.card.sel', inner)) x.classList.remove('sel'); const i = G.links.findIndex(l => (l[0] === a && l[1] === b) || (l[0] === b && l[1] === a));
      if (i >= 0){ if (okLinks().has(G.links[i].join('|'))){ toast('この糸は、もう外せない'); return; } G.links.splice(i, 1); AudioSys.sfx('back'); }
      else { if (G.links.length - okLinks().size >= 8){ AudioSys.sfx('wrong'); toast('糸が足りない。使わない糸を外す', 1); return; } G.links.push([a, b]); AudioSys.sfx('card'); }
      strings(); count(); checkHyp(); save(); };
    const checkHyp = async () => { for (const h in HYPS){ if (G.hyp.includes(h)) continue; if (HYPS[h].need.some(connected)){ G.hyp.push(h); const d = mk(h); d.classList.add('pop'); strings(); count(); AudioSys.sfx('wall'); toast(`<b>仮説</b>${HYPS[h].t}`); const ln = CASE.story[h][0]; sayEl.textContent = '翼「' + ln.t + '」'; AudioSys.speak('tsubasa', ln.t); d.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); save(); refreshHud(); } } };
    for (const id of ids()) mk(id); strings(); count(); window.__brd = { link: (a, b) => { pickCard(a, $(`.card[data-id="${a}"]`, inner)); pickCard(b, $(`.card[data-id="${b}"]`, inner)); } };
    if (!ids().length) sayEl.textContent = 'カードが、まだない。現場と証拠を調べる。';
  }
  for (const b of $$('.tabs button', ov)) b.onclick = () => { AudioSys.sfx('tick'); setTab(b.dataset.t); };
  $('#b-tidy', ov).onclick = () => { for (const id of ids()) delete G.pos[id]; AudioSys.sfx('card'); save(); setTab('board'); sayEl.textContent = 'カードを、並べ直した。糸は、そのまま。'; };
  $('#b-idea', ov).onclick = () => { const h = Object.keys(HYPS).find(h => !G.hyp.includes(h) && HYPS[h].need.some(alt => alt.every(x => ids().includes(x)))); if (!h){ sayEl.textContent = 'いまある材料では、新しい筋は見えない。'; return; } G.hints++; sayEl.textContent = 'ひらめき：' + HYPS[h].hint; save(); };
  $$('.x', ov).pop().onclick = () => { AudioSys.sfx('back'); AudioSys.stopVoice(); ov.remove(); refreshHud(); save(); };
  setTab(tab);
}
function timelineSVG(){ const X = m => 250 + (m - 90) / 105 * 1220, lanes = LANES.map(l => ({ id: l[0], n: l[1], f: G.facts.filter(f => FACTS[f].tl && FACTS[f].tl[0] === l[0]).sort((a, b) => FACTS[a].tl[1] - FACTS[b].tl[1]) })); let y = 60, rows = '';
  for (const l of lanes){ const n = Math.max(2, l.f.length + (l.id === 'cole' && G.hyp.includes('h_conf') ? 1 : 0)), h = n * 30 + 14; l.y = y; l.h = h; rows += `<rect x="0" y="${y}" width="1540" height="${h - 6}" fill="${lanes.indexOf(l) % 2 ? '#121622' : '#161b29'}"/><text x="16" y="${y + h / 2 + 4}" font-size="21" fill="#eef0f5" font-weight="700">${l.n}</text>`;
    l.f.forEach((f, k) => { const F = FACTS[f], [, a, b2] = F.tl, x1 = X(Math.max(90, a)), x2 = Math.max(x1 + 8, X(Math.min(195, b2))), yy = y + 8 + k * 30, left = x2 > 1150; rows += `<rect x="${x1}" y="${yy}" width="${x2 - x1}" height="20" rx="3" fill="${catc(F.c)}"/><text x="${left ? x1 - 8 : x2 + 8}" y="${yy + 15}" font-size="15" fill="#dfe4ee" ${left ? 'text-anchor="end"' : ''}>${F.t}</text>`; });
    if (l.id === 'cole' && G.hyp.includes('h_conf')){ const yy = y + 8 + l.f.length * 30; rows += `<rect x="${X(118)}" y="${yy}" width="${X(141) - X(118)}" height="20" rx="3" fill="none" stroke="#5a9bff" stroke-width="2.5"/><text x="${X(141) + 8}" y="${yy + 15}" font-size="15" fill="#5a9bff">会議に出ていた 1:58〜2:21</text>`; }
    y += h; }
  let s = `<svg viewBox="0 0 1540 ${y + 170}" width="1540" height="${y + 170}">`;
  for (let m = 90; m <= 195; m += 15) s += `<path d="M${X(m)} 48 V${y}" stroke="#2f3850" stroke-width="${m % 30 ? 1 : 2}"/><text x="${X(m)}" y="38" font-size="18" fill="#97a0b4" text-anchor="middle" font-family="monospace">${Math.floor(m / 60)}:${String(m % 60).padStart(2, '0')}</text>`;
  if (G.hyp.includes('h_window')) s += `<rect x="${X(131)}" y="48" width="${X(146) - X(131)}" height="${y - 48}" fill="#e5483d" opacity=".16"/><text x="${X(138.5)}" y="${y + 22}" font-size="16" fill="#e5483d" text-anchor="middle" font-weight="700">犯人が12階にいた時間</text>`;
  s += rows; const y0 = y + 56; s += `<text x="16" y="${y0}" font-size="19" fill="#e3b54a" font-weight="700" letter-spacing="3">この表の外の時刻</text>`;
  const out = [['f_slip', '5月28日'], ['f_msgMon', '6月4日 21:10'], ['f_news', '6月5日'], ['f_mailR', '6月6日 21:52'], ['f_gateM', '6月6日 22:05 〜 7日 7:28'], ['f_confRow', G.hyp.includes('h_conf') ? '日本時間 1:58〜2:21' : '16:58〜17:21（どの時計かは不明）']].filter(x => G.facts.includes(x[0]));
  out.forEach((o, i) => { s += `<text x="${30 + (i % 3) * 500}" y="${y0 + 32 + Math.floor(i / 3) * 30}" font-size="17" fill="#cfd4e0"><tspan fill="#97a0b4" font-family="monospace">${o[1]}　</tspan>${FACTS[o[0]].t}</text>`; });
  if (!G.facts.some(f => FACTS[f].tl)) s += `<text x="770" y="150" font-size="22" fill="#97a0b4" text-anchor="middle">時刻のわかる事実が、まだない。</text>`;
  return s + '</svg>'; }
function timelineStd(){ const fs = G.facts.filter(f => FACTS[f].tm).sort((a, b) => FACTS[a].tm[0] - FACTS[b].tm[0]); if (!fs.length) return '<p style="font-size:22px;color:#97a0b4;padding:40px">時刻のわかる事実が、まだない。</p>';
  const lo = Math.floor((Math.min(...fs.map(f => FACTS[f].tm[0])) - 20) / 30) * 30, hi = Math.ceil((Math.max(...fs.map(f => FACTS[f].tm[1])) + 20) / 30) * 30, X = m => 60 + (m - lo) / (hi - lo) * 1100, step = hi - lo > 600 ? 120 : hi - lo > 240 ? 60 : 30;
  let s = `<svg viewBox="0 0 1540 ${90 + fs.length * 38}" width="1540" height="${90 + fs.length * 38}">`; for (let m = lo; m <= hi; m += step) s += `<path d="M${X(m)} 48 V${70 + fs.length * 38}" stroke="#2f3850"/><text x="${X(m)}" y="38" font-size="18" fill="#97a0b4" text-anchor="middle" font-family="monospace">${Math.floor(m / 60) % 24}:${String(m % 60).padStart(2, '0')}</text>`;
  fs.forEach((f, k) => { const F = FACTS[f], x1 = X(F.tm[0]), x2 = Math.max(x1 + 10, X(F.tm[1])), y = 62 + k * 38; s += `<rect x="0" y="${y - 6}" width="1540" height="34" fill="${k % 2 ? '#121622' : '#161b29'}"/><rect x="${x1}" y="${y}" width="${x2 - x1}" height="22" rx="3" fill="${catc(F.c)}"/><text x="${x2 + 10}" y="${y + 17}" font-size="17" fill="#dfe4ee">${F.t}</text>`; });
  return s + '</svg>'; }
function relStd(){ const ids = [...new Set([...Object.values(LOCS).flatMap(l => l.people.map(p => p.id)), ...REL.flatMap(e => [e.a, e.b])])].filter(id => CHARS[id]), n = ids.length, pos = {}; ids.forEach((id, i) => { const a = -Math.PI / 2 + i * 2 * Math.PI / n; pos[id] = [770 + Math.cos(a) * 520, 350 + Math.sin(a) * 250]; });
  let s = `<svg viewBox="0 0 1540 700" width="1540" height="700">`; for (const e of REL){ if (!pos[e.a] || !pos[e.b] || (e.need && !has(e.need) && !G.flags[e.need])) continue; const a = pos[e.a], b = pos[e.b], mx = (a[0] + b[0]) / 2, my = (a[1] + b[1]) / 2; s += `<path d="M${a[0]} ${a[1]} L${b[0]} ${b[1]}" stroke="${e.need ? '#e3b54a' : '#4a5470'}" stroke-width="${e.need ? 4 : 2}"/><rect x="${mx - e.l.length * 9 - 8}" y="${my - 15}" width="${e.l.length * 18 + 16}" height="28" fill="#0a0c13" stroke="#2f3850"/><text x="${mx}" y="${my + 5}" font-size="16" fill="${e.need ? '#e3b54a' : '#cfd4e0'}" text-anchor="middle">${e.l}</text>`; }
  for (const id of ids){ const c = CHARS[id], [x, y] = pos[id], col = AFF[id] || '#97a0b4'; s += `<g transform="translate(${x} ${y})"><rect x="-110" y="-36" width="220" height="72" fill="#121622" stroke="${col}" stroke-width="3"/><rect x="-110" y="-36" width="8" height="72" fill="${col}"/><text x="0" y="-4" font-size="24" fill="#eef0f5" text-anchor="middle" font-weight="800">${c.name}</text><text x="0" y="22" font-size="13" fill="#97a0b4" text-anchor="middle">${(c.role || '').slice(0, 16)}</text></g>`; }
  return s + '</svg>'; }
function relSVG(){ const N = REL.nodes.filter(n => !n.c || n.c(G)), by = Object.fromEntries(N.map(n => [n.id, n])); let s = `<svg viewBox="0 0 1540 700" width="1540" height="700">`;
  for (const e of REL.edges){ const a = by[e.a], b = by[e.b]; if (!a || !b) continue; const on = !e.c || e.c(G); if (!on && !e.alt) continue; const mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2, lb = on ? e.l : e.alt; s += `<path d="M${a.x} ${a.y} L${b.x} ${b.y}" stroke="${on && e.c ? '#e3b54a' : '#4a5470'}" stroke-width="${on && e.c ? 4 : 2}" ${on ? '' : 'stroke-dasharray="6 8"'}/><rect x="${mx - lb.length * 9 - 8}" y="${my - 15}" width="${lb.length * 18 + 16}" height="28" fill="#0a0c13" stroke="#2f3850"/><text x="${mx}" y="${my + 5}" font-size="16" fill="${on && e.c ? '#e3b54a' : '#cfd4e0'}" text-anchor="middle">${lb}</text>`; }
  for (const n of N){ const col = n.id === 'azzam' ? '#c9824a' : AFF[n.id] || (n.id === 'khalid' || n.id === 'two' ? '#5fae6a' : '#97a0b4'); s += `<g transform="translate(${n.x} ${n.y})"><rect x="-96" y="-36" width="192" height="72" fill="#121622" stroke="${col}" stroke-width="3"/><rect x="-96" y="-36" width="8" height="72" fill="${col}"/><text x="0" y="-4" font-size="24" fill="#eef0f5" text-anchor="middle" font-weight="800">${n.n}</text><text x="0" y="22" font-size="14" fill="#97a0b4" text-anchor="middle">${n.s}</text></g>`; }
  return s + '</svg>'; }

/* --- picker (evidence, facts, hypotheses) --- */
function pick(title, kinds = ['ev', 'fact', 'hyp']){ return new Promise(res => { const ov = el('div', 'ov'); ov.id = 'pick'; let tab = kinds.includes('hyp') && G.hyp.length ? 'hyp' : kinds[0], cur = null; const names = { ev: '証拠', fact: '事実カード', hyp: '仮説' };
  ov.innerHTML = `<div class="ov-h"><h2>${title}</h2><div class="r"><div class="tabs">${kinds.map(k => `<button data-t="${k}">${names[k]}</button>`).join('')}</div><button class="x">やめる</button></div></div><div class="grid"></div><div class="foot"><span class="d"></span><button class="big" id="p-ok" disabled>これにする</button></div>`; stage.appendChild(ov);
  const grid = $('.grid', ov), draw = () => { for (const b of $$('.tabs button', ov)) b.classList.toggle('on', b.dataset.t === tab); grid.innerHTML = ''; const list = tab === 'ev' ? G.ev : tab === 'fact' ? G.facts : G.hyp;
    for (const id of list){ const c = tab === 'ev' ? { t: EV[id].n, d: EV[id].d, c: '人' } : cardOf(id), b = el('button', 'pc' + (tab === 'hyp' ? ' hyp' : '') + (cur === id ? ' on' : ''), `${c.t}<small>${c.d}</small>`); b.style.setProperty('--c', tab === 'hyp' ? catc('仮説') : tab === 'ev' ? '#97a0b4' : catc(c.c)); b.dataset.id = id; b.onclick = () => { cur = id; AudioSys.sfx('tick'); for (const x of $$('.pc', grid)) x.classList.toggle('on', x === b); $('#p-ok', ov).disabled = false; $('.d', ov).textContent = c.t; }; grid.appendChild(b); }
    if (!list.length) grid.innerHTML = `<p style="grid-column:1/-1;color:#97a0b4;font-size:22px">まだ、1つもない。</p>`; };
  for (const b of $$('.tabs button', ov)) b.onclick = () => { tab = b.dataset.t; draw(); };
  $('.x', ov).onclick = () => { AudioSys.sfx('back'); ov.remove(); res(null); }; $('#p-ok', ov).onclick = () => { AudioSys.sfx('select'); ov.remove(); res(cur); }; draw(); }); }

/* --- interrogation --- */
let IT = null;
async function cutin(txt, ok){ const c = el('div', ok ? 'ok' : '', `<b>${txt}</b>`); c.id = 'cutin'; stage.appendChild(c); AudioSys.sfx(ok ? 'cutin' : 'shock'); await sleep(900); c.remove(); }
async function interrogate(key){ const D = INTR[key], S = G.intr[key]; mode = 'intr'; hud.hidden = true; bar.hidden = true;
  if (!bgSame(D.bg)) await fadeTo(() => { setBg(D.bg); hideChar('all'); });
  AudioSys.bgm('battle'); showChar(D.foe, 'foe'); S.g = 5;
  if (!S.n){ if (D.intro) await play(D.intro); S.open = D.open.slice(); for (const id of S.open) await play(id); } S.n++;
  endDlg(); showChar(D.foe, 'foe'); IT = { key, sel: null }; drawIntr(); save(); }
function drawIntr(){ const { key } = IT, D = INTR[key], S = G.intr[key], box = $('#intr'); hideChar('tsubasa'); setSpeaker('*'); box.hidden = false; hud.hidden = false; bar.hidden = true; mode = 'intr'; refreshHud();
  box.innerHTML = `<div class="hd"><b>尋問　${D.title}</b><div class="gauge">信頼 ${[0, 1, 2, 3, 4].map(i => `<i class="${i < S.g ? '' : 'off'}"></i>`).join('')}</div></div>` + S.open.map((id, n) => { const st = D.st[id], br = S.done.includes(id); return `<div class="st${br ? ' broken' : ''}${IT.sel && IT.sel[0] === id ? ' cur' : ''}" data-id="${id}"><u>${n + 1}</u>${st.ph.map((p, i) => `<span data-i="${i}" class="${IT.sel && IT.sel[0] === id && IT.sel[1] === i ? 'on' : ''}">${p}</span>`).join('')}</div>`; }).join('') + `<div class="guide">${IT.msg ? IT.msg : IT.sel ?'「ゆさぶる」で、くわしく聞く。食いちがう物を持っていれば「突きつける」。' : 'まず、証言の中の言葉を押して選ぶ。点線の区切りごとに選べる。'}</div><div class="ac"><button class="big alt" id="i-press">ゆさぶる</button><button class="big red" id="i-pres">突きつける</button>${G.hintOn ? '<button class="big alt" id="i-hint">ヒント</button>' : ''}<button class="big alt" id="i-back">退く</button></div>`;
  for (const sp of $$('.st:not(.broken) span', box)) sp.onclick = () => { IT.msg = null; IT.sel = [sp.parentNode.dataset.id, +sp.dataset.i]; AudioSys.sfx('tick'); drawIntr(); };
  $('#i-press').disabled = $('#i-pres').disabled = !IT.sel;
  $('#i-press').onclick = () => guard(async () => { const id = IT.sel[0]; box.hidden = true; hud.hidden = true; await play(id); await play(D.st[id].p); endDlg(); drawIntr(); });
  $('#i-pres').onclick = () => guard(() => present());
  $('#i-back').onclick = () => guard(async () => { AudioSys.sfx('back'); await leaveIntr(); });
  const hb = $('#i-hint'); if (hb) hb.onclick = () => { const id = S.open.find(x => !S.done.includes(x) && D.st[x].ans); if (id){ G.hints++; toast(`<b>ヒント</b>${D.st[id].hint}`); save(); } };
}
function nearMsg(st){ const hs = (st.ok || []).filter(x => HYPS[x]);
  if (!hs.length) return '惜しい。近い物だが、決め手ではない。別の証拠か、事実カードを探す。';
  if (hs.some(h => G.hyp.includes(h))) return '惜しい。決め手は、もう持っている。「突きつける」の右上の「仮説」から選ぶ。';
  return '惜しい。カード1枚では崩せない。「退く」で戻り、ボードでカードを2枚つないで「仮説」を作る。カードが足りなければ、証拠の字を押して増やす。'; }
async function leaveIntr(){ $('#intr').hidden = true; IT = null; hideChar('all'); await enterLoc(G.loc, true); }
async function present(){ const { key, sel } = IT, D = INTR[key], S = G.intr[key], st = D.st[sel[0]], box = $('#intr');
  const item = await pick('突きつける物を選ぶ'); if (!item) return; box.hidden = true; hud.hidden = true;
  const okItem = st.ok && st.ok.includes(item), okPh = st.ans && st.ans.includes(sel[1]);
  if (okItem && okPh){ await cutin('矛盾', 1); AudioSys.bgm('tension'); await play(st.o); S.done.push(sel[0]); if (st.opens) for (const n of st.opens){ S.open.push(n); endDlg(); await play(n); } IT.sel = null; save();
    if (D.need.every(x => S.done.includes(x))){ S.clear = 1; await play(D.end); endDlg(); $('#intr').hidden = true; IT = null; hideChar('all'); save(); if (!X011()){ G.flags.rep = 1; save(true); toast('<b>報告</b>推理レポートが書けるようになった'); await enterLoc(G.loc, true); return; } if (key === 'C'){ await ending(); return; } await triggers(); if (!G.flags.mid || G.loc !== 'soukan') await enterLoc(G.loc, true); return; }
    AudioSys.bgm('battle'); endDlg(); showChar(D.foe, 'foe'); drawIntr(); return; }
  if (okItem && !okPh){ await play('x_near'); endDlg(); showChar(D.foe, 'foe'); IT.msg = '物は合っている。突く言葉がちがう。証言の、別の区切りを選ぶ。'; drawIntr(); return; }
  if (st.near && st.near[item]){ await play(st.near[item]); endDlg(); IT.msg = nearMsg(st); drawIntr(); return; }
  S.g--; G.miss++; AudioSys.sfx('damage'); stage.classList.remove('shake'); void stage.offsetWidth; stage.classList.add('shake'); await play(D.miss[G.miss % 2]); endDlg(); save();
  if (S.g <= 0){ G.brk++; await play('x_break'); endDlg(); await leaveIntr(); return; }
  drawIntr(); }

/* --- final report --- */
function openReport(){ AudioSys.sfx('select'); const ov = el('div', 'ov'); ov.id = 'rep';
  ov.innerHTML = `<div class="ov-h"><h2>推理レポート<small>${REPORT.length}つの欄を埋める。根拠を添えると、評価が上がる。</small></h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b"><div class="form"><h3>捜査報告書</h3><div class="meta"><span>事件　${X011() ? '港区マンション亡命記者殺害' : META.name}</span><span>報告者　日米統合サイバー捜査総監</span><span>${DAYS[G.day]}</span></div><div class="rows"></div><div class="sub"><span class="msg"></span><button class="big red" id="r-go">提出する</button></div></div></div>`; stage.appendChild(ov);
  const rows = $('.rows', ov), draw = () => { rows.innerHTML = ''; for (const R of REPORT){ const r = el('div', 'fr' + (R.a === 'o-1' ? ' open' : ''), `<h4>${R.q}<small>${R.sub}</small></h4><div class="op"></div><button class="sp${G.sup[R.k] ? ' set' : ''}" data-k="${R.k}"><b>根拠</b>${G.sup[R.k] ? (EV[G.sup[R.k]] ? EV[G.sup[R.k]].n : cardOf(G.sup[R.k]).t) : '押して、カードか証拠を1つ添える'}</button>`);
      for (const [v, l] of R.opts){ const b = el('button', G.rep[R.k] === v ? 'on' : '', l); b.dataset.v = v; b.onclick = () => { G.rep[R.k] = v; AudioSys.sfx('tick'); draw(); save(); }; $('.op', r).appendChild(b); }
      $('.sp', r).onclick = async () => { const it = await pick(`「${R.q}」の根拠`, ['hyp', 'fact', 'ev']); if (it){ G.sup[R.k] = it; draw(); save(); } }; rows.appendChild(r); }
    const n = REPORT.filter(R => G.rep[R.k]).length; $('#r-go', ov).disabled = n < REPORT.length; $('.msg', ov).textContent = n < REPORT.length ? `あと${REPORT.length - n}つの欄が空いている。` : (G.wrongRep ? `書き直し ${G.wrongRep}回目。` : '提出すると、結論に従って事が動く。'); };
  let armed = false; $('#r-go', ov).onclick = () => { if (!armed){ armed = true; $('#r-go', ov).textContent = '本当に提出する'; $('.msg', ov).textContent = '提出すると、取り消せない。'; return; } ov.remove(); guard(X011() ? submitReport : submitStd); };
  $('.x', ov).onclick = () => { AudioSys.sfx('back'); ov.remove(); }; draw(); }
function scoreReport(){ let right = 0, sup = 0; for (const R of REPORT){ if (R.a === 'o-1'){ if (G.rep[R.k]){ right++; sup++; } } else if (G.rep[R.k] === R.a){ right++; if (R.sup.includes(G.sup[R.k])) sup++; } } return { right, sup }; }
async function submitStd(){ mode = 'dlg'; G.score = scoreReport(); const R0 = REPORT[0];
  if (G.rep[R0.k] !== R0.a){ G.wrongRep++; await play('bad'); endDlg(); hideChar('all'); await result('BAD END', '取りちがえ', 'C', true); return; }
  await play('fin'); for (const R of REPORT) if (R.a === 'o-1'){ const b = 'pick_' + R.k + '_' + G.rep[R.k]; if (CASE.story[b]) await play(b); } if (CASE.story.last) await play('last'); endDlg(); hideChar('all'); G.flags.done = 1; const n = REPORT.length, sc = G.score, pts = Math.round(2 + sc.right * 56 / n + sc.sup * 42 / n) - G.miss * 2 - G.brk * 5 - G.hints * 3 - G.wrongRep * 10, rank = pts >= 90 ? 'S' : pts >= 75 ? 'A' : pts >= 55 ? 'B' : 'C';
  G.final = ['CASE CLOSED', META.name, rank, false, pts]; save(true); await result(...G.final); }
async function submitReport(){ mode = 'dlg'; const mole = G.rep.mole; await play('rep_intro');
  if (mole !== 'mashiba'){ G.wrongRep++; await play(mole === 'cole' ? 'bad_cole' : mole === 'saegusa' ? 'bad_saegusa' : 'bad_other'); endDlg(); hideChar('all'); await result('BAD END', { cole: '同盟の終わり', saegusa: '閉じた扉' }[mole] || '振り出し', 'C', true); return; }
  G.flags.repOK = 1; G.score = scoreReport(); G.loc = 'renraku'; save(); endDlg(); await interrogate('C'); }
async function ending(){ const i = await choose('真柴に、何と言うか', [{ l: '静かに、事実だけを言う' }, { l: '怒りを、そのままぶつける', cls: 'hot' }]); await play(i ? 'c_angry' : 'c_calm'); endDlg(); hideChar('all');
  const full = G.rep.doer === 'two' && G.rep.boss === 'khalid'; await play(full ? 'end_true' : 'end_half'); endDlg(); hideChar('all'); G.flags.done = 1; save();
  const sc = G.score, pts = 2 + sc.right * 8 + sc.sup * 6 - G.miss * 2 - G.brk * 5 - G.hints * 3 - G.wrongRep * 10, rank = !full ? (pts >= 55 ? 'B' : 'C') : pts >= 90 ? 'S' : pts >= 75 ? 'A' : pts >= 55 ? 'B' : 'C';
  G.final = [full ? 'TRUE END' : 'NORMAL END', full ? '鍵のない部屋' : '名前のない実行犯', rank, false, pts]; save();
  await result(...G.final); }
async function result(kind, name, rank, bad, pts){ AudioSys.bgm(bad ? 'tension' : 'truth'); const sc = G.score || scoreReport(), ov = el('div', 'ov'), n = REPORT.length, x11 = X011(); ov.id = 'res'; if (!bad) recordDone(kind, rank, pts);
  const nx = String(+CID + 1).padStart(3, '0'), hasNext = !bad && AVAIL.includes(nx);
  const txt = bad ? (x11 ? '内通者を取りちがえた。報告書は、もう1度書ける。物を見直し、ボードで筋を組み直す。' : '最初の欄を取りちがえた。報告書は、もう1度書ける。物を見直し、ボードで筋を組み直す。') : rank === 'S' ? '全ての欄が正しく、根拠もそろった。物だけで、筋を通した。' : rank === 'A' ? '結論は正しい。根拠の添え方か、尋問の運びに、少し無駄があった。' : kind === 'NORMAL END' ? '内通者は挙げた。だが、実行犯か指示役の欄が、物と合っていない。' : '結論には届いた。だが、空振りか、まちがった欄か、手助けが多かった。';
  ov.innerHTML = `<div class="end">${kind}　FILE ${CID}</div><h2>${name}</h2><div class="rank ${rank}">${rank}</div><table><tr><td>報告書の正しさ</td><td>${sc.right}／${n}</td></tr><tr><td>正しい根拠</td><td>${sc.sup}／${n}</td></tr><tr><td>尋問の空振り</td><td>${G.miss}</td></tr><tr><td>尋問の中断</td><td>${G.brk}</td></tr><tr><td>ヒント</td><td>${G.hints}</td></tr><tr><td>書き直し</td><td>${G.wrongRep}</td></tr>${pts != null ? `<tr><td>評点</td><td>${pts}</td></tr>` : ''}</table><p>${txt}</p><div style="display:flex;gap:14px">${bad ? '<button class="big" id="rs-re">報告書を書き直す</button>' : (hasNext ? '<button class="big" id="rs-nx">次の事件へ</button>' : '') + '<button class="big alt" id="rs-rep">報告書からやり直す</button>'}<button class="big alt" id="rs-t">事件を選ぶ</button></div>`;
  stage.appendChild(ov); window.__res = { kind, rank, pts, id: CID };
  const r = await new Promise(res => { const re = $('#rs-re', ov), rp = $('#rs-rep', ov), nxb = $('#rs-nx', ov); if (re) re.onclick = () => { ov.remove(); res('re'); }; if (nxb) nxb.onclick = () => { ov.remove(); res('next'); };
    if (rp) rp.onclick = () => { ov.remove(); G.final = null; G.flags.repOK = 0; G.flags.done = 0; if (G.intr.C) G.intr.C = { open: [], done: [], g: 5, clear: 0, n: 0 }; G.miss = 0; G.brk = 0; res('re'); }; $('#rs-t', ov).onclick = () => { ov.remove(); res('title'); }; });
  save(true); if (r === 'title'){ showTitle(); openSelect(); return; } if (r === 'next'){ busy = false; startCase(nx, false); return; } await enterLoc(x11 ? 'soukan' : G.loc, true); }
function openLog(){ const ov = el('div', 'ov'); ov.id = 'log'; ov.innerHTML = `<div class="ov-h"><h2>記録</h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b">${LOG.map(l => `<div class="lg${l[0] ? '' : ' n'}">${l[0] ? `<b>${l[0]}</b>` : ''}${l[1]}</div>`).join('') || '<p>まだ、何もない。</p>'}</div>`; stage.appendChild(ov); $('.x', ov).onclick = () => ov.remove(); const b = $('.ov-b', ov); b.scrollTop = b.scrollHeight; }
function openSet(){ AudioSys.sfx('select'); const ov = el('div', 'ov'); ov.id = 'set'; const seg = (k, opts, cur) => `<div class="seg" data-k="${k}">${opts.map(o => `<button data-v="${o[0]}" class="${String(cur) === String(o[0]) ? 'on' : ''}">${o[1]}</button>`).join('')}</div>`;
  ov.innerHTML = `<div class="ov-h"><h2>設定</h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b">
  <div class="sr"><label>ヒント<small>入にすると、探す場所や筋の手がかりが出る。使うたびに評価が下がる。</small></label>${seg('hint', [[0, '切'], [1, '入']], G ? G.hintOn : O.hint)}</div>
  <div class="sr"><label>保存<small>${Cloud.state === 'ok' ? 'Claudeのアカウントと、この端末に、自動で保存している。' : lsOK ? 'この端末のブラウザに、自動で保存している。' : 'この端末には保存できない。合言葉で持ち出す。'}</small></label><div class="seg"><button id="s-save">いま保存する</button><button id="s-code">合言葉</button></div></div>
  <div class="sr"><label>動き<small>音が途切れる時や、動きが重い時は「軽い」にする。</small></label>${seg('q', [['auto', '自動'], ['high', 'なめらか'], ['lite', '軽い']], O.q)}</div>
  <div class="sr"><label>声</label>${seg('voice', [[1, '入'], [0, '切']], O.voice)}</div>
  <div class="sr"><label for="s-bgm">音楽の大きさ</label><input id="s-bgm" type="range" min="0" max="1" step=".05" value="${O.bgm}"></div>
  <div class="sr"><label for="s-se">効果音の大きさ</label><input id="s-se" type="range" min="0" max="1" step=".05" value="${O.se}"></div>
  <div class="sr"><label>文字の速さ</label>${seg('speed', [[46, 'ゆっくり'], [26, 'ふつう'], [10, '速い']], O.speed)}</div>
  <div class="sr"><label>全画面</label><div class="seg"><button id="s-full">切り替える</button></div></div>
  <div class="sr"><label>記録<small>これまでの会話を読み返す。</small></label><div class="seg"><button id="s-log">開く</button></div></div>
  <div class="sr"><label>声と音について</label><div class="seg"><button id="s-cred">クレジットを見る</button></div></div>
  <div class="sr"><label>タイトルへ戻る<small>進み具合は、自動で保存されている。</small></label><div class="seg"><button id="s-title">戻る</button></div></div></div>`; stage.appendChild(ov);
  for (const s of $$('.seg[data-k]', ov)) for (const b of $$('button', s)) b.onclick = () => { const k = s.dataset.k, v = k === 'q' ? b.dataset.v : +b.dataset.v; if (k === 'hint'){ O.hint = v; saveOpt(); if (G){ G.hintOn = v; save(); refreshHud(); } } else { O[k] = v; saveOpt(); applyOpt(); if (k === 'q') initQuality(); } for (const x of $$('button', s)) x.classList.toggle('on', x === b); AudioSys.sfx('tick'); };
  $('#s-bgm', ov).oninput = e => { O.bgm = +e.target.value; saveOpt(); applyOpt(); }; $('#s-se', ov).oninput = e => { O.se = +e.target.value; saveOpt(); applyOpt(); AudioSys.sfx('tick'); };
  $('#s-full', ov).onclick = () => { try { (document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen()).catch(() => toast('この画面では、全画面にできない', 1)); } catch (e) { toast('この画面では、全画面にできない', 1); } };
  $('#s-save', ov).onclick = () => { if (!G){ toast('事件の中で押す'); return; } save(true); toast(Cloud.state === 'ok' ? '<b>保存</b>アカウントと端末に保存した' : lsOK ? '<b>保存</b>この端末に保存した' : '保存できなかった。合言葉を使う', !lsOK && Cloud.state !== 'ok'); }; $('#s-code', ov).onclick = openCode; $('#s-log', ov).onclick = openLog; $('#s-cred', ov).onclick = openCred; $('#s-title', ov).onclick = () => { if (busy && mode !== 'intr') { toast('会話が終わってから戻る', 1); return; } save(true); ov.remove(); showTitle(); };
  $('.x', ov).onclick = () => { AudioSys.sfx('back'); ov.remove(); }; }
function applyOpt(){ AudioSys.setVol('bgm', O.bgm); AudioSys.setVol('se', O.se); AudioSys.setVol('voice', O.voice ? 1 : 0); }
function openCred(){ const ov = el('div', 'ov'); ov.id = 'cred'; ov.innerHTML = `<div class="ov-h"><h2>クレジット</h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b"><p>声は、音声合成ソフト VOICEVOX で作った。</p><p>${CREDIT}</p><p>音楽と効果音は、このページの中で鳴らしている合成音。絵は全て、このゲームのために描いた物。</p><p>この物語はフィクション。実在の人物、団体、製品とは関係がない。</p></div>`; stage.appendChild(ov); $('.x', ov).onclick = () => ov.remove(); }
function showTitle(keep){ if (!keep){ mode = 'title'; $$('.ov').forEach(o => o.remove()); $('#intr').hidden = true; IT = null; G = null; hud.hidden = true; bar.hidden = true; endDlg(); hideChar('all'); setTel('off'); curBg = null; setBg('genkan'); cam(815, 400, 1.5, 0); world.classList.add('drift'); AudioSys.bgm('tension'); $('#title').hidden = false; }
  const c = $('#t-cont'), last = MET.last && AVAIL.includes(MET.last) && hasSave(MET.last) ? MET.last : null; c.hidden = !last; if (last) c.textContent = 'つづきから　FILE ' + last; }
async function startCase(id, cont){ AudioSys.init(); applyOpt(); if (busy) return; busy = true; try { await useCase(id); } catch (e) { console.error(e); toast('事件を読み込めなかった。通信を確かめる', 1); busy = false; return; }
  const sv = cont ? await loadSave(id) : null; busy = false; $('#title').hidden = true; $$('.ov').forEach(o => o.remove()); LOG = []; FAST = false; dlgTools(); AudioSys.loadPack(META.vurl, META.vidx); mode = 'dlg';
  if (sv){ G = sv; curBg = null; if (G.final){ setBg(LOCS[G.loc].bg); await guard(() => result(...G.final)); return; } if (X011() && G.intr.C.n && G.flags.repOK && !G.intr.C.clear) G.loc = 'renraku'; await enterLoc(G.loc, true); return; }
  G = newG(); await guard(async () => { mode = 'dlg'; for (const b of META.intro) await play(b); G.phase = 'free'; endDlg(); await enterLoc(META.start, true); }); }
function openSelect(){ AudioSys.init(); applyOpt(); AudioSys.sfx('select'); const ov = el('div', 'ov'); ov.id = 'sel'; let ch = MET.last ? Math.floor((+MET.last - 1) / 10) : 1, cur = null;
  ov.innerHTML = `<div class="ov-h"><h2>事件を選ぶ<small>全100事件。好きな順に遊べる。</small></h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b"><div class="chs"></div><div class="cs"></div></div><div class="foot"><span class="d">事件を押して選ぶ。</span><span class="bt"><button class="big alt" id="c-new" disabled>はじめから</button><button class="big" id="c-cont" disabled>つづきから</button></span></div>`; stage.appendChild(ov);
  const chs = $('.chs', ov), cs = $('.cs', ov), draw = () => { chs.innerHTML = ''; CHAPS.forEach((nm, i) => { const ids = CASELIST.filter(c => c[2] === i + 1).map(c => c[0]), dn = ids.filter(x => MET.done[x]).length, b = el('button', i === ch ? 'on' : '', `<b>第${i + 1}章</b>${nm}<small>${dn}／10</small>`); b.onclick = () => { ch = i; cur = null; AudioSys.sfx('tick'); draw(); }; chs.appendChild(b); });
    cs.innerHTML = ''; for (const c of CASELIST.filter(c => c[2] === ch + 1)){ const id = c[0], av = AVAIL.includes(id), dn = MET.done[id], sv = hasSave(id), b = el('button', 'ct' + (av ? '' : ' na') + (cur === id ? ' on' : ''), `<u>${id}</u><b>${c[1]}</b><small>${!av ? '準備中' : dn ? '解決　評価 ' + dn.rank : sv ? '捜査中' : '未着手'}</small>${dn ? `<i class="rk ${dn.rank}">${dn.rank}</i>` : ''}`); b.dataset.id = id;
      b.onclick = () => { if (!av){ toast('この事件は、まだ準備中'); return; } cur = id; AudioSys.sfx('tick'); draw(); }; cs.appendChild(b); }
    const d = $('.d', ov), bn = $('#c-new', ov), bc = $('#c-cont', ov); bn.disabled = !cur; bc.disabled = !cur || !hasSave(cur); bn.textContent = 'はじめから'; d.textContent = cur ? `FILE ${cur}　${CASELIST.find(c => c[0] === cur)[1]}` : '事件を押して選ぶ。'; };
  let armed = false; $('#c-new', ov).onclick = () => { if (hasSave(cur) && !armed){ armed = true; $('#c-new', ov).textContent = '消して、はじめから'; $('.d', ov).textContent = '途中の記録は消える。もう1度押すと始まる。'; return; } startCase(cur, false); }; $('#c-cont', ov).onclick = () => startCase(cur, true);
  $('.x', ov).onclick = () => { AudioSys.sfx('back'); ov.remove(); }; draw(); }
const enc64 = s => btoa(unescape(encodeURIComponent(s))), dec64 = s => decodeURIComponent(escape(atob(s.replace(/\s+/g, ''))));
function openCode(){ const ov = el('div', 'ov'); ov.id = 'code';
  ov.innerHTML = `<div class="ov-h"><h2>合言葉<small>記録を文字にして持ち出す。別の端末や、消えた時に戻せる。</small></h2><div class="r"><button class="x">閉じる</button></div></div><div class="ov-b"><p>${G ? 'いまの事件の記録。全部を選んで、写しておく。' : '事件の中で開くと、その事件の記録が出る。'}</p><textarea id="code-out" readonly rows="6"></textarea><p><button class="big alt" id="code-copy">写す</button></p><p>戻す時は、下に貼って「戻す」を押す。</p><textarea id="code-in" rows="6" placeholder="ここに貼る"></textarea><p><button class="big" id="code-go">戻す</button></p></div>`; stage.appendChild(ov);
  if (G) $('#code-out', ov).value = enc64(JSON.stringify({ id: CID, g: G }));
  $('#code-copy', ov).onclick = () => { const t = $('#code-out', ov); t.select(); try { navigator.clipboard.writeText(t.value).then(() => toast('写した'), () => toast('選んだ状態にした。長押しで写す')); } catch (e) { toast('選んだ状態にした。長押しで写す'); } };
  $('#code-go', ov).onclick = () => { try { const o = JSON.parse(dec64($('#code-in', ov).value)); if (!o || !o.g || o.g.v !== 1 || !AVAIL.includes(o.id)) throw 0; o.g.ts = Date.now(); LS.set(saveKey(o.id), o.g); Cloud.put('c' + o.id, { s: JSON.stringify(o.g), ts: o.g.ts }, true); MET.saves[o.id] = o.g.ts; MET.last = o.id; saveMeta(true); busy = false; startCase(o.id, true); } catch (e) { toast('合言葉が読めない。全部を貼ったか確かめる', 1); } };
  $('.x', ov).onclick = () => ov.remove(); }
$('#t-new').onclick = openSelect; $('#t-cont').onclick = () => { if (MET.last) startCase(MET.last, true); }; $('#t-set').onclick = () => { AudioSys.init(); applyOpt(); openSet(); };
$('#t-ev').onclick = () => { if (!busy || mode === 'intr') openIns(); }; $('#t-brd').onclick = () => { if (!busy || mode === 'intr') openBoard(); }; $('#t-set2').onclick = openSet; $('#t-log').onclick = openLog;
$('#a-map').onclick = openMap; $('#a-rep').onclick = () => { if (!busy && mode === 'free') openReport(); };
window.__g = { start: startCase, get meta(){ return MET; }, get cloud(){ return Cloud.state; }, get D(){ return { id: CID, HYPS, INTR, REPORT, locs: Object.keys(LOCS), ev: Object.keys(EV), facts: Object.keys(FACTS), names: Object.fromEntries(Object.keys(CHARS).map(k => [k, CHARS[k].name])) }; }, get G(){ return G; }, get mode(){ return mode; }, get busy(){ return busy; }, fast(v){ FAST = v; dlgTools(); }, hs(){ const L = LOCS[G.loc]; return activeHs().map(h => { const r = hsRect(L, h), pt = bg.createSVGPoint(); pt.x = r[0] + r[2] / 2; pt.y = r[1] + r[3] / 2; const q = pt.matrixTransform(bg.getScreenCTM()); return { id: h.id, x: q.x, y: q.y, seen: !!G.seen[h.id], enter: h.enter || null, desk: !!h.desk }; }); }, advance: onAdvance };
if (window.claude && window.claude.hot && window.claude.hot.snapshot) try { window.claude.hot.snapshot(() => ({})); } catch (e) {}
initQuality();
showTitle();
