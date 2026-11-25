/* ---------- case data: places, evidence, facts, hypotheses, interrogations, report ---------- */
const H = (f, inner, z) => `<b class="h" data-f="${f}"${z ? ` data-z="${z}"` : ''}>${inner}</b>`;
const T = (txt, inner, z) => `<b class="h" data-t="${txt}"${z ? ` data-z="${z}"` : ''}>${inner}</b>`;
const row = (cells, f, tag = 'td') => `<tr${f ? ` class="h" data-f="${f}"` : ''}>${cells.map(c => `<${tag}>${c}</${tag}>`).join('')}</tr>`;

/* facts: t = card title, d = what it says, c = category, tl = [lane, start, end] in minutes after 0:00 on 6/7 (negative = the evening before) */
const FACTS = {
  f_board:    { t: '濡れた大理石のまな板', d: '乾いた食器の中で、まな板だけが濡れている。洗って間もない。', c: '現場' },
  f_wound:    { t: '傷の中の白い粉', d: '傷は平たく硬い面でついた。中に大理石と同じ成分の粉。', c: '現場' },
  f_tod:      { t: '死亡は2:00〜2:30', d: '解剖の所見による死亡推定時刻。', c: '現場', tl: ['room', 120, 150] },
  f_addr:     { t: '住所を知るのは4人', d: '真柴、三枝、コール、ライラ。ほかの誰も、この部屋を知らない。', c: '人' },
  f_count:    { t: '錠の裏の回数計は214', d: '機械仕掛けの回数計。かんぬきが動くたびに、1つ進む。', c: '錠' },
  f_log212:   { t: '会社の記録は通算212回', d: 'キーストン社のクラウドに残る操作は212件。夜の最後は19:02の施錠。', c: '錠' },
  f_volt:     { t: '2:13と2:24に電圧の谷', d: '施錠や解錠の時と同じ深さで、電池の電圧が下がる。記録には何もない。', c: '錠', tl: ['room', 133, 144] },
  f_voltS:    { t: '1:57に浅い谷が2つ', d: 'かんぬきは動いていない。通信だけが2度、動いた。', c: '錠', tl: ['room', 117, 118] },
  f_msg158:   { t: '1:58「錠が青く光った」', d: 'アッザームが「N.C.」に送った。「ひとりでに。2度」。', c: '通信', tl: ['room', 118, 119] },
  f_msgMon:   { t: '月曜10時に渡す約束', d: '6月4日、アッザームは「N.C.」に書いた。「パソコンごと渡す」。', c: '通信' },
  f_missed:   { t: 'N.C.から不在着信3回', d: '2:22、2:23、2:41。アッザームは出ていない。', c: '通信', tl: ['cole', 142, 161] },
  f_elev:     { t: '昇降機 2:11上り 2:26下り', d: '2:11に1階から12階へ。2:26に12階から1階へ。', c: '映像', tl: ['hall', 131, 146] },
  f_elev2:    { t: '昇降機 2:54上り 3:03下り', d: '2:54に1階から12階へ。3:03に12階から1階へ。', c: '映像', tl: ['hall', 174, 183] },
  f_lamp:     { t: '2:08〜2:30 灯りが点滅しない', d: '廊下の映像。非常口の灯りは切れかけのはずが、この間だけ、ずっと点いている。', c: '映像', tl: ['hall', 128, 150] },
  f_figure:   { t: '2:55 扉の前に男', d: '廊下の映像。1204の呼び鈴を押し、扉に耳を当てる男。コールだ。', c: '映像', tl: ['cole', 175, 182] },
  f_login:    { t: '2:07 録画機に遠隔接続', d: 'アカウントnpa-add01。接続元203.0.113.77。2:31まで。設定変更が2件。', c: '映像', tl: ['hall', 127, 151] },
  f_two:      { t: '2:11 かごの中に2人組', d: '帽子と口おおいの男が2人。同じ時刻の廊下の映像には、誰もいない。', c: '映像', tl: ['hall', 131, 132] },
  f_bag:      { t: '2:26 ふくらんだ鞄', d: '帰りの鞄に、四角く平たい物が入っている。机から消えたパソコンの大きさ。', c: '映像' },
  f_utc:      { t: '会議記録は協定世界時', d: '欄外の細字。記録の時刻は協定世界時。日本は9時間進んでいる。', c: 'コール' },
  f_confRow:  { t: 'コールの参加 16:58〜17:21', d: '本部の記録の書き方のまま。「早退」と付記がある。', c: 'コール' },
  f_etc:      { t: 'コールの車 2:34 首都高', d: '品川330 す 41-07はコールの車。2:34に芝公園の入口を通った。', c: 'コール', tl: ['cole', 154, 155] },
  f_parkC:    { t: '品川41-07 2:52〜3:05', d: '現場のとなりの駐車場の控え。', c: 'コール', tl: ['cole', 172, 185] },
  f_parkS:    { t: '足立12-88 2:50〜3:06', d: '現場のとなりの駐車場の控え。', c: '三枝', tl: ['saegusa', 170, 186] },
  f_scar:     { t: '足立12-88は警備局の車', d: '登録は警察庁。警備局の公用車。', c: '三枝' },
  f_dipl:     { t: '「外」の車 1:49〜2:29', d: '外交官の車が、犯行の前から後まで、となりの駐車場にいた。', c: '大使館', tl: ['emb', 109, 149] },
  f_gateS:    { t: '三枝 1:31退庁 3:12入庁', d: '当直のはずの三枝は、庁舎を1時間41分、空けている。', c: '三枝', tl: ['saegusa', 91, 192] },
  f_gateM:    { t: '真柴 22:05退庁 翌7:28入庁', d: '真柴は前の晩に庁舎を出て、朝まで戻っていない。', c: '真柴' },
  f_mailR:    { t: 'メールは前夜21:52に予約', d: '2:15に届いた真柴のメール。細字のヘッダに、予約の時刻が残る。', c: '真柴' },
  f_mailIP:   { t: 'メールの送信元 203.0.113.77', d: '真柴のメールを仕込んだ回線の番号。', c: '真柴' },
  f_acct:     { t: 'npa-add01は真柴が作った', d: '届の裏に、手書きの表。写しは管理人室と警備局外事課にもある。', c: '真柴' },
  f_sched:    { t: '予定を知るのはコールと真柴', d: '月曜10時の引き渡し。三枝は知らされていない。', c: '人' },
  f_note:     { t: '三枝のメモ 2:55 呼び鈴', d: '「対象、1204の呼び鈴。応答なし。扉に耳」。三枝は非常階段から見ていた。', c: '三枝', tl: ['saegusa', 175, 183] },
  f_noteHome: { t: '三枝のメモ コールは2:31まで自宅', d: '「1:40 対象宅前。室内灯あり。2:31 対象、車で出る」。', c: '三枝', tl: ['cole', 100, 151] },
  f_khalid:   { t: '外79-41はハリドの車', d: '外務省の台帳。湾岸の国の大使館。使用者は警備担当官K.ハリド。', c: '大使館' },
  f_slip:     { t: '5/28 面会先はハリド', d: '真柴の机の面会票。領事ではなく、警備担当官K.ハリド。', c: '大使館' },
  f_news:     { t: '6/5 真柴の兄が釈放', d: '湾岸の国で8か月拘束されていた会社員。6日朝、成田に着いた。', c: '真柴' }
};
const CATC = { '現場': '#c9824a', '錠': '#4f8dff', '通信': '#3fb7a6', '映像': '#9a7be0', 'コール': '#5aa0ff', '三枝': '#d5a53a', '真柴': '#d96a8a', '大使館': '#5fae6a', '人': '#aab2c2', '仮説': '#e3b54a' };

