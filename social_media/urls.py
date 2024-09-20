from django.urls import include, path
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    PostViewSet,
    HashtagViewSet,
    MyProfileView,
    MyPostViewSet,
    LatestPostsView,
    MyFollowingView,
    MyFollowersView,
    FollowView,
    UnfollowView, LikeView
)

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
router.register("my-posts", MyPostViewSet, basename="my-posts")


urlpatterns = [
    path('', include(router.urls)),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
    path("latest-posts/", LatestPostsView.as_view(), name="latest-posts"),
    path("my-following/", MyFollowingView.as_view(), name="my-following"),
    path("my-followers/", MyFollowersView.as_view(), name="my-followers"),
    path("follow/", FollowView.as_view(), name="follow"),
    path("unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("like/", LikeView.as_view(), name="like"),
]

app_name = "social_media"
