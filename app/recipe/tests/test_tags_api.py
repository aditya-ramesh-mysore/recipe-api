from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Recipe
from recipe.serializers import RecipeSerializer, TagSerializer

TAGS_LIST_URL = reverse('recipe:tag-list')
RECIPES_URL = reverse('recipe:recipe-list')

def tags_detail_url(id):
    return reverse('recipe:tag-detail', args=[id])
class TagsPrivateApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email="aditya@ex.com", password="password", name="aditya")
        self.client.force_authenticate(user=self.user)

    def test_get_tags_list(self):
        t1 = Tag.objects.create(user=self.user, name="Vegan")
        t2 = Tag.objects.create(user=self.user, name="Dessert")
        l = [t1, t2]
        another_user = get_user_model().objects.create_user(email="another@ex.com", password="another", name="another")
        Tag.objects.create(user=another_user, name="Fruity")

        response = self.client.get(TAGS_LIST_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], t2.name) # Ordered by ascending order

    def test_get_tags_detail(self):
        t1 = Tag.objects.create(user = self.user, name="Vegan")
        url = tags_detail_url(t1.id)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_recipe_tag(self):
        recipe_obj = {
            'title': 'sample title',
            'description': 'sample description',
            'time_required': 5,
            'link': "www.example.com/example",
            'price': 5.5,
            'tags': [
                {'name': "Vegan"},
                {"name": "Dessert"}
            ]
        }

        response = self.client.post(RECIPES_URL, recipe_obj, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Tag.objects.all()), 2)

    def test_update_recipe_tags(self):
        recipe_obj = {
            'title': 'sample title',
            'description': 'sample description',
            'time_required': 5,
            'link': "www.example.com/example",
            'price': 5.5
        }
        recipe_obj = Recipe.objects.create(user=self.user, **recipe_obj)
        recipe_obj.tags.set([
            Tag.objects.create(user=self.user, name="Vegan"),
            Tag.objects.create(user=self.user, name="Dessert")
        ])
        recipe_obj.save()
        update_payload = {
            'title': 'sample title 2',
            'description': 'sample description',
            'time_required': 5,
            'link': "www.example.com/example",
            'price': 5.5,
            'tags': [
                {'name': "updated"},
                {"name": "Dessert"}
            ]
        }
        recipes_detail_url = reverse('recipe:recipe-detail', args=[recipe_obj.id])
        response = self.client.patch(recipes_detail_url, update_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(Tag.objects.filter(recipe=recipe_obj)), 2)
        self.assertEqual(response.data['tags'][0]['name'], 'Dessert')
        self.assertEqual(response.data['tags'][1]['name'], 'updated')
