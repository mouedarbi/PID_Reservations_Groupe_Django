from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAdminUser

from catalogue.models.location import Location
from ..serializers.locations import LocationSerializer


class LocationsView(APIView):
    """
    LIST  (GET)  : Public
    CREATE (POST): Admin uniquement
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, format=None):
        locations = Location.objects.all()

        locality_id = request.query_params.get('locality_id')
        if locality_id:
            locations = locations.filter(locality_id=locality_id)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationsDetailView(APIView):
    """
    DETAIL (GET) : Public
    UPDATE / DELETE : Admin uniquement
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_object(self, pk):
        try:
            return Location.objects.get(id=pk)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        location = self.get_object(pk)
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        location = self.get_object(pk)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)