import subprocess
import os

print("AI StudioのAPIキーを貼り付けてEnterを押してください。")
api_key = input("API Key: ").replace(" ", "").replace("\n", "").strip()

if not api_key:
    print("エラー: キーが入力されていません。")
    exit(1)

print(f"\n入力されたキー: {api_key[:5]}...{api_key[-5:]} (文字数: {len(api_key)})  ※余分な文字を削除しました")

try:
    gcloud_path = "/Users/yuiyane/google-cloud-sdk/bin/gcloud"
    process = subprocess.Popen(
        [gcloud_path, 'secrets', 'versions', 'add', 'GEMINI_API_KEY', '--data-file=-', '--project=k-trend-autobot'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=api_key)
    if process.returncode == 0:
        print("✅ Secret Managerの更新が完了しました！")
    else:
        print(f"❌ エラーが発生しました:\n{stderr}")
except Exception as e:
    print(f"エラー: {e}")
