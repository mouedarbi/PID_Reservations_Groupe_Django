from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required

from catalogue.models import Price
from catalogue.forms.PriceForm import PriceForm

def index(request):
    prices = Price.objects.all()
    title = 'Liste des Prix'
    return render(request, 'price/index.html', {'prices': prices, 'title': title})

def show(request, price_id):
    try:
        price = Price.objects.get(id=price_id)
    except Price.DoesNotExist:
        raise Http404('Prix inexistant')
    
    title = 'Fiche d\'un prix'
    return render(request, 'price/show.html', {'price': price, 'title': title})

@login_required
@permission_required('catalogue.add_price', raise_exception=True)
def create(request):
    if request.method == 'POST':
        form = PriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Prix créé avec succès.")
            return redirect('catalogue:price-index')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PriceForm()

    return render(request, 'price/create.html', {'form': form})

@login_required
@permission_required('catalogue.change_price', raise_exception=True)
def edit(request, price_id):
    price = get_object_or_404(Price, id=price_id)

    if request.method == 'POST':
        form = PriceForm(request.POST, instance=price)
        if form.is_valid():
            form.save()
            messages.success(request, "Prix modifié avec succès.")
            return redirect('catalogue:price-show', price.id)
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = PriceForm(instance=price)

    return render(request, 'price/edit.html', {'form': form, 'price': price})

@login_required
@permission_required('catalogue.delete_price', raise_exception=True)
def delete(request, price_id):
    price = get_object_or_404(Price, id=price_id)

    if request.method == 'POST':
        price.delete()
        messages.success(request, "Prix supprimé avec succès.")
        return redirect('catalogue:price-index')
    
    return redirect('catalogue:price-show', price.id)