from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminForCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return 'A' == request.user.customUser.role

