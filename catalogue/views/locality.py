from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from catalogue.models import Locality
from catalogue.forms.LocalityForm import LocalityForm

def index(request):
    localities = Locality.objects.all()
    title = 'Liste des localitées'
    return render(request, 'locality/index.html', {'localities': localities, 'title': title})

def show(request, locality_id):
    try:
        locality = Locality.objects.get(id=locality_id)
    except Locality.DoesNotExist:
        raise Http404('Localité inexistante')
    
    title = 'Fiche d\'une localité'
    return render(request, 'locality/show.html', {'locality': locality, 'title': title})

@login_required
@permission_required('catalogue.add_locality', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = LocalityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Localité créée avec succès.")
            return redirect('catalogue:locality-index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = LocalityForm()

    return render(request, 'locality/create.html', {'form': form})

@login_required
@permission_required('catalogue.change_locality', raise_exception=True)
def edit(request, locality_id):
    locality = get_object_or_404(Locality, id=locality_id)

    if request.method == 'POST':
        form = LocalityForm(request.POST, instance=locality)
        if form.is_valid():
            form.save()
            messages.success(request, "Localité modifiée avec succès.")
            return redirect('catalogue:locality-show', locality.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = LocalityForm(instance=locality)

    return render(request, 'locality/edit.html', {'form': form, 'locality': locality})

@login_required
@permission_required('catalogue.delete_locality', raise_exception=True)
def delete(request, locality_id):
    locality = get_object_or_404(Locality, id=locality_id)

    if request.method == 'POST':
        locality.delete()
        messages.success(request, "Localité supprimée avec succès.")
        return redirect('catalogue:locality-index')
    
    return redirect('catalogue:locality-show', locality.id)
