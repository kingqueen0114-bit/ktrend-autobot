import os
from src.storage_manager import StorageManager
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/yuiyane/.config/gcloud/application_default_credentials.json'
os.environ["GCP_PROJECT_ID"] = "k-trend-autobot"
storage = StorageManager()
docs = storage.db.collection(storage.collection_name).order_by('created_at', direction='DESCENDING').limit(1).stream()
for doc in docs:
    data = doc.to_dict()
    print("TITLE:", data['cms_content']['title'])
    print("BODY:\n", data['cms_content']['body'])
    break
