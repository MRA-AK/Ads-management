from django.contrib import admin

from .models import Ad, Comment


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Registering the Ad model in the admin panel."""

    list_display = ["title", "user", "created_at", "updated_at"]
    search_fields = ["title", "description"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Registering the Comment model in the admin panel."""

    list_display = ["ad", "user", "created_at", "updated_at"]
    search_fields = ["ad__title", "comment_message"]
