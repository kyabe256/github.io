"""問題集 第18章 設問タイプ別の解き方。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号・長文の語数・記述の字数）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

def P(s):
    return f'<p class="en">{s}</p>'

def wc(s):
    """英文の語数（タグを除き、空白で区切った語のうち英字・数字を含むもの。ハイフンでつないだ語は1語）"""
    return len([w for w in re.sub(r"<[^>]+>", " ", s).split() if re.search(r"[A-Za-z0-9]", w)])

NO = 18

# ---- C1 の長文 ----
L1 = [
 "For most of human history, people could look up on a clear night and see thousands of stars. Today, however, a large part of the world's population lives in places where the night sky is never truly dark. Streetlights, advertising signs, and office buildings send so much light into the sky that only the brightest stars remain visible. Scientists call this problem light pollution.",
 "Light pollution is not only a problem for people who enjoy looking at the stars. Many animals depend on natural patterns of light and darkness. Baby sea turtles, for example, find their way to the ocean after hatching by moving toward the brightest horizon, which is usually the moonlit sea. When bright lights shine from hotels and roads along the beach, the young turtles may crawl in the wrong direction. ( A ), birds that migrate at night can become confused by city lights and crash into buildings.",
 "Humans are affected as well. Our bodies have an internal clock that uses darkness as a signal to prepare for sleep. Exposure to bright light late at night can disturb <u>this clock</u>, making it harder to fall asleep.",
 "Unlike many other forms of pollution, however, light pollution can be reduced quickly and cheaply. Simple steps such as covering streetlights so that they shine only downward, turning off unnecessary lights, and using warmer, dimmer bulbs can make a significant difference. Some towns have already taken such steps and now attract visitors who come specifically to enjoy the starry sky. If more communities choose to act, the stars that our grandparents saw may once again be visible to our grandchildren.",
]
N1 = wc(" ".join(L1))

# ---- C2 の英文と記述の模範解答 ----
L2 = ("Why do people often love a simple bookshelf they put together themselves more than a better one bought in a store? "
      "Psychologists have found that people tend to place a higher value on things they have helped to create. "
      "When we spend time and energy building something, we feel a sense of ownership and pride that a finished product cannot give us. "
      "In a way, <u>the effort itself becomes part of the value</u>. "
      "This may explain why meal kits that require customers to do some of the cooking are so popular, and why children are more willing to eat vegetables they have grown in a school garden. "
      "There is a limit, though: if a task is so difficult that we fail to complete it, the effect disappears.")
N2 = wc(L2)
ANS2 = "自分で時間や労力をかけて作ったものには所有感や誇りが生まれるため、その努力の分だけ、物の価値が高く感じられるということ。"

CH = {NO: {
"goal": "内容一致・英問英答・語句の意味・タイトル選択・空所補充・理由説明・指示語・記述説明など、設問の型ごとに「本文のどこを見て、どう判断するか」の手順を身につける。",
"items": [
 {"lv": "A", "tag": "内容一致", "q": "次の英文を読み、内容と一致するものを選べ。<br>" + E("Emma started learning the piano at the age of forty. Because she had a busy job, she could practice for only ten minutes a day at first. Two years later, she performed at a small concert held at her local library.") + "<br>① " + E("Emma began playing the piano when she was a child.") + "<br>② " + E("At first, Emma practiced for a short time every day.") + "<br>③ " + E("Emma quit her job so that she could practice more.") + "<br>④ " + E("Emma's concert took place at a school."),
  "a": "②",
  "s": "②は " + E("she could practice for only ten minutes a day at first") + " の言いかえ（" + E("only ten minutes") + " → " + E("a short time") + "）。①は " + E("at the age of forty") + " と矛盾、③は本文に書かれていない、④は " + E("library") + " と矛盾。<br><b>ポイント</b>：正解の選択肢は本文の<b>言いかえ</b>。不正解の選択肢は、本文の語句を使いながら一部を変えたものが多い。"},
 {"lv": "A", "tag": "英問英答", "q": "次の英文を読み、質問の答えとして最も適切なものを選べ。<br>" + E("The bakery on Main Street usually stays open until seven in the evening. Yesterday, however, it closed at three because its oven broke down and the owner had to wait for a repair worker.") + "<br>" + E("Question: Why did the bakery close early yesterday?") + "<br>① " + E("Because it had sold all its bread.") + "<br>② " + E("Because its oven stopped working.") + "<br>③ " + E("Because the owner felt sick.") + "<br>④ " + E("Because it was a national holiday."),
  "a": "②",
  "s": E("broke down") + "（故障した）＝ " + E("stopped working") + "。設問の " + E("Why ... early") + " に対応するのは、本文の " + E("because") + " 以下。<br><b>ポイント</b>：英問英答は<b>設問を先に読み</b>、疑問詞（" + E("Why, When, Where") + " など）に対応する部分を本文で探す。"},
 {"lv": "A", "tag": "語句の意味", "q": "下線部の意味に最も近いものを選べ。<br>" + E("After the long meeting, everyone was <u>worn out</u>, so we decided to continue the discussion the next day.") + "<br>① " + E("very tired") + "　② " + E("very angry") + "　③ " + E("well prepared") + "　④ " + E("deeply moved"),
  "a": "①",
  "s": E("wear out") + " は「すり減らす・疲れ果てさせる」で、" + E("be worn out") + " は「疲れ果てている」。「長い会議のあと」→「疲れ果てていた」→「だから話し合いは翌日続けることにした」という因果関係にも合う。<br><b>ポイント</b>：語句の言いかえ問題は、選択肢を下線部に<b>当てはめて</b>、前後の因果関係が成り立つかを確かめる。"},
 {"lv": "A", "tag": "タイトル", "q": "次の英文のタイトルとして最も適切なものを選べ。<br>" + E("When you cut an onion, it releases a chemical into the air. When this chemical reaches your eyes, it causes a slight stinging feeling, and your eyes produce tears to wash it away. Chilling the onion in the refrigerator before cutting it can reduce this effect.") + "<br>① " + E("Why Onions Make Us Cry") + "<br>② " + E("How to Grow Onions at Home") + "<br>③ " + E("The Long History of Onions") + "<br>④ " + E("Onions Are Good for Your Health"),
  "a": "①",
  "s": "文章全体が「玉ねぎを切ると涙が出る仕組みと、その防ぎ方」について述べている。②③④の内容は本文で触れられていない。<br><b>ポイント</b>：タイトルは本文<b>全体</b>をカバーし、かつ広すぎない（「玉ねぎについて」だけでは広すぎる）ものを選ぶ。"},
 {"lv": "B", "tag": "空所補充", "q": "空所 (1)(2) に入る最も適切なものを、それぞれ選べ。<br>" + E("Many people assume that eating late at night always leads to weight gain. ( 1 ), many nutrition experts say that what matters most is not the time of day but the total amount of food we eat. ( 2 ), late-night snacking can still be a problem, because people often choose foods that are high in sugar and fat when they are tired.") + "<br>(1)　① " + E("In fact") + "　② " + E("For example") + "　③ " + E("As a result") + "　④ " + E("Similarly") + "<br>(2)　① " + E("Therefore") + "　② " + E("That said") + "　③ " + E("In other words") + "　④ " + E("For instance"),
  "a": "(1) ①　(2) ②",
  "s": "(1)「夜遅く食べると必ず太ると思い込んでいる人が多い」→「実は、大切なのは時間帯ではなく量だ」。一般の思い込みを訂正する " + E("In fact") + "（実際は）。<br>(2) 前の文で「時間帯は重要ではない」と述べたあと、「それでも夜食は問題になりうる」と<b>部分的に修正</b>している → " + E("That said") + "（そうは言っても）。① " + E("Therefore") + " は前の文から当然導かれる結論を述べる語なので合わない。<br><b>ポイント</b>：空所補充は、空所の<b>前後の2文の関係</b>（対立・例示・結果・言いかえ・譲歩）を先に決め、それに合うつなぎ語を選ぶ。"},
 {"lv": "B", "tag": "理由説明", "q": "次の英文を読み、下線部のようになった理由を日本語で説明せよ。<br>" + E("When Ken moved to a small town in Canada, he was worried that he would feel lonely. On his first morning, however, a neighbor knocked on his door with a homemade pie and an invitation to a barbecue. <u>Ken's worries disappeared almost immediately.</u>"),
  "a": "引っ越した最初の朝に、隣人が手作りのパイを持って訪ねてきて、バーベキューに誘ってくれたから。",
  "s": "下線部「ケンの心配はほとんどすぐに消えた」の「心配」の中身は、第1文の「孤独を感じるのではないか」。それが消えた理由は、" + E("however") + " のあとの出来事（隣人の訪問と招待）。<br><b>ポイント</b>：理由説明は、下線部の<b>直前・直後</b>と、逆接（" + E("however, but") + "）のあとを探す。答えは「〜から。」の形で終える。"},
 {"lv": "B", "tag": "内容一致", "q": "次の英文の内容と<b>一致しないもの</b>を選べ。<br>" + E("The city library introduced a new service last year that allows people to borrow musical instruments, such as guitars and violins, for up to two weeks. The service is free for residents, but users must attend a short training session before borrowing an instrument for the first time. So far, more than 500 people have used the service, and the library plans to add drums and keyboards next spring.") + "<br>① 楽器は最長2週間借りられる。<br>② 市の住民は無料で利用できる。<br>③ 楽器を借りるたびに講習を受けなければならない。<br>④ 来年の春に、貸し出す楽器の種類が増える予定だ。",
  "a": "③",
  "s": "③は本文の " + E("before borrowing an instrument for the first time") + "（初めて借りる前に）と食い違う。「借りるたびに」は言いすぎ。①は " + E("for up to two weeks") + "、②は " + E("free for residents") + "、④は " + E("plans to add drums and keyboards next spring") + " と一致する。<br><b>ポイント</b>：「〜たびに」「すべて」「〜だけ」（" + E("every time, all, only") + "）のような<b>範囲や頻度を広げる・狭める語</b>が選択肢にあれば、本文と細かく照合する。"},
 {"lv": "B", "tag": "指示語・和訳", "q": "次の英文を読み、問いに答えよ。<br>" + E("Some scientists are trying to bring back animals that have died out, such as the woolly mammoth. <u>They</u> believe that such animals could help restore ecosystems that have been lost. Others, however, argue that the money would be better spent protecting species that are still alive.") + "<br>問1　下線部 " + E("They") + " が指すものを、本文中の英語で答えよ。<br>問2　最後の文を和訳せよ。",
  "a": "問1 " + E("Some scientists") + "　問2 しかし、そのお金は今も生きている種を守るために使うほうがよいと主張する人々もいる。",
  "s": "問1　直前の複数名詞は " + E("Some scientists") + " と " + E("animals") + "。" + E("believe") + "（信じている）の主語になれるのは人なので、" + E("Some scientists") + "。<br>問2　" + E("Others") + " は " + E("Some scientists") + " と対比されて「別の人々」。" + E("the money would be better spent doing") + " は「そのお金は〜することに使うほうがよいだろう」（" + E("spend money doing") + "「〜するのにお金を使う」の受動態）。<br><b>ポイント</b>：代名詞の指す語は、<b>数</b>（単数・複数）と、<b>述語動詞との意味の相性</b>で決める。"},
 {"lv": "B", "tag": "英問英答", "q": "次の英文を読み、質問に英語で答えよ。<br>" + E("Maria had planned to spend her vacation at the beach, but a week before her trip, she broke her leg while playing soccer. Instead of canceling her vacation, she decided to stay at home and finally read the stack of novels she had been collecting for years.") + "<br>" + E("Question: What did Maria do during her vacation?"),
  "a": E("She stayed at home and read the novels she had been collecting for years."),
  "s": "設問は「休暇中に何をしたか」。該当するのは " + E("she decided to stay at home and finally read ...") + "。そのまま写すと「〜することに決めた」としか答えていないので、" + E("stayed / read") + " と過去形の動詞にして答える（" + E("read") + " の過去形はつづりが同じで、発音は「レッド」）。" + E("She broke her leg.") + " は休暇の前の出来事なので答えにならない。<br><b>ポイント</b>：英問英答の記述は、本文の該当部分を<b>設問の主語・時制に合わせて</b>書きかえる。代名詞（" + E("She") + "）で始めるとよい。"},
 {"lv": "C", "tag": "長文", "q": "次の英文を読み、問いに答えよ。" + "".join(P(x) for x in L1) +
  "問1　空所 ( A ) に入る最も適切なものを選べ。　① " + E("Similarly") + "　② " + E("However") + "　③ " + E("Otherwise") + "　④ " + E("In contrast") + "<br>"
  "問2　下線部 " + E("this clock") + " が指すものを、日本語で具体的に答えよ。<br>"
  "問3　第2段落で、子ガメが誤った方向に進んでしまうのはなぜか。日本語で説明せよ。<br>"
  "問4　本文の内容と一致するものを選べ。<br>"
  "　① 光害は、星を眺めるのが好きな人だけの問題である。<br>"
  "　② 光害は、ほかの多くの汚染と比べて、早く安く減らすことができる。<br>"
  "　③ 明るい街灯を増やせば、夜に渡る鳥は道に迷わなくなる。<br>"
  "　④ 光害の対策をとった町は、観光客が減ってしまった。<br>"
  "問5　本文のタイトルとして最も適切なものを選べ。<br>"
  "　① " + E("Why the Stars Are Disappearing and How We Can Bring Them Back") + "<br>"
  "　② " + E("The Life Cycle of Sea Turtles") + "<br>"
  "　③ " + E("Ten Tips for Sleeping Better") + "<br>"
  "　④ " + E("The History of Streetlights"),
  "a": "問1 ①　問2 暗さを眠る準備の合図として使う、体内時計。　問3 子ガメはふ化後、最も明るい水平線（ふつうは月明かりの海）に向かって進むが、浜辺沿いのホテルや道路の明かりが明るいと、そちらに向かってしまうから。　問4 ②　問5 ①",
  "s": f"本文は {N1}語。段落の要点：第1段落＝光害とは何か／第2段落＝動物への影響（ウミガメ・渡り鳥）／第3段落＝人間への影響（睡眠）／第4段落＝対策は早く安くできる、という希望。<br>"
  "問1【空所補充】直前は「子ガメが明かりで方向を誤る」、直後は「渡り鳥が明かりで混乱する」。同じ種類の例を並べているので " + E("Similarly") + "（同様に）。<br>"
  "問2【指示語】" + E("this ＋ 名詞") + " は直前の " + E("an internal clock that uses darkness as a signal to prepare for sleep") + " を受ける。<br>"
  "問3【理由説明】" + E("find their way to the ocean ... by moving toward the brightest horizon, which is usually the moonlit sea") + " と " + E("When bright lights shine from hotels and roads along the beach") + " の2点を組み合わせる。「明かりがあるから」だけでは、なぜ方向を誤るのかの説明として不十分。<br>"
  "問4【内容一致】②は " + E("Unlike many other forms of pollution, however, light pollution can be reduced quickly and cheaply.") + " と一致。①は " + E("not only a problem for people who enjoy looking at the stars") + " と矛盾、③は本文の逆（街の明かりで鳥が混乱する）、④は " + E("now attract visitors") + " と矛盾。<br>"
  "問5【タイトル】①は「星が見えなくなっている理由（光害とその影響）」と「取り戻す方法（対策）」の両方を含む。②③は本文の一部の話題にすぎず、④は本文で扱っていない。<br>"
  "<b>ポイント</b>：設問ごとに「見る場所」が違う。空所補充は前後の文、指示語は直前、理由説明は因果を表す語の前後、内容一致は選択肢のキーワードがある段落、タイトルは全体の流れ。設問を先に見て、どこを読めばよいかの見当をつけておく。"},
 {"lv": "C", "tag": "記述説明", "q": "次の英文を読み、下線部の内容を、本文に即して60字以内の日本語で説明せよ。" + P(L2),
  "a": ANS2 + f"（{len(ANS2)}字）",
  "s": f"本文は {N2}語。下線部「ある意味で、努力そのものが価値の一部になる」の直前に理由が書かれている：" + E("When we spend time and energy building something, we feel a sense of ownership and pride that a finished product cannot give us.") + "（何かを作るのに時間とエネルギーを使うと、完成品からは得られない所有感と誇りを感じる）。<br>"
  "採点のポイント：① 自分で時間・労力をかけて作ること　② 所有感や誇りが生まれること　③ その結果、物の価値を高く感じること。3つの要素がそろって満点。本棚・料理キット・家庭菜園などの具体例を書き並べても、説明にはならない。<br>"
  "<b>ポイント</b>：「内容を説明せよ」は、比喩的・抽象的な下線部を、本文の具体的な言葉で<b>言いかえる</b>問題。答えは「〜ということ。」で終える。"},
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
    assert len(ANS2) <= 60, len(ANS2)           # 記述の字数制限
    # 長文が段落ごとに欠けずに問題文に入っているか
    assert "".join(P(x) for x in L1) in its[-2]["q"] and P(L2) in its[-1]["q"]
