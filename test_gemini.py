import os
import requests
import json

api_key = input("APIキーを入力してください: ")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
payload = {
    "contents": [{"parts": [{"text": "Hello"}]}],
    "generationConfig": {"temperature": 0.7}
}

response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
