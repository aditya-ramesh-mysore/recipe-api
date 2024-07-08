from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')

def create_recipe(user, **params):
    recipe_obj = {
        'title': 'sample title',
        'description': 'sample description',
        'time_required': 5,
        'link': "www.example.com/example",
        'price': 5.5
    }
    recipe_obj.update(**params)

    obj = Recipe.objects.create(user=user, **recipe_obj)
    print(obj)

class RecipePrivateTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="user@example.com", password="password", name="username")
        # print(self.user)
        self.client.force_authenticate(self.user)

    def test_list_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_authenticated_user_recipes(self):
        new_user = get_user_model().objects.create_user(email="newuser@example.com", name="newuser", password="newpassword")

        create_recipe(user=new_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
