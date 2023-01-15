# youtube-web-application

これはYoutube Data APIによりYoutubeで検索した動画の情報を表形式にして表示することができるアプリケーションです。

# 動作例

以下が動作例になります。

![動作例.gif](./動作例.gif)

# 機能

・Youtubeで動画検索したときには表示されない高評価やコメント数なども表形式でまとめてみることができます。

# 使用ライブラリ

streamlit==1.5.0

google-api-python-client==2.38.0

# ライブラリのインストール方法

```bash
pip install streamlit==1.5.0
pip install google-api-client=2.38.0
```

# 使用方法
次のURLでアプリを起動できます
https://kaitona-youtube-web-application-main-a73fcg.streamlit.app

# 工夫した点

・Youtube Data APIでは一度に最大50件しか動画を取得できないが、特定の処理により最大450件取得できるようにしました。

・Youtubeでの再生数順や関連度順のソート方法に再生数と高評価数から割り出した評価ポイントを設定することで再生数が低くても

 　高評価な動画(隠れた良い動画)が検索可能にしました。

# 開発の際に苦労した点

・Youtube Data APIキーには一日の利用制限があったため、プロトタイプなどを開発している際にAPIリクエストで無限ループなどが

　 起きてしまったり、無駄なリクエストを送ると利用上限に達してしまうことがありました。そういった問題を回避するために、
  
  　一回のリクエストではあまり大量のリクエストをしないことや、APIキーを複数利用するといった方法をとりました。

# 注意事項

使用時にHttpErrorというものが出てくることがありますが、それは一日のYoutube Data APIの利用上限に達したことを表します。翌日以降お試しください。

# 作成者情報

作成者:kaitona
