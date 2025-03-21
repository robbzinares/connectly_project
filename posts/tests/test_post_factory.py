from django.test import TestCase
from posts.models import Post
from posts.factories.post_factory import PostFactory

class PostFactoryTest(TestCase):
    def setUp(self):
        """Set up test data before each test."""
        self.default_metadata = {"file_size": 500, "duration": 10}

    def test_create_text_post(self):
        """Test creating a valid text post."""
        post = PostFactory.create_post(post_type="text", title="Test Text Post", content="Hello World!")
        self.assertEqual(post.post_type, "text")
        self.assertEqual(post.title, "Test Text Post")

    def test_create_image_post_with_valid_metadata(self):
        """Test creating an image post with correct metadata."""
        post = PostFactory.create_post(post_type="image", title="Test Image", metadata={"file_size": 1024})
        self.assertEqual(post.post_type, "image")
        self.assertEqual(post.metadata["file_size"], 1024)

    def test_create_video_post_with_valid_metadata(self):
        """Test creating a video post with required metadata."""
        post = PostFactory.create_post(post_type="video", title="Test Video", metadata={"duration": 120})
        self.assertEqual(post.post_type, "video")
        self.assertEqual(post.metadata["duration"], 120)

    def test_create_image_post_without_metadata(self):
        """Test creating an image post without required metadata (should fail)."""
        with self.assertRaises(ValueError) as context:
            PostFactory.create_post(post_type="image", title="Invalid Image Post")
        self.assertEqual(str(context.exception), "Image posts require 'file_size' in metadata")

    def test_create_video_post_without_metadata(self):
        """Test creating a video post without required metadata (should fail)."""
        with self.assertRaises(ValueError) as context:
            PostFactory.create_post(post_type="video", title="Invalid Video Post")
        self.assertEqual(str(context.exception), "Video posts require 'duration' in metadata")

    def test_invalid_post_type(self):
        """Test creating a post with an invalid type (should fail)."""
        with self.assertRaises(ValueError) as context:
            PostFactory.create_post(post_type="invalid", title="Invalid Post")
        self.assertEqual(str(context.exception), "Invalid post type")