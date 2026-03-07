import os
import sys

# Get tokens from user input since gcloud secrets fails locally
print("LINEのリッチメニューを設定します。")
token = input("LINE_CHANNEL_ACCESS_TOKEN を入力してください: ").strip()

if not token:
    print("エラー: トークンが入力されていません。")
    sys.exit(1)

# Write a temporary .env file
with open(".env", "a") as f:
    f.write(f"\nLINE_CHANNEL_ACCESS_TOKEN='{token}'\n")

print("実行中...")
os.system("python3 setup_richmenu.py --image assets/rich_menu_v7_minimal.png")

# Cleanup
os.system("sed -i '' '/LINE_CHANNEL_ACCESS_TOKEN/d' .env 2>/dev/null || true")
print("完了しました。")
