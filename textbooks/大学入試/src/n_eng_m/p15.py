"""問題集 第15章 英文解釈① 文構造の把握。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

NO = 15
CH = {NO: {
"goal": "S・V・O・C と修飾語を見分け、長い主語・名詞節・関係詞節・挿入があっても文の骨組みをつかんで、正確に訳せるようにする。",
"items": [
 {"lv": "A", "tag": "構造4択", "q": "下線部①〜④のうち、文全体の述語動詞（主節の V）はどれか。<br>" + E("The girl <u>sitting</u>① next to the man who <u>teaches</u>② math <u>looks</u>③ like my cousin, who <u>lives</u>④ in Kobe."),
  "a": "③",
  "s": "骨組みは S＝" + E("The girl") + "、V＝" + E("looks") + "（" + E("look like A") + "「A に似ている」）。① " + E("sitting next to the man") + " は " + E("The girl") + " を後ろから修飾する現在分詞、② " + E("teaches") + " は関係代名詞 " + E("who") + "（先行詞 " + E("the man") + "）の節の中の動詞、④ " + E("lives") + " は非制限用法の " + E("who") + "（先行詞 " + E("my cousin") + "）の節の中の動詞。<br>和訳：「数学を教えている男性の隣に座っている女の子は、私のいとこに似ている。いとこは神戸に住んでいる」。<br><b>ポイント</b>：主語の名詞のあとに分詞・関係詞節が続くと主語が長くなる。<b>修飾語をカッコでくくり</b>、残った動詞が述語動詞。"},
 {"lv": "A", "tag": "文法4択", "q": "（　）に入る最も適切なものを選べ。<br>" + E("The number of people who use public transportation in this city (　) increasing.") + "　① " + E("is") + "　② " + E("are") + "　③ " + E("have") + "　④ " + E("being"),
  "a": "①",
  "s": "主語の中心は " + E("The number") + "（数）で単数 → " + E("is") + "。" + E("of people who use public transportation in this city") + " は修飾語。「この市で公共交通機関を利用する人の数は増えている」。" + E("A number of people") + "（多くの人々）なら複数扱い（" + E("A number of people are ...") + "）。<br><b>ポイント</b>：述語動詞の形は、修飾語を除いた<b>主語の中心の名詞</b>で決まる。"},
 {"lv": "A", "tag": "文法4択", "q": E("(　) he said at the meeting was completely true.") + "　① " + E("What") + "　② " + E("That") + "　③ " + E("Which") + "　④ " + E("It"),
  "a": "①",
  "s": "空所から " + E("meeting") + " までが主語、" + E("was") + " が述語動詞。" + E("he said") + " には " + E("said") + " の目的語が欠けているので、先行詞を含む関係代名詞 " + E("what") + "（〜こと・もの）が入る。「彼が会議で言ったことは、完全に正しかった」。② " + E("That") + " は後ろに完全な文が必要（" + E("That he was right is clear.") + "）。<br><b>ポイント</b>：名詞節を作る " + E("what") + " と " + E("that") + " は、<b>後ろが不完全か完全か</b>で選ぶ。"},
 {"lv": "A", "tag": "文法4択", "q": E("The man (　) I thought was honest turned out to be a liar.") + "　① " + E("who") + "　② " + E("whom") + "　③ " + E("which") + "　④ " + E("whose"),
  "a": "①",
  "s": "元の形は " + E("I thought (that) the man was honest") + "。先行詞 " + E("the man") + " は " + E("was honest") + " の<b>主語</b>なので主格の " + E("who") + "。" + E("I thought") + " の目的語だと勘違いして " + E("whom") + " を選ぶのが典型的なミス。「私が正直だと思っていたその男は、うそつきだとわかった」。<br><b>ポイント</b>：関係詞の直後の " + E("I think / I believe / they say") + " をカッコに入れて、関係詞が後ろの動詞の主語か目的語かを判断する。"},
 {"lv": "B", "tag": "和訳", "q": "下線部を和訳せよ。<br>" + E("<u>The ability to explain complex ideas in simple words is one of the most valuable skills a teacher can have.</u>"),
  "a": "複雑な考えを簡単な言葉で説明する能力は、教師が持ちうる最も価値のある技能の一つである。",
  "s": "S＝" + E("The ability to explain complex ideas in simple words") + "（" + E("to explain") + " は " + E("ability") + " を修飾する形容詞的用法の不定詞）、V＝" + E("is") + "、C＝" + E("one of the most valuable skills") + "。" + E("a teacher can have") + " は " + E("skills") + " を修飾する関係詞節（目的格の関係代名詞の省略）。<br><b>ポイント</b>：名詞の直後に「主語＋動詞」が続いたら、関係代名詞の省略を疑う（" + E("skills ← a teacher can have") + "）。"},
 {"lv": "B", "tag": "和訳", "q": "和訳せよ。<br>" + E("Modern technology has made it possible for people living in remote areas to receive medical advice online."),
  "a": "現代の技術のおかげで、へき地に住む人々がオンラインで医療上の助言を受けられるようになった。",
  "s": "構造：S＝" + E("Modern technology") + "、V＝" + E("has made") + "、O＝" + E("it") + "（形式目的語）、C＝" + E("possible") + "、真の目的語＝" + E("for people ... to receive medical advice online") + "。" + E("for people") + " は不定詞の意味上の主語、" + E("living in remote areas") + " は " + E("people") + " を修飾する現在分詞。直訳は「現代の技術は、へき地に住む人々がオンラインで医療上の助言を受けることを可能にした」。<br><b>ポイント</b>：" + E("make it possible for A to do") + " は無生物主語の構文。「S のおかげで A は〜できるようになった」と訳すと自然。"},
 {"lv": "B", "tag": "和訳", "q": "次の英文の主語と述語動詞を指摘し、全文を和訳せよ。<br>" + E("The cost of living in large cities such as Tokyo and London has risen sharply in recent years."),
  "a": "主語 " + E("The cost") + "／述語動詞 " + E("has risen") + "。和訳：東京やロンドンのような大都市での生活費は、近年急激に上がっている。",
  "s": E("of living in large cities") + " は " + E("cost") + " を修飾（" + E("the cost of living") + "＝生活費）、" + E("such as Tokyo and London") + " は " + E("large cities") + " の例。主語の中心は単数の " + E("cost") + " なので " + E("has") + "。" + E("London has risen") + " と読んで、ロンドンを主語と取り違えないこと。" + E("rise – rose – risen") + "（自動詞「上がる」）。<br><b>ポイント</b>：前置詞で始まるかたまり（" + E("of ～, in ～, such as ～") + "）は主語にならない。前置詞句をくくると主語が見える。"},
 {"lv": "B", "tag": "和訳", "q": "和訳せよ。<br>" + E("Whether the plan will succeed depends on how much support it receives from local residents."),
  "a": "その計画が成功するかどうかは、地元の住民からどれだけの支援を得られるかにかかっている。",
  "s": "S＝" + E("Whether the plan will succeed") + "（名詞節「〜かどうか」）、V＝" + E("depends on") + "、O＝" + E("how much support it receives from local residents") + "（間接疑問の名詞節。" + E("it") + "＝" + E("the plan") + "）。<br><b>ポイント</b>：文頭の " + E("Whether") + " は、節のあとに述語動詞がもう1つあれば名詞節（主語）、なければ副詞節（〜であろうとなかろうと）。主語になる名詞節を " + E("If") + " で始めることはできない。"},
 {"lv": "B", "tag": "整序", "q": "日本語に合うように（　）内の語句を並べかえよ。<br>あなたが昨日話していた本を貸してくれませんか。<br>" + E("Could ( about / lend / me / talking / the book / were / you / you ) yesterday?"),
  "a": E("Could you lend me the book you were talking about yesterday?"),
  "s": E("lend A B") + "「A に B を貸す」の B が " + E("the book") + "。その後ろに、目的格の関係代名詞が省略された節 " + E("you were talking about") + " が続く（前置詞 " + E("about") + " の目的語が欠けている）。<br><b>ポイント</b>：関係詞節の終わりに前置詞が残る形（" + E("talk about, look for, depend on") + "）に慣れる。" + E("the book about which you were talking") + " とも書けるが、話し言葉では前置詞を後ろに残す形がふつう。"},
 {"lv": "C", "tag": "和訳", "q": "下線部を和訳せよ。<br>" + E("<u>What makes this approach different from earlier ones is that it treats students not as passive receivers of knowledge but as active participants who can shape their own learning.</u>"),
  "a": "この手法がそれ以前の手法と異なるのは、生徒を知識の受け身の受け手としてではなく、自らの学びを形づくることのできる能動的な参加者として扱う点である。",
  "s": "骨組み：S＝" + E("What makes this approach different from earlier ones") + "（" + E("what") + " 節）、V＝" + E("is") + "、C＝" + E("that it treats students ...") + "（" + E("that") + " 節）。<br>・" + E("what makes A different from B") + " は「A を B と異なるものにしているもの」→「A が B と異なる点」と訳すと自然。" + E("ones") + "＝" + E("approaches") + "。<br>・" + E("treat O not as A but as B") + "「O を A としてではなく B として扱う」（" + E("not A but B") + " の A・B に " + E("as") + " の句が入った形）。<br>・" + E("who can shape their own learning") + " は " + E("participants") + " を修飾。<br><b>ポイント</b>：「" + E("What") + " 節＋ " + E("is") + " ＋ " + E("that") + " 節」は「〜なのは…ということだ」の型。文頭の " + E("What") + " 節がどこで終わるか（2つ目の動詞 " + E("is") + " の直前）を見きわめる。"},
 {"lv": "C", "tag": "構造・和訳", "q": "次の英文について、問いに答えよ。<br>" + E("The idea that plants can “communicate” with one another, which many scientists once dismissed as unrealistic, is now supported by a growing body of research.") + "<br>問1　" + E("that") + " の働きを説明せよ。<br>問2　" + E("which") + " の先行詞を答えよ。<br>問3　全文を和訳せよ。",
  "a": "問1 " + E("The idea") + " の内容を説明する同格の " + E("that") + "　問2 " + E("The idea that plants can “communicate” with one another") + "　問3 植物が互いに「意思を伝え合う」ことができるという考えは、かつて多くの科学者が非現実的だとして退けたものだが、今では増えつつある研究によって裏づけられている。",
  "s": "骨組みは S＝" + E("The idea") + "、V＝" + E("is supported") + "。<br>問1　" + E("that") + " のあと " + E("plants can communicate with one another") + " は欠けた要素のない完全な文なので、関係代名詞ではなく<b>同格の " + E("that") + "</b>（〜という考え）。<br>問2　" + E("dismiss A as B") + "「A を B だとして退ける」の A にあたるのが " + E("which") + "。「非現実的だとして退けられた」のは「考え」なので、先行詞は同格節を含む " + E("The idea ... one another") + " のかたまり。非制限用法（カンマつき）で、S と V の間に挿入されている。<br>問3　非制限用法の関係詞節は「〜だが」と補足的に訳し下すと自然。" + E("a growing body of research") + "「増えつつある多くの研究」。<br><b>ポイント</b>：S と V の間にカンマで挟まれた部分があれば、いったんくくって " + E("The idea ... is now supported") + " という骨組みを先に確定させる。"},
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
