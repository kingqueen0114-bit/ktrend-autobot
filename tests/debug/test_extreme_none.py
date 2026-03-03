import traceback

def test_extreme_none_draft():
    from handlers.draft_editor import view_draft
    import handlers.draft_editor
    
    mock_draft = {
        "status": None,
        "trend_source": {
            "title": None,
            "url": None,
            "snippet": None,
            "image_url": None,
            "image_source": None,
            "category": None,
            "artist_tags": None
        },
        "sns_content": {
            "news_post": None,
            "luna_post_a": None,
            "luna_post_b": None
        },
        "cms_content": {
            "title": None,
            "body": None,
            "meta_description": None,
            "x_post_1": None,
            "x_post_2": None
        }
    }
    
    class TestStorage:
        def __init__(self):
            pass
        def get_draft(self, draft_id):
            return mock_draft
            
    handlers.draft_editor.StorageManager = TestStorage
    
    class MockRequest:
        def __init__(self):
            self.args = {'id': 'extreme_none'}
            self.method = 'GET'
            
    print("🚀 Running extreme None test on view_draft...")
    try:
        req = MockRequest()
        res, status = view_draft(req)
        print(f"✅ Status: {status}")
        if status == 500:
            print("❌ Server Error Output:")
            print(res)
    except Exception as e:
        print("❌ CRASH:")
        traceback.print_exc()

if __name__ == "__main__":
    test_extreme_none_draft()
