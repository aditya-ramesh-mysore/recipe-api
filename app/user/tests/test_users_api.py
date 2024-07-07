from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse("user:me")

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

    def test_token_creation_success(self):
        get_user_model().objects.create_user(**self.payload)
        login_payload = {
            "email": self.payload["email"],
            "password": self.payload["password"]
        }
        res = self.client.post(TOKEN_URL, login_payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_bad_credentials_login(self):
        get_user_model().objects.create_user(**self.payload)
        login_payload = {
            "email": self.payload["email"],
            "password": "random-password"
        }
        res = self.client.post(TOKEN_URL, login_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_empty_password_login(self):
        get_user_model().objects.create_user(**self.payload)
        login_payload = {
            "email": self.payload["email"],
            "password": ""
        }
        res = self.client.post(TOKEN_URL, login_payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", res.data)

    def test_me_url(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class UserPrivateApisTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(**{
            "email": "test@example.com",
            "password": "testpassword",
            "name": "testname"
        })
        self.client.force_authenticate(user=self.user)

    def test_retrieve_user_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"email": self.user.email, "name": self.user.name})

    def test_update_user(self):
        update_user = {
            "email": "newemail@example.com",
            "password": "updated password"
        }
        res = self.client.patch(ME_URL, update_user)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, update_user["email"])
        self.assertTrue(self.user.check_password(update_user["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)