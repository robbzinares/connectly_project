from django.urls import path
from .views import like_post, unlike_post, like_count

urlpatterns = [
    path("posts/<int:post_id>/like/", like_post, name="like_post"),
    path("posts/<int:post_id>/unlike/", unlike_post, name="unlike_post"),
    path("posts/<int:post_id>/likes/count/", like_count, name="like_count"),
]
