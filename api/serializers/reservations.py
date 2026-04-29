from rest_framework import serializers
from catalogue.models.reservation import Reservation, RepresentationReservation
from catalogue.models.representation import Representation
from catalogue.models.price import Price

class RepresentationReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepresentationReservation
        fields = ('id', 'representation', 'price', 'quantity')

class ReservationSerializer(serializers.ModelSerializer):
    representation_reservations = RepresentationReservationSerializer(many=True, required=False)
    
    # Virtual fields for backward compatibility or simple one-item creation
    representation = serializers.PrimaryKeyRelatedField(
        queryset=Representation.objects.all(), 
        write_only=True, 
        required=False
    )
    price = serializers.PrimaryKeyRelatedField(
        queryset=Price.objects.all(), 
        write_only=True, 
        required=False
    )
    quantity = serializers.IntegerField(write_only=True, required=False, default=1)

    class Meta:
        model = Reservation
        fields = ('id', 'user', 'booking_date', 'status', 'representation_reservations', 'representation', 'price', 'quantity')
        read_only_fields = ('user', 'booking_date', 'status')

    def validate(self, data):
        # Validation logic for the simple creation (one representation)
        representation = data.get('representation')
        quantity = data.get('quantity', 1)

        if representation:
            if representation.available_seats < quantity:
                raise serializers.ValidationError("Not enough seats available.")
        
        return data

    def create(self, validated_data):
        # Extract virtual fields
        representation = validated_data.pop('representation', None)
        price = validated_data.pop('price', None)
        quantity = validated_data.pop('quantity', 1)
        rep_reservations_data = validated_data.pop('representation_reservations', [])

        # Create the main reservation
        reservation = Reservation.objects.create(**validated_data)

        # Handle single item creation (legacy/simple support)
        if representation and price:
            RepresentationReservation.objects.create(
                reservation=reservation,
                representation=representation,
                price=price,
                quantity=quantity
            )
            # Update seats
            representation.available_seats -= quantity
            representation.save()
        
        # Handle nested items if provided
        for item in rep_reservations_data:
            RepresentationReservation.objects.create(reservation=reservation, **item)
            # Update seats
            rep = item['representation']
            rep.available_seats -= item['quantity']
            rep.save()

        return reservation
