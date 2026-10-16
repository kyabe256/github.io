"""英語ドリルを drills.json に出力する。
語形（三単現・ing・過去・過去分詞・複数形・比較）は下の表から作るので、表が正しければ答えも正しい。
表の規則形はスペル規則と突き合わせて自己チェックする。"""
import json, random, re
random.seed(7)

def E(s):
    return f'<span class="en">{s}</span>'

# 原形, 三単現, ing, 過去, 過去分詞, 例の目的語など
V = [l.split("|") for l in """play|plays|playing|played|played|tennis
study|studies|studying|studied|studied|English
watch|watches|watching|watched|watched|TV
wash|washes|washing|washed|washed|the dishes
go|goes|going|went|gone|to school
do|does|doing|did|done|the homework
have|has|having|had|had|a dog
make|makes|making|made|made|breakfast
take|takes|taking|took|taken|a bus
come|comes|coming|came|come|home early
get|gets|getting|got|got (gotten)|up at six
see|sees|seeing|saw|seen|the doctor
know|knows|knowing|knew|known|the answer
give|gives|giving|gave|given|a present
write|writes|writing|wrote|written|a letter
read|reads|reading|read|read|a book
speak|speaks|speaking|spoke|spoken|English
run|runs|running|ran|run|in the park
swim|swims|swimming|swam|swum|in the sea
sit|sits|sitting|sat|sat|on the bench
begin|begins|beginning|began|begun|the lesson
stop|stops|stopping|stopped|stopped|the car
plan|plans|planning|planned|planned|a trip
live|lives|living|lived|lived|in Osaka
use|uses|using|used|used|a computer
like|likes|liking|liked|liked|music
try|tries|trying|tried|tried|new things
cry|cries|crying|cried|cried|a lot
carry|carries|carrying|carried|carried|the bag
enjoy|enjoys|enjoying|enjoyed|enjoyed|the party
stay|stays|staying|stayed|stayed|at home
teach|teaches|teaching|taught|taught|math
catch|catches|catching|caught|caught|fish
buy|buys|buying|bought|bought|bread
bring|brings|bringing|brought|brought|lunch
think|thinks|thinking|thought|thought|about it
fly|flies|flying|flew|flown|a kite
eat|eats|eating|ate|eaten|rice
drink|drinks|drinking|drank|drunk|milk
sing|sings|singing|sang|sung|songs
break|breaks|breaking|broke|broken|the window
choose|chooses|choosing|chose|chosen|a book
forget|forgets|forgetting|forgot|forgotten|the name
lose|loses|losing|lost|lost|the key
find|finds|finding|found|found|the key
tell|tells|telling|told|told|a story
say|says|saying|said|said|hello
pay|pays|paying|paid|paid|the bill
leave|leaves|leaving|left|left|home at eight
meet|meets|meeting|met|met|friends
sleep|sleeps|sleeping|slept|slept|well
keep|keeps|keeping|kept|kept|a diary
send|sends|sending|sent|sent|an email
spend|spends|spending|spent|spent|money
build|builds|building|built|built|a house
put|puts|putting|put|put|the box here
cut|cuts|cutting|cut|cut|the paper
become|becomes|becoming|became|become|a teacher
grow|grows|growing|grew|grown|vegetables
draw|draws|drawing|drew|drawn|pictures
throw|throws|throwing|threw|thrown|the ball
wear|wears|wearing|wore|worn|a cap
win|wins|winning|won|won|the game
hold|holds|holding|held|held|the baby
stand|stands|standing|stood|stood|by the door
understand|understands|understanding|understood|understood|the question
fall|falls|falling|fell|fallen|asleep
hear|hears|hearing|heard|heard|the news
show|shows|showing|showed|shown|the picture
ride|rides|riding|rode|ridden|a bike
drive|drives|driving|drove|driven|a car
lie|lies|lying|lay|lain|on the bed
die|dies|dying|died|died|
fix|fixes|fixing|fixed|fixed|the bike
finish|finishes|finishing|finished|finished|the work
open|opens|opening|opened|opened|the door
visit|visits|visiting|visited|visited|the museum
listen|listens|listening|listened|listened|to music
help|helps|helping|helped|helped|the old man
want|wants|wanting|wanted|wanted|a new bike
need|needs|needing|needed|needed|help
wait|waits|waiting|waited|waited|for the bus
walk|walks|walking|walked|walked|to the station
cook|cooks|cooking|cooked|cooked|dinner
clean|cleans|cleaning|cleaned|cleaned|the room
arrive|arrives|arriving|arrived|arrived|at the station
dance|dances|dancing|danced|danced|well
drop|drops|dropping|dropped|dropped|the cup
miss|misses|missing|missed|missed|the train
mix|mixes|mixing|mixed|mixed|the eggs
touch|touches|touching|touched|touched|the dog
push|pushes|pushing|pushed|pushed|the button
worry|worries|worrying|worried|worried|about the test
hurry|hurries|hurrying|hurried|hurried|to school
prefer|prefers|preferring|preferred|preferred|tea
tie|ties|tying|tied|tied|the shoes""".splitlines()]

