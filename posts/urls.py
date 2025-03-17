from django.urls import path
from .views import hello_world, post_list, post_detail, get_csrf_token
from .views import create_user, user_list

urlpatterns = [
    path("csrf-token/", get_csrf_token),  
    path("hello/", hello_world, name="hello-world"),
    path("posts/", post_list, name="post-list"),  # GET all, POST new
    path("posts/<int:pk>/", post_detail, name="post-detail"),  # GET, PUT, DELETE a single post
    path("users/", user_list, name="user-list"),  # GET all users
    path("users/create/", create_user, name="create-user"),  # Create a new user
]