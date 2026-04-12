import requests
import sys

def test_api(base_url, lang):
    url = f"{base_url.rstrip('/')}/api/shows/"
    headers = {"Accept-Language": lang}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                show = data[0]
                print(f"[{lang}] Title: {show.get('title')}")
        else:
            print(f"Error {response.status_code} for {lang}")
    except Exception as e:
        print(f"Request failed for {lang}: {e}")

if __name__ == "__main__":
    # Usage: python test_api_translation.py [port_or_url]
    # Default to 8000 if no argument provided
    
    arg = sys.argv[1] if len(sys.argv) > 1 else "8000"
    
    if arg.startswith("http"):
        base_url = arg
    elif arg.isdigit():
        base_url = f"http://127.0.0.1:{arg}"
    else:
        base_url = "http://127.0.0.1:8000"
        
    print(f"Testing API on: {base_url}")
    
    for lang in ['fr', 'en', 'nl']:
        test_api(base_url, lang)
