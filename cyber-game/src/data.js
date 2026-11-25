/* ---------- game data: evidence, places, showdowns ---------- */
const EVID = {
  tejou:  { n: '伯父の手錠', k: '錠', d: '父の兄が警視庁で30年使った手錠。父から受け取った。' },
  nyutai: { n: '入退室の記録', k: '記', d: '22時14分、三浦部長の職員証でサーバー室に入室。そのあとの出入りは、記録にない。' },
  ransom: { n: '身代金の画面', k: '脅', d: '「あなたの病院は暗号化された。50BTC」。期限は48時間。署名は「ドーン」。' },
  coffee: { n: '飲みかけの缶コーヒー', k: '缶', d: 'サーバー室の机の上。廊下の自販機と同じ銘柄。半分残っている。' },
  kizu:   { n: '曲がった椅子と扉の傷', k: '傷', d: '椅子の脚が曲がっている。扉の内側、取っ手のまわりに新しい傷。' },
  phone:  { n: 'つながらない内線', k: '電', d: 'サーバー室の内線電話。0時ちょうどから、電話の機械ごと止まっている。' },
  kusuri: { n: 'ロッカーの薬', k: '薬', d: '三浦部長の発作の薬。更衣室のロッカーに残っていた。ほとんど減っていない。' },
  counter:{ n: '錠前の回数計', k: '回', d: '記録より2回多く回っている。最後の2回は22時14分のあと。2回の間は数分。' },
  kaibou: { n: '解剖の結果', k: '医', d: '心臓の発作。外傷なし。亡くなったのは朝5時20分ごろ。' },
  nwlog:  { n: 'ネットワークの記録', k: '網', d: '22時31分 外から侵入。23時40分 入退室の記録の機械が止まる。0時 電話。0時5分 扉の制御。' },
  sousa:  { n: '画面の操作の記録', k: '操', d: '0時10分から5時20分まで、三浦部長が1人で暗号化を止めようとしていた。病棟の機械を3つ守った。' },
  jihanki:{ n: '自販機の売上記録', k: '販', d: '地下2階の自販機。あの夜に売れたのは1本だけ。23時42分、缶コーヒー。' },
  remote: { n: '保守の遠隔接続の記録', k: '接', d: '22時31分に入ったのは、保守担当の堀のアカウント。接続元は海外。' },
  pc:     { n: '保守用パソコンの電源記録', k: '源', d: '堀の保守用パソコンは、あの夜、1度も起動していない。' },
  nidan:  { n: '二段階の確認の解除記録', k: '解', d: '1月12日、堀のアカウントだけ二段階の確認が外された。操作は、堀の席のパソコンから。' },
  hensai: { n: '課長の話', k: '話', d: '堀は去年、借金で元気がなかった。1月の半ばに「全部返した」と言った。' },
  darkweb:{ n: 'ダークウェブの出品', k: '売', d: '1月13日の出品。「東京の大学病院。保守の入口。0.3ビットコイン」。1月14日に買い手。' },
  okane:  { n: '送金の流れ', k: '金', d: '0.3ビットコインは日本の取引所の口座へ。1月15日に円で出金。名義は堀健吾。' }
};
const VIEWS = { tsubasa: { n: '翼', d: '物を見て、筋を通す' }, onodera: { n: '小野寺', d: '人に聞く。足で稼ぐ' }, chihaya: { n: '千早', d: '機械と記録を読む' } };
const PLACES = {
  pro: { start: 'kouhei', simple: 1, need: ['f:tv', 'f:miso', 'tejou'], locs: {
    kouhei: { n: '食堂「こうへい」', bg: 'kouhei', people: ['kohei'], hs: [
      { id: 'tv', v: 'any', r: [44, 32, 162, 108], l: 'テレビ', b: 'pro_tv', f: 'tv' },
      { id: 'miso', v: 'any', r: [250, 250, 100, 110], l: '味噌汁', b: 'pro_miso', f: 'miso' },
      { id: 'tsutsumi', v: 'any', r: [402, 300, 118, 76], l: '紙包み', b: 'pro_tsutsumi' }] } } },
  c1: { start: 'rouka', need: ['ransom', 'coffee', 'kizu', 'phone', 'kusuri', 'f:reader', 'f:hijou', 'f:door'], locs: {
    rouka: { n: '地下2階の廊下', bg: 'rouka', people: ['hayase', 'onizuka', 'kanri'],
      hs: [ { id: 'door', v: 'tsubasa', r: [392, 96, 116, 236], l: '扉の錠前', b: 'c1_door', f: 'door' }, { id: 'kabe', v: 'tsubasa', r: [530, 116, 102, 230], l: '外した壁', b: 'c1_kabe' },
            { id: 'jihanki', v: 'tsubasa', r: [244, 146, 74, 138], l: '自販機', b: 'c1_jihanki' }, { id: 'reader', v: 'chihaya', r: [344, 178, 54, 62], l: '入退室の機械', b: 'c1_reader', f: 'reader' } ],
      talk: [ { who: 'kanri', v: 'onodera', tp: [ { l: '三浦さんは、どんな人でしたか', b: 'c1_t_kanri_hito', f: 'lockerhint' }, { l: '扉のしくみを教えてください', b: 'c1_t_kanri_tobira', f: 'hijou' } ] },
              { who: 'onizuka', v: 'tsubasa', tp: [ { l: '鬼塚課長の見立ては', b: 'c1_t_onizuka' } ] }, { who: 'hayase', v: 'tsubasa', tp: [ { l: '身代金の要求について', b: 'c1_t_hayase' } ] } ] },
    server: { n: 'サーバー室', bg: 'server', people: [],
      hs: [ { id: 'monitor', v: 'tsubasa', r: [262, 112, 146, 108], l: 'モニター', b: 'c1_monitor' }, { id: 'coffee', v: 'tsubasa', r: [394, 198, 42, 48], l: '缶コーヒー', b: 'c1_coffee' },
            { id: 'chair', v: 'tsubasa', r: [468, 150, 150, 190], l: '椅子と扉', b: 'c1_chair' }, { id: 'phone', v: 'chihaya', r: [200, 200, 62, 44], l: '内線電話', b: 'c1_phone' },
            { id: 'rack', v: 'chihaya', r: [14, 50, 190, 270], l: 'サーバー', b: 'c1_rack' }, { id: 'tape', v: 'onodera', r: [250, 300, 160, 78], l: '床のテープ', b: 'c1_tape' } ] },
    locker: { n: '更衣室', bg: 'locker', cond: 'f:lockerhint', people: [],
      hs: [ { id: 'locker', v: 'any', r: [282, 66, 84, 258], l: '三浦のロッカー', b: 'c1_locker' }, { id: 'bench', v: 'any', r: [80, 310, 232, 78], l: '長いす', b: 'c1_locker_bench' } ] } } },
  c2: { start: 'kasouken', need: ['kaibou', 'nwlog', 'sousa', 'jihanki', 'f:suufun'], locs: {
    kasouken: { n: '科捜研', bg: 'kasouken', people: ['furukawa', 'shiraishi', 'kiryu'],
      hs: [ { id: 'gear', v: 'any', r: [250, 262, 124, 62], l: '分解した錠前', b: 'c2_gear' }, { id: 'candy', v: 'any', r: [466, 244, 60, 76], l: '飴の瓶', b: 'c2_candy' } ],
      talk: [ { who: 'furukawa', v: 'tsubasa', tp: [ { l: '2回について、ほかに分かる事は', b: 'c2_t_furukawa', f: 'suufun' } ] }, { who: 'kiryu', v: 'tsubasa', tp: [ { l: '解剖の結果は', b: 'c2_t_kiryu' } ] }, { who: 'miyashita', v: 'tsubasa', tp: [ { l: '缶の中身は', b: 'c2_t_miyashita' } ] } ] },
    tokumei: { n: '特命班の部屋', bg: 'tokumei', people: ['sawaguchi', 'mendes'], enter: 'c2miss',
      hs: [ { id: 'logs', v: 'chihaya', r: [46, 76, 228, 148], l: 'ネットワークの記録', b: 'c2_nwlog' }, { id: 'sousa', v: 'chihaya', r: [286, 76, 178, 148], l: 'サーバーの写し', b: s => s.has('nwlog') ? 'c2_sousa' : 'c2_sousa_early', done: 'sousa' }, { id: 'clock', v: 'any', r: [484, 46, 136, 84], l: '2つの時計', b: 'c2_clock' } ],
      talk: [ { who: 'mendes', v: 'tsubasa', tp: [ { l: '段取りを聞く', b: 'c2_t_mendes' } ] } ] },
    rouka: { n: '病院　地下2階の廊下', bg: 'rouka', people: ['kanri'],
      hs: [ { id: 'jihanki2', v: 'onodera', r: [244, 146, 74, 138], l: '自販機', b: 'c2_jihanki' }, { id: 'door2', v: 'tsubasa', r: [392, 96, 116, 236], l: '扉までの距離', b: 'c2_door' } ],
      talk: [ { who: 'kanri', v: 'onodera', tp: [ { l: '三浦さんの、夜の習慣は', b: 'c2_t_kanri' } ] } ] } } },
  c3: { start: 'maker', need: ['pc', 'nidan', 'hensai', 'darkweb', 'okane'], locs: {
    maker: { n: 'メディコア・ジャパン　保守部', bg: 'maker', people: ['hori', 'kacho'],
      hs: [ { id: 'pc', v: 'chihaya', r: [122, 198, 122, 92], l: '堀のパソコン', b: 'c3_pc' }, { id: 'server', v: 'chihaya', r: [22, 84, 88, 212], l: '管理のサーバー', b: 'c3_nidan' },
            { id: 'cabinet', v: 'tsubasa', r: [464, 114, 104, 132], l: 'トークンの棚', b: 'c3_token' }, { id: 'window', v: 'any', r: [246, 36, 198, 120], l: '窓', b: 'c3_window' } ],
      talk: [ { who: 'kacho', v: 'onodera', tp: [ { l: '堀さんは、どんな人ですか', b: 'c3_t_kacho' } ] },
              { who: 'hori', v: 'tsubasa', tp: [ { l: '二段階の確認について', b: 'c3_t_hori_nidan', cond: 'nidan' }, { l: 'お金に困っていませんでしたか', b: 'c3_t_hori_kane' }, { l: '三浦部長との付き合いは', b: 'c3_t_hori_miura' } ] } ] },
    tokumei: { n: '特命班の部屋', bg: 'tokumei', people: ['sawaguchi', 'mendes'], objs: { screenT: 'on' }, hs: [ { id: 'clock3', v: 'any', r: [484, 46, 136, 84], l: '2つの時計', b: 'c2_clock' } ],
      talk: [ { who: 'rosen', v: 'tsubasa', tp: [ { l: 'お金の流れは、どうですか', rep: 1, b: s => !s.has('nidan') ? 'c3_t_rosen0' : !s.has('darkweb') ? 'c3_t_rosen1' : !s.has('hensai') ? 'c3_t_rosen1b' : 'c3_t_rosen2' } ] },
              { who: 'sawaguchi', v: 'any', tp: [ { l: 'ドーンの動きは', b: 'c3_t_sawaguchi' } ] } ] } } }
};
const BATTLES = {
  b1: { foe: 'onizuka', title: '鬼塚の見立てを崩せ', bg: 'rouka', miss: ['b1_miss', 'b1_miss2'], end: 'b1_end', ph: [
    { c: 'b1_c1', t: 'ev', a: 'kusuri', ok: 'b1_o1', h: '発作の持病があるのに、手元になかった物がある。「証拠」から出そう。' },
    { c: 'b1_c2', t: 'ev', a: 'kizu', ok: 'b1_o2', h: '倒れる前に、何かをしようとした跡が、部屋に残っている。「証拠」。' },
    { c: 'b1_c3', t: 'view', a: 'chihaya', ok: 'b1_o3', h: '機械の記録の話だ。「視点」で、機械に強い仲間に代わろう。' },
    { c: 'b1_c4', t: 'ev', a: 'phone', ok: 'b1_o4', h: '助けを呼ぶ道具は、使えたのか。「証拠」。' },
    { c: 'b1_c5', t: 'ded', a: 0, ok: 'b1_o5', h: '「推理」で、起きた事を言い切ろう。', o: ['三浦さんは、あの部屋に閉じこめられていた', '誰かと争って、倒れた', '自分で鍵をかけて、閉じこもった'] } ] },
  b2: { foe: 'onizuka', title: '消えた2回を説明せよ', bg: 'kasouken', miss: ['b2_miss', 'b2_miss2'], end: 'b2_end', ph: [
    { c: 'b2_c1', t: 'ev', a: 'jihanki', ok: 'b2_o1', h: '2回は「出て、戻った」。あの夜、廊下で起きた事の記録がある。「証拠」。' },
    { c: 'b2_c2', t: 'ev', a: 'nwlog', ok: 'b2_o2', h: '記録の機械そのものが、いつ止まったか。「証拠」。' },
    { c: 'b2_c3', t: 'ded', a: 1, ok: 'b2_o3', h: '「推理」で、三浦さんの気持ちを考えよう。', o: ['誰かに脅されて、出られなかった', '攻撃に、まだ気づいていなかった', '席で眠ってしまっていた'] },
    { c: 'b2_c4', t: 'ev', a: 'sousa', ok: 'b2_o4', h: '閉じこめられたあとの5時間の記録がある。「証拠」。' } ] },
  b3: { foe: 'hori', title: '堀の嘘を崩せ', bg: 'maker', miss: ['b3_miss', 'b3_miss2'], end: 'b3_break', ph: [
    { c: 'b3_c1', t: 'ev', a: 'nidan', ok: 'b3_o1', h: '堀のアカウントにだけ、されていた事がある。「証拠」。' },
    { c: 'b3_c2', t: 'ev', a: 'darkweb', ok: 'b3_o2', h: '日付を比べよう。売りに出た日が分かる物を「証拠」で。' },
    { c: 'b3_c3', t: 'obs', a: 'wrist', ok: 'b3_o3', h: '「観察」で、堀の動きを見よう。ある言葉のたびに、どこかが動く。', z: [ { id: 'eyes', l: '目', r: [66, 112, 108, 46] }, { id: 'collar', l: 'えり', r: [84, 204, 72, 40] }, { id: 'wrist', l: '手首', r: [70, 264, 104, 50] } ] },
    { c: 'b3_c4', t: 'view', a: 'onodera', ok: 'b3_o4', h: '人から聞いた話が効く。「視点」で、聞き込みの仲間に代わろう。' },
    { c: 'b3_c5', t: 'ev', a: 'okane', ok: 'b3_o5', h: 'お金がどこへ行ったか。「証拠」。' },
    { c: 'b3_c6', t: 'ded', a: 2, ok: 'b3_o6', h: '「推理」で、堀がした事を正しく言おう。言いすぎても、足りなくてもいけない。', o: ['あなたは、ドーンの一員です', '三浦さんを閉じこめたのは、あなたです', '病院の入口を売ったのは、あなたです'] } ] }
};
const TIMELINE = [ ['三浦部長が、サーバー室に入る', '22:14'], ['外から、侵入される', '22:31'], ['入退室の記録の機械が止まる', '23:40'], ['自販機で、缶コーヒーが売れる', '23:42'], ['内線電話が切れる', '0:00'], ['扉の制御が止まる', '0:05'] ];
if (typeof module !== 'undefined') module.exports = { EVID, PLACES, BATTLES };
