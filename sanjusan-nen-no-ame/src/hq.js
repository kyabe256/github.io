/* ---------- 三十三年目の雨: the investigation headquarters, the crime lab, warrants ---------- */
/* Saku is the chief of the First Investigation Division. In 2026 he has people to command, a lab that returns numbers and not names, and a judge who signs nothing without grounds. In 1993 and 1960 he has none of them. */
Object.assign(CAST, {
  doji:   { name: '堂島 剛', role: '強行犯係長 警部', sex: 'm', age: 52, hs: 'buzz', grey: .4, brow: 1.25, jaw: .8, beard: 'stubble', hair: '#2a2a2e', eye: '#4a3a2e', cloth: { t: 'suit', c: '#4a4f58', tie: '#5a2f38' } },
  makabe: { name: '真壁 葵', role: '強行犯係 巡査部長', sex: 'f', age: 29, hs: 'bob', hair: '#2e2630', eye: '#6a4a3a', cloth: { t: 'suit', c: '#3d4a5e', tie: '#8a9aa0' } },
  okono:  { name: '小此木 松江', role: '霧渕署 刑事課', sex: 'f', age: 48, hs: 'shortf', grey: .18, hair: '#3a2e2a', eye: '#7a5a3a', cloth: { t: 'coat', c: '#7a6a55', tie: '#6a4a3a' } },
  himuro: { name: '氷室 澄', role: '科捜研 法医・化学', sex: 'f', age: 44, hs: 'tied', glasses: 'round', es: .92, hair: '#26222a', eye: '#4d6a78', cloth: { t: 'labcoat', tie: '#5a6a8a' } },
  tate:   { name: '楯岡 惣一', role: '科捜研 物理・文書', sex: 'm', age: 58, hs: 'thin', grey: .7, glasses: 'round', beard: 'mustache', hair: '#3a3430', eye: '#5a4a3a', cloth: { t: 'labcoat', tie: '#6a5a3a' } },
  kuze:   { name: '久世 航', role: '科捜研 情報', sex: 'm', age: 31, hs: 'messy', hair: '#2a2630', eye: '#3f5a6a', cloth: { t: 'knit', c: '#55607a' } },
});
CAST.saku.role = '県警 捜査一課長'; CAST.akari.role = '県警 鑑識課';
Object.assign(FACE, { doji: 'doji', makabe: 'makabe', okono: 'okono', himuro: 'himuro', tate: 'tate', kuze: 'kuze' });
/* the lab is in the prefectural capital: one more road out of town, only in 2026 */
NODES.lab = { n: '県警本部 科捜研', scene: 'lab', at: 'out', map: [84, 186], eras: [2026] };
EDGES['town-lab'] = { a: 'town', b: 'lab', len: 100, kind: 'town', n: '県道（県都へ）', curve: [[14, 34, -1.8], [52, 78, 2.2]], hill: [[30, 70, -12]] };
CARS[2026] = '課長の車'; PLACE.lab = '県警本部　科学捜査研究所'; PLACE.police[2026] = '霧渕署　特別捜査本部';
OBJ.police = OBJ.police.filter(o => o.id !== 'pc2').concat([{ id: 'war', x: 'war', l: '令状を請求する', k: 'warrant', e: [2026], if: 'hq' }, { id: 'mtg', x: 'mtg', l: '捜査会議を開く', k: 'meet', e: [2026], if: 'hq' }]);
OBJ.lab = [{ id: 'out', x: 'out', l: '科捜研を出て車に乗る', k: 'car', node: 'lab' }, { id: 'gcms', x: 'gcms', l: '分析の機械を見る', k: 'look', b: 'lab_gcms' }, { id: 'scope', x: 'scope', l: '比較顕微鏡を見る', k: 'look', b: 'lab_scope' }, { id: 'server', x: 'server', l: '解析の画面を見る', k: 'look', b: 'lab_server' }];
{ const m = OBJ.mansion; m.find(o => o.id === 'mon').if = 'gate_ok|ev:e_gate'; m.find(o => o.id === 'monx').if = '!gate_ok&!w3&!ev:e_gate';
  m.push({ id: 'monw', x: 'monitor', l: '門の録画を差し押さえる', k: 'look', b: 'm26_seize', e: [2026], if: 'w3&!gate_ok&!ev:e_gate&!p4' }, { id: 'monw2', x: 'monitor', l: '門の録画を差し押さえる', k: 'look', b: 'm26_monitor_w', e: [2026], if: 'w3&!gate_ok&!ev:e_gate&p4' }); }
