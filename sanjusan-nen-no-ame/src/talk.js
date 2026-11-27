/* ---------- 三十三年目の雨: talking in your own words ---------- */
/* QW: the words a listener understands. A word that starts with '=' is matched as written (no kana folding); the rest go through NORM and a small typo tolerance.
   The reply is chosen from these, in order: a prepared topic (QT) or a sharp question (QA) whose words are all there; a person; a thing; a place; a manner (greeting, thanks ...); and when nothing fits, one of three lines in the listener's own voice with a lead to follow. Nothing here ever costs the player anything. */
const QW = {
  人: { saku: ['三雲朔', '朔', '=サク', 'さくちゃん', 'さくくん', '三雲さん'], iwao: ['三雲巌', '巌', 'いわお', '巡査部長', '岩男', '親父', 'おやじ'], kiichi: ['三雲喜一', '喜一', 'きいち', '貴一', '駐在'],
    seiji: ['鷹取征二', '征二', 'せいじ', '誠二', '正二', '清二', '政治', '誠司', '当主', '副所長', '鷹取さん', '坊ちゃん'], rei: ['鷹取玲', '玲', 'れいさん', 'れいちゃん', 'お嬢さま', 'おじょうさま', 'お嬢さん'], chief: ['所長'],
    soichiro: ['鷹取宗一郎', '宗一郎', 'そういちろう', '総一郎', '先代', '親方'], osamu: ['汐見修', '修', 'おさむ', '汐見先生', '汐見さん', 'お医者', '医者', '先生'],
    ren: ['汐見蓮', '蓮', 'れんくん', 'れんさん', 'しおみれん', '連くん', '廉', 'れんは', 'れんの', 'れんを', 'れんと', 'れんに', 'れんが'], youth: ['青年', 'せいねん', '若いの', '若者', 'わかもの', '若い男', '記憶のない'],
    tae: ['汐見多恵', '多恵', 'たえさん', '産婆', 'さんば', '妙さん', 'たえおば'], tadashi: ['朽木匡', '匡', 'ただしさん', 'ご主人', '朽木さん', '被害者', 'ひがいしゃ', '亡くなった人', '朽木の主人'],
    sayo: ['朽木小夜', '小夜', 'さよさん', 'さよちゃん', '女将', 'おかみ', '沙代'], akari: ['朽木灯', '灯', 'あかり', '明かり', '明り'], haru: ['朽木ハル', '=ハル', 'はるさん', '祖母', 'おばあさん', 'おばあちゃん'],
    toki: ['=トキ', 'ばあや', '婆や', 'ときさん', '乳母'], nozomu: ['三雲望', '望', 'のぞむ', '弟', 'おとうと', '双子', 'ふたご'], muen: ['無縁仏', 'むえんぼとけ', '無縁', '白骨', 'はっこつ', '旅の老人', '骨を', '骨が', '骨は'],
    guest: ['お客', '客', 'きゃく', '泊まった人', '泊まった男'], kid: ['男の子', 'おとこのこ', '拾った子', '拾った男', '拾われた', 'ひろった', 'あの子', '迷子', 'まいご'], olddoc: ['老医師', '年寄りの医者', '通りがかりの医者', '手伝った医者'], busman: ['バスの老人', 'バスの年寄り', 'バスの窓'],
    you: ['あなた', 'あんた', 'きみ', '君は', '君の', 'お前', 'おまえ', '自己紹介', 'ご自身', '自分の事', 'じぶんのこと'],
    father: ['父親', 'お父さん', 'おとうさん', 'お父さま', 'とうちゃん', '父は', '父の', '父を', '父と', '父に', 'パパ'], mother: ['母親', 'お母さん', 'おかあさん', 'お母さま', 'かあちゃん', '母は', '母の', '母を', '母と', '母に', 'ママ'],
    son: ['息子', 'むすこ', '倅', 'せがれ', 'お子さん', '坊や'], daughter: ['娘', 'むすめ'], husband: ['旦那', 'だんな', '亭主', '主人', '連れあい', 'つれあい'], wife: ['妻', '奥さん', '家内', '女房'], grandpa: ['祖父', 'おじいさん', 'おじいちゃん', 'じいさん', 'おじいさま'],
    family: ['家族', 'かぞく', '身内', '兄弟', 'きょうだい', '結婚', '独身', '子どもはいる', '子供はいる'] },
  所: { inn: ['朽木屋', 'くちきや', '宿', '旅館', 'やどや', '帳場'], clinic: ['医院', '病院', '診療所', '産院', 'びょういん'], plant: ['発電所', '原発', 'げんぱつ', 'はつでんしょ', '飯場'], mansion: ['屋敷', 'やしき', '鷹取の家', '鷹取家'],
    police: ['警察', 'けいさつ', '駐在所', '交番'], forest: ['森', '黒檜', 'くろべ', '登山口'], cave: ['雨穴', 'あまあな', '穴', '洞窟', 'どうくつ', 'ほらあな', '洞穴'], tunnel: ['排水坑', 'はいすいこう', '試掘坑', 'しくつこう', 'トンネル', '坑道'],
    grave: ['墓', 'お墓', 'はかば', 'ぼち', 'お寺'], town: ['霧渕', 'きりぶち', 'この町', '町の事', '町について'], bus: ['バス', '停留所'] },
  時: { y1960: ['1960', '昭和35', '昭和三十五'], y1993: ['1993', '平成5', '平成五'], y2026: ['2026', '令和8', '令和八', '未来'], y33: ['33年前', '33年まえ', '三十三年前', '33年'], y66: ['66年前', '66年'],
    lastnight: ['きのう', '昨日', '昨夜', 'ゆうべ', '昨晩', '夕べ'], d4: ['4日'], d5: ['5日前', '5日'], d6: ['6日'], d9: ['9日'], d11: ['11日'], year: ['何年', '元号', '今年', 'ことし', '西暦', '何月', '日付'],
    past: ['昔', 'むかし', '過去', '若いころ', '若い頃', '子どものころ', '子供の頃', '生い立ち', 'おいたち', '小さいころ', '生まれは'] },
  物: { body: ['遺体', '死体', '亡くなった', '殺され', '事件', '現場', 'げんば'], watch: ['腕時計', '時計', 'とけい', 'うでどけい'], cane: ['杖', 'つえ', 'ステッキ'], jacket: ['作業着', 'さぎょうぎ', '上着', 'うわぎ', '着ていた'],
    tag: ['タグ', '47番'], ticket: ['整理券', 'せいりけん', '切符', 'きっぷ'], bill: ['百円札', '100円札', 'お札', '板垣', '古いお金'], coal: ['石炭', 'せきたん'], badge: ['フィルムバッジ', 'バッジ'],
    plate: ['プレート', '金属の板', '足の板', '手術', 'しゅじゅつ', '骨折', 'こっせつ', '右足', '当主の足', '足の骨'], burn: ['火傷', 'やけど', '三日月', 'みかづき', 'ボイラー'], arm: ['腕', 'うでの', 'うでを', 'うでに'], scar: ['傷', 'きず', '怪我', 'けがを', 'けがは', 'けがの'], brow: ['眉', 'まゆ', 'おでこ'],
    box: ['箱', 'はこを', 'はこの', 'はこは', '原本', 'げんぽん'], safe: ['金庫', 'きんこ'], ledger: ['宿帳', 'やどちょう', '台帳'], dna: ['dna', 'ディーエヌエー', '鑑定', 'かんてい', '照らし合わせ', '照合'], toothbrush: ['歯ブラシ', 'はぶらし'], valve: ['バルブ', 'ハンドル'],
    car: ['車', 'くるま', 'ドライブレコーダー', 'ドラレコ'], photo: ['写真', 'しゃしん'], pin: ['所長章', '襟', 'えりの', '章を', '章の', '章は', '針箱', 'はりばこ'], luggage: ['荷物', 'にもつ', '持ち物', 'もちもの', '財布', '黒い板'],
    diary: ['日誌', 'にっし', '日記', 'にっき', '手帳', 'てちょう'], mole: ['ほくろ', '黒子'], record: ['記録', 'きろく', '運転日誌', '書類', '報告', '調査', '調べていた'], accident: ['事故', 'じこ', '漏れ', '配管', '湯気', '蒸気'],
    rain: ['雨が', '雨は', '雨の日', '雨の夜', 'あめ', '天気', '雨について', '雨の事'], quarrel: ['口論', 'こうろん', 'けんか', '喧嘩', '言い争い', 'どなりこ', '怒鳴', 'もめ'],
    gone: ['失踪', '行方不明', 'ゆくえ', 'いなくな', '消えた', '帰らない', '連絡がつかない', '出張', 'しゅっちょう', '居場所', 'いばしょ'], memory: ['記憶', 'きおく', '覚えて', 'おぼえて', '思い出'], meeting: ['会議', 'かいぎ', '廃炉', 'はいろ', '委員会'],
    absent: ['おかしな', 'おかしい', '変わった', 'かわった', '変な', 'へんな', '不思議', 'ふしぎ', '妙な', '異変', '気になる', '近ごろ', '最近', 'さいきん'], seeoff: ['見送り', 'みおくり', '出かけ', '出て行', '出ていっ', '宿を出'],
    stay: ['泊ま', 'とまりたい', 'とまる', '宿泊', '一泊', '休みたい', 'あしたにする', '明日にする', '部屋を'], blast: ['発破', 'はっぱ', '試掘', '鳴る', 'うなる', '低い音'], supply: ['支給品', '支給', 'しきゅう', '貸した', '貸して'],
    dream: ['将来', 'しょうらい', '夢', 'ゆめ', '大きくなったら', 'おおきくなったら'], house: ['この家', 'このお屋敷', '奉公', '仕えて', 'つかえて', 'いつから'], home: ['おうち', 'うちの事', '家に帰', '帰りたい', 'かえりたい'],
    back: ['帰る', '帰り', 'かえる', '戻る', 'もどる', '心配'], raise: ['育て', 'そだて'], injured: ['けが人', '怪我人', 'けがにん', '患者', 'かんじゃ', '診た', 'カルテ', '治療', '手当'], why: ['なぜ', 'なんで', 'どうして', '理由', 'わけを', '目的', 'もくてき'], fuda: ['木の札', '古い札', '札の', 'ふだ', '名札'] },
  聞き方: { who: ['誰', 'だれ', '何者', 'なにもの', 'どなた'], where: ['どこ', '何処', 'どちら'], alibi: ['アリバイ', '何をしてい', 'なにをしてい', '何してた', 'なにしてた', 'どこにい', 'どこへ行', 'どこに行'],
    rel: ['関係', 'かんけい', '知り合い', 'しりあい', '知ってい', '知ってる', 'しってる', 'しってい', 'ご存じ', 'ごぞんじ', '面識', '仲は'], about: ['について', 'のこと', 'の事', '教えて', 'おしえて', '聞かせて', 'きかせて', '話して', 'はなして', '聞きたい', 'ききたい'],
    seen: ['見覚え', 'みおぼえ', '見た事', '見たこと', '心当たり', 'こころあたり'], show: ['見せる', '見せます', 'みせる', '見せた', 'これを見', '見てくれ', '見てください', '見せたい'], look: ['見せて', 'みせて', '見たい', 'みたい'],
    name: ['名前', 'なまえ', 'お名前', '名は'], age: ['何歳', 'なんさい', '年齢', 'ねんれい', 'いくつ', '何才', '歳は'], job: ['仕事', 'しごと', '職業', 'しょくぎょう', '勤め'],
    hello: ['こんにちは', 'こんにちわ', 'こんばんは', 'こんばんわ', 'おはよう', 'はじめまして', '初めまして', 'もしもし', 'よろしく', 'お邪魔', 'おじゃま', 'ごめんください', 'どうも'],
    thanks: ['ありがとう', '有難う', '感謝', '助かった', '助かりました', 'たすかった', '礼を言'], bye: ['さようなら', 'さよなら', '失礼します', 'しつれいします', 'また来', 'またくる', 'じゃあね', 'お元気で', '行ってきます'],
    help: ['ヒント', '何を聞けば', 'なにをきけば', '何を話せば', '何を聞いたら', 'わからない', '分からない', '困った', 'こまった', '手がかり', 'てがかり', 'どうすれば', '糸口', 'いとぐち', 'ほかに', '他に'],
    lie: ['嘘', 'うそ', '本当の事', 'ほんとうのこと', '隠して', 'かくして', '隠し事', 'かくしごと', '正直に'], press: ['問いただ', 'といただ', '論破', 'ろんぱ', '追及', 'ついきゅう', '白状', 'はくじょう', '矛盾', 'むじゅん'],
    rude: ['馬鹿', '=バカ', 'ばかやろう', 'ばかもの', 'あほ', '阿呆', 'うるさい', '黙れ', 'だまれ', '死ね', 'まぬけ', 'ふざけ'], fine: ['元気', 'げんき', '大丈夫', 'だいじょうぶ', '具合', 'ぐあい', 'つらい', '辛い', '悲しい', 'かなしい', 'お悔やみ', 'おくやみ', '体調'] },
};
/* who the listener is, and whom "father", "son" ... mean when said to them */
const QSELF = { akari: 'akari', osamu71: 'osamu', sayo58: 'sayo', rei: 'rei', seiji76: 'seiji', iwao: 'iwao', sayo25: 'sayo', ren: 'ren', ren2: 'ren', osamu38: 'osamu', seiji43: 'seiji', toki: 'toki', rei8: 'rei', nozomu: 'nozomu', kiichi: 'kiichi', haru: 'haru', tae: 'tae', soichiro: 'soichiro', seiji10: 'seiji' };
const QFAM = { akari: { father: 'tadashi', mother: 'sayo' }, osamu71: { son: 'ren', mother: 'tae' }, sayo58: { husband: 'tadashi', daughter: 'akari' }, rei: { father: 'seiji', grandpa: 'soichiro' }, seiji76: { daughter: 'rei', father: 'soichiro' },
  iwao: { father: 'kiichi' }, ren: { father: 'osamu' }, ren2: { father: 'osamu' }, osamu38: { mother: 'tae' }, seiji43: { daughter: 'rei', father: 'soichiro' }, toki: {}, rei8: { father: 'seiji', grandpa: 'soichiro' }, nozomu: { father: 'iwao' },
  kiichi: { son: 'iwao' }, haru: {}, tae: {}, soichiro: { son: 'seiji' }, seiji10: { father: 'soichiro' } };
