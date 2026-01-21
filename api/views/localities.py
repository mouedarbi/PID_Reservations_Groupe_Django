from rest_framework import generics
from catalogue.models.locality import Locality
from ..serializers.localities import LocalitySerializer


class LocalitiesView(generics.ListAPIView):
    """
    API view to retrieve a list of localities.
    """
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer


class LocalitiesDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single locality.
    """
    queryset = Locality.objects.all()
    serializer_class = LocalitySerializer
