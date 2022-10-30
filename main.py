import pandas as pd
import json

from googleapiclient.discovery import build
import streamlit as st


#表示するDataFrameの行数を500までにする
pd.set_option("display.max_rows", 500)

#APIキーがまとめられているjsonファイルを読み込む
with open("secret.json") as f:
    keys = json.load(f)

#youtubeの動画検索システムをつかい、検索結果をjson形式で取得する関数
def youtube_request(youtube, query, target, page_token=None):
    response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=50,
            pageToken=page_token,
            order=target,
            type="video"
        ).execute()
    return response

#入力したクエリから動画を検索し、簡易的な情報をDataFrameにまとめる関数
def search_function(keys, key, recursion_count, target, default_df, query, page_token=None):
    youtube = set_developerkey(keys, key)
    response = youtube_request(youtube, query, target, page_token)
    

    if "nextPageToken" in response: next_page = response["nextPageToken"]
    videos_search = response["items"]
    video_ids = [data["id"]["videoId"] for data in videos_search]

    video_list = []
    for data in videos_search:
        data_dict = {}
        data_dict["video_id"] = data["id"]["videoId"]
        data_dict["title"] = data["snippet"]["title"]
        data_dict["channel_id"] = data["snippet"]["channelId"]
        data_dict["channel_title"] = data["snippet"]["channelTitle"]
        video_list.append(data_dict)

    df_video = pd.DataFrame(video_list)
    df_video = df_formatting(df_video, "index")
    video_ids = list(df_video["video_id"])
    df_video_data = video_data(youtube, video_ids)
    results = df_formatting(create_table(df_video, df_video_data), "index")
    results = vertical_dataframe_join(default_df, results)

    if recursion_count <=0: return results
    else: return search_function(keys, key, recursion_count-1, target, results, query, next_page)

#search_functionで得た動画IDの配列から動画IDに対応した動画の各情報を取得し、DataFrameにまとめる関数
def video_data(youtube, video_ids):
    response = youtube.videos().list(
        id=",".join(video_ids),
        part="id,snippet,statistics"
    ).execute()

    video_items = response["items"]

    video_data = []
    for item in video_items:
        video_item = {}
        video_item["view_count"] = int(item["statistics"]["viewCount"])
        try:
            video_item["like_count"] =int(item["statistics"]["likeCount"])
        except:
            video_item["like_count"] = 0

        if video_item["like_count"] > 0:
            video_item["point"] = round(int(item["statistics"]["likeCount"])/int(item["statistics"]["viewCount"])*10**4,1)
        else:
            video_item["point"] = 0
        try:
            video_item["comment_count"] = int(item["statistics"]["commentCount"])
        except:
            video_item["comment_count"] = 0
        video_item["video_id"] = item["id"]
        video_data.append(video_item) 

    df_video_data = pd.DataFrame(video_data)
    return df_video_data

#search_functionとvideo_dataで得たDataFrameをvideo_id列で結合しcolumnsを並べ替える関数
def create_table(df_video_list, df_video_data):
    df_results = pd.merge(left=df_video_data, right=df_video_list, on="video_id")
    df_results = df_results.loc[:,
        ["video_id","title","view_count","like_count","point","comment_count","channel_id","channel_title"]]
    df_results = df_results.sort_values("point", ascending=False)
    return df_results

#DataFrameのindexを振りなおす関数
def df_formatting(df, index):
    df = df.reset_index()
    del df[f"{index}"]
    return df

#youtubeの機能を使うのにあたって必要なAPIキーなどの情報の設定を行う関数
def set_developerkey(keys, key):
    DEVELOPER_KEY = keys["KEY"][key]
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)
    return youtube

#DataFrameを縦に結合する関数
def vertical_dataframe_join(df1, df2):
    return pd.concat([df1, df2])

#参照したい動画IDを入力して動画を表示する関数
def st_video_show(video_id):
    video_url = f"https://www.youtube.com/watch?v=" + video_id
    video_erea = st.empty()
    video_erea.video(video_url)

#並べ替えクエリの設定
target_dict = {
    "新しい動画":"date",
    "高評価が多い動画":"rating",
    "関連した動画":"relevance",
    "高再生数の動画":"viewCount"
}
#以下でstreamlit上での画面構築やmain処理
st.title("Youtube 高評価の多い動画検索")
st.write("動画一覧")
query = st.sidebar.text_input("クエリを入力してください")
target_videos = st.sidebar.selectbox(
    "取得したい動画の特徴を選択してください",
    ["新しい動画","高評価が多い動画","関連した動画","高再生数の動画"]
)
num_of_videos = st.sidebar.selectbox(
    "取得したい動画の数を選択してください",
    [i*50 for i in range(1,10)]
)

df_columns = ["video_id", "title", "view_count", "like_count", "point", "comment_count", "channel_id", "channel_title"]
default_df = pd.DataFrame(data=None, columns=df_columns)
response = search_function(keys, 0, num_of_videos/50-1, target_dict[target_videos], default_df, query).sort_values("point", ascending=False)
sorted_df = df_formatting(response, "index")

st.dataframe(sorted_df)

video_id = st.text_input("以下に動画IDを入力すると動画が表示されます")
st_video_show(video_id)