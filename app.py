import streamlit as st
import pandas as pd
import numpy as np

# 入力を消すボタン
if st.button("入力をクリア"):
    for key in ["score1", "score2", "score3", "score4", "score5", "score6"]:
        st.session_state[key] = ""  # 空に戻す
    st.rerun()  # 画面をリロードして反映

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

# 1～6コースの勝率を入力
col1, col2, col3, col4, col5, col6 = st.columns(6)

def blank_number_input(col, label, min_val=0.0, max_val=10.0, step=0.2):
    txt = col.text_input(label, "")  # 初期値ブランク
    if txt.strip() == "":
        return 0.0  # 空白は0扱い
    try:
        val = float(txt)
        # 範囲チェック
        if val < min_val or val > max_val:
            st.warning(f"{label} は {min_val}～{max_val} の範囲で入力してください")
            return 0.0
        return round(val / step) * step  # stepに丸める
    except ValueError:
        st.warning(f"{label} は数値を入力してください")
        return 0.0

scores = [
    blank_number_input(col1, "1コース"),
    blank_number_input(col2, "2コース"),
    blank_number_input(col3, "3コース"),
    blank_number_input(col4, "4コース"),
    blank_number_input(col5, "5コース"),
    blank_number_input(col6, "6コース"),
]

#st.write("入力結果:", scores)

st.title("競艇着順予想")
st.header("コース別の勝率を入力してね")

# 変換ボタン
if st.button("予想"):
    rank_str = convert_to_rank(scores)

    # CSVから該当組み合わせを検索
    df = pd.read_csv("ranked_patterns_total.csv", encoding="utf-8-sig")
    result = df[df["偏差rank"] == rank_str]
    if not result.empty:
        st.dataframe(result)
    else:
        st.warning("該当する組み合わせは見つかりませんでした。")
