from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ads.models import Ad, Comment


class CommentSerializer(serializers.ModelSerializer):
    """Comments instance serializer"""

    class Meta:
        model = Comment
        fields = ["id", "user", "ad", "comment_message", "created_at", "updated_at"]
        read_only_fields = ["user", "created_at", "updated_at"]

    def validate(self, attrs):
        """
        Check if the user has already commented on the ad.
        """
        user = self.context["request"].user
        ad = attrs["ad"]

        if Comment.objects.filter(user=user, ad=ad).exists():
            raise ValidationError("You have already commented on this ad.")

        return attrs


class AdSerializer(serializers.ModelSerializer):
    """Ads instance serializer"""

    comments = serializers.SerializerMethodField()

    class Meta:
        model = Ad
        fields = ["id", "user", "title", "description", "created_at", "updated_at", "comments"]
        read_only_fields = ["user", "created_at", "updated_at"]

    def get_comments(self, obj):
        comments = Comment.objects.filter(ad=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data