NPC.push({ id: 'doji', q: 'hq', s: 'police', e: 2026, x: 1090, if: 'hq', t: [], cmd: 1 }, { id: 'himuro', s: 'lab', e: 2026, x: 700, t: [], lab: 'himuro' }, { id: 'tate', s: 'lab', e: 2026, x: 1340, t: [], lab: 'tate' }, { id: 'kuze', s: 'lab', e: 2026, x: 1980, t: [], lab: 'kuze' });
TRIG.push({ s: 'police', e: 2026, x: 300, b: 'hq_first', if: '!hq', met: ['doji'] }, { s: 'lab', e: 2026, x: 300, b: 'lab_first', if: '!lab', met: ['himuro', 'tate', 'kuze'] });
/* reports: they arrive later, and they give numbers. Reading them is the chief's work. */
DOCS.e_dna = ['DNA型鑑定書', '県警 科捜研 法医。', [['遺体 と 汐見蓮の歯ブラシ', 'STR型の21座位が、全て一致。別人で一致する確率は、4.7×10の21乗分の1。同一人物。', 'f_dna_same'], ['遺体 と 汐見修', '全ての座位で、型の片方を共有。親子である確率 99.9998％。汐見修が、親。', 'f_dna_parent'], ['遺体 と 朽木灯', '親子である確率 99.9997％。遺体が、親。', null], ['年齢', '骨と歯から、遺体は60歳前後。汐見修は71歳。汐見蓮は27歳。', null], ['担当者の注', '試料の取り違えを疑い、別の日に、別の者がやり直した。結果は同じ。', null]]];
DOCS.e_dna2 = ['DNA型鑑定書（追加）', '県警 科捜研 法医。11月11日。', [['遺体 と 三雲朔', 'おじと、おいの間柄である確率 99.2％。', 'f_dna_uncle'], ['三雲朔 と 汐見修', '21座位が、全て一致。同一人物、または一卵性の双子。', 'f_twin_dna'], ['担当者の注', '捜査員の試料は、まぎれこみを除くための対照として、全員ぶんを調べる。年齢は、38と71。', null]]];
Object.assign(DOCS, {
  e_autopsy: ['司法解剖の所見', '県立医大 法医学教室。科捜研 氷室がまとめた。', [['死因', '右のこめかみを打たれた事による、脳挫傷。頭の骨が、弧の形にへこんでいる。打撃は1回。', null], ['創の形', '弧の長さ18ミリ、幅4ミリ、深さ9ミリ。先の曲がった、金属の突起。', 'f_aut_wound'], ['胃の中身', '米と、きのこ。消化は、始まったばかり。食後、およそ1時間。', null], ['死亡の時刻', '夕食は19時50分（妻の話）。死亡は、6日の20時45分から21時15分の間。', 'f_aut_time'], ['直腸の温度と死斑', '温度だけなら、20時半から22時半。死斑は背中。遺体は、動かされていない。', null], ['薬と毒', 'アルコール、睡眠薬、ともに検出されない。', null], ['爪', '右手の爪の間に、濃紺の毛の繊維が2本。', 'f_aut_fiber']]],
  e_relay: ['リレー捜査の報告', '強行犯係 真壁。11月6日の夜。', [['20:33　朽木屋の前（商店のカメラ）', '白い車に、朽木匡が乗る。運転は、汐見蓮。', null], ['20:37　Nシステム 霧渕南', '白い車が、森の方へ通る。', null], ['20:41　登山口', '白い車が着く。ドライブレコーダーと合う。', null], ['20:59　森の分かれ道（県の道路カメラ）', '黒いセダンが、登山口の方へ曲がる。21時32分、逆の向きに通る。映像は荒く、ナンバーは読めない。', 'f_car2'], ['Nシステム', '20時から22時に、霧渕南を通った車は、白い車の1台だけ。黒いセダンは、通っていない。', 'f_car2']]],
  e_owner: ['車の照会の報告', '強行犯係 真壁。', [['条件', '黒の大型セダン。ナンバーの下2桁が「87」。県内の登録は、2台。', null], ['1台目', '県都の会社の車。6日の夜は、車庫のカメラに映っている。', null], ['2台目', '鷹取征二の名義。車庫は、鷹取の屋敷。', 'f_owner']]],
  e_alibi: ['アリバイの裏付けの報告', '強行犯係 堂島。', [['会議の接続の記録', '鷹取征二　21時44分51秒　入室。22時31分　退室。', 'f_alibi_gap'], ['家政婦', '6日は、18時に帰った。夜の屋敷には、当主だけ。', 'f_alibi_gap'], ['鷹取玲', '6日の夜は、発電所の所長室から会議に出た。屋敷には、いなかった。父を、見ていない。', null]]],
  e_phone: ['通話の履歴', '差押許可状による。電話会社。', [['11月5日 21:12', '鷹取の屋敷の電話 → 朽木屋。4分10秒。', 'f_calls'], ['11月6日 19:05', '朽木屋 → 汐見蓮の携帯。1分。', null], ['11月6日 20:47', '汐見蓮の携帯。登山口の基地局を最後に、圏外。電源は、切られていない。そのまま、きょうまで圏外。', 'f_ren_cell']]],
  e_jidori: ['地取りの報告', '霧渕署 小此木。', [['11月4日 6:10', '登山口のカメラ。朽木匡が、1人で森へ入る。手に、箱。', 'f_trail45'], ['11月5日 19:20', '同じカメラ。朽木匡が、森から出る。古い作業着。手ぶら。', 'f_trail45'], ['森の中', '2日の間、森のどこにいたかは、分からない。小屋も、たき火の跡も、無い。', null]]],
  e_lab_coal: ['鑑定書　靴底の石炭がら', '科捜研 化学。蛍光X線、顕微鏡。', [['成分', '瀝青炭の燃えがら。硫黄 2.1％、灰分 14％。', null], ['産地', '成分の比は、北沢炭鉱の石炭に合う。北沢炭鉱は、1987年に閉山。', 'f_lab_coal'], ['付き方', '粒の角が立っている。踏んでから、数日以内。', 'f_lab_coal']]],
  e_lab_lime: ['鑑定書　すその白い粉', '科捜研 化学。X線回折。', [['成分', '方解石 97％。石英が、少し。', null], ['対照', '鑑識が雨穴で採った岩の粉と比べた。入口から40メートル奥の岩と、一致。入口の岩とは、合わない。', 'f_lab_lime']]],
  e_lab_cane: ['鑑定書　杖のしみ', '科捜研 法医。', [['予備試験', 'くちばしの黒いしみ。ルミノール陽性。ヒトの血。', null], ['DNA型', '21座位が、遺体と一致。', 'f_lab_cane'], ['指紋', '水に2日つかっていた。握りからは、出ない。', null], ['注', '血は、くちばしの内側の溝に残っていた。洗っても、落ちにくい所。', null]]],
  e_lab_fiber: ['鑑定書　爪の間の繊維', '科捜研 化学。顕微分光、赤外分光。', [['繊維', 'カシミヤ70％、羊毛30％。濃紺。', null], ['対照', '遺体の服、朽木屋の衣類に、同じ物は無い。', 'f_lab_fiber'], ['注', '高価なコート地。誰の服かは、比べる服が無いと言えない。', null]]],
  e_lab_cloth: ['鑑定書　作業着の布', '科捜研 化学。', [['繊維', '綿100％の綾織り。', null], ['染料', '硫化染料。いまは、ほとんど使われない。蛍光増白剤は、無い。', null], ['炭素14', '綿が育ったのは、1958年から60年。核実験のなごりの濃さから。', 'f_lab_cloth'], ['強さ', '引っぱり強さは、新品と同じ。66年たった綿なら、半分以下になる。', 'f_lab_cloth'], ['担当者の注', '材料は66年前。なのに、布は、去年おろしたように新しい。説明は、つかない。', null]]],
  e_lab_tool: ['鑑定書　創と杖', '科捜研 物理。', [['比べた物', '解剖の創の型と、杖の頭。', null], ['くちばし', '弧の長さ18.2ミリ、幅4.1ミリ。創と、重なる。', 'f_lab_tool'], ['石突き', '径22.0ミリ。遺体のそばの丸い跡と、同じ。', 'f_lab_tool'], ['結論', 'この杖か、同じ型の杖でできた創と考えて、矛盾しない。', null]]],
  e_lab_watch: ['鑑定書　腕時計', '科捜研 物理。', [['風防', '割れは、外からの1回の打撃。', null], ['機械', '歯車にも、てんぷにも、打たれた傷が無い。', 'f_lab_watch'], ['りゅうず', '2段引き。針を合わせる位置。この位置では、機械は止まる。', 'f_lab_watch'], ['日付', '日付の窓は「6」。針を進めても、0時をまたがなければ、変わらない。', null], ['結論', '時計は、打たれて止まったのではない。止めて、針を合わせてから、割られた。', null]]],
  e_lab_paper: ['鑑定書　百円札と整理券', '科捜研 文書。', [['百円札', '本物。板垣退助のB号券。昭和28年から49年に発行。', null], ['札の紙', '折り目、手の脂、酸化が、ほとんど無い。銀行から出たばかりの状態。', 'f_lab_paper'], ['整理券', '霧渕交通の物。「5.11.5」は、平成5年11月5日。この型の券は、平成9年に廃止。', null], ['券の紙', '黄ばみが無い。33年前の紙には、見えない。', 'f_lab_paper'], ['担当者の注', 'にせ物なら、もっと古く見せる。', null]]],
  e_lab_hand: ['鑑定書　宿帳の字', '科捜研 文書。昭和35年の宿帳。', [['「三雲 朔」の字', '課長の署名と比べた。15の特徴のうち、14が合う。同じ人の字と、考えられる。', 'f_lab_hand'], ['インク', 'ブルーブラック。酸化の進み方は、60年以上。', 'f_lab_hand'], ['「汐見 蓮」の字', '朽木匡の帳簿の字と、13の特徴が合う。', 'f_lab_hand_ren'], ['担当者の注', '60年前のインクで、38歳の人の字。わしには、説明がつかん。', null]]],
  e_lab_gait: ['解析書　2人の歩き方', '科捜研 情報。ドライブレコーダー 20:48 の6秒。', [['身長', '左の男 177センチ前後。右の男 175センチ前後。', null], ['歩容', '歩幅、腕のふり、左肩の下がり方。2人の似かたは、0.93。', 'f_lab_gait'], ['目安', '他人どうしは、0.3以下。親子でも、0.6をこえない。', 'f_lab_gait'], ['担当者の注', '同じ人を、2度写した時の数に近い。', null]]],
  e_plate: ['解析書　道路カメラの車', '科捜研 情報。森の分かれ道 20:59。', [['手法', '続いた38コマを重ねて、ぶれを取りのぞいた。', null], ['ナンバー', '4桁のうち、下2桁は「87」。上2桁は、読めない。', 'f_plate87'], ['車', '黒の大型セダン。', 'f_plate87'], ['担当者の注', '持ち主は、ここでは分からない。登録の照会は、捜査の仕事。', null]]],
  e_lab_soil: ['鑑定書　遺体の下の土', '科捜研 化学。含水率。', [['遺体の下', '含水率 8％。', 'f_lab_soil'], ['遺体から1メートルの所', '含水率 31％。', 'f_lab_soil'], ['担当者の注', '雨は、遺体の上に降った。遺体は、降り始めより前から、そこにあった。何分前かは、土からは言えない。', null]]],
  e_lab_log: ['解析書　入退構の記録', '科捜研 情報。発電所の守衛所の記録。', [['「出張」の行', '作られたのは、11月7日 8時30分12秒。入力は、所長室の端末。', 'f_lab_log'], ['もとの行', '11月6日 18時02分の退構。書きかえも、消した跡も、無い。', 'f_lab_log'], ['担当者の注', '消したのではなく、あとから1行、足している。隠すつもりの人のやり方ではない。', null]]],
  e_lab_gate: ['解析書　門の録画', '科捜研 情報。', [['真正', '書きかえの跡は、無い。記録の時刻は、標準時と2秒の差。', 'f_lab_gate'], ['運転者', '顔の照合。鷹取征二と、0.91。', null], ['20:52', '助手席に、杖。頭は、鳥の形。', 'f_lab_gate'], ['21:38', '助手席は、空。杖は、車内のどこにも写らない。', 'f_lab_gate'], ['車体', '戻った車は、ぬれていない。雨は、21時40分から。', null]]],
});
Object.assign(FACTS, {
  f_aut_wound: ['創は、弧の長さ18ミリ、幅4ミリ。先の曲がった金属', '司法解剖。打撃は1回。', '2026'], f_aut_time: ['解剖：死亡は、6日の20時45分から21時15分', '胃の中身から。夕食は19時50分。', '2026', 2026, '6日 20:45-21:15'], f_aut_fiber: ['右手の爪の間に、濃紺の毛の繊維が2本', '司法解剖。', '2026'],
  f_car2: ['20時59分、黒いセダンが分かれ道を登山口へ。21時32分に戻る', '県の道路カメラ。Nシステムには、かかっていない。', '2026', 2026, '6日 20:59-21:32'], f_owner: ['2台目の黒いセダンは、鷹取征二の名義', '下2桁「87」。車庫は、鷹取の屋敷。', '2026'],
  f_alibi_gap: ['征二の入室は21時44分。それより前を、誰も見ていない', '会議の接続の記録。家政婦は18時に帰った。', '2026', 2026, '6日 21:44'], f_calls: ['5日21時12分、鷹取の屋敷から朽木屋へ、4分の通話', '通話の履歴。', '2026', 2026, '5日 21:12'],
  f_ren_cell: ['蓮の携帯は、6日20時47分、登山口で圏外になった', '電源は、切られていない。そのまま、圏外。', '2026', 2026, '6日 20:47'], f_trail45: ['匡は4日の朝に森へ入り、5日の夕方に出てきた', '登山口のカメラ。入る時は箱を持ち、出る時は作業着で手ぶら。', '2026', 2026, '4日-5日'],
  f_plate87: ['2台目の車は、黒の大型セダン。ナンバーの下2桁は「87」', '道路カメラの映像を、38コマ重ねた。', '2026'], f_lab_coal: ['靴底の石炭がらは、1987年に閉山した炭鉱の石炭', '粒の角が立っている。踏んだのは、数日以内。', '2026'],
  f_lab_lime: ['すその石灰は、雨穴の入口から40メートル奥の岩と一致', '入口の岩とは、合わない。', '2026'], f_lab_cane: ['杖のくちばしの血は、被害者の物（DNA型の21座位が一致）', '水につかっていたが、内側の溝に残っていた。', '2026'],
  f_lab_fiber: ['爪の繊維は、濃紺のカシミヤのコート地。被害者の服ではない', 'カシミヤ70％、羊毛30％。', '2026'], f_lab_cloth: ['作業着の綿は1958〜60年の物。だが、66年ぶんの劣化が無い', '炭素14と、引っぱり強さ。', '2026'],
  f_lab_tool: ['杖の頭は、こめかみの創と重なる。石突きは、土の跡と同じ径', 'くちばし18.2ミリ。石突き22.0ミリ。', '2026'], f_lab_watch: ['時計は、打たれて止まったのではない', '歯車に傷が無い。りゅうずを引いて止め、針を合わせてから、割られた。', '2026'],
  f_lab_paper: ['百円札も整理券も本物。だが、紙が古びていない', '発行されたばかりの状態。', '2026'], f_lab_hand: ['1960年の宿帳の「三雲 朔」は、課長の字。インクは60年以上前', '15の特徴のうち、14が合う。', '2026'], f_lab_hand_ren: ['1960年の宿帳の「汐見 蓮」は、朽木匡の字', '帳簿の字と、13の特徴が合う。', '2026'],
  f_lab_gait: ['ドライブレコーダーの2人は、歩き方が同じ（似かた0.93）', '他人どうしは0.3以下。親子でも0.6をこえない。', '2026'], f_lab_gate: ['門の録画に書きかえは無い。出る時の杖が、戻った時には無い', '運転者の顔は、鷹取征二と0.91。', '2026'],
  f_lab_soil: ['遺体の下の土は含水率8％。まわりは31％', '遺体は、雨の降り始めより前から、そこにあった。', '2026'], f_lab_log: ['「出張」の行は、7日8時30分に、所長室の端末から足された', 'もとの行は、消されていない。', '2026'],
  p_time: ['方針：犯行の時刻は、時計に頼らない', '第1回の会議。りゅうずが、引き出されている。', '2026'], p_alibi: ['方針：当主のアリバイは、成り立たない', '第2回の会議。死亡は21時15分まで。会議は21時45分から。', '2026'], p_route: ['2台目の車は、鷹取の屋敷の坂から来た', '第2回の会議。Nシステムを通らずに分かれ道へ出る道は、屋敷の坂だけ。', '2026'],
});
LINKS.find(L => L.h === 'h_ren').B.push('f_lab_gait'); LINKS.find(L => L.h === 'h_guest').A.push('f_lab_hand_ren');
{ const F = BATTLE.F.r; F[0].ev.push('f_lab_soil'); F[1].ev.push('f_lab_watch'); F[2].ev.push('f_owner', 'f_car2', 'f_lab_gate', 'e_owner'); F[2].need.push([['car'], ['seiji', 'forest', 'trail']]); F[3].ev.push('f_lab_tool', 'f_lab_cane', 'f_aut_wound'); }
/* words of the trade, added to what listeners understand */
Object.assign(QW.人, { doji: ['堂島', 'どうじま', '係長'], makabe: ['真壁', 'まかべ'], okono: ['小此木', 'おこのぎ'], himuro: ['氷室', 'ひむろ'], tate: ['楯岡', 'たておか'], kuze: ['久世', 'くぜさん'] });
QW.所.mansion.push('屋敷の坂', '坂'); QW.所.town.push('町から'); QW.人.akari.push('鑑識');
QW.聞き方.help.push('何を指示', '何を頼めば', 'どう頼めば', '何をすれば', 'なにをすれば', '何ができる'); QW.捜査 = { culprit: ['犯人', 'はんにん', '真犯人', '誰が殺し', 'だれがころし'], kasoken: ['科捜研', 'かそうけん', '科学捜査'], autopsy: ['司法解剖', '解剖', 'かいぼう', '検死'], relay: ['リレー捜査', 'リレー', '防犯カメラ', 'カメラ', 'Nシステム', 'エヌシステム', '足取りを追'], nsys: ['Nシステム', 'エヌシステム'], owner: ['持ち主', 'もちぬし', '所有者', '名義', '登録', '誰の車', '車の照会', 'ナンバー照会'], inquire: ['照会', 'しょうかい'], bank: ['口座', '銀行', 'こうざ', '預金', '金の流れ'], summon: ['任意同行', '任意で', '事情聴取', '事情を聴', '呼び出', '呼べ', '引っぱ', '取り調べ'], footprint: ['足跡', 'あしあと', '下足', '指紋を採', '遺留品'], car2: ['2台目', '二台目', 'もう1台', '黒いセダン', 'セダン', '黒い車'],
  phone: ['通話履歴', '通話記録', '通話', 'つうわ', '電話の記録', '位置情報', '携帯の記録', '着信'], jidori: ['地取り', 'じどり', '目撃', '4日と5日', '宿を空け'], arrest: ['逮捕', 'たいほ', '身柄'], searchq: ['捜索', 'そうさく', '家宅捜索', 'ガサ入れ', '差し押さえ', '差押', '押収'], warrant: ['令状', 'れいじょう', '許可状'],
  confirm: ['裏付け', '裏づけ', 'うらづけ', '裏を取', 'うらをと', '洗え', '洗い直', '当たれ', '確認しろ', '確かめろ', '調べろ'], deploy: ['配備', 'はいび', '張り込', 'はりこ', '固めろ', 'かためろ', '検問', '人を置', '先回り', '向かう', '向かっ'],
  deathtime: ['死亡推定', '死亡時刻', '死亡の時刻', '死んだ時刻', '犯行時刻', '犯行の時刻', '死亡は', '死んだのは', '20時45分', '21時15分', '2045', '2115', '解剖の所見', '所見'], before: ['より前', '前だ', '前に', '以前', '30分', '空いて', '間に合', 'ずれ', '合わない', '矛盾', 'むじゅん', '食いちが', '成り立たない', 'ならない', '崩れ'],
  motive: ['動機', 'どうき', '殺す理由'], hideq: ['隠', 'かくし', '破棄', 'もみ消', '口止め', '握りつぶ'], crown: ['りゅうず', 'りゅず', '竜頭', '針を合わせ', '引き出され', 'ひきだされ'], doubt: ['偽装', 'ぎそう', '細工', 'わざと', 'あてにならない', '当てにならない', 'あてにするな', '当てにするな', '信用できない', '信用するな', '早い', '決めるな', '待て', '保留', '早合点'], t2217: ['22時17分', '2217'] };
