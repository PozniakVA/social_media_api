from rest_framework import serializers

from social_media.models import (
    Profile,
    Follow,
    Post,
    Hashtag
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "id",
            "nickname",
            "user",
            "bio",
            "profile_image",
            "posts",
        ]


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = [
            "id",
            "profile",
            "subscribed",
        ]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "name",
            "text",
            "image",
            "hashtag",
        ]


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = [
            "id",
            "name",
        ]
