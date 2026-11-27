/* ---------- backgrounds, part 4: the crime lab at prefectural headquarters; the investigation headquarters set up in the Kiribuchi station ---------- */
(() => {
  const st = `stroke="${SK.ink}" stroke-width="2.5"`, st2 = `stroke="${SK.ink}" stroke-width="1.8"`, rr = rnd(404);
  const DEF = `<linearGradient id="lwg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".34"/><stop offset=".4" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".2"/></linearGradient><linearGradient id="llc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e8f6ff" stop-opacity=".3"/><stop offset="1" stop-color="#e8f6ff" stop-opacity="0"/></linearGradient><radialGradient id="lvg" cx=".5" cy=".5" r=".75"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>` + glow('lg1', '#bfe6ff', .5) + glow('lg2', '#ffe9a8', .7) + glow('lg3', '#7de0a0', .8);
  const bench = (x, w, c = '#d7dde0') => rect(x, 632, w, 16, c, st) + rect(x + 8, 648, w - 16, 94, '#8d999e', st2) + Array.from({ length: Math.floor(w / 150) }, (_, i) => rect(x + 20 + i * 150, 662, 120, 66, '#a3aeb2', st2) + rect(x + 68 + i * 150, 690, 24, 6, '#5a666b')).join('');
  const sign = (x, t) => ln(`M${x - 80} 0 V190 M${x + 80} 0 V190`, 3, '#3d4447') + rect(x - 120, 190, 240, 54, '#1f3a4a', st) + tx(x - t.length * 15, 228, t, 30, '#e6f2f6');
  const panel = x => rect(x - 110, 60, 220, 16, '#f4fbff', st2) + `<path d="M${x - 110} 76 L${x + 110} 76 L${x + 330} 742 L${x - 330} 742 Z" fill="url(#llc)"/>`;
  const bottle = (x, y, h, c) => rect(x, y - h, 16, h, c, st2) + rect(x + 4, y - h - 8, 8, 8, '#e9ebe6', st2);
  const monitor = (x, y, w, h, body) => rect(x, y, w, h, '#14191d', st) + rect(x + 6, y + 6, w - 12, h - 12, '#0e2530') + body + rect(x + w / 2 - 8, y + h, 16, 14, '#2a3035') + rect(x + w / 2 - 34, y + h + 12, 68, 6, '#2a3035', st2);
  const stool = x => rect(x - 26, 700, 52, 12, '#3d4447', st) + ln(`M${x} 712 V750 M${x - 24} 756 L${x} 742 L${x + 24} 756`, 5, '#22282a');
  SC.lab = e => { const W = 2400, sp = { out: 130, gcms: 470, himuro: 700, scope: 1130, tate: 1340, kuze: 1980, server: 2210 };
    let m = rect(0, 0, W, 742, '#aebbc0') + `<rect x="0" y="0" width="${W}" height="742" fill="url(#lwg)"/>` + rect(0, 0, W, 60, '#8f9da2') + rect(0, 600, W, 142, '#98a7ac', 'opacity=".6"') + ln(`M0 600 H${W}`, 3, '#000', 'opacity=".25"') + rect(0, 742, W, 16, '#3a4347', st2) + rect(0, 758, W, 142, '#566267');
    { let d = ''; for (let x = 0; x < W; x += 120) d += `M${x} 758 L${x - 60} 900 `; for (const y of [790, 830, 876]) d += `M0 ${y} H${W} `; m += ln(d, 1.4, '#000', 'opacity=".28"'); }
    m += [520, 1200, 1880].map(panel).join('');
    // door, coat rack, notice
    m += rect(60, 420, 140, 322, '#5a6a70', st) + rect(76, 440, 108, 120, '#8fb0b8', st2) + `<circle cx="176" cy="590" r="7" fill="#c9cfd2" ${st2}/>` + rect(80, 380, 100, 34, '#e9e6d8', st2) + tx(96, 405, '出口', 22) + rect(230, 300, 120, 160, '#f1f3ee', st) + ln('M244 326 h92 M244 346 h92 M244 366 h70 M244 396 h92 M244 416 h60', 2, '#6a7478') + tx(244, 448, '白衣着用', 18, '#b3261e');
    // forensic medicine and chemistry
    m += sign(600, '法医・化学') + bench(380, 620);
    m += rect(398, 500, 150, 132, '#e3e8ea', st) + rect(408, 512, 86, 54, '#10303c', st2) + ln('M414 552 l12 -18 l10 12 l14 -26 l12 20 l14 -10', 2.2, '#7de0a0') + rect(504, 512, 34, 110, '#c5cdd0', st2) + [0, 1, 2].map(i => `<circle cx="521" cy="${528 + i * 26}" r="6" fill="${['#7de0a0', '#e3aa4c', '#c5cdd0'][i]}" ${st2}/>`).join('') + ln('M548 600 q30 0 30 32', 3, '#6a7478') + rect(408, 580, 86, 42, '#b9c2c6', st2) + tx(414, 608, 'GC-MS', 20, '#3d4447', 'font-family="sans-serif"');
    m += rect(600, 400, 360, 12, '#8d999e', st2) + rect(600, 490, 360, 12, '#8d999e', st2) + Array.from({ length: 12 }, (_, i) => bottle(612 + i * 28, 400, 34 + Math.floor(rr() * 30), ['#b98a6a', '#8fb0b8', '#e9c377', '#9bc49f', '#c9a0b8'][i % 5])).join('') + Array.from({ length: 11 }, (_, i) => bottle(616 + i * 30, 490, 30 + Math.floor(rr() * 34), ['#e9ebe6', '#8a6a4a', '#8fb0b8', '#d9d2b0'][i % 4])).join('');
    m += pf('M800 632 h70 v-10 h-22 l-6 -70 h-10 l-8 -30 h-16 l10 38 l-10 6 l10 56 h-18 Z', '#3d4447', 2.5) + `<circle cx="808" cy="520" r="12" fill="#22282a" ${st2}/>` + rect(790, 606, 60, 8, '#c5cdd0', st2);
    m += rect(880, 566, 90, 66, '#dfe5e7', st) + `<circle cx="925" cy="596" r="24" fill="#3d4447" ${st2}/><circle cx="925" cy="596" r="8" fill="#8d999e"/>` + Array.from({ length: 6 }, (_, i) => rect(628 + i * 22, 596, 12, 36, '#f4fbff', st2) + rect(628 + i * 22, 616, 12, 16, ['#b3261e', '#b3261e', '#e3aa4c', '#7a9fb8', '#b3261e', '#9bc49f'][i])).join('') + rect(620, 628, 140, 6, '#5a666b', st2);
    // physics and documents
    m += sign(1280, '物理・文書') + bench(1060, 590);
    m += pf('M1090 632 h110 v-12 h-36 v-60 h30 v-16 h-30 v-34 h-16 v34 h-30 v16 h30 v60 h-58 Z', '#30373b', 2.5) + rect(1096, 596, 36, 10, '#c5cdd0', st2) + rect(1158, 596, 36, 10, '#c5cdd0', st2) + `<circle cx="1147" cy="500" r="10" fill="#8fb0b8" ${st2}/>`;
    m += [0, 1, 2, 3].map(i => `<circle cx="${1250 + i * 78}" cy="330" r="30" fill="#f1eedf" stroke="#3a2a1c" stroke-width="5"/>` + ln(`M${1250 + i * 78} 330 l${[10, -14, 0, 16][i]} ${[-18, -10, -22, 8][i]} M${1250 + i * 78} 330 l${[-12, 8, 14, -6][i]} ${[6, 14, 4, -16][i]}`, 3)).join('') + rect(1210, 380, 320, 8, '#8d999e', st2);
    m += rect(1300, 612, 150, 20, '#2a3035', st) + Array.from({ length: 7 }, (_, i) => `<circle cx="${1316 + i * 20}" cy="622" r="${5 + (i % 3)}" fill="#c9a94e" ${st2}/>`).join('') + ln('M1470 632 l-8 -60 l26 -8', 4, '#30373b') + `<circle cx="1490" cy="562" r="16" fill="none" stroke="#30373b" stroke-width="5"/>`;
    m += rect(1520, 596, 110, 36, '#f6fbe8', st) + lamp(1575, 610, 110, 'lg2') + rect(1536, 602, 78, 22, '#d8c9a0', st2) + `<circle cx="1575" cy="613" r="8" fill="none" ${st2}/>` + ln('M1542 608 h20 M1590 618 h18', 1.5, '#6a5a3a');
    // digital forensics
    m += sign(1960, '情報') + rect(1740, 632, 390, 14, '#3d4447', st) + rect(1752, 646, 16, 96, '#2a3035', st2) + rect(2102, 646, 16, 96, '#2a3035', st2);
    m += monitor(1756, 500, 120, 96, Array.from({ length: 5 }, (_, i) => rect(1766 + i * 4, 512 + i * 4, 84, 56, '#3f6a7a', `opacity="${.25 + i * .12}" ${st2}`)).join('') + tx(1790, 566, '··87', 26, '#e6f2f6', 'font-family="sans-serif"'));
    m += monitor(1884, 480, 130, 116, ln('M1896 560 l10 -30 l8 30 l10 -44 l8 44 l10 -24 l8 24 l10 -36 l8 36 l10 -18 l8 18 l8 -10', 2, '#7de0a0') + ln('M1896 520 h110', 1, '#3f6a7a') + [0, 1].map(i => ln(`M${1920 + i * 46} 500 v18 l-8 16 M${1920 + i * 46} 518 l8 16 M${1912 + i * 46} 506 h16`, 2, '#e3aa4c')).join(''));
    m += monitor(2022, 500, 104, 96, Array.from({ length: 6 }, (_, i) => ln(`M2034 ${514 + i * 12} h${50 + Math.floor(rr() * 36)}`, 2, i % 2 ? '#7de0a0' : '#8fb0b8')).join('')) + rect(1790, 618, 140, 12, '#22282a', st2) + rect(1960, 620, 40, 10, '#22282a', st2) + lamp(1940, 540, 240, 'lg1');
    m += rect(2150, 330, 130, 412, '#1c2226', st) + Array.from({ length: 9 }, (_, i) => rect(2160, 344 + i * 43, 110, 34, '#2a3035', st2) + [0, 1, 2].map(j => `<circle cx="${2172 + j * 14}" cy="${361 + i * 43}" r="3.4" fill="${(i + j) % 3 ? '#7de0a0' : '#e3aa4c'}"/>`).join('') + ln(`M2220 ${361 + i * 43} h40`, 2, '#3d4447')).join('') + lamp(2215, 520, 150, 'lg3');
    m += stool(640) + stool(1400) + stool(1830) + rect(2310, 600, 60, 142, '#8d999e', st) + rect(2316, 560, 48, 40, '#3f6a4a', st2) + pf('M2322 560 q18 -60 36 0 Z', '#2f5a3e', 2);
    m += `<rect x="0" y="0" width="${W}" height="900" fill="url(#lvg)"/>`;
    return { w: W, fw: W + 600, bw: W, defs: DEF, bg: '', main: m, fore: rect(-50, 0, 90, 900, '#0d0f11') + rect(W + 500, 0, 120, 900, '#0d0f11'), spots: sp, ground: 792, amb: 'room', inside: 1 }; };
  /* the headquarters: the case name on a long paper, the table where the meeting is held, the tray where warrant requests are written */
  const police0 = SC.police; SC.police = e => { const r = police0(e); if (e !== 2026) return r; const col = (x, t) => [...t].map((c, i) => tx(x, 300 + i * 33, c, 28, '#151515')).join('');
    r.main += rect(1452, 258, 100, 330, '#f6f3e6', st) + col(1462, '旅館経営者殺人事件') + col(1508, '特別捜査本部') + ln('M1452 258 h100', 6, '#3a2a1c')
      + rect(1420, 664, 190, 14, '#6f7a7c', st) + rect(1432, 678, 14, 80, '#4f595c', st2) + rect(1584, 678, 14, 80, '#4f595c', st2) + rect(1450, 652, 54, 12, '#f6f3e6', st2) + rect(1530, 650, 50, 14, '#cfe1e3', st2) + ln('M1516 664 v-40 l14 -8', 3, '#22282a')
      + rect(676, 604, 62, 30, '#8a3f38', st2) + rect(682, 596, 50, 8, '#f6f3e6', st2) + tx(684, 626, '令状', 20, '#f6f3e6');
    r.spots = Object.assign({}, r.spots, { war: 705, mtg: 1520 }); return r; };
})();