/* hypotheses: need = alternatives, each a list of cards that must all be joined by string */
const HYPS = {
  h_weapon:    { t: '凶器はまな板。殺害は台所', d: '浴室の事故は、偽装。遺体は運ばれた。', need: [['f_board', 'f_wound']], hint: '台所で見た物と、解剖の細字。' },
  h_ghost:     { t: '記録にない開け閉めが2回', d: '回数計は214。記録は212。差の2回は、どこにも書かれていない。', need: [['f_count', 'f_log212']], hint: '錠には、数字が2つある。' },
  h_time:      { t: '2:13に開き、2:24に閉じた', d: '記録にない2回は、電圧の谷の時刻に起きた。', need: [['h_ghost', 'f_volt']], hint: '記録にない2回は、いつ起きたか。電池は知っている。' },
  h_loop:      { t: '廊下の映像は2:08〜2:30が偽物', d: '人が上がった時刻に誰もいない。灯りも点滅しない。古い映像に差し替えてある。', need: [['f_lamp', 'f_elev'], ['f_lamp', 'f_two']], hint: '点滅しない灯りと、その時刻に動いた物。' },
  h_window:    { t: '実行犯は2人組。2:11〜2:26', d: '2人組が上がり、隠れた鍵で入り、15分で降りた。', need: [['h_time', 'f_two'], ['h_time', 'f_elev']], hint: '錠が開いた時刻と、12階へ上がった者。' },
  h_conf:      { t: 'コールの会議は1:58〜2:21', d: '協定世界時に9時間を足す。2:40までは出ていない。', need: [['f_utc', 'f_confRow']], hint: '会議記録の時刻は、どの時計か。' },
  h_coleLate:  { t: 'コールは2:52に現場へ来た', d: '2:34に首都高。2:52に駐車場。朝まで自宅には、いない。', need: [['f_etc', 'f_parkC']], hint: 'コールの車は、2か所に記録を残した。' },
  h_coleClear: { t: 'コールが来たのは犯行の後', d: '2人組が降りたのは2:26。コールが扉の前に立ったのは2:55。', need: [['h_window', 'f_note'], ['h_window', 'f_figure'], ['h_window', 'f_parkC']], hint: '犯人がいた時刻と、コールが着いた時刻。' },
  h_alibi:     { t: '2:15のメールは仕込み', d: '22:05に庁舎を出た者が、2:15に「庁舎から」送る。前の晩の予約。', need: [['f_mailR', 'f_gateM']], hint: 'メールの細字と、ゲートの記録。' },
  h_same:      { t: '映像の差し替えは真柴の回線', d: '録画機に入った番号と、メールを仕込んだ番号が同じ。', need: [['f_mailIP', 'f_login']], hint: '同じ番号が、2つの紙にある。' },
  h_three:     { t: '3つを持つのは真柴だけ', d: '住所。カメラのアカウント。月曜の予定。三枝は予定を、コールはアカウントを持たない。', need: [['f_addr', 'f_acct', 'f_sched']], hint: '犯行に要る知識は3つ。3枚を、糸でつなぐ。' },
  h_trade:     { t: '兄の釈放と引き換え', d: '5/28にハリドと会う。6/5に兄が釈放。6/7に事件。', need: [['f_slip', 'f_news']], hint: '面会の日付と、新聞の日付。' },
  h_embassy:   { t: '2人組は大使館の車で来た', d: '犯行の間、ハリドの車がとなりにいた。命じたのはハリド。', need: [['f_dipl', 'f_khalid']], hint: '「外」の車の持ち主。' }
};

