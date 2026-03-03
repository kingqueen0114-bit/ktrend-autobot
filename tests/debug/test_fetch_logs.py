import os
from google.cloud import logging

def fetch_logs():
    # Attempt to use the existing SA key if present for local read access
    sa_key = "/Users/yuiyane/ktrend-autobot/analytics-key.json"
    if os.path.exists(sa_key):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_key
        
    try:
        client = logging.Client()
        # Look for the last few errors on the Cloud Run service
        filter_str = 'resource.type="cloud_run_revision" severity>=ERROR'
        print(f"🔍 Fetching recent ERROR logs for Cloud Run...")
        
        entries = client.list_entries(filter_=filter_str, order_by=logging.DESCENDING, max_results=10)
        found = False
        for entry in entries:
            found = True
            print("-" * 40)
            print(f"Time: {entry.timestamp}")
            if entry.payload:
                if isinstance(entry.payload, dict):
                    print(entry.payload.get("message", entry.payload))
                else:
                    print(entry.payload)
        
        if not found:
            print("No recent errors found matching the filter.")
            
    except Exception as e:
        print(f"❌ Failed to fetch logs: {e}")

if __name__ == "__main__":
    fetch_logs()
