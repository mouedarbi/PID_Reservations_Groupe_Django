from rest_framework import serializers

class PriceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    show_id = serializers.IntegerField()
    # Ajoutez d'autres champs selon le modèle Price