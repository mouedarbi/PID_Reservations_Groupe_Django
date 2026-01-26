from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from api.serializers.signup import SignUpSerializer
from django.contrib.auth.models import User


class AuthSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)


class AuthLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class AuthLogoutView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except (AttributeError, Token.DoesNotExist):
                return Response({"detail": "No token found for user."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)