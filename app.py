from datetime import datetime
import pandas as pd
import streamlit as st

# ページ全体のレイアウト設定
st.set_page_config(
    page_title="Trend Analytics Dashboard", page_icon="🔥", layout="wide"
)

st.title("🔥 リアルタイム・トレンド分析ダッシュボード")
st.markdown("GitHub Actionsで自動収集したトレンドデータを可視化します。")


# CSVデータを読み込む関数
@st.cache_data
def load_data():
  try:
    df = pd.read_csv("trend_log.csv")
    return df
  except FileNotFoundError:
    return None


df = load_data()

if df is not None and not df.empty:
  # サイドバーの設定
  st.sidebar.header("⚙️ 表示設定")
  top_n = st.sidebar.slider("ランキングの表示件数", min_value=5, max_value=30, value=10)

  # 画面を2カラムに分割
  col1, col2 = st.columns(2)

  with col1:
    st.subheader(f"📊 上位キーワード 出現頻度（Top {top_n}）")
    # キーワードごとの出現回数を集計
    keyword_counts = df["keyword"].value_counts().reset_index()
    keyword_counts.columns = ["keyword", "count"]

    # 棒グラフの表示
    st.bar_chart(
        keyword_counts.set_index("keyword").head(top_n), color="#ff4b4b"
    )

  with col2:
    st.subheader("🕒 最近収集されたログの推移")
    # 日時ごとの取得ワード数などをサマリー表示
    time_counts = df["datetime"].value_counts().sort_index()
    st.line_chart(time_counts)

  # 下部に生データ一覧を表示
  st.markdown("---")
  st.subheader("📋 収集データ一覧（Raw Data）")
  st.dataframe(df, use_container_width=True)

else:
  st.warning(
      "⚠️ `trend_log.csv` が見つからないか、データが空です。データの蓄積をお待ち"
      "ください。"
  )
