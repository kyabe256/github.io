/* ---------- 16:9 backgrounds (1600x900), drawn in one-point perspective ---------- */
const W3 = 1600, H3 = 900;
const ol = (w = 2.4, op = .7, c = '#241a2c') => `stroke="${c}" stroke-width="${w}" stroke-opacity="${op}" stroke-linejoin="round" stroke-linecap="round"`;
let _g3 = 0; const gid = () => 'q' + (++_g3);
function lgr(stops, x2 = 0, y2 = 1){ const id = gid(); return [id, `<linearGradient id="${id}" x1="0" y1="0" x2="${x2}" y2="${y2}">${stops.map(s => `<stop offset="${s[0]}" stop-color="${s[1]}" stop-opacity="${s[2] ?? 1}"/>`).join('')}</linearGradient>`]; }
function rgr(stops, cx = .5, cy = .5, r = .5){ const id = gid(); return [id, `<radialGradient id="${id}" cx="${cx}" cy="${cy}" r="${r}">${stops.map(s => `<stop offset="${s[0]}" stop-color="${s[1]}" stop-opacity="${s[2] ?? 1}"/>`).join('')}</radialGradient>`]; }
const ANCH = {};
let RM = null;
function room(p){
  const r = RM = Object.assign({ x0: 250, x1: 1350, y0: 130, y1: 630, boards: 12, rows: 5 }, p);
  const [a, A] = lgr([[0, shade(r.wall, 1.1)], [1, shade(r.wall, .84)]]), [b, B] = lgr([[0, shade(r.floor, .7)], [1, shade(r.floor, 1.06)]]);
  const [c, C] = lgr([[0, shade(r.side, .66)], [1, shade(r.side, 1)]], 1, 0), [d, D] = lgr([[0, shade(r.side, 1)], [1, shade(r.side, .66)]], 1, 0);
  let s = `<defs>${A}${B}${C}${D}</defs><polygon points="0,0 ${W3},0 ${r.x1},${r.y0} ${r.x0},${r.y0}" fill="${r.ceil}"/><polygon points="0,0 ${r.x0},${r.y0} ${r.x0},${r.y1} 0,${H3}" fill="url(#${c})"/><polygon points="${W3},0 ${r.x1},${r.y0} ${r.x1},${r.y1} ${W3},${H3}" fill="url(#${d})"/><rect x="${r.x0}" y="${r.y0}" width="${r.x1 - r.x0}" height="${r.y1 - r.y0}" fill="url(#${a})"/><polygon points="${r.x0},${r.y1} ${r.x1},${r.y1} ${W3},${H3} 0,${H3}" fill="url(#${b})"/>`;
  for (let i = 1; i < r.boards; i++){ const t = i / r.boards; s += `<path d="M${r.x0 + (r.x1 - r.x0) * t} ${r.y1} L${W3 * t} ${H3}" stroke="#000" stroke-opacity=".1" stroke-width="2"/>`; }
  for (let i = 1; i <= r.rows; i++){ const t = Math.pow(i / (r.rows + 1), 1.7), y = r.y1 + (H3 - r.y1) * t; s += `<path d="M${r.x0 * (1 - t)} ${y} H${r.x1 + (W3 - r.x1) * t}" stroke="#000" stroke-opacity="${r.tile ? .12 : .05}" stroke-width="2"/>`; }
  s += `<path d="M${r.x0} ${r.y1 - 14} H${r.x1} V${r.y1} H${r.x0}Z" fill="${shade(r.wall, .62)}"/><polygon points="0,${H3} ${r.x0},${r.y1} ${r.x0},${r.y1 - 14} 0,${H3 - 34}" fill="${shade(r.side, .5)}"/><polygon points="${W3},${H3} ${r.x1},${r.y1} ${r.x1},${r.y1 - 14} ${W3},${H3 - 34}" fill="${shade(r.side, .5)}"/>`;
  s += `<path d="M0 0 L${r.x0} ${r.y0} V${r.y1} L0 ${H3} M${W3} 0 L${r.x1} ${r.y0} V${r.y1} L${W3} ${H3} M${r.x0} ${r.y0} H${r.x1} M${r.x0} ${r.y1} H${r.x1}" fill="none" ${ol(2.6, .55)}/>`;
  return s;
}
// points on the side walls: t = depth (0 near the viewer, 1 at the back wall), v = height (0 top, 1 floor)
const LW = (t, v) => { const r = RM, x = r.x0 * t, yt = r.y0 * t, yb = H3 - (H3 - r.y1) * t; return [x, yt + (yb - yt) * v]; };
const RW = (t, v) => { const r = RM, x = W3 - (W3 - r.x1) * t, yt = r.y0 * t, yb = H3 - (H3 - r.y1) * t; return [x, yt + (yb - yt) * v]; };
const quad = (f, t0, t1, v0, v1) => [f(t0, v0), f(t1, v0), f(t1, v1), f(t0, v1)].map(p => p.map(n => n.toFixed(1)).join(',')).join(' ');
function box3(x, y, w, h, dx, dy, col, opt = {}){
  const top = shade(col, opt.top || 1.18), sd = shade(col, .72);
  let s = `<polygon points="${x},${y} ${x + w},${y} ${x + w + dx},${y - dy} ${x + dx},${y - dy}" fill="${top}" ${ol()}/>`;
  if (dx > 0) s += `<polygon points="${x + w},${y} ${x + w + dx},${y - dy} ${x + w + dx},${y + h - dy} ${x + w},${y + h}" fill="${sd}" ${ol()}/>`;
  if (dx < 0) s += `<polygon points="${x},${y} ${x + dx},${y - dy} ${x + dx},${y + h - dy} ${x},${y + h}" fill="${sd}" ${ol()}/>`;
  return s + `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${col}" ${ol()}/>` + (opt.shadow === 0 ? '' : `<ellipse cx="${x + w / 2}" cy="${y + h + 6}" rx="${w * .56}" ry="16" fill="#000" opacity=".16"/>`);
}
function skyline(x, y, w, h, col, seed, lit){
  let p = `M${x} ${y + h}`, s = '', bx = x; let i = seed;
  while (bx < x + w){ const bw = 26 + (i * 37) % 44, bh = h * (.22 + ((i * 53) % 60) / 100); p += ` V${y + h - bh} H${bx + bw}`; if (lit) for (let k = 0; k < 5; k++){ const wx = bx + 5 + (k * 13 + i * 7) % Math.max(6, bw - 10), wy = y + h - bh + 8 + (k * 29 + i * 11) % Math.max(8, bh - 14); s += `<rect x="${wx}" y="${wy}" width="4" height="5" fill="${lit}" opacity="${.5 + (k % 3) * .2}"/>`; } bx += bw; i++; }
  return `<path d="${p} V${y + h}Z" fill="${col}"/>` + s;
}
function win3(x, y, w, h, o = {}){
  const sky = o.sky || ['#8fc4ec', '#e6f2fb'], [g, G] = lgr([[0, sky[0]], [1, sky[1]]]), cid = gid(), n = o.n || 3;
  let s = `<defs>${G}<clipPath id="${cid}"><rect x="${x}" y="${y}" width="${w}" height="${h}"/></clipPath></defs><rect x="${x - 12}" y="${y - 12}" width="${w + 24}" height="${h + 24}" fill="${o.frame || '#3a3f4c'}" ${ol()}/><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="url(#${g})"/><g clip-path="url(#${cid})">`;
  if (o.sun) s += `<circle cx="${x + w * o.sun[0]}" cy="${y + h * o.sun[1]}" r="${h * .32}" fill="#fff4d0" opacity=".5"/><circle cx="${x + w * o.sun[0]}" cy="${y + h * o.sun[1]}" r="${h * .1}" fill="#fffbe8"/>`;
  s += `<g class="a-cloud"><ellipse cx="${x + w * .2}" cy="${y + h * .22}" rx="${w * .12}" ry="${h * .05}" fill="#fff" opacity=".8"/><ellipse cx="${x + w * .62}" cy="${y + h * .32}" rx="${w * .16}" ry="${h * .045}" fill="#fff" opacity=".65"/></g>`;
  s += skyline(x, y + h * .2, w, h * .8, o.far || '#9db4cc', 3, 0) + skyline(x, y + h * .42, w, h * .58, o.near || '#5f7896', 8, o.lit || 0);
  s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" opacity=".07"/><path d="M${x + w * .08} ${y} l${w * .1} 0 l-${w * .2} ${h} l-${w * .1} 0Z M${x + w * .3} ${y} l${w * .04} 0 l-${w * .2} ${h} l-${w * .04} 0Z" fill="#fff" opacity=".13"/></g>`;
  for (let i = 1; i < n; i++) s += `<rect x="${x + w * i / n - 5}" y="${y}" width="10" height="${h}" fill="${o.frame || '#3a3f4c'}"/>`;
  if (o.blind){ for (let i = 0; i < h / 16; i++) s += `<rect class="a-slat" style="animation-delay:${(i % 7) * .37}s" x="${x}" y="${y + i * 16}" width="${w}" height="${o.blind}" fill="${o.blindc || '#d8d4c8'}" opacity=".92"/>`; }
  return s + `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="none" ${ol(2, .5)}/><rect x="${x - 20}" y="${y + h + 12}" width="${w + 40}" height="12" fill="${shade(o.frame || '#3a3f4c', 1.3)}" ${ol()}/>`;
}
const spill = (pts, col = '#fff2c8', op = .16) => `<polygon class="a-spill" points="${pts}" fill="${col}" opacity="${op}"/>`;
function screen3(x, y, w, h, kind, o = {}){
  const cid = gid(), col = o.col || '#0d1b2a', ink = o.ink || '#7fd0ff'; let c = '';
  if (kind === 'log'){ let ln = ''; for (let i = 0; i < 2 * Math.ceil(h / 12); i++) ln += `<rect x="${x + 10 + (i % 3) * 8}" y="${y + 8 + i * 12}" width="${(w - 30) * (.3 + ((i * 37) % 60) / 100)}" height="4" rx="2" fill="${i % 7 === 3 ? (o.hot || '#ffb347') : ink}" opacity="${.5 + (i % 4) * .12}"/>`; c = `<g class="a-scroll" style="--sy:${-Math.ceil(h / 12) * 12}px;animation-duration:${o.dur || 9}s">${ln}</g>`; }
  if (kind === 'wave'){ let d = `M${x} ${y + h / 2}`; for (let i = 0; i <= 48; i++) d += ` L${x + (w * 2) * i / 48} ${y + h / 2 + Math.sin(i * 1.3) * h * .22 * (1 + Math.sin(i * .37)) / 2 + (i % 12 === 5 ? -h * .3 : 0)}`; c = `<path class="a-wave" style="--sx:${-w}px" d="${d}" fill="none" stroke="${ink}" stroke-width="3"/><path d="M${x} ${y + h * .25} H${x + w} M${x} ${y + h * .75} H${x + w}" stroke="${ink}" stroke-opacity=".2"/>`; }
  if (kind === 'map'){ c = `<path d="M${x + w * .1} ${y + h * .7} q${w * .2} -${h * .5} ${w * .4} -${h * .2} t${w * .4} -${h * .25}" fill="none" stroke="${ink}" stroke-opacity=".5" stroke-width="2"/>` + [[.2, .5], [.45, .42], [.62, .6], [.8, .3], [.33, .72]].map((q, i) => `<circle class="a-ping" style="animation-delay:${i * .5}s" cx="${x + w * q[0]}" cy="${y + h * q[1]}" r="5" fill="${i === 1 ? '#ff6b5a' : ink}"/>`).join('') + `<path d="M${x} ${y + h * .33} H${x + w} M${x} ${y + h * .66} H${x + w} M${x + w * .33} ${y} V${y + h} M${x + w * .66} ${y} V${y + h}" stroke="${ink}" stroke-opacity=".14"/>`; }
  if (kind === 'cctv'){ const hw = w / 2, hh = h / 2; for (let i = 0; i < 4; i++){ const cx = x + (i % 2) * hw, cy = y + (i > 1 ? hh : 0); c += `<rect x="${cx + 2}" y="${cy + 2}" width="${hw - 4}" height="${hh - 4}" fill="${['#1c2a2c', '#22262e', '#1e2630', '#262a24'][i]}"/><path d="M${cx + hw * .3} ${cy + hh * .35} L${cx + hw * .7} ${cy + hh * .35} L${cx + hw - 4} ${cy + hh - 3} L${cx + 4} ${cy + hh - 3}Z" fill="#fff" opacity=".07"/><rect x="${cx + hw * .42}" y="${cy + hh * .22}" width="${hw * .16}" height="${hh * .16}" fill="#fff" opacity=".1"/><text x="${cx + 8}" y="${cy + 18}" font-size="11" font-family="monospace" fill="#cfe">${['12F 廊下', '1F 玄関', 'EV前', '駐輪場'][i]}</text><circle class="a-blink" cx="${cx + hw - 12}" cy="${cy + 13}" r="4" fill="#ff4a3a"/>`; } c += `<rect class="a-scan" x="${x}" y="${y}" width="${w}" height="26" fill="#fff" opacity=".06" style="--sy:${h}px"/>`; }
  if (kind === 'doc'){ for (let i = 0; i < Math.floor(h / 16) - 1; i++) c += `<rect x="${x + 12}" y="${y + 12 + i * 16}" width="${(w - 24) * [.9, .7, .82, .5, .88, .64][i % 6]}" height="5" rx="2" fill="${ink}" opacity=".7"/>`; c += `<rect class="a-blink" x="${x + 12}" y="${y + h - 16}" width="8" height="6" fill="${ink}"/>`; }
  return `<g class="scr"><defs><clipPath id="${cid}"><rect x="${x}" y="${y}" width="${w}" height="${h}"/></clipPath></defs><rect x="${x - 8}" y="${y - 8}" width="${w + 16}" height="${h + 16}" rx="6" fill="#1a1c24" ${ol()}/><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${col}"/><g clip-path="url(#${cid})">${c}</g><rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${ink}" opacity=".06"/><path d="M${x} ${y} h${w * .5} l-${w * .3} ${h} h-${w * .2}Z" fill="#fff" opacity=".04"/>${o.stand === 0 ? '' : `<rect x="${x + w / 2 - 10}" y="${y + h + 8}" width="20" height="16" fill="#2a2c36" ${ol()}/><rect x="${x + w / 2 - 44}" y="${y + h + 22}" width="88" height="8" rx="3" fill="#2a2c36" ${ol()}/>`}</g>`;
}
function shelf3(x, y, w, h, col, rows, o = {}){
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${shade(col, .6)}" ${ol()}/>`; const pal = o.pal || ['#a8443a', '#3a6aa2', '#c9a43a', '#3f7f5a', '#7a4a86', '#d9d4c4', '#2d3c5c', '#b9683a'];
  for (let r = 0; r < rows; r++){ const ry = y + 8 + r * (h - 8) / rows, rh = (h - 8) / rows - 12; let bx = x + 8, i = r * 5 + (o.seed || 0);
    while (bx < x + w - 22){ const bw = o.binder ? 20 + (i % 3) * 5 : 10 + (i * 7) % 12, bh = rh * (o.binder ? .92 : .68 + ((i * 13) % 30) / 100); if ((i * 11) % 9 === 4 && !o.binder){ bx += 14; i++; continue; } s += `<rect x="${bx}" y="${ry + rh - bh}" width="${bw}" height="${bh}" fill="${pal[i % pal.length]}" ${ol(1.4, .6)}/>` + (o.binder ? `<rect x="${bx + 4}" y="${ry + rh - bh + 10}" width="${bw - 8}" height="${bh * .34}" fill="#f4f1e6"/><circle cx="${bx + bw / 2}" cy="${ry + rh - 12}" r="3.5" fill="none" stroke="#222" stroke-opacity=".5"/>` : `<rect x="${bx + 2}" y="${ry + rh - bh + 8}" width="${bw - 4}" height="3" fill="#fff" opacity=".35"/>`); bx += bw + 2; i++; }
    s += `<rect x="${x}" y="${ry + rh}" width="${w}" height="8" fill="${col}" ${ol(1.4, .6)}/>`; }
  return s;
}
const flag3 = (x, y, jp, h = 300) => `<path d="M${x} ${y} v${h}" stroke="#c9a94a" stroke-width="7"/><path d="M${x} ${y} v${h}" ${ol(1.2, .5)} fill="none"/><circle cx="${x}" cy="${y - 4}" r="9" fill="#e0c060" ${ol()}/><ellipse cx="${x}" cy="${y + h}" rx="34" ry="9" fill="#3a3a44" ${ol()}/>` + (jp
  ? `<g class="a-sway"><path d="M${x + 4} ${y + 12} q40 -10 78 4 q-10 60 -4 150 q-34 18 -74 6Z" fill="#fbfbf6" ${ol()}/><circle cx="${x + 42}" cy="${y + 84}" r="24" fill="#c8283a"/><path d="M${x + 24} ${y + 14} q-6 70 0 156 M${x + 60} ${y + 12} q-8 70 -2 160" stroke="#000" stroke-opacity=".08" stroke-width="5" fill="none"/></g>`
  : `<g class="a-sway"><path d="M${x + 4} ${y + 12} q40 -10 78 4 q-10 60 -4 150 q-34 18 -74 6Z" fill="#fbfbf6" ${ol()}/>${[0, 1, 2, 3, 4, 5].map(i => `<path d="M${x + 6 + i * 13} ${y + 60 + i * 0} q-5 50 0 ${112 - i * 2}" stroke="#b8283a" stroke-width="6" fill="none"/>`).join('')}<path d="M${x + 4} ${y + 12} q40 -10 78 4 q-3 24 -5 46 q-36 -8 -73 -2Z" fill="#27366e"/>${[0, 1, 2, 3, 4, 5, 6, 7].map(i => `<circle cx="${x + 16 + (i % 4) * 17}" cy="${y + 24 + Math.floor(i / 4) * 16}" r="2.4" fill="#fff"/>`).join('')}<path d="M${x + 4} ${y + 12} q40 -10 78 4 q-10 60 -4 150 q-34 18 -74 6Z" fill="none" ${ol()}/></g>`);
