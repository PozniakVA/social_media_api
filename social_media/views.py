from rest_framework import viewsets, generics, request

from social_media.models import (
    Profile,
    Hashtag,
    Post,
    Follow
)
from social_media.serializer import (
    ProfileSerializer,
    HashtagSerializer,
    PostSerializer,
    FollowSerializer,
    MyProfileSerializer,
    PostDetailSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MyProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class MyPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.filter(profiles__user=self.request.user).order_by('-created_at')


class LatestPostsView(generics.ListAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        return Post.objects.all().order_by('-created_at')