"""問題集 第5章 不定詞。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 5

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
  "q": Q4("It is very kind (　) you to help me.", ["for", "of", "to", "with"], LEAD),
  "a": "②",
  "s": "{kind} のように人の性質・性格を評価する形容詞（{kind, nice, careless, foolish, rude} など）では、不定詞の意味上の主語を {of ＋人} で表す。{You are very kind to help me.} と言いかえられるのが目印。"
       "①{for ＋人} は {easy, difficult, necessary} など「行為そのもの」を評価する形容詞のとき（{It is easy for me to swim.}）。③④は意味上の主語を表さない。"
       "<br><b>ポイント</b>：「人 ＋ {be} ＋ 形容詞」と言える（人の性質）→ {of}、言えない（行為の評価）→ {for}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I need a pen to write (　).", ["with", "in", "on", "by"]),
  "a": "①",
  "s": "形容詞用法の不定詞では、修飾される名詞が前置詞の目的語になることがある。「ペンで書く」は {write with a pen} なので {a pen to write with}。"
       "③{on} は「（紙など）の上に書く」で、{paper to write on} なら正しい。②{in}・④{by} は「ペンで」の意味にならない。"
       "<br><b>ポイント</b>：〈名詞 ＋ {to do} ＋前置詞〉は、もとの〈動詞＋前置詞＋名詞〉（{write with a pen}）を思い浮かべて前置詞を決める。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("My grandmother lived (　) ninety.", ["being", "to be", "to have been", "having been"]),
  "a": "②",
  "s": "{live to be 〜}「〜歳まで生きる」は、結果を表す副詞用法の不定詞（生きた結果、90歳になった）。"
       "③完了不定詞は主節より前の時を表すので、この意味にならない。①④の分詞・動名詞は {live} の後に「〜歳まで」の意味で続かない。"
       "<br><b>ポイント</b>：結果用法の決まった形 {live to be 〜 / grow up to be 〜 / wake up to find 〜 / only to do}（〜したが結局…）。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("This box is too heavy for me (　).", ["to carry it", "to carry", "carrying", "carry"]),
  "a": "②",
  "s": "{too 〜 to do}「…するには〜すぎる」。不定詞 {carry} の目的語は文の主語 {this box} と同じものなので、{it} を重ねて置かない（× {to carry it}）。"
       "③④は {too 〜} の後に続く形として誤り。なお、{so 〜 that} 構文に書きかえると {it} が必要になる：{This box is so heavy that I can't carry it.}"
       "<br><b>ポイント</b>：{too 〜 to do}・{easy to do} などで、不定詞の目的語が文の主語と同じなら、目的語を書かない。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語句を並べかえよ。<br>私は毎朝散歩することにしている。<br>（ {make / it / a rule / to / take / I / a walk} ） {every morning.}",
  "a": "{I make it a rule to take a walk every morning.}",
  "s": "{make it a rule to do}「〜することにしている」。{it} は形式目的語で、真の目的語は {to take a walk every morning}。"
       "第5文型 {make O C} の O が長い不定詞なので、{it} を仮に置いて後ろに回している。同じ型：{I found it difficult to answer the question.}"
       "<br><b>ポイント</b>：〈{make / find / think} ＋ {it} ＋ C ＋ {to do}〉の {it} は形式目的語。{to do} の内容を指す。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{It seems that she was rich when she was young.}<br>＝ {She seems (　) (　) been rich when she was young.}",
  "a": "{to, have}",
  "s": "{seems}（現在）より {was}（過去）のほうが前の時なので、完了不定詞 {to have ＋過去分詞} を使う。"
       "{It seems that she is rich.}（同じ時）なら {She seems to be rich.} となる。"
       "<br><b>ポイント</b>：主節と同じ時 → {to do}、主節より前の時 → {to have done}。{seem, appear, be said} などでよく問われる。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{He is ①<u>enough old</u> ②<u>to drive</u> a car, but he ③<u>has</u> never ④<u>wanted to</u>.}",
  "a": "① {enough old → old enough}",
  "s": "{enough} が形容詞・副詞を修飾するときは、その後ろに置く（{old enough to do}「〜できるほどの年齢だ」）。名詞を修飾するときはふつう前に置く（{enough money to buy a car}）。"
       "④{wanted to} の {to} は、{to drive a car} の繰り返しを避けて動詞以下を省いた代不定詞で正しい。③現在完了 {has never wanted}「一度も〜したいと思ったことがない」も正しい。"
       "<br><b>ポイント</b>：〈形容詞・副詞 ＋ {enough to do}〉の語順。文末の {to} だけの形（代不定詞）は誤りではない。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>さらに悪いことに、雨が降り始めた。<br>{To make (　) worse, it began to rain.}",
  "a": "{matters}",
  "s": "{to make matters worse}「さらに悪いことに」は独立不定詞（文全体にかかる慣用表現）。{matters} は「事態、状況」の意味で、この表現ではふつう複数形。"
       "ほかに {to tell the truth}（実を言うと）、{to be honest}（正直に言うと）、{needless to say}（言うまでもなく）、{so to speak}（いわば）、{strange to say}（奇妙なことに）。"
       "<br><b>ポイント</b>：独立不定詞は形を丸ごと覚える。文の主語とは関係なく使える。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{He woke up to find himself in a strange room.}",
  "a": "彼が目を覚ますと、見知らぬ部屋にいた。",
  "s": "{wake up to find 〜}「目を覚ますと〜だとわかった」は、結果を表す副詞用法。「〜を見つけるために目を覚ました」（目的）と訳さない。"
       "{find oneself 〜}「（気づくと）自分が〜にいる」。{strange} はここでは「奇妙な」より「見知らぬ、初めての」。"
       "<br><b>ポイント</b>：意志で行わない動作（{wake up, grow up, live}）＋ {to do} は結果。「〜して（その結果）…」と前から訳す。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{The best way to learn a language is not to memorize lists of words but to use it to say something you really want to say.}",
  "a": "言語を学ぶ最もよい方法は、単語のリストを暗記することではなく、自分が本当に言いたいことを言うためにその言語を使うことである。",
  "s": "不定詞の用法を1つずつ確認する。{to learn a language}：形容詞用法（{way} を修飾）。{not to memorize … but to use it}：名詞用法（{is} の補語）で、{not A but B}「A ではなく B」。"
       "{to say something}：副詞用法（目的「〜するために」）。{want to say}：名詞用法（{want} の目的語）。"
       "{it} は {a language} を指す。{something you really want to say} は、目的格の関係代名詞が省略された形。"
       "<br><b>ポイント</b>：1文に不定詞が多いときは、それぞれ「名詞・形容詞・副詞」のどの働きかを決めてから訳す。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>知らない町で道に迷ったら、どちらへ行けばよいかを地元の人に尋ねるのがいちばんだ。",
  "a": "{If you get lost in a town you don't know, the best thing to do is (to) ask a local person which way to go.}",
  "s": "「どちらへ行けばよいか」は〈疑問詞 ＋ {to} 不定詞〉で {which way to go}。{ask ＋人＋ which way to go} の語順にする。"
       "「〜するのがいちばんだ」は {the best thing to do is (to) do}（補語の {to} は省略できる）や {It is best to ask 〜}。"
       "「道に迷う」は {get lost}（{lose your way} も可）。「知らない町」は {a town you don't know / an unfamiliar town}、「地元の人」は {a local person / someone who lives there}。"
       "主語は一般の人なので {you}（{we} でもよい）。"
       "<br><b>ポイント</b>（採点）：{which way to go} の形と位置、条件の {if} 節が現在形（{get}）になっているか。"},
]

CH = {N: {"goal": "to 不定詞の3用法（名詞・形容詞・副詞）を見分け、意味上の主語・完了不定詞・慣用表現を正しく使えるようにする。",
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
