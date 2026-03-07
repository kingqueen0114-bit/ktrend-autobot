import requests

api_key = input("API Key: ").strip()

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("Available Models:")
    for model in data.get('models', []):
        if 'flash' in model['name'] or 'gemini-2.0' in model['name'] or 'gemini-1.5' in model['name']:
            print(f"- {model['name']} (Supported methods: {model.get('supportedGenerationMethods', [])})")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
