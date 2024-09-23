from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


class TestUnauthenticatedSocialMediaApi(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_authenticated_required(self) -> None:
        ENDPOINTS = [
            "profile-list",
            "post-list",
            "hashtag-list",
            "my-posts-list",
            "comment-list",
            "latest-posts-list",
            "my-following-list",
            "my-followers-list",
            "my-profile",
            "follow",
            "unfollow",
            "like",
        ]
        for endpoint in ENDPOINTS:
            ENDPOINT_URL = reverse(f"social_media:{endpoint}")
            response = self.client.get(ENDPOINT_URL)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"{endpoint} must request authentication",
            )
