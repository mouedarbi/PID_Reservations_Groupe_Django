import requests
import json

pk = 1
import os

# Utilise une variable d'environnement pour l'URL de base, avec un défaut à 8000
BASE_URL = os.getenv('API_BASE_URL', 'http://127.0.0.1:8000')
api_url = f"{BASE_URL}/api/shows/{pk}/"


try:
    response = requests.get(api_url)
    response.raise_for_status()
    show_data = response.json()
    print(f"Keys: {list(show_data.keys())}")
    print(f"Representations: {show_data.get('representations')}")
    print(f"Representations count: {len(show_data.get('representations', []))}")
except Exception as e:
    print(f"Error: {e}")
