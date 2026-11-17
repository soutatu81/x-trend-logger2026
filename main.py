from datetime import datetime
import os
from bs4 import BeautifulSoup
import pandas as pd
import requests

URL = "https://search.yahoo.co.jp/realtime"


def get_trends():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }
  try:
    response = requests.get(URL, headers=headers, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    trends = []

    # 無視したいメニューや定型文のリスト（ノイズカット用）
    ignore_words = {
        "プライバシーポリシー",
        "プライバシーセンター",
        "利用規約",
        "広告について",
        "検索サービス一覧",
        "ログイン",
        "ID新規取得",
        "ヘルプ",
        "ご意見",
        "フィードバック",
        "北海道",
        "東北",
        "関東",
        "中部",
        "近畿",
        "中国",
        "四国",
        "九州",
        "全国の運行情報（Yahoo!路線情報）",
    }

    for a in soup.select("a"):
      text = a.get_text(strip=True)
      # 文字数が2〜20文字程度で、URLやノイズワードに含まれないものだけを抽出
      if 2 <= len(text) <= 20 and not text.startswith("http"):
        if text not in ignore_words and not text.startswith("エラー"):
          if text not in [t["keyword"] for t in trends]:
            trends.append({"datetime": now, "keyword": text})

    if not trends:
      trends.append(
          {"datetime": now, "keyword": "トレンド取得件数0件（構造確認要）"}
      )

    return trends[:30]  # 上位30件に絞る
  except Exception as e:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [{"datetime": now, "keyword": f"エラー: {str(e)}"}]


def save_to_csv(trends):
  csv_file = "trend_log.csv"
  new_df = pd.DataFrame(trends)

  if os.path.exists(csv_file):
    existing_df = pd.read_csv(csv_file)
    updated_df = pd.concat([existing_df, new_df], ignore_index=True)
    updated_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
  else:
    new_df.to_csv(csv_file, index=False, encoding="utf-8-sig")
  print(f"成功: {len(trends)} 件のトレンドを保存しました。")


if __name__ == "__main__":
  trend_data = get_trends()
  save_to_csv(trend_data)
