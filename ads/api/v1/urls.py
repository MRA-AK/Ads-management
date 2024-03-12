from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ads.api.v1 import views

router = DefaultRouter()
router.register("ads", views.AdViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
