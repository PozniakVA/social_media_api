from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from social_media.models import Hashtag
from social_media.tests.function_for_creating_objects_and_urls import (
    list_url,
    sample_hashtag,
    detail_url
)


class AdminHashtagAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@gmail.com",
            password="admin12345",
            is_staff=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_create_hashtag(self) -> None:
        data = {
            "name": "Box"
        }
        response = self.client.post(list_url("hashtag-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_update_hashtag(self) -> None:
        hashtag = sample_hashtag()

        update_hashtag = {"name": "Football"}

        response = self.client.patch(detail_url("hashtag-detail", hashtag.id), update_hashtag)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], update_hashtag["name"])

    def test_delete_hashtag(self) -> None:
        hashtag = sample_hashtag()

        response = self.client.delete(detail_url("hashtag-detail", hashtag.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Hashtag.objects.count(), 0)
