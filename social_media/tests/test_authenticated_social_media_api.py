from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from social_media.models import Profile, Post, Hashtag, Comment
from social_media.serializer import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    PostListSerializer,
    PostDetailSerializer,
    HashtagSerializer,
    CommentSerializer,
    MyProfileListSerializer
)
from social_media.tests.function_for_creating_objects_and_urls import (
    list_url,
    detail_url,
    get_simple_profile,
    sample_user,
    sample_post,
    add_like_count_field,
    sample_hashtag,
    create_two_posts_and_profiles,
    sample_comment
)


class AuthenticatedProfileAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password = "test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_profiles(self) -> None:
        profiles = Profile.objects.all()
        serializer = ProfileListSerializer(profiles, many=True)

        response = self.client.get(list_url("profile-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_profile(self) -> None:
        profile = get_simple_profile(user=self.user)
        serializer = ProfileDetailSerializer(profile)

        response = self.client.get(detail_url("profile-detail",profile.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_profile_by_nickname(self) -> None:
        profile_1 = get_simple_profile(user=self.user)

        user_2 = sample_user(email="test_22gmail.com")
        profile_2 = get_simple_profile(user=user_2)

        serializer_1 = ProfileListSerializer(profile_1)
        serializer_2 = ProfileListSerializer(profile_2)

        response = self.client.get(list_url("profile-list"), {"nickname": profile_2.nickname})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)


class AuthenticatedPostAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password = "test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_posts(self) -> None:
        sample_post()
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        serializer_data = add_like_count_field(serializer.data)

        response = self.client.get(list_url("post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_detail_post(self) -> None:
        post = sample_post()
        serializer = PostDetailSerializer(post)
        serializer_data = add_like_count_field(serializer.data)

        response = self.client.get(detail_url("post-detail", post.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_filter_post_by_hashtag(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        response = self.client.get(list_url("post-list"), {"hashtag": data["hashtag_2"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)

    def test_filter_post_by_title(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        response = self.client.get(list_url("post-list"), {"title": data["post_2"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)

    def test_filter_post_by_author(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        response = self.client.get(list_url("post-list"), {"author": data["profile_2"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)


class AuthenticatedHashtagAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_hashtags(self) -> None:
        sample_hashtag()
        hashtags = Hashtag.objects.all()

        serializer = HashtagSerializer(hashtags, many=True)

        response = self.client.get(list_url("hashtag-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_detail_hashtag(self) -> None:
        hashtag = sample_hashtag()
        serializer = HashtagSerializer(hashtag)

        response = self.client.get(detail_url("hashtag-detail", hashtag.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_filter_hashtag_by_name(self) -> None:
        hashtag_1 = sample_hashtag()
        hashtag_2 = sample_hashtag(name="sport")

        serializer_1 = HashtagSerializer(hashtag_1)
        serializer_2 = HashtagSerializer(hashtag_2)

        response = self.client.get(list_url("hashtag-list"), {"name": hashtag_2.name})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)

    def test_create_hashtag_forbidden(self) -> None:
        data = {"name": "sport"}

        response = self.client.post(list_url("hashtag-list"), data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_hashtag_forbidden(self) -> None:
        hashtag = sample_hashtag()
        data = {"name": "sport"}

        response = self.client.put(detail_url("hashtag-detail", hashtag.id), data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_hashtag_forbidden(self) -> None:
        hashtag = sample_hashtag()

        response = self.client.post(detail_url("hashtag-detail", hashtag.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticatedMyProfileAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_my_profile(self) -> None:
        profile = get_simple_profile(self.user)
        serializer = MyProfileListSerializer(profile)

        response = self.client.get(list_url("my-profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_my_profile(self) -> None:
        profile = get_simple_profile(self.user)
        data = {
            "nickname": "top_user",
            "bio": "top_user"
        }

        response = self.client.patch(list_url("my-profile"), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile.refresh_from_db()
        for key, value in data.items():
            self.assertEqual(getattr(profile, key), value)

    def test_update_my_profile_nested_user(self) -> None:
        profile = get_simple_profile(self.user)
        data = {
            "user": {
                "email": "top_user@gmail.com",
            }
        }

        response = self.client.patch(list_url("my-profile"), data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile.refresh_from_db()
        for key, value in data["user"].items():
            self.assertEqual(getattr(profile.user, key), value)


class AuthenticatedMyPostAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_my_post(self) -> None:
        user_1 = sample_user()
        profile_1 = get_simple_profile(user=user_1)
        post_1 = sample_post(author=profile_1)

        profile_2 = get_simple_profile(user=self.user)
        post_2 = sample_post(author=profile_2)

        response = self.client.get(list_url("my-posts-list"))

        serializer_1 = PostListSerializer(post_1)
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(post_2)
        serializer_data_2 = add_like_count_field(serializer_2.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)

    def test_detail_my_post(self) -> None:
        profile = get_simple_profile(user=self.user)
        post = sample_post(author=profile)

        serializer = PostDetailSerializer(post)
        serializer_data = add_like_count_field(serializer.data)

        response = self.client.get(detail_url("my-posts-detail", post.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer_data)

    def test_filter_my_post_by_title(self) -> None:
        user_1 = sample_user()
        profile_1 = get_simple_profile(user=user_1)
        post_1 = sample_post(author=profile_1)

        profile_2 = get_simple_profile(user=self.user)
        post_2 = sample_post(title="sport", author=profile_2)

        serializer_1 = PostListSerializer(post_1)
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(post_2)
        serializer_data_2 = add_like_count_field(serializer_2.data)

        response = self.client.get(list_url("my-posts-list"), {"title": post_2.title})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)

    def test_filter_my_post_by_hashtag(self) -> None:
        user_1 = sample_user()
        profile_1 = get_simple_profile(user=user_1)
        hashtag_1 = sample_hashtag()
        post_1 = sample_post(author=profile_1, hashtags=[hashtag_1])

        profile_2 = get_simple_profile(user=self.user)
        hashtag_2 = sample_hashtag(name="sport")
        post_2 = sample_post(title="sport", author=profile_2, hashtags=[hashtag_2])

        serializer_1 = PostListSerializer(post_1)
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(post_2)
        serializer_data_2 = add_like_count_field(serializer_2.data)

        response = self.client.get(list_url("my-posts-list"), {"hashtag": hashtag_2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)

    def test_create_my_post(self) -> None:
        profile = get_simple_profile(user=self.user)
        data = {
            "title": "sport",
            "author": profile
        }
        response = self.client.post(list_url("my-posts-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.items():
            self.assertEqual(data[key], value)

    def test_update_my_post(self) -> None:
        profile = get_simple_profile(user=self.user)
        post = sample_post(author=profile)

        update_post = {"title": "test hello"}

        response = self.client.patch(detail_url("my-posts-detail", post.id), update_post)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in update_post.items():
            self.assertEqual(response.data[key], value)

    def test_delete_my_post(self) -> None:
        profile = get_simple_profile(user=self.user)
        post = sample_post(author=profile)

        response = self.client.delete(detail_url("my-posts-detail", post.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Post.objects.all()), 0)


class AuthenticatedLatestPostsAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_latest_posts(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        profile = get_simple_profile(user=self.user)
        profile.following.add(data["profile_2"])

        response = self.client.get(list_url("latest-posts-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)

    def test_detail_latest_posts(self) -> None:
        user_1 = sample_user()
        profile_1 = get_simple_profile(user=user_1)
        post_1 = sample_post(author=profile_1)
        serializer_1 = PostDetailSerializer(post_1)
        serializer_data_1 = add_like_count_field(serializer_1.data)

        profile_2 = get_simple_profile(user=self.user)
        profile_2.following.add(profile_1)

        response = self.client.get(detail_url("latest-posts-detail", post_1.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data_1, response.data)

    def test_filter_post_by_hashtag(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        hashtag_3 = sample_hashtag(name="music")
        post_3 = sample_post(author=data["profile_2"], hashtags=[hashtag_3])
        serializer_3 = PostListSerializer(post_3)
        serializer_data_3 = add_like_count_field(serializer_3.data)

        profile = get_simple_profile(user=self.user)
        profile.following.add(data["profile_2"])

        response = self.client.get(list_url("latest-posts-list"), {"hashtag": data["hashtag_2"]})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_2, response.data)
        self.assertNotIn(serializer_data_1, response.data)
        self.assertNotIn(serializer_data_3, response.data)

    def test_filter_post_by_title(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        post_3 = sample_post(title="music", author=data["profile_2"])
        serializer_3 = PostListSerializer(post_3)
        serializer_data_3 = add_like_count_field(serializer_3.data)

        profile = get_simple_profile(user=self.user)
        profile.following.add(data["profile_2"])

        response = self.client.get(list_url("latest-posts-list"), {"title": post_3.title})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_3, response.data)
        self.assertNotIn(serializer_data_1, response.data)
        self.assertNotIn(serializer_data_2, response.data)

    def test_filter_post_by_author(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = PostListSerializer(data["post_1"])
        serializer_data_1 = add_like_count_field(serializer_1.data)

        serializer_2 = PostListSerializer(data["post_2"])
        serializer_data_2 = add_like_count_field(serializer_2.data)

        user_3 = sample_user()
        profile_3 = get_simple_profile(user=user_3)
        post_3 = sample_post(author=profile_3)
        serializer_3 = PostListSerializer(post_3)
        serializer_data_3 = add_like_count_field(serializer_3.data)

        profile = get_simple_profile(user=self.user)
        profile.following.add(data["profile_2"], profile_3)

        response = self.client.get(list_url("latest-posts-list"), {"author": post_3.author })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_data_3, response.data)
        self.assertNotIn(serializer_data_1, response.data)
        self.assertNotIn(serializer_data_2, response.data)


class AuthenticatedMyFollowersAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_followers(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = ProfileListSerializer(data["profile_1"])
        serializer_2 = ProfileListSerializer(data["profile_2"])

        profile = get_simple_profile(user=self.user)
        profile.followers.add(data["profile_2"])

        response = self.client.get(list_url("my-followers-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)

    def test_detail_followers(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = ProfileDetailSerializer(data["profile_1"])

        profile = get_simple_profile(user=self.user)
        profile.followers.add(data["profile_1"])

        response = self.client.get(detail_url("my-followers-detail", data["profile_1"].id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_1.data, response.data)

    def test_filter_followers_by_nickname(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = ProfileListSerializer(data["profile_1"])
        serializer_2 = ProfileListSerializer(data["profile_2"])

        user_3 = sample_user()
        profile_3 = get_simple_profile(user=user_3)
        serializer_3 = ProfileListSerializer(profile_3)

        profile = get_simple_profile(user=self.user)
        profile.followers.add(profile_3)

        response = self.client.get(list_url("my-followers-list"), {"nickname": profile_3.nickname})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_3.data, response.data)
        self.assertNotIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)


class AuthenticatedMyFollowingAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_list_followers(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = ProfileListSerializer(data["profile_1"])
        serializer_2 = ProfileListSerializer(data["profile_2"])

        profile = get_simple_profile(user=self.user)
        profile.following.add(data["profile_2"])

        response = self.client.get(list_url("my-following-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)

    def test_detail_followers(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = ProfileDetailSerializer(data["profile_1"])

        profile = get_simple_profile(user=self.user)
        profile.following.add(data["profile_1"])

        response = self.client.get(detail_url("my-following-detail", data["profile_1"].id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_1.data, response.data)

    def test_filter_followers_by_nickname(self) -> None:
        data = create_two_posts_and_profiles()

        serializer_1 = ProfileListSerializer(data["profile_1"])
        serializer_2 = ProfileListSerializer(data["profile_2"])

        user_3 = sample_user()
        profile_3 = get_simple_profile(user=user_3)
        serializer_3 = ProfileListSerializer(profile_3)

        profile = get_simple_profile(user=self.user)
        profile.following.add(profile_3)

        response = self.client.get(list_url("my-following-list"), {"nickname": profile_3.nickname})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_3.data, response.data)
        self.assertNotIn(serializer_2.data, response.data)
        self.assertNotIn(serializer_1.data, response.data)


class AuthenticatedCommentAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_detail_comments(self) -> None:
        comment = sample_comment()
        serializer = CommentSerializer(comment)

        response = self.client.get(detail_url("comment-detail", comment.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_create_comment(self) -> None:
        profile = get_simple_profile(user=self.user)
        data = {
            "post": sample_post(author=profile).id,
            "profile": profile.id,
            "text": "hello world"
        }

        response = self.client.post(list_url("comment-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data["profile"] = profile.nickname
        for key, value in data.items():
            self.assertEqual(response.data[key], value)

    def test_update_comment(self) -> None:
        comment = sample_comment()

        update_comment = {"text": "test hello"}

        response = self.client.patch(detail_url("comment-detail", comment.id), update_comment)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for key, value in update_comment.items():
            self.assertEqual(response.data[key], value)

    def test_delete_comment(self) -> None:
        comment = sample_comment()

        response = self.client.delete(detail_url("comment-detail", comment.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(Comment.objects.all()), 0)


class AuthenticatedFollowAndLikeAPITest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test12345"
        )
        self.client.force_authenticate(self.user)

    def test_follow(self) -> None:
        profile_1 = get_simple_profile(user=self.user)
        profile_2 = get_simple_profile(user=sample_user())

        response = self.client.post(list_url("follow"), {"nickname": profile_2.nickname})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(profile_1, profile_2.followers.all())

    def test_unfollow(self) -> None:
        profile_1 = get_simple_profile(user=self.user)
        profile_2 = get_simple_profile(user=sample_user())

        profile_1.following.add(profile_2)

        response = self.client.post(list_url("unfollow"), {"nickname": profile_2.nickname})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(profile_1, profile_2.followers.all())

    def test_like(self) -> None:
        profile = get_simple_profile(user=self.user)
        post = sample_post(author=profile)

        response = self.client.post(list_url("like"), {"post_id": post.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.like.count(), 1)

    def test_unlike(self) -> None:
        profile = get_simple_profile(user=self.user)
        post = sample_post(author=profile)
        post.like.add(profile)

        response = self.client.post(list_url("like"), {"post_id": post.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.like.count(), 0)