QW.鑑定 = { m_dna: ['dna', 'ディーエヌエー', 'str'], blood: ['血痕', 'けっこん', '血液', '血を', '血の', '血が', 'しみ', 'ルミノール'], finger: ['指紋', 'しもん'], fiberq: ['繊維', 'せんい', '種類'], comp: ['成分', 'せいぶん', '分析', 'ぶんせき', '組成', 'X線', '産地', '何の粉'], dating: ['年代', 'ねんだい', '炭素', 'いつの物', 'いつ作', '古さ', '何年前'],
  shape: ['形', 'かたち', '照合', '重ね', '合うか', '一致するか', '成傷器', '傷と'], mech: ['しくみ', '止まった', 'とまった', '故障', '機械', 'なぜ止ま', '分解'], genuine: ['本物', 'ほんもの', 'にせ', '偽造', '真贋', '紙', '古び'], hand: ['筆跡', 'ひっせき', '字を', '字が', '字と', 'インク', '署名'],
  enhance: ['鮮明', 'せんめい', 'ナンバー', '拡大', 'はっきり', '読めるよう', '画質'], gait: ['歩き方', 'あるきかた', '歩容', 'ほよう', '身長', '骨格'], tamper: ['改ざん', 'かいざん', '書きかえ', '書き換え', '真正', '編集', '加工', '写っている物', '車内'],
  lime: ['石灰', 'せっかい', '白い粉', 'すその粉', '粉'], soil: ['土壌', 'どじょう', '下の土', '土の', '土を', '土は', '地面'], water: ['水分', 'すいぶん', '含水', '乾き', '乾いて', 'ぬれ', '湿り'], entrylog: ['入退構', 'にゅうたいこう', 'ログ', '出張の記録', '出張の行'], tox: ['薬毒物', '毒物', '毒', '睡眠薬', 'アルコール', '薬を', '薬の'], phonedev: ['スマホ', 'スマートフォン', '携帯', 'けいたい', '黒い板', 'パソコン', 'PC'], cloth: ['布', 'ぬの', '生地'], nailfiber: ['爪', 'つめ'], dash: ['ドライブレコーダー', 'ドラレコ', '後ろ姿'], roadcam: ['道路カメラ', '分かれ道のカメラ', '分かれ道の映像', '道路の映像'], gatevid: ['門の録画', '録画', '門の映像'] };
