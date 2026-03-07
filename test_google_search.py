import os
import requests
from dotenv import load_dotenv

load_dotenv(".env.deploy.yaml")
api_key = os.popen('/Users/yuiyane/google-cloud-sdk/bin/gcloud secrets versions access latest --secret="GOOGLE_CUSTOM_SEARCH_API_KEY" --project="k-trend-autobot"').read().strip()
search_engine_id = os.environ.get("GOOGLE_CSE_ID")

print(f"Testing Google Custom Search API...")
print(f"Engine ID: {search_engine_id}")

try:
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q=韓国トレンド&num=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        items = data.get("items", [])
        print(f"Success! Found {len(items)} results.")
        if items:
            print(f"First result: {items[0].get('title')} - {items[0].get('link')}")
    else:
        print(f"Error {response.status_code}: {response.text}")
except Exception as e:
    print(f"Request failed: {e}")