/* typed words for the prepared topics: groups are split by a space (all needed), words in a group by | (any one) */
const QT = { akari26_night: 'lastnight|d6|seeoff', akari26_ren: 'ren|gone', akari26_dna: 'dna|toothbrush',
  osamu26_quarrel: 'quarrel|d5|tadashi', osamu26_tooth: 'toothbrush|dna', osamu26_plate: 'plate',
  sayo26_night: 'lastnight|d6|seeoff', sayo26_absent: 'absent|d4|d5|coal|safe', sayo26_past: 'past|memory|tadashi', sayo26_ledger: 'ledger',
  rei26_ren: 'ren|gone', rei26_father: 'seiji|meeting', rei26_toki: 'toki|raise|mother', rei26_pin: 'pin|badge', rei26_p4: 'box|record',
  seiji26_night: 'd6|lastnight|alibi|meeting', seiji26_watch: 'watch', seiji26_cane: 'cane', seiji26_tadashi: 'tadashi|body',
  iwao93_file: 'absent|muen|body', iwao93_bones: 'muen show|look|seen', iwao93_ren: 'ren|tadashi|memory|youth', iwao93_son: 'son|saku|nozomu|family', iwao93_after: 'bye|thanks',
  sayo93_luggage: 'luggage', sayo93_bus: 'absent|bus|busman', sayo93_stay: 'stay',
  ren93_why: 'why|tunnel|record', ren93_arm: 'arm|burn|scar', ren93_home: 'y2026|osamu|back',
  osamu93_after: 'injured|burn|accident|olddoc|ren|youth|brow|kid', seiji93_watch: 'watch',
  toki93_house: 'house|mansion|job', toki93_past: 'past|memory|name', rei8_toki: 'toki|mole', rei8_dream: 'dream',
  nozomu60_name: 'name|age|who', nozomu60_home: 'home|iwao|saku|family|father',
  kiichi60_diary: 'diary|muen', kiichi60_son: 'son|iwao|family', kiichi60_guest: 'guest|box|d5|tadashi',
  haru60_guest: 'guest|d5|jacket', tae60_scar: 'guest|burn|scar|arm|d5', tae60_boy: 'kid|nozomu', tae60_family: 'family|son|dream',
  soichiro60_blast: 'tunnel|blast|cave', soichiro60_ledger: 'supply|ledger|jacket|tag', boy60_watch: 'watch', boy60_dream: 'dream|plant' };
