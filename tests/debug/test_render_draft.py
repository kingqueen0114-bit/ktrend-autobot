import traceback
import sys
# Mock the StorageManager to avoid DB connections
import src.storage_manager
class MockStorage:
    def __init__(self):
        pass
    def get_draft(self, draft_id):
        return {
            "status": "pending",
            "trend_source": {
                "category": "trend",
                "image_url": "https://example.com/image.jpg",
                "title": "Mock Title",
            },
            "cms_content": {
                "title": "Mock CMS Title",
                "body": "Mock body content",
                "meta_description": "Mock meta",
                "x_post_1": "Mock x post",
            },
            "sns_content": {
                "news_post": "Mock news post"
            }
        }
src.storage_manager.StorageManager = MockStorage

def test_render():
    from handlers.draft_editor import view_draft
    class MockRequest:
        def __init__(self):
            self.args = {'id': 'mocked_id'}
            self.method = 'GET'
    try:
        req = MockRequest()
        res, status = view_draft(req)
        print("Status", status)
        if status == 200:
            print("Length", len(res))
            print("Render Success!")
    except Exception as e:
        print("CRASH")
        traceback.print_exc()

if __name__ == "__main__":
    test_render()