/* evidence */
const lockFront = () => `<svg viewBox="0 0 760 600" width="760" height="600"><rect width="760" height="600" fill="#2b303c"/>${[...Array(19)].map((_, i) => `<path d="M${i * 40} 0 V600" stroke="#fff" stroke-opacity=".05"/>`).join('')}${[...Array(15)].map((_, i) => `<path d="M0 ${i * 40} H760" stroke="#fff" stroke-opacity=".05"/>`).join('')}
<rect x="40" y="540" width="300" height="26" fill="#f4efe2"/>${[...Array(31)].map((_, i) => `<path d="M${40 + i * 10} 540 v${i % 5 ? 8 : 16}" stroke="#222" stroke-width="1"/>`).join('')}<text x="350" y="560" font-size="14" fill="#cbd2e0">cm</text>
<text x="40" y="44" font-size="18" fill="#cbd2e0" font-weight="700">証拠 第1号　スマートロック（1204号室 玄関）　表</text>
<ellipse cx="380" cy="536" rx="150" ry="12" fill="#000" opacity=".3"/><rect x="280" y="70" width="200" height="450" rx="38" fill="#1b1e26" stroke="#0a0b10" stroke-width="4"/><rect x="290" y="80" width="180" height="430" rx="30" fill="none" stroke="#3a4050" stroke-width="2"/>
<rect x="312" y="104" width="136" height="50" rx="10" fill="#0c0e14"/><g class="h" data-t="操作のたびに光る、青い灯り。……アッザームは「ひとりでに光った」と書いていた。"><circle class="a-ledb" cx="380" cy="129" r="13" fill="#4aa8ff"/><circle class="a-ledb" cx="380" cy="129" r="28" fill="#4aa8ff" opacity=".2"/></g>
${['1', '2', '3', '4', '5', '6', '7', '8', '9', '＊', '0', '＃'].map((d, i) => `<circle cx="${332 + (i % 3) * 48}" cy="${200 + Math.floor(i / 3) * 52}" r="19" fill="#2b3140" stroke="#0a0b10" stroke-width="2"/><text x="${332 + (i % 3) * 48}" y="${207 + Math.floor(i / 3) * 52}" font-size="19" text-anchor="middle" fill="#cbd2e0" font-family="monospace">${d}</text>`).join('')}
<text x="380" y="424" font-size="17" text-anchor="middle" fill="#8a94a8" font-family="monospace" letter-spacing="5">KEYSTONE</text><text x="380" y="446" font-size="11" text-anchor="middle" fill="#5a6274" font-family="monospace" letter-spacing="3">K-7 SMART LOCK</text>
<g class="h" data-t="暗証番号の板。よく押す数字だけ、少しすり減っている。こじ開けた傷は、ない。"><rect x="300" y="176" width="160" height="210" fill="transparent"/></g>
<rect x="250" y="470" width="150" height="24" rx="12" fill="#b9bcc4" stroke="#0a0b10" stroke-width="3"/><circle cx="392" cy="482" r="22" fill="#c9ccd4" stroke="#0a0b10" stroke-width="3"/></svg>`;
const lockBack = () => `<svg viewBox="0 0 760 600" width="760" height="600"><rect width="760" height="600" fill="#2b303c"/>${[...Array(19)].map((_, i) => `<path d="M${i * 40} 0 V600" stroke="#fff" stroke-opacity=".05"/>`).join('')}${[...Array(15)].map((_, i) => `<path d="M0 ${i * 40} H760" stroke="#fff" stroke-opacity=".05"/>`).join('')}
<text x="40" y="44" font-size="18" fill="#cbd2e0" font-weight="700">証拠 第1号　スマートロック　裏</text>
<rect x="280" y="70" width="200" height="450" rx="38" fill="#8f949e" stroke="#0a0b10" stroke-width="4"/>${[[306, 96], [454, 96], [306, 494], [454, 494]].map(p => `<circle cx="${p[0]}" cy="${p[1]}" r="9" fill="#5a606c" stroke="#0a0b10" stroke-width="2"/><path d="M${p[0] - 5} ${p[1]} h10 M${p[0]} ${p[1] - 5} v10" stroke="#0a0b10" stroke-width="2"/>`).join('')}
<g class="h" data-t="電池は単3が4本。……この電池の電圧は、会社のクラウドに記録されるらしい。"><rect x="312" y="118" width="136" height="150" rx="8" fill="#2a2e38" stroke="#0a0b10" stroke-width="3"/>${[0, 1, 2, 3].map(i => `<rect x="${322 + i * 30}" y="130" width="24" height="126" rx="6" fill="${i % 2 ? '#c9a43a' : '#3a3f4c'}" stroke="#0a0b10" stroke-width="2"/><rect x="${329 + i * 30}" y="${i % 2 ? 124 : 256}" width="10" height="6" fill="#b9bcc4"/>`).join('')}</g>
<rect x="306" y="284" width="148" height="92" fill="#f4efe2" stroke="#0a0b10" stroke-width="2"/><text x="314" y="301" font-size="10" fill="#222" font-family="monospace" font-weight="700">KEYSTONE K-7</text><text x="314" y="315" font-size="8" fill="#222" font-family="monospace">S/N K7-2231-0456</text><text x="314" y="327" font-size="8" fill="#222" font-family="monospace">FW 4.2.1  DC6V</text>
<text x="314" y="345" font-size="5" fill="#444" font-family="monospace">BOLT CYCLE (MECH.)</text><g class="h" data-f="f_count" data-z="2"><rect x="312" y="349" width="62" height="16" fill="#0c0e14" stroke="#444"/>${'00214'.split('').map((d, i) => `<rect x="${315 + i * 12}" y="351" width="10" height="12" fill="#f4efe2"/><text x="${320 + i * 12}" y="360.5" font-size="8.5" text-anchor="middle" fill="#111" font-family="monospace" font-weight="700">${d}</text>`).join('')}</g><text x="382" y="358" font-size="4.6" fill="#444" font-family="monospace">かんぬきが動く</text><text x="382" y="364" font-size="4.6" fill="#444" font-family="monospace">たびに1進む</text>
<g class="h" data-t="保守用の端子。封印のシールは、破れていない。……端子を使わずに開ける道が、どこかにある。" data-z="1.6"><rect x="340" y="400" width="80" height="34" rx="5" fill="#2a2e38" stroke="#0a0b10" stroke-width="2"/><rect x="352" y="410" width="56" height="14" fill="#0c0e14"/><rect x="334" y="404" width="92" height="12" fill="#c8382f" opacity=".85" transform="rotate(-8 380 410)"/><text x="380" y="414" font-size="7" text-anchor="middle" fill="#fff" font-weight="700" transform="rotate(-8 380 410)">封印 KEYSTONE</text></g>
<rect x="356" y="456" width="48" height="30" rx="6" fill="#5a606c" stroke="#0a0b10" stroke-width="2"/><text x="380" y="548" font-size="13" text-anchor="middle" fill="#9aa3b5">小さな字は、拡大して読む</text></svg>`;
const phoneDoc = () => `<div class="phone"><div class="ph-top"><span>6:00</span><span>圏内　電池 81%</span></div>
<div class="ph-alarm">アラーム　6:00　鳴動中</div>
<div class="ph-h">メッセージ　N.C.</div>
<div class="ph-day">6月4日（金）</div>
<div class="bub me">${H('f_msgMon', '月曜10時。パソコンごと渡す。場所は、いまの部屋。')}<i>21:10</i></div>
<div class="bub you">了解。それまで連絡は控える。部屋を出るな。<i>21:12</i></div>
<div class="ph-day">6月7日（月）</div>
<div class="bub me">${H('f_msg158', '錠が、ひとりでに青く光った。2度。誰も触っていない。')}<i>1:58　既読 2:21</i></div>
<div class="bub you">いま読んだ。電話に出ろ。<i>2:22</i></div>
<div class="ph-h">通話の履歴</div>
<div class="call">${H('f_missed', '<span class="miss">不在</span> N.C.　2:22')}</div><div class="call">${H('f_missed', '<span class="miss">不在</span> N.C.　2:23')}</div><div class="call">${H('f_missed', '<span class="miss">不在</span> N.C.　2:41')}</div>
<div class="call">${T('前の晩、娘と3分話している。変わった様子は、なかったそうだ。', '発信　ライラ　6月6日 18:40　3分')}</div>
<div class="ph-h">写真</div><div class="call">${T('最後の写真は、6月3日。新聞の切り抜きを写した物。', '6月3日　切り抜き（4枚）')}</div></div>`;
const tbl = (head, rows, cls = '') => `<table class="t ${cls}"><thead>${row(head, null, 'th')}</thead><tbody>${rows.join('')}</tbody></table>`;
const EV = {
  lock: { n: 'スマートロックの本体', k: '物', d: 'キーストン社の電子錠。古川が玄関から外した。', faces: [lockFront, lockBack], fl: ['表', '裏'] },
  phone: { n: 'アッザームのスマホ', k: '機', d: '居間の充電台にあった。中身を千早が写した。', faces: [phoneDoc] },
  video: { n: '廊下のカメラの映像', k: '映', d: '管理人室の録画機から。12階の廊下、6月7日の夜中。', video: 1 },
  loginlog: { n: '録画機の接続記録', k: '紙', d: '誰がいつ、録画機に入ったか。', faces: [() => `<div class="paper typed"><h3>録画機 DVR-1200　接続記録</h3><p class="sub">管理会社 出力　／　対象 6月5日〜7日</p>${tbl(['日時', 'アカウント', '種別', '接続元', '操作'], [
    row(['6/5 08:01:12', 'kanri01', '本体', '—', 'ログイン']), row(['6/5 17:30:40', 'kanri01', '本体', '—', 'ログアウト']), row(['6/6 08:03:55', 'kanri01', '本体', '—', 'ログイン']), row(['6/6 17:28:09', 'kanri01', '本体', '—', 'ログアウト']),
    row(['6/7 02:07:11', 'npa-add01', '遠隔', '203.0.113.77', 'ログイン'], 'f_login'), row(['6/7 02:07:58', 'npa-add01', '遠隔', '203.0.113.77', '設定変更（1件）'], 'f_login'), row(['6/7 02:30:41', 'npa-add01', '遠隔', '203.0.113.77', '設定変更（1件）'], 'f_login'), row(['6/7 02:31:02', 'npa-add01', '遠隔', '203.0.113.77', 'ログアウト'], 'f_login'),
    row(['6/7 07:55:20', 'kanri01', '本体', '—', 'ログイン'])])}<p class="fine">※ この機種は、設定変更の中身を記録しない。</p></div>`] },
  elev: { n: 'エレベーターの運転記録', k: '紙', d: '1基だけの昇降機。いつ、どの階からどの階へ動いたか。', faces: [() => `<div class="paper typed"><h3>昇降機 運転記録</h3><p class="sub">6月6日 22:00 〜 6月7日 8:00</p>${tbl(['日付', '時刻', '出発', '到着'], [
    row(['6/6', '22:41', '1階', '5階']), row(['6/6', '22:58', '5階', '1階']), row(['6/6', '23:12', '1階', '9階']), row(['6/6', '23:40', '9階', '1階']),
    row(['6/7', '02:11', '1階', '12階'], 'f_elev'), row(['6/7', '02:26', '12階', '1階'], 'f_elev'), row(['6/7', '02:54', '1階', '12階'], 'f_elev2'), row(['6/7', '03:03', '12階', '1階'], 'f_elev2'),
    row(['6/7', '05:38', '7階', '1階']), row(['6/7', '07:08', '1階', '12階'])])}<p class="fine">※ 23:40から2:11まで、運転なし。</p></div>`] },
  form: { n: 'カメラ増設の届', k: '紙', d: '5月17日、廊下にカメラを足した時の届。管理人室のとじこみから。', fl: ['表', '裏'], faces: [
    () => `<div class="paper"><h3>防犯設備 増設届</h3><p class="sub">管理組合 御中</p><table class="f"><tr><th>工事日</th><td>2027年5月17日</td></tr><tr><th>場所</th><td>12階 共用廊下 天井</td></tr><tr><th>機器</th><td>ドーム型カメラ 1台。既設の録画機に接続</td></tr><tr><th>届出者</th><td>警察庁 連絡調整室　調整官　真柴</td></tr><tr><th>承認</th><td>警察庁 警備局 外事課　警部　三枝</td></tr><tr><th>理由</th><td>居住者の保護のため（詳細は秘）</td></tr></table><p class="stamp">受付 5.17</p><p class="fine">※ 裏面に控えあり</p></div>`,
    () => `<div class="paper hand"><p>${H('f_acct', '録画機に 追加アカウントを作成<br>　npa-add01　／　初期の合言葉は別紙<br>　遠隔から映像を見られる設定　　真柴')}</p><p>${H('f_acct', '写し　→　管理人室<br>写し　→　警備局 外事課（三枝警部）')}</p><p class="small">※ FBIには渡さない事（警備局の希望）</p></div>`] },
  parking: { n: '駐車場の入出庫控え', k: '紙', d: 'マンションのとなりのコインパーキング。', faces: [() => `<div class="paper typed"><h3>コインパーキング 入出庫控え</h3><p class="sub">6月6日 18:00 〜 6月7日 8:00</p>${tbl(['車番', '入庫', '出庫', '料金'], [
    row(['練馬 501 ね 30-15', '6/6 19:20', '6/6 21:05', '600円']), row(['品川 300 て 77-02', '6/6 22:10', '6/6 23:48', '600円']),
    row(['外 79-41', '6/7 01:49', '6/7 02:29', '300円'], 'f_dipl'), row(['足立 500 は 12-88', '6/7 02:50', '6/7 03:06', '300円'], 'f_parkS'), row(['品川 330 す 41-07', '6/7 02:52', '6/7 03:05', '300円'], 'f_parkC')])}<p class="fine">※ 車番は入口のカメラが読み取った物。</p></div>`] },
  elcam: { n: 'かごの中の写真', k: '映', d: 'エレベーターの会社の機械に残っていた。廊下のカメラとは、別の会社の物。', fl: ['2:11', '2:26'], faces: [() => elcamSVG(0), () => elcamSVG(1)] },
  conf: { n: '会議の接続記録', k: '紙', d: 'FBI本部から取り寄せた。真柴が手配した。', faces: [() => `<div class="paper typed en"><h3>SECURE VIDEO CONFERENCE — SESSION LOG</h3><p class="sub">Session WFO-TKY-0606-17　／　Host: WASHINGTON FIELD OFFICE　／　Scheduled 17:00 – 17:40</p>${tbl(['PARTICIPANT', 'SITE', 'JOIN', 'LEAVE', 'NOTE'], [
    row(['A. REYNOLDS', 'WFO', '16:55:10', '17:41:02', 'host']), row(['N. COLE', 'TOKYO', '16:58:04', '17:21:37', 'left early（早退）'], 'f_confRow'), row(['M. ORTIZ', 'WFO', '16:59:48', '17:41:00', '']), row(['J. PARK', 'HQ', '17:00:31', '17:40:58', ''])])}<p class="fine tiny">${H('f_utc', 'All timestamps in UTC (Coordinated Universal Time). 記録の時刻は全て協定世界時。', 1.8)}</p></div>`] },
  gate: { n: '庁舎ゲートの通過記録', k: '紙', d: '総監の名前で全件を出させた。6月6日の夜から7日の朝。', faces: [() => `<div class="paper typed"><h3>警察庁 庁舎ゲート 通過記録</h3><p class="sub">6月6日 21:00 〜 6月7日 8:00　／　長官命令 第27-061号により全件出力</p>${tbl(['時刻', '職員番号', '氏名', '区分'], [
    row(['21:12', 'K-20417', '野々村　係長', '退庁']), row(['21:40', 'G-11802', '三枝　警部', '入庁（当直）']), row(['22:05', 'R-00713', '真柴　調整官', '退庁'], 'f_gateM'), row(['22:31', 'K-31150', '堀　主任', '退庁']), row(['23:02', 'S-40221', '宇野　技官', '退庁']),
    row(['23:47', 'K-20991', '久我　警部補', '入庁']), row(['00:15', 'K-20991', '久我　警部補', '退庁']), row(['01:31', 'G-11802', '三枝　警部', '退庁'], 'f_gateS'), row(['03:12', 'G-11802', '三枝　警部', '入庁'], 'f_gateS'),
    row(['05:50', 'X-00092', '清掃（委託）', '入庁']), row(['06:45', 'K-31150', '堀　主任', '入庁']), row(['07:28', 'R-00713', '真柴　調整官', '入庁'], 'f_gateM'), row(['07:52', 'S-00031', '雪　秘書', '入庁'])])}</div>`] },
  autopsy: { n: '解剖の所見', k: '紙', d: '科捜研の桐生が出した速報。', faces: [() => `<div class="paper"><h3>解剖所見（速報）</h3><p class="sub">科学捜査研究所　桐生</p><table class="f"><tr><th>対象</th><td>男性　58歳</td></tr><tr><th>死亡推定</th><td>${H('f_tod', '6月7日　2:00 〜 2:30')}</td></tr><tr><th>死因</th><td>頭部の打撲による急性硬膜下血腫</td></tr><tr><th>創</th><td>右の側頭部に1か所。当たった面は平たく、辺は直線。丸みのある物では、できない。</td></tr><tr><th>その他</th><td>手と腕に、防ごうとした傷なし。横か後ろからの一撃。</td></tr><tr><th>着衣</th><td>背中に、床を引きずった擦れ。</td></tr></table><p class="fine tiny">${H('f_wound', '微物：創の中に白色の微粒子。主成分は炭酸カルシウム。大理石の成分と一致する。', 1.8)}</p></div>`] },
  locklog: { n: '錠の操作記録', k: '紙', d: 'キーストン社のクラウドに残っていた記録。', faces: [() => `<div class="paper typed"><h3>KEYSTONE CLOUD　操作記録</h3><p class="sub">機器 K7-2231-0456（港区 1204）　／　${H('f_log212', '通算の操作回数：212（6月7日 7:11まで）')}</p>${tbl(['日時', '操作', '方法'], [
    row(['6/5 09:14', '解錠', '暗証番号']), row(['6/5 09:15', '施錠', '自動']), row(['6/6 10:02', '解錠', '内側のつまみ']), row(['6/6 10:03', '施錠', '自動']), row(['6/6 18:55', '解錠', '暗証番号']), row(['6/6 19:02', '施錠', '内側のつまみ'], 'f_log212'), row(['6/7 07:11', '解錠', 'アプリ（共有鍵 L.A.）'])])}<p class="fine">※ かんぬきが動くたびに、1件を記録する。</p></div>`] },
  volt: { n: '電池の電圧の記録', k: '図', d: '錠の電池の電圧。1分ごとにクラウドへ送られていた。', faces: [() => voltSVG()] },
  mail: { n: '真柴のメール', k: '紙', d: '6月7日の2:15に、総監あてに届いていた。雪が印刷した。', faces: [() => `<div class="paper"><table class="f"><tr><th>差出人</th><td>真柴（連絡調整室）</td></tr><tr><th>宛先</th><td>総監</td></tr><tr><th>日時</th><td>2027年6月7日（月）2:15</td></tr><tr><th>件名</th><td>【至急】合同会議の資料（修正版）</td></tr></table><p>総監<br>夜分に失礼します。庁舎で仕上げた資料を、お送りします。<br>あすの合同会議の前に、目を通していただければ幸いです。<br>FBI側の席は、コール駐在官の希望で変えてあります。</p><p>連絡調整室　真柴</p><p class="fine tiny">X-Mailer: NPA-Mail 6.1<br>${H('f_mailR', 'X-Scheduled-At: 2027-06-06 21:52:30 +0900　（予約送信の設定時刻）', 1.8)}<br>${H('f_mailIP', 'X-Originating-IP: 203.0.113.77', 1.8)}<br>Received: 2027-06-07 02:15:00 +0900</p></div>`] },
  note: { n: '三枝の監視メモ', k: '紙', d: '三枝が出した。コールを見張っていた夜の走り書き。', faces: [() => `<div class="paper hand"><p>6/7　対象：FBI駐在官</p><p>${H('f_noteHome', '1:40　対象宅（麻布）前に着く。室内灯あり。<br>〜2:31　外出なし。<br>2:31　対象、車で出る。')}</p><p>2:34　首都高 芝公園入口。<br>　　　行き先は港区1204と判断。先回り。</p><p>2:50　となりの駐車場。非常階段で12階へ。</p><p>${H('f_note', '2:55　対象、1204の呼び鈴。応答なし。扉に耳。<br>3:03　対象、降りる。')}</p><p>3:06　離脱。</p></div>`] },
  carlist: { n: '外交団の車両台帳', k: '紙', d: '外務省から届いた。「外」の車の持ち主。', faces: [() => `<div class="paper typed"><h3>外交団車両台帳（抜粋）</h3><p class="sub">外務省 儀典官室　／　照会番号 27-儀-1182</p>${tbl(['車番', '所属', '使用者', '車'], [
    row(['外 79-12', '■■■国 大使館', '大使', '黒 セダン']), row(['外 79-40', '■■■国 大使館', '領事', '銀 セダン']), row(['外 79-41', '■■■国 大使館', '警備担当官 K.ハリド', '黒 ワゴン'], 'f_khalid'), row(['外 79-43', '■■■国 大使館', '通商担当', '白 セダン'])])}<p class="fine">※ 外交官とその車は、日本の警察が強制的に調べる事ができない。</p></div>`] },
  slip: { n: '大使館の面会票', k: '紙', d: '真柴の机の引き出しにあった。', fl: ['表', '裏'], faces: [
    () => `<div class="paper"><h3>来訪者票　VISITOR</h3><p class="sub">■■■国 大使館</p><table class="f"><tr><th>日時</th><td>2027年5月28日　14:00</td></tr><tr><th>来訪者</th><td>真柴（警察庁）</td></tr><tr><th>面会先</th><td>${H('f_slip', '警備担当官　K.ハリド')}</td></tr><tr><th>用件</th><td>領事相談</td></tr></table><p class="stamp">入館</p></div>`,
    () => `<div class="paper hand"><p>${T('ハリドの字だろうか。釈放の日取りが、面会票の裏に書いてある。', '6/5　釈放<br>6/6　7:40　成田')}</p><p class="small">約束は守る。そちらも。</p></div>`] },
  news: { n: '6月6日の朝刊', k: '紙', d: '真柴の机の横にあった。赤い丸がついている。', faces: [() => `<div class="paper news"><h3>拘束の邦人男性、8か月ぶり解放</h3><p class="sub">湾岸の国　「容疑は晴れた」と当局</p><p>${H('f_news', '湾岸の国で昨年10月から拘束されていた会社員、真柴修さん（52）が5日、解放された。6日朝の便で成田に着く。')}</p><p>真柴さんは商談のため入国し、空港で拘束された。容疑の中身は公表されていない。外務省は「申し入れを続けてきた」としている。</p><p class="fine">弟は警察庁の職員。「家族として、ただ安心している」と話した。</p></div>`] }
};
function elcamSVG(k){ const t = k ? '02:26:14' : '02:11:32', bag = k ? `<path d="M470 296 h86 q10 0 10 10 v58 q0 10 -10 10 h-86 q-10 0 -10 -10 v-58 q0 -10 10 -10Z" fill="#2a2c34" stroke="#111" stroke-width="3"/><rect x="474" y="306" width="78" height="56" fill="#3a3f4c" opacity=".7"/>` : `<path d="M470 300 h86 v70 h-86Z" fill="#2a2c34" stroke="#111" stroke-width="3"/><path d="M470 300 l43 -6 l43 6" fill="none" stroke="#111" stroke-width="3"/>`;
  const man = (x, y, s) => `<g transform="translate(${x} ${y}) scale(${s})"><path d="M-70 250 q0 -120 70 -130 q70 10 70 130Z" fill="#30333c" stroke="#111" stroke-width="3"/><circle cx="0" cy="70" r="46" fill="#c9b09a" stroke="#111" stroke-width="3"/><path d="M-48 60 q48 -70 96 0 l14 4 q-62 -30 -124 0Z" fill="#1c1e26" stroke="#111" stroke-width="3"/><path d="M-40 78 q40 14 80 0 v30 q-40 22 -80 0Z" fill="#e9e6de" stroke="#111" stroke-width="2"/></g>`;
  return `<svg viewBox="0 0 760 480" width="760" height="480"><rect width="760" height="480" fill="#23262c"/><polygon points="120,40 640,40 720,460 40,460" fill="#3a3e46"/><polygon points="200,40 560,40 600,300 160,300" fill="#4a4f58"/><path d="M380 40 v260" stroke="#2a2d34" stroke-width="4"/><rect x="590" y="140" width="34" height="90" fill="#2a2d34"/>${[0, 1, 2, 3].map(i => `<circle cx="607" cy="${156 + i * 20}" r="5" fill="${i === 0 ? '#ffb347' : '#555'}"/>`).join('')}
  <g class="h" data-f="f_two"><rect x="226" y="170" width="320" height="120" fill="transparent"/>${man(300, 150, 1)}${man(470, 130, 1.05)}</g><g class="h" data-${k ? 'f="f_bag"' : 't="平たい鞄。中身は、ほとんど入っていないように見える。"'}>${bag}</g>
  ${[...Array(40)].map((_, i) => `<path d="M0 ${i * 12} H760" stroke="#000" stroke-opacity=".18"/>`).join('')}<rect width="760" height="480" fill="#7fd0ff" opacity=".05"/><text x="24" y="34" font-size="18" fill="#e9f3ff" font-family="monospace">EV-CAM 1　2027/06/07 ${t}</text><text x="736" y="462" font-size="14" fill="#e9f3ff" font-family="monospace" text-anchor="end">行先 ${k ? '1F' : '12F'}</text></svg>`; }
