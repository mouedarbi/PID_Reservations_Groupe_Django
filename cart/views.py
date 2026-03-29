from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalogue.models import Representation, Price
from .cart import Cart

from django.contrib import messages

@require_POST
def cart_add(request, representation_id):
    """
    Vue pour ajouter une représentation au panier avec un prix spécifique.
    """
    cart = Cart(request)
    representation = get_object_or_404(Representation, id=representation_id)
    
    price_id = request.POST.get('price_id')
    quantity = int(request.POST.get('quantity', 1))
    
    price = get_object_or_404(Price, id=price_id)
    
    # Vérification des places disponibles
    if quantity > representation.available_seats:
        messages.error(request, f"Désolé, il ne reste que {representation.available_seats} places disponibles.")
        return redirect('catalogue:representation-show', pk=representation.id)

    # Vérification : le prix appartient-il bien au spectacle de cette représentation ?
    if price in representation.show.prices.all():
        cart.add(representation=representation,
                 price=price,
                 quantity=quantity)
        messages.success(request, f"Ajouté au panier : {quantity} x {price.type} pour {representation.show.title}")
    
    return redirect('cart:cart_detail')

def cart_remove(request, representation_id, price_id):
    """
    Supprimer un article spécifique (Combinaison Séance/Prix) du panier.
    """
    cart = Cart(request)
    representation = get_object_or_404(Representation, id=representation_id)
    price = get_object_or_404(Price, id=price_id)
    cart.remove(representation, price)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """
    Afficher le contenu du panier.
    """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
