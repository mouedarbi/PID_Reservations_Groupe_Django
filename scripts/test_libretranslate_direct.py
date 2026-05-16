import requests
import json

URL = "http://159.223.211.21:5000/translate"
payload = {
    'q': "Comedy",
    'source': 'auto',
    'target': 'fr',
    'format': 'text'
}
headers = {'Content-Type': 'application/json'}

try:
    response = requests.post(URL, data=json.dumps(payload), headers=headers, timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
