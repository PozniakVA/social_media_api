from django.db.models import Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
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
from social_media.permissions import IsAdminOrAuthenticatedReadOnly
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
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        elif self.action == "retrieve":
            return ProfileDetailSerializer
        return ProfileSerializer

    def get_queryset(self):

        nickname = self.request.query_params.get("nickname")
        queryset = self.queryset

        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)

        return queryset.order_by("-user__date_joined")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "nickname",
                type=OpenApiTypes.STR,
                description="Filter by nickname (ex. ?nickname=test1)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


class PostViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Post.objects.annotate(like_count=Count("like"))

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        elif self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):

        name = self.request.query_params.get("name")
        author = self.request.query_params.get("author")
        hashtag = self.request.query_params.get("hashtag")
        queryset = self.queryset

        if hashtag:
            queryset = queryset.filter(hashtag__name__icontains=hashtag)
        if name:
            queryset = Post.objects.filter(name__icontains=name)
        if author:
            queryset = Post.objects.filter(author__nickname__icontains=author)

        return queryset.order_by("-created_at")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtag",
                type=OpenApiTypes.STR,
                description="Filter by hashtag name (ex. ?hashtag=sport)",
            ),
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by post name (ex. ?name=test)",
            ),
            OpenApiParameter(
                "author",
                type=OpenApiTypes.STR,
                description="Filter by author nickname (ex. ?author=test)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [IsAdminOrAuthenticatedReadOnly]

    def get_queryset(self):
        name = self.request.query_params.get("name")
        queryset = self.queryset

        if name:
            queryset = Hashtag.objects.filter(name__icontains=name)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by hashtag name (ex. ?name=sport)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


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
        queryset = Post.objects.filter(author=author)

        name = self.request.query_params.get("name")
        hashtag = self.request.query_params.get("hashtag")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if hashtag:
            queryset = queryset.filter(hashtag__name__icontains=hashtag)

        return queryset.order_by("-created_at")

    def perform_create(self, serializer):
        author = self.request.user.profile
        serializer.save(author=author)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by post name (ex. ?name=test)",
            ),
            OpenApiParameter(
                "hashtag",
                type=OpenApiTypes.STR,
                description="Filter by hashtag name (ex. ?hashtag=sport)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


class LatestPostsView(generics.ListAPIView):
    serializer_class = PostDetailSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = Post.objects.filter(author__in=user_profile.following.all())

        name = self.request.query_params.get("name")
        author = self.request.query_params.get("author")
        hashtag = self.request.query_params.get("hashtag")

        if hashtag:
            queryset = queryset.filter(hashtag__name__icontains=hashtag)
        if name:
            queryset = Post.objects.filter(name__icontains=name)
        if author:
            queryset = Post.objects.filter(author__nickname__icontains=author)

        return queryset.order_by("-created_at")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtag",
                type=OpenApiTypes.STR,
                description="Filter by hashtag name (ex. ?hashtag=sport)",
            ),
            OpenApiParameter(
                "name",
                type=OpenApiTypes.STR,
                description="Filter by post name (ex. ?name=test)",
            ),
            OpenApiParameter(
                "author",
                type=OpenApiTypes.STR,
                description="Filter by author nickname (ex. ?author=test1)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


class MyFollowersView(generics.ListAPIView):
    serializer_class = ProfileListSerializer

    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = user_profile.followers.all()

        nickname = self.request.query_params.get("nickname")
        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)

        return queryset.order_by("nickname")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "nickname",
                type=OpenApiTypes.STR,
                description="Filter by nickname (ex. ?nickname=test1)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


class MyFollowingView(generics.ListAPIView):
    serializer_class = ProfileListSerializer


    def get_queryset(self):
        user_profile = self.request.user.profile
        queryset = user_profile.following.all().order_by("nickname")

        nickname = self.request.query_params.get("nickname")
        if nickname:
            queryset = queryset.filter(nickname__icontains=nickname)

        return queryset.order_by("nickname")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "nickname",
                type=OpenApiTypes.STR,
                description="Filter by nickname (ex. ?nickname=test1)",
            )
        ]
    )
    def list(self, request):
        return super().list(request)


@extend_schema(
    request=FollowAndUnfollowSerializer,
    responses={200: OpenApiResponse(description="Successfully followed a user")}
)
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
                return Response({"detail": f"You have followed {profile.nickname}."}, status=status.HTTP_200_OK)

            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=FollowAndUnfollowSerializer,
    responses={200: OpenApiResponse(description="Successfully unfollowed a user")}
)
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


@extend_schema(
    request=LikeSerializer,
    responses={200: OpenApiResponse(description="Successfully like or un-like this post")}
)
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