function voltSVG(){ const x = m => 70 + (m + 360) / 840 * 640, y = v => 330 - (v - 5.6) / .6 * 250; // m: minutes after 0:00 (from 18:00 to 08:00)
  const dips = [[-305, .34], [-298, .34], [117, .08], [117.6, .08], [133, .34], [144, .34], [431, .34]]; let d = `M${x(-360)} ${y(6.1)}`;
  for (let m = -360; m <= 480; m += 2){ let v = 6.1 - (m + 360) / 840 * .05 + Math.sin(m * .7) * .004; d += ` L${x(m).toFixed(1)} ${y(v).toFixed(1)}`; for (const q of dips) if (q[0] >= m && q[0] < m + 2) d += ` L${x(q[0]).toFixed(1)} ${y(v - q[1]).toFixed(1)} L${x(q[0] + .8).toFixed(1)} ${y(v).toFixed(1)}`; }
  let ax = ''; for (let h = -6; h <= 8; h++) ax += `<path d="M${x(h * 60)} 80 V330" stroke="#23202a" stroke-opacity=".12"/><text x="${x(h * 60)}" y="350" font-size="11" text-anchor="middle" fill="#23202a" font-family="monospace">${(h + 24) % 24}:00</text>`;
  for (const v of [5.7, 5.8, 5.9, 6.0, 6.1]) ax += `<path d="M70 ${y(v)} H710" stroke="#23202a" stroke-opacity=".12"/><text x="62" y="${y(v) + 4}" font-size="11" text-anchor="end" fill="#23202a" font-family="monospace">${v.toFixed(1)}V</text>`;
  const lab = (m, v, txt) => `<text x="${x(m)}" y="${y(v) + 9}" font-size="4.6" text-anchor="middle" fill="#23202a" font-family="monospace">${txt}</text>`;
  const hot = (m0, m1, attr) => `<rect class="h" ${attr} x="${x(m0) - 7}" y="${y(6.12)}" width="${x(m1) - x(m0) + 14}" height="${y(5.66) - y(6.12)}" fill="transparent"/>`;
  return `<svg viewBox="0 0 760 420" width="760" height="420"><rect width="760" height="420" fill="#f4efe2"/><text x="40" y="40" font-size="20" font-weight="800" fill="#23202a">電池電圧の記録　K7-2231-0456</text><text x="40" y="62" font-size="12" fill="#55525e">6月6日 18:00 〜 6月7日 8:00　／　1分ごと　／　かんぬきを動かすと、深い谷ができる</text>${ax}<path d="${d}" fill="none" stroke="#2456c8" stroke-width="1.6" stroke-linejoin="round"/>
  ${lab(-305, 5.72, '18:55')}${lab(-292, 5.72, '19:02')}${lab(117, 5.99, '1:57')}${lab(131, 5.72, '2:13')}${lab(146, 5.72, '2:24')}${lab(431, 5.72, '7:11')}
  ${hot(-305, -298, 'data-t="18:55と19:02。操作記録にも、同じ時刻の解錠と施錠がある。これが普通の谷の深さだ。" data-z="1.6"')}${hot(116, 119, 'data-f="f_voltS" data-z="1.8"')}${hot(133, 144, 'data-f="f_volt" data-z="1.8"')}${hot(429, 433, 'data-t="7:11。ライラがアプリで開けた時の谷。記録にもある。" data-z="1.6"')}
  <text x="40" y="396" font-size="11" fill="#55525e">谷の横の小さな字が、時刻。拡大して読む。</text></svg>`; }

