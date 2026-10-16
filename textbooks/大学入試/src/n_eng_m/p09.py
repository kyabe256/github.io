"""問題集 第9章 比較。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 9

def E(s):
    return f'<span class="en">{s}</span>'

def T(s):
    return re.sub(r"\{([^{}]+)\}", lambda m: E(m.group(1)), s)

def Q4(stem, opts, lead=""):
    assert len(opts) == 4
    return lead + "{" + stem + "}<br>" + "　".join(f"{n} {{{o}}}" for n, o in zip("①②③④", opts))

LEAD = "（　）に入る最も適切なものを、①〜④から1つ選べ。<br>"
SEIGO = "下線部①〜④のうち、誤りを含むものを1つ選び、正しく直せ。<br>"

ITEMS = [
 {"lv": "A", "tag": "文法4択",
  "q": Q4("This bag is (　) more expensive than that one.", ["very", "much", "more", "so"], LEAD),
  "a": "②",
  "s": "比較級を強めて「ずっと〜」とするのは {much, far, even, still, a lot} など。"
       "①{very} は原級を強める語で、比較級には使えない（{very expensive} は可）。③{more more} は不可。④{so} も比較級の前には置かない。"
       "<br><b>ポイント</b>：比較級の強調は {much / far / even / still / a lot}、最上級の強調は {by far / much / the very}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("No other mountain in Japan is (　) than Mt. Fuji.", ["high", "higher", "highest", "the highest"]),
  "a": "②",
  "s": "{No other ＋ 単数名詞 ＋ is 比較級 ＋ than 〜}「〜ほど…なものはほかにない」は、最上級と同じ意味（{Mt. Fuji is the highest mountain in Japan.}）。{than} があるので比較級。"
       "①原級なら {as high as Mt. Fuji} の形が必要。③④最上級は {than} と使えない。"
       "<br><b>ポイント</b>：最上級の書きかえ ― {No other 〜 is 比較級 than A} / {No other 〜 is as 原級 as A} / {A is 比較級 than any other 〜}（単数名詞）。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("The (　) you practice, the better you will become.", ["much", "more", "most", "many"]),
  "a": "②",
  "s": "{The ＋比較級 〜, the ＋比較級 …}「〜すればするほど、ますます…」。{you practice more}（もっと練習する）の比較級 {more} を、{the} とともに節の先頭に出した形。"
       "①{much}・④{many} は原級、③{most} は最上級なので、{the better} と組み合わせられない。"
       "<br><b>ポイント</b>：〈{the} ＋比較級〉の後は語順に注意。名詞を伴うときは {The more books you read, 〜} のように比較級と名詞をまとめて前に出す。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("This room is three times (　) that one.", ["as large as", "larger as", "as larger as", "as large than"]),
  "a": "①",
  "s": "倍数表現は〈{X times as ＋ 原級 ＋ as} 〜〉「〜の X 倍…」。"
       "②{larger as}・④{as large than} は {as} と {than} の組み合わせが誤り。③{as} と {as} の間には比較級ではなく原級を置く。"
       "「2倍」は {twice as large as}、「半分」は {half as large as}。{three times larger than} という言い方も使われるが、入試では {as 〜 as} の形が基本。"
       "<br><b>ポイント</b>：倍数・分数は〈倍数 ＋ {as} 原級 {as}〉。倍数は {as} の前に置く。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語を並べかえよ。<br>これは私が今までに読んだ中で最もおもしろい本だ。<br>{This is} （ {interesting / ever / the / I / most / book / have / read} ）.",
  "a": "{This is the most interesting book I have ever read.}",
  "s": "〈最上級 ＋ 名詞 ＋ ({that}) S {have ever done}〉「今までに〜した中で最も…」。{ever} は「今までに」で、経験の現在完了とともに使う。"
       "{book} の後には目的格の関係代名詞 {that} が省略されている。"
       "<br><b>ポイント</b>：同じ内容を {I have never read such an interesting book.} / {I have never read a more interesting book.} と書きかえられる。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{Time is the most precious thing of all.}<br>＝ {Nothing is (　) (　) than time.}",
  "a": "{more, precious}",
  "s": "{Nothing is 比較級 than 〜}「〜ほど…なものはない」は最上級の意味になる。"
       "原級を使えば {Nothing is as (so) precious as time.}。"
       "<br><b>ポイント</b>：否定の主語（{Nothing / No one / No other 〜}）＋比較級／原級で、最上級の意味を表す。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{This new computer ①<u>is</u> ②<u>far</u> ③<u>superior than</u> the old one ④<u>in</u> speed.}",
  "a": "③ {superior than → superior to}",
  "s": "{superior}（〜より優れた）, {inferior}（劣った）, {senior}（年上の）, {junior}（年下の）など {-ior} で終わる形容詞は、{than} ではなく {to} で比較の相手を示す。{prefer A to B} も同じく {to}。"
       "②{far} は比較の意味を強める語で、{superior} にも使える。④{in speed}「速度の点で」は正しい。"
       "<br><b>ポイント</b>：{-ior} の形容詞 ＋ {to}。{more superior} のように {more} を付けることもしない。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>彼は5ドルしか持っていない。<br>{He has no (　) than five dollars.}",
  "a": "{more}",
  "s": "{no more than 〜}「〜しか（ない）」（＝ {only}）、{no less than 〜}「〜も（ある）」（＝ {as much as}）。"
       "{no} ＋比較級は「差がゼロ」を表し、{no more than} は「〜より多くない、少ない」という話し手の気持ちを含む。"
       "{not more than 〜}「多くても〜（＝ {at most}）」、{not less than 〜}「少なくとも〜（＝ {at least}）」と区別する。"
       "<br><b>ポイント</b>：{no more than}＝{only}、{no less than}＝{as many / much as}。{not} の形は「多くても／少なくとも」。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{She is no more a singer than I am.}",
  "a": "私が歌手でないのと同様に、彼女も歌手ではない。",
  "s": "{A is no more B than C is (D)}「C が D でないのと同様に、A も B ではない」。{than} 以下には「明らかに成り立たないこと」（私が歌手であること）を置き、それと同じくらい A も B ではない、と強く否定する。"
       "「私よりも歌手ではない」のような直訳は誤り。反対に {A is no less B than C is (D)} は「C が D であるのと同様に A も B である」（肯定）。"
       "<br><b>ポイント</b>：{no more 〜 than …} は「…でないのと同様に〜でない」（両方否定）。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{It is not so much what you say as how you say it that determines whether people will listen to you.}",
  "a": "人が話を聞いてくれるかどうかを決めるのは、何を言うかというよりむしろ、どのように言うかである。",
  "s": "{It is 〜 that …} の強調構文で、強調されているのは {not so much A as B}「A というよりむしろ B」の部分。A ＝ {what you say}（何を言うか）、B ＝ {how you say it}（どう言うか）で、どちらも間接疑問。"
       "{whether people will listen to you} は {determines} の目的語の名詞節「人々が耳を傾けるかどうか」。名詞節なので、未来のことに {will} を使っている。{you} は一般の人を指すので「あなた」と訳さなくてよい。"
       "<br><b>ポイント</b>：{It is} と {that} を外し、強調された語句を主語の位置に戻して {〜 determines whether …} という文が完成すれば強調構文。強調部分を「…のは〜だ」の「〜」に置いて訳す。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>日本の人口は、アメリカの人口の約3分の1だ。",
  "a": "{The population of Japan is about one third as large as that of the United States.}（{about one third of that of the United States} も可）",
  "s": "比べるのは「人口」どうしなので、2つ目の {population} を {that} で受けて {that of the United States} とする（× {as large as the United States}：人口と国を比べることになる）。"
       "分数も倍数と同じく {as 原級 as} の前に置く（{one third} は {a third} でもよい）。"
       "人口の大小は {large / small} で表す（× {many / much}）。"
       "<br><b>ポイント</b>（採点）：比較の対象をそろえる {that of 〜}、人口に使う形容詞 {large}、分数の位置。"},
]

CH = {N: {"goal": "原級・比較級・最上級の基本形と、比較級の強調・倍数表現・最上級の書きかえ・比較の慣用表現を使いこなせるようにする。",
          "items": [dict(it, q=T(it["q"]), a=T(it["a"]), s=T(it["s"])) for it in ITEMS]}}

def verify():
    its = CH[N]["items"]
    lv = [it["lv"] for it in its]
    assert lv.count("A") == 4 and 4 <= lv.count("B") <= 5 and lv.count("C") == 2 and lv == sorted(lv)
    for it in its:
        for k in ("lv", "tag", "q", "a", "s"):
            assert it.get(k), k
        for k in ("q", "a", "s"):
            v = it[k]
            assert "$" not in v and "{" not in v and "}" not in v, v
            assert "( )" not in v and "()" not in v, v
            for o, c in (("<span ", "</span>"), ("<u>", "</u>"), ("<b>", "</b>")):
                assert v.count(o) == v.count(c), (o, v)
        assert "<b>ポイント</b>" in it["s"], it["q"]
        if it["tag"] == "文法4択":
            assert all(c in it["q"] for c in "①②③④") and it["q"].count("(　)") == 1
            assert it["a"] in ("①", "②", "③", "④")
        if it["tag"] == "正誤":
            assert it["q"].count("<u>") == 4 and it["a"][0] in "①②③④"
