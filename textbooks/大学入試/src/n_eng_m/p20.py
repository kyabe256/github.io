"""問題集 第20章 和文英訳。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号・模範解答と別解と採点のポイントの有無）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

NO = 20
CH = {NO: {
"goal": "日本語をそのまま置きかえず、「英語にしやすい日本語」に言いかえ（和文和訳）、主語・時制・冠詞・名詞の数を確かめながら、自然で誤りのない英文を書けるようにする。",
"items": [
 {"lv": "A", "tag": "英訳4択", "q": "日本語に合う英文として最も適切なものを選べ。<br>その店は駅から歩いて5分のところにある。<br>① " + E("The store is five minutes walk from the station.") + "<br>② " + E("The store is a five-minute walk from the station.") + "<br>③ " + E("The store is a five-minutes walk from the station.") + "<br>④ " + E("The store is five-minute walk from the station."),
  "a": "②",
  "s": E("a five-minute walk") + "：数詞と名詞をハイフンでつないで形容詞のように使うとき、名詞は単数形（③は誤り）。名詞 " + E("walk") + " は数えられるので冠詞 " + E("a") + " が必要（④は誤り）。所有格を使った " + E("five minutes' walk") + " も正しいが、①はアポストロフィがない。<br><b>ポイント</b>：" + E("a ten-year-old boy, a three-day trip") + " も同じ。ハイフンでつないだ数量表現の名詞は単数形。"},
 {"lv": "A", "tag": "英訳4択", "q": "日本語に合う英文として最も適切なものを選べ。<br>この町は人口が多い。<br>① " + E("This town has a large population.") + "<br>② " + E("This town has many population.") + "<br>③ " + E("This town's population is many.") + "<br>④ " + E("This town is many people."),
  "a": "①",
  "s": E("population") + "（人口）の多い・少ないは " + E("large / small") + " で表し、" + E("many / few") + " は使わない（②③は誤り）。④は「町＝多くの人々」となって意味が通らない。" + E("Many people live in this town.") + " と書いてもよい。<br><b>ポイント</b>：日本語の「〜は…が多い」の「は」をそのまま英語の主語にしない。<b>何が多いのか</b>（人口）を考えて、英語の主語・目的語を決める。"},
 {"lv": "A", "tag": "英訳4択", "q": "日本語に合うように、（　）に入る最も適切なものを選べ。<br>私は彼に会うのを楽しみにしている。<br>" + E("I'm looking forward to (　) him.") + "　① " + E("see") + "　② " + E("seeing") + "　③ " + E("be seeing") + "　④ " + E("have seen"),
  "a": "②",
  "s": E("look forward to") + " の " + E("to") + " は前置詞なので、後ろは名詞か動名詞 → " + E("seeing") + "。不定詞の " + E("to") + " と勘違いして原形にするのが典型的なミス。<br><b>ポイント</b>：前置詞の " + E("to") + " をとる表現：" + E("be used to doing") + "（〜に慣れている）、" + E("object to doing") + "（〜に反対する）、" + E("when it comes to doing") + "（〜のこととなると）。"},
 {"lv": "A", "tag": "英訳4択", "q": "日本語に合う英文として最も適切なものを選べ。<br>昨日は一日中雨だった。<br>① " + E("It rained all day yesterday.") + "<br>② " + E("Yesterday was rain all day.") + "<br>③ " + E("It has rained all day yesterday.") + "<br>④ " + E("Yesterday rained all day."),
  "a": "①",
  "s": "天候は " + E("it") + " を主語にして表す。②は " + E("rain") + "（名詞）が補語になって「昨日＝雨」となり誤り（" + E("Yesterday was rainy.") + " なら可）。③ " + E("yesterday") + " は過去の一時点を示すので、現在完了とは一緒に使えない。④ " + E("Yesterday") + " は " + E("rain") + " の主語になれない。" + E("It was raining all day yesterday.") + " も正しい。<br><b>ポイント</b>：天候・時間・距離は " + E("it") + " を主語にする。「昨日は」を主語にしない。"},
 {"lv": "B", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>この本を読めば、日本の歴史がよくわかるだろう。",
  "a": E("This book will give you a good understanding of Japanese history."),
  "s": "和文和訳：「この本は、あなたに日本史のよい理解を与えるだろう」と無生物主語にすると簡潔になる。<br>別解：" + E("If you read this book, you will understand Japanese history well.") + "／" + E("Reading this book will help you understand Japanese history.") + "<br>採点のポイント：① " + E("if") + " 節の中は現在形（" + E("If you will read") + " は誤り）。②「日本の歴史」は " + E("Japanese history") + "／" + E("the history of Japan") + "。" + E("the Japanese history") + " とはふつう言わない。③「わかる」を " + E("know") + " にすると「知っている」という状態になり、「読んで理解が深まる」という意味からずれる。<br><b>ポイント</b>：「〜すれば…」は、" + E("if") + " を使う形と無生物主語の形の両方で書けるようにしておく。"},
 {"lv": "B", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>彼女が来るかどうかは、まだわからない。",
  "a": E("We don't know yet whether she will come."),
  "s": "日本語にない主語（" + E("We / I") + "）を補う。「〜かどうか」は " + E("whether") + "（目的語の位置なので " + E("if") + " も可）。名詞節の中では、未来のことは " + E("will") + " で表す。<br>別解：" + E("It is not yet known whether she will come.") + "／" + E("I'm still not sure if she will come.") + "<br>採点のポイント：① 名詞節の中を " + E("whether she comes") + " にしない（「時・条件の副詞節では未来でも現在形」というルールとの混同）。② " + E("yet") + " は否定文の文末、" + E("still") + " は否定語の前に置く（" + E("I still don't know") + "）。<br><b>ポイント</b>：日本語に主語がなくても、英語では「<b>誰が</b>わからないのか」を補う。"},
 {"lv": "B", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>最近、紙の本を読む人が減っている。",
  "a": E("Fewer people read paper books these days."),
  "s": "「〜する人が減っている」は " + E("fewer people ＋ 動詞") + " で簡潔に書ける。<br>別解：" + E("The number of people who read printed books has been decreasing recently.") + "／" + E("These days, fewer and fewer people read paper books.") + "<br>採点のポイント：① " + E("The number of ～") + " は単数扱い（" + E("is / has been decreasing") + "）。② " + E("recently") + " は現在完了（進行形）と、" + E("these days / nowadays") + " は現在形・現在進行形と組み合わせる。③ " + E("People who read paper books are decreasing.") + " は日本語の直訳で不自然。減るのは人ではなく人の<b>数</b>。<br><b>ポイント</b>：「〜が増える・減る」は、主語を " + E("the number of ～") + " にするか、" + E("more / fewer") + " を使って書く。"},
 {"lv": "B", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>もっと早く出発していれば、電車に間に合ったのに。",
  "a": E("If we had left earlier, we could have caught the train."),
  "s": "実際は「出発が遅く、電車に乗れなかった」→ 過去の事実に反する仮定なので<b>仮定法過去完了</b>。主語は文脈に合わせて " + E("we / I") + " を補う。<br>別解：" + E("We would have been in time for the train if we had left earlier.") + "／" + E("Had we left earlier, we could have made the train.") + "<br>採点のポイント：① " + E("if") + " 節は " + E("had ＋ 過去分詞") + "、主節は " + E("would / could have ＋ 過去分詞") + "。② 「電車に間に合う」は " + E("catch / make the train") + "、" + E("be in time for the train") + "。" + E("meet the train") + " は「列車で着く人を出迎える」の意味になってしまう。<br><b>ポイント</b>：「〜していれば…したのに」は、まず<b>実際はどうだったか</b>を確かめてから仮定法の時制を選ぶ。"},
 {"lv": "B", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>どんなに忙しくても、朝食は食べるべきだ。",
  "a": E("No matter how busy you are, you should eat breakfast."),
  "s": "「どんなに〜でも」は " + E("no matter how ＋ 形容詞 ＋ S V") + " または " + E("however ＋ 形容詞 ＋ S V") + "。一般論なので主語は " + E("you") + "（一般の人）。<br>別解：" + E("However busy you are, you should have breakfast.") + "／" + E("You should eat breakfast, however busy you may be.") + "<br>採点のポイント：① " + E("No matter how you are busy") + " は誤り。" + E("how") + " と形容詞は離さない。②「朝食をとる」は " + E("eat / have breakfast") + "。" + E("breakfast") + " にはふつう冠詞をつけない。<br><b>ポイント</b>：一般論の「〜すべきだ」は、主語を " + E("you") + " にすると自然な英語になる。"},
 {"lv": "C", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>外国語を学ぶ利点は、その言語を話せるようになることだけではない。自分の母語を新しい目で見られるようになることも、大きな利点の一つである。",
  "a": E("Learning a foreign language does more than enable you to speak it. One of its greatest benefits is that it also lets you see your native language in a new light."),
  "s": "和文和訳：「外国語を学ぶことは、その言語を話せるようにする以上のことをしてくれる。最大の利点の一つは、母語を新しい観点から見させてくれることだ」と、動名詞 " + E("Learning a foreign language") + " を主語にして組み立てた。<br>別解（日本語の構造に近い形）：" + E("The advantage of learning a foreign language is not just that you can speak it. Being able to look at your own language from a new point of view is also a great advantage.") + "<br>採点のポイント：①「〜だけではない」を " + E("not just / not only / more than") + " で表せているか。②「話せるようになる」は " + E("can speak / be able to speak / learn to speak") + "。" + E("become to speak") + " は誤り（" + E("become") + " の後ろに " + E("to") + " 不定詞はこない）。" + E("come to do") + " は " + E("understand, like, know") + " など心の状態を表す動詞と使うのがふつう。③「母語」は " + E("native language / mother tongue / first language") + "。④「新しい目で」は " + E("in a new light / from a new perspective / with fresh eyes") + "。" + E("with new eyes") + " も通じるが、" + E("by new eyes") + " は誤り。<br><b>ポイント</b>：「A だけではない。B も…」という日本語の2文は、英語では " + E("not only A but also B") + " の論理でまとめると、つながりがはっきりする。"},
 {"lv": "C", "tag": "和文英訳", "q": "次の日本語を英語に直せ。<br>便利な道具が増えるにつれて、私たちは待つことが苦手になってきているのかもしれない。ほんの数分の待ち時間でさえ、スマートフォンを取り出さずにはいられない人も多い。",
  "a": E("As convenient devices become more common, we may be getting worse at waiting. Many people cannot help taking out their smartphones even when they only have to wait for a few minutes."),
  "s": "和文和訳：「便利な道具が増える」→「便利な機器がより一般的になる」、「待つことが苦手になってきている」→「待つのが下手になりつつある」。<br>別解：" + E("With more and more convenient tools around us, we may be losing the ability to wait. Many people find it hard to wait even a few minutes without checking their smartphones.") + "<br>採点のポイント：①「〜につれて」は " + E("as ＋ S V") + "（比較級や " + E("become, increase") + " などの変化を表す語と組み合わせる）、または " + E("with ～") + "。②「苦手になってきている」は進行形で変化を表す（" + E("be getting worse at doing / be losing the ability to do") + "）。" + E("be bad at") + " だけでは「〜になってきている」という変化が出ない。③「〜せずにはいられない」は " + E("cannot help doing / cannot help but do") + "。④ " + E("Many people") + " に合わせて " + E("their smartphones") + " と複数形にする。⑤「〜かもしれない」は " + E("may / might") + "。<br><b>ポイント</b>：長い日本語は、文ごとに「主語・動詞・時制」を先に決めてから肉づけする。2文目の「人も多い」は " + E("Many people ～") + " を主語にすると書きやすい。"},
]}}

def verify():
    its = CH[NO]["items"]
    lv = [it["lv"] for it in its]
    assert lv.count("A") == 4 and 4 <= lv.count("B") <= 5 and lv.count("C") == 2, lv
    assert lv == sorted(lv), "A→B→C の順に並べる"
    for i, it in enumerate(its, 1):
        assert it["lv"] in ("A", "B", "C") and all(str(it[k]).strip() for k in ("tag", "q", "a", "s")), i
        txt = it["q"] + it["a"] + it["s"]
        assert "$" not in txt and "( )" not in txt, i
        for t in ("span", "u", "b", "p", "table", "tr", "td", "th"):
            assert len(re.findall(rf"<{t}[ >]", txt)) == txt.count(f"</{t}>"), (i, t)
        assert "<b>ポイント</b>" in it["s"], i
        if it["tag"].endswith("4択"):
            assert all(c in it["q"] for c in "①②③④"), i
        for c in re.findall("[①-⑩]", it["a"]):   # 答えの番号が選択肢の中にあるか
            assert c in it["q"], (i, c)
        if it["tag"] == "和文英訳":               # 英訳問題は模範解答・別解・採点のポイントをそろえる
            assert it["a"].startswith('<span class="en">') and "別解" in it["s"] and "採点のポイント" in it["s"], i
