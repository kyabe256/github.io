/* ---------- backgrounds, part 1: helpers, forest, cave, street. Ink line and flat tone, 900 high panoramas. ----------
   A scene is { w, bg, main, fore, spots }. bg scrolls slowly, fore scrolls fast and is drawn over the walker. spots name the x of things the game refers to. */
const SC = {};
const SK = { ink: '#0b0d10', fog: '#6d7c80', teal: '#3b5557', moss: '#27372f', amber: '#e3aa4c', paper: '#d9d7cd', rust: '#7b4a36' };
const rnd = seed => { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; };
const R1 = n => Math.round(n * 10) / 10;
const svgw = (w, body, defs = '') => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} 900" width="${w}" height="900" preserveAspectRatio="none"><defs>${defs}</defs>${body}</svg>`;
const rect = (x, y, w, h, f, x2 = '') => `<rect x="${R1(x)}" y="${R1(y)}" width="${R1(w)}" height="${R1(h)}" fill="${f}" ${x2}/>`;
const ln = (d, w = 2, c = SK.ink, x = '') => `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${x}/>`;
const pf = (d, f, w = 2.5, x = '') => `<path d="${d}" fill="${f}" stroke="${w ? SK.ink : 'none'}" stroke-width="${w}" stroke-linejoin="round" ${x}/>`;
const tx = (x, y, s, size, f = SK.ink, x2 = '') => `<text x="${x}" y="${y}" font-size="${size}" fill="${f}" font-family="'Shippori Mincho','Hiragino Mincho ProN',serif" font-weight="700" ${x2}>${s}</text>`;
const glow = (id, c, o = .9) => `<radialGradient id="${id}"><stop offset="0" stop-color="${c}" stop-opacity="${o}"/><stop offset="1" stop-color="${c}" stop-opacity="0"/></radialGradient>`;
const lamp = (x, y, r, id) => `<circle cx="${x}" cy="${y}" r="${r}" fill="url(#${id})"/>`;
function hatch(x, y, w, h, n, c = SK.ink, op = .35, slant = 10){ let s = ''; for (let i = 0; i < n; i++){ const xx = x + (w * (i + .5)) / n; s += `M${R1(xx)} ${R1(y)} l${-slant} ${R1(h)} `; } return ln(s, 1.2, c, `opacity="${op}"`); }
/* a cedar trunk: straight column, bark strokes, root flare */
function trunk(x, w, top, base, fill, rr, bark = '#000', op = .5){ let s = pf(`M${R1(x - w / 2)} ${top} L${R1(x - w / 2 - w * .06)} ${base - 40} Q${R1(x - w * .8)} ${base - 6} ${R1(x - w * 1.25)} ${base} L${R1(x + w * 1.25)} ${base} Q${R1(x + w * .8)} ${base - 6} ${R1(x + w / 2 + w * .06)} ${base - 40} L${R1(x + w / 2)} ${top} Z`, fill, 2.5), d = '';
  for (let i = 0; i < Math.max(4, w / 7); i++){ const xx = x - w / 2 + 4 + rr() * (w - 8), y0 = top + rr() * (base - top - 120), l = 40 + rr() * 150; d += `M${R1(xx)} ${R1(y0)} q${R1(rr() * 5 - 2.5)} ${R1(l / 2)} ${R1(rr() * 4 - 2)} ${R1(l)} `; }
  return s + ln(d, 1.3, bark, `opacity="${op}"`) + `<path d="M${R1(x + w / 2 - w * .22)} ${top} L${R1(x + w / 2)} ${top} L${R1(x + w / 2 + w * .06)} ${base - 40} L${R1(x + w / 2 - w * .16)} ${base - 40} Z" fill="#9fb7b8" opacity=".13"/>`; }
