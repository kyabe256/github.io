"""問題集 第8章 関係詞。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 8

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
  "q": Q4("This is the town (　) I visited last year.", ["where", "which", "in which", "what"], LEAD),
  "a": "②",
  "s": "関係詞の後ろの節 {I visited ＿ last year} を見ると、他動詞 {visit} の目的語が欠けている → 目的格の関係代名詞 {which}。"
       "①{where}・③{in which} は、後ろが欠けのない完全な文のときに使う（{the town where I lived last year}）。④{what} は先行詞を含む関係代名詞なので、先行詞 {the town} の後には置けない。"
       "<br><b>ポイント</b>：先行詞が「場所」でも、後ろの節に名詞の欠け（主語・目的語）があれば {which / that}、なければ {where}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I'll give you (　) you need.", ["that", "which", "what", "whom"]),
  "a": "③",
  "s": "{give you ＿} の直接目的語の位置で、前に先行詞がない → 先行詞を含む関係代名詞 {what}「〜するもの」（＝ {the thing(s) which}）。"
       "①{that}・②{which}・④{whom} はどれも先行詞が必要で、ここでは使えない。"
       "<br><b>ポイント</b>：空所の前に先行詞（名詞）がなく、後ろの節に名詞の欠けがある → {what}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("He said nothing, (　) made her even angrier.", ["that", "which", "what", "it"]),
  "a": "②",
  "s": "前の文の内容（彼が何も言わなかったこと）を先行詞とする、非制限用法の {which}。"
       "①{that} は非制限用法（コンマの後）では使えない。③{what} は先行詞を含むので、ここでは不可。④{it} では、接続詞なしに2つの文をコンマだけでつなぐことになり誤り。"
       "<br><b>ポイント</b>：〈コンマ ＋ {which}〉は前の文全体や一部を先行詞にできる。「そしてそのことが〜」と前から訳す。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("(　) hard you may try, you can't finish the work in a day.", ["However", "Whatever", "Whenever", "Although"]),
  "a": "①",
  "s": "{however ＋ 形容詞・副詞 ＋ S V}「どんなに〜しても」（＝ {No matter how hard you may try}）。直後に副詞 {hard} があるのが決め手。"
       "②{whatever} は名詞の働きをする（{Whatever you say, 〜}）か名詞を修飾するので、{hard} の前に置けない。③{Whenever}「いつ〜しても」は意味も語順も合わない。"
       "④{Although} は直後に {hard} を置く語順にならない（{Although you may try hard, 〜} なら可）。"
       "<br><b>ポイント</b>：複合関係副詞 {however} の直後には形容詞・副詞が来る。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語を並べかえよ。ただし、前置詞を関係代名詞の直前に置くこと。<br>彼女は、私がいっしょに働きたいと思っている人だ。<br>{She is the person} （ {with / whom / I / want / to / work} ）.",
  "a": "{She is the person with whom I want to work.}",
  "s": "もとの文は {I want to work with her.}。前置詞 {with} を関係代名詞の前に出すと {with whom}。前置詞の直後では {who} や {that} は使えない。"
       "前置詞を後ろに残すなら {the person (whom / who / that) I want to work with}（この場合、関係代名詞は省略できる）。"
       "<br><b>ポイント</b>：〈前置詞 ＋ 関係代名詞〉は {whom}（人）／{which}（物）だけ。{that} は前置詞の後に置けない。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{That is the ①<u>reason</u> ②<u>which</u> he ③<u>didn't come</u> to the party ④<u>last night</u>.}",
  "a": "② {which → why}（{for which} も可）",
  "s": "後ろの節 {he didn't come to the party last night} は欠けのない完全な文なので、関係代名詞 {which} ではなく関係副詞 {why}（＝ {for which}）。"
       "先行詞を省いて {That is why he didn't come to the party last night.}（そういうわけで彼は来なかった）とも言える。"
       "<br><b>ポイント</b>：関係代名詞か関係副詞かは、先行詞ではなく「後ろの節に欠けがあるか」で決める。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>彼は10年前の彼ではない。<br>{He is not (　) he was ten years ago.}",
  "a": "{what}",
  "s": "{what S is / was}「今の S／昔の S」（人柄・状態）。{what he was ten years ago}「10年前の彼」。"
       "{what he has}「彼の持っているもの（財産）」と対比して使われることも多い（{What he is is more important than what he has.}）。"
       "<br><b>ポイント</b>：{what} を使った慣用表現 ― {what S is}（今のS）/ {what is called}・{what we call}（いわゆる）/ {what is more}（そのうえ）。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語を補え。<br>{I have a friend. His father is a famous pianist.}<br>＝ {I have a friend (　) father is a famous pianist.}",
  "a": "{whose}",
  "s": "2つ目の文の {His}（所有格）を関係代名詞にする → {whose ＋ 名詞}。{whose father} が関係詞節の主語になっている。"
       "先行詞が物でも {whose} は使える（{a house whose roof is red}）。"
       "<br><b>ポイント</b>：所有格（{his, her, its, their}）を置きかえる関係代名詞は {whose}。直後に必ず名詞が来る。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{The day will soon come when anyone can travel to space.}",
  "a": "誰でも宇宙旅行ができる日が、まもなくやって来るだろう。",
  "s": "{when 〜} は、文頭の先行詞 {The day} を修飾する関係副詞の節。主語が長くなるのを避けて、関係詞節が動詞 {will soon come} の後ろに回っている（先行詞と関係詞の分離）。"
       "「その日がまもなく来るだろう、そのとき誰でも…」と切らず、{The day} にかけて訳す。{anyone} は肯定文で「誰でも」。"
       "<br><b>ポイント</b>：関係詞が先行詞から離れていても、意味のつながる名詞を探して修飾関係をつかむ。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{What matters is not how much you know but what you do with what you know.}",
  "a": "大切なのは、どれだけ多くのことを知っているかではなく、知っていることを使って何をするかである。",
  "s": "3つの {what} を区別する。1つ目 {What matters} は関係代名詞「〜こと」（大切なこと）で、文の主語。"
       "2つ目 {what you do} は「何をするか」という間接疑問の {what}（疑問詞）。{how much you know}（どれだけ知っているか：間接疑問）と {not A but B} で並んでいるので、疑問詞と読むのが自然。"
       "3つ目 {what you know} は関係代名詞「知っていること」で、前置詞 {with} の目的語。{do 〜 with …} は「…を使って〜する、…を扱う」。"
       "<br><b>ポイント</b>：{what} は「〜こと・もの」（関係代名詞）か「何を〜か」（疑問詞）かを、並んでいる語句や文脈から決める。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>私が生まれ育った町は、この10年で大きく変わった。",
  "a": "{The town where I was born and raised has changed a lot in the last ten years.}",
  "s": "「生まれ育った」は {was born and raised}（{was born and grew up / was born and brought up} も可）。後ろが完全な文なので関係副詞 {where}。"
       "関係代名詞を使うなら {The town (that) I was born and grew up in} とし、前置詞 {in} を忘れない（× {The town which I was born and grew up}）。"
       "「この10年で」は {in the last (past) ten years} で、現在完了 {has changed} と組み合わせる。"
       "<br><b>ポイント</b>（採点）：関係詞の選択、主語 {The town}（単数）に合った {has changed}、関係詞節の範囲（{where 〜 raised}）が正しく閉じているか。"},
]

CH = {N: {"goal": "関係代名詞・関係副詞・what・複合関係詞を、後ろの節に何が欠けているかから判断して選び、正確に訳せるようにする。",
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
