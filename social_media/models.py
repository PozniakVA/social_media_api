import pathlib
import uuid
from typing import Any

from django.db import models
from django.utils.text import slugify

from social_media_api import settings

def image_path(instance: Any, filename: str) -> pathlib.Path:

    mark = "other"
    path_at_media = "upload/"
    if isinstance(instance, Post):
        path_at_media = "upload/post/"
        mark = instance.name
    elif isinstance(instance, Profile):
        path_at_media = "upload/profile_image/"
        mark = instance.nickname

    filename = f"{slugify(mark)}-{uuid.uuid4()}" + pathlib.Path(filename).suffix

    return pathlib.Path(path_at_media) / pathlib.Path(filename)


class Profile(models.Model):
    nickname = models.CharField(max_length=120, unique=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True, upload_to=image_path)
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
    image = models.ImageField(null=True, upload_to=image_path)
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
