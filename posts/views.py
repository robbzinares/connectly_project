from contextvars import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from posts.serializers import PostSerializer, UserSerializer
from .models import Post
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthor
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.authentication import TokenAuthentication
from .factories.post_factory import PostFactory
from .singletons.logger_singleton import LoggerSingleton
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.cache import cache


# CSRF Token View
@api_view(["GET"])
@permission_classes([AllowAny])  # Allow public access
def get_csrf_token(request):
    return Response({"csrfToken": get_token(request)})

# CREATE & GET ALL POSTS
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Allow public access for testing
def post_list(request):
    if request.method == 'GET':  # Retrieve all posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':  # Create a new post (no user authentication required)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET, UPDATE, DELETE A SINGLE POST
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])  # Allow public access for testing
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':  # Retrieve a single post
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method == 'PUT':  # Full update
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':  # Partial update
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # Delete a post
        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)

# CREATE USER
@api_view(["POST"])
@permission_classes([AllowAny])  # Allow public access for testing
def create_user(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")

    if not username or not email or not password:
        return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

# LIST ALL USERS
@api_view(["GET"])
@permission_classes([AllowAny])  # Allow public access for testing
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is not None:
        # Generate or get token for authenticated user
        token, created = Token.objects.get_or_create(user=user)
        return Response({"message": "Authentication successful!", "token": token.key})
    else:
        return Response({"error": "Invalid credentials."}, status=400)
    
@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated, IsPostAuthor])  # ✅ Apply permissions
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    # This will automatically check if the user is the author
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    if request.method in ['PUT', 'PATCH']:  # Update post
        serializer = PostSerializer(post, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':  # Delete post
        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class PostDetailView(APIView):
    """
    Retrieve, update, or delete a post instance.
    """
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get_object(self, pk, request):
        try:
            post = Post.objects.get(pk=pk)
            # Enforce privacy: Only owner can access private posts
            if post.privacy == "private" and post.author != request.user:
                raise Http404
            return post
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk, request)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk, request)
        self.check_object_permissions(request, post)  # Ensures only author can edit
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = self.get_object(pk, request)
        self.check_object_permissions(request, post)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk, request)
        self.check_object_permissions(request, post)
        post.delete()
        return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)
    
class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated!"})  
    
class CreatePostView(APIView):
    def post(self, request):
        data = request.data
        try:
            post = PostFactory.create_post(
                post_type=data['post_type'],
                title=data['title'],
                content=data.get('content', ''),
                metadata=data.get('metadata', {})
            )
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

logger = LoggerSingleton().get_logger()
logger.info("API initialized successfully.")


class NewsFeedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = request.GET.get("page", 1)
        try:
            page = int(page)  # Convert page to integer early
        except ValueError:
            page = 1  # Default to page 1 if invalid input

        # Generate cache key with latest post timestamp
        latest_post = Post.objects.order_by("-created_at").first()
        latest_timestamp = latest_post.created_at.timestamp() if latest_post else 0
        cache_key = f"news_feed_{request.user.id}_page_{page}_{latest_timestamp}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        posts = Post.objects.filter(
            Q(privacy="public") | Q(author=request.user)
        ).order_by("-created_at").select_related("author")

        paginator = Paginator(posts, 10)

        # 🔥 **Fix: Handle out-of-range page numbers manually**
        total_pages = paginator.num_pages
        if page > total_pages:  # If requested page is greater than total available pages
            return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            paginated_posts = paginator.page(page)
        except PageNotAnInteger:
            page = 1
            paginated_posts = paginator.page(page)
        except EmptyPage:  # 🚀 Redundant now, but still good practice
            return Response({"error": "Page not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(paginated_posts, many=True)
        response_data = {
            "posts": serializer.data,
            "page": page,
            "total_pages": total_pages
        }

        if paginated_posts:  # Cache only when there is valid data
            cache.set(cache_key, response_data, timeout=300)

        return Response(response_data)