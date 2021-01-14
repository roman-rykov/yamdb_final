from django.db.models.expressions import F
from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == 'moderator' or request.user.is_superuser
        else:
            return False

class IsAdministrator(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == 'admin' or request.user.is_superuser
        else:
            return False

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_anonymous:
            return request.user.role == 'user'
        else:
            return False