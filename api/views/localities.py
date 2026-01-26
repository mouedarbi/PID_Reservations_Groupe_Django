from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAdminUser

from catalogue.models.locality import Locality
from ..serializers.localities import LocalitySerializer


class LocalitiesView(APIView):
    """
    LIST  (GET)  : Public
    CREATE (POST): Admin uniquement
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get(self, request, format=None):
        localities = Locality.objects.all()
        serializer = LocalitySerializer(localities, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = LocalitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocalitiesDetailView(APIView):
    """
    DETAIL (GET) : Public
    UPDATE / DELETE : Admin uniquement
    """
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def get_object(self, id):
        try:
            return Locality.objects.get(id=id)
        except Locality.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        locality = self.get_object(id)
        serializer = LocalitySerializer(locality)
        return Response(serializer.data)

    def put(self, request, id, format=None):
        locality = self.get_object(id)
        serializer = LocalitySerializer(locality, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id, format=None):
        locality = self.get_object(id)
        serializer = LocalitySerializer(locality, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        locality = self.get_object(id)
        locality.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)