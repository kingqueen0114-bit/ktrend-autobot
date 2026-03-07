import os
import sys
import subprocess

print("🔄 Gcloud から LINE_CHANNEL_ACCESS_TOKEN を取得しています...")
try:
    result = subprocess.run(
        ['/Users/yuiyane/google-cloud-sdk/bin/gcloud', 'secrets', 'versions', 'access', 'latest', '--secret=LINE_CHANNEL_ACCESS_TOKEN', '--project=k-trend-autobot'],
        capture_output=True,
        text=True,
        check=True
    )
    token = result.stdout.strip()
    if not token:
        print("❌ トークンが空です。Secret Manager を確認してください。")
        sys.exit(1)
    print("✅ トークンを取得しました。リッチメニューを設定します...")
except subprocess.CalledProcessError as e:
    print(f"❌ gcloud コマンドの実行に失敗しました。: {e.stderr}")
    sys.exit(1)

# .env に一時的に書き込む
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
with open(env_path, "a") as f:
    f.write(f"\nLINE_CHANNEL_ACCESS_TOKEN='{token}'\n")

# setup_richmenu.py を実行
print("\n=== setup_richmenu.py の実行 ===")
os.system(f"python3 setup_richmenu.py --image assets/rich_menu_v7_minimal.png")

# クリーンアップ (今回追記した行を削除)
lines = []
if os.path.exists(env_path):
    with open(env_path, "r") as f:
        lines = f.readlines()
    with open(env_path, "w") as f:
        for line in lines:
            if "LINE_CHANNEL_ACCESS_TOKEN" not in line:
                f.write(line)

print("✨ 自動セットアップが完了しました。")
