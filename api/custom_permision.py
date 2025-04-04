from rest_framework import permissions
from rest_framework import exceptions
class AuthorizedAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get("Authorization")
        if not token:
            return False
        if token != "1012":
            raise exceptions.PermissionDenied("Invalid token")
        return True