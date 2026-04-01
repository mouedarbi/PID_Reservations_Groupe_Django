from decimal import Decimal
from django.conf import settings
from catalogue.models import Representation, Price

class Cart:
    def __init__(self, request):
        """
        Initialisation du panier.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Sauvegarder un panier vide dans la session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, representation, price, quantity=1, override_quantity=False):
        """
        Ajouter une représentation au panier ou mettre à jour sa quantité.
        On utilise une clé composée : 'repID_priceID'
        """
        item_id = f"{representation.id}_{price.id}"
        
        if item_id not in self.cart:
            self.cart[item_id] = {
                'representation_id': representation.id,
                'price_id': price.id,
                'quantity': 0,
                'price': str(price.price) # Stocké en string pour le JSON
            }
        
        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
            
        self.save()

    def save(self):
        # Marquer la session comme "modifiée" pour s'assurer qu'elle soit enregistrée
        self.session.modified = True

    def remove(self, representation, price):
        """
        Supprimer un article du panier.
        """
        item_id = f"{representation.id}_{price.id}"
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        """
        Boucle sur les articles du panier et récupération des objets de la DB.
        """
        # On crée une liste des clés pour pouvoir modifier le dictionnaire pendant l'itération si besoin
        item_ids = list(self.cart.keys())
        
        for item_id in item_ids:
            item = self.cart.get(item_id)
            if not item:
                continue
                
            try:
                # Vérification des clés essentielles
                if 'representation_id' not in item or 'price_id' not in item or 'price' not in item or 'quantity' not in item:
                    raise KeyError("Clés manquantes dans l'article du panier")

                # Tentative de récupération des objets réels en DB
                item['representation'] = Representation.objects.get(id=item['representation_id'])
                item['price_obj'] = Price.objects.get(id=item['price_id'])
                item['total_price'] = Decimal(item['price']) * item['quantity']
                yield item
            except (Representation.DoesNotExist, Price.DoesNotExist, KeyError, TypeError):
                # Si l'objet n'existe plus en DB ou données corrompues, on le retire
                self.remove_by_id(item_id)

    def remove_by_id(self, item_id):
        """
        Supprimer un article du panier par sa clé 'repID_priceID'.
        """
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __len__(self):
        """
        Compter le nombre total de tickets dans le panier.
        Ignore les articles corrompus.
        """
        count = 0
        item_ids = list(self.cart.keys())
        for item_id in item_ids:
            item = self.cart[item_id]
            try:
                count += item['quantity']
            except (KeyError, TypeError):
                self.remove_by_id(item_id)
        return count

    def get_total_price(self):
        """
        Calculer le montant total du panier.
        Ignore les articles corrompus.
        """
        total = Decimal('0')
        item_ids = list(self.cart.keys())
        for item_id in item_ids:
            item = self.cart[item_id]
            try:
                total += Decimal(item['price']) * item['quantity']
            except (KeyError, TypeError, Decimal.InvalidOperation):
                self.remove_by_id(item_id)
        return total

    def clear(self):
        """
        Vider le panier de la session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
