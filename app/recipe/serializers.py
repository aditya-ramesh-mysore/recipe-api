from rest_framework import serializers
from django.contrib.auth import (get_user_model, authenticate)
from core.models import Recipe, Tag, Ingredient

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "id"]
        model = Tag
        read_only_fields = ["id"]

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ["name", "id"]
        model = Ingredient
        read_only_fields = ["id"]

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance

class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)
    class Meta:
        fields = ["id", "title", "price", "time_required", "link", "description", "tags", "ingredients"]
        read_only_fields = ["id"]
        model = Recipe

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", [])
        recipe_obj = Recipe.objects.create(**validated_data)
        authenticated_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=authenticated_user, **tag)
            recipe_obj.tags.add(tag_obj)
        for ingredient in ingredients:
            ingredient_obj, created = Ingredient.objects.get_or_create(user=authenticated_user, **ingredient)
            recipe_obj.ingredients.add(ingredient_obj)
        recipe_obj.save()
        return recipe_obj

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        ingredients = validated_data.pop("ingredients", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        authenticated_user = self.context['request'].user
        if tags is not None:
            instance.tags.clear()
            for tag in tags:
                tag_obj, created = Tag.objects.get_or_create(user=authenticated_user, **tag)
                instance.tags.add(tag_obj)
        if ingredients is not None:
            instance.ingredients.clear()
            for ingredient in ingredients:
                ingredient_obj, created = Ingredient.objects.get_or_create(user=authenticated_user, **ingredient)
                instance.ingredients.add(ingredient_obj)
        instance.save()
        return instance

