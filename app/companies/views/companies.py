"""Companies views."""

# Django REST framework
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Models
from app.companies.models import Company

# Serializer
from app.companies.serializers import CompanyModelSerializer, CreateCompanySerializer
from app.users.serializers import UserSignUpSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    Company Viewset.
    Handle the creation, updating, obtaining,
    listing and deletion of companies.
    """

    queryset = Company.objects.all()
    lookup_field = 'name'

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
