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
        item_ids = self.cart.keys()
        # On pourrait optimiser ici avec des requêtes groupées si nécessaire
        
        cart_copy = self.cart.copy()
        
        for item_id in item_ids:
            item = cart_copy[item_id]
            item['representation'] = Representation.objects.get(id=item['representation_id'])
            item['price_obj'] = Price.objects.get(id=item['price_id'])
            item['total_price'] = Decimal(item['price']) * item['quantity']
            yield item

    def __len__(self):
        """
        Compter le nombre total de tickets dans le panier.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Calculer le montant total du panier.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Vider le panier de la session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
