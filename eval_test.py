import sys
sys.path.append('/Users/yuiyane/ktrend-autobot')
import os
os.environ['GCP_PROJECT_ID'] = 'k-trend-autobot'

from handlers.draft_editor import view_draft

class MockRequest:
    method = 'GET'
    args = {'id': 'test'}
    form = {}
    files = {}

import src.storage_manager
class MockStorage:
    def get_draft(self, draft_id):
        return {
            'id': draft_id,
            'status': 'draft',
            'cms_content': {'title':'Test', 'body':'Body', 'meta_description':'Meta'},
            'trend_source': {'category': 'trend', 'image_url': 'https://example.com/test.jpg'}
        }
src.storage_manager.StorageManager = MockStorage

# Call view-draft handler directly
try:
    response = view_draft(MockRequest())
    # response is a tuple (html_string, status_code)
    html = response[0]
    with open('rendered.html', 'w') as f:
        f.write(html)
except Exception as e:
    print("Error generating html:", e)
