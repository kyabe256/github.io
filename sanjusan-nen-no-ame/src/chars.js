/* ---------- people: inked bust portraits. viewBox 0 0 600 760, slight three-quarter view, light from the upper right ----------
   Anatomy first: skull -> jaw -> neck column (sternomastoid, pit of the neck) -> trapezius slope -> shoulder points -> clothes laid over that. */
const PORT = (() => {
  const INK = '#2a1d22';
  const r = n => Math.round(n * 10) / 10, P = (...a) => a.map(v => typeof v === 'number' ? r(v) : v).join(' ');
  const mixc = (a, b, t) => { const h = s => [1, 3, 5].map(i => parseInt(s.slice(i, i + 2), 16)), x = h(a), y = h(b); return '#' + x.map((v, i) => Math.round(v + (y[i] - v) * t).toString(16).padStart(2, '0')).join(''); };
  const EMO = { // eye opening, brow inner dy, brow outer dy, mouth kind
    n: [1, 0, 0, 'flat'], k: [.82, 3.5, -1, 'firm'], d: [.74, -4.5, 2.5, 'down'], a: [.86, 7, -3.5, 'grit'], u: [1.28, -7, -6, 'open'], s: [.72, -1, 0, 'smile'], t: [.95, -5.5, 1, 'wavy'], c: [0, 0, 1, 'flat'] };
  function build(c, emo = 'n', o = {}){
    const E = EMO[emo] || EMO.n, male = c.sex !== 'f', age = c.age || 35, kid = age < 14, old = age >= 60, mid = age >= 42, cx = 300, tx = -9;
    const fw = (kid ? 73 : male ? 81 : 74) * (c.fw || 1), top = kid ? 126 : 110, eyeY = kid ? 240 : 230, chin = (kid ? 320 : male ? 331 : 322) + (c.long || 0), fh = chin - eyeY;
    const nw = (kid ? 30 : male ? (old ? 47 : 51) : 38) * (c.nw || 1), ncx = cx + 6, sw = kid ? 102 : male ? 164 : 132, shY = kid ? 420 : male ? 426 : 420, pit = [ncx - 4, kid ? 384 : male ? 396 : 388];
    const skin = c.skin || '#fbe3cf', sh1 = mixc(skin, '#cf7f63', .34), sh2 = mixc(skin, '#a0543f', .5), hairC = c.hair || '#2c232b', hairHi = mixc(hairC, '#ffe9d6', .42), grey = c.grey || 0;
    const hc = grey ? mixc(hairC, '#d6d0cb', grey) : hairC, hInk = grey > .5 ? '#3b3f45' : INK, jw = c.jaw ?? (kid ? .1 : male ? .42 : .1);
    const L = (d, w = 2, x = '') => `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${x}/>`;
    const F = (d, fill, w = 2.6, x = '') => `<path d="${d}" fill="${fill}" stroke="${w ? INK : 'none'}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round" ${x}/>`;
    const T = (d, fill, op = 1) => `<path d="${d}" fill="${fill}" opacity="${op}"/>`;
    /* --- skeleton landmarks --- */
    const TL = [cx - fw + 7, eyeY - 30], CL = [cx - fw + 4, eyeY + 22], JL = [cx - fw + 14 + (1 - jw) * 7, eyeY + fh * .72], CHL = [cx + tx - 19 - jw * 7, chin - 5], CH = [cx + tx, chin], CHR = [cx + tx + 21 + jw * 8, chin - 5],
      JR = [cx + fw - 9 - (1 - jw) * 9, eyeY + fh * .6], CR = [cx + fw + 1, eyeY + 14], TR = [cx + fw - 1, eyeY - 34];
    const face = P('M', ...TL, 'C', TL[0] - 3, eyeY - 4, CL[0] - 1, CL[1] - 12, ...CL, 'C', CL[0] + 1, CL[1] + 22, JL[0] - 5, JL[1] - 16, ...JL, 'C', JL[0] + 6, JL[1] + 15, CHL[0] - 14, CHL[1] - 7, ...CHL, 'Q', ...CH, ...CHR,
      'C', CHR[0] + 15, CHR[1] - 4, JR[0] - 5, JR[1] + 17, ...JR, 'C', JR[0] + 8, JR[1] - 20, CR[0], CR[1] + 22, ...CR, 'C', CR[0], CR[1] - 20, TR[0] + 2, TR[1] + 12, ...TR, 'C', TR[0] - 2, top + 22, cx + 52, top, cx + 2, top, 'C', cx - 50, top, TL[0] + 2, top + 26, ...TL, 'Z');
    /* --- neck and shoulders (bare; the clothes go over) --- */
    const nL = ncx - nw, nR = ncx + nw, nbL = [nL - 3, pit[1] - 18], nbR = [nR + 4, pit[1] - 23];
    const torso = P('M', nL + 1, chin - 34, 'L', nL - 1, nbL[1] - 14, 'C', nL - 4, nbL[1] + 6, cx - sw + 78, shY - 30, cx - sw + 10, shY - 2, 'C', cx - sw - 12, shY + 6, cx - sw - 22, shY + 40, cx - sw - 26, shY + 90, 'L', cx - sw - 34, 760, 'L', cx + sw + 34, 760, 'L', cx + sw + 26, shY + 88,
      'C', cx + sw + 22, shY + 38, cx + sw + 12, shY + 4, cx + sw - 10, shY - 4, 'C', cx + sw - 78, shY - 32, nR + 5, nbR[1] + 6, nR + 2, nbR[1] - 14, 'L', nR - 1, chin - 46, 'Z');
    let neck = F(torso, skin, 2.6);
    neck += T(P('M', nL + 1, chin - 30, 'L', nR - 1, chin - 44, 'L', nR + 1, chin + (male ? 6 : 2), 'C', ncx + 20, chin + 30, ncx - 14, chin + 34, nL - 1, chin + 16, 'Z'), sh1, .6); // cast shadow of the jaw
    neck += T(P('M', nL - 1, chin + 10, 'L', nL - 2, nbL[1] + 4, 'L', nL + 9, nbL[1] + 2, 'L', nL + 7, chin + 18, 'Z'), sh1, .3); // far side of the column
    neck += L(P('M', nR - 7, chin - 24, 'C', nR - 12, chin + 14, pit[0] + 20, pit[1] - 26, pit[0] + 9, pit[1] - 3), 1.6, 'opacity=".8"'); // sternomastoid, near side
    neck += L(P('M', nL + 9, chin + 18, 'C', nL + 11, chin + 34, pit[0] - 12, pit[1] - 20, pit[0] - 8, pit[1] - 3), 1.3, 'opacity=".55"');
    neck += L(P('M', pit[0] - 9, pit[1], 'Q', pit[0], pit[1] + 7, pit[0] + 10, pit[1] - 1), 1.5, 'opacity=".7"'); // pit of the neck
    neck += L(P('M', pit[0] + 14, pit[1] + 2, 'C', pit[0] + 50, pit[1] - 4, pit[0] + 84, pit[1] + 2, cx + sw - 46, shY - 12), 1.4, 'opacity=".5"') + L(P('M', pit[0] - 13, pit[1] + 3, 'C', pit[0] - 46, pit[1] - 2, pit[0] - 80, pit[1] + 4, cx - sw + 50, shY - 8), 1.4, 'opacity=".5"'); // collarbones
    if (male && !kid) neck += L(P('M', ncx - 9, chin + 26, 'q', 5, 7, 1, 15), 1.3, 'opacity=".6"');
    if (old) neck += L(P('M', ncx - 16, chin + 20, 'L', ncx - 12, pit[1] - 16), 1, 'opacity=".4"') + L(P('M', ncx + 12, chin + 14, 'L', ncx + 6, pit[1] - 18), 1, 'opacity=".4"');
    /* --- clothes --- */
    const K = c.cloth || { t: 'shirt' }, col = K.c || '#3a4250', colS = mixc(col, '#05070a', .42), colH = mixc(col, '#ffffff', .22), white = K.w || '#e9ebe8', whS = mixc(white, '#59606e', .32);
    const bodyOut = P('M', nbL[0] - 2, nbL[1] + 2, 'C', nL - 6, nbL[1] + 14, cx - sw + 80, shY - 34, cx - sw + 6, shY - 8, 'C', cx - sw - 18, shY, cx - sw - 30, shY + 36, cx - sw - 34, shY + 92, 'L', cx - sw - 44, 760, 'L', cx + sw + 44, 760, 'L', cx + sw + 34, shY + 90,
      'C', cx + sw + 30, shY + 34, cx + sw + 18, shY - 2, cx + sw - 6, shY - 10, 'C', cx + sw - 80, shY - 36, nR + 8, nbR[1] + 14, nbR[0] + 2, nbR[1] + 2);
    const armL = L(P('M', cx - sw + 18, shY + 70, 'C', cx - sw + 26, shY + 150, cx - sw + 20, 700, cx - sw + 24, 760), 2, 'opacity=".75"'), armR = L(P('M', cx + sw - 20, shY + 66, 'C', cx + sw - 28, shY + 150, cx + sw - 24, 700, cx + sw - 26, 760), 2, 'opacity=".75"');
    const shirt = (open) => { // collar band wraps the base of the neck; wings fall from it
      let s = F(P('M', nbL[0] - 1, nbL[1] + 3, 'C', nbL[0] + 6, pit[1] + 16, pit[0] - 10, pit[1] + 40, pit[0] - 2, 760, 'L', pit[0] + 40, 760, 'C', pit[0] + 18, pit[1] + 40, nbR[0] - 4, pit[1] + 10, nbR[0] + 1, nbR[1] + 3, 'C', nbR[0] - 14, pit[1] + 2, nbL[0] + 16, pit[1] + 6, nbL[0] - 1, nbL[1] + 3, 'Z'), white, 0);
      if (open) s += F(P('M', pit[0] - 16, pit[1] + 6, 'L', pit[0] + 2, pit[1] + 62, 'L', pit[0] + 20, pit[1] + 4, 'Q', pit[0] + 2, pit[1] + 12, pit[0] - 16, pit[1] + 6, 'Z'), skin, 0) + T(P('M', pit[0] - 16, pit[1] + 6, 'L', pit[0] + 2, pit[1] + 62, 'L', pit[0] + 4, pit[1] + 30, 'Z'), sh1, .6);
      s += F(P('M', nbL[0] - 3, nbL[1] - 2, 'C', nbL[0] + 2, pit[1] - 2, pit[0] - 20, pit[1] + 8, pit[0] - 3, pit[1] + 13, 'L', pit[0] - 36, pit[1] + 52, 'L', nbL[0] - 15, nbL[1] + 16, 'Z'), white, 2.4) + T(P('M', pit[0] - 3, pit[1] + 13, 'L', pit[0] - 36, pit[1] + 52, 'L', pit[0] - 30, pit[1] + 34, 'Z'), whS, .7);
      s += F(P('M', nbR[0] + 3, nbR[1] - 2, 'C', nbR[0] - 3, pit[1] - 4, pit[0] + 24, pit[1] + 7, pit[0] + 5, pit[1] + 13, 'L', pit[0] + 42, pit[1] + 50, 'L', nbR[0] + 16, nbR[1] + 16, 'Z'), white, 2.4);
      return s; };
    const tie = (tc) => F(P('M', pit[0] - 9, pit[1] + 15, 'L', pit[0] + 11, pit[1] + 15, 'L', pit[0] + 8, pit[1] + 40, 'L', pit[0] - 6, pit[1] + 40, 'Z'), tc, 2) + F(P('M', pit[0] - 6, pit[1] + 40, 'L', pit[0] + 8, pit[1] + 40, 'L', pit[0] + 20, 760, 'L', pit[0] - 16, 760, 'Z'), tc, 2) + T(P('M', pit[0] + 1, pit[1] + 40, 'L', pit[0] + 8, pit[1] + 40, 'L', pit[0] + 20, 760, 'L', pit[0] + 4, 760, 'Z'), '#000', .22);
    const lapels = (lw = 1, notch = 1) => { const y0 = pit[1] + 34, lx = pit[0] - 40 * lw, rx = pit[0] + 46 * lw; // jacket front: V opening, lapels rolling from the collar
      let s = F(P('M', nbL[0] - 14, nbL[1] + 6, 'L', lx - 18, y0 + 26, 'L', lx - 2, y0 + 44, 'L', pit[0] - 2, 700, 'L', pit[0] - 8, 760, 'L', cx - sw + 40, 760, 'L', cx - sw + 44, shY + 30, 'Z'), col, 2.4);
      s += F(P('M', nbR[0] + 15, nbR[1] + 6, 'L', rx + 20, y0 + 22, 'L', rx + 2, y0 + 42, 'L', pit[0] + 4, 700, 'L', pit[0] + 12, 760, 'L', cx + sw - 40, 760, 'L', cx + sw - 46, shY + 28, 'Z'), col, 2.4);
      if (notch) s += L(P('M', lx - 18, y0 + 26, 'L', lx - 34, y0 + 12), 2.2) + L(P('M', rx + 20, y0 + 22, 'L', rx + 38, y0 + 8), 2.2);
      s += T(P('M', nbL[0] - 14, nbL[1] + 6, 'L', lx - 18, y0 + 26, 'L', lx - 2, y0 + 44, 'L', pit[0] - 2, 700, 'L', pit[0] - 30, 640, 'L', lx - 26, y0 + 60, 'Z'), '#000', .2);
      return s; };
    const fold = (x1, y1, x2, y2, bend = 14, w = 1.8, op = .6) => L(P('M', x1, y1, 'Q', (x1 + x2) / 2 + bend, (y1 + y2) / 2, x2, y2), w, `opacity="${op}"`);
    let cloth = '', back = '';
    const base = (fill = col) => F(bodyOut + ' Z', fill, 2.8) + T(P('M', cx - sw - 34, shY + 92, 'L', cx - sw - 44, 760, 'L', cx - sw + 46, 760, 'C', cx - sw + 30, 640, cx - sw + 34, shY + 80, cx - sw + 52, shY + 8, 'C', cx - sw + 10, shY, cx - sw - 22, shY + 30, cx - sw - 34, shY + 92, 'Z'), '#000', .26)
      + T(P('M', cx + sw - 60, shY - 14, 'C', cx + sw - 10, shY - 8, cx + sw + 16, shY + 10, cx + sw + 26, shY + 60, 'L', cx + sw + 12, shY + 54, 'C', cx + sw + 2, shY + 14, cx + sw - 20, shY - 2, cx + sw - 60, shY - 14, 'Z'), colH, .55) + armL + armR;
    if (K.t === 'suit' || K.t === 'uniform'){
      cloth = base() + shirt(false) + tie(K.tie || '#2a2f3a') + lapels(1, 1) + fold(cx - sw + 60, shY + 40, cx - sw + 90, shY + 150, -10) + fold(cx + sw - 62, shY + 36, cx + sw - 96, shY + 150, 10);
      if (K.t === 'uniform'){ cloth += F(P('M', cx - sw + 26, shY - 2, 'L', cx - sw + 92, shY - 30, 'L', cx - sw + 98, shY - 16, 'L', cx - sw + 34, shY + 14, 'Z'), colS, 2) + F(P('M', cx + sw - 26, shY - 4, 'L', cx + sw - 92, shY - 32, 'L', cx + sw - 98, shY - 18, 'L', cx + sw - 34, shY + 12, 'Z'), colS, 2)
        + `<circle cx="${cx - sw + 84}" cy="${shY - 16}" r="5" fill="#c9a94e" stroke="${INK}" stroke-width="1.5"/><circle cx="${cx + sw - 84}" cy="${shY - 18}" r="5" fill="#c9a94e" stroke="${INK}" stroke-width="1.5"/>`
        + F(P('M', cx + 62, shY + 92, 'l', 26, 0, 'l', 0, 22, 'l', -13, 10, 'l', -13, -10, 'Z'), '#c9a94e', 1.8) + L(P('M', cx - 110, shY + 96, 'l', 64, 0), 2) + L(P('M', cx - 110, shY + 96, 'l', 0, 60), 2, 'opacity=".5"'); }
    } else if (K.t === 'coat'){ // rain coat over shirt and tie; broad storm collar lying open so the neck stays readable
      cloth = base() + shirt(!K.tie) + (K.tie ? tie(K.tie) : '') + lapels(1.25, 0);
      cloth += F(P('M', nbL[0] - 10, nbL[1] - 4, 'C', nbL[0] - 34, nbL[1] + 6, pit[0] - 92, pit[1] + 36, pit[0] - 104, pit[1] + 70, 'L', pit[0] - 56, pit[1] + 96, 'L', pit[0] - 40, pit[1] + 50, 'L', nbL[0] - 12, nbL[1] + 14, 'Z'), col, 2.4) + T(P('M', pit[0] - 104, pit[1] + 70, 'L', pit[0] - 56, pit[1] + 96, 'L', pit[0] - 52, pit[1] + 80, 'Z'), '#000', .28);
      cloth += F(P('M', nbR[0] + 10, nbR[1] - 4, 'C', nbR[0] + 36, nbR[1] + 4, pit[0] + 98, pit[1] + 30, pit[0] + 112, pit[1] + 64, 'L', pit[0] + 62, pit[1] + 92, 'L', pit[0] + 46, pit[1] + 46, 'L', nbR[0] + 13, nbR[1] + 14, 'Z'), colH, 2.4);
      cloth += F(P('M', cx - sw + 22, shY + 2, 'L', cx - sw + 86, shY - 26, 'L', cx - sw + 92, shY - 12, 'L', cx - sw + 30, shY + 18, 'Z'), colS, 2) + F(P('M', cx + sw - 22, shY, 'L', cx + sw - 86, shY - 28, 'L', cx + sw - 92, shY - 14, 'L', cx + sw - 30, shY + 16, 'Z'), colS, 2);
      cloth += fold(cx - sw + 50, shY + 60, cx - sw + 84, shY + 190, -14) + fold(cx + sw - 54, shY + 56, cx + sw - 88, shY + 190, 14) + fold(pit[0] - 70, pit[1] + 130, pit[0] - 40, pit[1] + 250, 8, 1.5, .45) + `<circle cx="${pit[0] - 26}" cy="${pit[1] + 190}" r="7" fill="${colS}" stroke="${INK}" stroke-width="1.8"/><circle cx="${pit[0] + 34}" cy="${pit[1] + 186}" r="7" fill="${colS}" stroke="${INK}" stroke-width="1.8"/>`;
    } else if (K.t === 'work'){ // work jacket, low stand collar, zip, chest pocket
      cloth = base() + F(P('M', pit[0] - 22, pit[1] + 2, 'L', pit[0] + 2, pit[1] + 40, 'L', pit[0] + 26, pit[1], 'Q', pit[0] + 2, pit[1] + 10, pit[0] - 22, pit[1] + 2, 'Z'), white, 2);
      cloth += F(P('M', nbL[0] - 8, nbL[1] - 6, 'C', nbL[0] - 2, pit[1] - 2, pit[0] - 26, pit[1] + 4, pit[0] - 14, pit[1] + 30, 'L', pit[0] - 2, pit[1] + 58, 'L', pit[0] - 44, pit[1] + 40, 'L', nbL[0] - 22, nbL[1] + 12, 'Z'), colH, 2.4) + F(P('M', nbR[0] + 9, nbR[1] - 6, 'C', nbR[0] + 2, pit[1] - 4, pit[0] + 30, pit[1] + 2, pit[0] + 18, pit[1] + 28, 'L', pit[0] + 4, pit[1] + 58, 'L', pit[0] + 50, pit[1] + 36, 'L', nbR[0] + 24, nbR[1] + 12, 'Z'), colH, 2.4);
      cloth += L(P('M', pit[0] + 1, pit[1] + 58, 'L', pit[0] + 3, 760), 2.6) + L(P('M', pit[0] + 9, pit[1] + 66, 'L', pit[0] + 11, 760), 1.2, 'opacity=".5"') + F(P('M', cx + 46, shY + 84, 'l', 78, -6, 'l', 3, 64, 'l', -78, 6, 'Z'), col, 2) + L(P('M', cx + 46, shY + 100, 'l', 78, -6), 1.6)
        + (K.tag ? `<text x="${cx - 118}" y="${shY + 104}" font-size="19" font-weight="700" fill="${white}" font-family="'Zen Kaku Gothic New',sans-serif" transform="rotate(-2 ${cx - 118} ${shY + 104})">${K.tag}</text>` : '') + fold(cx - sw + 54, shY + 50, cx - sw + 84, shY + 170, -12) + fold(cx + sw - 56, shY + 46, cx + sw - 88, shY + 170, 12);
    } else if (K.t === 'kimono'){ // collars cross left over right; white under-collar hugs the neck
      const a = [nbL[0] - 16, nbL[1] + 2], b = [nbR[0] + 17, nbR[1] + 2], x = [pit[0] - 2, pit[1] + 74];
      cloth = base() + F(P('M', nbL[0] - 2, nbL[1] - 2, 'C', nbL[0] + 8, pit[1] + 10, pit[0] - 12, pit[1] + 36, x[0], x[1] - 14, 'C', pit[0] + 14, pit[1] + 36, nbR[0] - 8, pit[1] + 8, nbR[0] + 3, nbR[1] - 2, 'L', b[0], b[1], 'L', x[0] + 4, x[1] + 16, 'L', a[0], a[1], 'Z'), white, 2.2);
      cloth += F(P('M', a[0] - 12, a[1] + 6, 'L', a[0] + 4, a[1] - 6, 'C', a[0] + 30, pit[1] + 24, x[0] - 14, x[1] - 8, x[0] + 26, x[1] + 60, 'L', x[0] + 6, x[1] + 84, 'C', x[0] - 40, x[1] + 30, a[0] + 6, pit[1] + 40, a[0] - 12, a[1] + 6, 'Z'), colS, 2.4);
      cloth += F(P('M', b[0] + 12, b[1] + 6, 'L', b[0] - 4, b[1] - 6, 'C', b[0] - 30, pit[1] + 26, x[0] + 6, x[1] + 10, pit[0] - 86, 700, 'L', pit[0] - 118, 716, 'C', x[0] - 30, x[1] + 60, b[0] - 14, pit[1] + 50, b[0] + 12, b[1] + 6, 'Z'), colH, 2.4);
      if (K.apron) cloth += F(P('M', cx - sw + 30, shY + 20, 'C', cx - 90, shY + 60, cx - 60, 560, cx - 70, 760, 'L', cx + 90, 760, 'C', cx + 70, 560, cx + 96, shY + 60, cx + sw - 30, shY + 16, 'L', cx + sw + 30, shY + 96, 'L', cx + sw + 40, 760, 'L', cx - sw - 40, 760, 'L', cx - sw - 30, shY + 96, 'Z'), '#e6e7e2', 2.4, 'opacity=".96"') + fold(cx - 60, 600, cx - 40, 740, 10, 1.4, .4) + fold(cx + 70, 610, cx + 50, 740, -10, 1.4, .4);
      cloth += fold(cx - sw + 50, shY + 50, cx - sw + 80, shY + 180, -14) + fold(cx + sw - 52, shY + 46, cx + sw - 84, shY + 180, 14);
    } else if (K.t === 'labcoat'){
      cloth = base('#e4e6e3') + shirt(!K.tie) + (K.tie ? tie(K.tie) : '');
      const lx = pit[0] - 44, rx = pit[0] + 50, y0 = pit[1] + 40;
      cloth += F(P('M', nbL[0] - 14, nbL[1] + 6, 'L', lx - 22, y0 + 40, 'L', lx, y0 + 60, 'L', pit[0] - 2, 720, 'L', pit[0] - 6, 760, 'L', cx - sw + 40, 760, 'L', cx - sw + 44, shY + 30, 'Z'), '#eceeeb', 2.4) + F(P('M', nbR[0] + 15, nbR[1] + 6, 'L', rx + 24, y0 + 36, 'L', rx + 2, y0 + 58, 'L', pit[0] + 4, 720, 'L', pit[0] + 10, 760, 'L', cx + sw - 40, 760, 'L', cx + sw - 46, shY + 28, 'Z'), '#f3f4f1', 2.4);
      cloth += L(P('M', lx - 22, y0 + 40, 'L', lx - 40, y0 + 22), 2) + L(P('M', rx + 24, y0 + 36, 'L', rx + 42, y0 + 18), 2) + T(P('M', cx - sw - 34, shY + 92, 'L', cx - sw - 44, 760, 'L', cx - sw + 40, 760, 'L', cx - sw + 44, shY + 30, 'Z'), '#59606e', .28) + F(P('M', cx + 60, shY + 110, 'l', 58, -4, 'l', 2, 56, 'l', -58, 4, 'Z'), '#eceeeb', 1.8) + L(P('M', cx + 76, shY + 96, 'l', 2, 40), 3, 'stroke="#27456b"');
    } else if (K.t === 'knit'){ // cardigan over a blouse
      cloth = base() + shirt(true) + F(P('M', nbL[0] - 14, nbL[1] + 6, 'C', pit[0] - 60, pit[1] + 60, pit[0] - 24, pit[1] + 170, pit[0] - 4, pit[1] + 230, 'L', pit[0] - 8, 760, 'L', cx - sw + 40, 760, 'L', cx - sw + 44, shY + 30, 'Z'), col, 2.4) + F(P('M', nbR[0] + 15, nbR[1] + 6, 'C', pit[0] + 66, pit[1] + 60, pit[0] + 30, pit[1] + 170, pit[0] + 8, pit[1] + 230, 'L', pit[0] + 12, 760, 'L', cx + sw - 40, 760, 'L', cx + sw - 46, shY + 28, 'Z'), col, 2.4);
      for (let i = 0; i < 5; i++) cloth += L(P('M', pit[0] - 52 + i * 2, pit[1] + 80 + i * 34, 'q', 10, 4, 22, 0), 1.2, 'opacity=".35"');
      cloth += `<circle cx="${pit[0] + 2}" cy="${pit[1] + 252}" r="7" fill="${colS}" stroke="${INK}" stroke-width="1.8"/>` + fold(cx - sw + 50, shY + 50, cx - sw + 80, shY + 170, -12) + fold(cx + sw - 52, shY + 46, cx + sw - 84, shY + 170, 12);
    } else if (K.t === 'gakuran'){ // boy's stand-collar uniform
      cloth = base() + F(P('M', nbL[0] - 5, nbL[1] - 12, 'C', nbL[0] + 6, pit[1] - 8, pit[0] - 10, pit[1] + 4, pit[0], pit[1] + 6, 'C', pit[0] + 12, pit[1] + 4, nbR[0] - 6, pit[1] - 10, nbR[0] + 6, nbR[1] - 12, 'L', nbR[0] + 8, nbR[1] + 12, 'C', nbR[0] - 8, pit[1] + 16, pit[0] + 12, pit[1] + 28, pit[0], pit[1] + 30, 'C', pit[0] - 12, pit[1] + 28, nbL[0] + 8, pit[1] + 16, nbL[0] - 7, nbL[1] + 12, 'Z'), colH, 2.4)
        + L(P('M', pit[0], pit[1] + 6, 'L', pit[0] + 2, 760), 2.2) + [0, 1, 2, 3].map(i => `<circle cx="${pit[0] + 1}" cy="${pit[1] + 62 + i * 76}" r="7" fill="#c9a94e" stroke="${INK}" stroke-width="1.8"/>`).join('') + `<path d="M${r(nbL[0] - 2)} ${r(nbL[1] - 8)} C${r(nbL[0] + 8)} ${r(pit[1] - 4)} ${r(pit[0] - 8)} ${r(pit[1] + 8)} ${r(pit[0])} ${r(pit[1] + 9)}" fill="none" stroke="#e9ebe8" stroke-width="3"/>`;
    } else { cloth = base() + shirt(true) + lapels(.9, 0); }
    if (K.hood) back += F(P('M', cx - sw + 40, shY + 10, 'C', cx - 150, 330, cx - 120, 250, cx - 70, 300, 'L', cx + 80, 300, 'C', cx + 130, 250, cx + 160, 330, cx + sw - 40, shY + 6, 'Z'), colS, 2.6);
    /* --- hair --- */
    const H = c.hs || (male ? 'short' : 'bob'), rec = (c.recede ?? (male ? Math.max(0, (age - 38) * .5) : 0)), hl = eyeY - 60 - rec, ht = top - 21, hx = fw + 9;
    const jag = pts => pts.map((p, i) => (i ? 'L ' : '') + r(p[0]) + ' ' + r(p[1])).join(' ');
    let hairB = '', hairF = '', hi = '';
    const capTo = (l, rr) => P('M', cx - hx - (l || 0), eyeY - 8, 'C', cx - hx - 12, top + 30, cx - 66, ht, cx + 4, ht, 'C', cx + 74, ht, cx + hx + 15, top + 32, cx + hx + 6 + (rr || 0), eyeY - 4);
    if (H === 'short' || H === 'messy' || H === 'bowl'){
      const fr = H === 'bowl' ? [[cx + fw - 2, eyeY - 6], [cx + fw - 14, eyeY - 30], [cx + 44, eyeY - 28], [cx + 38, eyeY - 20], [cx + 10, eyeY - 30], [cx + 2, eyeY - 21], [cx - 26, eyeY - 30], [cx - 34, eyeY - 21], [cx - fw + 14, eyeY - 28], [cx - fw + 4, eyeY - 8]]
        : H === 'messy' ? [[cx + fw + 3, eyeY + 8], [cx + fw - 7, eyeY - 18], [cx + fw - 20, hl + 20], [cx + 46, hl + 2], [cx + 40, eyeY - 30], [cx + 26, hl + 6], [cx + 14, eyeY - 22], [cx + 4, hl + 2], [cx - 8, eyeY - 16], [cx - 20, hl + 8], [cx - 34, eyeY - 24], [cx - 46, hl + 10], [cx - fw + 16, eyeY - 30], [cx - fw + 5, eyeY - 6]]
        : [[cx + fw + 3, eyeY + 6], [cx + fw - 6, eyeY - 20], [cx + fw - 16, hl + 14], [cx + 46, hl - 2], [cx + 30, hl + 12], [cx + 6, hl + 2], [cx - 18, hl + 12], [cx - 40, hl + 6], [cx - fw + 18, hl + 22], [cx - fw + 6, eyeY - 12]];
      if (H !== 'bowl') hairF = F(P('M', cx - 52, ht + 26, 'l', -17, -15, 'l', 26, 3, 'Z'), hc, 2.4) + F(P('M', cx + 14, ht + 6, 'l', 12, -15, 'l', 12, 18, 'Z'), hc, 2.4) + F(P('M', cx + 60, ht + 26, 'l', 22, -8, 'l', -8, 20, 'Z'), hc, 2.4) + (H === 'messy' ? F(P('M', cx - 20, ht + 8, 'l', -6, -15, 'l', 20, 10, 'Z'), hc, 2.4) + F(P('M', cx + hx + 2, eyeY - 30, 'l', 13, 8, 'l', -11, 12, 'Z'), hc, 2.4) : '');
      hairF += F(capTo(H === 'messy' ? 2 : 0, H === 'messy' ? 3 : 0) + ' L ' + jag(fr) + ' Z', hc, 2.6);
      if (H === 'messy') hairF += L(P('M', cx + 14, eyeY - 22, 'q', -3, 10, 2, 17), 2) + L(P('M', cx - 34, eyeY - 24, 'q', -4, 9, -1, 16), 2);
    } else if (H === 'back' || H === 'thin'){ // swept back, the hairline shows
      const m = H === 'thin' ? 16 : 0;
      hairF = F(capTo() + ' L ' + jag([[cx + fw + 3, eyeY + 4], [cx + fw - 5, eyeY - 22], [cx + fw - 12, hl + 16 - m], [cx + 50, hl - 14 - m], [cx + 26, hl - 4 - m], [cx + 4, hl + 2 - m], [cx - 24, hl - 6 - m], [cx - 46, hl - 12 - m], [cx - fw + 14, hl + 18 - m], [cx - fw + 6, eyeY - 14]]) + ' Z', hc, 2.6);
      for (let i = 0; i < 5; i++) hairF += L(P('M', cx - 40 + i * 22, hl - 4 - m - (i % 2) * 4, 'Q', cx - 30 + i * 22, ht + 22, cx - 10 + i * 20, ht + 8), 1.2, `stroke="${grey > .4 ? '#555b63' : '#3d4149'}" opacity=".7"`);
    } else if (H === 'buzz'){
      hairF = F(capTo(-4, -4).replace(String(r(ht)), String(r(ht + 8))).replace(String(r(ht)), String(r(ht + 8))) + ' L ' + jag([[cx + fw - 1, eyeY - 14], [cx + fw - 10, hl + 10], [cx + 40, hl - 6], [cx, hl], [cx - 40, hl - 4], [cx - fw + 12, hl + 14], [cx - fw + 5, eyeY - 14]]) + ' Z', mixc(hc, skin, .35), 2.4);
    } else if (H === 'bob' || H === 'long' || H === 'tied' || H === 'bun' || H === 'shortf'){
      const fringe = H === 'bun' || H === 'tied' ? [[cx + fw + 4, eyeY + 4], [cx + fw - 4, eyeY - 22], [cx + fw - 18, hl + 10], [cx + 34, hl - 10], [cx + 6, hl - 4], [cx - 14, hl + 8], [cx - 36, hl + 24], [cx - fw + 14, eyeY - 26], [cx - fw + 4, eyeY - 4]]
        : [[cx + fw + 6, eyeY + 26], [cx + fw - 2, eyeY - 4], [cx + fw - 12, eyeY - 30], [cx + 44, eyeY - 34], [cx + 36, eyeY - 22], [cx + 16, eyeY - 34], [cx + 6, eyeY - 21], [cx - 16, eyeY - 33], [cx - 26, eyeY - 22], [cx - 44, eyeY - 32], [cx - fw + 12, eyeY - 18], [cx - fw + 2, eyeY + 20]];
      hairF = F(capTo(3, 4) + ' L ' + jag(fringe) + ' Z', hc, 2.6);
      if (H === 'bob') hairB = F(P('M', cx - hx - 4, eyeY - 20, 'C', cx - hx - 16, eyeY + 40, cx - hx - 12, chin - 10, cx - hx + 4, chin + 12, 'L', cx - 30, chin + 16, 'L', cx + 50, chin + 14, 'L', cx + hx + 4, chin + 10, 'C', cx + hx + 20, chin - 20, cx + hx + 22, eyeY + 30, cx + hx + 8, eyeY - 20, 'Z'), hc, 2.6);
      if (H === 'shortf') hairB = F(P('M', cx - hx - 4, eyeY - 20, 'C', cx - hx - 14, eyeY + 30, cx - hx - 8, eyeY + 70, cx - hx + 8, eyeY + 86, 'L', cx + hx, eyeY + 84, 'C', cx + hx + 18, eyeY + 60, cx + hx + 20, eyeY + 20, cx + hx + 8, eyeY - 20, 'Z'), hc, 2.6);
      if (H === 'long') hairB = F(P('M', cx - hx - 4, eyeY - 20, 'C', cx - hx - 22, eyeY + 60, cx - hx - 30, 470, cx - hx - 22, 560, 'L', cx - 40, 540, 'L', cx + 60, 540, 'L', cx + hx + 30, 556, 'C', cx + hx + 36, 470, cx + hx + 26, eyeY + 60, cx + hx + 8, eyeY - 20, 'Z'), hc, 2.6);
      if (H === 'tied') hairB = F(P('M', cx + hx - 6, eyeY + 10, 'C', cx + hx + 34, eyeY + 40, cx + hx + 40, 400, cx + hx + 22, 520, 'C', cx + hx + 6, 480, cx + hx - 2, 400, cx + hx - 14, eyeY + 60, 'Z'), hc, 2.6) + F(P('M', cx - hx - 2, eyeY - 10, 'C', cx - hx - 8, eyeY + 30, cx - hx + 2, eyeY + 60, cx - hx + 14, eyeY + 70, 'L', cx + hx - 2, eyeY + 66, 'C', cx + hx + 10, eyeY + 40, cx + hx + 12, eyeY + 10, cx + hx + 6, eyeY - 10, 'Z'), hc, 2.4);
      if (H === 'bun') hairB = F(P('M', cx - 34, ht + 14, 'C', cx - 50, ht - 40, cx + 60, ht - 44, cx + 50, ht + 12, 'Z'), hc, 2.6) + F(P('M', cx - hx - 2, eyeY - 10, 'C', cx - hx - 8, eyeY + 30, cx - hx + 2, eyeY + 56, cx - hx + 14, eyeY + 64, 'L', cx + hx - 2, eyeY + 60, 'C', cx + hx + 10, eyeY + 36, cx + hx + 12, eyeY + 10, cx + hx + 6, eyeY - 10, 'Z'), hc, 2.4);
    }
    if (H !== 'buzz') for (let i = 0; i < 7; i++) hairF += L(P('M', cx - 44 + i * 16, ht + 14 + Math.abs(i - 3) * 5, 'Q', cx - 58 + i * 20, ht + 44, cx - 62 + i * 22, hl + (H === 'back' || H === 'thin' ? -6 : 10)), 1.3, `stroke="${grey > .4 ? '#8d8580' : mixc(hairC, '#ffe9d6', .22)}" opacity=".85"`);
    const sheen = grey > .5 ? '#ffffff' : hairHi;
    if (!o.plain && H !== 'buzz') hi += `<path d="${P('M', cx - 50, ht + 40, 'Q', cx + 4, ht + 20, cx + 60, ht + 42, 'Q', cx + 4, ht + 30, cx - 50, ht + 40, 'Z')}" fill="${sheen}" opacity="${grey > .5 ? .5 : .3}"/>`;
    hi = `<path d="${P('M', cx - 46, ht + 34, 'Q', cx + 4, ht + 12, cx + 58, ht + 36)}" fill="none" stroke="${sheen}" stroke-width="${o.wet ? 7 : 5}" stroke-linecap="round" stroke-dasharray="${o.wet ? '22 7 34 9 12 14' : '12 9 26 12 8 16'}" opacity="${grey > .5 ? .7 : .5}"/>` + (o.wet ? `<path d="${P('M', cx + 30, ht + 50, 'Q', cx + 54, ht + 44, cx + 70, ht + 66)}" fill="none" stroke="${sheen}" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 8" opacity=".5"/>` : '');
    if (grey > .15 && grey <= .6 && H !== 'buzz') for (let i = 0; i < 7; i++) hi += L(P('M', cx - 54 + i * 18, ht + 30 + (i % 3) * 8, 'q', 6, 14, 2, 30), 1.3, 'stroke="#c9cdd0" opacity=".75"');
    /* --- ear --- */
    const ex = cx + fw - 3, e1 = eyeY - 8, e2 = eyeY + 46;
    const ear = F(P('M', ex, e1 + 6, 'C', ex + 21, e1 - 9, ex + 27, e1 + 22, ex + 17, e2 - 8, 'C', ex + 13, e2 + 2, ex + 4, e2, ex + 1, e2 - 12, 'Z'), skin, 2.4) + L(P('M', ex + 6, e1 + 13, 'C', ex + 17, e1 + 6, ex + 18, e1 + 25, ex + 10, e2 - 14), 1.5) + T(P('M', ex + 3, e1 + 16, 'C', ex + 12, e1 + 14, ex + 12, e2 - 16, ex + 3, e2 - 16, 'Z'), sh1, .7);
    const earL = F(P('M', cx - fw + 6, eyeY, 'C', cx - fw - 6, eyeY - 4, cx - fw - 6, eyeY + 30, cx - fw + 5, eyeY + 34, 'Z'), sh1, 2);
    /* --- face shading --- */
    let shade = T(P('M', ...TL, 'C', TL[0] - 3, eyeY - 4, CL[0] - 1, CL[1] - 12, ...CL, 'C', CL[0] + 1, CL[1] + 22, JL[0] - 5, JL[1] - 16, ...JL, 'C', JL[0] + 6, JL[1] + 15, CHL[0] - 14, CHL[1] - 7, ...CHL, 'L', CHL[0] + 12, CHL[1] - 12, 'C', JL[0] + 22, JL[1] - 4, CL[0] + 30, CL[1] + 34, CL[0] + 22, CL[1] + 2, 'C', CL[0] + 15, eyeY - 4, TL[0] + 20, eyeY - 20, TL[0] + 22, TL[1] - 6, 'Z'), sh1, .34);
    shade += T(P('M', cx - fw + 10, hl + 14, 'C', cx - 30, hl + 26, cx + 30, hl + 22, cx + fw - 8, hl + 16, 'L', cx + fw - 8, hl + 2, 'L', cx - fw + 10, hl, 'Z'), sh1, H === 'back' || H === 'thin' || H === 'buzz' ? .0 : .34); // fringe shadow on the brow
    /* --- features --- */
    const nx = cx + tx, es = c.es || 1, bro = c.brow || 1, eyeC = c.eye || '#6b4530', ty = c.tilt || 0;
    const eye = (x, w, near) => { const op = E[0], y = eyeY + 2, hh = (kid ? 28 : male ? 21.5 : 25) * es * (old ? .84 : 1) * Math.min(op, 1.14), in_ = near ? x - w / 2 : x + w / 2, out = near ? x + w / 2 : x - w / 2, sgn = near ? 1 : -1, id = o.id + 'e' + (near ? 1 : 0);
      if (!op) return L(P('M', in_, y + 1, 'Q', x, y + 9, out, y - 2), 3.2) + L(P('M', out, y - 2, 'l', sgn * 6, -4), 2);
      const up = y - hh * .6, lo = y + hh * .4, shape = P('M', in_, y + 3, 'C', in_ + sgn * w * .2, up - 2, out - sgn * w * .28, up - 3 - ty * sgn, out, y - 3 - ty * sgn, 'C', out - sgn * w * .12, lo + 1, in_ + sgn * w * .3, lo + 3, in_, y + 3, 'Z');
      const big = emo === 'u', irx = hh * (big ? .4 : .47), iry = hh * (big ? .47 : .57), ix = x + (c.gaze || -1), iy = y - hh * .08;
      let s = `<clipPath id="${id}"><path d="${shape}"/></clipPath>` + T(shape, '#fffdfa');
      s += `<g clip-path="url(#${id})"><ellipse cx="${r(ix)}" cy="${r(iy)}" rx="${r(irx)}" ry="${r(iry)}" fill="url(#${o.id}ir)" stroke="${INK}" stroke-width="1.6"/><ellipse cx="${r(ix)}" cy="${r(iy - iry * .06)}" rx="${r(irx * .42)}" ry="${r(iry * .5)}" fill="#1c1216"/>`
        + `<ellipse cx="${r(ix)}" cy="${r(iy + iry * .62)}" rx="${r(irx * .62)}" ry="${r(iry * .26)}" fill="#fff" opacity=".28"/><rect x="${r(x - w)}" y="${r(up - 6)}" width="${r(w * 2)}" height="${r(hh * .3)}" fill="${INK}" opacity=".22"/>`
        + `<circle cx="${r(ix + irx * .36)}" cy="${r(iy - iry * .42)}" r="${r(irx * .36)}" fill="#fff"/><circle cx="${r(ix - irx * .42)}" cy="${r(iy + iry * .4)}" r="${r(irx * .17)}" fill="#fff" opacity=".95"/></g>`;
      s += T(P('M', in_ - sgn, y + 3.5, 'C', in_ + sgn * w * .2, up - 5, out - sgn * w * .28, up - 7 - ty * sgn, out + sgn * 4, y - 5 - ty * sgn, 'L', out + sgn * (male ? 7 : 11), y - (male ? 9 : 13) - ty * sgn, 'L', out + sgn * 1.5, y - .5 - ty * sgn, 'C', out - sgn * w * .28, up + 1.8 - ty * sgn, in_ + sgn * w * .2, up + 2.8, in_ - sgn, y + 3.5, 'Z'), INK);
      s += L(P('M', out - sgn * w * .08, lo - 1.5, 'Q', x + sgn * w * .12, lo + 3.5, x - sgn * w * .2, lo + 3), 1.5, 'opacity=".6"') + L(P('M', in_ + sgn * w * .2, up - 8, 'Q', x, up - 13, out - sgn * w * .22, up - 10), 1.2, 'opacity=".4"');
      if (age >= 55) s += L(P('M', in_ + sgn * 4, lo + 9, 'Q', x, lo + 14, out - sgn * 6, lo + 8), 1.1, `opacity="${old ? .4 : .28}"`);
      if (old) s += L(P('M', out + sgn * 6, y - 2, 'l', sgn * 8, -3), 1, 'opacity=".4"') + L(P('M', out + sgn * 6, y + 3, 'l', sgn * 8, 2), 1, 'opacity=".4"');
      return s; };
    const brow = (x, w, near) => { const sgn = near ? 1 : -1, by = eyeY - (kid ? 38 : male ? 30 : 33) * (.86 + es * .14) - (E[0] > 1.1 ? 3 : 0), in_ = [x - sgn * w * .52, by + E[1]], out = [x + sgn * w * .6, by + 3 + E[2] - ty * sgn * 2], th = (male ? 5 : 2.8) * bro * (kid ? .7 : 1);
      return T(P('M', in_[0], in_[1] - th * .5, 'Q', x, by - th - 1 + (E[1] + E[2]) * .2, out[0], out[1], 'Q', x, by + th * .5 + (E[1] + E[2]) * .2, in_[0], in_[1] + th * .6, 'Z'), grey > .6 ? '#6b7078' : INK); };
    const eL = [nx - 38, 43 * es + (kid ? 2 : 0)], eR = [nx + 43, 51 * es + (kid ? 2 : 0)];
    let feat = eye(eL[0], eL[1], 0) + eye(eR[0], eR[1], 1) + brow(eL[0], eL[1], 0) + brow(eR[0], eR[1], 1);
    if (emo === 'a' || emo === 'k') feat += L(P('M', nx - 3, eyeY - 20, 'l', 1, 9), 1.2, 'opacity=".6"') + L(P('M', nx + 5, eyeY - 21, 'l', -1, 9), 1.2, 'opacity=".6"');
    const nl = (kid ? 30 : male ? 42 : 38) * (c.nose || 1), ny = eyeY + nl; // nose: a small tip and a touch of shade
    feat += T(P('M', nx - 3, ny - 13, 'L', nx - 12, ny - 1, 'L', nx - 3, ny + 2, 'Z'), sh1, .5) + L(P('M', nx - 9, ny - 10, 'Q', nx - 14, ny - 3, nx - 8, ny), 2.1);
    if (!kid && male) feat += L(P('M', nx - 4, eyeY + 12, 'Q', nx - 6, eyeY + nl * .55, nx - 9, ny - 11), 1.1, 'opacity=".3"');
    const my = (kid ? ny + 19 : ny + 23), mw = (kid ? 12 : male ? 17 : 13) * (c.mw || 1), mx = nx - 4, lip = c.lip || (male ? 0 : .55);
    const mouths = { flat: P('M', mx - mw, my, 'Q', mx, my + 3, mx + mw, my - 1), firm: P('M', mx - mw, my + 1.5, 'Q', mx, my - .5, mx + mw, my + .5), down: P('M', mx - mw, my + 4, 'Q', mx, my - 2.5, mx + mw, my + 3), smile: P('M', mx - mw - 2, my - 3, 'Q', mx, my + 8, mx + mw + 3, my - 5), wavy: P('M', mx - mw, my + 2, 'q', mw * .5, -4, mw, 0, 't', mw, 0) };
    let mouth = '';
    if (E[3] === 'open') mouth = F(P('M', mx - mw * .55, my - 1, 'Q', mx, my - 5, mx + mw * .55, my - 1, 'Q', mx, my + 12, mx - mw * .55, my - 1, 'Z'), '#3a2226', 2);
    else if (E[3] === 'grit') mouth = F(P('M', mx - mw, my + 1, 'Q', mx, my - 4, mx + mw, my, 'Q', mx, my + 8, mx - mw, my + 1, 'Z'), '#f2efea', 2) + L(P('M', mx - mw + 3, my + 2, 'L', mx + mw - 3, my + 1.5), 1.2);
    else mouth = L(mouths[E[3]], 2.4);
    const mOpen = F(P('M', mx - mw * .7, my - 1, 'Q', mx, my - 3, mx + mw * .7, my - 1, 'Q', mx, my + 13, mx - mw * .7, my - 1, 'Z'), '#3a2226', 2) + T(P('M', mx - mw * .5, my, 'Q', mx, my - 1, mx + mw * .5, my, 'L', mx + mw * .4, my + 3, 'L', mx - mw * .4, my + 3, 'Z'), '#f2efea');
    feat += `<g class="m0">${mouth}</g><g class="m1">${mOpen}</g>` + L(P('M', mx - mw * .45, my + (kid ? 9 : 12), 'Q', mx, my + (kid ? 12 : 15), mx + mw * .5, my + (kid ? 8 : 11)), 1.3, 'opacity=".45"');
    if (lip) feat += T(P('M', mx - mw + 2, my + 1, 'Q', mx, my + 9, mx + mw - 2, my, 'Q', mx, my + 3, mx - mw + 2, my + 1, 'Z'), '#e0766e', lip * .6);
    feat += `<ellipse cx="${r(eL[0] - 4)}" cy="${r(eyeY + 32)}" rx="19" ry="9" fill="#f58f7c" opacity="${kid ? .34 : male ? (old ? .12 : .17) : (old ? .18 : .3)}"/><ellipse cx="${r(eR[0] + 6)}" cy="${r(eyeY + 32)}" rx="23" ry="10" fill="#f58f7c" opacity="${kid ? .34 : male ? (old ? .12 : .17) : (old ? .18 : .3)}"/>`;
    if (age >= 52) feat += L(P('M', nx - 22, ny - 4, 'Q', nx - 30, ny + 10, nx - 27, my - 2), 1.2, `opacity="${old ? .42 : .26}"`) + L(P('M', nx + 16, ny - 6, 'Q', nx + 27, ny + 8, nx + 25, my - 4), 1.2, `opacity="${old ? .42 : .26}"`);
    if (age >= 56) feat += L(P('M', nx - 40, hl + 30, 'Q', nx, hl + 24, nx + 46, hl + 30), 1, `opacity="${old ? .34 : .2}"`);
    if (old) feat += L(P('M', JL[0] + 8, JL[1] - 6, 'q', 3, 12, 12, 18), 1.2, 'opacity=".28"') + L(P('M', JR[0] - 12, JR[1] - 4, 'q', -2, 12, -12, 18), 1.2, 'opacity=".28"');
    if (c.beard === 'stubble') feat += T(P('M', JL[0] + 2, JL[1] - 8, 'C', JL[0] + 10, JL[1] + 18, CHL[0] - 9, CHL[1] - 3, ...CHL, 'Q', ...CH, ...CHR, 'C', CHR[0] + 15, CHR[1] - 4, JR[0] - 5, JR[1] + 17, JR[0] - 3, JR[1] - 10, 'C', JR[0] - 18, my + 22, mx + mw + 8, my - 10, mx, my - 12, 'C', mx - mw - 8, my - 10, JL[0] + 16, my + 20, JL[0] + 2, JL[1] - 8, 'Z'), '#6b4a45', .13);
    if (c.beard === 'mustache') feat += T(P('M', mx - mw - 4, my - 3, 'Q', mx, my - 15, mx + mw + 5, my - 4, 'Q', mx, my - 6, mx - mw - 4, my - 3, 'Z'), grey > .5 ? '#878d94' : INK);
    if (c.mole) feat += `<circle cx="${r(eR[0] + 8)}" cy="${r(eyeY + 19)}" r="2.3" fill="${INK}"/>`;
    if (c.scar) feat += `<path d="${P('M', eR[0] + 10, eyeY - 36, 'L', eR[0] + 3, eyeY - 12)}" stroke="#b9837c" stroke-width="3" fill="none" stroke-linecap="round"/><path d="${P('M', eR[0] + 10, eyeY - 36, 'L', eR[0] + 3, eyeY - 12)}" stroke="#f3e9df" stroke-width="1.1" fill="none" stroke-linecap="round"/>`;
    if (c.band) feat += F(P('M', eR[0] - 8, eyeY - 44, 'l', 30, -3, 'l', 2, 18, 'l', -30, 3, 'Z'), '#f1efe9', 1.8);
    let glasses = '';
    if (c.glasses){ const gy = eyeY + 1, gw = c.glasses === 'round' ? 25 : 28, gh = c.glasses === 'round' ? 22 : 17, rr = c.glasses === 'round' ? 20 : 6;
      glasses = `<rect x="${r(eL[0] - gw + 2)}" y="${r(gy - gh)}" width="${gw * 2 - 6}" height="${gh * 2}" rx="${rr}" fill="#dfe8ea" fill-opacity=".14" stroke="${INK}" stroke-width="2.6"/><rect x="${r(eR[0] - gw)}" y="${r(gy - gh)}" width="${gw * 2}" height="${gh * 2}" rx="${rr}" fill="#dfe8ea" fill-opacity=".14" stroke="${INK}" stroke-width="2.6"/>` + L(P('M', eL[0] + gw - 4, gy - 4, 'Q', nx + 1, gy - 9, eR[0] - gw, gy - 4), 2.4) + L(P('M', eR[0] + gw, gy - 6, 'L', ex + 8, gy - 4), 2.2) + `<path d="${P('M', eR[0] - 14, gy - gh + 5, 'l', 12, 0)}" stroke="#fff" stroke-width="2" opacity=".6"/>`; }
    let cap = '';
    if (c.cap) cap = F(P('M', cx - hx - 8, hl + 6, 'C', cx - hx - 16, top - 20, cx - 40, top - 52, cx + 6, top - 54, 'C', cx + 60, top - 54, cx + hx + 22, top - 24, cx + hx + 12, hl + 2, 'Z'), c.cap, 2.8) + F(P('M', cx - hx - 4, hl + 2, 'C', cx - 40, hl - 12, cx + 50, hl - 14, cx + hx + 10, hl - 2, 'L', cx + hx + 12, hl + 14, 'C', cx + 50, hl + 2, cx - 40, hl + 4, cx - hx - 8, hl + 18, 'Z'), '#15171b', 2.4) + F(P('M', cx - hx - 14, hl + 16, 'C', cx - 60, hl + 2, cx + 30, hl - 2, cx + 60, hl + 6, 'C', cx + 20, hl + 26, cx - 50, hl + 34, cx - hx - 30, hl + 36, 'Z'), '#0c0d10', 2.4) + `<circle cx="${cx - 4}" cy="${top - 14}" r="11" fill="#c9a94e" stroke="${INK}" stroke-width="2"/>`;
    /* --- rain --- */
    let wet = '';
    if (o.wet){ const dr = [[cx - 150, shY + 30], [cx + 132, shY + 22], [cx - 96, shY + 2], [cx + 84, shY - 8], [cx + 40, top + 6], [cx - 30, top + 2], [cx + 160, shY + 70], [cx - 170, shY + 84]];
      wet = dr.map(([x, y]) => `<path d="M${r(x)} ${r(y)} l-3 9 a3.4 3.4 0 1 0 6 0 Z" fill="#fff" opacity=".7"/>`).join('') + L(P('M', CR[0] - 16, eyeY + 30, 'q', 2, 16, -2, 30), 1.6, 'stroke="#fff" opacity=".7"') + `<path d="${P('M', cx - sw + 30, shY + 4, 'C', cx - sw + 70, shY - 22, cx - 110, shY - 30, cx - 80, shY - 38)}" stroke="#fff" stroke-width="3" fill="none" opacity=".35" stroke-linecap="round" stroke-dasharray="26 12 10 16"/><path d="${P('M', cx + sw - 30, shY + 2, 'C', cx + sw - 70, shY - 24, cx + 112, shY - 32, cx + 84, shY - 40)}" stroke="#fff" stroke-width="3.4" fill="none" opacity=".5" stroke-linecap="round" stroke-dasharray="30 10 12 14"/>`; }
    const rim = `<path d="${P('M', ...CR, 'C', CR[0], CR[1] - 20, TR[0] + 2, TR[1] + 12, ...TR)}" fill="none" stroke="#fff6ea" stroke-width="2.2" opacity=".55"/>`;
    const tiltDeg = (o.tilt || 0) + (emo === 'd' ? 2.5 : emo === 't' ? -2 : 0);
    const rot = `transform="rotate(${tiltDeg} ${ncx} ${chin + 10})"`, head = `<g ${rot}>${earL}${ear}${F(face, skin, 2.9)}${shade}${rim}${feat}${hairF}${hi}${glasses}${cap}</g>`;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${o.vb || '66 52 468 593'}" class="port${o.cls ? ' ' + o.cls : ''}" ${o.attr || ''}><defs><linearGradient id="${o.id}ir" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${mixc(eyeC, '#150d10', .55)}"/><stop offset=".55" stop-color="${eyeC}"/><stop offset="1" stop-color="${mixc(eyeC, '#ffe2b8', .45)}"/></linearGradient></defs><g ${o.flip ? 'transform="translate(600 0) scale(-1 1)"' : ''}>${back}<g ${rot}>${hairB}</g>${neck}${cloth}${head}${wet}</g></svg>`;
  }
  let uid = 0;
  return { svg: (c, emo, o = {}) => build(c, emo, Object.assign({ id: 'p' + (uid++) }, o)) };
})();
if (typeof module !== 'undefined') module.exports = { PORT };
