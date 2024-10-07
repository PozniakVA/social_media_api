from django.urls import include, path
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    PostViewSet,
    HashtagViewSet,
    MyProfileView,
    MyPostViewSet,
    FollowView,
    UnfollowView,
    LikeView,
    CommentViewSet,
    LatestPostsViewSet,
    MyFollowingViewSet,
    MyFollowersViewSet,
)

router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet)
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
router.register("my-posts", MyPostViewSet, basename="my-posts")
router.register("comment", CommentViewSet)
router.register("latest-posts", LatestPostsViewSet, basename="latest-posts")
router.register("my-following", MyFollowingViewSet, basename="my-following")
router.register("my-followers", MyFollowersViewSet, basename="my-followers")

urlpatterns = [
    path("", include(router.urls)),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
    path("follow/", FollowView.as_view(), name="follow"),
    path("unfollow/", UnfollowView.as_view(), name="unfollow"),
    path("like/", LikeView.as_view(), name="like"),
]

app_name = "social_media"
