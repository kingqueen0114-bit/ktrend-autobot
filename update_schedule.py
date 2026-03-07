import os
import subprocess

print("🕒 K-Trend AutoBot 記事自動作成のスケジュール変更")
print("Cloud Schedulerジョブの一覧を取得し、18時に変更するジョブを選択します。")
print("-" * 50)

# 1. ジョブ一覧の取得
cmd_list = '/Users/yuiyane/google-cloud-sdk/bin/gcloud scheduler jobs list --location=asia-northeast1 --format="value(ID)"'
print("ジョブ一覧を取得中...")

try:
    result = subprocess.run(cmd_list, shell=True, check=True, capture_output=True, text=True)
    jobs = result.stdout.strip().split('\n')
    valid_jobs = [j for j in jobs if j]

    if not valid_jobs:
        print("❌ asia-northeast1 に Cloud Scheduler のジョブが見つかりません。")
        exit(1)

    print("\n見つかったジョブ:")
    for i, job in enumerate(valid_jobs):
        print(f"[{i + 1}] {job}")
    
    print("\nターゲットとなる記事自動生成のジョブ（例: ktrend-daily-fetch や ktrend-article-generator など）の番号を入力してください。")
    choice = input("入力 (1-{}): ".format(len(valid_jobs)))

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(valid_jobs):
            target_job = valid_jobs[idx]
        else:
            print("❌ 無効な番号です。")
            exit(1)
    except ValueError:
        print("❌ 無効な入力です。")
        exit(1)

    print(f"\n[{target_job}] のスケジュールを「毎日 18:00 のみ」に変更します。")
    cmd_update = f'/Users/yuiyane/google-cloud-sdk/bin/gcloud scheduler jobs update http {target_job} --schedule="0 18 * * *" --time-zone="Asia/Tokyo" --location="asia-northeast1"'
    
    response = os.system(cmd_update)
    
    if response == 0:
        print("\n✅ スケジュールの更新が完了しました！これからは毎日18時に1回だけ実行されます。")
    else:
        print("\n❌ スケジュールの更新に失敗しました。")

except subprocess.CalledProcessError as e:
    print(f"❌ ジョブ一覧の取得に失敗しました: {e.stderr}")
