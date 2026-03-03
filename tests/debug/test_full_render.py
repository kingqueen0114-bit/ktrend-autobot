import os
import json
import traceback
from dotenv import load_dotenv

load_dotenv()
os.environ["GEMINI_API_KEY"] = "AIzaSyDnssaqiBmzXI2I_3aupeU_N1Fgx0bB6tk"

def debug_full_render_pipeline():
    from src.fetch_trends import TrendFetcher
    from src.content_generator import ContentGenerator
    import src.storage_manager
    from handlers.draft_editor import view_draft
    
    print("1. Fetching trends...")
    api_key = os.environ["GEMINI_API_KEY"]
    fetcher = TrendFetcher(api_key)
    trends = fetcher.fetch_trends()
    if not trends:
        print("❌ No trends generated")
        return
        
    trend = trends[0]
    print(f"✅ Trend fetched: {trend.get('title')}")
    
    print("2. Generating article via REST API...")
    generator = ContentGenerator(api_key)
    article, grounding = generator.generate_cms_article(trend, trend_sign_context=trend.get('snippet', ''))
    
    sns = generator.generate_content(trend)
    
    print("3. Assembling mock draft object...")
    mock_draft = {
        "status": "pending",
        "trend_source": {
            "title": trend.get("title", ""),
            "url": trend.get("link", ""),
            "snippet": trend.get("snippet", ""),
            "image_url": trend.get("image_url", "https://example.com/mock.jpg"),
            "image_source": trend.get("image_source", ""),
            "category": trend.get("category", "trend"),
            "artist_tags": trend.get("artist_tags", [])
        },
        "sns_content": {
            "news_post": sns.get("news_post", ""),
            "luna_post_a": sns.get("luna_post_a", ""),
            "luna_post_b": sns.get("luna_post_b", "")
        },
        "cms_content": article
    }
    
    # Dump it to see what it looks like
    print("--- DRAFT DATA ---")
    print(json.dumps(mock_draft, indent=2, ensure_ascii=False))
    print("------------------")
    
    # Mock Storage
    class TestStorage:
        def __init__(self):
            pass
        def get_draft(self, draft_id):
            return mock_draft
            
    import handlers.draft_editor
    handlers.draft_editor.StorageManager = TestStorage
    
    # Mock Request
    class MockRequest:
        def __init__(self):
            self.args = {'id': 'test_draft_id'}
            self.method = 'GET'
            
    print("4. Running view_draft HTML renderer...")
    try:
        req = MockRequest()
        res, status = view_draft(req)
        print(f"✅ Render Status: {status}")
        if status == 500:
            print("❌ Render returned 500 error!")
            print(res)
    except Exception as e:
        print("❌ CRASH DURING RENDER ❌")
        traceback.print_exc()

if __name__ == "__main__":
    debug_full_render_pipeline()
