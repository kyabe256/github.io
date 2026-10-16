"""問題集 第22章 リスニング（音声の代わりにスクリプトを示す）。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・タグの対応・選択肢の番号・スクリプトの有無）のみ。"""
import re

def E(s):
    return f'<span class="en">{s}</span>'

def SC(s):
    """読まれる英文（スクリプト）を枠で囲む"""
    return f'<table class="l w"><tr><td><span class="en">{s}</span></td></tr></table>'

def wc(s):
    return len([w for w in re.sub(r"<[^>]+>", " ", s).split() if re.search(r"[A-Za-z0-9]", w)])

NO = 22

L1 = ("Today I'd like to talk about how cities are trying to stay cool as summers get hotter. "
      "Cities can be several degrees warmer than the areas around them, because concrete and asphalt absorb heat during the day and release it at night. "
      "There are three main approaches to this problem. The first is to plant more trees, which provide shade and cool the air. "
      "The second is to paint roofs white or other light colors, so that they reflect sunlight instead of absorbing it. "
      "The third is to create more open water, such as fountains and small streams. "
      "All of these help, but in my opinion, trees are the most effective, because they also improve air quality and make streets more pleasant to walk along. "
      "Next week, we'll look at some cities that have used these methods successfully.")
N1 = wc(L1)

