from handlers.webhook import handle_line_webhook
from linebot.models import MessageEvent, TextMessage, SourceUser
from linebot import LineBotApi, WebhookHandler
import os

# Create mock objects
class MockRequest:
    def __init__(self, data=None, headers=None):
        self._data = data
        self.headers = headers or {}
        self.method = 'POST'
    def get_data(self, as_text=False):
        return self._data

os.environ['LINE_CHANNEL_SECRET'] = 'test_secret'
os.environ['LINE_CHANNEL_ACCESS_TOKEN'] = 'test_token'

# Mock LineBotApi to not actually send HTTP requests
class MockLineBotApi:
    def __init__(self, token):
        pass
    def reply_message(self, token, messages):
        print(f"[MOCK] Replying to {token} with {messages[0].text if hasattr(messages[0], 'text') else 'NON-TEXT'}")
    def push_message(self, to, messages):
        print(f"[MOCK] Pushing to {to} with {messages[0].text if hasattr(messages[0], 'text') else 'NON-TEXT'}")
    def get_message_content(self, message_id):
        pass

# Monkey patch
import linebot
linebot.LineBotApi = MockLineBotApi

# We need to bypass the webhook handler signature check
# Let's create a fake body and parse it manually.
fake_body = '{"events":[{"type":"message","message":{"type":"text","id":"123","text":"統計"},"timestamp":123,"source":{"type":"user","userId":"U12345"},"replyToken":"test_token"}]}'

class MockHandler:
    def __init__(self, secret):
        pass
    def parse(self, body, signature):
        event = MessageEvent(
            message=TextMessage(id='123', text='統計'),
            source=SourceUser(user_id='U12345'),
            reply_token='test_token',
            timestamp=123
        )
        return [event]

linebot.WebhookHandler.parser = MockHandler('test_secret')

# Run the webhook
request = MockRequest(data=fake_body, headers={'X-Line-Signature': 'fake_signature'})
print(handle_line_webhook(request))
