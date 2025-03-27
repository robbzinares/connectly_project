from rest_framework.permissions import BasePermission

class IsPostAuthor(BasePermission):
    """
    Custom permission to allow only authors of a post to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user  # Fix: Use 'author' instead of 'user'

class IsAdmin(BasePermission):
    """
    Custom permission to allow only admin users to perform certain actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == "admin"

class IsPostOwnerOrAdmin(BasePermission):
    """
    Custom permission to allow post owners or admins to modify posts.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.profile.role == "admin"

class CanViewPost(BasePermission):
    """
    Custom permission to allow access to public posts or private posts owned by the user.
    """
    def has_object_permission(self, request, view, obj):
        if obj.privacy == "public":
            return True  # Public posts are accessible to everyone
        return obj.author == request.user  # Private posts are only accessible to the owner
