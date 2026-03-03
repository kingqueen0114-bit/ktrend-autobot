import requests, json
api_key = "AIzaSyDnssaqiBmzXI2I_3aupeU_N1Fgx0bB6tk"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
prompt = """あなたは韓国トレンド情報の専門家です。「韓国旅行 おすすめ 穴場」に関する最新のトレンド情報を3つ提供してください。
以下のJSON配列形式で回答してください（JSONのみ、他のテキスト不要）：
[
  {
    "title": "...",
    "link": "...",
    "snippet": "..."
  }
]"""
payload = {"contents": [{"parts": [{"text": prompt}]}], "tools": [{"googleSearch": {}}], "generationConfig": {"temperature": 0.5}}
r = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
data = r.json()
print("FULL RESPONSE:")
print(json.dumps(data, indent=2, ensure_ascii=False))