IRREG_PAST = {"go", "do", "have", "make", "take", "come", "get", "see", "know", "give", "write", "read", "speak", "run", "swim", "sit",
              "begin", "teach", "catch", "buy", "bring", "think", "fly", "eat", "drink", "sing", "break", "choose", "forget", "lose",
              "find", "tell", "say", "pay", "leave", "meet", "sleep", "keep", "send", "spend", "build", "put", "cut", "become", "grow",
              "draw", "throw", "wear", "win", "hold", "stand", "understand", "fall", "hear", "show", "ride", "drive", "lie"}
VOW = "aeiou"

# --- 規則のチェック（表の打ち間違いを見つける） ---
def s3_rule(b):
    if b == "have": return "has"
    if re.search(r"(s|x|ch|sh|o)$", b): return b + "es"
    if re.search(r"[^aeiou]y$", b): return b[:-1] + "ies"
    return b + "s"
DOUBLE = {"run", "swim", "sit", "begin", "stop", "plan", "get", "put", "cut", "win", "drop", "forget", "prefer"}
def ing_rule(b):
    if b.endswith("ie"): return b[:-2] + "ying"
    if b in DOUBLE: return b + b[-1] + "ing"
    if b.endswith("e") and b not in ("see",): return b[:-1] + "ing"
    return b + "ing"
def ed_rule(b):
    if b.endswith("e"): return b + "d"
    if re.search(r"[^aeiou]y$", b): return b[:-1] + "ied"
    if b in DOUBLE: return b + b[-1] + "ed"
    return b + "ed"
for b, s, ing, p, pp, _ in V:
    assert s == s3_rule(b), (b, s)
    assert ing == ing_rule(b), (b, ing)
    if b not in IRREG_PAST:
        assert p == ed_rule(b) == pp, (b, p, pp)
VD = {v[0]: v for v in V}

D = {}
def add(no, title, items, one=False):
    D[str(no)] = {"title": title, "items": items, **({"one": True} if one else {})}

# ---------- 1 ----------
add(1, "アルファベットと発音", [
    ["母音字をすべて選べ：b, e, k, o, u", "e, o, u"],
    [f"大文字で始めるべきものに直せ：{E('monday')}", E("Monday")],
    [f"大文字で始めるべきものに直せ：{E('japan')}", E("Japan")],
    [f"{E('cake')} の a の読み", "エイ"], [f"{E('cat')} の a の読み", "ア（エとアの中間）"],
    [f"{E('bike')} の i の読み", "アイ"], [f"{E('milk')} の i の読み", "イ"], [f"{E('home')} の o の読み", "オウ"],
    [f"{E('ship')} の sh の読み", "シュ"], [f"{E('phone')} の ph の読み", "フ"],
    [f"{E('know')} で読まない文字", E("k")], [f"{E('write')} で読まない文字", E("w")], [f"{E('listen')} で読まない文字", E("t")],
    [f"{E('hour')} で読まない文字", E("h")], [f"{E('night')} で読まない文字", E("gh")],
    [f"{E('banana')} で強く読むのは何音節目？", "2音節目（ba-<b>NA</b>-na）"], [f"{E('hotel')} で強く読むのは何音節目？", "2音節目"],
    ["水曜日を英語で", E("Wednesday")], ["2月を英語で", E("February")], ["木曜日を英語で", E("Thursday")],
    [f"( ) に a か an：( ) {E('egg')}", E("an")], [f"( ) に a か an：( ) {E('dog')}", E("a")],
])

# ---------- 2 be動詞 ----------
SUBJ = [("I", "am"), ("You", "are"), ("He", "is"), ("She", "is"), ("It", "is"), ("We", "are"), ("They", "are"), ("My father", "is"),
        ("Tom and I", "are"), ("These books", "are"), ("This cat", "is"), ("My parents", "are"), ("Ken", "is"), ("Your sisters", "are"),
        ("That girl", "is"), ("The students", "are")]
COMP = ["happy", "busy", "in the room", "very kind", "from Japan", "hungry", "at the park", "tired"]
items = []
for i in range(30):
    s, be = SUBJ[i % len(SUBJ)]
    c = COMP[(i * 3) % len(COMP)]
    items.append([E(f"{s} ( ) {c}."), E(be)])
add(2, "am / is / are", items)

