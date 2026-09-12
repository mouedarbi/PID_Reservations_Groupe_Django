from django.db import transaction
from rest_framework import serializers

from catalogue.models import Price, Representation, RepresentationReservation, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    representation = serializers.PrimaryKeyRelatedField(
        queryset=Representation.objects.all(),
        write_only=True,
        required=False,
    )
    price = serializers.PrimaryKeyRelatedField(
        queryset=Price.objects.all(),
        write_only=True,
        required=False,
    )
    quantity = serializers.IntegerField(write_only=True, min_value=1, required=False)

    class Meta:
        model = Reservation
        fields = (
            'id',
            'booking_date',
            'status',
            'user',
            'representations',
            'representation',
            'price',
            'quantity',
        )
        read_only_fields = ('id', 'booking_date', 'status', 'user', 'representations')

    def validate(self, data):
        representation = data.get('representation')
        quantity = data.get('quantity')
        price = data.get('price')

        if not representation or quantity is None or not price:
            raise serializers.ValidationError(
                'representation, price et quantity sont obligatoires.'
            )
        if not representation.show.prices.filter(pk=price.pk).exists():
            raise serializers.ValidationError(
                'Le tarif sélectionné n’est pas associé à ce spectacle.'
            )
        if representation.available_seats < quantity:
            raise serializers.ValidationError('Not enough seats available.')
        return data

    @transaction.atomic
    def create(self, validated_data):
        representation = validated_data.pop('representation')
        price = validated_data.pop('price')
        quantity = validated_data.pop('quantity')
        status = validated_data.pop('status', 'PAID')
        representation = Representation.objects.select_for_update().get(pk=representation.pk)
        if representation.available_seats < quantity:
            raise serializers.ValidationError('Not enough seats available.')

        reservation = Reservation.objects.create(**validated_data, status=status)
        RepresentationReservation.objects.create(
            reservation=reservation,
            representation=representation,
            price=price,
            quantity=quantity,
        )
        representation.available_seats -= quantity
        representation.save(update_fields=['available_seats'])
        return reservation

    def to_representation(self, instance):
        data = super().to_representation(instance)
        line = instance.representation_reservations.select_related(
            'representation', 'price'
        ).first()
        if line:
            data['representation'] = line.representation_id
            data['price'] = line.price_id
            data['quantity'] = line.quantity
        return data
