import requests

def test_api(lang):
    url = "http://127.0.0.1:8000/api/shows/"
    headers = {"Accept-Language": lang}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data:
                show = data[0]
                print(f"[{lang}] Title: {show.get('title')}")
                # print(f"[{lang}] Keys: {list(show.keys())}")
        else:
            print(f"Error {response.status_code}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Note: This requires the server to be running on 127.0.0.1:8000
    # Since I cannot start the server and keep it running while running this script easily,
    # I will try to use the Django shell to test the serializer directly.
    pass
