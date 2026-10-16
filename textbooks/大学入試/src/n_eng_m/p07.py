"""問題集 第7章 分詞・分詞構文。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 7

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
  "q": Q4("The game was so (　) that nobody wanted to leave early.", ["excite", "excited", "exciting", "excitement"], LEAD),
  "a": "③",
  "s": "{excite} は「（人を）わくわくさせる」という他動詞。試合は人をわくわくさせる側なので現在分詞 {exciting}。"
       "②{excited} は「（人が）わくわくさせられた」＝「わくわくした」で、人を主語にするときの形（{The fans were excited.}）。④名詞 {excitement} は {so} の後に置けない。①原形も不可。"
       "<br><b>ポイント</b>：感情を表す分詞は「（人に）その感情を起こさせる → {-ing}」「（人が）その感情をもつ → {-ed}」。人でも、他人を退屈させる人なら {a boring person}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("Look at the boy (　) with a dog in the park.", ["plays", "played", "playing", "to play"]),
  "a": "③",
  "s": "「公園で犬と遊んでいる少年」。少年は遊ぶ側（能動・進行中）なので現在分詞 {playing}。分詞が語句（{with a dog in the park}）を伴うので名詞の後ろに置く。"
       "①{plays} では {Look at} の文に動詞がもう1つ入り、文が成り立たない。②過去分詞の後置修飾は「〜される」の意味になる。④不定詞では「これから遊ぶ（べき）少年」となり、「見てごらん」と合わない。"
       "<br><b>ポイント</b>：名詞と分詞の関係が「する」なら {-ing}、「される」なら過去分詞。分詞1語なら名詞の前、語句を伴えば名詞の後ろ。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I heard my name (　) from behind.", ["call", "calling", "called", "to call"]),
  "a": "③",
  "s": "知覚動詞 {hear ＋ O ＋ 原形／現在分詞／過去分詞}。{my name} は「呼ばれる」側なので過去分詞 {called}。"
       "①原形・②現在分詞は、O が「呼ぶ」側のときの形（{I heard someone call my name.}）。④能動態の {hear O to do} は不可（受動態 {be heard to do} なら可）。"
       "<br><b>ポイント</b>：知覚動詞・使役動詞の O と C の関係を「O が〜する」か「O が〜される」かで判断する。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("(　) from a distance, the rock looks like a human face.", ["Seeing", "Seen", "To see", "Having seen"]),
  "a": "②",
  "s": "分詞構文の意味上の主語は、主節の主語 {the rock}。岩は「見られる」側なので過去分詞 {Seen}（＝ {When it is seen from a distance}）。"
       "①{Seeing}・④{Having seen} では「岩が（何かを）見る」ことになる。③不定詞は「見るために」などの意味になり、文意も意味上の主語も合わない。"
       "<br><b>ポイント</b>：分詞構文では、まず主節の主語を確認し、それが「する」側か「される」側かで {-ing} か過去分詞かを決める。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語を並べかえよ。<br>彼は目を閉じたまま音楽を聞いていた。<br>{He} （ {to / was / with / closed / his / music / listening / eyes} ）.",
  "a": "{He was listening to music with his eyes closed.}",
  "s": "{with ＋ O ＋ 分詞}「O を〜したまま、O が〜した状態で」（付帯状況）。目は「閉じられた」状態なので過去分詞 {closed}。"
       "{with his eyes closing} は「目が閉じつつある」となり、意味が合わない。{with the TV on} のように形容詞・副詞が来ることもある。"
       "<br><b>ポイント</b>：付帯状況の {with} は「O と C の関係」で分詞を選ぶ（{with his arms folded} 腕を組んで／{with the engine running} エンジンをかけたまま）。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{As I had finished my homework, I went out to play.}<br>＝ {(　) (　) my homework, I went out to play.}",
  "a": "{Having, finished}",
  "s": "接続詞 {As} と、主節と同じ主語 {I} を消し、動詞を分詞にする。宿題を終えたのは遊びに出かけるより前なので、完了形の分詞構文 {Having ＋過去分詞}。"
       "<br><b>ポイント</b>：主節より前の出来事 → {Having done}。否定は {Not having finished 〜} のように {not} を分詞の前に置く。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{The news ①<u>was</u> very ②<u>surprised</u> to everyone ③<u>who</u> ④<u>heard</u> it.}",
  "a": "② {surprised → surprising}",
  "s": "その知らせは人を驚かせる側なので {surprising}。人を主語にすれば {Everyone who heard the news was very surprised.} となる。"
       "①{news} は不可算名詞で単数扱いなので {was} で正しい。③{who} は {everyone} を先行詞とする関係代名詞、④{heard} は過去の話に合っていて正しい。"
       "<br><b>ポイント</b>：{surprise, interest, bore, disappoint} などは「物 → {-ing}、それを感じる人 → {-ed}」が基本。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>彼のなまりから判断すると、彼は九州の出身に違いない。<br>{(　) from his accent, he must be from Kyushu.}",
  "a": "{Judging}",
  "s": "{judging from 〜}「〜から判断すると」は慣用的な分詞構文。意味上の主語は一般の人（話し手）なので、主節の主語 {he} と一致していなくてよい。"
       "<br><b>ポイント</b>：慣用的な分詞構文 ― {generally speaking}（一般的に言えば）/ {frankly speaking}（率直に言えば）/ {considering 〜}（〜を考えると）/ {speaking of 〜}（〜と言えば）/ {judging from 〜}。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{There being no bus service, we had to walk all the way to the village.}",
  "a": "バスの便がなかったので、私たちは村までずっと歩いて行かなければならなかった。",
  "s": "{There being 〜} は {There is} 構文の分詞構文（独立分詞構文）。意味上の主語（{there}）が主節の主語（{we}）と違うので、消さずに残してある。"
       "＝ {As there was no bus service, 〜}。{all the way}「（途中）ずっと、はるばる」。"
       "<br><b>ポイント</b>：分詞の前に主節と違う主語が残っていたら独立分詞構文。{It being Sunday, 〜}（日曜日だったので）なども同じ。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{Written in plain English, the book is easy to read even for beginners; read carefully, however, it reveals a surprising depth of thought.}",
  "a": "平易な英語で書かれているので、その本は初心者にとっても読みやすいが、注意深く読むと、驚くほど深い思想が見えてくる。",
  "s": "{Written 〜} は過去分詞の分詞構文で、{the book} が「書かれている」ことから理由（＝ {Because it is written 〜}）。"
       "後半の {read carefully} の {read} も過去分詞（本は「読まれる」側）で、条件・時（＝ {if / when it is read carefully}）。"
       "分詞構文の意味（理由・時・条件・譲歩など）は、前後の文脈で決める。{easy to read} は「読むのにやさしい」。"
       "{a surprising depth of thought}「驚くほどの思想の深さ」は、日本語では「驚くほど深い思想」とすると自然。"
       "<br><b>ポイント</b>：文頭や文中の過去分詞が分詞構文なら、主節の主語を補って「〜されると／〜されているので」と意味を決める。"},
 {"lv": "C", "tag": "英作文",
  "q": "分詞構文を用いて、英語に直せ。<br>浜辺を歩いていると、美しい貝殻が目にとまった。",
  "a": "{Walking along the beach, I noticed a beautiful shell.}（{I found a beautiful shell} も可）",
  "s": "分詞構文の意味上の主語は、主節の主語と一致させる。日本語の「貝殻が目にとまった」につられて "
       "× {Walking along the beach, a beautiful shell caught my eye.} と書くと、「貝殻が浜辺を歩いていた」ことになってしまう（懸垂分詞）。"
       "主節の主語を {I} にして {I noticed / found / saw} とするのが正しい。分詞構文を使わなければ {While I was walking along the beach, a beautiful shell caught my eye.} は正しい。"
       "<br><b>ポイント</b>（採点）：意味上の主語の一致、{along}（〜に沿って）の使い方。"},
]

CH = {N: {"goal": "現在分詞と過去分詞を「する側／される側」で見分け、分詞構文を正しく作り、文脈に合わせて訳せるようにする。",
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
