"""問題集 第16章 英文解釈② 難構文。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

NO = 16
CH = {NO: {
"goal": "否定・比較の慣用表現、倒置、共通関係、挿入、省略、修飾語の分離、名詞構文など、直訳ではつまずく構文を見抜き、自然な日本語に訳せるようにする。",
"items": [
 {"lv": "A", "tag": "構文4択", "q": "次の英文の意味として最も適切なものを選べ。<br>" + E("He is the last person to break a promise.") + "<br>① 彼はいちばん最後に約束を破った人だ<br>② 彼は決して約束を破るような人ではない<br>③ 彼は約束を破ってばかりいる人だ<br>④ 彼は約束を破られると怒る人だ",
  "a": "②",
  "s": E("the last ＋ 名詞 ＋ to do") + "「最も〜しそうにない…」→「決して〜しない…」。直訳の「約束を破る最後の人」は、約束を破りそうな順に人を並べたら最後にくる人、つまり最も破りそうにない人ということ。<br><b>ポイント</b>：同じ発想の表現に " + E("the last thing I expected") + "（まったく予想していなかったこと）がある。"},
 {"lv": "A", "tag": "構文4択", "q": "次の英文の意味として最も適切なものを選べ。<br>" + E("She is not so much a singer as a poet.") + "<br>① 彼女は歌手ほど詩人ではない<br>② 彼女は歌手というよりむしろ詩人だ<br>③ 彼女は歌手でも詩人でもない<br>④ 彼女は歌手であり詩人でもある",
  "a": "②",
  "s": E("not so much A as B") + "「A というよりむしろ B」（＝" + E("B rather than A") + "）。" + E("She is a poet rather than a singer.") + " と同じ意味。直訳すると「彼女は、詩人であるほどには歌手ではない」で、重点は詩人の側にある。①は比べる2つの関係を取り違えた訳で、「歌手の面のほうが強い」という逆の意味になっている。<br><b>ポイント</b>：" + E("not so much A as B") + " は<b>重点が B</b>。" + E("not so much as do") + "（〜さえしない）とも区別する。"},
 {"lv": "A", "tag": "文法4択", "q": "（　）に入る最も適切なものを選べ。<br>" + E("(　) I known the truth, I would have told you at once.") + "　① " + E("Had") + "　② " + E("If") + "　③ " + E("Have") + "　④ " + E("Should"),
  "a": "①",
  "s": "仮定法過去完了 " + E("If I had known the truth, ...") + " の " + E("if") + " を省略すると、" + E("Had I known the truth") + " と倒置する。「もし本当のことを知っていたら、すぐにあなたに話したのに」。② " + E("If I known") + " は " + E("had") + " が欠けている。④ " + E("Should") + " の倒置は「万一〜なら」で、" + E("Should S ＋ 原形") + " の形になる。<br><b>ポイント</b>：文頭の " + E("Had / Were / Should ＋ S") + " のあとにカンマと主節が続いていたら、" + E("if") + " の省略による倒置。"},
 {"lv": "A", "tag": "構文4択", "q": "次の英文の意味として最も適切なものを選べ。<br>" + E("Money is no more the goal of life than a map is the goal of a journey.") + "<br>① 地図が旅の目的でないのと同様に、お金は人生の目的ではない<br>② お金は、地図が旅の目的である以上に、人生の目的である<br>③ お金も地図も、人生という旅の目的である<br>④ 地図を持たずに旅をするように、お金を持たずに生きるべきだ",
  "a": "①",
  "s": E("A is no more B than C is D") + "「A が B でないのは、C が D でないのと同じ」。" + E("than") + " 以下に「明らかに成り立たないこと」（地図は旅の目的ではない）を置いて、前半も成り立たないと強く否定する。<br><b>ポイント</b>：" + E("no more ... than") + " は「<b>両方とも否定</b>」と覚える。" + E("no less ... than") + "（〜と同様に…である）は「両方とも肯定」。"},
 {"lv": "B", "tag": "和訳", "q": "下線部を和訳せよ。<br>" + E("<u>Some people believe, and others strongly doubt, that artificial intelligence will one day replace teachers in the classroom.</u>"),
  "a": "人工知能がいつか教室で教師に取って代わると信じている人もいれば、それを強く疑っている人もいる。",
  "s": E("that") + " 節が " + E("believe") + " と " + E("doubt") + " の<b>共通の目的語</b>になっている（" + E("Some people believe [that ～], and others strongly doubt [that ～]") + "）。" + E("Some ～, and others ...") + " は「〜する人もいれば、…する人もいる」。<br><b>ポイント</b>：カンマで挟まれた " + E("and others strongly doubt") + " をいったん外すと、" + E("believe that ～") + " のつながりが見える。「" + E("A and B") + " ＋ 共通の要素」の型を見抜く。"},
 {"lv": "B", "tag": "和訳", "q": "和訳せよ。<br>" + E("The problem, it seems to me, lies not in the system itself but in the way it is used."),
  "a": "問題は、私が思うに、制度そのものにあるのではなく、その使われ方にある。",
  "s": E("it seems to me") + " は挿入（" + E("It seems to me that the problem lies ...") + " の主節が文中に入った形）。骨組みは " + E("The problem lies not in A but in B") + "「問題は A ではなく B にある」。" + E("lie in ～") + "「〜にある」。" + E("the way it is used") + "「それが使われる方法」→「その使われ方」（" + E("it") + "＝" + E("the system") + "）。<br><b>ポイント</b>：カンマで挟まれた " + E("I think / it seems to me / I believe") + " は、文頭に戻して読む。"},
 {"lv": "B", "tag": "和訳", "q": "次の英文の主語を指摘し、全文を和訳せよ。<br>" + E("Among the guests was a woman who had once worked with my father in London."),
  "a": "主語：" + E("a woman (who had once worked with my father in London)") + "。和訳：招待客の中に、かつてロンドンで私の父と一緒に働いたことのある女性がいた。",
  "s": "元の語順は " + E("A woman who had once worked ... was among the guests.") + "。場所を表す副詞句 " + E("Among the guests") + " が文頭に出て、「V（" + E("was") + "）＋ S」の倒置になっている。主語が長いので文末に回し、文のバランスをとっている。" + E("the guests was") + " を見て「主語と動詞の数が一致していない」と誤解しないこと。<br><b>ポイント</b>：文頭が前置詞句で、直後に " + E("be") + " 動詞や " + E("come, stand, lie") + " などがきたら、倒置を疑う。"},
 {"lv": "B", "tag": "和訳", "q": "名詞構文に注意して、全文を自然な日本語に訳せ。<br>" + E("His sudden departure from the company surprised everyone in the office."),
  "a": "彼が突然会社を辞めたので、職場の誰もが驚いた。",
  "s": E("His sudden departure from the company") + " は、" + E("He suddenly left the company.") + " という文を名詞のかたまりにしたもの（名詞構文。" + E("departure") + " は " + E("depart") + "「去る」の名詞形）。所有格 " + E("His") + " は意味上の主語、形容詞 " + E("sudden") + " は副詞「突然」に戻して訳す。無生物主語なので「〜したので、…が驚いた」と原因・結果の形にすると自然。直訳の「彼の会社からの突然の出発は」は不自然。<br><b>ポイント</b>：「所有格＋形容詞＋動作の名詞＋ " + E("of / from") + " ～」は<b>文に戻して</b>訳す（" + E("the rapid growth of the city") + "＝都市が急速に成長したこと）。"},
 {"lv": "B", "tag": "和訳", "q": "和訳せよ。<br>" + E("The longer a problem is ignored, the more difficult it becomes to solve."),
  "a": "問題は放置されればされるほど、解決するのが難しくなる。",
  "s": E("The ＋ 比較級 ～, the ＋ 比較級 ...") + "「〜すればするほど、ますます…」。元の文は " + E("a problem is ignored long") + " と " + E("it becomes difficult to solve") + "（" + E("it") + "＝" + E("a problem") + "。" + E("to solve") + " は " + E("difficult") + " を限定する不定詞で「解決するのが」）。それぞれの比較級が " + E("the") + " を伴って前に出ている。<br><b>ポイント</b>：" + E("the") + " 比較級構文は語順が崩れるので、<b>元の文に戻して</b>から訳すと構造がわかる。"},
 {"lv": "C", "tag": "和訳", "q": "下線部を和訳せよ。<br>" + E("<u>It is not that young people today are less interested in politics than their parents were; rather, they express their interest in ways that older generations do not always recognize.</u>"),
  "a": "今日の若者が、親たちがかつてそうであったより政治への関心が薄いというわけではない。むしろ若者は、年長の世代が必ずしも気づかない方法で、その関心を表しているのである。",
  "s": "・" + E("It is not that ～") + "「〜というわけではない」。後ろの " + E("rather") + "（むしろ）と組んで、「〜なのではなく、むしろ…なのだ」と誤解を打ち消して本当の主張を示す。<br>・" + E("than their parents were") + " は " + E("were (interested in politics)") + " の省略。<br>・" + E("ways that older generations do not always recognize") + "：" + E("that") + " は目的格の関係代名詞（先行詞 " + E("ways") + "）。" + E("not always") + " は部分否定「必ずしも〜ない」。<br><b>ポイント</b>：省略された語句は、前に出た同じ形（ここでは " + E("interested in politics") + "）を補って読む。部分否定と全部否定を訳し分ける。"},
 {"lv": "C", "tag": "和訳", "q": "下線部(1)(2)を和訳せよ。<br>(1) " + E("<u>A report was published last week that suggests the city's air quality has improved significantly.</u>") + "<br>(2) " + E("<u>Little did she imagine that the small shop she opened in her twenties would one day become a national chain.</u>"),
  "a": "(1) 市の大気の質が大幅に改善したことを示す報告書が、先週発表された。　(2) 20代で開いた小さな店がいつか全国チェーンになるとは、彼女は夢にも思わなかった。",
  "s": "(1) " + E("that suggests ～") + " は " + E("A report") + " を修飾する関係代名詞節（" + E("that") + " は主格）。主語に長い修飾語がつくと頭でっかちになるので、述語 " + E("was published last week") + " のあとに回されている（修飾語の<b>分離</b>）。" + E("suggests") + " のあとでは接続詞 " + E("that") + " が省略されている。<br>(2) " + E("Little") + "（少しも〜ない）が文頭に出て " + E("did she imagine") + " と倒置。" + E("Little did S know / imagine / dream") + " は「S は〜とは夢にも思わなかった」と訳すのが定番。" + E("she opened in her twenties") + " は " + E("the small shop") + " を修飾（関係代名詞の省略）。" + E("would") + " は過去から見た未来。<br><b>ポイント</b>：関係詞節が先行詞から離れていても、意味と数（" + E("suggests") + " は三人称単数 → " + E("a report") + "）から先行詞を決める。"},
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
