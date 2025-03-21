from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Like
from posts.models import Post
from .serializers import LikeSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user already liked the post
    if Like.objects.filter(user=request.user, post=post).exists():
        return Response({"error": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

    like = Like.objects.create(user=request.user, post=post)
    serializer = LikeSerializer(like)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    try:
        like = Like.objects.get(user=request.user, post_id=post_id)
    except Like.DoesNotExist:
        return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

    like.delete()
    return Response({"message": "Like removed"}, status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def like_count(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    count = post.likes.count()
    return Response({"post_id": post_id, "like_count": count})
