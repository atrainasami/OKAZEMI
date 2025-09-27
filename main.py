import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- ログイン処理（簡易版） ---
password = st.text_input("パスワード:", type="password")
if password != st.secrets["APP_PASSWORD"]:
    st.stop()

st.title("仲間内スケジュール管理")

# --- 保存用ファイル ---
FILE_PATH = "schedule.csv"

# ファイルがあれば読み込み、なければ空のDataFrameを用意
if os.path.exists(FILE_PATH):
    schedule_df = pd.read_csv(FILE_PATH)
else:
    schedule_df = pd.DataFrame(columns=["time", "event"])

# --- SNSフォーマット設定 ---
st.sidebar.header("SNS出力フォーマット")
st.sidebar.write("使える変数: {time}, {event}")
sns_format = st.sidebar.text_area(
    "フォーマットを入力してください",
    value="【新しい予定】\n{time} - {event}\n#予定 #スケジュール"
)

# --- 予定入力 ---
event = st.text_input("予定を入力してください")
if st.button("追加"):
    new_event = {"event": event, "time": datetime.now().strftime("%Y-%m-%d %H:%M")}
    schedule_df = pd.concat([schedule_df, pd.DataFrame([new_event])], ignore_index=True)
    schedule_df.to_csv(FILE_PATH, index=False)

    sns_text = sns_format.format(**new_event)
    st.success("予定を追加しました！")
    st.text_area("SNS投稿用テキスト（コピーして使ってください）", sns_text, height=100)

# --- 予定一覧表示 ---
if not schedule_df.empty:
    st.write("### スケジュール一覧")
    st.table(schedule_df)
