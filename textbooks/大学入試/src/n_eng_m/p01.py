"""問題集 第1章 文型と動詞の語法。英語は機械検算ができないので、verify() は形式の点検のみ。"""

def E(s):
    return f'<span class="en">{s}</span>'

CH = {1: {
"goal": "動詞の後ろの形（文型・語法）を見て、正しい形を選び、正確に訳せるようにする。",
"items": [
 {"lv": "A", "tag": "文法4択", "q": "（　）に入る最も適切なものを選べ。<br>" + E("The sun (　) in the east.") + "　① raises　② rises　③ lays　④ lies",
  "a": "②", "s": "目的語がないので自動詞 " + E("rise") + "（上がる）。主語が三人称単数・現在の一般的事実なので rises。" + E("raise") + " は「〜を上げる」で目的語が必要。"},
 {"lv": "A", "tag": "文法4択", "q": E("We have to (　) the matter with our teacher.") + "　① discuss about　② discuss　③ talk　④ speak",
  "a": "②", "s": E("discuss") + " は他動詞で前置詞をとらない。talk・speak は自動詞なので about などが必要（talk about the matter）。<br><b>ポイント</b>：「〜について話し合う」という訳につられない。"},
 {"lv": "A", "tag": "文法4択", "q": E("My father didn't let me (　) out after dark.") + "　① go　② to go　③ going　④ went",
  "a": "①", "s": E("let + O + 原形") + "「（許可して）O に〜させる」。"},
 {"lv": "A", "tag": "文法4択", "q": E("This song always makes me (　) happy.") + "　① to feel　② feeling　③ feel　④ felt",
  "a": "③", "s": E("make + O + 原形") + "。me は「感じる」側（能動）なので原形。「この歌を聞くといつも幸せな気分になる」。"},
 {"lv": "B", "tag": "整序", "q": "日本語に合うように並べかえよ。<br>父は私に車を洗わせた。（ wash / had / my father / me / the car ）",
  "a": E("My father had me wash the car."), "s": E("have + O + 原形") + "「O に〜させる・してもらう」。me は「洗う」側（能動）なので原形 wash。"},
 {"lv": "B", "tag": "正誤", "q": "誤りを含む部分を指摘して正せ。<br>" + E("I'm going to have my hair cutting at the new salon tomorrow."),
  "a": E("cutting → cut"), "s": "my hair は「切られる」側（受動）なので " + E("have + O + 過去分詞") + "。cut の過去分詞は cut。"},
 {"lv": "B", "tag": "和訳", "q": "和訳せよ。<br>" + E("The heavy rain prevented us from going out."),
  "a": "大雨のせいで、私たちは外出できなかった。", "s": E("prevent O from doing") + "「O が〜するのを妨げる」。無生物主語は「〜のせいで／〜によって」と原因に訳し、O を主語にして「〜できなかった」とすると自然。同じ型：" + E("keep / stop O from doing") + "。"},
 {"lv": "B", "tag": "空所補充", "q": E("The committee demanded that the plan (　) changed.") + " の空所に1語を補え。",
  "a": E("be"), "s": "要求の動詞 " + E("demand") + " に続く that 節は原形（または should ＋原形）。受動態なので " + E("be changed") + "。"},
 {"lv": "B", "tag": "書きかえ", "q": "ほぼ同じ意味になるように空所に1語を補え。<br>" + E("She cooked us a delicious dinner.") + " ＝ " + E("She cooked a delicious dinner (　) us."),
  "a": E("for"), "s": E("cook") + " は「自分だけでもできる動作を相手のためにする」動詞 → for。give・show・tell などは to。"},
 {"lv": "C", "tag": "和訳", "q": "下線部を和訳せよ。<br>" + E("<u>Living abroad for a year made her realize how little she had known about her own country.</u>"),
  "a": "1年間海外で暮らしたことで、彼女は自分の国についていかに知らなかったかに気づいた。",
  "s": "構造：S＝" + E("Living abroad for a year") + "（動名詞句）、V＝made、O＝her、C＝" + E("realize ～") + "（原形）。" + E("how little she had known") + " は「どれほど少ししか知らなかったか」＝「いかに知らなかったか」。had known は「気づいた時点」より前からの状態なので過去完了。<br><b>ポイント</b>：無生物主語＋make O do は「S によって O は〜する」と訳すと自然。"},
 {"lv": "C", "tag": "英作文", "q": "次の日本語を、「その知らせ」を主語にして英語に直せ。<br>その知らせを聞いて、私たちは言葉を失った。",
  "a": E("The news left us speechless.") + "（" + E("The news made us speechless.") + " も可）",
  "s": "「言葉を失った」＝ speechless（言葉が出ない状態）。無生物主語 ＋ SVOC（" + E("leave / make O C") + "）で「その知らせが私たちを言葉の出ない状態にした」と組み立てる。" + E("When we heard the news, we were at a loss for words.") + " のように人を主語にした文も正しいが、指示に従うこと。"},
]}}

def verify():
    for it in CH[1]["items"]:
        assert it["lv"] in "ABC" and it["q"] and it["a"] and it["s"]
    lv = [it["lv"] for it in CH[1]["items"]]
    assert lv.count("A") >= 4 and lv.count("B") >= 4 and lv.count("C") >= 2
