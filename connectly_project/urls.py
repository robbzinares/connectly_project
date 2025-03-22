from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path("admin/", admin.site.urls),  # Django admin panel
    path("api/", include("posts.urls")),  # Include posts app URLs
    path("api-auth/", include("rest_framework.urls")),  # DRF login/logout views
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),  # Token Authentication
    path("api/", include("comments.urls")),
    path("api/", include("likes.urls")),
    path("api/users/", include("users.urls")),
    path('auth/', include('allauth.urls')),
]