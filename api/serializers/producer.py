from rest_framework import serializers

class ProducerSerializer(serializers.Serializer):
    # Placeholder pour les données du producteur
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    # Ajoutez d'autres champs selon le modèle Producer