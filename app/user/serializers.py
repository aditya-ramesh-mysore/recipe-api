from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        model = get_user_model()

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)