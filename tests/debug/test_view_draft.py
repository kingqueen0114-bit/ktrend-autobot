import os
from dotenv import load_dotenv

load_dotenv()

# We need a mock request for functions_framework
class MockRequest:
    def __init__(self, method='GET', args=None, form=None):
        self.method = method
        self.args = args or {}
        self.form = form or {}

def test_view_draft():
    from src.storage_manager import StorageManager
    from handlers.draft_editor import view_draft
    
    # 1. Fetch latest draft ID from Firestore
    print("🔍 Finding the latest draft ID...")
    storage = StorageManager()
    docs = storage.db.collection(storage.collection_name).order_by('created_at', direction='DESCENDING').limit(1).stream()
    
    draft_id = None
    for doc in docs:
        draft_id = doc.id
        break
        
    if not draft_id:
        print("❌ No drafts found in DB")
        return
        
    print(f"✅ Found Draft ID: {draft_id}")
    
    # 2. Mock GET Request to view_draft
    print("🚀 Rendering View Draft page...")
    req = MockRequest(args={'id': draft_id})
    try:
        response, status = view_draft(req)
        print(f"Status: {status}")
        if status == 200:
            print("✅ Successfully rendered HTML (length:", len(response), "chars)")
        else:
            print(f"⚠️ Render failed with status {status}: {response}")
    except Exception as e:
        import traceback
        print("\n❌ CRASH DETECTED ❌")
        traceback.print_exc()

if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "AIzaSyDnssaqiBmzXI2I_3aupeU_N1Fgx0bB6tk"
    
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        # Explicitly set the SA key path for local DB connection
        sa_key = "/Users/yuiyane/ktrend-autobot/ktrend-tools-ad1ef43ae99b.json"
        if os.path.exists(sa_key):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_key
        else:
            print("⚠️ GCP Service Account JSON not found. DB connection might fail.")
            
    test_view_draft()
