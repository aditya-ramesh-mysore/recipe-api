from rest_framework import generics
from user.serializers import (UserSerializer, AuthSerializer)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

class AuthTokenView(ObtainAuthToken):
    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_valid_data = serializer.validated_data
        print(user_valid_data)
        token, created = Token.objects.get_or_create(user=user_valid_data["user"])
        return Response({
            "token": token.key,
            "email": user_valid_data["email"]
        })
