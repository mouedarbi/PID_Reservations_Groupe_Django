from django.contrib.auth.models import User, Group
from rest_framework import serializers
from catalogue.models import UserMeta

class SignUpSerializer(serializers.ModelSerializer):
    langue = serializers.CharField(write_only=True, max_length=2)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'langue')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        langue = validated_data.pop('langue')
        user = User.objects.create_user(**validated_data)
        
        # Add user to MEMBER group
        member_group = Group.objects.get(name='MEMBER')
        member_group.user_set.add(user)

        # Create UserMeta
        UserMeta.objects.create(user=user, langue=langue)
        
        return user
