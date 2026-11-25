/* ---------- engine v2: many cases, each from its own script file ---------- */
const $ = s => document.querySelector(s), $$ = s => Array.from(document.querySelectorAll(s));
const sleep = ms => new Promise(r => setTimeout(r, ms));
const CAST = parseCase(CAST_TXT);
Object.assign(CHARS, CAST.chars);
const CASES = {}; for (const id of Object.keys(CASE_TXT)) CASES[id] = parseCase(CASE_TXT[id]);
const CASE_IDS = Object.keys(CASES).sort();
let C = null, STORY = {}, EVID = {}, VIEWS = {};
const st = { flags: new Set(), ev: [], seen: new Set(), view: 'tsubasa', loc: null, miss: 0, hints: 0, retries: 0, step: 0, log: [], auto: false, fast: false, speed: 34, inv: null };
const has = k => k.startsWith('f:') ? st.flags.has(k.slice(2)) : (st.ev.includes(k) || st.flags.has(k));
const SAVE_KEY = 'soukan-tsubasa-v2';
function loadStore(){ try { return JSON.parse(localStorage.getItem(SAVE_KEY) || '{}') || {}; } catch (e) { return {}; } }
function putStore(o){ try { localStorage.setItem(SAVE_KEY, JSON.stringify(o)); } catch (e) {} }
function saveProgress(){ const s = loadStore(); s.cur = { id: C.id, step: st.step, flags: [...st.flags], ev: st.ev, seen: [...st.seen], miss: st.miss, hints: st.hints, retries: st.retries }; putStore(s); }
const stage = $('#stage'), bg = $('#bg'), charsG = $('#chars'), hsG = $('#hs'), fxG = $('#fx');
const dialog = $('#dialog'), nameEl = $('#name'), textEl = $('#text'), nextEl = $('#next'), menu = $('#menu');
let tapRes = null, talkId = null, typingNow = false, mode = 'dialog', tel = null, curBg = null, autoSlots = [];
const waitTap = () => new Promise(r => { tapRes = r; });
function onTap(){ if (tapRes){ const r = tapRes; tapRes = null; r(); } }
dialog.addEventListener('click', onTap);
stage.addEventListener('click', () => { if (mode === 'dialog') onTap(); });
$('#card').addEventListener('click', onTap); $('#getpop').addEventListener('click', onTap);
document.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('button,input,select')){ e.preventDefault(); onTap(); } });
/* --- characters on stage --- */
const CS = 0.84, CY = 400 - 360 * CS + 6, POS = { left: 150 - 120 * CS, center: 320 - 120 * CS, right: 490 - 120 * CS };
function findCh(id){ return $$(`.ch[data-id="${id}"]`); }
function showChar(id, pos = 'center'){
  const c = CHARS[id]; if (!c || c.noart) return;
  let s = charsG.querySelector(`.slot[data-id="${id}"]`); const flip = pos === 'right';
  if (s && s.dataset.flip !== String(flip)){ s.remove(); s = null; }
  if (!s){ s = document.createElementNS('http://www.w3.org/2000/svg', 'g'); s.setAttribute('class', 'slot'); s.dataset.id = id; s.dataset.flip = String(flip);
    s.innerHTML = `<g class="slot-in">${c.remote ? '<rect x="6" y="-14" width="228" height="380" rx="12" fill="#17344f" stroke="#7fd0ff" stroke-width="3"/><text x="120" y="6" font-size="12" fill="#7fd0ff" text-anchor="middle" font-family="monospace">● LIVE</text>' : ''}<g class="ch" data-id="${id}">${charSVG(id, flip)}</g></g>`;
    charsG.appendChild(s); applyExpr(s.querySelector('.ch'), 'n'); }
  for (const o of $$('.slot')) if (o !== s && o.dataset.pos === pos){ o.remove(); autoSlots = autoSlots.filter(x => x !== o.dataset.id); }
  s.dataset.pos = pos; s.setAttribute('transform', `translate(${POS[pos]} ${CY}) scale(${CS})`); stage.classList.toggle('has-ch', true);
}
function hideChar(id){ if (id === 'all'){ charsG.innerHTML = ''; autoSlots = []; } else { const s = charsG.querySelector(`.slot[data-id="${id}"]`); if (s) s.remove(); autoSlots = autoSlots.filter(x => x !== id); } stage.classList.toggle('has-ch', !!charsG.children.length); }
function setSpeaker(who, e){
  for (const s of $$('.slot')){ s.classList.toggle('speaking', s.dataset.id === who); s.classList.toggle('dim', who !== '*' && s.dataset.id !== who); }
  if (who === '*') return;
  for (const g of findCh(who)){ applyExpr(g, e); const si = g.closest('.slot-in') || g; const a = { u: 'jump', a: 'shake', d: 'droop', t: 'shiver', s: 'hop' }[e]; if (a){ si.classList.remove('jump', 'shake', 'droop', 'shiver', 'hop'); void si.getBoundingClientRect(); si.classList.add(a); } }
}
function tick(ts){
  const t = ts / 1000, lvl = AudioSys.level(), sp = AudioSys.speaking();
  for (const g of $$('.ch')){
    const ph = g._ph ?? (g._ph = Math.random() * 6);
    if (!g._nb) g._nb = t + 1 + Math.random() * 3;
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
  const tm = bg.querySelector('.timer'); if (tm){ const left = Math.max(0, 46 * 3600 + 19 * 60 + 58 - Math.floor(t)); tm.textContent = [Math.floor(left / 3600), Math.floor(left / 60) % 60, left % 60].map(v => String(v).padStart(2, '0')).join(':'); }
  requestAnimationFrame(tick);
}
/* --- stage commands --- */
function setObj(name, state){
  if (name === 'tejou'){ fxCuffs(); return; }
  if (name === 'tell'){ for (const g of $$('.slot .ch')){ g.classList.remove('tell'); void g.getBoundingClientRect(); g.classList.add('tell'); } return; }
  bg.setAttribute('data-' + name, ''); void bg.getBoundingClientRect(); bg.setAttribute('data-' + name, state);
  for (const el of bg.querySelectorAll('.o-' + name)){ el.removeAttribute('data-st'); void el.getBoundingClientRect(); el.setAttribute('data-st', state); }
}
async function setBg(id){
  if (curBg === id) return; const f = $('#fade'); f.classList.add('on'); await sleep(st.fast ? 50 : 260);
  if (!SCENES[id]) console.warn('no scene', id);
  bg.innerHTML = (SCENES[id] || SCENES.kaigi)(); for (const a of [...bg.attributes]) if (a.name.startsWith('data-')) bg.removeAttribute(a.name);
  bg.dataset.scene = id; curBg = id; for (const g of bg.querySelectorAll('.ch')) applyExpr(g, 'n');
  if (id === 'kouhei' && st.ev.includes('tejou')) bg.dataset.tsutsumi = 'open';
  hideChar('all'); f.classList.remove('on'); await sleep(st.fast ? 20 : 160);
}
async function card(txt){ const [a, b] = txt.split('｜'); const c = $('#card'); c.innerHTML = `<div class="c1">${a}</div>${b ? `<div class="c2">${b}</div>` : ''}`; c.hidden = false; AudioSys.sfx('card'); await Promise.race([sleep(st.fast ? 120 : 1900), waitTap()]); tapRes = null; c.hidden = true; }
async function getEv(id){
  if (st.ev.includes(id)) return; st.ev.push(id); const e = EVID[id]; if (!e){ console.warn('no evidence', id); return; } AudioSys.sfx('get');
  const p = $('#getpop'); p.innerHTML = `<div class="gp-h">証拠ファイルに追加</div><div class="gp-b"><span class="evk">${e.k}</span><div><b>${e.n}</b><p>${e.d}</p></div></div>`; p.hidden = false;
  await Promise.race([waitTap(), sleep(st.fast ? 100 : 600000)]); tapRes = null; p.hidden = true; updHud();
}
function fxCuffs(){ fxG.innerHTML = `<g class="cuffx"><rect width="640" height="400" fill="#fff" class="flash"/><g class="cl"><circle cx="270" cy="200" r="46" fill="none" stroke="#dfe5ee" stroke-width="14"/><circle cx="270" cy="200" r="46" fill="none" stroke="#2b1b2e" stroke-width="2"/></g><g class="cr"><circle cx="370" cy="200" r="46" fill="none" stroke="#dfe5ee" stroke-width="14"/><circle cx="370" cy="200" r="46" fill="none" stroke="#2b1b2e" stroke-width="2"/></g><path class="cc" d="M316 200 h8" stroke="#aab3c0" stroke-width="10"/></g>`; setTimeout(() => { fxG.innerHTML = ''; }, 1700); }
async function runCmd(c){
  const a = c.a;
  switch (c.cmd){
    case 'bg': if (curBg !== a[0]){ setPlace(''); textEl.textContent = ''; nameEl.hidden = true; } await setBg(a[0]); break;
    case 'bgm': AudioSys.bgm(a[0]); break;
    case 'sfx': AudioSys.sfx(a[0]); if (a[0] === 'shock'){ stage.classList.remove('quake'); void stage.getBoundingClientRect(); stage.classList.add('quake'); } break;
    case 'card': await card(a.join(' ')); break;
    case 'show': showChar(a[0], a[1] || 'center'); break;
    case 'hide': hideChar(a[0]); break;
    case 'tel': tel = a[0] === 'off' ? null : a[0]; break;
    case 'get': await getEv(a[0]); break;
    case 'flag': st.flags.add(a[0]); break;
    case 'wait': await sleep(st.fast ? 20 : +a[0]); break;
    case 'obj': setObj(a[0], a[1]); await sleep(st.fast ? 20 : a[0] === 'tejou' ? 900 : 350); break;
    default: console.warn('unknown command', c.cmd);
  }
}
async function say(who, e, text){
  mode = 'dialog'; menu.innerHTML = ''; dialog.hidden = false; dialog.classList.remove('short');
  const narr = who === '*', c = CHARS[who]; if (!narr && !c){ console.warn('no char', who); return; }
  if (!narr && !c.noart && who !== tel && !findCh(who).length){ const used = $$('.slot').map(s => s.dataset.pos); const pos = who === 'tsubasa' ? (used.includes('left') ? 'right' : 'left') : ['center', 'left', 'right'].find(p => !used.includes(p)) || 'left'; showChar(who, pos); autoSlots.push(who); }
  setSpeaker(who, e);
  nameEl.textContent = narr ? '' : c.name + (who === tel ? '（電話）' : ''); nameEl.hidden = narr; dialog.dataset.kind = narr ? 'narr' : who === 'tsubasa' ? 'me' : 'npc';
  st.log.push([narr ? '' : c.name, text]); if (st.log.length > 80) st.log.shift();
  let dur = 0; if (!narr && !st.fast) dur = await AudioSys.speak(who, text);
  talkId = narr ? null : who; typingNow = true; nextEl.hidden = true; textEl.textContent = '';
  let skipped = false; const tp = waitTap().then(() => { skipped = true; });
  const per = st.fast ? 0 : dur > 0 ? Math.max(16, Math.min(70, dur * 850 / text.length)) : st.speed;
  for (let i = 1; i <= text.length && !skipped && per > 0; i++){ textEl.textContent = text.slice(0, i); if (!dur && i % 3 === 1) AudioSys.sfx('tick'); await sleep(per); }
  textEl.textContent = text; typingNow = false; nextEl.hidden = false;
  if (st.fast){ tapRes = null; await sleep(20); }
  else if (st.auto){ const rest = Math.max(700, dur * 1000 - text.length * per + 500); if (skipped) await Promise.race([waitTap(), sleep(rest)]); else await Promise.race([tp, sleep(rest)]); tapRes = null; }
  else if (skipped) await waitTap(); else await tp;
  AudioSys.stopVoice(); talkId = null; nextEl.hidden = true;
}
const narr = t => say('*', 'n', t);
async function play(id){
  const blk = STORY[id]; if (!blk){ console.warn('no block', id); return; }
  for (const it of blk){ if (it.cmd) await runCmd(it); else await say(it.who, it.e, it.t); }
  for (const a of autoSlots.slice()) hideChar(a); setSpeaker('*');
}
const resolve = b => typeof b === 'function' ? b(has) : b;
/* --- menus --- */
function choose(opts, o = {}){
  return new Promise(res => {
    mode = 'menu'; menu.innerHTML = ''; menu.className = o.cls || (opts.length > 3 ? 'two' : ''); dialog.hidden = !o.msg; dialog.classList.add('short');
    if (o.msg){ nameEl.hidden = true; dialog.dataset.kind = o.kind || 'narr'; textEl.textContent = o.msg; nextEl.hidden = true; }
    opts.forEach((op, i) => { const b = document.createElement('button'); b.className = 'opt' + (op.cls ? ' ' + op.cls : ''); b.innerHTML = `<span>${op.l}</span>${op.sub ? `<small>${op.sub}</small>` : ''}`; b.disabled = !!op.dis; b.dataset.i = i;
      b.onclick = () => { AudioSys.sfx(op.back ? 'back' : 'select'); menu.innerHTML = ''; res(op.back ? -1 : i); }; menu.appendChild(b); });
  });
}
function updHud(){ $('#b-ev').dataset.n = st.ev.length; }
function setPlace(t){ $('#place').textContent = t || ''; }
function setView(v){ st.view = v; const b = $('#viewbadge'); b.innerHTML = `<svg viewBox="30 0 170 170"><g class="ch mini" data-id="${v}">${charSVG(v)}</g></svg><span>${VIEWS[v].n}</span>`; applyExpr(b.querySelector('.ch'), 'n'); b.hidden = false; }
async function banner(t, sub){ const c = $('#cutin'); c.className = 'banner'; c.innerHTML = `<div class="bn">${t}</div>${sub ? `<div class="bs">${sub}</div>` : ''}`; c.hidden = false; AudioSys.sfx('cutin'); await sleep(st.fast ? 60 : 1400); c.hidden = true; }
async function cutin(txt, who = 'tsubasa'){ const c = $('#cutin'); c.className = 'eyes'; c.innerHTML = `<svg viewBox="62 84 124 46" preserveAspectRatio="xMidYMid slice"><rect x="-200" y="-200" width="800" height="800" fill="#ffd23a"/><g class="speed">${Array.from({ length: 14 }, (_, i) => `<path d="M${-40 + i * 9} ${70 + (i * 37) % 70} h${60 + (i * 13) % 50}" stroke="#fff" stroke-width="${1 + i % 3}" opacity=".8"/>`).join('')}</g><g class="ch" data-id="${who}">${charSVG(who)}</g></svg><div class="ct">${txt}</div>`; applyExpr(c.querySelector('.ch'), 'k'); c.hidden = false; AudioSys.sfx('cutin'); await sleep(st.fast ? 50 : 950); c.hidden = true; }
/* --- modals --- */
function modal(html, onReady){ const m = $('#modal'); m.innerHTML = `<div class="mbox">${html}<button class="mclose">とじる</button></div>`; m.hidden = false; m.querySelector('.mclose').onclick = () => { AudioSys.sfx('back'); m.hidden = true; }; if (onReady) onReady(m); }
function evList(pick){ return st.ev.map(id => EVID[id] ? `<button class="evrow" data-id="${id}" ${pick ? '' : 'disabled'}><span class="evk">${EVID[id].k}</span><span><b>${EVID[id].n}</b><small>${EVID[id].d}</small></span></button>` : '').join('') || '<p>まだ何もない。</p>'; }
$('#b-ev').onclick = () => { AudioSys.sfx('select'); modal(`<h2>証拠ファイル</h2><div class="evlist">${evList(false)}</div>`); };
$('#b-log').onclick = () => { AudioSys.sfx('select'); modal(`<h2>会話のログ</h2><div class="loglist">${st.log.map(l => `<p>${l[0] ? `<b>${l[0]}</b>` : ''}${l[1]}</p>`).join('')}</div>`, m => { const l = m.querySelector('.loglist'); l.scrollTop = l.scrollHeight; }); };
$('#b-set').onclick = () => { AudioSys.sfx('select'); modal(`<h2>設定</h2><div class="setlist">
  <label for="s-vm"><span>声の種類</span><select id="s-vm"><option value="game">ゲームの声</option><option value="device">この端末の声</option><option value="off">声なし</option></select></label>
  <label for="s-vo">声の大きさ<input id="s-vo" type="range" min="0" max="1" step="0.05" value="${AudioSys.vol.voice}"></label>
  <label for="s-bgm">音楽の大きさ<input id="s-bgm" type="range" min="0" max="1" step="0.05" value="${AudioSys.vol.bgm}"></label>
  <label for="s-se">効果音の大きさ<input id="s-se" type="range" min="0" max="1" step="0.05" value="${AudioSys.vol.se}"></label>
  <label for="s-auto"><span>オート（声が終わったら次へ）</span><input id="s-auto" type="checkbox" ${st.auto ? 'checked' : ''}></label>
  <label for="s-fast"><span>早送り（声なしで飛ばす）</span><input id="s-fast" type="checkbox" ${st.fast ? 'checked' : ''}></label>
  <button id="s-quit" class="opt back"><span>事件えらびにもどる</span></button></div>`, m => {
    m.querySelector('#s-vm').value = AudioSys.mode; m.querySelector('#s-vm').onchange = e => AudioSys.setMode(e.target.value);
    m.querySelector('#s-vo').oninput = e => AudioSys.setVol('voice', +e.target.value); m.querySelector('#s-bgm').oninput = e => AudioSys.setVol('bgm', +e.target.value); m.querySelector('#s-se').oninput = e => AudioSys.setVol('se', +e.target.value);
    m.querySelector('#s-auto').onchange = e => { st.auto = e.target.checked; }; m.querySelector('#s-fast').onchange = e => { st.fast = e.target.checked; if (st.fast) onTap(); };
    m.querySelector('#s-quit').onclick = () => location.reload(); }); };
function pickEvidence(){ return new Promise(res => { modal(`<h2>どの証拠を出す？</h2><div class="evlist">${evList(true)}</div>`, m => { m.querySelectorAll('.evrow').forEach(b => b.onclick = () => { AudioSys.sfx('select'); m.hidden = true; res(b.dataset.id); }); m.querySelector('.mclose').onclick = () => { AudioSys.sfx('back'); m.hidden = true; res(null); }; m.querySelector('.mclose').textContent = 'やめる'; }); }); }
/* --- investigation --- */
const needDone = P => P.need.every(has);
const needCount = P => P.need.filter(has).length;
function clearHs(){ hsG.innerHTML = ''; charsG.classList.remove('away'); }
function pickHotspot(P, key, L, withBack){
  return new Promise(res => {
    mode = 'hot'; hsG.innerHTML = ''; charsG.classList.add('away'); dialog.hidden = false; dialog.classList.add('short'); nameEl.hidden = true; dialog.dataset.kind = 'narr'; nextEl.hidden = true;
    textEl.textContent = P.simple ? '光っている所をタップ。' : `光っている所をタップ。うすい印は、ほかの人の視点で見える物。（いま：${VIEWS[st.view].n}）`;
    for (const h of L.hs){ const mine = h.v === 'any' || h.v === st.view, seen = st.seen.has(key + ':' + h.id) && !(h.done && !has(h.done)), [x, y, w, hh] = h.r;
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); g.setAttribute('class', 'hot' + (mine ? '' : ' ghost') + (seen ? ' seen' : '')); g.dataset.id = h.id;
      g.innerHTML = `<rect x="${x}" y="${y}" width="${w}" height="${hh}" rx="10"/><g transform="translate(${x + w / 2} ${y + hh / 2})"><circle r="15" class="ring"/><circle r="9" class="dot"/><text y="4.5" text-anchor="middle">${mine ? (seen ? '✓' : '！') : VIEWS[h.v].n[0]}</text></g><text class="hl" x="${Math.min(590, Math.max(50, x + w / 2))}" y="${Math.max(14, y - 5)}" text-anchor="middle">${h.l}</text>`;
      g.onclick = ev => { ev.stopPropagation(); AudioSys.sfx('select'); clearHs(); menu.innerHTML = ''; res(mine ? h : { ghost: h }); }; hsG.appendChild(g); }
    menu.innerHTML = ''; menu.className = '';
    if (withBack){ const b = document.createElement('button'); b.className = 'opt back'; b.innerHTML = '<span>もどる</span>'; b.onclick = () => { AudioSys.sfx('back'); clearHs(); menu.innerHTML = ''; res(null); }; menu.appendChild(b); }
  });
}
async function runHs(key, h){ st.seen.add(key + ':' + h.id); await play(resolve(h.b)); if (h.f) st.flags.add(h.f); }
function showPeople(L){ hideChar('all'); const ps = (L.people || []).filter(p => !bg.querySelector(`.mini[data-id="${p}"]`)).slice(0, 3), pos = ps.length === 1 ? ['center'] : ps.length === 2 ? ['left', 'right'] : ['left', 'center', 'right']; ps.forEach((p, i) => showChar(p, pos[i])); setSpeaker('*'); }
async function enterLoc(P, key, id, first){
  const L = P.locs[id]; st.loc = id; await setBg(L.bg); for (const k in L.objs) setObj(k, L.objs[k]);
  setPlace(L.n); if (!first) await card(L.n); showPeople(L);
  if (L.enter && !st.flags.has(L.enter[0])){ st.flags.add(L.enter[0]); await runFlow(C.flows[L.enter[1]], 0, false); await setBg(L.bg); for (const k in L.objs) setObj(k, L.objs[k]); setPlace(L.n); showPeople(L); }
}
async function investigate(key){
  const P = C.places[key]; let id = P.start; await enterLoc(P, key, id, true);
  if (P.simple){ while (!needDone(P)){ const h = await pickHotspot(P, key, P.locs[id], false); await runHs(key, h); showPeople(P.locs[id]); } clearHs(); return; }
  if (!VIEWS[st.view]) st.view = Object.keys(VIEWS)[0]; setView(st.view);
  for (;;){
    const L = P.locs[id];
    if (needDone(P)){ await narr('手がかりが、そろった。'); break; }
    showPeople(L);
    const i = await choose([{ l: '調べる', sub: '物を見る' }, { l: '話す', sub: '人に聞く' }, { l: '移動', sub: '場所を変える' }, { l: '視点', sub: VIEWS[st.view].n + 'から代わる' }], { cls: 'grid', msg: `${L.n}。手がかり ${needCount(P)} / ${P.need.length}` });
    if (i === 0){ if (!L.hs.length){ await narr('ここには、調べる物がない。'); continue; } for (;;){ const h = await pickHotspot(P, key, L, true); if (!h) break; if (h.ghost) await narr(`${VIEWS[h.ghost.v].n}の視点なら、何か分かりそうだ。`); else { await runHs(key, h); if (needDone(P)) break; } } }
    else if (i === 1){
      const ts = L.talk; if (!ts.length){ await narr('ここには、話を聞ける人がいない。'); continue; }
      const ok = T => T.v === 'any' || T.v === st.view, whos = [...new Set(ts.map(t => t.who))], mine = w => ts.filter(t => t.who === w && ok(t)), other = w => ts.find(t => t.who === w && !ok(t));
      const j = await choose(whos.map(w => ({ l: CHARS[w].name, sub: mine(w).length ? (other(w) ? VIEWS[other(w).v].n + 'なら、ほかの話も聞ける' : '') : VIEWS[other(w).v].n + 'の視点で聞ける', cls: mine(w).length ? '' : 'ghost' })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: '誰に聞く？' });
      if (j < 0) continue; const who = whos[j];
      if (!mine(who).length){ await narr(`${VIEWS[other(who).v].n}になら、話してくれそうだ。「視点」で代わろう。`); continue; }
      if (!bg.querySelector(`.mini[data-id="${who}"]`)){ hideChar('all'); showChar(who, 'center'); }
      for (;;){ const tps = mine(who).flatMap(T => T.tp).filter(t => !t.cond || has(t.cond)); if (!tps.length){ await narr('いまは、聞ける事がない。'); break; }
        const k = await choose(tps.map(t => ({ l: t.l, cls: st.seen.has(key + ':' + who + ':' + t.l) && !t.rep ? 'seen' : '' })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: CHARS[who].name + 'に聞く。' });
        if (k < 0) break; const t = tps[k]; st.seen.add(key + ':' + who + ':' + t.l); await play(resolve(t.b)); if (t.f) st.flags.add(t.f); if (needDone(P)) break; if (!findCh(who).length && !CHARS[who].noart) showChar(who, 'center'); }
    }
    else if (i === 2){ const ls = Object.keys(P.locs).filter(k => !P.locs[k].cond || has(P.locs[k].cond)); if (ls.length < 2){ await narr('いまは、ここを調べよう。'); continue; } const j = await choose(ls.map(k => ({ l: P.locs[k].n, dis: k === id, sub: k === id ? 'いまここ' : '' })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: 'どこへ行く？' }); if (j >= 0){ id = ls[j]; await enterLoc(P, key, id, false); } }
    else if (i === 3){ const vs = Object.keys(VIEWS); const j = await choose(vs.map(v => ({ l: VIEWS[v].n, sub: VIEWS[v].d, dis: v === st.view })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: '誰の視点で見る？' }); if (j >= 0){ setView(vs[j]); await banner('視点チェンジ', VIEWS[vs[j]].n + '：' + VIEWS[vs[j]].d); } }
  }
  clearHs(); $('#viewbadge').hidden = true;
}
/* --- showdown --- */
let focus = 5;
function drawBhud(B, i){ const h = $('#bhud'); h.hidden = false; h.innerHTML = `<div class="wall"><span>${CHARS[B.foe].name}の言い分</span><div class="segs">${B.ph.map((_, k) => `<i class="${k < i ? 'broken' : ''}"></i>`).join('')}</div></div><div class="focus"><span>集中</span>${[0, 1, 2, 3, 4].map(k => `<b class="${k < focus ? 'on' : ''}"></b>`).join('')}</div>`; }
function lastLine(id){ const b = STORY[id].filter(x => x.who && x.who !== '*'); return b[b.length - 1]; }
async function observe(B, ph){
  return new Promise(res => {
    mode = 'hot'; hsG.innerHTML = ''; const slot = charsG.querySelector(`.slot[data-id="${B.foe}"]`), ch = slot ? slot.querySelector('.ch') : bg.querySelector(`.mini[data-id="${B.foe}"]`); ch.classList.add('tell-loop', 'tell-' + ph.a);
    dialog.hidden = false; nameEl.hidden = true; dialog.dataset.kind = 'narr'; textEl.textContent = '相手をよく見る。おかしな動きをする所をタップ。'; nextEl.hidden = true;
    const ox = slot ? POS[slot.dataset.pos] : 0, oy = slot ? CY : 0, zs = slot ? CS : 1, done = v => { hsG.innerHTML = ''; menu.innerHTML = ''; ch.classList.remove('tell-loop', 'tell-' + ph.a); res(v); };
    for (const z of ph.z){ const [x, y, w, h] = z.r.map(v => v * zs); const g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); g.setAttribute('class', 'zone'); g.dataset.id = z.id; g.innerHTML = `<rect x="${ox + x}" y="${oy + y}" width="${w}" height="${h}" rx="8"/><text x="${ox + x + w + 6}" y="${oy + y + h / 2 + 5}">${z.l}</text>`;
      g.onclick = ev => { ev.stopPropagation(); AudioSys.sfx('select'); done(z.id); }; hsG.appendChild(g); }
    menu.innerHTML = ''; const b = document.createElement('button'); b.className = 'opt back'; b.innerHTML = '<span>やめる</span>'; b.onclick = () => { AudioSys.sfx('back'); done(null); }; menu.appendChild(b);
  });
}
async function battle(key){
  const B = C.battles[key]; await setBg(B.bg); hideChar('all'); if (!bg.querySelector(`.mini[data-id="${B.foe}"]`)) showChar(B.foe, 'center'); setPlace('追及'); $('#viewbadge').hidden = true; focus = 5;
  AudioSys.bgm('battle'); await banner('追及', B.title);
  const vs = Object.keys(VIEWS).filter(v => v !== 'tsubasa');
  for (let i = 0; i < B.ph.length; i++){
    const ph = B.ph[i]; window.__ph = ph; drawBhud(B, i); await play(ph.c); const claim = lastLine(ph.c);
    for (let ok = false; !ok;){
      drawBhud(B, i); if (!bg.querySelector(`.mini[data-id="${B.foe}"]`)) showChar(B.foe, 'center'); setSpeaker('*');
      const c = await choose([{ l: '証拠', sub: '物を出す' }, { l: '推理', sub: '答えを言う' }, { l: '視点', sub: '仲間に代わる' }, { l: '観察', sub: '動きを見る' }, { l: 'ヒント', cls: 'hint' }], { cls: 'grid battle', msg: `${CHARS[claim.who].name}「${claim.t}」`, kind: 'claim' });
      let res = null;
      if (c === 0){ const e = await pickEvidence(); if (e) res = ph.t === 'ev' && e === ph.a; }
      else if (c === 1){ if (ph.t !== 'ded') await narr('まだ、言い切れる答えがない。物か、人の話か、相手の動きで崩そう。'); else { const j = await choose(ph.o.map(l => ({ l })).concat([{ l: 'やめる', back: 1, cls: 'back' }]), { msg: '何と言う？' }); if (j >= 0) res = j === ph.a; } }
      else if (c === 2){ if (!vs.length){ await narr('いまは、代われる仲間がいない。'); } else { const j = await choose(vs.map(v => ({ l: VIEWS[v].n, sub: VIEWS[v].d })).concat([{ l: 'やめる', back: 1, cls: 'back' }]), { msg: '誰に代わる？' }); if (j >= 0){ if (ph.t === 'view' && vs[j] === ph.a) res = true; else await narr(`${VIEWS[vs[j]].n}は、首を横に振った。いまは、出番ではないらしい。`); } } }
      else if (c === 3){ if (ph.t !== 'obs') await narr('相手の動きに、変わった所は見えない。'); else { const z = await observe(B, ph); if (z) res = z === ph.a; } }
      else { st.hints++; await narr('ヒント：' + ph.h); }
      if (res === true){ await cutin(ph.t === 'view' ? 'たのむ！' : ph.t === 'obs' ? '見えた！' : 'そこだ！'); AudioSys.sfx('correct'); await play(ph.ok); AudioSys.sfx('wall'); drawBhud(B, i + 1); stage.classList.remove('quake'); void stage.getBoundingClientRect(); stage.classList.add('quake'); await sleep(st.fast ? 30 : 500); ok = true; }
      else if (res === false){ st.miss++; focus--; AudioSys.sfx('damage'); $('#app').classList.remove('hurt'); void $('#app').getBoundingClientRect(); $('#app').classList.add('hurt'); drawBhud(B, i); await play(B.miss[st.miss % B.miss.length]);
        if (focus <= 0){ st.retries++; focus = 5; await narr('集中が切れた。深呼吸して、もう1度、相手の言い分を聞く。'); } }
    }
  }
  $('#bhud').hidden = true; await play(B.end);
}
/* --- timeline puzzle --- */
async function timeline(key){
  const T = C.timelines[key], E = T.events, tl = $('#tl'); tl.hidden = false; const order = E.map((x, i) => i).sort(() => Math.random() - 0.5); let n = 0;
  const draw = () => { tl.innerHTML = `<h3>${T.title}</h3>` + E.slice(0, n).map(x => `<p><b>${x[1]}</b>${x[0]}</p>`).join('') + (n < E.length ? '<p class="q"><b>？</b>次に起きたのは</p>' : ''); };
  while (n < E.length){ draw(); const rem = [...new Set(order.filter(i => i >= n).map(i => E[i][0]))]; const j = await choose(rem.map(l => ({ l })), { msg: n === 0 ? '起きた順に選ぶ。最初に起きたのは？（「証拠」で日付や時刻を確かめられる）' : '次に起きたのは？' });
    if (rem[j] === E[n][0]){ AudioSys.sfx('select'); n++; } else { st.miss++; AudioSys.sfx('wrong'); await play(T.wrong); } }
  draw(); AudioSys.sfx('correct');
  for (const q of T.qs){ for (;;){ const j = await choose(q.o.map(l => ({ l })), { msg: q.m }); if (j === q.a){ AudioSys.sfx('correct'); break; } st.miss++; AudioSys.sfx('wrong'); await play(T.wrong); } }
  if (T.hit) tl.innerHTML += `<p class="hit"><b>${T.hit[1]}</b>${T.hit[0]}</p>`; await sleep(st.fast ? 40 : 1400); tl.hidden = true;
}
/* --- flow --- */
async function runFlow(F, from, top){
  for (let i = from; i < F.length; i++){
    const s = F[i];
    if (s.op === 'cp'){ if (top){ st.step = i; saveProgress(); setPlace(''); } }
    else if (s.op === 'play') await play(s.a);
    else if (s.op === 'inv') await investigate(s.a);
    else if (s.op === 'battle') await battle(s.a);
    else if (s.op === 'bg') await setBg(s.a);
    else if (s.op === 'flowx') await runFlow(C.flows[s.a], 0, false);
    else if (s.op === 'timeline') await timeline(s.a);
    else if (s.op === 'banner'){ hideChar('all'); await banner(s.a, s.b); }
    else if (s.op === 'ask'){ const j = await choose(s.opts.map(o => ({ l: o.l, cls: o.angry ? 'angry' : '' })), { msg: s.msg }); if (s.opts[j].b) await play(s.opts[j].b); }
  }
}
async function runCase(id, resume){
  C = CASES[id]; STORY = C.story; EVID = C.evid; VIEWS = Object.keys(C.views).length ? C.views : CAST.views; Object.assign(CHARS, C.chars);
  st.flags = new Set(resume ? resume.flags : []); st.ev = resume ? resume.ev.slice() : (C.meta.have ? C.meta.have.split(',') : []); st.seen = new Set(resume ? resume.seen : []); st.miss = resume ? resume.miss : 0; st.hints = resume ? resume.hints : 0; st.retries = resume ? resume.retries : 0; st.view = 'tsubasa'; st.log = []; curBg = null; updHud();
  await AudioSys.loadPack(`voice-${id}.mp3`, VOICE_INDEX[id]);
  $('#title').hidden = true;
  await runFlow(C.flows.main, resume ? resume.step : 0, true);
  const sc = st.miss + st.hints * 0.5 + st.retries * 2, rank = sc <= 1 ? 'S' : sc <= 4 ? 'A' : 'B';
  const s = loadStore(); s.cleared = s.cleared || {}; const old = s.cleared[id]; if (!old || 'SAB'.indexOf(rank) < 'SAB'.indexOf(old)) s.cleared[id] = rank; delete s.cur; putStore(s);
  AudioSys.bgm('truth'); $('#bhud').hidden = true;
  const r = $('#result'); r.innerHTML = `<div class="rbox"><div class="rf">FILE ${id}　${C.title}</div><div class="rs">解決</div><div class="rank rank-${rank}">${rank}</div><div class="rd">まちがい ${st.miss} 回　／　ヒント ${st.hints} 回</div><p class="rc">${C.end[rank] || ''}</p><p class="rn">${C.meta.next || ''}</p><button id="again" class="opt"><span>事件えらびへ</span></button><p class="credit">${CREDIT}</p></div>`; r.hidden = false;
  $('#again').onclick = () => location.reload();
}
const CREDIT = '声：Open JTalk と HTS voice "Mei"（MMDAgent Project Team）、"NIT ATR503 M001"（HTS Working Group）。どちらも © Nagoya Institute of Technology、CC BY 3.0。加工して使っています。物語と人物は架空です。';
/* --- title and case select --- */
function boot(){
  requestAnimationFrame(tick); bg.innerHTML = SCENES.rouka(); curBg = 'rouka';
  const tv = $('#titlechar'); tv.innerHTML = `<svg viewBox="0 -20 240 380"><g class="ch" data-id="tsubasa">${charSVG('tsubasa')}</g></svg>`; applyExpr(tv.querySelector('.ch'), 'k');
  const s = loadStore(), cleared = s.cleared || {}, list = $('#caselist');
  const open = id => { const i = CASE_IDS.indexOf(id); return i === 0 || !!cleared[CASE_IDS[i - 1]] || !!cleared[id] || $('#t-free').checked; };
  const start = async (id, resume) => { AudioSys.init(); $('#t-load').hidden = false; list.hidden = true; await runCase(id, resume); };
  const draw = () => { list.innerHTML = CASE_IDS.map(id => { const c = CASES[id], ok = open(id), cur = s.cur && s.cur.id === id; return `<button class="case${ok ? '' : ' locked'}" data-id="${id}" ${ok ? '' : 'disabled'}><span class="cn">FILE ${id}</span><b>${ok ? c.title : '？？？'}</b><small>${ok ? (c.meta.intro || '') : '前の事件を解くと開く'}</small>${cleared[id] ? `<i class="rk rk-${cleared[id]}">${cleared[id]}</i>` : ''}${cur ? '<em>つづきから</em>' : ''}</button>`; }).join('');
    list.querySelectorAll('.case').forEach(b => b.onclick = () => { const id = b.dataset.id; if (s.cur && s.cur.id === id) start(id, s.cur); else start(id, null); }); };
  $('#t-free').onchange = draw; draw();
}
boot();
