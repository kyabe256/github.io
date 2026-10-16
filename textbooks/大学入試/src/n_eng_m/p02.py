"""問題集 第2章 時制。英語は機械検算ができないので、verify() は形式の点検（問題数・空欄・4択の答えの範囲・書式）のみ。
本文中の {…} は英語の書体（span.en）に変換する。"""
import re

N = 2

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
  "q": Q4("I (　) home from school when it started to rain.", ["walk", "was walking", "have walked", "am walking"], LEAD),
  "a": "②",
  "s": "「雨が降り始めた」という過去の一時点に、歩いて帰る動作が進行中だったので過去進行形 {was walking}。"
       "①現在形 {walk} は過去の話に合わない。③現在完了は、{when} ＋過去形のように過去の一時点をはっきり示す語句とはいっしょに使えない。④現在進行形も過去の話には使えない。"
       "<br><b>ポイント</b>：「〜していたとき…した」は〈過去進行形 ＋ {when} ＋ 過去形〉が基本の組み合わせ。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("Please call me as soon as you (　) at the station.", ["will arrive", "arrive", "arrived", "would arrive"]),
  "a": "②",
  "s": "{as soon as}（〜するとすぐに）は時を表す副詞節をつくる。時・条件の副詞節の中では、未来のことでも現在形で表すので {arrive}。"
       "①{will arrive}・④{would arrive} は副詞節の中なので不可。③過去形 {arrived} では、これからのことを頼む {Please call me} と時が合わない。"
       "<br><b>ポイント</b>：{when, before, after, until, as soon as, if, unless} などが導く副詞節では、未来のことを現在形で表す（未来完了の内容は現在完了で表す）。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("My uncle (　) to Canada three years ago.", ["has moved", "moves", "moved", "had moved"]),
  "a": "③",
  "s": "{ago}（今から〜前）は過去の一時点を表すので過去形 {moved}。"
       "①現在完了は {ago, yesterday, last week} などの過去を示す語句と使えない。④過去完了は「過去のある時点よりさらに前」を表す形で、基準となる過去の時点が文中にないので不可。②現在形も不可。"
       "<br><b>ポイント</b>：現在完了は「今」とつながる形。はっきりした過去の時点を示す語句（{ago} / {yesterday} / {When 〜?} など）があれば過去形。"},
 {"lv": "A", "tag": "文法4択",
  "q": Q4("By the time you come back, I (　) writing this report.", ["finish", "will have finished", "had finished", "have been finishing"]),
  "a": "②",
  "s": "{by the time 〜}「〜するときまでに」。未来のある時点（あなたが戻るとき）までに完了しているはずの動作なので、未来完了 {will have finished}。{by the time} の節は時の副詞節なので、未来のことでも {come}（現在形）になっている点にも注意。"
       "①現在形では、主節で「戻るときまでに終えてしまっているだろう」という未来の完了を表せない。③過去完了は過去の基準時が必要。④現在完了進行形は「今までずっと〜している」で、未来の時点までの完了を表さない。"
       "<br><b>ポイント</b>：「（未来の時点）までに…してしまっているだろう」→ 未来完了 {will have done}。"},
 {"lv": "B", "tag": "整序",
  "q": "日本語に合うように（　）内の語句を並べかえよ。<br>彼女は今朝からずっとピアノを練習している。<br>（ {been / practicing / she / has / the piano / since this morning} ）",
  "a": "{She has been practicing the piano since this morning.}",
  "s": "動作動詞 {practice} が、過去のある時点（今朝）から今まで続いているので、現在完了進行形 {have / has been doing}。{since} は起点「〜から（ずっと）」を表す。"
       "<br><b>ポイント</b>：継続を表すとき、状態動詞（{know, be, have} など）は現在完了 {have done}、動作動詞は現在完了進行形 {have been doing} が基本。"},
 {"lv": "B", "tag": "正誤",
  "q": SEIGO + "{I wonder ①<u>if</u> it ②<u>rains</u> tomorrow. If it ③<u>rains</u>, the game ④<u>will be put off</u>.}",
  "a": "② {rains → will rain}",
  "s": "最初の {if} 節は {wonder} の目的語になる名詞節「〜かどうか」。名詞節の中では未来のことは {will} で表すので {will rain}。"
       "2つ目の {If} 節は「もし〜なら」という条件の副詞節なので、③現在形 {rains} で正しい。④{put off}（延期する）の受動態 {will be put off} も正しい。①{wonder if 〜}「〜かしらと思う」も正しい。"
       "<br><b>ポイント</b>：{if}・{when} の節は、「〜かどうか／いつ〜か」（名詞節）なら {will}、「もし〜なら／〜するとき」（副詞節）なら現在形。"},
 {"lv": "B", "tag": "書きかえ",
  "q": "ほぼ同じ意味になるように、空所に1語ずつ補え。<br>{My grandfather died five years ago.}<br>＝ {My grandfather has (　) (　) for five years.}",
  "a": "{been, dead}",
  "s": "{die}「死ぬ」は一瞬で終わる動作なので、{for five years} のような期間を表す語句とは結べない（× {has died for five years}）。「死んでいる」という状態を表す形容詞 {dead} を使い、継続の現在完了 {has been dead} とする。"
       "同じ内容は {It has been five years since my grandfather died.} / {Five years have passed since my grandfather died.} でも表せる。"
       "<br><b>ポイント</b>：一瞬の動作の動詞（{die, arrive, leave} など）で継続を言うときは、状態の表現（{be dead / be here / be away}）に言いかえる。"},
 {"lv": "B", "tag": "空所補充",
  "q": "日本語に合うように、空所に1語を補え。<br>彼女は、翌日パリに発つと言った。<br>{She said that she (　) leave for Paris the next day.}",
  "a": "{would}",
  "s": "主節の動詞が過去（{said}）なので、従属節の {will} は過去形 {would} になる（時制の一致）。"
       "直接話法なら {She said, \"I will leave for Paris tomorrow.\"} で、間接話法にすると {tomorrow} は {the next day} に変わる。"
       "<br><b>ポイント</b>：時制の一致では {will → would}、{can → could}、現在 → 過去、過去 → 過去完了（前後関係が明らかなら過去のままでもよい）。ただし不変の真理（{The earth goes around the sun.}）は現在形のままでよい。"},
 {"lv": "B", "tag": "和訳",
  "q": "和訳せよ。<br>{By the time she was twenty, she had already visited more than thirty countries.}",
  "a": "20歳になるまでに、彼女はすでに30を超える国を訪れていた。",
  "s": "{by the time 〜}「〜するまでに」。基準は過去（20歳のとき）で、それまでに完了していた経験を表すので過去完了 {had visited}。"
       "{more than thirty} は厳密には「30より多い（31以上）」なので、「30か国以上」と訳すとわずかにずれる。和訳では「30を超える」「30余りの」とするのが安全。"
       "<br><b>ポイント</b>：過去完了を見たら、まず「過去の基準時」（ここでは {she was twenty}）を探し、それより前のことだと確認する。"},
 {"lv": "C", "tag": "和訳",
  "q": "和訳せよ。<br>{For decades, doctors had believed that the disease was caused only by stress, but recent research has shown that bacteria also play an important role.}",
  "a": "何十年もの間、医師たちはその病気はストレスだけが原因で起こると信じていたが、最近の研究によって、細菌も重要な役割を果たしていることが明らかになった。",
  "s": "時制の流れを確認する。{had believed} は過去完了（継続）で、「最近の研究」が出るより前の過去までずっと信じていた、という意味。"
       "{was caused} は {believed} に合わせた時制の一致なので、日本語では「起こる」と現在のように訳してよい。"
       "{has shown} は現在完了（結果）で、研究の成果が今も有効であることを表す。後半の {that} 節の {play} は、主節が現在完了（現在の仲間）なので時制の一致を受けず現在形のまま。"
       "{research has shown that 〜} は無生物主語なので「研究によって〜が明らかになった」と訳すと自然。{only by stress} の {only} が「ストレスだけ」と {also}「細菌も」の対比をつくっている。"
       "<br><b>ポイント</b>：時制の一致で過去形になった動詞は、日本語では現在形のように訳す。"},
 {"lv": "C", "tag": "英作文",
  "q": "英語に直せ。<br>私がこの町に引っ越してきて3年になるが、近所の人の名前をまだほとんど知らない。",
  "a": "{It has been three years since I moved to this town, but I still hardly know any of my neighbors' names.}",
  "s": "「〜して3年になる」は {It has been three years since S ＋過去形} が基本（{It is three years since 〜} も可）。"
       "{Three years have passed since I moved to this town} や {I have lived in this town for three years} も正しい。"
       "{since} の節は「引っ越した」という過去の一時点なので過去形 {moved}（× {since I have moved}）。"
       "「ほとんど〜ない」は {hardly}（{I still know very few of my neighbors' names.} も可）。{still} は否定の語の前に置く。"
       "<br><b>ポイント</b>（採点）：{since} 節の時制（過去形）と主節の現在完了、複数形の所有格 {neighbors'} のアポストロフィの位置。"},
]

CH = {N: {"goal": "時を表す語句と文脈から、進行形・完了形・未来の表し方と時制の一致を正しく使い分けられるようにする。",
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
