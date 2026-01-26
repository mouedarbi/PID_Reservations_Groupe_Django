from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from catalogue.models.artist_type import ArtistType
from api.serializers.artist_types import ArtistTypeSerializer

# Optionnel : permission custom
try:
    from api.catalogue.permissions import IsAuthenticatedOrReadOnly
    DEFAULT_PERMS = [IsAuthenticatedOrReadOnly]
except Exception:
    DEFAULT_PERMS = []

class ArtistTypesView(APIView):
    permission_classes = DEFAULT_PERMS

    def get(self, request, *args, **kwargs):
        qs = ArtistType.objects.all()
        serializer = ArtistTypeSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Body attendu:
        {"artist": <artist_id>, "type": <type_id>}
        """
        serializer = ArtistTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Body attendu:
        {"artist": <artist_id>, "type": <type_id>}
        """
        artist_id = request.data.get("artist")
        type_id = request.data.get("type")

        if not artist_id or not type_id:
            return Response(
                {"error": "Champs requis: artist, type"},
                status=status.HTTP_400_BAD_REQUEST
            )

        deleted, _ = ArtistType.objects.filter(artist_id=artist_id, type_id=type_id).delete()
        if deleted == 0:
            return Response({"error": "Relation non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
    