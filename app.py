import streamlit as st
import pandas as pd
import numpy as np

# 偏差値 → ランク変換
def zscore_to_rank(z):
    if z >= 61:
        return 'S'
    elif z >= 54:
        return 'A'
    elif z >= 47:
        return 'B'
    elif z >= 41:
        return 'C'
    else:
        return 'D'

# 勝率から偏差値ランクに変換
def convert_to_rank(scores):
    scores = np.array(scores, dtype=float)
    scores = np.clip(scores, 3.0, None)  # 下限を3.0に固定
    mean = scores.mean()
    std = 1.35
    zscores = (scores - mean) / std * 10 + 50
    ranks = [zscore_to_rank(z) for z in zscores]
    return ''.join(ranks)  # "-"なし

st.title("競艇順位予想")
st.header("コース順の勝率を入力してね")

# 1～6コースの勝率を入力
col1, col2, col3, col4, col5, col6 = st.columns(6)
scores = [
    col1.number_input("1コース", min_value=0.0, max_value=20.0, step=0.3, value=5.0),
    col2.number_input("2コース", min_value=0.0, max_value=20.0, step=0.3, value=5.0),
    col3.number_input("3コース", min_value=0.0, max_value=20.0, step=0.3, value=5.0),
    col4.number_input("4コース", min_value=0.0, max_value=20.0, step=0.3, value=5.0),
    col5.number_input("5コース", min_value=0.0, max_value=20.0, step=0.3, value=5.0),
    col6.number_input("6コース", min_value=0.0, max_value=20.0, step=0.3, value=5.0),
]


# 変換ボタン
if st.button("ランク計算"):
    rank_str = convert_to_rank(scores)
    st.success(f"計算結果: {rank_str}")

    # CSVから該当組み合わせを検索
    df = pd.read_csv("ranked_patterns_total.csv", encoding="utf-8-sig")
    result = df[df["偏差rank"] == rank_str]
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("該当する組み合わせは見つかりませんでした。")