Object.assign(QSELF, { hq: 'doji', himuro: 'himuro', tate: 'tate', kuze: 'kuze' }); Object.assign(QFAM, { hq: {}, himuro: {}, tate: {}, kuze: {} });
/* orders: what the chief can tell the room to do. The same order gets a different answer when a warrant or a lead is still missing. */
QA.hq = [
  { k: 'autopsy', b: 'o_aut_nw', if: '!w1' }, { k: 'autopsy', b: 'o_aut_ok', if: 'w1&!o_aut' }, { k: 'autopsy', b: 'o_done', if: 'o_aut' },
  { k: 'jidori', b: 'o_jidori_nw', if: '!f:f_absent', w: 2 }, { k: 'jidori', b: 'o_jidori_ok', if: 'f:f_absent&!o_jidori', w: 2 }, { k: 'jidori', b: 'o_done', if: 'o_jidori', w: 2 },
  { k: 'owner|car2', b: 'o_owner_what', if: '!f:f_car2', w: 1 }, { k: 'owner|car2', b: 'o_owner_blur', if: 'f:f_car2&!f:f_plate87', w: 1 }, { k: 'owner|car2', b: 'o_owner_ok', if: 'f:f_plate87&!o_owner', w: 1 }, { k: 'owner|car2', b: 'o_done', if: 'o_owner', w: 1 },
  { k: 'alibi', b: 'o_alibi_nw', if: '!f:f_call' }, { k: 'alibi', b: 'o_alibi_ok', if: 'f:f_call&!o_alibi' }, { k: 'alibi', b: 'o_done', if: 'o_alibi' },
  { k: 'phone', b: 'o_phone_nw', if: '!w2' }, { k: 'phone', b: 'o_phone_ok', if: 'w2&!o_phone' }, { k: 'phone', b: 'o_done', if: 'o_phone' },
  { k: 'relay', b: 'o_relay_ok', if: '!o_relay' }, { k: 'relay', b: 'o_done', if: 'o_relay' },
  { k: 'bank', b: 'o_bank' }, { k: 'summon', b: 'o_summon' }, { k: 'deploy', b: 'o_watch', w: -1 }, { k: 'motive', b: 'o_motive', w: -1 }, { k: 'footprint|finger', b: 'o_kanshiki', w: -1 },
  { k: 'arrest', b: 'o_arrest_nw', if: '!w4' }, { k: 'arrest', b: 'o_arrest_ok', if: 'w4' }, { k: 'searchq', b: 'o_search_nw', if: '!w3' }, { k: 'searchq', b: 'o_search_ok', if: 'w3' }, { k: 'warrant', b: 'o_warrant', w: -1 } ];
