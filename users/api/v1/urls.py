from django.contrib.auth import get_user_model
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet)


User = get_user_model()

urlpatterns = [
    path("", include(router.urls)),
    path("", include("djoser.urls.jwt")),
]
