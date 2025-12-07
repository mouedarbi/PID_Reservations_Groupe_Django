from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    show_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # Ajoutez d'autres champs selon le modèle CartItem

class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    # Ajoutez d'autres champs selon le modèle Cart