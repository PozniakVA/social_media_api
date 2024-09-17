from rest_framework import routers

from social_media.views import (
    ProfileViewSet,
    FollowViewSet,
    PostViewSet,
    HashtagViewSet
)

router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("follow", FollowViewSet)
router.register("posts", PostViewSet)
router.register("hashtags", HashtagViewSet)
urlpatterns = router.urls

app_name = "social_media"
