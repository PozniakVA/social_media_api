from django.contrib import admin

from social_media.models import (
    Profile,
    Post,
    Follow,
    Hashtag
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    pass


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    pass