/* places */
const DAYS = ['', '6月7日（月）', '6月8日（火）', '6月9日（水）'];
const LOCS = {
  genkan: { n: '1204号室　玄関', g: '現場', bg: 'genkan', bgm: 'invest', people: [{ id: 'onizuka', tp: [{ l: '現場の見立て', b: 't_oni_2' }, { l: '大使館の動き', b: 't_oni_1' }] }],
    hs: [{ id: 's_lock', a: 'lock', z: 2.6 }, { id: 's_door_chain', a: 'chain', z: 2.6 }, { id: 's_shoes', a: 'shoes', z: 2.2 }, { id: 's_gshelf', a: 'shelf', z: 1.9 }, { id: 's_door', a: 'door', z: 1.7 }] },
  living: { n: '1204号室　居間と台所', g: '現場', bg: 'living', bgm: 'invest', people: [{ id: 'laila', tp: [{ l: 'この部屋のこと', b: 't_laila_1' }, { l: 'お父さんの約束', b: 't_laila_2' }, { l: '「N.C.」という名前', b: 't_laila_3', cond: g => g.ev.includes('phone') }] }],
    hs: [{ id: 's_phone', a: 'phone', z: 2.6 }, { id: 's_desk', a: 'desk', z: 2.2 }, { id: 's_cork', a: 'cork', z: 2.4 }, { id: 's_board', a: 'board', z: 4, zone: 'kitchen' }, { id: 's_cup', a: 'cup', z: 4, zone: 'kitchen' }, { id: 's_rack', a: 'rack', z: 4, zone: 'kitchen' }, { id: 's_kettle', a: 'kettle', z: 4, zone: 'kitchen' },
      { id: 'z_kitchen', a: 'kitchen', z: 2.5, enter: 'kitchen', l: '台所' }, { id: 's_sofa', a: 'sofa', z: 1.8 }, { id: 's_window', a: 'window', z: 1.7 }, { id: 's_rug', r: [420, 700, 760, 150], z: 1.6 }] },
  bath: { n: '1204号室　浴室', g: '現場', bg: 'bath', bgm: 'invest', people: [],
    hs: [{ id: 's_tub', a: 'tub', z: 2.6 }, { id: 's_drain', a: 'drain', z: 2.6 }, { id: 's_floor', a: 'floor', z: 1.6 }, { id: 's_towel', a: 'towel', z: 2 }, { id: 's_bwin', a: 'window', z: 2.2 }, { id: 's_mirror', a: 'mirror', z: 2.4 }] },
  hall: { n: '12階の廊下', g: '現場', bg: 'hall', bgm: 'invest', people: [{ id: 'mashiba', cond: g => !g.flags.mid, tp: [{ l: 'この部屋を選んだ理由', b: 't_mashiba_3' }, { l: 'コール駐在官の夜', b: 't_mashiba_1' }, { l: '三枝警部の夜', b: 't_mashiba_2' }] }],
    hs: [{ id: 's_cam', a: 'cam', z: 3.2 }, { id: 's_lamp', a: 'lamp', z: 3 }, { id: 's_elev', a: 'elev', z: 1.9 }, { id: 's_1204', a: 'door1204', z: 1.5 }, { id: 's_ext', a: 'ext', z: 2.2 }] },
  kanri: { n: '管理人室', g: '現場', bg: 'kanri', bgm: 'invest', people: [{ id: 'kanrinin', tp: [{ l: 'ゆうべのこと', b: 't_kanri_1' }, { l: 'となりの駐車場', b: 't_kanri_2' }, { l: '5月に来た警察の人', b: 't_kanri_3' }] }],
    hs: [{ id: 'k_aid', a: 'aid', z: 4 }, { id: 'k_monitor', a: 'monitor', z: 2.6 }, { id: 'k_rec', a: 'rec', z: 1.8 }, { id: 'k_shelf', a: 'shelf', z: 1.9 }, { id: 'k_keys', a: 'keys', z: 2.6 }] },
  soukan: { n: '総監室', g: '霞が関', bg: 'soukan', bgm: 'calm', day: 2, people: [{ id: 'yuki', tp: [{ l: '両方からの指示', b: 't_yuki_1' }, { l: '真柴という人', b: 't_yuki_2' }] }], hs: [{ id: 'desk', a: 'desk', z: 1.5, desk: 1 }] },
  keibi: { n: '警備局の一室', g: '霞が関', bg: 'keibi', bgm: 'tension', day: 2, people: [{ id: 'saegusa', tp: [{ l: '尋問する', intr: 'B', cond: g => !g.intr.B.clear }, { l: 'あの夜の話をもう1度', b: 'b_end', cond: g => g.intr.B.clear }] }], hs: [{ id: 'kb_cab', a: 'cab', z: 1.8 }, { id: 'kb_win', a: 'window', z: 1.9 }] },
  kasouken: { n: '科捜研', g: '霞が関', bg: 'kasouken', bgm: 'calm', day: 2, people: [{ id: 'kiryu', tp: [{ l: '傷のこと', b: 't_kiryu' }] }, { id: 'furukawa', tp: [{ l: '錠のこと', b: 't_furu' }] }], hs: [{ id: 'ks_tray', a: 'tray', z: 2.4 }] },
  cyber: { n: 'サイバー課', g: '霞が関', bg: 'cyber', bgm: 'calm', day: 2, people: [{ id: 'sawaguchi', tp: [{ l: '駐車場の車番', b: 't_sawa_car', cond: g => g.ev.includes('parking') }, { l: '録画機の接続元', b: 't_sawa_ip', cond: g => g.ev.includes('loginlog') }] }, { id: 'chihaya', tp: [{ l: 'キーストン社の更新', b: 't_chi_1' }] }], hs: [] },
  renraku: { n: '連絡調整室', g: '霞が関', bg: 'renraku', bgm: 'tension', day: 3, people: [{ id: 'mashiba', cond: g => g.flags.repOK && !g.intr.C.clear, tp: [{ l: '尋問する', intr: 'C' }] }],
    hs: [{ id: 'r_desk', a: 'desk', z: 2.6 }, { id: 'r_news', a: 'news', z: 2.6 }, { id: 'r_photo', a: 'photo', z: 3 }, { id: 'r_cal', a: 'cal', z: 3.2 }, { id: 'r_shelf', a: 'shelf', z: 1.8 }] },
  fbi: { n: 'FBI東京駐在官室', g: '赤坂', bg: 'fbi', bgm: 'tension', day: 2, people: [{ id: 'cole', tp: [{ l: '尋問する', intr: 'A', cond: g => !g.intr.A.clear }, { l: 'あの夜の話をもう1度', b: 'a_end', cond: g => g.intr.A.clear }] }], hs: [{ id: 'f_clocks', a: 'clocks', z: 2 }, { id: 'f_seal', a: 'seal', z: 2.4 }] }
};
const MAPPOS = { genkan: [300, 470], living: [470, 380], bath: [470, 560], hall: [140, 380], kanri: [140, 560], soukan: [1010, 250], keibi: [1230, 190], kasouken: [1230, 330], cyber: [1010, 400], renraku: [1400, 260], fbi: [820, 640] };

