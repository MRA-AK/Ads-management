from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="ADs management",
        default_version="v1",
        description="A platform where users can post advertisements and comment on other people's ads.",
        terms_of_service="",
        contact=openapi.Contact(email="mra1373@gmail.com"),
        # license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("admin/", admin.site.urls),
    # API endpoints
    path("users/api/v1/", include("users.api.v1.urls")),
    path("social/api/v1/", include("ads.api.v1.urls")),
]

# Swagger API documentation
urlpatterns.append(path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger"))
# Redoc API documentation
urlpatterns.append(path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"))
