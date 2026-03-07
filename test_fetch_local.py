from dotenv import load_dotenv
import os

# Ensure we use the latest env vars
load_dotenv(".env.deploy.yaml")
# Override the .env.deploy.yaml's lack of GEMINI_API_KEY with the actual secret
api_key = os.popen('/Users/yuiyane/google-cloud-sdk/bin/gcloud secrets versions access latest --secret="GEMINI_API_KEY" --project="k-trend-autobot"').read().strip()
os.environ["GEMINI_API_KEY"] = api_key

from src.fetch_trends import TrendFetcher
fetcher = TrendFetcher(api_key)
try:
    print("Testing fetcher locally...")
    trends = fetcher.fetch_trends(include_kpop=True, limit=1)
    print("Success")
except Exception as e:
    print(f"Error occurred: {e}")
