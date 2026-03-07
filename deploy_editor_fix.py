import os
print("🚀 最新の Sanity エディタ修復パッチを Cloud Functions にデプロイします...")

cmd = '''
/Users/yuiyane/google-cloud-sdk/bin/gcloud functions deploy ktrend-autobot \
  --gen2 --region=asia-northeast1 --runtime=python311 \
  --entry-point=main --trigger-http --allow-unauthenticated \
  --memory=512MB --timeout=540s \
  --env-vars-file=.env.deploy.yaml \
  --set-secrets="GEMINI_API_KEY=GEMINI_API_KEY:latest,GOOGLE_CUSTOM_SEARCH_API_KEY=GOOGLE_CUSTOM_SEARCH_API_KEY:latest,LINE_CHANNEL_ACCESS_TOKEN=LINE_CHANNEL_ACCESS_TOKEN:latest,LINE_CHANNEL_SECRET=LINE_CHANNEL_SECRET:latest,WORDPRESS_APP_PASSWORD=WORDPRESS_APP_PASSWORD:latest,SANITY_API_TOKEN=SANITY_API_TOKEN:latest,EDIT_SECRET=EDIT_SECRET:latest,PREVIEW_SECRET=PREVIEW_SECRET:latest" \
  --source=.
'''
os.system(cmd)
print("✅ デプロイコマンドの実行が完了しました！")