function fern(x, y, s, f = '#18231e', rr){ let d = ''; for (let i = 0; i < 7; i++){ const a = -Math.PI * (.12 + i * .13), l = (60 + (rr ? rr() : .5) * 50) * s; d += `M${R1(x)} ${R1(y)} Q${R1(x + Math.cos(a) * l * .5)} ${R1(y + Math.sin(a) * l * .9)} ${R1(x + Math.cos(a) * l)} ${R1(y + Math.sin(a) * l * .55)} `; } return ln(d, 5 * s, f) + ln(d, 1.4 * s, '#0a0f0d'); }
function rain(w, seed, n, c = '#cfe1e3', op = .35, len = 70){ const rr = rnd(seed); let d = ''; for (let i = 0; i < n; i++){ const x = rr() * w, y = rr() * 900, l = len * (.5 + rr()); d += `M${R1(x)} ${R1(y)} l${R1(-l * .16)} ${R1(l)} `; } return ln(d, 1.3, c, `opacity="${op}"`); }
/* cars seen from the side, one per era. x,y = ground point under the middle */
function carSide(e, x, y, o = {}){ const g = (s) => `<g transform="translate(${x} ${y})${o.flip ? ' scale(-1 1)' : ''}">${s}</g>`, wheel = (wx, r = 30) => `<circle cx="${wx}" cy="${-r}" r="${r}" fill="#0c0d10" stroke="${SK.ink}" stroke-width="3"/><circle cx="${wx}" cy="${-r}" r="${r * .45}" fill="#6f777c" stroke="${SK.ink}" stroke-width="2"/>`;
  if (e === 1960) return g(pf('M-150 -40 L-150 -110 L-40 -110 L-30 -160 L60 -160 L84 -100 L150 -92 L154 -40 Z', o.c || '#4f6b63', 3) + pf('M-22 -152 L52 -152 L70 -104 L-30 -104 Z', '#1b2428', 2.5) + rect(-146, -118, 104, 12, '#39493f', `stroke="${SK.ink}" stroke-width="2.5"`) + ln('M-150 -78 L-40 -78 M-96 -110 L-96 -40', 2) + pf('M150 -92 l14 6 l0 22 l-12 4 Z', '#d9d2b0', 2) + wheel(-96) + wheel(112, 28) + (o.lit ? `<path d="M164 -74 L420 -120 L420 -10 Z" fill="#f0d79a" opacity=".16"/>` : ''));
  if (e === 1993) return g(pf('M-178 -44 L-176 -84 Q-150 -96 -112 -98 L-76 -140 L58 -140 L102 -98 Q156 -92 178 -78 L180 -44 Z', '#e6e6e0', 3) + pf('M-178 -44 L-176 -84 Q-150 -96 -112 -98 L102 -98 Q156 -92 178 -78 L180 -44 Z', o.plain ? '#8d9296' : '#17191d', 3) + pf('M-66 -132 L-12 -132 L-12 -100 L-98 -100 Z', '#1b2428', 2.5) + pf('M0 -132 L52 -132 L86 -100 L0 -100 Z', '#1b2428', 2.5) + (o.plain ? '' : rect(-30, -154, 54, 14, '#b3261e', `stroke="${SK.ink}" stroke-width="2.5" rx="5"`) + rect(-140, -86, 250, 12, '#e6e6e0')) + ln('M-6 -98 L-6 -46', 2) + wheel(-112) + wheel(116) + (o.lit ? `<path d="M180 -70 L460 -120 L460 -6 Z" fill="#f0d79a" opacity=".16"/>` : ''));
  return g(pf('M-184 -44 Q-188 -92 -150 -100 L-100 -150 Q-20 -164 60 -150 L120 -104 Q176 -98 186 -74 L188 -44 Z', o.c || '#3a4046', 3) + pf('M-92 -144 Q-40 -154 -8 -152 L-8 -104 L-136 -104 Z', '#1a2227', 2.5) + pf('M4 -152 Q40 -152 56 -144 L104 -104 L4 -104 Z', '#1a2227', 2.5) + ln('M-2 -104 L-2 -46 M-150 -100 L120 -104', 2) + rect(150, -92, 34, 9, '#e9f1f2', 'rx="4"') + rect(-186, -90, 16, 10, '#b3261e', 'rx="3"') + wheel(-116, 32) + wheel(120, 32) + (o.lit ? `<path d="M188 -84 L500 -130 L500 -4 Z" fill="#dfeef2" opacity=".14"/>` : ''));
}
/* ============ forest: trailhead -> narrow path -> rock face with the cave mouth ============ */
SC.forest = e => { const W = 3600, rr = rnd(11 + e), sp = { car: 330, sign: 640, tunnel: 2080, body: 2900, cane: 2990, cave: 3230, tape: 2640, vend: 520 };
  const D = glow('fg1', '#b9d2d4', .55) + glow('fg2', SK.amber, .8) + `<linearGradient id="fsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#10171b"/><stop offset=".55" stop-color="#2c3b3e"/><stop offset="1" stop-color="#5a6c6f"/></linearGradient><linearGradient id="fgnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#20292a"/><stop offset="1" stop-color="#0b0f10"/></linearGradient><linearGradient id="fmist" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d8f92" stop-opacity="0"/><stop offset="1" stop-color="#7d8f92" stop-opacity=".5"/></linearGradient>`;
  let bg = rect(0, 0, 2400, 900, 'url(#fsky)') + pf('M0 520 L160 430 L330 500 L520 380 L760 470 L980 400 L1240 490 L1500 410 L1760 480 L2040 390 L2400 470 L2400 900 L0 900 Z', '#243235', 0);
  for (let i = 0; i < 46; i++){ const x = 20 + i * 52 + rr() * 30, w = 10 + rr() * 16; bg += rect(x, 120 + rr() * 80, w, 700, i % 3 ? '#33454a' : '#3d5156') + `<path d="M${R1(x - 40)} ${R1(200 + rr() * 60)} l${R1(40 + w / 2)} -90 l${R1(40 + w / 2)} 90 Z" fill="#2a3a3e" opacity=".8"/>`; }
  bg += rect(0, 420, 2400, 480, 'url(#fmist)');
  let m = rect(0, 770, W, 130, 'url(#fgnd)') + pf(`M0 800 C400 770 900 812 1500 790 S2700 800 ${W} 786 L${W} 900 L0 900 Z`, '#1a2223', 0) + pf(`M0 812 C500 790 1100 826 1700 804 S2900 812 ${W} 800 L${W} 838 C2800 850 1700 838 1100 852 S300 832 0 846 Z`, '#3a4744', 0, 'opacity=".55"');
  // trailhead
  m += pf('M0 640 L0 792 L760 792 L760 760 L700 640 Z', '#252d2e', 0) + ln('M20 742 L720 742 M20 742 L20 790 M260 742 L260 790 M500 742 L500 790 M720 742 L720 790', 5, '#8b9597') + ln('M20 760 L720 760', 3, '#8b9597');
  m += rect(600, 560, 14, 232, '#3b3229', `stroke="${SK.ink}" stroke-width="2.5"`) + pf('M560 540 L690 540 L690 620 L560 620 Z', e === 1960 ? '#5a4a36' : '#3f5a4a', 3) + tx(575, 572, '黒檜の森', 24, '#e6e2d2') + tx(578, 604, e === 1960 ? '雨穴道' : '登山口', 24, '#e6e2d2');
  if (e === 1993) m += rect(470, 600, 96, 192, '#b9c2c4', `stroke="${SK.ink}" stroke-width="3"`) + rect(480, 612, 76, 86, '#22303a', `stroke="${SK.ink}" stroke-width="2"`) + [0, 1, 2, 3].map(i => rect(486 + i * 18, 622, 12, 30, ['#c9412f', '#e3aa4c', '#2f6f8f', '#6a7f3a'][i])).join('') + rect(480, 706, 76, 14, '#e3aa4c') + lamp(518, 660, 150, 'fg2');
  if (e === 1960) m += pf('M430 792 L440 690 L470 676 L500 690 L510 792 Z', '#59605d', 3) + tx(456, 740, '雨', 22, '#1a1d1f') + tx(456, 768, '穴', 22, '#1a1d1f');
  if (e === 2026) m += carSide(2026, 130, 792, { c: '#d7dbdc' }) + ln('M-20 700 L330 704', 6, '#e3c23a') + ln('M-20 700 L330 704', 2, '#111', 'stroke-dasharray="18 18"');
  // the narrow path through the trunks
  const tr = [820, 990, 1130, 1340, 1500, 1720, 1900, 2290, 2460, 2620];
  for (const x of tr){ const w = 60 + rr() * 46; m += trunk(x + rr() * 30, w, -20, 792 - rr() * 14, '#1d2729', rr); }
  for (let i = 0; i < 26; i++) m += fern(760 + rr() * 1900, 800 + rr() * 16, .5 + rr() * .5, '#1d2a25', rr);
  // the drain portal in the slope (1960: a raw trial adit; 1993: concrete mouth, broken grate; 2026: sealed)
  m += pf('M1960 792 L1975 600 Q2080 520 2190 600 L2205 792 Z', '#2b3231', 3) + pf('M2010 792 L2010 660 Q2080 590 2150 660 L2150 792 Z', e === 2026 ? '#70777a' : '#050607', 3);
  if (e === 1960) m += ln('M2010 792 L2010 660 M2150 792 L2150 660 M2000 664 L2160 664', 12, '#4a3a2a') + ln('M2010 792 L2010 660 M2150 792 L2150 660 M2000 664 L2160 664', 2) + tx(2024, 640, '鷹取組 試掘坑', 20, '#d8d2bd');
  if (e === 1993) m += ln('M2030 792 L2030 668 M2060 792 L2060 640 M2090 792 L2090 632 M2130 792 L2130 668', 5, '#6e5a48') + ln('M2100 792 L2120 700 L2096 640', 5, '#6e5a48') + rect(1990, 566, 180, 30, '#d8d2bd', `stroke="${SK.ink}" stroke-width="2"`) + tx(1998, 588, '霧渕原発 第2排水坑', 18, '#7a1f18');
  if (e === 2026) m += hatch(2014, 664, 132, 126, 9, '#000', .25) + rect(2040, 700, 80, 46, '#e3c23a', `stroke="${SK.ink}" stroke-width="2"`) + tx(2048, 720, '閉塞済', 18, '#111') + tx(2046, 740, '2026.11.04', 12, '#111');
  // rock face and the cave mouth
  m += pf(`M2700 792 L2720 560 L2800 420 L2900 300 L3010 200 L3120 90 L3230 20 L3330 -10 L${W} -10 L${W} 792 Z`, '#232a2b', 3) + pf('M2900 300 L2980 330 L3040 250 L3120 280 L3120 90 Z', '#2f3839', 0) + pf('M3330 -10 L3420 160 L3520 120 L3600 220 L3600 -10 Z', '#2f3839', 0);
  m += hatch(2760, 430, 240, 300, 12, '#000', .35, 40) + hatch(3400, 200, 180, 520, 10, '#000', .35, -30);
  m += pf('M3060 792 C3050 640 3090 500 3180 452 C3270 420 3380 480 3400 620 C3410 700 3408 760 3404 792 Z', '#020304', 3.5) + pf('M3100 792 C3096 680 3120 560 3190 510 C3262 480 3340 530 3360 640 C3366 710 3366 760 3364 792 Z', '#0a1012', 0, 'opacity=".9"');
  for (let i = 0; i < 9; i++) m += ln(`M${3080 + i * 38} ${470 - Math.abs(i - 4) * -8} q4 30 0 ${40 + rr() * 70}`, 2, '#5d6b6d', 'opacity=".5"');
  m += pf('M2700 792 L2716 700 L2790 660 L2860 720 L2880 792 Z', '#2b3233', 3) + pf('M3420 792 L3440 690 L3520 650 L3580 720 L3600 792 Z', '#2b3233', 3);
  if (e === 1960) m += ln('M3040 470 Q3230 520 3420 462', 9, '#b9a77a') + ln('M3040 470 Q3230 520 3420 462', 2) + [3110, 3200, 3290, 3370].map(x => pf(`M${x} 492 l-9 44 l18 0 Z`, '#e6e2d2', 2)).join('');
  if (e === 1993) m += rect(2990, 560, 60, 232, '#3b3229', 'opacity="0"') + rect(2996, 600, 12, 192, '#4a4038', `stroke="${SK.ink}" stroke-width="2"`) + rect(2950, 560, 110, 60, '#d8d2bd', `stroke="${SK.ink}" stroke-width="2.5"`) + tx(2962, 586, '立入禁止', 22, '#7a1f18') + tx(2962, 610, '霧渕町', 16, '#222');
  if (e === 2026){ // the scene of the crime: tape, markers, the body under the lip of the rock
    m += ln('M2640 690 L2850 676 L3050 690', 7, '#e3c23a') + ln('M2640 690 L2850 676 L3050 690', 2.2, '#111', 'stroke-dasharray="20 20"') + rect(2634, 660, 10, 132, '#51585a') + rect(2846, 650, 10, 142, '#51585a');
    m += `<g transform="translate(2900 786)">${pf('M-150 0 C-150 -16 -120 -30 -92 -30 L60 -34 C110 -36 150 -20 164 0 Z', '#4b5547', 3)}${pf('M-150 0 C-150 -16 -120 -30 -92 -30 L-40 -31 L-36 0 Z', '#2d3338', 3)}${pf('M150 -8 C150 -30 176 -44 198 -36 C216 -28 218 -6 204 0 L160 0 Z', '#d9cfc2', 3)}${pf('M168 -40 C184 -52 206 -46 212 -30 C200 -40 184 -42 168 -40 Z', '#9aa0a3', 2.5)}${pf('M40 -30 L96 -12 L120 -2 L104 4 L30 -8 Z', '#434c40', 2.5)}${pf('M-196 0 L-150 -22 L-144 0 Z', '#17191b', 3)}${ln('M-60 -30 L-58 -2 M10 -32 L14 -4', 1.6, '#000', 'opacity=".5"')}</g>`;
    for (const [x, n] of [[2760, 1], [2990, 2], [3040, 3]]) m += pf(`M${x} 792 l10 -30 l10 30 Z`, '#e3c23a', 2.5) + tx(x + 5, 786, n, 14, '#111');
    m += lamp(2900, 640, 330, 'fg1');
  }
  let f = '';
  for (const x of [240, 1700, 3100, 4300]){ f += trunk(x, 120, -20, 930, '#070a0b', rr, '#1d2a2c', .9); }
  for (let i = 0; i < 16; i++) f += fern(rr() * 4400, 905, 1.2 + rr(), '#06090a', rr);
  f += rain(4500, 5, 520, '#d5e6e8', .3, 90);
  return { w: W, fw: 4500, bw: 2400, defs: D, bg, main: m + rain(W, 9, 420, '#c7dadc', .22, 60), fore: f, spots: sp, ground: 792, amb: 'forest' }; };
