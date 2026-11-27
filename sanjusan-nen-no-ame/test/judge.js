// node test/judge.js : typed answers. Spelling variants and small typos pass; wrong or scattershot answers do not.
const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(), p = await b.newPage(); await p.goto(`http://127.0.0.1:${process.env.PORT || 8770}/index.html`); await p.waitForFunction(() => window.__g, null, { timeout: 30000 }); let fails = 0;
  const T = [ // battle, round, text, expected
    ['F', 0, '遺体の下の土は乾いていた。雨は21時40分から', true], ['F', 0, 'したのつちが かわいていた。あめは 21:40 から', true], ['F', 0, '地面が濡れていなかった。雨の降り始めは２１時４０分', true], ['F', 0, '土が乾いてた、雨', true], ['F', 0, '時計が壊れていた', false], ['F', 0, '匡は自殺した', false],
    ['F', 1, 'リューズが引き出されている。偽装だ', true], ['F', 1, '竜頭をわざと', true], ['F', 1, 'りゅーずで、時計の針をすすめた', true], ['F', 1, '時計は止まっていた', false],
    ['F', 2, '20時52分に出て21時38分に戻った', true], ['F', 2, '門のカメラに車が映っている', true], ['F', 2, '20:52 と 21:38', true], ['F', 2, '21時45分に会議', false],
    ['F', 3, 'つえの跡と、たかの頭', true], ['F', 3, '杖。くちばしの形の傷', true], ['F', 3, '凶器はバルブ', false],
    ['F', 4, '1993年の排水坑の事故を隠した', true], ['F', 4, '平成5年に事故をもみ消した', true], ['F', 4, '箱を盗むため', false],
    ['F', 5, '朽木匡は汐見蓮と同一人物', true], ['F', 5, 'しおみれんが33年前へ行った', true], ['F', 5, '汐見蓮が未来から来た', true], ['F', 5, '匡は汐見修の兄弟', false],
    ['F', 6, '無縁仏はあなた、鷹取征二。足のプレートの番号が同じ', true], ['F', 6, '白骨は鷹取征二本人。KT-2021-0387', true], ['F', 6, '老人は当主自身で金属の板が同じ', true], ['F', 6, '無縁仏は朽木匡', false], ['F', 6, '鷹取征二はプレート', false],
    ['B3', 0, '汐見蓮', true], ['B3', 0, 'しおみ れん', true], ['B3', 0, '汐見 蓮です', true], ['B3', 0, '朽木匡', false], ['B3', 0, '汐見蓮と朽木匡と汐見修', false], ['B3', 0, '汐見修', false],
    ['B3', 1, '平成5年11月9日に子どもの三雲朔をかばった', true], ['B3', 1, '1993年、子供のころの私を', true], ['B3', 1, '1960年に灯を', false],
    ['B3', 2, '1999年', true], ['B3', 2, '平成11年', true], ['B3', 2, '1993年', false], ['B3', 2, '1960年か1999年か1993年', false],
    ['B1', 0, '蓮の車は登山口にある', true], ['B1', 0, '出張は7日の朝に書き足された', true], ['B1', 0, '出張はうそ', false],
    ['B2', 1, 'やけどは三日月の形で、バルブのハンドル', true], ['B2', 1, 'ボイラーではない', false] ];
  for (const [bt, r, text, want] of T){ const got = await p.evaluate(([bt, r, text]) => __g.judgeText(text, BATTLE[bt].r[r]).ok, [bt, r, text]); if (got !== want){ fails++; console.log('FAIL', bt, r + 1, JSON.stringify(text), 'got', got, 'want', want, await p.evaluate(t => [...__g.conceptsIn(t)].join(','), text)); } }
  // every chip at once must never pass; random handfuls of chips almost never pass
  const shot = await p.evaluate(() => { const all = Object.values(WORDS).flatMap(g => Object.values(g).map(v => v[0])).join(''); let pass = 0, rounds = 0; for (const b in BATTLE) for (const R of BATTLE[b].r){ rounds++; if (__g.judgeText(all, R).ok) pass++; } let rnd = 0, tries = 0; const chips = Object.values(WORDS).flatMap(g => Object.values(g).map(v => v[0])); let s = 12345; const rr = () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; };
    for (let i = 0; i < 4000; i++){ const k = 2 + Math.floor(rr() * 3), t = Array.from({ length: k }, () => chips[Math.floor(rr() * chips.length)]).join(''); const R = BATTLE.F.r[Math.floor(rr() * 7)]; tries++; if (__g.judgeText(t, R).ok) rnd++; } return { pass, rounds, rnd, tries, chips: chips.length }; });
  console.log('all chips at once passes', shot.pass, 'of', shot.rounds, 'rounds | random 2-4 chips pass', shot.rnd, 'of', shot.tries, '| chips', shot.chips); if (shot.pass) fails++;
  console.log('cases', T.length, 'fails', fails); await b.close(); process.exit(fails ? 1 : 0); })();
