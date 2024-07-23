from rest_framework import serializers
from django.contrib.auth import (get_user_model, authenticate)
from core.models import Recipe, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "id"]
        model = Tag
        read_only_fields = ["id"]

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    class Meta:
        fields = ["id", "title", "price", "time_required", "link", "description", "tags"]
        read_only_fields = ["id"]
        model = Recipe

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        tags = validated_data.pop("tags", [])
        recipe_obj = Recipe.objects.create(**validated_data)
        authenticated_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=authenticated_user, **tag)
            recipe_obj.tags.add(tag_obj)
        recipe_obj.save()
        return recipe_obj

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if tags is not None:
            instance.tags.clear()
            authenticated_user = self.context['request'].user
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(user=authenticated_user, **tag)
                print(tag_obj, created)
                instance.tags.add(tag_obj)
        instance.save()
        return instance

    # def validate(self, attrs):
    #     for key, value in attrs.items():
    #         if key not in self.fields:
    #             raise serializers.ValidationError()
    #     return attrs