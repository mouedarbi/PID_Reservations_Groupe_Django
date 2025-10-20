from django.shortcuts import render
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
    artist = Artist.objects.get(id=artist_id)

    form = ArtistForm(request.POST or None, instance =artist)
    if request.method =='POST':
        if form.is_valid():
            form.save()

            return render(request, "artist/show.html", {'artist' : artist,})

    return render(request, 'artist/edit.html', { 'form' : form, 'artist' : artist,})

