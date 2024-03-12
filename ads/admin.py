from django.contrib import admin

from .models import Ad


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Registering the Ad model in the admin panel."""

    list_display = ["title", "user", "created_at", "updated_at"]
    search_fields = ["title", "description"]
