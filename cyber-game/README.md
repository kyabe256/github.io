# 総監・翼　日米統合サイバー捜査ファイル

「日米統合サイバー捜査総監・翼」の世界（`cyber/`）の第1章「身代金の章」を、推理アドベンチャーゲームにしたもの。FILE 001〜010。

- 遊ぶ：`index.html` を開く（`voice-001.mp3`〜`voice-010.mp3` を同じフォルダに置く）。
- 遊び方：調べる／話す／移動／視点と、追及（証拠・推理・視点・観察）。事件ごとに、視点の仲間が変わる。
- 事件の台本：`src/cases/001.txt`〜`010.txt`。登場人物、証拠、場所、追及、話の流れ、台詞が1つのファイルに入っている。
- 作り直す：`src/` を編集して `node src/check.js`（整合チェック）、`python3 src/voices_vv.py build`（声）、`python3 src/build.py`（ページ）。

## クレジット
声は VOICEVOX で作った（`src/voices_vv.py`。VOICEVOX ENGINE を手元で動かして使う）。

VOICEVOX:玄野武宏、VOICEVOX:白上虎太郎、VOICEVOX:青山龍星、VOICEVOX:剣崎雌雄、VOICEVOX:雀松朱司、VOICEVOX:麒ヶ島宗麟、VOICEVOX:ちび式じい、VOICEVOX:栗田まろん、VOICEVOX:黒沢冴白、VOICEVOX:離途、VOICEVOX:満別花丸、VOICEVOX:†聖騎士 紅桜†、VOICEVOX:No.7、VOICEVOX:春日部つむぎ、VOICEVOX:波音リツ、VOICEVOX:後鬼、VOICEVOX:冥鳴ひまり、VOICEVOX:九州そら、VOICEVOX:東北イタコ、VOICEVOX:東北ずん子、VOICEVOX:WhiteCUL、VOICEVOX:中部つるぎ、VOICEVOX:琴詠ニア、VOICEVOX:四国めたん、VOICEVOX:雨晴はう

- No.7 は非商用での利用。このゲームは無料で、お金を取らない。
- `src/voices.py` は、VOICEVOX が使えない時のための古い作り方（Open JTalk）。いまの声には使っていない。
- 物語、人物、団体は架空。
