import requests
import json
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from catalogue.models import Location, Representation

def home(request):
    """
    View for the home page, fetching show data from the API.
    """
    api_url = "http://127.0.0.1:8000/api/shows/"
    shows_data = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        shows_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching shows for home page from API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API: {e}")
        print(f"Response text: {response.text}")


    context = {
        'shows': shows_data,
        'page_title': 'Bienvenue à ThéâtrePlus',
    }
    return render(request, 'home.html', context)

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

def location_list(request):
    """
    View for displaying a list of locations fetched from the API.
    """
    api_url = "http://127.0.0.1:8000/api/locations/"
    locations_data = []
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        locations_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching locations from API: {e}")

    context = {
        'locations': locations_data,
        'page_title': 'Nos Lieux de Spectacles',
    }
    return render(request, 'location_list.html', context)


def location_detail(request, slug):
    """
    View for displaying the details of a single location, including the next upcoming show.
    """
    location = get_object_or_404(Location, slug=slug)
    
    # Find the next upcoming representation at this location
    next_representation = Representation.objects.filter(
        location=location,
        schedule__gte=timezone.now()
    ).order_by('schedule').first()

    context = {
        'location': location,
        'next_representation': next_representation,
        'page_title': location.designation or location.slug,
    }
    return render(request, 'location_detail.html', context)


def about_us(request):
    """
    View for the About Us page.
    """
    context = {
        'page_title': 'À propos de ThéâtrePlus',
    }
    return render(request, 'about.html', context)