/* ============ cave: wet rock, a long throat, then the fork ============ */
SC.cave = e => { const W = 3000, rr = rnd(77), sp = { out: 120, carve: 1180, lamp: 700, pool: 1700, left: 2430, right: 2790 };
  const D = glow('cg1', '#e3aa4c', .7) + glow('cg2', '#8fd0d4', .5) + `<linearGradient id="cgnd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1b2224"/><stop offset="1" stop-color="#050708"/></linearGradient>`;
  let bg = rect(0, 0, 2100, 900, '#06090a'); for (let i = 0; i < 30; i++){ const x = rr() * 2100, y = 120 + rr() * 500, w = 80 + rr() * 220; bg += pf(`M${R1(x)} ${R1(y)} l${R1(w * .4)} ${R1(-40 - rr() * 60)} l${R1(w * .6)} ${R1(50 + rr() * 40)} l${R1(-w * .3)} ${R1(60 + rr() * 80)} Z`, i % 2 ? '#0e1416' : '#121a1c', 0); }
  let m = '';
  // ceiling and floor silhouettes with stalactites
  let top = 'M0 0 L0 250 ', bot = `M0 900 L0 792 `; for (let x = 0; x <= W; x += 100){ top += `L${x + 50} ${R1(150 + rr() * 130 + (x < 300 ? 60 : 0))} L${x + 100} ${R1(120 + rr() * 90)} `; bot += `L${x + 50} ${R1(792 + rr() * 8)} L${x + 100} ${R1(790 + rr() * 10)} `; }
  m += pf(top + `L${W} 0 Z`, '#0a0e10', 3) + pf(bot + `L${W} 900 Z`, 'url(#cgnd)', 3);
  for (let i = 0; i < 44; i++){ const x = 80 + rr() * (W - 160), h = 40 + rr() * 170, w = 10 + rr() * 22, y = 150 + rr() * 60; m += pf(`M${R1(x - w)} ${R1(y)} Q${R1(x)} ${R1(y + h * .6)} ${R1(x)} ${R1(y + h)} Q${R1(x)} ${R1(y + h * .6)} ${R1(x + w)} ${R1(y)} Z`, '#11181a', 2); }
  for (let i = 0; i < 20; i++){ const x = 200 + rr() * (W - 300), h = 20 + rr() * 60, w = 12 + rr() * 26; m += pf(`M${R1(x - w)} 794 Q${R1(x)} ${R1(794 - h * .5)} ${R1(x)} ${R1(794 - h)} Q${R1(x)} ${R1(794 - h * .5)} ${R1(x + w)} 794 Z`, '#151d1f', 2); }
  // the way out, grey daylight and rain
  m += pf('M0 792 L0 330 C60 300 150 330 190 420 C220 520 214 700 204 792 Z', '#56676a', 3) + rain(200, 3, 40, '#e6f2f3', .6, 70) + lamp(110, 600, 380, 'cg2');
  // an oil lamp on a hook, year carvings, a pool
  m += ln('M700 300 L700 420', 3, '#3d3a34') + pf('M684 420 L716 420 L722 470 L678 470 Z', '#3a3328', 2.5) + rect(688, 430, 24, 30, '#f1d48a') + lamp(700, 450, e === 2026 ? 120 : 260, 'cg1');
  m += rect(1090, 430, 190, 150, '#172022', 'opacity=".7"') + ln('M1110 470 l30 0 M1125 455 l0 60 M1160 470 l40 0 M1180 470 l0 46 M1160 516 l40 0 M1220 460 l0 60 l30 -30', 3, '#7f8f90', 'opacity=".8"') + tx(1104, 560, '昭和三十五年 鷹取組', 16, '#8fa0a1', 'opacity=".85"');
  m += `<ellipse cx="1700" cy="806" rx="230" ry="14" fill="#31494c" opacity=".8"/><ellipse cx="1660" cy="804" rx="90" ry="5" fill="#9fc6c9" opacity=".35"/>`;
  m += ln('M1300 792 L2300 792', 4, '#3b3a36', 'stroke-dasharray="70 36" opacity=".8"') + ln('M1300 780 L2300 780', 3, '#4a4842', 'opacity=".5"'); // old rail of the trial adit
  // the fork: two throats
  m += pf('M2300 792 C2290 600 2340 470 2430 450 C2520 440 2560 560 2566 792 Z', '#010202', 3.5) + pf('M2660 792 C2650 580 2700 440 2800 428 C2890 424 2940 560 2944 792 Z', '#010202', 3.5);
  m += pf('M2566 792 L2572 560 L2610 470 L2650 560 L2660 792 Z', '#1a2224', 3) + hatch(2580, 520, 70, 260, 6, '#000', .5, 6);
  m += tx(2392, 430, '下', 34, '#8fa0a1', 'opacity=".8"') + tx(2772, 410, '上', 34, '#8fa0a1', 'opacity=".8"');
  if (e === 2026) m += pf('M2672 792 L2700 640 L2760 600 L2830 620 L2880 580 L2930 680 L2940 792 Z', '#1d2628', 3) + pf('M2700 792 L2730 700 L2790 690 L2820 792 Z', '#263133', 2.5) + hatch(2700, 620, 220, 160, 9, '#000', .4, 20);
  if (e === 1960) m += pf('M2312 792 L2340 620 L2410 580 L2470 610 L2530 590 L2560 700 L2562 792 Z', '#263133', 3) + hatch(2330, 610, 220, 170, 9, '#000', .4, -20) + ln('M2360 640 l40 20 l-20 40 M2460 630 l30 50', 2, '#9fb0b1', 'opacity=".7"');
  let f = ''; for (const x of [300, 1500, 2700, 3700]) f += pf(`M${x - 160} 0 L${x - 60} 360 L${x} 620 L${x + 40} 360 L${x + 170} 0 Z`, '#030506', 0) + pf(`M${x - 300} 900 L${x - 120} 860 L${x} 820 L${x + 140} 862 L${x + 320} 900 Z`, '#030506', 0);
  return { w: W, fw: 3900, bw: 2100, defs: D, bg, main: m, fore: f, spots: sp, ground: 792, amb: 'cave', dark: 1 }; };
