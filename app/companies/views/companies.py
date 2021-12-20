"""Companies views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from app.companies.models import Company, Employee

# Permissions
from app.companies.permissions import IsSuperUser, IsCompanyAdmin
from rest_framework.permissions import IsAuthenticated

# Serializer
from app.companies.serializers import (
    CompanyModelSerializer,
    CreateCompanySerializer,
    EmployeeModelSerializer,
    InviteEmployee
)
from app.users.serializers import UserSignUpSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company Viewset.
    Handle the creation, updating, obtaining,
    listing and deletion of companies.
    """

    queryset = Company.objects.all()
    lookup_field = 'name'

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['create', 'create_admin']:
            permissions = [IsSuperUser]
        elif self.action in [
            'update', 'partial_update', 'destroy', 'invite_employee']:
            permissions = [IsCompanyAdmin]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == 'create':
            return CreateCompanySerializer
        return CompanyModelSerializer

    @action(detail=True, methods=['post'])
    def create_admin(self, request, *args, **kwargs):
        """Create user admin of the company."""
        company = self.get_object()
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_admin = serializer.save()

        # Update user admin
        user_admin.company = company
        user_admin.save()

        # Add company admin
        company.admin = user_admin
        company.save()
        data = {
            'company': CompanyModelSerializer(company).data,
            'message': 'An invitation has been sent to the user to be admin to the email you provided'
            }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def invite_employee(self, request, *args, **kwargs):
        """Invite an employee to register in the application."""
        company = self.get_object()
        serializer = InviteEmployee(data=request.data, context={'company': company})
        serializer.is_valid(raise_exception=True)
        employee_email = serializer.save()
        data = {'message': f'Successful sending of the invitation to the email {employee_email}.'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True)
    def employees(self, request, *args, **kwargs):
        """List employees of a company."""
        company = self.get_object()
        employees = Employee.objects.filter(company=company)
        data = EmployeeModelSerializer(employees, many=True).data
        return Response(data, status=status.HTTP_200_OK)