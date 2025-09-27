import streamlit as st
from datetime import datetime
import pandas as pd
import os
import plotly.express as px

# --- パスワード認証 ---
APP_PASSWORD = st.secrets["APP_PASSWORD"]

password = st.text_input("パスワード:", type="password")
if not password:
    st.info("パスワードを入力してください")
    st.stop()
if password != APP_PASSWORD:
    st.warning("パスワードが違います")
    st.stop()

st.success("ログイン成功！")
st.title("仲間内スケジュール管理（カレンダー対応）")

# --- CSV ファイル ---
FILE_PATH = "schedule.csv"

# CSV 読み込み or 空 DataFrame 作成
if os.path.exists(FILE_PATH):
    schedule_df = pd.read_csv(FILE_PATH)
else:
    schedule_df = pd.DataFrame(columns=["予定日", "更新日", "概要", "詳細"])

# --- SNS フォーマット ---
st.sidebar.header("SNS出力フォーマット")
st.sidebar.write("使える変数: {予定日}, {更新日}, {概要}, {詳細}")
sns_format = st.sidebar.text_area(
    "フォーマットを入力してください",
    value="【新しい予定】\n{予定日} - {概要}\n{詳細}\n#予定 #スケジュール"
)

# --- 予定追加 ---
with st.form("予定追加フォーム"):
    event_date = st.date_input("予定日")
    summary = st.text_input("概要")
    detail = st.text_area("詳細")
    submitted = st.form_submit_button("追加")
    if submitted:
        new_event = {
            "予定日": event_date.strftime("%Y-%m-%d"),
            "更新日": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "概要": summary,
            "詳細": detail
        }
        schedule_df = pd.concat([schedule_df, pd.DataFrame([new_event])], ignore_index=True)
        schedule_df.to_csv(FILE_PATH, index=False)

        sns_text = sns_format.format(**new_event)
        st.success("予定を追加しました！")
        st.text_area("SNS投稿用テキスト（コピーして使ってください）", sns_text, height=100)

# --- DataFrame 編集可能表示 ---
st.write("### スケジュール一覧（編集可）")
edited_df = st.data_editor(schedule_df, num_rows="dynamic")

i
