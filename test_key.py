import requests

# PASTE YOUR GEMINI KEY HERE (The one from AI Studio)
API_KEY = "AQ.API"

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite-001:generateContent?key={API_KEY}"
data = {"contents": [{"parts": [{"text": "Say hello in 3 words"}]}]}

print("🔍 Testing your key directly with Google...")
try:
    response = requests.post(url, json=data, timeout=10)
except requests.RequestException as e:
    print("❌ Request failed:", e)
    raise SystemExit(1)

if response.status_code == 200:
    print("✅ SUCCESS! Your key is perfect.")
    try:
        text = response.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        text = response.text
    print("AI says:", text)
else:
    print("❌ FAILED. Google is blocking this key.")
    print("Error details:", response.text)