from rest_framework import serializers

class AuthSerializer(serializers.Serializer):
    # Placeholder pour l'authentification
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    # Ajoutez d'autres champs selon les besoins d'authentification