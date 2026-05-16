import requests
import json
import sys

API_KEY = "a83MpOcyzpdlXQIXW5u4K0Qrpf39v61p"
BASE_URL = "https://app.ticketmaster.com/discovery/v2"

def search_attraction(keyword):
    print(f"\n--- Recherche de l'attraction : {keyword} ---")
    url = f"{BASE_URL}/attractions.json"
    params = {
        "keyword": keyword,
        "apikey": API_KEY,
        "size": 5
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Erreur API: {response.status_code}")
        return

    data = response.json()
    attractions = data.get("_embedded", {}).get("attractions", [])
    
    if not attractions:
        print("Aucune attraction trouvée.")
        return

    for att in attractions:
        name = att.get("name")
        att_id = att.get("id")
        att_type = att.get("type")
        classifications = att.get("classifications", [])
        genre = classifications[0].get("genre", {}).get("name") if classifications else "N/A"
        
        print(f"Nom: {name} | ID: {att_id} | Type: {att_type} | Genre: {genre}")

def search_events_with_artist(keyword):
    print(f"\n--- Recherche d'événements pour : {keyword} ---")
    url = f"{BASE_URL}/events.json"
    params = {
        "keyword": keyword,
        "apikey": API_KEY,
        "size": 5,
        "countryCode": "BE" # On restreint à la Belgique pour le projet
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Erreur API: {response.status_code}")
        return

    data = response.json()
    events = data.get("_embedded", {}).get("events", [])
    
    if not events:
        print("Aucun événement trouvé en Belgique.")
        # Réessayer sans restriction de pays pour voir la structure
        params.pop("countryCode")
        response = requests.get(url, params=params)
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

    for event in events:
        event_name = event.get("name")
        embedded = event.get("_embedded", {})
        attractions = embedded.get("attractions", [])
        
        artist_names = [a.get("name") for a in attractions if a.get("type") == "attraction"]
        print(f"Événement: {event_name}")
        print(f"  Artistes trouvés dans _embedded.attractions: {artist_names}")

if __name__ == "__main__":
    search_attraction("Haroun")
    search_attraction("Houria les yeux verts")
    
    search_events_with_artist("Haroun")
    search_events_with_artist("Houria les yeux verts")
