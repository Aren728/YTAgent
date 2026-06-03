import requests

# PASTE YOUR GEMINI KEY HERE (The one from AI Studio)
API_KEY = "AQ.GEMINI" 

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print("🔍 Asking Google for the list of available models...")
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get('models', [])
    print("✅ SUCCESS! Here are your available models:")
    for model in models:
        # We only want models that can generate text
        if 'generateContent' in model.get('supportedGenerationMethods', []):
            print("👉", model['name'])
else:
    print("❌ Error:", response.text)