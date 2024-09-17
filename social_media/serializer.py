from rest_framework import serializers

from social_media.models import (
    Profile,
    Follow,
    Post,
    Hashtag
)
from user.serializer import UserSerializer


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
            "created_at",
            "hashtag",
        ]


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = [
            "id",
            "name",
        ]


class PostDetailSerializer(PostSerializer):
    hashtag = HashtagSerializer(many=True)

    def create(self, validated_data):
        hashtags_data = validated_data.pop("hashtag", None)
        post = Post.objects.create(**validated_data)

        if hashtags_data:
            for hashtag_data in hashtags_data:
                hashtag = Hashtag.objects.create(name=hashtag_data["name"])
                post.hashtag.add(hashtag)

        user = self.context["request"].user
        profile = Profile.objects.get(user=user)
        post.profiles.add(profile)
        return post



class MyProfileSerializer(ProfileSerializer):
    user = UserSerializer()
    posts = PostDetailSerializer(many=True)

    def update(self, instance, validated_data):

        user_data = validated_data.pop("user", None)
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        posts_data = validated_data.pop("posts", None)
        if posts_data:
            for post_data in posts_data:
                hashtags_data = post_data.pop("hashtag", None)
                post, created = Post.objects.get_or_create(**post_data)

                if hashtags_data:
                    for hashtag_data in hashtags_data:
                        hashtag, created = Hashtag.objects.get_or_create(name=hashtag_data["name"])
                        post.hashtag.add(hashtag)

                instance.posts.add(post)

        return instance
