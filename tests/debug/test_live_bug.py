import os
import requests

def get_real_draft_and_test():
    sa_key = "/Users/yuiyane/ktrend-autobot/analytics-key.json"
    if os.path.exists(sa_key):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_key
        # FORCE project injection so it doesn't crash on credentials missing metadata
        os.environ["GCP_PROJECT_ID"] = "k-trend-autobot"
        
    try:
        from src.storage_manager import StorageManager
        from google.cloud import firestore
        import google.auth
        
        # Manually initialize firestore bypassing manager if needed,
        # but the manager reads GCP_PROJECT_ID which we just set.
        storage = StorageManager()
        
        print("🔍 Connecting to Firestore...")
        docs = storage.db.collection(storage.collection_name).order_by('created_at', direction='DESCENDING').limit(1).stream()
        
        real_id = None
        for doc in docs:
            real_id = doc.id
            break
            
        if not real_id:
            print("❌ No articles in DB")
            return
            
        print(f"✅ Found real Draft ID: {real_id}")
        
        # Test Live URL
        live_url = f"https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/view-draft?id={real_id}"
        print(f"🚀 Fetching Live URL: {live_url}")
        res = requests.get(live_url)
        print(f"Status Code: {res.status_code}")
        if res.status_code == 500:
            print("❌ 500 INTERNAL SERVER ERROR REPRODUCED")
            print(res.text[:500])
        else:
            print("✅ SUCCESS!")
            print(res.text[:100])
            
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    get_real_draft_and_test()
