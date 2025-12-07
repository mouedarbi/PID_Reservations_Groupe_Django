from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from catalogue.models import Show
from catalogue.forms.ShowForm import ShowForm

def index(request):
    shows = Show.objects.all()
    title = 'Liste des spectacles'
    return render(request, 'show/index.html', {'shows': shows, 'title': title})

def show(request, show_id):
    try:
        show = Show.objects.get(id=show_id)
    except Show.DoesNotExist:
        raise Http404('Spectacle inexistant')
        
    title = "Fiche d'un spectacle"
    return render(request, 'show/show.html', {'show': show, 'title': title})

@login_required
@permission_required('catalogue.add_show', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Spectacle créé avec succès.")
            return redirect('catalogue:show-index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ShowForm()

    return render(request, 'show/create.html', {'form': form})

@login_required
@permission_required('catalogue.change_show', raise_exception=True)
def edit(request, show_id):
    show_instance = get_object_or_404(Show, id=show_id)

    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Spectacle modifié avec succès.")
            return redirect('catalogue:show-show', show_id=show_instance.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ShowForm(instance=show_instance)

    return render(request, 'show/edit.html', {'form': form, 'show': show_instance})

@login_required
@permission_required('catalogue.delete_show', raise_exception=True)
def delete(request, show_id):
    show_instance = get_object_or_404(Show, id=show_id)

    if request.method == 'POST':
        show_instance.delete()
        messages.success(request, "Spectacle supprimé avec succès.")
        return redirect('catalogue:show-index')
    
    return redirect('catalogue:show-show', show_id=show_instance.id)
