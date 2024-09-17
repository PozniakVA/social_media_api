from django.urls import include, path
from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    FollowViewSet,
    PostViewSet,
    HashtagViewSet,
    MyProfileView
)

router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("follow", FollowViewSet)
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path("my-profile/", MyProfileView.as_view(), name="my-profile"),
]

app_name = "social_media"
