from django.contrib import admin
from django.contrib.auth import get_user_model

from social_media.models import (
    Profile,
    Post,
    Hashtag
)

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline,)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    pass
