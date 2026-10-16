"""問題集 第11章 名詞・代名詞・冠詞。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 11

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
  "q": Q4("(　) of the students has a smartphone.", ["Every", "Each", "All", "Both"], LEAD),
  "a": "②",
  "s": "{each of the ＋ 複数名詞}「〜のそれぞれ」は単数扱いなので、動詞 {has} と合う。"
       "①{every} は形容詞としてだけ使い、× {every of} とは言えない（{every student} なら可）。③{All of the students} は複数扱いで {have} になる。④{Both} も複数扱いで、しかも2人のときにしか使えない。"
       "<br><b>ポイント</b>：{each}（代名詞・形容詞、単数扱い）／{every}（形容詞のみ、単数扱い）／{all・both}（複数扱い）。動詞の形も判断の手がかりになる。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I have two brothers. One lives in Osaka, and (　) lives in Tokyo.", ["another", "other", "the other", "others"]),
  "a": "③",
  "s": "2人のうち1人を {one} で表すと、残りの1人は決まっている（特定できる）ので {the other}。"
       "①{another} は「（ほかにもある中の）もう1つ」で、3つ以上あるときに使う。②{other} は単独では単数の代名詞として使えない（{other people} のように形容詞として使う）。④{others} は複数で、{lives} と合わない。"
       "<br><b>ポイント</b>：残りが1つ → {the other}、残り全部（複数）→ {the others}、不特定の別の1つ → {another}、不特定の別のいくつか → {others}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("There is (　) furniture in her room.", ["many", "a few", "little", "a lot"]),
  "a": "③",
  "s": "{furniture}（家具）は不可算名詞なので、可算名詞に使う①{many}・②{a few} は不可。④{a lot} は {a lot of} としなければ名詞の前に置けない。"
       "{little ＋ 不可算名詞}「ほとんどない」。家具を1点、2点と数えるときは {a piece of furniture / two pieces of furniture}。"
       "<br><b>ポイント</b>：日本語では数えられそうでも英語では不可算の名詞 ― {furniture, baggage (luggage), information, advice, news, homework, equipment}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("Please help (　) to the cake on the table.", ["you", "your", "yourself", "yours"]),
  "a": "③",
  "s": "{help oneself to 〜}「〜を自由に取って食べる（飲む）」。命令文の主語は {you} なので、目的語が主語と同じ人なら再帰代名詞 {yourself}（相手が複数なら {yourselves}）。"
       "①{you} は、主語と同じ人を指す目的語としては使えない。②{your}・④{yours} は形が合わない。"
       "<br><b>ポイント</b>：主語と目的語が同じ人 → 再帰代名詞（{enjoy oneself / make oneself at home / help oneself to}）。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語を並べかえよ。<br>彼の話を信じる人もいれば、信じない人もいる。<br>（ {believe / some / others / people / him / and / don't} ）.",
  "a": "{Some people believe him, and others don't.}",
  "s": "{Some 〜, others …}「〜する人もいれば、…する人もいる」。{others} は「ほかの人々（不特定の複数）」。全体のうち残りの全員を指すなら {the others}。"
       "{don't} の後には {believe him} が省略されている。"
       "<br><b>ポイント</b>：{some} と {others} の対比は「〜もいれば…もいる」と訳す。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{Let me ①<u>give</u> you ②<u>an advice</u> ③<u>before</u> you ④<u>start</u> your new job.}",
  "a": "② {an advice → some advice}（{a piece of advice} も可）",
  "s": "{advice}（助言）は不可算名詞なので、{an} を付けられず、複数形にもしない。数えるときは {a piece of advice / two pieces of advice}。"
       "①{let me give} は {let ＋ O ＋原形} で正しい。④{before} 節は時の副詞節なので、これからのことでも現在形 {start} で正しい。"
       "<br><b>ポイント</b>：不可算名詞には {a / an} も複数の {-s} も付けない。量は {some / much / a little}、数えるには {a piece of}。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>その店では、卵は1ダース単位で売られている。<br>{Eggs are sold by (　) dozen at that store.}",
  "a": "{the}",
  "s": "{by the ＋ 単位}「〜単位で、〜ぎめで」。単位を表す名詞には定冠詞 {the} を付ける（{by the hour}「1時間いくらで」、{by the kilo}「キロ単位で」）。"
       "× {by a dozen} や × {by dozen} とは言わない。なお、交通手段の {by bus / by train} は無冠詞なので混同しない。"
       "同じく {the} を使う慣用：{He caught me by the arm.}（体の部分を {the} で表す）。"
       "<br><b>ポイント</b>：{by the 単位}（{the} が必要）と {by ＋交通・通信手段}（無冠詞）を区別する。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語を補え。<br>{She kindly showed me the way to the station.}<br>＝ {She had the (　) to show me the way to the station.}",
  "a": "{kindness}",
  "s": "{have the ＋ 抽象名詞 ＋ to do}「親切にも（勇気を出して）〜する」の形。形容詞 {kind} を名詞 {kindness} にする。"
       "{She was kind enough to show me 〜} / {It was kind of her to show me 〜} とも言える。同じ型：{have the courage to do}（勇気を出して〜する）。"
       "<br><b>ポイント</b>：副詞 {kindly} ⇔ {have the kindness to do} ⇔ {be kind enough to do} の書きかえ。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{It is one thing to know a language, and quite another to teach it.}",
  "a": "言語を知っていることと、それを教えることとは、まったく別のことである。",
  "s": "{A is one thing, and B is another}「A と B とは別のことだ」。ここでは形式主語 {It} が {to know a language} と {to teach it} を受けている。{quite} は {another} を強めて「まったく」。"
       "{one} と {another} を「1つのこと」「もう1つのこと」と直訳せず、「〜と…とは別物だ」とまとめる。"
       "<br><b>ポイント</b>：{one 〜 another} の対比は「別のもの」。{to know} と {to teach} の対比を訳にきちんと出す。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{Those who say they have no time to read are often the very people who would benefit most from it.}",
  "a": "読書をする時間がないと言う人こそ、実は読書から最も恩恵を受けるであろう人であることが多い。",
  "s": "{those who 〜}「〜する人々」（{those} ＝ {people}）が長い主語で、動詞は {are}。{the very ＋名詞}「まさにその〜」。"
       "{would} は「（もし読書をすれば）〜するだろう」という仮定の気持ちを含む。{it} は {to read} の内容（読書すること）を指す。"
       "{often} は「しばしば」より「〜であることが多い」と訳すと自然。{the very} の強調は「〜人こそ」と表すとよい。"
       "<br><b>ポイント</b>：{those who 〜} の主語の範囲（{read} まで）を確定し、代名詞 {it} が何を指すかを訳に反映する。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>最近は、新聞を読むかわりにインターネットでニュースを見る人が多い。",
  "a": "{These days, many people get their news on the internet instead of reading newspapers.}",
  "s": "「〜する人が多い」は {Many people 〜} を主語にすると簡潔（{There are many people who 〜} も文法的には正しい）。"
       "{news} は不可算名詞で、{-s} が付いていても単数扱い（{The news is 〜}）。「ニュースを見る」は {get / read / check the news} などで表す。"
       "「インターネットで」は {on the internet}（{online} も可）。「〜のかわりに」は {instead of ＋ 動名詞}。「最近」は {these days / nowadays}（× {recently} は現在形の文には合わない）。"
       "<br><b>ポイント</b>（採点）：{news} の扱い、{instead of doing}、{these days} と現在形の組み合わせ。"},
]

CH = {N: {"goal": "可算・不可算の区別、other / another / each などの代名詞、再帰代名詞、冠詞と名詞の慣用表現を、数と文脈から正しく判断できるようにする。",
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