const clock3 = (x, y, r, hh, mm, label, face = '#f6f3ea') => `<circle cx="${x}" cy="${y}" r="${r}" fill="${face}" stroke="#241a2c" stroke-width="5"/>${[...Array(12)].map((_, i) => `<path d="M${x + Math.sin(i * Math.PI / 6) * r * .84} ${y - Math.cos(i * Math.PI / 6) * r * .84} L${x + Math.sin(i * Math.PI / 6) * r * .94} ${y - Math.cos(i * Math.PI / 6) * r * .94}" stroke="#241a2c" stroke-width="2"/>`).join('')}<path d="M${x} ${y} L${x + Math.sin((hh + mm / 60) * Math.PI / 6) * r * .5} ${y - Math.cos((hh + mm / 60) * Math.PI / 6) * r * .5}" stroke="#241a2c" stroke-width="5" stroke-linecap="round"/><path d="M${x} ${y} L${x + Math.sin(mm * Math.PI / 30) * r * .76} ${y - Math.cos(mm * Math.PI / 30) * r * .76}" stroke="#241a2c" stroke-width="3.4" stroke-linecap="round"/><path class="a-sec" d="M${x} ${y + r * .18} V${y - r * .82}" stroke="#d2382f" stroke-width="2" style="transform-origin:${x}px ${y}px"/><circle cx="${x}" cy="${y}" r="3.5" fill="#241a2c"/>` + (label ? `<text x="${x}" y="${y + r + 24}" font-size="15" text-anchor="middle" fill="#e8ecf4" font-weight="700" letter-spacing="2" font-family="monospace">${label}</text>` : '');
const cone = (x, y, w, h, col = '#fff3cf', op = .14) => { const [g, G] = lgr([[0, col, op * 1.6], [1, col, 0]]); return `<defs>${G}</defs><polygon points="${x - 18},${y} ${x + 18},${y} ${x + w / 2},${y + h} ${x - w / 2},${y + h}" fill="url(#${g})"/>`; };
const downlight = (x, y) => `<ellipse cx="${x}" cy="${y}" rx="30" ry="9" fill="#fff8de" ${ol(2, .5)}/><ellipse cx="${x}" cy="${y}" rx="60" ry="18" fill="#fff8de" opacity=".25"/>`;
const dust = (x, y, w, h, n = 14) => [...Array(n)].map((_, i) => `<circle class="a-dust" style="animation-delay:${-i * 1.3}s;animation-duration:${9 + (i % 5) * 2}s" cx="${x + (i * 97) % w}" cy="${y + (i * 61) % h}" r="${1.4 + (i % 3) * .7}" fill="#fff" opacity=".5"/>`).join('');
const vig3 = (col = '#0b0a18', op = .5) => { const [g, G] = rgr([[.55, col, 0], [1, col, op]], .5, .46, .75); return `<defs>${G}</defs><rect width="${W3}" height="${H3}" fill="url(#${g})" pointer-events="none"/>`; };
const grade = (col, op, mode = 'multiply') => `<rect width="${W3}" height="${H3}" fill="${col}" opacity="${op}" pointer-events="none"/>`;
const plant3 = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})"><g class="a-sway2"><path d="M0 0 q-50 -60 -30 -130 q24 50 30 130 q6 -90 44 -116 q10 62 -44 116 q-10 -56 -62 -70 q12 46 62 70 q30 -30 66 -30 q-20 36 -66 30" fill="#3d8a58" ${ol()}/><path d="M0 0 q-8 -60 -22 -110 M0 0 q14 -60 38 -100" stroke="#2a6a40" stroke-width="2" fill="none"/></g><path d="M-34 0 h68 l-8 70 h-52Z" fill="#b9714a" ${ol()}/><path d="M-34 0 h68 l-2 14 h-64Z" fill="#000" opacity=".12"/></g>`;
const paper3 = (x, y, r = 0, w = 70, h = 46) => `<g transform="translate(${x} ${y}) rotate(${r})"><rect width="${w}" height="${h}" fill="#f7f4ea" ${ol(1.6, .6)}/><path d="M8 10 h${w - 18} M8 19 h${w - 28} M8 28 h${w - 20} M8 37 h${w * .4}" stroke="#7a7a86" stroke-width="2.4" stroke-opacity=".7"/></g>`;
const frame3 = (x, y, w, h, col, inner) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${col}" ${ol()}/><rect x="${x + 8}" y="${y + 8}" width="${w - 16}" height="${h - 16}" fill="${inner}"/><path d="M${x + 8} ${y + 8} l${w * .5} 0 l-${w * .3} ${h - 16} l-${w * .2} 0Z" fill="#fff" opacity=".1"/>`;
const tent = (x, y, n) => `<g><path d="M${x} ${y} l14 -30 l14 30Z" fill="#f2c230" ${ol(1.8)}/><text x="${x + 14}" y="${y - 6}" font-size="15" font-weight="900" text-anchor="middle" fill="#241a2c">${n}</text></g>`;
const chair3 = (x, y, col = '#3a3d48') => `<rect x="${x}" y="${y}" width="120" height="130" rx="14" fill="${col}" ${ol()}/><rect x="${x + 10}" y="${y + 12}" width="100" height="80" rx="10" fill="${shade(col, 1.25)}"/><rect x="${x - 6}" y="${y + 120}" width="132" height="26" rx="8" fill="${shade(col, .8)}" ${ol()}/>`;

