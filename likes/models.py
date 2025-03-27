from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")  # Ensures a user can only like a post once

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"

    def is_visible_to(self, user):
        """
        Determines if the like should be visible to a specific user based on post privacy.
        - Public posts: Everyone can see likes.
        - Private posts: Only the post owner and the user who liked can see the like.
        """
        if self.post.privacy == "public":
            return True
        return self.post.author == user or self.user == user
