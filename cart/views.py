from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from catalogue.models import Representation, Price
from .cart import Cart

from django.contrib import messages

from django.utils.translation import gettext as _

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
        messages.error(request, _("Désolé, il ne reste que %(seats)s places disponibles.") % {'seats': representation.available_seats})
        return redirect('catalogue:representation-show', pk=representation.id)

    # Vérification : le prix appartient-il bien au spectacle de cette représentation ?
    if price in representation.show.prices.all():
        cart.add(representation=representation,
                 price=price,
                 quantity=quantity)
        messages.success(request, _("Ajouté : %(qty)s x %(type)s. Vous pouvez continuer vos achats ou aller au panier.") % {'qty': quantity, 'type': price.type})
    
    # Rediriger vers la page précédente (la séance) au lieu du panier
    return redirect('catalogue:representation-show', representation_id=representation.id)

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

from django.contrib.auth.decorators import login_required
from catalogue.models import Reservation, RepresentationReservation

@login_required
def cart_checkout(request):
    """
    Vue pour valider le panier et créer des réservations séparées par séance.
    """
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, _("Votre panier est vide."))
        return redirect('catalogue:show-index')

    if request.method == 'POST':
        # On ne crée plus les réservations ici car elles sont créées par Stripe lors du succès du paiement
        # Redirection vers Stripe via le template
        return redirect('cart:cart_detail')

    return render(request, 'cart/checkout.html', {'cart': cart})

@login_required
def reservation_detail(request, reservation_id):
    """
    Afficher les détails d'une réservation spécifique (style facture/billet).
    """
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    # Calculer le total de la réservation
    total = sum(rr.quantity * rr.price.price for rr in reservation.representation_reservations.all())
    
    return render(request, 'cart/reservation_detail.html', {
        'reservation': reservation,
        'total': total
    })