# ---------- 3 三単現 ----------
S3 = ["He", "She", "My brother", "Ken", "Our teacher", "The boy"]
NS3 = ["I", "You", "They", "We", "My friends"]
cand = [v for v in V if v[5] and v[0] not in ("lie", "die", "fall", "sit", "stand", "put")]
random.shuffle(cand)
items = []
for i, (b, s, ing, p, pp, obj) in enumerate(cand[:30]):
    third = i % 3 != 2
    sub = random.choice(S3 if third else NS3)
    items.append([E(f"{sub} ( ) {obj} every day.") + f"（{b}）", E(s if third else b)])
PRON_S = [("likes", "/s/"), ("stops", "/s/"), ("eats", "/s/"), ("helps", "/s/"), ("walks", "/s/"), ("plays", "/z/"), ("lives", "/z/"),
          ("goes", "/z/"), ("reads", "/z/"), ("runs", "/z/"), ("studies", "/z/"), ("watches", "/iz/"), ("washes", "/iz/"),
          ("teaches", "/iz/"), ("uses", "/iz/"), ("dances", "/iz/")]
items += [[f"{E(w)} の s の発音は /s/・/z/・/iz/ のどれ？", a] for w, a in PRON_S]
add(3, "三単現の s", items)

# ---------- 4 名詞・冠詞・代名詞 ----------
PL = [("book", "books"), ("box", "boxes"), ("bus", "buses"), ("dish", "dishes"), ("watch", "watches"), ("city", "cities"), ("baby", "babies"),
      ("boy", "boys"), ("day", "days"), ("leaf", "leaves"), ("knife", "knives"), ("wife", "wives"), ("potato", "potatoes"), ("tomato", "tomatoes"),
      ("piano", "pianos"), ("photo", "photos"), ("man", "men"), ("woman", "women"), ("child", "children"), ("foot", "feet"), ("tooth", "teeth"),
      ("mouse", "mice"), ("fish", "fish"), ("sheep", "sheep"), ("person", "people"), ("family", "families"), ("key", "keys"), ("class", "classes"),
      ("country", "countries"), ("wolf", "wolves")]
items = [[f"複数形に：{E(a)}", E(b)] for a, b in PL]
PR = [("This is ( ) bag.", "私の", "my"), ("Do you know ( )?", "彼を", "him"), ("( ) name is Mika.", "彼女の", "Her"), ("That car is ( ).", "私たちのもの", "ours"),
      ("I like ( ) very much.", "彼らを", "them"), ("Is this pen ( )?", "あなたのもの", "yours"), ("( ) are good friends.", "私たちは", "We"),
      ("The dog wagged ( ) tail.", "その（犬の）", "its"), ("Please help ( ).", "私を", "me"), ("These books are ( ).", "彼女のもの", "hers"),
      ("( ) house is big.", "彼らの", "Their"), ("Look at ( ).", "彼女を", "her"), ("This is ( ) room.", "ケンの", "Ken's"),
      ("Whose cap is this? — It's ( ).", "彼のもの", "his")]
items += [[E(q) + f"（{j}）", E(a)] for q, j, a in PR]
AN = [("umbrella", "an"), ("university", "a"), ("hour", "an"), ("old car", "an"), ("useful book", "a"), ("honest man", "an"), ("uniform", "a"), ("egg", "an")]
items += [[f"a か an：( ) {E(w)}", E(a)] for w, a in AN]
add(4, "複数形・代名詞・a と an", items)

# ---------- 5 疑問詞 ----------
Q5 = [("( ) is your birthday? — It's July 3.", "When"), ("( ) do you live? — In Kobe.", "Where"), ("( ) is that girl? — She's my sister.", "Who"),
      ("( ) bike is this? — It's Tom's.", "Whose"), ("( ) do you like, red or blue? — Blue.", "Which"), ("( ) are you happy? — Because I won.", "Why"),
      ("( ) do you go to school? — By bike.", "How"), ("( ) ( ) pens do you have? — Three.", "How many"), ("( ) ( ) is this bag? — It's 3,000 yen.", "How much"),
      ("( ) ( ) is your father? — He's 45.", "How old"), ("( ) ( ) is it? — It's two o'clock.", "What time"), ("( ) ( ) is it today? — It's Monday.", "What day"),
      ("( ) ( ) do you play tennis? — Twice a week.", "How often"), ("( ) ( ) is it from here to the station? — About 2 km.", "How far"),
      ("( ) ( ) did you stay there? — For a week.", "How long"), ("( ) are you doing? — I'm cooking.", "What"), ("( ) plays the piano? — Mika does.", "Who"),
      ("( ) ( ) do you like? — I like green.", "What color"), ("( ) is the weather? — It's sunny.", "How"), ("( ) is the date today? — It's May 5.", "What")]
add(5, "疑問詞", [[E(q), E(a)] for q, a in Q5])