QA.hq.push({ k: 'culprit', b: 'q_hq_x2', w: -1 }); for (const k of ['himuro', 'tate', 'kuze']) QA[k] = [{ k: 'culprit', b: `q_${k}_who`, w: -1 }]; QA.himuro.push({ k: 'tox', b: 'q_himuro_tox' }); QA.kuze.push({ k: 'phonedev', b: 'q_kuze_phone' });
/* meetings: reports first, then the chief speaks. items: [flag, what has to be settled, an example for players who turn hints on] */
const MTG = {
  m1: { n: '第1回 捜査会議', if: 'body_done', open: 'm1_open', done: 'm1_done', items: [['m1a1', '死因と時刻を、どう確かめるか', '司法解剖に回す'], ['o_relay', '被害者の足取りを、どう追うか', '防犯カメラとNシステムで足取りを追え'], ['m1c1', '報告の中に、早合点が1つある', '時計はあてにするな。りゅうずが引き出されている']] },
  m2: { n: '第2回 捜査会議', if: 'm1&b1&ev:e_autopsy&ev:e_relay', open: 'm2_open', done: 'm2_done', items: [['m2c2', '当主のアリバイは、本当に成り立つか', '死亡は21時15分まで。21時45分からの会議は、アリバイにならない'], ['m2c3', '2台目の車は、どこから来たか', '2台目はNシステムを通っていない。屋敷の坂から来た車だ']] },
  m3: { n: '第3回 捜査会議', if: 'm2&p4&ev:e_box', open: 'm3_open', done: 'm3_done', items: [['m3a6', 'なぜ、当主は、宿の主人を殺したか', '動機は1993年の排水坑の事故の隠ぺい。原本がある'], ['m3c4', '当主は、いま、どこへ向かっているか', '当主は雨穴へ向かう。登山口を固めろ'], ['m3a7', '逮捕に、踏み切るか', '鷹取征二の逮捕状を請求する']] } };
