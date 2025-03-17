from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, min_length=5)  # Validate title length
    content = serializers.CharField(min_length=10)  # Validate content length
    user = serializers.ReadOnlyField(source='user.username')  # Display username instead of ID

    class Meta:
        model = Post
        fields = '__all__'

    def validate_title(self, value):
        """Ensure the title isn't just numbers."""
        if value.isdigit():
            raise serializers.ValidationError("Title cannot be only numbers.")
        return value

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)  # Include posts in user response

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'posts']