# ---------- 6 命令文・can ----------
Q6 = [("( ) quiet.", "静かにしなさい", "Be"), ("( ) run here.", "ここで走ってはいけません", "Don't"), ("( ) play tennis.", "テニスをしましょう", "Let's"),
      ("He can ( ) fast.", "swim / swims", "swim"), ("Can you ride a bike? — Yes, I ( ).", "", "can"), ("Can she cook? — No, she ( ).", "", "can't"),
      ("( ) open the window.", "窓を開けてください", "Please"), ("( ) I use your pen?", "あなたのペンを使ってもいいですか", "Can（May）"),
      ("( ) you help me?", "手伝ってくれますか", "Can（Will / Could）"), ("( ) ( ) late.", "遅れないで", "Don't be"),
      ("My sister can't ( ) French.", "speaks / speak", "speak"), ("Let's go shopping. — Yes, ( ).", "", "let's"),
      ("Ken, ( ) here.", "ケン、こっちに来て", "come"), ("Hurry up, ( ) you'll be late.", "急ぎなさい、さもないと遅れますよ", "or"),
      ("He ( ) ( ) well.", "彼は上手に歌えます", "can sing")]
add(6, "命令文と can", [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q6])

# ---------- 7 ing 形 ----------
cand = V[:]
random.shuffle(cand)
add(7, "ing 形", [[f"ing 形に：{E(v[0])}", E(v[2])] for v in cand[:30]])

# ---------- 8 過去形 ----------
irr = [v for v in V if v[0] in IRREG_PAST]
reg = [v for v in V if v[0] not in IRREG_PAST and v[0] != "die"]
random.shuffle(irr); random.shuffle(reg)
items = [[f"過去形に：{E(v[0])}", E(v[3])] for v in (irr[:26] + reg[:14])]
PRON_D = [("watched", "/t/"), ("stopped", "/t/"), ("liked", "/t/"), ("helped", "/t/"), ("walked", "/t/"), ("played", "/d/"), ("lived", "/d/"),
          ("opened", "/d/"), ("cleaned", "/d/"), ("studied", "/d/"), ("visited", "/id/"), ("wanted", "/id/"), ("needed", "/id/"), ("waited", "/id/")]
items += [[f"{E(w)} の ed の発音は /t/・/d/・/id/ のどれ？", a] for w, a in PRON_D]
WW = [("I", "was"), ("You", "were"), ("He", "was"), ("They", "were"), ("My mother", "was"), ("We", "were"), ("The books", "were"), ("It", "was")]
items += [[E(f"{s} ( ) busy yesterday."), E(w)] for s, w in WW]
add(8, "過去形・was / were", items)

# ---------- 9 未来 ----------
Q9 = [("It ( ) be rainy tomorrow.", "", "will"), ("I'm ( ) ( ) visit Kyoto next week.", "", "going to"), ("( ) you be free tomorrow? — Yes, I will.", "", "Will"),
      ("Are you going to play soccer? — No, I'm ( ).", "", "not"), ("He ( ) come.", "来ないだろう（1語）", "won't"), ("I ( ) get it.", "（電話が鳴って）私が出ます", "'ll（will）"),
      ("It's ( ) ( ) rain.", "（黒い雲を見て）雨が降りそうだ", "going to"), ("( ) I carry your bag?", "バッグを運びましょうか", "Shall"),
      ("( ) we dance?", "いっしょに踊りましょうか", "Shall"), ("( ) you open the door?", "ドアを開けてくれますか", "Will"),
      ("What are you going to ( ) tomorrow?", "", "do"), ("She will ( ) a nurse.", "is / be", "be"),
      ("This time tomorrow, I will ( ) flying.", "明日の今ごろは飛行機に乗っているだろう", "be"), ("The train ( ) at nine.", "時刻表の予定。leave", "leaves"),
      ("If it ( ) tomorrow, I'll stay home.", "rain", "rains")]
add(9, "未来の表現", [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q9])

# ---------- 10 助動詞 ----------
Q10 = [("She ( ) ( ) get up early.", "規則で〜しなければならない", "has to"), ("You ( ) ( ) smoke here.", "〜してはいけない", "must not"),
       ("You ( ) ( ) ( ) hurry.", "〜する必要はない", "don't have to"), ("You ( ) see a doctor.", "〜すべきだ", "should"),
       ("It ( ) snow tonight.", "〜かもしれない", "may"), ("He ( ) be tired.", "〜にちがいない", "must"), ("It ( ) be true.", "〜のはずがない", "can't"),
       ("I ( ) ( ) work yesterday.", "〜しなければならなかった", "had to"), ("You will ( ) ( ) ( ) swim.", "〜できるようになるだろう", "be able to"),
       ("( ) you help me?", "〜していただけますか（ていねい）", "Could（Would）"), ("( ) you like some tea?", "お茶はいかがですか", "Would"),
       ("I'd ( ) to go.", "〜したいのですが", "like"), ("You ( ) ( ) go now.", "〜したほうがいい", "had better"),
       ("( ) I come in?", "入ってもよろしいですか", "May"), ("Must I go? — No, you ( ) ( ) ( ).", "行かなくていい", "don't have to")]
