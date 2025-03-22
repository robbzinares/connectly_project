from django.urls import path
from .views import (
    get_csrf_token,
    post_list,
    post_detail,  # Or PostDetailView if using class-based views
    user_list,
    create_user,
    CreatePostView,
    ProtectedView,
    NewsFeedView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("csrf-token/", get_csrf_token),
    path("posts/", post_list, name="post-list"),
    path("posts/<int:pk>/", post_detail, name="post-detail"),  # Keep only one
    path("users/", user_list, name="user-list"),
    path("users/create/", create_user, name="create-user"),
    path("api-token-auth/", obtain_auth_token, name="api-token-auth"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("create-post/", CreatePostView.as_view(), name="create-post"),  # Factory-based Post Creation
    path("feed/", NewsFeedView.as_view(), name="news-feed"),
]