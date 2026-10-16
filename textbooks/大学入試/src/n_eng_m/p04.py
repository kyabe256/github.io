"""問題集 第4章 態（受動態）。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 4

def E(s):
    return f'<span class="en">{s}</span>'

def T(s):
    return re.sub(r"\{([^{}]+)\}", lambda m: E(m.group(1)), s)

def Q4(stem, opts, lead=""):
    assert len(opts) == 4
    return lead + "{" + stem + "}<br>" + "　".join(f"{n} {{{o}}}" for n, o in zip("①②③④", opts))

LEAD = "（　）に入る最も適切なものを、①〜④から1つ選べ。<br>"
SEIGO = "下線部①〜④のうち、誤りを含むものを1つ選び、正しく直せ。<br>"

ITEMS = [
 {"lv": "A", "tag": "文法4択",
  "q": Q4("The road is (　) now, so we have to take a different route.", ["repairing", "being repaired", "been repaired", "be repaired"], LEAD),
  "a": "②",
  "s": "「道路は今修理されているところだ」なので、進行形の受動態 {be being ＋過去分詞}。"
       "①{is repairing} では「道路が（何かを）修理している」になる。③{been} は {is} の直後に置けない（完了形なら {has been repaired}）。④{is be} は不可。"
       "<br><b>ポイント</b>：進行形の受動態は {be being done}、完了形の受動態は {have been done}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I was laughed (　) by everyone in the class.", ["at", "to", "on", "by"]),
  "a": "①",
  "s": "{laugh at 〜}「〜を笑う」のような〈動詞＋前置詞〉は、受動態にしてもひとまとまりの他動詞として扱い、前置詞を残す → {be laughed at by 〜}。"
       "②{to}・③{on} は {laugh} と「笑う」の意味で結びつかない。④{by} を入れると、すでにある {by everyone} と {by} が重なる。"
       "<br><b>ポイント</b>：群動詞の受動態（{be laughed at / be taken care of / be spoken to}）では前置詞を落とさない。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("He was made (　) the room by his mother.", ["clean", "to clean", "cleaning", "cleaned"]),
  "a": "②",
  "s": "能動態 {His mother made him clean the room.} では {make O ＋原形} だが、受動態にすると原形が {to} 不定詞になる → {be made to do}。"
       "①原形は受動態では使えない。③{cleaning}・④{cleaned} も不可。"
       "<br><b>ポイント</b>：使役の {make} と知覚動詞（{see, hear} など）の受動態は {be made / be seen / be heard to do}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("Many new houses (　) in this area since last year.", ["built", "have been built", "have built", "were built"]),
  "a": "②",
  "s": "{since last year}「去年から（今まで）」があるので現在完了。家は「建てられる」側なので、完了形の受動態 {have been ＋過去分詞}。"
       "④過去形 {were built} は {since} と合わない。③{have built} は能動態で「家が（何かを）建てた」になる。①{built} だけでは「建てられた家」という名詞のかたまりになり、文に述語動詞がなくなる。"
       "<br><b>ポイント</b>：時を表す語句で時制を決め、主語が「する側」か「される側」かで態を決める、の2段階で考える。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語句を並べかえよ。<br>私は見知らぬ人に駅への道を尋ねられた。<br>（ {a stranger / asked / by / I / the way / to / was / the station} ）",
  "a": "{I was asked the way to the station by a stranger.}",
  "s": "能動態 {A stranger asked me the way to the station.}（第4文型）の、間接目的語 {me} を主語にした受動態。直接目的語 {the way to the station} は {was asked} の後にそのまま残る。"
       "（{I was asked by a stranger the way to the station.} も文法的には成り立つが、上の語順がふつう。）"
       "<br><b>ポイント</b>：第4文型の受動態は「人」を主語にするのが自然。{ask} では「物」を主語にした受動態（× {The way to the station was asked me}）はふつう使わない。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{Who invented this machine?}<br>＝ {By whom (　) this machine (　)?}",
  "a": "{was, invented}",
  "s": "疑問詞が主語の疑問文を受動態にする。{this machine} を主語にし、「誰によって」＝ {by whom} を文頭に出し、{was this machine invented} と疑問文の語順にする。"
       "話し言葉では {Who was this machine invented by?} のほうがふつう。"
       "<br><b>ポイント</b>：疑問詞を含む受動態は、受動態の平叙文を作る → 疑問文の語順にする → 疑問詞（{by whom}）を前に出す、の順で組み立てる。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{The accident ①<u>was happened</u> ②<u>on</u> a rainy night, and three people ③<u>were</u> badly ④<u>injured</u>.}",
  "a": "① {was happened → happened}",
  "s": "{happen}「起こる」は自動詞で目的語をとらないので、受動態にできない。{occur, take place, appear, disappear} も同じ。"
       "②{on a rainy night} は特定の日の夜なので {on}（ばくぜんと「夜に」なら {at night}）。③④{be injured}「けがをする」は英語では受動態で表すのが正しい。"
       "<br><b>ポイント</b>：自動詞は受動態にならない。逆に「けがをする」「驚く」「興味がある」は {be injured / be surprised / be interested} と受動態で表す。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>私は昨日、電車の中で財布を盗まれた。<br>{I (　) my wallet stolen on the train yesterday.}",
  "a": "{had}（{got} も可）",
  "s": "「（自分の持ち物）を〜される」という被害は {have ＋ O ＋過去分詞}。{My wallet was stolen on the train yesterday.} とも言える。"
       "× {I was stolen my wallet.} は誤り。{steal} は「盗む物」を目的語にとる動詞（{steal A from B}）なので、「人」を主語にした受動態は作れない。人を主語にするなら {rob}：{I was robbed of my wallet.}"
       "<br><b>ポイント</b>：「〜を盗まれる」は {have O stolen} か {O was stolen}。{rob 人 of 物} と {steal 物 (from 人)} の目的語の違いに注意。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{The novel is believed to have been written by a woman who had never left her village.}",
  "a": "その小説は、自分の村を一度も出たことのない女性によって書かれたと信じられている。",
  "s": "{be believed to do}「〜すると信じられている」。{to have been written} は完了不定詞の受動態で、「信じられている」（現在）より前に「書かれた」ことを表す。"
       "{It is believed that the novel was written by 〜} と書きかえられる。{who had never left her village} は、小説が書かれた時点（過去）までの経験なので過去完了。"
       "<br><b>ポイント</b>：{S is said / believed / thought to have done}「S は〜したと言われている／信じられている／考えられている」。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{It is often said that what is not measured cannot be improved, but some of the most important things in education are those that cannot be measured at all.}",
  "a": "測定されないものは改善できないとよく言われるが、教育において最も大切なことのいくつかは、まったく測定できないものである。",
  "s": "{It is often said that 〜}「〜とよく言われる」。{that} 節の主語は関係代名詞 {what} の節 {what is not measured}「測定されないもの」で、動詞は {cannot be improved}（助動詞＋受動態）。"
       "後半の {those that 〜} は「〜するもの」（{those} ＝ {the things}）。{not … at all}「まったく〜ない」。"
       "受動態をすべて「〜される」と直訳すると不自然になるので、{cannot be improved}・{cannot be measured} は「改善できない」「測定できない」と訳すとよい。"
       "<br><b>ポイント</b>：受動態は「される」にこだわらず、日本語として自然な形（可能・自発など）に訳す。"},
 {"lv": "C", "tag": "英作文",
  "q": "「この寺は約1,000年前に建てられたと言われている。」を、(1) {It} を主語にして、(2) {This temple} を主語にして、それぞれ英語に直せ。",
  "a": "(1) {It is said that this temple was built about 1,000 years ago.}<br>(2) {This temple is said to have been built about 1,000 years ago.}",
  "s": "(1) {It is said that S V}。{that} 節の中は「建てられた」のが過去なので {was built}。"
       "(2) {S is said to do} の形にするが、「言われている」（現在）より「建てられた」（過去）が前なので、完了不定詞の受動態 {to have been built}。"
       "× {is said to be built} では「（今）建てられていると言われている」の意味になってしまう。"
       "{They say that 〜} / {People say that 〜} でも同じ内容を表せる。{about 1,000 years ago} は {about a thousand years ago} と書いてもよい。"
       "<br><b>ポイント</b>（採点）：(2) の完了不定詞 {to have been built}。「言われている」と「建てられた」の時のずれを形に反映できているか。"},
]

CH = {N: {"goal": "受動態の基本形と、進行形・完了形・助動詞・第4文型・使役・群動詞の受動態を正しく作り、自然な日本語に訳せるようにする。",
          "items": [dict(it, q=T(it["q"]), a=T(it["a"]), s=T(it["s"])) for it in ITEMS]}}

def verify():
    its = CH[N]["items"]
    lv = [it["lv"] for it in its]
    assert lv.count("A") == 4 and 4 <= lv.count("B") <= 5 and lv.count("C") == 2 and lv == sorted(lv)
    for it in its:
        for k in ("lv", "tag", "q", "a", "s"):
            assert it.get(k), k
        for k in ("q", "a", "s"):
            v = it[k]
            assert "$" not in v and "{" not in v and "}" not in v, v
            assert "( )" not in v and "()" not in v, v
            for o, c in (("<span ", "</span>"), ("<u>", "</u>"), ("<b>", "</b>")):
                assert v.count(o) == v.count(c), (o, v)
        assert "<b>ポイント</b>" in it["s"], it["q"]
        if it["tag"] == "文法4択":
            assert all(c in it["q"] for c in "①②③④") and it["q"].count("(　)") == 1
            assert it["a"] in ("①", "②", "③", "④")
        if it["tag"] == "正誤":
            assert it["q"].count("<u>") == 4 and it["a"][0] in "①②③④"