add(10, "助動詞", [[E(q) + f"（{j}）", E(a)] for q, j, a in Q10])

# ---------- 11 不定詞・動名詞 ----------
Q11 = [("I enjoyed ( ) with friends.", "talk", "talking"), ("She finished ( ) the letter.", "write", "writing"), ("He stopped ( ) TV.", "watch", "watching"),
       ("We practice ( ) the piano every day.", "play", "playing"), ("I gave up ( ).", "smoke", "smoking"), ("Would you mind ( ) the window?", "open", "opening"),
       ("I want ( ) a doctor.", "be", "to be"), ("She hopes ( ) abroad.", "study", "to study"), ("He decided ( ) the job.", "take", "to take"),
       ("We are planning ( ) Kyoto.", "visit", "to visit"), ("He promised ( ) on time.", "come", "to come"), ("I need ( ) some milk.", "buy", "to buy"),
       ("Thank you for ( ) me.", "help", "helping"), ("He is good at ( ).", "cook", "cooking"), ("I'm sorry for ( ) late.", "be", "being"),
       ("Remember ( ) the door when you leave.", "lock：これからすること", "to lock"), ("I remember ( ) him once.", "meet：過去のこと", "meeting"),
       ("He stopped ( ) a rest.", "take：休むために立ち止まった", "to take"), ("How about ( ) shopping?", "go", "going"),
       ("Don't forget ( ) me.", "call：これからすること", "to call")]
items = [[E(q) + f"（{j}）", E(a)] for q, j, a in Q11]
U11 = [("I want to be a pilot.", "名詞的用法"), ("I have no time to watch TV.", "形容詞的用法"), ("He went to the park to play tennis.", "副詞的用法（目的）"),
       ("I was surprised to hear the news.", "副詞的用法（感情の原因）"), ("To read books is fun.", "名詞的用法"), ("Give me something to drink.", "形容詞的用法")]
items += [[f"不定詞の用法は？ {E(q)}", a] for q, a in U11]
items += [[E(q) + f"（{j}）", E(a)] for q, j, a in [("( ) to swim", "泳ぎ方", "how"), ("( ) to do", "何をすべきか", "what"), ("It is easy ( ) me to cook.", "", "for"),
                                                   ("I want you ( ) come.", "", "to"), ("This box is ( ) heavy to carry.", "重すぎて運べない", "too"),
                                                   ("He is old ( ) to drive.", "運転できる年齢だ", "enough")]]
add(11, "不定詞と動名詞", items)

# ---------- 12 比較 ----------
CMP = [l.split("|") for l in """tall|taller|tallest
long|longer|longest
old|older|oldest
young|younger|youngest
big|bigger|biggest
hot|hotter|hottest
large|larger|largest
nice|nicer|nicest
easy|easier|easiest
happy|happier|happiest
busy|busier|busiest
early|earlier|earliest
heavy|heavier|heaviest
beautiful|more beautiful|most beautiful
interesting|more interesting|most interesting
difficult|more difficult|most difficult
important|more important|most important
popular|more popular|most popular
famous|more famous|most famous
useful|more useful|most useful
expensive|more expensive|most expensive
good|better|best
well|better|best
bad|worse|worst
many|more|most
much|more|most
little|less|least
fast|faster|fastest
hard|harder|hardest
thin|thinner|thinnest
wide|wider|widest
slowly|more slowly|most slowly""".splitlines()]
add(12, "比較級と最上級", [[f"比較級・最上級に：{E(a)}", E(f"{b} – {c}")] for a, b, c in CMP])

# ---------- 13 受け身 ----------
cand = [v for v in V if v[0] in IRREG_PAST]
random.shuffle(cand)
items = [[f"過去分詞に：{E(v[0])}", E(v[4])] for v in cand[:30]]
Q13 = [("This room ( ) cleaned every day.", "", "is"), ("These pictures ( ) taken by Ken.", "過去", "were"), ("The window was ( ) by Tom.", "break", "broken"),
       ("Is French ( ) in Canada?", "speak", "spoken"), ("The song is loved ( ) young people.", "", "by"), ("He is known ( ) everyone.", "", "to"),
       ("The table is made ( ) wood.", "", "of"), ("Wine is made ( ) grapes.", "", "from"), ("I'm interested ( ) music.", "", "in"),
       ("The letter will ( ) sent tomorrow.", "", "be")]
items += [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q13]
add(13, "過去分詞と受け身", items)