/* sharper questions: asked in the player's own words, they bring out a testimony that no button offers. w: weight against a prepared topic that also fits */
const QA = {
  akari: [{ k: 'burn|arm|scar', b: 'q_akari_burn' }], osamu71: [{ k: 'rain', b: 'q_osamu71_rain' }], sayo58: [{ k: 'burn|arm|scar', b: 'q_sayo58_burn', w: 9 }], rei: [{ k: 'mole', b: 'q_rei_mole' }],
  seiji76: [{ k: 'y33|y1993|accident|tunnel', b: 'q_seiji76_1993', w: 9 }], iwao: [{ k: 'cave', b: 'q_iwao_cave' }], sayo25: [{ k: 'name|fuda|tadashi|ren|youth', b: 'q_sayo25_tag' }], ren: [{ k: 'tadashi', b: 'q_ren_tadashi' }],
  osamu38: [{ k: 'tae|mother|past|family', b: 'q_osamu38_past' }], seiji43: [{ k: 'toki|raise', b: 'q_seiji43_toki' }], toki: [{ k: 'mole', b: 'q_toki_mole' }], kiichi: [{ k: 'cave', b: 'q_kiichi_cave' }],
  haru: [{ k: 'fuda|husband|tadashi', b: 'q_haru_tag' }, { k: 'box', b: 'q_haru_box', if: '!b3' }] };
