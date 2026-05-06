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
        data = response.json()
        
        # Handle paginated response
        if isinstance(data, dict) and 'results' in data:
            shows_data = data['results'][:4] # Limit to 4 shows for home page
        else:
            shows_data = data
            
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
    View for displaying a list of shows fetched from the API with pagination.
    """
    page_num = request.GET.get('page', 1)
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/shows/?page={page_num}"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    
    shows_data = []
    pagination_data = {}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict) and 'results' in data:
            shows_data = data['results']
            count = data.get('count', 0)
            page_size = 8  # Doit correspondre à PAGE_SIZE dans settings.py
            total_pages = (count + page_size - 1) // page_size if count > 0 else 1
            
            pagination_data = {
                'count': count,
                'next': data.get('next'),
                'previous': data.get('previous'),
                'current_page': int(page_num),
                'total_pages': total_pages,
            }
        else:
            shows_data = data
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching shows from API: {e}")

    context = {
        'shows': shows_data,
        'pagination': pagination_data,
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

def press_article_list(request):
    """
    View for displaying a list of press articles with pagination.
    """
    page_num = request.GET.get('page', 1)
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/press-articles/?page={page_num}"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    
    articles_data = []
    pagination_data = {}
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict) and 'results' in data:
            articles_data = data['results']
            count = data.get('count', 0)
            page_size = 4
            total_pages = (count + page_size - 1) // page_size if count > 0 else 1
            
            pagination_data = {
                'count': count,
                'next': data.get('next'),
                'previous': data.get('previous'),
                'current_page': int(page_num),
                'total_pages': total_pages,
            }
        else:
            articles_data = data
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching articles from API: {e}")

    context = {
        'articles': articles_data,
        'pagination': pagination_data,
        'page_title': _('Articles de Presse'),
    }
    return render(request, 'press_article_list.html', context)

def press_article_detail(request, pk):
    """
    View for displaying a full press article.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    api_url = f"{base_url}/api/press-articles/{pk}/"
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    article_data = None
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        article_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article detail from API: {e}")

    context = {
        'article': article_data,
        'page_title': article_data.get('title', _('Article de Presse')) if article_data else _('Article introuvable'),
    }
    return render(request, 'press_article_detail.html', context)

