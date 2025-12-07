from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    street = serializers.CharField(max_length=255)
    locality_id = serializers.IntegerField()
    # Ajoutez d'autres champs selon le modèle Location