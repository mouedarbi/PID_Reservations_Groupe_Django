from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import Http404

from catalogue.models.location import Location
from ..serializers.locations import LocationSerializer


class LocationsView(APIView):
    """
    List all locations (public) or create a new location (superuser only).
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        queryset = Location.objects.all()
        # Filtrage optionnel par locality_id
        locality_id = request.query_params.get('locality_id')
        if locality_id:
            queryset = queryset.filter(locality_id=locality_id)
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Vérification si l'utilisateur est superuser
        if not request.user.is_superuser:
            return Response(
                {"detail": "Vous n'avez pas la permission d'effectuer cette action."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationsDetailView(APIView):
    """
    Retrieve, update, or delete a location instance.
    GET is public.
    PUT, PATCH, DELETE are restricted to superuser.
    """

    def get_object(self, id):
        try:
            return Location.objects.get(id=id)
        except Location.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        location = self.get_object(id)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Vous n'avez pas la permission d'effectuer cette action."},
                status=status.HTTP_403_FORBIDDEN
            )
        location = self.get_object(id)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, format=None):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Vous n'avez pas la permission d'effectuer cette action."},
                status=status.HTTP_403_FORBIDDEN
            )
        location = self.get_object(id)
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        if not request.user.is_superuser:
            return Response(
                {"detail": "Vous n'avez pas la permission d'effectuer cette action."},
                status=status.HTTP_403_FORBIDDEN
            )
        location = self.get_object(id)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