CH = {NO: {
"goal": "音の変化（連結・脱落・同化・弱形・ラ行化）を知り、数字・言いかえ・逆接のあとなど聞き取りの要点をつかめるようにする。※この章では音声の代わりにスクリプト（読まれる英文）を示す。必ず声に出して読み、音の変化を自分の口で確かめよう。",
"items": [
 {"lv": "A", "tag": "音の変化4択", "q": "次の英文を自然な速さで読むとき、下線部の発音に最も近いものを選べ。<br>" + E("Could you <u>pick it up</u> for me?") + "<br>① ピック・イット・アップ　② ピキラップ　③ ピクト・アプ　④ ピッカップ",
  "a": "②",
  "s": "子音で終わる語と母音で始まる語は<b>連結</b>する：" + E("pick it") + "→「ピキッ」、" + E("it up") + "→「イタップ」。さらにアメリカ英語では、母音にはさまれた " + E("t") + " が軽い「ラ行」のような音になり（<b>ラ行化</b>）、全体が「ピキラップ」のように聞こえる。④は " + E("it") + " が抜けた " + E("pick up") + " の音。<br><b>ポイント</b>：" + E("check it out") + "（チェキラウ（ト））、" + E("put it on") + "（プリロン）、" + E("a lot of") + "（アララヴ）も同じ仕組み。"},
 {"lv": "A", "tag": "音の変化4択", "q": "次の英文の下線部を自然な速さで読むとき、ほとんど聞こえなくなりやすい音を選べ。<br>" + E("He <u>went to</u> the station by bus.") + "<br>① " + E("went") + " の最後の " + E("t") + "　② " + E("to") + " の " + E("t") + "　③ " + E("went") + " の " + E("w") + "　④ " + E("to") + " の母音",
  "a": "①",
  "s": "同じ（または似た）子音が続くと、前の子音はほとんど発音されず、1回分のように聞こえる（<b>脱落</b>）。" + E("went to") + " は「ウェントゥ」。同様に " + E("next time") + "（ネクスタイム）、" + E("good day") + "（グッデイ）、" + E("hot tea") + "（ホッティー）。<br><b>ポイント</b>：聞こえなかった音は、文法（過去形の " + E("went") + "）と文脈から補って理解する。"},
 {"lv": "A", "tag": "音の変化4択", "q": "次の英文の下線部の発音に最も近いものを選べ。<br>" + E("<u>Could you</u> open the window?") + "<br>① クッド・ユー　② クッジュー　③ クッド・ヨー　④ コールド・ユー",
  "a": "②",
  "s": E("Could") + " の最後の " + E("d") + " と " + E("you") + " の最初の音が混ざり、「ジュ」の音になる（<b>同化</b>）。同様に " + E("Did you") + "（ディジュ）、" + E("Would you") + "（ウッジュ）。" + E("t") + " ＋ " + E("you") + " は「チュ」になる：" + E("meet you") + "（ミーチュー）、" + E("Don't you") + "（ドンチュー）。<br><b>ポイント</b>：" + E("Could you ～? / Would you ～?") + " で始まる依頼の表現は、会話の問題で頻出。"},
 {"lv": "A", "tag": "音の変化4択", "q": E("I can swim.") + " と " + E("I can't swim.") + " を聞き分ける方法の説明として、最も適切なものを選べ。<br>① 肯定の " + E("can") + " はふつう弱く短く「クン」のように読まれ、後ろの動詞 " + E("swim") + " が強く聞こえる。<br>② 肯定の " + E("can") + " は強く長く読まれ、否定の " + E("can't") + " は弱く短く読まれる。<br>③ " + E("can't") + " の " + E("t") + " は必ずはっきり発音されるので、" + E("t") + " の有無だけで判断できる。<br>④ 肯定と否定はまったく同じ発音なので、文脈でしか判断できない。",
  "a": "①",
  "s": "肯定文の " + E("can") + " は弱形（あいまいな母音の「クン」）で読まれ、強勢は動詞 " + E("swim") + " に置かれる。否定の " + E("can't") + " は強く「キャン（ト）」と読まれるが、語末の " + E("t") + " はほとんど聞こえないことが多い。そのため、" + E("t") + " の有無より「" + E("can") + " の部分が強く長いかどうか」で判断する。②は逆、③は誤り、④は強弱で区別できるので言いすぎ。<br><b>ポイント</b>：助動詞・前置詞・代名詞などの機能語はふつう弱く読まれる（<b>弱形</b>）。機能語が強く聞こえたら、否定や対比の意図がある。"},
 {"lv": "B", "tag": "対話", "q": "次の対話を聞き、質問の答えとして最も適切なものを選べ。（スクリプト）" + SC("W: The concert starts at seven, doesn't it?<br>M: It was supposed to, but it's been moved to seven thirty because of the rain.<br>W: Oh, then we have time for dinner first.") + E("Question: What time will the concert start?") + "　① 7:00　② 7:13　③ 7:30　④ 8:30",
  "a": "③",
  "s": "最初に出た7時は、" + E("but") + " のあとで7時30分に<b>変更</b>されている。②はまぎらわしい数字のひっかけ：" + E("thirty") + " は第1音節に強勢（サーティ）、" + E("thirteen") + " は第2音節に強勢（サーティーン）で、語末の「ン」の有無も手がかりになる。音の変化：" + E("It was supposed to") + "（イッワズサポウストゥ）、" + E("it's been moved") + "（イッツビンムーヴド）。<br><b>ポイント</b>：対話では、最初に出た情報が後で変更されることが多い。" + E("but / actually / instead") + " のあとを聞き逃さない。"},
 {"lv": "B", "tag": "対話", "q": "次の対話を聞き、質問の答えとして最も適切なものを選べ。（スクリプト）" + SC("M: I'd love to join you for lunch, but I've got a report due at two.<br>W: That's too bad. Maybe next time.") + E("Question: Why can't the man have lunch with the woman?") + "<br>① " + E("He has already eaten.") + "<br>② " + E("He has to finish some work by two o'clock.") + "<br>③ " + E("He doesn't like the restaurant.") + "<br>④ " + E("He has a meeting at two."),
  "a": "②",
  "s": E("a report due at two") + "（2時締め切りのレポート）が、" + E("finish some work by two o'clock") + " に<b>言いかえ</b>られている。④は " + E("two") + " という同じ語を使ったひっかけ。音の変化：" + E("I've got a") + " は「アイヴガラ」（" + E("got a") + " の連結とラ行化）、" + E("I'd love to") + " は「アイドラヴトゥ」。<br><b>ポイント</b>：正解は本文の<b>言いかえ</b>、ひっかけは本文と<b>同じ語</b>を使った選択肢であることが多い。"},
 {"lv": "B", "tag": "対話", "q": "次の対話を聞き、質問の答えとして最も適切なものを選べ。（スクリプト）" + SC("W: Would you like to go hiking this weekend?<br>M: I wish I could. My sister is moving into a new apartment, and I promised to help her.") + E("Question: What will the man probably do this weekend?") + "<br>① " + E("Go hiking with the woman.") + "<br>② " + E("Help his sister move.") + "<br>③ " + E("Look for a new apartment.") + "<br>④ " + E("Visit his sister's old apartment."),
  "a": "②",
  "s": E("I wish I could.") + "（できたらいいのだけど＝実際はできない）は、" + E("Yes / No") + " を言わずに断る表現（仮定法）。続く理由から、妹の引っ越しを手伝うと推測できる。③は " + E("apartment") + " という同じ語を使ったひっかけ。音の変化：" + E("Would you") + "（ウッジュ）、" + E("help her") + "（ヘルパー：" + E("her") + " の " + E("h") + " が弱まって連結）。<br><b>ポイント</b>：直接答えない応答（" + E("I wish I could. / I'm afraid ～. / I'd love to, but ～.") + "）は断りの合図。"},
 {"lv": "B", "tag": "ディクテーション", "q": "次の英文は、自然な速さでは「　」内のように聞こえる。空所に入る語を書け。<br>(1)「アイムガナ コーリュー レイラー」　" + E("I'm (　) (　) call you later.") + "<br>(2)「ユーヴガラ スィーディス ムーヴィー」　" + E("You've (　) (　) see this movie.") + "<br>(3)「ワッチャ ドゥーイン」　" + E("What (　) you doing?"),
  "a": "(1) " + E("going to") + "　(2) " + E("got to") + "　(3) " + E("are"),
  "s": "(1) " + E("going to") + " は話し言葉で " + E("gonna") + "（ガナ／ゴナ）。" + E("call you") + " は連結、" + E("later") + " は " + E("t") + " のラ行化で「レイラー」。<br>(2) " + E("have got to") + "（〜しなければならない、ここでは「ぜひ〜すべきだ」）の " + E("got to") + " は " + E("gotta") + "（ガラ／ガタ）。" + E("You've") + " の " + E("'ve") + " は弱くほとんど聞こえない。<br>(3) " + E("What are you") + " は、" + E("are") + " が弱く短くなってほとんど消え、" + E("t") + " と " + E("you") + " が同化して「ワッチャ」。" + E("doing") + " の語末の音も弱まり「ドゥーイン」と聞こえる。<br><b>ポイント</b>：" + E("gonna, wanna, gotta") + " は書き言葉では使わないが、聞き取りでは<b>元の形に戻せる</b>ことが大切。"},
 {"lv": "B", "tag": "図表と対話", "q": "次の対話を聞き、女性が買う T シャツを表から選べ。（スクリプト）" + SC("W: I'm looking for a T-shirt for my brother. He usually wears a medium.<br>M: We have medium ones in blue and red.<br>W: He already has a lot of blue shirts, so I'll take the other color.") +
  "<table class=\"l w\"><tr><th></th><th>サイズ</th><th>色</th><th>値段</th></tr><tr><td>①</td><td>" + E("Small") + "</td><td>" + E("blue") + "</td><td>1,200円</td></tr><tr><td>②</td><td>" + E("Medium") + "</td><td>" + E("blue") + "</td><td>1,500円</td></tr><tr><td>③</td><td>" + E("Medium") + "</td><td>" + E("red") + "</td><td>1,500円</td></tr><tr><td>④</td><td>" + E("Large") + "</td><td>" + E("red") + "</td><td>1,800円</td></tr></table>",
  "a": "③",
  "s": "条件を1つずつ絞る：" + E("He usually wears a medium.") + " → ②③。" + E("He already has a lot of blue shirts, so I'll take the other color.") + " → 青ではないほう（" + E("the other") + "＝2つのうちのもう一方）＝赤 → ③。値段は判断に使わない情報。音の変化：" + E("a lot of") + "（アララヴ）、" + E("I'll take the other") + "（アイルテイクズィアザー）。<br><b>ポイント</b>：図表つきの問題では、<b>消去の根拠</b>（ここでは「青はたくさん持っている」）を聞き逃さない。音声が流れる前に表を見て、何で区別されるか（サイズ・色・値段）を確認しておく。"},
 {"lv": "C", "tag": "講義", "q": "次の講義を聞き、問いに答えよ。（スクリプト）" + SC(L1) +
  "問1　講義の主題として最も適切なものを選べ。<br>　① 暑さが増す中で、都市が涼しさを保つための取り組み　② コンクリートとアスファルトの作り方　③ 世界の噴水の歴史　④ 都市が周辺の地域より暑くなる仕組み<br>"
  "問2　2つ目の方法として述べられているものを選べ。<br>　① 屋根を白など明るい色に塗り、日光を反射させる　② 噴水や小川を作る　③ 木を植える　④ アスファルトの道路を増やす<br>"
  "問3　話し手が最も効果的だと考える方法と、その理由として最も適切なものを選べ。<br>　① 木を植えること：空気の質もよくし、通りを歩きやすくするから<br>　② 屋根を塗ること：費用が最も安いから<br>　③ 水辺を作ること：子どもが遊べるから<br>　④ 木を植えること：日陰を作る唯一の方法だから",
  "a": "問1 ①　問2 ①　問3 ①",
  "s": f"スクリプトは {N1}語。講義は「話の道しるべ（サインポスト）」に注目すると整理しやすい：" + E("Today I'd like to talk about ～") + "（主題）→ " + E("There are three main approaches") + "（数の予告）→ " + E("The first / The second / The third") + " → " + E("in my opinion") + "（話し手の意見）→ " + E("Next week") + "（次回の予告）。<br>"
  "問1　冒頭の " + E("how cities are trying to stay cool as summers get hotter") + "。④の「都市が暑くなる仕組み」は、導入で背景として触れているだけ。<br>"
  "問2　" + E("The second is to paint roofs white or other light colors, so that they reflect sunlight") + "。②は3つ目、③は1つ目。<br>"
  "問3　" + E("in my opinion, trees are the most effective, because they also improve air quality and make streets more pleasant to walk along") + "。④の「唯一の方法」は述べられていない。<br>"
  "音の変化：" + E("I'd like to talk about") + "（アイライクトゥ トーカバウ（ト））、" + E("All of these") + "（オーラヴズィーズ）、" + E("look at") + "（ルッカッ（ト））。<br>"
  "<b>ポイント</b>：長い講義では全部を覚えようとせず、<b>数の予告と順序を表す語</b>でメモの枠を作り、" + E("in my opinion / the most important") + " のあとの話し手の主張を確実に聞き取る。"},
 {"lv": "C", "tag": "音の変化", "q": "次の「　」は、自然な速さの英語の聞こえ方を示したものである。もとの英文を書き、どのような音の変化が起きているかを説明せよ。<br>(1)「ワラユ ゴナ ドゥ ウィズィッ」<br>(2)「アイ シュダ トールジュー」<br>(3)「ドンチュー ワナ カム ウィザス」",
  "a": "(1) " + E("What are you going to do with it?") + "　(2) " + E("I should have told you.") + "　(3) " + E("Don't you want to come with us?"),
  "s": "(1) " + E("What are") + "：" + E("t") + " が母音にはさまれてラ行化し、弱形の " + E("are") + " とつながって「ワラ」。" + E("going to") + " → " + E("gonna") + "。" + E("with it") + "：連結して「ウィズィッ」、語末の " + E("t") + " はほとんど聞こえない。<br>"
  "(2) " + E("should have") + "：" + E("have") + " が弱形になり " + E("shoulda") + "（シュダ）。" + E("told you") + "：" + E("d") + " ＋ " + E("you") + " の同化で「トールジュー」。「〜すべきだったのに（言わなかった）」と過去の後悔を表す " + E("should have ＋ 過去分詞") + " だと気づけるかが聞き取りのカギ。<br>"
  "(3) " + E("Don't you") + "：" + E("t") + " ＋ " + E("you") + " の同化で「ドンチュー」。" + E("want to") + " → " + E("wanna") + "（ワナ）。" + E("with us") + "：連結して「ウィザス」。否定疑問文で「一緒に来たくないの？（来ればいいのに）」と誘っている。<br>"
  "<b>ポイント</b>：音の変化が起きるのは、主に " + E("are, have, to, you, it") + " などの<b>機能語</b>。聞こえ方から<b>文法的に正しい文を復元する</b>練習は、リスニング力と英作文の正確さの両方を伸ばす。"},
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
        if it["tag"] in ("対話", "図表と対話", "講義"):   # 聞き取り問題はスクリプトを示す
            assert "（スクリプト）" in it["q"] and "<table" in it["q"], i
    assert 120 <= N1 <= 200, N1
    assert f"{N1}語" in its[-2]["s"]
    assert SC(L1) in its[-2]["q"]               # スクリプトが欠けずに入っているか
