from rest_framework import serializers
from django.contrib.auth import (get_user_model, authenticate)
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "title", "price", "time_required", "description"]
        read_only_fields = ["id"]
        model = Recipe

    def validate(self, attrs):
        print(self.initial_data)
        for key, value in attrs.items():
            if key not in self.fields:
                raise serializers.ValidationError()
        return attrs