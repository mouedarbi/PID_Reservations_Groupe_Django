from django.shortcuts import render
from django.http import Http404

from catalogue.models import Locality

def index (request):
    localities = Locality.objects.all()
    title = 'Liste des localitées'

    return render (request, 'locality/index.html', {'localities' : localities, 'title' : title})

def show(request, locality_id):
    try:
        locality = Locality.objects.get(id=locality_id)
    except Locality.DoesNotExist:
        raise Http404

    title = "Fiche d\'un code postal"

    return render (request, 'locality/show.html', {'locality' : locality, 'title' : title})

