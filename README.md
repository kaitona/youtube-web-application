# youtube-web-application

これはYoutube Data APIによりYoutubeで検索した動画の情報を表形式にして表示することができるアプリケーションです。

# 動作例

# 機能

・Youtubeで動画検索したときには表示されない高評価やコメント数などもまとめてみることが可能

・Youtubeでの再生数順や関連度順のソート方法に再生数と高評価数から割り出した評価ポイントを設定することで再生数が低くても

 　高評価な動画(隠れた良い動画)が検索可能

・Youtube Data APIでは一度に最大50件しか動画を取得できないが、特定の処理により最大450件取得可能

# requirement

streamlit==1.5.0

google-api-python-client==2.38.0

# ライブラリのインストール方法

'''
pip install streamlit==1.5.0
pip install google-api-client=2.38.0
'''

# 使用方法
次のURLでアプリを起動できます
https://kaitona-youtube-web-application-main-a73fcg.streamlit.app

# 注意事項

使用時にHttpErrorというものが出てくることがありますが、それは一日のYoutube Data APIの利用上限に達したことを表します。翌日以降お試しください。

# 作成者情報

作成者:kaitona
