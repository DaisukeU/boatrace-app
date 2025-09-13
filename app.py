import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------
# 偏差値 → ランク変換
# ------------------------------
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

# ------------------------------
# Streamlitタイトル
# ------------------------------
st.title("競艇着順予想")
st.header("コース別の勝率を入力してね")

# ------------------------------
# セッションステート初期化
# ------------------------------
for i in range(1, 7):
    key = f"score{i}"
    if key not in st.session_state:
        st.session_state[key] = ""

# ------------------------------
# クリア用コールバック
# ------------------------------
def clear_inputs():
    for i in range(1, 7):
        st.session_state[f"score{i}"] = ""

# ------------------------------
# 入力欄
# ------------------------------
cols = st.columns(6)
scores = []
for i, col in enumerate(cols, start=1):
    val = col.text_input(f"{i}コース", st.session_state.get(f"score{i}", ""), key=f"score{i}")
    scores.append(val)  # 文字列のまま保持

# ------------------------------
# ボタン横並び
# ------------------------------
btn_col1, btn_col2 = st.columns([1,1])
with btn_col1:
    st.button("入力をクリア", on_click=clear_inputs)
with btn_col2:
    predict_pressed = st.button("予想")

# ------------------------------
# 予想処理
# ------------------------------
if predict_pressed:
    # 空白や不正値は0に変換
    numeric_scores = []
    for s in scores:
        try:
            numeric_scores.append(float(s))
        except (ValueError, TypeError):
            numeric_scores.append(0.0)

    # 偏差値ランクに変換
    rank_str = convert_to_rank(numeric_scores)

    # CSVから該当組み合わせを検索
    try:
        df = pd.read_csv("ranked_patterns_total.csv", encoding="utf-8-sig")
        result = df[df["偏差rank"] == rank_str]
        if not result.empty:
            st.dataframe(result)
        else:
            st.warning("該当する組み合わせは見つかりませんでした。")
    except FileNotFoundError:
        st.error("ranked_patterns_total.csv が見つかりません。")