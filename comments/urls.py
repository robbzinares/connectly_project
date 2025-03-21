from django.urls import path
from .views import add_comment, list_comments

urlpatterns = [
    path("posts/<int:post_id>/comment/", add_comment, name="add_comment"),
    path("posts/<int:post_id>/comments/", list_comments, name="list_comments"),
]
