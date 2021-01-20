from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False  # иначе в тестах кинется AttributeError: 'AnonymousUser' object has no attribute 'is_admin'
        return request.user.is_admin or request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return request.user.is_admin or request.user.is_superuser


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        return request.user.is_moderator or request.user.is_admin

    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        return request.user.is_moderator or request.user.is_admin


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS
