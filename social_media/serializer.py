from rest_framework import serializers

from social_media.models import (
    Profile,
    Post,
    Hashtag, Comment
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
        ]


class ProfileListSerializer(ProfileSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "id",
            "nickname",
            "user",
            "bio",
            "profile_image",
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
            "like",
            "author",
            "hashtag",
        ]
        read_only_fields = ["created_at", "like", "author", "id"]


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = [
            "id",
            "name",
        ]


class PostListSerializer(PostSerializer):
    hashtag = HashtagSerializer(many=True)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field="nickname",
    )

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


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(
        read_only=True,
        slug_field="nickname",
    )
    class Meta:
        model = Comment
        fields = [
            "id",
            "profile",
            "post",
            "text",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "profile"]


class CommentListSerializer(CommentSerializer):
    class Meta(CommentSerializer.Meta):
        fields = ["id", "profile", "text", "created_at"]



class PostDetailSerializer(PostListSerializer):
    comments = CommentListSerializer(many=True)
    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ["comments"]


class ProfileDetailSerializer(ProfileSerializer):
    user = UserSerializer()
    posts = PostDetailSerializer(many=True)


class MyProfileSerializer(ProfileSerializer):
    user = UserSerializer()
    posts = PostListSerializer(many=True)

    class Meta(ProfileSerializer.Meta):
        fields = ProfileSerializer.Meta.fields + ["posts"]

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


class FollowAndUnfollowSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length=100)


class LikeSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
