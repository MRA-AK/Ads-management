from rest_framework import generics, permissions, viewsets

from ads.models import Ad, Comment

from .paginations import DefaultPageNumberPagination
from .serializers import AdSerializer, CommentSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.prefetch_related("comments").all()
    serializer_class = AdSerializer
    pagination_class = DefaultPageNumberPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Add user field based on requested user"""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class CommentCreateAPIView(generics.CreateAPIView):
    """Create a new comment"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