/* interrogations */
const INTR = {
  A: { foe: 'cole', bg: 'fbi', title: 'FBI東京駐在官　コール', intro: 'a_intro', end: 'a_end', miss: ['a_miss', 'a_miss2'], open: ['a_s1', 'a_s2', 'a_s3', 'a_s4'], need: ['a_s2', 'a_s3', 'a_s4'],
    st: { a_s1: { p: 'a_p1', ph: ['アッザームは、我々の協力者だ。', '事件は、FBIが引き取る。'] },
      a_s2: { p: 'a_p2', ph: ['昨夜は、ワシントンとの会議に出ていた。', '日本時間の2時から、', '2時40分までだ。'], ans: [2], ok: ['h_conf'], near: { conf: 'a_n2', f_confRow: 'a_n2', f_utc: 'a_n2' }, o: 'a_o2', hint: '「2時40分まで」。本部の記録を、日本の時計に直して比べる。' },
      a_s3: { p: 'a_p3', ph: ['会議のあとは、', '朝まで自宅にいた。'], ans: [1], ok: ['h_coleLate', 'f_etc'], o: 'a_o3', hint: '「朝まで自宅」。コールの車は、夜中にどこを走ったか。' },
      a_s4: { p: 'a_p4', ph: ['アッザームとは、', 'この1週間、', '連絡を取っていない。'], ans: [1, 2], ok: ['phone', 'f_msg158', 'f_msgMon', 'f_missed'], o: 'a_o4', hint: '「連絡を取っていない」。被害者のスマホに「N.C.」がいる。' } } },
  B: { foe: 'saegusa', bg: 'keibi', title: '警備局 外事課　三枝', intro: 'b_intro', end: 'b_end', miss: ['b_miss', 'b_miss2'], open: ['b_s1', 'b_s2'], need: ['b_s2', 'b_s3', 'b_s4'],
    st: { b_s1: { p: 'b_p1', ph: ['アッザームの保護は、公安の所管です。', 'FBIにも、一課にも、渡せません。'] },
      b_s2: { p: 'b_p2', ph: ['昨夜は当直でした。', '一晩中、', '庁舎の席にいました。'], ans: [1, 2], ok: ['gate', 'f_gateS'], o: 'b_o2', opens: ['b_s3'], hint: '「一晩中」。庁舎の出入りは、ゲートが覚えている。' },
      b_s3: { p: 'b_p3', ph: ['……外の空気を吸いに、出ただけです。', '現場の方角には、行っていません。'], ans: [1], ok: ['f_scar'], near: { parking: 'b_n3', f_parkS: 'b_n3' }, o: 'b_o3', opens: ['b_s4'], hint: '「行っていません」。となりの駐車場にいた車の、持ち主。' },
      b_s4: { p: 'b_p4', ph: ['内通者は、コールです。', '夜中に、あの部屋の前に立っていた。', '私が、この目で見ました。'], ans: [0], ok: ['h_coleClear'], o: 'b_o4', hint: '「内通者はコール」。犯人がいた時刻と、コールが着いた時刻を、ボードで比べる。' } } },
  C: { foe: 'mashiba', bg: 'renraku', title: '連絡調整官　真柴', intro: 'c_intro', end: 'c_end', miss: ['c_miss', 'c_miss2'], open: ['c_s1', 'c_s2', 'c_s5'], need: ['c_s2', 'c_s3', 'c_s4', 'c_s5', 'c_s6'],
    st: { c_s1: { p: 'c_p1', ph: ['私は、連絡調整官です。', '両方の間に、立っていただけです。'] },
      c_s2: { p: 'c_p2', ph: ['あの夜は庁舎で、', '総監への資料を作っていました。', '2時15分に、お送りしたはずです。'], ans: [0, 2], ok: ['h_alibi'], near: { mail: 'c_n2', gate: 'c_n2', f_gateM: 'c_n2', f_mailR: 'c_n2' }, o: 'c_o2', opens: ['c_s3'], hint: '「庁舎で」「2時15分に」。メールの細字とゲートの記録を、ボードでつなぐ。' },
      c_s3: { p: 'c_p3', ph: ['……家で仕上げて、', '時刻を決めて送っただけです。', '事件とは、関係がありません。'], ans: [2], ok: ['h_same'], near: { f_mailIP: 'c_n2', f_login: 'c_n2', loginlog: 'c_n2' }, o: 'c_o3', opens: ['c_s4'], hint: '「関係がありません」。メールの回線の番号を、ほかの紙で探す。' },
      c_s4: { p: 'c_p4', ph: ['回線が同じでも、私とは限らない。', 'あのアカウントの表は、三枝さんも持っています。', '住所も、ご存じだ。'], ans: [0], ok: ['h_three'], o: 'c_o4', hint: '「私とは限らない」。犯行に要る知識を3つ、ボードでつなぐ。' },
      c_s5: { p: 'c_p5', ph: ['大使館へは、兄の件で、', '領事に相談に行っただけです。'], ans: [1], ok: ['slip', 'f_slip'], o: 'c_o5', opens: ['c_s6'], hint: '「領事に」。机の引き出しの紙。' },
      c_s6: { p: 'c_p6', ph: ['兄が帰れたのは、外務省のおかげです。', '私は、何も渡していません。'], ans: [0, 1], ok: ['h_trade'], o: 'c_o6', hint: '「何も渡していません」。面会の日と、釈放の日。' } } }
};

