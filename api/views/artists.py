from rest_framework.response import Response
from rest_framework.views import APIView
from catalogue.models import Artist
from api.serializers.artists import ArtistSerializer

class ArtistsView(APIView):
    def get(self, request, *args, **kwargs):
        artists = Artist.objects.all()
        serializer = ArtistSerializer(artists, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)
    
    def delete(self, request, *args, **kwargs):
        return Response({"detail": "Placeholder"}, status=501)


class ArtistsDetailView(APIView):
    def get(self, request, pk, *args, **kwargs):
        try:
            artist = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response({"error": "Artist not found"}, status=404)
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        try:
            artist = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response({"error": "Artist not found"}, status=404)
        serializer = ArtistSerializer(artist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        try:
            artist = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response({"error": "Artist not found"}, status=404)
        artist.delete()
        return Response(status=204)
