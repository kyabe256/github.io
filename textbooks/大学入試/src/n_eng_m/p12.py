"""問題集 第12章 形容詞・副詞・前置詞。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 12

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
  "q": Q4("There were (　) people at the concert than we had expected.", ["less", "fewer", "little", "few"], LEAD),
  "a": "②",
  "s": "{than} があるので比較級。{people} は可算名詞（複数扱い）なので、{few} の比較級 {fewer}。"
       "①{less} は不可算名詞に使うのが原則（{less money}）。③{little}・④{few} は原級なので {than} と合わない。"
       "<br><b>ポイント</b>：数（可算）は {many / few → more / fewer}、量（不可算）は {much / little → more / less}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I could (　) believe my eyes.", ["hard", "hardly", "harder", "hardness"]),
  "a": "②",
  "s": "{hardly}「ほとんど〜ない」は否定の意味をもつ副詞（準否定語）。「自分の目がほとんど信じられなかった」。"
       "①{hard} は「熱心に、激しく」で意味が合わず、{could} と動詞の間に置く位置も不自然。③比較級、④名詞は文法的に入らない。"
       "<br><b>ポイント</b>：{-ly} の有無で意味が変わる副詞 ― {hard / hardly}、{late}（遅く）/ {lately}（最近）、{near}（近くに）/ {nearly}（ほとんど）。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("My brother is (　) of passing the exam.", ["possible", "likely", "capable", "able"]),
  "a": "③",
  "s": "{be capable of doing}「〜する能力がある」。"
       "④{able} は {be able to do} の形で、{of} は続かない。②{likely} は {be likely to do}「〜しそうだ」。①{possible} は人を主語にとらない（{It is possible for him to pass the exam.}）。"
       "<br><b>ポイント</b>：形容詞は後ろの形（{of doing} / {to do}）と、人を主語にとれるかどうかをセットで覚える。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("Please finish this report (　) next Monday.", ["until", "by", "in", "since"]),
  "a": "②",
  "s": "{by}「〜までに（期限）」、{until}「〜まで（ずっと）」（継続）。{finish} はある時点までに完了させる動作なので {by}。"
       "①{until} は {wait / stay} など継続する動作と使う（{Please wait until next Monday.}）。③{next} の付いた時の表現には前置詞を付けない（{next Monday} だけで副詞の働き）。④{since} は完了形と使う。"
       "<br><b>ポイント</b>：「〜までに」→ {by}（完了）、「〜までずっと」→ {until / till}（継続）。動詞の性質で判断する。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語を並べかえよ。<br>何か冷たい飲み物がほしい。<br>{I want} （ {cold / drink / something / to} ）.",
  "a": "{I want something cold to drink.}",
  "s": "{-thing / -one / -body} で終わる代名詞を修飾する形容詞は、その後ろに置く（× {cold something}）。不定詞（{to drink}）はさらにその後ろ。"
       "<br><b>ポイント</b>：〈{something} ＋ 形容詞 ＋ {to do}〉の語順を丸ごと覚える（{anything interesting to read} など）。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{①<u>Almost</u> students in ②<u>my class</u> ③<u>have</u> their own smartphones, ④<u>though</u> few use them during lessons.}",
  "a": "① {Almost → Most}（{Almost all (the)} も可）",
  "s": "{almost} は副詞なので、名詞 {students} を直接修飾できない。「ほとんどの生徒」は {most students} か {almost all (of) the students}。"
       "③主語 {students} は複数なので {have} で正しい。④{though}「〜だけれども」は接続詞で正しい。後半の {few} は「ほとんど〜ない」という否定の意味。"
       "<br><b>ポイント</b>：{almost} は {all / every / no} などを修飾して {almost all students / almost every student} とする。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>その会議は嵐のために延期された。<br>{The meeting was put off (　) account of the storm.}",
  "a": "{on}",
  "s": "{on account of 〜}「〜のために（理由）」＝ {because of / owing to / due to}。{account} は「理由、根拠」の意味。"
       "{put off}「延期する」の受動態 {was put off} にも注意。"
       "<br><b>ポイント</b>：{on} を使う群前置詞・成句 ― {on account of}（〜のために）/ {on purpose}（わざと）/ {on time}（時間どおりに）/ {on business}（仕事で）。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{Though he is rich, he isn't happy.}<br>＝ {(　) (　) (　) his wealth, he isn't happy.}",
  "a": "{In, spite, of}",
  "s": "接続詞 {though} の後は S V、群前置詞 {in spite of} の後は名詞（句）。{he is rich} を名詞 {his wealth} にして前置詞の後に置いている。"
       "1語なら {Despite his wealth}（× {despite of}）。"
       "<br><b>ポイント</b>：接続詞（{though / although / because}）＋ S V ⇔ 前置詞（{in spite of / despite / because of}）＋ 名詞。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{The movie was so boring that hardly anyone stayed until the end.}",
  "a": "その映画はとても退屈だったので、最後まで残った人はほとんどいなかった。",
  "s": "{so 〜 that …}「とても〜なので…」。{hardly anyone}「ほとんど誰も〜ない」は、「〜した人はほとんどいなかった」と訳すと自然。"
       "{boring} は「（人を）退屈させる」で、映画が主語なので {-ing}。{until the end}「最後まで（ずっと）」は継続の {until}。"
       "<br><b>ポイント</b>：準否定語 {hardly / scarcely / few / little} を含む文は、「ほとんど〜ない」と否定で訳す。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{Most of the information we receive every day is of little use, yet we find it surprisingly hard to ignore.}",
  "a": "私たちが毎日受け取る情報のほとんどは、ほとんど役に立たない。それなのに、私たちはそれを無視するのが驚くほど難しいと感じる。",
  "s": "主語は {Most of the information}。{information} は不可算名詞なので、{most of} が付いても単数扱いの {is}。{we receive every day} は目的格の関係代名詞が省略された節。"
       "{of ＋ 抽象名詞} は形容詞の働き：{of little use}＝ほとんど役に立たない（{of use} ＝ {useful}、{of importance} ＝ {important}）。"
       "{yet} は「それなのに」。{find it hard to ignore} の {it} は形式目的語ではなく、{the information} を指す代名詞で、{find O C}「O が C だとわかる、感じる」の O。"
       "{hard to ignore}「無視しにくい」の {ignore} の目的語は O の {it} と同じものなので書かない（{The information is hard to ignore.} と同じ関係）。"
       "<br><b>ポイント</b>：{it} が形式目的語か、前の名詞を指す代名詞かは、{to do} の後ろに目的語が欠けているかで見分ける。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>その店は駅から歩いて5分のところにあり、月曜日以外は毎日夜9時まで開いている。",
  "a": "{The shop is a five-minute walk from the station, and it is open until 9 p.m. every day except Monday.}",
  "s": "「歩いて5分」は {a five-minute walk}（{five-minute} はハイフンでつないで形容詞になるので {minute} は単数）。{five minutes' walk} も可。"
       "{It takes five minutes to walk from the station to the shop.} と書いてもよい。"
       "「〜まで（ずっと）開いている」は継続なので {until}（× {by}）。「〜以外は」は {except}。「開いている」は形容詞 {open}（× {is opening}：「開店しつつある」の意味になる）。"
       "<br><b>ポイント</b>（採点）：{five-minute} の形、{until} と {by} の区別、{open} を形容詞として使えているか。"},
]

CH = {N: {"goal": "形容詞・副詞の形と位置、数量の表し方、紛らわしい前置詞の使い分けを、語法に基づいて判断できるようにする。",
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
