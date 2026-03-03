import os
import requests
from google.cloud import firestore
import google.auth
from google.oauth2 import service_account

def run_test():
    creds = service_account.Credentials.from_service_account_file("/Users/yuiyane/ktrend-autobot/analytics-key.json")
    db = firestore.Client(project="k-trend-autobot", credentials=creds)
    
    docs = db.collection("ktrend_drafts").order_by("created_at", direction="DESCENDING").limit(1).stream()
    real_id = None
    for d in docs:
        real_id = d.id
        
    print(f"Draft ID: {real_id}")
    if real_id:
        url = f"https://ktrend-autobot-nnfhuwwfiq-an.a.run.app/view-draft?id={real_id}"
        print(f"Fetching: {url}")
        res = requests.get(url)
        print("Status", res.status_code)
        if res.status_code == 500:
            print("ERROR:")
            print(res.text[:1000])

if __name__ == "__main__":
    run_test()
