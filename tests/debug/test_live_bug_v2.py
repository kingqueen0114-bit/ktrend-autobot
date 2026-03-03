import os
import requests
from src.storage_manager import StorageManager
from google.cloud import firestore

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/yuiyane/.config/gcloud/application_default_credentials.json'
os.environ["GCP_PROJECT_ID"] = "k-trend-autobot"

storage = StorageManager()
docs = storage.db.collection(storage.collection_name).order_by('created_at', direction='DESCENDING').limit(1).stream()

real_id = None
for doc in docs:
    real_id = doc.id
    break

if real_id:
    print(f"✅ Found real Draft ID: {real_id}")
    live_url = f"https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/view-draft?id={real_id}"
    print(f"🚀 Fetching Live URL: {live_url}")
    res = requests.get(live_url)
    print(f"Status Code: {res.status_code}")
    if res.status_code >= 400:
        print(res.text[:800])
else:
    print("❌ No articles in DB")
