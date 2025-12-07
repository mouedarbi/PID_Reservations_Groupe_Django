from rest_framework import serializers

class ReservationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    representation_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # Ajoutez d'autres champs selon le modèle Reservation