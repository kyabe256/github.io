/* ---------- engine ---------- */
const $ = s => document.querySelector(s), $$ = s => Array.from(document.querySelectorAll(s));
const sleep = ms => new Promise(r => setTimeout(r, ms));
function parseStory(txt){ const B = {}; let cur = null; for (const ln of txt.split('\n')){ if (!ln.trim()) continue; let m; if ((m = ln.match(/^## (\w+)/))){ cur = B[m[1]] = []; continue; } if (!cur) continue; if (ln[0] === '@'){ const p = ln.slice(1).split(' '); cur.push({ cmd: p[0], a: p.slice(1) }); continue; } if ((m = ln.match(/^\*: (.+)$/))){ cur.push({ who: '*', t: m[1] }); continue; } if ((m = ln.match(/^([a-z]+)(?:\.([a-z]))?: (.+)$/))) cur.push({ who: m[1], e: m[2] || 'n', t: m[3] }); } return B; }
const STORY = parseStory(STORY_TXT);
const st = { flags: new Set(), ev: [], seen: new Set(), view: 'tsubasa', loc: null, miss: 0, hints: 0, retries: 0, cp: 'pro', log: [], auto: false, fast: false, speed: 34 };
const S = { has: k => st.ev.includes(k) || st.flags.has(k) };
const has = k => k.startsWith('f:') ? st.flags.has(k.slice(2)) : st.ev.includes(k);
const SAVE_KEY = 'soukan-tsubasa-file001';
function save(cp){ st.cp = cp; try { localStorage.setItem(SAVE_KEY, JSON.stringify({ cp, flags: [...st.flags], ev: st.ev, seen: [...st.seen], miss: st.miss, hints: st.hints, retries: st.retries })); } catch (e) {} }
function loadSave(){ try { return JSON.parse(localStorage.getItem(SAVE_KEY) || 'null'); } catch (e) { return null; } }
const stage = $('#stage'), bg = $('#bg'), charsG = $('#chars'), hsG = $('#hs'), fxG = $('#fx');
const dialog = $('#dialog'), nameEl = $('#name'), textEl = $('#text'), nextEl = $('#next'), menu = $('#menu');
let tapRes = null, talkId = null, typingNow = false, mode = 'dialog', tel = null, curBg = null, autoSlots = [];
const waitTap = () => new Promise(r => { tapRes = r; });
function onTap(){ if (tapRes){ const r = tapRes; tapRes = null; r(); } }
dialog.addEventListener('click', onTap);
stage.addEventListener('click', () => { if (mode === 'dialog') onTap(); });
$('#card').addEventListener('click', onTap); $('#getpop').addEventListener('click', onTap);
document.addEventListener('keydown', e => { if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('button,input')){ e.preventDefault(); onTap(); } });

/* --- characters on stage --- */
const CS = 0.84, CY = 400 - 360 * CS + 4, POS = { left: 150 - 120 * CS, center: 320 - 120 * CS, right: 490 - 120 * CS };
function findCh(id){ return $$(`.ch[data-id="${id}"]`); }
function showChar(id, pos = 'center'){
  const c = CHARS[id]; if (!c || c.noart) return;
  let s = charsG.querySelector(`.slot[data-id="${id}"]`);
  if (!s){ s = document.createElementNS('http://www.w3.org/2000/svg', 'g'); s.setAttribute('class', 'slot'); s.dataset.id = id;
    s.innerHTML = `<g class="slot-in">${c.remote ? '<rect x="14" y="-8" width="212" height="372" rx="12" fill="#17344f" stroke="#7fd0ff" stroke-width="3"/><text x="120" y="12" font-size="12" fill="#7fd0ff" text-anchor="middle" font-family="monospace">● LIVE</text>' : ''}<g class="ch" data-id="${id}">${charSVG(id)}</g></g>`;
    charsG.appendChild(s); applyExpr(s.querySelector('.ch'), 'n'); }
  for (const o of $$('.slot')) if (o !== s && o.dataset.pos === pos){ o.remove(); autoSlots = autoSlots.filter(x => x !== o.dataset.id); }
  s.dataset.pos = pos; s.setAttribute('transform', `translate(${POS[pos]} ${CY}) scale(${CS})`);
}
function hideChar(id){ if (id === 'all'){ charsG.innerHTML = ''; autoSlots = []; return; } const s = charsG.querySelector(`.slot[data-id="${id}"]`); if (s) s.remove(); autoSlots = autoSlots.filter(x => x !== id); }
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
    const hr = Math.sin(t * 0.8 + ph) * 1.3, hy = Math.sin(t * 1.7 + ph + 0.6) * 0.9 + (talk && open > 0.1 ? Math.sin(t * 10) * 0.9 : 0);
    if (head) head.style.transform = `translateY(${hy.toFixed(2)}px) rotate(${hr.toFixed(2)}deg)`;
    if (hb) hb.style.transform = `translateY(${hy.toFixed(2)}px) rotate(${(hr * 1.5).toFixed(2)}deg)`;
  }
  const tm = bg.querySelector('.timer'); if (tm){ const left = Math.max(0, 46 * 3600 + 19 * 60 + 58 - Math.floor(t)); tm.textContent = [Math.floor(left / 3600), Math.floor(left / 60) % 60, left % 60].map(v => String(v).padStart(2, '0')).join(':'); }
  requestAnimationFrame(tick);
}
/* --- stage commands --- */
async function setBg(id){
  if (curBg === id) return; const f = $('#fade'); f.classList.add('on'); await sleep(st.fast ? 60 : 260);
  bg.innerHTML = SCENES[id](); for (const a of [...bg.attributes]) if (a.name.startsWith('data-')) bg.removeAttribute(a.name);
  bg.dataset.scene = id; curBg = id; for (const g of bg.querySelectorAll('.ch')) applyExpr(g, 'n');
  if (id === 'kouhei' && st.ev.includes('tejou')) bg.dataset.tsutsumi = 'open';
  hideChar('all'); f.classList.remove('on'); await sleep(st.fast ? 30 : 160);
}
async function card(txt){ const [a, b] = txt.split('｜'); const c = $('#card'); c.innerHTML = `<div class="c1">${a}</div>${b ? `<div class="c2">${b}</div>` : ''}`; c.hidden = false; AudioSys.sfx('card'); await Promise.race([sleep(st.fast ? 200 : 1900), waitTap()]); tapRes = null; c.hidden = true; }
async function getEv(id){
  if (st.ev.includes(id)) return; st.ev.push(id); const e = EVID[id]; AudioSys.sfx('get');
  const p = $('#getpop'); p.innerHTML = `<div class="gp-h">証拠ファイルに追加</div><div class="gp-b"><span class="evk">${e.k}</span><div><b>${e.n}</b><p>${e.d}</p></div></div>`; p.hidden = false;
  await Promise.race([waitTap(), sleep(st.fast ? 150 : 600000)]); tapRes = null; p.hidden = true; updHud();
}
function fxCuffs(){ fxG.innerHTML = `<g class="cuffx"><rect width="640" height="400" fill="#fff" class="flash"/><g class="cl"><circle cx="270" cy="200" r="46" fill="none" stroke="#dfe5ee" stroke-width="14"/><circle cx="270" cy="200" r="46" fill="none" stroke="#fff" stroke-width="3"/></g><g class="cr"><circle cx="370" cy="200" r="46" fill="none" stroke="#dfe5ee" stroke-width="14"/><circle cx="370" cy="200" r="46" fill="none" stroke="#fff" stroke-width="3"/></g><path class="cc" d="M316 200 h8" stroke="#aab3c0" stroke-width="10"/></g>`; setTimeout(() => { fxG.innerHTML = ''; }, 1700); }
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
    case 'wait': await sleep(st.fast ? 20 : +a[0]); break;
    case 'obj':
      if (a[0] === 'tejou'){ fxCuffs(); await sleep(st.fast ? 50 : 900); }
      else if (a[0] === 'tell'){ for (const g of findCh('hori')){ g.classList.remove('tell'); void g.getBoundingClientRect(); g.classList.add('tell'); } }
      else { bg.setAttribute('data-' + a[0], ''); void bg.getBoundingClientRect(); bg.setAttribute('data-' + a[0], a[1]); await sleep(st.fast ? 20 : 350); }
      break;
  }
}
async function say(who, e, text){
  mode = 'dialog'; menu.innerHTML = ''; dialog.hidden = false; dialog.classList.remove('short');
  const narr = who === '*', c = CHARS[who];
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
  if (st.fast){ tapRes = null; await sleep(25); }
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
function setView(v){ st.view = v; const b = $('#viewbadge'); b.innerHTML = `<svg viewBox="40 34 160 150"><g class="ch mini" data-id="${v}">${charSVG(v)}</g></svg><span>${VIEWS[v].n}</span>`; applyExpr(b.querySelector('.ch'), 'n'); b.hidden = false; }
async function banner(t, sub){ const c = $('#cutin'); c.className = 'banner'; c.innerHTML = `<div class="bn">${t}</div>${sub ? `<div class="bs">${sub}</div>` : ''}`; c.hidden = false; AudioSys.sfx('cutin'); await sleep(st.fast ? 80 : 1300); c.hidden = true; }
async function cutin(txt){ const c = $('#cutin'); c.className = 'eyes'; c.innerHTML = `<svg viewBox="52 118 136 46" preserveAspectRatio="xMidYMid slice"><rect x="0" y="0" width="240" height="340" fill="#ffd23a"/><g class="ch" data-id="tsubasa">${charSVG('tsubasa')}</g></svg><div class="ct">${txt}</div>`; applyExpr(c.querySelector('.ch'), 'k'); c.hidden = false; AudioSys.sfx('cutin'); await sleep(st.fast ? 60 : 950); c.hidden = true; }
/* --- modals --- */
function modal(html, onReady){ const m = $('#modal'); m.innerHTML = `<div class="mbox">${html}<button class="mclose">とじる</button></div>`; m.hidden = false; m.querySelector('.mclose').onclick = () => { AudioSys.sfx('back'); m.hidden = true; }; if (onReady) onReady(m); }
function evList(pick){ return st.ev.map(id => `<button class="evrow" data-id="${id}" ${pick ? '' : 'disabled'}><span class="evk">${EVID[id].k}</span><span><b>${EVID[id].n}</b><small>${EVID[id].d}</small></span></button>`).join('') || '<p>まだ何もない。</p>'; }
$('#b-ev').onclick = () => { AudioSys.sfx('select'); modal(`<h2>証拠ファイル</h2><div class="evlist">${evList(false)}</div>`); };
$('#b-log').onclick = () => { AudioSys.sfx('select'); modal(`<h2>会話のログ</h2><div class="loglist">${st.log.map(l => `<p>${l[0] ? `<b>${l[0]}</b>` : ''}${l[1]}</p>`).join('')}</div>`, m => { const l = m.querySelector('.loglist'); l.scrollTop = l.scrollHeight; }); };
$('#b-set').onclick = () => { AudioSys.sfx('select'); modal(`<h2>設定</h2><div class="setlist">
  <label for="s-vo">声の大きさ<input id="s-vo" type="range" min="0" max="1" step="0.05" value="${AudioSys.vol.voice}"></label>
  <label for="s-bgm">音楽の大きさ<input id="s-bgm" type="range" min="0" max="1" step="0.05" value="${AudioSys.vol.bgm}"></label>
  <label for="s-se">効果音の大きさ<input id="s-se" type="range" min="0" max="1" step="0.05" value="${AudioSys.vol.se}"></label>
  <label for="s-auto"><span>オート（声が終わったら次へ）</span><input id="s-auto" type="checkbox" ${st.auto ? 'checked' : ''}></label>
  <label for="s-fast"><span>早送り（声なしで飛ばす）</span><input id="s-fast" type="checkbox" ${st.fast ? 'checked' : ''}></label></div>`, m => {
    m.querySelector('#s-vo').oninput = e => AudioSys.setVol('voice', +e.target.value); m.querySelector('#s-bgm').oninput = e => AudioSys.setVol('bgm', +e.target.value); m.querySelector('#s-se').oninput = e => AudioSys.setVol('se', +e.target.value);
    m.querySelector('#s-auto').onchange = e => { st.auto = e.target.checked; }; m.querySelector('#s-fast').onchange = e => { st.fast = e.target.checked; if (st.fast) onTap(); }; }); };
function pickEvidence(){ return new Promise(res => { modal(`<h2>どの証拠を出す？</h2><div class="evlist">${evList(true)}</div>`, m => { m.querySelectorAll('.evrow').forEach(b => b.onclick = () => { AudioSys.sfx('select'); m.hidden = true; res(b.dataset.id); }); m.querySelector('.mclose').onclick = () => { AudioSys.sfx('back'); m.hidden = true; res(null); }; m.querySelector('.mclose').textContent = 'やめる'; }); }); }
/* --- investigation --- */
const needDone = P => P.need.every(has);
const needCount = P => P.need.filter(has).length;
function clearHs(){ hsG.innerHTML = ''; charsG.classList.remove('away'); }
function pickHotspot(P, key, L, withBack){
  return new Promise(res => {
    mode = 'hot'; hsG.innerHTML = ''; charsG.classList.add('away'); dialog.hidden = false; nameEl.hidden = true; dialog.dataset.kind = 'narr'; nextEl.hidden = true;
    textEl.textContent = P.simple ? '光っている所をタップ。' : `光っている所をタップ。うすい印は、ほかの視点で見える物。（いま：${VIEWS[st.view].n}）`;
    for (const h of L.hs){ const mine = h.v === 'any' || h.v === st.view, seen = st.seen.has(key + ':' + h.id) && !(h.done && !has(h.done)), [x, y, w, hh] = h.r;
      const g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); g.setAttribute('class', 'hot' + (mine ? '' : ' ghost') + (seen ? ' seen' : '')); g.dataset.id = h.id;
      g.innerHTML = `<rect x="${x}" y="${y}" width="${w}" height="${hh}" rx="10"/><g transform="translate(${x + w / 2} ${y + hh / 2})"><circle r="15" class="ring"/><circle r="9" class="dot"/><text y="4.5" text-anchor="middle">${mine ? (seen ? '✓' : '！') : VIEWS[h.v].n[0]}</text></g><text class="hl" x="${x + w / 2}" y="${Math.max(14, y - 5)}" text-anchor="middle">${h.l}</text>`;
      g.onclick = ev => { ev.stopPropagation(); AudioSys.sfx('select'); clearHs(); menu.innerHTML = ''; res(mine ? h : { ghost: h }); }; hsG.appendChild(g); }
    menu.innerHTML = ''; menu.className = '';
    if (withBack){ const b = document.createElement('button'); b.className = 'opt back'; b.innerHTML = '<span>もどる</span>'; b.onclick = () => { AudioSys.sfx('back'); clearHs(); menu.innerHTML = ''; res(null); }; menu.appendChild(b); }
  });
}
async function runHs(key, h){ const b = typeof h.b === 'function' ? h.b(S) : h.b; st.seen.add(key + ':' + h.id); await play(b); if (h.f) st.flags.add(h.f); }
function showPeople(L){ hideChar('all'); const ps = (L.people || []).slice(0, 3), pos = ps.length === 1 ? ['center'] : ps.length === 2 ? ['left', 'right'] : ['left', 'center', 'right']; ps.forEach((p, i) => showChar(p, pos[i])); setSpeaker('*'); }
async function enterLoc(P, key, id, first){
  const L = P.locs[id]; st.loc = id; await setBg(L.bg); for (const k in (L.objs || {})) bg.setAttribute('data-' + k, L.objs[k]);
  setPlace(L.n); if (!first) await card(L.n); showPeople(L);
  if (L.enter === 'c2miss' && !st.flags.has('c2miss')){ st.flags.add('c2miss'); await play('c2_miss'); const i = await choose([{ l: 'すぐ言ってくれて、助かりました' }, { l: '大丈夫。時刻は、ほかの機械にも残ります' }, { l: '一番早く言ってくれた。それが大事です' }], { msg: '千早に、何と言う？' }); await play('c2_miss_' + 'abc'[i]); await play('c2_miss_after'); showPeople(L); }
}
async function investigate(key){
  const P = PLACES[key]; let id = P.locs[st.loc] && st.cp === key ? st.loc : P.start; await enterLoc(P, key, id, true);
  if (P.simple){ while (!needDone(P)){ const h = await pickHotspot(P, key, P.locs[id], false); await runHs(key, h); showPeople(P.locs[id]); } clearHs(); return; }
  setView(st.view);
  for (;;){
    const L = P.locs[id];
    if (needDone(P)){ await narr('手がかりが、そろった。'); break; }
    showPeople(L);
    const i = await choose([{ l: '調べる', sub: '物を見る' }, { l: '話す', sub: '人に聞く' }, { l: '移動', sub: '場所を変える' }, { l: '視点', sub: VIEWS[st.view].n + 'から代わる' }], { cls: 'grid', msg: `${L.n}。手がかり ${needCount(P)} / ${P.need.length}` });
    if (i === 0){ for (;;){ const h = await pickHotspot(P, key, L, true); if (!h) break; if (h.ghost) await narr(`${VIEWS[h.ghost.v].n}の視点なら、何か分かりそうだ。`); else { await runHs(key, h); if (needDone(P)) break; } } }
    else if (i === 1){
      const ts = L.talk || []; if (!ts.length){ await narr('ここには、話を聞ける人がいない。'); continue; }
      const j = await choose(ts.map(t => ({ l: CHARS[t.who].name, sub: t.v === 'any' || t.v === st.view ? '' : VIEWS[t.v].n + 'の視点で聞ける', cls: t.v === 'any' || t.v === st.view ? '' : 'ghost' })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: '誰に聞く？' });
      if (j < 0) continue; const T = ts[j];
      if (!(T.v === 'any' || T.v === st.view)){ await narr(`${VIEWS[T.v].n}になら、話してくれそうだ。「視点」で代わろう。`); continue; }
      if (!bg.querySelector(`.mini[data-id="${T.who}"]`)){ hideChar('all'); showChar(T.who, 'center'); }
      for (;;){ const tps = T.tp.filter(t => !t.cond || has(t.cond)); const k = await choose(tps.map(t => ({ l: t.l, cls: st.seen.has(key + ':' + T.who + ':' + t.l) && !t.rep ? 'seen' : '' })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: CHARS[T.who].name + 'に聞く。' });
        if (k < 0) break; const t = tps[k]; st.seen.add(key + ':' + T.who + ':' + t.l); await play(typeof t.b === 'function' ? t.b(S) : t.b); if (t.f) st.flags.add(t.f); if (needDone(P)) break; }
    }
    else if (i === 2){ const ls = Object.keys(P.locs).filter(k => !P.locs[k].cond || has(P.locs[k].cond)); const j = await choose(ls.map(k => ({ l: P.locs[k].n, dis: k === id, sub: k === id ? 'いまここ' : '' })).concat([{ l: 'もどる', back: 1, cls: 'back' }]), { msg: 'どこへ行く？' }); if (j >= 0){ id = ls[j]; await enterLoc(P, key, id, false); } }
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
    mode = 'hot'; hsG.innerHTML = ''; const slot = charsG.querySelector(`.slot[data-id="${B.foe}"]`), ch = slot.querySelector('.ch'); ch.classList.add('tell-loop');
    dialog.hidden = false; nameEl.hidden = true; dialog.dataset.kind = 'narr'; textEl.textContent = '相手をよく見る。おかしな動きをする所をタップ。'; nextEl.hidden = true;
    const ox = POS[slot.dataset.pos], oy = CY;
    for (const z of ph.z){ const [x, y, w, h] = z.r.map(v => v * CS); const g = document.createElementNS('http://www.w3.org/2000/svg', 'g'); g.setAttribute('class', 'zone'); g.innerHTML = `<rect x="${ox + x}" y="${oy + y}" width="${w}" height="${h}" rx="8"/><text x="${ox + x + w + 6}" y="${oy + y + h / 2 + 5}">${z.l}</text>`;
      g.onclick = ev => { ev.stopPropagation(); AudioSys.sfx('select'); hsG.innerHTML = ''; menu.innerHTML = ''; ch.classList.remove('tell-loop'); res(z.id); }; hsG.appendChild(g); }
    menu.innerHTML = ''; const b = document.createElement('button'); b.className = 'opt back'; b.innerHTML = '<span>やめる</span>'; b.onclick = () => { AudioSys.sfx('back'); hsG.innerHTML = ''; menu.innerHTML = ''; ch.classList.remove('tell-loop'); res(null); }; menu.appendChild(b);
  });
}
async function battle(key){
  const B = BATTLES[key]; await setBg(B.bg); hideChar('all'); showChar(B.foe, 'center'); setPlace('追及'); $('#viewbadge').hidden = true; focus = 5;
  AudioSys.bgm('battle'); await banner('追及', B.title);
  for (let i = 0; i < B.ph.length; i++){
    const ph = B.ph[i]; window.__ph = ph; drawBhud(B, i); await play(ph.c); const claim = lastLine(ph.c);
    for (let ok = false; !ok;){
      drawBhud(B, i); showChar(B.foe, 'center'); setSpeaker('*');
      const c = await choose([{ l: '証拠', sub: '物を出す' }, { l: '推理', sub: '答えを言う' }, { l: '視点', sub: '仲間に代わる' }, { l: '観察', sub: '動きを見る' }, { l: 'ヒント', cls: 'hint' }], { cls: 'grid battle', msg: `${CHARS[B.foe].name}「${claim.t}」`, kind: 'claim' });
      let res = null; // true = hit, false = miss, null = nothing
      if (c === 0){ const e = await pickEvidence(); if (e) res = ph.t === 'ev' && e === ph.a; }
      else if (c === 1){ if (ph.t !== 'ded') await narr('まだ、言い切れる答えがない。物か、人の話か、相手の動きで崩そう。'); else { const j = await choose(ph.o.map(l => ({ l })).concat([{ l: 'やめる', back: 1, cls: 'back' }]), { msg: '何と言う？' }); if (j >= 0) res = j === ph.a; } }
      else if (c === 2){ const vs = ['onodera', 'chihaya']; const j = await choose(vs.map(v => ({ l: VIEWS[v].n, sub: VIEWS[v].d })).concat([{ l: 'やめる', back: 1, cls: 'back' }]), { msg: '誰に代わる？' }); if (j >= 0){ if (ph.t === 'view' && vs[j] === ph.a) res = true; else await narr(`${VIEWS[vs[j]].n}は、首を横に振った。いまは、出番ではないらしい。`); } }
      else if (c === 3){ if (ph.t !== 'obs') await narr('相手の動きに、変わった所は見えない。'); else { const z = await observe(B, ph); if (z) res = z === ph.a; } }
      else { st.hints++; await narr('ヒント：' + ph.h); }
      if (res === true){ await cutin(ph.t === 'view' ? 'たのむ！' : 'そこだ！'); AudioSys.sfx('correct'); await play(ph.ok); AudioSys.sfx('wall'); drawBhud(B, i + 1); stage.classList.remove('quake'); void stage.getBoundingClientRect(); stage.classList.add('quake'); await sleep(st.fast ? 40 : 500); ok = true; }
      else if (res === false){ st.miss++; focus--; AudioSys.sfx('damage'); $('#app').classList.remove('hurt'); void $('#app').getBoundingClientRect(); $('#app').classList.add('hurt'); drawBhud(B, i); await play(B.miss[st.miss % 2]);
        if (focus <= 0){ st.retries++; focus = 5; await narr('集中が切れた。深呼吸して、もう1度、相手の言い分を聞く。'); } }
    }
  }
  $('#bhud').hidden = true; await play(B.end);
}
/* --- timeline puzzle --- */
async function timeline(){
  const tl = $('#tl'); tl.hidden = false; const left = TIMELINE.map((x, i) => i), order = left.slice().sort(() => Math.random() - 0.5); let n = 0;
  const draw = () => { tl.innerHTML = '<h3>あの夜の時刻表</h3>' + TIMELINE.slice(0, n).map(x => `<p><b>${x[1]}</b>${x[0]}</p>`).join('') + (n < TIMELINE.length ? '<p class="q"><b>？</b>次に起きたのは</p>' : ''); };
  while (n < TIMELINE.length){ draw(); const rem = order.filter(i => i >= n); const j = await choose(rem.map(i => ({ l: TIMELINE[i][0] })), { msg: n === 0 ? '起きた順に選ぶ。最初に起きたのは？（証拠ファイルで時刻を確かめられる）' : '次に起きたのは？' });
    if (rem[j] === n){ AudioSys.sfx('select'); n++; } else { st.miss++; AudioSys.sfx('wrong'); await play('c2_q_wrong'); } }
  draw(); AudioSys.sfx('correct');
  for (const q of [ { m: '錠前の回数計の「2回」は、時刻表のどこに入る？', o: ['22時14分より前', '記録の機械が止まった23時40分と、扉が止まった0時5分の間', '扉が止まった0時5分より後'], a: 1 }, { m: 'その2回、錠前を回したのは誰？', o: ['外から来た犯人', '管理者', '三浦部長、本人'], a: 2 } ]){
    for (;;){ const j = await choose(q.o.map(l => ({ l })), { msg: q.m }); if (j === q.a){ AudioSys.sfx('correct'); break; } st.miss++; AudioSys.sfx('wrong'); await play('c2_q_wrong'); } }
  tl.innerHTML += '<p class="hit"><b>23:42</b>三浦部長が、出て、戻る（2回）</p>'; await sleep(st.fast ? 50 : 1200); tl.hidden = true;
}
/* --- chapters --- */
const ORDER = ['pro', 'c1', 'b1', 'c2', 'b2', 'c3', 'b3', 'ep'];
const CHAP = {
  async pro(){ await play('pro_shop'); await investigate('pro'); await play('pro_takano'); await play('pro_brief'); await choose([{ l: '現場へ行きます' }], { msg: '翼は、どうする？' }); await play('pro_go'); hideChar('all'); await banner('FILE 001', '止まった病院'); },
  async c1(){ await play('c1_arrive'); await investigate('c1'); },
  async b1(){ await setBg('rouka'); await play('c1_prebattle'); await choose([{ l: '待ってください。筋が通りません' }], { msg: '翼は、どうする？' }); await play('c1_prebattle2'); await battle('b1'); },
  async c2(){ await play('c2_kasouken'); await investigate('c2'); },
  async b2(){ await setBg('kasouken'); await play('c2_think'); await timeline(); await play('c2_think_ok'); await play('c2_prebattle'); await battle('b2'); },
  async c3(){ await play('c3_brief'); await play('c3_maker'); await investigate('c3'); },
  async b3(){ await play('c3_prebattle'); await battle('b3');
    const i = await choose([{ l: '静かに告げる' }, { l: '鬼のように怒る', cls: 'angry' }], { msg: '翼は、堀に何と言う？' }); await play(i === 0 ? 'b3_calm' : 'b3_angry');
    await play('b3_arrest_q'); const j = await choose([{ l: '自分でかける（伯父の手錠）' }, { l: '鬼塚課長に任せる' }], { msg: '手錠は？' }); await play(j === 0 ? 'b3_arrest_self' : 'b3_arrest_oni'); await play('b3_last'); },
  async ep(){ await play('ep_hospital'); const i = await choose([{ l: '払わない。3日前のバックアップから戻す' }, { l: '払わない。交渉で時間を稼ぎながら戻す' }], { msg: '病院を、どうする？' }); await play(i === 0 ? 'ep_a' : 'ep_b'); await play('ep_hospital2'); await play('ep_shop'); await play('ep_hook'); }
};
async function run(cp){
  for (let i = Math.max(0, ORDER.indexOf(cp)); i < ORDER.length; i++){ save(ORDER[i]); setPlace(''); await CHAP[ORDER[i]](); st.loc = null; }
  try { localStorage.removeItem(SAVE_KEY); } catch (e) {}
  AudioSys.bgm('truth'); const sc = st.miss + st.hints * 0.5 + st.retries * 2, rank = sc <= 1 ? 'S' : sc <= 4 ? 'A' : 'B';
  const r = $('#result'); r.innerHTML = `<div class="rbox"><div class="rf">FILE 001　止まった病院</div><div class="rs">解決</div><div class="rank rank-${rank}">${rank}</div><div class="rd">まちがい ${st.miss} 回　／　ヒント ${st.hints} 回</div><p class="rc">${{ S: '耕平「……味噌汁、もう1杯だ。卵も焼く」', A: '鬼塚「総監。次も、一課は付き合いますよ」', B: '千早「総監、次は私も、もっと早く気づきます！」' }[rank]}</p><p class="rn">FILE 002「母の病院」につづく</p><button id="again" class="opt"><span>タイトルへ</span></button><p class="credit">声：Open JTalk と HTS voice "Mei"（© Nagoya Institute of Technology / MMDAgent Project Team, CC BY 3.0）を加工。物語と人物は架空です。</p></div>`; r.hidden = false;
  $('#again').onclick = () => location.reload();
}
/* --- title --- */
async function boot(){
  requestAnimationFrame(tick); bg.innerHTML = SCENES.rouka(); curBg = 'rouka';
  const tv = $('#titlechar'); tv.innerHTML = `<svg viewBox="0 -14 240 330"><g class="ch" data-id="tsubasa">${charSVG('tsubasa')}</g></svg>`; applyExpr(tv.querySelector('.ch'), 'k');
  const sv = loadSave(), bc = $('#t-cont'); bc.hidden = !sv || !sv.cp || sv.cp === 'pro';
  const start = async cp => { AudioSys.init(); $('#t-load').hidden = false; $('#t-btns').hidden = true; await AudioSys.loadPack(); $('#title').hidden = true; curBg = null; updHud(); run(cp); };
  $('#t-new').onclick = () => start('pro');
  bc.onclick = () => { st.flags = new Set(sv.flags); st.ev = sv.ev; st.seen = new Set(sv.seen); st.miss = sv.miss; st.hints = sv.hints; st.retries = sv.retries; st.cp = sv.cp; start(sv.cp); };
}
boot();
