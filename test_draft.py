import os
from google.cloud import firestore

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/yuiyane/.config/gcloud/application_default_credentials.json'

try:
    db = firestore.Client(project='k-trend-autobot')
    drafts = db.collection('drafts').limit(1).stream()
    for draft in drafts:
        print(f"Draft ID: {draft.id}")
        break
    else:
        print("No drafts found.")
except Exception as e:
    print(f"Error: {e}")
