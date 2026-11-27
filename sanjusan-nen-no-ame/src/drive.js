/* ---------- driving: a road seen through the windscreen. The car is on rails; it cannot crash. ----------
   One edge of the road graph is one stretch of road. The car cruises when "go" is on and stops by itself at the end. */
const DRIVE = (() => {
  const SEG = 200, CAMH = 1000, DEPTH = 0.9, DRAWN = 90;
  let cv, ctx, W = 800, H = 450, segs = [], pos = 0, speed = 0, go = false, laneX = 0, laneT = 0, kind = 'town', era = 2026, total = 0, raf = 0, last = 0, lite = false, fast = false, onEnd = null, onTick = null, running = false, wip = 0, t0 = 0, drops = [];
  const rr = (() => { let s = 7; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; })();
  function build(E, dir, e, k2){ era = e; kind = E.kind; segs = []; const n = E.len, cur = new Array(n).fill(0), hil = new Array(n).fill(0);
    for (const [a, b, c] of E.curve || []) for (let i = a; i < b; i++) cur[i] = c * Math.sin(Math.PI * (i - a) / (b - a));
    for (const [a, b, h] of E.hill || []) for (let i = a; i < b; i++) hil[i] = h * (1 - Math.cos(Math.PI * 2 * (i - a) / (b - a))) / 2;
    let y = 0; for (let j = 0; j < n + DRAWN; j++){ const i = Math.min(n - 1, j), src = dir > 0 ? i : n - 1 - i, c = (dir > 0 ? 1 : -1) * cur[src]; y = hil[src] * 60; const sp = [];
      if (j < n){ const kd = E.kind, den = kd === 'deep' ? 1 : kd === 'forest' ? 2 : 3;
        if (kd === 'forest' || kd === 'deep' || kd === 'hill'){ if (j % den === 0) sp.push(['tree', -1.5 - rr() * 2.2, .8 + rr() * .7]); if ((j + 1) % den === 0) sp.push(['tree', 1.5 + rr() * 2.2, .8 + rr() * .7]); if (kd === 'deep' && j % 2) sp.push(['tree', (rr() > .5 ? 1 : -1) * (3.5 + rr() * 2), 1.2]); }
        if (kd === 'town'){ if (j % 7 === 2) sp.push(['house', -2.3 - rr(), 1]); if (j % 7 === 5) sp.push(['house', 2.3 + rr(), 1]); if (j % 6 === 0) sp.push(['pole', 1.35, 1]); if (e !== 1960 && j % 12 === 3) sp.push(['lamp', -1.3, 1]); }
        if (kd === 'fence'){ if (j % 2 === 0) sp.push(['post', 1.4, 1]); if (j % 9 === 4) sp.push(['pole', -1.4, 1]); if (e !== 1960 && j % 14 === 7) sp.push(['lamp', 1.3, 1]); if (j % 11 === 0) sp.push(['tree', -2.6 - rr() * 2, .9]); }
        if (kd === 'hill' && e !== 1960 && j % 13 === 6) sp.push(['lamp', -1.3, 1]);
        if (j === n - 4) sp.push(['sign', 1.5, 1]); }
      segs.push({ c, y, sp, end: j >= n }); }
    total = n * SEG; pos = 0; speed = 0; go = false; laneX = 0; laneT = 0; }
  const COL = () => era === 1960 ? { road: '#3a332a', road2: '#40382e', edge: null, grass: '#171a15', grass2: '#1b1f19', mid: null } : { road: '#23272b', road2: '#272b30', edge: '#aab3b4', grass: kind === 'town' || kind === 'fence' ? '#1b2022' : '#131a17', grass2: kind === 'town' || kind === 'fence' ? '#1f2527' : '#17201c', mid: kind === 'deep' ? null : '#c9b56a' };
  function sprite(type, x, y, s, fog){ const c = ctx; c.globalAlpha = Math.max(0, 1 - fog * .85);
    if (type === 'tree'){ const h = 2600 * s, w = 150 * s; c.fillStyle = '#0d1412'; c.fillRect(x - w / 2, y - h, w, h); c.fillStyle = '#101a17'; for (let i = 0; i < 4; i++){ const yy = y - h * (.35 + i * .17), ww = 900 * s * (1 - i * .16); c.beginPath(); c.moveTo(x - ww / 2, yy); c.lineTo(x, yy - h * .3); c.lineTo(x + ww / 2, yy); c.fill(); } c.fillStyle = '#1c2a26'; c.fillRect(x + w * .2, y - h, w * .12, h); }
    else if (type === 'pole'){ const h = 1900 * s; c.fillStyle = '#17150f'; c.fillRect(x - 22 * s, y - h, 44 * s, h); c.fillRect(x - 150 * s, y - h + 90 * s, 300 * s, 26 * s); }
    else if (type === 'post'){ const h = 520 * s; c.fillStyle = '#4a5254'; c.fillRect(x - 12 * s, y - h, 24 * s, h); c.fillRect(x - 12 * s, y - h * .9, 420 * s, 12 * s); c.fillRect(x - 12 * s, y - h * .45, 420 * s, 12 * s); }
    else if (type === 'lamp'){ const h = 1500 * s; c.fillStyle = '#2a2e30'; c.fillRect(x - 16 * s, y - h, 32 * s, h); const lc = era === 1993 ? '255,190,90' : '225,240,255'; const g = c.createRadialGradient(x, y - h, 0, x, y - h, 700 * s); g.addColorStop(0, `rgba(${lc},.9)`); g.addColorStop(.25, `rgba(${lc},.3)`); g.addColorStop(1, `rgba(${lc},0)`); c.fillStyle = g; c.fillRect(x - 700 * s, y - h - 700 * s, 1400 * s, 1400 * s); }
    else if (type === 'house'){ const w = 1700 * s, h = 1100 * s; c.fillStyle = '#1a2024'; c.fillRect(x - w / 2, y - h, w, h); c.fillStyle = '#0f1316'; c.beginPath(); c.moveTo(x - w * .58, y - h); c.lineTo(x, y - h * 1.5); c.lineTo(x + w * .58, y - h); c.fill(); c.fillStyle = (Math.round(x * 7 + w) % 3) ? '#e9c377' : '#1d2a33'; c.fillRect(x - w * .3, y - h * .7, w * .22, h * .3); c.fillStyle = '#1d2a33'; c.fillRect(x + w * .1, y - h * .7, w * .22, h * .3); }
    else if (type === 'sign'){ const h = 900 * s; c.fillStyle = '#51585a'; c.fillRect(x - 12 * s, y - h, 24 * s, h); c.fillStyle = '#2f5a8a'; c.fillRect(x - 220 * s, y - h - 240 * s, 440 * s, 260 * s); c.fillStyle = '#e9ebe6'; c.fillRect(x - 160 * s, y - h - 130 * s, 320 * s, 30 * s); }
    c.globalAlpha = 1; }
  function frame(now){ if (!running) return; raf = requestAnimationFrame(frame); const dt = Math.min(.05, (now - last) / 1000 || 0); last = now; if (lite && (t0 = (t0 + 1) % 2)) { step(dt); return; } step(dt); draw(now / 1000); }
  function step(dt){ const vmax = (fast ? 60000 : 1900), tgt = go ? vmax : 0; speed += Math.max(-vmax * 1.6 * dt, Math.min(vmax * .8 * dt, tgt - speed)); if (pos > total - 1400 && go) speed = Math.min(speed, Math.max(260, (total - pos) * 1.3));
    pos += speed * dt; laneX += (laneT - laneX) * Math.min(1, dt * 2.2); wip += dt * (speed > 50 || true ? 1 : 0);
    if (pos >= total){ pos = total; speed = 0; go = false; const f = onEnd; if (f){ onEnd = null; f(); } } if (onTick) onTick(pos / total, speed, curveNow()); }
  const curveNow = () => { const s = segs[Math.min(segs.length - 1, Math.floor(pos / SEG))]; return s ? s.c : 0; };
  function draw(t){ const c = ctx, C = COL(), base = Math.floor(pos / SEG), frac = (pos % SEG) / SEG, roadW = kind === 'deep' ? 820 : 1150;
    const sky = c.createLinearGradient(0, 0, 0, H * .62); sky.addColorStop(0, '#0d1318'); sky.addColorStop(.7, '#26353a'); sky.addColorStop(1, '#4f6165'); c.fillStyle = sky; c.fillRect(0, 0, W, H);
    const bx = -((segs[base] ? segs[base].c : 0) * 40 + pos * .002) % 400; c.fillStyle = '#18242a'; c.beginPath(); c.moveTo(0, H * .6); for (let i = -1; i < 5; i++){ const x = bx + i * 400; c.lineTo(x + 120, H * .44); c.lineTo(x + 250, H * .52); c.lineTo(x + 400, H * .47); } c.lineTo(W, H * .6); c.fill();
    let x = 0, dx = -(segs[base] ? segs[base].c : 0) * frac, maxy = H; const camY = CAMH + (segs[base] ? segs[base].y + ((segs[base + 1] || segs[base]).y - segs[base].y) * frac : 0), camX = laneX * 330, P = [];
    for (let n = 0; n < DRAWN; n++){ const s = segs[base + n]; if (!s) break; const z1 = (n - frac) * SEG, z2 = (n + 1 - frac) * SEG; const p = (z, wx, wy) => { const sc = DEPTH / Math.max(z, 40); return [W / 2 + sc * (wx - camX) * W / 2, H * .56 - sc * (wy - camY) * W / 2, sc * roadW * W / 2, sc]; };
      const a = p(Math.max(z1, 60), x, s.y), s2 = segs[base + n + 1] || s; x += dx; dx += s.c; const b = p(z2, x, s2.y); P.push([a, b, s, base + n, n]); }
    for (const [a, b, s, idx, n] of P){ if (b[1] >= maxy) continue; const alt = Math.floor(idx / 3) % 2;
      c.fillStyle = alt ? C.grass : C.grass2; c.fillRect(0, b[1], W, maxy - b[1] + 1);
      c.fillStyle = alt ? C.road : C.road2; c.beginPath(); c.moveTo(a[0] - a[2], a[1]); c.lineTo(a[0] + a[2], a[1]); c.lineTo(b[0] + b[2], b[1]); c.lineTo(b[0] - b[2], b[1]); c.fill();
      if (C.edge){ c.fillStyle = C.edge; for (const sg of [-1, 1]){ c.beginPath(); c.moveTo(a[0] + sg * a[2] * .93, a[1]); c.lineTo(a[0] + sg * a[2] * .97, a[1]); c.lineTo(b[0] + sg * b[2] * .97, b[1]); c.lineTo(b[0] + sg * b[2] * .93, b[1]); c.fill(); } }
      if (C.mid && alt){ c.fillStyle = C.mid; c.beginPath(); c.moveTo(a[0] - a[2] * .02, a[1]); c.lineTo(a[0] + a[2] * .02, a[1]); c.lineTo(b[0] + b[2] * .02, b[1]); c.lineTo(b[0] - b[2] * .02, b[1]); c.fill(); }
      if (s.end){ c.fillStyle = 'rgba(227,170,76,.35)'; c.beginPath(); c.moveTo(a[0] - a[2], a[1]); c.lineTo(a[0] + a[2], a[1]); c.lineTo(b[0] + b[2], b[1]); c.lineTo(b[0] - b[2], b[1]); c.fill(); }
      maxy = b[1]; }
    for (let i = P.length - 1; i >= 0; i--){ const [a, , s, , n] = P[i]; if (n < 1) continue; for (const [type, off, sc] of s.sp){ const sx = a[0] + off * a[2], k = a[3] * W / 2 * sc; if (sx < -400 || sx > W + 400) continue; sprite(type, sx, a[1], k, n / DRAWN); } }
    const fog = c.createLinearGradient(0, H * .36, 0, H * .7); fog.addColorStop(0, 'rgba(90,108,112,0)'); fog.addColorStop(.5, 'rgba(90,108,112,.5)'); fog.addColorStop(1, 'rgba(90,108,112,0)'); c.fillStyle = fog; c.fillRect(0, H * .3, W, H * .45);
    const hl = c.createRadialGradient(W / 2, H * 1.02, 20, W / 2, H * .9, W * .62); hl.addColorStop(0, era === 2026 ? 'rgba(225,240,255,.34)' : 'rgba(255,225,160,.3)'); hl.addColorStop(1, 'rgba(0,0,0,0)'); c.fillStyle = hl; c.fillRect(0, H * .5, W, H * .5);
    c.strokeStyle = 'rgba(210,228,232,.5)'; c.lineWidth = 1.2; c.beginPath(); const k = speed / 1900; for (let i = 0; i < (lite ? 40 : 90); i++){ const rx = (i * 97.3 + t * 300 * (1 + (i % 5) * .2)) % W, ry = (i * 53.7 + t * 900) % H, dxr = (rx - W / 2) * .06 * k; c.moveTo(rx, ry); c.lineTo(rx + dxr - 3, ry + 16 + k * 10); } c.stroke();
    // drops on the glass, cleared by the wiper
    const ph = (wip % 2.4) / 2.4, ang = ph < .5 ? ph * 2 : 2 - ph * 2, th = -1.25 + ang * 2.5; if (drops.length < (lite ? 26 : 60) && rr() < .5) drops.push([rr() * W, rr() * H * .8, 2 + rr() * 4, 0]);
    c.fillStyle = 'rgba(205,225,230,.42)'; for (let i = drops.length - 1; i >= 0; i--){ const d = drops[i]; d[3] += .016; d[1] += d[3] * .4; const a = Math.atan2(d[0] - W * .5, H * 1.05 - d[1]); if (Math.abs(a - th) < .11 || d[1] > H * .86){ drops.splice(i, 1); continue; } c.beginPath(); c.ellipse(d[0], d[1], d[2], d[2] * 1.3, 0, 0, 6.3); c.fill(); }
    c.strokeStyle = '#07090a'; c.lineWidth = 7; c.lineCap = 'round'; for (const px of [W * .3, W * .72]){ c.beginPath(); c.moveTo(px, H * 1.02); c.lineTo(px + Math.sin(th) * H * .7, H * 1.02 - Math.cos(th) * H * .7); c.stroke(); }
  }
  /* the cabin: pillars, mirror, dashboard and wheel, drawn once per era as an overlay */
  function cabin(e){ const INK = '#0b0d10', dash = e === 2026 ? '#191c21' : e === 1993 ? '#2b2a28' : '#3a4a44', trim = e === 2026 ? '#2a2f37' : e === 1993 ? '#3a3835' : '#4f6b63';
    let s = `<path d="M0 0 H1600 V70 Q800 30 0 70 Z" fill="#0b0d10"/><path d="M0 0 H110 L40 900 H0 Z M1600 0 H1490 L1560 900 H1600 Z" fill="#0b0d10"/><rect x="690" y="52" width="220" height="64" rx="12" fill="#12151a" stroke="${INK}" stroke-width="4"/><rect x="702" y="62" width="196" height="44" rx="6" fill="#2c3b40"/>`;
    s += `<path d="M0 900 V690 Q400 610 800 618 Q1200 610 1600 690 V900 Z" fill="${dash}" stroke="${INK}" stroke-width="5"/><path d="M0 720 Q400 640 800 648 Q1200 640 1600 720" fill="none" stroke="${trim}" stroke-width="10"/>`;
    if (e === 2026) s += `<rect x="560" y="660" width="330" height="200" rx="14" fill="#0c0f13" stroke="${INK}" stroke-width="4"/><rect x="1010" y="676" width="250" height="76" rx="10" fill="#0c0f13" stroke="${INK}" stroke-width="3"/><text id="dv-speed" x="1135" y="730" text-anchor="middle" font-size="46" fill="#9fd0e6" font-family="monospace">0</text><text x="1230" y="730" font-size="16" fill="#55707c" font-family="monospace">km/h</text>`;
    else if (e === 1993) s += `<rect x="560" y="680" width="330" height="180" rx="6" fill="#d9d2b8" stroke="${INK}" stroke-width="4"/><circle cx="1090" cy="730" r="62" fill="#111" stroke="#55504a" stroke-width="6"/><circle cx="1220" cy="730" r="48" fill="#111" stroke="#55504a" stroke-width="6"/><path id="dv-needle" d="M1090 730 L1050 760" stroke="#e3aa4c" stroke-width="5" stroke-linecap="round"/><rect x="380" y="700" width="130" height="60" rx="6" fill="#151515" stroke="${INK}" stroke-width="3"/><path d="M400 760 q-20 60 30 90" fill="none" stroke="#111" stroke-width="7"/><rect x="930" y="690" width="60" height="30" fill="#b3261e" stroke="${INK}" stroke-width="3"/>`;
    else s += `<rect x="560" y="690" width="330" height="170" rx="4" fill="#d8d2bd" stroke="${INK}" stroke-width="4"/><circle cx="1130" cy="736" r="56" fill="#e9e6d8" stroke="${INK}" stroke-width="5"/><path id="dv-needle" d="M1130 736 L1094 764" stroke="#b3261e" stroke-width="5" stroke-linecap="round"/><circle cx="420" cy="760" r="16" fill="#c9a94e" stroke="${INK}" stroke-width="3"/><circle cx="470" cy="760" r="16" fill="#111" stroke="${INK}" stroke-width="3"/>`;
    const wr = e === 1960 ? 190 : 165, wc = e === 1960 ? '#1a1410' : '#0e1013';
    s += `<g id="dv-wheel" style="transform-origin:1150px 900px"><circle cx="1150" cy="900" r="${wr}" fill="none" stroke="${wc}" stroke-width="${e === 1960 ? 16 : 30}"/><circle cx="1150" cy="900" r="${wr}" fill="none" stroke="#3a3f47" stroke-width="3"/><path d="M${1150 - wr} 900 H${1150 + wr} M1150 900 V${900 - wr}" stroke="${wc}" stroke-width="${e === 1960 ? 12 : 26}"/><circle cx="1150" cy="900" r="44" fill="${wc}" stroke="#3a3f47" stroke-width="3"/></g>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="none">${s}</svg>`; }
  return {
    mount(canvas, isLite){ cv = canvas; lite = !!isLite; W = lite ? 640 : 800; H = lite ? 360 : 450; cv.width = W; cv.height = H; ctx = cv.getContext('2d'); },
    start(E, dir, e, cb, tick){ build(E, dir, e); onEnd = cb; onTick = tick; drops = []; if (!running){ running = true; last = performance.now(); raf = requestAnimationFrame(frame); } draw(0); },
    stop(){ running = false; cancelAnimationFrame(raf); onEnd = null; onTick = null; },
    setGo(v){ go = !!v; }, get go(){ return go; }, setLane(v){ laneT = Math.max(-1, Math.min(1, v)); }, get lane(){ return laneT; }, setFast(v){ fast = !!v; }, setLite(v){ lite = !!v; }, get prog(){ return total ? pos / total : 0; }, get speed(){ return speed; }, cabin, redraw(){ if (ctx) draw(performance.now() / 1000); } };
})();
if (typeof module !== 'undefined') module.exports = { DRIVE };