/* ============ street: police box / clinic / inn, the plant on the horizon ============ */
SC.street = e => { const W = 3600, rr = rnd(31), sp = { police: 520, clinic: 1560, inn: 2620, car: 3290, bus: 2080, post: 1080 };
  const D = glow('sg1', SK.amber, .75) + glow('sg2', '#cfe6ea', .5) + `<linearGradient id="ssky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#11181d"/><stop offset=".6" stop-color="#33444a"/><stop offset="1" stop-color="#5f7074"/></linearGradient><linearGradient id="srd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3134"/><stop offset="1" stop-color="#0c0f11"/></linearGradient>`;
  let bg = rect(0, 0, 2400, 900, 'url(#ssky)') + pf('M0 560 L200 470 L420 540 L700 430 L980 520 L1240 450 L1560 540 L1800 460 L2100 520 L2400 470 L2400 900 L0 900 Z', '#1f2b2f', 0);
  // the plant across the valley: reactor dome and stack (1960: cranes and a pit)
  if (e === 1960) bg += ln('M1300 560 L1300 300 L1480 340 M1300 300 L1220 380 M1640 560 L1640 340 L1770 370', 5, '#16202a') + pf('M1180 560 L1220 500 L1760 500 L1800 560 Z', '#17212a', 0) + lamp(1420, 500, 200, 'sg1');
  else bg += pf('M1250 560 L1250 420 A90 90 0 0 1 1430 420 L1430 560 Z', '#16202a', 0) + rect(1450, 470, 250, 90, '#16202a') + rect(1720, 230, 22, 330, '#16202a') + `<circle cx="1731" cy="232" r="5" fill="#c9412f"/>` + (e === 2026 ? ln('M1250 420 L1430 520 M1430 420 L1250 520', 3, '#33454d', 'opacity=".8"') + ln('M1500 470 L1500 360 L1640 380', 4, '#16202a') : lamp(1340, 430, 220, 'sg2'));
  bg += rect(0, 500, 2400, 400, '#6d7c80', 'opacity=".22"');
  let m = rect(0, 770, W, 130, 'url(#srd)') + rect(0, 760, W, 14, '#454d50') + ln(`M0 836 L${W} 836`, 4, '#b9c0c0', 'stroke-dasharray="90 70" opacity=".5"');
  const win = (x, y, w, h, lit) => rect(x, y, w, h, lit ? '#e9c377' : '#141b20', `stroke="${SK.ink}" stroke-width="2.5"`) + (lit ? '' : `<path d="M${x + 4} ${y + h - 6} L${x + w * .5} ${y + 4}" stroke="#55676d" stroke-width="2"/>`) + ln(`M${x + w / 2} ${y} l0 ${h} M${x} ${y + h / 2} l${w} 0`, 1.6);
  const roof = (x, y, w, o = 26, c = '#1a2024') => pf(`M${x - o} ${y} L${x + w * .5} ${y - 84} L${x + w + o} ${y} Z`, c, 3) + hatch(x - o + 20, y - 60, w + o * 2 - 40, 56, Math.round(w / 26), '#000', .3, 0);
  const pole = x => rect(x, 250, 14, 522, '#2a2622', `stroke="${SK.ink}" stroke-width="2.5"`) + rect(x - 40, 280, 94, 9, '#2a2622', `stroke="${SK.ink}" stroke-width="2"`) + (e === 1960 ? '' : rect(x - 12, 350, 38, 50, '#3d4447', `stroke="${SK.ink}" stroke-width="2"`));
  // row of houses behind
  for (let i = 0; i < 9; i++){ const x = i * 420 - 60 + rr() * 40, w = 250 + rr() * 110, y = 470 + rr() * 60; m += rect(x, y, w, 300, '#1c2428', `stroke="${SK.ink}" stroke-width="2.5"`) + roof(x, y, w, 20, '#141a1d') + win(x + 40, y + 60, 54, 60, rr() > .6) + win(x + w - 100, y + 60, 54, 60, rr() > .7); }
  m += ln(`M0 292 Q540 340 1087 286 T2170 290 T${W} 286`, 2, '#0b0d10') + ln(`M0 306 Q540 354 1087 300 T2170 304 T${W} 300`, 1.5, '#0b0d10');
  // police
  if (e === 1960){ m += rect(330, 520, 380, 250, '#39382f', `stroke="${SK.ink}" stroke-width="3"`) + roof(330, 520, 380, 30, '#22241f') + rect(470, 610, 100, 160, '#1a1c1a', `stroke="${SK.ink}" stroke-width="3"`) + win(350, 600, 90, 90, 1) + win(600, 600, 90, 90, 0) + rect(442, 548, 156, 44, '#d8d2bd', `stroke="${SK.ink}" stroke-width="2.5"`) + tx(450, 580, '霧渕駐在所', 26) + `<circle cx="520" cy="500" r="20" fill="#b3261e" stroke="${SK.ink}" stroke-width="3"/>` + lamp(520, 500, 130, 'sg1'); }
  else { const c = e === 1993 ? '#55605f' : '#4a5357'; m += rect(260, 400, 520, 370, c, `stroke="${SK.ink}" stroke-width="3"`) + rect(250, 384, 540, 22, '#262c2f', `stroke="${SK.ink}" stroke-width="3"`) + [0, 1, 2, 3].map(i => win(292 + i * 122, 440, 80, 70, i === 1 || (e === 2026 && i === 3))).join('') + [0, 3].map(i => win(292 + i * 122, 560, 80, 90, i === 0)).join('') + rect(430, 560, 180, 210, '#161c20', `stroke="${SK.ink}" stroke-width="3"`) + ln('M520 560 L520 770', 2.5) + rect(410, 520, 220, 40, '#22282c', `stroke="${SK.ink}" stroke-width="3"`) + tx(428, 550, '霧渕警察署', 26, '#e6e2d2') + `<circle cx="520" cy="418" r="15" fill="#c9a94e" stroke="${SK.ink}" stroke-width="2.5"/>` + lamp(520, 600, 240, 'sg1'); }
  // post box / pole / phone
  m += pole(900) + pole(1940) + pole(3020);
  m += e === 1960 ? rect(1066, 650, 46, 122, '#8a2f24', `stroke="${SK.ink}" stroke-width="3" rx="20"`) : rect(1060, 660, 60, 112, '#b3261e', `stroke="${SK.ink}" stroke-width="3"`) + rect(1070, 690, 40, 8, '#111');
  // clinic
  m += rect(1340, 470, 440, 300, e === 1960 ? '#40423a' : '#aab3b2', `stroke="${SK.ink}" stroke-width="3"`) + roof(1340, 470, 440, 26, '#1d2327') + rect(1500, 600, 120, 170, '#1a2227', `stroke="${SK.ink}" stroke-width="3"`) + ln('M1560 600 L1560 770', 2.5) + win(1370, 580, 100, 100, 1) + win(1650, 580, 100, 100, e !== 1960) + rect(1470, 508, 180, 50, '#e9ebe6', `stroke="${SK.ink}" stroke-width="2.5"`) + tx(1486, 543, e === 1960 ? '汐見産院' : '汐見医院', 28, '#1c3a55') + lamp(1420, 630, 190, 'sg1');
  if (e !== 1960) m += rect(1796, 560, 16, 212, '#3d4447', `stroke="${SK.ink}" stroke-width="2.5"`) + pf('M1776 520 h56 v56 h-56 Z', '#e9ebe6', 2.5) + ln('M1804 530 v36 M1786 548 h36', 7, '#2f7a4a');
  // bus stop (1960: a wooden bench) and phone
  m += e === 1960 ? rect(2030, 730, 130, 12, '#4a3a2a', `stroke="${SK.ink}" stroke-width="2.5"`) + rect(2040, 742, 10, 30, '#4a3a2a') + rect(2140, 742, 10, 30, '#4a3a2a') : rect(2074, 560, 10, 212, '#51585a', `stroke="${SK.ink}" stroke-width="2"`) + `<circle cx="2079" cy="540" r="34" fill="#d9d7cd" stroke="${SK.ink}" stroke-width="3"/>` + tx(2060, 548, 'バス', 18) + rect(2050, 590, 60, 80, '#d9d7cd', `stroke="${SK.ink}" stroke-width="2"`);
  if (e === 1993) m += rect(2200, 560, 90, 212, '#6f8f86', `stroke="${SK.ink}" stroke-width="3" fill-opacity=".55"`) + rect(2222, 640, 46, 60, '#4f9a6a', `stroke="${SK.ink}" stroke-width="2.5"`) + rect(2200, 548, 90, 16, '#2f5a48', `stroke="${SK.ink}" stroke-width="2.5"`) + lamp(2245, 600, 120, 'sg2');
  // the inn: wide eaves, lattice, lantern, noren
  m += rect(2360, 430, 560, 340, '#2e2a24', `stroke="${SK.ink}" stroke-width="3"`) + pf('M2310 440 L2640 330 L2970 440 Z', '#15191b', 3) + hatch(2350, 360, 580, 76, 22, '#000', .35, 0) + pf('M2330 560 L2950 560 L2970 584 L2310 584 Z', '#15191b', 3);
  m += rect(2560, 600, 170, 170, '#0f1214', `stroke="${SK.ink}" stroke-width="3"`) + [0, 1, 2, 3].map(i => pf(`M${2562 + i * 42} 600 l40 0 l0 ${50 + (i % 2) * 6} l-40 0 Z`, '#5a2f2a', 2)).join('') + tx(2590, 640, '朽木屋', 30, '#e6e2d2');
  for (let i = 0; i < 9; i++) m += rect(2384 + i * 18, 610, 8, 150, '#1a1612') + rect(2760 + i * 18, 610, 8, 150, '#1a1612');
  m += win(2400, 470, 110, 70, 1) + win(2560, 470, 110, 70, 0) + win(2760, 470, 110, 70, e !== 2026) + pf('M2480 596 l34 0 l6 16 l0 60 l-6 14 l-34 0 l-6 -14 l0 -60 Z', '#e9c377', 2.5) + tx(2484, 650, '宿', 24, '#3a1a12') + lamp(2497, 640, 190, 'sg1');
  if (e === 2026) m += rect(2960, 690, 70, 82, '#d9d7cd', `stroke="${SK.ink}" stroke-width="2.5"`) + tx(2968, 720, '忌中', 22, '#111');
  // parking bay
  m += ln('M3160 776 L3160 880 M3430 776 L3430 880', 4, '#b9c0c0', 'opacity=".6"') + tx(3250, 870, 'P', 44, '#b9c0c0', 'opacity=".5"');
  let f = pole(-200); for (const x of [700, 2600, 4200]) f += rect(x, -10, 26, 930, '#06080a') + rect(x - 90, 120, 210, 16, '#06080a');
  f += rain(4500, 21, 520, '#d5e6e8', .3, 90);
  return { w: W, fw: 4500, bw: 2400, defs: D, bg, main: m + rain(W, 19, 380, '#c7dadc', .2, 60), fore: f, spots: sp, ground: 792, amb: 'town' }; };
if (typeof module !== 'undefined') module.exports = { SC, SK, rnd, R1, svgw, rect, ln, pf, tx, glow, lamp, hatch, trunk, fern, rain, carSide };
