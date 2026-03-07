import os

print("Google Custom Search API Key の設定を行います。")
print("取得した新しいAPIキー (AIzaSy...) を貼り付けてください（Geminiと同じものでOKです）。")
api_key = input("API Key: ").strip()

if not api_key:
    print("エラー: APIキーが入力されていません。")
    exit(1)

with open("/tmp/search_api_key.txt", "w") as f:
    f.write(api_key)

print("Secret Manager に登録中...")
os.system('/Users/yuiyane/google-cloud-sdk/bin/gcloud secrets versions add GOOGLE_CUSTOM_SEARCH_API_KEY --data-file="/tmp/search_api_key.txt" --project="k-trend-autobot"')
os.remove("/tmp/search_api_key.txt")
print("✅ 完了しました！")
