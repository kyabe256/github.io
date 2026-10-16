"""問題集 第13章 接続詞と特殊構文。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

NO = 13
CH = {NO: {
"goal": "接続詞の意味（条件・譲歩・時）を区別し、倒置・強調構文・省略・同格の " + E("that") + " などの特殊構文を見抜いて、正確に訳し、書けるようにする。",
"items": [
 {"lv": "A", "tag": "文法4択", "q": "（　）に入る最も適切なものを選べ。<br>" + E("Hurry up. (　) you leave now, you will miss the last train.") + "　① " + E("If") + "　② " + E("Unless") + "　③ " + E("Because") + "　④ " + E("Though"),
  "a": "②",
  "s": E("unless") + "＝「〜しない限り・〜しなければ」（" + E("if ... not") + " に近い）。「急いで。今出発しないと終電に乗り遅れるよ」。① " + E("If") + " だと「今出発すれば乗り遅れる」となり、前の " + E("Hurry up.") + " と合わない。③ " + E("Because") + "、④ " + E("Though") + " も意味が通らない。<br><b>ポイント</b>：条件の副詞節の中は、未来のことでも現在形（" + E("leave") + "）。"},
 {"lv": "A", "tag": "文法4択", "q": E("I will lend you my notebook (　) you return it by Friday.") + "　① " + E("as long as") + "　② " + E("even if") + "　③ " + E("as far as") + "　④ " + E("unless"),
  "a": "①",
  "s": E("as long as") + "＝「〜しさえすれば・〜する限りは」（<b>条件</b>）。「金曜日までに返してくれるなら、ノートを貸してあげる」。③ " + E("as far as") + " は「〜する範囲では」（<b>範囲・程度</b>）で、" + E("as far as I know") + "（私の知る限りでは）のように使う。② " + E("even if") + "（たとえ〜でも）、④ " + E("unless") + "（〜しない限り）は意味が通らない。<br><b>ポイント</b>：日本語ではどちらも「〜する限り」。条件なら " + E("as long as") + "、範囲なら " + E("as far as") + "。"},
 {"lv": "A", "tag": "文法4択", "q": E("(　) you like it or not, you have to attend the meeting.") + "　① " + E("If") + "　② " + E("Whether") + "　③ " + E("Unless") + "　④ " + E("Since"),
  "a": "②",
  "s": E("whether A or not") + "「A であろうとなかろうと」（譲歩の副詞節）。「好むと好まざるとにかかわらず、その会議には出席しなければならない」。" + E("if") + " は副詞節で「〜であろうとなかろうと」の意味を表せない（" + E("if") + " が「〜かどうか」の意味になるのは名詞節で、主に動詞の目的語の位置）。<br><b>ポイント</b>：文中に " + E("or not") + " があれば " + E("whether") + " を第一候補にする。"},
 {"lv": "A", "tag": "文法4択", "q": E("No sooner had she finished her speech (　) the audience began to applaud.") + "　① " + E("when") + "　② " + E("than") + "　③ " + E("that") + "　④ " + E("before"),
  "a": "②",
  "s": E("No sooner had S done ... than ～") + "「S が…するとすぐに～」。否定の副詞 " + E("No sooner") + " が文頭に出たので、" + E("had she finished") + " と疑問文の語順に倒置している。「彼女がスピーチを終えるとすぐに、聴衆は拍手を始めた」。" + E("Hardly / Scarcely had S done ... when / before ～") + " と組み合わせを区別する。<br><b>ポイント</b>：" + E("sooner") + " は比較級なので、相棒は " + E("than") + "。"},
 {"lv": "B", "tag": "整序", "q": "日本語に合うように（　）内の語句を並べかえよ。文頭にくる語も小文字で示してある。<br>彼が何と言おうと、私は考えを変えるつもりはない。<br>" + E("( matter / I / change / says / what / no / he / won't / my mind ).") ,
  "a": E("No matter what he says, I won't change my mind."),
  "s": E("no matter what S V") + "＝" + E("whatever S V") + "「S が何を〜しようとも」（譲歩の副詞節）。譲歩の副詞節の中は、未来のことでも現在形（" + E("says") + "）。" + E("Whatever he says, I won't change my mind.") + " と同じ意味。<br><b>ポイント</b>：" + E("no matter what") + " は副詞節を作るだけで、名詞節（「〜するものは何でも」）の働きはない。名詞節なら " + E("whatever") + " を使う（" + E("You can take whatever you like.") + "）。"},
 {"lv": "B", "tag": "正誤", "q": "誤りを含む部分を指摘して正せ。<br>" + E("Only after the meeting was over she noticed that her phone was missing."),
  "a": E("she noticed → did she notice"),
  "s": E("Only ＋ 副詞（句・節）") + " が文頭に出ると、そのあとの<b>主節</b>が疑問文の語順に倒置する。" + E("after") + " 節の中（" + E("the meeting was over") + "）はふつうの語順のまま。一般動詞の過去形なので " + E("did she notice") + "。「会議が終わって初めて、彼女は電話がなくなっていることに気づいた」。<br><b>ポイント</b>：" + E("Never / Little / Only ... / Not until ... / Hardly") + " など、否定・限定の語句が文頭にきたら倒置。"},
 {"lv": "B", "tag": "和訳", "q": "和訳せよ。<br>" + E("There is little hope that the missing climbers will be found alive."),
  "a": "行方不明の登山者たちが生きて発見される見込みは、ほとんどない。",
  "s": E("that") + " 節は " + E("hope") + " の内容を説明する<b>同格の " + E("that") + "</b>（" + E("that") + " のあとが完全な文：" + E("the missing climbers will be found alive") + "）。" + E("little") + " は不可算名詞について「ほとんどない」（否定的）。" + E("a little hope") + " なら「少しは望みがある」。" + E("be found alive") + " は " + E("find O C") + "（O が C の状態で見つかる）の受動態で、" + E("alive") + " は補語。<br><b>ポイント</b>：同格の " + E("that") + " をとる名詞は " + E("fact, idea, news, hope, belief, possibility, chance") + " など。関係代名詞の " + E("that") + " と違い、後ろに欠けている要素がない。"},
 {"lv": "B", "tag": "書きかえ", "q": "ほぼ同じ意味になるように、空所に1語を補え。<br>" + E("While I was walking along the beach, I found a strange shell.") + "<br>＝ " + E("While (　) along the beach, I found a strange shell."),
  "a": E("walking"),
  "s": "時・条件・譲歩の副詞節（" + E("when, while, if, though") + " など）では、節の主語が主節の主語と同じとき、「<b>主語＋ " + E("be") + " 動詞</b>」をまとめて省略できる。" + E("I was") + " を省いて " + E("While walking") + "。「浜辺を歩いていると、変わった貝殻を見つけた」。<br><b>ポイント</b>：" + E("When in doubt, ask.") + "（迷ったら聞きなさい）、" + E("Though tired, she kept working.") + "（疲れていたが、彼女は働き続けた）も同じ省略。"},
 {"lv": "B", "tag": "和訳", "q": "次の2つの文を、違いがわかるように和訳せよ。<br>(1) " + E("It is important that you keep your promises.") + "<br>(2) " + E("It was at this small station that I first met my wife."),
  "a": "(1) 約束を守ることが大切だ。　(2) 私が初めて妻に会ったのは、この小さな駅だった。",
  "s": "(1) は<b>形式主語</b>の文：" + E("It") + " ＝ " + E("that") + " 節（約束を守ること）。(2) は<b>強調構文</b>：" + E("It was ～ that ...") + " の「～」に強調したい語句（" + E("at this small station") + "）を入れたもの。<br>見分け方：" + E("It is / was") + " と " + E("that") + " を取り除いて文が成り立てば強調構文。(2) は " + E("I first met my wife at this small station.") + " と完全な文に戻る。(1) は " + E("important you keep your promises") + " となり、文として成り立たない。<br><b>ポイント</b>：強調構文は「…のは～だ」と、強調された部分を文末に置いて訳すと自然。"},
 {"lv": "C", "tag": "和訳", "q": "下線部を和訳せよ。<br>" + E("<u>So rapidly has mobile technology developed over the past decade that few young people can imagine what life was like without smartphones.</u>"),
  "a": "この10年でモバイル技術はあまりにも急速に発達したので、スマートフォンのない生活がどのようなものだったかを想像できる若者はほとんどいない。",
  "s": "元の語順は " + E("Mobile technology has developed so rapidly over the past decade that ...") + "。" + E("so ＋ 副詞") + " が文頭に出たため、" + E("has mobile technology developed") + " と疑問文の語順に倒置している。" + E("so ... that ～") + "「とても…なので～」。<br>・" + E("few young people can imagine") + "：" + E("few") + " は「ほとんど〜ない」。「〜を想像できる若者はほとんどいない」と訳す。<br>・" + E("what life was like") + "：" + E("What is S like?") + "（S はどのようなものか）が名詞節になった形で、「生活がどのようなものだったか」。<br><b>ポイント</b>：文頭の「" + E("So ＋ 形容詞・副詞") + "＋倒置」を見たら、後ろの " + E("that") + " を探して " + E("so ... that") + " 構文だと見抜く。"},
 {"lv": "C", "tag": "英作文", "q": "次の日本語を英語に直せ。<br>彼女が本当の理由に気づいたのは、家に帰ってからのことだった。",
  "a": E("It was not until she got home that she realized the real reason."),
  "s": "「〜して初めて…した」「〜するまで…しなかった」は " + E("It was not until ～ that ...") + "（強調構文）で表せる。<br>別解：" + E("She did not realize the real reason until she got home.") + "／" + E("Not until she got home did she realize the real reason.") + "（否定の語句が文頭にきて倒置）<br>採点のポイント：① " + E("until") + " 節の中は過去形（" + E("got home") + "／" + E("came home") + "）。" + E("got to home") + " は誤り（" + E("home") + " は副詞）。② 倒置の文で " + E("she realized") + " のままにしない。③「（理由に）気づく」は頭で理解することなので " + E("realize") + " が適切（" + E("notice") + " は目や耳で気づく場合に使うことが多い）。<br><b>ポイント</b>：" + E("not until") + " は「〜まで…しない」→「〜して初めて…する」と発想を転換する。"},
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
