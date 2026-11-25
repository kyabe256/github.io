/* ---------- audio: voice pack, synth BGM, SFX ---------- */
const AudioSys = (() => {
  let ctx = null, master, bgmG, seG, voG, ana, anaBuf, pack = null, packIdx = null, vmode = 'game', curV = null, bgmName = null, timer = null, nextT = 0, step = 0, noiseBuf;
  const vol = { bgm: 0.45, se: 0.7, voice: 1 };
  const fnv = s => { let h = 0x811c9dc5; const b = new TextEncoder().encode(s); for (const x of b){ h ^= x; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, '0'); };
  function init(){
    if (ctx) { if (ctx.state === 'suspended') ctx.resume(); return; }
    const AC = window.AudioContext || window.webkitAudioContext; try { ctx = new AC({ latencyHint: 'playback' }); } catch (e) { ctx = new AC(); }
    master = ctx.createGain(); master.gain.value = 0.9;
    try { const lim = ctx.createDynamicsCompressor(); lim.threshold.value = -8; lim.knee.value = 6; lim.ratio.value = 12; lim.attack.value = 0.003; lim.release.value = 0.2; master.connect(lim); lim.connect(ctx.destination); } catch (e) { master.connect(ctx.destination); }
    bgmG = ctx.createGain(); bgmG.gain.value = vol.bgm; bgmG.connect(master);
    seG = ctx.createGain(); seG.gain.value = vol.se; seG.connect(master);
    voG = ctx.createGain(); voG.gain.value = vol.voice * 1.15; ana = ctx.createAnalyser(); ana.fftSize = 512; anaBuf = new Uint8Array(ana.fftSize); voG.connect(ana); ana.connect(master);
    noiseBuf = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate); const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  }
  async function loadPack(url, idx){ pack = null; packIdx = idx || null; try { const r = await fetch(url); if (!r.ok) throw 0; pack = await r.arrayBuffer(); } catch (e) { pack = null; } return !!pack; }
  function setMode(m){ vmode = m; stopVoice(); }
  function setVol(k, v){ vol[k] = v; if (!ctx) return; if (k === 'bgm') bgmG.gain.value = v; if (k === 'se') seG.gain.value = v; if (k === 'voice') voG.gain.value = v * 1.15; }
  function stopVoice(){ if (curV){ try { curV.onended = null; curV.stop(); } catch (e) {} curV = null; } if (window.speechSynthesis) try { speechSynthesis.cancel(); } catch (e) {} }
  const TTS = { tsubasa:[1.0,1.05], kohei:[0.6,0.9], onizuka:[0.5,1.0], chihaya:[1.6,1.2], yuki:[1.4,1.15], hori:[0.9,1.0] };
  function speak(who, text){ // resolves with duration in seconds (0 when there is no voice)
    stopVoice();
    return new Promise(res => {
      if (!ctx || !vol.voice || vmode === 'off') return res(0);
      const e = packIdx && packIdx[fnv(who + '|' + text)];
      if (pack && e && vmode === 'game'){
        const done = buf => { const s = ctx.createBufferSource(); s.buffer = buf; s.connect(voG); s.start(); curV = s; s.onended = () => { if (curV === s) curV = null; }; res(buf.duration); };
        try { const p = ctx.decodeAudioData(pack.slice(e[0], e[0] + e[1]), done, () => res(0)); if (p && p.catch) p.catch(() => {}); } catch (err) { res(0); }
      } else if ((!pack || vmode === 'device') && window.speechSynthesis && /[ぁ-んァ-ヶ一-龠]/.test(text)){
        try { const u = new SpeechSynthesisUtterance(text.replace(/[「」…]/g, '')); u.lang = 'ja-JP'; const t = TTS[who] || [(typeof CHARS !== 'undefined' && CHARS[who] && CHARS[who].sex === 'f') ? 1.3 : 0.8, 1]; u.pitch = t[0]; u.rate = t[1]; u.volume = vol.voice; speechSynthesis.speak(u); } catch (err) {}
        res(Math.min(9, 0.6 + text.length * 0.13));
      } else res(0);
    });
  }
  function level(){ if (!ana || !curV) return 0; ana.getByteTimeDomainData(anaBuf); let s = 0; for (let i = 0; i < anaBuf.length; i += 4){ const v = (anaBuf[i] - 128) / 128; s += v * v; } return Math.min(1, Math.sqrt(s / (anaBuf.length / 4)) * 3.2); }
  const speaking = () => !!curV || (window.speechSynthesis && speechSynthesis.speaking);
  /* --- synth voices --- */
  const hz = m => 440 * Math.pow(2, (m - 69) / 12);
  function tone(out, type, f, t, dur, g, opt = {}){
    const o = ctx.createOscillator(), a = ctx.createGain(); o.type = type; o.frequency.setValueAtTime(f, t); if (opt.to) o.frequency.exponentialRampToValueAtTime(opt.to, t + dur);
    if (opt.det) o.detune.value = opt.det;
    a.gain.setValueAtTime(0.0001, t); a.gain.linearRampToValueAtTime(g, t + (opt.att || 0.008)); a.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    let n = o; if (opt.lp){ const fl = ctx.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = opt.lp; o.connect(fl); n = fl; }
    n.connect(a); a.connect(out); o.start(t); o.stop(t + dur + 0.05);
  }
  function noise(out, t, dur, g, hp, lp){ const s = ctx.createBufferSource(); s.buffer = noiseBuf; const a = ctx.createGain(); a.gain.setValueAtTime(g, t); a.gain.exponentialRampToValueAtTime(0.0001, t + dur); let n = s; if (hp){ const f = ctx.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = hp; n.connect(f); n = f; } if (lp){ const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp; n.connect(f); n = f; } n.connect(a); a.connect(out); s.start(t, Math.random() * 0.5, dur + 0.05); }
  /* --- BGM: 16 steps per bar; chord = [root midi, intervals] --- */
  const MAJ = [0, 4, 7], MIN = [0, 3, 7], M7 = [0, 4, 7, 11], m7 = [0, 3, 7, 10], SUS = [0, 5, 7];
  const SONGS = {
    home:   { bpm: 84,  ch: [[48, MAJ], [45, MIN], [41, MAJ], [43, MAJ]], bass: 'x.......x.....x.', arp: '..0.1.2.1.0.1.2.', k: '', h: '', pad: 0.05, lead: [[0, 76, 4], [4, 74, 2], [6, 72, 6], [16, 72, 4], [22, 69, 6], [32, 69, 4], [36, 72, 4], [40, 77, 6], [48, 74, 6], [56, 71, 6]], lv: 0.07 },
    calm:   { bpm: 96,  ch: [[50, m7], [43, MAJ], [48, M7], [45, m7]], bass: 'x.....x.x.......', arp: '0.2.1.3.0.2.1.2.', k: 'x.......x.......', h: '..x...x...x...x.', pad: 0.035, lead: [[2, 77, 2], [6, 76, 2], [12, 72, 4], [18, 74, 4], [28, 71, 4], [34, 76, 2], [38, 79, 6], [50, 76, 2], [54, 72, 6]], lv: 0.05 },
    invest: { bpm: 106, ch: [[45, MIN], [41, MAJ], [38, MIN], [40, MAJ]], bass: 'x..x..x.x..x.x..', arp: '0..1..2.0..1..2.', k: 'x.....x...x.....', h: 'x.x.x.x.x.x.x.xx', s: '....x.......x...', pad: 0.03, lead: [[0, 69, 3], [3, 72, 3], [6, 76, 6], [16, 77, 3], [19, 76, 3], [22, 72, 6], [32, 74, 3], [35, 77, 3], [38, 81, 6], [48, 80, 4], [54, 76, 2], [56, 71, 6]], lv: 0.05 },
    tension:{ bpm: 118, ch: [[40, MIN], [40, MIN], [36, MAJ], [35, SUS]], bass: 'x.x.x.x.x.x.x.x.', arp: '....0.......1...', k: 'x.......x.......', h: '', pad: 0.045, lead: [[8, 76, 8], [24, 79, 8], [40, 76, 8], [56, 78, 8]], lv: 0.035 },
    battle: { bpm: 140, ch: [[38, MIN], [46, MAJ], [36, MAJ], [45, MAJ]], bass: 'x.xxx.xxx.xxx.xx', arp: '0.1.2.1.0.1.2.1.', k: 'x...x...x...x...', h: '..x...x...x...xx', s: '....x.......x...', pad: 0.03, lead: [[0, 74, 2], [2, 77, 2], [4, 81, 4], [10, 79, 2], [12, 77, 4], [16, 77, 2], [18, 74, 2], [20, 70, 6], [28, 74, 4], [32, 76, 2], [34, 79, 2], [36, 84, 4], [42, 79, 2], [44, 76, 4], [48, 73, 4], [52, 76, 4], [56, 81, 8]], lv: 0.06 },
    truth:  { bpm: 72,  ch: [[41, MAJ], [40, MIN], [38, MIN], [46, MAJ]], bass: 'x...............', arp: '0.1.2.1.3.2.1.2.', k: '', h: '', pad: 0.04, lead: [[0, 81, 6], [8, 77, 6], [16, 79, 8], [28, 76, 4], [32, 77, 6], [40, 74, 6], [48, 74, 4], [52, 77, 4], [56, 82, 8]], lv: 0.07, piano: 1 }
  };
  function sched(){
    const S = SONGS[bgmName]; if (!S || !ctx) return; const sp = 60 / S.bpm / 4;
    if (nextT < ctx.currentTime + 0.02){ const miss = Math.ceil((ctx.currentTime + 0.08 - nextT) / sp); nextT += miss * sp; step += miss; } // the page stalled: skip the missed notes instead of firing them all at once
    while (nextT < ctx.currentTime + 0.7){
      const bar = Math.floor(step / 16) % S.ch.length, st = step % 16, t = nextT, c = S.ch[bar], tones = c[1].map(i => c[0] + 12 + i);
      if (S.bass[st] === 'x') tone(bgmG, 'triangle', hz(c[0] - (c[0] > 44 ? 12 : 0)), t, sp * 2.6, 0.22, { lp: 600 });
      if (st === 0){ for (const m of tones.slice(0, 3)){ tone(bgmG, 'sawtooth', hz(m + 12), t, sp * 16.5, lite ? S.pad * 1.7 : S.pad, { att: sp * 3, lp: 900, det: -7 }); if (!lite) tone(bgmG, 'sawtooth', hz(m + 12), t, sp * 16.5, S.pad, { att: sp * 3, lp: 900, det: 7 }); } }
      const a = S.arp[st]; if (a !== '.' && a !== undefined){ const m = tones[+a % tones.length] + 12 + (+a >= tones.length ? 12 : 0); tone(bgmG, S.piano ? 'triangle' : 'sine', hz(m), t, sp * (S.piano ? 5 : 2.2), S.piano ? 0.09 : 0.06, { lp: 2400 }); if (S.piano) tone(bgmG, 'sine', hz(m + 12), t, sp * 3, 0.025); }
      if (S.k && S.k[st] === 'x') tone(bgmG, 'sine', 130, t, 0.16, 0.5, { to: 42 });
      if (S.h && S.h[st] === 'x') noise(bgmG, t, 0.035, 0.07, 7000);
      if (S.s && S.s[st] === 'x'){ noise(bgmG, t, 0.11, 0.14, 1500); tone(bgmG, 'triangle', 190, t, 0.08, 0.1); }
      const ls = step % (16 * S.ch.length); for (const n of S.lead){ if (n[0] === ls){ tone(bgmG, 'triangle', hz(n[1]), t, sp * n[2] * 1.4, S.lv, { att: 0.02, lp: 3200 }); tone(bgmG, 'sine', hz(n[1] + 12), t, sp * n[2], S.lv * 0.3); } }
      nextT += sp; step++;
    }
  }
  function bgm(name){ if (name === bgmName) return; bgmName = SONGS[name] ? name : null; clearInterval(timer); timer = null; if (!ctx || !bgmName) return; step = 0; nextT = ctx.currentTime + 0.12; timer = setInterval(sched, 100); }
  const SFX = {
    tick: t => tone(seG, 'square', 880, t, 0.03, 0.035, { lp: 3000 }),
    select: t => { tone(seG, 'triangle', 660, t, 0.07, 0.2); tone(seG, 'triangle', 990, t + 0.05, 0.09, 0.18); },
    back: t => tone(seG, 'triangle', 420, t, 0.1, 0.18, { to: 300 }),
    get: t => [72, 76, 79, 84].forEach((m, i) => tone(seG, 'triangle', hz(m), t + i * 0.07, 0.25, 0.2)),
    correct: t => { [76, 81, 88].forEach((m, i) => tone(seG, 'square', hz(m), t + i * 0.06, 0.2, 0.09, { lp: 4000 })); noise(seG, t, 0.25, 0.12, 3000); },
    wrong: t => { tone(seG, 'sawtooth', 150, t, 0.3, 0.2, { to: 90, lp: 800 }); tone(seG, 'sawtooth', 157, t, 0.3, 0.2, { to: 94, lp: 800 }); },
    damage: t => { noise(seG, t, 0.3, 0.4, 0, 1800); tone(seG, 'sine', 200, t, 0.3, 0.4, { to: 50 }); },
    shock: t => { [50, 56, 62, 69].forEach(m => tone(seG, 'sawtooth', hz(m), t, 0.9, 0.09, { lp: 2000 })); noise(seG, t, 0.2, 0.25, 800); },
    door: t => { noise(seG, t, 0.35, 0.2, 200, 1400); tone(seG, 'sine', 90, t + 0.3, 0.12, 0.35, { to: 60 }); },
    thud: t => { tone(seG, 'sine', 120, t, 0.2, 0.5, { to: 45 }); noise(seG, t, 0.08, 0.2, 0, 900); },
    phone: t => { for (let i = 0; i < 6; i++){ tone(seG, 'sine', 1400, t + i * 0.09, 0.05, 0.14); tone(seG, 'sine', 1750, t + i * 0.09 + 0.04, 0.05, 0.14); } },
    cuff: t => { [0, 0.06, 0.12, 0.2].forEach((d, i) => { tone(seG, 'square', 2400 + i * 300, t + d, 0.03, 0.12); noise(seG, t + d, 0.03, 0.2, 5000); }); tone(seG, 'triangle', 500, t + 0.24, 0.25, 0.2); },
    card: t => noise(seG, t, 0.3, 0.14, 1200, 5000),
    wall: t => { noise(seG, t, 0.5, 0.4, 300, 3000); tone(seG, 'sine', 300, t, 0.4, 0.3, { to: 60 }); [84, 91].forEach((m, i) => tone(seG, 'triangle', hz(m), t + 0.05 + i * 0.05, 0.3, 0.12)); },
    cutin: t => { noise(seG, t, 0.25, 0.2, 2000); tone(seG, 'sawtooth', 300, t, 0.25, 0.14, { to: 1200, lp: 3000 }); }
  };
  let lastTick = 0;
  function sfx(n){ if (!ctx || !SFX[n]) return; if (n === 'tick'){ if (lite || ctx.currentTime - lastTick < 0.09) return; lastTick = ctx.currentTime; } try { SFX[n](ctx.currentTime + 0.005); } catch (e) {} }
  let lite = false;
  return { setLite(v){ lite = !!v; }, init, loadPack, setMode, get mode(){ return vmode; }, speak, stopVoice, level, speaking, bgm, sfx, setVol, vol, get hasPack(){ return !!pack && vmode === 'game'; }, get ok(){ return !!ctx; } };
})();
