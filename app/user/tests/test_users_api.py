from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")

class UserPublicApisTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()

    def setUp(self):
        self.payload = {
            "email": "test@example.com",
            "password": "testpassword",
            "name": "testname"
        }

    def test_create_valid_user_success(self):
        res = self.client.post(CREATE_USER_URL, self.payload)
        data = res.data
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        db_data = get_user_model().objects.get(email=self.payload["email"])
        self.assertTrue(db_data.check_password(self.payload["password"]))
        self.assertEqual(db_data.email, self.payload["email"])

    def test_password_too_short(self):
        self.payload["password"] = "test"
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        db_data = get_user_model().objects.filter(email=self.payload["email"])
        self.assertFalse(db_data.exists())

    def test_user_already_exists(self):
        u = get_user_model().objects.create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)