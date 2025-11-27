from django.shortcuts import render
from django.http import Http404

from catalogue.models import Location

def index(request):
    locations = Location.objects.all()
    title = 'Liste des lieux de spectacle'
    
    return render(request, 'location/index.html', {
        'locations':locations,
        'title':title
    })

def show(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        raise Http404('Lieu inexistant');
        
    title = "Fiche d'un lieu de spectacle"
    
    return render(request, 'location/show.html', {
        'location':location,
        'title':title 
    })
