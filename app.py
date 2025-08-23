import streamlit as st
import pandas as pd

# CSVを読み込み
@st.cache_data
def load_data():
    return pd.read_csv("ranked_patterns_total.csv", encoding="utf-8-sig")

df = load_data()

st.title("ランク別 着順検索アプリ")
st.write("例: SABCDD, AABCDD などを入力して検索してください")

# 入力ボックス
query = st.text_input("組み合わせを入力", "")

if query:
    query = query.strip().upper()  # 大文字に統一
    result = df[df["組み合わせ"] == query]

    if not result.empty:
        st.success(f"結果: {query}")
        st.dataframe(result)
    else:
        st.warning("該当する組み合わせは見つかりませんでした。")

# 全体データを表示するチェックボックス
if st.checkbox("全データを表示"):
    st.dataframe(df)
