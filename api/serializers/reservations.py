from rest_framework import serializers
from catalogue.models.reservation import Reservation
from catalogue.models.representation import Representation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
        read_only_fields = ('user', 'booking_date', 'status')

    def validate(self, data):
        """
        Check that there are enough seats available.
        """
        representation = data.get('representation')
        quantity = data.get('quantity')

        if representation and quantity:
            if representation.available_seats < quantity:
                raise serializers.ValidationError("Not enough seats available.")
        
        return data

    def create(self, validated_data):
        # Update available seats
        representation = validated_data['representation']
        quantity = validated_data['quantity']
        
        # Decrement seats (simple approach, race conditions possible but acceptable for this context)
        representation.available_seats -= quantity
        representation.save()
        
        return super().create(validated_data)

