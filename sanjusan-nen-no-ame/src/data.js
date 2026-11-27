/* ---------- the world: eras, roads, places, things to look at, people to talk to, evidence, facts, links, battles ---------- */
const ERA = { 2026: { g: '令和8年', n: '2026' }, 1993: { g: '平成5年', n: '1993' }, 1960: { g: '昭和35年', n: '1960' } };
const dayOf = (e, F) => e === 2026 ? (F.p4 ? '11月11日（水）' : F.cave_open ? '11月8日（日）' : '11月7日（土）') : e === 1993 ? (F.b2 ? '11月10日（水）' : F.day9 ? '11月9日（火）' : '11月8日（月）') : '11月10日（木）';
/* roads: a small graph. Junction exits are listed clockwise, so left and right can be told from the way you came in. */
const NODES = {
  town:    { n: '町の通り', scene: 'street', at: 'car', map: [70, 150] },
  j1:      { n: '町はずれの四つ辻', map: [170, 120], ex: ['j1-j2', 'j1-plant', 'town-j1', 'j1-grave'] },
  grave:   { n: '霧渕の墓地', scene: 'grave', at: 'car', map: [92, 92] },
  plant:   { n: { 2026: '霧渕原発 正門', 1993: '霧渕原発 正門', 1960: '発電所の建設地' }, scene: 'plant', at: 'car', map: [250, 170] },
  j2:      { n: '森の分かれ道', map: [215, 62], ex: ['j1-j2', 'j2-mansion', 'j2-trail'] },
  trail:   { n: '黒檜の森 登山口', scene: 'forest', at: 'car', map: [290, 30] },
  mansion: { n: '鷹取の屋敷', scene: 'mansion', at: 'out', map: [130, 26], eras: [2026, 1993] },
};
const EDGES = {
  'town-j1':    { a: 'town', b: 'j1', len: 70, kind: 'town', n: '町の道', curve: [[12, 26, 1.6], [40, 56, -2.2]], hill: [[20, 50, 14]] },
  'j1-plant':   { a: 'j1', b: 'plant', len: 80, kind: 'fence', n: '発電所の道', curve: [[10, 30, -2.4], [46, 70, 1.4]], hill: [[10, 40, -10]] },
  'j1-j2':      { a: 'j1', b: 'j2', len: 80, kind: 'forest', n: '森の道', curve: [[8, 28, 2.6], [34, 52, -3], [58, 74, 2]], hill: [[10, 70, 30]] },
  'j2-trail':   { a: 'j2', b: 'trail', len: 60, kind: 'deep', n: '森の細道', curve: [[6, 22, -3.4], [28, 44, 3.6], [48, 58, -1.5]], hill: [[6, 50, 22]] },
  'j1-grave':   { a: 'j1', b: 'grave', len: 50, kind: 'hill', n: '寺の坂', curve: [[8, 24, -2.8], [30, 44, 2.2]], hill: [[6, 44, 26]] },
  'j2-mansion': { a: 'j2', b: 'mansion', len: 70, kind: 'hill', n: '屋敷の坂道', curve: [[10, 30, 3], [40, 60, -2.6]], hill: [[10, 64, 40]] },
};
const CARS = { 2026: '署の車', 1993: '巌のパトカー', 1960: '朽木屋のオート三輪' };
/* interiors hang off the street; x is the spot on the street you come back to */
const INDOOR = { police: ['street', 'police'], clinic: ['street', 'clinic'], inn: ['street', 'inn'], tunnel: ['forest', 'tunnel'], cave: ['forest', 'cave'] };
const PLACE = { forest: { 2026: '黒檜の森　雨穴の道', 1993: '黒檜の森　雨穴の道', 1960: '黒檜の森　雨穴道' }, cave: '雨穴', street: '霧渕の町', police: { 2026: '霧渕警察署', 1993: '霧渕警察署', 1960: '霧渕駐在所' }, clinic: '汐見医院', inn: '朽木屋', plant: { 2026: '霧渕原子力発電所　正門', 1993: '霧渕原子力発電所　正門', 1960: '発電所の建設地' }, mansion: '鷹取の屋敷　書斎', grave: '霧渕の墓地', tunnel: { 1993: '第2排水坑', 1960: '鷹取組の試掘坑' } };
/* things in a scene. x: spot name. e: eras. if: flags ("a", "!a", "a&b"). k: look | exit | car | body | travel. b: story block. */
const OBJ = {
  forest: [
    { id: 'car', x: 'car', l: '車に乗る', k: 'car', node: 'trail', e: [2026] }, { id: 'car93', x: 'car', l: 'パトカーに乗る', k: 'car', node: 'trail', e: [1993], if: 'met_iwao' }, { id: 'car60', x: 'car', l: 'オート三輪に乗る', k: 'car', node: 'trail', e: [1960], first: 'f60_car' },
    { id: 'rencar', x: 130, l: '白い車を調べる', k: 'look', b: 'f26_rencar', e: [2026] }, { id: 'sign', x: 'sign', l: '看板を見る', k: 'look', b: 'f26_sign' }, { id: 'vend', x: 'vend', l: '自動販売機を見る', k: 'look', b: 'f93_vend', e: [1993] },
    { id: 'tun26', x: 'tunnel', l: '排水坑の口を調べる', k: 'look', b: 'f26_tunnel', e: [2026] }, { id: 'tun93x', x: 'tunnel', l: '排水坑の口を調べる', k: 'look', b: 'f93_tunnel_ng', e: [1993], if: '!day9' }, { id: 'tun93', x: 'tunnel', l: '排水坑に入る', k: 'exit', to: 'tunnel', at: 'out', first: 'f93_tunnel', e: [1993], if: 'day9' }, { id: 'tun60', x: 'tunnel', l: '試掘坑に入る', k: 'exit', to: 'tunnel', at: 'out', first: 'f60_tunnel', e: [1960] },
    { id: 'body', x: 'body', l: '遺体を検分する', k: 'body', e: [2026], if: 'met_akari&!p4' },
    { id: 'final', x: 2990, l: '雨穴の前で、当主を待つ', k: 'final', e: [2026], if: 'p4&ev:e_box&!done' },
    { id: 'cavex', x: 'cave', l: '雨穴をのぞく', k: 'look', b: 'f26_cave_closed', e: [2026], if: '!cave_open' }, { id: 'cave26', x: 'cave', l: '雨穴に入る', k: 'exit', to: 'cave', at: 'out', first: 'f26_cave_open', e: [2026], if: 'cave_open' }, { id: 'cave93', x: 'cave', l: '雨穴に入る', k: 'exit', to: 'cave', at: 'out', first: 'f93_cave', e: [1993] }, { id: 'cave60', x: 'cave', l: '雨穴に入る', k: 'exit', to: 'cave', at: 'out', first: 'f60_cave', e: [1960] } ],
  cave: [ { id: 'out', x: 'out', l: '外へ出る', k: 'exit', to: 'forest', at: 'cave' }, { id: 'lamp', x: 'lamp', l: 'ランプを見る', k: 'look', b: 'c_lamp' }, { id: 'carve', x: 'carve', l: '岩の字を見る', k: 'look', b: 'c_carve' },
    { id: 'pool26', x: 'pool', l: '水たまりを調べる', k: 'look', b: 'c26_pool', e: [2026], if: '!f:f_canefound' }, { id: 'pool', x: 'pool', l: '水たまりを見る', k: 'look', b: 'c_pool', if: 'f:f_canefound|!e2026' },
    { id: 'left', x: 'left', l: '左の道「下」へ進む', k: 'travel', d: -33 }, { id: 'right', x: 'right', l: '右の道「上」へ進む', k: 'travel', d: 33 } ],
  street: [ { id: 'car', x: 'car', l: '車に乗る', k: 'car', node: 'town' }, { id: 'police', x: 'police', l: { 2026: '警察署に入る', 1993: '警察署に入る', 1960: '駐在所に入る' }, k: 'exit', to: 'police', at: 'out' },
    { id: 'clinic', x: 'clinic', l: '汐見医院に入る', k: 'exit', to: 'clinic', at: 'out', e: [2026, 1993] }, { id: 'clinic60', x: 'clinic', l: '産院をのぞく', k: 'look', b: 'st60_clinic', e: [1960] }, { id: 'inn', x: 'inn', l: '朽木屋に入る', k: 'exit', to: 'inn', at: 'out' } ],
  police: [ { id: 'out', x: 'out', l: '外へ出る', k: 'exit', to: 'street', at: 'police' }, { id: 'pc', x: 'pc', l: '端末を使う', k: 'look', b: 'p26_pc', e: [2026], if: '!ev:e_weather' }, { id: 'pc2', x: 'pc', l: '端末を使う（新しい知らせ）', k: 'look', b: 'p26_pc_dna', e: [2026], if: 'ev:e_weather&b1&tooth&!ev:e_dna' },
    { id: 'desk', x: 'desk', l: '机を見る', k: 'look', b: { 2026: 'p26_desk', 1993: 'p93_desk', 1960: 'p60_desk' } }, { id: 'pc3', x: 'pc', l: '端末を使う（追加の知らせ）', k: 'look', b: 'p26_pc_dna2', e: [2026], if: 'p4&ev:e_dna&!ev:e_dna2' }, { id: 'bones', x: 'archive', l: '白骨を検分する', k: 'sheet', sheet: 'bones', e: [1993], if: 'bones_ok' }, { id: 'board', x: 'board', l: '掲示板を見る', k: 'look', b: { 2026: 'p26_board', 1993: 'p93_board', 1960: 'p60_board' } }, { id: 'archive', x: 'archive', l: '書庫を調べる', k: 'look', b: { 2026: 'p26_archive', 1993: 'p93_archive', 1960: 'p60_archive' }, if: '!bones_ok|!e1993' } ],
  clinic: [ { id: 'out', x: 'out', l: '外へ出る', k: 'exit', to: 'street', at: 'clinic' }, { id: 'shelf', x: 'shelf', l: 'カルテの棚を見る', k: 'look', b: 'cl_shelf' }, { id: 'light', x: 'light', l: 'レントゲンの写真を見る', k: 'look', b: 'cl_light' }, { id: 'notice', x: 'out', dx: 190, l: '休診の札を見る', k: 'look', b: 'cl26_notice', e: [2026], if: 'p4' } ],
  inn: [ { id: 'out', x: 'out', l: '外へ出る', k: 'exit', to: 'street', at: 'inn' }, { id: 'front', x: 'front', l: '帳場を見る', k: 'look', b: { 2026: 'i26_front', 1993: 'i93_front', 1960: 'i60_front' }, dx: -230 },
    { id: 'led26', x: 'ledger', l: '古い宿帳を調べる', k: 'look', b: 'i26_ledger', e: [2026], if: 'ledger_ok' }, { id: 'led26x', x: 'ledger', l: '棚を見る', k: 'look', b: 'i26_ledger_ng', e: [2026], if: '!ledger_ok' }, { id: 'led93', x: 'ledger', l: '棚を見る', k: 'look', b: 'i93_ledger', e: [1993] }, { id: 'led60', x: 'ledger', l: '宿帳を調べる', k: 'look', b: 'i60_ledger', e: [1960] },
    { id: 'hearth', x: 'hearth', l: '居間を見る', k: 'look', b: { 2026: 'i26_hearth', 1993: 'i93_hearth', 1960: 'i60_hearth' }, dx: 200 },
    { id: 'lug93', x: 'luggage', l: '青年の荷物を調べる', k: 'look', b: 'i93_luggage', e: [1993], if: 'luggage_ok' }, { id: 'lug93x', x: 'luggage', l: '荷物を見る', k: 'look', b: 'i93_luggage_ng', e: [1993], if: '!luggage_ok' }, { id: 'lug', x: 'luggage', l: '客室を見る', k: 'look', b: { 2026: 'i26_luggage', 1960: 'i60_luggage' }, e: [2026, 1960], if: '!child_ok|!e1960' }, { id: 'child', x: 'luggage', l: '男の子の持ち物を検分する', k: 'sheet', sheet: 'child', e: [1960], if: 'child_ok' },
    { id: 'safe', x: 'safe', l: '金庫を見る', k: 'look', b: { 2026: 'i26_safe', 1993: 'i93_safe', 1960: 'i60_safe' } } ],
  plant: [ { id: 'car', x: 'car', l: '車に乗る', k: 'car', node: 'plant' }, { id: 'guard', x: 'guard', l: '守衛所で聞く', k: 'look', b: { 2026: 'pl26_guard', 1993: 'pl93_guard' }, e: [2026, 1993] }, { id: 'board', x: 'board', l: '掲示板を見る', k: 'look', b: { 2026: 'pl26_board', 1993: 'pl93_board' }, e: [2026, 1993] },
    { id: 'tent', x: 'tent', l: '台帳を調べる', k: 'look', b: 'pl60_tent', e: [1960], if: 'supply_ok' }, { id: 'tentx', x: 'tent', l: '天幕を見る', k: 'look', b: 'pl60_tent_ng', e: [1960], if: '!supply_ok' }, { id: 'hut', x: 'hut', l: '飯場を見る', k: 'look', b: 'pl60_hut', e: [1960] }, { id: 'crane', x: 'crane', l: 'やぐらの下を見る', k: 'look', b: 'pl60_crane', e: [1960] } ],
  grave: [ { id: 'car', x: 'car', l: '車に乗る', k: 'car', node: 'grave' }, { id: 'gate', x: 'gate', l: '寺の門を見る', k: 'look', b: 'g_gate' }, { id: 'toki', x: 'toki', l: { 2026: '小さな石を調べる', 1993: '鷹取の墓を見る', 1960: '鷹取の墓を見る' }, k: 'look', b: { 2026: 'g26_toki', 1993: 'g93_toki', 1960: 'g60_toki' } },
    { id: 'muen', x: 'muen', l: { 2026: '古い石を調べる', 1993: '掘り返した穴を見る', 1960: '空き地を見る' }, k: 'look', b: { 2026: 'g26_muen', 1993: 'g93_muen', 1960: 'g60_muen' } }, { id: 'iwao', x: 'iwao', l: '三雲の墓を見る', k: 'look', b: { 2026: 'g26_iwao', 1993: 'g93_iwao', 1960: 'g60_iwao' } }, { id: 'tae', x: 'tae', l: '汐見の墓を見る', k: 'look', b: 'g26_tae', e: [2026] } ],
  mansion: [ { id: 'out', x: 'out', l: '屋敷を出て車に乗る', k: 'car', node: 'mansion' }, { id: 'photo', x: 'photo', l: '額の写真を見る', k: 'look', b: { 2026: 'm26_photo', 1993: 'm93_photo' } }, { id: 'desk', x: 'desk', l: '机を見る', k: 'look', b: { 2026: 'm26_desk', 1993: 'm93_desk' } }, { id: 'cane', x: 'cane', l: '傘立てを見る', k: 'look', b: { 2026: 'm26_cane', 1993: 'm93_cane' } }, { id: 'sewing', x: 'sewing', l: 'ばあやの針箱を調べる', k: 'look', b: 'm93_sewing', e: [1993], if: 'met_toki' }, { id: 'mon93', x: 'monitor', l: '棚の上を見る', k: 'look', b: 'm93_monitor', e: [1993] },
    { id: 'mon', x: 'monitor', l: '門の録画を見る', k: 'look', b: 'm26_monitor', e: [2026], if: 'gate_ok' }, { id: 'monx', x: 'monitor', l: '録画の機械を見る', k: 'look', b: 'm26_monitor_ng', e: [2026], if: '!gate_ok' } ],
  tunnel: [ { id: 'out', x: 'out', l: '外へ出る', k: 'exit', to: 'forest', at: 'tunnel' },
    { id: 'office', x: 'office', l: '見張りの小屋を調べる', k: 'look', b: 't93_office', e: [1993], if: '!accident' }, { id: 'office2', x: 'office', l: '日誌を調べる', k: 'look', b: 't93_office_after', e: [1993], if: 'accident' },
    { id: 'rack', x: 'rack', l: 'バッジの棚を見る', k: 'look', b: 't93_rack', e: [1993], if: '!accident' }, { id: 'rack2', x: 'rack', l: 'バッジの棚を調べる', k: 'look', b: 't93_rack_after', e: [1993], if: 'accident' },
    { id: 'valve', x: 'valve', l: 'バルブを見る', k: 'look', b: 't93_valve_after', e: [1993], if: 'accident' }, { id: 'cart', x: 'rack', l: 'トロッコを見る', k: 'look', b: 't60_cart', e: [1960] }, { id: 'breach', x: 'breach', l: 'くずれた岩を調べる', k: 'look', b: 't60_breach', e: [1960] } ],
};
/* walking into these x ranges plays a block once */
const TRIG = [ { s: 'forest', e: 2026, x: 2480, b: 'f26_akari_first', if: '!met_akari' }, { s: 'tunnel', e: 1993, x: 1330, b: 't93_accident', if: '!accident' }, { s: 'mansion', e: 2026, x: 400, b: 'm26_empty', if: 'p4&!seen_empty', set: 'seen_empty' } ];
/* people standing in scenes. t: topics [label, block, if, once]. first: block for the first talk. battle: id */
const NPC = [
  { id: 'akari', s: 'forest', e: 2026, x: 2760, if: '!p4', t: [['きのうの夜の事', 'akari26_night'], ['汐見蓮の事', 'akari26_ren'], ['2人を照らし合わせる', 'akari26_dna', 'body_done']] },
  { id: 'akari', s: 'forest', e: 2026, x: 2560, if: 'p4', t: [['2人を照らし合わせる', 'akari26_dna', '!need_tooth']] },
  { id: 'osamu71', s: 'clinic', e: 2026, x: 880, first: 'osamu26_first', t: [['5日の夜の口論', 'osamu26_quarrel'], ['歯ブラシを借りる', 'osamu26_tooth', 'need_tooth&!tooth'], ['鷹取の当主の足', 'osamu26_plate', 'met_seiji']], battle: 'B4', bif: 'p4&f:f_twin_dna&!b4', bl: '先生自身の事を、問いただす' },
  { id: 'sayo58', s: 'inn', e: 2026, x: 700, first: 'sayo26_first', t: [['きのうの夜の事', 'sayo26_night'], ['おかしな事', 'sayo26_absent'], ['匡さんの昔', 'sayo26_past'], ['古い宿帳', 'sayo26_ledger']], battle: 'B5', bif: 'p4&ev:e_belong&!b5', bl: '黙っている事を、問いただす' },
  { id: 'rei', s: 'plant', e: 2026, x: 1720, first: 'rei26_first', t: [['汐見蓮の事', 'rei26_ren'], ['当主の、6日の夜', 'rei26_father'], ['育ててくれた人', 'rei26_toki'], ['襟の章', 'rei26_pin'], ['箱を見せる', 'rei26_p4', 'p4&ev:e_box&!gate_ok']], battle: 'B1', bif: '!b1', bl: '3つの点を、問いただす' },
  { id: 'seiji76', s: 'mansion', e: 2026, x: 1480, if: '!p4', first: 'm26_first', t: [['6日の夜の事', 'seiji26_night'], ['腕時計', 'seiji26_watch'], ['杖', 'seiji26_cane'], ['朽木匡の事', 'seiji26_tadashi']] },
  { id: 'iwao', s: 'forest', e: 1993, x: 470, if: '!met_iwao', first: 'iwao93_first', t: [] },
  { id: 'iwao', s: 'police', e: 1993, x: 980, if: 'met_iwao', t: [['妙な事件', 'iwao93_file'], ['白骨を見せてもらう', 'iwao93_bones', 'ev:e_file'], ['記憶のない青年', 'iwao93_ren'], ['息子の事', 'iwao93_son'], ['別れを言う', 'iwao93_after', 'b2&!iwao_bye']] },
  { id: 'sayo25', s: 'inn', e: 1993, x: 700, first: 'sayo93_first', t: [['青年の荷物', 'sayo93_luggage'], ['近ごろ、変わった事', 'sayo93_bus'], ['泊まって、あしたにする', 'sayo93_stay', 'met_ren&!day9', 1]] },
  { id: 'ren', s: 'inn', e: 1993, x: 1560, if: '!accident', first: 'ren93_meet', set: 'met_ren', t: [['なぜ、ここへ来た', 'ren93_why'], ['腕を見せてもらう', 'ren93_arm'], ['2026年の事', 'ren93_home']] },
  { id: 'ren', s: 'inn', e: 1993, x: 2090, if: 'accident', first: 'ren93_after', fk: 'ren_after', t: [] },
  { id: 'osamu38', s: 'clinic', e: 1993, x: 880, first: 'osamu93_first', t: [['きょうの、けが人', 'osamu93_after', 'accident']] },
  { id: 'seiji43', s: 'plant', e: 1993, x: 1720, first: 'seiji93_first', t: [['腕時計を見る', 'seiji93_watch']], battle: 'B2', bif: 'accident&!b2', bl: '事故の事を、問いただす' },
  { id: 'toki', s: 'mansion', e: 1993, x: 1480, first: 'toki93_first', t: [['このお屋敷の事', 'toki93_house'], ['昔の事', 'toki93_past']], battle: 'B6', bif: 'f:f_toki_pin&!b6', bl: 'どこから来たのかを、問いただす' },
  { id: 'rei8', s: 'mansion', e: 1993, x: 900, first: 'rei8_first', t: [['ばあやの事', 'rei8_toki'], ['大きくなったら', 'rei8_dream']] },
  { id: 'nozomu', s: 'inn', e: 1960, x: 1860, first: 'nozomu60_first', t: [['名前を聞く', 'nozomu60_name'], ['おうちの事', 'nozomu60_home']] },
  { id: 'kiichi', s: 'police', e: 1960, x: 980, first: 'kiichi60_first', t: [['駐在の日誌', 'kiichi60_diary'], ['息子の事', 'kiichi60_son'], ['5日前の、宿の客', 'kiichi60_guest']] },
  { id: 'haru', s: 'inn', e: 1960, x: 700, first: 'haru60_first', t: [['5日前のお客', 'haru60_guest']], battle: 'B3', bif: '!b3', bl: '3つの問いに、答える' },
  { id: 'tae', s: 'inn', e: 1960, x: 1560, first: 'tae60_first', t: [['5日前の客の腕', 'tae60_scar'], ['拾った男の子', 'tae60_boy'], ['家族の事', 'tae60_family']], battle: 'B7', bif: 'f:f_found60&f:f_child_tag&met_nozomu&!b7', bl: 'あの子の事を、話す' },
  { id: 'soichiro', s: 'plant', e: 1960, x: 1900, first: 'soichiro60_first', t: [['試掘坑の事', 'soichiro60_blast'], ['支給品の台帳', 'soichiro60_ledger']] },
  { id: 'seiji10', s: 'plant', e: 1960, x: 2520, first: 'boy60_first', t: [['腕時計の事', 'boy60_watch'], ['将来の事', 'boy60_dream']] },
];
/* which portrait a speaker uses */
const FACE = { saku: 'saku', akari: 'akari', rei: 'rei', seiji76: 'seiji76', seiji43: 'seiji43', seiji10: 'seiji10', sayo58: 'sayo58', sayo25: 'sayo25', osamu71: 'osamu71', osamu38: 'osamu38', ren: e => e === 1993 ? 'tadashi27' : 'ren27', tadashi60: 'tadashi60', iwao: 'iwao35', kiichi: 'kiichi35', haru: 'haru40', soichiro: 'soichiro45', tae: 'tae30', kid: 'kid5', toki: 'toki74', rei8: 'rei8', nozomu: 'nozomu5' };
/* facts: [title, detail, group, era, time label] */
const FACTS = {
  f_tag: ['作業着のタグは「昭和35年度 支給 №47」', '鷹取組の支給品。66年前の年度だ。', '遺体'], f_newcloth: ['作業着の布は新しい', '色あせも、すり切れもない。66年たった布ではない。', '遺体'],
  f_scar: ['左腕に、三日月形の古い火傷', '何十年も前の物。丸い縁を、押しつけた形。', '遺体'], f_wound: ['右こめかみに、鉤形の傷', '鳥のくちばしのような形の固い物で、1度。これが死因。', '遺体'],
  f_watch: ['腕時計は22時17分で止まっている', 'ガラスが割れている。', '遺体', 2026, '6日 22:17'], f_crown: ['腕時計のりゅうずが引き出されている', '針を合わせる位置のまま、止まっている。', '遺体'],
  f_dry: ['遺体の下の土は乾いている', 'まわりの土は、雨でぬかるんでいる。', '遺体'], f_cane: ['遺体のそばに、丸い杖の跡', '径22ミリ。足跡の横に、同じ間をおいて続く。', '遺体'],
  f_coal: ['靴の底に、石炭がら', 'いまの町に、石炭を燃やす所はない。', '遺体'], f_note: ['ポケットに、板垣退助の百円札', '折り目のない、新しい札。60年前のお金だ。', '遺体'], f_ticket: ['ポケットに、バスの整理券「5.11.5」', '霧渕交通。平成5年11月5日。紙は、黄ばんでいない。', '遺体'],
  f_tod: ['死亡推定は、6日の20時半から22時半', '体温と、体の固まり方から。', '2026', 2026, '6日 20:30-22:30'], f_rain: ['雨の降り始めは、6日の21時40分', '気象の記録。それまでは、降っていない。', '2026', 2026, '6日 21:40'],
  f_rencar: ['蓮の車は、6日20時41分から登山口にある', '中に社員証。動かした跡はない。', '2026', 2026, '6日 20:41'], f_two: ['20時48分、蓮と匡が森へ歩いていく', 'ドライブレコーダーの、2人の後ろ姿。', '2026', 2026, '6日 20:48'], f_light: ['21時04分と21時27分に、別の車のライト', '登山口を、行って、戻った。車体は映っていない。', '2026', 2026, '6日 21:04 / 21:27'],
  f_trip: ['「出張」は、7日の朝に書き足された', '蓮は6日18時02分に出たきり。入力したのは所長。', '2026', 2026, '7日 8:30'], f_call: ['征二は21時45分から22時半まで、会議の画面にいた', '廃炉委員会。20人が見ている。', '2026', 2026, '6日 21:45-22:30'],
  f_absent: ['匡は4日と5日、宿を空けた', '石炭の煙のにおいと、古い作業着で帰った。金庫の中身を持って出て、手ぶらで戻った。', '2026', 2026, '4日-5日'],
  f_dna_same: ['遺体と汐見蓮のDNAは、同一', '歯ブラシと全ての型が一致。「同一人物」。', '2026'], f_dna_parent: ['遺体は、汐見修の実の子', 'DNAでは親子。だが、修は71、遺体は60。', '2026'],
  f_arrive: ['匡は1993年11月6日、雨穴の前で保護された', '記憶がない、と言った。巌の手帳。', '1993', 1993, '6日 夜'], f_iwao_saku: ['1993年に「サク」と名乗る旅の刑事', '巌の手帳、11月9日。左の眉に傷。身分証に「令和8年」。', '1993', 1993, '9日'], f_iwao_burn: ['匡の火傷は、1993年11月9日の物', '排水坑で、子どもを助けて腕を焼いた。巌の手帳。', '1993', 1993, '9日'], f_iwao_stop: ['排水坑の件は「調べるな」', '巌の手帳、11月10日。署長の指示。', '1993', 1993, '10日'],
  f_ledger_ren: ['1960年の宿帳に「汐見 蓮　六十」', '昭和35年11月4日。', '1960', 1960, '4日'], f_ledger_saku: ['1960年の宿帳に「三雲 朔　三十八」', '昭和35年11月10日。自分の字に見える。', '1960', 1960, '10日'], f_ledger_box: ['4日の客が箱を預け、10日の客が受け取った', '宿帳の欄外。ハルの字。', '1960', 1960, '4日 / 10日'],
  f_survey: ['第2排水坑は、奥で雨穴につながっている', '蓮の調査。11月4日。', '2026'], f_missing: ['平成5年11月9日の運転日誌だけが、抜けている', '蓮の調査。', '2026'], f_valvemark: ['バルブのハンドルに、布の焼けついた跡', '蓮の調査。古い物。', '2026'],
  f_plate2021: ['征二の右足のプレートは KT-2021-0387', '2021年、大腿骨の骨折の手術。', '2026'], f_watchgift: ['征二の腕時計は、10歳の時に旅の老人からもらった', '「これは、お前のだ」と言われた。本人の話。', '2026'], f_hawk: ['征二の杖の頭は、真鍮の鷹', 'くちばしが、鉤のように曲がっている。先月の写真。', '2026'], f_canefound: ['雨穴の水たまりに、鷹の頭の杖', 'くちばしに、黒いしみ。', '2026'],
  f_gate: ['6日20時52分に征二の車が出て、21時38分に戻った', '屋敷の門の録画。運転は当主。', '2026', 2026, '6日 20:52-21:38'],
  f_iwao_met: ['1993年11月8日、巌に「サク」と名乗った', '身分証を見せた。「令和8年交付」。', '1993', 1993, '8日'], f_tag2025: ['青年の上着のタグは「2025 AW」', '四角い迷路のような印がある。', '1993'], f_reiwa: ['青年の財布に「令和5年」の硬貨', '1993年に、その元号はない。', '1993'], f_id: ['青年の荷物に、汐見蓮の社員証', '霧渕原発。顔写真つき。', '1993'],
  f_noscar: ['11月8日、青年の腕に火傷はない', '薪割りの腕まくり。', '1993', 1993, '8日'], f_skeleton: ['白骨の右足に、金属の板 KT-2021-0387', '1993年10月28日に出た無縁仏。70代の男。死後およそ30年。', '1993'], f_diary: ['1960年11月11日の夜、雨穴から老人', '落盤で重傷。あくる朝、死亡。身元不明。喜一の日誌。', '1960', 1960, '11日 夜'], f_watchboy: ['老人は、少年の征二に腕時計を渡した', '「これは、お前のだ」。喜一の日誌。', '1960', 1960, '11日 夜'],
  f_leak: ['1993年11月9日15時20分、排水坑で配管が破れた', '冷却水。', '1993', 1993, '9日 15:20'], f_close: ['15時41分、部外者が手でバルブを閉めた', '破り捨てられた日誌の頁。', '1993', 1993, '9日 15:41'], f_badge: ['フィルムバッジ3個が、基準をこえた', '作業員3人。', '1993'], f_memo: ['征二の指示「報告不要。記録は破棄」', '副所長の字。', '1993'],
  f_burn: ['青年は、バルブで左腕に三日月形の火傷を負った', '1993年11月9日。焼けた丸いハンドル。', '1993', 1993, '9日 15:41'], f_brow: ['5歳の朔は、排水坑で左の眉を切った', '1993年11月9日。3針。', '1993', 1993, '9日'], f_stay: ['青年は、11日まで動けない', '修の診立て。', '1993', 1993, '9日-11日'], f_watch93: ['1993年の征二も、同じ腕時計をしている', '', '1993'],
  f_noentry: ['11月10日、日誌に老人の記事はまだ無い', '喜一の話。雨穴から出た者は、いない。', '1960', 1960, '10日'], f_scar60: ['箱を預けた客の左腕に、三日月の古い火傷', '「33年あとの傷です」と言った。多恵の話。', '1960', 1960, '4日'], f_nowatch: ['11月10日、少年の征二は腕時計を持っていない', '', '1960', 1960, '10日'], f_blast: ['11月3日の発破で、試掘坑が雨穴に抜けた', 'その日から、穴が鳴る。', '1960', 1960, '3日'],
  f_ledger47: ['作業着№47は11月4日、朽木屋の客に貸した', '鷹取組の台帳。ハル扱い。', '1960', 1960, '4日'], f_box: ['箱の中に、1993年の原本', 'フィルムバッジ、バルブの記録、征二の指示。', '1960'], f_letter: ['匡の手紙「箱は66年前に置く」', '2026年のどこに隠しても、鷹取の手が届く、と。署名は、汐見蓮。', '1960'], f_signed: ['1960年11月10日、宿帳に自分の名を書いた', '三雲朔、38。', '1960', 1960, '10日'],
  f_lime: ['ズボンのすそに、白い石灰の粉', '雨穴の奥の岩の粉だ。死ぬ前に、穴の奥まで入っている。', '遺体'],
  f_nozomu_lost: ['1993年11月9日、望は排水坑から雨穴へ消えた', '湯気をこわがって、奥へ走った。穴の中を探しても、いなかった。', '1993', 1993, '9日 15:20'],
  f_nozomu: ['双子の弟・望は、1993年11月9日に消えた', '5歳だった。机の写真。', '2026'], f_nozomu_stone: ['望の石に、骨は入っていない', '「平成五年十一月九日　行方知れず」。', '2026'], f_rei_nanny: ['玲を育てたのは、ばあやのトキ', '平成5年12月に死んだ。玲が言う前に、何でも分かった。', '2026'], f_rei_pin: ['玲の所長章の裏に「2024　鷹取玲」', '世界に1つしかない。', '2026'],
  f_toki_grave: ['トキは享年74。昭和35年11月より鷹取家に仕えた', '生年、生地は不詳。墓の字。', '2026'], f_closed: ['汐見医院は、8日と9日、休診した', '戸の札。', '2026', 2026, '8日-9日'], f_twin_dna: ['三雲朔と汐見修のDNAは、同一', '同一人物、または一卵性の双子。', '2026'], f_dna_uncle: ['遺体と三雲朔は、おじとおいの間柄', 'DNA鑑定。', '2026'],
  f_adopt: ['汐見修は、昭和35年11月に多恵の養子になった', '実の親は不詳。推定5歳。戸籍。', '2026'], f_seiji_inn: ['5日の夜、朽木屋の前に征二の車', '汐見修が見た。', '2026', 2026, '5日 夜'], f_threat: ['5日の夜、征二は匡をおどした', '「紙を出すな。出せば、娘も無事ではすまん」。匡の日記。', '2026', 2026, '5日 夜'], f_searched: ['宿は3度、探された', '箱は、もう66年前にある。匡の日記。', '2026'], f_toki_will: ['トキの遺言「私の本当の名は、玲」', '平成5年12月。匡にだけ言った。匡の日記。', '1993'],
  f_toki_pin: ['トキの針箱に、所長章「2024　鷹取玲」', '古びて、角が丸い。', '1993'], f_toki_1960: ['トキは、昭和35年11月に雨穴の前で気がついた', 'それより前の記憶はない、と言う。', '1993'], f_toki_confess: ['トキは、2026年から父を追って来た', '父は、着いた夜に死んだ。最後の言葉は「玲、すまない」。', '1993'],
  f_olddoc: ['1993年11月9日、通りがかりの老医師が手伝った', '70ほど。修のくせを知っていた。青年の顔を見て、泣いた。', '1993', 1993, '9日'], f_rx: ['老医師の処方箋の紙に「令和8年」', 'カルテにはさんである。', '1993'], f_busman: ['1993年11月5日、バスの窓から宿を見ていた老人', '60ほど。泣いているようだった。小夜の話。', '1993', 1993, '5日 朝'],
  f_bone_teeth: ['白骨の歯に、白い焼き物の差し歯', '金属を使っていない。1993年には、まだ無い作り。', '1993'], f_bone_ribs: ['白骨の肋骨が、5本折れている', '重い物に、つぶされた。落盤だ。', '1993'], f_bone_wrist: ['白骨の左手首に、時計の跡', '骨に、帯の跡が残る。時計そのものは、無い。', '1993'], f_bone_glass: ['白骨のそばに、とけたガラスの板', '薄い板。中に、細かい金属の線。', '1993'],
  f_found60: ['1960年11月9日、雨穴の前で5つの男の子が拾われた', '名は「のぞむ」。苗字は言えない。多恵があずかった。', '1960', 1960, '9日 夕'], f_child_tag: ['男の子の上着のタグに「1993」', '見た事のない、やわらかい布。', '1960'], f_child_name: ['男の子の上着のえりに「みくも のぞむ」', '子どもの字で書いた名前。', '1960'], f_child_shoes: ['男の子の靴は、布のテープで留める', 'べりべりと、はがれる。1960年には無い。', '1960'], f_woman60: ['1960年11月11日、老人に付き添う女がいた', '40ほど。記憶がないと言う。鷹取の家が引き取った。喜一の日誌。', '1960', 1960, '11日 夜'],
  f_tae_named: ['多恵は、拾った男の子を「汐見修」と名づけた', '1960年11月10日。', '1960', 1960, '10日'],
  h_toki: ['ばあやのトキは、鷹取玲である', '2026年から1960年へ行き、33年を生きた。', '結論'], h_woman: ['老人に付き添った女は、鷹取玲である', '1960年11月11日の夜。', '結論'], h_found: ['拾われた男の子は、汐見修である', '', '結論'], h_twin: ['消えた弟の望は、汐見修である', '1993年から1960年へ。', '結論'], h_olddoc: ['通りがかりの老医師は、71歳の汐見修である', '2026年から、息子に会いに行った。', '結論'], h_bus: ['バスの窓の老人は、朽木匡である', '殺される前の日に、若い妻を見に行った。', '結論'],
  h_ren: ['朽木匡は、汐見蓮である', '2026年から1993年へ行き、33年を生きた。', '結論'], h_muen: ['1960年の無縁仏は、鷹取征二である', '2026年から、1960年へ。', '結論'], h_saku: ['1993年の「旅の刑事」は、自分である', '', '結論'], h_guest: ['1960年に箱を預けた客は、朽木匡である', '', '結論'],
};
/* documents: [title, source, [[label, text, fact]]] */
const DOCS = {
  e_dash: ['蓮の車のドライブレコーダー', '11月6日の夜。登山口。', [['20:41', '登山口に止まる。エンジンが切れる。', 'f_rencar'], ['20:48', '2人の後ろ姿。汐見蓮と、朽木匡。森の道へ歩いていく。', 'f_two'], ['21:04', '別の車のライトが、後ろを通る。車体は、映らない。', 'f_light'], ['21:27', 'また、ライトが通る。こんどは、逆の向き。', 'f_light'], ['21:40', '雨が、ガラスに当たり始める。', null]]],
  e_weather: ['気象の記録', '霧渕の観測点。11月6日。', [['〜21:30', '雨は、ない。0.0ミリ。', null], ['21:40', '降り始め。', 'f_rain'], ['21:40〜', 'あくる朝5時まで、降り続く。', null]]],
  e_entry: ['入退構の記録', '霧渕原発の守衛所。', [['汐見 蓮', '11月6日 18:02　退構。そのあと、記録なし。', 'f_trip'], ['汐見 蓮', '「出張　11月6日〜」。入力は11月7日 8:30。入力者：鷹取 玲。', 'f_trip'], ['朽木 匡', '記録なし。', null]]],
  e_note: ['三雲巌の手帳', '平成5年。父の字。', [['11月6日', '夜、雨穴の前で、若い男を保護。記憶がない。朽木屋にあずける。', 'f_arrive'], ['11月9日', '「サク」と名乗る旅の刑事。県警と言うが、身分証に「令和8年交付」。左の眉に傷。妙に、うちの倅と同じ名。', 'f_iwao_saku'], ['11月9日', '倅が、排水坑でけが。朽木屋の若いのが、腕を焼いて助けた。', 'f_iwao_burn'], ['11月10日', '署長より。「排水坑の件は、調べるな」。', 'f_iwao_stop'], ['11月9日', 'もう1人の倅、望が見つからない。排水坑の奥は、雨穴に抜けている。', 'f_nozomu_lost'], ['11月10日', 'サクは、雨穴に入ったきり、出てこなかった。', null], ['11月12日', '穴の中を3日探した。望は、いない。', null]]],
  e_ledger: ['朽木屋の宿帳', '昭和35年11月。紙は、茶色く焼けている。', [['十一月四日', '汐見 蓮　六十', 'f_ledger_ren'], ['十一月十日', '三雲 朔　三十八', 'f_ledger_saku'], ['欄外', '「四日の客、箱を預ける。十日の客、受け取る」　ハルの字。', 'f_ledger_box']]],
  e_ledger60: ['朽木屋の宿帳', '昭和35年11月。インクが、まだ新しい。', [['十一月四日', '汐見 蓮　六十', 'f_ledger_ren'], ['十一月十日', '（まだ、空いている）', null]]],
  e_dna: ['DNA鑑定書', '県の鑑定所。11月7日。', [['遺体 と 汐見蓮の歯ブラシ', '全ての型が一致。同一人物。', 'f_dna_same'], ['遺体 と 汐見修', '親子。汐見修が、親。', 'f_dna_parent'], ['遺体 と 朽木灯', '親子。遺体が、親。', null], ['年齢', '遺体は60ほど。汐見修は71。汐見蓮は27。', null], ['鑑定所の注', '試料の取り違えを疑い、やり直した。結果は同じ。', null]]],
  e_survey: ['汐見蓮の調査報告', '第2排水坑。11月4日。', [['1', '排水坑は、奥で雨穴につながっている。', 'f_survey'], ['2', '運転日誌は、平成5年11月9日の分だけが、抜けている。', 'f_missing'], ['3', 'バルブのハンドルの縁に、布の焼けついた跡。古い。', 'f_valvemark'], ['所長の書きこみ', '「これ以上、調べない事」。', null]]],
  e_op: ['手術の説明書の控え', '県立病院。2021年3月。', [['患者', '鷹取 征二。', null], ['手術', '右の大腿骨の骨折。金属のプレートで固定。', null], ['プレートの製造番号', 'KT-2021-0387', 'f_plate2021'], ['紹介元', '汐見医院。', null]]],
  e_gate: ['屋敷の門の録画', '11月6日の夜。', [['20:52', '当主の車が出る。運転は、当主。杖を、助手席に置く。', 'f_gate'], ['21:38', '車が戻る。車体は、ぬれていない。当主が降りる。杖が、ない。', 'f_gate'], ['21:45', '書斎に、灯り。', null]]],
  e_meet: ['廃炉委員会の会議の記録', '11月6日。画面の会議。', [['21:45', '鷹取征二、入室。「遅れて、すまない」。', null], ['22:17', '鷹取征二、発言中。', 'f_call'], ['22:30', '終了。', null]]],
  e_file: ['無縁仏の資料', '巌のまとめ。平成5年。', [['発見', '平成5年10月28日。増設工事の現場。森の端。', null], ['骨', '70代の男。死後、およそ30年。', null], ['右の大腿骨', '金属の板が、ねじで留めてある。刻印 KT-2021-0387。', 'f_skeleton'], ['喜一の日誌　昭和35年11月11日', '夜、雨穴より老人。落盤にて重傷。あくる朝、死亡。身元不明。森の端に葬る。', 'f_diary'], ['同じ日誌', '老人は、鷹取の倅・征二（十）に腕時計を渡し、「これは、お前のだ」と言った。', 'f_watchboy'], ['同じ日誌', '同じ夜、老人に付き添う女あり。四十ほど。記憶なしと言う。鷹取の家が引き取る。', 'f_woman60'], ['巌の書きこみ', '「刻印の2021は、年ではあるまい。型の番号か」。', null]]],
  e_belong: ['青年の荷物', '朽木屋の客室。平成5年。', [['上着のタグ', '「2025 AW　再生ポリエステル」。四角い、迷路のような印。', 'f_tag2025'], ['財布の硬貨', '500円玉に、「令和5年」。', 'f_reiwa'], ['社員証', '霧渕原発　汐見 蓮。顔写真つき。', 'f_id'], ['黒い板', 'ガラスと金属の板。押しても、何も映らない。', null]]],
  e_valve: ['破り捨てられた日誌の頁', '第2排水坑。平成5年11月9日。', [['15:20', '冷却水の配管が破れる。', 'f_leak'], ['15:41', '部外者が、手でバルブを閉止。', 'f_close'], ['余白', '副所長より。「外へは、報告しない」。', null]]],
  e_chart: ['汐見医院のカルテ', '平成5年11月9日。', [['青年（氏名不詳、27ほど）', '左の前腕に、三日月形の熱傷。焼けた丸い鉄の縁。', 'f_burn'], ['小児　三雲朔（5）', '左の眉に裂創。3針。', 'f_brow'], ['青年', '歯に、樹脂の詰め物。見た事のない材料。', null], ['診立て', '青年は、11日まで動かさない事。', 'f_stay'], ['はさんである紙', '手伝いの老医師が置いていった処方箋の紙。上に、「令和8年」と刷ってある。', 'f_rx']]],
  e_supply: ['鷹取組の支給品台帳', '昭和35年。作業着。', [['№46', '十一月二日　人夫　佐吉。', null], ['№47', '十一月四日　朽木屋の客人に貸す。ハル扱い。', 'f_ledger47'], ['№48', '未支給。', null]]],
  e_box: ['あずけられた箱', '朽木屋。昭和35年11月4日に置かれた。', [['フィルムバッジ　3個', '平成5年11月9日。基準をこえている。', 'f_box'], ['原本', 'バルブの記録。副所長の指示「報告不要。記録は破棄」。署名、鷹取征二。', 'f_box'], ['手紙', '三雲さん。これを読むころ、私は死んでいるでしょう。誰に殺されるのかは、知りません。知らないまま、若い自分を見送ります。', 'f_letter'], ['手紙', '箱は、66年前に置きます。2026年のどこに隠しても、鷹取の手が届く。昭和35年には、届かない。そして、あなたは必ず、この宿に来る。33年前、あなたが、そう言ったから。', 'f_letter'], ['手紙', '帰りに、平成5年の町をバスで通りました。若い小夜が、宿の前を掃いていました。あしたの夜、若い私が来る。声は、かけませんでした。', null], ['手紙', '灯を、頼みます。　汐見 蓮', null]]],
};
DOCS.e_dna2 = ['DNA鑑定書（追加）', '県の鑑定所。11月11日。', [['遺体 と 三雲朔', 'おじと、おいの間柄。', 'f_dna_uncle'], ['三雲朔 と 汐見修', '全ての型が一致。同一人物、または一卵性の双子。', 'f_twin_dna'], ['鑑定所の注', '担当刑事の試料を、対照として調べた。年齢は、38と71。', null]]];
DOCS.e_koseki = ['汐見修の戸籍の写し', '本人から、あずかった。', [['昭和35年11月20日', '汐見多恵の養子となる。', 'f_adopt'], ['実の親', '不詳。雨穴の前で保護。推定5歳。', 'f_adopt'], ['生年', '昭和30年と、届け出てある。', null]]];
DOCS.e_diary = ['朽木匡の日記', '小夜から、あずかった。33年ぶん。', [['平成5年11月12日', '穴が閉じた。帰れない。汐見先生は、父だ。38歳の父に、私は名のれない。', null], ['平成5年12月', 'トキさんが、死ぬ前に、私を呼んだ。「あなたも、あちらから来た人でしょう。私の本当の名は、玲」。', 'f_toki_will'], ['平成11年4月', '汐見の家に、男の子が生まれた。蓮。……私だ。', null], ['令和8年11月5日', '夜、鷹取の当主が来た。「紙を出すな。出せば、娘も無事ではすまん」。', 'f_threat'], ['同じ日', '宿は、3度、探された。むだだ。箱は、もう、66年前にある。', 'f_searched'], ['令和8年11月6日', '今夜、若い私が行く。見送ったら、小夜に、全部話そう。', null]]];
const EVN = k => k === 'body' ? '遺体の検分' : DOCS[k][0];
/* board: nodes by family column and era row; unknown figures to be identified */
const FAM = ['三雲', '鷹取', '汐見', '朽木'];
const BNODE = [
  { id: 'kiichi', c: 0, e: 1960, f: 'kiichi35', n: '三雲 喜一', s: '駐在　35', k: 'met:kiichi' }, { id: 'iwao', c: 0, e: 1993, f: 'iwao35', n: '三雲 巌', s: '巡査部長　35', k: 'ev:e_note|met:iwao' }, { id: 'saku', c: 0, e: 2026, f: 'saku', n: '三雲 朔', s: '自分　38' },
  { id: 'soichiro', c: 1, e: 1960, f: 'soichiro45', n: '鷹取 宗一郎', s: '鷹取組　45', k: 'met:soichiro' }, { id: 'seiji43', c: 1, e: 1993, f: 'seiji43', n: '鷹取 征二', s: '副所長　43', k: 'met:seiji43' }, { id: 'seiji76', c: 1, e: 2026, f: 'seiji76', n: '鷹取 征二', s: '当主　76', k: 'met:seiji76' }, { id: 'rei', c: 1, e: 2026, f: 'rei', n: '鷹取 玲', s: '所長　41', k: 'met:rei', sub: 1 },
  { id: 'tae', c: 2, e: 1960, f: 'tae30', n: '汐見 多恵', s: '産婆　30', k: 'met:tae' }, { id: 'osamu38', c: 2, e: 1993, f: 'osamu38', n: '汐見 修', s: '医師　38', k: 'met:osamu38' }, { id: 'osamu71', c: 2, e: 2026, f: 'osamu71', n: '汐見 修', s: '院長　71', k: 'met:osamu71' }, { id: 'ren', c: 2, e: 2026, f: 'ren27', n: '汐見 蓮', s: '技師　27　行方不明', sub: 1 },
  { id: 'haru', c: 3, e: 1960, f: 'haru40', n: '朽木 ハル', s: '女将　40', k: 'met:haru' }, { id: 'tadashi27', c: 3, e: 1993, f: 'tadashi27', n: '記憶のない青年', s: '「匡」　27ほど', k: 'f:f_arrive|met:ren' }, { id: 'tadashi60', c: 3, e: 2026, f: 'tadashi60', n: '朽木 匡', s: '遺体　60' }, { id: 'akari', c: 3, e: 2026, f: 'akari', n: '朽木 灯', s: '鑑識　31', sub: 1 },
  { id: 'toki', c: 1, e: 1993, f: 'toki74', n: 'トキ', s: 'ばあや　74', k: 'met:toki|f:f_rei_nanny|f:f_toki_grave', sub: 1 }, { id: 'nozomu', c: 0, e: 1993, f: 'nozomu5', n: '三雲 望', s: '双子の弟　5　行方不明', k: 'f:f_nozomu|f:f_nozomu_lost|f:f_nozomu_stone', sub: 1 },
  { id: 'X7', c: 1, e: 1960, x: 1, n: '老人に付き添う女', s: '40ほど', k: 'f:f_woman60', sub: 1 }, { id: 'X4', c: 2, e: 1960, x: 1, n: '拾われた男の子', s: '5つほど', k: 'f:f_found60', sub: 1 }, { id: 'X6', c: 2, e: 1993, x: 1, n: '通りがかりの老医師', s: '70ほど', k: 'f:f_olddoc', sub: 1 }, { id: 'X8', c: 3, e: 1993, x: 1, n: 'バスの窓の老人', s: '60ほど', k: 'f:f_busman', sub: 1 },
  { id: 'X1', c: 1, e: 1960, x: 1, n: '雨穴から出た老人', s: '無縁仏　70代', k: 'f:f_diary|f:f_skeleton', sub: 1 }, { id: 'X2', c: 0, e: 1993, x: 1, n: '旅の刑事「サク」', s: '左の眉に傷', k: 'f:f_iwao_saku', sub: 1 }, { id: 'X3', c: 3, e: 1960, x: 1, n: '箱を預けた客', s: '60ほど', k: 'f:f_ledger_box|f:f_scar60|f:f_ledger47', sub: 1 },
];
/* identity links: pair of node ids -> hypothesis; need one fact from A and one from B (or any two from A when B is absent) */
const LINKS = [
  { a: ['tadashi60', 'tadashi27'], b: ['ren'], h: 'h_ren', A: ['f_dna_same', 'f_id', 'f_ledger_ren', 'f_dna_parent'], B: ['f_dna_same', 'f_id', 'f_ledger_ren', 'f_dna_parent', 'f_tag2025', 'f_reiwa', 'f_scar', 'f_burn', 'f_iwao_burn', 'f_arrive'], say: '同じDNA。33年ぶんの年の差。……朽木匡は、汐見蓮だ。あの夜、穴に入った若者が、33年かけて、ここへ戻ってきた。' },
  { a: ['X1'], b: ['seiji76', 'seiji43'], h: 'h_muen', pairs: [['f_skeleton', 'f_plate2021'], ['f_watchboy', 'f_watchgift']], say: '足の板の番号が、同じだ。……66年前に死んだ老人は、いま生きている、鷹取征二だ。まだ、行っていないだけだ。' },
  { a: ['X2'], b: ['saku'], h: 'h_saku', A: ['f_iwao_saku'], B: ['f_brow', 'f_iwao_met'], say: '左の眉の傷。「令和8年」の身分証。……親父の手帳の男は、俺だ。読んだ時には、まだ、行っていなかった。' },
  { a: ['X3'], b: ['tadashi60'], h: 'h_guest', A: ['f_ledger47', 'f_scar60', 'f_ledger_ren'], B: ['f_tag', 'f_scar', 'f_absent', 'f_coal', 'f_note', 'f_newcloth'], say: '№47の作業着。三日月の火傷。……箱を預けたのは、殺される2日前の、朽木さんだ。' },
];
LINKS.push(
  { a: ['toki'], b: ['rei'], h: 'h_toki', pairs: [['f_toki_pin', 'f_rei_pin'], ['f_toki_will', 'f_rei_nanny'], ['f_toki_will', 'f_rei_pin'], ['f_toki_confess', 'f_rei_pin'], ['f_toki_will', 'f_toki_pin']], say: '世界に1つの章が、2つある。……ばあやのトキは、鷹取玲だ。玲を育てたのは、年を取った玲、本人だった。' },
  { a: ['X7'], b: ['rei', 'toki'], h: 'h_woman', A: ['f_woman60'], B: ['f_toki_1960', 'f_toki_confess', 'f_toki_grave', 'f_toki_will'], say: '昭和35年の11月。記憶のない、40ほどの女。……老人に付き添って穴を出たのは、玲だ。父親を、追ってきた。' },
  { a: ['X4'], b: ['osamu38', 'osamu71'], h: 'h_found', A: ['f_found60', 'f_tae_named'], B: ['f_adopt', 'f_tae_named'], say: '昭和35年の11月。雨穴の前で拾われた、5つの子。……汐見先生は、多恵さんの産んだ子じゃない。' },
  { a: ['nozomu'], b: ['X4', 'osamu38', 'osamu71'], h: 'h_twin', A: ['f_nozomu_lost', 'f_nozomu', 'f_nozomu_stone'], B: ['f_child_tag', 'f_child_name', 'f_twin_dna'], say: '同じ型。1993年の服。……弟は、あの日、穴を抜けて、33年前に出た。そこで育って、俺より33も年上の、医者になった。' },
  { a: ['X6'], b: ['osamu71'], h: 'h_olddoc', A: ['f_olddoc', 'f_rx'], B: ['f_closed', 'f_rx'], say: '令和8年の紙。医院を閉めた2日。……老医師は、71の汐見先生だ。33年前の息子に、ひと目、会いに行った。' },
  { a: ['X8'], b: ['tadashi60'], h: 'h_bus', A: ['f_busman'], B: ['f_ticket', 'f_absent', 'f_letter'], say: '平成5年11月5日の整理券。……バスの窓の老人は、朽木さんだ。殺される前の日に、25の小夜さんを、見に行った。' });
