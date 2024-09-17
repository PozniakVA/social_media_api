from django.urls import include, path
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    FollowViewSet,
    PostViewSet,
    HashtagViewSet,
    MyProfileView,
    MyPostViewSet, LatestPostsView
)

router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("follow", FollowViewSet)
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
router.register("my-posts", MyPostViewSet, basename="my-posts")


urlpatterns = [
    path('', include(router.urls)),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
    path("latest-posts/", LatestPostsView.as_view(), name="latest-posts"),
]

app_name = "social_media"
