from django.urls import path
from .views import PostDetailView
from .views import ProtectedView
from .views import (
    post_list, post_detail, get_csrf_token, create_user, user_list
)
from rest_framework.authtoken.views import obtain_auth_token  # Import DRF token authentication

urlpatterns = [
    path("csrf-token/", get_csrf_token),
    path("posts/", post_list, name="post-list"),
    path("posts/<int:pk>/", post_detail, name="post-detail"),
    path("users/", user_list, name="user-list"),
    path("users/create/", create_user, name="create-user"),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),  # Token Authentication
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('protected/', ProtectedView.as_view(), name='protected'),
]