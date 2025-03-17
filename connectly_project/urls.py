from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin panel
    path("api/", include("posts.urls")),  # Include posts app URLs
    path("api-auth/", include("rest_framework.urls")),  # DRF login/logout views
]