from django.contrib import admin

from social_media.models import (
    Post,
    Hashtag
)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    pass
