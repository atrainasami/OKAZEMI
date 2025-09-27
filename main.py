import streamlit as st
from datetime import datetime, time
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
st.title("仲間内スケジュール管理（開始時間・終了時間対応）")

# --- CSV ファイル ---
FILE_PATH = "schedule.csv"

if os.path.exists(FILE_PATH):
    schedule_df = pd.read_csv(FILE_PATH)
    # 不要列削除
    for col in ['to', 'event']:
        if col in schedule_df.columns:
            schedule_df.drop(columns=col, inplace=True)
else:
    schedule_df = pd.DataFrame(columns=[
        "予定日", "開始時間", "終了時間", "更新日", "概要", "詳細"
    ])

# --- 予定追加フォーム ---
with st.form("予定追加フォーム"):
    event_date = st.date_input("予定日")
    start_time = st.time_input("開始時間", value=time(9,0))
    end_time = st.time_input("終了時間", value=time(10,0))
    summary = st.text_input("概要")
    detail = st.text_area("詳細")
    submitted = st.form_submit_button("追加")
    
    if submitted:
        new_event = {
            "予定日": event_date.strftime("%Y-%m-%d"),
            "開始時間": start_time.strftime("%H:%M"),
            "終了時間": end_time.strftime("%H:%M"),
            "更新日": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "概要": summary,
            "詳細": detail
        }
        schedule_df = pd.concat([schedule_df, pd.DataFrame([new_event])], ignore_index=True)
        schedule_df.to_csv(FILE_PATH, index=False)

        # --- SNS用テキスト化（更新日以外の列を結合） ---
        sns_text = "\n".join([f"{col}: {new_event[col]}" for col in new_event if col != "更新日"])
        st.success("予定を追加しました！")
        st.text_area("SNS投稿用テキスト（コピーして使ってください）", sns_text, height=150)

# --- 編集可能 DataFrame 表示 ---
st.write("### スケジュール一覧（編集可）")
edited_df = st.data_editor(schedule_df, num_rows="dynamic")

# --- 編集後の状態で CSV 保存 ---
if st.button("変更を保存"):
    edited_df["更新日"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    edited_df.to_csv(FILE_PATH, index=False)
    st.success("変更を保存しました！")

# --- カレンダー表示 ---
if not edited_df.empty:
    # datetime型に変換
    edited_df["開始"] = pd.to_datetime(edited_df["予定日"] + " " + edited_df["開始時間"])
    edited_df["終了"] = pd.to_datetime(edited_df["予定日"] + " " + edited_df["終了時間"])
    
    fig = px.timeline(
        edited_df,
        x_start="開始",
        x_end="終了",
        y="概要",
        hover_data=["詳細", "更新日"],
        title="予定カレンダー"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
