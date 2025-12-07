from rest_framework import serializers

class RepresentationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    show_id = serializers.IntegerField()
    location_id = serializers.IntegerField()
    when = serializers.DateTimeField()
    # Ajoutez d'autres champs selon le modèle Representation