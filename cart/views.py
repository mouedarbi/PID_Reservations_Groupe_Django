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
        messages.success(request, f"Ajouté : {quantity} x {price.type}. Vous pouvez continuer vos achats ou aller au panier.")
    
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
        messages.error(request, "Votre panier est vide.")
        return redirect('catalogue:show-index')

    if request.method == 'POST':
        # SÉCURITÉ : On supprime les anciennes réservations 'PENDING' de l'utilisateur
        # pour éviter les doublons en cas de rafraîchissement de page ou retour arrière.
        Reservation.objects.filter(user=request.user, status='PENDING').delete()

        # On groupe les articles du panier par représentation
        items_by_rep = {}
        for item in cart:
            rep_id = item['representation'].id
            if rep_id not in items_by_rep:
                items_by_rep[rep_id] = []
            items_by_rep[rep_id].append(item)

        created_reservation_ids = []

        # Pour chaque séance, on crée une réservation distincte
        for rep_id, items in items_by_rep.items():
            reservation = Reservation.objects.create(
                user=request.user,
                status='PENDING'
            )
            created_reservation_ids.append(str(reservation.id))

            for item in items:
                RepresentationReservation.objects.create(
                    reservation=reservation,
                    representation=item['representation'],
                    price=item['price_obj'],
                    quantity=item['quantity']
                )
        
        # On passe la liste des IDs à la simulation de paiement (séparés par des virgules)
        ids_str = ",".join(created_reservation_ids)
        return redirect(f"/cart/payment/{ids_str}/")

    return render(request, 'cart/checkout.html', {'cart': cart})

def payment_simulation(request, reservation_id):
    """
    Vue pour simuler le paiement d'une ou plusieurs réservations.
    Note : reservation_id peut être une chaîne d'IDs séparés par des virgules.
    """
    # On gère le cas multi-réservations
    id_list = str(reservation_id).split(',')
    reservations = Reservation.objects.filter(id__in=id_list, user=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'success':
            for reservation in reservations:
                reservation.status = 'PAID'
                reservation.save()
                
                # Mise à jour des stocks
                for rr in reservation.representation_reservations.all():
                    rr.representation.available_seats -= rr.quantity
                    rr.representation.save()
            
            cart = Cart(request)
            cart.clear()
            messages.success(request, f"Paiement réussi ! {reservations.count()} réservation(s) validée(s).")
            return redirect('accounts:user-profile')
            
        elif action == 'failure':
            for reservation in reservations:
                reservation.status = 'FAILED'
                reservation.save()
            messages.error(request, "Le paiement a échoué.")
            return redirect('cart:cart_detail')

    return render(request, 'cart/payment_simulation.html', {
        'reservations': reservations,
        'is_multiple': len(id_list) > 1
    })

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
