/* ---------- sound: voice packs, rain and room tone, engine, footsteps, sparse music ---------- */
const AudioSys = (() => {
  let ctx = null, master, ambG, seG, voG, bgmG, noiseBuf, curV = null, packs = {}, loading = {}, index = null, amb = null, ambNodes = [], eng = null, bgmName = null, bgmTimer = 0, nextT = 0, step = 0, lite = false, dripT = 0;
  const vol = { voice: 1, bgm: .5, se: .7 };
  const fnv = s => { let h = 0x811c9dc5; const b = new TextEncoder().encode(s); for (const x of b){ h ^= x; h = Math.imul(h, 0x01000193) >>> 0; } return h.toString(16).padStart(8, '0'); };
  function init(){ if (ctx){ if (ctx.state === 'suspended') ctx.resume(); return; }
    const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return; try { ctx = new AC({ latencyHint: 'playback' }); } catch (e) { ctx = new AC(); }
    master = ctx.createGain(); master.gain.value = .9; try { const lim = ctx.createDynamicsCompressor(); lim.threshold.value = -8; lim.ratio.value = 10; master.connect(lim); lim.connect(ctx.destination); } catch (e) { master.connect(ctx.destination); }
    ambG = ctx.createGain(); ambG.gain.value = vol.se * .8; ambG.connect(master); seG = ctx.createGain(); seG.gain.value = vol.se; seG.connect(master); voG = ctx.createGain(); voG.gain.value = vol.voice * 1.2; voG.connect(master); bgmG = ctx.createGain(); bgmG.gain.value = vol.bgm; bgmG.connect(master);
    noiseBuf = ctx.createBuffer(1, ctx.sampleRate * 2, ctx.sampleRate); const d = noiseBuf.getChannelData(0); let b0 = 0; for (let i = 0; i < d.length; i++){ const w = Math.random() * 2 - 1; b0 = b0 * .6 + w * .4; d[i] = w * .6 + b0 * .4; }
    if (amb) setAmb(amb, true); if (bgmName){ const n = bgmName; bgmName = null; bgm(n); } }
  function setVol(k, v){ vol[k] = v; if (!ctx) return; if (k === 'voice') voG.gain.value = v * 1.2; if (k === 'bgm') bgmG.gain.value = v; if (k === 'se'){ seG.gain.value = v; ambG.gain.value = v * .8; } }
  /* voice */
  function setIndex(ix){ index = ix; }
  async function loadPack(p){ if (packs[p] || loading[p]) return loading[p]; loading[p] = (async () => { try { const r = await fetch('v/' + p + '.mp3'); if (!r.ok) throw 0; packs[p] = await r.arrayBuffer(); } catch (e) { packs[p] = null; } })(); return loading[p]; }
  function stopVoice(){ if (curV){ try { curV.onended = null; curV.stop(); } catch (e) {} curV = null; } }
  function speak(who, text){ stopVoice(); return new Promise(async res => { if (!ctx || !vol.voice || !index) return res(0); const e = index[fnv(who + '|' + text)]; if (!e) return res(0); if (packs[e[0]] === undefined) await loadPack(e[0]); const pk = packs[e[0]]; if (!pk) return res(0);
      try { const done = buf => { stopVoice(); const s = ctx.createBufferSource(); s.buffer = buf; s.connect(voG); s.start(); curV = s; s.onended = () => { if (curV === s) curV = null; }; res(buf.duration); }; const p = ctx.decodeAudioData(pk.slice(e[1], e[1] + e[2]), done, () => res(0)); if (p && p.catch) p.catch(() => {}); } catch (err) { res(0); } }); }
  const speaking = () => !!curV;
  /* one-shot sounds */
  function tone(out, type, f, t, dur, g, o = {}){ const os = ctx.createOscillator(), a = ctx.createGain(); os.type = type; os.frequency.setValueAtTime(f, t); if (o.to) os.frequency.exponentialRampToValueAtTime(o.to, t + dur); a.gain.setValueAtTime(.0001, t); a.gain.linearRampToValueAtTime(g, t + (o.att || .01)); a.gain.exponentialRampToValueAtTime(.0001, t + dur); let n = os; if (o.lp){ const fl = ctx.createBiquadFilter(); fl.type = 'lowpass'; fl.frequency.value = o.lp; os.connect(fl); n = fl; } n.connect(a); a.connect(out); os.start(t); os.stop(t + dur + .05); }
  function noise(out, t, dur, g, hp, lp){ const s = ctx.createBufferSource(); s.buffer = noiseBuf; const a = ctx.createGain(); a.gain.setValueAtTime(g, t); a.gain.exponentialRampToValueAtTime(.0001, t + dur); let n = s; if (hp){ const f = ctx.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = hp; n.connect(f); n = f; } if (lp){ const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp; n.connect(f); n = f; } n.connect(a); a.connect(out); s.start(t, Math.random(), dur + .05); }
  const hz = m => 440 * Math.pow(2, (m - 69) / 12);
  const SFX = {
    tick: t => tone(seG, 'triangle', 760, t, .04, .08), select: t => { tone(seG, 'triangle', 620, t, .08, .16); tone(seG, 'triangle', 930, t + .06, .1, .14); }, back: t => tone(seG, 'triangle', 420, t, .1, .14, { to: 300 }),
    get: t => [72, 76, 79, 84].forEach((m, i) => tone(seG, 'triangle', hz(m), t + i * .07, .28, .16)), fact: t => [79, 86].forEach((m, i) => tone(seG, 'sine', hz(m), t + i * .08, .3, .16)),
    right: t => { [69, 76, 81, 88].forEach((m, i) => tone(seG, 'triangle', hz(m), t + i * .06, .4, .14)); noise(seG, t, .3, .1, 3000); }, wrong: t => { tone(seG, 'sawtooth', 150, t, .32, .16, { to: 92, lp: 700 }); tone(seG, 'sawtooth', 157, t, .32, .16, { to: 96, lp: 700 }); },
    link: t => { [62, 69, 74, 81, 86].forEach((m, i) => tone(seG, 'sine', hz(m), t + i * .09, .7, .14)); }, door: t => { noise(seG, t, .3, .2, 200, 1300); tone(seG, 'sine', 90, t + .26, .12, .3, { to: 60 }); }, cardoor: t => { noise(seG, t, .12, .3, 100, 900); tone(seG, 'sine', 110, t, .14, .4, { to: 55 }); },
    thud: t => { tone(seG, 'sine', 120, t, .22, .5, { to: 45 }); noise(seG, t, .08, .2, 0, 900); }, steam: t => { noise(seG, t, 2.2, .5, 2500); noise(seG, t + .2, 2, .3, 800, 4000); }, rumble: t => { noise(seG, t, 3, .6, 0, 300); tone(seG, 'sine', 50, t, 2.6, .5, { to: 30 }); }, rain: t => noise(seG, t, 1.6, .25, 1500),
    travel: t => { tone(seG, 'sine', 55, t, 3.2, .4, { to: 110, att: 1.2 }); tone(seG, 'sine', 82.5, t, 3.2, .25, { to: 165, att: 1.5 }); noise(seG, t, 3, .12, 300, 1200); }, step: t => { noise(seG, t, .07, .09, 300, 1800); tone(seG, 'sine', 90, t, .06, .08, { to: 60 }); }, stepw: t => { noise(seG, t, .1, .1, 900, 5000); noise(seG, t, .06, .08, 200, 900); },
  };
  let lastTick = 0; function sfx(n){ if (!ctx || !SFX[n]) return; if (n === 'tick'){ if (ctx.currentTime - lastTick < .08) return; lastTick = ctx.currentTime; } try { SFX[n](ctx.currentTime + .005); } catch (e) {} }
  /* ambience: looped filtered noise layers */
  function layer(hp, lp, g){ const s = ctx.createBufferSource(); s.buffer = noiseBuf; s.loop = true; const a = ctx.createGain(); a.gain.value = 0; a.gain.linearRampToValueAtTime(g, ctx.currentTime + 1.2); let n = s; if (hp){ const f = ctx.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = hp; n.connect(f); n = f; } if (lp){ const f = ctx.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = lp; n.connect(f); n = f; } n.connect(a); a.connect(ambG); s.start(0, Math.random()); return { s, a }; }
  function setAmb(name, force){ if (name === amb && !force) return; amb = name; if (!ctx) return; for (const L of ambNodes){ try { L.a.gain.cancelScheduledValues(ctx.currentTime); L.a.gain.setValueAtTime(L.a.gain.value, ctx.currentTime); L.a.gain.linearRampToValueAtTime(0, ctx.currentTime + .8); L.s.stop(ctx.currentTime + .9); } catch (e) {} } ambNodes = [];
    if (name === 'forest') ambNodes = [layer(1800, 9000, .22), layer(200, 900, .1)]; else if (name === 'town') ambNodes = [layer(2200, 9000, .17), layer(300, 900, .05)]; else if (name === 'room') ambNodes = [layer(500, 1600, .06)]; else if (name === 'cave') ambNodes = [layer(60, 260, .16)]; else if (name === 'car') ambNodes = [layer(1500, 6000, .16), layer(100, 500, .07)]; }
  function tickAmb(){ if (!ctx || amb !== 'cave') return; const t = ctx.currentTime; if (t > dripT){ dripT = t + 1.2 + Math.random() * 3; const f = 900 + Math.random() * 900; tone(ambG, 'sine', f, t, .25, .12, { to: f * 1.5 }); tone(ambG, 'sine', f * .5, t + .09, .3, .05); } }
  /* engine: two detuned saws through a low-pass; pitch follows speed */
  function engine(on, speed){ if (!ctx) return; if (!on){ if (eng){ try { eng.g.gain.linearRampToValueAtTime(0, ctx.currentTime + .4); eng.o1.stop(ctx.currentTime + .5); eng.o2.stop(ctx.currentTime + .5); } catch (e) {} eng = null; } return; }
    if (!eng){ const o1 = ctx.createOscillator(), o2 = ctx.createOscillator(), f = ctx.createBiquadFilter(), g = ctx.createGain(); o1.type = 'sawtooth'; o2.type = 'square'; f.type = 'lowpass'; f.frequency.value = 260; g.gain.value = 0; o1.connect(f); o2.connect(f); f.connect(g); g.connect(ambG); o1.start(); o2.start(); eng = { o1, o2, f, g }; }
    const k = Math.min(1, speed / 1900), t = ctx.currentTime; eng.o1.frequency.setTargetAtTime(38 + k * 46, t, .2); eng.o2.frequency.setTargetAtTime(19.2 + k * 23.4, t, .2); eng.f.frequency.setTargetAtTime(180 + k * 420, t, .3); eng.g.gain.setTargetAtTime(.09 + k * .07, t, .3); }
  /* music: slow, sparse. chords as midi roots; a few bell notes */
  const SONGS = { calm: { bpm: 54, ch: [[45, [0, 7, 12, 15]], [41, [0, 7, 12, 16]], [48, [0, 7, 12, 16]], [43, [0, 7, 14, 17]]], mel: [[0, 72], [6, 76], [16, 79], [22, 76], [32, 76], [38, 72], [48, 74], [56, 71]], pad: .05, bell: .09 },
    dark: { bpm: 46, ch: [[38, [0, 7, 15]], [38, [0, 7, 14]], [34, [0, 7, 16]], [36, [0, 7, 14]]], mel: [[4, 74], [20, 77], [36, 73], [52, 69]], pad: .06, bell: .06 },
    tense: { bpm: 76, ch: [[40, [0, 7, 15]], [40, [0, 7, 15]], [36, [0, 7, 16]], [35, [0, 7, 14]]], mel: [[0, 76], [8, 79], [16, 76], [24, 83], [32, 76], [40, 79], [48, 74], [56, 71]], pad: .045, bell: .07, pulse: 1 },
    truth: { bpm: 60, ch: [[41, [0, 7, 12, 16]], [43, [0, 7, 12, 16]], [45, [0, 7, 12, 15]], [45, [0, 7, 12, 15]]], mel: [[0, 81], [4, 84], [8, 88], [16, 86], [24, 83], [32, 84], [36, 81], [40, 76], [48, 79], [56, 77]], pad: .06, bell: .11 } };
  function sched(){ const S = SONGS[bgmName]; if (!S || !ctx) return; const sp = 60 / S.bpm / 4; if (nextT < ctx.currentTime + .02){ const m = Math.ceil((ctx.currentTime + .08 - nextT) / sp); nextT += m * sp; step += m; }
    while (nextT < ctx.currentTime + .8){ const bar = Math.floor(step / 16) % S.ch.length, st = step % 16, t = nextT, c = S.ch[bar];
      if (st === 0) for (const iv of c[1]){ tone(bgmG, 'sawtooth', hz(c[0] + 12 + iv), t, sp * 17, S.pad, { att: sp * 5, lp: 700 }); } if (st === 0) tone(bgmG, 'sine', hz(c[0]), t, sp * 14, .16, { att: .1 });
      if (S.pulse && st % 4 === 0) tone(bgmG, 'triangle', hz(c[0] + 12), t, sp * 1.6, .1, { lp: 500 });
      const ls = step % 64; for (const n of S.mel) if (n[0] === ls){ tone(bgmG, 'sine', hz(n[1]), t, sp * 9, S.bell, { att: .01 }); tone(bgmG, 'sine', hz(n[1] + 12), t, sp * 5, S.bell * .25); }
      nextT += sp; step++; } }
  function bgm(name){ if (name === bgmName) return; bgmName = SONGS[name] ? name : null; clearInterval(bgmTimer); bgmTimer = 0; if (!ctx || !bgmName) return; step = 0; nextT = ctx.currentTime + .15; bgmTimer = setInterval(sched, 120); }
  return { init, setVol, vol, setIndex, loadPack, speak, stopVoice, speaking, sfx, setAmb, tickAmb, engine, bgm, setLite(v){ lite = !!v; }, get ok(){ return !!ctx; }, fnv };
})();
