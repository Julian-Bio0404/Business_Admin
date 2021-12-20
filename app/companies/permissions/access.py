"""Access permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from app.companies.models import Employee


class IsAdminPoint(BasePermission):
    """Allow access only to company admin."""

    def has_permission(self, request, view):
        """Check that request user is company admin."""
        company = view.company
        return request.user == company.admin
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.company.admin


class IsAdminOrEmployee(BasePermission):

    def has_permission(self, request, view):
        employee = Employee.objects.filter(
            company=view.company, user=request.user)
        return request.user == view.company.admin or employee.exists()
    
    def has_object_permission(self, request, view, obj):
        admin = obj.access_point.company.admin
        return request.user == admin


class IsCompanyEmployee(BasePermission):
    """Allow access only to company employess or admin."""

    def has_object_permission(self, request, view, obj):
        employee = Employee.objects.filter(
            company=obj.company, user=request.user)
        return employee.exists()


class IsEmployeeHour(BasePermission):
    """
    Allows access only to the employee who
    appears in the access time or to the company admin.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in [obj.user, obj.company.admin]
