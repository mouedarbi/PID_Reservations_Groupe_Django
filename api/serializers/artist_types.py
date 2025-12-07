from rest_framework import serializers

class ArtistTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    artist_id = serializers.IntegerField()
    type_id = serializers.IntegerField()
    # Ajoutez d'autres champs selon le modèle ArtistType