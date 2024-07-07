from rest_framework import serializers
from django.contrib.auth import (get_user_model, authenticate)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        model = get_user_model()

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.email = validated_data.get("email", instance.email)
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        return instance

class AuthSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style = {"input_type": "password"})

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        data["user"] = user
        return data