import requests
import json
from django.shortcuts import render, get_object_or_404, redirect
from catalogue.models.location import Location
from catalogue.models.representation import Representation
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings

def home(request):
    """
    View for the home page, fetching show data and press articles from the API.
    """
    base_url = request.build_absolute_uri('/')[:-1]
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    
    # Fetch 8 next shows
    api_url_shows = f"{base_url}/api/shows/?ordering=next_date&page=1"
    shows_data = []
    try:
        response = requests.get(api_url_shows, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            shows_data = data['results']
        else:
            shows_data = data
    except Exception as e:
        print(f"Error fetching shows for home page: {e}")

    # Fetch 4 latest press articles
    api_url_press = f"{base_url}/api/press-articles/?page=1"
    press_data = []
    try:
        response = requests.get(api_url_press, headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'results' in data:
            press_data = data['results']
        else:
            press_data = data
    except Exception as e:
        print(f"Error fetching press articles for home page: {e}")

    context = {
        'shows': shows_data,
        'press_articles': press_data,
        'page_title': _('Bienvenue à ThéâtrePlus'),
    }
    return render(request, 'home.html', context)

def show_list(request):
    """
    View for displaying a list of shows fetched from the API with pagination and search.
    """
    page_num = request.GET.get('page', 1)
    search_query = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    
    base_url = request.build_absolute_uri('/')[:-1]
    
    # Build API URL with parameters
    api_url = f"{base_url}/api/shows/?page={page_num}"
    if search_query:
        api_url += f"&search={search_query}"
    if genre_id:
        api_url += f"&genre={genre_id}"
        
    headers = {'Accept-Language': request.LANGUAGE_CODE}
    
    shows_data = []
    pagination_data = {}
    genres_data = []
    
    # Fetch genres for the search form
    try:
        genres_response = requests.get(f"{base_url}/api/genres/", headers=headers)
        if genres_response.status_code == 200:
            genres_data = genres_response.json()
    except Exception as e:
        print(f"Error fetching genres: {e}")

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
        'genres': genres_data,
        'search_query': search_query,
        'selected_genre': genre_id,
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

def contact(request):
    """
    View for the contact page.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            full_message = f"Message de: {name} <{email}>\n\nSujet: {subject}\n\n{message}"
            
            try:
                send_mail(
                    f"[Contact ThéâtrePlus] {subject}",
                    full_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL], # Send to our own email
                    fail_silently=False,
                )
                messages.success(request, _("Votre message a été envoyé avec succès. Nous vous répondrons dès que possible."))
                return redirect('frontend:home')
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, _("Une erreur est survenue lors de l'envoi de votre message. Veuillez réessayer plus tard."))
    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'page_title': _('Contactez-nous'),
    }
    return render(request, 'contact.html', context)

