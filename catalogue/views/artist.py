from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from catalogue.forms.ArtistForm import ArtistForm
from catalogue.models import Artist



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


def edit(request, artist_id):
    # fetch the object related to passed id
    artist = Artist.objects.get(id=artist_id)

    # pass the object as instance in form
    form = ArtistForm(request.POST or None, instance=artist)

    if request.method == 'POST':
        method = request.POST.get('_method', '').upper()

        if method == 'PUT':
            # save the data from the form and
            # redirect to detail_view
            if form.is_valid():
                form.save()

                return render(request, "artist/show.html", {
                    'artist': artist,
                })

    return render(request, 'artist/edit.html', {
        'form': form,
        'artist': artist,
    })


def create (request):
    form = ArtistForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()

        return redirect('catalogue:artist-index')
    return render(request, 'artist/create.html', {'form' : form,})

def delete(request, artist_id):
    artist = get_object_or_404(Artist, id =artist_id)
    if request.method =="POST":
        method = request.POST.get('_method', '').upper()
        if method =='DELETE':
            artist.delete()

            return redirect('catalogue:artist-index')
    return render(request, 'artist/show.html', {'artist': artist,})