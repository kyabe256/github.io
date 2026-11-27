/* ---------- backgrounds, part 2: rooms, the plant, the mansion, the drain tunnel ---------- */
const SCB = (() => { const S = {};
  const st = `stroke="${SK.ink}" stroke-width="3"`, st2 = `stroke="${SK.ink}" stroke-width="2.2"`;
  const room = (W, wall, floor, base = '#2a2420') => rect(0, 0, W, 900, wall) + rect(0, 742, W, 16, base, st2) + rect(0, 758, W, 142, floor) + hatch(0, 770, W, 120, Math.round(W / 60), '#000', .12, 40);
  const windowR = (x, y, w, h, night = 1) => rect(x, y, w, h, night ? '#1b2a33' : '#8fb0b8', st) + rain(w, x, 26, '#cfe1e3', .5, 60).replace('<path', `<path transform="translate(${x} ${y - 300}) scale(1 ${(h + 300) / 900})"`) + ln(`M${x + w / 2} ${y} v${h} M${x} ${y + h / 2} h${w}`, 4, '#3a3028') + rect(x - 8, y + h, w + 16, 12, '#3a3028', st2);
  const desk = (x, w, c = '#5a4632') => rect(x, 640, w, 18, c, st) + rect(x + 10, 658, 16, 100, c, st2) + rect(x + w - 26, 658, 16, 100, c, st2) + rect(x + 30, 658, w - 60, 46, mix(c, -18), st2);
  const mix = (c, d) => '#' + [1, 3, 5].map(i => Math.max(0, Math.min(255, parseInt(c.slice(i, i + 2), 16) + d)).toString(16).padStart(2, '0')).join('');
  const shelf = (x, w, h, c, rr, books = 1) => { let s = rect(x, 742 - h, w, h, c, st); const rows = Math.floor(h / 96); for (let i = 0; i < rows; i++){ const y = 742 - h + 10 + i * 96; s += rect(x + 8, y + 82, w - 16, 8, mix(c, -30)); if (books) for (let bx = x + 12; bx < x + w - 24;){ const bw = 12 + rr() * 16, bh = 50 + rr() * 30; s += rect(bx, y + 82 - bh, bw, bh, ['#7a5a3a', '#4f6b63', '#8a3f38', '#c9b98a', '#3f5a7a', '#6a6a6a'][Math.floor(rr() * 6)], `stroke="${SK.ink}" stroke-width="1.5"`); bx += bw + 1; } } return s; };
  const door = (x, c = '#4a3a2a', label) => rect(x - 70, 420, 140, 322, c, st) + `<circle cx="${x + 46}" cy="590" r="7" fill="#c9a94e" stroke="${SK.ink}" stroke-width="2"/>` + rect(x - 54, 440, 108, 120, mix(c, 14), st2) + (label ? rect(x - 50, 380, 100, 34, '#e9e6d8', st2) + tx(x - 40, 405, label, 20) : '');
  const hang = (x, y, r, id, c = '#e9c377') => ln(`M${x} 0 L${x} ${y - 16}`, 2.5) + pf(`M${x - 34} ${y} L${x - 14} ${y - 20} L${x + 14} ${y - 20} L${x + 34} ${y} Z`, '#2d3a35', 2.5) + `<ellipse cx="${x}" cy="${y + 2}" rx="20" ry="6" fill="${c}"/>` + lamp(x, y + 40, r, id);
  const D = glow('ig1', '#f1c777', .5) + glow('ig2', '#cfe6ea', .4) + glow('ig3', '#ff9a4a', .6);
  /* ----- police ----- */
  S.police = e => { const W = 2100, rr = rnd(5 + e), sp = { out: 130, pc: 520, desk: 900, board: 1280, archive: 1750 };
    const wall = e === 1960 ? '#6b5d48' : e === 1993 ? '#8f9488' : '#8a9aa0';
    let m = room(W, wall, e === 1960 ? '#4a3c2c' : '#5b6468') + rect(0, 0, W, 60, mix(wall, -24)) + door(130, e === 1960 ? '#4a3a2a' : '#5a6468', '出口');
    m += windowR(300, 250, 190, 230) + hang(620, 150, 330, 'ig1') + hang(1400, 150, 330, 'ig1');
    m += desk(380, 330, e === 1960 ? '#5a4632' : '#6f7a7c') + desk(780, 330, e === 1960 ? '#5a4632' : '#6f7a7c');
    if (e === 2026) m += rect(470, 548, 130, 86, '#1b2228', st) + rect(480, 556, 110, 66, '#9fd0e6') + rect(524, 634, 22, 8, '#30383c') + rect(430, 626, 70, 10, '#d9d7cd', st2) + rect(860, 548, 120, 86, '#1b2228', st) + rect(870, 556, 100, 66, '#35505c');
    if (e === 1993) m += rect(470, 536, 110, 100, '#c9c2ae', st) + rect(482, 548, 86, 62, '#31503f') + rect(600, 610, 80, 26, '#d9d2bd', st2) + rect(880, 600, 70, 38, '#2a2a2a', st) + ln('M950 618 q30 -30 50 10', 3);
    if (e === 1960) m += rect(480, 596, 60, 42, '#1d1d1d', st) + `<circle cx="510" cy="612" r="16" fill="#2a2a2a" stroke="${SK.ink}" stroke-width="2"/>` + rect(880, 610, 110, 26, '#d8d2bd', st2) + pf('M640 742 L650 520 L700 520 L710 742 Z', '#3a3a3a', 3) + rect(662, 540, 26, 40, '#ff9a4a') + lamp(675, 560, 200, 'ig3') + ln('M675 520 L675 60', 12, '#3a3a3a');
    m += rect(800, 600, 60, 40, '#e9e6d8', st2) + ln('M810 612 h40 M810 622 h40 M810 632 h28', 1.5); // open notebook on the second desk
    // board
    m += rect(1150, 260, 280, 250, e === 1960 ? '#3f4a3a' : '#d9d7cd', st) + (e === 1960 ? tx(1170, 310, '火の用心', 30, '#e6e2d2') + tx(1170, 360, '流言に注意', 26, '#e6e2d2') : [0, 1, 2, 3, 4, 5].map(i => rect(1166 + (i % 3) * 86, 280 + Math.floor(i / 3) * 110, 70, 90, ['#f1efe6', '#e9c377', '#f1efe6', '#cfe1e3', '#f1efe6', '#e7b7a8'][i], st2)).join('') + ln('M1200 330 L1290 410 L1380 320', 2, '#b3261e'));
    m += shelf(1600, 330, 480, e === 1960 ? '#4a3a2a' : '#59646a', rr) + rect(1610, 232, 310, 30, '#e9e6d8', st2) + tx(1640, 256, e === 1960 ? '日誌・台帳' : '書庫（過去の事件）', 22);
    m += rect(1960, 420, 120, 322, '#3d4447', st) + [0, 1, 2, 3, 4].map(i => rect(1972 + i * 22, 430, 8, 300, '#22282a')).join('');
    return { w: W, fw: W + 600, bw: W, defs: D, bg: '', main: m, fore: rect(-50, 0, 90, 900, '#0d0f11') + rect(W + 500, 0, 120, 900, '#0d0f11'), spots: sp, ground: 792, amb: 'room', inside: 1 }; };
  /* ----- clinic ----- */
  S.clinic = e => { const W = 1900, rr = rnd(15), sp = { out: 130, desk: 640, light: 1000, shelf: 1320, bed: 1660 };
    let m = room(W, e === 1960 ? '#a89c84' : '#c3d0cc', e === 1960 ? '#5a4a36' : '#7f9a94') + door(130, '#e9ebe6', '出口') + windowR(300, 250, 170, 230) + hang(760, 150, 340, 'ig1') + hang(1500, 150, 300, 'ig1');
    m += desk(520, 320, '#b9a37a') + rect(560, 590, 90, 50, '#f1efe6', st2) + ln('M570 604 h64 M570 616 h64 M570 628 h40', 1.5) + rect(700, 560, 60, 78, '#31404a', st) + pf('M870 742 L880 620 L960 620 L970 742 Z', '#3f6a6a', 3) + rect(870, 560, 100, 64, '#3f6a6a', st);
    m += rect(940, 300, 150, 190, '#e9f1f2', st) + pf('M970 330 q40 -10 60 20 q10 40 -20 80 q-30 20 -50 -10 Z', '#9fb4b8', 2) + ln('M1000 350 l0 110 M985 380 l30 0 M985 410 l30 0', 2, '#5d6b6d') + lamp(1015, 395, 150, 'ig2');
    m += shelf(1200, 250, 400, '#b9a37a', rr) + rect(1210, 320, 230, 26, '#e9e6d8', st2) + tx(1226, 341, 'カルテ', 20);
    m += rect(1520, 640, 300, 26, '#e9ebe6', st) + rect(1530, 666, 14, 92, '#8b9597', st2) + rect(1796, 666, 14, 92, '#8b9597', st2) + pf('M1520 640 L1520 600 Q1560 590 1600 640 Z', '#d6dedd', 2.5) + ln('M1860 300 L1860 742', 5, '#8b9597') + pf('M1830 320 L1890 320 L1880 400 L1840 400 Z', '#cfe1e3', 2.5);
    return { w: W, fw: W + 600, bw: W, defs: D, bg: '', main: m, fore: rect(-50, 0, 90, 900, '#0d0f11') + rect(W + 500, 0, 120, 900, '#0d0f11'), spots: sp, ground: 792, amb: 'room', inside: 1 }; };
  /* ----- inn ----- */
  S.inn = e => { const W = 2500, rr = rnd(25), sp = { out: 130, front: 620, ledger: 1010, hearth: 1480, luggage: 2000, safe: 2300 };
    let m = room(W, '#8a7355', '#6b5236', '#3a2a1c') + rect(0, 0, W, 70, '#3a2a1c') + [300, 760, 1220, 1760, 2240].map(x => rect(x, 70, 22, 672, '#3a2a1c', st2)).join('');
    m += rect(60, 420, 150, 322, '#d9cdb0', st) + ln('M135 420 V742 M60 520 H210 M60 620 H210', 2.5, '#3a2a1c') + tx(96, 400, '玄関', 24, '#e9e6d8') + hang(700, 160, 360, 'ig1') + hang(1500, 130, 300, 'ig1') + hang(2150, 160, 330, 'ig1');
    // front desk with bell, key board
    m += rect(430, 610, 380, 132, '#4a3420', st) + rect(420, 596, 400, 18, '#5f4630', st) + pf('M520 596 q14 -26 28 0 Z', '#c9a94e', 2.2) + rect(590, 566, 120, 30, '#e9e6d8', st2) + ln('M600 576 h100 M600 586 h80', 1.5);
    m += rect(470, 300, 300, 190, '#3a2a1c', st) + Array.from({ length: 12 }, (_, i) => `<circle cx="${500 + (i % 6) * 48}" cy="${340 + Math.floor(i / 6) * 70}" r="4" fill="#c9a94e"/>` + rect(497 + (i % 6) * 48, 344 + Math.floor(i / 6) * 70, 6, 26, i % 5 ? '#b9a37a' : '#3a2a1c')).join('');
    if (e === 1993) m += rect(760, 560, 70, 40, '#e88aa0', st) + `<circle cx="795" cy="580" r="13" fill="#2a2a2a"/>`;
    if (e === 2026) m += rect(740, 520, 80, 76, '#1b2228', st) + rect(748, 528, 64, 52, '#9fd0e6');
    // old ledgers
    m += shelf(900, 230, 300, '#4a3420', rr) + rect(910, 420, 210, 26, '#e9e6d8', st2) + tx(926, 441, e === 1960 ? '宿帳' : '古い宿帳', 20);
    // hearth / stove / tv corner
    if (e === 1960) m += rect(1340, 716, 300, 26, '#2a1c12', st) + rect(1370, 700, 240, 18, '#1a1410', st2) + pf('M1470 700 q20 -50 40 0 Z', '#ff9a4a', 0) + lamp(1490, 680, 260, 'ig3') + ln('M1490 0 V600', 4, '#1a1410') + pf('M1466 600 h48 l-8 50 h-32 Z', '#2a2a2a', 3) + rect(1680, 560, 110, 80, '#5a4632', st) + `<circle cx="1716" cy="600" r="22" fill="#2a2018" stroke="${SK.ink}" stroke-width="2.5"/>`;
    else m += rect(1360, 660, 260, 82, '#4a3420', st) + (e === 1993 ? rect(1400, 540, 180, 120, '#3a3a3a', st) + rect(1414, 552, 124, 96, '#5f8f9a') : rect(1380, 520, 220, 130, '#15191c', st) + rect(1388, 528, 204, 114, '#2f4a55')) + rect(1700, 690, 120, 52, '#7a2f28', st) + rect(1690, 680, 140, 14, '#8a3f38', st2);
    // guest room corner: luggage on tatami, safe
    m += rect(1880, 742, 520, 16, '#b9a86a', st2) + rect(1940, 690, 150, 52, e === 1993 ? '#3f5a7a' : '#6a5a3a', st) + ln('M1940 708 h150', 2) + rect(1996, 676, 38, 16, '#2a2a2a', st2) + (e === 1993 ? rect(2100, 716, 70, 26, '#1b1b1b', st2) : '');
    m += rect(2240, 600, 130, 142, '#4d5557', st) + `<circle cx="2305" cy="670" r="26" fill="#2a3032" stroke="${SK.ink}" stroke-width="3"/>` + ln('M2305 650 v40 M2285 670 h40', 3) + windowR(2060, 250, 170, 220);
    return { w: W, fw: W + 600, bw: W, defs: D, bg: '', main: m, fore: rect(-50, 0, 90, 900, '#0d0f11') + rect(W + 500, 0, 120, 900, '#0d0f11'), spots: sp, ground: 792, amb: 'room', inside: 1 }; };
  /* ----- the plant: gate and the main building (1960: the construction site) ----- */
  S.plant = e => { const W = 3200, rr = rnd(45), sp = { car: 240, gate: 620, guard: 900, board: 1340, door: 1820, tent: 1500, hut: 2250, crane: 2700 };
    const Dp = D + `<linearGradient id="psky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#141c22"/><stop offset=".6" stop-color="#36474d"/><stop offset="1" stop-color="#66777a"/></linearGradient>`;
    let bg = rect(0, 0, 2300, 900, 'url(#psky)') + pf('M0 600 L260 500 L520 580 L800 470 L1100 560 L1400 480 L1700 570 L2000 500 L2300 560 L2300 900 L0 900 Z', '#22303a', 0);
    if (e === 1960) bg += ln('M900 620 V200 L1240 250 M900 200 L760 330 M1500 620 V280 L1740 320', 9, '#1a242c') + ln('M1120 235 V420', 3, '#1a242c') + rect(1100, 420, 40, 30, '#1a242c');
    else bg += pf('M760 620 V330 A170 170 0 0 1 1100 330 V620 Z', '#26343e', 0) + rect(1120, 420, 520, 200, '#22303a') + rect(1700, 120, 34, 500, '#22303a') + `<circle cx="1717" cy="124" r="7" fill="#c9412f"/>` + (e === 2026 ? ln('M760 330 L1100 560 M1100 330 L760 560 M760 440 H1100', 4, '#3d515c') + ln('M1240 420 V240 L1500 280', 8, '#1a242c') : lamp(930, 380, 330, 'ig2'));
    let m = rect(0, 770, W, 130, '#1d2326') + rect(0, 760, W, 14, '#454d50');
    if (e === 1960){ // mud, fence, tent with the ledger table, bunkhouse, crane foot
      m = rect(0, 770, W, 130, '#2a2620') + pf(`M0 800 C600 780 1400 820 ${W} 790 L${W} 900 L0 900 Z`, '#1c1915', 0);
      for (let x = 380; x < W; x += 150) m += rect(x, 600, 14, 172, '#4a3a2a', st2); m += ln(`M380 640 H${W} M380 700 H${W}`, 5, '#4a3a2a');
      m += rect(560, 430, 130, 80, '#d8d2bd', st) + tx(572, 464, '霧渕発電所', 20) + tx(572, 494, '建設用地 鷹取組', 14) + rect(618, 510, 14, 262, '#4a3a2a', st2);
      m += pf('M1300 560 L1500 470 L1700 560 Z', '#8a8266', 3) + ln('M1320 560 V772 M1680 560 V772', 8, '#4a3a2a') + rect(1400, 660, 200, 14, '#5a4632', st) + rect(1410, 674, 12, 98, '#5a4632', st2) + rect(1578, 674, 12, 98, '#5a4632', st2) + rect(1440, 636, 90, 24, '#e9e6d8', st2) + hang(1500, 560, 240, 'ig1');
      m += rect(2050, 500, 420, 272, '#4a3f30', st) + pf('M2020 500 L2260 410 L2500 500 Z', '#2a241c', 3) + rect(2200, 600, 110, 172, '#1d1812', st) + rect(2090, 560, 80, 70, '#e9c377', st) + rect(2360, 560, 80, 70, '#1b2228', st) + tx(2190, 560, '鷹取組 飯場', 22, '#e6e2d2') + lamp(2130, 600, 170, 'ig1');
      m += pf('M2620 772 L2680 300 L2740 772 Z', '#2a2e30', 3) + ln('M2640 620 H2720 M2650 500 H2710 M2660 400 H2700', 4) + rect(2850, 690, 220, 82, '#3f3a30', st) + [0, 1, 2].map(i => `<circle cx="${2890 + i * 70}" cy="690" r="34" fill="#55504a" stroke="${SK.ink}" stroke-width="3"/>`).join('');
    } else { // fence, gate, guard box, notice board, office block
      for (let x = 0; x < W; x += 110) m += rect(x, 560, 8, 212, '#51585a'); m += ln(`M0 580 H520 M720 580 H${W}`, 4, '#51585a') + hatch(0, 590, 520, 170, 40, '#8b9597', .25, 30) + hatch(720, 590, W - 720, 170, 180, '#8b9597', .25, 30);
      m += rect(500, 480, 30, 292, '#3d4447', st) + rect(710, 480, 30, 292, '#3d4447', st) + rect(470, 410, 300, 70, '#e9e6d8', st) + tx(490, 456, '霧渕原子力発電所', 30, '#1c3a55') + (e === 2026 ? rect(486, 494, 268, 40, '#e3c23a', st2) + tx(500, 522, '廃止措置工事中', 24, '#111') : '');
      m += rect(820, 560, 170, 212, '#b9c2c4', st) + rect(810, 546, 190, 18, '#3d4447', st) + rect(840, 600, 90, 80, '#e9c377', st) + lamp(885, 640, 190, 'ig1') + rect(1240, 520, 200, 150, '#e9e6d8', st) + rect(1330, 670, 14, 102, '#51585a', st2) + ln('M1260 550 h160 M1260 576 h160 M1260 602 h120 M1260 628 h140', 3, '#55606a');
      m += rect(1560, 330, 900, 442, e === 2026 ? '#8e989a' : '#b3bcbc', st) + rect(1550, 314, 920, 22, '#3d4447', st) + Array.from({ length: 12 }, (_, i) => rect(1600 + (i % 6) * 140, 370 + Math.floor(i / 6) * 120, 96, 76, (i * 7 + e) % 4 === 0 ? '#e9c377' : '#1b2a33', st2)).join('') + rect(1740, 600, 180, 172, '#161c20', st) + ln('M1830 600 V772', 2.5) + rect(1730, 560, 200, 40, '#22282c', st) + tx(1750, 590, e === 2026 ? '廃炉管理棟' : '管理棟', 26, '#e6e2d2') + lamp(1830, 660, 260, 'ig1');
      m += rect(2540, 620, 560, 152, '#59646a', st) + [0, 1, 2, 3, 4, 5].map(i => `<circle cx="${2590 + i * 92}" cy="620" r="40" fill="#6f7a7c" stroke="${SK.ink}" stroke-width="3"/>`).join('') + ln('M2540 700 H3100', 6, '#3d4447');
    }
    let f = ''; for (const x of [900, 2600, 4000]) f += rect(x, -10, 22, 930, '#06080a'); f += rain(4100, 23, 480, '#d5e6e8', .3, 90);
    return { w: W, fw: 4100, bw: 2300, defs: Dp, bg, main: m + rain(W, 29, 360, '#c7dadc', .2, 60), fore: f, spots: sp, ground: 792, amb: 'town' }; };
  /* ----- the Takatori house: study ----- */
  S.mansion = e => { const W = 2400, rr = rnd(55), sp = { out: 130, photo: 760, desk: 1240, cane: 1700, monitor: 2060 };
    let m = room(W, '#5c4a40', '#3f2c24', '#2a1c16') + rect(0, 0, W, 70, '#2a1c16') + rect(0, 520, W, 222, '#4a3830') + hatch(0, 530, W, 200, 60, '#000', .15, 0) + door(130, '#3a2a20', '玄関') + hang(1000, 150, 380, 'ig1') + hang(1900, 150, 330, 'ig1');
    m += windowR(300, 210, 210, 270);
    // portrait photograph: the old man with a hawk-headed cane
    m += rect(650, 220, 220, 280, '#3a2a1c', st) + rect(668, 238, 184, 244, '#c9c2ae', st2) + `<circle cx="760" cy="300" r="34" fill="#8a8478" stroke="${SK.ink}" stroke-width="2.5"/>` + pf('M700 482 L712 360 Q760 330 808 360 L820 482 Z', '#3b3a45', 2.5) + ln('M826 380 L826 482', 5, '#2a1c16') + pf('M812 368 q14 -18 30 -4 q-4 10 -14 10 l-2 10 Z', '#c9a94e', 2);
    // fireplace
    m += rect(950, 560, 220, 182, '#2a2a2a', st) + rect(930, 540, 260, 26, '#6a5a50', st) + rect(990, 620, 140, 122, '#0c0c0c', st2) + pf('M1030 742 q30 -80 60 0 Z', '#ff9a4a', 0) + lamp(1060, 690, 240, 'ig3');
    // desk with papers, chair
    m += rect(1140, 630, 360, 22, '#3a2416', st) + rect(1150, 652, 340, 90, '#4a3020', st) + rect(1220, 600, 120, 30, '#e9e6d8', st2) + ln('M1230 610 h100 M1230 620 h70', 1.5) + rect(1380, 560, 30, 70, '#2f5a48', st2) + pf('M1385 560 q10 -26 20 0 Z', '#e9c377', 2) + lamp(1395, 560, 150, 'ig1');
    m += pf('M1560 742 L1570 520 Q1620 490 1670 520 L1680 742 Z', '#5a2f2a', 3);
    // umbrella and cane stand (one plain cane; the hook for the old one is empty)
    m += rect(1660 + 30, 640, 90, 102, '#2a2a2a', st) + ln('M1720 640 V520 q0 -22 20 -22', 5, '#1a1410') + ln('M1750 640 V540', 5, '#6a4a2a') + rect(1690, 420, 100, 16, '#3a2416', st2) + ln('M1716 436 v20 M1764 436 v20', 4, '#c9a94e');
    m += shelf(1850, 150, 420, '#3a2416', rr) + rect(2010, 520, 150, 100, '#1b2228', st) + rect(2020, 530, 130, 80, '#2f4a55') + ln('M2020 570 h130 M2085 530 v80', 1.5, '#9fd0e6') + rect(2030, 620, 110, 122, '#3a2416', st) + tx(2018, 510, '門の録画', 20, '#e9e6d8');
    m += windowR(2200, 210, 160, 270);
    return { w: W, fw: W + 600, bw: W, defs: D, bg: '', main: m, fore: rect(-50, 0, 90, 900, '#0d0f11') + rect(W + 500, 0, 120, 900, '#0d0f11'), spots: sp, ground: 792, amb: 'room', inside: 1 }; };
  /* ----- the drain tunnel (1993) / the trial adit (1960) ----- */
  S.tunnel = e => { const W = 2500, rr = rnd(65), sp = { out: 130, office: 640, memo: 860, rack: 1080, valve: 1560, breach: 2280 };
    let m = rect(0, 0, W, 900, '#0c1113');
    m += pf(`M0 250 Q${W / 2} 170 ${W} 250 L${W} 792 L0 792 Z`, e === 1960 ? '#2e2a24' : '#3a4447', 3) + rect(0, 780, W, 120, '#14191b') + hatch(0, 260, W, 500, 70, '#000', .12, 20);
    m += pf('M0 792 L0 360 C70 330 170 360 200 450 C226 560 220 720 212 792 Z', '#56676a', 3) + lamp(110, 600, 320, 'ig2');
    if (e === 1960){ for (let x = 330; x < W - 200; x += 260) m += rect(x, 280, 22, 512, '#4a3a2a', st2) + rect(x - 30, 270, 82, 20, '#4a3a2a', st2); m += hang(700, 330, 260, 'ig1') + hang(1500, 330, 260, 'ig1') + ln(`M300 792 H2200`, 5, '#55504a') + ln('M300 778 H2200', 3, '#55504a') + rect(1000, 700, 200, 80, '#4a4038', st) + `<circle cx="1040" cy="780" r="20" fill="#2a2a2a"/><circle cx="1160" cy="780" r="20" fill="#2a2a2a"/>` + pf('M1520 792 l20 -120 l110 0 l10 120 Z', '#3a3a3a', 3) + ln('M1650 690 l90 -40', 8, '#6a6a6a');
      m += pf('M2160 792 C2150 620 2200 480 2290 470 C2380 470 2420 620 2424 792 Z', '#020304', 3.5) + [0, 1, 2, 3, 4].map(i => pf(`M${2140 + i * 60} 792 l20 -${30 + rr() * 40} l30 ${10} l10 ${20 + rr() * 30} Z`, '#3a362e', 2.5)).join('') + tx(2190, 440, '雨穴に抜けた穴', 20, '#d8d2bd');
    } else { // pipes along the wall, a small watch post, badge rack, the valve wheel
      m += ln(`M240 400 H${W}`, 26, '#59686b') + ln(`M240 400 H${W}`, 3) + ln(`M240 460 H${W}`, 16, '#7b4a36') + [600, 1200, 1800].map(x => rect(x, 384, 20, 96, '#3d4447', st2)).join('') + hang(520, 300, 280, 'ig1') + hang(1300, 300, 280, 'ig1') + hang(2000, 300, 280, 'ig1');
      m += rect(520, 560, 260, 222, '#6f7a7c', st) + rect(540, 580, 120, 80, '#e9c377', st) + rect(560, 690, 190, 16, '#5a4632', st) + rect(600, 664, 90, 26, '#e9e6d8', st2) + ln('M610 672 h70 M610 682 h50', 1.5) + rect(800, 600, 110, 70, '#d8d2bd', st) + ln('M812 616 h86 M812 630 h86 M812 644 h60', 2, '#7a1f18');
      m += rect(1000, 540, 170, 150, '#3d4447', st) + Array.from({ length: 6 }, (_, i) => rect(1016 + (i % 3) * 50, 556 + Math.floor(i / 3) * 62, 36, 46, i < 3 ? '#c9412f' : '#e9e6d8', st2)).join('') + tx(1004, 530, 'フィルムバッジ', 18, '#e9e6d8');
      m += ln('M1560 400 V560', 30, '#59686b') + ln('M1560 400 V560', 3) + `<circle cx="1560" cy="600" r="74" fill="none" stroke="#8a2f24" stroke-width="16"/><circle cx="1560" cy="600" r="74" fill="none" stroke="${SK.ink}" stroke-width="2.5"/><circle cx="1560" cy="600" r="16" fill="#8a2f24" stroke="${SK.ink}" stroke-width="2.5"/>` + ln('M1486 600 H1634 M1560 526 V674', 9, '#8a2f24');
      m += pf('M1700 792 q40 -160 120 -200 q-40 100 -20 200 Z', '#e6eef0', 0, 'opacity=".25"') + pf('M1640 400 q60 -80 140 -60 q-80 20 -100 100 Z', '#e6eef0', 0, 'opacity=".3"');
      m += rect(2150, 300, 240, 492, '#2a3032', st) + hatch(2160, 320, 220, 460, 10, '#000', .4, 0) + tx(2176, 290, '森の側の出口', 20, '#d8d2bd');
    }
    return { w: W, fw: W + 600, bw: W, defs: D, bg: '', main: m, fore: pf('M-100 0 H140 L60 420 L-100 900 Z', '#050708', 0) + pf(`M${W + 380} 0 H${W + 640} V900 H${W + 460} Z`, '#050708', 0), spots: sp, ground: 792, amb: 'cave', inside: 1, dark: 1 }; };
  return S; })();
Object.assign(SC, SCB);
if (typeof module !== 'undefined') module.exports = { SCB };
