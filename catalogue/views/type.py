from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from catalogue.models import Type
from catalogue.forms.TypeForm import TypeForm

def index(request):
    types = Type.objects.all()
    title = 'Liste des types'
    return render(request, 'type/index.html', {'types': types, 'title': title})

def show(request, type_id):
    try:
        type_instance = Type.objects.get(id=type_id)
    except Type.DoesNotExist:
        raise Http404('Type inexistant')
    
    title = "Fiche d\'un type"
    return render(request, 'type/show.html', {'type': type_instance, 'title': title})

@login_required
@permission_required('catalogue.add_type', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = TypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Type créé avec succès.")
            return redirect('catalogue:type-index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = TypeForm()

    return render(request, 'type/create.html', {'form': form})

@login_required
@permission_required('catalogue.change_type', raise_exception=True)
def edit(request, type_id):
    type_instance = get_object_or_404(Type, id=type_id)

    if request.method == 'POST':
        form = TypeForm(request.POST, instance=type_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Type modifié avec succès.")
            return redirect('catalogue:type-show', type_instance.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = TypeForm(instance=type_instance)

    return render(request, 'type/edit.html', {'form': form, 'type': type_instance})

@login_required
@permission_required('catalogue.delete_type', raise_exception=True)
def delete(request, type_id):
    type_instance = get_object_or_404(Type, id=type_id)

    if request.method == 'POST':
        type_instance.delete()
        messages.success(request, "Type supprimé avec succès.")
        return redirect('catalogue:type-index')
    
    return redirect('catalogue:type-show', type_instance.id)
