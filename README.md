# Vocabby

Nov20, 2021

うちの実験的web記事追加：[Vocabby: 我が家のSlack bot、辞書を引いてGoogle Sheetsに書き込んでくれます。](https://makeintoshape.com/vocabby/)



Oxford Dictionary APIを使ってSlack botに単語の意味と例文を調べてもらいます。結果はGoogle sheetsに書き込まれます。



Dec12, 2021

`readVocabbyGSheets.py`を書いて追加。`crontab`で定時に実行させるとSheetsにあるものをGoogle Homeが読み上げてくれる。python=3.7.7 (my Laptop)、3.7.3 (raspberry pi 3Bplus)で動くことを確認した。

