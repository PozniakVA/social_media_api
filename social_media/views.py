from rest_framework import viewsets, generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from social_media.models import (
    Profile,
    Hashtag,
    Post,
)
from social_media.serializer import (
    ProfileSerializer,
    HashtagSerializer,
    PostSerializer,
    MyProfileSerializer,
    PostDetailSerializer,
    ProfileListSerializer,
    FollowAndUnfollowSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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
        return Post.objects.filter(profiles__follow__subscribed=True).order_by('-created_at')


class MyFollowersView(generics.ListAPIView):
    serializer_class = ProfileListSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        return user_profile.followers.all().order_by("nickname")


class MyFollowingView(generics.ListAPIView):
    serializer_class = ProfileListSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        return user_profile.following.all().order_by("nickname")


class FollowView(APIView):

    def post(self, request: Request) -> Response:
        serializer = FollowAndUnfollowSerializer(data=request.data)
        if serializer.is_valid():

            nickname = serializer.validated_data["nickname"]
            try:
                profile = Profile.objects.get(nickname=nickname)
            except Profile.DoesNotExist:
                return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

            user_profile = request.user.profile
            if user_profile != profile:
                user_profile.following.add(profile)
                return Response({"detail": f"You have followed {profile.nickname}."}, status=status.HTTP_201_CREATED)

            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnfollowView(APIView):
    def post(self, request: Request) -> Response:
        serializer = FollowAndUnfollowSerializer(data=request.data)
        if serializer.is_valid():

            nickname = serializer.validated_data["nickname"]
            try:
                profile = Profile.objects.get(nickname=nickname)
            except Profile.DoesNotExist:
                return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

            user_profile = request.user.profile
            if user_profile != profile:
                user_profile.following.remove(profile)
                return Response({"detail": f"You have unfollowed {profile.nickname}."}, status=status.HTTP_201_CREATED)

            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
