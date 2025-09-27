import streamlit as st
from datetime import datetime
import pandas as pd
import os

# --- パスワード判定 ---
APP_PASSWORD = st.secrets["APP_PASSWORD"]

password = st.text_input("パスワード:", type="password")
if not password:
    st.info("パスワードを入力してください")
    st.stop()
if password != APP_PASSWORD:
    st.warning("パスワードが違います")
    st.stop()

st.success("ログイン成功！")
st.title("仲間内スケジュール管理")

# --- CSV ファイルパス ---
FILE_PATH = "schedule.csv"

# CSV 読み込み or 空 DataFrame 作成
if os.path.exists(FILE_PATH):
    schedule_df = pd.read_csv(FILE_PATH)
else:
    schedule_df = pd.DataFrame(columns=["time", "event"])

# --- SNS フォーマット設定 ---
st.sidebar.header("SNS出力フォーマット")
st.sidebar.write("使える変数: {time}, {event}")
sns_format = st.sidebar.text_area(
    "フォーマットを入力してください",
    value="【新しい予定】\n{time} - {event}\n#予定 #スケジュール"
)

# --- 予定追加 ---
event = st.text_input("予定を入力してください")
if st.button("追加") and event.strip():
    new_event = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "event": event
    }
    schedule_df = pd.concat([schedule_df, pd.DataFrame([new_event])], ignore_index=True)
    schedule_df.to_csv(FILE_PATH, index=False)

    sns_text = sns_format.format(**new_event)
    st.success("予定を追加しました！")
    st.text_area("SNS投稿用テキスト（コピーして使ってください）", sns_text, height=100)

# --- DataFrame 編集可能に表示 ---
st.write("### スケジュール一覧（編集可）")
edited_df = st.data_editor(schedule_df, num_rows="dynamic")

# 編集結果を CSV に反映
if st.button("変更を保存"):
    edited_df.to_csv(FILE_PATH, index=False)
    st.success("変更を保存しました！")
