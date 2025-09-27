import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- パスワード判定 ---
# Cloud 上の Secret だけを参照
APP_PASSWORD = st.secrets["APP_PASSWORD"]

password = st.text_input("パスワード:", type="password")

# 入力が空のときは待機
if not password:
    st.info("パスワードを入力してください")
    st.stop()

# パスワードが違う場合
if password != APP_PASSWORD:
    st.warning("パスワードが違います")
    st.stop()

# ログイン成功
st.success("ログイン成功！")
st.title("仲間内スケジュール管理")

# --- CSV 保存用ファイル ---
FILE_PATH = "schedule.csv"

# ファイルがあれば読み込み、なければ空の DataFrame を作成
if os.path.exists(FILE_PATH):
    schedule_df = pd.read_csv(FILE_PATH)
else:
    schedule_df = pd.DataFrame(columns=["time", "event"])

# --- SNS 出力フォーマット設定 ---
st.sidebar.header("SNS出力フォーマット")
st.sidebar.write("使える変数: {time}, {event}")
sns_format = st.sidebar.text_area(
    "フォーマットを入力してください",
    value="【新しい予定】\n{time} - {event}\n#予定 #スケジュール"
)

# --- 予定入力 ---
event = st.text_input("予定を入力してください")
if st.button("追加") and event.strip():  # 空白は追加しない
    new_event = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "event": event
    }
    schedule_df = pd.concat([schedule_df, pd.DataFrame([new_event])], ignore_index=True)
    schedule_df.to_csv(FILE_PATH, index=False)  # ローカルに保存

    sns_text = sns_format.format(**new_event)
    st.success("予定を追加しました！")
    st.text_area("SNS投稿用テキスト（コピーして使ってください）", sns_text, height=100)

# --- 予定一覧表示 ---
if not schedule_df.empty:
    st.write("### スケジュール一覧")
    st.table(schedule_df)
