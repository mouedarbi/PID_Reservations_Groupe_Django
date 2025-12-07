from rest_framework import serializers

class LocalitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=10)
    # Ajoutez d'autres champs selon le modèle Locality