import requests
import json
import sys

API_KEY = "a83MpOcyzpdlXQIXW5u4K0Qrpf39v61p"
BASE_URL = "https://app.ticketmaster.com/discovery/v2"

def test_event_genre(keyword):
    print(f"\n--- Recherche du genre pour l'événement : {keyword} ---")
    url = f"{BASE_URL}/events.json"
    params = {
        "keyword": keyword,
        "apikey": API_KEY,
        "size": 1,
        "countryCode": "BE"
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Erreur API: {response.status_code}")
        return

    data = response.json()
    events = data.get("_embedded", {}).get("events", [])
    
    if not events:
        print("Aucun événement trouvé.")
        return

    event = events[0]
    classifications = event.get("classifications", [])
    if classifications:
        c = classifications[0]
        segment = c.get("segment", {}).get("name")
        genre = c.get("genre", {}).get("name")
        subgenre = c.get("subGenre", {}).get("name")
        print(f"Événement: {event.get('name')}")
        print(f"Segment: {segment}")
        print(f"Genre: {genre}")
        print(f"SubGenre: {subgenre}")
    else:
        print("Aucune classification trouvée.")

if __name__ == "__main__":
    test_event_genre("Haroun")
    test_event_genre("Houria les yeux verts")
    test_event_genre("Musique")
