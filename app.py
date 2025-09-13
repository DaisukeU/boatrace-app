import streamlit as st
import pandas as pd
import numpy as np

# 偏差値 → ランク変換
def zscore_to_rank(z):
    if z >= 61: return 'S'
    elif z >= 54: return 'A'
    elif z >= 47: return 'B'
    elif z >= 41: return 'C'
    else: return 'D'

def convert_to_rank(scores):
    scores = np.array(scores, dtype=float)
    scores = np.clip(scores, 3.0, None)
    mean = scores.mean()
    std = 1.35
    zscores = (scores - mean) / std * 10 + 50
    return ''.join([zscore_to_rank(z) for z in zscores])

st.title("競艇着順予想")
st.header("コース別の勝率を入力してね")

# セッションステート初期化
for i in range(1, 7):
    key = f"score{i}"
    if key not in st.session_state:
        st.session_state[key] = ""

# 入力欄
cols = st.columns(6)
scores = []
for i, col in enumerate(cols, start=1):
    val = col.text_input(f"{i}コース", st.session_state.get(f"score{i}", ""), key=f"score{i}")
    scores.append(val if val.strip() != "" else "0")  # 空白は0扱い

# 横並びボタン
btn_col1, btn_col2 = st.columns([1,1])
with btn_col1:
    clear_pressed = st.button("入力をクリア")
with btn_col2:
    predict_pressed = st.button("予想")


# クリア処理（rerun不要）
if clear_pressed:
    for i in range(1, 7):
        st.session_state[f"score{i}"] = ""  # 空白に戻す

# 予想処理
if predict_pressed:
    numeric_scores = [float(s) if s.strip() != "" else 0.0 for s in scores]
    rank_str = convert_to_rank(numeric_scores)
    try:
        df = pd.read_csv("ranked_patterns_total.csv", encoding="utf-8-sig")
        result = df[df["偏差rank"] == rank_str]
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("該当する組み合わせは見つかりませんでした。")
    except FileNotFoundError:
        st.error("ranked_patterns_total.csv が見つかりません。")
