from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    POST_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    PRIVACY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        # Add 'friends' if you implement friends-only visibility
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")  # Ensure author field exists
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    metadata = models.JSONField(null=True, blank=True)
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICES, default='public')  # NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post_type} - {self.title}"
