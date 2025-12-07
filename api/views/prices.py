from rest_framework import generics
from catalogue.models.price import Price
from api.serializers.prices import PriceSerializer


class PricesView(generics.ListCreateAPIView):
    """
    GET  /api/prices/  -> liste des prix
    POST /api/prices/  -> créer un prix
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer


class PricesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/prices/<id>/ -> détail d'un prix
    PUT    /api/prices/<id>/ -> modifier un prix
    DELETE /api/prices/<id>/ -> supprimer un prix
    """
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
