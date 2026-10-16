"""問題集 第21章 自由英作文。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号・模範解答の語数・別解と採点のポイントの有無）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

def wc(s):
    """英文の語数（タグを除き、空白で区切った語のうち英字・数字を含むもの。ハイフンでつないだ語は1語）"""
    return len([w for w in re.sub(r"<[^>]+>", " ", s).split() if re.search(r"[A-Za-z0-9]", w)])

NO = 21

# ---- 模範解答と別解（語数を数えて、指定の範囲に入っているか点検する） ----
R1 = "Learning to cook helps students develop healthy eating habits for the rest of their lives."
R2 = "Cooking classes teach students how to prepare balanced meals on their own."
M50 = ("I prefer living in a city. First, public transportation is convenient, so I can go to school, museums, and libraries easily without a car. "
       "Second, cities offer more chances to meet people from different backgrounds, which helps me broaden my view of the world. "
       "For these reasons, city life suits me better.")
A50 = ("I would rather live in the countryside. The air is clean and the surroundings are quiet, so I can relax and sleep well. "
       "Also, people in small communities often know and help each other. "
       "Although shopping may be less convenient, I think a peaceful and friendly environment is more important for a happy life.")
M100 = ("I disagree with the idea that students should be allowed to use smartphones during school hours. "
        "First, smartphones can easily distract students from their lessons. Even a single notification can break their concentration, and it takes time to focus again. "
        "Second, students need to communicate face to face during breaks. If everyone is looking at a screen, they lose valuable chances to build friendships and practice social skills. "
        "Some people argue that smartphones are useful for looking up information in class. However, schools can provide tablets for that purpose. "
        "For these reasons, I believe students should not use smartphones at school except in emergencies.")
M120 = ("I disagree with this opinion. It is true that AI translation tools have become very accurate, and they are helpful when we travel or read documents in other languages. "
        "However, I believe learning foreign languages is still necessary for two reasons. "
        "First, language is closely connected to culture. When we learn a language, we also learn how its speakers think and what they value, which a translation tool cannot teach us. "
        "Second, communication is not only about exchanging information. Building trust with someone is much easier when we speak to them directly in their language, even if we make mistakes. "
        "In conclusion, AI tools are useful, but they cannot replace the experience of learning a language ourselves.")
W = {k: wc(v) for k, v in dict(R1=R1, R2=R2, M50=M50, A50=A50, M100=M100, M120=M120).items()}

RUBRIC = ("<table class=\"l w\"><tr><th style=\"white-space:nowrap\">観点</th><th>チェックすること</th></tr>"
          "<tr><td style=\"white-space:nowrap\">内容</td><td>立場がはっきりしているか。理由が2つあり、それぞれに具体的な説明・例がついているか</td></tr>"
          "<tr><td style=\"white-space:nowrap\">構成</td><td>主張 → 理由1 → 理由2 →（反論への応答）→ 結論の順か。" + E("First / Second / However / For these reasons") + " などのつなぎ語が適切か</td></tr>"
          "<tr><td style=\"white-space:nowrap\">語彙</td><td>同じ語のくり返しを避けているか（" + E("smartphones → them / such devices") + "）。話題に合った語を使っているか</td></tr>"
          "<tr><td style=\"white-space:nowrap\">文法</td><td>主語と動詞の一致、名詞の単数・複数、時制、" + E("Because ～.") + " だけの文の断片がないか</td></tr>"
          "<tr><td style=\"white-space:nowrap\">語数</td><td>指定の語数の±10%程度に収まっているか</td></tr></table>")

CH = {NO: {
"goal": "「主張 → 理由 → 具体例 → 結論」の型で、指定の語数の中で論理的に書けるようにする。内容・構成・語彙・文法の観点から、自分の答案を見直せるようにする。",
"items": [
 {"lv": "A", "tag": "構成4択", "q": "次のテーマで英作文を書くとき、最初の文（主張文）として最も適切なものを選べ。<br>" + E("Topic: Should high school students wear school uniforms?") + "<br>① " + E("I think high school students should wear uniforms for two reasons.") + "<br>② " + E("Uniforms are a type of clothing.") + "<br>③ " + E("There are many different opinions about this topic.") + "<br>④ " + E("My sister's school has a blue uniform."),
  "a": "①",
  "s": "①は<b>立場</b>（賛成）と、理由がいくつあるかの<b>予告</b>を最初に示している。②は定義で主張がない。③は立場を示していない。④は個人的な事実で、主張ではない。<br><b>ポイント</b>：自由英作文の1文目は「立場＋予告」。" + E("I agree / disagree with ～.") + "、" + E("I think ～ for two reasons.") + " が基本形。"},
 {"lv": "A", "tag": "構成4択", "q": "（　）に入る最も適切なものを選べ。<br>" + E("I support this idea for two reasons. First, uniforms help students focus on their studies. (　), they reduce the cost of clothing for families.") + "<br>① " + E("Second") + "　② " + E("However") + "　③ " + E("In short") + "　④ " + E("For example"),
  "a": "①",
  "s": E("for two reasons") + " と予告し、" + E("First") + " で1つ目の理由を述べたので、2つ目は " + E("Second") + "（" + E("Also / In addition") + " も可）。② " + E("However") + " は逆接、③ " + E("In short") + " はまとめ、④ " + E("For example") + " は例示で、ここでは2つ目の理由を加える流れに合わない。<br><b>ポイント</b>：つなぎ語は、最初に<b>予告した構成</b>と一致させる。"},
 {"lv": "A", "tag": "構成4択", "q": "次の主張を支える具体例として最も適切なものを選べ。<br>" + E("Reading novels helps us understand other people.") + "<br>① " + E("For example, a novel lets us see the world through the eyes of a character whose life is very different from ours.") + "<br>② " + E("Novels are often more expensive than magazines.") + "<br>③ " + E("Some people prefer watching movies to reading.") + "<br>④ " + E("Many famous novels were written in the nineteenth century."),
  "a": "①",
  "s": "主張は「小説は他者の理解を助ける」。①は「自分とは大きく異なる人生を送る登場人物の目を通して世界を見られる」と、<b>なぜ他者の理解につながるのか</b>を具体的に示している。②③④は話題（小説・読書）は同じでも、主張を支えていない。<br><b>ポイント</b>：具体例は「主張が正しいことを示す場面」を選ぶ。話題が同じでも主張を支えない文は、内容の減点の対象になる。"},
 {"lv": "A", "tag": "文法4択", "q": "文法的に正しい文を選べ。<br>① " + E("I am agree with the idea.") + "<br>② " + E("I agree with the idea.") + "<br>③ " + E("I agree the idea.") + "<br>④ " + E("I am agreeing with the idea."),
  "a": "②",
  "s": E("agree") + " は動詞なので " + E("be") + " 動詞は不要（①は誤り）。人・意見に同意するときは " + E("agree with") + "（③は前置詞が必要）。" + E("agree") + " は状態を表す動詞で、ふつう進行形にしない（④は誤り）。なお、" + E("agree to ～") + " は提案・計画に同意する場合（" + E("agree to the plan") + "）。<br><b>ポイント</b>：" + E("I am agree") + " は自由英作文で最も多いミスの一つ。書き終えたら必ず見直す。"},
 {"lv": "B", "tag": "段落構成", "q": "次の (A)〜(D) を並べかえて、" + E("Topic: Is it better to study alone or with friends?") + " に対するまとまった意見文にしたい。最も適切な順序を選べ。<br>(A) " + E("For example, when I prepared for my last English test, I could concentrate for three hours in the library without any interruptions.") + "<br>(B) " + E("I believe that studying alone is more effective than studying with friends.") + "<br>(C) " + E("Therefore, I prefer to study by myself, especially before important exams.") + "<br>(D) " + E("This is mainly because I can focus on my own weak points at my own pace.") + "<br>① B→D→A→C　② B→A→D→C　③ D→B→A→C　④ B→D→C→A",
  "a": "①",
  "s": "主張 (B)「1人で勉強するほうが効果的だ」→ 理由 (D) " + E("This is mainly because ～") + "（自分の弱点に自分のペースで集中できる）→ 具体例 (A) " + E("For example ～") + "（前回の英語のテスト前、図書館で3時間集中できた）→ 結論 (C) " + E("Therefore ～") + "。<br><b>ポイント</b>：「主張 → 理由 → 例 → 結論」の型を体にしみこませる。" + E("This is because") + " は理由、" + E("For example") + " は例、" + E("Therefore / For these reasons") + " は結論の目印。"},
 {"lv": "B", "tag": "自由英作文", "q": "次の意見文の空所に、主張を支える理由を英語1文（10〜20語）で書け。<br>" + E("I think schools should offer cooking classes. (　) For example, students who can cook simple meals will eat fewer unhealthy snacks."),
  "a": E(R1) + f"（{W['R1']}語）",
  "s": "空所のあとの " + E("For example") + " の内容（簡単な料理ができる生徒は、不健康な間食が減る）が「健康的な食習慣」の例になっているので、理由は<b>健康・食習慣</b>に関するものにする。<br>別解：" + E(R2) + f"（{W['R2']}語）<br>採点のポイント：① 後ろの具体例とつながる理由になっているか。" + E("Cooking is fun.") + " のような文は理由として弱く、後ろの例ともつながらないので減点。② 語数（10〜20語）を守っているか。③ " + E("help ＋ O ＋ 原形") + "、" + E("how to do") + " などの形が正しいか。<br><b>ポイント</b>：理由は「後ろの具体例とつながるか」を確かめてから書く。"},
 {"lv": "B", "tag": "誤り訂正", "q": "次の英作文の下線部①〜④には、それぞれ誤りがある。正しく直せ。<br>" + E("Nowadays, many people <u>has</u>① a smartphone. Smartphones are very <u>convenience</u>②. However, some people use them too much. <u>Because they cannot stop watching videos.</u>③ I think we <u>should to</u>④ decide how much time we spend on our phones each day."),
  "a": "① " + E("has → have") + "　② " + E("convenience → convenient") + "　③ " + E("This is because they cannot stop watching videos.") + "（または前の文とつなげて " + E("some people use them too much because ...") + "）　④ " + E("should to → should"),
  "s": "① 主語 " + E("many people") + " は複数なので " + E("have") + "。② " + E("be") + " 動詞の後ろの補語は形容詞 " + E("convenient") + "（" + E("convenience") + " は名詞で「便利さ」）。③ " + E("Because") + " で始まる節だけでは文にならない（文の断片）。" + E("This is because ～.") + " とするか、前の文と1文にする。④ 助動詞の後ろは原形なので " + E("should decide") + "（" + E("ought to") + " と混同しない）。<br>別解：③は " + E("This is because") + " の代わりに " + E("For example, they cannot stop watching videos.") + " のように具体例として示してもよい。<br>採点のポイント：この4種類（主語と動詞の一致・品詞・文の断片・助動詞の形）は、採点で確実に減点される典型的な誤り。<br><b>ポイント</b>：自由英作文では、難しい表現より<b>基本的な誤りがないこと</b>が得点に直結する。"},
 {"lv": "B", "tag": "自由英作文", "q": "次のテーマについて、反対意見に触れたうえで自分の意見を述べる英文を、3文で書け。書き出しは " + E("Some people say that ...") + " とすること。<br>" + E("Topic: Should elementary schools stop giving homework?"),
  "a": E("Some people say that homework takes away children's time to play. It is true that play is important for young children. However, I believe a small amount of homework helps them develop good study habits, so schools should not stop giving it."),
  "s": "構成：① 反対意見の紹介（" + E("Some people say that ～") + "）→ ② いったん認める（譲歩：" + E("It is true that ～ / Certainly, ～") + "）→ ③ 反論と自分の結論（" + E("However, ～") + "）。<br>別解（逆の立場）：" + E("Some people say that homework helps children develop good study habits. That may be true for older students. However, I think young children learn more by playing and talking with their families, so elementary schools should stop giving homework.") + "<br>採点のポイント：① 反対意見を紹介しただけで終わらず、" + E("However") + " のあとに自分の主張と理由を書いているか。② 譲歩の部分で自分の立場がぶれていないか（認めるのは一部だけ）。③ " + E("homework") + " は不可算名詞（" + E("homeworks") + " は誤り）。<br><b>ポイント</b>：「譲歩 → 反論」の型を入れると、論理に深みが出て「内容」の評価が上がる。"},
 {"lv": "B", "tag": "自由英作文", "q": "次の質問に、理由を含めて50語程度の英語で答えよ。<br>" + E("Which do you prefer, living in a city or living in the countryside?"),
  "a": E(M50) + f"（{W['M50']}語）",
  "s": "構成：主張（都会がよい）→ 理由1（" + E("First") + "：公共交通が便利）→ 理由2（" + E("Second") + "：さまざまな人と出会える）→ 結論（" + E("For these reasons") + "）。50語程度なら、理由2つに短い説明を1つずつつければ十分。<br>別解（田舎の立場）：" + E(A50) + f"（{W['A50']}語）<br>採点のポイント：① 最初の文で立場を明示しているか（" + E("I prefer ～ / I would rather ～") + "）。② " + E("prefer A to B") + "、" + E("would rather do") + " の形が正しいか。③ 理由が「便利」「楽しい」だけで終わらず、具体的な説明があるか。④ 45〜55語程度に収まっているか。<br><b>ポイント</b>：短い英作文ほど、つなぎ語（" + E("First, Second, Also, Although") + "）で骨組みをはっきり見せる。"},
 {"lv": "C", "tag": "自由英作文", "q": "次のテーマについて、あなたの意見を100語程度の英語で書け。<br>" + E("Some people say that high school students should be allowed to use smartphones during school hours. Do you agree or disagree?"),
  "a": E(M100) + f"（{W['M100']}語）",
  "s": "構成：主張（反対）→ 理由1（集中をさまたげる）＋説明 → 理由2（休み時間の対面のコミュニケーションが減る）＋説明 → 反論への応答（" + E("Some people argue that ～. However, ～") + "）→ 結論。<br>別解（賛成の立場）の組み立て例：主張 " + E("I agree that students should be allowed to use smartphones at school.") + " → 理由1：調べ学習や辞書として授業に役立つ（" + E("They can look up words and information quickly.") + "）→ 理由2：災害や緊急時に家族と連絡がとれる（" + E("In an emergency, they can contact their families at once.") + "）→ 譲歩：使いすぎの心配はあるが、学校がルールを決めればよい（" + E("Of course, schools need clear rules about when phones can be used.") + "）→ 結論。<br>採点のポイント：" + RUBRIC +
  "<b>ポイント</b>：100語は「主張1文＋理由2つ×各2〜3文＋結論1文」で組み立てる。反論への応答（譲歩→反論）を1つ入れると、内容点が伸びやすい。"},
 {"lv": "C", "tag": "自由英作文", "q": "次の意見に賛成か反対かを明らかにし、その理由を120語程度の英語で書け。<br>" + E("“Thanks to AI translation tools, it is no longer necessary to learn foreign languages.”"),
  "a": E(M120) + f"（{W['M120']}語）",
  "s": "構成：主張（反対）→ 譲歩（" + E("It is true that ～") + "：翻訳ツールは正確で役に立つ）→ 反論（" + E("However, ～ for two reasons") + "）→ 理由1（言語は文化と結びついている）→ 理由2（信頼関係は相手の言語で直接話すことで築ける）→ 結論（" + E("In conclusion, ～") + "）。<br>別解（賛成の立場）の組み立て例：主張 " + E("I agree with this opinion.") + "（「ある程度」などとぼかさず、立場ははっきり書く）→ 理由1：外国語の習得には長い時間がかかるので、その時間を専門分野の勉強に使える（" + E("Students could use that time to study their own fields more deeply.") + "）→ 理由2：翻訳ツールは今後さらに正確になる → 譲歩：外国語を楽しみとして学ぶ価値は認める → 結論。<br>採点のポイント：① 冒頭で立場を明示しているか（" + E("I agree / disagree with this opinion.") + "）。② 譲歩を入れるときも、自分の立場とのつながりがはっきりしているか（" + E("It is true that ～. However, ～") + "）。③ 理由が「便利だから」「大切だから」で終わらず、なぜそう言えるのかを説明しているか。④ " + E("which a translation tool cannot teach us") + " のような関係詞を使うと、文を短く区切りすぎずに書ける。⑤ 110〜130語程度。<br><b>ポイント</b>：テーマが「〜はもう必要ない」という極端な意見のときは、相手の言い分を一部認めてから反論すると、説得力のある答案になる。"},
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
        if it["tag"] in ("自由英作文", "誤り訂正"):  # 模範解答・別解・採点のポイントをそろえる
            assert "別解" in it["s"] and "採点のポイント" in it["s"], i
    # 模範解答の語数が指定に合っているか
    assert 10 <= W["R1"] <= 20 and 10 <= W["R2"] <= 20, W
    assert 45 <= W["M50"] <= 55 and 45 <= W["A50"] <= 55, W
    assert 90 <= W["M100"] <= 110, W
    assert 110 <= W["M120"] <= 130, W
    for k in ("M50", "M100", "M120"):
        assert f"（{W[k]}語）" in " ".join(it["a"] for it in its), k
    # 模範解答・別解が欠けずに入っているか
    A = " ".join(it["a"] for it in its); S = " ".join(it["s"] for it in its)
    assert all(E(x) in A for x in (R1, M50, M100, M120)) and E(R2) in S and E(A50) in S
