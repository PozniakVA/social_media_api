from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from social_media.models import Profile, Post, Hashtag, Comment


def list_url(endpoint):
    return reverse(f"social_media:{endpoint}")


def detail_url(endpoint, object_id):
    return reverse(f"social_media:{endpoint}", args=[object_id])


def sample_user(**params):
    defaults = {"email": "test_user@gmail.com", "password": "test12345"}
    defaults.update(params)
    return get_user_model().objects.create_user(**defaults)


def get_simple_profile(user):
    return Profile.objects.get(user=user)


def sample_hashtag(**params):
    defaults = {"name": "test"}
    defaults.update(params)
    return Hashtag.objects.create(**defaults)


def sample_post(**params):
    hashtags = params.pop("hashtags", None)

    defaults = {
        "title": "test",
        "author": None,
    }
    defaults.update(params)

    post = Post.objects.create(**defaults)

    if hashtags:
        for hashtag in hashtags:
            post.hashtags.add(hashtag)

    return post


def add_like_count_field(serializer_data):
    if isinstance(serializer_data, list):
        for item in serializer_data:
            item["like_count"] = 0
    else:
        serializer_data["like_count"] = 0
    return serializer_data


def create_two_posts_and_profiles():
    user_1 = sample_user(email="test_11gmail.com")
    profile_1 = get_simple_profile(user=user_1)
    hashtag_1 = sample_hashtag(name="box")
    post_1 = sample_post(author=profile_1, hashtags=[hashtag_1])

    user_2 = sample_user(email="test_22gmail.com")
    profile_2 = get_simple_profile(user=user_2)
    hashtag_2 = sample_hashtag(name="sport")
    post_2 = sample_post(title="sport", author=profile_2, hashtags=[hashtag_2])

    return {
        "post_1": post_1,
        "post_2": post_2,
        "hashtag_1": hashtag_1,
        "hashtag_2": hashtag_2,
        "profile_1": profile_1,
        "profile_2": profile_2,
    }


def sample_comment(**params):
    profile = get_simple_profile(user=sample_user())
    defaults = {
        "post": sample_post(author=profile),
        "profile": profile,
        "text": "test"
    }
    defaults.update(params)
    return Comment.objects.create(**defaults)