# ---------- 14 現在完了 ----------
Q14 = [("I have lived here ( ) five years.", "", "for"), ("She has been busy ( ) last week.", "", "since"), ("Have you ( ) been to Hokkaido?", "", "ever"),
       ("I have ( ) seen a panda.", "一度もない", "never"), ("He has ( ) arrived.", "ちょうど", "just"), ("I have ( ) finished my homework.", "もう", "already"),
       ("Have you cleaned your room ( )?", "もう", "yet"), ("I haven't eaten lunch ( ).", "まだ", "yet"),
       ("( ) ( ) have you known him? — For ten years.", "", "How long"), ("( ) ( ) times have you visited Kyoto? — Three times.", "", "How many"),
       ("I ( ) him since I was a child.", "know", "have known"), ("She has ( ) to Paris.", "go：行ってしまった", "gone"),
       ("I have ( ) to Paris twice.", "be", "been"), ("It has been ( ) since morning.", "rain", "raining"),
       ("Have you finished it? — No, ( ) ( ).", "まだです", "not yet"), ("I ( ) my key yesterday.", "lose", "lost"),
       ("When ( ) you buy that bag?", "", "did"), ("He has ( ) three books.", "write", "written"), ("We have been friends ( ) 2015.", "", "since"),
       ("Has she ever ( ) Mt. Fuji?", "see", "seen")]
add(14, "現在完了", [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q14])

# ---------- 15 文型と接続詞 ----------
TOFOR = [("give", "gave", "to"), ("show", "showed", "to"), ("send", "sent", "to"), ("tell", "told", "to"), ("teach", "taught", "to"), ("lend", "lent", "to"),
         ("buy", "bought", "for"), ("make", "made", "for"), ("cook", "cooked", "for"), ("get", "got", "for"), ("find", "found", "for"), ("choose", "chose", "for")]
items = [[E(f"He {p} a book ( ) me.") + "（to か for）", E(tf)] for _, p, tf in TOFOR]
items[3][0] = E("He told the story ( ) me.") + "（to か for）"
items[4][0] = E("He taught English ( ) me.") + "（to か for）"
items[5][0] = E("He lent a book ( ) me.") + "（to か for）"
items[7][0] = E("He made a cake ( ) me.") + "（to か for）"
items[8][0] = E("He cooked dinner ( ) me.") + "（to か for）"
items[9][0] = E("He got a ticket ( ) me.") + "（to か for）"
Q15 = [("You look ( ).", "happy / happily", "happy"), ("That sounds ( ).", "great / greatly", "great"), ("The news made me ( ).", "sad / sadly", "sad"),
       ("We call our dog ( ).", "ポチ", "Pochi"), ("I think ( ) he is kind.", "", "that"), ("I stayed home ( ) I was sick.", "", "because"),
       ("When he ( ), I'll tell him.", "come", "comes"), ("Hurry up, ( ) you'll miss the bus.", "", "or")]
items += [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q15]
add(15, "文型と接続詞", items)

# ---------- 16 分詞・関係代名詞 ----------
Q16 = [("I have a friend ( ) lives in Paris.", "", "who（that）"), ("This is the book ( ) I bought yesterday.", "", "which（that）／省略可"),
       ("Look at the boy ( ) under the tree.", "sleep", "sleeping"), ("This is a letter ( ) in English.", "write", "written"),
       ("The man ( ) is talking with Ken is my uncle.", "", "who（that）"), ("I saw a dog ( ) had long ears.", "", "which（that）"),
       ("The girl ( ) hair is long is Mika.", "", "whose"), ("This is the best movie ( ) I have ever seen.", "", "that"),
       ("Do you know the man ( ) to Tom?", "talk", "talking"), ("I like the cake ( ) my mother made.", "", "which（that）／省略可"),
       ("The language ( ) in Brazil is Portuguese.", "speak", "spoken"), ("He is a singer ( ) everyone knows.", "", "who(m)（that）／省略可"),
       ("a ( ) bird", "sing", "singing"), ("a ( ) window", "break：割れた", "broken"), ("The people ( ) live here are kind.", "", "who（that）")]
add(16, "分詞と関係代名詞", [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q16])

# ---------- 17 ----------
Q17 = [("I don't know where he ( ).", "live", "lives"), ("Do you know what this ( )?", "be", "is"), ("Tell me when you ( ) here.", "come の過去", "came"),
       ("I wonder ( ) he will come.", "〜かどうか", "if（whether）"), ("If I ( ) a bird, I could fly.", "be", "were"), ("If I ( ) money, I would buy it.", "have", "had"),
       ("I wish I ( ) swim.", "泳げたらいいのに", "could"), ("I wish I ( ) a brother.", "have", "had"), ("If I were you, I ( ) not do that.", "", "would"),
       ("My mother made me ( ) my room.", "clean", "clean"), ("Let me ( ) myself.", "introduce", "introduce"), ("Do you know who ( ) this picture?", "draw の過去", "drew")]
add(17, "間接疑問と仮定法", [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in Q17])

