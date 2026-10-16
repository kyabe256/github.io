"""問題集 第10章 仮定法。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 10

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
  "q": Q4("If I (　) you, I would accept the offer.", ["am", "were", "had been", "will be"], LEAD),
  "a": "②",
  "s": "主節が {would ＋原形} なので、現在の事実に反する仮定 → 仮定法過去。{be} 動詞は主語に関係なく {were} が基本（くだけた言い方では {was} も使う）。"
       "③{had been} は仮定法過去完了で、主節が {would have accepted} でなければ合わない。①{am}・④{will be} は直説法で、「私があなたである」という現実にありえない仮定には使えない。"
       "<br><b>ポイント</b>：仮定法過去は〈{If S 過去形}, {S would / could / might ＋原形}〉。{if} 節と主節の形をセットで確認する。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("She missed the train by one minute. If she had left home earlier, she (　) it.", ["would catch", "would have caught", "will catch", "had caught"]),
  "a": "②",
  "s": "実際には1分差で電車に乗り遅れた（過去の事実）。それに反する仮定なので、{if} 節は仮定法過去完了 {had left}、主節は {would have ＋過去分詞}。"
       "①{would catch} は「（今）乗るだろう」となり、すでに出てしまった電車の話と合わない。③{will catch} は直説法。④{had caught} は主節に助動詞がなく、仮定の結果を表せない。"
       "<br><b>ポイント</b>：仮定法過去完了は〈{If S had done}, {S would / could / might have done}〉。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("I wish I (　) more time to talk with you yesterday.", ["have", "had", "had had", "would have"]),
  "a": "③",
  "s": "{yesterday} があるので、過去の事実に反する願望 → {I wish ＋ 仮定法過去完了（had ＋過去分詞）}。{had had} は {have}（持つ）の過去完了形。"
       "②{had} は仮定法過去で「今もっと時間があればなあ」となり、{yesterday} と合わない。①{have} は直説法で {wish} の後に使えない。④{I wish I would 〜} は自分の行動についてはふつう使わず、時も合わない。"
       "<br><b>ポイント</b>：{I wish} ＋仮定法過去（今の願望）／仮定法過去完了（過去への後悔）。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("(　) your help, I would have failed.", ["But for", "Because", "In spite", "Unless"]),
  "a": "①",
  "s": "{but for 〜}「〜がなかったら」（＝ {without 〜}）。主節が {would have failed} なので過去の仮定で、{If it had not been for your help} と同じ意味。"
       "②{Because} は接続詞で、後ろに名詞だけを置けない（{because of} でも意味が合わない）。③{In spite} は {of} が必要で、意味も「〜にもかかわらず」で合わない。④{Unless} は接続詞で、後ろに S V が必要。"
       "<br><b>ポイント</b>：{without / but for 〜} は、主節の形（{would do} か {would have done}）で今の仮定か過去の仮定かを判断する。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語を並べかえよ。<br>もしその列車に乗っていたら、私は事故に巻き込まれていたかもしれない。<br>（ {I / had / train / taken / that} ）, {I might have been involved in the accident.}",
  "a": "{Had I taken that train, I might have been involved in the accident.}",
  "s": "{If I had taken that train} の {if} を省略すると、主語と {had} の語順が入れかわる（倒置）→ {Had I taken that train}。"
       "{were}・{should} で始まる仮定でも同じ倒置が起こる（{Were I you, 〜} / {Should you need help, 〜}）。"
       "<br><b>ポイント</b>：文頭の {Had / Were / Should ＋ S} を見たら、{if} が省略された仮定法と考える。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{As I don't have a car, I can't drive you home.}<br>＝ {If I (　) a car, I (　) drive you home.}",
  "a": "{had, could}",
  "s": "直説法の現在（車を持っていない）を、仮定法過去で裏返して表す。肯定・否定も逆になる（{don't have → had}、{can't → could}）。"
       "<br><b>ポイント</b>：直説法 → 仮定法の書きかえは、時を1つ過去にずらし、肯定と否定を入れかえる。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{I ①<u>wish</u> I ②<u>can speak</u> French ③<u>as well as</u> my sister ④<u>does</u>.}",
  "a": "② {can speak → could speak}",
  "s": "{I wish} の後は仮定法。今の事実に反する願望なので仮定法過去の {could speak}。"
       "③{as well as}「〜と同じくらい上手に」は正しい。④{does} は {speaks French} の代わりをする代動詞で正しい。"
       "<br><b>ポイント</b>：{I wish} の後に {can / will} などの現在形を置かない。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語ずつ補え。<br>水がなければ、どんな生物も存在できないだろう。<br>{If it (　) not (　) water, no living thing could exist.}",
  "a": "{were, for}",
  "s": "{if it were not for 〜}「（今）〜がなければ」は仮定法過去の慣用表現。過去のことなら {if it had not been for 〜}。"
       "どちらも {without 〜 / but for 〜} で言いかえられ、{if} を省略すると {Were it not for water, 〜} となる。"
       "<br><b>ポイント</b>：{if it were not for}（今）／{if it had not been for}（過去）を主節の形と対応させる。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{He looked at me as if he had never seen me before.}",
  "a": "彼は、まるでそれまで一度も私に会ったことがないかのように私を見た。",
  "s": "{as if ＋ 仮定法過去完了}「まるで〜したかのように」。主節（{looked}）より前のことなので過去完了になっている。"
       "主節と同じ時のことなら {as if ＋ 仮定法過去}（{as if he didn't know me}「私を知らないかのように」）。{as if} の節の形は、主節が過去か現在かでは変わらない。"
       "<br><b>ポイント</b>：{as if} の後の時制は「主節と同じ時 → 仮定法過去、主節より前 → 仮定法過去完了」。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{If humans had not learned to use fire, our brains might not be as large as they are today.}",
  "a": "もし人類が火を使うことを覚えていなかったら、私たちの脳は今日ほど大きくはなっていなかったかもしれない。",
  "s": "{if} 節は仮定法過去完了（過去の事実に反する仮定：実際は火を使うことを覚えた）、主節は仮定法過去（今の事実に反する推量：{might not be}）。"
       "「過去の仮定 → 今の結果」を表す混合型の仮定法。{as large as they are today} の {are} は、現実の今の脳の大きさを表すので直説法。"
       "{learn to do}「〜できるようになる、〜することを覚える」。"
       "<br><b>ポイント</b>：主節に {now / today} があり、{if} 節が {had done} なら混合型を疑う。"},
 {"lv": "C", "tag": "条件英作文",
  "q": "次の問いに、仮定法を用いて30語程度の英語で答えよ。<br>{If you could have any special ability, what would it be, and why?}",
  "a": "（解答例）{I would choose the ability to speak every language in the world. Then I could talk freely with people from any country without an interpreter and understand their cultures more deeply.}（31語）",
  "s": "問いが仮定法（{could have / would it be}）なので、答えも {would / could} を使い、「もし〜できたら」という仮の話として書く。× {I will choose 〜} では、現実に起こることのように聞こえる。"
       "構成は、(1) どの能力か（{I would choose 〜} / {I would like to be able to 〜}）、(2) その能力で何ができるか・理由（{Then I could 〜} / {because I could 〜}）の2文が書きやすい。"
       "別解の例：{I would like to be able to fly. Then I could visit my grandparents, who live far away, whenever I wanted.}"
       "<br><b>ポイント</b>（採点）：仮定法の動詞の形が最後まで一貫しているか、理由が具体的か、語数（30語程度）。"},
]

CH = {N: {"goal": "仮定法過去・仮定法過去完了・混合型・if の省略（倒置）・wish / as if / without などを、時を表す語句と照らし合わせて正しく使えるようにする。",
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
    # 条件英作文の解答例の語数（「30語程度」）
    ex = [it for it in its if it["tag"] == "条件英作文"][0]["a"]
    words = re.sub(r"<[^>]+>", "", ex.split("（31語）")[0]).replace("（解答例）", "").split()
    assert len(words) == 31, len(words)