/* same-person pairs the game already knows (drawn as plain lines) */
const KNOWN = [['seiji43', 'seiji76'], ['osamu38', 'osamu71'], ['tadashi27', 'tadashi60']];
/* words: concept id -> [chip text, other spellings...]; g: group for the helper panel */
const WORDS = {
  人物: { saku: ['三雲朔', '朔', 'みくもさく', '自分', '私', 'わたし', '俺', 'おれ', '僕'], iwao: ['三雲巌', '巌', 'いわお'], kiichi: ['三雲喜一', '喜一', 'きいち'], seiji: ['鷹取征二', '征二', 'せいじ', 'あなた', '当主'], rei: ['鷹取玲', '玲'], soichiro: ['鷹取宗一郎', '宗一郎'], osamu: ['汐見修', '修'], ren: ['汐見蓮', '蓮', 'しおみれん', 'れん'], tae: ['汐見多恵', '多恵'], tadashi: ['朽木匡', '匡', 'ただし'], sayo: ['朽木小夜', '小夜'], akari: ['朽木灯', '灯', 'あかり'], haru: ['朽木ハル', 'ハル'], child: ['子ども', '子供', 'こども', '5歳', '五歳', '幼い'], toki: ['トキ', 'とき', 'ばあや'], nozomu: ['三雲望', '望', 'のぞむ'], mikumo: ['三雲の家', '三雲'] },
  年と時刻: { y1960: ['1960年', '1960', '昭和35', '昭和三十五'], y1993: ['1993年', '1993', '平成5', '平成五'], y1999: ['1999年', '1999', '平成11', '平成十一'], y2026: ['2026年', '2026', '令和8', '令和八'], y1967: ['1967年', '1967', '昭和42'], y1933: ['1933年', '1933', '昭和8年'], d1106: ['11月6日', '6日'], d1109: ['11月9日', '9日'], d1111: ['11月11日', '11日'], d1107: ['11月7日', '7日の朝', '7日'],
    t1520: ['15時20分', '15:20', '1520', '午後3時20分'], t2048: ['20時48分', '20:48', '2048'], t2052: ['20時52分', '20:52', '2052'], t2138: ['21時38分', '21:38', '2138'], t2140: ['21時40分', '21:40', '2140', '9時40分'], t2145: ['21時45分', '21:45', '2145'], t2217: ['22時17分', '22:17', '2217'], y33: ['33年', '三十三年'], y66: ['66年', '六十六年'], y2024: ['2024年', '2024', '令和6'], y2025: ['2025年', '2025', '令和7'], d1105: ['11月5日', '5日'], age5: ['5つ', '5才', '五つ', 'いつつ'] },
  物: { cane: ['杖', 'つえ', 'ステッキ'], hawk: ['鷹の頭', '鷹', 'たか', 'くちばし', '鉤', 'かぎ'], watch: ['腕時計', '時計'], crown: ['りゅうず', '竜頭', 'リューズ', 'リュウズ', '針を合わせ', '針を進め', '針を動か'], jacket: ['作業着', '上着'], tag: ['タグ', '札'], badge: ['フィルムバッジ', 'バッジ'], plate: ['プレート', '金属の板', '金属板', 'KT-2021-0387', 'KT20210387', '番号'], burn: ['火傷', 'やけど', 'ヤケド'], crescent: ['三日月', 'みかづき'], box: ['箱', '原本'], ledger: ['宿帳'], dna: ['DNA', 'ＤＮＡ', 'ディーエヌエー'], valve: ['バルブ', '弁', 'ハンドル'], car: ['車', 'くるま'], gatecam: ['門の録画', '録画', '門', 'カメラ'], dashcam: ['ドライブレコーダー', 'ドラレコ'], soil: ['土', '地面', '下の土'], trail: ['登山口'], forest: ['森'], memo: ['指示', 'メモ'], coin: ['硬貨', '500円玉'], pin: ['所長章', '章', 'ピン'], idcard: ['社員証'] },
  言葉: { same: ['同一人物', '同じ人物', '同じ人', '本人', '自身'], fake: ['偽装', 'わざと', '見せかけ', 'ごまかし', '細工', '嘘'], dry: ['乾いていた', '乾いて', '乾い', 'ぬれていな', '濡れていな'], rainw: ['雨', '降り始め', '降りはじめ'], before: ['より前', '前に', '以前'], hide: ['隠した', '隠し', '隠ぺい', '隠蔽', '口止め', '破棄', 'もみ消'], accident: ['事故', '漏れ', '破れ', '配管'], tunnel: ['排水坑', '第2排水坑'], cave: ['雨穴', '穴', '洞窟'], muen: ['無縁仏', '白骨', '老人', '骨'], trip: ['出張'], added: ['書き足', '後から', 'あとから', '書き加'], two: ['2人', '二人', 'ふたり'], future: ['未来', '33年後', '33年あと'], past: ['過去', '33年前'], boiler: ['ボイラー'], alibi: ['アリバイ', '会議'], motive: ['動機'], suicide: ['自殺'], accident2: ['転んだ', '転落'], adopted: ['拾われた', '拾われ', '拾った', '養子', '捨て子'], sib: ['双子', 'ふたご', '弟', '兄', '兄弟', 'きょうだい'], son: ['息子', 'せがれ', '倅'], die: ['死ぬ', '死ん', '亡くな'], director: ['所長'], name: ['名前', '名が'] },
};
/* battles. round: s statement block, ev accepted items, need: alternatives -> groups -> concept ids, o: block on success, hint */
const BATTLE = {
  B1: { foe: 'rei', title: '所長　鷹取 玲', intro: 'b1_intro', miss: ['b1_m0', 'b1_m1'], end: 'rei26_after', then: 'after_b1', r: [
    { s: 'b1_s1', q: '汐見蓮は、出張中か。', ev: ['f_rencar', 'f_trip', 'e_dash', 'e_entry'], need: [[['car'], ['trail']], [['trip'], ['added', 'd1107']]], o: 'b1_o1', hint: '蓮の車は、どこにあるか。「出張」は、いつ書かれたか。' },
    { s: 'b1_s2', q: '亡くなった匡は、発電所と関係がないか。', ev: ['f_tag'], need: [[['jacket', 'tag'], ['y1960']]], o: 'b1_o2', hint: '遺体の着ている物。どこの、いつの物か。' },
    { s: 'b1_s3', q: '蓮と匡に、接点はないか。', ev: ['f_two', 'e_dash'], need: [[['two'], ['dashcam', 't2048', 'forest']]], o: 'b1_o3', hint: '6日の夜、登山口の車が映した物。' } ] },
  B2: { foe: 'seiji43', title: '副所長　鷹取 征二', intro: 'b2_intro', miss: ['b2_m0', 'b2_m1'], end: 'seiji93_after', r: [
    { s: 'b2_s1', q: '事故は、起きていないか。', ev: ['f_leak', 'e_valve', 'f_close'], need: [[['tunnel', 'accident'], ['t1520', 'accident']]], o: 'b2_o1', hint: '何時に、どこで、何が破れたか。' },
    { s: 'b2_s2', q: '青年の火傷は、宿のボイラーか。', ev: ['f_burn', 'e_chart'], need: [[['valve'], ['burn', 'crescent']]], o: 'b2_o2', hint: '火傷の形と、それを作った物。' },
    { s: 'b2_s3', q: '記録は、どこにも無いか。', ev: ['f_badge', 'f_memo'], need: [[['badge'], ['hide', 'memo']]], o: 'b2_o3', hint: '棚に残った物と、机に残った紙。' } ] },
  B3: { foe: 'haru', title: '朽木屋　ハルの3つの問い', intro: 'b3_intro', miss: ['b3_m0', 'b3_m1'], end: 'haru60_after', noev: 1, r: [
    { s: 'b3_s1', q: '箱を預けた客の、まことの名は。', need: [[['ren']]], strict: 1, o: 'b3_o1', hint: '宿帳に、客は自分で名を書いた。' },
    { s: 'b3_s2', q: '腕の火傷は、いつ、誰をかばって、できた物か。', need: [[['y1993', 'd1109'], ['saku', 'child']]], o: 'b3_o2', hint: '排水坑で起きた事。そこにいた子ども。' },
    { s: 'b3_s3', q: 'あの客が生まれたのは、何年か。', need: [[['y1999']]], strict: 1, o: 'b3_o3', hint: '2026年に、27歳。' } ] },
  B4: { foe: 'osamu71', title: '院長　汐見 修', intro: 'b4_intro', miss: ['b4_m0', 'b4_m1'], end: 'osamu26_after', r: [
    { s: 'b4_s1', q: '修は、多恵の産んだ子か。', ev: ['f_found60', 'f_tae_named', 'h_found', 'f_adopt'], need: [[['adopted'], ['y1960', 'cave', 'tae']]], o: 'b4_o1', hint: '1960年に、多恵があずかった子。' },
    { s: 'b4_s2', q: '修は、どこの子か。', ev: ['f_twin_dna', 'h_twin', 'f_child_name', 'e_dna2'], need: [[['sib', 'nozomu'], ['dna', 'same', 'saku']]], o: 'b4_o2', hint: '鑑定所の、追加の知らせ。' },
    { s: 'b4_s3', q: '8日と9日、修はどこにいたか。', ev: ['f_olddoc', 'f_rx', 'h_olddoc', 'f_closed'], need: [[['y1993', 'past'], ['ren', 'son', 'tadashi']]], o: 'b4_o3', hint: '33年前の医院に、手伝いが1人いた。' } ] },
  B5: { foe: 'sayo58', title: '女将　朽木 小夜', intro: 'b5_intro', miss: ['b5_m0', 'b5_m1'], end: 'sayo26_after', r: [
    { s: 'b5_s1', q: '匡の昔の物は、残っていないか。', ev: ['e_belong', 'f_tag2025', 'f_id', 'f_reiwa'], need: [[['jacket', 'tag', 'idcard', 'coin'], ['y2025', 'y1993', 'ren', 'future']]], o: 'b5_o1', hint: '33年前の客室に、置いてあった物。' },
    { s: 'b5_s2', q: '小夜は、匡が誰かを知らなかったか。', ev: ['h_ren', 'f_dna_same', 'f_id'], need: [[['ren'], ['same', 'tadashi', 'idcard']]], o: 'b5_o2', hint: '社員証に、書いてあった名。' },
    { s: 'b5_s3', q: '5日の夜、宿で何があったか。', ev: ['f_seiji_inn'], need: [[['seiji'], ['car', 'd1105']]], o: 'b5_o3', hint: '汐見先生が、その夜、宿の前で見た物。' } ] },
  B6: { foe: 'toki', title: 'ばあや　トキ', intro: 'b6_intro', miss: ['b6_m0', 'b6_m1'], end: 'toki93_after', r: [
    { s: 'b6_s1', q: 'トキは、ただの女中か。', ev: ['f_toki_pin'], need: [[['pin'], ['y2024', 'future']]], o: 'b6_o1', hint: '針箱の底の物。裏の年。' },
    { s: 'b6_s2', q: '章は、拾い物か。', ev: ['f_toki_pin', 'f_rei_pin'], need: [[['rei'], ['name', 'same', 'pin']]], o: 'b6_o2', hint: '章の裏の、もう1つの字。同じ章を、誰が持っているか。' },
    { s: 'b6_s3', q: '8つの玲は、大きくなったら何になるか。', ev: ['f_rei_pin', 'f_toki_pin'], need: [[['director']]], o: 'b6_o3', hint: '章は、何の章か。' } ] },
  B7: { foe: 'tae', title: '産婆　汐見 多恵の問い', intro: 'b7_intro', miss: ['b7_m0', 'b7_m1'], end: 'tae60_after', noev: 1, r: [
    { s: 'b7_s1', q: '男の子の、名前と歳は。', need: [[['nozomu'], ['age5', 'child']]], o: 'b7_o1', hint: 'えりに書いてある。歳は、双子の兄と同じ。' },
    { s: 'b7_s2', q: '男の子の家は、どこにあるか。', need: [[['y1993', 'future', 'y33'], ['mikumo', 'iwao', 'kiichi']]], o: 'b7_o2', hint: 'いつの、誰の家か。' },
    { s: 'b7_s3', q: '自分は、男の子の何か。', need: [[['sib']]], o: 'b7_o3', hint: '5つの時の写真。' } ] },
  B8: { foe: 'rei', title: '所長　鷹取 玲', intro: 'b8_intro', miss: ['b8_m0', 'b8_m1'], final2: 1, r: [
    { s: 'b8_s1', q: '征二は、どこへ行ったか。', ev: ['h_muen', 'f_skeleton', 'f_diary', 'f_plate2021'], need: [[['y1960', 'y66'], ['muen', 'die']]], o: 'b8_o1', hint: '66年前の墓。' },
    { s: 'b8_s2', q: '穴に入った玲は、どうなるか。', ev: ['h_toki', 'h_woman', 'f_toki_will', 'f_toki_confess'], need: [[['toki'], ['rei', 'same', 'seiji']]], o: 'b8_o2', hint: 'ボードで、ばあやを、いまの誰かとつなぐ。', last: 1 } ] },
  F: { foe: 'seiji76', title: '当主　鷹取 征二', intro: 'final_intro', miss: ['bf_m0', 'bf_m1'], final: 1, r: [
    { s: 'bf_s1', q: '匡が死んだのは、本当に22時17分か。', ev: ['f_dry', 'f_rain', 'e_weather'], need: [[['dry', 'soil'], ['rainw', 't2140']]], o: 'bf_o1', hint: '遺体の下の土。雨は、いつから降ったか。' },
    { s: 'bf_s2', q: '止まった時計は、嘘をつかないか。', ev: ['f_crown'], need: [[['crown'], ['fake', 'watch']]], o: 'bf_o2', hint: '時計の横の、小さな部品。' },
    { s: 'bf_s3', q: '征二は、屋敷を出ていないか。', ev: ['f_gate', 'e_gate'], need: [[['t2052'], ['t2138']], [['gatecam'], ['car']]], o: 'bf_o3', hint: '屋敷の門が、覚えている。' },
    { s: 'bf_s4', q: '凶器と、そこに立った跡は。', ev: ['f_cane', 'f_wound', 'f_hawk', 'f_canefound'], need: [[['cane'], ['hawk']]], o: 'bf_o4', hint: '傷の形と、土の跡。当主が、いつも手にしていた物。' },
    { s: 'bf_s5', q: '征二の動機は、何か。', ev: ['f_box', 'e_box', 'f_memo', 'f_letter', 'f_threat'], need: [[['y1993', 'accident', 'tunnel'], ['hide']]], o: 'bf_o5', hint: '33年前に、当主が隠した物。' },
    { s: 'bf_s6', q: '朽木匡とは、何者か。', ev: ['h_ren', 'f_dna_same', 'f_id'], need: [[['ren'], ['same', 'y33', 'future', 'past', 'tadashi']]], o: 'bf_o6', hint: 'ボードで、2人をつなぐ。' },
    { s: 'bf_s7', q: '穴に入った征二は、どうなるか。', ev: ['h_muen', 'f_skeleton', 'f_plate2021'], need: [[['muen'], ['seiji', 'same'], ['plate']]], o: 'bf_o7', hint: 'ボードで、66年前の老人を、いまの誰かとつなぐ。', last: 1 } ] },
};
if (typeof module !== 'undefined') module.exports = { ERA, NODES, EDGES, OBJ, NPC, FACTS, DOCS, BNODE, LINKS, WORDS, BATTLE, TRIG, FACE, KNOWN };
