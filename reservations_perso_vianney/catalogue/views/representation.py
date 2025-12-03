from django.shortcuts import render
from django.http import Http404

from catalogue.models import Representation


def index(request):
    representations = Representation.objects.all()
    title = 'Liste des représentations'

    return render(request, 'representation/index.html', {
        'representations': representations,
        'title': title
    })


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