# ---------- 18 ----------
Q18 = [("The baby is sleeping.", "SV"), ("She looks young.", "SVC"), ("I bought a new bag.", "SVO"), ("He told me the story.", "SVOO"),
       ("We named the cat Tama.", "SVOC"), ("My father works in a bank.", "SV（in a bank は M）"), ("The story sounds strange.", "SVC"),
       ("She made me a dress.", "SVOO"), ("The song made me happy.", "SVOC"), ("There are three books on the desk.", "SV"),
       ("I found the box empty.", "SVOC"), ("He became a famous singer.", "SVC")]
items = [[f"文型は？ {E(q)}", a] for q, a in Q18]
items += [[f"前置詞は必要？ {E(q)}", a] for q, a in [("discuss ( ) the plan", "不要"), ("marry ( ) her", "不要"), ("graduate ( ) college", E("from")), ("apologize ( ) him", E("to"))]]
add(18, "5文型と品詞", items)

def fillq(no, title, rows):
    add(no, title, [[E(q) + (f"（{j}）" if j else ""), E(a)] for q, j, a in rows])

fillq(19, "時制", [("Water ( ) at 0℃.", "freeze", "freezes"), ("When I arrived, the movie ( ).", "already, start", "had already started"),
                   ("I ( ) here for ten years by next year.", "live", "will have lived"), ("He said that he ( ) hungry.", "be", "was"),
                   ("The teacher said that the earth ( ) around the sun.", "go", "goes"), ("Look! The bus ( ).", "come", "is coming"),
                   ("I ( ) a book when he called.", "read", "was reading"), ("She ( ) sick since last Monday.", "be", "has been"),
                   ("I lost the pen my father ( ) me.", "give", "had given"), ("This time tomorrow I ( ) to London.", "fly", "will be flying"),
                   ("I'll call you when I ( ) home.", "get", "get"), ("I ( ) the movie last week.", "see", "saw")])
fillq(20, "助動詞の発展", [("He ( ) ( ) missed the train.", "〜したにちがいない", "must have"), ("She ( ) ( ) said so.", "〜したはずがない", "can't have"),
                         ("It ( ) ( ) rained last night.", "〜したかもしれない", "may（might）have"), ("You ( ) ( ) studied harder.", "〜すべきだったのに", "should have"),
                         ("You ( ) ( ) come.", "〜する必要はなかったのに", "needn't have"), ("There ( ) ( ) be a tree here.", "以前は〜があった", "used to"),
                         ("I'm ( ) ( ) getting up early.", "〜に慣れている", "used to"), ("You ( ) ( ) not eat too much.", "〜しないほうがいい", "had better"),
                         ("I would ( ) stay home than go out.", "", "rather"), ("I cannot ( ) laughing.", "笑わずにはいられない", "help"),
                         ("He suggested that she ( ) home.", "go", "(should) go")])
fillq(21, "準動詞の発展", [("The game was ( ).", "exciting / excited", "exciting"), ("I was ( ).", "exciting / excited", "excited"),
                         ("The movie was ( ).", "boring / bored", "boring"), ("( ) along the street, I met Ken.", "walk", "Walking"),
                         ("( ) what to say, I kept silent.", "know の否定", "Not knowing"), ("( ) his homework, he went out.", "finish：完了形", "Having finished"),
                         ("( ) in easy English, the book is popular.", "write", "(Being) Written"), ("She sat with her legs ( ).", "cross", "crossed"),
                         ("( ) speaking, he is right.", "一般的に言えば", "Generally"), ("I'm looking forward to ( ) you.", "see", "seeing"),
                         ("This book is worth ( ).", "read", "reading"), ("He seems to ( ) ill last week.", "be", "have been")])
fillq(22, "関係詞の発展", [("This is the house ( ) I was born.", "", "where"), ("I remember the day ( ) we met.", "", "when"),
                         ("That is the reason ( ) he was angry.", "", "why"), ("This is ( ) he solved it.", "方法", "how"),
                         ("( ) he said is true.", "", "What"), ("This is the town ( ) I visited last year.", "", "which（that）"),
                         ("He said nothing, ( ) made her angry.", "", "which"), ("( ) comes first will win.", "だれでも", "Whoever"),
                         ("( ) happens, I'll be with you.", "何が起きても", "Whatever"), ("( ) tired you are, you must finish it.", "どんなに", "However"),
                         ("This is the house in ( ) he lives.", "", "which"), ("She is no longer ( ) she used to be.", "昔の彼女", "what")])
fillq(23, "仮定法の発展", [("If I ( ) rich, I would travel.", "be", "were"), ("If I had known, I ( ) you.", "tell", "would have told"),
                         ("If you ( ) earlier, you would have caught it.", "leave", "had left"), ("I wish I ( ) harder when I was young.", "study", "had studied"),
                         ("He talks as if he ( ) a king.", "be", "were"), ("( ) water, we could not live.", "〜がなければ：1語", "Without"),
                         ("( ) I you, I would go.", "倒置", "Were"), ("( ) I known, I would have come.", "倒置", "Had"),
                         ("It's time you ( ) to bed.", "go", "went"), ("If you ( ) need help, call me.", "万一", "should"),
                         ("If I had studied harder then, I ( ) a doctor now.", "be", "would be"), ("I took a taxi; ( ), I would have been late.", "さもなければ", "otherwise")])
