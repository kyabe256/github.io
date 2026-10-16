"""問題集 第17章 パラグラフ・リーディング。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号・長文の語数・要約の字数）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

def P(s):
    return f'<p class="en">{s}</p>'

def wc(s):
    """英文の語数（タグを除き、空白で区切った語のうち英字・数字を含むもの。ハイフンでつないだ語は1語）"""
    return len([w for w in re.sub(r"<[^>]+>", " ", s).split() if re.search(r"[A-Za-z0-9]", w)])

NO = 17

# ---- C1 の長文 ----
L1 = [
 "Boredom has a bad reputation. Most of us try to escape it as quickly as possible, and modern technology makes this easier than ever. Whenever we have to wait for a bus or stand in line at a store, we can take out our phones and fill the empty minutes with videos, games, or messages. As a result, many people now go through an entire day without feeling bored even once.",
 "At first glance, this seems like progress. ( 1 ), some psychologists argue that we may be losing something valuable. When the mind has nothing to focus on, it begins to wander. It replays past events, imagines possible futures, and makes unexpected connections between ideas. <u>This</u> is not wasted time. Many people report that their best ideas come to them not while they are working hard at a desk but while they are walking, taking a shower, or staring out of a train window.",
 "Boredom may also play a role in motivation. The uncomfortable feeling it produces works like a signal, telling us that our current situation is not satisfying and that we should look for something more meaningful to do. If we always silence this signal with our phones, we may never ask ourselves what we really want.",
 "None of this means that we should try to be bored all the time. Long periods of boredom can lead to stress and unhealthy habits. However, allowing ourselves a few quiet moments each day, without reaching for a screen, might be one of the simplest ways to think more creatively and to understand ourselves better.",
]
N1 = wc(" ".join(L1))

# ---- C2 の要約用の英文 ----
L2 = ("Around the world, thousands of languages are spoken only by small communities, and many of them are in danger of disappearing. "
      "When parents believe that a major language such as English or Spanish will give their children better jobs, they often stop using their own language at home. "
      "Within a generation or two, the local language may have no speakers left. This loss matters for more than the community itself. "
      "Each language contains a unique way of describing the world, including knowledge about local plants, animals, and traditions that may not exist anywhere else. "
      "Fortunately, the situation is not hopeless. In several regions, communities have started language classes for children, recorded the stories of elderly speakers, and created apps for learning vocabulary. "
      "These efforts show that a language can survive when its speakers see it not as a burden but as something worth passing on.")
N2 = wc(L2)
SUM2 = "経済的理由で親が子に母語を使わなくなり、多くの少数言語が消滅の危機にある。言語は独自の知識を含み損失は大きいが、話者が価値を認めて継承に努めれば存続できる。"

CH = {NO: {
"goal": "段落の主題文と支持文、つなぎ語（ディスコースマーカー）、段落どうしの関係をつかみ、長文の要旨を速く正確に読み取れるようにする。",
"items": [
 {"lv": "A", "tag": "空所補充", "q": "（　）に入る最も適切なものを選べ。<br>" + E("Many people think that cats are independent animals that do not care much about humans. (　), recent studies suggest that cats form strong bonds with their owners.") + "<br>① " + E("However") + "　② " + E("Therefore") + "　③ " + E("For example") + "　④ " + E("In addition"),
  "a": "①",
  "s": "前の文「猫は人間にあまり関心のない自立した動物だと多くの人が考えている」と、後ろの文「猫は飼い主と強い絆を結ぶ」は内容が<b>対立</b>している → 逆接の " + E("However") + "。<br><b>ポイント</b>：" + E("Many people think ～") + "（一般の考え）で始まる段落は、そのあと " + E("However / But / In fact") + " で筆者の主張や新しい事実に転換することが多い。"},
 {"lv": "A", "tag": "空所補充", "q": E("Regular exercise has many benefits for the body. (　), it strengthens the heart and helps people sleep better.") + "<br>① " + E("For example") + "　② " + E("However") + "　③ " + E("Otherwise") + "　④ " + E("In contrast"),
  "a": "①",
  "s": "前の文が「多くの利点」という<b>抽象</b>、後ろの文が「心臓を強くする・よく眠れる」という<b>具体</b> → 例示の " + E("For example") + "。<br><b>ポイント</b>：抽象 → 具体の流れでは " + E("For example / For instance") + "、具体 → 抽象（まとめ）の流れでは " + E("In short / In other words / Thus") + "。"},
 {"lv": "A", "tag": "主題文", "q": "次の段落の主題文（トピック・センテンス）を①〜④から選べ。<br>" + E("① Bicycles are becoming an important part of city life around the world. ② In many European cities, special lanes have been built so that people can cycle safely. ③ Some companies now pay their employees a small amount for every kilometer they cycle to work. ④ Bike-sharing services have also spread rapidly in Asian cities."),
  "a": "①",
  "s": "②〜④は、いずれも①「自転車は世界中で都市生活の重要な一部になりつつある」の<b>具体例</b>（ヨーロッパの専用レーン、企業の手当、アジアの自転車シェア）。①が段落全体をまとめる主題文。<br><b>ポイント</b>：主題文は、段落の他の文を「傘」のように包む一般的な文。段落の最初（ときに最後）に置かれることが多い。"},
 {"lv": "A", "tag": "不要文", "q": "次の段落の流れに合わない文を①〜④から選べ。<br>" + E("Sleep plays a key role in learning. ① While we sleep, the brain sorts and stores the information it took in during the day. ② Students who get enough sleep tend to remember more of what they studied. ③ Many students drink coffee simply because they like its taste. ④ For this reason, staying up all night before a test may do more harm than good."),
  "a": "③",
  "s": "主題文は第1文「睡眠は学習に重要な役割を果たす」。①睡眠中の脳の働き、②十分な睡眠と記憶、④だから徹夜は逆効果、と「睡眠と学習」の話が続く。③「味が好きだからコーヒーを飲む」は睡眠とも学習とも関係がない。③を除くと、②から④の " + E("For this reason") + " へ自然につながる。<br><b>ポイント</b>：不要文は、段落に出てくる語（ここでは " + E("students") + "）を含みながら主題から外れている文であることが多い。"},
 {"lv": "B", "tag": "要旨", "q": "次の段落の要旨として最も適切なものを選べ。<br>" + E("Trees in cities do more than make streets look attractive. They provide shade that can lower the temperature of the surrounding area by several degrees in summer. Their leaves catch dust and other tiny particles, which helps keep the air cleaner. In addition, people who live near parks and tree-lined streets often report feeling less stressed. For these reasons, a growing number of cities are planting trees not as decoration but as an essential part of public health planning.") + "<br>① 都市の木は美観のために植えられてきたが、維持に費用がかかりすぎる。<br>② 都市の木は気温や空気、人の心に良い影響を与えるため、健康を守る手段として植えられるようになっている。<br>③ 夏の都市の気温を下げるには、木を植えるより道路を減らすほうが効果的である。<br>④ 公園の近くに住む人は、そうでない人より収入が多い傾向がある。",
  "a": "②",
  "s": "第1文 " + E("do more than make streets look attractive") + "（街並みを美しく見せる以上のことをする）が主題文。続く " + E("They provide shade ... / Their leaves catch dust ... / In addition, ...") + " が具体例（気温を下げる・空気をきれいにする・ストレスを減らす）、最終文 " + E("For these reasons") + " がまとめ。②がこれらをすべて含んでいる。①③④は本文に書かれていない。<br><b>ポイント</b>：要旨は「主題文＋まとめの文」から組み立て、具体例の細部は追いすぎない。本文にない情報を加えた選択肢や、具体例の一部だけを述べた選択肢は不正解。"},
 {"lv": "B", "tag": "文の並べかえ", "q": "次の文に続く (A)〜(C) を、意味が通るように並べかえよ。<br>" + E("Many people believe that doing several things at once makes them more productive.") + "<br>(A) " + E("As a result, tasks take longer to finish, and more mistakes are made.") + "<br>(B) " + E("In reality, however, the brain does not handle two tasks at the same time; it switches rapidly between them.") + "<br>(C) " + E("Each switch costs a little time and attention.") + "<br>① (A)→(B)→(C)　② (B)→(C)→(A)　③ (C)→(A)→(B)　④ (B)→(A)→(C)",
  "a": "②",
  "s": "冒頭の文「同時にいくつものことをすると生産性が上がると多くの人が信じている」→ (B) " + E("In reality, however") + "（しかし実際は）で一般の考えを否定し、「脳は2つの作業をすばやく切り替えているだけ」と述べる → (C) " + E("Each switch") + "（その切り替え1回ごとに）は (B) の " + E("switches") + " を受ける → (A) " + E("As a result") + " で結果（時間がかかり、ミスが増える）。<br><b>ポイント</b>：並べかえは<b>つなぎ語</b>（" + E("however, as a result") + "）と、<b>前の語句を受ける語</b>（" + E("each switch, this, such") + "）を手がかりにする。"},
 {"lv": "B", "tag": "指示語", "q": "次の英文を読み、問いに答えよ。<br>" + E("Some elementary schools have stopped giving homework to their students. Supporters of <u>this change</u> argue that young children need time to play, rest, and spend time with their families after school. Critics, on the other hand, worry that without homework, children will not develop good study habits.") + "<br>問1　下線部 " + E("this change") + " の内容を日本語で具体的に答えよ。<br>問2　支持する人と批判する人の意見を、それぞれ日本語で簡潔にまとめよ。",
  "a": "問1 一部の小学校が児童に宿題を出すのをやめたこと。　問2 支持：子どもには放課後に遊び、休み、家族と過ごす時間が必要だ。批判：宿題がないと、子どもによい学習習慣が身につかない。",
  "s": "問1　" + E("this ＋ 名詞") + " は直前の文の内容を受ける。" + E("change") + "（変化）にあたるのは「宿題をやめた」こと。<br>問2　" + E("Supporters ... argue that ～") + " と " + E("Critics, on the other hand, worry that ～") + " が対比されている。" + E("on the other hand") + "（一方）は、対立する2つの立場を並べる目印。<br><b>ポイント</b>：指示語の答えは、指示語の位置に<b>当てはめて意味が通るか</b>を必ず確かめる。"},
 {"lv": "B", "tag": "結論文", "q": "空所に入る文として最も適切なものを選べ。<br>" + E("Language changes constantly. Words such as “cloud” and “stream” have taken on new meanings with the spread of digital technology. Expressions that once sounded strange to older people are now part of everyday speech, while some words that were common fifty years ago are rarely heard today. (　)") + "<br>① " + E("Therefore, no dictionary can ever be completely up to date.") + "<br>② " + E("Digital technology is harmful to young people.") + "<br>③ " + E("Older people speak more slowly than young people.") + "<br>④ " + E("Most English words have only one meaning."),
  "a": "①",
  "s": "主題文は第1文「言語は絶えず変化する」。具体例（新しい意味を持つようになった語、日常語になった表現、使われなくなった語）のあとに、" + E("Therefore") + " で「だから、どんな辞書も完全に最新ではありえない」という結論が自然に導かれる。②③は主題と無関係。④は " + E("cloud") + " や " + E("stream") + " の例（意味が増えた）と矛盾する。<br><b>ポイント</b>：段落の最後の文は、主題文を別の角度から言いかえたまとめや結論になることが多い。"},
 {"lv": "C", "tag": "長文", "q": "次の英文を読み、問いに答えよ。" + "".join(P(x) for x in L1) +
  "問1　空所 ( 1 ) に入る最も適切なものを選べ。　① " + E("However") + "　② " + E("For example") + "　③ " + E("Therefore") + "　④ " + E("In other words") + "<br>"
  "問2　下線部 " + E("This") + " が指す内容を、日本語で説明せよ。<br>"
  "問3　第3段落の内容と一致するものを選べ。<br>"
  "　① 退屈によって生じる不快な感覚は、今の状況に満足していないことを知らせ、より意味のあることを探すよう促す合図になる。<br>"
  "　② 退屈を感じたら、すぐに携帯電話で気分を切りかえるのがよい。<br>"
  "　③ 退屈を感じやすい人ほど、物事に対する意欲が低い。<br>"
  "　④ 退屈は、自分が本当に望むものを考える妨げになる。<br>"
  "問4　本文全体の主旨として最も適切なものを選べ。<br>"
  "　① 1日に少しでも画面から離れて静かな時間を持つことは、創造的に考え、自分を理解することにつながりうる。<br>"
  "　② 長い時間退屈でいればいるほど、人は創造的になる。<br>"
  "　③ よいアイデアは、机に向かって懸命に働いているときにこそ生まれる。<br>"
  "　④ 退屈は現代の技術によってなくなったので、もはや考える必要はない。",
  "a": "問1 ①　問2 何も集中する対象がないときに心がさまよい始め、過去の出来事を思い返したり、起こりうる未来を想像したり、考えどうしを思いがけない形で結びつけたりすること。　問3 ①　問4 ①",
  "s": f"本文は {N1}語。段落の役割は次のとおり。"
  "<table class=\"l w\"><tr><th>段落</th><th>役割</th><th>内容</th></tr>"
  "<tr><td>第1段落</td><td>導入（一般の状況）</td><td>退屈は嫌われ、技術のおかげで一度も退屈せずに1日を過ごせるようになった</td></tr>"
  "<tr><td>第2段落</td><td>転換・主張①</td><td>しかし価値あるものを失っているかもしれない。心がさまよう時間はむだではない</td></tr>"
  "<tr><td>第3段落</td><td>主張②（追加）</td><td>退屈は「今の状況に満足していない」と知らせ、動機につながる合図</td></tr>"
  "<tr><td>第4段落</td><td>譲歩＋結論</td><td>長い退屈は有害だが、毎日少し画面から離れる時間は創造性と自己理解に役立つ</td></tr></table>"
  "問1　前の「一見、進歩のように思える」と、後ろの「価値あるものを失っているかもしれない」が対立 → " + E("However") + "。<br>"
  "問2　" + E("This") + " は直前の2文（" + E("When the mind has nothing to focus on, it begins to wander. It replays ... ideas.") + "）の内容を受ける。直後の " + E("is not wasted time") + "（むだな時間ではない）に当てはめて意味が通ることも確かめる。<br>"
  "問3　①は " + E("The uncomfortable feeling it produces works like a signal, telling us that ... we should look for something more meaningful to do") + " の言いかえ。②は本文の " + E("If we always silence this signal with our phones") + " と逆の内容、④も「退屈が考えるきっかけになる」という本文と逆。③は書かれていない。<br>"
  "問4　筆者の主張は最終段落の " + E("However") + " 以下（①）。②は " + E("Long periods of boredom can lead to stress") + " と矛盾、③は第2段落の内容と逆、④は第2段落以降の主張と合わない。<br>"
  "<b>ポイント</b>：長文では、各段落の役割（導入・転換・追加・譲歩・結論）を1行でメモしながら読む。" + E("At first glance") + "（一見）、" + E("None of this means ～. However, ...") + "（〜というわけではない。しかし…）は、筆者の本当の主張が後ろにくる合図。"},
 {"lv": "C", "tag": "要約", "q": "次の英文の要旨を、70〜80字の日本語でまとめよ。" + P(L2),
  "a": SUM2 + f"（{len(SUM2)}字）",
  "s": f"本文は {N2}語。流れは「問題（少数言語の消滅）→ 原因（親が経済的な理由で大言語を選ぶ）→ なぜ問題か（各言語は独自の世界の見方・知識を含む）→ 希望（" + E("Fortunately") + " 以下：継承の取り組み）」。<br>"
  "採点のポイント：① 多くの言語が消滅の危機にあることと、その原因　② 言語が失われると独自の知識や世界の見方も失われること　③ 話者が言語の価値を認めて受け継ごうとすれば存続できること。この3点がそろえば満点。授業・録音・アプリなどの具体例は字数が足りなければ省いてよい。<br>"
  "<b>ポイント</b>：要約では<b>具体例を削り、論理の骨組み（問題 → 理由 → 解決）を残す</b>。" + E("Fortunately, ...") + " や最終文 " + E("These efforts show that ～") + " のような「まとめ」の文は、必ず要約に反映させる。"},
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
    assert 200 <= N1 <= 350, N1                 # 長文の語数
    assert f"{N1}語" in its[-2]["s"] and f"{N2}語" in its[-1]["s"]
    assert 70 <= len(SUM2) <= 80, len(SUM2)     # 要約の字数
    # 長文が段落ごとに欠けずに問題文に入っているか
    assert "".join(P(x) for x in L1) in its[-2]["q"] and P(L2) in its[-1]["q"]
