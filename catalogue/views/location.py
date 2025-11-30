from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from catalogue.models import Location
from catalogue.forms.LocationForm import LocationForm

def index(request):
    locations = Location.objects.all()
    title = 'Liste des lieux de spectacle'
    return render(request, 'location/index.html', {'locations': locations, 'title': title})

def show(request, location_id):
    try:
        location = Location.objects.get(id=location_id)
    except Location.DoesNotExist:
        raise Http404('Lieu inexistant')
    
    title = 'Fiche d\'un lieu de spectacle'
    return render(request, 'location/show.html', {'location': location, 'title': title})

@login_required
@permission_required('catalogue.add_location', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lieu créé avec succès.")
            return redirect('catalogue:location-index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = LocationForm()

    return render(request, 'location/create.html', {'form': form})

@login_required
@permission_required('catalogue.change_location', raise_exception=True)
def edit(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, "Lieu modifié avec succès.")
            return redirect('catalogue:location-show', location.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = LocationForm(instance=location)

    return render(request, 'location/edit.html', {'form': form, 'location': location})

@login_required
@permission_required('catalogue.delete_location', raise_exception=True)
def delete(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    if request.method == 'POST':
        location.delete()
        messages.success(request, "Lieu supprimé avec succès.")
        return redirect('catalogue:location-index')
    
    return redirect('catalogue:location-show', location.id)
