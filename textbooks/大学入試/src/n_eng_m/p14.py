"""問題集 第14章 語彙力の伸ばし方。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

NO = 14
CH = {NO: {
"goal": "コロケーション・多義語・派生語を例文の中で覚え、接頭辞・語根や前後の文脈を手がかりに、知らない語の意味を推測できるようにする。",
"items": [
 {"lv": "A", "tag": "語彙4択", "q": "（　）に入る最も適切なものを選べ。<br>" + E("Could you do me a (　)? I need someone to help me carry this box.") + "　① " + E("favor") + "　② " + E("help") + "　③ " + E("kindness") + "　④ " + E("service"),
  "a": "①",
  "s": E("do A a favor") + "「A の頼みを聞く」。" + E("Could you do me a favor?") + "（お願いがあるのですが）は決まった言い方。「手伝う」は " + E("help A") + " や " + E("give A a hand") + " で表し、" + E("do me a help") + " とは言わない。<br><b>ポイント</b>：動詞と名詞の組み合わせ（コロケーション）は、訳語ではなく<b>セットで</b>覚える。"},
 {"lv": "A", "tag": "語彙4択", "q": E("I was late for work because the traffic was (　).") + "　① " + E("heavy") + "　② " + E("many") + "　③ " + E("crowded") + "　④ " + E("much"),
  "a": "①",
  "s": "「交通量が多い」は " + E("The traffic is heavy.") + "（" + E("heavy traffic") + "）、少ないなら " + E("light") + "。" + E("traffic") + " は不可算名詞なので " + E("many") + " は使えない。" + E("crowded") + " は " + E("a crowded street / train") + " のように<b>場所・乗り物</b>が「混雑した」と言う語。" + E("The traffic was much.") + " とも言わない。<br><b>ポイント</b>：日本語の「多い・少ない」が、英語では " + E("heavy / light") + "（交通量）、" + E("large / small") + "（人口・金額）になる。"},
 {"lv": "A", "tag": "語彙4択", "q": "次の文の " + E("run") + " と同じ意味で使われているものを選べ。<br>" + E("She <u>runs</u> a small bakery near the station.") + "<br>① " + E("The river runs through the center of the city.") + "<br>② " + E("He runs five kilometers every morning.") + "<br>③ " + E("My uncle runs a hotel by the sea.") + "<br>④ " + E("The buses run every ten minutes."),
  "a": "③",
  "s": "問題文の " + E("run") + " は他動詞で「〜を経営する」。③も「海辺のホテルを経営している」。①「（川が）流れる」、②「走る」、④「（バスが）運行する」は、いずれも自動詞。<br><b>ポイント</b>：多義語は<b>自動詞か他動詞か、目的語に何がくるか</b>で意味を絞る。" + E("run ＋ 店・会社") + " なら「経営する」。"},
 {"lv": "A", "tag": "語彙4択", "q": E("This medicine may have a strong (　) on your heart.") + "　① " + E("affect") + "　② " + E("effect") + "　③ " + E("effective") + "　④ " + E("affection"),
  "a": "②",
  "s": E("have an effect on A") + "「A に影響を与える」。" + E("a strong (　)") + " の空所には名詞が入る。" + E("effect") + " は名詞（影響・効果）、" + E("affect") + " は動詞（〜に影響する）、" + E("effective") + " は形容詞（効果的な）、" + E("affection") + " は名詞だが「愛情」。<br><b>ポイント</b>：" + E("This medicine may affect your heart.") + " と動詞で書きかえられる。<b>品詞の区別</b>が語彙問題の第一歩。"},
 {"lv": "B", "tag": "文脈推測", "q": "下線部の語の意味に最も近いものを選べ。<br>" + E("The hikers were exhausted after walking for six hours, so they decided to take a short <u>respite</u> before climbing the last hill.") + "　① " + E("rest") + "　② " + E("risk") + "　③ " + E("meal") + "　④ " + E("route"),
  "a": "①",
  "s": "手がかりは " + E("exhausted") + "（疲れ切った）→ " + E("so") + "（だから）→ " + E("before climbing the last hill") + "（最後の丘を登る前に）。疲れたので登る前に短い「休息」をとった、と読むのが自然。" + E("respite") + " は「（つらいことの）一時的な休み・小休止」。② " + E("risk") + "（危険）、④ " + E("route") + "（道筋）は文脈に合わず、" + E("take a short meal") + " という言い方もしない。<br><b>ポイント</b>：知らない語は、前後の<b>因果（" + E("so") + ", " + E("because") + "）・対比（" + E("but") + "）・言いかえ（" + E("or") + ", " + E("that is") + "）</b>から意味を推測する。"},
 {"lv": "B", "tag": "空所補充", "q": "(a)(b) の空所に共通して入る1語を答えよ。<br>(a) " + E("Could you (　) an eye on my bag while I buy a ticket?") + "<br>(b) " + E("The class moved so fast that I couldn't (　) up with it."),
  "a": E("keep"),
  "s": "(a) " + E("keep an eye on A") + "「A から目を離さない・見張る」。(b) " + E("keep up with A") + "「A に遅れずについていく」。(b) だけなら " + E("catch up with") + "（追いつく）も考えられるが、(a) で " + E("catch an eye on") + " とは言わないので、両方に入るのは " + E("keep") + "。<br><b>ポイント</b>：基本動詞（" + E("keep, take, get, make, put") + "）は、後ろにつく名詞・前置詞・副詞とのセットで意味が決まる。"},
 {"lv": "B", "tag": "派生語", "q": "（　）内の語を適切な形に変えて、空所に入れよ。<br>(1) " + E("Her (　) to study abroad surprised her parents.") + "（" + E("decide") + "）<br>(2) " + E("The new library is easily (　) by wheelchair.") + "（" + E("access") + "）<br>(3) " + E("The city plans to (　) the main road next year.") + "（" + E("wide") + "）",
  "a": "(1) " + E("decision") + "　(2) " + E("accessible") + "　(3) " + E("widen"),
  "s": "(1) 所有格 " + E("Her") + " のあとで、" + E("to study abroad") + " に修飾される<b>名詞</b> → " + E("decision") + "（" + E("decide → decision") + "）。(2) " + E("is easily (　)") + " で、" + E("be") + " 動詞の補語になる<b>形容詞</b> → " + E("accessible") + "（利用できる・行きやすい）。(3) " + E("plans to (　)") + " なので<b>動詞</b>の原形 → " + E("widen") + "（接尾辞 " + E("-en") + " は「〜にする」：" + E("short → shorten, strength → strengthen") + "）。<br><b>ポイント</b>：空所の前後から品詞を決め、接尾辞で形を作る（名詞 " + E("-tion / -ment / -ness") + "、形容詞 " + E("-able / -ible / -ive") + "、動詞 " + E("-en / -ize / -ify") + "）。"},
 {"lv": "B", "tag": "語彙4択", "q": "下線部の意味として最も適切なものを選べ。<br>" + E("The old man spoke in an almost <u>inaudible</u> voice, so I had to ask him to repeat himself.") + "<br>① とても大きな　② 聞き取れない　③ 怒った　④ 心地よい",
  "a": "②",
  "s": E("in-") + "（否定）＋ " + E("aud") + "（聞く：" + E("audio, audience, audition") + "）＋ " + E("-ible") + "（〜できる）→「聞くことができない」。後半の " + E("so I had to ask him to repeat himself") + "（だからもう一度言ってもらわなければならなかった）も手がかりになる。「老人はほとんど聞き取れない声で話したので、もう一度言ってもらわなければならなかった」。<br><b>ポイント</b>：<b>語の分解</b>（接頭辞＋語根＋接尾辞）と<b>文脈</b>の両方で確かめると、推測の精度が上がる。"},
 {"lv": "B", "tag": "正誤", "q": "誤りを含む部分を指摘して正せ。<br>" + E("We should do an effort to reduce the amount of plastic waste we produce."),
  "a": E("do an effort → make an effort"),
  "s": "「努力する」は " + E("make an effort") + "。" + E("make") + " は " + E("make a decision / make a mistake / make progress / make a plan") + " のように「何かを生み出す」イメージ、" + E("do") + " は " + E("do one's homework / do the dishes / do damage") + " のように「作業・行為を行う」イメージで使い分けられる。「私たちは、自分たちが出すプラスチックごみの量を減らす努力をすべきだ」。<br><b>ポイント</b>：" + E("make / do / take / have") + " ＋名詞の組み合わせは、正誤問題の頻出ポイント。"},
 {"lv": "C", "tag": "文脈推測", "q": "次の英文を読み、下線部の語の意味を文脈から推測して日本語で答えよ。また、そう判断した根拠を2つ挙げよ。<br>" + E("My grandmother was remarkably <u>frugal</u>. She reused wrapping paper, repaired old clothes instead of buying new ones, and never left a light on in an empty room. Yet she was always generous when her neighbors needed help."),
  "a": "倹約な・質素な（むだづかいをしない）。根拠：直後の具体例／" + E("Yet") + " による " + E("generous") + " との対比",
  "s": "根拠①：2文目が " + E("frugal") + " の<b>具体例</b>になっている。包装紙を再利用する、新しい服を買わずに古い服を直す、誰もいない部屋の明かりをつけたままにしない → いずれも「むだを省く」行動。<br>根拠②：" + E("Yet") + "（それでも）で " + E("generous") + "（気前がよい）と<b>対比</b>されている。" + E("frugal") + " は「お金や物を節約する」方向の語であり、しかも「けち」とは区別されている（けちなら近所の人を助けないはず）。<br>全訳：「祖母は非常に倹約家だった。包装紙を再利用し、新しい服を買う代わりに古い服を直し、誰もいない部屋の明かりをつけたままにすることは決してなかった。それでも、近所の人が助けを必要としているときは、いつも気前がよかった」。<br><b>ポイント</b>：抽象的な語の直後には具体例が、逆接のあとには反対の性質がくる。この2つの手がかりで、辞書なしでも意味をかなり正確に絞れる。"},
 {"lv": "C", "tag": "和訳", "q": "下線部の語の意味に注意して、各文を和訳せよ。<br>(1) " + E("Few people <u>appreciated</u> how difficult the task really was.") + "<br>(2) " + E("The new rule will <u>apply</u> to all students, including those in their first year.") + "<br>(3) " + E("This rule does not <u>hold</u> in every case."),
  "a": "(1) その仕事が実際どれほど難しいかを正しく理解している人は、ほとんどいなかった。　(2) 新しい規則は、1年生を含むすべての生徒に適用される。　(3) この規則は、あらゆる場合に当てはまるわけではない。",
  "s": "(1) " + E("appreciate") + " は「感謝する」のほかに「（価値・重要性・難しさを）正しく理解する」。目的語が " + E("how difficult ...") + " という名詞節なので、「感謝する」では意味が通らない。<br>(2) " + E("apply to A") + "「A に適用される・当てはまる」（自動詞）。" + E("apply for a job") + "（仕事に応募する）と区別する。" + E("those in their first year") + " の " + E("those") + " は「人々」。<br>(3) 自動詞の " + E("hold") + " は「（理論・規則が）成り立つ・当てはまる」。" + E("not ... every") + " は部分否定で「すべての場合に〜わけではない」。<br><b>ポイント</b>：多義語は、最初に浮かぶ訳語で意味が通らないときこそ要注意。<b>目的語・前置詞・主語</b>が何かで意味を決める。"},
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
