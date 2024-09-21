from django.db.models import Count
from rest_framework import viewsets, generics, status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from social_media.models import (
    Profile,
    Hashtag,
    Post, Comment,
)
from social_media.serializer import (
    ProfileSerializer,
    HashtagSerializer,
    PostSerializer,
    MyProfileSerializer,
    PostDetailSerializer,
    ProfileListSerializer,
    FollowAndUnfollowSerializer,
    LikeSerializer,
    ProfileDetailSerializer,
    PostListSerializer,
    CommentSerializer,
)


class ProfileViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Profile.objects.all().order_by("-user__date_joined")

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        elif self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileSerializer


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Post.objects.annotate(like_count=Count("like")).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


class MyProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = MyProfileSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class MyPostViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        author = self.request.user.profile
        return Post.objects.filter(author=author).order_by('-created_at')

    def perform_create(self, serializer):
        author = self.request.user.profile
        serializer.save(author=author)


class LatestPostsView(generics.ListAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Post.objects.filter(author__in=user_profile.following.all()).order_by('-created_at')


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


class LikeView(APIView):
    def post(self, request: Request) -> Response:

        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():

            try:
                post = Post.objects.get(pk=request.data["post_id"])
            except Post.DoesNotExist:
                return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

            user_profile = request.user.profile
            if user_profile in post.like.all():
                post.like.remove(user_profile)
                message = "removed the like"
            else:
                post.like.add(user_profile)
                message = "like"

            return Response({"detail": f"You have {message} this post."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(profile=profile)