const SC3 = {
/* 総監室: wide window, two flags, a heavy desk with ringing phones */
soukan(){
  let s = room({ x0: 190, x1: 1410, y0: 110, y1: 610, wall: '#5a5470', side: '#4a4560', floor: '#6a4c3c', ceil: '#2f2c44', boards: 10 });
  s += win3(300, 170, 700, 340, { sky: ['#f3b98a', '#fde7c9'], sun: [.72, .7], far: '#c79a8e', near: '#7a6480', n: 4, frame: '#2e2a3e' });
  s += spill('330,610 990,610 1250,900 120,900', '#ffd9a6', .2) + dust(300, 200, 760, 380);
  s += flag3(1080, 190, true, 420) + flag3(1170, 210, false, 400);
  s += shelf3(1240, 170, 160, 440, '#5a3e30', 5, { seed: 2 });
  s += frame3(214, 200, 60, 84, '#c9a94a', '#3a3550');
  s += box3(470, 590, 660, 250, -0, 44, '#5f3d2c', { top: 1.3 }) + `<rect x="490" y="612" width="620" height="200" fill="none" stroke="#000" stroke-opacity=".18" stroke-width="3"/><rect x="730" y="640" width="140" height="44" rx="4" fill="#c9a94a" ${ol()}/><text x="800" y="671" font-size="24" font-weight="900" text-anchor="middle" fill="#3a2a1a" letter-spacing="6">総監</text>`;
  s += screen3(900, 452, 170, 100, 'log', { dur: 12 }) + paper3(560, 556, -6, 96, 30) + paper3(600, 548, 4, 96, 30);
  s += `<g class="o-phone"><rect x="700" y="552" width="120" height="30" rx="6" fill="#22232c" ${ol()}/><rect x="712" y="540" width="60" height="16" rx="6" fill="#30323e" ${ol()}/>${[0, 1, 2].map(i => `<circle class="a-ring" style="animation-delay:${i * .21}s" cx="${784 + i * 13}" cy="566" r="4.5" fill="#ff5a4a"/>`).join('')}</g>`;
  s += `<path d="M512 548 q-4 -60 30 -84 l26 10 q-30 20 -30 74Z" fill="#2b2d38" ${ol()}/><path d="M536 462 l44 16 l-14 26 l-46 -18Z" fill="#c9a94a" ${ol()}/>` + cone(548, 492, 220, 96, '#ffe9b0', .2);
  ANCH.soukan = { desk: [470, 500, 660, 330] };
  return s + grade('#ffb070', .08, 'soft-light') + vig3('#120c22', .55);
},
/* 玄関: looking at the front door from inside the flat */
genkan(){
  let s = room({ x0: 420, x1: 1180, y0: 100, y1: 640, wall: '#d9cdb8', side: '#c8baa2', floor: '#a9825e', ceil: '#efe8da', boards: 8, rows: 4 });
  s += `<polygon points="420,640 1180,640 1290,712 310,712" fill="#7d7f86"/><path d="M310 712 H1290" ${ol(3, .5)} fill="none"/>` + [0, 1, 2, 3, 4, 5].map(i => `<path d="M${420 + i * 152} 640 L${310 + i * 196} 712" stroke="#000" stroke-opacity=".15" stroke-width="2"/>`).join('') + `<polygon points="310,712 1290,712 1296,728 304,728" fill="#5d4530"/>`;
  s += downlight(800, 60) + cone(800, 66, 760, 620, '#fff0cc', .1);
  // door
  s += `<rect x="586" y="156" width="288" height="484" fill="#4a4036" ${ol()}/><rect x="600" y="170" width="260" height="470" fill="#3d5568" ${ol()}/><rect x="622" y="196" width="216" height="170" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="3"/><rect x="622" y="392" width="216" height="220" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="3"/><path d="M600 170 h60 l-40 470 h-20Z" fill="#fff" opacity=".06"/><circle cx="730" cy="270" r="7" fill="#1a1c22" stroke="#c9a94a" stroke-width="3"/>`;
  s += `<rect x="636" y="560" width="60" height="16" rx="3" fill="#2a2c34" ${ol(1.6)}/><rect x="642" y="564" width="48" height="8" fill="#0d0e12"/>`;
  // smart lock: body, keypad, LED, lever
  s += `<g class="o-lock"><rect x="792" y="352" width="52" height="124" rx="10" fill="#1d2028" ${ol()}/><rect x="798" y="358" width="40" height="18" rx="4" fill="#0e1016"/><circle class="a-ledb" cx="818" cy="367" r="5" fill="#4aa8ff"/><circle class="a-ledb" cx="818" cy="367" r="12" fill="#4aa8ff" opacity=".25"/>${[...Array(12)].map((_, i) => `<circle cx="${806 + (i % 3) * 12}" cy="${388 + Math.floor(i / 3) * 13}" r="3.6" fill="#3a4150"/>`).join('')}<text x="818" y="452" font-size="6.5" text-anchor="middle" fill="#8a94a8" font-family="monospace" letter-spacing="1">KEYSTONE</text><rect x="770" y="490" width="74" height="14" rx="7" fill="#b9bcc4" ${ol()}/><circle cx="836" cy="497" r="13" fill="#c9ccd4" ${ol()}/></g>`;
  // chain (hanging, not hooked)
  s += `<rect x="866" y="286" width="18" height="34" rx="3" fill="#b9bcc4" ${ol(1.6)}/><path class="a-sway3" d="M874 318 q-4 30 2 60 q4 12 -2 22" fill="none" stroke="#c9ccd4" stroke-width="5" stroke-dasharray="7 5" style="transform-origin:874px 318px"/><rect x="800" y="296" width="44" height="12" rx="4" fill="#b9bcc4" ${ol(1.6)}/>`;
  // shoe cabinet with key tray and plant
  s += box3(920, 470, 240, 170, -22, 22, '#b08a62') + `<path d="M1040 470 v170 M936 500 h88 M1056 500 h88" stroke="#000" stroke-opacity=".22" stroke-width="3"/><ellipse cx="980" cy="456" rx="34" ry="9" fill="#e8e2d2" ${ol(1.6)}/><path d="M966 452 l10 -4 l14 5" stroke="#8a7a4a" stroke-width="3" fill="none"/>` + plant3(1104, 448, .5);
  s += frame3(940, 220, 150, 110, '#3a3028', '#e9e1cf') + `<path d="M970 300 q20 -50 40 -20 q16 -30 44 20" fill="none" stroke="#3a4a5a" stroke-width="4"/>`;
  // umbrella stand
  s += `<rect x="470" y="540" width="56" height="100" rx="8" fill="#5a6470" ${ol()}/><path d="M486 540 l-10 -130 M508 540 l16 -150" stroke="#2a2c36" stroke-width="7" stroke-linecap="round"/><path d="M476 410 q-10 -14 4 -18 M524 390 q12 -14 -4 -18" fill="none" stroke="#2a2c36" stroke-width="5"/>`;
  // one pair of shoes on the stone step
  s += `<g class="o-shoes"><path d="M642 690 q4 -22 34 -22 q20 0 32 14 l0 10Z" fill="#2c2420" ${ol()}/><path d="M722 690 q4 -22 34 -22 q20 0 32 14 l0 10Z" fill="#2c2420" ${ol()}/><path d="M660 674 h20 M740 674 h20" stroke="#6a5a4a" stroke-width="3"/></g>` + tent(820, 706, 1);
  // way into the living room (right wall), warm light
  s += `<polygon points="${quad(RW, .28, .62, .2, 1)}" fill="#f6dfb0"/><polygon points="${quad(RW, .28, .62, .2, 1)}" fill="none" ${ol(3, .5)}/>` + spill(`${RW(.28, 1).join(',')} ${RW(.62, 1).join(',')} 900,760 1080,900 1500,900`, '#ffe2a8', .22);
  s += `<polygon points="${quad(LW, .35, .6, .3, .62)}" fill="#3a3028" ${ol()}/><polygon points="${quad(LW, .37, .58, .33, .59)}" fill="#b9d2dc"/>`;
  ANCH.genkan = { lock: [772, 340, 92, 176], chain: [790, 276, 110, 64], shoes: [620, 646, 190, 70], shelf: [920, 400, 250, 240], door: [600, 170, 170, 380] };
  return s + grade('#ffd9a0', .06, 'soft-light') + vig3('#1a1020', .5);
},
/* 居間と台所: desk with an empty outline, phone on a stand, kitchen counter with a wet marble board */
living(){
  let s = room({ x0: 190, x1: 1410, y0: 110, y1: 600, wall: '#e2d8c6', side: '#cfc3ae', floor: '#b48d66', ceil: '#f3ede0', boards: 12 });
  s += win3(590, 170, 430, 330, { sky: ['#a9d2f0', '#f2f7fb'], sun: [.2, .2], n: 2, frame: '#f1ece0', far: '#b8c8d8', near: '#7d92a8' });
  s += `<g class="a-curtain" style="transform-origin:600px 160px"><path d="M572 158 h120 q-30 180 -8 360 h-112Z" fill="#f6efe2" opacity=".9" ${ol(1.6, .4)}/><path d="M600 160 q-10 180 4 356 M640 160 q-14 180 8 356" stroke="#000" stroke-opacity=".08" stroke-width="5" fill="none"/></g><g class="a-curtain" style="transform-origin:1010px 160px;animation-delay:-2s"><path d="M1038 158 h-120 q30 180 8 360 h112Z" fill="#f6efe2" opacity=".9" ${ol(1.6, .4)}/><path d="M1010 160 q10 180 -4 356 M970 160 q14 180 -8 356" stroke="#000" stroke-opacity=".08" stroke-width="5" fill="none"/></g><rect x="556" y="148" width="498" height="12" rx="5" fill="#8a6a4a" ${ol(1.6)}/>`;
  s += spill('640,600 1000,600 1180,900 380,900', '#fff0c8', .22) + dust(560, 200, 520, 400, 16);
  // desk (left): cord only; a clean rectangle in the dust where the laptop sat
  s += `<rect x="232" y="196" width="250" height="150" fill="#b78f5e" ${ol()}/>` + [[246, 208, 70, 50, '#f4efe2'], [326, 214, 60, 70, '#e6dfcc'], [396, 206, 72, 46, '#f4efe2'], [250, 270, 84, 60, '#dfe6ea'], [344, 296, 60, 38, '#f4efe2'], [414, 262, 54, 70, '#efe2c8']].map((q, i) => `<rect x="${q[0]}" y="${q[1]}" width="${q[2]}" height="${q[3]}" fill="${q[4]}" transform="rotate(${[-3, 2, 4, -2, 3, -4][i]} ${q[0] + q[2] / 2} ${q[1] + q[3] / 2})" ${ol(1.2, .5)}/><circle cx="${q[0] + q[2] / 2}" cy="${q[1] + 6}" r="3.5" fill="#c8382f"/>`).join('') + `<path d="M280 232 L350 250 L430 228" stroke="#c8382f" stroke-width="1.6" fill="none"/>`;
  s += box3(226, 470, 320, 26, 30, 40, '#7b5a40', { shadow: 0 }) + `<rect x="238" y="496" width="16" height="130" fill="#5f4430" ${ol()}/><rect x="520" y="496" width="16" height="130" fill="#5f4430" ${ol()}/><rect x="554" y="460" width="14" height="150" fill="#4f3828" ${ol()}/>`;
  s += `<g class="o-desk"><polygon points="330,462 470,462 486,440 350,440" fill="#fff" opacity=".12"/><polygon points="330,462 470,462 486,440 350,440" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="4 4"/><path d="M486 452 q40 6 30 30 q-8 20 26 24" fill="none" stroke="#1f2026" stroke-width="5" stroke-linecap="round"/><rect x="536" y="498" width="22" height="14" rx="3" fill="#1f2026"/><rect x="262" y="424" width="44" height="34" fill="#2e4a6a" ${ol(1.6)}/><rect x="266" y="414" width="40" height="12" fill="#a8443a" ${ol(1.6)}/><path d="M296 440 q-10 -70 26 -84 l22 8 q-26 14 -22 60" fill="#2b2d38" ${ol()}/></g>` + chair3(400, 540, '#4a4e5c');
  // sofa under the window, side table with the phone on its stand
  s += `<rect x="690" y="470" width="330" height="80" rx="18" fill="#6f7f9a" ${ol()}/><rect x="672" y="520" width="366" height="96" rx="18" fill="#8090ac" ${ol()}/><rect x="660" y="500" width="40" height="118" rx="14" fill="#93a2bc" ${ol()}/><rect x="1010" y="500" width="40" height="118" rx="14" fill="#93a2bc" ${ol()}/><rect x="740" y="496" width="90" height="60" rx="12" fill="#d9a05a" ${ol()}/><ellipse cx="855" cy="630" rx="200" ry="14" fill="#000" opacity=".14"/>`;
  s += `<g class="o-phone"><ellipse cx="616" cy="584" rx="46" ry="12" fill="#6a4c36" ${ol()}/><rect x="610" y="584" width="12" height="60" fill="#5a3f2c" ${ol()}/><ellipse cx="616" cy="646" rx="30" ry="8" fill="#5a3f2c" ${ol()}/><path d="M598 580 l8 -50 h30 l-6 50Z" fill="#17181e" ${ol()}/><path class="a-alarm" d="M609 572 l6 -36 h16 l-4 36Z" fill="#ffb347"/><path d="M590 582 h44 v6 h-44Z" fill="#d9d4c8" ${ol(1.4)}/></g>`;
  // kitchen (right): wall cabinets, hood, counter, sink, drying rack
  s += `<rect x="1070" y="170" width="320" height="150" fill="#f1ece2" ${ol()}/><path d="M1176 170 v150 M1284 170 v150" stroke="#000" stroke-opacity=".2" stroke-width="3"/><rect x="1150" y="240" width="14" height="6" fill="#8a8a92"/><rect x="1258" y="240" width="14" height="6" fill="#8a8a92"/><rect x="1366" y="240" width="14" height="6" fill="#8a8a92"/><rect x="1070" y="330" width="320" height="130" fill="#cfd9dc" opacity=".8"/>` + [...Array(5)].map((_, i) => `<path d="M${1070 + i * 80} 330 v130" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>`).join('') + `<path d="M1070 394 h320" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>`;
  s += box3(1060, 462, 360, 178, -30, 30, '#e9e2d3', { top: 1.05 }) + `<path d="M1180 462 v178 M1300 462 v178" stroke="#000" stroke-opacity=".16" stroke-width="3"/><rect x="1150" y="530" width="18" height="6" fill="#8a8a92"/><rect x="1270" y="530" width="18" height="6" fill="#8a8a92"/><rect x="1390" y="530" width="18" height="6" fill="#8a8a92"/>`;
  s += `<g class="o-sink"><polygon points="1068,456 1176,456 1166,438 1062,438" fill="#9aa4ac" ${ol(1.6)}/><polygon points="1076,453 1168,453 1160,441 1070,441" fill="#6f7a84"/><path d="M1118 438 v-40 q0 -14 14 -14 h12 v10" fill="none" stroke="#c4c8d0" stroke-width="7" stroke-linecap="round"/><ellipse cx="1126" cy="447" rx="15" ry="5" fill="#f4f6f8" ${ol(1.4)}/><path d="M1120 446 q6 3 12 0" stroke="#4a9a5a" stroke-width="3" fill="none"/></g>`;
  s += `<g class="o-rack"><path d="M1196 452 h170 l-10 -14 h-150Z" fill="#b9bec6" ${ol(1.6)}/>${[0, 1, 2].map(i => `<ellipse cx="${1218 + i * 16}" cy="420" rx="6" ry="24" fill="#f6f4ee" ${ol(1.4)}/>`).join('')}<rect x="1270" y="412" width="18" height="30" rx="3" fill="#dfeef4" opacity=".8" ${ol(1.4)}/><g class="o-board"><path d="M1302 446 l6 -78 h48 l-4 78Z" fill="#eceae6" ${ol()}/><path d="M1314 380 q12 20 2 40 q-6 14 6 24 M1338 372 q-8 26 6 44" stroke="#9a9aa6" stroke-width="2" fill="none"/><path d="M1310 372 l6 0 l-5 70 l-6 0Z" fill="#fff" opacity=".7"/><ellipse class="a-drip" cx="1330" cy="440" rx="3" ry="5" fill="#bfe4f6"/><ellipse cx="1330" cy="451" rx="26" ry="4" fill="#bfe4f6" opacity=".75"/></g></g>`;
  s += `<rect x="1378" y="408" width="30" height="40" rx="8" fill="#c8382f" ${ol()}/><path d="M1408 420 q14 4 0 18" fill="none" ${ol(3)}/><rect x="1384" y="398" width="18" height="12" rx="3" fill="#2a2c34"/>`;
  s += `<ellipse cx="800" cy="760" rx="420" ry="90" fill="#7d6a8a" opacity=".35"/><ellipse cx="800" cy="760" rx="380" ry="76" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="4"/>` + plant3(1470, 760, 1.1);
  ANCH.living = { desk: [226, 400, 340, 110], cork: [232, 196, 250, 150], phone: [566, 516, 100, 140], sofa: [680, 470, 360, 150], window: [590, 170, 430, 290], kitchen: [1050, 330, 370, 310], board: [1296, 362, 66, 96], cup: [1104, 432, 46, 26], rack: [1200, 392, 96, 60], kettle: [1372, 394, 44, 58] };
  return s + grade('#ffe2b0', .07, 'soft-light') + vig3('#1c1220', .45);
},
/* 浴室 */
bath(){
  let s = room({ x0: 300, x1: 1300, y0: 90, y1: 600, wall: '#cfe2e2', side: '#b8d0d2', floor: '#9fb6ba', ceil: '#eef4f2', boards: 9, rows: 6, tile: 1 });
  for (let i = 1; i < 9; i++) s += `<path d="M${300 + i * 111} 90 V586" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>`; for (let i = 1; i < 5; i++) s += `<path d="M300 ${90 + i * 102} H1300" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>`;
  s += `<rect x="680" y="140" width="220" height="130" fill="#e9f3f6" ${ol()}/><path d="M680 140 l220 130 M790 140 v130" stroke="#fff" stroke-opacity=".7" stroke-width="3"/><rect x="680" y="140" width="220" height="130" fill="#bfe0ee" opacity=".4"/>` + spill('700,600 900,600 1060,900 560,900', '#e8fbff', .2) + downlight(800, 50);
  // tub
  s += `<g class="o-tub"><path d="M330 500 h640 q20 0 20 20 v150 q0 24 -24 24 h-632 q-24 0 -24 -24 v-150 q0 -20 20 -20Z" fill="#f4f6f4" ${ol()}/><polygon points="330,500 970,500 930,452 380,452" fill="#fbfcfb" ${ol()}/><polygon points="372,492 930,492 900,462 404,462" fill="#c9dcdf" ${ol(1.6, .4)}/><path d="M330 500 h640" stroke="#fff" stroke-width="6" stroke-linecap="round"/><path d="M340 560 h620" stroke="#000" stroke-opacity=".06" stroke-width="26"/><path d="M610 494 q10 -6 22 0 q8 5 18 -1" stroke="#8a2f2a" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="660" cy="506" r="3" fill="#8a2f2a"/><path d="M880 452 v-60 q0 -16 -18 -16 h-20" fill="none" stroke="#c4c8d0" stroke-width="9" stroke-linecap="round"/><circle cx="880" cy="430" r="10" fill="#d4d8de" ${ol(1.6)}/></g>` + tent(590, 448, 2);
  // towels on the shelf, bottles
  s += `<g class="o-towel"><rect x="1050" y="300" width="210" height="14" fill="#8a9aa0" ${ol(1.6)}/><rect x="1050" y="430" width="210" height="14" fill="#8a9aa0" ${ol(1.6)}/><rect x="1050" y="560" width="210" height="14" fill="#8a9aa0" ${ol(1.6)}/>${[0, 1, 2].map(i => `<rect x="1066" y="${394 - i * 30}" width="130" height="30" rx="8" fill="${['#f4efe4', '#e6efe9', '#f4efe4'][i]}" ${ol()}/><path d="M1076 ${409 - i * 30} h110" stroke="#000" stroke-opacity=".1" stroke-width="3"/>`).join('')}<rect x="1210" y="380" width="22" height="50" rx="6" fill="#6aa0c2" ${ol(1.6)}/><rect x="1070" y="498" width="26" height="62" rx="6" fill="#e0b85a" ${ol(1.6)}/><rect x="1106" y="510" width="26" height="50" rx="6" fill="#d98a8a" ${ol(1.6)}/><rect x="1150" y="520" width="70" height="40" rx="6" fill="#f4efe4" ${ol(1.6)}/></g>`;
  s += `<rect x="1090" y="150" width="150" height="120" rx="8" fill="#dfeef2" ${ol()}/><path d="M1100 160 l60 0 l-40 100 l-20 0Z" fill="#fff" opacity=".5"/>`;
  s += `<path d="M1010 760 q30 -30 80 -24 q46 6 70 -10" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="5" stroke-dasharray="14 10"/>` + tent(1120, 800, 3);
  s += `<circle cx="760" cy="760" r="34" fill="#7f969a" ${ol()}/>` + [...Array(6)].map((_, i) => `<path d="M${738 + i * 9} 742 v36" stroke="#000" stroke-opacity=".35" stroke-width="3"/>`).join('');
  ANCH.bath = { tub: [560, 440, 180, 90], floor: [620, 700, 560, 170], towel: [1050, 290, 220, 290], window: [680, 140, 220, 130], mirror: [1090, 150, 150, 120], drain: [716, 716, 90, 90] };
  return s + grade('#bfe8f0', .08, 'soft-light') + vig3('#0e1a22', .5);
},
/* 12階の廊下 */
hall(){
  let s = room({ x0: 560, x1: 1040, y0: 250, y1: 610, wall: '#c9c4b6', side: '#bdb7a6', floor: '#5d6876', ceil: '#e3dfd2', boards: 4, rows: 7 });
  s += `<polygon points="620,610 980,610 1420,900 180,900" fill="#6d7a8a" opacity=".5"/>`;
  // ceiling lights
  for (const t of [.25, .55, .8]){ const y = 250 * t, xl = 560 * t + (W3 - 2 * 560 * t) * .38, xr = 560 * t + (W3 - 2 * 560 * t) * .62; s += `<polygon points="${xl},${y} ${xr},${y} ${xr - 20 * (1 - t)},${y + 26 * (1 - t) + 6} ${xl + 20 * (1 - t)},${y + 26 * (1 - t) + 6}" fill="#fffbe6" ${ol(1.6, .4)}/>`; }
  s += cone(800, 30, 900, 860, '#fff6d8', .08);
  // elevator at the far end
  s += `<g class="o-elev"><rect x="690" y="300" width="220" height="310" fill="#8a8f98" ${ol()}/><rect x="704" y="324" width="94" height="286" fill="#b4bac2" ${ol(1.6)}/><rect x="802" y="324" width="94" height="286" fill="#aab0b8" ${ol(1.6)}/><path d="M712 330 l30 0 l-20 270 l-10 0Z" fill="#fff" opacity=".25"/><rect x="770" y="266" width="60" height="28" rx="4" fill="#12141a" ${ol(1.6)}/><text x="800" y="288" font-size="20" font-family="monospace" font-weight="700" text-anchor="middle" fill="#ffb347">12</text><rect x="930" y="430" width="22" height="46" rx="4" fill="#d4d8de" ${ol(1.6)}/><circle class="a-blink" cx="941" cy="444" r="4" fill="#ffb347"/><circle cx="941" cy="462" r="4" fill="#6a6e78"/></g>`;
  // right wall: 1203 (far) and 1204 (near, taped)
  const door = (t0, t1, n, tape) => { const p = quad(RW, t0, t1, .3, 1), a = RW(t0, .3), b = RW(t1, .3), c = RW(t1, 1), d = RW(t0, 1); let o = `<polygon points="${p}" fill="#4b5f70" ${ol()}/><polygon points="${quad(RW, t0 + (t1 - t0) * .12, t1 - (t1 - t0) * .12, .36, .62)}" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="3"/>`; const m = RW((t0 + t1) / 2, .25); o += `<text x="${m[0]}" y="${m[1]}" font-size="${22 - t0 * 8}" font-weight="900" text-anchor="middle" fill="#3a3a44" font-family="monospace">${n}</text>`; const k = RW(t1 - (t1 - t0) * .16, .66); o += `<rect x="${k[0] - 7}" y="${k[1] - 22}" width="14" height="44" rx="4" fill="#1d2028" ${ol(1.4)}/><circle class="a-ledb" cx="${k[0]}" cy="${k[1] - 14}" r="2.6" fill="#4aa8ff"/>`; if (tape) o += `<path d="M${a[0] + 6} ${a[1] + 30} L${c[0] - 6} ${c[1] - 60} M${b[0] - 6} ${b[1] + 40} L${d[0] + 6} ${d[1] - 80}" stroke="#f2c230" stroke-width="16"/><path d="M${a[0] + 6} ${a[1] + 30} L${c[0] - 6} ${c[1] - 60} M${b[0] - 6} ${b[1] + 40} L${d[0] + 6} ${d[1] - 80}" stroke="#241a2c" stroke-width="16" stroke-dasharray="6 22" opacity=".8"/>`; return o; };
  s += door(.7, .86, '1203', 0) + door(.22, .52, '1204', (typeof CID === 'undefined' || CID === '011') ? 1 : 0);
  // left wall: emergency exit with a failing green lamp, extinguisher
  const ex = LW(.74, .22), e2 = LW(.86, .22); s += `<polygon points="${quad(LW, .7, .9, .32, 1)}" fill="#8f9a8a" ${ol()}/><polygon points="${quad(LW, .74, .86, .4, .7)}" fill="none" stroke="#000" stroke-opacity=".2" stroke-width="3"/>`;
  s += `<g class="o-lamp"><polygon points="${quad(LW, .73, .87, .2, .285)}" fill="#0f3a22" ${ol(1.6)}/><polygon class="a-exit" points="${quad(LW, .735, .865, .208, .277)}" fill="#3dff8f"/><polygon class="a-exit" points="${quad(LW, .7, .9, .17, .32)}" fill="#3dff8f" opacity=".16"/></g>`;
  s += `<polygon points="${quad(LW, .36, .48, .56, .8)}" fill="#c8382f" ${ol()}/><polygon points="${quad(LW, .39, .45, .6, .76)}" fill="#f4efe4" opacity=".4"/>`;
  // ceiling camera with the NPA sticker
  s += `<g class="o-cam"><ellipse cx="800" cy="168" rx="40" ry="10" fill="#d9d9de" ${ol()}/><path d="M770 170 q4 44 30 44 q26 0 30 -44Z" fill="#20222a" ${ol()}/><ellipse cx="800" cy="196" rx="13" ry="10" fill="#0a0b10" stroke="#3a3f4c" stroke-width="2"/><circle cx="796" cy="193" r="3" fill="#fff" opacity=".6"/><circle class="a-blink" cx="822" cy="180" r="3" fill="#ff4a3a"/><rect x="842" y="160" width="34" height="13" fill="#f4efe4" ${ol(1)}/><text x="859" y="169.5" font-size="6" text-anchor="middle" fill="#27366e" font-weight="900" font-family="monospace">NPA 5/17</text></g>`;
  s += `<path d="M0 900 L560 610 M1600 900 L1040 610" stroke="#000" stroke-opacity=".2" stroke-width="3"/>`;
  ANCH.hall = { cam: [748, 150, 140, 76], lamp: [Math.round(LW(.73, .2)[0]) - 14, Math.round(LW(.73, .17)[1]), Math.round(LW(.9, .2)[0] - LW(.7, .2)[0]) + 40, 110], elev: [690, 266, 270, 344], door1204: [Math.round(RW(.52, .3)[0]), Math.round(RW(.22, .3)[1]), Math.round(RW(.22, .3)[0] - RW(.52, .3)[0]), 520], ext: [Math.round(LW(.36, .5)[0]) - 10, Math.round(LW(.36, .56)[1]) - 10, 110, 190] };
  return s + grade('#9fd0c0', .06, 'soft-light') + vig3('#0c1016', .6);
},
/* 管理人室 */
kanri(){
  let s = room({ x0: 240, x1: 1360, y0: 110, y1: 610, wall: '#b9b39c', side: '#a59f88', floor: '#7a7466', ceil: '#d6d0bc', boards: 10 });
  s += `<g class="o-rec"><rect x="300" y="190" width="460" height="420" fill="#3a3d46" ${ol()}/>` + screen3(326, 214, 408, 240, 'cctv', { stand: 0 }) + `<rect x="326" y="480" width="408" height="50" rx="4" fill="#22242c" ${ol(1.6)}/>${[...Array(8)].map((_, i) => `<circle class="a-blink" style="animation-delay:${i * .23}s" cx="${350 + i * 22}" cy="505" r="4" fill="${i % 3 ? '#5aff9a' : '#ffb347'}"/>`).join('')}<rect x="560" y="494" width="150" height="22" fill="#0d0e12"/><text x="635" y="510" font-size="13" font-family="monospace" text-anchor="middle" fill="#7fd0ff">REC 7日保存</text><rect x="326" y="546" width="408" height="50" rx="4" fill="#22242c" ${ol(1.6)}/><path d="M346 571 h368" stroke="#3a3f4c" stroke-width="12" stroke-dasharray="3 9"/></g>`;
  s += `<rect x="800" y="170" width="130" height="170" fill="#8a6a4a" ${ol()}/>` + [...Array(12)].map((_, i) => `<path d="M${822 + (i % 4) * 30} ${200 + Math.floor(i / 4) * 46} v18" stroke="#d9d4c4" stroke-width="5" stroke-linecap="round"/><circle cx="${822 + (i % 4) * 30}" cy="${196 + Math.floor(i / 4) * 46}" r="4" fill="#c9a94a"/>`).join('');
  s += `<g class="o-kshelf">` + shelf3(980, 180, 340, 430, '#7a8088', 4, { binder: 1, pal: ['#3a6aa2', '#a8443a', '#4a7a5a', '#c9a43a', '#5a5a66'], seed: 1 }) + `</g>`;
  s += box3(700, 540, 320, 190, 0, 34, '#8a7458', { top: 1.2 }) + `<g class="o-kmon">` + screen3(770, 400, 150, 96, 'doc', { col: '#14201c', ink: '#8fe0a8' }) + `</g><text x="845" y="392" font-size="13" text-anchor="middle" fill="#3a3a44" font-weight="700">EV</text>`;
  s += `<path d="M960 500 h36 l-5 32 h-26Z" fill="#f4efe4" ${ol()}/><path class="a-steam" d="M970 492 q-8 -14 0 -28" stroke="#fff" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/><path class="a-steam" style="animation-delay:-1.2s" d="M984 492 q-8 -14 0 -28" stroke="#fff" stroke-width="4" fill="none" opacity=".6" stroke-linecap="round"/>`;
  s += `<g class="o-aid"><rect x="716" y="512" width="40" height="18" rx="5" fill="#f4efe4" ${ol(1.4)}/><circle class="a-blink" cx="748" cy="521" r="2.6" fill="#5aff9a"/><path d="M724 512 q4 -12 12 -6" stroke="#c9a08a" stroke-width="4" fill="none" stroke-linecap="round"/></g>`;
  s += `<rect x="262" y="250" width="26" height="150" fill="#f4efe4" ${ol(1.4)}/><text x="275" y="280" font-size="14" text-anchor="middle" fill="#a8443a" font-weight="900">6</text>` + downlight(800, 56) + cone(800, 62, 900, 700, '#fff4c8', .1);
  ANCH.kanri = { rec: [300, 190, 460, 420], shelf: [980, 180, 340, 430], monitor: [756, 384, 180, 150], keys: [800, 170, 130, 170], aid: [706, 498, 60, 40] };
  return s + grade('#ffe0a0', .08, 'soft-light') + vig3('#14100c', .6);
},
/* FBI東京駐在官室: three clocks */
fbi(){
  let s = room({ x0: 210, x1: 1390, y0: 110, y1: 610, wall: '#2c3a58', side: '#25304a', floor: '#3c3a44', ceil: '#1a2236', boards: 10 });
  s += `<rect x="210" y="430" width="1180" height="180" fill="#3a2c24"/><path d="M210 430 h1180" ${ol(2, .5)} fill="none"/>`;
  s += `<g class="o-clocks"><rect x="470" y="150" width="660" height="170" rx="8" fill="#1c2438" ${ol()}/>` + clock3(580, 222, 50, 4, 10, 'WASHINGTON') + clock3(800, 222, 50, 8, 10, 'UTC') + clock3(1020, 222, 50, 5, 10, 'TOKYO') + `</g>`;
  s += `<circle cx="372" cy="260" r="76" fill="#1c2438" stroke="#c9a94a" stroke-width="6"/><circle cx="372" cy="260" r="58" fill="none" stroke="#c9a94a" stroke-width="2"/><path d="M372 214 l12 34 h36 l-29 21 l11 34 l-30 -21 l-30 21 l11 -34 l-29 -21 h36Z" fill="#c9a94a"/><text x="372" y="364" font-size="16" text-anchor="middle" fill="#c9a94a" font-weight="900" letter-spacing="4">LEGAT TOKYO</text>`;
  s += win3(1180, 170, 180, 240, { sky: ['#8fb6dc', '#dbe8f3'], n: 1, frame: '#141a2a', blind: 9, blindc: '#3a4666' }) + spill('1180,610 1360,610 1500,900 1000,900', '#bcd8ff', .12);
  s += flag3(232, 250, false, 360);
  s += box3(430, 590, 740, 250, 0, 44, '#2a2f3e', { top: 1.35 }) + screen3(560, 440, 190, 110, 'log', { ink: '#8fb8ff', dur: 14 }) + screen3(820, 440, 190, 110, 'map', { ink: '#8fb8ff' }) + `<rect x="1050" y="548" width="34" height="40" rx="6" fill="#f4efe4" ${ol()}/><text x="1067" y="574" font-size="9" text-anchor="middle" fill="#27366e" font-weight="900">LEGAT</text>` + paper3(470, 556, -8, 80, 28);
  ANCH.fbi = { clocks: [470, 150, 660, 170], seal: [292, 180, 160, 200], desk: [430, 440, 740, 200] };
  return s + grade('#3a6aff', .08, 'soft-light') + vig3('#05070f', .65);
},
/* 警備局の一室 */
keibi(){
  let s = room({ x0: 230, x1: 1370, y0: 110, y1: 610, wall: '#8d9198', side: '#7c8088', floor: '#55585f', ceil: '#b4b8be', boards: 10 });
  s += win3(300, 180, 300, 260, { sky: ['#c9d2da', '#eef1f3'], n: 1, frame: '#4a4e56', blind: 10, blindc: '#c9cdd2' });
  s += [...Array(9)].map((_, i) => `<polygon class="a-slat" style="animation-delay:${i * .3}s" points="${330 + i * 6},${640 + i * 26} ${600 + i * 30},${640 + i * 26} ${606 + i * 30},${650 + i * 26} ${332 + i * 6},${650 + i * 26}" fill="#fff" opacity=".1"/>`).join('');
  s += `<g class="o-cab">` + [0, 1, 2].map(i => `<rect x="${980 + i * 124}" y="240" width="116" height="370" fill="#6a7078" ${ol()}/>` + [0, 1, 2, 3].map(j => `<rect x="${988 + i * 124}" y="${250 + j * 90}" width="100" height="80" fill="#7c828a" ${ol(1.6)}/><rect x="${1022 + i * 124}" y="${284 + j * 90}" width="32" height="10" rx="3" fill="#3a3f4c"/>${(i + j) % 3 === 0 ? `<rect x="${996 + i * 124}" y="${258 + j * 90}" width="26" height="18" fill="#f4efe4"/><text x="${1009 + i * 124}" y="${272 + j * 90}" font-size="13" text-anchor="middle" fill="#b8283a" font-weight="900">秘</text>` : ''}`).join('')).join('') + `</g>`;
  s += clock3(800, 190, 42, 10, 40, '') + `<rect x="700" y="270" width="200" height="120" fill="#7c8088" ${ol()}/><text x="800" y="318" font-size="20" text-anchor="middle" fill="#3a3f4c" font-weight="900" letter-spacing="6">警備局</text><text x="800" y="352" font-size="14" text-anchor="middle" fill="#3a3f4c" letter-spacing="3">外事課</text>`;
  s += box3(420, 620, 760, 40, 0, 60, '#4a4e56', { top: 1.5 }) + `<rect x="460" y="660" width="26" height="200" fill="#3a3d44" ${ol()}/><rect x="1114" y="660" width="26" height="200" fill="#3a3d44" ${ol()}/>` + paper3(700, 580, -4, 110, 30) + `<path d="M930 600 q-6 -70 30 -92 l24 10 q-28 20 -26 82Z" fill="#22242c" ${ol()}/>` + cone(960, 520, 300, 110, '#fff0c0', .22);
  ANCH.keibi = { cab: [980, 240, 372, 370], window: [300, 180, 300, 260] };
  return s + grade('#8fa8c0', .1, 'soft-light') + vig3('#0a0c10', .65);
},
/* 科捜研 */
kasouken(){
  let s = room({ x0: 230, x1: 1370, y0: 110, y1: 610, wall: '#d4e2e4', side: '#bfd0d4', floor: '#7f9298', ceil: '#eef3f2', boards: 10, tile: 1 });
  s += shelf3(260, 180, 300, 250, '#9aa8ac', 3, { pal: ['#6aa0c2', '#e0b85a', '#d98a8a', '#8fc0a0', '#f4efe4'], seed: 4 }) + screen3(640, 200, 300, 180, 'wave', { ink: '#6fe0c0', col: '#0c2224', stand: 0 }) + screen3(1000, 200, 300, 180, 'log', { ink: '#6fe0c0', col: '#0c2224', stand: 0, dur: 16 });
  s += box3(250, 520, 1100, 120, 0, 50, '#e6ecec', { top: 1.02 }) + `<path d="M620 520 v120 M990 520 v120" stroke="#000" stroke-opacity=".15" stroke-width="3"/>`;
  s += `<g class="o-scope"><rect x="330" y="486" width="110" height="16" rx="4" fill="#2a2c36" ${ol()}/><path d="M370 486 v-70 l40 -40 l16 16 l-30 30 v64Z" fill="#3a3f4c" ${ol()}/><rect x="398" y="360" width="26" height="40" rx="4" fill="#22242c" transform="rotate(45 411 380)" ${ol()}/></g>`;
  s += `<g class="o-tray"><ellipse cx="800" cy="492" rx="110" ry="20" fill="#c4ccd0" ${ol()}/><rect x="770" y="450" width="60" height="36" rx="8" fill="#1d2028" ${ol()}/><circle class="a-ledb" cx="800" cy="462" r="4" fill="#4aa8ff"/><circle cx="800" cy="380" r="56" fill="none" stroke="#fff6d8" stroke-width="10" opacity=".9"/><circle cx="800" cy="380" r="56" fill="none" ${ol(1.6, .4)}/><path d="M856 380 h60 v-200" fill="none" stroke="#3a3f4c" stroke-width="8"/></g>` + cone(800, 420, 240, 90, '#fff6d8', .3);
  s += [0, 1, 2, 3].map(i => `<path d="M${1090 + i * 44} 500 v-50 h20 v50 q0 8 -10 8 q-10 0 -10 -8Z" fill="${['#8fd0e8', '#e8c88f', '#c8e88f', '#e88fb0'][i]}" opacity=".85" ${ol(1.6)}/>`).join('');
  ANCH.kasouken = { tray: [690, 320, 230, 200] };
  return s + grade('#a0e8e0', .08, 'soft-light') + vig3('#081416', .55);
},
/* サイバー課 */
cyber(){
  let s = room({ x0: 230, x1: 1370, y0: 110, y1: 610, wall: '#1a2030', side: '#141a28', floor: '#22262e', ceil: '#0e121c', boards: 10 });
  s += screen3(280, 170, 330, 220, 'map', { ink: '#5ad0ff', col: '#08141e', stand: 0 }) + screen3(640, 170, 330, 220, 'log', { ink: '#5ad0ff', col: '#08141e', stand: 0, dur: 7 }) + screen3(1000, 170, 330, 220, 'wave', { ink: '#5aff9a', col: '#08141e', stand: 0 });
  s += [0, 1, 2].map(i => `<rect x="${290 + i * 110}" y="430" width="96" height="180" fill="#10141c" ${ol()}/>` + [...Array(8)].map((_, j) => `<rect x="${298 + i * 110}" y="${440 + j * 21}" width="80" height="15" fill="#1a2030"/><circle class="a-blink" style="animation-delay:${(i * 3 + j) * .17}s" cx="${308 + i * 110}" cy="${447 + j * 21}" r="3" fill="${(i + j) % 4 ? '#5aff9a' : '#ffb347'}"/>`).join('')).join('');
  s += box3(700, 560, 640, 200, 0, 40, '#2a2f3e', { top: 1.4 }) + screen3(780, 420, 180, 100, 'log', { ink: '#5ad0ff', dur: 5 }) + screen3(1040, 420, 180, 100, 'doc', { ink: '#5ad0ff' }) + cone(1000, 110, 900, 600, '#5ad0ff', .06);
  ANCH.cyber = {};
  return s + grade('#2a6aff', .12, 'soft-light') + vig3('#02040a', .7);
},
/* 連絡調整室 */
renraku(){
  let s = room({ x0: 250, x1: 1350, y0: 110, y1: 610, wall: '#c6c9c2', side: '#b3b6ae', floor: '#6c6258', ceil: '#dfe1da', boards: 10 });
  s += win3(330, 180, 360, 280, { sky: ['#f0b890', '#f8e0c4'], sun: [.6, .8], n: 2, frame: '#5a5e5a', blind: 8, blindc: '#e6e2d6', far: '#c8a090', near: '#8a6a70' }) + spill('360,610 700,610 900,900 200,900', '#ffcf9a', .16);
  s += shelf3(980, 170, 340, 440, '#7a6a58', 4, { binder: 1, pal: ['#27366e', '#27366e', '#8a2a2a', '#8a2a2a', '#4a4e56', '#c9a43a'], seed: 3 }) + `<text x="1150" y="162" font-size="14" text-anchor="middle" fill="#3a3a44" font-weight="700" letter-spacing="3">FBI ／ 警備局 ／ 一課</text>`;
  s += `<g class="o-news"><ellipse cx="420" cy="640" rx="110" ry="24" fill="#7a5c44" ${ol()}/><rect x="412" y="640" width="16" height="120" fill="#5f4430" ${ol()}/><g transform="rotate(-8 420 624)"><rect x="350" y="606" width="140" height="34" fill="#efeadc" ${ol(1.6)}/><path d="M360 616 h60 M360 626 h44 M430 614 h50 M430 622 h50 M430 630 h36" stroke="#55555f" stroke-width="3"/><ellipse cx="455" cy="622" rx="30" ry="14" fill="none" stroke="#c8283a" stroke-width="3"/></g></g>`;
  s += box3(520, 600, 620, 240, 0, 46, '#6a5038', { top: 1.3 }) + `<g class="o-drawer"><rect x="540" y="618" width="260" height="62" fill="#7a5e44" ${ol(1.8)}/><rect x="646" y="642" width="48" height="12" rx="4" fill="#c9a94a" ${ol(1.2)}/></g><rect x="540" y="692" width="260" height="130" fill="#7a5e44" ${ol(1.8)}/><rect x="860" y="618" width="260" height="204" fill="#7a5e44" ${ol(1.8)}/>`;
  s += `<g class="o-photo"><path d="M900 590 l10 -78 h86 l10 78Z" fill="#3a3028" ${ol()}/><path d="M912 582 l8 -62 h66 l8 62Z" fill="#9fc4d8"/><circle cx="940" cy="546" r="11" fill="#e8c0a0"/><circle cx="968" cy="542" r="12" fill="#e2b898"/><path d="M924 582 q16 -28 32 0 M950 582 q18 -32 36 0" fill="#3a4a66"/><path d="M912 574 h82" stroke="#3a6a8a" stroke-width="5"/></g>`;
  s += `<g class="o-cal"><path d="M660 590 l8 -60 h70 l8 60Z" fill="#f4efe4" ${ol()}/><rect x="668" y="530" width="70" height="14" fill="#b8283a"/>${[...Array(15)].map((_, i) => `<rect x="${674 + (i % 5) * 13}" y="${550 + Math.floor(i / 5) * 12}" width="8" height="7" fill="#9a9aa6" opacity=".6"/>`).join('')}<circle cx="704" cy="553" r="8" fill="none" stroke="#c8283a" stroke-width="2.4"/></g>`;
  s += `<path d="M800 590 v-40 M830 590 v-40" stroke="#c9a94a" stroke-width="4"/><rect x="776" y="548" width="26" height="18" fill="#fbfbf6" ${ol(1.2)}/><circle cx="789" cy="557" r="5" fill="#c8283a"/><rect x="830" y="548" width="26" height="18" fill="#fbfbf6" ${ol(1.2)}/><path d="M830 552 h26 M830 558 h26 M830 564 h26" stroke="#b8283a" stroke-width="2"/><rect x="830" y="548" width="11" height="9" fill="#27366e"/>` + screen3(560, 470, 150, 90, 'doc', { ink: '#9fd0ff' });
  ANCH.renraku = { desk: [540, 612, 260, 76], news: [320, 590, 200, 80], photo: [896, 506, 114, 90], cal: [656, 524, 94, 70], shelf: [980, 170, 340, 440] };
  return s + grade('#ffb880', .1, 'soft-light') + vig3('#140c0a', .6);
}
};
if (typeof module !== 'undefined') module.exports = { SC3, ANCH };
