from rest_framework import serializers

class ShowSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False)
    location_id = serializers.IntegerField()
    artist_id = serializers.IntegerField()
    # Ajoutez d'autres champs selon le modèle Show