QA.m1 = [{ k: 'autopsy', b: 'm1_a1', if: '!m1a1', w: 5 }, { k: 'relay', b: 'm1_a2', if: '!o_relay', w: 5 }, { k: 'watch|t2217 crown|doubt', b: 'm1_c1', if: 'f:f_crown&!m1c1', w: 5 }, { k: 'watch|t2217 crown|doubt', b: 'm1_c1_no', if: '!f:f_crown', w: 5 }, { k: 'crown|doubt', b: 'm1_c1', if: 'f:f_crown&!m1c1', w: 4 }, { k: 'crown|doubt', b: 'm1_c1_no', if: '!f:f_crown&!m1c1', w: 4 }];
QA.m2 = [{ k: 'alibi|meeting deathtime|before', b: 'm2_c2', if: 'f:f_aut_time&!m2c2', w: 5 }, { k: 'deathtime before', b: 'm2_c2', if: 'f:f_aut_time&!m2c2', w: 5 }, { k: 'alibi|meeting deathtime|before', b: 'm2_c2_no', if: '!f:f_aut_time', w: 5 }, { k: 'deathtime before', b: 'm2_c2_no', if: '!f:f_aut_time', w: 5 }, { k: 'car2|nsys mansion', b: 'm2_c3', if: '!m2c3', w: 5 }];
QA.m3 = [{ k: 'accident|tunnel|y1993|y33|motive hideq|box|record', b: 'm3_a6', if: '!m3a6', w: 5 }, { k: 'cave|forest deploy|seiji', b: 'm3_c4', if: '!m3c4', w: 5 }, { k: 'arrest|warrant', b: 'm3_a7', if: 'm3a6&!m3a7', w: 5 }, { k: 'arrest|warrant', b: 'm3_a7_no', if: '!m3a6', w: 5 }];
/* the lab: who does what. spec: the thing brought in. meth: how to examine it. Both have to be said. */
const LAB = [
  { id: 'dna', who: 'himuro', spec: 'toothbrush', meth: 'm_dna', need: 'tooth', b: 'l_dna' }, { id: 'coal', who: 'himuro', spec: 'coal', meth: 'comp|dating', need: 'f:f_coal', b: 'l_coal' }, { id: 'cane', who: 'himuro', spec: 'cane', meth: 'blood|m_dna|finger', need: 'f:f_canefound', b: 'l_cane' },
  { id: 'fiber', who: 'himuro', spec: 'nailfiber', meth: 'fiberq|comp', need: 'f:f_aut_fiber', b: 'l_fiber' }, { id: 'cloth', who: 'himuro', spec: 'jacket|cloth', meth: 'fiberq|comp|dating', need: 'f:f_tag|f:f_newcloth', b: 'l_cloth' }, { id: 'lime', who: 'himuro', spec: 'lime', meth: 'comp|shape', need: 'f:f_lime', b: 'l_lime' }, { id: 'soil', who: 'himuro', spec: 'soil', meth: 'water|comp', need: 'f:f_dry', b: 'l_soil' },
  { id: 'tool', who: 'tate', spec: 'cane', meth: 'shape', need: 'f:f_canefound', b: 'l_tool' }, { id: 'watch', who: 'tate', spec: 'watch', meth: 'mech|shape', need: 'f:f_watch|f:f_crown', b: 'l_watch' }, { id: 'paper', who: 'tate', spec: 'bill|ticket', meth: 'genuine|dating', need: 'f:f_note|f:f_ticket', b: 'l_paper' }, { id: 'hand', who: 'tate', spec: 'ledger', meth: 'hand|dating', need: 'ev:e_ledger', b: 'l_hand' },
  { id: 'gait', who: 'kuze', spec: 'dash', meth: 'gait|enhance', need: 'ev:e_dash', b: 'l_gait' }, { id: 'plate', who: 'kuze', spec: 'roadcam|car2', meth: 'enhance', need: 'ev:e_relay', b: 'l_plate' }, { id: 'gate', who: 'kuze', spec: 'gatevid', meth: 'tamper|enhance', need: 'ev:e_gate', b: 'l_gate' }, { id: 'log', who: 'kuze', spec: 'entrylog', meth: 'tamper|enhance', need: 'ev:e_entry', b: 'l_log' } ];
