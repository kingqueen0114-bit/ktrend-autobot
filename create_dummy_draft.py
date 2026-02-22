import os
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/yuiyane/.config/gcloud/application_default_credentials.json'

if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'k-trend-autobot',
    })

db = firestore.client()

dummy_draft = {
    'created_at': datetime.now(),
    'status': 'draft',
    'trend_source': {
        'title': 'Test Trend',
        'query': 'Test',
        'image_url': 'https://via.placeholder.com/800x450?text=Testing+Image',
        'category': 'trend'
    },
    'cms_content': {
        'title': 'Test Draft Title',
        'meta_description': 'Test meta description',
        'body': 'This is the test body content with a dummy image: \n\n![Testing](https://via.placeholder.com/800x450?text=Testing+Image)\n'
    }
}

try:
    doc_ref = db.collection('drafts').document()
    doc_ref.set(dummy_draft)
    print(f"Created dummy draft ID: {doc_ref.id}")
except Exception as e:
    print(f"Error creating dummy draft: {e}")
