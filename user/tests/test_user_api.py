from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from user.models import User


class UnauthenticatedUserApi(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_unauthenticated_create_user(self) -> None:
        data = {
            "email": "test@gmail.com",
            "password": "test12345",
        }

        response = self.client.post(reverse("user:register"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
