from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.post.title}"

    def is_visible_to(self, user):
        """
        Check if the comment is visible based on the post's privacy settings.
        - Public posts: Everyone can see comments.
        - Private posts: Only the post owner and comment author can see comments.
        """
        if self.post.privacy == "public":
            return True
        return self.post.author == user or self.user == user
