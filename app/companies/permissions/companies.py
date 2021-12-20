"""Companies permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    """Allow access only to superuser."""

    def has_permission(self, request, view):
        return request.user.is_superuser == True


class IsCompanyAdmin(BasePermission):
    """Allow access only to company admin."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.admin