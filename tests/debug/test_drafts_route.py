import sys
import traceback

def test_drafts_route():
    from main import main as cloud_main
    
    class MockRequest:
        def __init__(self):
            self.method = "GET"
            self.path = "/drafts"
            self.args = {}
            self.headers = {}
            self.is_json = False
            self.data = b""
        def get_json(self, silent=True):
            return {}

    try:
        print("🚀 Executing /drafts route locally through cloud_entry...")
        req = MockRequest()
        res = cloud_main(req)
        print("Result:", res)
    except Exception as e:
        print("❌ CRASH DURING ROUTING ❌")
        traceback.print_exc()

if __name__ == "__main__":
    import os
    sa_key = "/Users/yuiyane/ktrend-autobot/analytics-key.json"
    if os.path.exists(sa_key):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_key
        
    test_drafts_route()
