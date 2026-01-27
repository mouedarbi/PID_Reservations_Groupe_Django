from rest_framework import serializers
from catalogue.models.cart import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "representation",
            "quantity",
            "price_per_item",
            "item_total",
        ]
        read_only_fields = ["price_per_item", "item_total"]

    def get_item_total(self, obj):
        return obj.get_item_total()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    total_items = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_price",
            "total_items",
            "created_at",
            "updated_at",
        ]

    def get_total_price(self, obj):
        return obj.get_total_price()

    def get_total_items(self, obj):
        return obj.get_item_count()
