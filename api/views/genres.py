from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from catalogue.models import Genre
from api.serializers.genres import GenreSerializer

class GenresView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, *args, **kwargs):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data)
