"""問題集 第6章 動名詞。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 6

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
  "q": Q4("I'm looking forward to (　) you again.", ["see", "seeing", "be seen", "have seen"], LEAD),
  "a": "②",
  "s": "{look forward to doing}「〜するのを楽しみに待つ」の {to} は前置詞なので、後ろは名詞か動名詞。"
       "①原形を入れるのが典型的な誤り。③{be seen}・④{have seen} も前置詞の後には置けない形。"
       "<br><b>ポイント</b>：{to} が前置詞の表現 ― {look forward to / be used to / object to / when it comes to / What do you say to} ＋ {doing}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("Would you mind (　) the window?", ["to open", "opening", "open", "opened"]),
  "a": "②",
  "s": "{mind}「〜をいやだと思う」は動名詞だけを目的語にとる動詞。①不定詞、③原形、④過去分詞はいずれも不可。"
       "「窓を開けていただけませんか」の意味で、承諾するときは「いやではない」ので {Not at all.} / {Of course not.} と否定で答える。"
       "<br><b>ポイント</b>：動名詞だけをとる動詞 ― {mind, enjoy, finish, avoid, give up, put off, deny, consider, practice, escape}。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I remember (　) this man somewhere before.", ["meet", "to meet", "meeting", "met"]),
  "a": "③",
  "s": "{remember doing}「（過去に）〜したことを覚えている」、{remember to do}「（これから）忘れずに〜する」。{somewhere before}（以前どこかで）があり過去のことなので動名詞。"
       "②{to meet} では「忘れずに会う」となり文意に合わない。①原形、④過去形は {remember} の目的語にならない。"
       "<br><b>ポイント</b>：{remember / forget / regret} は、動名詞＝すでにしたこと、不定詞＝これからすること。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("There is no (　) what will happen next.", ["know", "knowing", "to know", "known"]),
  "a": "②",
  "s": "{There is no doing}「〜することはできない」（＝ {It is impossible to do}）は動名詞の慣用表現。{no} の後には名詞か動名詞が来るので、③不定詞は不可。①原形、④過去分詞も不可。"
       "<br><b>ポイント</b>：動名詞の慣用表現 ― {There is no doing / It is no use doing}（〜しても無駄だ）/ {cannot help doing}（〜せずにはいられない）/ {feel like doing}（〜したい気がする）。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語句を並べかえよ。<br>彼は私がその会に参加することに反対した。<br>（ {objected / my / to / joining / he} ） {the meeting.}",
  "a": "{He objected to my joining the meeting.}",
  "s": "{object to doing}「〜することに反対する」の {to} は前置詞。動名詞の意味上の主語は、所有格（{my}）か目的格（{me}）で動名詞の直前に置く。"
       "{He objected to me joining the meeting.} も可（くだけた言い方）。"
       "<br><b>ポイント</b>：文の主語と動名詞の動作をする人が違うとき、〈所有格／目的格 ＋ {doing}〉で意味上の主語を示す。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{Please ①<u>stop to talk</u> and ②<u>listen</u> to me ③<u>carefully</u>; this is ④<u>really important</u>.}",
  "a": "① {stop to talk → stop talking}",
  "s": "{stop doing}「〜するのをやめる」、{stop to do}「〜するために立ち止まる（手を止める）」。ここは「おしゃべりをやめてよく聞いて」の意味なので {stop talking}。"
       "{stop to talk} は文法的には成り立つが「話すために立ち止まる」となり、文脈に合わない。②{listen to}、③副詞 {carefully}、④{really important} はいずれも正しい。"
       "<br><b>ポイント</b>：{stop} の目的語になるのは動名詞だけ。{stop to do} の不定詞は目的を表す副詞用法。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "動名詞を用いて、ほぼ同じ意味になるように空所に1語ずつ補え。<br>{I'm sure that he will succeed.}<br>＝ {I'm sure of (　) (　).}",
  "a": "{his, succeeding}（{him succeeding} も可）",
  "s": "前置詞 {of} の後に {that} 節は置けないので、{that} 節を動名詞句にする。{he} は動名詞の意味上の主語として所有格 {his}（または目的格 {him}）にする。"
       "名詞を使えば {I'm sure of his success.} とも言える。"
       "<br><b>ポイント</b>：{that} 節 →〈前置詞 ＋ 意味上の主語 ＋ 動名詞〉の書きかえ。{be sure of / be proud of / insist on} などで出る。"},
 {"lv": "B", "tag": "空所補充",
  "q": "〔　〕内の語を適切な形にして空所に入れよ。<br>{This shirt needs (　).}　〔 {wash} 〕",
  "a": "{washing}",
  "s": "{need doing} は「〜される必要がある」と受動の意味になる。{This shirt needs to be washed.} と同じ意味。"
       "シャツは「洗う」側ではなく「洗われる」側だが、{need} の後の動名詞は能動の形のままで受動の意味を表す。"
       "<br><b>ポイント</b>：{need doing} ＝ {need to be done}（イギリス英語では {want doing} も同じ意味）。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{On hearing the news, she burst into tears.}",
  "a": "その知らせを聞くとすぐに、彼女はわっと泣き出した。",
  "s": "{on doing}「〜するとすぐに」（＝ {As soon as she heard the news}）。{burst into tears}「急に泣き出す」。"
       "{in doing}「〜するときに、〜する際に」と区別する。"
       "<br><b>ポイント</b>：〈前置詞 ＋ 動名詞〉の慣用 ― {on doing}（〜するとすぐに）/ {in doing}（〜するときに）/ {by doing}（〜することによって）/ {without doing}（〜せずに）。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{Being able to admit that you were wrong is not a sign of weakness; on the contrary, it takes courage to change your mind in front of others.}",
  "a": "自分が間違っていたと認められることは、弱さの表れではない。それどころか、人前で考えを変えるには勇気がいるのだ。",
  "s": "文の主語は動名詞句 {Being able to admit that you were wrong}（自分が間違っていたと認められること）で、動詞は {is}。主語が長いので、{is} を見つけて区切る。"
       "{you} は一般の人を表すので「あなた」と訳さない。{on the contrary}「それどころか」は、前の否定を受けて、むしろ反対だと述べる表現。"
       "{it takes ＋名詞＋ to do}「〜するには…が必要だ」の {it} は形式主語。{change one's mind}「考えを変える」。"
       "<br><b>ポイント</b>：動名詞が主語の長い文は、述語動詞を見つけて主語の範囲を確定する。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>寝る前にスマートフォンを使うのをやめてから、よく眠れるようになった。",
  "a": "{Since I stopped using my smartphone before going to bed, I have been able to sleep well.}",
  "s": "「〜するのをやめる」は {stop doing}（× {stop to use}）。「寝る前に」は {before going to bed}（前置詞 {before} ＋動名詞）または {before I go to bed}。"
       "「〜してから（ずっと）…」は {since} ＋過去形と、主節の現在完了を組み合わせる。「眠れるようになった」は {have been able to sleep well}。"
       "別解：{After I stopped using my smartphone before bed, I began to sleep better.} / {I sleep much better now that I've stopped using my smartphone before bed.}"
       "<br><b>ポイント</b>（採点）：{stop doing}、{before} の後の形（動名詞か S V）、{since} と現在完了の組み合わせ。"},
]

CH = {N: {"goal": "動名詞と不定詞の使い分け（動詞の目的語・前置詞の後）、動名詞の意味上の主語、慣用表現を確実にする。",
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
