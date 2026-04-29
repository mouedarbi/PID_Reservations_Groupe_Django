import requests
import json
from django.shortcuts import render, get_object_or_404
from catalogue.models.location import Location
from catalogue.models.representation import Representation
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

def home(request):
    """
    View for the home page, fetching show data from the API.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/shows/"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    shows_data = []
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        shows_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching shows for home page from API: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from API: {e}")
        print(f"Response text: {response.text}")


    context = {
        'shows': shows_data,
        'page_title': _('Bienvenue à ThéâtrePlus'),
    }
    return render(request, 'home.html', context)

def show_list(request):
    """
    View for displaying a list of shows fetched from the API.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/shows/"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    shows_data = []
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        shows_data = response.json()
    except requests.exceptions.RequestException as e:
        # Handle API request errors (e.g., connection refused, 404, 500)
        print(f"Error fetching shows from API: {e}")
        # Optionally, pass an error message to the template
        # return render(request, 'show_list.html', {'error_message': 'Could not fetch shows.'})

    context = {
        'shows': shows_data,
        'page_title': _('Catalogue des Spectacles'),
    }
    return render(request, 'show_list.html', context)

def show_detail(request, pk):
    """
    View for displaying details of a single show fetched from the API.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/shows/{pk}/"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    show_data = None
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        show_data = response.json()
        print(f"DEBUG: Show data for ID {pk}: {list(show_data.keys())}")
        print(f"DEBUG: Representations count: {len(show_data.get('representations', []))}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching show detail from API: {e}")

    context = {
        'show': show_data,
        'page_title': show_data.get('title', _('Détails du Spectacle')) if show_data else _('Spectacle introuvable'),
    }
    return render(request, 'show_detail.html', context)

def location_list(request):
    """
    View for displaying a list of locations fetched from the API.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/locations/"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    locations_data = []
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        locations_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching locations from API: {e}")

    context = {
        'locations': locations_data,
        'page_title': _('Nos Lieux de Spectacles'),
    }
    return render(request, 'location_list.html', context)

def location_detail(request, pk):
    """
    View for displaying details of a single location and its next representation.
    """
    location = get_object_or_404(Location, pk=pk)
    
    # Get the next representation for this location
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

def about(request):
    """
    View for the about page.
    """
    context = {
        'page_title': _('À propos de ThéâtrePlus'),
    }
    return render(request, 'about.html', context)

