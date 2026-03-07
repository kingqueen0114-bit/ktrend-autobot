import os

print("🕒 K-Trend AutoBot: 記事自動作成のスケジュールを「毎日 18:00 のみ」に変更します")
print("-" * 50)

GCLOUD = '/Users/yuiyane/google-cloud-sdk/bin/gcloud'
LOCATION = '--location="asia-northeast1"'

# 1. メインのスケジュールを18:00に更新
print("[1/3] メインのスケジュール (ktrend-daily-fetch-scheduler) を 18:00 に変更中...")
cmd1 = f'{GCLOUD} scheduler jobs update http ktrend-daily-fetch-scheduler --schedule="0 18 * * *" --time-zone="Asia/Tokyo" {LOCATION}'
os.system(cmd1)

# 2. 昼の重複ジョブを一時停止
print("[2/3] 重複する昼のジョブ (ktrend-daily-fetch-scheduler-noon) を一時停止中...")
cmd2 = f'{GCLOUD} scheduler jobs pause ktrend-daily-fetch-scheduler-noon {LOCATION}'
os.system(cmd2)

# 3. 夜の重複ジョブを一時停止
print("[3/3] 重複する夜のジョブ (ktrend-daily-fetch-scheduler-evening) を一時停止中...")
cmd3 = f'{GCLOUD} scheduler jobs pause ktrend-daily-fetch-scheduler-evening {LOCATION}'
os.system(cmd3)

print("-" * 50)
print("✅ スケジュールの更新・統合が完了しました！")
print("これからは毎日 18:00 の 1日1回だけ 記事が自動生成されます。")
