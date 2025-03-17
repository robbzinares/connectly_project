"""
URL configuration for connectly_project project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin panel
    path("api/", include("posts.urls")),  # ✅ Includes both posts & users endpoints
    path("api-auth/", include("rest_framework.urls")),  # DRF login/logout views
]