/* warrants: need is a list of groups; the chosen facts have to hit every group. why says what a group stands for, in the judge's words. */
const WAR = [
  { id: 'w1', n: '鑑定処分許可状', sub: '司法解剖のため', if: 'm1a1', no: '会議で、解剖の方針を決めてから。', need: [['f_wound'], ['f_cane', 'f_dry', 'f_crown', 'f_tod', 'f_newcloth', 'f_lab_soil']], why: ['人の手による傷である事', '事件である事を示す、もう1つの資料'], ok: 'w_ok1' },
  { id: 'w2', n: '差押許可状', sub: '通話の履歴と位置', if: 'hq', no: '', need: [['f_tod', 'f_wound'], ['f_two', 'f_rencar', 'f_absent']], why: ['人が死んだ時刻か、傷を示す資料', '被害者と汐見蓮の動きが、事件に関わる事を示す資料'], ok: 'w_ok2' },
  { id: 'w3', n: '捜索差押許可状', sub: '鷹取の屋敷　門の録画', if: 'f:f_owner', no: '屋敷と事件を結ぶ物が、まだ無い。', need: [['f_owner'], ['f_car2', 'p_route', 'f_light'], ['f_hawk', 'f_aut_wound', 'f_wound', 'f_cane', 'p_alibi', 'f_alibi_gap']], why: ['あの夜の車が、屋敷の物である事', 'その車が、現場へ向かった事', '当主と、傷や時刻を結ぶ資料'], ok: 'w_ok3' },
  { id: 'w4', n: '逮捕状', sub: '鷹取征二　殺人', if: 'm3a7', no: '会議で、逮捕の方針を決めてから。', need: [['f_lab_cane', 'f_lab_tool'], ['f_gate', 'f_owner', 'f_lab_gate'], ['f_box', 'f_threat', 'f_memo', 'f_letter', 'p_alibi', 'f_aut_time', 'f_lab_watch']], why: ['凶器と、被害者を結ぶ鑑定', '当主が、現場へ行けた事を示す資料', '動機か、時刻の偽装を示す資料'], ok: 'w_ok4' } ];
