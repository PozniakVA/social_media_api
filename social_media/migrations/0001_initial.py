# Generated by Django 5.1.1 on 2024-09-20 05:25

import django.db.models.deletion
import social_media.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Hashtag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("text", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        null=True, upload_to=social_media.models.image_path
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "hashtag",
                    models.ManyToManyField(
                        blank=True, related_name="posts", to="social_media.hashtag"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nickname", models.CharField(max_length=120, unique=True)),
                ("bio", models.TextField(blank=True, null=True)),
                (
                    "profile_image",
                    models.ImageField(
                        blank=True, null=True, upload_to=social_media.models.image_path
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        blank=True, related_name="followers", to="social_media.profile"
                    ),
                ),
                (
                    "posts",
                    models.ManyToManyField(
                        blank=True, related_name="profiles", to="social_media.post"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="post",
            name="like",
            field=models.ManyToManyField(blank=True, to="social_media.profile"),
        ),
    ]
