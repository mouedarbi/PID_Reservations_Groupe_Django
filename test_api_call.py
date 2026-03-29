import requests
import json

pk = 1
api_url = f"http://127.0.0.1:8000/api/shows/{pk}/"

try:
    response = requests.get(api_url)
    response.raise_for_status()
    show_data = response.json()
    print(f"Keys: {list(show_data.keys())}")
    print(f"Representations: {show_data.get('representations')}")
    print(f"Representations count: {len(show_data.get('representations', []))}")
except Exception as e:
    print(f"Error: {e}")
