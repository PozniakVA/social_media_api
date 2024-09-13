from django.db import models

from social_media_api import settings


class Profile(models.Model):
    nickname = models.CharField(max_length=120, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True)
    posts = models.ManyToManyField("Post", blank=True)

    def __str__(self) -> str:
        return self.nickname


class Follow(models.Model):
    profile = models.ManyToManyField(
        Profile,
        related_name="follow",
        blank=True,
    )
    subscribed = models.BooleanField(default=False)


class Post(models.Model):
    name = models.CharField(max_length=100)
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    hashtag = models.ManyToManyField(
        "Hashtag",
        related_name="posts",
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Hashtag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name
