from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """Allow only admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsPostOwnerOrAdmin(BasePermission):
    """Allow only post owners or admins to modify posts."""
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.user.role == "admin"
