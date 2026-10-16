"""問題集 第19章 共通テスト リーディング。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号・長文の語数・計算問題の答え）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

def P(s):
    return f'<p class="en">{s}</p>'

def BOX(s):
    """掲示・ウェブページ・メールなどの資料を枠で囲む"""
    return f'<table class="l w"><tr><td><span class="en">{s}</span></td></tr></table>'

def wc(s):
    """英文の語数（タグを除き、空白で区切った語のうち英字・数字を含むもの。ハイフンでつないだ語は1語）"""
    return len([w for w in re.sub(r"<[^>]+>", " ", s).split() if re.search(r"[A-Za-z0-9]", w)])

NO = 19

# ---- B1 の料金計算（検算用） ----
FEE5, LUNCH, DISC = 18000, 600, 0.10
TOTAL = round(2 * FEE5 * (1 - DISC) + 2 * 5 * LUNCH)      # 姉妹2人・5日間・昼食つき

# ---- C1 の長文（記事） ----
T1 = "Fixing Things, Building Community"
L1 = [
 "Last November, a small event called a “repair café” started in our town's community hall. Once a month, residents can bring broken items, such as lamps, toasters, and torn clothes, and volunteers help them fix the items for free. The idea is simple: instead of throwing things away and buying new ones, people learn to repair what they already have.",
 "I first visited the café with my grandfather, who wanted to fix an old radio. A retired engineer named Mr. Ito showed us how to open the radio and find the problem. It turned out that only one small wire had come loose. Within twenty minutes, the radio was playing music again. My grandfather was delighted, and I was surprised at how easy the repair had been once someone explained it.",
 "Since then, I have volunteered at the café three times. According to the organizers, about 40 people come to each event, and roughly 70 percent of the items brought in are successfully repaired. That means fewer things end up in the trash. However, I believe the café's biggest benefit is not the reduction of waste. It is the conversations. Young people learn practical skills from older residents, and older residents enjoy sharing knowledge that might otherwise be forgotten.",
 "Of course, not everything can be fixed. Some modern devices are designed in ways that make repair almost impossible, and spare parts can be hard to find. Even so, I think every town should have a place like this. Next month, I am planning to bring my broken bicycle, and this time I want to try fixing it myself.",
]
N1 = wc(T1 + " " + " ".join(L1))

# ---- C2 の複数テキスト ----
LA = ("I think students should be allowed to use AI tools for homework, as long as they use them in the right way. "
      "In the future, most jobs will require us to work with AI, so school is the best place to learn how to use it wisely. "
      "For example, when I get stuck on a math problem late at night, an AI tool can explain the steps to me, just as a tutor would. "
      "Of course, simply copying answers is wrong. Teachers could ask us to write down how we used the tool, so that they can check that we are still thinking for ourselves.")
LB = ("Using AI tools for homework may seem convenient, but I am worried about what we might lose. "
      "The purpose of homework is not to produce correct answers but to practice thinking. "
      "If an AI tool does the difficult part for us, we will not develop that skill. "
      "Struggling with a problem for a while, even when it feels frustrating, is an important part of learning. "
      "I also think it is unfair, because some students can pay for better tools than others. "
      "I agree that we need to learn about AI, but this should happen in special lessons at school, where teachers can guide us, not at home.")
NA, NB = wc(LA), wc(LB)

TOUR = ("<table class=\"l w\"><tr><th>Tour</th><th>Day</th><th>Start</th><th>Length</th><th>Language</th></tr>"
        "<tr><td>A　Old Town Walk</td><td>Saturday</td><td>9:00 a.m.</td><td>2 hours</td><td>English</td></tr>"
        "<tr><td>B　River Cruise</td><td>Saturday</td><td>2:00 p.m.</td><td>1.5 hours</td><td>Japanese</td></tr>"
        "<tr><td>C　Food Market Tour</td><td>Sunday</td><td>10:00 a.m.</td><td>3 hours</td><td>English</td></tr>"
        "<tr><td>D　Night View Bus</td><td>Sunday</td><td>7:00 p.m.</td><td>2 hours</td><td>English</td></tr></table>")
TOUR = TOUR.replace("<td>", '<td class="en">').replace("<th>", '<th class="en">')

CH = {NO: {
"goal": "掲示・ウェブページ・メール・表・記事・複数の意見文などの実用的な英文から、必要な情報を速く探し出し、事実と意見を区別し、情報を照合して判断できるようにする。",
"items": [
 {"lv": "A", "tag": "掲示", "q": "次の掲示を読み、質問の答えとして最も適切なものを選べ。" + BOX("<b>Maple Hill Public Library — Summer Hours</b><br>Monday–Friday: 9:00 a.m. – 8:00 p.m.<br>Saturday: 10:00 a.m. – 5:00 p.m.<br>Sunday: Closed<br>* From July 20 to August 31, the study room on the second floor will be open until 9:00 p.m. on weekdays.") + E("Question: Until what time can you use the study room on a Wednesday in August?") + "<br>① " + E("5:00 p.m.") + "　② " + E("8:00 p.m.") + "　③ " + E("9:00 p.m.") + "　④ " + E("The study room is closed."),
  "a": "③",
  "s": "8月の水曜日は平日（" + E("weekdays") + "）で、注意書き（*）の期間（7月20日〜8月31日）に入るので、2階の自習室は午後9時まで使える。図書館の閉館時刻 " + E("8:00 p.m.") + " に飛びつかないこと。<br><b>ポイント</b>：掲示では、<b>注意書き（*、" + E("Note") + "）</b>に例外が書かれていることが多い。設問の条件（曜日・月）を本文の条件と1つずつ照合する。"},
 {"lv": "A", "tag": "事実と意見", "q": "あるリュックサックの商品レビューの文のうち、<b>意見</b>を述べているものを選べ。<br>① " + E("This backpack weighs 800 grams.") + "<br>② " + E("It has three outside pockets.") + "<br>③ " + E("It comes in five colors.") + "<br>④ " + E("It is the most comfortable backpack I have ever used."),
  "a": "④",
  "s": "①②③は重さ・ポケットの数・色の数で、確かめられる<b>事実</b>。④の " + E("the most comfortable ... I have ever used") + " は書き手の感じ方で<b>意見</b>。<br><b>ポイント</b>：" + E("I think, best, should, comfortable, beautiful") + " など、評価や判断を表す語があれば意見。数値・日時・固有名詞で確かめられる内容は事実。"},
 {"lv": "A", "tag": "メッセージ", "q": "次のメッセージのやりとりを読み、質問の答えとして最も適切なものを選べ。" + BOX("<b>Yuki:</b> Are we still meeting at the station at 10 tomorrow?<br><b>Sam:</b> Actually, could we make it 10:30? My piano lesson was moved to 9:30.<br><b>Yuki:</b> Sure. Then let's meet at the café next to the station instead. It's going to rain.<br><b>Sam:</b> Good idea. See you there!") + E("Question: Where and when will Yuki and Sam meet?") + "<br>① " + E("At the station at 10:00") + "　② " + E("At the station at 10:30") + "<br>③ " + E("At the café at 10:00") + "　④ " + E("At the café at 10:30"),
  "a": "④",
  "s": "時刻は " + E("Sam") + " の提案（" + E("could we make it 10:30?") + "）に " + E("Yuki") + " が " + E("Sure.") + " と応じて10時30分に変更。場所は " + E("Yuki") + " の提案（" + E("let's meet at the café ... instead") + "）に " + E("Sam") + " が " + E("Good idea.") + " と応じて駅の隣のカフェに変更。<br><b>ポイント</b>：やりとりの問題では、<b>最後に合意された内容</b>が答え。途中の変更を1つずつ追う。"},
 {"lv": "A", "tag": "図表", "q": "次の表は、ある高校の生徒200人に通学手段をたずねた結果である。表の内容と一致するものを選べ。"
  "<table class=\"l w\"><tr><th>" + E("Means of transportation") + "</th><th>" + E("Number of students") + "</th></tr><tr><td>" + E("Walking") + "</td><td>46</td></tr><tr><td>" + E("Bicycle") + "</td><td>72</td></tr><tr><td>" + E("Bus") + "</td><td>38</td></tr><tr><td>" + E("Train") + "</td><td>44</td></tr></table>"
  "① " + E("More students go to school by bus than by train.") + "<br>② " + E("Riding a bicycle is the most common way of getting to school.") + "<br>③ " + E("Fewer than 40 students walk to school.") + "<br>④ " + E("Half of the students use public transportation."),
  "a": "②",
  "s": "①バス38人＜電車44人なので誤り。②自転車72人が最多で正しい。③徒歩は46人なので誤り。④公共交通機関（バス＋電車）は82人で、200人の半分（100人）に届かないので誤り。<br><b>ポイント</b>：" + E("more / fewer than, the most, half") + " などの数量表現を、表の数値と1つずつ照合する。合計や割合が必要なときは、余白で計算する。"},
 {"lv": "B", "tag": "ウェブページ", "q": "次のウェブページを読み、質問の答えとして最も適切なものを選べ。" + BOX("<b>Riverside Summer Science Camp</b><br>Dates: August 5–9 (5 days)<br>Fee: 4,000 yen per day, or 18,000 yen for all five days<br>Lunch: 600 yen per day (optional)<br>* Brothers and sisters who join together get a 10% discount on the camp fee (lunch not included).") + E("Question: Two sisters will join the camp for all five days, and both will have lunch every day. How much will they pay in total?") + "<br>① " + E("32,400 yen") + "　② " + E("38,400 yen") + "　③ " + E("36,000 yen") + "　④ " + E("42,000 yen"),
  "a": "②",
  "s": f"(1) 参加費：5日間通しの 18,000円 × 2人 ＝ 36,000円。きょうだい割引10%で 36,000 × 0.9 ＝ 32,400円。(2) 昼食：600円 × 5日 × 2人 ＝ 6,000円（割引の対象外）。(3) 合計 32,400 ＋ 6,000 ＝ {TOTAL:,}円。<br>①は昼食代を忘れた額、③は割引も昼食も入れていない額、④は割引を忘れた額。<br><b>ポイント</b>：料金問題では、<b>割引の対象</b>（" + E("lunch not included") + "）と<b>まとめ買いの料金</b>（" + E("18,000 yen for all five days") + "）を読み落とさない。"},
 {"lv": "B", "tag": "出来事の順序", "q": "次のブログの記事を読み、(A)〜(D) を起こった順に並べたものを選べ。<br>" + E("Last spring, I decided to start a vegetable garden. First, I read several books about gardening, but they were too difficult for a beginner. So I joined a gardening course at the community center, where I learned how to prepare the soil. After the course ended, I visited a local farm to buy seeds that suit our climate. In June, I finally planted tomatoes and beans. By August, I was able to share my first harvest with my neighbors.") + "<br>(A) 地元の農場で種を買った　(B) 園芸講座に参加した　(C) 収穫を近所の人に分けた　(D) 園芸の本を読んだ<br>① D→B→A→C　② B→D→A→C　③ D→A→B→C　④ A→D→B→C",
  "a": "①",
  "s": "時や順序を表す語句をたどる：" + E("First") + "（本を読んだ：D）→ " + E("So") + "（講座に参加：B）→ " + E("After the course ended") + "（農場で種を買った：A）→ " + E("In June") + "（植えた）→ " + E("By August") + "（収穫を分けた：C）。<br><b>ポイント</b>：本文に書かれた順と実際に起こった順が違うことがある（" + E("before, after, had done") + "）。時を表す語句に印をつけながら読む。"},
 {"lv": "B", "tag": "メール", "q": "次のメールを読み、質問の答えとして最も適切なものを選べ。" + BOX("<b>To:</b> Ms. Clark<br><b>Subject:</b> Question about the essay contest<br><br>Dear Ms. Clark,<br>I read the poster about the essay contest, and I would like to take part. The poster says that essays must be about 800 words long, but it does not say whether they should be typed or handwritten. Could you tell me which is acceptable? Also, I will be on a school trip on the day of the deadline. Would it be possible to hand in my essay a few days early?<br><br>Best regards,<br>Kenta Mori") + E("Question: What does Kenta want to know?") + "<br>① 作文の語数と、締め切りの日付<br>② 作文を手書きで書いてもよいかと、早めに提出できるかどうか<br>③ 作文のテーマと、賞品の内容<br>④ 修学旅行の日程と、作文の書き方のこつ",
  "a": "②",
  "s": "質問・依頼の表現は2つ：" + E("Could you tell me which is acceptable?") + "（タイプと手書きのどちらがよいか）と " + E("Would it be possible to hand in my essay a few days early?") + "（数日早く提出できるか）。①の語数（800語）はポスターに書いてあり、" + E("Kenta") + " はすでに知っている。<br><b>ポイント</b>：メールの問題では、" + E("Could you ～? / Would it be possible ～? / I was wondering if ～") + " などの<b>依頼・質問の表現</b>に印をつける。"},
 {"lv": "B", "tag": "事実と意見", "q": "次の学校新聞の記事を読み、本文中の<b>事実</b>を述べたものとして最も適切なものを選べ。<br>" + E("Our school started a “Meatless Monday” program in April. Since then, the cafeteria has served only vegetable dishes on Mondays. According to a survey of 300 students, 65 percent said they had tried a vegetable they had never eaten before. I think this program is a great way to help students learn about healthy eating, and other schools should try it too.") + "<br>① " + E("The program is a great way to learn about healthy eating.") + "<br>② " + E("Other schools should start the same program.") + "<br>③ " + E("In the survey, more than half of the students said they had tried a new vegetable.") + "<br>④ " + E("Vegetable dishes are more delicious than meat dishes."),
  "a": "③",
  "s": "③は調査結果（300人中65%）の言いかえで、事実。65%は半分（50%）を超えているので " + E("more than half") + " で正しい。①②は " + E("I think ～") + "・" + E("should") + " で示された筆者の<b>意見</b>。④は本文に書かれておらず、内容も意見。<br><b>ポイント</b>：数値の<b>言いかえ</b>（" + E("65 percent → more than half") + "、" + E("200 out of 300 → two-thirds") + "）に慣れておく。"},
 {"lv": "B", "tag": "情報の照合", "q": "観光案内所のツアー一覧と、" + E("Ms. Lee") + " のメモを読み、" + E("Ms. Lee") + " が参加できるツアーを選べ。" + TOUR + E("Ms. Lee") + " のメモ：" + E("“I arrive on Saturday afternoon and have to leave for the airport at 6 p.m. on Sunday. I don't understand Japanese, and I'd like to try some local food.”") + "<br>① A　② B　③ C　④ D",
  "a": "③",
  "s": "条件を1つずつ当てはめて消去する。A：土曜の午前9時開始で、土曜の午後に着く " + E("Ms. Lee") + " は間に合わない。B：日本語のツアー。D：日曜の午後7時開始で、午後6時に空港へ向かう " + E("Ms. Lee") + " は参加できない。C：日曜の午前10時〜午後1時、英語、食べ物の市場 → すべての条件に合う。<br><b>ポイント</b>：複数の条件がある照合問題は、<b>条件ごとに×をつけて消去</b>する。開始時刻だけでなく、所要時間から終了時刻も計算する。"},
 {"lv": "C", "tag": "長文（記事）", "q": "高校生が地域の取り組みについて書いた次の記事を読み、問いに答えよ。" + P("<b>" + T1 + "</b>") + "".join(P(x) for x in L1) +
  "問1　次の (A)〜(D) を起こった順に並べたものを選べ。<br>"
  "　(A) 筆者が祖父とラジオを直しに行った　(B) 町でリペア・カフェが始まった　(C) 筆者がボランティアとして参加した　(D) 筆者が自転車を持っていく<br>"
  "　① B→A→C→D　② A→B→C→D　③ B→C→A→D　④ A→C→B→D<br>"
  "問2　筆者の<b>意見</b>として述べられているものを選べ。<br>"
  "　① 毎回約40人がイベントに来る。<br>"
  "　② 持ちこまれた物の約7割が修理される。<br>"
  "　③ カフェの最大の利点は、ごみの削減ではなく、世代を超えた会話である。<br>"
  "　④ ラジオの故障の原因は、1本の線が外れていたことだった。<br>"
  "問3　本文の内容と一致するものを選べ。<br>"
  "　① 修理は無料で行われる。<br>"
  "　② 持ちこまれた物は、すべて修理できる。<br>"
  "　③ イベントは毎週開かれている。<br>"
  "　④ 筆者は、ラジオの修理に1時間以上かかったことに驚いた。<br>"
  "問4　筆者がこの記事で最も伝えたいことを選べ。<br>"
  "　① リペア・カフェは、ごみを減らすだけでなく、世代を超えて人をつなぐ場として価値がある。<br>"
  "　② 現代の機械は修理できないので、新しいものに買いかえるべきだ。<br>"
  "　③ 若い人のほうが、高齢者よりも機械にくわしい。<br>"
  "　④ ボランティア活動は、月に1回で十分である。",
  "a": "問1 ①　問2 ③　問3 ①　問4 ①",
  "s": f"本文はタイトルを含めて {N1}語。<br>"
  "問1【順序】" + E("Last November") + "（カフェが始まった：B）→ " + E("I first visited the café with my grandfather") + "（A）→ " + E("Since then, I have volunteered ... three times") + "（C）→ " + E("Next month, I am planning to bring my broken bicycle") + "（D：これからの予定）。<br>"
  "問2【事実と意見】③は " + E("I believe the café's biggest benefit is not the reduction of waste. It is the conversations.") + " で、" + E("I believe") + " が意見の目印。①②は主催者の数字（" + E("According to the organizers") + "）、④は実際に起きたことで、いずれも事実。<br>"
  "問3【内容一致】①は " + E("volunteers help them fix the items for free") + " と一致。②は " + E("not everything can be fixed") + "・" + E("roughly 70 percent") + " と矛盾、③は " + E("Once a month") + " と矛盾、④は " + E("Within twenty minutes") + " と矛盾し、筆者が驚いたのは修理が簡単だったこと。<br>"
  "問4【主張】第3段落の " + E("However, I believe ～") + " と第4段落の " + E("Even so, I think every town should have a place like this.") + " が筆者の主張。②は第4段落の譲歩の部分（" + E("Of course, not everything can be fixed.") + "）だけを取り出して、結論をすりかえている。<br>"
  "<b>ポイント</b>：共通テストの記事では、" + E("Of course ～. Even so, ...") + "（もちろん〜。それでも…）のような<b>譲歩→主張</b>の流れが多い。意見問題は " + E("I think / I believe / should") + " を探し、事実問題は数値・出典（" + E("According to ～") + "）を探す。"},
 {"lv": "C", "tag": "複数テキスト", "q": "「宿題に AI ツールを使ってよいか」について、2人の高校生が学校新聞に意見を寄せた。2つの文章を読み、問いに答えよ。"
  "<p><b>" + E("Hana") + " の意見</b></p>" + P(LA) + "<p><b>" + E("Daniel") + " の意見</b></p>" + P(LB) +
  "問1　2人が<b>ともに</b>認めていることを選べ。<br>"
  "　① 生徒は AI について学ぶ必要がある。<br>"
  "　② 宿題に AI ツールを使うことは全面的に禁止すべきだ。<br>"
  "　③ 宿題はもう必要ない。<br>"
  "　④ AI ツールの使用は、生徒の間で不公平を生む。<br>"
  "問2　" + E("Hana") + " が自分の意見の根拠として挙げていることを選べ。<br>"
  "　① 将来、多くの仕事で AI とともに働くことが求められる。<br>"
  "　② 宿題の目的は、正しい答えを出すことではない。<br>"
  "　③ 教師は授業中に AI の使い方を指導できる。<br>"
  "　④ 高価な AI ツールを買えない生徒がいる。<br>"
  "問3　" + E("Daniel") + " が「不公平だ」と考える理由を、日本語で説明せよ。",
  "a": "問1 ①　問2 ①　問3 よりよい（有料の）ツールにお金を払える生徒とそうでない生徒がいるから。",
  "s": "語数は " + E("Hana") + f" の文章が {NA}語、" + E("Daniel") + f" の文章が {NB}語、合わせて {NA + NB}語。<br>"
  "問1　" + E("Hana") + " は " + E("school is the best place to learn how to use it wisely") + "、" + E("Daniel") + " は " + E("I agree that we need to learn about AI") + " と述べており、「AI について学ぶ必要がある」点は共通（①）。ただし、学ぶ場所（宿題か、授業か）で意見が分かれる。②は " + E("Hana") + " の意見と合わず、" + E("Daniel") + " も「全面禁止」とまでは言っていない。③はどちらも述べていない。④は " + E("Daniel") + " だけの意見。<br>"
  "問2　" + E("In the future, most jobs will require us to work with AI") + " が根拠（①）。②④は " + E("Daniel") + " の意見、③は " + E("Daniel") + " の提案（" + E("special lessons at school, where teachers can guide us") + "）。<br>"
  "問3　" + E("because some students can pay for better tools than others") + " が理由。「お金」の要素を落とさないこと。<br>"
  "<b>ポイント</b>：複数テキストの問題は、<b>2人の主張・根拠・譲歩</b>を表に整理しながら読む。「共通点」を問う設問では、一方が譲歩として認めている部分（" + E("I agree that ～, but ...") + "）が答えになることが多い。"},
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
    # 料金計算：正解②の金額が計算結果と一致し、誤答の金額と重ならないこと
    q5 = its[4]["q"]
    assert f'② <span class="en">{TOTAL:,} yen</span>' in q5 and q5.count(f"{TOTAL:,} yen") == 1, TOTAL
    # 図表：合計200人、自転車が最多、公共交通機関は半分未満
    assert 46 + 72 + 38 + 44 == 200 and 38 + 44 < 100
    assert 200 <= N1 <= 350 and 200 <= NA + NB <= 350, (N1, NA, NB)   # 長文の語数
    assert f"{N1}語" in its[-2]["s"] and f"{NA + NB}語" in its[-1]["s"]
    # 長文が段落ごとに欠けずに問題文に入っているか
    assert P("<b>" + T1 + "</b>") + "".join(P(x) for x in L1) in its[-2]["q"]
    assert P(LA) in its[-1]["q"] and P(LB) in its[-1]["q"]
