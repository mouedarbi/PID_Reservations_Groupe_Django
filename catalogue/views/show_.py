from django.shortcuts import render
from django.http import Http404

from catalogue.models import Show

def index(request):
    shows = Show.objects.all()
    title = 'Liste des spectacles'
    
    return render(request, 'show/index.html', {
        'shows':shows,
        'title':title
    })

def show(request, show_id):
    try:
        show = Show.objects.get(id=show_id)
    except Show.DoesNotExist:
        raise Http404('Spectacle inexistant');
        
    title = "Fiche d'un spectacle"
    
    return render(request, 'show/show.html', {
        'show':show,
        'title':title 
    })
