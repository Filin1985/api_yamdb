from rest_framework import permissions


class IsAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin' or request.user.is_superuser)

class IsAdminOrModeratorOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == 'admin' or request.user.role == 'moderator')

class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.role == 'admin':
            return True
        else:
            return False