/* final report */
const REPORT = [
  { k: 'doer', q: '実行犯', sub: 'あの夜、部屋に入って手を下した者', opts: [['cole', 'コール駐在官'], ['saegusa', '三枝警部'], ['two', '帽子の2人組（大使館の者）'], ['mashiba', '真柴調整官'], ['laila', '娘のライラ'], ['kanri', '管理人']], a: 'two', sup: ['h_window', 'h_embassy', 'f_two'] },
  { k: 'mole', q: '内通者', sub: '住所と時刻を、外へ渡した者', opts: [['cole', 'コール駐在官'], ['saegusa', '三枝警部'], ['mashiba', '真柴調整官'], ['kanri', '管理人'], ['none', '内通者はいない']], a: 'mashiba', sup: ['h_three', 'h_same', 'h_alibi'] },
  { k: 'boss', q: '指示役', sub: '内通者と実行犯をつなぎ、命じた者', opts: [['cole', 'コール駐在官'], ['kujo', '九条警備局長'], ['keystone', 'キーストン社'], ['khalid', '大使館の警備担当官 ハリド'], ['unknown', '分からない']], a: 'khalid', sup: ['h_embassy', 'f_khalid', 'f_slip', 'slip', 'h_trade'] },
  { k: 'entry', q: '侵入の手口', sub: '鍵のかかった部屋へ、どう入ったか', opts: [['app', '娘の合鍵アプリを盗んで開けた'], ['victim', '被害者が自分で開けた'], ['master', '記録に残らない隠れた鍵で開けた'], ['window', '窓から入った']], a: 'master', sup: ['h_time', 'h_ghost'] },
  { k: 'camera', q: 'カメラの手口', sub: '廊下のカメラに、なぜ映っていないか', opts: [['broken', 'カメラが故障していた'], ['swap', '古い映像に差し替えた'], ['blind', 'カメラの死角を通った']], a: 'swap', sup: ['h_loop'] },
  { k: 'weapon', q: '凶器と殺害の場所', sub: '何で、どこで', opts: [['tub', '浴槽の縁。浴室'], ['lock', '外した錠の本体。玄関'], ['board', '大理石のまな板。台所'], ['unknown', '分からない']], a: 'board', sup: ['h_weapon'] },
  { k: 'motive', q: '内通者の動機', sub: 'なぜ渡したか', opts: [['money', '金'], ['career', '出世'], ['brother', '拘束された兄の釈放'], ['threat', '自分の秘密で脅された']], a: 'brother', sup: ['h_trade', 'f_news'] }
];

