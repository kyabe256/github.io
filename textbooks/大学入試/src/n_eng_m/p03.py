"""問題集 第3章 助動詞。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 3

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
  "q": Q4("Emma (　) have been at home at three yesterday afternoon. I saw her at the stadium at that time.", ["must", "can't", "may", "need"], LEAD),
  "a": "②",
  "s": "その時刻にスタジアムで見たのだから、「家にいたはずがない」。過去のことへの強い否定の推量は {can't have ＋過去分詞}。"
       "①{must have been}「いたに違いない」は文脈と逆。③{may have been}「いたかもしれない」も、見たという事実と矛盾する。④{need} は肯定文では助動詞として使わない（否定の {needn't have done}「〜する必要はなかったのに」はある）。"
       "<br><b>ポイント</b>：過去への推量は {must have done}（〜したに違いない）⇔ {can't have done}（〜したはずがない）、{may have done}（〜したかもしれない）。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("You had better (　) late again.", ["not be", "be not", "not to be", "don't be"]),
  "a": "①",
  "s": "{had better ＋原形}「〜したほうがよい（さもないと困ったことになる）」。否定は {had better not ＋原形} の語順。"
       "②は {not} の位置が誤り。③{had better} の後に {to} は付けない。④{don't} は {had better} の後に置けない。"
       "<br><b>ポイント</b>：{had better not do}。{had better} は強い忠告で、目上の人に使うと命令的に響く。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I would rather (　) at home than go out in this storm.", ["stay", "to stay", "staying", "stayed"]),
  "a": "①",
  "s": "{would rather A than B}「B するよりむしろ A したい」。A・B とも原形で、{than} の後の {go} も原形になっている。"
       "②③は形が誤り。④過去形が来るのは {would rather S ＋過去形}「S に〜してほしい」（{I'd rather you stayed home.}）の形で、主語なしで過去形を続けることはできない。"
       "<br><b>ポイント</b>：{would rather do}（自分が〜したい）と {would rather S did}（他人に〜してほしい）を区別する。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("My father is used to (　) up early.", ["get", "getting", "got", "be got"]),
  "a": "②",
  "s": "{be used to doing}「〜するのに慣れている」の {to} は前置詞なので、後ろは名詞か動名詞。"
       "①を入れた {is used to get up} は、{use}（使う）の受動態＋目的の不定詞「起きるために使われる」になってしまい、文意が通らない。③④は形が誤り。"
       "<br><b>ポイント</b>：{used to do}（以前は〜したものだ）／{be used to doing}（〜するのに慣れている）／{be used to do}（〜するために使われる）の3つを区別する。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語句を並べかえよ。<br>彼がそんなことを言ったはずがない。<br>（ {said / have / he / such / can't / a thing} ）",
  "a": "{He can't have said such a thing.}",
  "s": "「〜したはずがない」は過去の内容への否定の推量なので {can't}（{cannot}）{have ＋過去分詞}。{such a thing} は〈{such ＋ a ＋名詞}〉の語順（× {a such thing}）。"
       "<br><b>ポイント</b>：「〜したはず（がない）」「〜したに違いない」は、助動詞の後を {have done} にして過去のことを表す。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{You ①<u>needn't to worry</u> about the test, ②<u>because</u> you ③<u>have studied</u> so ④<u>hard</u>.}",
  "a": "① {needn't to worry → needn't worry}（{don't need to worry} も可）",
  "s": "助動詞の {need}（おもに否定文・疑問文で使う）の後は原形で、{to} は付けない。一般動詞の {need} を使うなら {don't need to worry}。"
       "③現在完了「これまでずっと熱心に勉強してきた」で正しい。④{hard} は副詞「熱心に」で正しい（{hardly}「ほとんど〜ない」と混同しない）。"
       "<br><b>ポイント</b>：{needn't do} ＝ {don't need to do} ＝ {don't have to do}「〜する必要はない」。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{It is natural that he should get angry.}<br>＝ {He (　) (　) get angry.}",
  "a": "{may, well}（{might well} も可）",
  "s": "{may well do} には「〜するのももっともだ」と「たぶん〜するだろう」の2つの意味がある。ここは {It is natural that 〜 should …}「…するのは当然だ」の言いかえなので前者。"
       "似た形の {may as well do}「〜したほうがよい（〜してもよい）」と混同しない。"
       "<br><b>ポイント</b>：{may well}（もっともだ／たぶん〜だろう）と {may as well}（〜したほうがよい）は {as} の有無で意味が変わる。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>健康にはいくら注意してもしすぎることはない。<br>{You cannot be (　) careful about your health.}",
  "a": "{too}",
  "s": "{cannot … too 〜}「いくら〜してもしすぎることはない」。「〜しすぎることはありえない」→「いくら〜してもよい」と考える。"
       "同じ意味で {cannot … enough} も使う（{I cannot thank you enough.}「いくら感謝してもしきれません」）。"
       "<br><b>ポイント</b>：{cannot} と {too / enough} の組み合わせは「いくら〜しても足りない」の意味の慣用表現。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{You should have seen the sunset from the hill last night. It was amazing.}",
  "a": "昨夜の丘からの夕日を、君にも見せたかったよ。すばらしかった。",
  "s": "{should have ＋過去分詞} は「〜すべきだった（のに実際はしなかった）」が基本。ここは相手を責めているのではなく、相手が見なかったことを惜しんで「見ればよかったのに」→「見せたかった」と言っている。"
       "次の {It was amazing.} が、その気持ちの理由になっている。"
       "<br><b>ポイント</b>：{should have done} は「実際にはしなかった」ことが前提。後悔（自分）・非難（相手）・残念な気持ちのどれかは文脈で決める。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{Good teachers need not know every answer, but they must be willing to admit what they do not know, for students learn as much from their honesty as from their knowledge.}",
  "a": "よい教師はあらゆる答えを知っている必要はないが、自分が知らないことを進んで認めなければならない。というのも、生徒は教師の知識からと同じくらい、その誠実さからも学ぶからである。",
  "s": "{need not do}「〜する必要はない」（助動詞 {need} の否定）。{not 〜 every …} は部分否定で、「すべての答えを知っている必要はない」の意味（「どの答えも知らなくてよい」ではない）。"
       "{must be willing to do}「進んで〜する気持ちがなければならない」。{what they do not know} は関係代名詞 {what}「知らないこと」。"
       "{for} は等位接続詞で「というのも〜だから」と理由を補う（ふつうコンマの後に置き、前の内容の根拠を付け足す）。{as much from A as from B} は「B からと同じくらい A からも」。{their} は2つとも {teachers} を指す。"
       "<br><b>ポイント</b>：{need not} ＋部分否定 {every} の組み合わせと、理由を補う接続詞 {for} の訳し方。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>駅にかさを置き忘れてきたに違いない。もっと注意すべきだった。",
  "a": "{I must have left my umbrella at the station. I should have been more careful.}",
  "s": "「〜したに違いない」は過去への推量 {must have done}。「〜すべきだった（のにしなかった）」は {should have done}（{ought to have done} も可）。"
       "「（物を場所に）置き忘れる」は {leave}。{forget} はふつう場所を表す語句といっしょには使わない（× {I forgot my umbrella at the station.}）。"
       "<br><b>ポイント</b>（採点）：〈助動詞 ＋ {have} ＋過去分詞〉の形、{leave} の過去分詞 {left}、{careful} の前の {be}（{been}）を落としていないか。"},
]

CH = {N: {"goal": "助動詞の意味（可能・義務・推量）と〈助動詞＋have＋過去分詞〉、助動詞を含む慣用表現を、文脈から使い分けられるようにする。",
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
