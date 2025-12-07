from rest_framework import serializers

class AffiliateSerializer(serializers.Serializer):
    # Placeholder pour les données de l'affilié
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    # Ajoutez d'autres champs selon le modèle Affiliate