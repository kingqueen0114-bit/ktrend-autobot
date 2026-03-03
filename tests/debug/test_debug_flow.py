import os
import json
import traceback
from dotenv import load_dotenv

load_dotenv()

def run_debug():
    print("🚀 Starting Debug Pipeline...")
    try:
        from src.fetch_trends import TrendFetcher
        from src.content_generator import ContentGenerator
        from src.storage_manager import StorageManager
        from src.notifier import Notifier
        
        # 1. Init
        print("1. Initializing classes...")
        api_key = os.getenv("GEMINI_API_KEY")
        fetcher = TrendFetcher(api_key)
        generator = ContentGenerator(api_key)
        
        # We will stop before actually touching DB to avoid spamming unless we need to
        # Let's just run fetch and generate first, they are the most suspicious
        
        print("2. Fetching trends...")
        trends = fetcher.fetch_trends()
        if not trends:
            print("❌ No trends found")
            return
            
        trend = trends[0]
        print(f"✅ Trend fetched: {trend.get('title')}")
        
        print("3. Generating content...")
        sns_content = generator.generate_content(trend)
        print("✅ SNS Content generated")
        
        print("4. Generating article...")
        article, grounding = generator.generate_cms_article(trend, trend_sign_context=trend.get('snippet', ''))
        print(f"✅ Article generated: {article.get('title')}")
        
        print("5. Checking quality...")
        from src.content_generator import check_article_quality
        quality = check_article_quality(article, trend)
        print(f"✅ Quality Score: {quality['score']}")
        if not quality['passed']:
            print("⚠️ Article failed quality check! This might trigger rewrite.")
            print(quality['warnings'])
            
            # This is likely where it fails! A rewrite might be crashing.
            print("6. Rewriting article...")
            article, grounding = generator.rewrite_article(article, quality["warnings"], trend, trend_sign_context=trend.get('snippet', ''))
            print("✅ Rewrite complete")
            
            quality2 = check_article_quality(article, trend)
            print(f"✅ Quality Score after rewrite: {quality2['score']}")
            
        print("--- Pipeline ran perfectly up to storage ---")
        
    except Exception as e:
        print("\n❌ CRASH DETECTED ❌")
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure key is present
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️ Setting hardcoded GEMINI_API_KEY for debug")
        os.environ["GEMINI_API_KEY"] = "AIzaSyDnssaqiBmzXI2I_3aupeU_N1Fgx0bB6tk"
        
    run_debug()