/* relation chart */
const REL = {
  nodes: [
    { id: 'azzam', n: 'アッザーム', s: '亡命した記者。被害者', x: 750, y: 120 }, { id: 'laila', n: 'ライラ', s: '娘', x: 1060, y: 90, ch: 'laila' },
    { id: 'cole', n: 'コール', s: 'FBI東京駐在官', x: 300, y: 300, ch: 'cole' }, { id: 'saegusa', n: '三枝', s: '警備局 外事課', x: 1200, y: 300, ch: 'saegusa' },
    { id: 'mashiba', n: '真柴', s: '連絡調整官', x: 750, y: 380, ch: 'mashiba' }, { id: 'onizuka', n: '鬼塚', s: '捜査一課', x: 1330, y: 520, ch: 'onizuka' },
    { id: 'khalid', n: 'K.ハリド', s: '大使館 警備担当官', x: 520, y: 610, c: g => g.facts.includes('f_khalid') || g.facts.includes('f_slip') }, { id: 'two', n: '帽子の2人組', s: '実行犯', x: 180, y: 480, c: g => g.facts.includes('f_two') },
    { id: 'bro', n: '真柴の兄', s: '8か月拘束', x: 1000, y: 590, c: g => g.facts.includes('f_news') }
  ],
  edges: [
    { a: 'azzam', b: 'laila', l: '父と娘' }, { a: 'cole', b: 'azzam', l: '協力者（届出なし）', c: g => g.intr.A.clear, alt: '「我々の協力者」' }, { a: 'saegusa', b: 'azzam', l: '保護' }, { a: 'mashiba', b: 'azzam', l: '住居を手配' },
    { a: 'mashiba', b: 'cole', l: '連絡' }, { a: 'mashiba', b: 'saegusa', l: '連絡' }, { a: 'saegusa', b: 'cole', l: '無断で監視', c: g => g.ev.includes('note') },
    { a: 'mashiba', b: 'khalid', l: '5/28 面会', c: g => g.facts.includes('f_slip') }, { a: 'khalid', b: 'two', l: '車を出す', c: g => g.hyp.includes('h_embassy') }, { a: 'two', b: 'azzam', l: '2:13 侵入', c: g => g.hyp.includes('h_window') },
    { a: 'mashiba', b: 'bro', l: '兄弟', c: g => g.facts.includes('f_news') }, { a: 'khalid', b: 'bro', l: '6/5 釈放', c: g => g.hyp.includes('h_trade') }
  ]
};
const LANES = [['room', '錠と部屋'], ['hall', '廊下と昇降機'], ['emb', '駐車場の「外」の車'], ['cole', 'コール'], ['saegusa', '三枝']];
if (typeof module !== 'undefined') module.exports = { FACTS, HYPS, EV, LOCS, INTR, REPORT, REL, LANES, MAPPOS, DAYS };