fillq(24, "比較の発展", [("This room is ( ) as large as that one.", "2倍", "twice"), ("The ( ) you practice, the ( ) you play.", "", "more, better"),
                       ("It is getting ( ) and ( ).", "cold", "colder, colder"), ("He has no ( ) than 100 yen.", "たった100円", "more"),
                       ("She has no ( ) than ten cats.", "10匹も", "less"), ("This is superior ( ) that.", "", "to"), ("I prefer tea ( ) coffee.", "", "to"),
                       ("No other mountain in Japan is ( ) than Mt. Fuji.", "high", "higher"), ("He is not so much a singer ( ) an actor.", "", "as"),
                       ("Run as fast as ( ).", "できるだけ", "possible（you can）")])
fillq(25, "特殊構文", [("It was Ken ( ) broke the vase.", "", "that（who）"), ("Never ( ) I seen such a big fish.", "", "have"),
                     ("Little ( ) he know the truth.", "", "did"), ("I like cats. — So ( ) I.", "", "do"), ("I can't swim. — ( ) can I.", "", "Neither"),
                     ("When ( ) ( ) young, he lived in Kyoto.", "省略されている2語", "he was"), ("The rain prevented us ( ) going out.", "", "from"),
                     ("This photo reminds me ( ) my trip.", "", "of"), ("Rich people are not ( ) happy.", "いつも〜とは限らない", "always"),
                     ("Hardly had he arrived ( ) it began to rain.", "", "when（before）")])
add(26, "読解のつなぎ言葉と語の推測", [
    [E("I was tired. ( ), I kept working.") + "（それでも）", E("However（Still）")],
    [E("He studied hard. ( ), he passed the exam.") + "（その結果）", E("As a result（Therefore）")],
    [E("I like fruits, ( ) apples and oranges.") + "（〜のような：2語）", E("such as")],
    [E("She is smart. ( ), she is kind.") + "（さらに）", E("In addition（Moreover / Besides）")],
    [E("( ), the plan failed.") + "（要するに：2語）", E("In short")],
    [E("Some like summer. ( ), others like winter.") + "（一方で：4語）", E("On the other hand")],
    [f"{E('unhappy')} の意味（un＋happy）", "不幸な"], [f"{E('careless')} の意味（care＋less）", "不注意な"],
    [f"{E('reuse')} の意味（re＋use）", "再利用する"], [f"{E('useful')} の意味（use＋ful）", "役に立つ"]])
add(27, "和文英訳（解答は一例）", [[j, E(a)] for j, a in [
    ("私は毎朝7時に起きる。", "I get up at seven every morning."), ("彼女は泳ぐのが得意だ。", "She is good at swimming."),
    ("私は昨日駅で彼に会った。", "I met him at the station yesterday."), ("この本は読む価値がある。", "This book is worth reading."),
    ("宿題をするのに2時間かかった。", "It took me two hours to do my homework."), ("もし明日雨なら、家にいます。", "If it rains tomorrow, I will stay home."),
    ("私はそんなに速く走れない。", "I can't run that fast."), ("日本には四季がある。", "Japan has four seasons. (There are four seasons in Japan.)"),
    ("私は英語を話すのが楽しい。", "I enjoy speaking English."), ("彼は私が今まで会った中で一番親切な人だ。", "He is the kindest person (that) I have ever met.")]], one=True)
ACC = [("banana", "2（ba-NA-na）"), ("computer", "2（com-PU-ter）"), ("hotel", "2（ho-TEL）"), ("guitar", "2（gui-TAR）"), ("piano", "2（pi-A-no）"),
       ("volunteer", "3（vol-un-TEER）"), ("Japanese", "3（Jap-a-NESE）"), ("interesting", "1（IN-ter-est-ing）"), ("important", "2（im-POR-tant）"),
       ("engineer", "3（en-gi-NEER）"), ("museum", "2（mu-SE-um）"), ("event", "2（e-VENT）"), ("chocolate", "1（CHOC-o-late）"), ("vitamin", "1（VI-ta-min）"),
       ("idea", "2（i-DE-a）"), ("thirteen", "2（thir-TEEN）"), ("thirty", "1（THIR-ty）")]
add(28, "アクセントの位置（何音節目を強く読む？）", [[E(w), a] for w, a in ACC])

json.dump(D, open("drills.json", "w", encoding="utf-8"), ensure_ascii=False)
print({k: len(v["items"]) for k, v in D.items()}, sum(len(v["items"]) for v in D.values()))
