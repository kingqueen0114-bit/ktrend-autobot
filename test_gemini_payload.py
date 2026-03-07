import os
import requests
import json

api_key = input("APIキーを入力してください: ")

prompt = """あなたは韓国トレンド情報の専門家です。「韓国 最新 トレンド」に関する最新のトレンド情報を3つ提供してください。
以下の条件を厳守してください：
1. ただの事実やニュースの要約ではなく、SNSでのユーザーの反応や、他ブランドとのコラボ、市場の動きなど「なぜ今これが流行る兆しなのか」という流行のサイン（兆し）を必ず含めること。
2. K-POPアイドルの情報の場合は、PR TIMES等の公式プレスリリースやInstagramでの発言など、具体的なソースや一次情報を意識した内容にすること。
3. 推測ではなく、事実に基づいた最新情報を出力すること。

以下のJSON配列形式で回答してください（JSONのみ、他のテキスト不要）：
[
  {
    "title": "トレンドのタイトル（魅力的で具体的なもの）",
    "link": "参考になるURL（公式ニュース、PR TIMES、Instagramリンクなど。架空のものでも形式が合っていれば可）",
    "snippet": "トレンドの具体的な内容。ただの事実ではなく、なぜ話題なのか、どのような「流行のサイン」があるのかを含めた150文字程度の解説。"
  }
]
- linkはダミーURLで構いません"""

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "temperature": 0.7
    }
}

response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload)
print(f"Status: {response.status_code}")
if response.status_code != 200:
    print(f"Error detail: {response.text}")
else:
    print("Success!")
