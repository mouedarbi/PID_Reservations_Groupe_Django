from rest_framework import serializers

class TypeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    # Ajoutez d'autres champs selon le modèle Type