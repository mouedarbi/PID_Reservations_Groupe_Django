from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import Http404

from catalogue.models.price import Price
from ..serializers.prices import PriceSerializer

class PricesView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]
    """
    List all prices, or create a new price.
    """
    def get(self, request, format=None):
        prices = Price.objects.all()
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PricesDetailView(APIView):
    permission_classes = [permissions.IsAdminUser]
    """
    Retrieve, update or delete a price instance.
    """
    def get_object(self, id):
        try:
            return Price.objects.get(id=id)
        except Price.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        price = self.get_object(id)
        serializer = PriceSerializer(price)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        price = self.get_object(id)
        serializer = PriceSerializer(price, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        price = self.get_object(id)
        price.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
