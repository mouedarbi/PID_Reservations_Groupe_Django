from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages #chapitre 3


from catalogue.forms.ArtistForm import ArtistForm
from catalogue.models import Artist
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


# Create your views here.
def index(request):
	artists = Artist.objects.all()
	
	return render(request, 'artist/index.html', {
		'artists':artists,
	})

def show(request, artist_id):
	try:
		artist = Artist.objects.get(id=artist_id)
	except Artist.DoesNotExist:
		raise Http404('Artist inexistant');
		
	return render(request, 'artist/show.html', {
		'artist':artist,
	})

@login_required
@permission_required('catalogue.change_artist', raise_exception=True)
def edit(request, artist_id):
    # fetch the object related to passed id
    artist = get_object_or_404(Artist, id=artist_id)

    # pass the object as instance in form
    form = ArtistForm(request.POST or None, instance=artist)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Artiste modifié avec succès.")

            return redirect('catalogue:artist-show', artist.id)
        else:
            messages.add_message(request, messages.ERROR, "Échec de la modification de l'artiste.")
    return render(request, 'artist/edit.html', {
        'form': form,
        'artist': artist,
    })


@login_required
@permission_required('catalogue.add_artist', raise_exception=True)
def create (request):
    form = ArtistForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, "Nouvel artiste créer avec succès.")

        return redirect('catalogue:artist-index')
    else :
        messages.add_message(request, messages.ERROR, "Echec de l'ajout d'un nouvel artiste !")

    return render(request, 'artist/create.html', {'form' : form,})

@login_required
@permission_required('catalogue.delete_artist', raise_exception=True)
def delete(request, artist_id):
    artist = get_object_or_404(Artist, id =artist_id)
    if request.method =="POST":
        artist.delete()
        messages.add_message(request, messages.SUCCESS, "Artiste supprimer avec succès.")

        return redirect('catalogue:artist-index')
    messages.add_message(request, messages.ERROR, "Échec de la suppression de l'artiste !")
    return render(request, 'artist/show.html', {'artist': artist,})