/* helper buttons for orders, meetings and lab requests */
const HCHIP = { 指示の型: ['を司法解剖に回せ', 'を洗え', 'の裏付けを取れ', 'を照会しろ', 'で足取りを追え', 'を固めろ', 'の逮捕状を請求する', 'は矛盾している', 'はアリバイにならない', 'はあてにするな', 'から来た車だ', 'が動機だ'],
  捜査の言葉: ['司法解剖', '防犯カメラ', 'Nシステム', '通話履歴', '銀行口座', '任意同行', '動機', 'アリバイ', '死亡推定時刻', '21時15分', '21時45分からの会議', '2台目の車', '持ち主', '地取り', '4日と5日', '腕時計', 'りゅうず', '屋敷の坂', '1993年の事故の隠ぺい', '原本', '雨穴', '登山口'],
  部署と人: ['堂島係長', '真壁', '小此木', '鑑識', '科捜研', '被害者', '朽木匡', '汐見蓮', '鷹取征二', '鷹取玲', '汐見修'] };
const LCHIP = { 鑑定の型: ['のDNA型を調べて', 'の成分を分析して', 'の血痕を調べて', 'の繊維の種類を調べて', 'の年代を調べて', 'の水分を測って', 'と傷の形を照合して', 'が止まったしくみを調べて', 'が本物かを調べて', 'の筆跡を比べて', 'を鮮明にして', 'の歩き方を解析して', 'の書きかえを調べて'],
  検体: [['歯ブラシ', 'tooth'], ['靴底の石炭がら', 'f:f_coal'], ['すその石灰', 'f:f_lime'], ['遺体の下の土', 'f:f_dry'], ['入退構の記録', 'ev:e_entry'], ['作業着の布', 'f:f_tag|f:f_newcloth'], ['百円札と整理券', 'f:f_note|f:f_ticket'], ['腕時計', 'f:f_watch|f:f_crown'], ['杖', 'f:f_canefound'], ['爪の繊維', 'f:f_aut_fiber'], ['宿帳', 'ev:e_ledger'], ['ドライブレコーダー', 'ev:e_dash'], ['道路カメラの映像', 'ev:e_relay'], ['門の録画', 'ev:e_gate']] };