/* helper buttons: one press puts the words into the box */
const QCHIP = {
  聞き方: ['について教えて', 'を知っている？', 'との関係は？', 'はどこにいる？', 'のアリバイは？', 'に見覚えはある？', 'を見せる', 'あなたの事を教えて', 'きのうの夜はどこにいた？', '何か変わった事は？', '何を聞けばいい？', 'ありがとう'],
  人物: { 2026: ['朽木匡', '汐見蓮', '汐見修', '朽木小夜', '朽木灯', '鷹取征二', '鷹取玲', '三雲巌', ['三雲望', 'f:f_nozomu'], ['ばあやのトキ', 'f:f_rei_nanny|met:toki']],
    1993: ['記憶のない青年', '三雲巌', '朽木小夜', '汐見修', '鷹取征二', ['ばあやのトキ', 'met:toki|met:rei8'], ['鷹取玲', 'met:rei8'], '汐見多恵', '朽木ハル', '三雲喜一', ['三雲望', 'f:f_nozomu']],
    1960: ['5日前の客', '朽木ハル', '汐見多恵', '三雲喜一', '鷹取宗一郎', '鷹取征二', ['拾われた男の子', 'f:f_found60|met:nozomu'], ['三雲巌', 'met:kiichi']] },
  場所と時: ['雨穴', '森', '朽木屋', '医院', '発電所', '屋敷', '警察', '排水坑', '墓地', 'きのうの夜', '5日の夜', '6日の夜', '9日', '33年前', '1960年', '1993年', '2026年'],
};
/* testimony: what only a typed question brings out */
Object.assign(FACTS, {
  t_akari_burn: ['匡は火傷を「お前が生まれるための傷」と言った', '灯が小さいころに聞いた。意味は、言わなかった。', '証言'], t_osamu_rain: ['修は、雨の日に、誰かを待っている気がする', '子どものころから、ずっと。誰をかは、分からない。', '証言'],
  t_sayo_boiler: ['匡の火傷は、宿のボイラーの物ではない', '来た時には無かった。3日あとに、包帯をして帰った。小夜の話。', '証言'], t_mole: ['玲とトキは、左手の同じ所に、ほくろがある', '2人で、よく手を並べた。', '証言'],
  t_seiji_noacc: ['征二の言い分：「1993年は、無事故の年だ」', '33年前は副所長。「記録を調べてみたまえ」。', '証言'], t_iwao_cave: ['雨穴は、33年ごとに鳴る', '喜一から巌へ。前は昭和35年。ことしは、3日から鳴っている。', '証言'],
  t_sayo_tag: ['「匡」は、帳場の古い札からもらった名', 'ハルの、亡くなった連れあいの名。', '証言'], t_ren_tadashi: ['2026年の匡は、蓮の子どものころのけがまで知っていた', '好物も。「父より、僕にくわしい」。', '証言'],
  t_osamu38_memory: ['修は、5つより前の事を、何も覚えていない', '母は「雨の日に来た子だ」と笑う。', '証言'], t_seiji43_toki: ['トキは「9日は、排水坑に人を入れるな」と言った', '事故の前の週。征二は、聞かなかった。', '証言'],
  t_kiichi_1927: ['昭和2年にも、雨穴は鳴った', 'その年、村に、身もとの知れない者が2人ふえた。', '証言'], t_haru_tag: ['客は札をなでて言った。「この名に、33年、世話になりました」', '「匡」は、ハルの亡くなった主人の名。札は形見。', '証言'],
});
for (const [h, key, f] of [['h_toki', 'pairs', ['t_mole', 'f_toki_pin']], ['h_toki', 'pairs', ['t_mole', 'f_rei_pin']], ['h_toki', 'pairs', ['t_mole', 'f_rei_nanny']], ['h_guest', 'A', 't_haru_tag'], ['h_found', 'B', 't_osamu38_memory'], ['h_ren', 'B', 't_sayo_boiler'], ['h_ren', 'B', 't_ren_tadashi'], ['h_ren', 'B', 't_akari_burn']]) LINKS.find(L => L.h === h)[key].push(f);
