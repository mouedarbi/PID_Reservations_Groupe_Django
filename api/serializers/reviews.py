from rest_framework import serializers

class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    show_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False)
    validated = serializers.BooleanField(default=False)
    # Ajoutez d'autres champs selon le modèle Review