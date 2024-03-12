from rest_framework import serializers

from ads.models import Ad


class AdSerializer(serializers.ModelSerializer):
    """Ads instance serializer"""

    class Meta:
        model = Ad
        fields = ["id", "user", "title", "description", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]
