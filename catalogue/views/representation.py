from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from catalogue.models import Representation
from catalogue.forms.RepresentationForm import RepresentationForm

def index(request):
    representations = Representation.objects.all()
    title = 'Liste des représentations'
    return render(request, 'representation/index.html', {'representations': representations, 'title': title})

def show(request, representation_id):
    try:
        representation = Representation.objects.get(id=representation_id)
    except Representation.DoesNotExist:
        raise Http404('Représentation inexistante')
        
    title = "Fiche d'une représentation"
    rep_date = representation.schedule.strftime('%Y-%m-%d')
    rep_time = representation.schedule.strftime('%H:%M')
    
    return render(request, 'representation/show.html', {
        'representation': representation,
        'title': title,
        'rep_date': rep_date,
        'rep_time': rep_time,
    })

@login_required
@permission_required('catalogue.add_representation', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = RepresentationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Représentation créée avec succès.")
            return redirect('catalogue:representation-index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = RepresentationForm()

    return render(request, 'representation/create.html', {'form': form})

@login_required
@permission_required('catalogue.change_representation', raise_exception=True)
def edit(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)

    if request.method == 'POST':
        form = RepresentationForm(request.POST, instance=representation)
        if form.is_valid():
            form.save()
            messages.success(request, "Représentation modifiée avec succès.")
            return redirect('catalogue:representation-show', representation.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = RepresentationForm(instance=representation)

    return render(request, 'representation/edit.html', {'form': form, 'representation': representation})

@login_required
@permission_required('catalogue.delete_representation', raise_exception=True)
def delete(request, representation_id):
    representation = get_object_or_404(Representation, id=representation_id)

    if request.method == 'POST':
        representation.delete()
        messages.success(request, "Représentation supprimée avec succès.")
        return redirect('catalogue:representation-index')
    
    return redirect('catalogue:representation-show', representation.id)
