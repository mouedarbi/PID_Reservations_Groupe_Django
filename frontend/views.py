import requests
from django.shortcuts import render

def home(request):
    """
    View for the home page.
    """
    return render(request, 'home.html')

def show_list(request):
    """
    View for displaying a list of shows fetched from the API.
    """
    api_url = "http://127.0.0.1:8000/api/shows/"  # Adjust if API runs on a different port/host
    shows_data = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        shows_data = response.json()
    except requests.exceptions.RequestException as e:
        # Handle API request errors (e.g., connection refused, 404, 500)
        print(f"Error fetching shows from API: {e}")
        # Optionally, pass an error message to the template
        # return render(request, 'show_list.html', {'error_message': 'Could not fetch shows.'})

    context = {
        'shows': shows_data,
        'page_title': 'Catalogue des Spectacles',
    }
    return render(request, 'show_list.html', context)

